UNDECIDED at reached N

# C_W(N) growth audit

Verdict is deliberately scoped to the computed data through N=10,000,000. The measured sequence is incompatible with the proposed fixed-slope loglog law, but the finite sample also has spikes (notably N=300,000 and 10,000,000) outside the claimed 0.679 ± 0.002 band.

## Decade increments

The `0.24 prediction` is 0.24·[log log(10N) − log log N]. All C values below are actual rows in the CSV; no interpolation is used.

| N | 10N | C_W(N) | C_W(10N) | measured Δ | Δloglog | 0.24·Δloglog | |Δ|/prediction |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 100 | 1,000 | 0.496783551 | 0.634761472 | +0.137977922 | 0.405465108 | 0.097311626 | 1.418 |
| 1,000 | 10,000 | 0.634761472 | 0.666148775 | +0.031387303 | 0.287682072 | 0.069043697 | 0.455 |
| 10,000 | 100,000 | 0.666148775 | 0.668123962 | +0.001975187 | 0.223143551 | 0.053554452 | 0.037 |
| 100,000 | 1,000,000 | 0.668123962 | 0.679304965 | +0.011181003 | 0.182321557 | 0.043757174 | 0.256 |
| 300,000 | 3,000,000 | 0.698697063 | 0.682497667 | -0.016199396 | 0.167696516 | 0.040247164 | 0.402 |
| 1,000,000 | 10,000,000 | 0.679304965 | 0.696380179 | +0.017075213 | 0.154150680 | 0.036996163 | 0.462 |

Additional requested 3× pair: `300,000 → 3,000,000` has Δ=-0.016199396; 0.24·Δloglog=0.040247164.

Across the high-N decade pairs (N≥1,000), max |Δ|/predicted increment = 0.462; the measured changes are below the 0.24·loglog increments, but are not monotone or rapidly convergent to one fixed value. The 100→1,000 row is a low-N transient and is shown for completeness.

## Anchor reproduction

| N | expected | measured C_W | source | rounded | pass to 3 decimals |
|---:|---:|---:|---|---:|:---:|
| 100 | 0.497 | 0.496783551 | direct_longdouble | 0.497 | PASS |
| 1,000 | 0.635 | 0.634761472 | direct_longdouble | 0.635 | PASS |
| 100,000 | 0.668 | 0.668123962 | fast_Mertens_proxy | 0.668 | PASS |

The direct route reproduces the N=100 and N=1,000 anchors. N=100,000 is the fast Mertens/Jordan row and reproduces the stated 0.668 anchor.

## Direct versus fast validation

The Mertens identity is exact for the inclusive CDF integral J, not for the requested discrete rank sum W. Therefore both residuals are reported:

| check over N≤2,000 | max absolute difference | interpretation |
|---|---:|---|
| fast J versus direct inclusive-J stream | 8.811e-12 | identity/implementation check; numerical roundoff |
| N·J/Phi proxy versus requested C_W | 0.005312051 | finite statistic/convention gap; max over N=100,1000,2000 |
| same proxy residual restricted to N≥1,000 | 0.000545813 | decays approximately like a boundary correction, but is not zero |

This is the key scope limitation: claiming zero fast-vs-direct error for C_W would conflate W with J. The report keeps the exact requested direct values and labels the large-N Mertens rows as a proxy whose small-N calibration is visible.

## Measured trajectory

| N | C_W row | row source | T(N) |
|---:|---:|---|---:|
| 100 | 0.496783551 | direct_longdouble | -4.635866 |
| 1,000 | 0.634761472 | direct_longdouble | -9.193430 |
| 2,000 | 0.654481470 | direct_longdouble | -7.595470 |
| 10,000 | 0.666148775 | fast_Mertens_proxy | -28.147933 |
| 100,000 | 0.668123962 | fast_Mertens_proxy | -50.015576 |
| 300,000 | 0.698697063 | fast_Mertens_proxy | 142.368090 |
| 1,000,000 | 0.679304965 | fast_Mertens_proxy | 138.629679 |
| 3,000,000 | 0.682497667 | fast_Mertens_proxy | 5.762700 |
| 10,000,000 | 0.696380179 | fast_Mertens_proxy | 605.725465 |

## Loglog fit

Free least-squares fit on all measured rows with N≥10,000: C_W = α + β log log N, α=0.560337749, β=0.047635213.
The imported claim's fixed slope β=0.24 was also fit in α only: α_fixed=0.069600674.

| N | residual free (β fitted) | residual best α, β=0.24 | residual claimed 0.16+0.24loglog | residual from C=0.679 |
|---:|---:|---:|---:|---:|
| 10,000 | +0.000045286 | +0.063669668 | -0.026729658 | -0.012851225 |
| 100,000 | -0.008609017 | +0.012090403 | -0.078308923 | -0.010876038 |
| 300,000 | +0.017622527 | +0.020789488 | -0.069609839 | +0.019697063 |
| 1,000,000 | -0.006112941 | -0.020485768 | -0.110885094 | +0.000304965 |
| 3,000,000 | -0.006565128 | -0.035657072 | -0.126056398 | +0.003497667 |
| 10,000,000 | +0.003619272 | -0.040406718 | -0.130806044 | +0.017380179 |

Free-fit RMSE=0.008927848; best-α fixed-β RMSE=0.036414291; claimed-parameter RMSE=0.097457882.
The fitted β is far below 0.24, so these runs reject the stated loglog slope as a description of this trajectory. They do not establish convergence to 0.679 ± 0.002, because the sampled spikes remain larger than that band.
The fit uses the `C_W` column: its N≤2,000 rows are direct rank sums, while all N≥10,000 rows are the explicitly labeled Mertens/Jordan proxy.

## Method and scope

Direct route: next-Farey recurrence, endpoint-inclusive ranks, numpy.longdouble accumulation, N≤2,000. Fast route: numpy Möbius sieve, Mertens prefix M, quotient-block evaluation of T(x), and the Jordan-totient convolution for J; no Farey fractions are enumerated at N≥10,000.

Largest reached: N=10,000,000 by the fast route. Runtime and sieve metadata are in cw_growth_receipt.json. No value beyond 10,000,000 is extrapolated; the α,β numbers are fits only.

Source files inspected: `research_notes/imported_farey_now/FRANEL_LANDAU_LOWER_BOUND.md:15-23,49-70`, `projects/mimo-mini-project/research_notes/Mertens_NW_conjecture.md:11-24,76-78`, and `equispaced-primes/bcz-cocycle/verify_bcz_cocycle.py:86-96,160-204`.

