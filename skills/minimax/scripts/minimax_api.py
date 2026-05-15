#!/usr/bin/env python3
"""Generic MiniMax Open Platform JSON API caller."""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any, Dict, Optional


DEFAULT_BASE_URL = "https://api.minimaxi.com"


def read_body(args: argparse.Namespace) -> Optional[bytes]:
    if args.body and args.body_file:
        raise ValueError("use either --body or --body-file, not both")

    if args.body_file:
        with open(args.body_file, "rb") as file:
            return file.read()

    if args.body:
        return args.body.encode("utf-8")

    return None


def build_url(base_url: str, path_or_url: str) -> str:
    if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
        return path_or_url
    return base_url.rstrip("/") + "/" + path_or_url.lstrip("/")


def request_minimax(
    api_key: str,
    method: str,
    url: str,
    body: Optional[bytes],
    timeout: int,
    raw: bool,
) -> Any:
    headers: Dict[str, str] = {
        "Authorization": f"Bearer {api_key}",
    }

    if body is not None:
        headers["Content-Type"] = "application/json"

    request = urllib.request.Request(url, data=body, headers=headers, method=method.upper())

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            content_type = response.headers.get("Content-Type", "")
            response_body = response.read()
    except urllib.error.HTTPError as error:
        error_body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"MiniMax API HTTP {error.code}: {error_body}") from error
    except urllib.error.URLError as error:
        raise RuntimeError(f"MiniMax API request failed: {error}") from error

    if raw or "application/json" not in content_type:
        return response_body

    return json.loads(response_body.decode("utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Call MiniMax Open Platform API")
    parser.add_argument("--api-key", default=os.getenv("MINIMAX_API_KEY"), help="MiniMax API key")
    parser.add_argument("--base-url", default=os.getenv("MINIMAX_API_BASE", DEFAULT_BASE_URL))
    parser.add_argument("--method", default="GET", choices=("GET", "POST", "PUT", "PATCH", "DELETE"))
    parser.add_argument("--path", required=True, help="API path such as /v1/lyrics_generation, or full URL")
    parser.add_argument("--body", help="JSON request body string")
    parser.add_argument("--body-file", help="File containing JSON request body")
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--raw", action="store_true", help="Write raw response bytes")
    parser.add_argument("-o", "--output", help="Write response to file")
    args = parser.parse_args()

    if not args.api_key:
        parser.error("missing API key. Set MINIMAX_API_KEY or pass --api-key")

    try:
        body = read_body(args)
        if body is not None:
            json.loads(body.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        parser.error(str(error))

    result = request_minimax(
        api_key=args.api_key,
        method=args.method,
        url=build_url(args.base_url, args.path),
        body=body,
        timeout=args.timeout,
        raw=args.raw,
    )

    if isinstance(result, bytes):
        if args.output:
            with open(args.output, "wb") as file:
                file.write(result)
        else:
            sys.stdout.buffer.write(result)
        return 0

    output = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as file:
            file.write(output + "\n")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
