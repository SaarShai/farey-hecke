# Q8 / q-generic certification lane — progress and obstruction

**Date:** 2026-08-19
**Scope:** Route A (q=8 continuous certification) and the proposed moving-
`lambda` shortcut.  This note is a progress artifact, not a promotion.  Any
statement that would identify a finite determinant zero with a Selberg zero is
**CONJECTURAL** until the missing Fredholm-tail, E1, `K_s`, and MMS
factorization links are separately closed and cold-refereed.

## Verdict

The old q=8 certificate remains refuted.  The endpoint-only gate and observed-
ratio dimension tail are not proof devices.  A new q=8 derivative engine and a
closed-subarc Jacobi/Taylor runner now exist and pass finite-section smoke
tests.  A q=8 weight envelope and R2 column envelope were also re-derived at
Arb precision.  They do **not** close the theorem: the R2 tail is far too large
at the N values used by the old q=8 run, and the analytic linkage is explicitly
`UNPROVEN`.

The moving-`lambda` shortcut does not remove the obstruction.  The MMS block
dimension and block combinatorics change with `q`; there is no fixed operator
family on the whole interval `[lambda_8,2)` to which one continuous Rouché
certificate could apply.

## 1. Old false gates reproduced

The prior q=8 referee found two independent logical failures.  The following
fresh command reproduces the countermodels without touching the repository:

```text
$ /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from fractions import Fraction
A=(Fraction(1,4),Fraction(0)); B=A
print('OLD_ENDPOINT_COUNTERMODEL', 'f(0)=f(1)=1/4', 'interior f(1/2)=0', 'Re(B*conj(A))=1/16>0', 'accepted=True')
inc=[1.0,.5,.25,.125,100.0]
print('OLD_TAIL_COUNTERMODEL', 'observed_ratios=',[inc[i+1]/inc[i] for i in range(3)], 'q_obs=0.5', 'estimated_tail=0.125', 'next_increment=100.0', 'bound_violated=True')
PY
OLD_ENDPOINT_COUNTERMODEL f(0)=f(1)=1/4 interior f(1/2)=0 Re(B*conj(A))=1/16>0 accepted=True
OLD_TAIL_COUNTERMODEL observed_ratios= [0.5, 0.5, 0.5] q_obs=0.5 estimated_tail=0.125 next_increment=100.0 bound_violated=True
```

The source-level referee receipt remains the controlling correction:
[F8_R3B_REFUTATION_REFEREE.md](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_f/F8_R3B_REFUTATION_REFEREE.md:1).
The historical q=8 JSON labels are therefore retained as finite sampled
evidence only; they are not silently upgraded here.

## 2. Exact even-q MMS-(32) binding

The q=8 operator is the even-q `h_8=kappa_8=3` assembly.  The exact eight
source blocks are recorded by the live source module:

```text
$ /Users/za/.venvs/farey-rh/bin/python - <<'PY'
import sys
sys.path.insert(0,'research_notes/rh_goals_2026-08-14/lane_f')
import f8_certify_tb_blocks as f8
print('Q8_BLOCKS',len(f8.BLOCKS),f8.BLOCKS)
PY
Q8_BLOCKS 8 [(1, 3, 2, False, True), (1, 3, 1, True, True),
(2, 1, 1, False, False), (2, 3, 2, False, True),
(2, 3, 1, True, True), (3, 2, 1, False, False),
(3, 3, 2, False, True), (3, 3, 1, True, True)]
```

`q8_r3b_engine.py` binds these blocks to the q-independent Acb s-jet
primitives from the q=5 R3b engine.  The only new mathematical content is the
explicit even-q assembly; the values and s-derivatives are independently
checked by the finite Taylor runner.  This is **AWAITING COLD REFEREE** and is
not banked as a theorem.

## 3. Continuous finite-section Taylor/Jacobi enclosure

`q8_finite_taylor_probe.py` replaces the refuted endpoint test by a genuine
closed-subarc enclosure for `det(I-M_N(s))`: a midpoint inverse, Acb derivative
box, Neumann preconditioner, Jacobi trace bound, and adaptive bisection.  The
N=8 smoke run was:

```text
$ /Users/za/.venvs/farey-rh/bin/python research_notes/rh_goals_2026-08-14/lane_f/q8_finite_taylor_probe.py --N 8 --K 1
Q8_FINITE_TAYLOR arc=1/4 edge=bottom rH=[0.0066286784401232881 +/- ...] lower=[0.0004716658360109988 +/- ...]
Q8_FINITE_TAYLOR arc=2/4 edge=right  rH=[0.0065806760146270574 +/- ...] lower=[0.0004750649148415108 +/- ...]
Q8_FINITE_TAYLOR arc=3/4 edge=top    rH=[0.0065425781994382621 +/- ...] lower=[0.0004775852757957901 +/- ...]
Q8_FINITE_TAYLOR arc=4/4 edge=left   rH=[0.0065900123665778859 +/- ...] lower=[0.0004741862293978942 +/- ...]
{
  "status": "FINITE_SECTION_ONLY",
  "all_finite_taylor_exclude_zero": true,
  "max_neumann_q_upper": "[0.8216380513827480 +/- ...]",
  "max_rH_upper": "[0.0066286784401232881 +/- ...]",
  "finite_section_winding": 0,
  "fredholm_tail": "OPEN: no theorem-valid R2 tail bound was supplied"
}
```

The winding `0` in this low-N smoke run is not a refutation of the target
zero: it is only a finite-section control with too little truncation
resolution.  The run demonstrates that the interior-continuity mechanism is
available while preserving the precise scope boundary.

## 4. q=8 W envelope and R2 result

The q=8 W envelope was recomputed from the eight q=8 TB rows using the
q-independent Hurwitz-closed weight majorants.  Receipt:
[Q8_W_ENVELOPE_RECEIPT.json](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_f/f8_receipts/Q8_W_ENVELOPE_RECEIPT.json).

```text
$ /Users/za/.venvs/farey-rh/bin/python research_notes/rh_goals_2026-08-14/lane_f/q8_weight_envelope.py
Q8_W block=3→3, −1, tail W_ge1=[2.8930614752527543 +/- ...]
{
  "status": "WEIGHT_ENVELOPE_CERTIFIED_R2_PENDING",
  "W_ge1_upper_bound": "[9.8736526508131028 +/- ...]",
  "W0_upper_bound": "[9.7854017469164507 +/- ...]",
  "F_upper_bound": "[3.3935237709075591e+140 +/- ...]"
}
```

The R2 adapter then ran at the full `M=512`, 384-bit production resolution.
The output is a valid R2 column-envelope receipt, but it correctly keeps the
analytic linkage open:

```text
$ /Users/za/.venvs/farey-rh/bin/python research_notes/rh_goals_2026-08-14/lane_f/q8_certify_r2_flagship.py --M 512 --K-head 16 --precision 384 --N-targets 64 80
[ 1/19] 1→3, +2, tail tail
[ 8/19] 3→3, −1, tail tail
{'status': 'CERTIFIED', 'verdict': 'R2_COLUMN_ENVELOPE_CERTIFIED_R3_PENDING',
 'T_tail': {'64': '[11.7018980999093182 +/- ...]',
            '80': '[2.7519594995047667 +/- ...]'},
 'B_total': '[1024.4002498091004 +/- ...]'}
```

The receipt itself reports `analytic_linkage.status = UNPROVEN`.  In
particular, `T_tail(80)` is still an upper bound of more than `2.75`, while the
old q=8 contour determinant lower margin was of order `10^-6`.  The exponential
R2/R3 correction factor using `B_total` is correspondingly unusable at these
N values.  This is a quantitative geometry/majorant obstruction, not a
successful q=8 theorem.

The q=8 smoke R2 run at `M=64`, `K_head=4`, 256 bits independently returned
`T_tail(32) = [197.84269799 +/- ...]` and `T_tail(40) = [102.01363060 +/- ...]`;
the production run therefore genuinely improves with resolution and N but
does not close the gap.

## 5. Moving-`lambda` / q-generic shortcut audit

The proposed interval certificate over `lambda in [lambda_8,2)` cannot use a
single fixed MMS operator.  The source formulas make the obstruction exact:

```text
$ /Users/za/.venvs/farey-rh/bin/python - <<'PY'
for q in (8,10,12,14,16):
 h=(q-2)//2
 print('EVEN',q,'h=',h,'kappa=',h,'add_columns_calls=',2+3*(h-1))
for q in (7,9,11,13,15):
 h=(q-3)//2; k=2*h+1
 print('ODD',q,'h=',h,'kappa=',k,'add_columns_calls=',4+4*(k-2))
print('LAMBDA_INTERVAL_OBSTRUCTION', 'q=8 lambda=',1.8477590650,
      'q->infty lambda->2', 'even kappa=(q-2)/2 unbounded',
      'odd kappa=q-2 unbounded')
PY
EVEN 8 h= 3 kappa= 3 add_columns_calls= 8
EVEN 10 h= 4 kappa= 4 add_columns_calls= 11
EVEN 12 h= 5 kappa= 5 add_columns_calls= 14
EVEN 14 h= 6 kappa= 6 add_columns_calls= 17
EVEN 16 h= 7 kappa= 7 add_columns_calls= 20
ODD 7 h= 2 kappa= 5 add_columns_calls= 16
ODD 9 h= 3 kappa= 7 add_columns_calls= 24
ODD 11 h= 4 kappa= 9 add_columns_calls= 32
ODD 13 h= 5 kappa= 11 add_columns_calls= 40
ODD 15 h= 6 kappa= 13 add_columns_calls= 48
LAMBDA_INTERVAL_OBSTRUCTION q=8 lambda= 1.8477590650 q->infty lambda->2 even kappa=(q-2)/2 unbounded odd kappa=q-2 unbounded
```

The underlying source confirms the same formulas: even `q` uses `kappa=h_q`
and MMS-(32), odd `q` uses `kappa=2h_q+1` and MMS-(34), with different
single/tail landing columns.  A fixed-`kappa` interval slab can at most cover
the continuous deformation of one fixed combinatorial model; it cannot cover
all integers q as `kappa` grows without bound.  A valid q-generic route would
therefore require a new uniform infinite-dimensional operator theorem, not a
finite interval rerun of the q=8 matrix.

## 6. Remaining gates

1. **R2 theorem tail — OPEN.** Supply an a-priori, theorem-valid Fredholm
   dimension-tail bound, or redesign the q=8 disc/majorant geometry so the
   certified `F_R` correction is below the continuous determinant margin.
2. **Full q=8 continuous contour — AWAITING R2.** The finite Taylor machinery
   is present, but no full determinant winding may be claimed while gate 1 is
   open.
3. **E1 enlarged-disc contraction — OPEN.** No q=8 E1 receipt has been made.
4. **`K_s` nonvanishing — OPEN.** No q=8 closed-box product/lattice receipt has
   been made.
5. **Common continuation/factorization — OPEN.** No q=8 cold-reviewed bridge
   from the selected determinant to the Selberg zeta/resonance has been
   banked.
6. **q-generic interval shortcut — REFUTED AS A SUFFICIENT FINITE-DIMENSION
   STRATEGY.** The obstruction is changing, unbounded block dimension, not an
   interval arithmetic precision issue.

No Kaggle run was launched: the local full-Fredholm runner is not theorem-valid
until gate 1 is supplied, so a remote same-byte execution would be **NOT
EVIDENCE** for the missing theorem.

## Artifacts and verification

- `q8_r3b_engine.py` — explicit MMS-(32) value/derivative assembly.
- `q8_finite_taylor_probe.py` — adaptive closed-subarc finite-section Taylor
  enclosure.
- `q8_weight_envelope.py` and `f8_receipts/Q8_W_ENVELOPE_RECEIPT.json` — q=8
  W-envelope replay.
- `q8_certify_r2_flagship.py`, `Q8_R2_FLAGSHIP_CERT.md`, and
  `f8_receipts/Q8_R2_FLAGSHIP_RECEIPT.json` — production-resolution R2 output.

Validation commands:

```text
$ /Users/za/.venvs/farey-rh/bin/python -m py_compile q8_r3b_engine.py q8_finite_taylor_probe.py q8_weight_envelope.py q8_certify_r2_flagship.py
exit 0
$ git diff --check
exit 0
```

**Status:** all mathematical promotion claims in this note are **AWAITING
COLD REFEREE**.  The first remaining gap is the theorem-valid R2 dimension
tail / geometry closure.

## 7. Dated correction block — 2026-08-19

This block is appended rather than silently rewriting §§4–6.  It supersedes
the stale quantitative statement in §4 that the q=8 R2 tail was still of order
one at the production geometry.  The older `M=512`/`N=64,80` receipt remains
historical evidence; the branch-alone q8 replay below uses the corrected
`F1024` geometry and the endpoint `B_finite`, not the R2 column sum.

### 7.1 Branch-alone MMS-(32) and weight receipts

The exact q=8 block list remains the eight rows already quoted in §2.  The
source convention is, explicitly, (h_8=kappa_8=3), plus sector, with

```text
(L g)_1 = L_{∞,+2} g_3 + L_{∞,−1} g_3
(L g)_2 = L_{+1} g_1 + L_{∞,+2} g_3 + L_{∞,−1} g_3
(L g)_3 = L_{+1} g_2 + L_{∞,+2} g_3 + L_{∞,−1} g_3.
```

Here `L_{∞,+2}` denotes the `(+2)` Hurwitz-tail family, `L_{∞,−1}` the
`(−1)` family, and `L_{+1}` the finite head map.  The branch maps used by
the local value/derivative engine are

```text
theta_{+n}(z) = -1/(z+n*lambda),
theta_{-n}(z) =  1/(z-n*lambda),
weight_{s,n}(z) = (z +/- n*lambda)^(-2s)
```

with the principal branch on the certified discs.  This is an explicit
q=8 instantiation of MMS-(32), but its linkage to the full MMS operator is
still **AWAITING COLD REFEREE**.

The fresh F1024 run was:

```text
$ /Users/za/.venvs/farey-rh/bin/python research_notes/rh_goals_2026-08-14/lane_f/q8_candidate_tb_cert.py
Q8_F1024 block=1→3, +2, tail ratio=[0.570851832297562800275650 +/- 1.22e-25]
Q8_F1024 block=1→3, −1, tail ratio=[0.576254611223915512176277 +/- 3.11e-25]
Q8_F1024 block=2→1, +1, head ratio=[0.625846727889502138595173 +/- 4.58e-25]
Q8_F1024 block=2→3, +2, tail ratio=[0.569426095116476819149998 +/- 2.41e-25]
Q8_F1024 block=2→3, −1, tail ratio=[0.574605675865332427267373 +/- 3.60e-25]
Q8_F1024 block=3→2, +1, head ratio=[0.696590428020637535884545 +/- 2.54e-25]
Q8_F1024 block=3→3, +2, tail ratio=[0.568678204710670413876598 +/- 4.38e-25]
Q8_F1024 block=3→3, −1, tail ratio=[0.671604678146759859002060 +/- 3.67e-25]
{
  "rho_star_upper_bound": "[0.696590428020637535884545 +/- 2.55e-25]",
  "all_pole_clearances_pass": true,
  "all_branch_cut_clearances_pass": true,
  "runtime_seconds": 0.3524642500124173
}
```

The corresponding local W-envelope replay was:

```text
$ /Users/za/.venvs/farey-rh/bin/python research_notes/rh_goals_2026-08-14/lane_f/q8_weight_envelope.py
{
  "status": "WEIGHT_ENVELOPE_CERTIFIED_R2_PENDING",
  "W_ge1_upper_bound": "[9.87365265081310277462644 +/- 1.17e-23]",
  "W0_upper_bound": "[9.78540174691645069446512 +/- 4.02e-24]",
  "F_upper_bound": "[3.39352377090755906788005e+140 +/- 6.54e+119]",
  "runtime_seconds": 0.44813195799360983
}
```

The W output is an R2 majorant input, not a Fredholm determinant bound; the
large `F_upper_bound` is consequently not the corrected (F_R) below.

### 7.2 Corrected R2/R3 tail arithmetic

The branch-alone R2 computation, with its tracked q=5 engine and local q=8
support modules, returned:

```text
$ /Users/za/.venvs/farey-rh/bin/python research_notes/rh_goals_2026-08-14/lane_f/q8_r2_local.py --N-targets 256 320
Q8_R2_LOCAL N=256 T_tail=[3.4499945503265230464527639567213577262548803647375061375452736025323943245729900e-39 +/- 1.85e-119]
Q8_R2_LOCAL N=320 T_tail=[3.0481340275887105508444872207199434529464104721998028331647767441175424434761729e-49 +/- 3.38e-129]
{
  "receipt": "/Users/za/Documents/farey-hecke/.worktrees/law-q8-generic-20260819/research_notes/rh_goals_2026-08-14/lane_f/f8_receipts/Q8_R2_F1024_LOCAL_RECEIPT.json",
  "B_total": "[210.14521492931971232170979202292205134748983390033309673338685951951965406962853 +/- 3.23e-78]",
  "T_tail": {
    "256": "[3.4499945503265230464527639567213577262548803647375061375452736025323943245729900e-39 +/- 1.85e-119]",
    "320": "[3.0481340275887105508444872207199434529464104721998028331647767441175424434761729e-49 +/- 3.38e-129]"
  }
}
```

The endpoint `B_finite` replay, using the same local branch, returned

```text
$ /Users/za/.venvs/farey-rh/bin/python research_notes/rh_goals_2026-08-14/lane_f/q8_endpoint_B.py --N 256 320
Q8_ENDPOINT_B factors=('10','4','2') N=256 B_finite_upper=[39.162333736337258832479088678160583659224562058665365906221102957934537903919244 +/- 4.57e-79] runtime=36.339s
Q8_ENDPOINT_B factors=('10','4','2') N=320 B_finite_upper=[39.162333736337258832479088815439151314881324723709958679095589296591001634134888 +/- 2.68e-79] runtime=58.769s
```

Using `F_R = T_tail * exp(1 + 2*B_finite)`, the corrected arithmetic
is:

```text
$ /Users/za/.venvs/farey-rh/bin/python research_notes/rh_goals_2026-08-14/lane_f/q8_r3_correction.py
Q8_R3_CORRECTION N=256 T_tail=[3.4499945503265230464527639567213577262548803647375061375452736025323943245729900e-39 +/- 1.86e-119] B=[39.162333736337258832479088678160583659224562058665365906221102957934537903919244 +/- 4.58e-79] F_R=[9.7293487550026303628682679940766109501031363339606542488539982532787152686788824e-5 +/- 3.18e-85]
Q8_R3_CORRECTION N=320 T_tail=[3.0481340275887105508444872207199434529464104721998028331647767441175424434761729e-49 +/- 3.39e-129] B=[39.162333736337258832479088815439151314881324723709958679095589296591001634134888 +/- 2.69e-79] F_R=[8.5960596672810867943045024839605243831934627616956281204687918447113684141162991e-15 +/- 4.91e-95]
```

Thus (N=256) gives a corrected tail error below (9.730\times10^{-5})
(rounded upward), while (N=320) gives a corrected tail error below
\(8.597\times10^{-15}\) (rounded upward).  These are quantitative
improvements only: no continuous determinant lower margin at the selected
finite section has yet been certified, so neither row upgrades the theorem
status.

The old `q8_certify_r2_flagship.py` adapter remains historical only: it loads
the pre-existing q=7 wrapper whose constants contain an external worktree
path.  The reproducible branch-alone command for this correction is
`q8_r2_local.py`; no claim below relies on the old adapter.

### 7.3 Continuous contour and E1 status

The closed-subarc machinery is genuine interval/Taylor machinery, but the
current full-contour attempt does not yet pass its Neumann gate at an
unsplit (N=32) edge.  The exact branch-alone diagnostic was:

```text
$ /Users/za/.venvs/farey-rh/bin/python - <<'PY'
... q8_finite_taylor_probe.arc_certificate(32, segment) ...
PY
bottom ERR ArithmeticError('finite Neumann q not below one: [144.777393349500368725940872780353983554670551687... +/- 1.59e-113]')
right ERR ArithmeticError('finite Neumann q not below one: [144.777199263888029002206161947546547222516168373... +/- 4.78e-113]')
top ERR ArithmeticError('finite Neumann q not below one: [144.777920913222134293374459763962642597780520524... +/- 3.53e-113]')
left ERR ArithmeticError('finite Neumann q not below one: [144.778079703820061767670831869245358385007223181... +/- 1.45e-113]')
```

This is an enclosure/implementation failure for those unsplit arcs, not a
refutation of the target.  Adaptive subdivision at production (N=320),
followed by a determinant winding and a theorem-valid comparison to the
Fredholm limit, remains **OPEN**.

The next repair can remain theorem-valid: either (i) bisect each edge until
the same interval Taylor/resolvent test proves the strict inequalities
`Neumann_q_upper < 1` and `Jacobi_rH_upper < 1` on every closed subarc, or
(ii) use a resolvent-centered propagation bound with an explicitly enclosed
inverse and derivative norm.  The first failing inequality in the current
unsplit run is the Neumann one itself: the required `q_upper < 1` is reported
as `q_upper ≈ 144.7772–144.7781` in the command output above.  No adaptive
production receipt has yet established the repaired inequalities, so this is
an identified implementation gate, not a proof.

The enlarged-disc E1 diagnostic does pass its scalar contraction check:

```text
$ /Users/za/.venvs/farey-rh/bin/python research_notes/rh_goals_2026-08-14/lane_f/q8_e1_probe.py
{
  "rho_hat_upper_bound": "[0.76506827070502964149539400000000000000000000000000000000000000000000000000000000 +/- 4.35e-25]",
  "rho_hat_less_than_one": true,
  "enlargement_lower": [
    "[0.11888450083583040950344741600199291497479562566929130243562234501908220468569223 +/- 6.81e-82]",
    "[0.067251229375194767717159028808322494038485118477971591455891252680630928313750015 +/- 3.99e-82]",
    "[0.081179415021929547659958480804958413009160809506702316702194564347948346031151900 +/- 2.86e-83]"
  ]
}
```

The E1 output is **AWAITING COLD REFEREE** and does not by itself supply the
missing continuous contour, Fredholm tail, or MMS factorization.

### 7.4 q=8 (K_s) diagnostic and corrected lattice margin

The q=8 even cycle used in the local probe is (L_1,L_1,L_2), with matrix
word (M_2M_1M_1).  The branch-alone Arb output is:

```text
$ /Users/za/.venvs/farey-rh/bin/python research_notes/rh_goals_2026-08-14/lane_f/q8_ks_probe.py
{
  "trace_lower": "[5.2262518595055061114265726937087486143350447533970781101955934676323241658447682 +/- 3.81e-81]",
  "ell": "[0.19891236737965800691159762264467622859785050132159098192111699582542960446027706 +/- 3.06e-81]",
  "vertical_spacing": "[1.9453900087781875901691894847309682975594386386220698900532052622768813525369782 +/- 1.31e-80]",
  "nearest_box_distance_lower": "[0.62275772234726125216357493993765150538433625021203997615264574300368762687318629 +/- 1.67e-82]",
  "detKs_abs_lower": "[0.738968034275870967792872074971256316266319640630753... +/- 2.25e-81]"
}
```

The `nearest_box_distance_lower` field reproduces the plan's approximately
`0.6227577` diagonal lattice clearance after correcting the earlier probe,
which had reported only vertical clearance.  The product lower bound is a
q=8 diagnostic, not yet a theorem claim: the cycle orientation, MMS source
convention, and closed-box monotonicity argument require a separate cold
referee.  `K_s` therefore remains **OPEN / AWAITING COLD REFEREE**.

### 7.5 Moving-λ interval check and all-q conclusion

A fixed q=8 model is locally stable only on the first tiny slab tested:

```text
$ /Users/za/.venvs/farey-rh/bin/python research_notes/rh_goals_2026-08-14/lane_f/q8_lambda_slab_probe.py
Q8_LAMBDA_SLAB 1.8477590650225735..1.848 rho=[0.69704646198078989982605000000000000000000000000000000000000000000000000000000000 +/- 3.95e-4] all_block_pass=True
Q8_LAMBDA_SLAB 1.848..1.850 rho=[0.70030430704355239868164100000000000000000000000000000000000000000000000000000000 +/- 3.30e-3] all_block_pass=False
```

This does not prove that no smaller subdivision could work; it proves only
that the tested (2\times10^{-3}) second slab fails the selected ratio gate.
More importantly, it remains a fixed-κ q=8 model.  The exact source counts
quoted in §5 still show unbounded κ as (q\to\infty), so a finite q=8
interval enclosure cannot be promoted to the full law.  A q-generic theorem
would need a new uniform infinite-dimensional construction or a genuinely
effective finite-range theorem; that route is **OPEN / CONJECTURAL**.

### 7.6 Updated status

The corrected status is therefore:

1. q=8 MMS-(32) block binding: explicit and branch-reproducible, **AWAITING
   COLD REFEREE**.
2. q=8 TB/W/R2 numerical majorants: recomputed at F1024; the N=320 scalar
   R3 correction is (<8.597\times10^{-15}) by the quoted receipt, but the
   theorem-valid Fredholm tail/continuous contour comparison is **OPEN**.
3. Continuous closed-contour winding for the full Fredholm determinant:
   **OPEN**.
4. E1 scalar contraction: diagnostic passes with the quoted `rho_hat` but is
   **AWAITING COLD REFEREE**.
5. (K_s) nonvanishing: diagnostic gives the quoted diagonal clearance and
   product bound but is **OPEN / AWAITING COLD REFEREE**.
6. Common continuation/factorization to Selberg zeros: **OPEN**.
7. Full q-generic λ/q interval: **OPEN / CONJECTURAL**; changing unbounded
   block dimension is the exact obstruction to the finite q=8 shortcut.

No Kaggle run was launched.  With the Fredholm comparison and continuous
enclosure still open, a remote same-byte run would be **NOT EVIDENCE** for the
missing theorem.

The local q8 scripts used for the corrected receipts resolve all imports from
the branch itself.  A branch-alone check was:

```text
$ /Users/za/.venvs/farey-rh/bin/python -m py_compile ...
PYCOMPILE_EXIT=0
BRANCH_ALONE_IMPORTS 15 PASS
$ rg -n "aletheia-restore|\.worktrees" lane_f/q8_*.py lane_f/f8_source_builder.py lane_f/f8_certify_tb_blocks.py
(no output)
$ git diff --check
(no output; exit 0)
```

All promotion-level items in this correction remain **AWAITING COLD
REFEREE**; the first remaining mathematical gap is still the theorem-valid
Fredholm tail plus a continuous full-contour enclosure at a certified
finite-section margin.

## 8. Dated correction block — 2026-08-19 — adaptive acceptance defect

This block is appended rather than rewriting §7.3.  The first serial adaptive
run exposed a false target in the driver: `arc_certificate` reported whether
the finite Taylor image excluded zero, but the adaptive loop subdivided only
when the Neumann or Jacobi inequalities raised an exception.  It could
therefore accept a subarc with `finite_taylor_abs_lower=0`.  The proposed run
was **REFUTED as a continuous finite-section certificate** and was terminated;
it is not evidence for a winding.

A direct fresh replay of four depth-7 bottom subarcs gave:

```text
$ PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python -c \
    '<construct depth-7 bottom subarcs; call arc_certificate(32, seg)>'
depth7_i 0 q [0.21101694584349112887758422932742941673552857465510236014584888445305880717411280 +/- 4.24e-82] rH [0.47909396346609150190538098910372947665035846544469063359619625124470720113806669 +/- 3.03e-81] lower 0 excludes False
depth7_i 32 q [0.24584593412013942685331759087447720863690099789717489333359312933278168485797049 +/- 1.88e-82] rH [0.73970826868101673129170947534477868983769664060156555296388073946954118361559783 +/- 4.65e-81] lower 0 excludes False
depth7_i 64 ERR ArithmeticError('finite Jacobi rH not below one: [1.205588034870194486422405081797422972950229249596373422603911172639326779239927609681070199892441163029928541617292 +/- 4.71e-116]')
depth7_i 96 q [0.29250501708270615238943568439953851570636779940800540674434535964106118038498305 +/- 3.43e-81] rH [0.94363388892703881512225264217287689842727498801331180407998701980476137900784764 +/- 4.23e-82] lower 0 excludes False
```

Thus `rH<1` does not imply zero exclusion; the negation is witnessed by
three quoted interval rows.  The loop is now repaired to treat every
non-excluding finite Taylor box as a subdivision failure.  No corrected full
run is claimed here.  Moreover, even a positive finite lower bound is not the
full theorem gate: an accepted subarc must eventually have a strict lower
bound exceeding an upward theorem-valid Fredholm determinant-tail allowance.
That comparison remains **OPEN / CONJECTURAL**.  The proposed terminal
block-Schur evaluator is being developed separately to make the corrected
continuous computation tractable.

The terminated process receipt was:

```text
$ kill -TERM 39096
$ ps -ww -p 39096 -o pid=,ppid=,stat=,etime=,%cpu=,command=
[no output]
```

No TB, R2 scalar arithmetic, E1, or `K_s` diagnostic is numerically refuted by
this driver bug.  Their paper-level binding and all downstream promotion
statuses remain exactly as caveated in §7.6 and await a cold referee.
