# R1 — Hilbert-space restatement of the truncation bound

> **SCOPE BANNER (2026-08-15, per Kimi audit 1-E5): Steps 1–2 of this
> file are LIVE and cited by the declared theorem (assembly link 2).
> Steps 3–4 are SUPERSEDED — Step 3's F_R used the voided
> B_tot = 97.77 envelope (certifies nothing at N=160), and the line-27
> geometric-tail claim is false per V7 and disowned by R5 v3.1. The
> operative F_R, endpoint bounds, and tail treatment are those of
> R3B_FLAGSHIP_CERT.md. Do not cite this file for Steps 3–4.**

Frontier write-up v1, 2026-08-14. Replaces L3/L3′/L3″ (voided by V3).
Consumes: R2's certified column sups b_k; L1 nesting (TB_BLOCK_
CERTIFICATES_V2, still valid); A4-sound branch handling.

## Setting

H := ⊕_{j=1}^{κ} H²(D_j), D_j = D(c_j, R_j) the certified discs. The
normalized monomials e_k^{(j)}(w) = ((w−c_j)/R_j)^k form an orthonormal
basis of each H²(D_j) (standard, boundary-measure normalization). The
operator L = L_{s,+} acts by the 11 certified blocks; by L1 (certified
nesting, ρ* < 1) and A4 (weights analytic and bounded on the closed
discs), each block is a bounded weighted composition operator with image
strictly inside the target disc.

## Step 1 — trace class + trace-norm bound from column sups

For any f analytic on cl(D_i): ‖f‖_{H²(D_i)} ≤ sup_{∂D_i} |f|. Hence for
every input basis vector e_k:
  ‖L e_k‖_H ≤ Σ_{blocks B from k's component} sup_{∂D_i} |Φ_k^B|
           =: b_k,
with b_k EXACTLY the column-sup quantities R2 certifies (center offsets
kept; Hurwitz-closed tail kernels evaluated as kernels, never as
divergent absolute series). By the polar-decomposition inequality
‖T‖₁ ≤ Σ_k ‖T e_k‖ (valid for any orthonormal basis; Simon, Trace
Ideals, ch. 1):
  ‖L‖₁ ≤ Σ_{k≥0} b_k  =: B_tot   (finite: b_k ≤ W·ρ*^k for k beyond the
  certified head, W the corrected head-envelope constant from R2).
So L is trace-class on H with a fully certified trace-norm bound. The
same bound covers ‖L P_N‖₁ ≤ B_tot (P_N orthogonal projection).

## Step 2 — the finite section computes det(I − L P_N)

P_N := projection onto span{e_k : k < N} (per component). The engine's
matrix is M_N = [⟨e_m, L e_k⟩]_{m,k<N}, i.e. P_N L P_N on P_N H.
(a) P_N L P_N and P_N L agree on P_N H, and P_N L has range in P_N H, so
    det_{P_N H}(I − P_N L P_N) = det_H(I − P_N L)
    (finite-rank operator; determinant = determinant of the restriction
    to any finite-dimensional subspace containing the range).
(b) Sylvester's identity for trace-class pairs (det(I−AB) = det(I−BA);
    Simon, Trace Ideals, Thm 3.7 form): with A = P_N, B = L:
    det_H(I − P_N L) = det_H(I − L P_N).
Hence: the computed matrix determinant EQUALS det_H(I − L P_N). Only the
INPUT-column tail separates it from det_H(I − L):
  ‖L − L P_N‖₁ = ‖L (I − P_N)‖₁ ≤ Σ_{k≥N} b_k =: T_tail(N).

## Step 3 — determinant comparison

Gohberg–Krein/Simon perturbation bound (Trace Ideals, Thm 3.4):
  |det(I − L) − det(I − L P_N)| ≤ T_tail(N) · exp(1 + ‖L‖₁ + ‖L P_N‖₁)
  ≤ T_tail(N) · exp(1 + 2 B_tot)  =:  F_R(N).
All constants certified: b_k head terms by R2 arc covers; tail of Σ b_k
by the corrected k-power ratio bound (exponent k + 2σ, center offset via
|θ_n − c_j| ≤ |θ_n| + |c_j| ONLY inside the k-th power where convergent).

## Step 4 — winding on the CLOSED contour (consumes R3)

Cover ∂Box by closed overlapping arcs {A_l}. R3 certifies det-enclosures
d_l ⊇ {det(I − P_N L P_N)(s) : s ∈ A_l}. Inflate each by F_R(N):
d_l^+ := d_l + ball(0, F_R(N)) ⊇ {det(I − L)(s) : s ∈ A_l}. If every
d_l^+ excludes 0 and the certified argument increments over the closed
cover sum to 2π·w with w ≥ 1, then by the argument principle det(I − L)
has ≥ w zeros inside the box. (Rouché is subsumed: 0 ∉ d_l^+ on the
whole boundary is exactly the non-vanishing hypothesis.)

## What remains for the theorem statement

- R2/R3 receipts with the constants (running).
- The identification "zero of det_H(I − L_{s,+}) in the box" +
  "det(1−K_s) ≠ 0 there (CLOSED, exact lattice)" + MMS factorization ⇒
  zero of Z_S(s) with the stated multiplicity — the resonance statement
  per the V1-approved phrasing (P-symmetric sector; essential-gap form).
- Citation ledger: Simon Trace Ideals Thms 3.4/3.7 + ch.1 inequality;
  H²(D) monomial orthonormality; MMS eq.(32)/(34) + Lemma 6.3.
- Aristotle candidates: the finite-dim restriction identity (a); the
  polar column-norm inequality (finite version); b_k tail summation
  algebra. Dispatch after R2 fixes the constants.

## Honesty

This restatement was forced by V3's adversarial review; nothing from the
voided L3 variants is reused. The one remaining heuristic-free gap to
watch: R2 must certify b_k for ALL k < N_head with the SUMMED kernels —
if the per-k arc covers get expensive, the fallback is a smaller certified
head + larger analytic tail constant, costing a larger N in F_R(N).
