# FINDINGS — Confinement assembly: eliminating the monolithic `hconfine` (2026-06-05)

## TL;DR

The genuine-map (C′) "no sustained sub-threshold orbit" was conditional on a **single monolithic
open hypothesis** `hconfine` (`BCZHeckeGenuineMap_allq_WIP.perq_general_no_sustained`):

> `hconfine : (∀ j, Q j < 1/l³) → ∃ scalar F-corridor sequence c, everywhere sub-threshold`

i.e. the global "sustained sub-threshold ⟹ confined to the scalar branch" reduction (§6 item (2),
"OPEN in Lean, numerically robust q≤30/40").

**This session eliminates `hconfine`** via a symbolic-dynamics confinement engine and reduces the open
content to a **local branch trichotomy** `htri` (= the genuine map definition) plus a single isolated
geometric lemma `hmin`. Every *dynamical* ingredient is now PROVEN, axiom-clean.

New file: `lean/BCZHeckeConfinement_VERIFIED.lean` — 9 decls, `lake env lean` EXIT=0, all
`[propext, Classical.choice, Quot.sound]`, 0 `sorryAx`.

## What is now PROVEN (axiom-clean)

| piece | decl (in `BCZHeckeConfinement_VERIFIED.lean` unless noted) | status |
|---|---|---|
| **★ Confinement engine** (the previously-open assembly) | `subthreshold_forces_scalar` | PROVEN |
| Assembled (C′), `hconfine` gone | `genuine_no_sustained_assembled` | PROVEN (mod `htri`,`hdeep`) |
| Faithfulness (legs reconstruct old `hconfine`) | `hconfine_of_legs` | PROVEN |
| **Leg (C) cusp** discharged as theorem | `cusp_envelope` / `cusp_step_bound` | PROVEN |
| Fully-cusp-discharged capstone | `genuine_no_sustained_cusp_discharged` | PROVEN (mod `htri`,`hdeep`) |
| Transfer `Pgen<t ⟹ a·b<t` | `prod_le_Pgen` / `prod_lt_of_Pgen_lt` | PROVEN |
| Scalar read-off (Tmap/Dcorr orbit ⟹ F-corridor seq) | `orbit_to_cseq_hyps` | PROVEN |
| Leg (D) threshold admissibility `1/l³∈[129/1000,663/5000]` | `deep_threshold_admissible` | PROVEN |
| Leg (D) floor-1 ejection (kick-universal, ∀k≥0) | `genuine_ejection_floor1` (WIP file) | PROVEN |
| F-window q=5..21 | `g{q}_no_window_below_genuine` | PROVEN |

### The engine (the new mathematical content)

`subthreshold_forces_scalar`: given per-step trichotomy + two legs and "every step sub-threshold",
**every step is scalar**. Three-case argument:
- a **cusp** step has `t ≤ P n` (leg C) — contradicts `P n < t`;
- a sub-threshold **deep-mid** step ejects, `t ≤ P(n+1)` (leg D) — contradicts `P(n+1) < t`;
- ⟹ the only consistent branch at every step is **scalar**.

Then the orbit is a genuine `Tmap`/`Dcorr` F-corridor sequence; the transfer turns sub-threshold
`Pgen` into sub-threshold products; the proven per-q F-window refutes the 6-window. (C′) closed,
modulo `htri`.

## Adversarial audit (4-agent workflow `wf_bf6a1ee2-7cf`, all re-verified by hand)

- **Logic red-team: SOUND.** The 3-case engine proof is individually valid; an explicit Lean
  counterexample attempt is provably blocked at the `hdeep` obligation (cannot supply `1 ≤ P(n+1)`
  under sustained sub-threshold). F-window feed `⟨hsubc 0..hsubc 5⟩` matches the six conjuncts at
  `i=0` with no off-by-one; transfer direction (`a·b ≤ Pgen`, slack `a²/l ≥ 0`) is correct.
- **Vacuity: SOUND / NON-VACUOUS.** Hypothesis class inhabited via the **cusp branch**: explicit
  witness `l=197/100`, `orbit ≡ (4/5,0)`, `deepmid ≡ False`; `htri` takes the cusp disjunct
  (`CuspGuards`), and the conclusion `¬(∀n, Pgen < 1/l³)` is genuinely FALSE there since
  `Pgen l (4/5,0) = (16/25)/l ≥ 1/l³` (from `l > 9/5`). The `(mpoly,hF,hmp)` triple is independently
  inhabited by g18 (`hF18 = g18_no_window_below_genuine`, `l = 2cos(π/18)`). Not a vacuous abstraction.
- **Numeric: SOUND.** Genuine Taha BCZ_q map, q∈{17,18,19,20,21}, ~1.2M in-domain steps/q (+ a
  boundary-stress reseed). `code/audit_confine_legs.py`. Re-run by hand:

  | q | Tviol | cuspViol | D_subthr | D_FAIL | longRun |
  |---|---|---|---|---|---|
  | 17 | 0 | 0 | 168941 | 0 | 2 |
  | 18 | 0 | 0 | 169233 | 0 | 2 |
  | 19 | 0 | 0 | 170195 | 0 | 2 |
  | 20 | 0 | 0 | 171332 | 0 | 2 |
  | 21 | 0 | 0 | 172433 | 0 | 2 |

  0 trichotomy / 0 cusp / 0 deep-mid-ejection violations; longest sustained sub-threshold run = **2**.

### Critical disambiguation (why NO Lean correction is needed)

The numeric "floor k" is the **kick coefficient** (`new_b = t_{i+1} + k·l·t_i`), and Lean's ejection
lemmas are *universally* quantified over it (`succ_prod_lb` needs only `0 ≤ k`). Empirically deep-mid
sub-threshold steps are **100% kick k=0** — a strengthening, not a restriction. This is distinct from
the **branch-selecting BCZ floor** `K = ⌊(1+u)/(λv)⌋`: `genuine_ejection_floor1` covers `K=1`
deep-mid; `K≥2` deep-mid is routed to the **cusp leg** (proven `cusp-guards ⟹ K≥2`), NOT a separate
`hdeep` obligation. So `hdeep` as stated is correct and need not be floor-restricted.

## What remains OPEN (the precise residual)

The reduction shrinks the residual from the **global** `hconfine` to:

- **(R1) Orbit-level trichotomy `htri`** — that every in-domain genuine-BCZ step falls into
  `{ scalar Tmap/Dcorr | floor-1 deep-mid | cusp-guard }`. This is the **genuine multi-branch map
  definition** (§6 item (1)). Numerically confirmed (0 None-branch over 6M in-domain steps), supplied
  to the capstone as `htri`, not yet derived.
- **(R2) High-floor (K≥2) → cusp routing**, closed modulo the isolated geometric hypothesis `hmin`
  (`BCZHeckeGenuineMap_allq_WIP` §12c, L1404-1438): the hump/no-earlier-crossing unimodality of
  `cheb i = sin(iπ/q)/sin(π/q)` on `[1,q-1]` — an `O(1/q²)` trig-geometry fact, exposed as `hmin` and
  not yet proved arithmetically.

**Honest status:** this is a *reduction + assembly*, not the unconditional theorem. The genuine map
definition (R1) and the single geometric lemma `hmin` (R2) are the only remaining gates. Everything
dynamical — engine, both legs, transfer, scalar read-off, F-window, box-containment, threshold
admissibility — is PROVEN and axiom-clean, and the assembly is certified sound and non-vacuous.

## Files

- `lean/BCZHeckeConfinement_VERIFIED.lean` (new) — the engine + assembled (C′) + cusp leg + audit hooks.
- `code/audit_confine_legs.py` (new) — genuine-map numerical leg audit (q=17..21).
- This findings doc.
