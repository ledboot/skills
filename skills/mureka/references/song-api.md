# Song Generation API

## POST /v1/song/generate

Generate song based on the input by the user.

### Authorization
BearerAuth - Type: HTTP (bearer)

### Request Body (JSON)
- `lyrics` (string, required): Song lyrics with section markers
- `model` (string, optional): Model version - "auto", "mureka-7.5", "mureka-7.6", "mureka-o2", "mureka-8"
- `prompt` (string, optional): Musical style description
- `n` (integer, optional): Defaults to 2, maximum 3. How many songs to generate for each request. Note that you will be charged based on the number of songs.
- `reference_id` (string, optional): Control music generation by referencing music, generated through the files/upload API (for reference purpose). Besides individual control, it also supports combination with other options: reference_id + vocal_id.
- `vocal_id` (string, optional): Control music generation by any voice you like, generated through the files/upload API (for vocal purpose). Besides individual control, it also supports combination with other options: vocal_id + reference_id, vocal_id + prompt.
- `melody_id` (string, optional): Control music generation by melody idea, generated through the files/upload API (for melody purpose). Besides individual control, this option does not support combination with other control options.
- `stream` (boolean, optional): If set to true, the status of the generation task will include a streaming phase. During this phase, you can obtain the stream_url of the generated song and play this URL, enabling playback while the generation is in progress. When the model is mureka-o1, this mode is not supported.

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
