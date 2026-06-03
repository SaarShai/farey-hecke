#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GOAL K (q=6) DEDICATED window-3 pre-test.  lam=sqrt(3), lam^2=3, threshold thr=1/lam^3=sqrt3/9.

Window-3 scalar lemma claim (the q=6 analogue of g5's window-4, per FINDINGS_goalE):
  scalar seq c0..c3 (4 coords, 3 products P0=c0c1,P1=c1c2,P2=c2c3), 2 floors K0,K1>=1,
  recurrence  c_n + c_{n+2} = K_n * lam * c_{n+1},  (n=0,1)
  BOTH Taha edges on every consecutive pair:  lam*c_n + c_{n+1} > 1  AND  c_n + lam*c_{n+1} > 1,
  cap 0 < c_n <= 1.
  CLAIM: NOT all three products < thr.

We:
 (1) confirm the genuine longest below-thr run is 2 (=> window 3) for genuine orbits;
 (2) LOCAL truth test of the window-3 lemma: over ALL feasible (c0,c1,c2,c3) satisfying the
     hypotheses for each floor combo (K0,K1), is min over feasible of max(P0,P1,P2) > thr?
     Also test WITHOUT one edge / WITHOUT cap to see which hypotheses are load-bearing.
 (3) report the worst (tightest) floor word and its margin -> tells us how many certs we need.
"""
import math
import itertools

lam = math.sqrt(3.0)
thr = 1.0/lam**3   # = sqrt3/9 ~ 0.19245

def feasible(c0, c1, c2, c3, K0, K1, use_cap=True, use_edge_gen=True, use_edge_reg=True,
             tol=1e-9):
    cs = [c0, c1, c2, c3]
    if any(c <= tol for c in cs):
        return False
    if use_cap and any(c > 1+tol for c in cs):
        return False
    # recurrence
    if abs((c0 + c2) - K0*lam*c1) > 1e-7: return False
    if abs((c1 + c3) - K1*lam*c2) > 1e-7: return False
    # floor consistency: K_n = floor((1+c_n)/(lam c_{n+1}))  -- equivalently
    #   K_n*lam*c_{n+1} <= 1+c_n < (K_n+1)*lam*c_{n+1}
    for n,(cn,cn1,Kn) in enumerate([(c0,c1,K0),(c1,c2,K1)]):
        if not (Kn*lam*cn1 - 1e-7 <= 1+cn < (Kn+1)*lam*cn1 + 1e-7):
            return False
    # edges on every consecutive pair
    pairs = [(c0,c1),(c1,c2),(c2,c3)]
    for (cn,cn1) in pairs:
        if use_edge_reg and not (cn + lam*cn1 > 1 - tol):   # c_n + lam c_{n+1} > 1
            return False
        if use_edge_gen and not (lam*cn + cn1 > 1 - tol):   # lam c_n + c_{n+1} > 1 (genuine edge)
            return False
    return True

def scan_combo(K0, K1, N=140, **flags):
    """Grid over (c0,c1): the recurrence fixes c2=K0 lam c1 - c0, c3=K1 lam c2 - c1.
       Return min over feasible of max(P0,P1,P2), the argmin, count below-thr-feasible."""
    best = None; arg=None; n_all_below=0; n_feas=0
    for i in range(1, N):
        c0 = i/N
        for j in range(1, N):
            c1 = j/N
            c2 = K0*lam*c1 - c0
            c3 = K1*lam*c2 - c1
            if not feasible(c0,c1,c2,c3,K0,K1,**flags):
                continue
            n_feas += 1
            P = [c0*c1, c1*c2, c2*c3]
            m = max(P)
            if best is None or m < best:
                best = m; arg=(c0,c1,c2,c3,P)
            if all(p < thr-1e-12 for p in P):
                n_all_below += 1
    return best, arg, n_all_below, n_feas

def genuine_run_check():
    """Longest below-thr run over GENUINE orbits (full 2D map), q=6."""
    x={-1:0.0,0:1.0}
    for i in range(1,10): x[i]=lam*x[i-1]-x[i-2]
    def Lf(a,b,j): return a*x[j]+b*x[j-1]
    def branch(a,b,eps=1e-9):
        for i in range(2,6):
            if Lf(a,b,i-1)>1-eps and Lf(a,b,i)<=1+eps: return i
        return None
    def inT(a,b,e=1e-9): return (1e-12<a<=1+e) and (1-lam*a-e<b<=1+e)
    def step(a,b):
        i=branch(a,b)
        if i is None: return None
        Li=Lf(a,b,i); Li1=Lf(a,b,i+1)
        if lam*Li<=1e-13: return None
        k=math.floor((1-Li1)/(lam*Li))
        return (Li,Li1+k*lam*Li),i,k
    def Pval(a,b,i): return a*Lf(a,b,i)/x[i-1]
    best=0
    N=200
    for ia in range(1,N):
        a=ia/N; blo=1-lam*a
        for ib in range(0,N+1):
            b=blo+(1.0-blo)*ib/N
            if not inT(a,b): continue
            cur=0
            aa,bb=a,b
            for _ in range(120):
                if not inT(aa,bb): break
                r=step(aa,bb)
                if r is None: break
                (na,nb),i,k=r
                p=Pval(aa,bb,i)
                if p<thr-1e-11: cur+=1; best=max(best,cur)
                else: cur=0
                aa,bb=na,nb
    return best

if __name__=="__main__":
    print(f"q=6  lam=sqrt3={lam:.10f}  thr=1/lam^3={thr:.10f}  (NOTE: =sqrt3/9, NOT sqrt3/6)")
    print("="*78)
    grun = genuine_run_check()
    print(f"GENUINE longest below-thr run = {grun}  => window W = {grun+1} (expect run=2,W=3)")
    print("="*78)
    print("LOCAL window-3 lemma truth test (min over feasible of max(P0,P1,P2)):")
    print("Floor words K0,K1 in 1..4.  margin = minmax - thr.  ALLBELOW must be 0.\n")
    print(f"{'K0,K1':>6} | {'BOTH edges+cap':>22} | {'no-gen-edge':>14} | {'no-cap':>12}")
    worst=None
    for K0,K1 in itertools.product(range(1,5),repeat=2):
        b1,a1,nb1,nf1 = scan_combo(K0,K1, use_cap=True, use_edge_gen=True, use_edge_reg=True)
        b2,_,nb2,_ = scan_combo(K0,K1, use_cap=True, use_edge_gen=False, use_edge_reg=True)
        b3,_,nb3,_ = scan_combo(K0,K1, use_cap=False, use_edge_gen=True, use_edge_reg=True)
        def fmt(b,nb,nf):
            if b is None: return "infeasible"
            return f"{b:.5f}(m{b-thr:+.4f},#{nb})"
        print(f"{K0},{K1:>3} | {fmt(b1,nb1,nf1):>22} | {fmt(b2,nb2,0):>14} | {fmt(b3,nb3,0):>12}")
        if b1 is not None and nf1>0:
            if worst is None or b1<worst[0]:
                worst=(b1,K0,K1,a1,nb1)
    print("\nWORST (tightest) floor word with BOTH edges + cap:")
    if worst:
        b,K0,K1,arg,nb=worst
        print(f"  K=({K0},{K1})  minmax={b:.6f}  margin={b-thr:+.6f}  allbelow_count={nb}")
        if arg:
            c0,c1,c2,c3,P=arg
            print(f"  argmin c=({c0:.4f},{c1:.4f},{c2:.4f},{c3:.4f})  P={[round(p,4) for p in P]}")
    print("\nVERDICT: window-3 lemma TRUE iff every (K0,K1) shows margin>0 AND allbelow #=0")
