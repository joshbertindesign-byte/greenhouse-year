# Greenhouse Year

A greenhouse management game in a single HTML file. The year runs in eight periods: between periods you plan orders and contracts on a bench-by-period board, and during each period you and your crew pot, water, spray, fix and load trucks in a chunky isometric greenhouse that can grow to three floors.

The earlier quarterly version lives in `classic/`.

## Play

Open `index.html` in a browser, or turn on GitHub Pages for this repo (Settings → Pages → deploy from the `main` branch, root folder) and play at your Pages link.

## How it plays

- **Quarters:** the year opens a buying round each winter, spring, summer and fall. The clock stops while you take offers for pickups in the next two quarters and place their plots; anything left undecided is declined when the quarter starts. In summer, short-notice pop-up contracts (mostly vinca, plus some pothos and mums) pay a premium if you decide within two weeks.
- **Close the quarter:** once nothing is due or waiting to be potted before the quarter ends, close it to sell leftover stock at clearance prices and skip to the next buying round.
- **Tablet** (top button or T): order offers and accepted orders, a tab for each greenhouse with its switches and live forecast, crew, customers and the books. Settings apply instantly; no walking needed.
- **Plots:** pick an offer on the tablet, then drop its plot on a greenhouse bench. Placing it accepts the order, and it only fits if those bench spots are free for its weeks.
- **Hands-on tasks:** bubbles pop up over the greenhouse. Tap them to add them to your to-do list and your grower runs over and does them:
  - pot plots on their start week
  - load trucks at the dock behind the greenhouse before the week ends (unloaded trucks leave empty)
  - spray (two products; rotate them to avoid resistance)
  - fix breakdowns (heater, vents, fans, shade cloth, irrigation)
  - clear old or overgrown stock off the benches
- **Crew:** hired growers pick up tasks in the houses and roles you assign them.
- **Time:** about 15 seconds per week at 1x, with 2x or 4x speed. There's no pause; the clock only stops for buying rounds.

## Tech

Plain HTML, CSS and JavaScript with a canvas renderer. No build step and no dependencies apart from Google Fonts.
