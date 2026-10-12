"""Settings for FitFindr."""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).parent
load_dotenv(ROOT / ".env")

if sys.platform == "win32":
    for _stream in (sys.stdout, sys.stderr):
        try:
            _stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass

TEMPERATURE = 0.9
CACHE_ENABLED = os.getenv("AI201_CACHE", "1") != "0"
MAX_ITERATIONS = 10
SEARCH_RESULT_LIMIT = 10
MODEL = os.getenv("AI201_MODEL", "gemini-3.5-flash-lite")
REQUESTS_PER_MINUTE = 15
SESSION_REQUEST_BUDGET = 300
MAX_RETRIES = 5
CACHE_DIR = ROOT / ".cache"
DATA_DIR = ROOT / "data"
RESULTS_DIR = ROOT / "results"
