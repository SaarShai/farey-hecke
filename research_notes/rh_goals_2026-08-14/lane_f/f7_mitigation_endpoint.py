#!/usr/bin/env python3
"""F7 endpoint finite-column bound B_finite under candidate disc radii.

NON-RIGOROUS FLOAT PREPARATION context: the radii come from the float stage-0
optimization (not yet Arb TB-block certified).  The matrix build itself and the
column 2-norm sums are 384-bit Arb/Acb ball arithmetic over the entire closed
1e-6 flagship box, identical in kind to the pilot's endpoint measurement
(F7_PILOT_REPORT.md section 5), so numbers are directly comparable.

Builder: the q-generic certified path of zeta_cert_rosen.build_reduced_matrix_ball
(q=7, sign=+1, n_head=4), copied verbatim except that the disc radii are
per-disc inflated radii  rho_i = factor_i * (pts_i - pts_{i-1}) / 2  instead of
the engine default (uniform safety factor 2.5).  This is exactly how the frozen
factors (2.79, 2.39, 1.90, 1.56, 1.35) enter: the pilot's N=32 value
18.0743955713902... must reproduce (validation gate below).

B_finite = sum over all kappa*N retained columns of the Arb upper endpoint of
the column Euclidean 2-norm.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

REPO = Path("/Users/za/Documents/farey-hecke")
sys.path.insert(0, str(REPO / ".worktrees/aletheia-restore/code"))

from flint import acb, acb_mat, acb_series, arb, ctx  # noqa: E402

import zeta_cert_rosen as zcr  # noqa: E402

ctx.prec = 384

Q = 7
SIGN = +1
N_HEAD = 4
PIN_RE = "0.4751647621098225"
PIN_IM = "4.668743786424289"
HALF_WIDTH = "1e-6"
OUT = Path(__file__).resolve().parent / "f7_mitigation_endpoint_results.json"

FROZEN = ("2.79", "2.39", "1.90", "1.56", "1.35")
PILOT_B32 = 18.074395571390211522643097827116


def flagship_s_box() -> acb:
    return acb(arb(PIN_RE) + arb(0, arb(HALF_WIDTH)),
               arb(PIN_IM) + arb(0, arb(HALF_WIDTH)))


def build_reduced_matrix_ball_factors(s, N, sign, q, factors, n_head=4):
    """Verbatim copy of zeta_cert_rosen.build_reduced_matrix_ball with the
    single change that radii come from per-disc inflation factors (units of
    the half partition interval), matching the float stage-0 convention."""
    if q % 2 == 0:
        raise NotImplementedError("odd q only")
    lam = zcr.lam_ball(q)
    hq, kappa = zcr.hecke_params(q)
    pts = zcr.partition_points_ball(q, lam)
    c = [(pts[i - 1] + pts[i]) / 2 for i in range(1, len(pts))]
    rho = [arb(factors[i - 1]) * (pts[i] - pts[i - 1]) / 2
           for i in range(1, len(pts))]
    sgn = acb(sign)
    _single = zcr._single_block_allcols
    _tail = zcr._tail_block_allcols

    blocks = {}

    def add_cols(i, j, cols, prefac=None):
        key = (i, j)
        existing = blocks.get(key)
        if existing is None:
            existing = [acb_series([0]) for _ in range(N)]
            blocks[key] = existing
        for kk in range(N):
            col = cols[kk] if prefac is None else (prefac * cols[kk])
            existing[kk] = existing[kk] + col

    def single_block(i, j, n, neg):
        return _single(s, c[i - 1], rho[i - 1], c[j - 1], rho[j - 1], lam, n, neg, N)

    def inf_block(i, j, n0, neg):
        ci, ri, cj, rj = c[i - 1], rho[i - 1], c[j - 1], rho[j - 1]
        cols = _tail(s, ci, ri, cj, rj, lam, n0 + n_head, neg, N)
        for l in range(n0, n0 + n_head):
            hc = _single(s, ci, ri, cj, rj, lam, l, neg, N)
            for kk in range(N):
                cols[kk] = cols[kk] + hc[kk]
        return cols

    twoh = 2 * hq
    k_idx = kappa
    add_cols(1, twoh, single_block(1, twoh, 2, False))
    add_cols(1, k_idx, inf_block(1, k_idx, 3, False))
    add_cols(1, twoh, single_block(1, twoh, 1, True), prefac=sgn)
    add_cols(1, k_idx, inf_block(1, k_idx, 2, True), prefac=sgn)
    add_cols(2, k_idx, inf_block(2, k_idx, 2, False))
    add_cols(2, twoh, single_block(2, twoh, 1, True), prefac=sgn)
    add_cols(2, k_idx, inf_block(2, k_idx, 2, True), prefac=sgn)
    for i in range(3, k_idx + 1):
        add_cols(i, i - 2, single_block(i, i - 2, 1, False))
        add_cols(i, k_idx, inf_block(i, k_idx, 2, False))
        add_cols(i, twoh, single_block(i, twoh, 1, True), prefac=sgn)
        add_cols(i, k_idx, inf_block(i, k_idx, 2, True), prefac=sgn)

    dim = kappa * N
    M = acb_mat(dim, dim)
    for (i, j), cols in blocks.items():
        for kk in range(N):
            cser = cols[kk]
            for m in range(N):
                M[(i - 1) * N + m, (j - 1) * N + kk] = (
                    cser[m] if m < len(cser) else acb(0))
    return M, kappa


def b_finite(M, dim):
    """Sum of Arb upper endpoints of column Euclidean 2-norms."""
    total = arb(0)
    for col in range(dim):
        acc = arb(0)
        for row in range(dim):
            mag = M[row, col].abs_upper()
            acc = acc + mag * mag
        total = total + acc.sqrt()
    return total


def run_case(name, factors, n_values, results):
    s = flagship_s_box()
    for N in n_values:
        t0 = time.time()
        M, kappa = build_reduced_matrix_ball_factors(s, N, SIGN, Q, factors, N_HEAD)
        t1 = time.time()
        B = b_finite(M, kappa * N)
        t2 = time.time()
        rec = {
            "N": N,
            "dim": kappa * N,
            "B_finite_upper": B.upper().str(30, more=False),
            "B_finite_float": float(B.upper()),
            "build_seconds": t1 - t0,
            "build_plus_norms_seconds": t2 - t0,
        }
        results.setdefault(name, {"factors": list(factors), "runs": []})["runs"].append(rec)
        print(f"{name} N={N}: B_finite <= {rec['B_finite_upper']}  "
              f"(build {t1 - t0:.2f}s, +norms {t2 - t0:.2f}s)", flush=True)
        OUT.write_text(json.dumps(results, indent=2) + "\n")
        M = None


def main() -> None:
    if OUT.exists():
        results = json.loads(OUT.read_text())
    else:
        results = {
            "label": ("radii from NON-RIGOROUS FLOAT stage-0; matrix + column norms "
                      "are 384-bit Arb/Acb over the closed 1e-6 flagship box"),
            "q": Q, "sign": SIGN, "n_head": N_HEAD, "prec_bits": 384,
            "pin_re": PIN_RE, "pin_im": PIN_IM, "half_width": HALF_WIDTH,
            "pilot_B32_frozen": PILOT_B32,
        }

    which = sys.argv[1] if len(sys.argv) > 1 else "validate"
    if which == "validate":
        # Validation gate: reproduce the pilot's frozen-factor N=32 value.
        run_case("frozen", FROZEN, [32], results)
    elif which == "scaling_frozen":
        run_case("frozen", FROZEN, [64, 96, 128], results)
    else:
        # "candidate:<f1,f2,f3,f4,f5>:N1,N2,..."
        _, facs, ns = which.split(":")
        factors = tuple(facs.split(","))
        run_case("candidate_" + facs, factors, [int(x) for x in ns.split(",")], results)

    OUT.write_text(json.dumps(results, indent=2) + "\n")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
