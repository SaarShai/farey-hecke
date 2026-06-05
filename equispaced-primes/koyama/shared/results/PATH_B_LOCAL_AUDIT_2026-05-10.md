# Path B local audit (2026-05-10)

## Scope

This is a local audit of the Koyama GL(2) "Path B" records after resuming the
Koyama track. It uses the data present in this checkout, not reconstructed
values.

Inputs checked:

- `koyama-shared/data/PATH_B_20FORMS.csv`
- `koyama-shared/data/PHASE1_EC_RECOMPUTE.json`
- `koyama-shared/data/RANK3_5077A1.json`
- `koyama-shared/data/PHASE1_500ZEROS_CORRECTED.json`
- `formal-conjectures/DPAC_full.lean`
- `formal-conjectures/DPAC_aristotle_result.tar.gz`

The current machine does not have `gp`, `lean`, or `lake`, so this audit does
not rerun PARI or rebuild Aristotle's Lean artifact. It only recomputes
statistics from stored local CSV/JSON data.

## DPAC status

Aristotle project `59d181d5-b207-4882-a5ba-0786ec51d361` returned
`COMPLETE_WITH_ERRORS`.

Downloaded outputs:

- `formal-conjectures/DPAC_aristotle_result.tar.gz`
- `formal-conjectures/DPAC_full.lean`
- `formal-conjectures/DPAC_aristotle_result_extract/`

Mathematical content is only a checkpoint:

- Main DPAC theorem remains `sorry`.
- LI-to-DPAC bridge `dpac_of_LI` remains `sorry`.
- Aristotle claims one auxiliary real-analysis growth-comparison lemma is
  sorry-free, but local rebuild was not possible because `lake`/`lean` are not
  installed.

Conclusion: no new DPAC theorem. Treat the artifact as a formalization scaffold
and a record of missing prerequisites, not as closure.

## Path B CSV audit

`koyama-shared/results/path_b_analysis.md` says it could not access the CSV.
That statement is stale for this checkout: `PATH_B_20FORMS.csv` is present and
has 20 rows.

Per `koyama-shared/README.md`, the Delta row in this CSV is invalid. The
statistics below use the 19 EC rows only.

### EC class means from `PATH_B_20FORMS.csv`

| rank | n | mean E[C1^2] | sd | min | max |
|---:|---:|---:|---:|---:|---:|
| 0 | 8 | 1.915635 | 0.190041 | 1.667322 | 2.179215 |
| 1 | 6 | 2.100339 | 0.289129 | 1.873493 | 2.643024 |
| 2 | 4 | 2.680774 | 0.306595 | 2.488029 | 3.138691 |
| 3 | 1 | 4.647380 | n/a | 4.647380 | 4.647380 |

Rank is visible, but rank 0 and rank 1 overlap strongly. The rank 3 point is a
single high-leverage curve.

### Regression checks, EC rows only

Target variable: `E_C1_sq`.

| model | coefficients | R^2 | RMSE |
|---|---|---:|---:|
| rank only | `1.754630 + 0.585860 rank` | 0.640938 | 0.399740 |
| log conductor only | `0.766384 + 0.362318 log(N)` | 0.767247 | 0.321840 |
| rank + log conductor | `-0.181076 - 0.677256 rank + 0.734456 log(N)` | 0.814362 | 0.287426 |
| rank + log conductor + interaction | `1.704923 - 0.649666 rank + 0.083772 log(N) + 0.155977 rank log(N)` | 0.873223 | 0.237527 |

Interpretation:

- The Path B CSV does not isolate rank from conductor.
- `log(N)` alone outperforms rank alone on these 19 EC rows.
- In the joint model, the rank coefficient flips sign because rank and
  conductor are collinear in the current design.
- The interaction model fits better but is overparameterized for 19 rows and
  especially fragile because rank 3 has only one curve.

If the single rank-3 row is removed, rank-only drops to:

`E[C1^2] = 1.868148 + 0.358825 rank`, `R^2 = 0.564626`, `RMSE = 0.247558`.

### Anchor data check

Stored higher-confidence anchors:

| source | form | rank | n zeros | E[C1^2] |
|---|---|---:|---:|---:|
| `PHASE1_EC_RECOMPUTE.json` | 37a1 | 1 | 500 | 2.189912 |
| `PHASE1_EC_RECOMPUTE.json` | 389a1 | 2 | 500 | 3.113924 |
| `RANK3_5077A1.json` | 5077a1 | 3 | 500 | 4.617200 |
| `PHASE1_500ZEROS_CORRECTED.json` | Delta | 0 | 683 | 0.950232 |

Caution: despite its filename, `PHASE1_500ZEROS_CORRECTED.json` contains huge
invalid EC values from the old EC normalization; only the Delta value should be
used from that file. This matches the warning in `C1_500_ZEROS.md` and
`PHASE1_RECOMPUTE_SUMMARY.md`.

Fitting the four anchor points `(Delta, 37a1, 389a1, 5077a1)` gives:

`E[C1^2] = 0.929080 + 1.192492 rank`, `R^2 = 0.991990`.

That is a strong visual trend, but it mixes one weight-12 Delta point with EC
points and should not be cited as an EC-only rank law.

## Updated verdict

The strong README claim

`E[C1^2] ~= 1.47 + 0.90 rank (R^2 ~= 0.998)`

is not supported by the local `PATH_B_20FORMS.csv` as an EC-only regression.

Best current statement:

1. There is a real upward rank signal in the stored data.
2. The EC-only Path B sweep cannot distinguish rank from conductor.
3. Rank-0 ECs cluster tightly enough to support within-class stability.
4. The rank-3 point is important but currently a singleton.
5. The Delta rank-0 analytic point should be treated separately from EC
   rank-0 data until the normalization bridge is made explicit.

## Next research move

Most useful next experiment:

1. Add at least two more rank-3 ECs and one or two rank-4 ECs.
2. Add rank-matched conductor controls where possible.
3. Refit `E[C1^2] ~ rank + log(N) + rank:log(N)`.
4. Only then decide whether the coefficient is genuinely rank-linear or mostly
   a conductor/low-lying-zero spacing effect.

Blocked locally: this requires PARI/GP (`gp`) and `pari-elldata`; `gp` is not
installed on this machine.
