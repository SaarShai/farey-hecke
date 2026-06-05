---
title: "DPAC finite phase bridge moonshot"
date: 2026-05-11
type: theorem-packaging
tier: claim-safe
scope: "Separate unconditional finite exponential-polynomial facts from zeta-zero phase inputs"
sources:
  - formal-conjectures/DPAC_NEXT_STEPS_2026-05-10.md
  - formal-conjectures/DPAC_full.lean
  - formal-conjectures/DPAC_HYGIENE_STATUS_2026-05-10.md
  - handoff-2026-05-09-followup/KOYAMA_RESEARCH_DECISION_MEMO_2026-05-10.md
tags: [dpac, phase-bridge, exponential-polynomial, zeta-zeros, lean-plan]
---

# DPAC finite phase bridge moonshot

## Status

Claim-safe documentation only.

No Lean files were edited. No Lean build was run; local `lean` and `lake`
were not found in this environment.

This note deprecates the idea behind `dpac_of_LI` as stated. It does not
silently rename it. A future code patch should leave a loud deprecation trail
and introduce a separate finite log-prime phase theorem. The analytic layer
below is a proof sketch and theorem-statement plan, not a Lean-verified
artifact.

## Claim

For fixed `K` and fixed real `beta`, the function

```text
C_{K,beta}(gamma)
  = sum_{2 <= n <= K} mu(n) n^(-beta) exp(-i gamma log n)
```

is a finite exponential polynomial in the real variable `gamma`.

Claim-safe analytic proof sketch:

```text
B_{K,beta} = { gamma in R : C_{K,beta}(gamma) = 0 }
```

is discrete, hence countable and Lebesgue measure zero, unless the associated
entire exponential polynomial is identically zero. For the actual Mobius
polynomial and `K >= 2`, the planned non-identity lemma would imply that the
bad gamma set is measure zero for every fixed real `beta`.

This is not DPAC. A measure-zero exceptional subset of `R` can still contain
specified zeta-zero ordinates. Pointwise DPAC at zeta zeros still needs one
of:

- a direct finite log-prime phase avoidance hypothesis;
- an external theorem proving that zeta-zero ordinates avoid the finite phase
  zero locus;
- certified external zeta-zero sampling for a finite height range.

## Evidence

Before the 2026-05-11 patch, `DPAC_full.lean` defined the unsafe bridge in
this shape:

```lean
def moebiusDirichletPoly (K : Nat) (s : Complex) : Complex := ...

def LinearIndependenceHypothesis : Prop := ...

-- former bridge name: dpac_of_LI
    (hLI : LinearIndependenceHypothesis)
    (K : Nat) (hK : K >= 2)
    (rho : Complex) (hrho : riemannZeta rho = 0)
    (hrho_nontrivial : 0 < rho.re /\ rho.re < 1) :
    moebiusDirichletPoly K rho != 0 := by
  sorry
```

The hygiene memo and Koyama decision memo agree that this bridge is unsafe:
LI among zeta-zero ordinates does not control the finite phases
`exp(-i gamma log p)` for primes `p <= K`.

The unconditional fixed-line fact is independent of zeta:

```text
F_{K,beta}(z)
  = sum_{2 <= n <= K} mu(n) n^(-beta) exp(-i z log n)
```

is entire in `z`. If `F_{K,beta}` is not identically zero, the identity
theorem gives isolated complex zeros. Intersecting with the real axis gives
no finite accumulation points; every compact interval contains finitely many
bad real `gamma`, so `B_{K,beta}` is countable and measure zero.

For the actual Mobius polynomial with `K >= 2`, non-identity follows from
linear independence of exponentials with distinct frequencies `log n`.
Equivalently, along `z = i t`, the largest squarefree `n <= K` with
`mu(n) != 0` dominates as `t -> +infty`.

## Safe Theorem Layers

### Layer 1: pointwise phase avoidance

This is the safe replacement for the false LI bridge.

```text
LogPrimePhaseAvoidance(K, rho):
  C_{K,rho.re}(rho.im) != 0
```

or equivalently, with `P_K = {p prime : p <= K}`,

```text
Q_{K,beta}(z)
  = sum_{2 <= n <= K, squarefree}
      mu(n) n^(-beta) product_{p | n} z_p

LogPrimePhaseAvoidance(K, rho):
  Q_{K,rho.re}((exp(-i rho.im log p))_{p in P_K}) != 0
```

The theorem is nearly by unfolding:

```text
dpac_of_logPrimePhaseAvoidance:
  zeta(rho) = 0
  and 0 < Re(rho) < 1
  and LogPrimePhaseAvoidance(K, rho)
  imply moebiusDirichletPoly(K, rho) != 0.
```

### Layer 2: almost-everywhere gamma avoidance

This is unconditional, but it is not a zeta-zero theorem.

```text
badGammaSet_discrete_or_identically_zero:
  for fixed K,beta,
  either F_{K,beta} is identically zero
  or {gamma : C_{K,beta}(gamma) = 0} has no finite accumulation point.

badGammaSet_measureZero_of_not_identically_zero:
  if F_{K,beta} is not identically zero,
  volume({gamma : C_{K,beta}(gamma) = 0}) = 0.

ae_logPrimePhaseAvoidance_fixed_beta:
  for fixed K >= 2 and beta,
  for almost every gamma, C_{K,beta}(gamma) != 0.
```

This layer is useful hygiene: it explains why random ordinate sampling should
miss bad phases. It cannot prove that the deterministic zeta-zero ordinate
sequence misses them.

### Layer 3: external zeta-zero sampling bridge

Finite computations belong here, not inside an LI theorem.

```text
dpac_of_certifiedZetaZeroSample:
  if certified boxes cover all zeta zeros in a finite height range
  and interval evaluation proves moebiusDirichletPoly K avoids 0 on each box,
  then DPAC holds for that finite sample/range.
```

The existing project context reports 100-digit interval arithmetic for
`K in {10,20,50}` at the first 100 zeta zeros, with `300/300` certified
nonvanishing cases. That is evidence and finite verification, not an
unconditional all-zero theorem.

### Layer 4: external all-zero phase theorem

Only this layer can replace the missing global bridge.

```text
ExternalZetaZeroPhaseAvoidance:
  forall K rho,
    K >= 2 ->
    zeta(rho) = 0 ->
    0 < Re(rho) < 1 ->
    LogPrimePhaseAvoidance(K, rho).

dpac_of_externalZetaZeroPhaseAvoidance:
  ExternalZetaZeroPhaseAvoidance -> full DPAC.
```

This should be treated as a named external analytic input until proved.

## Exact Theorem Statement Candidates

Lean names below are statement candidates. Names for measure/discreteness
may need Mathlib adjustment.

```lean
noncomputable def gammaExponentialPoly (K : ℕ) (β γ : ℝ) : ℂ :=
  ∑ k ∈ Finset.range (K - 1),
    (ArithmeticFunction.moebius (k + 2) : ℂ) *
      (((k + 2 : ℝ) ^ (-β) : ℝ) : ℂ) *
      Complex.exp (-(Complex.I) * (γ : ℂ) * Complex.log (k + 2 : ℂ))

def badGammaSet (K : ℕ) (β : ℝ) : Set ℝ :=
  {γ | gammaExponentialPoly K β γ = 0}

def HasNoFiniteAccumulation (S : Set ℝ) : Prop :=
  ∀ x : ℝ, ∃ ε > 0, (S ∩ Metric.ball x ε).Finite

theorem badGammaSet_discrete_or_identically_zero
    (K : ℕ) (β : ℝ) :
    (∀ γ : ℝ, gammaExponentialPoly K β γ = 0) ∨
    HasNoFiniteAccumulation (badGammaSet K β) := by
  -- Entire identity theorem for finite exponential polynomials.
  sorry

theorem badGammaSet_measureZero_of_not_identically_zero
    (K : ℕ) (β : ℝ)
    (hnot : ¬ (∀ γ : ℝ, gammaExponentialPoly K β γ = 0)) :
    MeasureTheory.volume (badGammaSet K β) = 0 := by
  -- Local finiteness on compact intervals -> countable -> null.
  sorry

theorem gammaExponentialPoly_not_identically_zero
    (K : ℕ) (hK : 2 ≤ K) (β : ℝ) :
    ¬ (∀ γ : ℝ, gammaExponentialPoly K β γ = 0) := by
  -- Linear independence of exp(-i gamma log n), or largest squarefree n
  -- after evaluating the entire function on z = i t.
  sorry

theorem badGammaSet_measureZero_moebius
    (K : ℕ) (hK : 2 ≤ K) (β : ℝ) :
    MeasureTheory.volume (badGammaSet K β) = 0 := by
  exact badGammaSet_measureZero_of_not_identically_zero K β
    (gammaExponentialPoly_not_identically_zero K hK β)

def LogPrimePhaseAvoidance (K : ℕ) (ρ : ℂ) : Prop :=
  gammaExponentialPoly K ρ.re ρ.im ≠ 0

theorem moebiusDirichletPoly_eq_gammaExponentialPoly
    (K : ℕ) (ρ : ℂ) :
    moebiusDirichletPoly K ρ =
      gammaExponentialPoly K ρ.re ρ.im := by
  -- Positive real bases only; expand n^(-rho) into modulus and phase.
  sorry

theorem dpac_of_logPrimePhaseAvoidance
    (K : ℕ) (hK : K ≥ 2)
    (ρ : ℂ) (hρ : riemannZeta ρ = 0)
    (hρ_nontrivial : 0 < ρ.re ∧ ρ.re < 1)
    (hphase : LogPrimePhaseAvoidance K ρ) :
    moebiusDirichletPoly K ρ ≠ 0 := by
  rw [moebiusDirichletPoly_eq_gammaExponentialPoly K ρ]
  exact hphase

theorem ae_logPrimePhaseAvoidance_fixed_beta
    (K : ℕ) (hK : 2 ≤ K) (β : ℝ) :
    ∀ᵐ γ ∂MeasureTheory.volume, gammaExponentialPoly K β γ ≠ 0 := by
  -- From badGammaSet_measureZero_moebius.
  sorry
```

Sampling bridge candidate:

```lean
theorem dpac_of_certifiedZetaZeroSample
    (K : ℕ) (hK : K ≥ 2)
    (T : ℝ) (sample : Finset ℂ)
    (box : ℂ → Set ℂ)
    (hcover :
      ∀ ρ : ℂ,
        riemannZeta ρ = 0 →
        0 < ρ.re ∧ ρ.re < 1 →
        0 < ρ.im ∧ ρ.im ≤ T →
        ∃ z ∈ sample, ρ ∈ box z)
    (havoid :
      ∀ z ∈ sample, ∀ s ∈ box z,
        moebiusDirichletPoly K s ≠ 0) :
    ∀ ρ : ℂ,
      riemannZeta ρ = 0 →
      0 < ρ.re ∧ ρ.re < 1 →
      0 < ρ.im ∧ ρ.im ≤ T →
      moebiusDirichletPoly K ρ ≠ 0 := by
  intro ρ hρ hstrip hheight
  rcases hcover ρ hρ hstrip hheight with ⟨z, hzsample, hρb⟩
  exact havoid z hzsample ρ hρb
```

External theorem bridge candidate:

```lean
def ExternalZetaZeroPhaseAvoidance : Prop :=
  ∀ (K : ℕ) (ρ : ℂ),
    K ≥ 2 →
    riemannZeta ρ = 0 →
    0 < ρ.re ∧ ρ.re < 1 →
    LogPrimePhaseAvoidance K ρ

theorem dpac_of_externalZetaZeroPhaseAvoidance
    (hbridge : ExternalZetaZeroPhaseAvoidance)
    (K : ℕ) (hK : K ≥ 2)
    (ρ : ℂ) (hρ : riemannZeta ρ = 0)
    (hρ_nontrivial : 0 < ρ.re ∧ ρ.re < 1) :
    moebiusDirichletPoly K ρ ≠ 0 :=
  dpac_of_logPrimePhaseAvoidance K hK ρ hρ hρ_nontrivial
    (hbridge K ρ hK hρ hρ_nontrivial)
```

Density comparison should remain separate:

```lean
theorem density_zero_bad_zeros_from_counts
    (K : ℕ) (hK : 2 ≤ K)
    (bad zetaCount : ℝ → ℝ)
    (hbad :
      ∃ A T0 : ℝ, 0 ≤ A ∧
        ∀ T ≥ T0, bad T ≤ A * T * Real.log K)
    (hzeta :
      ∃ B : ℝ, 0 < B ∧
        Filter.Tendsto
          (fun T : ℝ => zetaCount T / (T * Real.log T))
          Filter.atTop (nhds B))
    (hpos :
      Filter.Eventually (fun T : ℝ => 0 < zetaCount T) Filter.atTop) :
    Filter.Tendsto
      (fun T : ℝ => bad T / zetaCount T)
      Filter.atTop (nhds 0) := by
  -- Pure real-analysis comparison for fixed K.
  sorry
```

## Patch Plan

Future Lean patch should be explicit and breaking where necessary:

1. Add `gammaExponentialPoly`, `badGammaSet`, and the fixed-`beta`
   analytic lemmas above.
2. Add `LogPrimePhaseAvoidance` and `dpac_of_logPrimePhaseAvoidance`.
3. Deprecate `dpac_of_LI` loudly. Do not silently rename it.
   Suggested action:

```lean
/--
DEPRECATED 2026-05-11.
LI among zeta-zero ordinates does not imply finite log-prime phase avoidance.
Use `dpac_of_logPrimePhaseAvoidance`, or provide
`ExternalZetaZeroPhaseAvoidance`.
-/
@[deprecated dpac_of_logPrimePhaseAvoidance (since := "2026-05-11")]
-- former bridge name: dpac_of_LI
theorem dpac_of_logPrimePhaseAvoidance_or_external_phase ... := by
  -- historical scaffold only; do not cite as a valid LI bridge
  ...
```

If the old theorem statement cannot be proved without `sorry`, remove it in a
deliberate breaking patch and leave a searchable tombstone comment:

```lean
-- DPAC_LI_BRIDGE_DEPRECATED:
-- `dpac_of_LI` was removed because LI over ordinates is insufficient.
```

4. Rename the section title from `Linear Independence Hypothesis -> DPAC` to
   `Finite log-prime phase avoidance -> DPAC`.
5. Keep `LinearIndependenceHypothesis` only as background unless a real
   external theorem connects it to finite log-prime phases.
6. Keep `density_zero_from_growth_comparison` as an abstract counting lemma;
   do not present it as pointwise DPAC.

## Risks

- Almost-everywhere gamma avoidance does not imply avoidance at zeta-zero
  ordinates.
- The phrase "phase independence" is too vague unless it names the exact zero
  locus of `Q_{K,beta}`.
- Formalizing the analytic layer may require Mathlib support for identity
  theorems, entire finite exponential sums, local finiteness of zeros, and
  nullity of countable subsets of `R`.
- The equality between `moebiusDirichletPoly K rho` and
  `gammaExponentialPoly K rho.re rho.im` must respect Lean's complex-power
  conventions for positive real bases.
- Deprecating `dpac_of_LI` may break downstream references. That is desired:
  any downstream proof must choose a real phase hypothesis or a sampling
  certificate.

## Verification

Read:

- `formal-conjectures/DPAC_NEXT_STEPS_2026-05-10.md`
- `formal-conjectures/DPAC_full.lean`
- `formal-conjectures/DPAC_HYGIENE_STATUS_2026-05-10.md`
- `handoff-2026-05-09-followup/KOYAMA_RESEARCH_DECISION_MEMO_2026-05-10.md`

Additional context checked:

- `formal-conjectures/DPAC_dispatch_receipt.md`
- `formal-conjectures/DPAC_aristotle_result_extract/aristotle_dispatch_DPAC_aristotle/DPAC_context.md`

Commands/checks:

```text
rg -n "dpac_of_LI|LogPrime|Phase|c_K|zero|gamma" formal-conjectures/DPAC_full.lean
rg -n "sorry|axiom|admit|unsafe|dpac_of_LI" formal-conjectures/DPAC_full.lean
command -v lean || true
command -v lake || true
```

Result:

- `DPAC_full.lean` still has the two known `sorry` sites:
  `dpac_of_LI` and `dirichlet_polynomial_avoidance_conjecture`.
- No `axiom`, `admit`, or `unsafe` token was found in `DPAC_full.lean`.
- Local `lean` and `lake` were absent, so no build was attempted.

## Changed Files

- `formal-conjectures/DPAC_PHASE_BRIDGE_MOONSHOT_2026-05-11.md`
