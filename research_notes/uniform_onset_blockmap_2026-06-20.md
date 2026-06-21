<!-- P1-scout block-map for the uniform onset bound X_Ω(q) ≥ 1/λ_q³. 2026-06-20. READ-ONLY scout; this is the only file written. -->

# Uniform-onset proved/open block-map — X_Ω(q) = 1/λ_q³

Target for the energy-route and gap agents. Root:
`/Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v15/uniform_q5to18/`.
λ_q = 2 cos(π/q); threshold t = 1/λ_q³ = cusp-tip value of P_gen at corner (1/λ, 0).

## (1) What is machine-verified for q = 5..21 (lemma + file)

EQUALITY X_Ω(q) = 1/λ_q³ as a NON-ATTAINED infimum over the closed-section /
P_gen invariant-measure class, axiom-clean `[propext, Classical.choice, Quot.sound]`:

- core: `OnsetEquality.Xomega_eq` (`OnsetEquality.lean`); halves `Xomega_ge`,
  `Xomega_le`, `cusp_dirac_admissible`.
- q=5 (golden L) + q=6 FULLY CLOSED, NO hypotheses (band facts discharged
  in-file via `cos_pi_div_five`/`cos_pi_div_six`; window `wins6_q5`/`wins6_q6`):
  `OnsetEqualityLowQ.Xomega_eq_q5_concrete`, `.Xomega_eq_q6_concrete`
  (`OnsetEqualityLowQ.lean`).
- q=7..21: `OnsetEqualityUniform.Xomega_eq_uniform`, `.Xomega_eq_q{7..21}`
  (`OnsetEqualityUniform.lean`) — equality modulo per-q band facts (arithmetic
  truths about λ_q) + per-q F-window `hF{q}`.

LOWER bound X_Ω(q) ≥ 1/λ_q³ (scalar F-window route, no corridor), axiom-clean:
`GenuineMapFacts.Xomega_lb_q5to21` (`ToplevelStitchQ5to21.lean` /
`GenuineMapFacts.lean`); built on `UniformOnset_q5to18.Xomega_lb_q5to18` (q≤18).

UPPER bound: cusp parabolic-Dirac δ_{(s,0)}, s↓1/λ, gives s²/λ → 1/λ³
(`OnsetEquality.Xomega_le`; `BCZHeckeGenuine_allq_VERIFIED.cusp_gt_inf`,
`.cusp_approaches`). The SAME Dirac is INADMISSIBLE in the scalar/P_prod/Dcorr
engine class (`EqualityUB.cusp_dirac_inadmissible`, `EqualityUpperBound.lean`) —
so equality is correctly stated over the closed section, not the scalar engine.

Mechanism algebra (det/trace/ellipse, q-uniform, axiom-clean):
`BCZHeckeNoInfiniteRotation_allq_VERIFIED.{E_conserved, no_infinite_rotation}`
with E = c_n² + c_{n+1}² − λ c_n c_{n+1}; corridor block monodromy M_W trace=λ,
det=1, `MW_preserves_ellipse` in the corridor/L1b files.

## (2) The per-q corridor-confinement obligation hCorr

For q ≤ 21 there is NO hCorr: confinement is discharged directly by the per-q
F-window certificate (Layer 4). The actual per-q obligation is the F-WINDOW
predicate `UQ.FwindowHyp{4,5,6}` (`UniformOnset_q5to18.lean:144/156/168`),
discharged by `BCZHeckeG{q}_window_VERIFIED.g{q}_no_window_below_genuine`:

> For every λ with mpoly_q(λ) and 9/5<λ<2, and every corridor sequence c (0<c_n≤1,
> c_n+λc_{n+1}>1, λc_n+c_{n+1}>1, BCZ recurrence c_n+c_{n+2}=⌊(1+c_n)/(λc_{n+1})⌋λc_{n+1}),
> NO index i has W consecutive products c_{i+j}·c_{i+j+1} < 1/λ³ (j=0..W−1).

W (window length) per q: **4-window** q∈{5,7,8,9,10,11}; **5-window** q∈{12,13,14,15,16};
**6-window** q∈{17,18,19,20,21}. So the per-q obligation hCorr discharges is:
"no length-W sub-threshold corridor run exists," with W = the empirical cluster
ceiling B(q)+1 for that q.

hCorr proper (the NAMED hypothesis) only appears in the q≥22 all-q assembly
`ToplevelStitch.Xomega_lb_allq` (`ToplevelStitch.lean:343`): it packages
"1/λ³ ≤ ess-sup_μ P_gen" as delivered by the M_W block-monodromy + L1b route,
i.e. the wiring of the block-boundary sequence to an actual Tmap-orbit essSup
(+ realization bridge hbridge: g_corr ≤ g_true). That dynamical wiring is NOT a
discharged theorem — its analytic input L1b IS sealed (`L1bArcCoverage.fcorr_lb`,
`.B1_target`).

## (3) Why the method caps at q = 21 (what breaks at 22)

The fixed-window method is literally a FIXED finite window. The F-window
predicate has a HARD-CODED conjunct count W (`FwindowHyp4/5/6`). There is no
`FwindowHyp7` and none can be a single fixed bound, because:

- The sub-threshold cluster ceiling B(q) = (#consecutive π/q rotation-arc steps
  inside the sub-threshold sector) + 1 grows ~0.22·q (asymptotic slope w_∞/π).
  A window of length W refutes a run only when W > B(q).
- Empirically B(q) crosses 5 right around q = 22. The escalation in the verified
  files tracks this exactly: 4-window holds through q=11 (B≤3), 5-window through
  q=16 (B≤4), 6-window through q=21 (B≤5). At q=22 a length-6 window no longer
  refutes the (length-6) sub-threshold run, so NO fixed window works.

So the wall is NOT a Lean-engineering limit; it is structural: a per-q FIXED
window can never beat a B(q) that grows linearly. Closing q≥22 by THIS route
needs the closed-form cluster-growth law B(q) = ⌊w(q)q/π⌋ + 1 (currently
NUMERICAL only) to supply a q-dependent window length — i.e. replace the fixed
window with `L_blk q = ⌈33q/256⌉ + 2` (`L1bArcCoverage.L_blk`) and prove the
corresponding arc-coverage at that length (L1b — already sealed for the corridor
abstraction, but not wired to a Tmap-orbit via hCorr).

## (4) Where the Koyama energy route plugs in

The fixed-window route refutes long sub-threshold runs combinatorially, per q.
The energy route replaces this q-by-q combinatorics with ONE q-independent
dynamical argument, discharging exactly **hCorr** (the corridor-assembly
hypothesis), which is the only thing the all-q lower bound carries beyond L1b.

Concretely:
- Conserved energy E = c_n² + c_{n+1}² − λ c_n c_{n+1} is exactly the invariant
  of the trace-λ elliptic rotation M = [[0,1],[−1,λ]] (k=1 BCZ step), rotation
  angle θ = π/q. `E_conserved` + `no_infinite_rotation` already PROVED (axiom-
  clean, q-uniform) — a pure rotation run is finite.
- The MISSING piece hCorr needs: (a) ESCAPE-OF-MASS — a corridor switch forces
  |trace| ≥ 2 (`switch_forces_nonelliptic`, `trace_compose`), hence
  parabolic/hyperbolic, hence mass escapes the corridor; combined with the
  cusp envelope (cusp steps super-threshold, `cusp_step_bound`) this confines
  any sustained sub-threshold orbit to ONE corridor word. (b) The rotating
  observable P_n = a sinusoid of nθ on the conserved ellipse must cross 1/λ³
  within the in-domain arc; this is L1b (`fcorr_lb`, SEALED).
- The TRANSFER-OPERATOR formulation is the clean replacement for hCorr: instead
  of wiring block-boundary sequences to a Tmap-orbit essSup per q, show the
  transfer operator on the corridor cross-section has no invariant measure
  supported entirely in the sub-threshold sector (escape-of-mass rate bounded
  below by the elliptic rotation sweeping the super-threshold arc each O(q)
  blocks). That gives ess-sup_μ P_gen ≥ 1/λ³ DIRECTLY and q-independently —
  exactly the conclusion `hCorr` asserts at `ToplevelStitch.lean:343-346`.

So the energy route REPLACES `hCorr` (and removes the per-q F-window escalation
entirely), leaving only L1b (sealed) + the genuine-map orbit-invariance bridge
(P2, `GenuineClassP2.hEject`) as inputs.

## (5) Single cleanest q-INDEPENDENT sub-lemma to target first

**"No invariant probability measure of the single-corridor block map is supported
entirely in the sub-threshold sector":** i.e. the escape-of-mass lemma —
for every q, any M-rotation (θ=π/q) trajectory confined to the conserved
ellipse E=const inside the corridor must enter the super-threshold arc
{P_gen ≥ 1/λ³} within O(q) blocks, with the arc-width bounded BELOW by a
positive constant (Δ(q) → 0.1282π > 0) uniformly in q.

This is the q-independent core because: it needs NO per-q minpoly, NO per-q
window count; it is pure rotation-on-a-fixed-ellipse geometry; its analytic
half (the arc-coverage inequality 2·arccos(2√6/5)/π < 33/256, `arc_coverage_ineq`,
and L1b `fcorr_lb`) is ALREADY SEALED. What remains is the MEASURE-THEORETIC
wrapper: rotation by a fixed irrational-multiple-of-π angle on a compact arc has
no invariant sub-arc measure (equidistribution / no-dwell) — this is the single
clean lemma that turns the sealed pointwise arc-coverage into the hCorr essSup
bound, q-independently. Target statement form:

> For 0<λ<2, θ=π/q, and the conserved ellipse E, the rotation R_θ has no R_θ-
> invariant probability measure μ with μ({P_gen ≥ 1/λ³}) = 0.

Discharging this discharges hCorr for ALL q at once.

## Key files
- `OnsetEquality.lean`, `OnsetEqualityUniform.lean`, `OnsetEqualityLowQ.lean`,
  `EqualityUpperBound.lean`, `GenuineClassDischarge.lean` — equality route.
- `BCZHeckeUniformOnset.lean` (engine, Fwindow4/5/6, cusp_step_bound,
  per_q_Xomega_lb_6win), `UniformOnset_q5to18.lean` (FwindowHyp + per-q
  discharge), `GenuineMapFacts.lean`/`GenuineMapFactsP1.lean` (q19-21 + P1),
  `ToplevelStitch.lean` (hCorr, Xomega_lb_allq), `ToplevelStitchQ5to21.lean`.
- `L1bArcCoverage.lean` (L_blk, g_corr, fcorr_lb SEALED).
- `EjectionUniform.lean` (deep-mid ejection), `BCZHeckeS1_trichotomy.lean`.
- mimo: `BCZHeckeNoInfiniteRotation_allq_VERIFIED.lean` (E_conserved,
  no_infinite_rotation), `BCZHeckeGenuine_allq_VERIFIED.lean` (cusp value),
  `BCZHeckeXOmega_corridor_q18_UNCONDITIONAL.lean` (trace_compose,
  switch_forces_nonelliptic, peak_touch_exists).
