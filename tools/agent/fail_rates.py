import json,sys,collections
R=[json.loads(l) for l in open(sys.argv[1]) if l.strip()]
by=collections.defaultdict(lambda:[0,0]);yb=collections.defaultdict(lambda:[0,0]);mx=collections.defaultdict(int)
for r in R:
  for y in r.get('years',[]):
    t=y.get('tries',1);b=by[r['profile']];b[0]+=t;b[1]+=t-1;mx[r['profile']]=max(mx[r['profile']],t)
    band='1-5' if y['y']<=5 else '6-10' if y['y']<=10 else '11-20' if y['y']<=20 else '21-40'
    k=(r['profile'].split(':')[1],band);yb[k][0]+=t;yb[k][1]+=t-1
print('share of year attempts that failed (most tries at one year)')
sp=['Lightning','Steady','Distracted'];tiers=['expert','average','novice']
print('| | '+' | '.join(t.capitalize() for t in tiers)+' |\n|---|---|---|---|')
for s in sp:print(f'| {s} | '+' | '.join(f"{by[s+':'+t][1]/max(1,by[s+':'+t][0]):.0%} ({mx[s+':'+t]})" for t in tiers)+' |')
print('\nby calendar years')
for t in tiers:print(t,'  '.join(f"{b}: {yb[(t,b)][1]/max(1,yb[(t,b)][0]):.0%}" for b in ['1-5','6-10','11-20','21-40']))
