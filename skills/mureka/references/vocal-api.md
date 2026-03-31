# Vocal Cloning API

## POST /v1/vocal/clone

Upload a vocal sample to create a reusable Vocal ID.

### Authorization
BearerAuth - Type: HTTP (bearer)

### Content-Type
multipart/form-data (NOT JSON)

### Request Body (Form Data)
- `file` (file, required): Vocal sample file
  - Supported formats: mp3, m4a
  - File size must be less than 10 MB

### Example
```bash
curl -X POST https://api.mureka.ai/v1/vocal/clone \
  -H "Authorization: Bearer $MUREKA_API_KEY" \
  -F "file=@vocal_sample.mp3"
```

### Response (200)
The created vocal clone resource with `vocal_id`.

```json
{
  "id": "vocal_id",
  "name": "My Vocal",
  "created_at": 1677610602
}
```

## Usage in Song Generation

After cloning, use the returned `vocal_id` in song generation requests to use that vocal style.
