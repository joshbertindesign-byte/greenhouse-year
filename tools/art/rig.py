# Cel-shaded people for Greenhouse Year: a small part-based rig drawn in 3/4 view.
#   'front' faces down-right (south-east), 'back' faces up-right (north-east); the game mirrors them for the other two.
#   Frames: _0 idle, _1 and _2 walking, _work, and for the grower _shovel0/1 and _hammer0/1.
# Skin and hair use the game's recolour tokens (SKINS[0], HAIRS[0] plus the shade/ink entries added for this art),
# so crew looks and the grower's skin choice keep working.
import math, json

def f(v): return f"{v:.2f}".rstrip('0').rstrip('.')
U = [0]
def nid(p): U[0] += 1; return f"{p}{U[0]}"

SK = dict(base='#ffd8b8', hand='#ffd3b0', ink='#c98a63', shade='#f0b28c')   # skin tokens (tone 0)
HR = dict(base='#8a5631', shade='#6a3e22', ink='#4a2814')                    # hair tokens
LW = 1.0      # outline weight
DW = .6       # inner detail weight

def cel(d, base, shade, hi, ink, s=(1.0, 1.2), h=(.9, .9), lw=LW, hion=True, extra=''):
    """A filled shape with a hard shadow crescent (bottom-right) and highlight crescent (top-left), then its outline.
    The path is stored once and reused with <use> to keep files small."""
    p = nid('p'); c = nid('c'); m = nid('m'); u = f'xlink:href="#{p}"'
    o = [f'<defs><path id="{p}" d="{d}"/></defs><clipPath id="{c}"><use {u}/></clipPath>']
    o.append(f'<g clip-path="url(#{c})"><use {u} fill="{shade}"/><use {u} fill="{base}" transform="translate({f(-s[0])},{f(-s[1])})"/>')
    if hion and hi:
        o.append(f'<mask id="{m}"><use {u} fill="#fff"/><use {u} fill="#000" transform="translate({f(h[0])},{f(h[1])})"/></mask><use {u} fill="{hi}" mask="url(#{m})"/>')
    o.append(extra + '</g>')
    if ink: o.append(f'<use {u} fill="none" stroke="{ink}" stroke-width="{f(lw)}" stroke-linejoin="round"/>')
    return ''.join(o)

def rrect(x, y, w, h, r):
    r = min(r, w / 2, h / 2)
    return (f"M{f(x+r)},{f(y)} H{f(x+w-r)} Q{f(x+w)},{f(y)} {f(x+w)},{f(y+r)} V{f(y+h-r)} Q{f(x+w)},{f(y+h)} {f(x+w-r)},{f(y+h)} "
            f"H{f(x+r)} Q{f(x)},{f(y+h)} {f(x)},{f(y+h-r)} V{f(y+r)} Q{f(x)},{f(y)} {f(x+r)},{f(y)} Z")
def ell(cx, cy, rx, ry, rot=0):
    if rot:
        a = math.radians(rot); pts = []
        for i in range(24):
            t = i / 24 * 2 * math.pi; x, y = rx * math.cos(t), ry * math.sin(t)
            pts.append((cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)))
        return 'M' + ' L'.join(f"{f(x)},{f(y)}" for x, y in pts) + ' Z'
    return f"M{f(cx-rx)},{f(cy)} A{f(rx)},{f(ry)} 0 1 0 {f(cx+rx)},{f(cy)} A{f(rx)},{f(ry)} 0 1 0 {f(cx-rx)},{f(cy)} Z"
def poly(pts): return 'M' + ' L'.join(f"{f(x)},{f(y)}" for x, y in pts) + ' Z'
def limb(x0, y0, x1, y1, w):
    """A capsule from (x0,y0) to (x1,y1)."""
    a = math.atan2(y1 - y0, x1 - x0); px, py = -math.sin(a) * w / 2, math.cos(a) * w / 2
    return (f"M{f(x0+px)},{f(y0+py)} L{f(x1+px)},{f(y1+py)} A{f(w/2)},{f(w/2)} 0 0 0 {f(x1-px)},{f(y1-py)} "
            f"L{f(x0-px)},{f(y0-py)} A{f(w/2)},{f(w/2)} 0 0 0 {f(x0+px)},{f(y0+py)} Z")

# ---------------- outfits ----------------
def C(base, shade, hi, ink): return dict(base=base, shade=shade, hi=hi, ink=ink)
DENIM = C('#4f78d6', '#3a5aa8', '#7ea0ec', '#22396e')
DENIM_D = C('#3f63b8', '#2f4b8e', '#6d8fe0', '#1d3160')
BOOT = C('#7a4a2b', '#5a341d', '#9c6a43', '#3a2010')
GREEN = C('#5ccf74', '#3a9e55', '#8fe8a0', '#1f6a36')
PINK = C('#ff86b2', '#e05a8e', '#ffb4cf', '#9a2a58')
CORAL = C('#ff8a6a', '#e0603f', '#ffb39a', '#9a3420')
BLUESH = C('#58a8ff', '#3a7fd6', '#9acbff', '#1d4e94')
GREY = C('#8a96a3', '#66727e', '#b4bec8', '#363e47')
WHITE = C('#f6f7fb', '#cfd5e2', '#ffffff', '#6a7385')
CREAM = C('#fff3d6', '#ecd6a4', '#ffffff', '#8a6a34')
GOLD = C('#f2c230', '#c9951a', '#ffe27a', '#7a5600')
HIVIS = C('#d7f03a', '#a8c020', '#f0ff8a', '#5a6a00')
KHAKI = C('#d8c48a', '#b39f62', '#efe0b0', '#6a5a2a')
BROWN = C('#b77a42', '#8f5a2c', '#d9a06a', '#4e2e12')
ORANGE = C('#ff8a3a', '#e0661c', '#ffb57a', '#8a3a06')
BLACK = C('#3a3f46', '#262a30', '#5c636c', '#121417')
YELLOW = C('#ffd23a', '#e0a91c', '#fff08a', '#8a6000')
STRAW = C('#f7d77e', '#d9b052', '#fff0b4', '#8a6a1a')
RED = C('#ef5b4c', '#c43a2e', '#ff8a7c', '#7a1a12')
PURPLE = C('#8a4fd0', '#6a34a8', '#b48af0', '#3a1a6a')

PEOPLE = {
 'grower':  dict(shirt=GREEN, legs=DENIM, bib=DENIM, hat='straw', hair='short', prop='can'),
 'growerf': dict(shirt=PINK, legs=DENIM, bib=DENIM, hat='sunhat', hair='braid', prop='can'),
 'crew_pot':   dict(shirt=CORAL, legs=DENIM_D, apron=BROWN, hat='cap', capc=ORANGE, hair='short', prop='pot'),
 'crew_water': dict(shirt=BLUESH, legs=DENIM, bib=DENIM, hat='bucket', hair='short', prop='can'),
 'crew_pest':  dict(shirt=CORAL, legs=DENIM, bib=DENIM, hat='helmet', hair='short', mask=True, tank=True, prop='spray'),
 'crew_fix':   dict(shirt=GREY, legs=GREY, coverall=True, belt=True, hat='cap', capc=BLACK, hair='short', prop='wrench'),
 'crew_load':  dict(shirt=GREEN, legs=DENIM, vest=HIVIS, hat='hardhat', hair='short', prop='box'),
 'crew_prize': dict(shirt=CREAM, legs=DENIM, vest=GOLD, hat='bigsun', hair='short', rosette=True, prop='shears'),
 'mgr':        dict(shirt=WHITE, legs=DENIM_D, tie=True, hat=None, hair='tidy', prop='clip'),
}
PEOPLE['crew'] = PEOPLE['crew_pot']

# ---------------- parts ----------------
GROUND = 54.0
def shadow(): return f'<ellipse cx="32" cy="{f(GROUND+.6)}" rx="9.5" ry="3" fill="#1d3a24" opacity=".2"/>'

def legs(p, view, fr):
    L = p['legs']; o = []
    # leg swing: (dx, lift) for back and front leg
    sw = {0: ((0, 0), (0, 0)), 1: ((-1.8, -.4), (1.9, 0)), 2: ((1.7, 0), (-1.6, -.4))}.get(fr, ((0, 0), (0, 0)))
    for i, (xx, (dx, lift)) in enumerate([(29.0, sw[0]), (34.6, sw[1])]):
        back = i == 0
        col = L if not back else C(L['shade'], L['shade'], None, L['ink'])
        x = xx + dx; top = 40.5; bot = GROUND - 3.2 + lift
        o.append(cel(rrect(x - 2.5, top, 5, bot - top + 1, 2), col['base'], col['shade'], col['hi'], col['ink'], s=(.7, 0), hion=not back))
        toe = 1.4 if view == 'front' else 1.0
        o.append(cel(ell(x + toe * .6, bot + 1.1, 3.1, 1.9), BOOT['base'] if not back else BOOT['shade'], BOOT['shade'], BOOT['hi'], BOOT['ink'], s=(.4, .6), hion=not back))
    return ''.join(o)

def torso_path(): return rrect(23.2, 27.0, 17.6, 16.4, 6)

def arm(p, x0, y0, x1, y1, back, hand=True):
    s = p['shirt']; col = C(s['shade'], s['shade'], None, s['ink']) if back else s
    o = [cel(limb(x0, y0, x1, y1, 4.8), col['base'], col['shade'], col['hi'], col['ink'], s=(.6, .4), hion=not back)]
    if hand: o.append(cel(ell(x1, y1 + .4, 2.3, 2.3), SK['hand'] if not back else SK['shade'], SK['shade'], None, SK['ink'], s=(.4, .5), hion=False))
    return ''.join(o)

def body(p, view):
    s = p['shirt']; o = []
    if p.get('tank') and view == 'front':   # sprayer tank peeking out behind the shoulders
        o.append(cel(rrect(20.0, 25.0, 7.5, 14, 3), YELLOW['base'], YELLOW['shade'], YELLOW['hi'], YELLOW['ink']))
    base = p['legs'] if p.get('coverall') else s
    o.append(cel(torso_path(), base['base'], base['shade'], base['hi'], base['ink'], s=(1.6, 1.0)))
    fx = 1.6 if view == 'front' else 0   # front details shift toward the facing side
    if view == 'front':
        if p.get('bib'):
            b = p['bib']; d = f"M{f(26+fx)},{f(33)} H{f(38.6+fx*.4)} V{f(41)} Q{f(38.6+fx*.4)},{f(43.6)} {f(35.6)},{f(43.6)} H{f(29)} Q{f(26+fx)},{f(43.6)} {f(26+fx)},{f(41)} Z"
            o.append(cel(d, b['base'], b['shade'], b['hi'], b['ink'], s=(1.0, .8)))
            for sx in (27.2 + fx, 37.6 + fx * .4):
                o.append(f'<path d="M{f(sx)},33.5 L{f(sx-.3)},27.6" stroke="{b["base"]}" stroke-width="2" stroke-linecap="round"/><path d="M{f(sx)},33.5 L{f(sx-.3)},27.6" stroke="{b["ink"]}" stroke-width=".5" stroke-linecap="round" opacity=".6"/>')
                o.append(f'<circle cx="{f(sx)}" cy="34" r=".9" fill="#ffd36a" stroke="#9a6a00" stroke-width=".4"/>')
            o.append(cel(rrect(30.6 + fx * .7, 36.2, 4.4, 3.2, 1), b['shade'], b['ink'], None, b['ink'], lw=.5, hion=False))
        if p.get('apron'):
            a = p['apron']; d = f"M{f(25.6+fx)},{f(31.5)} H{f(38.8+fx*.3)} L{f(39.4+fx*.3)},{f(44.6)} Q{f(32.5+fx)},{f(46)} {f(25)},{f(44.6)} Z"
            o.append(cel(d, a['base'], a['shade'], a['hi'], a['ink']))
            o.append(cel(rrect(29.4 + fx, 37.2, 6.6, 4, 1.2), a['shade'], a['ink'], None, a['ink'], lw=.5, hion=False))
            o.append(f'<path d="M{f(31.2+fx)},37.4 v-2.2 M{f(33.4+fx)},37.4 v-3" stroke="#6a4a2a" stroke-width=".8" stroke-linecap="round"/>')
        if p.get('coverall'):
            o.append(f'<path d="M{f(32+fx)},28 V41" stroke="{p["legs"]["ink"]}" stroke-width=".6" opacity=".7"/>')
            o.append(cel(rrect(26.5 + fx * .5, 30.2, 4, 3, .8), p['legs']['shade'], p['legs']['ink'], None, p['legs']['ink'], lw=.5, hion=False))
        if p.get('belt'):
            o.append(f'<path d="M23.6,38.4 H40.4" stroke="#2a2d33" stroke-width="2"/><rect x="{f(30.6+fx)}" y="37.3" width="3" height="2.2" rx=".4" fill="#d9dde3" stroke="#2a2d33" stroke-width=".4"/>')
        if p.get('vest'):
            v = p['vest']
            for d in (f"M23.4,{f(29.5)} Q24,28 {f(27.8+fx*.3)},28 L{f(29.6+fx)},43.4 L24.2,43.4 Q23.2,40 23.4,29.5 Z",
                      f"M40.6,{f(29.5)} Q40,28 {f(36.8+fx)},28 L{f(35.4+fx)},43.4 L39.8,43.4 Q40.8,40 40.6,29.5 Z"):
                o.append(cel(d, v['base'], v['shade'], v['hi'], v['ink']))
            if v is HIVIS:
                o.append('<path d="M23.6,36.2 H29.6 M35.2,36.2 H40.4 M23.8,39.4 H29.9 M35.0,39.4 H40.2" stroke="#e9eef2" stroke-width="1.2"/>')
        if p.get('tie'):
            o.append(f'<path d="M{f(30+fx)},28.2 L{f(33.4+fx)},28.2 L{f(31.7+fx)},30 Z" fill="#fff" stroke="#6a7385" stroke-width=".4"/>')
            o.append(cel(poly([(31.0 + fx, 29.6), (32.5 + fx, 29.6), (33.2 + fx, 37.6), (31.75 + fx, 39.4), (30.3 + fx, 37.6)]), '#2f5fb0', '#1f3f80', '#5a8ae0', '#132a5a', lw=.6))
        if p.get('rosette'):
            o.append(f'<circle cx="{f(36.4+fx*.4)}" cy="32" r="1.9" fill="#8a4fd0" stroke="#3a1a6a" stroke-width=".5"/><circle cx="{f(36.4+fx*.4)}" cy="32" r=".8" fill="#ffd23a"/><path d="M{f(35.6+fx*.4)},33.4 l-.6,2.4 M{f(37.2+fx*.4)},33.4 l.6,2.4" stroke="#8a4fd0" stroke-width=".9"/>')
    else:   # back view details
        if p.get('bib'):
            b = p['bib']
            o.append(f'<path d="M26.4,28.4 L35.6,36.6 M37.6,28.4 L28.4,36.6" stroke="{b["base"]}" stroke-width="2.2" stroke-linecap="round"/><path d="M26.4,28.4 L35.6,36.6 M37.6,28.4 L28.4,36.6" stroke="{b["ink"]}" stroke-width=".5" opacity=".55"/>')
            d = f"M24.4,37 H39.6 V41.6 Q39.6,43.6 37.4,43.6 H26.6 Q24.4,43.6 24.4,41.6 Z"
            o.append(cel(d, b['base'], b['shade'], b['hi'], b['ink'], s=(1.0, .8)))
        if p.get('apron'):
            o.append(f'<path d="M23.6,38 H40.4" stroke="{p["apron"]["base"]}" stroke-width="1.4"/><path d="M31,38 l-1.6,3 M33,38 l1.6,3" stroke="{p["apron"]["base"]}" stroke-width="1.1" stroke-linecap="round"/>')
        if p.get('belt'): o.append('<path d="M23.6,38.4 H40.4" stroke="#2a2d33" stroke-width="2"/>')
        if p.get('vest'):
            v = p['vest']; o.append(cel(rrect(23.6, 28.2, 16.8, 15.2, 5), v['base'], v['shade'], v['hi'], v['ink']))
            if v is HIVIS: o.append('<path d="M23.8,36.2 H40.2 M23.8,39.4 H40.2" stroke="#e9eef2" stroke-width="1.3"/>')
            if v is GOLD: o.append('<path d="M32,28.4 V43" stroke="#c9951a" stroke-width=".6"/>')
        if p.get('tank'):
            o.append(cel(rrect(26.0, 26.0, 12, 15, 4), YELLOW['base'], YELLOW['shade'], YELLOW['hi'], YELLOW['ink']))
            o.append('<path d="M27,30 H37 M27,36.5 H37" stroke="#8a6000" stroke-width=".6"/><rect x="30.4" y="24.2" width="3.2" height="2.4" rx=".6" fill="#2a2d33"/>')
    return ''.join(o)

def head(p, view):
    o = []; hcx, hcy, r = 32.0, 20.2, 9.0
    hair = p['hair']
    if view == 'front':
        if hair == 'braid':   # braid falls behind the shoulder
            o.append(cel(limb(25.4, 22, 23.6, 34.5, 3.6), HR['base'], HR['shade'], None, HR['ink'], hion=False))
            for yy in (26, 29.2, 32.2): o.append(f'<path d="M22.4,{f(yy)} q1.6,1.4 3.4,0" stroke="{HR["ink"]}" stroke-width=".5" fill="none"/>')
            o.append(f'<circle cx="23.6" cy="35.4" r="1.2" fill="#ff86b2" stroke="#9a2a58" stroke-width=".4"/>')
        o.append(cel(ell(hcx, hcy, r, r * .97), SK['base'], SK['shade'], '#fff0e2', SK['ink'], s=(1.4, 1.3)))
        # ear on the far side, features pushed toward the facing side
        o.append(cel(ell(23.4, 21.2, 1.7, 2.2), SK['base'], SK['shade'], None, SK['ink'], hion=False, lw=.7))
        if hair in ('short', 'tidy', 'braid'):
            d = f"M{f(23.2)},{f(20.5)} Q{f(23)},{f(11.4)} {f(32.4)},{f(11.2)} Q{f(40.2)},{f(11.6)} {f(40.9)},{f(18.6)} Q{f(36)},{f(15.6)} {f(30.4)},{f(16.6)} Q{f(26.4)},{f(17.4)} {f(25.4)},{f(21.6)} Z"
            o.append(cel(d, HR['base'], HR['shade'], '#b57a4e', HR['ink']))
        ex = 2.2
        for i, (x, rx) in enumerate([(30.0 + ex, .82), (35.6 + ex, 1.0)]):
            o.append(f'<ellipse cx="{f(x)}" cy="21.6" rx="{f(rx)}" ry="1.45" fill="#3a2b3d"/><circle cx="{f(x-.3)}" cy="21.0" r=".38" fill="#fff"/>')
        o.append(f'<path d="M{f(29.3+ex)},18.6 q1,-.6 1.9,-.1 M{f(34.9+ex)},18.6 q1,-.6 2,-.1" stroke="{HR["ink"]}" stroke-width=".55" fill="none" stroke-linecap="round"/>')
        o.append(f'<ellipse cx="{f(27.8+ex)}" cy="24.4" rx="1.6" ry="1" fill="#ff8f8f" opacity=".6"/><ellipse cx="{f(38.0+ex)}" cy="24.2" rx="1.4" ry=".95" fill="#ff8f8f" opacity=".6"/>')
        o.append(f'<path d="M{f(31.6+ex)},25.2 q1.7,1.7 3.6,.1" stroke="#7a3b3b" stroke-width=".9" fill="none" stroke-linecap="round"/>')
        o.append(f'<path d="M{f(38.2+ex)},22.6 q.9,.6 .2,1.4" stroke="{SK["ink"]}" stroke-width=".6" fill="none" stroke-linecap="round"/>')
    else:
        o.append(cel(ell(hcx, hcy, r, r * .97), SK['base'], SK['shade'], None, SK['ink'], s=(1.4, 1.3), hion=False))
        o.append(cel(ell(40.4, 21.4, 1.6, 2.1), SK['base'], SK['shade'], None, SK['ink'], hion=False, lw=.7))
        if hair in ('short', 'tidy', 'braid'):
            d = f"M{f(23.1)},{f(22.4)} Q{f(22.6)},{f(11.2)} {f(32)},{f(11.1)} Q{f(41.2)},{f(11.4)} {f(40.6)},{f(19.6)} Q{f(40.2)},{f(25.6)} {f(37.6)},{f(27.2)} Q{f(32)},{f(28.6)} {f(26.2)},{f(27.0)} Q{f(23.4)},{f(25.4)} {f(23.1)},{f(22.4)} Z"
            o.append(cel(d, HR['base'], HR['shade'], '#b57a4e', HR['ink']))
            o.append(f'<path d="M28,15 q1.5,5 .8,10 M33.5,14 q1,6 0,12 M37.6,16 q.6,4 -.6,8.6" stroke="{HR["shade"]}" stroke-width=".7" fill="none" stroke-linecap="round"/>')
        if hair == 'braid':
            o.append(cel(limb(32.4, 26.6, 32.0, 38.6, 3.6), HR['base'], HR['shade'], None, HR['ink'], hion=False))
            for yy in (30, 33.2, 36.2): o.append(f'<path d="M30.4,{f(yy)} q1.6,1.4 3.4,0" stroke="{HR["ink"]}" stroke-width=".5" fill="none"/>')
            o.append('<circle cx="32" cy="39.6" r="1.3" fill="#ff86b2" stroke="#9a2a58" stroke-width=".4"/>')
    if p.get('mask') and view == 'front':
        o.append(cel(ell(36.6, 25.4, 3.6, 2.6), '#e9edf2', '#c3ccd6', '#ffffff', '#5a6472', lw=.7))
        o.append('<circle cx="38.6" cy="25.8" r="1.1" fill="#7a8492" stroke="#3a4250" stroke-width=".4"/>')
    o.append(hat(p, view))
    return ''.join(o)

def hat(p, view):
    h = p.get('hat'); o = []; fr = view == 'front'; tilt = -5 if fr else 5
    if h == 'straw':
        o.append(cel(ell(32.6, 15.6, 14.2, 4.4, tilt), STRAW['base'], STRAW['shade'], STRAW['hi'], STRAW['ink'], s=(.8, 1.4)))
        o.append(cel(f"M24.8,15.6 Q24.8,6.4 32.6,6.2 Q40.2,6.4 40.4,14.6 Q32.6,17.6 24.8,15.6 Z", STRAW['base'], STRAW['shade'], STRAW['hi'], STRAW['ink'], s=(1.4, .8)))
        o.append(f'<path d="M25,13.4 Q32.6,16.2 40.2,12.6 L40.4,14.6 Q32.6,17.6 24.8,15.4 Z" fill="{RED["base"]}" stroke="{RED["ink"]}" stroke-width=".5"/>')
        o.append(f'<path d="M20,17 q2,1 4,.6 M40.6,15 q2.4,.2 4.4,-1" stroke="{STRAW["ink"]}" stroke-width=".45" fill="none" opacity=".6"/>')
    elif h == 'sunhat':
        o.append(cel(ell(32.4, 15.4, 15.4, 4.9, tilt), '#ffe9a6', '#e3c46a', '#fff8d8', '#8a6a1a', s=(.8, 1.5)))
        o.append(cel("M25.4,15.4 Q25.4,7 32.4,6.8 Q39.4,7 39.6,14.4 Q32.4,17.2 25.4,15.4 Z", '#ffe9a6', '#e3c46a', '#fff8d8', '#8a6a1a', s=(1.3, .8)))
        o.append('<path d="M25.6,13.6 Q32.4,16 39.4,12.8 L39.6,14.4 Q32.4,17.2 25.4,15.4 Z" fill="#ff86b2" stroke="#9a2a58" stroke-width=".5"/>')
        fx = 26.6 if fr else 37.8
        for k in range(5):
            a = k * 2 * math.pi / 5; o.append(f'<circle cx="{f(fx+math.cos(a)*1.3)}" cy="{f(12.8+math.sin(a)*1.3)}" r="1.15" fill="#ff6fa8" stroke="#9a2a58" stroke-width=".4"/>')
        o.append(f'<circle cx="{f(fx)}" cy="12.8" r=".8" fill="#ffe14a"/>')
    elif h == 'bigsun':
        o.append(cel(ell(32.4, 15.0, 16.4, 5.0, tilt), CREAM['base'], CREAM['shade'], CREAM['hi'], CREAM['ink'], s=(.8, 1.5)))
        o.append(cel("M25.2,15 Q25.2,6.2 32.4,6 Q39.6,6.2 39.8,14 Q32.4,17 25.2,15 Z", CREAM['base'], CREAM['shade'], CREAM['hi'], CREAM['ink'], s=(1.3, .8)))
        o.append(f'<path d="M25.4,13 Q32.4,15.6 39.6,12.2 L39.8,14 Q32.4,17 25.2,15 Z" fill="{PURPLE["base"]}" stroke="{PURPLE["ink"]}" stroke-width=".5"/>')
        o.append(f'<circle cx="{f(37.2 if fr else 27.6)}" cy="13.2" r="1.6" fill="#ffd23a" stroke="#7a5600" stroke-width=".5"/>')
    elif h == 'bucket':
        o.append(cel(f"M20.4,17.6 Q32.4,12.4 44.4,17.6 Q42,19.6 32.4,19.2 Q23,19.6 20.4,17.6 Z", KHAKI['base'], KHAKI['shade'], KHAKI['hi'], KHAKI['ink'], s=(.6, .9)))
        o.append(cel("M24.8,16.6 Q25.6,7.4 32.6,7.2 Q39.6,7.4 40.2,16 Q32.6,18 24.8,16.6 Z", KHAKI['base'], KHAKI['shade'], KHAKI['hi'], KHAKI['ink'], s=(1.3, .8)))
        o.append('<path d="M25,14 Q32.6,16 40,13.4 L40.2,15.6 Q32.6,18 24.9,16.2 Z" fill="#3a7fd6" stroke="#1d4e94" stroke-width=".5"/>')
    elif h == 'hardhat':
        o.append(cel(ell(32.4, 15.8, 11.4, 3.2, tilt), YELLOW['base'], YELLOW['shade'], YELLOW['hi'], YELLOW['ink'], s=(.6, 1.0)))
        o.append(cel("M23.6,15.8 Q23.8,5.8 32.4,5.6 Q41,5.8 41.2,15.2 Q32.4,17.8 23.6,15.8 Z", YELLOW['base'], YELLOW['shade'], YELLOW['hi'], YELLOW['ink'], s=(1.5, .9)))
        o.append(f'<path d="M32.6,5.8 Q{f(33.4 if fr else 31.6)},10 {f(33.2 if fr else 31.8)},16.4" stroke="{YELLOW["shade"]}" stroke-width="1.6" fill="none"/>')
    elif h == 'helmet':
        o.append(cel("M23.4,17.4 Q23.4,6.6 32.4,6.4 Q41.4,6.6 41.4,16.6 Q32.4,18.8 23.4,17.4 Z", WHITE['base'], WHITE['shade'], WHITE['hi'], WHITE['ink'], s=(1.5, .9)))
        if fr:
            o.append(cel(rrect(28.4, 11.2, 12.4, 4, 1.8), '#7fd0ff', '#4aa6e0', '#c8eeff', '#1d4e94', lw=.7))
        else:
            o.append('<path d="M24,13.2 Q32.4,15.4 40.8,12.6" stroke="#2a2d33" stroke-width="1.2" fill="none"/>')
    elif h == 'cap':
        cc = p['capc']
        o.append(cel("M23.4,16.4 Q23.6,7.2 32.4,7.0 Q41.2,7.2 41.4,15.8 Q32.4,17.6 23.4,16.4 Z", cc['base'], cc['shade'], cc['hi'], cc['ink'], s=(1.4, .8)))
        if fr: o.append(cel("M35.6,14.6 Q44,13.4 46.4,15.8 Q42.2,17.8 36.4,17 Z", cc['shade'], cc['ink'], None, cc['ink'], hion=False))
        else:  o.append(cel("M30.8,15.6 Q39.4,13.6 42.4,15.2 Q39,17.4 32,17.4 Z", cc['shade'], cc['ink'], None, cc['ink'], hion=False))
        o.append(f'<circle cx="32.6" cy="7.4" r=".9" fill="{cc["shade"]}" stroke="{cc["ink"]}" stroke-width=".4"/>')
    return ''.join(o)

# ---------------- props for the work and homestead poses ----------------
def prop(kind, x, y):
    if kind == 'can':
        return (cel(rrect(x, y - 3, 7.4, 6.4, 1.4), '#58a8ff', '#3a7fd6', '#9acbff', '#1d4e94') +
                f'<path d="M{f(x+7)},{f(y-1)} L{f(x+11.4)},{f(y-4.6)}" stroke="#3a7fd6" stroke-width="1.6" stroke-linecap="round"/>'
                f'<ellipse cx="{f(x+11.8)}" cy="{f(y-5)}" rx="1.4" ry=".9" fill="#58a8ff" stroke="#1d4e94" stroke-width=".5"/>'
                f'<path d="M{f(x+1)},{f(y-3)} Q{f(x+3.7)},{f(y-7.4)} {f(x+6.4)},{f(y-3)}" stroke="#1d4e94" stroke-width="1" fill="none"/>'
                f'<circle cx="{f(x+13.2)}" cy="{f(y-3.2)}" r=".7" fill="#7fd0ff"/><circle cx="{f(x+14.2)}" cy="{f(y-1.2)}" r=".6" fill="#7fd0ff"/><circle cx="{f(x+13.4)}" cy="{f(y+.6)}" r=".55" fill="#7fd0ff"/>')
    if kind == 'pot':
        return (cel(poly([(x, y - 3), (x + 7, y - 3), (x + 6, y + 3), (x + 1, y + 3)]), '#ee8656', '#c9643a', '#ffb98f', '#7a3216') +
                ''.join(f'<circle cx="{f(x+1.6+k*1.9)}" cy="{f(y-4.4-(k%2))}" r="1.4" fill="#ff6fa8" stroke="#9a2a58" stroke-width=".4"/>' for k in range(3)) +
                f'<path d="M{f(x+1)},{f(y-3.6)} q2.6,-1.6 5,0" stroke="#3a9e55" stroke-width="1" fill="none"/>')
    if kind == 'spray':
        return (f'<path d="M{f(x-2)},{f(y+1)} Q{f(x-6)},{f(y+6)} {f(x-9)},{f(y+2)}" stroke="#2a2d33" stroke-width=".8" fill="none"/>'
                f'<path d="M{f(x)},{f(y)} L{f(x+10)},{f(y-4)}" stroke="#2a2d33" stroke-width="1.3" stroke-linecap="round"/>'
                + ''.join(f'<circle cx="{f(x+11.6+k*1.3)}" cy="{f(y-4.6-k*.5+(k%2)*1.2)}" r="{f(1.1-k*.15)}" fill="#e9ffe9" opacity=".85"/>' for k in range(4)))
    if kind == 'wrench':
        return (f'<path d="M{f(x)},{f(y)} L{f(x+7)},{f(y-6)}" stroke="#9aa4b0" stroke-width="2" stroke-linecap="round"/>'
                f'<path d="M{f(x)},{f(y)} L{f(x+7)},{f(y-6)}" stroke="#4a525c" stroke-width=".5" stroke-linecap="round" opacity=".7"/>'
                f'<circle cx="{f(x+7.6)}" cy="{f(y-6.6)}" r="2" fill="#9aa4b0" stroke="#4a525c" stroke-width=".6"/><circle cx="{f(x+8.4)}" cy="{f(y-7.4)}" r=".9" fill="#e9ecf0"/>'
                f'<path d="M{f(x+10)},{f(y-9.6)} l1,-1.6 M{f(x+11)},{f(y-7.6)} l1.8,-.4 M{f(x+9)},{f(y-10.6)} l.2,-1.8" stroke="#ffd23a" stroke-width=".8" stroke-linecap="round"/>')
    if kind == 'box':
        return (cel(poly([(x, y - 4), (x + 5, y - 6.4), (x + 11, y - 4), (x + 6, y - 1.6)]), '#e9b36a', '#c98a3a', '#ffd9a0', '#6a4210') +
                cel(poly([(x, y - 4), (x + 6, y - 1.6), (x + 6, y + 4.4), (x, y + 2)]), '#d39a52', '#b07a32', None, '#6a4210', hion=False) +
                cel(poly([(x + 6, y - 1.6), (x + 11, y - 4), (x + 11, y + 2), (x + 6, y + 4.4)]), '#b98440', '#8f6226', None, '#6a4210', hion=False) +
                f'<path d="M{f(x+2.5)},{f(y-5.2)} L{f(x+8.5)},{f(y-2.8)}" stroke="#8f6226" stroke-width="1"/>')
    if kind == 'shears':
        return (f'<path d="M{f(x)},{f(y)} L{f(x+6)},{f(y-4)} M{f(x+1)},{f(y-1.6)} L{f(x+6.4)},{f(y-2.2)}" stroke="#9aa4b0" stroke-width="1.2" stroke-linecap="round"/>'
                f'<circle cx="{f(x-1)}" cy="{f(y+1)}" r="1.2" fill="none" stroke="#c43a2e" stroke-width="1"/><circle cx="{f(x)}" cy="{f(y-2.4)}" r="1.2" fill="none" stroke="#c43a2e" stroke-width="1"/>')
    if kind == 'clip':
        return (cel(rrect(x, y - 5, 6.4, 8.4, .8), '#c98a3a', '#a86e26', '#e9b36a', '#5a3a10') +
                f'<rect x="{f(x+.9)}" y="{f(y-3.6)}" width="4.6" height="6" fill="#fff"/><path d="M{f(x+1.6)},{f(y-2)} h3 M{f(x+1.6)},{f(y-.6)} h3 M{f(x+1.6)},{f(y+.8)} h2" stroke="#8a96a3" stroke-width=".5"/>'
                f'<rect x="{f(x+2.2)}" y="{f(y-5.6)}" width="2" height="1.4" rx=".3" fill="#8a96a3"/>')
    if kind == 'shovel':
        return (f'<path d="M{f(x)},{f(y)} L{f(x+9)},{f(y+12)}" stroke="#9c6a43" stroke-width="1.7" stroke-linecap="round"/>'
                + cel(poly([(x + 7.6, y + 11.4), (x + 11.6, y + 9.6), (x + 14.6, y + 15.4), (x + 12, y + 17.4)]), '#b4bec8', '#8a96a3', '#e9ecf0', '#363e47'))
    if kind == 'hammer':
        return (f'<path d="M{f(x)},{f(y)} L{f(x+3)},{f(y-8)}" stroke="#9c6a43" stroke-width="1.6" stroke-linecap="round"/>'
                + cel(rrect(x + .4, y - 11, 6.4, 3.2, .6), '#8a96a3', '#66727e', '#b4bec8', '#363e47'))
    return ''

# ---------------- assemble ----------------
def person(key, view, fr):
    U[0] = 0
    p = PEOPLE[key]; o = [shadow()]
    swing = {0: 0, 1: 2.0, 2: -2.0}.get(fr, 0) if isinstance(fr, int) else 0
    work = fr == 'work'; shovel = str(fr).startswith('shovel'); hammer = str(fr).startswith('hammer')
    o.append(legs(p, view, fr if isinstance(fr, int) else 0))
    # back arm first (it's behind the body)
    if view == 'front':
        o.append(arm(p, 24.6, 29.5, 22.6 - swing * .5, 39.0, back=True))
    else:
        o.append(arm(p, 39.4, 29.5, 41.4 + swing * .5, 39.0, back=True))
    o.append(body(p, view))
    if view == 'front':
        if work:
            o.append(arm(p, 38.6, 29.6, 43.6, 33.6, back=False)); o.append(prop(p['prop'], 42.6, 35.4))
        elif shovel:
            up = fr == 'shovel0'; o.append(prop('shovel', 37.2, 26.6 if up else 30.4)); o.append(arm(p, 38.6, 29.6, 41.6, 34.0 if up else 37.4, back=False))
        elif hammer:
            up = fr == 'hammer0'; o.append(arm(p, 38.6, 29.6, 43.0 if up else 42.6, 27.6 if up else 36.4, back=False)); o.append(prop('hammer', 42.0, 27.0 if up else 35.4))
        else:
            o.append(arm(p, 38.8, 29.5, 41.0 + swing * .5, 39.4, back=False))
    else:
        o.append(arm(p, 24.6, 29.5, 22.6 - swing * .5, 39.4, back=False))
    o.append(head(p, view))
    return '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 64 64" width="256" height="256"><!--hc-->' + ''.join(o) + '</svg>'

def build():
    out = {}
    for key in PEOPLE:
        for view in ('front', 'back'):
            for fr in (0, 1, 2): out[f'{key}_{view}_{fr}'] = person(key, view, fr)
        out[f'{key}_work'] = person(key, 'front', 'work')
    for g in ('grower', 'growerf'):
        for fr in ('shovel0', 'shovel1', 'hammer0', 'hammer1'): out[f'{g}_{fr}'] = person(g, 'front', fr)
    return out

if __name__ == '__main__':
    out = build()
    json.dump(out, open('/home/claude/gfx/rig/people.json', 'w'))
    print(len(out), sum(len(v) for v in out.values()) // 1024, 'KB')
