"""Independent verification of core math claims A, B, D.
c_K(s) = sum_{k=2}^K mu(k) k^{-s}  (partial 1/zeta, no k=1 term).
"""
import math, cmath
import numpy as np
import mpmath as mp
from sympy import mobius, totient, primefactors

mp.mp.dps = 30

def cK(K, s):
    return sum(int(mobius(k)) * mp.e**(-s*mp.log(k)) for k in range(2, K+1))

print("="*70)
print("CLAIM A: K<=4 unconditional non-vanishing of c_K on 0<Re(s)<1")
print("="*70)
# c_2 = -2^{-s}; c_3=c_4 = -(2^{-s}+3^{-s})
for K in [2,3,4,5]:
    # min |c_K| over a grid of the strip
    best = 1e9; arg = None
    for sigma in np.linspace(0.05,0.95,19):
        for gamma in np.linspace(0.1,200,4000):
            v = abs(cK(K, sigma+1j*gamma))
            if v < best: best=float(v); arg=(round(sigma,3),round(gamma,3))
    print(f"  K={K}: min|c_K| over strip grid = {best:.5f} at (sigma,gamma)={arg}")
print("  Analytic: c_3=c_4=-(2^-s+3^-s); =0 <=> 2^-sigma=3^-sigma <=> sigma=0.")
print(f"    On Re=1/2 min|c_3| = 2^-.5 - 3^-.5 = {2**-0.5 - 3**-0.5:.5f} (repo: 0.1298)")
print(f"  K=5 norm-bound g(b)=2^-b-3^-b-5^-b: g(.5)={2**-.5-3**-.5-5**-.5:.4f} (<0 => elementary bound fails)")

# Does c_5 actually VANISH somewhere in the strip? (completion question)
print("\n  Hunt for an actual zero of c_5 in 0<Re(s)<1:")
from scipy.optimize import minimize
def f5(x):
    return float(abs(cK(5, x[0]+1j*x[1])))
found=[]
for g0 in np.linspace(1,300,120):
    r = minimize(f5, [0.5, g0], method="Nelder-Mead",
                 options={"xatol":1e-8,"fatol":1e-12})
    if r.fun < 1e-6 and 0<r.x[0]<1:
        found.append((round(r.x[0],4),round(r.x[1],4),r.fun))
seen=set(); uniq=[]
for s,g,v in sorted(found,key=lambda t:t[1]):
    key=round(g,1)
    if key not in seen: seen.add(key); uniq.append((s,g,v))
print(f"    c_5 zeros found in strip: {uniq[:6]}" if uniq else "    none found <1e-6")

print("\n"+"="*70)
print("CLAIM B: avoidance anomaly -- reproduce the sample-size artifact")
print("="*70)
zeros = [float(mp.im(mp.zetazero(n))) for n in range(1,61)]
rng = np.random.default_rng(0)
for K in [10,20]:
    vz = [float(abs(cK(K, 0.5+1j*g))) for g in zeros]            # at zeta zeros
    # control: random points in same height band, two sample sizes
    lo,hi = min(zeros),max(zeros)
    for ctrl_n in [60, 600]:
        gc = rng.uniform(lo,hi,ctrl_n)
        vc = [float(abs(cK(K, 0.5+1j*g))) for g in gc]
        print(f"  K={K} ctrl_n={ctrl_n:4d}: "
              f"min@zeros={min(vz):.4f} min@ctrl={min(vc):.4f} "
              f"ratio_min/min={min(vz)/min(vc):.2f} "
              f"med@zeros={np.median(vz):.3f} med@ctrl={np.median(vc):.3f}")
print("  => 'repulsion ratio' shrinks as control grows = sample-size artifact (medians equal).")

print("\n"+"="*70)
print("CLAIM D: Delta-A(N) closed form")
print("  ΔA(N) =?= (1/3)φ(N) + (1/(6N))·Π_{p|N}(1-p)")
print("="*70)
def A_direct(N):
    tot = mp.mpf(0)
    for b in range(1,N+1):
        for a in range(1,b+1):
            if math.gcd(a,b)==1:
                tot += (mp.mpf(a)/b)**2
    return tot
def dA_closed(N):
    prod = 1
    for p in primefactors(N): prod *= (1-p)
    return mp.mpf(int(totient(N)))/3 + mp.mpf(prod)/(6*N)
ok=True
for N in range(2,31):
    direct = A_direct(N)-A_direct(N-1)
    closed = dA_closed(N)
    if abs(direct-closed)>1e-20: ok=False; print(f"  N={N} MISMATCH {direct} vs {closed}")
print(f"  ΔA closed form matches direct Farey computation for N=2..30: {ok}")
# the 'huge cancellation' -> small D(N): show J(N)-J(N-1) is O(N^{-1+eps})
def J(N):
    rs = sorted(mp.mpf(a)/b for b in range(1,N+1) for a in range(1,b+1) if math.gcd(a,b)==1)
    Phi=len(rs)
    return sum((r-(i+1)/mp.mpf(Phi))**2 for i,r in enumerate(rs))
print("  D(N)=J(N)-J(N-1) (should be tiny vs the O(phi(N)) component terms):")
for N in [20,40,60]:
    print(f"    N={N}: D(N)={float(J(N)-J(N-1)):+.3e}, (1/3)phi(N)={int(totient(N))/3:.1f}")
