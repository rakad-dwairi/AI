from __future__ import annotations

import os

import requests

from thohor_validation.core.io import load_metadata, read_json, write_json
from thohor_validation.core.models import FactorSignal, NormalizedToolOutput, ToolRunResult
from thohor_validation.core.paths import raw_output_path, sample_dir

from .import_adapter import ImportOnlyAdapter


class DeepgramAdapter(ImportOnlyAdapter):
    name = "deepgram"

    def __init__(self) -> None:
        super().__init__(self.name)

    def run(self, sample_id: str) -> ToolRunResult:
        api_key = os.getenv("DEEPGRAM_API_KEY")
        if not api_key:
            imported = super().run(sample_id)
            if imported.status == "imported":
                return imported
            return ToolRunResult(tool=self.name, sample_id=sample_id, status="skipped", message="DEEPGRAM_API_KEY is not configured. You can also import exported JSON.")
        audio_path = sample_dir(sample_id) / "audio.mp3"
        if not audio_path.exists():
            return ToolRunResult(
                tool=self.name,
                sample_id=sample_id,
                status="skipped",
                message=f"Missing {audio_path}. Run prepare-sample first.",
            )

        metadata = load_metadata(sample_id)
        expected_duration = metadata.expected_duration_seconds
        language = "ar" if metadata.language.lower().startswith("ar") else metadata.language
        params = {
            "model": "nova-3",
            "smart_format": "true",
            "punctuate": "true",
            "diarize": "true",
            "utterances": "true",
            "language": language,
        }
        with audio_path.open("rb") as file:
            response = requests.post(
                "https://api.deepgram.com/v1/listen",
                params=params,
                headers={
                    "Authorization": f"Token {api_key}",
                    "Content-Type": "audio/mpeg",
                },
                data=file,
                timeout=180,
            )
        if response.status_code >= 400:
            return ToolRunResult(
                tool=self.name,
                sample_id=sample_id,
                status="error",
                message=f"Deepgram request failed: {response.status_code} {response.text[:300]}",
            )

        path = raw_output_path(self.name, sample_id)
        write_json(path, response.json())
        return ToolRunResult(tool=self.name, sample_id=sample_id, status="ok", raw_path=str(path))

    def normalize(self, sample_id: str) -> NormalizedToolOutput:
        metadata = load_metadata(sample_id)
        expected_duration = metadata.expected_duration_seconds
        raw = read_json(raw_output_path(self.name, sample_id))
        channel = raw.get("results", {}).get("channels", [{}])[0]
        alternative = channel.get("alternatives", [{}])[0]
        transcript = alternative.get("transcript", "")
        words = alternative.get("words", [])
        utterances = raw.get("results", {}).get("utterances", [])
        duration = 0.0
        if words:
            duration = max(float(word.get("end", 0.0)) for word in words)
        word_count = len(words) or len(transcript.split())
        words_per_minute = (word_count / duration * 60) if duration else None
        pauses = _extract_word_pauses(words)
        pause_count = len(pauses)
        pause_rate_per_100_words = (pause_count / word_count * 100) if word_count else None
        speaker_ids = sorted(
            {
                str(item.get("speaker"))
                for item in (utterances or words)
                if item.get("speaker") is not None
            }
        )

        factors = [
            FactorSignal(
                factor_id="transcript",
                factor_name="Transcript availability",
                axis="المحتوى",
                value=bool(transcript),
                score=100 if transcript else 0,
                confidence=0.8,
            ),
            FactorSignal(
                factor_id="words_per_minute",
                factor_name="Speech speed",
                axis="الأداء الصوتي",
                value=round(words_per_minute, 2) if words_per_minute else None,
                score=_score_wpm(words_per_minute),
                confidence=0.7 if words_per_minute else 0.0,
            ),
            FactorSignal(
                factor_id="pause_count",
                factor_name="Pause count",
                axis="الأداء الصوتي",
                value={"count": pause_count, "threshold_seconds": 0.5, "examples": pauses[:10]},
                score=_score_pause_rate(pause_rate_per_100_words),
                confidence=0.7 if words else 0.0,
            ),
            FactorSignal(
                factor_id="pause_rate",
                factor_name="Pauses per 100 words",
                axis="الأداء الصوتي",
                value=round(pause_rate_per_100_words, 2) if pause_rate_per_100_words is not None else None,
                score=_score_pause_rate(pause_rate_per_100_words),
                confidence=0.7 if words else 0.0,
            ),
            FactorSignal(
                factor_id="actual_duration",
                factor_name="Actual speaking duration",
                axis="المحتوى",
                value=round(duration, 2) if duration else None,
                score=None,
                confidence=0.7 if duration else 0.0,
            ),
            FactorSignal(
                factor_id="expected_duration",
                factor_name="Expected duration",
                axis="المحتوى",
                value=expected_duration,
                score=None,
                confidence=0.7 if expected_duration else 0.0,
            ),
            FactorSignal(
                factor_id="duration_suitability",
                factor_name="Duration suitability",
                axis="المحتوى",
                value={
                    "actual_duration_seconds": round(duration, 2) if duration else None,
                    "expected_duration_seconds": expected_duration,
                },
                score=_score_duration_suitability(duration, expected_duration),
                confidence=0.7 if duration and expected_duration else 0.0,
            ),
            FactorSignal(
                factor_id="speaker_timing",
                factor_name="Speaker diarization / timing",
                axis="الحوار",
                value={"speaker_count": len(speaker_ids), "utterance_count": len(utterances)},
                score=85 if utterances else 40,
                confidence=0.7 if utterances else 0.35,
            ),
        ]
        return NormalizedToolOutput(tool=self.name, sample_id=sample_id, factors=factors)


def _score_wpm(words_per_minute: float | None) -> float | None:
    if words_per_minute is None:
        return None
    if 110 <= words_per_minute <= 120:
        return 100.0
    if 99 <= words_per_minute <= 130:
        return 90.0
    if 95 <= words_per_minute <= 135:
        return 80.0
    if 90 <= words_per_minute <= 140:
        return 70.0
    return 60.0


def _extract_word_pauses(words: list[dict], threshold_seconds: float = 0.5) -> list[dict]:
    pauses: list[dict] = []
    previous_end: float | None = None
    for word in words:
        start = word.get("start")
        end = word.get("end")
        if start is None or end is None:
            continue
        start_float = float(start)
        end_float = float(end)
        if previous_end is not None:
            gap = start_float - previous_end
            if gap >= threshold_seconds:
                pauses.append(
                    {
                        "start": round(previous_end, 2),
                        "end": round(start_float, 2),
                        "duration": round(gap, 2),
                    }
                )
        previous_end = end_float
    return pauses


def _score_pause_rate(pause_rate_per_100_words: float | None) -> float | None:
    if pause_rate_per_100_words is None:
        return None
    rate = pause_rate_per_100_words
    if abs(rate - 9) <= 1:
        return 100.0
    if 7 <= rate <= 11:
        return 90.0
    if rate in {6, 12}:
        return 80.0
    if 4 <= rate <= 14:
        return 70.0
    return 60.0


def _score_duration_suitability(
    actual_duration: float | None,
    expected_duration: float | None,
) -> float | None:
    if not actual_duration or not expected_duration:
        return None
    delta_ratio = abs(actual_duration - expected_duration) / expected_duration
    if delta_ratio <= 0.10:
        return 95.0
    if delta_ratio <= 0.20:
        return 85.0
    if delta_ratio <= 0.30:
        return 75.0
    if delta_ratio <= 0.45:
        return 65.0
    return 50.0
