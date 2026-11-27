import json,statistics as st,collections,sys
R=[json.loads(l) for l in open(sys.argv[1])]
by=collections.defaultdict(list)
for r in R: by[r['profile']].append(r)
for p in ['Lightning','Sharp','Steady','Casual','Distracted']:
    rs=by[p];ov=[r['over'] for r in rs if r['over']]
    print(p,'closed',len(ov),sorted([(o['why'],o['year']) for o in ov],key=lambda x:x[1]))
    for Y in [4,8,10,13,16,20,25,30,35,40]:
        ys=[r['years'][Y-1] for r in rs if len(r['years'])>=Y]
        if not ys: continue
        m=lambda k:st.median([y.get(k) or 0 for y in ys])
        print(f"  y{Y:2d} n{len(ys):2d} rev {m('rev'):>7.0f} op {m('op'):>7.0f} tax {m('tax'):>6.0f} margin {m('op')/max(1,m('rev')):.0%} full {m('full'):>4.0f} rep {m('rep'):>3.0f} houses {m('houses'):>2.0f} crew {m('crew'):>2.0f} stage {m('stage'):>2.0f} rank {m('rank'):.0f} stars {m('stars')} ed {m('ed')} cash {m('cash'):>8.0f}")
