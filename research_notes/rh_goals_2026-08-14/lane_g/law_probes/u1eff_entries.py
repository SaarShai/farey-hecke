"""u1eff_entries.py -- U1-eff entry-wise probe, step 1: entry convergence in q.

kappa(q) = q-2 grows, so M_q and any theta-limit do NOT share an index set in
the natural LEFT (ascending-cell) indexing used by the builder.  u1eff_geom
shows the Markov cells accumulate at the collapsing endpoint -lambda/2, while
the cells at the OTHER end converge to the fixed lambda=2 points -n/(n+1).
So the only index scheme in which an entry-wise limit could exist is
RIGHT-indexing:  i' = kappa - i,  j' = kappa - j  (0 = rightmost cell [-1/3,0]).

This probe measures, at fixed strip points s:

  (a) M_q[(i',m),(j',k)] for small right-indices i',j' and small Taylor indices
      m,k -> is there a limit, and at what rate in q?
  (b) the same at the LEFT (collapsing) end, rows i = 1, 2 -> does the envelope
      hold there, or do those entries blow up?
  (c) per-block max |entry| as a function of right-index, to test the claimed
      geometric (m+j)-envelope.

Read-only probe; writes only its own JSON next to itself.
"""
import json, math, os, sys, time

CODE = "/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code"
sys.path.insert(0, CODE)
from flint import acb, arb, ctx                                    # noqa: E402
import zeta_cert_rosen as RO                                       # noqa: E402

ctx.prec = 300

N = 12
NHEAD = 4
SPTS = [("s1", 0.25, 7.0674), ("s2", 0.35, 17.0)]
QS = [int(x) for x in (os.environ.get("QS") or "21,41,81,161,321").split(",")]
RIDX = [0, 1, 2, 3]          # right block indices i' = kappa - i
TIDX = [(0, 0), (1, 0), (0, 1), (1, 1), (2, 2), (3, 3), (5, 5)]


def cx(z):
    return complex(float(z.real.mid()), float(z.imag.mid()))


def run():
    out = {"N": N, "n_head": NHEAD, "qs": QS, "points": {}}
    for name, sr, si in SPTS:
        s = acb(sr, si)
        rows = {}
        for q in QS:
            t0 = time.time()
            M, kappa = RO.build_reduced_matrix_ball(s, N, +1, q, n_head=NHEAD)
            dt = time.time() - t0
            rec = {"q": q, "kappa": kappa, "dim": kappa * N, "build_s": round(dt, 2)}

            def ent(i, j, m, k):
                return cx(M[(i - 1) * N + m, (j - 1) * N + k])

            # (a) right-indexed entries
            e = {}
            for ip in RIDX:
                for jp in RIDX:
                    i, j = kappa - ip, kappa - jp
                    if i < 1 or j < 1:
                        continue
                    for (m, k) in TIDX:
                        e[f"R{ip},{jp}|{m},{k}"] = [ent(i, j, m, k).real,
                                                    ent(i, j, m, k).imag]
            rec["right_entries"] = e
            # (b) left/collapsing-end rows i = 1,2 (cols also left-indexed)
            el = {}
            for i in (1, 2, 3):
                for j in (kappa - 1, kappa):
                    for (m, k) in TIDX:
                        el[f"L{i},{'k' if j==kappa else 'k-1'}|{m},{k}"] = [
                            ent(i, j, m, k).real, ent(i, j, m, k).imag]
            rec["left_entries"] = el
            # (c) per-block sup |entry| by right-index of the ROW
            blk = {}
            for ip in range(0, min(6, kappa)):
                i = kappa - ip
                mx = 0.0
                for j in range(1, kappa + 1):
                    for m in range(N):
                        for k in range(N):
                            a = abs(ent(i, j, m, k))
                            if a > mx:
                                mx = a
                blk[f"row_R{ip}"] = mx
            for i in (1, 2, 3):
                mx = 0.0
                for j in range(1, kappa + 1):
                    for m in range(N):
                        for k in range(N):
                            a = abs(ent(i, j, m, k))
                            if a > mx:
                                mx = a
                blk[f"row_L{i}"] = mx
            rec["block_sup"] = blk
            # (d) global max entry and Frobenius-ish column norm max
            gmax = 0.0
            colmax = 0.0
            for jj in range(kappa * N):
                cn = 0.0
                for ii in range(kappa * N):
                    a = abs(cx(M[ii, jj]))
                    cn += a * a
                    if a > gmax:
                        gmax = a
                cn = math.sqrt(cn)
                if cn > colmax:
                    colmax = cn
            rec["max_entry"] = gmax
            rec["max_colnorm"] = colmax
            rows[q] = rec
            print(name, q, "kappa", kappa, "build", round(dt, 1), "s",
                  "maxent", f"{gmax:.4g}", "maxcol", f"{colmax:.4g}", flush=True)
        out["points"][name] = rows
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "u1eff_entries.json")
    with open(p, "w") as f:
        json.dump(out, f, indent=1)
    print("wrote", p)


if __name__ == "__main__":
    run()
