# Song Generation API

## POST /v1/song/generate

Generate song based on the input by the user.

### Authorization
BearerAuth - Type: HTTP (bearer)

### Request Body (JSON)
- `lyrics` (string, required): Song lyrics with section markers
- `model` (string, optional): Model version - "auto", "mureka-7.5", "mureka-7.6", "mureka-o2", "mureka-8"
- `prompt` (string, required): Musical style description

### Response (200)
Asynchronous task information for generating songs.
Use `/v1/song/query/{task_id}` API to poll for task information.

```json
{
  "id": "1436211",
  "created_at": 1677610602,
  "model": "mureka-8",
  "status": "preparing",
  "trace_id": "1e94aba5a2de4cc4bff54a2813c8d36c"
}
```

## GET /v1/song/query/{task_id}

Query task status for song generation.

### Response
Returns current status of the task: `preparing`, `processing`, `completed`, `failed`

## POST /v1/song/extend

Extend the song based on the input lyrics.

### Authorization
BearerAuth

### Request Body (JSON)
- `lyrics` (string, required): Original song lyrics
- `prompt` (string, required): Instructions for extension
- `model` (string, optional): Model version

### Response (200)
Asynchronous task information. Use `/v1/song/query/{task_id}` to poll.
