/-
Copyright 2026 Saar Shai. All rights reserved.
Released under Apache 2.0 license as described in the LICENSE file.
Authors: Saar Shai
-/

import Mathlib

/-!
# Mikolás Double-Sum Identity for J(Q)

## Source
Saar Shai, "MiMo mini-project: structural identity for Farey L²-discrepancy" (2026).

## Background

For the Farey sequence F_Q (denominators ≤ Q), let

  J(Q) := ∫₀¹ (count_Q(x) − Φ(Q)·x)² dx

be the L²-discrepancy. The Mikolás identity (Acta Sci. Math. Szeged 13
(1949), 93–117; Kanemitsu-Yoshimoto, Acta Arith. 75 (1996), 351–374) states

  J(Q) = (1/(2π²)) · Σ_{m=1}^∞ |S_Q(m)|² / m²

where S_Q(m) = Σ_{q=1}^Q c_q(m), and c_q(m) is the Ramanujan sum:

  c_q(m) = Σ_{d | gcd(m, q)} d · μ(q/d)

## Identity derived in this session

The Ramanujan sum partial-sum simplifies: by swapping the d, q order,

  S_Q(m) = Σ_{d | m} d · M(⌊Q/d⌋)

where M is the Mertens function M(n) = Σ_{k≤n} μ(k).

Then using ζ(2) = π²/6 and Σ_{m: L|m} 1/m² = ζ(2)/L² (with L = lcm(d,d')):

  J(Q) = (1/12) · Σ_{d=1}^Q Σ_{d'=1}^Q gcd(d,d')² · M(⌊Q/d⌋) · M(⌊Q/d'⌋) / (d · d')

(modulo a small constant factor we have not fully resolved — empirically
my formula overestimates J by a few percent at small Q; either a 2π² vs
4π² Parseval factor or a boundary term).

## Theorems to prove

The identities below are PURE ALGEBRAIC consequences of definitions, modulo
the underlying Mikolás identity which we take as RESEARCH-OPEN.
-/

open Real BigOperators

noncomputable section

/-- The Mertens function M(n) = Σ_{k=1}^n μ(k). -/
def mertens (n : ℕ) : ℤ := ∑ k ∈ Finset.range (n+1), ArithmeticFunction.moebius k

/-- The Ramanujan-sum partial sum S_Q(m) = Σ_{d | m} d · M(⌊Q/d⌋).
    Equivalent to Σ_{q=1}^Q c_q(m). -/
def S_Q (Q m : ℕ) : ℤ :=
  ∑ d ∈ (Nat.divisors m), (d : ℤ) * mertens (Q / d)

/-- m=1 case: S_Q(1) = M(Q), since the only divisor of 1 is itself,
    so the sum is just 1 · M(⌊Q/1⌋) = M(Q). -/
theorem S_Q_one (Q : ℕ) : S_Q Q 1 = mertens Q := by
  unfold S_Q
  simp [Nat.divisors_one]

/-
m=2 case: S_Q(2) = M(Q) + 2 M(⌊Q/2⌋).
-/
theorem S_Q_two (Q : ℕ) : S_Q Q 2 = mertens Q + 2 * mertens (Q / 2) := by
  unfold S_Q
  -- divisors of 2 are {1, 2}
  -- Since 2 is prime, its divisors are 1 and 2. Therefore, the sum over the divisors of 2 is just the sum of the terms for d=1 and d=2. We can use the fact that the divisors of 2 are {1, 2}.
  simp [Nat.Prime.divisors (by norm_num : Nat.Prime 2)]

/-
RESEARCH-OPEN: standard manipulation of Finset.divisors

m=p prime case: S_Q(p) = M(Q) + p · M(⌊Q/p⌋).
-/
theorem S_Q_prime (Q p : ℕ) (hp : Nat.Prime p) :
    S_Q Q p = mertens Q + (p : ℤ) * mertens (Q / p) := by
  unfold S_Q
  -- divisors of a prime p are {1, p}
  rw [ hp.sum_divisors ];
  grind +extAll

-- RESEARCH-OPEN

/-- A normalized form of the L²-discrepancy J(Q), placeholder definition.
    Should be ∫₀¹ (count_Q(x) − Φ(Q)·x)² dx, but that requires Farey-set
    machinery not yet in this dispatch. -/
def J_Q (_Q : ℕ) : ℝ := 0  -- placeholder; would be MeasureTheory integral

/-- **Mikolás Fourier-side identity** (target theorem, RESEARCH-OPEN):
    J(Q) = (1/(2π²)) · Σ_{m=1}^∞ |S_Q(m)|² / m². -/
theorem mikolas_fourier_identity (Q : ℕ) (hQ : 0 < Q) :
    J_Q Q = (1 / (2 * Real.pi^2)) *
            ∑' m, ((S_Q Q m : ℝ)^2 / (m^2 : ℝ)) := by
  sorry  -- RESEARCH-OPEN: requires Parseval + Farey enumeration setup

/-- **Double-sum identity** (target theorem, RESEARCH-OPEN):
    Σ_{m=1}^∞ |S_Q(m)|² / m² =
      (π²/6) · Σ_{d,d'} gcd(d,d')² · M(Q/d) · M(Q/d') / (d · d')

    Proof outline: use Σ_{m: L|m} 1/m² = ζ(2)/L², swap sum order,
    and L = lcm(d,d') with d·d'/L² = gcd(d,d')²/(d·d'). -/
theorem mikolas_double_sum_identity (Q : ℕ) (hQ : 0 < Q) :
    ∑' m : ℕ+, ((S_Q Q m : ℝ)^2 / (m.val^2 : ℝ)) =
    (Real.pi^2 / 6) *
    ∑ d ∈ Finset.range (Q+1), ∑ d' ∈ Finset.range (Q+1),
        ((Nat.gcd d d')^2 : ℝ) * (mertens (Q/d) : ℝ) * (mertens (Q/d') : ℝ) /
        ((d : ℝ) * (d' : ℝ)) := by
  sorry  -- RESEARCH-OPEN: requires zeta-2 manipulation and Σ over lcm-multiples

end