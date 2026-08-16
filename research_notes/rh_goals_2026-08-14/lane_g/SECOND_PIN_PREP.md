# SECOND_PIN_PREP — preparation package for a second certified G_5 pin (Re ≈ 0.24303)

- Date: 2026-08-16. Ticket: `plans/wayfinder/rh-goals/tickets/second-g5-pin.md`.
- Status: **PREP ONLY — nothing in this note has been executed.** No heavy compute was run.
  All float-level recomputations below are labelled **NON-RIGOROUS**; all margins are
  rounded DOWN. The flagship chain's certified receipts are untouched and their
  sha256 pins still verify.
- Goal (ticket): certify a second G_5 Selberg-zeta zero to the flagship standard
  (proven tail F_R, closed-contour winding, K_s gate) at a real part distinct from
  the flagship 0.4538951800749447, upgrading `NO_VERTICAL_LINE_COROLLARY.md` to
  "the non-real strip zeros of Z_{G_5} lie on NO single vertical line".

## 1. Pin coordinates and provenance

Best-known coordinates (N = 22 production value):

- **s = 0.24302842340131198 + 10.560296779143401 i**, |det| at midpoint 3.56e-15.

Provenance:

- Source scan: `code/out/resonance_v2.json` (worktree `aletheia-restore`),
  entry `g5_even_localization[9]`, Newton label `g5even(0.27,10.50)`, seed
  `(0.26542, 10.5)`, 6 Newton steps, `in_strip: true`.
- **Winding already certified at scan level**: `winding_number = 1`,
  `zero_certified: true`, winding ball `[0.99996722, 1.00003277]` (K_per_edge = 28,
  box half-widths hx = hy = 0.012). One of only five winding-certified G_5
  coordinates (V1, `lane_b/ADVERSARIAL_REVIEW_V1.md` §1.5).
- **N-stability (per the scan's own record)**:
  - N=16: Re 0.24303292864793075, Im 10.560295403304014
  - N=22: Re 0.24302842340131198, Im 10.560296779143401
  - N=28: Re 0.24302842350047418, Im 10.560296780329328
  - re_spread = 4.505e-6, im_spread = 1.377e-6, `N_stable: true` (scan tolerance).
- V1 ruling context: `plans/wayfinder/rh-goals/tickets/flagship-statement-ruling.md`
  and `lane_b/ADVERSARIAL_REVIEW_V1.md` §1.5 — this is "the omitted point nearest
  the arithmetic line"; the geometry run's band started at 0.30 and excluded it.

**Critical caveat for box placement:** the N=16→22 Re drift is 4.5e-6, i.e. the
N=16 pin lies OUTSIDE a 1e-6 half-width box centered on the N=22 value. The
flagship pin was re-pinned at N=22/28/36/44 stable to 8 decimals before its box
was frozen. The same re-pin must happen here before the 1e-6 box is fixed (see
§5, blocker B1).

## 2. Reuse assessment against the flagship R3b chain

The flagship orchestrator `.worktrees/aletheia-restore/code/tc_rerun/certify_r3b_flagship.py`
consumes: R2 envelope (sha-pinned, box hard-checked at
`certify_r3_flagship.py:420-425`), TB V2 blocks (sha-pinned), W V2 (via R2's
source bindings), and computes the endpoint bound B at
`r3b_endpoint.flagship_s_box()` (hard-coded flagship box, `r3b_endpoint.py:53-57`).
Verdicts below are from reading the certifying code's actual dependencies.

| Receipt | Verdict | Why / what changes at the new box |
|---|---|---|
| TB_BLOCK_CERTIFICATES_V2 | **REUSABLE VERBATIM** | Bounds |θ_n| image ratios, pole/branch-cut margins; no `s` anywhere (`certify_tb_blocks.py:162,205-218`). rho_star = 0.6978014..., radii (3.14, 2.27, 1.70) unchanged. `TB_V2_EXPECTED_SHA256` stays valid as-is. |
| E1_ENLARGED_CONTRACTION | **REUSABLE VERBATIM** | rho_hat ≤ 0.9483436, min pole/cut margin ≥ 1.0023799 on z-discs R_i+0.1; no `s` in `certify_e1_enlarged.py`. (Consumed at assembly-doc level, not by R3b code directly.) |
| K_s gate | **REUSABLE VERBATIM** | Exact global zero lattice, q=5 only (see §3). |
| W_ENVELOPE_CERT_V2 | **MUST RE-RUN** | Per-box weight sups `A·d_n^(−p)`, p = 2σ_lower; W⁽⁰⁾ = (λ²)^(−s)·ζ(2s, ·) evaluated on the closed s-box. Receipt holds only g5_pin_1..8; R2 strictly validates the box (`certify_r2_flagship.py:358-373`). |
| R2_FLAGSHIP_ENVELOPE | **MUST RE-RUN** | Whole envelope built at the box: ζ(2s+m) arc sups, (denom²)^(−s) weights, deep tail p = 2σ, angle factor exp(|Im s|·angle) (`certify_r2_flagship.py:465,489-503`). T_tail(128), T_tail(160), B_total all box-local. |
| Endpoint B (`r3b_endpoint`) | **box-LOCAL; code edit needed** | `flagship_s_box()` hard-coded; s enters enlarged-contour weight, Hurwitz Φ_0, σ_lower, deep-tail angle factor (`r3b_endpoint.py:95-121,189`). |

**Degradation warning (all three box-local pieces get strictly worse):**
σ drops 0.4539 → 0.2430, halving the deep-tail exponent (p ≈ 0.908 → 0.486);
|Im s| rises 5.76 → 10.56, inflating every exp(|t|·angle) factor. In the existing
W V2 table, dropping p from 0.908 to 0.800 already inflates the dominant head
weight from 18.64 to 232.2; at p ≈ 0.486 the re-run constants will be materially
larger than any existing row. Whether the final R3b margin (F_R vs. contour lower
bound) closes at N=160 at the new box CANNOT be inferred from existing receipts —
the flagship closed with a minimum margin of only 3.4e-8.

## 3. K_s gate check at the new pin

Gate statement (`lane_g/KS_GATE_REPORT.md`, `ks_gate_receipt.json`; code
`.worktrees/aletheia-restore/code/ks_gate/ks_gate.py`): K_s is the MMS
over-counted-orbit operator; `det(1−K_s) = ∏_{n≥0} (1 − ℓ_5^(2s+2n))` with
ℓ_5 ≈ 0.11442064802926044, a_5 = −log ℓ_5 = 2.167873726556495. The exact zero
lattice is **s = −n + iπk/a_5** (n ≥ 0, k ∈ Z; vertical spacing 1.44915850729921),
so **every K_s zero has Re = −n ≤ 0** and the whole open half-plane Re(s) > 0 is
certified free — independently crosschecked to ~1e-89 relative error
(`KS_CROSSCHECK.md`, CONFIRMED).

Flagship metric: point-to-lattice Euclidean distance from pin center to nearest
lattice zero (contamination tolerance 1e-10). Flagship pin's margin: 0.455100
(rounded down).

**New pin (flagship's own `nearest_zero` code, plain floats — NON-RIGOROUS
recomputation over an exact lattice):**

- Nearest lattice zero: (0, 10.144109551094493) (n=0, k=7).
- **Point clearance: 0.481952** (rounded down from 0.4819523531...) — verdict CLEAR.
- Closed 1e-6 box metric: **0.481950** (rounded down) — CLEAR.
- Supporting product check: |det(1−K_s)| ≈ 1.1339 (NON-RIGOROUS float value).

The margin at the new pin (0.481952) is LARGER than the flagship's (0.455100).
No new K_s certification is needed; only the per-pin distance evaluation, done
above. For the production run, re-evaluate through the certified Arb path rather
than these floats.

## 4. Execution plan (NOT executed)

Reuse the lane_f `kaggle_f7` bundle pattern (`research_notes/rh_goals_2026-08-14/lane_f/kaggle_f7/`,
16 chunk dirs, zlib+base64 self-contained runners, absolute-path scaffold,
`--arcs i:j --workers 4`, 5-slot feeder) with the q=5 engine.

- **Phase 0 — local re-pin (light, hours).** Re-pin at N = 22/28/36/44 (V1's
  flagship pattern) from seed (0.243, 10.56). Freeze the box center only if Re is
  stable to ≥ 8 decimals; otherwise widen the box or escalate N. Output: frozen
  `PIN_RE`/`PIN_IM` for the second-pin code copies.
- **Phase 1 — box-local receipts (local, background).** (a) W envelope for the new
  box; (b) R2 re-run in COPIES of `certify_r2_flagship.py`/`certify_r3_flagship.py`/
  `r3b_endpoint.py`/`certify_r3b_flagship.py` with new PIN constants (originals are
  sha-pinned by the flagship receipt — never edited in place); (c) update
  `R2_EXPECTED_SHA256` in the orchestrator copy after (b); (d) add the two Kimi-K3
  guards mandated for any re-run (assert rho ≥ center_ratio in `r3b_endpoint.py`;
  assert unique FTC direction overlap in the orchestrator).
- **Phase 2 — local smoke arc.** `--self-test` (derivative sanity), then
  `--arcs 0:2 --workers 4` locally. Expected ≈ 2 × 212 s CPU ≈ 7 min wall
  (NON-RIGOROUS, flagship calibration). Gate: both arcs accepted, chunk receipt
  well-formed, F_R(new box) from Phase 1 inspected against the flagship's 1.78e-6.
  If F_R or per-arc margins look fatal at N=160, STOP and re-plan N before Kaggle.
- **Phase 3 — 16-chunk Kaggle run.** Frozen partition of the 192 base arcs:
  chunk NN → `--arcs (12·NN):(12·NN+12)`, 00 → `0:12` … 15 → `180:192`;
  4 workers/kernel, CPU-only, internet on (pip install python-flint), 5-slot
  feeder loop. Per-chunk wall estimate: 12 arcs × 314 s CPU ÷ 4 workers + ~310 s
  fixed overhead ≈ 21 min (NON-RIGOROUS; flagship calibration, ×2 subdivision
  buffer ≈ 45 min) — far under the 12 h session cap. Total ≈ 17–27 CPU-h over
  ≈ 3 feeder cycles (16 chunks ÷ 5 slots). Per-chunk receipts to
  `/kaggle/working/`, harvested as in `kaggle_f7/harvest/chunk-00/`.
- **Phase 4 — merge and closure.** Feed the 16 chunk `closed_contour[str(N)]`
  dicts to `merge_chunks_and_verify_closure` (contiguous tiling, all
  `chunk_gate_pass`, record-count check), then the adjacent-box overlap-polygon
  winding check. NOTE: no driver script calls the merge yet (lane_f hasn't
  reached it either) — it must be written.
- **Phase 5 — comparison arm + assembly.** N=128-style lower-N control arm
  (expected NOT_CERTIFIED by design, ~90 s), report render, assembly into the
  second-pin cert doc, corollary upgrade in `NO_VERTICAL_LINE_COROLLARY.md`.

Flagship cost calibration (from `R3B_FLAGSHIP_CERT_RECEIPT.json`): total runtime
10193 s (8 workers, local); closed contour N=160 wall 10075 s; 284 accepted
subarcs from 192 base arcs (92 subdivisions); per-record wall mean 212.4 s
(190–236 s); per-base-arc CPU mean 314 s (max 466 s, arcs 17–21); setup phases
≈ 220 s total. Measured q=7 Kaggle chunk (for the bundle-pattern sanity check):
12 arcs, 4 workers, 4.85 h wall at N=256 — chunk mechanics work as designed.

## 5. Honest blocker list

- **B1 — Box not yet freezable.** N-stability spread at the scan is 4.5e-6 in Re,
  5× the intended 1e-6 half-width, measured only at N ≤ 28. The pin must be
  re-pinned at N = 22/28/36/44 (as V1 did for the flagship) before Phase 1;
  if 8-decimal stability fails, the box must be widened (raising all arc costs)
  or N escalated.
- **B2 — F_R closure at N=160 is not inferable.** Every box-local constant
  degrades (p: 0.908 → 0.486; |t|: 5.76 → 10.56), and the flagship closed with
  only 3.4e-8 minimum margin. The second pin may need N > 160, with per-arc cost
  rising steeply (q=7/N=256 arcs cost ~24× the q=5/N=160 arcs). Phase 1–2 must
  produce the actual F_R before any Kaggle spend.
- **B3 — Merge rejects subdivided chunks.** `merge_chunks_and_verify_closure`
  requires merged accepted-record count == 192 exactly; the flagship needed 92
  subdivisions (284 records). Either the merge helper must be extended to
  subarc-level seam handling, or each chunk must accept its 12 base arcs whole
  (not guaranteed at the new box). This is a code task, not just ops.
- **B4 — Bundle generator must be rewritten.** lane_f's `make_bundles.py` was
  session scratchpad, never committed; the q=5 dependency closure must be
  re-derived (self-test + `sys.modules` trace, per `F7_STAGE3_LAUNCH.md` §3).
  Expect the same multi-push debugging lane_f needed (3 failed pushes).
- **B5 — Hash-pin plumbing.** New R2 sha must replace `R2_EXPECTED_SHA256`;
  PIN constants live in three files; all edits in copies. The orchestrator's
  recorded source bindings will all change sha — the second-pin receipt must
  not be confused with the flagship's.
- **B6 — Latent code hazards (Kimi K3 audit, documented in `R3B_FLAGSHIP_CERT.md`).**
  Re-run must add: assert rho ≥ center_ratio (hazard 1-C3; valid at the flagship
  only because 0.6958 > 0.5882 — must be re-verified at the new box), assert
  unique FTC direction overlap (1-C4), and re-derive the two hard-coded gate
  literals from raw per-arc records (1-C5).
- **B7 — Convention sensitivity (V1, unresolved).** An independent
  reimplementation placed a G_5 pin at 0.4332 vs 0.4539 — the even-sector
  convention gate is not closed. The second pin at 0.24303 upgrades the
  no-vertical-line corollary only to the extent the convention gate holds for
  BOTH pins; the corollary statement must carry that caveat.
- **B8 — Live lanes untouched, by constraint.** Nothing in lane_f (live q=7
  Kaggle run), lane_p, or `law_probes/u1_guard_extended.*` may be modified; the
  q=5 bundle is built fresh under a new directory, and lane_g's flagship
  receipts stay byte-identical.
