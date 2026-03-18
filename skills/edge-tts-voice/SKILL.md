---
name: edge-tts-voice
description: Generate spoken audio files from text using Microsoft Edge's online TTS service when the user wants a voice message, spoken self-introduction, narration, or audio output from text. Use for Mandarin Chinese or Taiwanese Mandarin voice output without needing an API key.
---

# Edge TTS Voice

Use this skill to turn text into an MP3 file.

## Default workflow

```bash
node /home/andy/.openclaw/workspace/skills/edge-tts-voice/scripts/synthesize.js /home/andy/.openclaw/workspace/outputs/tts/output.mp3 "你好，我是憨吉。"
```

## Defaults

- Default voice: `zh-TW-HsiaoChenNeural`
- Default rate: `+0%`
- Output: MP3

## Best practices

- Remove emoji before synthesis.
- Use natural spoken punctuation.
- Keep sentences short if the user wants conversational delivery.
- For Taiwanese Mandarin, prefer `zh-TW-*` voices.

## Read when needed

- Voice suggestions: `references/voices.md`
