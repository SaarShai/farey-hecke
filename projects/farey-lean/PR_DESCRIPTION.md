# DRAFT Mathlib PR — `feat(NumberTheory): Farey sequences and the Stern–Brocot mediant`

> **STATUS: STAGED, NOT SUBMITTED.** This is a draft for the user to review and submit. Before
> submitting: (1) fill in the author name in the copyright header (`AUTHOR_PLACEHOLDER`); (2) re-check
> current Mathlib master + a Zulip `#Is-there-code-for-X?` for an in-flight Farey sequence; (3) rebase
> onto current master and `lake exe cache get` (developed against v4.28.0); (4) the imports are already
> specific and granular (no `import Mathlib`, no `import Mathlib.Tactic`) — optionally run
> `lake exe shake` + `lake exe lint-style` against current master as a final tighten.

## Title
`feat(NumberTheory): Farey sequences, mediants, and the neighbour theorem`

## What this adds
A new file `Mathlib/NumberTheory/Farey/Basic.lean` formalizing the **Farey sequence as an object**
and the elementary **mediant / Stern–Brocot** theory underneath it. Highlights:

- `Farey.farey n : Finset ℚ` — the Farey sequence `F n` (reduced rationals in `[0,1]` with
  denominator `≤ n`), with the faithful membership characterization `Farey.mem_farey`.
- `Farey.card_farey` — **the length of the Farey sequence**: `|F n| = 1 + ∑_{k=1}^n φ(k)`
  (Euler totient). Sanity-checked `|F₁|=2, |F₂|=3, |F₃|=5`.
- `Farey.neighbour_unimodular` — **the Farey neighbour theorem** (Hardy–Wright, Thm 28):
  consecutive Farey fractions `a/b < c/d` satisfy `b*c − a*d = 1`. Restated on the actual `F n`
  object as `Farey.unimodular_of_consecutive`.
- The mediant / unimodular-neighbour core: `det`, `Unimodular`, mediant preserves the determinant
  and lands in lowest terms (`Unimodular.isCoprime_mediant`); the denominator bound
  `Unimodular.den_ge_of_strictBetween` (the mediant is the unique simplest fraction strictly
  between two neighbours); the Stern–Brocot chain step `isFareyChain_insert_mediant`; and the gap
  formula `Unimodular.rat_sub` : `c/d − a/b = 1/(b*d)`.

## Why
The Farey sequence is a standard classical object (Hardy–Wright, Ch. III) that is **currently
absent from Mathlib**. Mathlib has the continued-fraction convergent determinant identity
(`Mathlib/Algebra/ContinuedFractions/…/Determinant.lean`) and Legendre's theorem
(`Mathlib/NumberTheory/DiophantineApproximation/…`), but those concern the convergents of a *single*
real number — a different object from the Farey sequence `F n` of all reduced fractions of bounded
denominator. This PR fills that gap and provides reusable infrastructure for continued fractions,
Diophantine approximation, equidistribution, and the "formalize famous theorems" effort.

## Scope / honesty
These are formalizations of **classical, known** results. The value is as machine-checked Mathlib
infrastructure and named theorems, **not** new mathematics. Nothing here bears on open problems.

## Verification (against Mathlib `v4.28.0`)
- Compiles with **real Lean exit 0** and **zero warnings**.
- `#print axioms` for every main result (`card_farey`, `mem_farey`, `neighbour_unimodular`,
  `unimodular_of_consecutive`, `Unimodular.den_ge_of_strictBetween`, `isFareyChain_insert_mediant`,
  `Unimodular.rat_sub`) reports only `[propext, Classical.choice, Quot.sound]` — sorry-free.
- **Duplication check:** the local Mathlib checkout (commit `8f9d9cf`, 2026-02-16) has **0** matches
  for `farey`, `mediant`, or `stern-brocot`. Re-run this against current master before submitting.
- **Minimal, fully granular imports** (verified — no `import Mathlib`, and no `import Mathlib.Tactic`
  catch-all; only the two tactic modules actually used, `Linarith` and `LinearCombination`, with
  `ring`/`norm_num` reached transitively):
  ```
  import Mathlib.Data.Nat.Totient
  import Mathlib.Data.Rat.Lemmas
  import Mathlib.Algebra.Ring.Rat
  import Mathlib.Algebra.Order.Ring.Unbundled.Rat
  import Mathlib.Algebra.Order.GroupWithZero.Unbundled.Basic
  import Mathlib.Algebra.Order.Field.Basic
  import Mathlib.Algebra.BigOperators.Group.Finset.Basic
  import Mathlib.Data.Finset.Card
  import Mathlib.Order.Interval.Finset.Basic
  import Mathlib.RingTheory.Coprime.Lemmas
  import Mathlib.Data.List.Chain
  import Mathlib.Tactic.Linarith
  import Mathlib.Tactic.LinearCombination
  ```
- All source lines are ≤ 100 Unicode codepoints (max = 100), within the Mathlib `lint-style` limit.

## Notes for review
- `farey 0 = {1}` is a degenerate boundary case (the intended object is `n ≥ 1`); `card_farey`
  holds for all `n`, while `mem_farey` is stated for `n ≥ 1`.
- Proof of `card_farey`: partition `F n` into the endpoint `1` plus, for each denominator
  `1 ≤ q ≤ n`, the level `{a/q : 0 ≤ a < q, gcd(a,q)=1}` of size `Nat.totient q`
  (disjoint by denominator) — `Finset.card_biUnion` + `card_insert_of_notMem`.
- References cited: Hardy & Wright — neighbour identity = **Theorem 28** (Ch. III §3.1), mediant =
  Theorem 29; the exact length `|F n| = Φ(n) + 1` is the §18.5 (p. 268) remark preceding the
  asymptotic **Theorem 331** (NOT Theorem 330, which is the asymptotic `Φ(n) ∼ 3n²/π²`); see also
  OEIS A005728. Graham–Knuth–Patashnik, *Concrete Mathematics* 2nd ed. §4.5 (Stern–Brocot, mediant).

## Follow-up (not in this PR)
Franel–Landau (Farey discrepancy ⇔ RH, an equivalence) and the three-gap/Steinhaus theorem are
natural next targets but are out of scope here.
