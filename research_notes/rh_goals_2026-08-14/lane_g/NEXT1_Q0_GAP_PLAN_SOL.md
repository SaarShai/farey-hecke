# NEXT-1 — the Q_0 gap: lever ranking and one executed rung

**STATUS OF THIS WHOLE FILE: UNREFEREED. Everything produced here is
CONJECTURAL / EXPLORATORY. No status of any banked object is upgraded by
this note, and this note edits no other file.** A cold referee runs later.

Append-only. New work goes in a new dated section below; nothing above a
dated header is ever rewritten.

---

## Section 1 (2026-08-22) — decomposition, ranking, and the executed α rung

### 1.0 What this note is and is not

It is (a) a restatement of the current `Q_0` decomposition with each term's
dominant constant-dependence, (b) a ranking of feasible levers by expected
`log10` reduction per unit effort, (c) a dischargeable-vs-open reading of the
eight gates, and (d) **one executed rung** of the top-ranked analytic lever.

It is **not** a theorem, not a promotion, not a referee report, and not a
claim that any threshold below is valid. Every number computed in §1.5–§1.7
is produced under **frozen inputs that the banked assembly does not license
freezing** (named explicitly in §1.7.6). Read those numbers as *sensitivity
estimates*, never as thresholds.

---

### 1.1 Receipts — the exact source statements this note consumes

Quoted verbatim, with file:line, before any claim is made about them.

**R1 — the operative threshold and its decomposition.**
`EFFECTIVE_THEOREM_ASSEMBLY_SOL.md:882-883` (correction block 3, STATUS
PROMOTED):

> ```
> Q_0 = max{q_RATE, q_divisor, q_side''', q_A0''', q_monotone}
>     >= 2810199067910634377586449487575862960.
> ```

and `:786-788` (correction block 2):

> "The theorem's threshold therefore reads Q₀ =
> max{q_RATE, q_divisor, q_side''', q_A0''', q_monotone} ≥
> 2810199067910634377586449487575862960, superseding §4.5's boxed value; all
> conditionality unchanged."

**R2 — the V3 term values, independently reproduced by the final pass.**
`EFFECTIVE_THEOREM_ASSEMBLY_SOL.md:836-839`:

> "Independently reproduced this pass: q_side''' = 1134004458443795841,
> q_A0''' = 2810199067910634377586449487575862960, log10 = 36.4487370
> 8539722848..., ratio to the old box 4.18530721..., both minimality
> directions and floor-endpoint agreement checked, E_R(q_A0''') <=
> 9.890974306e-21 < 117 and K_+^{1-nu} E_R^{nu} < 0.0439 <= m_z both
> re-displayed at the new constant."

**R3 — the two small terms.** `EFFECTIVE_THEOREM_ASSEMBLY_SOL.md:438-439`
(receipt block, unchanged across V1/V2/V3 since neither depends on `C_R`):

> ```
>   q_RATE                       = 12
>   q_divisor                    = 3
> ```

**R4 — the V3 constants.** `BOUNDARY_ALPHA_THEOREM_SOL.md` §10:

> "permit the paper-level coefficient \[ C_4'''=65459394456774532, \] and the
> identical assembly gives the sharper outward minimal ceiling
> \[ \boxed{C_R'''=541656022363559883954520},\qquad \log C_R''' =
> 54.6489\ldots \] — a further \(1.7179\) e-folds below Section 9 (cumulative
> \(30.5945\) below Section 4)."

and, same section:

> "\[ q_{A0}'''=2810199067910634377586449487575862960,\qquad \log q_{A0}''' =
> 83.9263\ldots,\qquad q_{\rm side}'''=1134004458443795841. \]"

**R5 — the closed forms.** `BOUNDARY_ALPHA_THEOREM_SOL.md:629-630` (5.1):

> \[ T:={(1-\nu)\log K_+-\log m\over\alpha\nu}+{1\over\alpha}\log C_R. \]

with, `:604-607`, `K_+=117`, `\nu=0.1552`, `m=0.0439`, `\alpha=6/5`; and the
side branch `T_side = (log C_R - log K_+)/alpha`
(`EFFECTIVE_THEOREM_ASSEMBLY_SOL.md:357`, Stage-2 code).

**R6 — the `C_R`-independent floor.**
`EFFECTIVE_THEOREM_ASSEMBLY_SOL.md:600-604`:

> "\(Q_0\sim C_R^{5/6}e^{T_0}\) and \(e^{T_0}\approx4.7\times10^{16}\) is
> \(C_R\)-independent: it is fixed by \(K_+=117\), \(m_z=0.0439\),
> \(\nu_z=0.1552\), \(\alpha=6/5\) alone. Driving \(C_R''\) to **1** would
> still leave \(Q_0\approx4.7\times10^{16}\)."

**R7 — the elasticities, and the corrected scope.**
`EFFECTIVE_THEOREM_ASSEMBLY_SOL.md:701-707` (correction block 1, D2):

> "nu_z is the most elastic parameter of the C_R-INDEPENDENT FLOOR e^{T_0}
> (elasticity -42.4 vs -38.4 for alpha). For the FULL Q_0 at C_R'', alpha is
> the most elastic parameter (elasticity -85.4), because alpha also discounts
> C_R^{1/alpha}. A geometry change raising alpha dominates one raising nu_z at
> current C_R; only nu_z (or m_z, K_+) moves the floor."

reproduced by `EFFECTIVE_THEOREM_ASSEMBLY_REREFEREE.md:395`:

> "All three independently reproduced: `ν·∂T₀/∂ν = −42.354`,
> `α·∂T₀/∂α = −38.386`, `α·∂logQ₀/∂α = −85.358`."

**R8 — the D12 scope split.** `R5_MONOTONICITY_GATE_SOL.md:1074-1087`:

> ```
> - Positive FULL-BOUNDARY RATE, and family-uniform N-independent whole-tail
>   monotonicity -- i.e. `(RATE-A) with alpha>0` in the form consumed by (G2)
>   ... no RIGOROUS (machine-certified) campaign proves alpha>0. This remains
>   the single standing blocker for the conditional statements above.
>
>   NOT open, and not what this row grades: `(RATE-A)` restricted to the single
>   matched boundary Gamma_R^A with exponent 6/5 and activation q_RATE=12. That
>   statement is CONFIRMED AT PAPER LEVEL ...
> ```

**R9 — the exponent's origin.** `BOUNDARY_ALPHA_THEOREM_SOL.md:238`,
`:253-255`, `:407` and `:529`:

> "Referee-confirmed `(FW)` gives, for \(p=2\sigma\), …"
> "Thus the first two pieces already have exponent \(p-1\). At \(p=11/5\),
> this is \(6/5\)."
> "For \(2<p<3\), positive layer cake now gives …"
> "Set \(p=11/5\)."

with the boundary fixed by `R3_TRANSPORT_EXECUTION_SOL.md:22-52`, quoted in
`EFFECTIVE_THEOREM_ASSEMBLY_SOL.md:70-74`:

> "\(\Omega=\{s:\frac12<\Re s<\frac{11}{10},\ |\Im s-t_0|<\frac12\}\);
> \(\Gamma_R=\{\frac{11}{10}+it:|t-t_0|\le\frac12\}\)"; "\(r_z=\tfrac18\)".

**R10 — what the finite block needs.**
`EFFECTIVE_THEOREM_ASSEMBLY_SOL.md:583-588` quoting
`R5_ACTIVATION_CLOSURE_SOL.md:483-488`, and `:589-604` (four reasons it is
out of reach). Not re-quoted here; it binds §1.8.

---

### 1.2 (a) The decomposition, term by term

`Q_0 = max{q_RATE, q_divisor, q_side''', q_A0''', q_monotone}` (R1). The
`max` is **not claimed closed** — `q_monotone`'s remainder is un-evaluated
(`EFFECTIVE_THEOREM_ASSEMBLY_SOL.md:533-544`), which is why R1 is an
inequality.

| term | value at V3 | closed form | dominant dependence | who moves it |
|---|---|---|---|---|
| `q_RATE` | **12** (R3) | absorption (4.1) at `p`, `q>=12` | none of `C_R,K_+,nu_z,m_z`; depends only on `p` through `F(q)=1/(3-p)+J_2(p)+J_4(p)/q` | (H-RATE) Scope 1 |
| `q_divisor` | **3** (R3) | printed-theory holomorphy | none | (H-HOL) |
| `q_side'''` | **1134004458443795841** (R2) | `floor(exp((log C_R - log K_+)/alpha))+1` | `C_R^{1/alpha}`, `K_+^{-1/alpha}` | (H-C4), (H-SIDE) |
| `q_A0'''` | **2810199067910634377586449487575862960** (R2) | `floor(exp(T))+1`, `T` as in R5 | `e^{T_0} * C_R^{1/alpha}`, `T_0=((1-nu)log K_+ - log m)/(alpha nu)` | (H-C4), (H-SIDE), (H-GEOM) |
| `q_monotone` | **un-evaluated remainder** | — | — | (H-RATE)/(H-ROUTE) scope |

`q_A0'''` is the binding term, by 18 orders of magnitude over `q_side'''` and
by 36 over `q_RATE`. **Every lever below is therefore a lever on `T`.**

`T` splits as
```
log Q_0  =  T_0  +  (log C_R)/alpha
T_0      =  ((1 - nu_z) log K_+  -  log m_z) / (alpha * nu_z)
```
At V3 constants this reads (reproduced §1.5, receipt R11):
`log10 Q_0 = 16.6706 + 19.7780 = 36.4487` — i.e. **the floor `e^{T_0}` is
already 46% of the exponent, and no `C_R` work can touch it** (R6).

**A derived identity worth stating, because it deflates R7's headline number.**
With `nu_z, m_z, K_+, C_R` frozen, `log Q_0 = A/alpha` for a constant `A`.
Hence identically
```
alpha * d(log Q_0)/d(alpha)  =  - log Q_0.
```
Check against R7: the banked elasticity `-85.358` at `C_R''` equals minus the
banked `log q_A0'' = 85.3579...`
(`EFFECTIVE_THEOREM_ASSEMBLY_SOL.md:441` prints `q_A0_pp` whose log is
`85.35789877...` at `:434`). At `C_R'''` the same quantity is
`-83.9263` (R4's `log q_A0''' = 83.9263`). **So the "-85.4 elasticity" is not
a measurement of how much `alpha` can buy; it is a restatement of how large
`Q_0` is.** Any parameter entering as an overall `1/alpha` has that
elasticity by definition. This does not refute R7 — R7 is arithmetically
correct and its own scope sentence is careful — but it means the ranking
below must be built on **constrained** derivatives (moving `alpha` along the
geometry it is tied to), not on frozen-parameter elasticities. That
observation is what motivated the executed rung in §1.5.

---

### 1.3 (b) Lever ranking

Effort classes: **E1** = re-run existing certified machinery at new
parameters (an Arb cover, a beta integral); **E2** = re-audit a banked
paper-level chain at a shifted parameter; **E3** = new mathematics.

Reductions are in `log10 Q_0`. To keep the arithmetic internally consistent
they are measured against **this note's own calibration baseline
`log10 Q_0 = 36.4190`** (§1.5.2, which uses this note's `m_z = 0.04444`
rather than the banked floor `0.0439`); against the banked `36.4487` (R2)
every figure below is a further `0.03` larger. All are **CONJECTURAL
estimates from §1.5–§1.7**, under the frozen inputs of §1.7.6.

| # | lever | est. Δlog10 | effort | per-unit-effort | evidence |
|---|---|---|---|---|---|
| **L1** | **`Omega` aspect ratio** — raise the rectangle height from `H=1` to `H≈6`, `sigma` unchanged | **−4.59** | E1 (+E2 for `K_+`) | **best** | §1.5.3, §1.6 |
| **L2** | **`r_z`** — shrink the transport disc from `1/8` to `≈1/40` | **−6.97** alone; L1+L2 together **−9.40** | E1 (+E2) | **best** | §1.6 |
| **L3** | **`alpha` via `sigma`** — move `Gamma_R` right, `alpha = 2*sigma - 1` | **−0.57 alone at `H=1`; +10.43 (WORSE) if pushed to `sigma=1.48` at `H=1`; −8.23 marginal once L1+L2 are in place** | E2 (whole §2–§4 chain at `p=2 sigma`) | conditional — see §1.5 | §1.5, §1.6 |
| **L1+L2+L3 joint** | `sigma=1.48, H=6, r_z=0.025` | **−17.63** (to `log10 Q_0 ≈ 18.79`) | E1+E2 | — | §1.6 |
| **L4** | **`K_+` sharpening** (117 → smaller) | `d log Q_0 / d log K_+ = (1-nu)/(alpha nu) = 4.5361` at banked geometry; 117→10 buys **−4.84** | E3 (the gate is only conditional today) | medium | §1.7.2 |
| **L5** | **further `C_4` / `C_R` shaving** | remaining headroom to the floor is **−19.78** total, but at `1/alpha = 0.833 log10` per e-fold, and V1→V3 spent three referee cycles for 30.59 e-folds = −25.5 | E2 per step, and the cheap substitutions are spent | **declining** | R4, §1.7.3 |
| **L6** | **gate consolidation** (see §1.4) | **0.00** | E2/E3 | n/a for `Q_0` | §1.4 |
| **L7** | **exponent beyond `alpha >= 2`** (`p >= 3`) | unbounded in principle | **E3, blocked** | — | §1.7.4 |

**Ranking commentary.**

1. **The geometry levers (L1, L2) dominate and are the cheapest.** They move
   the `C_R`-independent floor, which is the half of the exponent that
   constant-shaving provably cannot reach (R6). Both consume only
   recomputation of objects that already have certified machinery: the
   harmonic-measure cover for `nu_z` and the `phi_infty` minimum cover for
   `m_z` (both graded **PROVED, Arb interval cover** at
   `EFFECTIVE_THEOREM_ASSEMBLY_SOL.md:243-247`).
2. **L3 is NOT a standalone lever and R7's steering sentence should not be
   read as saying it is.** §1.5 shows `alpha` is bound to `nu_z` through the
   same wall position: raising `sigma` pushes `Gamma_R` away from `D_z` and
   `nu_z` falls. At the banked `H=1` the two effects nearly cancel (best
   available `−0.57` at `sigma≈1.16`) and then **reverse** (`sigma=1.48` at
   `H=1` gives `+10.40`, i.e. `Q_0` ten orders **worse**). L3 pays only
   *after* L1 has lifted `nu_z` toward its strip limit.
3. **L5 is the most-worked and now the least productive lever.** Its remaining
   total headroom (−19.78) is larger than L1+L2, but that is the headroom to
   `C_R = 1`, which is unattainable; and R4 records the V3 step as three
   further substitutions inside the atom bridge for 1.7179 e-folds = −0.62
   log10. At that rate L5 is roughly **−0.6 log10 per full referee cycle**,
   versus L1's **−4.59 for one Arb cover re-run**.
4. **L6 buys zero `log10`.** Gate work changes the theorem's *status*, not its
   threshold. It is nonetheless the higher-value axis if the goal is a
   publishable statement rather than a smaller number — see §1.8.

---

### 1.4 (c) The eight gates: dischargeable vs genuinely open

Statuses below are **the banked ones**, unchanged. The "verdict" column is
this note's UNREFEREED reading of *dischargeability*, not of truth.

| gate | banked status (verbatim source) | this note's read |
|---|---|---|
| **(H-RATE) Scope 1** | "CONFIRMED-conditional (paper level)" (`EFFECTIVE_THEOREM_ASSEMBLY_SOL.md:775-780`); R8 confirms Scope 1 is *not* what the OPEN rows grade | **DISCHARGEABLE (formalization only)** |
| **(H-HOL)** | "PROVED from printed theory" (`:250-252`) | **DISCHARGED** for the domains used |
| **(H-C4)** | "CONFIRMED ... Required repairs: none ... fit to be banked as candidates" (`CR_REDUCTION_V3_REFEREE.md`, quoted at `:865-869`) | **DISCHARGEABLE (banking act)** |
| **(H-ROUTE)** | "PROVED (domain correction), and BINDING on this note" (`:305`) | **DISCHARGED** (a constraint, honoured) |
| **(H-GEOM)** | "PROVED (Arb interval cover)" (`:245-247`) | **DISCHARGED** |
| **(H-SIDE)** | "CONFIRMED-conditional source input" (`:270`); historical row "CONJECTURAL / MISSING family-uniformly" (`R3_TRANSPORT_EXECUTION_SOL.md:250`) superseded only conditionally | **GENUINELY OPEN** |
| **(H-TRANS)** | "ANALYTIC CORE REFEREED-CONFIRMED at the stated conditional scope" (`:844-852`) | **DISCHARGEABLE (formalization only)** |
| **(H-REFL)** | "PRINTED-LITERATURE, same tier as (H-RATE)'s printed inputs" (`:781-786`, narrowed by F4 at `:871-878`) | **DISCHARGED** modulo citation hygiene |

**Discharge sketch / blocker, one paragraph each.**

- **(H-RATE) Scope 1 — dischargeable.** R8 settles the ledger conflict as a
  scope split, so nothing mathematical is missing: what remains is machine
  formalization of `BOUNDARY_ALPHA_THEOREM_SOL.md` §§3–4, whose sub-inputs
  `(FW)` and `(DH_{2,4})` are each separately referee-CONFIRMED at paper level
  (`EFFECTIVE_THEOREM_ASSEMBLY_SOL.md:194-195`). *Blocker:* none identified;
  cost only. **Caution:** Scope 2 (full-boundary rate + family-uniform
  whole-tail monotonicity) is **GENUINELY OPEN** per R8 and is *not* assumed
  by the theorem — but it *is* what `q_monotone`'s remainder lives in, so
  Scope 2 remains the reason R1 is an inequality.
- **(H-HOL) — discharged.** `q_divisor = 3`; it contributes the smallest term
  in the max and cannot bind.
- **(H-C4) — dischargeable by a banking act.** The constant now in use,
  `C_R'''`, has a repo referee file with "Required repairs: none". The
  residual is that `CR_REDUCTION_V3_SOL.md` self-grades its outputs
  "candidates". *Blocker:* administrative, not mathematical.
- **(H-ROUTE) — discharged.** It forbids mixing the Route-B sixth-zero wall
  with first-zero A0 quantities; the assembly consumes `K_+, m_z, nu_z` only.
  Any geometry change in §1.5–§1.6 must re-honour it: a new `Omega` must be
  re-declared as a first-zero A0 ledger, never silently paired with `K_F=109`.
- **(H-GEOM) — discharged, and the *most reusable* asset here.** Both floors
  are Arb interval covers of concrete functions. §1.5–§1.6 recompute the same
  two objects at new geometry with ordinary floating point; converting those
  to interval covers is exactly the existing machinery re-run.
- **(H-SIDE) — genuinely open.** `K_+=117` is conditional on full-width `H_0`
  and the anchor gate, and the family-uniformity concern is "answered
  conditionally, not removed" (`EFFECTIVE_THEOREM_ASSEMBLY_SOL.md:271-274`).
  *Blocker:* an unconditional family-uniform bound on `sup|F_q|` over the
  three non-RATE sides. This is also the gate every geometry lever leans on
  (§1.7.6), which makes it the single highest-value open item on the page.
- **(H-TRANS) — dischargeable (formalization only).** Its named discharger
  reported: `R3_TRANSPORT_EXECUTION_REFEREE.md` confirms the two-constants
  application, the `omega(s,Gamma_R;Omega)` interval cover, and Rouché
  strictness. *Blocker:* none mathematical; but note the referee explicitly
  did **not** discharge `C_R, alpha, q_RATE, q_divisor`, or a family-uniform
  `K_+`, so it does not help (H-SIDE).
- **(H-REFL) — discharged modulo citation.** Repaired at source to the
  unconditional `phi_q(s) phi_q(1-s) = 1` (Hejhal Cor. 7.12, p. 579) plus
  reality of the (7.5) coefficients; unitarity was withdrawn as an
  over-broad extra hypothesis. *Blocker:* the printed page must be asserted
  in-range before paper-level citation (D4/F4 chain).

**Net.** Seven of eight gates are dischargeable or discharged in the sense
above; **(H-SIDE) is the one genuinely open gate**, and it is also the one
that every lever in §1.3 must pay a tax to. That is the single most useful
output of part (c).

---

### 1.5 (d) THE EXECUTED RUNG — the sharpened `alpha` derivation

**The lever, stated exactly.** By R9, the boundary exponent is not a free
parameter: `alpha = p - 1` and `p = 2*sigma`, where `sigma = Re s` on
`Gamma_R`. The banked choice `sigma = 11/10` gives `p = 11/5` and
`alpha = 6/5`. The layer-cake (3.10) is valid for `2 < p < 3`, i.e.

```
1 < sigma < 3/2,      alpha = 2*sigma - 1  in  (1, 2).
```

So "sharpening `alpha`" **means moving the right wall of `Omega` to the
right**. There is no other route to it inside this chain.

**The constraint that R7's frozen elasticity omits.** `Gamma_R` is also the
edge whose harmonic measure defines `nu_z`. Moving it right moves it *away*
from `D_z`, so `nu_z` falls. `alpha` and `nu_z` are therefore **not
independent**, and the quantity that actually enters `T_0` is the product
`alpha * nu_z`.

#### 1.5.1 Method

All inequalities are re-derived, not assumed:

1. **`nu_z(sigma, H)`.** `Omega` is the rectangle
   `{1/2 < Re s < sigma, |Im s - t_0| < H/2}` (banked case `sigma = 11/10`,
   `H = 1`). Put `x = Re s - 1/2 in [0, w]`, `w = sigma - 1/2`, and
   `y = Im s - t_0 + H/2 in [0, H]`. The harmonic measure of the right edge
   solves Laplace's equation with boundary data `1` on `x = w`, `0` elsewhere;
   separation of variables gives the (uniformly convergent, termwise positive
   on the relevant range) series
   ```
   omega(x,y) = sum_{n odd} (4/(n pi)) sin(n pi y / H) sinh(n pi x / H) / sinh(n pi w / H).
   ```
   `nu_z = inf_{partial D_z} omega`. Evaluated with 400 odd modes (tail
   `< e^{-800 pi (w-x)/H}`, and `w - x >= 0.145` in every case run) at 1440–2880
   equispaced points of `partial D_z`; the reported value is then **floored to
   4 or 5 decimals (margin DOWN)**.
2. **`m_z(r_z)`.** `m_z = min_{|s - z_0| = r_z} |phi_infty(s)|` with
   `phi_infty` exactly as in `EFFECTIVE_THEOREM_ASSEMBLY_SOL.md:76-78`,
   `z_0 = 3/4 + i gamma_1/2`, evaluated at 360–720 boundary points, **floored
   (margin DOWN)**.
3. **`C_R(sigma, H)`.** The §4 assembly of R4/R9 re-run at general `p = 2 sigma`:
   ```
   C_R = M_0(sigma) * [ 2 pi^2 (S+1) p C_4''' F(12)  +  p * 128 (1+log 2) * G(p) ]
   F(q) = 1/(3-p) + J_2(p) + J_4(p)/q
   J_2(p) = 1/(p-2) + 2/(p-2)^2 + 2/(p-2)^3
   J_4(p) = 1/(p-2) + 4/(p-2)^2 + 12/(p-2)^3 + 24/(p-2)^4 + 24/(p-2)^5
   G(p)   = 1/(p-2) + 1/(p-2)^2
   S      = sup_{Gamma_R} |s| = sqrt(sigma^2 + (t_0 + H/2)^2)
   M_0(sigma) = B(sigma - 1/2, 1/2)
   ```
   `S` and `M_0` are **ceiled to 3 decimals (margin UP)**. `C_4'''` is held at
   R4's value: the atom-bridge count `W_q(Y)` it bounds is `p`-free
   (`BOUNDARY_ALPHA_THEOREM_SOL.md:407-418`), so this freeze is legitimate.
   `M_0(sigma) = B(sigma-1/2, 1/2)` is **decreasing in `sigma`**, since the
   integrand `u^{sigma-3/2}(1-u)^{-1/2}` decreases pointwise on `(0,1)`
   (`M3_UNIFORMITY_EXECUTION_SOL.md:255-275`, quoted at
   `EFFECTIVE_THEOREM_ASSEMBLY_SOL.md:200`) — so raising `sigma` moves this
   factor in the **favourable** direction, and the recomputation is legitimate
   rather than a freeze.
4. **`log Q_0`** from R5 with `K_+ = 117` frozen (see §1.7.6).

#### 1.5.2 Calibration — the method reproduces three banked constants

Run at the banked geometry `sigma = 1.1, H = 1, r_z = 1/8`:

```
nu_z computed  = 0.1552145055111849       banked floor: 0.1552          [R5]
m_z computed   = 0.04444150               banked floor: 0.0439          [R5]
log10 C_R      = 23.733673                banked: 54.6489/ln10 = 23.7337 [R4]
log10 Q_0      = 36.448695  (at nu=0.1552) banked: 36.44873708          [R2]
```

**Receipt R11.** All four agree. The two floors sit *below* the raw computed
values, i.e. the banked constants are conservative in the direction the
assembly needs, exactly as `:451-457` asserts. The residual `4.2e-5` in
`log10 Q_0` is explained: the banked assembly uses the rounded-up
`S = 7.648` where the exact value is `7.6468932...`; a `1.28e-4` relative
increase in `(S+1)`, scaled by `5/6`, is `4.3e-5` in `log10`. **My numbers are
therefore ~4e-5 optimistic relative to banked, uniformly. Recorded, not
corrected.**

#### 1.5.3 The rung: `log10 Q_0` as `sigma` moves, with `nu_z` recomputed

`H = 1` (banked height), `r_z = 1/8` (banked radius), `nu_z` floored:

| `sigma` | `alpha` | `nu_z` (raw) | `log10 C_R` | **`log10 Q_0`** | `log10 Q_0` if `nu_z` FROZEN at 0.1552 |
|---|---|---|---|---|---|
| 1.06 | 1.12 | 0.175910 | 24.7809 | 37.6680 | 39.9872 |
| 1.08 | 1.16 | 0.165236 | 24.1866 | 36.9442 | 38.0960 |
| **1.10** | **1.20** | **0.155215** | **23.7337** | **36.4487** | **36.4487** |
| 1.12 | 1.24 | 0.145802 | 23.3610 | 36.1200 | 34.9800 |
| 1.14 | 1.28 | 0.136960 | 23.0508 | 35.9423 | 33.6518 |
| **1.16** | **1.32** | **0.128654** | **22.7870** | **35.8768** ← min | 32.4388 |
| 1.18 | 1.36 | 0.120850 | 22.5586 | 35.9184 | 31.3231 |
| 1.20 | 1.40 | 0.113518 | 22.3587 | 36.0522 | 30.2912 |
| 1.30 | 1.60 | 0.082992 | 21.7264 | 38.1136 | 26.0820 |
| 1.48 | 1.96 | 0.056… | 21.4842 | **46.8492** | 22.9859 |

**RUNG OUTCOME — the honest result.**

1. **The `alpha` lever is real but shallow.** With `nu_z` recomputed
   honestly, `log10 Q_0` is minimised at `sigma ≈ 1.16` (`alpha = 1.32`) at
   `35.8768`, a reduction of **0.5719 log10 — a factor 3.73** — from the
   banked `36.4487`.
2. **The frozen-`nu_z` column is a mirage.** It shows `−13.5 log10` by
   `sigma = 1.48`. The honest column shows `+10.40` there. The frozen column
   is the picture R7's `−85.4` elasticity paints; §1.2's identity says why
   that number cannot be read as achievable reduction.
3. **The constrained elasticity is `−24.9`, not `−85.4`.** From the table,
   `d(log Q_0)/d(sigma) ≈ (36.2683 - 36.4487)*ln(10)/0.01 = -41.5` at
   `sigma = 1.1`; with `d(alpha) = 2 d(sigma)`, `alpha * d(log Q_0)/d(alpha)
   = 1.2 * (-41.5/2) = -24.9`. It falls to `0` at `sigma = 1.16` and turns
   positive after.
4. **The floor moves the wrong way.** `e^{T_0}` at `sigma = 1.1` is
   `10^{16.6706}` (= `4.68e16`, reproducing R6's `4.7e16`); at `sigma = 1.16`
   it is `10^{18.6139}`. **The `alpha` rung buys `0.57` today and raises the
   irreducible floor by `1.94` orders**, so it also devalues all future L5
   work.
5. **The gain is fragile against the open gate.** At `sigma = 1.16`,
   `d(log Q_0)/d(log K_+) = (1-nu)/(alpha nu) = 5.1334`. A `K_+` growth of
   only `exp(0.5719 * ln10 / 5.1334) = 1.29x` on the wider `Omega` erases the
   entire gain. Since `Omega` grows, `K_+` — a supremum over a larger set —
   can only grow or stay equal. **On its own, L3 is not worth taking.**

**Verdict on the rung: NEGATIVE-ish but informative.** The sharpened `alpha`
derivation succeeds analytically (`alpha` up to `1.32` is available inside
the `2<p<3` constraint with all constants recomputed) and fails economically
(`−0.57 log10`, wiped out by a `1.29x` move in the one genuinely open gate).
**This is the precise blocker requested: not that `alpha` cannot be raised,
but that `alpha * nu_z` is the invariant and raising `sigma` alone leaves it
almost unchanged.**

---

### 1.6 What the rung uncovered — the `alpha * nu_z` invariant, and two better levers

The rung's own algebra points at the fix. In the **tall-rectangle (strip)
limit** `H -> infinity`, the harmonic measure of the right edge of a vertical
strip is exactly linear, `omega(x) = x/w`. At the leftmost point of
`partial D_z`, `x = (Re z_0 - r_z) - 1/2`, so

```
nu_z  ->  (Re z_0 - r_z - 1/2) / w,        w = sigma - 1/2,   alpha = 2w,
```
hence
```
alpha * nu_z  ->  2 * (Re z_0 - r_z - 1/2)     — INDEPENDENT OF sigma.
```

At the banked geometry `Re z_0 = 3/4`, `r_z = 1/8`, this is `2*(1/8) = 1/4`.
Two consequences, both **CONJECTURAL/UNREFEREED**:

- **`sigma` is asymptotically free.** Once `H` is large enough for the strip
  limit, raising `sigma` raises `alpha` at **no cost in `alpha*nu_z`**, so the
  `(log C_R)/alpha` term shrinks with nothing pushing back. That is why L3
  only pays after L1.
- **The floor is governed by one number,
  `d := Re z_0 - r_z - 1/2 = 1/8`** — the distance from the left edge of `D_z`
  to the critical line. `Re z_0 = 3/4` is forced (`z_0 = (1+rho_1)/2` and
  `Re rho_1 = 1/2`). **`r_z` is not forced.** Shrinking `r_z` raises `d`, and
  costs only through `m_z`, which is roughly linear in `r_z` near a simple
  zero.

**Computed `m_z(r_z)`** (this note, `phi_infty` evaluated directly; values
floored):

| `r_z` | `m_z` | `m_z / r_z` |
|---|---|---|
| 0.125 | 0.0444415 | 0.3555 |
| 0.080 | 0.0323279 | 0.4041 |
| 0.050 | 0.0220696 | 0.4414 |
| 0.030 | 0.0140649 | 0.4688 |
| 0.025 | 0.0123394 | 0.4746 |
| 0.020 | 0.0096683 | 0.4834 |
| 0.015 | 0.0073640 | 0.4909 |

(`m_z/r_z -> |phi_infty'(z_0)| ≈ 0.5` as `r_z -> 0`, as a simple zero
requires — an internal consistency check.)

**Joint scan** (`nu_z, m_z` recomputed and floored; `S, M_0` ceiled;
`K_+ = 117` frozen; `C_4'''` frozen):

| `sigma` | `H` | `r_z` | `nu_z` | `m_z` | `log10 e^{T_0}` | **`log10 Q_0`** | Δ vs 36.4190 |
|---|---|---|---|---|---|---|---|
| 1.10 | 1 | 0.125 | 0.15521 | 0.04444 | 16.6409 | 36.4190 | 0 (calibration) |
| 1.16 | 1 | 0.125 | 0.12865 | 0.04444 | 18.6139 | 35.8768 | −0.54 |
| 1.48 | 1 | 0.125 | (small) | 0.04444 | — | 46.8492 | **+10.43** |
| 1.10 | 6 | 0.125 | 0.20830 | 0.04444 | — | 31.8277 | −4.59 |
| 1.10 | 1 | 0.025 | — | 0.01234 | — | 29.4456 | −6.97 |
| 1.10 | 6 | 0.025 | — | 0.01234 | — | 27.0186 | −9.40 |
| 1.48 | 1 | 0.025 | — | 0.01234 | — | 32.5580 | −3.86 |
| 1.48 | 6 | 0.125 | 0.12751 | 0.04444 | 12.6309 | 23.6022 | −12.82 |
| **1.48** | **6** | **0.025** | **0.22953** | **0.01190** | **7.8197** | **18.7911** | **−17.63** |

At the joint point, `alpha * nu_z = 1.96 * 0.22953 = 0.4499` versus
`1.2 * 0.15521 = 0.1863` at the banked point — a **2.4x** improvement in the
one invariant that matters, and the source of essentially the whole gain.

**Robustness of the joint point against the open gate.** At the joint point
`d(log Q_0)/d(log K_+) = (1-nu)/(alpha nu) = 1.713`. `K_+` would have to grow
by a factor `10^{17.63/1.713} ≈ 2.0e10` to erase the gain — versus `1.29x`
for the `alpha`-only rung. **The joint lever is ~10 orders more robust
against (H-SIDE) than the `alpha` lever alone.** That, not the raw `−17.63`,
is the reason to rank L1/L2 first.

**Bonus, recorded:** shrinking `r_z` also *strengthens* the theorem's
conclusion (c). At `r_z = 1/40` the localization becomes
`0.725 <= Re s_q <= 0.775`, `|Im s_q - gamma_1/2| <= 1/40`, in place of
`5/8 <= Re s_q <= 7/8`. A lever that improves both the threshold and the
conclusion is unusual and should be taken first.

---

### 1.7 Everything that is wrong with §1.5–§1.6 — read before quoting any number

#### 1.7.1 Status
**UNREFEREED. CONJECTURAL. Not a theorem. Not machine-verified.** No banked
constant is superseded. `Q_0` remains R1.

#### 1.7.2 `K_+` is FROZEN and this is the load-bearing optimism
Every table above holds `K_+ = 117`. `K_+` is a supremum of `|F_q|` over the
three non-`Gamma_R` sides of `partial Omega`. **Enlarging `Omega` enlarges
that set, so the true `K_+` on the modified `Omega` is `>= 117`.** Nothing
here bounds it. Sensitivity is given in §1.5(5) and §1.6. Any use of §1.6's
numbers must first discharge (H-SIDE) at the new geometry — which is
precisely the one gate §1.4 grades **GENUINELY OPEN**.

#### 1.7.3 The §2–§4 chain is not re-audited at `p != 11/5`
R9's chain is *stated* at `p = 11/5`. The re-run in §1.5.1(3) assumes the
following are `p`-uniform, and **each is an unverified assumption of this
note**: the Route-B/Ford premises; `C_4'''` (argued `p`-free above, but not
refereed at general `p`); the endpoint comparison `x_W <= y_W`; the
complex-power MVT step (3.12), whose stated validity condition
`sigma > -1/2` is satisfied but whose constants were not re-checked;
`(FW)`'s (2.3) at general `p > 2`; and `q_RATE = 12`, whose absorption (4.1)
I re-derived as `F(12) = 36.86` at `p = 2.96` versus `7940` at `p = 2.2` —
i.e. **easier**, so `q_RATE <= 12` appears to survive, but this is not
refereed.

#### 1.7.4 `alpha >= 2` is blocked, not merely unattempted
`p >= 3` makes `1/(3-p)` in (3.10) infinite. Reaching `alpha >= 2` requires a
new layer-cake with a different Ford/two-mark count, i.e. **E3 new
mathematics**. Recorded as L7; not attempted.

#### 1.7.5 Numerical hygiene
Float64 with mpmath only for `Gamma/zeta/B`; **no interval arithmetic**;
`nu_z` from a 1440–2880-point sample of `partial D_z`, not a certified
infimum; `m_z` from a 360–720-point sample. Margins were rounded **DOWN**
(`nu_z`, `m_z`: floor) and upper bounds **UP** (`S`, `M_0`: ceil), which is
the correct direction, but sampling error is not bounded. Calibration §1.5.2
is the only evidence of correctness. **These are not certified numbers.**

#### 1.7.6 Complete list of frozen inputs
`K_+ = 117` (unlicensed, §1.7.2); `C_4''' = 65459394456774532` (argued
`p`-free); the `(H-RATE)` Scope-1 chain at `p != 11/5` (§1.7.3);
`q_monotone`'s remainder (untouched, so R1 stays an inequality at every
geometry); `t_0 = gamma_1/2` and `Re z_0 = 3/4` (forced). `H > gamma_2 -
gamma_1 = 6.888` would admit `(1+rho_2)/2` into `Omega`; `H = 6` stays below
that, which is why the scan stops there — recorded as an observation, not a
proof that anything breaks above it.

#### 1.7.7 What is NOT claimed
That `log10 Q_0 = 18.79` is attainable. That the geometry may be changed at
all — (H-ROUTE) requires any new `Omega` to be re-declared as a first-zero A0
ledger. That the rung improves the theorem. That any gate is discharged.

---

### 1.8 Bottom line, and the honest bound on this whole programme

- **The `alpha` rung is executed and its outcome is `−0.57 log10`, with the
  precise blocker identified:** `alpha` and `nu_z` are tied by the same wall,
  the invariant is `alpha * nu_z`, and at the banked aspect ratio moving
  `sigma` leaves it nearly fixed — then makes it worse.
- **The ranking that came out of the rung inverts the banked steering
  sentence's practical reading:** the cheap wins are `H` (aspect ratio) and
  `r_z` (disc radius), not `alpha`, and not further `C_R` shaving.
- **Even the full joint optimum does not close the gap.** `10^{18.79}` against
  certified computations at `q <= 21` leaves **seventeen orders of
  magnitude**. `EFFECTIVE_THEOREM_ASSEMBLY_SOL.md:589-604` already says
  constant-shaving cannot rescue this and that a finite-base *theorem* is
  needed; **this note's independent conclusion is the same, and the levers
  above do not change it.** They are worth taking to make the effective
  statement less embarrassing and to make (H-SIDE) the single named blocker,
  not to bridge to computation.
- **Recommended next lane, in order:** (i) re-derive `K_+` on a tall/thin
  `Omega` — it is simultaneously the open gate and the tax on every lever;
  (ii) re-run the two Arb covers (`nu_z`, `m_z`) at `(sigma, H, r_z)` from
  §1.6 to convert §1.6 from float to certified; (iii) only then re-audit the
  §2–§4 chain at `p = 2 sigma`.

---

**READY FOR JUDGING — UNREFEREED, CONJECTURAL THROUGHOUT.**

Reproduction scripts for §1.5–§1.6 (written fresh for this note):
`<scratchpad>/alpha_rung2.py`, `alpha_rung3.py`, `alpha_rung4.py`,
`final.py`, `mz.py`, `joint.py` under
`/private/tmp/claude-501/-Users-za-Documents-farey-hecke/d132431f-d2c6-4401-96d1-90f58d3026fb/scratchpad/`.
They are temporary; the method in §1.5.1 is complete enough to rebuild them.

---

## Section 2 — Correction block (2026-08-23, from NEXT1_Q0_GAP_PLAN_REFEREE.md)

**Append-only.** Nothing in Section 1 is edited, deleted or rewritten. Every
item below is the cold referee's finding, quoted with its line numbers in
`NEXT1_Q0_GAP_PLAN_REFEREE.md`. Where Section 1 and this block disagree,
**this block governs.** House verdict (referee `:24-25`):
"CONFIRMED-with-corrections on Claims 1-3. Claim 4 (the gate audit) is
REFUTED as stated."

### D2 — §1.5.3's `sigma = 1.48` row (referee `:304-326`)

The printed row is a composite of three different runs; three of four cells
are wrong. Under §1.5's own stated method (`H = 1`, `r_z = 1/8`, `M_0`
recomputed, `nu_z` floored 4dp, `m = 0.0439`) the correct per-column values
are (referee `:309-311`):

| column | printed (§1.5.3) | **correct** |
|---|---|---|
| `nu_z` (raw) | `0.056…` | **0.047187** |
| `log10 C_R` | `21.4842` | **21.3956** |
| `log10 Q_0` | `46.8492` | **46.9696** |
| `log10 Q_0` (`nu_z` FROZEN) | `22.9859` | **21.1226** |

Provenance of the wrong cells (referee `:316-320`): `0.056…` is `nu_z` at
`sigma = 1.42`; `21.4842` is `log10 C_R` at `sigma = 1.48, H = 5`; `22.9859`
is the frozen-`nu_z` value at `sigma = 1.40`; `46.8492` corresponds to
`nu_z ≈ 0.0473`, matching neither. Direction (referee `:323-325`): the
printed `Q_0` is `0.12 log10` **more favourable** than honest, so §1.3/§1.5's
"`+10.40` worse" is an understatement — honest is **+10.52**. No conclusion
moves. Also D1 (referee `:278-302`): rows `1.06`, `1.08`, `1.30` and the
whole frozen-`nu_z` column were run with `M_0` **frozen** at `2.775`, against
§1.5.1(3)'s declared recomputation; the two `Q_0` columns of a single row are
not comparable.

### D3 — the `r_z = 0.026` mislabel (referee `:328-350`)

§1.6's `m_z` table row labelled `r_z = 0.025` is in fact `r_z = 0.026`:
`m_z(0.026) = 0.0123393745`, `m_z/r = 0.474591` — exactly the printed pair.
The true `r_z = 0.025` row is `m_z = 0.0119011586`, `m_z/r = 0.476046`.
**Computations are unaffected**: the referee confirms (`:346-349`) the
computation used `m_z = 0.01190` throughout — `29.4456`, `27.0186`,
`32.5580` reproduce exactly with `0.01190` and do **not** reproduce with
`0.01234`. Display defect only; the three joint-scan cells printing
`m_z = 0.01234` should read `0.01190`. All other rows of the table reproduce
to the printed digit.

### D6a — the nine corrected line receipts (referee `:376-404`)

All eight `file:line` pointers in §1.4 point at the wrong lines; the quoted
strings are genuine. Corrected receipts against
`EFFECTIVE_THEOREM_ASSEMBLY_SOL.md` (referee `:383-393`):

| # | receipt | §1.4 cites | **correct line** |
|---|---|---|---|
| 1 | (H-RATE) | `:775-780` | **165** (and `:748` for the superseding read) |
| 2 | (H-HOL) | `:250-252` | **213** (`:250-252` is the (H-SIDE) quote) |
| 3 | (H-ROUTE) | `:305` | **300** (`:305` reads "nothing — it is a constraint") |
| 4 | (H-GEOM) | `:245-247` (and `:243-247` in §1.3) | **235** |
| 5 | (H-SIDE) | `:270` | **255** (`:270` is the (H-C4) quote) |
| 6 | (H-TRANS) | `:844-852` | **820** |
| 7 | (H-REFL) | `:781-786` | **766** |
| 8 | (H-SIDE) detail, "answered conditionally, not removed" | `:271-274` | **258** |
| 9 | (H-REFL) "narrowed by F4" | `:871-878` | **850-856** |

((H-C4)'s `:865-869` vs actual `864` the referee grades "acceptable",
`:385`.) Further corrections outside the table (referee `:395-399`):
`BOUNDARY_ALPHA_THEOREM_SOL.md:407` (R9c) is actually **`:433`**; `:238` is
**`:237`**; the `phi_infty` definition cited as `EFFECTIVE:76-78` is at
**`:80-81`**; and §1.2's "`85.35789877...` at `:434`" is at **`:428`**
(`:434` is the Route-B `K_F=109` diagnostic line).

### D6b — the elided R8 clause, restored verbatim (referee `:406-418`)

R8 (§1.1) elides the load-bearing clause. The source
(`R5_MONOTONICITY_GATE_SOL.md` D12) reads, restored verbatim:

> "... in the form consumed by (G2) **and by the R5/DH2 activation, which
> additionally requires N-independent `K_+`, `K_F`, `nu_seed`, `omega_*`.
> Unchanged by this note;** no RIGOROUS ... campaign proves alpha>0."

**Consequence (referee `:414-418`):** the omitted clause states that the open
Scope-2 blocker *additionally requires a family-uniform `K_+`*. Scope 2 is
therefore **coupled to (H-SIDE)**, and **(H-SIDE) is NOT isolable as §1.4 and
§1.8 claim**. The referee grades this "a material misquote by omission, in
the one receipt the section's whole ledger-conflict resolution rests on."
§1.4's "the single highest-value open item on the page" and §1.8's "make
(H-SIDE) the single named blocker" are withdrawn to that extent.

### D7 — (H-RATE) is NOT discharge-clean (referee `:433-453`)

§1.4 grades (H-RATE) Scope 1 "DISCHARGEABLE (formalization only) … *Blocker:*
none identified". This omits five of the seven consumed sub-inputs
(`EFFECTIVE_THEOREM_ASSEMBLY_SOL.md:192-201`), including a conjectural one:
the M1 localization triple / Route-B repair row, whose referee
(`M1_LOCALIZATION_TRIPLE_REFEREE.md:12`) states (referee `:442-445`):

> "The note correctly leaves `O(q^{1-2 sigma})` conjectural."
> "… The `q^{1-2 sigma}` RATE bound is still conjectural."

At the banked `sigma = 11/10`, `q^{1-2 sigma} = q^{-6/5}` — **the very
exponent (H-RATE) Scope 1 claims** (referee `:447-448`). The M1 row is
listed as *consumed* and no banked source reconciles this with §2.3's
"N1-RATE no longer needed". **Corrected gate-table entry:**

| gate | corrected read |
|---|---|
| **(H-RATE) Scope 1** | **dischargeable ONLY IF** the M1 conjectural `O(q^{1-2σ})` piece is not consumed — unresolved in the banked ledger (referee `:261`). NOT "blocker: none identified". |

Two further corrected entries the referee records: **(H-C4)** is **NOT**
dischargeable by a banking act — the same `CR_REDUCTION_V3_REFEREE.md`
paragraph §1.4 quotes also says "**No gate moves.** `q_monotone` stays. This
is not a final `q_0`", a direct denial of §1.4's read (referee `:420-425`);
**(H-REFL)** is **PRINTED-LITERATURE, not discharged** — grading it
"DISCHARGED modulo citation hygiene" is an upgrade past its source, whose
tier-mate (H-RATE)'s printed inputs are CONFIRMED-*conditional* (referee
`:427-431`).

**Corrected headline — the "7 of 8" figure is WITHDRAWN.** Referee
`:270-272`:

> "Clearly discharged or dischargeable-by-formalization: (H-HOL), (H-ROUTE),
> (H-GEOM), (H-TRANS) — **four**, with (H-RATE) Scope 1 conditional on D7.
> 'Seven of eight' is not supported."

**The corrected count is FOUR** ((H-HOL), (H-ROUTE), (H-GEOM), (H-TRANS)),
plus (H-RATE) Scope 1 conditional on D7; (H-C4) and (H-REFL) are not
discharged; (H-SIDE) remains genuinely open **and coupled to Scope 2 per
D6b**. §1.4's "Net" paragraph and §1.8's derived reading are superseded here.

### D8 — L5's `−25.5` is wrong by a factor `ln 10` (referee `:455-472`)

§1.3's L5 evidence cell reads "V1→V3 spent three referee cycles for 30.59
e-folds = −25.5". One e-fold of `C_R` moves `log Q_0` by `1/alpha = 0.8333`
**nats**, i.e. `0.36191 log10`, not `0.833 log10`. Correctly (referee
`:463-466`):

```
30.5945 e-folds -> 30.5945/1.2/ln 10 = 11.0725 log10   (note printed: 25.5)
 1.7179 e-folds ->  1.7179/1.2/ln 10 =  0.6217 log10   (note: 0.62 — correct)
```

**`−25.5` → `−11.07`.** Cross-check (referee `:469-471`): `log10 Q_0(V1) =
47.52` against `36.4487` now, an `11.07 log10` total. The L5 verdict
("declining") is unaffected, but **`−25.5` must not be quoted**. §1.3's
commentary figure `1.7179 e-folds = −0.62 log10` was already correct.

### D9 — §1.7.6's "complete" frozen list is incomplete (referee `:474-516`)

Additions required, in the referee's severity order:

- **(a) (H-HOL) belongs in the frozen list** (referee `:478-485`). The banked
  finite-Hecke holomorphy theorem (`HOLOMORPHY_GATE_SOL.md:373-379`) is
  proved on "an open neighborhood of the full `H_0`, of the A0 domain
  `overline{Omega}`, of `D_z`, and of the old Route-B right domains". A
  rectangle of height `H = 6` is **none of those**; the domains used in
  §1.5–§1.6 are not the domains (H-HOL) was proved for.
- **(b) The `H`-axis of the §2–§4 chain** (referee `:506-511`). §1.7.3 is
  scoped entirely to `p != 11/5`; changing `H` is an independent axis
  (`Gamma_R` goes from a height-`1` to a height-`6` segment). The referee
  reads it as **benign** — (3.15) is pointwise in `s`, only
  `sup_{Gamma_R}|s|` enters, and `S(sigma,H)` is recomputed — but a list
  calling itself complete must contain it.
- **(c) The `H_0` underwriting `K_+ = 117` is only `±0.9999` tall** (referee
  `:487-493`). `HOLOMORPHY_GATE_SOL.md:80`: `H_0 = [1/2, 1.4999] × [t_c −
  0.9999, t_c + 0.9999]`. Against the proposed `H = 6` (half-width `3`) the
  whole conditional apparatus that produced `117` is **out of domain** — on
  the `sigma` axis the proposal stays inside (`1.48 < 1.4999`); on the `H`
  axis it is **3× outside**. Not a matter of degree.
- **(d) §1.7.2's monotonicity claim is FALSE for the `H` lever** (referee
  `:495-504`). §1.7.2 states "Enlarging `Omega` enlarges that set, so the
  true `K_+` on the modified `Omega` is `>= 117`." For the `sigma` lever
  this is right (left edge unchanged, top/bottom extend ⇒ superset). For the
  `H` lever it is **wrong**: the top and bottom edges *move* (from
  `Im = t_0 ± 1/2` to `t_0 ± 3`), so
  `∂Omega_{H=6} \ Gamma_R` does **not** contain `∂Omega_{H=1} \ Gamma_R`.
  **Correct statement: `K_+` on the new domain is simply UNKNOWN**, not
  `≥ 117`. The error is conservative in direction but is stated as fact and
  is false.
- **(e) `q_side'''` under every lever** (referee `:513-516`) — never
  re-checked in the note. The referee checked it; `q_A0` still binds
  everywhere (`log10 q_side = 18.945 < 31.603` at `K_+=10`;
  `9.916 < 18.791` at the joint point). Unflagged, benign.

### The REFUTED inference — §1.6's "nothing pushing back" (D5, referee `:196-211`, `:370-374`)

§1.6 concludes: *"raising sigma raises alpha at NO cost in alpha*nu_z, so the
`(log C_R)/alpha` term shrinks with nothing pushing back."* **This is false
and is replaced by the referee's monotonicity fact.** At fixed
`alpha*nu_z = 2d`,

```
T_0 = log(K_+/m_z)/(2d) - log(K_+)/alpha,
```

which is **strictly increasing in `alpha`**. From `alpha = 1.2` to
`alpha = 1.96` the floor rises by exactly
`log(K_+)*(1/1.2 - 1/1.96)/log 10 = +0.66829 log10` — and §1.6's own table
shows it (`7.1493 → 7.8197` in the `H=6, r_z=1/40` rows, difference
`0.6704`, the remainder being the `nu_z` residual off the exact strip limit).
The net move is still favourable, so **no ranking changes**; but the sentence
as written is contradicted by the note's own numbers. The strip-invariance
statement itself (`alpha*nu_z → 2*(Re z_0 − r_z − 1/2)`) is CONFIRMED
(referee `:191-194`).

### The finding in the note's favour — L2 needs no (H-SIDE) relicensing (N1, referee `:520-527`, `:601-604`)

> "`r_z` does not touch `Omega`, so the `(H-SIDE)` sup set is literally
> unchanged and `K_+ = 117` is **fully licensed** for the `r_z`-only rows."

Consequences:

1. §1.7.2's blanket "Any use of §1.6's numbers must first discharge (H-SIDE)
   at the new geometry" **over-caveats L2** and does not apply to the
   `r_z`-only rows.
2. §1.3's effort column mislabels L2 as "E1 (+E2)" — **the E2 leg is
   unnecessary**; L2 is **E1 only**.
3. L2 sharpens conclusion (c) to **`0.725 ≤ Re s_q ≤ 0.775`**,
   `|Im s_q − gamma_1/2| ≤ 1/40`, in place of `5/8 ≤ Re s_q ≤ 7/8` (referee
   `:138` grades this EXACT).
4. **L2 is the new TOP-RANKED lever, strictly ahead of L1** (referee `:527`,
   `:601-604`): "the only lever that needs no (H-SIDE) work at all, it is
   worth `−6.97 log10` on its own, and it simultaneously sharpens conclusion
   (c)".

**Corrected ranking (supersedes §1.3's table ordering and §1.8's next-lane
order):**

| rank | # | lever | est. Δlog10 | effort | (H-SIDE) exposure |
|---|---|---|---|---|---|
| **1** | **L2** | **`r_z`: `1/8 → 1/40`** | **−6.97** | **E1 only** | **NONE — `K_+=117` fully licensed**; also sharpens conclusion (c) |
| 2 | L1 | `Omega` aspect ratio `H: 1 → 6` | −4.59 | E1 (+E2 for `K_+`) | yes, and `K_+` is UNKNOWN not `≥117` (D9d); (H-HOL) out of domain (D9a,c) |
| 3 | L3 | `alpha` via `sigma` | −0.58 alone at `H=1` (D4); **+10.52 WORSE** if pushed to `sigma=1.48` at `H=1` (D2); pays only after L1 | E2 | yes |
| 4 | L4 | `K_+` sharpening 117 → 10 | −4.84 (exact, not a linearization — referee `:141-143`) | E3 | is the gate |
| 5 | L5 | further `C_4`/`C_R` shaving | headroom **−11.07** total (D8), ~−0.62 per referee cycle | E2 per step | — |
| 6 | L6 | gate consolidation | 0.00 for `Q_0` | E2/E3 | — |
| 7 | L7 | `alpha ≥ 2` (`p ≥ 3`) | unbounded in principle | E3, blocked | — |

Joint figures unchanged and referee-EXACT: L1+L2 `−9.40` (`27.0186`); joint
`sigma=1.48, H=6, r_z=1/40` `−17.63` (`18.7911`).

**Corrected §1.8 next-lane order:** (i) **L2** — re-run the `m_z` Arb cover at
`r_z = 1/40` (no gate work required, and N4 at referee `:546-550` notes the
sampled `m_z` clears its floor by only `1.4e-6`, so the Arb re-run "is not
optional"); (ii) re-derive `K_+` on a tall/thin `Omega`, noting D9d that it is
UNKNOWN there rather than `≥ 117`; (iii) re-run the `nu_z` cover at the new
`(sigma, H)`; (iv) only then re-audit the §2–§4 chain at `p = 2 sigma`.

### Nits recorded, no repair required (referee `:518-556`)

**N2** — "termwise positive on the relevant range" (§1.5.1(1)) is false: at
`y ≈ H/2`, `sin(n pi/2)` alternates and the `n=3` term is negative, so the
truncation error is unsigned and flooring does not by itself certify a lower
bound on `nu_z`. Tail is `~1e-40`, forty orders below flooring granularity —
no number moves. **N3** — §1.5.1's "400 odd modes … 1440–2880 points" does not
match the executed runs (100/200/300/400 modes; `M=720` for part of §1.5.3,
`M=360` for `m_z` in `joint.py`); stability verified, nothing moves. **N4** —
see above. **N5** — §1.2's `16.6706 + 19.7780` printed addends sum to
`36.4486` (second addend truncates `19.7781030`); §1.5.2's `1.28e-4` is
`1.157e-4` (the `4.2e-5` conclusion is right); §1.6's `m_z/r_z → 0.5` is
`→ 0.51447`.

### What the referee CONFIRMED (unchanged, for the record)

Referee `:120-146` reproduces to the printed digit: L1 `−4.5913`, L2
`−6.9734`, L1+L2 `−9.4004`, joint `18.7911` (`−17.6279`), rung min
`35.8768` (`−0.5719`) at `sigma=1.16`, sensitivities `5.1334`/`1.29x` and
`1.713`/`2.0e10`, L4 `4.5361`/`−4.84`, `alpha*nu_z` `0.4499` vs `0.1863`
(`2.4x`), `H < gamma_2 − gamma_1 = 6.887314`, and §1.8's "seventeen orders".
The elasticity artifact (`alpha·d(log Q_0)/d(alpha) = −log Q_0`), the
`alpha = 2 sigma − 1` welding, and the programme-level conclusion (only a
finite-base theorem bridges to `q ≤ 21`) are all CONFIRMED independently and
are the note's most valuable output. No banked constant, gate status or
threshold is altered by the note or by this block:
`Q_0 >= 2810199067910634377586449487575862960` stands, as an inequality, with
`q_monotone`'s remainder unevaluated.

---

**Post-correction status: CONFIRMED-with-corrections per referee; gate-audit
headline WITHDRAWN and replaced by the corrected count; ranking updated with
L2 first.**
