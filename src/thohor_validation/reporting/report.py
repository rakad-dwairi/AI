from __future__ import annotations

import csv
from pathlib import Path

from thohor_validation.core.io import read_json, write_json
from thohor_validation.core.models import NormalizedToolOutput
from thohor_validation.core.paths import FORM_PATH, REPORTS_DIR, normalized_output_path
from thohor_validation.core.rubric import load_form_criteria, load_rubric_levels
from thohor_validation.reporting.cleanup import remove_report_files

from thohor_validation.adapters.registry import known_tools


FACTOR_KEYWORDS = {
    "وضوح المخارج": ["transcript", "speech", "asr"],
    "نبرة الصوت": ["vocal", "tone", "prosody"],
    "مستوى الصوت": ["volume", "audio"],
    "الوقفات": ["pause", "speaker_timing"],
    "السرعة": ["words_per_minute", "transcript"],
    "خامة الصوت": ["pitch", "vocal"],
    "لغة جسد": ["body_visibility", "posture", "body_movement"],
    "اتصال بصري": ["gaze", "eye_contact", "blink_rate", "face_visibility"],
    "الإيماءات": ["hand_visibility", "hand_movement", "gesture"],
    "تعابير الوجه": ["facial_expression", "face_visibility", "smile_rate"],
    "الابتسامة": ["smile", "face_visibility"],
    "الرسائل": ["message_clarity", "transcript", "text_context"],
    "بنية": ["message_structure", "transcript"],
    "الاستهلال": ["opening", "transcript"],
    "الإقفال": ["closing", "transcript"],
    "الحوار": ["speaker_timing", "answer_strategy", "transcript"],
}


def _load_normalized(sample_id: str, tool: str) -> NormalizedToolOutput | None:
    path = normalized_output_path(tool, sample_id)
    if not path.exists():
        return None
    return NormalizedToolOutput.model_validate(read_json(path))


def _criterion_matches_factor(criterion_name: str, factor_id: str) -> bool:
    text = criterion_name
    for keyword, factor_ids in FACTOR_KEYWORDS.items():
        if keyword in text and any(expected in factor_id for expected in factor_ids):
            return True
    return False


def build_report(sample_id: str) -> dict:
    remove_report_files(sample_id, ("comparison", "summary"))
    criteria = load_form_criteria(FORM_PATH)
    rubric_levels = load_rubric_levels(FORM_PATH)
    normalized = {tool: _load_normalized(sample_id, tool) for tool in known_tools()}
    rows = []

    for criterion in criteria:
        tool_scores: dict[str, float | None] = {}
        best_tool = None
        best_score = -1.0
        for tool, output in normalized.items():
            score = None
            if output:
                matches = [
                    factor
                    for factor in output.factors
                    if _criterion_matches_factor(criterion.name, factor.factor_id)
                ]
                if matches:
                    score = max(float(match.score or 0) for match in matches)
            tool_scores[tool] = score
            if score is not None and score > best_score:
                best_score = score
                best_tool = tool

        rows.append(
            {
                "criterion_id": criterion.criterion_id,
                "axis": criterion.axis,
                "criterion": criterion.name,
                "source_row": criterion.source_row,
                "best_tool": best_tool or "",
                "best_score": round(best_score, 2) if best_tool else "",
                **{f"{tool}_score": tool_scores[tool] for tool in known_tools()},
            }
        )

    report = {
        "sample_id": sample_id,
        "criteria_count": len(criteria),
        "rubric_levels_count": len(rubric_levels),
        "rows": rows,
    }
    write_json(REPORTS_DIR / f"{sample_id}_comparison.json", report)
    _write_csv(REPORTS_DIR / f"{sample_id}_comparison.csv", rows)
    _write_markdown(REPORTS_DIR / f"{sample_id}_summary.md", rows)
    return report


def _write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _write_markdown(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Thohor Tool Comparison Summary",
        "",
        "| Axis | Criterion | Best Tool | Best Score |",
        "|---|---|---|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['axis']} | {row['criterion']} | {row['best_tool']} | {row['best_score']} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
