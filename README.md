# Greenhouse Year

A greenhouse management game that runs in the browser. The year runs in eight periods. Between periods you plan orders on a bench-by-period board. During each period you and your crew pot, water, spray, fix and load trucks. The operation grows from one greenhouse to four side by side, then up to three floors on each: twelve houses in all.

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
- **Trucks:** trucks queue at the road. Loading bays grow with the nursery (2 bays at 2 houses, 3 at 4, 4 at 7); each extra bay needs a loader, and loaders wait at their own bay. A truck that comes up short pauses the game so you can buy plants in or ship short.
- **Upgrades:** eleven upgrades, from pots and soil to watering booms, grow lights, a forklift and ladybugs. Each one shows up in the greenhouses.
- **Your nursery:** name it when you start (or rename it from the Ledger tab). The name goes on a roadside sign, the tablet and every magazine ranking.
- **Goals and levels:** each year has a goal (full trucks, operating profit, sales, reputation or a magazine rating). Hitting it moves you up a level, through 20 levels from Backyard grower to Hall of fame, and unlocks more upgrades, varieties, houses and crew. Miss it and you try again next year.
- **Best Homes and Gardens:** at the end of each year a fictional magazine ranks the best nurseries out of five stars. The Ledger tab keeps every year's ranking and stats.
- **Showcase house:** your first four-star year unlocks a gold-framed showcase house. Show entries for orchids, roses, peonies and calla lilies come up with your offers. Only the grower can work in it, and the plants need misting, staking and deadheading on time; each late or missed job lowers the entry's grade. At year end every entry is judged together for a Best Homes and Gardens ribbon, from Honorable mention to Best in Show, with prize money.
- **Prize grower:** after three years of showcase judging and a Silver ribbon or better, you can hire a prize grower ($5,000 fee, $600 a period) to run the showcase house so you can move on. They start out distracted; one expensive horticulture class a year ($4,000 up to $30,000) raises their attentiveness, up to Best in Show quality.
- **Grower levels:** every job your grower does personally earns experience (tree and showcase jobs count extra). There are 30 levels; each makes the grower a little faster at walking and working and gives tree and showcase jobs longer before they're missed. The grower starts a bit slow.
- **Vegetable starts:** from level 7, buy a vegetable nursery certificate. At the start of each year you can sign a spring vegetable contract, promising a customer benches of lettuce, cabbage, tomatoes, peppers, cucumbers and basil for early and late spring. Those orders come first in those periods and ship the period they're planted; each line you can't plant cuts the contract bonus by a third. A germination room makes vegetable plugs cheap, then free; organic certification raises vegetable prices but charges for every spray on vegetable benches.
- **Succulent house:** from level 12, a shop beside the greenhouses. Plant pups of five kinds; they need little care, keep growing from year to year (small, medium, specimen) and sell to customers who walk in. Customers ask for a size and sometimes a favorite kind: a perfect match tips, a size match pays full price, anything else sells for less. Six regulars have known tastes and visiting seasons.
- **Almanac:** read before each year starts (and any time from the Ledger, Shop tab or homestead): last year in review, the weather outlook, when your flowers sell best, the show calendar, trees coming ready, and the succulent consumer report with what's in, what's out and next year's early word.
- **Tree field:** from level 5 a field opens beside the greenhouses. Plant a sapling for 1 star in spring or fall (Japanese maple, blue spruce, magnolia, red maple, live oak). Trees take 2 to 5 years and need a few jobs a year that only the grower can do; missed jobs lower the grade. Sell grown trees to a landscaper for cash or to the county arboretum for stars.
- **Best Homes and Gardens:** the year-end rating is strict; your first five-star year opens the showcase house.
- **Phone calls:** a wall phone by the door of house 1 rings about once a period. Walk over in time and a caller asks for something (a discount, a rush order, a frost decision, a job seeker, a buyout offer and about 30 more, gated by level). Miss it and nothing happens.
- **Losing:** the nursery closes if every customer writes you off, or if you end two years in a row below zero. Money comes from bank loans, not credit; missed paydays can make crew quit.
- **Homestead:** between years you go home to the farm across the road. Your grower walks the paths between plots and does the clearing and building you order, one job at a time. Spend stars on clearing debris (sometimes there's a star underneath), building a display garden, farm stand, tool shed, pergola, pond, fruit trees or flower beds, growing the cat house and office, and adopting cats. Stars come from each year's Best Homes and Gardens rating, 3 more for hitting your goal, and the odd star that pops up in a greenhouse (tap it before it fades). Showcase ribbons hang on the office wall. A mailbox by the road raises its flag every 12 hours; tap it for a letter with 1 to 5 stars. Start the next year when you're ready.
- **Gift cards:** at the mailbox (or Gift cards in the Ledger tab), make a gift card once every 12 hours: a postcard of your farm and homestead with a QR code. A friend scans it in the game (live camera or a photo) or with their phone camera; they get 2 stars and you get 1. Each phone opens up to 3 gift cards every 12 hours, and each card only once. QR tools: jsQR (Apache 2.0) and QR Code Generator by Kazuhiko Arase (MIT); licences in `licenses/`.
- **Fruit trees:** shake each orchard every 6 hours for a star or two. Each orchard costs more than the last.
- **Cats:** Miley starts in the cat house. Adopt Anna, Max, Gremlin, Beatrice and Minaou as space allows; each gives a small bonus (fewer pests, fewer breakdowns, more reputation, faster new hires, better prices, more stars). They wander the greenhouses, nap, chase the odd mouse and visit their bowls. Tap one to pet it.
- **Tips:** the first time something matters, a bubble points at it and explains it, once. Key first steps are guided: the game dims everything else and waits for you to tap the highlighted spot. Readiness tips point you to features when you're ready for them (crew, upgrades, a second house, new varieties, the showcase house, a prize grower, cats). Turn tips off, replay them, or start over completely from the Ledger tab.
- **People:** when you name the nursery you choose a man or a woman as your grower (you can switch when renaming). Each crew role has its own outfit: planters in aprons, waterers in bucket hats, applicators with sprayer packs and masks, mechanics in coveralls, loaders in hard hats and hi-vis vests, and the prize grower in a sun hat and gold vest. Crew members get their own skin tone and hair colour.
- **Extras:** the seasons change the ground and weather.

## Art

All graphics are vector sprites in `art.js`, generated from Python:

- `art/vector_gen.py` writes `greenhouse_vector.svg` and `greenhouse_vector.json`, a 64×64 isometric tile set.
- `art/bundle.py` packs them into `art.js`.

## Tech

Plain HTML, CSS and JavaScript with a canvas renderer. There's no build step and no dependencies apart from Google Fonts.
