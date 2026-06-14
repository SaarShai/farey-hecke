<!-- INTERNAL DRAFT — not for submission; outward comms USER-gated. -->
<!-- Prepared 2026-06-13 (Goal-3). Supersedes research_notes/PAPER_DRAFT_arithmeticity_dichotomy.md. -->
<!-- Every claim is tagged. Numerics re-verified 2026-06-13 against the exact witness ladder (q=5..24). -->

# Arithmeticity Detected by a Local Gap Statistic:
# A Cluster-Size Dichotomy for Hecke Triangle Groups

---

**Provenance / status tags used throughout.** Every mathematical assertion carries exactly one
of the following tags. Nothing in this manuscript is communicated externally; all outward
communication is gated on explicit author approval.

- `[PROVEN:Lean]` — machine-verified in Lean 4 (Mathlib v4.28.0), sorry-free, with
  `#print axioms` returning exactly `[propext, Classical.choice, Quot.sound]` (no axiom stubs,
  no `native_decide`).
- `[PROVEN:exact-witness]` — an explicit algebraic certificate, verified by exact symbolic
  arithmetic over the number field ℚ(λ_q) (sympy algebraic-number arithmetic; no floating point;
  λ_q located by a rational-interval minimal-polynomial sign certificate). For q = 5 and q = 7
  the certificate is *additionally* formalized in Lean 4 under the `[PROVEN:Lean]` footprint.
- `[NUMERICAL]` — established by computer experiment (junction-safe orbit scan at stated depth);
  not a formal proof. Used here only for *upper* bounds on B(q) (i.e. "no longer cluster was
  found") and for the onset-ratio table.
- `[CONJECTURE]` — a pattern consistent with all data, with no proof strategy claimed.
- `[REFUTED]` — a previously-stated empirical pattern now *disproven* by later verified data;
  retained only as a cautionary record, never to be cited as a result.

---

## Abstract

Fix an integer q ≥ 3 and the Hecke triangle group G_q, with λ_q = 2 cos(π/q). On the last
branch of the Taha G_q–BCZ map — the Hecke-family analogue of the Farey–BCZ Poincaré section
(Taha, arXiv:1810.10668) — the map takes the uniform form (a, b) ↦ (b, −a + kλ_q b), and the
gap-product observable is P = a·b. Let X(q) be the ergodic-optimization edge value:
X(3) = 2/9, X(4) = √2/8, and X(q) = 1/λ_q³ for q ≥ 5. Define the *cluster ceiling* B(q) as the
maximal length of a run of consecutive last-branch orbit points all satisfying P < X(q).

We establish the following **arithmeticity dichotomy**:

> **B(q) = 2 if and only if G_q is arithmetic, i.e. q ∈ {3, 4, 6}** (Takeuchi 1977).

*Forward direction* (B(q) = 2 for q ∈ {3, 4, 6}) is `[PROVEN:Lean]`: for each arithmetic q,
a sorry-free Lean 4 theorem rules out any three consecutive last-branch points with P < X(q).
*Reverse direction* (B(q) ≥ 3 for non-arithmetic q) is `[PROVEN:exact-witness]` for every
q = 5, 7, 8, …, 24: explicit algebraic 3-clusters (and longer) certified by exact arithmetic
in ℚ(λ_q); the q = 5 and q = 7 cases are additionally Lean-formalized. Hence the dichotomy is
**proven outright on 3 ≤ q ≤ 7** (both directions), with the reverse direction additionally
certified by exact witnesses up to q = 24; that B(q) ≥ 3 for *all* non-arithmetic q is
`[CONJECTURE]`.

We position this honestly as the **machine-verified, local-gap-statistic instance** of the
classical Luo–Sarnak bounded-clustering program and the Geninska–Leuzinger characterization of
arithmeticity by the *global* trace set (Duke 2008); we do **not** claim a new arithmeticity
criterion, and we do not claim to be the first statistic to detect arithmeticity. For the
*non-arithmetic* family the cluster ceiling B(q) **grows** (asymptotic slope ≈ 0.216 q), and we
explain this growth by an exact **rotation-arc mechanism**: the floor-1 last-branch map is the
elliptic rotation by π/q of the conserved energy form E = a² − λ_q a b + b², and a cluster is a
run of consecutive sub-threshold rotation-lattice points on one energy ellipse (k-pattern
[1,…,1,2]), verified at 100% (34/34) against the genuine map for q = 7..40. We show plainly that
B(q) admits **no continuous closed form**, for a precise reason — an arithmetic
lattice-vs-notch resonance (the discrete π/q rotation can hop a sub-(π/q)-wide super-threshold
notch on the ellipse; e.g. q = 23 fits 6). The uniform onset identity X(q) = cluster-onset
threshold is a `[NUMERICAL]` observation, and the uniform ergodic-optimization identity
X_Ω(q) = 1/λ_q³ is OPEN (in progress; see §7).

---

## 1. Introduction

### 1.1 The local-detects-global hook

A recurring theme in homogeneous dynamics is that *arithmeticity* — a global, rigidity-type
property of a lattice — leaves fingerprints on *local* spacing statistics of its orbits.
The classical instance is the trace (length) spectrum. Luo–Sarnak [LS95] introduced the
**Bounded-Clustering Property (BCP)** of the length spectrum and conjectured (Sarnak) that BCP
characterizes arithmeticity among Fuchsian groups; Geninska–Leuzinger [GL08] **proved Sarnak's
conjecture for cofinite Fuchsian groups with parabolics** — which is *exactly* the cusped Hecke
case G_q — so that such a group is arithmetic iff its trace set satisfies BCP. These are global
statements — over *all* closed geodesics, *all* traces.

This paper exhibits an arithmeticity fingerprint of a different, strictly *local* kind: it is
read off from **three consecutive points** of a single orbit of a Poincaré-section return map.
The observable is the product P = a·b of the two section coordinates (a "gap product"), the
analogue across the Hecke family of the classical Farey consecutive-gap product. The statistic
is the maximal length B(q) of a consecutive run on which P stays below the ergodic-optimization
edge X(q). Our main result is that B(q) detects arithmeticity exactly:

> **Theorem (Arithmeticity Dichotomy).** For q ≥ 3, B(q) = 2 ⟺ q ∈ {3, 4, 6}
> ⟺ G_q is arithmetic ⟺ λ_q² ∈ ℤ.

### 1.2 The result, and what is proven

The dichotomy has two halves, with the following honest proof status:

- **Forward** (arithmetic ⇒ ceiling 2): for each q ∈ {3, 4, 6}, there is *no* run of three
  consecutive last-branch orbit points all with P < X(q). `[PROVEN:Lean]` — three sorry-free
  Lean 4 theorems (§3.2).
- **Reverse** (non-arithmetic ⇒ ceiling ≥ 3): for every q in 5, 7, 8, …, 24, there is an
  explicit algebraic 3-cluster (longer for larger q). `[PROVEN:exact-witness]` (§3.3); q = 5, 7
  additionally `[PROVEN:Lean]`.

Combining, the "if and only if" is **proven (both directions) for 3 ≤ q ≤ 7**, and the reverse
implication is exact-witness-certified through q = 24. The statement "B(q) ≥ 3 for *every*
non-arithmetic q" is `[CONJECTURE]` (the exact witnesses cover q ≤ 24 only).

### 1.3 Honest novelty (what is and is not new)

The phenomenon "bounded clustering ⟺ arithmetic" is **not new**: it is the Luo–Sarnak [LS95]
Bounded-Clustering-Property program, proved for the cusped Fuchsian (= Hecke) case by
Geninska–Leuzinger [GL08]; and the specific pin B(q) = 2 ⟺ q ∈ {3, 4, 6} is Takeuchi's [TK77]
classification of the arithmetic Hecke triangle groups. We do **not** claim a new arithmeticity
criterion, nor to be the first to detect arithmeticity by a statistic. Our contribution is
exactly two things, stated honestly:

- **(a) A machine-verified forward dichotomy + exact witnesses.** The forward direction
  (B(q) = 2 for the arithmetic q ∈ {3, 4, 6}) is, to our knowledge, the *first formal (Lean 4,
  sorry-free, axiom-clean) proof* of an instance of the bounded-clustering ⟺ arithmetic
  phenomenon, here for the local gap-product statistic; the reverse direction is certified by
  exact algebraic 3-cluster witnesses (q = 5, 7 additionally Lean-formalized) and an exact
  witness ladder q = 5..24.
- **(b) The rotation-arc mechanism for the growth, and the lattice-vs-notch resonance.** For
  non-arithmetic q we identify the *exact mechanism* generating the cluster ceiling: the floor-1
  last-branch map is the elliptic rotation by π/q of the conserved form E = a² − λ_q a b + b²,
  and B(q) is a discrete count of consecutive sub-threshold rotation-lattice points on one
  energy ellipse (§4, and `research_notes/Bq_rotation_arc_2026-06-14.md`). This mechanism
  explains *why B(q) has no continuous closed form* — an arithmetic lattice-vs-notch resonance —
  a positive structural finding rather than a gap. The rotation/conserved-form half is itself
  Lean-verified (`BCZHeckeNoInfiniteRotation_allq_VERIFIED.lean`, namespace `HeckeNoRot`).

We note in passing that the local statistic separates cases the trace *multiplicity* does not:
Bogomolny–Schmit [BS03] showed *non-arithmetic* Hecke groups also exhibit the exponential trace
multiplicities usually taken as an arithmeticity marker, whereas the gap-product clustering does
distinguish those same non-arithmetic G_q (§6.2).

### 1.4 Structure

§2 fixes the Taha setup, the observable P, and the threshold X(q) (with an explicit warning on
the q = 3 normalization). §3 states and proves the dichotomy. §4 describes the B(q) growth
story — the exact rotation-arc mechanism, the lattice-vs-notch resonance, and why there is no
continuous closed form. §5 describes the X(q) = cluster-onset bridge. §6 positions the result against the trace-set
literature. §7 lists open problems, including the uniform onset identity. Two appendices give
the machine-verification table and reproducibility notes; a third records the one cross-program
byproduct (Farey critical hyperuniformity) as a remark.

---

## 2. The Hecke G_q–BCZ Map, the Observable P, and the Threshold X(q)

We follow Taha [T18] (arXiv:1810.10668, Thm 2.2).

### 2.1 The Taha setup

Let q ≥ 3 be an integer and λ = λ_q = 2 cos(π/q). With U_q = [[λ, −1], [1, 0]], the special
vectors w_i = U_q^i (1, 0)ᵀ are

    w_0 = (1, 0),  w_1 = (λ, 1),  …,  w_{q−2} = (1, λ),  w_{q−1} = (0, 1),  w_q = (−1, 0).

The **G_q-Farey domain** is T^q = { (a, b) : 0 < a ≤ 1, 1 − λa < b ≤ 1 }, partitioned into
branches T_i^q = { w_{i−1}·(a, b) > 1, w_i·(a, b) ≤ 1 }, i = 2, …, q−1 (with
w_1·(a, b) = λa + b > 1 throughout T^q and w_{q−1}·(a, b) = b ≤ 1 throughout). The **BCZ map**
F : T^q → T^q acts on branch T_i^q by

    F(a, b) = (a′, b′),  a′ = w_i·(a, b),  b′ = w_{i+1}·(a, b) + k·λ·w_i·(a, b),
    k = ⌊ (1 − w_{i+1}·(a, b)) / (λ · w_i·(a, b)) ⌋.

The **observable** is P = 1/R_q, the reciprocal of Taha's roof function R_q (small P ⇔ large
gap). On branch T_i^q, P = a · (w_i·(a, b)) / y_i where w_i = (x_i, y_i).

### 2.2 The last branch is uniform in q

Because w_{q−2} = (1, λ) and w_{q−1} = (0, 1), the last branch is
T_{q−1} = { a + λb > 1 }, and there the map collapses to the **classical-shaped**

    F(a, b) = (b, −a + kλb),  k = ⌊ (1 + a) / (λb) ⌋,   and   P = a·b.

Thus the last-branch sub-dynamics is *the same map for every q*, parameterized only by λ. This
is the structural reason the q = 3 Farey theory governs the whole family on its extreme branch,
and it is why the entire analysis (Lean proofs and witnesses alike) lives on T_{q−1}.

### 2.3 The threshold X(q) and a warning on the q = 3 normalization

We set

    X(3) := 2/9,   X(4) := √2/8,   X(q) := 1/λ_q³   for q ≥ 5.

`[NUMERICAL]/[PROVEN:exact-witness]` Each X(q) is the ergodic-optimization edge value (the
value the longest sub-X cluster hugs from below; §5). The closed form 1/λ_q³ holds *literally
only for q ≥ 5*, and the q = 3, 4 entries require care:

- **q = 3 (normalization warning).** λ_3 = 2 cos(π/3) = 1, so 1/λ_3³ = 1 — but the correct
  threshold is X(3) = 2/9 (the classical Farey support edge, also denoted q* in the
  ergodic-optimization literature). A referee verifying q = 3 first must use **X(3) = 2/9, not
  1/λ_3³ = 1.** The two coincide *only* in the formal limit; at q = 3 the edge is interior.
- **q = 4 (interior optimum).** 1/λ_4³ = √2/4, whereas X(4) = √2/8 = (1/2)·(1/λ_4³): exactly
  half the cusp value. q = 4 is the tangent case, where X sits at an interior optimum rather
  than the cusp-geometry value.
- **q = 6.** Here X(6) = √3/9 = 1/λ_6³ exactly — the unique arithmetic q at which the closed
  form already holds. (Verified: √3/9 = 0.1924500897… = 1/(√3)³.)
- **q ≥ 5.** X(q) = 1/λ_q³ uniformly (cusp-geometry value). In particular
  X(5) = 1/φ³ = √5 − 2 (φ the golden ratio), verified exactly.

### 2.4 The last-branch sub-X cluster

**Definition.** A *sub-X(q) cluster of length n* is a sequence of consecutive orbit points
(a_0, b_0), …, (a_{n−1}, b_{n−1}) (each the F-image of the previous) such that, for every i:
(i) the point lies on the last branch, a_i + λ b_i > 1; and (ii) P = a_i·b_i < X(q). The
**cluster ceiling** is B(q) := sup{ n : a sub-X cluster of length n exists }.

The last-branch restriction is essential: it is exactly the object the Lean theorems bound and
the witnesses realize, and it is the correct counter (see the correction in Appendix B —
the earlier cross-branch counter inflated the growth rate twofold). For every q tested, the
extreme points (P < X) are *confined* to the last branch (§5, Mechanism), so the restriction is
not a loss of generality in practice.

---

## 3. The Arithmeticity Dichotomy Theorem

### 3.1 Statement and proof status

**Theorem (Arithmeticity Dichotomy).** Let q ≥ 3. Then

    B(q) = 2   ⟺   q ∈ {3, 4, 6}   ⟺   G_q arithmetic   ⟺   λ_q² ∈ ℤ.

(Takeuchi 1977 [TK77]: G_q is arithmetic iff q ∈ {3, 4, 6, ∞}, equivalently
λ_q ∈ {1, √2, √3, 2}, equivalently λ_q² ∈ {1, 2, 3} ⊂ ℤ among finite q.)

**Proof status (honest).**
- **Forward** (B(q) = 2 for q ∈ {3, 4, 6}): `[PROVEN:Lean]` (§3.2). For each arithmetic q,
  a sorry-free Lean 4 theorem proves no three consecutive last-branch points all satisfy
  P < X(q); hence B(q) ≤ 2, and B(q) = 2 since 2-clusters exist.
- **Reverse** (B(q) ≥ 3 for non-arithmetic q): `[PROVEN:exact-witness]` for each
  q = 5, 7, 8, …, 24 (§3.3); q = 5, 7 additionally `[PROVEN:Lean]`.
- **Combined "iff":** PROVEN for 3 ≤ q ≤ 7 (every q in range, both directions). For
  8 ≤ q ≤ 24 the reverse implication is exact-witness-certified; the forward implication is
  vacuous there (no further arithmetic q exist below ∞).
- **B(q) ≥ 3 for *all* non-arithmetic q:** `[CONJECTURE]` (exact witnesses reach q = 24 only;
  strongly supported by orbit scans beyond).

### 3.2 Forward direction: B(q) = 2 for q ∈ {3, 4, 6} `[PROVEN:Lean]`

The following are sorry-free Lean 4 theorems (Mathlib v4.28.0); `#print axioms` returns exactly
`[propext, Classical.choice, Quot.sound]` for each.

| q | λ_q | X(q) | Lean theorem | File | Build |
|---|-----|------|--------------|------|-------|
| 3 | 1 | 2/9 | `cluster_size_le_two_clean` | `projects/aristotle_dispatch_v8/` | 8026 jobs |
| 4 | √2 | √2/8 | `cluster_size_le_two_q4` | `projects/aristotle_dispatch_v11/BCZ4Cluster.lean` | 8026 jobs |
| 6 | √3 | √3/9 = 1/λ³ | `cluster_size_le_two_q6` | `projects/aristotle_dispatch_v12/BCZ6Cluster.lean` | 8026 jobs |

Each theorem states: there do not exist three consecutive last-branch G_q–BCZ orbit points
all with P < X(q).

**Mechanism (q = 4, the cleanest tangent case).** Extremes are confined to the last branch
T_3: on the intermediate branch T_2, with s = a + √2 b, the domain gives a + s > √2 and
(1 − a)(1 − s) ≥ 0, so P = a·s/√2 ≥ (√2 − 1)/√2 = 1 − √2/2 > √2/8 (Lemma A, exact). On T_3 the
map is (b, −a + k√2 b), so a + c = k√2 b for consecutive points (a, b), (b, c); positivity
forces k ≥ 1. Then ab + bc = b(a + c) = k√2 b² < 2X(4) = √2/4, i.e. k·b² < 1/4. Ruling out
k = 1 by a domain squeeze (k = 1 forces b > 1/2, contradicting b² < 1/4) gives k ≥ 2, hence
b² < 1/8 and c > 1 − √2 b > 1/2. The third point then satisfies P ≥ √2/8 = X(4) on either
branch. Each inequality was independently checked numerically with positive margins
(`code/goal1_q4_proof_verify.py`; observed min k = 3, min c ≈ 0.596 > 1/2, third-point
P − X ≥ 0.155).

**Mechanism (q = 6).** Same architecture, λ = √3, X = √3/9 = 1/λ³: extremes confined to T_5;
the closing argument uses a tight T_4 inequality (`lemA4`) plus a case split k ∈ {1, 2} on the
last-branch map, with k = 1 eliminated via `closing_k1_from_l2` (the next step l ≥ 2 is forced)
and k = 2 closed directly.

**Why arithmetic = closeable.** For q ∈ {3, 4, 6}, λ_q² ∈ {1, 2, 3} ⊂ ℤ, so the
Positivstellensatz certificates reduce to *rational* arithmetic and the closing inequalities
cancel exactly. For generic λ_q (λ² irrational or of higher degree), the same certificate
system must be run over ℚ(λ) and the closing inequality is no longer forced — see §3.4. The
closing is **arithmetic, not analytic**: it depends on λ² ∈ ℤ, not on a real inequality in λ.

### 3.3 Reverse direction: B(q) ≥ 3 for non-arithmetic q `[PROVEN:exact-witness]`

For each non-arithmetic q we exhibit an explicit cluster from a rational starting point
(a_0, b_0), with all subsequent points algebraic in ℚ(λ_q). For every point the following are
verified by **exact symbolic arithmetic** (sympy algebraic-number arithmetic; no floating
point): (1) domain membership 0 < a ≤ 1 and b > 1 − λa; (2) last-branch condition a + λb > 1;
(3) sub-threshold P = a·b < X(q) = 1/λ_q³ (strict); (4) the floor index k via both k ≤ ratio
and ratio < k + 1. The irrational λ_q is pinned by a rational-interval certificate (the
minimal polynomial changes sign across the two rational endpoints). Re-verified 2026-06-13:
both ladder scripts reproduce with **no failures**.

| q | field deg [ℚ(λ_q):ℚ] | minpoly | start (a_0, b_0) | cluster len | k-pattern | min margin X − P | source |
|---|---|---|---|---|---|---|---|
| 5 | 2 | x²−x−1 | (3/5, 1/3) | 3 | (2, 1) | √5 − 11/5 ≈ 0.0361 | Lean v13 + sympy |
| 7 | 3 | x³−x²−2x+1 | (20/61, 25/61) | 3 | (1, 1) | ≈ 0.00168 | Lean v14 + sympy |
| 8 | 4 | x⁴−4x²+2 | (1/3, 13/33) | 3 | (1, 1) | 3.08e−3 | sympy ladder |
| 9 | 3 | x³−3x−1 | (1/3, 8/21) | 3 | (1, 1) | 4.88e−3 | sympy ladder |
| 10 | 4 | x⁴−5x²+5 | (1/3, 3/8) | 3 | (1, 1) | 2.82e−3 | sympy ladder |
| 11 | 5 | x⁵−x⁴−4x³+3x²+3x−1 | (1/3, 10/27) | 3 | (1, 1) | 1.73e−3 | sympy ladder |
| 12 | 4 | x⁴−4x²+1 | (1/3, 11/30) | 3 | (1, 1) | 1.20e−3 | sympy ladder |
| 13 | 6 | x⁶−x⁵−5x⁴+4x³+6x²−3x−1 | (31/94, 17/47) | **4** | (1, 1, 1) | 1.74e−3 | sympy ladder (first 4-cluster) |
| 14–18 | — | — | — | 4 | (1,…) | ≥ 7.2e−4 | sympy ladder |
| 19 | 9 | (deg 9) | (33/100, 7/20) | **5** | (1, 1, 1, 1) | 1.07e−4 | sympy ladder (first 5-cluster) |
| 20–22 | — | — | — | 5 | (1,…) | ≥ 2.1e−4 | sympy ladder |
| 23 | 11 | (deg 11) | (100/303, 35/101) | **6** | (1, 1, 1, 1, 1) | 1.58e−4 | sympy ladder (first 6-cluster) |
| 24 | 8 | x⁸−8x⁶+20x⁴−16x²+1 | (43/130, 9/26) | 6 | (1, 1, 1, 1, 1) | 3.81e−4 | sympy ladder |

In every row the witnessed length is a strict lower bound on B(q) certified by exact arithmetic;
that B(q) is not *larger* is a separate `[NUMERICAL]` claim (§4). Two illustrative witnesses
in full:

#### q = 5 (first non-arithmetic case; quadratic field ℚ(√5)) `[PROVEN:Lean]`

Theorem `three_cluster_q5` (`projects/aristotle_dispatch_v13/BCZ5Witness.lean`), sorry-free,
axioms clean. λ_5 = φ = (1 + √5)/2, X(5) = 1/φ³ = √5 − 2 ≈ 0.23607. From the rational start
(3/5, 1/3):

| i | a_i | b_i | k | P_i = a_i·b_i | X(5) − P_i (exact) |
|---|-----|-----|---|---------------|--------------------|
| 0 | 3/5 | 1/3 | 2 | 1/5 | √5 − 11/5 ≈ 0.03607 |
| 1 | 1/3 | −4/15 + √5/3 | 1 | −4/45 + √5/9 | −86/45 + 8√5/9 ≈ 0.07650 |
| 2 | −4/15 + √5/3 | 11/30 + √5/30 | — | −19/450 + 17√5/150 | −881/450 + 133√5/150 ≈ 0.02487 |

All three inequalities are verified exactly in ℚ(√5). The k = 1 step at i = 1 is precisely the
step the q = 4 proof excludes by its "k ≥ 2" argument — confirming the mechanism crossing into
the non-arithmetic regime. The identity X(5) = 1/φ³ is itself Lean-formalized
(`X5_eq_inv_phi5_cubed`).

#### q = 7 (first cubic case; field ℚ(λ_7)) `[PROVEN:Lean]`

Theorem `three_cluster_q7` (`projects/aristotle_dispatch_v14/BCZ7Witness.lean`), sorry-free,
axioms clean. **The first machine-verified 3-cluster in a cubic number field.** λ_7 is the
root of x³ − x² − 2x + 1 in (1.8019, 1.8020); reduction λ_7³ = λ_7² + 2λ_7 − 1;
X(7) = 1/λ_7³ = −5λ_7² + 3λ_7 + 11 ≈ 0.17092. From the rational start (20/61, 25/61):

| i | P_i (in ℚ(λ_7)) | X(7) − P_i | lower bound |
|---|-----------------|------------|-------------|
| 0 | 500/3721 | 40431/3721 + 3λ − 5λ² | ≥ 0.03561 |
| 1 | −500/3721 + (625/3721)λ | 41431/3721 + (10538/3721)λ − 5λ² | ≥ 0.00168 |
| 2 | −375λ²/3721 + 1025λ/3721 − 125/3721 | 41056/3721 + (10138/3721)λ − (18230/3721)λ² | ≥ 0.03444 |

Each margin is a downward-opening quadratic in λ (negative leading coefficient), so its minimum
over λ ∈ (1.8019, 1.8020) is at the right endpoint, where rational substitution gives the lower
bounds shown; positivity is therefore certified by rational-interval arithmetic. The identity
X(7) = 1/λ_7³ is Lean-formalized (`X7_eq_inv_lam7_cubed`). The recipe — express each margin as
a quadratic in λ with negative leading coefficient, evaluate at the rational interval endpoint —
mechanizes for arbitrary q, which is why the ladder q = 8..24 certifies cleanly.

### 3.4 Why the arithmetic proof does not extend to non-arithmetic q

The forward arguments close by exact λ² ∈ ℤ cancellations. Their natural q-parameterization
reduces the third-step nonnegativity to an inequality of the form c ≥ √2/λ² on consecutive
last-branch points; the naive chain (rule out k₁ = 1 ⇒ b < 1/λ² ⇒ c > 1 − 1/λ) would need
1 − 1/λ ≥ √2/λ², i.e. λ ≳ 1.79004 — which would "predict" B = 2 for q ≥ 7. This
**mis-predicts the data on both sides**: q ∈ {3, 4, 6} close *despite* failing the inequality,
while q = 7 (which satisfies it) has B = 3. There is no uniform real inequality in λ governing
the closing; closure is arithmetic (λ² ∈ ℤ), not analytic. Consequently a uniform forward
direction cannot be a q-parameterization of the q = 4 case analysis — it requires new
mathematics (§7).

---

## 4. The B(q) Growth Story: the Rotation-Arc Mechanism

For non-arithmetic q the cluster ceiling B(q) is *not* bounded — it **grows**, with asymptotic
slope ≈ 0.216 q. We give below the witnessed values, then the exact geometric mechanism that
generates them, and explain why B(q) admits **no continuous closed form**. (An earlier empirical
fit B(q) = 2 + ⌊(q−1)/6⌋ is *refuted* — see §4.2 — and is retained here only as a cautionary
record.)

### 4.1 The witnessed ceiling

For non-arithmetic q, the exact-witness ladder (§3.3) gives the following *lower bounds*
B(q) ≥ (witnessed length), all `[PROVEN:exact-witness]`. Orbit scans give matching *upper*
bounds `[NUMERICAL]` (no longer last-branch run was found at depth up to 3 × 60M steps;
junction-safe; burn = 500). The combined best-estimate ceiling:

| q | arith? | λ_q | X(q) | B(q) | lower bound | upper bound |
|---|--------|-----|------|------|-------------|-------------|
| 3 | YES | 1.00000 | 2/9 | 2 | `[PROVEN:Lean]` | `[PROVEN:Lean]` |
| 4 | YES | 1.41421 | √2/8 | 2 | `[PROVEN:Lean]` | `[PROVEN:Lean]` |
| 5 | no | 1.61803 (φ) | 0.23607 | 3 | `[PROVEN:exact-witness]` | `[NUMERICAL]` (54,156 len-3 obs) |
| 6 | YES | 1.73205 | √3/9 | 2 | `[PROVEN:Lean]` | `[PROVEN:Lean]` |
| 7 | no | 1.80194 | 0.17092 | 3 | `[PROVEN:exact-witness]` | `[NUMERICAL]` (1,064 len-3 obs) |
| 8 | no | 1.84776 | 0.15851 | 3 | `[PROVEN:exact-witness]` | `[NUMERICAL]` |
| 9 | no | 1.87939 | 0.15064 | 3 | `[PROVEN:exact-witness]` | `[NUMERICAL]` |
| 10 | no | 1.90211 | 0.14531 | 3 | `[PROVEN:exact-witness]` | `[NUMERICAL]` |
| 11 | no | 1.91899 | 0.14151 | 3 | `[PROVEN:exact-witness]` | `[NUMERICAL]` |
| 12 | no | 1.93185 | 0.13870 | 3 | `[PROVEN:exact-witness]` | `[NUMERICAL]` (no len-4 found) |
| 13 | no | 1.94188 | 0.13656 | 4 | `[PROVEN:exact-witness]` (first 4) | `[NUMERICAL]` (310 len-4 obs) |
| 14–18 | no | — | — | 4 | `[PROVEN:exact-witness]` | `[NUMERICAL]` (no len-5 found) |
| 19 | no | 1.97272 | 0.13026 | 5 | `[PROVEN:exact-witness]` (first 5) | `[NUMERICAL]` (79–108 len-5 obs) |
| 20–22 | no | — | — | 5 | `[PROVEN:exact-witness]` | `[NUMERICAL]` (no len-6 found) |
| 23 | no | 1.98137 | 0.12856 | 6 | `[PROVEN:exact-witness]` (first 6) | `[NUMERICAL]` FRAGILE (1–6 events) |
| 24 | no | 1.98289 | 0.12826 | 6 | `[PROVEN:exact-witness]` | `[NUMERICAL]` (83–184 events) |

**Transitions** (first non-arithmetic q at each ceiling), all `[PROVEN:exact-witness]`:
B = 3 at q = 5; B = 4 at q = 13; B = 5 at q = 19; B = 6 at q = 23. Note the asymmetry of
evidence in this exact-witness band: the *lower* bounds (≥) are exact certificates; the *upper*
bounds (≤, hence the exact value B(q)) were Monte-Carlo and become fragile at q = 23, 24. These
upper bounds — including the fragile q = 23 value — are now *independently confirmed* by the
exact rotation-arc count (§4.3), which reproduces the genuine-map B(q) at 100% for q = 7..40
(`research_notes/Bq_rotation_arc_2026-06-14.md`). The witnessed transitions are consistent with
the derived linear growth (slope ≈ 0.216 q) of §4.3; the small early gaps are O(1) jitter around
that line from the resonance described below, **not** evidence of sub-linear growth.

### 4.2 A refuted empirical fit `[REFUTED]`

An earlier draft reported B(q) = 2 + ⌊(q − 1)/6⌋ as a conjectural growth law. **This is false
and must not be cited as a law.** It was an artifact of data that stopped at q = 24: the slope
1/6 ≈ 0.167 disagrees with the true asymptotic slope ≈ 0.216 (§4.3), and the formula is
**explicitly refuted by exact rotation-arc counts**, which reproduce the genuine map at 100%
(`research_notes/Bq_rotation_arc_2026-06-14.md`). The formula fails at, among others,
q = 5 (true 3 vs. formula 2), q = 23 (6 vs. 5), q = 24 (6 vs. 5), q = 30 (7 vs. 6), and
q = 40 (9 vs. 8); over q = 7..40 it disagrees with the ground truth at roughly a third of the
values, with the deficit growing as q grows. (It was statistically indistinguishable from
2 + √q and 2 + log q only on the short q ≤ 24 window — precisely the small-sample illusion that
made it look like a law.) It is retained here only as a cautionary record; the genuine growth
account is §4.3.

### 4.3 The rotation-arc mechanism and the lattice-vs-notch resonance

The growth of B(q) is generated by an **exact geometric mechanism**, which both reproduces the
ceiling and explains why it has no continuous closed form. Full detail and the verification
tables are in `research_notes/Bq_rotation_arc_2026-06-14.md`; we summarize.

**The conserved energy ellipse.** On the last branch with floor digit k = 1, the map
(a, b) ↦ (b, −a + λb) is the matrix M = [[0, 1], [−1, λ]], λ = 2 cos(π/q), which has det M = 1,
tr M = λ, and is therefore an **elliptic rotation by π/q** (rotation number 1/(2q)). It
preserves the positive-definite quadratic form (the "energy")

    E(a, b) = a² − λ a b + b².

In whitening coordinates E becomes |·|² and M becomes a literal rotation by −π/q; the
gap-product P = a·b along a level set E = E₀ is a fixed sinusoid of the rotation phase, peaking
at the symmetric point a = b with value E₀/(2 − λ). `[PROVEN:Lean]` — the conserved-form +
rotation + bounded-orbit + "no infinite k = 1 run" facts are sorry-free, axiom-clean in
`projects/mimo-mini-project/lean/BCZHeckeNoInfiniteRotation_allq_VERIFIED.lean` (namespace
`HeckeNoRot`: `Eform`, `E_conserved`, `E_const`, `E_pos`, `c_le_M`, `no_infinite_rotation`).

**A cluster is a rotation arc.** A maximal sub-threshold last-branch cluster is therefore a run
of consecutive π/q-rotation lattice points on **one** energy ellipse, all with P < X(q). The
floor digit is k = 1 on every interior step (a pure rotation) and increments to k = 2 on the
terminal step — which kicks the state off the ellipse (ejection) but is itself still
last-branch and sub-threshold. Hence every maximal cluster has **k-pattern [1, …, 1, 2]**, and

    B(q) = 1 + (max # consecutive interior k = 1 last-branch sub-threshold rotation steps).

`[NUMERICAL — exact, dps = 50]` This discrete rotation-arc count reproduces the genuine
full-Taha-map ceiling at **100% (34/34) for q = 7..40**, including the corrected B(23) = 6 and
B(24) = 6; the q = 23 value was additionally confirmed by 120-start heavy Monte-Carlo (7 length-6
runs, no length-7 run). The cluster ab-values are symmetric-unimodal about the peak, the rotation
signature.

**Asymptotic slope (derived, not fitted).** The sub-threshold last-branch arc has limiting
angular width W_∞ ≈ 0.679 rad (the ellipse degenerates parabolically toward E = (a − b)² as
λ → 2, non-degenerate at every finite q), so the number of π/q steps it holds grows as

    B(q) ~ (W_∞ / π) · q ≈ 0.216 · q.

The slope ≈ 0.216 is a derived geometric constant (limiting arc-fraction ÷ π), matching the
prior empirical ≈ 0.22 q — not a fit.

**No continuous closed form: the lattice-vs-notch resonance.** The continuous-arc proxy
⌊W(q)·q/π⌋ + 1 matches B(q) for all q = 7..40 **except q = 23**, where it gives 5 but the true
value is 6. The reason is a genuine **arithmetic resonance**: B(23) = 6 is realized on an ellipse
whose peak ab sits slightly *above* the threshold t = 1/λ³ (peak/t ≈ 1.0023), poking a
sub-(π/q)-wide super-threshold *notch* into the top of the arc and splitting the continuous
sub-threshold arc. But the discrete −π/23 rotation lattice **straddles the notch** — no lattice
point lands in the narrow super-threshold gap, the two points flanking the peak both stay just
below t (t − P ≈ 3·10⁻⁴), and a 6-point run fits. No continuous arc width can represent a
discrete step hopping a sub-step-width notch. This is the precise structural reason **B(q) is
exactly the *discrete* rotation-lattice count and has no continuous closed form** — a positive
finding (an arithmetic lattice-vs-notch resonance), not a gap in the analysis.

**Honest residuals.** The conserved-form/rotation/finite-run half is Lean-verified (above). The
"interior steps stay k = 1 on the whole arc" confinement is numerically certified (dps = 50) and
in the same family as the Lean confinement lemmas, but is not yet a uniform theorem; the
continuous arc-width bound and slope are an L1b-family calculus problem; and the *exact* value at
resonance q's needs a lattice-gap/Diophantine argument (§7.2).

### 4.4 No arithmetic invariant beyond the {3,4,6} pin tracks B(q)

`[NUMERICAL]` Computing [ℚ(λ_q):ℚ] = φ(2q)/2 and [ℚ(λ_q²):ℚ] for q = 3..24: the bound-2 set is
*exactly* {q : [ℚ(λ_q²):ℚ] = 1} = {q : λ_q² ∈ ℤ} = {3, 4, 6}. For q ≥ 5, neither degree tracks
B(q): they oscillate non-monotonically while B(q) grows monotonically (e.g. q = 8 and q = 12
both have [ℚ(λ²):ℚ] = 2 with B = 3, yet q = 11 has degree 5 and also B = 3; q = 17 has degree 8
and q = 18 degree 3, both B = 4). The structure is therefore one arithmetic fact
(λ² ∈ ℤ ⟺ q ∈ {3,4,6} ⟺ B = 2) governing the bound-2 pin, atop a **geometric, linearly growing**
(slope ≈ 0.216 q) rotation-arc ceiling whose only arithmetic dependence is the lattice-vs-notch
resonance of §4.3.

### 4.5 B(q) is an intrinsic dynamical quantity

`[NUMERICAL]` Run-length histograms show a characteristic non-geometric shape: a 200–500×
crash in the count at length B(q) + 1, after which the surviving shorter lengths show a
secondary bump (N(k)/N(k−1) climbing back to ≈ 0.6–1.4), not a geometric tail. This sharp
cutoff — not a slow tail — is the signature of an intrinsic dynamical ceiling, so B(q) is a
real object rather than merely "the longest run sampled." Its precise value at the soft high-q
onset (q ≥ 23) is nonetheless at the resolution floor for the upper bound.

---

## 5. The X(q) = Cluster-Onset Bridge

`[NUMERICAL]` Beyond the dichotomy, the threshold X(q) is uniformly the *cluster-onset*
threshold for runs of size B(q). Define onset_k as the largest threshold T at which the maximal
cluster size is ≤ k. Junction-safe orbit scan (`code/goal1_onset_scan.py`, n = 2.5M steps × 6
starts):

| q | arith? | onset_2 / X(q) | max-run at X(q) | onset_3 / X(q) |
|---|--------|----------------|-----------------|----------------|
| 3 | YES | **1.0004** | **2** | 1.0006 |
| 4 | YES | **1.0031** | **2** | 1.0046 |
| 5 | no | 0.8399 | 3 | **1.0025** |
| 6 | YES | **1.0034** | **2** | 1.0049 |
| 7 | no | 0.9801 | 3 | **1.0090** |
| 8 | no | 0.9591 | 3 | **1.0059** |

For arithmetic q, onset_2 ≈ X(q) (X is the bound-2 onset). For non-arithmetic q, onset_2 < X(q)
while onset_3 ≈ X(q) (X is the bound-3 onset). So the identity "X(q) is the B(q)-cluster onset"
is uniform across q (within < 0.4% for arithmetic q, ~1% for non-arithmetic q tested), and the
*size* at that onset is the arithmeticity signal. This is the local statistical bridge: the
ergodic-optimization edge X(q) coincides with the extreme-gap cluster onset.

**Mechanism (extreme confinement).** `[NUMERICAL]` Orbit scans
(`code/goal1_branch_minP.py`, q = 3..8) show extreme points (P < X) are confined to the last
branch T_{q−1}; intermediate branches have min P just *above* X(q) (e.g. q = 5: T_3 min
P = 0.236146 vs. X = 0.236068). The clusters in the table are therefore genuine last-branch
clusters, consistent with the Definition in §2.4 and the Lean theorems.

**Status of the uniform onset identity.** The identity X_Ω(q) = 1/λ_q³ (X_Ω the
ergodic-optimization ground value, inf over invariant measures of the essential supremum of P)
is **OPEN at the uniform level** — see §7.3. It is strongly supported by the onset ratios above
but is not claimed here.

---

## 6. Relation to Trace-Set Arithmeticity

### 6.1 Luo–Sarnak / Geninska–Leuzinger: the bounded-clustering program

This is the program our result belongs to. Luo–Sarnak [LS95] introduced the **Bounded-Clustering
Property (BCP)** of the trace/length spectrum and Sarnak conjectured that BCP characterizes
arithmeticity among Fuchsian groups. Geninska–Leuzinger [GL08] (Duke Math. J. 142;
arXiv:math/0609477) **proved Sarnak's conjecture for cofinite Fuchsian groups with parabolics** —
which is exactly the cusped Hecke case G_q. So "bounded clustering ⟺ arithmetic" is an
*established theorem* for our groups, over the *global* trace set (all closed geodesics). Our
dichotomy is the same arithmetic property of G_q read off a *local* object — the gap product at
three consecutive points of a horocycle-section orbit. We therefore make **no new criterion
claim**: our contribution is the machine-verified forward instance plus the rotation-arc growth
mechanism (§1.3). The conceptual contrast is global trace set [LS95, GL08] versus three
consecutive section points (ours).

### 6.2 Bogomolny–Schmit (2003): the head-on case

[BS03] (arXiv:nlin/0312057) showed *non-arithmetic* Hecke groups also exhibit exponential trace
multiplicities — a feature usually read as an arithmeticity marker — so the trace *multiplicity*
does not cleanly separate arithmetic from non-arithmetic within the Hecke family. Our
gap-product clustering statistic *does* separate them. The Bogomolny–Schmit finding is thus an
argument **for** the interest of the local observable: it distinguishes cases the trace
multiplicity conflates.

### 6.3 Athreya–Chaika (2012): the qualitative support edge

[AC12] (GAFA 2012; arXiv:1012.4298) proved that for Veech (lattice) surfaces — which include the
G_q Poincaré sections — the gap distribution has no accumulation at 0 (small gaps excluded).
Our result is the within-lattice-family arithmetic *refinement*: all G_q are lattice surfaces
("no small gaps"), but only arithmetic G_q have cluster ceiling B = 2. [AC12] supplies the
qualitative support-edge precedent; ours is the quantitative clustering refinement that splits
the lattice family by arithmeticity.

### 6.4 Taha (2018, 2019): the section

[T18] (arXiv:1810.10668) constructs the G_q–BCZ map, domain T^q, and roof R_q, and [T19]
(arXiv:1906.07250) identifies the Veech section. Neither establishes any extremal value or
cluster bound for q ≥ 4; our threshold X(q), the cluster ceiling B(q), and the dichotomy are
new on top of Taha's section.

### 6.5 Schmutz conjecture (2024)

arXiv:2410.05223 (2024) treats the Schmutz conjecture on arithmeticity and length spectra. Our
observable (gap-product clustering) and their object (length spectrum) are distinct; we cite it
as part of the broader "arithmeticity-from-spectra" landscape in which our local statistic sits.

### 6.6 The q = 3 case and Farey prior work

For q = 3 (the classical Farey–BCZ section) the bound B(3) = 2 and threshold X(3) = 2/9 are
closely related to (and may be implicit in) Cobeli–Zaharescu [CZ05] on the Hall distribution of
Farey consecutive-gap products and the ABCZ work [ABCZ01] on h-spacing. We position our q = 3
Lean formalization as the first machine-verified statement of this cluster bound, not as a new
mathematical result at q = 3.

---

## 7. Open Problems

These are explicitly open and are NOT claimed.

### 7.1 Reverse direction for all non-arithmetic q `[CONJECTURE]`

We have exact algebraic witnesses (and matching Lean formalizations at q = 5, 7) for every
q = 5..24. The margin-positivity recipe (quadratic in λ, negative leading coefficient, rational
interval endpoint) appears to mechanize for arbitrary q, but no uniform construction valid for
*all* non-arithmetic q is proved. The existence of a 3-cluster for every non-arithmetic q is a
conjecture, very strongly supported.

### 7.2 The B(q) growth — what is open after the rotation-arc mechanism

§4.3 establishes the *mechanism* (rotation-arc count, slope ≈ 0.216 q) and verifies it at 100%
against the genuine map for q = 7..40. The closed-form fit B(q) = 2 + ⌊(q − 1)/6⌋ is **refuted**,
not open (§4.2). What remains open is *making the mechanism a theorem*: (a) a uniform proof that
interior cluster steps stay k = 1 on the whole arc (numerically certified; same family as the
Lean confinement lemmas); (b) the continuous arc-width bound R(q) ≤ ⌊W(q)·q/π⌋ + 1 and the
asymptotic slope W_∞/π, an L1b-family calculus problem (Aristotle-suitable); and (c) the
*exact* value at resonance q's (e.g. q = 23), which requires a lattice-gap / inhomogeneous-
Diophantine argument — and is precisely why no clean *continuous* closed form exists.

### 7.3 The uniform onset identity X_Ω(q) = 1/λ_q³ (OPEN / in progress)

The central open problem of the broader program is to prove, for all q, that the
ergodic-optimization ground value X_Ω(q) = inf_μ ess-sup_μ P equals 1/λ_q³. Current status
(see `research_notes/fcorr_lb_human_handoff_2026-06-13.md`):

- **q = 5..18: UNCONDITIONAL, machine-verified** (14 Hecke groups; `uniform_q5to18/`,
  axiom-clean). A strong standalone result.
- **q ≥ 19:** gated on a single open calculus lemma — the **single-corridor arc-width
  inequality** `fcorr_lb` (`projects/aristotle_dispatch_v15/L1bArcCoverage.lean`), a uniform
  quantitative lower bound P ≥ 1/λ³ on one F-corridor rotation arc. Its worst case reduces
  exactly to cos²(33π/512) < 24/25 with closing coefficient 50; the margin is tight along the
  curve c = cos θ (any interval relaxation of c by 10⁻⁵ makes it false), so generic
  `nlinarith`/`polyrith` over a c-interval cannot discharge it — the proof must keep c = cos θ
  symbolic. This is a *human-insight bottleneck*, fully characterized in the handoff note; two
  automated passes did not close it.

We do **not** claim the uniform onset identity here. It is referenced for context only, and its
status is OPEN / in progress.

### 7.4 A uniform cluster-size Lean theorem

A single Lean theorem `B(q) = 2 ⟺ q ∈ {3,4,6}` for all q would require (a) the forward
direction for the three arithmetic cases [done, `[PROVEN:Lean]`] and (b) a uniform
algebraic-witness construction for all non-arithmetic q [§7.1, `[CONJECTURE]`]. This is not a
straightforward assembly of existing pieces.

---

## References

(Working identifiers; full bibliographic data to be completed before any submission.)

- [T18] M. Taha, arXiv:1810.10668 — G_q–BCZ map, roof function, domain partition.
- [T19] M. Taha, arXiv:1906.07250 — Veech section identification.
- [TK77] K. Takeuchi, 1977 — arithmeticity of Hecke triangle groups (arithmetic iff
  q ∈ {3, 4, 6, ∞}).
- [GL08] S. Geninska, E. Leuzinger, Duke Math. J. 142 (2008), arXiv:math/0609477 — proof of
  Sarnak's bounded-clustering conjecture for cofinite Fuchsian groups with parabolics (the
  cusped Hecke case).
- [LS95] W. Luo, P. Sarnak, 1995 — Bounded-Clustering Property of the length spectrum; Sarnak's
  conjecture that BCP characterizes arithmeticity.
- [AC12] J. Athreya, J. Chaika, GAFA 2012, arXiv:1012.4298 — no small gaps for Veech surfaces.
- [BS03] E. Bogomolny, C. Schmit, arXiv:nlin/0312057 — exponential trace multiplicities for
  non-arithmetic Hecke groups.
- [ABCZ01] Augustin, Boca, Cobeli, Zaharescu, MPCPS 131 (2001) — h-spacing for Farey fractions.
- [CZ05] C. Cobeli, A. Zaharescu, arXiv:math/0511363 — consecutive Farey gap support (q = 3).
- [Sch24] arXiv:2410.05223 (2024) — Schmutz conjecture, arithmeticity and length spectra.

---

## Appendix A: Machine-Verification Evidence Table

All Lean theorems: Lean 4, Mathlib v4.28.0; sorry-free; `#print axioms` =
`[propext, Classical.choice, Quot.sound]`; build ~8026–8027 jobs.

| Theorem | Statement | Status | Lean file | Dispatch |
|---------|-----------|--------|-----------|----------|
| `cluster_size_le_two_clean` | No 3-cluster at q=3, X=2/9 | `[PROVEN:Lean]` | `aristotle_dispatch_v8/` | v8 |
| `cluster_size_le_two_q4` | No 3-cluster at q=4, X=√2/8 | `[PROVEN:Lean]` | `aristotle_dispatch_v11/BCZ4Cluster.lean` | v11 |
| `cluster_size_le_two_q6` | No 3-cluster at q=6, X=√3/9 | `[PROVEN:Lean]` | `aristotle_dispatch_v12/BCZ6Cluster.lean` | v12 |
| `three_cluster_q5` | Explicit 3-cluster at q=5, P<X(5) | `[PROVEN:Lean]` | `aristotle_dispatch_v13/BCZ5Witness.lean` | v13 |
| `X5_eq_inv_phi5_cubed` | X(5) = 1/φ³ | `[PROVEN:Lean]` | `aristotle_dispatch_v13/BCZ5Witness.lean` | v13 |
| `three_cluster_q7` | Explicit 3-cluster at q=7, P<X(7) | `[PROVEN:Lean]` | `aristotle_dispatch_v14/BCZ7Witness.lean` | v14 |
| `X7_eq_inv_lam7_cubed` | X(7) = 1/λ_7³ | `[PROVEN:Lean]` | `aristotle_dispatch_v14/BCZ7Witness.lean` | v14 |

Exact-witness certificates (sympy algebraic-number arithmetic, not Lean), all
`[PROVEN:exact-witness]`, re-run 2026-06-13 with no failures:

| q range | cluster lengths | script | output |
|---------|-----------------|--------|--------|
| 5 | 3 | `code/goal1_q5_witness_exact.py` | `code/out/goal1_q5_witness_exact.{json,md}` |
| 7 | 3 | `code/goal1_q7_witness_exact.py` | `code/out/goal1_q7_witness_exact.{json,md}` |
| 8–16 | 3 (q≤12), 4 (q≥13) | `code/goal1_qladder_witness_exact.py` | `code/out/goal1_qladder_witness_exact.{json,md}` |
| 17–24 | 4 (q≤18), 5 (q≤22), 6 (q≥23) | `code/goal1_qladder_hi_witness_exact.py` | `code/out/goal1_qladder_hi_witness_exact.{json,md}` |

---

## Appendix B: Reproducibility and a Counter-Definition Correction

**Scripts.**
- `code/goal1_last_branch_ceiling.py` — B(q) ceiling table (last-branch counter; seed 20260609).
- `code/goal1_onset_scan.py` — onset_k / X(q) table (§5).
- `code/goal1_branch_minP.py` — per-branch min P (extreme-confinement mechanism).
- `code/goal1_q4_proof_verify.py` — q=4 proof lemmas, positive margins.
- `code/goal1_q5_witness_exact.py`, `code/goal1_q7_witness_exact.py`,
  `code/goal1_qladder_witness_exact.py`, `code/goal1_qladder_hi_witness_exact.py` — exact
  witnesses (re-verified 2026-06-13, no failures).

**Counter-definition correction (load-bearing).** An earlier note reported the growth rate as
"~ q/3". That was an artifact of a *cross-branch* cluster counter
(`code/goal1_cluster_ceiling_reconcile.py`), which counts consecutive sub-X points over all
branches and, at q ≥ 19, glues several genuine last-branch clusters together through
razor-margin off-last-branch excursions (e.g. the spurious q = 19 "8-run" alternates
T_18/T_16 with off-branch points at margins ~10⁻⁴). The correct counter — the **last-branch**
counter matching all Lean proofs and exact witnesses — has *derived* asymptotic slope
**≈ 0.216 q** (the rotation-arc constant W_∞/π of §4.3, confirmed against the genuine map at
100% for q = 7..40). (An earlier small-q linear fit on q ≤ 24 gave ≈ 0.168, i.e. the "~ q/6"
figure; that slope is too small — it is the same short-window artifact that produced the refuted
⌊(q−1)/6⌋ fit, §4.2 — and is superseded by the derived 0.216.) The q = 13 value B = 4 is
identical under both counters; only the *rate*, not that threshold, was inflated by the
cross-branch counter. This manuscript uses the last-branch counter throughout.

---

## Appendix C: A cross-program byproduct (remark only)

`[NUMERICAL]` A separate probe found the rescaled Farey point set to be **critically (marginally)
hyperuniform**: its structure factor satisfies S(k) ~ k^{1.8–1.9} (strongly suppressed, from
Stern–Brocot gap anticorrelation), sitting exactly on the d = 1 perturbed-lattice edge (rescaled
gap tail P(t > T) = C/T² ⇒ finite first moment, marginally divergent second). The estimator was
validated against Poisson, lattice, and jittered-lattice controls. This is a standalone
observation — arithmeticity does not change the hyperuniformity class — and does **not**
strengthen the dichotomy; it is recorded here only to delimit scope. It is not part of the main
result and should not be cited as such (see `research_notes/wide_appeal_verdict_2026-06-13.md`:
the wide-appeal / physics directions were all negative; the value of this work is mathematical).

---

*End of internal draft. All `[PROVEN:Lean]` and `[PROVEN:exact-witness]` claims are
machine-checkable from the repository; `[NUMERICAL]` claims are reproducible from the scripts
above; `[CONJECTURE]` claims are not asserted as theorems. Nothing herein has been communicated
externally — outward comms USER-gated.*
