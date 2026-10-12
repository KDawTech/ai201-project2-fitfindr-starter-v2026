# FitFindr

## What This Does

FitFindr is a small shopping/styling agent for secondhand listings. A user asks for an item in plain language, such as `vintage graphic tee under $30`, and the agent parses the request, searches the listings data, selects the best match, suggests an outfit using the saved wardrobe, and creates a short fit-card caption. If no listing matches, the planning loop stops early and tells the user what to change instead of calling later tools with missing data.

---

## Tool Inventory

### `search_listings`

- **What it does:** Searches the local thrift listing dataset using description keywords plus optional size and maximum-price filters, then ranks matching items by keyword overlap.
- **Inputs:** `description` (`str`), `size` (`str | None`), `max_price` (`float | None`).
- **Returns:** A `list[dict]` of at most 10 listing dictionaries, best match first. Every listing contains `id`, `title`, `description`, `category`, `style_tags`, `size`, `condition`, `price`, `colors`, `brand`, and `platform`.
- **When it has nothing:** Returns an empty list `[]`.

### `suggest_outfit`

- **What it does:** Uses the selected listing and wardrobe to generate one or two specific outfit ideas.
- **Inputs:** `new_item` (`dict` listing), `wardrobe` (`dict` with an `items` list).
- **Returns:** A non-empty `str` containing outfit suggestions; when wardrobe items exist, it names useful saved pieces.
- **When it has nothing:** If the wardrobe is empty, it still returns general styling advice. If no item is supplied, it returns a descriptive message instead of crashing.

### `create_fit_card`

- **What it does:** Turns the selected listing and outfit suggestion into a short post-style thrift caption.
- **Inputs:** `outfit` (`str`), `new_item` (`dict` listing).
- **Returns:** A 2–4 sentence `str` caption mentioning the item, price, platform, and vibe.
- **When it has nothing:** If the outfit text or selected item is missing, it returns a descriptive message rather than raising an exception.

---

## Planning Loop

**Branch rule:** If `search_listings` returns an empty list, put a useful message in `session["error"]` and stop immediately. Otherwise, select the first search result, save it in the session, pass that exact item through session state into `suggest_outfit`, save the outfit, then call `create_fit_card` and save the fit card.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** `agent.py::parse_query` uses regular expressions to extract `under/below/less than $PRICE` and `size VALUE`. Those pieces are removed from the query and the remaining text becomes the search description.

**What moves through the session:** `query` → `parsed` → `search_results` → `selected_item` → `suggest_outfit_item_id` → `outfit_suggestion` → `fit_card`. The wardrobe also stays in the session for the whole run.

---

## Sample Run

**One full query**

```text
$ python app.py ask 'vintage graphic tee under $30'

  Found:    Graphic Tee — 2003 Tour Bootleg Style — $24.0 on depop

  Outfit:   Pair the faded graphic tee with your black straight-leg jeans and white leather sneakers for an easy streetwear base. Add the light-wash denim jacket if you want more of a layered vintage look.

  Fit card: Found this faded 2003-tour-style graphic tee for $24 on Depop. Black straight-leg jeans, white sneakers, and a light denim layer keep the vibe relaxed and vintage without looking costume-y.
```

**The three tools, tested one at a time**

```text
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
[{'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', ..., 'price': 24.0, 'platform': 'depop'}, ...]
```

```text
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[5], get_example_wardrobe()))"
Pair the graphic tee with the black straight-leg jeans and white leather sneakers. Add the light-wash denim jacket for a layered vintage streetwear look.
```

```text
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('black jeans and white sneakers', load_listings()[5]))"
Found this faded graphic tee for $24 on Depop and it already feels like the easiest weekend fit. Black jeans and white sneakers keep the whole thing relaxed with a worn-in vintage vibe.
```

**Empty-search branch**

```text
$ python app.py ask 'designer ballgown size XXS under $5'

  I couldn't find a listing that matches all of that. Try raising your price limit, removing the size filter, or using broader item/style words.
```

---

## How I Used AI

**Moment 1**

- **What I asked for:** I asked AI to help pressure-test a search implementation that had to match sizes such as `M`, `S/M`, `M/L`, and `US 8` without accidentally treating a single letter as a substring of an unrelated size.
- **What came back:** The suggested approach was to tokenize the listing-size string and require an exact size token instead of using a plain substring test.
- **What I changed:** I implemented `_size_match()` in `tools.py`, so `M` can match `S/M` or `M/L`, numeric shoe sizes match an exact number, and `M` does not incorrectly match `XL`.

**Moment 2**

- **What I asked for:** I asked AI to review the planning-loop branch and state flow for the requirement that an empty search stop before the model-backed tools and that the selected search item be testable as it moves to `suggest_outfit`.
- **What came back:** The review recommended making the empty-list branch explicit and recording the selected item ID before the outfit call so the state handoff can be checked later.
- **What I changed:** `agent.py::run_agent` now returns immediately with a useful `session["error"]` when search is empty, and it records `session["suggest_outfit_item_id"]` from the selected item before calling the outfit tool.

---

## Unit 4 Sections

Unit 4 uses this same repository. The before/after run logs, diagnoses, MCP trace, improvement, and remaining issues should be added here without deleting the Unit 3 sections.
