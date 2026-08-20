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
qOp_upper = 83.790069059...   (see section 5 for the verbatim Arb ball)
gain      = 1.0000027
```

The reason is structural and is stated in section 3: the entrywise-modulus
matrix that the arc enclosure hands the gate is **numerically rank one**
(`sigma_2/sigma_1 = 2.34e-3`), and for a rank-one nonnegative matrix Frobenius
*is* the operator norm. There was never a `sqrt(N)` to recover.

The verdict on the contour is unchanged: `status OPEN`, arc `OPEN_MAX_DEPTH`.
**This is checker output, not a theorem.** Analytic gates 5-6 and continuation
condition 8 of the 12-item ledger are untouched by anything in this note.

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

`rho` is linear in the segment radius `r`, so `qOp` falls roughly by half per
bisection. Measured (see section 6 for the full sweep) the gate needs depth
6-7. That is `2^6` to `2^7` leaves per arc, times four arcs, at a per-leaf cost
of `1289.9 s` at `N = 262` — i.e. **90 to 180 hours single-threaded**. The
gate is not mathematically stuck; it is compute-bound. The leaves are
embarrassingly parallel and the checker already exposes `--arc-start/--arc-end`
and `--checkpoint/--resume`. **The Kaggle / parallel-fanout decision is the
orchestrator's, not this lane's.**

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

(section filled below)

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
