# Current state

The pulled model `karanchopda333/whisper:latest` currently appears to be a renamed `llama3.2` text model rather than a genuine speech-to-text model.

Evidence from `/api/show`:

- `parent_model` is `llama3.2:latest`
- `family` is `llama`
- the modelfile contains a standard chat template
- no explicit audio or speech modality was exposed in the returned metadata

## Practical consequence

Do not assume that a model named `whisper` inside Ollama is actually capable of audio transcription.

Before using any Ollama model for STT:

1. Inspect the model with `/api/show`
2. Verify it is genuinely audio/speech capable
3. Verify the API accepts audio input, not just text chat messages
4. Run a real transcription test on a short WAV/MP3 sample

## What this skill does today

- verifies whether the configured Ollama model looks like a real STT model
- normalizes audio to mono 16 kHz WAV for future STT backends
- refuses to claim success when the backend is actually text-only

## What this skill should do after a real backend exists

- accept local audio files like `.mp3`, `.m4a`, `.wav`, `.ogg`
- send the normalized audio to a verified speech backend
- return plain transcript text plus timestamped segments when available
