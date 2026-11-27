# Skill matrix: reaction speed x planner tier. One row per cell.
#   python3 matrix_report.py mat.jsonl > MATRIX.md
import json, sys, statistics as st, collections

R = [json.loads(l) for l in open(sys.argv[1])]
by = collections.defaultdict(list)
for r in R: by[r['profile']].append(r)
hm = lambda m: f"{int(m//60)}h {int(m%60):02d}m" if m >= 60 else f"{int(round(m))}m"
med = lambda v: st.median(v) if v else None

def lvl(r, L):
    for y in r['years']:
        if y['stage'] >= L: return y
    return None

def span(rs, Y0, Y1, k):
    v = [y.get(k) or 0 for r in rs for y in r['years'] if Y0 <= y['y'] <= Y1]
    return med(v)

def plan(y):
    p = y.get('plan'); return p.get('pct') if isinstance(p, dict) else p

out = ["# Skill matrix: reaction speed × planning tier\n",
       "6 runs per cell, 40 calendar years, current build. **Expert** picks ship date and shape for the most value per bench-period; "
       "**average** takes the customer's date and the first free spot; **novice** takes offers in any order, drops them on any free spot, "
       "ignores the pickups warning and sometimes skips the yearly shop.\n",
       "| Speed | Planner | Restarts / run | Level at yr 40 | Lvl 10 (yr · time) | Lvl 15 (yr · time) | Lvl 20 (yr · runs) | Profit yrs 5–10 | Profit yrs 20–40 | Bench use | Planning % |",
       "|---|---|---|---|---|---|---|---|---|---|---|"]
for name in sorted(by, key=lambda n: (['Lightning', 'Sharp', 'Steady', 'Casual', 'Distracted'].index(n.split(':')[0]), ['expert', 'average', 'novice'].index(n.split(':')[1]))):
    rs = by[name]; sp, pl = name.split(':')
    rest = st.mean([r.get('restarts', 0) for r in rs])
    final = med([r['years'][-1]['stage'] for r in rs])
    def cell(L):
        got = [lvl(r, L) for r in rs]; got = [g for g in got if g]
        if not got: return '—'
        return f"{med([g['y'] for g in got]):g} · {hm(med([g['min'] for g in got]))}" + (f" ({len(got)}/{len(rs)})" if len(got) < len(rs) else '')
    l20 = [lvl(r, 20) for r in rs]; l20 = [g for g in l20 if g]
    out.append(f"| {sp} | {pl} | {rest:.1f} | {final:g} | {cell(10)} | {cell(15)} | {(f'{med([g[chr(121)] for g in l20]):g} · {len(l20)}/{len(rs)}') if l20 else '—'} | "
               f"${span(rs,5,10,'op')/1000:.0f}k | ${span(rs,20,40,'op')/1000:.0f}k | {span(rs,1,40,'util'):.0%} | {span(rs,1,40,'plan') if False else med([plan(y) for r in rs for y in r['years'] if plan(y) is not None])} |")
print('\n'.join(out))
