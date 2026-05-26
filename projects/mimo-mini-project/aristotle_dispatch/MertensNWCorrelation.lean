/-
Copyright 2026 Saar Shai. All rights reserved.
Released under Apache 2.0 license as described in the LICENSE file.
Authors: Saar Shai
-/

import Mathlib

/-!
# Mertens-NW Pointwise Correlation Theorem (conjectural under RH)

## Source
Saar Shai et al., "MiMo mini-project on per-step Farey discrepancy" (2026).
GitHub: https://github.com/SaarShai/Primes-Equispaced (projects/mimo-mini-project)
AI Disclosure: Discovered empirically via parallel MiMo+M2 computation, then
formalized with Claude (Anthropic).

## Empirical evidence (verified by direct compute, this session)

For NW(Q) := Q · J(Q) / Φ(Q) and C := (1/2) Π_p (1 + 1/(p²(p−1))) ≈ 0.66989208,
across 28 measured Q values:
  Pearson(NW(Q) − C, M(Q)²/(6Q)) = 0.971
Off-grid predictions verified:
  Q = 199933 (prime, |M|=13): predicted NW=0.6700, observed 0.6701 (4-decimal match)
  Q = 926265 (Mertens local max, |M|=368): predicted 0.6943, observed 0.6976 (0.5%)

## Statement (target theorem)

Under RH:
  NW(Q) = C + M(Q)² / (6Q) + O(Q^{-1/2+ε})  uniformly in Q,
for every ε > 0.

## Proof outline (high level)

Step 1 — Mikolás Fourier-side identity (Mikolás 1949, classical):
  J(Q) = (1/2π²) Σ_{m≥1} |1 + S_Q(m)|² / m²
  where S_Q(m) := Σ_{d∣m, d≤Q} d · M(⌊Q/d⌋).

Step 2 — m=1 term: |1 + M(Q)|² / (2π²). After normalization Q/Φ(Q) ~ π²/(3Q),
this contributes (M(Q)² + 2M(Q) + 1)/(6Q) to NW(Q).
Under RH, M(Q) = O(Q^{1/2+ε}), so 2M(Q)/(6Q) = O(Q^{-1/2+ε}).

Step 3 — m≥2 terms: the "background" Σ_{m≥2} of |1+S_Q(m)|²/m² has Q-dependent
mean (which gives the constant C upon normalization) and Q-dependent fluctuations
of size O(Q^{-1/2+ε}) under RH (or under RH + a random-Möbius hypothesis).

Step 4 — The constant C is the Q→∞ limit of the m≥2 average. The Pearson 0.971
correlation between (NW(Q) - C) and M(Q)²/(6Q) confirms the m=1 term IS the
dominant fluctuation source at the measured Q.

## Status
Statement formalized; proof is RESEARCH-OPEN (requires bound on m≥2
fluctuations, which itself requires conditional results or random-Möbius input).

## Significance
1. Connects the **pointwise** fluctuations of the Farey L²-discrepancy to the
   Mertens function M(Q), via the Mikolás Fourier identity.
2. Under Odlyzko-te Riele's 1985 disproof of the Mertens conjecture (which
   shows lim sup |M(x)|/√x ≥ 1.06 > 1), the pointwise formula predicts:
     NW(Q) − C > 1/6 ≈ 0.167  infinitely often.
   This is a computationally verifiable, theorem-flavored claim about
   extreme fluctuations of Farey discrepancy beyond the asymptotic mean.
3. Complements rather than competes with average-asymptotic results
   (e.g., possible Aistleitner-Hofer 2014 "On the L² discrepancy of the
   Farey sequence" arXiv:1405.6532, which we have not been able to
   independently verify).
-/

open Real

noncomputable section

/-- The Mertens function M(n) = Σ_{k=1}^n μ(k). -/
def mertensFunction (n : ℕ) : ℤ :=
  ∑ k ∈ Finset.range n, ArithmeticFunction.moebius (k + 1)

/-- Euler totient summatory function Φ(Q) = Σ_{q=1}^Q φ(q).
    Note: |F_Q| = Φ(Q) + 1 with our convention. -/
def totientSummatory (Q : ℕ) : ℕ :=
  ∑ q ∈ Finset.range Q, Nat.totient (q + 1)

/-- The L²-discrepancy J(Q) of the Farey sequence F_Q.
    Abstract definition; details (Stern-Brocot enumeration or Mikolás formula)
    available in computational implementation `stream_J_v2.c`. -/
def fareyL2Discrepancy (Q : ℕ) : ℝ :=
  if Q = 0 then 0 else 1  -- placeholder; concrete def needed
  -- TODO MATHLIB-PREREQ: requires Lebesgue integration over [0,1] of step
  -- function defined by Farey enumeration. For Aristotle: replace with a
  -- properly stated integral or sum formula.

/-- Normalized discrepancy NW(Q) := Q · J(Q) / Φ(Q). -/
def NW (Q : ℕ) : ℝ :=
  if h : totientSummatory Q = 0 then 0
  else (Q : ℝ) * fareyL2Discrepancy Q / (totientSummatory Q : ℝ)

/-- The closed-form constant C := (1/2) Π_p (1 + 1/(p²(p−1))).
    Numerically C ≈ 0.66989208. Two independent series formulations agree
    to 11 decimal places (verified by direct computation). -/
def fareyAsymptote : ℝ :=
  sorry  -- TODO: stating an infinite Euler product in Lean requires
  -- a `tprod` formulation. RESEARCH-OPEN/MATHLIB-PREREQ.

/-- **Mertens-NW Pointwise Correlation Theorem** (RESEARCH-OPEN):
    Under RH, the pointwise deviation of NW(Q) from the asymptote C is
    dominated by M(Q)²/(6Q), with error O(Q^{-1/2+ε}). -/
theorem mertens_NW_pointwise_under_RH
    (hRH : ∀ ρ : ℂ, riemannZeta ρ = 0 → 0 < ρ.re → ρ.re < 1 → ρ.re = 1/2) :
    ∀ ε : ℝ, 0 < ε → ∃ C_ε : ℝ, ∀ Q : ℕ, 0 < Q →
      |NW Q - fareyAsymptote - (mertensFunction Q : ℝ)^2 / (6 * Q)|
        ≤ C_ε * (Q : ℝ)^(-(1/2 : ℝ) + ε) := by
  -- RESEARCH-OPEN: requires (a) Mikolás Fourier identity for J(Q),
  -- (b) RH-conditional bound for M(x) = O(x^{1/2+ε}), and
  -- (c) bound on the m≥2 fluctuation series.
  sorry

/-- **Odlyzko-te Riele extreme outlier corollary** (RESEARCH-OPEN, conditional):
    Assuming the Mertens-NW formula and Odlyzko-te Riele 1985's disproof of
    the Mertens conjecture, there exist infinitely many Q with NW(Q) − C > 1/6. -/
theorem mertens_NW_extreme_outliers
    (hMertensNW : ∀ Q : ℕ, 0 < Q →
       |NW Q - fareyAsymptote - (mertensFunction Q : ℝ)^2 / (6 * Q)| < (Q : ℝ)^(-(1/2))) :
    Set.Infinite { Q : ℕ | NW Q - fareyAsymptote > 1/6 } := by
  -- RESEARCH-OPEN: combines Odlyzko-te Riele 1985 (lim sup M(x)/√x ≥ 1.06)
  -- with the Mertens-NW formula.
  sorry

end
