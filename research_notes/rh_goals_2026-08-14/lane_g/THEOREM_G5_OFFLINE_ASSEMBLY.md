# THEOREM ASSEMBLY — a certified off-line Selberg-zeta zero for G_5
Frontier write-up v2, 2026-08-15 04:55.

STATUS: **DECLARED (computer-assisted; five adversarial review rounds
survived).** Review chain: V4 (all numerics CONFIRMED-SOUND; one
theorem-level gap = determinant identification) → V5 (repair strategy
viable, 3 repairs) → V6 (3-clause lemma prescribed) → V7 ("the
seven-link mathematical argument survives after a local erratum ...
Once they are made, the seven-link assembly earns THEOREM-GRADE YES")
→ V8 final compliance (Opus 5): "THEOREM-GRADE YES" — erratum verified
implemented-correctly item-by-item, E1 receipt independently
reproduced (closed-form margins, 200k-point boundary sweep), V7
quotations verified faithful. Reports: ADVERSARIAL_REVIEW_V{4,5,6,7,8}*.
Dissemination (Koyama letter, submission, distribution) remains
owner-gated per the HITL tickets.

## Statement (essential-gap form, per the V1-approved phrasing)

Let G_5 be the Hecke triangle group with λ_5 = 2cos(π/5) = golden ratio,
X_5 = G_5\H the (non-arithmetic) finite-area hyperbolic orbifold, and
Z_S(s) its Selberg zeta function.

THEOREM (computer-assisted; dependency ledger below). Z_S has a zero s*
with

  |Re(s*) − 0.4538951800749447| ≤ 10⁻⁶,
  |Im(s*) − 5.7635372417301305| ≤ 10⁻⁶.

In particular Re(s*) ≤ 0.4538962 < 1/2: s* lies OFF the critical line
with essential gap

  δ := 1/2 − Re(s*) ≥ 0.0461038.

Since Im(s*) ≈ 5.76 ≠ 0, s* is neither a small-eigenvalue parameter
(those are real) nor a tempered-eigenvalue zero (those lie on
Re(s) = 1/2); by the standard spectral interpretation of finite-area
Selberg zeros in the strip 0 < Re(s) < 1/2, s* is a scattering
RESONANCE of X_5. To our knowledge this is the first rigorous
localization of an off-line resonance of a non-arithmetic finite-area
hyperbolic surface (Bruggeman–Pohl leave the non-arithmetic Hecke
resonances conjectural; prior-art sweep lane_c).

## Proof chain and verification status of every link

1. FINITE WINDING + CLOSED-CONTOUR EXCLUSION [MACHINE, R3b receipt].
   det(I − P_N L_{s,+} P_N), N = 160, has certified argument winding 1
   around ∂Box; the boundary is covered by 284 closed Acb subarcs (71
   per edge, adaptive splits to depth 8); on every subarc the finite
   Taylor enclosure AND the F_R-inflated enclosure exclude 0; minimum
   certified margin (finite lower − F_R) = +3.4379e-8; per-subarc
   self-consistency rH ≤ 0.359 < 1. Receipt:
   R3B_FLAGSHIP_CERT_RECEIPT.json (384-bit Arb/Acb; all_theorem_gates_
   pass = True; immutable input shas verified). Independent frontier
   re-checks (2026-08-15): all 284 records' four gates true; min margin
   recomputed from raw fields = 3.437865e-8; 71×4 subarc census.

2. FINITE SECTION = det(I − L P_N) [PAPER + LEAN]. The computed matrix
   determinant equals det_H(I − L P_N) by the finite-rank restriction
   identity + Sylvester (TB_R1_HILBERT_RESTATEMENT.md Step 2; the
   restriction identity machine-proved in Lean, Aristotle v18
   det_one_sub_proj_mul_proj, axiom-clean).

3. DETERMINANT COMPARISON [PAPER + MACHINE CONSTANTS + LEAN JOINTS].
   |det(I−L) − det(I−LP_N)| ≤ T_tail(N)·exp(1 + ‖L‖₁ + ‖LP_N‖₁)
   (Gohberg–Krein/Simon, Trace Ideals Thm 3.4 form; citation-level).
   Machine constants (R3b receipt): both endpoint norms ≤ 17.29120
   (computed-row column 2-norms 17.29119 + enlarged-disc output-tail
   9.24e-6 + T_tail(160)); T_tail(160) = 6.2679e-22 (immutable R2
   receipt, all 11 families, center offsets kept, Hurwitz-closed m=0);
   F_R(160) = 1.77974e-6. Supporting Lean joints (Aristotle v18/v19,
   all axiom-clean [propext, Classical.choice, Quot.sound]):
   trace_unitary_le_sum_column_norms, l2_le_card_mul_sup_sq,
   coeff_bound_of_uniform, geom_tail_le.

4. TRUE-DETERMINANT ZERO IN BOX [ARGUMENT PRINCIPLE]. Every F_R-inflated
   tube excludes 0 ⇒ the straight-line homotopy det(I−LP_N) → det(I−L)
   never vanishes on ∂Box ⇒ winding of det(I−L_{s,+}) around ∂Box = 1 ⇒
   det(I−L_{s,+}) has exactly one zero s* (with multiplicity) in Box.

4b. HILBERT → BANACH TRANSPORT [PAPER-PROOF + MACHINE + REVIEWED].
   det_H(1 − L_{s,+}) = det_B(1 − L_{s,+}^{MMS}) on Ω* ⊃ Box:
   TB_R5_DETERMINANT_IDENTIFICATION.md v3.1 (smoothing via the
   enlarged discs D_i^{0.1} — receipt
   E1_ENLARGED_CONTRACTION_RECEIPT.json, sha256 cd1dc6f409ebca7852
   bc12a9607b4d2a2f6a10b10be3590055e50ee62ad37187, ρ̂ ≤ 0.9484 < 1,
   min clearance ≥ 1.0023 — independently reproduced by V7 and V8;
   Jordan-chain spectrum equality; spectral canonical determinants:
   Simon Thm 4.2 / Grothendieck Résumé Thm 8; locally-uniform
   trace-class holomorphy on Ω*; identity theorem). Hence the zero of
   link 4 is a zero of the MMS Banach determinant consumed by Thm 6.4.

5. NO DIVISOR CANCELLATION [MACHINE, CLOSED]. det(1−K_s) ≠ 0 on Box:
   the K_s divisor is the exact lattice s = −n + iπk/a_q, all Re ≤ 0
   (KS_GATE_REPORT.md; Lean v17 KsZeroLattice; 90-digit crosscheck
   KS_CROSSCHECK.md); Box sits at Re ≈ 0.454 > 0.

6. SELBERG-ZETA FACTORIZATION [PUBLISHED, CITED]. MMS Theorem 6.4:
   Z_S(s) = det(1−L_{s,+})·det(1−L_{s,−}) / det(1−K_s). The factor
   det(1−L_{s,−}) is analytic near Box (the MMS determinants are
   meromorphic with poles only on the real line, s = (1−k)/2 type;
   Box has Im ≈ 5.76). Hence Z_S(s*) = 0 with multiplicity ≥ that of
   the + factor.  [V4 is asked to re-check the pole set claim.]

7. RESONANCE INTERPRETATION [STANDARD, CITED]. For finite-area
   surfaces, Z_S zeros in 0 < Re(s) < 1/2 off the real axis are
   resonances (scattering poles of the meromorphically continued
   resolvent/scattering matrix); discrete-spectrum zeros lie on
   Re(s) = 1/2 or on the real segment. Citations for the paper:
   Selberg theory (Hejhal LNM 1001; Iwaniec Spectral Methods ch. 10-11;
   Borthwick for the resonance framing). Im(s*) ≈ 5.76 excludes the
   discrete alternatives.

## Convention and sector honesty

- L_{s,+} is the MMS P-symmetric (CF-reflection) sector of eq. (34),
  q = 5, as implemented by the certified engine (sign = +1; convention
  adjudicated in the worktree CONVENTION_AUDIT: pin 0.45390 stands).
- The P-sectors are NOT the geometric even/odd Maass sectors; the
  theorem statement above deliberately does not claim a parity label
  for the resonance — only its existence and location.
- Basis/norm setting: H = ⊕H²(D_j), normalized monomials; b_k are
  H²-norm bounds via sup ≥ H² norm (R1 Step 1).

## Dependency classes (for the paper's preamble)

- MACHINE-CERTIFIED (Arb/Acb interval receipts, replayable): links 1,
  3-constants, 5.
- LEAN-PROVED (Aristotle v17/v18/v19, axiom-clean): the abstract joints
  named in links 2, 3, 5.
- CITED PUBLISHED THEOREMS: Simon Trace Ideals Thm 3.4/3.7; MMS
  Theorem 6.4; standard Selberg/scattering theory (link 7).
- PAPER-PROOF (short, self-contained, in R1/R3b reports): the
  restriction identity assembly, the mean-value arc-enclosure lemma,
  the enlarged-disc Cauchy output-tail bound.

## What V4 must clear before declaration

(a) the mean-value arc-enclosure lemma + its H/Neumann implementation;
(b) enlarged-disc analyticity of the weights for the output-tail
    correction; (c) cover completeness from raw records; (d) the
    argument-increment summation and homotopy; (e) F_R arithmetic;
(f) two independent spot-recomputes; (g) the MMS pole-set claim in
    link 6.

## Constants table (paper-ready)

  s₀            = 0.4538951800749447 + 5.7635372417301305 i
  box half-width = 1e-6 (each coordinate)
  N             = 160 (per component; κ = 3)
  ρ*            = 0.697802 (certified branch contraction, TB_V2)
  T_tail(160)   = 6.26786e-22
  ‖L‖₁ bound    = 17.2911968
  F_R(160)      = 1.77974e-6
  min margin    = 3.43787e-8
  winding       = 1 (ball width 7.81e-114)
  δ (gap)       ≥ 0.0461038
