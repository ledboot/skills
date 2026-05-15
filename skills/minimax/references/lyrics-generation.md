# Lyrics Generation Reference

Official source:

- https://platform.minimaxi.com/docs/api-reference/lyrics-generation

Endpoint:

```text
POST https://api.minimaxi.com/v1/lyrics_generation
```

Authentication:

```text
Authorization: Bearer $MINIMAX_API_KEY
Content-Type: application/json
```

Common request fields:

- `mode`: `write_full_song` or `edit`
- `prompt`: theme, style, language, emotion, or edit instruction
- `lyrics`: existing lyrics when editing or extending
- `title`: title to preserve or guide

Use the bundled helper:

```bash
python scripts/lyrics_generation.py --prompt "一首关于夏日海边的轻快情歌"
```

For full JSON output:

```bash
python scripts/lyrics_generation.py --prompt "..." --json
```

For edit mode:

```bash
python scripts/lyrics_generation.py \
  --mode edit \
  --lyrics-file old_lyrics.txt \
  --prompt "续写第二段和副歌"
```

Expected response fields include generated lyrics and may include title, style tags, and `base_resp`. Always inspect the current official docs for exact response shape before writing downstream parsers.
