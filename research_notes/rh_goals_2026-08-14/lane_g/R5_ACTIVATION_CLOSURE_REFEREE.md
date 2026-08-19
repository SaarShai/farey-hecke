# CONFIRMED

**Scope:** cold adversarial referee of `R5_ACTIVATION_CLOSURE_SOL.md`.

**Verdict:** **CONFIRMED at paper level, conditional on the explicitly cited
RATE-A, A0, side-bound, and printed-theory inputs; not machine-verified.** The
selected A0 arithmetic and whole-tail upper-envelope argument survive the
required attacks. This does **not** close the finite block below the analytic
onset, and it does **not** promote the actual error function `E_R` to a
monotone function. The full all-q R5 program remains **OPEN / UNDEFINED**.

The target was read at the required source hash:

```text
$ shasum -a 256 research_notes/rh_goals_2026-08-14/lane_g/R5_ACTIVATION_CLOSURE_SOL.md
3b49d73d56cf963703137a6494f1f733fbb208d36c0afbe1affbd5d700ab2a53  research_notes/rh_goals_2026-08-14/lane_g/R5_ACTIVATION_CLOSURE_SOL.md
```

## 1. Scope and hypotheses

The first-zero A0 domain is exactly the one used in the source transport
lemma: `t_0=gamma_1/2`, `Omega={1/2<Re s<11/10, |Im s-t_0|<1/2}`, and
`Gamma_R={11/10+it: |t-t_0|<=1/2}`. The source receipt gives
`m_z>=0.0439` and `nu_z>=0.1552` on this fixed contour
(`R3_TRANSPORT_EXECUTION_SOL.md:20-66`). The source implication consumes
`K_+` on the other three sides and requires `0<E_R<=K_+`
(`R3_TRANSPORT_EXECUTION_SOL.md:68-93`).

The selected constants and their source locations are:

```text
$ nl -ba research_notes/rh_goals_2026-08-14/lane_g/R3_TRANSPORT_EXECUTION_SOL.md | sed -n '38,97p;237,252p'
    38  Choose
    41   delta=1/2, r_z=1/8
    48   Omega={s:1/2<Re s<11/10, |Im s-t_0|<1/2}
    55   Gamma_R={11/10+it: |t-t_0|<=1/2}
    61   m_z:=min_{partial D_z}|phi_infty(s)|>=0.0439
    64   nu_z:=inf_{partial D_z} omega(s,Gamma_R;Omega)>=0.1552
    75  and let K_+ be a bound for |F_q| on the other three sides of
    76  partial Omega. If both scattering functions are holomorphic on
    77  overline{Omega} and 0<E_R(q)<=K_+, then the two-constants theorem gives
   244  | `m_z` | `min_{partial D_z}|phi_infty| >= 0.0439` | **PROVED**, Arb interval cover |
   245  | `nu_z` | `inf_{partial D_z} omega(s,Gamma_R;Omega) >= 0.1552` | **PROVED**, Arb/Fourier interval cover |
   247  | `C_R, alpha, q_RATE` | `(R2*)` constants on the whole right side | **CONJECTURAL / MISSING** |
   250  | `K_+` | non-RATE-boundary bound for `|F_q|` | **CONJECTURAL / MISSING family-uniformly** |
```

The last two historical rows are superseded only by the later dated RATE-A
promotion and side-wall reports, not silently erased. The current RATE-A
promotion states the exact matched boundary, `alpha=6/5`, `q_RATE=12`, and
the unchanged upward `C_R`, while retaining paper-level/not-machine-verified
scope (`BOUNDARY_ALPHA_THEOREM_SOL.md:689-734`; `AM_REFEREE.md:7,371-408`).
The independent RATE referee confirms that `q_RATE=12` comes from the
analytic absorption at `F(12)=7940`, not a finite fit
(`RATE_A_REFEREE.md:308-324`).

The current A0 side-wall report confirms that the bound controls the same
`K_+` quantity and gives the safe ledger choice `K_+=117`, conditional on the
full-width `H_0` and the stated holomorphy/anchor gates
(`KF_WALL_REFEREE.md:17-44,211-246,408-420`). Thus the safe status is
`K_+=117` as a **conditional source input**, not an unconditional theorem
about every possible domain.

The printed-theory holomorphy report supplies the finite-index threshold for
the trivial scalar coefficient:

```text
$ nl -ba research_notes/rh_goals_2026-08-14/lane_g/HOLOMORPHY_GATE_SOL.md | sed -n '254,264p;363,390p'
   256  The finite-Hecke **pole/holomorphy gate is provable from the printed theory and
   257  closes with `q_pole = q_divisor = 3`** for the trivial scalar scattering
   260  nonvanishing gate is **FALSE**: Hejhal Theorem 7.11 says that the full rectangle
   261  eventually contains a zero. The corrected proof is a dichotomy: a zero closes
   262  the target immediately; otherwise nonvanishing is the contradiction hypothesis
   263  under which the `K_F` harmonic argument runs.
   373  > **Finite-Hecke holomorphy theorem.** For every finite Hecke index `q>=3`,
   374  > `phi_q` is holomorphic on an open neighborhood of the full `H_0`, of the
   375  > A0 domain `overline{Omega}`, of `D_z`, and of the old Route-B right domains.
   379  > `q_pole=q_divisor=3`.
   385  For the rebuilt disc `D_0`, its right half lies inside full `H_0`; under
   386  `H_0(q)`, the meromorphic scattering identity (7.22) maps any left-half pole
   387  to a right-half zero, so nonvanishing transfers to pole-freeness on the
   388  reflected left half. Hence no extra `q_divisor` activation is needed in that
   389  contradiction branch.
   389  Hence no extra q_divisor activation is needed in that contradiction branch.
```

This nonzero/zero case split is preserved. No family-wide nonvanishing claim
is used.

## 2. Monotonicity attack

The target defines only

`U(q)=K_+^(1-nu) C_R^nu q^(-alpha nu)`.

The rational check was rerun independently:

```text
$ /usr/bin/python3 - <<'PY'
from fractions import Fraction
alpha=Fraction(6,5); nu=Fraction(97,625); beta=alpha*nu
print('nu=',nu,'alpha_nu=',beta,'decimal=',float(beta),'positive=',beta>0)
print('derivative_sign=', '-' if beta>0 else '+')
PY
nu= 97/625 alpha_nu= 582/3125 decimal= 0.18624 positive= True
derivative_sign= -
```

Therefore `U'(q)=-beta*K_+^(1-nu)*C_R^nu*q^(-beta-1)<0` for every real
`q>0`, because all other factors are positive. The target uses this only to
carry a strict bound from one integer to the tail; it never asserts
`E_R'(q)<0` or monotonicity of `E_R`. This is the correct monotonicity gate.

## 3. Verbatim Arb replay and strict arithmetic

The complete embedded program in the target (lines 215--274) was executed
verbatim with the target's extraction command:

```text
$ (cd /Users/za/Documents/farey-hecke/.worktrees/rate-activation-referee-20260819 && \
    sed -n '215,274p' research_notes/rh_goals_2026-08-14/lane_g/R5_ACTIVATION_CLOSURE_SOL.md | bash)
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

The same-floor checks establish the strict-integer rules
`q_side=floor(exp(T_side))+1` and `q_transport=floor(exp(T))+1`; the two
minimality lines for each threshold establish the lower strict inequality and
the predecessor non-strict inequality. The endpoint values are not rounded
displays used as inputs.

An independent Arb expression, using exact rational construction of `nu` and
`m`, was also run:

```text
$ PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import arb, ctx
ctx.dps=160
a=arb(6)/5; v=arb(97)/625; m=arb(439)/10000
K=arb(117); C=arb(10489412368759562746433608215977724802)
qs=arb(134010166814705707171424895246)
qt=arb(332093267419812025416641789732742045430624465595)
Ts=(C.log()-K.log())/a
T=((1-v)*K.log()-m.log())/(a*v)+C.log()/a
print('independent_beta=',a*v)
print('side_lower_strict=',bool(qs.log()>Ts),'side_prev_non_strict=',bool((qs-1).log()<=Ts))
print('transport_lower_strict=',bool(qt.log()>T),'transport_prev_non_strict=',bool((qt-1).log()<=T))
print('side_eval_lt_117=',bool(C*qs**(-a)<K))
print('transport_mix_lt_m=',bool(K**(1-v)*(C*qt**(-a))**v<m))
print('transport_q_gt_side=',bool(qt>qs))
PY
independent_beta= [0.1862400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 +/- 1.22e-161]
side_lower_strict= True side_prev_non_strict= True
transport_lower_strict= True transport_prev_non_strict= True
side_eval_lt_117= True
transport_mix_lt_m= True
transport_q_gt_side= True
```

The exact integer max was checked independently:

```text
$ /usr/bin/python3 - <<'PY'
qs=[12,3,134010166814705707171424895246,332093267419812025416641789732742045430624465595]
print('max=',max(qs))
print('max_matches_transport=',max(qs)==qs[-1])
print('strict_side_lt_transport=',qs[2]<qs[3])
PY
max= 332093267419812025416641789732742045430624465595
max_matches_transport= True
strict_side_lt_transport= True
```

Thus the target's literal analytic ledger is arithmetically correct:

`q_analytic=max{12,3,134010166814705707171424895246,332093267419812025416641789732742045430624465595}`

equals the displayed `q_transport`. The side threshold is included rather
than hidden, and the strict predecessor tests pass.

## 4. Onset ledger and conditional status

The source RATE theorem is on the balanced/matched first-zero boundary and
holds for integer `q>=12` with `C_R` and exponent `6/5`; its promotion retains
the paper-level and not-machine-verified qualification
(`BOUNDARY_ALPHA_THEOREM_SOL.md:689-734`; `AM_REFEREE.md:371-408`).
The divisor/pole term `q_divisor=3` is from printed theory for the stated
trivial scalar right domains (`HOLOMORPHY_GATE_SOL.md:363-389`). The A0
geometry (`m_z`, `nu_z`, fixed contour) is q-independent, so there is no
invented `q_geometry`; envelope monotonicity is a real-`q` analytic PASS, so
there is no invented `q_monotone`. The side threshold is the actual integer
term and is dominated by `q_transport` by the receipts above.

The safe result is therefore a **paper-level conditional analytic-tail
threshold**. It is conditional on the source premises named above, including
the A0 side bound and the paper-level RATE-A theorem. It is not an unconditional
all-q theorem, a machine/formal certificate, or a claim that all finite
indices below this integer have been checked.

## 5. Domain-collision attack

The claimed pairing `K_F=109` with the old first-zero `d_*>0.6603` is correctly
rejected as one ledger combination. The ownership receipts are:

```text
$ nl -ba research_notes/rh_goals_2026-08-14/lane_g/KF_WALL_REFEREE.md | sed -n '373,390p'
   375  CONFIRMED; no hidden mixing inside either chain.
   377  A0 uses the first-zero contour t_0=gamma_1/2, the Rouché margin
   378  m_z>0.0439, and harmonic-measure floor nu_z>0.1552
   379  (R3_TRANSPORT_EXECUTION_SOL.md:38-97). It consumes neither
   380  d_*>0.6603 nor d_*>0.3186.
   381  The rebuilt Route B uses the sixth-zero shift
   382  t_c=t_6-0.050005, delta=0.9999, target segment
   383  [t_6-0.1,t_6-0.00001], and d_*>0.3186
   384  (C0_TRANSPORT_CAMPAIGN_SOL.md:461-485,680-685,819-825).
   385  The old d_*>0.6603 belongs to the first-zero Route-B window
   386  (R3_ROUTE_B_TRANSPORT_SOL.md:526-549) and is not used in the new
   387  5599.981 calculation.
   389  The only mixing is in the headline comparison between the old Route-B
   390  threshold and the new A0 threshold, already flagged as not like-for-like.
$ rg -n '0\.3186|0\.6603|sixth-zero|first-zero|t_c=t_6' \
  research_notes/rh_goals_2026-08-14/lane_g/C0_TRANSPORT_CAMPAIGN_SOL.md \
  research_notes/rh_goals_2026-08-14/lane_g/R3_ROUTE_B_TRANSPORT_SOL.md \
  research_notes/rh_goals_2026-08-14/lane_g/KF_WALL_ATTACK_SOL.md | head -n 12
research_notes/rh_goals_2026-08-14/lane_g/C0_TRANSPORT_CAMPAIGN_SOL.md:52:log K_F<5259, B_0<4905.067, d_*>0.3186.
research_notes/rh_goals_2026-08-14/lane_g/C0_TRANSPORT_CAMPAIGN_SOL.md:465:defect_lower=0.31863235495984554290771484375 worst_cell=0
research_notes/rh_goals_2026-08-14/lane_g/C0_TRANSPORT_CAMPAIGN_SOL.md:468:We use d_*>0.3186.
research_notes/rh_goals_2026-08-14/lane_g/C0_TRANSPORT_CAMPAIGN_SOL.md:472:t_c=t_6-0.050005.
research_notes/rh_goals_2026-08-14/lane_g/R3_ROUTE_B_TRANSPORT_SOL.md:533: d_*:=\\inf(1-|\\phi_\\infty|)>0.6603.                        \\tag{8.2}
research_notes/rh_goals_2026-08-14/lane_g/KF_WALL_ATTACK_SOL.md:221:At the relocated sixth-zero rectangle,
research_notes/rh_goals_2026-08-14/lane_g/KF_WALL_ATTACK_SOL.md:224:t_c=t_6-0.050005, delta=0.9999,
```

The selected A0 formula contains only `K_+=117`, `m_z`, and `nu_z`; it does
not consume either defect or `K_F`. The separate sixth-zero wall owns the
safe `K_F=109` and `d_*>0.3186`, while the old first-zero Route-B window owns
`d_*>0.6603`. This is a domain correction, not a refutation of either
conditional source implication.

## 6. Finite-base attack

The scoped inventory was rerun from the activation referee worktree:

```text
$ git ls-tree -r HEAD -- engine/certify
[no output]
$ rg --files research_notes/rh_goals_2026-08-14/lane_g | rg -i '(evaluator|winding|certif|finite.*q|q.*finite|detdcH|rate_measure)' | sort
research_notes/rh_goals_2026-08-14/lane_g/LAW_CERTIFIED_DEEPCOUNT_MULTI.md
research_notes/rh_goals_2026-08-14/lane_g/LAW_CERTIFIED_DEEPCOUNT_Q9.md
research_notes/rh_goals_2026-08-14/lane_g/LAW_RATE_MEASURE.md
research_notes/rh_goals_2026-08-14/lane_g/M1G_PREDICTION_WINDING_CERTS.md
research_notes/rh_goals_2026-08-14/lane_g/TB_BLOCK_CERTIFICATES.md
research_notes/rh_goals_2026-08-14/lane_g/TB_BLOCK_CERTIFICATES_RECEIPT.json
research_notes/rh_goals_2026-08-14/lane_g/TB_BLOCK_CERTIFICATES_V2.md
research_notes/rh_goals_2026-08-14/lane_g/TB_BLOCK_CERTIFICATES_V2_RECEIPT.json
research_notes/rh_goals_2026-08-14/lane_g/law_probes/certdc9_winding.py
research_notes/rh_goals_2026-08-14/lane_g/law_probes/certdc9_winding_q9_N16.json
research_notes/rh_goals_2026-08-14/lane_g/law_probes/certdc9_winding_q9_N20.json
research_notes/rh_goals_2026-08-14/lane_g/law_probes/certdcH_winding.py
research_notes/rh_goals_2026-08-14/lane_g/law_probes/certdcH_winding_q12_N32.json
research_notes/rh_goals_2026-08-14/lane_g/law_probes/certdcH_winding_q12_N36.json
research_notes/rh_goals_2026-08-14/lane_g/law_probes/certdcH_winding_q7_N20.json
research_notes/rh_goals_2026-08-14/lane_g/law_probes/certdcH_winding_q7_N24.json
research_notes/rh_goals_2026-08-14/lane_g/law_probes/certdcH_winding_q7_N28.json
research_notes/rh_goals_2026-08-14/lane_g/law_probes/certdcH_winding_q9_N24.json
research_notes/rh_goals_2026-08-14/lane_g/law_probes/certdcH_winding_q9_N28.json
research_notes/rh_goals_2026-08-14/lane_g/law_probes/certdcM_winding.py
research_notes/rh_goals_2026-08-14/lane_g/law_probes/certdcM_winding_q12_N20.json
research_notes/rh_goals_2026-08-14/lane_g/law_probes/certdcM_winding_q12_N24.json
research_notes/rh_goals_2026-08-14/lane_g/law_probes/certdcM_winding_q7_N16.json
research_notes/rh_goals_2026-08-14/lane_g/law_probes/certdcM_winding_q7_N20.json
research_notes/rh_goals_2026-08-14/lane_g/law_probes/rate_measure.py
research_notes/rh_goals_2026-08-14/lane_g/law_probes/rate_measure_data.json
research_notes/rh_goals_2026-08-14/lane_g/law_probes/rate_measure_run.py
research_notes/rh_goals_2026-08-14/lane_g/law_probes/rate_measure_validate.py
research_notes/rh_goals_2026-08-14/lane_g/law_probes/rate_measure_validate_n40.py
$ rg -n -i 'true.*phi|finite.*evaluator|certified.*winding|dimension tail|NOT EVIDENCE|SCOUT_FAILED|REJECTED' \
  research_notes/rh_goals_2026-08-14/lane_g/{KF_WALL_ATTACK_SOL,HOLOMORPHY_GATE_SOL,R3_ROUTE_B_TRANSPORT_SOL}.md | head -n 40
research_notes/rh_goals_2026-08-14/lane_g/KF_WALL_ATTACK_SOL.md:580:1. a true interval meromorphic-continuation evaluator for each finite q,
research_notes/rh_goals_2026-08-14/lane_g/KF_WALL_ATTACK_SOL.md:680:| certified true-phi_q finite evaluator and winding block | **OPEN** |
research_notes/rh_goals_2026-08-14/lane_g/HOLOMORPHY_GATE_SOL.md:103:stock_engine_q12_status=REJECTED
research_notes/rh_goals_2026-08-14/lane_g/HOLOMORPHY_GATE_SOL.md:230:This is **NOT EVIDENCE** for a zero or pole of phi_12
research_notes/rh_goals_2026-08-14/lane_g/HOLOMORPHY_GATE_SOL.md:575:| Direct per-q full-H_0 zero count | **PROVABLE BY COMPUTATION AFTER A NAMED BUILD** |
research_notes/rh_goals_2026-08-14/lane_g/HOLOMORPHY_GATE_SOL.md:576:| Existing `hecke_transfer_operator_zero` / R3B boxes close the gate | **FALSE** |
research_notes/rh_goals_2026-08-14/lane_g/R3_ROUTE_B_TRANSPORT_SOL.md:778:This is finite mathematics once a certified meromorphic-continuation evaluator exists.
research_notes/rh_goals_2026-08-14/lane_g/R3_ROUTE_B_TRANSPORT_SOL.md:778:This is finite mathematics once a certified meromorphic-continuation evaluator exists.
```

The inventory is not a claim that no code exists anywhere. It establishes the
relevant source status: existing determinant/winding artifacts are not a true
scalar-`phi_q` evaluator with a proved continuation tail, denominator/pole
clearance, segment variation, and zero-minus-pole winding certificate. The
source explicitly lists those as prerequisites
(`KF_WALL_ATTACK_SOL.md:577-594`; `R3_ROUTE_B_TRANSPORT_SOL.md:747-794`) and
labels current surrogates `NOT EVIDENCE`
(`HOLOMORPHY_GATE_SOL.md:220-236,552-580`).

Accordingly, naming `q_analytic` is valid as a conditional analytic-tail
onset, but the all-q pincer and every finite index below it remain
**OPEN / UNDEFINED**. No finite timing, determinant, or winding surrogate was
promoted.

## 7. Final claim ledger

| audited claim | referee verdict | reason |
|---|---|---|
| A0 contour and `m_z>=.0439`, `nu_z>=.1552` | CONFIRMED source-conditional | `R3_TRANSPORT_EXECUTION_SOL.md:20-93,237-252` |
| RATE-A scope, `alpha=6/5`, `C_R`, `q_RATE=12` | CONFIRMED at paper level; not machine-verified | `BOUNDARY_ALPHA_THEOREM_SOL.md:689-734`; `RATE_A_REFEREE.md:308-324`; `AM_REFEREE.md:371-408` |
| `K_+=117` for the selected A0 quantity | CONFIRMED conditional source input | `KF_WALL_REFEREE.md:211-246,408-420` |
| fixed-envelope decrease | CONFIRMED elementary | rational receipt and derivative in §2 |
| strict side threshold and minimality | CONFIRMED conditional | verbatim Arb and independent Arb receipts in §3 |
| strict A0 threshold and minimality | CONFIRMED conditional | verbatim Arb and independent Arb receipts in §3 |
| `q_divisor=3` | CONFIRMED from printed theory for stated trivial scalar domains | `HOLOMORPHY_GATE_SOL.md:254-264,363-389` |
| `K_F=109` paired with old `d_*>.6603` | REFUTED as a single domain combination | §5 source ownership receipts |
| true finite scalar evaluator/winding block | OPEN | §6 inventory and source statuses |
| conditional analytic-tail `q_analytic` | CONFIRMED at paper-level input scope | sourced max plus strict receipts; not all-q closure |
| full all-q R5 closure | OPEN / UNDEFINED | finite block remains missing |

## 8. Referee conclusion

The target survives all required negative tests. No rounded display was
exponentiated; `q_side` is included and is the minimal strict integer; the
selected A0 chain does not consume `K_F` or either defect; the finite
determinant/winding artifacts remain `NOT EVIDENCE`; and RATE-A is not
upgraded to machine verification. Bank only the conditional paper-level
analytic-tail result, with the finite-base and machine/formal caveats above.

LANE REPORT
Status: done
Files changed: /Users/za/Documents/farey-hecke/.worktrees/rate-activation-referee-20260819/research_notes/rh_goals_2026-08-14/lane_g/R5_ACTIVATION_CLOSURE_REFEREE.md
Verification receipts: target SHA-256 matched 3b49d73d56cf963703137a6494f1f733fbb208d36c0afbe1affbd5d700ab2a53; verbatim embedded Arb replay returned same floors, strict minimality, `q_side_lt_q_transport=True`, and `A0_strict_lt_m=True`; independent rational check returned `582/3125`, positive derivative coefficient; independent Arb returned all four strict inequalities `True`; exact max returned `max_matches_transport=True`; finite inventory returned no tracked `engine/certify` and source `OPEN`/`NOT EVIDENCE` statuses; `git diff --check` and `git status` recorded below.
Result: CONFIRMED at paper level, conditional on cited RATE-A/A0/side/holomorphy inputs; not machine-verified; full all-q closure remains OPEN / UNDEFINED.
Open: build and independently certify the true scalar-`phi_q` finite evaluator, continuation/pole clearance, and winding or Rouché certificates for the finite block below the analytic onset; machine/formal verification also remains open.

## 9. Final file-state receipts

```text
$ git diff --check
[no output]
$ git status --short --branch
## codex/rate-activation-referee-20260819
?? research_notes/rh_goals_2026-08-14/lane_g/R5_ACTIVATION_CLOSURE_REFEREE.md
```
