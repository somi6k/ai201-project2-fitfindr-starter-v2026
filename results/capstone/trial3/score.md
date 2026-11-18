# Capstone trial 3: score

## Summary

| Criterion | Target | Result |
|---|---|---|
| 1. Every query logged in Render's output | 10 of 10 | 10/10 |
| 2. Warm ok runs within 10 s | 9 of 10 | 10/10 |
| 3. /logs returns latest 20, matching stdout | 10 of 10 | 10/10 |
| 4. Fit card names title, price, platform | 5 of 5 | 4/5 |
| 5. Empty wardrobe gets 2+ sentences of advice | 5 of 5 | 5/5 |

## Criterion 1: every query leaves a `[request]` line in Render's log output
- PASS good            'vintage graphic tee under $30'              -> request_id 232581fa, outcome ok
- PASS good            'oversized flannel shirt'                    -> request_id c64b6ee6, outcome ok
- PASS good            'leather belt under $15'                     -> request_id d25eeddb, outcome ok
- PASS good            '90s slip dress size M'                      -> request_id cc46582b, outcome ok
- PASS good            'low-rise cargo pants'                       -> request_id 05939f79, outcome ok
- PASS good            'mesh long-sleeve top size S/M'              -> request_id 1d8cbbd8, outcome ok
- PASS good            'crewneck sweatshirt under $25'              -> request_id a22f6384, outcome ok
- PASS malformed_json  '{not json'                                  -> request_id 473fc40a, outcome bad_request
- PASS empty_query     '{"query": "   "}'                           -> request_id cd492b3f, outcome bad_request
- PASS no_match        '{"query": "ballgown size XXS under $2"}'    -> request_id 65cda8f6, outcome no_results

## Criterion 2: 9 of 10 warm `ok` runs finish within 10 s (server `duration_ms`)
Warm-up: GET /health -> 200 in 172 ms (client)
- PASS 'vintage graphic tee under $30'      duration_ms=5643  (client 5776 ms)
- PASS 'oversized flannel shirt'            duration_ms=7611  (client 7745 ms)
- PASS 'leather belt under $15'             duration_ms=6692  (client 6821 ms)
- PASS '90s slip dress size M'              duration_ms=9863  (client 9971 ms)
- PASS 'low-rise cargo pants'               duration_ms=7108  (client 7352 ms)
- PASS 'mesh long-sleeve top size S/M'      duration_ms=6365  (client 6500 ms)
- PASS 'crewneck sweatshirt under $25'      duration_ms=7174  (client 7451 ms)
- PASS 'faded band tee'                     duration_ms=6751  (client 6876 ms)
- PASS 'graphic hoodie size L'              duration_ms=6363  (client 6609 ms)
- PASS 'suede chelsea boots'                duration_ms=7493  (client 7640 ms)

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

## Criterion 5: empty wardrobe gets general advice of at least 2 sentences
- PASS 'vintage polo shirt': 8 sentences, status 200, wardrobe items on server=[], error=None
    advice: 'Outfit One: Skate Casual\nPair the polo with loose-fitting light wash denim jeans and a beat-up pair of canvas low-top sneakers in white. Add a simple black leather belt and a silver chain necklace to break up the green and blue. Throw on an unstructured canvas tote bag for daily errands.\n\nOutfit Two: Prep School Contrast\nWear the polo tucked into a pleated navy blue mini skirt or relaxed khaki tro'
- PASS 'platform sneakers': 4 sentences, status 200, wardrobe items on server=[], error=None
    advice: 'Outfit One: Pair the sneakers with baggy light-wash denim carpenter jeans and a fitted ribbed black baby tee. Throw on a nylon shoulder bag and small rectangle sunglasses to lean into the authentic Y2K streetwear vibe.\n\nOutfit Two: Contrast the chunky sneakers with an oversized grey zip-up hoodie worn over black biker shorts. Add white crew socks scrunched down around the ankles and a canvas tote '
- PASS 'linen blazer': 7 sentences, status 200, wardrobe items on server=[], error=None
    advice: 'Outfit One: Casual Weekend. Pair the blazer with a ribbed white tank top, relaxed-fit straight-leg blue jeans, and well-worn brown leather loafers. Add a canvas tote bag and minimal gold hoop earrings for an easy, textured daytime look.\n\nOutfit Two: Warm Weather Dinner. Layer the blazer over a simple black cotton midi slip dress. Ground the outfit with flat black leather slide sandals and a woven '
- PASS 'tie-dye long sleeve': 6 sentences, status 200, wardrobe items on server=[], error=None
    advice: 'Outfit one leans into the oversized streetwear vibe. Pair the pastel tie-dye long sleeve with relaxed-fit light wash denim jeans and chunky white leather sneakers. Add a plain baseball cap and a canvas crossbody bag to finish the casual, easy look.\n\nOutfit two balances the colors for a softer, textured style. Layer the top half-tucked into an olive green utility skirt or straight-leg cargo pants. '
- PASS 'corduroy wide-leg pants': 6 sentences, status 200, wardrobe items on server=[], error=None
    advice: 'Outfit one: Tuck a fitted black ribbed turtleneck into the pants. Add a pair of dark brown leather ankle boots and a structured tan leather shoulder bag. Layer a cream-colored wool cardigan over top for chilly days. \n\nOutfit two: Pair the cords with an oversized white button-down shirt, worn unbuttoned at the top with the front loosely tucked in. Slip on a pair of retro canvas sneakers in off-whit'
