from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


class SampleMetadata(BaseModel):
    sample_id: str
    video_file: str = "input.mp4"
    language: str = "ar"
    video_type: str = "interview"
    source: str | None = None
    speaker_name: str | None = None
    duration_seconds: float | None = None
    expected_duration_seconds: float | None = None
    quality_notes: str | None = None
    full_body_visible: bool | None = None
    face_clear: bool | None = None
    background_noise: str | None = None


class ToolRunResult(BaseModel):
    tool: str
    sample_id: str
    status: str
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    raw_path: str | None = None
    normalized_path: str | None = None
    message: str | None = None
    data: dict[str, Any] = Field(default_factory=dict)


class FactorSignal(BaseModel):
    factor_id: str
    factor_name: str
    axis: str | None = None
    value: Any = None
    score: float | None = None
    confidence: float | None = None
    evidence: list[str] = Field(default_factory=list)


class NormalizedToolOutput(BaseModel):
    tool: str
    sample_id: str
    status: str = "ok"
    factors: list[FactorSignal] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
