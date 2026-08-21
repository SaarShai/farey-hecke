# Final cold completeness pass — effective theorem assembly, eight-gate table

**Date:** 2026-08-20
**Lane:** G / (RATE)-R3-R5 assembly
**Target:** `research_notes/rh_goals_2026-08-14/lane_g/EFFECTIVE_THEOREM_ASSEMBLY_SOL.md`
sha256 `8b0069733fef90309553b4e8a0c137c1ea06b6dd6792bb8bee6f60f01df99276`
(body + dated correction block 1 + dated correction block 2)

**Pass number:** third and intended-last.
Pass 1 = `EFFECTIVE_THEOREM_ASSEMBLY_REFEREE.md` (attacks 2/4/6).
Pass 2 = `EFFECTIVE_THEOREM_ASSEMBLY_REREFEREE.md` (attacks 1b/3/5).
This pass does **not** redo those attacks. Scope: (1) final state of the
eight-gate table given all current sources, including the new
`R3_TRANSPORT_EXECUTION_REFEREE.md`; (2) a fresh end-to-end walk of the §2
chain listing every consumed assumption; (3) the promotability verdict;
(4) a numerics spot-check of the correction-block-2 `Q_0'''`.

**Independence.** I did not write the target, either correction block, or
either prior referee report. Every number below was recomputed with fresh
code at `/Users/za/.venvs/farey-rh/bin/python` (python-flint / Arb,
`ctx.dps = 160`). No existing file was modified; nothing was committed.

---

## 0. Verdict table

| # | Item | Verdict |
|---|---|---|
| 1 | Eight-gate table, final state — all eight gates graded correctly at all current sources | **PASS with one required status touch** (`(H-TRANS)` is stale) |
| 2 | Gate-count consistency (body "six" vs block 2 "eight") | **PASS** — block 2's supersession is explicit and unambiguous |
| 3 | Fresh chain walk §2 (a)->(b)->(c): every consumed assumption lies inside the eight gates | **PASS** — no unnamed assumption found |
| 4 | `E_R = 0` branch | **PASS** — closed at source, banked twice |
| 5 | `t_0` / `gamma_1` digits provenance | **PASS** — rigorous Arb enclosure, reproduced at two precisions |
| 6 | `zeta` non-vanishing on `Re = 1` / `phi_infty` holomorphy on `\overline{Omega}` | **PASS** — inside `(H-HOL)`, and now *proved* in a banked referee (`R3_..._REFEREE.md` §4.2); over-assumed at source, conservative |
| 7 | `q_monotone` open-remainder phrasing (the `>=` form) | **PASS** — honest in body §4.5 and block 2 |
| 8 | Numerics spot-check: `Q_0''' = 2810199067910634377586449487575862960`, `log10 = 36.4487` | **PASS — reproduced digit-for-digit, independently** |
| 9 | Deliverable shape / hygiene (hashes, pointers, vestigial text) | **FAIL (four hygiene defects, all documentation-only)** |
| 10 | Date anomaly in the `R3_..._SOL.md` correction block (2026-08-21) | **PASS after investigation** — UTC-vs-local clock convention, not a provenance break (§4.2) |

**FINAL HOUSE VERDICT: CONFIRMED at conditional scope** — see §4 for the
exact scope wording and the one promotion block that must land first.

---

## 1. The eight-gate table, final state

Enumerated as the note now stands across body §3 + block 1 + block 2, with my
own ruling on each, given every source available on 2026-08-20.

| gate | status as the note now carries it | my independent ruling | correct? |
|---|---|---|---|
| **(H-RATE)** Scope 1 — boundary rate on `Gamma_R^A`, `alpha = 6/5`, `q_RATE = 12` | CONFIRMED-conditional (paper level); block 2 supersedes §3's "LIVE LEDGER CONFLICT" and assigns the two OPEN rows to Scope 2 | Verified the scope split at source: `R5_MONOTONICITY_GATE_SOL.md:1063` carries the promised D12 block ("the bare label `(RATE-A)` in the OPEN list is under-scoped"). Scope 1 is what §2(a) consumes and nothing more. The eight sub-inputs are graded at their most-caveated referee wording, including the correct "NOT consumed" ruling on the `A = 11/20` N1-RATE row. | **PASS** |
| **(H-HOL)** finite-`q` holomorphy / no poles on `\overline{Omega}`, `\overline{D_z}` | PROVED from printed theory; `q_divisor = 3`; nonvanishing companion explicitly NOT assumed | Correct, and the attached negative (Hejhal Thm 7.11 gives eventual zeros — the theorem *produces* a zero rather than assuming none) is the right way round. The `phi_infty` half of this gate is now independently proved on the full `\overline{Omega}` in `R3_..._REFEREE.md` §4.2. | **PASS** |
| **(H-C4)** the reduced tag coefficient | CONFIRMED-conditional; the constant self-graded an *unbanked candidate*; block 2 flags that the "RE-REFEREE: CONFIRMED" quote is a session utterance, not a repo referee file | Correct **for `C_4''`**. But block 2 then moves the operative constant to `C_R'''`, and `C_R'''` has a genuine repo referee: `CR_REDUCTION_V3_REFEREE.md` final verdict "**CONFIRMED** … **Required repairs: none.** … fit to be **banked as candidates**". So the gate's evidence base is now *stronger* than the note records. Under-claimed, i.e. conservative. | **PASS (under-claimed)** |
| **(H-ROUTE)** A0 is a first-zero ledger; no `K_F`/`d_*` mixing | PROVED (domain correction), BINDING | Honoured throughout: the max consumes `K_+`, `m_z`, `nu_z` only; the `K_F = 109` pairing is computed for completeness and explicitly not used. | **PASS** |
| **(H-GEOM)** `m_z >= 0.0439`, `nu_z >= 0.1552` | PROVED (Arb interval cover) | Now *independently* re-proved by a second referee at a different discretisation, a different phase offset, and — for `nu_z` — by two series-free methods (walk-on-spheres Monte Carlo `0.1553`, Jacobi FD). `R3_..._REFEREE.md` §1.5, §2.4. Correct orientation of the harmonic measure (right edge, not left) confirmed. Carries recorded hygiene defect D4 (grid-critical certificates, 0.02% / 0.009% slack) — valid as printed, not a soundness issue. | **PASS** |
| **(H-SIDE)** `K_+ = 117` | CONFIRMED-conditional source input; family-uniformity answered *conditionally*, not removed; side hypothesis `0 < E_R <= K_+` discharged by part (a) | Correct and correctly caveated. The `E_R = 0` branch is separately closed (see §2.4 below). | **PASS** |
| **(H-TRANS)** the two-constants / Rouché transport implication itself | **"Status: PAPER-LEVEL, UNREFEREED."** (block 1; untouched by block 2) | **STALE.** The cold referee that block 1 named as the discharger now exists: `R3_TRANSPORT_EXECUTION_REFEREE.md` (2026-08-20). Its §7 quotes block 1's three discharge asks verbatim and confirms all three (two-constants incl. the subharmonic maximum-principle re-derivation and the orientation cross-check; the `omega(s, Gamma_R; Omega)` interval cover; Rouché strictness). Its attacks 1, 2, 4, 5 are CONFIRMED; every printed numeral reproduced at `dps = 60`. Its only blocking defect against the source, D1 (the mis-scoped Hejhal (7.22) citation), plus D3, **have been applied at source** — `R3_TRANSPORT_EXECUTION_SOL.md` now carries a dated correction block with the exact repair text, and its hash is now `d53b0ae6…`. | **FAIL — needs the final status touch** |
| **(H-REFL)** the reflection identity's own hypotheses | PRINTED-LITERATURE, same tier as (H-RATE)'s printed inputs; source Hejhal Cor. 7.12 p. 579 + FJS §2.4 | Gate correctly *exists* (it was pass 2's defect 5) and the pointer is right. Two cosmetic over-statements: (i) it lists unitarity `|phi_q(1/2+it)| = 1` as a consumed hypothesis, but the repaired route consumes only `phi_q(s)phi_q(1-s) = 1` plus reality `phi_q(\bar s) = \overline{phi_q(s)}` — which together *imply* unitarity, so listing it is conservative, not wrong; (ii) block 2 states "delta = 3/8 (< 1 and < gamma_1/10)", which is a hypothesis of the **abandoned** printed-(7.22) route and is not consumed by the Cor. 7.12 route at all. Vestigial. Note the source's own repair block chose `delta = 1/2`; the two do not agree, and neither is used. | **PASS (mathematically), two cosmetic residues** |

### 1.1 Gate-count consistency — verified unambiguous

- Body §2:89-91 — "Assume the six named gates".
- Block 1 — adds the `(H-TRANS)` row (does not restate a count).
- Block 2 — "**Gate count**: the theorem assumes EIGHT named gates (the
  original six + (H-TRANS) + (H-REFL)); §2's 'six' is superseded."

The supersession names the count, enumerates the additions, and names the
superseded location. Pass 2's defect 6 ("boxed theorem assumes six, appendix
says seven") is **repaired**. No third count appears anywhere in the file.
**PASS.**

---

## 2. Fresh end-to-end chain walk, both correction blocks applied

Every assumption the chain consumes, re-derived from the sources rather than
from the note's own framing. Bracketed tag = the gate it belongs to.

### 2.1 Part (a) — boundary rate

1. `E_R(q) = sup_{Gamma_R^A} |phi_q - phi_infty| <= C_R q^{-6/5}` for integer
   `q >= q_RATE = 12`, on the balanced/matched boundary. **[(H-RATE) Scope 1]**
   — consuming (FW), (DH_{2,4}), the M1 localization triple / Route-B repair,
   the endpoint comparison, Lemmas 3.1 (`:335`) and 3.2, and
   `sup_{K_15}|M(s)| < 2.775`. All eight sub-inputs are inside the gate.
2. The numeric value of `C_R`. **[(H-C4)]** — operative value now `C_R''' =
   541656022363559883954520`, referee-CONFIRMED.
3. `Gamma_R^A` (closed, `|t - t_0| <= 1/2`) is the same right edge as R3's
   `Gamma_R`. Definitional; checked against `R3_..._SOL.md:22-52` and
   `BOUNDARY_ALPHA_THEOREM_SOL.md:19-21`. No assumption.

### 2.2 Part (b) — two-constants transport

4. `F_q = phi_q - phi_infty` holomorphic on `\overline{Omega}`.
   **[(H-HOL)]** for `phi_q`; for `phi_infty` see §2.5 below.
5. `|F_q| <= K_+ = 117` on the three non-`Gamma_R` sides. **[(H-SIDE)]**
6. `0 < E_R(q) <= K_+`. Discharged *inside* the theorem by (a):
   `E_R(q_A0) <= 9.89e-21 < 117` — I reproduced `9.890974306379110548e-21`
   independently at `C_R'''`. The `E_R = 0` branch: §2.4 below.
7. `nu_z = inf_{\partial D_z} omega(s, Gamma_R; Omega) >= 0.1552`. **[(H-GEOM)]**
8. The two-constants/Phragmén–Lindelöf machinery itself — subharmonicity of
   `log|F| - [nu log E_R + (1-nu) log K_+]`, the extended maximum principle
   past the four (polar) corners, the monotonicity step in `nu`, and the
   Rouché application. **[(H-TRANS)]**
9. Threshold arithmetic `q >= q_A0'''`, `q >= q_side'''`. Computed, not
   assumed — reproduced in §3.
10. `q >= q_monotone`. **Retained symbolically**; its (1.11) sub-gate is
    evaluable and dominated, its remainder is OPEN-CONJECTURAL. See §2.6.

### 2.3 Part (c) — Rouché and reflection

11. `m_z = min_{\partial D_z}|phi_infty| >= 0.0439`. **[(H-GEOM)]**
12. `phi_infty` has a zero in `D_z`. **PROVED, not assumed** — `2z_0 - 1 =
    rho_1` holds as *exact algebra* from `z_0 = (1+rho_1)/2`, so
    `zeta(2z_0-1) = 0`. Verified independently by the R3 referee
    (`2*z0-1-rho1 = [+/- 2.49e-60]j`). **No RH, and no simplicity assumption
    on `rho_1`** — Rouché transfers the count with multiplicity and only
    `>= 1` is needed (`R3_..._SOL.md:118`).
13. `phi_infty` holomorphic and pole-free on `\overline{D_z}`. **PROVED**
    (`R3_..._SOL.md` §2.1, re-derived in `R3_..._REFEREE.md` §2.2). On the
    disc `Re(2s) \in [5/4, 7/4] > 1`, so this needs only the Euler product —
    *not* the `Re = 1` line.
14. `phi_q` holomorphic on `\overline{D_z}`. **[(H-HOL)]**
15. Strictness `|F_q| < 0.0439 <= m_z <= |phi_infty|` pointwise on
    `\partial D_z`. Chained, not assumed; confirmed `R3_..._REFEREE.md` §2.3,
    which explicitly checked for the "vacuous Rouché" failure mode and found
    it absent.
16. Reflection: `phi_q(s)phi_q(1-s) = 1` (Hejhal Cor. 7.12, p. 579) **plus**
    `phi_q(\bar s) = \overline{phi_q(s)}` from the real (7.5) Dirichlet
    coefficients. **[(H-REFL)]** — and the printed (7.22) is *not* invoked.
17. Domain discipline: no `K_F`, no `d_*`. **[(H-ROUTE)]** — a constraint,
    honoured.

**Result of the walk: every consumed assumption lands in one of the eight
named gates. I found no ninth assumption.** Items 12, 13, 15 are proved
in-chain, not assumed — the note is right to keep them out of the table.

### 2.4 The `E_R = 0` branch — closed, and closed twice

If `E_R(q) = 0` then `F_q` vanishes on the whole segment `Gamma_R`, so by the
identity theorem `F_q = 0` on `Omega` and the transport conclusion is trivial
with both sides zero; `0^{nu_0}` is `0` and no `0^0` arises because
`nu_0 = 0.1552 > 0`. Banked in `BOUNDARY_ALPHA_THEOREM_SOL.md:615-623` (which
the assembly cites at §3 (H-SIDE)) and re-derived independently in
`R3_..._REFEREE.md` §4.1, which grades the `:77` `0 < E_R` versus §3/§7
`E_R <= K_+` mismatch "cosmetic. No defect." I concur: the looser form is
sound and the branch is not a gap. **PASS.**

### 2.5 `zeta` non-vanishing on `Re = 1` — named, and now proved

The one place the chain touches the `Re = 1` line is the left edge of
`\overline{Omega}` (`Re s = 1/2`, so `Re(2s) = 1`), where `zeta(2s)` sits in
the denominator of `phi_infty`. The assembly does name it: §3 (H-HOL) grades
`phi_infty` pole-freeness "by explicit formula", and that formula's left edge
is exactly this. So it is **not** an unnamed assumption.

Its status has changed since the note was written. `R3_..._REFEREE.md` §4.2
(defect D2) supplies the full unconditional proof of `phi_infty` holomorphy on
`\overline{Omega}` — `Gamma(s-1/2)`, `Gamma(s)` pole-free (poles need real
`s`; `Im s \in [6.56, 7.57]`); `zeta(2s-1)`'s only pole at `s = 1` excluded by
the imaginary part; `4^s - 1 \ne 0` for `Re s > 0`; and `zeta(2s) \ne 0` by
Hadamard–de la Vallée Poussin on `Re = 1` and the Euler product beyond. That
classical input is separately banked in-repo
(`LAW_ANCHOR_T1_THETA.md:298,473` grades it "PROVED given CITATION").
`R3_TRANSPORT_EXECUTION_SOL.md`'s D2 block *records* the over-assumption but
does not insert the proof paragraph, so at source it is still bundled into a
CONJECTURAL hypothesis. **That is conservative in the safe direction — it can
only weaken the theorem, never make it false.** Ruling: consumed inside
(H-HOL), proved in a banked referee, over-assumed at source. **PASS**, with a
free strengthening left on the table.

### 2.6 The `q_monotone` open remainder — phrasing is honest

Body §4.5 computes only the (1.11) sub-gate (`N_monotone`), states that the
rest of `q_monotone` — "the point from which **all** envelopes used above are
proved monotone" — is untouched and CONJECTURAL, and writes the threshold as

`Q_0 = max{12, 3, q_side, q_A0, q_monotone} >= <integer>`

with "I do not claim the max is closed." Block 2 restates the same `>=` form
at `C_R'''`. §4.5 also records the `R5_ACTIVATION_CLOSURE_SOL.md:377-382`
reading (A0's envelope is monotone for all real `q > 0`, so no integer
`q_monotone` arises for A0) against D7 (which asserts `q_monotone` is broader
than any one envelope), **adopting neither** — the inequality form is safe
under either. The non-assumed table also carries the OPEN-CONJECTURAL row.
**PASS.** The one residue: §2's boxed `Q_0 = …` is an *equality*, superseded
in both value and form only in §4.5 and block 2. See defect F2.

---

## 3. Numerics spot-check (item 4 of my brief)

Fresh script, not copied from the note or from either prior referee.
`/Users/za/.venvs/farey-rh/bin/python`, python-flint / Arb, `ctx.dps = 160`,
integers extracted only after asserting the Arb string carries no `+/-` and no
exponent.

```python
alpha = arb(6)/5; nu = arb('0.1552'); m = arb('0.0439'); K = arb(117)
CR    = arb(541656022363559883954520)              # C_R''' (BOUNDARY_ALPHA §10)
beta  = alpha*nu
Ts    = (CR.log() - K.log())/alpha                 # q_side'''
T     = ((1-nu)*K.log() - m.log())/beta + CR.log()/alpha   # q_A0'''
x     = (CR/K)**(1/alpha)                          # N_monotone, route-H B = K_+
```

Complete stdout:

```text
q_side3= 1134004458443795841 floor agree True min_gt True min_le True
q_A03= 2810199067910634377586449487575862960 floor agree True min_gt True min_le True
ER<K True A0<m True ER_upper [9.890974306379110548771776148234686406065945478673991283631119990722354722164e-21 +/- 1.20e-181]
N_monotone3= 1134004458443795841 == q_side3: True
Q0= 2810199067910634377586449487575862960 ==q_A03 True
log10= [36.44873708539722848845416561638144741393233375395879619273720460873431429631 +/- 4.62e-159]
target match: True
ratio old/new= [4.185307210164024297063884028833950538344370570851687079582560234608 +/- 7.85e-161]
```

| claim in correction block 2 | my value | verdict |
|---|---|---|
| `q_A0''' = 2810199067910634377586449487575862960` | identical | **PASS** |
| `log10 = 36.4487` | `36.44873708539722848…` | **PASS** |
| "4.19x smaller than the boxed `Q_0`" | ratio `4.18530721016…` | **PASS** (rounds to 4.19) |
| `q_side''' = 1134004458443795841` (from `CR_REDUCTION_V3`) | identical | **PASS** |
| `Q_0''' = max{12, 3, q_side''', q_A0''', q_monotone}` closes on `q_A0'''` over the evaluable terms | `max` = `q_A0'''`; `N_monotone''' = q_side'''` exactly (the algebraic identity of block 1's D5, reproduced at the new constant) | **PASS** |

Rounding discipline re-checked independently: both thresholds are
`floor(e^T) + 1` with the Arb lower and upper endpoints agreeing on the floor
(`floor agree True`), and **both** minimality directions hold
(`min_gt True`, `min_le True`) — i.e. the integer is the least one meeting the
condition, and one less fails. `m_z` and `nu_z` are floored (margins DOWN),
`K_+` is the safe ledger value (bound UP), `C_R'''` is the ceiling of the
assembly upper endpoint (bound UP). Every rounding is adverse.

I also re-verified the two carried consequences at the new constant:
`E_R(q_A0''') <= 9.89e-21 < 117 = K_+` (**True**) and
`K_+^{1-nu} E_R^{nu} < 0.0439 <= m_z` (**True**) — so the theorem's (b) and
(c) survive the constant substitution intact, which block 2 asserted but did
not re-display.

---

## 4. Promotability verdict

### 4.1 What does NOT stand in the way

I looked for a surviving mathematical gap in the assembled statement and found
none. Specifically:

- No unnamed assumption (§2, seventeen items, all inside the eight gates).
- No arithmetic error (§3; and passes 1 and 2 reproduced `C_R''`, `q_side''`,
  `q_A0''`, the elasticities, and `q_A0'''` on independent stacks).
- The `(RATE-A)` conflict is adjudicated, and the adjudication is banked at
  source (`R5_MONOTONICITY_GATE_SOL.md:1063`, D12) — I verified the block
  exists rather than taking block 2's word for it.
- `(H-TRANS)`, the last undischarged gate at the end of pass 2, is
  substantively discharged: `R3_TRANSPORT_EXECUTION_REFEREE.md` confirms
  exactly the three asks block 1 wrote, and its D1/D3 repairs are applied at
  source.
- The Hejhal citation is repaired in both directions — assembly (block 2) and
  source (R3's dated block) now route through Cor. 7.12 p. 579, not (7.22).

### 4.2 What does stand in the way

Four documentation defects. **None is mathematical.** One (F1) is the status
line my brief anticipated; three are hygiene.

| id | defect | where | severity | why the author likely missed it |
|---|---|---|---|---|
| **F1** | `(H-TRANS)` still reads "Status: PAPER-LEVEL, UNREFEREED". Its own discharger now exists and confirms all three named asks. A reader grading the theorem off the gate table would under-rate it by one tier. | block 1, the `(H-TRANS)` row | **BLOCKING for a CONFIRMED grade** (the table would contradict the grade) | Block 2 was written *before* `R3_TRANSPORT_EXECUTION_REFEREE.md` landed, and block 2's own closing line names "a referee for R3_TRANSPORT_EXECUTION ((H-TRANS))" as a remaining discharger. The event happened after the last edit. |
| **F2** | Block 2 says the new `Q_0` supersedes "**§4.5's** boxed value". §4.5 has no box; the boxed `Q_0 = 11761546…` is at **§2:99**. A reader who checks §4.5, finds no box, and returns to §2 may read the §2 box as standing. | block 2, "Q₀ UPDATED BY §10" bullet | LOW (substance is unambiguous — the bullet prints the full `max` in `>=` form — but the pointer is wrong) | §4.5 is where the `>=` discussion lives, so it is the natural mental referent; the box itself is 400 lines earlier. |
| **F3** | §1.1 hash staleness, second instance: `R3_TRANSPORT_EXECUTION_SOL.md` is recorded as `a6b6a129…`; it is now `d53b0ae6…` after its own dated correction block. Block 2 disclosed the `BOUNDARY_ALPHA` drift but not this one. | §1.1; block 2's staleness bullet | LOW (the drift is the append-only D1/D3 repair, which strictly *helps* the assembly) | The R3 block landed after block 2 was written. Same root cause as F1. |
| **F4** | Two vestiges of the abandoned printed-(7.22) route survive: block 2 states "delta = 3/8 (< 1 and < gamma_1/10)", a hypothesis the Cor. 7.12 route does not consume (and which disagrees with the source's own repair, `delta = 1/2`); and `(H-REFL)` lists unitarity `\|phi_q(1/2+it)\| = 1` among consumed hypotheses when the repaired route consumes only `phi_q(s)phi_q(1-s) = 1` plus reality (which together imply unitarity). | block 2, the Hejhal bullet and the `(H-REFL)` row | COSMETIC (both conservative) | Block 2 repaired the *pointer* to Cor. 7.12 but kept the sentence structure of the (7.22) analysis around it. |

**Anomaly raised and RESOLVED.** The dated correction block inside
`R3_TRANSPORT_EXECUTION_SOL.md` is headed **2026-08-21** while its referee is
headed 2026-08-20. I chased this rather than passing it: `date -u` returns
`2026-08-21T04:54Z` against local `2026-08-20 21:54 PDT`, and a concurrent
lane artifact in this repo carries the stamp `bundle_d7_archived_
20260821T045111Z`. The two blocks are therefore the same instant written in
two clock conventions (UTC vs local), not a repair predating or postdating its
own referee. **Not a defect.** Recommendation for the lane, not for this note:
fix one convention, because dated supersession order is this lane's entire
audit mechanism and a one-day UTC skew will eventually invert two blocks
written the same evening.

### 4.3 Answer to the question asked

**It is not "nothing but a status line" — it is a status line plus three
one-line hygiene fixes, all in a single append-only block on one file.** No
new mathematics, no new computation, no new referee is required. Concretely:

- **Target file:** `research_notes/rh_goals_2026-08-14/lane_g/EFFECTIVE_THEOREM_ASSEMBLY_SOL.md`
- **Operation:** append (append-only discipline preserved; body untouched)
- **Also (lane hygiene, optional):** settle on one clock convention for dated
  blocks; the R3 block's `2026-08-21` header is UTC for the same instant its
  referee stamps as 2026-08-20 local.

**Exact promotion text to append:**

```markdown
---

## Dated correction block 3 (2026-08-20, final completeness pass, append-only)

Applied per EFFECTIVE_THEOREM_FINAL_PASS_REFEREE.md (house verdict
CONFIRMED at conditional scope).

- **(H-TRANS) status superseded (F1).**  Block 1's "Status:
  PAPER-LEVEL, UNREFEREED" is stale.  The gate's own named discharger
  has since reported: R3_TRANSPORT_EXECUTION_REFEREE.md (2026-08-20)
  confirms all three asks block 1 wrote — the two-constants
  application (subharmonic maximum principle re-derived; harmonic-
  measure orientation cross-checked by a series-free Monte Carlo), the
  omega(s, Gamma_R; Omega) interval cover (reproduced at a different
  discretisation and phase offset), and the Rouché strictness on
  \partial D_z.  Its blocking defect D1 (Hejhal (7.22) mis-scoped) and
  D3 (unstated real reflection) are APPLIED AT SOURCE in
  R3_TRANSPORT_EXECUTION_SOL.md's dated correction block.  (H-TRANS)
  now reads:

  ### (H-TRANS) — the two-constants/Rouché transport implication itself
  Source R3_TRANSPORT_EXECUTION_SOL.md:60-93,190-231 ((R3-Z), (3.4),
  §4), as repaired by its dated correction block.  Status: ANALYTIC
  CORE REFEREED-CONFIRMED at the stated conditional scope
  (R3_TRANSPORT_EXECUTION_REFEREE.md, attacks 1/2/4/5 CONFIRMED, every
  numeral reproduced at dps = 60); reflection clause repaired at source
  via Hejhal Cor. 7.12 p. 579 + real (7.5) coefficients.  NOT
  discharged by that pass and still carried elsewhere in this table:
  C_R, alpha, q_RATE (= (H-RATE)), q_divisor (= (H-HOL)), and a
  family-uniform K_+ (= (H-SIDE)).  What would discharge the remainder:
  machine formalization.

- **Supersession pointer corrected (F2).**  Block 2's "superseding
  §4.5's boxed value" is a mis-pointer: the boxed Q_0 is at §2 (the
  THEOREM display).  Read: the §2 box Q_0 = 11761546420922598622910053
  339543258496 is superseded BOTH in value (by q_A0''' =
  2810199067910634377586449487575862960) AND in form (equality ->
  the >= form of §4.5, since q_monotone's remainder is unevaluated).
  Independently reproduced this pass: q_side''' = 1134004458443795841,
  q_A0''' = 2810199067910634377586449487575862960, log10 = 36.4487370
  8539722848..., ratio to the old box 4.18530721..., both minimality
  directions and floor-endpoint agreement checked, E_R(q_A0''') <=
  9.890974306e-21 < 117 and K_+^{1-nu} E_R^{nu} < 0.0439 <= m_z both
  re-displayed at the new constant.

- **§1.1 hash staleness, second instance (F3).**
  R3_TRANSPORT_EXECUTION_SOL.md is now d53b0ae62e54fa34d07397807c6173
  15a7bf4f2a964f71b2460e66bf5cb6239e, not the recorded a6b6a1297...;
  the drift is exactly its append-only D1-D6 correction block, which
  strengthens this assembly.  BOUNDARY_ALPHA_THEOREM_SOL.md remains
  58ac377fc29af3daa3d869ec2d3a1dd9db630fdd3b5fa6e4864678cbbc4777d9.

- **(7.22)-route vestiges removed (F4).**  Block 2's "delta = 3/8" is a
  hypothesis of the ABANDONED printed-(7.22) route and is not consumed
  by the Cor. 7.12 route; it is withdrawn (the source's own repair uses
  delta = 1/2 for the same, now-unused, purpose).  (H-REFL) consumes
  exactly: meromorphic continuation of phi_q to C, the unconditional
  functional equation phi_q(s)phi_q(1-s) = 1 (Hejhal Cor. 7.12, p. 579,
  "Proof. Trivial."), and reality phi_q(\bar s) = conj(phi_q(s)) from
  the (7.5) coefficients.  Unitarity |phi_q(1/2+it)| = 1 is a
  CONSEQUENCE of those two, not an additional hypothesis; its listing
  in block 2 is withdrawn as over-broad.

- **(H-C4) evidence base strengthened (recorded, no status change
  claimed here).**  The operative constant is now C_R''' =
  541656022363559883954520, which HAS a repo referee file —
  CR_REDUCTION_V3_REFEREE.md, final verdict "CONFIRMED ... Required
  repairs: none ... fit to be banked as candidates".  Block 2's flag
  that the C_4'' backing quote was a session utterance stands for C_4'';
  it no longer describes the constant actually used.

- **phi_infty holomorphy on \overline{Omega} (recorded).**  Consumed
  inside (H-HOL) and UNCONDITIONALLY PROVED in
  R3_TRANSPORT_EXECUTION_REFEREE.md §4.2 (Gamma factors pole-free since
  Im s in [6.56, 7.57]; zeta(2s-1)'s pole at s = 1 excluded; 4^s != 1
  for Re s > 0; zeta(2s) != 0 by Hadamard-de la Vallee Poussin on
  Re = 1 and the Euler product beyond).  The source bundles it into a
  CONJECTURAL hypothesis; that is conservative, and the only genuinely
  open holomorphy gate is the finite-q one (q_divisor = 3).

STATUS: PROMOTED.  The assembled statement of §2, read with all three
correction blocks, is **CONFIRMED-conditional at paper level on the
EIGHT named gates** (H-RATE Scope 1), (H-HOL), (H-C4), (H-ROUTE),
(H-GEOM), (H-SIDE), (H-TRANS), (H-REFL), at threshold
Q_0 = max{q_RATE, q_divisor, q_side''', q_A0''', q_monotone}
    >= 2810199067910634377586449487575862960.
NOT machine-verified, NOT Lean-formalized, NOT unconditional; the finite
block 3 <= q < Q_0 remains OPEN / UNDEFINED and the remainder of
q_monotone remains CONJECTURAL, so the max is not claimed closed.
```

---

## 5. Side-effect sweep

- **Scope.** This pass wrote exactly one file, the report you are reading. No
  file under review was edited. `git status` shows the target and both prior
  referees unmodified relative to the session start.
- **Deliverable shape.** One report file, in the lane's established
  `*_REFEREE.md` convention, alongside the two prior passes. No stale
  prior-version artifact of this pass exists (no
  `EFFECTIVE_THEOREM_FINAL_PASS_*` predecessor in the directory).
- **No repeated element sampled.** All eight gates were checked, not a
  sample. All seventeen chain-consumed assumptions were enumerated, not a
  sample. Both correction blocks were read line by line. All five
  block-2 numeric assertions were recomputed, not one.
- **Out-of-scope content in the target:** none found. The two correction
  blocks are strictly append-only, additive, and touch no body text; the
  body's superseded numbers are left in place with explicit supersession,
  which is the correct discipline for this lane.
- **Deleted content:** none.

---

## 6. Final house verdict

> # **CONFIRMED at conditional scope.**
>
> The assembled statement of §2, read with both dated correction blocks, is
> **CONFIRMED-conditional at paper level on eight named gates** — (H-RATE)
> Scope 1, (H-HOL), (H-C4), (H-ROUTE), (H-GEOM), (H-SIDE), (H-TRANS),
> (H-REFL) — at threshold
> `Q_0 = max{q_RATE, q_divisor, q_side''', q_A0''', q_monotone} >=
> 2810199067910634377586449487575862960`.
>
> The gate table is complete: a fresh end-to-end walk of (a)->(b)->(c) found
> seventeen consumed assumptions and **every one lies inside the eight
> gates**. No ninth assumption exists. The `E_R = 0` branch is closed, the
> `t_0`/`gamma_1` provenance is a rigorous Arb enclosure reproduced at two
> precisions, `zeta` non-vanishing on `Re = 1` is named inside (H-HOL) and now
> unconditionally proved in a banked referee, and the `q_monotone` remainder
> is correctly carried as an open `>=`. The headline integer, its `log10`, its
> ratio to the superseded box, both minimality directions and both carried
> consequences reproduce digit-for-digit on fresh code.
>
> **Nothing mathematical stands between this note and the grade above.** What
> stands is one stale status line — (H-TRANS) still reads "UNREFEREED" after
> its named discharger reported CONFIRMED and its repairs landed at source —
> plus three documentation-hygiene fixes (a mis-pointed supersession, a second
> hash-staleness instance, and two vestiges of the abandoned (7.22) route).
> All four land in the single append-only block printed at §4.3. Once that
> block is appended, the grade is earned as printed.
>
> Grade limits, restated so no reader over-reads this verdict: the theorem is
> **not** unconditional, **not** machine-verified, **not** Lean-formalized,
> says nothing about `3 <= q < 2.81e36`, and is the tail half of a pincer
> whose other half has no route. §5 of the target says all of this plainly and
> should not be softened on promotion.
>
> One anomaly was raised and closed rather than waved through: the
> `R3_TRANSPORT_EXECUTION_SOL.md` correction block is dated **2026-08-21**
> against its referee's 2026-08-20. It is a UTC-versus-local clock convention
> (`date -u` = 2026-08-21T04:54Z, local = 2026-08-20 21:54 PDT), not a repair
> out of order with its own referee. Not a defect; the lane should still
> settle on one convention.

READY FOR JUDGING
