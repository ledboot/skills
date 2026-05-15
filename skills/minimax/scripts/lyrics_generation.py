#!/usr/bin/env python3
"""
Call MiniMax Lyrics Generation API.

Docs: https://platform.minimaxi.com/docs/api-reference/lyrics-generation
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any, Dict, Optional


API_PATH = "/v1/lyrics_generation"
DEFAULT_BASE_URL = "https://api.minimaxi.com"


def read_text_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def generate_lyrics(
    api_key: str,
    prompt: str = "",
    mode: str = "write_full_song",
    lyrics: Optional[str] = None,
    title: Optional[str] = None,
    base_url: str = DEFAULT_BASE_URL,
    timeout: int = 120,
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "mode": mode,
        "prompt": prompt,
    }

    if lyrics:
        payload["lyrics"] = lyrics

    if title:
        payload["title"] = title

    request = urllib.request.Request(
        base_url.rstrip("/") + API_PATH,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            response_body = response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        error_body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"MiniMax API HTTP {error.code}: {error_body}") from error
    except urllib.error.URLError as error:
        raise RuntimeError(f"MiniMax API request failed: {error}") from error

    result = json.loads(response_body)
    base_resp = result.get("base_resp") or {}

    if base_resp.get("status_code") not in (None, 0):
        status_code = base_resp.get("status_code")
        status_msg = base_resp.get("status_msg", "")
        raise RuntimeError(f"MiniMax API error {status_code}: {status_msg}")

    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate lyrics with MiniMax Lyrics Generation API")
    parser.add_argument("--api-key", default=os.getenv("MINIMAX_API_KEY"), help="MiniMax API key")
    parser.add_argument("--base-url", default=os.getenv("MINIMAX_API_BASE", DEFAULT_BASE_URL))
    parser.add_argument(
        "--mode",
        choices=("write_full_song", "edit"),
        default="write_full_song",
        help="Generation mode",
    )
    parser.add_argument("--prompt", default="", help="Song theme, style, or edit instruction")
    parser.add_argument("--lyrics", help="Existing lyrics text, only used with --mode edit")
    parser.add_argument("--lyrics-file", help="Read existing lyrics from file, only used with --mode edit")
    parser.add_argument("--title", help="Song title. If provided, API keeps the title unchanged")
    parser.add_argument("--timeout", type=int, default=120, help="Request timeout in seconds")
    parser.add_argument("--json", action="store_true", help="Print full JSON response")
    parser.add_argument("-o", "--output", help="Write generated lyrics to a file")
    args = parser.parse_args()

    if not args.api_key:
        parser.error("missing API key. Set MINIMAX_API_KEY or pass --api-key")

    lyrics = args.lyrics
    if args.lyrics_file:
        lyrics = read_text_file(args.lyrics_file)

    if args.mode == "edit" and not lyrics:
        parser.error("--mode edit requires --lyrics or --lyrics-file")

    result = generate_lyrics(
        api_key=args.api_key,
        prompt=args.prompt,
        mode=args.mode,
        lyrics=lyrics,
        title=args.title,
        base_url=args.base_url,
        timeout=args.timeout,
    )

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    song_title = result.get("song_title", "")
    style_tags = result.get("style_tags", "")
    generated_lyrics = result.get("lyrics", "")

    output_text = "\n".join(
        line
        for line in (
            f"Title: {song_title}" if song_title else "",
            f"Style: {style_tags}" if style_tags else "",
            "",
            generated_lyrics,
        )
        if line
    )

    if args.output:
        with open(args.output, "w", encoding="utf-8") as file:
            file.write(generated_lyrics)
        print(f"Lyrics saved to: {args.output}")
    else:
        print(output_text)

    return 0


if __name__ == "__main__":
    sys.exit(main())
