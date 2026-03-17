---
name: youtube-timeline-vision
description: Analyze YouTube videos as a timestamped timeline instead of relying only on raw listening or subtitle reading. Use when the user shares a YouTube link and wants to know what appears on screen at specific times, what is said at specific times, what on-screen text appears, or wants a combined visual + speech timeline report. Best for building a first-pass "watch the video for me" workflow from a YouTube URL.
---

# YouTube Timeline Vision

Use this skill to turn a YouTube URL into a timestamped report with:

- speech timeline from YouTube subtitles / auto-captions
- sampled visual timeline from extracted frames
- OCR text read from frames
- merged timeline output for quick querying

## Workflow

1. Run the analyzer script:

```bash
python3 /home/andy/.openclaw/workspace/skills/youtube-timeline-vision/scripts/analyze_youtube.py "YOUTUBE_URL"
```

Optional sampling interval:

```bash
python3 /home/andy/.openclaw/workspace/skills/youtube-timeline-vision/scripts/analyze_youtube.py "YOUTUBE_URL" --sample-every 15
```

2. Read the generated files under:

```bash
/home/andy/.openclaw/workspace/outputs/youtube-vision/<video-id>/
```

3. Start with `timeline.md` for a readable summary.
4. If the user asks precise questions, inspect `timeline.json`, `subtitles.json`, and `visual_events.json`.

## What the script does

- fetch video metadata with local `yt-dlp`
- download the video plus subtitles / auto-captions when available
- extract one frame every N seconds with local `ffmpeg`
- run OCR on frames with `tesseract.js`
- merge subtitle windows and visual buckets into one timeline

## Answering style

When reporting back to the user:

- separate **Speech** from **Visual/OCR** when confidence differs
- treat subtitle-derived speech as likely but not perfect
- treat OCR as partial visual evidence, not full scene understanding
- say when a timestamp is approximate because sampling is every N seconds
- if the video lacks subtitles, say that speech coverage is limited

## Read when needed

- For output files and caveats: `references/output-format.md`
