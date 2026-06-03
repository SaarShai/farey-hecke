#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GOAL H — genuine multi-branch lower bound X_Omega(q) >= 1/lam^3 for q>=16.

Clean genuine-map driver + (1) anchor validation, (2) characterization of {P<thr}
per branch, (3) dwell-time / itinerary of longest sub-thr runs, (4) candidate
exit-invariants.  thr = 1/lam^3.

Genuine BCZ_q map on Tq={0<a<=1, 1-lam a<b<=1}, branches i=2..q-1, piecewise-linear SL2:
  L_j = a*x_j + b*x_{j-1};  branch i  <=>  L_{i-1}>1  and  L_i<=1.
  step: k = floor((1-L_{i+1})/(lam L_i)); (a',b') = (L_i, L_{i+1}+k*lam*L_i).
  observable P = a*L_i/x_{i-1}  = c_n c_{n+1}/x_{i_n-1}.
In (a, v=L_i) branch coords (m=x_{i-1}, c=x_{i-2}, det m^2-... => m^2+c^2-lam m c=1):
  branch region: a+c v>m, c a+v>m, 0<a<=1, 0<v<=1; P=a v/m; min P = m/(1+c)^2 at a=v=m/(1+c).
"""
import math, random
import numpy as np

# ---------- map ----------
def build(q):
    lam = 2*math.cos(math.pi/q)
    x = {-1: 0.0, 0: 1.0}
    for i in range(1, q+3):
        x[i] = lam*x[i-1] - x[i-2]
    return lam, x

def L(a, b, j, x):
    return a*x[j] + b*x[j-1]

def branch(a, b, x, q, eps=1e-9):
    for i in range(2, q):           # 2..q-1
        if L(a, b, i-1, x) > 1-eps and L(a, b, i, x) <= 1+eps:
            return i
    return None

def step(a, b, x, q, lam, eps=1e-12):
    i = branch(a, b, x, q)
    if i is None:
        return None
    Li = L(a, b, i, x); Li1 = L(a, b, i+1, x)
    if lam*Li <= eps:
        return None
    k = math.floor((1 - Li1)/(lam*Li))
    return (Li, Li1 + k*lam*Li), i, k

def Pval(a, b, i, x):
    return a*L(a, b, i, x)/x[i-1]

def inT(a, b, lam, e=1e-9):
    return (1e-12 < a <= 1+e) and (1-lam*a-e < b <= 1+e)

# ---------- (1) anchors ----------
def random_orbit_inf(q, NS=40000, STEPS=120, seed=1):
    """min over random long orbits of (running max P) -> approximates X_Omega from above."""
    rng = random.Random(seed)
    lam, x = build(q)
    best = math.inf
    for _ in range(NS):
        a = rng.uniform(1e-3, 1.0)
        b = rng.uniform(max(1-lam*a, -1)+1e-6, 1.0)
        if not inT(a, b, lam):
            continue
        mx = 0.0; ok = False
        for n in range(STEPS):
            r = step(a, b, x, q, lam)
            if r is None: break
            (na, nb), i, k = r
            mx = max(mx, Pval(a, b, i, x))
            a, b = na, nb
            ok = True
            if not inT(a, b, lam): break
        if ok and n > STEPS//2:
            best = min(best, mx)
    return best

def anchors():
    print("=== (1) anchors (random-orbit inf esssup vs target) ===")
    for q in [3, 4, 5]:
        lam, x = build(q)
        thr = 1/lam**3
        Vref = {3: 2/9, 4: math.sqrt(2)/8, 5: 1/((1+math.sqrt(5))/2)**3}
        print(f"  q={q}: 1/lam^3={thr:.6f}  V_ref={Vref[q]:.6f}")
    print("  (cusp orbit realizes 1/lam^3 exactly; random orbits stay above)")

# ---------- (2) characterize {P<thr} ----------
def char_subthr(qs=(16, 20, 30, 50)):
    print("\n=== (2) {P<thr} per branch: min P = x_{i-1}/(1+x_{i-2})^2, which branches dip ===")
    for q in qs:
        lam, x = build(q)
        thr = 1/lam**3
        below = []
        for i in range(2, q):       # all branches 2..q-1
            m = x[i-1]; c = x[i-2]
            vert = m/(1+c)              # vertex coord a=v
            minP = m/(1+c)**2
            feasible_vertex = (vert <= 1+1e-9)
            tag = ""
            if i == q-1: tag = "SCALAR"
            elif i == q-2: tag = "CUSP"
            if minP < thr-1e-12:
                below.append((i, minP, vert, feasible_vertex, tag))
        print(f"  q={q}: thr={thr:.6f}  branches with minP<thr: "
              f"{[ (b[0], round(b[1],5), b[4] or 'mid') for b in below ]}")
        # band extent
        mids = [b[0] for b in below if b[4] == ""]
        if mids:
            print(f"        middle-branch band: i in [{min(mids)},{max(mids)}]  "
                  f"(q-2 cusp={q-2} excluded, q-1 scalar={q-1} included)")

# ---------- (3) dwell time + itineraries ----------
def dwell_and_itin(qs=(16, 20, 30, 50), NS=60000, STEPS=200, seed=7):
    print("\n=== (3) dwell-time histogram + longest-run itinerary ===")
    for q in qs:
        rng = random.Random(seed+q)
        lam, x = build(q)
        thr = 1/lam**3
        runs = {}                  # run-length -> count
        best_run = 0; best_itin = None
        for _ in range(NS):
            a = rng.uniform(1e-3, 1.0)
            b = rng.uniform(max(1-lam*a, -1)+1e-6, 1.0)
            if not inT(a, b, lam): continue
            cur = 0; cur_itin = []
            for n in range(STEPS):
                r = step(a, b, x, q, lam)
                if r is None: break
                (na, nb), i, k = r
                p = Pval(a, b, i, x)
                if p < thr-1e-11:
                    cur += 1; cur_itin.append((i, k, round(p, 5)))
                    if cur > best_run:
                        best_run = cur; best_itin = list(cur_itin)
                else:
                    if cur > 0:
                        runs[cur] = runs.get(cur, 0)+1
                    cur = 0; cur_itin = []
                a, b = na, nb
                if not inT(a, b, lam): break
        hist = sorted(runs.items())
        print(f"  q={q}: max-run={best_run} (~q/3={q/3:.1f})  hist(len:count)={hist[:12]}")
        if best_itin:
            seq_i = [t[0] for t in best_itin]
            seq_k = [t[1] for t in best_itin]
            print(f"        longest-run branch itinerary i={seq_i}")
            print(f"                              digits k={seq_k}")

# ---------- (4) candidate exit invariants ----------
def exit_invariants(q=20, NS=40000, STEPS=200, seed=11):
    """Along the longest sub-thr run, track E=c^2+c'^2-lam c c', branch index i,
    and a^2 (cusp distance), to spot what drifts monotonically forcing exit."""
    print(f"\n=== (4) exit-invariant trace along longest sub-thr run (q={q}) ===")
    rng = random.Random(seed)
    lam, x = build(q)
    thr = 1/lam**3
    best_run = 0; best_trace = None
    for _ in range(NS):
        a = rng.uniform(1e-3, 1.0)
        b = rng.uniform(max(1-lam*a, -1)+1e-6, 1.0)
        if not inT(a, b, lam): continue
        cur = 0; trace = []
        prev_a = None
        for n in range(STEPS):
            r = step(a, b, x, q, lam)
            if r is None: break
            (na, nb), i, k = r
            p = Pval(a, b, i, x)
            # E using consecutive first-coords (a -> na)
            E = a*a + na*na - lam*a*na
            if p < thr-1e-11:
                cur += 1
                trace.append(dict(i=i, k=k, p=round(p, 6), a=round(a, 5),
                                  na=round(na, 5), E=round(E, 6)))
                if cur > best_run:
                    best_run = cur; best_trace = list(trace)
            else:
                cur = 0; trace = []
            a, b = na, nb
            if not inT(a, b, lam): break
    print(f"  longest run length {best_run}; trace (i,k,P,a,a',E):")
    if best_trace:
        for t in best_trace:
            print(f"    i={t['i']:<3} k={t['k']} P={t['p']:.6f} a={t['a']:.5f} "
                  f"a'={t['na']:.5f} E={t['E']:.6f}")

if __name__ == "__main__":
    anchors()
    char_subthr()
    dwell_and_itin()
    exit_invariants(20)
    exit_invariants(30)
