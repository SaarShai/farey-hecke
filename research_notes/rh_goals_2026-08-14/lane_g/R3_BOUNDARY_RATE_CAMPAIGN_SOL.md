# R3 boundary RATE campaign at the exact target height

**Date:** 2026-08-18  
**Interpreter:** `/Users/za/.venvs/farey-rh/bin/python` (`python-flint 0.9.0`, `mpmath 1.4.1`)  
**Verdict:** **CERTIFIED COARSE ENCLOSURES OBTAINED; POSITIVE RATE NOT PROVED.**

The campaign was executed for every integer `12 <= q <= 48`.  On the exact
continuous right boundaries it proves

\[
 0\le E_R^A(q)<8.408224199432881,
 \qquad
 0\le E_R^B(q)<8.228313336614521.                    \tag{V1}
\]

The inequalities are genuine Arb/Ford certificates, with the displayed upper
endpoints rounded **up** by one binary64 ulp.  They are independent of \(q\), so
the only exponent proved by this campaign is \(\alpha=0\).  In particular, the
requested statement

\[
 E_R(q)\le C_Rq^{-\alpha}\quad(\alpha>0)              \tag{RATE}
\]

remains **CONJECTURAL / OPEN**.

The pre-existing `agp_phi.py` lineage does **not** currently yield rigorous
balls for the true \(\phi_q\).  Its finite transfer matrices use Arb, but its
Fredholm dimension-tail step is an empirical geometric extrapolation, the
returned `selberg_Z` ball omits that tail, and branch correction is performed by
floating `mpmath.quad`.  The target “promote that evaluator to a certified
\(\phi_q\) evaluator merely by changing scalar arithmetic to Arb” is therefore
**FALSE**.  The corrected statement is:

> Arb certifies the finite matrix algebra and the explicit theta function; a
> proof of a uniform Fredholm determinant tail (or a complete exact
> double-coset enumeration plus Ford remainder) is still required before a
> narrow ball can be asserted to contain the true \(\phi_q\).

The realistic R3 architecture is consequently **analytic RATE for the infinite
tail, plus per-\(q\) certification only for a finite base block after an analytic
\(q_0\) is known**.  Per-\(q\) computation cannot determine that \(q_0\) by
itself.

---

## 1. Exact contours consumed by the two R3 routes

Put

\[
 \rho_1=\tfrac12+i\gamma_1,
 \qquad t_0=\gamma_1/2,
 \qquad \sigma_R=\frac{11}{10}.
\]

The routes use different vertical spans.

| route | right boundary | interval used by this campaign |
|---|---|---|
| A / A0 (`R3_TRANSPORT_EXECUTION_SOL.md`) | \(\Gamma_R^A=\{1.1+it:|t-t_0|\le1/2\}\) | closed, exactly as stated |
| B (`R3_ROUTE_B_TRANSPORT_SOL.md`) | \(\Gamma_R^B=\{1.1+it:|t-t_0|<1/4\}\) | closed hull \(|t-t_0|\le1/4\), an upper-bound-safe enlargement |

The precise norms are

\[
 E_R^A(q)=\sup_{s\in\Gamma_R^A}|\phi_q(s)-\phi_\infty(s)|,
 \qquad
 E_R^B(q)=\sup_{s\in\Gamma_R^B}|\phi_q(s)-\phi_\infty(s)|,       \tag{1.1}
\]

where both notes use

\[
 \phi_\infty(s)=
 \frac{\sqrt\pi\,\Gamma(s-\tfrac12)\zeta(2s-1)}
      {\Gamma(s)\zeta(2s)(4^s-1)}.                                \tag{1.2}
\]

### Receipt 1A — source extraction

```text
$ rg -n -C 2 'Gamma_R|E_R|sigma_R|t_0|right side' \
    research_notes/rh_goals_2026-08-14/lane_g/R3_TRANSPORT_EXECUTION_SOL.md \
    research_notes/rh_goals_2026-08-14/lane_g/R3_ROUTE_B_TRANSPORT_SOL.md

R3_TRANSPORT_EXECUTION_SOL.md:48-55
 Omega={s: 1/2<Re s<11/10, |Im s-t_0|<1/2}.
 Gamma_R={11/10+it:|t-t_0|<=1/2}.

R3_TRANSPORT_EXECUTION_SOL.md:71-73
 F_q=phi_q-phi_infty,
 E_R(q)=sup_{Gamma_R}|F_q|.

R3_ROUTE_B_TRANSPORT_SOL.md:87-99
 d=1/4, sigma_R=11/10, z_c=1/2+it_0.
 P=(1/2,sigma_R) x (t_0-d,t_0+d).

R3_ROUTE_B_TRANSPORT_SOL.md:265-269
 Gamma_R={sigma_R+it:|t-t_0|<d}.
 H=2d=1/2, L=sigma_R-1/2=3/5.
```

Thus the single campaign contour that safely feeds both routes is the larger
\(\Gamma_R^A\).  A point evaluation at \(t=7.0665\) lies on both sides but does
not provide an upper-bound certificate for either supremum norm.

### Receipt 1B — exact height and endpoints

```text
$ /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import acb, arb, ctx
ctx.dps=100
t0=(acb.zeta_zero(1)/2).imag
print('t0_lower=',t0.lower())
print('t0_upper=',t0.upper())
print('route_A_t_lower=',(t0-arb('0.5')).lower())
print('route_A_t_upper=',(t0+arb('0.5')).upper())
print('route_B_t_lower=',(t0-arb('0.25')).lower())
print('route_B_t_upper=',(t0+arb('0.25')).upper())
print('t0_minus_7.0665_lower=',(t0-arb('7.0665')).lower())
PY
t0_lower= [7.067362570867346895228625991781235135392128557849621587842783730074981714904628382474505196585780506 +/- 2.43e-100]
t0_upper= [7.067362570867346895228625991781235135392128557849621587842783730074981714904628382474505196585780506 +/- 4.72e-100]
route_A_t_lower= [6.567362570867346895228625991781235135392128557849621587842783730074981714904628382474505196585780506 +/- 2.43e-100]
route_A_t_upper= [7.567362570867346895228625991781235135392128557849621587842783730074981714904628382474505196585780506 +/- 4.72e-100]
route_B_t_lower= [6.817362570867346895228625991781235135392128557849621587842783730074981714904628382474505196585780506 +/- 2.43e-100]
route_B_t_upper= [7.317362570867346895228625991781235135392128557849621587842783730074981714904628382474505196585780506 +/- 4.72e-100]
t0_minus_7.0665_lower= [0.0008625708673468952286259917812351353921285578496215878427837300749817149046283824745051965857805062999 +/- 3.50e-104]
```

The old sweep height (7.0665) is lower than (t_0) by more than
\(8.6257\times10^{-4}\), rigorously.

---

## 2. Audit of the branch-corrected evaluator

The starting identity is

\[
 \phi_q(s)=\frac{Z_{S,q}(1-s)}{Z_{S,q}(s)K_q(s)}.                 \tag{2.1}
\]

`rate_measure.py` repairs the principal-branch defect in \(K_q\) by integrating
the analytic logarithmic derivative on the vertical path from \(10^{-6}i\):

\[
 \log K_q(\sigma+it)=\log K_q(\sigma+10^{-6}i)
   +i\int_{10^{-6}}^t (\log K_q)'(\sigma+iu)\,du.                 \tag{2.2}
\]

That is the correct branch-tracking idea, and the arithmetic \(q=3,4,6\)
cross-check is useful.  Its present implementation is not an interval proof.

### Receipt 2A — the path and midpoint extraction are floating

```text
$ nl -ba research_notes/rh_goals_2026-08-14/lane_g/law_probes/rate_measure.py \
    | sed -n '97,119p'
  98  def logK_corrected(sig, t, q):
  99      """log K_q(sigma+it) reconstructed by path-integrating ..."""
 104      t0 = mpf('1e-6')
 106      base = log(A.K_q_corrected(s0, q))
 107      integrand = lambda tt: mpc(0, 1) * A.dlogK_ds(...)
 108      inc = quad(integrand, [t0, mpf(t)])
 112  def phi_q(q, s, N, n_head=4):
 115      Zs = A.selberg_Z(q, complex(s), N, n_head)
 116      Zm = A.selberg_Z(q, complex(1 - s), N, n_head)
 118      logphi = cmath.log(Zm) - cmath.log(Zs) - complex(logK)
 119      return cmath.exp(logphi)
```

### Receipt 2B — the dimension tail is not proved and is omitted

```text
$ nl -ba .worktrees/aletheia-restore/code/zeta_cert_rosen_even.py \
    | sed -n '278,318p;487,505p'
 278  def dim_tail_from_matrix_signed(...):
 280      """Same det-increment geometric-ratio tail heuristic ...
 283      ... this is NOT a proven uniform tail bound.
 315      tail = g_last * q / (1 - q)
 318      return tail, info
 487  def selberg_Z(...):
 497      The returned ball carries the determinant midpoints only (dimension tails
 498      are NOT folded in) ...
 501      dp, _t, _i, _k = cert_det(...)
 503      dm, _t, _i, _k = cert_det(...)
 505      return (dp * dm) / det_K(...)

$ nl -ba .worktrees/aletheia-restore/code/zeta_cert_rosen.py \
    | sed -n '436,453p'
 436  def selberg_Z(...):
 446      The returned ball carries the determinant midpoints only (the dimension
 447      tails from cert_det are NOT folded in) ...
 451      dp, _t, _i, _k = cert_det(...)
 452      dm, _t, _i, _k = cert_det(...)
 453      return (dp * dm) / det_K(...)
```

The name `cert_det` does not change this logical boundary: finite-\(N\) matrix
rounding is certified; convergence to the Fredholm determinant is not.

### Rigor ledger

| layer | status |
|---|---|
| \(t_0\), \(\lambda_q=2\cos(\pi/q)\), finite matrix entries, finite matrix determinant | **RIGOROUS BALLS** |
| exact Hurwitz closure of each infinite branch sum within a retained matrix column | **RIGOROUS BALLS** |
| \(\phi_\infty\) and its denominator clearances on interval boxes | **RIGOROUS BALLS** |
| Ford-packing full-series mass bound used in §3 | **PROVED ANALYTIC BOUND + ARB** |
| Fredholm dimension tail from retained matrix size \(N\) to infinity | **HEURISTIC / NOT A BALL FOR THE TRUE DETERMINANT** |
| `selberg_Z` returned ball as an enclosure of true (Z_S) | **FALSE; tail omitted** |
| branch-corrected `mpmath.quad`, `cmath.log`, midpoint conversion | **FLOATING ESTIMATE** |
| resulting narrow \(\phi_q\) value | **FLOATING ESTIMATE, NOT CERTIFIED** |

---

## 3. The certified fallback actually executed

For (Re s>1), Hejhal (7.5) gives

\[
 \phi_q(s)=M(s)D_q(s),\qquad
 M(s)=\sqrt\pi\frac{\Gamma(s-1/2)}{\Gamma(s)},\qquad
 D_q(s)=\sum_{[\gamma],\,c_\gamma\ne0}|c_\gamma|^{-2s}.          \tag{3.1}
\]

The proved Ford packing estimate in `M2_G1G2_CLOSURE_SOL.md:298-359` is

\[
 A_q(X):=\#\{[\gamma]:0<|c_\gamma|\le X\}\le X^2,               \tag{3.2}
\]

and hence, for \(\sigma>1\),

\[
 \sum_{|c_\gamma|>X}|c_\gamma|^{-2\sigma}
 \le \frac{\sigma}{\sigma-1}X^{2-2\sigma}.                     \tag{3.3}
\]

At \(\sigma=1.1\), set \(X=1\).  There is at most one term with \(|c|=1\),
and the strict tail is at most (11); therefore

\[
 |D_q(1.1+it)|\le12                                              \tag{3.4}
\]

for every finite Hecke group in the normalized family.  It follows that on
every \(t\)-box \(I\),

\[
 \sup_{t\in I}|\phi_q(1.1+it)-\phi_\infty(1.1+it)|
 \le 12\sup_{t\in I}|M(1.1+it)|
      +\sup_{t\in I}|\phi_\infty(1.1+it)|.                      \tag{3.5}
\]

`boundary_rate_kernel.py` subdivides each complete vertical segment into
16,384 Arb boxes, evaluates the right side of (3.5), forms the interval maximum
with `arb.max`, checks every denominator ball avoids zero, and rounds reported
upper bounds upward.

### Receipt 3A — all \(q=12,\ldots,48\)

```text
$ /Users/za/.venvs/farey-rh/bin/python \
  research_notes/rh_goals_2026-08-14/lane_g/law_probes/kaggle_boundary_rate/boundary_rate_kernel.py \
  --q-start 12 --q-end 48 --envelope-cells 16384 \
  --out /tmp/r3_boundary_envelope_16384_safe_max.json
RIGOROUS route_A E upper = 8.408224199432881
RIGOROUS route_B E upper = 8.228313336614521
wrote /tmp/r3_boundary_envelope_16384_safe_max.json

$ /Users/za/.venvs/farey-rh/bin/python - <<'PY'
import json
d=json.load(open('/tmp/r3_boundary_envelope_16384_safe_max.json'))['rigorous']
for k in ('route_A','route_B'):
 r=d[k]; print(k,r['E_interval'],r['worst_cell_index'],r['denominator_clearance_lower'])
print('q count',len(d['per_q']))
PY
route_A [0.0, 8.408224199432881] 0 {'abs_zeta_2s': 0.7333210697397589, 'abs_4pow_s_minus_1': 5.153296135365962, 'abs_gamma_s': 5.809243106114081e-05}
route_B [0.0, 8.228313336614521] 0 {'abs_zeta_2s': 0.7333288528025149, 'abs_4pow_s_minus_1': 5.387450709939002, 'abs_gamma_s': 8.432514346168317e-05}
q count 37
```

The worst box is the bottom box in both routes.  The Route-A worst-box pieces
were

\[
 \sup|M|<0.6919084284454585,
 \quad 12\sup|M|<8.302901141345503,
 \quad \sup|\phi_\infty|<0.10532305808737875.                    \tag{3.6}
\]

### Receipt 3B — subdivision refinement

```text
cells   Route-A upper       Route-B upper
2048    8.439800190972164   8.241852836916223
4096    8.424774152110330   8.234472980373539
8192    8.413694781833328   8.230801564059220
16384   8.408224199432881   8.228313336614521
```

Each row is independently rigorous; refinement only tightens an already valid
upper bound.

### Per-\(q\) verified quantities

All intervals below have status `RIGOROUS_ARB_FORD_ENCLOSURE`.

| \(q\) | verified \(E_R^A(q)\) interval | verified \(E_R^B(q)\) interval |
|---:|---:|---:|
| 12 | ([0,8.408224199432881]) | ([0,8.228313336614521]) |
| 13 | ([0,8.408224199432881]) | ([0,8.228313336614521]) |
| 14 | ([0,8.408224199432881]) | ([0,8.228313336614521]) |
| 15 | ([0,8.408224199432881]) | ([0,8.228313336614521]) |
| 16 | ([0,8.408224199432881]) | ([0,8.228313336614521]) |
| 17 | ([0,8.408224199432881]) | ([0,8.228313336614521]) |
| 18 | ([0,8.408224199432881]) | ([0,8.228313336614521]) |
| 19 | ([0,8.408224199432881]) | ([0,8.228313336614521]) |
| 20 | ([0,8.408224199432881]) | ([0,8.228313336614521]) |
| 21 | ([0,8.408224199432881]) | ([0,8.228313336614521]) |
| 22 | ([0,8.408224199432881]) | ([0,8.228313336614521]) |
| 23 | ([0,8.408224199432881]) | ([0,8.228313336614521]) |
| 24 | ([0,8.408224199432881]) | ([0,8.228313336614521]) |
| 25 | ([0,8.408224199432881]) | ([0,8.228313336614521]) |
| 26 | ([0,8.408224199432881]) | ([0,8.228313336614521]) |
| 27 | ([0,8.408224199432881]) | ([0,8.228313336614521]) |
| 28 | ([0,8.408224199432881]) | ([0,8.228313336614521]) |
| 29 | ([0,8.408224199432881]) | ([0,8.228313336614521]) |
| 30 | ([0,8.408224199432881]) | ([0,8.228313336614521]) |
| 31 | ([0,8.408224199432881]) | ([0,8.228313336614521]) |
| 32 | ([0,8.408224199432881]) | ([0,8.228313336614521]) |
| 33 | ([0,8.408224199432881]) | ([0,8.228313336614521]) |
| 34 | ([0,8.408224199432881]) | ([0,8.228313336614521]) |
| 35 | ([0,8.408224199432881]) | ([0,8.228313336614521]) |
| 36 | ([0,8.408224199432881]) | ([0,8.228313336614521]) |
| 37 | ([0,8.408224199432881]) | ([0,8.228313336614521]) |
| 38 | ([0,8.408224199432881]) | ([0,8.228313336614521]) |
| 39 | ([0,8.408224199432881]) | ([0,8.228313336614521]) |
| 40 | ([0,8.408224199432881]) | ([0,8.228313336614521]) |
| 41 | ([0,8.408224199432881]) | ([0,8.228313336614521]) |
| 42 | ([0,8.408224199432881]) | ([0,8.228313336614521]) |
| 43 | ([0,8.408224199432881]) | ([0,8.228313336614521]) |
| 44 | ([0,8.408224199432881]) | ([0,8.228313336614521]) |
| 45 | ([0,8.408224199432881]) | ([0,8.228313336614521]) |
| 46 | ([0,8.408224199432881]) | ([0,8.228313336614521]) |
| 47 | ([0,8.408224199432881]) | ([0,8.228313336614521]) |
| 48 | ([0,8.408224199432881]) | ([0,8.228313336614521]) |

These are meaningful as verified enclosures, but not as measured decay data:
the same Ford majorant was deliberately used for every \(q\).

---

## 4. Floating scout: what was reached locally

The midpoint scout was run at \(q=12\) on the three-point Route-A grid
(t=t_0-1/2,t_0,t_0+1/2).  This is **not** a continuous supremum and is not an
enclosure of the true \(\phi_{12}\).

### Receipt 4A — low-\(N\) failure and higher-\(N\) stabilization

```text
N pair    Route-A grid max at larger N   max pointwise relative phi change
8,12      0.08755220236896830            0.35556397699552006
16,24     0.08791032896062147            0.00030434555085993647
```

For \(N=24\), the **only** one of these three points lying in the Route-B span
was the center, with value \(0.046066165332989205\); the sampled Route-A maximum
occurred at the lower endpoint and was \(1.9083491826411378\) times larger.
Thus even a numerically stable value at \(t_0\) is not a substitute for either
full-side supremum.

The \(N=16,24\) command and terminal tail were:

```text
$ /Users/za/.venvs/farey-rh/bin/python boundary_rate_kernel.py \
    --q-start 12 --q-end 12 --envelope-cells 512 --scout --grid 3 \
    --n-values 16,24 --out /tmp/r3_boundary_scout_q12_grid3_N16_24.json
q=12 N=24 point=1/3 t=6.567362570867
q=12 N=24 point=2/3 t=7.067362570867
q=12 N=24 point=3/3 t=7.567362570867
finished q=12: FLOAT route_A grid max=8.791032896e-02
wrote /tmp/r3_boundary_scout_q12_grid3_N16_24.json
```

The local scout stopped at \(q=12\): its purpose was to expose the accuracy and
cost ceiling, not to manufacture an uncertified 37-row table.  The complete
\(q=12,\ldots,48\) shard plan is in §6.

---

## 5. Decay fit and comparison with \(q^{1-2\sigma}\)

At the boundary \(\sigma=1.1\), the proposed scale is

\[
 q^{1-2\sigma}=q^{-1.2}.                                      \tag{5.1}
\]

### 5.1 Certified data

The verified upper endpoints in §3 are constant in \(q\).  Their log-log slope
is exactly \(0\), so they prove no \(\alpha>0\).  This is a limitation of the
majorant, not evidence that \(E_R(q)\) fails to decay.

### 5.2 Existing single-height floating data

For context only, the old `rate_measure_data.json` rows at
\((\sigma,t)=(1.1,7.0665)\) give:

| \(q\) | floating \(D(q;1.1+7.0665i)\) | \(N\)-doubling relative difference | \(Dq^{1.2}\) |
|---:|---:|---:|---:|
| 12 | 0.04618230457 | 0.0044553 | 0.91095 |
| 16 | 0.00938386217 | 0.0150003 | 0.26141 |
| 24 | 0.00658156119 | 0.0236124 | 0.29825 |
| 32 | 0.00575997795 | 0.0142397 | 0.36864 |
| 48 | 0.00241546212 | 0.0185693 | 0.25147 |

A blind least-squares fit gives

\[
 D\asymp q^{-1.82525},\qquad R^2=0.85951.                       \tag{5.2}
\]

This fit is **NOT EVIDENCE**: every target-height row has a (0.4\%)–(2.4\%)
change in \(\phi_q\) under \(N\)-doubling, while \(D\) itself is small and can be
phase-cancellation sensitive; the height is also not (t_0), and the values are
points rather than suprema.  The nonconstant \(Dq^{1.2}\) column likewise does
not validate or refute the \(q^{-1.2}\) law.

The fit receipt was:

```text
$ /Users/za/.venvs/farey-rh/bin/python - <<'PY'
# select sigma=1.1, t=7.0665, q<=48 from rate_measure_data.json;
# least-squares fit log D against log q
PY
12 0.04618230456925413 0.004455321695914483 0.9109469715243984
16 0.009383862173947844 0.01500032412892248 0.26141204804555157
24 0.006581561194254793 0.0236124386452332 0.29825134695931727
32 0.005759977949086829 0.014239695619462249 0.368638588741557
48 0.0024154621152229056 0.01856925434261641 0.2514720459222455
fit_all slope -1.8252476971189182 alpha 1.8252476971189182 R2 0.8595106663107357
row_count_total 48
```

### 5.3 Consequence for the two R3 transports

Route A's currently printed sufficient condition is
\(E_R^A(q)<7.03\times10^{-46}\).  The certified bound (V1) is about 46 orders of
magnitude too coarse.  Even the purely illustrative assumptions
\(E_R^A(q)\approx1.734q^{-1.2}\) (normalizing from the uncertified \(q=12\)
three-point maximum) would not reach that threshold until
\(q\approx6.7\times10^{37}\).  This number is **CONJECTURAL DIAGNOSTIC ONLY**;
it shows that finite enumeration cannot compensate for the present transport
loss.

Route B raises \(E_R\) only to the power
\(c_0=1.827324\times10^{-5}\) after its two propagation stages.  It is therefore
even less numerically realistic without a radically sharper propagation
constant, despite being logically explicit conditional on RATE.

**Honest route verdict.**

1. A proved analytic RATE is indispensable for the infinite family and is the
   more realistic route to an actual \(q_0\).
2. A narrow per-\(q\) certificate is technically plausible only after replacing
   the Fredholm-tail heuristic by a theorem (or using complete exact cosets plus
   Ford remainder).  It is useful for a finite base block, direct winding, and
   falsification.
3. “Verify every \(q\le q_0\)” before another theorem produces \(q_0\) is
   circular.  With the present transport losses it is also computationally
   implausible.
4. The best corrected program is hybrid: prove RATE/M1–M3 analytically for the
   tail; if the resulting \(q_0\) is moderate, certify the finite block by direct
   winding of \(\phi_q\), which avoids the \(7.03\times10^{-46}\) comparison
   margin whenever possible.

---

## 6. Kaggle-ready bundle (not pushed)

Directory:

```text
research_notes/rh_goals_2026-08-14/lane_g/law_probes/kaggle_boundary_rate/
  boundary_rate_kernel.py
  manifest.json
  zeta_cert_rosen.py
  zeta_cert_rosen_even.py
  zeta_cert_rosen_q5.py
```

The three transfer-operator modules are vendored so the kernel does not depend
on `.worktrees/aletheia-restore/code`.  `manifest.json` pins package versions,
SHA-256 hashes, contours, status semantics, and commands.

Rigorous 37-\(q\) envelope:

```bash
python boundary_rate_kernel.py --q-start 12 --q-end 48 \
  --envelope-cells 16384 --out boundary_rate_rigorous.json
```

Floating one-\(q\)-per-job scout:

```bash
python boundary_rate_kernel.py --q-start Q --q-end Q \
  --envelope-cells 16384 --scout --grid 129 --n-values 16,24 \
  --out boundary_rate_qQ.json
```

Hard-cell escalation:

```bash
python boundary_rate_kernel.py --q-start Q --q-end Q \
  --envelope-cells 16384 --scout --grid 257 --n-values 24,32,40 \
  --out boundary_rate_qQ_escalated.json
```

Every scout row is mechanically labeled `FLOAT_GRID_ESTIMATE_NOT_SUP`; no
\(N\)-doubling threshold promotes it.  This fail-closed behavior is intentional
until a proved Fredholm-tail routine replaces the current extrapolation.  The
CLI also rejects `--prec-bits < 128`, ensuring that the final one-ulp outward
binary64 conversion is performed from working precision far finer than one ulp.

### Receipt 6A — bundle integrity

```text
$ shasum -a 256 kaggle_boundary_rate/*.py
d51f062142382cffa434d7a2aa144e6d3e1d210be6cd15fe785a77579bd3d8d9  boundary_rate_kernel.py
965c2e5f65ae88b458d79bc425375e31589dcbf50703173664ef0e30901dceac  zeta_cert_rosen.py
693d2a88fd525e94c8ab6a63486e82fe0670d9dce142effbd5be5e324597212a  zeta_cert_rosen_even.py
c84c5c3f6d9f7a320bca7f1dbfd96a4859c3eea9b3de5420eb4eb223ad0d597b  zeta_cert_rosen_q5.py
```

### Receipt 6B — fail-closed precision gate

```text
$ /Users/za/.venvs/farey-rh/bin/python boundary_rate_kernel.py \
    --prec-bits 64 --out /tmp/should_not_exist_boundary_rate.json
boundary_rate_kernel.py: error: --prec-bits must be at least 128 for rigorous float endpoint export
EXIT_CODE=2
```

No Kaggle API call or push was made.

---

## 7. Final claim ledger

| claim | status |
|---|---|
| Exact \(t_0\) and both contour spans | **ARB-CERTIFIED / SOURCE-EXTRACTED** |
| \(\phi_\infty\) interval evaluation and denominator clearance | **RIGOROUS** |
| Ford full-series mass \(\le12\) at \(\sigma=1.1\) | **PROVED**, conditional only on the standard normalized Hecke-group hypotheses stated in `M2_G1G2_CLOSURE_SOL.md` |
| (V1) for every \(q=12,\ldots,48\) | **RIGOROUS** |
| Narrow branch-corrected \(\phi_q\) balls from the determinant lineage | **FALSE AT PRESENT**; finite matrices only |
| \(q=12\) three-point values | **FLOATING ESTIMATES, NOT SUPREMA** |
| Old \(t=7.0665\) slope \(-1.82525\) | **FLOATING / NOT EVIDENCE** |
| \(E_R(q)\ll q^{-1.2}\) or any \(E_R(q)\le C_Rq^{-\alpha}\), \(\alpha>0\) | **CONJECTURAL / OPEN** |
| Effective R3 \(q_0\) | **UNDEFINED** |

The next proof-grade numerical milestone is not a denser grid.  It is a proved
Fredholm determinant truncation bound, uniform over each complex (s)-box and
each requested \(q\), followed by interval branch continuation and adaptive
box subdivision.  Until that exists, denser Kaggle runs improve scouting only.
