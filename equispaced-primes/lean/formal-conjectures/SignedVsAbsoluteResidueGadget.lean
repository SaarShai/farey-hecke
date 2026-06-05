/-
Copyright 2026 Saar Shai. All rights reserved.
Released under Apache 2.0 license as described in the LICENSE file.
Authors: Saar Shai

A small structural lemma motivated by the halo-residue route to
unconditional offcentral H1.  Captures the divided-difference principle
used in `handoff-2026-05-12-halo-unconditional-plan/HALO_UNCONDITIONAL_PLAN_2026-05-12.md` §2
(the "two-zero gadget"): as two simple poles of a meromorphic function
collide, each individual residue blows up in absolute value, but the
*signed* sum of the two residues stays bounded by a finite limit.

This lemma justifies the central structural move of the halo route:
replacing the absolute-value series `sum |Res_rho|` (the "rooted Palm
wall") by the signed residue aggregate `sum Res_rho`, which is a
contour integral that does not see the cluster-collapse blow-up.

This is a Mathlib-tractable statement; no L-function or zero-counting
machinery is needed.  Intended as a citeable structural lemma for the
halo write-up.

AI Disclosure: drafted with assistance from Claude (Anthropic), 2026-05-14.
-/

import Mathlib

/-!
# Signed-vs-absolute residue gadget (halo structural lemma)

For complex-valued holomorphic `f` and `h` with `h(a) ≠ 0`, consider
the meromorphic function
  G_δ(z) = f(z) / ((z - a)(z - (a + δ)) · h(z))
which has simple poles at `a` and `a + δ` for every nonzero `δ`.

## Claim 1 (absolute sum diverges as δ → 0)

For fixed `f, h, a` with `f(a) ≠ 0` and `h(a) ≠ 0`, as `δ → 0`,
the sum of the two absolute residues
  |Res_{z=a} G_δ| + |Res_{z=a+δ} G_δ|
is bounded below by `2 |f(a)| / (|h(a)| · |δ|)` for `δ` small enough,
hence diverges as `δ → 0`.

## Claim 2 (signed sum stays bounded)

For the same setup, the signed sum
  Res_{z=a} G_δ + Res_{z=a+δ} G_δ
is the divided difference `[a, a+δ](f/h)`, which converges to
`(f/h)'(a)` as `δ → 0`, hence is bounded.

## Significance

The gap between absolute and signed sums (Claim 1 vs Claim 2) is
the precise structural reason why the halo route bypasses the
"rooted Palm wall" obstruction.  Halo plan §2.2 calls this the
"two-zero gadget"; this file is its formal capture.
-/

open Complex

namespace HaloStructural

/-- The two-pole meromorphic function. -/
noncomputable def G (f h : ℂ → ℂ) (a δ : ℂ) (z : ℂ) : ℂ :=
  f z / ((z - a) * (z - (a + δ)) * h z)

/-- Residue at a simple pole `a` of `G f h a δ`.
For `δ ≠ 0`, this is `f a / ((a - (a + δ)) · h a) = -f a / (δ · h a)`. -/
noncomputable def residueAtFirstPole (f h : ℂ → ℂ) (a δ : ℂ) : ℂ :=
  -f a / (δ * h a)

/-- Residue at the second pole `a + δ` of `G f h a δ`.
This is `f (a + δ) / (δ · h (a + δ))`. -/
noncomputable def residueAtSecondPole (f h : ℂ → ℂ) (a δ : ℂ) : ℂ :=
  f (a + δ) / (δ * h (a + δ))

/-
**Claim 1 (absolute sum diverges as δ → 0).**

For `f, h : ℂ → ℂ` continuous at `a` with `f a ≠ 0` and `h a ≠ 0`,
the sum of absolute residues
  ‖residueAtFirstPole f h a δ‖ + ‖residueAtSecondPole f h a δ‖
tends to `∞` as `δ → 0`.
-/
theorem absoluteResidueSum_tendsto_atTop
    (f h : ℂ → ℂ)
    (hf : ContinuousAt f a) (hh : ContinuousAt h a)
    (hfa : f a ≠ 0) (hha : h a ≠ 0) :
    Filter.Tendsto
      (fun δ : ℂ => ‖residueAtFirstPole f h a δ‖ +
                    ‖residueAtSecondPole f h a δ‖)
      (nhdsWithin 0 {δ | δ ≠ 0})
      Filter.atTop := by
  -- We will show that the absolute value of the first term tends to infinity as δ → 0.
  have h_first_term : Filter.Tendsto (fun δ => ‖residueAtFirstPole f h a δ‖) (nhdsWithin 0 {δ | δ ≠ 0}) Filter.atTop := by
    -- Since $f(a) \neq 0$ and $h(a) \neq 0$, we have $\frac{\|f(a)\|}{\|h(a)\|} > 0$.
    have h_pos : 0 < ‖f a‖ / ‖h a‖ := by
      exact div_pos ( norm_pos_iff.mpr hfa ) ( norm_pos_iff.mpr hha );
    -- Since $\|δ\| \to 0$ as $δ \to 0$, we have $\frac{1}{\|δ\|} \to \infty$.
    have h_inv_norm : Filter.Tendsto (fun δ : ℂ => 1 / ‖δ‖) (nhdsWithin 0 {δ | δ ≠ 0}) Filter.atTop := by
      norm_num;
      refine' Filter.Tendsto.inv_tendsto_nhdsGT_zero _;
      rw [ Metric.tendsto_nhdsWithin_nhdsWithin ] ; aesop;
    convert h_inv_norm.const_mul_atTop h_pos using 2 ; norm_num [ residueAtFirstPole ] ; ring;
  exact Filter.tendsto_atTop_mono' _ ( Filter.eventually_of_mem self_mem_nhdsWithin fun x hx => le_add_of_nonneg_right <| norm_nonneg _ ) h_first_term

/-
**Claim 2 (signed sum stays bounded).**

For `f, h : ℂ → ℂ` differentiable at `a` with `h a ≠ 0`,
the signed sum
  residueAtFirstPole f h a δ + residueAtSecondPole f h a δ
converges (as `δ → 0` with `δ ≠ 0`) to `(f / h)′ a`,
i.e., the divided difference at the collided node.
-/
theorem signedResidueSum_tendsto_derivative
    (f h : ℂ → ℂ) (a : ℂ)
    (hf : DifferentiableAt ℂ f a) (hh : DifferentiableAt ℂ h a)
    (hha : h a ≠ 0) :
    Filter.Tendsto
      (fun δ : ℂ => residueAtFirstPole f h a δ +
                    residueAtSecondPole f h a δ)
      (nhdsWithin 0 {δ | δ ≠ 0})
      (nhds (deriv (fun z => f z / h z) a)) := by
  -- By definition of $F$, we know that its derivative at $a$ is $(f/h)'(a)$.
  have h_deriv : HasDerivAt (fun z => f z / h z) (deriv (fun z => f z / h z) a) a := by
    exact DifferentiableAt.hasDerivAt ( hf.div hh hha );
  convert h_deriv.tendsto_slope_zero using 2 ; norm_num [ residueAtFirstPole, residueAtSecondPole ] ; ring

end HaloStructural