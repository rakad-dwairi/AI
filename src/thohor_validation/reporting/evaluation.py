from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from thohor_validation.core.io import read_json, write_json
from thohor_validation.core.paths import REPORTS_DIR
from thohor_validation.reporting.cleanup import remove_report_files
from thohor_validation.reporting.rubric_engine import (
    AUTOMATIC,
    HUMAN,
    PARTIAL,
    UNSUPPORTED,
    build_rubric_readiness_report,
)


def build_speaker_evaluation(sample_id: str) -> dict[str, Any]:
    remove_report_files(sample_id, ("speaker_evaluation",))
    readiness = build_rubric_readiness_report(sample_id)
    rows = [_evaluation_row(row) for row in readiness["rows"]]
    summary = _summary(rows)
    report = {
        "sample_id": sample_id,
        "purpose": "Full per-criterion speaker evaluation based on the Excel rubric and available tool outputs.",
        "source_reference": "استمارة 2026.xlsx",
        "important_note": (
            "This report gives a result for every Excel criterion. A numeric score is only assigned "
            "when the current signals can support the rubric rule. Partial, human-review, and "
            "unsupported criteria are still included with evidence and next action."
        ),
        "summary": summary,
        "criteria": rows,
    }
    write_json(REPORTS_DIR / f"{sample_id}_speaker_evaluation.json", report)
    _write_csv(REPORTS_DIR / f"{sample_id}_speaker_evaluation.csv", rows)
    _write_markdown(REPORTS_DIR / f"{sample_id}_speaker_evaluation.md", report)
    return report


def _evaluation_row(readiness_row: dict[str, Any]) -> dict[str, Any]:
    status = readiness_row["measurability_status"]
    score = readiness_row["speaker_score"]
    rating = readiness_row["speaker_rating"]

    if status == AUTOMATIC:
        evaluation_status = "scored"
        result = f"Score {score} / {rating}"
    elif status == PARTIAL:
        evaluation_status = "partial_evidence_only"
        result = "Not scored yet; useful evidence exists but required signals are missing."
    elif status == HUMAN:
        evaluation_status = "human_review_required"
        result = "Not auto-scored; the Excel criterion requires expert judgment."
    else:
        evaluation_status = "not_supported"
        result = "Not scored; current tools do not provide supporting signals."

    return {
        "source_row": readiness_row["source_row"],
        "axis": readiness_row["axis"],
        "criterion": readiness_row["criterion"],
        "evaluation_status": evaluation_status,
        "score": score,
        "rating": rating,
        "result": result,
        "evidence": readiness_row["available_signals"],
        "score_basis": readiness_row["score_basis"],
        "detailed_evidence": readiness_row["detailed_signals"],
        "missing_data": readiness_row["missing_signals"],
        "explanation": readiness_row["reason"],
        "next_action": readiness_row["next_action"],
        "excel_evaluation_method": readiness_row["excel_evaluation_method"],
    }


def _summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    scored = [row for row in rows if row["evaluation_status"] == "scored"]
    numeric_scores = [float(row["score"]) for row in scored if row["score"] != ""]
    total = len(rows)
    counts = {
        "total_criteria": total,
        "scored": len(scored),
        "partial_evidence_only": sum(
            1 for row in rows if row["evaluation_status"] == "partial_evidence_only"
        ),
        "human_review_required": sum(
            1 for row in rows if row["evaluation_status"] == "human_review_required"
        ),
        "not_supported": sum(1 for row in rows if row["evaluation_status"] == "not_supported"),
        "scored_percent": round(len(scored) / total * 100, 1) if total else 0,
        "average_score_for_scored_criteria": round(sum(numeric_scores) / len(numeric_scores), 2)
        if numeric_scores
        else None,
    }
    return counts


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(_csv_row(row) for row in rows)


def _write_markdown(path: Path, report: dict[str, Any]) -> None:
    summary = report["summary"]
    lines = [
        "# Thohor Speaker Evaluation",
        "",
        f"Sample: `{report['sample_id']}`",
        f"Reference: `{report['source_reference']}`",
        "",
        report["important_note"],
        "",
        "## Summary",
        "",
        f"- Total criteria: {summary['total_criteria']}",
        f"- Scored automatically: {summary['scored']} ({summary['scored_percent']}%)",
        f"- Partial evidence only: {summary['partial_evidence_only']}",
        f"- Human review required: {summary['human_review_required']}",
        f"- Not supported: {summary['not_supported']}",
        f"- Average score for scored criteria: {summary['average_score_for_scored_criteria']}",
        "",
        "## How To Read This",
        "",
        "- `scored`: the current data supports a numeric speaker score.",
        "- `partial_evidence_only`: the tool found useful evidence, but not enough for a fair score.",
        "- `human_review_required`: the Excel file calls for expert judgment.",
        "- `not_supported`: current tools do not support this criterion yet.",
        "- `Score basis`: the exact signal used for the score, including measured value, signal score, confidence, and evidence.",
        "",
        "## Criteria Evaluation",
        "",
        "| Row | Axis | Criterion | Status | Score | Rating | Result | Evidence | Missing Data |",
        "|---:|---|---|---|---:|---|---|---|---|",
    ]
    for row in report["criteria"]:
        lines.append(
            "| {source_row} | {axis} | {criterion} | {evaluation_status} | {score} | "
            "{rating} | {result} | {evidence} | {missing_data} |".format(
                **{key: _md(value) for key, value in row.items()}
            )
        )
    lines.extend(["", "## Detailed Criterion Evidence", ""])
    for row in report["criteria"]:
        lines.extend(_criterion_detail_lines(row))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _md(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def _criterion_detail_lines(row: dict[str, Any]) -> list[str]:
    basis = row["score_basis"]
    selected = basis.get("selected_signal") if isinstance(basis, dict) else None
    details = row["detailed_evidence"]

    lines = [
        f"### Row {row['source_row']} - {row['criterion']}",
        "",
        f"- Axis: {row['axis']}",
        f"- Status: `{row['evaluation_status']}`",
        f"- Score: `{row['score']}`",
        f"- Rating: `{row['rating']}`",
        f"- Excel evaluation method: {row['excel_evaluation_method'] or 'Not specified'}",
        f"- Explanation: {row['explanation']}",
        f"- Calculation note: {basis.get('calculation_note') if isinstance(basis, dict) else ''}",
        f"- Next action: {row['next_action']}",
        "",
    ]

    if selected:
        lines.extend(
            [
                "**Selected Scoring Signal**",
                "",
                f"- Tool: `{selected.get('tool')}`",
                f"- Signal: `{selected.get('factor_id')}` - {selected.get('factor_name')}",
                f"- Measured value: `{_json_inline(selected.get('value'))}`",
                f"- Signal score: `{selected.get('score')}`",
                f"- Confidence: `{selected.get('confidence')}`",
                f"- Evidence: {_list_text(selected.get('evidence'))}",
                "",
            ]
        )
    else:
        lines.extend(
            [
                "**Selected Scoring Signal**",
                "",
                "- None. This criterion was not automatically scored from the current evidence.",
                "",
            ]
        )

    lines.extend(["**All Supporting Signals**", ""])
    if details:
        for signal in details:
            lines.extend(
                [
                    f"- `{signal.get('tool')}:{signal.get('factor_id')}` - {signal.get('factor_name')}",
                    f"  - Value: `{_json_inline(signal.get('value'))}`",
                    f"  - Score: `{signal.get('score')}`",
                    f"  - Confidence: `{signal.get('confidence')}`",
                    f"  - Evidence: {_list_text(signal.get('evidence'))}",
                ]
            )
    else:
        lines.append("- No supporting signal is currently attached to this criterion.")
    lines.append("")
    return lines


def _json_inline(value: Any) -> str:
    if value is None:
        return "None"
    text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    return text.replace("`", "'")


def _list_text(value: Any) -> str:
    if not value:
        return "None"
    if isinstance(value, list):
        return "; ".join(str(item).replace("\n", " ") for item in value)
    return str(value).replace("\n", " ")


def _csv_row(row: dict[str, Any]) -> dict[str, Any]:
    return {
        key: json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else value
        for key, value in row.items()
    }
