"""Data loading helpers for FitFindr."""
import json
from pathlib import Path
_DATA_DIR = Path(__file__).resolve().parent.parent / "data"

def load_listings() -> list[dict]:
    return json.loads((_DATA_DIR / "listings.json").read_text(encoding="utf-8"))

def load_wardrobe_schema() -> dict:
    return json.loads((_DATA_DIR / "wardrobe_schema.json").read_text(encoding="utf-8"))

def _wardrobe(name: str) -> dict:
    value = load_wardrobe_schema()[name]
    return {k:v for k,v in value.items() if not k.startswith("_")}

def get_example_wardrobe() -> dict:
    return _wardrobe("example_wardrobe")

def get_empty_wardrobe() -> dict:
    return _wardrobe("empty_wardrobe")
