"""Greenhouse vector sprite sheet: SVG <symbol>s on a 64x32 isometric tile.
Anchor = the floor tile's top vertex: (32,32) in a 64x64 symbol, (32,96) in a 64x128 symbol,
(64,80) in the 128x128 truck.
"""
import math, random, json

SYM = []      # (id, viewbox w, h, anchor, svg body)
DEFS = []

def lin(id, stops, x1=0, y1=0, x2=0, y2=1):
    s = ''.join(f'<stop offset="{o}" stop-color="{c}"{f" stop-opacity=\"{a}\"" if a is not None else ""}/>' for o, c, a in stops)
    DEFS.append(f'<linearGradient id="{id}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{s}</linearGradient>')
def rad(id, stops, cx=.35, cy=.3, r=.8):
    s = ''.join(f'<stop offset="{o}" stop-color="{c}"{f" stop-opacity=\"{a}\"" if a is not None else ""}/>' for o, c, a in stops)
    DEFS.append(f'<radialGradient id="{id}" cx="{cx}" cy="{cy}" r="{r}">{s}</radialGradient>')

# palette gradients
lin('gGrass', [(0, '#8fd06c', None), (1, '#8fd06c', None)])
lin('gFloor', [(0, '#fbf6ec', None), (1, '#ece3d2', None)])
lin('gRoad', [(0, '#626a76', None), (1, '#626a76', None)])
lin('gWoodTop', [(0, '#ffcf8a', None), (1, '#f0a55c', None)], 0, 0, 1, 1)
lin('gWoodL', [(0, '#e0914f', None), (1, '#c97a3d', None)])
lin('gWoodR', [(0, '#c47236', None), (1, '#a85e2c', None)])
lin('gMetal', [(0, '#b9c9d8', None), (1, '#8aa0b4', None)])
lin('gSoil', [(0, '#8a5a3a', None), (1, '#6a4129', None)])
rad('gLeaf', [(0, '#c4f08f', None), (.55, '#6fc25a', None), (1, '#3a9447', None)])
rad('gLeafP', [(0, '#e9f59c', None), (.5, '#8fcf5e', None), (1, '#3f8f45', None)])
rad('gPot', [(0, '#ffb98f', None), (.6, '#ee8656', None), (1, '#c9643a', None)], .3, .3, .9)
rad('gMum', [(0, '#fff6b8', None), (.6, '#ffc93d', None), (1, '#f08a1f', None)])
rad('gPet', [(0, '#ffd6ef', None), (.5, '#f26bb5', None), (1, '#c23c8b', None)])
rad('gGer', [(0, '#ffb7a0', None), (.55, '#ff5a4a', None), (1, '#c92f33', None)])
FL = {'petunia': ('#ffd6ef', '#f26bb5', '#c23c8b'), 'vinca': ('#ece3ff', '#9b7ff0', '#5b3fc0'), 'geranium': ('#ffb7a0', '#ff5a4a', '#c92f33'),
      'begonia': ('#ffd9b8', '#ff9a4a', '#d8642a'), 'mum': ('#fff6b8', '#ffc93d', '#f08a1f'), 'poinsettia': ('#ff9a9a', '#ef2f3f', '#a8121f'),
      'hydrangea': ('#e2f1ff', '#7fb4f5', '#3d74d6'), 'kale': ('#f3e2fb', '#c48fe0', '#7f4aa8'),
      'orchid': ('#ffffff', '#f6c9ec', '#b8297f'), 'rose': ('#ff8a8a', '#d8202f', '#8a0f1c'), 'peony': ('#fff0f3', '#ffadc4', '#e0567f'), 'calla': ('#fffdf3', '#f6edcf', '#c9b77a')}
FL.update({'tomato': ('#ffb0a0', '#ef3b2c', '#a8121f'), 'pepper': ('#fff1a0', '#f2a531', '#c2571f'), 'lettuce': ('#eaffc4', '#9be06a', '#4f9a3f'),
           'cabbage': ('#e2f4ef', '#8fc7b5', '#4f8a7a'), 'cucumber': ('#fff6a8', '#f2d43a', '#b8941f'), 'basil': ('#d8ffb0', '#5fcf4a', '#257a2f')})
for k, (a, b2, c) in FL.items(): rad(f'gF_{k}', [(0, a, None), (.55, b2, None), (1, c, None)])
rad('gLettuce', [(0, '#f3ffd0', None), (.5, '#a8e070', None), (1, '#5aa84a', None)])
rad('gCabbage', [(0, '#e6f6f0', None), (.5, '#94c9b9', None), (1, '#4c8576', None)])
rad('gBasil', [(0, '#dcffb4', None), (.5, '#6fd256', None), (1, '#2f8a38', None)])
rad('gTom', [(0, '#c8eea0', None), (.55, '#5aa94a', None), (1, '#2e6e35', None)])
rad('gLeafD', [(0, '#9fd88a', None), (.55, '#3f9152', None), (1, '#1f5a34', None)])
rad('gFern', [(0, '#b9e88f', None), (.5, '#4fa553', None), (1, '#1f6a38', None)])
rad('gKale', [(0, '#e7c6f5', None), (.45, '#a77bc4', None), (1, '#4f8a5a', None)])
TYPE = {'petunia': 'petal', 'vinca': 'petal', 'geranium': 'umbel', 'begonia': 'umbel', 'mum': 'pom', 'poinsettia': 'bract',
        'hydrangea': 'mop', 'pothos': 'vine', 'fern': 'frond', 'kale': 'rosette',
        'orchid': 'orchid', 'rose': 'rose', 'peony': 'peony', 'calla': 'calla',
        'tomato': 'tom', 'pepper': 'pep', 'lettuce': 'lettuce', 'cabbage': 'cab', 'cucumber': 'cuke', 'basil': 'basil'}
VEG = ('tomato', 'pepper', 'lettuce', 'cabbage', 'cucumber', 'basil')
SHOW = ('orchid', 'rose', 'peony', 'calla')
STROKE = {'petal': None, 'umbel': None}
lin('gGlass', [(0, '#e6fbff', .85), (1, '#bdeef3', .35)])
lin('gCream', [(0, '#fff8ea', None), (1, '#f3e3c4', None)])
lin('gCreamR', [(0, '#ecd7b2', None), (1, '#d9bf93', None)])
rad('gGlow', [(0, '#fff3a6', None), (.5, '#ffb347', None), (1, '#ff6a3d', None)], .5, .5, .6)
lin('gCab', [(0, '#ff8a68', None), (1, '#e85a3c', None)])
lin('gBox', [(0, '#ffffff', None), (1, '#efe9dc', None)])
lin('gSky', [(0, '#dff4ff', None), (1, '#f6fff2', None)])
for k, c1, c2 in (('pot', '#f08a55', '#c4572c'), ('water', '#4fa8ff', '#1f6fd0'), ('pest', '#ff6a5a', '#d23a3a'),
                  ('fix', '#8f9aa8', '#56606b'), ('load', '#4fcf7a', '#1f8f4a')):
    rad(f'gI{k}', [(0, c1, None), (1, c2, None)], .35, .3, .85)

f2 = lambda v: f'{v:.1f}'.rstrip('0').rstrip('.')
def path(pts, close=True): return 'M' + ' L'.join(f'{f2(x)},{f2(y)}' for x, y in pts) + (' Z' if close else '')
def poly(pts, fill, stroke='none', sw=1, extra=''):
    return f'<path d="{path(pts)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" {extra}/>'
def circ(x, y, r, fill, stroke='none', sw=1, extra=''):
    return f'<circle cx="{f2(x)}" cy="{f2(y)}" r="{f2(r)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'
def ell(x, y, rx, ry, fill, extra=''):
    return f'<ellipse cx="{f2(x)}" cy="{f2(y)}" rx="{f2(rx)}" ry="{f2(ry)}" fill="{fill}" {extra}/>'

class Iso:
    def __init__(s, ax=32, ay=32): s.ax, s.ay = ax, ay
    def P(s, u, v, z=0): return (s.ax + (u - v) * 32, s.ay + (u + v) * 16 - z)
    def box(s, u0, v0, u1, v1, z0, z1, top, left, right, stroke, sw=1):
        P = s.P
        return (poly([P(u0, v1, z0), P(u1, v1, z0), P(u1, v1, z1), P(u0, v1, z1)], left, stroke, sw) +
                poly([P(u1, v0, z0), P(u1, v1, z0), P(u1, v1, z1), P(u1, v0, z1)], right, stroke, sw) +
                poly([P(u0, v0, z1), P(u1, v0, z1), P(u1, v1, z1), P(u0, v1, z1)], top, stroke, sw))
    def tile(s, fill, stroke='none'): return poly([s.P(0, 0), s.P(1, 0), s.P(1, 1), s.P(0, 1)], fill, stroke)

def add(id, body, w=64, h=64, anchor=(32, 32)): SYM.append((id, w, h, anchor, body))

# ------------------------------------------------------------------ ground
def grass(seed):
    I = Iso(); r = random.Random(seed); b = I.tile('url(#gGrass)')
    for _ in range(3 + seed // 2):
        u, v = r.uniform(.15, .85), r.uniform(.15, .85); x, y = I.P(u, v)
        b += f'<path d="M{f2(x-2)},{f2(y)} q1,-4 2,-6 q0,4 1,6 q1,-3 3,-4 q-1,3 -1,4" fill="none" stroke="#72bd57" stroke-width="1.1" stroke-linecap="round"/>'
    for _ in range(seed // 2):
        u, v = r.uniform(.2, .8), r.uniform(.2, .8); x, y = I.P(u, v)
        col = r.choice(['#ffffff', '#ffe066', '#ff9ccf'])
        b += ''.join(circ(x + dx, y + dy, 1.2, col) for dx, dy in ((-1.3, 0), (1.3, 0), (0, -1), (0, 1))) + circ(x, y, .9, '#ffcf3a')
    return b
add('grass_a', grass(0)); add('grass_b', grass(2)); add('grass_c', grass(4))

lin('gWinter', [(0, '#eef5fa', None), (1, '#eef5fa', None)])
VS = {'spring': ('#9be07a', '#6cc45a', ['#ffffff', '#ffe066', '#ff9ccf', '#c9a7ff']),
      'summer': ('#8fd06c', '#72bd57', ['#ffe066', '#ffffff']),
      'fall':   ('#c9b35a', '#a8923f', ['#e8772b', '#c9432f', '#f2b43a', '#d6602c'])}
def season_grass(season, seed):
    I = Iso(); r = random.Random(seed * 7 + len(season))
    if season == 'winter':
        b = I.tile('url(#gWinter)')
        for _ in range(2 + seed):     # soft drift shadows
            u, v = r.uniform(.25, .75), r.uniform(.25, .75); x, y = I.P(u, v)
            b += ell(x, y, r.uniform(5, 9), r.uniform(1.6, 2.6), '#c9dbea', 'opacity=".7"')
        for _ in range(seed):        # grass poking through
            u, v = r.uniform(.2, .8), r.uniform(.2, .8); x, y = I.P(u, v)
            b += f'<path d="M{f2(x-1.5)},{f2(y)} l1,-4 M{f2(x)},{f2(y)} l0,-5 M{f2(x+1.5)},{f2(y)} l-.5,-3.5" stroke="#6f9a63" stroke-width="1" stroke-linecap="round"/>'
            b += ell(x, y + .5, 3.4, 1.2, '#ffffff')
        for _ in range(4):
            u, v = r.uniform(.15, .85), r.uniform(.15, .85); x, y = I.P(u, v)
            b += circ(x, y, .7, '#ffffff')
        return b
    base, tuft, dots = VS[season]
    b = I.tile(base)
    for _ in range(2 + seed):
        u, v = r.uniform(.15, .85), r.uniform(.15, .85); x, y = I.P(u, v)
        b += f'<path d="M{f2(x-2)},{f2(y)} q1,-4 2,-6 q0,4 1,6 q1,-3 3,-4 q-1,3 -1,4" fill="none" stroke="{tuft}" stroke-width="1.1" stroke-linecap="round"/>'
    if season == 'fall':
        for _ in range(4 + seed * 2):
            u, v = r.uniform(.15, .85), r.uniform(.15, .85); x, y = I.P(u, v); col = r.choice(dots); a = r.randint(0, 180)
            b += f'<g transform="translate({f2(x)},{f2(y)}) rotate({a}) scale(1 .6)"><path d="M-3,0 q3,-3 6,0 q-3,3 -6,0 Z" fill="{col}"/><path d="M-3,0 h6" stroke="#7a3a1a" stroke-width=".4"/></g>'
    else:
        n = (2 + seed * 2) if season == 'spring' else seed
        for _ in range(n):
            u, v = r.uniform(.2, .8), r.uniform(.2, .8); x, y = I.P(u, v); col = r.choice(dots)
            b += ''.join(circ(x + dx, y + dy, 1.2, col) for dx, dy in ((-1.3, 0), (1.3, 0), (0, -1), (0, 1))) + circ(x, y, .9, '#ffcf3a')
    return b
for _ss in ('winter', 'spring', 'summer', 'fall'):
    for _i, _v in enumerate('abc'): add(f'grass_{_ss}_{_v}', season_grass(_ss, _i + 1))

def floor(drain=False):
    I = Iso(); b = I.tile('url(#gFloor)')
    for t in (.5,):
        b += f'<path d="M{f2(I.P(t,0)[0])},{f2(I.P(t,0)[1])} L{f2(I.P(t,1)[0])},{f2(I.P(t,1)[1])} M{f2(I.P(0,t)[0])},{f2(I.P(0,t)[1])} L{f2(I.P(1,t)[0])},{f2(I.P(1,t)[1])}" stroke="#e3d8c4" stroke-width="1"/>'
    b += poly([I.P(0, 0), I.P(1, 0), I.P(1, 1), I.P(0, 1)], 'none', '#d9ccb4', .8)
    if drain:
        b += ell(32, 48, 6, 3, '#b9ad97') + ''.join(f'<path d="M{f2(28+i*2)},{f2(46.6+ (0))} l0,2.8" stroke="#8f846f" stroke-width=".9"/>' for i in range(5))
    return b
add('floor', floor()); add('floor_drain', floor(True))

def road(line):
    I = Iso(); b = I.tile('url(#gRoad)')
    if line:
        a, c = I.P(.25, .5), I.P(.75, .5)
        b += f'<path d="M{f2(a[0])},{f2(a[1])} L{f2(c[0])},{f2(c[1])}" stroke="#ffd36a" stroke-width="3" stroke-linecap="round"/>'
    return b
add('road', road(False)); add('road_line', road(True))

def dock():
    I = Iso(); b = I.box(0, 0, 1, 1, 0, 6, '#eee6d6', '#d6ccb8', '#c2b7a2', '#a99d87', .8)
    for i in range(4):
        u = .08 + i * .24
        b += poly([I.P(u, 1, 0), I.P(u + .12, 1, 0), I.P(u + .2, 1, 6), I.P(u + .08, 1, 6)], '#ffc83d')
    return b
add('dock', dock())

# ------------------------------------------------------------------ benches
def bench(kind, tray=False):
    I = Iso(); b = ''; st = '#7a4423'
    u0 = .05 if kind in ('left', 'single') else 0
    u1 = .95 if kind in ('right', 'single') else 1
    v0, v1 = .1, .9
    legs = [(u0 + .05, v1 - .1), (u1 - .12, v1 - .1), (u1 - .12, v0 + .04), (u0 + .05, v0 + .04)]
    if kind == 'mid': legs = [(u1 - .12, v1 - .1), (u1 - .12, v0 + .04)]
    if kind == 'right': legs = legs[1:3]
    if kind == 'left': legs = [legs[0], legs[3]]
    for (lu, lv) in sorted(legs, key=lambda p: p[0] + p[1]):
        b += I.box(lu, lv, lu + .07, lv + .07, 0, 18, '#c9d8e4', 'url(#gMetal)', '#7f95a8', '#5d7185', .7)
    b += I.box(u0 + .06, v1 - .08, u1 - .06, v1 - .04, 6, 9, '#c9d8e4', 'url(#gMetal)', '#7f95a8', '#5d7185', .7)
    b += I.box(u0, v0, u1, v1, 18, 24, 'url(#gWoodTop)', 'url(#gWoodL)', 'url(#gWoodR)', st, 1)
    for t in (.3, .5, .7):  # slat lines
        a, c = I.P(u0 + .02, t, 24), I.P(u1 - .02, t, 24)
        b += f'<path d="M{f2(a[0])},{f2(a[1])} L{f2(c[0])},{f2(c[1])}" stroke="#d98a45" stroke-width=".8"/>'
    if tray:
        b += I.box(u0 + .07, v0 + .08, u1 - .07, v1 - .08, 24, 27, 'url(#gSoil)', '#5a3622', '#4a2c1b', '#3a2215', .8)
        r = random.Random(kind)
        for _ in range(14):
            x, y = I.P(r.uniform(u0 + .12, u1 - .12), r.uniform(.25, .75), 27)
            b += circ(x, y, .7, '#a87452')
    return b
for k in ('left', 'mid', 'right', 'single'): add(f'bench_{k}', bench(k))
for k in ('left', 'mid', 'right'): add(f'bench_{k}_tray', bench(k, True))

# ------------------------------------------------------------------ plants
def cluster(x, y, r, grad='url(#gLeaf)', stroke='#2f7a3f', seed=0):
    rr = random.Random(seed); b = ''
    for dx, dy, k in sorted([(-.5, -.05, .62), (.48, -.1, .6), (0, -.5, .66), (-.28, .22, .55), (.3, .24, .55), (.05, .02, .6)], key=lambda p: p[1]):
        b += circ(x + dx * r * 1.1, y + dy * r, r * k, grad, stroke, .7)
    b += ell(x - r * .35, y - r * .55, r * .28, r * .16, '#ffffff', 'opacity=".45"')
    return b
def heart(x, y, s, fill, stroke):
    return (f'<path d="M{f2(x)},{f2(y+s*.9)} C{f2(x-s*1.4)},{f2(y)} {f2(x-s*.7)},{f2(y-s*1.1)} {f2(x)},{f2(y-s*.35)} '
            f'C{f2(x+s*.7)},{f2(y-s*1.1)} {f2(x+s*1.4)},{f2(y)} {f2(x)},{f2(y+s*.9)} Z" fill="{fill}" stroke="{stroke}" stroke-width=".6"/>')
def flat(crop, stage):
    I = Iso(); b = ''; r = random.Random(hash((crop, stage)) & 0xffff); base = 24
    if stage == 0:
        b += I.box(.12, .18, .88, .82, base, base + 3, 'url(#gSoil)', '#5a3622', '#4a2c1b', '#3a2215', .8)
        for i in range(4):
            for j in range(3):
                x, y = I.P(.22 + i * .19, .3 + j * .2, base + 3)
                b += (f'<path d="M{f2(x)},{f2(y)} l0,-2.5" stroke="#3f9a4a" stroke-width="1"/>' +
                      ell(x - 1.6, y - 3, 1.8, 1, '#8fda6a', f'transform="rotate(-25 {f2(x-1.6)} {f2(y-3)})"') +
                      ell(x + 1.6, y - 3, 1.8, 1, '#6fc25a', f'transform="rotate(25 {f2(x+1.6)} {f2(y-3)})"'))
        return b
    R = {1: 4.2, 2: 6.6, 3: 6.8}[stage]
    spots = sorted([(u, v) for v in (.3, .7) for u in (.2, .5, .8)], key=lambda p: p[0] + p[1])
    for n, (u, v) in enumerate(spots):
        x, y = I.P(u, v, base)
        if crop in SHOW:  # glazed showcase pot with a gold band
            b += poly([(x - 4.6, y - 5), (x + 4.6, y - 5), (x + 3.4, y + 1.8), (x - 3.4, y + 1.8)], '#f7f3ea', '#9c8a5c', .7)
            b += poly([(x - 4.3, y - 3.6), (x + 4.3, y - 3.6), (x + 4.1, y - 2.6), (x - 4.1, y - 2.6)], '#d9b44a')
            b += ell(x, y - 5, 5.2, 1.8, '#ffffff', 'stroke="#9c8a5c" stroke-width=".7"')
        elif crop in VEG:  # black plastic cell pack
            b += poly([(x - 4.4, y - 4.4), (x + 4.4, y - 4.4), (x + 3.6, y + 1.8), (x - 3.6, y + 1.8)], '#2e2e2e', '#151515', .7)
            b += poly([(x - 4.4, y - 4.4), (x + 4.4, y - 4.4), (x + 4.1, y - 3.3), (x - 4.1, y - 3.3)], '#4a4a4a')
            b += ell(x, y - 4.4, 4.6, 1.5, '#6a4129', 'stroke="#151515" stroke-width=".6"')
        else:  # terracotta pot
            b += poly([(x - 4.6, y - 5), (x + 4.6, y - 5), (x + 3.4, y + 1.8), (x - 3.4, y + 1.8)], 'url(#gPot)', '#a9512c', .7)
            b += ell(x, y - 5, 5.2, 1.8, '#f6a576', 'stroke="#a9512c" stroke-width=".7"')
        cy = y - 5 - R * .55
        T = TYPE[crop]; G = f'url(#gF_{crop})'; dk = FL.get(crop, ('', '', '#2f7a3f'))[2]
        if T == 'vine':
            b += cluster(x, cy, R * .85, 'url(#gLeafP)', '#2f7a3f', n + stage)
            for k in range(3 if stage == 1 else 6):
                a = (k / 6) * math.tau + .3
                b += heart(x + math.cos(a) * R * .55, cy + math.sin(a) * R * .35 - 1, 1.9 + stage * .2, '#7fcf5f' if k % 2 else '#e6f08c', '#2f7a3f')
            if stage >= 2 and v > .5:
                vx = x - 2; vy = y - 2
                b += f'<path d="M{f2(vx)},{f2(vy)} q-3,5 -1,9 q2,4 -1,8" fill="none" stroke="#3f8f45" stroke-width="1"/>'
                b += heart(vx - 1.5, vy + 6, 1.6, '#8fd16a', '#2f7a3f') + heart(vx - .5, vy + 12, 1.5, '#e6f08c', '#2f7a3f')
            continue
        if T == 'frond':
            b += cluster(x, cy + 1, R * .8, 'url(#gFern)', '#1f5a34', n + stage)
            for a in (-2.3, -1.6, -.9, -.3):
                L = R * (1.0 + .25 * (stage == 3)); ex, ey = x + math.cos(a) * L, cy + math.sin(a) * L * .8
                b += f'<path d="M{f2(x)},{f2(cy)} Q{f2((x+ex)/2)},{f2(min(cy,ey)-2)} {f2(ex)},{f2(ey)}" fill="none" stroke="#2f7a3f" stroke-width="1.3" stroke-linecap="round"/>'
                for t in (.35, .6, .85):
                    px2, py2 = x + (ex - x) * t, cy + (ey - cy) * t - 1.2
                    b += ell(px2, py2, 1.6, .8, '#5fb35a', f'transform="rotate({f2(math.degrees(a)+60)} {f2(px2)} {f2(py2)})"')
            continue
        if T == 'orchid':
            for a, sx in ((-.5, -1), (.4, 1)):
                b += ell(x + sx * 2.4, cy + R * .45, R * .55, R * .22, 'url(#gLeafD)', f'stroke="#1f5a34" stroke-width=".6" transform="rotate({f2(math.degrees(a))} {f2(x + sx * 2.4)} {f2(cy + R * .45)})"')
            if stage >= 2:
                b += f'<path d="M{f2(x)},{f2(cy+R*.4)} C{f2(x+1)},{f2(cy-R*1.2)} {f2(x+5)},{f2(cy-R*1.5)} {f2(x+7)},{f2(cy-R*.9)}" fill="none" stroke="#5a7a3a" stroke-width=".9"/>'
            if stage == 2:
                for t in (.6, .8, 1): b += circ(x + 7 * t, cy - R * (1.4 - .4 * t), 1, '#f6c9ec', '#b8297f', .4)
            if stage == 3:
                for fx, fy in ((x + 1.6, cy - R * 1.05), (x + 4.6, cy - R * 1.3), (x + 7, cy - R * .85)):
                    for ang in (-150, -30, 90):
                        rad_ = math.radians(ang); b += ell(fx + math.cos(rad_) * 1.6, fy + math.sin(rad_) * 1.6, 1.5, 1, '#ffffff', f'stroke="#d79ac9" stroke-width=".35" transform="rotate({ang} {f2(fx + math.cos(rad_) * 1.6)} {f2(fy + math.sin(rad_) * 1.6)})"')
                    b += circ(fx - 1.5, fy + .2, 1.6, '#ffffff', '#d79ac9', .35) + circ(fx + 1.5, fy + .2, 1.6, '#ffffff', '#d79ac9', .35)
                    b += circ(fx, fy + .6, .9, '#b8297f') + circ(fx, fy + .3, .35, '#ffd84a')
            continue
        if T == 'calla':
            for a in (-.35, -.1, .2, .45):
                lx_, ly_ = x + a * 9, cy - R * .3
                b += f'<path d="M{f2(x)},{f2(cy+R*.6)} Q{f2(x+a*4)},{f2(cy)} {f2(lx_)},{f2(ly_-R*.6)} Q{f2(lx_+1.6)},{f2(ly_)} {f2(x+.6)},{f2(cy+R*.6)} Z" fill="url(#gLeafD)" stroke="#1f5a34" stroke-width=".5"/>'
            if stage == 3:
                for k, ox in enumerate((-2.6, .4, 3.2)):
                    sx, sy = x + ox, cy - R * (1.1 + .15 * (k == 1))
                    b += f'<path d="M{f2(x+ox*.3)},{f2(cy+R*.4)} L{f2(sx)},{f2(sy+2)}" stroke="#4f8a3a" stroke-width=".9"/>'
                    b += f'<path d="M{f2(sx-.6)},{f2(sy+2.2)} C{f2(sx-2.6)},{f2(sy)} {f2(sx-2.4)},{f2(sy-2.6)} {f2(sx+.4)},{f2(sy-3.2)} C{f2(sx+2.6)},{f2(sy-3.4)} {f2(sx+2.4)},{f2(sy-1)} {f2(sx+.6)},{f2(sy+2.2)} Z" fill="url(#gF_calla)" stroke="#a8996a" stroke-width=".45"/>'
                    b += f'<path d="M{f2(sx)},{f2(sy+1)} L{f2(sx+.3)},{f2(sy-1.8)}" stroke="#f2c230" stroke-width="1" stroke-linecap="round"/>'
            elif stage == 2:
                for ox in (-2.2, 2.6): b += ell(x + ox, cy - R * .95, .9, 2, '#e8f0c8', 'stroke="#7a9a4a" stroke-width=".4"')
            continue
        if T in ('lettuce', 'cab'):
            gl = 'url(#gLettuce)' if T == 'lettuce' else 'url(#gCabbage)'; sk = '#3f7a35' if T == 'lettuce' else '#3a6a5e'
            rr_ = R * (.75 + .1 * stage)
            for a in range(7):
                ang = a * math.tau / 7 + .3
                b += ell(x + math.cos(ang) * rr_ * .55, cy + 1 + math.sin(ang) * rr_ * .35, rr_ * .55, rr_ * .38, gl, f'stroke="{sk}" stroke-width=".55" transform="rotate({f2(math.degrees(ang))} {f2(x + math.cos(ang) * rr_ * .55)} {f2(cy + 1 + math.sin(ang) * rr_ * .35)})"')
            b += circ(x, cy, rr_ * .42, gl, sk, .55)
            if T == 'lettuce' and stage >= 2:
                for a in range(5):
                    ang = a * math.tau / 5; b += f'<path d="M{f2(x+math.cos(ang)*rr_*.3)},{f2(cy+math.sin(ang)*rr_*.2)} q{f2(math.cos(ang)*2)},-1.2 {f2(math.cos(ang)*3.4)},.2" fill="none" stroke="#e6ffc0" stroke-width=".6"/>'
            if T == 'cab' and stage >= 2:
                b += circ(x, cy - .6, rr_ * .3, '#cfe9df', sk, .5) + f'<path d="M{f2(x-1.6)},{f2(cy-.4)} q1.6,-1.6 3.2,0" fill="none" stroke="{sk}" stroke-width=".4"/>'
            continue
        if T in ('tom', 'pep', 'basil', 'cuke'):
            gl = {'tom': 'url(#gTom)', 'pep': 'url(#gLeafD)', 'basil': 'url(#gBasil)', 'cuke': 'url(#gLeaf)'}[T]
            sk = {'tom': '#2a5e2f', 'pep': '#1f5a34', 'basil': '#257a2f', 'cuke': '#2f7a3f'}[T]
            if T == 'cuke':
                for a, s_ in ((-2.2, 1), (-.9, 1), (.3, .9)):
                    lx_, ly_ = x + math.cos(a) * R * .55, cy + math.sin(a) * R * .45
                    b += circ(lx_, ly_, R * .48 * s_, gl, sk, .6) + f'<path d="M{f2(lx_)},{f2(ly_+R*.3)} l0,-{f2(R*.5)}" stroke="{sk}" stroke-width=".4"/>'
                if stage >= 2: b += f'<path d="M{f2(x+R*.6)},{f2(cy)} q2,-2 1,-4 q-1,-1.5 .8,-2.6" fill="none" stroke="#5fae4a" stroke-width=".7"/>'
                if stage == 3:
                    for fx, fy in ((x - 2.2, cy - R * .7), (x + 2.6, cy - R * .4)):
                        b += ''.join(circ(fx + math.cos(a) * 1.2, fy + math.sin(a) * 1.2, 1.2, 'url(#gF_cucumber)', '#b8941f', .4) for a in [i * math.tau / 5 - 1.57 for i in range(5)])
                continue
            if T == 'basil':
                for k_ in range(3 if stage == 1 else 4):
                    ly_ = cy + R * .5 - k_ * R * .38; sp_ = R * (.7 - k_ * .12)
                    for sx in (-1, 1):
                        b += ell(x + sx * sp_ * .55, ly_, sp_ * .52, sp_ * .3, gl, f'stroke="{sk}" stroke-width=".55" transform="rotate({sx * -25} {f2(x + sx * sp_ * .55)} {f2(ly_)})"')
                b += ell(x - 1, cy - R * .45, 1.2, .6, '#ffffff', 'opacity=".5"')
                continue
            b += cluster(x, cy, R * (.85 if T == 'pep' else .95), gl, sk, n + stage * 7)
            if stage == 3 and T == 'tom':
                for fx, fy in ((x - 2.4, cy - R * .4), (x + 2.6, cy - R * .2)):
                    b += ''.join(circ(fx + math.cos(a) * 1, fy + math.sin(a) * 1, .9, '#ffe14a', '#c9a21f', .3) for a in [i * math.tau / 5 for i in range(5)])
                b += circ(x + .4, cy + R * .2, 1.6, 'url(#gF_tomato)', '#a8121f', .5) + circ(x - .1, cy + R * .2 - .6, .45, '#ffffff', extra='opacity=".6"')
            if stage == 3 and T == 'pep':
                for fx, fy in ((x - 2, cy + R * .1), (x + 2.4, cy - R * .25)):
                    b += f'<path d="M{f2(fx-1)},{f2(fy-1.6)} q-.6,2.6 .8,3.6 q1.4,-.6 1.2,-3.4 Z" fill="url(#gF_pepper)" stroke="#c2571f" stroke-width=".45"/>'
                    b += f'<path d="M{f2(fx)},{f2(fy-1.8)} l.3,-1" stroke="#2f7a3f" stroke-width=".7"/>'
            continue
        if T == 'rosette':
            b += cluster(x, cy, R, 'url(#gKale)', '#4a6e52', n + stage)
            if stage >= 2: b += circ(x, cy - 1, R * .35, G, '#6a3a90', .6) + circ(x - .6, cy - 1.6, R * .12, '#ffffff', extra='opacity=".5"')
            continue
        b += cluster(x, cy, R, 'url(#gLeafD)' if T == 'bract' else 'url(#gLeaf)', '#1f5a34' if T == 'bract' else '#2f7a3f', n + stage * 10)
        if stage == 3:
            if T == 'bract':
                for ox in (-2.4, 2.4):
                    bx_, by_ = x + ox, cy - R * .35
                    for a in range(6):
                        ang = a * math.tau / 6
                        b += ell(bx_ + math.cos(ang) * 2.2, by_ + math.sin(ang) * 1.4, 2.4, 1, G, f'stroke="{dk}" stroke-width=".4" transform="rotate({f2(math.degrees(ang))} {f2(bx_ + math.cos(ang) * 2.2)} {f2(by_ + math.sin(ang) * 1.4)})"')
                    b += circ(bx_, by_, .9, '#ffd84a')
            if T == 'mop':
                for ox in (-2, 2.2):
                    mx, my = x + ox, cy - R * .45
                    b += circ(mx, my, 3.8, G, dk, .6)
                    for a in range(6): b += circ(mx + math.cos(a) * 2, my + math.sin(a) * 1.8, .7, '#ffffff', extra='opacity=".55"')
            if T == 'petal':
                for k in range(3):
                    fx, fy = x + r.uniform(-R * .7, R * .7), cy + r.uniform(-R * .7, R * .1)
                    b += ''.join(circ(fx + math.cos(a) * 1.5, fy + math.sin(a) * 1.5, 1.6, G, dk, .5) for a in [i * math.tau / 5 - 1.57 for i in range(5)])
                    b += circ(fx, fy, 1, '#ffffff', extra='opacity=".8"') + circ(fx, fy, .45, '#f7c843')
            if T == 'umbel':
                for k, ox in enumerate((-2.5, 2.2)):
                    sx, sy = x + ox, cy - R * .6
                    b += f'<path d="M{f2(sx)},{f2(cy)} L{f2(sx + ox*.2)},{f2(sy - 3)}" stroke="#3f8a3f" stroke-width="1"/>'
                    for a in range(7):
                        ang = a * math.tau / 7; b += circ(sx + ox * .2 + math.cos(ang) * 2, sy - 5 + math.sin(ang) * 1.6, 1.5, G, dk, .4)
                    b += circ(sx + ox * .2, sy - 5, 1.4, G, dk, .4)
            if T == 'rose':
                for fx, fy in ((x - 2.6, cy - R * .5), (x + 2.4, cy - R * .6), (x, cy - R * .05)):
                    b += circ(fx, fy, 2.6, G, dk, .55)
                    b += f'<path d="M{f2(fx-1.6)},{f2(fy+.2)} q1.6,-2.2 3,-.4 q-.6,1.6 -2,1 q-.2,-1 .8,-1" fill="none" stroke="{dk}" stroke-width=".5"/>'
                    b += circ(fx - .6, fy - 1, .6, '#ffffff', extra='opacity=".4"')
            if T == 'peony':
                for fx, fy, rr_ in ((x - 1.8, cy - R * .5, 3.4), (x + 2.6, cy - R * .35, 2.8)):
                    for a in range(8):
                        ang = a * math.tau / 8; b += circ(fx + math.cos(ang) * rr_ * .55, fy + math.sin(ang) * rr_ * .4, rr_ * .55, G, dk, .4)
                    b += circ(fx, fy - .3, rr_ * .55, '#ffd2df', dk, .35) + circ(fx, fy - .4, rr_ * .25, '#fff0f3')
            if T == 'pom':
                for a, rr_ in ((0, .0), (.8, .55), (2.4, .55), (4.0, .55), (5.4, .5)):
                    mx, my = x + math.cos(a) * R * rr_, cy - 1 + math.sin(a) * R * rr_ * .6
                    b += circ(mx, my, 2.8, G, dk, .6) + circ(mx, my, 1.4, 'none', '#ffe38a', .6)
    return b
for crop in TYPE:
    for st in range(4):
        add(f'{crop}_{st}', flat(crop, st))

# ------------------------------------------------------------------ succulents (one pot per bench tile)
rad('gEche', [(0, '#e4f3ef', None), (.55, '#9cc7bd', None), (1, '#5f8f86', None)])
rad('gJade', [(0, '#b6e69a', None), (.55, '#5fae4a', None), (1, '#2f6e2f', None)])
rad('gAloe', [(0, '#c9ecb0', None), (.55, '#7fb86a', None), (1, '#3f7a3f', None)])
rad('gHaw', [(0, '#7fb08a', None), (.55, '#3f7a56', None), (1, '#1f4a36', None)])
rad('gCact', [(0, '#b9e08a', None), (.5, '#6fae4a', None), (1, '#3a7030', None)])
rad('gGlaze', [(0, '#a8d4ea', None), (.6, '#3f8fbf', None), (1, '#24607d', None)], .3, .3, .9)
def succ(sp, sz):
    I = Iso(); b = ''; x, y = I.P(.5, .5, 24)
    k = [.62, .82, 1.02, 1.22][sz]
    pw, ph = 7 * k + 2, 6 * k + 2
    if sz == 3:
        b += poly([(x - pw, y - ph), (x + pw, y - ph), (x + pw * .75, y + 2.4), (x - pw * .75, y + 2.4)], 'url(#gGlaze)', '#1f4f68', .7)
        b += ell(x, y - ph, pw + .6, 2.4, '#bfe4f4', 'stroke="#1f4f68" stroke-width=".7"')
    else:
        b += poly([(x - pw, y - ph), (x + pw, y - ph), (x + pw * .75, y + 2.4), (x - pw * .75, y + 2.4)], 'url(#gPot)', '#a9512c', .7)
        b += ell(x, y - ph, pw + .6, 2.4, '#f6a576', 'stroke="#a9512c" stroke-width=".7"')
    b += ell(x, y - ph, pw - .4, 1.7, '#cdb48a')  # gravel top dressing
    cy = y - ph - 1; R = 11 * k
    if sp == 'echeveria':
        for ring, n, rr_, col in ((0, 8, 1, 'url(#gEche)'), (1, 6, .66, 'url(#gEche)'), (2, 5, .36, '#dff0ea')):
            for a in range(n):
                ang = a * math.tau / n + ring * .4
                lx_, ly_ = x + math.cos(ang) * R * .55 * rr_, cy + math.sin(ang) * R * .3 * rr_ - ring * 1.2
                b += ell(lx_, ly_, R * .3 * (1 - ring * .2), R * .17, col, f'stroke="#4f7f76" stroke-width=".5" transform="rotate({f2(math.degrees(ang))} {f2(lx_)} {f2(ly_)})"')
                if ring == 0: b += circ(x + math.cos(ang) * R * .8, cy + math.sin(ang) * R * .44, .7, '#e07a9a')
    elif sp == 'haworthia':
        for a in range(9):
            ang = -math.pi / 2 + (a - 4) * .32
            tx, ty = x + math.cos(ang) * R * .75, cy - R * .2 + math.sin(ang) * R * .9
            b += f'<path d="M{f2(x-1.4)},{f2(cy+1)} L{f2(tx)},{f2(ty)} L{f2(x+1.4)},{f2(cy+1)} Z" fill="url(#gHaw)" stroke="#173a2a" stroke-width=".5"/>'
            for t in (.35, .6, .82): b += circ(x + (tx - x) * t, cy + 1 + (ty - cy - 1) * t, .45, '#e8f2ea')
    elif sp == 'aloe':
        for a in range(7):
            ang = -math.pi / 2 + (a - 3) * .42
            tx, ty = x + math.cos(ang) * R * .95, cy - R * .1 + math.sin(ang) * R * 1.05
            b += f'<path d="M{f2(x-2)},{f2(cy+1)} Q{f2((x+tx)/2-1.5)},{f2((cy+ty)/2)} {f2(tx)},{f2(ty)} Q{f2((x+tx)/2+1.5)},{f2((cy+ty)/2+1)} {f2(x+2)},{f2(cy+1)} Z" fill="url(#gAloe)" stroke="#2f5e2f" stroke-width=".55"/>'
            b += circ((x + tx) / 2, (cy + ty) / 2, .45, '#f2f8e8') + circ(x + (tx - x) * .7, cy + (ty - cy) * .7, .35, '#f2f8e8')
        if sz == 3: b += f'<path d="M{f2(x+1)},{f2(cy-R*.6)} L{f2(x+2)},{f2(cy-R*1.6)}" stroke="#7a8a3a" stroke-width=".8"/>' + ''.join(ell(x + 2.2, cy - R * 1.6 + i * 1.6, .7, 1.3, '#f2803a') for i in range(3))
    elif sp == 'jade':
        stem = '#8a6a3a'
        b += f'<path d="M{f2(x)},{f2(cy+1)} L{f2(x)},{f2(cy-R*.5)} M{f2(x)},{f2(cy-R*.25)} L{f2(x-R*.45)},{f2(cy-R*.75)} M{f2(x)},{f2(cy-R*.35)} L{f2(x+R*.5)},{f2(cy-R*.8)}" stroke="{stem}" stroke-width="{f2(1.1+sz*.35)}" stroke-linecap="round"/>'
        for px_, py_ in ((x, cy - R * .55), (x - R * .45, cy - R * .78), (x + R * .5, cy - R * .82), (x - R * .2, cy - R * .2), (x + R * .25, cy - R * .3)):
            for a in range(4 if sz else 3):
                ang = a * math.tau / 4 + .4; lx_, ly_ = px_ + math.cos(ang) * R * .2, py_ + math.sin(ang) * R * .12
                b += ell(lx_, ly_, R * .17, R * .11, 'url(#gJade)', f'stroke="#2a5a2a" stroke-width=".45" transform="rotate({f2(math.degrees(ang))} {f2(lx_)} {f2(ly_)})"')
    elif sp == 'cactus':
        h_ = R * (.75 + .1 * sz)
        b += ell(x, cy - h_ * .45, R * .55, h_ * .62, 'url(#gCact)', 'stroke="#2f5a2a" stroke-width=".7"')
        for dx in (-.32, 0, .32):
            b += f'<path d="M{f2(x+dx*R)},{f2(cy+.5)} Q{f2(x+dx*R*1.35)},{f2(cy-h_*.5)} {f2(x+dx*R)},{f2(cy-h_*1.02)}" fill="none" stroke="#3f7a35" stroke-width=".6"/>'
        for i in range(10):
            sx, sy = x + ((i % 5) - 2) * R * .2, cy - h_ * (.25 + .17 * (i // 5) + .1 * (i % 2))
            b += f'<path d="M{f2(sx)},{f2(sy)} l-1,-.6 M{f2(sx)},{f2(sy)} l1,-.6" stroke="#f3e6b0" stroke-width=".35"/>'
        if sz == 3:
            for a in range(5): b += ell(x + math.cos(a * 1.25) * 2, cy - h_ * 1.02 + math.sin(a * 1.25) * .8, 1.6, .9, '#ffd84a', 'stroke="#c99a1f" stroke-width=".35"')
            b += circ(x, cy - h_ * 1.05, 1, '#f08a3a')
    return b
for _sp in ('echeveria', 'jade', 'aloe', 'haworthia', 'cactus'):
    for _sz in range(4): add(f'suc_{_sp}_{_sz}', succ(_sp, _sz))

# ------------------------------------------------------------------ takeaway coffee
def coffee():
    b = ell(32, 58, 12, 3.4, '#1d3a24', 'opacity=".2"')
    b += '<path d="M21,22 L43,22 L39.5,57 Q32,59.5 24.5,57 Z" fill="#fbfaf6" stroke="#b9b2a2" stroke-width="1"/>'
    b += '<path d="M25.5,22 L28,57.5" stroke="#ffffff" stroke-width="2.2" opacity=".9"/>'
    b += '<path d="M21.9,32 L42.1,32 L40.6,46 L23.4,46 Z" fill="#c8955a" stroke="#9a6a38" stroke-width=".9"/>'
    b += '<path d="M23,36 h18 M23.6,42 h16.8" stroke="#b07f48" stroke-width=".6" opacity=".7"/>'
    b += '<circle cx="32" cy="39" r="4.2" fill="#f3e4c8" stroke="#9a6a38" stroke-width=".7"/><path d="M30.2,38.6 q1.8,-2.6 3.6,0 q-1.8,2.6 -3.6,0 Z" fill="#7a4a22"/>'
    b += '<path d="M19.5,22.5 Q19.5,17.5 24,17 L40,17 Q44.5,17.5 44.5,22.5 Z" fill="#ffffff" stroke="#a8a294" stroke-width="1"/>'
    b += '<rect x="19" y="21.5" width="26" height="3" rx="1.5" fill="#efece4" stroke="#a8a294" stroke-width=".8"/>'
    b += '<ellipse cx="37" cy="18.2" rx="2.2" ry=".9" fill="#5a5148"/>'
    for i, x in enumerate((27, 32.5, 37.5)):
        b += f'<path d="M{x},14 q-2.5,-3 0,-5.5 q2.5,-2.5 0,-5.5" fill="none" stroke="#ffffff" stroke-width="1.6" stroke-linecap="round" opacity="{.85 - i * .15:.2f}"/>'
    return b
add('coffee', coffee(), 64, 64, (32, 56))

# ------------------------------------------------------------------ people
SKIN, HAND, SKO = '#ffd8b8', '#ffd3b0', '#c98a63'
def hat_svg(hat, view):
    b = ''
    if hat == 'straw':
        b += ell(32, 15.5, 14, 4.6, '#f7d77e', 'stroke="#c99f45" stroke-width=".9"')
        b += '<path d="M24.5,15 q0,-9 7.5,-9 q7.5,0 7.5,9 Z" fill="#fbe39a" stroke="#c99f45" stroke-width=".9"/>'
        b += '<path d="M24.7,13.4 q7.3,2.6 14.6,0 v2 q-7.3,2.6 -14.6,0 Z" fill="#ef5b4c"/>'
    elif hat == 'strawf':
        b += ell(32, 15.5, 15, 4.8, '#f7d77e', 'stroke="#c99f45" stroke-width=".9"')
        b += '<path d="M24.5,15 q0,-9 7.5,-9 q7.5,0 7.5,9 Z" fill="#fbe39a" stroke="#c99f45" stroke-width=".9"/>'
        b += '<path d="M24.7,13.4 q7.3,2.6 14.6,0 v2 q-7.3,2.6 -14.6,0 Z" fill="#5fb2e8"/>'
        b += (circ(37.6, 13.2, 2.1, '#ff8fc0', '#d0558f', .6) + circ(37.6, 13.2, .8, '#ffe27a') if view == 'front' else circ(26.4, 13.2, 2.1, '#ff8fc0', '#d0558f', .6))
    elif hat.startswith('cap'):
        c, cd = {'cap': ('#2f6fd6', '#1f4f9e'), 'capw': ('#f4f4f0', '#b8b8b0'), 'capd': ('#3a4248', '#22282c'), 'capt': ('#c2603a', '#8a3f22')}[hat]
        b += f'<path d="M23.6,18 q0,-10 8.4,-10 q8.4,0 8.4,10 Z" fill="{c}" stroke="{cd}" stroke-width=".9"/>'
        b += (ell(37.5, 17.6, 7, 2.2, cd) if view == 'front' else ell(26.5, 17.6, 6, 2, cd))
        b += circ(32, 8.6, 1.2, '#ffd36a')
    elif hat == 'bucket':
        b += '<path d="M21.5,17.5 q10.5,5 21,0 l-2,-3 q-8.5,3.5 -17,0 Z" fill="#c9b27a" stroke="#9a8450" stroke-width=".8"/>'
        b += '<path d="M24,15.5 q0,-9 8,-9 q8,0 8,9 q-8,3 -16,0 Z" fill="#dcc68e" stroke="#9a8450" stroke-width=".9"/>'
        b += '<path d="M24.2,13.6 q7.8,2.8 15.6,0" fill="none" stroke="#2a78d0" stroke-width="1.4"/>'
    elif hat == 'hard':
        b += ell(32, 16.8, 11.5, 3.2, '#f2b81f', 'stroke="#b88a10" stroke-width=".8"')
        b += '<path d="M23.6,17 q0,-10.5 8.4,-10.5 q8.4,0 8.4,10.5 Z" fill="#ffd23a" stroke="#b88a10" stroke-width=".9"/>'
        b += '<path d="M32,6.8 v9.5" stroke="#f2b81f" stroke-width="2.2"/>'
    elif hat == 'sun':
        b += ell(32, 15.8, 16.5, 5.2, '#f3e6c4', 'stroke="#b89d5a" stroke-width=".9"')
        b += '<path d="M24.5,15.3 q0,-9 7.5,-9 q7.5,0 7.5,9 Z" fill="#faf0d4" stroke="#b89d5a" stroke-width=".9"/>'
        b += '<path d="M24.7,13.6 q7.3,2.6 14.6,0 v2.2 q-7.3,2.6 -14.6,0 Z" fill="#7a2fb8"/>'
        b += circ(38.2 if view == 'front' else 25.8, 13.8, 2.4, '#c99a12', '#8a6a12', .6) + circ(38.2 if view == 'front' else 25.8, 13.8, 1, '#7a2fb8')
    return b

def person(view='front', frame=0, st=None, work=None):
    st = st or {}
    shirt, shirtD = st.get('shirt', '#5ccf74'), st.get('shirtD', '#3a9e55')
    hat, hair, hairD = st.get('hat', 'straw'), st.get('hair', '#8a5631'), st.get('hairD', '#6a3e22')
    long_ = st.get('long', False); extra = st.get('extra', ())
    coverall = 'coverall' in extra
    b = ell(32, 55, 10, 3.4, '#1d3a24', 'opacity=".18"'); lo = 2 if frame else 0
    jean, jeanD, boot = ('#7f8c96', '#56606b', '#3a3030') if coverall else ('#4f78d6', '#3a5aa8', '#7a4a2b')
    if 'tank' in extra and view == 'back':
        pass
    # legs and boots
    b += f'<rect x="26.5" y="{40-lo}" width="5" height="12" rx="2" fill="{jeanD}"/>'
    b += f'<rect x="32.5" y="40" width="5" height="{12-lo}" rx="2" fill="{jean}"/>'
    b += f'<rect x="25.5" y="{50-lo}" width="6.5" height="4" rx="2" fill="{boot}"/><rect x="32" y="50" width="6.5" height="4" rx="2" fill="{boot}"/>'
    # braid behind the body when seen from the front
    # body
    b += f'<rect x="23.5" y="27" width="17" height="16" rx="6" fill="{shirt}" stroke="{shirtD}" stroke-width=".8"/>'
    if coverall:
        b += f'<rect x="25" y="34" width="14" height="8" rx="3" fill="{shirt}"/><path d="M32,28 v14" stroke="{shirtD}" stroke-width=".8"/>'
        if view == 'front': b += '<rect x="34" y="30" width="4" height="3" rx=".8" fill="#4a555e"/><rect x="24.5" y="37" width="15" height="2.6" fill="#3a4248"/>' + circ(32, 38.3, 1.2, '#c9ced6')
    elif 'apron' not in extra and 'casual' not in extra:
        if view == 'front':
            b += f'<path d="M26,33 h12 v8 a3,3 0 0 1 -3,3 h-6 a3,3 0 0 1 -3,-3 Z" fill="{jean}" stroke="{jeanD}" stroke-width=".7"/>'
            b += f'<path d="M27,33 L26.5,28 M37,33 L37.5,28" stroke="{jean}" stroke-width="1.8" stroke-linecap="round"/>'
            b += circ(28.2, 33.6, .8, '#ffd36a') + circ(35.8, 33.6, .8, '#ffd36a') + f'<rect x="30" y="36" width="4" height="3" rx="1" fill="{jeanD}"/>'
        else:
            b += f'<path d="M26,35 h12 v6 a3,3 0 0 1 -3,3 h-6 a3,3 0 0 1 -3,-3 Z" fill="{jean}" stroke="{jeanD}" stroke-width=".7"/><path d="M27,35 L30,28 M37,35 L34,28" stroke="{jean}" stroke-width="1.8" stroke-linecap="round"/>'
    if 'apron' in extra:
        if view == 'front':
            b += '<path d="M25.5,30 h13 v13 a2.5,2.5 0 0 1 -2.5,2.5 h-8 a2.5,2.5 0 0 1 -2.5,-2.5 Z" fill="#efe2bd" stroke="#b8a170" stroke-width=".7"/>'
            b += '<rect x="28" y="36" width="8" height="4" rx="1" fill="#e0cf9e" stroke="#b8a170" stroke-width=".5"/><path d="M29,36 v-3 M31,36 v-4" stroke="#8a5a3a" stroke-width="1"/>'
        else:
            b += '<path d="M24,36 h16" stroke="#efe2bd" stroke-width="1.6"/><path d="M30,36 l-1.5,4 M34,36 l1.5,4" stroke="#efe2bd" stroke-width="1.2"/>'
    if 'vest' in extra:
        if view == 'front':
            b += '<path d="M23.8,29 q0,-2 3,-2 h2.2 l3,5 l3,-5 h2.2 q3,0 3,2 v11 q0,3 -3,3 h-10.4 q-3,0 -3,-3 Z" fill="#ffe14a" stroke="#d9b20f" stroke-width=".7"/>'
            b += '<path d="M24,35 h16 M24,38.5 h16" stroke="#e9eef2" stroke-width="1.3"/>'
        else:
            b += '<rect x="23.8" y="27.4" width="16.4" height="15" rx="5" fill="#ffe14a" stroke="#d9b20f" stroke-width=".7"/><path d="M24,33 h16 M24,36.5 h16" stroke="#e9eef2" stroke-width="1.3"/><path d="M26,30 l12,9 M38,30 l-12,9" stroke="#e9eef2" stroke-width="1"/>'
    if 'gvest' in extra:
        if view == 'front':
            b += '<path d="M23.8,29 q0,-2 3,-2 h2 l3,7 l3,-7 h2 q3,0 3,2 v11 q0,3 -3,3 h-10 q-3,0 -3,-3 Z" fill="#c99a12" stroke="#8a6a12" stroke-width=".7"/>'
            b += circ(28, 32, 2, '#7a2fb8', '#4a1a70', .5) + f'<path d="M27,33.5 l-.8,3 l1.8,-1 l1.8,1 l-.8,-3" fill="#7a2fb8"/>' + circ(28, 32, .8, '#ffe27a')
        else:
            b += '<rect x="23.8" y="27.4" width="16.4" height="15" rx="5" fill="#c99a12" stroke="#8a6a12" stroke-width=".7"/>'
    if 'tank' in extra:
        if view == 'front':
            b += '<path d="M26,27.5 v7 M38,27.5 v7" stroke="#2b3a33" stroke-width="1.8"/>' + poly([(21.5, 25), (24, 24), (24, 31), (21.5, 31.5)], '#ffd23a', '#b88a10', .6)
        else:
            b += '<rect x="24" y="24.5" width="16" height="19" rx="6" fill="#ffd23a" stroke="#b88a10" stroke-width=".9"/><rect x="29" y="22.5" width="6" height="3" rx="1.2" fill="#d23a3a"/><path d="M26,30 h12" stroke="#e8a50f" stroke-width="1"/>'
            b += '<path d="M39,40 q5,1 6,-4" fill="none" stroke="#2b3a33" stroke-width="1.3"/>'
    # arms
    sw = (2 if frame else -2) if not work else 0
    hand = lambda x, y: circ(x, y, 2.2, HAND, SKO, .6)
    if work == 'can':
        b += f'<rect x="19.5" y="29" width="5" height="10" rx="2.5" fill="{shirt}" stroke="{shirtD}" stroke-width=".7" transform="rotate(-35 22 30)"/>'
        b += f'<rect x="39.5" y="29" width="5" height="10" rx="2.5" fill="{shirt}" stroke="{shirtD}" stroke-width=".7" transform="rotate(35 42 30)"/>'
        b += f'<path d="M40,38 h9 v7 a2,2 0 0 1 -2,2 h-5 a2,2 0 0 1 -2,-2 Z" fill="#4fa8ff" stroke="#1f6fd0" stroke-width=".8"/>'
        b += f'<path d="M49,40 l6,-4" stroke="#1f6fd0" stroke-width="1.6" stroke-linecap="round"/><path d="M41,38 q3,-5 7,0" fill="none" stroke="#1f6fd0" stroke-width="1.2"/>'
        b += ''.join(circ(56 + i * .6, 38 + i * 3, .9, '#8fd0ff') for i in range(3))
        b += circ(43, 37, 2, HAND, SKO, .6)
    elif work:
        # both arms reach forward to the job in hand
        b += f'<rect x="21" y="29" width="5" height="10" rx="2.5" fill="{shirt}" stroke="{shirtD}" stroke-width=".7" transform="rotate(-20 23 30)"/>'
        b += f'<rect x="38" y="29" width="5" height="10" rx="2.5" fill="{shirt}" stroke="{shirtD}" stroke-width=".7" transform="rotate(20 41 30)"/>'
        if work == 'pot':
            b += poly([(27, 37), (37, 37), (35.6, 44.5), (28.4, 44.5)], '#ee8656', '#c9643a', .8) + ell(32, 37, 5, 1.4, '#6a4129')
            b += cluster(32, 33.5, 3.4, 'url(#gLeaf)', '#2f7a3f', 3) + circ(30.6, 32.6, 1.1, '#f26bb5') + circ(33.6, 33.2, 1, '#f26bb5')
            b += hand(26.5, 40) + hand(37.5, 40)
            b += '<path d="M44,42 l5,-6" stroke="#8a5a3a" stroke-width="1.6" stroke-linecap="round"/><path d="M48.4,36.6 l2.2,-2.6 l1,1.6 Z" fill="#b9c9d8" stroke="#56606b" stroke-width=".5"/>'
        elif work == 'spray':
            b += hand(26, 40) + hand(38, 39)
            b += '<path d="M38,39 l12,-5" stroke="#2b3a33" stroke-width="1.6" stroke-linecap="round"/><path d="M26,40 q-4,3 -2,8" fill="none" stroke="#2b3a33" stroke-width="1.2"/>'
            for i, (dx, dy, r) in enumerate(((52, 32, 2.4), (55, 30, 2), (56, 34, 1.8), (58.5, 31, 1.5), (54, 36, 1.4))):
                b += circ(dx, dy, r, '#eafbe8', 'none', 1, 'opacity=".85"')
        elif work == 'wrench':
            b += hand(26, 40) + hand(40, 35)
            b += '<path d="M40,35 l8,-8" stroke="#9aa5ad" stroke-width="2.4" stroke-linecap="round"/><path d="M46.5,25 a3,3 0 1 1 3.8,3.8 l-1.4,-1.4 l1,-1 l-1.4,-1.4 l-1,1 Z" fill="#9aa5ad" stroke="#56606b" stroke-width=".5"/>'
            b += poly([(51, 22), (52.5, 24.5), (55, 23), (53, 26), (55.5, 27.5), (52, 27)], '#ffd23a')
        elif work == 'box':
            b += I_box_svg()
            b += hand(24.5, 37) + hand(39.5, 37)
        elif work in ('shovel0', 'shovel1'):
            up = work == 'shovel0'
            if up:
                b += hand(27, 34) + hand(37, 39)
                b += '<path d="M24,28 L44,46" stroke="#8a5a3a" stroke-width="2" stroke-linecap="round"/><path d="M42,44 l5,-1 l3,5 l-4,3 l-5,-2 Z" fill="#b9c9d8" stroke="#56606b" stroke-width=".7"/>'
            else:
                b += hand(29, 37) + hand(36, 42)
                b += '<path d="M26,31 L42,52" stroke="#8a5a3a" stroke-width="2" stroke-linecap="round"/><path d="M40,50 l5,-1 l3,5 l-4,3 l-5,-2 Z" fill="#b9c9d8" stroke="#56606b" stroke-width=".7"/>'
                b += circ(49, 55, 1.6, '#8a6a4a') + circ(52, 53, 1.2, '#a8805a') + circ(46, 57, 1.1, '#8a6a4a')
        elif work in ('hammer0', 'hammer1'):
            up = work == 'hammer0'
            b += hand(26, 40)
            if up:
                b += hand(40, 30) + '<path d="M40,30 l3,-9" stroke="#8a5a3a" stroke-width="2" stroke-linecap="round"/><rect x="39" y="17.5" width="9" height="4" rx="1" fill="#6f7b84" stroke="#3a4248" stroke-width=".6" transform="rotate(20 43.5 19.5)"/>'
            else:
                b += hand(41, 38) + '<path d="M41,38 l8,2" stroke="#8a5a3a" stroke-width="2" stroke-linecap="round"/><rect x="47" y="36" width="4" height="9" rx="1" fill="#6f7b84" stroke="#3a4248" stroke-width=".6"/>'
                b += '<path d="M53,38 l3,-2 M53,42 l3.5,0 M52.5,45 l2.5,2" stroke="#ffd23a" stroke-width="1.2" stroke-linecap="round"/>'
        elif work == 'snips':
            b += hand(27, 39) + hand(38, 37)
            b += '<path d="M38,37 l7,-5 M38,37 l7,-2" stroke="#b9c9d8" stroke-width="1.4" stroke-linecap="round"/><path d="M36,38 l2,-1" stroke="#d23a3a" stroke-width="2.2" stroke-linecap="round"/>'
            for x, y, r in ((48, 28, 2.2), (51, 33, 1.4), (45, 25, 1.2)):
                b += f'<path d="M{x},{y-r} L{x+r*.3},{y-r*.3} L{x+r},{y} L{x+r*.3},{y+r*.3} L{x},{y+r} L{x-r*.3},{y+r*.3} L{x-r},{y} L{x-r*.3},{y-r*.3} Z" fill="#ffe27a"/>'
    else:
        b += f'<rect x="19.5" y="{28+sw*.5}" width="5" height="12" rx="2.5" fill="{shirt}" stroke="{shirtD}" stroke-width=".7"/>'
        b += f'<rect x="39.5" y="{28-sw*.5}" width="5" height="12" rx="2.5" fill="{shirt}" stroke="{shirtD}" stroke-width=".7"/>'
        b += hand(22, 40.5 + sw * .5) + hand(42, 40.5 - sw * .5)
        if 'wrench' in extra and view == 'front':
            b += f'<path d="M42,{41-sw*.5} v6" stroke="#9aa5ad" stroke-width="1.8" stroke-linecap="round"/>'
    # head
    if long_ and view == 'front':
        b += f'<path d="M23.6,20 q-1.5,9 1.2,13 h4 q-2,-5 -1.4,-11 Z" fill="{hair}" stroke="{hairD}" stroke-width=".6"/>'
        b += f'<path d="M40.4,20 q1.5,9 -1.2,13 h-4 q2,-5 1.4,-11 Z" fill="{hair}" stroke="{hairD}" stroke-width=".6"/>'
    b += circ(32, 21, 8.6, SKIN, SKO, .8)
    if view == 'front':
        b += ell(28.4, 21.6, 1, 1.4, '#3a2b3d') + ell(35.6, 21.6, 1, 1.4, '#3a2b3d') + circ(28.1, 21.1, .35, '#ffffff') + circ(35.3, 21.1, .35, '#ffffff')
        if long_:
            b += '<path d="M26.8,20.4 l-.9,-.8 M36.9,20.4 l.9,-.8" stroke="#3a2b3d" stroke-width=".6" stroke-linecap="round"/>'
        b += ell(26.4, 24.4, 1.8, 1.1, '#ff9a9a', 'opacity=".7"') + ell(37.6, 24.4, 1.8, 1.1, '#ff9a9a', 'opacity=".7"')
        if 'mask' in extra:
            b += '<path d="M27.5,23.2 q4.5,-1.6 9,0 v3 q-4.5,3 -9,0 Z" fill="#e9eef2" stroke="#8a96a3" stroke-width=".6"/>' + circ(27.2, 25.6, 1.6, '#56606b') + circ(36.8, 25.6, 1.6, '#56606b')
        else:
            b += '<path d="M29.5,25.4 q2.5,2.4 5,0" fill="none" stroke="#7a3b3b" stroke-width="1" stroke-linecap="round"/>'
        if long_:
            b += f'<path d="M25,15.5 q7,4 14,0 v2.4 q-7,3 -14,0 Z" fill="{hair}"/>'
    else:
        b += circ(32, 21, 8.6, hair, hairD, .8)
        b += f'<path d="M25.5,24 q6.5,5 13,0" fill="none" stroke="{hairD}" stroke-width=".8"/>'
        b += ell(23.6, 22, 1.4, 2, SKIN, f'stroke="{SKO}" stroke-width=".6"') + ell(40.4, 22, 1.4, 2, SKIN, f'stroke="{SKO}" stroke-width=".6"')
        if long_:
            for i, y in enumerate((29, 32.2, 35.4, 38.4)):
                b += ell(32, y, 2.6 - i * .25, 2, hair, f'stroke="{hairD}" stroke-width=".6"')
            b += circ(32, 40.6, 1.3, '#5fb2e8')
        if 'mask' in extra: b += '<path d="M23.8,23.6 q8.2,3 16.4,0" fill="none" stroke="#8a96a3" stroke-width=".8"/>'
    if hat == 'none' and not long_:
        if view == 'front': b += f'<path d="M23.4,18 q-.4,-10.5 8.6,-10.5 q9,0 8.6,10.5 q-1.6,-5 -8.6,-5.2 q-7,.2 -8.6,5.2 Z" fill="{hair}" stroke="{hairD}" stroke-width=".7"/>'
        else: b += ell(32, 16, 8.7, 8.6, hair, f'stroke="{hairD}" stroke-width=".7"')
    b += hat_svg(hat, view)
    if 'goggles' in extra and view == 'front':
        b += '<rect x="26" y="9.5" width="12" height="3.6" rx="1.8" fill="#9fd0ff" stroke="#2b3a33" stroke-width=".8"/>'
    return b

def I_box_svg():
    I = Iso(32, 41)
    return I.box(-.15, -.15, .15, .15, 0, 8, '#e7c48a', '#c99a5a', '#b5864a', '#7a5a30', .7) + poly([I.P(-.15, -.02, 8), I.P(.15, -.02, 8), I.P(.15, .02, 8), I.P(-.15, .02, 8)], '#d0a868')

PEOPLE = {
    'grower':  dict(),
    'growerf': dict(hat='strawf', long=True, hair='#7a4422', hairD='#56301a', shirt='#ff8fb2', shirtD='#d0587f'),
    'crew_pot':   dict(shirt='#e98a5a', shirtD='#b85a30', hat='capt', extra=('apron',)),
    'crew_water': dict(shirt='#5aaef5', shirtD='#2a78d0', hat='bucket'),
    'crew_pest':  dict(shirt='#ff7a6a', shirtD='#c8402f', hat='capw', extra=('tank', 'mask', 'goggles')),
    'crew_fix':   dict(shirt='#9aa7b2', shirtD='#56606b', hat='capd', extra=('coverall', 'wrench')),
    'crew_load':  dict(shirt='#5ccf74', shirtD='#2c8a47', hat='hard', extra=('vest',)),
    'crew_prize': dict(shirt='#fff6e0', shirtD='#c9b88a', hat='sun', extra=('gvest',)),
    'shop_a': dict(hat='none', shirt='#7a6ad8', shirtD='#4f3fa8', hair='#3a2a1a', hairD='#24180e', extra=('casual',)),
    'shop_b': dict(hat='none', long=True, shirt='#f2a531', shirtD='#c2701f', hair='#c98a3a', hairD='#8a5a1f', extra=('casual',)),
    'shop_c': dict(hat='sun', shirt='#3fb0a8', shirtD='#24807a', extra=('casual',)),
    'shop_d': dict(hat='none', long=True, shirt='#e05a7a', shirtD='#a83a56', hair='#2a1a10', hairD='#180e08', extra=('casual',)),
}
WORKT = {'shop_a': 'box', 'shop_b': 'box', 'shop_c': 'box', 'shop_d': 'box', 'grower': 'can', 'growerf': 'can', 'crew_pot': 'pot', 'crew_water': 'can', 'crew_pest': 'spray', 'crew_fix': 'wrench', 'crew_load': 'box', 'crew_prize': 'snips'}
for who, st_ in PEOPLE.items():
    for v in ('front', 'back'):
        for fr in (0, 1): add(f'{who}_{v}_{fr}', person(v, fr, st_))
    add(f'{who}_work', person('front', 0, st_, WORKT[who]))
    if who.startswith('grower'):
        for t in ('shovel0', 'shovel1', 'hammer0', 'hammer1'): add(f'{who}_{t}', person('front', 0, st_, t))
# old crew ids stay valid
for v in ('front', 'back'):
    for fr in (0, 1): add(f'crew_{v}_{fr}', person(v, fr, PEOPLE['crew_pot']))
add('crew_work', person('front', 0, PEOPLE['crew_pot'], 'pot'))

# ------------------------------------------------------------------ heater
def heater(broken=False):
    I = Iso(); b = I.box(.18, .18, .82, .82, 0, 34, 'url(#gCream)', '#f0dcb8', 'url(#gCreamR)', '#b3936a', .9)
    b += I.box(.18, .18, .82, .82, 30, 34, '#ffe9c7', '#ef5b4c', '#d6473a', '#b3936a', .7)  # red band
    # glowing window on the right face
    cx_, cy_ = I.P(.82, .5, 15)
    if broken:
        b += ell(cx_, cy_, 5, 6.5, '#4a4a55', 'stroke="#2c2c33" stroke-width=".8"')
        for i, (dx, y, rr) in enumerate(((0, 9, 3.2), (4, 5, 4), (-1, 2, 4.4))):
            b += circ(32 + dx, y, rr, '#b9b9c2', extra='opacity=".75"')
        b += circ(32, 20, 2, '#ff4d3a', '#ffffff', .8)
    else:
        b += ell(cx_, cy_, 5, 6.5, 'url(#gGlow)', 'stroke="#c9541f" stroke-width=".8"')
        b += '<path d="M%s,%s q-2,-3 0,-6 q2,3 0,6" fill="#fff7c2"/>' % (f2(cx_), f2(cy_ + 3))
        b += circ(32, 20, 2, '#4fe07a', '#ffffff', .8)
    # vents on the left face
    for i in range(3):
        a, c = I.P(.3, .82, 10 + i * 5), I.P(.6, .82, 10 + i * 5)
        b += f'<path d="M{f2(a[0])},{f2(a[1])} L{f2(c[0])},{f2(c[1])}" stroke="#c9ad80" stroke-width="1.4" stroke-linecap="round"/>'
    return b
add('heater', heater()); add('heater_broken', heater(True))

# ------------------------------------------------------------------ icons
GL = {
 'pot': ('M6 11h12l-1.7 8.6a1 1 0 0 1-1 .9H8.7a1 1 0 0 1-1-.9z', 'M12 11V5.5 M12 8C10.5 5.5 8.2 5.4 7 6.8 M12 8c1.5-2.5 3.8-2.6 5-1.2'),
 'water': ('M12 3.5C9.2 7.6 6.5 10.8 6.5 14.2a5.5 5.5 0 0 0 11 0c0-3.4-2.7-6.6-5.5-10.7z', ''),
 'pest': ('M12 7.2c2.3 0 4 1.9 4 4.3V15a4 4 0 0 1-8 0v-3.5c0-2.4 1.7-4.3 4-4.3z', 'M8 11.5H4.5 M16 11.5h3.5 M8 15.5H4.5 M16 15.5h3.5 M10.2 7.6 8.6 4.8 M13.8 7.6l1.6-2.8'),
 'fix': ('M15.7 3.6a4.6 4.6 0 0 0-4.4 6.1L4.8 16.2a1.9 1.9 0 0 0 2.7 2.7l6.5-6.5a4.6 4.6 0 0 0 6.1-4.4l-2.8 2.8-2.6-.4-.4-2.6z', ''),
 'load': ('M2.5 6.5h11v10h-11z M14.5 9.5h3.8l3.2 3.4v3.6h-7z M5 18.2a1.9 1.9 0 1 0 3.8 0a1.9 1.9 0 1 0-3.8 0z M15.4 18.2a1.9 1.9 0 1 0 3.8 0a1.9 1.9 0 1 0-3.8 0z', ''),
}
def icon(k):
    f, s = GL[k]
    b = ell(32, 56, 9, 2.6, '#1d3a24', 'opacity=".2"')
    b += '<path d="M27,40 L32,50 L37,40 Z" fill="#ffffff"/>'
    b += circ(32, 27, 18, '#ffffff') + circ(32, 27, 15, f'url(#gI{k})')
    b += ell(26, 19, 7, 3.6, '#ffffff', 'opacity=".35" transform="rotate(-25 26 19)"')
    b += f'<g transform="translate(19.4 14.4) scale(1.05)" fill="#ffffff" stroke="#ffffff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="{f}" stroke="none"/>' + (f'<path d="{s}" fill="none"/>' if s else '') + '</g>'
    return b
for k in GL: add(f'icon_{k}', icon(k))

# ------------------------------------------------------------------ walls (64x128, anchor 32,96)
def wall(side):
    I = Iso(32, 96); b = ''
    if side == 'back':
        B = lambda a, c, z0, z1, t, l, r, s: I.box(a, -.07, c, .02, z0, z1, t, l, r, s, .8)
        gl = [I.P(0, -.025, 16), I.P(1, -.025, 16), I.P(1, -.025, 80), I.P(0, -.025, 80)]
        hl = lambda a, c, z0, z1: [I.P(a, -.02, z0), I.P(a + .08, -.02, z0), I.P(c + .08, -.02, z1), I.P(c, -.02, z1)]
    else:
        B = lambda a, c, z0, z1, t, l, r, s: I.box(-.07, a, .02, c, z0, z1, t, l, r, s, .8)
        gl = [I.P(-.025, 0, 16), I.P(-.025, 1, 16), I.P(-.025, 1, 80), I.P(-.025, 0, 80)]
        hl = lambda a, c, z0, z1: [I.P(-.02, a, z0), I.P(-.02, a + .08, z0), I.P(-.02, c + .08, z1), I.P(-.02, c, z1)]
    b += B(0, 1, 0, 16, '#f6f1e6', '#e4dccb', '#d3c9b4', '#b9ad95')
    b += poly(gl, 'url(#gGlass)', '#9fd3da', .6)
    b += poly(hl(.25, .45, 20, 76), '#ffffff', extra='opacity=".55"') + poly(hl(.55, .62, 30, 70), '#ffffff', extra='opacity=".4"')
    b += B(0, .07, 16, 82, '#7fcfa0', '#3f9a6c', '#2f7d57', '#246346')
    b += B(0, 1, 46, 49, '#7fcfa0', '#3f9a6c', '#2f7d57', '#246346')
    b += B(0, 1, 80, 85, '#8fdcae', '#3f9a6c', '#2f7d57', '#246346')
    return b
add('wall_back', wall('back'), 64, 128, (32, 96)); add('wall_left', wall('left'), 64, 128, (32, 96))

# ------------------------------------------------------------------ truck (128x128, anchor 64,80)
def truck():
    I = Iso(64, 80); b = ell(64, 104, 46, 9, '#1d3a24', 'opacity=".15"')
    b += I.box(-1.15, -.36, .92, .36, 6, 50, 'url(#gBox)', '#f3eee2', '#ddd5c4', '#a89f8b', 1)
    # leaf logo on the side
    lx, ly = I.P(-.1, .36, 28)
    b += circ(lx, ly, 8, '#4fcf7a', '#1f8f4a', 1) + f'<path d="M{f2(lx-4)},{f2(ly+3)} q1,-9 9,-8 q0,8 -9,8 Z" fill="#ffffff"/>'
    stripe = [I.P(-1.1, .36, 14), I.P(.88, .36, 14), I.P(.88, .36, 18), I.P(-1.1, .36, 18)]
    b += poly(stripe, '#4fcf7a')
    b += I.box(.97, -.3, 1.6, .3, 6, 36, 'url(#gCab)', '#e85a3c', '#c9442b', '#9e3220', 1)
    w = [I.P(1.6, -.22, 20), I.P(1.6, .22, 20), I.P(1.6, .22, 32), I.P(1.6, -.22, 32)]
    b += poly(w, '#cdefff', '#5b8fb0', .8) + poly([I.P(1.6, -.15, 22), I.P(1.6, -.02, 22), I.P(1.6, .08, 31), I.P(1.6, -.05, 31)], '#ffffff', extra='opacity=".6"')
    side_w = [I.P(1.05, .3, 22), I.P(1.45, .3, 22), I.P(1.45, .3, 32), I.P(1.05, .3, 32)]
    b += poly(side_w, '#cdefff', '#5b8fb0', .8)
    hx, hy = I.P(1.6, .2, 12); b += circ(hx, hy, 2.2, '#fff3a6', '#d9a72a', .7)
    for wu in (-.75, .55, 1.3):
        x, y = I.P(wu, .36, 5)
        b += ell(x, y, 7, 7.5, '#2f3138') + ell(x, y, 3.2, 3.4, '#c9ced6') + circ(x, y, 1, '#6b7280')
    return b
add('truck', truck(), 128, 128, (64, 80))

# ------------------------------------------------------------------ upgrade props
def soil_pallet(l):
    I = Iso(); b = I.box(.12, .14, .88, .86, 0, 4, '#e0ad66', '#c08945', '#a87436', '#7a4f24', .7)
    bag = lambda u0, v0, u1, v1, z: (I.box(u0, v0, u1, v1, z, z + 7, '#8cc152', '#6aa03c', '#568532', '#335a1e', .7) +
                                     poly([I.P(u0 + .08, (v0 + v1) / 2, z + 7), I.P(u1 - .08, (v0 + v1) / 2, z + 7), I.P(u1 - .08, (v0 + v1) / 2 + .06, z + 7), I.P(u0 + .08, (v0 + v1) / 2 + .06, z + 7)], '#f4e7b4'))
    b += bag(.18, .2, .82, .48, 4) + bag(.18, .52, .82, .8, 4)
    if l >= 2: b += bag(.18, .2, .82, .48, 11) + bag(.18, .52, .82, .8, 11)
    if l >= 3:
        b += I.box(.22, .24, .78, .76, 18, 32, '#ffffff', '#e8e3d6', '#d6d0c0', '#a39b86', .8)
        for u in (.22, .78):
            x, y = I.P(u, .24, 32); b += f'<path d="M{f2(x)},{f2(y)} q2,-6 5,-1" fill="none" stroke="#6aa03c" stroke-width="1.6"/>'
        b += poly([I.P(.32, .76, 22), I.P(.68, .76, 22), I.P(.68, .76, 28), I.P(.32, .76, 28)], '#6aa03c')
    return b
def hose_reel(l):
    I = Iso(); b = I.box(.3, .35, .75, .7, 0, 3, '#c9d8e4', 'url(#gMetal)', '#7f95a8', '#5d7185', .7)
    cx_, cy_ = I.P(.52, .52, 15)
    b += ell(cx_ - 7, cy_ + 4, 2.2, 6, '#33413a') + ell(cx_ + 7, cy_ + 4, 2.2, 6, '#33413a')
    b += circ(cx_, cy_, 9, '#2f7a3f', '#1f5a2e', 1)
    for r in (7.2, 5.4, 3.6): b += circ(cx_, cy_, r, 'none', '#6fd16a', 1.1)
    b += circ(cx_, cy_, 1.6, '#c9d8e4')
    b += f'<path d="M{f2(cx_)},{f2(cy_-9)} L{f2(cx_+2)},{f2(cy_-17)} L{f2(cx_+8)},{f2(cy_-15)}" fill="none" stroke="#56606b" stroke-width="1.8" stroke-linecap="round"/>'
    b += f'<path d="M{f2(cx_+8)},{f2(cy_+2)} q6,6 10,2 q4,-4 8,1" fill="none" stroke="#2f7a3f" stroke-width="2" stroke-linecap="round"/>'
    if l >= 2: b += I.box(.62, .12, .86, .32, 0, 12, '#9fd0ff', '#5a9ee0', '#4282c2', '#2a5a8a', .7)
    if l >= 3:
        b += I.box(.08, .14, .3, .34, 8, 20, '#ffe27a', '#f2c230', '#d9a51f', '#8a6a14', .7)
        x, y = I.P(.3, .24, 15); b += poly([(x - 3.5, y - 2), (x + .5, y - 4), (x + .5, y + .5), (x - 3.5, y + 2.5)], '#2b3a33')
    return b
def potter(l):
    I = Iso(); c = ('#ffb56b', '#f08a3c', '#d0702a', '#8a4a1a') if l == 1 else ('#8fe3d6', '#3fb8a6', '#2c9a8a', '#1f5f56')
    b = I.box(.08, .4, .92, .7, 0, 12, '#5d6b62', '#46524b', '#39433d', '#262d29', .7)   # belt
    for t in (.2, .4, .6, .8):
        x, y = I.P(t, .55, 12); b += f'<path d="M{f2(x-3)},{f2(y-1.5)} l6,3" stroke="#7f8c84" stroke-width=".8"/>'
    b += I.box(.12, .12, .55, .9, 0, 26, c[0], c[1], c[2], c[3], .9)
    b += poly([I.P(.18, .25, 26), I.P(.5, .25, 26), I.P(.46, .75, 26), I.P(.22, .75, 26)], '#6a4129')
    b += I.box(.2, .2, .48, .3, 26, 34, c[0], c[1], c[2], c[3], .7)
    x, y = I.P(.55, .6, 18); b += circ(x - 4, y, 2.2, '#ffffff', '#33413a', .8) + circ(x + 1, y + 2, 1.4, '#ff5a4a')
    pots = [(.68, .55), (.84, .55)] if l == 1 else [(.62, .55), (.75, .55), (.88, .55)]
    for u, v in pots:
        x, y = I.P(u, v, 12)
        b += poly([(x - 3, y - 4), (x + 3, y - 4), (x + 2.2, y + 1), (x - 2.2, y + 1)], '#3a3f3c', '#1f2321', .6)
        if l == 2: b += cluster(x, y - 6, 3.2, 'url(#gLeaf)', '#2f7a3f', int(u * 10))
    return b
def forklift(l):
    I = Iso(); c = ('#ffd75e', '#f2c230', '#d0a21a', '#7a5a10') if l == 1 else ('#9fd0ff', '#3a8fd6', '#2a72b8', '#1d4f80')
    b = ''
    for u, v in ((.4, .78), (.78, .78)):
        x, y = I.P(u, v, 3); b += ell(x, y, 4.5, 3.2, '#22282a')
    b += I.box(.12, .32, .2, .68, 0, 36, '#7f8c96', '#56606b', '#46505a', '#2c333a', .7)
    for v in (.36, .58):
        b += I.box(-.18, v, .14, v + .06, 1, 3, '#9aa5ad', '#6f7b84', '#5d6870', '#3a4248', .5)
    b += I.box(.24, .26, .88, .74, 3, 15, c[0], c[1], c[2], c[3], .9)
    b += I.box(.62, .32, .84, .68, 15, 22, '#3a4248', '#2c333a', '#232a30', '#1a1f23', .6)
    for u, v in ((.3, .3), (.82, .3), (.3, .7), (.82, .7)):
        b += I.box(u - .02, v - .02, u + .02, v + .02, 15, 36, '#33413a', '#33413a', '#262f2a', '#1a1f1c', .4)
    b += I.box(.27, .27, .85, .73, 36, 38, c[0], c[1], c[2], c[3], .6)
    if l == 2:
        x, y = I.P(.88, .5, 9); b += poly([(x - 1, y - 4), (x + 2, y - 1), (x, y - 1), (x + 1, y + 3), (x - 2, y), (x, y)], '#fff27a')
    return b
for _l in (1, 2, 3): add(f'soil_{_l}', soil_pallet(_l)); add(f'hose_{_l}', hose_reel(_l))
for _l in (1, 2): add(f'potter_{_l}', potter(_l)); add(f'forklift_{_l}', forklift(_l))

# ------------------------------------------------------------------ cats (facing right; flip for left)
VCOAT = {'anna':  dict(b='#fbf8f2', d='#c96f2c', w='#ffffff', o='#7a6656', eye='#3f8a3a', h='#f0a050', t='#4a4f57', ts='#9aa0a8',
                      patches=('#ee9a48', '#8e959e', '#5a3a28')),
         'miley': dict(b='#7d8592', d='#555c68', w='#ffffff', o='#3f4550', eye='#c7a12a'),
         'max':   dict(b='#f2a04e', d='#c96a26', w='#e8913f', o='#7a4622', eye='#6a9a2a', st='#c7652a', ts='#c7652a'),
         'gremlin': dict(b='#3a2b24', d='#2a1e19', w='#4a3a32', o='#1e1612', eye='#d9a52a', h='#3a2b24', t='#3a2b24', patches=('#c8732e', '#7a4a2a', '#d99a4e'), mz='#a39488', fh=False),
         'beatrice': dict(b='#fbfbf8', d='#d9d6cf', w='#ffffff', o='#6a6660', eye='#3a7bd5', h='#fbfbf8', t='#fbfbf8', patches=('#232326', '#2e2e33', '#232326'), mz=None, fh=False, fluffy=True),
         'minaou': dict(b='#2b221e', d='#1f1815', w='#3a2e28', o='#14100e', eye='#e0b23a', h='#2b221e', t='#2b221e', patches=('#c86a2a', '#5a3a28', '#d8893e'), mz=None, fh=False, small=True)}
def vcat(name, pose):
    c = VCOAT[name]; o = c['o']; sw = .9
    b = ell(32, 53, 11, 2.8, '#1d3a24', 'opacity=".18"')
    stripes = (lambda pts: ''.join(f'<path d="{d}" stroke="{c["st"]}" stroke-width="1.7" fill="none" stroke-linecap="round"/>' for d in pts)) if 'st' in c else (lambda pts: '')
    hc, tc = c.get('h', c['b']), c.get('t', c['b'])
    def tail(d, w1=4.6, w2=3):
        if c.get('fluffy'): w1, w2 = w1 * 1.7, w2 * 1.75
        t = f'<path d="{d}" fill="none" stroke="{o}" stroke-width="{w1}" stroke-linecap="round"/><path d="{d}" fill="none" stroke="{tc}" stroke-width="{w2}" stroke-linecap="round"/>'
        if 'ts' in c: t += f'<path d="{d}" fill="none" stroke="{c["ts"]}" stroke-width="{w2}" stroke-dasharray="1.3 2.1"/>'
        return t
    def patches(clip, spots):
        if 'patches' not in c: return ''
        cid = f'cp{name}{pose}'
        return f'<clipPath id="{cid}">{clip}</clipPath><g clip-path="url(#{cid})">' + ''.join(ell(x, y, rx, ry, c['patches'][k]) for k, x, y, rx, ry in spots) + '</g>'
    def head(x, y, closed=False):
        h = poly([(x - 5.5, y - 2), (x - 4.5, y - 8.5), (x - 1, y - 4.5)], hc, o, sw) + poly([(x + 5.5, y - 2), (x + 4.5, y - 8.5), (x + 1, y - 4.5)], c['patches'][2] if 'patches' in c else hc, o, sw)
        h += poly([(x - 4.4, y - 3), (x - 4, y - 7), (x - 2, y - 4.6)], '#ffb3c0') + poly([(x + 4.4, y - 3), (x + 4, y - 7), (x + 2, y - 4.6)], '#ffb3c0')
        h += ell(x, y, 6.4, 5.6, hc, f'stroke="{o}" stroke-width="{sw}"')
        if name == 'miley': h += ell(x + .5, y + 2.4, 3.6, 2.6, c['w'])
        if 'st' in c: h += ''.join(f'<path d="{p}" stroke="{c["st"]}" stroke-width="1.2" fill="none" stroke-linecap="round"/>' for p in (f'M{x-1.6},{y-5} v2', f'M{x+.6},{y-5.4} v2.3', f'M{x+2.8},{y-5} v2', f'M{x-5.6},{y+.6} h-1.6', f'M{x+6.4},{y+.6} h1.6'))
        if 'patches' in c:
            if c.get('mz', '#ffffff'): h += ell(x + .6, y + 2.8, 3.2, 2.2, c.get('mz', '#ffffff'))
            if c.get('fh', True): h += ''.join(f'<path d="{p}" stroke="#c9742e" stroke-width="1.1" fill="none" stroke-linecap="round"/>' for p in (f'M{x-1.5},{y-5} v1.8', f'M{x+.5},{y-5.3} v2', f'M{x+2.5},{y-5} v1.8'))
            if name in ('gremlin', 'minaou'): h += ell(x - 2.6, y - 2.2, 2.4, 1.8, c['patches'][0]) + ell(x + 3, y + .6, 1.8, 1.4, c['patches'][1])
            if name == 'beatrice': h += ell(x + 2.8, y - 3, 2.2, 1.7, c['patches'][0])
            if name == 'beatrice': h += poly([(x - 4.6, y - 6.6), (x - 7.4, y - 8.2), (x - 7.2, y - 4.6)], '#ff7eb6', '#c2407e', .5) + poly([(x - 4.6, y - 6.6), (x - 2, y - 8.6), (x - 1.8, y - 5)], '#ff7eb6', '#c2407e', .5) + circ(x - 4.6, y - 6.6, 1, '#ff4f9a')
        if closed:
            h += f'<path d="M{x-3.6},{y-.2} q1.3,1.2 2.6,0 M{x+1.6},{y-.2} q1.3,1.2 2.6,0" stroke="{o}" stroke-width=".9" fill="none" stroke-linecap="round"/>'
        else:
            h += ell(x - 2.2, y - .4, 1.2, 1.5, c['eye']) + ell(x + 2.9, y - .4, 1.2, 1.5, c['eye']) + circ(x - 1.9, y - .9, .4, '#fff') + circ(x + 3.2, y - .9, .4, '#fff')
        h += poly([(x + .1, y + 1.4), (x + 1.5, y + 1.4), (x + .8, y + 2.3)], '#ff8a9a')
        h += f'<path d="M{x+.8},{y+2.3} q-1,1.2 -2,.4 M{x+.8},{y+2.3} q1,1.2 2,.4" stroke="{o}" stroke-width=".6" fill="none"/>'
        return h
    if pose in ('walk0', 'walk1'):
        f = 1 if pose == 'walk1' else -1
        b += tail('M21,43 q-8,-2 -6,-12 q1,-3 3,-1')
        for lx, ph in ((24, f), (28, -f), (36, -f), (40, f)):
            b += f'<rect x="{lx-1.6+ph*.9}" y="44" width="3.4" height="8.5" rx="1.6" fill="{c["w"]}" stroke="{o}" stroke-width="{sw}"/>'
        b += ell(32, 43, 12, 6.5, c['b'], f'stroke="{o}" stroke-width="{sw}"')
        b += patches(ell(32, 43, 11.5, 6, '#000'), [(0, 27.5, 38.2, 7.2, 4.6), (1, 36.8, 38, 5.2, 4.2), (2, 21, 40.8, 4.2, 4.2), (0, 41, 41, 3, 2.6), (2, 32.5, 37.4, 2.2, 1.8)])
        if name == 'miley': b += ell(33, 46.5, 8, 2.6, c['w'])
        b += stripes(['M27,37.5 q1,3 0,6', 'M31,37 q1,3 0,6.5', 'M35,37 q1,3 0,6.5'])
        b += head(43, 35)
    elif pose == 'sit':
        if c.get('fluffy'): b += ell(33.5, 37, 7.5, 4.5, c['w'], f'stroke="{o}" stroke-width=".7"')
        b += tail('M26,51 q-9,1 -8,-5 q.5,-2 2.5,-1.5')
        b += f'<path d="M24,52 q-1,-16 9,-17 q9,1 8,17 Z" fill="{c["b"]}" stroke="{o}" stroke-width="{sw}"/>'
        b += patches('<path d="M24.4,51.6 q-1,-16 8.6,-16.6 q8.6,1 7.6,16.6 Z"/>', [(0, 26, 40.5, 3.8, 5), (2, 40, 39.5, 2.8, 4), (1, 37.5, 37, 3, 2.2)])
        if name != 'max': b += ell(33.5, 45, 4.4, 6, c['w'])
        b += stripes(['M26,42 q2,1 3,0', 'M26,46 q2,1 3,0'])
        b += ell(30.5, 51.5, 2.4, 1.6, c['w'], f'stroke="{o}" stroke-width=".7"') + ell(36.5, 51.5, 2.4, 1.6, c['w'], f'stroke="{o}" stroke-width=".7"')
        b += head(33.5, 30)
    elif pose == 'eat':
        b += tail('M21,45 q-8,-1 -7,-9 q1,-3 3,-1')
        for lx in (24, 28, 36, 40):
            b += f'<rect x="{lx-1.6}" y="47" width="3.4" height="5.5" rx="1.6" fill="{c["w"]}" stroke="{o}" stroke-width="{sw}"/>'
        b += ell(31, 45, 11.5, 6, c['b'], f'stroke="{o}" stroke-width="{sw}"')
        b += patches(ell(31, 45, 11, 5.5, '#000'), [(0, 26.5, 40.5, 7, 4.4), (1, 35.5, 40.2, 5, 4), (2, 20, 43, 4, 4)])
        if name == 'miley': b += ell(32, 48.5, 7.5, 2.4, c['w'])
        b += stripes(['M25,39.8 q1,3 0,6', 'M29,39.2 q1,3 0,6.5', 'M33,39.2 q1,3 0,6.5'])
        b += head(45, 46, True)
    else:  # sleep: curled loaf
        b += ell(31, 47, 12.5, 6.5, c['b'], f'stroke="{o}" stroke-width="{sw}"')
        b += patches(ell(31, 47, 12, 6, '#000'), [(0, 27, 42, 7, 4.2), (1, 36, 41.6, 5, 3.6), (2, 21, 45, 3.8, 3.4), (2, 31.5, 41, 2.2, 1.8)])
        b += stripes(['M24,42.5 q1,3 0,5.5', 'M28.5,41.2 q1,3 0,6', 'M33,41.2 q1,3 0,6'])
        b += tail('M19,49 q8,6 22,2', 4.4, 2.8)
        b += head(39, 45, True)
        b += f'<text x="44" y="33" font-family="Arial" font-weight="bold" font-size="6" fill="#7fa6d6">z</text><text x="48" y="28" font-family="Arial" font-weight="bold" font-size="4.5" fill="#7fa6d6">z</text>'
    if c.get('small'): b = f'<g transform="translate(32 52) scale(.84) translate(-32 -52)">{b}</g>'
    return b
def vmouse(frame):
    b = ell(32, 50, 7, 1.8, '#1d3a24', 'opacity=".18"')
    b += f'<path d="M25,47 q-6,1 -8,-3 q-1,-3 2,-3" fill="none" stroke="#c98b8b" stroke-width="1.1" stroke-linecap="round"/>'
    for fx in ((28, 35) if frame == 0 else (29.5, 33.5)):
        b += ell(fx, 49.2, 1.3, .8, '#c98b8b')
    b += ell(31, 46, 6.5, 3.6, '#9aa1aa', 'stroke="#5d646d" stroke-width=".7"')
    b += ell(30, 47.2, 4.5, 1.6, '#c5cad1')
    b += f'<path d="M36,43.6 q4.5,.8 5.2,3 q-2,1.4 -5.4,.8 Z" fill="#9aa1aa" stroke="#5d646d" stroke-width=".7" stroke-linejoin="round"/>'
    b += circ(35.6, 42.6, 2, '#9aa1aa', '#5d646d', .7) + circ(35.6, 42.6, 1.1, '#f2a7b5')
    b += circ(38.6, 45.1, .6, '#1f2321') + circ(41.3, 46.6, .7, '#f27a92')
    b += f'<path d="M41,46.4 l2.6,-1 M41,46.8 l2.8,.4" stroke="#5d646d" stroke-width=".4"/>'
    return b
add('mouse_0', vmouse(0)); add('mouse_1', vmouse(1))
for _n in ('anna', 'miley', 'max', 'gremlin', 'beatrice', 'minaou'):
    for _p in ('walk0', 'walk1', 'sit', 'sleep', 'eat'): add(f'cat_{_n}_{_p}', vcat(_n, _p))
def vbowls():
    I = Iso(); b = ''
    m = [I.P(.12, .3), I.P(.88, .3), I.P(.88, .78), I.P(.12, .78)]
    b += poly(m, '#e9c46a', '#b8913a', .8)
    def bowl(u, v, rim, inner, fill):
        x, y = I.P(u, v); s = ''
        s += ell(x, y + 2, 8.2, 4.1, '#1d3a24', 'opacity=".15"')
        s += f'<path d="M{x-7.6},{y-1.4} L{x-6},{y+2.6} Q{x},{y+5.6} {x+6},{y+2.6} L{x+7.6},{y-1.4} Z" fill="{rim}" stroke="#2f3a44" stroke-width=".7"/>'
        s += ell(x, y - 1.4, 7.6, 3.5, rim, 'stroke="#2f3a44" stroke-width=".7"')
        s += ell(x, y - 1.3, 6, 2.6, inner)
        return s + fill(x, y)
    kib = lambda x, y: ''.join(circ(x + dx*1.2, y - 1.3 + dy, 1.05, c) for dx, dy, c in ((-2.4, -.3, '#8a5a2b'), (-.8, .5, '#a86b33'), (.9, -.4, '#7a4a22'), (2.4, .3, '#a86b33'), (0, -.9, '#8a5a2b'), (-1.6, .9, '#7a4a22'), (1.6, .8, '#8a5a2b')))
    wat = lambda x, y: f'<path d="M{x-2.6},{y-1.4} q1.4,-.6 2.6,0" stroke="#ffffff" stroke-width=".8" fill="none" opacity=".9"/>'
    b += bowl(.32, .62, '#d2553f', '#8a5a2b', kib)
    b += bowl(.68, .44, '#3f7fc4', '#8fd0f2', wat)
    return b
add('catbowls', vbowls())

exec(open('/home/claude/sprites/home_art.py').read())

# ------------------------------------------------------------------ write files
defs = '\n'.join(DEFS)
syms = '\n'.join(f'<symbol id="{i}" viewBox="0 0 {w} {h}">{body}</symbol>' for i, w, h, a, body in SYM)
open('/home/claude/sprites/vec/greenhouse_vector.svg', 'w').write(
    f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">\n<defs>\n{defs}\n{syms}\n</defs>\n</svg>\n')
atlas = {'tile': [64, 32], 'note': 'anchor = point of the tile top vertex inside the symbol viewBox',
         'symbols': {i: {'w': w, 'h': h, 'anchor': list(a)} for i, w, h, a, b in SYM}}
json.dump(atlas, open('/home/claude/sprites/vec/greenhouse_vector.json', 'w'), indent=1)
print(len(SYM), 'symbols')
