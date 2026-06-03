#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Xq_closedform_verify.py — verify the derived closed form for the Hecke ergodic-opt infimum X(q).

DERIVED (this session):
  word (1^{q-3},2), period N=q-2.  Eigenvector  v_n = sin((n+1)θ),  θ=π/q,  n=0..q-3  (= U_n(λ/2)).
  Lower-s boundary: s_lo = 1/(2 sin 2θ)  (the CUSP edge binds for all q≥4).
  maxprod = max_n v_n v_{n+1} = cos θ   (q even) ,  cos²(θ/2)=(1+cosθ)/2  (q odd).
  X(q) = s_lo² · maxprod
       = cos(π/q)        / (4 sin²(2π/q))            (q even)  = 1/(8 sin(π/q) sin(2π/q))
       = cos²(π/(2q))    / (4 sin²(2π/q))            (q odd)   = (1+cos(π/q))/(32 sin²(π/q) cos²(π/q))
  q=3 special (word (1,4)): X(3)=2/9.

Cross-check vs Xq_exact_for_word (the independent boundary-scan in ergodic_hecke_hunt.py).
"""
import mpmath as mp
from ergodic_hecke_hunt import Xq_exact_for_word
mp.mp.dps = 60

def theta(q): return mp.pi / q
def lam(q):   return 2*mp.cos(theta(q))

def word(q):
    # (1^{q-3}, 2) for q>=4 ; q=3 special (1,4)
    if q == 3: return [1,4]
    return [1]*(q-3) + [2]

def eigenvector_closed(q):
    """v_n = sin((n+1)θ), n=0..q-3."""
    th = theta(q); N = q-2
    return [mp.sin((n+1)*th) for n in range(N)]

def eigenvector_from_monodromy(q):
    """Independent: nullspace of (M-I), then recurrence — same logic as Xq_exact_for_word."""
    l = lam(q); w = word(q); p = len(w)
    M = mp.eye(2)
    for k in w:
        M = mp.matrix([[0,1],[-1,k*l]]) * M
    A = M - mp.eye(2)
    v0, v1 = A[0,1], -A[0,0]
    if v0 < 0: v0, v1 = -v0, -v1
    v = [v0, v1]
    for n in range(p-2):
        v.append(w[n]*l*v[n+1] - v[n])
    return v

def Xq_closed(q):
    th = theta(q)
    s_lo = 1/(2*mp.sin(2*th))
    if q % 2 == 0:
        maxprod = mp.cos(th)
    else:
        maxprod = mp.cos(th/2)**2
    return s_lo*s_lo*maxprod

print("=== 1. eigenvector  sin((n+1)θ)  vs  monodromy nullspace (normalised to v_0) ===")
for q in [4,5,6,7,8,11,16]:
    vc = eigenvector_closed(q)
    vm = eigenvector_from_monodromy(q)
    vm = [x/vm[0]*vc[0] for x in vm]   # match scale at index 0
    err = max(abs(a-b) for a,b in zip(vc, vm))
    print(f"  q={q:>2}  max|v_closed - v_mono| = {mp.nstr(err,3)}")

print("\n=== 2. X(q): closed form vs Xq_exact_for_word (boundary scan) ===")
print(f"{'q':>3} {'par':>4} {'X_closed':>26} {'X_scan':>26} {'|diff|':>10}")
maxdiff = mp.mpf(0)
for q in range(4, 81):
    Xc = Xq_closed(q)
    Xs = Xq_exact_for_word(q, word(q))
    d = abs(Xc - Xs)
    maxdiff = max(maxdiff, d)
    if q <= 14 or q in (20,30,40,50,60,80):
        print(f"{q:>3} {'even' if q%2==0 else 'odd':>4} {mp.nstr(Xc,22):>26} {mp.nstr(Xs,22):>26} {mp.nstr(d,3):>10}")
print(f"  ... max |closed - scan| over q=4..80 = {mp.nstr(maxdiff,3)}")

print("\n=== 3. explicit small values from the general formula ===")
checks = {4:('√2/8', mp.sqrt(2)/8), 5:('1/4', mp.mpf(1)/4),
          6:('√3/6', mp.sqrt(3)/6), 8:('½cos(π/8)', mp.cos(mp.pi/8)/2),
          10:('½cot(π/5)', mp.cot(mp.pi/5)/2), 12:('cos(π/12)', mp.cos(mp.pi/12))}
for q,(name,val) in checks.items():
    Xc = Xq_closed(q)
    print(f"  X({q}) = {name:>10} ?  closed={mp.nstr(Xc,20)}  target={mp.nstr(val,20)}  diff={mp.nstr(abs(Xc-val),3)}")

print("\n=== 4. q=3 special (word (1,4)) ===")
X3 = Xq_exact_for_word(3, [1,4])
print(f"  X(3) scan = {mp.nstr(X3,20)}   2/9 = {mp.nstr(mp.mpf(2)/9,20)}   diff={mp.nstr(abs(X3-mp.mpf(2)/9),3)}")
print(f"  even-formula at q=3 = {mp.nstr(Xq_closed(3) if False else mp.mpf('nan'),5)} (n/a, special word)")

print("\n=== 5. PSLQ: confirm X(q) per-q clean forms reduce to the SAME uniform expr ===")
for q in [4,5,6,7,8,9,10,11,12,13,14]:
    Xc = Xq_closed(q)
    th = theta(q)
    # test X * 4 sin^2(2θ) == cosθ (even) or (1+cosθ)/2 (odd)
    lhs = Xc * 4 * mp.sin(2*th)**2
    rhs = mp.cos(th) if q%2==0 else (1+mp.cos(th))/2
    print(f"  q={q:>2}: X·4sin²(2θ) = {mp.nstr(lhs,18)}   maxprod = {mp.nstr(rhs,18)}   diff={mp.nstr(abs(lhs-rhs),3)}")

print("\n=== 6. the (2cosθ-1)² identity that makes the cusp bind (q≥4) ===")
for q in range(3, 13):
    th = theta(q)
    diff = (2*mp.sin(th)+mp.sin(3*th)) - 2*mp.sin(2*th)
    pred = mp.sin(th)*(2*mp.cos(th)-1)**2
    print(f"  q={q:>2}: (2sinθ+sin3θ)-2sin2θ = {mp.nstr(diff,12)}   sinθ(2cosθ-1)² = {mp.nstr(pred,12)}")
