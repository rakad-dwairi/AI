from __future__ import annotations

import os

from thohor_validation.core.models import ToolRunResult

from .import_adapter import ImportOnlyAdapter


class AzureVideoIndexerAdapter(ImportOnlyAdapter):
    name = "azure_video_indexer"

    def __init__(self) -> None:
        super().__init__(self.name)

    def run(self, sample_id: str) -> ToolRunResult:
        imported = super().run(sample_id)
        if imported.status == "imported":
            return imported
        required = [
            "AZURE_VIDEO_INDEXER_ACCOUNT_ID",
            "AZURE_VIDEO_INDEXER_LOCATION",
            "AZURE_VIDEO_INDEXER_ACCESS_TOKEN",
        ]
        missing = [key for key in required if not os.getenv(key)]
        if missing:
            return ToolRunResult(tool=self.name, sample_id=sample_id, status="skipped", message=f"Azure Video Indexer config missing: {', '.join(missing)}. You can import exported JSON.")
        return ToolRunResult(tool=self.name, sample_id=sample_id, status="skipped", message="Azure config detected; API upload can be enabled after confirming account endpoint/version.")
