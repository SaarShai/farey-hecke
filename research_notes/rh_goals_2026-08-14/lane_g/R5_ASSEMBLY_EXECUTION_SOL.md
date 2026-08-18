# R5 assembly execution: the effective `(RATE)` pincer

**Verdict:** **`UNVERIFIABLE: EXPLICIT N0 UNDEFINED`** in the proved/paper-level
regime.  No finite effective analytic threshold is justified today.  The
paper-level Selberg--Hejhal theorem recorded in
[`LAW_HEJHAL_S7_EXTRACT.md`](LAW_HEJHAL_S7_EXTRACT.md) still gives an
*ineffective existence* onset; this document does not negate that result.  The
exact route-H assembly is valid
as conditional algebra, but its RATE, transport, and continuous-defect premises
are still **`CONJECTURAL`**.  The only explicit finite number below is an
explicitly **`CONJECTURAL / COUNTERFACTUAL`** sensitivity calculation, not a
theorem threshold or forecast.

Here `N` is the Hecke-group index called `q` in the source notes:
`G_N=G_q`, `lambda_N=2 cos(pi/N)`.  Status words are literal:

- **`PROVED`**: proved in the cited repository source or elementary conditional
  algebra checked below;
- **`PAPER-LEVEL`**: source/referee-confirmed on paper, with any repository or
  Lean promotion caveat retained;
- **`MEASURED`**: receipt-backed finite computation only;
- **`CONJECTURAL`**: every unproved analytic or numerical extrapolation.

Primary source: [`R3_R5_ASSEMBLY_PLAN_SOL.md`](R3_R5_ASSEMBLY_PLAN_SOL.md),
especially Sections 5--8.  Current-status cross-checks are cited in the
closure-distance ledger.

## 1. Exact route-H assembly inequality

Put

```text
F_N(s) := phi_N(s) - phi_infty(s).
```

### 1.1 RATE input

The required input is the compact-boundary estimate

```text
E_R(N)
 := sup_{s in Gamma_R} |F_N(s)|
 <= C_R N^(-alpha),                         N >= N_RATE,       (1.1)

C_R > 0,       alpha > 0.
```

The pointwise candidate from R2 is

```text
epsilon_2(N;s)
 := |M(s)| [Delta_X(N,s) + E_N(X,sigma)
            + E_theta(X,sigma) + T_X(N,sigma)],

M(s) := sqrt(pi) Gamma(s-1/2)/Gamma(s).                       (1.2)
```

For R5, (1.2) must be assembled uniformly on the whole right boundary
`Gamma_R`, at a height covering the exact target window, into (1.1).  Today
that promotion is **`CONJECTURAL`**: `C_R`, `alpha`, `N_RATE`, the admissible
growth law `X(N)`, and boundary monotonicity are not proved there.  See
[`R3_R5_ASSEMBLY_PLAN_SOL.md`](R3_R5_ASSEMBLY_PLAN_SOL.md) (1.1),
[`LAW_R2_RATE_LEMMA_DRAFT.md`](LAW_R2_RATE_LEMMA_DRAFT.md) Section 3, and
[`M3_N1N4_PROMOTION_PLAN_SOL.md`](M3_N1N4_PROMOTION_PLAN_SOL.md) Section 2.

### 1.2 First R3 transport

Assume **`CONJECTURALLY`** that the divisor, domain, and family-uniform boundary
gates in the plan hold.  Put

```text
D_0 := D(1/2+i t0, delta/15),
D_1 := D(1/2+i t0, delta/20),
closure(D_+) subset D_0 intersect {Re s>1/2},
nu(z) := harmonic_measure_Omega+(z, Gamma_R).
```

Thus the diameter of `D_1` on `Re s=1/2` is exactly the R4 interval
`|t-t0|<=delta/20`.  Let

```text
nu_seed
 := inf_{z in D_+} harmonic_measure_Omega+(z, Gamma_R),
0 < nu_seed <= 1,

K_+
 := a family-uniform upper bound for |F_N| on every non-RATE
    boundary component of Omega_+.
```

The two-constants theorem then gives the conditional estimate

```text
E_seed(N)
 := sup_{z in D_+} |F_N(z)|
 <= K_+^(1-nu_seed) E_R(N)^nu_seed
 <= K_+^(1-nu_seed) C_R^nu_seed N^(-alpha nu_seed).          (1.3)
```

The algebra from the first to the second line is **`PROVED` conditional on
(1.1) and the first mixing gate in (1.11)**.  The existence of the required
common pole-free domain and the explicit, family-uniform `K_+` and `nu_seed`
are **`CONJECTURAL`**.

### 1.3 Conditional Hejhal disc bound under the zero-free hypothesis

Assume

```text
H0(N,delta): phi_N has no zero in
R_delta^+ = [1/2,1/2+delta] x [t0-delta,t0+delta].            (1.4)
```

Carry the Hejhal constants symbolically:

```text
M_H       := M_7.23(delta,t0,C_6,C_7,m_infty,a/2),
K_H       := C_6 exp(2 M_H/(1-r_H)^2),
K_infty,0 := sup_{z in D_0} |phi_infty(z)|,
K_F       := K_H + K_infty,0.                                (1.5)
```

The intended consequence is

```text
sup_{z in D_0} |phi_N(z)| <= K_H,
sup_{z in D_0} |F_N(z)|   <= K_F.                            (1.6)
```

Equations (1.5)--(1.6) are **`CONJECTURAL`** as instantiated family-uniform
bounds: the exact `C_6`, `C_7`, equation-(7.23) coefficient, and associated
family bookkeeping have not been transcribed and proved.  No coefficient is
filled in here.

### 1.4 Second R3 transport

Let

```text
omega_*
 := inf_{z in D_1, Re z=1/2}
       harmonic_measure_{D_0\closure(D_+)}(z, boundary D_+),
0 < omega_* <= 1.                                           (1.7)
```

The second two-constants step gives

```text
E_3(N)
 := sup_{z in D_1, Re z=1/2} |F_N(z)|
 <= K_F^(1-omega_*) E_seed(N)^omega_*
 <= C_3 N^(-p_3),                                           (1.8)

p_3
 := alpha nu_seed omega_*,                                  (1.9)

C_3
 := K_F^(1-omega_*)
    K_+^(omega_*(1-nu_seed))
    C_R^(omega_* nu_seed).                                  (1.10)
```

The substitutions in (1.3) and (1.8) are valid upper-bound substitutions only
after the monotonicity/mixing gates

```text
E_R(N) <= K_+,
K_+^(1-nu_seed) E_R(N)^nu_seed <= K_F                       (1.11)
```

hold on the activated tail.  This is **`PROVED`** by differentiating the log
of the geometric mix with respect to `nu_seed` and `omega_*`; without (1.11),
replacing harmonic measures by lower bounds can reverse the intended
inequality.  In the threshold ledger below, `N_monotone` includes (1.11).
All geometric and family-uniform premises of (1.7)--(1.10) remain
**`CONJECTURAL`**.

### 1.5 R4 lower side and the contradiction

The required continuous R4 statement is

```text
d_delta
 := inf_{|t-t0|<=delta/20}
      ||phi_infty(1/2+it)|-1|
 > 0.                                                       (1.12)
```

For a finite, one-cusp `G_N`, critical-line unitarity gives
`|phi_N(1/2+it)|=1`.  Hence the reverse triangle inequality gives

```text
d_delta <= |F_N(1/2+it)|.                                  (1.13)
```

Under `H0(N,delta)`, R3 would also give (1.8), so

```text
d_delta <= |F_N(1/2+it)| <= E_3(N) <= C_3 N^(-p_3).         (1.14)
```

Therefore the strict inequality

```text
C_3 N^(-p_3) < d_delta                                     (R5-H)
```

contradicts `H0(N,delta)`.  Its negation supplies a zero of `phi_N` in
`R_delta^+`; exact Hejhal (7.22) then supplies the reflected pole.  This final
logical implication is **`PROVED` conditional on (1.1), (1.3), (1.6), (1.8),
(1.11), (1.12), the divisor gates, and the exact functional identity**.  Those
activated analytic premises are not all proved today, so the resulting R5
theorem remains **`CONJECTURAL`**.

The current R4 receipt does **not** prove (1.12).  If `d_samp=0.6604` is the
rounded-down sampled witness and `Delta_4` is the total interval/interpolation
loss, the honest form is

```text
d_delta = 0.6604 - Delta_4 > 0,
E_3^up(N) + Delta_4 < 0.6604.                               (1.15)
```

Thus `E_3^up(N)<0.6604` alone is **`CONJECTURAL AND INSUFFICIENT`**.  The
continuous bound `Delta_4<0.6604` and its actual value are **`CONJECTURAL`**
until interval-certified.

## 2. Exact integer threshold, still symbolic

The Hejhal anchor used to build `K_F` must activate first.  Choose

```text
s_a := 1/2 + a_a + i t0,       0 < a_a < delta,
m_infty,a := |phi_infty(s_a)| > 0,
nu_a := nu(s_a).
```

This choice is admissible only after interval certification of
`m_infty,a>0` and every divisor exclusion.  In particular,
`delta=0.5, a_a=delta/2=0.25` is forbidden: then `s_a=z_0` and
`phi_infty(s_a)=0`, so it cannot be a lower-bound anchor.  With an admissible
anchor, define

```text
A_A := 2 K_+^(1-nu_a) C_R^nu_a / m_infty,a,
p_A := alpha nu_a,
N_A := floor(A_A^(1/p_A)) + 1.                              (2.1)
```

Define the contradiction crossing

```text
A_C := C_3/d_delta,
p_C := p_3 = alpha nu_seed omega_*,
N_C := floor(A_C^(1/p_C)) + 1.                              (2.2)
```

The prerequisite activation threshold is

```text
N_pre,H := max(12,
               N_RATE, N_M1, N_M2, N_M3, N_C1, N_K+,
               N_C6, N_C7, N_R4, N_divisor,
               N_geometry, N_monotone).                    (2.3)
```

Here `N_monotone` also activates (1.11).  Non-integer analytic gates cannot be
encoded by (2.3); they must already be `PASS`.  The exact pure-power threshold
is

```text
N0^(H) := max(N_pre,H, N_A, N_C).                           (2.4)
```

Conditional on every non-integer gate being `PASS` and the pure-power inputs
holding on the activated tail, **for every integer `N>=N0^(H)`**, the hypothesis
`H0(N,delta)` implies (1.14), while (2.2)--(2.4) imply the strict inequality
(R5-H); hence `H0(N,delta)` is contradictory and the zero/reflected-pole
conclusion follows.

The floor-plus-one is load-bearing: it preserves strictness if a real crossing
is itself an integer.  A bare ceiling is then wrong.

For a general monotone envelope, the exact replacement is

```text
E_3^up(N)
 := K_F(N)^(1-omega_*(N))
    K_+(N)^(omega_*(N)(1-nu_seed(N)))
    E_R(N)^(omega_*(N)nu_seed(N)),

N0^(H,env)
 := min {Q in integers : Q >= N_pre,H and
          sup_{integer N>=Q} E_3^up(N) < d_delta}.           (2.5)
```

If the set in (2.5) is empty or its tail supremum is not proved, the threshold
is `+infinity` by convention and remains **`UNVERIFIABLE`**.  Finite sampling
does not prove the tail supremum.

For completeness, the plan's preferred target-specific route Z would instead
use

```text
N_pre,Z := max(12, N_RATE, N_M1, N_M2, N_M3, N_C1, N_K+,
                    N_divisor, N_geometry, N_monotone),
C_Z := K_+^(1-nu_z) C_R^nu_z,
p_Z := alpha nu_z,
N_Z := floor((C_Z/m_z)^(1/p_Z)) + 1,
N0^(Z) := max(N_pre,Z,N_Z),                                 (2.6)

C_Z N^(-p_Z) < m_z.
```

Route Z avoids R4 but needs a proved closed-contour zero count, `m_z>0`, common
holomorphy, and `nu_z`; all are **`CONJECTURAL`** today.  Because the requested
pincer explicitly runs through the R4 defect, the regime table below uses
route H.

## 3. Three constant regimes

| Regime | Inputs admitted | Implied `N0` | Honest verdict |
|---|---|---:|---|
| **(i) proved/paper-level only** | Elementary inequalities, exact source identities, the paper-level Ford tail, and the paper-level ineffective Selberg--Hejhal existence theorem. No target-boundary `(RATE)`, no completed effective route H/Z, and no continuous R4 infimum. | **No explicit finite `N0`; undefined (`+infinity` convention for this effective assembly).** | `J_proved` is empty. Ineffective existence survives, but it supplies no computable onset. This is the real state today. |
| **(ii) proved + calibrated RATE conjecture** | Add **`CONJECTURAL / MEASURED`** `epsilon(N;s)<=C(sigma,t)N^(1-2sigma)`. At the only R2 calibration cell, the measured `D N^1.2` constant rounded up is `1.64`; the proposed envelope value `C_R=2` is internally contradicted by the printed assembled epsilon table, so it is forbidden as an R5 envelope and remains unvalidated at the target height. R3 constants and the continuous R4 defect are still absent. | **No explicit finite `N0`; undefined.** Formally it remains (2.4) with unknown `C_3,p_3,d_delta,N_A,N_pre,H`. | A pointwise measured `C` at the wrong height is neither `C_R` on `Gamma_R` nor a transport theorem. Ineffective existence still does not provide a number. |
| **(iii) optimistic-but-stated sensitivity model** | **`CONJECTURAL / COUNTERFACTUAL`** assumptions: `sigma=1.1`, `alpha=1.2`, `C_R=2`, `N_RATE=24`; `nu_seed=omega_*=1/2`; `K_+=K_F=1`; `Delta_4=0`, so `d_delta=0.6604`; and every anchor/prerequisite gate, including `N_A`, activates by `24`. | `C_3=2^(1/4)`, `p_3=0.3`, `N_C=8`, hence **`N0=max(24,8)=24`**. | Not admissible evidence. It deliberately fills every missing transport/defect constant optimistically; `C_R=2` already fails as an upper bound for the printed assembled epsilon values. It is only a scale/sensitivity receipt. |

Even the lossless counterfactual `nu_seed=omega_*=1` would give the bare
crossing `N_C=3`, but the activation assumption still forces `N0=24`.  This is
also **`CONJECTURAL / COUNTERFACTUAL`**, and harmonic measures equal to one are
not asserted for the actual geometry.

The conclusion of the table is deliberately asymmetric: regimes (i) and (ii)
do not produce large effective numbers; they produce **no explicit or receipted
threshold at all**, while leaving the paper-level ineffective existence result
intact.  Only the explicitly invented regime (iii) produces `24`, and that
value must not be quoted without its counterfactual label.

## 4. Numeric receipts

Every numerical value used above comes from one of the following commands run
for this execution.  Decimal empirical constants are rounded **up**; the R4
witness is rounded **down**.

### Receipt A — target, empirical constants, convergence, R4 witness, and the
### `C_R=2` obstruction

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 /Users/za/miniforge3/envs/pari-arb/bin/python3 - <<'PY'
import json
from decimal import Decimal, ROUND_CEILING
from pathlib import Path
import mpmath as mp
mp.mp.dps = 80
base=Path('research_notes/rh_goals_2026-08-14/lane_g/law_probes')
rows=json.loads((base/'rate_measure_data.json').read_text())
r4=json.loads((base/'r4_defect_data.json').read_text())
print('backend=mpmath dps=', mp.mp.dps)
t0=mp.im(mp.zetazero(1))/2
t_meas=mp.mpf('7.0665')
print('t0=', mp.nstr(t0,60))
print('t0_minus_t_meas=', mp.nstr(t0-t_meas,60))
for sigma,t in [(1.1,.5),(1.1,1.5),(1.25,.5),(1.25,1.5)]:
    sub=[r for r in rows if r['sigma']==sigma and r['t']==t]
    best=max(sub,key=lambda r: mp.mpf(str(r['D']))*mp.mpf(r['q'])**(2*mp.mpf(str(sigma))-1))
    C=mp.mpf(str(best['D']))*mp.mpf(best['q'])**(2*mp.mpf(str(sigma))-1)
    C_up=Decimal(str(C)).quantize(Decimal('0.01'),rounding=ROUND_CEILING)
    print(f'Ccell sigma={sigma} t={t} alpha={2*sigma-1:.2f} max_raw={mp.nstr(C,18)} at_N={best["q"]} conv={best["convergence_reldiff"]:.18g} C_up_0.01={C_up}')
target=[r for r in rows if r['t']==7.0665]
print('target_t_meas_rows=',len(target))
print('target_conv_min=',min(r['convergence_reldiff'] for r in target))
print('target_conv_max=',max(r['convergence_reldiff'] for r in target))
for key,rec in r4['anchor_online'].items():
    print(key,'sample_min=',rec['min'][1])
print('combined_sample_witness_down=0.6604')
for N,e in [(12,.6900),(16,.4645),(24,.2042),(32,.0973),(48,.0376)]:
    print('printed_epsilon_scaled',N,mp.nstr(mp.mpf(str(e))*mp.mpf(N)**mp.mpf('1.2'),18))
PY
```

Output:

```text
backend=mpmath dps= 80
t0= 7.06736257086734689522862599178123513539212855784962158784278
t0_minus_t_meas= 0.00086257086734689522862599178123513539212855784962158784278373
Ccell sigma=1.1 t=0.5 alpha=1.20 max_raw=2.77240637214719865 at_N=12 conv=9.13206234421075173e-07 C_up_0.01=2.78
Ccell sigma=1.1 t=1.5 alpha=1.20 max_raw=1.63890701753367635 at_N=24 conv=1.00366450159427567e-06 C_up_0.01=1.64
Ccell sigma=1.25 t=0.5 alpha=1.50 max_raw=4.17884069501319972 at_N=12 conv=2.22548443423853992e-06 C_up_0.01=4.18
Ccell sigma=1.25 t=1.5 alpha=1.50 max_raw=2.10705195463825441 at_N=32 conv=1.195191328742225e-06 C_up_0.01=2.11
target_t_meas_rows= 12
target_conv_min= 0.004455321695914483
target_conv_max= 0.025405127702252315
delta=0.1_online sample_min= 0.66126507774966940973187410052062260279176987412865
delta=0.5_online sample_min= 0.66043577698038089055374927033365063635956765148256
combined_sample_witness_down=0.6604
printed_epsilon_scaled 12 13.6102651484026293
printed_epsilon_scaled 16 12.9398635728335892
printed_epsilon_scaled 24 9.25356815070811127
printed_epsilon_scaled 32 6.2272
printed_epsilon_scaled 48 3.91450930531521292
```

Interpretation, preserving source caveats:

- The exact target and the RATE sweep height differ by the printed positive
  offset.  M3 must bridge this; treating them as identical is
  **`CONJECTURAL`**.
- The empirical constants are **`MEASURED`**, not RATE upper bounds.  The
  target-height rows have the displayed truncation disagreement and are not
  trustworthy calibration data.
- Every printed assembled `epsilon(N) N^1.2` value exceeds `2`.  Therefore the
  proposed `C_R=2` cannot majorize that envelope; using it in regime (iii) is
  explicitly counterfactual.
- The R4 numbers are sampled minima.  Only `0.6604` is used, rounded down; it is
  not a continuous infimum.

### Receipt B — outward-rounded strict crossings

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import arb, ctx
ctx.prec = 256
d = arb(6604) / 10000
C = arb(2)
lossless = (C / d) ** (arb(5) / 6)
C3_half = C ** (arb(1) / 4)
half = (C3_half / d) ** (arb(10) / 3)
print('backend=python-flint Arb prec_bits=', ctx.prec)
print('d_samp_down=', d)
print('lossless_crossing=', lossless)
print('lossless_qC=floor(crossing)+1=3')
print('half_transport_C3=', C3_half)
print('half_transport_p3=0.3')
print('half_transport_crossing=', half)
print('half_transport_qC=floor(crossing)+1=8')
print('with_q_pre_24_lossless_N0=max(24,3)=24')
print('with_q_pre_24_half_N0=max(24,8)=24')
PY
```

Output:

```text
backend=python-flint Arb prec_bits= 256
d_samp_down= [0.6604000000000000000000000000000000000000000000000000000000000000000000000000 +/- 1.50e-77]
lossless_crossing= [2.517787709548932812118037456448669960368047540240618691573218641656421004933 +/- 6.43e-76]
lossless_qC=floor(crossing)+1=3
half_transport_C3= [1.189207115002721066717499970560475915292972092463817413019002224719466668227 +/- 1.14e-76]
half_transport_p3=0.3
half_transport_crossing= [7.10397538158507015689084580391404659383579303999221732318655486294865984065 +/- 2.02e-75]
half_transport_qC=floor(crossing)+1=8
with_q_pre_24_lossless_N0=max(24,3)=24
with_q_pre_24_half_N0=max(24,8)=24
```

Both Arb balls lie strictly between the adjacent integers used by the
floor-plus-one calculation, so the strict thresholds in the counterfactual
model are unambiguous.  This certifies only the arithmetic, not any assumed
analytic constant.

## 5. Closure-distance ledger

| Piece | Current status | Exact contribution to R5 | What must exist before a finite real `N0` |
|---|---|---|---|
| **M1-coset** | **`CONJECTURAL`**. [`M1_COSET_STRATEGY_SOL.md`](M1_COSET_STRATEGY_SOL.md) is strategy only; M1-W/I/S/L remain open. The old `c`-only proxy is false, while the finite v27 algebra does not prove the coset theorem. | Makes the matched/escaping decomposition in (1.2) a theorem; supplies well-definedness, injectivity, surjectivity below the cutoff, and localization of the complement. Together with the still-required N1/N3/N4 estimates, it permits the weighted matched sum and the `N^(3-2sigma)` scale on the current RATE band `1.1<=sigma<=1.25` (hence `1<sigma<3/2`); an extension must instead use `O(log N)` at `sigma=3/2` and `O(1)` above. M1 alone does not prove RATE or its exponent. | A canonical full-key `(c,d mod c)` specialization theorem and explicit complement/cutoff bound, with an activation `N_M1`. Without it, `C_R` and `alpha` are not theorem-defined. |
| **M2 per-term / tails** | The Ford cumulative raw-tail bound is **`PAPER-LEVEL`** confirmed in [`M2_FORD_PACKING_REFEREE.md`](M2_FORD_PACKING_REFEREE.md); repository/Lean promotion is open. The separate Hejhal-7.7/Ch.6 per-term constants and family-uniform `C_6`/Theorem-12.9 bookkeeping remain **`CONJECTURAL`**. The old G1/G2 route is false and retired. | Ford controls the finite and theta raw-tail inputs to (1.2); it does **not** supply `K_H`. Separately, the missing per-term/Ch.6 bounds must supply the summable, family-uniform non-RATE inputs used in `K_+` and the Hejhal disc bound. Raw tail size alone does not control the `N`-dependent matched drift. | An explicit per-term majorant in the exact normalization, all hidden Ch.6 constants instantiated and family-uniform, and an activation `N_M2`/`N_C6`. |
| **M3** | **`CONJECTURAL / OPEN`**. The R2 assembly is single-cell; the exact-target rows are unconverged. | Promotes (1.2) to the boundary supremum (1.1), producing the load-bearing `C_R`, `alpha`, `N_RATE`, `X(N)`, and proved monotonicity over the exact height window. | An interval/analytic certificate on the whole frozen `Gamma_R`, including exact `t0`, not a point fit or a nearby-height measurement. |
| **R3 transport** | **`CONJECTURAL / OPEN`**. The plan supplies interfaces, not evaluated constants. | Produces `nu_seed`, `omega_*`, `K_+`, `K_F`, hence `p_3` and `C_3`; under `H0` it moves RATE from `Gamma_R` to the critical-line comparison. It also produces the anchor gate `N_A`. | Common pole-free domains, divisor clearances, exact harmonic-measure lower bounds, family-uniform boundary/disc bounds, the Hejhal log-area constants, and the mixing inequalities (1.11). |
| **R4 continuous defect** | **`MEASURED`** sampled witness only; the interval statement is **`CONJECTURAL`**. | Supplies the positive denominator `d_delta=0.6604-Delta_4` in (2.2). | Direct interval evaluation or a proved interpolation loss `Delta_4` with `d_delta>0`, plus activation `N_R4`. |
| **R5 monotonicity / integer tail** | **`CONJECTURAL`** until the preceding bounds exist. | Turns a point crossing into the for-all-`N>=N0` statement and validates floor-plus-one strictness. | Prove the tail supremum in (2.5), all activation thresholds, and the selected route's non-numeric analytic gates. |
| **Finite base** | Separate from the analytic threshold. Current certificate coverage is not re-audited here, so any coverage claim would be **`CONJECTURAL`**. | Closes the family below the analytic threshold. | Reopen artifact-level certificates and prove `N_cert >= N0_analytic-1` in the declared target class. |

The pincer is therefore not “a large-constant estimate away.”  It is missing
the objects that define the exponent `p_3`, constant `C_3`, positive continuous
margin `d_delta`, and activation maximum.  Closing M2's raw tail alone does not
create any of those.  Closing the calibrated RATE conjecture alone still leaves
R3 and R4 undefined.  An explicit effective `N0` becomes real only after one
complete route enters `J_proved`; at present `J_proved` is empty, so

```text
N0_analytic,effective = min {N0^(j) : j in J_proved}
                      = undefined                  (equivalently +infinity).
```

This statement is about effectivity and does not contradict the paper-level
ineffective existence theorem.  That is the corrected bring-it-home map.
