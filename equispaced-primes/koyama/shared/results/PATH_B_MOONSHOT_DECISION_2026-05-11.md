# Path B Moonshot Decision Packet

Date: 2026-05-11
Agent: C

## Status

External run required. Local fallback complete.

PARI/GP availability on this machine:

- `gp`: not on PATH.
- Python `cypari2`: unavailable.
- Standard `pari-elldata` directories checked: absent at `/opt/homebrew/share/pari/elldata`, `/usr/local/share/pari/elldata`, `/usr/share/pari/elldata`, `/opt/local/share/pari/elldata`.

Therefore B1/B2 discovery and new EC observable computation were not run here. This packet gives the external-run instructions plus the local NumPy-only failure-to-promote diagnostic from the stored EC CSV.

## Claim

No rank-survival claim is supported from the current Path B data.

Current decision:

- The stored EC data contain an upward rank-only signal.
- The signal is conductor-confounded.
- After adding `log(conductor)`, the rank coefficient fails the requested acceptance gates.
- B1/B2 are not decision-complete locally because the required conductor-matched lower-rank controls are absent.

Allowed sentence: current Path B remains a research hypothesis; rank-vs-conductor is undecided until B1/B2 controls are computed externally.

Forbidden sentence: rank survives conductor controls.

## Evidence

Input set:

- `koyama-shared/data/PATH_B_20FORMS.csv`
- `koyama-shared/results/PATH_B_CONTROL_QUEUE_2026-05-10.md`
- `koyama-shared/results/PATH_B_DECONFOUNDING_2026-05-10.md`
- `koyama-shared/results/PATH_B_LOCAL_AUDIT_2026-05-10.md`
- `koyama-shared/scripts/path_b_20forms.py`
- `koyama-shared/scripts/rank4_5_extension.py`

Local data used for diagnostics:

- 19 EC rows.
- `Delta` excluded.
- Response: `E_C1_sq`.
- `logNc = log(conductor) - mean(log(conductor))`.
- `mean(log(conductor)) = 4.174328568476445`.

Rank/conductor lock:

- `corr(rank, logN) = 0.9721071164173819`, `p = 3.8450334139788044e-12`.
- `corr(rank, conductor) = 0.6513483564324527`, `p = 0.0025196346291354805`.

Current conductor-band matrix:

| band | range | present rows | missing controls |
|---|---:|---|---|
| B1 | 350-650 | rank 2: `389a1`, `433a1`, `446d1`, `571b1` | 3 rank-0 + 3 rank-1 |
| B2 | 4500-5600 | rank 3: `5077a1` | 2 rank-0 + 2 rank-1 + 2 rank-2 |
| B3 | 18760-20735 | none | rank-4 candidate controls |
| B4 | 204108-225592 | none | rank-4 candidate controls |
| B5 | 222724-246168 | none | rank-4 candidate controls |

Acceptance-gate diagnostic, row bootstrap seed `20260510`, `B = 20000`, 95% empirical CI:

| model | rank beta | bootstrap 95% CI | P(beta <= 0) | LOO beta range | max leverage | verdict |
|---|---:|---:|---:|---:|---:|---|
| `y ~ 1 + rank` | 0.585860 | [0.238656, 0.845991] | 0.00005 | [0.358825, 0.621127] | 0.333333 | passes only as confounded screen |
| `y ~ 1 + rank + logNc` | -0.677256 | [-1.221404, 0.091164] | 0.95515 | [-0.786934, -0.253343] | 0.533428 | fail |
| `y ~ 1 + rank + logNc + rank:logNc` | 0.001435 | [-0.687660, 0.737488] | 0.60730 | [-0.317877, 0.194992] | 0.870262 | fail |

Fit comparison:

| model | R2 | RMSE |
|---|---:|---:|
| rank only | 0.640938 | 0.399740 |
| logN only | 0.767247 | 0.321840 |
| rank + logNc | 0.814362 | 0.287426 |
| interaction | 0.873223 | 0.237527 |

The accepted rank gate requires `beta > 0`, CI lower endpoint `> 0`, `P(beta <= 0) <= 0.025`, every LOO beta `> 0`, and leverage `< 0.50`. The conductor-controlled models fail. The additive model also exceeds the leverage gate; the interaction model is anchored by `5077a1`.

## External-Run Packet

Run on a machine with `gp` and `pari-elldata`.

Preflight:

```bash
gp -q --default parisizemax=4G <<'GP'
default(realprecision, 50);
print("ellsearch389_count,", #ellsearch(389));
E=ellinit("5077a1");
print("5077a1,rank,", ellanalyticrank(E)[1], ",N,", ellglobalred(E)[1]);
GP
```

Discover B1 controls:

```bash
gp -q --default parisizemax=4G <<'GP'
default(realprecision, 50);
for(N=350,650,
  C=ellsearch(N);
  for(i=1,#C,
    lab=C[i][1];
    E=ellinit(lab);
    r=ellanalyticrank(E)[1];
    if(r<=1, print(lab,",",r,",",ellglobalred(E)[1]))
  )
)
GP
```

Discover B2 controls:

```bash
gp -q --default parisizemax=4G <<'GP'
default(realprecision, 50);
for(N=4500,5600,
  C=ellsearch(N);
  for(i=1,#C,
    lab=C[i][1];
    E=ellinit(lab);
    r=ellanalyticrank(E)[1];
    if(r<=2, print(lab,",",r,",",ellglobalred(E)[1]))
  )
)
GP
```

Select controls:

- B1: nearest available 3 rank-0 and 3 rank-1 controls in 350-650 around `389a1`, `433a1`, `446d1`, `571b1`.
- B2: nearest available 2 rank-0, 2 rank-1, and 2 rank-2 controls in 4500-5600 around `5077a1`.

Compute each selected EC row with the same observable as `path_b_20forms.py`:

```text
K = 10^4
N_zeros = 200
mu_E(p) = -a_p
mu_E(p^2) = p
mu_E(p^k) = 0 for k >= 3
c_K(rho) = sum_{n <= K} mu_E(n) exp(-n/K) n^{-rho}, rho = 1 + i gamma
C1 = |c_K(rho)| |L'(rho,E)| / (log K + EulerGamma)
y = E[C1^2]
```

Patch hard-coded output paths in `koyama-shared/scripts/path_b_20forms.py` or clone the helper into a scratch script before running. Do not change normalization.

Post-run gates:

- B1 alone: fit `y ~ 1 + rank` and `y ~ 1 + rank + centered_logN`.
- B2 alone: fit `y ~ 1 + rank` and `y ~ 1 + rank + centered_logN`.
- Combined B1+B2: fit `y ~ 1 + rank + centered_logN`, `y ~ 1 + rank + centered_logN + rank:centered_logN`, and `y ~ 1 + rank + conductor_tier`.
- Bootstrap: seed `20260510`, `B = 20000`, row bootstrap, empirical 95% CI.
- Accept only if rank beta `> 0`, CI lower endpoint `> 0`, `P(beta <= 0) <= 0.025`, every LOO beta `> 0`, and max leverage `< 0.50`.

Decision rule:

- If B1 and B2 conductor-controlled gates pass: report a rank-vs-conductor survival candidate.
- If B1 passes and B2 fails or is incomplete: report local rank-2 evidence only, no broad rank-isolated theorem.
- If additive conductor-controlled B1+B2 fails: report conductor-confounded effect.
- If only the interaction model is positive: report conductor-dependent slope, not rank isolation.

## Verification

Commands/checks run locally:

- Read required queue/audit/deconfounding/data/script files.
- `command -v gp`: no result.
- Python environment check: `numpy` and `scipy` present; `pandas`, `statsmodels`, `cypari2` absent.
- Checked standard `pari-elldata` directories listed above: absent.
- NumPy/SciPy diagnostic run from `PATH_B_20FORMS.csv` with `seed = 20260510`, `B = 20000`, row bootstrap, Delta excluded.
- `python3 -m py_compile koyama-shared/scripts/path_b_20forms.py koyama-shared/scripts/rank4_5_extension.py`: passed.

## Changed files

- `koyama-shared/results/PATH_B_MOONSHOT_DECISION_2026-05-11.md`

No commit. No push.

## Risks

- This machine cannot compute new PARI-dependent EC rows, so B1/B2 remain externally blocked.
- Bootstrap CIs depend on the stated row-bootstrap implementation; acceptance must be rerun after new rows are added.
- `5077a1` is currently a singleton rank-3/high-conductor anchor and cannot support a broad rank claim alone.
- Rank-4 candidates remain out of scope until B1/B2 are resolved and matched rank-4 controls are computed.
