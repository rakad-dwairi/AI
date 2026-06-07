# Thohor Phase 1 Tool Validation Execution Plan

## 1. Phase 1 Objective

The objective of Phase 1 is **not** to build the final evaluator or generate final personality/communication scores.

The objective is to validate which ready-made tools can extract the raw factors/signals needed for later evaluation and analysis.

In this phase, we want to answer:

> Which tools can reliably extract the factors we need for the evaluation rubric?

Examples of raw factors include:

- Body movement
- Hand movement
- Face movement
- Facial expression indicators
- Speech-to-text
- Speaker timing
- Pauses
- Tone indicators
- Text/context indicators
- Video/audio quality indicators

The final scoring, interpretation, and business evaluation logic will be handled in later phases.

---

## 2. Current Constraint

The full Phase 1 duration is estimated at **2 weeks**.

Since around **4 days have already passed**, the remaining plan should focus on fast validation rather than full product development.

The priority is:

1. Test tools quickly.
2. Extract sample outputs.
3. Compare outputs against the needed evaluation factors.
4. Decide whether we can confidently move to Phase 2.

---

## 3. Phase 1 Scope

### In Scope

- Prepare 3 to 5 short video samples.
- Test each selected tool separately on the same videos.
- Extract raw factors/signals from each tool.
- Compare the quality, usefulness, and effort of each tool.
- Recommend the best tool stack for the MVP.
- Produce a short technical validation report.

### Out of Scope

- Full dashboard development.
- Final evaluation engine.
- Final scoring model.
- Dataset preparation.
- Model training.
- Fine-tuning.
- Custom gesture model development.
- Production-grade deployment.

---

## 4. Tools to Validate

| Tool | Purpose | Role in Phase 1 |
|---|---|---|
| MediaPipe | Body, hand, face, pose landmarks | Main gesture/body-language extraction candidate |
| Hume AI | Facial/vocal expression indicators | Expression and emotional-signal validation |
| Azure Video Indexer | Transcript, speaker/video/audio insights | Video/audio indexing baseline |
| AWS Rekognition | Face/person/activity detection | General video-analysis baseline |
| OpenAI / Deepgram | Transcription and text analysis | Speech-to-text and context factors |

Roboflow is intentionally excluded from Phase 1 because the current direction is **no training, no fine-tuning, and no dataset preparation**.

---

## 5. Recommended Testing Samples

Use **3 to 5 short clips**, not full long videos.

| Sample Type | Duration | Purpose |
|---|---:|---|
| Interview clip | 2–5 minutes | Face, voice, answers, body movement |
| Speech clip | 2–5 minutes | Body language, message structure, posture |
| Debate/dialogue clip | 2–5 minutes | Interruptions, speaker turns, response timing |
| Low-quality clip | 1–2 minutes | Test tool limitations and quality warnings |
| Optional high-quality clip | 2–5 minutes | Benchmark best-case results |

Each sample should include metadata:

- Speaker/person name
- Language
- Video type
- Source
- Duration
- Quality notes
- Whether the full body is visible
- Whether the face is clear
- Whether there is background noise

---

## 6. Preparation Step

For each video, prepare:

- Original video file
- Extracted audio file
- Sampled frames or low-FPS version
- Metadata file

Example commands:

```bash
ffmpeg -i input.mp4 -vn -acodec mp3 audio.mp3
ffmpeg -i input.mp4 -vf fps=2 frames/frame_%04d.jpg
```

Recommended folder structure:

```text
phase1_validation/
  samples/
    sample_01/
      input.mp4
      audio.mp3
      frames/
      metadata.json
    sample_02/
    sample_03/
  outputs/
    mediapipe/
    hume/
    aws_rekognition/
    azure_video_indexer/
    transcription/
  reports/
```

---

## 7. Remaining Execution Plan

Assuming around **6 working days remain**, the fastest execution plan is:

---

## Day 1 — Prepare Testing Package

### Goal

Prepare all test videos and make them ready for tool testing.

### Tasks

- Select 3 to 5 representative clips.
- Trim long videos into short clips.
- Extract audio.
- Extract frames or create low-FPS versions.
- Create metadata for each sample.
- Define the factor list to check per tool.

### Deliverable

A ready testing package containing videos, audio, frames, and metadata.

---

## Day 2 — Test MediaPipe

### Goal

Validate whether MediaPipe can extract body, hand, face, and movement factors without training.

### Setup

```bash
python -m venv venv
source venv/bin/activate
pip install mediapipe opencv-python pandas numpy
```

### Factors to Extract

| Factor | Expected Output |
|---|---|
| Face visibility | Visible/not visible per frame |
| Body visibility | Visible/not visible per frame |
| Hand visibility | Left/right/both/no hands |
| Hand movement | Movement intensity over time |
| Head movement | Direction and variation |
| Posture movement | Shoulder/body landmark changes |
| Movement spikes | Timestamps with high movement |

### Example Output

```json
{
  "tool": "mediapipe",
  "video_id": "sample_01",
  "factors": {
    "face_visibility_rate": 0.92,
    "hand_visibility_rate": 0.64,
    "hand_movement_intensity": "high",
    "head_movement_intensity": "medium",
    "body_movement_intensity": "low"
  },
  "timeline": []
}
```

### Decision Point

If MediaPipe gives usable movement and visibility signals, it becomes the main body-language factor extraction tool.

---

## Day 3 — Test Hume AI

### Goal

Validate whether Hume AI provides useful facial, vocal, and expression indicators.

### Setup

- Create Hume account.
- Generate API key.
- Upload or process the same video/audio clips.
- Export returned JSON.

### Factors to Extract

| Factor | Expected Output |
|---|---|
| Facial expression signals | Labels/scores over time |
| Vocal expression | Tone/emotion-like indicators |
| Expression timeline | Changes across the video |
| Emotional intensity | Trend indicators, not final judgment |

### Important Limitation

Hume should not be used to make final claims such as:

- This person is honest.
- This person is lying.
- This person is weak.
- This person is strong.

It should only be used for observable indicators such as:

- Increased expression intensity.
- More visible concern indicators.
- More smile indicators.
- More calmness-related signals.

### Decision Point

Keep Hume only if the output is understandable, useful, and adds value beyond MediaPipe and transcript analysis.

---

## Day 4 — Test AWS Rekognition and Azure Video Indexer

## AWS Rekognition

### Goal

Use AWS Rekognition as a general video-analysis baseline.

### Setup

- Create S3 bucket.
- Upload sample videos.
- Enable Rekognition access.
- Run video analysis jobs.

### Factors to Check

| Factor | Expected Usefulness |
|---|---|
| Person tracking | Useful |
| Face detection | Useful |
| Object/activity labels | Maybe useful |
| Detailed gesture detection | Weak |
| Timeline events | Useful if returned clearly |

### Decision Point

AWS Rekognition should be considered useful if it gives strong general person/face/activity baseline signals.

It is not expected to be the main detailed gesture analysis engine.

---

## Azure Video Indexer

### Goal

Use Azure Video Indexer as a video/audio indexing baseline.

### Setup

- Create Azure Video Indexer account.
- Upload same test samples through portal or API.
- Export insights JSON.

### Factors to Check

| Factor | Expected Usefulness |
|---|---|
| Transcript | Useful |
| Speaker insights | Useful |
| Topics/key moments | Useful |
| Visual insights | Useful |
| Detailed body gesture | Weak to medium |
| Timeline-based insights | Useful |

### Decision Point

Azure Video Indexer should be considered useful if it provides strong transcript, speaker, timeline, and general video insights.

---

## Day 5 — Test Speech-to-Text and Text Factors

### Goal

Validate speech-to-text quality and extract text/context factors.

### Tools

Start with:

- OpenAI transcription

Use Deepgram only if stronger diarization, timestamps, or speech analytics are needed.

### Factors to Extract

| Factor | Expected Output |
|---|---|
| Transcript | Full text |
| Timestamps | Segment-level timing |
| Speech speed | Words per minute |
| Pauses | Silence gaps |
| Filler words | Count and examples |
| Repeated phrases | Count and examples |
| Topics | Extracted topics |
| Message structure | Intro/body/closing |
| Answer relevance | Based on transcript |

### Example Output

```json
{
  "tool": "transcription_openai",
  "video_id": "sample_01",
  "factors": {
    "words_per_minute": 142,
    "pause_count": 17,
    "long_pause_count": 4,
    "filler_word_count": 12,
    "main_topics": ["economy", "public services"],
    "answer_structure": "medium"
  }
}
```

### Decision Point

The transcription/text-analysis layer is mandatory for the MVP if it gives acceptable Arabic/English transcription quality and timestamped output.

---

## Day 6 — Compare Results and Prepare Recommendation

### Goal

Compare all tools against the needed factor list and recommend the MVP tool stack.

### Comparison Table Template

| Factor | MediaPipe | Hume AI | AWS Rekognition | Azure Video Indexer | OpenAI/Deepgram | Best Tool |
|---|---|---|---|---|---|---|
| Hand movement | Strong | Weak | Weak | Weak | N/A | MediaPipe |
| Face expression | Medium | Strong | Medium | Medium | N/A | Hume/MediaPipe |
| Body movement | Strong | Weak | Weak | Weak | N/A | MediaPipe |
| Transcript | N/A | Medium | Weak | Strong | Strong | OpenAI/Azure |
| Speaker timing | N/A | Medium | Weak | Strong | Medium | Azure/Deepgram |
| Context analysis | N/A | Medium | N/A | Medium | Strong | OpenAI |
| General video indexing | Weak | Medium | Strong | Strong | N/A | Azure/AWS |

### Deliverables

- Factor extraction matrix.
- Raw JSON samples from each tool.
- Strengths and weaknesses per tool.
- Cost/effort notes.
- Recommended MVP tool stack.
- Go/no-go decision for Phase 2.

---

## 8. Recommended Fast Testing Architecture

For Phase 1, keep the setup simple.

```text
Local machine or Huawei ECS
        |
        |-- input videos
        |
        |-- MediaPipe script
        |-- Hume API script
        |-- AWS Rekognition test/manual script
        |-- Azure Video Indexer test/manual/API export
        |-- Transcription script
        |
        |-- outputs/
              |-- raw_json/
              |-- factor_summary.csv
              |-- comparison_report.docx/pdf
```

Do not build a full backend or dashboard during Phase 1 unless absolutely necessary.

---

## 9. Best Testing Method

Use the same sample videos for every tool.

For each tool, answer these five questions:

1. What factors can it extract?
2. Is the output machine-readable JSON?
3. Is the result understandable to the team?
4. Does it work well on Arabic/interview-style videos?
5. Is the quality enough to move forward?

---

## 10. Go / No-Go Criteria

Move to Phase 2 only if the following are satisfied:

| Criteria | Minimum Acceptable Result |
|---|---|
| Body/gesture factors | MediaPipe gives usable movement signals |
| Face/expression factors | Hume or MediaPipe gives usable indicators |
| Transcript/context | OpenAI/Azure gives strong transcript and text factors |
| Timeline support | At least 2 tools return timestamped outputs |
| Expert acceptance | Around 75% practical usefulness |
| Cost | Acceptable for pilot usage |
| Integration effort | Feasible within MVP timeline |

---

## 11. Recommended MVP Tool Stack After Successful Phase 1

If Phase 1 succeeds, the expected MVP stack should be:

| Layer | Recommended Tool |
|---|---|
| Video storage | Huawei OBS |
| Processing workers | Huawei ECS |
| Body/gesture extraction | MediaPipe |
| Expression/voice indicators | Hume AI, if useful |
| Transcription | OpenAI or Azure/Deepgram |
| Text/context analysis | OpenAI |
| General video baseline | Azure Video Indexer or AWS Rekognition if useful |
| Final report generation | OpenAI |

---

## 12. Final Phase 1 Success Statement

At the end of Phase 1, we should be able to say:

> We tested the candidate tools on real sample videos, identified which tools can extract the required analysis factors, confirmed the technical feasibility of the extraction pipeline, and selected the recommended stack for building the MVP in Phase 2.

---

## 13. Final Recommendation

The fastest and safest direction is:

> Extract factors → compare tool outputs → select MVP stack.

Not:

> Build full evaluator → build dashboard → calculate final score.

This keeps Phase 1 realistic, reduces risk, and gives enough evidence to move to Phase 2 with confidence.
