# LAW — the SELF-BOUNDING trace-formula attack on (THRESH)

**Date:** 2026-08-16. **Lane G, derivation lane.**
**Parents:** `LAW_ROUTEB_CONDITIONAL_THEOREM.md` (the positivity input (B4★), the Poisson
bookkeeping §1.4–1.5, the pigeonhole §4, `Q₀`); `LAW_B5J_JENSEN.md` §5.3 (B5 restated as
(THRESH), slope `c₂ < 0.14903` at `δ₀ = 0.2`); `LAW_U1EFF_ENTRYWISE.md` (operator/entry routes
dead; counting instruments live).
**Probe:** `law_probes/sbt_optimize.{py,json}` — **optimization only**; every bound below is
derived symbolically and the probe merely searches the test-functional family and runs the
mass-balance audit.
**No existing file was modified. No git was run.**

**Status labels** as in the parents: `PROVED-cited` / `PROVED-here` / `MEASURED` / `GAP` /
`REFUTED-here`.

---

## 0. Verdict up front

> ### **VERDICT: `NEEDS(named input)` — and the named input is not the one the brief expected.**
>
> The attack fails **twice over, independently**, and both failures are quantified.
>
> **(V1) The premise is not available. `REFUTED-here` (pointwise) + `GAP` (integrated).**
> The attack needs an **upper** bound on `−(φ'/φ)(½+ir)` of size `2 log q + O(1)`. HJL Lemma 5.3
> is a **one-sided lower** bound; no upper bound comes with it. Pointwise, an upper bound of that
> size is **false**: a pole at depth `d` and height `γ` forces
> `−(φ'/φ)(½+iγ) ≥ 2/d`, which is unbounded as `d → 0`, and the lane's own measurement admits an
> uncounted sliver `Re ∈ (0.487, ½)` where such poles live (parent §3 M2, `GAP` B5b-sliver).
> The integrated substitute — `∫_{t₀−1}^{t₀+1}(−φ'/φ) dr = 4π[M(t₀+1) − M(t₀−1)]` bounded by a
> Weyl law — is **also unavailable `q`-uniformly**, and §4.2 shows *why* from Garbin–Jorgenson's
> own Theorem 5.7: the discrete count in a **fixed** height window itself grows like
> `c₀(T) log Q`. Nothing in this circle of ideas is `q`-uniformly bounded in a bounded window.
>
> **(V2) Even granting the premise for free, the arithmetic falls short by a factor ≈ 8.**
> Let `PREMISE-U` be the (unproved) statement `∫ψ·P_q ≤ (2 log q + A)∫ψ` for non-negative test
> measures `ψ`. Then for **every** `ψ` and **every** `δ₀`, the provable deep-count slope obeys
>
> ```
>      c₂^prov(ψ, δ₀)  =  2 ∫ψ / W(ψ, δ₀)   ≥   2 / W*   =   0.9443 ,
> ```
>
> because the pole at the box corner `(d, γ) = (½, t₀ ± 1)` — present in the box for **every**
> `δ₀ ∈ (0, ½)` — caps the achievable minimum weight at `W* ≤ 2.11804` per unit test mass
> (§3.4, `PROVED-here` modulo one elementary one-variable maximum; the fully crude symbolic
> fallback `W* ≤ 2.4` still gives `c₂^prov ≥ 0.8333`).
>
> | | value | source |
> |---|---|---|
> | point evaluation at `r = t₀`, `δ₀ = 0.2` | `c₂^prov = 5.200` | §3.1, exactly the brief's prediction |
> | best indicator window (`R = 1.35`) | `c₂^prov = 1.369` | §3.2 |
> | **best test measure at all** (max-min) | **`c₂^prov = 1.237`** | §3.3, probe |
> | **information floor, any `ψ`, any `δ₀`** | **`c₂^prov ≥ 0.944`** | §3.4, symbolic |
> | (THRESH) at the measured `δ₀ = 0.2` | `0.14903` | parent B5-J §5.3 |
> | (THRESH) supremum over `δ₀ ∈ (0, ½)` | `0.23715` (at `δ₀ → ½`, self-defeating — §3.5) | §3.5 |
>
> ### **SHORTFALL FACTOR = 8.30** at the measured `δ₀ = 0.2` (achieved best `1.2366 / 0.14903`);
> ### **≥ 6.34** for *any* test functional at `δ₀ = 0.2`; **≥ 3.98** even optimizing `δ₀` too.
>
> **(V3) The cusp-subtraction prize is a CATEGORY ERROR, and the parent already says so.**
> The brief's step 4 proposes subtracting the cusp-form/on-line consumption, using
> Garbin–Jorgenson Thm 5.7 (`N_{M_q,0}(T) = c₀(T) log Q + O((log Q)^{3/4})`). **Cusp eigenvalues
> do not appear in `φ` at all** — parent §1.3, the bookkeeping ruling this lane already made.
> They consume **none** of `P_q`. GJ 5.7 counts the *discrete spectrum*, on the other side of the
> trace-formula identity. Subtracting it from the `P_q` budget is not conservative, it is
> meaningless. The **only** objects that can consume `P_q` mass are poles of `φ`, i.e. shallow
> resonances — and a *lower* bound on the shallow population is an obligation of exactly the same
> difficulty as B5 itself, currently unstated anywhere in the lane. Separately, GJ 5.7's constants
> are **not explicit**: the paper's error optimization is credited to "*some calculations that had
> been pointed out by Dennis Hejhal*" (`PROVED-cited`, re-fetched §4.2), so even the right-category
> version would arrive without numbers.
>
> **(V4) One genuinely new finding, banked: the MASS-BALANCE TENSION. `MEASURED`.**
> (B4★) demands that `4 log q` of Poisson mass be consumed per width-2 window. Capping **every**
> pole at its total mass `2π` and summing the far shells generously, the lane's own measured pole
> density (`0.402 log q` per width-2, parent M2) can absorb at most `3.844 log q` — **less than the
> `4 log q` required**, and that is with every inequality thrown maximally in the population's
> favour. Realistically the measured population absorbs ≈ `2.6 log q`. Either the winding probe is
> materially blind (the sliver), or **`A_Γ` is not `O(1)` but grows like `α log q`** — which is not
> slack, it is load-bearing: `α = 0.7` would drop (THRESH) from `0.14903` to `0.08892`, and
> `α ≥ 1.7355` would kill Route B outright (§5). **Obligation N-B4b is a bigger risk than the
> parent records it as, and this is a cheap test that has never been run.**
>
> **What would close it:** a proved lower bound `Σ_{shallow poles} ∫ψ K_ρ ≥ σ log q ∫ψ` with
> **`σ ≥ 1.759`** (i.e. ≈ **88%** of the entire positivity budget provably eaten by shallow poles),
> *together with* an upper-bound premise `PREMISE-U` that does not exist. Named, quantified, and
> in this lane's judgement not reachable — see §6.

---

## 1. The positivity identity, with all terms and signs

**[`PROVED-cited` for (1.1); `PROVED-here` for (1.2)–(1.4); `GAP` at `A_Γ`.]**

### 1.1 The cited inequality

Garbin–Jorgenson, arXiv:1603.01494 §5 (proof of Thm 5.4), quoting Huntley–Jorgenson–Lundelius,
*J. Funct. Anal.* **149** (1997), Lemma 5.3, itself from Hejhal, LNM 1001 vol. 2 (1983) p. 160.
**Re-fetched independently for this document** (ar5iv full text, 2026-08-16), returning verbatim:

```
   −φ'/φ(1/2+ir) − Σ (1−s_{k,q}) / ((s_{k,q}−1/2)² + r²)  ≥  2 log q_{M_q}  >  0
```

attributed as "*Quoting Lemma 5.3 of [HJL 97]*" which "*comes from pp. 160 of [He 83]*". This is a
**second independent read of the same secondary channel** (ar5iv), so obligation **N-B4** —
verification against the journal PDF or the arXiv source — is **not** discharged, but the
transcription in the parent (`1 − s_k` in the numerator, not `2(s_k − ½)`) is **confirmed as what
ar5iv renders**. The parent's recorded discrepancy §1.5 therefore stands as a genuine mathematical
disagreement between the cited lemma and the lane's own Poisson derivation, not as a garbling.
**Both readings have non-negative numerators for `s_k ∈ (½, 1]` and both are subtracted, so the
consequence (B4★) holds either way** — the parent's ruling, reused here unchanged.

### 1.2 The three families of terms, and their signs

`−(φ'/φ)(½+ir)` decomposes as (parent (1.4)):

```
   − (φ'_q/φ_q)(½ + ir)  =  P_q(r)  −  E_q(r)  +  A_Γ(r)                              (1.2)

   P_q(r) := Σ_{ρ: φ_q(ρ)=∞, Re ρ < ½}  2 d_ρ / ( d_ρ² + (r − γ_ρ)² )        ≥ 0     [resonances]
   E_q(r) := Σ_{k}  2(s_k − ½) / ( (s_k − ½)² + r² )                          ≥ 0     [residual, s_k ∈ (½,1]]
   A_Γ(r) := archimedean / non-Blaschke part                                          [sign unknown]
```

with `d_ρ := ½ − Re ρ > 0` the **depth**. Signs: `P_q ≥ 0` term-by-term (each summand is a Poisson
kernel of width `d_ρ`, total mass `∫_R = 2π` **independent of `d_ρ`** — this fact is used twice
below and is the single most consequential structural feature of the problem);
`E_q ≥ 0` and **subtracted**; `A_Γ` of unknown sign, `GAP` N-B4b.

**Cusp-form eigenvalues appear in NONE of the three.** They live in the `N_{M,w}(T)` term on the
other side of the trace-formula identity. This is the parent's §1.3 ruling and it is what kills the
brief's step-4 proposal (§5 below).

### 1.3 The one-sided consequence

Combining §1.1 and (1.2) and discarding the non-negative `E_q`:

> ### **(B4★)  `P_q(r) ≥ 2 log q − A_Γ(r)` for every real `r`, every `q`.**   `PROVED-here`, given N-B4/N-B4b.

`q_{M_q} = q` for `G_q` (parent §1.2(d), `PROVED-here` from GJ Example 5.8: only the order-`q`
elliptic point degenerates).

### 1.4 What the attack needs, and why it is not (B4★)

The self-bounding idea is: *each pole consumes mass; the total mass is bounded; hence the pole
count is bounded.* Written out, the argument requires, for a non-negative test measure `ψ`:

```
   Σ_{ρ deep in box}  ∫ψ(r) K_ρ(r) dr   ≤   ∫ψ(r) P_q(r) dr   ≤   (2 log q + A) ∫ψ .   (PREMISE-U)
```

The **first** inequality is free (`P_q` is a sum of non-negative terms; dropping the non-deep ones
is legitimate). The **second is `PREMISE-U` and it is exactly the reverse of (B4★).** HJL Lemma 5.3
supplies `≥`, never `≤`. §4 establishes that `PREMISE-U` is false pointwise and unproved in every
integrated form known to this lane. **The rest of §3 grants it for free anyway**, because the
resulting bound falls short regardless, and a shortfall computed under a *free* premise is the
strongest possible form of the negative.

---

## 2. The optimization problem, stated exactly

Fix `t₀` and set `t₀ = 0` WLOG (everything below is translation-invariant in height; note this
means the analysis is **`t₀`-uniform by construction**, unlike the parent's measured inputs — the
one place this lane improves on M3).

**Target.** `N_deep(t₀; δ₀) := #{ρ : φ_q(ρ) = ∞, Re ρ ≤ ½ − δ₀, |Im ρ − t₀| ≤ 1}`.

**Box.** `B(δ₀) = {(d, γ) : δ₀ ≤ d ≤ ½, |γ| ≤ 1}`. The upper limit `d ≤ ½` is the parent §4.2
convention (`Re ρ ≥ 0`).

**Kernel.** `K_{(d,γ)}(r) = 2d / (d² + (r − γ)²)`, with `∫_R K = 2π` for every `d`.

**Test family.** All non-negative Borel measures `ψ` of finite mass (point masses, indicators,
smooth bumps, and every mixture — strictly larger than the family the brief names).

**Minimum weight.** `W(ψ, δ₀) := min_{(d,γ) ∈ B(δ₀)} ∫ K_{(d,γ)} dψ`.

**Provable slope.** Under `PREMISE-U`, every deep pole in the box carries weight `≥ W`, so

```
   N_deep · W  ≤  (2 log q + A) ‖ψ‖    ⟹    N_deep ≤ c₂^prov · log q + O(1),
   c₂^prov(ψ, δ₀) = 2 ‖ψ‖ / W(ψ, δ₀).                                                   (2.1)
```

`PROVED-here` from (2.1)'s two displayed steps, given `PREMISE-U`.

**Survival criterion.** From `LAW_B5J_JENSEN.md` §5.3, re-derived here from the parent's (4.4) so
its `δ₀`-dependence is explicit (the brief asks for this):

```
   (THRESH)   c₂  <  T(δ₀) := [ 2 − (π²/3) δ₀ b ] / [ 2/δ₀ + π²/6 ],     b = 0.402.     (2.2)
```

`T(0.2) = 1.7355 / 11.6449 = 0.14903` ✓ reproduces the parent exactly. `T` is **increasing** in
`δ₀` on `(0, ½)`, with `T(0.1) = 0.08629`, `T(0.3) = 0.19289`, `T(½⁻) = 0.23715`.

---

## 3. The optimization, solved

### 3.1 Point evaluation at `r = t₀` — the brief's first candidate

`ψ = δ_{t₀}`, `‖ψ‖ = 1`. `W = min_{B(δ₀)} 2d/(d² + γ²)`. Since `d ↦ 2d/(d²+1)` is increasing on
`d < 1`, the minimum sits at the **shallowest** admissible depth and the **farthest** height:

```
   W_point(δ₀) = 2δ₀ / (δ₀² + 1),        c₂^prov = 2/W = (δ₀² + 1)/δ₀ .                 (3.1)
```

At `δ₀ = 0.2`: `W = 0.38462`, **`c₂^prov = 5.200`** — the brief's predicted `≈ 5.2`, confirmed
symbolically. Against `T(0.2) = 0.14903`: **fails by a factor of 34.9.** `PROVED-here`.

Note (3.1) is minimized over `δ₀` at `δ₀ = ½`, giving `c₂^prov = 2.5` — still 10.5× over
`T(½⁻)`. **Point evaluation cannot work at any `δ₀`.**

### 3.2 Indicator windows — integrating over `r`

`ψ = 1_{[−R, R]}`, `‖ψ‖ = 2R`. Exactly:

```
   ∫ K_{(d,γ)} dψ  =  2 [ arctan((R−γ)/d) + arctan((R+γ)/d) ] .                        (3.2)
```

The minimum over `B(δ₀)` is at a **corner**: `γ = ±1` and `d = ½` (for `R ≥ 1`; `arctan(x/d)`
decreases in `d`, so the *deepest* pole is the lightest — the opposite of §3.1, because integration
rewards the wide tails that a deep pole has).

- `R = 1` (the brief's window): `W = 2 arctan 4 = 2.65164`, `‖ψ‖ = 2`,
  **`c₂^prov = 1.50850`** — independent of `δ₀`. A 3.4× improvement on point evaluation.
- Optimizing `R`: the ratio `W/‖ψ‖` peaks at `R ≈ 1.35`, `W = 3.94376`, **`c₂^prov = 1.36925`**.

Against `T(0.2)`: **fails by a factor of 9.19.** `PROVED-here` (symbolic (3.2)) + probe for the
`R`-sweep.

### 3.3 The best test measure that exists — max-min

Maximizing `W(ψ, δ₀)/‖ψ‖` over all non-negative `ψ` is a zero-sum game (payoff
`∫K_ρ dψ`, maximizer `ψ` normalized to unit mass, minimizer a distribution over `B(δ₀)`). Solved
by multiplicative weights against exact best response (`law_probes/sbt_optimize.py`,
`W_optimal`; the reported value is the **exact** value of the returned `ψ` on the pole grid, hence
a genuine lower bound on the optimum — which is the conservative direction for the maximizer and
therefore the *aggressive* direction for this negative result):

| `δ₀` | `W*` per unit mass | `c₂^prov = 2/W*` | `T(δ₀)` | shortfall |
|---|---|---|---|---|
| 0.10 | 1.5695 | 1.2743 | 0.08629 | **14.77×** |
| 0.15 | 1.6005 | 1.2496 | 0.12028 | **10.39×** |
| **0.20** | **1.6173** | **1.2366** | **0.14903** | **8.30×** |
| 0.25 | 1.6285 | 1.2281 | 0.17308 | **7.10×** |
| 0.30 | 1.6360 | 1.2225 | 0.19289 | **6.34×** |
| 0.35 | 1.6408 | 1.2189 | 0.20871 | **5.84×** |
| 0.40 | 1.6438 | 1.2167 | 0.22137 | **5.50×** |
| 0.45 | 1.6466 | 1.2146 | 0.23071 | **5.26×** |
| 0.49 | 1.6484 | 1.2133 | 0.23609 | **5.14×** |

`MEASURED` (optimization probe), but bracketed above and below by the symbolic bounds of §3.2 and
§3.4. **No `(ψ, δ₀)` pair comes within a factor of 5 of (THRESH).**

The optimal `ψ` is broadly spread (support fills the computational window; the value drifts from
`1.640` at `R_max = 3` to `1.606` at `R_max = 20`, i.e. it is stable and the optimum is a genuine
spread profile, not a delta and not a sharp indicator).

### 3.4 The information floor — no test functional can do better

**`PROVED-here`** (modulo one elementary one-variable maximum), and this is the part that makes the
negative final rather than provisional. By minimax, `W*` is bounded above by the value against
**any single adversary mixture**. Take the two corners
`μ = ½(δ_{(½, +1)} + δ_{(½, −1)})`, which lie in `B(δ₀)` for **every** `δ₀ ∈ (0, ½)`:

```
   W*  ≤  max_r  ½ [ K_{(½,+1)}(r) + K_{(½,−1)}(r) ]
       =  max_r  ½ [ 1/(¼ + (r−1)²) + 1/(¼ + (r+1)²) ]
       =  2.118034…      (attained at r ≈ ±0.9930)                                     (3.4)
```

so, **for every non-negative test measure and every `δ₀`**,

> ### **`c₂^prov = 2‖ψ‖/W ≥ 2 / 2.118034 = 0.944272`.**

(If one wants the maximum in (3.4) with no calculus at all: `f(r) ≤ ½[4 + 1/(¼+1)] · 1.14 < 2.4`
crudely, still giving `c₂^prov ≥ 0.8333` and every conclusion below unchanged.)

Against `T(0.2) = 0.14903`: **shortfall ≥ 6.34×**. Against `sup_{δ₀} T = 0.23715`:
**shortfall ≥ 3.98×**. The self-bounding attack is dead by a factor of four **at best**, and that
"best" already grants `PREMISE-U` for free.

**Why, structurally.** `∫_R K_ρ = 2π` for every depth. A test measure that wants a deep pole to
register heavily must spread over a height range comparable to `1/d ~ 2`; but the budget it is
charged is `2 log q` per unit of test mass, so spreading costs exactly what it buys. The mass-per-
pole is depth-blind — that is the same blindness `LAW_B5J_JENSEN.md` F2 found in disc-Jensen and
`LAW_U1EFF_ENTRYWISE.md` found in the operator routes, now reappearing in the trace-formula
functional. **The Poisson kernel's depth-independent total mass is the reason no budget argument
can resolve depth.** That is the general lesson and it should be recorded as such.

### 3.5 Why `δ₀ → ½` is not the escape the table seems to offer

The shortfall shrinks as `δ₀ ↑ ½` only because `T(δ₀)` rises. But at `δ₀` near `½` the "deep" band
is `Re ρ ∈ [0, ½)` — *every* off-line pole — so `N_deep` **is** the total count, whose measured
slope is `b = 0.402` (parent M2), already `1.70 ×` over `T(½⁻) = 0.23715`. Route B fails at large
`δ₀` on the *measured* side before the provable side ever matters. **`δ₀ = 0.2` remains the right
cut**, and there the shortfall is 8.30× (achieved) / 6.34× (floor).

---

## 4. Is `PREMISE-U` obtainable? No.

### 4.1 Pointwise: false. `REFUTED-here`

`P_q` is a sum of non-negative Poisson kernels, so for any pole `ρ`,
`P_q(γ_ρ) ≥ K_ρ(γ_ρ) = 2/d_ρ`. Hence

```
   sup_r  −(φ'_q/φ_q)(½+ir)  ≥  2 / min_ρ d_ρ  −  sup|A_Γ| ,
```

which exceeds `2 log q + O(1)` as soon as `G_q` has a single pole with `d_ρ < 1/log q`. The lane's
measurement explicitly does not exclude this: the band `Re ∈ (0.487, ½)` is uncounted
(`GAP` B5b-sliver, parent §3 M2), and `d < 0.013` is exactly the regime that would break it at
`q ≈ 1465`. **A pointwise upper bound of the size the attack needs cannot hold in general.**

### 4.2 Integrated: unproved, and GJ Thm 5.7 says why. `GAP`

The natural integrated substitute is the scattering counting function,
`M(T) = (1/4π)∫_{−T}^{T}(−φ'/φ)(½+ir) dr`, whence
`∫_{t₀−1}^{t₀+1}(−φ'/φ) dr = 4π[M(t₀+1) − M(t₀−1)]`, and since the discrete count `N` is
increasing, `M(b) − M(a) ≤ (N+M)(b) − (N+M)(a)` — the "cusp subtraction" in its *correct* form.
Selberg's Weyl law `N(T) + M(T) ~ (|F_q|/4π)T²` has a `q`-uniform leading constant
(`|F_q| = π(1 − 2/q) ≤ π`, `PROVED`). So the shape is right.

**It fails on the error term, and not marginally.** Garbin–Jorgenson Thm 5.7 (re-fetched verbatim
2026-08-16, `PROVED-cited`):

```
   N_{M_q,0}(T)  =  c₀(T) log Q  +  O( (log Q)^{3/4} ) ,
```

i.e. **the discrete count in a FIXED height window itself grows like `log q`** as the elliptic
point degenerates. A Weyl asymptotic in `T` whose remainder is not uniform in `q` cannot bound a
bounded-height window at all; and the true window content is `Ω(log q)`, so there is no
`q`-uniform bound to be had. Any instrument bounding *deep count ≤ total window count* therefore
inherits slope `≥ c₀(T) > 0` and, per parent M2, `≈ 0.402 > 0.14903`. **This is `LAW_B5J_JENSEN`
F2 again, now derived from the literature rather than from the repo's measurements** — an
independent confirmation that depth-blind instruments are dead, and it upgrades F2 from
`MEASURED` to `PROVED-cited` in kind.

Consistency check for the reader worried these two facts collide: (B4★) integrated over a width-2
window gives `M(t₀+1) − M(t₀−1) ≥ (log q)/π`, so the *winding* count also grows like `log q`. Both
`N` and `M` grow in a fixed window while `N + M ~ (|F_q|/4π)T²` stays `q`-bounded **asymptotically
in `T` for each fixed `q`** — no contradiction, but a precise statement of why the asymptotic is
useless here.

---

## 5. The cusp-subtraction "prize": a category error, and what the right version costs

The brief's step 4 is that the `2 log q` budget is mostly eaten by cusp forms / on-line mass, so
the remainder available to deep poles is `O(1)`.

**`REFUTED-here` as stated.** Cusp-form eigenvalues are **not** poles of `φ_q` and contribute
**nothing** to `P_q` (parent §1.3; §1.2 above). `P_q` is a sum over poles of `φ` only. GJ Thm 5.7
counts `N_{M_q,0}`, the discrete spectrum — the *other* side of the trace-formula identity.
Subtracting it from the `P_q` budget subtracts an object that was never in the sum. The
window-1 observation that "shallow + cuspidal carries the `log q`" conflates two different
counting functions.

**The right version, and its price.** The only mass-consumers inside `P_q` are the **shallow
poles of `φ_q`**. A subtraction argument therefore needs a **proved lower bound**

```
   Σ_{ρ shallow}  ∫ K_ρ dψ   ≥   σ · log q · ‖ψ‖ ,
```

after which `c₂^prov = (2 − σ)/W`. Requiring `c₂^prov < T(0.2) = 0.14903`:

| `W` used | required `σ` | as a fraction of the whole budget |
|---|---|---|
| `W = 1.6173` (achieved optimum, §3.3) | **`σ ≥ 1.7590`** | **87.9 %** |
| `W = 2.11804` (the absolute ceiling, §3.4) | **`σ ≥ 1.6844`** | **84.2 %** |

So the named input is: *prove that at least ≈ 85 % of the entire HJL positivity budget is consumed
by shallow resonances of `φ_q`* — a **lower** bound on a population for which this lane has only an
(incomplete, non-certified) **upper** bound, and which is not stated as an obligation anywhere in
Route B. `GAP`, and in this lane's judgement harder than B5 itself.

### 5.1 The mass-balance audit — a new, cheap, and uncomfortable check. `MEASURED`

Turn the requirement around and ask whether the lane's own measurements can even *supply* the mass
that (B4★) says must be there. Integrating (B4★) over a width-2 window: total consumption
`≥ 4 log q − O(1)`. Now cap consumption generously:

- a pole *inside* the window consumes at most its **entire** Poisson mass, `2π = 6.2832`;
- a pole in shell `n ≥ 1` consumes at most `2·(2·½/n²)`, summing to `3.2798` over all shells;
- measured density (parent M2, conservative total-count reading): `0.402 log q` poles per width-2
  interval, per shell.

```
   maximum absorbable  =  0.402 · (6.2832 + 3.2798) · log q  =  3.844 log q   <   4 log q.
```

**The measured pole population cannot absorb the budget even under maximally generous weighting**,
and realistic weighting (shallow poles at `d ≲ δ₀` in-window absorb `2 arctan(2/d) ≈ 2.94`, not
`2π`) gives ≈ `2.6 log q`, a 35 % deficit. Two readings, both consequential:

1. **The winding probe is materially incomplete** — most likely in the uncounted sliver
   `Re ∈ (0.487, ½)`, whose poles absorb near the full `2π` each. This would *strengthen* the case
   for §5's subtraction but also means B5b's measured `(a, b)` are not upper bounds, as the parent
   already flags.
2. **`A_Γ` is not `O(1)`.** If `A_Γ = α log q` then (B4★) reads `P_q ≥ (2 − α) log q` and the
   deficit closes at `α ≈ 0.078` (generous weighting) or `α ≈ 0.7` (realistic weighting). There is
   a structural reason to expect this: the non-Blaschke part of `φ` contains the Dirichlet-series
   leading factor `c₀^{1−2s}`, contributing a term **constant in `r`** equal to `−2 log c₀`, and
   `c₀` is precisely what degenerates as the elliptic point opens. The parent's §1.4 argument
   ("the remaining factor's growth is carried by its zeros") does not cover an `e^{a+bs}`
   Hadamard factor.

**Consequence for (THRESH) if reading 2 holds** — `T(δ₀)` with `A_Γ = α log q` becomes
`[2 − (π²/3)δ₀b − α]/[2/δ₀ + π²/6]`:

| `α` | 0 | 0.2 | 0.5 | 0.7 | 1.0 | 1.7355 |
|---|---|---|---|---|---|---|
| `T(0.2)` | **0.14903** | 0.13186 | 0.10610 | 0.08892 | 0.06316 | **0 — Route B dies** |

> **Recommendation, and it is cheap.** Obligation **N-B4b** should be re-ranked from "expected
> harmless slack worth `+0.25` in the numerator" to **the second-largest risk in Route B after B5
> itself**. A single probe — evaluate `−(φ'/φ)(½+ir)` directly for `q = 5 … 21` and compare
> against `2 log q` and against the reconstructed `P_q` from the measured pole list — decides it.
> That probe does not exist in `law_probes/` and is the highest value-per-hour item this lane can
> point at.

---

## 6. Verdict, and the honest next lane

> **VERDICT: `NEEDS(named input)` — two of them, both harder than the obligation they would
> discharge.**
>
> 1. **`PREMISE-U`**: an upper bound `∫ψ P_q ≤ (2 log q + O(1))‖ψ‖`. False pointwise (§4.1);
>    unavailable integrated, with GJ Thm 5.7 explaining why (§4.2). `GAP` / `REFUTED-here`.
> 2. **`σ ≥ 1.759`**: a proved lower bound showing ≈ 88 % of the budget is consumed by shallow
>    resonances (§5). `GAP`, unstated in Route B, and of B5's own difficulty.
>
> **Best achievable slope, granting (1) for free:** `c₂^prov = 1.2366` at `δ₀ = 0.2`
> (`0.9443` is the floor for *any* test functional at *any* `δ₀`).
> **(THRESH) requirement:** `0.14903` at `δ₀ = 0.2`, `≤ 0.23715` anywhere.
> **SHORTFALL FACTOR: 8.30** (achieved), **≥ 6.34** (floor at `δ₀ = 0.2`), **≥ 3.98** (floor over
> all `δ₀`).
>
> No `(test, δ₀)` pair closes. `Q₀` is **not** recomputed, because nothing unconditional was
> obtained; the parent's `Q₀ = 1465` remains conditional on B5/(THRESH) exactly as before, and
> §5.1 raises a new question about one of its inputs.

**What this lane banks, positively:**

- **(A) A general obstruction, not a failed attempt.** `∫_R K_ρ = 2π` independent of depth ⇒ any
  budget/mass argument is depth-blind up to the corner constant `2.118`, giving the hard floor
  `c₂^prov ≥ 0.944` for the *entire* class of test-functional arguments. This closes off a family
  of attacks, rather than one attack. It is the trace-formula analogue of `LAW_B5J_JENSEN` F2 and
  of `LAW_U1EFF_ENTRYWISE`'s ruling. `PROVED-here`.
- **(B) `t₀`-uniformity for free.** Everything in §§2–3 is translation-invariant in height, so the
  floor holds for every `t₀` — the only `t₀`-uniform statement in the lane (parent M3 `GAP`).
- **(C) F2 upgraded via the literature.** GJ Thm 5.7's `c₀(T) log Q` growth of the discrete count
  in a *fixed* window is a `PROVED-cited` reason that depth-blind window counts cannot be
  `q`-uniform. §4.2.
- **(D) GJ 5.7's constants are not explicit** — the error optimization is credited in the paper to
  unpublished calculations of Hejhal (re-fetched, §0 V3). Any future use of 5.7 must not assume
  numbers are available.
- **(E) The mass-balance tension (§5.1)** and the consequent re-ranking of **N-B4b**.

**Ranked next steps** (superseding nothing in the parent, adding to it):

1. **The `A_Γ` probe (§5.1).** Direct evaluation of `−(φ'/φ)(½+ir)` against `2 log q` for
   `q = 5 … 21`. Cheap, decisive, currently absent. **Highest value in the lane.**
2. **Do not attempt further test-functional / budget arguments** for the deep count. §3.4 is a
   floor over the whole class; the shortfall is ≥ 4× under a premise that is itself false.
3. Certified winding counts remain the only depth-resolving instrument (parent RB-A1 ruling,
   unchanged and reinforced).

---

## 7. Per-step status ledger

| # | Step | Statement | Status |
|---|---|---|---|
| S1 | HJL Lemma 5.3, re-fetched | `−φ'/φ − Σ(1−s_k)/(…) ≥ 2 log q_M` | `PROVED-cited`; **N-B4 still open** (same secondary channel, ar5iv, twice) |
| S2 | sign decomposition (1.2) | `−φ'/φ = P_q − E_q + A_Γ`, `P_q ≥ 0`, `E_q ≥ 0` | `PROVED-here` (parent §1.4) |
| S3 | cusp eigenvalues absent from `φ` | | `PROVED-cited` (parent §1.3 ruling, reused) |
| S4 | (B4★) `P_q(r) ≥ 2 log q − A_Γ` | pointwise | `PROVED-here` given S1, N-B4b |
| S5 | `PREMISE-U` needed for the attack | `∫ψP_q ≤ (2log q + A)‖ψ‖` | **`GAP`** — not implied by S1 |
| S6 | `PREMISE-U` false pointwise | `P_q(γ_ρ) ≥ 2/d_ρ`, unbounded | **`REFUTED-here`** |
| S7 | integrated `PREMISE-U` via Weyl | blocked: window discrete count `~ c₀(T) log Q` | **`GAP`**, with `PROVED-cited` obstruction (GJ Thm 5.7) |
| S8 | slope formula `c₂^prov = 2‖ψ‖/W` | under `PREMISE-U` | `PROVED-here` |
| S9 | `(THRESH)` `δ₀`-dependence `T(δ₀)` | `[2−(π²/3)δ₀b]/[2/δ₀+π²/6]`; `T(0.2)=0.14903` | `PROVED-here` (reproduces B5-J §5.3) |
| S10 | point evaluation | `c₂^prov = (δ₀²+1)/δ₀ = 5.200` at `δ₀=0.2` | `PROVED-here` — **fails 34.9×** |
| S11 | indicator windows | `R=1`: `1.50850`; best `R=1.35`: `1.36925` | `PROVED-here` (3.2) + probe sweep — **fails 9.19×** |
| S12 | best test measure (max-min) | `c₂^prov = 1.2366` at `δ₀ = 0.2` | `MEASURED` (probe), bracketed by S11/S13 — **fails 8.30×** |
| S13 | **floor over all `(ψ, δ₀)`** | `W* ≤ 2.118034` ⇒ `c₂^prov ≥ 0.944272` | **`PROVED-here`** (minimax + one 1-var maximum) — **fails ≥ 3.98×** |
| S14 | `δ₀ → ½` is self-defeating | deep band = total, measured slope `0.402 > T(½⁻)` | `PROVED-here` + `MEASURED` |
| S15 | cusp subtraction as briefed | cusp eigenvalues consume none of `P_q` | **`REFUTED-here`** (category error) |
| S16 | correct subtraction's price | `σ ≥ 1.759` (≈ 88 % of budget), lower bound on shallow mass | **`GAP`** — named input, unstated in Route B |
| S17 | GJ Thm 5.7 constants | credited to unpublished Hejhal calculations | `PROVED-cited` (re-fetched) |
| S18 | mass-balance tension | measured population absorbs ≤ `3.844 log q` < `4 log q` required | **`MEASURED`** — new; implies probe-incompleteness or `A_Γ = α log q` |
| S19 | `A_Γ = α log q` sensitivity | `α=0.7 ⇒ T(0.2)=0.0889`; `α ≥ 1.7355 ⇒` Route B dies | `PROVED-here` given S18 |
| S20 | `t₀`-uniformity of §§2–3 | translation-invariant by construction | `PROVED-here` |

---

## 8. What this document claims, and does not

**Claims.** (i) The self-bounding attack does not close (THRESH), by a factor of `8.30` at the
measured `δ₀ = 0.2`, and by `≥ 3.98` for **every** non-negative test functional at **every**
`δ₀ ∈ (0, ½)` — a floor over the whole class, not a report on attempts. (ii) The attack's premise
(an upper bound on `−φ'/φ`) is not supplied by HJL Lemma 5.3, is false pointwise, and is
unavailable in integrated form for a reason visible in Garbin–Jorgenson Thm 5.7. (iii) The
cusp-subtraction proposal is a category error under this lane's own bookkeeping ruling; the correct
version requires a lower bound on shallow-resonance mass of `σ ≥ 1.759`, ≈ 88 % of the budget.
(iv) The lane's measured pole population cannot absorb the mass (B4★) demands, which either
impugns the winding probe's completeness or makes `A_Γ` grow like `log q`; either way N-B4b is
under-ranked. (v) The structural reason all of this fails is that the Poisson kernel's total mass
is depth-independent.

**Does not claim.** That (THRESH) is false — only that this instrument cannot establish it. That
`A_Γ` grows like `log q` — §5.1 is a `MEASURED` tension between two non-certified inputs, not a
proof, and the alternative explanation (probe incompleteness in the uncounted sliver) is at least
as likely. That N-B4 is discharged — it was re-fetched through the *same* secondary channel
(ar5iv), which raises confidence in the transcription and not at all in the mathematics. That the
max-min value in §3.3 is the exact optimum; it is a certified lower bound on the optimum from an
explicit `ψ`, which is the direction that makes the negative conservative, and §3.4 caps it
symbolically from above. That anything here bears on `Q₀`, which is unchanged and still
conditional. No novelty is claimed for the Poisson representation, for minimax, or for HJL Lemma
5.3; the contribution is the floor `c₂^prov ≥ 0.944`, the category ruling on cusp subtraction, and
the mass-balance audit.

---

**Sources.** arXiv:1603.01494 (Garbin–Jorgenson, L'Enseign. Math. **64** (2018) 161–206) — Thm 5.4,
Thm 5.7, and the §5 inequality, re-fetched via ar5iv 2026-08-16; Huntley–Jorgenson–Lundelius,
*J. Funct. Anal.* **149** (1997) 58–82, Lemma 5.3 (quoted through GJ, not read directly); Hejhal,
LNM 1001 vol. 2 (1983) p. 160 (**not consulted** — blocked HITL library item, parent constraint
honoured); repo: `LAW_ROUTEB_CONDITIONAL_THEOREM.md`, `LAW_B5J_JENSEN.md`,
`LAW_U1EFF_ENTRYWISE.md`, `LAW_ROUTEB_{DEEPCOUNT,SUBSTRATUM,Q18Q21}.md`;
probe `law_probes/sbt_optimize.{py,json}`.

No git was run. No existing file was modified.
