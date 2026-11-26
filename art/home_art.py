# Homestead art: one symbol per 3x3 lot, anchored at the lot's top (back) vertex.
# Exec'd from vec.py, so Iso, poly, circ, ell, lin, rad, add, cluster, FL and f2 are in scope.
HW, HH, HAX, HAY = 208, 236, 104, 128
rnd = random.Random(7)

lin('gRoofR', [(0, '#c8503f', None), (1, '#9a3328', None)])
lin('gRoofG', [(0, '#5f8f6a', None), (1, '#3e6a4c', None)])
lin('gRoofT', [(0, '#3fa6a0', None), (1, '#2a7a76', None)])
lin('gRoofS', [(0, '#7d8a90', None), (1, '#5a666c', None)])
lin('gSidingL', [(0, '#fbf5e6', None), (1, '#eadfc4', None)])
lin('gSidingR', [(0, '#e4d6b6', None), (1, '#cdbd98', None)])
lin('gWin', [(0, '#d9f1ff', None), (1, '#8fc4e6', None)], 0, 0, 1, 1)
lin('gWater', [(0, '#8fd4f2', None), (1, '#3f97c9', None)], 0, 0, 1, 1)
rad('gTree', [(0, '#a8e07a', None), (.55, '#5aa64e', None), (1, '#2f7a3f', None)], .35, .3, .85)
rad('gTreeD', [(0, '#8fce6a', None), (.55, '#3f8f45', None), (1, '#1f5a34', None)], .35, .3, .85)
rad('gPeach', [(0, '#ffe0a0', None), (.6, '#ffa04a', None), (1, '#e0602a', None)], .35, .3, .8)
rad('gRock', [(0, '#e2e5e6', None), (.6, '#a9b0b3', None), (1, '#727b80', None)], .35, .3, .85)
rad('gBrush', [(0, '#d9c47a', None), (.6, '#a88a4a', None), (1, '#6e5a2e', None)], .4, .3, .85)
rad('gRust', [(0, '#e0915a', None), (.6, '#a8552a', None), (1, '#6e3418', None)], .35, .3, .85)

def fv(I, v, u0, u1, z0, z1, fill, stroke='none', sw=.8):
    return poly([I.P(u0, v, z0), I.P(u1, v, z0), I.P(u1, v, z1), I.P(u0, v, z1)], fill, stroke, sw)
def fu(I, u, v0, v1, z0, z1, fill, stroke='none', sw=.8):
    return poly([I.P(u, v0, z0), I.P(u, v1, z0), I.P(u, v1, z1), I.P(u, v0, z1)], fill, stroke, sw)
def flat(I, u0, v0, u1, v1, z, fill, stroke='none', sw=.8):
    return poly([I.P(u0, v0, z), I.P(u1, v0, z), I.P(u1, v1, z), I.P(u0, v1, z)], fill, stroke, sw)
def seg(a, b, col, w=1, extra=''):
    return f'<path d="M{f2(a[0])},{f2(a[1])} L{f2(b[0])},{f2(b[1])}" stroke="{col}" stroke-width="{w}" stroke-linecap="round" {extra}/>'
def shadow(I, u0, v0, u1, v1, o=.18):
    return flat(I, u0 + o * .6, v0 + o, u1 + o * .6, v1 + o, 0, '#1d3a24', 'none', 0).replace('/>', ' opacity=".16"/>')

def win_v(I, v, u0, u1, z0, z1, shutters=True, box=False):
    b = ''
    if shutters:
        w = (u1 - u0) * .32
        b += fv(I, v + .01, u0 - w, u0, z0, z1, '#3f7a5a', '#2a5a40', .6) + fv(I, v + .01, u1, u1 + w, z0, z1, '#3f7a5a', '#2a5a40', .6)
    b += fv(I, v + .01, u0, u1, z0, z1, '#ffffff', '#b9ad95', .7) + fv(I, v + .02, u0 + .05, u1 - .05, z0 + 1.5, z1 - 1.5, 'url(#gWin)')
    m = (u0 + u1) / 2
    b += seg(I.P(m, v + .02, z0 + 1.5), I.P(m, v + .02, z1 - 1.5), '#ffffff', 1) + seg(I.P(u0 + .05, v + .02, (z0 + z1) / 2), I.P(u1 - .05, v + .02, (z0 + z1) / 2), '#ffffff', 1)
    if box:
        b += I.box(u0 - .05, v, u1 + .05, v + .12, z0 - 4, z0, '#8a5a3a', '#7a4a2b', '#6a3e22', '#4a2a18', .5)
        for i in range(5):
            x, y = I.P(u0 + (u1 - u0) * (i + .5) / 5, v + .08, z0 + 1)
            b += circ(x, y - 1, 1.8, ['#ff6fa0', '#ffd23a', '#ff8a5a', '#ffffff', '#c77dff'][i % 5], '#00000033', .3)
    return b
def win_u(I, u, v0, v1, z0, z1, shutters=False):
    b = ''
    if shutters:
        w = (v1 - v0) * .32
        b += fu(I, u + .01, v0 - w, v0, z0, z1, '#3f7a5a', '#2a5a40', .6) + fu(I, u + .01, v1, v1 + w, z0, z1, '#3f7a5a', '#2a5a40', .6)
    b += fu(I, u + .01, v0, v1, z0, z1, '#ffffff', '#b9ad95', .7) + fu(I, u + .02, v0 + .05, v1 - .05, z0 + 1.5, z1 - 1.5, 'url(#gWin)')
    m = (v0 + v1) / 2
    b += seg(I.P(u + .02, m, z0 + 1.5), I.P(u + .02, m, z1 - 1.5), '#ffffff', 1) + seg(I.P(u + .02, v0 + .05, (z0 + z1) / 2), I.P(u + .02, v1 - .05, (z0 + z1) / 2), '#ffffff', 1)
    return b

def gable_u(I, u0, v0, u1, v1, z, h, roof, roofD, wall, edge='#5a2a20', o=.12, lines=4):
    """Ridge runs along u; the front slope faces +v and the gable end faces +u."""
    vm = (v0 + v1) / 2
    b = poly([I.P(u0 - o, v0 - o, z), I.P(u1 + o, v0 - o, z), I.P(u1 + o, vm, z + h), I.P(u0 - o, vm, z + h)], roofD, edge, .8)
    b += poly([I.P(u1, v0, z), I.P(u1, v1, z), I.P(u1, vm, z + h)], wall, '#00000022', .6)
    b += poly([I.P(u0 - o, v1 + o, z), I.P(u1 + o, v1 + o, z), I.P(u1 + o, vm, z + h), I.P(u0 - o, vm, z + h)], roof, edge, .8)
    for k in range(1, lines):
        t = k / lines
        b += seg(I.P(u0 - o, v1 + o - (v1 + o - vm) * t, z + h * t), I.P(u1 + o, v1 + o - (v1 + o - vm) * t, z + h * t), '#00000026', .8)
    b += poly([I.P(u1 + o, v0 - o, z), I.P(u1 + o, vm, z + h), I.P(u1 + o, v1 + o, z), I.P(u1 + o + .02, v1 + o, z - 1.5), I.P(u1 + o + .02, vm, z + h - 1.5), I.P(u1 + o + .02, v0 - o, z - 1.5)], '#ffffff', 'none')
    return b
def gable_v(I, u0, v0, u1, v1, z, h, roof, roofD, wall, edge='#5a2a20', o=.12, lines=4):
    """Ridge runs along v; the right slope faces +u and the gable end faces +v."""
    um = (u0 + u1) / 2
    b = poly([I.P(u0 - o, v0 - o, z), I.P(u0 - o, v1 + o, z), I.P(um, v1 + o, z + h), I.P(um, v0 - o, z + h)], roofD, edge, .8)
    b += poly([I.P(u0, v1, z), I.P(u1, v1, z), I.P(um, v1, z + h)], wall, '#00000022', .6)
    b += poly([I.P(u1 + o, v0 - o, z), I.P(u1 + o, v1 + o, z), I.P(um, v1 + o, z + h), I.P(um, v0 - o, z + h)], roof, edge, .8)
    for k in range(1, lines):
        t = k / lines
        b += seg(I.P(u1 + o - (u1 + o - um) * t, v0 - o, z + h * t), I.P(u1 + o - (u1 + o - um) * t, v1 + o, z + h * t), '#00000026', .8)
    b += poly([I.P(u0 - o, v1 + o, z), I.P(um, v1 + o, z + h), I.P(u1 + o, v1 + o, z), I.P(u1 + o, v1 + o + .02, z - 1.5), I.P(um, v1 + o + .02, z + h - 1.5), I.P(u0 - o, v1 + o + .02, z - 1.5)], '#ffffff', 'none')
    return b

def bush(x, y, r, g='url(#gTree)', st='#2f6a38', seed=0, flowers=None):
    rr = random.Random(seed); b = ''
    for k in range(6):
        a = k / 6 * 6.28 + rr.random() * .5
        b += circ(x + math.cos(a) * r * .5, y + math.sin(a) * r * .28 - r * .2, r * (.55 + rr.random() * .15), g, st, .7)
    b += circ(x, y - r * .45, r * .62, g, st, .7)
    if flowers:
        for k in range(7):
            b += circ(x + (rr.random() - .5) * r * 1.4, y - r * .2 - rr.random() * r * .7, r * .13, flowers, '#00000030', .3)
    return b
def tree(x, y, s=1., g='url(#gTree)', fruit=None, seed=1):
    rr = random.Random(seed)
    b = ell(x + 6 * s, y + 2 * s, 20 * s, 7 * s, '#1d3a24', 'opacity=".16"')
    b += f'<path d="M{f2(x-3*s)},{f2(y)} q1,-14 -1,-26 h{f2(8*s)} q-2,12 -1,26 Z" fill="#8a5a3a" stroke="#5a3a22" stroke-width=".8"/>'
    b += f'<path d="M{f2(x)},{f2(y-20*s)} l-8,-8 M{f2(x+2*s)},{f2(y-18*s)} l9,-9" stroke="#7a4a2b" stroke-width="{f2(2.4*s)}" stroke-linecap="round"/>'
    for dx, dy, r in ((-13, -34, 13), (12, -34, 13), (0, -46, 15), (-7, -26, 11), (9, -25, 11), (0, -34, 14)):
        b += circ(x + dx * s, y + dy * s, r * s, g, '#2f6a38', .8)
    b += circ(x - 5 * s, y - 50 * s, 5 * s, '#ffffff', 'none', 1, 'opacity=".18"')
    if fruit:
        for k in range(9):
            b += circ(x + (rr.random() - .5) * 34 * s, y - (22 + rr.random() * 30) * s, 2.4 * s, fruit, '#a8401a', .4)
    return b
def pine(x, y, s=1.):
    b = ell(x + 5 * s, y + 2 * s, 15 * s, 5 * s, '#1d3a24', 'opacity=".16"') + f'<rect x="{f2(x-2.5*s)}" y="{f2(y-10*s)}" width="{f2(5*s)}" height="{f2(10*s)}" fill="#7a4a2b"/>'
    for k, (w, yy) in enumerate(((17, -8), (14, -22), (11, -35), (7, -46))):
        b += poly([(x - w * s, y + yy * s), (x + w * s, y + yy * s), (x, y + (yy - 20) * s)], 'url(#gTreeD)' if k % 2 else '#2f7a4a', '#1f5a34', .8)
    return b
def flowers(x, y, crop, r=4, n=6, seed=0):
    rr = random.Random(seed); b = cluster(x, y, r * 1.1, 'url(#gLeaf)', '#2f7a3f', seed)
    for k in range(n):
        a = rr.random() * 6.28; d = rr.random() * r * .8
        b += circ(x + math.cos(a) * d, y - r * .3 + math.sin(a) * d * .55, r * .36, f'url(#gF_{crop})', '#00000030', .3)
    return b
def picket(I, pts, h=9, col='#ffffff', dk='#c9c0ad'):
    b = ''
    for (u0, v0), (u1, v1) in zip(pts, pts[1:]):
        n = max(2, int(math.hypot(u1 - u0, v1 - v0) / .18))
        b += seg(I.P(u0, v0, h * .45), I.P(u1, v1, h * .45), dk, 1.6) + seg(I.P(u0, v0, h * .8), I.P(u1, v1, h * .8), dk, 1.6)
        for k in range(n + 1):
            u, v = u0 + (u1 - u0) * k / n, v0 + (v1 - v0) * k / n
            a, c = I.P(u, v, 0), I.P(u, v, h)
            b += f'<path d="M{f2(a[0]-1.2)},{f2(a[1])} V{f2(c[1]+1)} l1.2,-2 l1.2,2 V{f2(a[1])} Z" fill="{col}" stroke="{dk}" stroke-width=".5"/>'
    return b
def stones(I, pts, r=2.4):
    return ''.join(ell(*I.P(u, v, 0), r * 1.6, r * .9, '#d9d2c2', 'stroke="#a8a090" stroke-width=".6"') for u, v in pts)

def lot(fn):
    def w():
        I = Iso(HAX, HAY); return fn(I)
    return w

# ---------------------------------------------------------------- farmhouse
@lot
def farmhouse(I):
    b = tree(*I.P(.35, .25, 0), 1.15, seed=3) + shadow(I, .35, .5, 2.6, 2.0)
    b += I.box(.4, .55, 2.25, 2.0, 0, 3, '#cfc3a6', '#b8ab8c', '#a89a7a', '#8a7d60', .6)
    # side wing on the right
    b += I.box(2.25, .9, 2.85, 1.85, 3, 24, 'url(#gSidingL)', 'url(#gSidingL)', 'url(#gSidingR)', '#b9ad95', .8)
    b += poly([I.P(2.25, .82, 24), I.P(2.93, .82, 21), I.P(2.93, 1.93, 21), I.P(2.25, 1.93, 24)], 'url(#gRoofR)', '#5a2a20', .8)
    b += win_u(I, 2.85, 1.15, 1.6, 9, 18)
    # main house
    b += I.box(.4, .55, 2.25, 2.0, 3, 38, 'url(#gSidingL)', 'url(#gSidingL)', 'url(#gSidingR)', '#b9ad95', .8)
    for z in range(8, 38, 4): b += seg(I.P(.4, 2.0, z), I.P(2.25, 2.0, z), '#00000012', .6) + seg(I.P(2.25, .55, z), I.P(2.25, 2.0, z), '#00000014', .6)
    b += win_v(I, 2.0, .62, .98, 24, 34) + win_v(I, 2.0, 1.66, 2.02, 24, 34)
    b += win_u(I, 2.25, .78, 1.12, 24, 34, True) + win_u(I, 2.25, 1.42, 1.76, 24, 34, True)
    b += win_u(I, 2.25, .78, 1.12, 8, 18, True)
    b += gable_u(I, .4, .55, 2.25, 2.0, 38, 26, 'url(#gRoofR)', '#8a2e24', 'url(#gSidingR)', lines=5)
    # dormer on the front slope
    b += I.box(1.12, 1.35, 1.52, 1.72, 44, 54, 'url(#gSidingL)', 'url(#gSidingL)', 'url(#gSidingR)', '#b9ad95', .6)
    b += fv(I, 1.72, 1.2, 1.44, 46, 52, 'url(#gWin)', '#ffffff', 1)
    b += gable_v(I, 1.1, 1.3, 1.54, 1.75, 54, 7, 'url(#gRoofR)', '#8a2e24', 'url(#gSidingL)', o=.05, lines=2)
    b += I.box(1.85, .75, 2.05, .95, 50, 66, '#b5654a', '#9a4e38', '#874430', '#5a2a20', .7) + I.box(1.82, .72, 2.08, .98, 66, 68, '#6a6f72', '#55595c', '#45494b', '#333', .5)
    b += circ(*I.P(1.95, .85, 72), 3, '#ffffff', 'none', 1, 'opacity=".5"') + circ(*I.P(1.9, .8, 79), 4, '#ffffff', 'none', 1, 'opacity=".35"')
    # porch
    b += I.box(.32, 2.0, 2.33, 2.6, 0, 4, '#c9a77a', '#a8855a', '#94744c', '#6a5232', .7)
    for u in (.55, .85, 1.15, 1.45, 1.75, 2.05): b += seg(I.P(u, 2.0, 4), I.P(u, 2.6, 4), '#00000018', .6)
    b += fv(I, 2.0, 1.15, 1.45, 4, 20, '#7a4a2b', '#4a2a18', .8) + fv(I, 2.01, 1.2, 1.4, 12, 18, 'url(#gWin)') + circ(*I.P(1.4, 2.02, 11), 1, '#ffd23a')
    b += win_v(I, 2.0, .55, .95, 8, 18, False, True) + win_v(I, 2.0, 1.7, 2.1, 8, 18, False, True)
    b += I.box(1.12, 2.6, 1.5, 2.85, 0, 2, '#d9c29a', '#b8a07a', '#a88f6a', '#6a5232', .5)
    for u in (.36, 1.0, 1.62, 2.26):
        b += I.box(u, 2.52, u + .07, 2.59, 4, 22, '#ffffff', '#ffffff', '#e6dfd0', '#b9ad95', .5)
    b += seg(I.P(.36, 2.56, 10), I.P(1.12, 2.56, 10), '#ffffff', 1.6) + seg(I.P(1.5, 2.56, 10), I.P(2.33, 2.56, 10), '#ffffff', 1.6)
    b += poly([I.P(.25, 1.98, 25), I.P(2.4, 1.98, 25), I.P(2.4, 2.7, 21), I.P(.25, 2.7, 21)], '#7f8a8e', '#4a5256', .8)
    b += poly([I.P(2.4, 1.98, 25), I.P(2.4, 2.7, 21), I.P(2.4, 2.7, 19.5), I.P(2.4, 1.98, 23.5)], '#5a666c')
    # rocking chair and a pot of mums
    x, y = I.P(.7, 2.3, 4); b += f'<path d="M{f2(x-4)},{f2(y)} q4,3 8,0" fill="none" stroke="#6a3e22" stroke-width="1.4"/><rect x="{f2(x-3.5)}" y="{f2(y-12)}" width="7" height="10" rx="1.5" fill="#8a5a3a"/>'
    x, y = I.P(2.15, 2.35, 4); b += poly([(x - 4, y - 5), (x + 4, y - 5), (x + 3, y), (x - 3, y)], '#ee8656', '#c9643a', .6) + flowers(x, y - 8, 'mum', 5, 7, 2)
    # front fence, mailbox, path
    b += stones(I, [(1.32, 2.95), (1.36, 3.0)], 2)
    b += picket(I, [(.05, 2.92), (1.08, 2.92)]) + picket(I, [(1.62, 2.92), (2.95, 2.92)])
    x, y = I.P(2.75, 2.75, 0); b += seg((x, y), (x, y - 13), '#6a3e22', 1.8) + f'<rect x="{f2(x-4.5)}" y="{f2(y-19)}" width="9" height="6" rx="3" fill="#3a6fd6" stroke="#1f4f9e" stroke-width=".7"/><path d="M{f2(x+4)},{f2(y-19)} v-4 h3 v2 Z" fill="#e0402f"/>'
    b += bush(*I.P(.25, 1.6, 0), 9, seed=5, flowers='#ff8fc0') + bush(*I.P(2.85, 2.4, 0), 7, seed=8)
    return b

# ---------------------------------------------------------------- cat house
def cathouse(l):
    @lot
    def f(I):
        b = ''
        if l >= 2:  # cat tree tower at the back
            x, y = I.P(.45, .5, 0)
            b += ell(x, y, 9, 4, '#1d3a24', 'opacity=".14"') + f'<rect x="{f2(x-2.4)}" y="{f2(y-44)}" width="4.8" height="44" fill="#d9c29a" stroke="#a8855a" stroke-width=".6"/>'
            for k in range(0, 44, 3): b += seg((x - 2.4, y - k), (x + 2.4, y - k - 2), '#b8955f', .7)
            for z, s in ((16, 9), (30, 8), (44, 10)):
                b += ell(x, y - z, s, s * .45, '#8a5a8f', 'stroke="#5a3a60" stroke-width=".7"') + ell(x, y - z - 1.5, s * .8, s * .32, '#b07ab5')
            b += ell(x + 5, y - 30, 1.6, 6, '#ffd23a') + circ(x + 5, y - 23, 2, '#ff6fa0')
        b += shadow(I, .55, .85, 2.0, 2.25)
        b += I.box(.55, .85, 2.0, 2.25, 0, 22, '#f2a06a', '#ec8a54', '#cf6f3e', '#9a4a24', .9)
        for z in range(5, 22, 4): b += seg(I.P(.55, 2.25, z), I.P(2.0, 2.25, z), '#00000016', .6) + seg(I.P(2.0, .85, z), I.P(2.0, 2.25, z), '#00000016', .6)
        # arched door, round window, paw sign
        dx, dy = I.P(1.28, 2.25, 0)
        b += f'<path d="M{f2(dx-9)},{f2(dy-4.5)} v-10 a9,9 0 0 1 18,0 v10 Z" fill="#4a2a1e" stroke="#7a3f22" stroke-width="1.6" transform="skewY(26.57) translate(0 {f2(-dx*0.5)})"/>'
        x, y = I.P(1.85, 1.55, 14); b += f'<ellipse cx="{f2(x+2)}" cy="{f2(y)}" rx="3.6" ry="4.6" fill="url(#gWin)" stroke="#ffffff" stroke-width="1.4" transform="skewY(-26.57) translate(0 {f2((x+2)*0.5)})"/>'
        b += gable_v(I, .55, .85, 2.0, 2.25, 22, 17, 'url(#gRoofT)', '#25706b', '#f6b07a', '#1f5a56', o=.14, lines=4)
        # cat ears on the gable
        for du in (-.34, .34):
            x, y = I.P(1.275 + du, 2.39, 31)
            b += poly([(x - 4, y + 1), (x, y - 7), (x + 4, y + 1)], '#2a7a76', '#1f5a56', .8) + poly([(x - 2, y), (x, y - 4), (x + 2, y)], '#ff9ab5')
        x, y = I.P(1.275, 2.25, 25); b += circ(x, y, 3.6, '#ffffff', '#b9ad95', .6) + ''.join(circ(x + dx_, y + dy_, r_, '#e07a4a') for dx_, dy_, r_ in ((0, .9, 1.4), (-1.6, -.9, .7), (-.5, -1.8, .7), (.7, -1.8, .7), (1.7, -.8, .7)))
        if l >= 2:  # annex with a sun deck
            b += I.box(2.0, 1.25, 2.85, 2.25, 0, 14, '#f7c98e', '#f2b878', '#d99a5a', '#9a6a34', .8)
            b += I.box(1.96, 1.2, 2.9, 2.3, 14, 16, '#d9c29a', '#b8a07a', '#a88f6a', '#6a5232', .6)
            for u in (2.05, 2.8):
                for v in (1.25, 2.25): b += seg(I.P(u, v, 16), I.P(u, v, 22), '#ffffff', 1.2)
            b += seg(I.P(2.05, 2.25, 21), I.P(2.8, 2.25, 21), '#ffffff', 1.2) + seg(I.P(2.8, 1.25, 21), I.P(2.8, 2.25, 21), '#ffffff', 1.2)
            x, y = I.P(2.4, 1.75, 16); b += ell(x, y, 8, 3.6, '#7fb4f5', 'stroke="#3d74d6" stroke-width=".7"') + ell(x, y - 1, 6, 2.4, '#a8ccff')
            x, y = I.P(2.85, 1.75, 0); b += f'<path d="M{f2(x+1)},{f2(y-1)} v-8 a3.5,3.5 0 0 1 7,-3.5 v8 Z" fill="#4a2a1e" transform="skewY(-26.57) translate(0 {f2((x+1)*0.5)})"/>'
        if l >= 3:  # screened catio out front
            u0, v0, u1, v1, h = .25, 2.35, 1.35, 2.9, 18
            b += flat(I, u0, v0, u1, v1, 0, '#9fd07a', '#6aa04a', .6)
            b += circ(*I.P(.6, 2.6, 2), 3, '#ffd23a', '#c99a12', .5) + ell(*I.P(1.05, 2.55, 1), 6, 2.6, '#c77dff')
            b += fv(I, v1, u0, u1, 0, h, '#ffffff', 'none').replace('/>', ' opacity=".28"/>') + fu(I, u1, v0, v1, 0, h, '#ffffff', 'none').replace('/>', ' opacity=".22"/>')
            for u in (u0, u1):
                for v in (v0, v1): b += seg(I.P(u, v, 0), I.P(u, v, h), '#7a4a2b', 1.6)
            b += seg(I.P(u0, v1, h), I.P(u1, v1, h), '#7a4a2b', 1.6) + seg(I.P(u1, v0, h), I.P(u1, v1, h), '#7a4a2b', 1.6) + seg(I.P(u0, v0, h), I.P(u0, v1, h), '#7a4a2b', 1.2)
            for k in range(1, 6): b += seg(I.P(u0 + (u1 - u0) * k / 6, v1, 0), I.P(u0 + (u1 - u0) * k / 6, v1, h), '#ffffff', .5, 'opacity=".6"')
            b += seg(I.P(u0, v1, h / 2), I.P(u1, v1, h / 2), '#ffffff', .5, 'opacity=".6"')
        x, y = I.P(2.2, 2.6, 0); b += ell(x, y, 5, 2.2, '#d2553f') + ell(x + 9, y + 2, 5, 2.2, '#3f7fc4')
        b += bush(*I.P(.3, 2.0, 0), 6, seed=11) + bush(*I.P(2.9, 1.0, 0), 6, seed=12, flowers='#ffffff')
        return b
    return f

# ---------------------------------------------------------------- office
def office(l):
    @lot
    def f(I):
        u1 = 2.3 if l == 1 else 2.8
        b = shadow(I, .4, .6, u1, 2.4)
        if l == 2:
            x, y = I.P(.3, .45, 0); b += seg((x, y), (x, y - 70), '#7a5a3a', 2.4) + seg((x - 7, y - 64), (x + 7, y - 64), '#7a5a3a', 1.8)
            b += f'<path d="M{f2(x+7)},{f2(y-64)} q30,8 60,30" fill="none" stroke="#33413a" stroke-width=".8"/>'
        b += I.box(.4, .6, u1, 2.4, 0, 26, '#f4f6f6', '#eef2f3', '#cfd8dc', '#9aa8ae', .8)
        for z in range(5, 26, 4): b += seg(I.P(.4, 2.4, z), I.P(u1, 2.4, z), '#0000000f', .6) + seg(I.P(u1, .6, z), I.P(u1, 2.4, z), '#00000012', .6)
        b += I.box(.32, .52, u1 + .08, 2.48, 26, 30, '#6a7a80', '#5a6a70', '#4a585e', '#333d42', .7)
        b += flat(I, .4, .6, u1, 2.4, 30, '#8a969c')
        # door with an awning and a window
        b += fv(I, 2.4, .62, .98, 0, 17, '#3f6a8a', '#24405a', .8) + fv(I, 2.41, .68, .92, 9, 15, 'url(#gWin)') + circ(*I.P(.9, 2.42, 8), .9, '#ffd23a')
        b += poly([I.P(.52, 2.4, 20), I.P(1.08, 2.4, 20), I.P(1.08, 2.72, 16), I.P(.52, 2.72, 16)], '#2e7d4a', '#1f5a34', .7)
        for k in range(4): b += poly([I.P(.52 + k * .14, 2.72, 16), I.P(.59 + k * .14, 2.72, 16), I.P(.59 + k * .14, 2.72, 14), I.P(.52 + k * .14, 2.72, 14)], '#ffffff')
        b += win_u(I, u1, 1.0, 1.6, 9, 19)
        if l == 2: b += win_u(I, u1, 1.8, 2.25, 9, 19)
        # ribbon board on the front wall (ribbons are drawn live by the game)
        w1 = 2.2 if l == 1 else 2.65
        b += fv(I, 2.4, 1.32, w1 + .03, 5, 21, '#8a5a3a', '#5a3a22', .8) + fv(I, 2.405, 1.37, w1 - .02, 6, 20, '#d9b98a')
        x, y = I.P((1.32 + w1) / 2, 2.41, 23); b += f'<rect x="{f2(x-9)}" y="{f2(y-3)}" width="18" height="5" rx="1.5" fill="#c99a12" stroke="#8a6a12" stroke-width=".6" transform="skewY(26.57) translate(0 {f2(-x*.5)})"/>'
        # roof sign and extras
        sx, sy = I.P(1.0, 1.5, 30)
        b += seg((sx - 14, sy), (sx - 14, sy - 6), '#4a585e', 1.2) + seg((sx + 14, sy - 14), (sx + 14, sy - 20), '#4a585e', 1.2)
        b += poly([(sx - 17, sy - 6), (sx + 17, sy - 23), (sx + 17, sy - 13), (sx - 17, sy + 4)], '#173426', '#0f2419', .7)
        for k in range(5): b += circ(sx - 11 + k * 5.5, sy - 4 - k * 2.75, 1.3, '#f2c230')
        if l == 2:
            x, y = I.P(u1 - .35, .9, 30); b += ell(x, y - 9, 7, 7, '#e9eef2', 'stroke="#8a96a3" stroke-width=".8"') + seg((x, y - 9), (x + 3, y - 13), '#56606b', 1) + seg((x, y), (x, y - 5), '#56606b', 1.6)
            for u in (1.4, 2.1):
                x, y = I.P(u, 2.65, 0); b += poly([(x - 4, y - 6), (x + 4, y - 6), (x + 3, y), (x - 3, y)], '#3a3f3c', '#1f2321', .6) + bush(x, y - 6, 5, seed=int(u * 10))
        x, y = I.P(1.2, 2.7, 0); b += f'<rect x="{f2(x-3)}" y="{f2(y-8)}" width="6" height="8" rx="1" fill="#7a8a8e"/>' + ell(x, y - 8, 3, 1.2, '#9aa8ae')
        return b
    return f

# ---------------------------------------------------------------- debris
@lot
def deb_brush(I):
    b = flat(I, .1, .1, 2.9, 2.9, 0, '#9a8a4a', 'none').replace('/>', ' opacity=".35"/>')
    rr = random.Random(21); pts = [(rr.uniform(.25, 2.75), rr.uniform(.25, 2.75)) for _ in range(26)]
    for u, v in sorted(pts, key=lambda p: p[0] + p[1]):
        x, y = I.P(u, v, 0); h = rr.uniform(12, 24)
        b += ell(x, y + 1, 9, 3.4, '#1d3a24', 'opacity=".12"')
        for k in range(9):
            a = -1.57 + (k - 4) * .22 + rr.uniform(-.1, .1)
            c = ['#c9b25e', '#a88a4a', '#8a9a3a', '#d9c47a'][k % 4]
            b += f'<path d="M{f2(x)},{f2(y)} q{f2(math.cos(a)*h*.4)},{f2(-h*.6)} {f2(math.cos(a)*h)},{f2(math.sin(a)*h)}" fill="none" stroke="{c}" stroke-width="1.6" stroke-linecap="round"/>'
        if rr.random() < .45: b += bush(x, y, rr.uniform(6, 10), 'url(#gBrush)', '#6e5a2e', rr.randint(0, 99))
        if rr.random() < .3: b += f'<path d="M{f2(x-8)},{f2(y-3)} q6,-10 16,-4" fill="none" stroke="#5a3a22" stroke-width="1.6"/>'
    return b
@lot
def deb_rocks(I):
    b = flat(I, .1, .1, 2.9, 2.9, 0, '#8a8a70', 'none').replace('/>', ' opacity=".25"/>')
    rr = random.Random(5)
    for u, v, r in sorted([(.8, .8, 15), (1.9, .9, 11), (1.2, 1.9, 18), (2.3, 2.1, 10), (.5, 2.4, 7), (2.6, 1.4, 6), (1.6, .4, 6)], key=lambda p: p[0] + p[1]):
        x, y = I.P(u, v, 0)
        b += ell(x + 3, y + 2, r * 1.1, r * .4, '#1d3a24', 'opacity=".18"')
        b += f'<path d="M{f2(x-r)},{f2(y)} q-1,{f2(-r*.9)} {f2(r*.5)},{f2(-r*1.05)} q{f2(r*.9)},-3 {f2(r*1.35)},{f2(r*.55)} q2,{f2(r*.4)} -1,{f2(r*.5)} Z" fill="url(#gRock)" stroke="#5a6266" stroke-width=".9"/>'
        b += f'<path d="M{f2(x-r*.3)},{f2(y-r*.8)} l{f2(r*.2)},{f2(r*.35)} l{f2(r*.3)},-2" fill="none" stroke="#7a8488" stroke-width=".8"/>'
        if rr.random() < .6: b += ell(x - r * .2, y - r * .9, r * .35, r * .14, '#7fae5a', 'opacity=".85"')
    for k in range(14):
        x, y = I.P(rr.uniform(.2, 2.8), rr.uniform(.2, 2.8), 0); b += ell(x, y, rr.uniform(1.4, 3), rr.uniform(.9, 1.6), '#b9bfc2', 'stroke="#7a8488" stroke-width=".5"')
    for k in range(6):
        x, y = I.P(rr.uniform(.3, 2.7), rr.uniform(.3, 2.7), 0); b += cluster(x, y, 3, 'url(#gLeaf)', '#2f7a3f', k)
    return b
@lot
def deb_stump(I):
    b = flat(I, .1, .1, 2.9, 2.9, 0, '#7a6a3a', 'none').replace('/>', ' opacity=".3"/>')
    x, y = I.P(1.0, 1.0, 0)
    # fallen log behind
    lx, ly = I.P(1.6, .5, 4)
    b += f'<path d="M{f2(lx-30)},{f2(ly+8)} L{f2(lx+26)},{f2(ly-6)} a6,8 0 0 1 2,15 L{f2(lx-28)},{f2(ly+22)} Z" fill="#8a5a3a" stroke="#5a3a22" stroke-width=".9"/>'
    b += ell(lx + 27, ly + 1.5, 5, 7.5, '#d9b07a', 'stroke="#8a6038" stroke-width=".8"') + ell(lx + 27, ly + 1.5, 2.4, 3.6, 'none', 'stroke="#a87a48" stroke-width=".7"')
    for k in range(4): b += seg((lx - 26 + k * 13, ly + 12 - k * 3.2), (lx - 18 + k * 13, ly + 10 - k * 3.2), '#6a4228', .8)
    # the stump
    sx, sy = I.P(1.4, 1.6, 0)
    for a, l_ in ((2.5, 16), (3.3, 14), (.4, 15), (1.2, 12), (5.6, 10)):
        b += f'<path d="M{f2(sx)},{f2(sy-2)} q{f2(math.cos(a)*l_*.5)},{f2(math.sin(a)*l_*.2)} {f2(math.cos(a)*l_)},{f2(math.sin(a)*l_*.5+3)}" fill="none" stroke="#6a4228" stroke-width="4" stroke-linecap="round"/>'
    b += f'<path d="M{f2(sx-14)},{f2(sy)} V{f2(sy-16)} a14,7 0 0 1 28,0 V{f2(sy)} a14,7 0 0 1 -28,0 Z" fill="#8a5a3a" stroke="#5a3a22" stroke-width=".9"/>'
    for k in range(5): b += seg((sx - 11 + k * 5.5, sy - 14 + (k % 2)), (sx - 11 + k * 5.5, sy + 2 - abs(k - 2)), '#6a4228', .8)
    b += ell(sx, sy - 16, 14, 7, '#e0bd8a', 'stroke="#8a6038" stroke-width=".9"')
    for r in (10, 6.5, 3): b += ell(sx, sy - 16, r, r * .5, 'none', 'stroke="#b88a58" stroke-width=".7"')
    b += seg((sx - 2, sy - 16), (sx + 8, sy - 19), '#7a4a2b', .8)
    tx, ty = I.P(2.3, 2.2, 0); b += f'<path d="M{f2(tx-8)},{f2(ty)} V{f2(ty-9)} a8,4 0 0 1 16,0 V{f2(ty)} a8,4 0 0 1 -16,0 Z" fill="#8a5a3a" stroke="#5a3a22" stroke-width=".8"/>' + ell(tx, ty - 9, 8, 4, '#e0bd8a', 'stroke="#8a6038" stroke-width=".8"') + ell(tx, ty - 9, 4.5, 2.2, 'none', 'stroke="#b88a58" stroke-width=".6"')
    for dx in (-18, 16):
        x2, y2 = sx + dx, sy + 4; b += f'<rect x="{f2(x2-1)}" y="{f2(y2-5)}" width="2" height="5" fill="#f6eedc"/>' + ell(x2, y2 - 5, 4, 2.4, '#e0402f') + circ(x2 - 1.4, y2 - 6, .7, '#ffffff') + circ(x2 + 1.2, y2 - 5.4, .6, '#ffffff')
    rr = random.Random(9)
    for k in range(14):
        x2, y2 = I.P(rr.uniform(.2, 2.8), rr.uniform(.2, 2.8), 0); b += bush(x2, y2, rr.uniform(4, 7), 'url(#gBrush)' if k % 2 else 'url(#gLeaf)', '#5a6a2e', k)
    return b
@lot
def deb_junk(I):
    b = flat(I, .1, .1, 2.9, 2.9, 0, '#7a6a4a', 'none').replace('/>', ' opacity=".3"/>')
    # sheet metal leaning, crates, rusty barrel, tires, wheel
    b += poly([I.P(.3, .5, 0), I.P(1.3, .3, 0), I.P(1.25, .45, 22), I.P(.3, .65, 20)], '#9aa5ad', '#5d6870', .8)
    for k in range(5): b += seg(I.P(.4 + k * .2, .5 - k * .04, 1), I.P(.4 + k * .2, .62 - k * .04, 20), '#7f8c96', .9)
    b += I.box(1.6, .5, 2.2, 1.1, 0, 14, '#c9a06a', '#a8804a', '#94703e', '#5a3a22', .8) + I.box(1.7, .6, 2.15, 1.05, 14, 24, '#d9b07a', '#b8905a', '#a07a48', '#5a3a22', .8)
    for z in (5, 10): b += seg(I.P(1.6, 1.1, z), I.P(2.2, 1.1, z), '#5a3a22', .8) + seg(I.P(2.2, .5, z), I.P(2.2, 1.1, z), '#5a3a22', .8)
    x, y = I.P(.9, 1.5, 0)
    b += ell(x, y, 10, 4.5, '#6e3418') + f'<rect x="{f2(x-10)}" y="{f2(y-22)}" width="20" height="22" fill="url(#gRust)"/>' + ell(x, y - 22, 10, 4.5, '#a8552a', 'stroke="#6e3418" stroke-width=".8"')
    for z in (6, 15): b += f'<path d="M{f2(x-10)},{f2(y-z)} a10,4.5 0 0 0 20,0" fill="none" stroke="#6e3418" stroke-width="1.4"/>'
    b += ell(x - 2, y - 22, 5, 2, '#4a2a18')
    x, y = I.P(2.1, 2.0, 0)
    for k in range(3):
        b += ell(x, y - k * 5, 12, 5.5, '#2a2a2a', 'stroke="#111" stroke-width=".8"') + ell(x, y - k * 5 - 1, 6, 2.6, '#7a6a4a')
    b += ell(x, y - 10 - 3, 6, 2.6, '#4a3a28')
    x, y = I.P(1.0, 2.5, 0); b += ell(x, y - 5, 6, 7, 'none', 'stroke="#3a3a3a" stroke-width="2.4"') + circ(x, y - 5, 1.4, '#8a96a3')
    for k in range(4): b += seg((x, y - 5), (x + math.cos(k * .8) * 5.4, y - 5 + math.sin(k * .8) * 6.4), '#8a96a3', .8)
    x, y = I.P(2.35, .55, 0); b += I.box(2.0, 1.4, 2.8, 1.75, 0, 3, '#b8905a', '#9a7444', '#8a663a', '#5a3a22', .6)
    for k in range(4): b += I.box(2.02 + k * .2, 1.42, 2.14 + k * .2, 1.73, 3, 4.5, '#c9a06a', '#a8804a', '#94703e', '#5a3a22', .4)
    for u, v in ((2.6, .4), (.4, 2.0), (2.7, 2.7), (.3, .3), (1.6, 2.7), (2.8, 1.2)):
        x2, y2 = I.P(u, v, 0); b += bush(x2, y2, 5.5, 'url(#gBrush)', '#6e5a2e', int(u * 9 + v))
    return b

# ---------------------------------------------------------------- buildings
@lot
def b_garden(I):
    b = flat(I, .15, .15, 2.85, 2.85, 0, '#8fd06c', '#6aa04a', .6)
    b += stones(I, [(1.5, 2.8), (1.5, 2.45), (1.5, 2.1), (1.5, 1.75)], 2.8)
    beds = [(.25, .25, 1.25, 1.25, 'rose'), (1.75, .25, 2.75, 1.25, 'hydrangea'), (.25, 1.6, 1.25, 2.75, 'petunia'), (1.75, 1.6, 2.75, 2.75, 'mum')]
    for u0, v0, u1, v1, crop in beds:
        b += I.box(u0, v0, u1, v1, 0, 5, '#6a4129', '#b5654a', '#9a4e38', '#5a2a20', .7)
        for k in range(int((u1 - u0) / .2)): b += seg(I.P(u0 + k * .2, v1, 0), I.P(u0 + k * .2, v1, 5), '#00000022', .5)
        rr = random.Random(int(u0 * 10 + v0 * 3))
        for k in range(7):
            u, v = rr.uniform(u0 + .15, u1 - .15), rr.uniform(v0 + .15, v1 - .15)
            x, y = I.P(u, v, 5); b += flowers(x, y, crop, 4.6, 6, k)
    x, y = I.P(1.5, 1.4, 0)
    b += f'<path d="M{f2(x-3)},{f2(y)} h6 l-1,-14 h-4 Z" fill="#e6e0d4" stroke="#a8a090" stroke-width=".7"/>' + ell(x, y - 14, 9, 3.6, '#e6e0d4', 'stroke="#a8a090" stroke-width=".7"') + ell(x, y - 14.5, 7, 2.6, 'url(#gWater)')
    b += f'<path d="M{f2(x+3)},{f2(y-17)} q2,-3 4,0 l1.6,-1 l-.4,2 q-2,3 -5,1 Z" fill="#5a8fd6"/>'
    return b
@lot
def b_stand(I):
    b = shadow(I, .3, .8, 2.7, 2.1) + stones(I, [(1.4, 2.6), (2.0, 2.7)], 2.4)
    b += I.box(.4, 1.2, 2.6, 2.0, 0, 14, '#e0b07a', '#c98f55', '#b07a45', '#6a4228', .8)
    for u in (.75, 1.1, 1.45, 1.8, 2.15): b += seg(I.P(u, 2.0, 0), I.P(u, 2.0, 14), '#00000020', .7)
    b += I.box(.3, 1.1, 2.7, 2.1, 14, 16, '#a8804a', '#8a6a3a', '#7a5a30', '#4a3420', .7)
    for u in (.35, 2.6):
        for v in (1.15, 2.0): b += I.box(u, v, u + .08, v + .08, 16, 40, '#8a5a3a', '#7a4a2b', '#6a3e22', '#4a2a18', .5)
    stripes = ['#ffffff', '#e0402f']
    n = 8
    for k in range(n):
        u0, u1 = .2 + 2.6 * k / n, .2 + 2.6 * (k + 1) / n
        b += poly([I.P(u0, .95, 46), I.P(u1, .95, 46), I.P(u1, 2.35, 38), I.P(u0, 2.35, 38)], stripes[k % 2], '#00000022', .4)
    for k in range(n):
        u0, u1 = .2 + 2.6 * k / n, .2 + 2.6 * (k + 1) / n; x0, y0 = I.P(u0, 2.35, 38); x1, y1 = I.P(u1, 2.35, 38)
        b += f'<path d="M{f2(x0)},{f2(y0)} L{f2(x1)},{f2(y1)} q{f2((x0-x1)/2)},{f2(6+(y0-y1)/2)} {f2(x0-x1)},{f2(y0-y1)} Z" fill="{stripes[k % 2]}" stroke="#00000022" stroke-width=".4"/>'
    for k, (u, crop) in enumerate(((.6, 'mum'), (1.05, 'geranium'), (1.5, 'petunia'), (1.95, 'begonia'), (2.35, 'vinca'))):
        x, y = I.P(u, 1.6, 16); b += I.box(u - .16, 1.4, u + .16, 1.85, 16, 20, '#d9b07a', '#b8905a', '#a07a48', '#5a3a22', .5)
        b += flowers(x, y - 5, crop, 4.4, 6, k)
    for u, v in ((2.75, 2.45), (.25, 2.4)):
        x, y = I.P(u, v, 0); b += ell(x, y - 5, 7, 6, '#f08a2a', 'stroke="#b85a10" stroke-width=".8"') + f'<path d="M{f2(x-3)},{f2(y-10)} v-3 h2 Z" fill="#5a8a3a"/>' + seg((x - 3, y - 10), (x - 4, y - 1), '#d0701a', .7)
    x, y = I.P(1.1, 2.45, 0); b += poly([(x - 8, y), (x - 6, y - 18), (x + 6, y - 18), (x + 8, y)], '#2b3a33', '#5a3a22', 1.2)
    b += seg((x - 4, y - 13), (x + 4, y - 13), '#ffffff', .9) + seg((x - 3, y - 9), (x + 3, y - 9), '#ffd23a', .9) + seg((x - 4, y - 5), (x + 2, y - 5), '#ff8fc0', .9)
    return b
@lot
def b_shed(I):
    b = shadow(I, .55, .5, 2.4, 2.25)
    b += I.box(.55, .5, 2.4, 2.25, 0, 26, '#c0503f', '#b5453a', '#963a30', '#5a2a20', .9)
    for u in [.55 + k * .185 for k in range(11)]: b += seg(I.P(u, 2.25, 0), I.P(u, 2.25, 26), '#00000020', .6)
    for v in [.5 + k * .175 for k in range(11)]: b += seg(I.P(2.4, v, 0), I.P(2.4, v, 26), '#00000020', .6)
    b += fv(I, 2.25, .95, 1.95, 0, 20, '#f6f2ea', '#b9ad95', .6) + fv(I, 2.26, 1.0, 1.43, 1, 19, '#a83f32') + fv(I, 2.26, 1.47, 1.9, 1, 19, '#a83f32')
    for a, c in (((1.0, 1), (1.43, 19)), ((1.0, 19), (1.43, 1)), ((1.47, 1), (1.9, 19)), ((1.47, 19), (1.9, 1))):
        b += seg(I.P(a[0], 2.27, a[1]), I.P(c[0], 2.27, c[1]), '#f6f2ea', 1.6)
    b += win_u(I, 2.4, 1.05, 1.65, 12, 20)
    b += gable_v(I, .55, .5, 2.4, 2.25, 26, 18, 'url(#gRoofS)', '#4a5256', '#c0503f', '#333d42', o=.14, lines=5)
    x, y = I.P(1.47, 2.27, 34); b += circ(x, y, 3.2, '#f6f2ea', '#b9ad95', .7) + seg((x - 2, y + 1), (x + 2, y - 1), '#5a666c', 1)
    # tools leaning on the side and a wheelbarrow
    x, y = I.P(2.45, 2.0, 0); b += seg((x, y), (x + 3, y - 26), '#8a5a3a', 1.6) + f'<path d="M{f2(x+1)},{f2(y-25)} l8,-3 M{f2(x+2)},{f2(y-26)} l8,-1 M{f2(x+3)},{f2(y-27)} l7,1" stroke="#7f8c96" stroke-width=".9"/>'
    x, y = I.P(2.45, 1.75, 0); b += seg((x, y - 6), (x + 2, y - 28), '#8a5a3a', 1.6) + poly([(x - 2.5, y - 6), (x + 2.5, y - 5), (x + 1.5, y + 1), (x - 2, y)], '#b9c9d8', '#56606b', .6)
    x, y = I.P(.6, 2.65, 0); b += poly([(x - 10, y - 10), (x + 6, y - 14), (x + 4, y - 4), (x - 7, y - 2)], '#3f8fd6', '#24605a', .8) + circ(x + 8, y - 2, 3, '#2b2b2b') + seg((x - 10, y - 9), (x - 18, y - 4), '#8a5a3a', 1.4)
    b += bush(*I.P(.4, 1.0, 0), 6, seed=31)
    return b
@lot
def b_pergola(I):
    b = flat(I, .3, .3, 2.7, 2.7, 0, '#e3d6bd', '#c2b393', .7)
    for k in range(1, 6): b += seg(I.P(.3 + k * .4, .3, 0), I.P(.3 + k * .4, 2.7, 0), '#c9bc9c', .6) + seg(I.P(.3, .3 + k * .4, 0), I.P(2.7, .3 + k * .4, 0), '#c9bc9c', .6)
    for u, v in ((.4, .4), (2.5, .4), (.4, 2.5)): b += I.box(u, v, u + .12, v + .12, 0, 40, '#ffffff', '#f4f0e8', '#ddd6c6', '#b9ad95', .5)
    # bench and a little table
    b += I.box(.7, 1.2, 1.9, 1.5, 6, 9, '#a87a48', '#8a6038', '#7a5530', '#4a3420', .6)
    for u in (.75, 1.8): b += I.box(u, 1.25, u + .08, 1.45, 0, 6, '#7a5530', '#6a4a2a', '#5a3e22', '#3a2a18', .4)
    b += I.box(.7, 1.15, 1.9, 1.22, 9, 18, '#a87a48', '#8a6038', '#7a5530', '#4a3420', .5)
    x, y = I.P(1.8, 2.0, 0); b += f'<rect x="{f2(x-1.2)}" y="{f2(y-11)}" width="2.4" height="11" fill="#7a5530"/>' + ell(x, y - 11, 8, 3.4, '#d9b07a', 'stroke="#8a6038" stroke-width=".7"') + circ(x + 2, y - 14, 2.2, '#ffffff', '#b9ad95', .5)
    b += I.box(2.5, 2.5, 2.62, 2.62, 0, 40, '#ffffff', '#f4f0e8', '#ddd6c6', '#b9ad95', .5)
    for v in (.35, 2.55): b += I.box(.3, v, 2.72, v + .1, 40, 44, '#ffffff', '#f4f0e8', '#ddd6c6', '#b9ad95', .5)
    for k in range(7): u = .35 + k * .38; b += I.box(u, .3, u + .07, 2.72, 44, 47, '#ffffff', '#f4f0e8', '#ddd6c6', '#b9ad95', .4)
    rr = random.Random(4)
    for k in range(22):
        u, v = rr.uniform(.3, 2.7), rr.uniform(.3, 2.7); x, y = I.P(u, v, 47)
        b += circ(x, y, rr.uniform(3, 5), '#5aa64e' if k % 3 else '#7bbf5a', '#3a7a3a', .4)
        if k % 2: b += ell(x + 1, y + 5, 2, 4.5, '#b48fe0', 'stroke="#7a5ab0" stroke-width=".4"')
    for v, u in ((2.6, None),):
        pts = [I.P(.4 + k * .3, 2.6, 38 - (k % 2) * 3) for k in range(8)]
        b += f'<path d="M{" L".join(f"{f2(x)},{f2(y)}" for x, y in pts)}" fill="none" stroke="#33413a" stroke-width=".6"/>' + ''.join(circ(x, y + 1.5, 1.3, '#fff1a8') for x, y in pts)
    return b
@lot
def b_pond(I):
    b = flat(I, .1, .1, 2.9, 2.9, 0, '#8fd06c').replace('/>', ' opacity=".0"/>')
    cx_, cy_ = I.P(1.5, 1.5, 0)
    pts = []
    for k in range(18):
        a = k / 18 * 6.283; r = 1.05 + .12 * math.sin(a * 3) + .08 * math.cos(a * 5)
        pts.append(I.P(1.5 + math.cos(a) * r, 1.5 + math.sin(a) * r, 0))
    b += poly(pts, '#5a8a4a').replace('/>', ' transform="translate(0 3)"/>') + poly(pts, 'url(#gWater)', '#3a6a8a', 1)
    rr = random.Random(2)
    for (x, y) in pts:
        b += ell(x, y, rr.uniform(3.5, 5.5), rr.uniform(2.2, 3), 'url(#gRock)', 'stroke="#5a6266" stroke-width=".6"')
    b += ell(cx_ - 14, cy_ - 6, 16, 3.2, '#ffffff', 'opacity=".35"') + ell(cx_ + 10, cy_ + 8, 9, 1.8, '#ffffff', 'opacity=".25"')
    for dx, dy, fl in ((-20, 6, 1), (8, 10, 0), (22, -2, 1), (-4, -10, 0), (14, -12, 0)):
        b += f'<path d="M{f2(cx_+dx)},{f2(cy_+dy)} m-6,0 a6,3 0 1 0 6,-3 l0,3 Z" fill="#5aa652" stroke="#2f7a3f" stroke-width=".6"/>'
        if fl: b += circ(cx_ + dx - 1, cy_ + dy - 2, 2.6, '#ffb3d1', '#d0558f', .5) + circ(cx_ + dx - 1, cy_ + dy - 2.4, 1, '#ffe27a')
    for u, v in ((.45, 1.2), (.55, 1.0), (.4, 1.45), (2.5, 2.4)):
        x, y = I.P(u, v, 0); b += seg((x, y), (x - 1, y - 22), '#4a8a3a', 1.2) + ell(x - 1, y - 20, 1.6, 4.5, '#7a4a2b') + seg((x + 2, y), (x + 5, y - 14), '#5aa64e', 1)
    x, y = I.P(2.3, 2.75, 0); b += f'<rect x="{f2(x-10)}" y="{f2(y-8)}" width="20" height="3" rx="1" fill="#a87a48"/><rect x="{f2(x-9)}" y="{f2(y-5)}" width="2" height="5" fill="#6a4a2a"/><rect x="{f2(x+7)}" y="{f2(y-5)}" width="2" height="5" fill="#6a4a2a"/>'
    x, y = cx_ + 8, cy_ + 9; b += ell(x, y - 2, 3.6, 2.6, '#4fa83f', 'stroke="#2f6a2a" stroke-width=".6"') + circ(x - 2, y - 4, 1.2, '#ffffff') + circ(x + 2, y - 4, 1.2, '#ffffff') + circ(x - 2, y - 4, .5, '#111') + circ(x + 2, y - 4, .5, '#111')
    return b
@lot
def b_orchard(I):
    b = ''
    for u, v, s, sd in ((.75, .75, 1.0, 1), (2.25, .8, .95, 2), (.8, 2.2, .95, 3), (2.2, 2.2, 1.05, 4)):
        x, y = I.P(u, v, 0); b += ell(x, y, 16 * s, 6 * s, '#6fb04e', 'opacity=".55"') + tree(x, y, s * .85, fruit='url(#gPeach)', seed=sd)
    x, y = I.P(1.5, 1.6, 0)
    b += f'<path d="M{f2(x-6)},{f2(y)} L{f2(x-1)},{f2(y-34)} M{f2(x+4)},{f2(y+1)} L{f2(x+7)},{f2(y-32)}" stroke="#a87a48" stroke-width="1.8"/>'
    for k in range(5): b += seg((x - 5 + k * 1, y - 4 - k * 7), (x + 4.5 + k * .6, y - 3 - k * 7), '#a87a48', 1.2)
    x, y = I.P(1.6, 2.6, 0); b += f'<path d="M{f2(x-7)},{f2(y-8)} h14 l-2,8 h-10 Z" fill="#c99a5a" stroke="#8a6038" stroke-width=".8"/>' + ''.join(circ(x + dx, y - 9, 2.4, 'url(#gPeach)', '#a8401a', .4) for dx in (-4, 0, 4))
    return b
@lot
def b_beds(I):
    b = flat(I, .2, .2, 2.8, 2.8, 0, '#a07a50', 'none').replace('/>', ' opacity=".25"/>')
    rows = [(.3, 'sun'), (1.05, 'geranium'), (1.8, 'vinca'), (2.5, 'begonia')]
    for v0, crop in rows:
        b += I.box(.3, v0, 2.7, v0 + .45, 0, 6, '#6a4129', '#a8804a', '#94703e', '#5a3a22', .7)
        for k in range(8):
            u = .45 + k * .3; x, y = I.P(u, v0 + .22, 6)
            if crop == 'sun':
                b += seg((x, y), (x, y - 26), '#4a8a3a', 1.4) + ell(x - 3, y - 12, 3.5, 1.6, '#5aa64e') + ell(x + 3, y - 17, 3.5, 1.6, '#5aa64e')
                b += circ(x, y - 28, 5, '#ffd23a', '#e0a010', .7) + circ(x, y - 28, 2.2, '#6a4228')
            else:
                b += flowers(x, y, crop, 4.2, 5, k)
    return b
@lot
def b_frame(I):
    b = flat(I, .4, .5, 2.6, 2.4, 0, '#c9b38a', '#a8905a', .7)
    for u, v in ((.5, .6), (2.4, .6), (.5, 2.3), (2.4, 2.3), (1.45, .6), (1.45, 2.3)):
        b += I.box(u, v, u + .09, v + .09, 0, 30, '#e8c48a', '#d0a868', '#b8905a', '#8a6a3a', .5)
    b += I.box(.5, .6, 2.49, .69, 30, 33, '#e8c48a', '#d0a868', '#b8905a', '#8a6a3a', .5) + I.box(.5, 2.3, 2.49, 2.39, 30, 33, '#e8c48a', '#d0a868', '#b8905a', '#8a6a3a', .5)
    b += I.box(2.4, .6, 2.49, 2.39, 30, 33, '#e8c48a', '#d0a868', '#b8905a', '#8a6a3a', .5)
    b += seg(I.P(.55, 2.35, 2), I.P(1.45, 2.35, 28), '#d0a868', 2) + seg(I.P(2.45, .65, 2), I.P(2.45, 2.3, 28), '#d0a868', 2)
    x, y = I.P(1.2, 2.75, 0); b += I.box(.8, 2.6, 1.9, 2.85, 0, 6, '#e8c48a', '#d0a868', '#b8905a', '#8a6a3a', .5)
    x, y = I.P(2.6, 2.7, 0); b += f'<path d="M{f2(x-8)},{f2(y)} l3,-10 h10 l3,10 M{f2(x-5)},{f2(y-10)} h10" stroke="#8a6a3a" stroke-width="1.6" fill="none"/>'
    x, y = I.P(.35, 2.8, 0); b += seg((x, y), (x, y - 16), '#6a4a2a', 1.4) + poly([(x - 8, y - 24), (x + 8, y - 24), (x + 8, y - 15), (x - 8, y - 15)], '#ffd23a', '#8a6a12', .8) + seg((x - 5, y - 20), (x + 5, y - 20), '#2b2b2b', 1)
    return b

for _id, fn in (('h_farm', farmhouse), ('h_deb_brush', deb_brush), ('h_deb_rocks', deb_rocks), ('h_deb_stump', deb_stump), ('h_deb_junk', deb_junk),
                ('h_garden', b_garden), ('h_stand', b_stand), ('h_shed', b_shed), ('h_pergola', b_pergola), ('h_pond', b_pond), ('h_orchard', b_orchard),
                ('h_beds', b_beds), ('h_frame', b_frame)):
    add(_id, fn(), HW, HH, (HAX, HAY))
for _l in (1, 2, 3): add(f'h_cats_{_l}', cathouse(_l)(), HW, HH, (HAX, HAY))
for _l in (1, 2): add(f'h_office_{_l}', office(_l)(), HW, HH, (HAX, HAY))
# scenery
add('h_tree', tree(48, 112, 1.1, seed=41), 96, 128, (48, 112))
add('h_tree2', tree(48, 112, 1.25, 'url(#gTreeD)', seed=42), 96, 128, (48, 112))
add('h_pine', pine(48, 112, 1.2), 96, 128, (48, 112))
add('h_bush', bush(32, 50, 9, seed=43, flowers='#ffffff'), 64, 64, (32, 48))
