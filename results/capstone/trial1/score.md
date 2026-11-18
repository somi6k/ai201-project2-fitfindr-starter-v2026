# Capstone trial 1: score

## Summary

| Criterion | Target | Result |
|---|---|---|
| 1. Every query logged in Render's output | 10 of 10 | 9/10 |
| 2. Warm ok runs within 10 s | 9 of 10 | 2/10 |
| 3. /logs returns latest 20, matching stdout | 10 of 10 | 10/10 |
| 4. Fit card names title, price, platform | 5 of 5 | 4/5 |
| 5. Empty wardrobe gets 2+ sentences of advice | 5 of 5 | 5/5 |

## Criterion 1: every query leaves a `[request]` line in Render's log output
- PASS good            'vintage graphic tee under $30'              -> request_id 660920ac, outcome ok
- PASS good            'oversized flannel shirt'                    -> request_id 83c93b5f, outcome ok
- PASS good            'leather belt under $15'                     -> request_id 467682af, outcome ok
- FAIL good            '90s slip dress size M'                      -> no matching line
- PASS good            'low-rise cargo pants'                       -> request_id cf1245b6, outcome ok
- PASS good            'mesh long-sleeve top size S/M'              -> request_id 6a14e35b, outcome ok
- PASS good            'crewneck sweatshirt under $25'              -> request_id a791c1ec, outcome ok
- PASS malformed_json  '{not json'                                  -> request_id cedd8daa, outcome bad_request
- PASS empty_query     '{"query": "   "}'                           -> request_id 3287ffa8, outcome bad_request
- PASS no_match        '{"query": "ballgown size XXS under $2"}'    -> request_id 7a6410aa, outcome no_results

## Criterion 2: 9 of 10 warm `ok` runs finish within 10 s (server `duration_ms`)
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

## Criterion 3: /logs returns the latest 20 entries (or all, if fewer), matching Render's stdout
- PASS after vintage graphic tee under $30      1 records
- PASS after oversized flannel shirt            2 records
- PASS after leather belt under $15             3 records
- PASS after 90s slip dress size M              3 records  [note: the request just sent has no record in /logs OR stdout]
- PASS after low-rise cargo pants               4 records
- PASS after mesh long-sleeve top size S/M      5 records
- PASS after crewneck sweatshirt under $25      6 records
- PASS after malformed_json                     7 records
- PASS after empty_query                        8 records
- PASS after no_match                           9 records

## Criterion 4: fit card names the item's title, price and platform
- PASS 'vintage graphic tee under $30' -> lst_002 'Y2K Baby Tee — Butterfly Print' $18 depop
    price=Y platform=Y TITLE CHECK (confirm by eye): words matched ['baby', 'tee', 'butterfly']
    card: Scored this butterfly baby tee on depop for only $18 and I’m obsessed. Wearing it today under a cropped black zip hoodie with baggy dark wash jeans and chunky sneakers. 🦋✨ #y2k #thrifthaul
- PASS 'oversized flannel shirt' -> lst_003 'Oversized Flannel Shirt — Plaid Red/Black' $22 thredUp
    price=Y platform=Y TITLE CHECK (confirm by eye): words matched ['flannel', 'red']
    card: Scored this vintage Woolrich flannel for $22 on thredUp and it’s basically been my jacket all week. Tossed it on over a white ribbed tank and straight-leg jeans with some combat boots for a total 90s grunge vibe. 🖤🪵 #thrifted #grunge
- PASS 'leather belt under $15' -> lst_014 'Leather Belt — Brown, Braided' $12 thredUp
    price=Y platform=Y TITLE CHECK (confirm by eye): words matched ['leather', 'belt', 'braided']
    card: Found this braided leather belt on thredUp for only $12 and it instantly pulled my baggy jeans and white tank look together. It adds just the right western touch to break up the denim-on-denim vibe. 🤎 #thriftfind
- FAIL '90s slip dress size M': no fit card (status 500, error None)
- PASS 'low-rise cargo pants' -> lst_011 'Low-Rise Cargo Pants — Khaki' $27 poshmark
    price=Y platform=Y TITLE CHECK (confirm by eye): words matched ['low', 'rise', 'cargo', 'pants']
    card: Scored these low-rise cargo pants on Poshmark for $27 and I'm obsessed with the pockets. Threw them on with a white ribbed tank top and chunky white sneakers for an easy streetwear vibe. 👖✨ #thrifted #y2kstyle

## Criterion 5: empty wardrobe gets general advice of at least 2 sentences
- PASS 'vintage polo shirt': 7 sentences, status 200, wardrobe items on server=[], error=None
    advice: 'Outfit one: Pair the forest green polo with straight-leg light wash jeans. Tuck the polo in loosely. Add a simple brown leather belt and white canvas low-top sneakers. Throw on a canvas tote bag to finish the casual, everyday campus look.\n\nOutfit two: Layer the polo over a white cotton t-shirt with the collar popped slightly. Wear it with wide-leg pleated beige chinos and dark brown leather loafer'
- PASS 'platform sneakers': 4 sentences, status 200, wardrobe items on server=[], error=None
    advice: 'Outfit One: Pair the sneakers with baggy light-wash denim carpenter jeans and a fitted ribbed black baby tee. Throw on a nylon shoulder bag and small rectangle sunglasses to lean into the authentic Y2K streetwear vibe.\n\nOutfit Two: Contrast the chunky white shoes by wearing them with an olive green cargo mini skirt and a heather grey oversized crewneck sweatshirt. Add white crew socks with a subtl'
- PASS 'linen blazer': 7 sentences, status 200, wardrobe items on server=[], error=None
    advice: 'Outfit One: Casual Weekend. Pair the blazer with a ribbed white cotton tank top, relaxed-fit medium wash blue jeans, and brown leather slip-on sandals. Add a woven straw tote bag and simple gold hoop earrings for an easy daytime look that feels put-together without trying too hard.\n\nOutfit Two: Warm Weather Dinner. Layer the blazer over a simple black midi-length slip dress. Finish the look with b'
- PASS 'tie-dye long sleeve': 8 sentences, status 200, wardrobe items on server=[], error=None
    advice: 'Outfit One: Streetwear Contrast. Pair the pastel tie-dye top with baggy carpenter denim in a worn charcoal grey. Tuck in just the front. Add chunky white skate sneakers and a plain black canvas crossbody bag to ground the soft colors.\n\nOutfit Two: Cozy Layering. Wear the top loose over black ribbed biker shorts. Layer an oversized black zip-up hoodie half-zipped on top, letting the pastel sleeves '
- PASS 'corduroy wide-leg pants': 8 sentences, status 200, wardrobe items on server=[], error=None
    advice: 'Outfit one is for everyday. Tuck a fitted black ribbed turtleneck into the pants. Add brown leather ankle boots and a cropped denim jacket. Layer a few simple gold chains to finish the look. \n\nOutfit two is for a softer vibe. Pair the rust cords with an oversized cream cable-knit crewneck sweater, leaving it untucked for a relaxed fit. Slip on brown leather clogs or retro-style canvas sneakers. Th'
