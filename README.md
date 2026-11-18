# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->

FitFindr is a thrift-shopping assistant. You describe in plain English what you are looking for, including size, price, colors or material, and it searches for listings meeting your criteria. It then takes the best match and suggests a few outfits incorporating items already in your wardrobe, or gives general advice if you have yet to build out your wardrobe. Finally, it writes a short, casual description you can post as a caption for your new thrifty find. If nothing matches, it stops before suggesting anything and tells you what to adjust, such as the price, size or description.
---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:** search_listings searches the listings file for entries that match the description, and optionally the size and maximum price.
- **Inputs:** The inputs are description (string), size (optional, string) and max_price (optional, float, inclusive).
  - **Size rule:** Sizes are compared whole word by whole word, ignoring case, never by substring. Both the requested size and the listing's size are split on spaces, slashes and parentheses (so "S/M" becomes S and M, and "US 8.5" becomes US and 8.5). A listing matches if every part of the requested size appears in the listing's size. So "M" matches "M", "S/M" and "M/L"; "S" does not match "US 9"; "L" does not match "XL"; and "US 8" does not match "US 8.5". If size is None, sizes aren't filtered.
- **Returns:** The return item is a list of dicts which are the returned clothing items from the listings file, sorted by keyword-overlap score, highest first, at most 10 (config.SEARCH_RESULT_LIMIT); listings scoring 0 are dropped. Each dict has the fields id, title, description, category, style_tags, size, condition, price, colors, brand and platform.
- **When it has nothing:** When the search_listings function does not have anything to return it send an empty list.

### `suggest_outfit`

- **What it does:** suggest_outfit takes a new item and the user's existing wardrobe and suggests outfits to wear.
- **Inputs:** The inputs to suggest_outfit are new_item (dict) and wardrobe (dict). The wardrobe dict items have fields id, name, category, colors, style_tags and notes. The new_item dict has all of the same fields as the returned items from the search_listings function.
- **Returns:** suggest_outfit returns a non-empty string with outfit suggestions based on the user's existing wardrobe and the potential new item.
- **When it has nothing:** When the function is provided with an empty wardrobe, it will return a string with general styling advice involving the selected item.

### `create_fit_card`

- **What it does:** create_fit_card takes the suggested outfit and the new item and writes a caption based on the outfit and discovered item that a user would post to social media.
- **Inputs:** The inputs to create_fit_card are outfit (string), and new_item (dict), with the dict being of the same structure as the suggest_outfit functoni.
- **Returns:** create_fit_card returns a two to four sentence post containing the item description, price and platform written as if it were a real user making the post.
- **When it has nothing:** When the tool has nothing to return it should send back a descriptive message instead of an empty string.

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:** If search_listings returns an empty list, update the session and stop, otherwise take the first result from the list and call suggest_outfit.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** regex in agent.py::parse_query

**What moves through the session:** query → parsed → search_results → selected_item → outfit_suggestion → fit_card. error is set only on the empty-search path.

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query** 

```
$ python app.py ask 'some tan boots size 8.5'                             

  Found:    Suede Chelsea Boots — Tan — $44.0 on poshmark

  Outfit:   Outfit One: The Relaxed Everyday
Pair the Suede Chelsea Boots — Tan with the baggy straight-leg jeans, dark wash. Tuck in the white ribbed tank top, and add the brown leather belt. Layer the slightly cropped vintage black denim jacket on top, and carry the black crossbody bag. 

Outfit Two: The Tonal Minimalist
Wear the Suede Chelsea Boots — Tan with the wide-leg khaki trousers. Layer the white ribbed tank top underneath the oversized grey crewneck sweatshirt, letting the tank hem peek out slightly. Finish the look with the black crossbody bag for a casual daytime errand outfit.

  Fit card: Scored these tan suede Chelsea boots on Poshmark for $44 and they immediately became my go-to with wide-leg trousers and a cozy crewneck. Love the little bit of western edge they add to everyday errands. 🤎 #thriftyfinds #ootd

```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"

[{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_011', 'title': 'Low-Rise Cargo Pants — Khaki', 'description': 'Y2K era low-rise cargo pants. Lots of pockets. Khaki color, slightly distressed at the hems. Great for layering with a long tee.', 'category': 'bottoms', 'style_tags': ['y2k', 'cargo', '2000s', 'streetwear'], 'size': 'W29', 'condition': 'fair', 'price': 27.0, 'colors': ['khaki', 'tan'], 'brand': None, 'platform': 'poshmark'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}]

```

```
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"

Outfit One: Casual Everyday
Pair the Vintage Levi's 501 Jeans with the white ribbed tank top tucked in. Add the brown leather belt to define the waist. Throw on the oversized grey crewneck sweatshirt for a relaxed layer, and finish with the chunky white sneakers and the black crossbody bag.

Outfit Two: Streetwear Edge
Wear the Vintage Levi's 501 Jeans with the black cropped zip hoodie. Layer the vintage black denim jacket on top for a double-denim look. Ground the outfit with the black combat boots and complete the look with the black crossbody bag.

```

```
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
Scored these vintage Levi's on depop for $38 and I honestly might never take them off. Paired them with my beaten-up white sneakers for the easiest everyday uniform. Love how broken-in they feel right out of the box 👖✨ #thrifty #denim

```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:* I asked Claude to implement `search_listings` using `load_listings()`. It should filter by size and max_price when they're given, score what's left by keyword overlap with the description, drop zero scores, sort highest first, cap the results at `config.SEARCH_RESULT_LIMIT`, and return `[]` when nothing matches.
- *What came back:* A working version that matches sizes by whole token instead of substring, so "S" doesn't match "US 9" and "L" doesn't match "XL". It scores keywords against the title, category, tags and colors as well as the listing's description. Testing showed that when two listings score the same, they stay in the order of the data file, so "graphic tee" ranked the Y2K Baby Tee above the actual "Graphic Tee — 2003 Tour Bootleg Style".
- *What I changed:* My Tool Inventory didn't say what counts as a size match, so I added the size rule with examples of matches and non-matches. I also removed a `color` field from my Returns line, because listings only have `colors`.

**Moment 2**

- *What I asked for:* I asked Claude to implement `create_fit_card` following the docstring: a caption that reads like a real post, mentions the item, price and platform once each, and handles an empty outfit.
- *What came back:* Captions that read naturally and came out differently on each run with the cache off. But given the outfit "jeans and white sneakers", one caption mentioned a "white tee" that wasn't in the outfit.
- *What I changed:* I added a rule to the prompt that the caption may only mention pieces from the outfit it was given, then re-ran the same input to confirm the invented piece was gone. 4 out of 4 re-runs mentioned only the jeans and sneakers.



<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. A matching query completes all three tools | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. An impossible query stops before the second tool | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Same listing id at every hand-off: search → selected_item → suggest_outfit → create_fit_card (revised) | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card names the item, price and platform | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Empty wardrobe gets general styling advice | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

Full log: [results/run_2026-10-18_2109_before-c3-revised.md](results/run_2026-10-18_2109_before-c3-revised.md) — `python run_eval.py --label before-c3-revised`, caching off, temperature 0.9. All five rows are scored from this one run.

Criterion 3 was revised before this run (see `criteria.md`): the first run ([results/run_2026-10-18_2055_before.md](results/run_2026-10-18_2055_before.md)) scored it from the outfit text, which measures the model, not the session. For this run I added the listing id at each hand-off to the trace, and re-ran every scenario so the whole table comes from the same code.

**Real output from one try**, pasted as text, naming the file and function
that produced it:

Criterion 4, try 2 — query `platform sneakers size 8`, example wardrobe. Loop in
`agent.py::run_agent`; search via MCP (`mcp_server.py::search_listings`), outfit
from `tools.py::suggest_outfit`, caption from `tools.py::create_fit_card`.

```
[1] parse_query
      in:  'platform sneakers size 8'
      out: description='platform sneakers', size='8', max_price=None
[2] search_listings (via MCP)
      in:  description='platform sneakers', size='8', max_price=None
      out: 1 items: Platform Sneakers — White Chunky Sole
      →    branch: found results, top result id=lst_019, selected id=lst_019 (Platform Sneakers — White Chunky Sole)
[3] suggest_outfit
      in:  new_item.id=lst_019 ('Platform Sneakers — White Chunky Sole'), wardrobe=10 items
      out: Outfit 1: Skater Prep Pair the platform sneakers with the baggy straight-leg jeans, dark wash and the white ri…
[4] create_fit_card
      in:  new_item.id=lst_019 ('Platform Sneakers — White Chunky Sole'), outfit='Outfit 1: Skater Prep
Pair the platfor…
      out: Finally scored these chunky platform sneakers on Poshmark for $48 and I am obsessed with the heavy Y2K sole. H…

selected_item: Platform Sneakers — White Chunky Sole ($48.0, poshmark)

outfit_suggestion:
Outfit 1: Skater Prep
Pair the platform sneakers with the baggy straight-leg jeans, dark wash and the
white ribbed tank top. Layer the oversized grey crewneck sweatshirt on top to lean
into that late 90s streetwear proportion. Finish the look with the black crossbody
bag for a casual, everyday feel.

Outfit 2: Contrast Utility
Wear the platform sneakers with the wide-leg khaki trousers and the white ribbed
tank top tucked in. Throw on the vintage black denim jacket as a structured outer
layer. Add the brown leather belt to tie the earth tones together and keep the
crossbody bag.

fit_card:
Finally scored these chunky platform sneakers on Poshmark for $48 and I am obsessed
with the heavy Y2K sole. Had to test drive them immediately with baggy straight-leg
jeans and an oversized grey crewneck. 👟 #thrifted
```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | A matching query completes all three tools | 4 of 5 | MET (5/5) | A try passed if `session["error"]` was None and `session["fit_card"]` was a non-empty caption. All 5 tries of `vintage graphic tee under $30` show all four trace steps and a fit card. |
| 2 | An impossible query stops before the second tool | 5 of 5 | MET (5/5) | A try passed if the trace ended at `search_listings (via MCP)` with `[] (empty)` and "branch: empty, stopping", `fit_card` was None, and `error` said what to change (price, size, keywords). All 5 tries match. |
| 3 | Same listing id at every hand-off (revised) | 5 of 5 | MET (5/5) | Read off the trace: top-result id, selected id, and the `new_item.id` into `suggest_outfit` and into `create_fit_card` all had to match. All 5 tries were `lst_004` at every step. |
| 4 | Fit card names the item, price and platform | 5 of 5 | MET (5/5) | Using my pre-run rule (item named recognisably, price numeric or spelled out, platform named), all 5 cards say "sneakers", "$48" and "Poshmark". Three said "chunky velcro sneakers" rather than "platform sneakers"; I counted those as naming the item. |
| 5 | Empty wardrobe gets general styling advice | 5 of 5 | MET (5/5) | A try passed if there was no error and `outfit_suggestion` gave outfits built from generic pieces instead of naming wardrobe items. All 5 used generic pieces (leggings, midi dress, loafers, "a fitted ribbed white tank"). |

**Diagnoses**

No criterion missed, so there is no miss to diagnose. Three things came close
enough to be worth recording, because a slightly stricter criterion would have
caught them:

- **Spelled-out prices — the model's output.** In criterion 1's scenario, 4 of
  5 captions wrote the price as "eighteen bucks" instead of "$18". The prompt in
  `tools.py::create_fit_card` gives the price as `$18` and says to mention it,
  but it also asks for a casual first-person voice, and the model resolves that
  tension by writing the number out. It only happened on the $18 item; the $42,
  $45 and $48 items were numeric every time. Criterion 4 allows spelled-out
  prices, so it passed — but a criterion requiring a "$" figure would have
  missed at 1/5 on this item.
- **Item named loosely — the model's output.** In criterion 4, 3 of 5 cards
  called the item "chunky velcro sneakers", drawing on the listing description
  instead of the title. Same mechanism: the prompt says to mention the item but
  doesn't say by which name.
- **Search picks a weaker match on ties — a tool.** `vintage graphic tee`
  selects the Y2K Baby Tee rather than "Graphic Tee — 2003 Tour Bootleg Style",
  because both score 3 keyword hits in `tools.py::search_listings` and ties keep
  their order from `listings.json`, where the baby tee comes first. No criterion
  checks *which* item is chosen, so this passes everything, but it's the most
  visible quality problem in the run.

The first version of criterion 3 was also a measurement problem rather than a
miss: it scored the outfit *text*, so it was measuring the model rather than the
session. That is why it was revised before the run above.


---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```
python app.py ask 'modern shirt in XL' --trace                    
[1] parse_query
      in:  'modern shirt in XL'
      out: description='modern shirt in XL', size=None, max_price=None
[2] search_listings (via MCP)
      in:  description='modern shirt in XL', size=None, max_price=None
      out: 3 items: Oversized Flannel Shirt — Plaid Red/Black, Vintage Polo Shirt — Forest Green, Shacket — Olive Canvas
      →    branch: found results, selected Oversized Flannel Shirt — Plaid Red/Black
[3] suggest_outfit
      in:  new_item='Oversized Flannel Shirt — Plaid Red/Black', wardrobe=10 items
      out: Outfit One Wear the new Oversized Flannel Shirt open over the white ribbed tank top. Pair it with the baggy st…
[4] create_fit_card
      in:  outfit='Outfit One\nWear the new Oversized Flanne'…, new_item='Oversized Flannel Shirt — Plaid Red/Black'
      out: Scored this vintage Woolrich flannel on thredUp for $22 and it’s already doing heavy lifting for layering. Tos…

  Found:    Oversized Flannel Shirt — Plaid Red/Black — $22.0 on thredUp

  Outfit:   Outfit One
Wear the new Oversized Flannel Shirt open over the white ribbed tank top. Pair it with the baggy straight-leg jeans, dark wash. Add the black combat boots and the black crossbody bag to finish the grunge look.

Outfit Two
Layer the oversized grey crewneck sweatshirt underneath the new Oversized Flannel Shirt for extra warmth. Pair them with the wide-leg khaki trousers and cinch the waist with the brown leather belt. Step into the chunky white sneakers and wear the black crossbody bag for a streetwear-inspired outfit.

  Fit card: Scored this vintage Woolrich flannel on thredUp for $22 and it’s already doing heavy lifting for layering. Tossed it on over a white ribbed tank and baggy jeans today, but tomorrow I’m definitely wearing it over my grey crewneck with khaki trousers. 🍂🖤 #thrifted #grunge

2 model calls this session, 782 prompt + 174 output tokens
```

**Empty search**

```
python app.py ask 'designer ballgown in XXS' --trace                  
[1] parse_query
      in:  'designer ballgown in XXS'
      out: description='designer ballgown in XXS', size=None, max_price=None
[2] search_listings (via MCP)
      in:  description='designer ballgown in XXS', size=None, max_price=None
      out: [] (empty)
      →    branch: empty, stopping

  Nothing matched 'designer ballgown in XXS'. Try to use fewer or more general words (e.g. 'jacket' instead of 'designer ballgown').

0 model calls this session
```

**On the MCP move:** I registered `search_listings` in `mcp_server.py` with the same typed inputs as `tools.py` and a description written for an outside agent (units, size rule, fields returned, and `[]` on no match). In `agent.py::run_agent` I replaced the direct `search_listings(...)` call with `call_tool("search_listings", {...})` — that one line was the only change to the loop. Nothing behaved differently: the same query returned the identical 6 listings over MCP as directly, and the no-match query still came back as `[]`, so the empty branch still stops the run. The only visible difference is that the search step is slower, since each call starts the server process.


---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:** One line added to the caption prompt in `tools.py::create_fit_card`:
`- Write the price exactly as {price_text}, in digits with the dollar sign — never spelled out (not "eighteen bucks").`
Nothing else changed — same scenarios, same caching-off settings, same temperature (0.9).

**Which failure it was meant to fix:** The spelled-out price from my diagnoses. In the before run,
4 of 5 captions for the Y2K Baby Tee wrote the price as "eighteen bucks" instead of "$18". The
prompt already gave the price as `$18` and said to mention it, but it also asked for a casual voice,
and the model resolved that by writing the number out. The fix makes the format explicit instead of
leaving it to the voice instruction. It didn't cause a criterion miss, because criterion 4 allows
spelled-out prices — but a caption you'd use to go buy something should show the actual figure.

### Run Log — After

Full log: [results/run_2026-10-18_2354_after.md](results/run_2026-10-18_2354_after.md) — `python run_eval.py --label after`.

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. A matching query completes all three tools | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. An impossible query stops before the second tool | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Same listing id at every hand-off (revised) | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card names the item, price and platform | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Empty wardrobe gets general styling advice | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

**Did it help, and how do I know:** Yes, for the thing it targeted. Counting captions that show the
price as a "$" figure, across all four scenarios that reach the fit card:

| Scenario (item) | Before | After |
|---|---|---|
| Y2K Baby Tee ($18) | 1 / 5 | 5 / 5 |
| 90s Track Jacket ($45) | 5 / 5 | 5 / 5 |
| Platform Sneakers ($48) | 5 / 5 | 5 / 5 |
| Denim Jacket ($42) | 5 / 5 | 5 / 5 |

Every after-run Baby Tee caption reads "$18" ("Scored this little butterfly tee on depop for just $18
and I'm obsessed…"). Nothing regressed: all five criteria are still 5/5, the ids still match at
every hand-off, and the empty-wardrobe outfits are still generic.

Two honest limits. First, the criteria table can't show this improvement — every row was already
MET, so the evidence is the price count above, not the verdicts. Second, the sneaker captions changed
wording: "chunky velcro sneakers" (3 of 5 before) became "chunky platforms" / "chunky white
platforms" (3 of 5 after), which still names the item but drops "sneakers". I can't tell from five
tries at temperature 0.9 whether the new line caused that or it's run-to-run variation.

---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**


---

## Capstone

**What This Extends**

This extends FitFindr, my project 2 agent. You describe a thrift find in plain English. It searches listings over MCP (`search_listings`), suggests an outfit from your wardrobe (`suggest_outfit`), and writes a caption (`create_fit_card`). Until now it only ran from the command line on my laptop (`python app.py ask ...` and `python run_eval.py`). Each run printed to the terminal and was gone when the window closed.

What's new: FitFindr runs as a hosted web service (`serve.py` behind `gunicorn`, with a public URL). Every request writes a structured log record with a timestamp, the query, the outcome or error, which tools ran, the tokens used, and how long it took. That gives me a measured cost and latency per run instead of a guess.

**The Shape**

Shape A, deploy and instrument. The extension is the operational layer around the agent I already have:

- the hosted run path (`gunicorn serve:app` on a free host)
- structured logging in `serve.py` that records successful and failed requests, so failures don't disappear
- per-request timing and token counts, which I'll use to measure cost and latency

The agent itself doesn't change. `serve.py` calls the same `run_agent()` that the CLI does.

Out of scope, things I considered and decided not to do:

- **No new tools or agent behavior.** I'm not adding a fourth tool, changing the planning loop in `agent.py`, or rewriting the prompts in `tools.py`. If a request fails because of the agent's reasoning, I'll log it and diagnose it, but fixing it is the agent's job, not this unit's.
- **No concurrency.** `serve.py` handles one request at a time on purpose. Each MCP call starts a second Python process, and the free tier's 512 MB has no room for two at once. I'm keeping the lock rather than adding a queue or more workers.
- **No front end or database.** No web UI, no auth, no log storage service. Logs go to a JSON-lines file, and I copy entries into this README in the same session, because the free host wipes its disk when it sleeps.

**Running It**

Path A, hosted on Render: https://ai201-project2-fitfindr-v2026.onrender.com (`GET /health`, `POST /ask`, `GET /logs?n=20`). It redeploys from `main` on every push and starts with `gunicorn serve:app`. Build settings, env vars, curl examples and the local run commands are in [RUNNING.md](RUNNING.md). I tested the local instructions from a fresh clone in a separate folder: venv on 3.13, install, `test.py` 10/10, `serve.py`, and one request logged.

**Instrumentation**

Every `POST /ask` writes one JSON record to `logs/requests.jsonl` through `request_log.py::write`, called from `serve.py::ask`. That includes requests that were rejected or crashed. The same line goes to stdout with a `[request]` prefix, so it shows in Render's Logs tab. `GET /logs?n=N` returns the latest records over HTTP, which matters because Render wipes its disk when the service sleeps or redeploys.

Fields in each record:

| Field | Meaning |
|---|---|
| `ts`, `request_id` | UTC arrival time; short random id |
| `query` / `body_preview` | What came in. `body_preview` holds the first 200 raw characters, only when the body was rejected |
| `status`, `outcome` | HTTP status. Outcome is one of `ok`, `no_results`, `agent_error`, `exception`, `bad_request` |
| `error` | `session["error"]` or the exception text; `null` on success |
| `tools_run`, `n_results`, `selected_id` | How far the agent got, how many listings came back, which listing was used |
| `fit_card` | What came out: the caption |
| `wait_ms`, `duration_ms` | Time queued behind another request; total time from arrival to response |
| `api_calls`, `cache_hits` | Live model calls (retries included); answers served from the local cache |
| `prompt_tokens`, `output_tokens` | Token counts the service reported for this request only |

These 12 records are from the live Render service on 2026-11-18. I sent 9 queries that should match, 1 that shouldn't, and 2 malformed bodies (`{not json` and `{"query": "   "}`). I pulled them with `GET /logs?n=50`. The full file is [results/capstone_render_2026-11-18.jsonl](results/capstone_render_2026-11-18.jsonl).

```jsonl
{"ts": "2026-11-18T21:04:04.412+00:00", "request_id": "01686bb5", "route": "/ask", "query": "vintage graphic tee under $30", "status": 200, "outcome": "ok", "error": null, "tools_run": ["parse_query", "search_listings", "suggest_outfit", "create_fit_card"], "n_results": 10, "selected_id": "lst_002", "fit_card": "Scored this butterfly baby tee on depop for only $18 and I'm obsessed with the pink and purple print. Paired it with wide-leg khaki trousers and a black cropped zip hoodie for a fun little grunge moment today. 🦋✨ #y2k #thrifted", "wait_ms": 1, "duration_ms": 17668, "api_calls": 2, "cache_hits": 0, "prompt_tokens": 814, "output_tokens": 172}
{"ts": "2026-11-18T21:04:22.419+00:00", "request_id": "27bdfb18", "route": "/ask", "query": "oversized flannel shirt", "status": 200, "outcome": "ok", "error": null, "tools_run": ["parse_query", "search_listings", "suggest_outfit", "create_fit_card"], "n_results": 7, "selected_id": "lst_003", "fit_card": "Scored this vintage Woolrich flannel for $22 on thredUp and haven't taken it off since. Obsessed with wearing it unbuttoned over a white ribbed tank and baggy dark wash jeans. 🖤✨ #grunge #thrifted", "wait_ms": 0, "duration_ms": 7321, "api_calls": 2, "cache_hits": 0, "prompt_tokens": 824, "output_tokens": 175}
{"ts": "2026-11-18T21:04:29.976+00:00", "request_id": "10c1d8bb", "route": "/ask", "query": "leather belt under $15", "status": 200, "outcome": "ok", "error": null, "tools_run": ["parse_query", "search_listings", "suggest_outfit", "create_fit_card"], "n_results": 1, "selected_id": "lst_014", "fit_card": "Found this vintage braided belt on thredUp for only $12 and I'm obsessed with how it looks cinching these khaki trousers. It just ties the whole earth-tone minimal vibe together so well with my black combat boots. 🤎✨ #thrifted #secondhandstyle", "wait_ms": 0, "duration_ms": 7077, "api_calls": 2, "cache_hits": 0, "prompt_tokens": 818, "output_tokens": 199}
{"ts": "2026-11-18T21:04:37.362+00:00", "request_id": "5a38cb11", "route": "/ask", "query": "90s slip dress size M", "status": 200, "outcome": "ok", "error": null, "tools_run": ["parse_query", "search_listings", "suggest_outfit", "create_fit_card"], "n_results": 3, "selected_id": "lst_013", "fit_card": "Scored this floral silk slip dress on depop for just $30 and I’m obsessed. Layered it over a white ribbed tank with my chunky combat boots for an easy ninety-inspired vibe. 🌸✨ #thrifted #90sfashion", "wait_ms": 0, "duration_ms": 8500, "api_calls": 2, "cache_hits": 0, "prompt_tokens": 818, "output_tokens": 154}
{"ts": "2026-11-18T21:04:46.166+00:00", "request_id": "63ec613d", "route": "/ask", "query": "low-rise cargo pants", "status": 200, "outcome": "ok", "error": null, "tools_run": ["parse_query", "search_listings", "suggest_outfit", "create_fit_card"], "n_results": 3, "selected_id": "lst_011", "fit_card": "Scored these low-rise khaki cargo pants on Poshmark for $27 and I'm obsessed with the fit. Threw them on with my chunky white sneakers and a black cropped zip hoodie for a super easy daily look. 👖✨ #Y2K #thrifted", "wait_ms": 0, "duration_ms": 6974, "api_calls": 2, "cache_hits": 0, "prompt_tokens": 831, "output_tokens": 177}
{"ts": "2026-11-18T21:04:53.441+00:00", "request_id": "1d160deb", "route": "/ask", "query": "mesh long-sleeve top size S/M", "status": 200, "outcome": "ok", "error": null, "tools_run": ["parse_query", "search_listings", "suggest_outfit", "create_fit_card"], "n_results": 2, "selected_id": "lst_017", "fit_card": "Scored this mesh long-sleeve top on depop for only $15 and I’m obsessed with how it looks under my grey crewneck. Just added wide-leg khaki trousers and chunky white sneakers to pull the whole earth-tone vibe together. 🖤 #y2k #thrifted", "wait_ms": 0, "duration_ms": 9804, "api_calls": 2, "cache_hits": 0, "prompt_tokens": 820, "output_tokens": 183}
{"ts": "2026-11-18T21:05:03.548+00:00", "request_id": "c6bbe16e", "route": "/ask", "query": "crewneck sweatshirt under $25", "status": 200, "outcome": "ok", "error": null, "tools_run": ["parse_query", "search_listings", "suggest_outfit", "create_fit_card"], "n_results": 2, "selected_id": "lst_012", "fit_card": "Scored this faded navy crewneck on thredUp for just $20 and it’s basically been my whole personality this week. Love how it looks thrown over baggy straight-leg jeans with a peek of white tank underneath. 🌊 #thriftfind #ootd", "wait_ms": 0, "duration_ms": 7002, "api_calls": 2, "cache_hits": 0, "prompt_tokens": 805, "output_tokens": 171}
{"ts": "2026-11-18T21:05:10.769+00:00", "request_id": "c3366dd8", "route": "/ask", "query": "faded band tee", "status": 200, "outcome": "ok", "error": null, "tools_run": ["parse_query", "search_listings", "suggest_outfit", "create_fit_card"], "n_results": 9, "selected_id": "lst_006", "fit_card": "Scored this faded graphic tee on depop for only $24 and I'm obsessed with the boxy fit. Threw it on over a white ribbed tank with my dark wash jeans and black combat boots for the ultimate grunge look. 🖤✨ #thriftfind #streetwear", "wait_ms": 0, "duration_ms": 10565, "api_calls": 2, "cache_hits": 0, "prompt_tokens": 808, "output_tokens": 169}
{"ts": "2026-11-18T21:05:21.534+00:00", "request_id": "8f0bad25", "route": "/ask", "query": "graphic hoodie size L", "status": 200, "outcome": "ok", "error": null, "tools_run": ["parse_query", "search_listings", "suggest_outfit", "create_fit_card"], "n_results": 3, "selected_id": "lst_015", "fit_card": "Scored this faded black hoodie on depop for $26 and I'm obsessed with how soft it is. Paired it with baggy straight-leg jeans and chunky white sneakers for the ultimate grunge streetwear fit. 🖤 #thrifted #streetwear", "wait_ms": 0, "duration_ms": 7448, "api_calls": 2, "cache_hits": 0, "prompt_tokens": 809, "output_tokens": 174}
{"ts": "2026-11-18T21:05:29.186+00:00", "request_id": "8cf62653", "route": "/ask", "query": "ballgown size XXS under $2", "status": 200, "outcome": "no_results", "error": "Nothing matched 'ballgown' in size XXS under $2. Try to raise your price limit, or drop the size, or use fewer or more general words (e.g. 'jacket' instead of 'designer ballgown').", "tools_run": ["parse_query", "search_listings"], "n_results": 0, "selected_id": null, "fit_card": null, "wait_ms": 0, "duration_ms": 3962, "api_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"ts": "2026-11-18T21:05:33.481+00:00", "request_id": "a1f873f7", "route": "/ask", "query": null, "body_preview": "{not json", "status": 400, "outcome": "bad_request", "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "tools_run": [], "n_results": null, "selected_id": null, "fit_card": null, "wait_ms": 0, "duration_ms": 0, "api_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"ts": "2026-11-18T21:05:33.780+00:00", "request_id": "f19d9d73", "route": "/ask", "query": null, "body_preview": "{\"query\": \"   \"}", "status": 400, "outcome": "bad_request", "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "tools_run": [], "n_results": null, "selected_id": null, "fit_card": null, "wait_ms": 0, "duration_ms": 0, "api_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
```

Failed runs: records 11 and 12 above are rejected inputs (400, `bad_request`), and record 10 is the planned stop when nothing matches (`no_results`). Below is a real crash, which I caught by accident while testing locally. Gemini returned 503 "high demand" and `generate.py` doesn't retry 503s, so the request returned a 500. It still left a record:

```json
{"ts": "2026-11-18T20:03:46.112+00:00", "request_id": "50b87e06", "route": "/ask", "query": "vintage graphic tee under $30", "tools_run": [], "n_results": null, "selected_id": null, "fit_card": null, "wait_ms": 1, "api_calls": 1, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0, "status": 500, "outcome": "exception", "error": "ModelUnavailable: Couldn't reach the model: 503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}", "duration_ms": 5596}
```

**What It Costs**

The real cost of one run is Gemini API spend: two model calls, `suggest_outfit` and `create_fit_card`. Search and parsing don't call the model.

How I measured it: Render runs with `AI201_CACHE=0`, so every request is a real model call. For each request, `serve.py` takes a snapshot of `generate.token_counts()` before and after `run_agent()` and logs the difference. Those counts come from the API's `usage_metadata`, not an estimate. I checked that Flash-Lite reports no separate thinking tokens (`thoughts_token_count` is `None`, and total equals prompt plus output), so the logged counts are the whole bill. I averaged the 9 successful runs in the log above. All 9 had `cache_hits: 0` and `api_calls: 2`.

| | Mean per successful run (n=9) | Range |
|---|---|---|
| Prompt tokens | 816.3 | 805 – 831 |
| Output tokens | 174.9 | 154 – 199 |
| Duration | 9.15 s | 6.97 – 17.67 s |

At the Gemini API paid-tier price for `gemini-3.5-flash-lite` ($0.30 per 1M input tokens, $2.50 per 1M output tokens):

- input: 816.3 × $0.30 / 1,000,000 = $0.000245
- output: 174.9 × $2.50 / 1,000,000 = $0.000437
- **≈ $0.00068 per run**

**100 people a day, one query each:** 100 × $0.00068 = **$0.068 per day**, about $2.05 per 30-day month. Output is 64% of that cost even though it's only 18% of the tokens. On the Gemini free tier, input tokens are free, so this is the paid-tier cost. No-match and rejected requests cost $0 in API spend because they never reach the model. Hosting is $0 on Render's free tier.

**Re-measured over the six test runs.** All 90 successful requests in `results/capstone/trial1`–`trial6` had `api_calls: 2` and `cache_hits: 0`. They averaged 740.3 prompt tokens (range 552–877; the empty-wardrobe runs send shorter prompts) and 173.5 output tokens (range 139–224):

- 740.3 × $0.30 / 1,000,000 + 173.5 × $2.50 / 1,000,000 = $0.000222 + $0.000434 = **$0.000656 per run**
- **100 people a day:** 100 × $0.000656 = **$0.066 per day**, about $1.97 per 30-day month

That's within 4% of the 9-run figure above, so the per-run cost is stable. What varies is time, not tokens.

**Run Log and Verdicts**

Criteria are in [criteria.md](criteria.md), committed in `8ee67e6 add capstone criteria` before any of these runs. All three trials ran against the live Render service on 2026-11-18, back to back, with nothing changed between them: trial 1 from 21:49:40 to 21:53:59 UTC, trial 2 from 21:53:59 to 21:56:26, and trial 3 from 21:56:27 to 21:58:41.

- **Runner:** `capstone_trial.py`. It sends the same 30 requests in the same order every trial: a `/health` warm-up, 7 good queries and 3 bad ones (malformed JSON, empty query, no-match) each followed by a `/logs` call, 3 more good queries, spares only to replace a non-`ok` run under criterion 2's rule, and 5 empty-wardrobe queries. It saves every raw request and response to `results/capstone/trialN/calls.jsonl`.
- **Render's stdout:** copied from Render's Logs tab into `results/capstone/trialN/render_stdout.txt`.
- **Scorer:** `capstone_score.py` grades each trial against criteria.md and writes `results/capstone/trialN/score.md`. Criterion 4's title check is a word-overlap pre-check that I confirmed by eye for all 15 cards.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Every query (7 good + 3 bad) leaves a `[request]` line in Render's log output | 10 of 10 | 9/10 | 10/10 | 10/10 | MISSED |
| 2. Warm `ok` runs finish within 10 s (server `duration_ms`) | 9 of 10 | 2/10 | 7/10 | 10/10 | MISSED |
| 3. `/logs` returns the latest 20 entries (or all if fewer), matching Render's stdout | 10 of 10 | 10/10 | 10/10 | 10/10 | MET |
| 4. Fit card names the item's title, price and platform (5 different queries) | 5 of 5 | 4/5 | 5/5 | 4/5 | MISSED |
| 5. Empty wardrobe gets general advice of at least 2 sentences | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |

**Real output, one run per criterion**

*Criterion 1, run 1.* Lines from Render's stdout (`results/capstone/trial1/render_stdout.txt`). Records are written by `request_log.py::write`, called from `serve.py::ask`. The "leather belt" request logged. The next one, "90s slip dress size M", ran past 30 s: gunicorn killed the worker and no `[request]` line was ever written. The traceback shows the worker was blocked inside `tools.py::create_fit_card` → `generate.py::generate` → `google.genai` → `httpx`, waiting for Gemini's response headers. The client got an HTML 500 after 30.9 s.

```
2026-11-18T21:50:18.489376526Z [request] {"ts": "2026-11-18T21:50:11.789+00:00", "request_id": "467682af", "route": "/ask", "query": "leather belt under $15", "tools_run": ["parse_query", "search_listings", "suggest_outfit", "create_fit_card"], "n_results": 1, "selected_id": "lst_014", "fit_card": "Found this braided leather belt on thredUp for only $12 and it instantly pulled my baggy jeans and white tank look together. It adds just the right western touch to break up the denim-on-denim vibe. 🤎 #thriftfind", "wait_ms": 0, "api_calls": 2, "cache_hits": 0, "prompt_tokens": 812, "output_tokens": 186, "status": 200, "outcome": "ok", "error": null, "duration_ms": 6700}
2026-11-18T21:50:49.529595316Z [2026-11-18 21:50:49 +0000] [57] [CRITICAL] WORKER TIMEOUT (pid:58)
2026-11-18T21:50:49.535745626Z [2026-11-18 21:50:49 +0000] [58] [ERROR] Error handling request /ask
2026-11-18T21:50:49.536240332Z [2026-11-18 21:50:49 +0000] [58] [INFO] Worker exiting (pid: 58)
2026-11-18T21:50:50.574918107Z [2026-11-18 21:50:50 +0000] [57] [ERROR] Worker (pid:58) was sent SIGKILL! Perhaps out of memory?
2026-11-18T21:50:50.664320502Z [2026-11-18 21:50:50 +0000] [72] [INFO] Booting worker with pid: 72
2026-11-18T21:51:04.327629634Z [request] {"ts": "2026-11-18T21:50:50.803+00:00", "request_id": "cf1245b6", "route": "/ask", "query": "low-rise cargo pants", "tools_run": ["parse_query", "search_listings", "suggest_outfit", "create_fit_card"], "n_results": 3, "selected_id": "lst_011", "fit_card": "Scored these low-rise cargo pants on Poshmark for $27 and I'm obsessed with the pockets. Threw them on with a white ribbed tank top and chunky white sneakers for an easy streetwear vibe. 👖✨ #thrifted #y2kstyle", "wait_ms": 0, "api_calls": 2, "cache_hits": 0, "prompt_tokens": 800, "output_tokens": 144, "status": 200, "outcome": "ok", "error": null, "duration_ms": 13523}
```

*Criterion 2, run 1.* From `results/capstone/trial1/score.md`. `duration_ms` comes from the log records written by `serve.py::ask`. The slip-dress 500 was replaced by the spare "velvet blazer", per the criterion's rule.

```
Warm-up: GET /health -> 200 in 243 ms (client)
- replaced (not ok): '90s slip dress size M' status=500 error='<html>\n  <head>\n    <title>Internal Server Error</title>\n  </head>\n  <body>\n    <h1><p>Internal Serv'
- FAIL 'vintage graphic tee under $30'      duration_ms=19823  (client 19954 ms)
- FAIL 'oversized flannel shirt'            duration_ms=10463  (client 10596 ms)
- PASS 'leather belt under $15'             duration_ms=6700  (client 6823 ms)
- FAIL 'low-rise cargo pants'               duration_ms=13523  (client 13670 ms)
- PASS 'mesh long-sleeve top size S/M'      duration_ms=7365  (client 7483 ms)
- FAIL 'crewneck sweatshirt under $25'      duration_ms=13237  (client 13376 ms)
- FAIL 'faded band tee'                     duration_ms=25262  (client 25512 ms)
- FAIL 'graphic hoodie size L'              duration_ms=14957  (client 15120 ms)
- FAIL 'suede chelsea boots'                duration_ms=16436  (client 16617 ms)
- FAIL 'velvet blazer'                      duration_ms=16383  (client 16542 ms)
```

*Criterion 3, run 3.* The `/logs` response (`serve.py::logs`) right after the no-match request, newest 3 of the 20 records returned. Those 20 request ids are, in order, the latest 20 `[request]` lines in Render's stdout at that moment.

```json
{
 "count_on_disk": 46,
 "records (newest 3 of 20)": [
  {
   "request_id": "473fc40a",
   "ts": "2026-11-18T21:57:19.814+00:00",
   "query": null,
   "body_preview": "{not json",
   "outcome": "bad_request"
  },
  {
   "request_id": "cd492b3f",
   "ts": "2026-11-18T21:57:20.040+00:00",
   "query": null,
   "body_preview": "{\"query\": \"   \"}",
   "outcome": "bad_request"
  },
  {
   "request_id": "65cda8f6",
   "ts": "2026-11-18T21:57:20.310+00:00",
   "query": "ballgown size XXS under $2",
   "outcome": "no_results"
  }
 ]
}
```

*Criterion 4, run 3.* From `results/capstone/trial3/score.md`. Fit cards come from `tools.py::create_fit_card`, returned by `POST /ask`. The cargo-pants card names the price and platform but never says what the item is ("Scored these on Poshmark…").

```
- PASS 'vintage graphic tee under $30' -> lst_002 'Y2K Baby Tee — Butterfly Print' $18 depop
    price=Y platform=Y TITLE CHECK (confirm by eye): words matched ['tee', 'butterfly']
    card: Found this little butterfly tee on depop for just $18 and I'm obsessed. Paired it with baggy dark wash jeans and chunky white sneakers for an easy streetwear vibe today. 🦋 #thrifted
- PASS 'oversized flannel shirt' -> lst_003 'Oversized Flannel Shirt — Plaid Red/Black' $22 thredUp
    price=Y platform=Y TITLE CHECK (confirm by eye): words matched ['flannel', 'red']
    card: Scored this Woolrich flannel on thredUp for just $22 and I'm obsessed with how it looks over my white ribbed tank and baggy jeans. Total 90s grunge mood with these combat boots. 🖤 #thrifted #grunge
- PASS 'leather belt under $15' -> lst_014 'Leather Belt — Brown, Braided' $12 thredUp
    price=Y platform=Y TITLE CHECK (confirm by eye): words matched ['leather', 'belt', 'braided']
    card: Scored this braided leather belt on thredUp for just $12 and it instantly pulled my baggy jeans and black denim jacket together. Such a good little Western touch for an everyday look. 🐎✨ #thriftyfinds #ootd
- PASS '90s slip dress size M' -> lst_013 '90s Silk Slip Dress — Floral, Midi Length' $30 depop
    price=Y platform=Y TITLE CHECK (confirm by eye): words matched ['silk', 'slip', 'floral']
    card: Scored this ivory floral silk slip on depop for just $30 and I’m obsessed. Layered it under my grey crewneck sweatshirt with chunky white sneakers for that 90s streetwear contrast. 🌸✨ #thrifted #90sfashion
- FAIL 'low-rise cargo pants' -> lst_011 'Low-Rise Cargo Pants — Khaki' $27 poshmark
    price=Y platform=Y TITLE CHECK (confirm by eye): words matched none
    card: Scored these on Poshmark for just $27 and I'm obsessed with the pockets. Throwing on my black combat boots and cropped zip hoodie makes them feel so early 2000s. 👖✨ #thrifted #y2kstyle
```

*Criterion 5, run 2.* From `results/capstone/trial2/score.md`. The advice is `outfit_suggestion` from `tools.py::suggest_outfit`, returned by `POST /ask` with `"wardrobe": {"items": []}`. The scorer also confirms the server received an empty wardrobe and didn't fall back to the example one.

```
- PASS 'vintage polo shirt': 7 sentences, status 200, wardrobe items on server=[], error=None
    advice: 'Outfit 1: Casual Streetwear\nPair the forest green polo with loose-fitting light wash straight-leg jeans. Tuck the polo in halfway and add a brown leather belt. Finish the look with white retro canvas sneakers and a simple silver chain necklace for an easy, everyday vibe.\n\nOutfit 2: Elevated Prep\nLayer the polo over a white cotton t-shirt so the collar peeks out, and wear it with a pleated navy blu'
- PASS 'platform sneakers': 6 sentences, status 200, wardrobe items on server=[], error=None
    advice: 'Outfit One: Cargo pants in army green or beige, a fitted black baby tee, and a nylon shoulder bag. The chunky white sneakers balance the utility pockets of the pants, and the fitted top keeps the silhouette from looking too bulky. Add silver hoop earrings to finish the Y2K look.\n\nOutfit Two: An oversized grey graphic hoodie worn as a dress with sheer black tights. The platform sneakers anchor the '
```

**Diagnoses**

*Criterion 1, MISSED (9/10 in run 1).*
- **Stage:** the model call inside `create_fit_card` (`generate.py::generate` → `google.genai`), combined with where `serve.py::ask` writes its record.
- **Mechanism:** the Gemini client had no timeout, so a slow response held the request open with no limit. gunicorn's sync worker has a 30 s timeout. At 30 s it killed the worker. Render shows `WORKER TIMEOUT (pid:58)` followed by "was sent SIGKILL! Perhaps out of memory?" That second message is gunicorn's generic wording, not a memory problem: the traceback shows the worker sitting in `ssl.read`, waiting for Gemini's response headers. `serve.py::ask` writes the log record only after `run_agent()` returns, so a request killed mid-run never reaches that line. My instrumentation logs every failure that raises, but not one that takes the whole process down.

*Criterion 2, MISSED (2/10, 7/10, 10/10).*
- **Stage:** the two Gemini calls, `suggest_outfit` and `create_fit_card`.
- **Mechanism:** the run splits into a fixed part and a variable part.
  - The fixed part is parsing plus MCP search, which starts a fresh `mcp_server.py` process every call. The no-match runs, which stop after search, took 4.7 s, 3.9 s and 4.4 s across the three runs, so this part is a steady ~4 s.
  - The variable part is the model. Median `ok` duration was 14.5 s in run 1, then 7.2 s in run 2 and 7.2 s in run 3. Run 1 was slow from its first request to its last (6.7–25.3 s), and run 2's first three were slow (14–17 s) before dropping to about 6.5 s.
  - Nothing in my system changed between runs, so the swing is Gemini's response time varying over a few minutes. With a 4 s floor, the 10 s target leaves only 6 s for two model calls. That holds when Gemini is quick and fails when it isn't.
- **What my criterion assumed:** that latency is a property of my system. It mostly belongs to the upstream service.

*Criterion 4, MISSED (4/5, 5/5, 4/5). Two different causes.*
- **Run 1, "90s slip dress":** no fit card at all. This is the same timeout as criterion 1.
- **Run 3, "low-rise cargo pants":** the card says "Scored these on Poshmark for just $27…" and never names the item.
  - **Stage:** the caption prompt in `tools.py::create_fit_card`.
  - **Mechanism:** the prompt says "Mention the item, the price and the platform". The price and platform are given as literal values to copy, but "the item" has no wording to copy. At temperature 0.9, the model sometimes meets "mention the item" with a pronoun.

**The pattern:** three of the four misses come from one place, the Gemini call:
- the criterion 1 miss and the run 1 criterion 4 miss are the same timed-out request
- criterion 2 is Gemini's latency variance

Only the run 3 cargo-pants caption has a separate cause, the prompt. The Gemini call is the one stage I don't control, and my system had no limit on how long it waited for it.

**The Improvement**

**What I changed:** I added a 12-second deadline to every Gemini call. It's one setting, `MODEL_TIMEOUT_S = 12` in `config.py`, passed to the client in `generate.py::_get_client` as `HttpOptions(timeout=12000)`. I also added a clearer message for that case in `generate.py::_explain`. It's committed in `3f12ef3`. Nothing else changed: same prompts, same agent, same start command, same trial script and requests.

**Why this, from the diagnosis:** three of my four misses traced to the Gemini call, and the worst one (criterion 1) happened because the call had no limit. gunicorn's 30 s timeout killed the worker before `serve.py::ask` could write its record. A per-call deadline turns a hang into an ordinary exception inside `run_agent()`. `serve.py` already catches exceptions, returns a JSON 500 and logs the record. The budget is about 4 s of parsing and MCP search (from the no-match runs) plus 2 × 12 s, at most 28 s, which is under gunicorn's 30. Gemini rejects deadlines under 10 s.

**Checking the mechanism directly:** to find out what really happens, I pointed the client at a local server that accepts the connection and never answers.
- **SDK behavior:** one attempt, `httpx.ReadTimeout` at 12.01 s, no hidden retries.
- **Through `serve.py`** (Flask test client), the request now leaves this record instead of a killed worker and nothing:

```json
{"ts": "2026-11-18T22:25:06.163+00:00", "request_id": "a7f31d78", "route": "/ask", "query": "leather belt under $15", "tools_run": [], "n_results": null, "selected_id": null, "fit_card": null, "wait_ms": 1, "api_calls": 1, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0, "status": 500, "outcome": "exception", "error": "ModelUnavailable: The model didn't answer within 12 s, so this request stopped instead of hanging. Try again in a moment.", "duration_ms": 13648}
```

**Run Log — After.** Same script and requests, three trials against the redeployed service on 2026-11-18, 22:28:57–22:35:15 UTC. Saved in `results/capstone/trial4` to `trial6`, with Render's stdout pasted into each.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Every query (7 good + 3 bad) leaves a `[request]` line in Render's log output | 10 of 10 | 10/10 | 10/10 | 10/10 | MET |
| 2. Warm `ok` runs finish within 10 s (server `duration_ms`) | 9 of 10 | 8/10 | 7/10 | 7/10 | MISSED |
| 3. `/logs` returns the latest 20 entries (or all if fewer), matching Render's stdout | 10 of 10 | 10/10 | 10/10 | 10/10 | MET |
| 4. Fit card names the item's title, price and platform (5 different queries) | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Empty wardrobe gets general advice of at least 2 sentences | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |

**Before and after**

| Criterion | Target | Before (runs 1 / 2 / 3) | Verdict | After (runs 1 / 2 / 3) | Verdict |
|---|---|---|---|---|---|
| 1. Every query logged | 10 of 10 | 9 / 10 / 10 | MISSED | 10 / 10 / 10 | MET |
| 2. Warm `ok` within 10 s | 9 of 10 | 2 / 7 / 10 | MISSED | 8 / 7 / 7 | MISSED |
| 3. `/logs` matches stdout | 10 of 10 | 10 / 10 / 10 | MET | 10 / 10 / 10 | MET |
| 4. Fit card title, price, platform | 5 of 5 | 4 / 5 / 4 | MISSED | 5 / 5 / 5 | MET |
| 5. Empty wardrobe advice | 5 of 5 | 5 / 5 / 5 | MET | 5 / 5 / 5 | MET |

Real output from the after-run. Criterion 2, run 3 (`results/capstone/trial6/score.md`, `duration_ms` from `serve.py::ask`'s records):

```
Warm-up: GET /health -> 200 in 145 ms (client)
- FAIL 'vintage graphic tee under $30'      duration_ms=10482  (client 10630 ms)
- PASS 'oversized flannel shirt'            duration_ms=9936  (client 10046 ms)
- PASS 'leather belt under $15'             duration_ms=6565  (client 6739 ms)
- PASS '90s slip dress size M'              duration_ms=6412  (client 6613 ms)
- PASS 'low-rise cargo pants'               duration_ms=6143  (client 6257 ms)
- PASS 'mesh long-sleeve top size S/M'      duration_ms=6548  (client 6768 ms)
- PASS 'crewneck sweatshirt under $25'      duration_ms=5798  (client 5907 ms)
- PASS 'faded band tee'                     duration_ms=6157  (client 6282 ms)
- FAIL 'graphic hoodie size L'              duration_ms=10739  (client 10877 ms)
- FAIL 'suede chelsea boots'                duration_ms=10237  (client 10358 ms)
```

Criterion 1: Render's stdout starts with the redeploy, and the first record follows:

```
2026-11-18T22:28:18.547324375Z ==> Your service is live 🎉
2026-11-18T22:29:14.415052571Z [request] {"ts": "2026-11-18T22:28:57.878+00:00", "request_id": "f72ae724", "route": "/ask", "query": "vintage graphic tee under $30", "tools_run": ["parse_query", "search_listings", "suggest_outfit", "create_fit_card"], "n_resul…
```

**Did it help?**
- **Criteria 1 and 4 went from MISSED to MET, but I can't credit the fix for that.** No call in the after-run came near 12 s. All 54 `/ask` requests returned 200 or the expected 400, with no timeouts and no `WORKER TIMEOUT` in Render's stdout. So the deadline never fired. Those two criteria passed because Gemini didn't stall this time, and in run 3 the caption happened to name the cargo pants. What shows the fix works is the forced-hang test above, not these trials. The honest result: the failure that cost criterion 1 now leaves a record (shown directly), but the live after-run never reproduced it.
- **Criterion 2 is still MISSED, and the fix wasn't aimed at it.** A deadline can't make Gemini faster. The after-run was steadier than before (worst run 7/10 instead of 2/10), but that's Gemini's speed at the time, not my change. No runs were replaced, so the deadline didn't flatter this criterion by dropping slow runs.
- **The trade-off:** a model call between 12 s and roughly 26 s, which used to finish slowly, now fails with a 500 at 12 s. Before the fix, trial 1's "faded band tee" succeeded in 25.3 s, and with the deadline it could have been an error. I chose a fast, logged failure over a slow success or a silent kill, because a run that leaves no record can't be diagnosed, and a user waiting 25 s has usually left anyway. It also means criterion 2's "replace non-`ok` runs" rule could hide slow runs in a future test, so the replacement count needs to be reported next to criterion 2.

**What's Still Broken**

*Criterion 2 (warm `ok` runs within 10 s): still MISSED, at 8/10, 7/10 and 7/10 after the fix.*
- **What I'd do:** split the latency before trying to cut it. Every request costs about 4 s before the model is called, because `mcp_client.call_tool` starts a fresh `mcp_server.py` process for every search (the no-match runs take 3.9–4.8 s and never touch the model). That's 4 s of a 10 s budget spent on process start-up. Keeping one MCP server process alive for the life of the gunicorn worker, instead of one per call, should take most of that away. The two Gemini calls could then take about 9 s together instead of 6 before a run crosses 10 s.
- **Why I stopped:** this unit allows one measured improvement, and I spent it on the deadline, because the timeout was the only failure that destroyed evidence. The MCP change also touches `mcp_client.py` and the one-request-at-a-time design in `serve.py`, which I put out of scope in The Shape.
- **Something I can't explain yet:** "vintage graphic tee under $30" is the slowest query in five of the six runs (median 16.7 s against about 6.5 s for most queries), with normal token counts. "Vintage polo shirt" returns the same 10 results and is fast, so result count isn't the cause. But it's also the first `/ask` in every trial, so I can't tell a slow query from a slow first request. The next test would shuffle the query order before changing anything.

*Criterion 4 (fit card names the title, price and platform): MET after the fix, but the cause I found is still there.*
- In before-run 3, the caption for the cargo pants said "Scored these on Poshmark…" without naming the item. The prompt in `tools.py::create_fit_card` gives the price and platform as literal values to copy but only says "mention the item". The after-run passed because the model happened to name the item every time, not because anything changed. I'd add the item's short name to the prompt the same way the price is given, and require it word for word. I stopped because it isn't an operational fix, and Shape A is about the operational layer.

*Criterion 1 (every query logged): MET, but the fix was never triggered live.* No Gemini call in the after-run came near 12 s, so the only evidence that a slow call now leaves a record is the forced-hang test in The Improvement. A failure that kills the process outright (out of memory, or a crash in gunicorn itself) would still leave no record, because `serve.py::ask` writes only when the request finishes. Writing a short "started" record before `run_agent()` would close that gap.

*Targets I'd tighten:*
- **Criterion 3 met 30 of 30** and never came close to failing. Its only realistic failure mode, a wipe between writing and reading, is excluded by the "unless it has fewer" clause. I'd tighten it to cover a sleep: after the service sleeps and wakes, `/logs` returns 0 records and the README already holds every record from before the sleep.
- **Criterion 5 met 30 of 30**, with every answer at 4–8 sentences. A 2-sentence minimum is far below what the model always produces. I'd require that the advice names at least two specific item types and mentions nothing from a wardrobe, since the wardrobe sent is empty.

**What I'd do first with another unit:** keep one MCP server process alive per worker instead of starting one per search. The ~4 s start-up is the only part of every request that's both under my control and a fixed cost, and removing it is the most direct way to bring criterion 2 within reach whatever Gemini's speed that day.

**How I Used AI**

1. **Grading the trials with `capstone_score.py`.** I asked Claude to run Milestone 5 against the live service. It wrote `capstone_trial.py`, which sends the same 30 requests every trial, and `capstone_score.py`, which grades each trial against criteria.md. In its first pass, the criterion 3 check marked trial 1 as a miss. Right after the timed-out "90s slip dress" request, the newest `/logs` record wasn't that request. But my criterion 3 only says `/logs` must return the latest entries *as compared against Render's stdout*, and stdout was missing that request too, because the worker was killed before either was written. The scorer was testing a rule I never wrote. Fixing that exposed a second bug: it compared my laptop's clock with Render's, so 0 ms bad requests looked like they arrived after the `/logs` call that read them. Claude caught both and changed the check to compare `/logs` against stdout in request order. The missing request stays counted under criterion 1, where it belongs. Criterion 3 came out 10/10 in every run, and criteria 1, 2, 4 and 5 didn't change. What I took from it: a grading script can quietly add its own criteria, so I read its rules against my wording, not just its totals.

2. **Choosing the timeout for the improvement.** My diagnosis traced criterion 1's miss to the Gemini call having no time limit: gunicorn killed the worker at 30 s before `serve.py` could log anything. I asked Claude to make one improvement from that. The first attempt to test a short deadline failed: Gemini rejected a 1-second deadline with "Minimum allowed deadline is 10s", so the timeout couldn't be set arbitrarily low. The number had to fit a budget instead. About 4 s of parsing and MCP search (from the no-match runs) plus two model calls must finish under gunicorn's 30 s, so 12 s per call gives at most 28 s. Before trusting it, Claude pointed the client at a local server that never answers, to check that the SDK doesn't retry silently and blow past 30 s. It made one attempt and raised `ReadTimeout` at 12.01 s, and through `serve.py` the hang became a logged 500 at 13.7 s. What changed in my thinking: the timeout isn't a "make it faster" setting. It turns a slow success into a fast, logged failure. That's the trade-off I wrote up in The Improvement, and it's why criterion 2 now has to report how many runs were replaced.
