---
name: mureka
description: |
  Mureka AI music generation and audio processing. Use when user wants to generate AI music,
  songs, instrumentals, create/extend lyrics, clone vocals, generate text-to-speech or podcasts,
  or process audio files (stem separation, song recognition).

  Mureka platform (https://platform.mureka.ai) provides: Song generation (v7.5/O1 models),
  instrumental generation, lyrics generation/extension, vocal cloning, TTS, podcast generation,
  audio stem separation.

  Trigger on: Mureka, AI music, song generation, music generation, vocal cloning,
  lyrics generation, instrumental, TTS, text-to-speech, audio generation, stem separation,
  song recognition.
license: Apache 2.0
metadata:
  author: ledboot
  version: "1.0.0"
---

# Mureka AI Music Skill

Mureka is an AI music generation platform (https://platform.mureka.ai). This skill provides
comprehensive access to Mureka's API for music creation, audio processing, and voice synthesis.

## Retrieval Sources

**Always fetch the latest API information before making API calls:**

| Source | URL |
|--------|-----|
| Main Documentation | https://platform.mureka.ai/docs/ |
| Quickstart Guide | https://platform.mureka.ai/docs/en/quickstart.html |
| Error Codes | https://platform.mureka.ai/docs/en/error-codes.html |
| Changelog | https://platform.mureka.ai/docs/en/changelog.html |

**API Reference Files (bundled in `references/`):**

- `references/api-reference.md` - Complete API reference with request/response tables
- `references/api-endpoints.md` - All API endpoints overview
- `references/quickstart.md` - Authentication and first request guide
- `references/song-api.md` - Song generation and query APIs
- `references/lyrics-api.md` - Lyrics generation and extension
- `references/instrumental-api.md` - Instrumental generation
- `references/vocal-api.md` - Vocal cloning API
- `references/tts-api.md` - Text-to-speech and podcast APIs
- `references/song-processing-api.md` - Song recognition, describe, stem, file upload

## Base Configuration

- **API Base URL**: `https://api.mureka.ai`
- **Authentication**: Bearer token (API key in Authorization header)
- **Content-Type**: `application/json` (except file uploads use multipart/form-data)

### Environment Setup
```bash
export MUREKA_API_KEY="your_api_key_here"
```

### Verify API Key
Test your API key before making requests:
```bash
curl https://api.mureka.ai/v1/song/query/435134 \
  -H "Authorization: Bearer $MUREKA_API_KEY"
```
- **Valid key**: Returns task info or status
- **Invalid key**: Returns `{"error":{"message":"Invalid Authentication"}}`

## API Endpoints Summary

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/song/generate` | POST | Generate full song with lyrics |
| `/v1/song/query/{task_id}` | GET | Poll song task status |
| `/v1/song/extend` | POST | Extend existing song |
| `/v1/lyrics/generate` | POST | Generate lyrics from prompt |
| `/v1/lyrics/extend` | POST | Extend existing lyrics |
| `/v1/instrumental/generate` | POST | Generate instrumental music |
| `/v1/instrumental/query/{task_id}` | GET | Poll instrumental task status |
| `/v1/vocal/clone` | POST | Clone vocal from audio sample |
| `/v1/tts/generate` | POST | Text-to-speech |
| `/v1/tts/podcast` | POST | Generate podcast |
| `/v1/song/recognize` | POST | Identify song from audio |
| `/v1/song/describe` | POST | Analyze song characteristics |
| `/v1/song/stem` | POST | Separate audio stems |
| `/v1/files/upload` | POST | Upload files |
| `/v1/account/billing` | GET | Query billing info |

## Song Query Response Structure

**GET `/v1/song/query/{task_id}`** returns:

```json
{
  "id": "string",
  "created_at": 0,
  "finished_at": 0,
  "model": "string",
  "status": "string",
  "failed_reason": "string",
  "choices": [
    {
      "index": 0,
      "id": "string",
      "url": "string",
      "flac_url": "string",
      "wav_url": "string",
      "stream_url": "string",
      "duration": 0,
      "lyrics_sections": [
        {
          "section_type": "string",
          "start": 0,
          "end": 0,
          "lines": [
            {
              "start": 0,
              "end": 0,
              "text": "string",
              "words": [
                {"start": 0, "end": 0, "text": "string"}
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

**Status values**: `preparing`, `running`, `succeeded`, `failed`

**Field descriptions**:
- `id`: Task ID
- `created_at`: Unix timestamp of task creation
- `finished_at`: Unix timestamp when task completed
- `model`: Model used (e.g., "mureka-8")
- `status`: Current task status
- `failed_reason`: Error message if status is "failed"
- `choices`: Array of generated song versions (typically 1-2 versions)
- `choices[].lyrics_sections`: Structured lyrics with timing information
  - `section_type`: Section type (e.g., "intro", "verse", "chorus", "bridge", "outro")
  - `start`/`end`: Section start/end time in milliseconds
  - `lines[].text`: Lyric line text
  - `lines[].start`/`lines[].end`: Line start/end time in milliseconds

## Common Workflows

### Generate a Complete Song

1. Generate or provide lyrics using `/v1/lyrics/generate`
2. Generate song with `/v1/song/generate` using lyrics, model, and style prompt
3. Save the returned `task_id`
4. Poll `/v1/song/query/{task_id}` until status is "succeeded"
5. Use `scripts/parse_lyrics.py` to generate .lrc file from response

### Use Vocal Cloning

1. Clone voice: `POST /v1/vocal/clone` with audio sample to get `vocal_id`
2. Use `vocal_id` in song generation request

### Separate Audio Stems

1. Upload or reference song with `/v1/song/stem`
2. Poll task until completion
3. Receive separated tracks (vocals, drums, bass, etc.)

## LRC File Generation

Use the bundled script to parse API response and generate .lrc lyrics files:

```bash
# Fetch and parse from API
python scripts/parse_lyrics.py <task_id> <api_key>

# Parse from JSON file
python scripts/parse_lyrics.py --response-file response.json

# Parse from JSON string
python scripts/parse_lyrics.py --response-json '<json>'

# With options
python scripts/parse_lyrics.py <task_id> <api_key> --version 0 --output song.lrc --title "My Song" --artist "Artist"
```

**LRC format**:
```
[ti:Song Title]
[ar:Artist]
[al:Album]
[by:Generated by Mureka Skill]
[offset:0]

[00:00.00]Line 1 lyrics
[00:05.50]Line 2 lyrics
```

## Error Handling

Errors return:
```json
{
  "error": {
    "message": "Error description"
  },
  "trace_id": "1e94aba5a2de4cc4bff54a2813c8d36c"
}
```

Common error codes:
- `401`: Invalid or missing API key
- `400`: Bad request (missing parameters)
- `429`: Rate limit exceeded
- `500`: Server error

**Tip**: Always log `trace_id` for troubleshooting with support team.

## Example curl Commands

**Generate song:**
```bash
curl -X POST https://api.mureka.ai/v1/song/generate \
  -H "Authorization: Bearer $MUREKA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "lyrics": "[Verse]\nIn the stormy night, I wander alone\nLost in the rain, feeling like I have been thrown",
    "model": "auto",
    "prompt": "r&b, slow, passionate, male vocal"
  }'
```

**Query task status:**
```bash
curl https://api.mureka.ai/v1/song/query/{task_id} \
  -H "Authorization: Bearer $MUREKA_API_KEY"
```

**Generate instrumental:**
```bash
curl -X POST https://api.mureka.ai/v1/instrumental/generate \
  -H "Authorization: Bearer $MUREKA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "upbeat pop instrumental, summer vibes",
    "duration": 180
  }'
```

**Clone vocal:**
```bash
curl -X POST https://api.mureka.ai/v1/vocal/clone \
  -H "Authorization: Bearer $MUREKA_API_KEY" \
  -F "file=@vocal_sample.mp3"
```

**Generate lyrics:**
```bash
curl -X POST https://api.mureka.ai/v1/lyrics/generate \
  -H "Authorization: Bearer $MUREKA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A heartfelt ballad about traveling the world"
  }'
```

**Text-to-speech:**
```bash
curl -X POST https://api.mureka.ai/v1/tts/generate \
  -H "Authorization: Bearer $MUREKA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Welcome to the future of music creation",
    "voice": "default"
  }'
```

## Model Versions

- `auto`: Automatically select best model
- `mureka-7.5`: Enhanced melody and arrangement, realistic vocals, supports streaming
- `mureka-7.6`: Improved vocals and arrangement over 7.5
- `mureka-o2`: Intelligent algorithm for superior quality, multilingual, contextual BGM
- `mureka-8`: Latest model with highest quality output
