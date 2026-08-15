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
   per edge, adaptive split budget depth 8, achieved max depth 1 —
   receipt census 100 depth-0 + 184 depth-1); on every subarc the finite
   Taylor enclosure AND the F_R-inflated enclosure exclude 0; minimum
   certified margin (finite lower − F_R) ≥ 3.43786e-8 (lower bound,
   rounded down; receipt ball 3.4378649…e-8); per-subarc
   self-consistency rH ≤ 0.359 < 1. Receipt:
   R3B_FLAGSHIP_CERT_RECEIPT.json (384-bit Arb/Acb; all_theorem_gates_
   pass = True; immutable input shas verified). Independent frontier
   re-checks (2026-08-15): all 284 records' four gates true; min margin
   recomputed from raw fields ≥ 3.437864e-8; 71×4 subarc census.
   Serialization caveat (Kimi audit 1-E4): the printed per-arc increment
   deltas reconstruct winding = 1 only to ~1e-99, not to the receipt
   ball's 7.81e-114 — full replay of the tighter ball requires re-running
   the pinned code, not the serialized deltas alone.

2. FINITE SECTION = det(I − L P_N) [PAPER + LEAN]. The computed matrix
   determinant equals det_H(I − L P_N) by the finite-rank restriction
   identity + Sylvester (TB_R1_HILBERT_RESTATEMENT.md Steps 1–2 ONLY —
   R1's Steps 3–4 are SUPERSEDED: its Step-3 F_R used the voided
   B_tot = 97.77 envelope and its line-27 geometric-tail claim is
   disowned by R5 v3.1; the operative F_R and endpoint bounds are the
   R3b report's. The restriction identity is machine-proved in Lean,
   Aristotle v18 det_one_sub_proj_mul_proj, axiom-clean — receipt
   downloaded 2026-08-15 to projects/aristotle_dispatch_v18/
   project_aristotle/ (sorry-free; one documented statement adjustment:
   the Euclidean column written via WithLp.toLp, same L² norm). Erratum
   note: until 2026-08-15 the repo held only the dispatch file with
   sorry placeholders; the proof existed server-side since 2026-08-14
   but was unreceipted locally — found by the Kimi K3 audit (1-E1)).

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
   KS_CROSSCHECK.md); Box sits at Re ≈ 0.454 > 0. Precision note (Kimi
   1-E6): the recorded G_5 distance 0.4551002 is center-to-lattice, not
   box-to-lattice; the box half-diagonal √2·1e-6 is 5 orders below it,
   so nonvanishing on the closed Box follows, but the artifact itself
   records a point margin.

6. SELBERG-ZETA FACTORIZATION [PUBLISHED, CITED]. MMS Theorem 6.4:
   Z_S(s) = det(1−L_{s,+})·det(1−L_{s,−}) / det(1−K_s). The factor
   det(1−L_{s,−}) is analytic near Box (the MMS determinants are
   meromorphic with poles only on the real line, s = (1−k)/2 type;
   Box has Im ≈ 5.76). Hence Z_S(s*) = 0 with multiplicity ≥ that of
   the + factor. (Pole-set claim re-checked in review: V4 cleared it,
   and the Kimi K3 audit verified Thm 4.10's pole statement verbatim
   against the MMS primary PDF.) MMS source caveat (V7/V8/Kimi 1-E7):
   the heading above MMS eq. (34) prints "q = 2h_q + 3 > 5" while
   Lemma 4.2 states q ≥ 5; the q = 5 identification rests on the
   general incidence formula, not the displayed heading. The paper must
   carry this footnote.

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
  3-constants, 4b (E1_ENLARGED_CONTRACTION_RECEIPT.json), 5. Named
  dependency for the paper preamble: python-flint Arb/Acb ball-matrix
  enclosure semantics.
- LEAN-PROVED (Aristotle v17/v18/v19, axiom-clean, receipts in
  projects/aristotle_dispatch_v1*/project_aristotle/): the abstract
  joints named in links 2, 3, 5.
- CITED PUBLISHED THEOREMS: Simon, "Notes on infinite determinants,"
  Adv. Math. 24 (1977) Thm 4.2 (trace-class det multiplicativity;
  Lidskii = Cor. 4.3) and Thm 3.3 (analyticity); Gohberg–Krein/Simon
  perturbation bound in the form used by link 3; Grothendieck, Résumé
  (1952) Thm 8 (2/3-nuclear canonical product, link 4b); MMS Theorem
  6.4 and Theorem 4.10 (link 4b/6); standard Selberg/scattering theory
  (link 7). [Erratum 2026-08-15: this ledger previously cited "Simon
  Trace Ideals Thm 3.4/3.7" only, the pre-V7 binding, and omitted
  link 4b's citations; corrected per R5 v3.1 (Kimi 1-E3).]
- PAPER-PROOF (short, self-contained, in R1 Steps 1–2 / R3b / R5
  reports): the restriction identity assembly, the mean-value
  arc-enclosure lemma, the enlarged-disc Cauchy output-tail bound, and
  R5's smoothing, Jordan-chain spectrum-equality, and Clause-3 (Ω*
  holomorphy) proofs.

## Review clearance record

The pre-declaration checklist (items a–g originally addressed to V4:
arc-enclosure lemma, enlarged-disc analyticity, cover completeness,
argument-increment/homotopy, F_R arithmetic, independent
spot-recomputes, MMS pole set) was CLEARED across V4–V8; the Kimi K3
audit (ADVERSARIAL_AUDIT_KIMI_K3.md) independently re-verified the
margin arithmetic, contour closure, ball-arithmetic integrity,
operator-vs-MMS match, and all nine provenance hashes. Process note
(Kimi 1-E8): V8's ruling covers the pre-04:39 bytes; the two
V8-prescribed editorial fixes were applied minutes later within the
same commit d3ba0ed and are verified correct by the Kimi audit.

## Constants table (paper-ready)

  s₀            = 0.4538951800749447 + 5.7635372417301305 i
  box half-width = 1e-6 (each coordinate)
  N             = 160 (per component; κ = 3)
  ρ*            = 0.697802 (certified branch contraction, TB_V2)
  ρ̂             = 0.948344 (E1 enlarged-disc contraction, link 4b ONLY
                  — distinct constant, do not conflate with ρ*)
  T_tail(160)   = 6.26786e-22
  ‖L‖₁ bound    = 17.2911968
  F_R(160)      = 1.77974e-6
  min margin    = 3.43786e-8  [lower bound; rounded DOWN from the
                  receipt ball 3.4378649…e-8. Erratum 2026-08-15: a
                  previous quote 3.43787e-8 rounded up, overstating]
  winding       = 1 (ball width 7.81e-114)
  δ (gap)       ≥ 0.0461038
