from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

from .models import SampleMetadata
from .paths import sample_dir


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    ensure_parent(path)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )


def load_metadata(sample_id: str) -> SampleMetadata:
    path = sample_dir(sample_id) / "metadata.json"
    return SampleMetadata.model_validate(read_json(path))


def save_metadata(metadata: SampleMetadata) -> Path:
    path = sample_dir(metadata.sample_id) / "metadata.json"
    write_json(path, metadata.model_dump())
    return path


def require_ffmpeg() -> None:
    if not shutil.which("ffmpeg"):
        raise RuntimeError("ffmpeg is required for prepare-sample but was not found in PATH.")


def run_command(args: list[str]) -> None:
    subprocess.run(args, check=True)
