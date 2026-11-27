# Fit painted sprites (true isometric, large) to the game's 2:1 grid and store them as game sprites.
import json, base64, io, sys
import numpy as np
from PIL import Image
UP = '/mnt/user-data/uploads/'
OUT = '/home/claude/sprites/painted/'
SQ = 0.87          # true isometric (30 deg) -> the game's 2:1 grid
PX = 4             # stored at 4x
def save(id_, img, w, h, ax, ay):
    img.save(OUT + 'png/' + id_ + '.png')
    b = io.BytesIO(); img.save(b, 'WEBP', quality=90, method=6)
    uri = 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {w} {h}" width="{w*4}" height="{h*4}"><image width="{w}" height="{h}" xlink:href="{uri}" href="{uri}"/></svg>'
    json.dump({'id': id_, 'w': w, 'h': h, 'ax': ax, 'ay': ay, 'svg': svg}, open(OUT + id_ + '.json', 'w'))
    print(id_, img.size, len(svg) // 1024, 'KB')
def place(src, a, b, sx0, sy0, tx, ty, W, H):
    """Scale src by (a,b) units per source px and put source point (sx0,sy0) at sprite point (tx,ty); canvas W x H units."""
    s = src.resize((max(1, round(src.width * a * PX)), max(1, round(src.height * b * PX))), Image.LANCZOS)
    can = Image.new('RGBA', (W * PX, H * PX), (0, 0, 0, 0))
    can.alpha_composite(s, (round(tx * PX - sx0 * a * PX), round(ty * PX - sy0 * b * PX)))
    return can
# ---- benches: the top face spans x 80..943, its left/right corners at y 345, top corner y 97.
# The legs are shorter than the game's bench (top 30 units above the floor), so stretch everything below
# the frame by K, column by column.
K = 1.62
def frame_bottom(x):
    pts = [(80, 412), (511, 688), (943, 432)]
    if x <= 511: (x0, y0), (x1, y1) = pts[0], pts[1]
    else: (x0, y0), (x1, y1) = pts[1], pts[2]
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
def stretch_legs(im):
    a = np.array(im); H, W = a.shape[:2]; NH = int(H * 1.5)
    out = np.zeros((NH, W, 4), np.uint8); out[:H] = a
    for x in range(W):
        yb = int(round(frame_bottom(x))) + 2
        ys = np.arange(yb, NH); src = (yb + (ys - yb) / K).astype(int)
        ok = src < H; col = np.zeros((len(ys), 4), np.uint8); col[ok] = a[src[ok], x]
        out[yb:NH, x] = col
    return Image.fromarray(out)
A = 32 / 431.5; B = A * SQ
benches = {'bench_left': 'aa907956', 'bench_mid': '36f72e7d', 'bench_right': '9d876fa3'}
bench_img = {}
for id_, f in benches.items():
    im = stretch_legs(Image.open(UP + f + '-image.png').convert('RGBA'))
    can = place(im, A, B, 511.5, 345, 32, 24, 64, 80)   # canvas 64x80, anchor (32,32): the top face centre is at (32,24)
    bench_img[id_] = can; save(id_, can, 64, 80, 32, 32)
# ---- trays and crops: rim corners at x 50/973, y 446; rim top corner y 181; the tray is 132 px deep at the front.
TA = 28.8 / 461.5; TB = TA * SQ; WALL = 132 * TB
def crop(f):  # canvas 64x80, anchor (32,48): the tile's bench-top centre is at (32,40); the rim sits WALL above it
    return place(Image.open(UP + f + '-image.png').convert('RGBA'), TA, TB, 511.5, 446, 32, 40 - WALL, 64, 80)
for st, f in enumerate(['098babfd', 'ba74a488', 'c377f1dc', 'e8e55e60']): save(f'petunia_{st}', crop(f), 64, 80, 32, 48)
tray = crop('8474eaa1')
for id_, can in bench_img.items():   # bench with an empty tray waiting to be potted: same tray, 16 units higher in the bench canvas
    c = can.copy(); c.alpha_composite(tray, (0, -16 * PX)); save(id_ + '_tray', c, 64, 80, 32, 32)
