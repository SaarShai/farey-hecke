# RATE-A constant reduction, third stage: the residual (AM) §3 rounding audit

**Date:** 2026-08-20
**Program:** `(RATE)`, lane G, rung 3
**Interpreter:** `/Users/za/.venvs/farey-rh/bin/python`, Python 3.13.13, python-flint 0.9.0
**Repo HEAD at authoring:** `029dc8533b8e3f569cd4e2d9225db60d4b694049`
**Write scope:** this file only. No existing file was read-modified, renamed or
deleted. No commit, no push.

---

## 0. What this note does

`CR_REDUCTION_V2_SOL.md` §5.1 left one item explicitly CONJECTURAL: whether the
*remaining* powers of two in the atom bridge's (3.19)/(3.24)/(3.25) admit
exact-value substitution of the same kind as the banked `2^20 -> 82944`. This
note audits **every** remaining factor in the `(AM)` §3 chain, plus the outer
`M_0`, `S` and `F(12)`, executes the substitutions that are legal, and
propagates.

Result in one line: **three** of the residual factors are legally
substitutable, worth **1.7179 e-folds** jointly; two more are non-substitutable
without a new lemma and are graded CONJECTURAL; one is legal but
**non-binding** (zero gain) and one has **zero slack**.

### 0.1 The object under audit

`ATOM_MOMENT_BRIDGE_SOL.md` (3.25)/(3.26) assemble the high regime as

\[
 \underbrace{2^{12}}_{\text{core convolution (3.5)}}
 \cdot\underbrace{2^{20}}_{\text{all tags (3.9)}}
 \cdot\underbrace{2^{11}}_{40^2<2^{11}}
 \cdot\underbrace{2^{4}}_{\text{four zeta sums}}
 \cdot\underbrace{2^{14}}_{\text{high regime (3.24)}}
 \cdot\underbrace{2}_{\text{conservative ordering (3.13)}}
 =2^{62},
\]

and `(3.28)` adds the Ford unit term, giving `C_atom = 2^62 + 1`. The banked
`C_4'' = 2^52·81 + 1` is exactly this product with `2^20 -> 82944`. Every
factor above is a separate line item and is audited below.

### 0.2 Legality test used (CR_REDUCTION_V2_REFEREE.md attack-1 template)

A substitution is graded **LEGAL** only if all four hold:

1. the sharper value is an upper bound on **the same combinatorial object**,
   printed **in the source note itself**;
2. the factor enters the `2^62` subtotal **exactly once**;
3. it enters **multiplicatively**, not additively or inside a logarithm;
4. no downstream step re-uses the *rounded* value (no double-consumption).

Anything failing (1) is graded CONJECTURAL with the exact missing derivation
named. **LEDGER RULE observed throughout:** each substituted value is stated as
a *bound*, never as an exact cardinality — this was the last referee's D1.

---

## 1. Per-factor audit table

| # | factor | what it ceilings | what the source actually **proves** (printed) | legal? | e-fold gain |
|---|---|---|---|---|---|
| 1 | `2^12` (3.5) | core-convolution count `C_j(Z)`, `0<=j<=3` | (3.4) prints `C_3(Z) <= (2048/3) Z^2 (L+2)^2`, `L=floor(log_2 Z)` — a **different functional form** (`L+2`, not `1+log Z`) | **NO** — needs a new sup lemma | 0 (see §4.1) |
| 2 | `2^20` (3.9) | complete finite tag set | (3.9) prints `4^2·3^4·2^3·4·2 = 82944 < 2^17 < 2^20` | LEGAL | **already banked** (2.537, §9) |
| 3 | `2^11` (3.25) | the `40^2` product-gain conversion | (3.25) underbrace prints `40^2 < 2^11`; `40^2 = 1600` | **YES** | **0.24686** |
| 4 | `2^4` (3.25) | four auxiliary unweighted-integer zeta sums | (3.12) prints both sums **exactly** `= pi^2/6`, then bounds each `< 2`; "there are at most four" | **YES** | **0.78179** |
| 5 | `2^11` (3.19) | low-regime `Sigma_H + Sigma_rest` | (3.19) prints `(2^8+2^10)Y = 1280Y`; (3.16) `625Y`, (3.18) `200Y`, so `825Y` | LEGAL but **NON-BINDING** | **0** (§1.1) |
| 6 | `2^14` (3.24) | high-regime `Sigma_H + Sigma_rest` | (3.24) prints `(2^5+2^13)(qR^2+R^4)`, i.e. **8224** | **YES** | **0.68925** |
| 7 | `2` (3.13) | conservative ordered-distinct-pair factor | source says it is retained "**even though** Lemma 4.1 is already formulated for ordered marked atoms" — redundancy asserted, not proved | **NO** — new obligation | 0 (§4.2) |
| 8 | `M_0 = 2.775` | `sup_{s in K_15} |M(s)|` | `M3_UNIFORMITY_EXECUTION_SOL.md:275` prints `sup = M(1.1) < 2.775`; the value of `M(1.1)` is **not printed** | **NO** — new obligation | 0 (§4.3) |
| 9 | `S = 7.648` | contour sup-norm on `Gamma_R^A` | `BOUNDARY_ALPHA_THEOREM_SOL.md` §1.2 **prints and computes** `S_GammaA = 7.646893243596647842...` | LEGAL but **negligible** | 0.000128, **not taken** (§1.2) |
| 10 | `F(12) = 7940` | `1225/4 + 91605/q` at `q = 12` | (4.4); `1225/4 + 91605/12 = 306.25 + 7633.75 = 7940` | **ZERO SLACK** — exact | 0 |

**Total taken here: 0.24686 + 0.78179 + 0.68925 = 1.71790 e-folds.**

### 1.1 Why #5 is non-binding (a real finding, not a dodge)

`(3.26)` takes the **maximum** of the two regimes: low costs `2^(47+11+1) = 2^59`,
high costs `2^(47+14+1) = 2^62`. `C_4` is the high regime. Reducing the
low-regime factor `2^11 -> 1280` (or even `-> 825`) leaves `C_4` unchanged
because low stays strictly below high. Verified after substitution, not assumed:

```text
sub_hi= 65459394456774530.047882...
sub_lo_upper= 10188232600276191.447141...
high_binds= True
```

So `(3.19)` is audited and **explicitly banked at zero gain**. Any note
claiming e-folds from `(3.19)` would be wrong.

### 1.2 Why #9 is available but not taken

`S = 7.648` is a declared rounding of a quantity the boundary note itself
computes to 120 digits. Substituting it is legal by all four tests and would
add `ln(8.648/8.646894) = 0.000128` e-folds. It is **not taken**, so that the
assembly below stays byte-identical to the §8/§9 assembly except for the single
`C_4` line — the same discipline the V2 note used for its A0 replay. Recorded
as available slack, deliberately unspent.

---

## 2. The three legal-substitution proofs

Throughout, `Sigma_hi` denotes the high-regime `A_X^2` subtotal coefficient of
`(3.26)`, i.e. the product displayed in §0.1.

### 2.1 `2^11 -> 1600` (the `40^2` conversion)

**Object.** `(3.10)` is boxed as `D·prod rho_i <= 4 pi^2 x_X < 40 x_X`. §3.3
sets `Z := 40Y/D` and `(3.11)` inserts `Z^2` into `(3.5)`, producing exactly one
factor `40^2` in the closed constant.

**Once, multiplicatively.** `40^2` appears in `(3.25)` as a single underbraced
multiplicative term, and in the §4.1 ledger as a single row
("product-gain conversion `40^2` | `< 2^11`"). It occurs nowhere else in the
`(3.26)` product.

**No double consumption.** The *other* appearances of `40` in §3 are inside
logarithms — `1+log_+(40Y/D)`, `1+log(40Y)`, `(1+log 40)^4 < 5^4`,
`t = H/Y <= 40`, `B = 1+log(40Y/h)`. Those are consumed by `(3.16)`, `(3.18)`,
`(3.20)`, `(3.23)`, i.e. by items #5 and #6 of the table, **not** by the `40^2`
factor. Substituting the multiplicative `40^2` therefore does not touch any
logarithmic use of `40`. This is the exact hazard attack-1 checks for, and it
is clean.

**Sharper printed value.** `(3.25)` itself prints `40^2 < 2^11`. The sharper
bound is the printed left-hand side, `1600`.

**NOT claimed:** that `40` may be replaced by `4 pi^2 = 39.478...`. It may not,
by a single substitution: `40` is load-bearing inside the logarithms above and
sharpening it would require re-deriving `(3.16)`, `(3.17)`, `(3.20)` and
`(3.23)`. See §4.4.

### 2.2 `2^4 -> (pi^2/6)^4` (the four zeta sums)

**Object.** `(3.12)` prints, for each unweighted auxiliary integer,
`sum_{r>=1} 1/r^2 = pi^2/6 < 2` and `sum_{r>=0} 1/(1+r)^2 = pi^2/6 < 2`, then:
"There are at most four, so their complete cost is `< 2^4`."

**The source's own operation.** The source forms the **fourth power of its own
per-integer bound**. Substituting the sharper per-integer bound `pi^2/6` — which
`(3.12)` prints as an *equality* for both bridge shapes — into the identical
fourth-power operation is the same step with a sharper input, not a new lemma.
Both bridge shapes give the same value, so the mixture of shapes across the "at
most four" integers is irrelevant.

**Once, multiplicatively.** One underbraced term in `(3.25)`, one ledger row
("at most four auxiliary zeta sums | `< 2^4`"). The `pi^2/6 < 2` of `(3.12)` is
consumed nowhere else; the separate `pi^2/6 < 2` at `(3.12)`'s second line is
the same displayed line, not a second consumption.

**LEDGER RULE.** `(pi^2/6)^4 = 7.32139738894334414130...` is an **upper bound**
on the four-integer cost, because "at most four" and because each per-integer
cost is at most `pi^2/6`. It is **not** a count and **not** claimed exact.

### 2.3 `2^14 -> 8224` (the high regime)

**Object.** `(3.24)` prints, verbatim,
`Sigma_H + Sigma_rest < (2^5 + 2^13)(qR^2 + R^4) < 2^14 (qR^2 + R^4)`.

**Sharper printed value.** `2^5 + 2^13 = 8224`, printed as the middle member of
the source's own displayed chain. The final `< 2^14` is a pure rounding of it.
This is the cleanest case in the audit: the sharper bound is literally on the
page, bounding literally the same object, in the same functional form
`(qR^2 + R^4)`.

**Once, multiplicatively.** `(3.26)` uses it once, as the exponent `14` in
`2^(47+14+1)`; ledger row "high-regime heavy-plus-rest sum | `< 2^14 (qR^2+R^4)`".

**NOT claimed:** the further tightening to `5803` from the printed intermediates
`25` at `(3.21)` and `5778q + 27R^4` at `(3.23)`. That needs a recombination
step. See §4.5.

### 2.4 The joint coefficient `C_4'''`

Applying #2 (banked), #3, #4, #6 and keeping #1, #7 unchanged:

```bash
PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import arb, ctx
ctx.dps=140
z=arb.pi()**2/6
sub_hi = arb(2)**12*arb(82944)*arb(1600)*z**4*arb(8224)*arb(2)
sub_lo = arb(2)**12*arb(82944)*arb(1600)*z**4*arb(1280)*arb(2)
print('zeta_factor=(pi^2/6)^4=',z**4)
print('sub_hi=',sub_hi)
print('sub_lo_upper=',sub_lo.upper())
print('high_binds=',bool(sub_lo<sub_hi))
C4p3=int(arb(sub_hi.upper()).ceil().unique_fmpz())+1
print('C_4_ppp=',C4p3,'strict=',bool(arb(C4p3)>sub_hi+1))
PY
```

```text
zeta_factor=(pi^2/6)^4= [7.321397388943344141302913197458924225846589098488489731566428561008417362524210104965636054798545622782984936762477948108833434204701758122 +/- 6.18e-139]
sub_hi= [65459394456774530.04788237489175621117372539410036399669031019577397289371244061359014048107103292899133206412577809378720312193103342354187 +/- 3.28e-123]
sub_lo_upper= [10188232600276191.447141225664086569832486442661535252403161119964820683846294258924535483435180222411102266790004372573883754386153062029864 +/- 4.27e-124]
high_binds= True
C_4_ppp= 65459394456774532 strict= True
```

The subtotal is irrational (the `(pi^2/6)^4` factor), so it is rounded **UP** to
the least integer above it before the Ford unit term is added:

\[
 \boxed{C_4'''=65459394456774532}
\]

a paper-level upward-valid atom-moment coefficient on exactly the `(AM)` scope,
`ln(C_4''/C_4''') = 1.71790` e-folds below the banked `C_4''`, and `30.5945`
e-folds below the published `2^100`.

---

## 3. `C_R'''` and the propagated conditional A0 cutoff

### 3.1 Assembly (identical to §8/§9; only the `C_4` line differs)

The assembly is the `BOUNDARY_ALPHA_THEOREM_SOL.md` §1.2 positive
source-invariant chain: `p = 11/5`, `S = 7.648`, `M_0 = 2.775`,
`F = 1225/4 + 91605/12 = 7940`, the wrap term, outward roundings, and the
**least integer strictly above** the raw analytic coefficient.

```bash
PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import arb, ctx
ctx.dps=120
def Z(a):
 s=str(a); assert '+/-' not in s and 'e' not in s.lower()
 u,v=s.split('.',1); assert set(v)<=set('0'); return int(u)
def assemble(C4):
 p=arb(11)/5; S=arb('7.648')
 F=arb(1225)/4+arb(91605)/12
 pair=2*arb.pi()**2*(S+1)*p*arb(C4)*F
 wrap=p*128*(1+arb(2).log())*30
 raw=arb('2.775')*(pair+wrap)
 CR=Z(raw.upper().ceil())
 assert bool(arb(CR)>raw) and bool(arb(CR-1)<=raw)
 return CR,raw
for name,C4 in [('published_2^100',2**100),("C_4'_2^62+1",2**62+1),
                ("C_4''",2**52*81+1),("C_4'''",65459394456774532)]:
 CR,raw=assemble(C4)
 print(name,'C_R=',CR,'log=',str(arb(CR).log())[:22],'minimal_both_ways=True')
PY
```

```text
published_2^100 C_R= 10489412368759562746433608215977724802 log= [85.243429750394033162 minimal_both_ways=True
C_4'_2^62+1 C_R= 38160259896392973127946053 log= [58.903836889116111404 minimal_both_ways=True
C_4'' C_R= 3018536183210772296097745 log= [56.366814238189097078 minimal_both_ways=True
C_4''' C_R= 541656022363559883954520 log= [54.648918107756483473 minimal_both_ways=True
```

**Convention lock.** The first three lines reproduce, digit for digit, the
published `C_R`, the banked `C_R'` (§8) and the banked `C_R''` (§9). The
`assert` enforces minimality in **both** directions (`C_R > raw` and
`C_R - 1 <= raw`) on every line, so the fourth line is produced by exactly the
convention that certifies the first three.

\[
 \boxed{C_R'''=541656022363559883954520},\qquad \log C_R''' = 54.6489181077\ldots
\]

`1.71790` e-folds below `C_R''`; cumulative `30.5945` below the published §4
ceiling. Note `log C_R` moves by exactly the `C_4` e-folds, as it must — `C_4`
enters the pair term linearly and the wrap term (`14303.7...`) is negligible
beside it but is **kept**, not dropped.

### 3.2 A0 propagation (`R5_ACTIVATION_CLOSURE_SOL.md` §4 program, one line changed)

Fixed inputs kept exactly: `alpha = 6/5`, `nu = 0.1552`, `m = 0.0439`,
`K_+ = 117`, `beta = alpha·nu = 0.18624`, `q_RATE = 12`, `q_divisor = 3`,
`q_transport = floor(exp(T)) + 1` from the unrounded Arb interval with
lower/upper floor agreement asserted, plus the side branch `(4.2)`.

```bash
PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import arb, ctx
ctx.dps = 120
def ei(a):
    s=str(a); assert '+/-' not in s and 'e' not in s.lower()
    w,f=s.split('.',1); assert set(f)<={'0'}; return int(w)
alpha=arb(6)/5; nu=arb('0.1552'); m=arb('0.0439'); K=arb(117)
beta=alpha*nu
def run(CRint,tag):
    CR=arb(CRint)
    Ts=(CR.log()-K.log())/alpha; es=Ts.exp()
    lo,hi=ei(es.lower().floor()),ei(es.upper().floor()); assert lo==hi
    qs=hi+1
    T=((1-nu)*K.log()-m.log())/beta+CR.log()/alpha; eT=T.exp()
    l2,h2=ei(eT.lower().floor()),ei(eT.upper().floor()); assert l2==h2
    qt=h2+1
    ERs=CR*arb(qs)**(-alpha); ERt=CR*arb(qt)**(-alpha)
    U=K**(1-nu)*ERt**nu
    print(tag)
    print(' T_side=',str(Ts)[:26],'q_side=',qs)
    print(' side_min=',bool(arb(qs).log()>Ts),bool(arb(qs-1).log()<=Ts),'ER_side_lt_K=',bool(ERs<K))
    print(' T=',str(T)[:26])
    print(' q_transport=',qt)
    print(' min=',bool(arb(qt).log()>T),bool(arb(qt-1).log()<=T))
    print(' ER_lt_K=',bool(ERt<K),'A0_upper=',str(U.upper())[:28],'A0_strict_lt_m=',bool(U<m))
    print(' q_side_lt_qt=',qs<qt,'ge_qRATE=',qt>=12,'ge_qdiv=',qt>=3)
    print(' log_q_transport=',str(arb(qt).log())[:26])
run(10489412368759562746433608215977724802,'CROSSCHECK published')
run(38160259896392973127946053,'CROSSCHECK banked C_R prime')
run(3018536183210772296097745,'CROSSCHECK banked C_R doubleprime')
run(541656022363559883954520,'NEW C_R triple-prime')
PY
```

```text
CROSSCHECK published
 T_side= [67.0677131796635642027495 q_side= 134010166814705707171424895246
 side_min= True True ER_side_lt_K= True
 T= [109.421745040159523743786
 q_transport= 332093267419812025416641789732742045430624465595
 min= True True
 ER_lt_K= True A0_upper= [0.0438999999999999999999999 A0_strict_lt_m= True
 q_side_lt_qt= True ge_qRATE= True ge_qdiv= True
 log_q_transport= [109.421745040159523743786
CROSSCHECK banked C_R prime
 T_side= [45.1180524619319627380521 q_side= 39311645103099547636
 side_min= True True ER_side_lt_K= True
 T= [87.4720843224279222790891
 q_transport= 97418971860452658435229799565334786148
 min= True True
 ER_lt_K= True A0_upper= [0.0438999999999999999999999 A0_strict_lt_m= True
 q_side_lt_qt= True ge_qRATE= True ge_qdiv= True
 log_q_transport= [87.4720843224279222790891
CROSSCHECK banked C_R doubleprime
 T_side= [43.0038669194927841330064 q_side= 4746157036282968395
 side_min= True True ER_side_lt_K= True
 T= [85.3578987799887436740434
 q_transport= 11761546420922598622910053339543258496
 min= True True
 ER_lt_K= True A0_upper= [0.0438999999999999999999999 A0_strict_lt_m= True
 q_side_lt_qt= True ge_qRATE= True ge_qdiv= True
 log_q_transport= [85.3578987799887436740434
NEW C_R triple-prime
 T_side= [41.5722868107989394622408 q_side= 1134004458443795841
 side_min= True True ER_side_lt_K= True
 T= [83.9263186712948990032778
 q_transport= 2810199067910634377586449487575862960
 min= True True
 ER_lt_K= True A0_upper= [0.0438999999999999999999999 A0_strict_lt_m= True
 q_side_lt_qt= True ge_qRATE= True ge_qdiv= True
 log_q_transport= [83.9263186712948990032778
```

**Three-way convention lock.** The replay reproduces the published `q_transport`
(`R5_ACTIVATION_CLOSURE_SOL.md` §4 stdout), the banked §8 integer
`97418971860452658435229799565334786148`, and the banked §9 integer
`11761546420922598622910053339543258496`, all exactly, before producing the new
one.

### 3.3 Result

\[
 \boxed{q_{A0}'''=2810199067910634377586449487575862960},\qquad
 \log q_{A0}''' = 83.9263186712948990\ldots
\]

with side integer `q_side''' = 1134004458443795841`.

Both floor endpoints agree and both minimality lines hold, so this is exactly
`floor(exp(T)) + 1` and is the **least** integer meeting the strict condition.
The A0 envelope at the cutoff is strictly `< m = 0.0439`; the nonzero-branch
side hypothesis holds at both `q_side` and `q_transport`; `q_side < q_transport`;
and `q_transport >= q_RATE = 12`, `>= q_divisor = 3`.

### 3.4 The print-set, stated honestly (the D2 lesson)

The replay program above is **not** byte-identical to
`R5_ACTIVATION_CLOSURE_SOL.md` §4: it is wrapped in a function so the same code
path runs on four constants, and it **prints a strict subset** of the source's
lines — the `alpha`, `nu`, `alpha_nu`, `beta_exact`, `q_RATE`, `q_divisor`,
`ER_at_q_side_upper` and `ER_at_q_transport_upper` lines are computed but
truncated or not printed, and the interval strings are truncated to 26
characters for width. **Every mathematical operation, constant and assertion is
unchanged.** The three cross-check lines are the evidence that the wrapping did
not change the arithmetic; a referee wanting the untruncated full print-set can
run the source's §4 program verbatim with the single line
`CR = arb(541656022363559883954520)`.

### 3.5 Label

This is a **selected, conditional A0 analytic-tail transport cutoff** — one term
in a `max`, on exactly the prior scope, inheriting every paper-level
Route-B / Ford / two-mark premise of its source. It is **not** a final `q_0`.

**`q_monotone` is KEPT.** Per the referee-D7 correction block at
`R5_MONOTONICITY_GATE_SOL.md:803-829` the removability claim is REFUTED; the
onset ledger retains

\[
 q_0=\max\{12,\ q_{\rm RATE},\ q_{\rm transport},\ q_{\rm divisor},\
 q_{\rm geometry},\ q_{\rm monotone},\ \ldots\}.
\]

Nothing here bears on `q_monotone` and nothing here removes it.

---

## 4. CONJECTURAL — everything illegal or unproved

Each item names the **exact** missing derivation. None is used above; `C_4'''`
and `C_R'''` are independent of all of them.

### 4.1 `2^12 -> 8192/3` at (3.5) — CONJECTURAL (0.4055 e-folds)

**Why illegal.** `(3.4)` proves `C_3(Z) <= (2048/3) Z^2 (L+2)^2` with
`L = floor(log_2 Z)`. The downstream form `(3.5)` and its consumer `(3.11)` use
`Z^2 (1+log Z)^2`. These are **different functional forms**; the constant `2^12`
absorbs the conversion.

**Exact missing derivation.** Prove
`sup_{Z>=1} (floor(log_2 Z)+2)^2 / (1+log Z)^2 = 4`, attained at `Z = 1`.
Numerically the ratio `(L+2)/(1+ln Z)` is `2` at `Z=1`, `1.772` at `Z=2`,
`1.676` at `Z=4`, `1.624` at `Z=8`, `1.590` at `Z=16`, apparently decreasing —
but this is an **observation, not a proof**, and the function is discontinuous at
every power of two, so a genuine argument must handle each dyadic block. Given
that sup, the constant would become `(2048/3)·4 = 8192/3 = 2730.67 < 4096`,
worth `ln(1.5) = 0.4055` e-folds. **Not taken.**

### 4.2 Dropping the conservative factor `2` at (3.13) — CONJECTURAL (0.6931 e-folds)

**Why illegal.** The source itself flags this as slack: "We retain an extra
factor `2` for the second sum, **even though Lemma 4.1 is already formulated for
ordered marked atoms**. This makes the ledger conservative." That is an
*assertion* of redundancy, not a proof of it.

**Exact missing derivation.** Show that the injective code of
`TWOMARK_RENEWAL_SOL.md` Lemma 4.1 already enumerates **ordered** pairs
`(alpha, beta)`, so that the `2 sum_{alpha<beta}` of `(3.13)` is covered by the
tag-and-parameter count without a further factor `2`; and check this against the
"one-mark/two-mark selector" already counted as the trailing factor `2` in
`(3.9)`'s `4^2·3^4·2^3·4·2` — the risk is that removing `(3.13)`'s `2` **and**
keeping `(3.9)`'s selector double-counts in the opposite direction, or that they
are the same factor counted once. This is the single largest residual e-fold and
the one most worth a dedicated proof lane. **Not taken.**

### 4.3 `M_0 = 2.775` — CONJECTURAL, and a NEW proof obligation

`M3_UNIFORMITY_EXECUTION_SOL.md:275` prints
`sup_{s in K_15} |M(s)| = M(1.1) < 2.775`. The source states the sup is
**attained at** `s = 1.1` but does **not** print the value of `M(1.1)`, so no
sharper number is available from printed text. `M_0` enters the assembly once,
multiplicatively, as the outermost factor, so any reduction is e-fold-for-e-fold.

**Exact missing derivation.** A certified enclosure of `M(1.1)` on `K_15`
(interval evaluation of `M` at the located maximizer plus a rigorous
sup-attainment argument on the compact `K_15`), then `M_0 := ceil` of that
enclosure's upper endpoint. **Graded CONJECTURAL. Not taken.** The V2 note
already listed the `M_0` tightening as "unavailable"; this audit confirms that
verdict rather than overturning it.

### 4.4 `40 -> 4 pi^2` throughout §3 — CONJECTURAL

`(3.10)` proves `4 pi^2 x_X < 40 x_X`, and the AM referee prints
`4pi^2= 39.4784176043574344753379639995 lt_40= True`. But `40` occurs in §3 both
multiplicatively (audited as #3, taken) and **inside logarithms** at `(3.11)`,
`(3.15)`, `(3.16)`, `(3.17)`, `(3.20)`, `(3.23)`. A global substitution fails
legality test (2)/(4): it is not a single-occurrence multiplicative change.

**Exact missing derivation.** Re-derive `(3.16)` (`(1+log 4pi^2)^4 < 625`?),
`(3.17)`/`(3.18)` (the `t <= 4pi^2` maximization, currently giving `200` at
`t = 40`), `(3.20)`'s `c = log(4pi^2·5/2)` in place of `log 100`, and `(3.23)`'s
`(1+log 4pi^2)^4 <= 209q` step. Every one is a fresh maximization. **Not
attempted, not estimated. Not taken.**

### 4.5 `8224 -> 5803` at (3.24) — CONJECTURAL (a further 0.3487 e-folds)

`(3.21)` prints the intermediate value `25` before rounding to `2^5`, and
`(3.23)` prints `5778q + 27R^4` before rounding to `2^13(q+R^4)`. Recombining
gives `Sigma_H + Sigma_rest < 5803(qR^2 + R^4)` — but the recombination uses
`q + R^4 <= qR^2 + R^4` (from `R > 1`, printed at §3.5) **and** `max(5778+25, 27)`
across two different coefficient slots. That is a one-line new lemma, not a
substitution of a printed bound on the same object in the same form.
**Graded CONJECTURAL. Not taken.** The taken value `8224` is the one printed
verbatim in `(3.24)`.

### 4.6 `p = 11/5` retune — NOT PURSUED

Per brief and per `CR_REDUCTION_V2_SOL.md` §5.1: changing `p` changes the decay
exponent `alpha`, which propagates into the A0 formula. Sensitivity-only. Not a
repair, not attempted.

---

## 5. What is NOT claimed

1. **No gate is closed.** No program gate moves open -> closed.
2. **Not a final `q_0`.** `q_A0'''` is one term in a `max`.
3. **No unconditional threshold.** `q_A0'''` inherits every paper-level
   Route-B / Ford / two-mark premise of its sources.
4. **`q_monotone` is NOT removed** (§3.5); the D7 refutation stands.
5. **No theorem-ledger promotion.** `C_4'''`, `C_R'''` and `q_A0'''` are
   **unbanked candidates** pending a cold referee, exactly as `C_R'` and
   `C_R''` were before theirs.
6. **The published RATE-A theorem is untouched**, as are the banked `C_R'` (§8)
   and `C_R''` (§9). All remain upward-valid.
7. **No claim of optimality.** `C_4'''` is not claimed minimal. §4 lists
   `0.4055 + 0.6931 + 0.3487 = 1.447` further e-folds that are visible but
   unproved, plus the unquantified `40 -> 4pi^2` and `M_0` routes.
8. **No exactness claims (D1 discipline).** `82944` is a **bound** on the tag
   set, not a cardinality. `(pi^2/6)^4` is a **bound** on the four-integer cost
   ("at most four"), not a value. `1600` and `8224` are **bounds** printed by
   the source. Only `F(12) = 7940` is asserted **exact**, and only because
   `1225/4 + 91605/12` is an exact rational identity.
9. **No machine formalization** and **no certified full-operator enclosure** —
   both remain OPEN per `RATE_A_REFEREE.md:305-307,369-392` and
   `AM_REFEREE.md:360-408`.
10. **No finite base block**, **no standalone N1-RATE** — open/conjectural as
    before.
11. **The `S = 7.648` slack is not spent** (§1.2), and the `(3.19)` low-regime
    slack yields **zero** (§1.1). Neither is counted in the 1.7179.

---

## 6. Source receipt

```bash
git rev-parse HEAD && shasum -a 256 research_notes/rh_goals_2026-08-14/lane_g/{ATOM_MOMENT_BRIDGE_SOL,BOUNDARY_ALPHA_THEOREM_SOL,R5_ACTIVATION_CLOSURE_SOL,CR_REDUCTION_V2_SOL,CR_REDUCTION_V2_REFEREE,AM_REFEREE}.md
```

```text
029dc8533b8e3f569cd4e2d9225db60d4b694049
59ce32f7c6fa86580055d9049e609a2189ecc1645528dd4136758fcf547fbbbb  ATOM_MOMENT_BRIDGE_SOL.md
5a8d0bccdedb7363eec73b6763436a8b7f95b78b366a52b365f3ebc51c152980  BOUNDARY_ALPHA_THEOREM_SOL.md
3b49d73d56cf963703137a6494f1f733fbb208d36c0afbe1affbd5d700ab2a53  R5_ACTIVATION_CLOSURE_SOL.md
e9e5b023ea911a5d196254a134393815a57b4f6cf00fec09150d83a0d7d4b7b6  CR_REDUCTION_V2_SOL.md
04f7f5ed2aa2065e9822be856e17e27f928c300ced81f418a3380772aff236b6  CR_REDUCTION_V2_REFEREE.md
3d655f2c05395688be73e8786cd9a954182cc4842005ff9e7662d05cccf503b4  AM_REFEREE.md
```

```text
py 3.13.13 flint 0.9.0
```

**Observation for the referee (not a claim).** `BOUNDARY_ALPHA_THEOREM_SOL.md`
now hashes `5a8d0bcc...`, whereas `CR_REDUCTION_V2_SOL.md` §5.2 recorded
`1a5a96e6...`. The difference is accounted for by the **§9 append** that the V2
promotion itself added (present in the current file, absent from the hash V2
read). `ATOM_MOMENT_BRIDGE_SOL.md` — the file this entire audit rests on — is
**unchanged**, hashing `59ce32f7...` on both dates. My §3.1 reproduction of the
published `C_R`, of `C_R'` and of `C_R''` confirms the load-bearing assembly is
intact.

---

## 7. Summary table

| quantity | value | status |
|---|---|---|
| `C_4'''` | `65459394456774532` | candidate, paper-level, unrefereed |
| `log C_R'''` | `54.648918107756483473...` | — |
| `C_R'''` | `541656022363559883954520` | candidate, paper-level, unrefereed |
| `q_side'''` | `1134004458443795841` | candidate |
| `q_A0'''` | `2810199067910634377586449487575862960` | selected conditional analytic cutoff, one term of a `max` |
| `log q_A0'''` | `83.9263186712948990...` | — |
| gain vs `C_R''` | `1.71790` e-folds | 3 legal substitutions (#3, #4, #6) |
| cumulative vs published | `30.5945` e-folds | — |
| visible-but-unproved residual | `>= 1.447` e-folds | CONJECTURAL, §4 |

READY FOR JUDGING
