/-
Copyright 2026 The Formal Conjectures Authors.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-/

import FormalConjectures.Util.ProblemImports

/-!
# A density-one sign pattern for the prime-step Farey L² discrepancy

*Reference:* S. Shai, *The per-step Farey discrepancy* (2026); project
record `Primes-Equispaced` (`handoff-2026-05-09-followup`,
`handoff-2026-05-16-D3-functionfield`). arXiv: to be assigned.

## Statement

Let `fareySet N` be the Farey fractions of order `N` in `(0, 1]`, and let
`W N := ∫₀¹ (#{f ∈ fareySet N : f ≤ x} − |fareySet N|·x)² dx` be the `L²`
(Weyl) discrepancy. For a prime `p` the **prime-step increment** is
`ΔW p := W (p-1) − W p` — the change when the `p−1` new fractions `{k/p}`
are inserted. Let `mertens` be `M n = ∑_{k ≤ n} μ(k)`.

The naive **pointwise** relation `sgn (ΔW p) = sgn (−M p)` for *every*
prime `p` with `M p ≤ −3` is **false** (explicit counterexamples, e.g.
`p = 237733`, `M p = −20`; `p = 243799`, `M p = −3`; project record). The
surviving statement — numerically ≈ 73 % of qualifying primes at
`X = 10⁷`, expected to be density-one under the `L`-function hypotheses
controlling the explicit-formula expansion of `ΔW p` (a Chebyshev-bias
statement à la Rubinstein–Sarnak) — is the **density-one** form below.
It is an open problem; the body is `sorry`.

NOTE TO REVIEWERS / MAINTAINERS: this statement uses a *concrete* Farey
discrepancy (no opaque symbols). It is a faithful statement, but it has
**not yet been `lake build`-verified inside the formal-conjectures repo**
(authored outside it); a build check + any import/namespace adjustment is
expected as part of review. Supporting definitions can be moved to
`FormalConjecturesForMathlib` on request.
-/

namespace FareyDiscrepancySign

open scoped BigOperators Classical
open Finset MeasureTheory

/-- The Farey fractions of order `N`: reduced `p/q ∈ (0,1]` with
`1 ≤ q ≤ N`, `1 ≤ p ≤ q`, `Nat.Coprime p q`, as a `Finset ℚ`. -/
noncomputable def fareySet (N : ℕ) : Finset ℚ :=
  (Finset.Icc 1 N).biUnion fun q =>
    ((Finset.Icc 1 q).filter fun p => Nat.Coprime p q).image
      fun p => (p : ℚ) / (q : ℚ)

/-- Counting function `#{ f ∈ fareySet N : (f : ℝ) ≤ x }`. -/
noncomputable def fareyCount (N : ℕ) (x : ℝ) : ℕ :=
  ((fareySet N).filter fun f => (f : ℝ) ≤ x).card

/-- The signed Farey discrepancy `D_N(x) = #{f ≤ x} − |F_N|·x`. -/
noncomputable def fareyDiscrepancy (N : ℕ) (x : ℝ) : ℝ :=
  (fareyCount N x : ℝ) - ((fareySet N).card : ℝ) * x

/-- The `L²` (Weyl) second moment `W N = ∫₀¹ D_N(x)² dx`. -/
noncomputable def W (N : ℕ) : ℝ :=
  ∫ x in (0:ℝ)..1, (fareyDiscrepancy N x) ^ 2

/-- The prime-step increment `ΔW p = W (p-1) − W p`. -/
noncomputable def ΔW (p : ℕ) : ℝ := W (p - 1) - W p

/-- The Mertens function `M n = ∑_{k ≤ n} μ(k)`. -/
noncomputable def mertens (n : ℕ) : ℤ :=
  ∑ k ∈ Finset.range (n + 1), ArithmeticFunction.moebius k

/-- Real sign, `sgn 0 = 0`. -/
noncomputable def signR (x : ℝ) : ℤ :=
  if x > 0 then 1 else if x < 0 then -1 else 0

/-- Integer sign, `sgn 0 = 0`. -/
def signZ (n : ℤ) : ℤ := if n > 0 then 1 else if n < 0 then -1 else 0

/-- At prime `p`: `sgn (ΔW p) = sgn (−M p)`. -/
noncomputable def Agrees (p : ℕ) : Prop := signR (ΔW p) = signZ (- mertens p)

/-- **Density-one Farey discrepancy sign pattern (open).**

For every `ε > 0` there is `X₀` such that for all `X ≥ X₀`, whenever at
least one prime `p ≤ X` has `M p ≤ −3`, the proportion of such primes that
also satisfy `sgn (ΔW p) = sgn (−M p)` is `≥ 1 − ε`. The pointwise form
(`ε = 0`) is false; this density-one form is the surviving conjecture. -/
@[category research open, AMS 11]
theorem farey_discrepancy_density_one_sign :
    ∀ ε > (0 : ℝ), ∃ X₀ : ℕ, ∀ X ≥ X₀,
      let qualifying : ℝ :=
        (((Finset.range (X + 1)).filter
          (fun p => Nat.Prime p ∧ mertens p ≤ -3)).card : ℝ)
      let agreeing : ℝ :=
        (((Finset.range (X + 1)).filter
          (fun p => Nat.Prime p ∧ mertens p ≤ -3 ∧ Agrees p)).card : ℝ)
      0 < qualifying → 1 - ε ≤ agreeing / qualifying := by
  sorry

end FareyDiscrepancySign
