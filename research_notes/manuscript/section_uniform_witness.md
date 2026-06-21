# Section: The reverse direction — realization witnesses for the cluster ceiling B(q)

*Manuscript-ready section. Every quantitative claim is tagged with its evidential status:*
*`[PROVED:Lean]` = sorry-free, axiom-clean `[propext, Classical.choice, Quot.sound]` Lean term;*
*`[CERTIFIED-NUMERIC]` = interval / high-precision arithmetic certificate;*
*`[HEURISTIC]` = float-level / ground-truth observation, not certified.*
*Each `[PROVED:Lean]` claim names the Lean lemma and the file it lives in.*

---

## 1. Setup: what the reverse direction must supply

The forward half of the `B(q)` rotation-arc theorem is fully machine-verified: every genuine
sub-threshold last-branch cluster run *is* an `M`-rotation arc of the same length, so
`clusterCeiling → rotationArcCount`
(`cluster_is_rotation_arc`, `cluster_le_rotation_arc`, file
`projects/aristotle_dispatch_v15/uniform_q5to18/BCZHeckeRotationArc.lean`) `[PROVED:Lean]`.
The conserved-form mechanism it rests on — `M(a,b) = (b, −a+λb)` preserves
`E(a,b) = a² − λab + b²` and *is* the planar rotation by `−π/q` — is likewise verified
(`Mmap_preserves_E`, `Mmat_conj_eq_rot`, same file) `[PROVED:Lean]`.

The **reverse direction** is the *realization residual* R2: to turn the forward implication
into the value `B(q)`, one must exhibit an actual genuine cluster run of the claimed length —
this discharges the named hypothesis `hrealize` that `Bq_eq_rotation_arc` carries
(`BCZHeckeRotationArc.lean`). Concretely, a realization datum is a proof of
`clusterCeiling λ (1/λ³) (lastBranch λ) N`,
i.e. an explicit run `r₀, r₁, …, r_N` (length `N+1`) that is simultaneously
(i) sub-threshold `Pobs(rᵢ) = aᵢbᵢ < 1/λ³`,
(ii) last-branch `aᵢ + λbᵢ > 1`,
(iii) interior floor `k=1` (bracket `λbᵢ ≤ 1+aᵢ < 2λbᵢ`), and
(iv) a genuine BCZ orbit (each step is `kstep` with the actual floor digit), starting from a
cross-section domain point whose predecessor is *not* last-branch.

This section reports two distinct deliverables for R2: a **single uniform closed-form witness
family** (Section 2) and a **ladder of per-q realizations** q = 5..13 (Section 3). Section 4
states the resulting open frontier honestly.

---

## 2. The uniform closed-form reverse witness (q = 7..31, B(q) ≥ 3)

### 2.1 The family

The genuinely-uniform deliverable replaces the per-q hand-picked starts with **one** scale
function

> **s(λ) = (1104 − 385·λ) / 1000**,

placed on a length-3 arc that is symmetric about its middle point on the diagonal `r₁=(s,s)`:

> r₀ = M⁻¹r₁ = (s·(λ−1), s),   r₁ = (s, s),   r₂ = M r₁ = (s, s·(λ−1)).

The three relations `r₀ = M⁻¹r₁`, `r₂ = M r₁` are exact `ring` identities under `M`
(`step0`, `step1`, file
`projects/bq_closure_lean/RequestProject_R2uniform/RequestProject/Main.lean`) `[PROVED:Lean]`.

### 2.2 What is proved, uniformly in λ

For **every real** `λ ∈ [9/5, 199/100] = [1.8, 1.99]` the run `(r₀, r₁, r₂)` satisfies all four
cluster conditions, each discharged once as a polynomial inequality in `λ` over the whole
interval (not per-q):

- sub-threshold `Pobs(rᵢ) < 1/λ³` — `sub0`, `sub1`, `sub2`;
- last-branch `aᵢ + λbᵢ > 1` — `br0`, `br1`, `br2`;
- interior `k=1` bracket — `bracket0`, `bracket1`, hence floor-digit `=1` (`kfloor0`, `kfloor1`);
- genuine `M`-steps — `step0`, `step1`;

all in `RequestProject_R2uniform/RequestProject/Main.lean`. These assemble into

> `runw_isClusterRun` : `IsClusterRun l (1/l³) (lastBranch l) (runw l) 2`
> `uniform_clusterCeiling` : `clusterCeiling l (1/l³) (lastBranch l) 2`, for all `9/5 ≤ l ≤ 199/100`

`[PROVED:Lean]`, axiom-clean `[propext, Classical.choice, Quot.sound]` (axiom audit
`#print axioms HeckeRotArcR2Uniform.uniform_clusterCeiling`, same file).

### 2.3 Hecke specialization

Because `λ_q = 2cos(π/q)` lands in `[1.8, 1.99]` exactly for **q = 7..31**
(`λ₇ = 1.80194 > 1.8`, `λ₃₁ = 1.98974 < 1.99`) `[CERTIFIED-NUMERIC]`, the single family
yields the realization datum for every one of those Hecke groups at once:

> `hecke_clusterCeiling` : for `λ_q ∈ [9/5, 199/100]`, `clusterCeiling λ_q (1/λ_q³) (lastBranch λ_q) 2`

`[PROVED:Lean]` (`RequestProject_R2uniform/RequestProject/Main.lean`). The endpoint
membership is itself verified sorry-free for the q=11 anchor: `λ₁₁ = 2cos(π/11) ≈ 1.91899`,
bracketed by `lam11_gt : 191898/100000 < λ₁₁` and `lam11_lt : λ₁₁ < 191899/100000` (via the
Chebyshev-derived degree-5 minpoly `lam11_minpoly`), giving
`clusterCeiling11_uniform : clusterCeiling λ₁₁ (1/λ₁₁³) (lastBranch λ₁₁) 2`
`[PROVED:Lean]`, same file. This confirms the uniform statement is non-vacuous and reproduces
the independently-proved per-q fact (Section 3) from one formula.

### 2.4 Honest scope of the uniform witness

The uniform family proves a **lower bound only**:

- It establishes **`B(q) ≥ 3`** uniformly for q = 7..31 — a length-3 cluster *exists*. It does
  **not** prove **maximality** `B(q) ≤ 3`; tightness of `B(q) = 3` for the non-resonant q in
  range rests on numerical ground truth (dps≥40 grid scan), not on Lean `[HEURISTIC]`.
- It covers only the **closed λ-interval `[1.8, 1.99]`**, i.e. **q = 7..31**. It says nothing
  about **q ≥ 32** (where `λ_q > 1.99`), and nothing about q = 5, 6 (covered separately,
  Section 3).
- Inside the range it includes the **resonance q's** (e.g. q = 23) where `B(q)` exceeds the
  continuous count; there `B(q) ≥ 3` is still a valid — but **not tight** — lower bound. The
  uniform family makes no resonance claim.

So the uniform contribution is precisely: *one explicit continuous construction
`λ ↦ (s(λ)(λ−1), s(λ))` discharges the R2 realization bridge `hrealize` for the entire block
q = 7..31 simultaneously, as the lower bound `B(q) ≥ 3`* — strictly stronger than any finite
collection of per-q facts, but not the exact-value theorem.

---

## 3. Per-q realizations: the contiguous ladder q = 5..13

Independently of the uniform family, R2 has been discharged **per-q** with hand-picked rational
starts in `Q(λ_q)²`, each axiom-clean. These predate (and corroborate) the uniform family and
extend it at the low end (q = 5) and supply the only **length-4** witness (q = 13).

| q | Lean witness theorem | file | start | run len | B(q) | field / minpoly | status |
|---|---|---|---|---|---|---|---|
| 5 | `genuineCluster5_realized` (`run5_isGenuineCluster`) | `BCZHeckeRotationArcR2.lean` | Q(√5), λ=φ | 3 | ≥3 | golden | lower bound `B(5)≥3`, k-pattern `[2,1]` |
| 7 | `clusterCeiling7`, `Bq_eq_rotation_arc_q7` | `BCZHeckeRotationArcR2.lean` | `(20/61, 25/61)` | 3 | 3 | cubic | FULL — `hrealize` discharged |
| 8 | `clusterCeiling8`, `Bq_eq_rotation_arc_q8` | `BCZHeckeRotationArcR2hi.lean` | — | 3 | 3 | quartic | FULL |
| 9 | `clusterCeiling9`, `Bq_eq_rotation_arc_q9` | `BCZHeckeRotationArcR2hi.lean` | — | 3 | 3 | sextic | FULL |
| 10 | `clusterCeiling10`, `Bq_eq_rotation_arc_q10` | `BCZHeckeRotationArcR2hi2.lean` | — | 3 | 3 | quartic | FULL |
| 11 | `clusterCeiling11` (`run11_isClusterRun`) | `RequestProject_q11_realization/RequestProject/Main.lean` | `(34/101, 37/101)` | 3 | 3 | quintic `x⁵−x⁴−4x³+3x²+3x−1` | FULL |
| 12 | `clusterCeiling12`, `Bq_eq_rotation_arc_q12` | `BCZHeckeRotationArcR2hi2.lean` | — | 3 | 3 | quartic | FULL |
| 13 | `clusterCeiling13`, `Bq_eq_rotation_arc_q13` | `BCZHeckeRotationArcR2hi2.lean` | `(31/94, 17/47)` | 4 | 4 | sextic `x⁶−x⁵−5x⁴+4x³+6x²−3x−1` | FULL — **first length-4 arc** |

All entries `[PROVED:Lean]`, axiom-clean `[propext, Classical.choice, Quot.sound]` (axiom audits
at the foot of each file: e.g. `#print axioms HeckeRotArcR2.clusterCeiling7`,
`HeckeRotArcR2hi2.Bq_eq_rotation_arc_q13`, `HeckeRotArcQ11.clusterCeiling11`).

### 3.1 q = 13 — the 3→4 ceiling transition

q = 13 is the **first** value whose realized arc has length 4, i.e. `B(13) = 4`: the cluster
ceiling steps up from 3 to 4. The witness is the genuine length-4 run from start
`(31/94, 17/47)` over the degree-6 field `x⁶−x⁵−5x⁴+4x³+6x²−3x−1`, discharging `hrealize` with
`N = 3` (`clusterCeiling13 : clusterCeiling lam13 X13 lastBranch13 3`,
`BCZHeckeRotationArcR2hi2.lean`) `[PROVED:Lean]`. This is the formal witness of the
cluster-growth law's first increment; the asymptotic slope `B(q) ~ 0.22q` itself is not
Lean-proved (see Section 4).

### 3.2 q = 11 — the quintic, and a recorded correctness check

q = 11 was the last interior gap in the ladder. Its minpoly is the **quintic**
`λ₁₁⁵ − λ₁₁⁴ − 4λ₁₁³ + 3λ₁₁² + 3λ₁₁ − 1 = 0`, reproved here via the Chebyshev identity
`T₁₁(cos(π/11)) = −1` and the factorization `(λ+2)·minpoly² = 2(T₁₁(λ/2)+1)`
(`lam11_minpoly`, both `RequestProject_q11_realization/.../Main.lean` and the uniform file)
`[PROVED:Lean]`; it matches the separately Aristotle-verified `lambda_11_min_poly`. The witness
is the exact rational start `(34/101, 37/101)`, k-pattern `[1,1,2]`, giving
`clusterCeiling11 : clusterCeiling λ₁₁ X₁₁ lastBranch₁₁ 2` `[PROVED:Lean]`.

**Recorded correctness check (so it is not repeated).** A naive `M`-orbit search found a
length-4 candidate from `(19/61, 22/61)` satisfying last-branch + sub-threshold + `k=1` at all
interior points — but that start **fails** the cross-section domain condition `b > 1 − λa`
(`b = 0.3607 < 0.4023`) and its orbit leaves the section: a **transient**, not a genuine
cluster. `B(11) = 3` stands (ground-truth k-pattern `[1,1,2]`; continuous count `B₀(11) = 3`;
q = 11 is **not** a resonance, scalar gate `R(11) = 0` since `ρ_min ≈ 1.0451 > ρ_max ≈ 1.0211`)
`[HEURISTIC]` (numeric, `q11_witness_v2.py`, dps=60) `[CERTIFIED-NUMERIC]`. **Lesson:** any per-q
realization witness must be checked for cross-section domain-validity *and* genuine-cluster-start
(predecessor not last-branch), not merely last-branch + sub-threshold + bracket.

---

## 4. Updated open-frontier statement

Combining the realization deliverables of this section with the matching machinery:

### 4.1 What is closed

- **Equality `X_Ω(q) = 1/λ_q³`** (the onset value) is machine-verified for **q = 5..21**
  (core `OnsetEquality.Xomega_eq`; q=5,6 no-hypothesis `Xomega_eq_q5_concrete`,
  `Xomega_eq_q6_concrete`; q=7..21 `OnsetEqualityUniform.Xomega_eq_uniform`, all under
  `projects/aristotle_dispatch_v15/uniform_q5to18/`) `[PROVED:Lean]`, modulo per-q arithmetic
  band facts.
- The **reverse / realization** half of the `B(q)` rotation-arc theorem is closed as: the
  **uniform lower bound `B(q) ≥ 3` for q = 7..31** (`uniform_clusterCeiling`,
  `hecke_clusterCeiling`) `[PROVED:Lean]`, plus the **exact per-q ladder q = 5..13** including the
  first length-4 transition at q = 13 (`clusterCeiling{5..13}`) `[PROVED:Lean]`.
- The **R3 parity gate** (resonance `+1` fires only when `B₀(q)` is even-parity-admissible;
  "parity beats proximity") is fully proved (`resonance_parity_gate`,
  `BCZHeckeRotationArcR3Parity.lean`) `[PROVED:Lean]`.

### 4.2 What remains OPEN / structurally blocked

- **R2 uniform-all-q (exact value, all q):** the uniform family gives only `B(q) ≥ 3` and only on
  `[1.8, 1.99]` (q = 7..31). A uniform *exact-value* witness family `q ↦ (a₀(q), b₀(q))` realizing
  the full ladder is **OPEN** and likely stays open — the per-q starts have no evident closed form
  beyond the symmetric length-3 construction `[HEURISTIC]`.
- **q ≥ 22 onset equality:** the lower-bound route for `X_Ω(q) = 1/λ³` is **structurally blocked**
  beyond q = 21. The F-window method hard-codes a fixed conjunct count `W = B(q)+1` (4-window
  through q=11, 5-window through q=16, 6-window through q=21), but the cluster ceiling grows
  `B(q) ~ 0.22q` `[HEURISTIC]`, crossing 5 around q ≈ 22, so no *fixed* window length can refute a
  linearly-growing sub-threshold run. This wall is structural, not a Lean-engineering limit
  (`ToplevelStitch.Xomega_lb_allq` carries the named hypothesis `hCorr` beyond q = 21).
- **R3 transcendental near-fit:** the resonance set `{23, 61, 126, 570, …}` is decidable per-q
  (interval arithmetic on the closed-form arc width `W(q)`) `[CERTIFIED-NUMERIC]` but its
  closed-form characterization is analytic-**OPEN**. The closed-form cluster law
  `B(q) = ⌊W(q)·q/π⌋ + 1` is numerical-only `[HEURISTIC]`.

### 4.3 The candidate route past q = 22

The route that bypasses both the fixed-window wall and the need for an exact closed-form `B(q)` is
the **Koyama energy / transfer-operator** argument. It replaces the q-by-q F-window combinatorics
with one q-independent dynamical statement, discharging exactly the carried `hCorr`: the conserved
ellipse `E = c_n² + c_{n+1}² − λ c_n c_{n+1}` is the invariant of the trace-`λ` elliptic rotation
`M` (angle `π/q`); a finite pure-rotation run is already proved
(`E_conserved`, `no_infinite_rotation`,
`projects/mimo-mini-project/lean/BCZHeckeNoInfiniteRotation_allq_VERIFIED.lean`) `[PROVED:Lean]`,
and a corridor switch forces `|trace| ≥ 2` (`switch_forces_nonelliptic`,
`BCZHeckeXOmega_corridor_q18_UNCONDITIONAL.lean`) `[PROVED:Lean]`. The remaining target is the
single **no-dwell / escape-of-mass** lemma:

> for `0 < λ < 2`, angle `θ = π/q`, no `R_θ`-invariant probability measure on the conserved
> ellipse is supported entirely in the sub-threshold sector (equivalently, every θ-rotation
> trajectory enters the super-threshold arc within `O(q)` blocks).

Its analytic half is sealed (`arc_coverage_ineq`, `L1bArcCoverage.fcorr_lb`) `[PROVED:Lean]`; the
measure-theoretic wrapper — *a fixed-angle rotation on a compact arc has no invariant sub-arc
measure* — is **not yet formalized** and is the proposed q-independent target `[HEURISTIC/CONJECTURE]`.
Discharging it would turn the conditional all-q onset lower bound unconditional (modulo the genuine-map
orbit-invariance bridge P2), closing q ≥ 22 without the exact `B(q)`.

---

## 5. Summary

The reverse direction is delivered as a single closed-form witness family — one scale
`s(λ) = (1104 − 385λ)/1000` proving `B(q) ≥ 3` uniformly for q = 7..31
(`uniform_clusterCeiling`) — backed by an exact per-q ladder q = 5..13 that includes the
quintic q = 11 and the first length-4 arc at q = 13 (`clusterCeiling{5..13}`), all sorry-free
and axiom-clean. The onset equality `X_Ω(q) = 1/λ_q³` is machine-verified for q = 5..21; q ≥ 22
is structurally blocked under the fixed-window method, and the Koyama energy / transfer-operator
no-dwell lemma is the named candidate to close it. No exact-value all-q witness family and no
closed-form resonance characterization are claimed.
