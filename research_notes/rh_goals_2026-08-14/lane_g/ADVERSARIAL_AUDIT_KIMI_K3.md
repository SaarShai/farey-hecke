# ADVERSARIAL AUDIT — KIMI K3 (hostile referee pass)

Date: 2026-08-15. Scope: top ledger items per `plans/wayfinder/rh-goals/MAP.md` +
`tickets/`, execution log `research_notes/rh_goals_2026-08-14/EXECUTION_LOG.md`.
Mandate: FALSIFY. Four independent audit lanes were run (theorem-chain prose,
certification code, Kloosterman+M1, Kaggle+Koyama); raw receipt fields were
recomputed independently and external citations (MMS arXiv:0912.2236) checked
against the primary PDF.

## Verdict summary

| Item | Verdict |
|---|---|
| 1 — Declared G_5 off-line theorem | **STANDS** (no theorem-level defect found; 9 errata, 5 cosmetic) |
| 2 — Kloosterman gate NO-GO | **SOUND** (2 framing overstatements in tickets/outlook) |
| 3 — Mechanism M1b/M1c/M2 | **SOUND** (acceptance claims justified; 2 minor framing defects) |
| 4 — Gonek/Mertens Kaggle lane | **DEFECT** (1 HIGH latent pipeline defect, 1 MEDIUM, 1 LOW; nothing executed yet, so nothing corrupted) |
| 5 — Koyama letter draft | **DEFECT** (3 factual errors vs repo receipts, 2 unverifiable claims; must not be sent as-is) |

---

## ITEM 1 — THE DECLARED THEOREM

Claim: G_5 (lambda = golden ratio) has a Selberg-zeta zero s* within 1e-6 per
coordinate of 0.4538951800749447 + 5.7635372417301305i, hence
Re(s*) <= 1/2 - 0.0461.

### What was independently verified (not taken on the documents' say-so)

- **Margin arithmetic (the suspicious-looking pair margin 3.4379e-8 vs
  F_R = 1.77974e-6): NOT a defect.** The certified comparison is
  `|d_N|_lower - F_R > 0` per subarc, where
  `F_R = T_tail * exp(1 + ||L||_1 + ||LP_N||_1)` already contains the trace
  norms **inside the exponential** (Simon Trace Ideals Thm 3.4 form;
  `TB_R1_HILBERT_RESTATEMENT.md:47-51`, code at
  `.worktrees/aletheia-restore/code/tc_rerun/certify_r3b_flagship.py:390,497-500`).
  No theorem requires margin > F_R*||L|| (≈3.08e-5); that hypothesized
  requirement does not exist in the prose or the cited theorem. Recomputed from
  all 284 raw receipt records: min finite lower bound 1.8141177109e-6,
  F_R = 1.7797390611e-6, difference +3.4378649793e-8 — matches
  `R3B_FLAGSHIP_CERT_RECEIPT.json` exactly. Thin (2% of F_R) but rigorously
  positive; every ingredient bound raises on degradation rather than passing
  silently.
- **Contour closure: verified, not assumed.** Base arcs share exact endpoints
  including last->first (`certify_r3_flagship.py:221-241`); subdivision shares
  computed midpoints; a second independent check requires adjacent determinant
  boxes (including wraparound) to intersect (`certify_r3b_flagship.py:190-196`).
  284 = 4x71 subarcs; argument increments chain with 0 discontinuities and sum
  to 2pi (independent 100-digit recomputation), pinning winding = 1.
- **Interval arithmetic is genuine.** All certified paths use python-flint
  arb/acb ball arithmetic at 384 bits; no float/mpmath point evaluation is
  dressed as a bound. Float uses are labeled diagnostics or candidate selection
  followed by rigorous pins (e.g. `certify_r3b_flagship.py:231-235`).
  The one non-rigorous step (finite-difference derivative check) is explicitly
  labeled "non-proof sanity check" (`certify_r3b_flagship.py:360`).
- **s-uniformity of the tail bound.** R2's receipt and `r3b_endpoint.py:170`
  evaluate at the whole +-1e-6 box ball, so T_tail, ||L|| <= 17.2912, and F_R
  are uniform over the closed box — the exact interface link 3 needs.
- **Operator matches MMS.** The 11-block pattern (5 heads + 6 Hurwitz tails,
  weights ((z +/- n*lambda)^2)^{-s}, squared/principal-branch form per MMS
  p.21, kappa=3, N=160 -> 480x480, sign=+1) is byte-identical across all five
  independent listings (engine, builder, derivative builder, R2's enforced
  EXPECTED_BLOCKS, TB V2/E1 receipts), hash-bound. MMS Thm 6.4 verbatim:
  Z_S(s) = det[(1-L_{s,+})(1-L_{s,-})]/det(1-K_s) — exactly assembly link 6.
  Thm 4.10 verbatim: nuclear order zero for Re s > 1/2, meromorphic, poles only
  at s_k = (1-k)/2 — the box is pole-free. Lemma 6.3 at h_5 = 1 gives
  A_s = L_1 L_2 L_2 as used by the KS gate; kappa_5 = 3, h_5 = 1 match MMS
  eq. (8). KS algebra (trace 4+3*lambda, ell_5, a_5, spacing pi/a_5, lattice
  distance 0.4551002437) recomputed digit-for-digit against
  `KS_GATE_REPORT.md`.
- **R5 v3.1 determinant identification logic:** smoothing via point-eval bound
  + E1's rho_hat <= 0.9483436 < 1 with pole/cut margins 1.0024 >> 0.1
  enlargement; Jordan-chain equality of nonzero spectra; spectral determinants
  (trace-class genus-0 product per Simon Adv. Math. 24 (1977) Thm 4.2;
  2/3-nuclear Grothendieck product per Resume Thm 8); locally-uniform
  trace-class holomorphy on Omega*; identity theorem. No interface mismatch
  found: Clause 2 used only where Sigma n^{-2 sigma} converges, Clause 3 covers
  exactly Omega* containing the box, MMS pole lattice disjoint from Omega*,
  Omega* connected. Enlarged discs need no disjointness. V7's three erratum
  items and V8's defect-A fix are verifiably implemented in the current v3.1
  bytes.
- **Receipts reproduce; hashes verify.** T_tail(128)=5.2715959e-17,
  T_tail(160)=6.2678579e-22, B_total=97.76664753394086, F_R, min margin,
  winding ball, rH <= 0.359, rG <= 2.32e-6, E1 rho_hat and clearance — all
  recomputed from raw serialized fields. All nine sha256 provenance hashes
  verified against disk, including the R3B orchestrator self-hash.
- **Fail-safe design.** Every exception becomes a failed arc -> subdivision ->
  NOT_CERTIFIED; no swallow-to-pass path exists; inequality tests use the
  correct sides (`definitely_positive`, `definitely_less`); the N=128
  comparison arm fails exactly as arithmetic predicts.

### Prior-review follow-through

V4-V8 issues were checked for actual repair: the V7 errata (non-contractive
quarter-clearance contour usage, E1 enlargement separation, stale-tail
disowning) are implemented in current bytes; V8 defect A (stale ledger
citation) repaired. The endpoint contour with rho = 1.0757521 > 1 is used only
through the mean-value bound `A q^k + C k rho^{k-1}` (valid for any rho), with
eta^N decay crushing it — honest, not a gap. Where rho < 1 is genuinely needed
(R5 smoothing), the separate E1 enlargement is used; no conflation in the
current text.

### Defects — ERRATUM (fixable, none requires new mathematics or computation)

- **1-E1. Claimed Lean artifact for Aristotle v18 does not exist sorry-free.**
  `THEOREM_G5_OFFLINE_ASSEMBLY.md:59-61` and `:71-73` claim
  `det_one_sub_proj_mul_proj` and `trace_unitary_le_sum_column_norms` were
  "machine-proved in Lean, Aristotle v18 ... axiom-clean". The only v18 file,
  `projects/aristotle_dispatch_v18/R1Lemmas.lean:27,36`, contains both theorems
  **with `sorry`**; no result tarball exists (unlike v17/v19). The mathematics
  is a three-line paper proof, so the theorem does not logically depend on it,
  but the dependency class "LEAN-PROVED (v17/v18/v19, axiom-clean)" is
  currently false for v18. *Missed by all five prior review rounds.*
- **1-E2. DECLARED assembly retains pre-review directives.**
  `THEOREM_G5_OFFLINE_ASSEMBLY.md:102` still reads "[V4 is asked to re-check
  the pole set claim.]" and lines 136-143 retain the entire "## What V4 must
  clear before declaration" checklist, five rounds after V4 completed. V8's
  defect-B fix was only partially applied.
- **1-E3. Dependency ledger incomplete; execution-log correction claim false
  as committed.** Assembly lines 130-131 omit link 4b's load-bearing citations
  (Simon Adv. Math. 24 (1977) Thm 4.2 + Thm 3.3, Grothendieck Resume Thm 8,
  MMS Thm 4.10). `EXECUTION_LOG.md:377-380` claims this was "corrected ... per
  R5 v3.1" — the current bytes do not contain that correction. The
  MACHINE-CERTIFIED list also omits link 4b's E1 receipt; PAPER-PROOF omits
  R5's Jordan-chain/smoothing/Clause-3 proofs.
- **1-E4. Receipt serialization cannot reconstruct the winding ball.** The 284
  printed increment deltas reconstruct winding = 1 only to ~1e-99, while
  `R3B_FLAGSHIP_CERT_RECEIPT.json` claims midpoint 1 - 2.4e-120 +/- 7.81e-114 —
  ~15 orders of magnitude short. V4's serialization GAP confirmed
  quantitatively; conclusion unaffected, replayability claim overstated.
- **1-E5. `TB_R1_HILBERT_RESTATEMENT.md` partially stale but cited live.** Its
  Step 3 defines F_R with B_tot = 97.77 (F_R ~ 1e64, certifies nothing); the
  proof uses the tighter hybrid endpoint bound (17.2912) defined only in the
  R3b report. Its line-27 geometric-tail claim is false per V7 and explicitly
  disowned by R5 v3.1, yet assembly link 2 cites R1 wholesale. Cite R1 for
  Steps 1-2 only; mark Steps 3-4 superseded.
- **1-E6. Link-5 KS gate is a point margin, not a box margin, for the flagship
  pin.** `KS_GATE_REPORT.md:65` admits box-level distances were computed only
  for q=4/q=6; g5_pin_1's 0.4551002 is center-to-lattice. Harmless (margin >>
  sqrt(2)*1e-6) but the artifact does not literally certify nonvanishing on the
  closed box as link 5 states.
- **1-E7. MMS source-text caveat dropped.** The heading above MMS eq. (34)
  prints q = 2h_q+3 > 5 while MMS Lemma 4.2 states q >= 5; the q=5
  identification rests on the general incidence formula, not the displayed
  equation. V7 resolved in favor of q=5; V8 defect D(iii) noted R5 v3.1 omits
  the caveat. The paper must carry the footnote or a referee will find it
  first.
- **1-E8. Post-final-review edits are inside the declared commit.** R5 v3.1
  (mtime 04:39) and assembly v2 (04:40) were edited *after* V8's ruling
  (04:37) and committed in d3ba0ed. Edits match V8's prescribed must-fix items
  and verify correct, but V8's certification strictly covers pre-edit bytes;
  `EXECUTION_LOG.md:355-356` concedes this ("fixed same turn").
- **1-E9. Uncertified symbol in a displayed bound.** R5 v3.1 line 99 uses
  W_B^{0.1} ("weight sup on the enlarged contour"); E1 certifies margins and
  image ratios, not weight sups. Only existence of a finite bound is needed, so
  presentational, but as written the display contains an unquantified constant.

### Defects — COSMETIC

- 1-C1. Assembly link 1 "adaptive splits to depth 8": achieved max depth is 1
  (receipt census: 100 depth-0, 184 depth-1); 8 is the budget
  (`certify_r3b_flagship.py:61`). Flagged by V4; never fixed. (Also code-audit
  E1.)
- 1-C2. E1 receipt family labels are double-encoded UTF-8 mojibake. Numbers
  unaffected.
- 1-C3. Latent: `r3b_endpoint.py:~249` takes rho = max(head_base_sups,
  deep_rho), omitting center_ratio; valid here only because recorded
  rho >= 0.6958 > 0.5882 in all six tail families. A future parameter change
  could silently invalidate it.
- 1-C4. Latent: `certify_r3b_flagship.py:453-458` selects FTC direction ball by
  endpoint-ball overlap with no assertion; cannot trigger at 384-bit fuzz but
  is an unguarded silent-failure path.
- 1-C5. Hard-coded `True` gate literals (`certify_r3b_flagship.py:516,521`)
  instead of recomputed booleans — safe (failures raise earlier) but not
  independently re-derivable from the receipt.
- 1-C6. Assembly constants table omits rho_hat = 0.948344 alongside
  rho* = 0.697802 (V8 recommended; not done). Two contraction constants
  floating around invites conflation. Stale "CHAIN BROKEN" banner at
  `TB_LEMMA_CHAIN.md:3-5` contradicts the declaration; add a forward pointer.
  Dead code `_hurwitz_u_series_with_s_derivative` (`r3b_engine.py:22-48`);
  stale "L_{s,-} (ODD sector)" docstring (`zeta_cert_rosen_q5.py:322-327`).
- 1-C7. E1 receipt self-labels "FALLS_SHORT" against a reviewer's rounded print
  (1.0023798... < 1.00238) while exceeding the stated 1.0023 — honestly
  disclosed at `E1_ENLARGED_CONTRACTION_CERT.md:27-28`; cosmetic.
- 1-C8. Novelty claim ("first rigorous off-line localization for a
  non-arithmetic finite-area surface") rests on a lane_c prior-art sweep not
  independently redone here; plausible (MMS treat the eigenvalue-1
  correspondence as conjectural for non-arithmetic q) but it is a literature
  claim, not repo-verifiable.

### Issues ALL five prior rounds missed

1. The v18 sorry-only artifact (1-E1).
2. The winding-ball serialization gap made quantitative (1-E4).
3. The R1-Step-3 F_R definition mismatch (1-E5).
4. Point-vs-box KS margin for the flagship pin (1-E6).
5. Post-V8 edit window entering the declared commit (1-E8) — process-level;
   R5's quoted E1/wrapper hashes still verify, so no content slipped.

### Item 1 ruling

The 8-link chain as written (assembly v2 + R5 v3.1 + E1 + R3b/R2/TB_V2
receipts + KS gate) constitutes a complete computer-assisted proof of the
stated theorem. The numerical core survived raw-field recomputation; the code
implements what the lemmas require (correct Simon-bound comparison, verified
closure, genuine ball arithmetic, fail-safe gates); the external theorems say
what the documents claim (MMS verified verbatim against the primary PDF;
Simon/Grothendieck pinpointed consistently by two independent reviewers —
Simon's paywalled text was not opened directly, residual risk low). **No
theorem-level defect found.** Fix 1-E1 through 1-E7 before circulation; all are
one-line to one-paragraph edits. Structural soft spots (common to any
computer-assisted proof): code-implements-math rests on reviewer code-reading
plus hash-binding; four linear-algebra joints are Lean-verified only for the
v17/v19 artifacts present in-repo.

---

## ITEM 2 — KLOOSTERMAN GATE NO-GO: SOUND

All load-bearing arithmetic independently recomputed (exact rationals) and the
verifier re-run to a JSON-identical receipt:
`V_residue(13) = 8077/33264`, per-denominator identity exact for b=2..12,
`S_2(b)` verified b=2..59, `C_raw = 6781/1155`, H_13 = 45, M(13) = -3,
`DeltaW_integral(13) = -95083/180180`, discrete four-term identity error 0,
`N+B+C-A = 663287/249819570 > 0`. Direct brute-force integration of the
protocol observable against its own definition confirms the frozen DeltaW
formula.

Kill soundness: the gate spec (`KLOOSTERMAN_GATE_SPEC.md:7-13`) presupposes an
A,B,C,N decomposition that `RESEARCH_SPEC.md` does not contain; the discrete
(`main.tex:921-954`) and integral
(`INTEGRAL_FAREY_KILL_TEST_PROTOCOL_2026-07-19.md:7-38`) observables diverge at
the same qualifying prime (DeltaW_disc != DeltaW_int). Spec-defect kill ground
airtight; structural ground source-backed (`main.tex:1063-1064,1337-1346`;
`RESEARCH_SPEC.md:156-159`). Downstream: nothing depends on the gate having
been GO; no orphaned claims.

Defects (framing layer, low):
- 2-D1 (low-moderate, ERRATUM-of-record): `tickets/kloosterman-gate.md:16`
  ("NO-GO, recorded per the pre-registered binding condition") and
  `plans/wayfinder/rh-goals/MAP.md:39` ("pre-registered stop condition hit")
  overstate procedural fidelity — the receipt itself says
  `go_no_go: not assessed` (`v_extraction_receipt.json:9`) and gate steps 2-3
  were never run (`V_EXTRACTION.md:5-7`). The closure is substantively right
  but dresses a frontier adjudication as a mechanical trigger.
- 2-D2 (low): `lane_d/D3_OPEN_ITEMS.md:24-26` "Weil/Kloosterman methods cannot
  reach it ... any sufficient bound embeds Mertens cancellation" — impossibility
  phrasing; should read "direct completion invalid (frozen analysis); no
  unconditional route at Weil strength is known".

## ITEM 3 — MECHANISM M1b/M1c/M2: SOUND

M1b algebra spot-verified by hand (conjugation A_n = D2^{-1} C_n D2 = W2 T^n,
even-word matrices, det = 1, Gamma_0(2) membership, cocycle cancellation,
ell = sqrt(2)-1, index 3, singular mod-2 W2). Tag discipline honest: the
intertwiner U4 itself is tagged GAP; only word-length <= 4 falsification is
claimed, and the algebra does kill the ordinary-Gauss route.

M1c: receipt matches prose exactly (pin dets 1.54e-29 / 1.27e-17-class,
controls 21.78 and 3.58 — the test genuinely discriminates, including a control
between pins 1 and 2). Limitations all disclosed at source: M^+ = M^-
identically at level 2 (redundant column), and the Fricke-plus restriction
FAILED (no nontrivial 3x3 permutation action) — what was tested is the
Gamma_0(2) congruence determinant, not the Fricke-plus block (I4) needs
(prose lines 78-85, 113; receipt `claim_boundary`). Verdict wording
"CONTAINMENT SUPPORTED (finite numerical probe; not proved)" is calibrated.

M2: all 9 rows check out (ball-modulus semantics, tails >= 4 orders below lower
bounds); the G4 control at the q=4 pin is consistent-with-zero as required.
Logic correctly conditioned on h analytic near s_n; pointwise scope stated.

Defects (low):
- 3-D1: `tickets/mechanism-m2-nonfactorization.md:19-23` headline "9/9
  witnesses CERTIFIED-NONZERO" and "fully proven" vs every row labeled
  "certified-modulo-tail-heuristic" in `M2_NONFACT_WITNESSES.md:5,35-37`;
  mitigated by MAP.md leaving the ticket at "claimed".
- 3-D2: q=10 evaluations use a builder anchor-validated only at q=8
  (`M2_NONFACT_WITNESSES.md:31`); caveat not propagated to the ticket.

## ITEM 4 — GONEK/MERTENS KAGGLE LANE: DEFECT

Framing correction: there is no scan. The kernels refine seeds line-by-line
from Odlyzko's 100k table (`mertens_zeros_part1.py:1-7,104,117-118`) — the
hypothesized "scan step size" does not exist, but missed-/wrong-zero risk does.

- **4-D1 (HIGH, latent): no dedup / no wrong-zero guard.** `refine()`
  (`mertens_zeros_part1.py:64-70`) seeds secant at gamma_seed +/- 0.03; the
  residual gate (`:76`) passes on ANY zero. Measured on the bundled seed table:
  sorted, min gap 0.0147 at line 95249, and **40 gaps < 0.06** — for those 40
  pairs both secant brackets contain both zeros; either row can silently land
  on the wrong/duplicate ordinate. No deduplication, no output monotonicity
  check, no |gamma_refined - gamma_seed| sanity bound; `index` is written from
  table position (`:117-119`), so a duplicate/misindexed zero directly corrupts
  the n-th-row indexing the J_{-1} sums depend on. Nothing has executed yet, so
  nothing is corrupted — but the harvest must add these guards before any
  J_{-1} sum is consumed.
- **4-D2 (MEDIUM): zero completeness inherited, never verified.** No
  argument-principle count, no Riemann-von Mangoldt N(T) check, no sign-change
  coverage. The in-kernel SHA-256 (`:141`) is compared against nothing.
  Mitigated by borrowing Odlyzko's table quality (first/last entries match
  known values; five copies byte-identical) — but the repo contains no
  independent verification and the markdown never discloses this.
- 4-D3 (LOW): `KAGGLE_OFFLOAD.md:3,67` "No kernel is claimed as pushed or
  running" vs `EXECUTION_LOG.md:166-181` recording v4 of all five kernels
  "CONFIRMED RUNNING"; time-stamped staleness, not dishonesty — but no harvest
  artifact (no CSV anywhere) corroborates completion.

Checked and CLEAN: dps=25 vs residual 1e-15 is coherent (10 decades above the
precision floor; `findroot(tol=1e-20)`); off-line drift guard
(|Im gamma| > 1e-12 rejected) present; the J_{-1} sum formula in
`lane_a/zero_sum_pari_driver.py:198-209` matches the checkpoint declaration and
Gonek's J_{-1}; Hecke scan script matches its markdown exactly (9,588 cells,
manifest inflations).

## ITEM 5 — KOYAMA LETTER DRAFT: DEFECT (must not be sent as-is)

The G_5 theorem statement is transcribed faithfully
(`KOYAMA_UPDATE_DRAFT.md:30-31` vs `THEOREM_G5_OFFLINE_ASSEMBLY.md:26-32`,
including delta >= 0.0461038). But:

- **5-D1 (HIGH): "for G_5 we hold nine certified nonvanishing witnesses"
  (`:45-46`).** The receipt contains **three** G_5 witnesses; nine is the total
  across G_5+G_8+G_10 (`m2_nonfact_receipt.json`; `M2_NONFACT_WITNESSES.md:9-17`).
  Compounded by dropping the "certified-modulo-tail-heuristic" qualifier that
  labels every row; same dropped qualifier at `:23-24`.
- **5-D2 (HIGH): "G_5, G_7, G_8 the zeros scatter with Re-dispersion
  ~10^{-1}-10^{-2}" (`:21-22`).** G_8 has n=0, verdict INSUFFICIENT-DATA
  (`lane_b/FAMILY_SWEEP_G7G8.md:28-30,39-42`) — contradicted by the repo's own
  sweep.
- **5-D3 (MEDIUM): "three differently built operators agreeing to ~10^{-15}"
  (`:20-21`).** Law table gives q=3: 6.5e-14, q=4: 9.8e-12, q=6: 1.03e-11 with
  q=4/q=6 INSUFFICIENT-DATA (`FAMILY_SWEEP_G7G8.md:25-27`), and the V1 review
  (`EXECUTION_LOG.md:82-95`) rules these values not family-comparable.
  Overstates agreement by 3-4 orders of magnitude for two of three members.
- **5-D4 (unverifiable):** `:84` "part 5 harvested and verified" — no artifact
  anywhere in the repo (see 4-D3). `:26` "first computed/certified resonance
  data for non-arithmetic Hecke groups" — no scout receipt covers resonance
  novelty.
- **5-D5 (internally contradicted):** `:64` "Gonek's 1989 conjecture" — the
  repo's own scout dates the prediction to 1999
  (`lane_c/S1_ZERO_SUM_LIT.md:38,59`).

Verified-accurate (for balance): item 3(a) 0.02903 +/- 0.00016 / 2/pi^2
refuted / 3/pi^4 excluded at ~11 sigma (matches receipts; the draft actually
understates — v2 has N=10,000, 98 sigma); item 3(b) J_{-1}(T)/T ratio 0.9489
with honest "TOO EARLY" framing; "two independent reproductions" (V7 + E1);
"five rounds of internal adversarial review" (V4-V8); 384-bit Arb and
essential-gap language; K_s lattice machine-verified claim.

---

## FINAL RULING

**The declared theorem STANDS.** No theorem-level defect was found in the
8-link chain, the certification code, or the cited external results. The
central numerical suspicion (min margin 3.4379e-8 << F_R = 1.77974e-6) is a
misreading: the certificate compares |d_N|_lower - F_R with the trace norms
inside the exponential, which is exactly the Simon bound the prose invokes —
verified in code and by hand. The theorem's real exposure is (a) the standard
structural one of any computer-assisted proof (code-reading + hash-binding as
the code-implements-math link; Arb matrix-enclosure semantics should be named
as a dependency in the paper preamble), and (b) a pile of errata — chiefly the
phantom "axiom-clean v18" Lean claim (1-E1), the stale pre-review directives
inside the DECLARED assembly (1-E2), and the incomplete citation ledger (1-E3)
— all repairable in an afternoon, none requiring new mathematics.

Separately: the Kaggle zero-refinement pipeline has a real latent defect
(4-D1) that must be guarded before its harvest feeds any J_{-1} sum, and the
Koyama draft contains three factual errors against the repo's own receipts
(5-D1..5-D3), all in the direction of overstating the evidence — fix before
sending.

*Audit performed read-only; this report is the only file written.*
