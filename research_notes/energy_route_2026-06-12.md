# Koyama's energy × cusp-escape route — proof architecture and honest standing

Date: 2026-06-13. Lead-architect synthesis of 4 investigation reports
(INV-lean-extract, INV-P-E-relation, INV-numeric-falsify, INV-escape-lit) **plus**
direct re-verification of the Lean corpus the reports under-sampled.

Target: **X_Ω(q) = inf_μ ess-sup_μ P ≥ 1/λ_q³ for all Hecke q**, λ_q = 2cos(π/q),
P = genuine gap-product observable of the Taha G_q-BCZ map.

---

## VERDICT: PROMISING-GAP (route is sound; one analytic crux + map-faithfulness remain)

The four reports converged on "energy alone cannot lower-bound P" (TRUE and important)
and concluded the route is "new mathematics, not closed." **That conclusion is correct on
the headline but the reports materially under-described the current Lean state.** Direct
inspection shows the repo has already executed Koyama's route as a *concrete corridor
arc-width argument* and reduced the entire q≥18 uniform lower bound to **one explicit
analytic inequality (L1b)**, which an interval-arithmetic certificate verifies (rigorous
endpoints) for q = 18..3000 with strictly positive — though decaying — margin. The route
is not "aspirational/spectral"; it is combinatorial-geometric and largely built.

The single most important correction to the reports: **Koyama's "conserved energy E" is NOT
used as a pointwise floor on P (the reports correctly refute that). It is used as the
conserved invariant ELLIPSE of the corridor block-monodromy M_W, whose state ROTATES by
θ=π/q per block. The energy = the ellipse; the cusp-escape = the rotating state is forced
through the super-threshold arc within a window of length ∝ q.** That is exactly Koyama's
"couple E-boundary-behaviour with escape-of-mass," realized rigorously.

---

## 1. The proof architecture (energy × cusp-escape), step by step

Let l = λ_q, threshold t = 1/l³. "Sub-threshold" = P < t. Goal: no invariant μ has
ess-sup_μ P < t, i.e. **no orbit stays sub-threshold forever** ("no sustained sub-threshold
orbit", the (C′)/GATE-2 statement). Via the verified ergodic engine this yields the bound.

### Layer 0 — abstract ergodic engine  [LEAN-VERIFIED, uniform in q]
`HeckeFullBound.essSup_ge_of_no_sustained_strict` and `.full_bound`
(BCZHeckeFullBound_Taha_Pgen_VERIFIED.lean, sorry-free, axioms clean):
  (no orbit on Taha keeps P < t forever) ∧ (μ carried by Taha, T-invariant, P ≤ M a.e.)
  ⇒  t ≤ ess-sup_μ P.
This is the clean "no-sustained ⇒ support-edge bound" reduction. It DIRECTLY answers
INV-escape-lit's gap (M1) "convert escape into a support-edge lower bound": the conversion
is the contrapositive engine above — a finite-orbit fact (no sustained sub-threshold orbit)
implies the essential-inf-of-ess-sup bound. No off-the-shelf duality is needed; the engine
is elementary and already in Lean. Also `final_nonvacuity` / `full_bound_hyp_class_inhabited`
discharge ALL hypotheses on a concrete witness (cusp Dirac), proving the engine is non-vacuous.

### Layer 1 — branch trichotomy of the genuine map  [hypothesis htri = map definition]
Every genuine step is one of: scalar F-corridor (Tmap on Dcorr) / deep-mid / cusp.
Stated as `htri` in `HeckeConfinement.genuine_no_sustained_cusp_discharged`
(BCZHeckeConfinement_VERIFIED.lean). htri is the faithful encoding of the all-q genuine map
(GAP-3 below: the map's components — cheb, L, Pobs, branchIdx selector, Casorati det=1,
corridor matrices — are all defined and sorry-free in BCZHeckeGenuineMap_allq_WIP.lean;
the missing piece is assembling them into one measure-preserving system + invariant measure).

### Layer 2 — cusp leg (C): a cusp-branch step is super-threshold  [LEAN-VERIFIED, uniform, q≥5]
`cusp_envelope` (BCZHeckeCusp_envelope_allq_VERIFIED / re-inlined in AvoidCusp, Confinement):
on the cusp branch i=q-2, with cusp guards, P = a(a+lb)/l ≥ 1/l³ (tight at the cusp tip
(1/l,0) where P=1/l³). Packaged as `cusp_step_bound`. So leg (C) is a THEOREM, not an
assumption. Plus `cusp_tip_super_threshold`: the tip has P=s²/l > 1/l³, so the cusp branch
is genuinely super-threshold (the exclusion is non-trivial).

### Layer 3 — deep-mid leg (D): a sub-threshold deep-mid step ejects in one step  [LEAN-VERIFIED, q=16..21 box]
`HeckeEjection.ejection_kick` (BCZHeckeEjection_q16to21_VERIFIED.lean): on a non-F branch,
sub-threshold ⇒ successor product λv²−uv ≥ thr, INDEPENDENT of floor k. Proved by nlinarith
on the rational box l∈[1.96,1.98], r∈[0.94,1.22], thr∈[0.129,0.1326] (⊇ q=16..21).
`deep_threshold_admissible`: 1/l³ lies in that thr-box for q=16..21.
`DeepMidElim.deepmid_only_trailing` (UNCONDITIONAL, ejection only): a deep-mid step can occur
only as the LAST step of a sub-threshold run. With the additional `entry` ingredient
(`deepmid_free_run`, numerically verified q=17..21) a sub-threshold run of length ≥2 is
deep-mid-FREE. CAVEAT: the box is per-finite-q-range (NOT uniform in q) — see Risk R3.

### Layer 4 — confinement engine: sub-threshold ⇒ pure scalar/corridor  [LEAN-VERIFIED]
`subthreshold_forces_scalar` + `genuine_no_sustained_cusp_discharged`
(BCZHeckeConfinement_VERIFIED.lean): given htri + leg (C) [discharged] + leg (D) [hdeep],
a sustained sub-threshold orbit is forced ENTIRELY onto the scalar F-corridor branch, where
the per-q F-window certificate `hF` refutes a 6-window. Companion
`HeckeAvoidCusp.subthreshold_confined_interior`: a sub-threshold orbit AVOIDS the cusp branch
(branchIdx ≠ q-2) and lies in the interior a+lb>1. This is the rigorous form of "escape of
mass cannot dwell on the sub-threshold branches." It directly addresses INV-lean-extract's
GAP-1/GAP-2 (the contrapositive of "high-floor lands on cusp" IS "sub-threshold avoids cusp").

### Layer 5 — THE UNIFORM CRUX: corridor arc-width  [REDUCED TO ONE INEQUALITY (L1b)]
This is the genuinely new mathematics and the heart of Koyama's route.
File: BCZHeckeGATE2_L1b_skeleton.lean (`GATE2L1`), all sorry-free EXCEPT the single
`L1b_target` sorry. Backing numerics: GATE2_L1b_arcwidth_interval.py (+ _derive.py),
under projects/mimo-mini-project/code/.

Mechanism (Koyama's E × escape, made concrete):
- A *sustained* sub-threshold orbit cannot switch corridors: (L2)
  `switch_forces_nonelliptic` (BCZHeckeL2_composite_VERIFIED.lean, pure 2×2 trace algebra)
  shows any F-family corridor switch has |tr| ≥ 2 (hyperbolic/parabolic ⇒ escape). So it
  rides ONE corridor word W_q = (q-1,3)(q-1,0)(q-3,0).
- The W_q block monodromy is M_W = [[-λ, 2λ²+1],[-1, 2λ]], with **det = 1, trace = λ**
  (`det_MW`, `trace_MW`): it is an ELLIPTIC ROTATION by θ=π/q on the invariant ellipse
  Q'(a,b) = a²−3λab+(2λ²+1)b² (`MW_preserves_ellipse`, `Qp_posdef`). **THIS ELLIPSE IS
  KOYAMA'S CONSERVED ENERGY E** (the analog of Eform; same trace-λ elliptic invariant).
- On the block boundary the state is a_n = r cos(nθ−ψ), and the observable is the rotating
  sinusoid P_n = (r²/2A2)[3λ/2 + √A2 cos(2(nθ−ψ)+η)], A2=1+2λ². The in-domain corridor
  (Taha lower edge a+λb>1) is a PROPER ARC of phase-width Δ(q) → 0.1282·π (a positive
  constant as q→∞, NOT shrinking to 0). Rotation by θ=π/q sweeps through this arc in
  ~Δ(q)/θ ≈ 0.1282·q blocks — the DWELL grows LINEARLY in q.
- Within a window of L_blk(q) = ⌈33q/256⌉+2 blocks (slope 33/256 = 0.12891 > 0.1282, chosen
  strictly longer than the true dwell), the max of P_n must reach 1/l³. Rigorous lower-bound
  functional g_corr(L,q) on this window-max; the reduction `no_sustained_corridor` DERIVES the
  Chebyshev recurrences and conserved ellipse from the M_W step and concludes
  ¬(∀n P_n < 1/l³), GIVEN:
    (L1b)  1/λ³ ≤ g_corr(⌈33q/256⌉+2, q)   for all q ≥ 18      [the one open sorry]
  and a geometric realization hypothesis `hbridge` (= the numerically-certified g_corr ≤ g_true).

So the FULL chain for q ≥ 18 is:
  Layer 0 engine ∘ Layer 4 confinement ∘ {Layer 2 (C) ✓, Layer 3 (D) box, Layer 5 (L1b) open}
with the residual map-faithfulness htri/hbridge (GAP-3).

---

## 2. The single hardest remaining lemma

**(L1b):  For every integer q ≥ 18, with λ = 2cos(π/q) and L_blk(q) = ⌈33q/256⌉+2,
          1/λ³ ≤ g_corr(L_blk(q), q),**
where g_corr is the corridor window-min functional (Layer 5; verbatim in the Lean skeleton
and GATE2_L1b_arcwidth_interval.py). Equivalently: the rotating-corridor observable, over a
window of ⌈33q/256⌉+2 blocks, has window-max ≥ 1/λ³ uniformly in q.

It is one-dimensional calculus: sharp control of max_{0≤n<L} cos(2μ+φ_n) (a finite cosine
window-max) divided by cos²(|μ|+H) over the open domain interval, minimized over the window
center μ. NOT an ATP/spectral object. The difficulty is purely the **uniform-in-q** asymptotic:
both g_corr and 1/λ³ → 1/8 as q→∞ (λ→2), and the proof must show their difference stays
strictly positive for all q simultaneously.

Interval-arithmetic evidence (rigorous Arb-style endpoints, GATE2_L1b_arcwidth_interval.py):
  q:      18      200     300     800     1500    3000
  margin: 7.1e-3  5.2e-4  4.1e-4  2.5e-4  1.5e-4  9.2e-5   (ALL strictly positive)
Margin decays roughly like O(1/√q) (margin·√q ≈ 0.005–0.007, near-constant) — sub-linear,
NOT crossing zero. Structural reason it stays positive: the in-domain arc-fraction converges
to 0.1282π, strictly below the chosen slope 33/256 = 0.12891π (headroom ≈ 7e-4), so L_blk is
provably longer than the true dwell for all q. A clean proof would establish this headroom
analytically (arc-fraction limit < slope) plus a uniform Taylor/Lipschitz bound on the
window-max near the limit.

Target Lean/paper statement (the skeleton's `L1b_target`):
  theorem L1b_target : ∀ q : ℕ, 18 ≤ q → 1/λ_q³ ≤ g_corr (⌈33q/256⌉+2) q.

---

## 3. Off-the-shelf vs genuinely new

OFF-THE-SHELF / already in Lean (cite):
- Ergodic "no-sustained ⇒ support-edge" engine: ELEMENTARY, in Lean
  (essSup_ge_of_no_sustained_strict). Does NOT need Marklof–Pollicott escape laws or
  transfer-operator spectra. INV-escape-lit's category-mismatch worry (support edge ≠
  max-excursion ≠ pressure) is REAL for those cited tools but MOOT for this route, which
  bypasses them with the elementary engine.
- SL₂ trace identities / λ = max elliptic trace / switch-forces-nonelliptic:
  in Lean (BCZHeckeL2_*; BCZHeckeL2_traceIdentity_allq). Pure 2×2 algebra.
- Energy / conserved-form machinery: in Lean (BCZHeckeNoInfiniteRotation_allq; Eform,
  E_conserved, E_pos, no_infinite_rotation) AND its corridor incarnation Q'/M_W
  (GATE2_L1b skeleton). Conceptually the trace-λ elliptic invariant — classical.
- Casorati det = 1 (area preservation): in Lean (casorati, BCZHeckeGATE2Base).
- Cusp envelope, deep-mid ejection (per-box): in Lean.
- Validated numerics engine: Ruelle/Jenkinson–Pollicott (reproduces dim E_{1,2} to 1e-15) —
  used only for cross-checks; NOT load-bearing for this route.

GENUINELY NEW mathematics (must be proved):
- (L1b) the uniform arc-width inequality (§2). NEW. Backed by interval numerics only.
- The 33/256 slope law and its asymptotic headroom over the true arc-fraction (0.1282π).
  NEW; numerically derived (arcwidth_derive.py), not yet a theorem.
- htri / hbridge faithfulness (GAP-3): a single all-q genuine measure-preserving map T on
  Taha with an invariant probability measure, such that branch trichotomy htri holds and the
  block-window realization hbridge (g_corr ≤ g_true) is a theorem. Components exist
  (BCZHeckeGenuineMap_allq_WIP, sorry-free) but the dynamical-system + measure assembly is
  unbuilt. Routine-but-substantial measure theory.
- Uniform-in-q deep-mid ejection: Layer 3 is a per-box (q=16..21) Positivstellensatz; a
  uniform-in-q version (or absorbing deep-mid into the corridor argument for all q) is open.

NOT NEEDED (reports' worry retired): a uniform-in-q transfer-operator spectral gap (M2),
a support-edge-from-escape duality (M1), a spectral interpretation of 1/λ³ (M3). The route is
combinatorial-geometric; 1/λ³ is the cusp-tip value (1/l)²/l, fully explained by Layer 2.

---

## 4. What the reports got right / wrong (adversarial reconciliation)

RIGHT (all four, important):
- "Energy conservation alone does NOT force P ≥ 1/l³" — TRUE. INV-P-E-relation's algebra is
  airtight: on a fixed energy level inf P = 0, energy gives only the UPPER bound P ≤ E₀/(2−l).
  The lower bound lives in the cusp/arc-width geometry, not in a pointwise energy floor.
- "The naive reading of Koyama is false" — TRUE for the naive (pointwise) reading.
- "1/l³ is the cusp-tip value, not a spectral eigenvalue" — TRUE (INV-numeric-falsify).
- "Per-q F-window certs are not uniform" — TRUE; the uniform replacement IS (L1b).

WRONG / under-described:
- "No transfer-operator/spectral object ⇒ route aspirational" — the route never needed one;
  the energy enters as the conserved ELLIPSE driving a rotation, and the support-edge bound
  comes from the elementary engine. Reports searched for the wrong vehicle (spectral) and
  missed the built one (arc-width).
- INV-lean-extract's GAP-1/GAP-2/GAP-3 are real but PARTIALLY CLOSED: GAP-2 (sub-threshold
  avoids cusp) is DONE (subthreshold_confined_interior, AvoidCusp file the report didn't read);
  GAP-1 is reduced to the single (L1b) with explicit window length ⌈33q/256⌉+2 (the report's
  "window must scale with q ≈ O(q²)" is right in spirit but the true scaling is O(q), linear);
  GAP-3 components exist sorry-free.
- "the residual is O(q²)" — the dwell/window is O(q) (linear, arc-fraction × q/θ), not O(q²).

---

## 5. Risks (adversarial)

R1 — (L1b) asymptotic. Margin decays (9.2e-5 at q=3000) as both sides → 1/8. Interval checks
  cannot reach q=∞. IF the arc-fraction limit equals (not strictly below) the slope, the
  margin → 0 and the route fails at large q. Current data: limit 0.1282π < slope 0.12891π
  (headroom ~7e-4 > 0), and margin·√q ≈ const > 0 ⇒ likely safe, but THIS IS THE ROUTE'S LIFE
  OR DEATH and is unproven. Mitigation: prove the arc-fraction limit < 33/256 analytically.

R2 — hbridge faithfulness. g_corr ≤ g_true is numerically certified but is a HYPOTHESIS of
  no_sustained_corridor. If the closed-form block model mis-states the true genuine corridor
  observable at some q, the bridge fails. Needs the GenuineMap assembly (GAP-3) to discharge.

R3 — deep-mid uniformity. Layer 3 ejection is a q=16..21 box; deep-mid for all q≥22 is not
  yet covered (either a growing family of boxes or absorption into the corridor argument).

R4 — q < 18. The route is scoped q ≥ 18 (the general l∈(1,2) claim is false: q=4, l=√2). The
  arithmetic small-q cases {3,4,5,6,7,...,17} are handled separately (per-q window band already
  verified q≤16; q=18 corridor). Stitching small-q + large-q into ONE uniform theorem is
  bookkeeping but must be done for the literal "all q" statement.

R5 — missing-script illusion (RESOLVED). The Lean skeleton cites code/GATE2_L1b_arcwidth_*.py
  at the top-level code/ path; the scripts actually live at projects/mimo-mini-project/code/.
  They run and certify q=18..3000. Path is stale, content is real.

---

## 6. Recommended next step

Attempt the **asymptotic-headroom lemma** behind (L1b), the cleanest provable slice:
  Show lim_{q→∞} [in-domain corridor arc-fraction] = c* with c* < 33/256, and a uniform
  one-sided Lipschitz/Taylor bound giving g_corr(⌈33q/256⌉+2,q) − 1/λ³ ≥ κ/q^{1/2} (κ>0) for
  all q ≥ 18. Concretely: expand g_corr and 1/λ³ in ε = θ = π/q about ε=0 (both → 1/8), and
  show the O(ε)/O(ε²) coefficients give a strictly positive difference once L ≥ ⌈33q/256⌉+2.
  This converts the interval evidence into a proof of (L1b) and is a self-contained calculus
  problem suitable for Aristotle or a human analyst. Parallel track: build the GenuineMap
  measure-preserving assembly (GAP-3) to discharge htri/hbridge, since (L1b) is useless without
  a faithful map. Do the calculus lemma FIRST — it is the existential risk (R1).
