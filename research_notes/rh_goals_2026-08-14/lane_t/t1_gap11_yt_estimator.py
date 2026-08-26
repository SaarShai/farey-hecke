"""
GAP-11 y(t)-estimator cross-check: apply the SAME matched-filter estimator
used in t1_gap11_rerun.py directly to y(t) itself, as an independent
verification pass (not a re-derivation), and report against both the
Prop R prediction and the previously reported |C(gamma_1)|.

Reuses t1_gap11_rerun.sieve_mobius (borrowed, not reimplemented) and
reconstructs y(t) with IDENTICAL parameters (N_MAX, grid, R0/R_-1/R_triv,
matched-filter formula) so this is a same-estimator-on-y(t) confirmation
run, not a new method.
"""
import hashlib
import json
import sys
import time

import numpy as np
import mpmath as mp

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from t1_gap11_rerun import sieve_mobius, N_MAX, N_GRID, N_GRID_MIN, ZEROS  # noqa: E402

mp.mp.dps = 30

PREVIOUS_ABS_C1 = 6.287348644552258e-03  # T1_GAP11_N1_RECEIPT.json matched_filter_gamma1.abs_C1
PREDICTED_A_GAMMA1 = 6.271347603511035e-03  # same receipt, predicted_a_gamma1


def main():
    t0 = time.time()
    print("sieving mu(n) to N_MAX =", N_MAX)
    mu = sieve_mobius(N_MAX)
    print("sieve done in %.1fs" % (time.time() - t0))

    M = np.cumsum(mu.astype(np.int64))
    prefix2 = np.cumsum(M.astype(np.float64))

    grid = np.unique(np.round(np.geomspace(N_GRID_MIN, N_MAX, N_GRID)).astype(np.int64))
    grid = grid[(grid >= 2) & (grid <= N_MAX)]

    S_vals = prefix2[grid - 1] / grid.astype(np.float64)

    zetap_neg2 = float(-mp.zeta(3) / (4 * mp.pi ** 2))
    coeff1 = 1.0 / ((-2) * (1 - 2) * zetap_neg2)
    R_triv = coeff1 * grid.astype(np.float64) ** (-2.0)

    R0 = -2.0
    Rm1 = 12.0 / grid.astype(np.float64)

    t_grid = np.log(grid.astype(np.float64))
    y_emp = grid.astype(np.float64) ** (-0.5) * (S_vals - R0 - Rm1 - R_triv)

    # same matched-filter estimator as t1_gap11_rerun.py, applied to this y(t)
    def matched_filter(g):
        integrand = y_emp * np.exp(-1j * g * t_grid)
        val = np.trapezoid(integrand, t_grid) / (t_grid[-1] - t_grid[0])
        return val

    g1 = ZEROS[0]
    C1 = matched_filter(g1)
    abs_C1 = float(abs(C1))

    s = mp.mpc(0.5, g1)
    zp = mp.zeta(s, derivative=1)
    a_gamma1 = float(abs(1.0 / ((mp.mpc(0.5, g1)) * (mp.mpc(1.5, g1)) * zp)))

    ratio_vs_predicted = abs_C1 / a_gamma1
    ratio_vs_previous = abs_C1 / PREVIOUS_ABS_C1

    print(f"\n|C(gamma_1)| on y(t), this run       = {abs_C1:.6e}")
    print(f"predicted a_gamma_1 (Prop R)          = {a_gamma1:.6e}   ratio = {ratio_vs_predicted:.4f}")
    print(f"previous |C(gamma_1)| (N1 rerun)      = {PREVIOUS_ABS_C1:.6e}   ratio = {ratio_vs_previous:.4f}")

    with open(__file__, "rb") as fh:
        script_sha256 = hashlib.sha256(fh.read()).hexdigest()

    receipt = {
        "purpose": "GAP-11: apply the SAME matched-filter estimator directly to y(t) "
                   "(reusing t1_gap11_rerun.py's y(t) construction verbatim, same "
                   "N_MAX/grid/R0/R_-1/R_triv/matched-filter formula) as an independent "
                   "verification that |C(gamma_1)| already reported in T1_GAP11_N1_RECEIPT.json "
                   "was in fact computed on y(t) itself.",
        "script": "research_notes/rh_goals_2026-08-14/lane_t/t1_gap11_yt_estimator.py",
        "script_sha256": script_sha256,
        "reused_script": "research_notes/rh_goals_2026-08-14/lane_t/t1_gap11_rerun.py",
        "python": sys.version,
        "numpy_version": np.__version__,
        "mpmath_version": mp.__version__,
        "N_MAX": N_MAX,
        "grid_size": int(len(grid)),
        "grid_min": int(grid.min()),
        "grid_max": int(grid.max()),
        "gamma_1": g1,
        "abs_C1_this_run_on_yt": abs_C1,
        "predicted_a_gamma1": a_gamma1,
        "ratio_this_run_vs_predicted": ratio_vs_predicted,
        "previous_abs_C1_N1_rerun_receipt": PREVIOUS_ABS_C1,
        "ratio_this_run_vs_previous": ratio_vs_previous,
    }
    out_path = __file__.rsplit("/", 1)[0] + "/T1_GAP11_YT_RECEIPT.json"
    with open(out_path, "w") as fh:
        json.dump(receipt, fh, indent=2)
    print("\nreceipt written to", out_path)


def _self_check():
    """Trivial parameter-identity check: this script's N_MAX/N_GRID/N_GRID_MIN/ZEROS
    must match t1_gap11_rerun.py's, since we import them directly."""
    import t1_gap11_rerun as _r
    assert N_MAX == _r.N_MAX and N_GRID == _r.N_GRID and N_GRID_MIN == _r.N_GRID_MIN
    assert ZEROS == _r.ZEROS


if __name__ == "__main__":
    _self_check()
    main()
