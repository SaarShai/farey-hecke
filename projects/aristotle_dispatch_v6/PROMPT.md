# Aristotle Dispatch v6 — Close KL for the cluster=2 boundedness proof

## Background

Companion to:
- `BCZDenominatorRepulsion.lean` (v4, 0 sorries) — BCZ moments + Corr = −1/2
- `BCZThresholdIntegration.lean` (v5, 0 sorries) — closed form `P(XY < 2/9) = (8·ln(3/2) − 2)/9`

The cluster=2 universality theorem says: above `q*_BCZ = (11 − 8·ln(3/2))/9`, no three consecutive BCZ pairs can all be extreme (i.e. product < 2/9).

The bulk of this is provable: the case `x_{i+1} ∈ (0, 0.702]` closes via the quadratic squeeze `9y² − 9y + 2 > 0` (roots 1/3, 2/3) plus a `k₀ ≥ 5, x_{i+2} ≥ 2/(3√5)` argument.

The remaining "0.702-band" `x_{i+1} ∈ (1 − 2/(3√5), 1)` is the Key Lemma (KL). The sketch in the file shows it reduces to **k₀ = 1 is the only valid case in this band, and forces X₁X₂ ≥ X₁² − 2/9 > 2/9**.

## Targets (in order)

1. **`KL_X1_band_forces_X1X2_nonextreme`** — the main statement. Use the sketch in the file's doc-string:
   - For k₀ ≥ 2: derive `18 X₁² − 9 X₁ − 2 ≤ 0`, contradiction with `X₁ > 0.702`.
   - For k₀ = 1: `X₂ = X₁ − X₀`, then `X₁ X₂ = X₁² − X₀ X₁ > X₁² − 2/9 > 0.702² − 2/9 > 2/9`.
   
   Should be closeable with `nlinarith` + case-splitting on `k₀ : ℤ`.

2. **`cluster_size_le_two`** — the corollary. Requires also handling `x_{i+1} ∈ (2/3, 0.702]` separately (the `k₀ ≥ 5` case from §3 of the research note). May need to break into 3 sub-cases:
   - `x_{i+1} ∈ (0, 1/3) ∪ (2/3, 1)` from the quadratic squeeze (rigorous)
   - `x_{i+1} ∈ (2/3, 1 − 2/(3√5))` via `k₀ X₂² − X₁ X₂ ≥ 4/9 − 2/9 = 2/9`
   - `x_{i+1} ∈ (1 − 2/(3√5), 1)` via KL (target 1 above)

## Constraints

- Only standard Mathlib axioms (no new sorries propagated; can defer one sub-case to a separate lemma)
- Use `Real.sqrt 5`, `intervalIntegral` etc. as in v5
- If KL doesn't close, decompose it further and report which sub-piece is left

## Acceptance

Either:
- (A) Close KL fully → completes the cluster=2 boundedness theorem.
- (B) Close KL for k₀ = 1 case (the dominant one per the sketch) and report the k₀ ≥ 2 sub-case status.
- (C) If neither, return a structural reason and a refined sub-statement.

## Notes

The orbit constraint `X₂ = k₀ X₁ − X₀` is the key — it couples the system more than the static analysis used in the research note. The k₀ = 1 case is straightforward; k₀ ≥ 2 is ruled out by the band constraint.
