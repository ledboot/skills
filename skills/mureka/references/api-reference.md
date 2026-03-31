# Mureka API Reference

**Base URL**: `https://api.mureka.ai`

**Authentication**: `Authorization: Bearer $MUREKA_API_KEY`

**Content-Type**: `application/json` (except file uploads use `multipart/form-data`)

---

## Table of Contents

1. [Song APIs](#song-apis)
   - [POST /v1/song/generate](#post-v1songgenerate)
   - [GET /v1/song/query/{task_id}](#get-v1songquerytask_id)
   - [POST /v1/song/extend](#post-v1songextend)
   - [POST /v1/song/recognize](#post-v1songrecognize)
   - [POST /v1/song/describe](#post-v1songdescribe)
   - [POST /v1/song/stem](#post-v1songstem)
2. [Lyrics APIs](#lyrics-apis)
   - [POST /v1/lyrics/generate](#post-v1lyricsgenerate)
   - [POST /v1/lyrics/extend](#post-v1lyricsextend)
3. [Instrumental APIs](#instrumental-apis)
   - [POST /v1/instrumental/generate](#post-v1instrumentalgenerate)
   - [GET /v1/instrumental/query/{task_id}](#get-v1instrumentalquerytask_id)
4. [Vocal API](#vocal-api)
   - [POST /v1/vocal/clone](#post-v1vocalclone)
5. [TTS APIs](#tts-apis)
   - [POST /v1/tts/generate](#post-v1ttsgenerate)
   - [POST /v1/tts/podcast](#post-v1ttspodcast)
6. [File APIs](#file-apis)
   - [POST /v1/files/upload](#post-v1filesupload)
7. [Account API](#account-api)
   - [GET /v1/account/billing](#get-v1accountbilling)
8. [Common Structures](#common-structures)

---

## Song APIs

### POST /v1/song/generate

Generate a full song with lyrics.

**Request**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| lyrics | string | Yes | Song lyrics with section markers (e.g., `[Verse]`, `[Chorus]`) |
| prompt | string | Yes | Musical style description (genre, mood, instruments, vocal type) |
| model | string | No | Model version: `auto`, `mureka-7.5`, `mureka-7.6`, `mureka-o2`, `mureka-8` (default: `auto`) |
| vocal_id | string | No | Use cloned vocal instead of default voice |

**Request Example**
```json
{
  "lyrics": "[Verse]\nIn the stormy night, I wander alone\n[Pre-Chorus]\nLost in the rain, feeling like I have been thrown\n[Chorus]\nBut I'll find my way back home",
  "prompt": "r&b, slow, passionate, male vocal, 80bpm",
  "model": "mureka-8"
}
```

**Response**

| Field | Type | Description |
|-------|------|-------------|
| id | string | Task ID for polling status |
| created_at | integer | Unix timestamp of task creation |
| model | string | Model version used for generation |
| status | string | Task status: `preparing`, `processing`, `succeeded`, `failed` |
| trace_id | string | Trace ID for troubleshooting |
| failed_reason | string | Error message if status is `failed` |

**Response Example**
```json
{
  "id": "1436211",
  "created_at": 1677610602,
  "model": "mureka-8",
  "status": "preparing",
  "trace_id": "1e94aba5a2de4cc4bff54a2813c8d36c"
}
```

---

### GET /v1/song/query/{task_id}

Poll task status for song generation.

**Path Parameters**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| task_id | string | Yes | Task ID from `/v1/song/generate` response |

**Response**

| Field | Type | Description |
|-------|------|-------------|
| id | string | Task ID |
| created_at | integer | Unix timestamp of task creation |
| finished_at | integer | Unix timestamp when task completed (0 if not finished) |
| model | string | Model used for generation |
| status | string | Task status: `preparing`, `running`, `succeeded`, `failed` |
| failed_reason | string | Error message if status is `failed` |
| trace_id | string | Trace ID for troubleshooting |
| choices | array | Array of generated song versions |

**choices[]**

| Field | Type | Description |
|-------|------|-------------|
| index | integer | Version index (0-based) |
| id | string | Song version ID |
| url | string | Full song audio URL |
| flac_url | string | FLAC format audio URL (lossless) |
| wav_url | string | WAV format audio URL |
| stream_url | string | Streaming URL |
| duration | integer | Song duration in seconds |
| lyrics_sections | array | Structured lyrics with timing |

**lyrics_sections[]**

| Field | Type | Description |
|-------|------|-------------|
| section_type | string | Section type: `intro`, `verse`, `pre_chorus`, `chorus`, `bridge`, `outro` |
| start | integer | Section start time in milliseconds |
| end | integer | Section end time in milliseconds |
| lines | array | Lyric lines in this section |

**lines[]**

| Field | Type | Description |
|-------|------|-------------|
| start | integer | Line start time in milliseconds |
| end | integer | Line end time in milliseconds |
| text | string | Lyric text |
| words | array | Individual words with timing |

**words[]**

| Field | Type | Description |
|-------|------|-------------|
| start | integer | Word start time in milliseconds |
| end | integer | Word end time in milliseconds |
| text | string | Word text |

**Response Example**
```json
{
  "id": "1436211",
  "created_at": 1677610602,
  "finished_at": 1677611200,
  "model": "mureka-8",
  "status": "succeeded",
  "trace_id": "1e94aba5a2de4cc4bff54a2813c8d36c",
  "choices": [
    {
      "index": 0,
      "id": "song_abc123",
      "url": "https://cdn.mureka.ai/songs/abc123.mp3",
      "flac_url": "https://cdn.mureka.ai/songs/abc123.flac",
      "wav_url": "https://cdn.mureka.ai/songs/abc123.wav",
      "stream_url": "https://cdn.mureka.ai/songs/abc123/stream",
      "duration": 215,
      "lyrics_sections": [
        {
          "section_type": "verse",
          "start": 0,
          "end": 30000,
          "lines": [
            {
              "start": 0,
              "end": 5000,
              "text": "In the stormy night, I wander alone",
              "words": [
                {"start": 0, "end": 500, "text": "In"},
                {"start": 500, "end": 1000, "text": "the"},
                {"start": 1000, "end": 2000, "text": "stormy"},
                {"start": 2000, "end": 3500, "text": "night,"},
                {"start": 3500, "end": 5000, "text": "I"}
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

---

### POST /v1/song/extend

Extend an existing song with additional lyrics.

**Request**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| lyrics | string | Yes | Original song lyrics |
| prompt | string | Yes | Instructions for extension (e.g., "add a bridge and outro") |
| model | string | No | Model version: `auto`, `mureka-7.5`, `mureka-7.6`, `mureka-o2`, `mureka-8` |

**Request Example**
```json
{
  "lyrics": "[Verse]\nOriginal lyrics content...\n[Outro]\nFading out slowly",
  "prompt": "Add a bridge after the verse and extend the outro",
  "model": "mureka-8"
}
```

**Response**

| Field | Type | Description |
|-------|------|-------------|
| id | string | Task ID for polling status |
| created_at | integer | Unix timestamp of task creation |
| model | string | Model version used |
| status | string | Task status: `preparing`, `processing`, `succeeded`, `failed` |
| trace_id | string | Trace ID for troubleshooting |

**Response Example**
```json
{
  "id": "1436212",
  "created_at": 1677610602,
  "model": "mureka-8",
  "status": "preparing",
  "trace_id": "2e94aba5a2de4cc4bff54a2813c8d36c"
}
```

---

### POST /v1/song/recognize

Identify a song from audio file.

**Request** (multipart/form-data)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| file | file | Yes | Audio file to identify (mp3, wav, m4a, flac) |

**Response**

| Field | Type | Description |
|-------|------|-------------|
| status | string | Recognition status |
| song | object | Recognized song information |
| song.title | string | Song title |
| song.artist | string | Artist name |
| song.album | string | Album name (if available) |
| song.genre | string | Genre |
| song.duration | integer | Duration in seconds |
| confidence | float | Recognition confidence (0-1) |
| trace_id | string | Trace ID for troubleshooting |

**Response Example**
```json
{
  "status": "success",
  "song": {
    "title": "Starlight",
    "artist": "Unknown Artist",
    "album": "",
    "genre": "Pop",
    "duration": 215
  },
  "confidence": 0.95,
  "trace_id": "3e94aba5a2de4cc4bff54a2813c8d36c"
}
```

---

### POST /v1/song/describe

Analyze and describe a song's characteristics.

**Request** (multipart/form-data)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| file | file | Yes | Audio file to analyze (mp3, wav, m4a, flac) |

**Response**

| Field | Type | Description |
|-------|------|-------------|
| genre | string | Detected genre |
| mood | string | Detected mood (e.g., "energetic", "melancholic") |
| tempo | integer | BPM (beats per minute) |
| key | string | Musical key (e.g., "C minor") |
| instruments | array | Detected instruments |
| description | string | Text description of the song |
| trace_id | string | Trace ID for troubleshooting |

**Response Example**
```json
{
  "genre": "R&B",
  "mood": "Soulful",
  "tempo": 85,
  "key": "A minor",
  "instruments": ["piano", "drums", "bass", "vocals"],
  "description": "A slow, soulful R&B track with piano-driven melody",
  "trace_id": "4e94aba5a2de4cc4bff54a2813c8d36c"
}
```

---

### POST /v1/song/stem

Extract individual stems (vocals, drums, bass, etc.) from a song.

**Request** (multipart/form-data)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| file | file | Yes | Audio file to separate (mp3, wav, m4a, flac) |

**Response**

| Field | Type | Description |
|-------|------|-------------|
| id | string | Task ID |
| status | string | Task status: `preparing`, `processing`, `succeeded`, `failed` |
| stems | object | Separated stem tracks (available when status is `succeeded`) |
| stems.vocals | string | URL to vocals stem |
| stems.drums | string | URL to drums stem |
| stems.bass | string | URL to bass stem |
| stems.other | string | URL to other instruments stem |
| trace_id | string | Trace ID for troubleshooting |

**Response Example**
```json
{
  "id": "stem_task_123",
  "status": "succeeded",
  "stems": {
    "vocals": "https://cdn.mureka.ai/stems/abc123_vocals.mp3",
    "drums": "https://cdn.mureka.ai/stems/abc123_drums.mp3",
    "bass": "https://cdn.mureka.ai/stems/abc123_bass.mp3",
    "other": "https://cdn.mureka.ai/stems/abc123_other.mp3"
  },
  "trace_id": "5e94aba5a2de4cc4bff54a2813c8d36c"
}
```

---

## Lyrics APIs

### POST /v1/lyrics/generate

Generate lyrics from a prompt.

**Request**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| prompt | string | Yes | Description of the lyrics to generate |
| style | string | No | Lyrics style (e.g., "pop", "rock", "ballad") |
| language | string | No | Language code (e.g., "en", "zh", "ja") |

**Request Example**
```json
{
  "prompt": "A heartfelt ballad about traveling the world and finding home",
  "style": "ballad",
  "language": "en"
}
```

**Response**

| Field | Type | Description |
|-------|------|-------------|
| title | string | Generated song title |
| lyrics | string | Generated lyrics with section markers |
| sections | array | Structured sections |
| trace_id | string | Trace ID for troubleshooting |

**sections[]**

| Field | Type | Description |
|-------|------|-------------|
| type | string | Section type: `intro`, `verse`, `pre_chorus`, `chorus`, `bridge`, `outro` |
| content | string | Section lyrics text |

**Response Example**
```json
{
  "title": "Roads to Home",
  "lyrics": "[Verse 1]\nTraveling alone on winding roads\nFinding beauty in the heavy loads\n[Pre-Chorus]\nBut home is where the heart belongs\n[ Chorus]\nI'll find my way back someday",
  "sections": [
    {"type": "verse", "content": "Traveling alone on winding roads..."},
    {"type": "pre_chorus", "content": "But home is where the heart belongs..."},
    {"type": "chorus", "content": "I'll find my way back someday..."}
  ],
  "trace_id": "6e94aba5a2de4cc4bff54a2813c8d36c"
}
```

---

### POST /v1/lyrics/extend

Extend existing lyrics with additional sections.

**Request**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| lyrics | string | Yes | Original lyrics content |
| prompt | string | Yes | Instructions for extension (e.g., "add a bridge and outro") |
| model | string | No | Model version: `auto`, `mureka-7.5`, `mureka-7.6`, `mureka-o2`, `mureka-8` |

**Request Example**
```json
{
  "lyrics": "[Verse]\nOriginal lyrics here...\n[Chorus]\nMain chorus here...",
  "prompt": "Add a bridge after the second verse and extend the outro",
  "model": "mureka-8"
}
```

**Response**

| Field | Type | Description |
|-------|------|-------------|
| title | string | Song title (may be updated) |
| lyrics | string | Extended lyrics with new sections added |
| sections | array | Structured sections |
| trace_id | string | Trace ID for troubleshooting |

**Response Example**
```json
{
  "title": "Extended Song Title",
  "lyrics": "[Verse]\nOriginal lyrics here...\n[Bridge]\nNew bridge content...\n[Outro]\nFading out...",
  "sections": [
    {"type": "verse", "content": "Original lyrics here..."},
    {"type": "bridge", "content": "New bridge content..."},
    {"type": "outro", "content": "Fading out..."}
  ],
  "trace_id": "7e94aba5a2de4cc4bff54a2813c8d36c"
}
```

---

## Instrumental APIs

### POST /v1/instrumental/generate

Generate instrumental music.

**Request**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| prompt | string | Yes | Musical style description (genre, mood, instruments) |
| duration | integer | No | Duration in seconds (default: 180, max: 600) |
| model | string | No | Model version: `auto`, `mureka-7.5`, `mureka-7.6`, `mureka-o2`, `mureka-8` |

**Request Example**
```json
{
  "prompt": "upbeat pop instrumental, summer vibes, tropical house",
  "duration": 180
}
```

**Response**

| Field | Type | Description |
|-------|------|-------------|
| id | string | Task ID for polling status |
| status | string | Task status: `preparing`, `processing`, `succeeded`, `failed` |
| trace_id | string | Trace ID for troubleshooting |

**Response Example**
```json
{
  "id": "inst_task_456",
  "status": "preparing",
  "trace_id": "8e94aba5a2de4cc4bff54a2813c8d36c"
}
```

---

### GET /v1/instrumental/query/{task_id}

Poll task status for instrumental generation.

**Path Parameters**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| task_id | string | Yes | Task ID from `/v1/instrumental/generate` response |

**Response**

| Field | Type | Description |
|-------|------|-------------|
| id | string | Task ID |
| created_at | integer | Unix timestamp of task creation |
| finished_at | integer | Unix timestamp when task completed (0 if not finished) |
| status | string | Task status: `preparing`, `running`, `succeeded`, `failed` |
| failed_reason | string | Error message if status is `failed` |
| trace_id | string | Trace ID for troubleshooting |
| choices | array | Generated instrumental versions |

**choices[]**

| Field | Type | Description |
|-------|------|-------------|
| index | integer | Version index (0-based) |
| id | string | Instrumental ID |
| url | string | Full instrumental audio URL |
| flac_url | string | FLAC format URL |
| wav_url | string | WAV format URL |
| duration | integer | Duration in seconds |

**Response Example**
```json
{
  "id": "inst_task_456",
  "created_at": 1677610602,
  "finished_at": 1677611200,
  "status": "succeeded",
  "trace_id": "8e94aba5a2de4cc4bff54a2813c8d36c",
  "choices": [
    {
      "index": 0,
      "id": "inst_abc123",
      "url": "https://cdn.mureka.ai/instrumentals/abc123.mp3",
      "flac_url": "https://cdn.mureka.ai/instrumentals/abc123.flac",
      "wav_url": "https://cdn.mureka.ai/instrumentals/abc123.wav",
      "duration": 180
    }
  ]
}
```

---

## Vocal API

### POST /v1/vocal/clone

Upload a vocal sample to create a reusable Vocal ID.

**Request** (multipart/form-data)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| file | file | Yes | Vocal sample audio file |
| name | string | No | Custom name for the vocal clone |

**Request Example**
```bash
curl -X POST https://api.mureka.ai/v1/vocal/clone \
  -H "Authorization: Bearer $MUREKA_API_KEY" \
  -F "file=@vocal_sample.mp3" \
  -F "name=My Custom Vocal"
```

**Response**

| Field | Type | Description |
|-------|------|-------------|
| id | string | Vocal ID (use in song generation) |
| name | string | Vocal clone name |
| created_at | integer | Unix timestamp of creation |
| duration | integer | Duration of vocal sample in seconds |
| trace_id | string | Trace ID for troubleshooting |

**Response Example**
```json
{
  "id": "vocal_xyz789",
  "name": "My Custom Vocal",
  "created_at": 1677610602,
  "duration": 30,
  "trace_id": "9e94aba5a2de4cc4bff54a2813c8d36c"
}
```

**Usage in Song Generation**

Use the returned `vocal_id` in `/v1/song/generate` request:

```json
{
  "lyrics": "[Verse]\nLyrics here...",
  "prompt": "pop, upbeat",
  "vocal_id": "vocal_xyz789"
}
```

---

## TTS APIs

### POST /v1/tts/generate

Generate audio from text (text-to-speech).

**Request**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| text | string | Yes | Text to convert to speech |
| voice | string | No | Voice name. Valid values: `Ethan`, `Victoria`, `Jake`, `Luna`, `Emma` (default: `Victoria`) |
| speed | float | No | Speech speed (0.5 - 2.0, default: 1.0) |
| model | string | No | TTS model version |

**Request Example**
```json
{
  "text": "Welcome to the future of music creation",
  "voice": "default",
  "speed": 1.0
}
```

**Response**

| Field | Type | Description |
|-------|------|-------------|
| id | string | Task ID (if async) or audio URL |
| status | string | Status: `completed`, `processing` |
| url | string | Audio URL (when status is `completed`) |
| format | string | Audio format: `mp3`, `wav`, `flac` |
| duration | integer | Duration in seconds |
| trace_id | string | Trace ID for troubleshooting |

**Response Example**
```json
{
  "id": "tts_task_789",
  "status": "completed",
  "url": "https://cdn.mureka.ai/tts/abc123.mp3",
  "format": "mp3",
  "duration": 5,
  "trace_id": "ae94aba5a2de4cc4bff54a2813c8d36c"
}
```

---

### POST /v1/tts/podcast

Create podcast-style audio content with multiple speakers.

**Request**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| conversations | array | Yes | Conversation array (max 10 items) |
| background | string | No | Background music description |
| speed | float | No | Speech speed (0.5 - 2.0, default: 1.0) |

**conversations[]**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| text | string | Yes | Text of the conversation (max 400 characters) |
| voice | string | Yes | Voice name: `Ethan`, `Victoria`, `Jake`, `Luna`, `Emma` |

**Request Example**
```bash
curl https://api.mureka.ai/v1/tts/podcast \
  -H "Authorization: Bearer $MUREKA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "conversations": [
      {"text": "Hello, my name is Luna.", "voice": "Luna"},
      {"text": "Hello, my name is Jack.", "voice": "Jake"},
      {"text": "Prior study has shown that there would exist some variations.", "voice": "Luna"},
      {"text": "The integration of vision and speech in MLLMs is not straightforward.", "voice": "Jake"}
    ]
  }'
```

**Response**

| Field | Type | Description |
|-------|------|-------------|
| id | string | Task ID |
| status | string | Status: `completed`, `processing` |
| url | string | Audio URL (when status is `completed`) |
| format | string | Audio format |
| duration | integer | Duration in seconds |
| transcript | string | Full transcript of the podcast |
| trace_id | string | Trace ID for troubleshooting |

**Response Example**
```json
{
  "id": "podcast_task_101",
  "status": "completed",
  "url": "https://cdn.mureka.ai/podcasts/abc123.mp3",
  "format": "mp3",
  "duration": 300,
  "transcript": "Luna: Hello, my name is Luna...\nJake: Hello, my name is Jack...",
  "trace_id": "be94aba5a2de4cc4bff54a2813c8d36c"
}
```

---

## File APIs

### POST /v1/files/upload

Upload files for use with other API endpoints.

**Request** (multipart/form-data)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| file | file | Yes | File to upload |
| purpose | string | Yes | Intended purpose of the uploaded file |

**purpose valid values**

| Value | Supported Formats | Audio Duration | Description |
|-------|-------------------|----------------|-------------|
| reference | mp3, m4a | 30 seconds (trimmed if longer) | Reference audio |
| vocal | mp3, m4a | 15-30 seconds (trimmed if longer) | Vocal extracted from audio |
| melody | mp3, m4a, mid | 5-60 seconds (trimmed if longer) | Melody/music reference (MIDI recommended) |
| instrumental | mp3, m4a | 30 seconds (trimmed if longer) | Instrumental audio |
| voice | mp3, m4a | 5-15 seconds (trimmed if longer) | Voice sample |
| audio | mp3, m4a | - | Common audio file for song extension etc. |

**Request Example**
```bash
curl -X POST https://api.mureka.ai/v1/files/upload \
  -H "Authorization: Bearer $MUREKA_API_KEY" \
  -F "file=@vocal_sample.mp3" \
  -F "purpose=vocal"
```

**Response**

| Field | Type | Description |
|-------|------|-------------|
| id | string | File ID for referencing in other APIs |
| filename | string | Original filename |
| size | integer | File size in bytes |
| type | string | File MIME type |
| url | string | URL to access the uploaded file |
| purpose | string | Uploaded file purpose |
| duration | integer | Audio duration in seconds (if applicable) |
| created_at | integer | Unix timestamp of upload |
| trace_id | string | Trace ID for troubleshooting |

**Response Example**
```json
{
  "id": "file_abc123",
  "filename": "vocal_sample.mp3",
  "size": 524288,
  "type": "audio/mpeg",
  "url": "https://cdn.mureka.ai/files/abc123.mp3",
  "purpose": "vocal",
  "duration": 25,
  "created_at": 1677610602,
  "trace_id": "ce94aba5a2de4cc4bff54a2813c8d36c"
}
```

---

## Account API

### GET /v1/account/billing

Query account billing information and usage.

**Response**

| Field | Type | Description |
|-------|------|-------------|
| balance | float | Remaining credits/balance |
| currency | string | Currency code (e.g., "USD") |
| plan | object | Subscription plan details |
| plan.name | string | Plan name |
| plan.quota | integer | Monthly quota |
| plan.used | integer | Quota used this period |
| usage | array | API usage breakdown |
| trace_id | string | Trace ID for troubleshooting |

**usage[]**

| Field | Type | Description |
|-------|------|-------------|
| endpoint | string | API endpoint name |
| count | integer | Number of calls |
| quota | integer | Quota limit |

**Response Example**
```json
{
  "balance": 150.50,
  "currency": "USD",
  "plan": {
    "name": "Pro",
    "quota": 1000,
    "used": 250
  },
  "usage": [
    {"endpoint": "/v1/song/generate", "count": 100, "quota": 500},
    {"endpoint": "/v1/instrumental/generate", "count": 50, "quota": 200}
  ],
  "trace_id": "de94aba5a2de4cc4bff54a2813c8d36c"
}
```

---

## Common Structures

### Error Response

All endpoints may return error responses.

| Field | Type | Description |
|-------|------|-------------|
| error | object | Error details |
| error.message | string | Error description |
| error.code | string | Error code (if available) |
| trace_id | string | Trace ID for troubleshooting |

**Error Response Example**
```json
{
  "error": {
    "message": "Invalid Authentication"
  },
  "trace_id": "ee94aba5a2de4cc4bff54a2813c8d36c"
}
```

### Task Status Values

| Status | Description |
|--------|-------------|
| preparing | Task created, initializing |
| running | Task in progress |
| processing | Processing audio/data |
| succeeded | Task completed successfully |
| failed | Task failed (check `failed_reason`) |

### Model Versions

| Model | Description |
|-------|-------------|
| auto | Automatically select best model |
| mureka-7.5 | Enhanced melody and arrangement, realistic vocals, supports streaming |
| mureka-7.6 | Improved vocals and arrangement over 7.5 |
| mureka-o2 | Intelligent algorithm for superior quality, multilingual, contextual BGM |
| mureka-8 | Latest model with highest quality output |

---

## Example curl Commands

**Generate Song**
```bash
curl -X POST https://api.mureka.ai/v1/song/generate \
  -H "Authorization: Bearer $MUREKA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "lyrics": "[Verse]\nIn the stormy night, I wander alone\n[Chorus]\nI will find my way home",
    "model": "auto",
    "prompt": "r&b, slow, passionate, male vocal"
  }'
```

**Query Task Status**
```bash
curl https://api.mureka.ai/v1/song/query/1436211 \
  -H "Authorization: Bearer $MUREKA_API_KEY"
```

**Generate Instrumental**
```bash
curl -X POST https://api.mureka.ai/v1/instrumental/generate \
  -H "Authorization: Bearer $MUREKA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "upbeat pop instrumental, summer vibes",
    "duration": 180
  }'
```

**Clone Vocal**
```bash
curl -X POST https://api.mureka.ai/v1/vocal/clone \
  -H "Authorization: Bearer $MUREKA_API_KEY" \
  -F "file=@vocal_sample.mp3"
```

**Generate Lyrics**
```bash
curl -X POST https://api.mureka.ai/v1/lyrics/generate \
  -H "Authorization: Bearer $MUREKA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A heartfelt ballad about traveling the world"
  }'
```

**Text-to-Speech**
```bash
curl -X POST https://api.mureka.ai/v1/tts/generate \
  -H "Authorization: Bearer $MUREKA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Welcome to the future of music creation",
    "voice": "Victoria"
  }'
```

**Podcast**
```bash
curl https://api.mureka.ai/v1/tts/podcast \
  -H "Authorization: Bearer $MUREKA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "conversations": [
      {"text": "Hello, my name is Luna.", "voice": "Luna"},
      {"text": "Hello, my name is Jack.", "voice": "Jake"}
    ]
  }'
```

**Separate Audio Stems**
```bash
curl -X POST https://api.mureka.ai/v1/song/stem \
  -H "Authorization: Bearer $MUREKA_API_KEY" \
  -F "file=@song.mp3"
```

**Check Billing**
```bash
curl https://api.mureka.ai/v1/account/billing \
  -H "Authorization: Bearer $MUREKA_API_KEY"
```
