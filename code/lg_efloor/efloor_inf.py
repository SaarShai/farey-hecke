"""
Numeric verification that  inf_{Dcorr ∩ k=1-bracket} Eform  >=  EfloorQ,
uniformly in q = m+2 >= 3.

Sealed defs (from hsa_realization_lean / hsa_unconditional_lean):
  l = lamq q = 2 cos(pi/q),   theta = pi/q,  c = cos theta = l/2,  s = sin theta
  Eform(a,b) = a^2 - l a b + b^2
  Dcorr = {0<a<=1, 0<b<=1, a+l b>1, l a+b>1}
  k=1 floor bracket (isK1):  l b <= 1+a  AND  1+a < 2 l b
  alphaC l = (l^2+2)/(l(4-l^2))
  rhoC   l = 2 sqrt(2 l^2+1)/(l(4-l^2))
  EfloorQ = 1/(l^3 (alphaC + rhoC * c))      [since cos(pi/q)=l/2=c]

We minimize Eform over the closed region (Dcorr-closure ∩ bracket) and compare to EfloorQ.
High-dps grid + corner/edge analysis.
"""
import mpmath as mp
mp.mp.dps = 50

def lamq(q):
    return 2*mp.cos(mp.pi/q)

def alphaC(l):
    return (l**2+2)/(l*(4-l**2))

def rhoC(l):
    return 2*mp.sqrt(2*l**2+1)/(l*(4-l**2))

def EfloorQ(l, q):
    c = mp.cos(mp.pi/q)
    return 1/(l**3*(alphaC(l)+rhoC(l)*c))

def Eform(l,a,b):
    return a**2 - l*a*b + b**2

def in_region(l,a,b):
    if not (0 < a <= 1): return False
    if not (0 < b <= 1): return False
    if not (a + l*b > 1): return False
    if not (l*a + b > 1): return False
    # k=1 bracket
    if not (l*b <= 1+a): return False
    if not (1+a < 2*l*b): return False
    return True

def min_Eform_grid(q, N=400):
    l = lamq(q)
    ef = EfloorQ(l,q)
    best = None; bestpt=None
    for i in range(N+1):
        a = mp.mpf(i)/N
        if a<=0: continue
        for j in range(N+1):
            b = mp.mpf(j)/N
            if b<=0: continue
            if in_region(l,a,b):
                e = Eform(l,a,b)
                if best is None or e<best:
                    best=e; bestpt=(a,b)
    return l, ef, best, bestpt

print(f"{'q':>4} {'l':>10} {'EfloorQ':>16} {'minE(grid)':>16} {'minE-EfloorQ':>16} {'ratio':>10}")
for q in list(range(3,40)) + [50,80,120,200,500,1000]:
    l, ef, best, pt = min_Eform_grid(q, N=300)
    if best is None:
        print(f"{q:>4} {float(l):>10.5f}  region EMPTY on grid (refine)")
        continue
    diff = best-ef
    ratio = best/ef
    flag = "  <-- VIOLATION" if diff<0 else ""
    print(f"{q:>4} {float(l):>10.6f} {float(ef):>16.10f} {float(best):>16.10f} {float(diff):>16.3e} {float(ratio):>10.6f}{flag}")
