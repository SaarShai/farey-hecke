#!/usr/bin/env python3
"""
Fast straight-line UB search. A straight-line drawing with c crossings proves cr(G)<=c
(rectilinear cr >= topological cr, so the count is a valid upper bound on cr).
Incremental recount: moving vertex v only changes crossings on edges incident to v.
Witness = explicit float coordinates; recompute_crossings() re-checks any reported count.
"""
import itertools, math, random, sys, json

def pnk(n,k):
    V=list(range(n)); E=[(a,b) for a in V for b in V if a<b and b-a<=k]; return V,E

def properly_cross(p1,p2,p3,p4):
    def o(a,b,c):
        v=(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
        if abs(v)<1e-12: return 0
        return 1 if v>0 else -1
    d1=o(p3,p4,p1); d2=o(p3,p4,p2); d3=o(p1,p2,p3); d4=o(p1,p2,p4)
    return ((d1>0)!=(d2>0)) and (d1!=0 and d2!=0) and ((d3>0)!=(d4>0)) and (d3!=0 and d4!=0)

def recompute_crossings(pos, E):
    c=0
    for e,f in itertools.combinations(E,2):
        if set(e)&set(f): continue
        if properly_cross(pos[e[0]],pos[e[1]],pos[f[0]],pos[f[1]]): c+=1
    return c

def search(n,k,iters=120000,seed=0):
    random.seed(seed)
    V,E=pnk(n,k)
    inc={v:[e for e in E if v in e] for v in V}
    pos={v:(random.uniform(-1,1),random.uniform(-1,1)) for v in V}
    cur=recompute_crossings(pos,E)
    best=cur; bestpos=dict(pos)
    # incremental delta: crossings involving edges incident to v
    def local_count(v,pos):
        c=0
        ev=inc[v]
        for e in ev:
            for f in E:
                if set(e)&set(f): continue
                # count each crossing once: only if e<f OR f not incident to v (avoid double among ev)
                if f in ev and f<e: continue
                if properly_cross(pos[e[0]],pos[e[1]],pos[f[0]],pos[f[1]]): c+=1
        return c
    for it in range(iters):
        T=max(0.02, 1.5*(1-it/iters))
        v=random.choice(V)
        before=local_count(v,pos)
        old=pos[v]
        if random.random()<0.5:
            pos[v]=(old[0]+random.gauss(0,0.4*T+0.03), old[1]+random.gauss(0,0.4*T+0.03))
        else:
            pos[v]=(random.uniform(-1.2,1.2),random.uniform(-1.2,1.2))
        after=local_count(v,pos)
        delta=after-before
        if delta<=0 or random.random()<math.exp(-delta/max(T,1e-3)):
            cur+=delta
            if cur<best:
                best=cur; bestpos=dict(pos)
        else:
            pos[v]=old
    # verify best from scratch; TRUST the recompute (incremental is only a guide)
    chk=recompute_crossings(bestpos,E)
    if chk!=best:
        # incremental tracking drifted; the rechecked value is authoritative
        best=chk
    return best, bestpos, E

if __name__=="__main__":
    n=int(sys.argv[1]); k=int(sys.argv[2]); nseeds=int(sys.argv[3]) if len(sys.argv)>3 else 6
    its=int(sys.argv[4]) if len(sys.argv)>4 else 120000
    V,E=pnk(n,k)
    glob=10**9; gpos=None
    for s in range(nseeds):
        b,bp,E=search(n,k,iters=its,seed=s)
        print(f"  seed {s}: {b}")
        if b<glob: glob=b; gpos=bp
    print(f"BEST straight-line UB cr(P_{n}^{k}) <= {glob}")
    coords={str(v):[round(gpos[v][0],5),round(gpos[v][1],5)] for v in gpos}
    print("COORDS_JSON="+json.dumps(coords))
    # final independent recheck
    print("RECHECK recompute_crossings =", recompute_crossings(gpos,E))
