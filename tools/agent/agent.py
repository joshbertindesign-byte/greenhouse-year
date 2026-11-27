# Run the Greenhouse Year test agent at several reaction speeds and report average play time to each milestone.
#   python3 agent.py RUNS YEARS [profile,profile,...]
import sys, json, time, statistics as st, os
from concurrent.futures import ProcessPoolExecutor
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
UP = ['pots', 'hose', 'soil', 'bugs', 'potter', 'boom', 'fork', 'lights', 'vents', 'heat', 'roll']
SK = ['quick', 'steady', 'quick', 'steady', 'multi', 'quick', 'steady', 'shortcut', 'wind', 'multi', 'foreman', 'foreman', 'mentor', 'smooth', 'smooth',
      'pesteye', 'deepw', 'pesteye', 'deepw', 'gentle', 'gentle', 'starspot', 'starspot', 'caffeine', 'negot', 'negot', 'bulk', 'bulk', 'arbor', 'arbor',
      'finesse', 'finesse', 'shopkeep', 'shopkeep', 'whisper', 'greenlight', 'lucky', 'caffeine']
HOME = ['stand', 'cats', 'garden', 'office', 'shed', 'bunk', 'solar', 'solarUp', 'reserve', 'pond', 'pergola']
BASE = dict(dt=.15, patience=5, buffer=1800, upOrder=UP, skillOrder=SK, homeOrder=HOME, starReserve=8, festJoin=.85, callYes=.6, modal=6, skipChance=0)
PROFILES = {
  # react: seconds before a player notices a new job; glance: seconds between looks at the board (each look taps up to maxQueue jobs); lapse: chance per second of zoning out, for lapseLen seconds
  'Lightning': dict(react=.8, glance=.5, lapse=0, lapseLen=0, maxQueue=6, fifo=False, cupNotice=.95, planBase=15, perOrder=3, perAct=4, yearStart=20, homeBase=25, homePerAct=5, yearEnd=15),
  'Sharp':     dict(react=1.2, glance=1, lapse=.002, lapseLen=5, maxQueue=5, fifo=False, cupNotice=.8, planBase=22, perOrder=4, perAct=5, yearStart=30, homeBase=35, homePerAct=6, yearEnd=20),
  'Steady':    dict(react=2, glance=2, lapse=.004, lapseLen=8, maxQueue=4, fifo=False, cupNotice=.6, planBase=30, perOrder=5, perAct=6, yearStart=40, homeBase=45, homePerAct=8, yearEnd=25),
  'Casual':    dict(react=3, glance=3.5, lapse=.008, lapseLen=10, maxQueue=3, fifo=False, cupNotice=.45, planBase=40, perOrder=6, perAct=8, yearStart=50, homeBase=55, homePerAct=10, yearEnd=30, skipChance=.08),
  'Distracted':dict(react=4.5, glance=5, lapse=.015, lapseLen=15, maxQueue=3, fifo=True, cupNotice=.3, planBase=50, perOrder=8, perAct=10, yearStart=60, homeBase=65, homePerAct=12, yearEnd=40, skipChance=.15),
}

def run_one(args):
    name, runs, years = args
    sp, _, pl = name.partition(':')  # 'Steady:expert' = reaction profile + planner tier (expert / average / novice)
    prof = dict(BASE, **PROFILES[sp], planner=pl or 'average', name=name)
    out = []
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        for r in range(runs):
            pg = b.new_page(); pg.route("**/fonts.googleapis.com/**", lambda x: x.abort())
            pg.goto("file://" + HERE + "/" + os.environ.get("GAME", "a.html")); pg.wait_for_timeout(300); pg.add_script_tag(path=HERE + "/agent.js")
            pg.evaluate("p=>AG.start(p)", prof)
            t0 = time.time()
            for y in range(years):
                res = pg.evaluate("()=>{const r=AG.years(1);return {n:r.years.length,over:r.over}}")
                print(f"  {name} run {r+1} year {y+1}: {time.time()-t0:5.0f}s", file=sys.stderr, flush=True)
                if res['over'] or res['n'] <= y: break
            out.append(pg.evaluate("()=>AG.R")); pg.close()
        b.close()
    return name, out

def hm(m):
    return f"{int(m//60)}h {int(m%60):02d}m" if m >= 60 else f"{int(m)}m"

def run_single(args):
    name, idx, years, outl = args
    try:
        nm, out = run_one((name, 1, years))
        r = out[0]; r['run'] = idx
    except Exception as e:
        r = {'profile': name, 'run': idx, 'crashed': str(e)[:200], 'years': [], 'ms': {}, 'used': {}, 'errors': {}, 'over': {'why': 'crash', 'year': 0, 'min': 0}}
    with open(outl, 'a') as f: f.write(json.dumps(r) + '\n')
    return name, idx, (r['over'] or {}).get('why'), len(r['years'])

if __name__ == '__main__' and os.environ.get('LONG'):
    # LONG=1 python3 agent.py RUNS_PER_PROFILE MAX_YEARS: one task per run, results appended to OUT as JSON lines
    runs = int(sys.argv[1]); years = int(sys.argv[2]); names = sys.argv[3].split(',') if len(sys.argv) > 3 else list(PROFILES)
    outl = HERE + '/' + os.environ.get('OUT', 'long.jsonl')
    jobs = [(n, i, years, outl) for i in range(runs) for n in names]
    with ProcessPoolExecutor(max_workers=int(os.environ.get('WORKERS', 2))) as ex:
        for res in ex.map(run_single, jobs): print('DONE', *res, flush=True)
    sys.exit(0)

if __name__ == '__main__':
    runs = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    years = int(sys.argv[2]) if len(sys.argv) > 2 else 15
    names = sys.argv[3].split(',') if len(sys.argv) > 3 else list(PROFILES)
    with ProcessPoolExecutor(max_workers=int(os.environ.get('WORKERS', 2))) as ex:
        res = dict(ex.map(run_one, [(n, runs, years) for n in names]))
    json.dump(res, open(HERE + '/' + os.environ.get('OUT', 'results.json'), 'w'))
    print(json.dumps({n: {'over': [r['over'] for r in rs], 'errors': [r['errors'] for r in rs]} for n, rs in res.items()}, indent=1))
