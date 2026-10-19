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

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



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
