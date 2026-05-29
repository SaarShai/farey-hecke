# Ergodic optimization of the Farey gap-product: ground values and the non-existence of ground states for BCZ and Hecke return maps

**Working draft — v0.1 (2026-05-29).** Internal draft; authorship/affiliations TBD.
References [1]–[6] verified against primary sources (arXiv / journal pages), 2026-05-29.
Markdown now; convert to LaTeX for submission.

---

## Abstract

The Boca–Cobeli–Zaharescu (BCZ) map is the first-return map of the horocycle flow on the
modular surface to a natural cross-section; it governs the fine-scale statistics of Farey
fractions. We study this map, and its analogues for the Hecke triangle groups `G_q`, from the
viewpoint of **ergodic optimization** (in the sense of Jenkinson, Bousch, Contreras): we
optimize the time-/measure-extreme of the observable `P(x,y) = xy`, the product of two
consecutive Farey gaps. We prove three things. (1) For every invariant probability measure `μ`,
`ess-sup_μ P ≥ t_q`, with `t_3 = 2/9` and `t_4 = √2/8`; the bound is sharp. (2) **The optimal
value `t_q` is never attained: there is no ground state** — `inf_μ ess-sup_μ P = t_q` is an
unattained infimum, approached by period-2 orbit measures whose limiting (vertex) measure fails
to be invariant. This is a natural arithmetic dynamical system that has *no* ground-state measure,
in contrast with Contreras's theorem that ground states are generically periodic. (3) Across the
Hecke family, an interior period-2 ground-state configuration exists **iff** `sec²(π/q) ∈ ℤ` and
`q < ∞`, i.e. iff `q ∈ {3, 4}`. The `q = 3` results are **formally verified in Lean 4 / Mathlib**
(sorry-free, axioms `propext, Classical.choice, Quot.sound`).

**Scope, stated up front.** The novelty is the *formulation* — ergodic optimization applied to
horocycle return maps appears to be new — together with the no-ground-state phenomenon, the
arithmetic dichotomy, and the machine-checked proofs. The underlying inequalities are elementary
piecewise-bilinear min–max facts; `t_q` is *not* a spectral quantity, and none of this bears on
the Riemann Hypothesis. We make this explicit in §7.

---

## 1. Introduction

**The map.** For a parameter `λ > 0` define the (Hecke) BCZ map on `Ω_λ = {(x,y) : x>0, y>0,
x + λ y > 1}` by
```
        T_λ(x, y) = ( y,  ⌊(1+x)/(λ y)⌋ · λ y − x ).
```
For `λ = 1` this is the classical BCZ map on the open triangle `𝒯 = {0<x<1, 0<y<1, x+y>1}`
(Boca–Cobeli–Zaharescu [1]), the first-return map of the
horocycle flow on `SL(2,ℤ)\SL(2,ℝ)` to the cross-section `{lattices with a horizontal vector of
length ≤ 1}` (Athreya–Cheung [2]). For `λ = λ_q := 2cos(π/q)`
it is the analogous return map for the Hecke triangle group `G_q`. The coordinates `(x, y)` are
(normalized) consecutive Farey denominators; the **observable** `P(x,y) = xy` is the product of
two consecutive Farey gaps.

**Ergodic optimization.** For a continuous self-map `T` of a space `X` and an observable
`φ : X → ℝ`, ergodic optimization studies the extreme values of `φ` over the simplex of
`T`-invariant probability measures and the structure of the optimizing ("ground state") measures
(Jenkinson, survey [3]; Bousch; Contreras [4]). The literature concentrates on expanding maps
(Gauss map, doubling, subshifts). To our
knowledge ergodic optimization has **not** been applied to horocycle-flow return maps. We do so
for the value
```
        m(P) := inf over T_λ-invariant probability measures μ of  ess-sup_μ P.
```
Minimizing the essential supremum selects the invariant measure whose support stays lowest on
the gap-product landscape.

**Results and positioning.** Our three theorems are §4–§6. The first is a near-corollary of an
elementary combinatorial bound; the second and third are the genuinely new structural facts. We
position the work honestly against prior art in §7: the *static* identity tying Farey points to
the Mertens function is due to Cox–Ghosh–Sultanow [6]; the *dynamical/per-step* formulation here
sits within the circle of per-step horocycle/Farey questions opened by Athreya–Cheung [2] (we do
not attribute a specific section or statement).

---

## 2. The window bound (combinatorial input)

Write `P_n = P(T_λ^n p)` for the products along an orbit. The single combinatorial input is:

> **Proposition 2.1 (3-window bound).** Along any orbit of `T_λ` in `Ω_λ`, no three consecutive
> products are all `< t_q`: `max(P_n, P_{n+1}, P_{n+2}) ≥ t_q` for all `n`, with `t_3 = 2/9`,
> `t_4 = √2/8`.

This is a piecewise-bilinear min–max fact (the 3-cylinder `{P_n, P_{n+1}, P_{n+2} all < t_q}` is
empty). For `q = 3` it is the contrapositive of the cluster-size bound proved (six elementary
steps) in [BCZClusterCleanProof.lean]; for `q = 4` it is `g4_no_three_below` in
[BCZHeckeG4_core.lean]. Both are machine-checked in Lean 4 / Mathlib, sorry-free, with only the
standard axioms. We take Proposition 2.1 as given.

**Remark 2.2 (no spectral meaning).** `T_λ` is area-preserving (`|det DT_λ| = 1`), so the
geometric potential is trivial and `t_q` cannot be a Ruelle resonance, a dynamical-zeta zero, or
a pressure value. `t_q` is an elementary extremum (attained in the closure at the vertex
`(1/3, 2/3)` for `q=3`); it is *not* a spectral invariant. We stress this because the underlying
project repeatedly tested, and rejected, a spectral interpretation.

---

## 3. The abstract ergodic-optimization principle

> **Lemma 3.1 (`essSup_ge_of_window`).** Let `T` preserve a probability measure `μ` on `X`, let
> `P : X → ℝ` be a.e. bounded above, let `D` be measurable with `μ(Dᶜ) = 0`, and suppose that
> along every orbit staying in `D` the 3-window bound `max(P(x_i),P(x_{i+1}),P(x_{i+2})) ≥ t`
> holds. Then `t ≤ ess-sup_μ P`.

*Proof.* If `ess-sup_μ P < t`, then `P < t` a.e.; invariance (`MeasurePreserving.preimage_null`)
propagates `P(T^n ·) < t` and `T^n · ∈ D` to all `n` simultaneously on a full-measure set
(`ae_all_iff`); any point of that set is the start of an orbit in `D` whose first 3-window
violates the bound. ∎

This is map-, observable-, and threshold-agnostic; it is machine-checked
([essSup_ge_of_window]). Both ground-value theorems below are one-line instances.

---

## 4. Theorem 1 — the ground value (sharp)

> **Theorem 4.1.** For every `T_λ`-invariant probability measure `μ` on `Ω_λ`,
> `ess-sup_μ P ≥ t_q`. Moreover `m(P) = t_q`: the bound is sharp.

*Proof.* `≥` is Lemma 3.1 applied with the window bound (Prop. 2.1) and `P ≤ 1` a.e. (machine
-checked: [essSup_bczProduct_ge] for `q=3`, [essSup_g4Product_ge] for `q=4`). Sharpness: the
period-2 orbits below realize `ess-sup` arbitrarily close to `t_q`. ∎

**The optimizing family.** For `q = 3`, the points `(a, 2a) ↔ (2a, a)` with `a ∈ (1/3, 1/2)` form
a genuine period-2 orbit (floor word `[1,4]`), with product `2a² ∈ (2/9, 1/2)`. The orbit measure
`½(δ_{(a,2a)} + δ_{(2a,a)})` is `T`-invariant with `ess-sup = 2a² → 2/9⁺` as `a → 1/3⁺`. Hence
`m(P) = 2/9`. For `q = 4`, the family is `(a, a/√2) ↔ (a/√2, a)`, `a ∈ (1/2, 1]`, word `[2,1]`
(`k₀k₁ = 2`), product `a²/√2 → √2/8⁺`.

---

## 5. Theorem 2 — no ground state

> **Theorem 5.1.** The infimum `m(P) = t_q` is **not attained**: no `T_λ`-invariant probability
> measure `μ` on `Ω_λ` satisfies `ess-sup_μ P = t_q`. Equivalently, no orbit of `T_λ` keeps all
> products `≤ t_q`.

The "equivalently" follows from the abstract principle's argument: a measure with
`ess-sup_μ P = t_q` would force a full-measure set of orbits with all products `≤ t_q`. So
Theorem 5.1 reduces to the orbit statement, which is the heart.

### 5.1 The case `q = 3` (machine-checked)

The engine is one identity. On the floor-`=1` region (`x < 1/3`, `y > 2/3`) one has
`T(x,y) = (y, y − x)`, hence
```
        P(T(x,y)) = y² − P(x,y).                                            (★)
```

> **Lemma 5.2 (`exists_product_gt_two_ninths`).** Every orbit of the `q=3` map has some product
> `> 2/9`.

*Proof.* Suppose all `P_n ≤ 2/9`. The window bound (Prop. 2.1) plus `P_n ≤ 2/9` forces some
`P_m = 2/9` with `m ≥ 1`. On `{xy = 2/9}` with `x+y>1`, the shared coordinate satisfies
`(3y−1)(3y−2) > 0`, so `y < 1/3` or `y > 2/3` (no middle). If `y > 2/3`: the forward floor is
`≥ 1`, so `P_{m+1} = k y² − 2/9 ≥ y² − 2/9 > 2/9` by (★) — contradiction. If `y < 1/3` (so the
previous shared coordinate `x = a_m > 2/3`): the predecessor floor is `1`, and (★) backward gives
`P_m = a_m² − P_{m-1} > (2/3)² − 2/9 = 2/9`, contradicting `P_m = 2/9`. ∎

Theorem 5.1 for `q=3` follows ([no_ground_state]). **Both Lemma 5.2 and the measure form are
machine-checked in Lean** (sorry-free; standard axioms only), via the helper
`bczMap_snd_floor_one` for (★) and `not_two_ninths_at` for the two-case core.

**Why the infimum is unattained — the mechanism.** The only candidate optimizer is the limit of
the period-2 family, `μ_* = ½(δ_{(1/3,2/3)} + δ_{(2/3,1/3)})`. But `T(1/3,2/3) = (2/3,1)` and
`T(2/3,1/3) = (1/3,1)`: both vertices are sent onto the *top edge* `{y=1} ⊆ ∂𝒯`, not onto each
other. Thus `μ_*` is **not** `T`-invariant (the preimage of `{y=1}` carries full `μ_*`-mass while
`{y=1}` carries none — machine-checked: [vertexMeasure_not_invariant]). The infimum's only
candidate minimizer fails invariance, and Theorem 5.1 shows nothing replaces it.

### 5.2 The case `q = 4` (rigorous; not yet formalized)

The `q=4` map shares the conclusion but **not** the proof: its region constraint on
`{xy = √2/8}` is `8√2 (y − √2/4)² > 0`, a *double root* at `y = √2/4`, excluding only that point
(contrast `q=3`, which excludes the whole interval `(1/3, 2/3)`). This leaves a **middle band**
`x, y ∈ [√2/4, 1/2]` — where a floor-`=1` step is an elliptic rotation by `π/4` — reachable by
neither one-step argument. The complete proof uses four cases (`s := √2`, `t := s/8`; floor
`k ≥ 1` always along a valid orbit; floor-`=1` gives `P(T₄(x,y)) = s y² − P`):

- **A.** `y > 1/2`: `P_{m+1} = k s y² − t ≥ s y² − t > s/4 − t = t`.
- **A′.** `y ∈ (√2/4, 1/2]` with floor `k ≥ 2`: `P_{m+1} ≥ 2 s y² − t > t`.
- **B.** `x > 1/2`: backward — `P_m = k' s x² − P_{m-1} ≥ s x² − t > t`, contradicting `P_m = t`.
- **Middle.** `x, y ≤ 1/2` with forward floor `k = 1`: then `a_{m+2} = s y − x < √2/4`, which
  forces the floor at step `m+1` to be **exactly 3** (because `(1+y)/(s a_{m+2}) ∈ (3,4)`), giving
  `P_{m+2} = 3 s (s y − x)² − (s y² − t) > t`.

Every `√2/8`-point is killed; the case partition and the floor-`=3` step are verified numerically
([TrackA5_g4_middle.py], all checks pass). Theorem 5.1 holds for `q = 4`. A Lean formalization of
the `q=4` case (comparable in size to `g4_no_three_below`) is left to future work; the `q=3` case
is the formally-certified flagship.

**Interpretation.** Theorem 5.1 places the BCZ/Hecke return maps among the rare *natural* systems
with **no ground state** for a natural observable — the optimizing locus is a boundary limit at a
floor discontinuity, never realized by an invariant measure. This contrasts with Contreras's
generic periodicity of ground states [4], and is forced here by the arithmetic
(floor-discontinuity) structure rather than by a delicate genericity failure.

---

## 6. Theorem 3 — the arithmetic dichotomy

A period-2 ground-state configuration is a `2`-cycle of the diagonal recurrence
`c_{n+2} = k_n λ c_{n+1} − c_n` realizing the infimum. Its matrix is `M = B_{k_0} B_{k_1}` with
`B_k = [[0,1],[−1, kλ]]`, `det B_k = 1`. A 2-cycle needs `tr M = 2` (parabolic, eigenvalue 1),
i.e. `λ² k_0 k_1 − 2 = 2`, i.e.
```
        k_0 k_1 = 4/λ² = sec²(π/q).
```

> **Theorem 6.1.** Among the Hecke triangle groups, an interior period-2 ground-state
> configuration exists **iff** `sec²(π/q) ∈ ℤ` and `q < ∞` — i.e. iff `q ∈ {3, 4}`, giving the
> two ground values `2/9` and `√2/8`.

*Proof sketch.* `sec²(π/q) = 4/λ_q²`: `q=3 → 4`, `q=4 → 2`, `q=6 → 4/3`, `q=∞ → 1`. For `q ∈
{3,4}` the integer factorizations of `k_0 k_1` give the families of §4; for `q = 6`,
`sec² = 4/3 ∉ ℤ` so no integer floor word works (the optimizer degenerates to the boundary `b→0`);
for `q = ∞` (theta group) `λ = 2` is parabolic and the finite-region cross-section degenerates
(no genuine interior cycle). Hence exactly `{3,4}`. ∎ (Hand-proof; numerically corroborated.)

The dividing line is the Niven-type condition `sec²(π/q) ∈ ℤ` (`⇔ tan²(π/q) ∈ {0,1,3}`), **not**
arithmeticity: it is a clean two-condition criterion rather than a "family law in `q`."

---

## 7. Relation to prior work, and honest limitations

- **Prior art.** The *static* Farey↔Mertens identity is Cox–Ghosh–Sultanow [6]. The BCZ map and
  Farey gap statistics are Boca–Cobeli–Zaharescu [1] and Marklof [5]; the cross-section is
  Athreya–Cheung [2], in whose circle of per-step/dynamical questions this work sits (we do not
  attribute a specific section). The fine-scale (`h`-tuple) gap distributions are computed by
  Marklof [5]; consequently the *limiting distribution* of
  cluster sizes is a derived functional of known statistics and is **not** claimed here as new —
  we deliberately restrict to the *deterministic* threshold/optimization statements, which are
  support-level facts not implied by those distributional results.
- **What is new:** (i) the ergodic-optimization framing of horocycle return maps; (ii) the
  no-ground-state theorem (Thm 5.1); (iii) the `sec²(π/q) ∈ ℤ` dichotomy (Thm 6.1); (iv) the
  Lean 4 formalization of the `q=3` chain.
- **What is *not* claimed.** The bounds `2/9`, `√2/8` are elementary; `t_q` is not spectral (§2);
  nothing here is conditional on, or bears on, the Riemann Hypothesis or the Mertens function.
  The audience is ergodic optimization + homogeneous dynamics; the contribution is structural and
  expository, plus the formal verification — not a new analytic tool.

---

## 8. Formalization

All `q = 3` statements are formally verified in Lean 4 (Mathlib v4.28.0), sorry-free, depending
only on `[propext, Classical.choice, Quot.sound]`:
`WindowBound` (Prop. 2.1, from the v8 cluster proof), `essSup_ge_of_window` (Lemma 3.1),
`essSup_bczProduct_ge` (Thm 4.1), `bczMap_snd_floor_one` + `not_two_ninths_at` +
`exists_product_gt_two_ninths` + `no_ground_state` (Thm 5.1), and the equality-locus refutation
`vertexMeasure_not_invariant`. The `q=4` window bound (`g4_no_three_below`) and ground value
(`essSup_g4Product_ge`) are likewise machine-checked; the `q=4` no-ground-state proof (§5.2) and
Theorem 6.1 are rigorous on paper and numerically verified, with Lean formalization left to
future work. Source: `projects/aristotle_dispatch_v9/BCZErgodicOptimization.lean`,
`projects/mimo-mini-project/code/BCZHeckeG4_core.lean`,
`projects/aristotle_dispatch_v8/BCZClusterCleanProof.lean`.

---

## 9. References

*(Citations 1–6 verified against primary sources — arXiv / journal pages — on 2026-05-29.)*

1. F. P. Boca, C. Cobeli, A. Zaharescu. *A conjecture of R. R. Hall on Farey points.* J. Reine
   Angew. Math. **535** (2001), 207–236. [Introduces the BCZ map / Farey gap density `2·𝟙_{x+y>1}`.]
2. J. S. Athreya, Y. Cheung. *A Poincaré section for the horocycle flow on the space of lattices.*
   Int. Math. Res. Not. IMRN **2014**, no. 10, 2643–2690; arXiv:1206.6597.
3. O. Jenkinson. *Ergodic optimization in dynamical systems.* Ergodic Theory Dynam. Systems
   **39** (2019), 2593–2618; arXiv:1712.02307.
4. G. Contreras. *Ground states are generically a periodic orbit.* Invent. Math. **205** (2016),
   383–412; doi:10.1007/s00222-015-0638-0; arXiv:1307.0559.
5. J. Marklof. *Fine-scale statistics for the multidimensional Farey sequence.* arXiv:1207.0954
   (2012); in *Limit Theorems in Probability, Statistics and Number Theory*, Springer Proc. Math.
   Stat. **42** (2013).
6. D. Cox, S. Ghosh, E. Sultanow. *The Farey Sequence and the Mertens Function.* arXiv:2105.12352
   (2021).
7. The mathlib Community. *The Lean Mathematical Library (Mathlib4).* [pin the exact commit used.]

---

### Appendix A — status ledger (for the authors, delete before submission)

| Result | Status |
|---|---|
| Prop. 2.1 window bound, q=3 / q=4 | Lean ✓ / Lean ✓ |
| Lemma 3.1 abstract principle | Lean ✓ |
| Thm 4.1 ground value, q=3 / q=4 | Lean ✓ / Lean ✓ |
| Thm 5.1 no ground state, q=3 | Lean ✓ |
| Thm 5.1 no ground state, q=4 | paper ✓ + numerics ✓; Lean TODO (g4_core-scale) |
| Thm 6.1 dichotomy | paper ✓ + numerics ✓; Lean TODO |
| §5.1 equality-locus refutation | Lean ✓ |
