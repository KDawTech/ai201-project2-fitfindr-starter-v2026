# Acceptance criteria — FitFindr

These criteria are written in Unit 3 before the Unit 4 evaluation.

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes `search_listings`, `suggest_outfit`, and `create_fit_card` and returns a non-empty fit card — in at least **4 of 5 tries**.

**Why this target:** Search is a plain keyword/field filter and two later tools call a nondeterministic model, so I want consistent success while allowing one run to miss because of phrasing or a model response.

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling `suggest_outfit` and returns a message naming something the user can change — **5 of 5 tries**.

**Why this target:** This branch is deterministic code, not model behavior. An empty list should always cause the same safe stop, so anything below 5 of 5 means the loop is wrong.

---

## 3. Session state preserves the selected item

For a matching query, `session["selected_item"]["id"]` must equal `session["suggest_outfit_item_id"]`, showing that the exact item chosen from search is the item sent to the outfit step — **5 of 5 tries**.

**Why this target:** State transfer is deterministic and directly observable. If the IDs differ even once, the agent is styling a different item from the one it selected.

---

## 4. Fit cards contain the key listing facts

For a matching query, the fit card must be **2–4 sentences** and mention the selected item's **price and platform** — in at least **4 of 5 tries**.

**Why this target:** The wording can vary because the fit card is model-generated, but the price and platform are core facts that should survive that variation. I allow one miss because generation is nondeterministic.

---

## 5. Search always respects a price ceiling

Across five searches that include `max_price`, **every listing returned** must have `price <= max_price` — **5 of 5 searches**.

**Why this target:** Price filtering is deterministic and is a direct user constraint. Returning an over-budget item would make the search tool untrustworthy, so the target should be perfect.
