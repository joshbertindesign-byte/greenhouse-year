import json, base64, re
pj = json.load(open('/home/claude/sprites/greenhouse_sheet.json'))
frames = {k: [f['x'], f['y'], f['w'], f['h'], f['anchor'][0], f['anchor'][1]] for k, f in pj['frames'].items()}
src = 'data:image/png;base64,' + base64.b64encode(open('/home/claude/sprites/greenhouse_sheet.png', 'rb').read()).decode()
svg = open('/home/claude/sprites/vec/greenhouse_vector.svg').read()
vj = json.load(open('/home/claude/sprites/vec/greenhouse_vector.json'))['symbols']
defs = {m.group(1): m.group(0) for m in re.finditer(r'<(?:linear|radial)Gradient id="([^"]+)".*?</(?:linear|radial)Gradient>', svg)}
vec = {}
for m in re.finditer(r'<symbol id="([^"]+)" viewBox="0 0 (\d+) (\d+)">(.*?)</symbol>', svg, re.S):
    i, w, h, body = m.group(1), int(m.group(2)), int(m.group(3)), m.group(4)
    refs = sorted(set(re.findall(r'url\(#([^)]+)\)', body)))
    d = ''.join(defs[r] for r in refs)
    a = vj[i]['anchor']
    vec[i] = [w, h, a[0], a[1], f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w*4}" height="{h*4}"><defs>{d}</defs>{body}</svg>']
open('/home/claude/gy8/art.js', 'w').write('const ART=' + json.dumps({'pixel': {'src': src, 'frames': frames}, 'vector': vec}, separators=(',', ':')) + ';\n')
print(len(frames), len(vec))
