from __future__ import annotations

import json
import os

from openai import OpenAI

from thohor_validation.core.io import read_json, write_json
from thohor_validation.core.models import FactorSignal, NormalizedToolOutput, ToolRunResult
from thohor_validation.core.paths import FORM_PATH, raw_output_path
from thohor_validation.core.rubric import RubricCriterion, load_form_criteria

from .base import ToolAdapter


class OpenAIRubricAdapter(ToolAdapter):
    name = "openai_rubric"

    def run(self, sample_id: str) -> ToolRunResult:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return ToolRunResult(
                tool=self.name,
                sample_id=sample_id,
                status="skipped",
                message="OPENAI_API_KEY is not configured.",
            )

        transcript = _load_best_transcript(sample_id)
        if not transcript:
            return ToolRunResult(
                tool=self.name,
                sample_id=sample_id,
                status="skipped",
                message="No transcript found. Run openai or deepgram first.",
            )

        criteria = _select_text_criteria(load_form_criteria(FORM_PATH))
        client = OpenAI(api_key=api_key)
        model = os.getenv("OPENAI_TEXT_MODEL", "gpt-4.1-mini")
        response = client.chat.completions.create(
            model=model,
            temperature=0,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a strict Arabic executive communication evaluator. "
                        "Score only from the transcript and the provided rubric criteria. "
                        "Do not infer visual body language, appearance, facial expression, or vocal tone. "
                        "If the transcript clearly shows the feature is absent or weak, assign a low score. "
                        "Use partial with no numeric score only when the criterion truly cannot be judged from transcript alone. "
                        "Return valid JSON only."
                    ),
                },
                {
                    "role": "user",
                    "content": _build_prompt(sample_id, transcript, criteria),
                },
            ],
        )
        content = response.choices[0].message.content or "{}"
        parsed = json.loads(content)
        payload = {
            "tool": self.name,
            "sample_id": sample_id,
            "model": model,
            "criteria_count": len(criteria),
            "transcript_chars": len(transcript),
            "result": parsed,
        }
        path = raw_output_path(self.name, sample_id)
        write_json(path, payload)
        return ToolRunResult(tool=self.name, sample_id=sample_id, status="ok", raw_path=str(path))

    def normalize(self, sample_id: str) -> NormalizedToolOutput:
        raw = read_json(raw_output_path(self.name, sample_id))
        result = raw.get("result", {})
        rows = result.get("criteria", [])
        factors = []
        for row in rows:
            source_row = row.get("source_row")
            if source_row is None:
                continue
            score = row.get("score")
            try:
                score_float = float(score) if score not in (None, "") else None
            except (TypeError, ValueError):
                score_float = None
            evidence = row.get("evidence")
            evidence_items = evidence if isinstance(evidence, list) else [str(evidence)] if evidence else []
            factors.append(
                FactorSignal(
                    factor_id=f"criterion_score_{source_row}",
                    factor_name=f"Direct rubric score for Excel row {source_row}",
                    axis=row.get("axis"),
                    value={
                        "criterion": row.get("criterion"),
                        "rating": row.get("rating"),
                        "status": row.get("status"),
                        "explanation": row.get("explanation"),
                        "source": self.name,
                    },
                    score=score_float,
                    confidence=_normalize_confidence(row.get("confidence")),
                    evidence=evidence_items,
                )
            )
        return NormalizedToolOutput(
            tool=self.name,
            sample_id=sample_id,
            factors=factors,
            notes=[
                "Transcript-only rubric scoring. Visual, facial, body-language, and vocal-tone criteria are intentionally excluded."
            ],
        )


def _load_best_transcript(sample_id: str) -> str:
    openai_path = raw_output_path("openai", sample_id)
    if openai_path.exists():
        transcript = read_json(openai_path).get("transcript", "")
        if transcript:
            return transcript

    deepgram_path = raw_output_path("deepgram", sample_id)
    if deepgram_path.exists():
        raw = read_json(deepgram_path)
        return (
            raw.get("results", {})
            .get("channels", [{}])[0]
            .get("alternatives", [{}])[0]
            .get("transcript", "")
        )
    return ""


def _select_text_criteria(criteria: list[RubricCriterion]) -> list[RubricCriterion]:
    selected = []
    excluded_methods = ("تحليل بشري",)
    include_axis = ("المحتوى", "الأسئلة")
    include_names = (
        "الرسائل",
        "بنية",
        "الاستهلال",
        "الإقفال",
        "استمالات",
        "اللغة",
        "مناسبة طول",
        "القابلية",
        "استراتيجات",
        "التفاعل مع السائل",
    )
    for criterion in criteria:
        method = criterion.evaluation_method or ""
        if any(excluded in method for excluded in excluded_methods):
            continue
        if criterion.axis in include_axis or any(name in criterion.name for name in include_names):
            selected.append(criterion)
    return selected


def _build_prompt(sample_id: str, transcript: str, criteria: list[RubricCriterion]) -> str:
    criteria_payload = [
        {
            "source_row": criterion.source_row,
            "axis": criterion.axis,
            "criterion": criterion.name,
            "metric": criterion.metric,
            "equation": criterion.equation,
            "reference_scale": criterion.reference_scale,
        }
        for criterion in criteria
    ]
    return (
        "Evaluate this transcript against the selected Excel criteria.\n\n"
        "Rules:\n"
        "- Return one item for every criterion provided.\n"
        "- Use score 0-100 when the transcript gives enough evidence, including evidence that a feature is absent or weak.\n"
        "- If a transcript-based feature is missing, score it as weak/needs_development instead of partial.\n"
        "- Use status='partial' and score=null only when the criterion truly requires non-transcript data.\n"
        "- Ratings must be one of: excellent, very_good, good, needs_development, weak, not_scoreable.\n"
        "- Evidence must be short quotes or transcript observations.\n"
        "- Do not score body language, appearance, facial expression, hand movement, eye contact, or vocal tone.\n"
        "- Be strict and do not inflate scores.\n\n"
        f"Sample ID: {sample_id}\n\n"
        f"Transcript:\n{transcript}\n\n"
        "Criteria JSON:\n"
        f"{json.dumps(criteria_payload, ensure_ascii=False)}\n\n"
        "Return JSON with this shape:\n"
        "{\n"
        '  "criteria": [\n'
        "    {\n"
        '      "source_row": 37,\n'
        '      "axis": "المحتوى",\n'
        '      "criterion": "...",\n'
        '      "status": "scored|partial",\n'
        '      "score": 0,\n'
        '      "rating": "excellent|very_good|good|needs_development|weak|not_scoreable",\n'
        '      "evidence": ["..."],\n'
        '      "explanation": "...",\n'
        '      "confidence": 0.0\n'
        "    }\n"
        "  ]\n"
        "}"
    )


def _normalize_confidence(value) -> float | None:
    if value is None:
        return None
    try:
        confidence = float(value)
    except (TypeError, ValueError):
        return None
    if confidence > 1:
        confidence = confidence / 100
    return max(0.0, min(confidence, 1.0))
