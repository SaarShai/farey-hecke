#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Xq_cluster_crosscheck.py — INDEPENDENT cross-check of goal #7's cluster-law claim
  C(3)=2, C(4)=2, C(5)=3, C(6)=5  (longest run of consecutive products P_n=x_n y_n
  strictly below X(q) along a recurrent T_q orbit; 3-window floor is q=3,4-special).

Self-contained. Does NOT import #7's Xq_recurrent_window_test.py. Re-derives the map
from the definition and uses the recurrent-TAIL method (burn-in, then measure on the
settled tail; reseed on domain-escape). VALIDATION ANCHOR: must reproduce the PROVEN
q=3,4 bound maxRun=2 (3-window floor holds). If it does, the q>=5 read-out is trusted.
"""
import math, random

def Xq(q):
    t = math.pi/q
    if q == 3: return 2/9
    if q % 2 == 0: return math.cos(t)/(4*math.sin(2*t)**2)
    return math.cos(t/2)**2/(4*math.sin(2*t)**2)

def run_orbit(q, n_steps, seed):
    """Iterate T_q(x,y)=(y, floor((1+x)/(lam y))*lam y - x) on {x>0,y>0,x+lam y>1}.
    Return list of products P_n = x_n*y_n along the orbit (or None on immediate escape)."""
    rng = random.Random(seed)
    lam = 2*math.cos(math.pi/q)
    # seed inside the domain: pick x,y in (0,1], enforce x+lam*y>1
    for _try in range(200):
        x = rng.random(); y = rng.random()
        if x > 1e-9 and y > 1e-9 and x + lam*y > 1:
            break
    else:
        return None
    Ps = []
    for _ in range(n_steps):
        if not (x > 1e-12 and y > 1e-12 and x + lam*y > 1 - 1e-12):
            return Ps if len(Ps) > 50 else None      # escaped
        Ps.append(x*y)
        k = math.floor((1 + x)/(lam*y))
        z = k*lam*y - x
        x, y = y, z
        if abs(x) > 1e6 or abs(y) > 1e6:
            return Ps if len(Ps) > 50 else None
    return Ps

def longest_run_below(Ps, thr, eps=1e-9):
    best = cur = 0
    for p in Ps:
        if p < thr - eps:
            cur += 1; best = max(best, cur)
        else:
            cur = 0
    return best

def measure(q, n_steps=400000, burn_frac=0.3, n_seeds=8):
    X = Xq(q)
    maxrun_overall = 0
    tail_len_total = 0
    for s in range(n_seeds):
        Ps = run_orbit(q, n_steps, seed=1000*q + s)
        if not Ps or len(Ps) < 200:
            continue
        burn = int(len(Ps)*burn_frac)
        tail = Ps[burn:]
        tail_len_total += len(tail)
        maxrun_overall = max(maxrun_overall, longest_run_below(tail, X))
    return X, maxrun_overall, tail_len_total

if __name__ == "__main__":
    print("="*72)
    print("INDEPENDENT cluster cross-check  (recurrent-tail T_q sim)")
    print("C(q) = longest run of consecutive P_n < X(q) on the settled orbit tail.")
    print("="*72)
    expect = {3: 2, 4: 2, 5: 3, 6: 5}
    print(f"{'q':>2} {'X(q)':>10} {'C_meas':>7} {'#7 claim':>9} {'tail pts':>10}  status")
    anchor_ok = True
    rows = {}
    for q in (3, 4, 5, 6, 7):
        X, C, tail = measure(q)
        rows[q] = C
        exp = expect.get(q, '?')
        if q in (3, 4):
            ok = (C == 2)
            anchor_ok &= ok
            tag = "ANCHOR " + ("ok" if ok else "*** FAIL (proven=2) ***")
        else:
            tag = ("matches #7" if exp == C else f"DIFFERS (#7={exp})")
        print(f"{q:>2} {X:>10.6f} {C:>7d} {str(exp):>9} {tail:>10d}  {tag}")
    print("-"*72)
    if anchor_ok:
        print("ANCHOR PASS: method reproduces the PROVEN q=3,4 bound (maxRun=2).")
        m5 = "q=5 cluster=%d -> 3-window %s" % (rows[5], "HOLDS" if rows[5] < 3 else "FAILS (corroborates #7 correction)")
        print("  " + m5)
        print(f"  read-out: C(5)={rows[5]}, C(6)={rows[6]}, C(7)={rows[7]}  (genuine-point claim: 3,5,?)")
    else:
        print("ANCHOR FAIL: method does NOT reproduce proven q=3,4 — read-out NOT trusted.")
