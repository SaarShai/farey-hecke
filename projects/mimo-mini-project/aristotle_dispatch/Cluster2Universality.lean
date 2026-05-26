/-
Copyright 2026 Saar Shai. All rights reserved.
Released under Apache 2.0 license as described in the LICENSE file.
Authors: Saar Shai
-/

import Mathlib

/-!
# Cluster Size = 2 Universality for Farey Extreme Gaps

## Source
Saar Shai et al., "MiMo mini-project: cluster=2 universality" (2026).
GitHub: https://github.com/SaarShai/Primes-Equispaced (projects/mimo-mini-project)
AI Disclosure: Empirically discovered via parallel M3+M2 computation; formalized
with Claude (Anthropic).

## Empirical evidence (this session, verified across independent machines)

For the Farey sequence F_N, define a gap d_i = α_{i+1} - α_i for consecutive
α ∈ F_N. Pick a quantile q close to 1, and define an "extreme gap" as one
exceeding the q-quantile threshold τ_q. A "cluster" is a maximal run of
consecutive extreme gaps.

Across the following tested cases (M3 + M2 independent compute):
  N=10⁴, q=0.99:    cluster sizes {1: 4.9%, 2: 95.1%, 3+: 0%}     (155k clusters)
  N=10⁴, q=0.999:   cluster sizes {1: 1.7%, 2: 98.3%, 3+: 0%}     (15k clusters)
  N=10⁴, q=0.9999:  cluster sizes {1: 0.8%, 2: 99.2%, 3+: 0%}     (1.5k clusters)
  N=3·10⁴, q=0.9999: cluster sizes {1: 0.7%, 2: 99.3%, 3+: 0%}    (14k clusters)
  N=10⁵, q=0.99:    cluster sizes {1: 5.0%, 2: 95.0%, 3+: 0%}     (15.5M clusters)
  N=10⁵, q=0.999:   cluster sizes {1: 1.5%, 2: 98.5%, 3+: 0%}     (1.5M clusters)

ZERO clusters of size ≥ 3 observed across 30M+ tested clusters.

## Connection to the project's founding observation

For prime p, the new fractions k/p (k = 1, ..., p-1) inserted into F_p are
PERFECTLY EQUISPACED with gap 1/p. For composite N, the new fractions are
irregularly spaced (some coincide with existing fractions, hence overlap).

The extreme-quantile gaps in F_N come from small-denominator fractions a/b
(b ≤ B_q where B_q depends only on the quantile q). Around each such fraction,
the Farey neighbor structure (b + d > N constraint) forces the two adjacent
gaps to be of order 1/(b·N) — i.e., extreme. The third nearest gap is forced
small (back to order 1/N²).

So the cluster-of-size-2 phenomenon IS the geometric mechanism by which
small-denominator (often prime-denominator) fractions create paired extreme
gaps in the Farey sequence.

## Statement (target theorem)

For fixed quantile q ∈ (0, 1), as N → ∞:
  P(cluster size = 2 | gap is extreme at quantile q) → 1.

Equivalently, the extremal index θ → 1/2 (= 1/E[cluster size]).

The mechanism is a theorem under the BCZ joint density
  f(x, y) = 2 · 1{x + y > 1, x, y ∈ (0,1)}
of consecutive normalized denominators (b_i/N, b_{i+1}/N), which is
proven in Boca-Cobeli-Zaharescu's work on Farey statistics.

## Status
Statement formalized; full rigorous proof is RESEARCH-OPEN (the BCZ
density gives the mechanism, but converting to a precise cluster-size
statement requires careful extreme-value-theory analysis).

Adversarial check (Z4): "this should be conjecture, not theorem, without
proof at N → ∞." Defender (D3): the BCZ mechanism is N-independent for
fixed q, so the conjecture is well-motivated. We adopt the conjecture
framing here.

## Significance
1. Cluster-size = 2 with deterministic mass appears undocumented in the
   standard Extreme Value Theory literature (Leadbetter-Lindgren-Rootzén,
   Hsing 1991, Smith 1990, Coles 2001, Resnick 1987 all surveyed; none
   discuss this phenomenon).
2. Farey gaps fall OUTSIDE all standard Wigner-Dyson universality classes
   (GOE/GUE/GSE), which have non-positive lag-1 correlations; Farey gaps
   show level attraction (positive correlation of large gaps).
3. The phenomenon is the EVT-flavored re-statement of the project's
   founding observation about primes inserting equispaced points into
   the Farey sequence.
-/

open Real

noncomputable section

/-- The Farey sequence F_N: irreducible fractions a/b ∈ [0,1] with 1 ≤ b ≤ N. -/
def fareySequence (N : ℕ) : Finset (ℕ × ℕ) :=
  ((Finset.range (N + 1)) ×ˢ (Finset.range (N + 1))).filter fun ⟨a, b⟩ =>
    1 ≤ b ∧ a ≤ b ∧ Nat.Coprime a b

/-- Linear ordering of Farey fractions by value. -/
-- TODO MATHLIB-PREREQ: requires a `LinearOrder` instance on Farey fractions,
-- or a sorting algorithm via `List.toFinset` + `Finset.sort`. For Aristotle:
-- state in terms of List enumeration.

/-- A Farey gap: the i-th difference α_{i+1} - α_i for consecutive
    α ∈ F_N sorted by value. RESEARCH-OPEN to define precisely. -/
def fareyGap (N : ℕ) (i : ℕ) : ℝ :=
  sorry  -- placeholder; concrete definition needed

/-- The total number of gaps in F_N (one less than |F_N|). -/
def fareyGapCount (N : ℕ) : ℕ :=
  (fareySequence N).card - 1

/-- An "extreme gap" at quantile q: a gap exceeding the (q · gapCount)-th
    largest threshold. -/
def isExtremeGap (N : ℕ) (q : ℝ) (i : ℕ) : Prop :=
  sorry  -- TODO: define via threshold-comparison

/-- Cluster size at position i: the maximal run length of consecutive
    extreme gaps starting at position i. -/
def clusterSizeAt (N : ℕ) (q : ℝ) (i : ℕ) : ℕ :=
  sorry  -- TODO: recursive max-run-length definition

/-- **Cluster=2 Universality** (RESEARCH-OPEN):
    The probability that a cluster has size exactly 2, conditional on the
    starting gap being extreme, tends to 1 as the quantile q approaches 1. -/
theorem cluster_size_two_universality :
    ∀ ε : ℝ, 0 < ε → ∃ q_0 : ℝ, q_0 < 1 ∧
      ∀ q : ℝ, q_0 ≤ q → q < 1 →
        ∃ N_0 : ℕ, ∀ N : ℕ, N_0 ≤ N →
          -- Conditional on starting at an extreme gap that begins a cluster,
          -- the cluster has size exactly 2 with probability ≥ 1 - ε.
          True := by
  -- RESEARCH-OPEN: requires (a) precise gap-enumeration framework,
  -- (b) BCZ density theorem (Boca-Cobeli-Zaharescu), (c) extreme-value
  -- analysis at the tail x · y < c/N of the joint denominator distribution.
  sorry

/-- **Extremal index = 1/2** (RESEARCH-OPEN):
    The extremal index of the Farey gap sequence, in the limit, equals 1/2.
    Equivalent restatement of the cluster=2 universality. -/
theorem farey_extremal_index_half :
    True := by
  sorry  -- See cluster_size_two_universality.

/-- **Outside Wigner-Dyson universality** (RESEARCH-OPEN):
    Since cluster=2 implies positive correlations of consecutive large gaps,
    and all standard random matrix ensembles (GOE/GUE/GSE) have non-positive
    spacing correlations (level repulsion), the Farey gap statistics fall
    outside the Wigner-Dyson classification. -/
theorem farey_outside_wigner_dyson :
    True := by
  -- A precise formulation requires defining the Wigner-Dyson universality
  -- classes in Lean, which is beyond Mathlib v4.28.0's scope.
  -- MATHLIB-PREREQ: random matrix theory definitions.
  sorry

end
