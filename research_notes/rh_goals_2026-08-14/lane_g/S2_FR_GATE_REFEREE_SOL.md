# S2 `F_R` merge-gate soundness referee report

- Date: 2026-08-26
- Status: UNREFEREED
- Author: gpt-5.6-sol via codex

**VERDICT: SOUND-WITH-CONDITIONS.** The exact-string equality gate is stronger
than the mathematics requires. A common outward-rounded `F_max` plus a
definitely-positive adjusted radial margin is sound, subject to the conditions
in item 4. The present `merge_s2_chunks.py` does not implement that relaxation.

## 1. Premise audit: `F_R`, the stored margin, and Arb arithmetic

### Code and receipt identity actually checked

I read the complete `F_R` producer/consumer chain in:

- `research_notes/rh_goals_2026-08-14/lane_g/kaggle_s2_contour/merge_s2_chunks.py`;
- `.worktrees/aletheia-restore/code/second_pin/certify_r3b_flagship.py`;
- the directly-called tail, endpoint-correction, and contour-geometry routines
  in `certify_r2_flagship.py`, `r3b_endpoint.py`, and
  `certify_r3_flagship.py`.

I also parsed all 39 full JSON receipts in `chunk_receipts/` and
`local_receipts/`. Twenty-three are complete `CHUNK_ARCS_CLEAR` receipts. All
23 have `immutable_hashes_verified=true` and the same nine `source_bindings`
SHA-256 values. Re-hashing the current bound source files reproduces eight of
the nine hashes. The exception is the current
`certify_r3b_flagship.py`: its current hash is
`7468cbd19a5866b1df2870a93de1330ea4f35252afd665d4948b949a606a010e`,
whereas every receipt binds
`4ac59a18767bbf36ff39b0fb90a910685ea92b07391c352cff87ee75c8203840`.
The receipt-producing version is git commit `9763dba`; the complete diff to
the current file adds only platform/python-flint provenance imports and an
`environment` result field. It does not change any bound, arc, margin, tiling,
or winding computation.

The historical receipts themselves do **not** record platform provenance:
zero of 39 full receipts has an `environment` field. Thus I verified the two
numeric receipt families and their identical source hashes, but I cannot
independently certify from these receipts alone the asserted
Linux/x86_64-versus-macOS/arm64 attribution. That causal attribution is not
needed for the soundness result below.

### (a) `F_R` is an upper bound, not one canonical enclosed real — CONFIRMED

`compute_endpoint_trace_bound` constructs, with outward upper endpoints,

```text
B_retained = upper(sum(full_retained_column_bounds))
T_tail     = upper(parsed R2 tail bound)
B_same     = upper(B_retained + T_tail)
F_R        = upper(T_tail * exp(1 + 2*B_same))
```

at `certify_r3b_flagship.py:537-580`. The R2 tail formulas finish with
`.upper()` (`certify_r2_flagship.py:538-548`), and the omitted-output
corrections do likewise (`r3b_endpoint.py:339-374`). The result is named
`F_R_upper_bound`; it is subsequently used as a radius bounding the absolute
Fredholm-versus-finite determinant perturbation. There is no lower endpoint
claim for a uniquely defined optimal `F_R`.

Qualification: each printed Arb string is, of course, an interval enclosure of
the particular outward-rounded bound representative that was computed. What
is false is that the two strings must enclose one canonical exact value. Two
different rigorous upper bounds may be disjoint without contradiction.

The two complete-receipt families contain exactly these endpoint strings:

```text
local:
[2.08944841554480794546893170303518402484279326150214266103429255553903168777160838104954000553255960867179384564034473972e-8 +/- 4.18e-128]

harvested chunk family:
[2.08944841554497520863892307386648173354244770597320612790733059618003593619919947219887582026217633244896118392991260411e-8 +/- 4.52e-128]
```

They are disjoint. Comparing one complete receipt from each family verifies
that the 864 finite column-norm strings differ at exactly indices 576 through
863, and nowhere else; the maximum absolute norm difference is enclosed by

```text
[1.98389919286245224236706000987040436998706369422691006256173689017573980512694298816721646225402984209424652683187861715e-14 +/- 3.02e-134].
```

This changes the finite column-norm sum by approximately
`4.0025675854682237e-14`, the retained/`B_same` bound by approximately
`4.0025675854685200e-14`, and `F_R` by approximately
`1.6726316999137083e-21`. The task's causal summary is correct as the dominant
trace, but not literally exhaustive: 576 output-tail correction strings also
differ (indices 0-287 and 576-863), with total difference only about
`2.9632846812836567e-27`. `T_tail` is identical.

### (b) Meaning of `minimum_finite_lower_minus_F_margin` — CONFIRMED, with exact semantics

For every accepted leaf, `_jacobi_taylor_arc` computes

```python
finite_abs_lower = finite_box.abs_lower()
margin = (finite_abs_lower - F).lower()
```

and stores it as `finite_lower_minus_F_margin`
(`certify_r3b_flagship.py:676-716`). The chunk result stores the Arb minimum of
the reparsed per-record margins as
`minimum_finite_lower_minus_F_margin`
(`certify_r3b_flagship.py:1234-1241`; serial analogue at lines 911-920).

Thus the field is a conservative enclosure of the minimum, over accepted
leaves in that chunk, of

```text
(certified lower bound for |finite Taylor determinant|) - (F used by the leaf).
```

It is not an exact decimal scalar. It is also diagnostic in the current code:
the existing chunk gate uses the per-record `inflated_det_excludes_zero`
booleans, not this aggregate field.

### (c) Post-hoc margin arithmetic — VALID only with directed endpoints

For a chunk whose old bound is the constant `U_c`, let `M_c` be its stored
minimum lower margin and let `U_max >= U_c`. Algebraically,

```text
min_i(L_i - U_max) = min_i(L_i - U_c) - (U_max - U_c).
```

Therefore the proposed subtraction is valid. Arb text round-trips do not
invalidate it, but they forbid midpoint arithmetic. The installed
python-flint 0.9.0 documents that `.lower()` rounds toward `-infinity`,
`.upper()` rounds toward `+infinity`, and decimal serialization/reparse may
widen a ball. A proof-producing implementation must therefore use the
equivalent of:

```python
U_c = arb(record_F_text).upper()
U_max = outward_max_of_all_U_c
delta_upper = (U_max - U_c).upper()
new_margin_lower = (arb(recorded_margin_text).lower() - delta_upper).lower()
gate = new_margin_lower.lower() > arb(0)
```

The parallel worker serializes and reparses `F` before evaluating an arc
(`certify_r3b_flagship.py:935-947,1021-1033`). Accordingly, the cleanest gate
uses each record's `F_R_upper_bound`; either verify that it is constant within
the chunk or correct each record separately. Using a midpoint, Python float,
`Decimal` midpoint, lexicographic string maximum, or the upper end of a stored
margin would not be rigorous.

## 2. The crux: every closed-contour consumer of `F_R`

The dataflow is exhaustive:

1. `run` reparses the endpoint `F_R` with `.upper()` and passes it to the
   serial or parallel cover evaluator
   (`certify_r3b_flagship.py:1511-1579`).
2. `_jacobi_taylor_arc` is the only mathematical per-leaf consumer. It forms
   the finite determinant box, inflates it by `F`, checks exclusion, and
   records the scalar lower-minus-`F` margin
   (`certify_r3b_flagship.py:593-716`). `F` can affect whether that leaf is
   accepted or subdivided.
3. The serial/parallel cover code only aggregates the resulting booleans,
   boxes, and margins (`certify_r3b_flagship.py:735-930,972-1251`).
4. `merge_s2_chunks.py:87-117` reads the endpoint `F_R` text solely for the
   exact-string consistency refusal. After that refusal, neither `F_R` nor an
   inflated box enters closure or winding. Lines 120-134 merely copy the
   minimum recorded margin to the merged receipt.

The seam and winding logic has no hidden uniform-`F` dependency:

- chunk ranges must tile `[0,192)` contiguously;
- accepted L/R lineages must dyadically tile each base arc exactly once and
  remain in boundary order (`merge_chunks_and_verify_closure`,
  `certify_r3b_flagship.py:251-360`);
- only stored `finite_Taylor_det_box` values are reparsed for closure
  (`certify_r3b_flagship.py:361-365`);
- `certified_winding_via_overlap_polygon` independently requires every finite
  box to exclude zero, intersects every adjacent pair including the closing
  seam, selects overlap points, certifies a half-plane for each polygon edge,
  sums Arb argument increments, and pins the winding integer
  (`certify_r3b_flagship.py:179-248`).

The straight-line homotopy is not a separate numerical routine. The code
assigns the finite winding to the full determinant when all local perturbation
exclusions pass, and its report explains that the nonvanishing straight-line
perturbation preserves winding (`certify_r3b_flagship.py:906-908,1229-1231,
1376-1382`). No step of the overlap polygon, dyadic tiling, seam closure, or
winding sum consumes a uniform `F`.

There is one important representation distinction. `_inflate` adds an Arb
radius independently to the real and imaginary coordinates, so the code's
`inflated_det_excludes_zero` tests a coordinate square. A positive
`finite_abs_lower - F` margin does not, in general, imply exclusion by that
larger square. It does directly imply the needed radial theorem because `F_R`
bounds the complex absolute determinant error. The relaxed gate must therefore
be described as a radial-modulus homotopy gate. If an implementation wants to
continue claiming that the old coordinate-square predicate was checked at
`F_max`, it must instead re-inflate the stored finite boxes and recheck them.

## 3. Locality of the per-arc zero-exclusion argument

The argument is genuinely local. On an accepted leaf `A`, let `d_N(s)` be the
finite determinant and `d(s)` the Fredholm determinant. The receipt supplies

```text
|d_N(s)| >= L_A,        |d(s) - d_N(s)| <= U     for every s in A.
```

If `L_A - U > 0`, then for every `t in [0,1]`,

```text
|d_N(s) + t(d(s)-d_N(s))| >= L_A - t U > 0.
```

This proof uses no neighboring leaf and no global constant. At seams, the
underlying finite and Fredholm determinants are the same functions because
`N`, geometry, and bound source hashes are common; the merge independently
checks finite-box overlap and exact boundary order. Piecewise-valid local
bounds therefore patch to a nonvanishing homotopy on the entire closed
boundary. Taking their maximum is merely a conservative way to restate those
local bounds with one uniform number.

Post-hoc inflation does not require rerunning the matrix/Taylor certification.
It does require proving the adjusted inequality on every retained leaf (or,
when one constant `F` was used throughout a chunk, proving it from that
chunk's correctly aggregated minimum).

## 4. Verdict, exact conditions, and current-cover numeric check

**VERDICT: SOUND-WITH-CONDITIONS.** The conditions are exactly:

1. Retain the existing eligibility gates: complete N=288 chunk receipts,
   verified common source bindings, the same contour geometry, locally clear
   finite/old-`F` arc gates, a contiguous 192-base-arc cover, exact dyadic leaf
   tiling, finite-box seam overlap, and a pinned finite winding.
2. Verify record-level `F_R_upper_bound` consistency within each chunk, or
   correct every record separately. Do not silently pair an aggregate margin
   with an unrelated top-level `F_R` string.
3. Form `F_max` from outward Arb upper endpoints. Subtract an outward upper
   bound for `F_max-F_chunk` from a downward lower endpoint of the stored
   margin, and require definite positivity (`lower() > 0`) for every selected
   chunk. Midpoint arithmetic is forbidden at the theorem gate.
4. Make that positivity test an actual prerequisite of the merged/full
   determinant verdict. The present merge result's
   `closed_contour_gate_pass = (winding is not None and winding >= 1)` is not
   sufficient by itself after removing exact `F_R` equality.
5. State the resulting proof as the radial absolute-error straight-line
   homotopy. To retain the stronger coordinate-square
   `inflated_det_excludes_zero` claim at `F_max`, re-inflate every stored finite
   box and recheck it instead of relying only on the scalar margin.
6. Record `F_max`, every adjusted chunk margin, and the receipt/source hashes
   in the merged receipt. Preserve all seam, tiling, and winding checks; the
   `F_R` relaxation authorizes no weakening of them.

The current greedy cover selected by `merge_s2_chunks.py` contains 16 chunks:
15 local-family 12-arc chunks and the harvested-family `[36,48)` chunk. It
tiles `[0,192)`, with 452 accepted leaves and 260 subdivisions. All 16 record
one constant per-record `F_R` within the chunk and pass the directed Arb
adjustment against the record-level outward common maximum

```text
[2.0894484155449752086389230738664817335424477059732061279073305961800359361991994721988758202621763324489611839299127553876360731492623514721e-8 +/- 4.24e-148].
```

The tightest adjusted margin is in
`local_receipts/S2_CHUNK_a156-168.json`, range `[156,168)`, receipt SHA-256
`83d431ee142731ecfb7ec7df6950328e67c7b8806bd22522a382f1e701fa7598`.
After taking the stored margin downward, the common-minus-local increment
upward, and the final difference downward, its rigorous directed lower
endpoint is represented by Arb as

```text
[3.0645543293767844920819612492252622347645773199367381872629676457969447590949508442431022093015417627748037653114174708335223079669138204751e-8 +/- 1.03e-148],
```

which is definitely positive. No certification or winding pipeline was run;
this was receipt parsing plus the requested sub-core-minute margin arithmetic.

## What a second referee must check

- Independently verify that the operative determinant perturbation theorem
  makes `F_R` an absolute complex-modulus error bound uniformly on the stated
  closed coordinate box; this review traced how the code constructs and uses
  that bound but did not re-prove the trace-ideal theorem.
- Reproduce the 16-chunk cover, record-level `F_R` checks, outward `F_max`, and
  the full-exponent tight margin with python-flint at 384-bit precision.
- Recompute the nine source hashes from the exact receipt-producing snapshot,
  and confirm that the current orchestrator delta remains provenance-only.
- Review the eventual merge patch line by line: adjusted positivity must be a
  gate, not merely output metadata, and all range/tiling/seam/winding checks
  must remain intact.
- Check that result-field names distinguish the radial margin proof from the
  stronger coordinate-square inflation predicate, or require explicit square
  re-inflation if the latter name is retained.
- If the hardware-cause narrative matters, establish it from external run
  provenance. The current historical JSON receipts do not contain OS,
  architecture, or python-flint-version fields.
