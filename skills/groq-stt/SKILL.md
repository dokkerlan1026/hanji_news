---
name: groq-stt
description: Transcribe audio files and voice messages using Groq Speech-to-Text when the user sends MP3, WAV, M4A, OGG, WEBM, or other speech audio and wants to know what was said. Use this skill to give the assistant a practical "ear" via Groq's OpenAI-compatible speech transcription API.
---

# Groq STT

Use this skill when the input is speech audio and the goal is to understand the spoken content.

## Workflow

Run the transcription script:

```bash
python3 /home/andy/.openclaw/workspace/skills/groq-stt/scripts/transcribe_groq.py /path/to/audio.wav
```

Optional language hint:

```bash
python3 /home/andy/.openclaw/workspace/skills/groq-stt/scripts/transcribe_groq.py /path/to/audio.wav --language zh
```

The script expects a Groq API key via `GROQ_API_KEY` or `--api-key`.
Do not hardcode secrets into the repo.

## Recommended defaults

- model: `whisper-large-v3`
- response format: `verbose_json`
- temperature: `0`
- set `--language zh` for Chinese-heavy audio

## Response rules

- If the transcript is short, return the text directly.
- If the transcript is long, summarize it and offer the raw text.
- If confidence seems low, say which words may be uncertain.
- Do not invent missing words when the audio is unclear.

## Read when needed

For endpoint notes and handling guidance, read `references/usage.md`.
