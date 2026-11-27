// Greenhouse Year test agent. Runs inside the agent build of the game (a.html) and plays it the way a person would:
// it plans each period, reacts to jobs after a human-like delay, uses every feature, spends stars at the homestead,
// and keeps a "play clock" of how long a real person would have spent to get there.
window.AG = (() => {
  const PACE = BASE_PACE;                     // game seconds per real second at 1x speed
  let P, R, clock, lastTap, lapseUntil, cupSeenAt;
  const err = (where, e) => { const k = where + ': ' + (e && e.message || e); R.errors[k] = (R.errors[k] || 0) + 1; if (!R.stacks) R.stacks = {}; if (!R.stacks[k] && e && e.stack) R.stacks[k] = e.stack.split('\n').slice(0, 6).join(' | '); };
  const use = (k, n = 1) => { R.used[k] = (R.used[k] || 0) + n; };
  const tryDo = (k, f) => { try { const r = f(); return r; } catch (e) { err(k, e); } };
  const rand = Math.random;

  // ---------- drive a real modal: show it with quiet off, click the chosen button ----------
  function ui(show, pick) {
    const q = window.__quiet; window.__quiet = false;
    try { closeModal(); show(); if ($('modal').hidden) return false;
      const b = typeof pick === 'function' ? pick($('mbox')) : $('mbox').querySelector(pick);
      if (b && !b.disabled) { b.click(); return true; } return false;
    } finally { if (!$('modal').hidden) closeModal(); window.__quiet = q; }
  }
  const think = s => { clock += s; };        // planning/menu time, real seconds

  // ---------- milestones ----------
  const MS = [
    ['Nursery level 3', () => stage() >= 3], ['Nursery level 5', () => stage() >= 5], ['Nursery level 7 (vegetables)', () => stage() >= 7],
    ['Nursery level 10', () => stage() >= 10], ['Nursery level 12 (succulents)', () => stage() >= 12], ['Nursery level 15', () => stage() >= 15], ['Nursery level 20', () => stage() >= 20],
    ['Grower level 5', () => glv() >= 5], ['Grower level 10', () => glv() >= 10], ['Grower level 20', () => glv() >= 20], ['Grower level 30 (Robo-Cat)', () => glv() >= 30],
    ['2 greenhouses', () => S.floors >= 2], ['4 greenhouses', () => S.floors >= 4], ['6 greenhouses', () => S.floors >= 6], ['8 greenhouses', () => S.floors >= 8], ['12 greenhouses', () => S.floors >= 12],
    ['First 5-star magazine year', () => S.hist.some(h => h.stars >= 5)],
    ['Promoted to Greenhouse Monthly', () => (S.ed || 0) >= 1], ['Promoted to Pro Growers', () => (S.ed || 0) >= 2], ['Promoted to Prize Growers', () => (S.ed || 0) >= 3],
    ['Showcase house built', () => !!S.show], ['First showcase ribbon', () => S.hist.some(h => h.ribbon != null && h.ribbon >= 0)], ['Prize grower hired', () => !!prizeR()],
    ['First vegetable contract', () => !!(S.vc && !S.vc.none)], ['Succulent house built', () => sucOn()],
    ['Tree field open', () => fieldOpen()], ['First tree sold', () => ((S.field || {}).sold || 0) > 0],
    ['Festivals open', () => festCap() > 0], ['First festival won', () => Object.keys(S.fwin || {}).length > 0], ['First gold decoration', () => Object.keys(S.goldD || {}).length > 0],
    ['First homestead build', () => LOTS.some(l => lotState(l.id).b)], ['Second cat adopted', () => S.cats.length > 1], ['4 cats', () => S.cats.length >= 4], ['6 cats', () => S.cats.length >= 6],
    ['Office manager hired', () => mgrOn()], ['Bunkhouse built', () => hasBuild('bunk')], ['Solar array fully upgraded', () => solarLv() >= 3],
    ['Masterfully planned year', () => S.hist.some(h => h.plan && h.plan.st === 3)], ['First coffee cup', () => R.used.cup > 0],
    ['$100k in the bank', () => S.cash >= 100000],
    ['Survived the tax break (year 4)', () => S.year >= 4], ['Year 10 reached', () => S.year >= 10], ['Year 20 reached', () => S.year >= 20], ['Year 30 reached', () => S.year >= 30],
    ['Nursery level 8', () => stage() >= 8], ['Nursery level 18', () => stage() >= 18],
    ['10 greenhouses', () => S.floors >= 10], ['3 loading bays', () => bayCount() >= 3], ['4 loading bays', () => bayCount() >= 4],
    ['10 crew', () => S.crew.length >= 10], ['20 crew', () => S.crew.length >= 20],
    ['All equipment maxed', () => Object.keys(UPS).every(k => upLv(k) >= UPS[k].lv.length)], ['All varieties owned', () => Object.keys(GEN).every(k => owns(k))],
    ['$250k in the bank', () => S.cash >= 250000], ['$1M in the bank', () => S.cash >= 1000000],
  ];
  function checkMS() { for (const [n, f] of MS) if (!R.ms[n]) { let ok = false; try { ok = f(); } catch (e) { } if (ok) R.ms[n] = { min: +(clock / 60).toFixed(1), year: S.year, period: S.period }; } }

  // ---------- spending between periods ----------
  const buffer = () => P.buffer * (1 + .35 * (S.floors - 1));
  const afford = c => S.cash > c + buffer();
  const roleIn = (r, h) => S.crew.some(c => c.role === r && c.home === h);
  function buyYear() {   // the big shop at the start of the year
    let acts = 0;
    // a new house when the nursery allows it
    tryDo('houses', () => { while (S.floors < houseCap() && S.floors < MAXF && crewRoom() >= 1 && afford(FLOOR_COST[S.floors] || 0)) { const f = S.floors; buildFloor(); if (S.floors === f) break; use('houses'); acts++; } });
    // specialty houses: a vegetable house once there are 3 houses, a propagation house once there are 5; each gets its specialist
    tryDo('spec', () => {
      const conv = (k, minH) => { if (!specOpen(k) || specHouses(k).length || S.floors < minH) return; const h = [...regHouses()].reverse().find(h => h > 0 && !S.plots.some(pl => !pl.done && plotF(pl) === h)); if (h == null) return; const c = k === 'veg' && S.veg && S.veg.cert && !S.veg.conv ? 0 : SPEC_COST[k]; if (!afford(c)) return; convertHouse(h, k); if (specOf(h) === k) { use('spec'); acts++; } };
      conv('veg', 3); conv('prop', 5);
      for (const [k, role] of [['veg', 'olr'], ['prop', 'prop']]) if (specHouses(k).length && !S.crew.some(r => r.role === role) && crewRoom() > 0 && S.cash > 2000) { hire(role); use('hire'); acts++; }
    });
    // loading bays: one more at two, four and seven houses (the old automatic schedule), each staffed below
    tryDo('bays', () => { const want = S.floors >= 7 ? 4 : S.floors >= 4 ? 3 : S.floors >= 2 ? 2 : 1; while (bayCount() < want && upOpen('bays', upLv('bays')) && afford(UPS.bays.cost[upLv('bays')])) { const l = upLv('bays'); buyUp('bays'); if (upLv('bays') === l) break; use('upgrades'); acts++; } });
    // crew: water, pot and pest in each house beyond the first, a loader from two houses, a fixer from four
    tryDo('crew', () => {
      while (S.floors >= 2 && crewRoom() > 0 && S.crew.filter(c => c.role === 'load').length < bayCount() - 1 && S.cash > 2000) { hire('load'); use('hire'); acts++; }
      for (let h = 1; h < S.floors; h++) if (!specOf(h)) for (const r of ['water', 'pot', 'pest']) if (crewRoom() > 0 && !roleIn(r, h) && S.cash > 2000) { hire(r); setHome(S.crew[S.crew.length - 1].id, h); use('hire'); acts++; }
      if (S.floors >= 4 && crewRoom() > 0 && !S.crew.some(c => c.role === 'fix')) { hire('fix'); use('hire'); acts++; }
      if (S.floors >= 2 && crewRoom() > 0 && !roleIn('water', 0)) { hire('water'); setHome(S.crew[S.crew.length - 1].id, 0); use('hire'); acts++; }
    });
    // genetics, cheapest first
    tryDo('genetics', () => { for (const k of Object.keys(GEN).sort((a, b) => GEN[a] - GEN[b])) if (!owns(k) && cropOpen(k) && afford(GEN[k])) { buyGen(k); if (owns(k)) { use('genetics'); acts++; } } });
    // upgrades in a sensible order, one level at a time
    tryDo('upgrades', () => { for (let pass = 0; pass < 3; pass++) for (const k of P.upOrder) { const l = upLv(k), U = UPS[k]; if (l < U.lv.length && upOpen(k, l) && afford(U.cost[l])) { buyUp(k); if (upLv(k) > l) { use('upgrades'); acts++; } } } });
    // vegetables
    tryDo('veg', () => {
      if (stage() >= VEG_LV && !(S.veg && S.veg.cert) && afford(VEG_CERT)) { buyVeg('cert'); use('vegCert'); acts++; }
      if (S.veg && S.veg.cert && (S.veg.germ || 0) < 2 && afford(VEG_GERM[S.veg.germ || 0])) { buyVeg('germ'); use('vegGerm'); acts++; }
      if (S.veg && S.veg.cert && !S.veg.org && S.floors >= 4 && afford(VEG_ORG * 3)) { buyVeg('org'); use('vegOrg'); acts++; }
      if (vegOn() && !(S.vc && S.vc.year === S.year)) { const cs = makeVegContracts(); S.vc = cs[Math.min(cs.length - 1, S.floors >= 4 ? 2 : 1)]; use('vegContract'); think(P.modal); }
    });
    // showcase house, prize grower, classes, premium genetics
    tryDo('showcase', () => {
      if (S.showOpen && !S.show && afford(SHOW_COST)) { buildShow(); if (S.show) { use('showcase'); acts++; } }
      if (S.show && prizeOpen() && !prizeR() && afford(5000)) { hirePrize(); if (prizeR()) { use('prizeGrower'); acts++; } }
      if (prizeR() && (prizeR().att || 1) < 5 && afford(3000)) { takeClass(); use('class'); acts++; }
      if (S.show) for (const k of Object.keys(SHOWC)) { const C = SHOWC[k]; if (C.prem && !S.owned.includes(k) && stage() >= C.lv && afford(C.prem * 1.5)) { buyPrem(k); if (S.owned.includes(k)) { use('premGenetics'); acts++; } } }
    });
    // succulent house
    tryDo('succulents', () => { if (!sucOn() && stage() >= SUC_LV && afford(SUC_COST)) { sucBuild(); if (sucOn()) { use('sucHouse'); acts++; } } if (sucOn() && sucCap() <= 12 && S.floors >= 6 && afford(SUC_EXP * 2)) { sucExpand(); use('sucExpand'); acts++; } });
    // office manager
    tryDo('office', () => { if (!mgrOn() && stage() >= MGR_LV && (S.office || 1) >= 2 && afford(6000)) { hireMgr(); if (mgrOn()) { use('manager'); acts++; } } });
    // keep the best customers sweet
    tryDo('customers', () => {
      if (S.cash > 20000) { const top = Object.keys(S.cust || {}).sort((a, b) => custR(b) - custR(a))[0]; if (top && crmOf(top).gift !== S.year) { crmGift(top); use('crmGift'); acts++; } }
      if (mgrOn() && S.cash > 30000) for (const n of Object.keys(S.cust || {})) if (tierIx(custR(n)) <= 1 && crmOf(n).amends !== S.year) { crmAmends(n); use('crmAmends'); acts++; break; }
    });
    return acts;
  }
  function skills() { let n = 0; tryDo('skills', () => { for (let pass = 0; pass < 4 && skPts() > 0; pass++) for (const k of P.skillOrder) { if (skPts() < 1) break; const b = sk(k); skBuy(k); if (sk(k) > b) n++; } }); if (n) { use('skills', n); closeModal(); } return n; }
  function decorate() {
    let n = 0;
    tryDo('decorate', () => {
      if (!decorOpen()) return; S.place = S.place || {};
      // store pieces with boosts once the homestead is comfortable
      for (const k of ['fan', 'radio']) if ((S.stars || 0) > P.starReserve + 25 && decOwned(k) < S.floors) { buyDeco(k); use('decoBuy'); }
      for (const h of decoHouses()) { const sl = S.place[h] || (S.place[h] = [null, null, null, null, null]);
        for (let i = 0; i < 5; i++) { if (!spotOpen(i)) continue;
          const score = k => (isGold(k) ? 4 : 0) + (DECO[dBase(k)].b ? 2 : 0);
          const inv = [...Object.keys(S.goldD || {}).map(k => 'g:' + k), ...Object.keys(DECO)].filter(k => decFits(k, i) && (decOwned(k) > decUsed(k)) && !sl.includes(k) && !sl.includes(dBase(k)) && !sl.includes('g:' + dBase(k))).sort((a, b) => score(b) - score(a));
          if (inv[0] && (!sl[i] || score(inv[0]) > score(sl[i]))) { sl[i] = inv[0]; n++; } } }
    });
    if (n) use('decoPlace', n); return n;
  }
  function trees() {
    let n = 0;
    tryDo('trees', () => {
      if (!fieldOpen() || !treeLive() || !treeWindow()) return;
      const T = treesOf();
      for (const i of Object.keys(T)) { const t = T[i]; if (treeReady(t) && !t.sell) { if (ui(() => sellModal(+i), (S.stars || 0) < P.starReserve ? '#slS' : '#slC')) { use('treeSell'); n++; } } }
      for (let i = 0; i < fieldCap(); i++) { if (treesOf()[i] || (S.stars || 0) < 2 + P.starReserve / 3) continue;
        const best = b => [...b.querySelectorAll('[data-sp]')].filter(x => !x.disabled).sort((x, y) => TREES[y.dataset.sp].cash / TREES[y.dataset.sp].yrs - TREES[x.dataset.sp].cash / TREES[x.dataset.sp].yrs)[0];
        if (ui(() => plantModal(i), best)) { use('treePlant'); n++; } }
    });
    return n;
  }
  function succulents() {
    let n = 0;
    tryDo('sucPlant', () => { if (!sucOn()) return; const order = Object.keys(SUCS).sort((a, b) => trendM(b) - trendM(a));
      for (let i = 0; i < sucCap(); i++) if (!sucPlants()[i] && !sucBlocked(i) && S.cash > SUCS[order[0]].pup + buffer()) { sucPlant(i, order[n % 2]); use('sucPup'); n++; } });
    return n;
  }
  function festivals() {
    let n = 0;
    tryDo('festivals', () => { festGen();
      for (const k of festNow(S.period)) { if (FESTS[k].kind === 'tour' || S.fy.done[k] != null) continue;
        const F = FESTS[k], cost = F.kind === 'bench' ? festBenches() * capB() * CROPS[F.crop].price * .3 : Math.min(4, festEmpty().length) * F.each;
        const join = S.cash > cost + buffer() * .5 && rand() < P.festJoin;
        ui(() => festAsk(), join ? '#fsY' : '#fsN'); if (S.fy.done[k] === 1) { use('festJoin'); n++; } else if (S.fy.done[k] == null) S.fy.done[k] = 0; think(P.modal); } });
    return n;
  }
  function placeOffers() {
    let n = 0;
    tryDo('placing', () => {
      const pri = o => (o.veg ? 2 : 0) + (o.fest ? 1 : 0);
      let offers = S.offers.slice();
      if (P.planner === 'novice') offers.sort((a, b) => pri(b) - pri(a) || rand() - .5);
      else if (P.planner === 'expert') offers.sort((a, b) => pri(b) - pri(a) || (b.contract - a.contract) || bestPlan(b).dens - bestPlan(a).dens);
      else offers.sort((a, b) => pri(b) - pri(a) || (b.contract - a.contract) || (b.qty * b.price - a.qty * a.price));
      for (const o of offers) { if (P.skipChance && rand() < P.skipChance && !o.veg && !o.contract) continue; if (placeOne(o)) n++; }
      // the office manager holds a good order that didn't fit
      if (mgrOn()) for (let k = 0; k < HOLD_MAX; k++) { const q = queue(); if (q.length && holdable(q[0]) && (S.held || []).length < HOLD_MAX) { holdHand(); use('hold'); } else break; }
    });
    use('ordersPlaced', n); return n;
  }
  // ---- planning skill: expert picks ship date and shape for the most value per bench-period and keeps an eye on crowded markets;
  //      average takes the customer's date, default shape, first free spot (the game's own auto-accept); novice takes offers in any
  //      order and drops them on any free spot it finds ----
  function fillAt(p) { const rh = regHouses(), cap = Math.max(1, rh.length * 8); let n = 0; for (const pl of S.plots) if (!pl.done && pl.s <= p && pl.e >= p && rh.includes(plotF(pl))) n += pl.rows.length; return n / cap; }
  function bestPlan(o) {
    if (o.contract || o.veg || o.fest || !flexible(o)) { const F = formOf(o); return { d: dueOf(o), fm: o.fm || 0, v: valAt(o, dueOf(o)), dens: valAt(o, dueOf(o)) / Math.max(1, F.h * F.g) }; }
    let best = null; const fs = forms(o);
    for (let fm = 0; fm < fs.length; fm++) for (let d = Math.max(dMin({ ...o, fm }), 0); d <= o.p; d++) { const v = valAt(o, d), dens = v / (fs[fm].h * fs[fm].g); if (!best || dens > best.dens) best = { d, fm, v, dens }; }
    return best || { d: o.p, fm: 0, v: valAt(o, o.p), dens: 0 };
  }
  function placeOne(o) {
    if (!offerOwned(o)) return false;
    if (P.planner === 'expert' && !o.contract && !o.veg && !o.fest && flexible(o)) {
      // hold benches: turn down a low-value order when the periods it would tie up are already filling
      const b = bestPlan(o), seen = (R.densSeen = R.densSeen || []); seen.push(b.dens); if (seen.length > 200) seen.shift();
      const sorted = seen.slice().sort((x, y) => x - y), cut = sorted[Math.floor(sorted.length * .35)] || 0;
      const F = forms(o)[b.fm] || formOf(o), span = []; for (let p = b.d - F.g + 1; p <= b.d; p++) if (p > S.period) span.push(p);
      if (seen.length >= 20 && b.dens < cut && span.some(p => fillAt(p) > .6)) { use('heldBack'); return false; }
      const fs = forms(o), tries = [];
      for (let fm = 0; fm < fs.length; fm++) for (let d = Math.max(dMin({ ...o, fm }), 0); d <= o.p; d++) tries.push({ d, fm, v: valAt(o, d) / (fs[fm].h * fs[fm].g) });
      tries.sort((a, b) => b.v - a.v);
      for (const t of tries) { o.d = t.d; o.fm = t.fm; const r = firstFit(o); if (r >= 0 && place(o, r)) return true; }
      delete o.d; o.fm = 0; return false;
    }
    if (P.planner === 'novice' && !o.contract) {
      const rows = benchIds().filter(r => fits(o, r)); if (!rows.length) return false; return place(o, rows[Math.floor(rand() * rows.length)]);
    }
    return autoAccept(o);
  }
  function planPeriod() {
    const y0 = S.period === 0; let acts = 0;
    if (y0) { if (P.planner !== 'novice' || rand() < .6) acts += buyYear(); acts += decorate(); }
    acts += festivals(); acts += trees(); acts += succulents(); acts += skills();
    const n = placeOffers();
    // heed the pickups row: hire a loader or build a bay when it turns amber or red
    if (P.planner !== 'novice') tryDo('dock', () => { for (let k = 0; k < 3; k++) { let fix = ''; for (let p = S.period; p < 8 && !fix; p++) { const d = dockLoad(p); if (d.m >= .25) fix = d.fix; }
      if ((fix === 'open' || fix === 'loader') && crewRoom() > 0 && S.cash > 2000) { hire('load'); use('hire'); acts++; }
      else if (fix === 'bay' && afford(UPS.bays.cost[upLv('bays')])) { buyUp('bays'); use('upgrades'); acts++; } else break; } });
    { R.dock = R.dock || { periods: 0, warn: 0, pred: 0, empty: 0 }; const d = dockLoad(S.period); R.dock.periods++; if (d.m >= .25) R.dock.warn++; R.dock.pred += d.m; }
    think(P.planBase + P.perOrder * n + P.perAct * acts + (y0 ? P.yearStart : 0));
    tryDo('start', () => tryStart(true));
    if (S.phase === 'plan') { tryDo('start2', () => { S.offers = []; tryStart(true); }); }
  }

  // ---------- playing a period ----------
  const crewJob = t => S.crew.some(r => roleTakes(r.role, t) && (t.type === 'load' || r.home === taskF(t))) || (prizeR() && t.type !== 'load' && taskF(t) === SH);
  // the crew gets first go at their jobs; anything they leave waiting, the grower picks up
  const covered = t => crewJob(t) && S.t - t.seen < (P.react + P.patience) * PACE;
  function runStep(dt) {
    const now = S.t;
    for (const t of S.tasks) if (t.seen == null) t.seen = now;
    // zoning out now and then
    if (clock >= lapseUntil && rand() < P.lapse * dt / PACE) { lapseUntil = clock + P.lapseLen; use('lapse'); }
    const attentive = clock >= lapseUntil;
    if (attentive) {
      // mid-period offers (pop-ups)
      for (const o of S.offers.filter(o => o.popup)) { if (o.seenAt == null) o.seenAt = now; if (now - o.seenAt >= P.react * PACE * 1.5) { tryDo('popup', () => autoAccept(o)) ? use('popupTaken') : null; o.popup = false; } }
      // the coffee cup
      if (cup) { if (cupSeenAt == null) cupSeenAt = now; if (now - cupSeenAt >= P.react * PACE && rand() < P.cupNotice * dt * 2) { tryDo('cup', () => drinkCup()); use('cup'); cupSeenAt = null; } } else cupSeenAt = null;
      // glance at the board every so often, then tap several jobs in a quick burst
      if (now - lastTap >= P.glance * PACE || now < lastTap) {
        lastTap = now;
        const waiting = () => S.queue.filter(t => S.tasks.includes(t) && me.task !== t).length;
        let c = S.tasks.filter(t => now - t.seen >= P.react * PACE && !S.queue.includes(t) && !engaged(t) && !covered(t) && (t.type !== 'load' || truckById(t.truck)?.state === 'dock'));
        c.sort(P.fifo ? (a, b) => a.seen - b.seen : (a, b) => (a.due ?? now + 99) - (b.due ?? now + 99));
        let taps = 0;
        for (const t of c) { if (waiting() >= P.maxQueue) break; tryDo('enqueue', () => enqueue(t)); use('tap:' + t.type); taps++; }
      }
    }
    try { simStep(dt); } catch (e) { err('simStep', e); }
    clock += dt / PACE;
  }

  // ---------- the homestead ----------
  function home() {
    let acts = 0;
    tryDo('home', () => {
      const free = () => LOTS.filter(l => !l.pre && !lotState(l.id).b);
      const cleared = () => free().filter(l => lotState(l.id).clear);
      const getLot = () => { const c = cleared(); if (c.length) return c[0]; const u = free().filter(l => !lotState(l.id).clear).sort((a, b) => a.cost - b.cost)[0]; if (u && (S.stars || 0) >= u.cost) { clearLot(u.id); use('lotClear'); acts++; return lotState(u.id).clear ? u : null; } return null; };
      const build = k => { const B = BUILDS[k]; if ((B.uniq && hasBuild(k)) || (S.stars || 0) < bcost(k) + (cleared().length ? 0 : 3)) return false;
        if (B.lm) { // a landmark needs this plot and the empty plot to its right
          const pair = LOTS.filter(l => !l.pre && !lotState(l.id).b && lmPart(l.id) && !lotState(lmPart(l.id).id).b).sort((a, b) => (lotState(b.id).clear ? 1 : 0) + (lotState(lmPart(b.id).id).clear ? 1 : 0) - (lotState(a.id).clear ? 1 : 0) - (lotState(lmPart(a.id).id).clear ? 1 : 0))[0];
          if (!pair) return false; for (const L of [pair, lmPart(pair.id)]) if (!lotState(L.id).clear) { if ((S.stars || 0) < L.cost) return false; clearLot(L.id); use('lotClear'); acts++; }
          buildLot(pair.id, k); if (hasBuild(k)) { use('build:' + k); acts++; return true; } return false; }
        const L = getLot(); if (!L) return false; buildLot(L.id, k); if (lotState(L.id).b === k) { use('build:' + k); acts++; return true; } return false; };
      for (const step of P.homeOrder) {
        if (step === 'cats') { const want = ['beatrice', 'minaou', 'max', 'anna', 'miley', 'gremlin', 'otis', 'smokey'];
          for (const c of want) { if (catOn(c) || (c === 'smokey' && !smokeyHere())) continue; if (S.cats.length >= catCap()) { const l = S.catHouse || 1; if (l < 4 && (S.stars || 0) >= CATHOUSE_COST[l + 1] + 2) { growCatHouse(); use('catHouse'); acts++; } else break; }
            if (S.cats.length < catCap() && (S.stars || 0) >= catCost(c)) { adoptCat(c); if (catOn(c)) { use('adopt'); acts++; } } } }
        else if (step === 'office') { if ((S.office || 1) < 2 && stage() >= MGR_LV - 1 && (S.stars || 0) >= OFFICE_COST) { growOffice(); use('officeGrow'); acts++; } }
        else if (step === 'solarUp') { const L = LOTS.find(l => lotState(l.id).b === 'solar' && !lotState(l.id).part); if (L && solarLv() < 3 && (S.stars || 0) >= BUILDS.solar.ups[solarLv() - 1]) { upLandmark(L.id); use('solarUp'); acts++; } }
        else if (step === 'reserve') { if ((S.stars || 0) <= P.starReserve) break; }
        else if (BUILDS[step]) { if (BUILDS[step].lv && stage() < BUILDS[step].lv) continue; if (!BUILDS[step].uniq && hasBuild(step)) continue; build(step); }
      }
    });
    tryDo('wardrobe', () => { if (Object.keys(S.hats || {}).length) { S.hatSet = S.hatSet || {}; use('hats'); } });
    flushHJobs && tryDo('flush', () => flushHJobs());
    think(P.homeBase + P.homePerAct * acts); return acts;
  }

  // ---------- one year ----------
  function year() {
    const y = S.year;
    let guard = 0;
    while (S.phase !== 'done' && S.phase !== 'over' && guard++ < 3000000) {
      if (S.phase === 'plan') { planPeriod(); checkMS(); continue; }
      if (S.phase === 'run') { const p = S.period; runStep(P.dt); if (S.phase !== 'run' || S.period !== p) checkMS(); continue; }
      if (S.phase === 'home') { tryDo('leave', () => leaveHome()); continue; }
      break;
    }
    if (S.phase === 'over') { R.over = { year: S.year, min: +(clock / 60).toFixed(1), why: S.lost || '?' }; return false; }
    const h = S.hist[S.hist.length - 1];
    const ys = S.ys || {};
    R.restarts = (S.failLog || []).length; R.failLog = (S.failLog || []).slice();
    const used = S.plots.filter(pl => plotF(pl) !== SH && !specOf(plotF(pl))).reduce((a, pl) => a + pl.rows.length * (Math.min(7, pl.e) - Math.max(0, pl.s) + 1), 0), capT = (S.ys.cap || []).reduce((a, c) => a + (c || 0), 0);
    R.years.push({ util: capT ? +(used / capT).toFixed(2) : null, tries: h.tries || 1, assisted: h.assisted || 0, spec: Object.values(S.spec || {}).join(','), propSaved: S.ys.propSaved || 0, propSold: S.ys.propSold || 0, roy: S.ys.roy || 0, propProb: S.ys.propProb || 0, vegRev: S.ys.vegRev || 0, plugs: S.ys.plugs, crewCost: S.ys.crew, overhead: S.ys.overhead, full: h.full, rep: h.rep, op: h.op, tax: h.tax || 0, gRun: h.gRun ? h.gRun.n : null, y, min: +(clock / 60).toFixed(1), stage: stage(), glv: glv(), stars: h.stars, ed: S.ed || 0, rank: h.rank, profit: Math.round(h.profit), rev: Math.round(h.rev), houses: S.floors, crew: S.crew.length, cash: Math.round(S.cash), starBank: S.stars || 0, cats: S.cats.length, plan: h.plan ? h.plan.pct : null, build: Math.round(ys.build || 0), loans: (S.loans || []).reduce((a, l) => a + l.left, 0) });
    think(P.yearEnd); skills(); checkMS();
    tryDo('nextYear', () => { nextYear(); enterHome(); }); home(); checkMS(); tryDo('leaveHome', () => leaveHome()); closeModal(); checkMS();
    return true;
  }

  function start(prof, seed) {
    P = prof; R = { profile: prof.name, ms: {}, used: {}, errors: {}, years: [], over: null };
    if (!window.__tlWrap) { const o = truckLeaves; window.truckLeaves = function (k, m) { if (m && R && R.dock) { const pl = S.plots.find(p => p.id === k.plot); if (pl && !pl.done) { R.dock.empty++; const ey = (R.ey = R.ey || {}), e = (ey[S.year] = ey[S.year] || { n: 0, line: 0, dock: 0, noLoad: 0, short: 0, loaders: 0, cash: 0 }); e.n++; if (k.state === 'line') e.line++; else e.dock++; const t = S.tasks.find(t => t.type === 'load' && t.truck === k.id); if (t && !engagedT(t)) e.noLoad++; if (have(pl) < orderOf(pl).qty) e.short++; e.loaders = S.crew.filter(c => c.role === 'load').length; e.bays = bayUse(); e.cash = Math.round(S.cash); } } return o.apply(this, arguments); }; window.__tlWrap = 1; }
    window.engagedT = t => { try { return engaged(t); } catch (e) { return false; } };
    clock = 0; lastTap = -99; lapseUntil = -1; cupSeenAt = null;
    window.__quiet = true; window.__agent = 1; window.__autoLoan = 1; window.__rushHire = 1;
    window.__agentCall = (ctx, ok) => { use('call'); ok = ok.filter(o => !/Ends the game/.test(o.fx || '')); return ok.length > 1 && rand() < P.callYes ? ok[0] : ok[ok.length - 1]; };
    try { save = () => { }; } catch (e) { }
    fresh(); S.welcomed = true; S.tipsOff = 1; S.coached = 1; S.homeSeen = 1; genOffers(); beginPlan(); closeModal(); closeSheet();
    // log missed paydays: cash on hand vs payroll due
    if (!window.__pdWrap) { const o = payday; window.payday = function () { const c0 = S.cash, d0 = payroll(), m0 = S.ys.missed || 0; const r = o.apply(this, arguments); if ((S.ys.missed || 0) > m0 && R) { R.missed = (R.missed || 0) + 1; if ((R.missLog = R.missLog || []).length < 12) R.missLog.push({ y: S.year, p: S.period, cash: Math.round(c0), due: Math.round(d0), crew: S.crew.length, maxW: Math.max(0, ...S.crew.map(x => x.wage)) }); } return r; }; window.__pdWrap = 1; }
    // catch any single cash change bigger than $250k (or a non-finite one) with a stack, for chasing runaway costs
    { let c = S.cash; Object.defineProperty(S, 'cash', { configurable: true, enumerable: true, get: () => c, set: v => { if ((Math.abs(v - c) > 250000 || !isFinite(v)) && (R.big = R.big || []).length < 6) R.big.push({ y: S.year, p: S.period, from: Math.round(c), to: Math.round(v), stack: (new Error().stack || '').split('\n').slice(2, 7).join(' | ') }); c = v; } }); }
  }
  function years(n) { for (let i = 0; i < n; i++) { if (!year()) break; } return R; }
  return { start, years, get R() { return R; } };
})();
