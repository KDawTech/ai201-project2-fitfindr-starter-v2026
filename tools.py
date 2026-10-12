"""The three FitFindr tools required by Unit 3."""
from __future__ import annotations
import re
import config
from generate import generate
from utils.data_loader import load_listings

_STOPWORDS = {
    "a","an","the","for","and","or","of","to","in","on","with","looking","want","find","me",
    "size","under","below","less","than","please","something","item"
}

def _tokens(text: str) -> set[str]:
    return {t for t in re.findall(r"[a-z0-9]+", text.lower()) if len(t) > 1 and t not in _STOPWORDS}

def _size_match(requested: str | None, listing_size: str) -> bool:
    if not requested: return True
    req = requested.strip().lower()
    if not req: return True
    parts = re.findall(r"[a-z]+|\d+", listing_size.lower())
    # clothing letters: M matches M and S/M or M/L, but not XL
    if req in {"xxs","xs","s","m","l","xl","xxl","xxxl"}:
        return req in parts
    # numeric shoe/waist size: require exact numeric token
    if req.isdigit():
        return req in parts
    return req == listing_size.strip().lower()

def search_listings(description: str, size: str | None = None, max_price: float | None = None) -> list[dict]:
    """Return matching listing dicts, best keyword match first; [] when none match."""
    query = _tokens(description)
    ranked = []
    for listing in load_listings():
        if max_price is not None and float(listing["price"]) > float(max_price):
            continue
        if not _size_match(size, str(listing["size"])):
            continue
        haystack = " ".join([
            listing["title"], listing["description"], listing["category"],
            " ".join(listing.get("style_tags", [])), " ".join(listing.get("colors", [])),
            listing.get("brand") or "", listing.get("platform") or ""
        ])
        words = _tokens(haystack)
        overlap = query & words
        if not overlap:
            continue
        title_words = _tokens(listing["title"])
        score = len(overlap) + 1.5 * len(query & title_words)
        # a full phrase appearing in title/description is a strong signal
        phrase = description.strip().lower()
        if phrase and phrase in haystack.lower():
            score += 4
        ranked.append((score, -float(listing["price"]), listing))
    ranked.sort(key=lambda x: (x[0], x[1]), reverse=True)
    return [item for _, _, item in ranked[: config.SEARCH_RESULT_LIMIT]]

def _item_summary(item: dict) -> str:
    return (
        f"{item.get('title')} | ${item.get('price')} | size {item.get('size')} | "
        f"colors {', '.join(item.get('colors', []))} | style {', '.join(item.get('style_tags', []))}"
    )

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    """Return a non-empty outfit suggestion; empty wardrobe gets general styling advice."""
    if not new_item:
        return "I need a selected item before I can suggest an outfit."
    items = wardrobe.get("items", []) if isinstance(wardrobe, dict) else []
    if not items:
        prompt = f"""You are a concise thrift stylist. The user is considering:
{_item_summary(new_item)}
Their saved wardrobe is empty. Give 2 practical general outfit ideas using common basics they might own or buy. Keep it under 90 words."""
    else:
        formatted = "\n".join(
            f"- {x.get('name')} ({x.get('category')}): colors {', '.join(x.get('colors', []))}; style {', '.join(x.get('style_tags', []))}"
            for x in items
        )
        prompt = f"""You are a concise thrift stylist. Build 1-2 wearable outfits around this new item:
{_item_summary(new_item)}
Use pieces from this wardrobe by name when useful:
{formatted}
Keep it under 100 words and make the combinations specific."""
    return generate(prompt, system="Give practical, specific styling advice. Do not invent wardrobe pieces when a wardrobe is provided.")

def create_fit_card(outfit: str, new_item: dict) -> str:
    """Return a 2-4 sentence social caption; guard against missing outfit text."""
    if not outfit or not outfit.strip():
        return "I need an outfit suggestion before I can create a fit card."
    if not new_item:
        return "I need a selected item before I can create a fit card."
    prompt = f"""Write a 2-4 sentence thrift find caption someone would actually post.
New item: {new_item.get('title')}
Price: ${new_item.get('price')}
Platform: {new_item.get('platform')}
Outfit idea: {outfit}
Mention the item, its price exactly once, the platform exactly once, and the vibe. Keep it natural, not like a product listing."""
    return generate(prompt, system="Write concise, lively social captions. No markdown headings.")
