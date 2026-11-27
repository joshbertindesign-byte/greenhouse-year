# Decorations that mount on the greenhouse frame.
# Parts (dp_*) are drawn around their anchor at (0,0); the game places them on the wall, the doorway or the ledge.
# Icons (deco_*) show each piece on a bit of green greenhouse frame so the store says where it goes.

GRN, GRND, GLS = '#3f9a6c', '#246346', '#cfeef0'

def g(body, ax, ay): return f'<g transform="translate({ax} {ay})">{body}</g>'
def gs(body, ax, ay, s): return f'<g transform="translate({ax} {ay}) scale({s})">{body}</g>'
def line(a, b2, col, w=1, extra=''):
    return f'<path d="M{f2(a[0])},{f2(a[1])} L{f2(b2[0])},{f2(b2[1])}" stroke="{col}" stroke-width="{w}" stroke-linecap="round" fill="none" {extra}/>'
def qd(d, col, w, extra=''): return f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'

def jface(x, y, r):
    return (poly([(x - r * .55, y - r * .15), (x - r * .15, y - r * .15), (x - r * .35, y - r * .5)], '#ffe27a') +
            poly([(x + r * .15, y - r * .15), (x + r * .55, y - r * .15), (x + r * .35, y - r * .5)], '#ffe27a') +
            f'<path d="M{f2(x-r*.55)},{f2(y+r*.2)} q{f2(r*.55)},{f2(r*.45)} {f2(r*1.1)},0 l-{f2(r*.2)},{f2(r*.08)} l-{f2(r*.15)},-{f2(r*.12)} l-{f2(r*.2)},{f2(r*.12)} l-{f2(r*.2)},-{f2(r*.12)} l-{f2(r*.15)},{f2(r*.12)} Z" fill="#ffe27a"/>')
def pumpkin(x, y, r, face=True):
    b = ell(x, y, r * 1.12, r * .9, '#ff8a1a', 'stroke="#b8500f" stroke-width=".8"')
    b += ell(x, y, r * .45, r * .88, 'none', 'stroke="#d8681a" stroke-width=".7"')
    b += line((x, y - r * .85), (x + r * .2, y - r * 1.25), '#4f7a2a', max(1.2, r * .25))
    return b + (jface(x, y, r) if face else '')

# ---------------------------------------------------------------- standing parts (anchor = bottom centre)
def p_palm():
    b = ell(0, 0, 8, 2.6, '#1d3a24', 'opacity=".2"')
    b += poly([(-6.5, -11), (6.5, -11), (4.8, 0), (-4.8, 0)], 'url(#gPot)', '#a9512c', .7) + f'<rect x="-7.5" y="-13" width="15" height="3" rx="1" fill="#e07c4a" stroke="#a9512c" stroke-width=".6"/>'
    b += qd('M0,-13 q-1,-8 1,-16', '#8a6a3a', 2.4)
    for a, ln, c in ((-2.9, 17, '#2f7d3a'), (-.25, 17, '#2f7d3a'), (-2.5, 19, '#3f9a4a'), (-.65, 19, '#3f9a4a'), (-2.0, 17, '#4fb25a'), (-1.15, 17, '#4fb25a'), (-1.57, 13, '#5cc066')):
        ex, ey = math.cos(a) * ln, -29 + math.sin(a) * ln * .55 + (6 if a < -2.6 or a > -.4 else 0)
        mx, my = math.cos(a) * ln * .5, -29 + math.sin(a) * ln * .55 - 6
        b += f'<path d="M0,-29 Q{f2(mx)},{f2(my)} {f2(ex)},{f2(ey)}" fill="none" stroke="{c}" stroke-width="4.2" stroke-linecap="round"/>'
        b += f'<path d="M0,-29 Q{f2(mx)},{f2(my)} {f2(ex)},{f2(ey)}" fill="none" stroke="#9ae0a0" stroke-width=".7" stroke-linecap="round" opacity=".7"/>'
    return b

def p_tiki():
    b = ell(0, 0, 4, 1.4, '#1d3a24', 'opacity=".2"')
    b += f'<rect x="-1.6" y="-40" width="3.2" height="40" rx="1.2" fill="#c9a05a" stroke="#8a6a32" stroke-width=".6"/>'
    for yy in (-30, -20, -10): b += line((-1.6, yy), (1.6, yy), '#8a6a32', .8)
    b += f'<path d="M-4,-46 L4,-46 L2.6,-40 L-2.6,-40 Z" fill="#7a5232" stroke="#4a2f18" stroke-width=".6"/>'
    b += qd('M-4,-44 L4,-42 M-4,-42 L4,-44', '#c9a05a', .6)
    return b

def p_flamingo():
    b = ell(0, 0, 6, 1.8, '#1d3a24', 'opacity=".2"')
    b += line((-1, 0), (-1, -14), '#e86a8a', 1.1) + line((2, 0), (1.2, -14), '#e86a8a', 1.1)
    b += f'<path d="M-8,-19 Q-6,-24 1,-23 Q8,-22 7,-17 Q2,-13 -5,-15 Z" fill="#ff8ab0" stroke="#c84a70" stroke-width=".7"/>'
    b += f'<path d="M-4,-19 q4,-2 8,0" fill="none" stroke="#e8608a" stroke-width=".7"/>'
    b += f'<path d="M5,-20 Q10,-28 6,-33 Q3,-36 4,-31" fill="none" stroke="#ff8ab0" stroke-width="2.6" stroke-linecap="round"/>'
    b += circ(4.8, -34, 2.6, '#ff8ab0', '#c84a70', .5) + poly([(2.6, -34.5), (-1.5, -32), (2.8, -32.6)], '#2a2a2a') + circ(5.4, -34.6, .5, '#2a2a2a')
    return b

def p_scarecrow():
    b = ell(0, 0, 7, 2, '#1d3a24', 'opacity=".2"')
    b += f'<rect x="-1" y="-40" width="2" height="40" fill="#8a5a3a"/>' + line((-13, -27), (13, -27), '#8a5a3a', 2)
    b += f'<path d="M-8,-29 L8,-29 L7,-13 L-7,-13 Z" fill="#c0503f" stroke="#7a2a20" stroke-width=".7"/>'
    b += qd('M-8,-24 H8 M-8,-19 H8 M-3,-29 V-13 M3,-29 V-13', '#7a2a20', .6, 'opacity=".6"')
    b += f'<path d="M-13,-29 L-8,-29 L-8,-25 L-13,-25 Z" fill="#c0503f" stroke="#7a2a20" stroke-width=".5"/><path d="M13,-29 L8,-29 L8,-25 L13,-25 Z" fill="#c0503f" stroke="#7a2a20" stroke-width=".5"/>'
    for sx in (-14.5, 14.5):
        for d in (-1.5, 0, 1.5): b += line((sx, -27), (sx + (1.8 if sx > 0 else -1.8), -27 + d * 1.4), '#e8c45a', .8)
    b += line((-4, -13), (-5, -9), '#e8c45a', .8) + line((0, -13), (0, -8), '#e8c45a', .8) + line((4, -13), (5, -9), '#e8c45a', .8)
    b += circ(0, -33.5, 4.6, '#e9d3a0', '#a8905a', .6) + circ(-1.6, -34, .7, '#3a2a1a') + circ(1.6, -34, .7, '#3a2a1a') + qd('M-1.8,-31.6 q1.8,1.2 3.6,0', '#3a2a1a', .6)
    b += ell(0, -37.5, 9, 2.2, '#c9a24a', 'stroke="#8a6a22" stroke-width=".5"') + f'<path d="M-4.5,-37.5 L-3,-43 L3,-43 L4.5,-37.5 Z" fill="#d8b45a" stroke="#8a6a22" stroke-width=".5"/>'
    return b

def p_corn():
    b = ell(0, 0, 8, 2.2, '#1d3a24', 'opacity=".2"')
    for i in range(9):
        dx = -6 + i * 1.5; top = -36 + abs(i - 4) * 1.6
        b += f'<path d="M{f2(dx*.9)},0 Q{f2(dx*.25)},-16 {f2(dx*.35)},-18 Q{f2(dx*.6)},-26 {f2(dx*1.4)},{f2(top)}" fill="none" stroke="{["#c9a24a", "#d8b45a", "#b8903a"][i % 3]}" stroke-width="1.8" stroke-linecap="round"/>'
    for sd in (-1, 1): b += f'<path d="M{sd*2},-24 q{sd*6},-2 {sd*9},4" fill="none" stroke="#c9a24a" stroke-width="1.6"/>'
    b += f'<rect x="-3.6" y="-19.5" width="7.2" height="2.4" fill="#8a5a3a"/>'
    b += pumpkin(5, -3.2, 3.6, False)
    return b

def p_jstack():
    return ell(0, 0, 10, 2.6, '#1d3a24', 'opacity=".2"') + pumpkin(-4.6, -5, 5.2) + pumpkin(5, -4.4, 4.6) + pumpkin(0, -13, 5)

def p_pump(): return ell(0, 0, 5, 1.4, '#1d3a24', 'opacity=".25"') + pumpkin(0, -3.4, 3.6)

def p_gnome():
    b = ell(0, 0, 4.4, 1.3, '#1d3a24', 'opacity=".25"')
    b += ell(0, -4, 4, 4, '#3f6fc0', 'stroke="#1f3f80" stroke-width=".6"') + line((-2, -1), (-2, 0), '#4a2a18', 1.6) + line((2, -1), (2, 0), '#4a2a18', 1.6)
    b += circ(0, -8.6, 2.7, '#ffd8b8') + f'<path d="M-2.8,-8.2 q2.8,6.5 5.6,0 Z" fill="#ffffff" stroke="#c9c2b0" stroke-width=".3"/>' + circ(0, -8.8, .8, '#ff9a8a')
    b += f'<path d="M-3.4,-10 L3.4,-10 L1.2,-20 Z" fill="#e0303f" stroke="#8a0f1a" stroke-width=".6"/>'
    return b

def p_catfig():
    b = ell(0, 0, 4.6, 1.3, '#1d3a24', 'opacity=".25"')
    b += f'<rect x="-4.4" y="-3" width="8.8" height="3" fill="#d9d2c0" stroke="#8a8478" stroke-width=".5"/>'
    b += ell(0, -7.4, 3.6, 4.6, '#f4ecd8', 'stroke="#8a7a5a" stroke-width=".5"') + circ(0, -13, 3, '#f4ecd8', '#8a7a5a', .5)
    b += poly([(-2.8, -14.4), (-2.2, -17.8), (-.8, -15.4)], '#f4ecd8', '#8a7a5a', .4) + poly([(2.8, -14.4), (2.2, -17.8), (.8, -15.4)], '#f4ecd8', '#8a7a5a', .4)
    b += f'<path d="M3.4,-4.6 q3.6,-1 2,-6" fill="none" stroke="#f4ecd8" stroke-width="1.5" stroke-linecap="round"/>'
    b += circ(-1.1, -13.2, .45, '#3a3a3a') + circ(1.1, -13.2, .45, '#3a3a3a') + ell(0, -9.4, 1.4, .8, '#c9a24a')
    return b

# ---------------------------------------------------------------- hanging parts (anchor = hook at top)
def p_basket():
    b = line((0, 0), (-7.5, 14), '#5a5a5a', .5) + line((0, 0), (7.5, 14), '#5a5a5a', .5) + line((0, 0), (0, 15), '#5a5a5a', .5) + circ(0, 0, 1, 'none', '#5a5a5a', .6)
    for dx, ln in ((-6, 14), (-2, 18), (3, 16), (6.5, 12)): b += f'<path d="M{dx},19 q{1 if dx<0 else -1},{ln*.5} {-1 if dx<0 else 1},{ln}" fill="none" stroke="#3f8a3a" stroke-width="1.1"/>' + circ(dx + (-1 if dx < 0 else 1), 19 + ln, 1, '#5cb05a')
    b += f'<path d="M-8.5,14.5 Q-8,22.5 0,22.5 Q8,22.5 8.5,14.5 Z" fill="#8a5a30" stroke="#5a3a1a" stroke-width=".6"/>'
    b += qd('M-8,16.5 Q0,18.5 8,16.5 M-7.4,19 Q0,21 7.4,19', '#a87a48', .5)
    for x, y, c in ((-6, 13.4, '#ff6aa8'), (-2.4, 11.8, '#c86ae8'), (1.6, 12.2, '#ffffff'), (5.4, 13.2, '#ff6aa8'), (-4, 15, '#ffe27a'), (3.2, 15, '#c86ae8'), (0, 14.4, '#ff9ac8')):
        b += circ(x, y, 2, c, '#00000022', .3) + circ(x, y, .6, '#ffe27a' if c != '#ffe27a' else '#e0902a')
    for x, y in ((-7.6, 15), (7.2, 14.2), (-1, 10.6)): b += ell(x, y, 2.2, 1.1, '#4fa84a')
    return b

def p_lantern():
    b = line((0, 0), (0, 4), '#3a2a1a', .7)
    b += f'<rect x="-3.6" y="3.6" width="7.2" height="2.2" rx=".6" fill="#d8b02a" stroke="#8a6a12" stroke-width=".4"/>'
    b += ell(0, 12, 6.4, 7, '#e0202f', 'stroke="#8a0f1a" stroke-width=".7"')
    b += qd('M-2.6,5.6 Q-4.4,12 -2.6,18.4 M2.6,5.6 Q4.4,12 2.6,18.4 M0,5 V19', '#a8101f', .5) + ell(-2.4, 9.6, 1.4, 2.4, '#ff8a8a', 'opacity=".5"')
    b += f'<rect x="-3.6" y="18.2" width="7.2" height="2.2" rx=".6" fill="#d8b02a" stroke="#8a6a12" stroke-width=".4"/>'
    b += qd('M0,20.4 V22 M-1,22 L-1.4,27 M0,22 V27.4 M1,22 L1.4,27', '#e0202f', .7)
    return b

def p_chimes():
    b = circ(0, 1, 1, 'none', '#6a6a6a', .6) + line((0, 2), (0, 5), '#6a6a6a', .5)
    b += ell(0, 6, 6.6, 1.8, '#8a5a30', 'stroke="#5a3a1a" stroke-width=".5"')
    for i, (dx, ln) in enumerate(((-5, 14), (-2.5, 18), (0, 21), (2.5, 16), (5, 12))):
        b += line((dx, 6.6), (dx, 8.6), '#8a8478', .3) + f'<rect x="{f2(dx-.9)}" y="8.6" width="1.8" height="{ln}" rx=".8" fill="#d8e2ea" stroke="#7a8a9a" stroke-width=".35"/>'
    b += line((0, 6.6), (0, 26), '#8a8478', .3) + ell(0, 18, 2.4, .8, '#8a5a30') + f'<path d="M-2.4,27 L2.4,27 L1.4,33 L-1.4,33 Z" fill="#5a9ad8" stroke="#2a5a98" stroke-width=".4"/>'
    return b

# ---------------------------------------------------------------- mounted parts (anchor = bottom of bracket)
def p_birdhouse():
    b = f'<path d="M-7,0 L7,0 L5,2.4 L-5,2.4 Z" fill="#8a5a30" stroke="#5a3a1a" stroke-width=".5"/>'
    b += f'<rect x="-6" y="-13" width="12" height="13" fill="#ffd28a" stroke="#a8763a" stroke-width=".7"/>' + qd('M-6,-9 H6 M-6,-5 H6', '#e0b06a', .5)
    b += poly([(-8.4, -12), (0, -19.5), (8.4, -12)], '#c0503f', '#7a2a20', .7) + circ(0, -7.6, 2.1, '#4a2a18') + line((0, -3.6), (0, -1.6), '#7a5232', 1)
    b += circ(5.6, -14, 1.6, '#5a8ad0') + poly([(7, -14.1), (9, -13.7), (7, -13.3)], '#e0902a')
    return b

def p_radio():
    b = f'<path d="M-12,0 L12,0 L12,2.2 L-12,2.2 Z" fill="#c9965a" stroke="#7a5a30" stroke-width=".5"/>' + line((-9, 2.2), (-6, 7), '#7a5a30', 1.2) + line((9, 2.2), (6, 7), '#7a5a30', 1.2)
    b += f'<rect x="-10" y="-13" width="20" height="13" rx="3" fill="#2fa8a0" stroke="#1a6a64" stroke-width=".8"/>'
    b += circ(-4.4, -6.5, 4, '#f2e6c8', '#1a6a64', .6) + qd('M-7,-6.5 H-1.8 M-6.4,-8.4 H-2.4 M-6.4,-4.6 H-2.4', '#b8a888', .5)
    b += f'<rect x="1.4" y="-10.4" width="7" height="4.4" rx="1" fill="#f2e6c8"/>' + line((3, -8.2), (5, -8.2), '#c0503f', .8) + circ(5, -3.2, 1.4, '#f2e6c8') + line((7, -13), (11, -23), '#9aa5ad', .8)
    return b

# ---------------------------------------------------------------- flat parts, drawn in the plane of the wall
def p_neon():
    b = f'<rect x="-17" y="0" width="34" height="15" rx="3" fill="#1e1e28" stroke="#4a4a5a" stroke-width=".8"/>'
    b += f'<text x="0" y="11.2" font-family="Arial Black,Arial" font-weight="900" font-size="10" fill="none" stroke="#ff5ab0" stroke-width="2.4" stroke-opacity=".35" text-anchor="middle">OPEN</text>'
    b += f'<text x="0" y="11.2" font-family="Arial Black,Arial" font-weight="900" font-size="10" fill="#ffd0ec" stroke="#ff5ab0" stroke-width=".6" text-anchor="middle">OPEN</text>'
    return b

def p_banner():
    b = f'<path d="M-12,1 L12,1 L12,19 L0,24 L-12,19 Z" fill="#2a5fc0" stroke="#1a3f8a" stroke-width=".7"/>'
    b += qd('M-10.5,3 H10.5 M-10.5,17.6 L0,22 L10.5,17.6', '#ffd23a', .7)
    b += line((-14.5, 0), (14.5, 0), '#c99a12', 1.6) + circ(-14.6, 0, 1.3, '#ffd23a') + circ(14.6, 0, 1.3, '#ffd23a')
    b += poly([(-2.4, 12), (-4.6, 20.5), (-.6, 18.6)], '#d8303f') + poly([(2.4, 12), (4.6, 20.5), (.6, 18.6)], '#d8303f')
    for a in range(12):
        t = a * math.pi / 6; b += circ(math.cos(t) * 4.6, 10 + math.sin(t) * 4.6, 1.5, '#ffd23a', '#c99a12', .3)
    b += circ(0, 10, 3.8, '#ffe27a', '#c99a12', .5) + f'<text x="0" y="11.6" font-family="Arial" font-weight="700" font-size="4.2" fill="#8a6a12" text-anchor="middle">1st</text>'
    return b

def p_fountain():
    b = f'<path d="M-9,-6 L-9,-24 Q-9,-31 0,-31 Q9,-31 9,-24 L9,-6 Z" fill="#d9d2c0" stroke="#8a8478" stroke-width=".7"/>'
    b += f'<path d="M-6.4,-8 L-6.4,-23 Q-6.4,-28 0,-28 Q6.4,-28 6.4,-23 L6.4,-8 Z" fill="#c9c2b0"/>'
    b += circ(0, -21, 3.4, '#b8b0a0', '#8a8478', .6) + circ(-1.2, -21.8, .6, '#5a5448') + circ(1.2, -21.8, .6, '#5a5448') + ell(0, -19.6, 1.4, .8, '#5a5448')
    b += f'<rect x="-.9" y="-18.6" width="1.8" height="11" fill="#7ab8e0" opacity=".8"/>'
    b += f'<path d="M-11.5,-8 L11.5,-8 Q11,0 0,0 Q-11,0 -11.5,-8 Z" fill="#e4dccb" stroke="#8a8478" stroke-width=".7"/>' + ell(0, -7.8, 10, 1.6, '#7ab8e0')
    for x in (-6, 6): b += circ(x, -26, 1.4, '#6abf5a') + circ(x + (1.4 if x > 0 else -1.4), -24.6, 1.1, '#4fa84a')
    return b

def p_fanbox():
    b = f'<rect x="-14" y="-14" width="28" height="28" rx="1.5" fill="#d8dee3" stroke="#7a8794" stroke-width=".8"/>'
    b += circ(0, 0, 12, '#3a4248', '#7a8794', .8) + circ(0, 0, 10.4, '#2a3036')
    for cx_, cy_ in ((-12, -12), (12, -12), (-12, 12), (12, 12)): b += circ(cx_, cy_, .9, '#8a96a3')
    return b
def p_fangrille():
    b = circ(0, 0, 11.4, 'none', '#aab4bd', .7) + circ(0, 0, 8, 'none', '#aab4bd', .5) + circ(0, 0, 4.6, 'none', '#aab4bd', .5)
    b += line((-11.4, 0), (11.4, 0), '#aab4bd', .5) + line((0, -11.4), (0, 11.4), '#aab4bd', .5) + circ(0, 0, 2, '#c8d0d8', '#7a8794', .5)
    return b

def p_bench():
    I = Iso(0, 0); b = ''
    B = lambda u0, v0, u1, v1, z0, z1, c: I.box(u0, v0, u1, v1, z0, z1, c[0], c[1], c[2], '#5a3a1a', .6)
    wood = ('#d8a868', '#b8834a', '#9a6a38')
    b += poly([I.P(.04, -.8), I.P(.5, -.8), I.P(.5, .8), I.P(.04, .8)], '#1d3a24', 'none', 0, 'opacity=".16"')
    for v in (-.72, .62):
        b += I.box(.38, v, .46, v + .1, 0, 9, '#4a4a4a', '#3a3a3a', '#2a2a2a', 'none', 0) + I.box(.08, v, .16, v + .1, 0, 20, '#4a4a4a', '#3a3a3a', '#2a2a2a', 'none', 0)
    b += B(.08, -.78, .5, .78, 9, 11.5, wood)
    for z in (13, 16.5): b += B(.06, -.76, .14, .76, z, z + 2.6, wood)
    for v in (-.8, .7): b += I.box(.08, v, .46, v + .1, 15, 16.4, '#4a4a4a', '#3a3a3a', '#2a2a2a', 'none', 0)
    return b

PARTS = {'palm': (p_palm, 30, 50, 15, 46), 'tiki': (p_tiki, 12, 50, 6, 48), 'flamingo': (p_flamingo, 22, 40, 10, 38),
         'scarecrow': (p_scarecrow, 34, 48, 17, 46), 'corn': (p_corn, 22, 42, 10, 40), 'jstack': (p_jstack, 24, 22, 12, 20),
         'pump': (p_pump, 12, 10, 6, 9), 'gnome': (p_gnome, 10, 22, 5, 21), 'catfig': (p_catfig, 14, 20, 6, 19),
         'basket': (p_basket, 22, 38, 11, 2), 'lantern': (p_lantern, 14, 30, 7, 1), 'chimes': (p_chimes, 16, 36, 8, 1),
         'birdhouse': (p_birdhouse, 22, 28, 11, 24), 'radio': (p_radio, 28, 34, 14, 26),
         'neon': (p_neon, 38, 18, 19, 1), 'banner': (p_banner, 34, 26, 17, 1), 'fountain': (p_fountain, 26, 34, 13, 32),
         'fanbox': (p_fanbox, 32, 32, 16, 16), 'fangrille': (p_fangrille, 26, 26, 13, 13), 'bench': (p_bench, 70, 58, 26, 34)}
for _k, (_f, _w, _h, _ax, _ay) in PARTS.items():
    add(f'dp_{_k}', g(_f(), _ax, _ay), _w, _h, (_ax, _ay))

# ---------------------------------------------------------------- icons: the piece on a bit of greenhouse frame
def post(x, y0, y1): return f'<rect x="{f2(x-1.6)}" y="{y0}" width="3.2" height="{y1-y0}" fill="{GRN}" stroke="{GRND}" stroke-width=".6"/>'
def rail(x0, x1, y): return f'<rect x="{x0}" y="{f2(y-1.4)}" width="{x1-x0}" height="2.8" fill="{GRN}" stroke="{GRND}" stroke-width=".5"/>'
def frame(kind):
    b = f'<rect x="10" y="9" width="44" height="40" fill="{GLS}" opacity=".75"/>' + f'<rect x="10" y="41" width="44" height="8" fill="#f6f1e6" stroke="#d3c9b4" stroke-width=".6"/>'
    b += f'<path d="M16,13 l6,0 l-8,24 l-6,0 Z" fill="#ffffff" opacity=".4"/>'
    if kind == 'door':
        b += f'<rect x="24" y="15" width="16" height="34" fill="#efe7d4"/>' + post(24, 9, 49) + post(40, 9, 49)
    else:
        b += post(11, 9, 49) + post(53, 9, 49) + rail(11, 53, 27)
    return b + rail(10, 54, 10)
def swag(x0, x1, y, sag, col='#3a3a3a', w=.7): return qd(f'M{x0},{y} Q{(x0+x1)/2},{y+sag*2} {x1},{y}', col, w)
def sag_at(x0, x1, y, sag, t): return x0 + (x1 - x0) * t, y + sag * 4 * t * (1 - t)

def icon(k):
    if k in ('lights', 'bunting', 'papel', 'lantern', 'egg', 'swing'):
        b = frame('rail'); x0, x1, y, s = 11, 53, 12, 8
        if k == 'swing':
            for x in (21, 43): b += g(gs(p_basket(), 0, 0, 1.15), x, 11)
            return b
        b += swag(x0, x1, y, s, '#3a3a3a' if k != 'lantern' else '#5a2a1a')
        n = {'lights': 11, 'bunting': 9, 'papel': 7, 'lantern': 3, 'egg': 9}[k]
        for i in range(n):
            t = (i + .5) / n; x, yy = sag_at(x0, x1, y, s, t)
            if k == 'lights': b += circ(x, yy + 2.6, 4, ['#ff5a5a', '#ffe27a', '#7ad8ff', '#9aff7a'][i % 4], extra='opacity=".25"') + ell(x, yy + 2.4, 1.6, 2.2, ['#ff5a5a', '#ffd23a', '#5ac8ff', '#6ae05a'][i % 4], 'stroke="#00000033" stroke-width=".3"')
            elif k == 'bunting': b += poly([(x - 2.2, yy), (x + 2.2, yy + .3), (x, yy + 6)], ['#e0303f', '#ffffff', '#2a5fc0'][i % 3], '#00000044', .3)
            elif k == 'papel':
                c = ['#ff4fa0', '#ffb21a', '#3fc8a0', '#9a5ad8', '#ff5a3a', '#5ac8ff', '#ffe27a'][i]
                b += poly([(x - 2.6, yy), (x + 2.6, yy + .2), (x + 2.6, yy + 9), (x + 1.3, yy + 8), (x, yy + 9.2), (x - 1.3, yy + 8), (x - 2.6, yy + 9)], c, '#00000022', .3) + circ(x, yy + 4, .9, '#ffffff', extra='opacity=".85"') + circ(x - 1.2, yy + 2, .4, '#ffffff') + circ(x + 1.2, yy + 2, .4, '#ffffff')
            elif k == 'lantern': b += g(gs(p_lantern(), 0, 0, 1.05), x, yy)
            elif k == 'egg': b += ell(x, yy + 3.6, 2.2, 3, ['#ff9ac8', '#9ad8ff', '#ffe27a', '#b8f0a0', '#d0a8ff'][i % 5], 'stroke="#00000033" stroke-width=".3"') + qd(f'M{f2(x-2)},{f2(yy+3.6)} h4', '#ffffff', .6)
        return b
    if k in ('heart', 'palm', 'tiki', 'scarecrow', 'flamingo', 'jack'):
        b = frame('door')
        if k == 'heart':
            b += qd('M21,49 V26 A11,11 0 0 1 43,26 V49', '#f4efe4', 3.2) + qd('M21,49 V26 A11,11 0 0 1 43,26 V49', '#c9a26a', .5)
            for i in range(13):
                t = i / 12; a = math.pi * (1 - t)
                if t < .25: px, py = 21, 49 - (23 * t / .25)
                elif t > .75: px, py = 43, 26 + 23 * (t - .75) / .25
                else: a = math.pi * (1 - (t - .25) / .5); px, py = 32 + 11 * math.cos(a), 26 - 11 * math.sin(a)
                b += heart(px, py, 2.1, '#ff5a7a', '#a8123a') if i % 2 else circ(px, py, 1.8, '#ff8ab0', '#c84a70', .4) + ell(px + 1.6, py + 1, 1.3, .7, '#4fa84a')
            b += heart(32, 13, 3.8, '#ff2f5a', '#8a0f2a')
        elif k == 'palm': b += g(gs(p_palm(), 0, 0, .85), 16, 50) + g(gs(p_palm(), 0, 0, .85), 48, 50)
        elif k == 'tiki': b += g(p_tiki(), 17, 50) + g(p_tiki(), 47, 50) + ''.join(f'<path d="M{x},-0 q-3.4,-4.6 -1,-9 q1,3 2,1.6 q2.6,3.2 -1,7.4 Z" transform="translate(0 4)" fill="#ffb21a" stroke="#e0602a" stroke-width=".5"/>' for x in ())
        elif k == 'scarecrow': b += g(gs(p_corn(), 0, 0, .9), 15, 50) + g(gs(p_scarecrow(), 0, 0, .85), 48, 50)
        elif k == 'flamingo': b += g(p_flamingo(), 16, 50) + g(f'<g transform="scale(-1 1)">{p_flamingo()}</g>', 48, 50)
        elif k == 'jack': b += g(p_jstack(), 16, 50) + g(p_jstack(), 48, 50)
        if k == 'tiki':
            for x in (17, 47): b += f'<path d="M{x},1.5 q-3.4,4 -1.2,8 q1.4,1.6 2.4,0 q2.4,-4 -1.2,-8 Z" transform="translate(0 0)" fill="#ffb21a" stroke="#e0602a" stroke-width=".5"/>'
        return b
    if k in ('fan', 'radio', 'chimes', 'birdhouse', 'bath', 'neon', 'ribbon'):
        b = frame('wall')
        if k == 'fan': b += g(p_fanbox(), 32, 29) + ''.join(ell(32 + math.cos(a) * 5, 29 + math.sin(a) * 5, 5, 2.4, '#8a96a3', f'transform="rotate({f2(math.degrees(a))} {f2(32+math.cos(a)*5)} {f2(29+math.sin(a)*5)})"') for a in (0, 2.09, 4.19)) + g(p_fangrille(), 32, 29)
        elif k == 'radio': b += g(gs(p_radio(), 0, 0, 1.1), 32, 34) + qd('M44,18 q2,-3 4,0 M46,13 q2,-3 4,0', '#2a5fc0', .8)
        elif k == 'chimes': b += line((32, 10), (32, 11), GRND, 1) + g(gs(p_chimes(), 0, 0, 1.1), 32, 11)
        elif k == 'birdhouse': b += g(gs(p_birdhouse(), 0, 0, 1.25), 32, 29)
        elif k == 'bath': b += g(gs(p_fountain(), 0, 0, 1.05), 32, 42)
        elif k == 'neon': b += line((24, 11), (24, 18), '#5a5a5a', .6) + line((40, 11), (40, 18), '#5a5a5a', .6) + g(gs(p_neon(), 0, 0, 1.05), 32, 18)
        elif k == 'ribbon': b += g(gs(p_banner(), 0, 0, 1.2), 32, 12)
        return b
    # ledge pieces
    b = frame('ledge')
    if k == 'gnome': b += g(p_gnome(), 18, 41) + g(gs(p_gnome(), 0, 0, 1.15), 32, 41) + g(p_gnome(), 46, 41)
    elif k == 'catstatue': b += g(p_catfig(), 20, 41) + g(f'<g transform="scale(-1 1)">{p_catfig()}</g>', 44, 41)
    elif k == 'bench': b = frame('ledge') + g(gs(p_bench(), 0, 0, .62), 28, 44)
    return b

for _k in ('heart', 'egg', 'swing', 'bunting', 'jack', 'lights', 'lantern', 'papel', 'ribbon', 'birdhouse', 'bench', 'gnome', 'flamingo', 'chimes', 'bath', 'palm', 'neon', 'catstatue', 'scarecrow', 'tiki', 'fan', 'radio'):
    add(f'deco_{_k}', icon(_k))

# ---------------------------------------------------------------- seasonal cat hats (anchor = top of the cat's head)
def flower(x, y, r, c, mid='#ffe27a'):
    return ''.join(circ(x + math.cos(a) * r * .7, y + math.sin(a) * r * .7, r * .55, c) for a in (0, 1.26, 2.51, 3.77, 5.03)) + circ(x, y, r * .45, mid)
def hat(k):
    if k == 'christmas':
        b = f'<path d="M-5.4,0 Q-4,-9 3,-10.5 Q8,-11 8.6,-5.6 Q6,-8 3.6,-6.6 Q4.6,-3 5.4,0 Z" fill="#d8202f" stroke="#8a0f1a" stroke-width=".6"/>'
        b += f'<rect x="-6.6" y="-1.6" width="13.2" height="3.4" rx="1.7" fill="#ffffff" stroke="#c9c2b0" stroke-width=".4"/>' + circ(8.6, -5.2, 2.2, '#ffffff', '#c9c2b0', .4)
    elif k == 'halloween':
        b = ell(0, 0, 9.4, 2.4, '#3a2a4a', 'stroke="#1a1028" stroke-width=".6"')
        b += f'<path d="M-4.4,-.6 L4.4,-.6 Q3,-7 1.6,-10 Q3,-14 6.6,-14.6 Q2.4,-15 -.6,-11 Q-3,-6 -4.4,-.6 Z" fill="#4a3460" stroke="#1a1028" stroke-width=".6"/>'
        b += f'<path d="M-4.1,-2.4 L4.1,-2.4 L3.8,-.8 L-4.4,-.8 Z" fill="#ff8a1a"/>' + f'<rect x="-1" y="-2.6" width="2" height="2" fill="#ffd23a" stroke="#c99a12" stroke-width=".3"/>'
    elif k == 'easter':
        b = qd('M-6,1 Q0,-3.4 6,1', '#ff9ac8', 1.4)
        for sx, tx in ((-1, -5), (1, 5.4)):
            b += f'<path d="M{sx*2.6},-1.2 Q{tx-2.2*sx},-8 {tx},-14 Q{tx+2.2*sx},-8 {sx*5.2},-.4 Z" fill="#ffffff" stroke="#c9c2b0" stroke-width=".5"/>'
            b += f'<path d="M{sx*3.2},-2 Q{tx-1*sx},-8 {tx},-12 Q{tx+1.1*sx},-7.6 {sx*4.6},-1.6 Z" fill="#ffb3c8"/>'
    elif k == 'mother':
        b = qd('M-6.4,.6 Q0,-2.8 6.4,.6', '#4fa84a', 1.2)
        for i, (x, y, c) in enumerate(((-5.6, .2, '#ff8ab0'), (-2.8, -1.4, '#ffffff'), (0, -1.9, '#c86ae8'), (2.8, -1.4, '#ff8ab0'), (5.6, .2, '#ffffff'))):
            b += ell(x + (1.4 if i % 2 else -1.4), y + .6, 1.4, .7, '#5cb05a') + flower(x, y, 1.9, c)
    elif k == 'dia':
        b = qd('M-6.4,.6 Q0,-2.8 6.4,.6', '#3f8a3a', 1.2)
        for x, y, c in ((-5.4, -.2, '#ff8a1a'), (-1.9, -1.8, '#ffb21a'), (1.9, -1.8, '#ff8a1a'), (5.4, -.2, '#ffb21a')):
            b += ''.join(circ(x + math.cos(a) * 1.4, y + math.sin(a) * 1.4, 1.3, c, '#c8601a', .25) for a in range(0, 7)) + circ(x, y, 1.2, '#e0602a')
    elif k == 'july':
        b = ell(0, 0, 6.6, 1.8, '#1f3a8a', 'stroke="#10204a" stroke-width=".5"')
        b += f'<path d="M-4,-.4 L-4.4,-10 L4.4,-10 L4,-.4 Z" fill="#ffffff" stroke="#10204a" stroke-width=".5"/>'
        for x in (-2.6, 0, 2.6): b += f'<rect x="{f2(x-.6)}" y="-10" width="1.2" height="7" fill="#d8202f"/>'
        b += f'<path d="M-4.2,-3.4 L4.2,-3.4 L4,-.5 L-4,-.5 Z" fill="#1f3a8a"/>' + ell(0, -10, 4.4, 1.2, '#2a4fb0', 'stroke="#10204a" stroke-width=".5"')
        for x in (-2.2, 0, 2.2): b += circ(x, -1.9, .55, '#ffffff')
    elif k == 'fair':
        b = f'<path d="M-10,-1.6 Q-8,1.6 0,1.4 Q8,1.6 10,-1.6 Q7,0 0,-.2 Q-7,0 -10,-1.6 Z" fill="#c9965a" stroke="#7a5a30" stroke-width=".6"/>'
        b += f'<path d="M-4.8,-.4 Q-5.4,-6 -3,-7.6 Q0,-6 3,-7.6 Q5.4,-6 4.8,-.4 Z" fill="#d8a868" stroke="#7a5a30" stroke-width=".6"/>' + qd('M-4.6,-2 Q0,-1 4.6,-2', '#7a3a1a', 1.1)
    elif k == 'arbor':
        b = f'<path d="M-5.6,.4 Q-5.6,-6.4 0,-6.6 Q5.6,-6.4 5.6,.4 Q0,1.8 -5.6,.4 Z" fill="#a8763a" stroke="#6a4a22" stroke-width=".6"/>'
        b += qd('M-4.4,-1.4 L-1.4,-5.6 M-1.4,-.6 L2,-5.8 M1.6,-.4 L4.6,-3.8 M-4.6,-3.4 L1.4,-.6 M-2,-6 L4.6,-1.6', '#8a5a2a', .4) + qd('M0,-6.6 q.6,-2.4 2.2,-2.8', '#6a4a22', 1.1)
        b += ell(-4.4, -6.4, 2.4, 1.1, '#5cb05a', 'transform="rotate(-25 -4.4 -6.4)"')
    elif k == 'valentine':
        b = qd('M-6,1 Q0,-3.4 6,1', '#d8202f', 1.3)
        for sx in (-1, 1):
            b += qd(f'M{sx*2.6},-1.6 q{sx*-1},-2 0,-3.4 q{sx*1},-1.4 {sx*.4},-3.4 q{sx*-.6},-1.2 {sx*.8},-2.6', '#8a8a8a', .5) + heart(sx * 3.6, -11.6, 2.4, '#ff2f5a', '#8a0f2a')
    elif k == 'lunar':
        b = f'<path d="M-5.4,.6 Q-5.6,-6.6 0,-6.8 Q5.6,-6.6 5.4,.6 Z" fill="#d8202f" stroke="#7a0f1a" stroke-width=".6"/>'
        b += f'<path d="M-5.5,-1.4 Q0,-.2 5.5,-1.4 L5.4,.6 Q0,1.6 -5.4,.6 Z" fill="#d8b02a" stroke="#8a6a12" stroke-width=".4"/>' + qd('M0,-6.8 V-1', '#a8101f', .5) + circ(0, -8, 1.6, '#d8202f', '#7a0f1a', .5) + circ(0, -2.8, 1, '#ffd23a')
    elif k == 'tour':
        b = ell(0, 0, 9, 2.4, '#e8c878', 'stroke="#a8863a" stroke-width=".6"')
        b += f'<path d="M-5,-.4 L-5,-4.4 Q0,-5.6 5,-4.4 L5,-.4 Z" fill="#f2d68a" stroke="#a8863a" stroke-width=".6"/>' + ell(0, -4.6, 5, 1.3, '#f8e2a0', 'stroke="#a8863a" stroke-width=".5"')
        b += f'<path d="M-5,-2.4 Q0,-1.4 5,-2.4 L5,-.8 Q0,.2 -5,-.8 Z" fill="#2a3a5a"/>' + flower(4.2, -2, 1.7, '#ff8ab0')
    return b
for _k in ('valentine', 'lunar', 'easter', 'mother', 'arbor', 'july', 'fair', 'halloween', 'dia', 'christmas', 'tour'):
    add(f'hat_{_k}', g(hat(_k), 14, 18), 28, 24, (14, 18))

# ---------------------------------------------------------------- Robo-Cat (64x64, same frame as the cats)
lin('gSteel', [(0, '#eef3f7', None), (.55, '#c3ccd4', None), (1, '#8d99a5', None)])
def robocat(pose):
    o, sw, st = '#3e4852', .9, 'url(#gSteel)'
    b = ell(32, 53, 11, 2.8, '#1d3a24', 'opacity=".18"')
    def head(x, y, blink=False, lit=True):
        h = poly([(x - 5.8, y - 1.6), (x - 5, y - 9), (x - 1.2, y - 4.6)], st, o, sw) + poly([(x + 5.8, y - 1.6), (x + 5, y - 9), (x + 1.2, y - 4.6)], st, o, sw)
        h += poly([(x - 4.6, y - 3), (x - 4.3, y - 7.2), (x - 2.4, y - 4.6)], '#5a6670') + poly([(x + 4.6, y - 3), (x + 4.3, y - 7.2), (x + 2.4, y - 4.6)], '#5a6670')
        h += f'<rect x="{f2(x-6.6)}" y="{f2(y-5.4)}" width="13.2" height="11" rx="4.2" fill="{st}" stroke="{o}" stroke-width="{sw}"/>'
        h += line((x + .4, y - 5.4), (x + .4, y - 10.6), o, .8) + circ(x + .4, y - 11.4, 1.5, '#ff4a4a' if lit else '#7a2a2a', o, .5)
        h += f'<rect x="{f2(x-5)}" y="{f2(y-2)}" width="10.6" height="4.2" rx="2" fill="#1c2630"/>'
        if blink: h += line((x - 3.6, y), (x - 1, y), '#3ff0ff', .9) + line((x + 1.6, y), (x + 4.2, y), '#3ff0ff', .9)
        else: h += ell(x - 2.2, y, 1.4, 1.1, '#3ff0ff') + ell(x + 2.9, y, 1.4, 1.1, '#3ff0ff') + circ(x - 2.6, y - .4, .4, '#ffffff') + circ(x + 2.5, y - .4, .4, '#ffffff')
        h += f'<rect x="{f2(x-1.4)}" y="{f2(y+3)}" width="3.6" height="1.2" rx=".6" fill="#7a8794"/>' + circ(x - 5.2, y + 3.2, .5, '#5a6670') + circ(x + 5.8, y + 3.2, .5, '#5a6670')
        for sx in (-1, 1): h += line((x + sx * 6.6, y + 1.6), (x + sx * 9, y + 1), '#7a8794', .5) + line((x + sx * 6.6, y + 2.6), (x + sx * 9, y + 3), '#7a8794', .5)
        return h
    def tail(d):
        return f'<path d="{d}" fill="none" stroke="{o}" stroke-width="3.6" stroke-linecap="round"/><path d="{d}" fill="none" stroke="#c3ccd4" stroke-width="2.2" stroke-linecap="round" stroke-dasharray="2.2 .8"/>'
    if pose in ('walk0', 'walk1'):
        f = 1 if pose == 'walk1' else -1
        b += tail('M21,43 q-8,-2 -6,-12') + circ(15, 30.4, 1.8, '#3ff0ff', o, .5)
        for lx, ph in ((24, f), (28, -f), (36, -f), (40, f)):
            b += f'<rect x="{lx-1.6+ph*.9}" y="44" width="3.4" height="8.5" rx="1.2" fill="#9aa6b2" stroke="{o}" stroke-width="{sw}"/>' + line((lx - 1.2 + ph * .9, 48.5), (lx + 1.4 + ph * .9, 48.5), o, .5)
        b += f'<rect x="20" y="36.6" width="24" height="13" rx="6.5" fill="{st}" stroke="{o}" stroke-width="{sw}"/>'
        b += line((28, 37), (28, 49.4), '#8d99a5', .5) + line((36, 37), (36, 49.4), '#8d99a5', .5) + ''.join(circ(x, 39, .45, '#5a6670') for x in (23, 31, 39))
        b += f'<rect x="29.4" y="41" width="5.6" height="4" rx="1" fill="#1c2630"/>' + circ(31, 43, .8, '#6fe08a') + circ(33.4, 43, .8, '#ffd23a')
        b += head(43, 35)
    elif pose in ('sit', 'work0', 'work1'):
        b += tail('M26,51 q-9,1 -8,-6') + circ(18, 44.6, 1.8, '#3ff0ff', o, .5)
        b += f'<path d="M24,52 q-1,-16 9,-17 q9,1 8,17 Z" fill="{st}" stroke="{o}" stroke-width="{sw}"/>'
        b += f'<rect x="29.6" y="40" width="7.6" height="6.4" rx="1.4" fill="#1c2630"/>' + circ(31.6, 43.2, 1, '#6fe08a') + circ(35.2, 43.2, 1, '#ff6a8a' if pose == 'work1' else '#ffd23a')
        b += line((25, 47.5), (41.6, 47.5), '#8d99a5', .5) + circ(26.6, 39.6, .5, '#5a6670') + circ(40, 39.6, .5, '#5a6670')
        b += f'<rect x="28.2" y="49.4" width="4.6" height="3.4" rx="1.4" fill="#9aa6b2" stroke="{o}" stroke-width=".7"/><rect x="34.2" y="49.4" width="4.6" height="3.4" rx="1.4" fill="#9aa6b2" stroke="{o}" stroke-width=".7"/>'
        if pose != 'sit':
            up = pose == 'work1'
            b += f'<path d="M39,42 L{46 if up else 45},{36 if up else 39}" stroke="{o}" stroke-width="3.6" stroke-linecap="round"/><path d="M39,42 L{46 if up else 45},{36 if up else 39}" stroke="#c3ccd4" stroke-width="2.2" stroke-linecap="round"/>'
            wx, wy = (47, 34) if up else (46.4, 37.6)
            b += f'<g transform="rotate({-35 if up else -10} {wx} {wy})"><rect x="{wx-.8}" y="{wy-6}" width="1.6" height="7" fill="#d8a82a" stroke="#8a6a12" stroke-width=".4"/><path d="M{wx-2.4},{wy-6} a2.4,2.4 0 1 1 4.8,0 l-1.2,0 l0,-1.4 l-2.4,0 l0,1.4 Z" fill="#d8a82a" stroke="#8a6a12" stroke-width=".4"/></g>'
            if up: b += ''.join(line((wx + 3, wy - 8), (wx + 3 + math.cos(a) * 3, wy - 8 + math.sin(a) * 3), '#ffe27a', .7) for a in (-2.4, -1.2, 0, 1))
        b += head(33.5, 30, lit=pose != 'work0')
    else:  # sleep: powered down
        b += f'<rect x="19" y="41" width="24" height="12" rx="6" fill="{st}" stroke="{o}" stroke-width="{sw}"/>' + tail('M19,49 q8,6 22,2')
        b += head(39, 45, True, False)
        b += f'<text x="44" y="32" font-family="Arial" font-weight="bold" font-size="5" fill="#3ff0ff">z</text><text x="48" y="27" font-family="Arial" font-weight="bold" font-size="4" fill="#3ff0ff">z</text>'
    return f'<g transform="translate(32 52) scale(1.16) translate(-32 -52)">{b}</g>'
for _p in ('walk0', 'walk1', 'sit', 'work0', 'work1', 'sleep'):
    add(f'robo_{_p}', robocat(_p))

# ---------------------------------------------------------------- weekly login prizes
def p_topiary():
    b = ell(0, 0, 7, 2.2, '#1d3a24', 'opacity=".2"')
    b += poly([(-5.5, -9), (5.5, -9), (4.2, 0), (-4.2, 0)], '#d9d2c0', '#8a8478', .7) + f'<rect x="-6.5" y="-11" width="13" height="2.6" rx="1" fill="#e8e2d2" stroke="#8a8478" stroke-width=".5"/>'
    b += line((0, -11), (0, -16), '#7a5232', 1.6)
    for i, (y, r) in enumerate(((-19, 6.2), (-28, 5.2), (-36, 4.2), (-43, 3.2))):
        b += ell(0, y, r, r * .78, '#3f9a4a', 'stroke="#246330" stroke-width=".7"') + ell(-r * .35, y - r * .3, r * .4, r * .25, '#7fd08a', 'opacity=".6"')
    b += circ(0, -47.5, 1.6, '#ffd23a', '#c99a12', .5)
    return b
def p_bonsai():
    b = ell(0, 0, 6, 1.6, '#1d3a24', 'opacity=".25"') + f'<rect x="-6" y="-3.4" width="12" height="3.4" rx="1" fill="#3a5a8a" stroke="#22385a" stroke-width=".5"/>'
    b += qd('M-.5,-3.4 Q-2,-7 1,-9 Q3,-11 1.4,-13', '#6a4a2a', 1.6) + qd('M1,-9 Q4,-10 5.4,-11.4', '#6a4a2a', 1)
    for x, y, r in ((-2.4, -13.6, 3.4), (2.2, -14.6, 3), (5.4, -12, 2.4), (-4.8, -11.2, 2.2)): b += ell(x, y, r, r * .62, '#4f9a4a', 'stroke="#2f6a2f" stroke-width=".5"')
    return b
def p_cans():
    b = f'<path d="M-12,0 L12,0 L12,1.8 L-12,1.8 Z" fill="#7a5232"/>'
    for dx, s in ((-6, 1), (5.5, .82)):
        g_ = f'<path d="M-5,-10 L5,-10 L4.4,0 L-4.4,0 Z" fill="#c8743a" stroke="#7a3f1a" stroke-width=".6"/>' + qd('M-3.6,-10 Q0,-15 3.6,-10', '#7a3f1a', 1) + qd('M4.6,-6 L10,-11.6', '#c8743a', 1.6) + ell(10.6, -12.2, 1.6, 1, '#a85a2a') + line((-4.6, -6), (4.6, -6), '#e09a5a', .6)
        b += f'<g transform="translate({dx} 0) scale({s})">{g_}</g>'
    return b
def p_chandelier():
    b = line((0, 0), (0, 6), '#c99a12', .7) + circ(0, 6.5, 1.4, '#d8b02a', '#8a6a12', .4)
    b += ell(0, 12, 11, 2.6, 'none', 'stroke="#d8b02a" stroke-width="1.2"') + qd('M0,7 Q-8,8 -10,12 M0,7 Q8,8 10,12 M0,7 V16', '#d8b02a', .8)
    for x in (-10, -5, 0, 5, 10):
        y = 12 + (1.6 if abs(x) < 7 else 0)
        b += f'<rect x="{x-.8}" y="{y-5}" width="1.6" height="4.4" fill="#fff8e0"/>' + f'<path d="M{x},{y-7.2} q-1,1.2 0,2.2 q1,-1 0,-2.2 Z" fill="#ffb21a"/>'
        b += line((x, y), (x, y + 3.4), '#cfe8f0', .4) + poly([(x, y + 3.4), (x - 1.2, y + 5.4), (x, y + 7.6), (x + 1.2, y + 5.4)], '#e8f8ff', '#8ab8c8', .3)
    b += poly([(0, 16), (-1.6, 18.6), (0, 21.6), (1.6, 18.6)], '#e8f8ff', '#8ab8c8', .4)
    return b
for _k, (_f, _w, _h, _ax, _ay) in {'topiary': (p_topiary, 18, 54, 9, 52), 'bonsai': (p_bonsai, 16, 20, 8, 18), 'cans': (p_cans, 34, 22, 17, 18), 'chandelier': (p_chandelier, 28, 26, 14, 1)}.items():
    add(f'dp_{_k}', g(_f(), _ax, _ay), _w, _h, (_ax, _ay))
def icon2(k):
    if k == 'seeds':
        b = frame('rail') + swag(11, 53, 12, 8, '#7a5a3a')
        for i in range(6):
            t = (i + .5) / 6; x, yy = sag_at(11, 53, 12, 8, t)
            c = ['#f6efd8', '#e8f0d8', '#f6e0e8', '#e0ecf6', '#fff3c4', '#f0e4f8'][i]; fc = ['#ff5a7a', '#ffb21a', '#c86ae8', '#4fa8ff', '#ff8a1a', '#3fae5a'][i]
            b += f'<rect x="{f2(x-2.6)}" y="{f2(yy+.4)}" width="5.2" height="7.4" fill="{c}" stroke="#8a7a5a" stroke-width=".4"/>' + flower(x, yy + 3.4, 1.6, fc) + line((x - 2, yy + 6.4), (x + 2, yy + 6.4), '#8a7a5a', .4)
        return b
    if k == 'topiary': return frame('door') + g(gs(p_topiary(), 0, 0, .78), 16, 50) + g(gs(p_topiary(), 0, 0, .78), 48, 50)
    if k == 'bonsai': return frame('ledge') + g(p_bonsai(), 18, 41) + g(gs(p_bonsai(), 0, 0, 1.15), 32, 41) + g(f'<g transform="scale(-1 1)">{p_bonsai()}</g>', 46, 41)
    if k == 'cans': return frame('wall') + g(gs(p_cans(), 0, 0, 1.3), 32, 32)
    if k == 'chandelier': return frame('wall') + g(gs(p_chandelier(), 0, 0, 1.25), 32, 10)
for _k in ('seeds', 'topiary', 'bonsai', 'cans', 'chandelier'):
    add(f'deco_{_k}', icon2(_k))
def hat2(k):
    if k == 'crown':
        b = f'<path d="M-5.6,0 L-6,-7 L-3,-4 L0,-8.6 L3,-4 L6,-7 L5.6,0 Z" fill="#ffd23a" stroke="#b8860b" stroke-width=".6"/>' + f'<rect x="-5.8" y="-1.8" width="11.6" height="2.2" fill="#e8b830" stroke="#b8860b" stroke-width=".4"/>'
        b += circ(0, -.7, .9, '#d8202f') + circ(-3.4, -.7, .7, '#2a5fc0') + circ(3.4, -.7, .7, '#3fae5a') + circ(0, -8.6, .9, '#ffffff') + circ(-6, -7, .7, '#ffffff') + circ(6, -7, .7, '#ffffff')
    elif k == 'beanie':
        b = f'<path d="M-5.8,.4 Q-6,-7.4 0,-7.6 Q6,-7.4 5.8,.4 Z" fill="#d8202f" stroke="#7a0f1a" stroke-width=".6"/>' + f'<path d="M-3,-7 Q0,-7.8 3,-7 L3.4,-1 L-3.4,-1 Z" fill="#2a5fc0" opacity=".9"/><path d="M-5.8,-1.2 Q0,.2 5.8,-1.2 L5.8,.4 Q0,1.6 -5.8,.4 Z" fill="#ffd23a"/>'
        b += line((0, -7.6), (0, -10.4), '#5a5a5a', .8) + ell(-3.4, -10.8, 3.4, 1, '#ffd23a', 'stroke="#b8860b" stroke-width=".4"') + ell(3.4, -10.8, 3.4, 1, '#3fae5a', 'stroke="#2f7a3f" stroke-width=".4"') + circ(0, -10.8, .9, '#5a5a5a')
    elif k == 'wizard':
        b = ell(0, 0, 8.6, 2.2, '#2a3a8a', 'stroke="#10204a" stroke-width=".6"') + f'<path d="M-4.6,-.4 L4.6,-.4 Q2,-8 -.6,-16 Q-2.4,-8 -4.6,-.4 Z" fill="#3a4ab0" stroke="#10204a" stroke-width=".6"/>'
        for x, y, r in ((-1.6, -4, 1.1), (1.8, -7, .9), (-.6, -10.4, .8), (2.2, -2.4, .7)): b += f'<path d="M{x},{y-r} L{x+r*.3},{y-r*.3} L{x+r},{y} L{x+r*.3},{y+r*.3} L{x},{y+r} L{x-r*.3},{y+r*.3} L{x-r},{y} L{x-r*.3},{y-r*.3} Z" fill="#ffd23a"/>'
    else:  # party
        b = f'<path d="M-4.6,0 L4.6,0 L.6,-13 Z" fill="#ff6aa8" stroke="#c0407e" stroke-width=".6"/>' + qd('M-3,-4.4 L3.4,-3 M-1.6,-8.4 L2,-7.6', '#ffe27a', 1.2) + circ(.6, -13.6, 1.8, '#5ac8ff', '#2a8ac0', .4) + qd('M-4.4,.6 Q-6,3 -4.8,5', '#8a8a8a', .4)
        for x, y, c in ((-1.4, -1.8, '#5ac8ff'), (1.8, -6, '#3fae5a'), (-.4, -10, '#ffd23a')): b += circ(x, y, .7, c)
    return b
for _k in ('crown', 'beanie', 'wizard', 'party'):
    add(f'hat_{_k}', g(hat2(_k), 14, 18), 28, 24, (14, 18))
def trowel():
    b = f'<path d="M32,8 L44,22 Q46,30 38,36 L33,40 L24,31 L28,26 Q22,18 32,8 Z" fill="#bfeaff" stroke="#3a8ab0" stroke-width="1"/>'
    b += f'<path d="M32,8 L36,24 L28,26 Q22,18 32,8 Z" fill="#e8f8ff"/><path d="M36,24 L44,22 Q46,30 38,36 Z" fill="#8fd0f0"/><path d="M28,26 L36,24 L38,36 L33,40 L24,31 Z" fill="#a8def8"/>'
    b += line((26, 34), (18, 42), '#c9a24a', 3) + f'<path d="M18,42 L10,50 Q8,54 12,54 L20,46 Z" fill="#5a3a22" stroke="#2a1a0a" stroke-width=".7"/>'
    for x, y in ((30, 14), (40, 30), (35, 22)): b += f'<path d="M{x},{y-3} L{x+.8},{y-.8} L{x+3},{y} L{x+.8},{y+.8} L{x},{y+3} L{x-.8},{y+.8} L{x-3},{y} L{x-.8},{y-.8} Z" fill="#ffffff"/>'
    return b
add('trowel_dia', trowel())
