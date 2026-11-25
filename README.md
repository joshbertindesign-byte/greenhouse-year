# Greenhouse Year

A greenhouse management game that runs in the browser. The year runs in eight periods. Between periods you plan orders on a bench-by-period board. During each period you and your crew pot, water, spray, fix and load trucks in an isometric greenhouse that can grow to three floors.

The earlier quarterly version lives in `classic/`.

## Play

Open `index.html` in a browser, or play it on GitHub Pages: https://joshbertindesign-byte.github.io/greenhouse-year/

## How it plays

- **Planning:** offers come up one at a time, and you can see the next two. Place each one on the board or bin it.
- **Shapes:** each square on the board is one bench for one period. Most orders can be rotated between Standard, Tight and Spaced shapes.
- **Timing:** one-off orders can ship early but never late. Shipping early pays less, and shipping in a crop's peak season pays more.
- **Swaps:** placing an order over unplanted ones swaps them out. Breaking a promise from an earlier round costs reputation with that customer.
- **Customers:** each of the eight customers has a standing of Lost, Wary, Steady, Loyal or Partner. Better standing means better prices, more offers and contracts. You're asked before you knowingly drop a customer to a lower tier.
- **Work:** tap the icons over the greenhouse to queue jobs. Crew pick up work on their home floor and get faster with experience.
- **Trucks:** trucks queue at the dock. A truck that comes up short pauses the game so you can buy plants in or ship short.
- **Extras:** the seasons change the ground and weather, and two greenhouse cats, Anna and Miley, wander around. Tap one to pet her.

## Art

All graphics are vector sprites in `art.js`, generated from Python:

- `art/vector_gen.py` writes `greenhouse_vector.svg` and `greenhouse_vector.json`, a 64×64 isometric tile set.
- `art/bundle.py` packs them into `art.js`.

## Tech

Plain HTML, CSS and JavaScript with a canvas renderer. There's no build step and no dependencies apart from Google Fonts.
