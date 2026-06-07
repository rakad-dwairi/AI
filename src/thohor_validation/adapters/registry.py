from __future__ import annotations

from .aws_adapter import AWSRekognitionAdapter
from .azure_adapter import AzureVideoIndexerAdapter
from .base import ToolAdapter
from .deepgram_adapter import DeepgramAdapter
from .hume_adapter import HumeAdapter
from .import_adapter import ImportOnlyAdapter
from .local_audio_adapter import LocalAudioAdapter
from .mediapipe_adapter import MediaPipeAdapter
from .openai_adapter import OpenAIAdapter
from .openai_rubric_adapter import OpenAIRubricAdapter


def get_adapter(tool: str) -> ToolAdapter:
    adapters: dict[str, ToolAdapter] = {
        "mediapipe": MediaPipeAdapter(),
        "openai": OpenAIAdapter(),
        "deepgram": DeepgramAdapter(),
        "hume": HumeAdapter(),
        "aws_rekognition": AWSRekognitionAdapter(),
        "azure_video_indexer": AzureVideoIndexerAdapter(),
        "local_audio": LocalAudioAdapter(),
        "openai_rubric": OpenAIRubricAdapter(),
    }
    if tool in adapters:
        return adapters[tool]
    return ImportOnlyAdapter(tool)


def known_tools() -> list[str]:
    return [
        "mediapipe",
        "local_audio",
        "hume",
        "aws_rekognition",
        "azure_video_indexer",
        "openai",
        "openai_rubric",
        "deepgram",
    ]
