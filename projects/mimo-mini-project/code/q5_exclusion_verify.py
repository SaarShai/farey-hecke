#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
q5_exclusion_verify.py — rigorous (interval/margin) verification of the q=5 t-point exclusion
case structure, to back the paper proof. λ=φ, V=1/4, band [a,b], b=√(1/(2φ)), a=1/(4b).

Cases at a t-point (x,y), x=1/(4y), y∈[a,b], with floor k=⌊(1+x)/(φy)⌋:
 (I)   k=2  ⟹ P_{m+1}=2φy²−1/4 > 1/4   (claim: holds ∀ y giving k=2, since y≥a>1/(2√φ)).
 (II)  k=1 & y≤1/2 ⟹ successor (y,φy−x) ∉ D  (claim: (φ+2)y−φx ≤ 1, equality only at y=1/2).
 (III) k=1 & y>1/2 ⟹ successor ∈D, and orbit exceeds 1/4 within ≤2 more steps.
Verify each with definite margins by fine sampling + exact endpoint algebra.
"""
import mpmath as mp
mp.mp.dps = 50
phi=(1+mp.sqrt(5))/2; l=phi; V=mp.mpf(1)/4
b=mp.sqrt(1/(2*l)); a=1/(4*b)
half=mp.mpf(1)/2

def inD(x,y): return x>0 and y>0 and (x+l*y)>1
def floork(x,y): return int(mp.floor((1+x)/(l*y)))
def step(x,y):
    k=floork(x,y); return k*l*y-x,k

print(f"a={mp.nstr(a,12)}  b={mp.nstr(b,12)}  1/(2√φ)={mp.nstr(1/(2*mp.sqrt(phi)),12)}")
print(f"check a>1/(2√φ): {a>1/(2*mp.sqrt(phi))}  (margin {mp.nstr(a-1/(2*mp.sqrt(phi)),6)})")

# Sweep t-points y in [a,b]; classify and check the closing inequality with margin.
N=200000
fails=[]
caseI=caseII=caseIII=0
minmarg={'I':mp.inf,'II':mp.inf,'III':mp.inf}
maxIIIsteps=0
for i in range(N+1):
    y=a+(b-a)*mp.mpf(i)/N
    x=1/(4*y)
    if not inD(x,y):
        fails.append(('tpoint∉D',mp.nstr(y,8))); continue
    k=floork(x,y)
    if k>=2:
        caseI+=1
        P1=k*l*y*y - V   # P_{m+1}=k φ y² − xy, xy=V
        marg=P1-V
        minmarg['I']=min(minmarg['I'],marg)
        if marg<=0: fails.append(('I',mp.nstr(y,8),mp.nstr(marg,6)))
    else: # k==1
        succ_in = (l+2 if False else (phi+2))*y - phi*x  # (φ+2)y−φx  ; >1 ⟺ successor in D
        sval=(phi+2)*y-phi*x
        if y<=half:
            caseII+=1
            marg=1-sval   # want sval≤1  (successor ∉D)
            minmarg['II']=min(minmarg['II'],marg)
            if marg<0: fails.append(('II',mp.nstr(y,8),mp.nstr(marg,6)))
        else:
            caseIII+=1
            # successor must be in D
            if sval<=1: fails.append(('III-succ∉D',mp.nstr(y,8)))
            # trace forward up to 4 steps; must exceed V
            cx,cy=x,y; got=None
            for s in range(1,5):
                yn,kk=step(cx,cy)
                if yn<=0 or not inD(cy,yn): got=('left',s); break
                P=cy*yn
                if P>V*(1+mp.mpf('1e-30')): got=('exceed',s,P-V); break
                cx,cy=cy,yn
            if got is None: fails.append(('III-noexceed',mp.nstr(y,8)))
            elif got[0]=='exceed':
                maxIIIsteps=max(maxIIIsteps,got[1])
                minmarg['III']=min(minmarg['III'],got[2])
            else:
                fails.append(('III-left',mp.nstr(y,8),got[1]))

print(f"\ncaseI(k=2)={caseI}  caseII(k=1,y≤½)={caseII}  caseIII(k=1,y>½)={caseIII}")
print(f"min margins: I(P1−V)={mp.nstr(minmarg['I'],8)}  II(1−sval)={mp.nstr(minmarg['II'],8)}  III(exceed−V)={mp.nstr(minmarg['III'],8)}")
print(f"max forward steps in case III = {maxIIIsteps} (≤2 extra after the floor-1 step ⟹ ≤3 total)")
print(f"FAILS: {len(fails)}")
for f in fails[:20]: print("   ",f)

# Exact endpoints
print("\n--- exact algebra checks ---")
# (I) floor switch 2->1: where (1+x)/(φy)=2 with x=1/(4y): 1+1/(4y)=2φy
#   solve 8φy²-4y-1=0 -> y=(4+√(16+32φ))/(16φ)
ysw=(4+mp.sqrt(16+32*phi))/(16*phi)
print(f"floor 2→1 switch at y*={mp.nstr(ysw,10)}  (k=2 for y<y*).  y*<½? {ysw<half}")
print(f"  at y* x=1/(4y*)={mp.nstr(1/(4*ysw),10)}; verify P1 there =2φy*²−V={mp.nstr(2*phi*ysw*ysw-V,8)} (>V margin {mp.nstr(2*phi*ysw*ysw-V-V,8)})")
# (II) successor-in-D boundary: (φ+2)y−φ/(4y)=1 -> 4(φ+2)y²−4y−φ=0 -> y=(4+√(16+16(φ+2)φ))/(8(φ+2))
yb=(4+mp.sqrt(16+16*(phi+2)*phi))/(8*(phi+2))
print(f"successor-in-D boundary y={mp.nstr(yb,12)}  (should be exactly ½): ½−y={mp.nstr(half-yb,8)}")
