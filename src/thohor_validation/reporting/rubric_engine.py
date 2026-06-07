from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from thohor_validation.adapters.registry import known_tools
from thohor_validation.core.io import read_json, write_json
from thohor_validation.core.models import FactorSignal, NormalizedToolOutput
from thohor_validation.core.paths import FORM_PATH, REPORTS_DIR, normalized_output_path
from thohor_validation.core.rubric import RubricCriterion, load_form_criteria
from thohor_validation.reporting.cleanup import remove_report_files


AUTOMATIC = "automatically_measurable"
PARTIAL = "partially_measurable"
HUMAN = "human_review_required"
UNSUPPORTED = "not_supported_by_current_tools"


@dataclass(frozen=True)
class CriterionRule:
    keywords: tuple[str, ...]
    required_signals: tuple[str, ...]
    useful_signals: tuple[str, ...]
    scoring_signal: str | None
    automatic_when_required_present: bool
    missing_explanation: str
    next_action: str


RULES = [
    CriterionRule(
        keywords=("السرعة",),
        required_signals=("words_per_minute",),
        useful_signals=("transcript",),
        scoring_signal="words_per_minute",
        automatic_when_required_present=True,
        missing_explanation="Speech speed needs words-per-minute from a timestamped transcript.",
        next_action="Use Deepgram or another timestamped STT output to calculate WPM against the Excel ranges.",
    ),
    CriterionRule(
        keywords=("الوقفات", "التنفس"),
        required_signals=("pause_count", "pause_rate"),
        useful_signals=("speaker_timing", "transcript", "words_per_minute", "audio_silence_events"),
        scoring_signal="pause_rate",
        automatic_when_required_present=True,
        missing_explanation="The current outputs include timing, but not explicit pause count/rate per 100 words.",
        next_action="Add silence/pause extraction from word timestamps or audio waveform before scoring this criterion.",
    ),
    CriterionRule(
        keywords=("وضوح المخارج",),
        required_signals=("pcc", "asr_accuracy", "erc"),
        useful_signals=("transcript",),
        scoring_signal=None,
        automatic_when_required_present=True,
        missing_explanation="The Excel formula requires PCC, ASR accuracy, and ERC; transcript alone is not enough.",
        next_action="Add pronunciation/phoneme alignment or a human reference transcript to calculate PCC/ASR/ERC.",
    ),
    CriterionRule(
        keywords=("نبرة الصوت", "التلوين"),
        required_signals=("pitch_variation", "prosody_match"),
        useful_signals=("vocal_expression",),
        scoring_signal=None,
        automatic_when_required_present=True,
        missing_explanation="Tone coloring needs pitch/prosody features that are not currently extracted.",
        next_action="Add acoustic prosody extraction or connect a supported vocal-expression provider.",
    ),
    CriterionRule(
        keywords=("مستوى الصوت",),
        required_signals=("volume_db",),
        useful_signals=(),
        scoring_signal="volume_db",
        automatic_when_required_present=True,
        missing_explanation="Volume scoring needs dB/loudness measurements from the audio track.",
        next_action="Add audio loudness analysis with ffmpeg/Librosa to extract min/mean/max dB.",
    ),
    CriterionRule(
        keywords=("خامة الصوت",),
        required_signals=("pitch_range_hz",),
        useful_signals=("vocal_expression",),
        scoring_signal=None,
        automatic_when_required_present=True,
        missing_explanation="Voice timbre/range needs pitch range in Hz.",
        next_action="Add pitch tracking to calculate lowest/highest frequency and vocal range.",
    ),
    CriterionRule(
        keywords=("لغة جسد منضبطة",),
        required_signals=("posture", "body_visibility"),
        useful_signals=("body_movement", "face_visibility"),
        scoring_signal=None,
        automatic_when_required_present=True,
        missing_explanation="Posture scoring needs real pose landmarks/CVA/shoulder/kyphosis/pelvic measurements.",
        next_action="Replace the OpenCV fallback with true MediaPipe pose/holistic landmarks or task models.",
    ),
    CriterionRule(
        keywords=("التفاعل مع السائل", "الثبات الانفعالي"),
        required_signals=("transcript", "speaker_timing", "facial_expression", "vocal_expression"),
        useful_signals=("face_detection", "face_visibility"),
        scoring_signal=None,
        automatic_when_required_present=False,
        missing_explanation="Dialogue/emotional stability needs combined transcript, timing, face, body, and voice signals.",
        next_action="Combine transcript/timing with expression, blink, posture, and vocal stability before scoring.",
    ),
    CriterionRule(
        keywords=("اتصال بصري", "النظرات", "رمش"),
        required_signals=("gaze_direction", "blink_rate"),
        useful_signals=("face_visibility", "face_detection"),
        scoring_signal=None,
        automatic_when_required_present=True,
        missing_explanation="Eye contact needs gaze direction and blink-rate extraction, not only face detection.",
        next_action="Add face/eye landmark tracking to calculate gaze distribution and blink rate.",
    ),
    CriterionRule(
        keywords=("الإيماءات", "حركة اليدين"),
        required_signals=("gesture_classification", "hand_movement"),
        useful_signals=("hand_visibility", "body_movement"),
        scoring_signal=None,
        automatic_when_required_present=True,
        missing_explanation="Gesture scoring needs hand landmarks and positive/negative gesture classification.",
        next_action="Add hand landmarks plus gesture rules/classes for positive and negative hand positions.",
    ),
    CriterionRule(
        keywords=("تعابير الوجه", "الابتسامة"),
        required_signals=("facial_expression", "smile_rate", "smile_authenticity"),
        useful_signals=("face_visibility", "face_detection"),
        scoring_signal=None,
        automatic_when_required_present=True,
        missing_explanation="Expression/smile scoring needs expression labels or face landmarks.",
        next_action="Add face landmarks/expression provider output for openness, smile rate, and smile authenticity.",
    ),
    CriterionRule(
        keywords=("مناسبة طول الحديث",),
        required_signals=("actual_duration", "expected_duration"),
        useful_signals=("transcript", "speaker_timing"),
        scoring_signal=None,
        automatic_when_required_present=True,
        missing_explanation="Duration suitability needs actual duration and the expected/allowed time for the occasion.",
        next_action="Store the expected duration in sample metadata, then compare actual speaking time against it.",
    ),
    CriterionRule(
        keywords=("الرسائل", "بنية المحتوى", "الاستهلال", "الإقفال", "استمالات", "اللغة", "الوعي بالسياق", "الأصالة", "القابلية للاقتباس", "استراتيجات الإجابة"),
        required_signals=("transcript",),
        useful_signals=("message_clarity", "filler_words", "speaker_timing"),
        scoring_signal=None,
        automatic_when_required_present=False,
        missing_explanation="Content criteria need transcript plus rubric-specific NLP prompts or human validation.",
        next_action="Use the transcript with a controlled rubric prompt, then keep human review for subjective context.",
    ),
]

SOURCE_ROW_RULES = {
    11: CriterionRule(
        keywords=("row_11",),
        required_signals=("pronunciation_clarity",),
        useful_signals=("transcript",),
        scoring_signal="pronunciation_clarity",
        automatic_when_required_present=True,
        missing_explanation="Pronunciation clarity needs PCC/ASR/ERC or a defensible proxy.",
        next_action="Replace this ASR-agreement proxy with true PCC/phoneme alignment when a reference transcript is available.",
    ),
    12: CriterionRule(
        keywords=("row_12",),
        required_signals=("weak_letter_detection",),
        useful_signals=("transcript",),
        scoring_signal="weak_letter_detection",
        automatic_when_required_present=True,
        missing_explanation="Weak-letter detection needs phoneme-level error analysis or a proxy.",
        next_action="Replace this proxy with letter/phoneme error rates from aligned reference text.",
    ),
    13: CriterionRule(
        keywords=("row_13",),
        required_signals=("pitch_variation",),
        useful_signals=("transcript",),
        scoring_signal="pitch_variation",
        automatic_when_required_present=True,
        missing_explanation="Tone coloring needs pitch variation/prosody features.",
        next_action="Review as a pitch-variation proxy; add semantic prosody matching later for stricter scoring.",
    ),
    17: CriterionRule(
        keywords=("row_17",),
        required_signals=("pitch_range_hz",),
        useful_signals=("pitch_variation",),
        scoring_signal="pitch_range_hz",
        automatic_when_required_present=True,
        missing_explanation="Voice quality/range needs pitch range in Hz.",
        next_action="Review pitch range proxy; refine later with musical-note range and voice quality analysis.",
    ),
    22: CriterionRule(
        keywords=("row_22",),
        required_signals=("posture",),
        useful_signals=("body_visibility", "body_movement"),
        scoring_signal="posture",
        automatic_when_required_present=True,
        missing_explanation="Posture scoring needs pose landmarks.",
        next_action="Review posture proxy evidence; refine later into CVA/shoulder/kyphosis/pelvic sub-scores.",
    ),
    23: CriterionRule(
        keywords=("row_23",),
        required_signals=("body_repetition_rate",),
        useful_signals=("body_movement", "body_visibility", "posture"),
        scoring_signal="body_repetition_rate",
        automatic_when_required_present=True,
        missing_explanation="Repetitive tension movement needs event counting per minute, not only movement intensity.",
        next_action="Convert body landmark changes into repeated movement events per minute.",
    ),
    24: CriterionRule(
        keywords=("row_24",),
        required_signals=("foot_stance_width",),
        useful_signals=("body_visibility", "posture"),
        scoring_signal="foot_stance_width",
        automatic_when_required_present=True,
        missing_explanation="Foot spacing needs reliable ankle/foot landmarks and shoulder-width comparison.",
        next_action="Add foot stance extraction from lower-body pose landmarks when full body is visible.",
    ),
    25: CriterionRule(
        keywords=("row_25",),
        required_signals=("gaze_direction",),
        useful_signals=("face_detection",),
        scoring_signal="gaze_direction",
        automatic_when_required_present=True,
        missing_explanation="Distraction/eye-contact scoring needs gaze or head-direction tracking.",
        next_action="Review AWS head-pose proxy; refine later with true eye gaze landmarks.",
    ),
    26: CriterionRule(
        keywords=("row_26",),
        required_signals=("gaze_distribution",),
        useful_signals=("face_detection",),
        scoring_signal="gaze_distribution",
        automatic_when_required_present=True,
        missing_explanation="Gaze distribution needs left/center/right direction tracking.",
        next_action="Review AWS head-pose distribution proxy; refine later with true eye gaze.",
    ),
    27: CriterionRule(
        keywords=("row_27",),
        required_signals=("eye_contact_stability",),
        useful_signals=("face_detection",),
        scoring_signal="eye_contact_stability",
        automatic_when_required_present=True,
        missing_explanation="Eye-contact stability needs repeated gaze direction over time.",
        next_action="Review frontal-head-pose stability proxy; refine later with eye landmarks.",
    ),
    28: CriterionRule(
        keywords=("row_28",),
        required_signals=("blink_rate",),
        useful_signals=("face_detection", "face_visibility"),
        scoring_signal="blink_rate",
        automatic_when_required_present=True,
        missing_explanation="Blink-rate scoring needs reliable eye landmarks or blink events.",
        next_action="Add blink detection from face landmarks or another face-analysis provider.",
    ),
    30: CriterionRule(
        keywords=("row_30",),
        required_signals=("hand_movement", "hand_visibility"),
        useful_signals=("body_movement",),
        scoring_signal="hand_movement",
        automatic_when_required_present=True,
        missing_explanation="Movement-rate scoring needs hand landmarks and hand movement over time.",
        next_action="Review movement intensity; refine later into count-per-minute gesture events.",
    ),
    29: CriterionRule(
        keywords=("row_29",),
        required_signals=("gesture_classification",),
        useful_signals=("hand_visibility", "hand_movement"),
        scoring_signal="gesture_classification",
        automatic_when_required_present=True,
        missing_explanation="Positive/negative gesture scoring needs gesture classification.",
        next_action="Review gesture proxy; refine later with semantic positive/negative gesture classes.",
    ),
    31: CriterionRule(
        keywords=("row_31",),
        required_signals=("gesture_classification",),
        useful_signals=("hand_visibility", "hand_movement"),
        scoring_signal="gesture_classification",
        automatic_when_required_present=True,
        missing_explanation="Tension gesture scoring needs gesture classification.",
        next_action="Review gesture proxy; refine later with tension-specific gesture classes.",
    ),
    33: CriterionRule(
        keywords=("row_33",),
        required_signals=("facial_expression",),
        useful_signals=("face_detection",),
        scoring_signal="facial_expression",
        automatic_when_required_present=True,
        missing_explanation="Facial openness needs expression or emotion attributes.",
        next_action="Review AWS expression proxy; refine later with face landmarks/blendshapes.",
    ),
    34: CriterionRule(
        keywords=("row_34",),
        required_signals=("smile_rate",),
        useful_signals=("face_detection",),
        scoring_signal="smile_rate",
        automatic_when_required_present=True,
        missing_explanation="Smile rate needs smile events over time.",
        next_action="Review sampled-frame smile rate; refine later with continuous face landmarks.",
    ),
    35: CriterionRule(
        keywords=("row_35",),
        required_signals=("smile_authenticity",),
        useful_signals=("smile_rate", "face_detection"),
        scoring_signal="smile_authenticity",
        automatic_when_required_present=True,
        missing_explanation="Smile authenticity needs mouth/cheek/eye evidence.",
        next_action="Review AWS smile-confidence proxy; refine later with Duchenne-style face landmarks.",
    ),
    38: CriterionRule(
        keywords=("row_38",),
        required_signals=("message_clarity",),
        useful_signals=("transcript", "filler_words"),
        scoring_signal="message_clarity",
        automatic_when_required_present=True,
        missing_explanation="Message clarity needs transcript-derived directness, filler, and length signals.",
        next_action="Review transcript heuristic; refine later with sentence-level Arabic NLP.",
    ),
    40: CriterionRule(
        keywords=("row_40",),
        required_signals=("content_structure",),
        useful_signals=("transcript",),
        scoring_signal="content_structure",
        automatic_when_required_present=True,
        missing_explanation="Content structure needs transcript segmentation and structure detection.",
        next_action="Review content-structure proxy; refine later with a stricter structure classifier.",
    ),
    50: CriterionRule(
        keywords=("row_50",),
        required_signals=("duration_suitability",),
        useful_signals=("actual_duration", "expected_duration"),
        scoring_signal="duration_suitability",
        automatic_when_required_present=True,
        missing_explanation="Duration suitability needs actual duration and expected duration.",
        next_action="Set expected_duration_seconds in sample metadata for the relevant event/context.",
    ),
}


def build_rubric_readiness_report(sample_id: str) -> dict[str, Any]:
    remove_report_files(sample_id, ("rubric_readiness",))
    criteria = load_form_criteria(FORM_PATH)
    outputs = _load_outputs(sample_id)
    rows = [_evaluate_criterion(criterion, outputs) for criterion in criteria]
    summary = _summarize(rows)
    report = {
        "sample_id": sample_id,
        "purpose": "Evaluate readiness to score each Excel criterion using current tool outputs.",
        "important_distinction": (
            "This report separates speaker evaluation from tool validation. A criterion receives a "
            "speaker score only when the available signal directly supports the Excel formula/range."
        ),
        "summary": summary,
        "rows": rows,
    }
    write_json(REPORTS_DIR / f"{sample_id}_rubric_readiness.json", report)
    _write_csv(REPORTS_DIR / f"{sample_id}_rubric_readiness.csv", rows)
    _write_markdown(REPORTS_DIR / f"{sample_id}_rubric_readiness.md", report)
    return report


def _load_outputs(sample_id: str) -> dict[str, NormalizedToolOutput]:
    outputs: dict[str, NormalizedToolOutput] = {}
    for tool in known_tools():
        path = normalized_output_path(tool, sample_id)
        if path.exists():
            outputs[tool] = NormalizedToolOutput.model_validate(read_json(path))
    return outputs


def _evaluate_criterion(
    criterion: RubricCriterion,
    outputs: dict[str, NormalizedToolOutput],
) -> dict[str, Any]:
    rule = _find_rule(criterion)
    all_factors = _factor_index(outputs)
    composite_score = _composite_criterion_score(criterion, all_factors)
    direct_score = _direct_criterion_score(criterion, all_factors)
    human_requested = _is_human_review(criterion)

    if composite_score:
        status = AUTOMATIC
        reason = "A composite rubric score is available from multiple normalized signals."
        matched = [composite_score]
        missing = []
        score = composite_score[1].score
        rating = _rating_from_score(score)
        next_action = "Review composite evidence and weights before operational acceptance."
    elif direct_score:
        status = AUTOMATIC
        reason = "A direct transcript-based rubric score is available for this Excel row."
        matched = [direct_score]
        missing = []
        score = direct_score[1].score
        rating = _direct_rating(direct_score[1]) or _rating_from_score(score)
        next_action = "Review the transcript evidence and confidence before accepting this score operationally."
    elif human_requested:
        status = HUMAN
        reason = "The Excel form marks this criterion as human analysis."
        matched = _collect_matching_factors(all_factors, rule.useful_signals if rule else ())
        missing = []
        score = None
        rating = ""
        next_action = "Keep this as expert review; tool outputs may provide supporting evidence only."
    elif rule:
        required = list(rule.required_signals)
        useful = list(rule.useful_signals)
        matched = _collect_matching_factors(all_factors, tuple(required + useful))
        present_required = [signal for signal in required if _signal_available(all_factors, signal)]
        missing = [signal for signal in required if not _signal_available(all_factors, signal)]
        score = None
        rating = ""

        if not matched:
            status = UNSUPPORTED
            reason = rule.missing_explanation
        elif not missing and rule.automatic_when_required_present:
            status = AUTOMATIC
            reason = "All required signals for this rule are available."
            if rule.scoring_signal and rule.scoring_signal in all_factors:
                score = _best_factor(all_factors[rule.scoring_signal]).score
                rating = _rating_from_score(score)
        else:
            status = PARTIAL
            if present_required:
                reason = "Some required signals are available, but the criterion is not fully score-ready."
            else:
                reason = rule.missing_explanation

        next_action = rule.next_action
    else:
        matched = []
        missing = []
        score = None
        rating = ""
        status = UNSUPPORTED
        reason = "No current rule maps this Excel criterion to available tool signals."
        next_action = "Add a mapping rule after confirming how this criterion should be measured."

    detailed_signals = [_factor_detail(item) for item in matched]
    score_basis = _score_basis(status, score, rating, reason, matched, rule, direct_score, composite_score)

    return {
        "source_row": criterion.source_row,
        "criterion_id": criterion.criterion_id,
        "axis": criterion.axis,
        "criterion": criterion.name,
        "excel_evaluation_method": criterion.evaluation_method or "",
        "measurability_status": status,
        "speaker_score": round(score, 2) if isinstance(score, (int, float)) else "",
        "speaker_rating": rating,
        "available_signals": "; ".join(_format_factor(item) for item in matched),
        "detailed_signals": detailed_signals,
        "score_basis": score_basis,
        "missing_signals": "; ".join(missing),
        "reason": reason,
        "next_action": next_action,
    }


def _find_rule(criterion: RubricCriterion) -> CriterionRule | None:
    if criterion.source_row in SOURCE_ROW_RULES:
        return SOURCE_ROW_RULES[criterion.source_row]

    name_text = criterion.name
    for rule in RULES:
        if any(keyword in name_text for keyword in rule.keywords):
            return rule

    text = f"{criterion.axis} {criterion.name} {criterion.metric or ''} {criterion.equation or ''}"
    for rule in RULES:
        if any(keyword in text for keyword in rule.keywords):
            return rule
    return None


def _is_human_review(criterion: RubricCriterion) -> bool:
    method = criterion.evaluation_method or ""
    return "تحليل بشري" in method


def _factor_index(
    outputs: dict[str, NormalizedToolOutput],
) -> dict[str, list[tuple[str, FactorSignal]]]:
    index: dict[str, list[tuple[str, FactorSignal]]] = {}
    for tool, output in outputs.items():
        for factor in output.factors:
            index.setdefault(factor.factor_id, []).append((tool, factor))
    return index


def _direct_criterion_score(
    criterion: RubricCriterion,
    index: dict[str, list[tuple[str, FactorSignal]]],
) -> tuple[str, FactorSignal] | None:
    items = index.get(f"criterion_score_{criterion.source_row}", [])
    scored = [item for item in items if item[1].score is not None]
    if not scored:
        return None
    return max(scored, key=lambda item: item[1].confidence or 0)


def _composite_criterion_score(
    criterion: RubricCriterion,
    index: dict[str, list[tuple[str, FactorSignal]]],
) -> tuple[str, FactorSignal] | None:
    if criterion.source_row != 54:
        return None
    required = {
        "blink_rate": 0.20,
        "facial_expression": 0.25,
        "volume_db": 0.15,
        "pitch_variation": 0.10,
        "body_movement": 0.15,
        "filler_words": 0.15,
    }
    collected = []
    score = 0.0
    total_weight = 0.0
    for signal, weight in required.items():
        factor = _best_available_factor(index, signal)
        if not factor:
            continue
        score += float(factor.score or 0) * weight
        total_weight += weight
        collected.append(f"{signal}={round(float(factor.score or 0), 2)}")
    if total_weight < 0.70:
        return None
    composite = score / total_weight
    return (
        "composite",
        FactorSignal(
            factor_id="emotional_stability",
            factor_name="Composite emotional stability score",
            axis=criterion.axis,
            value={"components": collected},
            score=round(composite, 2),
            confidence=0.55,
            evidence=collected,
        ),
    )


def _best_available_factor(
    index: dict[str, list[tuple[str, FactorSignal]]],
    signal: str,
) -> FactorSignal | None:
    factors = [
        factor
        for _, factor in index.get(signal, [])
        if factor.score is not None and (factor.confidence is None or factor.confidence > 0)
    ]
    if not factors:
        return None
    return max(factors, key=lambda factor: factor.confidence or 0)


def _signal_available(index: dict[str, list[tuple[str, FactorSignal]]], signal: str) -> bool:
    return any(
        (factor.score is not None or factor.value is not None)
        and (factor.confidence is None or factor.confidence > 0)
        for _, factor in index.get(signal, [])
    )


def _direct_rating(factor: FactorSignal) -> str:
    if isinstance(factor.value, dict):
        rating = factor.value.get("rating")
        return str(rating) if rating else ""
    return ""


def _collect_matching_factors(
    index: dict[str, list[tuple[str, FactorSignal]]],
    wanted: tuple[str, ...],
) -> list[tuple[str, FactorSignal]]:
    matches: list[tuple[str, FactorSignal]] = []
    seen: set[tuple[str, str]] = set()
    for signal in wanted:
        for tool, factor in index.get(signal, []):
            key = (tool, factor.factor_id)
            if key in seen:
                continue
            seen.add(key)
            matches.append((tool, factor))
    return matches


def _best_factor(items: list[tuple[str, FactorSignal]]) -> FactorSignal:
    return max(items, key=lambda item: item[1].confidence or 0)[1]


def _score_basis(
    status: str,
    score: float | None,
    rating: str,
    reason: str,
    matched: list[tuple[str, FactorSignal]],
    rule: CriterionRule | None,
    direct_score: tuple[str, FactorSignal] | None,
    composite_score: tuple[str, FactorSignal] | None,
) -> dict[str, Any]:
    selected = None
    if composite_score:
        selected = _factor_detail(composite_score)
    elif direct_score:
        selected = _factor_detail(direct_score)
    elif rule and rule.scoring_signal:
        scoring_matches = [item for item in matched if item[1].factor_id == rule.scoring_signal]
        if scoring_matches:
            selected = _factor_detail((scoring_matches[0][0], _best_factor(scoring_matches)))

    return {
        "status": status,
        "score": round(score, 2) if isinstance(score, (int, float)) else None,
        "rating": rating or None,
        "reason": reason,
        "scoring_signal": rule.scoring_signal if rule else None,
        "required_signals": list(rule.required_signals) if rule else [],
        "useful_signals": list(rule.useful_signals) if rule else [],
        "selected_signal": selected,
        "calculation_note": _calculation_note(status, selected, direct_score, composite_score),
    }


def _calculation_note(
    status: str,
    selected: dict[str, Any] | None,
    direct_score: tuple[str, FactorSignal] | None,
    composite_score: tuple[str, FactorSignal] | None,
) -> str:
    if status != AUTOMATIC:
        return "No numeric score was assigned because the current evidence is not enough for an automatic score."
    if composite_score:
        return "The final score is a weighted composite of the listed normalized signals."
    if direct_score:
        return "The final score came from the rubric scorer for this exact Excel row."
    if selected:
        value = json.dumps(selected.get("value"), ensure_ascii=False, sort_keys=True)
        score = selected.get("score")
        return f"The final score used the selected signal value {value}, mapped by the tool to score {score}."
    return "The final score came from the available normalized signal for this criterion."


def _factor_detail(item: tuple[str, FactorSignal]) -> dict[str, Any]:
    tool, factor = item
    return {
        "tool": tool,
        "factor_id": factor.factor_id,
        "factor_name": factor.factor_name,
        "axis": factor.axis,
        "value": factor.value,
        "score": round(float(factor.score), 2) if factor.score is not None else None,
        "confidence": round(float(factor.confidence), 3)
        if factor.confidence is not None
        else None,
        "evidence": factor.evidence,
    }


def _format_factor(item: tuple[str, FactorSignal]) -> str:
    tool, factor = item
    score = "" if factor.score is None else f", score={round(float(factor.score), 2)}"
    confidence = "" if factor.confidence is None else f", confidence={round(float(factor.confidence), 2)}"
    return f"{tool}:{factor.factor_id}{score}{confidence}"


def _rating_from_score(score: float | None) -> str:
    if score is None:
        return ""
    if score >= 90:
        return "excellent"
    if score >= 80:
        return "very_good"
    if score >= 70:
        return "good"
    if score >= 60:
        return "needs_development"
    return "weak"


def _summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    counts = {AUTOMATIC: 0, PARTIAL: 0, HUMAN: 0, UNSUPPORTED: 0}
    for row in rows:
        counts[row["measurability_status"]] += 1
    total = len(rows)
    return {
        "total_criteria": total,
        **counts,
        "automatic_percent": round(counts[AUTOMATIC] / total * 100, 1) if total else 0,
        "partial_percent": round(counts[PARTIAL] / total * 100, 1) if total else 0,
        "human_review_percent": round(counts[HUMAN] / total * 100, 1) if total else 0,
        "unsupported_percent": round(counts[UNSUPPORTED] / total * 100, 1) if total else 0,
    }


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(_csv_row(row) for row in rows)


def _write_markdown(path: Path, report: dict[str, Any]) -> None:
    summary = report["summary"]
    rows = report["rows"]
    lines = [
        "# Thohor Rubric Scoring Readiness",
        "",
        f"Sample: `{report['sample_id']}`",
        "",
        "This report explains whether each Excel criterion is ready for speaker scoring. "
        "It does not confuse a tool being useful with the speaker receiving a final score.",
        "",
        "## Summary",
        "",
        f"- Total criteria: {summary['total_criteria']}",
        f"- Automatically measurable now: {summary[AUTOMATIC]} ({summary['automatic_percent']}%)",
        f"- Partially measurable: {summary[PARTIAL]} ({summary['partial_percent']}%)",
        f"- Human review required: {summary[HUMAN]} ({summary['human_review_percent']}%)",
        f"- Not supported by current tools: {summary[UNSUPPORTED]} ({summary['unsupported_percent']}%)",
        "",
        "## Pathway",
        "",
        "1. Read criteria from `استمارة 2026.xlsx`.",
        "2. Load normalized outputs from each tool.",
        "3. Match each Excel criterion to required and useful signals.",
        "4. Classify measurability.",
        "5. Assign a speaker score only when the signal directly supports the Excel rule.",
        "",
        "## Criteria",
        "",
        "| Row | Axis | Criterion | Status | Speaker Score | Rating | Available Signals | Missing Signals | Next Action |",
        "|---:|---|---|---|---:|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            "| {source_row} | {axis} | {criterion} | {measurability_status} | {speaker_score} | "
            "{speaker_rating} | {available_signals} | {missing_signals} | {next_action} |".format(
                **{key: _md(value) for key, value in row.items()}
            )
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _md(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def _csv_row(row: dict[str, Any]) -> dict[str, Any]:
    return {
        key: json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else value
        for key, value in row.items()
    }
