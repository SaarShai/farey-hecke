# q=8 Schur continuous-contour repair — cold referee

Date: 2026-08-19
Reviewed candidate commit: `8c1f401a66270de0fd7d2476c3137416b67802c`
Review worktree: `.worktrees/law-q8-schur-repair-20260819`
Review branch: `codex/law-q8-schur-repair-20260819`

## Verdict

**GAPS NOT REFUTED.**

At the bounded implementation scope, the repaired complex enclosure, F1024
factor/receipt/source binding, corrected adverse tail comparison, and explicit
fail-closed full-tail gate are confirmed by source inspection and fresh runs.
The overall cold review remains **GAPS NOT REFUTED** because checkpoint v2
does not bind the bytes of `q8_schur_contour.py` and accepts syntactically valid
PASS boxes without recomputing them. A forged full-shard checkpoint can change
the emitted diagnostic `finite_section_winding` and set
`all_strict_gates_pass=true`; the independent missing-tail gates still force
the global result to `OPEN`/exit 2, so this is not a demonstrated route to a
global PASS. The checkpoint claim must be narrowed or repaired before calling
the checkpoint path safe.

This is not a q=8 theorem, Fredholm, Selberg, resonance, or LAW certificate.
The first remaining mathematical gap is a certified omitted-output-row /
projection tail combined with the input-column tail in one explicitly bound
Hardy/Hilbert (and propagated trace) norm.

## 1. Scope and exact candidate pin

The isolated worktree was clean before review and resolved exactly to the
requested commit:

```text
$ git status --short --branch
## codex/law-q8-schur-repair-20260819
$ git rev-parse HEAD
8c1f401a66270de0fd7d2476c3137416b67802c
```

Only this referee file is changed in this worktree. No candidate, MAP, task,
receipt, or generated contour artifact was edited.

## 2. Confirmed repairs at bounded implementation scope

### Full complex displacement enclosure

`complex_modulus_enclosure` returns
`acb(arb(0, radius), arb(0, radius))` at
`q8_schur_contour.py:126-132`. This is the rectangle
`[-B,B] + i[-B,B]`, which contains every complex displacement with modulus at
most `B`. `arc_certificate` uses it for every entry at lines 453-459.

The literal prior endpoint counterexample is covered by the new unit test and
was rerun:

```text
$ PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python -m unittest -v test_q8_schur_contour_repair.py
Ran 7 tests in 0.031s
OK
```

The test specifically checks that the old pure-imaginary `acb(0,B)` excludes
the endpoint displacement while the new two-coordinate rectangle contains it.

### F1024 factors, receipt bytes, source bytes, and geometry

The production factors are the exact strings `("10", "4", "2")` at
`q8_schur_contour.py:56`; the loader rejects any other TB factor list at
lines 276-280. It verifies the R2/TB/W file bytes and four source-module bytes
against hard-coded SHA-256 values at lines 244-257, then computes engine
geometry with those same factors and requires interval overlap against the
R2, TB, and W geometry payloads at lines 282-317. The arc engine receives
`RECEIPT_FACTORS` at lines 437-442, so the checked geometry is the production
matrix geometry, not a label-only check.

Fresh hash receipt:

```text
q8_r3b_engine.py       8b63dfbfc6bad21b01a951cbbf9f25e5a218f0353f9dd1c3493674b311aca2fc
q8_contour_helpers.py  54ff4dcf39b6f1521cdf25ad769e37a1b4858fc8e07dc711e015fb7cd13da2f0
f8_source_builder.py   e7a27aaa23074eb5722c1d392a5a93f73f787c02ebc6f5faeb2af1d0802f747a
f8_certify_tb_blocks.py 30fd9b15a9425b1a356753f667909a8d58d826d4ac1e30f1a2e7667fcc73871c
R2                     80daa5de82c4e47d43c3b4aaa84a5955be5281f2cb147e7730766a1bba946043
TB                     5f9cd3f9179c5b15539b3666bd3a2a3144995408648369dc1db6eda36f51d35c
W                      7d7b33966e48c3fe5f45fcf9618943f17a65ca4ef91caa7e3b2067904d03011e
```

The tampered-R2 regression rejects a byte change before JSON use. This is a
real binding for the named F1024 receipts and their source/geometry inputs.

### Omitted-output tail and global fail-closed behavior

`load_operator_bounds` explicitly names the computed quantity
`input_tail_only`, sets `output_projection_tail=None`, `full_tau=None`, and
`full_tail_certified=False` at `q8_schur_contour.py:350-408`. The per-arc gates
include both the corrected receipt check and the unavailable full projection
tail at lines 461-465. `main` seeds `unresolved` from both false gates at lines
717-721, and emits `OPEN`/exit 2 whenever unresolved at lines 746-790.

The fresh N=2 and N=4 bounded runs both preserve this fail-closed state:

```text
N=2: smoke_exit=2; result_status OPEN; factor_strings ['10', '4', '2'];
     geometry_verified True; tail_formula_checks_pass False;
     full_tail_certified False; full_tau None
N=4: smoke_exit=2; result_status OPEN; factor_strings ['10', '4', '2'];
     geometry_verified True; tail_formula_checks_pass False;
     full_tail_certified False; full_tau None
```

The first-arc local diagnostics also reran at both dimensions:

```text
N=2 qF_upper 2.1843890406771576664e-5... rH_upper 9.3094277116900400328e-6...
N=4 qF_upper 0.0014676909332799674571... rH_upper 4.7738356903267168084e-5...
```

These are finite local diagnostics only; neither is promoted to a global
finite/Fredholm result.

### Corrected upper-bound comparison

The adverse comparison is now exactly
`recomputed.upper() <= source.upper()` at lines 358-378. Freshly recomputed
rows fail it in the pinned receipt, as required for a conservative refusal:

```text
tail 256: source_covers_recomputed_upper False
tail 320: source_covers_recomputed_upper False
recorded_tail_checks_pass False
```

The repair does not silently accept the stale source labels.

## 3. Residual checkpoint integrity gap (load-bearing for diagnostics)

The v2 loader does improve omission handling. `validate_checkpoint_records` at
lines 565-625 rejects records outside the shard, duplicate leaves, malformed
paths, invalid terminal statuses, malformed PASS boxes, and non-exact dyadic
partitions. `load_checkpoint` rejects v1, duplicate completed arcs, and type
errors at lines 656-672. `ordered_records_and_boxes` reparses every saved PASS
box unconditionally at lines 628-643. These checks refute the prior partial-
resume omission bug.

They do **not** establish provenance or semantic correctness of a PASS record:

* `params` contains `implementation: "q8-schur-contour-repair/v2"`, factors,
  receipt hashes, and four dependency source hashes at lines 701-711, but no
  SHA-256 for `q8_schur_contour.py` itself.
* The actual checker hash is
  `0e559176aa62abc5a8229d40949f5740474bf5cb5e3e68403422336f0d400d2a`, while
  the bound source-hash keys are only
  `q8_r3b_engine.py`, `q8_contour_helpers.py`, `f8_source_builder.py`, and
  `f8_certify_tb_blocks.py`.
* A saved PASS record need only have an accepted `initial_arc`, binary `path`,
  status, and parseable `finite_taylor_box`; its `arc_index`, endpoints,
  dimension, gate map, and box derivation are not checked or recomputed.

Adversarial replay used four syntactically valid PASS leaves (`initial_arc`
0--3, `path=[]`) and four nonzero overlapping boxes that wind once. The
checkpoint passed v2 loading and supplied the boxes directly to the winding
helper:

```text
forged_boxes_direct_winding (1, ... integer_pinned: True ...)
forged_checkpoint_exit 2
{ "status": "OPEN", "N": 2, "arcs": 4, "winding": 1, ... }
forged_result_status OPEN
forged_result_winding 1
forged_all_strict_gates_pass True
forged_full_tail_certified False
forged_tail_formula_checks_pass False
```

For comparison, a fresh full N=2 run without a checkpoint returned:

```text
normal_full_smoke_exit=2
normal_full_status OPEN
normal_full_arc_count 4
normal_full_winding None
normal_full_all_strict_gates_pass False
normal_full_tail_formula_checks_pass False
normal_full_full_tail_certified False
```

Therefore the false full-tail/receipt gates remain load-bearing: the forged
checkpoint cannot turn the global status into PASS. But it can alter the
diagnostic winding and report `all_strict_gates_pass=True` even while the
global tail gates are false. The bounded repair is consequently not entitled
to claim that checkpoint v2 makes saved PASS boxes semantically safe. The
wording should say “global status remains fail-closed despite untrusted resume
diagnostics,” or the loader should bind the checker SHA and recompute/validate
the saved PASS certificates.

## 4. Remaining mathematical and scope gaps

The first mathematical gap is unchanged and explicit in the implementation:
there is no certified omitted-output-row/projection coefficient tail compatible
with the input-column tail, and therefore no full trace-norm bound for the
finite-section-to-Fredholm comparison. The following remain separately open:

1. E1 on the required enlarged disc and branch/pole holomorphy region.
2. Exact q=8 MMS-to-Hardy/Hilbert operator, basis, and norm binding.
3. Nonvanishing and exact word/lattice identification of `K_s`.
4. Common meromorphic continuation and the Selberg determinant/zeta/scattering
   factorization.
5. A complete corrected four-edge winding from recomputed boxes and a new cold
   referee after checkpoint provenance is repaired or its claim is narrowed.

No q=8 theorem, Fredholm, or LAW promotion is supported by this commit.

## 5. Validation receipts

```text
$ PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python -m py_compile \
    q8_schur_contour.py q8_r3b_engine.py q8_contour_helpers.py \
    f8_source_builder.py f8_certify_tb_blocks.py test_q8_schur_contour_repair.py
py_compile_exit=0

$ git diff --check HEAD^..HEAD
diff_check_exit=0
```

The pre-handoff impact and security triage ran against the referee commit
(`6438547`, before the metadata-only amend below):

```text
$ python3 .codex/skills/impact-of-change/tools/impact.py --repo . --diff 6438547 --json
mode degraded; risk LOW; 0 symbol(s) changed; 0 affected caller(s)
warning: impact estimated WITHOUT graph; results are lexical and unverified

$ python3 .codex/skills/security-oversight/tools/security_scan.py --repo . --diff 6438547 --json
mode lexical-triage; risk NONE; 238 added line(s) across 1 file(s); 0 finding(s)
```

The security result is lexical triage, not a proof of safety. The impact result
is intentionally marked degraded because no graph was available.

The seven-test repair suite, the endpoint counterexample, F1024 tamper/hash
check, geometry check, stale-bound direction check, missing-output-tail gate,
and v1/partition checkpoint regressions all passed as recorded above. The
two N=2/N=4 smoke runs exited 2 with `OPEN`; no N=104 run or theorem claim was
made.

## 6. Review handoff

Overall verdict: **GAPS NOT REFUTED**.  Exact candidate SHA:
`8c1f401a66270de0fd7d2476c3137416b67802c`.  The only remaining worktree edit
is this referee report. No push was performed.

**READY FOR JUDGING.**
