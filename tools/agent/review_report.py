# Year-review results: share of year attempts that failed, by tier and by stretch of the game.
#   python3 review_report.py mat9.jsonl
import json, sys, statistics as st, collections

R = [json.loads(l) for l in open(sys.argv[1])]
B = [(1, 5), (6, 10), (11, 20), (21, 40)]
def rate(rs, a=1, b=40, why=None):
    fails = sum(1 for r in rs for f in r.get('failLog', []) if a <= f['year'] <= b and (why is None or f['why'] == why))
    passes = sum(1 for r in rs for y in r['years'] if a <= y['y'] <= b)
    return fails / max(1, fails + passes)
cells = sorted(set(r['profile'] for r in R), key=lambda n: (['Lightning', 'Steady', 'Distracted'].index(n.split(':')[0]), ['expert', 'average', 'novice'].index(n.split(':')[1])))
print("| Speed | Planner | Failed attempts | Years 1–5 | 6–10 | 11–20 | 21–40 | Review / broke / customers | Most tries at one year | Level at yr 40 | Lvl 15 (yr) |")
print("|---|---|---|---|---|---|---|---|---|---|---|")
for c in cells:
    rs = [r for r in R if r['profile'] == c]
    why = collections.Counter(f['why'] for r in rs for f in r.get('failLog', []))
    most = max([max(collections.Counter(f['year'] for f in r.get('failLog', [])).values(), default=0) for r in rs])
    lv = st.median([r['years'][-1]['stage'] for r in rs if r['years']])
    l15 = [next((y['y'] for y in r['years'] if y['stage'] >= 15), None) for r in rs]; l15 = [x for x in l15 if x]
    sp, pl = c.split(':')
    print(f"| {sp} | {pl} | {rate(rs)*100:.0f}% | " + " | ".join(f"{rate(rs,a,b)*100:.0f}%" for a, b in B) +
          f" | {why.get('review',0)} / {why.get('red',0)} / {why.get('rep',0)} | {most} | {lv:g} | {st.median(l15) if l15 else '—'}{'' if len(l15)==len(rs) else f' ({len(l15)}/{len(rs)})'} |")
