from __future__ import annotations

from pathlib import Path

from thohor_validation.core.paths import REPORTS_DIR


def remove_report_files(sample_id: str, suffixes: tuple[str, ...]) -> None:
    for suffix in suffixes:
        for extension in ("json", "csv", "md"):
            path = REPORTS_DIR / f"{sample_id}_{suffix}.{extension}"
            if path.exists():
                path.unlink()
