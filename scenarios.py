"""
The runs your test needs. ← UNIT 4, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
the empty-search branch needs an impossible query. One about the fit card needs
the same item run more than once. Working that out is Milestone 3's first step,
and this file is where you write it down.

`run_eval.py` runs everything here five times and writes the run log — five
because your criteria are written out of five.

Three scenarios are filled in to show the shape. Add or change whatever your
own criteria need — these are a starting point, not a fixed set.
"""

SCENARIOS = [
    {
        # A query the data can match. Criterion 1.
        "name": "matching query completes",
        "query": "vintage graphic tee under $30",
        "wardrobe": "example",
        "criterion": 1,
    },
    {
        # A query nothing can match. Criterion 2 — the branch.
        "name": "impossible query stops early",
        "query": "designer ballgown size XXS under $5",
        "wardrobe": "example",
        "criterion": 2,
    },
    {
        # State: the item search picked is the item each later tool received.
        # Criterion 3 (revised in unit 4). Pass = in the trace, the top-result
        # id, the selected id, and the new_item.id passed to suggest_outfit and
        # to create_fit_card are all the same (lst_004, the 90s Track Jacket).
        "name": "selected item reaches suggest_outfit",
        "query": "90s track jacket in size M",
        "wardrobe": "example",
        "criterion": 3,
    },
    {
        # Fit card content. Criterion 4. A different item from criterion 1, so
        # the check isn't only ever run on one listing. Pass = session["fit_card"]
        # names the item (e.g. "platform sneakers" — not the verbatim title),
        # its price ($48 or spelled out, e.g. "forty-eight bucks") and its
        # platform (poshmark).
        "name": "fit card names item, price and platform",
        "query": "platform sneakers size 8",
        "wardrobe": "example",
        "criterion": 4,
    },
    {
        # A user with nothing saved. One of unit 4's three failure modes.
        # Criterion 5. Pass = no error, and session["outfit_suggestion"] is
        # general styling advice that doesn't name pieces from the example wardrobe.
        "name": "empty wardrobe",
        "query": "denim jacket under $50",
        "wardrobe": "empty",
        "criterion": 5,
    },
]

WARDROBES = ("example", "empty")


def validate() -> list[str]:
    """Complain about anything malformed, before a long run rather than during."""
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("query", "").strip():
            problems.append(f"scenario {i} has no query")
        if scenario.get("wardrobe") not in WARDROBES:
            problems.append(
                f"scenario {i} has wardrobe {scenario.get('wardrobe')!r} — "
                f"it should be one of {WARDROBES}"
            )
    return problems
