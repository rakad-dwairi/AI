from __future__ import annotations

import shutil
from pathlib import Path

import click
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

from thohor_validation.adapters.registry import get_adapter, known_tools
from thohor_validation.core.io import load_metadata, require_ffmpeg, run_command, save_metadata, write_json
from thohor_validation.core.models import SampleMetadata
from thohor_validation.core.paths import FORM_PATH, REPORTS_DIR, SAMPLES_DIR, normalized_output_path, sample_dir, sample_video
from thohor_validation.core.rubric import load_form_criteria, load_rubric_levels
from thohor_validation.reporting.evaluation import build_speaker_evaluation
from thohor_validation.reporting.report import build_report
from thohor_validation.reporting.rubric_engine import build_rubric_readiness_report


console = Console()
DEFAULT_EVALUATION_TOOLS = (
    "mediapipe",
    "local_audio",
    "openai",
    "deepgram",
    "openai_rubric",
    "aws_rekognition",
)

@click.group()
def cli() -> None:
    load_dotenv()


@cli.command("inspect-form")
def inspect_form() -> None:
    criteria = load_form_criteria(FORM_PATH)
    levels = load_rubric_levels(FORM_PATH)
    console.print(f"Loaded [bold]{len(criteria)}[/bold] tool-capture criteria.")
    console.print(f"Loaded [bold]{len(levels)}[/bold] rubric rows.")
    table = Table("Row", "Axis", "Criterion")
    for criterion in criteria[:20]:
        table.add_row(str(criterion.source_row), criterion.axis, criterion.name)
    console.print(table)


@cli.command("init-sample")
@click.argument("sample_id")
@click.option("--video", "video_path", type=click.Path(exists=True, dir_okay=False), required=True)
@click.option("--language", default="ar", show_default=True)
@click.option("--video-type", default="interview", show_default=True)
@click.option("--speaker-name", default=None)
@click.option("--source", default=None)
@click.option("--expected-duration", type=float, default=None, help="Expected duration in seconds.")
def init_sample(sample_id: str, video_path: str, language: str, video_type: str, speaker_name: str | None, source: str | None, expected_duration: float | None) -> None:
    directory = sample_dir(sample_id)
    directory.mkdir(parents=True, exist_ok=True)
    shutil.copy2(video_path, sample_video(sample_id))
    metadata = SampleMetadata(
        sample_id=sample_id,
        language=language,
        video_type=video_type,
        speaker_name=speaker_name,
        source=source,
        expected_duration_seconds=expected_duration,
    )
    path = save_metadata(metadata)
    console.print(f"Sample created: {directory}")
    console.print(f"Metadata: {path}")


@cli.command("prepare-sample")
@click.argument("sample_id")
def prepare_sample(sample_id: str) -> None:
    require_ffmpeg()
    video = sample_video(sample_id)
    if not video.exists():
        raise click.ClickException(f"Missing video: {video}")
    directory = sample_dir(sample_id)
    frames_dir = directory / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    run_command(["ffmpeg", "-y", "-i", str(video), "-vn", "-acodec", "mp3", str(directory / "audio.mp3")])
    run_command(["ffmpeg", "-y", "-i", str(video), "-vf", "fps=2", str(frames_dir / "frame_%04d.jpg")])
    console.print(f"Prepared audio and frames for {sample_id}.")


def _run_and_normalize(sample_id: str, tool: str) -> None:
    adapter = get_adapter(tool)
    result = adapter.run(sample_id)
    console.print(result.model_dump())
    if result.status in {"ok", "imported"}:
        normalized = adapter.normalize(sample_id)
        path = normalized_output_path(tool, sample_id)
        write_json(path, normalized.model_dump())
        console.print(f"Normalized output: {path}")


@cli.command("run-tool")
@click.argument("sample_id")
@click.argument("tool")
def run_tool(sample_id: str, tool: str) -> None:
    _run_and_normalize(sample_id, tool)


@cli.command("run-all")
@click.argument("sample_id")
def run_all(sample_id: str) -> None:
    for tool in known_tools():
        console.rule(tool)
        _run_and_normalize(sample_id, tool)


@cli.command("normalize")
@click.argument("sample_id")
@click.argument("tool")
def normalize(sample_id: str, tool: str) -> None:
    adapter = get_adapter(tool)
    normalized = adapter.normalize(sample_id)
    path = normalized_output_path(tool, sample_id)
    write_json(path, normalized.model_dump())
    console.print(f"Normalized output: {path}")


@cli.command("report")
@click.argument("sample_id")
def report(sample_id: str) -> None:
    result = build_report(sample_id)
    console.print(f"Report rows: {len(result['rows'])}")
    console.print(f"JSON: {REPORTS_DIR / f'{sample_id}_comparison.json'}")
    console.print(f"CSV: {REPORTS_DIR / f'{sample_id}_comparison.csv'}")
    console.print(f"Markdown: {REPORTS_DIR / f'{sample_id}_summary.md'}")


@cli.command("rubric-readiness")
@click.argument("sample_id")
def rubric_readiness(sample_id: str) -> None:
    result = build_rubric_readiness_report(sample_id)
    summary = result["summary"]
    console.print(f"Rubric criteria: {summary['total_criteria']}")
    console.print(f"Automatically measurable: {summary['automatically_measurable']}")
    console.print(f"Partially measurable: {summary['partially_measurable']}")
    console.print(f"Human review required: {summary['human_review_required']}")
    console.print(f"Not supported: {summary['not_supported_by_current_tools']}")
    console.print(f"JSON: {REPORTS_DIR / f'{sample_id}_rubric_readiness.json'}")
    console.print(f"CSV: {REPORTS_DIR / f'{sample_id}_rubric_readiness.csv'}")
    console.print(f"Markdown: {REPORTS_DIR / f'{sample_id}_rubric_readiness.md'}")


@cli.command("evaluate")
@click.argument("sample_id")
def evaluate(sample_id: str) -> None:
    result = build_speaker_evaluation(sample_id)
    summary = result["summary"]
    console.print(f"Evaluation criteria: {summary['total_criteria']}")
    console.print(f"Scored automatically: {summary['scored']}")
    console.print(f"Partial evidence only: {summary['partial_evidence_only']}")
    console.print(f"Human review required: {summary['human_review_required']}")
    console.print(f"Not supported: {summary['not_supported']}")
    console.print(f"Average score for scored criteria: {summary['average_score_for_scored_criteria']}")
    console.print(f"JSON: {REPORTS_DIR / f'{sample_id}_speaker_evaluation.json'}")
    console.print(f"CSV: {REPORTS_DIR / f'{sample_id}_speaker_evaluation.csv'}")
    console.print(f"Markdown: {REPORTS_DIR / f'{sample_id}_speaker_evaluation.md'}")


@cli.command("evaluate-video")
@click.argument("sample_id")
@click.option("--video", "video_path", type=click.Path(exists=True, dir_okay=False), required=True)
@click.option("--language", default="ar", show_default=True)
@click.option("--video-type", default="interview", show_default=True)
@click.option("--speaker-name", default=None)
@click.option("--source", default=None)
@click.option("--expected-duration", type=float, default=None, help="Expected duration in seconds.")
@click.option(
    "--tool",
    "tools",
    multiple=True,
    help="Tool to run. Can be passed multiple times. Defaults to the stable evaluation tools.",
)
def evaluate_video(
    sample_id: str,
    video_path: str,
    language: str,
    video_type: str,
    speaker_name: str | None,
    source: str | None,
    expected_duration: float | None,
    tools: tuple[str, ...],
) -> None:
    selected_tools = tools or DEFAULT_EVALUATION_TOOLS
    directory = sample_dir(sample_id)
    directory.mkdir(parents=True, exist_ok=True)
    shutil.copy2(video_path, sample_video(sample_id))
    save_metadata(
        SampleMetadata(
            sample_id=sample_id,
            language=language,
            video_type=video_type,
            speaker_name=speaker_name,
            source=source,
            expected_duration_seconds=expected_duration,
        )
    )
    console.print(f"Sample created: {directory}")

    require_ffmpeg()
    frames_dir = directory / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    run_command(["ffmpeg", "-y", "-i", str(sample_video(sample_id)), "-vn", "-acodec", "mp3", str(directory / "audio.mp3")])
    run_command(["ffmpeg", "-y", "-i", str(sample_video(sample_id)), "-vf", "fps=2", str(frames_dir / "frame_%04d.jpg")])
    console.print(f"Prepared audio and frames for {sample_id}.")

    for tool in selected_tools:
        console.rule(tool)
        _run_and_normalize(sample_id, tool)

    build_report(sample_id)
    build_rubric_readiness_report(sample_id)
    result = build_speaker_evaluation(sample_id)
    summary = result["summary"]
    console.rule("evaluation")
    console.print(f"Evaluation criteria: {summary['total_criteria']}")
    console.print(f"Scored automatically: {summary['scored']}")
    console.print(f"Partial evidence only: {summary['partial_evidence_only']}")
    console.print(f"Human review required: {summary['human_review_required']}")
    console.print(f"Not supported: {summary['not_supported']}")
    console.print(f"Markdown: {REPORTS_DIR / f'{sample_id}_speaker_evaluation.md'}")


@cli.command("list-samples")
def list_samples() -> None:
    table = Table("Sample", "Language", "Type", "Speaker")
    for path in sorted(SAMPLES_DIR.glob("*/metadata.json")):
        metadata = load_metadata(path.parent.name)
        table.add_row(metadata.sample_id, metadata.language, metadata.video_type, metadata.speaker_name or "")
    console.print(table)


if __name__ == "__main__":
    cli()
