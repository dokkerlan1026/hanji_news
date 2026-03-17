# Groq STT usage

## Endpoint

`POST https://api.groq.com/openai/v1/audio/transcriptions`

## Good defaults

- Model: `whisper-large-v3`
- Response format: `verbose_json`
- Temperature: `0`
- Normalize long or messy audio to 16 kHz mono WAV when needed

## Input types

Use for:

- `.mp3`
- `.wav`
- `.m4a`
- `.ogg`
- `.webm`
- saved voice-message attachments

## Notes

- Groq's API is OpenAI-compatible for speech transcription.
- Free tier docs mention a 25 MB attachment limit.
- Use `verbose_json` if you want segment/timestamp-rich output.
- Prefer `language=zh` when the user audio is mainly Chinese to reduce confusion.

## Output handling

When returning results to the user:

- If the transcript is short, quote it directly.
- If it is long, summarize first and offer the raw transcript on request.
- Preserve obvious names, numbers, symbols, and mixed Chinese/English terms.
