from __future__ import annotations

import math

from thohor_validation.core.io import read_json, write_json
from thohor_validation.core.models import FactorSignal, NormalizedToolOutput, ToolRunResult
from thohor_validation.core.paths import PROJECT_ROOT, raw_output_path, sample_video

from .base import ToolAdapter


class MediaPipeAdapter(ToolAdapter):
    name = "mediapipe"

    def run(self, sample_id: str) -> ToolRunResult:
        import mediapipe as mp

        video_path = sample_video(sample_id)
        if not video_path.exists():
            raise FileNotFoundError(video_path)

        if _task_models_available():
            return self._run_tasks(sample_id)
        if hasattr(mp, "solutions"):
            return self._run_legacy_solutions(sample_id)
        return self._run_opencv_fallback(sample_id)

    def _run_tasks(self, sample_id: str) -> ToolRunResult:
        import cv2
        import mediapipe as mp
        from mediapipe.tasks import python
        from mediapipe.tasks.python import vision

        video_path = sample_video(sample_id)
        cap = cv2.VideoCapture(str(video_path))
        fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
        duration_seconds = frame_count / fps if frame_count else None
        sample_every = max(1, int(fps // 2))

        base = python.BaseOptions
        mode = vision.RunningMode.IMAGE
        pose_options = vision.PoseLandmarkerOptions(
            base_options=base(model_asset_path=str(_model_path("pose_landmarker_lite.task"))),
            running_mode=mode,
        )
        hand_options = vision.HandLandmarkerOptions(
            base_options=base(model_asset_path=str(_model_path("hand_landmarker.task"))),
            running_mode=mode,
            num_hands=2,
        )
        face_options = vision.FaceLandmarkerOptions(
            base_options=base(model_asset_path=str(_model_path("face_landmarker.task"))),
            running_mode=mode,
            num_faces=1,
            output_face_blendshapes=True,
        )

        frames: list[dict] = []
        previous_hand_centers: list[tuple[float, float]] = []
        previous_pose_center: tuple[float, float] | None = None
        index = 0

        with (
            vision.PoseLandmarker.create_from_options(pose_options) as pose,
            vision.HandLandmarker.create_from_options(hand_options) as hands,
            vision.FaceLandmarker.create_from_options(face_options) as face,
        ):
            while True:
                ok, frame = cap.read()
                if not ok:
                    break
                if index % sample_every != 0:
                    index += 1
                    continue

                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
                pose_result = pose.detect(image)
                hand_result = hands.detect(image)
                face_result = face.detect(image)

                pose_landmarks = pose_result.pose_landmarks[0] if pose_result.pose_landmarks else []
                hand_landmarks = hand_result.hand_landmarks or []
                face_blendshapes = face_result.face_blendshapes[0] if face_result.face_blendshapes else []

                hand_centers = [_landmark_center(hand) for hand in hand_landmarks]
                hand_motion = _mean_pairwise_motion(previous_hand_centers, hand_centers)
                previous_hand_centers = hand_centers

                pose_center = _landmark_center(pose_landmarks) if pose_landmarks else None
                body_motion = (
                    math.dist(previous_pose_center, pose_center)
                    if previous_pose_center is not None and pose_center is not None
                    else 0.0
                )
                if pose_center is not None:
                    previous_pose_center = pose_center

                frames.append(
                    {
                        "time_seconds": round(index / fps, 3),
                        "pose_visible": bool(pose_landmarks),
                        "face_visible": bool(face_result.face_landmarks),
                        "hand_count": len(hand_landmarks),
                        "wrist_motion": float(hand_motion),
                        "body_motion": float(body_motion),
                        "posture_score": _posture_score(pose_landmarks),
                        "foot_stance_score": _foot_stance_score(pose_landmarks),
                        "smile_score": _blendshape_score(
                            face_blendshapes, ("mouthSmileLeft", "mouthSmileRight")
                        ),
                        "blink_score": _blendshape_score(
                            face_blendshapes, ("eyeBlinkLeft", "eyeBlinkRight")
                        ),
                    }
                )
                index += 1

        cap.release()
        payload = {
            "tool": self.name,
            "backend": "mediapipe_tasks",
            "backend_note": "MediaPipe Tasks pose, hand, and face landmark models were used.",
            "sample_id": sample_id,
            "fps": fps,
            "frame_count": frame_count,
            "duration_seconds": duration_seconds,
            "sampled_frames": frames,
        }
        path = raw_output_path(self.name, sample_id)
        write_json(path, payload)
        return ToolRunResult(tool=self.name, sample_id=sample_id, status="ok", raw_path=str(path))

    def _run_legacy_solutions(self, sample_id: str) -> ToolRunResult:
        import cv2
        import mediapipe as mp
        import numpy as np

        video_path = sample_video(sample_id)
        cap = cv2.VideoCapture(str(video_path))
        fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
        duration_seconds = frame_count / fps if frame_count else None
        pose = mp.solutions.pose.Pose(static_image_mode=False)
        hands = mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=2)
        face_mesh = mp.solutions.face_mesh.FaceMesh(static_image_mode=False, refine_landmarks=True)
        frames: list[dict] = []
        previous_wrists: dict[str, tuple[float, float]] = {}
        index = 0

        while True:
            ok, frame = cap.read()
            if not ok:
                break
            if index % max(1, int(fps // 5)) != 0:
                index += 1
                continue
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pose_result = pose.process(rgb)
            hand_result = hands.process(rgb)
            face_result = face_mesh.process(rgb)
            wrist_motion = []
            if hand_result.multi_hand_landmarks:
                for hand_index, hand_landmarks in enumerate(hand_result.multi_hand_landmarks):
                    wrist = hand_landmarks.landmark[0]
                    key = f"hand_{hand_index}"
                    current = (wrist.x, wrist.y)
                    if key in previous_wrists:
                        wrist_motion.append(math.dist(previous_wrists[key], current))
                    previous_wrists[key] = current
            frames.append(
                {
                    "time_seconds": round(index / fps, 3),
                    "pose_visible": bool(pose_result.pose_landmarks),
                    "face_visible": bool(face_result.multi_face_landmarks),
                    "hand_count": len(hand_result.multi_hand_landmarks or []),
                    "wrist_motion": float(np.mean(wrist_motion)) if wrist_motion else 0.0,
                    "body_motion": 0.0,
                }
            )
            index += 1

        cap.release()
        pose.close()
        hands.close()
        face_mesh.close()
        payload = {
            "tool": self.name,
            "backend": "mediapipe_solutions",
            "sample_id": sample_id,
            "fps": fps,
            "frame_count": frame_count,
            "duration_seconds": duration_seconds,
            "sampled_frames": frames,
        }
        path = raw_output_path(self.name, sample_id)
        write_json(path, payload)
        return ToolRunResult(tool=self.name, sample_id=sample_id, status="ok", raw_path=str(path))

    def _run_opencv_fallback(self, sample_id: str) -> ToolRunResult:
        import cv2
        import numpy as np

        video_path = sample_video(sample_id)
        cap = cv2.VideoCapture(str(video_path))
        fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
        duration_seconds = frame_count / fps if frame_count else None
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        frames: list[dict] = []
        previous_gray = None
        index = 0
        sample_every = max(1, int(fps // 5))

        while True:
            ok, frame = cap.read()
            if not ok:
                break
            if index % sample_every != 0:
                index += 1
                continue
            small = cv2.resize(frame, (640, 360))
            gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
            motion = 0.0
            if previous_gray is not None:
                diff = cv2.absdiff(gray, previous_gray)
                motion = float(np.mean(diff) / 255.0)
            previous_gray = gray
            frames.append(
                {
                    "time_seconds": round(index / fps, 3),
                    "pose_visible": False,
                    "face_visible": len(faces) > 0,
                    "hand_count": 0,
                    "wrist_motion": 0.0,
                    "visual_motion": motion,
                }
            )
            index += 1

        cap.release()
        payload = {
            "tool": self.name,
            "backend": "opencv_fallback",
            "backend_note": "OpenCV fallback measured face visibility and visual motion.",
            "sample_id": sample_id,
            "fps": fps,
            "frame_count": frame_count,
            "duration_seconds": duration_seconds,
            "sampled_frames": frames,
        }
        path = raw_output_path(self.name, sample_id)
        write_json(path, payload)
        return ToolRunResult(
            tool=self.name,
            sample_id=sample_id,
            status="ok",
            raw_path=str(path),
            message="Used OpenCV fallback because MediaPipe landmark models were unavailable.",
        )

    def normalize(self, sample_id: str) -> NormalizedToolOutput:
        import numpy as np

        raw = read_json(raw_output_path(self.name, sample_id))
        frames = raw.get("sampled_frames", [])
        total = max(len(frames), 1)
        face_rate = sum(1 for frame in frames if frame.get("face_visible")) / total
        pose_rate = sum(1 for frame in frames if frame.get("pose_visible")) / total
        hand_rate = sum(1 for frame in frames if frame.get("hand_count", 0) > 0) / total
        avg_hand_motion = (
            float(np.mean([frame.get("wrist_motion", 0.0) for frame in frames])) if frames else 0.0
        )
        hand_movement_events = sum(
            1
            for frame in frames
            if frame.get("hand_count", 0) > 0 and frame.get("wrist_motion", 0.0) >= 0.04
        )
        avg_body_motion = (
            float(np.mean([frame.get("body_motion", frame.get("visual_motion", 0.0)) for frame in frames]))
            if frames
            else 0.0
        )
        body_movement_events = sum(
            1
            for frame in frames
            if frame.get("body_motion", frame.get("visual_motion", 0.0)) >= 0.03
        )
        posture_scores = [
            frame.get("posture_score")
            for frame in frames
            if isinstance(frame.get("posture_score"), (int, float))
        ]
        avg_posture = float(np.mean(posture_scores)) if posture_scores else None
        duration_minutes = max((raw.get("duration_seconds") or 0) / 60, 0.001)
        smile_rate = (
            sum(1 for frame in frames if frame.get("smile_score", 0.0) >= 0.35) / duration_minutes
        )
        blink_rate = (
            sum(1 for frame in frames if frame.get("blink_score", 0.0) >= 0.35) / duration_minutes
        )
        body_repetition_rate = _body_repetition_rate(frames, duration_minutes)
        foot_scores = [
            frame.get("foot_stance_score")
            for frame in frames
            if isinstance(frame.get("foot_stance_score"), (int, float))
        ]
        avg_foot_stance = float(np.mean(foot_scores)) if foot_scores else None

        tasks_backend = raw.get("backend") == "mediapipe_tasks"
        factors = [
            FactorSignal(
                factor_id="face_visibility",
                factor_name="Face visibility",
                axis="لغة الجسد",
                value=round(face_rate, 3),
                score=round(face_rate * 100, 2),
                confidence=0.8 if tasks_backend else 0.55,
            ),
            FactorSignal(
                factor_id="body_visibility",
                factor_name="Body / pose visibility",
                axis="لغة الجسد",
                value=round(pose_rate, 3),
                score=round(pose_rate * 100, 2),
                confidence=0.85 if tasks_backend else 0.55,
            ),
            FactorSignal(
                factor_id="hand_visibility",
                factor_name="Hand visibility",
                axis="لغة الجسد",
                value=round(hand_rate, 3),
                score=round(hand_rate * 100, 2),
                confidence=0.85 if tasks_backend else 0.55,
            ),
            FactorSignal(
                factor_id="hand_movement",
                factor_name="Hand movement intensity",
                axis="لغة الجسد",
                value={
                    "average_motion_intensity": round(avg_hand_motion, 5),
                    "movement_event_count": hand_movement_events,
                    "movement_events_per_minute": round(hand_movement_events / duration_minutes, 2),
                    "hand_visible_frames": sum(
                        1 for frame in frames if frame.get("hand_count", 0) > 0
                    ),
                    "sampled_frames": len(frames),
                    "event_threshold": "wrist_motion >= 0.04",
                },
                score=_score_hand_movement(avg_hand_motion, hand_rate),
                confidence=0.75 if tasks_backend else 0.4,
                evidence=[
                    "Score is based on average wrist-motion intensity and hand visibility. Event count is reported for explanation."
                ],
            ),
            FactorSignal(
                factor_id="body_movement",
                factor_name="Overall body movement intensity",
                axis="لغة الجسد",
                value={
                    "average_motion_intensity": round(avg_body_motion, 5),
                    "movement_event_count": body_movement_events,
                    "movement_events_per_minute": round(body_movement_events / duration_minutes, 2),
                    "sampled_frames": len(frames),
                    "event_threshold": "body_motion >= 0.03",
                },
                score=_score_body_movement(avg_body_motion),
                confidence=0.7 if tasks_backend else 0.35,
                evidence=[raw.get("backend_note", "")] if raw.get("backend_note") else [],
            ),
        ]
        if avg_posture is not None:
            factors.append(
                FactorSignal(
                    factor_id="posture",
                    factor_name="Posture alignment proxy",
                    axis="لغة الجسد",
                    value=round(avg_posture, 2),
                    score=round(avg_posture, 2),
                    confidence=0.65,
                    evidence=[
                        "Computed from pose landmark shoulder balance, head centering, and spine verticality."
                    ],
                )
            )
        factors.extend(
            [
                FactorSignal(
                    factor_id="body_repetition_rate",
                    factor_name="Repeated body movement rate",
                    axis="لغة الجسد",
                    value=round(body_repetition_rate, 2),
                    score=_score_body_repetition_rate(body_repetition_rate),
                    confidence=0.6 if tasks_backend and pose_rate > 0.5 else 0.0,
                    evidence=["Computed from repeated body-motion spikes per minute."],
                ),
                FactorSignal(
                    factor_id="gesture_classification",
                    factor_name="Gesture polarity proxy",
                    axis="لغة الجسد",
                    value={
                        "hand_visibility_rate": round(hand_rate, 3),
                        "hand_motion": round(avg_hand_motion, 5),
                        "hand_movement_event_count": hand_movement_events,
                        "hand_movement_events_per_minute": round(
                            hand_movement_events / duration_minutes, 2
                        ),
                        "classification": "controlled_visible_hand_movement"
                        if hand_rate > 0.5
                        else "insufficient_hand_visibility",
                    },
                    score=_score_gesture_proxy(hand_rate, avg_hand_motion),
                    confidence=0.45 if tasks_backend and hand_rate > 0.5 else 0.0,
                    evidence=[
                        "Proxy based on hand visibility and controlled movement; not semantic gesture recognition."
                    ],
                ),
            ]
        )
        if avg_foot_stance is not None:
            factors.append(
                FactorSignal(
                    factor_id="foot_stance_width",
                    factor_name="Foot stance width proxy",
                    axis="لغة الجسد",
                    value=round(avg_foot_stance, 2),
                    score=round(avg_foot_stance, 2),
                    confidence=0.45 if tasks_backend else 0.0,
                    evidence=["Computed from ankle distance relative to shoulder width when pose landmarks exist."],
                )
            )
        if tasks_backend:
            factors.extend(
                [
                    FactorSignal(
                        factor_id="smile_rate",
                        factor_name="Smile rate",
                        axis="لغة الجسد",
                        value=round(smile_rate, 2),
                        score=_score_smile_rate(smile_rate),
                        confidence=0.45 if face_rate else 0.0,
                    ),
                    FactorSignal(
                        factor_id="blink_rate",
                        factor_name="Blink rate",
                        axis="لغة الجسد",
                        value=round(blink_rate, 2),
                        score=_score_blink_rate(blink_rate),
                        confidence=0.45 if face_rate else 0.0,
                    ),
                ]
            )
        return NormalizedToolOutput(tool=self.name, sample_id=sample_id, factors=factors)


def _model_path(name: str):
    return PROJECT_ROOT / "phase1_validation" / "models" / name


def _task_models_available() -> bool:
    return all(
        _model_path(name).exists()
        for name in ("pose_landmarker_lite.task", "hand_landmarker.task", "face_landmarker.task")
    )


def _landmark_center(landmarks) -> tuple[float, float]:
    if not landmarks:
        return (0.0, 0.0)
    return (
        sum(float(landmark.x) for landmark in landmarks) / len(landmarks),
        sum(float(landmark.y) for landmark in landmarks) / len(landmarks),
    )


def _mean_pairwise_motion(
    previous: list[tuple[float, float]],
    current: list[tuple[float, float]],
) -> float:
    if not previous or not current:
        return 0.0
    distances = [math.dist(old, new) for old, new in zip(previous[: len(current)], current)]
    return sum(distances) / len(distances) if distances else 0.0


def _posture_score(landmarks) -> float | None:
    if not landmarks or len(landmarks) < 25:
        return None
    left_shoulder, right_shoulder = landmarks[11], landmarks[12]
    left_ear, right_ear = landmarks[7], landmarks[8]
    left_hip, right_hip = landmarks[23], landmarks[24]
    shoulder_center = (
        (left_shoulder.x + right_shoulder.x) / 2,
        (left_shoulder.y + right_shoulder.y) / 2,
    )
    hip_center = ((left_hip.x + right_hip.x) / 2, (left_hip.y + right_hip.y) / 2)
    ear_center = ((left_ear.x + right_ear.x) / 2, (left_ear.y + right_ear.y) / 2)
    shoulder_balance = max(0.0, 100 - abs(left_shoulder.y - right_shoulder.y) * 800)
    head_centering = max(0.0, 100 - abs(ear_center[0] - shoulder_center[0]) * 600)
    spine_verticality = max(0.0, 100 - abs(shoulder_center[0] - hip_center[0]) * 600)
    return (shoulder_balance * 0.35) + (head_centering * 0.35) + (spine_verticality * 0.30)


def _foot_stance_score(landmarks) -> float | None:
    if not landmarks or len(landmarks) < 29:
        return None
    left_shoulder, right_shoulder = landmarks[11], landmarks[12]
    left_ankle, right_ankle = landmarks[27], landmarks[28]
    shoulder_width = abs(left_shoulder.x - right_shoulder.x)
    ankle_width = abs(left_ankle.x - right_ankle.x)
    if shoulder_width <= 0.01 or ankle_width <= 0.01:
        return None
    ratio = ankle_width / shoulder_width
    if 0.8 <= ratio <= 1.3:
        return 95.0
    if 0.6 <= ratio < 0.8 or 1.3 < ratio <= 1.6:
        return 82.0
    if 0.4 <= ratio < 0.6 or 1.6 < ratio <= 2.0:
        return 67.0
    return 50.0


def _blendshape_score(blendshapes, names: tuple[str, ...]) -> float:
    if not blendshapes:
        return 0.0
    scores = [
        float(category.score)
        for category in blendshapes
        if getattr(category, "category_name", "") in names
    ]
    return sum(scores) / len(scores) if scores else 0.0


def _score_hand_movement(avg_motion: float, hand_rate: float) -> float:
    if hand_rate <= 0.05:
        return 50.0
    if 0.01 <= avg_motion <= 0.05:
        return 100.0
    if 0.005 <= avg_motion <= 0.08:
        return 85.0
    if 0.001 <= avg_motion <= 0.12:
        return 70.0
    return 55.0


def _score_body_movement(avg_motion: float) -> float:
    if 0.002 <= avg_motion <= 0.035:
        return 90.0
    if 0.001 <= avg_motion <= 0.06:
        return 80.0
    if avg_motion <= 0.10:
        return 70.0
    return 55.0


def _body_repetition_rate(frames: list[dict], duration_minutes: float) -> float:
    motions = [float(frame.get("body_motion", 0.0)) for frame in frames]
    if len(motions) < 3:
        return 0.0
    threshold = max(0.04, float(np_percentile(motions, 85)))
    peaks = 0
    for index in range(1, len(motions) - 1):
        if motions[index] >= threshold and motions[index] > motions[index - 1] and motions[index] > motions[index + 1]:
            peaks += 1
    return peaks / max(duration_minutes, 0.001)


def np_percentile(values: list[float], percentile: float) -> float:
    ordered = sorted(values)
    if not ordered:
        return 0.0
    position = (len(ordered) - 1) * percentile / 100
    lower = int(math.floor(position))
    upper = int(math.ceil(position))
    if lower == upper:
        return ordered[lower]
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (position - lower)


def _score_body_repetition_rate(rate: float) -> float:
    if rate <= 2:
        return 95.0
    if rate <= 5:
        return 82.0
    if rate <= 8:
        return 67.0
    return 55.0


def _score_gesture_proxy(hand_rate: float, avg_motion: float) -> float:
    if hand_rate <= 0.2:
        return 55.0
    if 0.005 <= avg_motion <= 0.08:
        return 82.0
    if 0.001 <= avg_motion <= 0.12:
        return 70.0
    return 60.0


def _score_smile_rate(smile_rate: float) -> float:
    if 0.5 <= smile_rate <= 2:
        return 95.0
    if 2 < smile_rate <= 3:
        return 85.0
    if 0 < smile_rate < 0.5 or 3 < smile_rate <= 4:
        return 75.0
    return 60.0


def _score_blink_rate(blink_rate: float) -> float:
    if 15 <= blink_rate <= 20:
        return 100.0
    if 8 <= blink_rate <= 25:
        return 85.0
    if 6 <= blink_rate <= 30:
        return 70.0
    return 50.0
