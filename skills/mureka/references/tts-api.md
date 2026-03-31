# TTS API

## POST /v1/tts/generate

Generate audio from the input text.

### Authorization
BearerAuth - Type: HTTP (bearer)

### Request Body (JSON)
```json
{
  "text": "Welcome to the future of music creation",
  "voice": "Victoria"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| text | string | Yes | Text to convert to speech |
| voice | string | No | Voice name. Valid values: `Ethan`, `Victoria`, `Jake`, `Luna`, `Emma` (default: `Victoria`) |
| speed | float | No | Speech speed (0.5 - 2.0, default: 1.0) |
| model | string | No | TTS model version |

### Response (200)
The audio content.

## POST /v1/tts/podcast

Create podcast-style audio content with multiple speakers.

### Authorization
BearerAuth - Type: HTTP (bearer)

### Request Body (JSON)
```json
{
  "conversations": [
    {"text": "Hello, my name is Luna.", "voice": "Luna"},
    {"text": "Hello, my name is Jack.", "voice": "Jake"}
  ]
}
```

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

### Response (200)
The generated podcast audio.

### Example
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
