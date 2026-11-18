# Capstone trial 6: score

## Summary

| Criterion | Target | Result |
|---|---|---|
| 1. Every query logged in Render's output | 10 of 10 | 10/10 |
| 2. Warm ok runs within 10 s | 9 of 10 | 7/10 |
| 3. /logs returns latest 20, matching stdout | 10 of 10 | 10/10 |
| 4. Fit card names title, price, platform | 5 of 5 | 5/5 |
| 5. Empty wardrobe gets 2+ sentences of advice | 5 of 5 | 5/5 |

## Criterion 1: every query leaves a `[request]` line in Render's log output
- PASS good            'vintage graphic tee under $30'              -> request_id 7a1fc2cc, outcome ok
- PASS good            'oversized flannel shirt'                    -> request_id 6f8ea924, outcome ok
- PASS good            'leather belt under $15'                     -> request_id 238fff36, outcome ok
- PASS good            '90s slip dress size M'                      -> request_id c220ad38, outcome ok
- PASS good            'low-rise cargo pants'                       -> request_id 86923ce6, outcome ok
- PASS good            'mesh long-sleeve top size S/M'              -> request_id 99a2aaa6, outcome ok
- PASS good            'crewneck sweatshirt under $25'              -> request_id 92c6b4fd, outcome ok
- PASS malformed_json  '{not json'                                  -> request_id 322e37bf, outcome bad_request
- PASS empty_query     '{"query": "   "}'                           -> request_id 7b73835d, outcome bad_request
- PASS no_match        '{"query": "ballgown size XXS under $2"}'    -> request_id 93de72e1, outcome no_results

## Criterion 2: 9 of 10 warm `ok` runs finish within 10 s (server `duration_ms`)
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

## Criterion 3: /logs returns the latest 20 entries (or all, if fewer), matching Render's stdout
- PASS after vintage graphic tee under $30      20 records
- PASS after oversized flannel shirt            20 records
- PASS after leather belt under $15             20 records
- PASS after 90s slip dress size M              20 records
- PASS after low-rise cargo pants               20 records
- PASS after mesh long-sleeve top size S/M      20 records
- PASS after crewneck sweatshirt under $25      20 records
- PASS after malformed_json                     20 records
- PASS after empty_query                        20 records
- PASS after no_match                           20 records

## Criterion 4: fit card names the item's title, price and platform
- PASS 'vintage graphic tee under $30' -> lst_002 'Y2K Baby Tee — Butterfly Print' $18 depop
    price=Y platform=Y TITLE CHECK (confirm by eye): words matched ['tee', 'butterfly']
    card: Scored this little butterfly tee on depop for just $18 and I'm obsessed. Paired it with baggy straight-leg jeans and a black denim jacket to balance out the tiny fit. 🦋 #y2kstyle #thrifty
- PASS 'oversized flannel shirt' -> lst_003 'Oversized Flannel Shirt — Plaid Red/Black' $22 thredUp
    price=Y platform=Y TITLE CHECK (confirm by eye): words matched ['flannel', 'red']
    card: Found this Woolrich flannel on thredUp for $22 and it’s the ultimate 90s grunge layer over my white ribbed tank and combat boots. Honestly obsessed with how heavy and worn-in it feels. 🖤 #thrifted #grunge
- PASS 'leather belt under $15' -> lst_014 'Leather Belt — Brown, Braided' $12 thredUp
    price=Y platform=Y TITLE CHECK (confirm by eye): words matched ['leather', 'belt', 'braided']
    card: Found this braided leather belt on thredUp for only $12 and I've already worn it two ways. It totally pulls together the white ribbed tank and baggy dark jeans, but I also love how it cinches my wide-leg khaki trousers. So good for adding a little western touch to basic outfits. 🤎🤠 #thrifted #secondhandstyle
- PASS '90s slip dress size M' -> lst_013 '90s Silk Slip Dress — Floral, Midi Length' $30 depop
    price=Y platform=Y TITLE CHECK (confirm by eye): words matched ['silk', 'slip', 'floral']
    card: Found this floral silk slip on depop for $30 and I’m obsessed with how it looks layered right under an oversized grey crewneck sweatshirt. Paired it with my black combat boots to keep the 90s contrast going strong. 🥀✨ #thrifty #90sstyle
- PASS 'low-rise cargo pants' -> lst_011 'Low-Rise Cargo Pants — Khaki' $27 poshmark
    price=Y platform=Y TITLE CHECK (confirm by eye): words matched ['low', 'rise', 'cargo', 'pants']
    card: Scored these low-rise cargo pants on Poshmark for $27 and I'm obsessed with the slouchy fit. Paired them with my chunky white sneakers and a black cropped zip hoodie for a full 2000s street look. 👖✨ #y2k #streetwear

## Criterion 5: empty wardrobe gets general advice of at least 2 sentences
- PASS 'vintage polo shirt': 4 sentences, status 200, wardrobe items on server=[], error=None
    advice: 'Outfit One: High-waisted straight-leg light wash jeans, a brown leather belt, and cream canvas low-top sneakers. Tuck the polo in completely to lean into the vintage preppy look, and add a simple silver wristwatch to finish it off.\n\nOutfit Two: Pleated khaki or beige midi skirt with black leather loafers and white crew socks. Leave the polo untucked to play with the slightly boxy fit, and throw on'
- PASS 'platform sneakers': 4 sentences, status 200, wardrobe items on server=[], error=None
    advice: 'Outfit One: Pair the sneakers with baggy light-wash cargo pants and a black ribbed baby tee. Add a nylon shoulder bag and small hoop earrings to lean into the authentic Y2K streetwear vibe.\n\nOutfit Two: Contrast the chunky shoes with a grey marled crewneck sweatshirt and a black pleated tennis skirt. Throw on white crew socks to bridge the gap between the skirt and the yellowed soles, giving it a '
- PASS 'linen blazer': 6 sentences, status 200, wardrobe items on server=[], error=None
    advice: 'Outfit one: Pair the cream blazer with a fitted black ribbed tank top and high-waisted straight-leg medium wash jeans. Add a brown leather belt, simple gold hoop earrings, and canvas low-top sneakers or leather loafers. This keeps the look grounded and effortless for daytime.\n\nOutfit two: Layer the blazer over a simple white cotton t-shirt tucked into a flowy black midi skirt. Slip on black leathe'
- PASS 'tie-dye long sleeve': 6 sentences, status 200, wardrobe items on server=[], error=None
    advice: 'Outfit One: Contrast the pastel softness with structure. Tuck the oversized tie-dye shirt into high-waisted, medium-wash straight-leg jeans with a brown leather belt. Finish with clean white canvas low-top sneakers and a simple silver pendant necklace to ground the colorful top.\n\nOutfit Two: Lean into streetwear comfort. Layer the long sleeve over a fitted white ribbed tank top, leaving the collar'
- PASS 'corduroy wide-leg pants': 8 sentences, status 200, wardrobe items on server=[], error=None
    advice: 'Outfit One: Coffee and Thrifting\nPair the rust cords with a fitted black ribbed turtleneck tucked in to balance the wide leg. Throw on an oversized cream cable-knit cardigan and finish with brown leather Chelsea boots. Add a structured canvas tote bag for an easy daytime errand look.\n\nOutfit Two: Autumn Picnic\nTuck a vintage white cotton button-down blouse with ruffled collar details into the high'
