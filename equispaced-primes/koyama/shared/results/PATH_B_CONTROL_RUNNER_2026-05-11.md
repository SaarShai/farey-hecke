# Path B Control Runner

Date: 2026-05-11
Agent: C

## Status

Runner added: `koyama-shared/scripts/path_b_control_queue_runner.py`.

Local status: control decision incomplete. This machine still has no `gp` on
PATH and no standard `pari-elldata` directory, so B1/B2 discovery and new EC
observable computation were not run here.

## Claim

No conductor-control pass is claimed.

Allowed statement: the runner now makes B1/B2 reproducible on a future
`gp`/`pari-elldata` machine and runs the NumPy-only bootstrap gates once computed
selected-control rows are present.

Forbidden statement: rank survives B1/B2 conductor controls.

## How to run

Local gate/status check:

```bash
python3 koyama-shared/scripts/path_b_control_queue_runner.py --current-diagnostic
```

Emit exact GP packets:

```bash
python3 koyama-shared/scripts/path_b_control_queue_runner.py --emit-gp all
python3 koyama-shared/scripts/path_b_control_queue_runner.py --compute-command 389a1
```

Future GP discovery:

```bash
python3 koyama-shared/scripts/path_b_control_queue_runner.py --discover all > /tmp/path_b_b1_b2_discovery.csv
python3 koyama-shared/scripts/path_b_control_queue_runner.py --select-discovery /tmp/path_b_b1_b2_discovery.csv --select-band B1
python3 koyama-shared/scripts/path_b_control_queue_runner.py --select-discovery /tmp/path_b_b1_b2_discovery.csv --select-band B2
```

After selected controls are computed with the same normalization as
`path_b_20forms.py`, provide a CSV with:

```text
label,rank,weight,conductor,E_C1,E_C1_sq,N_zeros,error
```

Then run:

```bash
python3 koyama-shared/scripts/path_b_control_queue_runner.py --controls-csv koyama-shared/data/PATH_B_SELECTED_CONTROLS.csv --current-diagnostic
```

Default optional control paths are also auto-read if present:

- `koyama-shared/data/PATH_B_SELECTED_CONTROLS.csv`
- `koyama-shared/data/PATH_B_CONTROL_ROWS.csv`
- `koyama-shared/data/PATH_B_B1_B2_CONTROLS.csv`

## Verification on current data

Commands run:

```bash
python3 -m py_compile koyama-shared/scripts/path_b_control_queue_runner.py
python3 koyama-shared/scripts/path_b_control_queue_runner.py --emit-gp all
python3 koyama-shared/scripts/path_b_control_queue_runner.py --compute-command 389a1
python3 koyama-shared/scripts/path_b_control_queue_runner.py --current-diagnostic
```

Observed environment:

- `gp`: absent.
- Standard `pari-elldata` directories: none found.
- Loaded CSV: `koyama-shared/data/PATH_B_20FORMS.csv`.
- EC rows used: 19. `Delta` excluded.
- Bootstrap: seed `20260510`, `B = 20000`, ordinary row bootstrap.

Control matrices today:

| matrix | present | missing | verdict |
|---|---|---|---|
| B1 | rank 2: 4 | rank 0: 3, rank 1: 3 | incomplete |
| B2 | rank 3: 1 | rank 0: 2, rank 1: 2, rank 2: 2 | incomplete |
| B1+B2 | rank 2: 4, rank 3: 1 | B1 lower controls and B2 lower controls | incomplete |

Current EC diagnostic, not an acceptance claim:

| model | rank beta | bootstrap 95% CI | P(beta <= 0) | LOO beta range | max leverage | verdict |
|---|---:|---:|---:|---:|---:|---|
| rank | 0.585860 | [0.238656, 0.845991] | 0.00005 | [0.358825, 0.621127] | 0.333333 | pass only as confounded screen |
| rank + logN | -0.677256 | [-1.221404, 0.091164] | 0.95515 | [-0.786934, -0.253343] | 0.533428 | fail |
| rank + logN + interaction | 0.001435 | [-0.687660, 0.737488] | 0.60730 | [-0.317877, 0.194992] | 0.870262 | fail |

The runner output matches the prior Path B decision packet: rank-only passes
mechanically, but conductor-controlled gates fail on current data.

## Changed files

- `koyama-shared/scripts/path_b_control_queue_runner.py`
- `koyama-shared/results/PATH_B_CONTROL_RUNNER_2026-05-11.md`

No commit. No push.

## Risks

- B1/B2 cannot pass until new computed selected-control rows exist.
- The runner can discover/select labels and gate computed rows; it does not
  replace the PARI-dependent C1 computation.
- If future selected controls are sparse or singular, the correct output remains
  incomplete/fail, not a softened rank claim.
