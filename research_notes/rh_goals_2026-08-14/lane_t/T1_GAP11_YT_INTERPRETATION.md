DRAFT (builder lane) 2026-08-26 — UNREFEREED

# GAP-11: does the 0.26% tension survive when the estimator runs on y(t) itself?

## Task

Check whether `|C(gamma_1)| = 6.287349e-03` vs predicted
`a_gamma_1 = 6.271348e-03` (ratio 1.0026) is an apples-to-oranges artifact —
i.e. whether that `6.287349e-03` figure actually came from a prime-count
estimator rather than from the signal y(t) as defined in
`T1_GAP11_N1_RERUN.md` / `t1_gap11_rerun.py`.

## What was built and run

`t1_gap11_yt_estimator.py` reuses `t1_gap11_rerun.py`'s `sieve_mobius` and
reconstructs y(t) with byte-identical parameters (N_MAX = 3e7, 200-point
log grid, N_GRID_MIN = 1000, R0 = -2, R_{-1}(N) = 12/N, R_triv leading
term), then applies the identical trapezoidal matched-filter estimator
`C(gamma) = (1/T) int y(t) e^{-i gamma t} dt` directly to that y(t) series,
at gamma_1 = 14.134725141734693.

## Result

```
|C(gamma_1)| on y(t), this run   = 6.287349e-03
predicted a_gamma_1 (Prop R)      = 6.271348e-03   ratio = 1.0026
previous |C(gamma_1)| (N1 rerun)  = 6.287349e-03   ratio = 1.0000
```

Full receipt: `T1_GAP11_YT_RECEIPT.json`.

## Finding

The `6.287349e-03` figure is **not** a prime-count-estimator artifact. It
was already, in `t1_gap11_rerun.py`, computed by a matched filter applied
directly to the same y(t) series constructed here — this run reproduces it
to 10 significant figures using an independently written script that only
borrows the Möbius sieve. The apples-to-oranges comparison flagged in
`T1_CRAMER_RAO_DRAFT.md` GAP-11 row and echoed in `T1_GAP11_N1_RERUN.md`'s
"Bearing on GAP-11" section is a **different pair of numbers**: the T1
model-N2 bound RMSE at gamma_1 (0.030874) vs. Gate-1's MUSIC/periodogram
empirical error on prime counts (0.005654) — not the `6.287349e-03` vs
`6.271348e-03` comparison.

So: **the 0.26% tension between the matched-filter amplitude and Prop R's
predicted amplitude is a genuine same-observable (y(t)-vs-y(t)-prediction)
result, and it survives** — it was never the apples-to-oranges leg of
GAP-11's open question. The apples-to-oranges leg (T1 bound vs Gate-1
empirical error) remains open and is untouched by this run, since it
compares two different estimators/observables by construction, not two
runs of the same estimator.

## Scope note

This is a same-estimator confirmation pass, not a new derivation or a
resolution of GAP-11's Gate-1/T1-bound apples-to-oranges question.

## FRONTIER VERIFICATION 2026-08-26 (fable) — cold re-run PASS
Independent re-run of t1_gap11_yt_estimator.py (sha256 b36efa6c…) reproduces
|C(gamma_1)| = 6.287349e-03 on y(t); ratio to Prop R prediction = 1.0026.
Banked: the 0.26% tension is a genuine same-observable comparison (the earlier
"apples-to-oranges" worry about THIS number is retired). The remaining GAP-11
item narrows to interpreting T1 bound RMSE (0.030874) vs Gate-1's empirical
MUSIC error (0.005654) — a bound-vs-achieved comparison, not a discrepancy:
an empirical error BELOW the unbiased-CR bound for a different estimator class
signals the Gate-1 estimator is biased/uses prior structure, which is exactly
what the GAP-7 van Trees lane formalizes. Final wording OWED to the T1 draft
after GAP-7 lands.
