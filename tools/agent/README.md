# Test agent

A simulated player that works through every system in the game and reports how long real players take to reach each milestone.

* `mk_agent.py index.html a.html` builds a copy of the game that keeps the UI quiet but runs all gameplay.
* `agent.js` is the player: it plans each period, notices and taps jobs after a human-like delay, uses every feature
  (houses, crew, upgrades, genetics, vegetables, festivals, decorations, trees, succulents, showcase, office manager,
  skills, calls, the coffee cup) and spends stars at the homestead. It keeps a play clock in real seconds.
* `agent.py RUNS YEARS [profiles]` runs the profiles in headless Chrome (Playwright) and writes `results.json`.
* `report.py` turns that into the milestone table; `RESULTS.md` is the latest run.
