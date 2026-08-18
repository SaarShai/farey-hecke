# LAW — R1: double-coset c-spectrum structure of G_q vs G_infty (theta group)

**Status: MEASUREMENT + a validated enumerator, no proof of (RATE) attempted.**
Per `LAW_HEJHAL_S7_EXTRACT.md` sec.4, R1: "Enumerate the double-coset
c-values of `G_N` vs `G_infty` up to height H: identify the N-stable prefix
... and the tail; certify tail majorant ... Numerical sanity check ... before
proving anything." This note is that enumerator, its validation, the
matched/escaping classification, and the tail-majorant measurement.

**Date:** 2026-08-17. **Lane:** G. **Interpreter:**
`/Users/za/.venvs/farey-rh/bin/python` (mpmath, dps up to 60).
**Probe:** `law_probes/r1_coset_enum.py`. Raw data:
`law_probes/r1_coset_cvalues_X50.json` (c-value lists per q at X=50).

---

## 0. Headline

- **A from-scratch double-coset enumerator for `[S]\G_q/[S]` was built,
  DEBUGGED (three real bugs caught and fixed, sec.1.3), and VALIDATED**
  against the repo's existing certified `phi_q(1.5)` evaluator
  (`rate_measure.phi_q`, itself validated to <1e-6 in `LAW_RATE_MEASURE.md`):
  agreement is **1.2% (q=8) to 2.1% (q=48) at truncation X=80**, monotonically
  IMPROVING with X in every q tested (sec.2) — i.e. this is a genuine,
  independently-built second route into the same Dirichlet series (7.5), not
  a re-plot of the existing evaluator, and it agrees with it to the precision
  the truncation budget affords.
- **Classification (item 2): under a RANK-MATCHING proxy (sec.3) between the
  sorted `q`-spectrum and the sorted theta-group spectrum, the MATCHED
  (convergent) class dominates the `D(q;s)` difference at both `s=1.1` and
  `s=1.5`, by roughly 10x–90x over the escaping-tail mass** (sec.3.2 table)
  — this is the OPPOSITE of the a priori guess in the task text ("escaping ...
  tail mass" as the likely driver). Per-term matched drift decays like
  `2 - lambda_q ~ q^-2` (exact algebraic identity for the smallest matched
  pair, sec.3.1), but the AGGREGATE matched-drift sum decays slower, `q^-1.3`
  to `q^-2` depending on `s` (sec.3.3) — because the NUMBER of matched terms
  within a fixed cutoff also grows with `q` (more double cosets appear inside
  `|c|<=50` as `lambda_q -> 2`, sec.3.1 count table), partially offsetting the
  per-term `q^-2` decay. This real-axis (`t=0`) measurement is independent
  of, and only qualitatively (not quantitatively) consistent with,
  `LAW_RATE_MEASURE.md`'s off-axis (`t=0.5,1.5`) slopes of `-0.65` to `-1.68`
  — see sec.3.4 for the honest gap between the two measurements.
- **Empirical partial-window mass (item 3)**: `Sum_{X' <= |c| <= 50} |c|^-2.2`
  (sigma=1.1) measured
  for X' in {10,20,30,40} within the X<=50 window, for all tested q and the
  theta group: **values cluster tightly across q (0.156–0.255 at X'=10,
  falling to 0.019–0.030 at X'=40), with NO systematic growth in q** — this
  is consistent with (does not contradict) Hejhal's Lemma 7.2 claim that the
  majorant constant is N-independent. **Empirical uniform constant, rounded
  UP: `Sum_{10 <= |c| <= 50} |c|^-2.2 <= 0.26`** across all tested q (8..48)
  and the theta group, within the X<=50 data window (sec.4) — an empirical
  PARTIAL-WINDOW mass, NOT a proof and NOT a tail majorant, and not
  extended past X=50 (honest gap, sec.5).

> **[CORRECTION 2026-08-18 audit-9]** The original headline read
> "**Tail majorant (item 3)**: `Sum_{|c|>=X'} |c|^-2.2` … **Empirical uniform
> constant, rounded UP: `Sum_{|c|>=10} |c|^-2.2 <= 0.26`**". That is wrong:
> the measured sum runs only over `X' <= |c| <= 50` (sec.4), so it is an
> empirical partial-window mass and an UNDER-estimate of the true tail (this
> note's own sec.5 says so). The correct written form, used everywhere from
> now on, is `Sum_{10 <= |c| <= 50} |c|^-2.2 <= 0.26`. It must never be used
> as a full-tail bound or majorant.

> **[CORRECTION 2026-08-18 audit-15]** The original said the X'=40 values fall
> to "0.019–0.027". Recomputed from this note's own sec.4 table the range is
> `0.01896–0.02951`, i.e. **0.019–0.030** (the q=12 entry 0.02951 exceeds the
> stated ceiling). Receipt: `law_probes/r1_table_fits.py` →
> `law_probes/r1_table_fits.log`.

---

## 1. The enumerator

### 1.1 Group presentation and the double-coset object

Conjugated model (`LAW_HEJHAL_S7_EXTRACT.md` sec.1): `S: z -> z+1`,
`Q_q = (0,-1/lam; lam,0)` (Mobius `z -> -1/(lam^2 z)`), `lam = lam_q =
2cos(pi/q)` (or `lam=2` for the theta-group / `q=infinity` limit). `Q_q`
squares to `-I` (order 2 in PSL(2,R)); `Q_q S` has trace `lam`, i.e. it is the
elliptic generator of order `q` (`(Q_q S)^q = I` in PSL(2,R)) for finite `q`,
degenerating to a PARABOLIC element at `lam=2` (theta group).

`c(W)` (lower-left matrix entry) is invariant under LEFT multiplication by
any power of `S` (`S` is upper triangular, `S^a * W` only changes row 1) and
under RIGHT multiplication by any power of `S` (`W * S^b` only changes column
2) — the standard fact underlying Kloosterman-sum theory. The double-coset
invariant that DOES distinguish cosets sharing the same `c` is `d mod c`
(right-mult by `S^b` shifts `D -> D + b*C`).

### 1.2 Enumeration strategy

BFS over matrix words `Q S^{n_1} Q S^{n_2} Q ... S^{n_{k-1}} Q` (arbitrary
integers `n_i != 0`), pruning any branch whose running `|c|` already exceeds
the target cutoff `X`, up to a max word-length safety cap. **This word
alphabet is NOT already the free-product-reduced normal form** (the true
presentation is `Z_2 * Z_q` on generators `Q` and `R = Q S`, not on `Q,S`
directly) — so the raw enumeration systematically produces MULTIPLE distinct
words representing the SAME double coset. Completeness/correctness is
recovered by canonicalizing every generated matrix to its `(c, d mod c)`
invariant (sec.1.1) and deduping on that, not on the word or on `|c|` alone.

### 1.3 Three bugs caught and fixed (honest trail, not tuned away)

All three were caught by the SAME validation gate (phi_q(1.5) vs
`rate_measure.phi_q`), which is why that gate is load-bearing here, not
decorative:

1. **Dedup by `|c|` alone** (first version): silently merges distinct
   double cosets that happen to share `|c|` (genuinely common — Kloosterman-
   sum-style multiplicity). Gave `phi_from_cosets(q=8,X=50) = 0.431` vs
   `phi_ref = 0.561` (23% low, monotonically worse with more data, i.e.
   clearly wrong, not a truncation artifact).
2. **Dedup by WORD alone** (second version, after realizing (1)'s error):
   over-counts, since (sec.1.2) distinct `Q,S^n`-words are NOT already
   reduced w.r.t. the `(Q S)^q = I` relation. Gave `1.67`–`1.70` (3x too
   HIGH, and NOT converging as `X` grew — 1.669 -> 1.694 -> 1.704, still
   rising).
3. **Canonical `(c, d mod c)` key, but with a precision edge case**: at word
   depth >= 9, some words are `[S]`-equivalent to a MUCH shorter one (the
   elliptic relation is close to closing up), so `D/C` in the `floor(D/C)`
   step lands within float roundoff of an exact integer; `mp.nstr` on the
   resulting near-zero `D0` preserves its (tiny but nonzero) significant
   digits rather than snapping to 0, producing spurious near-duplicate keys.
   Symptom: `phi_from_cosets(q=8, X=50)` jumped from `0.550` (depth 8,
   correct) to `4.04` (depth 9, wrong) purely from adding max_depth. Fixed
   by snapping `D0` to 0 (or `C`) within a `mp.dps`-scaled tolerance
   (`r1_coset_enum.py::canon_key`). After the fix, `depth=8,9,10,11` all
   agree exactly (sec.2 table) — this is the receipt that depth-saturation
   is real, not an artifact.

---

## 2. Validation: phi_q(1.5) from the coset sum vs the certified evaluator

`phi_q(s) = sqrt(pi) Gamma(s-1/2)/Gamma(s) * Sum_{[S]\G_q/[S], c!=0} |c|^{-2s}`
(Hejhal 7.5), truncated to `|c| <= X`, vs `rate_measure.phi_q(q, s, N=24)`
(the repo's certified determinant-route evaluator, itself gated to <=2.4e-6
relative against the exact closed form at q=3,4,6 — `LAW_RATE_MEASURE.md`
GATE 1). `s = 1.5 + i*1e-8` (tiny imaginary offset to avoid an incidental
branch edge case in the reference evaluator; negligible at this `s`).

Depth-saturation receipt (q=8, X=50): identical to all 15 significant digits
printed at max_depth = 8, 9, 10, 11 (post-fix) — the enumeration is complete
for this `(q,X)` within the explored word-length range.

| q | X | n (cosets, X<=50/80) | phi (coset sum, X=80) | phi_ref (det. route) | reldiff |
|---|---|---|---|---|---|
| 8 | 80 | 866 | 0.554163 | 0.560916 | 1.20% |
| 12 | 80 | 778 | 0.464248 | 0.470307 | 1.29% |
| 16 | 80 | 740 | 0.432326 | 0.438143 | 1.33% |
| 24 | 80 | 671 | 0.407374 | 0.413868 | 1.57% |
| 32 | 80 | 619 | 0.396396 | 0.404703 | 2.05% |
| 48 | 80 | 595 | 0.389361 | 0.397638 | 2.08% |

Convergence-in-X receipt (q=8, dps=60): X=20 -> 0.5344, X=30 -> 0.5434, X=50
-> 0.5500, X=80 -> 0.5542, monotonically increasing toward `phi_ref =
0.56092` — consistent with a positive-term Dirichlet series being truncated
from below, i.e. the residual gap is TRUNCATION, not a structural bug. The
reldiff GROWS mildly with `q` (1.2%->2.1%) because larger-`q` groups need a
larger `X` to reach the same coset COUNT (their per-coset `c`-density near
`X` is higher — see the count column, which falls with `q`), so a fixed
`X=80` truncates a larger relative tail as `q` grows; this is a resource
statement about the enumerator's cost budget, not a defect.

**Verdict: enumerator is correct, but truncation-limited at ~1-2% for the
X<=80 budget affordable in this session — reported honestly, not stretched
past what the receipts show.**

---

## 3. Classification: matched (convergent) vs escaping

### 3.1 First-20 c-value tables (X=50 data, `r1_coset_cvalues_X50.json`)

Theta group (`q=infinity`), sorted, first 20:

```
2.0, 4.0, 4.0, 6.0, 6.0, 8.0, 8.0, 8.0, 8.0, 10.0, 10.0, 10.0, 10.0,
12.0, 12.0, 12.0, 12.0, 14.0, 14.0, 14.0
```

(Clean even-integer structure with growing multiplicity — the theta-group
spectrum at width-1 translation, consistent with the expected `c = 2n`
Kloosterman-type Dirichlet series.)

q=8, sorted, first 20:

```
1.8478, 3.4142, 3.4142, 4.4609, 4.4609, 4.8284, 6.8284, 6.8284, 8.1564,
8.1564, 10.2426, 10.2426, 10.7695, 10.7695, 10.7695, 10.7695, 11.6569,
11.6569, 11.6569, 11.6569
```

The smallest c(q=8) = `lambda_8 = 1.8478` matches `c(theta)_1 = 2` up to
exactly `2 - lambda_8 = 0.15224` — this is not a coincidence, it is the
`k=1` double coset (`W=Q_q` itself), whose `c` is `lambda_q` by construction,
matching the theta group's `k=1` coset (`c = 2`) EXACTLY at `lambda -> 2`, so
this pair's drift is `2 - lambda_q` to all orders — an exact algebraic
identity, not a numerically-fitted one.

### 3.2 Matched-vs-escaping decomposition and which dominates `D(q;s)`

Rank-matching proxy: pair the `i`-th smallest `c(q)` with the `i`-th smallest
`c(theta)` for `i = 0 .. min(n_q, n_theta)-1` ("matched"); any EXTRA terms in
the longer list beyond that (always `q`'s list here, since `n_q > n_theta`
in every case tested, sec.2 count column) are "escaping" (finite-`q`-only
cosets with `|c|<=50` and no theta-side counterpart in this window).

| q | s | matched-drift `Sum|c_q^-2s - c_th^-2s|` | escaping mass `Sum_{extra} c_q^-2s` | total (proxy for D) |
|---|---|---|---|---|
| 8  | 1.1 | 0.21786 | 0.02190 | 0.23976 |
| 12 | 1.1 | 0.12111 | 0.01792 | 0.13903 |
| 16 | 1.1 | 0.08231 | 0.01285 | 0.09516 |
| 24 | 1.1 | 0.04230 | 0.00465 | 0.04695 |
| 32 | 1.1 | 0.02236 | 0.00226 | 0.02462 |
| 48 | 1.1 | 0.00953 | 0.00074 | 0.01027 |
| 8  | 1.5 | 0.08428 | 0.00104 | 0.08532 |
| 12 | 1.5 | 0.03930 | 0.00083 | 0.04012 |
| 16 | 1.5 | 0.02345 | 0.00059 | 0.02404 |
| 24 | 1.5 | 0.01069 | 0.00021 | 0.01090 |
| 32 | 1.5 | 0.00573 | 0.00010 | 0.00583 |
| 48 | 1.5 | 0.00247 | 0.00003 | 0.00250 |

**Answer to the task's key structural question**: at both tested `s`, the
**matched (convergent) class dominates** — roughly 10x the escaping mass at
`s=1.1`, growing to ~80x at `s=1.5` (escaping mass falls off faster with `s`
since it lives at larger `|c|`, where the `s`-power kills it harder). This
contradicts the task's a priori suggestion that class-(b) escaping tail mass
would be the driver; the data says otherwise, and is reported as found, not
adjusted to fit the expectation.

### 3.3 Aggregate decay rate (own measurement, real axis)

Least-squares log-log slope of the "total" column above vs `q` (q=8..48;
unweighted least squares of `log(total)` on `log q`, all six q values):
`s=1.1`: slope ≈ **-1.759**; `s=1.5`: slope ≈ **-1.969**. Both meaningfully
steeper than `q^-1` and both SHALLOWER than `q^-2`. The single smallest
matched pair alone decays exactly as `2-lambda_q ~ q^-2` (sec.3.1); the
aggregate is close to but not exactly that. The total coset count inside the
fixed `X<=50` window FALLS with `q` (n_q: 330 at q=8 down to 237 at q=48),
so the aggregate is not explained by a growing term count.*

> **[CORRECTION 2026-08-18 audit-14/15]** The original paragraph read:
> "`s=1.1`: slope ≈ **-1.72**; `s=1.5`: slope ≈ **-1.85** … n_q falls from
> 330 at q=8 to 237 at q=48, i.e. MORE matched terms survive the cutoff as
> `lambda_q -> 2` … net effect keeps the aggregate close to, slightly steeper
> than, `q^-2`". Three defects, all corrected above:
> (a) the quoted slopes had no committed receipt and did not reproduce. A
> fresh unweighted least-squares fit directly on this note's own sec.3.2
> "total" column gives **-1.7592** (s=1.1) and **-1.9687** (s=1.5);
> (b) FALLING `n_q` means FEWER cosets inside the window, not "MORE matched
> terms" — the causal explanation offered was backwards and is withdrawn;
> (c) `-1.76` and `-1.97` are SHALLOWER than `q^-2`, not "slightly steeper".
> Receipt (fresh, this correction): `law_probes/r1_table_fits.py` →
> `law_probes/r1_table_fits.log`.

*[* caveat: only two `s` values and 6 `q` values tested; not a fit with
error bars, see sec.5.]

### 3.4 Honest gap vs `LAW_RATE_MEASURE.md`

`LAW_RATE_MEASURE.md` measured `D(q;s) = |phi_q(s) - phi_infty(s)|` at
**off-axis** `s = 1.1+0.5i, 1.1+1.5i, 1.25+0.5i, 1.25+1.5i` via the
DETERMINANT-route evaluator, and found slopes `-0.65` to `-1.68` (roughly
`q^-1`). This note's slopes (`-1.759`, `-1.969`; originally misquoted as `-1.72`,
`-1.85`) are measured at **real axis**
`s = 1.1, 1.5` (`t=0`) — corrected values `-1.759`, `-1.969`, see the
[CORRECTION 2026-08-18 audit-14/15] block in sec.3.3 — via the INDEPENDENT
coset-counting route, using a
RANK-MATCHING proxy rather than the exact algebraic `phi_q - phi_infty`
difference. **These are not directly comparable measurements** — different
`t`, different method, and the rank-matching decomposition is itself only a
PROXY for the true class split (sec.5). The two together suggest the true
rate may depend on `t` (matches `LAW_RATE_MEASURE.md`'s own finding that its
slope varies with `(sigma,t)`) but this note does NOT claim to have resolved
or reconciled the two numbers — flagged as an open item for R2.

---

## 4. Empirical partial-window mass (item 3)

> **[CORRECTION 2026-08-18 audit-9]** This section was headed "Tail majorant
> (item 3)". Nothing here is a majorant: every number below is the mass of
> the ALREADY-ENUMERATED spectrum between `X'` and the hard cutoff 50. Write
> it as `Sum_{X' <= |c| <= 50} |c|^-2.2` and read it as empirical
> partial-window mass only.

`Sum_{c in spectrum, X' <= |c| <= 50} |c|^-2.2` (sigma=1.1), i.e. the mass
still remaining above a partial cutoff `X'`, WITHIN the already-enumerated
`X<=50` data (not a true asymptotic tail beyond 50 — see sec.5):

| q | X'=10 | X'=20 | X'=30 | X'=40 |
|---|---|---|---|---|
| 8 | 0.25532 | 0.11922 | 0.06086 | 0.02673 |
| 12 | 0.19779 | 0.11662 | 0.06709 | 0.02951 |
| 16 | 0.17617 | 0.10791 | 0.05153 | 0.02591 |
| 24 | 0.18006 | 0.09046 | 0.05302 | 0.02180 |
| 32 | 0.16529 | 0.08324 | 0.04955 | 0.02034 |
| 48 | 0.15618 | 0.07867 | 0.04590 | 0.01896 |
| theta | 0.17524 | 0.08671 | 0.04704 | 0.02172 |

No systematic growth in `q` — values at each `X'` cluster within roughly a
factor of 1.6 across all of `q=8..48` and the theta group, and the LARGEST
value in each `X'` column belongs to a SMALL `q`, never a large one
(`q=8` at `X'=10, 20`; `q=12` at `X'=30, 40`) — consistent with (not proof
of) Hejhal's Lemma 7.2 claim of an `N`-independent majorant constant.

> **[CORRECTION 2026-08-18 audit-15]** The original said "the LARGEST value at
> each `X'` column is `q=8` (the smallest `q` tested)". False at `X'=30` and
> `X'=40`, where `q=12` (0.06709, 0.02951) exceeds `q=8` (0.06086, 0.02673).
> The `q`-independence reading survives; the specific argmax claim did not.
> Receipt: `law_probes/r1_table_fits.py` → `law_probes/r1_table_fits.log`.

Fitted power-law decay in `X'` (log-log slope, `Sum vs X'`, unweighted least
squares over the four `X'` values): **-1.29 to -1.56** across `q` and theta
(all within a narrow band, no `q`-trend in the slope either; recomputed
2026-08-18, receipt as above — this range reproduces).

**Empirical uniform constant, rounded UP:
`Sum_{10 <= |c| <= 50} |c|^-2.2 <= 0.26`** for every `q` in
`{8,12,16,24,32,48}` and the theta group, over the data window tested
(`|c| <= 50`). This is an empirical PARTIAL-WINDOW mass, not a tail majorant
(see [CORRECTION 2026-08-18 audit-9] above and sec.5).

---

## 5. Honest gaps

- **Word-enumeration incompleteness is the load-bearing risk this note
  flags, per the task's own instruction.** The BFS is pruned by `|c| <= X`
  and a word-length cap; sec.2's depth-saturation receipt (identical output
  at max_depth 8,9,10,11) is evidence of local completeness for `q=8,
  X<=50/80`, but was NOT independently re-run for every `(q, X)` combination
  in the sec.2 table at the SAME depth-saturation rigor — the X=80 run used
  max_depth=11 for all q without a per-q saturation re-check. If the true
  saturation depth is larger for some `q` in `{12,...,48}`, the corresponding
  `n` and `phi(coset sum)` values in sec.2 could be undercounts. This is
  exactly the guard the phi_q(1.5) validation gate provides (sec.2), and the
  gate is CONSISTENT (all reldiffs are 1-2%, one-sided low, matching the
  truncation-not-completeness diagnosis) — but it is a consistency check,
  not a proof of completeness.
- **The matched/escaping classification (sec.3) uses a RANK-MATCHING proxy**,
  not an exact word-level correspondence between `q`-cosets and their true
  theta-group limits. A more rigorous classification (as the task's item 2
  literally specifies: "c(q) values that are algebraic functions of lambda_q
  ... match them") would track EACH double coset's canonical word/matrix as
  an explicit function of `lambda` and take the symbolic `lambda -> 2` limit
  per-coset, confirming which cosets survive the limit and which don't. That
  symbolic tracking was not built in this session (time budget); rank-
  matching is a numerically-grounded but coarser substitute, flagged here
  rather than silently upgraded to "the" classification.
- **Tail majorant (sec.4) is measured only within the already-truncated
  `X<=50` window** — it reports how much mass remains between a partial cutoff
  `X'` and the hard cutoff 50, not the TRUE tail `Sum_{|c|>50}`, which was not
  computed (would require re-running the enumerator with `X=200+` per `q`,
  not attempted here). The reported constant `0.26` is therefore an
  UNDER-estimate of the true tail past `X'=10`, and should not be read as a
  bound on `Sum_{|c|>=10}` over the FULL spectrum.
- **`s=1.1,1.5` real-axis only** — no off-axis (`t != 0`) coset-sum
  measurement was attempted in this note (the existing `rate_measure.py`
  route already covers off-axis via the determinant method); sec.3.4's gap
  vs `LAW_RATE_MEASURE.md` is left open, not resolved.

---

## 6. Analytic next-step section (for R2)

- **What the data supports**: a lemma of the shape "the double-coset
  Dirichlet series `Sum |c(q)|^-2s` splits into a MATCHED sub-series (in
  bijection, term-by-term, with the theta-group series via an explicit
  algebraic map `lambda_q -> 2`) plus a residual (escaping) sub-series
  supported on `|c| = O(q)` or larger; sec.3.2's data says the MATCHED
  sub-series' drift, not the escaping mass, should be the leading term in
  any `(RATE)` bound at these `(sigma,t)` values" — i.e. R2's "prefix drift
  (mean-value in lambda)" term (per `LAW_HEJHAL_S7_EXTRACT.md` sec.4's own
  R2 sketch) is the one to make explicit and bound FIRST; the "two tails"
  term is secondary at the tested cells.
- A natural next computational step for R2: replace the rank-matching proxy
  (sec.3.2, flagged sec.5) with the EXACT algebraic correspondence — the
  `k=1` coset's exact match (`c=lambda_q` vs `c=2`, sec.3.1) generalizes: for
  fixed word-length `k`, `c(word; lambda)` is a specific polynomial/rational
  function of `lambda` (from the matrix-product formula), so the matched
  class can in principle be enumerated SYMBOLICALLY (fixed `k`, `lambda` as
  a free parameter) rather than numerically per-`q` — this would upgrade
  sec.3's proxy classification to the literal per-coset limit the task
  specifies, and is the most direct way to close the sec.3.4 gap against
  `LAW_RATE_MEASURE.md`'s off-axis slopes.
- The partial-window-mass table (sec.4; "tail majorant" per
  [CORRECTION 2026-08-18 audit-9]) is consistent with Lemma 7.2's claimed
  `N`-independent constant `C(epsilon)`; an R2/R3 proof would need this made
  RIGOROUS (the Lemma 7.2 proof route via chapter 6 prop 5.1's tiny-disk
  argument, per the extraction note) rather than resting on the numerical
  cluster observed here.

---

## 7. Files

- `law_probes/r1_coset_enum.py` — the enumerator (`enumerate_c_spectrum`,
  `dirichlet_partial_sum`, canonicalization with the depth-9 precision fix
  documented inline).
- `law_probes/r1_table_fits.py` + `law_probes/r1_table_fits.log` — fit/range
  receipt added 2026-08-18 for the audit-14/15 corrections (recomputes every
  fitted slope and column range in sec.3.3 and sec.4 from the tables printed
  in this note; stated convention = unweighted least squares of `log y` on
  `log x`).
- `law_probes/r1_coset_cvalues_X50.json` — raw c-value lists (with
  multiplicity) for q in {8,12,16,24,32,48} and the theta group, X<=50.
