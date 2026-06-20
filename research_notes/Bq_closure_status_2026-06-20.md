# B(q) rotation-arc theorem — PROVED / OPEN map (2026-06-20)

Scope: the B(q) "sub-threshold last-branch cluster ceiling = rotation-arc lattice count"
theorem for the Rosen continued-fraction / Hecke G_q last-branch observable. This note is
the proved-vs-open audit requested for /goal G3, plus the new q=11 realization.

Files audited (all under
`projects/aristotle_dispatch_v15/uniform_q5to18/`, all `lake`-built, all axiom-clean
`[propext, Classical.choice, Quot.sound]`, NO `sorry`):
`BCZHeckeRotationArc.lean`, `…R1.lean`, `…R2.lean`, `…R2hi.lean`, `…R2hi2.lean`,
`…R3Parity.lean`.

New file this session:
`projects/bq_closure_lean/RequestProject_q11_realization/RequestProject/Main.lean`
(self-contained; compiles sorry-free + axiom-clean against Mathlib v4.28.0 locally).

---

## 1. The theorem and its three residuals

The mechanism: on the last (scalar) branch with floor digit k=1, the genuine BCZ successor
is the elliptic rotation `M(a,b) = (b, −a+λb)` (`λ = 2cos(π/q)`), which preserves the
conserved form `E(a,b) = a² − λab + b²` and IS the literal rotation by `−π/q`. A
sub-threshold last-branch cluster is therefore a contiguous arc of `M`-rotation-lattice
points (step `−π/q`). `B(q)` = the length of the longest such arc.

The full theorem `clusterCeiling ↔ rotationArcCount` had three named residuals:

| residual | meaning | status |
|---|---|---|
| **mechanism / forward** | every cluster IS an M-rotation arc ⇒ `clusterCeiling → rotationArcCount` | **PROVED** (`cluster_le_rotation_arc`, `cluster_is_rotation_arc`) |
| **R1** | interior-k=1 confinement (the floor bracket holds at every interior step) | **LOWER half PROVED** (`lower_bracket_preserved_on_ellipse`, R1); upper half ≡ R3 |
| **R2** | realization bridge `hrealize`: every sub-threshold last-branch M-arc is realized by a genuine cluster run — supplied per-q by exhibiting an explicit genuine cluster | **PROVED per-q** for q ∈ {5(≥3),7,8,9,10,11(new),12,13}; OPEN uniform-all-q |
| **R3** | exact value / resonance (notch-straddle): does the −π/q lattice hop the super-threshold notch? | **PARITY GATE PROVED** (`resonance_parity_gate`); transcendental near-fit residual OPEN |

---

## 2. PROVED (machine-verified, axiom-clean)

### Mechanism core (`BCZHeckeRotationArc.lean`)
- `Mmap_preserves_E`, `E_posdef`, `coord_sq_le` — `M` preserves the conserved ellipse `E`,
  which is positive-definite for `λ < 2`.
- `Mmat_conj_eq_rot` — `M` IS the literal planar rotation by `−θ` (`λ = 2cosθ`) in
  whitening coordinates (exact, not just det/trace).
- `kstep_eq_Mmap_of_k1`, `kfloor_eq_one_iff_bracket`, `genuine_step_eq_Mmap_of_bracket`
  — the k=1 step is `M`; floor digit = 1 ⟺ bracket `λb ≤ 1+a < 2λb`.
- `cluster_is_rotation_arc`, `cluster_le_rotation_arc` — every genuine sub-threshold
  last-branch cluster run is an M-rotation arc of the same length ⇒
  `clusterCeiling N → rotationArcCount N`. THE FORWARD DIRECTION IS FULLY PROVED.
- `Bq_eq_rotation_arc` — packages the equivalence taking `hrealize` as a named hypothesis.

### R1 (`BCZHeckeRotationArcR1.lean`)
- `lower_bracket_preserved_on_ellipse` — the LOWER bracket (`λb ≤ 1+a`, i.e. k ≥ 1) is
  PROVED on the sub-threshold ellipse (identity `1+a'−λb' = (λa+b−1)+(2−λ²b)` + ellipse
  confinement `λ²b < 2`). `cluster_is_rotation_arc'` now carries only the UPPER bracket,
  which coincides with R3 (the lattice-gap / notch-straddle).

### R3 parity gate (`BCZHeckeRotationArcR3Parity.lean`) — 13 theorems, all axiom-clean
- `rel_reflect`, `odd_center_on_peak`, `even_all_offpeak` — a symmetric N-point
  equal-spacing lattice has its nearest point to the peak at offset 0 (N odd) or ±θ/2
  (N even).
- `parity_gate`, `resonance_parity_gate`, `gain_requires_even`, `odd_always_impaled` —
  for a symmetric super-threshold notch of half-width `w < 1/2` (in θ-units): the whole
  run avoids the notch ⟺ N is EVEN. So the resonance gain `+1` (target N = B₀+1) can fire
  only when N is even (B₀ odd); N odd is always impaled (centre point on the peak),
  irrespective of how narrow the notch ("parity beats proximity", q=47).
- `Pphi_reflect`, `Pphi_peak`, `impale_observable`, `superthreshold_iff_cos` — the gate
  rephrased on the genuine cosine observable `P(φ) = E₀(c₀ + amp·cos2(φ−φ*))`.

### R2 per-q realizations (axiom-clean) — `Bq_eq_rotation_arc_qN` + `clusterCeilingN`
| q | file | run length (N+1) | B(q) | field / minpoly | notes |
|---|---|---|---|---|---|
| 5 | R2 | 3 (lower bd only) | ≥3 | Q(√5), λ=φ | `B(5) ≥ 3` (witness, raw genuine cluster) |
| 7 | R2 | 3 | 3 | cubic | FULL: `hrealize` discharged, witness (20/61,25/61) |
| 8 | R2hi | 3 | 3 | quartic | FULL |
| 9 | R2hi | 3 | 3 | sextic-ish | FULL |
| 10 | R2hi2 | 3 | 3 | quartic | FULL |
| **11** | **bq_closure_lean (new)** | **3** | **3** | **quintic** `x⁵−x⁴−4x³+3x²+3x−1` | **FULL: witness (34/101,37/101)** |
| 12 | R2hi2 | 3 | 3 | quartic | FULL |
| 13 | R2hi2 | 4 | 4 | degree-6 | FULL — FIRST length-4 arc (the 3→4 ceiling transition) |

The contiguous realized block is now **{7,8,9,10,11,12,13}** (plus lower bound B(5)≥3).

---

## 3. OPEN (honest)

### R2 uniform-all-q  — OPEN (likely stays open)
Each per-q realization is a finite, mechanical (field-degree-grind) certificate: pick the
genuine valid-domain cluster start, prove last-branch + sub-threshold + k=1-bracket via
`nlinarith` over the minpoly. There is NO uniform witness family `q ↦ (a₀(q), b₀(q))`
proven. Producing one is the genuine open piece of R2 (needs a closed-form genuine cluster
start as a function of q, then a uniform `nlinarith`/positivity argument — currently absent;
the per-q starts have no evident closed form). q = 14..21 and all q ≥ 14 realizations are
unproved (mechanical but unwritten); q ≥ 23 includes the resonances.

### R3 transcendental near-fit — OPEN (decidable per-q, analytic-open uniform)
The parity gate is proved; what remains is the near-fit inequality: that the notch
half-width is actually `δ < θ/2` AND the arc width `W(q)·q/π` reaches the (even) integer
`B₀+1` from below at `frac > 1` small enough. This is an `L1b`-family transcendental
inequality in `W(q) = arccos(…) − arctan(…)` (closed form in `λ = 2cos(π/q)`, see
`Bq_width_resonance_closed_form_2026-06-18.md`). It is decidable per-q (interval-arith on
`δ(q)`, `s(q) = W(q)q/π`); a closed-form characterization of the resonance set
`{23, 61, 126, 570, …}` is analytic-open.

### R1 upper bracket ≡ R3 — OPEN
Already noted: the R1 upper-bracket residual is the same inhomogeneous-Diophantine
lattice-gap as R3. So the two reduce to ONE hard residual (the near-fit), plus R2-uniform.

---

## 4. New result this session: q = 11 realization (B(11) = 3)

`projects/bq_closure_lean/RequestProject_q11_realization/` — self-contained Lean
RequestProject, compiles **sorry-free + axiom-clean** locally (direct `lean` elaboration
against prebuilt Mathlib v4.28.0; axiom audit on `lam11_minpoly`, `run11_isClusterRun`,
`clusterCeiling11` all `[propext, Classical.choice, Quot.sound]`).

- Quintic minpoly `λ₁₁⁵ − λ₁₁⁴ − 4λ₁₁³ + 3λ₁₁² + 3λ₁₁ − 1 = 0` reproved via Chebyshev
  `T₁₁(c) = −1` (matches the separately Aristotle-verified `lambda_11_min_poly`).
- Genuine length-3 cluster, witness start `(34/101, 37/101)`, k-pattern `[1,1,(2)]`,
  all valid-domain, predecessor not last-branch (genuine cluster start).

### Methodological catch (recorded so it is not repeated)
A naive `M`-orbit search found a length-4 run from start `(19/61, 22/61)` that satisfies
last-branch + sub-threshold + k=1 at all interior points — but that start FAILS the BCZ
cross-section domain condition `b > 1 − λa` (`b = 0.3607 < 0.4023`) and its orbit leaves
the cross-section: it is a TRANSIENT, not a genuine cluster. B(11) = 3 stands (ground truth
k-pattern `[1,1,2]`; continuous count B₀(11) = 3; scalar gate R(11) = 0 since
ρ_min ≈ 1.0451 > ρ_max ≈ 1.0211 — q=11 is NOT a resonance). LESSON: any per-q realization
witness MUST be checked for cross-section domain-validity AND genuine-cluster-start
(predecessor not last-branch), not merely last-branch + sub-threshold + bracket. The
existing repo q=7 and q=13 witnesses DO satisfy domain-validity (verified this session).

Numeric confirmation: `projects/bq_closure_lean/q11_witness_v2.py` (mpmath dps=60).

---

## 5. Bottom line

- The B(q) theorem's **forward mechanism** (cluster = rotation arc) and the **R3 parity
  gate** are fully machine-verified.
- **R2 realization** is proved for a contiguous block **q ∈ {7..13}** (now including q=11),
  plus B(5)≥3.
- The theorem is NOT globally closed. Two residuals remain: (i) **R2 uniform-all-q**
  (no closed-form witness family — likely stays open), and (ii) the single **R3/R1-upper
  transcendental near-fit** (decidable per-q, uniform analytic-open). These are the same
  two residuals flagged on 2026-06-14; this session shrank R2's per-q gap by one (q=11) and
  recorded the domain-validity correctness check that the realization witnesses require.
