---
name: minimax
description: |
  MiniMax Open Platform API integration for text, speech, voice cloning, voice design,
  video generation, image generation, music generation, lyrics generation, file management,
  and model listing. Use when the user explicitly asks for MiniMax, minimaxi.com,
  platform.minimaxi.com, Hailuo, MiniMax-M2, MiniMax speech, MiniMax image/video/music APIs,
  or wants to call MiniMax API endpoints.
metadata:
  author: ledboot
  version: "1.0.0"
---

# MiniMax Open Platform Skill

Use this skill to call MiniMax Open Platform APIs and to guide implementation work involving MiniMax models or multimodal generation.

## Documentation

Always prefer current official MiniMax docs before making or changing API calls:

- API overview: https://platform.minimaxi.com/docs/api-reference/api-overview
- Documentation index: https://platform.minimaxi.com/docs/llms.txt
- Error codes: https://platform.minimaxi.com/docs/api-reference/errorcode.md
- Rate limits: https://platform.minimaxi.com/docs/guides/rate-limits.md
- Local reference index: `references/api-overview.md`
- Lyrics quick reference: `references/lyrics-generation.md`

MiniMax exposes multimodal APIs for text, speech, voice cloning, voice design, voice management, video, image, music, lyrics, files, and model listing. Because the platform changes quickly, use `llms.txt` to locate the exact current page or OpenAPI spec for any endpoint that is not already covered by a bundled script.

## Authentication

Use a Bearer token. Never store API keys in skill files, memory, committed code, or examples with real values.

```bash
export MINIMAX_API_KEY="your_api_key"
```

The default base URL used by bundled scripts is:

```text
https://api.minimaxi.com
```

Override only when MiniMax documentation for a specific endpoint says to:

```bash
export MINIMAX_API_BASE="https://api.minimaxi.com"
```

## Bundled Scripts

### Generic JSON API Caller

Use `scripts/minimax_api.py` for JSON-based MiniMax endpoints once the endpoint path and body are confirmed from official docs.

```bash
python scripts/minimax_api.py \
  --method POST \
  --path /v1/lyrics_generation \
  --body '{"mode":"write_full_song","prompt":"一首关于夏日海边的轻快情歌"}'
```

Use `--body-file` for larger payloads:

```bash
python scripts/minimax_api.py --method POST --path /v1/lyrics_generation --body-file request.json
```

Use `--raw` when the endpoint returns non-JSON content:

```bash
python scripts/minimax_api.py --method GET --path /v1/files/retrieve_content?file_id=... --raw -o output.bin
```

### Lyrics Generation

Use `scripts/lyrics_generation.py` for the MiniMax Lyrics Generation endpoint.

```bash
python scripts/lyrics_generation.py \
  --prompt "一首关于夏日海边的轻快情歌"
```

Edit or extend existing lyrics:

```bash
python scripts/lyrics_generation.py \
  --mode edit \
  --title "夏日海风的约定" \
  --lyrics-file old_lyrics.txt \
  --prompt "续写第二段和副歌"
```

## Capability Routing

- Text: use MiniMax OpenAI-compatible or Anthropic-compatible docs when the user wants chat/completions or agent coding model integration.
- Speech: use T2A HTTP/WebSocket for synchronous speech, and T2A async for long text.
- Voice cloning: use upload clone audio first, then clone voice. Check account eligibility requirements in official docs before promising availability.
- Voice design: use voice design docs for text-described custom voices.
- Voice management: use voice query/delete docs for available voice IDs and cleanup.
- Video: use text-to-video, image-to-video, first/last-frame video, subject-reference video, video-agent, query, and download docs.
- Image: use text-to-image and image-to-image docs.
- Music: use lyrics generation and music generation docs. Use lyrics generation first when the user wants editable song text before generating audio.
- Files: use file upload, list, retrieve, download, and delete docs. File download URLs may expire; save important outputs promptly.
- Models: use OpenAI-compatible or Anthropic-compatible model listing docs depending on the integration surface.

## Workflow

1. Identify the desired MiniMax capability and whether the user explicitly named an endpoint or model.
2. Fetch or consult the current official page for that capability.
3. Confirm authentication, endpoint path, request body, response shape, polling requirements, and file handling.
4. Use a bundled script when it fits. Otherwise call the endpoint with `scripts/minimax_api.py`, `curl`, or a focused script following the official docs.
5. For async tasks, save the returned `task_id`, poll until a terminal state, then retrieve/download generated files if required.
6. Surface API errors with response body, error code, and trace/request id when present.
7. Do not hide safety, eligibility, quota, rate-limit, or expiration constraints.

## Error Handling

- Treat HTTP 401/403 as authentication, permission, or account eligibility problems.
- Treat HTTP 400 as a request schema or parameter issue; compare with the current endpoint docs.
- Treat HTTP 429 as rate limiting; back off and avoid tight polling loops.
- For async generation, distinguish submission success from generation success.
- Include MiniMax trace or request identifiers in troubleshooting notes when the API returns them.

## Output Hygiene

- Store generated files under the current project output folder when the user asks for saved artifacts.
- Keep API responses as JSON when they are needed for follow-up polling or debugging.
- Do not commit generated binaries, secrets, or account-specific identifiers unless the user explicitly asks and it is safe.
- For song workflows, keep lyrics, prompt, notes, generated audio, and raw API response in separate files.
