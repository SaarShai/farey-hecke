# Session summary — 2026-06-14 (Farey-Hecke)

**Branch:** `hecke-goalL-2026-06-03` · **Toolchain:** `leanprover/lean4:v4.28.0` + fresh Mathlib.
**Scope of this record:** what this session actually established, marked exactly as the underlying
records mark it — VERIFIED (machine-checked), conditional, negative, or open. Nothing here is
inflated; every claim is sourced to a research note and/or a Lean file that was built first-hand
this session. The standard axiom set for "axiom-clean" throughout is
`[propext, Classical.choice, Quot.sound]` (no `sorryAx`, no `nativeDecide`).

Source of truth: the auto-memory index, the `research_notes/*_2026-06-14.md` notes, and the Lean
files under `projects/aristotle_dispatch_v15/uniform_q5to18/`.

---

## A. VERIFIED — machine-checked, axiom-clean

### A.1 Onset theorem `X_Ω(q) = 1/λ³` (ergodic-optimization ground value)

`X_Ω(q) = inf_μ ess-sup_μ P` over invariant probability measures, the L∞ support-edge / cluster-onset
value of the gap-product observable on Taha's `G_q`-BCZ section; `λ = λ_q = 2cos(π/q)`.

**What is machine-verified (built and `#print axioms`-audited this session):**

- **Lower bound `X_Ω(q) ≥ 1/λ³`** — axiom-clean, unconditional, for the 17 Hecke indices
  `q ∈ {5,7,8,…,21}`. Engine: the per-q "no-sustained-window" combinatorial fact `Fwindow{4,5,6}`
  discharged by hand-built window files, fed into the lower-bound theorem.
  - `GenuineMapFacts.Xomega_lb_q5to21` (the genuinely unconditional ceiling, no `Fwindow`/`hCorr`
    hypothesis), plus the per-q `Xomega_lb_q5to18` (UniformOnset_q5to18.lean) and
    `Xomega_lb_q19/20/21`.
  - **Honesty caveat:** every lower-bound theorem carries `hlo : 9/5 < l`. For `q=5` (λ₅=φ≈1.618<1.8)
    and `q=6` (λ₆=√3≈1.732<1.8) this hypothesis is FALSE at the real λ, so those instances are
    *vacuous* in the lower-bound engine. First index where `9/5 < λ_q` genuinely holds is `q=7`.

- **Equality `X_Ω(q) = 1/λ³`** — axiom-clean, machine-verified, as a **non-attained infimum over the
  CLOSED-cusp ergodic-optimization class** `Sclosed = Taha ∩ {0 ≤ b}` (same measure class for both
  bounds). The matching upper bound is the cusp-tip Dirac sequence `δ_{(s,0)}`, `s ↓ 1/λ`, an honest
  `Tgen`-invariant probability measure (`Tgen (s,0)=(s,0)` PROVED; `Measurable Tgen` PROVED) with
  `ess-sup Pgen = s²/λ > 1/λ³` strictly for every `s`, descending to `1/λ³`; the realizer sits on the
  excluded boundary `s=1/λ`, so the inf is never attained.
  - General theorem `OnsetEqualityUniform.Xomega_eq_uniform` (cusp active-branch identity discharged
    uniformly for all m≥2 via the sine-arc bound `chebGeLambda_of_hecke` + `branchIdx_cusp_uniform`).
    Per-q corollaries `Xomega_eq_q7 … Xomega_eq_q21`.
  - `q=5` (golden-L / double-pentagon) and `q=6` (arithmetic) were made **non-vacuous** this session
    (GOAL H-1): the `9/5` band is a *packaging artifact of the `Fwindow*` types*, consumed at exactly
    one point (`genuine_no_sustained_6win`) and discardable for q=5,6 because their window cores
    (`g5_no_four_below_genuine`; the q=6 √3 Positivstellensatz core) need only `1<l, l<2, l²≥l+1`.
    Result: `OnsetEqualityLowQ.Xomega_eq_q5_concrete`, `…_q6_concrete`, with λ pinned to
    `2cos(π/5)=φ` / `2cos(π/6)=√3` and all band facts discharged from Mathlib closed forms.
  - **Honest non-vacuous verified equality range: `q ∈ {5,6,7,…,21}` = 17 Hecke indices.**

**Files** (all built, no `sorry`/`admit` in body):
`GenuineClassDischarge.lean`, `OnsetEquality.lean` (q=5 concrete + general),
`OnsetEqualityUniform.lean` (uniform discharge + `Xomega_eq_q7…q21`),
`OnsetEqualityLowQ.lean` (q=5,6 non-vacuous), `UniformOnset_q5to18.lean`, `GenuineMapFacts.lean`.

**The "all-q" caveat (do not overstate).** There is **no** machine-verified unconditional bound for
`q ≥ 22`. `ToplevelStitch.Xomega_lb_allq` is axiom-clean only because its q≥19 content is moved into
an **undischarged hypothesis `hCorr`** (the corridor-survival bridge "`g_corr ≥ 1/λ³ ⟹ ess-sup ≥
1/λ³`"), whose codomain *is* the conclusion; no theorem in the project produces it. The uniform L1b
arc-width inequality `1/λ³ ≤ g_corr(L_blk q, q)` (`L1bArcCoverage.B1_target`, `fcorr_lb`) IS proved
axiom-clean for all `q ≥ 18`, but it does NOT discharge the combinatorial `Fwindow6`; the two engines
are bridged only through `hCorr`. So: fully-discharged content stops at `q = 21`; `q ≥ 22` is
conditional. (Source: `unconditional_range_audit_2026-06-14.md`, `adversarial_biggest_win_…` Front 3.)

**The equality is over the CLOSED section.** The verified lower-bound engine
(`perq_Xomega_lb_qge19_GEN'`) quantifies over the open section `Taha ∩ {0<b}`, which excludes every
cusp tip. The closed-section equality re-proves the lower bound on `Sclosed` by a 2-case split
(reusing the sealed open-section bound, plus `Pgen ≥ 1/λ³` on the cusp line) so that the same class
hosts both bounds. The earlier in-session status "only `≥` is in the verified footprint" is
superseded for q=5..21; over the *open* `{0<b}` section the matching upper bound remains an open
weak-* boundary-approximation question. (Source: `onset_equality_resolution_2026-06-14.md`.)

### A.2 Rotation-arc cluster-ceiling MECHANISM (structural, machine-verified)

The last-branch `k=1` map `M = [[0,1],[−1,λ]]` is an **exact elliptic rotation by −π/q** on the
conserved positive-definite form `E(a,b) = a² − λab + b²` (det 1, tr λ; whitened R(−π/q) to machine
precision dps=50). A sub-threshold cluster is therefore a **rotation arc** on one E-level set; the run
of `k=1` steps is interior, and the run terminates at the first floor increment `k:1→2` (ejection =
floor change kicking the state off the ellipse, not a P-threshold crossing). Hence `B(q)` = number of
π/q-rotation steps the gap-product `P=ab` spends inside the sub-threshold arc `{P<1/λ³}`, plus the
terminal ejecting step. Discrete count matches the genuine-map ground truth `B(q)` for **q=7..40,
34/34** (the continuous closed form `B=⌊w·q/π⌋+1` is only an O(1) / asymptotic proxy — off-by-one at
q=23 — because of an arithmetic resonance; see C). Asymptotic slope ≈ 0.216·q, a *derived* geometric
constant (the prior empirical ~0.22q, now mechanistically explained; the old ~q/3 was a
cross-branch-counter artifact).

**Machine-verified (Lean), parametric in `l ∈ (0,2)`:**
- `BCZHeckeRotationArc.lean` — 18 theorems, the structural reduction (M = elliptic rotation, conserved
  form, arc⇒cluster-ceiling captured by the discrete rotation-arc count), reusing the sealed
  `BCZHeckeNoInfiniteRotation_allq_VERIFIED.lean` (HeckeNoRot) machinery.
- `BCZHeckeRotationArcR1.lean` — **R1 lower bracket** (`k≥1` half of the interior `k=1` confinement)
  proved as a theorem; the upper bracket is the residual (R3/phase-lattice family).
- `BCZHeckeRotationArcR2.lean` — **R2 realization bridge** discharged: an actual genuine sub-threshold
  last-branch arc exhibited, so `clusterCeiling ↔ rotationArcCount` holds with `hrealize` no longer
  assumed. **B(7)=3 fully verified**; B(5)≥3 realized (q=5's first step has k=2).
- `BCZHeckeRotationArcR3Parity.lean` — **R3 PARITY GATE proved** (`resonance_parity_gate`,
  axiom-audited).

The residual to a full closed-form `B(q)` (R1 upper bracket; the exact discrete value / resonance,
R3) is carried as **named hypotheses**, never `sorry`'d. (Source: `Bq_rotation_arc_2026-06-14.md`,
`resonance_threedistance_2026-06-14.md`, `adversarial_biggest_win_…` §C4.)

---

## B. HONEST NEGATIVES this session — do NOT re-chase

The unifying root cause (recurring across all of these): **`1/λ³` is an L∞ support-EDGE / BCZ
cross-section AREA object**, type-mismatched to spectral / Lyapunov / length objects; and
`λ = 2cos(π/q)` is a **serial false-friend** (Jones index, Temperley-Lieb loop, crystallographic
restriction, continued-fraction) with independent origins, so coincidences in `λ` are not bridges.

- **Twin primes via circle / Farey.** The twin-index point set is the *spatial-rigidity rendering of
  the Hardy-Littlewood twin singular series* — i.e. the circle-method MAJOR-arc side. The open core is
  the minor-arc / parity bottleneck, which is unreachable. Twin primes itself: do NOT attempt.
  (`twin_index_hyperuniformity_2026-06-14.md` §B/C below; the HU bridge also fails — see C.)
- **10-direction sweep — all dead:** tight-binding, Lyapunov, Selberg, Rosen-CF Lagrange, max-plus,
  words, Eisenstein, Jones-TL, length-spectrum (D10: `1/λ³ = 8/(systole trace)³` is an *algebraic*
  systole-trace restatement, already in Schmidt-Sheingorn 1995; no length-spectrum LENGTH equality,
  log-bridge provably empty — `D10_length_spectrum_2026-06-14.md`).
- **V1 universal-theta (θ=1/2):** the headline "θ=1/2 because exceedances pair up" is a classical
  textbook EVT identity; the "universal/parameter-independent" framing does not make it new
  (`novelty_V1_theta_evt_2026-06-14.md`).
- **U1/U2 unifying theorems:** the abstract inf-ess-sup identity is a near-triviality, and the
  cusp-geometry edge formula is essentially KNOWN (Athreya-Chaika hard edge; KSW/Taha uniform section;
  edge = ess-inf of the return/roof function) — `novelty_U1_parabolic_EO_…`, `novelty_U2_cusp_edge_…`.
- **Veech slope-gap bridge:** the BCZ gap-product cross-section and the H_q-Veech-surface slope-gap
  section are P,R-reciprocal, not the same object — bridge DROPPED (`Xomega_generalize_2026-06-14.md`).
- **Arithmeticity detector (beyond triangle groups):** "B=2 ⟺ arithmetic" is Takeuchi 1977 +
  crystallographic restriction rebadged; the integer-cancellation mechanism is the special
  (degree-2, totally-real) case of known Luo-Sarnak / Geninska-Leuzinger theory. DROP as a new local
  criterion (`trackB_local_arithmeticity_2026-06-14.md`).
- **Equality upper bound via an interior orbit:** honest NEGATIVE — the minimizer is the boundary
  cusp-tip Dirac, not an interior measure; no interior realizer exists
  (`equality_upperbound_…`, `adversarial_biggest_win_…` Front 1).
- **Reciprocity-obstruction / χ4 scans:** principled NEGATIVE, structurally explained
  (`chi4_reciprocity_…`, `reciprocity_scan_…`).

Adversarial audit of the "biggest win" (`adversarial_biggest_win_2026-06-14.md`) confirms: the
qualitative hard-edge result is OLD (golden-L q=5 published 2013, 2n-gon family 2021, uniform Veech
method 2021); the *defensible* novelty is narrow — the specific uniform value `1/λ³` with an
elementary no-sustained-window + ejection + arc-width proof, and (to our knowledge a first) a
machine-verified, axiom-clean lower bound for 17 Hecke indices.

---

## C. GENUINE MODEST RESIDUE / OPEN

- **θ = 1/2 extremal index (H-2).** Derived EXACTLY via a coordinate-universal period-2 cusp-swap
  involution ⇒ mean cluster size 2 ⇒ θ = 1/E[L] = 1/2, q-independent; confirmed at q=4,5,7. The
  `θ = 1/E[L]` obstruction is CLOSED. **Blocked only on the BCZ MIXING RATE:** measured polynomial
  decay of correlations `C(n) ~ n^{−β}`, β ≈ 0.9 (near 1/n), with first-return tail
  `P(R>n) ~ n^{−β_R}`, β_R ≈ 1.7–2.1 (estimator validated on doubling / Pomeau-Manneville / Gauss
  controls). A *rigorous* rate is a major open problem (parabolic cusp, no off-the-shelf Young tower;
  the project's 1-D transfer-operator engine is the wrong object for the 2-D parabolic
  area-preserving section). Verdict: (b) proved-modulo-a-named-limit-theorem.
  (`theta_half_repp_…`, `bcz_mixing_rate_…`.)
- **Cluster-ceiling resonance is PARITY-gated.** Where discrete B(q) exceeds the continuous arc count
  is decided by **parity of the arc count B₀(q)** (a notch-hop gains +1 only when B₀ is odd), NOT by
  any inhomogeneous-Diophantine / three-distance condition (REFUTED — the corridor rotation number is
  the *rational* 1/(2q), a single-gap lattice, too degenerate for three-gap structure). Resonant set
  is rare/isolated: `{23, 61, …}` (q=61 predicted and verified dps=50), NOT the dense set from the
  superseded buggy proxy. Residual: the resonance *location* is a transcendental near-integer window
  (W(q) near an odd integer) — one L1b-family near-fit, no closed arithmetic form; parity rule proved
  structurally + exact (dps=50), not yet Lean. (`resonance_threedistance_…`, `novelty_B1_…`.)
- **Uniform all-q onset:** OPEN. q≥22 conditional on the undischarged corridor bridge `hCorr` (A.1).
- **Twin-index hyperuniformity:** the twin-index set is **Poisson-class** (σ²(R)~R, α≈0), a *weaker*
  class than the prime-Farey critical hyperuniformity S(k)~k^1.8 — the HU bridge fails. A clean
  presentation of the HL singular series in HU language, not a twin-primes advance.
  (`twin_index_hyperuniformity_…`.)

---

## D. STRATEGIC

This session is consistent with the standing **pipeline-pivot verdict** (MEMORY 2026-06-14): there is
**no honest broad-reach solo new-math target** for this pipeline — where the edge is real it is niche
and owned; where the reach is broad the analytic core is unreachable. The same niche-trap reappeared
in every novelty audit above (X_Ω(Γ) is a trace-field-bound normalization artifact, not a new
invariant; the arithmeticity detector is Takeuchi rebadged; the bridges are P,R-reciprocal or
type-mismatched).

The durable value is therefore **(1)** the machine-verified results — the axiom-clean
`X_Ω(q) = 1/λ³` equality for q=5..21 and the rotation-arc mechanism (R1 lower / R2 realization / R3
parity gate) — and **(2)** the methods + falsification discipline (autonomous scout → adversarial
falsification gate that kills false positives before the prover → Lean/Aristotle machine-verification
over certified numerics, with NEGATIVE results recorded as first-class output;
`PIPELINE_methodology_2026-06-14.md`).

The remaining open analytic pieces are exactly the natural **THEORY-COLLABORATOR (Koyama) targets**,
not solo pursuits: the **BCZ mixing rate** (gates rigorous θ=1/2 and most BCZ limit theorems), the
**uniform all-q onset** (the q≥22 corridor-survival bridge `hCorr`), and **geodesic-section
arithmeticity** for general Fuchsian groups.

---

### File index (cited above)

Lean (built this session, axiom-clean, no `sorry`/`admit`), under
`projects/aristotle_dispatch_v15/uniform_q5to18/`:
`GenuineClassDischarge.lean`, `OnsetEquality.lean`, `OnsetEqualityUniform.lean`,
`OnsetEqualityLowQ.lean`, `UniformOnset_q5to18.lean`, `GenuineMapFacts.lean`,
`L1bArcCoverage.lean`, `BCZHeckeRotationArc.lean`, `BCZHeckeRotationArcR1.lean`,
`BCZHeckeRotationArcR2.lean`, `BCZHeckeRotationArcR3Parity.lean`.
Top-level (conditional q≥22): `ToplevelStitch.lean` (`Xomega_lb_allq` via undischarged `hCorr`).

Research notes (all `research_notes/…2026-06-14.md`):
`onset_equality_resolution`, `unconditional_range_audit`, `onset_equality_q5q6`,
`adversarial_biggest_win`, `Bq_rotation_arc`, `resonance_threedistance`, `theta_half_repp`,
`bcz_mixing_rate`, `twin_index_hyperuniformity`, `D10_length_spectrum`, `equality_upperbound`,
`Xomega_generalize`, `trackB_local_arithmeticity`, `chi4_reciprocity`, `reciprocity_scan`,
`novelty_U1_parabolic_EO`, `novelty_U2_cusp_edge`, `novelty_V1_theta_evt`, `novelty_V1_theta_homdyn`,
`novelty_B1_threegap_rotation`, `pipeline_target_verdict`, `PIPELINE_methodology`.
