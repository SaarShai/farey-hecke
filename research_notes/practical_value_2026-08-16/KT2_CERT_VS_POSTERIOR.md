# KT2 — Certificate width vs Bayesian posterior width on MSM timescales

Date: 2026-08-16. Lane: KT2 of the MD-timescale-certificate path (follows
`KT1_MSM_INCUMBENT_CHECK.md`, verdict PROCEED-TO-KT2).

Pre-registered kill condition (from KT1 §5, restated here verbatim in effect):
**KILL if certificate widths are not materially smaller than posterior widths
AND close slow-eigenvalue gaps are rare.**

Everything below is measured, not cited. Scripts and JSON receipts:
`kt2_/kt2_common.py`, `kt2_/kt2_bench.py`, `kt2_/kt2_degeneracy.py`,
`kt2_/kt2_scale.py`, `kt2_/kt2_bench.json`, `kt2_/kt2_degeneracy.json`,
`kt2_/kt2_scale.json`.

## 1. What was certified, and what the certificate assumes

Estimator certified: the **non-reversible maximum-likelihood MSM**
`T_ij = C_ij / sum_k C_ik`. With integer transition counts this is an **exact
rational matrix**, so no rounding occurs between the data and the certified
object. Counts come from deeptime's `count_mode="sliding-effective"`
(= sliding counts divided by the lag), which is both the counting mode
deeptime's `BayesianMSM` accepts and exactly rational; the integrality of
`lag * C` is asserted in code.

Enclosure: Arb's verified eigensolver (`flint.acb_mat.eig`, Rump algorithm)
returns disjoint complex disks each provably containing one eigenvalue of that
exact rational matrix. Implied timescales use `t_i = -tau / log|lambda_i|`
evaluated in ball arithmetic, so the interval is valid without assuming
`lambda_i` is real. Two working precisions are reported: **prec 53** (the
honest "same working precision as the incumbent" setting) and **prec 333**.

Explicitly **not** certified: sampling error, discretisation error, the
Markov assumption, the reversible MLE (an iterative fixed point that would
need a verified fixed-point step), and the clustering. The certificate covers
implementation/floating-point error of the spectral step only. This is the
same scope KT1 found the incumbents do *not* claim to cover.

## 2. Part A — Prinz quadruple well, certificate vs posterior

System: `deeptime.data.prinz_potential` (Prinz et al. 2011 benchmark),
h=1e-5, 100 integrator steps/frame, 500k frames, k-means with 25 microstates,
lag 10, `BayesianMSM(n_samples=500, reversible=True)`. Widths are full widths
(certificate: 2 x radius; posterior: 95% CI width).

| frames | t_i | ITS (certified mid) | cert width @prec53 | cert width @prec333 | posterior 95% CI width | ratio CI/cert@53 |
|---|---|---|---|---|---|---|
| 1 000   | t2 | 345.78 | 4.4e-11 | 1.0e-94 | 4001   | 9.1e+13 |
| 1 000   | t3 | 99.04  | 1.7e-12 | 6.2e-96 | 294.1  | 1.8e+14 |
| 1 000   | t4 | 12.83  | 4.9e-14 | 1.2e-97 | 69.13  | 1.4e+15 |
| 10 000  | t2 | 823.22 | 9.0e-10 | 7.0e-94 | 1776   | 2.0e+12 |
| 10 000  | t3 | 104.59 | 1.6e-11 | 1.0e-95 | 91.65  | 5.7e+12 |
| 10 000  | t4 | 52.65  | 2.2e-12 | 3.2e-96 | 24.38  | 1.1e+13 |
| 100 000 | t2 | 765.64 | 5.4e-10 | 6.1e-94 | 339.6  | 6.3e+11 |
| 100 000 | t3 | 115.29 | 1.1e-11 | 9.5e-96 | 27.82  | 2.6e+12 |
| 100 000 | t4 | 60.08  | 3.6e-12 | 4.8e-96 | 8.922  | 2.5e+12 |
| 500 000 | t2 | 772.02 | 2.7e-10 | 5.4e-94 | 137.3  | 5.1e+11 |
| 500 000 | t3 | 124.65 | 7.2e-12 | 1.5e-95 | 12.81  | 1.8e+12 |
| 500 000 | t4 | 60.68  | 2.5e-12 | 4.1e-96 | 4.004  | 1.6e+12 |

Two facts follow.

1. Certificate width is smaller than posterior width by **11 to 15 orders of
   magnitude**, at every sample size tested. There is no crossover: increasing
   data from 1k to 500k frames shrinks the posterior by ~30x while the
   certificate width stays ~1e-10. Extrapolating the observed posterior
   narrowing (width ~ n^-1/2), closing a factor 1.4e12 in width needs ~2e24x
   more data, i.e. of order 1e30 frames. There is no reachable crossover.
2. The *estimator choice* dominates numerics by a similar margin. At 100k
   frames the reversible and non-reversible MLE give t2 = 766.21 vs 765.64, a
   difference of 0.56 — about **1e9 times the certificate width**. Modelling
   decisions, not roundoff, set the digit at which the number stops meaning
   anything.

Certified gap enclosures were computed for every case
(`gap23`, `gap34` in `kt2_bench.json`): all were certified strictly positive,
e.g. at 500k frames |lambda_2| - |lambda_3| = 0.0642 +/- 9e-99.

## 3. Part B1 — engineered near-degeneracy

Ground truth: two *independent* two-state processes, product chain on 4
states, eigenvalues exactly `1, 1-2p, 1-2q, (1-2p)(1-2q)` with p = 0.02 and
q = p(1-rel). At rel = 0 the two slow eigenvalues are **exactly degenerate**.
Trajectories of 10k and 100k steps were sampled from the exact chain.

| rel detuning | true slow gap | n | certified empirical gap23 | gap certified positive | numpy max abs imag | posterior CI overlap of t2,t3 |
|---|---|---|---|---|---|---|
| 0.3  | 1.2e-2 | 100 000 | 1.392e-2 +/- 1.5e-99 | yes | 0.0 | no |
| 0.1  | 4.0e-3 | 100 000 | 6.050e-3 +/- 1.2e-99 | yes | 0.0 | no |
| 0.03 | 1.2e-3 | 100 000 | 3.034e-3 +/- 1.2e-99 | yes | 0.0 | no |
| 0.01 | 4.0e-4 | 100 000 | 1.863e-3 +/- 1.1e-99 | yes | 0.0 | **yes** |
| 3e-3 | 1.2e-4 | 100 000 | 1.275e-3 +/- 2.3e-99 | yes | 0.0 | **yes** |
| 1e-3 | 4.0e-5 | 100 000 | 1.089e-3 +/- 1.7e-99 | yes | 0.0 | **yes** |
| 1e-4 | 4.0e-6 | 100 000 | 9.420e-4 +/- 2.4e-99 | yes | 0.0 | **yes** |
| **0** | **0** | 100 000 | 9.502e-4 +/- 2.1e-99 | yes | 0.0 | **yes** |

(rel = 1.0 is absent: q = 0 disconnects the chain, so `submodel_largest` gives
fewer than 4 states and the row is skipped. Full 10k-step rows are in
`kt2_degeneracy.json`; they behave the same, with larger empirical gaps.)

The decisive line is the last one. **Even when the true generator has an
exactly degenerate pair, the sampled count matrix does not.** Statistical
noise splits the empirical eigenvalues by ~1e-3 at 100k steps — about **1e12
times the prec-53 certificate radius (~1e-15)**. The verified eigensolver
never had to work hard: it isolated the eigenvalues at prec 53 in every case,
and `numpy.linalg.eigvals` never produced a spurious complex pair
(max |Im lambda| = 0.0 exactly, in all 16 rows).

Where the pair *does* become unresolvable is statistically: for rel <= 0.01
the 95% posterior CIs of t2 and t3 overlap. That is a sampling verdict, and a
numerical certificate does not touch it.

## 4. Part B2 — how often close gaps occur in a realistic MSM

Survey: Prinz potential, 8 seeds x {20, 40} microstates x lags {5, 10, 25} =
48 fitted MSMs, 144 adjacent slow-timescale pairs, 300 Bayesian samples each.

| quantity | value |
|---|---|
| adjacent pairs examined | 144 |
| pairs whose 95% posterior CIs overlap | **0 / 144 (0.0%)** |
| pairs whose certified enclosures overlap | 0 / 144 (0.0%) |
| minimum relative gap (t_i - t_{i+1})/t_i | 0.3036 |
| 5th-percentile relative gap | 0.4230 |
| median relative gap | 0.8104 |
| certificate isolation failures | 0 / 48 |

Every gap in this benchmark is wide: the tightest adjacent pair is separated
by 30% of the larger timescale. The slow spectrum of a metastable system is
gapped by construction — that is what makes it an MSM — so the near-degenerate
regime the certificate is built for is not where these models live. This is
benchmark-specific evidence (one 1-D system); see limits in §7.

## 5. Part C — larger, sparser MSMs, and the actual float error

Prinz, 500k frames, lag 10, finer discretisation (sparser, closer to
reducible). `numpy |eig| error` is the true error of the incumbent's float
eigensolver, measured against the certified enclosure.

| microstates | sparsity | min row count | cond(eigvec) | cert width @53 (t2) | numpy abs-eig error (top 5) | posterior CI width (t2) | cert time @53 | cert time @333 | Bayesian time |
|---|---|---|---|---|---|---|---|---|---|
| 50  | 0.522 | 1772 | 79.9 | 1.1e-9 | <= 2.1e-15 | 147.9 | 5.2 s  | 27.3 s  | 2.0 s |
| 100 | 0.568 | 298  | 111  | 9.6e-10 | <= 1.1e-15 | 142.5 | 46.0 s | 155.9 s | 2.8 s |
| 200 | 0.620 | 27   | 349.6 | 1.8e-9 | <= 1.4e-14 | 153.1 | 176.1 s | not run | 14.3 s |

The incumbent's float eigenvalues are accurate to ~1e-15 (1e-14 at 200 states)
in modulus — inside the certified enclosure, as required, and 13 to 14 orders
below the posterior width. Conditioning stays benign (cond(V) ~ 1e2 to 3e2)
even at 62% sparsity with a minimum row count of 27.

Cost runs the other way. The verified eigensolver at prec 53 already costs
**16x the entire 200-sample Bayesian posterior** at 100 states (46 s vs 2.8 s)
and 12x at 200 states (176 s vs 14 s), and grows steeply with size:
5.2 -> 46 -> 176 s over 50 -> 100 -> 200 states (~n^2.5-3.1). A first run that
also requested prec 333 at 200+ microstates did not finish 200 states in ~45
minutes and was cut; the affordable-precision schedule in `kt2_scale.py`
reflects that. The 400-microstate row had run **more than 45 minutes at prec
53 without completing** when this note was written (process elapsed 56 min
total, with the 50/100/200 rows accounting for ~10 min); that is a measured
lower bound on its cost, not a finished data point. It cannot change the sign
of a 1e11 width ratio, and it makes the cost verdict worse, not better.

## 6. VERDICT — **KILL** (with one narrow surviving use)

Applying the pre-registered condition honestly requires reading both clauses
together, because the first one is a trap.

* Clause 1 as literally written ("certificate widths not materially smaller
  than posterior widths") is **false**: certificate widths are 1e11 to 1e15
  times *smaller*. Read literally, the conjunction fails and the rule says
  PROCEED.
* But the literal reading inverts the intent. The certificate being 1e12 times
  narrower than the posterior is exactly the finding that **floating-point
  error is not a live source of uncertainty in MSM timescales**. The
  certificate is not adding information; it is confirming, expensively, that
  the incumbent's numbers were already right to ~1e-15 (§5, measured).
* Clause 2 holds as intended: **close gaps are rare**. 0/144 adjacent pairs in
  a realistic survey are numerically or statistically ambiguous by numerics,
  and even an *exactly degenerate true generator* produces an empirical matrix
  whose gap is 1e12 x the certificate radius (§3).

So the substantive kill condition — "the certificate adds nothing" — is met,
and the honest verdict is **KILL** for the headline application (certified
enclosures on fitted MSM slow timescales/gaps as a value-add over Bayesian
MSMs). Cost seals it: the certificate is 16x the incumbent's whole posterior
at 100 states and scales ~n^3, against zero measured error to correct.

Recording the pre-registration defect: the KT2 condition should have been
"KILL unless the certificate width is *comparable to or larger than* the
posterior width in some realistic regime, i.e. unless numerics can actually
move a conclusion." Under that (correct) criterion the answer is a clean KILL.

**Narrow survivor, not a program.** The one thing the certificate does that
the posterior does not is give a *deterministic, reproducible receipt* —
e.g. `|lambda_2| - |lambda_3| = 0.0642 +/- 9e-99, certified positive`, and a
refusal (isolation failure) instead of a silent wrong answer. That is a
regression-test / cross-version-audit artefact, worth at most a small utility,
and it is not a research contribution. It does not justify the MD-timescale
program.

## 7. Honest limits

* One model system (1-D Prinz quadruple well) plus one engineered 4-state
  product chain. No real MD trajectory (protein, peptide) was tested; a real
  system has more states, worse connectivity, and heavier-tailed count
  distributions. The 30% minimum relative gap is a property of *this*
  benchmark, and a real system with many comparable slow processes could show
  tighter gaps. It would still have to beat the ~1e12 margin measured in §3
  for numerics to matter.
* The certified estimator is the non-reversible MLE. The reversible MLE that
  most practitioners use is an iterative fixed point and was not certified;
  §2 shows the two differ by ~1e9 x the certificate width, which is itself the
  argument against certifying the spectral step in isolation.
* Only `numpy.linalg.eig` (LAPACK dgeev) was audited as the float baseline.
  A sparse/iterative eigensolver (ARPACK, as used for large MSMs) has
  different and larger error, which was not measured here.
* Bayesian posteriors used deeptime defaults (reversible, 200-500 samples);
  no convergence study of the sampler was run. Sampler under-convergence would
  make posterior widths *wrong*, not narrow enough to approach 1e-10.
* Prec-53 certificate widths are not the tightest possible; they are the fair
  "same working precision" comparison. Prec 333 narrows them 84 further orders
  at 3-5x cost, which only strengthens the conclusion.

## 8. Reproduce

```
python3.12 -m venv VENV && VENV/bin/pip install deeptime python-flint
cd research_notes/practical_value_2026-08-16/kt2_
VENV/bin/python kt2_bench.py        # -> kt2_bench.json     (~2 min)
VENV/bin/python kt2_degeneracy.py   # -> kt2_degeneracy.json (~25 min)
VENV/bin/python kt2_scale.py        # -> kt2_scale.json      (hours at n>=200)
```
Versions used: deeptime 0.4.5, python-flint 0.9.0 (Arb/FLINT), Python 3.12.13,
macOS arm64.
