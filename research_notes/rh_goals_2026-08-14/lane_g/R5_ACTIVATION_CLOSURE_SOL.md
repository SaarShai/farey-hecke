# R5 activation closure: selected A0 whole-tail envelope

**Date:** 2026-08-19
**Program:** `(RATE)` / R5, lane G
**Interpreter:** `/Users/za/.venvs/farey-rh/bin/python` (`python-flint` / Arb)
**Scope:** paper-level activation arithmetic for the selected first-zero A0
route; no finite-base computation is promoted.

## 0. Verdict

The selected A0 route has a finite, strict analytic-tail onset at the
paper-level RATE scope:

\[
 q_{\rm transport}
 =332093267419812025416641789732742045430624465595.
 \tag{0.1}
\]

The upper envelope used to obtain it is strictly decreasing on real
`q > 0`. Thus one strict check at `q_transport`, together with the
paper-level RATE theorem for every integer `q >= 12`, closes the A0
whole-tail envelope gate. This does **not** assert that the unknown actual
error function `E_R(q)` is itself monotone; only its proved upper envelope is
used.

The literal integer analytic-tail ledger is

\[
\begin{aligned}
 q_{0,\mathrm{analytic}}
 &=\max\{q_{\rm RATE},q_{\rm divisor},q_{\rm side},q_{\rm transport}\}\\
 &=\max\{12,3,134010166814705707171424895246,
          332093267419812025416641789732742045430624465595\}
 =q_{\rm transport}.
\end{aligned}
\tag{0.2}
\]

The integer terms and their scopes are receipted in Sections 2--5. The A0
theta contour and its two geometric floors are q-independent analytic
`PASS` gates; there is no source-defined numeric `q_geometry`. Likewise,
the derivative calculation is an analytic `PASS` for every real `q > 0`,
not an artificial integer `q_monotone`. The strict side threshold
`q_side=134010166814705707171424895246` is independently receipted in
Section 4 and is dominated by `q_transport`.

This is **not** a completed all-q R5 pincer. The finite block below the
astronomical analytic onset remains **OPEN / UNDEFINED**: the repository has
no proved true scalar-`phi_q` meromorphic-continuation evaluator and winding
certificate for every finite index in that block. The existing determinant
surrogates are explicitly `NOT EVIDENCE` for this target. No finite timing
run is promoted.

The requested single ledger pairing `K_F=109` with the old
`d_*>0.6603` is **REFUTED as a domain combination**. It mixes the sixth-zero
Route-B wall with the first-zero defect. The correction does not refute either
conditional source theorem: selected A0 uses `K_+=117`, `m_z`, and `nu_z`; the
separate sixth-zero Route-B wall uses safe `K_F=109` and its own
`d_*>0.3186` defect.

## 1. Receipts before claims

All load-bearing source files were hashed from this worktree before the
claims below.

Command:

```bash
shasum -a 256 research_notes/rh_goals_2026-08-14/lane_g/{BOUNDARY_ALPHA_THEOREM_SOL,AM_REFEREE,RATE_A_REFEREE,R5_ASSEMBLY_EXECUTION_SOL,DH2_RENEWAL_PROOF_SOL,HOLOMORPHY_GATE_SOL,KF_WALL_ATTACK_SOL,KF_WALL_REFEREE,R3_TRANSPORT_EXECUTION_SOL,R3_ROUTE_B_TRANSPORT_SOL,R3_R5_ASSEMBLY_PLAN_SOL}.md
```

Output:

```text
58441b334a5f279aae6298e3b5383ef5677b3e6ec6e7d5bc6a908a4936111e6e  research_notes/rh_goals_2026-08-14/lane_g/BOUNDARY_ALPHA_THEOREM_SOL.md
3d655f2c05395688be73e8786cd9a954182cc4842005ff9e7662d05cccf503b4  research_notes/rh_goals_2026-08-14/lane_g/AM_REFEREE.md
b835804104f502f54cc757336ba8fe54a82a05eaa18261a4d78f697aba358590  research_notes/rh_goals_2026-08-14/lane_g/RATE_A_REFEREE.md
842b4a923dc71943cd933507039c087071891f4ec0aa944407cbf7bbd6f5ec14  research_notes/rh_goals_2026-08-14/lane_g/R5_ASSEMBLY_EXECUTION_SOL.md
096d389905ad21505e2c25c30aa37b5a2fa3d3f6d054bcb30229096fc5c8d885  research_notes/rh_goals_2026-08-14/lane_g/DH2_RENEWAL_PROOF_SOL.md
54e5df9bdaaba537b3b051cbb4ee46b4d29750c480632824120824b45888cdea  research_notes/rh_goals_2026-08-14/lane_g/HOLOMORPHY_GATE_SOL.md
efa518c9908e3c68005c3b7349bdee6c4af63dc7146ef85b13882560c2644aad  research_notes/rh_goals_2026-08-14/lane_g/KF_WALL_ATTACK_SOL.md
73c6eb59b25038f9e23ae38fa8c409af65d50fd0219b45417022663486361710  research_notes/rh_goals_2026-08-14/lane_g/KF_WALL_REFEREE.md
a6b6a1297fc4401e47e194a809064baa5cade1f9effb29fe28e3bde47d3b6345  research_notes/rh_goals_2026-08-14/lane_g/R3_TRANSPORT_EXECUTION_SOL.md
320c21a8d0558418531f23c1ecffd3e489c5c1ff12180ce29c8f9f90d9177468  research_notes/rh_goals_2026-08-14/lane_g/R3_ROUTE_B_TRANSPORT_SOL.md
ca7277a29282abae45c3133438262f2a4d067624ec9e1dccbe309beb059962cc  research_notes/rh_goals_2026-08-14/lane_g/R3_R5_ASSEMBLY_PLAN_SOL.md
```

The RATE-A source and its atom-moment referee retain the exact status
qualification: `CONFIRMED` at paper level, balanced/matched boundary scope,
not machine-verified. This is the status used here, not a stronger status:
`BOUNDARY_ALPHA_THEOREM_SOL.md:689-730` and `AM_REFEREE.md:360-389,405-408`.

## 2. Selected A0 ledger and source scope

The selected route is Candidate A0 in the first-zero geometry. Its fixed
domain and contour are

\[
 t_0=\gamma_1/2,\quad
 \Omega=\{1/2<\Re s<11/10,\ |\Im s-t_0|<1/2\},\quad
 \Gamma_R=\{11/10+it:|t-t_0|\le1/2\},
\]

with

\[
 m_z:=\min_{\partial D_z}|\phi_\infty|\ge0.0439,
 \qquad
 \nu_z:=\inf_{\partial D_z}\omega(\cdot,\Gamma_R;\Omega)\ge0.1552.
 \tag{2.1}
\]

These are the A0 source values and statuses (`PROVED`, Arb interval cover),
not the sixth-zero wall values: `R3_TRANSPORT_EXECUTION_SOL:20-97,237-252`.
The A0 side bound is the safe ledger value `K_+=117`, confirmed for the same
quantity by `KF_WALL_REFEREE.md:27-31,211-240,409-414` and used by the
boundary theorem at `BOUNDARY_ALPHA_THEOREM_SOL.md:600-613`.

The RATE-A source supplies, on this same first-zero boundary and for every
integer `q >= 12`,

\[
 E_R(q):=\sup_{s\in\Gamma_R}|\phi_q(s)-\phi_\infty(s)|
 \le C_Rq^{-\alpha},
 \quad C_R=10489412368759562746433608215977724802,
 \quad \alpha=6/5.
 \tag{2.2}
\]

The paper-level promotion and the exact RATE onset are stated at
`BOUNDARY_ALPHA_THEOREM_SOL:24-40,689-730`; the independent RATE referee
confirms `q_RATE=12` and the first-zero/A0 scope at
`RATE_A_REFEREE.md:308-324,326-351`.

The A0 inequality consumed by the two-constants/Rouché implication is

\[
 K_+^{1-\nu}(C_Rq^{-\alpha})^\nu<m,
 \qquad K_+=117,\quad \nu=0.1552,\quad m=0.0439,
 \quad \alpha=6/5.
 \tag{2.3}
\]

This is the selected first-zero A0 ledger. It uses neither `K_F` nor any
`d_*` defect; that exclusion is explicit at
`BOUNDARY_ALPHA_THEOREM_SOL:657-661` and `KF_WALL_REFEREE.md:375-387`.

## 3. Whole-tail monotonicity of the fixed envelope

Define the fixed A0 upper envelope

\[
 U(q):=K_+^{1-\nu}C_R^\nu q^{-\alpha\nu},\qquad q>0.
 \tag{3.1}
\]

All factors other than the final power are positive. The exact rational
values are

\[
 \nu=0.1552=97/625,
 \qquad \alpha=6/5,
 \qquad \beta:=\alpha\nu=582/3125=0.18624>0.
 \tag{3.2}
\]

Therefore elementary differentiation gives

\[
 U'(q)=-\beta K_+^{1-\nu}C_R^\nu q^{-\beta-1}<0
 \qquad(q>0).
 \tag{3.3}
\]

This proves the whole-tail monotonicity gate for the **upper envelope**. It
does not prove `E_R'(q)<0`, nor does it need to: (2.2) and (3.3) imply
`E_R(q) <= U(q) <= U(q_transport)` for every integer `q >= q_transport`.
The distinction is required by the R5 source, which warns that a single
crossing must be promoted only after a tail supremum and all activations are
proved: `R5_ASSEMBLY_EXECUTION_SOL:163-176,202-213` and
`HOLOMORPHY_GATE_SOL:276-289`.

## 4. Fresh strict Arb activation arithmetic

The strict inequality (2.3) is equivalent to

\[
 \log q>T,
 \qquad
 T=\frac{(1-\nu)\log K_+-\log m}{\alpha\nu}
       +\frac{1}{\alpha}\log C_R.
 \tag{4.1}
\]

The nonzero-branch side condition has its own strict threshold

\[
 C_Rq^{-\alpha}<K_+
 \quad\Longleftrightarrow\quad
 \log q>T_{\rm side}:=\frac{\log C_R-\log K_+}{\alpha}.
 \tag{4.2}
\]

Its binding integer is also `floor(exp(T_side))+1`; it must be computed from
the unrounded Arb interval rather than from a displayed decimal.

No displayed decimal is exponentiated. Because the inequality is strict, the
integer is `floor(exp(T))+1`, after checking that the lower and upper Arb
endpoints agree on the floor.

Binding command, complete stdin program:

```bash
PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import arb, ctx
ctx.dps = 120

def exact_integer(a):
    s = str(a)
    assert '+/-' not in s and 'e' not in s.lower()
    whole, frac = s.split('.', 1)
    assert set(frac) <= {'0'}
    return int(whole)

alpha = arb(6) / 5
nu = arb('0.1552')
m = arb('0.0439')
K = arb(117)
CR = arb(10489412368759562746433608215977724802)
q_rate = 12
q_divisor = 3
beta = alpha * nu
T_side = (CR.log() - K.log()) / alpha
exp_T_side = T_side.exp()
floor_side_lo = exact_integer(exp_T_side.lower().floor())
floor_side_hi = exact_integer(exp_T_side.upper().floor())
q_side = floor_side_hi + 1
T = ((1 - nu) * K.log() - m.log()) / beta + CR.log() / alpha
exp_T = T.exp()
floor_lo = exact_integer(exp_T.lower().floor())
floor_hi = exact_integer(exp_T.upper().floor())
q_transport = floor_hi + 1
ER_side = CR * arb(q_side) ** (-alpha)
ER_transport = CR * arb(q_transport) ** (-alpha)
U = K ** (1 - nu) * ER_transport ** nu
print('alpha=', alpha)
print('nu=', nu)
print('alpha_nu=', beta)
print('beta_exact=582/3125=0.18624')
print('q_RATE=', q_rate)
print('q_divisor=', q_divisor)
print('T_side=', T_side)
print('floor_exp_T_side_lower=', floor_side_lo)
print('floor_exp_T_side_upper=', floor_side_hi)
print('q_side=', q_side)
print('side_minimality_log_q_gt_T_side=', bool(arb(q_side).log() > T_side))
print('side_minimality_log_q_minus_1_le_T_side=', bool(arb(q_side - 1).log() <= T_side))
print('ER_at_q_side_upper=', ER_side.upper())
print('ER_at_q_side_lt_Kplus=', bool(ER_side < K))
print('T=', T)
print('floor_exp_T_lower=', floor_lo)
print('floor_exp_T_upper=', floor_hi)
print('q_transport=', q_transport)
print('minimality_log_q_gt_T=', bool(arb(q_transport).log() > T))
print('minimality_log_q_minus_1_le_T=', bool(arb(q_transport - 1).log() <= T))
print('ER_at_q_transport_upper=', ER_transport.upper())
print('ER_nonzero_branch_lt_Kplus=', bool(ER_transport < K))
print('A0_envelope_at_q_transport_upper=', U.upper())
print('A0_strict_lt_m=', bool(U < m))
print('q_side_lt_q_transport=', q_side < q_transport)
print('q_transport_ge_q_RATE=', q_transport >= q_rate)
print('q_transport_ge_q_divisor=', q_transport >= q_divisor)
PY
```

Complete stdout:

```text
alpha= [1.20000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 +/- 2.72e-121]
nu= [0.155200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 +/- 1.38e-122]
alpha_nu= [0.186240000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 +/- 9.98e-122]
beta_exact=582/3125=0.18624
q_RATE= 12
q_divisor= 3
T_side= [67.0677131796635642027495596815724906016616368757440863850113075017042248406666656874891993647632465360331184041008546188 +/- 4.66e-119]
floor_exp_T_side_lower= 134010166814705707171424895245
floor_exp_T_side_upper= 134010166814705707171424895245
q_side= 134010166814705707171424895246
side_minimality_log_q_gt_T_side= True
side_minimality_log_q_minus_1_le_T_side= True
ER_at_q_side_upper= [116.999999999999999999999999999315617648739858556713104224034776804010192662957016629502243073637056151946692896165365874 +/- 3.49e-118]
ER_at_q_side_lt_Kplus= True
T= [109.421745040159523743786563571204541418610221760122809740649383677414556636701621643295058126247232491747486173765945251 +/- 3.60e-118]
floor_exp_T_lower= 332093267419812025416641789732742045430624465594
floor_exp_T_upper= 332093267419812025416641789732742045430624465594
q_transport= 332093267419812025416641789732742045430624465595
minimality_log_q_gt_T= True
minimality_log_q_minus_1_le_T= True
ER_at_q_transport_upper= [9.89097430637911054877177614823468640968794281344579185756013275732945984464792127524610837468979670054487699612505873990e-21 +/- 2.75e-141]
ER_nonzero_branch_lt_Kplus= True
A0_envelope_at_q_transport_upper= [0.0438999999999999999999999999999999999999999999999906971726823547524124317246131129625859299593282570137277179991715092729 +/- 3.75e-122]
A0_strict_lt_m= True
q_side_lt_q_transport= True
q_transport_ge_q_RATE= True
q_transport_ge_q_divisor= True
```

The side same-floor output proves the binding side integer is exactly
`floor(exp(T_side))+1`; its two `side_minimality_*` lines prove both endpoint
inequalities for the strict side condition. The transport same-floor output
proves the binding transport integer is exactly `floor(exp(T))+1`; its two
`minimality_*` lines prove both endpoint inequalities:

\[
 \log q_{\rm transport}>T,
 \qquad
 \log(q_{\rm transport}-1)\le T.
 \tag{4.3}
\]

The side threshold is independently smaller than the transport threshold
(`q_side_lt_q_transport=True`). The nonzero branch side hypothesis is
therefore closed from `q_transport` onward; the receipt also directly gives
`E_R(q_transport) < K_+=117`. If `E_R(q)=0`, the A0 implication is immediate,
as recorded in `BOUNDARY_ALPHA_THEOREM_SOL:615-623`. Since the fixed RATE
envelope is decreasing, the same side inequality holds for every
`q >= q_transport`.

Finally, the receipt gives the strict A0 mix below `m=0.0439` at the binding
integer. Equation (3.3) carries that strict inequality to the complete
integer tail. No rounded base or rounded threshold is used.

## 5. Audit of every analytic-tail onset term

### 5.1 RATE activation

`q_RATE=12` is sourced by the RATE-A theorem and its adversarial referee:
the analytic absorption uses `F(12)=7940`, so the activation is not a fitted
numerical crossover (`BOUNDARY_ALPHA_THEOREM_SOL:584-598`;
`RATE_A_REFEREE.md:308-324`). The promotion remains paper-level and
balanced/matched, not machine-certified (`AM_REFEREE.md:371-408`).

### 5.2 Divisor/pole activation

The printed-theory holomorphy audit closes the finite trivial scalar scattering
coefficient on the full right `H_0` and A0/Route-B right domains for every
finite Hecke index `q >= 3`, with

\[
 q_{\rm pole}=q_{\rm divisor}=3.
 \tag{5.1}
\]

The same source explicitly rejects a family-wide nonvanishing assertion and
uses the contradiction case split instead; nonvanishing is not silently
promoted (`HOLOMORPHY_GATE_SOL:254-264,363-389`). Thus `q_divisor=3` is a
pole/holomorphy threshold only.

### 5.3 Geometry and side activation

The A0 contour, `m_z >= 0.0439`, and `nu_z >= 0.1552` are fixed theta-side
geometric receipts, not q-dependent measurements
(`R3_TRANSPORT_EXECUTION_SOL:38-66,237-252`). They are an analytic
`PASS` geometry gate, with no source-defined integer `q_geometry`; no numeric
geometry onset is inserted into (0.2). The finite-group `q>=3` domain is
already covered by `q_divisor=3` in (5.1), without reusing it as a geometry
claim.
The non-RATE side is bounded by the safe `K_+=117` ledger
(`KF_WALL_REFEREE.md:27-31,211-240`). The fresh Arb receipt proves the
minimal strict side threshold
`q_side=134010166814705707171424895246`, with floor agreement and
`q_side_lt_q_transport=True`. Thus the side condition is included as an actual
integer term in (0.2), and there is no hidden second side threshold.

### 5.4 Monotonicity activation

The derivative proof (3.3) is valid for every real `q>0`, so whole-tail
monotonicity is an analytic `PASS` gate, not an integer `q_monotone` term.
This is monotonicity of `U`, not of `E_R`. The distinction is exactly the
direction required by the R5 conditional algebra
(`R5_ASSEMBLY_EXECUTION_SOL:163-176`).

Consequently every integer term in the analytic-tail max (0.2) is sourced and
finite, while geometry and monotonicity are separately recorded analytic
`PASS` gates. The displayed equality to `q_transport` is a paper-level
conditional analytic-tail statement.

## 6. Domain correction: why `K_F=109` plus `d_*>0.6603` fails

The proposed pairing is not a valid single transport ledger. The source
records the first-zero A0 contour as the segment consumed by A0, while the
rebuilt direct `K_F` route uses sixth-zero geometry:
`RATE_A_REFEREE.md:326-351`.

The corrected domain-matched ledgers are:

| route | boundary/geometry | constants consumed | status |
|---|---|---|---|
| selected A0 | first-zero `t_0=gamma_1/2` contour | `K_+=117`, `m_z>=0.0439`, `nu_z>=0.1552`; neither `K_F` nor `d_*` | conditional A0 implication, now with the paper-level RATE input |
| rebuilt Route B | sixth-zero shift `t_c=t_6-0.050005`, `delta=0.9999` | safe `K_F=109`, sixth-zero `d_*>0.3186` | conditional under full `H_0`, anchor, holomorphy/reflection |
| old first-zero R5 window | first-zero `t_0` window | `d_*>0.6603` | separate defect certificate; not the sixth-zero wall |

The source receipt for this correction is explicit: A0 consumes neither
`d_*>0.6603` nor `d_*>0.3186`; the sixth-zero chain consumes `d_*>0.3186`,
and the old `d_*>0.6603` belongs to the first-zero Route-B window
(`KF_WALL_REFEREE.md:375-390`; `DH2_RENEWAL_PROOF_SOL:696-712`). This is a
domain correction, not a refutation of either conditional theorem.

The `K_F=109` wall therefore does not enter (2.3), (3.1), or (4.1). Feeding
RATE-A's first-zero boundary into that sixth-zero wall would be a domain error,
not an optimization.

## 7. Finite-base coverage: separate verdict

The analytic tail in (0.2) does not certify the finite indices below it. A
scoped inventory and source-status search was run before this verdict.

Command:

```bash
printf '%s\n' '$ git ls-tree -r HEAD -- engine/certify'
git ls-tree -r HEAD -- engine/certify
printf '%s\n' '$ rg --files research_notes/rh_goals_2026-08-14/lane_g | rg -i "(evaluator|winding|certif|finite.*q|q.*finite|detdcH|rate_measure)" | sort'
rg --files research_notes/rh_goals_2026-08-14/lane_g | rg -i '(evaluator|winding|certif|finite.*q|q.*finite|detdcH|rate_measure)' | sort
printf '%s\n' '$ rg -n -i "true.*phi|finite.*evaluator|certified.*winding|dimension tail|NOT EVIDENCE|SCOUT_FAILED|REJECTED" ...'
rg -n -i 'true.*phi|finite.*evaluator|certified.*winding|dimension tail|NOT EVIDENCE|SCOUT_FAILED|REJECTED' research_notes/rh_goals_2026-08-14/lane_g/{KF_WALL_ATTACK_SOL,HOLOMORPHY_GATE_SOL,R3_ROUTE_B_TRANSPORT_SOL}.md | head -n 40
```

Relevant output:

```text
$ git ls-tree -r HEAD -- engine/certify

$ rg --files research_notes/rh_goals_2026-08-14/lane_g | rg -i "(evaluator|winding|certif|finite.*q|q.*finite|detdcH|rate_measure)" | sort
research_notes/rh_goals_2026-08-14/lane_g/LAW_CERTIFIED_DEEPCOUNT_MULTI.md
research_notes/rh_goals_2026-08-14/lane_g/LAW_CERTIFIED_DEEPCOUNT_Q9.md
research_notes/rh_goals_2026-08-14/lane_g/LAW_RATE_MEASURE.md
research_notes/rh_goals_2026-08-14/lane_g/M1G_PREDICTION_WINDING_CERTS.md
research_notes/rh_goals_2026-08-14/lane_g/TB_BLOCK_CERTIFICATES.md
research_notes/rh_goals_2026-08-14/lane_g/TB_BLOCK_CERTIFICATES_RECEIPT.json
research_notes/rh_goals_2026-08-14/lane_g/TB_BLOCK_CERTIFICATES_V2.md
research_notes/rh_goals_2026-08-14/lane_g/TB_BLOCK_CERTIFICATES_V2_RECEIPT.json
research_notes/rh_goals_2026-08-14/lane_g/law_probes/certdc9_winding.py
research_notes/rh_goals_2026-08-14/lane_g/law_probes/certdcH_winding.py
research_notes/rh_goals_2026-08-14/lane_g/law_probes/certdcM_winding.py
research_notes/rh_goals_2026-08-14/lane_g/law_probes/rate_measure.py
research_notes/rh_goals_2026-08-14/lane_g/law_probes/certdcH_winding_q12_N32.json
research_notes/rh_goals_2026-08-14/lane_g/law_probes/certdcH_winding_q12_N36.json
research_notes/rh_goals_2026-08-14/lane_g/law_probes/certdcH_winding_q7_N20.json
research_notes/rh_goals_2026-08-14/lane_g/law_probes/certdcH_winding_q7_N24.json
research_notes/rh_goals_2026-08-14/lane_g/law_probes/certdcH_winding_q7_N28.json
research_notes/rh_goals_2026-08-14/lane_g/law_probes/certdcH_winding_q9_N24.json
research_notes/rh_goals_2026-08-14/lane_g/law_probes/certdcH_winding_q9_N28.json
research_notes/rh_goals_2026-08-14/lane_g/law_probes/certdcM_winding_q12_N20.json
research_notes/rh_goals_2026-08-14/lane_g/law_probes/certdcM_winding_q12_N24.json
research_notes/rh_goals_2026-08-14/lane_g/law_probes/certdcM_winding_q7_N16.json
research_notes/rh_goals_2026-08-14/lane_g/law_probes/certdcM_winding_q7_N20.json
research_notes/rh_goals_2026-08-14/lane_g/law_probes/rate_measure_data.json
research_notes/rh_goals_2026-08-14/lane_g/law_probes/rate_measure_run.log
research_notes/rh_goals_2026-08-14/lane_g/law_probes/rate_measure_run.py
research_notes/rh_goals_2026-08-14/lane_g/law_probes/rate_measure_validate.log
research_notes/rh_goals_2026-08-14/lane_g/law_probes/rate_measure_validate.py
research_notes/rh_goals_2026-08-14/lane_g/law_probes/rate_measure_validate_n40.log
research_notes/rh_goals_2026-08-14/lane_g/law_probes/rate_measure_validate_n40.py
```

The source-status lines that classify these artifacts are:

```text
KF_WALL_ATTACK_SOL.md:580:1. a true interval meromorphic-continuation evaluator for each finite q,
KF_WALL_ATTACK_SOL.md:680:| certified true-phi_q finite evaluator and winding block | **OPEN** |
HOLOMORPHY_GATE_SOL.md:103:stock_engine_q12_status=REJECTED
HOLOMORPHY_GATE_SOL.md:230:This is **NOT EVIDENCE** for a zero or pole of phi_12
HOLOMORPHY_GATE_SOL.md:575:| Direct per-q full-H_0 zero count | **PROVABLE BY COMPUTATION AFTER A NAMED BUILD** |
HOLOMORPHY_GATE_SOL.md:576:| Existing ... boxes close the gate | **FALSE** |
R3_ROUTE_B_TRANSPORT_SOL.md:778:This is finite mathematics once a certified meromorphic-continuation evaluator exists.
```

The omitted list entries are existing determinant/winding probes, not a true
scalar-`phi_q` evaluator. The exact missing item is therefore:

> For every finite integer index below the analytic onset (unless a separate
> covering theorem is supplied), build and independently certify a true scalar
> `phi_q` meromorphic-continuation evaluator, interval branch/derivative
> variation, denominator/pole clearance, and a Rouché or direct winding
> zero-minus-pole certificate. The source requires this finite block explicitly
> (`KF_WALL_ATTACK_SOL:577-595`; `R3_ROUTE_B_TRANSPORT_SOL:747-794`).

Therefore the strongest full-program verdict is
`OPEN / UNDEFINED`, not a claimed finite `q_0`. The q=12 surrogate timing and
the existing determinant boxes remain `NOT EVIDENCE`, as required by the
holomorphy audit (`HOLOMORPHY_GATE_SOL:157-236,552-576`).

## 8. Claim ledger

| claim | strongest safe status | receipt/scope |
|---|---|---|
| RATE-A on balanced/matched `Gamma_R^A`, exponent `6/5`, onset `12`, advertised `C_R` | **CONFIRMED at paper level; not machine-verified** | `BOUNDARY_ALPHA_THEOREM_SOL:689-730`; `AM_REFEREE.md:371-408` |
| A0 geometric floors `m_z>=0.0439`, `nu_z>=0.1552` | **PROVED, Arb interval cover** | `R3_TRANSPORT_EXECUTION_SOL:58-66,237-252` |
| A0 safe side constant `K_+=117` | **CONFIRMED conditional source input** | `KF_WALL_REFEREE.md:27-31,211-240,409-414` |
| strict side onset for `C_R q^(-alpha) < K_+` | **PROVED conditional on paper-level RATE input** | complete Arb stdout in Section 4; `q_side=134010166814705707171424895246` |
| fixed-envelope exponent `alpha*nu=582/3125=0.18624` | **PROVED elementary** | equations (3.1)--(3.3), fresh Arb replay in Section 4 |
| whole-tail monotonicity of `U` | **PROVED** | derivative (3.3); no claim about `E_R` monotonicity |
| strict A0 integer and minimality | **PROVED conditional on paper-level RATE/A0 inputs** | complete Arb stdout in Section 4 |
| `q_pole=q_divisor=3` for the stated trivial scalar right domains | **PROVED from printed theory** | `HOLOMORPHY_GATE_SOL:254-264,363-389` |
| `K_F=109` paired with old `d_*>0.6603` | **REFUTED as a single ledger combination** | domain correction in Section 6; `KF_WALL_REFEREE.md:375-390` |
| finite below-tail scalar evaluator/winding block | **OPEN** | scoped inventory and source statuses in Section 7 |
| full all-q R5 closure | **OPEN / UNDEFINED** | finite-base item remains missing; no surrogate promotion |
| `q_{0,\mathrm{analytic}}` in (0.2) | **paper-level conditional analytic-tail threshold** | all terms sourced in Section 5; not full all-q closure |

## 9. Handoff boundary

This deliverable closes the selected A0 envelope arithmetic and its whole-tail
monotonicity at paper level. It does not promote machine formalization,
full-operator numerics, or finite-base coverage. The next cold referee must
re-run the complete Arb program in Section 4 and independently check the
domain correction and the scoped finite-evaluator inventory before any status
is banked.
