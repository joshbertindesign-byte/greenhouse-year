"""Greenhouse pixel-art sprite sheet generator.
32x32 isometric cells (2:1 tiles, 32x16 diamond). Every sprite's anchor is the
top vertex of its floor tile: (16,16) in a 32x32 cell, (16,48) in a 32x64 cell.
"""
import json, random, math
from PIL import Image, ImageDraw

def C(h):
    h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4)) + (255,)

OUT = C('#241f33')
PAL = {
    'grass': [C('#3f7a44'), C('#4f9150'), C('#64a85a'), C('#86c46a'), C('#a6d97c')],
    'conc':  [C('#9a958a'), C('#b3ad9f'), C('#c9c3b4'), C('#dad5c6'), C('#e7e2d4')],
    'soil':  [C('#3d2a22'), C('#56392b'), C('#714b35'), C('#8c6142')],
    'wood':  [C('#6b4430'), C('#8c5b3a'), C('#ad7647'), C('#c99358'), C('#ddb072')],
    'metal': [C('#4c5761'), C('#6d7b86'), C('#95a3ab'), C('#bcc8cc')],
    'frame': [C('#20392f'), C('#2f5444'), C('#447259')],
    'leaf':  [C('#1d5b37'), C('#2c7a3f'), C('#45984a'), C('#6fbb5a'), C('#a3db78')],
    'road':  [C('#4a4f55'), C('#575d63'), C('#646a70')],
    'skin':  [C('#c98c64'), C('#e6b088'), C('#f3c9a0')],
}
CROP = {
    'petunia':  [C('#8d2a6b'), C('#c2448f'), C('#e982bc'), C('#ffd1ea')],
    'geranium': [C('#8e1f26'), C('#cf3a35'), C('#f2735f'), C('#ffc2a8')],
    'mum':      [C('#9a6514'), C('#d99b22'), C('#f6c84b'), C('#fff0a8')],
    'pothos':   [C('#6e7d2a'), C('#a7b83a'), C('#d6df73'), C('#f4f5b8')],
    'vinca':    [C('#3f2a80'), C('#7656d2'), C('#a990f0'), C('#e6defe')],
    'begonia':  [C('#9c3f17'), C('#e9803a'), C('#ffae74'), C('#ffe3cc')],
    'poinsettia': [C('#6e0a18'), C('#c41e2e'), C('#ff5a5a'), C('#ffd84a')],
    'hydrangea': [C('#244a96'), C('#3d8bd6'), C('#7fb8f0'), C('#d9eeff')],
    'kale':     [C('#4e2f6c'), C('#8d5aa6'), C('#c08ad6'), C('#efe0f7')],
    'fern':     [C('#1b4f2c'), C('#2d6e3a'), C('#4f9447'), C('#9fd07a')],
}
TYPE = {'petunia': 'petal', 'vinca': 'petal', 'geranium': 'umbel', 'begonia': 'umbel', 'mum': 'pom', 'poinsettia': 'bract',
        'hydrangea': 'mop', 'pothos': 'vine', 'fern': 'frond', 'kale': 'rosette'}

def h2(x, y, s=0):
    n = (x * 374761393 + y * 668265263 + s * 2147483647) & 0xFFFFFFFF
    n = (n ^ (n >> 13)) * 1274126177 & 0xFFFFFFFF
    return ((n ^ (n >> 16)) & 0xFFFF) / 65535

def new(w=32, h=32): return Image.new('RGBA', (w, h), (0, 0, 0, 0))

def P(u, v, z=0, oy=16):
    """Tile-space (u,v in tiles, z in px) to cell pixels; tile top vertex at (16,oy)."""
    return (16 + (u - v) * 16, oy + (u + v) * 8 - z)

def mask_poly(pts, w, h):
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).polygon(pts, fill=255); return m

def fill(img, pts, fn):
    w, h = img.size; m = mask_poly(pts, w, h); px = img.load(); mp = m.load()
    for y in range(h):
        for x in range(w):
            if mp[x, y]: px[x, y] = fn(x, y)

def box(img, u0, v0, u1, v1, z0, z1, top, left, right, oy=16):
    """Iso box. top/left/right: colour or fn(x,y)."""
    f = lambda c: c if callable(c) else (lambda x, y: c)
    fill(img, [P(u0, v1, z0, oy), P(u1, v1, z0, oy), P(u1, v1, z1, oy), P(u0, v1, z1, oy)], f(left))
    fill(img, [P(u1, v0, z0, oy), P(u1, v1, z0, oy), P(u1, v1, z1, oy), P(u1, v0, z1, oy)], f(right))
    fill(img, [P(u0, v0, z1, oy), P(u1, v0, z1, oy), P(u1, v1, z1, oy), P(u0, v1, z1, oy)], f(top))

def selout(img, dark=0.55, solid=None):
    """Outline: opaque pixels touching transparency get a darker shade of themselves."""
    w, h = img.size; px = img.load(); src = img.copy().load(); edge = []
    for y in range(h):
        for x in range(w):
            if src[x, y][3] < 128: continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if nx < 0 or ny < 0 or nx >= w or ny >= h or src[nx, ny][3] < 128:
                    edge.append((x, y)); break
    for x, y in edge:
        r, g, b, a = src[x, y]
        px[x, y] = solid if solid else (int(r * dark), int(g * dark), int(b * dark), 255)

def put(img, x, y, c):
    if 0 <= x < img.size[0] and 0 <= y < img.size[1]: img.putpixel((int(x), int(y)), c)

def blit_map(img, rows, pal, ox, oy):
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch in pal and pal[ch] is not None: put(img, ox + i, oy + j, pal[ch])

# ---------------------------------------------------------------- ground tiles
SEASON = {
    'spring': {'g': [C('#3f7a44'), C('#56a052'), C('#6dba5e'), C('#92d270'), C('#b6e686')], 'dots': [C('#ffffff'), C('#ffe066'), C('#ff9ccf'), C('#c9a7ff')], 'n': 7},
    'summer': {'g': [C('#4a7a3a'), C('#5f9447'), C('#76a852'), C('#97c060'), C('#b8d77a')], 'dots': [C('#f4e27a'), C('#ffffff')], 'n': 2, 'dry': C('#b9b25c')},
    'fall':   {'g': [C('#5f5a2c'), C('#79733a'), C('#938a46'), C('#ae9f52'), C('#c8b865')], 'dots': [C('#d9772b'), C('#b8432a'), C('#e8b33a'), C('#c9572f')], 'n': 9, 'leaf': True},
    'winter': {'g': [C('#aebdd0'), C('#cfdbe8'), C('#e3ebf4'), C('#f2f6fb'), C('#ffffff')], 'dots': [C('#5f7f56'), C('#7a9a6a')], 'n': 4, 'snow': True},
}
def tile_season(season, seed):
    im = new(); sp = SEASON[season]; g = sp['g']
    def fn(x, y):
        r = h2(x, y, seed + 31)
        if sp.get('snow'): return g[3] if r < .6 else g[2] if r < .85 else g[4] if r < .95 else g[1]
        c = g[1] if r < .55 else g[2] if r < .85 else g[0] if r < .93 else g[3]
        if sp.get('dry') and h2(x // 3, y // 2, seed + 9) < .12: c = sp['dry']
        return c
    fill(im, [P(0, 0), P(1, 0), P(1, 1), P(0, 1)], fn)
    rnd = random.Random(seed * 13 + len(season))
    if not sp.get('snow'):
        for _ in range(5):
            x, y = rnd.randint(8, 23), rnd.randint(20, 28)
            if im.getpixel((x, y))[3] and im.getpixel((x, y - 2))[3]:
                put(im, x, y, g[3]); put(im, x, y - 1, g[4]); put(im, x - 1, y, g[2]); put(im, x + 1, y, g[2])
    for _ in range(sp['n']):
        x, y = rnd.randint(6, 25), rnd.randint(19, 29)
        if not im.getpixel((x, y))[3]: continue
        c = rnd.choice(sp['dots'])
        if sp.get('leaf'):
            put(im, x, y, c); put(im, x + 1, y, c); put(im, x, y + 1, tuple(int(v * .8) for v in c[:3]) + (255,))
        elif sp.get('snow'):
            put(im, x, y, c); put(im, x, y - 1, g[0] if rnd.random() < .5 else c)
        else:
            put(im, x, y, c)
            if season == 'spring': put(im, x + 1, y, C('#f6d64a'))
    return im
def tile_grass(seed):
    im = new(); g = PAL['grass']
    def fn(x, y):
        r = h2(x, y, seed)
        c = g[1] if r < .55 else g[2] if r < .85 else g[0] if r < .93 else g[3]
        return c
    fill(im, [P(0, 0), P(1, 0), P(1, 1), P(0, 1)], fn)
    rnd = random.Random(seed)
    for _ in range(5):  # little tufts
        x, y = rnd.randint(8, 23), rnd.randint(20, 28)
        if im.getpixel((x, y))[3] and im.getpixel((x, y - 2))[3]:
            put(im, x, y, g[3]); put(im, x, y - 1, g[4]); put(im, x - 1, y, g[2]); put(im, x + 1, y, g[2])
    if seed == 2:  # a few flowers
        for x, y, c in ((12, 22, C('#f4e27a')), (19, 26, C('#ffffff')), (22, 22, C('#f4e27a'))):
            put(im, x, y, c)
    return im

def tile_floor(drain=False):
    im = new(); c = PAL['conc']
    def fn(x, y):
        r = h2(x, y, 7)
        return c[3] if r < .8 else c[2] if r < .95 else c[4]
    fill(im, [P(0, 0), P(1, 0), P(1, 1), P(0, 1)], fn)
    # seams along the two far edges so the floor reads as slabs when tiled
    for t in range(16):
        put(im, 16 + t, 16 + t // 2, c[1]); put(im, 15 - t, 16 + t // 2, c[1])
    if drain:
        for x, y in ((14, 23), (16, 23), (18, 23), (15, 24), (17, 24), (14, 25), (16, 25), (18, 25)):
            put(im, x, y, c[0])
    return im

def tile_road(line=False):
    im = new(); r = PAL['road']
    fill(im, [P(0, 0), P(1, 0), P(1, 1), P(0, 1)], lambda x, y: r[1] if h2(x, y, 3) < .85 else r[0] if h2(x, y, 4) < .5 else r[2])
    if line:  # dashed centre line running along u
        for t in range(4, 12):
            for dy in (0, 1):
                put(im, 8 + t + 0, 20 + t // 2 + dy, C('#e8d98a'))
    return im

def tile_dock():
    im = new(); c = PAL['conc']
    box(im, 0, 0, 1, 1, 0, 3, lambda x, y: c[2] if h2(x, y, 9) < .85 else c[1], c[1], c[0])
    selout(im, .7)
    for t in range(1, 15):  # yellow edge line along the front-left lip
        if (t // 2) % 2 == 0: put(im, t, 24 - 3 + t // 2, C('#e0b43a'))
    return im

# ---------------------------------------------------------------- structures
def bench(kind='mid', tray=False):
    im = new(); wd, mt = PAL['wood'], PAL['metal']
    u0 = .06 if kind in ('left', 'single') else 0
    u1 = .94 if kind in ('right', 'single') else 1
    v0, v1 = .1, .9
    # legs and a stretcher bar
    for (lu, lv) in ((u0 + .04, v1 - .06), (u1 - .1, v1 - .06), (u1 - .1, v0 + .04)):
        if kind == 'mid' and lu < .5: continue
        box(im, lu, lv - .06, lu + .06, lv, 0, 9, mt[2], mt[1], mt[0])
    box(im, u0 + .05, v1 - .08, u1 - .05, v1 - .04, 3, 5, mt[2], mt[1], mt[0])
    # slatted top with a rim
    def topfn(x, y):
        return wd[4] if (x + 2 * y) % 6 == 0 else wd[3]
    box(im, u0, v0, u1, v1, 9, 12, topfn, wd[2], wd[1])
    if tray:
        sl = PAL['soil']
        box(im, u0 + .06, v0 + .08, u1 - .06, v1 - .08, 12, 14,
            lambda x, y: sl[3] if h2(x, y, 11) < .2 else sl[2] if h2(x, y, 12) < .7 else sl[1], sl[1], sl[0])
    selout(im, .55)
    return im

def wall(side='back'):
    """Glass wall segment on the far edge of a tile. 32x64 cell, anchor (16,48)."""
    im = new(32, 64); fr, cn = PAL['frame'], PAL['conc']; oy = 48
    if side == 'back':
        U = lambda a, b, z0, z1, t, l, r: box(im, a, -.08, b, .02, z0, z1, t, l, r, oy)
    else:
        U = lambda a, b, z0, z1, t, l, r: box(im, -.08, a, .02, b, z0, z1, t, l, r, oy)
    U(0, 1, 0, 9, cn[3], cn[2], cn[1])          # kneewall
    # glass panel
    glass = (196, 232, 236, 120); shine = (240, 252, 252, 170)
    if side == 'back':
        pts = [P(0, -.03, 9, oy), P(1, -.03, 9, oy), P(1, -.03, 40, oy), P(0, -.03, 40, oy)]
    else:
        pts = [P(-.03, 0, 9, oy), P(-.03, 1, 9, oy), P(-.03, 1, 40, oy), P(-.03, 0, 40, oy)]
    fill(im, pts, lambda x, y: shine if (x + y) % 11 in (0, 1) and 20 < y + x // 3 < 40 else glass)
    U(0, .1, 9, 42, fr[2], fr[1], fr[0])        # post
    U(0, 1, 40, 43, fr[2], fr[1], fr[0])         # top rail
    U(0, 1, 23, 25, fr[2], fr[1], fr[0])         # mid rail
    return im

def heater(broken=False):
    im = new(); mt = PAL['metal']
    box(im, .16, .16, .84, .84, 0, 17, mt[3], mt[2], mt[1])
    px = im.load()
    for i in range(4):  # grille on the right face
        for t in range(9):
            x = 21 + i * 2 + t // 3; y = 13 + t + i
            if 0 <= x < 32 and px[x, y][3]: px[x, y] = mt[0]
    selout(im, .55)
    lamp = C('#ff4d3a') if broken else C('#4fe07a')
    for x, y in ((15, 7), (16, 7), (15, 8), (16, 8)): put(im, x, y, lamp)
    put(im, 15, 7, C('#ffffff') if not broken else C('#ffb1a6'))
    if broken:
        for x, y in ((14, 3), (15, 2), (17, 1), (18, 3), (16, 0)): put(im, x, y, C('#8d8d8d'))
    return im

# ---------------------------------------------------------------- plants
POT = [C('#2a2730'), C('#3b3742'), C('#55505d')]
def blob(im, x, y, rx, ry, lf, rnd, var=None):
    """Shaded foliage mound, lit from the top-left."""
    for dy in range(-int(ry) - 1, int(ry) + 2):
        for dx in range(-int(rx) - 1, int(rx) + 2):
            d = (dx / rx) ** 2 + (dy / ry) ** 2
            if d > 1: continue
            if d > .72 and rnd.random() < .35: continue        # ragged leafy edge
            k = (dx / rx + dy / ry) / 2
            c = lf[4] if k < -.45 else lf[3] if k < -.05 else lf[2] if k < .4 else lf[1]
            if var and rnd.random() < .28: c = var
            elif rnd.random() < .08: c = lf[min(4, lf.index(c) + 1)]
            put(im, x + dx, y + dy, c)
def plant(crop, stage):
    """A flat of six plants on a bench top (z=12). 0 plugs, 1 young, 2 full, 3 bloom/ready."""
    im = new(); lf = PAL['leaf']; fl = CROP[crop]; rnd = random.Random(sum(map(ord, crop)) * 7 + stage)
    base = 12
    T = TYPE[crop]
    if T == 'vine': lf = [C('#1c5a2e'), C('#2b7a37'), C('#479a3e'), C('#78bd56'), C('#b5df82')]
    if T in ('frond', 'bract'): lf = [C('#123f22'), C('#1f5a30'), C('#2f7a3c'), C('#4f9a4a'), C('#86c46a')]
    if stage == 0:
        sl = PAL['soil']
        box(im, .12, .18, .88, .82, base, base + 2, lambda x, y: sl[2] if h2(x, y, 5) < .7 else sl[1], sl[1], sl[0])
        for i in range(4):
            for j in range(3):
                x, y = P(.22 + i * .19, .28 + j * .2, base + 2); x, y = int(x), int(y)
                put(im, x, y - 1, lf[3]); put(im, x - 1, y - 2, lf[4]); put(im, x + 1, y - 2, lf[3]); put(im, x, y, lf[1])
        selout(im, .6); return im
    r = {1: 2.6, 2: 4.2, 3: 4.4}[stage]
    spots = [(u, v) for v in (.3, .7) for u in (.2, .5, .8)]
    spots.sort(key=lambda p: p[0] + p[1])
    var = C('#e4e58f') if T == 'vine' else fl[2] if T == 'rosette' and stage >= 2 else None
    for (u, v) in spots:
        px_, py_ = P(u, v, base); px_, py_ = int(round(px_)), int(round(py_))
        for dx in range(-2, 3):  # pot rim
            put(im, px_ + dx, py_, POT[1]); put(im, px_ + dx, py_ + 1, POT[0])
        put(im, px_ - 2, py_ - 1, POT[2]); put(im, px_ + 2, py_ - 1, POT[1])
        cy = py_ - 1 - int(r * .6)
        if T == 'umbel' and stage == 3:
            blob(im, px_, cy + 1, r, r * .72, lf, rnd)
            for k in (-2, 1):  # umbels on stalks
                sx = px_ + k; put(im, sx, cy - 2, lf[1]); put(im, sx, cy - 3, lf[1])
                for dx, dy in ((0, 0), (-1, 0), (1, 0), (0, -1), (-1, -1), (1, -1), (0, -2)):
                    put(im, sx + dx, cy - 4 + dy, fl[1])
                put(im, sx - 1, cy - 6 + 1, fl[2]); put(im, sx, cy - 6, fl[3]); put(im, sx + 1, cy - 4, fl[0])
        elif T == 'pom' and stage == 3:
            blob(im, px_, cy, r, r * .78, lf, rnd)
            for dy in range(-int(r * .78), 1):
                for dx in range(-int(r) + 1, int(r)):
                    if (dx / r) ** 2 + (dy / (r * .78)) ** 2 < .8 and rnd.random() < .8:
                        k = (dx + dy) / r
                        put(im, px_ + dx, cy + dy - 1, fl[3] if k < -.6 else fl[2] if k < .2 else fl[1])
        else:
            blob(im, px_, cy, r, r * .78, lf, rnd, var)
            if T == 'bract' and stage == 3:
                for fx, fy in ((px_ - 2, cy - 1), (px_ + 2, cy)):
                    for dx, dy, c in ((0, 0, fl[3]), (-1, 0, fl[1]), (1, 0, fl[1]), (0, -1, fl[2]), (0, 1, fl[1]), (-2, 0, fl[0]), (2, 0, fl[1]), (0, -2, fl[2]), (-1, -1, fl[2]), (1, 1, fl[0])):
                        put(im, fx + dx, fy + dy, c)
            if T == 'mop' and stage == 3:
                for dy in range(-3, 3):
                    for dx in range(-3, 4):
                        if dx * dx + dy * dy * 1.3 <= 9: put(im, px_ + dx, cy - 2 + dy, fl[3] if dx + dy < -2 else fl[2] if dx + dy < 1 else fl[1])
            if T == 'rosette':
                put(im, px_, cy, fl[1]); put(im, px_ + 1, cy, fl[0]); put(im, px_, cy - 1, fl[2])
            if T == 'frond':
                for k in (-3, 0, 3):
                    put(im, px_ + k, cy - 3, lf[4]); put(im, px_ + k + (1 if k > 0 else -1 if k < 0 else 0), cy - 4, lf[3])
            if T == 'petal' and stage == 3:
                for _ in range(4):
                    fx = px_ + rnd.randint(-3, 2); fy = cy + rnd.randint(-3, 1)
                    for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1)): put(im, fx + dx, fy + dy, fl[1])
                    put(im, fx, fy, fl[2]); put(im, fx + 1, fy + 1, fl[3])
            if T in ('vine', 'frond') and stage >= 2 and v > .5:  # trailing vines over the front
                for t in range(3 + stage):
                    put(im, px_ - 2 + (t % 2), py_ + 2 + t, lf[3] if t % 2 else lf[2])
    selout(im, .5)
    return im

# ---------------------------------------------------------------- characters
GROWER_FRONT = [
    "....oooooo....",
    "...ohhhhhho...",
    "..ohhhhhhhho..",
    ".ooHHHHHHHHoo.",
    "oHHHHHHHHHHHHo",
    ".oooossssoooo.",
    "....osesesso..",
    "....osssssso..",
    ".....oSSSSo...",
    "...ooggwwggoo.",
    "..oggggggggggo",
    "..ogGggggggGgo",
    "..osoGggggGoso",
    "..oso.gggg.oso",
    "...o.oGGGGo.o.",
    ".....oppppo...",
    ".....opPPpo...",
    ".....opo.opo..",
    ".....opo.opo..",
    ".....obo.obo..",
    "....obbo.obbo.",
    "....oooo.oooo.",
]
GROWER_BACK = [
    "....oooooo....",
    "...ohhhhhho...",
    "..ohhhhhhhho..",
    ".ooHHHHHHHHoo.",
    "oHHHHHHHHHHHHo",
    ".oooHHHHHHooo.",
    "....oSSSSSo...",
    "....oSSSSSo...",
    ".....oSSSo....",
    "...ooGGGGGGoo.",
    "..oGGGGGGGGGGo",
    "..oGGGGGGGGGGo",
    "..oSoGGGGGGoSo",
    "..oSo.GGGG.oSo",
    "...o.oGGGGo.o.",
    ".....oPPPPo...",
    ".....oPPPPo...",
    ".....oPo.oPo..",
    ".....oPo.oPo..",
    ".....obo.obo..",
    "....obbo.obbo.",
    "....oooo.oooo.",
]
def step(rows, phase):
    """Walk frame: shift one leg up."""
    rows = [list(r) for r in rows]
    if phase == 1:
        for y in (17, 18, 19, 20, 21):
            for x in range(9, 13):
                rows[y - 1][x] = rows[y][x] if y > 17 else rows[y - 1][x]
        rows[21][9:13] = list('....')
    return [''.join(r) for r in rows]
def work(rows):
    rows = [list(r) for r in rows]
    for y in (12, 13):  # arms forward and down
        rows[y][2:5] = list('...'); rows[y][11:14] = list('...')
    rows[13][4:6] = list('os'); rows[13][9:11] = list('so')
    rows[14][4:6] = list('oS'); rows[14][9:11] = list('So')
    return [''.join(r) for r in rows]
def person(rows, shirt, hat, ox=9, oy=4):
    im = new()
    pal = {'o': OUT, 'h': hat[1], 'H': hat[0], 's': PAL['skin'][1], 'S': PAL['skin'][0], 'e': C('#2b2233'),
           'g': shirt[1], 'G': shirt[0], 'w': C('#f2efe6'), 'p': C('#4a5370'), 'P': C('#353c54'), 'b': C('#4a3226')}
    # soft shadow first
    for x in range(10, 23):
        for y in range(26, 29):
            if ((x - 16) / 6.5) ** 2 + ((y - 27.3) / 1.6) ** 2 < 1: put(im, x, y, (20, 30, 20, 70))
    blit_map(im, rows, pal, ox, oy)
    return im

# ---------------------------------------------------------------- cats (facing right; flip for left)
CAT = {
 'walk0': ["...........o..o.",
           "..........obooboo",
           "..........obbbbbo",
           "..oo......obebebo",
           ".obbo.....obbpbbo",
           ".obo.oooooobbbbo.",
           "..oobbbbbbbbbbo..",
           "...obbbbbbbbbbo..",
           "...owbbbbbbbwwo..",
           "...obo.ob..obo...",
           "...oo..oo..oo....",
           ],
 'walk1': ["...........o..o.",
           "..........obooboo",
           "..........obbbbbo",
           "..oo......obebebo",
           ".obbo.....obbpbbo",
           ".obo.oooooobbbbo.",
           "..oobbbbbbbbbbo..",
           "...obbbbbbbbbbo..",
           "...owbbbbbbbwwo..",
           "....obo.obo.obo..",
           "....oo..oo..oo...",
           ],
 'sit':   ["........o..o....",
           ".......obooboo..",
           ".......obbbbbo..",
           ".......obebebo..",
           ".......obbpbbo..",
           "........obbbo...",
           ".......obbbbbo..",
           "..oo..obbbbbwo..",
           ".obbooobbbbbwo..",
           "..obbbbbbbbbwo..",
           "...oooooowowoo..",
           ],
 'sleep': ["................",
           "................",
           "................",
           "................",
           "......oooooo....",
           "....oobbbbbboo..",
           "...obbbbbbbbobo.",
           "..obbbbbbbobbebo",
           "..obbbbbbbbobbbo",
           "..oobwwwbbbbooo.",
           "....ooooooooo...",
           ],
}
COAT = {
    'anna':  {'b': C('#eb9a4c'), 'd': C('#b9642a'), 'w': C('#fff0d6'), 'p': C('#ff9aa8'), 'e': C('#2b2233')},
    'miley': {'b': C('#727986'), 'd': C('#4c525c'), 'w': C('#f6f6f6'), 'p': C('#ff9aa8'), 'e': C('#1f2a1f')},
}
def cat(name, pose):
    im = new(); co = COAT[name]
    for x in range(10, 24):
        for y in range(26, 29):
            if ((x - 16.5) / 6) ** 2 + ((y - 27.3) / 1.4) ** 2 < 1: put(im, x, y, (20, 30, 20, 60))
    rows = CAT[pose]; ox, oy = 9, 27 - len(rows)
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch == '.': continue
            c = OUT if ch == 'o' else co.get(ch, co['b'])
            if ch == 'b' and name == 'anna' and (i + j) % 4 == 0: c = co['d']          # tabby stripes
            if ch == 'b' and name == 'miley' and j >= len(rows) - 4 and i < 10: c = co['w']   # tuxedo belly
            put(im, ox + i, oy + j, c)
    return im

# ---------------------------------------------------------------- icons
GLYPH = {
 'pot': ["......w.......", "....ww.ww.....", "...w..w..w....", "......w.......", "..wwwwwwwwww..", "..wwwwwwwwww..",
         "...wwwwwwww...", "...wwwwwwww...", "....wwwwww....", "....wwwwww....", ".............."],
 'water': ["......ww......", ".....wwww.....", "....wwwwww....", "...wwwwwwww...", "..wwwwwwwwww..", "..wswwwwwwww..",
           "..wswwwwwwww..", "...wwwwwwww...", "....wwwwww....", ".............."],
 'pest': ["..w........w..", "...w..ww..w...", "....wwwwww....", "w..wwwwwwww..w", ".wwwwwwwwwwww.", "...wwwwwwww...",
          ".wwwwwwwwwwww.", "w..wwwwwwww..w", "....wwwwww....", "......ww......"],
 'fix': ["..........ww..", ".........ww.w.", ".........w..ww", "........ww.ww.", ".......wwww...", "......www.....",
         ".....www......", "....www.......", "...www........", "..www.........", "..ww.........."],
 'load': [".wwwwwwww.....", ".wwwwwwww.ww..", ".wwwwwwww.www.", ".wwwwwwww.wwww", ".wwwwwwwwwwwww", ".wwwwwwwwwwwww",
          "..ww......ww..", "..ww......ww.."],
}
ICOL = {'pot': C('#9a5b26'), 'water': C('#2a78d0'), 'pest': C('#cf3a2f'), 'fix': C('#56606b'), 'load': C('#2c8a47')}
def icon(kind):
    im = new(); col = ICOL[kind]; dark = tuple(int(c * .6) for c in col[:3]) + (255,)
    for y in range(32):
        for x in range(32):
            d = math.hypot(x - 15.5, y - 13.5)
            if d < 12.5: put(im, x, y, OUT)
            if d < 11.5: put(im, x, y, C('#ffffff'))
            if d < 9.6: put(im, x, y, col)
            if 7.6 < d < 9.6 and y > 15: put(im, x, y, dark)
    for (x, y) in ((14, 26), (15, 26), (16, 26), (17, 26), (15, 27), (16, 27), (15, 28)): put(im, x, y, OUT)
    for (x, y) in ((15, 25), (16, 25), (15, 26), (16, 26)): put(im, x, y, C('#ffffff'))
    gl = GLYPH[kind]; oy = 14 - len(gl) // 2
    for j, row in enumerate(gl):
        for i, ch in enumerate(row):
            if ch == 'w': put(im, 9 + i, oy + j, C('#ffffff'))
            elif ch == 's': put(im, 9 + i, oy + j, C('#bfe0ff'))
    return im

# ---------------------------------------------------------------- truck (64x64, anchor 32,40)
def truck():
    im = new(64, 64); oy = 40
    def Pt(u, v, z): return (32 + (u - v) * 16, oy + (u + v) * 8 - z)
    def bx(u0, v0, u1, v1, z0, z1, t, l, r):
        f = lambda c: c if callable(c) else (lambda x, y: c)
        fill(im, [Pt(u0, v1, z0), Pt(u1, v1, z0), Pt(u1, v1, z1), Pt(u0, v1, z1)], f(l))
        fill(im, [Pt(u1, v0, z0), Pt(u1, v1, z0), Pt(u1, v1, z1), Pt(u1, v0, z1)], f(r))
        fill(im, [Pt(u0, v0, z1), Pt(u1, v0, z1), Pt(u1, v1, z1), Pt(u0, v1, z1)], f(t))
    bx(-1.2, -.35, .9, .35, 4, 26, C('#f2efe5'), C('#d9d4c4'), C('#bdb7a6'))
    bx(.95, -.3, 1.6, .3, 4, 18, C('#3c9a5c'), C('#2e7d4a'), C('#22613a'))
    # windscreen and a stripe on the box
    fill(im, [Pt(1.6, -.22, 10), Pt(1.6, .22, 10), Pt(1.6, .22, 16), Pt(1.6, -.22, 16)], lambda x, y: C('#bfe6f2') if (x + y) % 5 else C('#ffffff'))
    fill(im, [Pt(-1.1, .35, 10), Pt(.85, .35, 10), Pt(.85, .35, 14), Pt(-1.1, .35, 14)], lambda x, y: C('#2e7d4a'))
    selout(im, .5)
    for wu in (-.8, .5, 1.3):  # wheels
        x, y = Pt(wu, .35, 2)
        for dx in range(-3, 4):
            for dy in range(-2, 3):
                if (dx / 3.4) ** 2 + (dy / 2.4) ** 2 <= 1: put(im, int(x) + dx, int(y) + dy, OUT if abs(dx) > 1 or abs(dy) > 1 else C('#6d6d6d'))
    return im

# ---------------------------------------------------------------- assemble the sheet
cells = []  # (name, image, w_cells, h_cells, anchor)
def add(name, im, w=1, h=1, anchor=(16, 16)): cells.append((name, im, w, h, anchor))

add('grass_a', tile_grass(1)); add('grass_b', tile_grass(2)); add('grass_c', tile_grass(3))
for _ss in ('winter', 'spring', 'summer', 'fall'):
    for _i, _v in enumerate('abc'): add(f'grass_{_ss}_{_v}', tile_season(_ss, _i + 1))
add('floor', tile_floor()); add('floor_drain', tile_floor(True)); add('road', tile_road()); add('road_line', tile_road(True)); add('dock', tile_dock())
add('bench_left', bench('left')); add('bench_mid', bench('mid')); add('bench_right', bench('right')); add('bench_single', bench('single'))
add('bench_left_tray', bench('left', True)); add('bench_mid_tray', bench('mid', True)); add('bench_right_tray', bench('right', True)); add('heater', heater())
for crop in TYPE:
    for st in range(4):
        add(f'{crop}_{st}', plant(crop, st))
GREEN = (C('#2f7d48'), C('#45a160')); STRAW = (C('#c9a24e'), C('#ecd27f'))
BLUE = (C('#2c5f9e'), C('#4b86cc')); CAP = (C('#1f3f6e'), C('#3a6aa8'))
add('grower_front_0', person(GROWER_FRONT, GREEN, STRAW)); add('grower_front_1', person(step(GROWER_FRONT, 1), GREEN, STRAW))
add('grower_back_0', person(GROWER_BACK, GREEN, STRAW)); add('grower_back_1', person(step(GROWER_BACK, 1), GREEN, STRAW))
add('grower_work', person(work(GROWER_FRONT), GREEN, STRAW))
add('crew_front_0', person(GROWER_FRONT, BLUE, CAP)); add('crew_front_1', person(step(GROWER_FRONT, 1), BLUE, CAP)); add('heater_broken', heater(True))
add('crew_back_0', person(GROWER_BACK, BLUE, CAP)); add('crew_back_1', person(step(GROWER_BACK, 1), BLUE, CAP)); add('crew_work', person(work(GROWER_FRONT), BLUE, CAP))
for k in ('pot', 'water', 'pest', 'fix', 'load'): add(f'icon_{k}', icon(k), anchor=(16, 28))
for _n in ('anna', 'miley'):
    for _p in ('walk0', 'walk1', 'sit', 'sleep'): add(f'cat_{_n}_{_p}', cat(_n, _p))
add('wall_back', wall('back'), 1, 2, (16, 48)); add('wall_left', wall('left'), 1, 2, (16, 48))
add('truck', truck(), 2, 2, (32, 40))

COLS = 8
# pack: walk a grid, placing multi-cell sprites where they fit
grid = {}; placed = []
def free(cx, cy, w, h): return all((cx + i, cy + j) not in grid for i in range(w) for j in range(h)) and cx + w <= COLS
for name, im, w, h, anc in cells:
    cy = 0
    while True:
        spot = next((cx for cx in range(COLS) if free(cx, cy, w, h)), None)
        if spot is not None: break
        cy += 1
    for i in range(w):
        for j in range(h): grid[(spot + i, cy + j)] = name
    placed.append((name, im, spot, cy, w, h, anc))
rows = max(cy + h for _, _, _, cy, _, h, _ in placed)
sheet = Image.new('RGBA', (COLS * 32, rows * 32), (0, 0, 0, 0))
atlas = {'tile': [32, 16], 'cell': 32, 'note': 'anchor = pixel of the tile top vertex inside the frame', 'frames': {}}
for name, im, cx, cy, w, h, anc in placed:
    sheet.alpha_composite(im, (cx * 32, cy * 32))
    atlas['frames'][name] = {'x': cx * 32, 'y': cy * 32, 'w': w * 32, 'h': h * 32, 'anchor': list(anc)}
sheet.save('/home/claude/sprites/greenhouse_sheet.png')
json.dump(atlas, open('/home/claude/sprites/greenhouse_sheet.json', 'w'), indent=1)
big = sheet.resize((sheet.width * 4, sheet.height * 4), Image.NEAREST)
bg = Image.new('RGBA', big.size, (238, 234, 222, 255)); bg.alpha_composite(big); bg.save('/home/claude/sprites/preview4x.png')
print(sheet.size, len(placed))
