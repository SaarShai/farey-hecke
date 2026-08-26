"""
GAP-10 sensitivity sweep: does the T1 (M3) amplitude-truncation quantile q
move the headline CR constant, the Lindeberg ratio, or the Berry-Esseen
bounded-summand constant?

Reuses lane_t/t1_verify.py's amplitude/FIM machinery (imported, not
rederived): log_abs_MW, log_S, fim_parts, lam_max, lindeberg, ZEROS, T, GAMMA, K.

Finding used throughout: t1_verify.py (and hence the T1 draft's own §4/§5
numerics) computes a_gamma = |M_W(1/2+i*gamma)| * r_gamma with r_gamma == 1
identically (the "intensity-smoothed mean of 1/|zeta'|" convention stated in
its module docstring). No stochastic amplitude LAW, and therefore no
quantile-q truncation, is present anywhere in the reused machinery. So:

  (a) the factor-24 / [I^-1]_ww computation and
  (b) the Lindeberg ratio Lambda(Gamma)
are computed from S_eps = |M_W|^2 * theta(|w|) alone -- q does not appear in
either formula. They are therefore *exactly* (bit-for-bit) invariant under a
sweep of q: 0.0% movement by construction, which is a strictly stronger
statement than the <1% the mootness argument (§7.2) needs.

  (c) the max-bounded-summand constant 2*a_gamma DOES depend on the amplitude
LAW's tail, because it is the realised amplitude of a single interferer, not
the intensity-smoothed mean that sigma^2(Gamma) uses. Since no empirical
r_gamma quantile function is committed as reusable machinery (lane_a has only
first-moment J_{-1} data), we use the NEAREST WELL-DEFINED ANALOGUE, labelled
as such: r_gamma ~ Pareto(alpha=2, x_m=1), the tail exponent implied directly
by the draft's own stated fact (§1.3/§7.2) that J_{-1} = E[r] is finite while
J_{-2} = E[r^2] diverges -- alpha=2 is the boundary value consistent with
both. Quantile function: r_q = (1-q)^{-1/2}, r_q -> inf as q -> 1 (no
truncation).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from t1_verify import (log_abs_MW, log_S, fim_parts, lam_max, lindeberg,
                        ZEROS, T, GAMMA, K, TWO_PI)

Q_GRID = [0.90, 0.95, 0.99, 0.995, 0.999, 1.0]
WINDOW = "riesz1"
GD = ZEROS[-1]


def pareto_quantile(q, alpha=2.0):
    """Nearest well-defined analogue of the (M3) truncation quantile
    (Pareto alpha=2, x_m=1; see module docstring). q=1.0 -> untruncated (inf)."""
    if q >= 1.0:
        return float("inf")
    return (1.0 - q) ** (-1.0 / alpha)


def main():
    rows = []

    # (a) factor-24 / [I^-1]_ww at gamma_d, approved cut Omega = 2*Gamma.
    # Uses fim_parts as-is: S_eps is the mean-field density, q does not enter.
    I, IN, IR = fim_parts(GD, T, 2 * GAMMA, WINDOW, K=K, dnu=2e-4)
    ratio24 = np.linalg.inv(I)[1, 1] / (24.0 / T ** 3)
    lm = lam_max(IN, IR)

    # (b) Lindeberg ratio at Gamma=50, mean-field convention -- q does not enter.
    lam50 = lindeberg(50.0, WINDOW)

    # (c) nearest well-defined analogue: max_gamma 2*a_gamma after truncating
    # r_gamma at its q-quantile, for interferers gamma > Gamma=50. |M_W| is
    # monotone decreasing on [50, inf) for riesz1, so the sup of |M_W| over
    # that range is attained at gamma = Gamma = 50 -- use that as the
    # worst-case interferer location.
    MW_at_Gamma = np.exp(log_abs_MW(np.array([50.0]), WINDOW))[0]
    sigma = np.sqrt(2.0) * np.exp(log_abs_MW(np.array([50.0]), WINDOW))[0]  # placeholder, replaced below
    # sigma^2(Gamma) via the same Prop 4.4 integral lindeberg() uses internally;
    # recompute sigma directly (lindeberg() returns 2*a_G^2/sigma^2, so
    # sigma^2 = 2*a_G^2/Lambda(G)).
    aG2 = np.exp(2 * log_abs_MW(np.array([50.0]), WINDOW))[0]
    sigma2 = 2.0 * aG2 / lam50
    sigma = np.sqrt(sigma2)

    print("=" * 78)
    print("GAP-10 truncation sweep. Window (W'), Gamma=50, Omega=2Gamma=100, T=%.4f" % T)
    print("(a) factor-24 ratio and (B1) lam_max at gamma_d: q-INVARIANT by construction")
    print("    [I^-1]_ww/local24 = %.5f   lam_max(IN^-1 IR) = %.5f" % (ratio24, lm))
    print("(b) Lindeberg Lambda(50): q-INVARIANT by construction = %.5f" % lam50)
    print()
    print(f"{'q':>7} {'r_q (Pareto a=2)':>18} {'max 2a_gamma':>14} {'sigma':>12} {'(c) ratio':>12}")
    for q in Q_GRID:
        rq = pareto_quantile(q)
        max_2a = 2.0 * MW_at_Gamma * rq
        ratio_c = max_2a / sigma
        rows.append({"q": q, "r_q": rq, "max_2a_gamma": max_2a,
                      "sigma": sigma, "ratio_c": ratio_c})
        rq_str = "inf" if not np.isfinite(rq) else f"{rq:.6g}"
        max2a_str = "inf" if not np.isfinite(max_2a) else f"{max_2a:.6g}"
        ratioc_str = "inf" if not np.isfinite(ratio_c) else f"{ratio_c:.6g}"
        print(f"{q:>7.3f} {rq_str:>18} {max2a_str:>14} {sigma:>12.6g} {ratioc_str:>12}")

    return {
        "window": WINDOW, "Gamma": 50.0, "Omega": 2 * GAMMA, "T": T,
        "a_factor24_ratio_local": ratio24, "a_lam_max_B1": lm,
        "b_lindeberg_50": lam50,
        "c_sigma_meanfield": sigma,
        "c_MW_at_Gamma": MW_at_Gamma,
        "c_rows": rows,
    }


if __name__ == "__main__":
    main()
