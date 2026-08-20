# R5 activation arithmetic replay — LUNA lane

**Date:** 2026-08-20  
**Scope:** G2 mechanical arithmetic only. No proof or gate-status upgrade is made here.  
**Interpreters:** `/Users/za/.venvs/farey-rh/bin/python` (python-flint/Arb), `/Users/za/miniforge3/envs/pari-arb/bin/python3` (mpmath).  
**Rounding:** defect margins down; upper bounds and strict thresholds up.

## 1. Constants and source line receipts

Source receipt commands were run from the repository root with `nl -ba`:

```bash
nl -ba research_notes/rh_goals_2026-08-14/lane_g/BOUNDARY_ALPHA_THEOREM_SOL.md | sed -n '24,54p'
nl -ba research_notes/rh_goals_2026-08-14/lane_g/KF_WALL_ATTACK_SOL.md | sed -n '162,187p;469,480p;506,524p'
nl -ba research_notes/rh_goals_2026-08-14/lane_g/KF_WALL_REFEREE.md | sed -n '291,308p;330,371p;408,421p'
nl -ba research_notes/rh_goals_2026-08-14/lane_g/DH2_RENEWAL_PROOF_SOL.md | sed -n '698,732p'
nl -ba research_notes/rh_goals_2026-08-14/lane_g/R5_ASSEMBLY_EXECUTION_SOL.md | sed -n '228,299p'
nl -ba research_notes/rh_goals_2026-08-14/lane_g/HOLOMORPHY_GATE_SOL.md | sed -n '276,289p;563,580p'
```

Relevant output excerpts:

```text
BOUNDARY_ALPHA_THEOREM_SOL.md:24-39
For every integer q>=12 ... C_R=10489412368759562746433608215977724802 ... alpha=6/5=1.2, q_RATE=12.

KF_WALL_ATTACK_SOL.md:162-187
K_+=117 ... nu=0.1552 ... m=0.0439 ... log q>38.386+(5/6)log C_R.
KF_WALL_ATTACK_SOL.md:469-480
raw sup_{D_0}|F_q|<109; take the safe constant K_F=109.
KF_WALL_ATTACK_SOL.md:506-524
routeB_direct_base_upper=4.68727707957322768732242032506431855023...
routeB_direct_logq_CR1_upper=5599.98072458948676591556126523592642128...

KF_WALL_REFEREE.md:291-308
A0_logq_CR1_upper=38.38555358149782944200035562679008...
B_logq_CR1_upper=5599.98072458948676591556126523593...
KF_WALL_REFEREE.md:330-371
The exact A0 threshold is 38.3855535814978294420...; the exact Route-B threshold is 5599.9807245894...
The correction says not to chain from rounded 38.386 or 5599.981; 5599.982 is needed only when 4.687278 is the sole displayed premise.

DH2_RENEWAL_PROOF_SOL.md:698-712
d_* > 0.6603; the strict R5 test is E_3(q)<0.6603.

R5_ASSEMBLY_EXECUTION_SOL.md:230-299
q_A=floor(A_A^(1/p_A))+1; q_C=floor(A_C^(1/p_C))+1;
N_pre,H=max(...,N_monotone); N0^(H)=max(N_pre,H,N_A,N_C).
The general tail threshold requires a proved sup_{integer N>=Q} E_3^up(N)<d_delta.

HOLOMORPHY_GATE_SOL.md:285-288,578-580
R5-RATE and tail-monotone are CONJECTURAL / OPEN; activation of the mixing inequalities is currently UNDEFINED; positive full-boundary RATE and whole-tail monotonicity are genuinely OPEN.
```

| quantity | value used in this replay | source + line receipt | status retained |
|---|---:|---|---|
| \(C_R\) | `10489412368759562746433608215977724802` | `BOUNDARY_ALPHA_THEOREM_SOL.md:24-32` | source-listed RATE ceiling; downstream use remains conditional on the source caveats |
| \(\alpha\) | \(6/5\) | `BOUNDARY_ALPHA_THEOREM_SOL.md:35-40` | source-listed |
| \(q_{\rm RATE}\) | `12` | `BOUNDARY_ALPHA_THEOREM_SOL.md:24-40` | activation number, not a final all-gates onset |
| safe \(K_+\) | `117` | `KF_WALL_ATTACK_SOL.md:162-187`; correction ledger `KF_WALL_REFEREE.md:412-419` | raw \(K_+<117\), safe ledger constant \(K_+=117\) |
| safe \(K_F\) | `109` | `KF_WALL_ATTACK_SOL.md:469-480`; `KF_WALL_REFEREE.md:414-419` | raw supremum \(<109\); use safe \(K_F=109\), not \(K_F<109\) as a chosen constant |
| A0 threshold base \(B_A\) | `38.385553581497829442000355626790...` | `KF_WALL_REFEREE.md:291-295,330-351` | corrected full-precision conditional diagnostic |
| Route-B threshold base \(B_B\) | `5599.980724589486765915561265235...` | `KF_WALL_REFEREE.md:307-308,353-371` | corrected full-precision conditional diagnostic |
| defect target \(d_0\) | `0.6603` | `DH2_RENEWAL_PROOF_SOL.md:698-712` | rounded-down strict target; the full DH2/R4 gate remains caveated |

The correction blocks are binding: this replay uses \(B_A\) and \(B_B\) at their full-precision receipts. It does not use the rounded displays `38.386`, `5599.981`, or the displayed Route-B base `4.687278` as arithmetic inputs.

## 2. Chain replay

### Step 1 — logarithmic \(C_R\) contribution

Formula:

\[
L:=\frac56\log C_R.
\]

Plugged numbers: \(C_R=10489412368759562746433608215977724802\), with exact integer input and rational \(5/6\).

Receipt A1 command:

```bash
PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import arb, ctx
ctx.prec = 512
CR=arb(10489412368759562746433608215977724802)
print('backend=python-flint Arb prec_bits=',ctx.prec)
print('C_R=',CR)
print('log_C_R=',CR.log())
print('L=(5/6)log_C_R=',(arb(5)/6)*CR.log())
PY
```

Receipt A1 output:

```text
backend=python-flint Arb prec_bits= 512
C_R= 10489412368759562746433608215977724802.0000...
log_C_R= [85.24342975039403316214344953329735873609421331129860968190200317998352306256 +/- 5.61e-152]
L=(5/6)log_C_R= [71.03619145866169430178620794441446561341184442608217473491833598331960255213 +/- 6.14e-152]
```

Independent mpmath receipt:

```text
backend=mpmath dps= 120
log_C_R= 85.24342975039403316214344953329735873609421331129860968190200317998352306256162693813384541078384951
L=(5/6)log_C_R= 71.03619145866169430178620794441446561341184442608217473491833598331960255213468911511153784231987459
```

### Step 2 — A0 strict transport cutoff

Formula from the A0 chain:

\[
 T_A=B_A+\frac56\log C_R,
 \qquad \log q>T_A,
 \qquad q_{A0}=\lfloor e^{T_A}\rfloor+1.
\]

The source formula cross-check is

\[
B_A=\frac{(1-\nu)\log K_+-\log m}{\alpha\nu},
\quad (K_+,\nu,m,\alpha)=(117,0.1552,0.0439,6/5).
\]

Receipt A2--A4 command (Arb; all threshold inputs are integer or decimal strings):

```bash
PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import arb, ctx
ctx.prec = 512
def floor_int(x):
    return int(str(x.floor()).split('.')[0])
CR=arb(10489412368759562746433608215977724802)
alpha=arb(6)/5; q_rate=12; d0=arb(6603)/10000
L=(arb(5)/6)*CR.log()
A=arb('38.3855535814978294420003556267900758051983773340406350057310476940949540845669325281835202839273579004267025611445252549')
B=arb('5599.98072458948676591556126523592642128')
TA=A+L; TB=B+L
qA=floor_int(TA.exp().upper())+1
Kp=arb(117); nu=arb(1552)/10000; m=arb(439)/10000
A_formula=((1-nu)*Kp.log()-m.log())/(alpha*nu)
qA_formula=floor_int((A_formula+L).exp().upper())+1
checks=((TA-arb(qA-1).log())>=0 and (arb(qA).log()-TA)>0)
print('backend=python-flint Arb prec_bits=',ctx.prec)
print('C_R=',CR)
print('alpha=',alpha,'q_RATE=',q_rate,'d0=',d0)
print('log_C_R=',CR.log())
print('L=(5/6)log_C_R=',L)
print('A0_base=',A.upper())
print('A0_base_formula_117_0.1552_0.0439=',A_formula)
print('A0_base_formula_le_banked=',bool(A_formula<=A))
print('T_A0=',TA.upper())
print('exp_T_A0=',TA.exp().upper())
print('q_A0=floor(exp(T_A0))+1=',qA)
print('q_A0_formula_replay=',qA_formula)
print('A0_strict_interval_checks=',checks)
print('RouteB_base=',B.upper())
print('T_RouteB=',TB.upper())
print('RouteB_log10_T=',TB/arb(10).log())
print('RouteB_integer_digits=',floor_int((TB/arb(10).log()).lower())+1)
print('RouteB_q_strict_form=floor(exp(T_RouteB))+1')
print('local_max(12,q_RATE,q_A0)=',max(12,q_rate,qA))
print('R5_H_missing=C_3,p_3,nu_seed,omega_*,nu_a,m_infty_a,q_pre_H')
print('R5_H_q_A=UNDEFINED; R5_H_q_C=UNDEFINED')
print('final_q0=UNDEFINED; blocker=q_monotone/whole-tail')
PY
```

Receipt A2 output:

```text
backend=python-flint Arb prec_bits= 512
A0_base= [38.38555358149782944200035562679007580519837733404063500573104769409495408456 ...]
A0_base_formula_117_0.1552_0.0439= [38.38555358149782944200035562679007580519837733404063500573104769409495408743 ...]
A0_base_formula_le_banked= True
T_A0= [109.42174504015952374378656357120454141861022176012280974064938367741455663670 ...]
exp_T_A0= [332093267419812025416641789732742045430624465594.62213423390800811103446340537049 ...]
q_A0=floor(exp(T_A0))+1= 332093267419812025416641789732742045430624465595
q_A0_formula_replay= 332093267419812025416641789732742045430624465595
A0_strict_interval_checks= True
```

The Arb interval places \(e^{T_A}\) strictly between the displayed adjacent integers, so the strict upward-rounded conditional cutoff is

\[
\boxed{q_{A0}=332093267419812025416641789732742045430624465595.}
\]

Independent mpmath receipt:

```text
T_A0= 109.4217450401595237437865635712045414186102217601228097406493836774145566367016216432950581262472325
exp_T_A0= 332093267419812025416641789732742045430624465594.6221342339080081110344634053704960912159652475974605
q_A0=floor(exp(T_A0))+1= 332093267419812025416641789732742045430624465595
```

The exact mpmath command producing this receipt is printed under Step 3; that one command computes both Step 2 and Step 3.

This is a conditional A0 transport cutoff only. It is not \(q_0\).

### Step 3 — corrected Route-B diagnostic cutoff

Formula:

\[
 T_B=B_B+\frac56\log C_R,
 \qquad \log q>T_B,
 \qquad q_B=\lfloor e^{T_B}\rfloor+1.
\]

Plugged numbers: the corrected full-precision \(B_B=5599.98072458948676591556126523592642128\ldots\), not `5599.981` chained from a rounded base.

Receipt A3 output from the same command:

```text
RouteB_base= [5599.98072458948676591556126523592642128 ...]
T_RouteB= [5671.01691604814846021734747318034088689341184442608217473491833598331960255213 ...]
RouteB_log10_T= [2462.89135341970760060200089842428415695234854617771563649292180636213401768989 ...]
RouteB_integer_digits= 2463
RouteB_q_strict_form=floor(exp(T_RouteB))+1
```

Independent mpmath command:

```bash
PYTHONDONTWRITEBYTECODE=1 /Users/za/miniforge3/envs/pari-arb/bin/python3 - <<'PY'
import mpmath as mp
mp.mp.dps=120
CR=mp.mpf('10489412368759562746433608215977724802')
A=mp.mpf('38.3855535814978294420003556267900758051983773340406350057310476940949540845669325281835202839273579004267025611445252549')
B=mp.mpf('5599.98072458948676591556126523592642128')
L=(mp.mpf(5)/mp.mpf(6))*mp.log(CR); TA=A+L; TB=B+L
print('backend=mpmath dps=',mp.mp.dps)
print('log_C_R=',mp.nstr(mp.log(CR),100))
print('L=(5/6)log_C_R=',mp.nstr(L,100))
print('T_A0=',mp.nstr(TA,100))
print('exp_T_A0=',mp.nstr(mp.exp(TA),100))
print('q_A0=floor(exp(T_A0))+1=',int(mp.floor(mp.exp(TA)))+1)
print('T_RouteB=',mp.nstr(TB,100))
print('RouteB_log10_T=',mp.nstr(TB/mp.log(10),100))
PY
```

Independent mpmath output:

```text
T_RouteB= 5671.016916048148460217347473180340886893411844426082174734918335983319602552134689115111537842319875
RouteB_log10_T= 2462.891353419707600602000898424284156952348546177715636492921806362134017689898079672216656452108068
```

Thus the exact strict integer is represented without a lossy decimal expansion as

\[
q_B=\lfloor\exp(5671.0169160481484602173474731803408868934\ldots)\rfloor+1,
\]

with `2463` decimal digits. This Route-B diagnostic is conditional and route-specific; it is not merged with the A0 cutoff or with the DH2 defect target.

### Step 4 — R5-H activation assembly and missing evaluations

The R5-H formulas are:

\[
A_A=\frac{2K_+^{1-\nu_a}C_R^{\nu_a}}{m_{\infty,a}},
\quad p_A=\alpha\nu_a,
\quad q_A=\lfloor A_A^{1/p_A}\rfloor+1,
\]

\[
A_C=\frac{C_3}{d_\delta},
\quad p_C=\alpha\nu_{\rm seed}\omega_*,
\quad q_C=\lfloor A_C^{1/p_C}\rfloor+1,
\]

\[
q_0^{(H)}=\max(q_{\rm pre,H},q_A,q_C),
\]

where \(q_{\rm pre,H}\) includes the activation gates and \(q_{\rm monotone}\). The DH2 receipt supplies the rounded-down strict defect target \(d_0=0.6603\), so the intended strict test is \(E_3(q)<d_0\). It does not supply the missing R5 transport quantities \(C_3,p_C,\nu_{\rm seed},\omega_*\), nor the anchor quantities \(\nu_a,m_{\infty,a}\).

Receipt A4 output:

```text
alpha= [1.2000 ...] q_RATE= 12 d0= [0.6603000 ...]
R5_H_missing=C_3,p_3,nu_seed,omega_*,nu_a,m_infty_a,q_pre_H
R5_H_q_A=UNDEFINED; R5_H_q_C=UNDEFINED
local_max(12,q_RATE,q_A0)= 332093267419812025416641789732742045430624465595
final_q0=UNDEFINED; blocker=q_monotone/whole-tail
```

Therefore the R5-H \(q_A\) and \(q_C\) evaluations are honestly `UNDEFINED`; no surrogate values are inserted.

## 3. Threshold verdict

The finite arithmetic that is defined by the banked constants is:

| conditional item | strict result |
|---|---:|
| RATE activation | \(q_{\rm RATE}=12\) |
| A0 transport | \(q_{A0}=332093267419812025416641789732742045430624465595\) |
| Route-B diagnostic | \(q_B=\lfloor e^{5671.0169160481484602173474731803408868934\ldots}\rfloor+1\) |
| R5-H anchor \(q_A\) | `UNDEFINED` — \(\nu_a,m_{\infty,a}\) absent |
| R5-H defect crossing \(q_C\) | `UNDEFINED` — \(C_3,p_3,\nu_{\rm seed},\omega_*\) absent |
| final all-gates \(q_0\) | **`UNDEFINED`** |

The exact blocker for the final \(q_0\) is the open `q_monotone` / whole-tail monotonicity gate: the source ledger says it is OPEN, and the general R5 threshold requires a proved tail supremum. In addition, the R5-H symbolic \(q_A,q_C\) inputs above are not instantiated. The local A0 maximum is only

\[
\max(12,q_{\rm RATE},q_{A0})=q_{A0},
\]

but this does not evaluate \(q_0^{(H)}\) or close the all-gates ledger.

Receipt A2--A4 output for that local maximum and verdict:

```text
local_max(12,q_RATE,q_A0)= 332093267419812025416641789732742045430624465595
final_q0=UNDEFINED; blocker=q_monotone/whole-tail
```

## 4. CONDITIONAL dependencies

1. The boundary inequality \(E_R(q)\le C_Rq^{-6/5}\) and its activation at \(q\ge12\) retain the source's paper-level/input caveats. This replay does not promote a whole-boundary machine theorem.
2. The A0 cutoff is conditional on the A0 holomorphy/domain/divisor premises and the side hypothesis used by the two-constants step. \(K_+=117\) is the safe ledger value corresponding to a raw \(<117\) statement.
3. The \(K_F\) value is used only as the safe constant \(K_F=109\). The raw \(<109\) wall is conditional on the stated \(H_0\), anchor, holomorphy, and reflection premises.
4. The DH2 value \(d_0=0.6603\) is used only as a rounded-down strict target. The full continuous defect/renewal gate remains caveated; no sampled value is promoted to a new theorem.
5. R5-H requires the absent \(C_3,p_3,\nu_{\rm seed},\omega_*,\nu_a,m_{\infty,a}\), plus every \(q_{\rm pre,H}\) activation and every non-integer analytic gate.
6. The `q_monotone` / whole-tail monotonicity gate is OPEN. Any threshold obtained by a pointwise or pure-power crossing is conditional until the all-integer-tail supremum is proved.
7. A finite base block and any remaining holomorphy/divisor/geometry gates are separate from the arithmetic cutoffs. They are not silently absorbed into the displayed A0 maximum.

READY FOR JUDGING
