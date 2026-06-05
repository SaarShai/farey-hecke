#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GOAL P — extend the RELIABLE X_Omega(q)=1/lam^3 verification past q<=70.

Memory record: the value is "numerically safe q<=200", but the only RELIABLE test
(true-map escape, not grid survivor COUNT which false-positives at fine grids) was
confirmed only to q<=70. This driver runs, per q, the DECISIVE two-stage test:

  (1) survivor_set(q)  -> rigorous grid forward-invariant fixpoint. survivors==0
      => NO sub-threshold invariant set at grid resolution => value holds, done.
  (2) if survivors>0   -> those cells are CANDIDATE islands (possibly grid artifacts,
      e.g. the known q=70 "33 survivors" NaN-cast artifact). Take their bounding box,
      pad it, and run the EXACT float64 genuine-map escape_test on a fine sweep with a
      long horizon. n_trapped==0 => every sub-thr seed escapes => artifact => value
      holds by the reliable method. n_trapped>0 => REAL candidate => would refute;
      flag for hi-precision follow-up.

Honest: a clean sweep is strong numerical EVIDENCE, never a proof. Any trapped seed is
the interesting outcome and is reported loudly.

Usage:  python3 code/Pgoal_escape_sweep.py "71,72,...,110"  [survivor_grid] [esc_grid] [horizon]
Run from ~/farey so that `code/` is importable.
"""
import sys, json, time
import numpy as np

sys.path.insert(0, "code")
sys.path.insert(0, ".")
from Igoal_survivor import survivor_set
from Egate2_q70 import escape_test


def verify_q(q, sgrid=1100, egrid=160, horizon=6000, pad_frac=0.15):
    t0 = time.time()
    nsurv, nS, thr, (A, B, P, surv) = survivor_set(
        q, Na=sgrid, Nb=sgrid, verbose=False)
    rec = dict(q=q, thr=float(thr), nS=int(nS), survivors=int(nsurv),
               method=None, trapped=None, max_dwell=None, box=None,
               secs=None, holds=None)
    if nsurv == 0:
        rec.update(method="survivor=0", trapped=0, max_dwell=0, holds=True,
                   secs=round(time.time() - t0, 1))
        return rec
    # candidate cluster -> reliable escape test on padded bbox
    idx = np.where(surv)[0]
    a_lo, a_hi = float(A[idx].min()), float(A[idx].max())
    b_lo, b_hi = float(B[idx].min()), float(B[idx].max())
    pa = max((a_hi - a_lo) * pad_frac, 5e-3)
    pb = max((b_hi - b_lo) * pad_frac, 5e-3)
    box = (a_lo - pa, a_hi + pa, b_lo - pb, b_hi + pb)
    n_trapped, worst_dwell = escape_test(q, box=box, Ng=egrid, horizon=horizon)
    rec.update(method="escape_test", trapped=int(n_trapped),
               max_dwell=int(worst_dwell), box=[round(v, 5) for v in box],
               holds=(n_trapped == 0), secs=round(time.time() - t0, 1))
    return rec


if __name__ == "__main__":
    if len(sys.argv) > 1:
        qs = [int(z) for z in sys.argv[1].split(",")]
    else:
        qs = [71, 72, 73, 74, 75]
    sgrid = int(sys.argv[2]) if len(sys.argv) > 2 else 1100
    egrid = int(sys.argv[3]) if len(sys.argv) > 3 else 160
    horizon = int(sys.argv[4]) if len(sys.argv) > 4 else 6000

    print(f"=== GOAL P reliable escape sweep: q in {qs[0]}..{qs[-1]} "
          f"(survivor_grid={sgrid}, esc_grid={egrid}, horizon={horizon}) ===",
          flush=True)
    results = []
    refutations = []
    for q in qs:
        rec = verify_q(q, sgrid=sgrid, egrid=egrid, horizon=horizon)
        results.append(rec)
        tag = "HOLDS" if rec["holds"] else ">>> TRAPPED SEEDS — REFUTATION CANDIDATE"
        print(f"  q={q:4d} thr={rec['thr']:.6f} |S|={rec['nS']:6d} "
              f"survivors={rec['survivors']:4d} method={rec['method']:>12s} "
              f"trapped={rec['trapped']} max_dwell={rec['max_dwell']} "
              f"[{rec['secs']}s]  {tag}", flush=True)
        if not rec["holds"]:
            refutations.append(rec)

    summary = dict(q_lo=qs[0], q_hi=qs[-1], n_q=len(qs),
                   all_hold=all(r["holds"] for r in results),
                   refutations=refutations, results=results)
    out = f"Pgoal_escape_sweep_q{qs[0]}_{qs[-1]}.json"
    with open(out, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\n=== SUMMARY: q={qs[0]}..{qs[-1]}  ALL_HOLD={summary['all_hold']}  "
          f"refutation_candidates={len(refutations)}  -> {out} ===", flush=True)
