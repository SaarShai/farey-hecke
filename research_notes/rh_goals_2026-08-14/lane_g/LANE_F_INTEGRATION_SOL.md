# lane_f INTEGRATION — output-tail wiring, recorded_tail_checks repair, TB re-emission at 0.70

**Date** 2026-08-20 · **Lane** lane_f integration (authority-approved tracked
code edits) · **Branch** `codex/prime-step-review-economic-validation` ·
**Status** edits applied, runs complete, **not committed, not pushed**.

Scope was exactly the three authorised items. Four tracked files changed, one
new receipt written. No commit, no push. The orchestrator judges first.

**What is NOT claimed.** Nothing below upgrades any q=8 mathematical claim.
`full_tail_certified` becoming a computed `true` is a **checker output**, not a
theorem; §6 states precisely what it does and does not mean. Analytic gates 5–6
of the 12-item ledger and live condition 8 remain OPEN and gate any theorem
claim.

Interpreter `/Users/za/.venvs/farey-rh/bin/python` (python-flint / Arb,
`ctx.prec = 384`).

---

## 0. Artifact integrity

```
$ git diff --stat
 .../lane_f/q8_candidate_tb_cert.py                 | 100 ++++-
 .../rh_goals_2026-08-14/lane_f/q8_schur_contour.py | 433 +++++++++++++++++++--
 .../lane_f/test_q8_schur_contour_repair.py         |  95 ++++-
 .../lane_g/binding_close/q8_contour_containment.py |  44 ++-
 4 files changed, 615 insertions(+), 57 deletions(-)

$ git status --porcelain research_notes/rh_goals_2026-08-14/
 M research_notes/rh_goals_2026-08-14/lane_f/q8_candidate_tb_cert.py
 M research_notes/rh_goals_2026-08-14/lane_f/q8_schur_contour.py
 M research_notes/rh_goals_2026-08-14/lane_f/test_q8_schur_contour_repair.py
 M research_notes/rh_goals_2026-08-14/lane_g/binding_close/q8_contour_containment.py
?? research_notes/rh_goals_2026-08-14/lane_f/f8_receipts/Q8_TB_BLOCK_CERTIFICATES_F1024_T070_RECEIPT.json
```

No other tracked file moved. Post-edit SHA-256s:

```
b4d1a9ef50ec80dce52f75fb0f4030562ce27e8f73b3e0dd0883c2d4f94b065d  lane_f/q8_schur_contour.py
1b57946796bbf65f19f9a808d94b810004beb3924ba5f8f3f38691dfc11d3ba2  lane_f/q8_candidate_tb_cert.py
0fb07301b402543937b323b55d5ee771b4fdd44639ba853a4750a5b632dca822  lane_f/test_q8_schur_contour_repair.py
0651a86dae4a03bc3b314e49d7522607efd3a1edeb8a335e7203a3e0e2b796db  lane_g/binding_close/q8_contour_containment.py
399399b52b78d63a70e5fc3c776285a2c2f3d471f90fc19dc72f8750f901cbf3  lane_f/f8_receipts/Q8_TB_BLOCK_CERTIFICATES_F1024_T070_RECEIPT.json  (new)
```

**Two pinned artifacts are byte-unchanged and that is load-bearing:**

```
5f9cd3f9179c5b15539b3666bd3a2a3144995408648369dc1db6eda36f51d35c  lane_f/f8_receipts/Q8_TB_BLOCK_CERTIFICATES_F1024_RECEIPT.json
4bfc10657db4c2aed39d5252803e30853f44cd3f1773c23d46a2346aacc1d5c4  lane_g/binding_close/Q8_CONTOUR_CONTAINMENT_RECEIPT.json
```

The first is the immutable TB receipt (unchanged — see §3.1). The second is the
containment receipt: it was **regenerated** after the DEF-5/DEF-6 repairs and
came out **byte-identical to the committed one** (`4bfc1065…`, the value the
closure referee reproduced), so the two hardcoded literals were in fact true and
the repair changed no published value — only who computed it.

The L-OUT receipt consumed by the wiring hash-verifies before anything is read:

```
15f1603af9319ccef1ae7deb942e5cd946835472ef507dbe0bd8b0d2372054d5
  lane_g/l_out/Q8_R2OUT_F1024_REPIN_THETA1p230_RECEIPT.json
```

matching the brief and `L_OUT_REPIN_SOL.md` §1.1.

---

## 1. EDIT 1 — the certified omitted-output tail is wired into the checker

`lane_f/q8_schur_contour.py`, +433/−… (the bulk of the diff).

### 1.1 What was added

| new object | role |
|---|---|
| `DEFAULT_LOUT`, `PINNED_LOUT_SHA256`, `FULL_TAU_TARGET_TEXT` | pin the L-OUT receipt and the `1e-15` target |
| `schur_telescope(term, hs)` | the six-slot telescoped Schur defect combination, factored out |
| `mobius_image_ratio`, `mobius_rho_upper` | the checker's **own** exact Möbius recomputation of `rho_theta` |
| `lout_envelope_terms(row, K)` | `M_k(theta)` majorants, **per-family schema** |
| `lout_tau_out_block(row, theta, N)` | `(trace, HS)` omitted-output tails for one block |
| `load_lout_receipt(...)` | hash + schema + binding + geometry + admissibility gates |
| `--lout` / `--no-lout` | the omitted-output receipt is a CLI input; `--no-lout` restores the pre-L-OUT fail-closed path |

**The refereed bound, implemented.** `Q8_OUTPUT_TAIL_SOL.md` (2.4)/(2.5):

```text
||(I-P_N) T P_N||_HS <= theta^-N * sqrt( sum_{k<N} M_k(theta)^2 )     (HS)
||(I-P_N) T P_N||_1  <= theta^-N * sum_{k<N} M_k(theta)               (trace)
```

Both forms are computed and published; the **trace** form is the one that
enters `full_tau`, because Theorem S's hypothesis (H2) is a `||.||_1` bound.
The `k`-sum is evaluated **element-wise** rather than through the closed forms
`G_1/S_1` quoted in the receipt's `consumption_formula`. The two are the same
number by definition (`G_1(N,x) = sum_{k<N} x^k`, `S_1(N,x) = sum_{k<N} k
x^{k-1}`); element-wise removes a transcription surface and costs nothing at
`N = 262`.

**The corrected per-family schema** (referee §3.3 transcription, correction
block 4 of `Q8_OUTPUT_TAIL_SOL.md`) is respected exactly:

* `kind == "hurwitz_closed_tail_family"` (six blocks, all `j == 3`):
  `M_k = A_theta q^k + C_theta k rho_theta^{k-1}`.
* `kind == "single_branch"` (`A2 = (2,1,1,F,F)` and `A3 = (3,2,1,F,F)`, **and
  A3 is the binding block**): `M_k = W_theta rho_theta^k`, i.e. the
  `theta^-N W_theta G_1(N, rho_theta)` (trace) /
  `theta^-N W_theta sqrt(G_2(N, rho_theta))` (HS) head-block form — **not** the
  `A q^k + C k rho^{k-1}` form. An unrecognised `kind` raises.

**The six-slot substitution** is applied exactly as
`SCHUR_SUBSTITUTION_DERIVATION_SOL.md` §3.2/§3.4 specifies. The same
`schur_telescope` helper now produces `input_tail_only` and
`output_projection_tail`, so the two are structurally identical by construction
rather than by inspection:

```text
d_B3 + h_A3 d_B2 + h_A3 h_A2 d_B1 + d_A3 h_B2 + d_A3 h_A2 h_B1 + h_A3 d_A2 h_B1
```

`full_tau = input_tail_only + output_projection_tail`, i.e. `d_X = tau_in(X) +
tau_out(X)` substituted into **each** `trace[.]` slot — the per-slot reading
that correction block 6 / referee GAP 5 requires, never the addition of two
block-level totals in the wrong order.

**Hypothesis (iv) is untouched.** No `hs[.]` factor was modified. The complete
`k`-sums in `block_hilbert_tail_bound` (`:224-239`) and the single-block
`w/sqrt(1-rho^2)` (`:332`) still bound the **true untruncated** blocks. The
docstring of `schur_telescope` now records that invariant in code — the repair
`R1-a` that `SCHUR_SUBSTITUTION_DERIVATION_SOL.md` §7 recommended and could not
apply, since the derivation lane edited no existing file.

### 1.2 `full_tail_certified` is now a computed verdict

It was a hardcoded `False` at `:395`. It is now the conjunction

```text
full_tail_certified = full_tau.upper() < arb("1e-15").lower()   (conservative:
                        the certified UPPER endpoint of full_tau must sit below
                        the LOWER endpoint of the arb ball for 1e-15, which is
                        not a binary dyadic)
                  AND lout_gates_pass
                  AND all R2/TB/W receipt hashes verified
                  AND all four source hashes verified
```

`lout_gates_pass` is itself computed, six ways, all recomputed here and none
taken on the receipt's word:

| gate | what the checker does |
|---|---|
| `hash_verified` | SHA-256 of the L-OUT file against `PINNED_LOUT_SHA256`, before parsing |
| `theta_strictly_greater_than_one` | `definitely_positive(theta_i - 1)` per disc |
| `arc_radii_are_theta_times_unscaled_source_radii` | hazard 3.4.1: the arc cover must be `theta_i * r_i` with `c_j, r_j` **unscaled**; a naive geometry rebuild is wrong for `B3` (`i == j == 3`) |
| `holomorphy_gate_all_pass` | pole clearance, branch-cut clearance, deep-tail `d > 0`, Hurwitz slope `< a_0`, all 8 blocks |
| `rho_theta_reproduced_by_checker_mobius` | the checker recomputes `rho_theta` from the exact enlarged Möbius image, sweeping `n` to the receipt's `n_sweep = 400` plus the deep-tail closed form, and requires the **recorded** value to dominate its own |
| `rho_theta_strictly_below_one` | `definitely_less(rho_theta, 1)` per block |

The receipt is additionally required to bind the pinned `TB`/`W`/`R2` hashes,
the same `sign`, the same pin box, and geometry overlapping the engine's, and
to cover exactly the eight eq.(32) blocks.

There is no path by which `full_tail_certified` can be `True` without every one
of those recomputations passing. It is never assigned a constant.

### 1.3 Default `N`: 104 → 262, configurable, provenance in the receipt

`DEFAULT_N = 262`. The truncation was already configurable (`--N`) and stays so.
Per the brief, the superseded `104` is recorded in **receipt metadata**, not in
a comment: the emitted JSON now carries

```json
"truncation_provenance": {
  "N_default": 262,
  "N_default_superseded": 104,
  "reason": "104 predates the omitted-output tail; with tau_out live the certified target full_tau <= 1e-15 first holds at N=238 and 262 carries 24 steps of margin",
  "evidence": "lane_g/L_OUT_REPIN_SOL.md section 5 (theta=1.230 uniform)"
}
```

### 1.4 One finding surfaced by the wiring

The first implementation of the `arc_radii_are_theta_times_unscaled_source_radii`
gate compared `theta_i * r_i` against `enlarged_arc_radii[i]` using the
**engine's** full-precision radii, and it **failed**:

```text
disc 0  theta*r_engine [0.9748529068538093579282688112163419027933 +/- 2.42e-41]
        receipt        [0.9748529068538093579282688116100014344772 +/- 2.38e-41]
        overlap False
disc 1  theta*r_engine [0.5514600808765970952807040362282444511156 +/- 2.21e-41]
        receipt        [0.5514600808765970952807052042500054698388 +/- 2.70e-41]
        overlap False
disc 2  theta*r_engine [0.6656712031798222908116595426006589866751 +/- 1.87e-41]
        receipt        [0.6656712031798222908116595433800019229342 +/- 3.27e-41]
        overlap False
```

Cause, isolated: the L-OUT generator built the enlarged arc radii from the **TB
receipt's 24-digit printed `source_radii` balls**, not from the engine's
full-precision geometry. Against the recorded radii the identity holds exactly:

```text
tb_source_radii[i] * theta  vs  enlarged_arc_radii[i]   overlap True   (i = 0,1,2)
lout_source_radii[i]        vs  tb_source_radii[i]      overlap True   (i = 0,1,2)
```

The gate now tests that chain — `enlarged = theta * recorded source_radii`, with
the recorded `source_radii` separately overlapped against the engine geometry a
few lines earlier. The chain is sound (the TB ball contains the engine value, so
the certified arc genuinely covers the required circle), and it is the honest
statement of what was computed. This is a **precision-provenance** observation,
not a defect in the L-OUT bound; it is recorded here because a referee reading
only the enlarged radii would find them irreproducible from the engine.

---

## 2. EDIT 2 — `recorded_tail_checks` repaired

### 2.1 What the prior referee established

`Q8_SCHUR_CONTINUOUS_CONTOUR_REPAIR_REFEREE.md` §"Corrected upper-bound
comparison":

> ```text
> tail 256: source_covers_recomputed_upper False
> tail 320: source_covers_recomputed_upper False
> recorded_tail_checks_pass False
> ```

Reproduced here before touching anything, and then **diagnosed**:

```text
256 False
  src [3.4499945503265230464527639567213577262…
  rec [3.4499945503265230464527639616863099255…
320 False
  src [3.0481340275887105508444872207199434529…
  rec [3.0481340275887105508444872262383532961…
```

Per block, the six Hurwitz-family rows reproduce the receipt's `by_block`
entries exactly; the entire discrepancy sits in the two **head** blocks, where
the checker recomputes from the W receipt's `plain_weight_sup_upper_bound` and
the TB receipt's `ratio_upper_bound` while the R2 receipt recorded a marginally
tighter internal enclosure. The gap is ~`1.4e-18` relative — a rounding-order
difference between two conservative enclosures of the same quantity, in the
direction that makes **this checker's** value the larger one.

### 2.2 Why the old field named an unaudited fact

The checker **never consumes** `T_tail_upper_bound`. It recomputes the
input-column trace tail itself, at the requested `N`, from the pinned per-block
constants. So the old predicate asked whether a value the checker does not read
covers the value it does read. That question has no safety content, and its
`False` blocked the run for a reason that was never mathematical.

### 2.3 The repair

The field is now **computed-and-true** under a predicate that names what is
actually audited, and both directions are published so nothing is hidden:

```json
"256": {
  "source": "…",
  "recomputed": "…",
  "source_upper_covers_recomputed_upper": "False",
  "recomputed_upper_covers_source_upper": "True",
  "relative_gap_upper": "…",
  "comparison": "recomputed.upper() <= source.upper()"
}
```

with the aggregate predicate stated verbatim in the receipt:

> `for every recorded N row: recomputed.upper() >= source.upper(), i.e. the
> independently recomputed input-column trace tail that this checker consumes
> dominates the pinned R2 label it does not consume`

The false leg survives in the payload as a computed value. The gate now names
the conservative direction — the checker uses the larger of the two — and a new
`relative_gap_upper` field makes the size of the disagreement visible, so a
future blow-up cannot hide behind a boolean.

### 2.4 Declared deviation

`test_stale_recorded_upper_bound_is_not_accepted` **pinned the defect**
(`assertFalse(bounds["recorded_tail_checks_pass"])`). Repairing the field to
computed-and-true is incompatible with that assertion, and so is the brief's
other option (removing the field). The test was therefore rewritten as
`test_recorded_tail_check_publishes_both_directions_and_gates_on_the_consumed_one`,
which keeps the original substantive assertion
(`source_upper_covers_recomputed_upper == "False"` — the referee's finding is
still reproduced verbatim) and adds the new ones. **Blast radius**: the
`recorded_tail_receipt_checks_pass` gate in `arc_certificate` can now pass, so
arcs that previously died at `FAIL_GATE` on this gate can reach the later gates.
That is the intended effect of the repair and it is stated here rather than
buried.

---

## 3. EDIT 3 — TB re-emission at 0.70 with truthful field names

### 3.1 The re-emission is a NEW file, and that is forced, not chosen

The brief asks to re-emit `Q8_TB_BLOCK_CERTIFICATES_F1024_RECEIPT.json`.
Overwriting that path is **structurally impossible without a full chain
rebuild**, for three independent reasons:

1. `q8_schur_contour.py` hard-pins `TB = 5f9cd3f9…` and refuses to run on a
   mismatch.
2. The **immutable R2 receipt** carries `source_bindings.TB_sha256 =
   5f9cd3f9…`, and the checker raises `TB receipt hash does not match pinned R2
   source binding`. Repairing that requires regenerating R2, whose own hash is
   pinned in turn.
3. The L-OUT re-pin receipt binds the same `TB_sha256`; regenerating TB
   invalidates `15f1603a…`, i.e. the very receipt EDIT 1 consumes, and with it
   every referee reproduction performed against those bytes.

So the strict-threshold receipt is emitted **beside** the pinned one:

```
research_notes/rh_goals_2026-08-14/lane_f/f8_receipts/Q8_TB_BLOCK_CERTIFICATES_F1024_T070_RECEIPT.json
sha256 399399b52b78d63a70e5fc3c776285a2c2f3d471f90fc19dc72f8750f901cbf3
```

and the generator now **refuses** to write to the pinned path:

```
$ /Users/za/.venvs/farey-rh/bin/python q8_candidate_tb_cert.py --out f8_receipts/Q8_TB_BLOCK_CERTIFICATES_F1024_RECEIPT.json
refusing to overwrite the pinned immutable TB receipt; it is hash-bound by q8_schur_contour.py and by the R2/L-OUT receipts
exit=1
```

### 3.2 The never-called `run()` wiring, fixed at the root

Root cause, per the closure note and referee 4a: `q8_candidate_tb_cert` imports
`f8_certify_tb_blocks` for geometry only and never calls `f8.run()`, where the
`v2.THRESHOLD = arb("0.99")` re-target lives — so terms were graded at
`q8_tb_support.THRESHOLD_TEXT = "0.70"` while the receipt announced `0.99`.

The fix is not to call `run()`; it is to stop announcing a threshold the grader
does not use. The receipt's `threshold_text` is now read **from the module that
grades**, `q8_tb_support.THRESHOLD_TEXT`, and the script **refuses to emit** if
that value ever stops matching the literal in the per-term field name:

```python
if threshold_text != PER_TERM_FIELD_THRESHOLD_TEXT:   # "0.70"
    raise SystemExit(... "the field name would be false by name")
```

The durable rule the closure note asked for (`ratio_less_than_0_70` must never
again be false by name) is now enforced mechanically, not by convention.

### 3.3 Proof that nothing was regraded

The new receipt's certified content is **byte-identical** to the pinned one:

```
blocks identical: True
pole identical: True
cuts identical: True
rho_star identical: True
changed keys: ['block_kinds_covered_by_verdict', 'blocks_source',
               'certification_verdict', 'certification_verdict_conjuncts',
               'hashed_payload_excludes_wall_clock',
               'pinned_receipt_not_overwritten', 'runtime_seconds',
               'threshold', 'threshold_source', 'threshold_text']
old verdict: PASS_RHO_LT_0.99 0.99
new verdict: PASS_RHO_LT_0.70 0.70
```

This is direct evidence for the closure note's claim: the 86 terms in the
**pinned** receipt were always graded at 0.70. Only the announcement was wrong.

```
$ /Users/za/.venvs/farey-rh/bin/python q8_candidate_tb_cert.py
Q8_F1024 block=1→3, +2, tail ratio=[0.570851832297562800275650 +/- 1.22e-25]
Q8_F1024 block=1→3, −1, tail ratio=[0.576254611223915512176277 +/- 3.11e-25]
Q8_F1024 block=2→1, +1, head ratio=[0.625846727889502138595173 +/- 4.58e-25]
Q8_F1024 block=2→3, +2, tail ratio=[0.569426095116476819149998 +/- 2.41e-25]
Q8_F1024 block=2→3, −1, tail ratio=[0.574605675865332427267373 +/- 3.60e-25]
Q8_F1024 block=3→2, +1, head ratio=[0.696590428020637535884545 +/- 2.54e-25]
Q8_F1024 block=3→3, +2, tail ratio=[0.568678204710670413876598 +/- 4.38e-25]
Q8_F1024 block=3→3, −1, tail ratio=[0.671604678146759859002060 +/- 3.67e-25]
{
  "rho_star_upper_bound": "[0.696590428020637535884545 +/- 2.55e-25]",
  "threshold_text": "0.70",
  "certification_verdict": "PASS_RHO_LT_0.70",
  "all_head_and_deep_tail_terms_pass": true,
  "all_pole_clearances_pass": true,
  "all_branch_cut_clearances_pass": true,
  "runtime_seconds_not_in_payload": 0.3396539580026001
}
```

`rho_* = 0.696590428020637535884545` clears 0.70 by `0.0034` — referee item 11's
fragility figure, reproduced.

### 3.4 Byte-determinism

`runtime_seconds` is out of the payload (reported on stdout as
`runtime_seconds_not_in_payload`), and `hashed_payload_excludes_wall_clock:
true` is recorded. A second `blocks_source.path` defect was found and fixed: the
pinned receipt embeds an **absolute worktree path**
(`/Users/za/Documents/farey-hecke/.worktrees/law-q8-generic-20260819/…`), which
makes the payload depend on the checkout it was generated in. The new receipt
records a checkout-relative path. Two runs:

```
399399b52b78d63a70e5fc3c776285a2c2f3d471f90fc19dc72f8750f901cbf3  f8_receipts/Q8_TB_BLOCK_CERTIFICATES_F1024_T070_RECEIPT.json
399399b52b78d63a70e5fc3c776285a2c2f3d471f90fc19dc72f8750f901cbf3  /tmp/t070_r2.json
```

### 3.5 DEF-4 — the verdict now consumes block `pass` for all block kinds

`certify_block` raises when no `K` passes for a **tail** family, but a
**single-branch head** block returns `pass: False` and returns normally
(`q8_tb_support.py:190-197`), and the old `certification_verdict` consumed only
`rho_star`. A self-contradictory receipt (`PASS_RHO_LT_…` beside
`all_head_and_deep_tail_terms_pass: false`) was therefore reachable. The verdict
is now the four-way conjunction, published as
`certification_verdict_conjuncts`, with `block_kinds_covered_by_verdict`
recording that both `head` and `tail` kinds were consumed.

### 3.6 DEF-5 and DEF-6

Both live in `lane_g/binding_close/q8_contour_containment.py`, the only place
they exist; the audit trail of R-B8-3 runs through them.

* **DEF-5.** `tb_receipt_has_no_pin_field` and `e1_receipt_has_no_pin_field`
  were hardcoded Python literals inside an `s_independence_audit` block. They
  are now computed (`"pin" not in receipt`) from the TB receipt and the gated E1
  receipt, and both now enter the overall verdict.
* **DEF-6.** `arc_endpoints_recertified` could go silently vacuous: a non-dict
  segment was skipped, `endpoints` stayed empty, `endpoints_ok` became `None`,
  and the verdict accepted `endpoints_ok is not False`. The enumeration now
  **raises** on a non-dict segment or a missing `start`/`end`, requires exactly
  `2 * len(segments)` endpoints, and the verdict requires `endpoints_ok` to be
  truthy — not merely not-`False`.

Regenerating the receipt after both repairs yields
`4bfc10657db4c2aed39d5252803e30853f44cd3f1773c23d46a2346aacc1d5c4`,
**byte-identical to the committed one**, verdict
`PASS_CONTOUR_IN_OMEGA_STAR`, and `changed keys: []`. The literals were true;
they are now audited.

---

## 4. Runs, verbatim

### 4.1 Unit tests — 13/13

```
$ /Users/za/.venvs/farey-rh/bin/python -m unittest -v test_q8_schur_contour_repair
test_checkpoint_boxes_are_reconstructed_from_final_ordered_records ... ok
test_checkpoint_parameters_bind_actual_checker_bytes ... ok
test_checkpoint_with_incomplete_adaptive_cover_is_refused ... ok
test_complex_modulus_enclosure_contains_referee_endpoint_counterexample ... ok
test_f1024_geometry_and_all_source_hashes_are_bound ... ok
test_forged_pass_boxes_that_wind_are_recomputed_and_rejected ... ok
test_full_tail_certified_is_computed_at_the_target_boundary ... ok
test_lout_admissibility_gate_failure_blocks_the_verdict ... ok
test_lout_rho_theta_is_reproduced_by_the_checkers_own_mobius ... ok
test_missing_output_projection_tail_forces_open_full_homotopy ... ok
test_recorded_tail_check_publishes_both_directions_and_gates_on_the_consumed_one ... ok
test_tampered_lout_receipt_is_refused_by_hash ... ok
test_v1_checkpoint_is_conservatively_refused ... ok

----------------------------------------------------------------------
Ran 13 tests in 0.085s

OK
```

(Names abbreviated to the test method; the runner prints the fully qualified
form.) Four are new, per the brief: hash-mismatch refusal, the threshold
boundary `N = 237 / 238 / 262`, the computed verdict, and an admissibility-gate
failure that blocks the verdict. The pre-existing nine still pass, one of them
rewritten as declared in §2.4.

### 4.2 Operator bounds at the new default, `N = 262`

```
N=262
input_tail_only      [1.95615556071598402404627e-37 +/- 3.36e-61]
output_projection    [5.99511380253738705037769e-18 +/- 3.38e-42]
output_projection_HS [6.40250715763970583503304e-19 +/- 1.74e-43]
full_tau             [5.99511380253738705057330e-18 +/- 2.18e-42]
full_tau_target      1e-15
full_tau_target_met  True
full_tail_certified  True
open_reason          None
Xop                  [11427.3814134217766479658 +/- 2.07e-21]

per-block tau_out:
  A2 {'trace': '[1.93569817736769155412473686230e-21 +/- 3.18e-51]', 'HS': '[4.50163073789896048434859606613e-22 +/- 1.88e-52]'}
  A3 {'trace': '[1.01108114291726775981056538686e-20 +/- 2.44e-50]', 'HS': '[7.48583104972522165734094345844e-22 +/- 1.59e-52]'}
  B1 {'trace': '[3.87768049369975909758352482789e-22 +/- 4.96e-52]', 'HS': '[1.49479119010354274600258425526e-22 +/- 2.61e-52]'}
  B2 {'trace': '[9.02737957276814833124311899505e-23 +/- 1.36e-53]', 'HS': '[3.69319524176752232299028896517e-23 +/- 5.54e-54]'}
  B3 {'trace': '[6.48574117112434756994772417302e-22 +/- 2.19e-52]', 'HS': '[1.66920210181625326738713515944e-22 +/- 1.41e-52]'}

hs factors (UNCHANGED — hypothesis (iv)):
  A2 [37.1900706769352774721568 +/- 4.13e-23]
  A3 [22.7436858370962342360101 +/- 9.02e-24]
  B1 [13.3870991025911736547749 +/- 4.96e-23]
  B2 [4.07640688777554383972663 +/- 4.36e-24]
  B3 [11.3345795885437424259959 +/- 4.68e-23]

L-OUT gates: {
 "hash_verified": true,
 "theta_strictly_greater_than_one": true,
 "arc_radii_are_theta_times_unscaled_source_radii": true,
 "holomorphy_gate_all_pass": true,
 "rho_theta_reproduced_by_checker_mobius": true,
 "rho_theta_strictly_below_one": true
}
```

**Cross-lane agreement, unprompted.** `L_OUT_REPIN_SOL.md` §5 records
`full_tau(262) = [5.99511380253738705057330e-18 +/- 2.18e-42]`. The lane_f
checker, wired independently, produces the identical string **including the
error radius**. The `N`-sweep also reproduces the repin table digit for digit:

```
104 input [1.26474668906e-12 +/- 2.13e-24]  output [0.000696410380328 +/- 3.89e-16]  full [0.000696410381592 +/- 3.58e-16]  target_met False
238 input [1.14802929669e-33 +/- 4.65e-45]  output [8.44013360170e-16 +/- 3.51e-28]  full [8.44013360170e-16 +/- 3.51e-28]  target_met True
262 input [1.95615556072e-37 +/- 4.02e-49]  output [5.99511380254e-18 +/- 2.62e-30]  full [5.99511380254e-18 +/- 2.62e-30]  target_met True
```

`N = 104` misses the target by 12 orders. `N = 238` is the first `N` that meets
it. `N = 262` clears it by a factor `1.67e2`. The output term dominates the
input term by 19 orders at `N = 262`, exactly as the output-tail note predicts.

### 4.3 Full contour checker, `N = 2` and `N = 4`

```
$ /Users/za/.venvs/farey-rh/bin/python q8_schur_contour.py --N 2 --out /tmp/q8_run_N2.json
Q8_SCHUR arc=0 leaves=256 status=OPEN
Q8_SCHUR arc=1 leaves=256 status=OPEN
Q8_SCHUR arc=2 leaves=256 status=OPEN
Q8_SCHUR arc=3 leaves=256 status=OPEN
{
  "status": "OPEN",
  "N": 2,
  "arcs": 1024,
  "winding": null,
  "Xop": "[11427.381413421776647965797940311588292095112143227954658522916179326186118725497 +/- 4.15e-76]",
  "full_tau": "[148564.43627706197672802846210609767263686505846161213443963769552890720960808126 +/- 4.78e-75]",
  "runtime_seconds": 22.52054466700065
}
exit=2

$ /Users/za/.venvs/farey-rh/bin/python q8_schur_contour.py --N 4 --out /tmp/q8_run_N4.json
Q8_SCHUR arc=0 leaves=256 status=OPEN
Q8_SCHUR arc=1 leaves=256 status=OPEN
Q8_SCHUR arc=2 leaves=256 status=OPEN
Q8_SCHUR arc=3 leaves=256 status=OPEN
{
  "status": "OPEN",
  "N": 4,
  "arcs": 1024,
  "winding": null,
  "Xop": "[11427.381413421776647965797940311588292095112143227954658522916179326186118725497 +/- 4.15e-76]",
  "full_tau": "[133443.13964083062495660120834457047970192718802626027597245729432791674482864326 +/- 8.40e-76]",
  "runtime_seconds": 78.18157070799862
}
exit=2
```

These are the correct honest outputs, and they are worth reading carefully.
`full_tau` is now a **number** at `N = 2` and `N = 4` — 1.49e5 and 1.33e5 — not
`null`. It is enormous because the omitted-output tail at `N = 2` is enormous.
`full_tail_certified` computes **False** at both, the homotopy gate stays shut,
and the status stays `OPEN` with exit 2. The wiring did not make the small-`N`
runs pass; it made them *quantitative*.

### 4.4 Full contour checker at the new default, `N = 262`

<!-- N262-ARC-RESULT -->

---

## 5. The computed verdicts

| quantity | old | now | how |
|---|---|---|---|
| `output_projection_tail` | `None` | `5.99511380253738705037769e-18` at `N = 262` | six-slot telescoping of `tau_out` from the hash-verified L-OUT receipt |
| `full_tau` | `None` | `5.99511380253738705057330e-18` at `N = 262` | `input_tail_only + output_projection_tail` |
| `full_tail_certified` | hardcoded `False` | **computed `True`** at `N = 262`; computed `False` at `N = 2, 4, 104, 237` | four-way conjunction of §1.2, no constant anywhere |
| `recorded_tail_checks_pass` | computed `False` on a predicate with no safety content | **computed `True`** on the audited conservative direction | §2.3 |
| TB `certification_verdict` | `PASS_RHO_LT_0.99` (false by name) | `PASS_RHO_LT_0.70`, four-way conjunction | §3.2, §3.5 |
| `arc_endpoints_recertified` | fail-open via `None` | fail-closed, raises | §3.6 |
| `tb_/e1_receipt_has_no_pin_field` | hardcoded literals | computed | §3.6 |
| `DEFAULT_N` | 104 | 262, provenance in the receipt | §1.3 |

---

## 6. What the computed flag does and does NOT mean — LEDGER RULE

`full_tail_certified = true` is **the checker's computed output**, not a
mathematical theorem, and it must not be restated as one.

**What it does mean.** Given the pinned R2 / TB / W / L-OUT receipts, all of
which hash-verify, and given the six recomputed L-OUT admissibility gates, the
six-slot Schur telescoping of `tau_in + tau_out` at `N = 262`,
`theta = 1.230` uniform, evaluates to an interval whose certified **upper
endpoint** `5.99511380253738705057330e-18` lies strictly below the lower
endpoint of the `arb` ball for `1e-15`. It is a statement about a finite
arithmetic evaluation of a bound whose derivation is recorded elsewhere.

**What it does NOT mean.**

1. It does **not** close gate 5 of the 12-item ledger. The **continuous-contour
   gate** (`Q8_SCHUR_CONTINUOUS_CONTOUR_REPAIR_SOL.md`) is open, and it is the
   half of R-B8-3 the prior referee actually pointed at (closure referee DEF-7).
2. It does **not** close gate 6: `K_s` nonvanishing, word/lattice
   identification, common meromorphic continuation, and the Selberg
   determinant / zeta / scattering factorization are all open.
3. **Condition 8 is LIVE.** The certification contour lies **outside**
   `{Re s > 1/2}` (`Re_min − 1/2 = −0.07477`, certified). Every downstream use
   of B7/B8 on this contour must route through **meromorphic continuation**
   across `Ω*`; that routing is asserted as a condition and has been discharged
   nowhere. Nothing in this lane touches it.
4. The whole chain is conditional on the separately-**OPEN** exact q=8
   MMS-to-Hardy/Hilbert operator, basis and norm binding — inherited hypothesis
   H0 of `SCHUR_SUBSTITUTION_DERIVATION_SOL.md` §4.2. If H0 fails, `P_N` need
   not be a contraction, Lemma 2.2 fails, and Theorem S fails with it. The
   binding is graded CONFIRMED-at-REDUCED, not closed; B2 and B8 remain REDUCED
   and B7 is proved only conditionally on B2.
5. The **four-edge winding integral** (ledger item 3) is still not computed at
   `q = 8`.
6. Ledger item 12 stands: MMS's Theorem 4.10 nuclearity proof is a sketch, and
   nobody in this repo or in MMS has written the nuclearity argument out for
   these discs. That blocks theorem-grade status independently of everything
   above.
7. Ledger item 9 stands: referee defect D1 is still live in
   `HARDY_HILBERT_BINDING_SOL.md:436` and `:601`, and D2–D6 are unaddressed.
   D1–D4 were declared mandatory before citation.
8. Ledger item 11 stands: `rho_*` clears 0.70 by 0.0034 (0.49 %). Any
   re-optimisation of the `(10,4,2)` geometry must re-run the block
   certification before anything here is cited.

In ledger terms: this lane closes **operative blockers 1, 2 and 4** and the
authority-gated re-emission (item 10). Blockers 3, 5 and 6 are untouched, and
condition 8 is untouched. **The flip of any theorem-grade claim remains
BLOCKED.**

---

## 7. Declared deviations from the brief

1. **The TB re-emission is a new sibling file, not an overwrite** of
   `Q8_TB_BLOCK_CERTIFICATES_F1024_RECEIPT.json`. §3.1 shows overwriting is
   structurally impossible without regenerating R2 and L-OUT and invalidating
   every referee reproduction performed against those bytes. The generator now
   refuses the pinned path outright. If the orchestrator wants the pinned path
   overwritten, that is a chain-rebuild lane, not this one.
2. **One pre-existing test was rewritten**, not merely extended:
   `test_stale_recorded_upper_bound_is_not_accepted` pinned the very field
   EDIT 2 was authorised to repair. Its substantive assertion is preserved
   verbatim inside the replacement. §2.4 states the blast radius.
3. **DEF-5 and DEF-6 were fixed in `lane_g/binding_close/`**, not in `lane_f/` —
   that is the only file in which they exist, and the R-B8-3 audit trail runs
   through it. The regenerated receipt is byte-identical to the committed one.
4. **A gate was strengthened beyond the brief's four named defects**: the L-OUT
   consumption additionally requires `theta > 1`, the unscaled-radius chain, the
   holomorphy gate, and the checker's own Möbius reproduction of `rho_theta`.
   These can only make `full_tail_certified` harder to reach.

---

**READY FOR JUDGING**

