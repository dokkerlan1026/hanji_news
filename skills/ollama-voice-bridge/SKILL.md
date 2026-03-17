---
name: ollama-voice-bridge
description: Bridge to a user-controlled Ollama service for speech-related models and voice workflows. Use when a user wants to call their local or private Ollama server, inspect available models, run the sematre/orpheus:zh TTS-style model, run the karanchopda333/whisper:latest STT-style model, or create / debug Python wrappers around Ollama HTTP APIs for local voice tooling.
---

# Ollama Voice Bridge

Use a user-controlled Ollama service through `OLLAMA_VOICE_BASE_URL`. Do not hardcode or casually repeat private IP addresses in chat replies, skills, or committed files unless the user explicitly wants that exposure.

## Quick workflow

1. Probe the server first with `scripts/probe_models.py`.
2. For generic text generation or model inspection, use `scripts/ollama_call.py`.
3. For speech-to-text style prompting, use `scripts/whisper_stt.py`.
4. For TTS-style model prompting, use `scripts/orpheus_tts.py`.
5. If a model does not return usable output, say so plainly and report the raw behavior.

## Important caveat

The current remote Ollama endpoint exposes these models through standard text completion APIs. In testing:

- `karanchopda333/whisper:latest` responds to text prompts through `/api/generate`
- `sematre/orpheus:zh` is reachable, but a normal text prompt returned an empty string

Treat both as model-specific and experimental. Do not promise real audio transcription or audio waveform generation unless the actual call succeeds.

## Endpoints

- List models: `GET /api/tags`
- Inspect model: `POST /api/show`
- Generate text: `POST /api/generate`
- Chat: `POST /api/chat`

Base URL default: `OLLAMA_VOICE_BASE_URL` or fallback `http://127.0.0.1:11434`

## When to use which script

### `scripts/probe_models.py`
Use to verify the server is up and to list models before building a workflow.

### `scripts/ollama_call.py`
Use for generic calls, experiments, or debugging prompts.

### `scripts/whisper_stt.py`
Use when the user wants STT-like behavior. Prefer `--text` for prompt-driven transcription tests. If given `--audio`, the script embeds base64 plus metadata into the prompt, but this is best-effort only because standard Ollama text completion does not natively accept audio files.

### `scripts/orpheus_tts.py`
Use when the user wants to try the Orpheus model. The script sends a prompt and saves the raw response. If the response is empty, report that the current remote model did not emit usable output for that prompt.

## Reporting guidance

When using this skill, always report:

- server URL used
- model used
- endpoint used
- whether output was non-empty
- whether the result is verified or only experimental

## References

Read `references/prompting.md` for tested prompts, limitations, and command examples.
