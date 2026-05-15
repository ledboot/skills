# MiniMax API Overview Reference

Official source:

- https://platform.minimaxi.com/docs/api-reference/api-overview
- https://platform.minimaxi.com/docs/llms.txt

MiniMax Open Platform provides multimodal APIs across:

- Text: Anthropic-compatible API, OpenAI-compatible API, text chat, text generation, prompt caching, model listing.
- Speech: synchronous text-to-audio over HTTP or WebSocket, asynchronous long text speech generation.
- Voice: voice cloning, voice design, voice management.
- Video: text-to-video, image-to-video, first/last-frame video, subject-reference video, video agent tasks, query, download.
- Image: text-to-image and image-to-image.
- Music: lyrics generation, music generation, music cover preprocessing.
- Files: upload, list, retrieve, download, delete.
- Models: list and retrieve model metadata for OpenAI-compatible and Anthropic-compatible surfaces.

Use `llms.txt` first when locating a current endpoint page or OpenAPI spec. The docs expose OpenAPI specs for several capabilities, including music, text, image, video, voice cloning uploads, and model listing.

General integration rules:

- Authenticate with `Authorization: Bearer $MINIMAX_API_KEY`.
- Confirm whether the key is pay-as-you-go API Key or Token Plan Key for the chosen API surface.
- Distinguish synchronous APIs from async task APIs. Async APIs usually return a task id that must be polled.
- For generated files, retrieve or download through File APIs when the result returns `file_id`.
- Watch for URL expiration windows on generated media outputs.
- Do not store real keys, file IDs, voice IDs, or generated URLs in durable memory unless the user explicitly asks and it is safe.
