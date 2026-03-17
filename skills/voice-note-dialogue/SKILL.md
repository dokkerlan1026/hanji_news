---
name: voice-note-dialogue
description: Handle voice-note conversations with a two-stage workflow. Use when a user sends an audio message and wants either (1) speech-to-text plus a normal text reply, or (2) speech-to-text plus a generated reply with a TTS handoff step. Supports testing with Groq STT first, then optional TTS integration.
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

### Mode B — STT to text reply to TTS handoff

Use when the user wants a voice-style round trip:

1. transcribe the inbound audio
2. generate the assistant reply in text
3. pass that reply into a TTS step
4. return or save the synthesized output

If TTS is not fully wired yet, still complete steps 1 and 2 and clearly mark step 3 as pending / experimental.

## Preferred pipeline

- Prefer Groq STT for transcription when available.
- Treat Ollama STT as experimental unless a specific model / route is verified for real audio input.
- Keep TTS modular. Do not hardwire one provider unless the environment is already configured.

## Workflow

1. Transcribe the inbound voice note.
2. Clean obvious punctuation or spacing errors only if meaning is clear.
3. Write a short `user_text` result.
4. Draft a concise assistant reply.
5. If Mode B is requested, save the reply text for downstream TTS.
6. Report what is verified vs what is still a placeholder.

## Scripts

- `scripts/voice_note_flow.py`
  - Runs Mode A end to end
  - Can also save a TTS input text file for Mode B
- `scripts/groq_transcribe.py`
  - Lightweight wrapper for Groq transcription

## References

Read `references/patterns.md` for example outputs and integration notes.
