from __future__ import annotations

import os
import time

from thohor_validation.core.io import read_json, write_json
from thohor_validation.core.models import FactorSignal, NormalizedToolOutput, ToolRunResult
from thohor_validation.core.paths import raw_output_path, sample_dir, sample_video

from .import_adapter import ImportOnlyAdapter


class AWSRekognitionAdapter(ImportOnlyAdapter):
    name = "aws_rekognition"

    def __init__(self) -> None:
        super().__init__(self.name)

    def run(self, sample_id: str) -> ToolRunResult:
        imported = super().run(sample_id)
        if imported.status == "imported":
            return imported
        bucket = os.getenv("AWS_S3_BUCKET")
        region = os.getenv("AWS_REGION", "us-east-1")
        if not bucket:
            return ToolRunResult(tool=self.name, sample_id=sample_id, status="skipped", message="AWS_S3_BUCKET is not configured. Export Rekognition JSON or configure S3/Rekognition.")
        video_path = sample_video(sample_id)
        if not video_path.exists():
            return ToolRunResult(tool=self.name, sample_id=sample_id, status="skipped", message=f"Missing video: {video_path}")

        import boto3

        s3_key = f"thohor-validation/{sample_id}/input.mp4"
        s3 = boto3.client("s3", region_name=region)
        rekognition = boto3.client("rekognition", region_name=region)
        s3.upload_file(str(video_path), bucket, s3_key)

        video = {"S3Object": {"Bucket": bucket, "Name": s3_key}}
        label_job = rekognition.start_label_detection(Video=video)["JobId"]
        face_job = rekognition.start_face_detection(Video=video)["JobId"]

        payload = {
            "tool": self.name,
            "sample_id": sample_id,
            "s3_bucket": bucket,
            "s3_key": s3_key,
            "label_job_id": label_job,
            "face_job_id": face_job,
            "label_detection": _poll_paginated_job(
                rekognition, "get_label_detection", label_job, result_key="Labels"
            ),
            "face_detection": _poll_paginated_job(
                rekognition, "get_face_detection", face_job, result_key="Faces"
            ),
            "image_face_attributes": _detect_frame_face_attributes(rekognition, sample_id),
        }
        path = raw_output_path(self.name, sample_id)
        write_json(path, payload)
        return ToolRunResult(tool=self.name, sample_id=sample_id, status="ok", raw_path=str(path))

    def normalize(self, sample_id: str) -> NormalizedToolOutput:
        raw = read_json(raw_output_path(self.name, sample_id))
        labels = raw.get("label_detection", {}).get("items", [])
        faces = raw.get("face_detection", {}).get("items", [])
        face_attributes = raw.get("image_face_attributes", {}).get("items", [])
        face_timestamps = {item.get("Timestamp") for item in faces if item.get("Timestamp") is not None}
        label_names = []
        for item in labels:
            label = item.get("Label", {})
            name = label.get("Name")
            confidence = label.get("Confidence")
            if name and confidence and confidence >= 70:
                label_names.append(name)

        gaze = _summarize_face_pose(faces)
        expression = _summarize_face_attributes(face_attributes, raw.get("duration_seconds"))

        return NormalizedToolOutput(
            tool=self.name,
            sample_id=sample_id,
            factors=[
                FactorSignal(
                    factor_id="face_detection",
                    factor_name="Face detection",
                    axis="لغة الجسد",
                    value={"detections": len(faces), "unique_timestamps": len(face_timestamps)},
                    score=90 if faces else 0,
                    confidence=0.75 if faces else 0.2,
                ),
                FactorSignal(
                    factor_id="activity_labels",
                    factor_name="General video labels / activities",
                    axis="لغة الجسد",
                    value={"label_count": len(label_names), "examples": sorted(set(label_names))[:20]},
                    score=80 if label_names else 0,
                    confidence=0.65 if label_names else 0.2,
                ),
                FactorSignal(
                    factor_id="gaze_direction",
                    factor_name="Head/gaze direction proxy",
                    axis="لغة الجسد",
                    value=gaze,
                    score=gaze.get("frontal_score"),
                    confidence=0.55 if faces else 0.0,
                    evidence=["Computed from AWS face pose yaw/pitch as a gaze-direction proxy."],
                ),
                FactorSignal(
                    factor_id="gaze_distribution",
                    factor_name="Gaze distribution proxy",
                    axis="لغة الجسد",
                    value={
                        "left_count": gaze.get("left_count"),
                        "center_count": gaze.get("center_count"),
                        "right_count": gaze.get("right_count"),
                    },
                    score=gaze.get("distribution_score"),
                    confidence=0.5 if faces else 0.0,
                    evidence=["Computed from left/center/right head pose distribution."],
                ),
                FactorSignal(
                    factor_id="eye_contact_stability",
                    factor_name="Eye contact stability proxy",
                    axis="لغة الجسد",
                    value={"frontal_rate": gaze.get("frontal_rate")},
                    score=gaze.get("stability_score"),
                    confidence=0.5 if faces else 0.0,
                    evidence=["Computed from percentage of face detections with mostly frontal yaw/pitch."],
                ),
                FactorSignal(
                    factor_id="facial_expression",
                    factor_name="Facial expression proxy",
                    axis="لغة الجسد",
                    value=expression,
                    score=expression.get("expression_score"),
                    confidence=0.55 if face_attributes else 0.0,
                    evidence=["Computed from AWS DetectFaces emotions on sampled frames."],
                ),
                FactorSignal(
                    factor_id="smile_rate",
                    factor_name="Smile rate from sampled frames",
                    axis="لغة الجسد",
                    value=expression.get("smile_rate_per_minute"),
                    score=expression.get("smile_rate_score"),
                    confidence=0.55 if face_attributes else 0.0,
                    evidence=["Computed from AWS DetectFaces Smile attribute on sampled frames."],
                ),
                FactorSignal(
                    factor_id="smile_authenticity",
                    factor_name="Smile authenticity proxy",
                    axis="لغة الجسد",
                    value=expression.get("smile_confidence_mean"),
                    score=expression.get("smile_authenticity_score"),
                    confidence=0.45 if face_attributes else 0.0,
                    evidence=["Proxy uses AWS smile confidence; not a full Duchenne smile analysis."],
                ),
                FactorSignal(
                    factor_id="blink_rate",
                    factor_name="Blink rate / eyes closed proxy",
                    axis="لغة الجسد",
                    value=expression.get("blink_rate_per_minute"),
                    score=expression.get("blink_rate_score"),
                    confidence=0.45 if face_attributes else 0.0,
                    evidence=["Proxy counts sampled frames where eyes are not open."],
                ),
            ],
        )


def _poll_paginated_job(client, method_name: str, job_id: str, result_key: str) -> dict:
    method = getattr(client, method_name)
    status = "IN_PROGRESS"
    for _ in range(90):
        response = method(JobId=job_id)
        status = response.get("JobStatus", status)
        if status in {"SUCCEEDED", "FAILED"}:
            break
        time.sleep(5)

    if status != "SUCCEEDED":
        return {"status": status, "items": []}

    items = []
    next_token = None
    while True:
        kwargs = {"JobId": job_id}
        if next_token:
            kwargs["NextToken"] = next_token
        response = method(**kwargs)
        items.extend(response.get(result_key, []))
        next_token = response.get("NextToken")
        if not next_token:
            break
    return {"status": status, "items": items}


def _detect_frame_face_attributes(client, sample_id: str) -> dict:
    frames = sorted((sample_dir(sample_id) / "frames").glob("*.jpg"))
    if not frames:
        return {"items": []}
    sampled = frames[:: max(1, len(frames) // 16)]
    items = []
    for frame in sampled[:20]:
        try:
            response = client.detect_faces(
                Image={"Bytes": frame.read_bytes()},
                Attributes=["ALL"],
            )
        except Exception as exc:
            items.append({"frame": frame.name, "error": str(exc)})
            continue
        items.append({"frame": frame.name, "faces": response.get("FaceDetails", [])})
    return {"items": items}


def _summarize_face_pose(faces: list[dict]) -> dict:
    if not faces:
        return {
            "frontal_rate": 0.0,
            "frontal_score": 0.0,
            "distribution_score": 0.0,
            "stability_score": 0.0,
        }
    left = center = right = frontal = 0
    for item in faces:
        pose = item.get("Face", {}).get("Pose", {})
        yaw = float(pose.get("Yaw", 0.0))
        pitch = float(pose.get("Pitch", 0.0))
        if yaw < -12:
            left += 1
        elif yaw > 12:
            right += 1
        else:
            center += 1
        if abs(yaw) <= 25 and abs(pitch) <= 18:
            frontal += 1

    total = len(faces)
    frontal_rate = frontal / total
    side_balance_penalty = abs(left - right) / max(left + right, 1) * 20
    center_ratio = center / total
    distribution_score = max(50.0, min(100.0, 70 + center_ratio * 25 - side_balance_penalty))
    frontal_score = _score_frontal_rate(frontal_rate)
    return {
        "frontal_rate": round(frontal_rate, 3),
        "left_count": left,
        "center_count": center,
        "right_count": right,
        "frontal_score": frontal_score,
        "distribution_score": round(distribution_score, 2),
        "stability_score": frontal_score,
    }


def _score_frontal_rate(rate: float) -> float:
    if rate >= 0.9:
        return 95.0
    if rate >= 0.8:
        return 85.0
    if rate >= 0.65:
        return 75.0
    if rate >= 0.5:
        return 65.0
    return 50.0


def _summarize_face_attributes(items: list[dict], duration_seconds: float | None = None) -> dict:
    faces = []
    for item in items:
        faces.extend(item.get("faces", []))
    if not faces:
        return {
            "expression_score": 0.0,
            "smile_rate_score": 0.0,
            "smile_authenticity_score": 0.0,
            "blink_rate_score": 0.0,
        }
    smile_faces = [
        face for face in faces if face.get("Smile", {}).get("Value") and face.get("Smile", {}).get("Confidence", 0) >= 70
    ]
    eyes_closed = [
        face for face in faces if not face.get("EyesOpen", {}).get("Value", True)
    ]
    positive_emotion_count = 0
    for face in faces:
        emotions = face.get("Emotions", [])
        top = max(emotions, key=lambda item: item.get("Confidence", 0), default={})
        if top.get("Type") in {"HAPPY", "CALM", "SURPRISED"}:
            positive_emotion_count += 1
    minutes = max((duration_seconds or 60) / 60, 0.001)
    smile_rate = len(smile_faces) / minutes
    blink_rate = len(eyes_closed) / minutes
    smile_confidence = (
        sum(face.get("Smile", {}).get("Confidence", 0) for face in smile_faces) / len(smile_faces)
        if smile_faces
        else 0.0
    )
    expression_rate = positive_emotion_count / len(faces)
    return {
        "face_attribute_frames": len(items),
        "face_attribute_detections": len(faces),
        "positive_expression_rate": round(expression_rate, 3),
        "expression_score": round(max(50.0, min(100.0, expression_rate * 100)), 2),
        "smile_rate_per_minute": round(smile_rate, 2),
        "smile_rate_score": _score_smile_rate(smile_rate),
        "smile_confidence_mean": round(smile_confidence, 2),
        "smile_authenticity_score": round(max(50.0, min(100.0, smile_confidence)), 2)
        if smile_faces
        else 50.0,
        "blink_rate_per_minute": round(blink_rate, 2),
        "blink_rate_score": _score_blink_rate(blink_rate),
    }


def _score_smile_rate(smile_rate: float) -> float:
    if 0.5 <= smile_rate <= 2:
        return 95.0
    if 2 < smile_rate <= 3:
        return 85.0
    if 0 < smile_rate < 0.5 or 3 < smile_rate <= 4:
        return 75.0
    return 60.0


def _score_blink_rate(blink_rate: float) -> float:
    if 10 <= blink_rate <= 20:
        return 100.0
    if 8 <= blink_rate <= 25:
        return 85.0
    if 6 <= blink_rate <= 30:
        return 70.0
    return 50.0
