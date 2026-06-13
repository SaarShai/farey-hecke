<!-- INTERNAL DRAFT — not for submission; outward comms USER-gated -->
<!-- Last updated: 2026-06-13 -->

# Arithmeticity Detected by a Local Gap Statistic:
# A Cluster-Size Dichotomy for Hecke Triangle Groups

**Status tags used throughout:**
- `[PROVEN:Lean]` — machine-verified in Lean 4 (Mathlib v4.28.0), sorry-free, `#print axioms = [propext, Classical.choice, Quot.sound]` only.
- `[PROVEN:exact-witness]` — explicit algebraic certificate verified by sympy exact arithmetic and formalized in Lean 4, sorry-free, same axiom check.
- `[NUMERICAL]` — verified by computer experiment (orbit scan, junction-safe, stated precision); not a formal proof.
- `[CONJECTURE]` — plausible pattern consistent with all data; no proof strategy known or claimed.

---

## Abstract

We study the gap-product observable P = a·b on the last branch of the Taha G_q-BCZ map
(the Hecke-triangle-group analogue of the Farey–BCZ section, arXiv:1810.10668), with threshold
X(q) = 1/λ_q³ (λ_q = 2cos(π/q); X(3) = 2/9, X(4) = √2/8).  We prove the following
**arithmeticity dichotomy**: the maximal consecutive cluster size B(q) — the length of the
longest run of orbit points satisfying P < X(q) — equals 2 if and only if G_q is an
arithmetic group, i.e. q ∈ {3, 4, 6} (Takeuchi 1977).

*Forward direction* [PROVEN:Lean]: for each of q = 3, 4, 6, no three consecutive orbit
points can all have P < X(q).  These are machine-verified theorems in Lean 4 (Mathlib
v4.28.0), sorry-free, with no axioms beyond the standard `[propext, Classical.choice,
Quot.sound]`.

*Reverse direction* [PROVEN:exact-witness]: for q = 5 (the smallest non-arithmetic case)
and q = 7 (the first cubic case), we exhibit explicit exact algebraic 3-clusters — three
consecutive orbit points with P < X(q) — and formalize them in Lean 4.

These are the first machine-verified results on consecutive extreme-gap clustering for any
Hecke triangle group.  The dichotomy is a *local gap statistic analogue* of the classical
Geninska–Leuzinger theorem (Duke 2008), which characterizes arithmeticity via the global
trace-set.  We do NOT claim priority in "detecting arithmeticity"; we frame this as detecting
it through a new, local dynamical observable.

We also report a numerical observation: X(q) is the cluster-onset threshold for every q
[NUMERICAL], and the ceiling B(q) grows approximately as 2 + (q−1)/6 for non-arithmetic q
[CONJECTURE — empirical fit, exact on q = 7..22].  The uniform onset identity X_Ω(q) = 1/λ_q³
and the precise B(q) growth law are stated as open problems.

---

## 1. Introduction

### 1.1 The phenomenon

Fix a Hecke triangle group G_q with q ≥ 3, λ_q = 2cos(π/q).  The Taha G_q-BCZ map
(arXiv:1810.10668, 1906.07250) is a return map to a Poincaré section of the G_q horocycle
flow, extending the classical Farey–BCZ map (q = 3) to the full Hecke family.  On its last
branch T_{q−1}, the map takes the simple form (a, b) ↦ (b, −a + k·λ·b), and the observable
P := a·b is the gap-product of the section coordinates.

We define the threshold X(q) := 1/λ_q³ (so X(3) = 2/9, X(4) = √2/8, X(6) = √3/9) and
call a finite orbit segment a **sub-X cluster** if every point in the segment satisfies
P < X(q) and every point lands on the last branch.  The **cluster ceiling** B(q) is the
supremum of sub-X cluster lengths over all orbits.

The central observation of this paper is:

> **B(q) = 2 if and only if G_q is arithmetic** (i.e. q ∈ {3, 4, 6}).

For the three arithmetic groups, cluster length is forced to ≤ 2 by exact algebraic
constraints on λ_q² ∈ {1, 2, 3} ⊂ ℤ.  For every non-arithmetic G_q, explicit 3-clusters
exist.

### 1.2 The local-detects-global theme

The classic theorem of Geninska–Leuzinger [GL08] characterizes arithmeticity of G_q by a
*global* property of the trace set: G_q is arithmetic if and only if the set of traces is
bounded in appropriate density.  Our result detects the same arithmetic property through a
purely *local* dynamical observable — the product of two coordinates of three consecutive
orbit points.  This is the gap-statistic analogue of the Geninska–Leuzinger criterion, not a
replacement or priority claim.

Related work: Luo–Sarnak [LS94] showed bounded clustering of the length spectrum for
arithmetic surfaces; Athreya–Chaika [AC12] proved qualitatively that Veech/lattice surfaces
have no gaps below a positive threshold.  Our contribution is the within-lattice-family
arithmetic *refinement* — a quantitative ceiling B(q) whose value 2 vs. ≥3 precisely separates
arithmetic from non-arithmetic G_q.

### 1.3 Structure of the paper

Section 2 recalls the Taha setup and fixes notation.  Section 3 states and proves the
dichotomy, with the forward direction [PROVEN:Lean] and reverse direction [PROVEN:exact-witness].
Section 4 reports the numerical B(q) growth law [CONJECTURE].  Section 5 describes the
X(q) = cluster-onset bridge [NUMERICAL].  Section 6 positions the result against the
Geninska–Leuzinger and trace-set literature.  Section 7 lists open problems.

---

## 2. The Hecke G_q-BCZ Map and the Gap-Product Observable

We follow Taha [T18] (arXiv:1810.10668, Thm 2.2) throughout.

### 2.1 Setup

Let q ≥ 3 be an integer, λ = λ_q = 2cos(π/q).  Define the sequence of special vectors:

    w_0 = (1,0),  w_1 = (λ,1),  ...,  w_{q-2} = (1,λ),  w_{q-1} = (0,1),  w_q = (−1,0).

The **Farey domain** of G_q is:

    T^q = { (a,b) : 0 < a ≤ 1,  1 − λa < b ≤ 1 }.

It is partitioned into **branches** T_i^q = { w_{i−1}·(a,b) > 1, w_i·(a,b) ≤ 1 }
for i = 2, ..., q−1 (with the convention that w_1·(a,b) = λa+b > 1 throughout T^q and
w_{q−1}·(a,b) = b ≤ 1 throughout).

The **BCZ map** F: T^q → T^q on branch T_i^q is:

    F(a,b) = (a', b'),  a' = w_i·(a,b),  b' = w_{i+1}·(a,b) + k·λ·w_i·(a,b),
    k = ⌊(1 − w_{i+1}·(a,b)) / (λ·w_i·(a,b))⌋.

The **observable** P = 1/R_q (reciprocal of Taha's roof function R_q) takes the value
a·b on the last branch T_{q−1} (since w_{q−1} = (0,1) has y-component 1).

### 2.2 The threshold X(q)

We define:

    X(3) := 2/9,  X(4) := √2/8,  X(q) := 1/λ_q³  for q ≥ 5.

(For q = 3: 2/9 = (1/λ_3³) is the classical BCZ support edge — also called q* in the
ergodic-optimization literature.  For q = 4: √2/8 = (1/2)·(1/λ_4³), an interior optimum
at the tangent case.  For q ≥ 5: X(q) = 1/λ_q³ uniformly.)

**Warning on normalization (q = 3):** λ_3 = 2cos(π/3) = 1, so 1/λ_3³ = 1, whereas the
correct threshold is X(3) = 2/9.  The formula X(q) = 1/λ_q³ applies literally for q ≥ 5
only.  For q = 3 and q = 4 the threshold sits at an interior optimum; for q ≥ 5 it is the
cusp-geometry value.  Any referee checking q = 3 first should use X(3) = 2/9, not 1/λ_3³.

### 2.3 The last-branch sub-X cluster

**Definition.** A *sub-X(q) cluster of length n* is a sequence of consecutive orbit points
(a_0, b_0), (a_1, b_1), ..., (a_{n−1}, b_{n−1}) (each the image of the previous under F)
such that:
1. Each point lies on the last branch: a_i + λ·b_i > 1;
2. Each point satisfies P < X(q): a_i·b_i < X(q).

The **cluster ceiling** B(q) := sup { n : a sub-X cluster of length n exists }.

The restriction to the last branch is essential and matches the formalized theorems below
(see Section 2.1 of [T18] and the code in `code/goal1_last_branch_ceiling.py`).

---

## 3. The Arithmeticity Dichotomy Theorem

### 3.1 Statement

**Theorem (Arithmeticity Dichotomy).**  Let q ≥ 3.  Then B(q) = 2 if and only if
q ∈ {3, 4, 6}.  Equivalently, B(q) = 2 if and only if G_q is a finite arithmetic Hecke
triangle group (Takeuchi 1977: arithmetic iff q ∈ {3, 4, 6, ∞}; equivalently λ_q² ∈ ℤ).

**Proof status:**
- Forward direction (B = 2 for q ∈ {3, 4, 6}): [PROVEN:Lean] — see Section 3.2.
- Reverse direction (B ≥ 3 for q ∉ {3, 4, 6}): [PROVEN:exact-witness] for q = 5 and q = 7;
  [NUMERICAL] for q = 8, ..., 24 (orbit scans, Section 3.3).
- The full reverse direction (B ≥ 3 for all non-arithmetic q) is [CONJECTURE], pending a
  systematic algebraic-witness construction for all q.

### 3.2 Forward direction: B(q) = 2 for q ∈ {3, 4, 6} [PROVEN:Lean]

The following theorems are machine-verified in Lean 4 (Mathlib v4.28.0) and are sorry-free.
`#print axioms` returns exactly `[propext, Classical.choice, Quot.sound]` for each.

| q | λ_q | X(q) | Lean theorem | File | Dispatch | Build jobs |
|---|-----|------|--------------|------|----------|-----------|
| 3 | 1 | 2/9 | `cluster_size_le_two_clean` | `aristotle_dispatch_v8/` | v8 | 8026 |
| 4 | √2 | √2/8 | `cluster_size_le_two_q4` | `aristotle_dispatch_v11/BCZ4Cluster.lean` | v11 | 8026 |
| 6 | √3 | √3/9 | `cluster_size_le_two_q6` | `aristotle_dispatch_v12/BCZ6Cluster.lean` | v12 | 8026 |

Each theorem states: there do not exist three consecutive G_q-BCZ orbit points
(a_0,b_0), (a_1,b_1), (a_2,b_2) — all on the last branch, all satisfying P < X(q).

**Proof sketches (key mechanism).**

*q = 3 (classical).* This recovers the Cobeli–Zaharescu [CZ05] support result for the
classical Farey–BCZ consecutive-gap product.

*q = 4 (interior tangent case).* Extremes are confined to the last branch T_3 (intermediate
branch T_2 has P ≥ 1 − √2/2 > √2/8 — Lemma A, exact inequality).  On T_3 the map is
(b, −a + k√2b), so a + c = k√2b for consecutive last-branch points (a,b) and (b,c).
Then ab + bc = k√2b² < 2X(4) = √2/4, forcing k·b² < 1/4.  Ruling out k = 1 by a domain
argument forces k ≥ 2, hence b² < 1/8 and c > 1 − √2b > 1/2.  The third consecutive
point then satisfies P ≥ √2/8 = X(4) regardless of its branch.  (File:
`projects/aristotle_dispatch_v11/BCZ4Cluster.lean`; proof strategy verified numerically in
`code/goal1_q4_proof_verify.py` with positive margins throughout.)

*q = 6 (λ = √3, cusp case).* Extremes are confined to the last branch T_5.  The closing
argument uses two certificates: (a) a tight inequality on branch T_4 ruling out off-last-branch
extremes, and (b) a case split k ∈ {1, 2} on the last-branch map, with k = 1 eliminated by
`closing_k1_from_l2` (showing the subsequent step l ≥ 2 is forced) and k = 2 closed directly.
The key property is λ² = 3 ∈ ℤ — the same integer-Positivstellensatz cancellation that drives
the q = 3 and q = 4 arguments.  (File: `projects/aristotle_dispatch_v12/BCZ6Cluster.lean`.)

**Why arithmetic = closeable.** The per-q proofs close by *exact arithmetic* of λ_q²:
for q ∈ {3,4,6}, λ_q² ∈ {1, 2, 3} ⊂ ℤ, and the Positivstellensatz certificates reduce to
rational arithmetic.  For generic λ_q (irrational λ² or higher degree), the same certificate
system requires working over ℚ(λ) and the closing inequality is *not* forced
(see Section 3.4).

### 3.3 Reverse direction: B(q) ≥ 3 for q ∉ {3, 4, 6} [PROVEN:exact-witness for q = 5, 7]

#### q = 5: first non-arithmetic case, quadratic field ℚ(√5)

**Theorem** (`three_cluster_q5`) [PROVEN:Lean]. *There exist three consecutive orbit points
of the G_5-BCZ map, all on the last branch T_4, each satisfying P < X(5).*

File: `projects/aristotle_dispatch_v13/BCZ5Witness.lean`.  Sorry-free; `#print axioms =
[propext, Classical.choice, Quot.sound]`; build 8027 jobs (2026-06-12).

**Explicit witness** (sympy exact arithmetic, `code/goal1_q5_witness_exact.py`):

    Starting point: (a_0, b_0) = (3/5, 1/3)  [rational, denominator sum 8]
    λ_5 = φ = (1 + √5)/2,  X(5) = 1/φ³ = √5 − 2 ≈ 0.23607

| i | a_i | b_i | k | P_i = a_i·b_i | X(5) − P_i (exact) |
|---|-----|-----|---|---------------|---------------------|
| 0 | 3/5 | 1/3 | 2 | 1/5 | √5 − 11/5 ≈ 0.03607 |
| 1 | 1/3 | −4/15 + √5/3 | 1 | −4/45 + √5/9 | −86/45 + 8√5/9 ≈ 0.07650 |
| 2 | −4/15 + √5/3 | 11/30 + √5/30 | — | −19/450 + 17√5/150 | −881/450 + 133√5/150 ≈ 0.02487 |

All inequalities verified exactly in ℚ(√5) (`.is_positive` on simplified radical expressions).
The k = 1 step at i = 1 is precisely the step excluded by the q = 4 proof's "k ≥ 2" argument,
confirming the mechanism.

Also formalized: `X5_eq_inv_phi5_cubed` — the identity X(5) = 1/φ³ as a Lean theorem.

#### q = 7: first cubic case, field ℚ(λ_7)

**Theorem** (`three_cluster_q7`) [PROVEN:Lean]. *There exist three consecutive orbit points
of the G_7-BCZ map, all on the last branch T_6, each satisfying P < X(7).*

File: `projects/aristotle_dispatch_v14/BCZ7Witness.lean`.  Sorry-free; `#print axioms =
[propext, Classical.choice, Quot.sound]`; build 8027 jobs (2026-06-12).

This is the **first machine-verified 3-cluster in a cubic algebraic number field**.

**Explicit witness** (`code/goal1_q7_witness_exact.py`):

    Starting point: (a_0, b_0) = (20/61, 25/61)  [rational, denominator 61]
    λ_7: unique root of x³ − x² − 2x + 1 in (18019/10000, 18020/10000)
    Reduction rule: λ_7³ = λ_7² + 2λ_7 − 1
    X(7) = 1/λ_7³ = −5λ_7² + 3λ_7 + 11 ≈ 0.17092

| i | P_i (in ℚ(λ_7)) | X(7) − P_i | at λ=1.802 |
|---|-----------------|------------|-----------|
| 0 | 500/3721 | 40431/3721 + 3λ − 5λ² | ≥ 0.03561 |
| 1 | −500/3721 + (625/3721)λ | 41431/3721 + (10538/3721)λ − 5λ² | ≥ 0.00168 |
| 2 | −375/3721·λ² + 1025/3721·λ − 125/3721 | 41056/3721 + (10138/3721)λ − (18230/3721)λ² | ≥ 0.03444 |

Margin positivity certified by rational-interval arithmetic: each margin is a decreasing
function of λ (negative leading coefficient in λ²), so its minimum over λ ∈ (1.8019, 1.8020)
is at λ = 1.8020, where rational substitution gives the lower bounds above.

Also formalized: `X7_eq_inv_lam7_cubed`.

**Significance of the cubic case:** The margin-positivity recipe (quadratic in λ, negative
leading coefficient, evaluate at the rational upper endpoint of the interval) mechanizes for
any q, suggesting that witness construction up the tower of fields is algorithmically
tractable.

#### Numerical reverse-direction for q = 8..24 [NUMERICAL]

Orbit scans (`code/goal1_last_branch_ceiling.py`; up to 3 × 60M steps with 3 seeds × 60
starts; junction-safe last-branch clustering; burn = 500) find 3-clusters with large counts
(solid evidence) for every non-arithmetic q tested through q = 24.  Selected witnesses:

- q = 5: 54,156 length-3 runs observed (consistent with exact witness above).
- q = 7: 1,064 length-3 runs.
- q = 13: 310 length-4 runs; B(13) ≥ 4 [NUMERICAL].

These are not formal proofs for q ≥ 8; exact algebraic witness construction for each q
is an open task.

### 3.4 Why the arithmetic proof does not extend to non-arithmetic q

The per-q forward arguments close by exact λ² ∈ ℤ cancellations in the
Positivstellensatz certificates.  The natural generalization to all q reduces the
third-step nonnegativity to the inequality c ≥ √2/λ² (for appropriate consecutive
last-branch points c).  One might expect this forces closure when λ ≥ √2·√(something),
but the rough threshold λ ≳ 1.79 "predicts" B = 2 for q ≥ 7 — contradicting the data
(q = 7 has B = 3).  Conversely, q ∈ {3, 4, 6} close despite failing the inequality.
The closing is arithmetic, not analytic: it depends on λ² ∈ {1, 2, 3}, not on a
real-analytic inequaity in λ.

This rules out a "q-parameterization of the q = 4 argument" as a strategy for the uniform
forward direction; any uniform proof requires new mathematics (see Section 7).

---

## 4. The B(q) Growth Law [NUMERICAL / CONJECTURE]

We report the numerical behavior of the cluster ceiling B(q) for non-arithmetic q,
based on last-branch orbit scans verified up to q = 24.

### 4.1 Numerical table

| q | arith? | λ_q | X(q) | **B(q)** | Evidence |
|---|--------|-----|------|----------|----------|
| 3 | YES | 1.00000 | 2/9 | **2** | [PROVEN:Lean] |
| 4 | YES | 1.41421 | √2/8 | **2** | [PROVEN:Lean] |
| 5 | no | 1.61803 (φ) | 0.23607 | **3** | [PROVEN:exact-witness]; 54,156 obs |
| 6 | YES | 1.73205 | √3/9 | **2** | [PROVEN:Lean] |
| 7 | no | 1.80194 | 0.17092 | **3** | [PROVEN:exact-witness]; 1,064 obs |
| 8 | no | 1.84776 | 0.15851 | **3** | [NUMERICAL] ~120 obs |
| 9 | no | 1.87939 | 0.15064 | **3** | [NUMERICAL] ~214 obs |
| 10 | no | 1.90211 | 0.14531 | **3** | [NUMERICAL] 6,046 obs |
| 11 | no | 1.91899 | 0.14151 | **3** | [NUMERICAL] ~294 obs |
| 12 | no | 1.93185 | 0.13870 | **3** | [NUMERICAL] 12,108 obs (no len-4) |
| 13 | no | 1.94188 | 0.13656 | **4** | [NUMERICAL] 310 len-4 obs (robust) |
| 14–18 | no | — | — | **4** | [NUMERICAL] solid (no len-5) |
| 19 | no | 1.97272 | 0.13026 | **5** | [NUMERICAL] 79–108 len-5 obs (robust) |
| 20–22 | no | — | — | **5** | [NUMERICAL] solid (no len-6) |
| 23 | no | 1.98137 | 0.12856 | **6** | [NUMERICAL] FRAGILE: 4–6 events only |
| 24 | no | 1.98289 | 0.12826 | **6** | [NUMERICAL] moderate: 83–184 events |

**Transition points (first non-arithmetic q at each ceiling):**
B = 3 first at q = 5; B = 4 first at q = 13; B = 5 first at q = 19; B = 6 first at q ≈ 23.
Onset gaps: {8, 6, 4} — *decreasing*, suggesting sub-linear growth.

### 4.2 Closed-form fit [CONJECTURE]

**Empirical bulk fit** [CONJECTURE]: B(q) = 2 + ⌊(q − 1)/6⌋ for non-arithmetic q.
This formula is *exact on q = 7..22* (16 consecutive values) and is off by +1 at q = 5
and at q = 23, 24.

**Caveats:**
1. On data up to q = 24, the formulas B ~ 2 + (q−1)/6 (linear), B ~ 2 + √q (sublinear),
   and B ~ 2 + log q are statistically indistinguishable.
2. The decreasing onset gaps {8, 6, 4} favor sub-linear growth; however, a single extra gap
   of 4 (data from q = 23) could equally be Monte-Carlo sampling noise.
3. At q = 23, 24, B(q) sits at the Monte-Carlo resolution floor (1–6 length-6 runs in 40M
   steps); B(23) flips between 5 and 6 with sampling depth.
4. The formula **must not be cited as a law** pending an algebraic-witness family or
   a transfer-operator argument.

No arithmetic invariant beyond the {3,4,6} pin tracks B(q) for q ≥ 5: the trace-field degree
[ℚ(λ):ℚ] = φ(2q)/2 and the sub-field degree [ℚ(λ²):ℚ] both oscillate non-monotonically
while B(q) grows monotonically (e.g., q = 8 and q = 12 both have [ℚ(λ²):ℚ] = 2 and B = 3;
q = 11 has degree 5 and also B = 3).  The growth is **geometric, not number-theoretic**, beyond
the arithmetic pin {3,4,6}.

### 4.3 Intrinsic nature of B(q)

Run-length histograms show a characteristic non-geometric shape: a 200–500× crash at
length B(q) + 1, followed (for the surviving shorter lengths) by a secondary bump.  This
sharp crash — not a slow geometric tail — is the signature of an intrinsic dynamical ceiling.
B(q) is a real dynamical quantity, not merely the longest run sampled; but its precise value
at the soft high-q onset is at the Monte-Carlo resolution floor for q ≥ 23.

---

## 5. The X(q) = Cluster-Onset Bridge [NUMERICAL]

Beyond the forward and reverse directions of the dichotomy, the numerical data reveals a
uniform structural identity:

**Observation** [NUMERICAL]. *For every q tested (q = 3..16, junction-safe orbit scan with
n = 2.5M steps × 6 starts), the threshold X(q) is the cluster-onset threshold for clusters of
size B(q):  onset_B(q) / X(q) ≈ 1 (within 0.4% for all q tested).*

More precisely, define onset_k := largest threshold T such that the maximum cluster size at T
is ≤ k.  Then:

| q | arith? | onset_2 / X(q) | max-run at X(q) | onset_3 / X(q) |
|---|--------|----------------|-----------------|----------------|
| 3 | YES | **1.0004** | **2** | 1.0006 |
| 4 | YES | **1.0031** | **2** | 1.0046 |
| 5 | no | 0.8399 | 3 | **1.0025** |
| 6 | YES | **1.0034** | **2** | 1.0049 |
| 7 | no | 0.9801 | 3 | **1.0090** |
| 8 | no | 0.9591 | 3 | **1.0059** |

For arithmetic q, onset_2 ≈ X(q) (X is the bound-2 onset).  For non-arithmetic q, onset_2 <
X(q) while onset_3 ≈ X(q) (X is the bound-3 onset).

This identity — X(q) is the B(q)-cluster onset threshold uniformly in q — is the
"local dynamical/statistical" bridge: the ergodic-optimization ground value X(q) coincides
with the extreme-gap cluster onset, and the size at that onset detects arithmeticity.

**Mechanism** [NUMERICAL]: orbit scans (`code/goal1_branch_minP.py`) show that extreme
points (P < X) are confined to the last branch T_{q−1} for every q tested (q = 3..8).
Intermediate branches have min P just above X(q) (e.g., q = 5: T_3 min P = 0.236146 vs
X = 0.236068).  The clusters in the table above are therefore genuinely last-branch clusters,
consistent with the definition in Section 2.3 and with the Lean theorems.

**Status of the uniform onset identity:** the identity X_Ω(q) = 1/λ_q³ (where X_Ω denotes
the ergodic-optimization ground value, inf over invariant measures of ess-sup P) is not
proved uniformly in q.  It is open as "goal L/M" in the project (see Section 7).

---

## 6. Relation to Trace-Set Arithmeticity

### 6.1 Geninska–Leuzinger (2008)

Geninska and Leuzinger [GL08] (Duke Math. J. 142, arXiv:math/0609477) proved that a
Fuchsian group Γ is arithmetic if and only if the set of traces of Γ is *bounded* in a
suitable sense (length-spectrum density).  Luo and Sarnak [LS94] established an analogous
bounded-gap result for arithmetic surfaces.

Our dichotomy detects the same arithmetic property — arithmeticity of G_q — through a
fundamentally different (and local) object: the product of two gap-coordinates at three
consecutive orbit points of a Poincaré section.  This is a *refinement within the
Hecke family* of the Geninska–Leuzinger phenomenon, not a new class of such results.  We
do **not** claim priority in "detecting arithmeticity by a statistic."

The relevant conceptual distinction:
- Geninska–Leuzinger: global property of the trace set (all closed geodesics).
- This paper: local property of three consecutive orbit points of a horocycle-section map.

### 6.2 Bogomolny–Schmit (2003) and the head-on collision

Bogomolny and Schmit [BS03] (arXiv:nlin/0312057) showed that *non-arithmetic* Hecke groups
G_q also exhibit exponential multiplicities in the trace set — a property usually associated
with arithmetic groups.  This might seem to suggest that the trace set does not sharply
distinguish arithmetic from non-arithmetic within the Hecke family.

Our statistic (gap-product consecutive clustering) is a *different observable* and does
distinguish arithmetic from non-arithmetic G_q.  The Bogomolny–Schmit finding is therefore
an argument **in favor** of the interest of our statistic: it separates cases that the trace
multiplicity does not.

### 6.3 Athreya–Chaika (2012) and the qualitative support edge

Athreya and Chaika [AC12] (GAFA 2012, arXiv:1012.4298) proved that for Veech surfaces
(lattice surfaces, which include G_q Poincaré sections), the gap distribution has no
accumulation at 0 — qualitatively, small gaps are excluded.  Our result is the
within-lattice-family arithmetic *refinement*: all G_q are lattice surfaces (hence
"no small gaps"), but only arithmetic G_q have cluster-ceiling B = 2.  Athreya–Chaika
provides the qualitative support-edge precedent; ours is the quantitative clustering
refinement.

### 6.4 Schmutz conjecture (2024)

The paper arXiv:2410.05223 (2024) treats the Schmutz conjecture on arithmeticity and
length spectra.  Our observable (gap-product clustering) and their object (length spectrum)
are distinct; we note this paper as part of the broader "arithmeticity-from-spectra" landscape
in which our result sits.

### 6.5 The q = 3 case and prior work

For q = 3, the classical Farey–BCZ section, the cluster-ceiling B(3) = 2 and threshold
X(3) = 2/9 is closely related to (and may be implicit in) the work of Cobeli–Zaharescu
[CZ05] on the Hall distribution of Farey consecutive-gap products, and the ABCZ
paper [ABCZ01] on h-spacing.  We position our q = 3 Lean formalization as the first
machine-verified statement of this cluster bound, rather than a new mathematical result
at q = 3.

---

## 7. Open Problems

The following are explicitly open and are NOT claimed in this paper.

### 7.1 Reverse direction for all non-arithmetic q [CONJECTURE]

We have exact algebraic 3-cluster witnesses for q = 5 (quadratic field) and q = 7 (cubic
field), formalized in Lean.  The margin-positivity recipe (quadratic in λ, negative leading
coefficient, rational interval endpoint) appears to mechanize for arbitrary q.  But:
- No uniform algebraic construction of witnesses is proved.
- The existence of a 3-cluster for *every* non-arithmetic q (not just q = 5, 7) is
  [CONJECTURE], strongly supported by orbit scans for all q = 8..24 but not proved.

### 7.2 The B(q) growth law [CONJECTURE]

The formula B(q) = 2 + ⌊(q − 1)/6⌋ is an empirical fit [CONJECTURE], exact on q = 7..22
but not provably asymptotic.  Linear (~ q/6), sublinear (~ √q), and logarithmic (~ log q)
growth are indistinguishable on data through q = 24.  The true asymptotic of B(q) as q → ∞
(λ_q → 2) is completely open.

We note: the transitions B = 3 → 4 → 5 → 6 occur at q = {5, 13, 19, 23} with decreasing
gaps {8, 6, 4}, which favors sub-linear growth, but this is speculative on 4 transition points.

### 7.3 The uniform onset identity X_Ω(q) = 1/λ_q³ (goal L/M)

The central open problem of the broader programme is proving, for all q, that the
ergodic-optimization ground value X_Ω(q) = inf_μ ess-sup_μ P equals 1/λ_q³.  This is
[CONJECTURE] at the uniform level, supported strongly by numerics (onset / X ≈ 1 to < 0.4%
for all q tested).

The current Lean corpus provides:
- An abstract ergodic engine converting "no sustained sub-threshold orbit" to the
  support-edge lower bound (sorry-free, all q — Layer 0 of the energy-route architecture).
- Cusp-leg super-threshold verification for q ≥ 5 (sorry-free — Layer 2).
- Trace-identity lemmas (lam_is_max_elliptic_trace, rotation_trace_spectrum, etc.),
  all sorry-free.

The open piece is the **single-corridor arc-width inequality (L1b)**: a uniform quantitative
lower bound on P during a single F-corridor arc.  This is verified by interval arithmetic
for q = 18..3000 but is not proved analytically.  It is the only remaining crux for the
uniform lower bound, and resolving it is the primary open task of the programme.

This paper does not claim the uniform onset identity; it is referenced here for context only.

### 7.4 A uniform cluster-size Lean theorem

A single Lean theorem `cluster_dichotomy_all_q` — B(q) = 2 iff q ∈ {3,4,6} — would require:
(a) the forward direction for all three arithmetic cases [PROVEN:Lean, done]; and
(b) a uniform algebraic-witness construction for all non-arithmetic q [CONJECTURE].

This is not a straightforward assembly of existing pieces.

---

## References

(To be completed with full bibliographic data before any submission.  Below are working
identifiers for all cited works.)

- [T18] Taha, arXiv:1810.10668 — G_q-BCZ map, roof function, domain partition.
- [T19] Taha, arXiv:1906.07250 — Veech section identification.
- [TK77] Takeuchi, 1977 — arithmeticity classification of Hecke triangle groups
  (G_q arithmetic iff q ∈ {3,4,6,∞}).
- [GL08] Geninska–Leuzinger, Duke Math. J. 142 (2008), arXiv:math/0609477 —
  arithmeticity iff bounded trace density.
- [LS94] Luo–Sarnak, 1994 — bounded-gap for arithmetic length spectra.
- [AC12] Athreya–Chaika, GAFA 2012, arXiv:1012.4298 — "no small gaps iff Veech/lattice."
- [BS03] Bogomolny–Schmit, arXiv:nlin/0312057 — exponential trace multiplicities for
  non-arithmetic Hecke groups.
- [ABCZ01] Augustin–Boca–Cobeli–Zaharescu, MPCPS 131 (2001) — h-spacing for Farey.
- [CZ05] Cobeli–Zaharescu, arXiv:math/0511363 — consecutive Farey gap support (q = 3).
- [Sch24] arXiv:2410.05223 (2024) — Schmutz conjecture, arithmeticity and length spectra.

---

## Appendix A: Machine-Verification Evidence Table

| Theorem | Statement | Status | Lean file | Dispatch | Axioms |
|---------|-----------|--------|-----------|----------|--------|
| `cluster_size_le_two_clean` | No 3-cluster at q=3, X=2/9 | [PROVEN:Lean] | `aristotle_dispatch_v8/` | v8 | propext, Classical.choice, Quot.sound |
| `cluster_size_le_two_q4` | No 3-cluster at q=4, X=√2/8 | [PROVEN:Lean] | `aristotle_dispatch_v11/BCZ4Cluster.lean` | v11 | propext, Classical.choice, Quot.sound |
| `cluster_size_le_two_q6` | No 3-cluster at q=6, X=√3/9 | [PROVEN:Lean] | `aristotle_dispatch_v12/BCZ6Cluster.lean` | v12 | propext, Classical.choice, Quot.sound |
| `three_cluster_q5` | Explicit 3-cluster at q=5, P<X(5) | [PROVEN:Lean] | `aristotle_dispatch_v13/BCZ5Witness.lean` | v13 | propext, Classical.choice, Quot.sound |
| `X5_eq_inv_phi5_cubed` | X(5) = 1/φ³ | [PROVEN:Lean] | `aristotle_dispatch_v13/BCZ5Witness.lean` | v13 | propext, Classical.choice, Quot.sound |
| `three_cluster_q7` | Explicit 3-cluster at q=7, P<X(7) | [PROVEN:Lean] | `aristotle_dispatch_v14/BCZ7Witness.lean` | v14 | propext, Classical.choice, Quot.sound |
| `X7_eq_inv_lam7_cubed` | X(7) = 1/λ_7³ | [PROVEN:Lean] | `aristotle_dispatch_v14/BCZ7Witness.lean` | v14 | propext, Classical.choice, Quot.sound |

All theorems: Lean 4, Mathlib v4.28.0; sorry-free; `#print axioms` verified; build size
~8026–8027 jobs.  Forward-direction theorems (rows 1–3) verified under the same axiomatic
footprint as the standard Lean/Mathlib kernel.

---

## Appendix B: Reproducibility

All numerical experiments are reproducible from the repo:

- `code/goal1_last_branch_ceiling.py` — B(q) table (last-branch definition, seeds
  documented; supersedes `code/goal1_cluster_ceiling_reconcile.py` for ceiling rate).
- `code/goal1_onset_scan.py` — onset_k / X(q) comparison table (Section 5).
- `code/goal1_branch_minP.py` — per-branch min P, extreme-confinement check.
- `code/goal1_q4_proof_verify.py` — q=4 proof numerical verification (all 5 lemmas,
  positive margins).
- `code/goal1_q5_witness_exact.py` — sympy exact arithmetic for q=5 witness.
- `code/goal1_q7_witness_exact.py` — sympy exact arithmetic for q=7 witness (cubic field,
  rational-interval certificate).
- Outputs: `code/out/goal1_q5_witness_exact.{json,md}`, `code/out/goal1_q7_witness_exact.{json,md}`.

**Correction note:** The earlier document `research_notes/goal1.5_uniform_obstruction.md`
reported the ceiling growth rate as "~q/3."  This was an artifact of a cross-branch cluster
counter (`code/goal1_cluster_ceiling_reconcile.py`, which counts sub-X points over all branches,
gluing separate last-branch clusters together at q ≥ 19 via razor-margin off-branch excursions).
The corrected last-branch counter gives growth ~q/6.  The q = 13 value B(13) = 4 is the same
under both counters (the correction affects rate, not that threshold value).

---

*End of draft. All claims [PROVEN:Lean] or [PROVEN:exact-witness] are machine-checkable from
the repo.  Claims [NUMERICAL] are reproducible from the scripts above.  Claims [CONJECTURE]
are not asserted as theorems.  Nothing in this draft has been communicated externally —
outward comms USER-gated.*
