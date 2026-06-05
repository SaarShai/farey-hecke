---
agent: A
day: 1
purpose: Cross-implement D2 sieve in Sage/Julia; verify existing slopes within machine eps; extend stubborn cases
---

# Agent A — Cross-implementation of D2 function-field sieve

## Context

A Python implementation of an Aoki–Koyama §3.4 cyclotomic-function-field Chebyshev-bias experiment exists at:

- `projects/ak-bias-followups/d2-function-field/fq_poly.py`  (F_q[T] arithmetic, Rabin irreducibility, F_2 packed-int + general F_q tuple)
- `projects/ak-bias-followups/d2-function-field/compute.py`  (driver: sieve all monic irreducibles up to degree N, bin by residue class mod M, accumulate `π_{1/2,K}(q^n)` and `π_{1/2}(q^n; M, A) = Σ_{P irr, deg P ≤ n, P ≡ A mod M} q^{−deg P / 2}`)
- `projects/ak-bias-followups/d2-function-field/out_T3.json`, `out_ex36.json`, `out_f3_t2.json`  (existing outputs)

Existing measured slopes (LSQ on `LHS_n(A) = π_{1/2,K}(q^n) − Φ(M)·π_{1/2}(q^n; M, A) = C log n + c + o(1)`):

| (q, M, A class) | t | predicted C | measured C | rel err |
|---|---|---|---|---|
| (2, T²) Ex 3.6 | 1 | +0.500 | +0.475 | 5.0% |
| (2, T³) A=1, QR | 1 | +0.500 | **+0.50449** | **0.45%** |
| (3, T²−1)       | 2 | +1.500 | +1.283 (n≤12) | 14% |
| (3, T³−T)       | 3 | +3.500 | +2.74 (n≤10) | 22% |

## Your task

1. **Re-implement from scratch in Sage (preferred — built-in `GF(q)['T']`) or Julia (Nemo.jl).** Do not use the existing Python code. Independently enumerate all monic irreducible polynomials of degree ≤ N in F_q[T], bin each by residue mod M, and compute the two cumulative quantities `π_{1/2,K}(q^n)` and `π_{1/2}(q^n; M, A)` for every unit class A.

2. **Match the four cases above.** Report your measured C for each. Pass criterion: |your C − existing measured C| < 1e-6 for the (2,T³) case (this is the headline number); < 1e-4 for the others (they have larger fitted residuals).

3. **Extend the F_3 cases.** Push `(3, T²−1)` to N ≥ 16 and `(3, T³−T)` to N ≥ 13. Compute the LSQ slope on the larger window and report.

4. **Sieve sanity.** Confirm prime count per degree matches Gauss: `N_q(n) = (1/n) Σ_{d|n} μ(n/d) q^d`. Tabulate for q∈{2,3}, n=1..N.

## Output format

Return JSON in a single fenced block at the end:

```json
{
  "implementation": "sage" | "julia",
  "version": "<sage/julia version + Nemo version if applicable>",
  "cases": [
    {"q": 2, "M": "T^2", "N": 22, "C_measured": ..., "C_expected": 0.5, "abs_diff": ..., "pass": true},
    {"q": 2, "M": "T^3", "N": 22, "A_class": "1", "C_measured": ..., "C_expected": 0.5, "abs_diff": ...},
    {"q": 3, "M": "T^2-1", "N": ..., "C_measured": ..., "C_expected": 1.5, "abs_diff": ...},
    {"q": 3, "M": "T^3-T", "N": ..., "C_measured": ..., "C_expected": 3.5, "abs_diff": ...}
  ],
  "gauss_check": [{"q":2, "n":1, "expected": 2, "got": 2}, ...],
  "verdict": "MATCH" | "MISMATCH" | "MISMATCH_DETAIL <description>",
  "blocker": null | "<one-line description if mismatch>",
  "code": "<the full reproducible script as a single string>"
}
```

If any case fails the pass criterion, set `verdict: "MISMATCH"` and describe the discrepancy. **Do not paper over a mismatch** — that's the whole point of this cross-check.

## Norms

- Independent reproduction: do not look at the Python source for guidance.
- Show your derivation of the LSQ fit window choice (the existing code uses `n_min_fit = max(5, N//3)`; pick yours independently and report).
- If you find the (2, T²) Ex 3.6 measured C of +0.475 is wrong (or right), say so explicitly.
