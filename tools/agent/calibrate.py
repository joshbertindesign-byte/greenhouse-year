# Calibrate the year review: per nursery level, targets for profit margin, full-truck share, planning score and
# reputation change; then check what share of years each tier would fail under "hit at least 3 of 4".
#   python3 calibrate.py cal.jsonl
import json, sys, statistics as st, collections

R = [json.loads(l) for l in open(sys.argv[1])]
rows = []
for r in R:
    tier = r['profile'].split(':')[1]; sp = r['profile'].split(':')[0]
    prev = None
    for y in r['years']:
        rev = y['rev'] or 0
        m = (y['op'] or 0) / rev if rev > 0 else 0
        tr = (y['full'] or 0) + (y.get('short') or 0) + (y.get('failed') or 0)
        full = (y['full'] or 0) / tr if tr else 1
        rep0 = 50 + ((prev['rep'] if prev else 50) - 50) * .7
        rows.append(dict(tier=tier, sp=sp, L=y.get('stageStart') or y['stage'], y=y['y'], m=m, full=full, plan=y.get('planPct'), drep=y['rep'] - rep0))
        prev = y

BANDS = [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10), (11, 12), (13, 14), (15, 16), (17, 18), (19, 20)]
band = lambda L: next(i for i, (a, b) in enumerate(BANDS) if a <= L <= b)
Q = float(sys.argv[2]) if len(sys.argv) > 2 else .35   # targets at this quantile of the average tier

def q(v, p): v = sorted(v); return v[min(len(v) - 1, int(len(v) * p))] if v else None
T = {}
for i, (a, b) in enumerate(BANDS):
    avg = [x for x in rows if x['tier'] == 'average' and band(x['L']) == i]
    T[i] = dict(m=q([x['m'] for x in avg], Q), full=q([x['full'] for x in avg], Q),
                plan=q([x['plan'] for x in avg if x['plan'] is not None], Q), drep=q([x['drep'] for x in avg], Q), n=len(avg))
print('targets (quantile %.2f of average tier):' % Q)
for i, (a, b) in enumerate(BANDS):
    t = T[i]
    if t['m'] is None: continue
    print(f"  L{a}-{b}: margin {t['m']*100:.0f}%  full {t['full']*100:.0f}%  plan {t['plan']}  rep {t['drep']:+.1f}   (n={t['n']})")

def fails(x):
    t = T[band(x['L'])]
    if t['m'] is None: return False
    hit = (x['m'] >= t['m']) + (x['full'] >= t['full']) + (x['plan'] is None or t['plan'] is None or x['plan'] >= t['plan']) + (x['drep'] >= t['drep'])
    return hit < 3
print('\nshare of years failing review (3 of 4 needed):')
for sp in ['Lightning', 'Steady', 'Distracted', None]:
    line = []
    for tier in ['expert', 'average', 'novice']:
        xs = [x for x in rows if x['tier'] == tier and (sp is None or x['sp'] == sp)]
        line.append(f"{tier} {sum(map(fails, xs))/len(xs)*100:.0f}%")
    print(f"  {sp or 'all':10s}", '  '.join(line))
print('\nby year band (all speeds):')
for a, b in [(1, 5), (6, 10), (11, 20), (21, 40)]:
    line = []
    for tier in ['expert', 'average', 'novice']:
        xs = [x for x in rows if x['tier'] == tier and a <= x['y'] <= b]
        line.append(f"{tier} {sum(map(fails, xs))/max(1,len(xs))*100:.0f}%")
    print(f"  yrs {a}-{b}", '  '.join(line))
json.dump({f"{a}-{b}": T[i] for i, (a, b) in enumerate(BANDS)}, open('review_targets.json', 'w'), indent=1)
