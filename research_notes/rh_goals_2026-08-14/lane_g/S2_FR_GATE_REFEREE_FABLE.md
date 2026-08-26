# S2 F_R merge-gate relaxation — cold referee report (Fable seat)

- Date: 2026-08-26
- Status: **UNREFEREED** (this report itself; single referee seat)
- Author: Fable referee seat (cold, adversarial; did not see the other seat's work)
- Question: is it sound to replace the "all chunks share one identical F_R(288)"
  merge gate in `merge_s2_chunks.py` with: take F_max = max chunk F_R, and require
  every chunk's re-checked margin `recorded_margin − (F_max − F_R_chunk) > 0`?

## 1. Factual premises (verified against code and receipts)

**(a) F_R is an upper bound, not an enclosure — CONFIRMED.**
`certify_r3b_flagship.py:561-563` (`compute_endpoint_trace_bound`):
`F = (T_tail * (arb(1) + arb(2)*B_same).exp()).upper()`, with every input
(`finite_norms`, `output_corrections`, `B_retained`, `T_tail`, `B_same`) built by
chained `.upper()` calls. The result is a rigorous upper bound valid on the
"entire closed flagship coordinate box" (the receipt's own `s_region`), derived
from ball enclosures whose radii depend on the platform's rounding path. Two
runs of identical code can legitimately yield disjoint upper-bound values; both
still bound the same true quantity (the finite-vs-Fredholm determinant
perturbation) from above. Formula string `T_tail(N) * exp(1 + 2*B_same(N))`
matches the code.

Verified the "identical code" premise directly: all nine `source_bindings`
sha256 values match between `chunk_receipts/S2_CHUNK_a036-048.json` (Kaggle)
and `local_receipts/S2_CHUNK_a036-048.json`; only the path prefixes differ
(`/kaggle/working/tree/...` vs `/Users/za/Documents/farey-hecke/...`). The two
distinct F values across the 16-chunk cover are exactly the two quoted:
`2.0894484155448079...e-8` (local) and `2.0894484155449752...e-8` (Kaggle),
with radii ~4.2e-128 / ~4.5e-128 — disjoint as intervals, which is harmless for
upper bounds.

**(b) `minimum_finite_lower_minus_F_margin` means what is claimed — CONFIRMED.**
Per leaf (`_jacobi_taylor_arc`): `margin = (finite_abs_lower - F).lower()` where
`finite_abs_lower = finite_box.abs_lower()` is a lower bound on |D_N| over the
closed leaf and F is that run's F_R. Directed rounding is correct at source
(lower bound minus upper bound, then `.lower()`). The chunk-level field is
`min_arb` over all leaf margins, stored as arb ball text.

**(c) `new_margin = recorded_margin − (F_max − F_R_chunk)` — VALID with directed
rounding.** Identity: `finite_lower − F_max = (finite_lower − F_chunk) − (F_max − F_chunk)`.
The recorded margin lower-bounds the first parenthesis; subtracting the ball
`(F_max − F_chunk)` in arb and taking `.lower()` of the result yields a valid
lower bound on `finite_lower − F_max`. Conditions: (i) do the arithmetic in arb
ball arithmetic on the stored texts and gate on `.lower() > 0`, never on floats;
(ii) use the **upper endpoint** of the max F ball as F_max (I used
`Fmax.upper()`, which is conservative). The stored F radii (~1e-128) and margin
radii (~1e-16..1e-20) are negligible against margins ~3e-8, so this is not
delicate in practice — but the directed form must still be used.

## 2. Does F enter anywhere besides the per-arc zero-exclusion margin? — NO.

Traced every consumer in `certify_r3b_flagship.py` and `merge_s2_chunks.py`:

- `merge_chunks_and_verify_closure` (line 251 ff.): checks contiguous chunk
  ranges, per-arc dyadic leaf tiling (Fraction bookkeeping of L/R lineages),
  chunk_gate_pass flags, then computes the winding from
  `finite_Taylor_det_box` records only, via
  `certified_winding_via_overlap_polygon`. **F appears nowhere in this path.**
- The overlap-polygon winding (`certified_winding_via_overlap_polygon`) sums
  argument increments of the FINITE det boxes; no F.
- The straight-line homotopy claim (receipt field
  `full_determinant_winding_by_nonvanishing_straight_line_homotopy`) rests on
  per-leaf `inflated_det_excludes_zero` / `finite_lower_minus_F_margin > 0`,
  i.e. exactly the per-arc exclusion the relaxation re-checks.
- `merge_s2_chunks.py` uses F only in the identity gate under referee (lines
  93-117) and as a reporting field in the merged receipt (`F_R_upper_bound`,
  line 129, and the aggregate min margin, line 132). No numeric use.

No seam, tiling, or winding step assumes a single uniform F for the closed
contour.

## 3. Is the per-arc zero-exclusion genuinely LOCAL? — YES.

The homotopy argument is pointwise: for s on the contour,
`D_t(s) = (1−t)·D_N(s) + t·D(s)` is nonzero provided `|D_N(s)| > |D(s) − D_N(s)|`.
Each contour point lies in exactly one accepted leaf, and that leaf's
certificate gives `|D_N| ≥ finite_abs_lower > F_chunk ≥ sup_box |D − D_N|`
(each chunk's F_chunk is certified over the whole coordinate box, hence at
every point of that leaf). Nothing couples the F used on one leaf to the F used
on another. In fact the relaxation is **stronger than mathematically
necessary**: since each F_chunk is already a valid upper bound of the same true
perturbation, each chunk's own recorded margin already certifies its leaves —
inflating everyone to F_max is a conservative uniformization for the merged
receipt, not a logical requirement. Post-hoc inflation to F_max is therefore
legitimate (a fortiori: exclusion vs a larger F implies exclusion vs the true
perturbation).

## 4. Verdict

**VERDICT: SOUND-WITH-CONDITIONS** — the F_max relaxation is sound provided:

1. The re-check arithmetic is done in arb ball arithmetic with directed
   rounding: `new_margin = (arb(recorded_margin) − (arb(F_max_upper) − arb(F_chunk))).lower()`,
   gate on `new_margin > 0`; F_max_upper = the upper endpoint of the largest
   F ball. No float shortcuts.
2. The identity check is replaced, not merely deleted: the gate must still
   verify every chunk shares the same N (288), that `immutable_hashes_verified`
   holds, and (recommended) that all nine `source_bindings` sha256 values agree
   across chunks — this is what licenses "two valid upper bounds of the same
   quantity" rather than "two different computations".
3. The merged receipt records F_max (and per-chunk F values) as its
   `F_R_upper_bound`, and its `minimum_finite_lower_minus_F_margin` is the min
   of the re-checked (F_max) margins, not the min of the raw per-chunk margins.
4. `chunk_gate_pass` and the tiling/winding checks in
   `merge_chunks_and_verify_closure` remain unchanged (they are F-independent).

## 5. Numeric re-check against the real receipts

Ran the merge script's own cover selection (chunk_receipts first, greedy widest
receipt per position) over `chunk_receipts/` + `local_receipts/`: 16 chunks
tiling [0,192) — 15 local 12-arc chunks plus Kaggle `a036-048`. Two distinct
F values (above); F_max = Kaggle's, upper endpoint
`2.08944841554497520863892307387e-8`.

**Every chunk passes** against F_max. Re-checked margins (arb `.lower()`
bounds) range from `3.0645543293767844921e-8` to `2.46222014715434e-6`.

**Tightest resulting margin: `3.0645543293767844921e-8`**
(chunk `local_receipts/S2_CHUNK_a156-168.json`; full exponent: times ten to the
minus eight). The F_max inflation cost each local chunk only
`F_max − F_local ≈ 1.673e-21`, thirteen orders below the smallest margin.

## What a second referee must check

1. That `F = (T_tail * (1 + 2*B_same).exp()).upper()` at
   `certify_r3b_flagship.py:563` really upper-bounds the finite-vs-Fredholm
   perturbation on the whole box — i.e. the trace-norm bound chain
   (`bound_chain` field) is mathematically valid, which this report took from
   the existing certificate structure, not re-derived.
2. Independently grep all consumers of `F_R_upper_bound` / the margin fields
   (including `evaluate_closed_cover_parallel` and any assembly/report docs)
   for a hidden uniform-F assumption — confirm my "no other use" finding.
3. Re-run the F_max margin re-check with independent code (any interval
   package), confirming all 16 pass and the tightest margin exponent (e-8).
4. Verify the nine source_bindings sha256 values match across ALL 16 cover
   chunks, not just the a036-048 pair spot-checked here.
5. Check that the greedy cover the merge script selects is the same 16-chunk
   set used here (Kaggle a036-048 shadows the local one because chunk_receipts
   is listed first), and that no accepted chunk has status != complete.
