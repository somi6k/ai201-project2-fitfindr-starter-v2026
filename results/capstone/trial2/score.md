# Capstone trial 2: score

## Summary

| Criterion | Target | Result |
|---|---|---|
| 1. Every query logged in Render's output | 10 of 10 | 10/10 |
| 2. Warm ok runs within 10 s | 9 of 10 | 7/10 |
| 3. /logs returns latest 20, matching stdout | 10 of 10 | 10/10 |
| 4. Fit card names title, price, platform | 5 of 5 | 5/5 |
| 5. Empty wardrobe gets 2+ sentences of advice | 5 of 5 | 5/5 |

## Criterion 1: every query leaves a `[request]` line in Render's log output
- PASS good            'vintage graphic tee under $30'              -> request_id e535967b, outcome ok
- PASS good            'oversized flannel shirt'                    -> request_id 6f0f0965, outcome ok
- PASS good            'leather belt under $15'                     -> request_id b90ca01d, outcome ok
- PASS good            '90s slip dress size M'                      -> request_id 07e90de7, outcome ok
- PASS good            'low-rise cargo pants'                       -> request_id 1d018957, outcome ok
- PASS good            'mesh long-sleeve top size S/M'              -> request_id c3085b8e, outcome ok
- PASS good            'crewneck sweatshirt under $25'              -> request_id 03a312c5, outcome ok
- PASS malformed_json  '{not json'                                  -> request_id 7da4f4af, outcome bad_request
- PASS empty_query     '{"query": "   "}'                           -> request_id 4a226307, outcome bad_request
- PASS no_match        '{"query": "ballgown size XXS under $2"}'    -> request_id 1827e4f9, outcome no_results

## Criterion 2: 9 of 10 warm `ok` runs finish within 10 s (server `duration_ms`)
Warm-up: GET /health -> 200 in 280 ms (client)
- FAIL 'vintage graphic tee under $30'      duration_ms=16904  (client 17053 ms)
- FAIL 'oversized flannel shirt'            duration_ms=15347  (client 15578 ms)
- FAIL 'leather belt under $15'             duration_ms=14322  (client 14453 ms)
- PASS '90s slip dress size M'              duration_ms=6257  (client 6394 ms)
- PASS 'low-rise cargo pants'               duration_ms=6553  (client 6800 ms)
- PASS 'mesh long-sleeve top size S/M'      duration_ms=7230  (client 7364 ms)
- PASS 'crewneck sweatshirt under $25'      duration_ms=6659  (client 6910 ms)
- PASS 'faded band tee'                     duration_ms=6454  (client 6694 ms)
- PASS 'graphic hoodie size L'              duration_ms=8044  (client 8208 ms)
- PASS 'suede chelsea boots'                duration_ms=6669  (client 6873 ms)

## Criterion 3: /logs returns the latest 20 entries (or all, if fewer), matching Render's stdout
- PASS after vintage graphic tee under $30      19 records
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
    price=Y platform=Y TITLE CHECK (confirm by eye): words matched ['baby', 'tee']
    card: Scored this cute little baby tee on depop for only $18 and I am obsessed. Paired it with some baggy straight-leg jeans and my favorite chunky white sneakers for the ultimate early 2000s street fit. 🦋✨ #y2k #thrifted
- PASS 'oversized flannel shirt' -> lst_003 'Oversized Flannel Shirt — Plaid Red/Black' $22 thredUp
    price=Y platform=Y TITLE CHECK (confirm by eye): words matched ['flannel', 'red']
    card: Found this Woolrich flannel on thredUp for $22 and I’m obsessed with how it looks thrown open over a ribbed tank and baggy jeans. Total 90s grunge mode with these combat boots. 🖤 #thrifted #90sstyle
- PASS 'leather belt under $15' -> lst_014 'Leather Belt — Brown, Braided' $12 thredUp
    price=Y platform=Y TITLE CHECK (confirm by eye): words matched ['leather', 'belt', 'braided']
    card: Found this braided leather belt on thredUp for only $12 and it instantly pulled my wide-leg khaki trousers and black combat boots together. Such an easy little detail to tie an earth tone fit together. 🤎🤠 #thrifted #streetstyle
- PASS '90s slip dress size M' -> lst_013 '90s Silk Slip Dress — Floral, Midi Length' $30 depop
    price=Y platform=Y TITLE CHECK (confirm by eye): words matched ['silk', 'slip', 'dress']
    card: Scored this vintage silk slip dress on depop for only $30 and I’m obsessed. Layered it under my baggy dark wash jeans and a chunky grey crewneck for that classic grungy 90s look 🥀✨ #thrifthaul #9style
- PASS 'low-rise cargo pants' -> lst_011 'Low-Rise Cargo Pants — Khaki' $27 poshmark
    price=Y platform=Y TITLE CHECK (confirm by eye): words matched ['cargo', 'khaki']
    card: Scored these khaki cargos on Poshmark for $27 and I’m obsessed with the Y2K streetwear vibe. Throwing on a white ribbed tank, black denim jacket, and chunky sneakers makes them look so effortless. 👖✨ #thrifted #y2kstyle

## Criterion 5: empty wardrobe gets general advice of at least 2 sentences
- PASS 'vintage polo shirt': 7 sentences, status 200, wardrobe items on server=[], error=None
    advice: 'Outfit 1: Casual Streetwear\nPair the forest green polo with loose-fitting light wash straight-leg jeans. Tuck the polo in halfway and add a brown leather belt. Finish the look with white retro canvas sneakers and a simple silver chain necklace for an easy, everyday vibe.\n\nOutfit 2: Elevated Prep\nLayer the polo over a white cotton t-shirt so the collar peeks out, and wear it with a pleated navy blu'
- PASS 'platform sneakers': 6 sentences, status 200, wardrobe items on server=[], error=None
    advice: 'Outfit One: Cargo pants in army green or beige, a fitted black baby tee, and a nylon shoulder bag. The chunky white sneakers balance the utility pockets of the pants, and the fitted top keeps the silhouette from looking too bulky. Add silver hoop earrings to finish the Y2K look.\n\nOutfit Two: An oversized grey graphic hoodie worn as a dress with sheer black tights. The platform sneakers anchor the '
- PASS 'linen blazer': 6 sentences, status 200, wardrobe items on server=[], error=None
    advice: 'Outfit one: Pair the blazer with relaxed white cotton trousers for a tonal, breezy summer look. Layer it over a fitted black tank top to add contrast and anchor the lightness of the linen. Finish with brown leather slide sandals and a simple leather shoulder bag.\n\nOutfit two: Dress down the blazer by wearing it over a striped long-sleeve cotton t-shirt. Pair with high-waisted straight-leg blue den'
- PASS 'tie-dye long sleeve': 7 sentences, status 200, wardrobe items on server=[], error=None
    advice: 'Outfit one leans into streetwear. Pair the pastel tie-dye long sleeve with baggy, high-waisted medium-wash denim jeans and scuffed white canvas low-top sneakers. Add a plain black nylon crossbody bag and a silver chain necklace to ground the soft colors with a little edge.\n\nOutfit two plays up the cozy, casual side. Layer the oversized top over black biker shorts. Finish the look with chunky white'
- PASS 'corduroy wide-leg pants': 6 sentences, status 200, wardrobe items on server=[], error=None
    advice: 'Outfit one: Tuck a plain cream ribbed turtleneck into the pants. Add a vintage brown leather belt and chunky brown lace-up ankle boots. Layer an oversized plaid wool blazer over top in tones of brown and tan. \n\nOutfit two: Pair the cords with a tucked-in black vintage band t-shirt with a faded graphic. Throw on a distressed oversized denim jacket and black canvas low-top sneakers. Accessorize with'
