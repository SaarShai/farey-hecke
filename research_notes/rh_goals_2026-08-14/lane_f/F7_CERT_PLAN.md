# F7 CERT PLAN — q=7 off-line resonance certificate (run plan)

Lane F, P1, 2026-08-15. Companion to `F7_CONSTANTS_MANIFEST.md` (all exact
constants live there). Template: the DECLARED G_5 chain
(`lane_g/THEOREM_G5_OFFLINE_ASSEMBLY.md` v2) — same seven links, same
script family, q=7 parameters. Target: winding-1 certificate for a 1e−6 box
around s₀ = 0.4751647621098225 + 4.668743786424289 i (mms+, sign = +1),
hence Re(s*) ≤ 0.4751648 < 1/2, δ ≥ 0.0248342.

Nothing in this plan has been executed; execution starts on owner word.

## 1. Pipeline (mirrors the G_5 chain stage-for-stage)

| Stage | q=5 artifact | q=7 action | Cost class |
|---|---|---|---|
| 0. Disc optimization | `tb_disc_opt.py` → factors (3.14,2.27,1.70), ρ*=0.6978 | DONE at float level (FAMILY_PREP: factors (2.79,2.39,1.90,1.56,1.35), ρ*=0.7823). Optional: deeper grid to push ρ* down (lever on N, see §3) | minutes–hours (float) |
| 1. TB block certificates (Arb) | `certify_tb_blocks_v2.py` → TB V2 receipt | Re-run at κ=5, 19 blocks, 5 factors; gates updated per §2 | minutes |
| 2. R2 envelope (T_tail, B) | `certify_r2_flagship.py` → R2 receipt | Re-run at q=7 pin box, N grid {128,160,192,224,256}; freeze N* per §3 | minutes–1 h |
| 2b. Boundary float pre-scan | (implicit in q=5 receipts) | Float |det(I−L P_N)| on ∂Box at N=32 → margin target for F_R | minutes |
| 3. R3b closed-contour winding | `certify_r3b_flagship.py` → R3B receipt | THE heavy cert; Kaggle, §5 | ~10–40 CPU-h |
| 4. K_s gate | `ks_gate/ks_gate.py` (q-generic `group_data(q)`) + KS_GATE_REPORT | Re-run with q=7; lattice already exact (manifest §4); box margin ≈ 0.5895480 | seconds |
| 4b. E1 enlarged-disc contraction (link 4b) | `certify_e1_enlarged.py` → E1 receipt | Re-certify at κ=5 geometry; need ρ̂ < 1 analog of 0.9484 | minutes–hours |
| 5. R5 determinant identification | `TB_R5_DETERMINANT_IDENTIFICATION.md` v3.1 | Paper-proof is q-independent; re-point its machine constants at the q=7 E1 receipt | drafting |
| 6. Lean joints | Aristotle v17/v18/v19 | All abstract joints (restriction identity, trace-norm lemmas, geom tail) are q-independent — REUSE. New dispatch needed ONLY for the q=7 K_s lattice statement (v17 `KsZeroLattice` analog with ell_7, a_7) | one Aristotle dispatch |
| 7. Assembly | THEOREM_G5_OFFLINE_ASSEMBLY.md | Write THEOREM_G7_OFFLINE_ASSEMBLY.md after 3,4,4b land; MMS eq-(34) heading footnote NOT needed at q=7 (heading says q > 5) | drafting |

## 2. Every G_5-specific constant that must change (file:line → q=7 value)

Engine / builders:
- `.worktrees/aletheia-restore/code/zeta_cert_rosen_q5.py` (the certified
  engine; effectively a q=5 fork): `Q = 5` (:106) → 7; `lam_ball` golden
  ratio (:114) → 2·cos(π/7) ball; `kappa = 3` (:130,:332) → 5; disc radii
  (:152) → 5-disc q=7 geometry; `twoh = 2` (:365) → 4; the 11-call eq-(34)
  block assembly (:367–380) → the 19-block assembly (manifest §3);
  `n_head = 4` (:328,:831) — keep 4 unless R2 says otherwise; receipt string
  "q=5 (h=1,kappa=3)" (:802). Cleanest route: port `zeta_mayer_rosen.py`'s
  q-generic `build_reduced_matrix` (:293–367, already handles odd q≥5) into
  a new `zeta_cert_rosen_q7.py` with Arb balls, and cross-validate against
  the float engine's 19 captured calls.
- `tc_rerun/tc_rerun.py` (imported as `source_builder`): `kappa = 3`,
  `twoh = 2`, `k_idx = 3` (:96–98) → 5, 4, 5; 11-call block assembly
  (:130–145) → 19-block; `DISC_FACTORS` 3-factor hard check (:51–59) →
  5 factors ("2.79","2.39","1.90","1.56","1.35"); `geometry_for_factors`
  `range(1,4)` (:76–78) → range(1,6).
- `tc_rerun/r3b_engine.py`: default factors (:173) → 5-tuple; `kappa = 3`
  (:178) → 5; literal 11 `add_columns` calls (:229–239) → 19 calls.
- `tb_certify/certify_tb_blocks.py` (v1, imported by v2 and R2): `Q = 5`
  (:30) → 7; `RADIUS_MULTIPLIERS` (:31) → 5-tuple; `lam_ball` (:95–98) →
  λ_7 ball; hardcoded 4-point q=5 CF partition list (:108–119) → q=7
  partition from the generic CF construction (`zeta_mayer_rosen.py:177–185`
  odd-q branch, ported to balls); `disc_geometry` `range(1,4)` (:122–130)
  → range(1,6).
- `tb_certify/certify_tb_blocks_v2.py`: `THRESHOLD_TEXT = "0.70"` (:29–30)
  → "0.80" (re-targeted gate, justification in §3); `"expected_count": 11`
  (:324–326,:522) → 19; sweep source `tb_disc_sweep.py` (`q = 5` :8,
  `BLOCKS` :19–21) → q=7 19-block sweep.

R2 envelope:
- `tb_certify/certify_r2_flagship.py`: `PIN_NAME/RE/IM/HALF_WIDTH` (:56–59)
  → "g7_pin_1", "0.4751647621098225", "4.668743786424289", "1e-6";
  `SIGN = 1` (:60) unchanged; `N_TARGETS = (128,160)` (:62) → (192, 224)
  provisional (§3); `EXPECTED_BLOCKS` 11 tuples (:67–79) → the 19 tuples;
  `q != 5` gate (:296) → q == 7; ρ* gate 0.70 (:306) → 0.80; block-count
  check (:330–332) → 19; κ=3 loops (:578 `range(3)`, :739 `(1,2,3)`) →
  κ=5; receipt `"q": 5` (:820) → 7; `ENGINE_PATH` (:42) → the q=7 engine.

R3b winding cert:
- `tc_rerun/certify_r3_flagship.py` (attempt-1 module, imported):
  `PIN_RE/PIN_IM/HALF_WIDTH` (:51–53) → g7 pin; `K_PER_EDGE = 48` (:49) —
  keep 48 initially (192 base arcs), raise only if subdivision budget blows.
- `tc_rerun/certify_r3b_flagship.py`: immutable-input hashes
  `R2_EXPECTED_SHA256`/`TB_V2_EXPECTED_SHA256` (:50–51) → regenerate after
  the q=7 receipts land; `N_PRIMARY/N_COMPARISON` (:55–56) → 224/192
  provisional; `EXACT_FACTORS` (:60) → 5-tuple; `ENGINE_PATH` (:41) → q=7
  engine; report text literals (:1063–1065) → q=7 narrative; precision
  floor 384 (:1403) unchanged; adaptive budget (depth 8, 1536 evals,
  :61–62) unchanged initially.
- `tb_certify/r3b_endpoint.py`: `EXACT_FACTORS` (:28) → 5-tuple;
  `flagship_s_box` literals (:53–57) → g7 pin; κ=3 loops (:165,:338,:353)
  → κ=5; `ENLARGEMENT_MARGIN_DIVISOR = 4` (:29) unchanged.

K_s gate:
- `ks_gate/ks_gate.py`: machinery already q-generic (`operator_word`,
  `scalar_composition_matrix`, `group_data`, :82–128) — run with q=7;
  replace `RECTANGLE_Q5` (:35–40) with a q=7 rectangle covering the box,
  e.g. Re ∈ [0.42, 0.53], Im ∈ [4.1, 5.3] (exact lattice answer: EMPTY —
  all zeros have Re ≤ 0); human-written derivation text (:361–386) → the
  manifest §4 algebra (m(x) cubic, not λ²=λ+1). Tolerances (1e−10 / 1e−32,
  ≤10000 product terms, :137) unchanged; ell_7 < ell_5 so ~18 terms suffice
  as at q=5.

## 3. Expected N — from scan convergence + the F_R trade-off

Scan evidence (`q7_mms_plus`, pin 1): |det| at N=22 vs N=28 agrees to
1.4e−16 absolute and the pin drifts only 1.1e−14 / 1.9e−14 (Re/Im) — the
zero LOCATION is N-stable at float level by N ≈ 28. The certified N is
therefore driven entirely by the tail bound, not by location stability.

The binding inequality is the link-3/link-4 requirement

  F_R(N) = T_tail(N)·exp(1 + 2·B(N))  <  min_{∂Box} |det(I−L P_N)|_lower,

with B(N) the computed-row column-2-norm bound (q=5: B = 17.2912,
T_tail(160) = 6.27e−22, F_R = 1.78e−6, margin 3.44e−8 — thin: 2% of F_R).
Two q=7 changes push N UP relative to 160:

- ρ* = 0.7823 vs 0.6978: ρ*^N decays ~1.46× slower per unit N
  (|ln ρ*| = 0.2456 vs 0.3598). Matching q=5's ρ*^160 ≈ 1e−25 needs
  N ≈ 235 at q=7.
- B grows with κ (5 component columns of blocks vs 3) and is only known
  after the q=7 endpoint computation. exp(1+2B) is the sensitive factor:
  every +5 in B costs ~e^10 ≈ 2.2e4 in F_R, i.e. ~+19 in N.

Decision rule (freeze AFTER the R2 + endpoint measurements, before any
contour work): N* = smallest N with F_R(N) ≤ 0.1 × m₀, where m₀ is the
float pre-scan estimate of min_{∂Box}|det| at N=32 (stage 2b). Provisional
values for planning: **N_PRIMARY = 224, N_COMPARISON = 192** (matrix
1120×1120 vs q=5's 480×480), ceiling 256, fallback 192/160 if the measured
T_tail beats the ρ*^N projection. Keep the N_COMPARISON arm as the designed
NOT_CERTIFIED control (the audit explicitly validated this fail-safe).

Risk flag: if the endpoint phase returns B ≳ 30, N* lands ≳ 350 and the
contour cost exceeds even the chunked Kaggle budget (§5) — the mitigation
lever is stage-0 re-optimization of the 5 disc inflations (deeper grid or
per-block radii) to buy ρ* down; do NOT start R3b before this closes.

## 4. R2 envelope families for the q=7 block structure

q=5's R2 receipt carried 11 per-block families (Hurwitz-closed at m=0,
center offsets kept). The q=7 envelope has **19 families**: the 9 head
blocks (finite columns, exact Hurwitz heads) and the 10 tail blocks, which
fall into 3 Hurwitz classes sharing target disc D_5: L_{3,s}^∞ (start n=3,
block 1→5), L_{2,s}^∞ (start n=2, blocks 2→5,3→5,4→5,5→5), L_{−2,s}^∞
(start n=−2, blocks 1→5,2→5,3→5,4→5,5→5). Tail-split search parameters
(K_START 12, MAX_K 64; q=5 used K = 14–15, deep tail from first_n = 18)
carry over as starting values; the worst block at the float level is
(2→5, n=2 tail) — expect it to set T_tail. All other R2 mechanics (M = 512
source arcs, K_HEAD = 16 exact columns, monotonicity gate
T_tail(N₂) < T_tail(N₁), box-ball s-uniformity per Kimi-audit item
"s-uniformity of the tail bound") are q-independent.

## 5. Contour box and Kaggle offload plan

Box: center s₀ = 0.4751647621098225 + 4.668743786424289 i, half-width 1e−6
each coordinate (template default; scan drift 1e−14 makes this conservative;
K_s box margin ≈ 0.5895480, MMS real pole lattice s_k = (1−k)/2 is 4.67 in
Im away, nearest sibling zero 1.70 away — isolation is not in doubt; the
winding count itself is what the cert establishes).

Cost model (from the q=5 receipt: 376 arc evaluations, 10 075 s wall at
8 workers, N=160, 480×480):

- Per-evaluation CPU cost: q=5 saturated at ~27 wall-s/eval at 8 workers,
  i.e. ~214 CPU-s/eval (8 × 10 075 / 376). Ball-matrix build + determinant
  scales ~ (κN)³, so q=7 at N=224 (1120×1120) is (1120/480)³ ≈ 12.7× ⇒
  ~2 700 CPU-s ≈ 45 CPU-min per evaluation; 376 evals ≈ **~280 CPU-h**
  total. At N=192 (8.0×): ~175 CPU-h. At N=160 (4.63×): ~100 CPU-h.
  (Column-construction terms scale weaker than cubic, so these are upper
  estimates; the pilot chunk in the sequence below replaces them with a
  measurement.)

  This EXCEEDS a single Kaggle session (12 h cap, 4 vCPU ⇒ ≤ 48 CPU-h) at
  any certifiable N. Chunking is therefore MANDATORY, not optional:

- **Chunk by contour edge, then by arc range.** The boundary is 4 edges ×
  48 base arcs; each arc's subarc tree is independent and the script already
  checkpoints (`--checkpoint-batch 8`). At ~2 evaluations per base arc
  (376/192), half-edge chunks (24 arcs ≈ 47 evals ≈ 35 CPU-h at N=224) are
  too tight against the 48 CPU-h session budget. Plan: **16 chunks of 12
  base arcs** ≈ 24 evals ≈ 18 CPU-h each at N = 224 (≈ 11 CPU-h at N=192) —
  each chunk fits a 12 h Kaggle session at 4 vCPU (≤ 48 CPU-h) with 2–3×
  headroom, checkpoint handoff between sessions via the receipt/checkpoint
  JSONs (Kaggle dataset in/out).
- Required code change (flagged, small): an `--arcs i:j` CLI filter on
  `certify_r3b_flagship.py` so a chunk certifies a contiguous base-arc
  range and the orchestrator merges subarc receipts; the merge must
  re-verify adjacent-box intersection across chunk seams (the audit's
  contour-closure check, `certify_r3b_flagship.py:190–196`, currently
  in-process). Winding is summed over the merged, closure-verified arc set.
- Kaggle environment: pure CPU, python-flint only (no GPU, no network
  dependency); pin the python-flint version in the notebook and record it
  in the receipt; `--workers 4` (Kaggle CPU sessions have 4 vCPUs; the q=5
  run's 8 was a local machine).
- Sequence: (1) stages 0–2b + 4 locally (cheap, hours); (2) freeze N*;
  (3) one Kaggle pilot chunk (12 arcs) to measure true per-eval cost at
  N*, THEN set the chunk count from measurement, not from this estimate;
  (4) remaining chunks; (5) local merge + closure verification + winding
  sum; (6) E1 (stage 4b) locally; (7) assembly.

Contingency order if cost overruns: (a) more, smaller chunks (arc-level
parallelism is effectively unlimited); (b) N* re-trade per §3; (c) stage-0
disc re-optimization; (d) backup pin 3 only if pin 1's boundary margin —
not cost — fails.

## 6. Gate discipline (per the hostile-referee checklist)

- Every receipt carries sha256 of inputs; `certify_r3b_flagship.py:50–51`
  hash pins regenerated for q=7 receipts; no self-approved constant changes
  (the 0.70 → 0.80 ρ* gate re-target must be recorded in the R2 report with
  the N derivation).
- Box-level (not center-level) K_s margin, per Kimi erratum 1-E6.
- The finite-difference derivative check stays labeled non-proof
  (`certify_r3b_flagship.py:360`).
- N_COMPARISON arm must FAIL (designed control); if it passes, stop and
  investigate — that would signal a tail-bound bug, not a stronger cert.
- Sector honesty: sign = +1 mms+, no geometric parity claim.
- MMS citation: Theorem 6.4 factorization + eq. (34) heading covers q=7
  verbatim ("q = 2h_q + 3 > 5"); still cite Lemma 4.2 (q ≥ 5) for the
  reduced-sector validity.
