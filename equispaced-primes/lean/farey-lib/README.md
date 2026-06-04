# Farey sequences, Stern–Brocot, and the three-gap theorem in Lean 4

Formalizations of **Farey sequences**, the **Stern–Brocot mediant structure**, and the
**three-gap (Steinhaus / three-distance) theorem**, built on
[Mathlib](https://github.com/leanprover-community/mathlib4). These objects are currently **absent
from Mathlib**; this library is intended for upstreaming (or use as a standalone dependency).

All results below are **`sorry`-free** and check against **Mathlib `v4.28.0` / Lean `v4.28.0`**
(`#print axioms` shows only `propext`, `Classical.choice`, `Quot.sound`).

## Contents

### `Farey/Mediant.lean` — mediant & unimodular-neighbour foundations
The algebraic core of Farey/Stern–Brocot. For fractions `a/b`, `c/d`:
- `det a b c d = b*c - a*d`; `Unimodular a b c d := det = 1` (the neighbour relation).
- `det_mediant_left/right` — inserting the mediant `(a+c)/(b+d)` preserves the determinant.
- `Unimodular.mediant_left/right` — the mediant is a unimodular neighbour of each parent.
- `Unimodular.isCoprime_mediant` — **the mediant of a unimodular pair is in lowest terms**
  (why Stern–Brocot stays reduced).
- `Unimodular.den_ge_of_strictBetween` — **between unimodular neighbours every fraction has
  denominator `≥ b+d`**; with the mediant achieving `b+d`, the mediant is the unique *simplest*
  fraction strictly between.
- `Unimodular.not_strictBetween_of_den_le` — adjacency (sufficient direction): unimodular and
  `b+d > n` ⟹ no fraction of denominator `≤ n` lies strictly between.
- `isFareyChain_insert_mediant` — **mediant insertion preserves the Farey-chain property** (the
  Stern–Brocot inductive step: consecutive entries stay unimodular).
- `Unimodular.rat_sub` — **the Farey gap formula** `c/d - a/b = 1/(b*d)` in `ℚ`.

### `Farey/Neighbour.lean` — the Farey neighbour theorem
- `neighbour_unimodular` — **the Farey neighbour theorem (Hardy–Wright, Thm 28):** if `a/b < c/d`
  are reduced with denominators in `[1,n]` and no fraction `x/y` with `0 < y ≤ n` lies strictly
  between them (i.e. they are consecutive in `F_n`), then `b*c - a*d = 1`. Proof: a Bézout
  solution of `b*x - a*y = 1` with denominator in `(n-b, n]`, the determinant identity
  `(b*c-a*d)·(y,x) = (d,c) - (d*x-c*y)·(b,a)`, and a two-case split.

**Together** these give the full adjacency characterization: for reduced `a/b < c/d` in `F_n`,
*consecutive `⟺` `b*c - a*d = 1` and `b+d > n`* (`⟸` is `not_strictBetween_of_den_le`; `⟹` is
`neighbour_unimodular` plus the mediant lying strictly between).

### `Farey/ThreeGap.lean` — the three-gap (Steinhaus / three-distance) theorem
- `three_gap` — **the three-gap theorem:** for irrational `α` and every `N`, the `N` points
  `{0·α}, {1·α}, …, {(N−1)·α}` on the circle `ℝ ⧸ ℤ` cut it into arcs taking **at most three**
  distinct lengths:
  ```lean
  theorem three_gap {α : ℝ} (hα : Irrational α) (N : ℕ) :
      ((Finset.univ : Finset (Fin N)).image (gap hα)).card ≤ 3
  ```
  Here `x α k = Int.fract (k·α)` is the orbit point `{kα} ∈ [0,1)`, `e` is the sorted enumeration
  of the `N` points via `Finset.orderEmbOfFin`, and `gap hα i` is the arc from the `i`-th sorted
  point to its cyclic successor (a dependent `if` handles the wraparound arc, correct for all `N`).

  **Proof (Liang's rigid-gap / dynamical argument, *Discrete Math.* 28 (1979) 325–326).** The whole
  theorem reduces to a *jump trichotomy*: every arc length equals `{(b−a)·α}` for the orbit-index
  jump `b−a` of the two points it spans (`fract_x_sub`), and that jump always lies in
  `{p, −q, p−q}`, where `p`, `q` are the two closest one-sided return times
  (`exists_return_right/left`). The trichotomy (`isGap_trichotomy`) is a strong induction on the
  left endpoint, organised around the shift `T y = {y+α}` acting on the *oriented forward distance*
  `fwdDist a c = {(c−a)·α}`:
  - base cases R1 / R2 — the gaps flanking `x_0` jump by `p` / `−q` (`isGap_zero`, `isGap_to_zero`);
  - descent — a gap whose forward arc misses the next point `x_N` pulls back to a strictly earlier
    gap of equal jump (`descent_step`);
  - R3 — otherwise `x_N` is swallowed and the gap splits at the last point `x_{N−1}` into a `+p`
    part and a `−q` part (`isGap_split`); the `−q` part is the clean one-sided argmin `isGap_last`,
    and the `+p` part (`isGap_pred_last`) follows by reflecting the orbit `k ↦ N−1−k`
    (`reflection_lemma`, via the succ⇒pred equivalence `succ_to_pred`) back onto R1.

  Distinctness of the `N` points uses only `Irrational α` (`x_injective`); the small cases `N ≤ 3`
  are the trivial "`≤ N ≤ 3`" bound.

## Building / checking

The proofs are checked with Mathlib `v4.28.0`. Each file is self-contained (`import Mathlib`) and
was verified with (run inside a Lean project with Mathlib `v4.28.0`; `lake exe cache get` first):

```
lake env lean Farey/Mediant.lean
lake env lean Farey/Neighbour.lean
lake env lean Farey/ThreeGap.lean
```

For **upstreaming to Mathlib**, the files slot into the number-theory / combinatorics tree (e.g.
`Mathlib/NumberTheory/Farey/`; the three-gap theorem near `Mathlib/Dynamics/` or
`Mathlib/NumberTheory/Diophantine/`); no separate build config is then needed. For a **standalone
repo**, add a `lakefile` requiring Mathlib at the matching revision and `lake exe cache get` before
building. (`lean-toolchain` pins the toolchain.)

## Prior art & scope — stated honestly

These are formalizations of **classical, known** results (Hardy & Wright; the Stern–Brocot tree;
the three-gap theorem of Sós, Surányi, and Świerczkowski, 1957–59). Their value is **as reusable
Mathlib infrastructure and machine-checked named theorems**, *not* as new mathematics. They are
useful to the Mathlib project (missing classical topics) and to formalizers working on continued
fractions / Diophantine approximation / equidistribution. Nothing here bears on open problems; the
three-gap *algorithm* (used in graphics/DSP/audio) is unaffected — this is the machine-checked
*proof*, for the formal-methods community.

**Three-gap prior art (must be cited).** The three-gap theorem was previously formalized in **Coq**
by **Micaela Mayero**, *The Three Gap Theorem (Steinhaus Conjecture)*, TYPES'99, Lökeberg (Selected
Papers, LNCS 1956, 2000), p. 162; arXiv:cs/0609124, following van Ravenstein's proof. This Lean
development is — to the best of a 2026-05 public check (Mathlib master, open PRs, Lean Zulip, AFP,
the cross-prover `1000-plus` tracker) — the **first formalization in Lean / Mathlib**, but **not**
the first in any prover. Do not overclaim.

*Disambiguation for Mathlib:* the entry already called "Steinhaus theorem" in Mathlib (Wikidata
`Q3527166`) is the unrelated **difference-set** theorem (`A − A` contains a neighbourhood of 0). The
three-gap theorem is **`Q3527252`**, currently absent from Mathlib's `docs/1000.yaml`.

## PR readiness (user-driven — not yet submitted)

`Farey/ThreeGap.lean` is complete, `sorry`-free, axiom-clean, and 0-warning. Opening a Mathlib PR or
Zulip post is **user-driven**; before doing so, re-run a fresh `#Is-there-code-for-X?` duplication
check against current Mathlib *master* (it can change at any time), split the file along Mathlib's
module conventions, and adapt docstrings to Mathlib style. Author: _(to be filled in by the
maintainer)_. Intended license: **Apache 2.0** (to match Mathlib).
