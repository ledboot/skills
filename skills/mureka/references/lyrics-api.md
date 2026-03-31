# Lyrics API

## POST /v1/lyrics/generate

Generate lyrics from a prompt.

### Authorization
BearerAuth - Type: HTTP (bearer)

### Request Body (JSON)
```json
{
  "prompt": "A heartfelt ballad about traveling the world and finding home"
}
```

### Response (200)
The generated title and lyrics.

## POST /v1/lyrics/extend

Extend existing lyrics with more sections.

### Authorization
BearerAuth

### Request Body (JSON)
```json
{
  "lyrics": "Existing lyrics content...",
  "prompt": "Add a bridge and outro"
}
```

### Response (200)
The extended lyrics with additional sections.
