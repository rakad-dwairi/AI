from __future__ import annotations

import os
from difflib import SequenceMatcher

from thohor_validation.core.io import read_json, write_json
from thohor_validation.core.models import FactorSignal, NormalizedToolOutput, ToolRunResult
from thohor_validation.core.paths import raw_output_path, sample_dir

from .base import ToolAdapter


FILLER_WORDS = ["يعني", "اه", "أمم", "امم", "مم", "طيب", "basically", "like", "um", "uh"]


class OpenAIAdapter(ToolAdapter):
    name = "openai"

    def run(self, sample_id: str) -> ToolRunResult:
        api_key = os.getenv("OPENAI_API_KEY")
        audio_path = sample_dir(sample_id) / "audio.mp3"
        if not api_key:
            return ToolRunResult(tool=self.name, sample_id=sample_id, status="skipped", message="OPENAI_API_KEY is not configured.")
        if not audio_path.exists():
            return ToolRunResult(tool=self.name, sample_id=sample_id, status="skipped", message=f"Missing {audio_path}. Run prepare-sample first.")

        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        model = os.getenv("OPENAI_TRANSCRIBE_MODEL", "gpt-4o-transcribe")
        with audio_path.open("rb") as audio_file:
            transcript = client.audio.transcriptions.create(model=model, file=audio_file)

        payload = {
            "tool": self.name,
            "sample_id": sample_id,
            "model": model,
            "transcript": getattr(transcript, "text", str(transcript)),
        }
        path = raw_output_path(self.name, sample_id)
        write_json(path, payload)
        return ToolRunResult(tool=self.name, sample_id=sample_id, status="ok", raw_path=str(path))

    def normalize(self, sample_id: str) -> NormalizedToolOutput:
        raw = read_json(raw_output_path(self.name, sample_id))
        transcript = raw.get("transcript", "")
        words = transcript.split()
        filler_hits = [word for word in words if word.strip("،,.!?؛:").lower() in FILLER_WORDS]
        sentences = [part.strip() for part in transcript.replace("؟", ".").split(".") if part.strip()]
        direct_sentence_rate = sum(1 for sentence in sentences if len(sentence.split()) <= 25) / max(len(sentences), 1)
        filler_rate = len(filler_hits) / max(len(words), 1)
        clarity_score = max(0.0, min(100.0, (direct_sentence_rate * 70) + ((1 - filler_rate) * 30)))
        structure_score = _score_structure(words, sentences)
        pronunciation = _pronunciation_proxy(sample_id, transcript)

        return NormalizedToolOutput(
            tool=self.name,
            sample_id=sample_id,
            factors=[
                FactorSignal(
                    factor_id="transcript",
                    factor_name="Transcript availability",
                    axis="المحتوى",
                    value=bool(transcript),
                    score=100 if transcript else 0,
                    confidence=0.8,
                ),
                FactorSignal(
                    factor_id="filler_words",
                    factor_name="Filler words",
                    axis="المحتوى",
                    value={"count": len(filler_hits), "examples": filler_hits[:10]},
                    score=max(0.0, round(100 - filler_rate * 1000, 2)),
                    confidence=0.55,
                ),
                FactorSignal(
                    factor_id="message_clarity",
                    factor_name="Message clarity proxy",
                    axis="المحتوى",
                    value={"word_count": len(words), "sentence_count": len(sentences)},
                    score=round(clarity_score, 2),
                    confidence=0.45,
                ),
                FactorSignal(
                    factor_id="content_structure",
                    factor_name="Content structure proxy",
                    axis="المحتوى",
                    value={"word_count": len(words), "sentence_count": len(sentences)},
                    score=structure_score,
                    confidence=0.45,
                ),
                FactorSignal(
                    factor_id="pronunciation_clarity",
                    factor_name="Pronunciation clarity proxy",
                    axis="الأداء الصوتي",
                    value=pronunciation,
                    score=pronunciation.get("score"),
                    confidence=0.4 if pronunciation.get("score") is not None else 0.0,
                    evidence=[
                        "Proxy based on OpenAI/Deepgram transcript agreement; not true PCC phoneme scoring."
                    ],
                ),
                FactorSignal(
                    factor_id="weak_letter_detection",
                    factor_name="Weak-letter detection proxy",
                    axis="الأداء الصوتي",
                    value=pronunciation,
                    score=pronunciation.get("weak_letter_score"),
                    confidence=0.3 if pronunciation.get("weak_letter_score") is not None else 0.0,
                    evidence=[
                        "Proxy only. True weak-letter detection needs phoneme alignment or human reference transcript."
                    ],
                ),
            ],
            notes=["This is a Phase 1 proxy. Final content scoring should use a stricter rubric prompt later."],
        )


def _score_structure(words: list[str], sentences: list[str]) -> float:
    word_count = len(words)
    sentence_count = len(sentences)
    if word_count >= 80 and sentence_count >= 4:
        return 85.0
    if word_count >= 50 and sentence_count >= 3:
        return 75.0
    if word_count >= 30 and sentence_count >= 2:
        return 65.0
    if word_count >= 20:
        return 50.0
    return 40.0


def _pronunciation_proxy(sample_id: str, openai_transcript: str) -> dict:
    from thohor_validation.core.paths import raw_output_path

    deepgram_path = raw_output_path("deepgram", sample_id)
    if not deepgram_path.exists() or not openai_transcript:
        return {}
    raw = read_json(deepgram_path)
    deepgram_transcript = (
        raw.get("results", {})
        .get("channels", [{}])[0]
        .get("alternatives", [{}])[0]
        .get("transcript", "")
    )
    if not deepgram_transcript:
        return {}
    normalized_openai = _normalize_arabic_text(openai_transcript)
    normalized_deepgram = _normalize_arabic_text(deepgram_transcript)
    agreement = SequenceMatcher(None, normalized_openai, normalized_deepgram).ratio()
    score = round(max(50.0, min(95.0, agreement * 100)), 2)
    return {
        "openai_deepgram_agreement": round(agreement, 3),
        "score": score,
        "weak_letter_score": score,
    }


def _normalize_arabic_text(text: str) -> str:
    replacements = {
        "أ": "ا",
        "إ": "ا",
        "آ": "ا",
        "ى": "ي",
        "ة": "ه",
    }
    for source, target in replacements.items():
        text = text.replace(source, target)
    return "".join(ch for ch in text if ch.isalnum() or ch.isspace()).lower()
