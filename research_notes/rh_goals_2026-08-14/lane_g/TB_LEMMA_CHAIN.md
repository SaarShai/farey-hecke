# T-b — The proven truncation bound: lemma chain with certified constants

> **STATUS 2026-08-14 (post V3 sol adversarial review): CHAIN BROKEN AS
> WRITTEN — see ADVERSARIAL_REVIEW_V3_TBCHAIN.md. Theorem NOT certified.**
> Confirmed defects: (A1) finite-section vs column-truncation conflation —
> repair via the Fredholm identity det(I−LP_N) = det_{P_NH}(I−P_N L P_N)
> on a trace-class Hilbert-space setting (to be stated properly, H² of the
> discs); (A2) trace-norm bound must cover the INFINITE operator at both
> perturbation endpoints; (V2-envelope) W^{(≥1)} INVALID — dropped the
> target-center offset and the per-column m=0 Hurwitz term ⇒ W=18.6, F,
> and "minimal N=567" are all void; (A3) winding implementation certifies
> samples, not the closed contour — must enclose det over closed boundary
> arcs. REPAIR PROGRAM: R1 Hilbert-space restatement + Fredholm identity
> (frontier write-up); R2 corrected envelope certification (with center
> offsets and summed-column Hurwitz bounds, per-k, on arc covers); R3
> closed-arc winding enclosures; R4 endpoint trace-norm hybrid using R2.
> Sections below are retained as history; do NOT cite constants from L3′/
> L3″/W2 until R1–R4 replace them.
Frontier draft v1, 2026-08-14. Inputs: TB_BLOCK_CERTIFICATES_V2 (certified
ρ* ≤ 0.69781), tb_disc_opt.json (radii), v17 Lean lemmas (tail_branch_abs_
bound, image_in_disc_with_margin), KS_GATE (exact, machine-proved lattice).

## Setup

Discs D_j = D(c_j, R_j), R_j = a_j h_j, (a₁,a₂,a₃) = (3.14, 2.27, 1.70),
c_j, h_j from the q=5 Markov partition. B = ⊕_j H^∞(D_j) with the
normalized-monomial "basis" e_k^{(j)}(w) = ((w−c_j)/R_j)^k. The operator
L_s (MMS eq. 34, mms+ sector, s in the certification box) acts by the 11
certified blocks; each block B applies weight u_B(z) = (θ′)^s (branch cut
clearances certified 11/11) and composition with θ_B.

## L1 (branch-image nesting — CERTIFIED)

For every block B with source i and target j:
  sup_{|z−c_i| = R_i} |θ_B(z) − c_j| ≤ ρ* R_j,  ρ* = 0.697802 (Arb ball,
  TB_BLOCK_CERTIFICATES_V2: 5 singles + 100 head-tail terms individually
  arc-covered; deep tails by the Lean-proved crude inequality pattern).

## L2 (coefficient decay of each block's output)

Fix block B and input basis element e_k^{(j)}. The output function
g(z) = u_B(z) · ((θ_B(z) − c_j)/R_j)^k is analytic on cl(D_i) (poles/cuts
certified clear), and on the contour |z−c_i| = R_i:
  |((θ_B(z) − c_j)/R_j)^k| ≤ (ρ*)^k   (by L1),
  |u_B(z)| ≤ W_B                       (certified sup of the weight on the
                                        contour; computed per box in T-c).
Cauchy's coefficient bound on the SAME contour gives, for the m-th
normalized output coefficient (extraction radius = R_i, the basis radius):
  |g_m| ≤ W_B · (ρ*)^k.
Note: with extraction on ∂D_i itself the Cauchy bound has no additional
(r/R)^m decay factor in m; the decay used below comes from the k-index
(input side) — this matches how the certified engine's coefficients are
extracted (Cauchy-FFT on ∂D_i). Column norms therefore satisfy
  Σ_m-truncated column k of block B has every entry ≤ W_B (ρ*)^k.

## L3 (truncation error of the determinant — the bound)

Let L_N be the operator with all input indices k ≥ N deleted (this is
exactly the N-truncation the engine computes: kappa·N × kappa·N). The
difference E_N = L_s − L_N acts only on input modes k ≥ N. By L2 each such
mode contributes a rank-≤1-per-block piece with norm
  ‖(block B) e_k‖_∞ ≤ W_B (ρ*)^k,
so, with W = max_B Σ_{B with source i, max over i} W_B (the per-target
block-multiplicity-weighted sup, computed in T-c; call it W*),
  Σ_{k≥N} s_k(E_N) ≤ κ W* (ρ*)^N / (1−ρ*),  κ = 3.
The operator is trace-class on B (Grothendieck/Mayer standard, given L1
nesting); by the Gohberg–Krein/Simon determinant-difference inequality
[Simon, Trace Ideals, Thm 3.5 / eq. (3.7) form]:
  |det(1−L_s) − det(1−L_N)|
    ≤ exp(1 + Σ_k s_k(L_s)) · Σ_{k≥N} s_k(E_N)
    ≤ exp(1 + κ W* /(1−ρ*)) · κ W* (ρ*)^N/(1−ρ*)  =:  F(W*, ρ*, N).

With ρ* = 0.6978: (ρ*)^48 = 3.2e-8, (ρ*)^60 = 4.2e-10. T-c reports W* and
the box contour lower bounds; the winding certificate survives iff
contour lower bound − F > 0 at every contour point.

## L3′ — REPAIR (2026-08-14, after W-cert v1 correctly certified W* = +∞)

W-cert v1 proved the ORIGINAL L3 aggregation is wrong: for Re(s) < 1/2 the
absolute sum over tail branches Σ_n sup|（θ′_n)^s| diverges (exponent
2Re(s) < 1). The operator is still trace-class because the ∞-blocks are
the ANALYTICALLY SUMMED (Hurwitz-zeta-closed) kernels, not absolute sums.
Corrected aggregation, per column class:

- k = 0 column of a tail block: its output is the Hurwitz-closed function
  Φ_0(z) = Σ_n u_n(z) (analytic closure; exactly what the engine's
  _tail_block computes with Arb balls). Bound W_B^{(0)} := certified sup of
  |Φ_0| on the contour — a DIRECT ball evaluation of the closed form, no
  divergent series.
- k ≥ 1 columns: |Φ_k(z)| ≤ Σ_n |u_n(z)| ρ_n^k with per-branch certified
  ρ_n (T-b2 data). Since ρ_n ≤ c/n for deep n, Σ_n n^{−2σ}(c/n)^k < ∞ for
  every k ≥ 1; bound by the certified head terms + integral tail with
  exponent k + 2σ > 1. Define W_B^{(≥1)} := certified bound at k = 1
  (the worst case; ratios only improve with k).
Then the L3 singular-value tail uses, per source component,
  Σ_{k≥N} s_k(E_N) ≤ κ · [W^{(≥1)}] · (ρ*)^N/(1−ρ*)   (N ≥ 1 always),
and the k=0 columns never enter E_N for N ≥ 1 — they are inside the
computed matrix. F(W^{(≥1)}, ρ*, N) is finite and the margin table is
well-posed. W-cert v2 certifies W^{(0)} (sanity/conditioning) and W^{(≥1)}
(the constant that enters F).

## L3″ — HYBRID TRACE-NORM REFINEMENT (2026-08-14, after W2 certified the
crude prefactor exp(1+3W/(1−ρ*)) astronomically large: W ∈ [18.6, 1926])

The Gohberg–Krein prefactor needs the TRACE NORM ‖L‖₁ = Σ sᵢ, and the
analytic bound κW/(1−ρ*) is grotesque (the actual operator has ‖L‖₁ =
O(10)). Refinement with no new theory: by polar decomposition,
  ‖A‖₁ = tr(UA) = Σ_k ⟨UA e_k, e_k⟩ ≤ Σ_k ‖A e_k‖₂
(sum of column 2-norms; classical, cite e.g. Simon Trace Ideals §1 —
Aristotle-able finite-dim version). Apply as:
  ‖L_s‖₁ ≤ Σ_{k<N} ‖(computed Arb matrix) e_k‖₂  [CERTIFIED ball norms]
          + κ W^{(≥1)} (ρ*)^N/(1−ρ*)              [analytic tail]
The computed part is O(10) (columns decay like the OBSERVED ~0.29^k, far
faster than the worst-case contour ρ*). Then
  F = exp(1 + ‖L_s‖₁-bound) · κ W^{(≥1)} (ρ*)^N/(1−ρ*),
and the margin arithmetic gives N ≈ 96–128 for the flagship pin (vs 567
under the crude prefactor). The theorem needs ONE pin; the family
production line will use the same hybrid per surface.

## Status / obligations ledger

- [CERTIFIED] L1 constants (Arb, receipt V2). [LEAN] the two shell lemmas
  (v17, sorry-free). [CERTIFIED] pole/cut clearances.
- [PAPER-PROOF, standard] Cauchy coefficient bound; trace-class property of
  nested-disc composition operators (Mayer 1976/Grothendieck); the
  determinant-difference inequality (Simon). These are citation-level,
  named in the theorem's preamble; NOT Lean (Mathlib gap disclosed).
- [T-c, pending] W* values per box; final margin table; the run itself.
- Honesty: this replaces the ×4 dim-tail heuristic entirely; nothing in
  the chain extrapolates observed ratios.
