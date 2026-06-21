import Mathlib

open scoped BigOperators
open scoped Real

set_option maxHeartbeats 1000000

/-!
# Uniform spectral-gap lower bound for the Rosen/Hecke transfer operator (goal P1)

This is a **self-contained** RequestProject packaging the Arb-CERTIFIED spectral-gap
data for the Rosen / Hecke `λ_q`-continued-fraction transfer operator `L_s` at the
conformal parameter `s = 1` (where the leading eigenvalue is `λ₁ = 1`, the
Gauss–Kuzmin invariant density).

## What is certified OUTSIDE Lean (the numeric input we package here)

For each odd `q ∈ {5,7,9,11,13}` the script
`code/uniform_gap/cert_gap_sweep.py` (reusing the validated
`code/equidist_gap/cert_gap_rosen.py` + `code/zeta_cert_rosen.py` engine)
computes RIGOROUS Arb-ball enclosures of the two top eigenvalue moduli of the
`κ_q·N`-truncated reduced operator via `acb_mat.eig(algorithm="rump")` (Rump's
verified ball eigensolver: each returned ball is PROVED to contain exactly one
eigenvalue).  The certified output (headline `N`, prec 300 bits, N-stable):

| q  | κ_q | `l1_lo` (→1)      | `|λ₂|` upper enclosure | `gap_lo = 1 − l2_hi/l1_lo` |
|----|-----|------------------|------------------------|----------------------------|
| 5  | 3   | 0.999999999999…  | 0.2025127171           | 0.7974872829               |
| 7  | 5   | 0.999999999999…  | 0.3406773836           | 0.6593226164               |
| 9  | 7   | 0.999999999946…  | 0.4465190796           | 0.5534809204               |
| 11 | 9   | 0.999999999945…  | 0.5172265902           | 0.4827734098               |
| 13 | 11  | 0.999999999946…  | 0.5702300963           | 0.4297699037               |

These eigenvalue-modulus enclosures are the certified facts.  Below we encode each
`|λ₂(q)|` certified UPPER bound as a rational `subL2 q` (rounded UP from the Arb
`l2_hi`, so the inequality `|λ₂(q)| ≤ subL2 q` is implied by the certificate), and
prove the resulting per-`q` gap lower bounds and a single UNIFORM lower bound over
the range.

## What this file proves (target)

With `gapLB q := 1 − subL2 q` the per-`q` certified gap lower bound (using
`λ₁ = 1` exactly at `s = 1`, the value the certificate confirms to 1e−12):

* `gap_lb_q5 … gap_lb_q13` : `gapLB q ≥ cq` for explicit rationals (matching the table);
* `subL2_le_uniform`        : `subL2 q ≤ 57024/100000` for every `q ∈ {5,7,9,11,13}`;
* **`uniform_gap_lower_bound`** : for every `q ∈ {5,7,9,11,13}`,
      `gapLB q ≥ 42976/100000`  ( = `0.42976`, the certified gap at the largest `q`),
  i.e. a UNIFORM positive lower bound on the certified finite-`N` truncation gap
  across the range, attained (to rounding) at `q = 13`.

## HONESTY / SCOPE (do NOT overstate)

1. This is the **1-D Rosen-CF map decay-of-correlations gap** at `s = 1`.  `gap_lo`
   is certified for the **finite-`N` nuclear truncation**; propagating the
   eigenvalue dimension-tail to the TRUE operator is a separate residual (not in
   this file).  It does **NOT** prove 2-D horocycle effective equidistribution
   (the BCZ-Farey section is parabolic / zero-entropy, no spectral gap).
2. **The certified gap is strictly DECREASING in `q`** (0.797 → 0.659 → 0.553 →
   0.483 → 0.430 across `q = 5,7,9,11,13`).  So the uniform constant `0.42976`
   below is uniform **only over the certified finite range** `q ≤ 13`; whether a
   positive lower bound persists as `q → ∞` (gap stays bounded below vs. shrinks
   to 0) is OPEN — the data over this short range fits both a positive-limit form
   `gap ≈ 2.98/q + 0.214` and a vanishing power law `gap ≈ 2.30·q^{-0.65}` and
   cannot distinguish them.  This file makes NO asymptotic claim.
3. Scope is **odd `q`** (the certified MMS eq.(34) engine; even `q` deferred).
4. The faithful content is exactly "the certificate's rational eigenvalue-modulus
   bounds imply these gap inequalities".  This file does NOT formalize the transfer
   operator itself; it certifies the arithmetic that turns the Arb enclosures into
   the stated uniform gap bound.  (A vacuous statement that merely re-asserts a
   definition would be the worst outcome — avoided: every bound below is a genuine
   numeric consequence of the certified `l2_hi` values.)
-/

namespace UniformGap

/-- The five certified odd `q` in range. -/
def Qrange : List ℕ := [5, 7, 9, 11, 13]

/-- Certified UPPER bound on `|λ₂(q)|` for the Rosen/Hecke transfer operator at
`s = 1`, as a rational rounded UP from the Arb `l2_hi` enclosure (so
`|λ₂(q)| ≤ subL2 q` is implied by the Rump-verified certificate).  Default `1`
(a trivial — never-binding — bound) for `q` outside the certified range. -/
def subL2 : ℕ → ℚ
  | 5  => 20252 / 100000
  | 7  => 34068 / 100000
  | 9  => 44652 / 100000
  | 11 => 51723 / 100000
  | 13 => 57024 / 100000
  | _  => 1

/-- The certified gap lower bound at `q`: `1 − subL2 q`.
(Uses `λ₁ = 1` exactly, the `s = 1` value the certificate confirms to `1e-12`;
the certificate's `gap_lo = 1 − l2_hi/l1_lo` with `l1_lo → 1` is bounded below by
this `1 − subL2 q` because `l1_lo ≤ 1` would only make the true `gap_lo` larger —
here we use the conservative `1 − subL2 q ≤ gap_lo`.) -/
def gapLB (q : ℕ) : ℚ := 1 - subL2 q

/-- The uniform lower-bound constant: the certified gap at the largest `q` in range
(`q = 13`), rounded DOWN to a clean rational.  `42976/100000 = 0.42976`. -/
def gapUniform : ℚ := 42976 / 100000

/-! ## §1.  Per-`q` certified gap lower bounds (each matches the table). -/

theorem gap_lb_q5  : gapLB 5  ≥ 79747 / 100000 := by norm_num [gapLB, subL2]
theorem gap_lb_q7  : gapLB 7  ≥ 65932 / 100000 := by norm_num [gapLB, subL2]
theorem gap_lb_q9  : gapLB 9  ≥ 55347 / 100000 := by norm_num [gapLB, subL2]
theorem gap_lb_q11 : gapLB 11 ≥ 48277 / 100000 := by norm_num [gapLB, subL2]
theorem gap_lb_q13 : gapLB 13 ≥ 42976 / 100000 := by norm_num [gapLB, subL2]

/-! ## §2.  The uniform `|λ₂|` ceiling and the uniform gap floor. -/

/-- Every certified `|λ₂(q)|` upper bound is `≤ 57024/100000` (the largest, at `q=13`). -/
theorem subL2_le_uniform : ∀ q ∈ Qrange, subL2 q ≤ 57024 / 100000 := by
  intro q hq
  fin_cases hq <;> norm_num [subL2]

/-- **★ UNIFORM SPECTRAL-GAP LOWER BOUND (goal P1).**
For every odd `q ∈ {5,7,9,11,13}`, the certified finite-`N` truncation spectral
gap of the Rosen/Hecke transfer operator at `s = 1` is at least `gapUniform =
0.42976`.  (Uniform over the certified range; the gap DECREASES in `q`, so this
floor is attained, to rounding, at `q = 13`.) -/
theorem uniform_gap_lower_bound : ∀ q ∈ Qrange, gapLB q ≥ gapUniform := by
  intro q hq
  have h := subL2_le_uniform q hq
  unfold gapLB gapUniform
  linarith

/-- The uniform floor is positive (the route is NOT blocked over this range). -/
theorem gapUniform_pos : (0 : ℚ) < gapUniform := by norm_num [gapUniform]

/-- Equivalent `|λ₂|` form: a uniform spectral RADIUS-2 ceiling strictly below `1`,
the actual certified obstruction.  For every `q ∈ Qrange`, `subL2 q ≤ 57024/100000 < 1`. -/
theorem subL2_lt_one : ∀ q ∈ Qrange, subL2 q < 1 := by
  intro q hq
  have h := subL2_le_uniform q hq
  linarith

end UniformGap

-- ════════════ AXIOM AUDIT ════════════
#print axioms UniformGap.uniform_gap_lower_bound
#print axioms UniformGap.subL2_le_uniform
#print axioms UniformGap.gapUniform_pos
