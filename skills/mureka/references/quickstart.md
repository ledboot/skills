# Quickstart Guide

## Set Up an Account
Sign up at https://platform.mureka.ai/

## Create an API Key
After registration, navigate to "API Keys" tab in dashboard to view and manage API keys.

**Important**: API key is secret. Do not share or expose in client-side code.

## Servers
```
https://api.mureka.ai
```

## Authentication
Use API key in Authorization header:
```
Authorization: Bearer MUREKA_API_KEY
```

### Set API Key as Environment Variable
```bash
export MUREKA_API_KEY="your_api_key_here"
```

Or add to `.env` file:
```
MUREKA_API_KEY=your_api_key_here
```

### Verify API Key
Test if your API key is valid by querying a task:
```bash
curl https://api.mureka.ai/v1/song/query/435134 \
  -H "Authorization: Bearer $MUREKA_API_KEY"
```

**Valid key** returns task info or status.
**Invalid key** returns:
```json
{"error":{"message":"Invalid Authentication"}}
```

## Example Request
```bash
curl https://api.mureka.ai/v1/song/generate \
  -H "Authorization: Bearer $MUREKA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "lyrics": "[Verse]\nIn the stormy night, I wander alone\nLost in the rain, feeling like I have been thrown",
    "model": "auto",
    "prompt": "r&b, slow, passionate, male vocal"
  }'
```

## Response
```json
{
  "id": "1436211",
  "created_at": 1677610602,
  "model": "mureka-8",
  "status": "preparing",
  "trace_id": "1e94aba5a2de4cc4bff54a2813c8d36c"
}
```

## Error Response
```json
{
  "error": {
    "message": "Invalid Authentication"
  },
  "trace_id": "1e94aba5a2de4cc4bff54a2813c8d36c"
}
```

## Troubleshooting
- Inspect `trace_id` for tracking requests
- Log `trace_id` in production for support troubleshooting
