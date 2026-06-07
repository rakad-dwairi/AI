from __future__ import annotations

from abc import ABC, abstractmethod

from thohor_validation.core.models import NormalizedToolOutput, ToolRunResult


class ToolAdapter(ABC):
    name: str

    @abstractmethod
    def run(self, sample_id: str) -> ToolRunResult:
        raise NotImplementedError

    @abstractmethod
    def normalize(self, sample_id: str) -> NormalizedToolOutput:
        raise NotImplementedError
