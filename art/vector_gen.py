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
      'hydrangea': ('#e2f1ff', '#7fb4f5', '#3d74d6'), 'kale': ('#f3e2fb', '#c48fe0', '#7f4aa8')}
for k, (a, b2, c) in FL.items(): rad(f'gF_{k}', [(0, a, None), (.55, b2, None), (1, c, None)])
rad('gLeafD', [(0, '#9fd88a', None), (.55, '#3f9152', None), (1, '#1f5a34', None)])
rad('gFern', [(0, '#b9e88f', None), (.5, '#4fa553', None), (1, '#1f6a38', None)])
rad('gKale', [(0, '#e7c6f5', None), (.45, '#a77bc4', None), (1, '#4f8a5a', None)])
TYPE = {'petunia': 'petal', 'vinca': 'petal', 'geranium': 'umbel', 'begonia': 'umbel', 'mum': 'pom', 'poinsettia': 'bract',
        'hydrangea': 'mop', 'pothos': 'vine', 'fern': 'frond', 'kale': 'rosette'}
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
        # terracotta pot
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
            if T == 'pom':
                for a, rr_ in ((0, .0), (.8, .55), (2.4, .55), (4.0, .55), (5.4, .5)):
                    mx, my = x + math.cos(a) * R * rr_, cy - 1 + math.sin(a) * R * rr_ * .6
                    b += circ(mx, my, 2.8, G, dk, .6) + circ(mx, my, 1.4, 'none', '#ffe38a', .6)
    return b
for crop in TYPE:
    for st in range(4):
        add(f'{crop}_{st}', flat(crop, st))

# ------------------------------------------------------------------ people
def person(view='front', frame=0, shirt='#5ccf74', shirtD='#3a9e55', hat='straw', work=False):
    b = ell(32, 55, 10, 3.4, '#1d3a24', 'opacity=".18"'); lo = 2 if frame else 0
    jean, jeanD, boot = '#4f78d6', '#3a5aa8', '#7a4a2b'
    # legs and boots
    b += f'<rect x="26.5" y="{40-lo}" width="5" height="{12}" rx="2" fill="{jeanD}"/>'
    b += f'<rect x="32.5" y="{40+lo*0}" width="5" height="{12-lo}" rx="2" fill="{jean}"/>'
    b += f'<rect x="25.5" y="{50-lo}" width="6.5" height="4" rx="2" fill="{boot}"/><rect x="32" y="{50}" width="6.5" height="4" rx="2" fill="{boot}"/>'
    # body
    b += f'<rect x="23.5" y="27" width="17" height="16" rx="6" fill="{shirt}" stroke="{shirtD}" stroke-width=".8"/>'
    if view == 'front':
        b += f'<path d="M26,33 h12 v8 a3,3 0 0 1 -3,3 h-6 a3,3 0 0 1 -3,-3 Z" fill="{jean}" stroke="{jeanD}" stroke-width=".7"/>'
        b += f'<path d="M27,33 L26.5,28 M37,33 L37.5,28" stroke="{jean}" stroke-width="1.8" stroke-linecap="round"/>'
        b += circ(28.2, 33.6, .8, '#ffd36a') + circ(35.8, 33.6, .8, '#ffd36a') + f'<rect x="30" y="36" width="4" height="3" rx="1" fill="{jeanD}"/>'
    else:
        b += f'<path d="M26,35 h12 v6 a3,3 0 0 1 -3,3 h-6 a3,3 0 0 1 -3,-3 Z" fill="{jean}" stroke="{jeanD}" stroke-width=".7"/><path d="M27,35 L30,28 M37,35 L34,28" stroke="{jean}" stroke-width="1.8" stroke-linecap="round"/>'
    # arms
    sw = (2 if frame else -2) if not work else 0
    if work:
        b += f'<rect x="19.5" y="29" width="5" height="10" rx="2.5" fill="{shirt}" stroke="{shirtD}" stroke-width=".7" transform="rotate(-35 22 30)"/>'
        b += f'<rect x="39.5" y="29" width="5" height="10" rx="2.5" fill="{shirt}" stroke="{shirtD}" stroke-width=".7" transform="rotate(35 42 30)"/>'
        # watering can held out front
        b += f'<path d="M40,38 h9 v7 a2,2 0 0 1 -2,2 h-5 a2,2 0 0 1 -2,-2 Z" fill="#4fa8ff" stroke="#1f6fd0" stroke-width=".8"/>'
        b += f'<path d="M49,40 l6,-4" stroke="#1f6fd0" stroke-width="1.6" stroke-linecap="round"/><path d="M41,38 q3,-5 7,0" fill="none" stroke="#1f6fd0" stroke-width="1.2"/>'
        b += ''.join(circ(56 + i * .6, 38 + i * 3, .9, '#8fd0ff') for i in range(3))
        b += circ(43, 37, 2, '#ffd3b0', '#c98a63', .6)
    else:
        b += f'<rect x="19.5" y="{28+sw*.5}" width="5" height="12" rx="2.5" fill="{shirt}" stroke="{shirtD}" stroke-width=".7"/>'
        b += f'<rect x="39.5" y="{28-sw*.5}" width="5" height="12" rx="2.5" fill="{shirt}" stroke="{shirtD}" stroke-width=".7"/>'
        b += circ(22, 40.5 + sw * .5, 2.2, '#ffd3b0', '#c98a63', .6) + circ(42, 40.5 - sw * .5, 2.2, '#ffd3b0', '#c98a63', .6)
    # head
    b += circ(32, 21, 8.6, '#ffd8b8', '#c98a63', .8)
    if view == 'front':
        b += ell(28.4, 21.6, 1, 1.4, '#3a2b3d') + ell(35.6, 21.6, 1, 1.4, '#3a2b3d') + circ(28.1, 21.1, .35, '#ffffff') + circ(35.3, 21.1, .35, '#ffffff')
        b += ell(26.4, 24.4, 1.8, 1.1, '#ff9a9a', 'opacity=".7"') + ell(37.6, 24.4, 1.8, 1.1, '#ff9a9a', 'opacity=".7"')
        b += '<path d="M29.5,25.4 q2.5,2.4 5,0" fill="none" stroke="#7a3b3b" stroke-width="1" stroke-linecap="round"/>'
    else:
        b += circ(32, 21, 8.6, '#8a5631', '#6a3e22', .8)
        b += '<path d="M25.5,24 q6.5,5 13,0" fill="none" stroke="#6a3e22" stroke-width=".8"/>'
        b += ell(23.6, 22, 1.4, 2, '#ffd8b8', 'stroke="#c98a63" stroke-width=".6"') + ell(40.4, 22, 1.4, 2, '#ffd8b8', 'stroke="#c98a63" stroke-width=".6"')
    if hat == 'straw':
        b += ell(32, 15.5, 14, 4.6, '#f7d77e', 'stroke="#c99f45" stroke-width=".9"')
        b += '<path d="M24.5,15 q0,-9 7.5,-9 q7.5,0 7.5,9 Z" fill="#fbe39a" stroke="#c99f45" stroke-width=".9"/>'
        b += '<path d="M24.7,13.4 q7.3,2.6 14.6,0 v2 q-7.3,2.6 -14.6,0 Z" fill="#ef5b4c"/>'
    else:
        b += '<path d="M23.6,18 q0,-10 8.4,-10 q8.4,0 8.4,10 Z" fill="#2f6fd6" stroke="#1f4f9e" stroke-width=".9"/>'
        b += (ell(37.5, 17.6, 7, 2.2, '#2559b8') if view == 'front' else ell(26.5, 17.6, 6, 2, '#2559b8'))
        b += circ(32, 8.6, 1.2, '#ffd36a')
    return b
add('grower_front_0', person('front', 0)); add('grower_front_1', person('front', 1))
add('grower_back_0', person('back', 0)); add('grower_back_1', person('back', 1))
add('grower_work', person('front', 0, work=True))
add('crew_front_0', person('front', 0, '#ffa34d', '#d77a2a', 'cap')); add('crew_front_1', person('front', 1, '#ffa34d', '#d77a2a', 'cap'))
add('crew_back_0', person('back', 0, '#ffa34d', '#d77a2a', 'cap')); add('crew_back_1', person('back', 1, '#ffa34d', '#d77a2a', 'cap')); add('crew_work', person('front', 0, '#ffa34d', '#d77a2a', 'cap', work=True))

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
VCOAT = {'anna':  dict(b='#f2a154', d='#c96f2c', w='#fff1dc', o='#9a5424', eye='#2b6b2f'),
         'miley': dict(b='#7d8592', d='#555c68', w='#ffffff', o='#3f4550', eye='#c7a12a')}
def vcat(name, pose):
    c = VCOAT[name]; o = c['o']; sw = .9
    b = ell(32, 53, 11, 2.8, '#1d3a24', 'opacity=".18"')
    stripes = (lambda pts: ''.join(f'<path d="{p}" stroke="{c["d"]}" stroke-width="1.4" fill="none" stroke-linecap="round"/>' for p in pts)) if name == 'anna' else (lambda pts: '')
    def head(x, y, closed=False):
        h = poly([(x - 5.5, y - 2), (x - 4.5, y - 8.5), (x - 1, y - 4.5)], c['b'], o, sw) + poly([(x + 5.5, y - 2), (x + 4.5, y - 8.5), (x + 1, y - 4.5)], c['b'], o, sw)
        h += poly([(x - 4.4, y - 3), (x - 4, y - 7), (x - 2, y - 4.6)], '#ffb3c0') + poly([(x + 4.4, y - 3), (x + 4, y - 7), (x + 2, y - 4.6)], '#ffb3c0')
        h += ell(x, y, 6.4, 5.6, c['b'], f'stroke="{o}" stroke-width="{sw}"')
        if name == 'miley': h += ell(x + .5, y + 2.4, 3.6, 2.6, c['w'])
        h += stripes([f'M{x-1.5},{y-5} v2', f'M{x+.5},{y-5.3} v2.2', f'M{x+2.5},{y-5} v2'])
        if closed:
            h += f'<path d="M{x-3.6},{y-.2} q1.3,1.2 2.6,0 M{x+1.6},{y-.2} q1.3,1.2 2.6,0" stroke="{o}" stroke-width=".9" fill="none" stroke-linecap="round"/>'
        else:
            h += ell(x - 2.2, y - .4, 1.2, 1.5, c['eye']) + ell(x + 2.9, y - .4, 1.2, 1.5, c['eye']) + circ(x - 1.9, y - .9, .4, '#fff') + circ(x + 3.2, y - .9, .4, '#fff')
        h += poly([(x + .1, y + 1.4), (x + 1.5, y + 1.4), (x + .8, y + 2.3)], '#ff8a9a')
        h += f'<path d="M{x+.8},{y+2.3} q-1,1.2 -2,.4 M{x+.8},{y+2.3} q1,1.2 2,.4" stroke="{o}" stroke-width=".6" fill="none"/>'
        return h
    if pose in ('walk0', 'walk1'):
        f = 1 if pose == 'walk1' else -1
        b += f'<path d="M21,43 q-8,-2 -6,-12 q1,-3 3,-1" fill="none" stroke="{o}" stroke-width="4.6" stroke-linecap="round"/>'
        b += f'<path d="M21,43 q-8,-2 -6,-12 q1,-3 3,-1" fill="none" stroke="{c["b"]}" stroke-width="3" stroke-linecap="round"/>'
        for lx, ph in ((24, f), (28, -f), (36, -f), (40, f)):
            b += f'<rect x="{lx-1.6+ph*.9}" y="44" width="3.4" height="8.5" rx="1.6" fill="{c["b"] if name=="anna" else c["w"]}" stroke="{o}" stroke-width="{sw}"/>'
        b += ell(32, 43, 12, 6.5, c['b'], f'stroke="{o}" stroke-width="{sw}"')
        if name == 'miley': b += ell(33, 46.5, 8, 2.6, c['w'])
        b += stripes(['M27,37.5 q1,3 0,6', 'M31,37 q1,3 0,6.5', 'M35,37 q1,3 0,6.5'])
        b += head(43, 35)
    elif pose == 'sit':
        b += f'<path d="M26,51 q-9,1 -8,-5 q.5,-2 2.5,-1.5" fill="none" stroke="{o}" stroke-width="4.6" stroke-linecap="round"/>'
        b += f'<path d="M26,51 q-9,1 -8,-5 q.5,-2 2.5,-1.5" fill="none" stroke="{c["b"]}" stroke-width="3" stroke-linecap="round"/>'
        b += f'<path d="M24,52 q-1,-16 9,-17 q9,1 8,17 Z" fill="{c["b"]}" stroke="{o}" stroke-width="{sw}"/>'
        b += ell(33.5, 45, 4.4, 6, c['w'])
        b += stripes(['M26,42 q2,1 3,0', 'M26,46 q2,1 3,0'])
        b += ell(30.5, 51.5, 2.4, 1.6, c['w'], f'stroke="{o}" stroke-width=".7"') + ell(36.5, 51.5, 2.4, 1.6, c['w'], f'stroke="{o}" stroke-width=".7"')
        b += head(33.5, 30)
    else:  # sleep: curled loaf
        b += ell(31, 47, 12.5, 6.5, c['b'], f'stroke="{o}" stroke-width="{sw}"')
        b += stripes(['M24,42 q1,3 0,6', 'M28,41 q1,3 0,7', 'M32,41 q1,3 0,7'])
        b += f'<path d="M19,49 q8,6 22,2" fill="none" stroke="{o}" stroke-width="4.4" stroke-linecap="round"/><path d="M19,49 q8,6 22,2" fill="none" stroke="{c["b"]}" stroke-width="2.8" stroke-linecap="round"/>'
        b += head(39, 45, True)
        b += f'<text x="44" y="33" font-family="Arial" font-weight="bold" font-size="6" fill="#7fa6d6">z</text><text x="48" y="28" font-family="Arial" font-weight="bold" font-size="4.5" fill="#7fa6d6">z</text>'
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
for _n in ('anna', 'miley'):
    for _p in ('walk0', 'walk1', 'sit', 'sleep'): add(f'cat_{_n}_{_p}', vcat(_n, _p))

# ------------------------------------------------------------------ write files
defs = '\n'.join(DEFS)
syms = '\n'.join(f'<symbol id="{i}" viewBox="0 0 {w} {h}">{body}</symbol>' for i, w, h, a, body in SYM)
open('/home/claude/sprites/vec/greenhouse_vector.svg', 'w').write(
    f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">\n<defs>\n{defs}\n{syms}\n</defs>\n</svg>\n')
atlas = {'tile': [64, 32], 'note': 'anchor = point of the tile top vertex inside the symbol viewBox',
         'symbols': {i: {'w': w, 'h': h, 'anchor': list(a)} for i, w, h, a, b in SYM}}
json.dump(atlas, open('/home/claude/sprites/vec/greenhouse_vector.json', 'w'), indent=1)
print(len(SYM), 'symbols')
