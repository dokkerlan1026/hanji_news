# Patterns

## Mode A output shape

```text
Transcription:
你好，憨吉，你能聽到嗎？

Reply:
有，我聽得到，老爸 😎
```

## Mode B output shape

```text
Transcription:
你好，憨吉，你能聽到嗎？

Reply text:
有，我聽得到，老爸 😎

TTS handoff:
Saved reply text for synthesis at ./reply_for_tts.txt
```

## Notes

- Keep replies short and natural.
- Do not over-correct ambiguous words in the transcript.
- If transcription confidence is shaky, say so.
- If TTS is not available, save the reply text and stop there.
