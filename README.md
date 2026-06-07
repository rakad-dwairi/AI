# Thohor Phase 1 Validation Project

This project validates which AI tools can extract the raw signals needed by `استمارة 2026.xlsx`.

The target workflow is:

```text
video file -> AI/API extraction -> Excel-based criterion evaluation -> final report
```

The Excel file `استمارة 2026.xlsx` is the evaluation reference. The tool does not invent its own criteria; it reads the criteria from the workbook and evaluates each row using the available tool outputs.

## What This Tool Does

For a shared video, the project can:

1. Register the video as a sample.
2. Extract audio and frames.
3. Run the configured tools/APIs.
4. Normalize raw API outputs into comparable signals.
5. Match those signals to the Excel criteria.
6. Generate a full per-criterion speaker evaluation report.

Every Excel criterion receives a result:

- A numeric score/rating when the current signals support scoring.
- A partial evidence result when useful signals exist but scoring is not fair yet.
- A human-review result when the Excel file calls for expert judgment.
- A not-supported result when current tools do not support the criterion yet.

## Full Video Evaluation

Use this when you want the closest current version of:

```text
upload video -> full evaluation for each Excel criterion
```

Example with `VideoOne`:

```bash
thohor evaluate-video sample_01 --video "Videos/VideoOne.MP4" --language ar --video-type interview
```

By default this runs the stable evaluation tools:

- `mediapipe` / OpenCV fallback for visual motion support.
- MediaPipe task models for pose, hand, and face landmarks when available in `phase1_validation/models/`.
- `local_audio` for volume and silence metrics.
- `openai` for transcription/text support.
- `deepgram` for transcript timing, WPM, pauses, and speaker timing.
- `openai_rubric` for transcript-based Excel rubric scoring.
- `aws_rekognition` for face detection, head-pose/gaze proxies, sampled-frame face attributes, and general video labels.

It then writes:

```text
phase1_validation/reports/sample_01_speaker_evaluation.md
phase1_validation/reports/sample_01_speaker_evaluation.csv
phase1_validation/reports/sample_01_speaker_evaluation.json
```

The speaker evaluation report is intentionally detailed. For every criterion it includes:

- The final score and rating, when scoring is supported.
- The selected scoring signal that produced the score.
- The measured value behind that score, such as words per minute, pause rate, pitch range, hand movement event count, hand visibility, body movement events, smile rate, or duration.
- All supporting signals from the available tools, with tool name, value, score, confidence, and evidence.
- A calculation note explaining what the score depended on.
- The next action when the current signal is only a proxy or needs future refinement.

The current evaluation is honest about limitations. It scores only criteria that have enough supporting signal. For the remaining criteria, it explains what is missing and what technical work is required.

Transcript-based rubric scoring currently covers content/question criteria when the transcript has enough evidence. Visual/body-language criteria use MediaPipe landmarks and AWS face attributes where available. Vocal criteria use local audio pitch/volume proxies.

For criteria that depend on context, pass metadata. For example, duration suitability needs an expected duration:

```bash
thohor evaluate-video sample_02 --video "Videos/C3323.MP4" --language ar --video-type interview --expected-duration 60
```

Some rows in `استمارة 2026.xlsx` are marked as human analysis. The tool keeps those as `human_review_required` unless the rubric is changed or an explicit AI-review layer is added for them.

## Manual Step-by-Step Flow

The step-by-step flow is:

1. Put short videos in `phase1_validation/samples/<sample_id>/input.mp4`.
2. Add sample metadata with `thohor init-sample`.
3. Run the same sample through the configured tools.
4. Normalize each tool output into factor signals.
5. Compare tool coverage/alignment against the Excel form.
6. Generate CSV/Markdown reports for choosing the MVP tool stack.

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env
```

Create a sample:

```bash
thohor init-sample sample_01 --video /path/to/video.mp4 --language ar --video-type interview
```

Extract audio and frames:

```bash
thohor prepare-sample sample_01
```

Run local MediaPipe:

```bash
thohor run-tool sample_01 mediapipe
```

Run every configured tool:

```bash
thohor run-all sample_01
```

Generate the final speaker evaluation:

```bash
thohor evaluate sample_01
```

Build the comparison report:

```bash
thohor report sample_01
```

Build the rubric scoring-readiness report:

```bash
thohor rubric-readiness sample_01
```

This report is different from the tool comparison report:

- `thohor report` answers: which tool produced useful signals for each Excel criterion?
- `thohor rubric-readiness` answers: can we score the speaker against this criterion now?
- `thohor evaluate` answers: what is the final per-criterion evaluation result for this sample?

Each Excel criterion is classified as:

- `automatically_measurable`: current signals can directly support a speaker score.
- `partially_measurable`: useful signals exist, but something important is missing.
- `human_review_required`: the Excel form itself requires expert judgment.
- `not_supported_by_current_tools`: no current tool output supports this criterion yet.

Current local/audio scoring signals include:

- `words_per_minute` from Deepgram word timestamps.
- `pause_count` and `pause_rate` from gaps between Deepgram words.
- `actual_duration` from Deepgram timing.
- `volume_db` from local `ffmpeg` analysis.
- `audio_silence_events` from local `ffmpeg` silence detection.
- `pitch_range_hz` and `pitch_variation` from local audio pitch estimation.
- MediaPipe landmark signals for posture, body movement, hand visibility, hand movement, repeated body motion, and foot stance.
- AWS face/head-pose signals for gaze direction, gaze distribution, eye-contact stability, facial expression, smile rate, smile authenticity, and blink proxy.

The readiness report writes:

```text
phase1_validation/reports/<sample_id>_rubric_readiness.md
phase1_validation/reports/<sample_id>_rubric_readiness.csv
phase1_validation/reports/<sample_id>_rubric_readiness.json
```

## Cloud Tools

Some tools require accounts or exported JSON:

- `mediapipe`: local, works from video frames.
- `openai`: uses OpenAI transcription and optional text analysis.
- `deepgram`: uses Deepgram when `DEEPGRAM_API_KEY` is available.
- `hume`: creates a clear placeholder unless `HUME_API_KEY` is configured; API integration point is ready.
- `aws_rekognition`: expects AWS credentials, an S3 bucket, and Rekognition permissions.
- `azure_video_indexer`: supports importing exported Azure Video Indexer JSON now; API upload can be added once account settings are final.

Manual/exported raw JSON can be placed at:

```text
phase1_validation/outputs/raw_json/<tool>/<sample_id>.json
```

Then run:

```bash
thohor normalize sample_01 <tool>
thohor report sample_01
```
