"""Small Gemini adapter used by the two model-backed FitFindr tools."""
from __future__ import annotations
import hashlib
import json
import os
import time
from pathlib import Path

import config

_calls = 0
_tokens_in = 0
_tokens_out = 0

class ModelUnavailable(RuntimeError):
    """Raised when the hosted model cannot be used."""


def _cache_path(prompt: str, system: str) -> Path:
    digest = hashlib.sha256((system + "\n" + prompt).encode("utf-8")).hexdigest()
    return config.CACHE_DIR / f"{digest}.json"


def generate(prompt: str, system: str = "", cache: bool | None = None) -> str:
    global _calls, _tokens_in, _tokens_out
    use_cache = config.CACHE_ENABLED if cache is None else cache
    path = _cache_path(prompt, system)
    if use_cache and path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))["text"]
        except Exception:
            pass

    key = os.getenv("GEMINI_API_KEY", "").strip()
    if not key or key == "your_key_here":
        raise ModelUnavailable(
            "No GEMINI_API_KEY found. Copy .env.example to .env and paste your Gemini key."
        )

    try:
        from google import genai
        from google.genai import types
    except Exception as exc:
        raise ModelUnavailable(
            "google-genai is not installed. Run: pip install -r requirements.txt"
        ) from exc

    client = genai.Client(api_key=key)
    last = None
    for attempt in range(config.MAX_RETRIES):
        try:
            response = client.models.generate_content(
                model=config.MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=config.TEMPERATURE,
                    system_instruction=system or None,
                ),
            )
            text = (response.text or "").strip()
            if not text:
                raise ModelUnavailable("The model returned an empty response.")
            _calls += 1
            usage = getattr(response, "usage_metadata", None)
            _tokens_in += int(getattr(usage, "prompt_token_count", 0) or 0)
            _tokens_out += int(getattr(usage, "candidates_token_count", 0) or 0)
            if use_cache:
                config.CACHE_DIR.mkdir(exist_ok=True)
                path.write_text(json.dumps({"text": text}), encoding="utf-8")
            return text
        except Exception as exc:
            last = exc
            message = str(exc).lower()
            if "429" not in message and "resource_exhausted" not in message and "rate" not in message:
                raise ModelUnavailable(str(exc)) from exc
            if attempt < config.MAX_RETRIES - 1:
                wait = min(2 ** attempt, 16)
                print(f"[rate limit] retrying in {wait}s...", flush=True)
                time.sleep(wait)
    raise ModelUnavailable(f"Model still unavailable after retries: {last}")


def usage() -> str:
    return f"{_calls} model calls this session, {_tokens_in + _tokens_out} tokens ({_tokens_in} in, {_tokens_out} out)"
