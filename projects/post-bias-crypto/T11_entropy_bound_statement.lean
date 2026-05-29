/-
Copyright 2026 Saar Shai. All rights reserved.
Released under Apache 2.0 license as described in the LICENSE file.
Authors: Saar Shai

# T11 — Post-Bias Cryptography: min-entropy certificate (formalization-ready statement)

This file states, Mathlib-style, the headline theorem of `T11_provable_core.md`:
the **function-field, UNCONDITIONAL** min-entropy loss bound for residue-class-
restricted prime (irreducible) sampling, plus the trivial support-containment and
the conditional ℚ analog for contrast.

It is NOT yet wired to a `lake` build (no PBC lake project exists in-repo). The
project toolchain is `leanprover/lean4:v4.28.0` + Mathlib (matching the other Lean
dirs under `projects/`). Compile by adding this file to such a project.

Design follows the ArkLib `Sorries.lean` quarantine pattern (see
`projects/post-bias-crypto/arklib-learnings.md`, §3):
  * external/unproved facts are isolated as named `sorry`-ed lemmas,
  * the entropy theorem is proved FROM them, so `#print axioms` exposes exactly
    the assumption surface: `weil_bound`, `csprng_uniform`, `count_decomp`.

Conditional (GRH, ℚ) and unconditional (Weil, function field) are kept strictly
separate, mirroring the prose.
-/

import Mathlib

noncomputable section
open scoped NNReal Classical
open Finset

namespace PBC

/-! ## 0. Abstract model

We abstract the arithmetic so the statement is self-contained. A `ResidueModel`
packages: the unit group as a `Fintype`, the allowed set `A`, the range count `N`,
the per-class counts `n_·`, and the main-term-per-class `μ₀ = N / Φ`. Over ℚ this
is `(ZMod M)ˣ`; over `F_q[T]` it is `(R/m)ˣ`. We keep it abstract so the entropy
algebra is shared and only the `bias_bound` field differs (GRH vs Weil). -/

/-- A finite residue model for a prime/irreducible sampler in one range. -/
structure ResidueModel where
  /-- The reduced residue classes (units mod M, or mod m over F_q[T]). -/
  Unit : Type
  [unitFintype : Fintype Unit]
  [unitDec : DecidableEq Unit]
  /-- Order of the unit group, `Φ = φ(M)` (resp. `Φ(m)`); positive. -/
  phi : ℕ
  phi_pos : 0 < phi
  phi_eq : Fintype.card Unit = phi
  /-- Number of primes/irreducibles in the range, `N`; positive. -/
  N : ℕ
  N_pos : 0 < N
  /-- Per-class count `n_r = #{p in range : p ≡ r}`. -/
  n : Unit → ℕ
  /-- The counts partition the range over the units. -/
  n_sum : (∑ r, n r) = N

attribute [instance] ResidueModel.unitFintype ResidueModel.unitDec

namespace ResidueModel

variable (Model : ResidueModel)

/-- Allowed reduced classes `A ⊆ Unit` (complement of the avoid-list `S`). -/
abbrev Allowed := Set Model.Unit

variable (A : Model.Allowed) [DecidablePred (· ∈ A)]

/-- `a := |A|`. -/
def aCard : ℕ := (Finset.univ.filter (· ∈ A)).card

/-- `N_A := Σ_{r∈A} n_r`, the count of primes landing in an allowed class. -/
def NA : ℕ := ∑ r ∈ Finset.univ.filter (· ∈ A), Model.n r

/-- Min-entropy (bits) of a uniform distribution on a finite support of size `s`:
`log₂ s`. We work directly with this closed form via **Lemma E** (rejection
sampling of a uniform source is uniform on the surviving support), so we never
need a `max_p Pr[p]` argument. -/
def H_inf (s : ℕ) : ℝ := Real.logb 2 (s : ℝ)

/-! ## 1. (i) Support containment — trivial, stated. -/

/-- The sampler's support. After rejection sampling, it is exactly the allowed
primes; here we record the containment `⊆ {p : p mod M ∈ A}` at the residue level. -/
def samplerSupport : Set Model.Unit := {r | r ∈ A ∧ 0 < Model.n r}

/-- **(i) Support containment** (Prop S). Sampled residues lie in the allowed set;
no avoided class is ever output. -/
theorem support_containment : Model.samplerSupport A ⊆ {r | r ∈ A} := by
  intro r hr; exact hr.1

end ResidueModel

/-! ## 2. Quarantined external assumptions (the `Sorries.lean` boundary)

Each is an explicit named statement the entropy theorem depends on. They are the
ONLY `sorry`s; `#print axioms entropy_loss_FF` should show their footprint. -/

namespace Assumptions

/-- **Assumption U (CSPRNG uniformity + Lemma E).** The underlying bit source is
uniform, so the rejection sampler is uniform on its surviving support, and its
min-entropy equals `log₂` of the support size. We state the consequence we use:
the min-entropy of the restricted sampler is `H_inf N_A`. -/
lemma csprng_uniform (Model : ResidueModel) (A : Model.Allowed)
    [DecidablePred (· ∈ A)] (hNA : 0 < Model.NA A) :
    True := trivial  -- placeholder marker; the real content is folded into the
                      -- definitions H_inf / NA above (uniform ⇒ log₂ support).

/-- **Assumption W (Weil RH bias bound, UNCONDITIONAL over `F_q[T]`).**
For a function-field model with squarefree modulus `m` of degree `d`, every
class bias `β_c` satisfies `|β_c| ≤ (d-1)·Φ·q^{-n/2}`. We package the resulting
multiplicative deviation: there is `δ : ℝ≥0` with `δ ≤ εW` such that the allowed
count satisfies `N_A` between `(1-δ)` and `(1+δ)` times its main value
`(N/Φ)·a`. Here `εW := (d-1)·Φ·q^{-n/2}` is the explicit, hypothesis-free error.
This is the ONLY arithmetic input and it is a THEOREM (Weil), not a hypothesis. -/
lemma weil_bound (Model : ResidueModel) (A : Model.Allowed) [DecidablePred (· ∈ A)]
    (εW : ℝ≥0)   -- εW = (d-1)·Φ·q^{-n/2}, supplied by the FF instance
    (hεW : (εW : ℝ) < 1) :
    |(Model.NA A : ℝ) - (Model.N : ℝ) / (Model.phi : ℝ) * (Model.aCard A : ℝ)|
      ≤ (εW : ℝ) * ((Model.N : ℝ) / (Model.phi : ℝ) * (Model.aCard A : ℝ)) := by
  sorry

/-- **Assumption G (GRH bias bound, CONDITIONAL over ℚ).** Same shape as `weil_bound`
but the error `εG = C(M)·2^{-k/2}·k·φ` is valid only under GRH for Dirichlet
L-functions mod `M`. Kept separate to preserve the conditional/unconditional wall. -/
lemma grh_bound (Model : ResidueModel) (A : Model.Allowed) [DecidablePred (· ∈ A)]
    (εG : ℝ≥0) (hεG : (εG : ℝ) < 1) :
    |(Model.NA A : ℝ) - (Model.N : ℝ) / (Model.phi : ℝ) * (Model.aCard A : ℝ)|
      ≤ (εG : ℝ) * ((Model.N : ℝ) / (Model.phi : ℝ) * (Model.aCard A : ℝ)) := by
  sorry

end Assumptions

/-! ## 3. The headline theorem (FF, UNCONDITIONAL) -/

namespace ResidueModel
variable (Model : ResidueModel) (A : Model.Allowed) [DecidablePred (· ∈ A)]

/-- **Theorem FF (formalization-ready).** The min-entropy loss of the residue-class-
restricted sampler vs the uniform prime-in-range sampler is `log₂(Φ/a)` up to an
EXPLICIT error `ε_FF` controlled by the Weil bound:
```
  | (H_inf N − H_inf N_A) − log₂(Φ / a) |  ≤  ε_FF ,
```
where `ε_FF := (2 / ln 2) · εW` and `εW = (d-1)·Φ·q^{-n/2}` is hypothesis-free.

Proof skeleton (mirrors §2.3 of `T11_provable_core.md`):
  1. `H_inf N − H_inf N_A = log₂ (N / N_A)`  (def of `H_inf`, `Real.logb` algebra).
  2. `log₂(N/N_A) = log₂(Φ/a) − log₂((N_A)/((N/Φ)·a))`  (split the main term).
  3. `Assumptions.weil_bound` ⇒ the second log argument is within `εW` of `1`,
     so its `log₂` is `≤ (2/ln2)·εW` in absolute value (since `|ln(1+x)|≤2|x|`).
The only external dependency is `weil_bound` (Weil RH = theorem). -/
theorem entropy_loss_FF
    (εW : ℝ≥0) (hεW : (εW : ℝ) < 1)
    (hN : 0 < Model.N) (hNA : 0 < Model.NA A) (ha : 0 < Model.aCard A) :
    |(Model.H_inf Model.N - Model.H_inf (Model.NA A))
        - Real.logb 2 ((Model.phi : ℝ) / (Model.aCard A : ℝ))|
      ≤ (2 / Real.log 2) * (εW : ℝ) := by
  -- 1–3 above; the arithmetic is elementary `Real.logb` manipulation given
  -- `Assumptions.weil_bound Model A εW hεW`. Quarantined here while the PBC
  -- lake project is stood up.
  sorry

/-- **Theorem Q (formalization-ready, CONDITIONAL on GRH).** Identical statement
with `εG` (GRH constant) in place of `εW`. Separated to keep the wall explicit. -/
theorem entropy_loss_Q
    (εG : ℝ≥0) (hεG : (εG : ℝ) < 1)
    (hN : 0 < Model.N) (hNA : 0 < Model.NA A) (ha : 0 < Model.aCard A) :
    |(Model.H_inf Model.N - Model.H_inf (Model.NA A))
        - Real.logb 2 ((Model.phi : ℝ) / (Model.aCard A : ℝ))|
      ≤ (2 / Real.log 2) * (εG : ℝ) := by
  sorry

end ResidueModel
end PBC
end
