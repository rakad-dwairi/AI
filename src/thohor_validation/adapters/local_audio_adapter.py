from __future__ import annotations

import re
import subprocess

import numpy as np

from thohor_validation.core.io import write_json
from thohor_validation.core.models import FactorSignal, NormalizedToolOutput, ToolRunResult
from thohor_validation.core.paths import raw_output_path, sample_dir

from .base import ToolAdapter


class LocalAudioAdapter(ToolAdapter):
    name = "local_audio"

    def run(self, sample_id: str) -> ToolRunResult:
        audio_path = sample_dir(sample_id) / "audio.mp3"
        if not audio_path.exists():
            return ToolRunResult(
                tool=self.name,
                sample_id=sample_id,
                status="skipped",
                message=f"Missing {audio_path}. Run prepare-sample first.",
            )

        volume = _run_ffmpeg_filter(audio_path, "volumedetect")
        silence = _run_ffmpeg_filter(audio_path, "silencedetect=noise=-35dB:d=0.5")
        pitch = _estimate_pitch(audio_path)
        payload = {
            "tool": self.name,
            "sample_id": sample_id,
            "volume": _parse_volume(volume),
            "silence": _parse_silence(silence),
            "pitch": pitch,
        }
        path = raw_output_path(self.name, sample_id)
        write_json(path, payload)
        return ToolRunResult(tool=self.name, sample_id=sample_id, status="ok", raw_path=str(path))

    def normalize(self, sample_id: str) -> NormalizedToolOutput:
        from thohor_validation.core.io import read_json

        raw = read_json(raw_output_path(self.name, sample_id))
        volume = raw.get("volume", {})
        silence = raw.get("silence", {})
        mean_volume = volume.get("mean_volume_db")
        max_volume = volume.get("max_volume_db")
        silence_events = silence.get("events", [])
        pitch = raw.get("pitch", {})
        pitch_range = pitch.get("pitch_range_hz")
        pitch_variation = pitch.get("pitch_variation_hz")

        return NormalizedToolOutput(
            tool=self.name,
            sample_id=sample_id,
            factors=[
                FactorSignal(
                    factor_id="volume_db",
                    factor_name="Audio loudness in dB",
                    axis="الأداء الصوتي",
                    value={"mean_volume_db": mean_volume, "max_volume_db": max_volume},
                    score=_score_volume(mean_volume, max_volume),
                    confidence=0.65 if mean_volume is not None else 0.0,
                ),
                FactorSignal(
                    factor_id="audio_silence_events",
                    factor_name="Audio silence events",
                    axis="الأداء الصوتي",
                    value={"count": len(silence_events), "events": silence_events[:10]},
                    score=None,
                    confidence=0.55,
                ),
                FactorSignal(
                    factor_id="pitch_range_hz",
                    factor_name="Pitch range in Hz",
                    axis="الأداء الصوتي",
                    value={
                        "min_pitch_hz": pitch.get("min_pitch_hz"),
                        "max_pitch_hz": pitch.get("max_pitch_hz"),
                        "pitch_range_hz": pitch_range,
                        "voiced_frame_count": pitch.get("voiced_frame_count"),
                    },
                    score=_score_pitch_range(pitch_range),
                    confidence=0.55 if pitch_range is not None else 0.0,
                ),
                FactorSignal(
                    factor_id="pitch_variation",
                    factor_name="Pitch variation / vocal coloring proxy",
                    axis="الأداء الصوتي",
                    value={
                        "pitch_variation_hz": pitch_variation,
                        "mean_pitch_hz": pitch.get("mean_pitch_hz"),
                    },
                    score=_score_pitch_variation(pitch_variation),
                    confidence=0.5 if pitch_variation is not None else 0.0,
                ),
            ],
            notes=["Local ffmpeg analysis; no external API cost."],
        )


def _run_ffmpeg_filter(audio_path, audio_filter: str) -> str:
    result = subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-nostats",
            "-i",
            str(audio_path),
            "-af",
            audio_filter,
            "-f",
            "null",
            "-",
        ],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.stdout + "\n" + result.stderr


def _parse_volume(output: str) -> dict:
    mean_match = re.search(r"mean_volume:\s*(-?\d+(?:\.\d+)?) dB", output)
    max_match = re.search(r"max_volume:\s*(-?\d+(?:\.\d+)?) dB", output)
    return {
        "mean_volume_db": float(mean_match.group(1)) if mean_match else None,
        "max_volume_db": float(max_match.group(1)) if max_match else None,
    }


def _parse_silence(output: str) -> dict:
    starts = [float(value) for value in re.findall(r"silence_start:\s*(\d+(?:\.\d+)?)", output)]
    ends = [
        (float(end), float(duration))
        for end, duration in re.findall(
            r"silence_end:\s*(\d+(?:\.\d+)?)\s*\|\s*silence_duration:\s*(\d+(?:\.\d+)?)",
            output,
        )
    ]
    events = []
    for index, start in enumerate(starts):
        if index < len(ends):
            end, duration = ends[index]
        else:
            end, duration = None, None
        events.append(
            {
                "start": round(start, 2),
                "end": round(end, 2) if end is not None else None,
                "duration": round(duration, 2) if duration is not None else None,
            }
        )
    return {"events": events}


def _score_volume(mean_volume: float | None, max_volume: float | None) -> float | None:
    if mean_volume is None or max_volume is None:
        return None
    if -24 <= mean_volume <= -12 and max_volume <= -1:
        return 90.0
    if -30 <= mean_volume <= -8 and max_volume <= 0:
        return 80.0
    if -36 <= mean_volume <= -6:
        return 70.0
    return 60.0


def _estimate_pitch(audio_path, sample_rate: int = 16000) -> dict:
    result = subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-nostats",
            "-i",
            str(audio_path),
            "-ac",
            "1",
            "-ar",
            str(sample_rate),
            "-f",
            "f32le",
            "-",
        ],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    if not result.stdout:
        return {}
    samples = np.frombuffer(result.stdout, dtype=np.float32)
    if samples.size < sample_rate:
        return {}

    frame_size = int(sample_rate * 0.04)
    hop = int(sample_rate * 0.02)
    min_lag = int(sample_rate / 300)
    max_lag = int(sample_rate / 80)
    pitches = []
    window = np.hanning(frame_size)

    for start in range(0, len(samples) - frame_size, hop):
        frame = samples[start : start + frame_size]
        energy = float(np.sqrt(np.mean(frame**2)))
        if energy < 0.01:
            continue
        frame = (frame - np.mean(frame)) * window
        corr = np.correlate(frame, frame, mode="full")[frame_size - 1 :]
        if corr[0] <= 0:
            continue
        segment = corr[min_lag:max_lag]
        if segment.size == 0:
            continue
        lag = int(np.argmax(segment) + min_lag)
        confidence = float(corr[lag] / corr[0])
        if confidence < 0.35:
            continue
        pitch = sample_rate / lag
        if 80 <= pitch <= 300:
            pitches.append(pitch)

    if not pitches:
        return {}
    pitch_array = np.array(pitches)
    low = float(np.percentile(pitch_array, 10))
    high = float(np.percentile(pitch_array, 90))
    return {
        "min_pitch_hz": round(low, 2),
        "max_pitch_hz": round(high, 2),
        "mean_pitch_hz": round(float(np.mean(pitch_array)), 2),
        "pitch_range_hz": round(high - low, 2),
        "pitch_variation_hz": round(float(np.std(pitch_array)), 2),
        "voiced_frame_count": int(len(pitches)),
    }


def _score_pitch_range(pitch_range: float | None) -> float | None:
    if pitch_range is None:
        return None
    if 60 <= pitch_range <= 160:
        return 90.0
    if 40 <= pitch_range <= 200:
        return 80.0
    if 25 <= pitch_range <= 240:
        return 70.0
    return 60.0


def _score_pitch_variation(pitch_variation: float | None) -> float | None:
    if pitch_variation is None:
        return None
    if 18 <= pitch_variation <= 55:
        return 90.0
    if 10 <= pitch_variation <= 75:
        return 80.0
    if 5 <= pitch_variation <= 95:
        return 70.0
    return 60.0
