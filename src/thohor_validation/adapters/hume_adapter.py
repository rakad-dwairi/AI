from __future__ import annotations

import os

from thohor_validation.core.models import ToolRunResult

from .import_adapter import ImportOnlyAdapter


class HumeAdapter(ImportOnlyAdapter):
    name = "hume"

    def __init__(self) -> None:
        super().__init__(self.name)

    def run(self, sample_id: str) -> ToolRunResult:
        imported = super().run(sample_id)
        if imported.status == "imported":
            return imported
        if not os.getenv("HUME_API_KEY"):
            return ToolRunResult(tool=self.name, sample_id=sample_id, status="skipped", message="HUME_API_KEY is not configured. Export Hume JSON into raw_json/hume or add credentials.")
        return ToolRunResult(tool=self.name, sample_id=sample_id, status="skipped", message="Hume credentials found; API job wiring should be completed after final Hume account/workflow choice.")
