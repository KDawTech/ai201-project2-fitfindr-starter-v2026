"""Unit 4 evaluation scenarios — one scored scenario for each criterion."""

SCENARIOS = [
    {
        "name": "matching query completes",
        "query": "vintage graphic tee under $30",
        "wardrobe": "example",
        "criterion": 1,
    },
    {
        "name": "impossible query stops early",
        "query": "designer ballgown size XXS under $5",
        "wardrobe": "example",
        "criterion": 2,
    },
    {
        "name": "state handoff preserves selected item",
        "query": "90s track jacket size M under $50",
        "wardrobe": "example",
        "criterion": 3,
    },
    {
        "name": "fit card contains key facts",
        "query": "denim jacket under $50",
        "wardrobe": "example",
        "criterion": 4,
    },
    {
        "name": "search respects price ceiling",
        "query": "vintage top under $20",
        "wardrobe": "example",
        "criterion": 5,
    },
    {
        "name": "empty wardrobe failure-mode check",
        "query": "denim jacket under $50",
        "wardrobe": "empty",
        "criterion": None,
    },
]

WARDROBES = ("example", "empty")


def validate() -> list[str]:
    problems = []
    seen_criteria = set()
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("query", "").strip():
            problems.append(f"scenario {i} has no query")
        if scenario.get("wardrobe") not in WARDROBES:
            problems.append(
                f"scenario {i} has wardrobe {scenario.get('wardrobe')!r}; expected one of {WARDROBES}"
            )
        criterion = scenario.get("criterion")
        if criterion is not None:
            if criterion not in {1, 2, 3, 4, 5}:
                problems.append(f"scenario {i} has invalid criterion {criterion!r}")
            if criterion in seen_criteria:
                problems.append(f"criterion {criterion} is assigned to more than one scenario")
            seen_criteria.add(criterion)
    missing = {1, 2, 3, 4, 5} - seen_criteria
    if missing:
        problems.append(f"missing scored scenarios for criteria: {sorted(missing)}")
    return problems
