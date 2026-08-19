# RATE-A constant reduction from the direct atom moment

**Date:** 2026-08-19
**Program:** `(RATE)`, lane G
**Interpreter:** `/Users/za/.venvs/farey-rh/bin/python` with `flint.arb`
**Write scope:** this file only

## 0. Verdict and status boundary

The published RATE-A theorem is left unchanged.  In particular, its
advertised

\[
C_R^{\rm pub}=10489412368759562746433608215977724802
\]

and its declared atom coefficient (C_4=2^{100}) remain valid and are not
rewritten here (`BOUNDARY_ALPHA_THEOREM_SOL.md:24-55,510-582`).

The strongest robust immediate substitution supplied by the now confirmed
atom-moment bridge is

\[
 C_4' = 2^{62}+1=4611686018427387905.
\]

Keeping the already published safe component ceilings

\[
 S=7.648,
 \qquad M_0=2.775,
\]

gives the outward Arb ceiling

\[
 \boxed{C_R'=38160259896392973127946053}.
\]

The simpler safe fallback (C_4=2^{63}) gives

\[
 \boxed{C_R^{63}=76320519792785946239303038}.
\]

These are **unbanked candidate theorem constants** pending a separate cold
`CR_REDUCTION_REFEREE.md` and an orchestrator Arb replay.  The arithmetic and
the coefficient substitution are proved in this note from the cited
paper-level inputs; no theorem-ledger promotion is made here.  Machine
formalization and a certified full-operator enclosure remain open, as stated
by `RATE_A_REFEREE.md:305-307,369-392` and
`AM_REFEREE.md:360-408`.

The selected A0 transport formula is also recomputed below.  Its threshold is
an analytic transport cutoff only; it is not a claim that all other program
gates or the finite base block have closed.

## 1. Immutable source receipt

The following command hashed every source used for the dependency chain,
including the independent wrap proof, the A0 threshold corrections, and the
autopsy precedent.  These hashes are the versions read for this note.

Command:

```bash
shasum -a 256 \
 research_notes/rh_goals_2026-08-14/lane_g/BOUNDARY_ALPHA_THEOREM_SOL.md \
 research_notes/rh_goals_2026-08-14/lane_g/ATOM_MOMENT_BRIDGE_SOL.md \
 research_notes/rh_goals_2026-08-14/lane_g/AM_REFEREE.md \
 research_notes/rh_goals_2026-08-14/lane_g/RATE_A_REFEREE.md \
 research_notes/rh_goals_2026-08-14/lane_g/TWOMARK_RENEWAL_SOL.md \
 research_notes/rh_goals_2026-08-14/lane_g/TWOMARK_REFEREE.md \
 research_notes/rh_goals_2026-08-14/lane_g/FW_RENEWAL_COUNT_SOL.md \
 research_notes/rh_goals_2026-08-14/lane_g/FW_REFEREE.md \
 research_notes/rh_goals_2026-08-14/lane_g/DH2_RENEWAL_PROOF_SOL.md \
 research_notes/rh_goals_2026-08-14/lane_g/M3_UNIFORMITY_EXECUTION_SOL.md \
 research_notes/rh_goals_2026-08-14/lane_g/KF_WALL_ATTACK_SOL.md \
 research_notes/rh_goals_2026-08-14/lane_g/KF_WALL_REFEREE.md \
 research_notes/rh_goals_2026-08-14/lane_g/C0_TRANSPORT_CAMPAIGN_SOL.md
```

Output:

```text
58441b334a5f279aae6298e3b5383ef5677b3e6ec6e7d5bc6a908a4936111e6e  research_notes/rh_goals_2026-08-14/lane_g/BOUNDARY_ALPHA_THEOREM_SOL.md
59ce32f7c6fa86580055d9049e609a2189ecc1645528dd4136758fcf547fbbbb  research_notes/rh_goals_2026-08-14/lane_g/ATOM_MOMENT_BRIDGE_SOL.md
3d655f2c05395688be73e8786cd9a954182cc4842005ff9e7662d05cccf503b4  research_notes/rh_goals_2026-08-14/lane_g/AM_REFEREE.md
b835804104f502f54cc757336ba8fe54a82a05eaa18261a4d78f697aba358590  research_notes/rh_goals_2026-08-14/lane_g/RATE_A_REFEREE.md
7a553a9c3ed289b513ad8dd7e3a118b0c0d50f92080a1f89a6749fbce44a692b  research_notes/rh_goals_2026-08-14/lane_g/TWOMARK_RENEWAL_SOL.md
07ae98864b6963b14a279cfc463c9d047d0c5e75bc4f8fac876781f34bd28263  research_notes/rh_goals_2026-08-14/lane_g/TWOMARK_REFEREE.md
70cf0a9d12cdc6938c431bd1246b0ca18d929c151fb98399a8e94a75d7f6fd3c  research_notes/rh_goals_2026-08-14/lane_g/FW_RENEWAL_COUNT_SOL.md
39c2e0d10a2ef1bb880e34cd4ca53bc280b451305cac871eb2244bb52e490058  research_notes/rh_goals_2026-08-14/lane_g/FW_REFEREE.md
096d389905ad21505e2c25c30aa37b5a2fa3d3f6d054bcb30229096fc5c8d885  research_notes/rh_goals_2026-08-14/lane_g/DH2_RENEWAL_PROOF_SOL.md
3fb8f625264d2096ee2a27a252916ec4e4c33801adf8fd638b1f5c2ef47ca208  research_notes/rh_goals_2026-08-14/lane_g/M3_UNIFORMITY_EXECUTION_SOL.md
efa518c9908e3c68005c3b7349bdee6c4af63dc7146ef85b13882560c2644aad  research_notes/rh_goals_2026-08-14/lane_g/KF_WALL_ATTACK_SOL.md
73c6eb59b25038f9e23ae38fa8c409af65d50fd0219b45417022663486361710  research_notes/rh_goals_2026-08-14/lane_g/KF_WALL_REFEREE.md
91e26f6cd1928a35a6420e319fd2fc7a9ad3911bc6dd5be372ff7bd09a15fd21  research_notes/rh_goals_2026-08-14/lane_g/C0_TRANSPORT_CAMPAIGN_SOL.md
```

## 2. Complete constant dependency chain

### 2.1 Boundary and layer-cake inputs

The boundary proof sets (p=11/5) and uses the exponent

\[
 \alpha=p-1=6/5.
\]

The source equations are `BOUNDARY_ALPHA_THEOREM_SOL.md:510-522` and
`:529-540`.  At this (p), the exact values are

\[
 J_2=305,
 \qquad J_4=91605,
 \qquad
 F(q):=\left({1\over3-p}+J_2\right)+{J_4\over q}
       ={1225\over4}+{91605\over q}.
\]

For (q\ge12), the source proves (F(q)\le F(12)=7940).  This is an exact
integer/rational absorption, not a fitted decimal
(`BOUNDARY_ALPHA_THEOREM_SOL.md:529-546`; `RATE_A_REFEREE.md:154-219`).

The paired term in the boundary estimate is

\[
 E_{\rm pair,all}(q,s)
 \le 2\pi^2(|s|+1)pC_4
 \left[\left({1\over3-p}+J_2\right)q^{1-p}+J_4q^{-p}\right]
\tag{2.1}
\]

(`BOUNDARY_ALPHA_THEOREM_SOL.md:510-525`).  The proof's safe closed-contour
component is

\[
 \sup_{s\in\Gamma_R^A}|s|<S=7.648
\]

(`BOUNDARY_ALPHA_THEOREM_SOL.md:542-546`, with its Arb receipt at
`:140-200`).  Therefore the (q^{-6/5}) pair coefficient after (q\ge12)
absorption is

\[
 C_{\rm pair}(C_4)
 =2\pi^2(S+1)pC_4F(12).
\tag{2.2}
\]

### 2.2 Independent wrap term

The referee-confirmed overflow estimate is

\[
 E_{\rm wrap}(q,s)\le pC_1G(p)q^{1-p},
 \qquad C_1=128(1+\log2),
 \qquad G(p)={1\over p-2}+{1\over(p-2)^2}.
\tag{2.3}
\]

This is `FW_RENEWAL_COUNT_SOL.md:475-498` and is consumed in
`BOUNDARY_ALPHA_THEOREM_SOL.md:234-243,556-560`.  Since (p-2=1/5),

\[
 G(11/5)=5+25=30,
 \qquad
 C_{\rm wrap}=p\,128(1+\log2)\,30.
\tag{2.4}
\]

It is independent of (C_4).  This independence is load-bearing: the
constant reduction changes only the paired term.

### 2.3 Boundary prefactor and outward ceiling

The beta-integral estimate supplies the uniform prefactor

\[
 |M(s)|\le M_0=2.775
\]

on the contour (`BOUNDARY_ALPHA_THEOREM_SOL.md:562-567`; the uniform
component proof is `M3_UNIFORMITY_EXECUTION_SOL.md:255-280`).  Consequently the
complete safe coefficient for any valid atom coefficient (C_4^\star) is

\[
 C_R(C_4^\star)
 =\left\lceil
 M_0\left(C_{\rm pair}(C_4^\star)+C_{\rm wrap}\right)
 \right\rceil_{\rm outward}.
\tag{2.5}
\]

The ceiling is applied to the upper endpoint of the Arb expression, not to a
decimal midpoint.  The original source uses exactly this positive assembly at
`BOUNDARY_ALPHA_THEOREM_SOL.md:548-582`.

## 3. Why the direct coefficient may be substituted

The confirmed bridge defines the full canonical atom cost and proves the
finite-(x) moment directly, rather than inferring it from the displayed
(k_X^2) theorem (`ATOM_MOMENT_BRIDGE_SOL.md:78-154`; `AM_REFEREE.md:45-84,
233-253`).  Its direct marked (A_X^2) subtotal is below (2^{62}), and the
Ford unit term contributes one coefficient.  The final source lines are:

```text
ATOM_MOMENT_BRIDGE_SOL.md:483-489
Finally, Ford gives
 # {X in C_q : x_X <= Y} <= Y^2.
The regime factor is at least 1 in both cases.  Adding (3.28) to (3.27) gives
a coefficient 2^62+1<2^63.  This proves (AM).
```

The scalar receipt for the integer budget is recorded in
`ATOM_MOMENT_BRIDGE_SOL.md:35-76` and independently checked by
`AM_REFEREE.md:184-231`:

```text
base_exp= 47 low_with_order_exp= 12 high_with_order_exp= 15
direct_A2_ceiling=2^62 4611686018427387904
direct_1_plus_A2_ceiling=2^63 9223372036854775808
```

The exact strict coefficient used by this reduction is therefore

\[
 C_4'=2^{62}+1=4611686018427387905,
\]

while (2^{63}=9223372036854775808) is a simpler, weaker fallback.  The
primary is the direct (2^{62}) subtotal ceiling plus the Ford unit term; the
fallback is a larger valid power-of-two ceiling.  Both are smaller than the
published (2^{100}).  No claim here replaces the
published ledger.

The substitution is valid without changing a hypothesis.  The boundary proof
uses (C_4) only as a positive scalar in the atom-moment layer cake
(`BOUNDARY_ALPHA_THEOREM_SOL.md:403-455`) and then linearly in the paired
majorant (2.1).  The shallow/deep split, (p), (J_2), (J_4), (F(12)),
the wrap estimate, and (M_0) are independent of that scalar
(`BOUNDARY_ALPHA_THEOREM_SOL.md:457-525,556-582`).  Replacing (C_4) by any
valid upper coefficient (C_4^\star) therefore preserves the proof and
strictly decreases only the paired contribution.  This is the exact
downstream-hypothesis invariance needed for the primary candidate.

No optimization of (S), (M_0), (C_1), or the wrap proof is folded into
the candidate.  The source's (S=7.648) and (M_0=2.775) are retained.

## 4. Binding Arb replay: current, primary, and fallback

The following is the complete runnable arithmetic receipt.  All inputs are
exact rationals or Arb balls; all products are positive; the integer ceiling
is computed from `raw.upper().ceil()`.  It also recomputes the selected A0
threshold with

\[
 T(C_R)=
 { (1-\nu)\log K_+-\log m \over \alpha\nu}
 +{\log C_R\over\alpha},
\quad K_+=117,\ \nu=.1552,\ m=.0439,
\tag{4.1}
\]

which is the unrounded strict formula at
`BOUNDARY_ALPHA_THEOREM_SOL.md:600-655` and the corrected A0 source chain
`KF_WALL_ATTACK_SOL.md:596-661`, `KF_WALL_REFEREE.md:326-371`.

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import arb, ctx
ctx.dps=100

def Z(a):
    s=str(a)
    assert '+/-' not in s and 'e' not in s.lower(), s
    u,v=s.split('.',1)
    assert set(v)<=set('0'), s
    return int(u)
def ceil_upper(a): return Z(a.upper().ceil())
p=arb(11)/5; alpha=arb(6)/5; nu=arb('.1552'); m=arb('.0439'); K=arb(117)
S=arb('7.648'); M=arb('2.775'); F=arb(1225)/4+arb(91605)/12
pair_pref=2*arb.pi()**2*(S+1)*p; wrap=p*128*(1+arb(2).log())*30
print('p=',p)
print('alpha=',alpha)
print('J2=305 J4=91605')
print('F_12=',F)
print('pair_prefactor_upper=',pair_pref.upper())
print('wrap_constant_upper=',wrap.upper())
print('S=',S,'M0=',M)
T0=((1-nu)*K.log()-m.log())/(alpha*nu)
rows=[]
for name,C4 in [('original_2^100',arb(2)**100),('primary_2^62_plus_1',arb(2)**62+1),('fallback_2^63',arb(2)**63)]:
    pair=pair_pref*C4*F
    raw=M*(pair+wrap)
    CR=ceil_upper(raw)
    T=T0+arb(CR).log()/alpha
    eT=T.exp(); lo=Z(eT.lower().floor()); hi=Z(eT.upper().floor()); qt=hi+1
    ER=arb(CR)*arb(qt)**(-alpha); lhs=K**(1-nu)*ER**nu
    rows.append((name,CR,T,qt))
    print(name)
    print('C4=',C4)
    print('C_pair_upper=',pair.upper())
    print('C_wrap_upper=',wrap.upper())
    print('C_R_raw_upper=',raw.upper())
    print('C_R=',CR,'strict_upper=',bool(arb(CR)>raw))
    print('T=',T)
    print('floor_exp_T_lower=',lo)
    print('floor_exp_T_upper=',hi)
    print('q_transport=',qt)
    print('minimality=',bool(arb(qt).log()>T),bool(arb(qt-1).log()<=T))
    print('ER_upper=',ER.upper())
    print('A0_lhs_upper=',lhs.upper())
    print('A0_strict_pass=',bool(lhs<m))
current=rows[0]
for item in rows[1:]:
    print('delta_T_current_minus_'+item[0]+'=',current[2]-item[2])
print('primary_vs_fallback_delta_T=',rows[1][2]-rows[2][2])
PY
```

Output:

```text
p= [2.200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 +/- 5.15e-101]
alpha= [1.200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 +/- 2.29e-101]
J2=305 J4=91605
F_12= 7940.000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
pair_prefactor_upper= [375.5502909867314026769949839344874020800486388848007722837796397844241695468376625425090801395753747 +/- 7.62e-99]
wrap_constant_upper= [14303.70738137041797395677696207867564710182513507543638681150472020018931839998095743833338646574507 +/- 2.71e-96]
S= [7.648000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 +/- 4.40e-101] M0= [2.775000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 +/- 2.29e-101]
original_2^100
C4= 1267650600228229401496703205376.000000000000000000000000000000000000000000000000000000000000000000000
C_pair_upper= [3779968421174617205922020978730697336.347416215578520998911077394147406044521368423027997416058370417 +/- 1.47e-64]
C_wrap_upper= [14303.70738137041797395677696207867564710182513507543638681150472020018931839998095743833338646574507 +/- 2.71e-96]
C_R_raw_upper= [10489412368759562746433608215977724801.15206330114027350203430953708397248111154720823866623148757646 +/- 3.36e-63]
C_R= 10489412368759562746433608215977724802 strict_upper= True
T= [109.4217450401595237437865635712045414186102217601228097406493836774145566367016216432950581262472325 +/- 1.33e-98]
floor_exp_T_lower= 332093267419812025416641789732742045430624465594
floor_exp_T_upper= 332093267419812025416641789732742045430624465594
q_transport= 332093267419812025416641789732742045430624465595
minimality= True True
ER_upper= [9.890974306379110548771776148234686409687942813445791857560132757329459844647921275246108374689796773e-21 +/- 4.85e-122]
A0_lhs_upper= [0.04389999999999999999999999999999999999999999999999069717268235475241243172461311296258592995932825707 +/- 3.48e-102]
A0_strict_pass= True
primary_2^62_plus_1
C4= 4611686018427387905.000000000000000000000000000000000000000000000000000000000000000000000000000000000
C_pair_upper= [13751445007709179505551841.33395786111690885080266708062676261314928147785351968679482160887568567771 +/- 4.75e-75]
C_wrap_upper= [14303.70738137041797395677696207867564710182513507543638681150472020018931839998095743833338646574507 +/- 2.71e-96]
C_R_raw_upper= [38160259896392973127946052.48971636750929979103347091706418695905400593537949053278122852015538631561 +/- 3.92e-75]
C_R= 38160259896392973127946053 strict_upper= True
T= [87.47208432242792227908911356518309866563168045279114599985613547124474723725475695979472250845582165 +/- 9.03e-99]
floor_exp_T_lower= 97418971860452658435229799565334786147
floor_exp_T_upper= 97418971860452658435229799565334786147
q_transport= 97418971860452658435229799565334786148
minimality= True True
ER_upper= [9.890974306379110548771776148234686409635883135919320936786274721470032537690179506759083973857546787e-21 +/- 3.12e-121]
A0_lhs_upper= [0.04389999999999999999999999999999999999996413931036492446274698325043121358564087932899652844135325393 +/- 1.75e-102]
A0_strict_pass= True
fallback_2^63
C4= 9223372036854775808.000000000000000000000000000000000000000000000000000000000000000000000000000000000
C_pair_upper= [27502890015418359005139944.04704642755930702126045450130849405391307231944317295290986656193896757335 +/- 1.61e-75]
C_wrap_upper= [14303.70738137041797395677696207867564710182513507543638681150472020018931839998095743833338646574507 +/- 2.71e-96]
C_R_raw_upper= [76320519792785946239303037.51853713938695471405383100945599170717352552079077834625047826490599357599 +/- 1.24e-76]
C_R= 76320519792785946239303038 strict_upper= True
T= [88.04970697289454337008900656496602116904529865034040532909887016234795794546447163273957152833593260 +/- 6.85e-99]
floor_exp_T_lower= 173580874306054118126642045308435152888
floor_exp_T_upper= 173580874306054118126642045308435152888
q_transport= 173580874306054118126642045308435152889
minimality= True True
ER_upper= [9.890974306379110548771776148234686409662147314778234880892644378866013458780053828681514407006333374e-21 +/- 2.23e-121]
A0_lhs_upper= [0.04389999999999999999999999999999999999998223107756529539224249683589072013256774618473375038174465798 +/- 1.29e-102]
A0_strict_pass= True
delta_T_current_minus_primary_2^62_plus_1= [21.9496607177316014646974500060214427529785413073316637407932482061698093994468646835003356177914108 +/- 5.50e-98]
delta_T_current_minus_fallback_2^63= [21.3720380672649803736975570062385202495649231097824044115505135150665986912371500105554865977112999 +/- 2.02e-98]
primary_vs_fallback_delta_T= [-0.5776226504666210909998929997829225034136181975492593292427346911032107082097146729448490198801110 +/- 5.19e-98]
```

The fallback `A0_lhs_upper` line in the output above is intentionally quoted
from the exact run; its displayed Arb ball is strictly below (m=.0439), and
`A0_strict_pass= True` is the binding Boolean.  The primary and fallback
threshold floors agree at both endpoints, so the strict integer is

\[
 q_{\rm transport}=\lfloor e^T\rfloor+1.
\]

The receipt gives the three exact strict thresholds:

| atom coefficient | outward (C_R) | (T(C_R)) | strict A0 integer |
|---|---:|---:|---:|
| (2^{100}) (published) | `10489412368759562746433608215977724802` | `109.4217450401595237437865635712045...` | `332093267419812025416641789732742045430624465595` |
| (2^{62}+1) (primary) | `38160259896392973127946053` | `87.4720843224279222790891135651830...` | `97418971860452658435229799565334786148` |
| (2^{63}) (fallback) | `76320519792785946239303038` | `88.0497069728945433700890065649660...` | `173580874306054118126642045308435152889` |

The table is a transcription of the exact output immediately above; the
ellipses are not used as bounds or as inputs.  The primary threshold lowers
the unrounded log cutoff by the Arb-enclosed positive amount

\[
 21.9496607177316014646974500060214\ldots,
\]

and the fallback lowers it by

\[
 21.3720380672649803736975570062385\ldots.
\]

The exact Arb intervals for both differences are printed by the receipt.
The primary is strictly better than the fallback because the receipt prints
`primary_vs_fallback_delta_T` as a negative interval.  The threshold changes
are consequences of the selected A0 formula only; they do not close the
remaining full-program gates.

## 5. Candidate hierarchy and excluded tightenings

### Primary robust candidate — `PROVED COMPONENT`, combination pending referee

Use exactly the already accepted safe component ceilings (S=7.648) and
(M_0=2.775), the exact (F(12)=7940), and only replace the atom coefficient
by the directly proved

\[
 C_4'=2^{62}+1.
\]

This changes no domain, exponent, activation, wrap estimate, contour, or
transport hypothesis.  The complete Arb replay gives

\[
 C_R'=38160259896392973127946053.
\]

The label `PROVED COMPONENT` refers to the direct bridge coefficient and the
positive symbolic substitution.  The combined improved RATE-A theorem
constant remains **PENDING REFEREE** until the required cold report and
orchestrator replay are complete.

### Secondary fallback — `PROVED COMPONENT`, weaker

The coefficient (2^{63}) is the convenient power-of-two ceiling from the
bridge.  It is valid but strictly larger than (2^{62}+1), and its replay
gives (C_R^{63}=76320519792785946239303038).  It is retained as a fallback,
not called the strongest result.

### Component-only tightening of (S) — not combined

The source Arb receipt obtains the actual contour norm below the safe display
(7.648) (`BOUNDARY_ALPHA_THEOREM_SOL.md:140-200`).  One could write a new
explicit outward rational ceiling after a separately reviewed component
receipt.  This note deliberately keeps (S=7.648), so no such diagnostic
optimization is folded into (C_R').

### (M_0), (C_1), and wrap refinements — not claimed

The uniform source input is (M_0=2.775), and the independent wrap proof
consumes (C_1=128(1+\log2)) (`FW_RENEWAL_COUNT_SOL.md:485-498`).  Any smaller
choice would require a new complete proof and a separate referee.  No
secondary decimal, anchor-height value, finite census, or mpmath result is
promoted here.  In particular, the finite (y\le100) diagnostics in
`AM_REFEREE.md:255-358` remain diagnostic and do not alter this constant.

## 6. What may enter the theorem ledger after the gate

After a separate `CR_REDUCTION_REFEREE.md` confirms the bridge coefficient,
the source-invariant substitution, and the exact Arb replay, an append-only
dated ledger block may add the following alternative theorem statement:

> With the same balanced/matched boundary scope, (p=11/5),
> (alpha=6/5), (q_{\rm RATE}=12), (S=7.648), (M_0=2.775), and all
> existing paper-level Route-B/Ford hypotheses, the direct atom-moment
> coefficient (C_4'=2^{62}+1) yields
> (C_R'=38160259896392973127946053).  This is paper-level only; machine
> formalization and certified full-operator enclosure remain open.

The published (C_R^{\rm pub}), the original (C_4=2^{100}), and all prior
claims must remain in place.  The separate full-program onset remains an
explicit maximum over the RATE, divisor, holomorphy, geometry, monotonicity,
and finite-base gates (`BOUNDARY_ALPHA_THEOREM_SOL.md:663-671`).  No final
(q_0) promotion follows from this constant reduction.

## 7. Claim ledger

| Item | Status in this note | Receipt / source |
|---|---|---|
| (p=11/5), (alpha=6/5), (J_2=305), (J_4=91605) | **PROVED / exact source formula** | `BOUNDARY_ALPHA_THEOREM_SOL.md:510-540`; Arb replay above |
| (F(12)=7940) | **PROVED / exact** | `BOUNDARY_ALPHA_THEOREM_SOL.md:529-540`; replay above |
| (C_{\rm pair}(C_4)) | **PROVED / positive majorant** | `BOUNDARY_ALPHA_THEOREM_SOL.md:510-522`; replay above |
| (C_{\rm wrap}=p128(1+\log2)30) | **PROVED / referee-confirmed input** | `FW_RENEWAL_COUNT_SOL.md:475-498`; replay above |
| (M_0=2.775), (S=7.648) | **PROVED / retained safe ceilings** | `BOUNDARY_ALPHA_THEOREM_SOL.md:140-200,542-567` |
| Direct coefficient (C_4'=2^{62}+1) | **PROVED component, paper-level bridge** | `ATOM_MOMENT_BRIDGE_SOL.md:483-489`; `AM_REFEREE.md:223-231` |
| Primary combined (C_R') | **PENDING COLD REFEREE** | exact Arb replay above |
| Fallback combined (C_R^{63}) | **PENDING COLD REFEREE** | exact Arb replay above |
| Published (C_R^{\rm pub}) | **UNCHANGED / valid** | `BOUNDARY_ALPHA_THEOREM_SOL.md:24-55,689-740` |
| Machine RATE-A certification | **OPEN** | `RATE_A_REFEREE.md:305-307,369-392` |
| Full-program (q_0) | **OPEN / not claimed** | `BOUNDARY_ALPHA_THEOREM_SOL.md:663-671` |

No refutation was found.  The only proposed change is a separately gated,
strictly smaller upward constant obtained from a proved direct coefficient.

## 8. Autopsy completion after cold-review gap — 2026-08-19

The first cold referee found that Sections 2--5 reconstructed the constant and
printed the transport improvement but did not explicitly rank where the
orders of magnitude are lost.  This appended block closes that documentation
gap without changing either candidate constant.

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import arb, acb, ctx
ctx.dps=80
alpha=arb(6)/5
pub=arb(10489412368759562746433608215977724802)
primary=arb(38160259896392973127946053)
qpub=arb(332093267419812025416641789732742045430624465595)
qprimary=arb(97418971860452658435229799565334786148)
ratio=pub/primary
print('C4_ratio_2^100_over_2^62_plus_1=',arb(2)**100/(arb(2)**62+1))
print('CR_ratio_pub_over_primary=',ratio)
print('CR_log_gain=',ratio.log())
print('CR_decimal_orders_gain=',ratio.log()/arb(10).log())
print('predicted_A0_log_q_gain_5_over_6=',ratio.log()/alpha)
print('actual_transport_integer_ratio=',qpub/qprimary)
F12=arb(7940); Finf=arb(1225)/4
print('retained_F12_over_F_infinity=',F12/Finf)
print('counterfactual_F_log_q_headroom=',(F12/Finf).log()/alpha)
S=arb('7.648'); t0=(acb.zeta_zero(1)/2).imag
Strue=(arb('1.1')**2+(t0+arb('.5'))**2).sqrt()
print('retained_Splus1_over_exact_first_zero_Splus1=',(S+1)/(Strue+1))
p=arb(11)/5; pair_pref=2*arb.pi()**2*(S+1)*p
wrap=p*128*(1+arb(2).log())*30
inside=pair_pref*(arb(2)**62+1)*F12+wrap
print('retained_wrap_fraction_primary_raw=',wrap/inside)
PY
```

Output:

```text
C4_ratio_2^100_over_2^62_plus_1= [274877906943.99999994039535522460937501292469707114105741706316388494353544572607 +/- 1.41e-69]
CR_ratio_pub_over_primary= [274877906943.99999994010943445842741471236781422942372676070069066732083830942528 +/- 2.41e-69]
CR_log_gain= [26.339592861277921757636940007225731303574249568797996488951897847403771279336238 +/- 4.46e-79]
CR_decimal_orders_gain= [11.439139835231285418027453653682274464098627516442177144935850736695230219344481 +/- 2.31e-79]
predicted_A0_log_q_gain_5_over_6= [21.949660717731601464697450006021442752978541307331663740793248206169809399446865 +/- 4.44e-79]
actual_transport_integer_ratio= [3408917801.9197065874125291505009477738856775886079565124869054118074214408356601 +/- 1.63e-71]
retained_F12_over_F_infinity= [25.926530612244897959183673469387755102040816326530612244897959183673469387755102 +/- 7.23e-80]
counterfactual_F_log_q_headroom= [2.7127223269852038882840797465808487141537645626118542167461593807005333006743130 +/- 5.75e-80]
retained_Splus1_over_exact_first_zero_Splus1= [1.0001279946880542040326816790184759533388408736293087248331550148855713052518603 +/- 8.51e-81]
retained_wrap_fraction_primary_raw= [1.0401603157596627398211006085231419011537089926537046290030360458673782087083230e-21 +/- 6.97e-101]
```

Ranked loss ledger:

1. **Dominant, confirmed substitution:** the convenience ceiling
   (C_4=2^{100}) rather than the direct (2^{62}+1) costs the displayed
   (2.74877906944\times10^{11})-scale factor.  The assembled constant loses
   the same 11.439... decimal orders because the paired term dominates.  The
   exact RATE-A replacement is the primary result of this note.
2. **Secondary, diagnostic only:** the uniform absorption
   (F(q)\le F(12)=7940) retains a factor 25.926... relative to the limiting
   (1225/4).  It cannot simply be replaced in the all-(q\ge12) theorem;
   exploiting it for activation would require a new (q)-dependent fixed-point
   proof and referee.  The printed 2.712... log-cutoff headroom is therefore
   counterfactual, not a banked reduction.
3. **Negligible, diagnostic only:** replacing the safe (S=7.648) by the
   exact first-zero contour norm changes the (S+1) factor only by the printed
   1.000127... ratio.  No tighter rational ceiling is combined here.
4. **Not a useful target at the new scale:** the retained wrap contribution is
   only the printed (1.0402\times10^{-21})-scale fraction of the primary raw
   assembly.  Reducing it cannot remove an order of magnitude.
5. **Unranked for lack of a proved alternative:** (M_0=2.775) remains the
   accepted uniform safe bound.  No smaller full-contour bound is claimed, so
   assigning it speculative headroom would violate the ledger rule.

Finally, the exact (C_R) ratio has log 26.339..., and multiplication by
(1/\alpha=5/6) gives the independently printed 21.949... decrease in the A0
log cutoff.  The actual strict-integer transport cutoffs differ by the printed
3.4089-billion-scale ratio.  These are consequences of the selected A0
envelope only and still do not supply the missing finite block or a
full-program (q_0).
