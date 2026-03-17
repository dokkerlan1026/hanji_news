# Prompting Notes

## Verified observations

Server:
- use `OLLAMA_VOICE_BASE_URL` for the private Ollama endpoint

Observed models of interest:
- `sematre/orpheus:zh`
- `karanchopda333/whisper:latest`

### Whisper model

A basic `/api/generate` text prompt succeeded:

Prompt idea:
```text
請逐字轉錄：你好，今天天氣很好。只輸出轉錄文字。
```

Observed behavior:
- Returned the expected Chinese sentence.
- This verifies that the model is reachable through text completion.
- This does **not** prove native audio-file transcription through Ollama.

### Orpheus model

A basic `/api/generate` prompt with a normal Chinese request returned an empty string.

Prompt idea:
```text
請用一句中文描述下雨天的聲音。
```

Observed behavior:
- Response body was empty.
- Treat the model as reachable but not yet validated for practical TTS output through this endpoint.

## Suggested usage patterns

### Inspect models

```bash
python3 scripts/probe_models.py
```

### Generic text call

```bash
python3 scripts/ollama_call.py \
  --model karanchopda333/whisper:latest \
  --prompt '請逐字轉錄：你好，今天天氣很好。只輸出轉錄文字。'
```

### Whisper best-effort audio prompt

```bash
python3 scripts/whisper_stt.py \
  --audio ./sample.mp3 \
  --language zh \
  --output ./transcript.txt
```

### Orpheus raw call

```bash
python3 scripts/orpheus_tts.py \
  --text '老爸，今天也辛苦了。' \
  --output ./orpheus-response.txt
```

## Interpreting failures

- Empty string: model reachable, prompt format may be wrong, or the model may expect a custom downstream decoder / format.
- HTTP 404: wrong base URL or model missing.
- HTTP 500: model / runtime issue on remote Ollama.
- Nonsense output: prompt format mismatch.

## Safe expectations

This skill is best used as a bridge and debugging harness around a known Ollama endpoint. It is reliable for:

- model discovery
- endpoint inspection
- raw prompt experiments
- saving raw outputs

It is not yet a guarantee of true end-to-end STT or TTS unless the specific model / prompt combination is verified in that run.
