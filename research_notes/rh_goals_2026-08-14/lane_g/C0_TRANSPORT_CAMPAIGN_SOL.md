# The \(c_0\) transport-constant campaign

**Date:** 2026-08-18  
**Lane:** G / R3--R5  
**Interpreter:** `/Users/za/.venvs/farey-rh/bin/python` (`python-flint`/Arb)  
**Rounding rule:** margins DOWN, bounds UP.  
**Status:** the transport calculation below is proved **conditional** on the
same missing full-side `(RATE)`, finite-family holomorphy/divisor, and activation
gates as `R3_ROUTE_B_TRANSPORT_SOL.md`.  Those inputs remain **OPEN**; hence the
current unconditional \(q_0\) is **`UNDEFINED`**.  Every bounded numerical search
is labelled as such and is not promoted to a global optimization theorem.

## 0. Verdict

The orders of magnitude die in two places, not in decimal rounding.

1. Route B multiplies two harmonic-measure floors.  Its printed
   \(c_0=1.827324\times10^{-5}\) is only \(0.140641\%\) below the product of
   the unrounded printed barriers.  Rounding is irrelevant.
2. Between those propagations, the Lemma-7.9/7.10 chain inserts
   \(\log K_F<57984\), producing the base \(56155\).  No harmonic-measure
   product can offset that base at \(q=12,100,1000\): with \(C_R=1\), the old
   chain would need respectively
   \(c_0>18832.168,10161.662,6774.441\), whereas a product of harmonic
   measures is at most one.

Two genuine convenience losses can be removed without changing the theorem:

- a full Arb cover of Hejhal's Poisson density improves
  \(C_7<18.307\) to \(C_7<5.286\);
- the elementary sub-mean inequality replaces the source convenience bound
  \(2M/(1-r)^2\) by \(M/(\pi(1-r)^2)\).

A bounded geometry/anchor search then gives the following rational, fully
certified conditional chain:

\[
\delta=0.9999,\quad \sigma_R=1.1,\quad
R_0=\frac{3\delta}{40},\quad
a=\frac{\delta}{80},\quad r=\frac{\delta}{280},
\]

at the sixth admissible zeta-zero height, with the theorem window shifted
down by \(0.050005\).  Safe constants are

\[
\nu_s>0.01288,\qquad \omega_*>0.06737,\qquad
\boxed{c_0^{\rm new}=0.0008677256},
\]

\[
\log K_F<5259,\qquad B_0<4905.067,\qquad d_*>0.3186.
\]

For the conditional \(\alpha=1.2\), the end-to-end requirement becomes

\[
\boxed{\log q>4{,}711{,}753.120+\frac56\log C_R.}
\]

This is a factor \(543.516\) reduction in the old rounded \(\log q\) ledger,
and a factor \(47.486\) increase in the safe \(c_0\), but it is still unusable
for the certified base \(q\le12\).  Even granting \(\omega_*=1\), and
consistently recomputing the induced base while keeping the recovered
first-stage geometry, would leave \(\log q>367.352\) for \(C_R=1\).

Mechanism A0 remains structurally superior: its single propagation retains
exponent floor \(0.1552\), and under its own **CONJECTURAL diagnostic**
\(K_+<4{,}876{,}833\) gives
\(\log q>86.640+\frac56\log C_R\).  A0 still has no proved target-side RATE,
family-uniform \(K_+\), or finite-family no-pole gate, so this is not a current
\(q_0\).

## 1. Receipts before claims: source state and original chain

### 1.1 Source hashes

```text
$ shasum -a 256 research_notes/rh_goals_2026-08-14/lane_g/R3_ROUTE_B_TRANSPORT_SOL.md research_notes/rh_goals_2026-08-14/lane_g/R3_TRANSPORT_EXECUTION_SOL.md research_notes/rh_goals_2026-08-14/lane_g/LAW_R4_THETA_DEFECT.md research_notes/rh_goals_2026-08-14/lane_g/DH2_RENEWAL_PROOF_SOL.md
320c21a8d0558418531f23c1ecffd3e489c5c1ff12180ce29c8f9f90d9177468  research_notes/rh_goals_2026-08-14/lane_g/R3_ROUTE_B_TRANSPORT_SOL.md
a6b6a1297fc4401e47e194a809064baa5cade1f9effb29fe28e3bde47d3b6345  research_notes/rh_goals_2026-08-14/lane_g/R3_TRANSPORT_EXECUTION_SOL.md
5eedbfad3f3c6763a9315c051a3df49da5828a1d0d97dfb18ac7c5fcdf66ae8a  research_notes/rh_goals_2026-08-14/lane_g/LAW_R4_THETA_DEFECT.md
096d389905ad21505e2c25c30aa37b5a2fa3d3f6d054bcb30229096fc5c8d885  research_notes/rh_goals_2026-08-14/lane_g/DH2_RENEWAL_PROOF_SOL.md
```

### 1.2 Static source trace

```text
$ rg -n 'nu_seed_lower=|omega_star_lower=|c_0=|transport_base_upper=|q0 = UNDEFINED' research_notes/rh_goals_2026-08-14/lane_g/R3_ROUTE_B_TRANSPORT_SOL.md
256:nu_seed_lower= [0.0005797335141035081895947545391859565...]
257:omega_star_lower= [0.0315644606396755702327250040803298581...]
501: c_0=0.03156\cdot0.000579=1.827324\times10^{-5}.           \tag{7.3}
592:proved.  Hence **q0 = UNDEFINED**.
719:rounded_transport_base_upper= 56155

$ rg -n 'alpha=1\.2|2\.560914' research_notes/rh_goals_2026-08-14/lane_g/DH2_RENEWAL_PROOF_SOL.md
90:| conditional exponent at `sigma=1.1` | **`alpha=1.2`** |
694:At `sigma=1.1`, `alpha=1.2`. This is conditional, not a RATE theorem.
722:For the conditional `alpha=1.2`, the strict upward-rounded requirement is
726: 2.560914\times10^9+\frac56\log C_R.                  \tag{9.3}
765:| conditional epsilon exponent at `sigma=1.1` | **`alpha=1.2`** | (8.5)--(8.6) |
```

The source locations are:

- first two-constants barrier and seed floor:
  `R3_ROUTE_B_TRANSPORT_SOL.md:263-319`;
- Lemmas 7.9/7.10 and \(K_F\): lines 337-458;
- second logarithmic barrier and product: lines 460-514;
- defect and conditional threshold: lines 516-592;
- A0's one-stage chain: `R3_TRANSPORT_EXECUTION_SOL.md:38-97,139-206`;
- DH2's conditional \(\alpha=1.2\) assembly:
  `DH2_RENEWAL_PROOF_SOL.md:662-732`.

### 1.3 Fresh Arb rounding and required-\(c_0\) receipt

```text
$ /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import arb, ctx
ctx.dps=100; p=arb.pi()
nu=(p/250).sinh()/(6*p/5).sinh()*(p/1000).cos()
om=(arb(17)/(3*arb(26).sqrt())).log()/(arb(85)/3).log()
c=nu*om; cf=arb('0.000579')*arb('0.03156')
print('nu_lower=',nu.lower()); print('omega_lower=',om.lower())
print('product_lower=',c.lower()); print('floor_product=',cf)
print('relative_rounding_loss_upper=',((c-cf)/c).upper())
B=arb(56155); d=arb('0.6603'); alpha=arb('1.2')
for q in map(arb,['12','100','1000']):
    print(q,((B-d.log())/(alpha*q.log())).upper())
PY
nu_lower= 0.00057973351410350818959475453918595651347099957474008429...
omega_lower= 0.031564460639675570232725004080329858158939930648996164...
product_lower= 1.8298975687420986327319170475889146590449519196238760e-5...
floor_product= 1.8273240000000000000000000000000000000000000000000000e-5
relative_rounding_loss_upper= 0.0014064004379588010304597836459727460974382322218138008...
12.000... 18832.167889081023798755197648283267154681000184963647...
100.000... 10161.661204158263904727537450134812265031287337742000...
1000.000... 6774.4408027721759364850249667565415100208582251613335...
```

For general \(C_R\), the required multiplier at a proposed onset \(Q\) is

\[
c_{0,\rm req}(Q;C_R)=
\frac{56155-\log(0.6603)}{1.2\log Q-\log C_R},
\]

provided the denominator is positive.  The displayed values use \(C_R=1\).
They prove that optimizing \(c_0\) alone cannot reach \(12,100\), or \(1000\)
while the base remains \(56155\).

## 2. Autopsy: where the two factors and the base come from

Put \(F_q=\phi_q-\phi_\infty\), and assume the missing boundary input

\[
E_R(q)\le C_Rq^{-\alpha}\le K.
\tag{RATE}
\]

In the original rectangle, \(H=1/2\), \(L=3/5\).  The first-mode harmonic
sub-barrier gives on the seed disc

\[
\nu_s\ge
\frac{\sinh(\pi/250)}{\sinh(6\pi/5)}\cos(\pi/1000)
>0.000579.
\]

Thus

\[
E_s\le K^{1-0.000579}E_R^{0.000579}.
\]

Under the zero-free hypothesis, the explicit Hejhal chain gives

\[
L_a<8.49806,\quad C_7<18.307,\quad
K_H<e^{57983},\quad K_F<e^{57984}.
\]

In \(U=D_0\setminus\overline D_+\), the logarithmic sub-barrier gives

\[
\omega_*\ge
\frac{\log(17/(3\sqrt{26}))}{\log(85/3)}>0.03156.
\]

Therefore

\[
E_3\le K_F^{1-0.03156}
K^{0.03156(1-0.000579)}
E_R^{0.03156\cdot0.000579},
\]

which is exactly the source envelope

\[
\log E_3<56155+c_0\log C_R-\alpha c_0\log q.
\]

### 2.1 Tightness classification

| inequality | classification | evidence |
|---|---|---|
| decimal floors | **tight / negligible** | only \(0.140641\%\) product loss, Receipt 1.3 |
| first-mode barrier | convenient, but original geometry is genuinely bad | at the seed's leftmost point, harmonic measure is at most \(x/L=(1/500)/(3/5)=1/300\); hence the old \(c_0\le1/300\) even if the second stage were perfect |
| separate seed coordinate extrema | convenient | the leftmost and largest-vertical-deviation points differ |
| logarithmic annular barrier | convenient | it is \(\le0\) on most of the outer circle while the true harmonic measure is \(0\) there; no equality claim is made |
| \(C_7<18.307\) | **severely convenient** | full certified Poisson-kernel cover gives \(C_7<5.286\), Section 4 |
| Lemma-7.10 coefficient \(2M/(1-r)^2\) | **severely convenient** | direct sub-mean gives \(M/(\pi(1-r)^2)\), Section 5 |
| \(C_6<242\) | nearly tight inside the chosen Ch.6 transcription | raw upper endpoint is \(241.421356\ldots\); replacing it cannot recover orders |
| two propagation stages | **structural** | rate exponents multiply; A0 avoids the product entirely |

Fresh structural-cap receipt:

```text
$ /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import arb
B=arb(56155); d=arb('.6603'); a=arb('1.2')
cap=(arb(1)/500)/(arb(3)/5)
print('old_nu_seed_cap=',cap)
print('best_logq_if_base_unchanged=',((B-d.log())/(a*cap)).lower())
PY
old_nu_seed_cap= 0.0033333333333333333333333333333333333333333333333333...
best_logq_if_base_unchanged= 14038853.765250445402844354525431189884954636849984...
```

So even exact harmonic measures cannot rescue the original base and seed
geometry.

## 3. Admissibility and anchor relocation

For every certified nontrivial zeta zero \(\rho_n=1/2+i\gamma_n\), the theta
entry

\[
\phi_\infty(s)=
\frac{\sqrt\pi\,\Gamma(s-1/2)\zeta(2s-1)}
{\Gamma(s)\zeta(2s)(4^s-1)}
\]

has two distinct relevant points:

\[
s_{p,n}=\rho_n/2=1/4+i\gamma_n/2
\quad\text{(pole from \(\zeta(2s)\))},
\]

\[
z_n=(1+\rho_n)/2=3/4+i\gamma_n/2
\quad\text{(zero from \(\zeta(2s-1)\))}.
\]

They satisfy \(1-\overline z_n=s_{p,n}\).  This is the admissibility rule:
the height must be tied to a certified zeta-zero ordinate if the same
theta-pole/zero contradiction is to drive the R3 conclusion.  Arbitrary
large-defect heights were not admitted.  `LAW_R4_THETA_DEFECT.md:22-28,107-124,
208-239` supplies the pole analysis; `R3_TRANSPORT_EXECUTION_SOL.md:101-129`
supplies the zero analysis.

### 3.1 Wider continuous defect windows at the original height

The exact Arb evaluator from the Route-B receipt was rerun with continuous
interval cells, not sampled points:

```text
$ /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import acb, arb, ctx
ctx.dps=100
def phi(s):
    h=acb(arb('.5'))
    return acb.pi().sqrt()*(s-h).gamma()*(2*s-acb(1)).zeta()/(s.gamma()*(2*s).zeta()*(acb(4)**s-acb(1)))
t0=(acb.zeta_zero(1)/2).imag
for Rtxt,n in [('0.05',20000),('0.1',40000)]:
    R=arb(Rtxt); half=R/arb(n); best=None; bestj=None
    for j in range(n):
        c=t0-R+arb(2*j+1)*R/arb(n)
        ti=(c-half).union(c+half)
        u=abs(phi(acb(arb('.5'),ti))).upper()
        if best is None or best<u: best,bestj=u,j
    print(Rtxt,n,best,(arb(1)-best).lower(),bestj)
PY
0.05 20000 0.3416978600434958934783935546875 0.6583021399565041065216064453125 19999
0.1 40000 0.3440449447371065616607666015625 0.6559550552628934383392333984375 39999
```

Hence, with downward rounding,

\[
d_{1,0.05}>0.6583,\qquad d_{1,0.10}>0.6559.
\]

Hejhal's theorem requires \(0<\delta<1\), so its symmetric target segment has
half-width \(\delta/20<0.05\).  The \(\pm0.10\) certificate is nevertheless
useful for shifting that target segment asymmetrically while keeping it inside
a certified positive-defect window.

### 3.2 Bounded admissible-height scan

The first 2,000 certified ordinates \(t_n=\Im(\operatorname{zeta\_zero}(n))/2\)
were prescreened at the point \(1/2+it_n\).  This is a bounded scan, not a
global statement about all zeta zeros.

```text
$ /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import acb, arb, ctx
ctx.dps=70
def phi(s):
    h=acb(arb('.5'))
    return acb.pi().sqrt()*(s-h).gamma()*(2*s-acb(1)).zeta()/(s.gamma()*(2*s).zeta()*(acb(4)**s-acb(1)))
rows=[]
for n in range(1,2001):
    t=(acb.zeta_zero(n)/2).imag
    d=(arb(1)-abs(phi(acb(arb('.5'),t)))).lower()
    rows.append((float(d),n,t,d))
rows.sort(reverse=True)
print('bounded_point_defect_scan_n=1..2000')
for _,n,t,d in rows[:3]: print('n=',n,'t=',t,'defect_lower=',d)
print('anchor_probe_sigma=0.995')
for n in [1,10,124,1475]:
    t=(acb.zeta_zero(n)/2).imag
    print('n=',n,'anchor_abs_lower=',abs(phi(acb(arb('.995'),t))).lower())
PY
bounded_point_defect_scan_n=1..2000
n=1475 t=[976.7242781625678850264103627784377625525135534324130605163034320678246 +/- 3.83e-68] defect_lower=[0.6666666349433720243025011750453465010680657787055859812003653105704079 +/- 4.41e-71]
n=1046 t=[736.5100661620928555718615772093155763300039054928915938276535875126710 +/- 4.41e-68] defect_lower=[0.6666664971766983486032574322815839322445194290811868331035036644396954 +/- 1.61e-71]
n=1508 t=[994.8510013540108094632313116074800981147804578982181740411366751460184 +/- 3.61e-68] defect_lower=[0.6666663676050355962579345885730316531160247972226624920552547729015470 +/- 3.72e-71]
anchor_probe_sigma=0.995
n=1 anchor_abs_lower=[0.06320269343400962335417904043586374519338753069850034260652239089709494 +/- 2.46e-72]
n=10 anchor_abs_lower=[0.04227065122536630834991818892312242639643300835730735840521233325068427 +/- 2.69e-72]
n=124 anchor_abs_lower=[0.01893329956492580673919648514067075723234816897132690775282222082165705 +/- 2.64e-72]
n=1475 anchor_abs_lower=[0.006768266373157568713018753274325362161164728467608488948042420149594578 +/- 1.15e-73]
```

The point-scan winner was then interval-certified on whole windows.  The two
completed commands were identical except for the displayed `R,n` assignment:

```text
$ /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import acb, arb, ctx
ctx.dps=70
def phi(s):
    h=acb(arb('.5'))
    return acb.pi().sqrt()*(s-h).gamma()*(2*s-acb(1)).zeta()/(s.gamma()*(2*s).zeta()*(acb(4)**s-acb(1)))
nz=1475; t=(acb.zeta_zero(nz)/2).imag; R=arb('.05'); n=10000
half=R/arb(n); best=None; bestj=None
for j in range(n):
    center=t-R+arb(2*j+1)*R/arb(n); ti=(center-half).union(center+half)
    u=abs(phi(acb(arb('.5'),ti))).upper()
    if best is None or best<u: best,bestj=u,j
print('zero_index=',nz,'t=',t)
print('radius=0.05 cells=',n,'max_abs_upper=',best)
print('defect_lower=',(arb(1)-best).lower(),'worst_cell=',bestj)
PY
zero_index=1475 t=[976.7242781625678850264103627784377625525135534324130605163034320678246 +/- 3.83e-68]
radius=0.05 cells=10000 max_abs_upper=0.3355506248772144317626953125
defect_lower=0.6644493751227855682373046875 worst_cell=9999
```

```text
$ /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import acb, arb, ctx
ctx.dps=70
def phi(s):
    h=acb(arb('.5'))
    return acb.pi().sqrt()*(s-h).gamma()*(2*s-acb(1)).zeta()/(s.gamma()*(2*s).zeta()*(acb(4)**s-acb(1)))
nz=1475; t=(acb.zeta_zero(nz)/2).imag; R=arb('.1'); n=10000
half=R/arb(n); best=None; bestj=None
for j in range(n):
    center=t-R+arb(2*j+1)*R/arb(n); ti=(center-half).union(center+half)
    u=abs(phi(acb(arb('.5'),ti))).upper()
    if best is None or best<u: best,bestj=u,j
print('zero_index=',nz,'t=',t)
print('radius=0.1 cells=',n,'max_abs_upper=',best)
print('defect_lower=',(arb(1)-best).lower(),'worst_cell=',bestj)
PY
zero_index=1475 t=[976.7242781625678850264103627784377625525135534324130605163034320678246 +/- 3.83e-68]
radius=0.1 cells=10000 max_abs_upper=0.33803532086312770843505859375
defect_lower=0.66196467913687229156494140625 worst_cell=9999
```

Thus the largest fully certified defect among the three window candidates
actually covered here (\(n=1,6,1475\)) is at \(n=1475\):

\[
d_{1475,0.05}>0.6644,\qquad d_{1475,0.10}>0.6619.
\]

This does **not** optimize the transport chain.  The same receipt shows that
at the new Hejhal anchor \(\sigma=0.995\), the point-defect winner has only
\(m_a>0.006768\).

The \(<1\%\) defect gain at \(n=1475\) is overwhelmed by the anchor loss inside
\(C_7\log(2C_6/m_a)\).  Also, the missing \(C_R\) is height-dependent until a
uniform theorem says otherwise.  Therefore no global “best height” is claimed.

### 3.3 Joint bounded prescreen and selected sixth height

A bounded point diagnostic over the same 2,000 heights, using the recovered
geometry below, ranked \(n=6\) first.  This prescreen was not itself a proof;
the selected height was then fully interval-certified.

```text
$ /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import acb, arb, ctx
ctx.dps=60
def phi(s):
    h=acb(arb('.5'))
    return acb.pi().sqrt()*(s-h).gamma()*(2*s-acb(1)).zeta()/(s.gamma()*(2*s).zeta()*(acb(4)**s-acb(1)))
C6=arb(242); C7=arb('5.286'); K=arb(244); c=arb('.0008677256')
om=arb('.06737'); nu=arb('.01288'); r0=arb('.75'); alpha=arb('1.2')
rows=[]
for n in range(1,2001):
    t=(acb.zeta_zero(n)/2).imag
    d=(arb(1)-abs(phi(acb(arb('.5'),t)))).lower()
    m=abs(phi(acb(arb('.995'),t))).lower()
    if d<=0 or m<=0: continue
    A=C7*(2*C6/m).log()+C6.log()
    logkf=20*A/(arb.pi()*(1-r0)**2)
    base=(1-om)*logkf+om*(1-nu)*K.log()
    score=((base-d.log())/(alpha*c)).upper()
    rows.append((float(score),n,t,d,m))
rows.sort()
print('bounded_relocation_prescan_n=1..2000; point-defect diagnostic only')
for score,n,t,d,m in rows[:3]:
    print('score_upper=',arb(score),'n=',n,'t=',t,
          'point_defect_lower=',d,'anchor_m_lower=',m)
PY
bounded_relocation_prescan_n=1..2000; point-defect diagnostic only
score_upper=4731190.709794436581432819366455078125 n=6 t=[18.7930890794128356286088817403526664107027986754153966091665 +/- 2.78e-60] point_defect_lower=[0.377035685729181623354591723367834479213471062682064882009339 +/- 2.67e-61] anchor_m_lower=[0.0752081330547691321745645333663609046287139303308395459095314 +/- 1.24e-62]
score_upper=4747441.32941670529544353485107421875 n=18 t=[36.0335788372409537912610539849130841952404533107283485433417 +/- 5.38e-59] point_defect_lower=[0.0846564870168685915015383900275976932385438501701815786726946 +/- 8.88e-63] anchor_m_lower=[0.0729326635714316860227520366649563351719137671778650618929828 +/- 1.0e-64]
score_upper=4766946.551754708401858806610107421875 n=3 t=[12.5054287900728443816068954962814109093297748362789983362483 +/- 3.03e-59] point_defect_lower=[0.542147918582981779285673529176510245129197552360254191667133 +/- 4.10e-61] anchor_m_lower=[0.0697831401134110229682351298460912699674576961890258624875538 +/- 4.08e-62]
```

At \(n=6\), continuous covers give the following completed receipt.  Notice
that this fresh rerun is slightly more adverse than the earlier exploratory
number; the ledger consumes only the new floor.

```text
$ /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import acb, arb, ctx
ctx.dps=100
def phi(s):
    h=acb(arb('.5'))
    return acb.pi().sqrt()*(s-h).gamma()*(2*s-acb(1)).zeta()/(s.gamma()*(2*s).zeta()*(acb(4)**s-acb(1)))
t6=(acb.zeta_zero(6)/2).imag
print('zero_index=6 t6=',t6)
for Rtxt,n in [('0.05',20000),('0.1',40000)]:
    R=arb(Rtxt); half=R/arb(n); best=None; bestj=None
    for j in range(n):
        center=t6-R+arb(2*j+1)*R/arb(n)
        ti=(center-half).union(center+half)
        u=abs(phi(acb(arb('.5'),ti))).upper()
        if best is None or best<u: best,bestj=u,j
    print('radius=',Rtxt,'cells=',n,'max_abs_upper=',best)
    print('defect_lower=',(arb(1)-best).lower(),'worst_cell=',bestj)
PY
zero_index=6 t6=[18.79308907941283562860888174035266641070279867541539660916650055681107454480926863236516455247291190 +/- 1.89e-99]
radius=0.05 cells=20000 max_abs_upper=0.651704735122621059417724609375
defect_lower=0.348295264877378940582275390625 worst_cell=0
radius=0.1 cells=40000 max_abs_upper=0.68136764504015445709228515625
defect_lower=0.31863235495984554290771484375 worst_cell=0
```

We use \(d_*>0.3186\).  For the widest certified window, take

\[
\delta=0.9999,\qquad
t_c=t_6-0.050005.
\]

Then the Hejhal target segment is

\[
[t_c-\delta/20,t_c+\delta/20]
=[t_6-0.1,t_6-0.00001],
\]

so the full \(\pm0.10\) certificate applies.  This downward shift is the
bounded window-asymmetry optimum used here: it improves the anchor while the
entire target segment remains certified.  The pole/zero height \(t_6\) remains
inside the \(\delta\)-rectangle.

## 4. Certified recovery of \(C_7\)

Hejhal's Poisson density in the source normalization is

\[
P_h(y)=\sum_{\substack{n\ge1\\n\text{ odd}}}
\cos(n\pi y/2)\frac{\sinh(n\pi/4)}
{\sinh(n\pi(1-h)/2)},
\quad 0\le h\le0.1,\quad |y|\le0.5.
\]

The old proof retained \(n=1\) and subtracted every later term absolutely.
The following Arb cover evaluates all odd terms through 51 and subtracts a
rigorous geometric tail beginning at 53.

```text
$ /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import arb, ctx
ctx.dps=80; p=arb.pi(); Nh=80; Ny=400; nmax=51
best=None; ij=None
for i in range(Nh):
    hc=arb(2*i+1)/arb(20*Nh); hh=arb(1)/arb(20*Nh)
    hb=(hc-hh).union(hc+hh)
    for j in range(Ny):
        yc=arb(2*j+1)/arb(4*Ny); yh=arb(1)/arb(4*Ny)
        yb=(yc-yh).union(yc+yh); u=arb(0)
        for n in range(1,nmax+1,2):
            nn=arb(n)
            u += (nn*p*yb/2).cos()*(nn*p/4).sinh()/(nn*p*(1-hb)/2).sinh()
        if best is None or u.lower()<best: best,ij=u.lower(),(i,j)
n0=nmax+2
tail=((-arb(n0)*p/5).exp()/((1-(-2*p/5).exp())*(1-(-27*p/10).exp()))).upper()
cert=(best-tail).lower()
print('raw_series_min_lower=',best,'worst_cell=',ij)
print('tail_upper=',tail)
print('poisson_density_lower=',cert)
print('C7_upper=',(arb(1)/cert).upper())
PY
raw_series_min_lower=0.1892034988882979964316283668313155478164... worst_cell=(0,399)
tail_upper=4.8212256607511821769261064987592943195e-15...
poisson_density_lower=0.1892034988882931752059676156491386217099...
C7_upper=5.2853145204804362688909013277472366571819...
```

Therefore the safe replacement is

\[
\boxed{C_7<5.286.}
\]

The tail inequality is the same one used in the source for odd \(n\ge3\):

\[
\frac{\sinh(n\pi/4)}{\sinh(9n\pi/20)}
\le \frac{e^{-n\pi/5}}{1-e^{-27\pi/10}},
\]

summed over odd \(n\ge53\).  All cells cover the entire closed rectangle in
\((h,|y|)\); symmetry covers negative \(y\).

## 5. Contour and Cauchy-radius optimization

Let the large disc available from the area estimate have radius \(\delta/10\).
If

\[
\iint_{|w|<1}\log^+|\phi_q(w)|\,dA(w)\le20A,
\qquad A=C_7L_a+\log C_6,
\]

then for every \(|w|\le r_0\), subharmonicity on the disc
\(D(w,1-r_0)\subset D(0,1)\) gives directly

\[
\log^+|\phi_q(w)|
\le\frac{20A}{\pi(1-r_0)^2}.
\tag{5.1}
\]

This replaces, rather than contradicts, the source's convenient
\(2M/(1-r)^2\) lemma.  It improves that coefficient by exactly \(2\pi\) at a
fixed radius.

### 5.1 Geometry search and rational candidate

For fixed \(\delta,L\), write

\[
w=\delta/20,\quad R_0=\kappa\delta,\quad
D_+=D(z_c+a\delta,r\delta).
\]

The certified barriers are

\[
\nu_s\ge
\frac{\sinh(\pi(a-r)/2)}{\sinh(\pi L/(2\delta))}
\cos(\pi r/2),
\]

\[
\omega_*\ge
\frac{\log((\kappa-a)/\sqrt{a^2+(1/20)^2})}
{\log((\kappa-a)/r)}.
\]

A bounded floating grid minimized the complete quotient
\((B_0-\log d_*)/(\nu_s\omega_*)\), not \(c_0\) alone.  It was a selector,
not evidence:

```text
improved_float_grid: C7=5.286, submean logKF=20*A/[pi(1-r)^2]
ratio=5844492.83 c=0.000884724985 base=5170.34708 delta=0.990 kappa=0.07540 a=0.0126731 r=0.0036209
ratio=5849129.08 c=0.000857087994 base=5012.79657 delta=0.990 kappa=0.07500 a=0.0125000 r=0.0035714
```

The horizontal extent was not silently varied.  The requested
\(\alpha=1.2\) comes from the boundary line \(\sigma_R=1.1\), so
\(L=\sigma_R-1/2=0.6\) is fixed.  Moving the RATE side left would change the
unproved RATE theorem and its exponent; moving it right only decreases the
right-side harmonic measure.  With \(L\) fixed, increasing \(\delta\) improves
the aspect ratio, so the rational choice \(0.9999\) sits just below Hejhal's
strict theorem limit \(\delta<1\).  The separate vertical shift in Section 3.3
uses the asymmetric portion of the certified \(\pm0.10\) window.

The simple rational near the grid minimum was chosen and then certified:

\[
\kappa=\frac3{40},\qquad a=\frac1{80},\qquad r=\frac1{280},
\qquad r_0=10\kappa=\frac34.
\]

Exact inclusions are

\[
a-r=\frac1{112}>0,\qquad a+r=\frac9{560}<\frac3{40},
\qquad \frac1{20}<\frac3{40}<\frac1{10}.
\]

The first barrier becomes

\[
\nu_s\ge
\frac{\sinh(\pi/224)}{\sinh(\pi L/(2\delta))}
\cos(\pi/560),
\]

and the logarithmic barrier becomes

\[
\omega_*\ge
\frac{\log(5/\sqrt{17})}{\log(35/2)}.
\]

For \(\delta=0.9999,L=0.6\), fresh Arb gives

```text
$ /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import arb, ctx
ctx.dps=100
pi=arb.pi(); delta=arb('0.9999'); L=arb('0.6')
nu=(pi/arb(224)).sinh()/(pi*L/(2*delta)).sinh()*(pi/arb(560)).cos()
omega=(arb(5)/arb(17).sqrt()).log()/(arb(35)/2).log()
c=nu*omega
nu_anchor=(pi/4).sinh()/(pi*L/(2*delta)).sinh()
print('delta=',delta,'L=',L)
print('nu_exact_lower=',nu.lower())
print('omega_exact_lower=',omega.lower())
print('c_exact_lower=',c.lower())
print('nu_anchor_exact_lower=',nu_anchor.lower())
print('safe_c0=',arb('0.01288')*arb('0.06737'))
PY
delta=[0.9999 +/- 6.78e-102] L=[0.6 +/- 5.73e-102]
nu_exact_lower=[0.01288518982092481439263909350141129766919225321362917197572800897482052728907305380741631947516471369 +/- 2.55e-102]
omega_exact_lower=[0.06737166552173392606875953051009198169539025218139305075931946044329988555877187569473776031496052251 +/- 4.82e-103]
c_exact_lower=[0.0008680966987993972588603794397938651406084129311658291578928775501602407006938417655430384117870527176 +/- 2.72e-104]
nu_anchor_exact_lower=[0.7980624312950549692053103163762770615877257008312723712313236224017949068615247912658863233754713042 +/- 1.06e-101]
safe_c0=[0.0008677256 +/- 1.01e-104]
```

We consume the lower floors

\[
\nu_s=0.01288,\qquad \omega_*=0.06737,\qquad
\nu_a=0.798,\qquad
c_0^{\rm new}=0.01288\cdot0.06737=0.0008677256.
\]

The elementary cap \(\nu\le x/L\) at the seed's leftmost point gives
\(\nu_s\le0.0148795\); the certified \(0.01288\) floor already captures
\(86.56\%\) of that structural cap.  The first propagation is no longer the
main convenience loss.

### 5.2 Fresh theta rectangle/disc cover at the selected height

The final cover uses
\(t_c=t_6-0.050005\), \(\delta=0.9999\), rectangle
\([0.5,1.1]\times[t_c-\delta,t_c+\delta]\), and
\(D_0=D(0.5+it_c,3\delta/40)\).

```text
$ /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import acb, arb, ctx
ctx.dps=80
def box(c,h): return (c-h).union(c+h)
def phi_with_den(s):
    half=acb(arb('0.5'))
    den=s.gamma()*(2*s).zeta()*(acb(4)**s-acb(1))
    if acb(0) in den: raise ArithmeticError('denominator ball contains zero')
    num=acb.pi().sqrt()*(s-half).gamma()*(2*s-acb(1)).zeta()
    return num/den, abs(den).lower()
delta=arb('0.9999'); offset=arb('-0.050005')
t6=(acb.zeta_zero(6)/2).imag; tc=t6+offset
print('delta=',delta,'offset=',offset,'target_halfwidth=',delta/20)
print('target_window_relative_to_zero=',offset-delta/20,offset+delta/20)
anchor,aden=phi_with_den(acb(arb('0.5')+delta/2,tc))
print('anchor_abs_lower=',abs(anchor).lower(),'anchor_den_abs_lower=',aden)
def edge(kind,n):
    if kind in ('left','right'):
        lo,hi=tc-delta,tc+delta
        fixed=arb('0.5') if kind=='left' else arb('1.1')
    else:
        lo,hi=arb('0.5'),arb('1.1')
        fixed=tc+delta if kind=='top' else tc-delta
    step=(hi-lo)/arb(n); half=step/2; best=None; mind=None; cell=None
    for j in range(n):
        v=lo+(arb(j)+arb('0.5'))*step
        s=acb(fixed,box(v,half)) if kind in ('left','right') else acb(box(v,half),fixed)
        val,dlow=phi_with_den(s); u=abs(val).upper()
        if best is None or best<u: best,cell=u,j
        if mind is None or dlow<mind: mind=dlow
    print(kind,'cells=',n,'max_abs_upper=',best,'worst_cell=',cell,
          'min_den_abs_lower=',mind)
for kind,n in [('left',4000),('right',4000),('top',1200),('bottom',1200)]:
    edge(kind,n)
R=3*delta/40; n=120; step=2*R/arb(n); half=step/2
best=None; mind=None; cell=None
for i in range(n):
    xb=box(arb('0.5')-R+(arb(i)+arb('0.5'))*step,half)
    for j in range(n):
        yb=box(tc-R+(arb(j)+arb('0.5'))*step,half)
        val,dlow=phi_with_den(acb(xb,yb)); u=abs(val).upper()
        if best is None or best<u: best,cell=u,(i,j)
        if mind is None or dlow<mind: mind=dlow
print('D0_square_n=',n,'R=',R,'K_infty_D0_upper=',best,
      'worst_cell=',cell,'min_den_abs_lower=',mind)
print('denominator_clearance=PASS')
PY
delta=[0.9999 +/- 9.06e-82] offset=[-0.050005 +/- 7.57e-84] target_halfwidth=[0.049995 +/- 1.64e-82]
target_window_relative_to_zero=[-0.1 +/- 1.72e-82] [-0.00001 +/- 1.64e-82]
anchor_abs_lower=[0.078438861488754402087978638139622329324856816014878007093077182532422389958649942 +/- 1.41e-83] anchor_den_abs_lower=[6.0865728563170330006982611960606027417343362927750319556958301192677061596118621e-12 +/- 4.06e-92]
left cells=4000 max_abs_upper=1.047275929711759090423583984375 worst_cell=734 min_den_abs_lower=2.840612902166891710897811407221524859778583049774169921875e-13
right cells=4000 max_abs_upper=0.16018755105324089527130126953125 worst_cell=177 min_den_abs_lower=2.59637336248188209386622560259638703428208827972412109375e-12
top cells=1200 max_abs_upper=0.3948258752934634685516357421875 worst_cell=0 min_den_abs_lower=2.841595189335163577915022159459113026969134807586669921875e-13
bottom cells=1200 max_abs_upper=0.8348431997001171112060546875 worst_cell=0 min_den_abs_lower=4.97813192035755081032988300648867152631282806396484375e-12
D0_square_n=120 R=[0.0749925 +/- 2.79e-82] K_infty_D0_upper=1.867345972917973995208740234375 worst_cell=(0,69) min_den_abs_lower=2.02962418202148908198678700642858530045486986637115478515625e-13
denominator_clearance=PASS
```

Thus safe upper ledgers are

\[
K=242+1.048<244,\qquad K_{\infty,0}<2,\qquad m_a>0.07843.
\]

Every division box in the cover succeeded with a printed positive lower bound
for the denominator modulus.  The reflected half-width is
\(\delta/10=0.09999<1/4\), so all target
domains stay strictly right of the theta pole at real part \(1/4\).

## 6. End-to-end conditional recomputation

Use

\[
C_6=242, C_7=5.286, m_a=0.07843, K=244,
\ K_{\infty,0}=2, r_0=3/4.
\]

Then

\[
L_a=\log(2C_6/m_a),\qquad A=C_7L_a+\log C_6,
\]

\[
\log K_H\le\frac{20A}{\pi(1-r_0)^2},\qquad
K_F=K_H+K_{\infty,0}.
\]

Fresh adverse-rounding receipt:

```text
$ /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import arb, ctx
ctx.dps=80; p=arb.pi()
nu=arb('.01288'); om=arb('.06737'); c=nu*om
C7=arb('5.286'); C6=arb(242); K=arb(244); m=arb('.07843')
La=(2*C6/m).log(); A=C7*La+C6.log()
logKH=20*A/(p*(1-arb(3)/4)**2)
logKF_actual=(logKH.exp()+arb(2)).log()
logKF=arb(logKF_actual.upper().ceil())
base=(1-om)*logKF+om*(1-nu)*K.log()
d=arb('.3186'); alpha=arb('1.2')
T=(base-d.log())/(alpha*c)
print('safe_c0=',c)
print('L_anchor_upper=',La.upper())
print('A_upper=',A.upper())
print('log_KH_upper=',logKH.upper())
print('log_KF_integer_upper=',logKF)
print('transport_base_upper=',base.upper())
print('conditional_log_qC_CR1_upper=',T.upper())
PY
safe_c0=0.0008677256000000000000000000000000000000...
L_anchor_upper=8.7276336784741936462504479379507501451...
A_upper=51.623209350571274011620987077396100435...
log_KH_upper=5258.2969257031489852768298786661322962...
log_KF_integer_upper=5259
transport_base_upper=4905.066744189741409531052786884796592...
conditional_log_qC_CR1_upper=4711753.119372498631703487959881930223...
```

Therefore

\[
\boxed{
\log E_3(q)<4905.067+c_0^{\rm new}\log C_R
-1.2c_0^{\rm new}\log q,
\qquad c_0^{\rm new}=0.0008677256.
}
\]

The strict defect test \(E_3<0.3186\) is ensured by

\[
\boxed{
\log q>4{,}711{,}753.120+\frac56\log C_R.
}
\tag{6.1}
\]

The remaining scale arithmetic is one fresh receipt.  The activation condition
uses the source's strict \(E_a<m_a/2\), so the factor \(2\) is retained.

```text
$ /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import arb, ctx
ctx.dps=80
alpha=arb('1.2'); d=arb('.3186'); base=arb('4905.067')
nu_a=arb('.798'); m=arb('.07843'); K=arb(244)
qA=((1-nu_a)*K.log()-(m/2).log())/(alpha*nu_a)
print('conditional_log_qA_CR1_upper=',qA.upper())
for q in map(arb,['12','100','1000']):
    c_req=(base-d.log())/(alpha*q.log())
    print('recovered_chain_c0_required_for_q=',q,'upper=',c_req.upper())
nu_cap=(arb('0.9999')/arb(112))/arb('.6')
best=((1-nu_cap)*K.log()-d.log())/(alpha*nu_cap)
print('recovered_geometry_nu_seed_upper_cap=',nu_cap)
print('best_possible_logq_if_omega=1_CR1_upper=',best.upper())
new_c=arb('.0008677256'); old_c=arb('.00001827324')
new_T=arb('4711753.120'); old_T=arb('2560914000')
print('new_c0_over_old_c0_lower=',(new_c/old_c).lower())
print('old_rounded_logq_over_new_upper_threshold_lower=',(old_T/new_T).lower())
PY
conditional_log_qA_CR1_upper=4.541691660220064772307509436636792492...
recovered_chain_c0_required_for_q=12 upper=1645.337065713675577410686012151635882...
recovered_chain_c0_required_for_q=100 upper=887.8084523726135915849502058060376492...
recovered_chain_c0_required_for_q=1000 upper=591.8723015817423943899668038706917662...
recovered_geometry_nu_seed_upper_cap=0.01487946428571428571428571428571428571...
best_possible_logq_if_omega=1_CR1_upper=367.3514977068110037327802194326063267...
new_c0_over_old_c0_lower=47.48613819990324649596896883092434620...
old_rounded_logq_over_new_upper_threshold_lower=543.5161679268968150012070241914542416...
```

Thus \(q_A\) needs only
\(\log q>4.541692+(5/6)\log C_R\), and \(q_C\), not \(q_A\), controls this
conditional transport ledger.  At \(q=12,100,1000\), the recovered fixed-base
chain would still need the impossible products printed above.

Even replacing the second-stage harmonic measure by the impossible ideal
\(\omega_*=1\) changes the base consistently to
\((1-\nu_{s,\max})\log K\).  Retaining the recovered seed cap then still gives
\(\log q>367.352\) for \(C_R=1\), far beyond \(q=12,100,1000\).

The remaining orders cannot be recovered inside the two-stage sup-norm
architecture.  The intermediate \(K_F\) stage must be eliminated or replaced
by a qualitatively sharper norm/propagation argument.

The complete conditional onset remains

\[
q_0=\max(12,q_{\rm RATE},q_A,q_C,q_{\rm divisor},q_{\rm monotone}),
\]

so, because those non-transport gates and \(C_R\) are missing,

\[
\boxed{q_0=\texttt{UNDEFINED}.}
\]

Equation (6.1) is the honest conditional \(q_C\) chain, not a proved current
onset.

## 7. Comparison with mechanism A0

A0 uses a single rectangle and a Rouché circle around
\(z_1=(1+\rho_1)/2\).  Its certified constants are

\[
m_z\ge0.0439,\qquad \nu_z\ge0.1552,
\]

and its conditional inequality is

\[
K_+^{1-0.1552}(C_Rq^{-\alpha})^{0.1552}<0.0439.
\]

Fresh comparison arithmetic:

```text
$ /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import arb
a=arb('1.2'); nu=arb('.1552'); m=arb('.0439')
for K in map(arb,['4876833','244']):
    T=((1-nu)*K.log()-m.log())/(a*nu)
    print(K,T.upper())
print('A0/original_c0=',(nu/arb('0.00001827324')).lower())
print('A0/recovered_c0=',(nu/arb('0.0008677256')).lower())
PY
Kplus=4876833 A0_logq_CR1_upper=86.63963986042833202325362246600309947...
Kplus=244     A0_logq_CR1_upper=41.71954830127098541567484211761381871...
A0/original_c0=8493.294019013595837410333361790246...
A0/recovered_c0=178.858385646337966748935377727706...
```

The \(K_+=244\) row is a counterfactual sensitivity check, **not** a proved A0
input.  A0's actual note explicitly labels family-uniform \(K_+\), target-side
RATE, and finite-family holomorphy as **OPEN**.  With its diagnostic
\(K_+=4{,}876{,}833\), the conditional result is

\[
\log q>86.640+\frac56\log C_R.
\]

A0's decimal margins are tight: its raw Arb values are
\(m_z>0.0439088447601\ldots\) and
\(\nu_z>0.1552144375083\ldots\), so the floors \(0.0439,0.1552\) lose no
orders.  The lossy part is the non-RATE boundary bound, not the contour
certificate.  Most importantly, A0 avoids \(C_7\), Lemma 7.10, the annular
second propagation, and the critical-line defect entirely.

| A0 component | verdict |
|---|---|
| \(m_z:0.0439088\ldots\to0.0439\) | tight decimal floor |
| \(\nu_z:0.1552144\ldots\to0.1552\) | tight decimal floor |
| circle radius \(r_z=1/8\) | convenient geometry choice; the joint margin/harmonic-measure tradeoff was not globally optimized |
| full Fourier harmonic-measure cover | certified on the entire circle; no one-mode loss |
| \(K_+<4{,}876{,}833\) | dominant crude supremum and itself only a **CONJECTURAL diagnostic** family input |
| one two-constants step | structural advantage; no multiplicative second exponent and no Cauchy-disc stage |

**Architecture verdict:** pursue A0 first if its family-uniform gates can be
proved.  Route B is now substantially better quantified and is a valid
conditional fallback, but its two-stage \(K_F\) architecture cannot meet the
finite base even under ideal harmonic measure.

## 8. Claim ledger

| item | verdict |
|---|---|
| original factor trace and rounding loss | **PROVED / fresh Arb arithmetic** |
| continuous \(\pm0.05,\pm0.10\) defects at \(n=1,6,1475\) | **Arb-certified interval covers** |
| “largest” height | **bounded only**: \(n=1475\) wins the point prescan and the three fully covered candidates; no global claim |
| admissibility of selected height | **certified theta zeta-zero height**; pole/zero locations exact |
| improved \(C_7<5.286\) | **Arb-certified Poisson-density cover + rigorous tail** |
| sub-mean replacement | **elementary proved inequality** |
| rational optimized geometry and theta-domain bounds | **Arb-certified** |
| \(c_0^{\rm new}=0.0008677256\), base \(<4905.067\) | **proved conditional transport constants** |
| \(\log q>4{,}711{,}753.120+(5/6)\log C_R\) | **CONDITIONAL** on full-side RATE and all stated R3 gates |
| bounded search is globally optimal | **UNPROVED / not claimed** |
| full `(RATE)`, \(C_R,q_{\rm RATE}\) at the selected height/window | **OPEN** |
| finite-family divisor/holomorphy and monotonicity thresholds | **OPEN** |
| unconditional effective \(q_0\) | **`UNDEFINED`** |
