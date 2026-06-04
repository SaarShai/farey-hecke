# Path B conductor-control queue, Agent C

Date: 2026-05-10

Scope: decision-complete run queue for a future machine with `gp` and
`pari-elldata`. No local PARI/GP was run here.

## Current decision

Path B is not accepted as a rank-isolated claim yet.

Reason: the EC-only `PATH_B_20FORMS.csv` has an upward rank signal, but it is
conductor-confounded. The deconfounding audit reports:

- `corr(rank, logN) = 0.972107`.
- `logN` alone beats rank alone.
- `rank + logN` flips the rank coefficient negative.
- `rank + logN + rank:logN` leaves rank at mean conductor essentially zero.
- `5077a1` is a singleton rank-3 point with leverage `0.870262`.

Rule for all next claims: do not say rank survives until conductor-matched
controls pass both bootstrap and leave-one-out (LOO) tests.

## Fixed observable

Use the same observable as `path_b_20forms.py`:

```text
K = 10^4
rho = 1 + i gamma
N_zeros = 200 for queue runs; 500 only for confirmation reruns
mu_E(p) = -a_p
mu_E(p^2) = p
mu_E(p^k) = 0 for k >= 3
c_K(rho) = sum_{n <= K} mu_E(n) exp(-n/K) n^{-rho}
C1 = |c_K(rho)| |L'(rho,E)| / (log K + EulerGamma)
response y = E[C1^2]
```

Exclude `Delta` from all EC rank/conductor decisions.

## Required conductor bands

| band id | conductor range | existing high-rank row | required new ranks | minimum new EC rows | purpose |
|---|---:|---|---|---:|---|
| B1 | 350-650 | rank 2: `389a1`, `433a1`, `446d1`, `571b1` | rank 0, rank 1 | 3 rank-0 + 3 rank-1 | Test rank 2 against local lower-rank controls. |
| B2 | 4500-5600 | rank 3: `5077a1` | rank 0, rank 1, rank 2 | 2 per lower-rank bucket | Decide whether `5077a1` remains high at matched conductor. |
| B3 | 18760-20735, fallback 17772-21722 | rank 4 candidate `19747a1` | rank 0 first, rank 1 next | 1 rank-0 + 1 rank-1 if available | First rank-4 control test. |
| B4 | 204108-225592, fallback 193365-236335 | rank 4 candidate `214850b1` | rank 0 first, rank 1 next | 1 rank-0 + 1 rank-1 if available | High-conductor rank-4 test. |
| B5 | 222724-246168, fallback 211001-257891 | rank 4 candidate `234446a1` | rank 0 first, rank 1 next | 1 rank-0 + 1 rank-1 if available | High-conductor rank-4 replication. |

Do not compare rank-4 candidates only against the conductor 11-61 rank-0/1
cluster. That comparison is not evidence for rank.

## Minimal crossed matrix

| conductor tier | rank 0 | rank 1 | rank 2 | rank 3 | rank 4 |
|---|---:|---:|---:|---:|---:|
| 350-650 | 3+ new | 3+ new | 4 existing | optional | n/a |
| 4500-5600 | 2+ new | 2+ new | 2+ new | 1 existing | n/a |
| near 19747 | 1+ new | 1+ new if available | optional | optional | candidate |
| near 214850 | 1+ new | 1+ new if available | optional | optional | candidate |
| near 234446 | 1+ new | 1+ new if available | optional | optional | candidate |

Decision-complete minimum for the next run: finish B1 and B2. B3-B5 are
promotion blockers for any rank-4 sentence, not blockers for deciding whether
the old rank-2/rank-3 evidence survives local conductor controls.

## Acceptance tests

Use EC rows only. Response is `E_C1_sq`.

For B1 alone:

```text
y ~ 1 + rank
y ~ 1 + rank + centered_logN
```

Accept a local rank-2 signal only if both models give:

- rank beta > 0;
- ordinary row-bootstrap 95% CI has lower endpoint > 0;
- bootstrap `P(beta <= 0) <= 0.025`;
- every LOO deletion keeps rank beta > 0;
- no single row has leverage >= 0.50 in the accepted model.

For B2 alone:

```text
y ~ 1 + rank
y ~ 1 + rank + centered_logN
```

Accept `5077a1` as a conductor-matched rank-3 elevation only if:

- the rank beta passes the same bootstrap + LOO gates;
- `5077a1` is not the only row controlling the slope after lower-rank controls
  are added;
- rank-3 remains above the matched lower-rank fitted band under LOO.

For combined B1+B2:

```text
y ~ 1 + rank + centered_logN
y ~ 1 + rank + centered_logN + rank:centered_logN
y ~ 1 + rank + conductor_tier
```

Accept a broad rank sentence only if the rank coefficient is positive and
bootstrap/LOO-stable in the additive conductor-controlled model. If only the
interaction model has a positive high-conductor slope, report that as a
conductor-dependent effect, not an isolated rank-only claim.

For B3-B5:

```text
y ~ 1 + is_candidate_rank4
```

within each narrow candidate band, then pooled:

```text
y ~ 1 + rank + conductor_tier
```

Rank 4 is publishable only after all completed rank-4 bands pass local controls
or failed/missing controls are explicitly reported as missing. A single
high-conductor rank-4 point without controls is only a candidate datum.

Bootstrap settings:

```text
seed = 20260510
B = 20000
resample unit = row
CI = empirical 2.5%, 97.5%
LOO = delete one EC row, refit full model
```

## PARI/GP discovery commands

The official PARI elliptic-curve manual says `ellinit("11a1")` retrieves a
curve from `elldata`, and `ellsearch(N)` selects curves by conductor. These
commands assume `pari-elldata` is installed.

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
    if(r<=1,
      print(lab,",",r,",",ellglobalred(E)[1])
    )
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
    if(r<=2,
      print(lab,",",r,",",ellglobalred(E)[1])
    )
  )
)
GP
```

Discover rank-4 candidate-band controls:

```bash
gp -q --default parisizemax=4G <<'GP'
default(realprecision, 50);
bands=[[18760,20735],[204108,225592],[222724,246168]];
for(b=1,#bands,
  lo=bands[b][1]; hi=bands[b][2];
  print("BAND,",lo,",",hi);
  for(N=lo,hi,
    C=ellsearch(N);
    for(i=1,#C,
      lab=C[i][1];
      E=ellinit(lab);
      r=ellanalyticrank(E)[1];
      if(r<=1,
        print(lab,",",r,",",ellglobalred(E)[1])
      )
    )
  )
)
GP
```

If a rank-4 first band has no rank-0 control, widen once:

```bash
gp -q --default parisizemax=4G <<'GP'
default(realprecision, 50);
bands=[[17772,21722],[193365,236335],[211001,257891]];
for(b=1,#bands,
  lo=bands[b][1]; hi=bands[b][2];
  print("FALLBACK_BAND,",lo,",",hi);
  for(N=lo,hi,
    C=ellsearch(N);
    for(i=1,#C,
      lab=C[i][1];
      E=ellinit(lab);
      r=ellanalyticrank(E)[1];
      if(r<=1,
        print(lab,",",r,",",ellglobalred(E)[1])
      )
    )
  )
)
GP
```

Verify named high-rank candidates before computing:

```bash
gp -q --default parisizemax=4G <<'GP'
default(realprecision, 50);
labs=["19747a1","214850b1","234446a1","19047851a1"];
for(i=1,#labs,
  lab=labs[i];
  E=ellinit(lab);
  print(lab,",rank,",ellanalyticrank(E)[1],",N,",ellglobalred(E)[1],
        ",zeros_to_2000,",#lfunzeros(E,[1e-6,2000]))
)
GP
```

## PARI/GP per-curve compute commands

Use this for each selected EC label to obtain the PARI-dependent inputs. The
Python scripts already implement the arithmetic-normalized `mu_E` and `c_K`;
this command is the exact GP side they need.

```bash
LABEL=389a1
TMAX=1000
KMAX=10000
gp -q --default parisizemax=4G <<GP
default(realprecision, 50);
E=ellinit("$LABEL");
print("META,", "$LABEL", ",", ellanalyticrank(E)[1], ",", ellglobalred(E)[1]);
Z=lfunzeros(E,[1e-6,$TMAX]);
n=min(#Z,200);
for(i=1,n, print("ZERO,",i,",",Z[i]));
forprime(p=2,$KMAX, print("AP,",p,",",ellap(E,p)));
for(i=1,n,
  v=lfun(E,1+I*Z[i],1);
  print("LPRIME,",i,",",real(v),",",imag(v))
);
GP
```

For rank-4 candidates where 200 zeros are not found by `TMAX=2000`, rerun with
`TMAX=5000` before marking the curve incomplete.

## Script use

Existing scripts to reuse after label selection:

```bash
python3 koyama-shared/scripts/path_b_20forms.py
python3 koyama-shared/scripts/rank4_5_extension.py
```

Before execution in a future environment, patch hard-coded output paths away
from `/Users/saar/Desktop/Farey-Local/experiments/` into the active checkout or
capture stdout. Do not change the normalization while doing conductor controls.

## Several-hour priority order

1. Sanity check `pari-elldata`: run `ellsearch(389)`, `ellinit("5077a1")`,
   and the named-candidate verification command.
2. Discover B1 labels, choose nearest 3 rank-0 and nearest 3 rank-1 controls
   around 389, 433/446, and 571.
3. Compute B1 controls at 200 zeros. Refit B1 immediately. If B1 fails, report
   rank-2 evidence as conductor-confounded and continue only if time remains.
4. Discover B2 labels, choose at least 2 each of rank 0, rank 1, rank 2 near
   5077.
5. Compute B2 controls at 200 zeros. Refit B2 and B1+B2. This is the main
   decision point for W2.
6. Verify and compute `19747a1` plus nearest rank-0/rank-1 controls. This is
   the first rank-4 triage because it has the smallest candidate conductor.
7. If time remains, compute `214850b1` and `234446a1` controls/candidates.
8. Skip rank 5 unless all rank-4 control work is complete and the verification
   command finds 200 zeros quickly.

## Source anchors

- `handoff-2026-05-09-followup/KOYAMA_RESEARCH_DECISION_MEMO_2026-05-10.md`
- `koyama-shared/results/PATH_B_DECONFOUNDING_2026-05-10.md`
- `koyama-shared/results/PATH_B_LOCAL_AUDIT_2026-05-10.md`
- `koyama-shared/data/PATH_B_20FORMS.csv`
- `koyama-shared/scripts/path_b_20forms.py`
- `koyama-shared/scripts/rank4_5_extension.py`
- PARI/GP elliptic-curve documentation:
  `https://pari.math.u-bordeaux.fr/dochtml/html/Elliptic_curves.html`

## Confidence

High for the compute queue and acceptance gates because they follow the local
deconfounding failure mode directly. Medium for exact future runtime because
`ellanalyticrank`, `lfunzeros`, and rank-4 candidates may be slow or unavailable
depending on the installed `pari-elldata` package.

## Risks

- `ellsearch(N)` over high-conductor fallback bands may return many curves and
  make discovery slower than the actual observable computation.
- Analytic-rank computation can dominate discovery time. Prefer nearest
  low-rank controls once enough labels are found; do not exhaustively classify
  every curve if the queue already has the required matrix.
- If B1/B2 controls are sparse, the correct result is "not decision-complete",
  not a softened rank claim.
