"""FitFindr planning loop with a visible session state and an empty-search branch."""
from __future__ import annotations
import re
import trace
from generate import ModelUnavailable
from tools import search_listings, suggest_outfit, create_fit_card

def new_session(query: str, wardrobe: dict) -> dict:
    return {
        "query": query,
        "parsed": {},
        "search_results": [],
        "selected_item": None,
        "suggest_outfit_item_id": None,
        "wardrobe": wardrobe,
        "outfit_suggestion": None,
        "fit_card": None,
        "error": None,
    }

def parse_query(query: str) -> dict:
    text = query.strip()
    price_match = re.search(r"(?:under|below|less than)\s*\$?\s*(\d+(?:\.\d+)?)", text, flags=re.I)
    max_price = float(price_match.group(1)) if price_match else None
    # Accept size M, in size M, size 8, etc.
    size_match = re.search(r"\bsize\s+([A-Za-z]{1,4}|\d{1,2})\b", text, flags=re.I)
    size = size_match.group(1).upper() if size_match else None
    description = text
    if price_match: description = description.replace(price_match.group(0), " ")
    if size_match: description = description.replace(size_match.group(0), " ")
    description = re.sub(r"\b(in|for)\s*$", "", description, flags=re.I).strip(" ,.-")
    description = re.sub(r"\s+", " ", description)
    return {"description": description, "size": size, "max_price": max_price}

def run_agent(query: str, wardrobe: dict) -> dict:
    session = new_session(query, wardrobe)
    iteration = 1
    trace.check_iterations(iteration)
    session["parsed"] = parse_query(query)
    p = session["parsed"]
    session["search_results"] = search_listings(p["description"], p["size"], p["max_price"])
    if not session["search_results"]:
        session["error"] = (
            "I couldn't find a listing that matches all of that. Try raising your price limit, "
            "removing the size filter, or using broader item/style words."
        )
        return session
    session["selected_item"] = session["search_results"][0]
    # State is intentionally visible/testable: the ID sent to the next tool is recorded.
    session["suggest_outfit_item_id"] = session["selected_item"]["id"]
    try:
        session["outfit_suggestion"] = suggest_outfit(
            session["selected_item"], session["wardrobe"]
        )
        session["fit_card"] = create_fit_card(
            session["outfit_suggestion"], session["selected_item"]
        )
    except ModelUnavailable as exc:
        session["error"] = f"The styling model is unavailable: {exc}"
    return session

def _show(session: dict):
    if session["error"]:
        print("  stopped:", session["error"])
        print("  fit_card is", repr(session["fit_card"]))
        return
    item = session["selected_item"]
    print(f"  found:    {item['title']} — ${item['price']} on {item['platform']}")
    print(f"  outfit:   {session['outfit_suggestion']}")
    print(f"  fit card: {session['fit_card']}")

if __name__ == "__main__":
    from utils.data_loader import get_example_wardrobe
    print("=== matching query ===")
    _show(run_agent("vintage graphic tee under $30", get_example_wardrobe()))
    print("\n=== impossible query ===")
    _show(run_agent("designer ballgown size XXS under $5", get_example_wardrobe()))
