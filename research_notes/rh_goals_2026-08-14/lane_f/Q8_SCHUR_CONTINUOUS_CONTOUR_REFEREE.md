# q=8 Schur continuous-contour cold referee

Date: 2026-08-19.  Reviewed candidate commit
`78a8e81efcd3a9e903091c3926c7d4316a8b5122` in the isolated referee worktree
`codex/law-q8-schur-referee-20260819`.

## Principal scoped verdict

**REFUTED as a theorem-valid continuous-contour certificate.**  The finite
block API and Schur product algebra replay, but the central closed-subarc
enclosure in `q8_schur_contour.py` does not enclose the actual complex line
integral.  Therefore the reported `qF`, `rH`, finite Taylor boxes, and any
downstream winding/homotopy status produced by this implementation are not
proof receipts.  This is a refutation of the implementation's theorem-valid
claim, not a claim that the underlying q=8 determinant or law is false.

There is a second independent load-bearing failure: the production engine uses
the `(3.4, 2.2, 1.4)` source-disc factors, while the loaded F1024 TB/R2/W
receipts use `(10, 4, 2)`.  The code never checks this geometry identity, so
the numerical `Xop`/`tau` bounds cannot be attached to the matrices being
enclosed.

The remaining infinite-dimensional/Hilbert/Selberg statements are **GAPS**;
they are not upgraded and the q=8 law remains **CONJECTURAL** at this lane's
scope.  A corrected implementation must fix both defects, add the omitted
output-projection tail, and obtain a fresh cold referee pass.

## Scope and source hashes

Command:

```text
$ git rev-parse HEAD
78a8e81efcd3a9e903091c3926c7d4316a8b5122
$ git status --short --branch
## codex/law-q8-schur-referee-20260819
$ sha256sum research_notes/rh_goals_2026-08-14/lane_f/Q8_SCHUR_CONTINUOUS_CONTOUR_SOL.md \
    research_notes/rh_goals_2026-08-14/lane_f/q8_r3b_engine.py \
    research_notes/rh_goals_2026-08-14/lane_f/q8_schur_contour.py \
    research_notes/rh_goals_2026-08-14/lane_f/q8_contour_helpers.py \
    research_notes/rh_goals_2026-08-14/lane_f/f8_receipts/Q8_R2_F1024_LOCAL_RECEIPT.json \
    research_notes/rh_goals_2026-08-14/lane_f/f8_receipts/Q8_TB_BLOCK_CERTIFICATES_F1024_RECEIPT.json \
    research_notes/rh_goals_2026-08-14/lane_f/f8_receipts/Q8_W_ENVELOPE_F1024_RECEIPT.json
993de9eb3658953f6f5272d59f2f4777ca22ea80485da7d8b7a7ff173a3948c0  .../Q8_SCHUR_CONTINUOUS_CONTOUR_SOL.md
8b63dfbfc6bad21b01a951cbbf9f25e5a218f0353f9dd1c3493674b311aca2fc  .../q8_r3b_engine.py
2b90944e217bd5df322aeca068f03af95465706c9c93bd9188bef669cc3ec924  .../q8_schur_contour.py
54ff4dcf39b6f1521cdf25ad769e37a1b4858fc8e07dc711e015fb7cd13da2f0  .../q8_contour_helpers.py
80daa5de82c4e47d43c3b4aaa84a5955be5281f2cb147e7730766a1bba946043  .../Q8_R2_F1024_LOCAL_RECEIPT.json
5f9cd3f9179c5b15539b3666bd3a2a3144995408648369dc1db6eda36f51d35c  .../Q8_TB_BLOCK_CERTIFICATES_F1024_RECEIPT.json
7d7b33966e48c3fe5f45fcf9618943f17a65ca4ef91caa7e3b2067904d03011e  .../Q8_W_ENVELOPE_F1024_RECEIPT.json
```

The abbreviated `...` path prefixes above are shell display elisions only;
the hashes were computed over the named files in the command.  The source
hashes are recorded to make the cold review reproducible.  The candidate does
not itself record hashes for its engine, contour helper, or R2 receipt, and
only checks the mutable TB/W hash strings supplied by the mutable R2 JSON;
that is a receipt-provenance gap noted below.

## 1. What replays

The new direct block API has the expected locations

```text
A2=(2,1), A3=(3,2), B1=(1,3), B2=(2,3), B3=(3,3).
```

For

```text
L = [[0, 0, B1], [A2, 0, B2], [0, A3, B3]],
```

eliminating the first two identity diagonal blocks gives

```text
C = B3 + A3*B2 + A3*A2*B1.
```

The product rule in the candidate has the corresponding five terms.  The
direct block matrices and derivatives also agree with the legacy `3*N` block
assembly at the tested sample.  This is only a finite algebra/API result.

Command:

```text
$ PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import acb,ctx
import q8_r3b_engine as e
import q8_schur_contour as q
ctx.prec=192
s=acb('0.4252310423737965','4.345760788321986')
for N in (2,4,8):
  L,Lp,_=e.build_reduced_matrix_and_s_derivative(s,N,1)
  V,D=e.build_q8_block_matrices_and_s_derivative(s,N,1)
  loc={'A2':(2,1),'A3':(3,2),'B1':(1,3),'B2':(2,3),'B3':(3,3)}
  maxv=acb(0); maxd=acb(0)
  for name,(i,j) in loc.items():
    for m in range(N):
      for k in range(N):
        dv=V[name][m,k]-L[(i-1)*N+m,(j-1)*N+k]
        dd=D[name][m,k]-Lp[(i-1)*N+m,(j-1)*N+k]
        if dv.abs_upper() > maxv.abs_upper(): maxv=dv
        if dd.abs_upper() > maxd.abs_upper(): maxd=dd
  print('N',N,'max_block_value_diff_abs_upper',maxv.abs_upper(),
        'contains_zero',maxv.contains(0),
        'max_derivative_diff_abs_upper',maxd.abs_upper(),
        'contains_zero',maxd.contains(0))
PY
N 2 max_block_value_diff_abs_upper [1.17219858674850272770076052515313052983141680053666664192e-55 +/- 2.23e-112] contains_zero True max_derivative_diff_abs_upper [5.46559081779271608915750496543585946734773667933117112457e-55 +/- 7.59e-113] contains_zero True
N 4 max_block_value_diff_abs_upper [1.17219494663426771567770305828482200714268152706668566671e-55 +/- 1.10e-112] contains_zero True max_derivative_diff_abs_upper [5.46556348039548875118982405153923667405470946272931509076e-55 +/- 1.63e-112] contains_zero True
N 8 max_block_value_diff_abs_upper [1.17219412518043933794029848506669678193265617231282032105e-55 +/- 1.39e-112] contains_zero True max_derivative_diff_abs_upper [5.46555757269558462656131243405779195682113525816171287285e-55 +/- 1.47e-112] contains_zero True
```

The finite determinant identity and its derivative also replay:

```text
N 2 value_diff_abs_upper [2.90500206564629515478312766518829023008709785619510175479e-54 +/- 1.97e-111] value_contains_zero True derivative_diff_abs_upper [2.20346892647890053817313619698512978463896326161748078365e-52 +/- 2.37e-109] derivative_contains_zero True
N 4 value_diff_abs_upper [3.26777306514271969550121667651057253290006517680793803295e-52 +/- 1.92e-109] value_contains_zero True derivative_diff_abs_upper [1.52071046509123601264499500656551257188662764870875958929e-48 +/- 9.90e-106] derivative_contains_zero True
N 8 value_diff_abs_upper [1.96298262857034987032936610375407323033981081847541831854e-52 +/- 1.83e-109] value_contains_zero True derivative_diff_abs_upper [3.09762150230788742128169828074040391073496033768786871906e-47 +/- 2.00e-104] derivative_contains_zero True
```

These finite determinant values are only an algebra/API replay; they do not
certify the continuous contour or the infinite operator.

## 2. REFUTED: the continuous line-integral enclosure is not an enclosure

Candidate source:

```text
$ nl -ba research_notes/rh_goals_2026-08-14/lane_f/q8_schur_contour.py | sed -n '327,340p'
327    A0 = matrix_sub(identity(dimension), c_mid)
328    A0_inverse = A0.inv()
329    # A direct Acb evaluation of C(s_arc)-C(midpoint) has severe dependency
330    # inflation for the Hurwitz jets.  The closed-segment integral gives the
331    # theorem-valid entrywise rectangle below: |C(s)-C(mid)| is bounded by
332    # radius * sup_arc |C'(s)|.  This is the continuous Taylor enclosure used
333    # by both the Frobenius Neumann gate and the Jacobi determinant box.
334    delta = acb_mat(dimension, dimension)
335    for row in range(dimension):
336        for col in range(dimension):
337            delta[row, col] = acb(0, radius * cprime_arc[row, col].abs_upper())
338    normalized_delta = A0_inverse * delta
339    qf = frobenius_upper(normalized_delta, dimension)
340    gates: dict[str, bool] = {"qF_lt_1": definitely_less(qf, arb(1))}
```

In Arb/Acb, `acb(0,B)` has real interval exactly zero and imaginary interval
`[-B,B]`; it is not the rectangle `[-B,B]+i[-B,B]`.  The line-integral modulus
bound only says `|delta| <= B`, so an enclosing rectangle requires both real
and imaginary components to be inflated, for example
`acb(arb(0,B), arb(0,B))` (or `inflate(acb(0), B)`).

Concrete counter-replay, using the candidate's own engine and first bottom
segment, shows a nonzero real endpoint displacement excluded by the candidate
`delta`:

```text
$ PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
... compute C(end)-C(mid) and candidate acb(0,r*|C'|) for N=2, entry (0,0) ...
PY
delta_counterexample entry=0,0
endpoint_diff [-1.768445340374934833575974614726695251410033088896e-6 +/- 8.21e-55] + [3.43215913162386120290084889232805301510904325078e-7 +/- 7.03e-55]j
candidate_delta [1.80201611275187226545528152441180865232321713388370131098e-6 +/- 2.27e-63]j
candidate_delta_real_contains_endpoint_real False
```

This is a direct **REFUTATION** of the comment's “theorem-valid entrywise
rectangle” claim.  Consequently `normalized_delta`, `qF`, `correction_inverse`,
`H`, `rH`, and the finite Taylor box are not certified enclosures in the
current code.  The Frobenius and Jacobi inequalities are mathematically
usable only after the corrected complex rectangle is implemented and rerun.

## 3. REFUTED: production matrices and F1024 receipts use different discs

The candidate calls the engine with `engine.EXACT_FACTORS` at both midpoint and
arc evaluation.  The engine's exact factors come from the q=8 TB builder and
are `(3.4,2.2,1.4)`, while the pinned files named `F1024` carry `(10,4,2)`.

Command:

```text
$ rg -n 'EXACT_FACTORS|radius_multipliers_exact_strings|build_q8_block_matrices_and_s_derivative' \
    research_notes/rh_goals_2026-08-14/lane_f/q8_r3b_engine.py \
    research_notes/rh_goals_2026-08-14/lane_f/q8_schur_contour.py \
    research_notes/rh_goals_2026-08-14/lane_f/f8_certify_tb_blocks.py
research_notes/.../q8_r3b_engine.py:107:EXACT_FACTORS = source_builder.EXACT_FACTORS
research_notes/.../q8_schur_contour.py:319:        midpoint, N, SIGN, N_HEAD, engine.EXACT_FACTORS
research_notes/.../q8_schur_contour.py:322:        s_arc, N, SIGN, N_HEAD, engine.EXACT_FACTORS
research_notes/.../f8_certify_tb_blocks.py:84:EXACT_FACTORS = ("3.4", "2.2", "1.4")
$ PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
... compare engine geometry with TB/R2 receipts ...
PY
engine_factors ('3.4', '2.2', '1.4')
engine_radii ['[0.269471535227882261541147 +/- 4.77e-25]', '[0.246587841042380814962916 +/- 4.39e-25]', '[0.378837270102337889079806 +/- 2.44e-25]']
Q8_TB_BLOCK_CERTIFICATES_F1024_RECEIPT.json factors ['10', '4', '2'] radii ['[0.792563338905536063356316 +/- 1.07e-25]', '[0.448341529167965118114394 +/- 4.75e-25]', '[0.541196100146196984399723 +/- 4.76e-25]']
Q8_R2_F1024_LOCAL_RECEIPT.json factors None radii ['[0.792563338905536063356316000... +/- 1.08e-25]', '[0.448341529167965118114394000... +/- 4.76e-25]', '[0.541196100146196984399723000... +/- 2.07e-25]']
```

The exact output above was abbreviated only in the long JSON strings; the
factor mismatch and the first two distinct radii are unambiguous.  Since the
matrix entries depend on the source radii and the R2/W column bounds also do,
the current `Xop` and `tau` are bounds for a different operator geometry.
This independently invalidates the homotopy gate even if the `delta` bug is
fixed.

Corrected statement: the finite Schur algebra is valid at the engine's
`(3.4,2.2,1.4)` geometry, and the F1024 R2/TB/W bounds are valid only for their
`(10,4,2)` geometry.  A proof path must choose one geometry, pass it explicitly
through the engine and runner, compare the geometry against every receipt, and
regenerate all dependent bounds.

## 4. GAPS: the loaded tail is not a bound for the full finite-section error

The candidate forms the trace terms as

```text
$ nl -ba research_notes/rh_goals_2026-08-14/lane_f/q8_schur_contour.py | sed -n '177,182p;236,260p'
177    def single_trace_tail(weight: arb, rho: arb, N: int) -> arb:
178        return (weight * rho**N / (arb(1) - rho)).upper()
181    def tail_trace_tail(A: arb, C: arb, q: arb, rho: arb, N: int) -> arb:
182        return (A * q**N / (arb(1) - q) + C * geometric_derivative_tail(rho, N)).upper()
236        trace[name] = single_trace_tail(weight, rho, N)
247            trace_parts.append(tail_trace_tail(A, C, q, rho, N))
254    tau = (
255        trace["B3"]
256        + a3 * trace["B2"]
257        + a3 * a2 * trace["B1"]
258        + trace["A3"] * b2
259        + trace["A3"] * a2 * b1
260        + a3 * trace["A2"] * b1
```

Those formulas sum the omitted **input columns**.  The code's finite direct
matrices are `N`-by-`N`, hence represent `P_i T P_j`, not `T P_j`: omitted
output rows `(I-P_i)T P_j` are also present in

```text
T - P_i T P_j = (I-P_i)T P_j + P_i T(I-P_j).
```

No q=8 output-row coefficient estimate occurs in this candidate.  The prior
q=7 theorem-oriented chain states the missing ingredient explicitly:

```text
$ nl -ba research_notes/rh_goals_2026-08-14/lane_f/f7_certify_r3b_flagship.py | sed -n '1364,1367p'
1364  ... Jacobi ... gives ... a closed-subarc determinant box ...
1366  For each retained column, Cauchy's coefficient estimate on the certified
      enlarged output disc gives |a_m| <= U eta^m; summing m>=N gives
      U eta^N/(1-eta), which dominates the omitted-output H2 norm. Adding this
      to the computed-row 2-norm gives a full retained-column bound. Adding
      immutable R2 T_tail(N) bounds ||L||_1; the same sum also bounds ||LP_N||_1.
```

The q=8 W receipt itself retains the caveat:

```text
$ PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
... print q=8 receipt status fields ...
PY
Q8_R2_F1024_LOCAL_RECEIPT.json {'schema': 'q8-r2-local/v1', 'status': 'CERTIFIED_R2_COLUMN_ENVELOPE_R3_PENDING', 'theorem_grade_verdict': 'NO', 'analytic_linkage': 'OPEN'}
Q8_TB_BLOCK_CERTIFICATES_F1024_RECEIPT.json {'schema': 'tb-block-certificates/v2-q8', 'certification_verdict': 'PASS_RHO_LT_0.99'}
Q8_W_ENVELOPE_F1024_RECEIPT.json {'schema': 'tb-weight-envelope-cert/v2', 'status': 'WEIGHT_ENVELOPE_CERTIFIED_R2_PENDING', 'fredholm_tail': 'OPEN: this W envelope does not prove the finite-section-to-Fredholm dimension tail'}
```

Thus `tau` is at best a conditional input-tail quantity.  It is not yet a
trace-norm bound for `C-X_N P3`.  The missing output-tail term must be proved
in compatible Hardy/Hilbert norms and then propagated through the Schur
telescoping inequality.  This is a **GAP**, not a numerical failure claim
about the actual q=8 operator.

## 5. Receipt recomputation check is directionally wrong

`load_operator_bounds` records only
`source.lower() <= recomputed.upper()`.  For validating a source upper bound,
the required adverse check is that the recomputed upper endpoint is no larger
than the source upper endpoint (or that the source interval contains the
recomputed interval).  The actual values show the source interval does not
cover the recomputed interval:

```text
$ PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
... load_operator_bounds(...,104) and compare source/recomputed upper endpoints ...
PY
256 source_covers_recomputed False recomputed_covers_source True stored_check True
320 source_covers_recomputed False recomputed_covers_source True stored_check True
```

The direct recomputation is slightly larger than the source value in both
rows, while the stored Boolean remains `True`.  This does not by itself make
the code's fresh formula an underestimate—the code uses fresh row parameters
for `tau`—but it refutes the SOL's statement that the checker “compares the
complete Arb intervals” and leaves the pinned-receipt audit **GAP**.  The
repair is to require `recomputed.upper() <= source.upper()` when claiming a
source upper bound, or to bank a fresh receipt whose upper endpoint contains
the recomputation.

## 6. Conditional Frobenius/Jacobi and homotopy review

Conditional on a valid full complex `delta` rectangle, these parts have the
following narrow status:

- The Frobenius upper bound on `A0^{-1} delta` is a valid upper bound for the
  operator 2-norm; the Neumann condition `qF < 1` is a sound sufficient gate.
- The Jacobi logarithmic derivative expression has the correct product order:
  `(I-A0^{-1}delta)^{-1} A0^{-1} (-v C_N')`.  The `rH < 1` Taylor radius is
  mathematically standard under the missing enclosure and holomorphy
  hypotheses.
- The straight-line homotopy would be valid if `tau` were a trace-norm bound
  for the same full operator and `inv_arc` bounded the finite inverse in the
  same Hilbert norm.  The current code has neither the geometry binding nor
  the output-tail/Hilbert theorem required for that premise.
- The displayed `1 + Xop*inv_arc` is a conservative finite-inverse bound only
  after `Xop` is proved for the same operator; it is not a substitute for the
  omitted finite-section error proof.

No conditional formula above upgrades the candidate.  In particular, a
passing finite `qF`/`rH` record is not a proof receipt under the current
`delta` implementation.

## 7. Winding and checkpoint review

The overlap/half-plane winding helper is conservative in its basic design:
each nonzero rectangle is convex, adjacent overlaps provide seam points, and
an axis rotation into a strict half-plane gives a branch of `arg`.  It still
requires all ordered boxes from a valid four-edge run; it does not repair any
upstream enclosure or tail gap.

There is also a resume bookkeeping gap.  On a partial resume, the code loads
prior records but only reconstructs their boxes when `all_boxes` is empty:

```text
$ nl -ba research_notes/rh_goals_2026-08-14/lane_f/q8_schur_contour.py | sed -n '473,505p'
473    if args.resume is not None:
474        completed, records = load_checkpoint(args.resume, params)
475    all_boxes: list[acb] = []
...
489    # If this is a resumed run, reconstruct successful boxes from saved records.
490    if args.resume is not None and not all_boxes:
491        for record in records:
492            if record.get("status") == "PASS":
493                all_boxes.append(parse_acb_text(record["finite_taylor_box"]))
...
499    if full_shard and all_pass and len(all_boxes) == len(ordered):
```

If a checkpoint contains one completed arc and the resumed run computes a later
arc, `all_boxes` is nonempty, so prior boxes are not reconstructed; the length
test then forces `OPEN` instead of running winding.  This is conservative, but
the advertised deterministic resume-to-winding behavior is **GAPPED**.  The
repair is to reconstruct all saved PASS boxes unconditionally, then append
new boxes or simply parse the final ordered records once.

At the time of this review the live root run had not produced a final JSON:

```text
$ ps -ww -p 62989 -o pid=,etime=,pcpu=,state=,command=
62989 22:14  99.0 Rs   /Users/za/.venvs/farey-rh/bin/python research_notes/rh_goals_2026-08-14/lane_f/q8_schur_contour.py --N 104 --K 1 --max-depth 2 --out /tmp/q8_schur_n104_full_d2.json --checkpoint /tmp/q8_schur_n104_full_d2.checkpoint.json
$ python3 - <<'PY'
... read /tmp/q8_schur_n104_full_d2.checkpoint.json ...
PY
checkpoint_completed_initial_arcs [0, 1, 2] records 12
status_counts {'PASS': 12}
output_exists False
```

Those twelve PASS records across initial arcs 0, 1, and 2 are bounded
computational progress only;
they do not overcome the refuted enclosure or the open full-contour state.

## 8. Downstream gaps not touched by this lane

The candidate itself prints the following scope, which remains correct and
must not be weakened:

```text
$ nl -ba research_notes/rh_goals_2026-08-14/lane_f/q8_schur_contour.py | sed -n '506,510p'
506    result = {
507        "schema": "q8-schur-contour/v1",
508        "status": "OPEN" if unresolved else "FINITE_SECTION_AND_TRACE_HOMOTOPY_CERTIFIED_AWAITING_COLD_REFEREE",
509        "theorem_grade": "NO: E1, q8 MMS/Hilbert binding, K_s, and common continuation/Selberg factorization remain OPEN",
```

Independent of the two implementation refutations, the following remain
**OPEN / CONJECTURAL**:

1. E1 on the enlarged disc and the required branch/pole holomorphy region.
2. Exact MMS-to-Hardy/Hilbert operator identification and basis/norm binding.
3. A full output-plus-input trace-class dimension-tail theorem for every block.
4. The nonvanishing `K_s` factor and its exact q=8 word/lattice identification.
5. Common meromorphic continuation and the Selberg determinant/zeta/scattering
   factorization needed to transport a certified Fredholm zero to the law.
6. A completed four-edge ordered winding after all corrected gates pass.

## 9. Required repair order

The smallest theorem-valid repair sequence is:

1. Make the source geometry explicit and receipt-bound.  Use either
   `(3.4,2.2,1.4)` everywhere with freshly regenerated TB/W/R2 receipts, or
   `(10,4,2)` everywhere; record exact factor strings and source hashes.
2. Replace the pure-imaginary `acb(0,B)` with a rectangle containing every
   complex number of modulus at most `B`; add a regression counterexample for
   the old construction.
3. Prove and implement the omitted-output coefficient tail, combine it with
   the R2 input-column tail, and state the compatible Hardy/Hilbert norms.
4. Correct the source/recomputed upper-endpoint receipt check and pin the R2
   JSON/engine/helper hashes.
5. Fix resume reconstruction, rerun all four edges, run the winding helper,
   and obtain a new independent cold referee.  Only then can the finite/
   Fredholm status be reconsidered; E1, `K_s`, common continuation, and
   Selberg factorization still require separate proof/referee work.

## 10. Verification and gates

Syntax and diff checks on the candidate commit:

```text
$ git diff --check 78a8e81^..HEAD; echo diff_check_exit=$?
diff_check_exit=0
$ PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python -m py_compile \
    research_notes/rh_goals_2026-08-14/lane_f/q8_r3b_engine.py \
    research_notes/rh_goals_2026-08-14/lane_f/q8_schur_contour.py \
    research_notes/rh_goals_2026-08-14/lane_f/q8_contour_helpers.py; echo py_compile_exit=$?
py_compile_exit=0
```

The bounded runner smoke exits conservatively with an open gate, not a false
pass:

```text
$ PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python \
    research_notes/rh_goals_2026-08-14/lane_f/q8_schur_contour.py \
    --N 2 --K 1 --max-depth 0 --arc-start 0 --arc-end 1 \
    --out /tmp/q8_schur_ref_smoke.json
smoke_exit=2
Q8_SCHUR arc=0 leaves=1 status=OPEN
{"status": "OPEN", "N": 2, "arcs": 1, "winding": null, ...}
result_status OPEN records 1 all_strict False arc_range [0, 1]
first_status OPEN_MAX_DEPTH gates {'qF_lt_1': True, 'tail_homotopy_lt_1': False, 'rH_lt_1': True, 'finite_lower_positive': True}
```

Impact-of-change was run against the candidate commit.  No graph was available,
so the tool explicitly labels its lexical result degraded/unverified:

```text
$ python3 .codex/skills/impact-of-change/tools/impact.py --repo . --diff 78a8e81 --json > /tmp/q8_schur_ref_impact.json
impact_exit=0
mode degraded
risk HIGH
summary 33 symbol(s) changed, 1145 affected caller(s), risk = HIGH  [degraded-mode: lexical estimate]
warnings ['ATTRIBUTION: changed Python body could not be attributed to a def/class ...', 'impact estimated WITHOUT graph; results are lexical and unverified. Run `graphify extract . --backend ollama` for precision.']
```

Security oversight on the candidate diff found no lexical secret, sink,
dependency, or authz finding; this is a triage result, not a proof of safety:

```text
$ python3 .codex/skills/security-oversight/tools/security_scan.py --repo . --diff 78a8e81 --json
{"mode": "lexical-triage", "risk": "NONE", "summary": "808 added line(s) across 3 file(s); 0 finding(s) — risk = NONE", "findings": [], "routed": [], "review": [], "warnings": []}
```

The source/code review is therefore **READY FOR JUDGING** by the parent
orchestrator.  This referee file is the only intended worktree artifact; no
candidate, MAP, plan, receipt, cache, or generated contour output was edited.
