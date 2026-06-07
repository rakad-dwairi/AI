from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
WORKSPACE = PROJECT_ROOT / "phase1_validation"
SAMPLES_DIR = WORKSPACE / "samples"
OUTPUTS_DIR = WORKSPACE / "outputs"
RAW_JSON_DIR = OUTPUTS_DIR / "raw_json"
NORMALIZED_DIR = OUTPUTS_DIR / "normalized"
REPORTS_DIR = WORKSPACE / "reports"
FORM_PATH = PROJECT_ROOT / "استمارة 2026.xlsx"


def sample_dir(sample_id: str) -> Path:
    return SAMPLES_DIR / sample_id


def sample_video(sample_id: str) -> Path:
    return sample_dir(sample_id) / "input.mp4"


def raw_output_path(tool: str, sample_id: str) -> Path:
    return RAW_JSON_DIR / tool / f"{sample_id}.json"


def normalized_output_path(tool: str, sample_id: str) -> Path:
    return NORMALIZED_DIR / tool / f"{sample_id}.json"
