"""
Agent D: numerical null-distribution check for delta_ff(N).

NULL HYPOTHESIS (function-field LI-analog):
For (q, M) with t = dim_{F_2}(G/G^2), the bias between a QR class a and a non-QR class b
is governed by sum_{chi nontrivial quadratic} bar(chi)(b - a) * (chi-twisted oscillation).

For our (q=2, M=T^2) and (q=2, M=T^3) cases (both t=1), there is a SINGLE nontrivial quadratic
character chi_2 whose L-function has degree deg(M)-1 zeros on |u|=q^{-1/2}.

Under LI for function-field zeros: the phases theta_j of those zeros are iid uniform on [0, 2*pi).
The chi-twisted prime sum at degree n is a sum over zeros: -sum_j (q^{-1/2} e^{i theta_j})^n / (something).

We simulate the unweighted prime-counting bias pi(q^n; M, b) - pi(q^n; M, a) under this null:

  X_n = sign of [ Re( sum_j A_j * e^{i n theta_j} ) ]

where A_j are O(1) class-dependent constants and theta_j are iid uniform.

For (q=2, M=T^2): chi_2 has L-poly degree 1, so a SINGLE zero with phase theta_1. The bias sign
flips when n*theta_1 wraps past pi/2 mod pi. Under uniform theta_1, fraction-of-n-with-bias-positive
asymptotes to 1/2, BUT we're asking about a fixed sample of 22 n-values from a single random theta_1.

For (q=2, M=T^3): chi_2 has L-poly degree 2, so two zeros theta_1, theta_2. Symmetry constrains them
(quadratic character with real coefficients → zeros come in conjugate pairs or fixed points).

We do two things:
(a) For each case, derive the asymptotic delta* (long-run fraction of n where bias > 0) analytically.
(b) Simulate to estimate P(delta_ff(N=22) = 1.0000 | null).

Output goes to results/agent_D_deltaff_null_local.json.
"""

import json, math, random
from pathlib import Path
from typing import Callable

random.seed(2026_05_26)

OUT = Path(__file__).parent / "agent_D_deltaff_null_local.json"

N_TRIALS = 200_000
N_RANGE = 22


def simulate_case(label: str, n_zeros: int, *, n_trials: int = N_TRIALS, n_range: int = N_RANGE):
    """For each trial: draw n_zeros iid phases theta_j ~ U[0, 2*pi).
    Compute the partial-sum bias sequence B_n = sum_{m=1..n} sign(Re sum_j cos(m*theta_j)) for m=1..n.
    Equivalently: at each m in [1, n_range], sample sign of Re-part of sum_j e^{i*m*theta_j}.
    Then delta_ff(N) = fraction of m in [1, N] where bias is +1 (or, in the unweighted formulation,
    where the running CUMULATIVE count of "wins" exceeds 0).

    We use the CUMULATIVE interpretation matching rs_density.py:
        delta_ff(N) = #{n in [1,N] : cumulative_bias(n) > 0} / N
    """
    delta_counts = {round(k/n_range, 4): 0 for k in range(0, n_range + 1)}
    eq_one_count = 0
    eq_zero_count = 0
    mean_delta = 0.0
    var_delta_sum = 0.0
    for _ in range(n_trials):
        thetas = [random.uniform(0, 2 * math.pi) for _ in range(n_zeros)]
        cum = 0
        wins = 0
        for m in range(1, n_range + 1):
            # Re(sum_j e^{i*m*theta_j}) = sum_j cos(m*theta_j)
            r = sum(math.cos(m * t) for t in thetas)
            # tiebreak: r==0 (measure 0 in continuous law, but include defensively)
            if r > 0:
                cum += 1
            elif r < 0:
                cum -= 1
            if cum > 0:
                wins += 1
        delta = wins / n_range
        mean_delta += delta
        var_delta_sum += delta * delta
        if delta >= 0.99999:
            eq_one_count += 1
        if delta <= 0.00001:
            eq_zero_count += 1
    mean_delta /= n_trials
    var_delta = var_delta_sum / n_trials - mean_delta * mean_delta
    stddev_delta = math.sqrt(max(var_delta, 0.0))
    return {
        "label": label,
        "n_zeros": n_zeros,
        "n_trials": n_trials,
        "N": n_range,
        "E_delta_ff_N": mean_delta,
        "stddev_delta_ff_N": stddev_delta,
        "P_delta_ff_eq_1": eq_one_count / n_trials,
        "P_delta_ff_eq_0": eq_zero_count / n_trials,
    }


def main():
    cases = []

    # (q=2, M=T^2): chi_2 has L-poly degree deg(M)-1 = 1, so 1 zero.
    cases.append(simulate_case("(q=2, M=T^2) chi_quad, n_zeros=1", n_zeros=1))

    # (q=2, M=T^3): chi_2 (the quadratic character) has L-poly degree 2, so 2 zeros.
    # The two zeros are conjugate (quadratic char with real coeffs), so theta_2 = -theta_1
    # under standard conventions. We simulate UNCONSTRAINED first; then the conjugate-constrained case.
    cases.append(simulate_case("(q=2, M=T^3) chi_quad, n_zeros=2 unconstrained", n_zeros=2))
    # Conjugate-constrained: only 1 free phase, paired sign — equivalent to 1-zero case with
    # doubled amplitude. Re-simulate with conjugate constraint by reflecting.
    def sim_conjugate_constrained(n_trials=N_TRIALS, N=N_RANGE):
        eq1 = 0; eq0 = 0; mean = 0.0; var_sum = 0.0
        for _ in range(n_trials):
            t1 = random.uniform(0, 2 * math.pi)
            cum = 0; wins = 0
            for m in range(1, N + 1):
                # cos(m*t1) + cos(-m*t1) = 2 cos(m*t1)
                r = 2 * math.cos(m * t1)
                if r > 0: cum += 1
                elif r < 0: cum -= 1
                if cum > 0: wins += 1
            d = wins / N
            mean += d; var_sum += d * d
            if d >= 0.99999: eq1 += 1
            if d <= 0.00001: eq0 += 1
        mean /= n_trials
        var = var_sum / n_trials - mean * mean
        return {
            "label": "(q=2, M=T^3) chi_quad, conjugate-constrained 1 free phase",
            "n_zeros": "2 (conjugate pair, 1 free)",
            "n_trials": n_trials,
            "N": N,
            "E_delta_ff_N": mean,
            "stddev_delta_ff_N": math.sqrt(max(var, 0.0)),
            "P_delta_ff_eq_1": eq1 / n_trials,
            "P_delta_ff_eq_0": eq0 / n_trials,
        }
    cases.append(sim_conjugate_constrained())

    output = {
        "null_hypothesis": (
            "Function-field LI: phases of zeros of nontrivial quadratic L-functions are iid uniform "
            "on [0, 2pi). For real quadratic char, zeros come in conjugate pairs."
        ),
        "interpretation_note": (
            "delta_ff(N) = #{n in [1,N]: cumulative bias > 0} / N. Cumulative bias = signed running "
            "sum of sign(Re sum_j e^{i*n*theta_j}). This matches rs_density.py unweighted convention."
        ),
        "cases": cases,
        "verdict_template": (
            "If P(delta_ff(22)=1 | null) >= 0.05, the observed delta_ff=1.0000 at n<=22 is "
            "CONSISTENT WITH NULL and must be downgraded in the paper."
        ),
    }

    OUT.write_text(json.dumps(output, indent=2))
    print(f"wrote {OUT}")
    for c in cases:
        print(f"  {c['label']}: E[delta_ff(22)]={c['E_delta_ff_N']:.4f}  stddev={c['stddev_delta_ff_N']:.4f}  P(=1)={c['P_delta_ff_eq_1']:.4f}  P(=0)={c['P_delta_ff_eq_0']:.4f}")


if __name__ == "__main__":
    main()
