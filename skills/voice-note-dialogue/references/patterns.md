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

TTS audio:
./2026-03-17/1923_語音留言回覆.mp3
```

## Mode C output shape

```json
{
  "transcription": "你好，憨吉，你能聽到嗎？",
  "reply": "有，我聽得到，老爸 😎",
  "archive_markdown": "/repo/2026-03-17/1923_語音留言測試.md",
  "tts_audio": "/repo/2026-03-17/1923_語音留言回覆.mp3"
}
```

## Notes

- Keep replies short and natural.
- Do not over-correct ambiguous words in the transcript.
- Apply only light normalization, such as punctuation cleanup and common Traditional Chinese replacements.
- TTS reply text should not include emoji.
- If transcription confidence is shaky, say so.
- Archive Markdown stays in the dated folder and `README.md` gets one extra bullet with tags and summary.
