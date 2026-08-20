# Constant-chain autopsy: `C_R`

**Date:** 2026-08-20  
**Lane:** G3 / LUNA  
**Scope:** analysis only; no proof, theorem-status, or repair claim  
**Target:** `C_R = 10489412368759562746433608215977724802` in
`BOUNDARY_ALPHA_THEOREM_SOL.md`

## 0. Verdict

The source chain is

\[
C_R=\left\lceil M_0\left(C_{\rm pair}+C_{\rm wrap}\right)\right\rceil,
\]

with

\[
\begin{aligned}
C_{\rm pair}
  &=2\pi^2(S+1)pC_4F(12),\\
C_{\rm wrap}
  &=p\,128(1+\log 2)\,30,
\end{aligned}
\]

where `p=11/5`, `S=7.648`, `M_0=2.775`, `C_4=2^100`, and
`F(12)=1225/4+91605/12=7940`.
The source receipts are `BOUNDARY_ALPHA_THEOREM_SOL.md:140-191,
510-579`, with the pair inequality at `:510-522`, the `q>=12` absorption at
`:529-540`, and the wrap estimate at `:556-560`.

The orders die in two places:

1. `C_4=2^100` contributes `log C_4=69.314718...` of the final
   `log C_R=85.243430...`. The atom bridge separately records a direct
   `2^63` ceiling, leaving `2^37` of declared headroom
   (`ATOM_MOMENT_BRIDGE_SOL.md:491-508`). This is the dominant
   lossy-by-convenience budget.
2. The layer-cake envelope `F(12)=7940` contributes `log F=8.979669...`.
   At the declared `p=11/5` and `q_RATE=12`, this is an endpoint value of the
   displayed positive formula, not decimal rounding. Its large `J_4` term is
   driven by the choice `p-2=1/5`; changing `p` would also change the decay
   exponent and is therefore only a sensitivity target, not a repair.

The wrap branch has `log C_wrap=9.568274...` but is additive and only
`3.7841e-33` of the pair branch. The outward integer ceiling changes the raw
value by less than `8.1e-38` relatively. Neither is an order-of-magnitude
source.

No status is upgraded here. Every proposed reduction below is labelled
**CONJECTURAL**.

## 1. Source chain and receipts

### 1.1 Analytic assembly

The source gives the atom-moment envelope with declared `C_4=2^100` at
`BOUNDARY_ALPHA_THEOREM_SOL.md:403-431`. Its layer-cake consequence is
`BOUNDARY_ALPHA_THEOREM_SOL.md:433-455`, and the shallow/deep conversion is
`BOUNDARY_ALPHA_THEOREM_SOL.md:457-522`:

\[
E_{\rm pair,all}(q,s)
\le 2\pi^2(|s|+1)pC_4
\left[
 \left({1\over3-p}+J_2(p)\right)q^{1-p}+J_4(p)q^{-p}
\right].
\]

At `p=11/5`, the source records

\[
J_2=305,\qquad J_4=91605,\qquad
F(q)=\frac{1225}{4}+\frac{91605}{q},
\]

and absorbs `F(q)<=F(12)=7940` for `q>=12`
(`BOUNDARY_ALPHA_THEOREM_SOL.md:529-540`). The contour bound is
`S=sup|s|<7.648` at `:542-546`; the beta-integral prefactor is
`M_0<2.775` at `:562-567`, with its uniform proof at
`M3_UNIFORMITY_EXECUTION_SOL.md:255-279`.

The independent wrap source is
`FW_RENEWAL_COUNT_SOL.md:475-498`, which supplies

\[
C_1=128(1+\log2),\qquad
G(p)=\frac1{p-2}+\frac1{(p-2)^2}.
\]

At `p=11/5`, `G=30`; this is consumed at
`BOUNDARY_ALPHA_THEOREM_SOL.md:234-243,556-560`.

The final positive assembly and outward integer selection are at
`BOUNDARY_ALPHA_THEOREM_SOL.md:136-138,573-582`.

### 1.2 Required mpmath log receipt

Every value and natural logarithm in the tables below was computed by the
following quoted command, using the required interpreter:

```bash
/Users/za/miniforge3/envs/pari-arb/bin/python3 - <<'PY'
from mpmath import mp
mp.dps = 80

def show(name, value):
    print(f'{name} value={mp.nstr(value, 50)} log={mp.nstr(mp.log(value), 50)}')

p = mp.mpf(11)/5
S = mp.mpf('7.648')
M0 = mp.mpf('2.775')
C4 = mp.mpf(2)**100
F0 = mp.mpf(1225)/4
F1 = mp.mpf(91605)/12
F = F0 + F1
pair_pref = 2 * mp.pi**2 * (S+1) * p
pair = pair_pref * C4 * F
wrap = p * 128 * (1+mp.log(2)) * 30
raw = M0 * (pair + wrap)
CR = mp.mpf(10489412368759562746433608215977724802)

for name, value in [
    ('CR', CR), ('M0', M0), ('pair_pref', pair_pref), ('pair', pair),
    ('wrap', wrap), ('pair_plus_wrap', pair+wrap),
    ('two', mp.mpf(2)), ('pi_squared', mp.pi**2), ('S_plus_one', S+1),
    ('p', p), ('C4', C4), ('F', F), ('F0_1225_over_4', F0),
    ('F1_91605_over_12', F1), ('wrap_128', mp.mpf(128)),
    ('wrap_1_plus_log2', 1+mp.log(2)), ('wrap_G', mp.mpf(30)),
    ('core_convolution_2^12', mp.mpf(2)**12),
    ('finite_tags_bound_2^20', mp.mpf(2)**20),
    ('finite_tags_explicit_82944', mp.mpf(82944)),
    ('product_gain_40_squared', mp.mpf(40)**2),
    ('product_gain_exact_(4pi^2)^2', (4*mp.pi**2)**2),
    ('four_zeta_sums_2^4', mp.mpf(2)**4),
    ('four_zeta_sums_exact_(pi^2/6)^4', (mp.pi**2/6)**4),
    ('low_regime_2^11', mp.mpf(2)**11),
    ('high_regime_2^14', mp.mpf(2)**14),
    ('ordered_distinct_2', mp.mpf(2)),
    ('direct_A2_2^62', mp.mpf(2)**62),
    ('C_atom_2^63', mp.mpf(2)**63),
    ('C4_slack_2^37', mp.mpf(2)**37),
]:
    show(name, value)
print('wrap_over_pair_log=', mp.nstr(mp.log(wrap/pair), 50))
Sraw = mp.mpf('7.646893243596647842577572508297090015450131')
print('S_rounding_log=', mp.nstr(mp.log(S/Sraw), 50))
print('tag_reduction_log=', mp.nstr(mp.log((mp.mpf(2)**20)/82944), 50))
print('high_pre_reduction_log=', mp.nstr(mp.log((mp.mpf(2)**14)/(mp.mpf(2)**5+mp.mpf(2)**13)), 50))
print('low_pre_reduction_log=', mp.nstr(mp.log((mp.mpf(2)**11)/(mp.mpf(2)**8+mp.mpf(2)**10)), 50))
print('four_zeta_reduction_log=', mp.nstr(mp.log((mp.mpf(2)**4)/((mp.pi**2/6)**4)), 50))
print('product_gain_reduction_log=', mp.nstr(mp.log((mp.mpf(40)**2)/((4*mp.pi**2)**2)), 50))
print('alpha_inverse=', mp.nstr(1/(mp.mpf(6)/5), 50))
PY
```

Selected output, including all table logs:

```text
CR value=10489412368759562746433608215977724802.0 log=85.243429750394033162143449533297358736094213311299
M0 value=2.775 log=1.0206507471983978329108852103532555247954663876411
pair_pref value=375.5502909867314026769949839344874020800486388848 log=5.9283923929599229809906965708070425604278220139149
pair value=3779968421174617205922020978730697336.3474162155785 log=84.222779003195635329232564322944099427136724824055
wrap value=14303.707381370417973956776962078675647101825075 log=9.5682740400850871926891490762438587660767651253615
two value=2.0 log=0.69314718055994530941723212145817656807550013436026
pi_squared value=9.8696044010893586188344909998761511353 log=2.2894597716988003482868547027061174233
S_plus_one value=8.648 log=2.1573280803369071538254255019038069088
p value=2.2 log=0.7884573603642701694611842447389416603
C4 value=1267650600228229401496703205376.0 log=69.31471805599453094172321214581765680755
F value=7940.0 log=8.9796685542411814065186556063194000592
F0_1225_over_4 value=306.25 log=5.7244017618589367405777599104223816022
F1_91605_over_12 value=7633.75 log=8.9403344845373445084752567440150226888
wrap_128 value=128.0 log=4.8520302639196171659206248502072359765
wrap_1_plus_log2 value=1.6931471805599453094 log=0.5265890341390444818941032896907912170
wrap_G value=30.0 log=3.4011973816621553754132366916068899122
core_convolution_2^12 value=4096.0 log=8.3177661667193437130067854574981188169
finite_tags_bound_2^20 value=1048576.0 log=13.862943611198906188344642429163531362
finite_tags_explicit_82944 value=82944.0 log=11.325920960271891859753302162271868499
product_gain_40_squared value=1600.0 log=7.377758908227872605704911395201434688
product_gain_exact_(4pi^2)^2 value=1558.5454565440389958 log=7.351508265637381934242637891244941119
four_zeta_sums_2^4 value=16.0 log=2.7725887222397812376689284858327062723
four_zeta_sums_exact_(pi^2/6)^4 value=7.3213973889433441413 log=1.9908012098829813898975093773016606023
low_regime_2^11 value=2048.0 log=7.6246189861593984035895533360399422488
high_regime_2^14 value=16384.0 log=9.7040605278392343318412497004144719531
ordered_distinct_2 value=2.0 log=0.6931471805599453094172321214581765681
direct_A2_2^62 value=4611686018427387904.0 log=42.975125194716609183868391530406947221
C_atom_2^63 value=9223372036854775808.0 log=43.668272375276554493285623651865123789
C4_slack_2^37 value=137438953472.0 log=25.646445680717976448437588493952533019
wrap_over_pair_log=-74.654504963110548136543415246700240661
S_rounding_log=0.00014472234459658248447749718473461346
tag_reduction_log=2.537022650927014328591340266891662862
high_pre_reduction_log=0.689248540144287986403294778362333661
low_pre_reduction_log=0.470003629245735553650937031148342065
four_zeta_reduction_log=0.781787512356799847771419108531045670
product_gain_reduction_log=0.026250642590490671462273503956493569
alpha_inverse=0.83333333333333333333333333333333333333
```

The `pair_plus_wrap` and raw-ceiling checks in the source Arb receipt are
`BOUNDARY_ALPHA_THEOREM_SOL.md:183-191`:

```text
C_pair_D_upper=3779968421174617205922020978730697336.3474...
C_wrap_D_upper=14303.7073813704179...
C_R_raw_upper=10489412368759562746433608215977724801.1520...
C_R=10489412368759562746433608215977724802 strict_upper=True
```

## 2. Loss table: outer `C_R` chain

The table is sorted by the natural-log size of the displayed factor or
additive contribution. “Effective reduction” means a reduction in the final
`C_R` chain, not merely the log of a term that is later dominated by another
positive term. All estimates in the last column are **CONJECTURAL**.

| factor / contribution | value; natural log | introduced by | classification | **CONJECTURAL** plausible reduction if redone carefully |
|---|---:|---|---|---:|
| `C_4` | `2^100 = 1.2676506002e30`; `69.314718055995` | Atom-moment envelope consumed in `BOUNDARY_ALPHA_THEOREM_SOL.md:403-431,433-455`; direct bridge ledger at `ATOM_MOMENT_BRIDGE_SOL.md:491-508` | **Lossy by convenience.** The source bridge records direct `C_atom=2^63`, while the RATE-A scalar remains `2^100`. | Replace the declared budget by `2^63`: `25.646446` e-fold of `C_R` (`2^37`), confidence `0.95`. This is an analysis estimate, not a status change. |
| `F(12)` | `7940`; `8.979668554241` | Positive layer cake and `q>=12` absorption, `BOUNDARY_ALPHA_THEOREM_SOL.md:433-455,529-540` | **Structural at fixed scope.** It is the exact endpoint of the displayed uniform `F(q)=1225/4+91605/q` at `q=12`; not decimal padding. | `0` under fixed `p=11/5`, `q_RATE=12`. A joint `p` redesign can be a separate sensitivity target; see §4. |
| wrap `128` | `128`; `4.852030263920` | `C_1=128(1+log 2)` in `FW_RENEWAL_COUNT_SOL.md:455-472` | **Lossy by convenience** in the overflow counting envelope. | At most `4.852030` e-fold of the wrap branch, but effectively `<3.8e-33` e-fold of final `C_R` because wrap is additive; confidence `0.45`. |
| wrap `G(11/5)` | `30`; `3.401197381662` | `G(p)=1/(p-2)+1/(p-2)^2`, `FW_RENEWAL_COUNT_SOL.md:475-498`; substitution at `BOUNDARY_ALPHA_THEOREM_SOL.md:556-560` | **Structural** for fixed `p=11/5`: it is the exact positive integral value. | `0` at fixed `p`; any change belongs to a joint exponent redesign. Effective final reduction is negligible. |
| `pi^2` | `9.869604401089`; `2.289459771699` | `delta_q<=pi^2/q^2` and bridge/path conversion, `BOUNDARY_ALPHA_THEOREM_SOL.md:457-501`; underlying `4pi^2` bridge at `ATOM_MOMENT_BRIDGE_SOL.md:253-265` | Mixed: the `q^-2` analytic scale is **structural**; the use of a scalar upper envelope is **convenience**. | **CONJECTURAL:** `<0.1` e-fold in the pair coefficient; effective final gain is small. |
| `S+1` | `8.648`; `2.157328080337` | `S<7.648` and the `(|s|+1)` factor, `BOUNDARY_ALPHA_THEOREM_SOL.md:510-546` | `+1` is structural in the displayed MVT/absolute bound; the decimal `S` ceiling is convenience. | **CONJECTURAL:** about `0.000145` e-fold from replacing `7.648` by the printed raw `7.646893...`; no order recovery. |
| `M_0` | `2.775`; `1.020650747198` | Beta-integral prefactor, `BOUNDARY_ALPHA_THEOREM_SOL.md:562-577`; `M3_UNIFORMITY_EXECUTION_SOL.md:255-279` | **Structural.** The source notes the supremum is attained at `s=1.1`; only the outward decimal ceiling is convenient. | **CONJECTURAL:** `<0.001` e-fold from more digits; no material reduction. |
| `p` | `2.2`; `0.788457360364` | Choice `p=11/5` in `BOUNDARY_ALPHA_THEOREM_SOL.md:529-534`, with `alpha=p-1=6/5` | **Structural choice/tradeoff.** It controls both `F` and the RATE exponent. | `0` if `alpha=6/5` is held fixed. Any retuning is a new joint optimization, not a local repair. |
| shallow/deep factor `2` | `2`; `0.693147180560` | MVT/absolute bounds and enlargement to the full positive sum, `BOUNDARY_ALPHA_THEOREM_SOL.md:472-501` | **Lossy by convenience**: triangle/absolute-value and overlapping full-sum enlargement. | **CONJECTURAL:** at most `0.693147` e-fold in the pair branch; confidence `0.35`. |
| wrap `(1+log 2)` | `1.693147180560`; `0.526589034139` | `C_1` in `FW_RENEWAL_COUNT_SOL.md:455-462` | **Lossy by convenience** from the `h` to `q` logarithmic envelope. | **CONJECTURAL:** at most `0.526589` e-fold of wrap; effective final gain negligible. |

The pair subtotal is `3.779968421174617e36` with log `84.222779003196`;
the final `M_0` multiplication gives the displayed `log C_R` once the
negligible wrap is added. Thus the `C_4` term alone is about `81%` of the
final natural-log budget; `F(12)` is the next material term at about `10.5%`.

## 3. Atom-moment subledger: where the `2^37` headroom sits

The following are the source components of the direct atom-moment accounting
at `ATOM_MOMENT_BRIDGE_SOL.md:454-508`; they are **not** to be multiplied a
second time after the outer `C_4` row. The source's component product closes at
`2^62` for the direct `A_X^2` subtotal and then at `2^63` after the Ford unit
term, while the RATE-A declaration remains `2^100`.

| source component / subtotal marker | value; natural log | introduction | classification | **CONJECTURAL** reduction estimate |
|---|---:|---|---|---:|
| declared `C_4` | `2^100`; `69.314718055995` | `ATOM_MOMENT_BRIDGE_SOL.md:491-508` | **Lossy by convenience:** final `2^k` padding above the direct bridge | `25.646446` e-fold to `2^63`; confidence `0.95` |
| `C_atom` subtotal | `2^63`; `43.668272375277` | Ford unit plus direct subtotal, `ATOM_MOMENT_BRIDGE_SOL.md:472-508` | Subtotal marker, not an additional component | `0` as the already recorded direct bridge ceiling; any smaller value is **CONJECTURAL** |
| direct `A_X^2` subtotal | `2^62`; `42.975125194717` | `ATOM_MOMENT_BRIDGE_SOL.md:454-489` | Subtotal marker, not an additional component | **CONJECTURAL:** further tightening is possible in principle, but no numeric target is justified here |
| finite tags | `2^20`; `13.862943611199` | Explicit tag count and bound, `ATOM_MOMENT_BRIDGE_SOL.md:245-251` | **Lossy by convenience:** `82944<2^17` is recorded, but `2^20` is carried | Exact tag-bound replacement would save `log(2^20/82944)=2.537023` e-fold; confidence `0.75` |
| high-regime sum | `2^14`; `9.704060527839` | `ATOM_MOMENT_BRIDGE_SOL.md:389-451` | **Lossy by convenience:** `2^5+2^13<2^14`, plus preceding regime envelope | The immediate pre-ceiling save is `0.689249` e-fold; a fuller regime audit is **CONJECTURAL**, up to roughly `1-3` e-fold, confidence `0.45` |
| core convolution | `2^12`; `8.317766166719` | Dyadic three-core overcount, `ATOM_MOMENT_BRIDGE_SOL.md:175-201` | **Lossy by convenience:** shell/tag convolution is deliberately coarse | **CONJECTURAL:** roughly `1-4` e-fold, confidence `0.35`; no certified replacement is asserted |
| low-regime sum | `2^11`; `7.624618986159` | `ATOM_MOMENT_BRIDGE_SOL.md:345-387` | **Lossy by convenience:** `2^8+2^10<2^11` | Immediate pre-ceiling save is `log(2048/1280)=0.470004` e-fold; effective downstream save is **CONJECTURAL** and small |
| product-gain conversion | `40^2=1600`; `7.377758908228` | `4pi^2<40` conversion, `ATOM_MOMENT_BRIDGE_SOL.md:253-265` | Mostly structural bridge geometry; small convenience ceiling | Exact `(4pi^2)^2` would save only `0.026251` e-fold; confidence `0.9` |
| four auxiliary sums | `2^4`; `2.772588722240` | Four `sum(1+r)^-2<2` bounds, `ATOM_MOMENT_BRIDGE_SOL.md:267-291` | **Lossy by convenience:** exact sum is `pi^2/6`, not `2` | Exact replacement saves `0.781788` e-fold; confidence `0.8` |
| ordered-distinct factor | `2`; `0.693147180560` | Conservative factor in `A_X^2`, `ATOM_MOMENT_BRIDGE_SOL.md:293-300,454-469` | **Lossy by convenience** | **CONJECTURAL:** up to `0.693147` e-fold; confidence `0.7` |

The dominant fact is the gap between the direct subtotal and the declared
constant:

\[
\log(2^{100}/2^{63})=37\log2=25.646445680718.
\]

The smaller internal ceilings are real audit targets, but they do not compete
with the 37-bit declaration gap.

## 4. Top-three reduction targets

Ranking uses `(plausible log reduction) x (confidence)`. The scores are a
triage heuristic only; every item remains **CONJECTURAL** and no theorem
constant is changed here.

| rank | target | plausible log reduction | confidence | score | reason |
|---:|---|---:|---:|---:|---|
| 1 | Consume the direct atom bridge instead of the `2^100` declaration; use `2^63` as the sensitivity baseline | `25.646446` e-fold | `0.95` | `24.364` | The `2^63` receipt and the `2^37` gap are explicit in `ATOM_MOMENT_BRIDGE_SOL.md:491-508`; downstream substitution is not being claimed here. |
| 2 | Replace the finite-tag ceiling `2^20` by the explicit count `82944` inside a fresh ledger audit | `2.537023` e-fold | `0.75` | `1.903` | The exact count is already printed at `ATOM_MOMENT_BRIDGE_SOL.md:245-249`; preserving every later injection/summation inequality would still need a separate audit. |
| 3 | Jointly retune the layer-cake parameter `p` rather than treating `p=11/5` as fixed | `3.152870` e-fold in `F(12)` for the sensitivity point `p=2.4` | `0.35` | `1.104` | mpmath sensitivity gives `F_2.2(12)=7940` and `F_2.4(12)=339.270833...`; however `alpha` changes from `1.2` to `1.4`, so this is not a like-for-like constant replacement. |

Near misses: the core-convolution ceiling is visibly coarse but its plausible
reduction is not numerically pinned down; the exact four-zeta-sum replacement
is only `0.781788` e-fold; the `40^2` replacement is `0.026251` e-fold. The
wrap constants are even less attractive because the whole wrap branch is
already `3.7841e-33` of the pair branch.

The sensitivity values in the third row were computed by this additional
required-interpreter receipt:

```bash
/Users/za/miniforge3/envs/pari-arb/bin/python3 - <<'PY'
from mpmath import mp
mp.dps = 80
def F(p):
    j2=1/(p-2)+2/(p-2)**2+2/(p-2)**3
    j4=1/(p-2)+4/(p-2)**2+12/(p-2)**3+24/(p-2)**4+24/(p-2)**5
    return 1/(3-p)+j2+j4/12
f22=F(mp.mpf('2.2'))
for p in [mp.mpf('2.2'), mp.mpf('2.4')]:
    f=F(p)
    print('p=', p, 'alpha=', p-1, 'F12=', mp.nstr(f,40),
          'logF12=', mp.nstr(mp.log(f),40))
print('log_reduction_2.2_to_2.4=',
      mp.nstr(mp.log(f22/F(mp.mpf('2.4'))),40))
PY
```

```text
p= 2.2 alpha= 1.2 F12= 7940.0 logF12= 8.979668554241181406518655606319400059159
p= 2.4 alpha= 1.4 F12= 339.2708333333333333333333333333333333333 logF12= 5.826798706802442936362202657592284495
log_reduction_2.2_to_2.4= 3.152869847438738470156452948726960775
```

## 5. One e-fold of `C_R` buys `5/6` e-fold of `log q_0`

The source transport inequality is
`BOUNDARY_ALPHA_THEOREM_SOL.md:609-644`:

\[
K_+^{1-\nu}(C_Rq^{-\alpha})^\nu<m,
\qquad \alpha=\frac65.
\]

Taking logs and solving for the analytic transport threshold gives

\[
\log q>
\frac{(1-\nu)\log K_+-\log m}{\alpha\nu}
 +\frac1\alpha\log C_R.
\]

Therefore

\[
\frac{\partial(\log q_{\rm transport})}{\partial(\log C_R)}
 =\frac1\alpha=\frac5{6}.
\]

An e-fold reduction means `C_R -> C_R/e`, so
`Delta log C_R=-1` and

\[
\Delta\log q_{\rm transport}=-\frac56.
\]

Thus one e-fold of `C_R` reduction buys `5/6` e-fold of the analytic
transport threshold, provided that this transport term remains the active
term in the eventual `q_0=max(...)`. The mpmath receipt above prints
`1/alpha=0.833333333333...`.

## 6. Status boundary

- This note is an autopsy, not a proof or repair.
- The source `2^63` bridge is recorded as a receipt for locating slack; no new
  theorem constant is installed here.
- All reduction amounts and confidence scores in §§2-4 are **CONJECTURAL**.
- No claim is made that any candidate reduction preserves the full theorem
  ledger, activation gates, machine formalization, or downstream status.

READY FOR JUDGING
