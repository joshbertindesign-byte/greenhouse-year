import json,statistics as st,collections,sys
src=sys.argv[1] if len(sys.argv)>1 else 'long3.jsonl'
R=[json.loads(l) for l in open(src)]
P=['Lightning','Sharp','Steady','Casual','Distracted']
by=collections.defaultdict(list)
for r in R: by[r['profile']].append(r)
N={p:len(by[p]) for p in P}
def hm(m): return f"{int(m//60)}h {int(m%60):02d}m" if m>=60 else f"{int(round(m))}m"
allms=collections.OrderedDict()
for r in R:
    for k in r['ms']: allms[k]=1
def med(p,k):
    v=[r['ms'][k] for r in by[p] if k in r['ms']]
    return v
order=sorted(allms,key=lambda k:st.median([r['ms'][k]['min'] for r in R if k in r['ms']]))
out=[]
out.append("# Greenhouse Year: long-term study (50 runs, until failure or year 40)\n")
out.append(f"Five simulated players, 10 runs each, played until the nursery closed or 40 in-game years. Build: slower clock (pace 1.48), grower 5% slower, startup tax break, purchasable loading bays, crew wages −5% and the extra crew slots, rush-hire wage fix. Times are median **real play time at 1x speed** (running periods plus modeled planning, homestead and year-end time). `· 7/10` means only that many runs got there; the median is over those runs.\n")
out.append("## Survival\n")
out.append("| Profile | Survived 40 years | Closed | Missed paydays (runs with any) | Houses at year 40 (median) | Crew at year 40 | Cash at year 40 | Play time for 40 years |")
out.append("|---|---|---|---|---|---|---|---|")
for p in P:
    rs=by[p];ov=[r['over'] for r in rs if r['over']]
    full=[r for r in rs if len(r['years'])>=40]
    def m(f): v=[f(r['years'][-1]) for r in full]; return st.median(v) if v else None
    cl=', '.join(f"{'bank' if o['why']=='bank' else 'customers'} yr {o['year']}" for o in ov) or 'none'
    out.append(f"| {p} | {len(full)}/{len(rs)} | {cl} | {sum(1 for r in rs if r.get('missed'))} | {m(lambda y:y['houses']):.0f} | {m(lambda y:y['crew']):.0f} | ${m(lambda y:y['cash'])/1e6:.1f}M | {hm(m(lambda y:y['min']))} |")
out.append("\n## Milestones\n")
out.append("Sorted by the median across every run that reached it.\n")
out.append("| Milestone | Reached | "+" | ".join(P)+" |")
out.append("|---|---|"+"---|"*len(P))
for k in order:
    tot=sum(1 for r in R if k in r['ms'])
    cells=[]
    for p in P:
        v=med(p,k)
        if not v: cells.append('not reached');continue
        t=st.median([x['min'] for x in v]);y=st.median([x['year'] for x in v])
        cells.append(f"{hm(t)} (yr {y:g})"+(f" · {len(v)}/{N[p]}" if len(v)<N[p] else ''))
    out.append(f"| {k} | {tot}/{len(R)} | "+" | ".join(cells)+" |")
open('LONGTERM.md','w').write('\n'.join(out)+'\n')
print('\n'.join(out))
