# F7 CONSTANTS MANIFEST — everything q=7 needs to instantiate the G_5 template

Lane F (family theorem), P1 prep, 2026-08-15. Author: frontier (Kimi).
Template: `lane_g/THEOREM_G5_OFFLINE_ASSEMBLY.md` v2 (DECLARED, V4–V8 +
Kimi-K3 audited). Hostile-referee checklist: `lane_g/ADVERSARIAL_AUDIT_KIMI_K3.md`.
Primary operator source: MMS arXiv:0912.2236, eq. (8) (h_q, κ_q), eq. (34)
(reduced ± sectors, label `reduced3`), §6.2 eqs. (42)–(43) + Lemma 6.3 (K_s).
Prior prep reused and cross-checked: `lane_g/FAMILY_PREP_CONSTANTS.md`
(float/symbolic prep) and `lane_g/KS_GATE_REPORT.md` (q=5 method anchor).
Scan fuel: `lane_k/harvest/hecke_family_q7_q8_scan.json` + `_stats.json`.

All K_s algebra below was re-derived independently of FAMILY_PREP by exact
integer-polynomial arithmetic in Z[λ]/(λ³−λ²−2λ+1) (this session, 120-digit
mpmath evaluation only for decimals); the two computations agree to every
printed digit.

---

## 1. Group data (MMS eq. (8) / C2.3)

- q = 7 (odd, non-arithmetic; the odd-q family q = 2h_q + 3).
- **λ_7 = 2cos(π/7) = 1.801937735804838252472204639014890102331...**
- **h_7 = 2** (vs h_5 = 1).
- **κ_7 = 2h_7 + 1 = q − 2 = 5** components/discs (vs κ_5 = 3).
- Parity of κ: **odd**, same as q=5 — for every odd q, κ_q = q−2 is odd, so
  q=7 stays in the same reduced-sector family (MMS eq. (34), `reduced3`) as
  the certified q=5 chain. The structurally different branch (κ_q = h_q,
  `reduced1`) is the even-q one and is NOT needed here.
- The reduced operator acts on B_5 = ⊕_{1≤i≤5} B(D_i). The two special
  columns are g_{2h_7} = g_4 (receives all single-branch/"head" terms) and
  g_{κ_7} = g_5 (receives all Hurwitz tail terms).

## 2. λ_7 algebra (minimal polynomial and reduction rules)

λ_7 = 2cos(π/7) = −2cos(6π/7); since 2cos(6π/7) = 2cos(2π·3/7) is a root of
x³ + x² − 2x − 1, λ_7 is a root of

  **m(x) = x³ − x² − 2x + 1 = 0.**

Q(λ_7) = Q(ζ_7 + ζ_7⁻¹), the maximal real subfield of Q(ζ_7): degree 3,
discriminant 49. (q=5 anchor: λ_5² = λ_5 + 1, degree 2.)

Reduction rules used in all exact computations below:

  λ³ = λ² + 2λ − 1,     λ⁴ = 3λ² + λ − 1.

Consequence flagged for the cert chain: any exact/canonical-form arithmetic
(partition points, disc centers, matrix words) now lives in a DEGREE-3 field,
so q=5's golden-ratio shortcuts (λ² = λ+1) must be replaced by cubic
reduction. Arb real-ball arithmetic is unaffected; the certified engine
evaluates λ_7 as a ball and never needs the field structure — but every
human-written exact identity must use m(x), not the golden-ratio identity.

## 3. Block structure (MMS eq. (34) at h_7 = 2, κ_7 = 5)

Eq. (34) (`reduced3`) with the ± sign of the mms sector:

- Row 1: (L g)_1 = L_{2,s} g_4 + L_{3,s}^∞ g_5 ± L_{−1,s} g_4 ± L_{−2,s}^∞ g_5
- Row 2: (L g)_2 = L_{2,s}^∞ g_5 ± L_{−1,s} g_4 ± L_{−2,s}^∞ g_5   (no L_1 head)
- Rows i = 3, 4, 5: (L g)_i = L_{1,s} g_{i−2} + L_{2,s}^∞ g_5
                              ± L_{−1,s} g_4 ± L_{−2,s}^∞ g_5

Atomic block count: 4 + 3 + 4 + 4 + 4 = **19 blocks = 9 heads + 10 Hurwitz
tails** (q=5: 11 = 5 heads + 6 tails; the two added generic rows i = 4, 5
contribute 4 blocks each).

The 19 blocks in the builder's (row → column, n, kind) tuple notation,
cross-checked against the 19 calls captured from the authoritative builder
(`zeta_mayer_rosen.py:build_reduced_matrix`, FAMILY_PREP receipt):

  heads (9):  (1→4, n=2), (1→4, n=−1), (2→4, n=−1),
              (3→1, n=1), (3→4, n=−1),
              (4→2, n=1), (4→4, n=−1),
              (5→3, n=1), (5→4, n=−1)
  tails (10): (1→5, n=3), (1→5, n=−2),
              (2→5, n=2), (2→5, n=−2),
              (3→5, n=2), (3→5, n=−2),
              (4→5, n=2), (4→5, n=−2),
              (5→5, n=2), (5→5, n=−2)

Distinct Hurwitz tail classes: L_{3,s}^∞ and L_{2,s}^∞ (positive index,
starts n=3 and n=2) and L_{−2,s}^∞ (negative index, start n=−2), all with
target disc D_5; the head singles are L_{2,s}, L_{1,s} (positive) and
L_{−1,s} (negative). Full Markov branches at unit inflation (must be
contracted by asymmetric disc radii, same phenomenon as q=5):
(1→4, n=2 head), (2→5, n=2 tail), (3→1, n=1 head), (4→2, n=1 head),
(5→3, n=1 head), (5→4, n=−1 head).

Disc inflation factors from the q=7 float disc optimization (FAMILY_PREP,
100k-grid + refinements; NOT yet Arb-certified):

  (d_1..d_5) = (2.79, 2.39, 1.90, 1.56, 1.35),   float ρ* = 0.782263813618,
  worst block (2→5, n=2 tail).

For the certified chain these become the exact-string `EXACT_FACTORS`
analog ("2.79","2.39","1.90","1.56","1.35") pending the Arb TB-block
certification; the float ρ* is a preparation value only.

## 4. K_s divisor lattice for q=7 — exact derivation

### 4.1 The operator cycle (MMS §6.2 eq. (43) at h = 2) — WHERE h_7 = 2 BITES

For odd q = 2h+3, K_s acts on B_{2h+1} as a single (2h+1)-cycle. At h_7 = 2
this is the **5-cycle** (vs the 3-cycle at h_5 = 1):

  (K_s g)_1 = L_{1,s} g_2
  (K_s g)_2 = L_{1,s} g_3          <- this row EXISTS ONLY because h_7 = 2
  (K_s g)_3 = L_{2,s} g_4
  (K_s g)_4 = L_{1,s} g_5
  (K_s g)_5 = L_{2,s} g_1

(q=5, h=1: the range 1≤i≤h has one row, the range 2≤i≤h is EMPTY, giving the
3-cycle (K g)_1 = L_1 g_2, (K g)_2 = L_2 g_3, (K g)_3 = L_2 g_1 of
KS_GATE_REPORT.md. The h=2 case inserts the extra L_{1,s} row and lengthens
every subsequent index.)

Lemma 6.3 (odd q): det(1 − K_s) = det(1 − L_{1,s}^h L_{2,s} L_{1,s}^{h−1} L_{2,s}).

- h_5 = 1: the factor L_1^{h−1} = L_1^0 VANISHES → A_s = L_1 L_2 L_2 (word length 3).
- **h_7 = 2: all four factors present → A_s = L_{1,s}² L_{2,s} L_{1,s} L_{2,s}
  (word length 5).** This is the structural difference the ticket warns about:
  the q=5 word is NOT obtained by "the same pattern with different λ"; the
  h−1 exponent is zero at q=5 and one at q=7.

### 4.2 The matrix word and its trace (exact, in Z[λ]/(λ³−λ²−2λ+1))

With θ_n(z) = −1/(z + nλ_7) and Möbius matrices M_n = [[0,−1],[1,nλ_7]]
(det M_n = 1), the argument map of A_s applies the rightmost operator first:

  ψ = θ_2 ∘ θ_1 ∘ θ_2 ∘ θ_1 ∘ θ_1,   matrix word **M_2 M_1 M_2 M_1 M_1**.

Exact product (integer-polynomial arithmetic mod m(λ), carried out this
session; elements written c_0 + c_1 λ + c_2 λ²):

  M_2 M_1 M_2 M_1 M_1 =
    [[ 2 − 2λ − 2λ²,   1 − 2λ − 2λ² ],
     [ −3 + 4λ + 6λ²,  −2 + 5λ + 6λ² ]]

  trace τ_7 = (2 − 2λ − 2λ²) + (−2 + 5λ + 6λ²) = **4λ_7² + 3λ_7**
  determinant = 1 (verified exactly).

Decimals (mpmath, 120 digits):

  τ_7 = 18.39373162228438300161665298907858879397...  (> 2: hyperbolic ✓)

Cross-checks: (a) the same code with the q=5 word M_2 M_2 M_1 in
Z[λ_5]/(λ_5²−λ_5−1) reproduces τ_5 = 4 + 3λ_5 of KS_GATE_REPORT.md;
(b) FAMILY_PREP's independent symbolic computation gives the identical trace
polynomial 4x² + 3x; (c) FAMILY_PREP's direct fixed-point iteration of ψ
gives attracting derivative ell_7² agreeing with the trace-derived value to
relative error 9.9e−95; (d) this session's eigenvalue ratio check:
μ_−/μ_+ = ell_7² exactly as required (μ_± = (τ_7 ± √(τ_7²−4))/2).

### 4.3 ell_7, a_7, and the zero lattice

The attracting multiplier's positive square root:

  **ell_7 = (τ_7 − √(τ_7² − 4))/2 = 0.05452799479805249083392519594349369...**

(ell_7 < ell_5 = 0.11442…: the q=7 scalar composition operator contracts
harder, so the determinant product converges FASTER than q=5 — fewer product
terms needed for the same tolerance.)

The scalar composition operator of ψ has eigenvalues ell_7^{2s+2n},
n = 0,1,2,… (MMS Proposition 2 after the Lemma 6.3 reduction), hence

  det(1 − K_s) = Π_{n≥0} (1 − ell_7^{2s+2n}).

With **a_7 = −log ell_7 = 2.90904104317485659559822217986241490...**, a zero
satisfies exp(−2 a_7 (s+n)) = 1, giving the exact lattice

  **s = −n + i π k / a_7,   n = 0,1,2,…,  k ∈ Z,**

vertical spacing **π/a_7 = 1.07994098638124936009609682819845...**
(q=5: 1.44915850729921…; the q=7 lattice is ~34% denser vertically).

Every lattice zero has Re(s) = −n ≤ 0, so **any winding box with Re > 0 is
automatically K_s-clean**; the gate reduces to a distance computation
(box-to-lattice, not center-to-lattice — Kimi erratum 1-E6 is applied at
the outset this time: the certified margin must be computed from the closed
box, with the √2·half-width diagonal subtracted).

## 5. Candidate pins from the q7 scan (mms+ sector, sign = +1)

Source: `lane_k/harvest/hecke_family_q7_q8_scan.json`, surface `q7_mms_plus`
(400-bit Arb scan, N=22 vs N=28 stability; wall 7533 s). All 10 pins are
N_stable; drift = |pin(N=22) − pin(N=28)|.

| # | Re | Im | absdet N22/N28 | drift (Re, Im) | K_s clearance |
|--:|---|---|---|---|---|
| **1** | **0.4751647621098225** | **4.668743786424289** | 3.2e−16 / 1.4e−16 | **(1.1e−14, 1.9e−14)** | **0.5895494** |
| 2 | 0.2302702343194269 | 6.370837585483981 | 4.9e−15 / 4.8e−15 | (1.6e−12, 9.2e−13) | 0.2304 |
| 3 | 0.4842071839745956 | 7.567217676288090 | 8.9e−16 / 9.8e−16 | (7.9e−13, 6.1e−12) | 0.4843 |
| 4 | 0.1535462800248664 | 8.183762967571962 | 7.3e−16 / 4.0e−15 | (1.5e−11, 2.0e−11) | 0.1559 |
| 5 | 0.3165025498360753 | 9.862846594966610 | 3.9e−16 / 3.7e−15 | (1.3e−9, 5.8e−10) | — |
| 6 | 0.3927511899394740 | 11.762205060988798 | 2.5e−15 / 4.8e−15 | (7.0e−9, 7.6e−9) | — |
| 7 | 0.4030667200461914 | 12.679113013275686 | 4.9e−15 / 3.6e−15 | (6.4e−9, 2.3e−8) | — |
| 8 | 0.4779913615707892 | 12.929347547333600 | 1.9e−15 / 2.0e−15 | (7.0e−9, 4.7e−8) | — |
| 9 | 0.4452921702418319 | 14.597632631564826 | 1.7e−15 / 5.8e−15 | (2.8e−8, 1.2e−7) | — |
| 10 | 0.4732292570986292 | 16.604510849842330 | 2.0e−14 / 1.8e−14 | (2.2e−6, 8.0e−7) | — |

**Primary candidate: pin 1**, s₀ = 0.4751647621098225 + 4.668743786424289 i.
Rationale: smallest N-drift of the family (1e−14, three orders better than
any other off-line pin), lowest Im (best determinant conditioning), largest
K_s clearance among the well-localized pins, and a comfortable essential gap

  δ = 1/2 − Re(s₀) ≥ 0.5 − 0.4751647621098225 − 1e−6 = **0.0248342** (with a
  1e−6 box).

K_s clearance detail (point margin; box margin = this − √2·1e−6 ≈ 0.5895480):
nearest lattice zeros (n=0): k=4 at Im = 4.3197639455249974… (distance
0.58954938767246554) and k=5 at Im = 5.3997049319062468… (distance
0.87182896680207872). Nearest scan neighbor (pin 2) is ΔIm ≈ 1.70 away, so a
1e−6 box isolates pin 1 trivially.

Backup candidate: pin 3 (0.4842071839745956 + 7.567217676288090 i, drift
~1e−12, clearance 0.4843, δ ≥ 0.0148) — only if pin 1's boundary margin
fails in the R3b run.

Sector note: the mms− (sign = −1) scan found 12 pins ALL within 5e−10 of
Re(s) = 1/2 — consistent with tempered eigenvalue zeros and USELESS for an
off-line theorem. The off-line cloud lives in mms+ at q=7 exactly as at q=5,
so SIGN = +1 carries over; per the template's convention honesty section, no
geometric parity label is claimed for the resonance.

## 6. Structural differences from the G_5 template — complete flag list

1. **h_7 = 2 (was 1).** K_s is a 5-cycle, not a 3-cycle; the Lemma 6.3 word
   keeps its L_1^{h−1} factor (length-5 word L_1²L_2L_1L_2 vs length-3
   L_1L_2²). Derived exactly in §4 — not by analogy.
2. **κ_7 = 5 (was 3), parity odd = unchanged family.** Block count 19
   (9 heads + 10 tails) vs 11 (5 + 6); truncated operator is 5N×5N vs 3N×3N
   (at equal N: 2.78× entries, ~4.6× determinant cost).
3. **Special columns move:** heads/L_{−1} terms land on g_{2h_7} = g_4 (was
   g_2); tails land on g_5 (was g_3). Every hardcoded `twoh = 2`, `k_idx = 3`
   in the q=5 chain becomes 4 and 5.
4. **Field degree 3 (was 2).** λ_7³ = λ_7² + 2λ_7 − 1 replaces
   λ_5² = λ_5 + 1 in all exact algebra; τ_7 = 4λ_7² + 3λ_7 genuinely needs
   the quadratic coefficient.
5. **ρ* regime worse:** float ρ* = 0.7823 (was 0.6978). The q=5 chain's hard
   gate ρ* < 0.70 (`certify_r2_flagship.py:306`, `certify_tb_blocks_v2.py:29`)
   is a chosen target, not a theorem constant; it must be re-set for q=7
   (proposed 0.80) with N re-derived from the new ρ* (see F7_CERT_PLAN.md §3).
6. **MMS heading caveat RESOLVES in our favor.** The q=5 assembly needed a
   footnote because the printed heading above eq. (34) says "q = 2h_q+3 > 5"
   while Lemma 4.2 states q ≥ 5 (V7/V8, Kimi 1-E7). For q=7 the printed
   heading itself applies verbatim — the q=7 run should still cite Lemma 4.2
   but does NOT need the erratum footnote.
7. **K_s lattice denser vertically** (spacing 1.0799 vs 1.4492) but still
   entirely in Re ≤ 0; ell_7 < ell_5, faster product convergence.
8. **Sector economics unchanged:** off-line pins in mms+ only (sign = +1);
   mms− pins are on-line to scan precision.
9. **Disc geometry:** 5 discs with asymmetric inflations
   (2.79, 2.39, 1.90, 1.56, 1.35) vs the 3-disc (3.14, 2.27, 1.70); every
   3-factor length check in the chain rejects q=7 input until generalized.
10. **E1 enlarged-disc contraction (link 4b)** must be re-established at
    κ=5 geometry (q=5: ρ̂ ≤ 0.9484); nothing about the κ=3 certificate
    transfers except the method.

## 7. Load-bearing constants summary (no placeholders)

  λ_7      = 2cos(π/7) = 1.801937735804838252472204639…;  min poly x³−x²−2x+1
  h_7 = 2, κ_7 = 5;  blocks = 19 (9 heads + 10 tails), listed in §3
  K_s word: A_s = L_1² L_2 L_1 L_2; matrix M_2 M_1 M_2 M_1 M_1
  τ_7      = 4λ_7² + 3λ_7 = 18.393731622284383001616653…,  det = 1
  ell_7    = (τ_7 − √(τ_7²−4))/2 = 0.054527994798052490833925196…
  a_7      = 2.909041043174856595598222180…;  π/a_7 = 1.079940986381249360096096828…
  lattice  : s = −n + iπk/a_7 (n ≥ 0, k ∈ Z); all Re ≤ 0
  pin s₀   = 0.4751647621098225 + 4.668743786424289 i (mms+, scan N-stable to 1e−14)
  K_s clearance (point) = 0.589549387672466; box margin ≈ 0.5895480
  essential gap δ ≥ 0.0248342 (1e−6 box)
  disc inflations (float, to be Arb-certified): (2.79, 2.39, 1.90, 1.56, 1.35)
  float ρ* = 0.782263813618
