from __future__ import annotations

from thohor_validation.core.io import read_json
from thohor_validation.core.models import FactorSignal, NormalizedToolOutput, ToolRunResult
from thohor_validation.core.paths import raw_output_path

from .base import ToolAdapter


class ImportOnlyAdapter(ToolAdapter):
    """Adapter for tools where Phase 1 may export JSON manually from a vendor portal."""

    name = "import"

    def __init__(self, name: str):
        self.name = name

    def run(self, sample_id: str) -> ToolRunResult:
        path = raw_output_path(self.name, sample_id)
        if path.exists():
            return ToolRunResult(
                tool=self.name,
                sample_id=sample_id,
                status="imported",
                raw_path=str(path),
                message="Existing raw JSON found.",
            )
        return ToolRunResult(
            tool=self.name,
            sample_id=sample_id,
            status="skipped",
            message=f"Place exported JSON at {path} and run normalize/report.",
        )

    def normalize(self, sample_id: str) -> NormalizedToolOutput:
        raw = read_json(raw_output_path(self.name, sample_id))
        factors: list[FactorSignal] = []
        text = str(raw).lower()

        if "transcript" in text:
            factors.append(
                FactorSignal(
                    factor_id="transcript",
                    factor_name="Transcript availability",
                    axis="المحتوى",
                    value=True,
                    score=80,
                    confidence=0.5,
                    evidence=["Transcript-like field found in raw JSON."],
                )
            )
        if "face" in text:
            factors.append(
                FactorSignal(
                    factor_id="face_detection",
                    factor_name="Face detection",
                    axis="لغة الجسد",
                    value=True,
                    score=75,
                    confidence=0.5,
                    evidence=["Face-like field found in raw JSON."],
                )
            )
        if "speaker" in text:
            factors.append(
                FactorSignal(
                    factor_id="speaker_timing",
                    factor_name="Speaker timing",
                    axis="الحوار",
                    value=True,
                    score=75,
                    confidence=0.5,
                    evidence=["Speaker-like field found in raw JSON."],
                )
            )

        return NormalizedToolOutput(
            tool=self.name,
            sample_id=sample_id,
            factors=factors,
            notes=["Generic import normalization. Add a specialized mapper after seeing vendor JSON."],
        )
