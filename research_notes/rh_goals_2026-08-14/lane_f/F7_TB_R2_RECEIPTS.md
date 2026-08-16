# F7 TB + R2 RECEIPTS — q=7 certification stages 1 and 2

Lane F, 2026-08-15. Executes `F7_CERT_PLAN.md` stages 1, 2 and 2b at the
ADOPTED disc radii of `F7_MITIGATION_REPORT.md` §7. Constants from
`F7_CONSTANTS_MANIFEST.md`. Nothing outside stages 1–2b was run: no R3b
contour work, no Kaggle, no other lanes' files, no commits.

**Verdict: GO for stage 3 (R3b winding), with N\* re-frozen from the planned
224 to 256.** Every stage-1 and stage-2 gate passes. The plan's provisional
`N_PRIMARY = 224` does **not** satisfy the plan's own stage-2 decision rule
`F_R(N) ≤ 0.1·m₀` and must not be used; the rule is first met at N = 238, and
N = 256 is recommended for headroom (see §5).

## 1. Headline numbers

| quantity | certified value (Arb upper bound, rounded UP) | gate | verdict |
|---|---|---|---|
| ρ\* (stage 1) | **0.763212029206899202166157** (± 1.40e−25) | < 0.80 | **PASS** |
| worst block | (5→3, +1, head) | — | matches float |
| T_tail(224) | 1.4792058281325539748603802619554e−23 | finite, monotone | PASS |
| T_tail(238) | 3.2635967886461274925009552968050e−25 | — | — |
| T_tail(256) | 2.4114870765008821786740995136173e−27 | — | — |
| B (= B_finite(256), endpoint column-2-norm) | 20.1696369233843988041045344390 | < 30 | **PASS** |
| B_total (R2 column sum, *not* the F_R B) | 119.06285559909506923733105505540 | — | reported |
| F_R(224) = T_tail·exp(1+2B) | 1.3288e−05 | ≤ 0.1·m₀ = 3.3132e−07 | **fail** |
| F_R(238) | 2.9317e−07 | ≤ 3.3132e−07 | **PASS** (×1.13) |
| F_R(256) | 2.1662e−09 | ≤ 3.3132e−07 | **PASS** (×153) |
| m₀ (N=32 boundary pre-scan) | 3.313176035446919e−06 | — | **NON-RIGOROUS** |

Float cross-check (NON-RIGOROUS PREPARATION, not used in any certified value):
`f7_tb_disc_sweep.py` reproduces the mitigation report's float ρ\* =
0.762251293807 exactly, with the same worst block (5→3, n=1 head). The
certified Arb ρ\* = 0.7632120 sits 0.00096 above it, which is the expected
outward width of the M=512 rectangular arc cover — the certified value is the
one that propagates.

## 2. Stage 1 — q=7 TB block certificates (Arb, all 19 blocks)

Backend python-flint Arb/Acb, precision 384 bits, arc cover M = 512, closed
1e−6 geometry; λ₇ = 2cos(π/7) as an Arb ball (min poly x³−x²−2x+1); κ₇ = 5
discs; disc inflation factors (3.522, 2.622, 2.372, 1.79, 1.6).

Block source `f7_tb_disc_sweep.py`, 19 blocks (9 heads + 10 Hurwitz tails),
captured from the authoritative builder `zeta_mayer_rosen.build_reduced_matrix`
(q=7, sign=+1, n_head=4) and identical to `F7_CONSTANTS_MANIFEST.md` §3.

| block | n₀ | K used | certified ratio upper bound |
|---|---:|---:|---:|
| 1→4, +2, head | 2 | — | 0.644564754555624317315529 |
| 1→5, +3, tail | 3 | 12 | 0.750963043983913640547266 |
| 1→4, −1, head | 1 | — | 0.577065169573208863290961 |
| 1→5, −2, tail | 2 | 12 | 0.759691869559052222618976 |
| 2→5, +2, tail | 2 | 12 | 0.758997399091102354126047 |
| 2→4, −1, head | 1 | — | 0.477232046840121915517053 |
| 2→5, −2, tail | 2 | 12 | 0.758997399091102354126047 |
| 3→1, +1, head | 1 | — | 0.762873680384498307517353 |
| 3→5, +2, tail | 2 | 12 | 0.758461098910631969823321 |
| 3→4, −1, head | 1 | — | 0.392222397323917065560313 |
| 3→5, −2, tail | 2 | 12 | 0.758461098910631969823321 |
| 4→2, +1, head | 1 | — | 0.754860262401469159012503 |
| 4→5, +2, tail | 2 | 12 | 0.757688247459720229609519 |
| 4→4, −1, head | 1 | — | 0.255439665636527629203731 |
| 4→5, −2, tail | 2 | 12 | 0.757688247459720229609519 |
| 5→3, +1, head | 1 | — | **0.763212029206899202166157** |
| 5→5, +2, tail | 2 | 12 | 0.756842981355763052901832 |
| 5→4, −1, head | 1 | — | 0.756505798585446464941458 |
| 5→5, −2, tail | 2 | 12 | 0.756842981355763052901832 |

Gates: `all_head_and_deep_tail_terms_pass` = true,
`all_pole_clearances_pass` = true (smallest pole margin 1.01589081324843),
`all_branch_cut_clearances_pass` = true. Every tail family closed at the
starting K = 12 (no K escalation was needed anywhere), deep tail from n₀+13.
Verdict `PASS_RHO_LT_0.80`.

**Threshold re-target, recorded explicitly.** The q=5 chain gates ρ\* < 0.70.
That 0.70 is a chosen target, not a theorem constant (`F7_CERT_PLAN.md` §2,
`F7_CONSTANTS_MANIFEST.md` item 5); the q=7 stage-0 optimum sits at 0.7623, so
the q=7 gate is 0.80. The re-target is recorded in the receipt field
`threshold_rationale`, and what propagates downstream is the certified ρ\*
value, never the gate. Note also that the shared V2 serializer keys are still
named `ratio_less_than_0_70`; at q=7 those booleans carry the 0.80 comparison
(the threshold itself is stored in `threshold_text`/`threshold`).

## 3. W-envelope port (prerequisite of R2)

Schema `tb-weight-envelope-cert/v2`, q=7, κ=5, one box `g7_pin_1`, 384 bits,
M=512, ρ\* read from the stage-1 receipt (not a supplied literal).

- W^(≥1) = 7.08501261150862810346347
- W^(0) (conditioning sanity only, does not enter F) = 6.54960613713658448989529
- F at N=224 with the q=5 L3′ formula = 1.973e+41 — reported for schema
  parity only; it is **not** the F_R of the plan's decision rule.

Scope difference from q=5, stated rather than papered over: the q=5 receipt
closed with PASS/NOT against per-pin T-c contour lower bounds. q=7 has no T-c
stage in stages 1–2, so the contour comparison fields carry
`NOT_APPLICABLE_NO_Q7_TC_STAGE` and no verdict is manufactured. R2 reads only
`plain_weight_sup_upper_bound` (per single block) and
`v2_image_ratio_upper_bound` (per head term), both present and cross-checked
against the TB receipt inside R2.

## 4. Stage 2 — R2 column envelope

Schema `r2-flagship-column-envelope/v1`, status CERTIFIED (mode PRODUCTION),
384 bits, M = 512, K_head = 16, engine = the q-GENERIC
`zeta_cert_rosen.py` at q=7 (not the q=5 fork). All 19 families certified;
input validation binds the run to the exact TB and W receipt hashes, the
19-block source, the ρ\* < 0.80 gate, the q=7/κ=5 fields, and the
`g7_pin_1` box; the negative control 2·Re(s) < 1 holds.

| N | T_tail(N) upper bound |
|---:|---|
| 192 | 8.9157654346977777415591223171e−20 |
| 224 | 1.4792058281325539748603802620e−23 |
| 232 | 1.6738553737157652110170447136e−24 |
| 234 | 9.7066807500808655697319584968e−25 |
| 236 | 5.6285531659092600671426151523e−25 |
| 238 | 3.2635967886461274925009552968e−25 |
| 240 | 1.8922146190273206484482479837e−25 |
| 256 | 2.4114870765008821786740995136e−27 |

B_total (R2 full-operator column-sum bound) = 119.062855599095069237331055055.
**Nomenclature guard:** B_total is *not* the B of `F_R = T_tail·exp(1+2B)`.
The plan's B is the endpoint column-2-norm bound B_finite (q=5: 17.2912;
q=5's B_total was 97.77). Both are carried, and `f7_stage2_FR.py` reads
B_finite, never B_total.

Endpoint B_finite at the adopted radii (384-bit Arb/Acb over the closed 1e−6
box), re-run and banked this session:

| N | B_finite upper bound | build + norms wall |
|---:|---|---:|
| 224 | 20.1696367902021933887065412675 | 50.3 s |
| 240 | 20.1696368693982737399997723391 | 57.8 s |
| 256 | 20.1696369233843988041045344390 | 65.8 s |

This reproduces `F7_MITIGATION_REPORT.md` §3's 20.1696367902 at N=224 to every
printed digit and confirms B is flat in N (Δ < 1.4e−7 over 32 added columns).

## 5. Stage 2b — m₀ pre-scan and the F_R decision rule

**m₀ is NON-RIGOROUS.** `f7_m0_prescan.py` evaluates |det(I − L P_N)| at N = 32
on 96 sampled boundary points (24 per edge) of the closed 1e−6 box. Each
individual value is a 384-bit Arb/Acb enclosure, but 96 points are a *sample*,
not a cover, and a sampled minimum over-estimates the true boundary minimum.
It is prep for freezing N\*, and can never enter a certificate.

  m₀ = 3.313176035446919e−06 (argmin on the `right` edge), so 0.1·m₀ = 3.3132e−07.

For scale: the determinant never came within four orders of zero anywhere on
the sampled boundary, consistent with the pin being isolated as the manifest
predicts.

Rule `N* = smallest N with F_R(N) ≤ 0.1·m₀`, with F_R certified (Arb, rounded
UP) and B taken at the same N where measured, else the largest measured B
(conservative, B is increasing):

| N | F_R(N) | ≤ 0.1·m₀ ? | margin factor |
|---:|---:|---|---:|
| 192 | 8.0090e−02 | no | — |
| 224 | 1.3288e−05 | **no** | — |
| 232 | 1.5036e−06 | no | — |
| 234 | 8.7195e−07 | no | — |
| 236 | 5.0561e−07 | no | — |
| 238 | 2.9317e−07 | yes | ×1.13 |
| 240 | 1.6998e−07 | yes | ×1.95 |
| 256 | 2.1662e−09 | yes | ×153 |

**N\* freeze recommendation: N_PRIMARY = 256, N_COMPARISON = 224.**
The literal rule gives N\* = 238, but its margin is 13 % — and the threshold
side of that comparison is the non-rigorous m₀, so a 13 % margin is not real
headroom. N = 256 clears by ×153 and is the plan's stated ceiling; its cost
penalty over the planned 224 is (256/224)³ ≈ 1.49× on the contour stage.
N = 224 is now a *justified* NOT_CERTIFIED control arm (it fails the rule by
×40), which is exactly the fail-safe the audit asked the comparison arm to be.

Deviation from the plan, disclosed: `F7_CERT_PLAN.md` §3 set provisional
N_PRIMARY = 224 / N_COMPARISON = 192 "pending the R2 + endpoint measurements".
Those measurements are now in and they move both arms up. Nothing was
re-targeted to make a gate pass; the R2 receipt carries T_tail at all eight N
values so the freeze is auditable.

## 6. Scripts, parameters, wall times

All scripts live in `research_notes/rh_goals_2026-08-14/lane_f/`; all receipts
in `lane_f/f7_receipts/`. Python: `/Users/za/.venvs/farey-rh/bin/python`.

| script | what | wall |
|---|---|---:|
| `f7_tb_disc_sweep.py` | 19-block source + float ρ\* check (NON-RIGOROUS) | < 1 s |
| `f7_certify_tb_blocks.py` | stage 1, Arb, `--M 512 --precision-bits 384 --K-start 12 --max-K 64` | 0.6 s |
| `f7_certify_tb_weights.py` | W envelope, `--M 512 --precision-bits 384 --N 224` | 0.8 s |
| `f7_certify_r2_flagship.py` | stage 2, `--M 512 --K-head 16 --precision 384 --N-targets 192 224 232 234 236 238 240 256` | 8.5 s |
| `f7_stage2_endpoint_B.py` | B_finite at N=224 (+240, 256 appended) | 50 s (+58 s, 66 s) |
| `f7_m0_prescan.py` | stage 2b m₀, N=32, 96 boundary samples (NON-RIGOROUS) | ~250 s |
| `f7_stage2_FR.py` | F_R table + N\* decision | < 1 s |

Receipts: `F7_TB_BLOCK_CERTIFICATES_RECEIPT.json` (+ `.md`),
`F7_W_ENVELOPE_CERT_RECEIPT.json` (+ `.md`),
`F7_R2_FLAGSHIP_ENVELOPE_RECEIPT.json` / `_CHECKPOINT.json` /
`F7_R2_FLAGSHIP_CERT.md`, `F7_ENDPOINT_B_RECEIPT.json`,
`F7_M0_PRESCAN_RECEIPT.json`, `F7_STAGE2_FR_RECEIPT.json`.

**Port discipline.** No q=5 file was modified. Every port imports the q=5
modules and reuses their proof functions verbatim (`arc_ball`, `contour_sup`,
`tail_dominating_bound`, `deep_tail_term`, `certify_block`, `clearance_rows`,
`exact_tail_columns_on_arc`, `direct_head_first_moment_sup`,
`deep_first_moment_bound`, `tail_block_envelope`, `tail_block_tail`,
`single_block_tail`) — those take (centers, radii, lam, s) as arguments and
carry no q. Only geometry, block list, κ-indexed aggregation, the pin box and
the gate constants are new. No structural blocker was found: the q=5
certification design generalizes to κ=5 / 19 blocks unchanged.

## 7. GO / NO-GO for stage 3

**GO**, conditional on three carry-forwards:

1. Freeze **N_PRIMARY = 256, N_COMPARISON = 224** (§5), not the plan's 224/192.
2. `tc_rerun/certify_r3b_flagship.py` reads exactly four fields from the R2
   receipt — `tail_bounds[str(N)]["T_tail_upper_bound"]`,
   `B_total_full_operator_column_sum_upper_bound`, `M_source_contour_arcs`,
   `K_head` — all present in the q=7 receipt, and `tail_bounds` carries both
   256 and 224 keys. Its `TB_V2_EXPECTED_SHA256` / `R2_EXPECTED_SHA256` pins,
   `ENGINE_PATH`, `EXACT_FACTORS` (now a 5-tuple), pin box and the 19-call
   `add_columns` block assembly still need the q=7 re-point flagged in
   `F7_PILOT2_REPORT.md`; that work is stage 3 and was not started here.
3. Cost re-estimate at N = 256: the plan's unmeasured ~280 CPU-h at N=224
   becomes ~420 CPU-h; the 16-chunk table needs re-deriving from a measured
   pilot chunk, not from this extrapolation.
