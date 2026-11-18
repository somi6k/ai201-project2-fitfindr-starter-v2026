# Capstone trial 4: score

## Summary

| Criterion | Target | Result |
|---|---|---|
| 1. Every query logged in Render's output | 10 of 10 | 10/10 |
| 2. Warm ok runs within 10 s | 9 of 10 | 8/10 |
| 3. /logs returns latest 20, matching stdout | 10 of 10 | 10/10 |
| 4. Fit card names title, price, platform | 5 of 5 | 5/5 |
| 5. Empty wardrobe gets 2+ sentences of advice | 5 of 5 | 5/5 |

## Criterion 1: every query leaves a `[request]` line in Render's log output
- PASS good            'vintage graphic tee under $30'              -> request_id f72ae724, outcome ok
- PASS good            'oversized flannel shirt'                    -> request_id 135cf31e, outcome ok
- PASS good            'leather belt under $15'                     -> request_id 98a2d043, outcome ok
- PASS good            '90s slip dress size M'                      -> request_id cb8a16a7, outcome ok
- PASS good            'low-rise cargo pants'                       -> request_id 3f851807, outcome ok
- PASS good            'mesh long-sleeve top size S/M'              -> request_id 28283856, outcome ok
- PASS good            'crewneck sweatshirt under $25'              -> request_id bf079491, outcome ok
- PASS malformed_json  '{not json'                                  -> request_id 2d526a9d, outcome bad_request
- PASS empty_query     '{"query": "   "}'                           -> request_id 773713c9, outcome bad_request
- PASS no_match        '{"query": "ballgown size XXS under $2"}'    -> request_id 82ec6ded, outcome no_results

## Criterion 2: 9 of 10 warm `ok` runs finish within 10 s (server `duration_ms`)
Warm-up: GET /health -> 200 in 205 ms (client)
- FAIL 'vintage graphic tee under $30'      duration_ms=16537  (client 16655 ms)
- PASS 'oversized flannel shirt'            duration_ms=5681  (client 5806 ms)
- PASS 'leather belt under $15'             duration_ms=5911  (client 6126 ms)
- PASS '90s slip dress size M'              duration_ms=5654  (client 5781 ms)
- PASS 'low-rise cargo pants'               duration_ms=6229  (client 6360 ms)
- PASS 'mesh long-sleeve top size S/M'      duration_ms=5257  (client 5517 ms)
- PASS 'crewneck sweatshirt under $25'      duration_ms=6107  (client 6232 ms)
- FAIL 'faded band tee'                     duration_ms=17301  (client 17416 ms)
- PASS 'graphic hoodie size L'              duration_ms=7369  (client 7545 ms)
- PASS 'suede chelsea boots'                duration_ms=5761  (client 5881 ms)

## Criterion 3: /logs returns the latest 20 entries (or all, if fewer), matching Render's stdout
- PASS after vintage graphic tee under $30      1 records
- PASS after oversized flannel shirt            2 records
- PASS after leather belt under $15             3 records
- PASS after 90s slip dress size M              4 records
- PASS after low-rise cargo pants               5 records
- PASS after mesh long-sleeve top size S/M      6 records
- PASS after crewneck sweatshirt under $25      7 records
- PASS after malformed_json                     8 records
- PASS after empty_query                        9 records
- PASS after no_match                           10 records

## Criterion 4: fit card names the item's title, price and platform
- PASS 'vintage graphic tee under $30' -> lst_002 'Y2K Baby Tee — Butterfly Print' $18 depop
    price=Y platform=Y TITLE CHECK (confirm by eye): words matched ['baby', 'tee', 'butterfly', 'print']
    card: Scored this butterfly print baby tee on depop for only $18 and I'm obsessed. Paired it with baggy straight-leg jeans and a cropped zip hoodie for a full-on throwback fit 🦋 #y2k #thrifthaul
- PASS 'oversized flannel shirt' -> lst_003 'Oversized Flannel Shirt — Plaid Red/Black' $22 thredUp
    price=Y platform=Y TITLE CHECK (confirm by eye): words matched ['flannel', 'red']
    card: Scored this Woolrich flannel on thredUp for $22 and I am never taking it off. Stacking it over a cropped hoodie with chunky white sneakers gives it the exact 90s streetwear energy I wanted. 🖤✨ #thrifty #grunge
- PASS 'leather belt under $15' -> lst_014 'Leather Belt — Brown, Braided' $12 thredUp
    price=Y platform=Y TITLE CHECK (confirm by eye): words matched ['belt']
    card: Scored this vintage western belt on thredUp for just $12 and I'm obsessed with how it looks over my grey crewneck. It adds the exact right texture to my baggy jeans and white tank. 🤎 #thriftyfinds #ootd
- PASS '90s slip dress size M' -> lst_013 '90s Silk Slip Dress — Floral, Midi Length' $30 depop
    price=Y platform=Y TITLE CHECK (confirm by eye): words matched ['silk', 'slip', 'dress', 'floral']
    card: Scored this floral silk slip dress on depop for just $30 and I’m obsessed. Layered it under my grey crewneck sweatshirt and toughened it up with some combat boots. 🥀 #90sfashion
- PASS 'low-rise cargo pants' -> lst_011 'Low-Rise Cargo Pants — Khaki' $27 poshmark
    price=Y platform=Y TITLE CHECK (confirm by eye): words matched ['low', 'rise', 'cargo', 'khaki']
    card: Scored these low-rise khaki cargos on Poshmark for $27 and I'm obsessed with the pockets. Paired them with my favorite white ribbed tank and a black cropped zip hoodie for total Y2K vibes. 👖✨ #thriftfind #y2kstyle

## Criterion 5: empty wardrobe gets general advice of at least 2 sentences
- PASS 'vintage polo shirt': 6 sentences, status 200, wardrobe items on server=[], error=None
    advice: 'Outfit one: Tuck the forest green polo into high-waisted, wide-leg cream trousers. Add a brown leather belt and vintage brown leather loafers. Throw on a tortoiseshell watch to keep the preppy vibe grounded and sharp for a casual office or weekend brunch.\n\nOutfit two: Wear it untucked over straight-leg medium-wash jeans with a slight relaxed fit. Layer an open oversized cream canvas chore jacket o'
- PASS 'platform sneakers': 6 sentences, status 200, wardrobe items on server=[], error=None
    advice: 'Outfit one leans into the Y2K streetwear vibe. Pair the sneakers with a ribbed baby tee in black or pastel pink, and loose-fitting cargo pants in olive green or grey. Add a small nylon shoulder bag and wire-rim sunglasses to finish the look.\n\nOutfit two tones down the chunky silhouette with casual basics. Wear them with straight-leg light wash jeans, a slightly oversized white crewneck t-shirt, an'
- PASS 'linen blazer': 7 sentences, status 200, wardrobe items on server=[], error=None
    advice: 'Outfit one: Wear the blazer over a fitted plain black cotton t-shirt. Pair with relaxed-fit, light-wash blue denim jeans. Finish with brown leather loafers and a simple canvas tote bag. This gives an easy, high-contrast casual look.\n\nOutfit two: Layer it over a ribbed white tank top tucked into a lightweight olive green midi skirt. Add dark brown leather sandals and a woven straw shoulder bag. Thi'
- PASS 'tie-dye long sleeve': 7 sentences, status 200, wardrobe items on server=[], error=None
    advice: 'Outfit One: Streetwear Contrast. Pair the pastel oversized tie-dye top with baggy carpenter cargo pants in washed black or charcoal grey. Add chunky white leather skate sneakers and a simple silver chain necklace to ground the soft colors with an edgy, utilitarian base.\n\nOutfit Two: Soft Layers. Wear the top tucked loosely into a cream-colored corduroy mini skirt. Layer an oversized vintage brown '
- PASS 'corduroy wide-leg pants': 6 sentences, status 200, wardrobe items on server=[], error=None
    advice: 'Outfit one: Pair the rust cords with a fitted black ribbed turtleneck tucked into the high waist. Add a brown leather belt, a slouchy tan cardigan, and chunky black leather ankle boots. Finish with a simple canvas tote bag for an easy everyday look.\n\nOutfit two: Style the pants with a tucked-in oversized cream crewneck sweater. Layer a vintage-style denim jacket over top. Slip on a pair of retro w'
