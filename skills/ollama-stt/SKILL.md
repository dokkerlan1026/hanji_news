---
name: ollama-stt
description: Validate and use an Ollama-hosted speech-to-text backend for audio transcription when the user sends a voice message, MP3, WAV, M4A, OGG, or other audio file and wants text from speech. Use this skill to inspect whether the configured Ollama model is a real STT/audio model before claiming transcription support. Also use it to normalize audio files for future speech backends.
---

# Ollama STT

Use this skill when the user wants speech transcribed from an audio file and the intended backend is an Ollama-hosted model or Ollama-adjacent speech service.

## Important warning

Do not assume a model is speech-capable just because its name says `whisper`.
Inspect it first.

The currently pulled model `karanchopda333/whisper:latest` appears to be a renamed `llama3.2` text model, not a verified audio transcription backend.

Read `references/current-state.md` when you need the evidence.

## Workflow

### 1. Inspect the configured model

```bash
python3 /home/andy/.openclaw/workspace/skills/ollama-stt/scripts/inspect_ollama_model.py
```

If it exits non-zero and reports `looks_text_only: true`, do not pretend transcription is available.

### 2. Normalize the audio input for STT

```bash
python3 /home/andy/.openclaw/workspace/skills/ollama-stt/scripts/transcribe_audio.py /path/to/audio.mp3
```

This currently:

- validates the configured model first
- converts audio to mono 16 kHz WAV with local ffmpeg
- stops with a clear error if the backend is not a real STT endpoint

## Supported input intent

Use for local audio files such as:

- `.mp3`
- `.wav`
- `.m4a`
- `.ogg`
- saved voice-message attachments

## Response rules

- If the backend is fake or text-only, say so clearly.
- Do not claim you transcribed audio if you only inspected metadata.
- If a genuine STT backend is added later, use this skill as the entry point and extend the script instead of inventing a new workflow.
