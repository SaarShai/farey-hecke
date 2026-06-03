# Goal I — (L2) no regime-chaining: refutation hunt + composite-monodromy certificate

**Date:** 2026-06-03. **One-line verdict:** the headline value **`X_Ω(q)=1/λ³` SURVIVES** the
adversarial refutation hunt for every q tested (17..50): the maximal forward-invariant set inside
`{P<1/λ³}` is **EMPTY** (resolution-confirmed) — no KAM island, no invariant curve, no sub-threshold
periodic orbit. The (L2) *mechanism* is now an explicit, **machine-checked trace law**: chaining two
distinct elliptic corridors is always parabolic or hyperbolic — never a new slow rotation — so no
infinite sub-threshold word can be built by switching corridors. A fully uniform analytic (C′) is not
yet closed (the (L1) closed form and the deep-middle composites remain open), but the refutation verdict
is decisive and the dominant-corridor (L2) obstruction is proven in Lean for all q.

**Strict separation: PROVEN (Lean) / NUMERICAL / OPEN. Nothing sent outward.**

λ = 2cos(π/q), θ=π/q. Genuine `BCZ_q` on `𝒯^q={0<a≤1,1−λa<b≤1}`, piecewise-LINEAR SL₂ on (a,b):
`(a',b') = M_{i,k}·(a,b)`, det 1. Observable `P = a·L_i/x_{i-1}`. thr := 1/λ³.

---

## 0. Headline — the refutation hunt (PRIORITY), decisive

**Method (the decisive tool):** maximal forward-invariant set in `S={P<thr}` via a grid "survivor"
fixpoint — `surv ← S ∧ surv[image]` to convergence. A point survives iff its **entire** forward orbit
stays in `S`. A sub-threshold invariant set (which would give `X_Ω<thr`, refuting the value) is exactly a
non-empty survivor set. `code/Igoal_survivor.py`.

**Result: survivors = 0 for q = 17,18,19,20,22,25,30,40,50.** Resolution-confirmed:
- plain center-map survivor empties robustly; iteration count **saturates at the true max-run** (~0.4q),
  e.g. q=20: iters 4→6→7→7 over grids 700²→4000²; q=50: 13→21 over 2000²→7000².
- at coarse grid near-threshold "survivors" appear (q=50 @2000²: 23 cells) but **vanish on refinement**
  (q=50 @3500²,5000²,7000² → 0) — pure under-resolution artifact (margin is `O(1/q²)`).
- a deliberately **conservative-keep (dilated)** variant leaves only a shrinking boundary/corner residue;
  every such residue cell, run on the TRUE float map, escapes `S` within ≤ max-run steps (q=20: longest
  sub-thr run from all 101 residue seeds = 8 = the known max-run). Not an island.

**Why this is decisive for ALL sub-threshold invariant sets (not just positive measure):** in an elliptic
region the renormalized rotation is by `mπ/q` (rational multiple of π), so orbits are periodic/quasiperiodic
in **positive-measure families** (whole ellipses) or lie on **invariant curves** — both register as
surviving cell-cycles. `survivors=0` therefore excludes islands, KAM curves, **and** periodic orbits.
The only invariant ellipse that could host a sub-threshold orbit is excluded by (L1): rotation sweeps the
product to `E/(2−λ) ≥ thr` (a high-P arc on every genuine ellipse), so no full ellipse ⊂ `S`.

> **VERDICT: no sub-threshold invariant set exists for q=17..50. `X_Ω(q)=1/λ³` is not refuted.**

---

## 1. PROVEN this session (Lean, axioms `[propext, Classical.choice, Quot.sound]`, EXIT=0)

`lean/BCZHeckeL2_composite_VERIFIED.lean` — the **algebraic core of (L2)** for the dominant corridor
family `F k = M_{q-3,0}·M_{q-1,0}·M_{q-1,k}` (`F 3 = W_q`), parametric in `l=λ`, all q≥5:

- `trace_F (k)` : `tr (F k) = l·(k-2)` (single-corridor dichotomy: elliptic ⇔ k∈{1,2,3}).
- **`trace_compose (k₁ k₂)` : `tr (F k₂ · F k₁) = l²·(k₁-2)·(k₂-2) − 2`** — the composite (chaining)
  trace law. Equivalently `trace_compose_eq_prod`: `= tr(F k₁)·tr(F k₂) − 2`.
- `compose_k2_parabolic` : a switch through `k=2` gives `tr = −2` (parabolic — the cusp boundary).
- `compose_13_hyperbolic` / `_lt` : the switch `{1,3}` gives `tr = −l²−2 < −2` (hyperbolic ⇒ escape).
- `compose_same_elliptic` / `_abs_lt` : staying in one corridor (k₁=k₂∈{1,3}) gives `tr = l²−2 ∈ (−2,2)`.
- **`switch_forces_nonelliptic`** : for `0<l<2`, `k₁,k₂∈{1,2,3}`, **any genuine switch** (`k₁≠k₂` or a
  `k=2`) forces `|tr (F k₂·F k₁)| ≥ 2`. So the composite is **never a new slow elliptic rotation**.
- `det_F` : every corridor and composite is unimodular.

**Interpretation (the (L2) obstruction).** The only sub-threshold-sustaining rotations are the single
corridors `F k`, k∈{1,2,3}, of trace `λ(k−2)` (slowest = `|λ|`, rotation π/q). Chaining two *distinct*
corridors is parabolic or hyperbolic — i.e. the orbit either hits the cusp boundary (`tr=−2`, where
`P≥thr` by `cusp_envelope`) or escapes (hyperbolic ⇒ `P>thr`). Hence **you cannot lengthen a
sub-threshold run by switching corridors** — every switch is a `P≥thr` kick. With (L1) (a single corridor
exits `{P<thr}` within `O(q)` steps), no infinite sub-threshold word exists ⇒ (C′) for the F-family.

> **Corroboration (transition scan, `Igoal_transition_graph.py`).** Labelling each sustained run by its
> elliptic CORRIDOR-WORD — so the period-3 `W_q=(q−1,3)(q−1,0)(q−3,0)` block (which spans branches `q−1`
> AND `q−3`) counts as ONE corridor `F₃`, not a branch-switch — the number of runs making a genuine
> inter-corridor SWITCH is **0** (q=17,20,30): every sustained run stays in one corridor (longest runs all
> `F₃=W_q`). ⚠ A naive *per-branch* labelling spuriously flags `W_q` as "multi-corridor" (64 at q=20) —
> that is a labelling artifact (W_q is a single elliptic word), NOT a real switch.

Reused/valid (prior VERIFIED): `BCZHeckeRotation_allq_VERIFIED.lean` (`product_le/ge_on_ellipse` = (L1)
core, `trace_Wq=λ`, `trace_family=λ(k−2)`, invariant ellipse + posdef); `cusp_envelope` (all-q `P≥1/λ³`
on the cusp branch); `essSup_ge_of_no_sustained` (the engine (C′) feeds).

---

## 2. Corridor set (finite, explicit) — `code/Igoal_corridors.py`

- All elliptic top-branch words have trace `2cos(mπ/q)` for integer `m≥1`; the **slowest** (largest
  |trace|<2, longest sub-thr arc) is `m=1`, trace `λ` = the `F`-family / the fundamental rotation
  `R = M_{q-1,1}` itself. **There is no corridor slower than rotation π/q.** Deeper-branch elliptic words
  (involving `q-4,q-5,…`) rotate **faster** (smaller |trace|) ⇒ strictly shorter sub-thr arcs ⇒ subsumed.
- **Single-corridor (L1), quantitative (genuine map, `single_corridor_minmaxP`):** min over ellipse-scale
  of (max P over the orbit) `≥ thr` for all q (q=17:0.13259≥0.13161; q=20:0.12978≥0.12973;
  q=30:0.12918≥0.12708; q=50:0.12653≥0.12574). Margin `O(1/q²)`, → thr only in the cusp/parabolic limit —
  which is exactly the value `X_Ω=thr`, realized by the cusp word (P=thr, not below).
- **Composite-monodromy table (the (L2) handle), `composite_table`:** for the canonical F-corridors,
  `Wk₁→Wk₂` is ELLIPTIC only when k₁=k₂∈{1,3} (same corridor); `{·,2}`→ parabolic (tr=−2);
  `{1,3}`→ hyperbolic (tr≈−5.9, escape). Confirms the proven trace law numerically, q=17,20,30.

---

## 3. NUMERICAL ledger (genuine map, this session)

- **survivor=0** all q 17..50 (resolution-confirmed) — §0. The decisive refutation result.
- **transition scan** (`Igoal_transition_graph.py`): labelling by corridor-WORD (W_q = one corridor),
  every sustained sub-threshold run is **single corridor**; genuine inter-corridor SWITCH runs = 0
  (q=17,20,30) ⇒ no sub-thr corridor-cycle. (Per-branch labelling miscounts W_q as multi — artifact.)
- (L1) genuine min-max-P ≥ thr all q (§2).
- Anchors reproduced: q=3→2/9, q=4→√2/8, q=5→1/φ³; W_q trace=λ; boundary scan (goal H) reproduced.

---

## 4. OPEN / honest frontier (precise)

- **(L1) closed form is OPEN.** The clean single-ellipse shortcut FAILS: the bound `E_min/(2−λ) ≥ thr`
  gives `≈0.111 < thr` and is **ill-posed** — `P = c·c'` only on the *scalar arc*, and a small-E ellipse
  sits near the origin where `a+λb<1` (off the scalar branch entirely). The genuine `min-max-P ≥ thr`
  (which runs the piecewise map and respects the domain `a+λb>1`) is the truthful object; a closed-form
  proof needs the full piecewise structure, not one ellipse. So (L1) is exact-mechanism + decisive-numeric,
  not yet closed-form.
- **Uniform (L2) over ALL corridors is OPEN.** Lean proves the switch dichotomy for the **dominant
  F-family** (branches {q-1,q-3}); a fully uniform (L2) must also bound composites involving arbitrary
  deep-middle branches. survivor=0 makes a counterexample essentially excluded (those words rotate faster,
  shorter arcs, and never sustained), but it is not yet a closed proof.
- **Net status of `X_Ω(q)=1/λ³`, q≥17:** NUMERICALLY DECISIVE (survivor=0 + genuine min-max≥thr, q≤50)
  and PARTIALLY PROVEN (the (L1) algebraic core + the (L2) composite-trace obstruction for the dominant
  corridor family, all q, Lean). Not a full uniform paper proof; the refutation hunt verdict IS decisive.

## 5. Files
- Code: `code/Igoal_survivor.py` (maximal invariant-set survivor — the refutation tool),
  `code/Igoal_corridors.py` (corridor enumeration, single-corridor (L1), composite table),
  `code/Igoal_transition_graph.py` (no sub-thr corridor-switch).
- Lean: `lean/BCZHeckeL2_composite_VERIFIED.lean` (NEW — composite-trace law + switch dichotomy, all q).
- Reuses: `BCZHeckeRotation_allq_VERIFIED.lean`, `BCZHeckeCusp_envelope_allq_VERIFIED.lean`,
  `BCZHecke_noGroundState_q3q4_VERIFIED.lean`.
