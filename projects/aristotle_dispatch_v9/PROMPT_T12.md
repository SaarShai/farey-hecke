# Aristotle v9 / T12 — formalize the BCZ ERGODIC-OPTIMIZATION promotion in Lean

(Companion to the existing `PROMPT.md` in this directory, which is the *sharpness* dispatch.
This brief is for `BCZErgodicOptimization.lean`, the *lower-bound / ergodic-optimization*
promotion. Do not touch `BCZSharpness.lean` or its `PROMPT.md`.)

## Goal

Promote the proven pointwise 3-window bound (v8 `cluster_size_le_two_clean`) to:

1. **Orbit form** — every BCZ orbit has forward ceiling `sup_n P(Tⁿx) ≥ 2/9`; infimum over
   orbits `= 2/9`, attained only at the period-2 vertex orbit `(1/3,2/3) ↔ (2/3,1/3)`.
2. **Measure form** — for every `bczMap`-invariant Borel probability `μ`, `essSup P μ ≥ 2/9`,
   with equality iff `μ = ½(δ_{(1/3,2/3)} + δ_{(2/3,1/3)})`.

## File

`BCZErgodicOptimization.lean` (provided). It reuses v8's `bczTriangle`, `bczMap` definitions
verbatim and abstracts v8's theorem behind `WindowBound` (the symmetric 3-window bound).

In the real build, place this file in the same Lake library as `BCZClusterCleanProof.lean`
(or `import` it) and supply the real `cluster_size_le_two_clean` to `windowBound_of_cluster`.

## What already compiles (target: keep it compiling, no `sorry` here)

- `windowBound_of_cluster` — derives `WindowBound` from the v8 theorem by contrapositive.
- `orbit_ceiling_ge`, `orbitCeiling_ge_two_ninths` — ORBIT-form lower bound (`≥ 2/9`).
- `vertexOrbit`, `vertexOrbit_product`, `vertexOrbit_ceiling_eq` — vertex orbit witnesses the
  infimum `= 2/9`.

These use only `linarith`, `nlinarith`, `max_lt`, `le_csSup`, `csSup_singleton`, `omega`,
`split_ifs`, `norm_num`. Verify they compile; fix any API-name drift (`csSup_singleton`,
`le_csSup`, `BddAbove`).

## What is `sorry`-quarantined (your job to complete or honestly report blockers)

### (A) `essSup_bczProduct_ge` — the measure-form INEQUALITY. **Tractable. Highest priority.**

Roadmap (also in the file + `T12_proof_writeup.md` §2):
1. `by_contra`; from `essSup P μ < 2/9` pick rational `t` with `essSup P μ < t < 2/9`.
2. `A := {x | bczProduct x ≤ t}`. From `essSup P μ < t` derive `μ Aᶜ = 0`
   (`MeasureTheory.measure_essSup_lt` / `ae_lt_of_essSup_lt` style: `P ≤ t` a.e.).
3. For each `n`, `μ ((bczMap^[n]) ⁻¹' Aᶜ) = μ Aᶜ = 0` via
   `(hinv.iterate n).measure_preimage` (measurability of `Aᶜ` needed — `P` is continuous, so
   `A` is closed/measurable).
4. `Gᶜ = ⋃ n, (bczMap^[n]) ⁻¹' Aᶜ` is null (`measure_iUnion_null`), so `μ G = 1`.
5. `μ G = 1 > 0` ⇒ `G.Nonempty` (`Measure.measure_pos` / `nonempty_of_measure_ne_zero`); also
   `μ bczTriangleᶜ = 0` lets you pick `x ∈ G ∩ bczTriangle`.
6. Orbit `fun n => bczMap^[n] x`. Needs the lemma `bczMap '' bczTriangle ⊆ bczTriangle`
   (T maps the triangle into itself) — a v8-adjacent fact; prove it or add it as a hypothesis.
7. Apply `hWB` at `i = 0`: window max `≥ 2/9`, but all three products `≤ t < 2/9`. ⊥.

Mathlib has everything for steps 2–5 (`essSup`, `MeasurePreserving.measure_preimage`,
`measure_iUnion_null`, `nonempty_of_measure_ne_zero`). Step 6 is the one extra geometric fact.

### (B) `essSup_eq_two_ninths_iff` — the EQUALITY characterization. **Needs NEW infra.**

- (⇐) direction is easy: `vertexMeasure` puts all mass on two points where `P = 2/9`, so
  `essSup = 2/9`. Use `essSup_eq` on a measure with two-point support, or compute directly.
- (⇒) direction needs a lemma **v8 does NOT currently expose**: the *equality locus* of the
  Step 1–6 chain — "if a window has `max = 2/9` and the other two entries `≤ 2/9`, then the
  middle coordinate is forced onto `b = 1/3, c = 2/3`." This must be extracted from / added to
  `BCZClusterCleanProof.lean` (re-run Steps 1–6 with `≤ 2/9` instead of `< 2/9` and track the
  equality cases of each `nlinarith`). This is genuinely new work; if you cannot produce it,
  REPORT THE GAP rather than papering it — leaving the (⇒) `sorry` with a precise note is
  acceptable for this dispatch.

## Honest scope (do NOT overclaim)

- The orbit form and the measure-form *inequality* are the solid, completable results.
- The equality characterization's forward direction is the only part needing new v8 infra and
  carries a closure-vs-open-triangle caveat (the vertex orbit lies on `∂T`; over the open
  triangle `2/9` is an unattained infimum). State this in any comment, do not hide it.

## Constraints (same discipline as v8)

- 0 sorries in §1–§2 (orbit form). Measure-form `sorry`s allowed only as documented above.
- NO `aesop`, `grind`, `simp_all`, `decide`. Use `linarith`, `nlinarith`, `simp [bczMap]`,
  `norm_num`, `ring`, `omega`, `by_contra`, `push_neg`, `rcases`, `split_ifs`, and named
  Mathlib measure-theory lemmas.
- Each measure-theory step should name the Mathlib lemma it uses, for referee-scannability.
- Verify with `lake build` against Mathlib v4.28.0.

## Acceptance

- §0–§2 (definitions, `windowBound_of_cluster`, both orbit-ceiling theorems, vertex witnesses)
  compile with 0 sorries.
- `essSup_bczProduct_ge` (A) completed with 0 sorries, OR a precise blocker report on which
  Mathlib lemma is missing.
- `essSup_eq_two_ninths_iff` (B): (⇐) completed; (⇒) completed if the v8 equality-locus lemma
  can be produced, else `sorry` retained with the gap documented.
- Report every tactic used beyond the allowed list and every Mathlib lemma name relied on.

## Why this matters

v8 gives the *pointwise* `min max(Pl,Pm,Pr) = 2/9`. This v9/T12 promotes it to the
*orbit-* and *measure-level* ergodic-optimization statement — the publishable form: "no
BCZ-invariant measure sustains gap products below `2/9`, and the unique minimizer of the
ess-sup ceiling is the period-2 vertex orbit." Together with `BCZSharpness.lean` (the matching
upper construction for `t > 2/9`) this closes the sharp `2/9` phase transition at the level of
invariant measures.
