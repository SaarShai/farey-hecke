# R5 — Determinant identification (common continuation), v3.1
Frontier write-up v3.1 (erratum revision), 2026-08-15 ~04:45. v3 was
reviewed by V7 (ADVERSARIAL_REVIEW_V7_R5V3.md): RULING — "the
seven-link mathematical argument survives after a local erratum"; no
missing lemma; Clause 1 binding PASS, smoothing PASS (with the
enlargement-provenance correction below, quantitatively verified by the
reviewer's own 384-bit check), envelope/holomorphy PASS, sector
identification PASS ("an exact identity"). v3.1 applies V7's three
prescribed corrections verbatim and nothing else. Chain of custody:
v2 → V6 three-clause repair → v3 (word-trace route deleted for the
smoothing+spectral route) → V7 erratum → this v3.1.
Closes the single GAP of ADVERSARIAL_REVIEW_V4_R3B.md.

## Clause 1 — exact operator binding (unique formulas, wrapper-bound)

The object is the reduced q=5 P-symmetric-sector block system of MMS
eq. (34) with h_q = 1, κ_q = 3, as certified: discs D_j = D(c_j, a_j
h_j) with radius factors EXACTLY the strings 3.14, 2.27, 1.70, sector
sign +1, engine head split 4 — bound to the certified wrapper
.worktrees/aletheia-restore/code/tc_rerun/certify_r3b_flagship.py
(sha 5b1bb0851fbb143651471fcf7737738a84a45e126b9971a94905c74357831945)
and its builder tc_rerun.py block calls (lines 130–145), NOT to any
standalone engine default. λ = 2cos(π/5).

Eleven blocks (TB_BLOCK_CERTIFICATES_V2 rows ≡ builder calls):
  heads: 1→2 (+2); 1→2 (−1); 2→2 (−1); 3→1 (+1); 3→2 (−1)
  tails: 1→3 (+n, n≥3); 1→3 (−n, n≥2); 2→3 (+n, n≥2);
         2→3 (−n, n≥2); 3→3 (+n, n≥2); 3→3 (−n, n≥2)

Unique symbol/weight formulas (ONE formula each; v2's duplicated
negative-symbol phrasing is withdrawn):
- positive branch +n:  (T_{+n} g)(z) = w_{+n}(z) · g( −1/(z + nλ) ),
  w_{+n}(z) = ((z + nλ)²)^{−s}, principal branch, certified by
  Re(z + nλ) > 0 on the closed source disc (TB_V2 branch-cut table);
- negative (reflected) branch −n:
  (T_{−n} g)(z) = w_{−n}(z) · g( 1/(z − nλ) ),
  w_{−n}(z) = ((z − nλ)²)^{−s}, principal branch, certified by
  Re(nλ − z) > 0 on the closed source disc — note (z − nλ)² =
  (nλ − z)², so the certified positive-real-part bound fixes the
  branch of the SQUARED expression; the composition argument is
  g(1/(z − nλ)), matching the engine implementation
  (zeta_cert_rosen_q5.py lines 203–212) and MMS eq. (34).
Tail blocks sum the corresponding T_{±n} over their n-range; the exact
Hurwitz closure of a tail block applied to input column k uses the
Hurwitz-zeta terms for every m = 0, …, k (engine
zeta_cert_rosen_q5.py, per-column and all-column implementations; MMS
eqs. (26)–(27)). The m = 0 term is the specially Hurwitz-closed CENTER
term used by the R2 envelope — it does not by itself implement the
whole column sum (V7 correction 3).

Two realizations of this ONE system:
- L_s^B on B = ⊕_j B(D_j), B(D) the disc algebra (holomorphic on D,
  continuous on cl(D), sup norm) — the MMS setting; nuclear of order
  zero (MMS §4).
- L_s^H on H = ⊕_j H²(D_j) — the certified realization (R2/R3b).

## Claim

Ω* := ( { Re s > 1/2 } ∪ { Re s > 0 and Im s > 1 } ). (The real pole
lattice { (1−k)/2 } has Im = 0 and Re ≤ 1/2, so it is disjoint from
Ω* automatically — V6 §2.) Ω* is open, connected, contains the
flagship box (Re ∈ [0.45389, 0.45390] > 0, Im ≈ 5.7635 > 1) and the
absolute-convergence region Ω₀ := { Re s > 1/2, Im s > 1 }. On Ω*:

  det_B(1 − L_s^B) = det_H(1 − L_s^H)                            (R5)

## Clause 2 — equality on Ω₀ via smoothing + spectral determinants

(a) SMOOTHING: L_s maps H into B (and B into B, H into H). For
f ∈ H²(D_j) in the normalized-monomial Hardy basis, Cauchy–Schwarz
gives the point-evaluation bound |f(w)| ≤ ‖f‖_{H²}·(1 − r²)^{−1/2} for
|w − c_j| ≤ r·R_j, r < 1 (no stray R^{1/2} factor; V7 §(ii) verified
the normalization). The ENLARGEMENT (V7 correction 1 — NOT the R3b
quarter-clearance contour, which is demonstrably non-contractive for
the 2→3 (+2) family, and NOT a pre-existing TB_V2 field): define
  D_i^{0.1} := D(c_i, R_i + 0.1),   target radii R_j unchanged.
Claim: every branch of every family is holomorphic on cl(D_i^{0.1})
with positive pole/cut margin, and
  sup_{z ∈ cl(D_i^{0.1})} |θ_n(z) − c_j| / R_j ≤ ρ̂ < 1
uniformly over all eleven families — for the six tails via the
finite-head/deep-tail split: certified head branches individually, and
the deep tails by the monotone first-n crude bound (the TB_V2
pattern), which makes the choice uniform in n. Quantitative instance:
CERTIFIED, twice independently. (1) Our receipted run
E1_ENLARGED_CONTRACTION_CERT.md / E1_ENLARGED_CONTRACTION_RECEIPT.json
(sha256 cd1dc6f409ebca7852bc12a9607b4d2a2f6a10b10be3590055e50ee62ad37187;
384-bit Arb; verdict PASS_RHO_HAT_LT_1_AND_CLEARANCE_POSITIVE):
  ρ̂ = [0.948343590350471954782853 ± 4.84e-25],
  min pole/cut margin = [1.00237987356225289328078 ± 9.41e-25],
  worst branch 3→1 (+1) head; all 11 families pass; tails by the
  finite-head/deep-tail split with the monotone first-n bound.
(2) The V7 reviewer's independent read-only diagnostic reproduced the
same values (V7 §(ii)). The qualitative continuity argument — strict
original-disc contraction gap ρ* ≤ 0.6978 plus equicontinuity of the
finitely many head branches and monotone tails — independently gives
existence of SOME ε > 0, per V7 §(ii).
Every block image T f = w_B · (f ∘ θ_B) is then holomorphic on a
neighborhood of cl(D_i) with
  sup_{cl(D_i^{0.1})} |T f| ≤ W_B^{0.1} (1 − ρ̂²)^{−1/2} ‖f‖_{H²},
W_B^{0.1} := sup over cl(D_i^{0.1}) of the block weight |w_B| — a
finite constant since w_B is holomorphic and zero-free on a
neighborhood of the compact cl(D_i^{0.1}) (E1's certified pole/cut
clearance ≥ 1.0023 > 0.1 keeps the singularities out); only
finiteness is used, no numerical value is claimed or needed
[presentational fix 2026-08-15 per Kimi 1-E9]; a function
holomorphic on a neighborhood of cl(D_i) lies in the disc algebra, and
the tail-block sums converge in sup norm on the enlarged discs on Ω₀
(weights uniformly O(n^{−2σ}), σ > 1/2). Hence L_s^H : H → B ⊂ H is
bounded, with the SAME action as L_s^B on B ⊂ H.

(b) COMMON NONZERO SPECTRUM WITH MULTIPLICITIES: if L_s^H v_0 = λ v_0
with λ ≠ 0 then v_0 = λ^{−1} L_s^H v_0 ∈ B by (a); inductively for a
Jordan chain v_j = λ^{−1}(L v_j − v_{j−1}) ∈ B. Conversely
B(D) ⊂ H²(D). So the nonzero eigenvalue sequences of L_s^B and L_s^H,
with algebraic multiplicities, are IDENTICAL (V5 §(a) and V6 §4 both
validated this argument conditional on (a), which is now proved).

(c) BOTH DETERMINANTS ARE SPECTRAL (attributions per V7 correction 2):
on H, L_s^H is trace-class on Ω₀ by CLAUSE 3 below (the locally
uniform Σ_k b_k envelope; NOT the stale TB_R1 line-27 geometric tail),
and the Fredholm determinant equals the canonical product
Π_i (1 − λ_i) with algebraic multiplicities [CITED: Simon, Notes on
infinite determinants, Adv. Math. 24 (1977), THEOREM 4.2, eq. (4.2),
p. 258 — the determinant product; Lidskii's theorem is the subsequent
TRACE identity, Corollary 4.3, and is not the result used here].
On B, L_s^B is nuclear of order ZERO (MMS Theorem 4.10 / §4), hence
p-nuclear for p = 2/3; for the p ≤ 2/3 nuclear class Grothendieck's
Fredholm theory gives the genus-zero product over the eigenvalues with
algebraic multiplicities [CITED: Grothendieck, Résumé des résultats
essentiels dans la théorie des produits tensoriels topologiques…,
Ann. Inst. Fourier 4 (1952), Théorème 8, pp. 108–109; standard
transfer-operator usage: Ruelle, Zeta functions for expanding maps
(1976)]. Both canonical products are entire genus-zero products
normalized to equal 1 at the scalar zero, so no exponential factor or
other normalization residue can distinguish them. With (b), the two
products are identical on Ω₀. Hence (R5) holds on Ω₀.

(Remark: Bandtlow–Jenkinson, On the Ruelle eigenvalue sequence, ETDS
28 (2008), Thm 4.2, proves space-independence of the dynamical
determinant for single-domain systems including B(D) and H²(D); it is
cited here as corroboration only — the proof above does not rely on
extending its hypotheses to the graph-directed setting, which was V6
defect 3/4's concern. No word expansion and no trace-log evaluation at
t = 1 are used anywhere.)

## Clause 3 — trace-class holomorphy of s ↦ L_s^H on Ω*

s enters through the squared-denominator weights ((z±nλ)²)^{−s}
(entire in s given the certified positive-real-part bounds) and the
Hurwitz factors ζ(2s + k, ·) (analytic away from the real points
2s + k = 1 ∉ Ω*). For compact K ⊂⊂ Ω* put σ_K := inf_K Re s > 0. The
R2 centered envelope holds with locally uniform constants:

  b_k(s) ≤ A_K q^k + C_K k ρ^{k−1},   s ∈ K,

with A_K the (continuous-in-s, hence bounded-on-K) Hurwitz-closed
m=0 column sups, ρ the certified contraction, and C_K the first-moment
remainder constant from the absolutely convergent sum
  Σ_n |u_n b_n| ≍ Σ_n n^{−(2σ_K + 1)} < ∞
(the exact R2 aggregation — NOT a claimed 2σ+k centered exponent,
which the R2 report itself rules out; V6 defect 2 adopted verbatim).
Then Σ_k b_k(s) < ∞ uniformly on K, so s ↦ L_s^H is an analytic
trace-class-valued family on Ω*, and its determinant is analytic
[CITED: Simon, Notes on infinite determinants, Adv. Math. 24 (1977),
Theorem 3.3].

## Step 3 — analyticity of det_B(1 − L_s^B) on Ω* [CITED, V6-accepted]

MMS Theorem 4.10: meromorphic in s, poles confined to the real points
s = (1−k)/2 — all outside Ω*.

## Step 4 — identity theorem [V6-accepted]

Ω* is open and connected; both sides of (R5) are analytic on Ω* and
agree on the nonempty open Ω₀ (Clause 2). Hence (R5) on Ω*, in
particular on the flagship box. ∎

## Sector identification [structure V6-accepted; now unconditional]

The compared object is the already-reduced three-component system with
the UNIQUE formulas of Clause 1, which is precisely the reduced
operator of MMS eq. (34) with the + coefficient on the negative-index
blocks — i.e., L_{s,+} as consumed by MMS Theorem 6.4. The certified
wrapper passes sign +1 (V6 §5 verified the coefficient match at the
builder call sites). No involution is used.

## Consequences for the assembly

Assembly link 4 (a zero of det_H in the box) transports to a zero of
det_B(1 − L_{s,+}^{MMS}) in the box; links 5–7 proceed as written
(V4/V5/V6 found no obstruction there).

## Obligations ledger

- [CITED] Grothendieck (Produits tensoriels, Chap. II: determinant of
  nuclear order ≤ 2/3 operators is spectral); Ruelle 1976 (usage).
- [CITED] Simon, Notes on infinite determinants, Adv. Math. 24 (1977):
  Thm 3.3 (analyticity); Thm 4.2, eq. (4.2), p. 258 (the trace-class
  determinant product used in Clause 2(c)); Lidskii = Cor. 4.3 (trace
  identity, not used here).
- [CITED] MMS: §4 nuclearity; Thm 4.10 (real pole lattice); eqs.
  (26)–(27) (Hurwitz closure); eq. (34) (the reduced system); Thm 6.4.
- [CITED, corroboration only] Bandtlow–Jenkinson, ETDS 28 (2008),
  Thm 4.2.
- [PAPER-PROOF, this note] reproducing-kernel smoothing bound (Clause
  2a); Jordan-chain spectrum equality (2b); locally-uniform envelope
  on Ω* (Clause 3).
- [MACHINE] TB_V2 nesting/clearances/branch-cut positivity; R2 receipt
  (A, C, ρ constants at the box); wrapper binding (sha above).
