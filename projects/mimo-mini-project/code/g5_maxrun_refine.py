#!/usr/bin/env python3
"""
Nail the MAX below-1/4 run on forward T_5 orbits with high confidence.
Decides whether the smallest valid local window is 5 (max run 4) or larger.

Strategy: the long below-runs happen at the ENTRY edge of D. We:
  (a) high-res grid over all in-D seeds, fine;
  (b) targeted refinement: zoom recursively around any seed achieving the current
      max run, on a shrinking box, many rounds;
  (c) also enumerate by floor-WORD: any below-run is a forward segment with some
      floor word (k_1,k_2,...); parametrize the segment by (c0,c1) and the word,
      solve for the (c0,c1) region giving all-below + in-region, maximize run length.
"""
import math, random
phi = (1+math.sqrt(5))/2
T = 0.25
EPS = 1e-9
random.seed(12345)  # fixed: no Date/random-in-loop issues here (plain python)

def in_D(x,y): return x>EPS and y>EPS and x+phi*y > 1+1e-12
def step(x,y):
    k = math.floor((1+x)/(phi*y)); return y, k*phi*y - x

def below_run(x0,y0,cap=50):
    """count leading consecutive P_n<1/4 along forward orbit while in D (from start)."""
    x,y=x0,y0; run=0
    for _ in range(cap):
        if not in_D(x,y): break
        if x*y < T-1e-12: run+=1
        else: break
        x,y=step(x,y)
    return run

def global_below_run(x0,y0,cap=2000):
    """longest below run anywhere along the orbit while in D."""
    x,y=x0,y0; run=best=0
    for _ in range(cap):
        if not in_D(x,y): break
        if x*y<T-1e-12: run+=1; best=max(best,run)
        else: run=0
        x,y=step(x,y)
    return best

def scan_fine(grid=1400):
    best=0; wit=None
    for i in range(1,grid+1):
        x=1.4*i/grid
        for j in range(1,grid+1):
            y=1.4*j/grid
            if not in_D(x,y): continue
            r=global_below_run(x,y,cap=400)
            if r>best: best=r; wit=(x,y)
    return best,wit

def refine(cx,cy,rounds=40,box=0.05,pts=40):
    best=0; wit=(cx,cy)
    for _ in range(rounds):
        nb=0; nw=wit
        for _ in range(pts*pts):
            x=wit[0]+ (random.random()*2-1)*box
            y=wit[1]+ (random.random()*2-1)*box
            if not in_D(x,y): continue
            r=global_below_run(x,y,cap=400)
            if r>nb: nb=r; nw=(x,y)
        if nb>best: best=nb; wit=nw
        box*=0.7
    return best,wit

def word_search(maxlen=9, samples=200000):
    """For each floor-word of given length, sample (c0,c1) and check all-below+in-D.
    Reports the max word length admitting an all-below in-region forward segment."""
    import itertools
    best_len=0; best_word=None; best_wit=None
    for L in range(1,maxlen+1):
        found=False
        # words over small floors {1,2,3}; below-runs use mostly floor 1 and the (1,1,2) motif
        for word in itertools.product([1,2,3],repeat=L):
            # sample (c0,c1) in a box; build segment with FIXED word (override floor),
            # but require floor-consistency = the word AND region AND all products<T.
            for _ in range(max(1, samples//(3**L))):
                c0=random.random()*0.8+0.05
                c1=random.random()*0.8+0.05
                c=[c0,c1]; ok=True
                for n in range(L):
                    k=word[n]
                    # floor consistency at step n: floor((1+c[n])/(phi c[n+1]))==k
                    if c[n+1]<=EPS: ok=False;break
                    if math.floor((1+c[n])/(phi*c[n+1]))!=k: ok=False;break
                    c.append(k*phi*c[n+1]-c[n])
                if not ok: continue
                # region on all consecutive pairs in the segment (need L+2 coords -> L+1 pairs)
                if any(c[m]<=EPS for m in range(len(c))): continue
                if not all(c[m]+phi*c[m+1]>1+1e-12 for m in range(len(c)-1)): continue
                # products: we have coords c0..c_{L+1} -> products P_0..P_L (L+1 products)
                prods=[c[m]*c[m+1] for m in range(len(c)-1)]
                # count the all-below run = number of consecutive products < T from start
                if all(p<T-1e-12 for p in prods):
                    if len(prods)>best_len:
                        best_len=len(prods); best_word=word; best_wit=tuple(round(v,4) for v in c)
                    found=True
        print("  word-search len=%d: best all-below product-run so far=%d" % (L,best_len))
        if not found and L>best_len+1:
            break
    return best_len,best_word,best_wit

if __name__=="__main__":
    print("(a) fine grid:")
    b,w=scan_fine(1200)
    print("   max below-run (grid) =",b," at",tuple(round(v,5) for v in w))
    print("(b) refine around grid witness:")
    b2,w2=refine(w[0],w[1])
    print("   max below-run (refined) =",b2," at",tuple(round(v,6) for v in w2))
    print("(c) floor-word search (max all-below product run):")
    bl,bw,bwit=word_search(maxlen=9)
    print("   => MAX all-below product run =",bl," word=",bw," coords=",bwit)
    print()
    M=max(b2,bl)
    print("CONCLUSION: max below-1/4 run on T_5 forward segments =",M)
    print("  smallest valid LOCAL window bound = window",M+1,
          "(no",M+1,"consecutive products all < 1/4).")
