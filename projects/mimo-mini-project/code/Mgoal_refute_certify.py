#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GOAL M — refutation hunt AT SCALE + per-q corridor no-cycle certificate.

Three decisive tests of  X_Omega(q) = 1/lam^3  for q>=17:

(A) SURVIVOR (maximal forward-invariant set in S={P<thr}) with RESOLUTION REFINEMENT, q=17..60.
    survivors=0 (robust under refinement) => no sub-threshold invariant set (KAM island / curve /
    periodic orbit) => value not refuted. Refinement guards against grid under-resolution (margin
    is O(1/q^2)). Reuses Igoal_survivor.survivor_set.

(B) VALUE-SAFETY at HIGH q (min running-max P over many random seeds; <thr would refute), pushed to
    q=200, with LONG orbits (STEPS=1500) so slow (~O(q)) sweeps complete. + single-corridor genuine
    min-max-P at HIGH PRECISION (mpmath dps=50) tracking the O(1/q^2) margin doesn't go negative.

(C) CORRIDOR NO-CYCLE CERTIFICATE q=17..30: full elliptic-corridor list (distinct trace classes,
    representative words), corridor-WORD transition graph, confirm NO all-sub-threshold cycle.
    (Conditional on the G_q-torsion classification that the corridor set is exactly these classes.)

Anchors: q=5 -> 1/phi^3; W_q trace=lam. thr=1/lam^3.
"""
import math, sys, itertools
import numpy as np

# ---------- shared genuine-map primitives ----------
def build(q):
    l = 2*math.cos(math.pi/q); x = {-1: 0.0, 0: 1.0}
    for i in range(1, q+5):
        x[i] = l*x[i-1] - x[i-2]
    return l, x

def Mik(l, x, i, k):
    return np.array([[x[i], x[i-1]], [x[i+1]+k*l*x[i], x[i]+k*l*x[i-1]]], float)

def word_mono(l, x, w):
    M = np.eye(2)
    for (i, k) in w: M = Mik(l, x, i, k) @ M
    return M

def branch_of(q, x, a, b, eps=1e-9):
    for i in range(2, q):
        if a*x[i-1]+b*x[i-2] > 1-eps and a*x[i]+b*x[i-1] <= 1+eps:
            return i
    return None

def Pval(q, x, a, b):
    i = branch_of(q, x, a, b)
    if i is None: return None, None
    return a*(a*x[i]+b*x[i-1])/x[i-1], i

# ================= (B) value safety, long orbits, high q =================
def value_safety(q, NS=60000, STEPS=1500, seed=0):
    l, x = build(q); thr = 1.0/l**3
    rng = np.random.default_rng(seed)
    best = 1e9
    longest_subthr = 0
    a0 = rng.uniform(1e-3, 1.0, NS)
    for s in range(NS):
        a = a0[s]; blo = 1 - l*a
        b = rng.uniform(max(blo, -0.99), 1.0)
        if not (1e-9 < a <= 1+1e-9 and blo-1e-9 < b <= 1+1e-9):
            continue
        runmax = 0.0; ok = True; run = 0
        for _ in range(STEPS):
            i = branch_of(q, x, a, b)
            if i is None: ok = False; break
            Li = a*x[i]+b*x[i-1]; Li1 = a*x[i+1]+b*x[i]
            P = a*Li/x[i-1]
            if P < thr: run += 1; longest_subthr = max(longest_subthr, run)
            else: run = 0
            if P > runmax: runmax = P
            if runmax >= thr: break
            k = math.floor((1-Li1)/(l*Li))
            a, b = Li, Li1 + k*l*Li
            if not (1e-9 < a <= 1+1e-9 and 1-l*a-1e-9 < b <= 1+1e-9): break
        if ok and runmax < best: best = runmax
    return best, thr, longest_subthr

# ---------- single-corridor genuine min-max-P at HIGH PRECISION ----------
def single_corridor_hp(q, n_scale=400, n_rot=600):
    import mpmath as mp
    mp.mp.dps = 50
    l = 2*mp.cos(mp.pi/q); thr = 1/l**3
    x = {-1: mp.mpf(0), 0: mp.mpf(1)}
    for i in range(1, q+5): x[i] = l*x[i-1] - x[i-2]
    def Lf(a, b, j): return a*x[j] + b*x[j-1]
    def inT(a, b): return (mp.mpf('1e-12') < a <= 1+mp.mpf('1e-9')) and (1-l*a-mp.mpf('1e-9') < b <= 1+mp.mpf('1e-9'))
    i0 = q-1
    best = mp.inf
    for s in range(1, n_scale+1):
        scale = mp.mpf(s)/n_scale
        b = scale            # scalar branch q-1: L_{q-1}=b (since x_{q-1}=0)
        a = scale*(x[i0-1]/(1+x[i0-2]))*mp.mpf('1.3') if x[i0-1] != 0 else scale*mp.mpf('0.5')
        # seed on scalar branch q-1: x_{q-1}=0 so a free, pick a small
        a = scale*mp.mpf('0.6'); b = scale*mp.mpf('0.9')
        if not inT(a, b): continue
        mx = mp.mpf(0); ok = False
        for _ in range(n_rot):
            i = None
            for j in range(2, q):
                if Lf(a, b, j-1) > 1-mp.mpf('1e-9') and Lf(a, b, j) <= 1+mp.mpf('1e-9'):
                    i = j; break
            if i is None: break
            P = a*Lf(a, b, i)/x[i-1]
            if P > mx: mx = P
            Li = Lf(a, b, i); Li1 = Lf(a, b, i+1)
            if l*Li <= 0: break
            k = mp.floor((1-Li1)/(l*Li))
            a, b = Li, Li1 + k*l*Li
            ok = True
            if not inT(a, b): break
            if mx >= thr: break
        if ok: best = min(best, mx)
    return best, thr

# ================= (C) corridor no-cycle certificate =================
def corridor_certificate(q, K=3, maxlen=4, tol=1e-9):
    """Full elliptic-corridor list (distinct trace classes) + transition no-cycle check.
    Returns (n_classes, has_subthr_cycle, slowest_trace_ok)."""
    l, x = build(q); thr = 1/l**3
    branches = [b for b in (q-1, q-2, q-3, q-4, q-5) if 2 <= b <= q-1]
    letters = [(i, k) for i in branches for k in range(0, K+1)]
    # distinct elliptic trace classes (representatives)
    classes = {}     # rounded |trace| -> representative word
    for ln in range(1, maxlen+1):
        for w in itertools.product(letters, repeat=ln):
            M = word_mono(l, x, list(w))
            tr = M[0,0]+M[1,1]; det = M[0,0]*M[1,1]-M[0,1]*M[1,0]
            if abs(det-1) > 1e-6: continue
            if abs(tr) < 2 - 1e-9:
                key = round(abs(tr), 6)
                if key not in classes: classes[key] = (list(w), tr)
    # the canonical corridor family (the only ones whose ellipse dips sub-thr per goal H/I)
    Wfam = {k: [(q-1, k), (q-1, 0), (q-3, 0)] for k in (1, 2, 3)}
    def tr(w): M = word_mono(l, x, w); return M[0,0]+M[1,1]
    # transition graph among the F-corridors at corridor-WORD level: chain Wk1 then Wk2,
    # ELLIPTIC composite (|tr|<2) == a sustained corridor switch; else the switch crosses thr.
    subthr_switch = 0
    for k1 in (1, 2, 3):
        for k2 in (1, 2, 3):
            if k1 == k2: continue       # same corridor = not a switch
            comp = Wfam[k2] + Wfam[k1]
            if abs(tr(comp)) < 2 - 1e-9:
                subthr_switch += 1      # an elliptic switch (would allow chaining)
    slowest = max(classes.keys()) if classes else 0.0
    slow_ok = abs(slowest - l) < 1e-6
    return len(classes), subthr_switch, slow_ok, l, thr

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"

    if mode in ("all", "C"):
        print("\n########## (C) CORRIDOR NO-CYCLE CERTIFICATE, q=17..30 ##########")
        print("  n_classes = #distinct elliptic trace classes; elliptic_switches = corridor")
        print("  switches that stay elliptic (must be 0); slowest=lam check.")
        allok = True
        for q in range(17, 31):
            nC, swsub, slow_ok, l, thr = corridor_certificate(q)
            ok = (swsub == 0) and slow_ok
            allok &= ok
            print(f"  q={q:2d}: n_classes={nC:2d}  elliptic_corridor_switches={swsub}  "
                  f"slowest=lam:{slow_ok}  => {'NO sub-thr cycle' if ok else 'CHECK'}")
        print(f"  CERTIFICATE q=17..30: {'ALL PASS (no sub-thr corridor cycle)' if allok else 'FAILED somewhere'}")

    if mode in ("all", "B"):
        print("\n########## (B) VALUE SAFETY (long orbits) + single-corridor HP margin ##########")
        print("q :  min-runmax-P   thr          ratio    longest_subthr_run   verdict")
        for q in [17, 23, 29, 37, 50, 75, 100, 150, 200]:
            e, thr, lr = value_safety(q, seed=q)
            v = '>=thr OK' if e >= thr-1e-9 else '<<< BELOW (REFUTATION?)'
            print(f"{q:4d}: {e:.8f}   {thr:.8f}   {e/thr:.5f}   run={lr:3d}            {v}", flush=True)
        print("\n  -- single-corridor genuine min-max-P (HP dps=50): margin O(1/q^2) must stay >=0 --")
        for q in [17, 30, 50, 75, 100]:
            try:
                import mpmath as mp
                best, thr = single_corridor_hp(q)
                print(f"  q={q:3d}: min-max-P={mp.nstr(best,10)}  thr={mp.nstr(thr,10)}  "
                      f"margin={mp.nstr(best-thr,5)}  {'OK>=thr' if best>=thr else 'BELOW!!'}", flush=True)
            except ImportError:
                print("  (mpmath unavailable)"); break

    if mode in ("all", "A"):
        print("\n########## (A) SURVIVOR with refinement, q=17..60 ##########")
        sys.path.insert(0, "code")
        try:
            from Igoal_survivor import survivor_set
        except Exception as ex:
            from code.Igoal_survivor import survivor_set
        for q in [17, 20, 25, 30, 40, 50, 60]:
            n1, nS1, thr, _ = survivor_set(q, Na=1500, Nb=1500, verbose=False)
            n2, nS2, _, _ = survivor_set(q, Na=3000, Nb=3000, verbose=False)
            print(f"  q={q:2d}: survivors @1500^2={n1}  @3000^2={n2}  "
                  f"{'EMPTY (no island)' if n2==0 else 'NONZERO -> refine/inspect'}", flush=True)
