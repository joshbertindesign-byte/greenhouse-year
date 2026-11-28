# Cel-shaded cats in 3/4 view. Poses: walk0/walk1 (facing down-right), walkb0/walkb1 (facing up-right, seen from behind),
# sit, sleep, eat. The game mirrors them for the other directions. Each cat's head sits where the hat code expects it
# (CHEAD, scaled by CSCALE about the feet), so festival hats still land on their heads.
import math, json
def f(v): return f"{v:.2f}".rstrip('0').rstrip('.')
U = [0]
def nid(p): U[0] += 1; return f"{p}{U[0]}"
def ell(cx, cy, rx, ry, rot=0):
    a = math.radians(rot); pts = []
    for i in range(18):
        t = i / 28 * 2 * math.pi; x, y = rx * math.cos(t), ry * math.sin(t)
        pts.append((cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)))
    return smooth(pts)
def smooth(P):
    n = len(P); d = f"M{f(P[0][0])},{f(P[0][1])}"
    for i in range(n):
        p0, p1, p2, p3 = P[i-1], P[i], P[(i+1) % n], P[(i+2) % n]
        c1 = (p1[0]+(p2[0]-p0[0])/6, p1[1]+(p2[1]-p0[1])/6); c2 = (p2[0]-(p3[0]-p1[0])/6, p2[1]-(p3[1]-p1[1])/6)
        d += f" C{f(c1[0])},{f(c1[1])} {f(c2[0])},{f(c2[1])} {f(p2[0])},{f(p2[1])}"
    return d + ' Z'
def limb(x0, y0, x1, y1, w):
    a = math.atan2(y1-y0, x1-x0); px, py = -math.sin(a)*w/2, math.cos(a)*w/2
    return (f"M{f(x0+px)},{f(y0+py)} L{f(x1+px)},{f(y1+py)} A{f(w/2)},{f(w/2)} 0 0 0 {f(x1-px)},{f(y1-py)} "
            f"L{f(x0-px)},{f(y0-py)} A{f(w/2)},{f(w/2)} 0 0 0 {f(x0+px)},{f(y0+py)} Z")
def tailpath(pts, w0, w1):
    """A tapering tail along a list of points."""
    L, R = [], []
    for i, (x, y) in enumerate(pts):
        a = pts[min(i+1, len(pts)-1)]; b = pts[max(i-1, 0)]
        ang = math.atan2(a[1]-b[1], a[0]-b[0]); w = (w0 + (w1-w0) * i/(len(pts)-1)) / 2
        L.append((x - math.sin(ang)*w, y + math.cos(ang)*w)); R.append((x + math.sin(ang)*w, y - math.cos(ang)*w))
    tip = pts[-1]
    return smooth(L + [tip] + R[::-1])

def cel2(d, base, ink, marks='', lw=1.0, s=(1.2, 1.2), hi=True, shade_op=.3):
    """Flat base + markings, then a tinted shadow crescent and a soft highlight crescent over both, then the outline."""
    p, c, m, h = nid('p'), nid('c'), nid('m'), nid('h'); u = f'xlink:href="#{p}"'
    o = [f'<defs><path id="{p}" d="{d}"/></defs><clipPath id="{c}"><use {u}/></clipPath><mask id="{m}"><use {u} fill="#fff"/><use {u} fill="#000" transform="translate({f(-s[0])},{f(-s[1])})"/></mask>']
    o.append(f'<g clip-path="url(#{c})"><use {u} fill="{base}"/>{marks}<use {u} fill="{ink}" opacity="{shade_op}" mask="url(#{m})"/>')
    if hi:
        o.append(f'<mask id="{h}"><use {u} fill="#fff"/><use {u} fill="#000" transform="translate(.9,.9)"/></mask><use {u} fill="#fff" opacity=".35" mask="url(#{h})"/>')
    o.append(f'</g><use {u} fill="none" stroke="{ink}" stroke-width="{f(lw)}" stroke-linejoin="round"/>')
    return ''.join(o)

CATS = {
 'anna':     dict(base='#fff7ec', ink='#5a3a24', eye='#5fbf4a', pat='calico', tail='#8a909a', tailink='#3a3f46'),
 'miley':    dict(base='#7d8592', ink='#2e333b', eye='#f2c230', pat='tuxedo', white='#f6f6f6'),
 'max':      dict(base='#f2a04e', ink='#7a3a10', eye='#5fbf4a', pat='tabby', stripe='#d0702a'),
 'gremlin':  dict(base='#5a3a26', ink='#1e1410', eye='#f2c230', pat='tortie', mot='#e09a4a', old=True),
 'beatrice': dict(base='#fbfaf6', ink='#4a4a52', eye='#58a8ff', pat='spots', spot='#26262c', fluffy=True, bow='#ff6fa8'),
 'minaou':   dict(base='#3a2a22', ink='#120c08', eye='#f2c230', pat='tortie', mot='#c9803a'),
 'otis':     dict(base='#b3b9c1', ink='#3e454e', eye='#5fbf4a', pat='silver', stripe='#7a828c', white='#ffffff'),
 'smokey':   dict(base='#f4e6c8', ink='#6a5638', eye='#58a8ff', pat='points', point='#8a6a4a'),
}
CHEAD = {'walk0': (43, 35), 'walk1': (43, 35), 'walkb0': (41, 32), 'walkb1': (41, 32), 'sit': (33.5, 30), 'eat': (45, 46), 'sleep': (39, 45)}
CSCALE = {'max': 1.14, 'minaou': .84, 'otis': 1.06}

def marks_for(c, region, box):
    """Pattern shapes clipped inside a body part. box = (x0,y0,x1,y1) of the part."""
    x0, y0, x1, y1 = box; w, h = x1-x0, y1-y0; p = c['pat']; o = []
    if p == 'calico':
        if region == 'head':
            o.append(f'<path d="{ell(x0+w*.18, y0+h*.12, w*.26, h*.32)}" fill="#f0943a"/><path d="{ell(x0+w*.86, y0+h*.08, w*.2, h*.26)}" fill="#3a3030"/>')
        else:
            o.append(f'<path d="{ell(x0+w*.3, y0+h*.25, w*.32, h*.3, -10)}" fill="#f0943a"/>')
            o.append(f'<path d="{ell(x0+w*.75, y0+h*.35, w*.22, h*.25, 20)}" fill="#3a3030"/>')
        pass
    elif p == 'tuxedo':
        if region == 'body': o.append(f'<path d="{ell(x0+w*.72, y0+h*.8, w*.3, h*.45)}" fill="{c["white"]}"/>')
        if region == 'head': o.append(f'<path d="{ell(x0+w*.62, y0+h*.82, w*.32, h*.3)}" fill="{c["white"]}"/>')
    elif p in ('tabby', 'silver'):
        st = c['stripe']
        for k in range(5 if region == 'body' else 3):
            xx = x0 + w*(.15 + k*.18)
            o.append(f'<path d="M{f(xx)},{f(y0-1)} q{f(w*.06)},{f(h*.35)} {f(-w*.02)},{f(h*.55)}" stroke="{st}" stroke-width="{f(max(1.1, w*.07))}" fill="none" stroke-linecap="round"/>')
        if p == 'silver' and region == 'body': o.append(f'<path d="{ell(x0+w*.75, y0+h*.85, w*.28, h*.4)}" fill="{c["white"]}"/>')
        if p == 'silver' and region == 'head': o.append(f'<path d="{ell(x0+w*.62, y0+h*.85, w*.3, h*.26)}" fill="{c["white"]}"/>')
    elif p == 'tortie':
        for (a, b, rx, ry) in [(.2, .3, .2, .18), (.55, .2, .14, .12), (.7, .65, .2, .16), (.35, .75, .14, .12)]:
            o.append(f'<path d="{ell(x0+w*a, y0+h*b, w*rx, h*ry, 25)}" fill="{c["mot"]}"/>')
    elif p == 'spots':
        for (a, b, r) in [(.25, .35, .13), (.62, .25, .1), (.78, .62, .12), (.4, .7, .09)]:
            if region == 'head' and a > .5: continue
            o.append(f'<path d="{ell(x0+w*a, y0+h*b, w*r, w*r*.8)}" fill="{c["spot"]}"/>')
    elif p == 'points':
        if region == 'head': o.append(f'<path d="{ell(x0+w*.62, y0+h*.7, w*.3, h*.26)}" fill="{c["point"]}" opacity=".55"/>')
    return ''.join(o)

def leg(c, x, y0, y1, back=False):
    col = c['base'] if not back else c['ink']
    o = cel2(limb(x, y0, x, y1, 3.5), c['base'], c['ink'], (f'<path d="{limb(x, y0, x, y1, 3.5)}" fill="#000" opacity=".22"/>' if back else '') +
             (f'<path d="{ell(x, y1, 1.6, 1.3)}" fill="{c.get("white", "#fff")}"/>' if c['pat'] in ('tuxedo', 'silver') else ''), lw=.8, hi=False)
    o += f'<ellipse cx="{f(x+.4)}" cy="{f(y1+.4)}" rx="2.2" ry="1.2" fill="{c.get("white", c["base"]) if c["pat"] in ("tuxedo","silver") else c["base"]}" stroke="{c["ink"]}" stroke-width=".7"/>'
    return o

def head(c, hx, hy, view='front', closed=False, r=6.6):
    o = []; ink = c['ink']
    # ears
    for sx, dx in ((-1, -4.0), (1, 3.6)) if view != 'back' else ((-1, -3.8), (1, 3.8)):
        ex, ey = hx + dx, hy - 4.6
        ear = f"M{f(ex-2.3*sx*-1 if False else ex-2.2)},{f(ey+2.2)} L{f(ex+(0.4*sx))},{f(ey-3.4)} L{f(ex+2.2)},{f(ey+2.2)} Z"
        o.append(cel2(ear, c['point'] if c['pat'] == 'points' else c['base'], ink, lw=.9, hi=False))
        if view != 'back': o.append(f'<path d="M{f(ex-1)},{f(ey+1.6)} L{f(ex+.3*sx)},{f(ey-1.6)} L{f(ex+1)},{f(ey+1.6)} Z" fill="#ffb3c1"/>')
    hd = ell(hx, hy, r*1.08, r*.9)
    box = (hx - r*1.08, hy - r*.9, hx + r*1.08, hy + r*.9)
    mk = marks_for(c, 'head', box) if view != 'back' else (marks_for(c, 'head', box) if c['pat'] in ('calico', 'tortie', 'tabby', 'silver', 'spots') else '')
    if c.get('fluffy'):
        P = []
        for i in range(36):
            t = i/36*2*math.pi; rr = 1 + .07*math.cos(t*9)
            P.append((hx + r*1.12*rr*math.cos(t), hy + r*.94*rr*math.sin(t)))
        hd = smooth(P)
    o.append(cel2(hd, c['base'], ink, mk, s=(1.0, 1.1)))
    if view == 'back':
        return ''.join(o)
    fx = 1.2   # features toward the facing side
    if closed:
        for ex in (hx - 2.3 + fx, hx + 2.3 + fx):
            o.append(f'<path d="M{f(ex-1.2)},{f(hy-.2)} q1.2,1 2.4,0" stroke="{ink}" stroke-width=".8" fill="none" stroke-linecap="round"/>')
    else:
        for i, ex in enumerate((hx - 2.3 + fx, hx + 2.3 + fx)):
            rx = 1.05 if i else .9
            o.append(f'<ellipse cx="{f(ex)}" cy="{f(hy-.4)}" rx="{f(rx)}" ry="1.35" fill="{c["eye"]}" stroke="{ink}" stroke-width=".55"/>'
                     f'<ellipse cx="{f(ex+.1)}" cy="{f(hy-.3)}" rx=".38" ry="1" fill="#1a1414"/><circle cx="{f(ex-.35)}" cy="{f(hy-.9)}" r=".32" fill="#fff"/>')
    mx = hx + fx + .2
    o.append(f'<path d="M{f(mx-.6)},{f(hy+1.5)} L{f(mx+.6)},{f(hy+1.5)} L{f(mx)},{f(hy+2.2)} Z" fill="#ff8fa3" stroke="{ink}" stroke-width=".4"/>')
    o.append(f'<path d="M{f(mx)},{f(hy+2.2)} q-.9,1 -1.8,.3 M{f(mx)},{f(hy+2.2)} q.9,1 1.8,.3" stroke="{ink}" stroke-width=".55" fill="none" stroke-linecap="round"/>')
    o.append(f'<path d="M{f(hx-3.6+fx)},{f(hy+1.6)} l-3,-.4 M{f(hx-3.6+fx)},{f(hy+2.3)} l-3,.4 M{f(hx+4+fx)},{f(hy+1.6)} l3,-.5 M{f(hx+4+fx)},{f(hy+2.3)} l3,.3" stroke="{ink}" stroke-width=".35" opacity=".7"/>')
    if c.get('old'): o.append(f'<path d="M{f(hx-1.6+fx)},{f(hy-2.4)} q1,-.4 1.8,0 M{f(hx+2.2+fx)},{f(hy-2.4)} q1,-.4 1.8,0" stroke="#d9d2c8" stroke-width=".5" fill="none"/>')
    if c.get('bow'):
        bx, by = hx + 3.8, hy - 5.2
        o.append(f'<path d="M{f(bx)},{f(by)} l-2.2,-1.4 v2.8 Z M{f(bx)},{f(by)} l2.2,-1.4 v2.8 Z" fill="{c["bow"]}" stroke="#9a2a58" stroke-width=".45" stroke-linejoin="round"/><circle cx="{f(bx)}" cy="{f(by)}" r=".7" fill="#ff9ac2" stroke="#9a2a58" stroke-width=".35"/>')
    return ''.join(o)

def tail(c, pts, w0=2.6, w1=1.2):
    t = tailpath(pts, w0, w1); col = c.get('tail', c['point'] if c['pat'] == 'points' else c['base']); ink = c.get('tailink', c['ink'])
    mk = ''
    if c['pat'] in ('tabby', 'silver') or c.get('tail'):
        st = c.get('stripe', '#5a6068')
        for i in range(2, len(pts) - 1, 2):
            x, y = pts[i]; mk += f'<circle cx="{f(x)}" cy="{f(y)}" r="1.5" fill="{st}"/>'
    if c['pat'] == 'tortie': mk += f'<circle cx="{f(pts[2][0])}" cy="{f(pts[2][1])}" r="1.6" fill="{c["mot"]}"/>'
    if c.get('fluffy'): w0, w1 = 3.6, 2.2; t = tailpath(pts, w0, w1)
    return cel2(t, col, ink, mk, lw=.85, hi=False)

def body_shape(cx, cy, rx, ry, rot=0, fluffy=False):
    if not fluffy: return ell(cx, cy, rx, ry, rot)
    P = []; a = math.radians(rot)
    for i in range(40):
        t = i/40*2*math.pi; rr = 1 + .05*math.cos(t*10)
        x, y = rx*rr*math.cos(t), ry*rr*math.sin(t)
        P.append((cx + x*math.cos(a) - y*math.sin(a), cy + x*math.sin(a) + y*math.cos(a)))
    return smooth(P)

def cat(cid, pose):
    U[0] = 0; c = CATS[cid]; o = []
    hx, hy = CHEAD[pose]
    shadow = {'sleep': (37, 50.6, 11, 2.8), 'sit': (32, 52.6, 8, 2.4), 'eat': (36, 52.6, 12, 2.6)}.get(pose, (36, 52.6, 12, 2.6))
    o.append(f'<ellipse cx="{shadow[0]}" cy="{shadow[1]}" rx="{shadow[2]}" ry="{shadow[3]}" fill="#1d3a24" opacity=".2"/>')
    fl = c.get('fluffy', False)
    if pose in ('walk0', 'walk1'):
        a = pose == 'walk1'
        o.append(tail(c, [(25.4, 40.6), (21, 38.6), (18.8, 33.6), (19.8, 29.2), (22.8, 27.2)], 3.0, 1.4))
        o.append(leg(c, 27.8 + (1.2 if a else -1), 44, 49.8, back=True)); o.append(leg(c, 39.4 + (-1.2 if a else 1), 44, 50, back=True))
        box = (23.6, 35, 44.8, 48)
        o.append(cel2(body_shape(34.2, 41.6, 10.6, 6.3, -4, fl), c['base'], c['ink'], marks_for(c, 'body', box), s=(1.2, 1.5)))
        o.append(leg(c, 30.6 + (-1.3 if a else 1.2), 45.4, 51.2)); o.append(leg(c, 42.0 + (1.2 if a else -1.2), 45, 51.4))
        o.append(head(c, hx, hy))
    elif pose in ('walkb0', 'walkb1'):
        a = pose == 'walkb1'
        o.append(leg(c, 36.6 + (1 if a else -1), 42, 47.6, back=True)); o.append(leg(c, 41.6 + (-1 if a else 1), 40.4, 46.2, back=True))
        box = (23, 33, 45, 49)
        o.append(head(c, hx, hy, view='back'))
        o.append(cel2(body_shape(33.4, 42.2, 9.6, 6.8, -26, fl), c['base'], c['ink'], marks_for(c, 'body', box), s=(1.2, 1.5)))
        o.append(leg(c, 27.6 + (-1 if a else 1), 46.4, 51.6)); o.append(leg(c, 33.0 + (1 if a else -1), 47, 52.2))
        o.append(tail(c, [(26.6, 41.6), (23.6, 37), (23.4, 31.6), (25.6, 28), (28.6, 27)], 3.0, 1.4))
    elif pose == 'sit':
        o.append(tail(c, [(36.4, 50.6), (40.6, 51.2), (43.6, 49.4), (44.4, 46.4)], 2.6, 1.4))
        box = (25.6, 33, 39.6, 52)
        o.append(cel2(body_shape(32.4, 43.6, 7.0, 8.8, 0, fl), c['base'], c['ink'], marks_for(c, 'body', box), s=(1.4, 1.2)))
        if c['pat'] in ('tuxedo', 'silver'):
            o.append(f'<path d="{ell(33.6, 44.4, 3.4, 6.2)}" fill="{c["white"]}"/>')
        o.append(f'<ellipse cx="30.4" cy="51.4" rx="2.2" ry="1.3" fill="{c.get("white", c["base"]) if c["pat"] in ("tuxedo","silver") else c["base"]}" stroke="{c["ink"]}" stroke-width=".75"/>')
        o.append(f'<ellipse cx="35.2" cy="51.6" rx="2.2" ry="1.3" fill="{c.get("white", c["base"]) if c["pat"] in ("tuxedo","silver") else c["base"]}" stroke="{c["ink"]}" stroke-width=".75"/>')
        o.append(head(c, hx, hy))
    elif pose == 'eat':
        o.append(tail(c, [(26, 43), (21.4, 41.6), (18.6, 38), (18.6, 34)]))
        o.append(leg(c, 28.2, 46, 51, back=True)); o.append(leg(c, 39.4, 47.4, 51.4, back=True))
        box = (22.4, 37, 44, 50)
        o.append(cel2(body_shape(32.6, 43.6, 10.4, 6.0, 8, fl), c['base'], c['ink'], marks_for(c, 'body', box), s=(1.2, 1.4)))
        o.append(leg(c, 31.4, 47.6, 51.8)); o.append(leg(c, 41.0, 48.6, 52.2))
        o.append(head(c, hx, hy, closed=True))
    elif pose == 'sleep':
        box = (25, 40, 48, 52)
        o.append(cel2(body_shape(36.4, 46.4, 11.2, 5.4, 0, fl), c['base'], c['ink'], marks_for(c, 'body', box), s=(1.2, 1.3)))
        o.append(tail(c, [(27.6, 47.6), (28.6, 50.4), (34, 51.4), (40, 51)], 2.6, 1.6))
        o.append(head(c, hx, hy, closed=True, r=5.8))
        o.append('<path d="M47,36 h2.4 l-2.4,2.6 h2.4 M50.6,31.6 h1.8 l-1.8,2 h1.8" stroke="#5a8ad0" stroke-width=".8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    k = CSCALE.get(cid, 1)
    body = ''.join(o)
    if k != 1: body = f'<g transform="translate(32,52) scale({k}) translate(-32,-52)">{body}</g>'
    return '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 64 64" width="256" height="256"><!--hc-->' + body + '</svg>'

def build():
    return {f'cat_{cid}_{pose}': cat(cid, pose) for cid in CATS for pose in ('walk0', 'walk1', 'walkb0', 'walkb1', 'sit', 'eat', 'sleep')}
if __name__ == '__main__':
    out = build(); json.dump(out, open('/home/claude/gfx/rig/cats.json', 'w'))
    print(len(out), sum(len(v) for v in out.values()) // 1024, 'KB')
