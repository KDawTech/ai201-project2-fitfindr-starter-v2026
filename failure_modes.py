"""Deliberately trigger the three Unit 4 failure modes and print the handling."""
from __future__ import annotations

import os

from agent import run_agent
from utils.data_loader import get_empty_wardrobe, get_example_wardrobe


def show(label: str, session: dict) -> None:
    print(f"\n=== {label} ===")
    print("error:", session.get("error"))
    print("selected_item:", (session.get("selected_item") or {}).get("title"))
    print("outfit_suggestion:", session.get("outfit_suggestion"))
    print("fit_card:", session.get("fit_card"))


def main() -> None:
    # 1) Empty search: must stop before suggest_outfit/create_fit_card.
    show(
        "Failure mode 1 — empty search",
        run_agent("designer ballgown size XXS under $5", get_example_wardrobe()),
    )

    # 2) Empty wardrobe: should still produce general styling advice and a card.
    show(
        "Failure mode 2 — empty wardrobe",
        run_agent("denim jacket under $50", get_empty_wardrobe()),
    )

    # 3) Model unavailable: override the key for one run, then restore it.
    import generate

    old_key = os.environ.get("GEMINI_API_KEY")
    old_client = generate._client
    try:
        os.environ["GEMINI_API_KEY"] = "definitely-invalid-fitfindr-key"
        generate._client = None
        show(
            "Failure mode 3 — model unavailable / bad key",
            run_agent("vintage graphic tee under $30", get_example_wardrobe()),
        )
    finally:
        if old_key is None:
            os.environ.pop("GEMINI_API_KEY", None)
        else:
            os.environ["GEMINI_API_KEY"] = old_key
        generate._client = old_client


if __name__ == "__main__":
    main()
