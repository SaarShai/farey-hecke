# A zero-temperature / escape-of-mass demonstration on the Hecke BCZ map

*Internal write-up, 2026-06-03. Numerical demonstration of a proven theorem; not a new proof.
Part of the author's Hecke ergodic-optimization paper. Nothing herein sent outward.*

## Setup

For an integer `q ≥ 3` let `λ = 2cos(π/q)` and let `BCZ_q` be the genuine Taha Boca–Cobeli–Zaharescu
map on the `G_q`-Farey triangle `𝒯^q = {0 < a ≤ 1, 1 − λa < b ≤ 1}`. It is piecewise-`SL₂(ℝ)`,
preserves the flat (Lebesgue) measure, and has `q−2` branches `M_{i,k}`. The "gap" observable is
`P(a,b) = a·((a,b)·w_i)/y_i` on branch `i` (for `q=3` this is the classical `ab`). The map has a single
parabolic cusp; the **cusp vertex** is `(1/λ, 0)` and the **cusp word** is the parabolic
`M_{q−2,0} = [[1, λ],[0, 1]]`.

The author's theorem (machine-checked in Lean,
`lean/BCZHeckeGenuine_allq_VERIFIED.lean`) is

> **`X_Ω(q) := inf_μ ess-sup_{supp μ} P = 1/λ³` for all `q ≥ 5`** (with `X_Ω(3)=2/9`, `X_Ω(4)=√2/8`),
> and the infimum is **not attained** — there is **no ground state**.

This note demonstrates that theorem as an explicit, computable instance for thermodynamic formalism
(Ruelle–Bowen Gibbs limits; the Riquelme–Velozo escape-of-mass dichotomy, AHP 23 (2022); Leplaideur
ground states), and isolates a clean distinction between two zero-temperature limits.

## Two zero-temperature limits

There are two ergodic-optimization objectives over invariant probability measures `μ`:

- **min-MAX (`L∞`):** `inf_μ ess-sup_μ P`. This is `X_Ω(q) = 1/λ³`.
- **min-AVG (Birkhoff, `L¹`):** `inf_μ ∫P dμ =: β_min`. This is the value selected by the *standard*
  Gibbs / zero-temperature limit `μ_β ∝ e^{−βP}`, `β→∞`.

They are different. At `q = 5`, `β_min = 0.18634` (the period-3 word `[(4,1),(4,1),(4,2)]`, an interior
orbit) while `1/λ³ = 0.23607`. Crucially their *behaviour* differs:

| objective | value (`q=5`) | optimizer | ground state |
|---|---|---|---|
| min-MAX (ess-sup) | `1/λ³ = 0.23607` | cusp word, `s ↓ s_lo` | **none — escapes to cusp** |
| min-AVG (Birkhoff) | `β_min = 0.18634` | interior period-3 orbit | **exists (compact)** |

The **escape / no-ground-state is specific to the `L∞` objective.** `P` is not bounded below by `1/λ³`
pointwise (it drops to `≈10⁻³` in transient domain corners); `1/λ³` is the floor of the *essential
supremum over invariant measures*, attained only in the cusp limit. The standard Gibbs measure, which
optimizes the *average*, instead concentrates on an interior periodic orbit — a genuine ground state.

## The escape, made explicit

On the invariant cusp segment `{b = 0, 1/λ < a ≤ 1}` the cusp branch acts as the identity (fixed
points) and `P = a²/λ`, which decreases to `1/λ³` as `a → 1/λ⁺` but never reaches it: the vertex
`a = 1/λ` is excluded (`1 − λa = 0` violates `1 − λa < b = 0`). Hence the minimizing sequence
`μ_n = δ_{a_n}`, `a_n → 1/λ⁺`, has `ess-sup P → 1/λ³` from above while escaping to the boundary vertex.

The same picture holds off `b = 0` along the genuine periodic-orbit family of the cusp word: writing the
trace-2 family as `s·v_n`, the value `V(s) = s²·max_n P̂_n → 1/λ³` (exactly, to 40 digits, for every `q`)
as `s ↓ s_lo`, and the orbit base point converges to `(1/λ, 0)`. For `q = 3, 4` the cusp word is *not*
optimal — an interior orbit gives `2/9`, `√2/8` — so a ground state exists there; the escape switches on
exactly at `q ≥ 5`. *(Figure: `Ogoal_two_values.png`.)*

The mechanism is parabolic. Seeding an orbit at distance `δ` from the cusp vertex, the number of steps
it spends in a fixed cusp neighbourhood before expulsion grows like `1/δ` (`q=5`: `148, 494, 1483` for
`δ = 10⁻³, 10⁻³·⅓, 10⁻⁴`). This marginal `1/δ` divergence — neither bounded (which would give a ground
state) nor exponential — is precisely why no invariant probability measure attains the floor.
*(Figure: `Ogoal_escape_vs_noescape.png`.)*

## Transfer operator and freezing

A mass-conserving Ulam discretization of the weighted transfer operator
`L_β f(x) = Σ_{T y = x} e^{−βP(y)} f(y)` on a `140×140` grid reproduces, at `β = 0`, leading eigenvalue
`ρ = 1` and the flat invariant density (validation). The free energy `f(β) = −log ρ(β)/β` decreases
monotonically and, for `q = 5`, passes below `1/λ³ = 0.236` toward `β_min ≈ 0.19` — the freezing
(zero-temperature) transition with vanishing entropy. *(Figure: `Ogoal_freezing.png`.)* We deliberately
do **not** read the fine *location* of `μ_β` off the grid: beyond `β ≈ 64` the weighted spectrum
collapses and the eigensolver returns spurious boundary modes (a `q`-dependent artifact). The interior
ground state of the average problem is established instead by the exact word search above.

## A closed-form escape rate

The cusp-corridor margin `2 − λ = 4sin²(π/2q)` satisfies `(2 − λ)·q² → π² = 9.8696`, and the value's
approach to its `q→∞` asymptote `1/8` satisfies `(1/λ³ − 1/8)·q² → (3/16)π² = 1.8506`. Both give an
`O(1/q²)` freezing/escape scale in closed form. *(Figure: `Ogoal_escape_rate.png`.)*

## Status and framing

This is a *demonstration* of a proven theorem, not a new proof. Its value is as an explicit, computable
(and, for the underlying value, machine-checked) example for a field that is otherwise dominated by
abstract dichotomies: a Hecke BCZ map with a **closed-form ground energy `1/λ³`**, an **`O(1/q²)` escape
rate**, and a clean separation between an `L∞` objective that has no ground state (escape of mass) and an
`L¹` objective that does. The novelty is one of realization; the relevant literature is Riquelme–Velozo
(escape of mass as the sole obstruction) and Leplaideur (ground states / freezing), with the standing
footnote that the Gauss-map value `2/9` coincides at `q = 3` (JMU 2007). No physical or application claims
are made; the content is mathematical (ergodic optimization / thermodynamic formalism / homogeneous
dynamics).
