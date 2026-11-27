# Goal benchmarks for the no-losing build: when each nursery level is reached, in play time,
# calendar years and years actually played (calendar years plus replayed years), plus restart stats.
#   python3 goal_report.py long8.jsonl > GOALS.md
import json, sys, statistics as st, collections

R = [json.loads(l) for l in open(sys.argv[1])]
P = ['Lightning', 'Sharp', 'Steady', 'Casual', 'Distracted']
by = collections.defaultdict(list)
for r in R: by[r['profile']].append(r)
hm = lambda m: f"{int(m//60)}h {int(m%60):02d}m" if m >= 60 else f"{int(round(m))}m"

def played(r, year):  # years actually played up to and including `year`
    return year + sum(1 for f in r.get('failLog', []) if f['year'] <= year)

def level_at(r, L):
    """first year-end at which the nursery is at level L or higher: (calendar year, play minutes)"""
    for y in r['years']:
        if y['stage'] >= L: return y['y'], y['min']
    return None

out = ["# Greenhouse Year: goal benchmarks (no losing, year restarts)\n",
       "Five simulated players, 10 runs each, 40 calendar years. A year that ends below zero, or loses every customer, starts over; "
       "the fourth try at a year comes with a stipend and no goal. Play time is real time at 1x speed, replays included. "
       "**Played** counts years actually played (calendar years plus replays). Levels are counted at the end of the year the goal was met.\n",
       "## Restarts\n",
       "| Profile | Runs with a restart | Restarts per run (mean) | Most in one run | Years given a stipend | Restart years (median) | Play time for 40 years |",
       "|---|---|---|---|---|---|---|"]
for p in P:
    rs = by[p]
    n = [r.get('restarts', 0) for r in rs]
    yrs = [f['year'] for r in rs for f in r.get('failLog', [])]
    stip = sum(1 for r in rs for y in r['years'] if y.get('assisted'))
    t40 = [r['years'][-1]['min'] for r in rs if len(r['years']) >= 40]
    out.append(f"| {p} | {sum(1 for x in n if x)}/{len(rs)} | {st.mean(n):.1f} | {max(n)} | {stip} | {st.median(yrs) if yrs else '-'} | {hm(st.median(t40)) if t40 else '-'} |")

out += ["\n## When each level is reached\n", "Median across runs that got there: play time · calendar year · years played. `7/10` = runs that reached it.\n",
        "| Level | " + " | ".join(P) + " |", "|---|" + "---|" * len(P)]
for L in range(2, 21):
    cells = []
    for p in P:
        got = [(level_at(r, L), r) for r in by[p]]
        got = [(a, r) for a, r in got if a]
        if not got: cells.append('not reached'); continue
        t = st.median([a[1] for a, r in got]); y = st.median([a[0] for a, r in got]); pl = st.median([played(r, a[0]) for a, r in got])
        cells.append(f"{hm(t)} · yr {y:g} · played {pl:g}" + (f" · {len(got)}/{len(by[p])}" if len(got) < len(by[p]) else ''))
    out.append(f"| {L} | " + " | ".join(cells) + " |")

out += ["\n## Years spent on each level's goal\n", "Mean calendar years at each level before its goal was met (runs still on it at year 40 count their years so far).\n",
        "| Level | " + " | ".join(P) + " |", "|---|" + "---|" * len(P)]
for L in range(5, 21):
    cells = []
    for p in P:
        v = [sum(1 for y in r['years'] if y['stage'] == L) for r in by[p]]
        v = [x for x in v if x]
        cells.append(f"{st.mean(v):.1f}" if v else '-')
    out.append(f"| {L} | " + " | ".join(cells) + " |")
print('\n'.join(out))
