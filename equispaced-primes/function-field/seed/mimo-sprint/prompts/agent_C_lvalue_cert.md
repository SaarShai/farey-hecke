---
agent: C
day: 1
purpose: Independently certify m(σ) = 0 by computing L_K(u, χ) at u = q^{-1/2} for every nontrivial χ
---

# Agent C — Independent L-value certificates for m(σ) = 0

## Context

For each case (q, M) in the D2 sprint, AK Theorem 3.4 has an additive term m(σ_A) = ord_{s=1/2} L_K(s, ·) in the leading coefficient. We *assume* m = 0 in the Python; this agent independently verifies it by:

(a) constructing each nontrivial Dirichlet character χ of G = (F_q[T]/M)*,
(b) computing L_K(u, χ) = Σ_{n=0}^{deg M − 1} c_n u^n,  c_n = Σ_{f monic, deg = n, gcd(f, M) = 1} χ(f),
(c) evaluating |L_K(q^{−1/2}, χ)| for every χ,
(d) issuing a m(σ) = 0 certificate iff every value is nonzero.

The existing claim is that the smallest magnitude across all (q, M) cases is **0.293** for Ex 3.6 (q=2, M=T², `1 − 1/√2`).

Reference implementation: `projects/ak-bias-followups/d2-function-field/lfunc.py` (do not consult).

## Your task

For each of the four cases — (2,T²), (2,T³), (3,T²−1), (3,T³−T):

1. Enumerate (F_q[T]/M)* explicitly. State |G|, generator structure.
2. Enumerate **all** characters χ of G via the Smith normal form / character group identification.
3. For each nontrivial χ, write down L_K(u, χ) as a polynomial in u of degree ≤ deg(M) − 1. Show the coefficient sums c_n explicitly.
4. Evaluate |L_K(q^{−1/2}, χ)| with at least 30-digit precision. (Use exact arithmetic where possible — these are finite sums of roots of unity.)
5. Issue per-case verdict: m(σ) = 0 certified iff ∀ nontrivial χ: |L| > 1e−6.
6. State the **minimum** magnitude across all (q, M, χ). Verify or correct the existing 0.293 claim (which should be `1 − 1/√2 ≈ 0.293` for Ex 3.6).

## Output format

```json
{
  "cases": [
    {
      "label": "(2, T^2) Ex 3.6",
      "G_order": 2,
      "generators": [{"rep": "T+1", "order": 2}],
      "characters": [
        {"index": 0, "trivial": true, "L_coeffs": ["..."], "L_at_qhalf": null, "abs_L": null},
        {"index": 1, "trivial": false, "L_coeffs": ["1", "-1"], "L_at_qhalf_real": "1 - 1/sqrt(2)", "L_at_qhalf_imag": 0, "abs_L_30digits": "0.292893218813452475599155637895"}
      ],
      "min_nontrivial_abs_L": "0.293...",
      "m_sigma_zero_certified": true
    },
    ...
  ],
  "global_min_abs_L": "<exact form, e.g. 1 - 1/sqrt(2)>",
  "global_min_abs_L_decimal_30": "...",
  "matches_claim_0_293": true | false,
  "all_cases_m_zero": true | false,
  "blocker": null | "<one-line if any L vanishes>"
}
```

## Norms

- These are deg(M) ≤ 3 polynomials — exact arithmetic is feasible everywhere. Do not use floating-point unless you can bound the error.
- If you find m(σ) ≠ 0 for any case, that is a blocker for D2 — flag immediately, do not paper over.
- The (3, T²−1) case has Φ = 4, t=2, so 3 nontrivial characters. The (3, T³−T) case has Φ = 12, t=3, so 11 nontrivial characters. List them all.
