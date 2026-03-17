# Output files

The analyzer writes results under `outputs/youtube-vision/<video-id>/`.

## Files

- `summary.json` — basic metadata and counts
- `subtitles.json` — timestamped speech from YouTube subtitles / auto-captions
- `visual_events.json` — sampled frames with OCR text
- `timeline.json` — merged time buckets with speech + visual/OCR
- `timeline.md` — readable markdown report
- `frames/` — extracted JPG frames

## Important limitations

This is a v1 workflow.

- Speech comes from YouTube subtitles or auto-captions, not local Whisper ASR.
- Visual analysis is sampled every N seconds plus OCR. It does not yet do object tracking or dense scene captioning.
- If a video has no subtitles, speech output will be sparse or empty.
- OCR works best when the frame contains large, clear text.

## Best use cases

- Ask what appears on screen at rough time windows.
- Ask what the speaker says around a timestamp.
- Ask whether on-screen text matches the spoken content.
- Build a first-pass timeline before doing deeper manual review.
