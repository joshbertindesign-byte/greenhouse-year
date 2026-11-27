# Build the agent copy of the game: UI stays quiet, but gameplay that "quiet" used to switch off runs again.
import sys, re
src, out = sys.argv[1], sys.argv[2]
s = open(src).read()
A = '(window.__quiet&&!window.__agent)'
reps = [
  ("if(!sucOn()||window.__quiet)return;", f"if(!sucOn()||{A})return;"),                       # succulent walk-ins
  ("if(!fieldOpen()||window.__quiet)return;", f"if(!fieldOpen()||{A})return;"),               # tree jobs
  ("if(!S.fy||window.__quiet)return;", f"if(!S.fy||{A})return;"),                             # festival field jobs, garden tour
  ("if(!window.__quiet){const nc=", f"if(!{A}){{const nc="),                                   # phone calls
  ("if(!window.__quiet&&rnd()<Math.min(.95,", f"if(!{A}&&rnd()<Math.min(.95,"),               # stars
  ("function stepCup(dt){\n  if(window.__quiet||S.phase!=='run')return;", f"function stepCup(dt){{\n  if({A}||S.phase!=='run')return;"),  # coffee cup
  ("if(checkRepLoss()&&!window.__quiet){gameOver();return;}", f"if(checkRepLoss()&&!{A}){{gameOver();return;}}"),   # losing every customer ends the game
  ("function beginPlan(){if(S.lost&&!window.__quiet){gameOver();return;}", f"function beginPlan(){{if(S.lost&&!{A}){{gameOver();return;}}"),
  ("if(window.__quiet){const res=ctx.opts[ctx.opts.length-1].go();return;}", "if(window.__quiet){const ok=ctx.opts.filter(o=>!o.dis),o=window.__agentCall?window.__agentCall(ctx,ok):ctx.opts[ctx.opts.length-1];o.go();return;}"),  # the agent answers calls
  ("const R0=closeYear();save();hud();", "const R0=closeYear();hud();"),                         # no saving to localStorage every year
]
for a, b in reps:
    n = s.count(a); assert n == 1, (a[:70], n); s = s.replace(a, b)
s = s.replace("tips:{},coached:1,name:'',", "tips:{},coached:1,tipsOff:1,name:'Agent Nursery',")
s = s.replace('setTimeout(()=>dailyModal(),1800);', '').replace('setTimeout(()=>dailyModal(),1200);', '')
s = s.replace("\nboot();\n", "\nwindow.__agent=1;window.__quiet=true;\nboot();\n")
open(out, 'w').write(s)
print('ok', len(reps), 'patches')
