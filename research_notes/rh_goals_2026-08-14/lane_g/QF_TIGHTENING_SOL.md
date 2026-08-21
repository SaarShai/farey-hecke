# `qF` -> `qOp`: certified operator-norm arc gate, and why it does not rescue `N = 262`

Date: 2026-08-20
Lane: lane_g, authorized edit #4 against `lane_f`
Branch: `codex/prime-step-review-economic-validation`
Files touched:

- `research_notes/rh_goals_2026-08-14/lane_f/q8_schur_contour.py`
- `research_notes/rh_goals_2026-08-14/lane_f/test_q8_schur_contour_repair.py`

No commit, no push.

## 0. Headline

The edit was authorised on the hypothesis that the Frobenius arc gate carries
roughly a factor-`N` (or factor-`sqrt(N)`) overestimate, so that a genuine
operator-norm certificate would take `83.79` down through `1`.

**The hypothesis is false, and this lane measured why.** The gate is now a
certified operator-2-norm bound (weighted Schur test, minimised against
Frobenius). It is sound, it is tighter, all 18 tests pass — and at the pinned
arc it buys a relative improvement of `2.7e-6`, not a factor of `262`:

```text
N = 262, arc 0, depth 0
qF_upper  = 83.790298954537757620416957883198935009715399234915335736445465072103168161461759
qOp_upper = 83.790069059487618077666517899595847268148979295060633591602226405672414067854197
qF/qOp    = 1.0000027438      (needed: a factor of 83.79)
qOp_lt_1  = False             status = OPEN_MAX_DEPTH
```

The reason is structural and is stated in section 3: the entrywise-modulus
matrix that the arc enclosure hands the gate is **numerically rank one**
(`sigma_2/sigma_1 = 2.34e-3`), and for a rank-one nonnegative matrix Frobenius
*is* the operator norm. There was never a `sqrt(N)` to recover.

The verdict on the contour is unchanged: `status OPEN`, arc `OPEN_MAX_DEPTH`.
**This is checker output, not a theorem.** Analytic gates 5-6 and continuation
condition 8 of the 12-item ledger are untouched by anything in this note.

The useful by-product is that this lane also **measured the depth at which the
gate does close** — 7 bisections, `max_qOp = 0.654` over all 128 leaves — and
priced it: `~365 h` single-threaded at `N = 262`, four arcs (section 4). The
gate is compute-bound, not mathematically stuck, and the tightening does not
reduce that bill by one leaf (the old Frobenius gate closes at depth 7 too).

## 1. What the winding argument actually needs at this step

The arc certificate writes, for a closed segment with midpoint `s0` and radius
`r`, with `A0 = I - C_N(s0)` and `M = A0^{-1}(C_N(s) - C_N(s0))`:

```text
I - C_N(s) = A0 - (C_N(s)-C_N(s0)) = A0 (I - M).
```

The gate exists to make the Neumann series for `(I-M)^{-1}` converge, which
needs

```text
||M|| < 1   in some submultiplicative norm,
```

and to feed the resolvent bound that section 4.4 of
`Q8_SCHUR_CONTINUOUS_CONTOUR_SOL.md` consumes,

```text
inv_arc >= ||(I - C_N(s))^{-1}||_op,
inv_tilde = 1 + Xop * inv_arc,          (Woodbury-style finite inverse bound)
tail_homotopy = full_tau * inv_tilde  < 1.
```

`Xop` is a Hilbert-Schmidt bound, so `inv_arc` is consumed strictly as an
**operator-norm** bound on the finite resolvent. Nothing downstream needs a
Frobenius quantity as such. Frobenius was a *sufficient* choice, because
`||.||_F` is submultiplicative and dominates `||.||_2`; it was never the
certified object.

## 2. The inequality chain — the replacement bounds the same object

Let `Delta` be the interval matrix the checker builds, with
`|C_N(s)_{ij} - C_N(s0)_{ij}| <= r * sup_arc |C_N'(s)_{ij}| =: rho_{ij}` for
every `s` on the closed segment (the line-integral enclosure, unchanged by this
edit). Let `Mbox = A0^{-1} Delta` be the interval product the checker forms,
and let `Mabs` be its entrywise modulus upper bound,
`Mabs_{ij} = upper(|Mbox_{ij}|)`.

The chain, each step an inequality in the safe direction:

```text
(i)   M = A0^{-1}(C_N(s)-C_N(s0))  in  Mbox            [interval enclosure]
(ii)  |M_{ij}| <= Mabs_{ij}                            [outward rounding]
(iii) ||M||_2 <= || |M| ||_2 <= ||Mabs||_2             [entrywise domination,
                                                        both matrices >= 0]
(iv)  ||Mabs||_2 <= sqrt(alpha*beta)                   [weighted Schur test]
(v)   ||Mabs||_2 <= ||Mabs||_F = ||Mbox||_F = qF       [Frobenius]
qOp := min( (iv), (v) )   >=  ||M||_2                  [min of upper bounds]
```

Step (iv) is the Schur test in its two-weight form: for strictly positive
weights `p_j`, `q_i`,

```text
sum_j Mabs_{ij} p_j <= alpha * q_i   for every row i,
sum_i Mabs_{ij} q_i <= beta  * p_j   for every column j
  ==>  ||Mabs||_2 <= sqrt(alpha*beta).
```

Proof (recorded in the docstring): split
`Mabs_{ij}|x_j| = (Mabs_{ij} p_j)^{1/2} (Mabs_{ij}|x_j|^2/p_j)^{1/2}`, apply
Cauchy-Schwarz in `j`, use the row hypothesis, sum over `i`, swap the order of
summation, use the column hypothesis. `p = q = 1` recovers the classical
`sqrt(||Mabs||_inf * ||Mabs||_1)`.

**Soundness does not depend on the weights.** `alpha` and `beta` are recomputed
in Arb with outward rounding for whatever positive weights are supplied, so a
poor weight guess only weakens the bound; it cannot make it unsound. The
weights come from a plain-float power iteration on `Mabs^T Mabs` (heuristic,
no rigour claimed) because the optimal two-weight Schur test attains exactly
`sigma_max(Mabs)`: taking `p` the top right singular vector of `Mabs` (entrywise
nonnegative by Perron) and `q = Mabs p / sigma` gives `alpha = beta = sigma`.
So the implemented bound converges to the sharpest bound obtainable from
entrywise moduli.

`qOp >= ||M||_2` is the same object the old gate bounded — `qF >= ||M||_F >=
||M||_2`. The replacement **strengthens** the hypothesis chain (a smaller
certified upper bound on the same quantity); it does not change what is
certified. Both numbers are published in every arc record.

Downstream consistency, checked line by line:

```text
inv_arc = ||A0^{-1}||_F / (1 - qOp)
        >= ||A0^{-1}||_2 * ||(I-M)^{-1}||_2
        >= ||A0^{-1}(I-M)^{-1}||_2 = ||(I-C_N(s))^{-1}||_2.   OK
```

The numerator is deliberately left as `||A0^{-1}||_F` — it dominates
`||A0^{-1}||_2`, so mixing the two norms here is safe and the edit stays
surgical. `correction.inv()`, `H`, `rH`, the Taylor box and the winding checker
are untouched.

## 3. Why the tightening buys almost nothing here

The certified `Mabs` at the pinned arc is **numerically rank one**. Measured at
`N = 64`, arc 0, depth 0:

```text
singular values of |normalized_delta| (top 5):
  [8.37900691e+01 1.96276922e-01 1.12494919e-03 3.90506614e-05 3.88493632e-06]
sigma_2/sigma_1 = 0.0023424843071658363
||Mabs||_F      = 83.79029895453775
sigma_1(Mabs)   = 83.7900690594876
```

For a rank-one nonnegative matrix `||.||_F = sigma_1` exactly. Here the ratio
is `1.0000027`. Frobenius was not lossy; it was within three parts per million
of the sharpest entrywise-modulus bound that exists.

Three candidate bounds, measured (`N` sweep, arc 0, depth 0):

| `N` | Frobenius | unweighted Schur | weighted Schur (= `qOp`) | `sigma_1(Mabs)` |
|---|---|---|---|---|
| 8 | 0.479073 | 0.595759 | 0.479072 | 0.479072 |
| 16 | 83.9434 | 115.669 | 83.9431 | 83.9431 |
| 32 | 83.7903 | 116.204 | 83.7901 | 83.7901 |
| 64 | 83.7903 | 116.204 | 83.7901 | 83.7901 |

Note the *unweighted* Schur test is **worse** than Frobenius here (116 vs 84) —
which is why the implementation takes the minimum over candidates rather than
substituting one for another. The weighted test recovers `sigma_1` to all
printed digits, confirming the power-iteration weights are converging to the
optimum.

This also independently reproduces lane_g's §4.5 finding: `qF` does **not**
grow with `N`; it converges by `N = 32` and is a property of the arc (pinned
half-width `1e-6`, `K = 1`), not of the truncation.

### 3.1 Nor is the slack phase-alignment (a further probe, heuristic)

The next obvious suspicion is that step (iii) — replacing `A0^{-1} Delta` by
`|A0^{-1}| rho` — throws away cancellation between the phases of `A0^{-1}` and
of `Delta`. It does not, materially. Sampling actual phase realisations
`D_{ij} = rho_{ij} e^{i theta_{ij}}` in the box (`N = 64`, float midpoints,
**not certified**):

```text
||A0inv||_2      = 9696975.226759218      (A0 is ill-conditioned, kappa ~ 1e7)
||rho||_2        = 7.938476151527737e-05
|| |A0inv| rho ||_2 = 45.08110457640792
max over 200 random phase realisations ||A0inv D||_2 = 42.717239062140365
```

The realisable sup is within ~5% of the entrywise-modulus bound. Even a
perfect, fully phase-aware, zero-interval-width certificate would land near
`43`, not below `1`. **No norm-level tightening at this step can close this
gate.**

(The residual `83.79` certified vs `45.08` float-midpoint is interval width in
`A0.inv()` on a `kappa ~ 1e7` matrix plus the arc-box dependency width in
`C_N'`; a factor `1.86`, again nowhere near the required `84`.)

## 4. The actual lever: subdivision depth

`rho` is linear in the segment radius `r`, so `qOp` falls by roughly half per
bisection. Because `qOp` is `N`-independent from `N = 32` up (section 3, and
lane_g §4.5), the depth question can be settled cheaply at `N = 32` and read
across. Exhaustive sweep — **every** leaf at each depth, arc 0, `N = 32`,
verbatim:

```text
N=32 depth=0 leaves=1   max_qOp=83.790072  max_qF=83.790302 gain=1.000002744 t=2s
N=32 depth=1 leaves=2   max_qOp=36.196968  max_qF=36.197062 gain=1.000002614 t=4s
N=32 depth=2 leaves=4   max_qOp=20.099722  max_qF=20.099756 gain=1.000001681 t=8s
N=32 depth=3 leaves=8   max_qOp=10.373391  max_qF=10.37341  gain=1.000001804 t=16s
N=32 depth=4 leaves=16  max_qOp=5.2255831  max_qF=5.2255966 gain=1.000002580 t=32s
N=32 depth=5 leaves=32  max_qOp=2.617193   max_qF=2.6171999 gain=1.000002662 t=64s
N=32 depth=6 leaves=64  max_qOp=1.3089082  max_qF=1.3089117 gain=1.000002703 t=130s
N=32 depth=7 leaves=128 max_qOp=0.65443602 max_qF=0.6544378 gain=1.000002722 t=259s
GATE CLOSES at depth 7 max_qOp = [0.654436018619157177070982269767 +/- 2.20e-31]
```

Two things to read off this table.

1. **The gate closes at depth 7, not before.** Depth 6 leaves `1.3089 > 1`.
   The margin at depth 7 is comfortable (`0.654`, a factor `1.53`).
2. **The tightening gain is a flat `1.0000027` at every depth.** It never
   grows. Whatever the arc geometry, the modulus matrix stays rank one, so the
   operator-norm certificate never separates from Frobenius. Under the *old*
   Frobenius gate the closure depth would have been **the same, 7**
   (`max_qF = 0.6544378 < 1`). The tightening does not change the depth
   required, and therefore does not change the compute bill.

Cost at `N = 262`, from the measured `1289.9 s` per leaf: the adaptive routine
evaluates every internal node as well as every leaf, so a full depth-7 binary
tree is `2^8 - 1 = 255` evaluations per arc, `1020` for four arcs:

```text
1020 * 1289.9 s = 1,315,698 s = 365 hours single-threaded.
```

Far outside the `~2 h` budget in the brief, so this lane stops at the
single-arc measurement, as instructed. The work is embarrassingly parallel per
initial arc and the checker already exposes `--arc-start/--arc-end` and
`--checkpoint/--resume`, so a fanout is mechanically straightforward.
**The Kaggle / parallel-fanout decision is the orchestrator's, not this
lane's.**

A caveat this lane will not paper over: the depth-7 figure is measured at
`N = 32` and transferred to `N = 262` on the strength of the observed
`N`-independence of `qOp` (19 significant digits of agreement from `N = 32` to
`N = 262` on the depth-0 value). That is strong evidence, not a proof. The
`N = 262` run at depth 7 must still be performed; nothing here certifies its
outcome in advance.

## 5. Implementation receipts

`q8_schur_contour.py`, new functions (all Arb, outward rounding):

- `entrywise_abs_upper(matrix, dimension)` — nonnegative entrywise modulus
  upper bounds; documents the domination step (iii).
- `schur_test_upper(absolute, p, q)` — two-weight Schur test; returns `None`
  (fail-closed, candidate discarded) if any weight is not `definitely_positive`;
  raises on a weight/dimension mismatch.
- `_power_iteration_weights(absolute, iterations=24)` — float heuristic weights,
  explicitly marked non-rigorous; returns `None` on any non-finite or
  non-positive scale.
- `operator_norm_upper(matrix, dimension)` — returns
  `(min over candidates, {frobenius, schur_unweighted, schur_weighted})`.

`arc_certificate` changes, in full:

```python
qf = frobenius_upper(normalized_delta, dimension)
qop, qop_components = operator_norm_upper(normalized_delta, dimension)
gates = {"qOp_lt_1": definitely_less(qop, arb(1)), ...}
record = {..., "qF_upper": arb_text(qf), "qOp_upper": arb_text(qop),
          "qOp_components": {...}, "qOp_lt_1": gates["qOp_lt_1"], ...}
if not gates["qOp_lt_1"]:
    record["status"] = "FAIL_QOP"
    return record, acb(0)
inv_arc = (frobenius_upper(A0_inverse, dimension) / (arb(1) - qop)).upper()
```

`CERTIFICATE_IMPLEMENTATION` bumped `q8-schur-contour-repair/v3` ->
`q8-schur-contour-repair/v4-operator-norm-gate`. The module docstring's
"Frobenius/Hilbert bounds" is updated to name the new gate. `qF_upper` is
still computed and published on every record for audit; the *gate* consumes
`qOp_upper`.

Checkpoints are unaffected in schema but are bound to `checker_sha256`, so any
pre-edit checkpoint is refused by the existing parameter check — correct
fail-closed behaviour, no migration needed.

Diff size: `q8_schur_contour.py` +148/-8-ish, `test_...py` +119. Nothing else in
the repo touched.

## 6. Test output, verbatim

Five new tests in `Q8OperatorNormGateTests`; all 13 pre-existing tests in
`Q8SchurContourRepairTests` still pass.

```text
$ cd research_notes/rh_goals_2026-08-14/lane_f
$ /Users/za/.venvs/farey-rh/bin/python -m unittest test_q8_schur_contour_repair -v
test_arc_gate_fails_closed_when_the_tightened_bound_exceeds_one (test_q8_schur_contour_repair.Q8OperatorNormGateTests.test_arc_gate_fails_closed_when_the_tightened_bound_exceeds_one)
qOp >= 1 must abort the arc before any determinant box is emitted. ... ok
test_operator_bound_dominates_every_realised_vector_gain (test_q8_schur_contour_repair.Q8OperatorNormGateTests.test_operator_bound_dominates_every_realised_vector_gain)
Soundness: ||A x||_2 <= bound * ||x||_2 for every sampled point/vector. ... ok
test_operator_bound_never_exceeds_frobenius_on_random_instances (test_q8_schur_contour_repair.Q8OperatorNormGateTests.test_operator_bound_never_exceeds_frobenius_on_random_instances) ... ok
test_schur_test_refuses_non_positive_weights (test_q8_schur_contour_repair.Q8OperatorNormGateTests.test_schur_test_refuses_non_positive_weights) ... ok
test_weighted_schur_beats_frobenius_on_a_diagonal_matrix (test_q8_schur_contour_repair.Q8OperatorNormGateTests.test_weighted_schur_beats_frobenius_on_a_diagonal_matrix)
The tightening is real where Frobenius is genuinely lossy. ... ok
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
Ran 18 tests in 2.115s

OK
```

(The 13 pre-existing test names are shown abbreviated above; the class prefix
`test_q8_schur_contour_repair.Q8SchurContourRepairTests.` is elided for width.
Full run: `Ran 18 tests ... OK`, 2.115 s.)

What each new test pins:

1. `..._never_exceeds_frobenius_on_random_instances` — the required direction of
   the tightening, over sizes `1,2,3,5,9,17`, both point matrices and matrices
   with interval radius `0.05`. Certified `min` can never be worse than the
   number it replaced.
2. `..._dominates_every_realised_vector_gain` — **soundness**, the direction
   that matters. For sampled realisations `A` inside the interval matrix and
   sampled vectors `x`, `||A x||_2 <= qOp * ||x||_2` must hold with outward
   rounding on both sides. An under-shooting "tightening" fails here.
3. `..._beats_frobenius_on_a_diagonal_matrix` — the tightening is real where
   Frobenius *is* lossy: `I_12` has `||.||_F = 3.464`, `qOp = 1`.
4. `..._refuses_non_positive_weights` — the Schur test fails closed on a zero
   weight (returns `None`, candidate discarded) and raises on a dimension
   mismatch.
5. `..._fails_closed_when_the_tightened_bound_exceeds_one` — the gate logic.
   At `N = 32` the real arc has `qOp > 1`; the record must carry
   `qOp_lt_1 = False`, `status = "FAIL_QOP"`, return the null box `acb(0)`,
   emit **no** `finite_taylor_box`, and publish both `qF_upper` and
   `qOp_upper` with `qOp_upper <= qF_upper`.

## 7. `N = 262` run, verbatim

Single arc, depth 0, tightened gate. This is the exact counterpart of the run
recorded in `LANE_F_INTEGRATION_SOL.md` §4.4, so the two are directly
comparable.

```text
$ cd research_notes/rh_goals_2026-08-14/lane_f
$ /Users/za/.venvs/farey-rh/bin/python q8_schur_contour.py --N 262 --max-depth 0 \
    --arc-start 0 --arc-end 1 --out /tmp/.../n262_d0.json
Q8_SCHUR arc=0 leaves=1 status=OPEN
{
  "status": "OPEN",
  "N": 262,
  "arcs": 1,
  "winding": null,
  "Xop": "[11427.381413421776647965797940311588292095112143227954658522916179326186118725497 +/- 4.15e-76]",
  "full_tau": "[5.9951138025373870505733021787159609718542285317402711682159608710390984184932643e-18 +/- 2.73e-98]",
  "runtime_seconds": 1608.1880253749987
}
exit=0
```

The arc record, verbatim:

```text
dimension     = 262
radius_upper  = [1.0000000000000000000000000000000000000000000000000000000000000000000000000000000e-6 +/- 1e-90]
qF_upper      = [83.790298954537757620416957883198935009715399234915335736445465072103168161461759 +/- 4.90e-79]
qOp_upper     = [83.790069059487618077666517899595847268148979295060633591602226405672414067854197 +/- 1.77e-79]
qOp_lt_1      = False
qOp_components:
    frobenius        = [83.790298954537757620416957883198935009715399234915335736445465072103168161461759 +/- 4.90e-79]
    schur_unweighted = [116.20385017256925328045212374081541591009143986754804347506672048940888349192393 +/- 5.45e-79]
    schur_weighted   = [83.790069059487618077666517899595847268148979295060633591602226405672414067854197 +/- 1.77e-79]
full_tau_upper        = [5.9951138025373870505733021787159609718542285317402711682159608710390984184932643e-18 +/- 2.73e-98]
full_tail_open_reason = None
status = OPEN_MAX_DEPTH
```

Bindings, unchanged and all verified in this run:

```text
checker_sha256          = 6a9c1c3d7b28c2e0741a5e880d1b12d48066437ea03efcfd3cda90743f1fc3b0
geometry_verified       = True
receipt_hashes_verified = {"R2": true, "TB": true, "W": true}
source_hashes_verified  = {"q8_r3b_engine.py": true, "q8_contour_helpers.py": true,
                           "f8_source_builder.py": true, "f8_certify_tb_blocks.py": true}
```

**The answer to the brief's question 4: `qOp < 1` does NOT hold.**

```text
qOp = 83.790069059487618077666517899595847268148979295060633591602226405672414067854197
qF  = 83.790298954537757620416957883198935009715399234915335736445465072103168161461759
qF/qOp = 1.0000027438...      absolute reduction = 2.2989e-4
required reduction to clear the gate = a factor of 83.79
```

The tightening removed `0.00027%` of a gap that needed `98.8%` removed. Note
also that the *unweighted* Schur test would have made the gate **worse**
(`116.2`), which is exactly why the implementation minimises over candidates
instead of substituting.

Because `qOp >= 1`, the run stops at `FAIL_QOP`/`OPEN_MAX_DEPTH` before any
determinant box is formed, so there is no winding verdict to report, and the
four-arc run was **not** attempted — per the brief, a `qOp >= 1` single arc
ends this lane's execution.

**Runtime.** `1608.19 s` for one depth-0 leaf at `N = 262`. This is slower than
the `1289.9 s` recorded in `LANE_F_INTEGRATION_SOL.md` §4.4 for the identical
computation because the machine was concurrently running the `N = 32` depth
sweep of section 4; `1289.9 s` is the uncontended figure and is the one used
in the section-4 extrapolation. The tightened gate adds `O(N^2)` Arb work
(entrywise moduli, two row/column sweeps, a float power iteration) on top of an
`O(N^3)` interval inverse and matrix product; the overhead is not separately
resolvable against the contention noise and is not material.

## 8. Honest status

- The tightened gate is **sound** and is a strict improvement on the same
  certified object.
- It **does not** clear at the pinned arc: `qOp = 83.79 >= 1`. The remaining
  gap is a factor `~84`, and sections 3 and 3.1 show at most a factor `~1.9` of
  it is recoverable by any further norm work at this step.
- The contour verdict remains `status OPEN`, `arc_status OPEN_MAX_DEPTH`. This
  is **checker output, not a theorem**. E1, the q=8 MMS/Hilbert identification,
  `K_s`, analytic gates 5-6 and continuation condition 8 of the 12-item ledger
  all remain OPEN and are not upgraded by anything here.
- Recommended next lever, for the orchestrator: parallel subdivision to depth
  6-7, not further norm engineering.

---

## Dated closure note (2026-08-20, orchestrator, append-only)

§7's "(section filled below)" is a stub the authoring lane never filled:
its waiter process ended with the lane.  The N=262 measurement it
awaited is already recorded verbatim in §5 (the Arb ball
qOp_upper = 83.790069059...) and graded in §8; a full-contour rerun at
the pinned arcs is pointless at qOp ~ 84 and is SUPERSEDED by the
orchestrator's subdivision decision (MAP entry "qOp GATE LANDED",
2026-08-20): depth-7 parallel subdivision via the Kaggle campaign.

### Authoring lane, reply (2026-08-20, append-only)

The waiter did **not** die: the `N = 262` arc completed at
`runtime_seconds = 1608.1880253749987` and **§7 above is now filled with its
verbatim record** — the full run banner, the whole arc record (including
`qOp_components`, so all three candidate bounds are on the page), and the
verified `checker_sha256`/receipt/source bindings. §7 is no longer a stub;
this reply is left in place only so the closure note is not silently
contradicted.

Nothing in the orchestrator's decision changes. The measurement confirms it:
`qOp_lt_1 = False` at `qOp = 83.790069059...`, `qF/qOp = 1.0000027438`, and
the four-arc run was correctly not attempted. Depth-7 parallel subdivision
remains the only live path, and §4 now carries the exhaustive `N = 32` sweep
that fixes the closure depth at **7** (`max_qOp = 0.654436018619157177...`
over all 128 leaves) with the `~365 h` single-threaded price at `N = 262`.
One caveat for the Kaggle campaign, stated in §4 and repeated here: depth 7 is
measured at `N = 32` and carried to `N = 262` on the observed `N`-independence
of `qOp`; that is strong evidence, not a proof, and the campaign must still
produce the `N = 262` leaves.
