# S2 merged-contour receipt — cold adversarial referee report (Fable seat)

Date: 2026-08-26. Status: UNREFEREED (this report is itself one referee seat).
Author: Fable referee seat (cold, adversarial; did not produce any artifact under review).

Object under review:
`research_notes/rh_goals_2026-08-14/lane_g/kaggle_s2_contour/chunk_receipts/S2_MERGED_CONTOUR_RECEIPT.json`
(merged_winding = 1, closed_contour_gate_pass = true, N = 288, 16 chunks, ranges tiling [0,192)).

Claim under review: this certifies a SECOND zero of the G_5 Fredholm/Selberg
determinant in the S2 box (centre 0.41054373549473627 + 7.81976824701551188i,
half-width 1e-6), yielding with SCAT-1 Lemma 3.1 two phi_5 zeros at distinct
real parts and closing NOGO-OPEN-1 / the open item of NO_VERTICAL_LINE_COROLLARY.

All numeric checks below were re-derived by this referee from the receipt files
(<1 core-minute total); no certification code was re-run. No file with SOL in
its name was read.

---

## 1. Does winding >= 1 certify a zero here? — CONFIRMED for the finite determinant; the finite-to-Fredholm passage is licensed but rests on inherited flagship lemmas

Code examined: `.worktrees/aletheia-restore/code/second_pin/certify_r3b_flagship.py`,
`certified_winding_via_overlap_polygon` (~line 179), `_jacobi_taylor_arc` (~593),
`merge_chunks_and_verify_closure` (~251).

Structure of the argument, as implemented:

- Per leaf, `_jacobi_taylor_arc` encloses the FINITE N=288 determinant over the
  whole closed sub-segment in `finite_Taylor_det_box` (midpoint det + certified
  Taylor radius r*G, with Neumann q < 1 and rH < 1 hard gates — both recorded
  True on every record). The 1-C4 unique-FTC-direction guard is present.
- `certified_winding_via_overlap_polygon` requires EVERY box to exclude zero,
  picks the midpoint of each adjacent-box intersection, and uses convexity of a
  nonzero rectangle to homotope the true image arc onto the polygon — winding of
  the finite determinant along the boundary is then pinned to the integer 1
  (winding_ball = [0.999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999996472261 +/- 1.22e-113], integer_pinned = true).
  By the argument principle the FINITE determinant has >= 1 zero in the box.
- Finite -> Fredholm: every record also has `inflated_det_excludes_zero` = true,
  i.e. the finite box inflated by F_R still excludes zero (I checked all 452
  merged records: 0 failures). If |det_Fredholm(s) - det_finite(s)| <= F_R for
  all s ON the boundary, the straight-line homotopy
  H(t,s) = det_fin(s) + t*(det_Fred(s) - det_fin(s)) stays in the inflated
  boxes, never vanishes, so the Fredholm winding equals the finite winding = 1.

What licenses the passage — and what this receipt does NOT itself establish:

- (a) F_R = T_tail(N) * exp(1 + 2*B_same(N)) (formula recorded in the receipt)
  must actually bound |det_Fred - det_fin| uniformly on the box. The chunk
  receipts record it for the "entire closed flagship coordinate box"
  (s_region field), which covers the boundary. I did NOT re-derive this bound:
  it is the flagship R2/TB machinery, bound in by `source_bindings`
  (single sha256 set across all 16 chunks). UNVERIFIED here, inherited.
- (b) Analyticity of the Fredholm determinant of the L_{s,+} family inside the
  box (needed for the argument principle on the Fredholm side). Not restated in
  the receipt; inherited from the flagship assembly.

Verdict on item 1: CONFIRMED as "same straight-line homotopy argument as the
flagship", with the explicit caveat that (a) and (b) are inherited hypotheses,
not contents of this receipt. The receipt's own note phrases this correctly.

## 2. Is the contour genuinely closed? — CONFIRMED (independently recomputed)

The merge code checks (i) chunk ranges tile [0,192) contiguously, (ii) every
chunk gate passes, (iii) dyadic leaf lineages tile each base arc's [0,1)
exactly once in order, with wraparound handled by `boxes[index-1]` at index 0.

I did not trust the indices. Independent recomputation from the 16 receipt
files (452 leaf records, sorted by (base_arc_index, dyadic start)):

- Seam continuity in s: mid(s_end) of every leaf equals mid(s_start) of the
  next, INCLUDING the wraparound leaf 451 -> 0. 0 breaks at tolerance 1e-14.
- Geometry: endpoint real parts span [0.41054273549473624, 0.41054473549473625],
  imaginary parts span [7.819767247015512, 7.819769247015512] — exactly the
  declared box centre 0.41054373549473627 + 7.81976824701551188i with
  coordinate_half_width 1e-6 (identical `s_region` JSON in all 16 chunks).
- Orientation: signed polygon area of the ordered leaf start-points is
  +3.999911513119514e-12 ~= (2e-6)^2, i.e. one full positively-oriented (CCW)
  traversal of the box; consistent with winding +1 counting zeros, not an
  orientation-flipped artifact.

No gap, no double-count, no orientation error found.

## 3. Are the 16 chunks legitimately combinable? — CONFIRMED, with one provenance defect

- All 16 sha256 values in the merged receipt match the files in
  `local_receipts/` byte-for-byte. The same-named files in `chunk_receipts/`
  (Kaggle harvest) do NOT match (10 name collisions, all hash-mismatched), and
  they carry a DIFFERENT F_R:
    Kaggle:  [2.0894484155449752086389230738664817335...e-8]
    local:   [2.08944841554480794546893170303518402484279326150214266103429255553903168777160838104954000553255960867179384564034473972e-8 +/- 4.18e-128]
  — the known platform split at the 12th significant digit (commit d39b8ad).
  The merge code refuses mixed F_R, so the successful merge implies it was fed
  local receipts only. That is the CORRECT homogeneous choice, but the merged
  receipt does not record which --chunk-dir fed it; provenance is recoverable
  only by hashing, as done here. DEFECT (correction 1 below).
- Consistency across the 16 local chunks (checked): identical `source_bindings`
  sha256 set (R2/TB receipts), identical `s_region`, precision_bits = 384
  everywhere, N = 288 everywhere, single F_R, every chunk status
  CHUNK_ARCS_CLEAR with chunk_gate_pass = true, min_margin positive in all 16;
  merged minimum = [3.06455432937695175525195262005655994346423176440780165413600568643794900752254193539243802403115848655197110360098571341e-8 +/- 3.07e-126] > 0.
- a036-048 replacement (re-run locally 2026-08-26): the local log
  `local_receipts/local_a036-048.log` shows a FRESH full run — 12 base arcs
  each subdivided once, 36 evaluations, 24 accepted, matching the receipt
  (accepted_leaves 24, subdivisions 12); updated_unix 1787730632 = 2026-08-26
  00:50:32 PDT. Its checkpoint `S2_CHUNK_a036-048.ckpt.json` carries the LOCAL
  F_R (2.08944841554480794...e-8), so no Kaggle-derived phase leaked in; the
  merge script explicitly skips `*.ckpt.json`, so the stale-checkpoint
  contamination vector is closed. CONFIRMED equivalent.
- Note: the local_receipts a036-048 artifacts and the merged receipt are
  uncommitted working-tree state at review time.

## 4. Fredholm zero -> Selberg zero — UNVERIFIED BY THIS RECEIPT (assembly step absent)

The flagship needed (NO_VERTICAL_LINE_COROLLARY.md, assembly links 5-7):
(i) K_s divisor: zeros of det(1 - K_s) form the lattice s = -n + i*pi*k/a_q,
all Re <= 0, hence outside any box with Re > 0 — the S2 box has
Re ~= 0.41054 > 0, so the same exclusion applies GEOMETRICALLY;
(ii) sector identification (MMS P-symmetric sector, not geometric parity);
(iii) multiplicity link from the + factor to Z_S.

For S2, the assembly-referee table (S2_SECOND_WINDING_BOX_REFEREE.md row 10)
records an s_2 K_s clearance value 0.48194877778378137 — PASS on values, but
that same referee flagged the "certified" LABEL as an open correction (C7).
No S2 analog of the assembly document exists; the merged receipt's own note
says the assembly doc is a separate outstanding step. Until that document
binds links 5-7 to THIS box, "zero of Z_{G_5}" is a forward reference, not a
certified statement. UNVERIFIED here.

## 5. Is the second real part genuinely distinct? — CONFIRMED (values re-derived from artifacts)

- Flagship pin (from NO_VERTICAL_LINE_COROLLARY.md, Corollary 1):
  Re s* in 0.4538951800749447 +/- 1e-6, Im s* in 5.7635372417301305 +/- 1e-6.
- S2 pin (from the identical `s_region` of all 16 chunk receipts, and my
  recomputed boundary span in §2): Re in 0.41054373549473627 +/- 1e-6,
  Im in 7.81976824701551188 +/- 1e-6.
- Separation of real parts: |0.4538951800749447 - 0.41054373549473627|
  = 0.04335144458020843 >> 2e-6 (sum of half-widths). Genuinely distinct in
  exactly the sense NOGO-OPEN-1 / Scope-limit 4 requires.
- Reflected phi_5 real parts (rho = 1 - s per SCAT1/S2 referee cross-check):
  1 - 0.4538951800749447 = 0.5461048199250553;
  1 - 0.41054373549473627 = 0.58945626450526373.
  The value 0.5894562645052637 in the ledger claim is the correct value
  (truncated one digit; full value 0.58945626450526373). The earlier figure
  0.5894543 is WRONG — a documented transposition error
  (S2_SECOND_WINDING_BOX_REFEREE.md, correction C2). Any promotion text must
  use 0.58945626450526373 (or a stated truncation of it), never 0.5894543.
- Caveat: calling these "phi_5 zeros" runs through SCAT-1 Lemma 3.1, whose
  applicability to the S2 point is part of the absent assembly step (item 4/6).

## 6. Missing controls — CONFIRMED absent, and material

The merged receipt's own note names two outstanding steps:
- The N=128 control arm. The flagship standard includes a second-N stability
  arm; without it, an N-sensitive artifact (a finite-rank accident at N=288)
  is not excluded by the receipt chain itself. The winding argument is valid
  at a single N given F_R, so this is a robustness control, not a logical gap
  — but "same standard as the flagship" (which NOGO-OPEN-1's wording invokes)
  is not met without it.
- The assembly document (items 4 and 5 caveats). This is a LOGICAL gap for
  every step past "zero of the finite/Fredholm determinant in the S2 box."
Additionally: the receipt is UNREFEREED, and key artifacts are uncommitted.

## 7. Overclaiming audit — the receipt vs the ledger claim

What the receipt (plus my independent checks) actually certifies:
winding 1 of the FINITE N=288 determinant along the geometrically-closed,
CCW S2 box boundary, with every leaf margin above the single local
F_R = 2.08944841554480794546893170303518402484...e-8 — hence, granting the
inherited flagship F_R-bound and analyticity lemmas, >= 1 zero of the
FREDHOLM determinant in the S2 box.

Gaps between that and the ledger claim, exhaustively:
1. "zero of the G_5 Selberg determinant / Z_{G_5}" — needs the S2 assembly
   step (K_s divisor certification for this box, sector, multiplicity). Absent.
2. "two phi_5 zeros at Re ~ 0.5461 and Re = 0.5894562645052637" — needs
   SCAT-1 Lemma 3.1 applied to the S2 point; part of the absent assembly.
3. "closing NOGO-OPEN-1" — Scope-limit 4 demands the second pin "certified to
   the same standard as s*": that standard included the assembly document,
   the control arm, and adversarial refereeing. None of the three is done.
4. NO_VERTICAL_LINE_COROLLARY's open item is a Z_S-level statement; it closes
   only when gaps 1-3 close.
5. Receipt-internal: merge provenance (which chunk dirs) unrecorded; F_R
   platform split with the Kaggle copies documented only in commit history.

None of these gaps is a refutation; every one is an unfinished step.

---

## VERDICT

PROMOTABLE-WITH-CORRECTIONS — the merged contour receipt is sound as a
finite/Fredholm winding certificate; the ledger claim may be promoted only
after ALL of:
(1) record merge provenance in S2_MERGED_CONTOUR_RECEIPT.json (chunk source =
    local_receipts only; Kaggle chunk_receipts excluded for the F_R platform
    split at the 12th significant digit);
(2) run and file the N=128 control arm;
(3) write the S2 assembly document binding K_s-divisor exclusion (box
    Re ~= 0.41054 > 0), sector identification, multiplicity, and SCAT-1
    Lemma 3.1 to the S2 box — until then the certified object is a
    Fredholm-determinant zero, not a Z_{G_5} or phi_5 zero, and NOGO-OPEN-1
    stays OPEN;
(4) quote the reflected real part only as 0.58945626450526373 (the figure
    0.5894543 is a documented transposition error and must not appear);
(5) commit the a036-048 local artifacts and the merged receipt;
(6) obtain the second referee seat below.

## What a second referee must check (independently)

1. Re-derive the F_R formula T_tail(N) * exp(1 + 2*B_same(N)) as a uniform
   bound on |det_Fredholm - det_finite| over the closed box, from the R2/TB
   receipts named in `source_bindings` (sha256
   6410dff31e503176dbf03a1b181568c99f5bc386287b109ced371f08d7eee83d for the
   R2 receipt) — this seat inherited it.
2. Analyticity of the Fredholm determinant of L_{s,+} inside the S2 box
   (argument-principle hypothesis on the Fredholm side).
3. Spot-recompute at least one leaf's `finite_Taylor_det_box` enclosure
   (midpoint det + rG radius) from the matrix builder, at a different
   precision, on a different platform.
4. The overlap-polygon homotopy lemma itself: convexity of a zero-free
   axis-aligned rectangle => the straight-line homotopy between the true image
   arc and the chord through the chosen intersection midpoints avoids zero,
   including at the two moving endpoints.
5. Re-run the seam/orientation recomputation of §2 from the raw receipts
   (not from this report's script).
6. The K_s clearance for the S2 box (value on record: 0.48194877778378137)
   and the C7 "certified-label" correction from the S2 winding-box referee.
7. That no Kaggle-computed record entered the merged leaf set: re-hash the 16
   files against the merged receipt and against `local_receipts/`.
