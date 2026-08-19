# q=8 Schur continuous-contour repair — second cold rereferee

Date: 2026-08-19
Reviewed stacked repair commit: `788a486c2d56ad98bc3fb2a26602e9a361dbcf4e`
Parent repair/referee commit: `e0a9b30b893a13193e7567e61e6d3961a718f92a`
Review worktree: `.worktrees/law-q8-schur-repair-20260819`
Review branch: `codex/law-q8-schur-repair-20260819`

## Verdict

**CONFIRMED at bounded implementation scope.**

The v3 checkpoint repair closes the prior cold-referee gap: checkpoint params
bind the actual checker bytes, v2 checkpoints are incompatible, saved PASS
segments are reconstructed from trusted `(initial_arc, path)` and recomputed by
the current checker, and the saved boxes are replaced before winding. The exact
prior forged four-box winding fixture now fails closed before any winding is
emitted. A call-counted harness confirmed all four saved PASS records are
recomputed and that winding consumes the fresh boxes, not saved boxes.

This verdict is only for the bounded checkpoint/finite implementation repair.
The omitted-output/projection tail remains hard `OPEN`; the finite-section to
Fredholm step, E1, q=8 MMS/Hilbert identification, `K_s`, common continuation,
Selberg factorization, and the q=8 theorem/LAW remain `OPEN`/conjectural.

## 1. Exact pin and scope

The existing isolated worktree was at the requested stacked commit before this
review:

```text
$ git status --short --branch
## codex/law-q8-schur-repair-20260819
$ git rev-parse HEAD
788a486c2d56ad98bc3fb2a26602e9a361dbcf4e
```

Only this separate rereferee file is owned here. The candidate, first referee,
MAP, tasks, receipts, and implementation files were not edited.

## 2. Checker-byte and v3-parameter binding

`CHECKPOINT_SCHEMA` and `CERTIFICATE_IMPLEMENTATION` are v3 at
`q8_schur_contour.py:68-70`. `checkpoint_parameters` at lines 566-584 stores
`checker_sha256 = sha256(Path(__file__).resolve())`, precision, contour/run
parameters, F1024 factors, receipt hashes, and source hashes. `main` computes
these current parameters before loading a resume at lines 762-783; the loader
requires exact schema and parameter equality at lines 727-743.

Fresh bytes/params receipt:

```text
v3_schema q8-schur-contour-checkpoint/v3
checker_sha_bound ef088d357da72ea44079bccfa643a4a76fc86fb87db3305566cff5e2b9233c76
checker_sha_actual ef088d357da72ea44079bccfa643a4a76fc86fb87db3305566cff5e2b9233c76
precision_bits 384
```

A checkpoint carrying a different hash is refused:

```text
mismatched_params ValueError checkpoint schema/parameters do not match this run
```

The byte-binding test was also run against a temporary one-byte-mutated copy of
the checker while reusing an original checkpoint:

```text
mutated_checker_sha 4b9a7a8aac262fe85801b5d8db335aec95f911535725dcaa3f74cf58f5c70807
mismatched_checker_exit 1
mismatched_checker_last_stderr ValueError: checkpoint schema/parameters do not match this run
```

Thus the implementation label alone is no longer the trust boundary; the
current checker bytes are in the v3 params and a changed checker cannot resume
an old checkpoint.

## 3. Exact prior forged-checkpoint fixture

I reran the four nonzero overlapping boxes from the first referee report (the
boxes directly certify winding 1 but are not checker output). Structural v3
loading accepts their shape, then PASS recomputation rejects them:

```text
prior_fixture_direct_winding 1
v3_structural_load [0, 1, 2, 3] 4
prior_fixture_recompute ValueError checkpoint PASS leaf 0:[] did not recompute to PASS
prior_fixture_cli_exit 1
prior_fixture_cli_last_stderr ValueError: checkpoint PASS leaf 0:[] did not recompute to PASS
prior_fixture_output_exists False
```

This is the required adversarial distinction: the forged boxes can still fool
the winding helper if sent directly to it, but resume never forwards them.
The current pinned full-tail and recorded-receipt gates cannot freshly produce
PASS, so the fail-closed exception occurs before `ordered_records_and_boxes`
and before winding.

## 4. Every saved PASS segment and box is recomputed

`segment_from_initial_path` at `q8_schur_contour.py:587-600` discards saved
endpoints and boxes and reconstructs from the trusted initial contour arc and
binary path. `recompute_saved_pass_records` at lines 603-633 loops over every
saved record with status `PASS`, calls `arc_certificate` on that reconstructed
segment, rejects any fresh non-PASS result, and appends only the fresh record
with `checkpoint_pass_recomputed=True`. `main` invokes this for every resume
before setting `unresolved`, computing ordered boxes, or calling winding
(`q8_schur_contour.py:778-808`).

A call-counted independent harness replaced `arc_certificate` with a fresh
PASS producer and supplied four records whose saved boxes were unrelated. All
four records were visited; the fresh boxes, not saved boxes, reached the
winding helper:

```text
recompute_call_count 4 [(2, 0, ()), (2, 1, ()), (2, 2, ()), (2, 3, ())]
recomputed_markers [True, True, True, True]
refreshed_boxes_winding 0
```

The prior forged input winding was 1. No saved PASS box can therefore alter
the winding field without first passing a fresh current-checker certificate.
Structural partition/duplicate/type checks remain at lines 636-696, and
`ordered_records_and_boxes` consumes only the post-recompute records at lines
699-714.

## 5. Remaining bypass scan

No load-bearing checkpoint bypass was found:

* v1/v2 schema values fail exact v3 schema comparison.
* A changed checker, precision, run range, pin, factor list, receipt hash, or
  dependency source hash changes the exact params and refuses resume.
* Saved PASS endpoints, `arc_index`, gate maps, dimensions, and boxes are not
  trusted; only validated initial/path coordinates are used to recompute.
* Saved `OPEN_MAX_DEPTH` records are never recomputed as PASS and keep
  `all_pass` false, so they cannot reach winding.
* Missing, duplicate, malformed, out-of-shard, or non-partitioning leaves are
  rejected before resume.

Two metadata/contract observations are non-load-bearing and do not change the
verdict:

1. `validate_checkpoint_records` does not enforce `len(path) <= params["max_depth"]`.
   A deliberately deeper OPEN partition is accepted structurally, but the
   resulting resume remains `OPEN`/exit 2 and cannot produce winding; any PASS
   path is still recomputed from the current checker. This is a resource and
   declared-depth consistency issue, not a forged-certificate bypass.
2. The result payload literal remains `q8-schur-contour/v2` at line 814 while
   the checkpoint schema is v3. This is a version-label inconsistency, not a
   path around the recomputation or hard-open gates.

## 6. Tail and bounded runtime receipts

The repaired code retains the prior conservative gates: `input_tail_only` is
diagnostic, `output_projection_tail=None`, `full_tau=None`, and
`full_tail_certified=False`. The corrected adverse receipt comparison remains
false for the pinned rows. Fresh bounded runs stayed closed:

```text
N2_exit=2
N2_status OPEN
N2_tail_formula_checks_pass False
N2_full_tail_certified False
N2_full_tau None
N2_checkpoint_resume {'used': False, 'saved_pass_records_recomputed': 0}
N2_first_status OPEN_MAX_DEPTH

N4_exit=2
N4_status OPEN
N4_tail_formula_checks_pass False
N4_full_tail_certified False
N4_full_tau None
N4_checkpoint_resume {'used': False, 'saved_pass_records_recomputed': 0}
N4_first_status OPEN_MAX_DEPTH
```

No N=104 run or theorem-grade contour result is claimed. The first remaining
mathematical gap is a certified omitted-output-row/projection tail combined
with the input-column tail in one compatible Hardy/Hilbert/trace norm.

## 7. Tests, compile, and review gates

```text
$ PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python -m unittest -v test_q8_schur_contour_repair.py
Ran 9 tests in 0.047s
OK

$ PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python -m py_compile \
    q8_schur_contour.py q8_r3b_engine.py q8_contour_helpers.py \
    f8_source_builder.py f8_certify_tb_blocks.py test_q8_schur_contour_repair.py
py_compile_exit=0

$ git diff --check 788a486c^..788a486c
candidate_diff_check_exit=0
```

The nine tests include the endpoint enclosure, F1024 hash/geometry tamper
check, adverse comparison, missing-output gate, partition/v1 refusal, v3
checker-byte binding, and forged-winding recomputation regression.

## 8. Report diff and security receipt

The staged change was restricted to this report, with no whitespace errors:

```text
$ git diff --cached --name-status
A research_notes/rh_goals_2026-08-14/lane_f/Q8_SCHUR_CONTINUOUS_CONTOUR_REPAIR_REREFEREE.md
$ git diff --cached --check
exit=0
```

Security lexical triage of the staged report found no introduced risk:

```text
{"mode":"lexical-triage","risk":"NONE","summary":"230 added line(s) across 1 file(s); 0 finding(s) — risk = NONE","findings":[]}
```

This is a diff triage receipt, not a proof about the unchanged checker.

## 9. Handoff

Verdict: **CONFIRMED at bounded implementation scope**. Omitted-output,
Fredholm, E1, MMS/Hilbert, `K_s`, continuation/Selberg, and q=8 theorem/LAW
claims remain `OPEN`.

The rereferee report is the only intended new file. No candidate or first
referee file was changed, and no push was performed.

**READY FOR JUDGING.**
