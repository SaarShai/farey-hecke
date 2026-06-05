---
agent: B
day: 1
purpose: Derive QR coefficient C and next-order correction from AK §3.4; explain pre-asymptotic residuals
---

# Agent B — Symbolic next-order correction to the AK §3.4 QR coefficient

## Context

In Aoki–Koyama "Chebyshev's bias against splitting and principal primes in global fields" (JNT 245 (2023)), Theorem 3.4 (cyclotomic function field case, char p > 0), the prediction is:

  LHS_n(A) := π_{1/2,K}(q^n) − Φ(M) · π_{1/2}(q^n; M, A)
            = (constant_t,σ_A) · log n + c_A + o(1)         (n → ∞)

with

  constant_t,σ_A =
    +(2^t − 1)/2 + m(σ_A)         if A is a QR mod M
    −1/2 + m(σ_A)                  otherwise

where:
- t = dim_{F_2} (G/G²), G = (F_q[T]/M)*
- m(σ_A) = ord_{s=1/2} L_K(s, ·) summed in the appropriate quadratic-character sense

Empirically (see `out_*.json` in `projects/ak-bias-followups/d2-function-field/`), the measured slope at finite n is:

| (q, M) | t | predicted C | measured C (LSQ) | rel err |
|---|---|---|---|---|
| (2, T²) | 1 | +0.500 | +0.475 | 5.0% |
| (2, T³) | 1 | +0.500 | +0.50449 | 0.45% |
| (3, T²−1) | 2 | +1.500 | +1.283 (n≤12) | 14% |
| (3, T³−T) | 3 | +3.500 | +2.74 (n≤10) | 22% |

The (2, T³) case is at 0.45% — clean. The other three are too far off to be Monte-Carlo noise (this is direct enumeration, not sampling) and too clean to be bugs. There is a next-order correction term being absorbed into the fit residual.

## Your task

1. **From AK §3.4 alone, re-derive the leading coefficient** for each of the four cases. Do not consult the existing Python. Show t computed from Φ(M)/|squares|. Verify the predicted C column.

2. **Derive the next-order correction.** AK's o(1) hides a term of the form

   D_t · (log log n)/(log n) + E_t / log n + O(1/(log n)^2)        (conjectured form — verify or correct)

   Compute D_t and E_t symbolically as functions of t and the residual L-function data (L_K(u, χ) values at u = q^{−1/2}, summed over nontrivial χ of (F_q[T]/M)*).

3. **Predict measured C at each (q, M, N).** Plug in the actual N values and predict what the LSQ slope on `[N//3, N]` should yield. Compare to measured. The difference should drop from 5%/14%/22% to under 2%.

4. **Special case (2, T³)**: the rel err here is already 0.45%. Either (a) the correction is structurally smaller for this case (explain why), or (b) the case is just at larger effective n (Φ(T³)·N = 4·22 = 88 vs (3, T³−T): 12·10 = 120 — so not just N). Resolve.

## Output format

```json
{
  "leading_C": {
    "(2, T^2)": 0.5,
    "(2, T^3)": 0.5,
    "(3, T^2-1)": 1.5,
    "(3, T^3-T)": 3.5
  },
  "leading_C_derivation": "<6-12 line proof sketch citing AK §3.4 equations>",
  "correction_form": "<symbolic form, e.g. C(n) = C + D·(log log n / log n) + E/log n + O(...)>",
  "correction_constants": {
    "(2, T^2)": {"D": ..., "E": ...},
    "(2, T^3)": {"D": ..., "E": ...},
    "(3, T^2-1)": {"D": ..., "E": ...},
    "(3, T^3-T)": {"D": ..., "E": ...}
  },
  "predicted_LSQ_slope_at_finite_N": {
    "(2, T^2, N=22)": ...,
    "(2, T^3, N=22)": ...,
    "(3, T^2-1, N=12)": ...,
    "(3, T^3-T, N=10)": ...
  },
  "explains_residual": true | false,
  "(2,T^3)_smallness_explanation": "<why this case is at 0.45% while others are at 5-22%>",
  "uncertainty_flags": ["<anything CONJECTURAL>"]
}
```

## Norms

- This is exact symbolic work. Show derivation, don't just state results.
- If you can't derive the correction analytically, do not invent numbers. Output `correction_form: "UNRESOLVED"` and say what you tried.
- Cross-check the +0.5 prediction for (2, T³): t=1 → (2^1 − 1)/2 = 1/2. Confirm.
