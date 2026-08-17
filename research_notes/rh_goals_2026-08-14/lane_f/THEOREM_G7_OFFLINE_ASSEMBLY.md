# THEOREM ASSEMBLY — a certified off-line Selberg-zeta zero for G_7

Lane F, 2026-08-17. Template: `lane_g/THEOREM_G5_OFFLINE_ASSEMBLY.md` v2
(DECLARED, V4–V8 + Kimi-K3 audited). This document ports the remaining
theorem links from the q=5 flagship to q=7 on top of the banked
closed-contour YES (`lane_f/F7_R3B_ASSEMBLY_CERT.md`).

STATUS: **ASSEMBLED, ONE ADVERSARIAL ROUND PASSED (SOUND-WITH-REPAIRS,
repairs enacted 2026-08-17); NOT YET DECLARED.** `ADVERSARIAL_REVIEW_G7_V1.md`
(independent cold pass, 2026-08-17) ruled **SOUND-WITH-REPAIRS**: no
theorem-level defect, one FALSE printed bound inside the Link-5 lemma (D1,
the det(1−K_s) upper bound — non-load-bearing but false), two editorial
defects (D2 link renumbering, D3 mis-attributed erratum) and two disclosure
defects (D4, D5). All five repairs are enacted in this revision, and the
review's clarifying notes are recorded in §"Review notes". The q=5 chain
earned "THEOREM-GRADE YES" only after **five** adversarial rounds (V4–V8)
plus an independent hostile audit (Kimi K3); q=7 has had **one**. The owner
may commission further rounds before dissemination. Dissemination stays
owner-gated.

New work in the assembly session: **Link 4b** (E1 validity at the box,
re-derived from the banked raw fields) and **Link 5** (the K_s divisor
gate, certified from scratch in ball arithmetic, together with the
det(1−K_7) lemma that closes the "determinant zero ⇒ Z_S zero" step for
this box). Every other link is quoted from an existing artifact with its
status label. Repair session 2026-08-17: this document and
`f7links_ks_gate.py` (with its own receipt) were edited to enact review
defects D1–D5; no other existing file was modified and no `git` command
was run.

## Statement (essential-gap form, the q=5 phrasing instantiated at q=7)

Let G_7 be the Hecke triangle group with λ_7 = 2cos(π/7) (non-arithmetic;
minimal polynomial x³ − x² − 2x + 1), X_7 = G_7\H the finite-area
hyperbolic orbifold, and Z_S(s) its Selberg zeta function.

THEOREM (computer-assisted; dependency ledger below). Z_S has a zero s*
with

  |Re(s*) − 0.4751647621098225| ≤ 10⁻⁶,
  |Im(s*) − 4.668743786424289| ≤ 10⁻⁶.

In particular Re(s*) ≤ 0.4751658 < 1/2: s* lies OFF the critical line
with essential gap

  δ := 1/2 − Re(s*) ≥ 0.0248342.

Since Im(s*) ≈ 4.67 ≠ 0, s* is neither a small-eigenvalue parameter
(those are real) nor a tempered-eigenvalue zero (those lie on
Re(s) = 1/2); by the standard spectral interpretation of finite-area
Selberg zeros in the strip 0 < Re(s) < 1/2, s* is a scattering RESONANCE
of X_7. With the declared G_5 result this is the second member of the
non-arithmetic Hecke family to carry a rigorously localized off-line
resonance, and the first at h_q = 2 (Bruggeman–Pohl leave the
non-arithmetic Hecke resonances conjectural; prior-art sweep lane_c).
**This last sentence is a literature claim, not a certified one**: it rests
on the lane_c prior-art sweep, which was not redone in this session and not
re-run by the V1 reviewer — logged as open item 9 (q=5 class 1-C8,
recurring).

Erratum inherited from the plan: `F7_CERT_PLAN.md` §1 (line 8) prints
"Re(s*) ≤ 0.4751648". That is the box CENTRE rounded up, not a bound on the
closed box; the correct
rounded-up bound is **0.4751658** = 0.4751647621098225 + 10⁻⁶. The
δ ≥ 0.0248342 figure is unaffected (it was computed with the half-width
included; re-verified here as
1/2 − Re₀ − 10⁻⁶ = 0.02483423789017750, rounded DOWN to 0.0248342).
Attribution corrected per review defect D3: an earlier revision of this
paragraph also charged `F7_CONSTANTS_MANIFEST.md` §5 with the same figure.
It does not carry it — manifest §5 line 207 writes
δ = 1/2 − 0.4751647621098225 − 10⁻⁶ = 0.0248342 **with the half-width
included, i.e. correctly**. The erratum is against `F7_CERT_PLAN.md:8` only.
(The separate erratum against the manifest — the 0.5895480 round-UP of the
K_s box margin at manifest lines 210 and 270 — stands and is verified; see
§"Link 5 in detail".)

## Proof chain and verification status of every link

1. FINITE WINDING + CLOSED-CONTOUR EXCLUSION [MACHINE, CERTIFIED].
   det(I − P_N L_{s,+} P_N), N = 256 (matrix 1280×1280, κ_7 = 5),
   has certified argument winding 1 around ∂Box; the boundary is covered
   by 192 closed Acb base arcs (4 × 48), every arc accepted whole
   (adaptive splits 0), assembled from 16 Kaggle chunks of 12 arcs that
   tile [0,192) exactly once with seam closure re-verified at all 192
   junctions including the 191→0 wrap. On every arc the finite Taylor
   enclosure AND the F_R-inflated enclosure exclude 0; minimum certified
   margin (finite lower − F_R) ≥ 2.41285e-6 (rounded DOWN, attained in
   chunk-06); per-arc rH ≤ 0.211065 < 1, rG ≤ 8.88501e-7 (rounded UP).
   Margin quality min(finite lower − F)/F_R ≈ 1.11e3 — the q=7 cert is
   NOT thin (q=5's was 2% of F_R). The designed control arm N = 224
   FAILED as intended (NOT_CERTIFIED in all 16 chunks).
   Receipt: `F7_R3B_ASSEMBLY_CERT.md` + `F7_R3B_ASSEMBLY_RECEIPT.json`
   (384-bit Arb/Acb; all seven assembly gates PASS; immutable R2/TB-V2
   input sha256s consumed unchanged in all 16 chunks).
   Honest note carried forward: the primary engine path
   `.worktrees/aletheia-restore/code/zeta_cert_rosen.py` DRIFTED after
   the run; the certified bytes (`b6ee87fd…e28a0f`) survive at
   `…/out/kaggle_top4/hecke-gap-sweep/zeta_cert_rosen.py`. Also carried
   forward: latent code notes 1-C3 (missing `assert rho >= center_ratio`),
   1-C4 (unguarded FTC direction-ball selection), 1-C5 (two hard-coded
   `True` gate literals — which is why the assembly re-derives the global
   margin from the 192 raw per-arc records).

2. FINITE SECTION = det(I − L P_N) [PAPER + LEAN, q-INDEPENDENT, REUSED].
   The computed matrix determinant equals det_H(I − L P_N) by the
   finite-rank restriction identity + Sylvester
   (`TB_R1_HILBERT_RESTATEMENT.md` Steps 1–2 ONLY; R1 Steps 3–4 are
   SUPERSEDED at q=5 and are not used at q=7 either — the operative F_R
   and endpoint bounds are the q=7 R3b/endpoint receipts'). The
   restriction identity is machine-proved in Lean, Aristotle v18
   `det_one_sub_proj_mul_proj`, axiom-clean, receipt in
   `projects/aristotle_dispatch_v18/project_aristotle/`. The statement is
   about an abstract finite-rank projection, so **nothing in it depends on
   q, κ, or the block list** — reused verbatim.

3. DETERMINANT COMPARISON [PAPER + MACHINE CONSTANTS at q=7 + LEAN JOINTS].
   |det(I−L) − det(I−LP_N)| ≤ T_tail(N)·exp(1 + ‖L‖₁ + ‖LP_N‖₁)
   (Gohberg–Krein/Simon, Trace Ideals Thm 3.4 form; citation-level).
   q=7 machine constants (all from `F7_R3B_ASSEMBLY_RECEIPT.json` and
   `f7_receipts/F7_R3B_ENDPOINT_V2_RECEIPT.json`, N = 256): both endpoint
   norms ≤ 20.1696370 (rounded UP; = computed-row column-2-norm sum
   20.16963692338… + enlarged-disc output-tail corrections 7.7061e-13 +
   T_tail(256)); T_tail(256) ≤ 2.41149e-27 (immutable R2 receipt
   `4e5f0105…9202efc`, 19 families, Hurwitz-closed m = 0, monotone in N);
   F_R(256) ≤ 2.16623e-9 (rounded UP). The B_total = 119.0628556 figure in
   the R2 receipt is a comparison envelope, NOT the theorem-valid endpoint
   bound — the theorem-valid bound is the 20.1697 above.
   Supporting Lean joints (Aristotle v18/v19, axiom-clean [propext,
   Classical.choice, Quot.sound]): `trace_unitary_le_sum_column_norms`,
   `l2_le_card_mul_sup_sq`, `coeff_bound_of_uniform`, `geom_tail_le` — all
   q-independent, reused.

4. TRUE-DETERMINANT ZERO IN BOX [ARGUMENT PRINCIPLE]. Every F_R-inflated
   tube excludes 0 ⇒ the straight-line homotopy det(I−LP_N) → det(I−L)
   never vanishes on ∂Box ⇒ winding of det(I−L_{s,+}) around ∂Box = 1 ⇒
   det(I−L_{s,+}) has exactly one zero s* (with multiplicity) in Box.

4b. HILBERT → BANACH TRANSPORT [PAPER-PROOF q-INDEPENDENT + MACHINE at q=7].
   det_H(1 − L_{s,+}) = det_B(1 − L_{s,+}^{MMS}) on Ω* ⊃ Box, by
   `TB_R5_DETERMINANT_IDENTIFICATION.md` v3.1 with its machine constants
   re-pointed at the q=7 receipts. See §"Link 4b in detail" below for what
   E1 requires at q=7 and which banked numbers discharge it. q=7 constants:
   ρ̂ ≤ 0.9152412 (rounded UP; worst block 5→3 +1 head), η ≤ 0.8695653 for
   all 19 blocks, min remaining pole/branch-cut clearance ≥ 0.9915 > 0.
   Receipt: `f7_receipts/F7_E1_ENLARGED_CONTRACTION_V2_RECEIPT.json`
   (schema `f7-e1-enlarged-contraction/v2`, verdict `PASS_RHO_HAT_LT_1`),
   re-derived block-by-block from its raw ball fields in
   `f7_receipts/F7LINKS_E1_RECHECK_RECEIPT.json` (this session).

5. NO DIVISOR CANCELLATION + Z_S IDENTIFICATION [MACHINE, CLOSED at q=7].
   det(1−K_s) ≠ 0 on Box — the load-bearing claim, and the only one the
   R5 identification consumes — with the certified lower bound
   |det(1−K_s)| ≥ 0.936818983390 for every s in the closed Box (rounded
   DOWN). The certified elementary upper bound is |det(1−K_s)| ≤
   1.063204693008 (rounded UP; grid-measured true modulus ≈ 1.0295836).
   The K_s divisor is the exact lattice s = −n + iπk/a_7 (n ≥ 0, k ∈ ℤ),
   all Re ≤ 0; certified box-to-lattice distance ≥ **0.5895479**. See
   §"Link 5 in detail, part 1 — the K_s divisor gate at q=7" and part 2.
   Receipt (new): `f7links_ks_gate.py` →
   `f7_receipts/F7LINKS_KS_GATE_RECEIPT.json`, verdict
   `PASS_KS_BOX_CLEAR_AND_DETK_NONVANISHING`.

6. SELBERG-ZETA FACTORIZATION [PUBLISHED, CITED]. MMS Theorem 6.4:
   Z_S(s) = det(1−L_{s,+})·det(1−L_{s,−}) / det(1−K_s). The factor
   det(1−L_{s,−}) is analytic near Box (MMS Theorem 4.10: the MMS
   determinants are meromorphic with poles only on the real points
   s = (1−k)/2; Box has Im ≈ 4.67). The q=5 footnote appears not to be
   needed here: per the MMS heading condition as transcribed in
   `F7_CONSTANTS_MANIFEST.md` — "q = 2h_q + 3 > 5" above MMS eq. (34) —
   the condition holds at q = 7 arithmetically (2·2 + 3 = 7 > 5). **The
   heading's source text is not banked in-repo (no MMS e-print or PDF in
   the tree), so this is a TODO-VERIFY against the e-print, not a
   repo-verifiable claim** (review defect D5; open item 8). Lemma 4.2
   (q ≥ 5) is still cited for the reduced-sector validity.
   Journal-numbering caveat inherited from
   `lane_g/LAW_Q3_BRANCH_DIAGNOSIS.md` §1: the arXiv e-print labels the
   factorization `\label{main-theorem}` with no printed number — confirm
   DCDS 32 (2012) 2453–2484 numbering before printing "Theorem 6.4".

7. RESONANCE INTERPRETATION [STANDARD, CITED]. For finite-area surfaces,
   Z_S zeros in 0 < Re(s) < 1/2 off the real axis are resonances
   (scattering poles of the meromorphically continued
   resolvent/scattering matrix); discrete-spectrum zeros lie on
   Re(s) = 1/2 or on the real segment. Citations: Hejhal LNM 1001;
   Iwaniec, Spectral Methods, ch. 10–11; Borthwick for the resonance
   framing. Im(s*) ≈ 4.67 excludes the discrete alternatives.

## Link table — status per link

| # | Link | Status | Evidence |
|---|---|---|---|
| 1 | Closed-contour winding 1 at N=256 | **CERTIFIED** (machine, q=7) | `F7_R3B_ASSEMBLY_CERT.md` / `…RECEIPT.json` |
| 2 | Finite section = det(I−LP_N) | **PROVED** (Lean, q-independent, reused) | Aristotle v18 `det_one_sub_proj_mul_proj` |
| 3 | Gohberg–Krein comparison | **CITED** + **CERTIFIED** constants (q=7) | Simon; `F7_R3B_ENDPOINT_V2_RECEIPT.json` |
| 4 | Zero in box by argument principle | **PROVED** (from 1 + 3) | this document |
| 4b | Hilbert → Banach (R5 Clauses 1–3) | **PROVED** (paper, q-independent) + **CERTIFIED** (q=7 E1) | `TB_R5_…md` v3.1; `F7_E1_…V2_RECEIPT.json`; `F7LINKS_E1_RECHECK_RECEIPT.json` |
| 5 | det(1−K_7) ≠ 0 on box ⇒ Z_S zero | **CERTIFIED** (machine, q=7, new) | `F7LINKS_KS_GATE_RECEIPT.json` |
| 6 | MMS factorization + pole set | **CITED**; heading condition holds at q=7 arithmetically, source text **TODO-VERIFY** (D5) | MMS Thm 6.4, Thm 4.10, Lemma 4.2; heading as transcribed in `F7_CONSTANTS_MANIFEST.md` |
| 7 | Resonance interpretation | **CITED** (standard) | Hejhal; Iwaniec; Borthwick |
| 8 | Adversarial review of THIS assembly | **ONE ROUND PASSED** (SOUND-WITH-REPAIRS; repairs D1–D5 enacted 2026-08-17). Not equivalent to q=5's five rounds + hostile audit | `ADVERSARIAL_REVIEW_G7_V1.md` |
| 9 | Lean statement of the q=7 K_s lattice | **GAP (minor)** | q=5 had v17 `KsZeroLattice`; no q=7 dispatch. The 384-bit ball certificate of Link 5 stands in; the Lean joint would be a formalization of an already-machine-certified finite computation |

## Link 5 in detail, part 1 — the K_s divisor gate at q=7

(Renumbered per review defect D2: this section carries LINK 5's content. An
earlier revision headed it "Link 4 in detail", which collided with the
chain's Link 4 = argument principle. Link 4 needs no detail section; its
detail is the chain entry plus Link 1's certificate.)

Receipt: `f7links_ks_gate.py` → `f7_receipts/F7LINKS_KS_GATE_RECEIPT.json`
(python-flint Arb/Acb, 384 bits, `PASS_KS_BOX_CLEAR_AND_DETK_NONVANISHING`).
Nothing is taken from `F7_CONSTANTS_MANIFEST.md`; every constant is
recomputed from λ_7 = 2cos(π/7) upward and only THEN compared with the
manifest.

Certified chain (each step a ball computation):

1. λ_7 = 2cos(π/7) satisfies m(λ) = λ³ − λ² − 2λ + 1 (the ball
   m(λ_7) contains 0). Degree 3 — the golden-ratio identity of q=5 is
   correctly absent.
2. MMS Lemma 6.3 at h_7 = 2 gives A_s = L_{1,s}² L_{2,s} L_{1,s} L_{2,s}
   (the L_1^{h−1} factor that VANISHES at h_5 = 1), matrix word
   M_2 M_1 M_2 M_1 M_1 with M_n = [[0,−1],[1, nλ_7]]. In balls:
   det = 1 (contains 1), trace − (4λ_7² + 3λ_7) contains 0, and
   τ_7 ≥ **18.393731622284383001616652** (rounded DOWN) > 2, so the word
   is hyperbolic.
3. ell_7 = (τ_7 − √(τ_7²−4))/2 = 0.05452799479805249083392519594349…,
   μ₊μ₋ = 1 verified in balls; a_7 = −log ell_7 =
   2.909041043174856595598222179862…; spacing π/a_7 =
   1.079940986381249360096096828198…. All three agree with the
   manifest's printed digits (checked to 1 ulp of the printed place — the
   manifest prints truncations, so ball CONTAINMENT of the printed string
   is the wrong test and is not what is asserted).
4. Zero lattice: det(1−K_s) = Π_{n≥0}(1 − ell_7^{2s+2n}) vanishes iff
   ell_7^{2(s+n)} = 1, i.e. s = −n + iπk/a_7, n ≥ 0, k ∈ ℤ. **Every
   lattice point has Re ≤ 0**, and the closed Box has
   Re ≥ 0.4751637 > 0, so the gate is a finite distance computation.
5. BOX-to-lattice distance (not centre-to-lattice — Kimi erratum 1-E6
   applied at the outset): nearest point is (n,k) = (0,4) at
   Im = 4.319763945524997…; distance ball
   [0.5895479897495818278130858801517574259447 ± 3.93e-41], hence

     **box-to-lattice distance ≥ 0.5895479 (rounded DOWN).**

   Second-nearest point (0,5): box distance ≥ 0.8718275.
   The centre-to-lattice distance is 0.5895493876724655… and reproduces
   the manifest's point margin 0.589549387672466.

**Erratum against the manifest.** `F7_CONSTANTS_MANIFEST.md` §4.3/§7 print
the box margin as "≈ 0.5895480". The true value is 0.58954798975…, so
0.5895480 is a round-UP and overstates the margin by 1.0e-8. Rounded DOWN
the honest figure is **0.5895479**, which is what this document and the
receipt carry (same class of error as the q=5 min-margin erratum
3.43787e-8 → 3.43786e-8). The gate is unaffected: the margin exceeds the
box half-diagonal √2·10⁻⁶ by more than five orders of magnitude.

Independent cross-check of the algebra: `lane_g/LAW_Q3_BRANCH_DIAGNOSIS.md`
§1.2 computes the same divisor from a DIFFERENT route — MMS's Proposition
spectrum b_q = Π_{l<κ_q}(f_q^l(r_q))² over the orbit of
r_7 = [0; \overline{1,1,2,1,2}], κ_7 = 5, giving b_7 = 0.0029733022166964396
(`lane_g/law_probes/q3diag_detK.json`). The receipt verifies
ell_7² = 0.00297330221669643950… agrees with that value to its printed
place. Two independent derivations (trace of the Lemma-6.3 word vs. the
orbit product) of the same divisor.

## Link 4b in detail — what E1 requires at q=7, and what discharges it

**First, a distinction the banked numbers make easy to conflate.** The
per-arc quantities rG ≤ 8.88501e-7 and rH ≤ 0.211065 < 1 of
`F7_R3B_ASSEMBLY_CERT.md` §5 belong to LINK 1: they are the mean-value /
self-consistency device that turns a midpoint determinant value into a
certified enclosure over a closed sub*arc of the s-contour*. **They do
NOT discharge E1.** E1 is a statement about the z-geometry of the
transfer-operator branches, uniform in s over the box, and needs its own
certificate. `rH < 1` and `ρ̂ < 1` are different constants about different
objects; the q=5 assembly keeps them separate too (and warns explicitly
against conflating ρ̂ with ρ*).

**What E1 must supply**, reading `TB_R5_DETERMINANT_IDENTIFICATION.md`
Clause 2(a) at q=7 (κ = 5, 19 blocks, discs D_1…D_5):

- (E1-i) an enlargement D_i^ε := D(c_i, R_i + e_i) with e_i > 0 on which
  **every branch of every block family is holomorphic**, i.e. the
  pole/branch-cut clearance survives the enlargement — the receipt's
  "remaining pole/cut clearance > 0";
- (E1-ii) uniform contraction of the enlarged source into the target disc:
  sup_{z ∈ cl(D_i^ε)} |θ_n(z) − c_j| / R_j ≤ ρ̂ < 1, over **all 19**
  families, with the tails handled by the finite-head/deep-tail split and
  the monotone first-n bound so that the choice is uniform in n;
- (E1-iii) nothing else. In particular the block-weight sup W_B^ε is used
  only for FINITENESS (Kimi 1-E9 presentational fix), so no numerical
  weight bound is owed. ρ̂ < 1 then gives the point-evaluation bound
  (1 − ρ̂²)^{−1/2}, hence L_s^H : H → B ⊂ H bounded with the same action
  as L_s^B, which is what Clauses 2(b) (Jordan-chain spectrum equality)
  and 2(c) (both determinants spectral: Simon Thm 4.2; Grothendieck
  Résumé Thm 8 via MMS §4/Thm 4.10 nuclearity of order 0) consume.
  Clauses 2(b), 2(c), 3 and the identity-theorem step are
  **q-independent paper-proofs** — they quantify over "the reduced system
  of Clause 1", not over κ = 3.

**Does q=5's E1 need anything beyond ρ̂ < 1?** Yes, exactly one thing, and
it is (E1-i): q=5's certificate reports min pole/cut margin ≥ 1.0023,
which is what licenses the flat ε = 0.1 enlargement (1.0023 > 0.1). Both
conditions are ported.

**What discharges E1 at q=7.** `f7_receipts/F7_E1_ENLARGED_CONTRACTION_V2_RECEIPT.json`
(384-bit Arb, 512 enlarged-contour arcs per block, all 19 blocks,
verdict `PASS_RHO_HAT_LT_1`), produced by `f7_stage4b_reopt.py` and
reported in `F7_4B_REOPT_REPORT.md` gate 2. Re-derived this session,
block-by-block, from that receipt's raw ball fields — no summary literal
trusted — in `f7_receipts/F7LINKS_E1_RECHECK_RECEIPT.json`
(`PASS_E1_REDERIVED_FROM_RAW_FIELDS`, 19/19 blocks, 10 checks each):

- (E1-ii) ρ̂ = max over 19 blocks of the enlarged-contour ratio
  ≤ **0.9152412** (rounded UP), worst block 5→3 (+1) head — the same
  block that binds the un-enlarged ρ* ≤ 0.763213, so the geometry is
  consistent rather than pathological. Below the q=5 chain's own
  ρ̂ ≤ 0.948344.
- (E1-i) every block's remaining pole/branch-cut clearance is strictly
  positive, minimum ≥ 0.9915 (block 3→1 +1 head) against enlargements
  e_i ≤ 0.15·R_i ≤ 0.0429 — three orders of headroom is not claimed, but
  a factor ≳ 23 is.
- Internal consistency re-derived per block: R_enl = R + e, η = R/R_enl
  ≤ 0.8695653 < 1 for all 19, remaining clearance = clearance − e, and
  e = min(clearance/4, 0.15·R) as the receipt's recorded rule states.

**Honest caveats on Link 4b.** (i) The relative cap 0.15 is a CHOSEN
constant, exactly like q=5's ε = 0.1 and like the ρ* gate 0.80; what is
certified is ρ̂ ≤ 0.9152 *at that cap*, and the receipt records the cap.
(ii) The q=5 → q=7 port of the enlargement rule was initially a defect
(`F7_4B_REOPT_REPORT.md` §1: "clearance/4" produced 2–6× radius blow-ups
at q=7's small discs and large clearances, ρ̂ > 1, F_R ≈ 1.98e+61452309);
the surgical relative cap fixed it and the adopted radii did not change.
The blocked smoke receipts under `f7_receipts/smoke/` are left in place as
the historical record. (iii) The E1 certificate is a re-run of the same
method, not an independent implementation; the "twice independently"
status q=5 enjoys (our run + the V7 reviewer's diagnostic) has no q=7
analogue yet.

## Link 5 in detail, part 2 — determinant zero ⇒ Z_S zero, at this box

`lane_g/LAW_Q3_BRANCH_DIAGNOSIS.md` established (Q3D.2, Q3D.7) that the
repo engines compute MMS's NUMERATOR det(1−L_{s,+})·det(1−L_{s,−}) only,
and that the omitted divisor det(1−K_s) = Π_{n≥0}(1 − b_q^{s+n}),
b_q = ell_q², is zero-free on Re s > 0. That closes the identification
step for this box, as follows.

> **LEMMA (Z_S zero at the q=7 flagship box).** Let
> Box = { |Re s − 0.4751647621098225| ≤ 10⁻⁶,
> |Im s − 4.668743786424289| ≤ 10⁻⁶ }, and let b_7 = ell_7² =
> 0.00297330221669643950…, so
> det(1 − K_s) = Π_{n≥0}(1 − b_7^{s+n}). Then for every s ∈ Box
>
>   0.936818983390 ≤ |det(1 − K_s)| ≤ 1.063204693008,
>
> both bounds certified in 384-bit ball arithmetic (lower rounded DOWN,
> upper rounded UP). **The load-bearing claim is NON-VANISHING, i.e. the
> LOWER bound alone** — that is all the R5 identification step below
> consumes; finiteness follows from Σ_n t_n < ∞ and needs no numeric bound.
> The upper bound is elementary context: it is Π_{n≥0}(1 + t_n), not tight,
> and the true modulus on this box is ≈ 1.0295836 (grid-measured, not
> certified). Consequently
> det(1 − K_s) is finite and non-vanishing on Box, and by MMS Theorem 6.4
> together with the analyticity of det(1−L_{s,−}) near Box (Theorem 4.10:
> poles only at the real points s = (1−k)/2; Box has Im ≈ 4.67), the zero
> s* of det(1 − L_{s,+}) supplied by Links 1–4b is a zero of Z_S with
> multiplicity at least that of the + factor.

*Proof of the numeric part (as executed in `f7links_ks_gate.py`).* Write
σ_lo := inf_{Box} Re s ≥ 0.4751637 > 0. For every s ∈ Box and every
n ≥ 0, |b_7^{s+n}| = ell_7^{2Re s + 2n} ≤ ell_7^{2σ_lo + 2n} =: t_n, and
t_0 ≤ 0.063004963347 < 1, so each factor satisfies
|1 − b_7^{s+n}| ≥ 1 − t_n ≥ 1 − t_0 ≥ 0.936995036653 > 0. Therefore
|det(1−K_s)| ≥ Π_{n<24}(1 − t_n) · (1 − Σ_{n≥24} t_n) with
Σ_{n≥24} t_n = t_0·ell_7^{48}/(1 − ell_7²) ≤ 1e-60, giving the stated
lower bound 0.936818983390 (rounded DOWN) — which is the load-bearing
non-vanishing claim. For the upper bound, |1 − b_7^{s+n}| ≤ 1 + t_n on
every factor, so |det(1−K_s)| ≤ Π_{n≥0}(1 + t_n) ≤ Π_{n<24}(1 + t_n) ·
exp(Σ_{n≥24} t_n) ≤ 1.063204693008 (rounded UP), using 1 + t ≤ e^t on the
tail. ∎

*Repair note (review defect D1).* An earlier revision printed the upper
bound as 1.000000000001, from `1 + Σ_{n≥24} t_n`. That is **not** an upper
bound on |Π_{n≥0}(1 − z_n)|: it applies |1 − z| ≤ 1 + |z| to the tail only
and drops the n = 0 factor, whose modulus exceeds 1 because b_7^{s} is far
from the positive reals (arg ≈ −2.0304 rad, modulus ≈ 0.06300460). The true
modulus on the box is ≈ 1.0295836, so the old figure was FALSE by ≈ 3%,
not merely loose. `f7links_ks_gate.py` now computes Π_{n<24}(1 + t_n)·
exp(tail) in balls, rounded UP, and the receipt field
`abs_detK_upper_bound_rounded_up` reads `1.063204693008`. Nothing
load-bearing changed: the lower bound, the box, δ, and the conclusion are
untouched.

Two consequences worth stating plainly:

- **The identification link is now CLOSED for this box by a machine
  certificate, not by a citation-level appeal.** At q=5 the corresponding
  step rested on the K_s lattice being confined to Re ≤ 0 plus a
  point-margin artifact (Kimi 1-E6); here the divisor is certified
  bounded away from 0 on the closed box — which is the whole of what the
  identification consumes — with an elementary finite upper bound
  alongside it.
- **The LAW numerator defect does not touch this theorem.** The certified
  winding is of the + sector's Fredholm determinant, and the divisor
  correction on this box multiplies |Z_S| by a factor whose certified
  range is [0.936818983390, 1.063204693008] — grid-measured, the true
  modulus is ≈ 1.0295836, so the magnitude effect is **≈ 2.9%** (division
  by 1.0295836); the certified elementary bounds allow at most ~6.3%
  in either direction (1 − 0.9368 = 6.32%, 1.0632 − 1 = 6.32%). The
  load-bearing clause is unchanged and does not
  depend on either number: the divisor moves NO zero, because on this box
  it neither vanishes nor blows up. Magnitude
  claims elsewhere (and any winding on Re s ≤ 0) remain subject to
  `LAW_Q3_BRANCH_DIAGNOSIS.md` §5.

## Convention and sector honesty

- L_{s,+} is the MMS P-symmetric (CF-reflection) sector of eq. (34),
  q = 7 (`reduced3`, κ_7 = q−2 = 5, h_7 = 2), 19 blocks = 9 heads + 10
  Hurwitz tails, as implemented by the certified engine with sign = +1.
- The P-sectors are NOT the geometric even/odd Maass sectors; the
  statement above deliberately claims **no parity label** for the
  resonance. This is open at q=5 and stays open at q=7 — porting did not
  improve it.
- The mms− (sign = −1) q=7 scan found 12 pins all within 5e-10 of
  Re(s) = 1/2, consistent with tempered-eigenvalue zeros and useless for
  an off-line statement; the off-line cloud lives in mms+ at q=7 exactly
  as at q=5.
- Basis/norm setting: H = ⊕_{i=1..5} H²(D_i), normalized monomials; b_k
  are H²-norm bounds via sup ≥ H² norm (R1 Step 1).

## Dependency classes (for the paper's preamble)

- MACHINE-CERTIFIED (Arb/Acb interval receipts, replayable): Link 1
  (`F7_R3B_ASSEMBLY_RECEIPT.json` + the 16 chunk receipts), Link 3
  constants (`F7_R3B_ENDPOINT_V2_RECEIPT.json`, `F7_R2_FLAGSHIP_ENVELOPE_RECEIPT.json`,
  `F7_TB_BLOCK_CERTIFICATES_RECEIPT.json`), Link 4b
  (`F7_E1_ENLARGED_CONTRACTION_V2_RECEIPT.json`, re-derived in
  `F7LINKS_E1_RECHECK_RECEIPT.json`), Link 5
  (`F7LINKS_KS_GATE_RECEIPT.json`). Named dependency: python-flint
  Arb/Acb ball-matrix enclosure semantics.
- LEAN-PROVED (Aristotle v18/v19, axiom-clean, q-independent, REUSED):
  the abstract joints named in Links 2 and 3. **Not reused:** q=5's v17
  `KsZeroLattice`, which is a q=5 statement; the q=7 analogue is Link
  table row 9 (GAP, minor).
- CITED PUBLISHED THEOREMS: Simon, "Notes on infinite determinants,"
  Adv. Math. 24 (1977) Thm 3.3 (analyticity), Thm 4.2 eq. (4.2)
  (trace-class determinant product; Lidskii = Cor. 4.3, not used);
  Gohberg–Krein/Simon perturbation bound in Link 3's form;
  Grothendieck, Résumé (1952) Thm 8 (2/3-nuclear canonical product,
  Link 4b); MMS Theorem 6.4, Theorem 4.10, Lemma 4.2, eq. (34), §6.2
  eqs. (42)–(43) + Lemma 6.3 + Proposition (K_s spectrum);
  Bandtlow–Jenkinson ETDS 28 (2008) Thm 4.2 (corroboration only);
  standard Selberg/scattering theory (Link 7).
- PAPER-PROOF (short, self-contained): the restriction-identity assembly
  (R1 Steps 1–2), the mean-value arc-enclosure lemma and the
  enlarged-disc Cauchy output-tail bound (`F7_R3B_ASSEMBLY_CERT.md` §7),
  R5's smoothing / Jordan-chain / Ω*-holomorphy clauses, and the Link 5
  lemma above.

## Constants table (paper-ready; error bounds rounded UP, everything else DOWN)

  s₀             = 0.4751647621098225 + 4.668743786424289 i (mms+, sign +1)
  box half-width = 1e-6 (each coordinate)
  q, h_q, κ_q    = 7, 2, 5;  blocks = 19 (9 heads + 10 tails)
  λ_7            = 1.801937735804838252472204639014890102331…;  m(x) = x³−x²−2x+1
  N              = 256 per component (matrix 1280×1280); control arm N = 224 FAILS
  base arcs      = 192 (4 × 48), accepted whole, adaptive splits 0, 16 chunks
  disc radius strings = 3.522, 2.622, 2.372, 1.79, 1.6
  ρ*             ≤ 0.763213   (TB V2 certified un-enlarged contraction)
  ρ̂              ≤ 0.9152412  (E1 enlarged-disc contraction, Link 4b ONLY —
                   distinct constant, do not conflate with ρ*)
  η = R/R_enl    ≤ 0.8695653  (all 19 blocks; relative cap 0.15)
  min remaining pole/cut clearance ≥ 0.9915
  T_tail(256)    ≤ 2.41149e-27
  ‖L‖₁, ‖LP_N‖₁  ≤ 20.1696370
  F_R(256)       ≤ 2.16623e-9
  min margin     ≥ 2.41285e-6   (finite lower − F_R, rounded DOWN, chunk-06)
  margin / F_R   ≈ 1.11e3
  rG             ≤ 8.88501e-7;   rH ≤ 0.211065 < 1
  winding        = 1 (ball width 5.17e-114)
  τ_7            ≥ 18.393731622284383001616652;  det of the word = 1
  ell_7          = 0.05452799479805249083392519594349…;  b_7 = ell_7²
  a_7            = 2.909041043174856595598222179862…;  π/a_7 = 1.0799409863812493600960968281…
  K_s box margin ≥ 0.5895479   [manifest's 0.5895480 is a round-UP; see Link 5]
  |det(1−K_s)| on Box ∈ [0.936818983390, 1.063204693008]
                 (LOWER = the load-bearing non-vanishing bound; UPPER =
                  elementary Π(1+t_n) context bound; true modulus ≈ 1.0295836
                  grid-measured, not certified)
  Re(s*)         ≤ 0.4751658   [plan's 0.4751648 omits the half-width]
  δ (gap)        ≥ 0.0248342

## What remains open — q=7 versus the declared q=5 chain

1. **Adversarial review depth.** q=5 survived V4–V8 plus the Kimi K3
   hostile audit; this assembly has had ONE independent hostile round
   (`ADVERSARIAL_REVIEW_G7_V1.md`, SOUND-WITH-REPAIRS, repairs enacted).
   That round read code and receipts and re-derived every constant, but did
   not open Simon, Grothendieck or MMS, ran no Lean build, and did not
   re-execute the 107.8-hour contour certification or the E1 run from
   scratch. Until the owner is satisfied with the round count, the honest
   label stays ASSEMBLED, not DECLARED.
2. **Lean coverage of the q=7 K_s lattice** (Link table row 9). Minor: it
   would formalize a finite computation that is already ball-certified.
3. **MMS sector labeling.** No geometric parity claim, at either q. Open
   at q=5, unchanged here.
4. **E1 not independently re-implemented** at q=7 (only re-derived from
   raw fields). The chosen cap 0.15 is a constant, not a theorem.
5. **Engine-path provenance drift** after the Kaggle run (Link 1); the
   certified bytes exist elsewhere in the repo and every chunk agrees on
   the hash, but any re-run must restore the pinned bytes first.
6. **Latent code notes 1-C3/1-C4/1-C5** carried forward from the q=5
   runner; 1-C5 is mitigated in the assembly (raw-field re-derivation),
   1-C3/1-C4 remain unguarded asserts to add before any re-run.
7. **m₀ non-rigor.** The N* freeze used a 96-point float sample at N=32;
   it is a planning gate only and no theorem statement depends on it (the
   theorem consumes the certified F_R and the certified boundary minimum).
8. **MMS primary-source items, both `TODO-VERIFY`** (review defect D5):
   (a) the journal numbering of the factorization theorem (LAW §1); and
   (b) the **heading text above eq. (34)** on which Link 6's dissolution of
   the q=5 footnote rests. No MMS e-print or PDF is banked in this repo, so
   the heading wording is currently taken from the transcription in
   `F7_CONSTANTS_MANIFEST.md`. Verify both against the e-print, or paste
   the heading into the manifest as a quoted source line, before printing.
9. **The h_q = 2 priority claim is not repo-verifiable** (review defect D4;
   q=5 class 1-C8, recurring). "The first at h_q = 2" and "the second
   member of the non-arithmetic Hecke family" rest on the lane_c prior-art
   sweep, which was not redone in this session and not re-run by the V1
   reviewer. Either redo the sweep or downgrade the sentence to a citation
   of lane_c before any priority claim is circulated.

Things that are BETTER at q=7 than at q=5, for the record: the boundary
margin is ~1.11e3 × F_R instead of 2% of F_R; ρ̂ is 0.9152 instead of
0.9484; the K_s box margin is 0.5895 instead of 0.4551 (and is a box
margin from the outset, not a point margin); and the MMS eq.-(34) heading
condition holds at q = 7 arithmetically, so the q=5 erratum footnote looks
unnecessary — subject to open item 8(b).

## Review notes (from `ADVERSARIAL_REVIEW_G7_V1.md`, non-defect findings)

Two anomalies a referee may hit are explained here so they are not
re-litigated:

- **The 16 per-chunk margin minima cluster into four near-identical groups
  by chunk index mod 4** (≈2.81662e-6 / 2.43478e-6 / 2.41285e-6 /
  2.72361e-6, agreeing to ~8 significant digits across groups) even though
  the groups sit on different edges of the box. This is NOT a copy-paste
  artifact: each 48-arc edge is split into exactly 4 chunks of 12, so chunk
  index mod 4 **is** position-within-edge, and over a box of diameter 2e-6
  the determinant is near-constant while the four edges are near-symmetric.
  The reviewer independently confirmed each chunk's own `chunk_arc_range`,
  the 48-per-edge `edge_name` census, and that the 192 `s_start`/`s_end`
  balls form one closed cycle — the four groups are genuinely distinct
  arcs, not duplicated records.
- **E1's disc radii are not the R2 receipt's radius balls, and the balls do
  not overlap.** E1 block 1's `original_radius_upper_bound` =
  0.174393823623839918698224185000000418… against the R2 receipt's
  certified radius [0.174393823623839918698223815347389… ± 2.19e-115];
  they diverge at ~3.7e-21. The direction is **conservative** for the
  source enlargement (the field is an upper bound), and the induced
  perturbation of the ρ̂ ratio is ~1e-20 against 0.0848 of headroom to 1,
  so the gate cannot flip. Stated here so the difference is not read as a
  geometry mismatch between Link 1's operator and Link 4b's certificate.

## Reproduce

```bash
/Users/za/.venvs/farey-rh/bin/python \
  research_notes/rh_goals_2026-08-14/lane_f/f7links_ks_gate.py
/Users/za/.venvs/farey-rh/bin/python \
  research_notes/rh_goals_2026-08-14/lane_f/f7links_e1_recheck.py
```

Both are read-only apart from their own receipts under `f7_receipts/`
(`F7LINKS_KS_GATE_RECEIPT.json`, `F7LINKS_E1_RECHECK_RECEIPT.json`).
Wall time: < 2 s each.

READY FOR JUDGING
