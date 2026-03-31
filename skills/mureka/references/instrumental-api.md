# Instrumental API

## POST /v1/instrumental/generate

Generate instrumental based on the input by the user.

### Authorization
BearerAuth - Type: HTTP (bearer)

### Request Body (JSON)
```json
{
  "prompt": "upbeat pop instrumental, summer vibes",
  "duration": 180
}
```

- `prompt` (string, required): Musical style description
- `duration` (integer, optional): Duration in seconds

### Response (200)
Asynchronous task information. Use `/v1/instrumental/query/{task_id}` API to poll.

```json
{
  "id": "task_id",
  "status": "preparing",
  "trace_id": "..."
}
```

## GET /v1/instrumental/query/{task_id}

Query task status for instrumental generation.

### Authorization
BearerAuth

### Response
Returns current status: `preparing`, `processing`, `completed`, `failed`
