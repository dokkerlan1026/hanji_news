---
name: voice-note-dialogue
description: Handle voice-note conversations with a practical end-to-end workflow. Use when a user sends an audio message and wants either (1) speech-to-text plus a normal text reply, (2) speech-to-text plus a generated reply with real TTS audio output, or (3) a one-command workflow that transcribes, replies, archives the result into the dated repo structure, and prepares the conversation for ongoing voice-note use.
---

# Voice Note Dialogue

Use this skill for practical voice-note conversations.

## Modes

### Mode A — STT to text reply

Use when the goal is simply:

1. transcribe the inbound audio
2. understand the message
3. reply normally in text

This is the default and most reliable workflow.

### Mode B — STT to text reply to real TTS audio

Use when the user wants a voice-style round trip:

1. transcribe the inbound audio
2. generate the assistant reply in text
3. synthesize that reply into audio
4. return or save the generated audio file

This skill uses Edge TTS through the `node-edge-tts` dependency already present inside OpenClaw.

### Mode C — full voice-note job

Use when the user wants a reusable workflow:

1. transcribe the inbound voice note
2. generate the assistant reply
3. optionally synthesize the reply to mp3
4. save a Markdown note into the daily repo folder
5. update `README.md` with tags, summary, and link

## Preferred pipeline

- Prefer Groq STT for transcription when available.
- Treat Ollama STT as experimental unless a specific model / route is verified for real audio input.
- Use Edge TTS for easy local synthesis when no dedicated API-backed TTS is required.

## Scripts

- `scripts/voice_note_flow.py`
  - Mode A / B core logic
- `scripts/groq_transcribe.py`
  - Lightweight wrapper for Groq transcription
- `scripts/edge_tts_synthesize.py`
  - Generate mp3 output with Edge TTS
- `scripts/archive_voice_note.py`
  - Save transcript + reply into the dated repo structure and update `README.md`
- `scripts/run_voice_note_job.py`
  - One-command workflow for A + B + C together
  - Auto-fills current date and time prefix when omitted
  - Archives into the daily repo structure

## References

Read `references/patterns.md` for example outputs and integration notes.
