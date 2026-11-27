# Turn results.json into a milestone table: median play time (and in-game year) per reaction profile.
import json, statistics as st, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(sys.argv[1] if len(sys.argv) > 1 else HERE + '/results.json'))
names = [n for n in ['Lightning', 'Sharp', 'Steady', 'Casual', 'Distracted'] if n in R]
order = []
for n in names:
    for r in R[n]:
        for m in sorted(r['ms'], key=lambda m: r['ms'][m]['min']):
            if m not in order: order.append(m)
def hm(m): return f"{int(m // 60)}h {int(m % 60):02d}m" if m >= 60 else f"{int(round(m))}m"
med = {}
for m in order:
    med[m] = {}
    for n in names:
        hits = [r['ms'][m] for r in R[n] if m in r['ms']]
        med[m][n] = (st.median(h['min'] for h in hits), st.median(h['year'] for h in hits), len(hits), len(R[n])) if hits else None
order.sort(key=lambda m: min([v[0] for v in med[m].values() if v] or [9e9]))
rows = []
for m in order:
    cells = []
    for n in names:
        v = med[m][n]
        if not v: cells.append('not reached')
        else:
            t, y, k, N = v; cells.append(f"{hm(t)} (yr {y:g})" + ('' if k == N else f" · {k}/{N} runs"))
    rows.append((m, cells))
out = {'names': names, 'rows': rows}
# year-by-year shape and endings
summ = {}
for n in names:
    rs = R[n]; Y = max(len(r['years']) for r in rs)
    yl = []
    for y in range(Y):
        ys = [r['years'][y] for r in rs if len(r['years']) > y]
        yl.append({'y': y + 1, 'n': len(ys), 'min': st.median(v['min'] for v in ys), 'stage': st.median(v['stage'] for v in ys), 'glv': st.median(v['glv'] for v in ys),
                   'houses': st.median(v['houses'] for v in ys), 'profit': st.median(v['profit'] for v in ys), 'stars': st.median(v['stars'] for v in ys), 'ed': st.median(v['ed'] for v in ys)})
    summ[n] = {'years': yl, 'over': [r['over'] for r in rs], 'errors': {k: sum(r['errors'].get(k, 0) for r in rs) for r in rs for k in r['errors']},
               'used': {k: round(sum(r['used'].get(k, 0) for r in rs) / len(rs), 1) for r in rs for k in r['used']}}
out['summary'] = summ
json.dump(out, open(HERE + '/report.json', 'w'), indent=1)
w = max(len(m) for m, _ in rows)
print('Milestone'.ljust(w), ' | '.join(n.ljust(22) for n in names))
for m, c in rows: print(m.ljust(w), ' | '.join(x.ljust(22) for x in c))
for n in names:
    s = summ[n]; ov = [o for o in s['over'] if o]
    print(f"\n{n}: closed early in {len(ov)}/{len(s['over'])} runs {[o['year'] for o in ov]}; errors {s['errors']}")
    print('  yr  time    stage glv houses profit  stars ed')
    for y in s['years']: print(f"  {y['y']:2}  {hm(y['min']):7} {y['stage']:5g} {y['glv']:4g} {y['houses']:5g} {y['profit']:8.0f} {y['stars']:4g} {y['ed']:3g}  (n={y['n']})")
