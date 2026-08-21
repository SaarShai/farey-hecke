# Cold referee: R3 strip transport execution — (H-TRANS) discharge attempt

**Date:** 2026-08-20
**Lane:** G / R3
**Target:** `research_notes/rh_goals_2026-08-14/lane_g/R3_TRANSPORT_EXECUTION_SOL.md`
sha256 `a6b6a1297fc4401e47e194a809064baa5cade1f9effb29fe28e3bde47d3b6345`
**Scope refereed:** the CONDITIONAL transport theorem `(R3-Z)` and its proof at
`:60-93` and `:190-231`, at the note's own stated hypotheses (holomorphy gate,
`E_R` bound, `K_+` side bound).  The note's unconditional-`R3` self-graded gap
(`C_R`, `alpha`, `q_RATE`, `q_divisor`, family-uniform `K_+`) is NOT under
review and is NOT discharged here.
**Referee independence:** this pass did not write the target; all receipts below
were produced by this referee with fresh code, at different discretisations and
different phase offsets from the note's, plus two non-Fourier cross-checks of
the harmonic measure.  No existing file was modified.

**Environment:** `/Users/za/.venvs/farey-rh/bin/python`, python-flint / Arb,
`ctx.dps = 60` (the note used 80; lower precision is the adverse choice here).

---

## 0. Verdict table

| # | Attack | Verdict |
|---|---|---|
| 1 | Two-constants application: subharmonicity, boundary decomposition, monotonicity, `nu_0` orientation and geometry | **CONFIRMED** |
| 2 | Rouché: `m_z` receipt, strictness, existence of a `phi_infty` zero in `D_z`, absence of `phi_infty` poles in `D_z` | **CONFIRMED** |
| 3 | Reflection `s_q -> 1 - conj(s_q)` via Hejhal (7.22) | **DEFECT D1 — GAPS NOT REFUTED** (repairable citation/hypothesis defect; not a refutation) |
| 4 | Hidden hypotheses: `0 < E_R <= K_+`, holomorphy on `\overline{Omega}`, the `E_R = 0` branch | **CONFIRMED** (with defect D2, over-assumption; D3, unstated real-reflection input) |
| 5 | Numerics: `t_0`, `m_z`, `nu_0`, tail bound, `K_+`, `(6.1)`, `(6.3)`, `(6.4)` | **CONFIRMED — every constant reproduced independently** (with defect D4, razor-thin certification margins) |

**FINAL HOUSE VERDICT: GAPS NOT REFUTED.**
The transport core — `(R3-Z)`, its two-constants derivation, the harmonic-measure
constant, the Rouché step producing a zero of `phi_q` in `D_z`, and every printed
numeral — is **CONFIRMED** at the stated conditional scope.  The full §7 statement
as printed is **not** cleanly confirmable because its final clause (the pole at
`1 - conj(s_q)`) rests on a mis-scoped citation (D1) plus one unstated analytic
input (D3).  Nothing in the note is refuted.  D1 and D3 are one-paragraph repairs;
the mathematics behind them is unconditionally true.

---

## 1. Attack 1 — the two-constants / harmonic-measure application

### 1.1 The classical statement, re-derived

`Omega` is a bounded Jordan domain (an open rectangle) with
`\partial Omega = Gamma_R \cup (\partial Omega \setminus Gamma_R)`.
Assume `F` holomorphic on `\overline{Omega}`, `|F| <= E_R` on `Gamma_R`,
`|F| <= K_+` on the rest, `0 < E_R <= K_+`.  Put

```
u(s) = log|F(s)| - [ nu(s) log E_R + (1 - nu(s)) log K_+ ],
```

`nu = omega(., Gamma_R; Omega)` harmonic on `Omega`.  Then `u` is subharmonic
on `Omega` (sum of a subharmonic and a harmonic function), bounded above
(`|F|` is bounded on the compact closure), and `limsup u <= 0` at every
boundary point except the four corners, which form a polar set.  The extended
maximum principle for subharmonic functions bounded above off a polar boundary
set gives `u <= 0` on `Omega`, i.e.

```
|F(s)| <= E_R^{nu(s)} K_+^{1 - nu(s)}                       (*)
```

This is exactly the note's `(3.3)`.  **The note's invocation is legitimate.**
The rectangle's boundary is everywhere regular for the Dirichlet problem, so no
regularity hypothesis is missing.

### 1.2 Monotonicity step

The note writes: "Because `E_R/K_+ <= 1`, the right side decreases as `nu(s)`
increases.  Using `nu(s) >= nu_0` on `\partial D_z` proves `(R3-Z)`."
Re-derived: `E_R^{nu}K_+^{1-nu} = K_+ (E_R/K_+)^{nu}`, and `t -> c^t` is
non-increasing for `0 < c <= 1`.  Hence `nu >= nu_0` gives
`K_+(E_R/K_+)^{nu} <= K_+(E_R/K_+)^{nu_0} = K_+^{1-nu_0}E_R^{nu_0}`.
**Correct, and the direction of the inequality in the `(R3-Z)` box is right.**
Note that the argument *requires* `E_R <= K_+`; the note states it (hypothesis 4
of §7 and the inline condition at `:77`).  Not a gap.

### 1.3 Geometry: is `D_z` inside `Omega`, and is the translation right?

`Omega = {1/2 < Re s < 11/10, |Im s - t_0| < 1/2}`.
Translation `x = Re s - 1/2`, `y = Im s - (t_0 - 1/2)` maps `Omega` to
`0 < x < L`, `0 < y < 1` with `L = 11/10 - 1/2 = 3/5`.  Verified in Arb:
`Omega width L = [0.6000...]`.
`D_z = D(3/4 + i t_0, 1/8)` maps to the disc centred `(1/4, 1/2)` of radius
`1/8`, i.e. `x \in [1/8, 3/8]`, `y \in [3/8, 5/8]` — **strictly interior**
(`1/8 > 0`, `3/8 < 3/5`, `3/8 > 0`, `5/8 < 1`).  The note's parametrisation at
`:159-160` (`x = 1/4 + (1/8)cos t`, `y = 1/2 + (1/8)sin t`) is consistent.
Also `Re s \in [5/8, 7/8]` on `\overline{D_z}` as claimed, and
`Re s >= 5/8 > 1/2` strictly.  **CONFIRMED.**

### 1.4 Is `(3.1)` the harmonic measure of the RIGHT side? (orientation attack)

The series

```
nu(x,y) = sum_{n odd >= 1} (4/(n pi)) sinh(n pi x)/sinh(n pi L) sin(n pi y)
```

is harmonic, vanishes identically on `y = 0`, `y = 1` and on `x = 0`
(`sinh 0 = 0`), and on `x = L` reduces to the Fourier square wave
`sum_{n odd} (4/(n pi)) sin(n pi y) = 1` on `0 < y < 1`.  So it IS the harmonic
measure of the right side, not of the left, top or bottom.  Independent Arb
receipt of the three boundary values:

```
series at x=L,   y=1/2  (should be 1) : [1.0015836214753934725...]   (Gibbs, truncated at n=401)
series at x=0,   y=1/2  (should be 0) : 0
series at x=L/2, y=1/2                : [0.4077742647083144485...]
series at x=1/8, y=1/2                : [0.15521450551118485791...]
```

**Two independent non-Fourier cross-checks of the same number** (these use no
series at all, so they catch an orientation or index error):

- Walk-on-spheres Monte Carlo, 200 000 paths, seed 7, exit-side tally in the
  rectangle `[0,0.6] x [0,1]` started at `(0.125, 0.5)`:
  `WoS nu(0.125,0.5) ~ 0.1553`.
- Jacobi finite-difference Laplace solve, `h = L/480`, Dirichlet `1` on `x = L`
  and `0` elsewhere: converging from below toward the same value
  (`nu(0.3,0.5) ~ 0.1638` after 60 000 sweeps; unconverged, direction consistent).

Monte Carlo `0.1553` versus series `0.155214` — agreement to Monte-Carlo error.
**Orientation and geometry CONFIRMED; no side-swap.**

### 1.5 Where is the infimum on `\partial D_z`, and is `nu_0 = 0.1552` a genuine lower bound?

`nu` is strictly increasing in `x`, so the leftmost circle point `(1/8, 1/2)`
is the natural minimiser.  My independent covers (phase offset `arb(2 pi k / N)`
rather than the note's `arb(2 pi (k + 1/2)/N)`, `n_max = 151` rather than `101`,
and my own re-derived geometric tail) confirm both the location and the value:

```
my tail bound (n0 = 153, a = pi*9/40) = [1.8065419518059150784e-49]
N= 2000  nu lower = [0.155214370190481746768...]  ge 0.1552: True  min at theta/2pi = 0.5005
N= 6000  nu lower = [0.155214461736720999418...]  ge 0.1552: True  min at theta/2pi = 0.49983
```

`theta/2pi = 1/2` is `theta = pi`, the leftmost point, as predicted.
The note's own receipt (`N = 4096`, box index 2048) reports the same minimiser
and `0.15521443750831436...`.  **`nu_z >= 0.1552` CONFIRMED independently.**

### 1.6 The tail bound is valid

Re-derived: for `n >= 1`,
`sinh(n pi x)/sinh(n pi L) <= e^{n pi x}/(e^{n pi L}(1 - e^{-2 n pi L}))
<= e^{-n pi (L-x)}/(1 - e^{-2 pi L})`, and `|sin| <= 1`, `4/(n pi) <= 4/(n_0 pi)`,
`sum_{n >= n_0} e^{-na} = e^{-n_0 a}/(1 - e^{-a})` with `a = pi (L - x_max)`,
`x_max = 3/8`, so `a = 9 pi / 40`.  This is exactly the note's code.  The bound
majorises the tail in ABSOLUTE value (necessary — for `y \in [3/8, 5/8]` and `n`
odd, `sin(n pi y)` does take negative values, so the partial sum is NOT by itself
a lower bound), and the note correctly SUBTRACTS it from `u.lower()`.
**CONFIRMED — this is the step most likely to hide a sign error, and it does not.**

**Attack 1 verdict: CONFIRMED.**

---

## 2. Attack 2 — Rouché

### 2.1 `phi_infty` really has a zero in `D_z`

`z_0 = (1 + rho_1)/2 = 3/4 + i gamma_1/2`, so `2 z_0 - 1 = 1/2 + i gamma_1 = rho_1`
**exactly, as algebra, not as a numerical coincidence**.  Arb receipt:

```
2*z0-1 - rho1 = [+/- 2.49e-60]j
zeta(2*z0-1)  = [+/- 2.11e-59] + [+/- 2.32e-59]j
```

Hence `zeta(2 z_0 - 1) = 0` and `phi_infty(z_0) = 0`, provided no other factor
blows up there — checked in 2.2.  This does **not** assume RH: `rho_1` is a
known zero and `acb.zeta_zero(1)` returns it with a rigorous enclosure whose real
part is the exact `1/2` interval.  The note's remark that no simplicity
assumption on `rho_1` is needed is correct: Rouché transfers the count with
multiplicity, and the count is `>= 1` either way.  **CONFIRMED.**

### 2.2 `phi_infty` is holomorphic and pole-free on `\overline{D_z}`

On `\overline{D_z}`, `Re s \in [5/8, 7/8]`:
`Gamma(s - 1/2)` — poles only at `s - 1/2 \in {0,-1,-2,...}`, i.e. `s` real; `Im s ~ 7.07`, excluded.
`Gamma(s)` — same, and it sits in the denominator, so its poles would give zeros, not poles; irrelevant either way.
`zeta(2s - 1)` — entire except the simple pole at `2s - 1 = 1`, i.e. `s = 1`; `|1 - z_0| >= 7.06`, excluded.
`zeta(2s)` in the denominator — `Re(2s) \in [5/4, 7/4] > 1`, Euler product non-vanishing, so no pole of `phi_infty` from this factor.
`4^s - 1` in the denominator — vanishes only when `4^s = 1`, i.e. `Re s = 0`; excluded.
So `phi_infty` is holomorphic on `\overline{D_z}` with no poles.  **The note's §2.1
argument is complete and correct.**  Rouché's hypothesis (both functions
holomorphic in the disc) therefore reduces to the `phi_q` holomorphy gate,
which the note carries explicitly.  **CONFIRMED.**

### 2.3 Strictness

`(1.2)` reads `K_+^{1-nu_0} E_R^{nu_0} < 0.0439`, with `(R3-Z)` giving
`sup_{\partial D_z}|F_q| <= K_+^{1-nu_0}E_R^{nu_0}`.  Chaining:
`|F_q| < 0.0439 <= m_z <= |phi_infty|` pointwise on `\partial D_z`.  The first
inequality is strict, so `|phi_q - phi_infty| < |phi_infty|` on `\partial D_z`
strictly, which is precisely Rouché's hypothesis.  Zero counts of `phi_q` and
`phi_infty` in `D_z` agree with multiplicity; `(2.1)` makes that count `>= 1`;
so `phi_q` has a zero `s_q \in D_z`.  **The comparison function is `phi_infty`,
it does have a zero, and the inequality direction is right — the classic
"vacuous Rouché" failure mode is NOT present.  CONFIRMED.**

### 2.4 The `m_z` receipt, independently reproduced

My own covers (different phase offset, `dps = 60`):

```
N =  3000  min|phi_inf| lower = 0.04308167385170236...   ge 0.0439: FALSE
N =  5000  min|phi_inf| lower = 0.04364935919875279...   ge 0.0439: FALSE
N = 12000  min|phi_inf| lower = 0.04411989316577091...   ge 0.0439: TRUE
N = 40000  min|phi_inf| lower = 0.04434299969580024...   ge 0.0439: TRUE
pointwise infimum (200 000-point non-rigorous scan) = 0.04444137474289863 at theta/2pi = 0.99516
```

The true infimum is `~0.0444414`; the note's asserted `m_z >= 0.0439` is
therefore TRUE with about `1.2%` of genuine slack.  The note's own `N = 8192`
cover reports `0.043908844760...`, i.e. it clears its own threshold by `0.02%`.
Interval arithmetic is sound, so the note's certificate is valid as printed;
but see defect **D4**.

**Attack 2 verdict: CONFIRMED.**

---

## 3. Attack 3 — the reflection step (**DEFECT D1**)

`R3_TRANSPORT_EXECUTION_SOL.md:220-232` cites Hejhal (7.22) as an "exact
reflection identity" and applies it at the point `s_q` where `phi_q(s_q) = 0`.

The verbatim printed (7.22), as read off p. 577 of the banked scan and recorded
in `EFFECTIVE_THEOREM_ASSEMBLY_REREFEREE.md:36-46`, is:

> THEN select a subsequence 𝒥 such that:
>   φ_N(s) ≠ 0 on [½, ½+δ] × [t_o−δ, t_o+δ]  whenever N ∈ 𝒥 .
> Recall that |φ_N(½+it)| ≡ 1 for t ∈ ℝ. By the Schwarz reflection principle,
> φ_N(s) extends holomorphically to [½−δ, ½+δ] × [t_o−δ, t_o+δ]. In fact:
> **(7.22) φ_N(½ − h + it) · conj( φ_N(½ + h + it) ) ≡ 1, 0 ≤ h ≤ δ, |t − t_o| ≤ δ.**
> In this equation N ∈ 𝒥 .

`LAW_HEJHAL_S7_EXTRACT.md:67-70` records the same scoping ("1. [E] Assume
φ_N ≠ 0 on R_δ ... 2. ... with the functional identity (7.22)").

**The defect.**  As printed, (7.22) is derived *under* the standing contradiction
hypothesis `phi_N != 0` on `[1/2, 1/2 + delta] x [t_0 +/- delta]`, along a
selected subsequence `𝒥`.  R3 §4 invokes it at exactly a point `s_q` with
`phi_q(s_q) = 0` — the direct negation of that hypothesis — and for an arbitrary
single `q`, not along `𝒥`.  **As cited, the pole conclusion does not follow.**

This is the same defect the assembly re-referee raised against
`EFFECTIVE_THEOREM_ASSEMBLY_SOL.md` (its finding 1b-D, defect 4, and the
corrected pointer at `EFFECTIVE_THEOREM_ASSEMBLY_SOL.md:751-760`).  The
correction was applied to the assembly and **was never applied to R3, its
source.**  R3 §4 needs the identical repair.

**It is a citation defect, not a refutation.**  The needed identity is
unconditionally true: `phi_q` continues meromorphically to `\mathbb{C}` with
`phi_q(s) phi_q(1-s) \equiv 1` (Selberg's theory of the Eisenstein series for a
one-cusp group), which is what Hejhal's Corollary 7.12 (p. 579, "Proof.
Trivial.") uses.  A zero of order `k` at `s_q` therefore forces a pole of order
`k` at `1 - s_q`.

**Repair text for `R3_TRANSPORT_EXECUTION_SOL.md` §4 (replace `:220-232`):**

> `phi_q` continues to a meromorphic function on `\mathbb{C}` satisfying the
> unconditional functional equation `phi_q(s) phi_q(1-s) \equiv 1` (Selberg;
> Hejhal LNM 1001 Vol. 2, Cor. 7.12, p. 579).  Since `phi_q(s_q) = 0` with
> `Re s_q \in [5/8, 7/8]`, the identity forces a pole of `phi_q` of the same
> order at `1 - s_q`, whose real part lies in `[1/8, 3/8]`, strictly left of the
> critical line.  Since `phi_q` has real Dirichlet coefficients in `(7.5)`, it
> also satisfies `phi_q(\bar s) = \overline{phi_q(s)}`, so `1 - \overline{s_q}`
> is a pole of the same order as well.  Hejhal's printed (7.22) (p. 577) is NOT
> invoked: as printed it holds only along the subsequence `𝒥` on which `phi_N`
> is assumed zero-free on `[1/2, 1/2+delta] x [t_0 +/- delta]`, a hypothesis
> negated at `s_q`.  With `delta = 1/2` the reflection window of §1 contains
> `\overline{D_z}` and its mirror image (`h <= 3/8 < delta`,
> `|t - t_0| <= 1/8 < delta`).

**Attack 3 verdict: GAPS NOT REFUTED (defect D1, repairable).**

---

## 4. Attack 4 — hidden hypotheses

### 4.1 The `E_R = 0` branch — no gap

§1 `:77` states `0 < E_R(q) <= K_+`; §3 `:175` and §7 hypothesis 4 state only
`E_R(q) <= K_+`.  Re-derived: if `E_R(q) = 0` then `F_q` vanishes on the full
segment `Gamma_R`, so by the identity theorem `F_q \equiv 0` on `Omega`, and
`(R3-Z)` holds trivially with both sides zero.  The `0^{nu_0}` expression is
also `0`, so no `0^0` pathology arises (`nu_0 = 0.1552 > 0`).  **The looser §3/§7
form is sound and the §1/§3 inconsistency is cosmetic.  No defect.**

### 4.2 Holomorphy of both functions on `\overline{Omega}` — stated, and over-stated (**DEFECT D2**)

Two-constants requires `F_q = phi_q - phi_infty` holomorphic on
`\overline{Omega}`, hence BOTH summands.  §7 hypothesis 1 does list both.
**Complete.**

However, `phi_infty`'s holomorphy on `\overline{Omega}` is *unconditionally
provable* and should not be sitting inside a `CONJECTURAL` gate.  On
`\overline{Omega}` we have `Re s \in [1/2, 11/10]`, `Im s \in [t_0 - 1/2, t_0 + 1/2]
\subset [6.56, 7.57]`, so: `Gamma(s-1/2)` and `Gamma(s)` have no poles (poles need
`s` real); `zeta(2s-1)`'s only pole is at `s = 1`, excluded by the imaginary part;
`4^s - 1 \ne 0` since `Re s > 0`; and `zeta(2s) \ne 0` because `Re(2s) \in [1, 2.2]`
and `zeta` is non-vanishing on `Re = 1` (classical, Hadamard--de la Vallee Poussin)
and in `Re > 1` (Euler product).  The note proves this only on `\overline{D_z}`
(§2.1) and never on `\overline{Omega}`.  This is an over-assumption, i.e.
conservative — it cannot make the theorem false — but it is a free strengthening
the note leaves on the table, and it hides the fact that the ONLY genuinely open
holomorphy gate is the finite-`q` one (`q_divisor`).

**Repair:** insert after `:124` a paragraph proving `phi_infty` holomorphic on
`\overline{Omega}` by the display above, and split §7 hypothesis 1 into
"1a. `phi_infty` holomorphic on `\overline{Omega}` — **PROVED** (§2.1')" and
"1b. `phi_q` holomorphic on `\overline{Omega}` for `q >= q_divisor` —
**CONJECTURAL**".

### 4.3 Unstated input: the real reflection `phi_q(\bar s) = \overline{phi_q(s)}` (**DEFECT D3**)

The note concludes a pole at `1 - \overline{s_q}`.  The functional equation
`phi_q(s)phi_q(1-s) = 1` alone yields a pole at `1 - s_q`.  Getting
`1 - \overline{s_q}` additionally needs `phi_q(\bar s) = \overline{phi_q(s)}`
(true from the real coefficients `|c|^{-2s}` in Hejhal (7.5), and used implicitly
inside (7.22)'s complex conjugate).  **The note never states this input.**  Either
state it (as in the D1 repair text above) or weaken the conclusion to
`1 - s_q`; both give an off-line pole, so the theorem's substance is unaffected.

### 4.4 `K_+` scope

§1 `:75-76` defines `K_+` as a bound on the other THREE sides; §5.1's `(5.1)`
supplies a bound on all of `\overline{Omega}` via Prop. 12.4.  I checked Prop.
12.4's stated range of validity against `Omega`: `1/2 <= Re s <= 3/2` covers
`[1/2, 11/10]`, and `|Im s| >= 1` covers `[6.56, 7.57]`.  **Applicable.**
The triangle inequality `|F_q| <= |phi_q| + |phi_infty| <= 2(1+\sqrt2)B^2` is
correct.  The common-`y_0 = 1000` premise is properly flagged **CONJECTURAL**
at `:270-273`, and the note does not promote `(5.1)` into `(R3-Z)`.  **Honest.**

**Attack 4 verdict: CONFIRMED, with defects D2 (over-assumption) and D3 (unstated input).**

---

## 5. Attack 5 — every numeral, independently reproduced

All values below were computed by this referee at `dps = 60` (the note used 80).
Command: `/Users/za/.venvs/farey-rh/bin/python` with the scripts described in §1
and §2; the constants block:

```
t0 = [7.06736257086734689522862599178123513539212855784962158784278 +/- 4.20e-60]
t0 - 7.0665 = [0.00086257086734689522862599178123513539212855784962158784278 +/- 4.20e-60]
t0 > 7.067362570867346895 : True
|phi_inf(1/2+it0)| = [0.338537177013144849034575191482102987463102704763157424935 +/- 3.44e-58]
  <= 0.338537177013144850 : True
  point defect >= 0.661462822986855150 : True
K_12.4(B=1005) = [2438416.05333588532666592565366990030180733283592760197761028 +/- 4.96e-54]
2*K_12.4       = [4876832.10667177065333185130733980060361466567185520395522055 +/- 2.03e-54]  < 4876833 : True
E_R threshold  = [7.038157697395552327318349923512151331648818802382598392723e-46]  > 7.03e-46 : True
p_Z (alpha=6/5) = [0.186240000000000000000...]
C_Z (C_R=2)     = [497575.21552000233614083075104041754843725689130640016871186] < 497576 : True
q bound ceil    = 75578028497170725293702300965513602908
Omega width L   = [0.600000000000000000000...]
```

| Note's claim | Location | Independently reproduced | Verdict |
|---|---|---|---|
| `t_0 = 7.067362570867346895...` | `:295` | yes, `7.0673625708673468952286...` | PASS |
| `t_0 - 7.0665 > 0.000862570867346895` | `:301` | yes, `0.000862570867346895228...` | PASS |
| `m_z >= 0.0439` | `:62`, `:244` | yes; true inf `~0.0444414`, my `N=40000` cover gives `0.044343` | PASS |
| `nu_z >= 0.1552` | `:65`, `:245` | yes; my `N=6000`/`n_max=151` cover gives `0.1552144617` | PASS |
| harmonic tail is rigorously majorised | `:450-453` | re-derived; my independent `n_0=153` tail `1.8e-49` | PASS |
| `|phi_infty(1/2+it_0)| < 0.338537177013144850` | `:318` | yes | PASS |
| `1 - |phi_infty(1/2+it_0)| > 0.661462822986855150` | `:322` | yes | PASS |
| `K_+ < 4876833` | `(5.1)` `:266` | yes, `4876832.1067` | PASS |
| `E_R < 7.03e-46` suffices | `(6.3)` `:353` | yes; exact threshold `7.0381...e-46`, rounded DOWN | PASS |
| `p_Z >= 0.18624`, `C_Z < 497576` | `:363-364` | yes | PASS |
| `q >= 75578028497170725293702300965513602908` | `(6.4)` `:370` | yes; and the algebra `C_Z q^{-p_Z} < m_0 <=> C_R q^{-alpha} < E_crit` re-derived | PASS |
| `phi_infty` regular/nonzero factors on `\overline{D_z}` | `:120-124` | re-derived analytically, §2.2 above | PASS |
| `(6.4)` is labelled CONJECTURAL DIAGNOSTIC, not `q_0` | `:375-381` | present and unambiguous | PASS |
| `D` values in §8.2 marked NOT EVIDENCE (failed N-doubling) | `:595-596` | `convergence_reldiff ~ 0.0254`; the disclaimer is correct | PASS |

**Every printed numeral in the note reproduces.  All roundings I checked go in the
adverse (conservative) direction, as the note claims at `:14-16`.**

**Attack 5 verdict: CONFIRMED, with defect D4.**

---

## 6. Defect list

| id | defect | where | severity | why the author likely missed it |
|---|---|---|---|---|
| **D1** | Hejhal (7.22) is cited as an "exact reflection identity" but as printed it holds only along the subsequence `𝒥` on which `phi_N` is assumed ZERO-FREE on `[1/2,1/2+delta] x [t_0 +/- delta]` — and R3 applies it precisely at a zero `s_q`. | `:220-232`, and the `(1.2)` sentence at `:92-93` | **HIGH (blocks a clean CONFIRMED of §7 as printed; repairable, not fatal)** | The author read (7.22) from the extract's summary line, which prints the display without re-printing the enclosing "In this equation N ∈ 𝒥". The identical defect was later caught and repaired in the DOWNSTREAM assembly, and the repair was never pushed back to this SOURCE note. | 
| **D2** | `phi_infty`'s holomorphy on `\overline{Omega}` is bundled into the CONJECTURAL §7 hypothesis 1 although it is unconditionally provable (`zeta` non-vanishing on `Re = 1` handles the left edge `Re s = 1/2`). | `:390-391`, §2.1 proves it only on `\overline{D_z}` | LOW (conservative; costs precision, not soundness) | §2.1 was written for the Rouché disc, and the two-constants domain `Omega` was never given its own holomorphy paragraph. The left edge `Re(2s) = 1` is the one place needing a non-Euler-product argument. |
| **D3** | The conclusion `1 - \overline{s_q}` needs `phi_q(\bar s) = \overline{phi_q(s)}` in addition to `phi_q(s)phi_q(1-s) = 1`; this input is never stated. | `:228-232`, §7 final clause | MEDIUM | The conjugate is hidden inside (7.22)'s own notation, so using (7.22) as a black box makes the extra input invisible. Exposed only once D1 forces the route through `phi(s)phi(1-s) = 1`. |
| **D4** | The `m_z` certificate clears its own threshold by `0.02%` (`0.0439088` vs `0.0439`) and the `nu_z` certificate by `0.009%` (`0.15521444` vs `0.1552`). Both are VALID, but a reader re-running at a coarser grid gets a FALSE certificate (my `N = 3000` and `N = 5000` covers both report `ge 0.0439: FALSE`). | `:519-524`, `:244-245` | LOW (hygiene / reproducibility, not soundness) | Box counts were tuned until the assertion passed, rather than until it passed with stated slack. Nothing flags to the reader that the receipt is grid-critical. **Repair:** state the true infima (`m_z^* ~ 0.04444`, `nu_z^* ~ 0.1552145`) alongside the certified bounds, and record the minimum box count at which the certificate holds. |
| **D5** | Malformed LaTeX `,qquad` (missing backslash) in two displays. | `:71`, `:144` | COSMETIC | Typo; both displays still parse to the reader. |
| **D6** | §4 transcribes (7.22) as `conj(phi_q(1/2 + h + i \bar t))`; the printed p. 577 text has `it`, not `i\bar t`. Harmless for real `t`, but it is not the source's convention. | `:225` | COSMETIC | Carried over from `LAW_HEJHAL_S7_EXTRACT.md`'s own paraphrase rather than the page image. |

**No out-of-scope content found in the note; no deleted or contradicted prior
result; §5's ledger does not suppress any `CONJECTURAL / MISSING` row (I checked
all ten rows against the body text).  The note's self-grade at `:7-12` is honest:
it does not claim an effective `q_0`, and `(6.4)` is explicitly fenced.**

---

## 7. What this pass does and does not discharge for (H-TRANS)

**Discharged.**  The `(H-TRANS)` gate as written in
`EFFECTIVE_THEOREM_ASSEMBLY_REFEREE.md:75` asks for "a cold referee on the
harmonic-measure/two-constants application (boundedness of `F_q` on `\overline{Omega}`,
the `omega(s, Gamma_R; Omega)` interval cover, and the Rouché strictness on
`\partial D_z`)".  All three are **CONFIRMED** above: §1 (two-constants,
including the subharmonicity and monotonicity re-derivations and the
orientation cross-check), §1.5-1.6 (the interval cover, reproduced independently
plus a Monte-Carlo check), §2.3 (strictness).  `(R3-Z)` and the Rouché-zero
conclusion stand.

**Not discharged.**  (a) The reflection clause of §7 — defect D1, pending the
repair text in §3.  (b) Everything the note itself grades `CONJECTURAL /
MISSING`: `C_R`, `alpha`, `q_RATE`, `q_divisor`, and a family-uniform `K_+`.
This pass makes no progress on those and was not asked to.

---

## 8. Final house verdict

> **GAPS NOT REFUTED.**
>
> `(R3-Z)` — the two-constants/harmonic-measure transport of the boundary rate
> `E_R(q)` on `Gamma_R` into `sup_{\partial D_z}|phi_q - phi_infty| <=
> K_+^{1-nu_0} E_R(q)^{nu_0}` — is **CONFIRMED** at its stated hypotheses,
> with the geometry, the orientation of the harmonic measure, the tail bound,
> the Rouché strictness, and every printed constant independently reproduced by
> this referee at a different discretisation and, for the harmonic measure, by a
> method that uses no series at all.  The Rouché conclusion "`phi_q` has a zero
> in `D_z`" is **CONFIRMED**.
>
> The full §7 statement as printed is **not** cleanly confirmable: its final
> clause routes through Hejhal's printed (7.22), which is valid only under a
> zero-free hypothesis that the clause itself negates (**D1**), and silently
> consumes the real-reflection identity (**D3**).  Both are repairable by the
> text supplied in §3; the underlying mathematics
> (`phi_q(s)phi_q(1-s) \equiv 1`, Hejhal Cor. 7.12, p. 579) is unconditional.
> **Nothing in the note is refuted.**
>
> Recommended status line for the note after repair:
> "CONDITIONAL TRANSPORT THEOREM PROVED AND REFEREED (`R3_TRANSPORT_EXECUTION_REFEREE.md`,
> 2026-08-20); CURRENT UNCONDITIONAL R3 REMAINS A GAP."

READY FOR JUDGING
