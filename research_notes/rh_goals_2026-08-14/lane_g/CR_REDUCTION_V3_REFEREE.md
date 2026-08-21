# Cold referee report: `CR_REDUCTION_V3_SOL.md` (rung-3 `C_R` reduction)

**Date:** 2026-08-20
**Target:** `research_notes/rh_goals_2026-08-14/lane_g/CR_REDUCTION_V3_SOL.md` at commit `c1e1b11`
**Referee:** independent, no shared context with the author of the target.
**Interpreter used for receipts:** `/Users/za/.venvs/farey-rh/bin/python`
(Python 3.13.13, python-flint 0.9.0 / Arb) **and an independent mpmath leg**
(`mp.dps=160`) written from scratch, not derived from the target's programs.
**Write scope:** this file only. No existing file was read-modified, renamed or
deleted. No commit, no push.

---

## 0. House verdict

> **CONFIRMED.**
>
> The three substitutions are legal on the printed text of
> `ATOM_MOMENT_BRIDGE_SOL.md` §3. `C_4''' = 65459394456774532`,
> `C_R''' = 541656022363559883954520`,
> `q_A0''' = 2810199067910634377586449487575862960` and
> `q_side''' = 1134004458443795841` reproduce **digit for digit** on two
> independent arithmetic stacks. The `1.7179` e-fold ledger, the non-binding
> `(3.19)` finding, the zero-slack `F(12)` finding, the unspent `S` slack and
> the five CONJECTURAL gradings are all correct as stated. No consumed-but-
> unlisted factor was found. No gate is closed, `q_monotone` is kept.
>
> Three **nits** (N1-N3) below; none touches a number and none blocks banking.
> One **environment limitation** (E1) is disclosed: a subset of prior notes was
> unreadable in my sandbox, so two ledger items are attested indirectly.

---

## Attack 1 — attack-1 checklist on each of the three substitutions

I re-read `ATOM_MOMENT_BRIDGE_SOL.md` §3 (lines 156-508) directly. Verbatim
anchors:

- line 264 `(3.10)`: `D\prod_i\rho_i \le \lambda_q^2\pi^2 x_X \le 4\pi^2 x_X < 40 x_X`
- line 280 `(3.11)`: `\le 2^{12}(40Y/D)^2(1+\log_+(40Y/D))^2`
- lines 286-291 `(3.12)`: `\sum_{r\ge1}1/r^2=\pi^2/6<2`, `\sum_{r\ge0}1/(1+r)^2=\pi^2/6<2`, "There are at most four, so their complete cost is `<2^4`."
- line 297-300 `(3.13)`: `A_X^2=\sum\omega^2+2\sum_{\alpha<\beta}\omega\omega`; "We retain an extra factor 2 ... even though Lemma 4.1 is already formulated for ordered marked atoms."
- lines 449-451 `(3.24)`: `\Sigma_H+\Sigma_{rest} < (2^5+2^{13})(qR^2+R^4) < 2^{14}(qR^2+R^4)`
- lines 459-463 `(3.25)`: `2^{12}\cdot2^{20}\cdot\underbrace{2^{11}}_{40^2<2^{11}}\cdot\underbrace{2^4}_{\text{four zeta sums}}=2^{47}`
- lines 466-469 `(3.26)`: low `2^{47+11+1}=2^{59}`, high `2^{47+14+1}=2^{62}`
- line 486 `(3.28)`: Ford `\le Y^2`; line 489: coefficient `2^{62}+1`.

| # | substitution | (1) sharper value printed, same object | (2) exactly once | (3) multiplicative | (4) no re-use of the rounded value | verdict |
|---|---|---|---|---|---|---|
| (i) | `2^11 -> 1600` | YES — `(3.25)` line 461 prints the underbrace `40^2<2^{11}`; the sharper member `40^2=1600` is the printed LHS. The object is the single `Z^2 = (40Y/D)^2` insertion of `(3.11)` | YES — one underbrace at `(3.25)`, one ledger row (line 499). `40` occurs elsewhere in §3 **only inside logarithms** (`(3.11)` `1+\log_+(40Y/D)`, `(3.14)` `B`, `(3.15)`, `(3.16)` `(1+\log40)^4`, `(3.17)` `t=H/Y\le40`, `(3.20)`, `(3.23)`) — I grepped all 21 occurrences of `40` in §3 and every non-`40^2` one is logarithmic or a range bound | YES | YES — logarithmic uses are consumed by `(3.16)/(3.18)/(3.20)/(3.23)`, i.e. by items #5/#6, disjoint from the `40^2` slot | **LEGAL** |
| (ii) | `2^4 -> (\pi^2/6)^4` | YES — `(3.12)` prints the per-integer sum as an **equality** `=\pi^2/6` for **both** bridge shapes, then rounds each to `<2`. The `2^4` is the source's own 4th power of its own per-integer bound | YES — one underbrace at `(3.25)`, one ledger row (line 500) | YES | YES — the `\pi^2/6<2` line is a single displayed line consumed once | **LEGAL** |
| (iii) | `2^14 -> 8224` | YES — `(3.24)` prints `(2^5+2^{13})(qR^2+R^4)` as the middle member of its own chain, bounding the same object in the same functional form; `2^5+2^{13}=8224` | YES — used once as the exponent `14` in `(3.26)`, one ledger row (line 502) | YES | YES | **LEGAL** |

Two hazards I probed specifically and cleared:

- **(ii) "at most four".** The substitution is only valid if fewer than four
  auxiliary integers is also bounded by `(\pi^2/6)^4`. Since `\pi^2/6=1.6449>1`,
  `(\pi^2/6)^k \le (\pi^2/6)^4` for `k\le4`. Clean. Scope is also preserved:
  `(3.12)` covers only the **unweighted** auxiliary integers, and the
  substitution changes nothing else.
- **Strictness degradation.** `(3.12)`'s `\pi^2/6` is an **equality**, so after
  substitution the subtotal chain is `\le sub_hi`, not `< sub_hi`, where
  `(3.27)` needs strict `<`. The target's outward rounding rescues this: it
  takes `ceil(sub_hi)+1`, and its `strict=` assertion checks
  `C_4''' > sub_hi + 1` strictly. I re-ran that check independently (below):
  `65459394456774532 > 65459394456774531.0478...` — **strict, PASS**. The
  target does not spell this hazard out, but its convention covers it.

### Outward rounding of `C_4'''` — replayed

Independent mpmath leg (not the target's code):

```text
sub_hi   = 65459394456774530.0478823748918   (mpmath, dps=160)
arb leg  = [65459394456774530.04788237489175621117372539410036399669031... ]
floor(sub_hi)+1+1 = 65459394456774532
minimal-above-(sub_hi+1): C_4''' > sub_hi+1 = True ; C_4'''-1 <= sub_hi+1 = True
```

`C_4''' = 65459394456774532` is the **least** integer meeting the strict
requirement. Both directions checked. **PASS.**

### Joint execution — no interaction, and the regime does not flip

The three substitutions touch three disjoint slots of the same product; none is
inside a logarithm; none re-enters `(3.26)`. The one real interaction risk is
the **regime max flipping**, because `(3.26)` uses a single constant for both
branches of `(3.27)`. Re-derived independently:

```text
sub_hi (8224)          = 65459394456774530.05
sub_lo (1280 = 2^8+2^10) = 10188232600276191.45   ratio hi/lo = 6.425
sub_lo (825 = 625+200)   =  6566634293146764.02
high_binds = True  (both variants)
```

The high regime still binds after all three substitutions. **PASS.** The target
checked this rather than assuming it (§1.1), which is the right instinct.

**Verdict attack 1: PASS.**

---

## Attack 2 — the `(3.19)` NON-BINDING claim

`(3.19)` prints `\Sigma_H+\Sigma_{rest} < (2^8+2^{10})Y < 2^{11}Y`, i.e. `1280Y`;
`(3.16)` gives `625Y` and `(3.18)` gives `200Y`, i.e. `825Y`. Both are legal
substitutions by the same checklist. Recomputed above: the low-regime
coefficient is `1.0188e16` (at `1280`) or `6.5666e15` (at `825`) against a
high-regime `6.5459e16`. Low stays strictly below high in both cases, so
`C_4'''` is unchanged and the gain is **exactly zero**.

Confirmed: the claim is a real finding, not a dodge, and the target correctly
banks it at zero and warns that any note claiming e-folds from `(3.19)` would be
wrong. **PASS.**

*Note for the dispatching agent:* the brief's paraphrase "low regime stays 8x
below high" is not what the note says and is not what the arithmetic gives — the
factor is **6.425x** (at `1280`), or `9.97x` at `825`. The note itself only
claims "strictly below", which is correct.

---

## Attack 3 — full re-derivation of `C_R'''` and the A0 propagation

I re-read `BOUNDARY_ALPHA_THEOREM_SOL.md` §1.2 (lines 140-200) and
`R5_ACTIVATION_CLOSURE_SOL.md` §4, then wrote my own mpmath programs from those
sources, with no code copied from the target.

### 3a. Assembly inputs re-derived from `(4.1)`, not taken on trust

From `ATOM_MOMENT_BRIDGE_SOL.md` (4.1)/(4.2) at `p=11/5`:

```text
1/(3-p) + J_2(11/5) = 5/4 + 305 = 306.25 = 1225/4      [recomputed: 306.2500...]
J_4(11/5) = 5+100+1500+15000+75000 = 91605             [recomputed: 91605.000...]
F(q) = q^{4/5}(1225/4 + 91605/q); 91605/q decreasing => sup on q>=12 at q=12
F(12) = 306.25 + 7633.75 = 7940                        exact rational, ZERO SLACK
G(11/5) = 1/(1/5) + 1/(1/5)^2 = 5 + 25 = 30            exact (the wrap `30`)
```

So the target's `F = 1225/4 + 91605/12 = 7940` and its "zero slack — exact"
grading are **independently confirmed**, including that the sup over `q>=12` is
attained at the endpoint `q=12`, which is what makes the slack genuinely zero on
the declared scope.

### 3b. `C_R` for all four constants — mpmath leg, minimality both directions

```text
pub    C_R= 10489412368759562746433608215977724802  logCR= 85.24342975039403316214  minimal: True True
C4'    C_R= 38160259896392973127946053              logCR= 58.90383688911611140451  minimal: True True
C4''   C_R= 3018536183210772296097745               logCR= 56.36681423818909707845  minimal: True True
C4'''  C_R= 541656022363559883954520                logCR= 54.64891810775648347353  minimal: True True
```

Cross-checked against the sources, not against the target:

- `10489412368759562746433608215977724802` = the published `(RATE-A)` constant,
  `BOUNDARY_ALPHA_THEOREM_SOL.md:31`.
- `38160259896392973127946053` = `CR_REDUCTION_V2_SOL.md:194`.
- `3018536183210772296097745` = `CR_REDUCTION_V2_SOL.md:195,208`.

Three-way convention lock **independently confirmed**. `C_R'''` is produced by
exactly the convention that certifies the three banked lines.

\[ \boxed{C_R'''=541656022363559883954520} \qquad \log C_R'''=54.648918107756483473\ldots \]

### 3c. A0 propagation — mpmath leg

```text
pub    q_side= 134010166814705707171424895246  q_t= 332093267419812025416641789732742045430624465595  T= 109.4217450401595237438  A0<m: True ER<K: True qs<qt: True
CR'    q_side= 39311645103099547636            q_t= 97418971860452658435229799565334786148            T=  87.47208432242792227909 A0<m: True ER<K: True qs<qt: True
CR''   q_side= 4746157036282968395             q_t= 11761546420922598622910053339543258496            T=  85.35789877998874367404 A0<m: True ER<K: True qs<qt: True
CR'''  q_side= 1134004458443795841             q_t= 2810199067910634377586449487575862960             T=  83.92631867129489900328 A0<m: True ER<K: True qs<qt: True
```

Cross-checks against sources: `332093267419812025416641789732742045430624465595`
and `134010166814705707171424895246` = `R5_ACTIVATION_CLOSURE_SOL.md:16,33-34,289,297`;
`97418971860452658435229799565334786148` and
`11761546420922598622910053339543258496` = `CR_REDUCTION_V2_SOL.md:263-264,287,302`.

\[ \boxed{q_{A0}'''=2810199067910634377586449487575862960},\quad q_{\rm side}'''=1134004458443795841 \]
\[ \log q_{A0}'''=83.9263186712948990\ldots \]

**Digit-for-digit agreement with the target on every one of the four rows and on
both integers.** The Arb floor-endpoint agreement, the two-sided minimality, the
strict `A0 < m = 0.0439` and the `q_side < q_transport`, `q_t >= 12`, `q_t >= 3`
side conditions all reproduce. **PASS.**

---

## Attack 4 — the e-fold ledger

```text
ln(2^11/1600)          = 0.24686008
ln(2^4/(pi^2/6)^4)     = 0.78178751       (pi^2/6)^4 = 7.321397388943344141302913197
ln(2^14/8224)          = 0.68924854
sum                    = 1.7178961        <- matches the claimed 1.7179
ln(C_4''/C_4''')       = 1.7178961
ln(C_R''/C_R''')       = 1.7178961
ln(2^100/C_4''')       = 30.594512        <- matches the claimed cumulative 30.5945
ln(C_R_pub/C_R''')     = 30.594512
```

Residual §4 ledger also checks: `ln(1.5)=0.405465`, `ln2=0.693147`,
`ln(8224/5803)=0.348682`, sum `1.4473` — the target's `>=1.447`. The unspent
`S` slack `ln(8.648/8.646893243596647842) = 0.000127986` — the target's
`0.000128`. **PASS.**

---

## Attack 5 — audit of the five CONJECTURAL gradings

| item | target grade | my finding |
|---|---|---|
| `2^12 -> 8192/3` at (3.5) | CONJECTURAL, needs `sup_{Z>=1}(\lfloor\log_2 Z\rfloor+2)^2/(1+\log Z)^2 = 4` | **Correct.** (3.4) line 190-191 proves `\le(2048/3)Z^2(L+2)^2 \le 2^{12}Z^2(1+\log Z)^2` — genuinely two different functional forms, `L=\lfloor\log_2Z\rfloor` vs `1+\log Z`, and the constant `2^{12}` absorbs the conversion. The step function is discontinuous at every power of two, so the target's insistence on a per-dyadic-block argument is right, and its numeric table is correctly labelled an observation |
| drop the `2` at (3.13) | CONJECTURAL, largest residual, double-counting risk vs (3.9) | **Correctly graded, but see N3.** Line 300 asserts redundancy ("even though Lemma 4.1 is already formulated for ordered marked atoms") without proving it — CONJECTURAL is right. On the double-counting risk: the two factors have **textually distinct roles** — (3.9)'s trailing `2` is declared at line 251 as "the one-mark/two-mark selector", whereas (3.13)'s `2` is the ordering factor of `2\sum_{\alpha<\beta}`. They are prima facie *not* the same factor. So the risk as the target words it ("or that they are the same factor counted once") is stated slightly too strongly. But the risk is nonetheless **real in the other direction**: `TWOMARK` Lemma 4.1's code must be checked to be over **ordered** pairs, which is not verifiable from (3.9)'s printed product alone. Since the target does **not** take this gain, the overstatement is conservative and costs nothing |
| `M_0=2.775` | CONJECTURAL, new obligation | **Correct.** I read `M3_UNIFORMITY_EXECUTION_SOL.md:275`: `\sup_{s\in K_{15}}|M(s)|=M(1.1)<2.775` with "Equality is attained at `s=1.1`". The value of `M(1.1)` is indeed **not printed**, so no sharper number exists in the printed text. The requested repair (certified enclosure of `M(1.1)` on `K_15`) is exactly the right obligation. `M_0` does enter the assembly once, as the outermost multiplicative factor — I verified this on `BOUNDARY_ALPHA_THEOREM_SOL.md:159` (`CRraw=arb('2.775')*(pair+wrap)`) — so a reduction there is e-fold-for-e-fold, as claimed |
| `40 -> 4\pi^2` | CONJECTURAL, fails single-occurrence | **Correct, and this is the sharpest call in the note.** `40` occurs logarithmically at `(3.11)`, `(3.14)-(3.18)`, `(3.20)`, `(3.23)`. A global change fails checklist items (2) and (4). Each named repair — `(1+\log 4\pi^2)^4`, the `t\le4\pi^2` maximization replacing the `200` at `t=40`, `c=\log(4\pi^2\cdot5/2)` for `\log100`, the `5^4\le209q` step — is a fresh maximization. Refusing to estimate the gain is the honest call |
| `8224 -> 5803` | CONJECTURAL, needs recombination | **Correct.** `(3.21)` line 412-413 prints `25<32=2^5`; `(3.23)` lines 439-441 print `5778q+27R^4<2^{13}(q+R^4)\le2^{13}(qR^2+R^4)`. Recombining to `5803(qR^2+R^4)` needs both `q+R^4\le qR^2+R^4` (from `R>1`) and a max across two different coefficient slots — a new one-line lemma, not a printed bound on the same object. Grading it CONJECTURAL while taking the verbatim-printed `8224` is the correct line |

### Consumed-but-unlisted sweep

I enumerated every multiplicative contributor to the `(AM)` coefficient and to
the outer assembly and matched each to a ledger row:

- `(3.3)` `2T^2` and the `8\cdot4^i` dyadic shell count — absorbed inside
  `(3.4)`, i.e. covered by item #1.
- `(3.5)` `2^{12}` #1; `(3.9)` `2^{20}` #2; `40^2` #3; zeta `2^4` #4;
  `(3.19)`/`(3.24)` #5/#6; `(3.13)` `2` #7; `(3.28)` Ford `+1` — all listed.
- `\pi^{-2}` and `\lambda_q^2` are absorbed into `(3.10)`'s `40`, i.e. into
  #3/§4.4.
- `27`, `209`, `5` of `(3.22)/(3.23)` sit inside `2^{13}`, covered by #6/§4.5.
- Outer assembly: `2\pi^2`, `(S+1)`, `p=11/5`, `C_4`, `F`, `128(1+\log2)`,
  `G(p)=30`, `M_0`. Audited: `S` (#9), `F` (#10), `M_0` (#8), `p` (§4.6).
  Unlisted: `2\pi^2` (exact), `128(1+\log2)` (exact, from
  `DH2_RENEWAL_PROOF_SOL.md:619` via `BOUNDARY_ALPHA_THEOREM_SOL.md` (2.3)),
  and `G(11/5)=30` (I recomputed: exactly `30`). **All three are exact and
  slack-free**, so nothing is consumed-but-unlisted in any way that hides
  e-folds. See nit N1.

**Nothing consumed but unlisted. PASS.**

---

## Attack 6 — ledger discipline

| ledger item | evidence | verdict |
|---|---|---|
| `q_monotone` KEPT, D7 refutation stands | §3.5 and §5 item 4 of the target state this explicitly and the `q_0` max is printed with `q_{\rm monotone}` in it. See E1 for the one thing I could not read | **PASS** (see E1) |
| label "selected conditional analytic-tail cutoff, one term of a max" | §3.5 and the §7 summary row both carry exactly this wording; §5 items 2 and 3 repeat it; the label matches `R5_ACTIVATION_CLOSURE_SOL.md`'s own framing of `q_transport` as one term of the `max` at lines 33-34 | **PASS** |
| no gate closed | §5 item 1; nothing in the note touches a gate status, and §5 item 9 correctly re-affirms that machine formalization and the certified full-operator enclosure remain OPEN | **PASS** |
| **D1 lesson (bound vs count)** actually observed | §0.2 states the LEDGER RULE up front; §2.2 explicitly re-states `(\pi^2/6)^4` as an upper bound "not a count and not claimed exact"; §5 item 8 lists all four substituted values as bounds and singles out `F(12)=7940` as the **only** exact assertion, justified by the rational identity. I checked every place the note prints one of `82944`, `1600`, `8224`, `(\pi^2/6)^4`, `7940`: no cardinality language anywhere | **PASS — genuinely observed, not merely claimed** |
| **D2 lesson (replay-program honesty)** actually observed | §3.4 volunteers, unprompted, that the replay is **not** byte-identical to `R5_ACTIVATION_CLOSURE_SOL.md` §4, names the exact lines that are computed-but-not-printed (`alpha`, `nu`, `alpha_nu`, `beta_exact`, `q_RATE`, `q_divisor`, `ER_at_q_side_upper`, `ER_at_q_transport_upper`), names the 26-character truncation, asserts the mathematics is unchanged, and points a referee at the verbatim re-run recipe. I independently confirmed the arithmetic is unchanged by writing my own program from the source and reproducing all four rows | **PASS — genuinely observed** |
| source-hash receipt honest | I re-ran `shasum -a 256` on all six files of §6 and got byte-identical output to the note's §6 block, including `ATOM_MOMENT_BRIDGE_SOL.md = 59ce32f7...`. The note's volunteered observation about `BOUNDARY_ALPHA_THEOREM_SOL.md` moving `1a5a96e6... -> 5a8d0bcc...` is flagged as "an observation, not a claim", which is the right register; my §3b reproduction of the published `C_R`, `C_R'` and `C_R''` from the current file independently shows the load-bearing assembly is intact | **PASS** |

---

## Defect list

No **defects**. Three **nits** and one **environment limitation**:

- **N1 (documentation, harmless).** §0 claims the note audits "**every** remaining
  factor in the `(AM)` §3 chain, plus the outer `M_0`, `S` and `F(12)`". The
  outer assembly also contains `2\pi^2`, `128(1+\log2)` and `G(11/5)=30`, none of
  which appears in the §1 table. I verified all three are exact and slack-free
  (`G(11/5) = 5+25 = 30` recomputed), so no e-fold is hidden — but the word
  "every" is one row short of literal. *Repair: add three zero-slack rows, or
  soften "every" to "every rounded factor".*
- **N2 (precision of phrasing).** §3.1 says `\log C_R` "moves by **exactly** the
  `C_4` e-folds, as it must". It cannot be exact: the wrap term `14303.7...` is
  added before the outer scaling and the result is then ceiled. I measured the
  discrepancy: `ln(C_R''/C_R''') - ln(C_4''/C_4''') = -6.01e-20`. Numerically
  irrelevant, but "exactly" is the wrong word in a note whose whole discipline
  is bound-vs-exact hygiene. *Repair: "moves by the `C_4` e-folds to within
  `6e-20`, the wrap term and the ceilings being the only difference."*
- **N3 (risk slightly overstated, in the safe direction).** §4.2's phrasing
  "**or that they are the same factor counted once**" for the (3.9)/(3.13)
  collision is stronger than the printed text supports: `(3.9)`'s trailing `2` is
  declared at line 251 as the one-mark/two-mark **selector**, a different role
  from `(3.13)`'s pair-**ordering** factor. The real residual obligation is the
  narrower one the target also names — confirm `TWOMARK` Lemma 4.1's code
  enumerates ordered pairs. Since the gain is **not taken**, the overstatement is
  conservative and costs nothing. *Repair: optional, wording only.*
- **E1 (environment limitation, disclosed).** A subset of prior lane-G notes was
  unreadable from my sandbox (`EPERM` on every access path tried: Read tool,
  `grep`, `sed`, `git show`, direct Python `open`) — specifically
  `CR_REDUCTION_V2_REFEREE.md`, `AM_REFEREE.md`, `CR_REDUCTION_REFEREE.md`,
  `R5_ACTIVATION_CLOSURE_REFEREE.md` and `R5_MONOTONICITY_GATE_SOL.md`. I could
  read `CR_REDUCTION_V2_SOL.md`, `ATOM_MOMENT_BRIDGE_SOL.md`,
  `BOUNDARY_ALPHA_THEOREM_SOL.md`, `R5_ACTIVATION_CLOSURE_SOL.md` and
  `M3_UNIFORMITY_EXECUTION_SOL.md`, which carry all load-bearing numbers, so
  attacks 1-5 are fully receipted. The two items I could **not** verify at
  source are (a) the verbatim text of the referee-D7 correction block at
  `R5_MONOTONICITY_GATE_SOL.md:803-829` and (b) the verbatim D1/D2 wording in
  `CR_REDUCTION_V2_REFEREE.md`. Both are *conservative-direction* items:
  **keeping** `q_monotone` in a `max` can only weaken the conclusion, never
  strengthen it, and D1/D2 compliance I graded on the target's own text
  (above), which is the operative question. Neither affects any number. A
  referee with full read access should close (a) and (b).

---

## Final verdict

> **CONFIRMED.**
>
> `C_4''' = 65459394456774532`, `C_R''' = 541656022363559883954520`
> (`log = 54.648918107756483473...`),
> `q_side''' = 1134004458443795841`,
> `q_A0''' = 2810199067910634377586449487575862960`
> (`log = 83.9263186712948990...`) are correct, upward-valid on exactly the
> stated scope, and reproduced independently on two arithmetic stacks.
> The `1.71790` e-fold gain and the `30.5945` cumulative are correct.
>
> The three substitutions pass the full attack-1 checklist, do not interact,
> and do not flip the binding regime. The non-binding `(3.19)` finding, the
> zero-slack `F(12)`, the unspent `S` slack and all five CONJECTURAL gradings
> are correct. D1 and D2 were genuinely observed, not merely invoked.
>
> **Required repairs: none.** N1-N3 are optional wording repairs. E1 leaves two
> conservative-direction ledger items attested indirectly rather than at source.
>
> Recommendation: `C_4'''`, `C_R'''`, `q_side'''` and `q_A0'''` are fit to be
> **banked as candidates** on the same footing as `C_R'` and `C_R''` after their
> referees. No gate moves. `q_monotone` stays. This is not a final `q_0`.

READY FOR JUDGING
