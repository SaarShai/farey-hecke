# RATE-A constant reduction, second stage: the exact finite tag count

**Date:** 2026-08-20
**Program:** `(RATE)`, lane G
**Interpreter:** `/Users/za/.venvs/farey-rh/bin/python`, Python 3.13.13, python-flint 0.9.0
**Repo HEAD at authoring:** `708eafb9c5a8730c6acc0b1fe16e7e389ce23161`
**Write scope:** this file only. No existing file was read-modified, renamed, or deleted. No commit, no push.

---

## 0. Filename deviation from the task brief (read first)

The brief asked for a **new** file at
`research_notes/rh_goals_2026-08-14/lane_g/CR_REDUCTION_SOL.md`.

That path is **already occupied** by a banked note dated 2026-08-19 which has
passed **two** cold referees:

| file | sha256 |
|---|---|
| `CR_REDUCTION_SOL.md` | `89fc61e9bc33db55c95856f5412e87c45da72d3623616435575fb494321b3417` |
| `CR_REDUCTION_REFEREE.md` | `f0f71f09c1c4547805c44f4c649c12a26568fa0f2e8843a90d574ea856dcfa5a` |
| `CR_REDUCTION_REREFEREE.md` | `00cebb30a7370e5487575c181be1878d37ea1a99a9ff8fdacbbdeb05f1898de6` |

Writing to the requested path would have **destroyed refereed banked work**,
in direct conflict with the brief's own LEDGER RULE ("change nothing in
existing files"). The two instructions cannot both be satisfied. I resolved
the conflict in favour of the LEDGER RULE and wrote to
`CR_REDUCTION_V2_SOL.md`. **This is the only deviation from the brief.**

The deviation is not cosmetic: it changes what this note *is*. The brief was
written as if `C_R` were still at its published value and both autopsy targets
were open. Target 1 is **already banked**. This note therefore executes only
the genuinely residual part — target 2 — and does so **on top of** the banked
result rather than re-deriving from the published constant.

---

## 1. Status of the two autopsy targets

`CR_AUTOPSY_LUNA.md` (2026-08-20, sha `e9b7303326c08a4263614a68c1d4ce9e1051ffe539ff7a12eea226e5e2289171`)
lists two reduction targets. Their true state as of this note:

| target | autopsy claim | actual state |
|---|---|---|
| 1. `C_4`: `2^100` → direct atom ceiling | 25.65 e-folds | **ALREADY BANKED** on 2026-08-19 as `C_4'=2^62+1`, twice refereed |
| 2. finite tag count: `2^20` → `82944` | 2.54 e-folds | **RESIDUAL — executed here** |

The re-referee is explicit that target 2 was *not* taken:

> "an independent 120-digit assembly confirms that the only banked reduction is
> C4: 2^100 -> 2^62+1"
> — `CR_REDUCTION_REREFEREE.md`, Summary

So the autopsy is stale on target 1 and correct on target 2.

---

## 2. The double-counting question, resolved

The brief flagged the central hazard: *if the `2^63` bridge constant already
contains the `2^20` tag ceiling, does target 2 stack or double-count?*

**Answer: it does NOT stack additively — it is a further reduction of the same
subtotal, applied by substitution inside it. It is not double-counted.**

Proof, from the bridge's own assembly. `ATOM_MOMENT_BRIDGE_SOL.md:455-470`
displays the outside-factor product (3.25):

\[
 \underbrace{2^{12}}_{\text{core convolution}}
 \underbrace{2^{20}}_{\text{all tags}}
 \underbrace{2^{11}}_{40^2<2^{11}}
 \underbrace{2^4}_{\text{four zeta sums}}
 =2^{47}.
 \tag{3.25}
\]

The tag ceiling `2^20` occurs **exactly once**, as a **multiplicative** factor,
in forming `2^47`. The bridge then adds one ordering bit and the high-regime
factor `2^14` (3.24) to reach

\[
 2^{47+14+1}=2^{62},
 \tag{3.26}
\]

and Ford's unit count (3.28) adds `+1`, giving `C_atom = 2^62+1 < 2^63`
(`ATOM_MOMENT_BRIDGE_SOL.md:480-490`). The bridge's own constant ledger
(`:496-506`) lists the same dependency explicitly as a row
"complete finite tag set (3.9) | `2^20`" feeding "direct `A_X^2` subtotal |
`<2^62`".

Therefore the `2^20` is **inside** `2^62`, and the exact count (3.9)

\[
 4^2\,3^4\,2^3\cdot4\cdot2=82944<2^{17}<2^{20}
 \tag{3.9}
\]

replaces it **in place**. There is nothing to add on top; there is a factor to
divide out. Since `82944 = 2^10·3^4` exactly, the improvement factor is
`2^20/82944 = 1024/81 = 12.641975…`, i.e. `ln(1024/81) = 2.5370226509…`
e-folds — matching the autopsy's stated 2.54 to its printed precision.

Receipt:

```
tag_exact = 4^2*3^4*2^3*4*2 = 82944
82944 == 2^10*3^4 : True
outside_factor_exact = 2^12*82944*2^11*2^4 = 11132555231232 = 2^37*81: 11132555231232
high_regime_exact = 2^37*81*2^14*2 = 364791569817010176 = 2^52*81: 364791569817010176
C4_new = 2^52*81+1 = 364791569817010177
ln(1024/81) = 2.5370226509270143285913402668916628621650391123115547342680227603839590468225 +/- 2.31e-200
```

### 2.1 Substitution theorem

**Theorem (tag-exact atom coefficient).** Under the identical hypotheses,
coding conventions, injectivity factors and index ranges of `(AM)` as proved
in `ATOM_MOMENT_BRIDGE_SOL.md` §3, the displayed conclusion (3.27)–(3.28)
holds with the coefficient `2^62+1` replaced by

\[
 C_4''=2^{52}\cdot81+1=364791569817010177 .
\]

*Proof.* The `(AM)` derivation uses the tag ceiling at exactly one point,
(3.25), and only through the inequality "number of finite tags `< 2^20`". By
(3.9) the complete tag set has cardinality exactly `82944`, and (3.9) is proved
in the same note from the same enumeration, with the same one-mark/two-mark
selector as its last factor and the same absorption/read-back argument
guaranteeing no unrecorded length parameter (`:245-252`). Substituting the
exact cardinality for its own upper bound in the single place it is used gives
outside factor `2^12·82944·2^11·2^4 = 2^37·3^4`. Carrying the same ordering bit
and the same `2^14` of (3.24) gives high regime `2^52·81`; the same route with
`2^11` of (3.19) gives low regime `2^49·81`, which is smaller, so the single
displayed coefficient is the high-regime one, `2^52·81`. Ford (3.28) adds `Y^2`
exactly as before, contributing `+1`. No other step of §3 references the tag
count. ∎

**Convention match.** The substitution is *internal to one note*: it changes a
bound to the exact value it was derived from, inside `(AM)`'s own §3, with no
re-coding, no change of index range, and no change of injectivity factor.
There is therefore **no convention drift to bridge** — this is strictly weaker
than the cross-note match the brief anticipated. The cross-note direction
(`(AM)` → RATE-A) was already established and refereed on 2026-08-19; §3 below
re-verifies it mechanically rather than re-arguing it.

---

## 3. Convention lock: the chain reproduces all three prior constants

RATE-A's assembly is (`BOUNDARY_ALPHA_THEOREM_SOL.md:140-191,510-579`):

\[
 C_R=\Big\lceil M_0\big(C_{\rm pair}+C_{\rm wrap}\big)\Big\rceil,\qquad
 C_{\rm pair}=2\pi^2(S+1)\,p\,C_4\,F(12),\qquad
 C_{\rm wrap}=p\cdot128(1+\log 2)\cdot30,
\]

with `p=11/5`, `S=7.648`, `M_0=2.775`, `F(12)=1225/4+91605/12=7940`. The chain
is **positive and linear in `C_4`**, every other input fixed.

I implemented this chain once, at `ctx.dps=200`, and fed it three values of
`C_4` without touching any other step. Command:

```bash
PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import arb, ctx
ctx.dps = 200
def CR_of(C4):
    p    = arb(11)/5
    S    = arb('7.648')
    M0   = arb('2.775')
    F    = arb(7940)
    Cpair = 2*arb.pi()**2*(S+1)*p*C4*F
    Cwrap = p*128*(1+arb(2).log())*30
    tot   = M0*(Cpair+Cwrap)
    c = arb(tot.upper()).ceil()
    return int(str(c).split('.')[0]), tot
for name, C4 in (('C4=2^100 (published)', 2**100),
                 ('C4=2^62+1 (banked)',   2**62+1),
                 ('C4=2^52*81+1 (new)',   2**52*81+1)):
    v, tot = CR_of(C4)
    print(f'{name:26s} -> C_R = {v}')
PY
```

Complete stdout:

```text
C4=2^100 (published)       -> C_R = 10489412368759562746433608215977724802
C4=2^62+1 (banked)         -> C_R = 38160259896392973127946053
C4=2^52*81+1 (new)         -> C_R = 3018536183210772296097745
```

The first line reproduces the **published** RATE-A constant
(`BOUNDARY_ALPHA_THEOREM_SOL.md:579`) digit-for-digit. The second reproduces
the **banked refereed** constant (`CR_REDUCTION_SOL.md` §0) digit-for-digit.
Two independent exact hits from one unmodified implementation is the convention
receipt: my chain is in the same convention as both prior results, and the only
thing that moved is `C_4`.

### 3.1 The corrected constant

\[
 \boxed{C_R''=3018536183210772296097745}
\]

\[
 \log C_R''=56.366814238189097078451729806169290097691480385731\ldots
\]

### 3.2 Outward rounding and ceiling minimality

Both the interval upper endpoint and the one-less integer were checked, so the
ceiling is an upper bound and is the least such integer.

```text
tot_lower= 3018536183210772296097744.83302092424861444146809550183635495093336361490738063898320041178334587609024722278375114316988464 +/- 3.39e-176
tot_upper= 3018536183210772296097744.83302092424861444146809550183635495093336361490738063898320041178334587609024722278375114316988464 +/- 4.88e-177
ceil_is_upper_bound  (CR >= tot): True
ceil_is_minimal (CR-1 < tot):     True
```

All roundings are outward: the ceiling is taken from the interval **upper**
endpoint, so `C_R''` upper-bounds the true assembly.

### 3.3 Reduction achieved

```text
log_CR_new       = 56.366814238189097078451729806169290097691480385731...
log_CR_banked    = 58.903836889116111404506509526071627432519963742500...
log_CR_published = 85.243429750394033162143449533297358736094213311298...
efolds_vs_banked    = 2.53702265092701432605477971990233733482848335676...
efolds_vs_published = 28.87661551220493608369171972712806863840273292556...
ln(1024/81)         = 2.53702265092701432859134026689166286216503911231...
```

The gain over the banked constant agrees with `ln(1024/81)` to 18 significant
figures; the residual difference is exactly the expected effect of the additive
wrap term, the `+1` Ford unit, and the integer ceiling — all of which are
retained unchanged. This is a self-consistency check on the substitution, not
an independent input.

---

## 4. Propagated conditional A0 transport cutoff

I replayed `R5_ACTIVATION_CLOSURE_SOL.md` §3–§4 **byte-identically**, changing
only the single line `CR = arb(...)`. All fixed inputs kept: `alpha=6/5`,
`nu=0.1552=97/625`, `m=0.0439`, `K_+=117`, `beta=alpha*nu=582/3125`,
`T=((1-nu)·log K_+ - log m)/beta + (log C_R)/alpha`, `q_A0=floor(exp(T))+1`
computed from the unrounded Arb interval with lower/upper floor agreement
asserted.

**Cross-check first.** Fed the *banked* constant, my replay must return the
integer the cold referee certified:

```text
published q_A0 = 332093267419812025416641789732742045430624465595
banked    q_A0 = 97418971860452658435229799565334786148
new       q_A0 = 11761546420922598622910053339543258496
referee_banked_target = 97418971860452658435229799565334786148
```

The banked line reproduces `CR_REDUCTION_REFEREE.md` Summary
("the primary A0 strict integer is exactly `97418971860452658435229799565334786148`")
exactly, and the published line reproduces
`R5_ACTIVATION_CLOSURE_SOL.md` §4 stdout (`q_transport=3320932674198120254166417897327420454306244655\
95`) exactly. Convention lock holds on the A0 leg too.

**Full replay at `C_R''`, complete stdout:**

```text
T_side= [43.0038669194927841330064599089657667363260261044378878503078806491231687655605940306698233008894169666783281895099806211 +/- 4.90e-119]
floor_exp_T_side_lower= 4746157036282968394
floor_exp_T_side_upper= 4746157036282968394
q_side= 4746157036282968395
side_minimality_log_q_gt_T_side= True
side_minimality_log_q_minus_1_le_T_side= True
ER_at_q_side_lt_Kplus= True
T= [85.3578987799887436740434637985978175532746109888166112059459568248335005615955499864756820623734029223926959591750712536 +/- 5.66e-119]
floor_exp_T_lower= 11761546420922598622910053339543258495
floor_exp_T_upper= 11761546420922598622910053339543258495
q_transport= 11761546420922598622910053339543258496
minimality_log_q_gt_T= True
minimality_log_q_minus_1_le_T= True
ER_nonzero_branch_lt_Kplus= True
A0_envelope_at_q_transport_upper= [0.04389999999999999999999999999999999999981027575908442172237117998433590868797851161921993146289719130753665995176549754 +/- 2.90e-122]
A0_strict_lt_m= True
q_side_lt_q_transport= True
q_transport_ge_q_RATE= True
q_transport_ge_q_divisor= True
log_q_transport= [85.3578987799887436740434637985978175532978161901434780353375787768233511807811574019308700002574548040656765832096990392 +/- 1.91e-119]
```

### 4.1 Result

\[
 \boxed{q_{A0}''=11761546420922598622910053339543258496},
 \qquad \log q_{A0}''=85.35789877998874367404346379859781755329\ldots
\]

Both floor endpoints agree, and both minimality lines hold, so this integer is
exactly `floor(exp(T))+1` and is the least integer satisfying the strict
condition. The A0 envelope at the cutoff is `< m = 0.0439` strictly, and both
side-branch and `q≥q_RATE=12`, `q≥q_divisor=3` gates pass, as in the source.

### 4.2 Label

Exactly as the source labels it: this is a **selected, conditional A0
analytic-tail transport cutoff**. It is **not** a final `q_0`, not a finite
all-`q` threshold, and not a full-program bound. The other gates stand
unchanged.

**`q_monotone` is KEPT.** Per the 2026-08-20 referee-D7 correction block at
`R5_MONOTONICITY_GATE_SOL.md:803-829`, the earlier "`q_monotone` is removable"
claim is **REFUTED on three independent grounds**, and its PROVED row was
downgraded. The onset ledger therefore retains the term:

\[
 q_0=\max\{12,\;q_{\rm RATE},\;q_{\rm transport},\;q_{\rm divisor},\;q_{\rm geometry},\;q_{\rm monotone},\ldots\}
\]

Nothing in this note bears on `q_monotone`, and this note does not remove it.

---

## 5. What is NOT claimed

Explicitly, none of the following is claimed, implied, or banked here:

1. **No gate is closed.** No program gate moves from open to closed.
2. **No unconditional threshold.** `q_{A0}''` is conditional on the same
   paper-level Route-B / Ford / two-mark premises as its source, and inherits
   every one of them.
3. **Not a final `q_0`.** It is one term in a `max`, not the max.
4. **`q_monotone` is not removed** (§4.2); the refutation stands.
5. **No theorem-ledger promotion.** `C_R''` is an *unbanked candidate*
   constant pending a cold referee, exactly as `C_R'` was before its two
   referees.
6. **The published RATE-A theorem is untouched.** Its `C_R` and its declared
   `C_4=2^100` remain valid upward-valid constants; this note does not rewrite
   them.
7. **The banked `C_R'` is untouched.** `CR_REDUCTION_SOL.md` is left exactly as
   refereed.
8. **No machine formalization**, and **no certified full-operator enclosure** —
   both remain open per `RATE_A_REFEREE.md:305-307,369-392` and
   `AM_REFEREE.md:360-408`.
9. **No finite base block**, and **no standalone N1-RATE** — open/conjectural
   as before.
10. **No claim that `2^52·81+1` is optimal.** It is the exact-tag substitution
    only. Other factors in (3.25) (`2^12`, `2^11`, `2^4`) and the `2^14` of
    (3.24) are themselves roundings that were **not** examined here; further
    reduction may well be available. Any such further gain is **CONJECTURAL**
    and is not quantified in this note.

### 5.1 Explicitly CONJECTURAL

- That the remaining powers-of-two in (3.19), (3.24) and (3.25) admit exact-value
  substitution of the same kind. **CONJECTURAL** — not attempted, not estimated.
- That `p=11/5` is a good choice; the autopsy's sensitivity remark about
  `F(12)=7940` being driven by `p-2=1/5` is **CONJECTURAL** and is *not* a
  repair, because changing `p` also changes the decay exponent `alpha`, which
  propagates into the A0 formula. Not pursued here.

### 5.2 Observation for the referee (not a claim)

`BOUNDARY_ALPHA_THEOREM_SOL.md` now hashes
`1a5a96e6e2a5ca76a917a7e20e8458038e43e5609139b70624ab5a59b8e13c59`, whereas
`CR_REDUCTION_REFEREE.md` recorded `58441b334a5f279aae6298e3b5383ef5677b3e6e\
c6e7d5bc6a908a4936111e6e` on 2026-08-19. The file changed between the two
dates. I read the **current** version; its `C_R`, its chain at `:510-579`, and
its `C_4=2^100` are unchanged, and my §3 reproduction of the published constant
confirms the load-bearing content is intact. I did not audit what else changed.

---

## 6. Source receipt

Command:

```bash
git rev-parse HEAD && shasum -a 256 research_notes/rh_goals_2026-08-14/lane_g/{BOUNDARY_ALPHA_THEOREM_SOL,ATOM_MOMENT_BRIDGE_SOL,AM_REFEREE,CR_REDUCTION_SOL,CR_REDUCTION_REFEREE,CR_REDUCTION_REREFEREE,R5_ACTIVATION_CLOSURE_SOL,R5_MONOTONICITY_GATE_SOL,CR_AUTOPSY_LUNA}.md
```

Output:

```text
708eafb9c5a8730c6acc0b1fe16e7e389ce23161
1a5a96e6e2a5ca76a917a7e20e8458038e43e5609139b70624ab5a59b8e13c59  BOUNDARY_ALPHA_THEOREM_SOL.md
59ce32f7c6fa86580055d9049e609a2189ecc1645528dd4136758fcf547fbbbb  ATOM_MOMENT_BRIDGE_SOL.md
3d655f2c05395688be73e8786cd9a954182cc4842005ff9e7662d05cccf503b4  AM_REFEREE.md
89fc61e9bc33db55c95856f5412e87c45da72d3623616435575fb494321b3417  CR_REDUCTION_SOL.md
f0f71f09c1c4547805c44f4c649c12a26568fa0f2e8843a90d574ea856dcfa5a  CR_REDUCTION_REFEREE.md
00cebb30a7370e5487575c181be1878d37ea1a99a9ff8fdacbbdeb05f1898de6  CR_REDUCTION_REREFEREE.md
3b49d73d56cf963703137a6494f1f733fbb208d36c0afbe1affbd5d700ab2a53  R5_ACTIVATION_CLOSURE_SOL.md
162f1cdb564a986460a4c7a79da8101c68d89ceff867692f2a0750b2f4dbcf88  R5_MONOTONICITY_GATE_SOL.md
e9b7303326c08a4263614a68c1d4ce9e1051ffe539ff7a12eea226e5e2289171  CR_AUTOPSY_LUNA.md
```

Environment:

```text
py 3.13.13 flint 0.9.0
```

---

## 7. Summary table

| quantity | published | banked (2026-08-19) | this note |
|---|---|---|---|
| `C_4` | `2^100` | `2^62+1` | `2^52·81+1 = 364791569817010177` |
| `C_R` | `10489412368759562746433608215977724802` | `38160259896392973127946053` | `3018536183210772296097745` |
| `log C_R` | `85.2434297503…` | `58.9038368891…` | `56.3668142381…` |
| conditional A0 cutoff `q` | `3320932674198120254166417897327420454\`<br>`30624465595` | `97418971860452658435229799565334786148` | `11761546420922598622910053339543258496` |
| `log q` | `109.4217450401…` | — | `85.3578987799…` |
| status | banked theorem | banked, twice refereed | **unbanked candidate** |

Cumulative reduction from published: **28.877 e-folds** in `C_R`, of which
26.340 was banked on 2026-08-19 and **2.537 is new here**.

READY FOR JUDGING

---

## Dated correction block (2026-08-20, referee D1–D3, append-only)

Applied per CR_REDUCTION_V2_REFEREE.md (final verdict CONFIRMED,
documentation repairs only; no number moves).

### Correction (2026-08-20, referee D1): 82944 is a BOUND, not an exact cardinality

Defective phrasing in §2/§2.1 and the title: "the complete tag set has
cardinality exactly 82944", "Substituting the exact cardinality", "the
exact finite tag count".  The source, ATOM_MOMENT_BRIDGE_SOL.md:245,
proves only "The total tag count is bounded explicitly by
4^2 3^4 2^3·4·2 = 82944 < 2^17 < 2^20" — an upper bound whose factors
are themselves at-most enumerations.  Corrected statement: every
occurrence of "exact cardinality"/"exactly 82944"/"exact finite tag
count" in this note is to be read as "the smaller explicit tag BOUND
82944 from (3.9)".  The substitution remains valid (a smaller proved
upper bound replacing a larger one; inequality direction safe); only
the exactness claim is withdrawn.  Disclosure added to the NOT-claimed
list: 82944 is itself an upper bound, not a proved count.

### Correction (2026-08-20, referee D2): "byte-identical" replay overstated

Defective sentence in §4: the source program was replayed
"byte-identically, changing only the single line CR = arb(...)".
False as literally stated: the replay program dropped eight print
statements (alpha=, nu=, alpha_nu=, beta_exact=, q_RATE=, q_divisor=,
ER_at_q_side_upper=, ER_at_q_transport_upper=) and added one
(log_q_transport=).  Corrected statement: the same program as
R5_ACTIVATION_CLOSURE_SOL.md §4 with the CR line changed and the print
set trimmed/extended as listed; every computed quantity was verified
unchanged by the referee's independent run (referee Attack 3, all
integers and gates reproduced).

### Correction (2026-08-20, referee D3): q_side propagation stated in prose

Omission in §4: the reduction also moves q_side.  Propagated values,
from the same replay (referee-verified): q_side'' = 4746157036282968395
(down from the banked 39311645103099547636 and published
134010166814705707171424895246), and the literal ledger (0.2) of
R5_ACTIVATION_CLOSURE_SOL.md, q_{0,analytic} = max{q_RATE, q_divisor,
q_side, q_transport}, therefore evaluates at the V2 constant to
q_{0,analytic}'' = 11761546420922598622910053339543258496 — still a
CONDITIONAL analytic-tail quantity, one term of the full max; q_monotone
and all other gates unchanged and KEPT.
