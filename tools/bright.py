# "Bright" style test: no outlines, saturated colours, soft two-tone shading, and a distinct silhouette per crop.
import math,random,json
def f(v):return f"{v:.2f}".rstrip('0').rstrip('.')
POTS=[(24.2,11),(33.8,15.8),(11.4,17.4),(43.4,20.6),(21,22.2),(30.6,27)]
def pot(x,yt):
    c=x+4.6;b=yt+6.8
    return (f'<ellipse cx="{f(c)}" cy="{f(b+.4)}" rx="5" ry="1.5" fill="#000" opacity=".12"/>'
            f'<path d="M{f(x)},{f(yt)} L{f(x+9.2)},{f(yt)} L{f(x+8)},{f(b)} Q{f(c)},{f(b+.9)} {f(x+1.2)},{f(b)} Z" fill="url(#gPot)"/>'
            f'<path d="M{f(c+1.6)},{f(yt)} L{f(x+9.2)},{f(yt)} L{f(x+8)},{f(b)} Q{f(c+2.2)},{f(b+.6)} {f(c+1.2)},{f(b+.5)} Z" fill="#a9512c" opacity=".45"/>'
            f'<path d="M{f(x+1.5)},{f(yt+1.6)} L{f(x+2.5)},{f(yt+1.6)} L{f(x+2.9)},{f(b-.6)} L{f(x+2.1)},{f(b-.6)} Z" fill="#fff" opacity=".3"/>'
            f'<ellipse cx="{f(c)}" cy="{f(yt)}" rx="5.2" ry="1.8" fill="#f6a576"/><ellipse cx="{f(c)}" cy="{f(yt+.2)}" rx="4.1" ry="1.15" fill="#6b4226"/>')
def leaf(x,y,ang,L,w,c1,c2,vein=None):
    a=math.radians(ang);ux,uy=math.cos(a),math.sin(a);px,py=-uy,ux;tx,ty=x+ux*L,y+uy*L
    l1=(x+ux*L*.4+px*L*w,y+uy*L*.4+py*L*w);l2=(x+ux*L*.4-px*L*w,y+uy*L*.4-py*L*w)
    s=f'<path d="M{f(x)},{f(y)} Q{f(l1[0])},{f(l1[1])} {f(tx)},{f(ty)} Q{f(l2[0])},{f(l2[1])} {f(x)},{f(y)} Z" fill="{c1}"/><path d="M{f(x)},{f(y)} L{f(tx)},{f(ty)} Q{f(l2[0])},{f(l2[1])} {f(x)},{f(y)} Z" fill="{c2}"/>'
    if vein:s+=f'<path d="M{f(x+ux*L*.1)},{f(y+uy*L*.1)} L{f(x+ux*L*.75)},{f(y+uy*L*.75)}" stroke="{vein}" stroke-width=".35" stroke-linecap="round"/>'
    return s
def blob(cx,cy,rx,ry,c,op=1):return f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(rx)}" ry="{f(ry)}" fill="{c}"'+(f' opacity="{op}"' if op!=1 else '')+'/>'

# ---------- petunia: low spreading mound, trumpets spilling over the rim ----------
PK=('#ff62b6','#ffb6dd','#e03c93','#9c1f62','#fff3a6')
def trumpet_face(cx,cy,r,rot,sy=.8,col=PK):
    base,hi,mid,dk,th=col;P=[]
    for i in range(30):
        t=i/30*2*math.pi;lobe=abs(math.cos(5*(t-rot)/2));R=r*(.66+.34*lobe**.6)
        P.append((cx+R*math.cos(t),cy+R*math.sin(t)*sy))
    d='M'+' L'.join(f"{f(x)},{f(y)}" for x,y in P)+' Z'
    s=f'<path d="{d}" fill="{base}"/><path d="{d}" fill="{hi}" transform="translate({f(-r*.18)},{f(-r*.2)}) scale(1)" opacity=".0"/>'
    s+=blob(cx-r*.28,cy-r*.3*sy,r*.42,r*.28*sy,hi)
    for k in range(5):
        a=rot+k*2*math.pi/5;s+=f'<path d="M{f(cx)},{f(cy)} L{f(cx+math.cos(a)*r*.62)},{f(cy+math.sin(a)*r*.62*sy)}" stroke="{mid}" stroke-width="{f(r*.16)}" stroke-linecap="round"/>'
    s+=blob(cx,cy,r*.3,r*.3*sy,dk)+blob(cx-r*.05,cy-r*.05,r*.12,r*.12*sy,th)
    return s
def trumpet_side(x,y,ang,L,col=PK):
    base,hi,mid,dk,th=col;a=math.radians(ang);ux,uy=math.cos(a),math.sin(a);px,py=-uy,ux
    tip=(x+ux*L,y+uy*L)
    tube=f'<path d="M{f(x+px*.35)},{f(y+py*.35)} L{f(tip[0]+px*L*.42)},{f(tip[1]+py*L*.42)} L{f(tip[0]-px*L*.42)},{f(tip[1]-py*L*.42)} L{f(x-px*.35)},{f(y-py*.35)} Z" fill="{mid}"/>'
    mouth=f'<ellipse cx="{f(tip[0])}" cy="{f(tip[1])}" rx="{f(L*.5)}" ry="{f(L*.24)}" fill="{base}" transform="rotate({f(ang+90)} {f(tip[0])} {f(tip[1])})"/>'
    inner=f'<ellipse cx="{f(tip[0]-ux*.2)}" cy="{f(tip[1]-uy*.2)}" rx="{f(L*.22)}" ry="{f(L*.1)}" fill="{dk}" transform="rotate({f(ang+90)} {f(tip[0])} {f(tip[1])})"/>'
    return tube+mouth+inner
def petunia(x,yt,seed):
    random.seed(seed);c=x+4.6;o=[]
    # foliage mound spills wider than the pot
    for dx,dy,r in [(-4.8,-1.2,2.6),(4.8,-1.0,2.6),(-2.6,-3.2,3),(2.8,-3.4,3),(0,-4.2,3.2),(0,-1.4,3.4)]:
        o.append(blob(c+dx+.4,yt+dy+.5,r,r*.82,'#2f8f3a'))
    for dx,dy,r in [(-4.8,-1.6,2.3),(4.8,-1.4,2.3),(-2.6,-3.6,2.7),(2.8,-3.8,2.7),(0,-4.6,2.9),(0,-1.8,3.0)]:
        o.append(blob(c+dx,yt+dy,r,r*.8,'#56c24a'));o.append(blob(c+dx-r*.35,yt+dy-r*.3,r*.45,r*.3,'#8fe06a'))
    # trumpets hang over the rim at the sides, faces on top
    o.append(trumpet_side(c-4.2,yt-.6,160,3.4));o.append(trumpet_side(c+4.4,yt-.4,20,3.4));o.append(trumpet_side(c-1.4,yt+.4,115,2.8))
    for dx,dy,r in [(-2.8,-5.2,2.3),(2.4,-5.6,2.3),(-.2,-2.8,2.6),(4.6,-2.6,2.0)]:
        o.append(trumpet_face(c+dx,yt+dy,r,random.uniform(0,6.3)))
    return ''.join(o)

# ---------- mum: a near-perfect cushion dome studded with little daisies ----------
def mum(x,yt,seed):
    random.seed(seed);c=x+4.6;o=[];R=6.6;top=yt-.6
    dome=f'M{f(c-R)},{f(top+1.4)} A{f(R)},{f(R*1.05)} 0 0 1 {f(c+R)},{f(top+1.4)} Q{f(c)},{f(top+3.2)} {f(c-R)},{f(top+1.4)} Z'
    o.append(f'<path d="{dome}" fill="#2f8f3a" transform="translate(.3,.5)"/>')
    for k in range(7):  # leaf tips peeking out under the flowers
        a=math.pi*(.95+k*.1/1)+0;o.append(leaf(c-R+.6+k*1.8,top+1.6,90+random.uniform(-25,25),1.8,.45,'#56c24a','#3a9c3e'))
    o.append(f'<path d="{dome}" fill="#f29a12"/>')
    # flower heads in rows over the dome, lighter toward the top-left
    rows=[(top-5.6,2.6,3),(top-4.0,4.6,5),(top-2.2,5.8,6),(top-.4,6.2,7),(top+1.0,5.6,6)]
    for yy,half,n in rows:
        for i in range(n):
            xx=c-half+i*(2*half/(n-1))+random.uniform(-.2,.2)
            lit=(xx-c)*.5+(yy-top)*.8<0
            pet,cen='#ffd23a' if lit else '#ffb21e','#e07a10'
            for k in range(8):
                a=k*math.pi/4;o.append(blob(xx+math.cos(a)*.75,yy+math.sin(a)*.55,.5,.36,pet))
            o.append(blob(xx,yy,.5,.4,cen))
    o.append(f'<ellipse cx="{f(c-2.6)}" cy="{f(top-4)}" rx="2.4" ry="1.2" fill="#fff" opacity=".22"/>')
    return ''.join(o)

# ---------- pothos: upright heart leaves plus vines trailing down the pot ----------
def heart(cx,cy,s,ang,c1,c2,streak):
    t=f'rotate({f(ang)} {f(cx)} {f(cy)})'
    d=f'M{f(cx)},{f(cy+s)} C{f(cx-s*1.4)},{f(cy+s*.1)} {f(cx-s*1.0)},{f(cy-s*1.1)} {f(cx)},{f(cy-s*.45)} C{f(cx+s*1.0)},{f(cy-s*1.1)} {f(cx+s*1.4)},{f(cy+s*.1)} {f(cx)},{f(cy+s)} Z'
    half=f'M{f(cx)},{f(cy+s)} C{f(cx+s*1.4)},{f(cy+s*.1)} {f(cx+s*1.0)},{f(cy-s*1.1)} {f(cx)},{f(cy-s*.45)} Z'
    return (f'<g transform="{t}"><path d="{d}" fill="{c1}"/><path d="{half}" fill="{c2}"/>'
            f'<path d="M{f(cx-s*.5)},{f(cy-s*.2)} Q{f(cx-s*.15)},{f(cy+s*.2)} {f(cx-s*.05)},{f(cy+s*.6)}" stroke="{streak}" stroke-width="{f(s*.28)}" stroke-linecap="round" fill="none"/></g>')
def pothos(x,yt,seed):
    random.seed(seed);c=x+4.6;o=[]
    G1,G2,ST='#5fcf3e','#35a535','#f2f77a'
    for sx,L in [(-1,1),(1,1)]:  # trailing vines
        px,py=c+sx*3.9,yt+.3;pts=[(px,py)]
        for k in range(5):px+=sx*.5+random.uniform(-.4,.4);py+=2.1;pts.append((px,py))
        o.append('<path d="M'+' L'.join(f"{f(a)},{f(b)}" for a,b in pts)+'" stroke="#2f8f3a" stroke-width=".55" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
        for k,(a,b) in enumerate(pts[1:]):o.append(heart(a+sx*.6*(1 if k%2 else -1),b,1.1-.08*k,sx*(40 if k%2 else -30),G1,G2,ST))
    for dx,dy,s,ang in [(-1.4,-6.2,2.1,-20),(1.6,-6.4,2.1,22),(-3.8,-4.0,2.1,-50),(3.9,-4.1,2.1,50),(0,-3.6,2.4,0),(-4.6,-1.2,1.8,-80),(4.7,-1.2,1.8,80),(-1.8,-1.4,2.0,-25),(1.9,-1.5,2.0,25)]:
        o.append(heart(c+dx,yt+dy,s,ang,G1,G2,ST))
    return ''.join(o)

# ---------- geranium: round zoned leaves low, tall stalks with red ball umbels ----------
def geranium(x,yt,seed):
    random.seed(seed);c=x+4.6;o=[]
    for dx,dy,r in [(-3.8,-1.0,2.4),(3.8,-1.0,2.4),(-1.6,-2.4,2.6),(1.8,-2.6,2.6),(0,-.6,2.6)]:
        o.append(blob(c+dx,yt+dy,r,r*.78,'#3f9f3a'));o.append(f'<ellipse cx="{f(c+dx)}" cy="{f(yt+dy)}" rx="{f(r*.62)}" ry="{f(r*.48)}" fill="none" stroke="#2c7a2e" stroke-width=".55" opacity=".8"/>')
        o.append(blob(c+dx-r*.3,yt+dy-r*.25,r*.42,r*.28,'#7fd860'))
    for dx,h,r in [(-2.2,8.6,2.5),(2.4,9.6,2.6),(0.2,6.6,2.2)]:
        bx,by=c+dx,yt-1.5-h
        o.append(f'<path d="M{f(c+dx*.4)},{f(yt-1.5)} Q{f(bx-.6)},{f(by+h*.5)} {f(bx)},{f(by+r*.6)}" stroke="#3a8f34" stroke-width=".7" fill="none" stroke-linecap="round"/>')
        o.append(blob(bx+.3,by+.4,r,r*.9,'#b51f2a'))
        for k in range(9):
            a=k*2*math.pi/9;o.append(blob(bx+math.cos(a)*r*.62,by+math.sin(a)*r*.55,r*.42,r*.38,'#f23a3a'))
        o.append(blob(bx,by,r*.5,r*.45,'#ff4a46'));o.append(blob(bx-r*.35,by-r*.35,r*.32,r*.22,'#ff9a8a'))
    return ''.join(o)

DEFS='<defs><radialGradient id="gPot" cx="0.3" cy="0.3" r="0.9"><stop offset="0" stop-color="#ffb98f"/><stop offset="0.6" stop-color="#ee8656"/><stop offset="1" stop-color="#c9643a"/></radialGradient></defs>'
def tile(fn):
    body=''.join(pot(x,y)+fn(x,y,i) for i,(x,y) in sorted(enumerate(POTS),key=lambda e:e[1][1]))
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="256" height="256">{DEFS}{body}</svg>'
out={f'{k}_3':tile(fn) for k,fn in [('petunia',petunia),('mum',mum),('pothos',pothos),('geranium',geranium)]}
for k,v in out.items():open(k+'.svg','w').write(v)
open('art_bright.js','w').write('// "Bright" art style test: replacement sprites keyed like art.js\nconst ART_BRIGHT='+json.dumps(out,separators=(',',':'))+';\n')
print({k:len(v) for k,v in out.items()})
