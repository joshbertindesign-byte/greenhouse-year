# Greenhouse Year

A live, isometric greenhouse management game in a single HTML file. Walk your grower around a nursery yard, take orders, plan plots on the benches, keep each house's climate in line with the forecast, and keep your customers happy year over year.

## Play

Open `index.html` in a browser, or turn on GitHub Pages for this repo (Settings → Pages → deploy from the `main` branch, root folder) and play at your Pages link.

## How it plays

- **Tablet** (top button or T): order offers and accepted orders, a tab for each greenhouse with its switches and live forecast, crew, customers and the books. Settings apply instantly; no walking needed.
- **Plots:** pick an offer on the tablet, then drop its plot on a greenhouse bench. Placing it accepts the order, and it only fits if those bench spots are free for its weeks.
- **Hands-on tasks:** bubbles pop up in the yard. Tap them to add them to your to-do list and your grower runs over and does them:
  - pot plots on their start week
  - load trucks before the week ends (unloaded trucks leave empty)
  - spray (two products; rotate them to avoid resistance)
  - fix breakdowns (heater, vents, fans, shade cloth, irrigation)
  - clear old or overgrown stock off the benches
- **Crew:** hired growers pick up tasks in the houses and roles you assign them.
- **Lots for sale:** build more greenhouses. Each one has its own quirk.
- **Time:** about 15 seconds per week at 1x, with pause (space bar) and 2x or 4x speed.

## Tech

Plain HTML, CSS and JavaScript with a canvas renderer. No build step and no dependencies apart from Google Fonts.
