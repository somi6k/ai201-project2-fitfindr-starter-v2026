"""
The three FitFindr tools.

Each one is a standalone function you can call and test on its own, before any
of them are wired into the loop. Build and test them one at a time — three
untested tools joined by a loop is one problem that looks like six, because you
can't tell which layer is lying to you.

    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)             → str
    create_fit_card(outfit, new_item)              → str

All three are stubs right now. They run and they do nothing — that's the
starting position and it's deliberate.

⚠️ Before you write any of them, fill in the **Tool Inventory** section of your
README (Milestone 2). Four lines per tool: what it does, each input with its
type, exactly what it returns, and what it returns when it has nothing to give.
That last line is what your loop branches on. "Returns a list" earns nothing —
the description has to say what is *in* the list.
"""

import re

import config
from generate import generate
from utils.data_loader import load_listings


# ── Tool 1: search_listings ───────────────────────────────────────────────────

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    Search the listings data for items matching a description, and optionally a
    size and a price ceiling.

    This is the tool that doesn't call the model, which makes it the easiest one
    to test and the one to move onto MCP in unit 4.

    Args:
        description: keywords describing what the user wants
                     (e.g. "vintage graphic tee").
        size:        a size string to filter by, or None to skip size filtering.
                     Match case-insensitively — "M" should match "S/M".

                     ⚠️ Read the sizes in the data before you reach for a plain
                     substring test. `"s" in "us 9"` is True, and so is
                     `"l" in "xl"`. A filter that returns shoes when someone
                     asked for a small top reads like a broken search, and it
                     will quietly cost you in unit 4 when you test criterion 1.
                     What counts as a size match is part of your spec — decide
                     it and write it into your Tool Inventory.
        max_price:   maximum price, inclusive, or None to skip price filtering.

    Returns:
        A list of matching listing dicts, best match first.
        **Returns an empty list when nothing matches — an empty list, not None,
        and not an exception.** Your loop branches on this.

    Each listing dict has these fields:
        id, title, description, category, style_tags (list), size,
        condition, price (float), colors (list), brand (str or None), platform

    Note that `brand` is None for most listings. That is deliberate and
    realistic — thrift listings often have no brand. If something you write
    assumes a brand is always there, you will find out in unit 4.

    TODO:
        1. Load every listing with load_listings().
        2. Filter by max_price and by size, when each is provided.
        3. Score what's left by keyword overlap with `description`.
        4. Drop anything scoring zero.
        5. Sort by score, highest first, and return the listing dicts —
           at most config.SEARCH_RESULT_LIMIT of them.

    Test it from a terminal before you move on:
        python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
    """
    listings = load_listings()

    if max_price is not None:
        listings = [item for item in listings if item["price"] <= max_price]

    if size:
        wanted = _size_tokens(size)
        listings = [item for item in listings if wanted <= _size_tokens(item["size"])]

    query_words = _words(description or "") - _STOPWORDS
    if not query_words:
        return []

    scored = []
    for item in listings:
        text = " ".join([
            item["title"],
            item["description"],
            item["category"],
            " ".join(item["style_tags"]),
            " ".join(item["colors"]),
        ])
        score = len(query_words & _words(text))
        if score > 0:
            scored.append((score, item))

    # sorted() is stable, so ties keep their order from the data file.
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [item for _, item in scored[: config.SEARCH_RESULT_LIMIT]]


_STOPWORDS = {"a", "an", "the", "and", "or", "in", "on", "for", "with", "of", "to", "size", "under"}


def _words(text: str) -> set[str]:
    """Lowercase alphanumeric words in `text`, e.g. "90s Track-Jacket" → {"90s", "track", "jacket"}."""
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def _size_tokens(size: str) -> set[str]:
    """
    Split a size string into whole tokens, so matching is token-for-token
    rather than substring: "S/M" → {"s", "m"}, "US 8.5" → {"us", "8.5"},
    "One Size (adjustable)" → {"one", "size", "adjustable"}.

    A requested size matches a listing when every one of its tokens appears in
    the listing's tokens. So "M" matches "S/M" and "M/L", but "S" does not
    match "US 9", "L" does not match "XL", and "US 8" does not match "US 8.5".
    """
    return {tok for tok in re.split(r"[\s/()]+", size.lower()) if tok}


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    """
    Given a thrifted item and the user's wardrobe, suggest one or two outfits.

    This one calls the model, through `generate()`. You don't need to think
    about rate limits — the adapter handles pacing for you.

    Args:
        new_item: a listing dict — the item the user is considering.
        wardrobe: a wardrobe dict with an 'items' key holding a list of items.
                  **It may be empty.** Handle that.

    Returns:
        A non-empty string with outfit suggestions.
        With an empty wardrobe, return general styling advice rather than
        raising or returning "". Unit 4 has you trigger the empty wardrobe on
        purpose, so decide now what it should do.

    TODO:
        1. Check whether wardrobe['items'] is empty.
        2. If it is, ask the model for general styling ideas for this item.
        3. If it isn't, format the wardrobe items into the prompt and ask for
           specific combinations naming pieces the user already owns.
        4. Return the model's response.

    Test it from a terminal before you move on:
        python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
    """
    items = (wardrobe or {}).get("items") or []
    item_text = _describe_listing(new_item)

    if not items:
        prompt = (
            f"Someone is thinking about buying this thrifted item:\n\n{item_text}\n\n"
            "They haven't told us anything about their wardrobe yet. Suggest one "
            "or two outfits built around this item, using general wardrobe staples "
            "(describe the kind of piece, e.g. 'straight-leg dark jeans'). Keep it "
            "under 120 words."
        )
    else:
        wardrobe_text = "\n".join(_describe_wardrobe_item(w) for w in items)
        prompt = (
            f"Someone is thinking about buying this thrifted item:\n\n{item_text}\n\n"
            f"Here is what they already own:\n{wardrobe_text}\n\n"
            "Suggest one or two outfits that pair the new item with pieces from "
            "their wardrobe. Name each wardrobe piece exactly as it is listed above, "
            "and only use pieces from that list. Keep it under 120 words."
        )

    response = generate(prompt, system=_STYLIST_SYSTEM)
    if not response.strip():
        return f"No outfit ideas came back for the {new_item.get('title', 'item')} — try asking again."
    return response


_STYLIST_SYSTEM = (
    "You are a practical thrift stylist. Give concrete outfit combinations, "
    "not fashion theory. Plain text, no markdown headings."
)


def _describe_listing(item: dict) -> str:
    """One readable block for a listing. Skips brand when the listing has none."""
    lines = [
        f"Title: {item.get('title')}",
        f"Category: {item.get('category')}",
        f"Description: {item.get('description')}",
        f"Colors: {', '.join(item.get('colors') or [])}",
        f"Style: {', '.join(item.get('style_tags') or [])}",
        f"Size: {item.get('size')}",
        f"Condition: {item.get('condition')}",
    ]
    if item.get("brand"):
        lines.append(f"Brand: {item['brand']}")
    return "\n".join(lines)


def _describe_wardrobe_item(item: dict) -> str:
    """One line per wardrobe piece, e.g. "- Black combat boots (shoes; black; boots, grunge) — Lace-up"."""
    line = (
        f"- {item.get('name')} ({item.get('category')}; "
        f"{', '.join(item.get('colors') or [])}; "
        f"{', '.join(item.get('style_tags') or [])})"
    )
    if item.get("notes"):
        line += f" — {item['notes']}"
    return line


# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
    """
    Write a short caption someone would actually post about the find.

    This calls the model too.

    Args:
        outfit:   the outfit suggestion string from suggest_outfit().
        new_item: the listing dict for the item.

    Returns:
        A two-to-four sentence caption.
        If `outfit` is empty or whitespace, return a descriptive message rather
        than raising.

    The caption should read like a real post rather than a product description,
    mention the item and its price and platform once each, and be specific about
    the vibe.

    It should also come out **differently for different inputs**. If you run
    this three times on the same item and get three word-for-word identical
    strings, it's one of two things, and both are near the top of `config.py`:

        • CACHE_ENABLED — the adapter handed back an answer it already had
        • TEMPERATURE   — at 0.0 the model gives the same words every time

    TODO:
        1. Guard against an empty or whitespace-only `outfit`.
        2. Build a prompt with the item details and the outfit.
        3. Call generate() and return the response.

    Test it from a terminal before you move on:
        python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
    """
    title = new_item.get("title", "this find")
    if not outfit or not outfit.strip():
        return f"No outfit to caption yet for the {title} — get an outfit suggestion first."

    price = new_item.get("price")
    price_text = f"${price:g}" if isinstance(price, (int, float)) else "an unlisted price"
    platform = new_item.get("platform", "a thrift app")

    prompt = (
        f"Write a caption for a social media post about a thrift find.\n\n"
        f"The item:\n{_describe_listing(new_item)}\n"
        f"Price: {price_text}\n"
        f"Found on: {platform}\n\n"
        f"How they're wearing it:\n{outfit}\n\n"
        "Rules:\n"
        "- 2 to 4 sentences, first person, casual — like a real person posting "
        "their fit, not a product listing.\n"
        f"- Mention the item, the price ({price_text}) and the platform ({platform}) "
        "exactly once each.\n"
        "- Be specific about the vibe of the outfit — name a piece or two from it.\n"
        "- Only mention clothing and accessories that appear in the outfit above "
        "or the item itself. Don't add pieces that aren't there.\n"
        "- Don't repeat the listing description, and don't list condition or "
        "measurements.\n"
        "- At most two emojis and two hashtags. Return only the caption."
    )

    response = generate(prompt, system=_CAPTION_SYSTEM)
    if not response.strip():
        return f"Couldn't write a caption for the {title} this time — try again."
    return response


_CAPTION_SYSTEM = (
    "You write short, natural outfit-post captions in the voice of someone "
    "showing off a thrift find to friends. Never sound like an ad or a listing."
)
