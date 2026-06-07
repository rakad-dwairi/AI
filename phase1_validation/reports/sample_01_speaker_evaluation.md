# Thohor Speaker Evaluation

Sample: `sample_01`
Reference: `استمارة 2026.xlsx`

This report gives a result for every Excel criterion. A numeric score is only assigned when the current signals can support the rubric rule. Partial, human-review, and unsupported criteria are still included with evidence and next action.

## Summary

- Total criteria: 44
- Scored automatically: 33 (75.0%)
- Partial evidence only: 0
- Human review required: 11
- Not supported: 0
- Average score for scored criteria: 73.5

## How To Read This

- `scored`: the current data supports a numeric speaker score.
- `partial_evidence_only`: the tool found useful evidence, but not enough for a fair score.
- `human_review_required`: the Excel file calls for expert judgment.
- `not_supported`: current tools do not support this criterion yet.
- `Score basis`: the exact signal used for the score, including measured value, signal score, confidence, and evidence.

## Criteria Evaluation

| Row | Axis | Criterion | Status | Score | Rating | Result | Evidence | Missing Data |
|---:|---|---|---|---:|---|---|---|---|
| 11 | الأداء الصوتي | وضوح المخارج | scored | 50.0 | weak | Score 50.0 / weak | openai:pronunciation_clarity, score=50.0, confidence=0.4; openai:transcript, score=100.0, confidence=0.8; deepgram:transcript, score=100.0, confidence=0.8 |  |
| 12 | الأداء الصوتي | وضوح المخارج | scored | 50.0 | weak | Score 50.0 / weak | openai:weak_letter_detection, score=50.0, confidence=0.3; openai:transcript, score=100.0, confidence=0.8; deepgram:transcript, score=100.0, confidence=0.8 |  |
| 13 | الأداء الصوتي | نبرة الصوت التلوين ( تعريفها: وجود مشاعر في الصوت) | scored | 90.0 | excellent | Score 90.0 / excellent | local_audio:pitch_variation, score=90.0, confidence=0.5; openai:transcript, score=100.0, confidence=0.8; deepgram:transcript, score=100.0, confidence=0.8 |  |
| 14 | الأداء الصوتي | مستوى الصوت | scored | 80.0 | very_good | Score 80.0 / very_good | local_audio:volume_db, score=80.0, confidence=0.65 |  |
| 15 | الأداء الصوتي | الوقفات و التنفس | scored | 60.0 | needs_development | Score 60.0 / needs_development | deepgram:pause_count, score=60.0, confidence=0.7; deepgram:pause_rate, score=60.0, confidence=0.7; deepgram:speaker_timing, score=85.0, confidence=0.7; openai:transcript, score=100.0, confidence=0.8; deepgram:transcript, score=100.0, confidence=0.8; deepgram:words_per_minute, score=90.0, confidence=0.7; local_audio:audio_silence_events, confidence=0.55 |  |
| 17 | الأداء الصوتي | خامة الصوت | scored | 90.0 | excellent | Score 90.0 / excellent | local_audio:pitch_range_hz, score=90.0, confidence=0.55; local_audio:pitch_variation, score=90.0, confidence=0.5 |  |
| 19 | الأداء الصوتي | السرعة | scored | 90.0 | excellent | Score 90.0 / excellent | deepgram:words_per_minute, score=90.0, confidence=0.7; openai:transcript, score=100.0, confidence=0.8; deepgram:transcript, score=100.0, confidence=0.8 |  |
| 20 | لغة الجسد | المظهر العام | human_review_required |  |  | Not auto-scored; the Excel criterion requires expert judgment. |  |  |
| 21 | لغة الجسد | الثقة الإنطباع الأولى و الثبات الانفعالي | human_review_required |  |  | Not auto-scored; the Excel criterion requires expert judgment. | aws_rekognition:face_detection, score=90.0, confidence=0.75; mediapipe:face_visibility, score=0.0, confidence=0.8 |  |
| 22 | لغة الجسد | لغة جسد منضبطة | scored | 93.4 | excellent | Score 93.4 / excellent | mediapipe:posture, score=93.4, confidence=0.65; mediapipe:body_visibility, score=98.57, confidence=0.85; mediapipe:body_movement, score=90.0, confidence=0.7 |  |
| 23 | لغة الجسد | لغة جسد منضبطة | scored | 55.0 | weak | Score 55.0 / weak | mediapipe:body_repetition_rate, score=55.0, confidence=0.6; mediapipe:body_movement, score=90.0, confidence=0.7; mediapipe:body_visibility, score=98.57, confidence=0.85; mediapipe:posture, score=93.4, confidence=0.65 |  |
| 24 | لغة الجسد | لغة جسد منضبطة | scored | 68.22 | needs_development | Score 68.22 / needs_development | mediapipe:foot_stance_width, score=68.22, confidence=0.45; mediapipe:body_visibility, score=98.57, confidence=0.85; mediapipe:posture, score=93.4, confidence=0.65 |  |
| 25 | لغة الجسد | اتصال بصري( توزيع النظرات، معدل رمش) | scored | 50.0 | weak | Score 50.0 / weak | aws_rekognition:gaze_direction, score=50.0, confidence=0.55; aws_rekognition:face_detection, score=90.0, confidence=0.75 |  |
| 26 | لغة الجسد | اتصال بصري( توزيع النظرات، معدل رمش) | scored | 50.19 | weak | Score 50.19 / weak | aws_rekognition:gaze_distribution, score=50.19, confidence=0.5; aws_rekognition:face_detection, score=90.0, confidence=0.75 |  |
| 27 | لغة الجسد | اتصال بصري( توزيع النظرات، معدل رمش) | scored | 50.0 | weak | Score 50.0 / weak | aws_rekognition:eye_contact_stability, score=50.0, confidence=0.5; aws_rekognition:face_detection, score=90.0, confidence=0.75 |  |
| 28 | لغة الجسد | اتصال بصري( توزيع النظرات، معدل رمش) | scored | 50.0 | weak | Score 50.0 / weak | mediapipe:blink_rate, score=50.0, confidence=0.0; aws_rekognition:blink_rate, score=50.0, confidence=0.45; aws_rekognition:face_detection, score=90.0, confidence=0.75; mediapipe:face_visibility, score=0.0, confidence=0.8 |  |
| 29 | لغة الجسد | الإيماءات و توظيف حركة اليدين | scored | 82.0 | very_good | Score 82.0 / very_good | mediapipe:gesture_classification, score=82.0, confidence=0.45; mediapipe:hand_visibility, score=94.29, confidence=0.85; mediapipe:hand_movement, score=85.0, confidence=0.75 |  |
| 30 | لغة الجسد | الإيماءات و توظيف حركة اليدين | scored | 85.0 | very_good | Score 85.0 / very_good | mediapipe:hand_movement, score=85.0, confidence=0.75; mediapipe:hand_visibility, score=94.29, confidence=0.85; mediapipe:body_movement, score=90.0, confidence=0.7 |  |
| 31 | لغة الجسد | الإيماءات و توظيف حركة اليدين | scored | 82.0 | very_good | Score 82.0 / very_good | mediapipe:gesture_classification, score=82.0, confidence=0.45; mediapipe:hand_visibility, score=94.29, confidence=0.85; mediapipe:hand_movement, score=85.0, confidence=0.75 |  |
| 32 | لغة الجسد | الإيماءات و توظيف حركة اليدين | human_review_required |  |  | Not auto-scored; the Excel criterion requires expert judgment. | mediapipe:hand_visibility, score=94.29, confidence=0.85; mediapipe:body_movement, score=90.0, confidence=0.7 |  |
| 33 | لغة الجسد | تعابير الوجه و الابتسامة | scored | 100.0 | excellent | Score 100.0 / excellent | aws_rekognition:facial_expression, score=100.0, confidence=0.55; aws_rekognition:face_detection, score=90.0, confidence=0.75 |  |
| 34 | لغة الجسد | تعابير الوجه و الابتسامة | scored | 95.0 | excellent | Score 95.0 / excellent | mediapipe:smile_rate, score=60.0, confidence=0.0; aws_rekognition:smile_rate, score=95.0, confidence=0.55; aws_rekognition:face_detection, score=90.0, confidence=0.75 |  |
| 35 | لغة الجسد | تعابير الوجه و الابتسامة | scored | 95.09 | excellent | Score 95.09 / excellent | aws_rekognition:smile_authenticity, score=95.09, confidence=0.45; mediapipe:smile_rate, score=60.0, confidence=0.0; aws_rekognition:smile_rate, score=95.0, confidence=0.55; aws_rekognition:face_detection, score=90.0, confidence=0.75 |  |
| 36 | لغة الجسد | تعابير الوجه و الابتسامة | human_review_required |  |  | Not auto-scored; the Excel criterion requires expert judgment. | mediapipe:face_visibility, score=0.0, confidence=0.8; aws_rekognition:face_detection, score=90.0, confidence=0.75 |  |
| 37 | المحتوى | الرسائل الاتصالية | scored | 85.0 | very_good | Score 85.0 / very_good | openai_rubric:criterion_score_37, score=85.0, confidence=0.9 |  |
| 38 | المحتوى | الرسائل الاتصالية | scored | 30.0 | weak | Score 30.0 / weak | openai:message_clarity, score=30.0, confidence=0.45; openai:transcript, score=100.0, confidence=0.8; deepgram:transcript, score=100.0, confidence=0.8; openai:filler_words, score=100.0, confidence=0.55 |  |
| 39 | المحتوى | الرسائل الاتصالية | human_review_required |  |  | Not auto-scored; the Excel criterion requires expert judgment. | openai:message_clarity, score=30.0, confidence=0.45; openai:filler_words, score=100.0, confidence=0.55; deepgram:speaker_timing, score=85.0, confidence=0.7 |  |
| 40 | المحتوى | بنية المحتوى | scored | 50.0 | weak | Score 50.0 / weak | openai:content_structure, score=50.0, confidence=0.45; openai:transcript, score=100.0, confidence=0.8; deepgram:transcript, score=100.0, confidence=0.8 |  |
| 41 | المحتوى | بنية المحتوى | human_review_required |  |  | Not auto-scored; the Excel criterion requires expert judgment. | openai:message_clarity, score=30.0, confidence=0.45; openai:filler_words, score=100.0, confidence=0.55; deepgram:speaker_timing, score=85.0, confidence=0.7 |  |
| 42 | المحتوى | الاستهلال | scored | 100.0 | excellent | Score 100.0 / excellent | openai_rubric:criterion_score_42, score=100.0, confidence=0.95 |  |
| 43 | المحتوى | الإقفال | scored | 90.0 | very_good | Score 90.0 / very_good | openai_rubric:criterion_score_43, score=90.0, confidence=0.9 |  |
| 44 | المحتوى | الاستمالات العقلانية | scored | 80.0 | good | Score 80.0 / good | openai_rubric:criterion_score_44, score=80.0, confidence=0.9 |  |
| 45 | المحتوى | جودة الاستمالات العقلانية | human_review_required |  |  | Not auto-scored; the Excel criterion requires expert judgment. | openai:message_clarity, score=30.0, confidence=0.45; openai:filler_words, score=100.0, confidence=0.55; deepgram:speaker_timing, score=85.0, confidence=0.7 |  |
| 46 | المحتوى | الاستمالات العاطفية | scored | 0.0 | weak | Score 0.0 / weak | openai_rubric:criterion_score_46, score=0.0, confidence=0.95 |  |
| 47 | المحتوى | جودة الاستمالات العاطفية | human_review_required |  |  | Not auto-scored; the Excel criterion requires expert judgment. | openai:message_clarity, score=30.0, confidence=0.45; openai:filler_words, score=100.0, confidence=0.55; deepgram:speaker_timing, score=85.0, confidence=0.7 |  |
| 48 | المحتوى | اللغة: سليمة من الأخطاء، و العيوب | scored | 90.0 | very_good | Score 90.0 / very_good | openai_rubric:criterion_score_48, score=90.0, confidence=0.9 |  |
| 49 | المحتوى | اللغة: سليمة من الأخطاء، و العيوب | human_review_required |  |  | Not auto-scored; the Excel criterion requires expert judgment. | openai:message_clarity, score=30.0, confidence=0.45; openai:filler_words, score=100.0, confidence=0.55; deepgram:speaker_timing, score=85.0, confidence=0.7 |  |
| 50 | المحتوى | مناسبة طول الحديث للمناسبة | scored | 95.0 | excellent | Score 95.0 / excellent | deepgram:duration_suitability, score=95.0, confidence=0.7; deepgram:actual_duration, confidence=0.7; deepgram:expected_duration, confidence=0.7 |  |
| 51 | المحتوى | الوعي بالسياق | human_review_required |  |  | Not auto-scored; the Excel criterion requires expert judgment. | openai:message_clarity, score=30.0, confidence=0.45; openai:filler_words, score=100.0, confidence=0.55; deepgram:speaker_timing, score=85.0, confidence=0.7 |  |
| 52 | المحتوى | الأصالة والإبداع | human_review_required |  |  | Not auto-scored; the Excel criterion requires expert judgment. | openai:message_clarity, score=30.0, confidence=0.45; openai:filler_words, score=100.0, confidence=0.55; deepgram:speaker_timing, score=85.0, confidence=0.7 |  |
| 53 | الأسئلة | التفاعل مع السائل و السؤال | scored | 85.0 | very_good | Score 85.0 / very_good | openai_rubric:criterion_score_53, score=85.0, confidence=0.9 |  |
| 54 | الأسئلة | الثبات الانفعالي | scored | 84.5 | very_good | Score 84.5 / very_good | composite:emotional_stability, score=84.5, confidence=0.55 |  |
| 55 | الأسئلة | القابلية للاقتباس و التداول | scored | 70.0 | needs_development | Score 70.0 / needs_development | openai_rubric:criterion_score_55, score=70.0, confidence=0.85 |  |
| 56 | الأسئلة | استراتيجات الإجابة | scored | 100.0 | excellent | Score 100.0 / excellent | openai_rubric:criterion_score_56, score=100.0, confidence=0.95 |  |

## Detailed Criterion Evidence

### Row 11 - وضوح المخارج

- Axis: الأداء الصوتي
- Status: `scored`
- Score: `50.0`
- Rating: `weak`
- Excel evaluation method: Tool
- Explanation: All required signals for this rule are available.
- Calculation note: The final score used the selected signal value {"openai_deepgram_agreement": 0.013, "score": 50.0, "weak_letter_score": 50.0}, mapped by the tool to score 50.0.
- Next action: Replace this ASR-agreement proxy with true PCC/phoneme alignment when a reference transcript is available.

**Selected Scoring Signal**

- Tool: `openai`
- Signal: `pronunciation_clarity` - Pronunciation clarity proxy
- Measured value: `{"openai_deepgram_agreement": 0.013, "score": 50.0, "weak_letter_score": 50.0}`
- Signal score: `50.0`
- Confidence: `0.4`
- Evidence: Proxy based on OpenAI/Deepgram transcript agreement; not true PCC phoneme scoring.

**All Supporting Signals**

- `openai:pronunciation_clarity` - Pronunciation clarity proxy
  - Value: `{"openai_deepgram_agreement": 0.013, "score": 50.0, "weak_letter_score": 50.0}`
  - Score: `50.0`
  - Confidence: `0.4`
  - Evidence: Proxy based on OpenAI/Deepgram transcript agreement; not true PCC phoneme scoring.
- `openai:transcript` - Transcript availability
  - Value: `true`
  - Score: `100.0`
  - Confidence: `0.8`
  - Evidence: None
- `deepgram:transcript` - Transcript availability
  - Value: `true`
  - Score: `100.0`
  - Confidence: `0.8`
  - Evidence: None

### Row 12 - وضوح المخارج

- Axis: الأداء الصوتي
- Status: `scored`
- Score: `50.0`
- Rating: `weak`
- Excel evaluation method: Tool
- Explanation: All required signals for this rule are available.
- Calculation note: The final score used the selected signal value {"openai_deepgram_agreement": 0.013, "score": 50.0, "weak_letter_score": 50.0}, mapped by the tool to score 50.0.
- Next action: Replace this proxy with letter/phoneme error rates from aligned reference text.

**Selected Scoring Signal**

- Tool: `openai`
- Signal: `weak_letter_detection` - Weak-letter detection proxy
- Measured value: `{"openai_deepgram_agreement": 0.013, "score": 50.0, "weak_letter_score": 50.0}`
- Signal score: `50.0`
- Confidence: `0.3`
- Evidence: Proxy only. True weak-letter detection needs phoneme alignment or human reference transcript.

**All Supporting Signals**

- `openai:weak_letter_detection` - Weak-letter detection proxy
  - Value: `{"openai_deepgram_agreement": 0.013, "score": 50.0, "weak_letter_score": 50.0}`
  - Score: `50.0`
  - Confidence: `0.3`
  - Evidence: Proxy only. True weak-letter detection needs phoneme alignment or human reference transcript.
- `openai:transcript` - Transcript availability
  - Value: `true`
  - Score: `100.0`
  - Confidence: `0.8`
  - Evidence: None
- `deepgram:transcript` - Transcript availability
  - Value: `true`
  - Score: `100.0`
  - Confidence: `0.8`
  - Evidence: None

### Row 13 - نبرة الصوت التلوين ( تعريفها: وجود مشاعر في الصوت)

- Axis: الأداء الصوتي
- Status: `scored`
- Score: `90.0`
- Rating: `excellent`
- Excel evaluation method: Tools
- Explanation: All required signals for this rule are available.
- Calculation note: The final score used the selected signal value {"mean_pitch_hz": 136.24, "pitch_variation_hz": 40.49}, mapped by the tool to score 90.0.
- Next action: Review as a pitch-variation proxy; add semantic prosody matching later for stricter scoring.

**Selected Scoring Signal**

- Tool: `local_audio`
- Signal: `pitch_variation` - Pitch variation / vocal coloring proxy
- Measured value: `{"mean_pitch_hz": 136.24, "pitch_variation_hz": 40.49}`
- Signal score: `90.0`
- Confidence: `0.5`
- Evidence: None

**All Supporting Signals**

- `local_audio:pitch_variation` - Pitch variation / vocal coloring proxy
  - Value: `{"mean_pitch_hz": 136.24, "pitch_variation_hz": 40.49}`
  - Score: `90.0`
  - Confidence: `0.5`
  - Evidence: None
- `openai:transcript` - Transcript availability
  - Value: `true`
  - Score: `100.0`
  - Confidence: `0.8`
  - Evidence: None
- `deepgram:transcript` - Transcript availability
  - Value: `true`
  - Score: `100.0`
  - Confidence: `0.8`
  - Evidence: None

### Row 14 - مستوى الصوت

- Axis: الأداء الصوتي
- Status: `scored`
- Score: `80.0`
- Rating: `very_good`
- Excel evaluation method: Tools
- Explanation: All required signals for this rule are available.
- Calculation note: The final score used the selected signal value {"max_volume_db": -2.0, "mean_volume_db": -25.9}, mapped by the tool to score 80.0.
- Next action: Add audio loudness analysis with ffmpeg/Librosa to extract min/mean/max dB.

**Selected Scoring Signal**

- Tool: `local_audio`
- Signal: `volume_db` - Audio loudness in dB
- Measured value: `{"max_volume_db": -2.0, "mean_volume_db": -25.9}`
- Signal score: `80.0`
- Confidence: `0.65`
- Evidence: None

**All Supporting Signals**

- `local_audio:volume_db` - Audio loudness in dB
  - Value: `{"max_volume_db": -2.0, "mean_volume_db": -25.9}`
  - Score: `80.0`
  - Confidence: `0.65`
  - Evidence: None

### Row 15 - الوقفات و التنفس

- Axis: الأداء الصوتي
- Status: `scored`
- Score: `60.0`
- Rating: `needs_development`
- Excel evaluation method: Tool
- Explanation: All required signals for this rule are available.
- Calculation note: The final score used the selected signal value 3.64, mapped by the tool to score 60.0.
- Next action: Add silence/pause extraction from word timestamps or audio waveform before scoring this criterion.

**Selected Scoring Signal**

- Tool: `deepgram`
- Signal: `pause_rate` - Pauses per 100 words
- Measured value: `3.64`
- Signal score: `60.0`
- Confidence: `0.7`
- Evidence: None

**All Supporting Signals**

- `deepgram:pause_count` - Pause count
  - Value: `{"count": 4, "examples": [{"duration": 0.62, "end": 41.9, "start": 41.27}, {"duration": 0.56, "end": 47.09, "start": 46.53}, {"duration": 1.12, "end": 60.17, "start": 59.05}, {"duration": 2.4, "end": 63.29, "start": 60.89}], "threshold_seconds": 0.5}`
  - Score: `60.0`
  - Confidence: `0.7`
  - Evidence: None
- `deepgram:pause_rate` - Pauses per 100 words
  - Value: `3.64`
  - Score: `60.0`
  - Confidence: `0.7`
  - Evidence: None
- `deepgram:speaker_timing` - Speaker diarization / timing
  - Value: `{"speaker_count": 1, "utterance_count": 20}`
  - Score: `85.0`
  - Confidence: `0.7`
  - Evidence: None
- `openai:transcript` - Transcript availability
  - Value: `true`
  - Score: `100.0`
  - Confidence: `0.8`
  - Evidence: None
- `deepgram:transcript` - Transcript availability
  - Value: `true`
  - Score: `100.0`
  - Confidence: `0.8`
  - Evidence: None
- `deepgram:words_per_minute` - Speech speed
  - Value: `102.98`
  - Score: `90.0`
  - Confidence: `0.7`
  - Evidence: None
- `local_audio:audio_silence_events` - Audio silence events
  - Value: `{"count": 12, "events": [{"duration": 0.63, "end": 0.63, "start": 0.0}, {"duration": 0.69, "end": 9.38, "start": 8.68}, {"duration": 0.5, "end": 11.27, "start": 10.76}, {"duration": 0.81, "end": 20.79, "start": 19.99}, {"duration": 0.86, "end": 26.52, "start": 25.66}, {"duration": 0.57, "end": 29.23, "start": 28.67}, {"duration": 0.72, "end": 36.03, "start": 35.31}, {"duration": 0.62, "end": 50.91, "start": 50.29}, {"duration": 0.57, "end": 52.03, "start": 51.45}, {"duration": 1.6, "end": 60.2, "start": 58.6}]}`
  - Score: `None`
  - Confidence: `0.55`
  - Evidence: None

### Row 17 - خامة الصوت

- Axis: الأداء الصوتي
- Status: `scored`
- Score: `90.0`
- Rating: `excellent`
- Excel evaluation method: Tool
- Explanation: All required signals for this rule are available.
- Calculation note: The final score used the selected signal value {"max_pitch_hz": 192.77, "min_pitch_hz": 91.43, "pitch_range_hz": 101.34, "voiced_frame_count": 1694}, mapped by the tool to score 90.0.
- Next action: Review pitch range proxy; refine later with musical-note range and voice quality analysis.

**Selected Scoring Signal**

- Tool: `local_audio`
- Signal: `pitch_range_hz` - Pitch range in Hz
- Measured value: `{"max_pitch_hz": 192.77, "min_pitch_hz": 91.43, "pitch_range_hz": 101.34, "voiced_frame_count": 1694}`
- Signal score: `90.0`
- Confidence: `0.55`
- Evidence: None

**All Supporting Signals**

- `local_audio:pitch_range_hz` - Pitch range in Hz
  - Value: `{"max_pitch_hz": 192.77, "min_pitch_hz": 91.43, "pitch_range_hz": 101.34, "voiced_frame_count": 1694}`
  - Score: `90.0`
  - Confidence: `0.55`
  - Evidence: None
- `local_audio:pitch_variation` - Pitch variation / vocal coloring proxy
  - Value: `{"mean_pitch_hz": 136.24, "pitch_variation_hz": 40.49}`
  - Score: `90.0`
  - Confidence: `0.5`
  - Evidence: None

### Row 19 - السرعة

- Axis: الأداء الصوتي
- Status: `scored`
- Score: `90.0`
- Rating: `excellent`
- Excel evaluation method: Tool
- Explanation: All required signals for this rule are available.
- Calculation note: The final score used the selected signal value 102.98, mapped by the tool to score 90.0.
- Next action: Use Deepgram or another timestamped STT output to calculate WPM against the Excel ranges.

**Selected Scoring Signal**

- Tool: `deepgram`
- Signal: `words_per_minute` - Speech speed
- Measured value: `102.98`
- Signal score: `90.0`
- Confidence: `0.7`
- Evidence: None

**All Supporting Signals**

- `deepgram:words_per_minute` - Speech speed
  - Value: `102.98`
  - Score: `90.0`
  - Confidence: `0.7`
  - Evidence: None
- `openai:transcript` - Transcript availability
  - Value: `true`
  - Score: `100.0`
  - Confidence: `0.8`
  - Evidence: None
- `deepgram:transcript` - Transcript availability
  - Value: `true`
  - Score: `100.0`
  - Confidence: `0.8`
  - Evidence: None

### Row 20 - المظهر العام

- Axis: لغة الجسد
- Status: `human_review_required`
- Score: ``
- Rating: ``
- Excel evaluation method: تحليل بشري
- Explanation: The Excel form marks this criterion as human analysis.
- Calculation note: No numeric score was assigned because the current evidence is not enough for an automatic score.
- Next action: Keep this as expert review; tool outputs may provide supporting evidence only.

**Selected Scoring Signal**

- None. This criterion was not automatically scored from the current evidence.

**All Supporting Signals**

- No supporting signal is currently attached to this criterion.

### Row 21 - الثقة الإنطباع الأولى و الثبات الانفعالي

- Axis: لغة الجسد
- Status: `human_review_required`
- Score: ``
- Rating: ``
- Excel evaluation method: تحليل بشري
- Explanation: The Excel form marks this criterion as human analysis.
- Calculation note: No numeric score was assigned because the current evidence is not enough for an automatic score.
- Next action: Keep this as expert review; tool outputs may provide supporting evidence only.

**Selected Scoring Signal**

- None. This criterion was not automatically scored from the current evidence.

**All Supporting Signals**

- `aws_rekognition:face_detection` - Face detection
  - Value: `{"detections": 134, "unique_timestamps": 128}`
  - Score: `90.0`
  - Confidence: `0.75`
  - Evidence: None
- `mediapipe:face_visibility` - Face visibility
  - Value: `0.0`
  - Score: `0.0`
  - Confidence: `0.8`
  - Evidence: None

### Row 22 - لغة جسد منضبطة

- Axis: لغة الجسد
- Status: `scored`
- Score: `93.4`
- Rating: `excellent`
- Excel evaluation method: Tool
- Explanation: All required signals for this rule are available.
- Calculation note: The final score used the selected signal value 93.4, mapped by the tool to score 93.4.
- Next action: Review posture proxy evidence; refine later into CVA/shoulder/kyphosis/pelvic sub-scores.

**Selected Scoring Signal**

- Tool: `mediapipe`
- Signal: `posture` - Posture alignment proxy
- Measured value: `93.4`
- Signal score: `93.4`
- Confidence: `0.65`
- Evidence: Computed from pose landmark shoulder balance, head centering, and spine verticality.

**All Supporting Signals**

- `mediapipe:posture` - Posture alignment proxy
  - Value: `93.4`
  - Score: `93.4`
  - Confidence: `0.65`
  - Evidence: Computed from pose landmark shoulder balance, head centering, and spine verticality.
- `mediapipe:body_visibility` - Body / pose visibility
  - Value: `0.986`
  - Score: `98.57`
  - Confidence: `0.85`
  - Evidence: None
- `mediapipe:body_movement` - Overall body movement intensity
  - Value: `{"average_motion_intensity": 0.03437, "event_threshold": "body_motion >= 0.03", "movement_event_count": 49, "movement_events_per_minute": 45.89, "sampled_frames": 140}`
  - Score: `90.0`
  - Confidence: `0.7`
  - Evidence: MediaPipe Tasks pose, hand, and face landmark models were used.

### Row 23 - لغة جسد منضبطة

- Axis: لغة الجسد
- Status: `scored`
- Score: `55.0`
- Rating: `weak`
- Excel evaluation method: Tool
- Explanation: All required signals for this rule are available.
- Calculation note: The final score used the selected signal value 16.86, mapped by the tool to score 55.0.
- Next action: Convert body landmark changes into repeated movement events per minute.

**Selected Scoring Signal**

- Tool: `mediapipe`
- Signal: `body_repetition_rate` - Repeated body movement rate
- Measured value: `16.86`
- Signal score: `55.0`
- Confidence: `0.6`
- Evidence: Computed from repeated body-motion spikes per minute.

**All Supporting Signals**

- `mediapipe:body_repetition_rate` - Repeated body movement rate
  - Value: `16.86`
  - Score: `55.0`
  - Confidence: `0.6`
  - Evidence: Computed from repeated body-motion spikes per minute.
- `mediapipe:body_movement` - Overall body movement intensity
  - Value: `{"average_motion_intensity": 0.03437, "event_threshold": "body_motion >= 0.03", "movement_event_count": 49, "movement_events_per_minute": 45.89, "sampled_frames": 140}`
  - Score: `90.0`
  - Confidence: `0.7`
  - Evidence: MediaPipe Tasks pose, hand, and face landmark models were used.
- `mediapipe:body_visibility` - Body / pose visibility
  - Value: `0.986`
  - Score: `98.57`
  - Confidence: `0.85`
  - Evidence: None
- `mediapipe:posture` - Posture alignment proxy
  - Value: `93.4`
  - Score: `93.4`
  - Confidence: `0.65`
  - Evidence: Computed from pose landmark shoulder balance, head centering, and spine verticality.

### Row 24 - لغة جسد منضبطة

- Axis: لغة الجسد
- Status: `scored`
- Score: `68.22`
- Rating: `needs_development`
- Excel evaluation method: Tool
- Explanation: All required signals for this rule are available.
- Calculation note: The final score used the selected signal value 68.22, mapped by the tool to score 68.22.
- Next action: Add foot stance extraction from lower-body pose landmarks when full body is visible.

**Selected Scoring Signal**

- Tool: `mediapipe`
- Signal: `foot_stance_width` - Foot stance width proxy
- Measured value: `68.22`
- Signal score: `68.22`
- Confidence: `0.45`
- Evidence: Computed from ankle distance relative to shoulder width when pose landmarks exist.

**All Supporting Signals**

- `mediapipe:foot_stance_width` - Foot stance width proxy
  - Value: `68.22`
  - Score: `68.22`
  - Confidence: `0.45`
  - Evidence: Computed from ankle distance relative to shoulder width when pose landmarks exist.
- `mediapipe:body_visibility` - Body / pose visibility
  - Value: `0.986`
  - Score: `98.57`
  - Confidence: `0.85`
  - Evidence: None
- `mediapipe:posture` - Posture alignment proxy
  - Value: `93.4`
  - Score: `93.4`
  - Confidence: `0.65`
  - Evidence: Computed from pose landmark shoulder balance, head centering, and spine verticality.

### Row 25 - اتصال بصري( توزيع النظرات، معدل رمش)

- Axis: لغة الجسد
- Status: `scored`
- Score: `50.0`
- Rating: `weak`
- Excel evaluation method: Tool
- Explanation: All required signals for this rule are available.
- Calculation note: The final score used the selected signal value {"center_count": 1, "distribution_score": 50.19, "frontal_rate": 0.396, "frontal_score": 50.0, "left_count": 133, "right_count": 0, "stability_score": 50.0}, mapped by the tool to score 50.0.
- Next action: Review AWS head-pose proxy; refine later with true eye gaze landmarks.

**Selected Scoring Signal**

- Tool: `aws_rekognition`
- Signal: `gaze_direction` - Head/gaze direction proxy
- Measured value: `{"center_count": 1, "distribution_score": 50.19, "frontal_rate": 0.396, "frontal_score": 50.0, "left_count": 133, "right_count": 0, "stability_score": 50.0}`
- Signal score: `50.0`
- Confidence: `0.55`
- Evidence: Computed from AWS face pose yaw/pitch as a gaze-direction proxy.

**All Supporting Signals**

- `aws_rekognition:gaze_direction` - Head/gaze direction proxy
  - Value: `{"center_count": 1, "distribution_score": 50.19, "frontal_rate": 0.396, "frontal_score": 50.0, "left_count": 133, "right_count": 0, "stability_score": 50.0}`
  - Score: `50.0`
  - Confidence: `0.55`
  - Evidence: Computed from AWS face pose yaw/pitch as a gaze-direction proxy.
- `aws_rekognition:face_detection` - Face detection
  - Value: `{"detections": 134, "unique_timestamps": 128}`
  - Score: `90.0`
  - Confidence: `0.75`
  - Evidence: None

### Row 26 - اتصال بصري( توزيع النظرات، معدل رمش)

- Axis: لغة الجسد
- Status: `scored`
- Score: `50.19`
- Rating: `weak`
- Excel evaluation method: Tool
- Explanation: All required signals for this rule are available.
- Calculation note: The final score used the selected signal value {"center_count": 1, "left_count": 133, "right_count": 0}, mapped by the tool to score 50.19.
- Next action: Review AWS head-pose distribution proxy; refine later with true eye gaze.

**Selected Scoring Signal**

- Tool: `aws_rekognition`
- Signal: `gaze_distribution` - Gaze distribution proxy
- Measured value: `{"center_count": 1, "left_count": 133, "right_count": 0}`
- Signal score: `50.19`
- Confidence: `0.5`
- Evidence: Computed from left/center/right head pose distribution.

**All Supporting Signals**

- `aws_rekognition:gaze_distribution` - Gaze distribution proxy
  - Value: `{"center_count": 1, "left_count": 133, "right_count": 0}`
  - Score: `50.19`
  - Confidence: `0.5`
  - Evidence: Computed from left/center/right head pose distribution.
- `aws_rekognition:face_detection` - Face detection
  - Value: `{"detections": 134, "unique_timestamps": 128}`
  - Score: `90.0`
  - Confidence: `0.75`
  - Evidence: None

### Row 27 - اتصال بصري( توزيع النظرات، معدل رمش)

- Axis: لغة الجسد
- Status: `scored`
- Score: `50.0`
- Rating: `weak`
- Excel evaluation method: Tool
- Explanation: All required signals for this rule are available.
- Calculation note: The final score used the selected signal value {"frontal_rate": 0.396}, mapped by the tool to score 50.0.
- Next action: Review frontal-head-pose stability proxy; refine later with eye landmarks.

**Selected Scoring Signal**

- Tool: `aws_rekognition`
- Signal: `eye_contact_stability` - Eye contact stability proxy
- Measured value: `{"frontal_rate": 0.396}`
- Signal score: `50.0`
- Confidence: `0.5`
- Evidence: Computed from percentage of face detections with mostly frontal yaw/pitch.

**All Supporting Signals**

- `aws_rekognition:eye_contact_stability` - Eye contact stability proxy
  - Value: `{"frontal_rate": 0.396}`
  - Score: `50.0`
  - Confidence: `0.5`
  - Evidence: Computed from percentage of face detections with mostly frontal yaw/pitch.
- `aws_rekognition:face_detection` - Face detection
  - Value: `{"detections": 134, "unique_timestamps": 128}`
  - Score: `90.0`
  - Confidence: `0.75`
  - Evidence: None

### Row 28 - اتصال بصري( توزيع النظرات، معدل رمش)

- Axis: لغة الجسد
- Status: `scored`
- Score: `50.0`
- Rating: `weak`
- Excel evaluation method: Tool
- Explanation: All required signals for this rule are available.
- Calculation note: The final score used the selected signal value 0.0, mapped by the tool to score 50.0.
- Next action: Add blink detection from face landmarks or another face-analysis provider.

**Selected Scoring Signal**

- Tool: `mediapipe`
- Signal: `blink_rate` - Blink rate / eyes closed proxy
- Measured value: `0.0`
- Signal score: `50.0`
- Confidence: `0.45`
- Evidence: Proxy counts sampled frames where eyes are not open.

**All Supporting Signals**

- `mediapipe:blink_rate` - Blink rate
  - Value: `0.0`
  - Score: `50.0`
  - Confidence: `0.0`
  - Evidence: None
- `aws_rekognition:blink_rate` - Blink rate / eyes closed proxy
  - Value: `0.0`
  - Score: `50.0`
  - Confidence: `0.45`
  - Evidence: Proxy counts sampled frames where eyes are not open.
- `aws_rekognition:face_detection` - Face detection
  - Value: `{"detections": 134, "unique_timestamps": 128}`
  - Score: `90.0`
  - Confidence: `0.75`
  - Evidence: None
- `mediapipe:face_visibility` - Face visibility
  - Value: `0.0`
  - Score: `0.0`
  - Confidence: `0.8`
  - Evidence: None

### Row 29 - الإيماءات و توظيف حركة اليدين

- Axis: لغة الجسد
- Status: `scored`
- Score: `82.0`
- Rating: `very_good`
- Excel evaluation method: Tool
- Explanation: All required signals for this rule are available.
- Calculation note: The final score used the selected signal value {"classification": "controlled_visible_hand_movement", "hand_motion": 0.07793, "hand_movement_event_count": 43, "hand_movement_events_per_minute": 40.27, "hand_visibility_rate": 0.943}, mapped by the tool to score 82.0.
- Next action: Review gesture proxy; refine later with semantic positive/negative gesture classes.

**Selected Scoring Signal**

- Tool: `mediapipe`
- Signal: `gesture_classification` - Gesture polarity proxy
- Measured value: `{"classification": "controlled_visible_hand_movement", "hand_motion": 0.07793, "hand_movement_event_count": 43, "hand_movement_events_per_minute": 40.27, "hand_visibility_rate": 0.943}`
- Signal score: `82.0`
- Confidence: `0.45`
- Evidence: Proxy based on hand visibility and controlled movement; not semantic gesture recognition.

**All Supporting Signals**

- `mediapipe:gesture_classification` - Gesture polarity proxy
  - Value: `{"classification": "controlled_visible_hand_movement", "hand_motion": 0.07793, "hand_movement_event_count": 43, "hand_movement_events_per_minute": 40.27, "hand_visibility_rate": 0.943}`
  - Score: `82.0`
  - Confidence: `0.45`
  - Evidence: Proxy based on hand visibility and controlled movement; not semantic gesture recognition.
- `mediapipe:hand_visibility` - Hand visibility
  - Value: `0.943`
  - Score: `94.29`
  - Confidence: `0.85`
  - Evidence: None
- `mediapipe:hand_movement` - Hand movement intensity
  - Value: `{"average_motion_intensity": 0.07793, "event_threshold": "wrist_motion >= 0.04", "hand_visible_frames": 132, "movement_event_count": 43, "movement_events_per_minute": 40.27, "sampled_frames": 140}`
  - Score: `85.0`
  - Confidence: `0.75`
  - Evidence: Score is based on average wrist-motion intensity and hand visibility. Event count is reported for explanation.

### Row 30 - الإيماءات و توظيف حركة اليدين

- Axis: لغة الجسد
- Status: `scored`
- Score: `85.0`
- Rating: `very_good`
- Excel evaluation method: Tool
- Explanation: All required signals for this rule are available.
- Calculation note: The final score used the selected signal value {"average_motion_intensity": 0.07793, "event_threshold": "wrist_motion >= 0.04", "hand_visible_frames": 132, "movement_event_count": 43, "movement_events_per_minute": 40.27, "sampled_frames": 140}, mapped by the tool to score 85.0.
- Next action: Review movement intensity; refine later into count-per-minute gesture events.

**Selected Scoring Signal**

- Tool: `mediapipe`
- Signal: `hand_movement` - Hand movement intensity
- Measured value: `{"average_motion_intensity": 0.07793, "event_threshold": "wrist_motion >= 0.04", "hand_visible_frames": 132, "movement_event_count": 43, "movement_events_per_minute": 40.27, "sampled_frames": 140}`
- Signal score: `85.0`
- Confidence: `0.75`
- Evidence: Score is based on average wrist-motion intensity and hand visibility. Event count is reported for explanation.

**All Supporting Signals**

- `mediapipe:hand_movement` - Hand movement intensity
  - Value: `{"average_motion_intensity": 0.07793, "event_threshold": "wrist_motion >= 0.04", "hand_visible_frames": 132, "movement_event_count": 43, "movement_events_per_minute": 40.27, "sampled_frames": 140}`
  - Score: `85.0`
  - Confidence: `0.75`
  - Evidence: Score is based on average wrist-motion intensity and hand visibility. Event count is reported for explanation.
- `mediapipe:hand_visibility` - Hand visibility
  - Value: `0.943`
  - Score: `94.29`
  - Confidence: `0.85`
  - Evidence: None
- `mediapipe:body_movement` - Overall body movement intensity
  - Value: `{"average_motion_intensity": 0.03437, "event_threshold": "body_motion >= 0.03", "movement_event_count": 49, "movement_events_per_minute": 45.89, "sampled_frames": 140}`
  - Score: `90.0`
  - Confidence: `0.7`
  - Evidence: MediaPipe Tasks pose, hand, and face landmark models were used.

### Row 31 - الإيماءات و توظيف حركة اليدين

- Axis: لغة الجسد
- Status: `scored`
- Score: `82.0`
- Rating: `very_good`
- Excel evaluation method: Tool
- Explanation: All required signals for this rule are available.
- Calculation note: The final score used the selected signal value {"classification": "controlled_visible_hand_movement", "hand_motion": 0.07793, "hand_movement_event_count": 43, "hand_movement_events_per_minute": 40.27, "hand_visibility_rate": 0.943}, mapped by the tool to score 82.0.
- Next action: Review gesture proxy; refine later with tension-specific gesture classes.

**Selected Scoring Signal**

- Tool: `mediapipe`
- Signal: `gesture_classification` - Gesture polarity proxy
- Measured value: `{"classification": "controlled_visible_hand_movement", "hand_motion": 0.07793, "hand_movement_event_count": 43, "hand_movement_events_per_minute": 40.27, "hand_visibility_rate": 0.943}`
- Signal score: `82.0`
- Confidence: `0.45`
- Evidence: Proxy based on hand visibility and controlled movement; not semantic gesture recognition.

**All Supporting Signals**

- `mediapipe:gesture_classification` - Gesture polarity proxy
  - Value: `{"classification": "controlled_visible_hand_movement", "hand_motion": 0.07793, "hand_movement_event_count": 43, "hand_movement_events_per_minute": 40.27, "hand_visibility_rate": 0.943}`
  - Score: `82.0`
  - Confidence: `0.45`
  - Evidence: Proxy based on hand visibility and controlled movement; not semantic gesture recognition.
- `mediapipe:hand_visibility` - Hand visibility
  - Value: `0.943`
  - Score: `94.29`
  - Confidence: `0.85`
  - Evidence: None
- `mediapipe:hand_movement` - Hand movement intensity
  - Value: `{"average_motion_intensity": 0.07793, "event_threshold": "wrist_motion >= 0.04", "hand_visible_frames": 132, "movement_event_count": 43, "movement_events_per_minute": 40.27, "sampled_frames": 140}`
  - Score: `85.0`
  - Confidence: `0.75`
  - Evidence: Score is based on average wrist-motion intensity and hand visibility. Event count is reported for explanation.

### Row 32 - الإيماءات و توظيف حركة اليدين

- Axis: لغة الجسد
- Status: `human_review_required`
- Score: ``
- Rating: ``
- Excel evaluation method: تحليل بشري
- Explanation: The Excel form marks this criterion as human analysis.
- Calculation note: No numeric score was assigned because the current evidence is not enough for an automatic score.
- Next action: Keep this as expert review; tool outputs may provide supporting evidence only.

**Selected Scoring Signal**

- None. This criterion was not automatically scored from the current evidence.

**All Supporting Signals**

- `mediapipe:hand_visibility` - Hand visibility
  - Value: `0.943`
  - Score: `94.29`
  - Confidence: `0.85`
  - Evidence: None
- `mediapipe:body_movement` - Overall body movement intensity
  - Value: `{"average_motion_intensity": 0.03437, "event_threshold": "body_motion >= 0.03", "movement_event_count": 49, "movement_events_per_minute": 45.89, "sampled_frames": 140}`
  - Score: `90.0`
  - Confidence: `0.7`
  - Evidence: MediaPipe Tasks pose, hand, and face landmark models were used.

### Row 33 - تعابير الوجه و الابتسامة

- Axis: لغة الجسد
- Status: `scored`
- Score: `100.0`
- Rating: `excellent`
- Excel evaluation method: Tool
- Explanation: All required signals for this rule are available.
- Calculation note: The final score used the selected signal value {"blink_rate_per_minute": 0.0, "blink_rate_score": 50.0, "expression_score": 100.0, "face_attribute_detections": 16, "face_attribute_frames": 16, "positive_expression_rate": 1.0, "smile_authenticity_score": 95.09, "smile_confidence_mean": 95.09, "smile_rate_per_minute": 1.0, "smile_rate_score": 95.0}, mapped by the tool to score 100.0.
- Next action: Review AWS expression proxy; refine later with face landmarks/blendshapes.

**Selected Scoring Signal**

- Tool: `aws_rekognition`
- Signal: `facial_expression` - Facial expression proxy
- Measured value: `{"blink_rate_per_minute": 0.0, "blink_rate_score": 50.0, "expression_score": 100.0, "face_attribute_detections": 16, "face_attribute_frames": 16, "positive_expression_rate": 1.0, "smile_authenticity_score": 95.09, "smile_confidence_mean": 95.09, "smile_rate_per_minute": 1.0, "smile_rate_score": 95.0}`
- Signal score: `100.0`
- Confidence: `0.55`
- Evidence: Computed from AWS DetectFaces emotions on sampled frames.

**All Supporting Signals**

- `aws_rekognition:facial_expression` - Facial expression proxy
  - Value: `{"blink_rate_per_minute": 0.0, "blink_rate_score": 50.0, "expression_score": 100.0, "face_attribute_detections": 16, "face_attribute_frames": 16, "positive_expression_rate": 1.0, "smile_authenticity_score": 95.09, "smile_confidence_mean": 95.09, "smile_rate_per_minute": 1.0, "smile_rate_score": 95.0}`
  - Score: `100.0`
  - Confidence: `0.55`
  - Evidence: Computed from AWS DetectFaces emotions on sampled frames.
- `aws_rekognition:face_detection` - Face detection
  - Value: `{"detections": 134, "unique_timestamps": 128}`
  - Score: `90.0`
  - Confidence: `0.75`
  - Evidence: None

### Row 34 - تعابير الوجه و الابتسامة

- Axis: لغة الجسد
- Status: `scored`
- Score: `95.0`
- Rating: `excellent`
- Excel evaluation method: Tool
- Explanation: All required signals for this rule are available.
- Calculation note: The final score used the selected signal value 1.0, mapped by the tool to score 95.0.
- Next action: Review sampled-frame smile rate; refine later with continuous face landmarks.

**Selected Scoring Signal**

- Tool: `mediapipe`
- Signal: `smile_rate` - Smile rate from sampled frames
- Measured value: `1.0`
- Signal score: `95.0`
- Confidence: `0.55`
- Evidence: Computed from AWS DetectFaces Smile attribute on sampled frames.

**All Supporting Signals**

- `mediapipe:smile_rate` - Smile rate
  - Value: `0.0`
  - Score: `60.0`
  - Confidence: `0.0`
  - Evidence: None
- `aws_rekognition:smile_rate` - Smile rate from sampled frames
  - Value: `1.0`
  - Score: `95.0`
  - Confidence: `0.55`
  - Evidence: Computed from AWS DetectFaces Smile attribute on sampled frames.
- `aws_rekognition:face_detection` - Face detection
  - Value: `{"detections": 134, "unique_timestamps": 128}`
  - Score: `90.0`
  - Confidence: `0.75`
  - Evidence: None

### Row 35 - تعابير الوجه و الابتسامة

- Axis: لغة الجسد
- Status: `scored`
- Score: `95.09`
- Rating: `excellent`
- Excel evaluation method: Tool
- Explanation: All required signals for this rule are available.
- Calculation note: The final score used the selected signal value 95.09, mapped by the tool to score 95.09.
- Next action: Review AWS smile-confidence proxy; refine later with Duchenne-style face landmarks.

**Selected Scoring Signal**

- Tool: `aws_rekognition`
- Signal: `smile_authenticity` - Smile authenticity proxy
- Measured value: `95.09`
- Signal score: `95.09`
- Confidence: `0.45`
- Evidence: Proxy uses AWS smile confidence; not a full Duchenne smile analysis.

**All Supporting Signals**

- `aws_rekognition:smile_authenticity` - Smile authenticity proxy
  - Value: `95.09`
  - Score: `95.09`
  - Confidence: `0.45`
  - Evidence: Proxy uses AWS smile confidence; not a full Duchenne smile analysis.
- `mediapipe:smile_rate` - Smile rate
  - Value: `0.0`
  - Score: `60.0`
  - Confidence: `0.0`
  - Evidence: None
- `aws_rekognition:smile_rate` - Smile rate from sampled frames
  - Value: `1.0`
  - Score: `95.0`
  - Confidence: `0.55`
  - Evidence: Computed from AWS DetectFaces Smile attribute on sampled frames.
- `aws_rekognition:face_detection` - Face detection
  - Value: `{"detections": 134, "unique_timestamps": 128}`
  - Score: `90.0`
  - Confidence: `0.75`
  - Evidence: None

### Row 36 - تعابير الوجه و الابتسامة

- Axis: لغة الجسد
- Status: `human_review_required`
- Score: ``
- Rating: ``
- Excel evaluation method: تحليل بشري
- Explanation: The Excel form marks this criterion as human analysis.
- Calculation note: No numeric score was assigned because the current evidence is not enough for an automatic score.
- Next action: Keep this as expert review; tool outputs may provide supporting evidence only.

**Selected Scoring Signal**

- None. This criterion was not automatically scored from the current evidence.

**All Supporting Signals**

- `mediapipe:face_visibility` - Face visibility
  - Value: `0.0`
  - Score: `0.0`
  - Confidence: `0.8`
  - Evidence: None
- `aws_rekognition:face_detection` - Face detection
  - Value: `{"detections": 134, "unique_timestamps": 128}`
  - Score: `90.0`
  - Confidence: `0.75`
  - Evidence: None

### Row 37 - الرسائل الاتصالية

- Axis: المحتوى
- Status: `scored`
- Score: `85.0`
- Rating: `very_good`
- Excel evaluation method: Tool
- Explanation: A direct transcript-based rubric score is available for this Excel row.
- Calculation note: The final score came from the rubric scorer for this exact Excel row.
- Next action: Review the transcript evidence and confidence before accepting this score operationally.

**Selected Scoring Signal**

- Tool: `openai_rubric`
- Signal: `criterion_score_37` - Direct rubric score for Excel row 37
- Measured value: `{"criterion": "الرسائل الاتصالية", "explanation": "المتحدث قدم 4 رسائل رئيسية واضحة ومكررة بشكل مناسب خلال الحديث، مما يدل على تركيز جيد للرسائل الاتصالية.", "rating": "very_good", "source": "openai_rubric", "status": "scored"}`
- Signal score: `85.0`
- Confidence: `0.9`
- Evidence: يشربوا المياه قبل أن يعطشوا; استخدام المظلة لتجنب شععة الشمس; الاستظلال في الظل والابتعاد عن الإجهاد الحراري; استخدام الكمامة في حالة الازدحام الشديد

**All Supporting Signals**

- `openai_rubric:criterion_score_37` - Direct rubric score for Excel row 37
  - Value: `{"criterion": "الرسائل الاتصالية", "explanation": "المتحدث قدم 4 رسائل رئيسية واضحة ومكررة بشكل مناسب خلال الحديث، مما يدل على تركيز جيد للرسائل الاتصالية.", "rating": "very_good", "source": "openai_rubric", "status": "scored"}`
  - Score: `85.0`
  - Confidence: `0.9`
  - Evidence: يشربوا المياه قبل أن يعطشوا; استخدام المظلة لتجنب شععة الشمس; الاستظلال في الظل والابتعاد عن الإجهاد الحراري; استخدام الكمامة في حالة الازدحام الشديد

### Row 38 - الرسائل الاتصالية

- Axis: المحتوى
- Status: `scored`
- Score: `30.0`
- Rating: `weak`
- Excel evaluation method: Tool
- Explanation: All required signals for this rule are available.
- Calculation note: The final score used the selected signal value {"sentence_count": 1, "word_count": 107}, mapped by the tool to score 30.0.
- Next action: Review transcript heuristic; refine later with sentence-level Arabic NLP.

**Selected Scoring Signal**

- Tool: `openai`
- Signal: `message_clarity` - Message clarity proxy
- Measured value: `{"sentence_count": 1, "word_count": 107}`
- Signal score: `30.0`
- Confidence: `0.45`
- Evidence: None

**All Supporting Signals**

- `openai:message_clarity` - Message clarity proxy
  - Value: `{"sentence_count": 1, "word_count": 107}`
  - Score: `30.0`
  - Confidence: `0.45`
  - Evidence: None
- `openai:transcript` - Transcript availability
  - Value: `true`
  - Score: `100.0`
  - Confidence: `0.8`
  - Evidence: None
- `deepgram:transcript` - Transcript availability
  - Value: `true`
  - Score: `100.0`
  - Confidence: `0.8`
  - Evidence: None
- `openai:filler_words` - Filler words
  - Value: `{"count": 0, "examples": []}`
  - Score: `100.0`
  - Confidence: `0.55`
  - Evidence: None

### Row 39 - الرسائل الاتصالية

- Axis: المحتوى
- Status: `human_review_required`
- Score: ``
- Rating: ``
- Excel evaluation method: تحليل بشري
- Explanation: The Excel form marks this criterion as human analysis.
- Calculation note: No numeric score was assigned because the current evidence is not enough for an automatic score.
- Next action: Keep this as expert review; tool outputs may provide supporting evidence only.

**Selected Scoring Signal**

- None. This criterion was not automatically scored from the current evidence.

**All Supporting Signals**

- `openai:message_clarity` - Message clarity proxy
  - Value: `{"sentence_count": 1, "word_count": 107}`
  - Score: `30.0`
  - Confidence: `0.45`
  - Evidence: None
- `openai:filler_words` - Filler words
  - Value: `{"count": 0, "examples": []}`
  - Score: `100.0`
  - Confidence: `0.55`
  - Evidence: None
- `deepgram:speaker_timing` - Speaker diarization / timing
  - Value: `{"speaker_count": 1, "utterance_count": 20}`
  - Score: `85.0`
  - Confidence: `0.7`
  - Evidence: None

### Row 40 - بنية المحتوى

- Axis: المحتوى
- Status: `scored`
- Score: `50.0`
- Rating: `weak`
- Excel evaluation method: Tool
- Explanation: All required signals for this rule are available.
- Calculation note: The final score used the selected signal value {"sentence_count": 1, "word_count": 107}, mapped by the tool to score 50.0.
- Next action: Review content-structure proxy; refine later with a stricter structure classifier.

**Selected Scoring Signal**

- Tool: `openai`
- Signal: `content_structure` - Content structure proxy
- Measured value: `{"sentence_count": 1, "word_count": 107}`
- Signal score: `50.0`
- Confidence: `0.45`
- Evidence: None

**All Supporting Signals**

- `openai:content_structure` - Content structure proxy
  - Value: `{"sentence_count": 1, "word_count": 107}`
  - Score: `50.0`
  - Confidence: `0.45`
  - Evidence: None
- `openai:transcript` - Transcript availability
  - Value: `true`
  - Score: `100.0`
  - Confidence: `0.8`
  - Evidence: None
- `deepgram:transcript` - Transcript availability
  - Value: `true`
  - Score: `100.0`
  - Confidence: `0.8`
  - Evidence: None

### Row 41 - بنية المحتوى

- Axis: المحتوى
- Status: `human_review_required`
- Score: ``
- Rating: ``
- Excel evaluation method: تحليل بشري
- Explanation: The Excel form marks this criterion as human analysis.
- Calculation note: No numeric score was assigned because the current evidence is not enough for an automatic score.
- Next action: Keep this as expert review; tool outputs may provide supporting evidence only.

**Selected Scoring Signal**

- None. This criterion was not automatically scored from the current evidence.

**All Supporting Signals**

- `openai:message_clarity` - Message clarity proxy
  - Value: `{"sentence_count": 1, "word_count": 107}`
  - Score: `30.0`
  - Confidence: `0.45`
  - Evidence: None
- `openai:filler_words` - Filler words
  - Value: `{"count": 0, "examples": []}`
  - Score: `100.0`
  - Confidence: `0.55`
  - Evidence: None
- `deepgram:speaker_timing` - Speaker diarization / timing
  - Value: `{"speaker_count": 1, "utterance_count": 20}`
  - Score: `85.0`
  - Confidence: `0.7`
  - Evidence: None

### Row 42 - الاستهلال

- Axis: المحتوى
- Status: `scored`
- Score: `100.0`
- Rating: `excellent`
- Excel evaluation method: Tool
- Explanation: A direct transcript-based rubric score is available for this Excel row.
- Calculation note: The final score came from the rubric scorer for this exact Excel row.
- Next action: Review the transcript evidence and confidence before accepting this score operationally.

**Selected Scoring Signal**

- Tool: `openai_rubric`
- Signal: `criterion_score_42` - Direct rubric score for Excel row 42
- Measured value: `{"criterion": "الاستهلال", "explanation": "الخطاب يبدأ بعبارة ترحيبية وشكر واضحة وجاذبة تمهد للرسالة الرئيسية.", "rating": "excellent", "source": "openai_rubric", "status": "scored"}`
- Signal score: `100.0`
- Confidence: `0.95`
- Evidence: أذن لكم متابعين الأعزاء وظيفي وظيفكم سعادة المتحدث الرسمي لوزارة الصحة في موسم الحج الأستاذ عبد العزيز عبد الباقي أستاذي حياك الله

**All Supporting Signals**

- `openai_rubric:criterion_score_42` - Direct rubric score for Excel row 42
  - Value: `{"criterion": "الاستهلال", "explanation": "الخطاب يبدأ بعبارة ترحيبية وشكر واضحة وجاذبة تمهد للرسالة الرئيسية.", "rating": "excellent", "source": "openai_rubric", "status": "scored"}`
  - Score: `100.0`
  - Confidence: `0.95`
  - Evidence: أذن لكم متابعين الأعزاء وظيفي وظيفكم سعادة المتحدث الرسمي لوزارة الصحة في موسم الحج الأستاذ عبد العزيز عبد الباقي أستاذي حياك الله

### Row 43 - الإقفال

- Axis: المحتوى
- Status: `scored`
- Score: `90.0`
- Rating: `very_good`
- Excel evaluation method: Tool
- Explanation: A direct transcript-based rubric score is available for this Excel row.
- Calculation note: The final score came from the rubric scorer for this exact Excel row.
- Next action: Review the transcript evidence and confidence before accepting this score operationally.

**Selected Scoring Signal**

- Tool: `openai_rubric`
- Signal: `criterion_score_43` - Direct rubric score for Excel row 43
- Measured value: `{"criterion": "الإقفال", "explanation": "الختام يلخص الرسالة ويترك أثر تحفيزي مع دعوة ضمنية للالتزام بالإرشادات وشكر.", "rating": "very_good", "source": "openai_rubric", "status": "scored"}`
- Signal score: `90.0`
- Confidence: `0.9`
- Evidence: مهم جدا أن نتأكد أن الحاج يستمر في أداء مناسكه بطمأنينة وسهولة ومأمونية وسلامة باتباع هذه الإرشادات شكرا

**All Supporting Signals**

- `openai_rubric:criterion_score_43` - Direct rubric score for Excel row 43
  - Value: `{"criterion": "الإقفال", "explanation": "الختام يلخص الرسالة ويترك أثر تحفيزي مع دعوة ضمنية للالتزام بالإرشادات وشكر.", "rating": "very_good", "source": "openai_rubric", "status": "scored"}`
  - Score: `90.0`
  - Confidence: `0.9`
  - Evidence: مهم جدا أن نتأكد أن الحاج يستمر في أداء مناسكه بطمأنينة وسهولة ومأمونية وسلامة باتباع هذه الإرشادات شكرا

### Row 44 - الاستمالات العقلانية

- Axis: المحتوى
- Status: `scored`
- Score: `80.0`
- Rating: `good`
- Excel evaluation method: Tool
- Explanation: A direct transcript-based rubric score is available for this Excel row.
- Calculation note: The final score came from the rubric scorer for this exact Excel row.
- Next action: Review the transcript evidence and confidence before accepting this score operationally.

**Selected Scoring Signal**

- Tool: `openai_rubric`
- Signal: `criterion_score_44` - Direct rubric score for Excel row 44
- Measured value: `{"criterion": "الاستمالات العقلانية", "explanation": "الخطاب يحتوي على أدلة منطقية وعملية تدعم الرسائل مثل شرب الماء وتجنب الشمس والازدحام، مما يعكس استمالات عقلانية واضحة.", "rating": "good", "source": "openai_rubric", "status": "scored"}`
- Signal score: `80.0`
- Confidence: `0.9`
- Evidence: يشربوا المياه قبل أن يعطشوا; تجنب شععة الشمس قدر الإمكان; استخدام الكمامة في حالة الازدحام الشديد

**All Supporting Signals**

- `openai_rubric:criterion_score_44` - Direct rubric score for Excel row 44
  - Value: `{"criterion": "الاستمالات العقلانية", "explanation": "الخطاب يحتوي على أدلة منطقية وعملية تدعم الرسائل مثل شرب الماء وتجنب الشمس والازدحام، مما يعكس استمالات عقلانية واضحة.", "rating": "good", "source": "openai_rubric", "status": "scored"}`
  - Score: `80.0`
  - Confidence: `0.9`
  - Evidence: يشربوا المياه قبل أن يعطشوا; تجنب شععة الشمس قدر الإمكان; استخدام الكمامة في حالة الازدحام الشديد

### Row 45 - جودة الاستمالات العقلانية

- Axis: المحتوى
- Status: `human_review_required`
- Score: ``
- Rating: ``
- Excel evaluation method: تحليل بشري
- Explanation: The Excel form marks this criterion as human analysis.
- Calculation note: No numeric score was assigned because the current evidence is not enough for an automatic score.
- Next action: Keep this as expert review; tool outputs may provide supporting evidence only.

**Selected Scoring Signal**

- None. This criterion was not automatically scored from the current evidence.

**All Supporting Signals**

- `openai:message_clarity` - Message clarity proxy
  - Value: `{"sentence_count": 1, "word_count": 107}`
  - Score: `30.0`
  - Confidence: `0.45`
  - Evidence: None
- `openai:filler_words` - Filler words
  - Value: `{"count": 0, "examples": []}`
  - Score: `100.0`
  - Confidence: `0.55`
  - Evidence: None
- `deepgram:speaker_timing` - Speaker diarization / timing
  - Value: `{"speaker_count": 1, "utterance_count": 20}`
  - Score: `85.0`
  - Confidence: `0.7`
  - Evidence: None

### Row 46 - الاستمالات العاطفية

- Axis: المحتوى
- Status: `scored`
- Score: `0.0`
- Rating: `weak`
- Excel evaluation method: Tool
- Explanation: A direct transcript-based rubric score is available for this Excel row.
- Calculation note: The final score came from the rubric scorer for this exact Excel row.
- Next action: Review the transcript evidence and confidence before accepting this score operationally.

**Selected Scoring Signal**

- Tool: `openai_rubric`
- Signal: `criterion_score_46` - Direct rubric score for Excel row 46
- Measured value: `{"criterion": "الاستمالات العاطفية", "explanation": "لا توجد استخدامات واضحة للعاطفة أو البلاغة مثل الأسئلة البلاغية أو المجاز أو الحديث عن المشاعر في النص.", "rating": "weak", "source": "openai_rubric", "status": "scored"}`
- Signal score: `0.0`
- Confidence: `0.95`
- Evidence: None

**All Supporting Signals**

- `openai_rubric:criterion_score_46` - Direct rubric score for Excel row 46
  - Value: `{"criterion": "الاستمالات العاطفية", "explanation": "لا توجد استخدامات واضحة للعاطفة أو البلاغة مثل الأسئلة البلاغية أو المجاز أو الحديث عن المشاعر في النص.", "rating": "weak", "source": "openai_rubric", "status": "scored"}`
  - Score: `0.0`
  - Confidence: `0.95`
  - Evidence: None

### Row 47 - جودة الاستمالات العاطفية

- Axis: المحتوى
- Status: `human_review_required`
- Score: ``
- Rating: ``
- Excel evaluation method: تحليل بشري
- Explanation: The Excel form marks this criterion as human analysis.
- Calculation note: No numeric score was assigned because the current evidence is not enough for an automatic score.
- Next action: Keep this as expert review; tool outputs may provide supporting evidence only.

**Selected Scoring Signal**

- None. This criterion was not automatically scored from the current evidence.

**All Supporting Signals**

- `openai:message_clarity` - Message clarity proxy
  - Value: `{"sentence_count": 1, "word_count": 107}`
  - Score: `30.0`
  - Confidence: `0.45`
  - Evidence: None
- `openai:filler_words` - Filler words
  - Value: `{"count": 0, "examples": []}`
  - Score: `100.0`
  - Confidence: `0.55`
  - Evidence: None
- `deepgram:speaker_timing` - Speaker diarization / timing
  - Value: `{"speaker_count": 1, "utterance_count": 20}`
  - Score: `85.0`
  - Confidence: `0.7`
  - Evidence: None

### Row 48 - اللغة: سليمة من الأخطاء، و العيوب

- Axis: المحتوى
- Status: `scored`
- Score: `90.0`
- Rating: `very_good`
- Excel evaluation method: Tool
- Explanation: A direct transcript-based rubric score is available for this Excel row.
- Calculation note: The final score came from the rubric scorer for this exact Excel row.
- Next action: Review the transcript evidence and confidence before accepting this score operationally.

**Selected Scoring Signal**

- Tool: `openai_rubric`
- Signal: `criterion_score_48` - Direct rubric score for Excel row 48
- Measured value: `{"criterion": "اللغة: سليمة من الأخطاء، و العيوب", "explanation": "اللغة المستخدمة سليمة من الأخطاء النحوية واللفظية، مع استخدام لغة فصحى مناسبة للخطاب الرسمي.", "rating": "very_good", "source": "openai_rubric", "status": "scored"}`
- Signal score: `90.0`
- Confidence: `0.9`
- Evidence: النص خالٍ من الأخطاء النحوية الواضحة، ولا يحتوي على كلمات عامية أو تكرار زائد

**All Supporting Signals**

- `openai_rubric:criterion_score_48` - Direct rubric score for Excel row 48
  - Value: `{"criterion": "اللغة: سليمة من الأخطاء، و العيوب", "explanation": "اللغة المستخدمة سليمة من الأخطاء النحوية واللفظية، مع استخدام لغة فصحى مناسبة للخطاب الرسمي.", "rating": "very_good", "source": "openai_rubric", "status": "scored"}`
  - Score: `90.0`
  - Confidence: `0.9`
  - Evidence: النص خالٍ من الأخطاء النحوية الواضحة، ولا يحتوي على كلمات عامية أو تكرار زائد

### Row 49 - اللغة: سليمة من الأخطاء، و العيوب

- Axis: المحتوى
- Status: `human_review_required`
- Score: ``
- Rating: ``
- Excel evaluation method: تحليل بشري
- Explanation: The Excel form marks this criterion as human analysis.
- Calculation note: No numeric score was assigned because the current evidence is not enough for an automatic score.
- Next action: Keep this as expert review; tool outputs may provide supporting evidence only.

**Selected Scoring Signal**

- None. This criterion was not automatically scored from the current evidence.

**All Supporting Signals**

- `openai:message_clarity` - Message clarity proxy
  - Value: `{"sentence_count": 1, "word_count": 107}`
  - Score: `30.0`
  - Confidence: `0.45`
  - Evidence: None
- `openai:filler_words` - Filler words
  - Value: `{"count": 0, "examples": []}`
  - Score: `100.0`
  - Confidence: `0.55`
  - Evidence: None
- `deepgram:speaker_timing` - Speaker diarization / timing
  - Value: `{"speaker_count": 1, "utterance_count": 20}`
  - Score: `85.0`
  - Confidence: `0.7`
  - Evidence: None

### Row 50 - مناسبة طول الحديث للمناسبة

- Axis: المحتوى
- Status: `scored`
- Score: `95.0`
- Rating: `excellent`
- Excel evaluation method: Tool
- Explanation: All required signals for this rule are available.
- Calculation note: The final score used the selected signal value {"actual_duration_seconds": 64.09, "expected_duration_seconds": 60.0}, mapped by the tool to score 95.0.
- Next action: Set expected_duration_seconds in sample metadata for the relevant event/context.

**Selected Scoring Signal**

- Tool: `deepgram`
- Signal: `duration_suitability` - Duration suitability
- Measured value: `{"actual_duration_seconds": 64.09, "expected_duration_seconds": 60.0}`
- Signal score: `95.0`
- Confidence: `0.7`
- Evidence: None

**All Supporting Signals**

- `deepgram:duration_suitability` - Duration suitability
  - Value: `{"actual_duration_seconds": 64.09, "expected_duration_seconds": 60.0}`
  - Score: `95.0`
  - Confidence: `0.7`
  - Evidence: None
- `deepgram:actual_duration` - Actual speaking duration
  - Value: `64.09`
  - Score: `None`
  - Confidence: `0.7`
  - Evidence: None
- `deepgram:expected_duration` - Expected duration
  - Value: `60.0`
  - Score: `None`
  - Confidence: `0.7`
  - Evidence: None

### Row 51 - الوعي بالسياق

- Axis: المحتوى
- Status: `human_review_required`
- Score: ``
- Rating: ``
- Excel evaluation method: تحليل بشري
- Explanation: The Excel form marks this criterion as human analysis.
- Calculation note: No numeric score was assigned because the current evidence is not enough for an automatic score.
- Next action: Keep this as expert review; tool outputs may provide supporting evidence only.

**Selected Scoring Signal**

- None. This criterion was not automatically scored from the current evidence.

**All Supporting Signals**

- `openai:message_clarity` - Message clarity proxy
  - Value: `{"sentence_count": 1, "word_count": 107}`
  - Score: `30.0`
  - Confidence: `0.45`
  - Evidence: None
- `openai:filler_words` - Filler words
  - Value: `{"count": 0, "examples": []}`
  - Score: `100.0`
  - Confidence: `0.55`
  - Evidence: None
- `deepgram:speaker_timing` - Speaker diarization / timing
  - Value: `{"speaker_count": 1, "utterance_count": 20}`
  - Score: `85.0`
  - Confidence: `0.7`
  - Evidence: None

### Row 52 - الأصالة والإبداع

- Axis: المحتوى
- Status: `human_review_required`
- Score: ``
- Rating: ``
- Excel evaluation method: تحليل بشري
- Explanation: The Excel form marks this criterion as human analysis.
- Calculation note: No numeric score was assigned because the current evidence is not enough for an automatic score.
- Next action: Keep this as expert review; tool outputs may provide supporting evidence only.

**Selected Scoring Signal**

- None. This criterion was not automatically scored from the current evidence.

**All Supporting Signals**

- `openai:message_clarity` - Message clarity proxy
  - Value: `{"sentence_count": 1, "word_count": 107}`
  - Score: `30.0`
  - Confidence: `0.45`
  - Evidence: None
- `openai:filler_words` - Filler words
  - Value: `{"count": 0, "examples": []}`
  - Score: `100.0`
  - Confidence: `0.55`
  - Evidence: None
- `deepgram:speaker_timing` - Speaker diarization / timing
  - Value: `{"speaker_count": 1, "utterance_count": 20}`
  - Score: `85.0`
  - Confidence: `0.7`
  - Evidence: None

### Row 53 - التفاعل مع السائل و السؤال

- Axis: الأسئلة
- Status: `scored`
- Score: `85.0`
- Rating: `very_good`
- Excel evaluation method: Tool
- Explanation: A direct transcript-based rubric score is available for this Excel row.
- Calculation note: The final score came from the rubric scorer for this exact Excel row.
- Next action: Review the transcript evidence and confidence before accepting this score operationally.

**Selected Scoring Signal**

- Tool: `openai_rubric`
- Signal: `criterion_score_53` - Direct rubric score for Excel row 53
- Measured value: `{"criterion": "التفاعل مع السائل و السؤال", "explanation": "المتحدث استمع للسؤال، شكر السائل، وأجاب بشكل مباشر وواضح مع احترام السائل وعدم مقاطعته.", "rating": "very_good", "source": "openai_rubric", "status": "scored"}`
- Signal score: `85.0`
- Confidence: `0.9`
- Evidence: حياك الله أخوي عبد العزيز مهم جدا للحجاج ...; الرد مباشر على السؤال حول أفضل السلوكيات للحاج

**All Supporting Signals**

- `openai_rubric:criterion_score_53` - Direct rubric score for Excel row 53
  - Value: `{"criterion": "التفاعل مع السائل و السؤال", "explanation": "المتحدث استمع للسؤال، شكر السائل، وأجاب بشكل مباشر وواضح مع احترام السائل وعدم مقاطعته.", "rating": "very_good", "source": "openai_rubric", "status": "scored"}`
  - Score: `85.0`
  - Confidence: `0.9`
  - Evidence: حياك الله أخوي عبد العزيز مهم جدا للحجاج ...; الرد مباشر على السؤال حول أفضل السلوكيات للحاج

### Row 54 - الثبات الانفعالي

- Axis: الأسئلة
- Status: `scored`
- Score: `84.5`
- Rating: `very_good`
- Excel evaluation method: Tool
- Explanation: A composite rubric score is available from multiple normalized signals.
- Calculation note: The final score is a weighted composite of the listed normalized signals.
- Next action: Review composite evidence and weights before operational acceptance.

**Selected Scoring Signal**

- Tool: `composite`
- Signal: `emotional_stability` - Composite emotional stability score
- Measured value: `{"components": ["blink_rate=50.0", "facial_expression=100.0", "volume_db=80.0", "pitch_variation=90.0", "body_movement=90.0", "filler_words=100.0"]}`
- Signal score: `84.5`
- Confidence: `0.55`
- Evidence: blink_rate=50.0; facial_expression=100.0; volume_db=80.0; pitch_variation=90.0; body_movement=90.0; filler_words=100.0

**All Supporting Signals**

- `composite:emotional_stability` - Composite emotional stability score
  - Value: `{"components": ["blink_rate=50.0", "facial_expression=100.0", "volume_db=80.0", "pitch_variation=90.0", "body_movement=90.0", "filler_words=100.0"]}`
  - Score: `84.5`
  - Confidence: `0.55`
  - Evidence: blink_rate=50.0; facial_expression=100.0; volume_db=80.0; pitch_variation=90.0; body_movement=90.0; filler_words=100.0

### Row 55 - القابلية للاقتباس و التداول

- Axis: الأسئلة
- Status: `scored`
- Score: `70.0`
- Rating: `needs_development`
- Excel evaluation method: Tool
- Explanation: A direct transcript-based rubric score is available for this Excel row.
- Calculation note: The final score came from the rubric scorer for this exact Excel row.
- Next action: Review the transcript evidence and confidence before accepting this score operationally.

**Selected Scoring Signal**

- Tool: `openai_rubric`
- Signal: `criterion_score_55` - Direct rubric score for Excel row 55
- Measured value: `{"criterion": "القابلية للاقتباس و التداول", "explanation": "الجمل المقدمة واضحة لكنها ليست مركزة أو قوية بشكل كافٍ لتكون جملًا قابلة للاقتباس بسهولة في الإعلام أو منصات التواصل.", "rating": "needs_development", "source": "openai_rubric", "status": "scored"}`
- Signal score: `70.0`
- Confidence: `0.85`
- Evidence: يشربوا المياه قبل أن يعطشوا; استخدام الكمامة على الوجه في حالة الازدحام الشديد

**All Supporting Signals**

- `openai_rubric:criterion_score_55` - Direct rubric score for Excel row 55
  - Value: `{"criterion": "القابلية للاقتباس و التداول", "explanation": "الجمل المقدمة واضحة لكنها ليست مركزة أو قوية بشكل كافٍ لتكون جملًا قابلة للاقتباس بسهولة في الإعلام أو منصات التواصل.", "rating": "needs_development", "source": "openai_rubric", "status": "scored"}`
  - Score: `70.0`
  - Confidence: `0.85`
  - Evidence: يشربوا المياه قبل أن يعطشوا; استخدام الكمامة على الوجه في حالة الازدحام الشديد

### Row 56 - استراتيجات الإجابة

- Axis: الأسئلة
- Status: `scored`
- Score: `100.0`
- Rating: `excellent`
- Excel evaluation method: Tool
- Explanation: A direct transcript-based rubric score is available for this Excel row.
- Calculation note: The final score came from the rubric scorer for this exact Excel row.
- Next action: Review the transcript evidence and confidence before accepting this score operationally.

**Selected Scoring Signal**

- Tool: `openai_rubric`
- Signal: `criterion_score_56` - Direct rubric score for Excel row 56
- Measured value: `{"criterion": "استراتيجات الإجابة", "explanation": "المتحدث استخدم استراتيجيات إجابة واضحة مثل التحضير، التأطير، والتجسير في الرد على السؤال.", "rating": "excellent", "source": "openai_rubric", "status": "scored"}`
- Signal score: `100.0`
- Confidence: `0.95`
- Evidence: بدأ بالترحيب والشكر; أجاب مباشرة على السؤال; قدم حلول واضحة ومحددة

**All Supporting Signals**

- `openai_rubric:criterion_score_56` - Direct rubric score for Excel row 56
  - Value: `{"criterion": "استراتيجات الإجابة", "explanation": "المتحدث استخدم استراتيجيات إجابة واضحة مثل التحضير، التأطير، والتجسير في الرد على السؤال.", "rating": "excellent", "source": "openai_rubric", "status": "scored"}`
  - Score: `100.0`
  - Confidence: `0.95`
  - Evidence: بدأ بالترحيب والشكر; أجاب مباشرة على السؤال; قدم حلول واضحة ومحددة

