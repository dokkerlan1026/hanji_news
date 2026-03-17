# Errors

Unexpected failures, command errors, integration issues, and debugging notes.

**Areas**: frontend | backend | infra | tests | docs | config
**Statuses**: pending | in_progress | resolved | wont_fix | promoted

## Entry Template

```markdown
## [ERR-YYYYMMDD-XXX] skill_or_command_name

**Logged**: ISO-8601 timestamp
**Priority**: high
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Summary
Brief description of what failed

### Error
Actual error message or output

### Context
- Command/operation attempted
- Input or parameters used
- Environment details if relevant

### Suggested Fix
If identifiable, what might resolve this

### Metadata
- Reproducible: yes | no | unknown
- Related Files: path/to/file.ext
- See Also: ERR-20250110-001 (if recurring)
```

---
## [ERR-20260317-001] groq-stt-api-auth

**Logged**: 2026-03-17T18:33:00+08:00
**Priority**: high
**Status**: pending
**Area**: config

### Summary
Groq STT integration test failed with HTTP 403 Forbidden using provided API key.

### Error
```
urllib.error.HTTPError: HTTP Error 403: Forbidden
```

### Context
- Operation: test Groq STT transcription against `/openai/v1/audio/transcriptions`
- Script: `skills/groq-stt/scripts/transcribe_groq.py`
- Input: `outputs/youtube-vision/jNQXAC9IVRw/test-audio.wav`
- Likely causes: invalid key, revoked key, project restriction, or missing speech API entitlement.

### Suggested Fix
Verify the Groq API key in console, ensure speech-to-text access is enabled, and retry with a fresh key.

### Metadata
- Reproducible: yes
- Related Files: skills/groq-stt/scripts/transcribe_groq.py

---
