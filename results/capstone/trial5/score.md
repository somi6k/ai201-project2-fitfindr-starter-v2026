# Capstone trial 5: score

## Summary

| Criterion | Target | Result |
|---|---|---|
| 1. Every query logged in Render's output | 10 of 10 | 10/10 |
| 2. Warm ok runs within 10 s | 9 of 10 | 7/10 |
| 3. /logs returns latest 20, matching stdout | 10 of 10 | 10/10 |
| 4. Fit card names title, price, platform | 5 of 5 | 5/5 |
| 5. Empty wardrobe gets 2+ sentences of advice | 5 of 5 | 5/5 |

## Criterion 1: every query leaves a `[request]` line in Render's log output
- PASS good            'vintage graphic tee under $30'              -> request_id a6a77548, outcome ok
- PASS good            'oversized flannel shirt'                    -> request_id 98924dc9, outcome ok
- PASS good            'leather belt under $15'                     -> request_id 828d3fec, outcome ok
- PASS good            '90s slip dress size M'                      -> request_id 34ad771b, outcome ok
- PASS good            'low-rise cargo pants'                       -> request_id 1251578f, outcome ok
- PASS good            'mesh long-sleeve top size S/M'              -> request_id 61d6141b, outcome ok
- PASS good            'crewneck sweatshirt under $25'              -> request_id a5cd2613, outcome ok
- PASS malformed_json  '{not json'                                  -> request_id 94f41473, outcome bad_request
- PASS empty_query     '{"query": "   "}'                           -> request_id 8ddf9092, outcome bad_request
- PASS no_match        '{"query": "ballgown size XXS under $2"}'    -> request_id f2f7ea81, outcome no_results

## Criterion 2: 9 of 10 warm `ok` runs finish within 10 s (server `duration_ms`)
Warm-up: GET /health -> 200 in 270 ms (client)
- FAIL 'vintage graphic tee under $30'      duration_ms=17669  (client 17918 ms)
- PASS 'oversized flannel shirt'            duration_ms=6080  (client 6182 ms)
- PASS 'leather belt under $15'             duration_ms=6343  (client 6476 ms)
- PASS '90s slip dress size M'              duration_ms=6381  (client 6487 ms)
- PASS 'low-rise cargo pants'               duration_ms=5656  (client 5773 ms)
- PASS 'mesh long-sleeve top size S/M'      duration_ms=6120  (client 6245 ms)
- PASS 'crewneck sweatshirt under $25'      duration_ms=6367  (client 6486 ms)
- FAIL 'faded band tee'                     duration_ms=10561  (client 10669 ms)
- FAIL 'graphic hoodie size L'              duration_ms=11482  (client 11610 ms)
- PASS 'suede chelsea boots'                duration_ms=6271  (client 6403 ms)

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
    price=Y platform=Y TITLE CHECK (confirm by eye): words matched ['tee', 'butterfly']
    card: Scored this little butterfly tee on depop for just $18 and I’m obsessed. Balances out the slouchy vibe when I throw it on with baggy straight-leg jeans and a zip hoodie. 🦋✨ #y2k #thrifty
- PASS 'oversized flannel shirt' -> lst_003 'Oversized Flannel Shirt — Plaid Red/Black' $22 thredUp
    price=Y platform=Y TITLE CHECK (confirm by eye): words matched ['flannel', 'red']
    card: Found this vintage Woolrich flannel on thredUp for just $22 and I am never taking it off. It’s so cozy thrown open over a white ribbed tank with baggy straight-leg jeans and combat boots. Total 90s grunge. 🖤 #thrifted
- PASS 'leather belt under $15' -> lst_014 'Leather Belt — Brown, Braided' $12 thredUp
    price=Y platform=Y TITLE CHECK (confirm by eye): words matched ['leather', 'belt', 'braided']
    card: Scored this braided leather belt on thredUp for just $12 and it’s already doing heavy lifting for my wardrobe. Loving how it pulls together these wide-leg khaki trousers and a white ribbed tank top. 🤎✨ #thriftfind #earthtones
- PASS '90s slip dress size M' -> lst_013 '90s Silk Slip Dress — Floral, Midi Length' $30 depop
    price=Y platform=Y TITLE CHECK (confirm by eye): words matched ['silk', 'slip', 'floral']
    card: Scored this floral silk slip on depop for only $30 and I'm obsessed with how it looks poking out under an oversized grey crewneck sweatshirt. Toughened it up with some black combat boots so it feels a little less delicate for everyday. 🌸✨ #90sfashion #thriftfind
- PASS 'low-rise cargo pants' -> lst_011 'Low-Rise Cargo Pants — Khaki' $27 poshmark
    price=Y platform=Y TITLE CHECK (confirm by eye): words matched ['cargo', 'khaki']
    card: Scored these khaki cargos on Poshmark for $27 and I'm obsessed with how the distressed hems pool over my combat boots. Layered them with an oversized crewneck and a long tee for that ultimate grungy streetwear vibe. 🖤👖 #y2k #streetwear

## Criterion 5: empty wardrobe gets general advice of at least 2 sentences
- PASS 'vintage polo shirt': 5 sentences, status 200, wardrobe items on server=[], error=None
    advice: 'Outfit one: Wear the forest green polo untucked over straight-leg medium-wash blue jeans. Add a brown leather belt and white leather tennis shoes for a clean, casual weekend look. \n\nOutfit two: Tuck the polo into pleated wide-leg khaki trousers. Layer an oversized beige trench coat over the top and finish with black loafers. This leans into the vintage preppy vibe for cooler weather.'
- PASS 'platform sneakers': 4 sentences, status 200, wardrobe items on server=[], error=None
    advice: 'Outfit One: Pair the sneakers with baggy light-wash denim carpenter jeans and a fitted black baby tee. Throw on a nylon shoulder bag and small rectangle sunglasses to lean into the nostalgic Y2K streetwear vibe.\n\nOutfit Two: Contrast the chunky shoes with a grey marled hoodie and black biker shorts. Add white crew socks that peek out above the sneakers and a black baseball cap for an easy, sporty '
- PASS 'linen blazer': 6 sentences, status 200, wardrobe items on server=[], error=None
    advice: 'Outfit one: Casual weekend. Pair the blazer with a plain white cotton crewneck t-shirt, relaxed-fit medium-wash straight-leg denim, and comfortable tan leather sandals. Add a simple canvas tote bag and minimal gold hoop earrings for an easy daytime look.\n\nOutfit two: Warm weather smart-casual. Layer the blazer over a black ribbed tank top tucked into olive green linen trousers. Finish the outfit w'
- PASS 'tie-dye long sleeve': 8 sentences, status 200, wardrobe items on server=[], error=None
    advice: 'Outfit 1: The Casual Weekend. Pair the oversized pastel tie-dye long sleeve with high-waisted, straight-leg light wash jeans. Add a pair of classic white canvas low-top sneakers and a canvas tote bag. Cinch the waist with a simple brown leather belt and leave the top half-tucked.\n\nOutfit 2: The Streetwear Edge. Layer the pastel top under an oversized black denim jacket or a utilitarian black chore'
- PASS 'corduroy wide-leg pants': 6 sentences, status 200, wardrobe items on server=[], error=None
    advice: 'Outfit one: Tuck a fitted ribbed black turtleneck into the pants. Add a pair of dark brown leather ankle boots and a structured tan leather shoulder bag. Layer a vintage denim jacket on top for a classic 70s texture contrast.\n\nOutfit two: Pair the cords with an oversized cream cable-knit crewneck sweater, leaving it slightly front-tucked to show the high waist. Slip on off-white canvas low-top sne'
