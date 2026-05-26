---
agent: D
day: 1
purpose: Compute null distribution of δ_ff at finite N; determine whether δ_ff = 1.0000 is a real signal or sample-size artifact
---

# Agent D — Null-distribution check for δ_ff = 1.0000

## Context — and why this matters

The function-field Rubinstein-Sarnak density `δ_ff(b, a; N) := #{n ∈ [1,N] : π(q^n; M, b) > π(q^n; M, a)} / N` was reported at **δ_ff = 1.0000 over n = 1..22** for (q=2, M=T², non-QR vs QR) and (q=2, M=T³, A=3 vs A=1).

In the classical (number-field) R-S setting, δ ≈ 0.9959 for (4; 3, 1). Hitting **exactly 1.0000** in the function-field case looks too clean — it could be:

(α) genuine: the function-field bias is structurally larger and signs never flip in the observable n range, or
(β) artifact: at N=22 the LI-class-of-function-fields null distribution *also* concentrates near 1.0000, so the observed 1.0000 carries no information.

This sprint has a hard precedent for catching (β): see `~/.claude/projects/-Users-za-Documents-Farey-NOW/memory/project_dpac_status.md` — the "9×–52× avoidance margin" claim in the DPAC PR was REFUTED as exactly this kind of sample-size artifact.

We do NOT want to ship D2 with the same pattern.

## Your task

1. **Define the null.** State precisely the LI-class null for function-field Chebyshev bias. The classical LI hypothesis is: imaginary parts of nontrivial zeros of L_K(s, χ) are Q-linearly independent. In the function-field case, zeros are at `q^{-1/2} e^{iθ}` for `θ ∈ [0, 2π)` — the analog of LI is that the phases θ_j across the relevant characters are uniformly distributed and independent. State this carefully.

2. **Derive δ_ff under the null.** For (q, M) with t=1 (so a single non-QR class b vs a single QR class a), δ_ff is the long-run fraction of n where a random walk in the phase space has the b-component leading. Compute the asymptotic δ_ff under the null — call this `δ*` — and the finite-N expected value `E[δ_ff(N)]` and its standard deviation.

3. **Crucial: tail probabilities.** Compute `P(δ_ff(N=22) = 1.0000 | null)` for the (2, T²) and (2, T³) cases. If this probability is ≥ 0.10, the observed δ_ff = 1.0000 is consistent with the null and the claim must be downgraded.

4. **Simulate.** As a cross-check, simulate the null process (random IID phases, accumulate the partial sums) 10^5 times for N = 22 and report the empirical distribution of δ_ff. Match analytics to simulation.

5. **Verdict.** Per-case:
   - **REAL SIGNAL**: P(δ_ff(N) = 1 | null) < 0.05.
   - **CONSISTENT WITH NULL**: P(δ_ff(N) = 1 | null) ≥ 0.05.
   - In either case, report `δ*` (asymptotic value, which is the meaningful number for the paper).

## Output format

```json
{
  "null_definition": "<precise statement of function-field LI>",
  "cases": [
    {
      "label": "(2, T^2) non-QR vs QR",
      "delta_star_asymptotic": ...,
      "E_delta_ff_N22": ...,
      "Stddev_delta_ff_N22": ...,
      "P_delta_ff_eq_1_under_null_N22": ...,
      "observed_delta_ff_N22": 1.0000,
      "simulation_n_trials": 100000,
      "simulation_empirical_P_eq_1": ...,
      "verdict": "REAL SIGNAL" | "CONSISTENT WITH NULL"
    },
    {
      "label": "(2, T^3) A=3 vs A=1",
      "delta_star_asymptotic": ...,
      ...
    }
  ],
  "recommendation_for_paper": "<one paragraph: how to phrase the delta_ff claim honestly>",
  "code_for_simulation": "<reproducible Python script>"
}
```

## Norms

- Be adversarial. If P(δ_ff=1 | null, N=22) is meaningful (e.g. ≥ 0.10), say so loudly. That's the whole point.
- "Long-run fraction equal to 1" is a *strong* null statement — only true if the bias has zero overlap probability asymptotically. If `δ* = 1` even under the null, the observed 1.0000 is uninformative.
- If `δ* < 1` but `δ* > 0.99`, the null gives `P(δ_ff(22) = 1) ≈ δ*^22` ≈ 0.80 — totally consistent with null. Make this calculation.
