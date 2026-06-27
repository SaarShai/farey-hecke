#!/usr/bin/env python3
"""
Upper-bound search via explicit straight-line / circular drawings, with an
INDEPENDENTLY CHECKABLE crossing count.

A drawing = an injective map of each vertex to a point in R^2; edges are straight
segments. Crossings = pairs of independent edges whose open segments properly intersect.
The crossing count of such a drawing is a rigorous UPPER BOUND on cr(G).

We optimize vertex positions (simulated annealing over the plane, plus structured
seeds: convex-position/circular orders which realize the 2-page/book number) to push
the count down. Any count we report comes WITH the explicit coordinates so anyone can
recompute it.
"""
import itertools, math, random, sys

def pnk(n,k):
    V=list(range(n)); E=[(a,b) for a in V for b in V if a<b and b-a<=k]; return V,E

def seg_cross(p1,p2,p3,p4):
    # proper segment intersection (open segments), exclude shared endpoints handled by caller
    def o(a,b,c):
        v=(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
        if abs(v)<1e-12: return 0
        return 1 if v>0 else -1
    d1=o(p3,p4,p1); d2=o(p3,p4,p2); d3=o(p1,p2,p3); d4=o(p1,p2,p4)
    if ((d1>0 and d2<0) or (d1<0 and d2>0)) and ((d3>0 and d4<0) or (d3<0 and d4>0)):
        return True
    return False  # treat collinear/touch as non-crossing; we keep points generic

def count_crossings(pos, E):
    c=0; bad=False
    for (e,f) in itertools.combinations(E,2):
        if set(e)&set(f): continue
        a,b=e; cc,d=f
        if seg_cross(pos[a],pos[b],pos[cc],pos[d]):
            c+=1
    return c

def circular_positions(order, n):
    pos={}
    for idx,v in enumerate(order):
        ang=2*math.pi*idx/n
        pos[v]=(math.cos(ang), math.sin(ang))
    return pos

def anneal(n,k,iters=40000, seed=0):
    random.seed(seed)
    V,E=pnk(n,k)
    # start from a random plane layout
    pos={v:(random.uniform(-1,1), random.uniform(-1,1)) for v in V}
    cur=count_crossings(pos,E)
    best=cur; bestpos=dict(pos)
    T=2.0
    for it in range(iters):
        T=max(0.01, 2.0*(1-it/iters))
        v=random.choice(V)
        old=pos[v]
        pos[v]=(old[0]+random.gauss(0,0.3*T+0.05), old[1]+random.gauss(0,0.3*T+0.05))
        new=count_crossings(pos,E)
        if new<=cur or random.random()<math.exp((cur-new)/max(T,1e-3)):
            cur=new
            if new<best:
                best=new; bestpos=dict(pos)
        else:
            pos[v]=old
    return best, bestpos, E

def circular_anneal(n,k,iters=200000, seed=0):
    """Optimize the circular ORDER (2-page-style) by swapping positions on a circle."""
    random.seed(seed)
    V,E=pnk(n,k)
    order=list(V); random.shuffle(order)
    pos=circular_positions(order,n)
    cur=count_crossings(pos,E)
    best=cur; bestorder=list(order)
    for it in range(iters):
        T=max(0.05, 3.0*(1-it/iters))
        i,j=random.sample(range(n),2)
        order[i],order[j]=order[j],order[i]
        pos=circular_positions(order,n)
        new=count_crossings(pos,E)
        if new<=cur or random.random()<math.exp((cur-new)/T):
            cur=new
            if new<best:
                best=new; bestorder=list(order)
        else:
            order[i],order[j]=order[j],order[i]
    return best, bestorder, E

if __name__=="__main__":
    n=int(sys.argv[1]); k=int(sys.argv[2])
    mode=sys.argv[3] if len(sys.argv)>3 else "plane"
    nseeds=int(sys.argv[4]) if len(sys.argv)>4 else 4
    V,E=pnk(n,k)
    print(f"P_{n}^{k}: |V|={n} |E|={len(E)}")
    glob=None; gpos=None
    for s in range(nseeds):
        if mode=="circ":
            b,od,E=circular_anneal(n,k,seed=s)
            posrep=("circular_order", od)
        else:
            b,bp,E=anneal(n,k,seed=s)
            posrep=("plane_coords", {v:[round(x,4) for x in bp[v]] for v in bp})
        if glob is None or b<glob:
            glob=b; gpos=posrep
        print(f"  seed {s} [{mode}]: {b} crossings")
    print(f"BEST UB for P_{n}^{k}: {glob} crossings")
    print("WITNESS:", gpos)
