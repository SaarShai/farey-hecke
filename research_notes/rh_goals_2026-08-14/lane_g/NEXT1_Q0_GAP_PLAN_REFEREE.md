# Cold referee report: `NEXT1_Q0_GAP_PLAN_SOL.md`

**Date:** 2026-08-22
**Target:** `research_notes/rh_goals_2026-08-14/lane_g/NEXT1_Q0_GAP_PLAN_SOL.md`
(612 lines, commit `662f93a`, self-graded UNREFEREED/CONJECTURAL throughout)
**Referee:** independent, no shared context with the author of the target.
**Mandate:** attempt to REFUTE. Re-derive every number from the cited sources,
not from the target.
**Interpreter:** `/Users/za/.venvs/farey-rh/bin/python` (Python 3.13.13,
mpmath at `dps=25..60`, numpy float64 for the mode sums).
**Independent legs written from the sources, not from the target's scripts:**
an mpmath leg for the `C_R`/`T`/`T_0` assembly and all elasticities; a numpy
leg for the rectangle harmonic measure; an mpmath leg for `phi_infty`.
The target's scratchpad scripts (`alpha_rung2..6.py`, `final.py`, `mz.py`,
`joint.py`) were read **only after** my own numbers were produced, and only to
diagnose the origin of the discrepancies recorded in D1-D4 below.
**Write scope:** this file only. No existing file read-modified, renamed or
deleted. No commit, no push.

---

## 0. House verdict

> **CONFIRMED-with-corrections on Claims 1-3. Claim 4 (the gate audit) is
> REFUTED as stated.**
>
> The two load-bearing analytic findings are correct and I reproduce them
> exactly: (i) the banked `-85.4` alpha-elasticity **is** identically
> `-log Q_0` under frozen parameters, so it measures size and not achievable
> reduction; (ii) `alpha` is not a free parameter, `alpha = 2*sigma - 1`, and
> `alpha*nu_z` is exactly `2*(Re z_0 - r_z - 1/2)` in the strip limit. The
> executed rung's `-0.5719 log10` at `sigma = 1.16` and the joint optimum
> `log10 Q_0 = 18.7911` both reproduce **digit-for-digit** on my independent
> legs. The programme-level conclusion (levers do not bridge to `q<=21`; a
> finite-base theorem is required) is correct and I reach it independently.
>
> Against that: **eight of eight `file:line` receipts in the section 1.4 gate
> table point at the wrong lines**; the R8 quote elides the clause that ties
> the open Scope-2 blocker to a family-uniform `K_+`; the section 1.5.3 table
> mixes three incompatible computational conventions and its `sigma = 1.48`
> row is a composite of three different runs with three wrong cells; the
> section 1.6 `m_z` table row labelled `r_z = 0.025` is in fact `r_z = 0.026`;
> the L5 evidence cell `-25.5` is wrong by a factor `ln 10` (correct:
> `-11.07`); and section 1.7.6, which advertises itself as a **complete** list
> of frozen inputs, omits (H-HOL), the `H`-axis of the section 2-4 chain, and
> the fact that the `H_0` underwriting `K_+ = 117` is only `+/-0.9999` tall
> against the proposed `H = 6`.
>
> No banked constant is threatened. Nothing in the note licenses a status
> change, and the note does not claim one. **Required repairs: D1-D9 below
> before any number from sections 1.5-1.6 is quoted outside this file.**

---

## 1. What reproduced exactly (independent legs)

### 1.1 The banked assembly (basis for everything downstream)

I rebuilt the `C_R` assembly from `BOUNDARY_ALPHA_THEOREM_SOL.md` (3.15),
(4.1), (4.2), section 10 and `M3_UNIFORMITY_EXECUTION_SOL.md`, without reading
the target's code:

```
C_R = M_0 * [ 2*pi^2*(S+1)*p*C_4*F(12) + p*128*(1+log2)*G(p) ]
F(q)=1/(3-p)+J_2(p)+J_4(p)/q,  M_0 = B(sigma-1/2, 1/2),  S = sup_{Gamma_R}|s|
```

At `p = 11/5`, `S = 7.648`, `M_0 = 2.775`, `C_4''' = 65459394456774532`:

```
C_R  = 541656022363559883954520          == C_R'''            [exact]
log C_R = 54.648918107756483474          vs banked 54.648918107756483473
F(2.2,12) = 7940.0  (zero slack, matches (4.1))   G(2.2) = 30.0
```

and at `C_4'' = 364791569817010177` it returns `C_R'' =
3018536183210772296097745` exactly. **The target's section 1.5.1(3) formula is
the banked assembly. CONFIRMED.**

Propagating through `T` (R5 (5.1)) with `K_+=117, nu=0.1552, m=0.0439,
alpha=6/5`:

```
T_0 = 38.38555358149782944200036    e^{T_0} = 46841857142466893.056
                                    log10 e^{T_0} = 16.6706341052
C_R'''  ->  T = 83.92631867129489900327788   log10 Q_0 = 36.448737085397228488
            q_A0''' = 2810199067910634377586449487575862960   [exact]
            q_side''' = 1134004458443795841                   [exact]
C_R''   ->  T = 85.35789877998874367404346   log10 Q_0 = 37.070464427005422697
1/(alpha*nu) = 5.369415807560137457   (1-nu)/(alpha*nu) = 4.536082474226804124
```

R1, R2, R3, R4, R6 all check. The section 1.2 split
`log10 Q_0 = 16.6706 + 19.7780` is `16.6706341 + 19.7781030`; the second term
is truncated, not rounded, and the printed sum `36.4487` is 1 ulp above the
printed addends (see N3).

### 1.2 The harmonic measure and `phi_infty`

Written from scratch from the geometry in `R3_TRANSPORT_EXECUTION_SOL.md:22-52`
and the `phi_infty` formula at `EFFECTIVE_THEOREM_ASSEMBLY_SOL.md:80-81`:

```
omega(x,y) = sum_{n odd} (4/(n pi)) sin(n pi y/H) sinh(n pi x/H)/sinh(n pi w/H)
nu_z(sigma=1.1, H=1, r_z=1/8) = 0.1552145055111849     [target: identical]
   argmin at theta = pi (leftmost point of dD_z)
   stable to 5 significant figures under 720 / 1440 / 5760 / 46080 points
m_z(1/8)  = 0.0444413749  (M=11520)   0.0444414999 (M=720, = target's value)
m_z(1/40) = 0.0119011543  (M=11520)   0.0119011586 (M=720)
|phi_infty'(z_0)| = 0.51447259  (consistent with m_z/r_z -> 0.5145)
sup_{Gamma_R}|s| = 7.64689324359665   -> ceil3 = 7.647  (valid UP)
```

Calibration (target section 1.5.2) reproduces on my leg:
`log10 C_R = 23.733673`, `log10 Q_0 = 36.448695` at `nu = 0.1552`, banked
`36.44873708`. The residual `4.21e-5` is explained by `S = 7.647` vs banked
`7.648`: `(S+1)` relative gap `1.157e-4`, times `5/6`, is `4.19e-5`. The
target's intermediate `1.28e-4` is wrong; its conclusion is right.

### 1.3 The load-bearing results

Every one of these reproduced on my leg to the printed digit:

| target claim | my value | verdict |
|---|---|---|
| L1 `H: 1 -> 6` at `sigma=1.10, r=1/8` | `31.8277` (`-4.5913`) | EXACT |
| L2 `r_z: 1/8 -> 1/40` at `sigma=1.10, H=1` | `29.4456` (`-6.9734`) | EXACT |
| L1+L2 | `27.0186` (`-9.4004`) | EXACT |
| joint `sigma=1.48, H=6, r=1/40` | `18.7911` (`-17.6279`) | EXACT |
| joint `nu_z = 0.22953`, `m_z = 0.01190`, floor `7.8197` | identical | EXACT |
| rung min `sigma=1.16, alpha=1.32` -> `35.8768` (`-0.5719`) | identical | EXACT |
| rung sensitivity `(1-nu)/(alpha nu) = 5.1334`, `1.29x` | `5.13340`, `1.2924x` | EXACT |
| joint sensitivity `1.713`, `2.0e10` | `1.71262`, `1.96e10` | EXACT |
| L4 `d log Q_0/d log K_+ = 4.5361`, `117->10` buys `-4.84` | `4.536082`, `-4.84538` | EXACT |
| `alpha*nu_z` at joint `0.4499` vs `0.1863`, `2.4x` | `0.44988` / `0.18626`, `2.415x` | EXACT |
| section 1.7.6 `H < gamma_2-gamma_1 = 6.888` | `6.887314` | EXACT |
| section 1.8 "seventeen orders" vs `q<=21` | `18.79 - 1.32 = 17.47` | EXACT |
| bonus: `r_z=1/40` gives `0.725 <= Re s_q <= 0.775` | exact | EXACT |

**Strengthening the target does not claim.** L4's `-4.84` is not a
linearization: `T` is *exactly* affine in `log K_+` with slope
`(1-nu)/(alpha nu)`, so `-4.84538` is exact for the whole `117 -> 10` move. I
also checked the term the target never checks: at `K_+ = 10`,
`log10 q_side = 18.945 < 31.603 = log10 q_A0`, so `q_A0` still binds and the
`max` does not change hands. Same check at the joint point:
`log10 q_side = 9.916 < 18.791`. Both pass.

---

## 2. Claim-by-claim verdicts

### CLAIM 2 (the elasticity artifact) - **CONFIRMED, and understated**

With `nu_z, m_z, K_+, C_R` frozen, `log Q_0 = A/alpha`, hence identically
`alpha * d(log Q_0)/d(alpha) = -log Q_0`. My leg:

```
alpha*dlogQ0/dalpha  at C_R''  = -85.357898779988743674  == -T''
alpha*dlogQ0/dalpha  at C_R''' = -83.926318671294899003  == -T'''
```

`-85.358` is the banked figure at `EFFECTIVE_THEOREM_ASSEMBLY_SOL.md:701-707`
and `EFFECTIVE_THEOREM_ASSEMBLY_REREFEREE.md:395`. **CONFIRMED.**

*Dimensional check requested by the mandate.* The quantity is `-ln Q_0`
(natural log), `85.358`, not `-log10 Q_0 = -37.070`. The elasticity itself is
base-free (`alpha d(log_b Q_0)/d alpha = -log_b Q_0` in every base `b`); the
banked *number* `-85.4` is the natural-log instance, and the target's
identification with "the banked `log q_A0''` = 85.3579" is right because the
whole `CR_REDUCTION`/`BOUNDARY_ALPHA` chain writes `log` for `ln`
(`CR_REDUCTION_V3_REFEREE.md:173-174`, `T = 85.35789877998874367404`). Strictly
the identity is `-T`, not `-ln q_A0''` (which is `T` plus the `floor+1`
increment); the two agree to 30 digits.

**The target understates its own finding.** The same artifact governs R7's
*comparator*: `alpha * dT_0/dalpha = -T_0 = -38.3856` is likewise identically
minus the floor. So R7/D2's headline comparison `-85.4` (alpha, full `Q_0`)
against `-38.4` (alpha, floor) is a comparison of two *sizes* of two different
objects, and the only non-artifact number in D2 is
`nu*dT_0/dnu = -log(K_+/m_z)/(alpha nu_z) = -42.354031860`. The apples-to-
apples frozen comparison at the full `Q_0` is `-85.358` (alpha) against
`-42.354` (nu), which is what D2's steering sentence actually rests on. The
target should say this; it strengthens its case.

### CLAIM 2b (`alpha = 2 sigma - 1`, and `alpha*nu_z` strip invariance) - **CONFIRMED, with one refuted inference**

`alpha = p - 1`, `p = 2 sigma` is `BOUNDARY_ALPHA_THEOREM_SOL.md:237` /
`:254` / `:529`, and the layer cake (3.10) is stated for `2 < p < 3` at `:433`.
So `1 < sigma < 3/2` and `alpha in (1,2)`. **CONFIRMED.**

Strip limit: `omega(x) = x/w`, `nu_z -> (Re z_0 - r_z - 1/2)/w`, `alpha = 2w`,
so `alpha*nu_z -> 2*(Re z_0 - r_z - 1/2)`. Numerically at `H=6, r_z=1/40`:
`alpha*nu_z = 0.44999` at `sigma=1.10` and `0.44988` at `sigma=1.48`, against
the strip value `0.45`. **CONFIRMED.**

**REFUTED inference (D5).** Section 1.6 concludes from this that raising
`sigma` past the strip threshold costs nothing: *"raising sigma raises alpha at
NO cost in alpha*nu_z, so the (log C_R)/alpha term shrinks with nothing pushing
back."* There **is** pushback. At fixed `alpha*nu_z = 2d`,

```
T_0 = log(K_+/m_z)/(2d) - log(K_+)/alpha,
```

which is strictly **increasing** in `alpha`. From `alpha=1.2` to `alpha=1.96`
the floor rises by exactly `log(K_+)*(1/1.2 - 1/1.96)/log 10 = 0.66829 log10`
- and the target's own table shows it (`7.1493 -> 7.8197` in the `H=6,
r_z=1/40` rows, difference `0.6704`, the remainder being the `nu_z` residual
off the exact strip limit). The net move is still favourable, so no ranking
changes; but the sentence as written is false and the note's own numbers
contradict it.

### CLAIM 3 (the executed `alpha` rung) - **CONFIRMED**

Under the note's own stated method (`M_0(sigma)` recomputed, `S` ceiled to
3dp, `nu_z` floored to 4dp, `m_z = 0.0439` banked, `H=1`, `r_z=1/8`) my
independent leg returns, for `sigma = 1.10 .. 1.20`:

```
sigma   alpha   nu_z(raw)   log10 C_R   log10 Q_0   [target]
1.10    1.20    0.155215    23.7337     36.4487     36.4487
1.12    1.24    0.145802    23.3610     36.1200     36.1200
1.14    1.28    0.136960    23.0508     35.9423     35.9423
1.16    1.32    0.128654    22.7870     35.8768     35.8768   <- min
1.18    1.36    0.120850    22.5586     35.9184     35.9184
1.20    1.40    0.113518    22.3587     36.0522     36.0522
```

Six rows, six exact matches. `-0.5719 log10` (factor `3.73`) at
`sigma = 1.16`. **CONFIRMED.**

Floor rise: `16.6706 -> 18.6139`, `+1.9433 log10`. Reproduced exactly under
the `(nu` 4dp`, m=0.0439)` convention; under section 1.6's declared convention
(`nu` 5dp, `m=0.04444`) it is `16.6409 -> 18.5748 = +1.9339`. Either way
`+1.93/+1.94`. **CONFIRMED.**

Constrained elasticity `-24.9`: my central difference gives
`d(log10 Q_0)/d(sigma) = -18.03` at `sigma = 1.1`, i.e.
`d(log Q_0)/d(sigma) = -41.5`, and `alpha*d(log Q_0)/d(alpha) = 1.2*(-41.5)/2
= -24.9`, vanishing between `sigma = 1.16` and `1.17`. **CONFIRMED.**

But see D2: this section's *table* is not internally consistent.

### CLAIM 1 (the lever ranking) - **CONFIRMED-with-corrections**

The five headline reductions (`-4.59`, `-6.97`, `-9.40`, `-4.84`, `-17.63`)
all reproduce exactly (section 1.3 above). The **ranking conclusion** - the
geometry levers L1/L2 dominate, L3 is not a standalone lever, L5 is spent -
survives every check I ran, and I reach it independently.

Corrections: D1-D4 and D8 below. One of them (D8) is a straight arithmetic
error in a cell presented as evidence; the other four are convention errors
that leave every headline number intact.

### CLAIM 4 (gate audit: "7 of 8 dischargeable, (H-SIDE) the one open gate") - **REFUTED as stated**

See D6, D7, D9. My independent read of the same sources:

| gate | source status (with actual line) | my read |
|---|---|---|
| (H-RATE) Sc.1 | "CONFIRMED-conditional (paper level), **WITH A LIVE LEDGER CONFLICT**" `:165`, superseded to plain "CONFIRMED-conditional (paper level)" at `:748` | **dischargeable ONLY IF** the M1 conjectural `O(q^{1-2 sigma})` piece is not consumed - unresolved in the banked ledger (D7) |
| (H-HOL) | "PROVED from printed theory" `:213` | DISCHARGED **for the banked domains only** (D9) |
| (H-C4) | `CR_REDUCTION_V3_REFEREE` "Required repairs: none" `:864`, but same referee: "**No gate moves.** `q_monotone` stays. This is not a final `q_0`" | **NOT** dischargeable by a banking act (D6c) |
| (H-ROUTE) | "PROVED (domain correction), and BINDING" `:300` | DISCHARGED (constraint, honoured) |
| (H-GEOM) | "PROVED (Arb interval cover)" `:235` | DISCHARGED at banked geometry; float-only at any new one |
| (H-SIDE) | "CONFIRMED-conditional source input" `:255` | GENUINELY OPEN - agreed |
| (H-TRANS) | "ANALYTIC CORE REFEREED-CONFIRMED at the stated conditional scope" `:820` | dischargeable (formalization) - agreed |
| (H-REFL) | "PRINTED-LITERATURE, same tier as (H-RATE)'s printed inputs" `:766` | **PRINTED-LITERATURE, not discharged** (D6d) |

Clearly discharged or dischargeable-by-formalization: (H-HOL), (H-ROUTE),
(H-GEOM), (H-TRANS) - **four**, with (H-RATE) Scope 1 conditional on D7.
"Seven of eight" is not supported.

---

## 3. Defect list (required repairs)

### D1 - section 1.5.3 mixes three computational conventions inside one table

The `log10 C_R` column and the two `log10 Q_0` columns do not come from the
same computation. Reproducing each convention on my leg:

| sigma | `log10 C_R` printed | my `M_0(sigma)` recomputed | my `M_0` **frozen at 2.775** |
|---|---|---|---|
| 1.06 | 24.7809 | **24.8011** | 24.7810 |
| 1.08 | 24.1866 | **24.1966** | 24.1867 |
| 1.10-1.20 | (agree) | agree | - |
| 1.30 | 21.7264 | **21.6449** | 21.7264 |

So rows `1.06`, `1.08`, `1.30` were produced with `M_0` **frozen** at the
`sigma = 1.1` value `2.775`, in direct contradiction of section 1.5.1(3),
which argues at length that recomputing `M_0(sigma) = B(sigma-1/2, 1/2)` "is
legitimate rather than a freeze". Worse, the **frozen-`nu_z` column is frozen-
`M_0` at every `sigma`** while the honest column is recomputed-`M_0`: e.g. at
`sigma = 1.16` the printed `32.4388` is the frozen-`M_0` value and
`32.4180` is the recomputed one. The two `Q_0` columns of a single row are not
comparable.

Direction: for `sigma < 1.1`, `M_0(sigma) > 2.775`, so freezing **understates**
`C_R` - the rows are optimistic by `0.018` and `0.009 log10`. For
`sigma > 1.1` it overstates, so row `1.30` is pessimistic by `0.051`.
No conclusion moves. **Repair: recompute the whole table on one convention.**

### D2 - section 1.5.3's `sigma = 1.48` row is a composite of three different runs; three of its four cells are wrong

Under the note's own stated method (`H = 1`, `r_z = 1/8`, `M_0` recomputed,
`nu_z` floored 4dp, `m = 0.0439`) my leg returns

```
nu_z = 0.047187    log10 C_R = 21.3956    log10 Q_0 = 46.9696    frozen = 21.1226
```

against the printed `0.056...`, `21.4842`, `46.8492`, `22.9859`. The
provenance of each printed cell:

- `0.056...` is `nu_z` at **`sigma = 1.42`** (`0.056964`), not `1.48`.
- `21.4842` is `log10 C_R` at `sigma = 1.48, **H = 5**`, not `H = 1`.
- `22.9859` is the frozen-`nu_z` value at **`sigma = 1.40`**, not `1.48`.
- `46.8492` corresponds to `nu_z ~ 0.0473`, i.e. neither the printed `0.056`
  nor any consistent run I could reconstruct.

The row is internally incoherent: its own `Q_0` implies `nu_z ~ 0.0473`, which
contradicts the `nu_z` it prints. **Direction: the printed `Q_0` is `0.12
log10` more favourable than the honest value, so the note's "`+10.40` worse"
is if anything an understatement (honest: `+10.52`). No conclusion moves.**
Repair: recompute the row, or delete it.

### D3 - section 1.6's `m_z` table row labelled `r_z = 0.025` is in fact `r_z = 0.026`

My leg:

```
m_z(0.026) = 0.0123393745    m_z/r = 0.474591     <- the printed "0.025" row
m_z(0.025) = 0.0119011586    m_z/r = 0.476046
```

The printed pair (`0.0123394`, `0.4746`) is `r_z = 0.026` exactly. It is also
internally inconsistent as printed: `0.0123394/0.025 = 0.49358`, not the
`0.4746` in the adjacent column. Every other row of that table (`0.125`,
`0.08`, `0.05`, `0.03`, `0.02`, `0.015`) reproduces on my leg to the printed
digit; this is the only bad row.

Three cells of the joint scan (`sigma=1.10 H=1 r=0.025`, `sigma=1.10 H=6
r=0.025`, `sigma=1.48 H=1 r=0.025`) then display `m_z = 0.01234`, while the
bolded joint row displays the correct `0.01190`. **I confirmed that the
*computation* used `0.01190` throughout** - all three `log10 Q_0` values
(`29.4456`, `27.0186`, `32.5580`) reproduce exactly on my leg with
`m_z = 0.01190` and do not reproduce with `0.01234`. So this is a display
defect only; no number changes. **Repair: relabel the table row `0.026`, add
the true `0.025` row, and correct the three display cells.**

### D4 - section 1.6's `sigma=1.16` row is imported from section 1.5.3 under a different `m_z`

Row 2 prints `nu_z = 0.12865, m_z = 0.04444, floor 18.6139, Q_0 35.8768`. On
my leg, under the four candidate conventions:

```
nu 5dp, m=0.04444  (as declared) -> floor 18.5748   Q_0 35.8377
nu 4dp, m=0.04444                -> floor 18.5827   Q_0 35.8456
nu 5dp, m=0.0439                 -> floor 18.6061   Q_0 35.8690
nu 4dp, m=0.0439  (= 1.5.3)      -> floor 18.6139   Q_0 35.8768   <- printed
```

So the row is section 1.5.3's number carrying section 1.5.3's `m = 0.0439`,
displayed in a table whose calibration baseline `36.4190` uses `m = 0.04444`.
The `Delta` cell should read `-0.58`, not `-0.54`; and section 1.3's L3 entry
`-0.57`, measured against the declared `36.4190` baseline, should be `-0.58`.
Direction: favourable to L3 by `0.04 log10`. Immaterial to the ranking.

### D5 - "nothing pushing back" is false

See Claim 2b above. The floor rises by `log(K_+)(1/alpha - 1/alpha')`, i.e.
`+0.668 log10` over the `sigma: 1.10 -> 1.48` move at `H = 6`. Repair the
sentence; the numbers are already right.

### D6 - the section 1.4 gate table's receipts

**(a) All eight `file:line` pointers are wrong.** The quoted *strings* are
genuine - I located every one of them - but not where the note says. Against
`EFFECTIVE_THEOREM_ASSEMBLY_SOL.md`:

| gate | note cites | **actual line** |
|---|---|---|
| (H-RATE) | `:775-780` | **165** (and `:748` for the superseding read) |
| (H-HOL) | `:250-252` | **213** (`:250-252` is the (H-SIDE) quote) |
| (H-C4) | `:865-869` | 864 (acceptable) |
| (H-ROUTE) | `:305` | **300** (`:305` reads "nothing - it is a constraint") |
| (H-GEOM) | `:245-247` (also `:243-247` in section 1.3) | **235** |
| (H-SIDE) | `:270` | **255** (`:270` is the (H-C4) quote) |
| (H-TRANS) | `:844-852` | **820** |
| (H-REFL) | `:781-786` | **766** |
| (H-SIDE) detail "answered conditionally, not removed" | `:271-274` | **258** |
| (H-REFL) "narrowed by F4" | `:871-878` | **850-856** |

Also `BOUNDARY_ALPHA_THEOREM_SOL.md:407` (R9c, "For `2<p<3`, positive layer
cake") is actually `:433`; `:238` is `:237`; the `phi_infty` definition cited
at `EFFECTIVE:76-78` is at `:80-81`; and the section 1.2 claim that
`85.35789877...` is "at `:434`" is wrong - it is at **`:428`** (`:434` is the
Route-B `K_F=109` diagnostic line).

By contrast the section 1.1 receipts R1-R7 and R9d are accurate. The failure is
confined to - and total within - the one section that is entirely
receipt-driven. Given that the cited source file itself carries a "Cite fixes"
correction bullet at `:774-778`, this is not a defensible miss.

**(b) The R8 quote elides the load-bearing clause.** The source
(`R5_MONOTONICITY_GATE_SOL.md` D12) reads:

> "... in the form consumed by (G2) **and by the R5/DH2 activation, which
> additionally requires N-independent `K_+`, `K_F`, `nu_seed`, `omega_*`.
> Unchanged by this note;** no RIGOROUS ... campaign proves alpha>0."

The note's ellipsis removes exactly the clause stating that the open Scope-2
blocker *additionally requires a family-uniform `K_+`*. That clause couples
(H-RATE) Scope 2 to (H-SIDE). Removing it is what lets section 1.4 present
(H-SIDE) as an isolable single open gate. This is a material misquote by
omission, in the one receipt the section's whole ledger-conflict resolution
rests on.

**(c) (H-C4).** The note grades it "DISCHARGEABLE (banking act) ... Blocker:
administrative, not mathematical". `CR_REDUCTION_V3_REFEREE.md`'s final
verdict, the same paragraph the note quotes from, also says: "**No gate
moves.** `q_monotone` stays. This is not a final `q_0`", and "E1 leaves two
conservative-direction ledger items attested indirectly rather than at source."
"No gate moves" is a direct denial of the note's read.

**(d) (H-REFL).** Source status is "PRINTED-LITERATURE, same tier as
(H-RATE)'s printed inputs" - and (H-RATE)'s printed inputs are graded
CONFIRMED-*conditional*, not discharged. Grading (H-REFL) "DISCHARGED modulo
citation hygiene" is an upgrade past its source, however defensible the
underlying Hejhal Cor. 7.12 citation is.

### D7 - "(H-RATE) Scope 1: Blocker: none identified" omits five of the seven consumed sub-inputs, including a conjectural one

The banked sub-input table (`EFFECTIVE_THEOREM_ASSEMBLY_SOL.md:192-201`) lists
**seven consumed** sub-inputs. The note names two of them ((FW), (DH_{2,4}))
and concludes "none identified; cost only". The third listed consumed row is

> M1 localization triple / Route-B repair | ... `M1_LOCALIZATION_TRIPLE_REFEREE.md:12`

whose referee's own executive verdict reads:

> "`M1_ROUTE_B_REPAIR_SOL.md` | **CONFIRMED** | ... The note correctly leaves
> `O(q^{1-2 sigma})` conjectural."
> "... The `q^{1-2 sigma}` RATE bound is still conjectural."

At the banked `sigma = 11/10`, `q^{1-2 sigma} = q^{-6/5}` - **the very exponent
(H-RATE) Scope 1 claims**. The assembly does argue (section 2.3) that the
N1-RATE route is "no longer needed", and grades standalone N1-RATE
"OPEN-CONJECTURAL - but NOT consumed"; but the M1 row is separately listed as
**consumed**, and no banked source reconciles the two. A referee report that
declares "Blocker: none identified" without touching this is not entitled to
the conclusion.

### D8 - the L5 evidence cell `-25.5` is wrong by a factor `ln 10`

Section 1.3, L5: *"at `1/alpha = 0.833 log10` per e-fold, and V1->V3 spent
three referee cycles for 30.59 e-folds = -25.5"*.

One e-fold of `C_R` moves `log Q_0` by `1/alpha = 0.8333` **nats**, i.e.
`0.36191 log10` - not `0.833 log10`. Hence

```
30.5945 e-folds -> 30.5945/1.2/ln 10 = 11.0725 log10      (note: 25.5)
 1.7179 e-folds ->  1.7179/1.2/ln 10 =  0.6217 log10      (note: 0.62  - correct)
```

The note converts correctly in its commentary (`1.7179 e-folds = -0.62 log10`)
and incorrectly in its table (`30.59 e-folds = -25.5`). Cross-check: the V1
`C_R` sits `30.5945` e-folds above `C_R'''`, giving `log10 Q_0(V1) = 47.52`
against `36.4487` now - a `11.07 log10` total, as required. The L5 verdict
("declining") is unaffected, but `-25.5` must not be quoted.

### D9 - section 1.7.6 advertises a COMPLETE list of frozen inputs and is not complete

Missing, in decreasing order of severity:

**(a) (H-HOL).** The banked finite-Hecke holomorphy theorem
(`HOLOMORPHY_GATE_SOL.md:373-379`) is proved on "an open neighborhood of the
full `H_0`, of the A0 domain `overline{Omega}`, of `D_z`, and of the old
Route-B right domains". A rectangle of height `H = 6` is **none of those**. The
note lists (H-ROUTE) as the geometry constraint (section 1.7.7) and grades
(H-HOL) "DISCHARGED for the domains used" - but the domains used in sections
1.5-1.6 are not the domains it was proved for. (H-HOL) belongs in the frozen
list.

**(b) The `H_0` underwriting `K_+ = 117` is only `+/- 0.9999` tall.**
`HOLOMORPHY_GATE_SOL.md:80`: `H_0 = [1/2, 1.4999] x [t_c - 0.9999, t_c +
0.9999]`. Section 1.7.2 treats the `H = 6` geometry as merely "a larger set,
so `K_+ >= 117`". It is not a matter of degree: the whole conditional
apparatus that produced `117` (full-width `H_0` plus the anchor gate) is out of
domain at half-width `3`. On the `sigma` axis the proposal stays inside
(`1.48 < 1.4999`); on the `H` axis it is `3x` outside.

**(c) The monotonicity claim in section 1.7.2 is false for the `H` lever.**
"Enlarging `Omega` enlarges that set, so the true `K_+` on the modified
`Omega` is `>= 117`." For the `sigma` lever this is right: the left edge is
unchanged and the top/bottom edges extend, so the three non-`Gamma_R` sides
form a superset. For the `H` lever it is **wrong**: the top and bottom edges
*move* (from `Im = t_0 +/- 1/2` to `t_0 +/- 3`); they are not supersets of
the old ones, and `partial Omega_{H=6} \ Gamma_R` does not contain
`partial Omega_{H=1} \ Gamma_R`. The correct statement for the `H` lever is
that `K_+` on the new domain is simply **unknown**. Direction: the error is
conservative for the note, but it is stated as fact and is false.

**(d) `H`-uniformity of the section 2-4 chain.** Section 1.7.3 is scoped
entirely to `p != 11/5`. Changing `H` is an independent axis: `Gamma_R` goes
from a height-`1` to a height-`6` segment. My own reading is that this one is
**benign** - (3.15) is pointwise in `s`, so only `sup_{Gamma_R}|s|` enters, and
the note does recompute `S(sigma,H)` - but the note never states or argues
this, and a list that calls itself complete must contain it.

**(e) `q_side'''` under every lever.** `Q_0` is a `max`, and `q_side'''`
depends on `C_R` and `alpha`. The note never re-checks that `q_A0` still binds
after a lever is applied. I checked; it does everywhere (section 1.3 above).
Unflagged, benign.

### N1-N5 - nits (no repair required)

**N1 - L2 is cleaner than the note says.** `r_z` does not touch `Omega`, so the
`(H-SIDE)` sup set is literally unchanged and `K_+ = 117` is **fully licensed**
for the `r_z`-only rows. Section 1.7.2's blanket "Any use of section 1.6's
numbers must first discharge (H-SIDE) at the new geometry" over-caveats L2, and
section 1.3's effort column mislabels L2 as "E1 (+E2)" when the E2 leg is
unnecessary. L2 alone (`-6.97`, no (H-SIDE) exposure, and it strengthens
conclusion (c) to `0.725 <= Re s_q <= 0.775`) is the note's most robust
output and should be ranked strictly ahead of L1.

**N2 - "termwise positive on the relevant range" is false.** In
`sum_{n odd} (4/(n pi)) sin(n pi y/H) sinh(...)`, at `y ~ H/2` the factor
`sin(n pi/2) = (-1)^{(n-1)/2}` alternates: the `n=3` term is negative. The
truncation error is therefore unsigned, so "floored to 4-5 decimals (margin
DOWN)" does not by itself certify a lower bound on `nu_z`. The tail is
`~1e-40`, forty orders below the flooring granularity, so no number moves - but
the stated justification does not hold.

**N3 - method description does not match the executed runs.** Section 1.5.1
says "400 odd modes" and "1440-2880 equispaced points". The executed scripts
use 100 odd modes (`N=201`, sections 1.5.2-1.5.3), 200 (`N=401`), 300
(`N=601`) and 400 (`N=801`, only the section 1.6 joint scan); and `M=720`
points for part of the section 1.5.3 scan and `M=360` for `m_z` in `joint.py`.
I verified `nu_z` is stable to 6 significant figures from `M=720` to
`M=46080`, and `m_z` from `M=360` to `M=11520`, so nothing moves.

**N4 - the sampled `m_z` clears its floor by `1.4e-6`.** A point-sampled
minimum is an **upper** bound on the infimum, while `m_z` must be a **lower**
bound. `m_z(1/8)` refines from `0.0444415` (`M=360`) to `0.0444413749`
(`M=11520`); the floored `0.04444` clears that by `1.4e-6`. Thin, and it is
exactly why section 1.7.5's "not certified" caveat is the right one. The Arb
cover re-run recommended in section 1.8(ii) is not optional.

**N5 - display arithmetic.** Section 1.2's split prints `16.6706 + 19.7780 =
36.4487`; the second addend truncates `19.7781030` and the printed addends sum
to `36.4486`. Section 1.5.2's "1.28e-4 relative increase in `(S+1)`" is
`1.157e-4` (the `4.2e-5` conclusion is right). Section 1.6's `m_z/r_z -> 0.5`
is `-> 0.51447`.

---

## 4. Scope and side-effect sweep

- The banking commit `662f93a` touches exactly two files:
  `NEXT1_Q0_GAP_PLAN_SOL.md` (new, 612 lines) and `plans/wayfinder/rh-goals/
  MAP.md` (+24 lines, a dated ledger entry). No lane-G source file was
  modified. The note's claim "this note edits no other file" is true of the
  note; the MAP entry is the standing wayfinder rule and carries no status
  change ("NO status change before its verdict").
- The MAP entry's headline summary is faithful to the note, including its
  caveats. It does inherit the note's `-0.54`/`-0.57` L3 figure (D4) and the
  "7 of 8" gate read (D6/D7), both of which this report corrects.
- No banked constant, no gate status, and no threshold is altered by the note
  or by this report. `Q_0 >= 2810199067910634377586449487575862960` stands, as
  an inequality, with `q_monotone`'s remainder unevaluated.

---

## 5. Bottom line

The mathematics the note was dispatched to produce is sound and I reproduce
it independently: the `-85.4` elasticity is an artifact of `log Q_0 = A/alpha`
and cannot be spent; `alpha` is welded to `nu_z` through the same wall; the
invariant is `alpha*nu_z = 2*(Re z_0 - r_z - 1/2)` in the strip limit; and the
consequent re-ranking (disc radius and aspect ratio ahead of `alpha` and ahead
of further `C_R` shaving) is correct. The executed rung's `-0.5719` and the
joint optimum's `18.7911` are exact. Its programme-level conclusion - that even
the full joint optimum leaves seventeen orders to certified computation, so
only a finite-base theorem bridges the gap - is right, and it is the note's
most valuable output.

The presentation is not yet fit to be quoted. The section 1.4 gate audit has a
100% receipt-miss rate, a material misquote by omission, and a "7 of 8"
headline that four of its own sources contradict. Three tables mix
incompatible conventions, one table row is mislabelled by `0.001` in `r_z`, one
row is a three-way composite, and one evidence cell is wrong by `ln 10`. None
of these move a headline number, which is precisely why they would survive
unnoticed into the next note that cites this one.

**Recommendation:** repairs D1-D9 as an append-only correction block, then the
note is fit to be banked as an UNREFEREED planning document with its section
1.5.3 and 1.6 numbers usable as *sensitivity estimates* - never as thresholds,
exactly as its own section 1.0 says. The section 1.8 next-lane ordering should
be amended to put the `r_z` lever (L2) first: it is the only lever that needs
no (H-SIDE) work at all, it is worth `-6.97 log10` on its own, and it
simultaneously sharpens conclusion (c) to `0.725 <= Re s_q <= 0.775`.

READY FOR JUDGING
