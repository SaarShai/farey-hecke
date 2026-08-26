# S2 ASSEMBLY — a second certified off-line Selberg-zeta zero for G_5, and the two-pin φ_5 consequence

Frontier write-up v1, 2026-08-26.

STATUS: **UNREFEREED / CONJECTURAL as an assembly.** This document is the
S2-specific assembly required by both merged-certificate referee seats
(S2_MERGED_REFEREE_FABLE.md, S2_MERGED_REFEREE_SOL.md — unanimous
PROMOTABLE-WITH-CORRECTIONS). It binds the merged contour certificate to
R5, MMS Theorem 6.4, the K_s exclusion, and the scalar scattering-divisor
source. Per the standing rule, NOGO-OPEN-1 and NO_VERTICAL_LINE_COROLLARY
remain **OPEN** until a cold adversarial referee passes THIS document.
The template and all shared links follow THEOREM_G5_OFFLINE_ASSEMBLY.md
(the first pin, DECLARED 2026-08-15 after five adversarial rounds); only
S2-specific data and the two-pin consequence are new here.

## Statement (essential-gap form; boxes, not points)

Let G_5 be the Hecke triangle group with λ_5 = 2cos(π/5), X_5 = G_5\H,
Z_S = Z_{G_5} its Selberg zeta function, and φ_5 the scalar scattering
determinant (one cusp; trivial representation ⇒ the scattering matrix is
1×1, per MMS).

CLAIM S2 (computer-assisted; dependency ledger below). Z_S has a zero s₂
with

  Re(s₂) ∈ [0.41054273549473627, 0.41054473549473627],
  Im(s₂) ∈ [7.81976724701551188, 7.81976924701551188].

In particular Re(s₂) ≤ 0.41054473549473627 < 1/2: a second off-line zero,
with essential gap δ₂ := 1/2 − Re(s₂) ≥ 0.08945526450526372 (rounded
down). Since Im(s₂) ≈ 7.82 ≠ 0, s₂ is neither a small-eigenvalue
parameter nor a tempered zero; by the standard spectral reading it is a
second scattering RESONANCE of X_5.

TWO-PIN CONSEQUENCE (for NOGO-OPEN-1). The reflected φ_5 zeros

  ρ₁: Re ∈ [0.54610381992505530, 0.54610581992505530],
      Im ∈ [−5.7635382417301305, −5.7635362417301305]   (first pin),
  ρ₂: Re ∈ [0.58945526450526373, 0.58945726450526373],
      Im ∈ [−7.81976924701551188, −7.81976724701551188]  (this pin),

have real-part intervals separated by a rigorous gap ≥
0.04334944458020843 (closed-interval distance; centre difference
0.04335144458020843). Both intervals lie strictly inside
1/2 < Re s < 1. Hence φ_5 has two zeros with PROVABLY DISTINCT real
parts — the distinct-real-part premise of NOGO-OPEN-1 and the two-pin
premise of NO_VERTICAL_LINE_COROLLARY. Only the interval statements are
licensed: winding = 1 places one zero somewhere in the box, never at its
centre. (The figure 0.5894543, which appeared in one superseded ledger
entry, is a documented transposition error and must never be reused.)

## Proof chain — S2 instantiation of the seven links

Links 2, 3(joints), 4, 4b, 6, 7 are IDENTICAL in mathematical content to
the first-pin assembly (THEOREM_G5_OFFLINE_ASSEMBLY.md); they are
restated here only where the S2 box requires a fresh domain or constant
check.

1. FINITE WINDING + CLOSED-CONTOUR EXCLUSION [MACHINE, merged receipt].
   det(I − P_N L_{s,+} P_N), N = 288, has certified argument winding 1
   around ∂Box₂ (centre s₀ = 0.41054373549473627 + 7.81976824701551188 i,
   half-width 1e-6 per coordinate). The boundary is covered by 192 base
   arcs (48 per edge) certified in 16 chunks of 12; census across the
   merged chunks: 452 accepted closed subarcs, 260 adaptive
   subdivisions, max depth ≤ 8. On every subarc the finite Taylor
   enclosure AND the F_R-inflated enclosure exclude 0; minimum certified
   margin (finite lower − F_R) ≥ 3.064554329376951375e-8 (rounded DOWN);
   max per-subarc rH ≤ 0.49470747 (rounded UP) < 1. Winding ball
   integer-pinned: [0.999…9996 ± 1.22e-113] → 1. Receipt:
   kaggle_s2_contour/chunk_receipts/S2_MERGED_CONTOUR_RECEIPT.json
   (schema s2-merged-contour/v1) with full merge provenance: 16 chunk
   receipts from local_receipts/ ONLY (macOS/arm64; the Kaggle copies
   are excluded because their equally valid F_R upper bound differs at
   the 14th significant digit — F_R is a bound, not an enclosure, and
   the merge gate requires a single common F_R), merge script sha256
   1fb975c2…f0b9, run-time producer sha256 4ac59a18…8040 (identical in
   all 16 receipts' source_bindings; certified bytes preserved at
   worktree commit 9763dba), reproduction command verified to recreate
   every stored aggregate field. Disclosure (fable-seat correction 2):
   the merge_provenance block was appended by the orchestrator AFTER the
   merge run, not emitted by the sha-bound merge script; the aggregate
   fields are byte-reproduced by the recorded merge command (verified to
   scratch and independently by the fable referee seat).

2. FINITE SECTION = det(I − L P_N) [PAPER + LEAN]. Unchanged from the
   first pin: restriction identity + Sylvester; Lean
   det_one_sub_proj_mul_proj (Aristotle v18, axiom-clean).

3. DETERMINANT COMPARISON [PAPER + MACHINE CONSTANTS]. S2 constants
   (identical in all 16 chunk receipts):
   T_tail(288) ≤ 1.4251151e-41 (R2 second-pin envelope receipt,
   R2_SECONDPIN_ENVELOPE_RECEIPT.json, sha 6410dff3…e83d);
   ‖L‖₁, ‖LP_N‖₁ ≤ 37.6839779 (rounded UP; finite column-norm sum
   37.68397782322482394… + output tail + T_tail);
   F_R(288) = T_tail(288)·exp(1 + 2·B_same) ≤ 2.0894485e-8 (rounded UP;
   receipt ball 2.08944841554480794546893170303518402484…e-8).
   Same Gohberg–Krein/Simon form and Lean joints as the first pin.

4. TRUE-DETERMINANT ZERO IN BOX₂ [ARGUMENT PRINCIPLE]. As in the first
   pin: every F_R-inflated tube excludes 0 ⇒ the straight-line homotopy
   det(I−LP_N) → det(I−L) never vanishes on ∂Box₂ ⇒ winding of
   det(I−L_{s,+}) around ∂Box₂ = 1 ⇒ exactly one zero (with
   multiplicity, i.e. total multiplicity 1, hence a SIMPLE zero) in Box₂.

4b. HILBERT → BANACH TRANSPORT — S2 DOMAIN CHECK [R5]. R5
   (TB_R5_DETERMINANT_IDENTIFICATION.md v3.1) proves
   det_H(1 − L_{s,+}) = det_B(1 − L_{s,+}^{MMS}) on
   Ω* = {Re s > 1/2} ∪ {Re s > 0, Im s > 1}. Box₂ lies ENTIRELY in the
   second component: its lower corner (0.41054273549473627,
   7.81976724701551188) already satisfies Re > 0 and Im > 1, and both
   coordinates only increase across the box. R5's block list, signs,
   branch maps, squared-weight convention, and tail starts match the
   certified engine for q = 5, h_q = 1, κ_q = 3, sign +1 (the MMS
   P-symmetric reduced + sector). Hence the link-4 zero is a zero of the
   MMS Banach determinant consumed by Theorem 6.4.

5. NO DIVISOR CANCELLATION — WHOLE-BOX K_s EXCLUSION [MACHINE, CLOSED].
   For q = 5 the exact K_s divisor (KS_GATE_REPORT.md; Lean v17
   KsZeroLattice; 90-digit crosscheck) has zeros ONLY at
   s = −n + iπk/a_q with Re = −n ≤ 0. Box₂ has
   Re ≥ 0.41054273549473627 > 0 on the entire CLOSED box, so
   det(1 − K_s) is zero-free on all of Box₂. This is an exact whole-box
   statement — no point-distance approximation is used (repairing the
   first-pin Kimi 1-E6 precision note by construction).

6. SELBERG-ZETA FACTORIZATION [PUBLISHED, CITED — corrected citation].
   MMS (arXiv 0912.2236, banked PDF sha a10020bd…e072) THEOREM 6.4 (the
   determinant-quotient factorization — NOT eq. (34)):
   Z_{G_q}(s) = det(1−L_{s,+})·det(1−L_{s,−}) / det(1−K_s).
   Equation (34) is the odd-q REDUCED-OPERATOR display that defines
   L_{s,±}; the heading above it prints "q = 2h_q + 3 > 5" while the
   paper's general odd-q incidence formulas, Lemma 6.3, Theorem 6.4, and
   the explicit q = 5 functional equation use odd q ≥ 5; the q = 5
   identification rests on the general incidence formula (h_q = 1
   specialization independently checked against the three-row engine
   code). Any publication must carry this internal heading
   inconsistency. det(1−L_{s,−}) is analytic near Box₂ (MMS determinant
   poles are real-line only; Im ≈ 7.82). With link 5, Z_S(s₂) = 0 with
   multiplicity ≥ that of the + factor.

7. SELBERG ZERO → φ_5 SCATTERING DIVISOR → REFLECTED ZERO [CITED +
   LEAN, correctly attributed]. Two separate steps:
   (a) DIVISOR STEP [CITED — Friedman–Jorgenson–Smajlović, PDF banked
   2026-08-26 at lane_p/literature/FJS_completed_zeta_divisor.pdf,
   sha256 36c9d020fcc7d0118264c486330db9936f866670c45c0e77b185cdc2b9127228
   (matches the sol-seat hash; fable-seat correction 1 closed)]: the FJS completed-zeta factorization
   Z₊(s) = Z(s)/(G₁(s)Γ(s−1/2)^k), Z₋(s) = Z₊(s)φ(s), with its
   enumerated nontrivial zero set, identifies nonreal left-half-strip
   Selberg zeros with reflections of scattering-determinant zeros; the
   Γ/G₁ trivial divisors lie on real loci and meet neither pin box. MMS
   states every Hecke triangle group has one cusp, so the scattering
   matrix is 1×1 and its determinant is the scalar φ_5. Hence the
   nonreal off-line zero s₂ supplies a pole/zero of the scalar φ_5 as
   FJS prescribes. (M1F_EISENSTEIN_DERIVATION.md does NOT supply this
   bridge and is not cited for it.)
   (b) REFLECTION CORE [LEAN — SCAT1_LEMMA31_ARISTOTLE.md]: machine-
   verified: a pole of φ at s is a zero of the same order at 1−s under
   φ(s)φ(1−s) = 1. ONLY this step is attributed to the Aristotle/Lean
   core.
   Composition: ρ₂ = 1 − s̄-type reflection of the s₂ box gives the ρ₂
   intervals in the Statement.

## Interval-separation arithmetic (link for NOGO-OPEN-1)

With box half-width 1e-6 on each pin:
  Re ρ₁ ⊂ [0.54610381992505530, 0.54610581992505530]
  Re ρ₂ ⊂ [0.58945526450526373, 0.58945726450526373]
  centre difference = 0.58945626450526373 − 0.54610481992505530
                    = 0.04335144458020843
  guaranteed gap    = centre difference − 2·1e-6
                    = 0.04334944458020843  (> 0, exact decimal
                      arithmetic; independently re-verified with arb
                      directed rounding 2026-08-26)
The two closed intervals are disjoint; both lie strictly in
1/2 < Re s < 1.

## Controls

- N* floor (S2): N = 274 measured floor; N = 273 fails honestly
  (margin −2.11e-7) — the certificate is not a loose-tail artefact.
- N = 128 control arm: RUN and FILED 2026-08-26, receipt
  kaggle_s2_contour/local_receipts/S2_CONTROL_N128.json
  (status: complete). Result: N = 128 fails HONESTLY as designed —
  NOT_CERTIFIED at base arc 0, depth 0, Jacobi self-consistency
  rH = [1.2165204080717385566… ± 2.33e-115] > 1 — while the N = 288
  arm in the same run certifies its arc (CHUNK_ARCS_CLEAR). The
  certificate is therefore not a loose-tail artefact. The arm is
  NEGATIVE and NON-LOAD-BEARING (the N = 288 trace-norm bound and
  positive boundary margin stand alone; both seats agree it is not a
  logical premise). Fable-seat correction 4: CLOSED.

## Dependency classes

Identical taxonomy to the first pin. MACHINE-CERTIFIED: link 1 (merged
receipt + 16 chunk receipts), 3-constants (R2 second-pin envelope), 5.
LEAN-PROVED: links 2, 3-joints, 5 (KsZeroLattice), 7b (reflection core).
CITED: Simon Thm 4.2/3.3, Gohberg–Krein/Simon bound, Grothendieck Résumé
Thm 8, MMS Thm 6.4 + Thm 4.10, FJS completed-zeta divisor statement +
one-cusp scalar specialization, standard Selberg/scattering theory.
PAPER-PROOF: restriction identity, mean-value arc-enclosure lemma,
enlarged-disc output-tail bound, R5 v3.1 proofs.

## Constants table (paper-ready; directed rounding)

  s₀ (centre)     = 0.41054373549473627 + 7.81976824701551188 i
  box half-width  = 1e-6 (each coordinate)
  N               = 288 (per component; κ = 3); N* floor = 274
  base arcs       = 192 (48/edge), 16 chunks × 12
  subarc census   = 452 accepted, 260 adaptive splits, max depth ≤ 8
  T_tail(288)     ≤ 1.4251151e-41
  ‖L‖₁ bound      ≤ 37.6839779
  F_R(288)        ≤ 2.0894485e-8
  min margin      ≥ 3.064554329376951375e-8  [rounded DOWN]
  max rH          ≤ 0.49470747 < 1           [rounded UP]
  winding         = 1 (ball width 1.22e-113)
  δ₂ (gap)        ≥ 0.08945526450526372
  ρ-separation    ≥ 0.04334944458020843
