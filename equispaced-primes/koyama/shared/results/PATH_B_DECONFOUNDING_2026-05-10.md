# Path B rank/conductor deconfounding, Agent D

Date: 2026-05-10

Scope: EC-only refit from local stored data. No PARI/GP was run.

Inputs:

- `koyama-shared/data/PATH_B_20FORMS.csv`
- `koyama-shared/data/RANK0_CLUSTER.json`
- `koyama-shared/data/PHASE1_EC_RECOMPUTE.json`
- `koyama-shared/data/RANK3_5077A1.json`
- `koyama-shared/data/PHASE1_500ZEROS_CORRECTED.json` only as a warning source: its EC rows are invalid per project notes, so they are not used.

Primary regression set: 19 EC rows from `PATH_B_20FORMS.csv`. The `Delta` row is excluded.

Response: `y = E_C1_sq`.

Conductor covariate: `logNc = log(conductor) - mean(log(conductor))`, where
`mean(log(conductor)) = 4.174328568476445`.

Bootstrap: ordinary row bootstrap, deterministic seed `20260510`, `B = 20000`.

## Data shape

| rank | n | conductor range | mean E[C1^2] | sd |
|---:|---:|---:|---:|---:|
| 0 | 8 | 11-24 | 1.915635 | 0.190041 |
| 1 | 6 | 37-61 | 2.100339 | 0.289129 |
| 2 | 4 | 389-571 | 2.680774 | 0.306595 |
| 3 | 1 | 5077-5077 | 4.647380 | n/a |

Rank and conductor are almost locked together:

- Pearson corr(rank, logN) = 0.972107, p = 3.85e-12.
- Pearson corr(rank, conductor) = 0.651348, p = 0.00252.

This is the main design defect. Current Path B can see an upward ladder, but it cannot say whether the ladder is rank or conductor.

## Model refits

Equations use centered `logNc`.

| model | fitted equation | R2 | RMSE |
|---|---|---:|---:|
| rank | `y = 1.754630 + 0.585860 rank` | 0.640938 | 0.399740 |
| logN | `y = 2.278821 + 0.362318 logNc` | 0.767247 | 0.321840 |
| rank + logN | `y = 2.884786 - 0.677256 rank + 0.734456 logNc` | 0.814362 | 0.287426 |
| rank + logN + interaction | `y = 2.054615 + 0.001435 rank + 0.083772 logNc + 0.155977 rank*logNc` | 0.873223 | 0.237527 |

Raw uncentered check matches the previous local audit: in the interaction model the uncentered rank coefficient is `-0.649666` with 95% CI `[-1.261470, -0.037861]`. This raw coefficient is an extrapolated effect at conductor 1, so the centered coefficient above is the cleaner survival test.

## Rank survival screen

Acceptance rule requested: rank survives only if coefficient is positive, CI excludes 0, and LOO is robust.

| model | rank beta | parametric 95% CI | bootstrap 95% CI | bootstrap P(beta <= 0) | LOO rank beta range | verdict |
|---|---:|---:|---:|---:|---:|---|
| rank | 0.585860 | [0.361476, 0.810243] | [0.238656, 0.845991] | 0.00005 | [0.358825, 0.621127] | pass, but confounded |
| rank + logN | -0.677256 | [-1.389720, 0.035209] | [-1.215800, 0.100555] | 0.95565 | [-0.786934, -0.253343] | fail |
| rank + logN + interaction | 0.001435 | [-0.819718, 0.822588] | [-0.689960, 0.739053] | 0.61475 | [-0.317877, 0.194992] | fail |

Notes:

- Rank-only passes mechanically, but this is exactly the model that ignores the confounder.
- `logN` alone beats rank-only on R2 and RMSE.
- In the additive conductor-controlled model, rank flips negative and LOO is negative for every omitted row.
- In the interaction model, the rank main effect at mean log conductor is essentially zero and LOO changes sign.
- The interaction term itself is positive: `0.155977`, 95% CI `[0.029998, 0.281957]`, p = 0.0186. This says the apparent rank slope grows with conductor, not that rank has been isolated.

Conditional rank slope in the interaction model:

| conductor | implied dE[C1^2]/drank |
|---:|---:|
| 20 | -0.182399 |
| 50 | -0.039479 |
| 65 | 0.001444 |
| 389 | 0.280518 |
| 5077 | 0.681207 |
| 19747 | 0.893068 |
| 214850 | 1.265376 |
| 234446 | 1.278991 |

This is another way to see the confounding: the model turns rank into a high-conductor effect.

## LOO details

Most important leave-one-out facts:

- Rank-only remains positive under all omissions, but removing `5077a1` drops rank beta from `0.585860` to `0.358825` and drops R2 to `0.564626`.
- Additive rank+logN remains negative under all omissions.
- Interaction rank effect is sign-unstable. The minimum is after dropping `5077a1` (`-0.317877`); the maximum is after dropping `11a1` (`0.194992`).

## Leverage and residual diagnostics

Diagnostics below use the full interaction model. `stud_resid` is the internally studentized residual.

| label | rank | conductor | y | fitted | residual | leverage | stud_resid |
|---|---:|---:|---:|---:|---:|---:|---:|
| 11a1 | 0 | 11 | 1.667322 | 1.905799 | -0.238478 | 0.337291 | -1.095827 |
| 14a1 | 0 | 14 | 2.098570 | 1.926002 | 0.172568 | 0.160593 | 0.704579 |
| 15a1 | 0 | 15 | 1.895785 | 1.931782 | -0.035997 | 0.136117 | -0.144874 |
| 17a1 | 0 | 17 | 1.755942 | 1.942267 | -0.186325 | 0.121328 | -0.743555 |
| 19a1 | 0 | 19 | 1.786922 | 1.951584 | -0.164662 | 0.140225 | -0.664289 |
| 20a1 | 0 | 20 | 2.111537 | 1.955881 | 0.155655 | 0.159098 | 0.634960 |
| 21a1 | 0 | 21 | 1.829791 | 1.959969 | -0.130178 | 0.183000 | -0.538742 |
| 24a1 | 0 | 24 | 2.179215 | 1.971155 | 0.208060 | 0.278083 | 0.916009 |
| 37a1 | 1 | 37 | 1.873493 | 1.920973 | -0.047480 | 0.289731 | -0.210743 |
| 43a1 | 1 | 43 | 1.922311 | 1.957003 | -0.034692 | 0.188820 | -0.144088 |
| 53a1 | 1 | 53 | 1.948656 | 2.007132 | -0.058476 | 0.113011 | -0.232260 |
| 57a1 | 1 | 57 | 2.200051 | 2.024576 | 0.175475 | 0.104260 | 0.693553 |
| 58a1 | 1 | 58 | 2.643024 | 2.028746 | 0.614278 | 0.103516 | 2.426882 |
| 61a1 | 1 | 61 | 2.014497 | 2.040837 | -0.026339 | 0.104298 | -0.104107 |
| 389a1 | 2 | 389 | 2.549622 | 2.765539 | -0.215917 | 0.147076 | -0.874555 |
| 433a1 | 2 | 433 | 2.488029 | 2.807945 | -0.319915 | 0.156654 | -1.303129 |
| 446d1 | 2 | 446 | 3.138691 | 2.819651 | 0.319040 | 0.161718 | 1.303485 |
| 571b1 | 2 | 571 | 2.546753 | 2.917423 | -0.370670 | 0.244921 | -1.595680 |
| 5077a1 | 3 | 5077 | 4.647380 | 4.463327 | 0.184053 | 0.870262 | 1.911452 |

High-leverage warning:

- `5077a1` has leverage `0.870262`. The only rank-3 point effectively anchors the high-conductor/high-rank end.
- `58a1` has the largest residual (`stud_resid = 2.426882`) despite moderate leverage. It should be kept as a real local fluctuation, not silently trimmed.

## JSON anchor cross-check

Valid EC JSON subset:

- Rank 0: six curves from `RANK0_CLUSTER.json`, conductors 11-20.
- Rank 1: `37a1` from `PHASE1_EC_RECOMPUTE.json`, 500 zeros.
- Rank 2: `389a1` from `PHASE1_EC_RECOMPUTE.json`, 500 zeros.
- Rank 3: `5077a1` from `RANK3_5077A1.json`, 500 zeros.

This subset is smaller and even more conductor-confounded, so it is not the acceptance basis. It gives the same qualitative result:

| model | rank beta | 95% CI | R2 | verdict |
|---|---:|---:|---:|---|
| rank | 0.811128 | [0.586503, 1.035754] | 0.912401 | pass, confounded |
| logN | n/a | n/a | 0.969982 | logN stronger |
| rank + logN | -0.222541 | [-0.931961, 0.486879] | 0.972666 | fail |
| rank + logN + interaction | 0.065544 | [-0.856212, 0.987299] | 0.979271 | fail |

## Conductor-control queue

Goal: break the rank/logN lock before making any rank-linear claim.

### Queue A: controls near existing rank-2 conductors

Target conductor band: 389-571.

Existing high-rank rows:

- `389a1`, rank 2, conductor 389
- `433a1`, rank 2, conductor 433
- `446d1`, rank 2, conductor 446
- `571b1`, rank 2, conductor 571

Needed controls:

- At least 3 rank-0 ECs with conductor in 350-650.
- At least 3 rank-1 ECs with conductor in 350-650.
- Prefer direct nearest-neighbor controls around 389, 433/446, and 571.

Decision test:

- Fit within 350-650 first, before mixing with low-conductor rank 0/1 rows.
- Rank survives this band only if rank coefficient is positive, bootstrap CI excludes 0, and every LOO deletion keeps it positive.

### Queue B: controls near the rank-3 singleton

Target conductor band: centered at 5077.

Existing high-rank row:

- `5077a1`, rank 3, conductor 5077.

Needed controls:

- Rank-0 ECs in 4500-5600.
- Rank-1 ECs in 4500-5600.
- Rank-2 ECs in 4500-5600.
- At least two curves per lower-rank bucket if available.

Decision test:

- Do not use `5077a1` as a singleton rank-3 anchor in a global rank claim.
- Accept only if rank-3 remains high against conductor-matched lower-rank controls, not merely against conductor 11-61 controls.

### Queue C: high-conductor rank-0 controls near rank-4 candidates

Rank-4 candidate conductors named in the sprint brief:

- 19747
- 214850
- 234446

Required before any rank-4 claim:

| candidate conductor | first control band | fallback band | required control |
|---:|---:|---:|---|
| 19747 | 18760-20735 | 17772-21722 | rank-0 EC, then rank-1 if available |
| 214850 | 204108-225592 | 193365-236335 | rank-0 EC, then rank-1 if available |
| 234446 | 222724-246168 | 211001-257891 | rank-0 EC, then rank-1 if available |

Use exact conductor-nearest controls when available. If no curve exists in the first band, widen once and record the widening. Do not compare rank 4 against the current low-conductor rank-0 cluster as evidence for rank.

### Minimum new matrix

The next useful dataset is not "more high rank only"; it is a crossed matrix:

| conductor tier | rank 0 | rank 1 | rank 2 | rank 3 | rank 4 |
|---|---:|---:|---:|---:|---:|
| 350-650 | 3+ | 3+ | existing 4 | optional | n/a |
| 4500-5600 | 2+ | 2+ | 2+ | existing 1 | n/a |
| near 19747 | 1+ | optional | optional | optional | candidate |
| near 214850 | 1+ | optional | optional | optional | candidate |
| near 234446 | 1+ | optional | optional | optional | candidate |

## Verdict

Current rank/conductor verdict: rank does not survive deconfounding.

Precise statement:

- The EC-only Path B CSV contains an upward rank signal.
- The signal is not isolated from conductor.
- Under the requested acceptance rule, only the rank-only model passes.
- Once `log(conductor)` is added, rank fails by sign, CI, and LOO robustness.
- The interaction model fits best, but it converts the apparent rank effect into a conductor-dependent slope and leaves the rank main effect unidentified.

Status: W2 remains plausible as a research hypothesis, but the current Path B evidence should be reported as conductor-confounded, not as an accepted rank law.
