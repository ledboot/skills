# Song Processing APIs

## POST /v1/song/recognize

Identify a song from audio.

### Authorization
BearerAuth

### Content-Type
multipart/form-data

### Request Body (Form Data)
- `file` (file, required): Audio file to identify

### Response (200)
Recognized song information.

## POST /v1/song/describe

Analyze and describe a song's characteristics.

### Authorization
BearerAuth

### Content-Type
multipart/form-data

### Request Body (Form Data)
- `file` (file, required): Audio file to analyze

### Response (200)
Description of song's genre, mood, instruments, tempo, etc.

## POST /v1/song/stem

Extract individual stems (vocals, drums, bass, etc.) from a song.

### Authorization
BearerAuth

### Content-Type
multipart/form-data

### Request Body (Form Data)
- `file` (file, required): Audio file to separate

### Response (200)
Returns separated stem tracks:
- vocals
- drums
- bass
- other instruments

## POST /v1/files/upload

Upload files for use with other API endpoints.

### Authorization
BearerAuth

### Content-Type
multipart/form-data

### Request Body (Form Data)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| file | file | Yes | File to upload |
| purpose | string | Yes | Intended purpose: `reference`, `vocal`, `melody`, `instrumental`, `voice`, `audio` |

**purpose formats and durations:**

| purpose | Formats | Duration |
|---------|---------|----------|
| reference | mp3, m4a | 30s (trimmed) |
| vocal | mp3, m4a | 15-30s (trimmed) |
| melody | mp3, m4a, mid | 5-60s (trimmed) |
| instrumental | mp3, m4a | 30s (trimmed) |
| voice | mp3, m4a | 5-15s (trimmed) |
| audio | mp3, m4a | - |

### Response (200)
Upload confirmation with file ID, URL, and metadata.
