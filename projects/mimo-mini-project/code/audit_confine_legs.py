#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_confine_legs.py — NUMERICAL adversary on the confinement legs of the
GENUINE Taha BCZ_q map, against the LEAN observable Pgen(a,b)=a*(a+l*b)/l and
threshold t=1/l^3.

GENUINE map (Taha, arXiv:1810.10668; see code/Bgoal_taha_genuine.py):
  U = T S = [[lam,-1],[1,0]], lam=2cos(pi/q).
  Ellipse vectors w_i = U^i (1,0)^T, w_0=(1,0), w_1=(lam,1), ..., w_{q-1}=(0,1).
  Domain Tq = { 0 < a <= 1, 1 - lam*a < b <= 1 }.
  Branch i in 2..q-1: (a,b).w_{i-1} > 1 and (a,b).w_i <= 1.
  Map on branch i:
     new_a = (a,b).w_i
     k     = floor( (1 - (a,b).w_{i+1}) / (lam*(a,b).w_i) )
     new_b = (a,b).w_{i+1} + k*lam*(a,b).w_i
  Branch labels: scalar = q-1, cusp = q-2, deep-mid = 2..q-3.

Lean observable:  Pgen(a,b) = a*(a + l*b)/l.   Threshold t = 1/l^3.

Legs tested empirically (many random orbits in Tq):
  (T) trichotomy: every in-domain step has branch i in {q-1}u{q-2}u{2..q-3};
      flag any step where branch_of returns None while (a,b) is in Tq.
  (C) cusp leg:    every step on i=q-2 has Pgen >= t.
  (D) deep-mid ejection (CRUX): every step on i in 2..q-3 with Pgen<t has its
      NEXT point with Pgen>=t.  Stats split by floor (k=1 vs k>=2).
  (E) sustained:   longest run of consecutive steps with Pgen<t.
"""
import math
import numpy as np

EPS = 1e-12

def build(q):
    """Return lam and ellipse vectors w_0..w_q as float pairs."""
    l = 2*math.cos(math.pi/q)
    U = np.array([[l, -1.0], [1.0, 0.0]])
    w = [np.array([1.0, 0.0])]
    for _ in range(q):
        w.append(U @ w[-1])
    return l, w  # w has length q+1, indices 0..q

def in_Tq(a, b, l, eps=1e-9):
    return (0 < a <= 1+eps) and (1 - l*a - eps < b <= 1+eps)

def branch_of(a, b, w, q, eps=EPS):
    """i in 2..q-1 with (a,b).w_{i-1}>1 and (a,b).w_i<=1; else None."""
    p = np.array([a, b])
    for i in range(2, q):
        ti_1 = p @ w[i-1]
        ti = p @ w[i]
        if ti_1 > 1 - eps and ti <= 1 + eps:
            return i
    return None

def genuine_step(a, b, w, q, l):
    """Return (new_a,new_b), i, k or (None,None,None)."""
    i = branch_of(a, b, w, q)
    if i is None:
        return None, None, None
    p = np.array([a, b])
    ti = p @ w[i]
    ti1 = p @ w[i+1]
    if l*ti <= 0:
        return None, i, None
    k = math.floor((1 - ti1) / (l * ti))
    new_a = ti
    new_b = ti1 + k * l * ti
    return (new_a, new_b), i, k

def Pgen(a, b, l):
    """Lean observable Pgen(a,b) = a*(a + l*b)/l."""
    return a * (a + l*b) / l

def audit_q(q, NS=3000, STEPS=400, seed=0):
    l, w = build(q)
    t = 1.0 / l**3
    rng = np.random.default_rng(seed)

    # counters
    steps_total = 0
    nobranch_in_Tq = 0            # (T) violation: None branch while in Tq
    nobranch_total = 0
    branch_offset_seen = set()    # q-i values observed

    cusp_steps = 0                # steps on i=q-2
    cusp_subthr = 0               # i=q-2 with Pgen<t  -> (C) violations
    cusp_worst = None             # worst (most sub-threshold) cusp violation

    # deep-mid (D)
    dm_subthr = 0                 # deep-mid steps with Pgen<t (have a next point)
    dm_hold = 0                   # of those, next has Pgen>=t  (leg holds)
    dm_fail = 0                   # of those, next has Pgen<t   (leg fails)
    dm_subthr_f0 = 0             # floor k==0
    dm_hold_f0 = 0
    dm_fail_f0 = 0
    dm_subthr_f1 = 0             # floor k==1
    dm_hold_f1 = 0
    dm_fail_f1 = 0
    dm_subthr_fk = 0            # floor k>=2
    dm_hold_fk = 0
    dm_fail_fk = 0
    dm_worst = None               # worst-margin deep-mid failure (any floor)
    dm_worst_f1 = None            # worst-margin deep-mid failure floor>=2
    floors_dm_subthr = set()

    longest_run = 0               # (E)
    longest_run_example = None

    for s in range(NS):
        a = float(rng.uniform(1e-3, 1.0))
        blo = 1 - l*a
        b = float(rng.uniform(max(blo, -0.999), 1.0))
        if not in_Tq(a, b, l):
            continue

        cur_run = 0
        for _ in range(STEPS):
            # current point in domain?
            indom = in_Tq(a, b, l)
            res, i, k = genuine_step(a, b, w, q, l)
            if res is None:
                if indom:
                    nobranch_in_Tq += 1
                nobranch_total += 1
                break
            steps_total += 1
            branch_offset_seen.add(q - i)

            P = Pgen(a, b, l)
            sub = P < t - EPS

            # (E) sustained run of sub-threshold steps
            if sub:
                cur_run += 1
                if cur_run > longest_run:
                    longest_run = cur_run
                    longest_run_example = (q, round(a, 6), round(b, 6))
            else:
                cur_run = 0

            na, nb = res
            Pnext = Pgen(na, nb, l)
            next_in_dom = in_Tq(na, nb, l)

            if i == q - 2:
                # (C) cusp leg
                cusp_steps += 1
                if sub:
                    cusp_subthr += 1
                    margin = t - P
                    if cusp_worst is None or margin > cusp_worst[0]:
                        cusp_worst = (margin, round(a,8), round(b,8), i, k, round(P,8))
            elif 2 <= i <= q - 3:
                # (D) deep-mid ejection leg
                if sub:
                    dm_subthr += 1
                    floors_dm_subthr.add(k)
                    holds = Pnext >= t - EPS
                    if holds:
                        dm_hold += 1
                    else:
                        dm_fail += 1
                        margin = t - Pnext
                        if dm_worst is None or margin > dm_worst[0]:
                            dm_worst = (margin, round(a,8), round(b,8), i, k,
                                        round(P,8), round(Pnext,8))
                    if k == 0:
                        dm_subthr_f0 += 1
                        if holds: dm_hold_f0 += 1
                        else:     dm_fail_f0 += 1
                    elif k == 1:
                        dm_subthr_f1 += 1
                        if holds: dm_hold_f1 += 1
                        else:     dm_fail_f1 += 1
                    else:
                        dm_subthr_fk += 1
                        if holds:
                            dm_hold_fk += 1
                        else:
                            dm_fail_fk += 1
                    if not holds and k >= 1:
                        margin = t - Pnext
                        if dm_worst_f1 is None or margin > dm_worst_f1[0]:
                            dm_worst_f1 = (margin, round(a,8), round(b,8), i, k,
                                           round(P,8), round(Pnext,8))
            # i == q-1 is scalar branch (not part of (C)/(D))

            a, b = na, nb
            if not next_in_dom:
                break

    return dict(
        q=q, l=l, t=t, steps_total=steps_total,
        nobranch_in_Tq=nobranch_in_Tq, nobranch_total=nobranch_total,
        branch_offset_seen=sorted(branch_offset_seen),
        cusp_steps=cusp_steps, cusp_subthr=cusp_subthr, cusp_worst=cusp_worst,
        dm_subthr=dm_subthr, dm_hold=dm_hold, dm_fail=dm_fail,
        dm_subthr_f0=dm_subthr_f0, dm_hold_f0=dm_hold_f0, dm_fail_f0=dm_fail_f0,
        dm_subthr_f1=dm_subthr_f1, dm_hold_f1=dm_hold_f1, dm_fail_f1=dm_fail_f1,
        dm_subthr_fk=dm_subthr_fk, dm_hold_fk=dm_hold_fk, dm_fail_fk=dm_fail_fk,
        dm_worst=dm_worst, dm_worst_fk=dm_worst_f1,
        floors_dm_subthr=sorted(floors_dm_subthr),
        longest_run=longest_run, longest_run_example=longest_run_example,
    )

def main():
    QS = [17, 18, 19, 20, 21]
    NS, STEPS = 3000, 400
    results = []
    print("="*100)
    print(f"CONFINEMENT-LEG AUDIT (genuine Taha BCZ_q map)  Pgen=a*(a+l*b)/l, t=1/l^3")
    print(f"orbits/q={NS}  steps/orbit={STEPS}")
    print("="*100)
    for q in QS:
        r = audit_q(q, NS=NS, STEPS=STEPS, seed=1000+q)
        results.append(r)
        print(f"\n----- q={q}  lam={r['l']:.6f}  t=1/lam^3={r['t']:.6f}  "
              f"(in-domain steps={r['steps_total']}) -----")
        print(f"  (T) trichotomy: branch offsets (q-i) seen = {r['branch_offset_seen']} "
              f"(expect 1=scalar,2=cusp,>=3=deep-mid)")
        print(f"      None-branch while IN Tq (violations) = {r['nobranch_in_Tq']}  "
              f"(None-branch total incl. domain-exit = {r['nobranch_total']})")
        print(f"  (C) cusp leg (i=q-2): steps={r['cusp_steps']}  "
              f"sub-threshold(Pgen<t) VIOLATIONS={r['cusp_subthr']}")
        if r['cusp_worst']:
            m,a,b,i,k,P = r['cusp_worst']
            print(f"      worst cusp violation: margin={m:.3e} at a={a} b={b} i={i} k={k} Pgen={P}")
        print(f"  (D) deep-mid ejection (i in 2..q-3), sub-threshold steps:")
        print(f"      ALL floors : subthr={r['dm_subthr']:6d}  hold(next>=t)={r['dm_hold']:6d}  "
              f"FAIL={r['dm_fail']:6d}   floors_seen={r['floors_dm_subthr']}")
        print(f"      floor k==0 : subthr={r['dm_subthr_f0']:6d}  hold={r['dm_hold_f0']:6d}  "
              f"FAIL={r['dm_fail_f0']:6d}")
        print(f"      floor k==1 : subthr={r['dm_subthr_f1']:6d}  hold={r['dm_hold_f1']:6d}  "
              f"FAIL={r['dm_fail_f1']:6d}")
        print(f"      floor k>=2 : subthr={r['dm_subthr_fk']:6d}  hold={r['dm_hold_fk']:6d}  "
              f"FAIL={r['dm_fail_fk']:6d}")
        if r['dm_worst']:
            m,a,b,i,k,P,Pn = r['dm_worst']
            print(f"      worst (D) FAIL (any floor): margin={m:.3e} a={a} b={b} i={i} k={k} "
                  f"Pgen={P} Pgen_next={Pn}")
        if r['dm_worst_fk']:
            m,a,b,i,k,P,Pn = r['dm_worst_fk']
            print(f"      worst (D) FAIL (floor>=2)  : margin={m:.3e} a={a} b={b} i={i} k={k} "
                  f"Pgen={P} Pgen_next={Pn}")
        print(f"  (E) longest sustained run of Pgen<t: {r['longest_run']} "
              f"(seed-ish {r['longest_run_example']})")

    # ---- per-q table ----
    print("\n" + "="*100)
    print("PER-q SUMMARY TABLE")
    print("="*100)
    hdr = (f"{'q':>3} {'Tviol':>6} {'cuspViol':>9} {'D_subthr':>9} {'D_FAIL':>7} "
           f"{'sub_k=0':>8} {'sub_k=1':>8} {'sub_k>=2':>9} {'longRun':>8}")
    print(hdr)
    for r in results:
        print(f"{r['q']:>3} {r['nobranch_in_Tq']:>6} {r['cusp_subthr']:>9} "
              f"{r['dm_subthr']:>9} {r['dm_fail']:>7} {r['dm_subthr_f0']:>8} "
              f"{r['dm_subthr_f1']:>8} {r['dm_subthr_fk']:>9} {r['longest_run']:>8}")

    # ---- verdict ----
    any_T = any(r['nobranch_in_Tq'] > 0 for r in results)
    any_C = any(r['cusp_subthr'] > 0 for r in results)
    any_D_all = any(r['dm_fail'] > 0 for r in results)
    # do any non-zero floors EVER appear on a deep-mid sub-threshold step?
    nonzero_floor_dm = any((r['dm_subthr_f1'] + r['dm_subthr_fk']) > 0 for r in results)
    max_run = max(r['longest_run'] for r in results)

    print("\n" + "="*100)
    print("SUMMARY VERDICT")
    print("="*100)
    print(f"  (T) trichotomy holds (no None-branch in Tq): {not any_T}")
    print(f"  (C) cusp leg holds (no i=q-2 sub-threshold): {not any_C}")
    print(f"  (D) deep-mid ejection holds for ALL observed sub-threshold steps: {not any_D_all}")
    print(f"  (D) floor structure: deep-mid sub-threshold steps use ONLY floor k=0? "
          f"{not nonzero_floor_dm}  "
          f"(nonzero-floor deep-mid sub-thr steps observed: {nonzero_floor_dm})")
    print(f"  (E) longest sustained sub-threshold run across all q: {max_run}")

    legs_C_D_hold = (not any_C) and (not any_D_all)
    if legs_C_D_hold:
        if not nonzero_floor_dm:
            verdict = ("SOUND — (C) and (D) hold for ALL observed deep-mid sub-threshold "
                       "steps; empirically deep-mid steps are ENTIRELY floor-0 (no k>=1 ever "
                       "seen sub-threshold), so the 'floor-1 restriction' is automatic: "
                       "non-zero floors are confined to the scalar branch i=q-1.")
        else:
            verdict = "SOUND — (C) and (D) hold for ALL floors empirically."
    else:
        verdict = "DEFECT_FOUND — a confinement leg ((C) or (D)) is violated."
    print(f"\n  >>> {verdict}")
    return results

if __name__ == "__main__":
    main()
