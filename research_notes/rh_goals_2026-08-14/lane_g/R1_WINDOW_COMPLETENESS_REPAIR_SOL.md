# (RATE) R1 window-completeness repair

**Date:** 2026-08-18

**Scope:** `X=50`; `q=5,8,12`; theta endpoint; downstream R1/M2/N2/R2 audit.

**Interpreter:** `/Users/za/miniforge3/envs/pari-arb/bin/python3`, mpmath 1.4.1, `mp.dps=50` unless a receipt says otherwise.
**Data receipt:** `law_probes/r1_coset_enum_complete_X50.json`.

## 0. Verdict ledger

| Item | Verdict |
|---|---|
| Depth-12 theta enumeration | **INCOMPLETE:** 237 of the exact 263 keys; 26 missing. |
| Required depths 16/18/20 | In the all-integer quotient-state replay, finite `q=5,8,12` key sets are identical at both increments. Theta is **not** saturated there: `245 -> 249 -> 253`. The literal script completed these depths only for `q=12`; see §2.1. |
| Theta saturation | **CERTIFIED-FINITE and exact:** 263 keys at depth 26; the same key set occurs at depths 28 and 30; it equals the independently defined 263-key arithmetic window. |
| Finite-q saturation | **CERTIFIED-FINITE within the current in-window transition/canonicalization regime:** 428, 330, 318 keys for `q=5,8,12`. Global completeness against paths that leave `|C|<=50` and later re-enter is **CONJECTURAL**, because `r1_coset_enum.py:17-25,152-157` does not prove that prune safe. |
| Old “all uses were one-sided lower-mass estimates” explanation | **FALSE.** Raw positive masses were undercounts, but R1 rank matching is not monotone, the empirical `0.26` was used as an upper ceiling, N2 target undercount made surjectivity easier, and R2 omitted positive unmatched-theta mass. Corrected directions are audited in §5. |
| BANKED theorem-level conclusion | **NO FLIP.** The Ford/Stieltjes tail theorem is independent of this enumeration; N2-finite remains refuted; N2-global and RATE remain conjectural/open. Several published numerical measurements do change. |

No finite computation below is promoted to a global theorem. Bounds are rounded up when used as bounds; margins are rounded down.

## 1. Reproduction of the defect

At theta, the exact target is

\[
 \mathcal K_{\theta,50}
 =\{(2n,r):1\le n\le25,\ 0\le r<2n,\ (n,r)=1,\ n+r\equiv1\pmod2\}.
\]

`N1N3_PROMOTION_EXECUTION_SOL.md:228-243` cites the machine-verified fixed-`C` count and gives

\[
 |\mathcal K_{\theta,50}|=\sum_{n=1}^{25}\varphi(2n)=263.
\]

Its explicit missing depth-13 target is `(C,D mod C)=(26,14)` (`N1N3_PROMOTION_EXECUTION_SOL.md:245-260`).

Executed from the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research_notes/rh_goals_2026-08-14/lane_g/law_probes /Users/za/miniforge3/envs/pari-arb/bin/python3 - <<'PY'
from math import gcd
from mpmath import mp
import r2_drift as d
mp.dps=80; X=mp.mpf(50); depth=12
expected={(2*n,r) for n in range(1,26) for r in range(2*n)
          if gcd(n,r)==1 and (n+r)%2==1}
th,_=d.enumerate_with_words(None,X,depth)
got={(int(round(float(k[0]))),int(round(float(k[1])))) for k in th}
missing=sorted(expected-got)
print(f'complete_theta={len(expected)} bfs_theta={len(got)} missing={len(missing)} extra={len(got-expected)}')
print('first_missing=',missing[:8])
for q in (32,48):
    found,_=d.enumerate_with_words(q,X,depth); claimed=set()
    for key,(ac,w,M) in sorted(found.items(),key=lambda kv:kv[1][0]):
        tk,ct=d.theta_key(w,X)
        if tk is not None and tk in th and tk not in claimed: claimed.add(tk)
    print(f'q={q} bfs_source={len(found)} claimed_in_incomplete_theta={len(claimed)} complete_theta={len(expected)} cardinality_deficit={len(expected)-len(found)}')
PY
```

Output:

```text
complete_theta=263 bfs_theta=237 missing=26 extra=0
first_missing= [(26, 12), (26, 14), (28, 13), (28, 15), (30, 14), (30, 16), (32, 15), (32, 17)]
q=32 bfs_source=253 claimed_in_incomplete_theta=237 complete_theta=263 cardinality_deficit=10
q=48 bfs_source=241 claimed_in_incomplete_theta=237 complete_theta=263 cardinality_deficit=22
```

Thus the depth-12 target was not merely missing multiplicity: it omitted 26 distinct canonical keys, including minimum-depth-13 classes.

## 2. Saturation certificate

### 2.1 All-integer quotient-state replay

The literal word-tree retains every relator-equivalent word. Direct invocations of the requested script at `q=5,8`, depth 16 did not finish in a bounded rerun; consequently, the literal-script part of the requested depth-16/18/20 rerun is **NOT COMPLETED** for those two groups. This is a performance failure, not evidence of saturation. The certificate below is an explicitly identified quotient-state replay, not a claim that those infeasible literal runs completed.

Executed bounded rerun:

```bash
for q in 5 8; do
  PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/gtimeout --signal=TERM 10s \
    /Users/za/miniforge3/envs/pari-arb/bin/python3 \
    research_notes/rh_goals_2026-08-14/lane_g/law_probes/r1_coset_enum.py \
    --q "$q" --X 50 --max-depth 16
  rc=$?
  echo "q=$q requested_depth=16 bounded_run_exit=$rc timeout_seconds=10"
done
```

Output (empty script stdout before termination, followed by the shell receipt):

```text
q=5 requested_depth=16 bounded_run_exit=124 timeout_seconds=10
q=8 requested_depth=16 bounded_run_exit=124 timeout_seconds=10
```

Depths 18 and 20 were not attempted literally for these groups after depth 16 failed to finish. Earlier interactive attempts were manually interrupted; the bounded exit-124 receipt above is the reproducible failure authority.

The repair replays the same matrix transition on canonical bottom-row states. If the current bottom row is `(C,D)`, appending `S^m Q_lambda` gives exactly

\[
 (C,D)\longmapsto
 \left(\lambda(D+mC),-\frac C\lambda\right).
\]

Replacing `D` by `D+bC` shifts `m` by `b`. The apparent extra quotient transition with effective raw exponent zero is harmless for cumulative keys: if `M=UQ`, then `MQ=UQ^2=-U`, and a right translation removes the last `S`-power of `U`, yielding the same key as a shorter `Q`-ending prefix already in the cumulative set. Thus ranging over every integer `m` satisfying `|lambda(D+mC)|<=50` defines the canonical all-integer in-window quotient graph and removes duplicate quotient states.

This graph is not claimed identical at every depth to the literal script's *capped* raw-word graph: the script also imposes `|m|<=m_max`. The default caps are `34,31,29,29` for `q=5,8,12,theta`, while the largest absolute exponent among the stored final witnesses is `19,14,13,12`; that witness fact does not prove the cap redundant for every possible path. Equality with the literal script is established only at the feasible cross-check depths in §2.2. Nor does the replay prove that an out-of-window state cannot later re-enter. Both stronger global claims remain **CONJECTURAL**.

Executed command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research_notes/rh_goals_2026-08-14/lane_g/law_probes /Users/za/miniforge3/envs/pari-arb/bin/python3 - <<'PY'
from mpmath import mp
import hashlib, r1_coset_enum as r
mp.dps=50; X=mp.mpf(50)
def canon(C,D):
 if C<0:C,D=-C,-D
 if abs(C)<mp.mpf(10)**(-20):return None
 b=int(mp.floor(D/C)); D-=b*C
 if D<0:D+=C
 if D>=C:D-=C
 if D<C*mp.mpf(10)**(-25) or C-D<C*mp.mpf(10)**(-25):D=mp.mpf(0)
 return (mp.nstr(C,18),mp.nstr(D,18)),C,D
def H(K):return hashlib.sha256('\n'.join(a+'|'+b for a,b in sorted(K)).encode()).hexdigest()
def run(q, depths):
 lam=r.lam_of_q(q); k,C,D=canon(lam,mp.mpf(0)); F={k:(C,D)}; fr={k}; snap={}
 for d in range(2,max(depths)+1):
  nf=set()
  for k in fr:
   C,D=F[k]; lo=int(mp.ceil((-X/lam-D)/C)); hi=int(mp.floor((X/lam-D)/C))
   for m in range(lo,hi+1):
    z=canon(lam*(D+m*C),-C/lam)
    if z and z[0] not in F:F[z[0]]=z[1:];nf.add(z[0])
  fr=nf
  if d in depths:snap[d]=set(F)
 prev=None
 for d in depths:
  K=snap[d]; print(f'q={"inf" if q is None else q} depth={d} n={len(K)} hash={H(K)} equal_prev={None if prev is None else K==prev} add={None if prev is None else len(K-prev)} drop={None if prev is None else len(prev-K)}')
  prev=K
for q,ds in ((5,(16,18,20)),(8,(16,18,20)),(12,(16,18,20)),(None,(16,18,20,22,24,26,28,30))):run(q,ds)
PY
```

Output:

```text
q=5 depth=16 n=428 hash=5bda2a563d8d515e3ab972b926aeaddb87423789c0587e0ac104a17b47000ea6 equal_prev=None add=None drop=None
q=5 depth=18 n=428 hash=5bda2a563d8d515e3ab972b926aeaddb87423789c0587e0ac104a17b47000ea6 equal_prev=True add=0 drop=0
q=5 depth=20 n=428 hash=5bda2a563d8d515e3ab972b926aeaddb87423789c0587e0ac104a17b47000ea6 equal_prev=True add=0 drop=0
q=8 depth=16 n=330 hash=3cd2ae481ff049cdbc906b093612a03fa861656743f59b66d76924a35b066f11 equal_prev=None add=None drop=None
q=8 depth=18 n=330 hash=3cd2ae481ff049cdbc906b093612a03fa861656743f59b66d76924a35b066f11 equal_prev=True add=0 drop=0
q=8 depth=20 n=330 hash=3cd2ae481ff049cdbc906b093612a03fa861656743f59b66d76924a35b066f11 equal_prev=True add=0 drop=0
q=12 depth=16 n=318 hash=7d14b02cb7a0ec7cf3171a173b474f0ad6b2b2ecd977298dd63f9fc4b14af126 equal_prev=None add=None drop=None
q=12 depth=18 n=318 hash=7d14b02cb7a0ec7cf3171a173b474f0ad6b2b2ecd977298dd63f9fc4b14af126 equal_prev=True add=0 drop=0
q=12 depth=20 n=318 hash=7d14b02cb7a0ec7cf3171a173b474f0ad6b2b2ecd977298dd63f9fc4b14af126 equal_prev=True add=0 drop=0
q=inf depth=16 n=245 hash=8adef6c8e7f1beedcf77a09eec41fd8cf7184cc4e45dfb1aebd34f2dc323c1f2 equal_prev=None add=None drop=None
q=inf depth=18 n=249 hash=2bd4e549863882eda8f06924e4e2fa07ee0ac57857c35de5604508df27d40db2 equal_prev=False add=4 drop=0
q=inf depth=20 n=253 hash=ea2f94de8eb51602799176ea1c8fe14169c45aba86bc4cf294d74f7f0ef9241e equal_prev=False add=4 drop=0
q=inf depth=22 n=257 hash=0e87a31946d649651b5ec382d99324296748d77b7043bdb2207ebe8ab3818b2d equal_prev=False add=4 drop=0
q=inf depth=24 n=261 hash=e10954b37b92b9275b95a16522849af4016298fd0201fc781c6902d3f5533ab6 equal_prev=False add=4 drop=0
q=inf depth=26 n=263 hash=6b389ddca1dd5e18035470512ec420712f187ca95abc5dc1b85c7b452319e819 equal_prev=False add=2 drop=0
q=inf depth=28 n=263 hash=6b389ddca1dd5e18035470512ec420712f187ca95abc5dc1b85c7b452319e819 equal_prev=True add=0 drop=0
q=inf depth=30 n=263 hash=6b389ddca1dd5e18035470512ec420712f187ca95abc5dc1b85c7b452319e819 equal_prev=True add=0 drop=0
```

### 2.2 Cross-check against the unmodified word enumerator

The unmodified script is feasible through the largest witness depths. Its exact key sets agree with the quotient replay:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research_notes/rh_goals_2026-08-14/lane_g/law_probes \
  /Users/za/miniforge3/envs/pari-arb/bin/python3 - <<'PY'
from mpmath import mp
import hashlib, r1_coset_enum as r
mp.dps=50
def H(K):
    return hashlib.sha256('\n'.join(a+'|'+b for a,b in sorted(K)).encode()).hexdigest()
for q, depths in ((5,(8,)),(8,(11,)),(12,(16,18,20)),(None,(26,))):
    for depth in depths:
        found,reached=r.enumerate_c_spectrum(q,mp.mpf(50),max_depth=depth)
        print(f'q={"inf" if q is None else q} requested_depth={depth} '
              f'depth_reached={reached} n_keys={len(found)} sha256={H(found)}')
PY
```

Output:

```text
q=5 requested_depth=8  depth_reached=8  n_keys=428 sha256=5bda2a563d8d515e3ab972b926aeaddb87423789c0587e0ac104a17b47000ea6
q=8 requested_depth=11 depth_reached=11 n_keys=330 sha256=3cd2ae481ff049cdbc906b093612a03fa861656743f59b66d76924a35b066f11
q=12 requested_depth=16 depth_reached=16 n_keys=318 sha256=7d14b02cb7a0ec7cf3171a173b474f0ad6b2b2ecd977298dd63f9fc4b14af126
q=12 requested_depth=18 depth_reached=18 n_keys=318 sha256=7d14b02cb7a0ec7cf3171a173b474f0ad6b2b2ecd977298dd63f9fc4b14af126
q=12 requested_depth=20 depth_reached=20 n_keys=318 sha256=7d14b02cb7a0ec7cf3171a173b474f0ad6b2b2ecd977298dd63f9fc4b14af126
q=inf requested_depth=26 depth_reached=26 n_keys=263 sha256=6b389ddca1dd5e18035470512ec420712f187ca95abc5dc1b85c7b452319e819
```

The final witness depths are 6, 8, 9, and 25 for `q=5,8,12,theta`. The quotient frontier becomes empty at depths 7, 9, 10, and 26 respectively. The q=12 output above came from literal requested-depth runs; q=5 and q=8 are shallow feasible cross-checks. The theta unmodified cross-check stored in the JSON is through depth 26; the depth-16/18/20/28/30 rows in §2.1 are quotient-replay snapshots.

### 2.3 Saturation table

| group | `K_16` | `K_18` | `K_20` | continuation | two identical increments | final key hash |
|---|---:|---:|---:|---|---|---|
| `q=5` | 428 | 428 | 428 | frontier empty at 7 | `16=18=20` | `5bda2a...00ea6` |
| `q=8` | 330 | 330 | 330 | frontier empty at 9 | `16=18=20` | `3cd2ae...66f11` |
| `q=12` | 318 | 318 | 318 | frontier empty at 10 | `16=18=20` | `7d14b0...af126` |
| theta | 245 | 249 | 253 | `K_22=257`, `K_24=261`, `K_26=263`, `K_28=K_30=263` | `26=28=30` | `6b389d...e819` |

For theta, converting every final string key to its integer pair gives exact set equality with $\mathcal K_{\theta,50}$: expected 263, enumerated 263, missing 0, extra 0. This arithmetic equality, not depth repetition alone, is the completeness authority for theta.

## 3. Corrected dataset receipt

`law_probes/r1_coset_enum_complete_X50.json` contains:

- source-script SHA-256, repository HEAD, interpreter, mpmath version, precision, cutoff, and canonicalization tolerances;
- the key-set hash serialization contract (sorted `C|D` lines, UTF-8, SHA-256), the per-group script-default `m_max`, and maximum exponent among stored witnesses;
- every requested-depth count, exact key-set SHA-256, equality flag, and symmetric-difference count;
- the quotient-frontier history through emptiness;
- every canonical `(C,D mod C)` key, high-precision `|C|`, a word witness, its depth, and the full witness matrix;
- the exact theta formula and its `263=263`, missing-zero, extra-zero check.

Generation output:

```text
wrote=research_notes/rh_goals_2026-08-14/lane_g/law_probes/r1_coset_enum_complete_X50.json bytes=954586 sha256=c1efc1336b1c2a1ccdcb9698653442788270e0f1466738b119d747f2acacaf20
q=5 n=428 max_witness_depth=6 frontier_empty=7 sha256=5bda2a563d8d515e3ab972b926aeaddb87423789c0587e0ac104a17b47000ea6
q=8 n=330 max_witness_depth=8 frontier_empty=9 sha256=3cd2ae481ff049cdbc906b093612a03fa861656743f59b66d76924a35b066f11
q=12 n=318 max_witness_depth=9 frontier_empty=10 sha256=7d14b02cb7a0ec7cf3171a173b474f0ad6b2b2ecd977298dd63f9fc4b14af126
q=inf n=263 max_witness_depth=25 frontier_empty=26 sha256=6b389ddca1dd5e18035470512ec420712f187ca95abc5dc1b85c7b452319e819
theta_exact={'expected_count': 263, 'enumerated_count': 263, 'exact_integer_keyset_equal': True, 'missing_count': 0, 'extra_count': 0}
```

## 4. Published-number audit

### 4.1 R1

#### X=80 validation percentages

The published `1.20%, 1.29%, 1.33%, 1.57%, 2.05%, 2.08%` at `q=8,12,16,24,32,48` (`LAW_R1_COSET_STRUCTURE.md:142-167`) are **unchanged numerically**: they are q-only `X=80` comparisons and do not consume the theta `X=50` list. The old inference that shallow repeated output established completeness is withdrawn. This `X=50` repair does not supply corrected `X=80` saturation.

Also, the comparison is evaluated at `s=1.5+10^-8 i`; strict “positive-term, one-sided low” order applies on the real axis, not literally to a complex Dirichlet series. The one-sided language remains empirical at the printed offset.

#### X=50 rank proxy

The old proxy used 233 theta keys from `r1_coset_cvalues_X50.json`, not even the later 237-key depth-12 set. The following exact recomputation replaces it by the 263-key theta multiset. Rows `q=8,12` have saturated q-side inputs; rows `q=16,24,32,48` are conditional audits of their published q lists, because those q sides were not re-saturated in this task.

| q | matched share, `s=1.1`, old -> new | matched/extra, `s=1.1`, old -> new | matched share, `s=1.5`, old -> new | matched/extra, `s=1.5`, old -> new |
|---:|---:|---:|---:|---:|
| 8 | 90.87% -> 93.72% | 9.95x -> 14.92x | 98.78% -> 99.22% | 81.25x -> 127.89x |
| 12 | 87.11% -> 91.26% | 6.76x -> 10.45x | 97.94% -> 98.74% | 47.55x -> 78.68x |
| 16 | 86.50% -> 92.03% | 6.41x -> 11.54x | 97.57% -> 98.74% | 40.08x -> 78.51x |
| 24 | 90.10% -> 97.11% | 9.11x -> 33.65x | 98.10% -> 99.54% | 51.52x -> 214.19x |
| 32 | 90.82% -> 87.20% | 9.89x -> 6.81x | 98.29% -> 97.56% | 57.31x -> 40.05x |
| 48 | 92.78% -> 74.84% | 12.85x -> 2.97x | 98.70% -> 93.09% | 75.73x -> 13.46x |

The blanket “roughly 10x-90x” statement is therefore **FALSE**. Its corrected conditional range is about `3x-214x`, which is too unstable to headline. The qualitative matched-dominance observation survives in every row of this proxy, but it is not a proof and is not monotone under target enlargement.

The proxy totals and fitted slopes change as follows:

| quantity | old -> new |
|---|---|
| totals at `s=1.1`, q=8..48 | `(0.23976,0.13903,0.09516,0.04695,0.02462,0.01027)` -> `(0.22564,0.12491,0.08127,0.03803,0.02572,0.01931)` |
| totals at `s=1.5`, q=8..48 | `(0.08532,0.04012,0.02404,0.01090,0.00583,0.00250)` -> `(0.08438,0.03919,0.02312,0.01033,0.00591,0.00310)` |
| unweighted log-log slope, `s=1.1` | `-1.7592 -> -1.4440` |
| unweighted log-log slope, `s=1.5` | `-1.9687 -> -1.8683` |

For `q=32,48`, the complete theta list is longer than the published q list, so the old assertion “the q list is always longer” is false; the extra class is theta-side there. At `q=24`, the published q list still has 276 entries versus theta's 263.

#### Positive partial-window masses

Theta changes from

```text
X'=10: 0.1752381195 -> 0.1893603248
X'=20: 0.086706...  -> 0.1008281393
X'=30: 0.047036...  -> 0.0542400383
X'=40: 0.021720...  -> 0.0245443876
```

The newly included saturated `q=5` row is

```text
0.31375877745171454351, 0.15356171150262869179,
0.08616147068484235758, 0.03501575555806839256
```

at `X'=10,20,30,40`. It exceeds every old row in every column. Thus the empirical uniform ceiling changes from `<=0.26` to the UP-rounded `<=0.32` over the repaired `q=5,8,12,theta` set. This is still only an enumerated partial-window observation, not a full-tail majorant.

### 4.2 M2's 25x comparison

`LAW_M2_TAIL_MAJORANT_DRAFT.md:63-88` used

\[
 T(10,1.1)=6.4357649136979711442\ldots < 6.435764913697972
\]

and divided by the old UP-rounded empirical `0.26`:

| comparison | old -> new |
|---|---|
| comparison denominator | UP-rounded `0.26` -> exact `0.3137587774517145...` at saturated `q=5` |
| displayed empirical ceiling over repaired `q=5,8,12,theta` | `0.26 -> 0.32` (UP) |
| slack against exact measured mass | `24.75x -> 20.51x` |
| slack against displayed ceiling | `24.75x -> 20.11x` |

The “about 25x” numeric is false; the corrected finite-window comparison is “about 20x against this repaired measured partial mass.” It is **not** a lower bound on slack against the unknown full tail, because the finite-window mass remains an undercount of that tail. The analytic candidate majorant is unchanged. More importantly, the later Ford/Stieltjes bound in `M2_FORD_PACKING_REFEREE.md:128-148` does not consume this comparison at all.

Two further references to the old `0.26` were found. `M1_COSET_STRATEGY_SOL.md:354-359` uses it only to say that an empirical partial window cannot discharge M1-L or M2: `0.26` is invalidated, and `0.32` is the least UP-rounded replacement demonstrated on the repaired `q=5,8,12,theta` set, but no uniform `q<=48` ceiling is certified because `q=16,24,32,48` were not re-saturated. The negative conclusion is unchanged. `RATE_NOTEGRAPH_REFEREE_AUDIT.md:86-95,270-279` uses `0.26` while demanding that it never be called a full-tail majorant: the same scoped `0.32` replacement and non-uniformity caveat apply, while that demanded classification is unchanged. No other true consumer of `r1_coset_cvalues_X50.json` was found by the final dependency sweep.

### 4.3 N2's 237/263

Two distinct ratios must not be conflated:

| statement | old -> new |
|---|---|
| theta enumerator coverage | `237/263 = 90.11%` at depth 12 -> `263/263 = 100%` at depth 26, repeated at 28 and 30 |
| q=32,48 depth-12 source onto target | claimed `237/237` -> actual `237/263`; 26 targets remain unclaimed |

Therefore the repaired target dataset does **not** rescue N2-finite. It strengthens its negation. N2-global remains **CONJECTURAL** under corrected coset-level M1.

### 4.4 R2 matched/escaping split

`LAW_R2_RATE_LEMMA_DRAFT.md:185-205` used a depth-12 q source and the same incomplete depth-12 theta target. Replacing the target by all 263 exact theta keys gives:

| q | source | matched old -> new | q-escaping old -> new | theta-unmatched old -> new |
|---:|---:|---:|---:|---:|
| 12 | 318 | 204 -> 204 | 114 -> 114 | 33 -> 59 |
| 16 | 296 | 224 -> 224 | 72 -> 72 | 13 -> 39 |
| 24 | 276 | 236 -> 236 | 40 -> 40 | 1 -> 27 |
| 32 | 253 | 237 -> 237 | 16 -> 16 | 0 -> 26 |
| 48 | 241 | 237 -> 237 | 4 -> 4 | 0 -> 26 |

No depth-12 q word maps to any of the 26 newly admitted theta keys. The `q=12` row has a saturated q-side set in this repair. The other four rows are corrected-target audits conditional on their old depth-12 q sources, not fully re-saturated q-side results.

At `sigma=1.1`, the missing theta keys contribute positive mass

\[
 \Delta E_\theta=0.0100563782113606042\ldots.
\]

Conditional on holding every other old R2 component fixed, the numerical assembly changes:

| q | old printed epsilon -> corrected UP-rounded epsilon | measured `D` | still majorizes? |
|---:|---:|---:|---|
| 12 | `0.6900 -> 0.7046` | 0.05521 | yes |
| 16 | `0.4645 -> 0.4791` | 0.05062 | yes |
| 24 | `0.2042 -> 0.2187` | 0.03617 | yes |
| 32 | `0.0973 -> 0.1118` | 0.02506 | yes |
| 48 | `0.0376 -> 0.0521` | 0.01378 | yes |

These remain numerical draft assemblies, not proved RATE bounds. The old q=32/48 zero-unmatched input was false, so the old displayed epsilon values cannot remain receipts for the complete target.

The R2 draft's header references to the empirical `0.26` ceiling (`LAW_R2_RATE_LEMMA_DRAFT.md:6-13`) and its `237`-target/onto claims (`:201-205,366`) are therefore stale. Under the deliverable-only write boundary they are audited here rather than edited in place: read `0.32` only as the repaired UP-rounded partial-window observation, and replace the onto claim by `237/263` fixed-source coverage.

## 5. One-sidedness and BANKED conclusions

| use | verified direction after enumeration enlargement | consequence |
|---|---|---|
| R1 positive real-axis partial mass | Missing keys decrease the sum. | Old partial masses were lower estimates. Treating their maximum as an upper empirical ceiling was unsafe; `0.26` fails after adding q=5. |
| R1 rank-matching proxy | **Not one-sided.** New theta entries change pairings and can raise or lower totals. | Retire “10x-90x” and the old slopes; use the conditional recomputation only as measurement. |
| M2 `T/measured` finite-window comparison | An undercounted denominator inflates the ratio. | `25x` decreases to about `20x` for the repaired measured window; this is not a lower bound on full-tail slack. The analytic/Ford upper bounds do not weaken. |
| N2 onto test | An undercounted target makes surjectivity easier. | `237/237` was a false onto test; corrected fixed-source coverage is `237/263`. |
| R2 unmatched-theta mass | Omitted terms decrease the positive `E_theta` charge. | Corrected numerical epsilon goes up. It still exceeds measured `D` in the audited rows. |
| Ford/Stieltjes two-tail bound | Independent of enumeration and matching. | Paper-level N3/RATE-use conclusion unchanged. |

Accordingly:

1. **No BANKED theorem-level conclusion flips.** The paper-level Ford tail bound remains; its proof uses `A_Gamma(Y)<=Y^2`, not the `X=50` data.
2. **N2-finite remains REFUTED**, now with a complete target receipt.
3. **N2-global, N1-RATE, corrected M1, N4-scale, M3, and assembled RATE remain CONJECTURAL/open.** No numerical repair promotes them.
4. **Several non-theorem numerical claims do flip or change:** R1's rank headline/slopes, the `0.26` ceiling, M2's `25x`, R2's unmatched split, and the fixed-window epsilon values.
5. The expected “no flip because every use was one-sided” rationale is therefore **NEGATED**. The corrected reason no theorem flips is that the only banked theorem-level tail conclusion is enumeration-independent, while the affected R1/R2/N2 items were measurements, drafts, or already-refuted/conjectural statements.

## 6. Residual limits

- Theta completeness is exact. Finite `q=5,8,12` completeness is relative to the current in-window transition regime; the no-outside-then-reentry lemma is unproved and hence **CONJECTURAL**.
- R2 `q=16,24,32,48` source lists were not re-saturated in this task. Their corrected rows above hold the published depth-12 sources fixed and repair only the target.
- The JSON uses 18-digit canonical keys because that is the script's key contract. High-precision matrix/witness fields are provided so a later exact-algebraic checker can replace floating canonicalization.
- No existing R1/M2/R2 note or script was edited. The only new files are this report and the specified JSON receipt.
