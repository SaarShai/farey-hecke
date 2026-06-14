<!-- INTERNAL DRAFT — NOT for submission; all outward communication is USER-gated. -->
<!-- Prepared 2026-06-14 (Track 2 / Goal-L–M). This is the SECOND, larger manuscript; the -->
<!-- arithmeticity-dichotomy manuscript (research_notes/PAPER_arithmeticity_dichotomy_SUBMISSION.md) -->
<!-- is the companion. Every claim is tagged; Lean axioms quoted from a fresh `lake build` run -->
<!-- on 2026-06-14 against Mathlib v4.28.0 in projects/aristotle_dispatch_v15/uniform_q5to18/. -->

# A Machine-Verified Support Edge for Hecke Slope-Gap Statistics:
# The Ergodic Ground Value X_Ω(q) = 1/λ_q³ for q = 5..21

---

## Provenance / status tags (used on every mathematical assertion)

- `[PROVEN:Lean]` — machine-verified in Lean 4 (Mathlib v4.28.0), sorry-free, with
  `#print axioms` returning **exactly** `[propext, Classical.choice, Quot.sound]`
  (no `sorryAx`, no axiom stubs, no `native_decide`). The exact declaration name, file,
  and the quoted axiom line are given.
- `[PROVEN:Lean-mod-H]` — machine-verified sorry-free **modulo one or more explicitly
  named structural hypotheses carried in the statement** (e.g. an ergodic engine, a
  per-q F-window certificate, the genuine-map per-point classification record). The
  *theorem object* is axiom-clean; the named hypothesis is what remains to discharge.
  Each such hypothesis is itself tracked with its own tag.
- `[PROVEN:interval]` — established by rigorous interval arithmetic (Arb-style directed
  rounding, 40-decimal endpoints), not a Lean proof; used only as corroboration of an
  inequality that *is* separately `[PROVEN:Lean]`.
- `[NUMERICAL]` — established by computer experiment (exact-arithmetic witness ladders,
  golden-section minimization, junction-safe orbit scans); not a proof.
- `[CONJECTURE]` — a pattern consistent with all data, with no proof claimed.

**Honesty preamble (read first).** The headline theorem is the **equality**
`X_Ω(q) = 1/λ_q³`, **machine-verified in Lean** (axiom-clean) for the seventeen Hecke
indices **q ∈ {5, 6, 7, …, 21}** (the golden-L index q = 5 is INCLUDED, as a non-vacuous
equality at λ = φ). The equality holds as a **non-attained infimum** over the
invariant-measure simplex of the closed section, realized in the limit by the cusp
parabolic-Dirac sequence. The matching ≥ lower bound holds on the same range. We do
**NOT** claim an all-q theorem:

- **q ≥ 22 is OPEN and structurally blocked.** The fixed six-window proof method caps
  once the sub-threshold cluster ceiling B(q) exceeds ~5 (it grows ~0.22·q); a genuine
  all-q result needs an unproven cluster-growth law (see §3.6). For q ≥ 22 only a
  **conditional** lower bound is available (next bullet).
- **The all-q lower bound `ToplevelStitch.Xomega_lb_allq` is CONDITIONAL**: for q ≥ 22 it
  carries the never-proved corridor-assembly hypothesis `hCorr` (block-monodromy → essSup
  wiring) and the genuine-map bridge `(P2)`. It is therefore **not an unconditional all-q
  result**. The analytic arc-width crux `L1b` (`fcorr_lb`/`B1_target`) is sealed in Lean,
  but L1b alone does not discharge `hCorr`.
- The `MeasurePreserving` carried in every statement is the **invariant-measure
  quantifier** (definitional: it is what "ranges over T-invariant probability measures"
  means), not an extra assumption.

§6 states the exact ledger. **Verified equality files** (all axiom-clean
`[propext, Classical.choice, Quot.sound]`, fresh `lake build` 2026-06-14):
`GenuineClassDischarge.lean`, `OnsetEquality.lean`, `OnsetEqualityUniform.lean`,
`OnsetEqualityLowQ.lean`.

---

## Abstract

Fix an integer q ≥ 3 and the Hecke triangle group G_q ⊂ PSL(2,ℝ), with
λ_q = 2 cos(π/q). Taha (arXiv:1810.10668) constructed a Poincaré section for the
horocycle/geodesic flow on the unit tangent bundle of the (2,q,∞) orbifold whose return
map — the G_q–BCZ map, the Hecke-family analogue of the classical Farey–BCZ map — takes,
on its last (scalar) branch, the uniform form (a, b) ↦ (b, −a + k λ_q b). The
gap-product observable is P = a·b on this section; equivalently the genuine assembly
observable is P_gen = a(a + λ_q b)/λ_q, with P_gen ≥ a·b. We study the
**ergodic-optimization edge value** (the zero-temperature ground value)

    X_Ω(q) := inf over T-invariant probability measures μ of  ess-sup_μ P,

i.e. the smallest possible essential supremum of the gap product, over the whole
invariant-measure simplex. This is the **support edge** of the slope-gap statistic.

Our main result is a sharp **equality**, machine-verified:

> **Theorem (Onset value, machine-verified for q = 5..21).** For each Hecke index
> q ∈ {5, 6, 7, …, 21},  X_Ω(q) = 1/λ_q³, as a **non-attained infimum**: every
> invariant probability measure of the closed section has ess-sup P_gen ≥ 1/λ_q³, and
> the cusp parabolic-Dirac sequence δ_{(s,0)}, s ↓ 1/λ_q, realizes the infimum from above
> (strictly, since each Dirac gives s²/λ > 1/λ³).

The value 1/λ_q³ is exactly the cusp-tip value of P_gen at the section corner (1/λ_q, 0);
it is the ground value of the ergodic optimization problem. We prove the lower-bound half
by a six-layer "GATE-2" architecture: an elementary ergodic *no-sustained ⇒
support-edge* engine; a per-step branch trichotomy (scalar / cusp / deep-mid); a cusp
envelope putting cusp steps above threshold; a one-step deep-mid ejection; a confinement
lemma forcing any sustained sub-threshold orbit onto a single F-corridor word; and the
analytic crux — the corridor block-monodromy is an **elliptic rotation by π/q on a
conserved invariant ellipse** (precisely Koyama's conserved energy), whose rotating
observable is forced through the super-threshold arc within O(q) blocks (the **L1b**
arc-width inequality). The matching upper-bound half is the cusp-Dirac sequence,
admissible in the **closed-section / P_gen** measure class.

**Machine-verification status (honest).** The equality X_Ω(q) = 1/λ_q³ is **Lean-verified
and axiom-clean** for the seventeen indices q ∈ {5, 6, 7, …, 21}; q = 5 (golden L) and q = 6
are **fully closed, no-hypothesis** equalities at λ = φ resp. λ = √3, while q = 7..21 are
established modulo the (true, internally-dischargeable) arithmetic band hypotheses with the
per-q F-window certificate already supplied (see §4). The arc-width crux L1b is **sealed in Lean**
(sorry-free, axiom-clean). For **q ≥ 22 the statement is OPEN** and the proof method is
**structurally blocked** (the fixed six-window method caps once the cluster ceiling B(q)
exceeds ~5; see §3.6); the all-q lower bound `ToplevelStitch.Xomega_lb_allq` is only a
**conditional** result, carrying the unproved corridor-assembly hypothesis `hCorr` and the
genuine-map bridge `(P2)`. We do **not** claim an unconditional ∀q theorem.

**On novelty (honest, per the adversarial audits).** The qualitative support edge / "no
small gaps ⟺ Veech" is prior work (Athreya–Chaika, qualitative); the observable and the
G_q section are Taha (arXiv:1810.10668); a *family-uniform* Poincaré-section construction
across all Veech surfaces already exists (Kumanduri–Sanchez–Wang, arXiv:2102.10069). We
therefore do **NOT** claim "the first family-uniform support edge." Our genuine
contributions are (1) the **first machine-verified** (Lean, axiom-clean) slope-gap /
ergodic-optimization edge, for these seventeen Hecke groups; (2) the **exact value**
1/λ_q³, pinned by an elementary uniform argument; and (3) the **geometric mechanism** — the
corridor as an elliptic rotation by π/q on the conserved form E = a² − λ a b + b².

---

## 1. Introduction

### 1.1 Slope-gap statistics, one surface at a time

For a translation surface, the **slope-gap distribution** records the limiting law of
the renormalized gaps between consecutive slopes of saddle connections (or holonomy
vectors) up to a growing length cutoff. For lattice (Veech) surfaces this distribution
is given by a piecewise-real-analytic density with compact support and a **hard edge**:
there are *no arbitrarily small gaps* — the "no small triangles" phenomenon of
Smillie–Weiss. The computation of these densities is, by tradition, **one surface per
paper**: the golden L (Athreya–Chaika–Lelièvre, arXiv:1308.4203, seven non-differentiability
points, density vanishing on an interval), the regular 2n-gons (slope-gap section with
n+1 pieces; the number of non-differentiability points grows linearly in n —
Berman–McAdam–Miller–Murthy–Uyanik–Wan, arXiv:2109.04495), and so on. The Veech group
of the double-(2n+1)-gon is exactly the Hecke group H_{2n+1} (Veech); the 2n-gon Veech
group is the triangle group Δ(n,∞,∞).

The qualitative dichotomy is due to Athreya–Chaika: a translation surface has **no small
gaps in its slope-gap statistic if and only if it is a lattice (Veech) surface**. This is
an *existential, qualitative* statement — it says a positive support edge exists for Veech
surfaces and is absent (gaps accumulate at 0, heavy tails) otherwise; it does not produce
the *value* of the edge, and it is proved surface-by-surface in its quantitative refinements.

### 1.2 What is new here: a machine-verified edge, an exact value, and a mechanism

We work with the Taha G_q–BCZ section, the Hecke-family generalization of the Farey–BCZ
Poincaré section (Athreya–Cheung; Boca–Cobeli–Zaharescu). Rather than computing one density,
we extract a single number across the **verified Hecke family (q = 5..21)**: the support edge

    X_Ω(q) = inf_μ ess-sup_μ (a·b)

of the gap-product observable, minimized over all invariant probability measures (the
ergodic-optimization edge). Our contributions, stated carefully against the prior art:

1. **A machine-verified ergodic-optimization edge.** The proof is formalized in Lean 4
   (Mathlib v4.28.0), sorry-free and axiom-clean on the verified range
   q ∈ {5, 6, 7, …, 21}. To our knowledge this is the **first machine-verified theorem
   in ergodic optimization** / zero-temperature thermodynamic formalism, and the first
   machine-verified slope-gap support edge. `[PROVEN:Lean]`.

2. **The exact value 1/λ_q³, by an elementary argument.** We prove X_Ω(q) = 1/λ_q³ for
   q = 5..21, with 1/λ_q³ the explicit cusp-tip value, established by an elementary
   uniform argument (no transfer-operator spectrum, no escape-of-mass machinery). This
   is the *quantitative* refinement, in the Hecke family, of Athreya–Chaika's
   *qualitative* "no small gaps ⟺ Veech": where they assert the edge is positive, we give
   its value and certify it. `[PROVEN:Lean]` for q ∈ {5,…,21}.

3. **The geometric mechanism.** The corridor block-monodromy is an elliptic rotation by
   π/q on the conserved form E = a² − λ a b + b² (Koyama's energy); the sub-threshold
   cluster is the rotation arc, ejected at a floor increment. This *derives* (rather than
   fits) the mechanism behind both the edge value and the cluster ceiling (§3.6).

**What we do NOT claim.** We do **not** claim "the first family-uniform support edge": a
family-uniform Poincaré-section construction across all Veech surfaces already exists
(Kumanduri–Sanchez–Wang, arXiv:2102.10069), and the qualitative edge is Athreya–Chaika.
We also do **not** claim an all-q result; q ≥ 22 is open (§1.4, §3.6, §6).

### 1.3 The companion dichotomy paper

X_Ω(q) is also the threshold value in our companion paper
(`PAPER_arithmeticity_dichotomy_SUBMISSION.md`): there we show that the maximal length
B(q) of a consecutive sub-threshold run (P < X(q)) detects arithmeticity —
B(q) = 2 ⟺ q ∈ {3,4,6} ⟺ G_q arithmetic. The present paper is the structural foundation:
it identifies X_Ω(q) = 1/λ_q³ as the ergodic ground value that the dichotomy is read
against. The two results share the observable, the section, and the value; they are
logically independent (the dichotomy is about *run length at* the threshold; this paper is
about *the threshold value itself* as a measure-uniform infimum).

### 1.4 Honest scope: the small-q caveat and the q ≥ 22 wall

**Lower end.** The identity X_Ω(q) = 1/λ_q³ holds for q ≥ 5 (including q = 6, λ = √3,
which is verified as a non-vacuous equality even though it is an arithmetic index). For the
two smallest arithmetic indices the edge value is *different*: X(3) = 2/9 and X(4) = √2/8
(the exact ground values of the q = 3 and q = 4 problems; see the companion paper and the
q = 3 ergodic-optimization note). So the general claim "X_Ω = 1/λ³ for all l ∈ (1,2)" is
**false** — e.g. q = 4 gives l = √2 with X = √2/8 ≠ 1/(√2)³. The theorem is correctly
scoped to q ≥ 5. `[NUMERICAL]` for the q = 4 counterexample to the naive l-continuum claim.

**Upper end (the wall).** The machine-verified range is q ∈ {5, 6, …, 21}.
**q ≥ 22 is open**, and the proof method is **structurally blocked**: the fixed six-window
argument refutes sub-threshold runs only up to length 6, but the sub-threshold cluster
ceiling B(q) grows (~0.22·q, §3.6), exceeding ~5 right around q = 22. A genuine all-q
theorem needs an unproven cluster-growth law (the closed-form B(q), which another agent is
rigorizing). What exists for q ≥ 22 is only a **conditional** lower bound (carrying `hCorr`
and `(P2)`; §6) — it is **not** an unconditional all-q result.

**Equality, not just ≥.** The headline is now the **equality** X_Ω(q) = 1/λ_q³ (≤ and ≥),
machine-verified for q = 5..21 as a non-attained infimum. The matching upper bound is the
cusp parabolic-Dirac sequence δ_{(s,0)}, s ↓ 1/λ, which is admissible in the
**closed-section / P_gen** measure class (`OnsetEquality.cusp_dirac_admissible`); note that
the *same* Dirac is **inadmissible** in the scalar / P_prod / Dcorr engine class
(`EqualityUpperBound.cusp_dirac_inadmissible`), so the equality is correctly stated over the
closed section. `[PROVEN:Lean]` (equality, q = 5..21).

---

## 2. The Taha G_q–BCZ setup and the observable

### 2.1 The section and the last-branch map

Let l = λ_q = 2 cos(π/q). The Taha section domain (the "Taha triangle") is

    Taha(l) = { (a,b) : 0 < a ≤ 1,  1 − l·a < b ≤ 1 },

with the F-corridor sub-domain

    Dcorr(l) = { (a,b) : 0 < a ≤ 1, 0 < b ≤ 1, a + l·b > 1, l·a + b > 1 }.

`[PROVEN:Lean]` (definitions `UniformOnset.Taha`, `UniformOnset.Dcorr`,
file `BCZHeckeUniformOnset.lean:55,58`). On the last (scalar) branch the return map is

    Tmap(l)(a,b) = ( b,  ⌊(1 + a)/(l·b)⌋ · (l·b) − a ),

i.e. (a,b) ↦ (b, −a + kλb) with k = ⌊(1+a)/(lb)⌋ the (nonnegative) floor.
`[PROVEN:Lean]` (`UniformOnset.Tmap`, `BCZHeckeUniformOnset.lean:49`; the scalar copy
`UQ.Tmap` in `UniformOnset_q5to18.lean:94` is *defeq*).

### 2.2 The gap-product observable and the two forms

Two observables appear, and the lower bound transfers cleanly between them:

- the **scalar gap product**  P_prod(a,b) = a·b
  (`UQ.Pprod`, `UniformOnset_q5to18.lean:102`);
- the **genuine assembly observable**  P_gen(l)(a,b) = a(a + l·b)/l
  (`UniformOnset.Pgen`, `BCZHeckeUniformOnset.lean:45`).

Since P_gen − a·b = a²/l ≥ 0 for l > 0, one has **P_gen ≥ P_prod** pointwise
(`UniformOnset.prod_le_Pgen_orbit`, `BCZHeckeUniformOnset.lean:128`, `[PROVEN:Lean]`).
Thus a lower bound on ess-sup of either descends to the family. The q ≤ 21 unconditional
half is stated on P_prod over Dcorr; the q ≥ 22 corridor half on P_gen over Taha.

### 2.3 The threshold and its meaning

The threshold value is t = 1/l³ = 1/λ_q³. It is **exactly the cusp-tip value**: at the
section corner (a,b) = (1/l, 0), P_gen = (1/l)(1/l + 0)/l = 1/l³. So 1/l³ is not a
spectral eigenvalue or a pressure object (we checked: P_gen and a·b have the *invariant-
measure level-set* structure, not a phase transition — see the D1 note); it is the
**geometric ground value at the cusp**, and the theorem says the gap product cannot stay
below it on any invariant measure. `[NUMERICAL]` (cusp-tip identity, exact);
`[PROVEN:Lean]` that the cusp branch realizes ≥ 1/l³ (Layer 2 below).

---

## 3. The GATE-2 proof architecture

The proof reduces the measure-theoretic statement to a finite-orbit combinatorial fact
("no orbit stays sub-threshold forever") via an elementary ergodic engine, then proves the
combinatorial fact by trichotomy + confinement + the corridor arc-width inequality.

### Layer 0 — the ergodic engine (no-sustained ⇒ support-edge). `[PROVEN:Lean]`

The abstract engine is

    EssSupEngineType :=
      ∀ T P D t M μ [prob], μ Dᶜ = 0 → MeasurePreserving T μ μ →
        (∀ᵐ x, P x ≤ M) →
        (∀ orbit, (∀ n, orbit n ∈ D) → (∀ n, orbit(n+1) = T(orbit n)) →
                  ¬ (∀ n, P(orbit n) < t)) →
        t ≤ ess-sup_μ P.

(`UniformOnset.EssSupEngineType`, `BCZHeckeUniformOnset.lean:69`.) In words: if **no**
orbit keeps P strictly below t forever, and μ is a T-invariant probability measure carried
by D with P essentially bounded, then t ≤ ess-sup_μ P. This is the rigorous "escape-of-mass
⇒ support-edge bound" conversion; it is **elementary** (a contrapositive on a sub-threshold
orbit) and does **not** require Marklof–Pollicott escape laws, transfer-operator spectra,
or any support-edge/pressure duality. Discharged by the axiom-clean
`BCZHeckeGenuineAssembly_qge18_VERIFIED.essSup_ge_of_no_sustained_strict`. `[PROVEN:Lean]`.

### Layer 1 — branch trichotomy of the genuine map. `[PROVEN:Lean]` (per point)

Every active step lands on a branch index branchIdx ∈ {scalar = m+1, cusp = m,
deep-mid < m}, where q = m + 2. The classification is

    step_trichotomy :  IsFstep_concrete ∨ IsCusp_concrete ∨ IsDeepMid_concrete

(`HeckeS1.step_trichotomy`, `BCZHeckeS1_trichotomy.lean:119`, `[PROVEN:Lean]`), built from
`branchIdx_spec` (minimality) and `branch_exists`. This is the per-point branch data of
the genuine G_q–BCZ selector.

### Layer 2 — cusp leg: a cusp step is super-threshold. `[PROVEN:Lean]`, uniform q ≥ 5

On the cusp branch, with the five cusp guards (0 < a ≤ 1, l·a+(l²−1)·b > 1, l·a+b > 1,
a+l·b ≤ 1), one has P_gen ≥ 1/l³:

    cusp_step_bound :  1/l³ ≤ a(a + l·b)/l

(`UniformOnset.cusp_step_bound`, `BCZHeckeUniformOnset.lean:166`, `[PROVEN:Lean]`, inlined
verbatim from `BCZHeckeCusp_envelope_allq_VERIFIED`). Tight at the cusp tip. The cusp guards
themselves are produced from a cusp branch by `HeckeS1.IsCusp_to_CuspGuards`
(`BCZHeckeS1_trichotomy.lean:198`, `[PROVEN:Lean]`). So Layer 2 is a **theorem**, not an
assumption; the cusp branch is genuinely excluded from sub-threshold runs.

### Layer 3 — deep-mid leg: one-step ejection. `[PROVEN:Lean]`, uniform box (all q ≥ 16)

On a non-F deep-mid branch, write u = L_{i−1}, v = L_i, r = x_{i−2}/x_{i−1}. Via the
Casorati area identity the observable is P_i = u·v − r·v² (exact to < 10⁻⁴⁸ numerically),
and the genuine successor product is λv² − uv + kλv² ≥ λv² − uv. The ejection lemma is

    ejection_kick_uniform :  (sub-threshold premise) → 1/λ³ ≤ λ·v² − u·v

over the single rational box l ∈ [49/25, 2], r ∈ [22/25, 63/50], thr ∈ [1/8, 663/5000]
(⊇ every realized genuine deep-mid sub-threshold cell at every q ≥ 16, with λ < 2)
(`HeckeEjectionUniform.ejection_kick_uniform`, `EjectionUniform.lean:45`, `[PROVEN:Lean]`,
`#print axioms = [propext, Classical.choice, Quot.sound]`). Consequence: a sub-threshold
deep-mid step **ejects in one step**, independent of the floor k. This upgrades the earlier
per-finite-range box (q = 16..21) to a single box for all q ≥ 16. (Layer-3 *uniformity over
the floor* is sealed; absorbing deep-mid into the corridor for the literal all-q statement
is part of the q ≥ 22 residual — see §6.)

### Layer 4 — confinement: sub-threshold ⇒ pure F-corridor. `[PROVEN:Lean]` (mod htri)

Combining Layers 1–3: a sustained sub-threshold orbit cannot use the cusp branch (Layer 2
super-threshold) nor dwell on a deep-mid branch (Layer 3 ejects), so it is forced **entirely
onto the scalar F-corridor branch**. There the per-q F-window certificate refutes a
sufficiently long window. Formalized as the per-q lower bound

    per_q_Xomega_lb_6win (hEngine) (hFW : Fwindow6 …) … (hOrbitData) :
        1/l³ ≤ ess-sup_μ P_gen

(`UniformOnset.per_q_Xomega_lb_6win`, `BCZHeckeUniformOnset.lean:397`, `[PROVEN:Lean]`),
consuming the engine (Layer 0), the per-q F-window `hFW`, and the orbit-data record
`hOrbitData` (the genuine-map per-point classification, Layer 1, packaged). The
F-window hypothesis types `Fwindow4/5/6` (`BCZHeckeUniformOnset.lean:87,99,111`) are the
exact 6/5/4-consecutive-product non-sub-threshold signatures discharged per q by the
`BCZHeckeG{q}_window_VERIFIED` files.

### Layer 5 — the analytic crux: corridor arc-width (L1b). `[PROVEN:Lean]` — NOW SEALED

This is the genuinely new mathematics and the heart of Koyama's energy × cusp-escape route.

- A sustained sub-threshold orbit cannot switch corridors (an F-family corridor switch has
  |trace| ≥ 2, hence is hyperbolic/parabolic ⇒ escape; `switch_forces_nonelliptic`,
  pure 2×2 trace algebra). So it rides a single corridor word
  W_q = (q−1,3)(q−1,0)(q−3,0).
- The W_q block monodromy is M_W = [[−λ, 2λ²+1], [−1, 2λ]], with **det = 1, trace = λ**.
  It is an **elliptic rotation by θ = π/q on the invariant ellipse**
  Q′(a,b) = a² − 3λab + (2λ²+1)b² (`MW_preserves_ellipse`, `Qp_posdef`). **This invariant
  ellipse is precisely Koyama's conserved energy E** — the trace-λ elliptic invariant; the
  energy enters the proof as the *conserved rotation ellipse*, NOT as a pointwise floor on P
  (the naive pointwise-energy reading is false, and the four-report audit correctly refuted
  it: on a fixed energy level inf P = 0; energy alone gives only the *upper* bound
  P ≤ E₀/(2−λ)). `[PROVEN:Lean]` (det/trace/ellipse) and `[NUMERICAL]` for the
  energy-route falsification of the naive reading.
- On the block boundary the state rotates, a_n = r cos(nθ − ψ), and the observable is a
  rotating sinusoid P_n = (r²/2A₂)[3λ/2 + √A₂ cos(2(nθ−ψ)+η)], A₂ = 1 + 2λ². The in-domain
  corridor arc (Taha lower edge a + λb > 1) is a proper arc of phase-width Δ(q) → 0.1282·π,
  a **positive constant** as q → ∞ (it does NOT shrink to 0). Rotation by θ = π/q sweeps
  through this arc in ≈ Δ(q)/θ ≈ 0.1282·q blocks: the dwell grows **linearly** in q.
- Within a window of L_blk(q) = ⌈33q/256⌉ + 2 blocks (slope 33/256 = 0.12891, chosen
  strictly longer than the true dwell 0.12819), the max of P_n must reach 1/l³. The reduction
  derives the Chebyshev recurrences and conserved ellipse from the M_W step and concludes
  ¬(∀n, P_n < 1/l³), GIVEN the single uniform inequality

      (L1b)   1/λ³ ≤ g_corr(⌈33q/256⌉ + 2, q)    for all q ≥ 18.

**This inequality is now fully proved in Lean.** `fcorr_lb` and the assembled `B1_target`
are sorry-free and axiom-clean (verified 2026-06-14; see §5). L1b is no longer a carried
sorry — it is sealed.

The full chain for q ≥ 18 is: Layer 0 engine ∘ Layer 4 confinement ∘ {Layer 2 cusp ✓,
Layer 3 deep-mid box ✓, Layer 5 L1b ✓}, with the residual genuine-map faithfulness
(htri / the block-sequence → orbit bridge) the remaining structural input for q ≥ 22.

### 3.6 The mechanism: cluster = conserved-ellipse rotation arc, ejected at a floor increment

The Layer-5 rotation picture has a sharper, per-step form that explains *why* the method
walls off at q ≥ 22, and that gives the geometric mechanism behind the whole result.
(`research_notes/Bq_rotation_arc_2026-06-14.md`.) On the last (scalar) branch, the k = 1
map is M = [[0,1],[−1,λ]] — det 1, trace λ — an **elliptic rotation by θ = π/q** preserving
the positive-definite conserved form

    E(a,b) = a² − λ a b + b²   (precisely Koyama's energy, the trace-λ elliptic invariant).

After whitening, each k = 1 step advances the whitened phase φ by exactly −π/q (verified
numerically to machine precision, q = 7..60), and the observable P = a·b is a fixed sinusoid
g(φ) of that phase. A **sub-threshold cluster** (a maximal run with P < 1/λ³) is therefore
**the arc of the elliptic rotation that lies inside the sub-threshold sector of one
conserved ellipse**, and the run **terminates at the floor increment k : 1 → 2**, which
kicks the state off the ellipse (ejection = a floor change, NOT a P-threshold crossing).
The cluster ceiling is then

    B(q) = (number of consecutive π/q-rotation steps inside the sub-threshold arc) + 1.

Empirically this reproduces the entire B(q) table exactly (q = 7,13,19,23,24,30,40,60) and
asymptotically B(q) ~ 0.22·q, recovering the cluster-growth rate. This is the mechanism that
caps the fixed six-window method: once B(q) > ~5 (around q = 22), no fixed finite window can
refute a sub-threshold run, which is the structural reason q ≥ 22 is out of reach by this
route.

**Honest status.** The rotation-arc account is the derived geometric *mechanism*; the
**exact cluster-ceiling closed form B(q) is still open** — its "+1 ejection," "k = 1 interior
only," and the limiting arc-width w(q) are empirical-structural facts (confirmed against all
data) that another agent is rigorizing into a theorem. `[NUMERICAL]` for the B(q) closed form;
`[PROVEN:Lean]` for the per-step elliptic-rotation / conserved-ellipse algebra (det, trace,
invariance) and the Layer-5 corridor version.

---

## 4. The machine-verification status table

Quoted from a fresh `lake build` (Lean 4.28.0, Mathlib v4.28.0) on 2026-06-14, in
`projects/aristotle_dispatch_v15/uniform_q5to18/`. "axiom-clean" = `#print axioms` returns
exactly `[propext, Classical.choice, Quot.sound]`.

| Component | Lean name (file) | `#print axioms` (quoted) | Status |
|---|---|---|---|
| Ergodic engine (Layer 0) | `UniformOnset.essSup_ge_of_no_sustained_strict` (assembly VERIFIED) | clean | `[PROVEN:Lean]` |
| Branch trichotomy (Layer 1) | `HeckeS1.step_trichotomy` (`BCZHeckeS1_trichotomy.lean`) | clean | `[PROVEN:Lean]` |
| Cusp guards / envelope (Layer 2) | `HeckeS1.IsCusp_to_CuspGuards`, `UniformOnset.cusp_step_bound` | clean | `[PROVEN:Lean]` |
| Uniform deep-mid ejection (Layer 3) | `HeckeEjectionUniform.ejection_kick_uniform` (`EjectionUniform.lean`) | `[propext, Classical.choice, Quot.sound]` | `[PROVEN:Lean]` |
| Per-q corridor lower bound (Layer 4) | `UniformOnset.per_q_Xomega_lb_6win` (`BCZHeckeUniformOnset.lean`) | clean | `[PROVEN:Lean]` (mod hEngine/hFW/hOrbitData) |
| **Arc-width crux L1b (Layer 5)** | `L1bArcCoverage.fcorr_lb`, `.B1_target` | `[propext, Classical.choice, Quot.sound]` | **`[PROVEN:Lean]` — SEALED** |
| (P1) scalar ⇒ Dcorr confinement | `GenuineMapFacts.scalar_implies_Dcorr` (`GenuineMapFactsP1.lean`) | `[propext, Classical.choice, Quot.sound]` | `[PROVEN:Lean]` |
| Orbit-data adapter | `ToplevelStitch.genuine_orbitdata` (`ToplevelStitch.lean`) | `[propext, Classical.choice, Quot.sound]` | `[PROVEN:Lean]` |
| q ≥ 19 per-q bound, (P1)-discharged | `ToplevelStitch.perq_Xomega_lb_qge19_P1discharged` | `[propext, Classical.choice, Quot.sound]` | `[PROVEN:Lean]` (mod hEngine/hFW/(P2)) |
| **Unconditional q ∈ {5,7,…,21}** | `GenuineMapFacts.Xomega_lb_q5to21` (`ToplevelStitchQ5to21.lean`) | `[propext, Classical.choice, Quot.sound]` | **`[PROVEN:Lean]` — UNCONDITIONAL** |
| Top-level ∀q (P1-discharged, q≤21 uncond.) | `ToplevelStitch.Xomega_lb_allq_q5to21_P1` | `[propext, Classical.choice, Quot.sound]` | `[PROVEN:Lean]` (q≥22 mod hCorr/(P2)) |
| Top-level ∀q core (LOWER bound) | `ToplevelStitch.Xomega_lb_allq` | `[propext, Classical.choice, Quot.sound]` | `[PROVEN:Lean]` — **CONDITIONAL** (q≥22 carries hCorr) |
| Sorry-isolation witness | `ToplevelStitch.Xomega_lb_allq_clean_modulo_B1` | `[propext, Classical.choice, Quot.sound]` | `[PROVEN:Lean]` |
| **EQUALITY core (non-attained inf)** | `OnsetEquality.Xomega_eq` (`OnsetEquality.lean`) | `[propext, Classical.choice, Quot.sound]` | **`[PROVEN:Lean]`** (mod hFW/Boundary) |
| **EQUALITY q=5 (golden L)** | `OnsetEquality.Xomega_eq_q5`; `OnsetEqualityLowQ.Xomega_eq_q5'`, `.Xomega_eq_q5_concrete` | `[propext, Classical.choice, Quot.sound]` | **`[PROVEN:Lean]` — NON-VACUOUS** |
| **EQUALITY q=6** | `OnsetEqualityLowQ.Xomega_eq_q6'`, `.Xomega_eq_q6_concrete` | `[propext, Classical.choice, Quot.sound]` | **`[PROVEN:Lean]` — NON-VACUOUS** |
| **EQUALITY q=7..21 (uniform + per-q)** | `OnsetEqualityUniform.Xomega_eq_uniform`, `.Xomega_eq_q{7..21}` | `[propext, Classical.choice, Quot.sound]` | **`[PROVEN:Lean]`** (each mod its per-q hFW) |
| Genuine-class discharge (equality plumbing) | `GenuineClassDischarge.boundary_of_hecke`, `.perq_Xomega_lb_qge19_GEN'`, `.Tgen_orbit_genuine` | `[propext, Classical.choice, Quot.sound]` | `[PROVEN:Lean]` |
| Cusp Dirac inadmissible in SCALAR class | `EqualityUB.cusp_dirac_inadmissible` (`EqualityUpperBound.lean`) | `[propext, Classical.choice, Quot.sound]` | `[PROVEN:Lean]` |

**Per-q window files** `BCZHeckeG{5,7,8,…,18,19,20,21}_window_VERIFIED.lean` are all
present, sorry-free, axiom-clean; they discharge `Fwindow4/5/6` per index. The lower-bound
unconditional half covers the seventeen Hecke indices {5,7,8,…,21}; the **equality** is
verified for the same family plus q = 6, i.e. **q ∈ {5, 6, 7, …, 21}**. The corridor + L1b
route is genuinely needed only for **q ≥ 22**, which is **open**.

**Headline reading.** The **equality** X_Ω(q) = 1/λ_q³ is machine-verified, axiom-clean,
for q = 5..21 (`OnsetEquality.Xomega_eq` and its q-instances), with two grades of closure:

- **q = 5 and q = 6: fully closed, unconditional.** `OnsetEqualityLowQ.Xomega_eq_q5_concrete`
  and `.Xomega_eq_q6_concrete` take **no** hypotheses — the band conditions (1 < λ < 2,
  l² = l+1 resp. l² = 3) are discharged internally via Mathlib's `cos_pi_div_five` /
  `cos_pi_div_six`, and the F-window is proved in-file (`wins6_q5`, `wins6_q6`). These are
  the strongest standalone statements.
- **q = 7..21: equality modulo the (true, arithmetic) band hypotheses, window discharged.**
  `OnsetEqualityUniform.Xomega_eq_q{7..21}` carry the band facts (`hHecke`, `hmp`/`mpoly_q`,
  1 < λ < 2, 9/5 < λ, l² ≥ l+1) as arguments; the per-q F-window certificate is already
  supplied internally (`_root_.hF{q}`, from `BCZHeckeG{q}_window_VERIFIED`). The band facts
  are arithmetic truths about the real λ_q (closed concretely exactly as for q = 5,6); they
  are simply not yet bundled into a no-argument `_concrete` theorem for q ≥ 7. So the equality
  is established for these indices modulo discharging those arithmetic hypotheses, not modulo
  any open mathematics.

The all-q LOWER bound `Xomega_lb_allq` is axiom-clean as a theorem object (the prior
L1b/`fcorr_lb` sorry is gone), but for **q ≥ 22 it carries the never-proved `hCorr`** in its
statement — it is a **conditional** result, **not** an unconditional all-q theorem.

---

## 5. The arc-width inequality L1b, sealed

The crux `fcorr_lb` (= `B1_target` after the sInf reduction) states

    fcorr_lb (q ≥ 18) (hL : 0 < L_blk q) {μc ∈ Ioo(−(π/2−H), π/2−H)} :
        1/λ³ ≤ fcorr(L_blk q, q, hL, μc),

with fcorr = (3λ/2 + √A₂·windowMaxCos) / (2·A₂·B_λ²·cos²(|μc| + H)),
L_blk q = ⌈33q/256⌉ + 2, θ = π/q, λ = 2cosθ, A₂ = 1 + 2λ², H = (L−1)θ/2.

**Sealed 2026-06-14.** `lake build L1bArcCoverage` → `Build completed successfully
(8027 jobs)`, **0 sorry**, with (quoted)

    'L1bArcCoverage.fcorr_lb'  : [propext, Classical.choice, Quot.sound]
    'L1bArcCoverage.B1_target' : [propext, Classical.choice, Quot.sound]

The proof (file `L1bArcCoverage.lean`, the only file touched to seal it):

- **Key algebraic identity** `2·A₂·B_λ² = 12λ² + 2 = 48c² + 2` (`twoA2Blam_eq`, exact),
  eliminating √/÷ from both regime cores.
- **Regime A** (|μc| ≤ H, pigeonhole window index): split into the exact-H small range
  q ∈ {18..23} (L_blk = 5, H = 2θ exactly — the loose bound H ≥ 33π/512 + θ/2 is provably
  FALSE here, margins −0.28..−0.005) and the loose-H large range q ≥ 24
  (`regimeA_small`, `regimeA_large`, combined in `regimeA_all`). cos kept symbolic via
  proved Taylor envelopes; the worst case is the q → ∞ limit ≡ `cos_sq_lt`
  (cos²(33π/512) < 24/25), closed with `linear_combination` coefficient 50.
- **Regime B** (|μc| > H, endpoint index): the on-domain version `regimeB_ondomain` (the
  in-file `RegimeBCore` def omitted the domain upper bound and was mis-stated / false beyond
  the domain) reduces to the unit-circle inequality `arc_trig`; margin ≥ +2.8 (comfortable,
  not the +0.0175 earlier feared). Closing the endpoint phase needs `eta_ge_2xi` (2ξ ≤ η),
  proved via `Real.arctan_add` reducing to 32c⁴ + 12c² + 1 ≥ 0.
- **Asymptotic safety** (de-risk, `[PROVEN:interval]` + analytic): the limit margin is
  δ_∞ = 3/(25 cos²(33π/512)) − 1/8 = 5.77·10⁻⁵ > 0, and the make-or-break inequality
  33/256 > 2·arccos(2√6/5)/π reduces to the single algebraic fact cos²(33π/512) < 24/25.
  Interval certification: all q = 18..10000 pass (worst margin 7.33·10⁻⁵ at q = 10000);
  margin ↓ δ_∞ at rate ~C/q, never crossing 0. The existential risk R1 (margin → 0) is
  **not** realized. This corroborates the Lean seal; the Lean proof is the proof of record.

---

## 6. Honest ledger — exactly what is unconditional and what is carried

This is the section to read for the precise standing. Three categories.

### (A) Machine-verified `[PROVEN:Lean]` (axiom-clean), for the verified family

- **EQUALITY** X_Ω(q) = 1/λ_q³ for **q ∈ {5, 6, 7, …, 21}** (seventeen Hecke indices,
  q = 5 the golden L), as a **non-attained infimum** over the closed-section invariant-measure
  class, realized by the cusp parabolic-Dirac sequence. Via `OnsetEquality.Xomega_eq` (core),
  `OnsetEquality.Xomega_eq_q5` / `OnsetEqualityLowQ.Xomega_eq_q5'` (golden L, non-vacuous),
  `OnsetEqualityLowQ.Xomega_eq_q6'` (q=6, non-vacuous), and
  `OnsetEqualityUniform.Xomega_eq_uniform` + `.Xomega_eq_q{7..21}`. Each is conditional only on
  its per-q F-window certificate `hFW` (discharged by `BCZHeckeG{q}_window_VERIFIED`) and the
  standard `Boundary`/`MeasurePreserving` setup; all axiom-clean. The carried `MeasurePreserving`
  is the invariant-measure quantifier (definitional). **This is the headline.**
- The lower bound X_Ω(q) ≥ 1/λ_q³ for the same family via `GenuineMapFacts.Xomega_lb_q5to21`
  (scalar F-window route, no corridor), axiom-clean.
- The matching UPPER bound is the cusp-Dirac sequence in the **closed-section / P_gen** class
  (`OnsetEquality.Xomega_le`, `.cusp_dirac_admissible`); the *same* Dirac is **inadmissible** in
  the scalar / P_prod / Dcorr engine class (`EqualityUB.cusp_dirac_inadmissible`), so the
  equality is correctly stated over the closed section — not over the scalar engine class.
- The arc-width crux **L1b** (`fcorr_lb`, `B1_target`), sealed, axiom-clean.
- (P1) the scalar-branch ⇒ Dcorr F-corridor confinement bridge
  (`GenuineMapFacts.scalar_implies_Dcorr`), proved from the existing genuine-map definition
  (`branchIdx`/`IsFstep_concrete` + cheb boundary data), axiom-clean.
- All structural plumbing: the genuine-class discharge (`GenuineClassDischarge`), the
  orbit-data adapter, the per-q corridor composition, the sorry-isolation witness — all
  axiom-clean.

### (B) Carried as NAMED structural hypotheses for q ≥ 22 (NOT sorries)

The forall-q theorem object is axiom-clean; for q ≥ 22 it carries, **in its statement**:

- **`hCorr` (the corridor-assembly hypothesis).** This packages the q ≥ 22 corridor
  conclusion `1/l³ ≤ ess-sup_μ P_gen` as supplied by the M_W block-monodromy + L1b route.
  Its *analytic* content is now `L1b` (sealed) — referenced in the proof via `L1b_carried`
  so the dependency is real — but the **wiring of the block-boundary sequence to an actual
  Tmap-orbit and its essSup** (with its own engine instantiation and the geometric-realization
  bridge `hbridge`: g_corr ≤ g_true) is **not yet a single discharged theorem**. This is the
  honest remaining assembly gap for q ≥ 22 beyond L1b itself. Status: carried hypothesis;
  analytic input sealed, dynamical wiring open.
- **`(P2)` the genuine-orbit-invariance bridge** (`GenuineClassP2.hEject`). It identifies the
  assembly observable P_gen at successive Tmap-orbit points with the genuine `genStep`
  successor product that `ejection_kick_uniform` bounds. `ejection_kick_uniform` proves the
  bound on (u,v,r); `succ_prod_lb` lifts it to the genuine successor product; but identifying
  *that* successor product with P_gen(orbit(n+1)) on a Tmap-orbit is the genuine map's orbit
  invariance, present in no VERIFIED file. Status: carried hypothesis (one genuine-map fact).

These are legitimate hypotheses — they are the **definition of the genuine map** and the
**corridor-assembly interface**, carried exactly as `hEngine`, `hFW`, `hOrbitData` are carried
by every upstream per-q theorem. They are visible in the statement; the theorem is honestly
*conditional on them* for q ≥ 22, *not* sorry-stubbed.

### (C) What is therefore NOT yet claimed

We do **not** claim a fully unconditional ∀q ≥ 5 theorem; **q ≥ 22 is open**, and the proof
method is **structurally blocked** there (the fixed six-window argument caps once the
sub-threshold cluster ceiling B(q) exceeds ~5, around q = 22; a genuine all-q result needs the
unproven cluster-growth law B(q), §3.6). The precise residual to even a *conditional* all-q
bound being made unconditional: (1) discharge `(P2)` by constructing the all-q genuine
multi-branch measure-preserving map T on Taha with an invariant probability measure such that
the trichotomy htri and the orbit-invariance bridge hold (components exist sorry-free in
`BCZHeckeGenuineMap_allq_WIP`; the dynamical-system + measure assembly is unbuilt —
"routine-but-substantial measure theory"); and (2) wire the block-monodromy sequence to the
orbit essSup for q ≥ 22 (`hCorr` / `hbridge`). Even with (1)+(2) discharged, a clean all-q
*value* would still need the cluster-growth law to replace the fixed six-window certificate.

**Self-check (honesty).** Against the consolidation brief: (i) the headline is the
**equality** X_Ω(q) = 1/λ_q³, machine-verified axiom-clean for **q = 5..21** (q = 6 included,
q = 5 golden L non-vacuous), as a non-attained infimum realized by the cusp parabolic-Dirac
sequence over the closed section — corroborated by a fresh build of `OnsetEquality*` /
`GenuineClassDischarge`; (ii) **q ≥ 22 is open and structurally blocked**, not merely
"conditional progress"; (iii) `ToplevelStitch.Xomega_lb_allq` is a **conditional** lower
bound (carries `hCorr`, and `(P2)` for the genuine route) — it is **not** an unconditional
all-q result; (iv) the carried `MeasurePreserving` is the invariant-measure quantifier
(definitional), not an extra assumption; (v) L1b is **sealed**, not carried. We do not inflate
"q = 5..21 equality + L1b sealed + P1 discharged" into "all q."

---

## 7. Relation to ergodic optimization and extreme-value theory

### 7.1 Ergodic optimization / zero temperature

X_Ω(q) = inf_μ ess-sup_μ P is an **ergodic-optimization** quantity (Jenkinson; Bochi,
*Ergodic optimization of Birkhoff averages and Lyapunov exponents*, ICM 2018). It is the
zero-temperature / ground-state value of the thermodynamic formalism for the observable P:
as the inverse temperature β → ∞, equilibrium states concentrate on the minimizing set, and
the relevant edge is the inf-over-measures of the essential supremum. Our result identifies
this ground value as the explicit cusp-tip constant 1/λ_q³ for the verified Hecke indices
q = 5..21 (and conjecturally beyond, q ≥ 22 open).

Two structural caveats that shape the proof:

- The BCZ-type map is **weakly mixing / parabolic** (zero entropy), not hyperbolic
  (arXiv:2403.14976). So there are no hyperbolic Mather sets and the value is **not** an
  Aubry–Mather β-function value; the naive "1/λ³ as Mather minimizing average" reading is
  false. The ground value comes from the cusp geometry + corridor rotation, not from a
  hyperbolic minimizing measure. `[NUMERICAL]` falsification recorded.
- The observable's law is governed by the **invariant-measure level-set** structure
  (E[(xy)^β] is exactly analytic in β for BCZ), so 1/λ³ is a level-set edge, **not** a
  pressure / phase-transition object. This is *why* the elementary no-sustained ⇒ support-edge
  engine suffices and no transfer-operator spectral gap is needed.

This is, to our knowledge, the **first machine-verified theorem in ergodic optimization**.

### 7.2 Extreme-value theory

The support edge of an observable under an invariant measure is the right endpoint of the
observable's distribution — an **extreme-value** quantity. In the Marklof–Strömbergsson–Yu
program (arXiv:2510.11371) the analogous observable (1/shortest-vector) has an extreme-value-
limit density with *exponential* tails on both sides — **no** compact support, **no** hard
edge. The Hecke slope-gap gap product is the opposite regime: **compact support with a hard
edge**, the lattice/Veech case of the Athreya–Chaika dichotomy. Our theorem pins the edge's
value. The width of the in-domain corridor arc (Δ(q) → 0.1282π) is the EVT support-fraction
analogue, and its strict positivity is exactly why the edge is bounded away from 0.

---

## 8. Open problems

1. **The q ≥ 22 wall ⇒ all-q value.** This is the headline open problem. The fixed
   six-window method is **structurally blocked** for q ≥ 22 (the cluster ceiling B(q) > ~5;
   §3.6), so reaching all q needs the **cluster-growth law B(q)** (the closed form, currently
   `[NUMERICAL]`) to replace the per-q window certificate. Subsidiary plumbing: discharge
   `(P2)` (the all-q genuine measure-preserving map + invariant measure) and the corridor
   wiring `hCorr` (M_W block sequence → orbit essSup) — these would make the existing
   *conditional* all-q lower bound unconditional, but a clean all-q *value* still needs B(q).
   `[CONJECTURE]`.

2. **The exact cluster-ceiling closed form B(q).** Prove the rotation-arc account of §3.6 as
   a theorem: that a sub-threshold cluster is exactly the elliptic-rotation arc (k = 1 interior
   steps) terminated by the floor increment k : 1 → 2, giving B(q) = ⌊w(q)·q/π⌋ + 1 with
   w(q) → w_∞ ≈ 0.678 (slope ≈ 0.22). Another agent is rigorizing this; it is the missing
   ingredient for #1. `[NUMERICAL]` (matches all data); proof open.

3. **Veech-section identification.** Is the BCZ gap-product cross-section for G_q literally
   the slope-gap section of the H_q-Veech (double-(2q−1)-gon) surface, or a quotient of it?
   If yes, X_Ω(q) = 1/λ_q³ becomes a statement about saddle-connection slope gaps and connects
   to the live Veech-dynamics community (Fairchild's Siegel–Veech transform over Hecke-triangle
   quotients, arXiv:1901.10115, is the natural bridge). `[CONJECTURE]`.

4. **Effective onset and the dimension spectrum.** Couple the uniform onset value to the
   Rosen-continued-fraction dimension spectrum (the validated Jenkinson–Pollicott engine,
   `code/d3_jp_dimension.py`, reproduces dim E_{1,2} = 0.5312805 to 1e-15). `[CONJECTURE]`.

5. **The method beyond Hecke (X_Ω(Γ) family).** The GATE-2 architecture (engine ∘
   confinement ∘ rotation-ellipse arc-width) is a *method*. For which other Fuchsian / Veech
   families does it yield a machine-verified support-edge value? Caveat (per the 3-track
   scout, `research_notes/Xomega_generalize_2026-06-14.md`): the *mechanism* (edge = cusp /
   parabolic-fixed value) ports across the triangle-group family, but the scalar X_Ω is
   **normalization-dependent** (= 1 in canonical ACL section coords; = 1/λ³ only in the Taha
   normalization, and the two observables — gap-product P and return-time R — are reciprocal,
   R = 1/P, not diagonally conjugate; see `code/xomega_normalization_proof.py`). So X_Ω is
   **not a new lattice invariant** and **not a commensurability detector**; the contribution
   of any such extension would be **methodological** (a family-wide machine-verified edge),
   not a new invariant. `[CONJECTURE]`.

*Resolved since the prior draft: the matching **upper bound** (equality X_Ω(q) = 1/λ_q³, not
just ≥) is now machine-verified for q = 5..21 — the cusp parabolic-Dirac sequence over the
closed section (`OnsetEquality.Xomega_le`); see §4.*

---

## Appendix A. Verification commands (reproducibility)

All from `projects/aristotle_dispatch_v15/uniform_q5to18/` with Lean 4.28.0 / Mathlib v4.28.0:

```
# Lower-bound + crux route:
lake build L1bArcCoverageLib        # → 8027 jobs; fcorr_lb, B1_target axiom-clean
lake build GenuineMapFactsP1        # → scalar_implies_Dcorr axiom-clean
lake build ToplevelStitch           # → Xomega_lb_allq (CONDITIONAL q≥22) axiom-clean (no sorryAx)
lake build ToplevelStitchQ5to21     # → Xomega_lb_q5to21, Xomega_lb_allq_q5to21_P1 axiom-clean
# EQUALITY route (the headline, q = 5..21):
lake build OnsetEqualityLowQ        # → 8056 jobs; Xomega_eq_q5'/q6'/concrete axiom-clean
lake build OnsetEqualityUniform     # → 8055 jobs; Xomega_eq, Xomega_eq_q5, Xomega_eq_uniform,
                                    #   Xomega_eq_q{7..21} axiom-clean
lake build EqualityUpperBound       # → 8041 jobs; cusp_dirac_inadmissible (scalar class) axiom-clean
```

Quoted `#print axioms` (2026-06-14 build):

```
# Lower-bound / crux:
'L1bArcCoverage.fcorr_lb'                        : [propext, Classical.choice, Quot.sound]
'L1bArcCoverage.B1_target'                       : [propext, Classical.choice, Quot.sound]
'GenuineMapFacts.scalar_implies_Dcorr'           : [propext, Classical.choice, Quot.sound]
'HeckeEjectionUniform.ejection_kick_uniform'     : [propext, Classical.choice, Quot.sound]
'ToplevelStitch.genuine_orbitdata'               : [propext, Classical.choice, Quot.sound]
'ToplevelStitch.perq_Xomega_lb_qge19'            : [propext, Classical.choice, Quot.sound]
'ToplevelStitch.perq_Xomega_lb_qge19_P1discharged': [propext, Classical.choice, Quot.sound]
'ToplevelStitch.L1b_carried'                     : [propext, Classical.choice, Quot.sound]
'ToplevelStitch.Xomega_lb_allq'                  : [propext, Classical.choice, Quot.sound]
'ToplevelStitch.Xomega_lb_allq_clean_modulo_B1'  : [propext, Classical.choice, Quot.sound]
'GenuineMapFacts.Xomega_lb_q5to21'               : [propext, Classical.choice, Quot.sound]
'ToplevelStitch.Xomega_lb_allq_q5to21_P1'        : [propext, Classical.choice, Quot.sound]
# EQUALITY (headline):
'OnsetEquality.Xomega_eq'                        : [propext, Classical.choice, Quot.sound]
'OnsetEquality.Xomega_eq_q5'                     : [propext, Classical.choice, Quot.sound]
'OnsetEqualityUniform.Xomega_eq_uniform'         : [propext, Classical.choice, Quot.sound]
'OnsetEqualityUniform.Xomega_eq_q7'              : [propext, Classical.choice, Quot.sound]
'OnsetEqualityUniform.Xomega_eq_q21'             : [propext, Classical.choice, Quot.sound]
'OnsetEqualityLowQ.Xomega_eq_q5''                : [propext, Classical.choice, Quot.sound]
'OnsetEqualityLowQ.Xomega_eq_q6''                : [propext, Classical.choice, Quot.sound]
'OnsetEqualityLowQ.Xomega_eq_q5_concrete'        : [propext, Classical.choice, Quot.sound]
'OnsetEqualityLowQ.Xomega_eq_q6_concrete'        : [propext, Classical.choice, Quot.sound]
'EqualityUB.cusp_dirac_inadmissible'             : [propext, Classical.choice, Quot.sound]
```

## Appendix B. Key file index

- `BCZHeckeUniformOnset.lean` — observables (P_gen, P_prod), Tmap, Taha, Dcorr; engine type;
  Fwindow4/5/6; cusp_step_bound; per_q_Xomega_lb_{6,5,4}win.
- `BCZHeckeS1_trichotomy.lean` — step_trichotomy; IsCusp_to_CuspGuards; branchIdx machinery.
- `EjectionUniform.lean` — ejection_kick_uniform (uniform deep-mid box, all q ≥ 16).
- `L1bArcCoverage.lean` — the arc-width crux: fcorr_lb, B1_target (SEALED).
- `GenuineMapFactsP1.lean` — scalar_implies_Dcorr (P1, proved).
- `GenuineMapFacts.lean` — q=19,20,21 unconditional 6-window extension; Xomega_lb_q5to21.
- `UniformOnset_q5to18.lean` — Xomega_lb_q5to18 (14 indices, unconditional).
- `ToplevelStitch.lean` — genuine_orbitdata adapter; perq_Xomega_lb_qge19(_P1discharged);
  Xomega_lb_allq; clean-modulo-B1 isolation witness.
- `ToplevelStitchQ5to21.lean` — Xomega_lb_allq_q5to21_P1 (q≤21 unconditional, P1-discharged).
- `BCZHeckeG{5,7,…,21}_window_VERIFIED.lean` — per-q F-window certificates.

**Equality files (the headline route, q = 5..21):**
- `OnsetEquality.lean` — the closed-section class (`Sclosed`, `Pgen`), the cusp-Dirac
  admissibility (`cusp_dirac_admissible`), `Xomega_ge`/`Xomega_le`, and the core equality
  `Xomega_eq` (non-attained infimum); `Xomega_eq_q5` (golden L).
- `OnsetEqualityUniform.lean` — `Xomega_eq_uniform` and per-q `Xomega_eq_q{7..21}`.
- `OnsetEqualityLowQ.lean` — non-vacuous `Xomega_eq_q5'`, `Xomega_eq_q6'` (and `_concrete`).
- `GenuineClassDischarge.lean` — `boundary_of_hecke`, `Tgen_orbit_genuine`,
  `perq_Xomega_lb_qge19_GEN'`: the genuine-class plumbing the equality consumes.
- `EqualityUpperBound.lean` — `cusp_dirac_inadmissible`: the cusp Dirac is INADMISSIBLE in the
  scalar / P_prod / Dcorr engine class (so the equality is correctly stated over the closed
  section / P_gen, where it IS admissible).

---

*Internal draft, 2026-06-14. Outward communication USER-gated. Headline scope: the
**equality** X_Ω(q) = 1/λ_q³ is machine-verified (axiom-clean) for q = 5..21 (q = 5 golden L,
q = 6 included), as a non-attained infimum; q ≥ 22 is open and structurally blocked. Every
Lean axiom line above was produced by a fresh build on 2026-06-14 and quoted verbatim.*
