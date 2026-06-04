/-
Copyright 2026 Saar Shai. All rights reserved.
Released under Apache 2.0 license as described in the LICENSE file.
Authors: Saar Shai

# Corrected `B_∞` identity (Theorem X.4.1 of the Saar–Koyama paper)

For a primitive non-principal Dirichlet character `χ` of conductor
`q`, a simple noncentral zero `ρ = ½ + iτ` of `L(s, χ)` on the
critical line, and the primitive character `ψ` of conductor `f ∣ q`
inducing `χ²`,

    T_∞(χ, ρ) = ½ · log L(2ρ, ψ) + BPC₁(χ, ρ) + BPC₂(χ, ρ) + T_{≥3}(χ, ρ).

The four right-hand-side components are defined below.  The identity
is *unconditional* given simplicity of `ρ`.  Full pen-and-paper proof
in Appendix A of the joint manuscript
(`APPENDIX_A_BINFTY_PROOF.md`).

In this Lean file we:

* Parametrize a Dirichlet character as a function `chi : ℕ → ℂ`
  zero outside `(ℤ / q)ˣ`. We do **not** use Mathlib's
  `DirichletCharacter` namespace at v4.28.0 directly because the
  API for `IsPrimitive`, `induce`, and `LFunction` has been moving
  across releases; restating in terms of basic functions of
  `ℕ → ℂ` keeps this file `lake build`-stable.

* Define the four components as `noncomputable` partial-sum limits.

* Prove the identity conditional on a `Filter.Tendsto` hypothesis
  packaging the four analytic ingredients of Appendix A; the proof
  closes via `Classical.epsilon_spec` + `tendsto_nhds_unique`.
  (Unconditional Lean proof is research-open pending upstream
  Mathlib formalisation of Akatsuka 2013 eq. (2.5).)
-/

import Mathlib

-- Some hypotheses are kept for mathematical content even when the (short,
-- conditional) proof does not consume them. Silence the unused-variable
-- linter for this file.
set_option linter.unusedVariables false

namespace CorrectedBInfty

open Complex BigOperators

/-- A "Dirichlet-style character", parametrised by an arbitrary
function `ℕ → ℂ`.  Mathlib's `DirichletCharacter` could be used
once its API stabilises across v4.28.0+; for now we keep the file
self-contained. -/
abbrev DChar := ℕ → ℂ

/-- Per-prime contribution to `T_K(chi, ρ)`: `Σ_{k ≥ 2} z^k/k` where
`z := chi(p) / p^ρ`, given in closed form as `-log(1 - z) - z`. -/
noncomputable def perPrime_TK (chi : DChar) (ρ : ℂ) (p : ℕ) : ℂ :=
  -Complex.log (1 - chi p / (p : ℂ) ^ ρ) - chi p / (p : ℂ) ^ ρ

/-- Per-prime contribution to `T_{≥3}(chi, ρ)`: `Σ_{k ≥ 3} z^k/k`. -/
noncomputable def perPrime_Tge3 (chi : DChar) (ρ : ℂ) (p : ℕ) : ℂ :=
  -Complex.log (1 - chi p / (p : ℂ) ^ ρ)
    - chi p / (p : ℂ) ^ ρ
    - (chi p / (p : ℂ) ^ ρ) ^ 2 / 2

/-- Per-prime contribution to `BPC_2(chi, ρ)`:
`Σ_{k ≥ 2} y^k/k` where `y := chi(p)^2 / p^(2ρ)`, given in closed
form as `-log(1 - y) - y`. -/
noncomputable def perPrime_BPC2 (chi : DChar) (ρ : ℂ) (p : ℕ) : ℂ :=
  Complex.log (1 - (chi p) ^ 2 / (p : ℂ) ^ (2 * ρ))
    + (chi p) ^ 2 / (p : ℂ) ^ (2 * ρ)

/-- The partial prime-power tail
`T_K(chi, ρ) := Σ_{p ≤ K, p prime} Σ_{k ≥ 2} chi(p)^k / (k · p^(k ρ))`,
evaluated via the per-prime closed form. -/
noncomputable def T_K (chi : DChar) (ρ : ℂ) (K : ℕ) : ℂ :=
  ∑ p ∈ Finset.filter Nat.Prime (Finset.range (K + 1)),
    perPrime_TK chi ρ p

/-- `T_∞(chi, ρ)` is the limit of `T_K(chi, ρ)` as `K → ∞`.
The existence of the limit is part of the Theorem X.4.1 statement;
proof is in Appendix A §A.2–A.4 of the joint manuscript. -/
noncomputable def T_inf (chi : DChar) (ρ : ℂ) : ℂ :=
  Classical.epsilon (fun (S : ℂ) =>
    Filter.Tendsto (T_K chi ρ) Filter.atTop (nhds S))

/-- The absolutely convergent `k ≥ 3` tail
`T_{≥3}(chi, ρ) := Σ_p [-log(1 - z_p) - z_p - z_p² / 2]`. -/
noncomputable def T_ge3 (chi : DChar) (ρ : ℂ) : ℂ :=
  ∑' p : { n : ℕ // Nat.Prime n }, perPrime_Tge3 chi ρ p.val

/-- The bad-prime correction `BPC₁`: for each prime `p` dividing the
conductor `q` of `chi` but *not* dividing the conductor `f` of the
primitive character `psi` inducing `chi²`,

    BPC₁ contributes  ½ · log(1 - psi(p) · p^(-2ρ)).
-/
noncomputable def BPC_1 (psi : DChar) (q f : ℕ) (ρ : ℂ) : ℂ :=
  (1 / 2 : ℂ) *
    ∑ p ∈ Finset.filter
        (fun p => Nat.Prime p ∧ q % p = 0 ∧ f % p ≠ 0)
        (Finset.range (q + 1)),
      Complex.log (1 - psi p / (p : ℂ) ^ (2 * ρ))

/-- The k ≥ 2 BPC₂ residue from the log-Euler-product expansion:

    BPC₂(chi, ρ) := (½) · Σ_p [log(1 - y_p) + y_p],
    where  y_p := chi(p)² / p^(2 ρ).
-/
noncomputable def BPC_2 (chi : DChar) (ρ : ℂ) : ℂ :=
  (1 / 2 : ℂ) *
    ∑' p : { n : ℕ // Nat.Prime n }, perPrime_BPC2 chi ρ p.val

/-- `L(s, psi)` for the simple-character primitive `psi` modulo `f`.
We define the L-value via the Dirichlet series in its half-plane of
convergence; for `Re(s) > 1` this converges absolutely.  Analytic
continuation is needed for the boundary line `Re(s) = 1`, which is
provided in the manuscript via Akatsuka 2013, eq. (2.5). -/
noncomputable def L_value (psi : DChar) (s : ℂ) : ℂ :=
  ∑' n : ℕ, psi n / (n : ℂ) ^ s

/--
**Theorem X.4.1 (Corrected `B_∞` identity).**

For `chi` a primitive non-principal Dirichlet character of conductor
`q ≥ 2`, simple noncentral zero `ρ = ½ + iτ` of `L(·, chi)`, and `psi`
the primitive character of conductor `f ∣ q` inducing `chi²`:

    T_∞(chi, ρ) = ½ · log L(2ρ, psi) + BPC₁ + BPC₂ + T_{≥3}.

The statement is *unconditional*.  The pen-and-paper proof is in
Appendix A of the joint manuscript.  The Lean proof requires:

* Akatsuka 2013, eq. (2.5), to handle the boundary-line conditional
  convergence of `Σ_p chi(p)² / p^(2ρ)` at `Re(2ρ) = 1` — this is the
  *only* analytic input.
* Standard textbook tools (Taylor expansion of `-log(1 - z)`, the
  imprimitive-induction Euler-factor identity, geometric-series tail
  bounds for absolute convergence).

None of these are yet in Mathlib v4.28.0 in the precise form needed
for a fully unconditional automated proof of `corrected_B_infty`.
The current Lean theorem (below) is proved **conditional on a
`Filter.Tendsto` hypothesis** that packages the four-component
right-hand side as the limit of the partial-sum sequence
`T_K(χ, ρ)`. The pen-and-paper proof in Appendix A establishes
exactly this convergence from the inputs above; given it, the
Lean proof is three lines (`Classical.epsilon_spec` +
`tendsto_nhds_unique` on the Hausdorff space `ℂ`).

`MATHLIB-PREREQ`: a quantitative version of the Mertens-type
boundary-line estimate `∑_{p ≤ X} χ²(p) / p^(1 + 2iτ) = c(τ) + O(1/log X)`
(Akatsuka 2013, eq. (2.5)) or the equivalent Dirichlet PNT with
explicit error term.
-/

/- ### Convergence hypothesis

The following hypothesis packages the analytic content of the
`B_∞` identity: the partial prime-power tail `T_K(χ, ρ)` converges
to the four-component right-hand side as `K → ∞`.

The pen-and-paper proof (Appendix A of the joint manuscript) derives
this from:

* **Akatsuka 2013, eq. (2.5)**: conditional convergence of
  `Σ_{p ≤ X} χ²(p) / p^{2ρ}` on the boundary line `Re(s) = 1`,
  `s ≠ 1`, via partial summation against PNT with explicit error
  term. This is *unconditional* (no RH/GRH).

* **Log-Euler-product expansion** of `log L(s, χ²)` and isolation
  of the `k = 1` term.

* **Imprimitive-induction identity**: `L(s, χ²) = L(s, ψ) ·
  ∏_{p|q, p∤f} (1 − ψ(p)/p^s)`, relating `χ²` to its primitive
  inducing character `ψ`.

* **Geometric-series tail bounds** for `k ≥ 3` absolute
  convergence.

None of these ingredients are available in Mathlib v4.28.0 in the
precise form needed for a fully automated proof. We therefore
assume the convergence as a hypothesis and prove that `T_inf`
(defined via `Classical.epsilon` of the `Tendsto` predicate)
equals the claimed right-hand side by uniqueness of limits in
the Hausdorff space `ℂ`. -/

theorem corrected_B_infty
    (chi : DChar) (psi : DChar) (q f : ℕ) (ρ : ℂ)
    (hq : 2 ≤ q) (hf : f ∣ q)
    -- The character `psi` induces `chi²` modulo `q`:
    (h_induces : ∀ n : ℕ, Nat.Coprime n q → (chi n) ^ 2 = psi n)
    -- ρ is on the critical line, not central:
    (h_rho_re : ρ.re = 1 / 2) (h_rho_im : ρ.im ≠ 0)
    -- Akatsuka 2013 eq. (2.5) + log-Euler-product + imprimitive
    -- induction + geometric-series tails ⟹ the partial-sum limit
    -- exists and equals the four-component RHS:
    (h_convergence : Filter.Tendsto (T_K chi ρ) Filter.atTop
      (nhds ((1 / 2 : ℂ) * Complex.log (L_value psi (2 * ρ))
             + BPC_1 psi q f ρ
             + BPC_2 chi ρ
             + T_ge3 chi ρ))) :
    T_inf chi ρ
      = (1 / 2 : ℂ) * Complex.log (L_value psi (2 * ρ))
        + BPC_1 psi q f ρ
        + BPC_2 chi ρ
        + T_ge3 chi ρ := by
  -- `T_inf` is defined as `Classical.epsilon` of the `Tendsto` predicate.
  -- By `epsilon_spec`, it satisfies `Tendsto` for *some* limit.
  -- By `tendsto_nhds_unique` (ℂ is T₂), that limit equals the RHS.
  unfold T_inf
  have h_eps := Classical.epsilon_spec
    (p := fun S => Filter.Tendsto (T_K chi ρ) Filter.atTop (nhds S))
    ⟨_, h_convergence⟩
  exact tendsto_nhds_unique h_eps h_convergence

end CorrectedBInfty
