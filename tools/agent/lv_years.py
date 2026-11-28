import json,sys,collections,statistics as st
R=[json.loads(l) for l in open(sys.argv[1]) if l.strip()]
R=[r for r in R if 'years' in r]
cnt=collections.defaultdict(list)
for r in R:
  c=collections.Counter(y['stageStart'] for y in r['years'])
  last=max(c) if c else 0
  for s,n in c.items():
    if s<last: cnt[s].append(n)   # finished levels only
  cnt[('open',last)].append(c[last])
print('runs',len(R))
for s in range(1,21):
  v=cnt.get(s,[]);o=cnt.get(('open',s),[])
  if v or o:print(f"L{s:2d} done:{len(v):3d} mean {st.mean(v) if v else 0:4.1f} med {st.median(v) if v else 0:4.1f} max {max(v) if v else 0:2d} | still on it at end: {len(o)} (yrs {o})")
