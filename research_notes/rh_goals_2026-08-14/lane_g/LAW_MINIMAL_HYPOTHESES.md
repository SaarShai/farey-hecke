# LAW — minimal-hypothesis audit of the tail argument

**Date:** 2026-08-16. **Lane G. AUDIT ONLY — no new numerics, no certificate, no commit,
`lane_f/` untouched, no probe run.**

**Question audited.** Since the (T2′) reformulation the lane has served the assumption
*"the tail argument needs U1, a `q`-uniform growth bound on `Ω̃`."* This note re-derives the
Vitali/Hurwitz continuation end-to-end, records the **exact** hypothesis consumed at each step
(not the strongest available one), and reports the minimal hypothesis set, **U1-min**.

**Parents read in full:** `LAW_TAIL_SCOPING.md`, `LAW_T2_DETERMINANT.md` (incl. the 2026-08-16
`Ω̃` amendment, §3.2), `LAW_U3_TRANSPORT.md`, `LAW_U2B_CLOSURE.md` (post-repair),
`LAW_U1_GROWTH.md` (incl. §10 addendum and §11 correction notice), `LAW_U1PHI_PROOF_ROUTE.md`.

**Status convention (identical to T1/T2/U1/U2b/U3).** `PROVED` = derived here in closed form, or
already `PROVED` in a named note+section. `PROVABLE` = follows from proved pieces by a sketched
argument that nobody has written out; the sketch is given. `CITATION` = classical import, named.
`OPEN` = genuinely not available, with the missing statement written out. `HEURISTIC` = float
evidence.

---

## 0. Verdict up front

> ### **U1 as stated is NOT minimal. Three of its four dimensions collapse; one does not.**
>
> | dimension of U1 | minimal requirement | verdict |
> |---|---|---|
> | growth **shape** (`A e^{B(1+|s|)²}`) | plain boundedness | **collapses** — already `PROVED` (U1.1) |
> | **`t`-extent** | one bounded band `|Im s − t_∞| < δ`, `δ` arbitrarily small | **collapses** |
> | **left edge of `Ω̃`** (`Re s = −1/10`) | `Re s > 1/4 − r`, `r` arbitrarily small ⇒ **anything `> 1/8` suffices, and `> 3/16` if one is content with `r = 1/16`** | **collapses** |
> | **connectivity to `{Re s > 1}`** | a corridor from `D̄(s_∞,r)` to an open piece of `{Re s > 1}`, on which the family is locally uniformly bounded | **DOES NOT collapse — this is irreducible** |
>
> ### **U1-min (§4).** There exist `r ∈ (0, 1/4)`, `Q₁`, `A < ∞` and an open **connected**
> ### `Ω̃` with `D̄(s_∞, r) ⊂ Ω̃ ⊂ {Re s > 1/4 − r} ∩ {|Im s − t_∞| < 1/2}` and
> ### `Ω̃ ∩ {Re s > 1} ≠ ∅`, such that `{Z_{G_q}}_{q ≥ Q₁}` is locally uniformly bounded on `Ω̃`.
>
> Every other hypothesis of the tail argument is `PROVED` or `PROVABLE` (§2 table). **U1-min is
> the whole remaining obligation.**

**Five findings, in descending order of consequence.**

1. **The corridor is irreducible, and this is a theorem about the method, not a limitation of
   effort.** Boundedness on a *small disc around `s_∞` alone* — the brief's first candidate
   weakening — is **provably insufficient**: Montel then yields a locally uniformly convergent
   subsequence on that disc, but **nothing identifies its limit**, because the only set on which
   `Z_{G_q} → Z_{Γ_θ}` is known lies in `Re s > 1`, disjoint from the disc. Vitali's
   accumulation set and the boundedness domain must be **the same connected domain**. §3.1,
   `PROVED`.
2. **`(U1-φ-a′)` and `U1-min` are two readings of one unknown**, and the unknown is sharp:
   **the size of `φ_q(s)` in the strip `3/4 < Re s < 1`.** `LAW_U1PHI_PROOF_ROUTE.md` §4.3's
   heuristic that `|Z_{G_q}(σ+it)|` grows like `q^{1−2σ}` — which at `Re s = 1/4` predicts
   `q^{+1/2}`, i.e. predicts **U1-min FALSE** — is *exactly* the assumption that `φ_q` does not
   decay at the reflected abscissa `Re s = 3/4`. The adverse heuristic and the open obligation are
   the same statement with opposite sign. §5.3, `PROVED` (as an equivalence of the two
   *statements*; the statement itself is `OPEN`).
3. **`(U1-φ-a′)`'s required decay exponent is milder than the parent note lets on, and it is a
   free parameter.** The Hurwitz radius `r` is unconstrained in `(0, 1/4)` — the parent's
   `r < 1/8` is over-tight, since the final margin is `1/4 − r > 0` for every `r < 1/4`. Sending
   `r → 0` sends the admissible `σ → 3/4⁺` and the required exponent `2σ − 1 → 1/2⁺`. So the
   sharpest true version of (ii) is: **`|φ_q(σ+it)| = O(q^{−ε})` for some single `σ ∈ (3/4,1)`
   and some `ε > 2σ − 1`, with `σ` choosable as close to `3/4` as desired** — i.e. **any decay
   exponent `> 1/2` at any single abscissa in `(3/4,1)` suffices.** §5.2, `PROVED`.
4. **A hypothesis is missing from `(U1-φ-a′)` as written: the horizontal edges.** The maximum
   principle on the rectangle `[1−σ, σ] × [t_∞ ± δ]` needs **four** sides. `(i)` and `(ii)` supply
   the two vertical ones. The two horizontal segments are supplied by nothing. The repair is
   Phragmén–Lindelöf in the strip, which is available (per-`q` finite order is `CITATION`) — but
   **it forces `(i)` and `(ii)` to hold for all real `t`, not for `|t| ≤ t_∞ + 1`.** So
   `t`-uniformity, which the *theorem* does not need, re-enters through the *implementation*.
   §5.4, `PROVED` (the gap) + `PROVABLE` (the repair).
5. **`LAW_U1_GROWTH.md` §6's "either one closes U1" over-claims for `(U1-φ-b)`.** A `q`-uniform
   resonance count on `|s − 1/2| ≤ 8` controls only the *local* Hadamard factors. Converting a
   zero count into a sup bound additionally needs `q`-uniform control of the Hadamard exponential
   `e^{P_q(s)}` and of the *global* zero distribution — and `LAW_U1_GROWTH.md` §5.2 (U1.16) has
   already shown the global counting is **not** uniform at fixed height (elliptic mass
   `≍ (log q)/π`, comparable to the `T²` term at `T ≈ 8`). **(U1-φ-b) is an ingredient, not a
   closure.** §6.2, `PROVED`.

---

## 1. The continuation, written as a numbered chain

Notation fixed once: `ρ₁ = 1/2 + iγ₁`, `γ₁ = 14.134725141734693790…`;
`s_∞ = ρ₁/2 = 1/4 + i t_∞`, `t_∞ = γ₁/2 = 7.067362570867346895…`.

Each step lists **the exact hypothesis it consumes** — deliberately the weakest form that makes
that step go through, ignoring what happens to be available.

---

**STEP 1 — choose the domain.**
*Consumes:* nothing. *Produces:* an open connected `Ω̃ ⊂ C`.
Free choice. Constraints appear only in Steps 3, 4, 6, 7 and are collected in §4.
`PROVED` (a choice).

**STEP 2 — the anchor has a zero at `s_∞`.**
*Consumes:* `Z_{Γ_θ}` has a zero of order `m ≥ 1` at `s_∞`.
*Status:* **`PROVED`** — `LAW_U3_TRANSPORT.md` §3.4 (U3-θ), order `2·m(ρ₁) ≥ 2`, `= 2` given
`ρ₁` simple. Two logically independent routes (§2.2 citation; §2.6 derivation from Teo's
functional equation), every cancellation channel excluded (§3.5).
*Minimality note:* the chain needs only **`m ≥ 1`**. The order `2` is used nowhere except to say
Hurwitz delivers *two* zeros rather than one. `V5` of the U3 note already records this.

**STEP 3 — the anchor is holomorphic and `≢ 0` on `Ω̃`.**
*Consumes:* `Ω̃` avoids the poles of `Z_{Γ_θ}`, and `Z_{Γ_θ} ≢ 0` on `Ω̃`.
*Status:* **`PROVED`** — the complete pole set of `Z_Γ` for cofinite `Γ` is items 3 and 4 of the
7-item divisor (`LAW_U3_TRANSPORT.md` §2.3), i.e. `s = 1/2` and `s = −n − 1/2`, **all real**; so
`Z_{Γ_θ}` is holomorphic off `R`. Any `Ω̃` with `Im s > 1` qualifies. `Z_{Γ_θ} ≢ 0` because it is
a convergent non-vanishing Euler product on `Re s > 1`, which every admissible `Ω̃` meets
(Step 5). **This is an implicit hypothesis the parent notes never state**; it is free, but it is
a hypothesis, and it is one of the reasons `Ω̃` may not be pushed down to the real axis.

**STEP 4 — pointwise convergence on a set with an accumulation point in `Ω̃`.**
*Consumes:* a set `E ⊂ Ω̃` with an accumulation point in `Ω̃` on which `Z_{G_q}(s) → Z_{Γ_θ}(s)`.
*Status:* **`PROVED`** — `LAW_T2_DETERMINANT.md` §3.4 (U2a, word-level: `tr_w(λ) ∈ Z[λ]`, one
polynomial, `2 − λ_q = π²/q² + O(q⁻⁴)`) + `LAW_U2B_CLOSURE.md` §4 (U2b, the `q`-uniform Euler
tail: `S_q(σ) ≤ 0.4861` for `σ ≥ 3.5`, `PROVED` with explicit constants, systole
`sys(G_q) = 2 arccosh λ_q` `PROVED` in §1.2).
*Minimality note:* **the cheapest `E` is a single sequence `{s_n} ⊂ Ω̃ ∩ {Re s > 3.5}` with
`s_n → s_* ∈ Ω̃`.** Vitali–Porter needs no more. The parent's "pointwise on `{Re s > 1}`" is
enormously more than the step consumes — but it is free, so this weakening buys nothing. Recorded
for completeness. Note the abscissa: U2b's proof is `q`-uniform only for `σ ≥ 3.05` (method
floor), so take `E ⊂ {Re s ≥ 3.5}`.

**STEP 5 — `Ω̃` meets the convergence region.**
*Consumes:* `Ω̃ ∩ {Re s > 3.5} ≠ ∅` (open, so it contains a set with an accumulation point).
*Status:* `PROVED` (a constraint on the Step-1 choice).
*This is the step that forbids a small disc around `s_∞`.* See §3.1.

**STEP 6 — local uniform boundedness. ⟵ THE ONLY OPEN HYPOTHESIS**
*Consumes:* `sup_{q ≥ Q₁} sup_{K'} |Z_{G_q}| < ∞` for every compact `K' ⊂ Ω̃`.
*Status:* **`OPEN`.** This is U1-min (§4). Nothing weaker is known to suffice (§3).

**STEP 7 — Vitali–Porter.**
*Consumes:* Steps 4, 5, 6 + `Ω̃` connected.
*Produces:* `Z_{G_q} → F` locally uniformly on `Ω̃`, `F` holomorphic.
*Status:* `CITATION`, classical (Vitali–Porter / Montel + identity theorem).
*Minimality note:* Vitali as usually stated gives convergence of the whole sequence given
pointwise convergence on a set with an accumulation point; the version that only gives a
*subsequence* (Montel) is not enough, and the upgrade is exactly what Step 4 pays for.

**STEP 8 — identify the limit.**
*Consumes:* Steps 3, 4, 7 + connectedness.
*Produces:* `F ≡ Z_{Γ_θ}` on `Ω̃`.
*Status:* `PROVED` — identity theorem: `F` and `Z_{Γ_θ}` are holomorphic on the connected `Ω̃`
(Step 3) and agree on `E`, which has an accumulation point in `Ω̃` (Step 4).
*Minimality note:* **connectedness of `Ω̃` is consumed here, and it is not decorative.** On a
disconnected `Ω̃` the limit would be identified on the `Re s > 1` component only.

**STEP 9 — choose the Hurwitz radius.**
*Consumes:* `∃ r > 0` with `D̄(s_∞, r) ⊂ Ω̃` and `Z_{Γ_θ} ≠ 0` on `∂D(s_∞, r)`.
*Status:* `PROVED` — zeros of `Z_{Γ_θ}` are isolated (Step 3: holomorphic, `≢ 0`), so all but
countably many `r` work, and arbitrarily small `r` works. This is U6 of
`LAW_T2_DETERMINANT.md` §5.2, and it is cheap exactly as recorded there.

**STEP 10 — Hurwitz.**
*Consumes:* Steps 2, 7, 8, 9.
*Produces:* `∃ Q₀(r)` such that for all `q ≥ Q₀`, `Z_{G_q}` has exactly `m = 2` zeros in
`D(s_∞, r)`, with multiplicity — in particular **at least one zero**.
*Status:* `CITATION`, classical. Uniform convergence on the compact `∂D` is what is used.

**STEP 11 — the zero is off the critical line.**
*Consumes:* `r < 1/4`.
*Produces:* any such zero `s_q` has `Re s_q ≤ 1/4 + r < 1/2`, margin `1/4 − r > 0`.
*Status:* `PROVED` (arithmetic).
*Correction owed:* `LAW_T2_DETERMINANT.md` §3.2 and `LAW_U1_GROWTH.md` §9 both restrict to
`r ∈ (0, 1/8)` and quote the margin as `η = 1/8 − r`. The true constraint is `r < 1/4` and the
true margin is `1/4 − r`. Non-load-bearing for the theorem, **but load-bearing for §5.2**,
because `r` is what sets the admissible `σ`-window and hence the required `φ_q` decay exponent.

**STEP 12 — assemble with the finite base.**
*Consumes:* certified instances for `5 ≤ q ≤ Q₀` (which needs U4 per instance) + Takeuchi
arithmeticity exclusion of `q ∈ {3,4,6}`.
*Status:* out of scope of this audit; unchanged from `LAW_T2_DETERMINANT.md` §5.1. Note `Q₀` is
**ineffective** as the chain stands (Vitali+Hurwitz are qualitative) — obligation U5.

---

## 2. Hypothesis-by-hypothesis ledger

| step | hypothesis, in the exact form consumed | label | reason / where |
|---|---|---|---|
| 2 | `ord_{s_∞} Z_{Γ_θ} ≥ 1` | **`PROVED`** | `LAW_U3_TRANSPORT.md` §3.4; two independent routes; order is `2m(ρ₁) ≥ 2` |
| 3a | `Z_{Γ_θ}` holomorphic on `Ω̃` | **`PROVED`** | poles of `Z_Γ` are all real (`LAW_U3_TRANSPORT.md` §2.3 items 3,4); `Ω̃ ⊂ {Im s > 1}` |
| 3b | `Z_{Γ_θ} ≢ 0` on `Ω̃` | **`PROVED`** | Euler product non-vanishing on `Re s > 1`; `Ω̃` meets it |
| 4a | `Z_{G_q}(s) → Z_{Γ_θ}(s)` for `s` in the far right | **`PROVED`** | U2a (`LAW_T2_DETERMINANT.md` §3.4) + U2b (`LAW_U2B_CLOSURE.md` §4) |
| 4b | `sys(G_q) ≥ ℓ₀ > 0` uniformly | **`PROVED`** | `LAW_U2B_CLOSURE.md` Thm U2b-A: `sys = 2 arccosh λ_q ≥ 2.1225501` |
| 4c | `q`-uniform geodesic counting | **`PROVED`** for `σ ≥ 3.5` | `LAW_U2B_CLOSURE.md` Thm U2b-C, `S_q ≤ 0.4861`, explicit constants |
| 4d | `sup_q W_q < 1` for all `q`, not just `q ≤ 3000` | **`PROVED`** | discharged by the verifier's antitone check, `LAW_U2B_CLOSURE.md` §5.1 `[REPAIRED]`; `W_∞ = 0.867` |
| 5 | `Ω̃ ∩ {Re s ≥ 3.5} ≠ ∅` | **`PROVED`** | a constraint on the choice, satisfiable |
| **6** | **`{Z_{G_q}}` locally uniformly bounded on `Ω̃`** | **`OPEN`** | **U1-min, §4. The whole remaining obligation.** |
| 7 | Vitali–Porter | `CITATION` | classical |
| 8 | identity theorem; `Ω̃` connected | **`PROVED`** | |
| 9 | `∃r`: `D̄(s_∞,r) ⊂ Ω̃`, `Z_{Γ_θ} ≠ 0` on `∂D` | **`PROVED`** | isolated zeros; = U6 |
| 10 | Hurwitz | `CITATION` | classical |
| 11 | `r < 1/4` | **`PROVED`** | arithmetic; **corrects the parent's `r < 1/8`** |
| 12 | finite base `q ≤ Q₀` (U4 per instance); `Q₀` effectivity | `OPEN`, off-audit | U4, U5, unchanged |

**No step other than 6 is open.** The lane's working assumption — "the tail needs U1" — is
**correct in substance and wrong in strength**: what it needs is Step 6 on the *minimal* domain,
which is a materially weaker statement than U1 as written in `LAW_T2_DETERMINANT.md` §3.2 or as
implemented in `LAW_U1_GROWTH.md` §1.2.

---

## 3. The candidate weakenings of Step 6, each adjudicated

### 3.1 `PROVED` — "boundedness on a small disc around `s_∞` only" is **insufficient**

> **Lemma M-1.** Suppose `{Z_{G_q}}` is locally uniformly bounded on `D = D(s_∞, r)` and nothing
> more is assumed. Then the tail conclusion does not follow.
>
> *Proof.* Montel gives a subsequence converging locally uniformly on `D` to some holomorphic
> `F`. Hurwitz applied to that subsequence needs `F(s_∞) = 0` and `F ≢ 0`. Nothing in the
> hypotheses connects `F` to `Z_{Γ_θ}`: the only proved convergence statement (Step 4) lives on
> `Re s ≥ 3.5`, which is disjoint from `D ⊂ {Re s ≤ 1/2}`, and two holomorphic functions agreeing
> nowhere in `D` are unconstrained on `D`. Concretely, `F ≡ c ≠ 0` is consistent with every
> hypothesis, and then Hurwitz yields *no zeros* in `D` for large `q`. ∎

**Consequence, and it is the structural core of this audit.** The boundedness domain and the
convergence set must be **the same connected domain**. Since the convergence set is pinned to
`Re s > 1` by the abscissa of the Selberg Euler product (`δ = 1` for every `G_q`), and the target
is pinned to `Re s = 1/4` by `s_∞ = ρ₁/2`, **the family must be controlled across the whole
segment `1/4 − r ≤ Re s ≤ 3.5` at height `≈ t_∞`.** That corridor is irreducible. Everything
else in U1 is negotiable.

**What *is* negotiable in the corridor's geometry:**
- its **height** `2δ` may be arbitrarily small (Step 4's `E` can sit inside the tube);
- its **left end** may be anywhere `> 1/4 − r`, hence anywhere `> 3/16` if `r = 1/16` is chosen,
  and in the limit anywhere `> 1/4 − ε`;
- its **right end** must reach `Re s ≥ 3.5` (U2b's proved threshold) — or `Re s > 1` if a
  convergence proof at a lower abscissa is ever supplied; `LAW_U2B_CLOSURE.md` §5.2's `σ₀ = 3.05`
  method floor is the current limit and §5.2 there says exactly which inequality is missing.

### 3.2 `PROVED` — "one-point bound + equicontinuity" is **equivalent, not weaker**

The brief's second candidate. For a family of *holomorphic* functions on a domain `Ω̃`:

- local uniform boundedness ⟹ equicontinuity on compacts (Cauchy estimate on derivatives);
- equicontinuity on compacts + boundedness at **one** point `s_0 ∈ Ω̃` ⟹ local uniform
  boundedness (chain compacts along a path from `s_0`; connectedness again).

So the two formulations differ by one point-bound, and that point-bound is **free**: take
`s_0 ∈ Ω̃ ∩ {Re s ≥ 3.5}`, where `LAW_U2B_CLOSURE.md` Thm U2b-C gives
`|Z_{G_q}(s_0)| ≤ 1.6259` `PROVED`.

> **Ruling.** `U1-min` may be *restated* as "the family `{Z_{G_q}}` is equicontinuous on `Ω̃`,
> uniformly in `q` on compacts". This is a **cosmetic** reformulation. It is worth recording only
> because it names a different attack surface (derivative bounds, e.g. via `Z'/Z` = a sum over
> geodesics — but that sum diverges left of `Re s = 1`, so the surface is the same wall).
> **No reduction.** `PROVED`.

### 3.3 `PROVED` — "Montel via zero-free right edge + FE" is **dead twice over**

The brief's third candidate. Two independent kills:

1. **Zero-freeness / boundedness on a region disjoint from the corridor gives nothing.**
   `LAW_U1_GROWTH.md` §5.3 already proves this with an explicit witness
   (`Z_q · e^{−N(s−2)²}` is uniformly bounded on `Re s ≥ 3/2` and unbounded on `U`).
   U2b Thm U2b-C's two-sided bound `0.3783 ≤ |Z_{G_q}| ≤ 1.6259` on `Re s ≥ 3.5` is exactly such
   a region: it is *both* a bound and a zero-free statement, and it is still worth nothing on `U`
   by itself. `PROVED`.
2. **Transporting it by the functional equation lands outside the corridor, and lands on a
   quantity that is `PROVED` unbounded.** `Re s ≥ σ₀ ≥ 3.05 ↦ Re s ≤ 1 − σ₀ ≤ −2.05`, disjoint
   from `Ω̃_min ⊂ {Re s > 1/8}`; and `LAW_U1PHI_PROOF_ROUTE.md` §3.2 (Uφp.12) `PROVED`
   `|Z_{G_q}(1−σ₀−it)| → ∞`. So the transported bound does not exist. `PROVED`.

> **But the FE is not dead in general — only at `σ₀ > 1`.** Reflecting a line
> `Re s = σ ∈ (3/4, 1)` lands at `Re s = 1 − σ ∈ (0, 1/4)`, **inside** the corridor, and Theorem
> E3 (`LAW_U1PHI_PROOF_ROUTE.md` §2.4) does **not** apply there because the Dirichlet series
> (2.1) diverges for `Re s < 1`. That surviving window is `(U1-φ-a′)`, and §5 audits it.

### 3.4 `PROVED` — "the cheapest Vitali" is already being used

Vitali–Porter's own minimal hypotheses are: (a) a **domain** (open, connected); (b) local uniform
boundedness on it; (c) pointwise convergence on a subset with an accumulation point **in the
domain**. There is no cheaper classical statement: dropping (b) to pointwise boundedness gives
only Osgood's theorem (local uniform boundedness on a *dense open* subset, by Baire), which does
not locate the good set and in particular cannot be forced to contain `D(s_∞, r)`. Dropping (a)'s
connectedness breaks Step 8. **The lane's use of Vitali is already at the classical floor.**
`PROVED` (by inspection of the theorem's hypotheses).

---

## 4. U1-min — the sharpest true statement of the remaining obligation

> ### **(U1-min).** There exist `r ∈ (0, 1/4)`, `δ ∈ (0, 1/2]`, `σ_R ≥ 3.5`, `Q₁`, and `A < ∞`
> ### — all independent of `q` — such that, with
> ```
>      Om~  :=  { 1/4 - r < Re s < sigma_R + 1 ,  | Im s - t_inf | < delta }        (open rectangle)
>      requiring   r < delta            (so that D(s_inf, r) subset Om~)
> ```
> ### one has
> ```
>      sup_{q >= Q1}  sup_{s in K'}  | Z_{G_q}(s) |  <=  A(K')  <  infinity
>      for every compact  K' subset Om~ .
> ```
>
> Then, with everything else in §2 `PROVED`, the tail theorem follows: for every `q ≥ Q₀(r)`,
> `Z_{G_q}` has a zero `s_q` with `|s_q − s_∞| < r`, hence `Re s_q < 1/2 − (1/4 − r)`.

**Why this is minimal, clause by clause.**

| clause | why it cannot be dropped |
|---|---|
| `Ω̃` **connected** | Step 8 (identity theorem). Lemma M-1 is the counterexample. |
| left edge `> 1/4 − r` **but no further left** | `D(s_∞,r)` must fit; nothing below is used. §3.1. **`Re s = 0` and `Re s = −1/10` are not required by anything.** |
| right edge `≥ σ_R` | Step 5 + Step 4's proved abscissa. |
| `|Im s − t_∞| < δ`, `δ` arbitrary | Steps 2, 9–11 are all at height `t_∞`. **No `t`-uniformity.** |
| **local** uniform boundedness (not global, not exponential-order) | Steps 7, 10 use only compacts. `LAW_U1_GROWTH.md` U1.1 already `PROVED` this half. |
| `q`-uniform (`sup_q`) | Steps 7, 10 are statements about the sequence. Irreducible. |

**What U1-min does *not* ask for, and the parent formulations do.**
- No `A e^{B(1+|s|)²}` shape (`LAW_T2_DETERMINANT.md` §3.2 (T2′-a)) — retired by U1.1.
- No `Ω̃ ⊇ {Re s > 1}` (`LAW_T2_DETERMINANT.md` §3.2, pre-amendment) — retired by the 2026-08-16
  amendment; U1-min confirms the amendment and goes further.
- No `K = [−1/10, σ₀] × …` (`LAW_U1_GROWTH.md` §1.2 / `LAW_U2B_CLOSURE.md` Lemma U2b-8) — the
  left edge `−1/10` is **not needed**, and §5.1 shows this is the single most consequential
  weakening, because it is what moves the crux out of the region where Theorem E3 refutes it.
- No bound at `Re s = −1` — which is precisely why `LAW_U1PHI_PROOF_ROUTE.md` §4.1's refutation of
  Lemma U1φ-1's necessity half is correct, and this audit independently confirms it: **`Re s = −1`
  is outside `Ω̃_min` by a margin of `1.1`, not by a hair.**

**Evidence for U1-min, honestly.** `HEURISTIC` and **mixed**:
- *for*: `LAW_U1_GROWTH.md` §10 addendum — the identified-domain `∂U` sup is flat (log-log slope
  `+0.071`) over `q = 12…100`, and the `Re s = 1/2` point decays (`−0.574`). Both live inside
  `Ω̃_min`.
- *against*: `LAW_U1PHI_PROOF_ROUTE.md` §4.3's per-point table gives `dU_2` (`Re s = 0.2500`,
  the abscissa of `s_∞` itself) a measured slope `+0.61` over `q = 12…40`, against an FE-predicted
  `+0.50`. That point is **inside** `Ω̃_min`. The two readings are computed over different `q`
  ranges (`12…40` vs `12…100`) and are not reconciled anywhere in the lane.
- *caveats standing*: the proxy is `det(1−L⁺)det(1−L⁻)`, whose identification with `Z_{G_q}` is
  obligation **U4**, `GAP` for `q ≠ 5`; float midpoints; no interval arithmetic; no winding.

> **The single cheapest decisive experiment this audit can name** (recorded, not run — this is an
> audit): **the per-point `q`-slope at `dU_2`, `Re s = 1/4`, over the full extended range
> `q = 12…100`.** `LAW_U1_GROWTH.md` §10's aggregate is flat; `LAW_U1PHI_PROOF_ROUTE.md` §4.3's
> `q ≤ 40` slice is `+0.61` at that very point. That number is already inside the extended-guard
> receipts (`law_probes/u1_guard_extended.json`) and needs only to be read out and refitted — no
> new compute. It measures U1-min at the exact abscissa of `s_∞`, which is the abscissa that
> matters, and it discriminates between the two contradictory readings the lane currently holds.

---

## 5. Audit of `(U1-φ-a′)` against U1-min

`(U1-φ-a′)` (`LAW_U1PHI_PROOF_ROUTE.md` §5.1) is a *sufficient condition* for U1-min via the
maximum principle. It is not the obligation; it is one implementation. Four findings.

### 5.1 `PROVED` — the window `(3/4, 1)` is correct, and the reason is exactly the left edge

Reflection `s ↦ 1 − s` maps `Re s = σ` to `Re s = 1 − σ`. To cover a left edge at `1/4 − r` one
needs `1 − σ ≤ 1/4 − r`, i.e. **`σ ≥ 3/4 + r`**. Theorem E3 (`LAW_U1PHI_PROOF_ROUTE.md` §2.4)
`PROVED` kills every `σ ≥ 1`. Hence `σ ∈ [3/4 + r, 1)`, non-empty for every `r < 1/4`. The
parent's stated window `(3/4, 1)` is the **union over `r`**; a *single* instance needs
`σ > 3/4 + r`. Both readings are correct; the parent does not distinguish them and the
distinction is what §5.2 exploits.

**This is the payoff of U1-min's left-edge weakening.** With the old `K = [−1/10, …]` one would
need `σ ≥ 11/10 > 1` — inside E3's kill zone. **The lane's crux was refuted at an abscissa it
never needed to visit.** That is the single most consequential finding of this audit, and it
independently confirms `LAW_U1PHI_PROOF_ROUTE.md` §5.1 by a route that does not pass through
`LAW_U1PHI_TEST.md` at all.

### 5.2 `PROVED` — the required `φ_q` decay is **any exponent `> 1/2`**, not `3/4`

`r` is free in `(0, 1/4)` (Step 11 — the parent's `r < 1/8` is over-tight). Taking `r ↓ 0` allows
`σ ↓ 3/4`, and the required decay exponent `2σ − 1 ↓ 1/2`. Concretely:

| `r` | admissible `σ` | required exponent `2σ − 1` | final off-line margin `1/4 − r` |
|---|---|---|---|
| `1/8` (parent's choice) | `> 7/8` | `> 3/4` | `1/8 = 0.125` |
| `1/16` | `> 13/16` | `> 5/8` | `3/16 = 0.1875` |
| `1/32` | `> 25/32` | `> 9/16` | `7/32 = 0.219` |
| `→ 0` | `→ 3/4⁺` | `→ 1/2⁺` | `→ 1/4` |

> **Note the direction is favourable in both columns simultaneously.** Shrinking `r` makes the
> required decay **weaker** *and* the delivered margin **larger**. There is no trade-off. The only
> cost is that `Q₀(r)` grows, which is invisible because `Q₀` is ineffective anyway (U5).
>
> **Sharpest true form of the left-edge obligation:**
> `∃ σ ∈ (3/4, 1)` and `ε > 2σ − 1` with `|φ_q(σ + it)| = O(q^{−ε})`. Since `σ` may be taken
> arbitrarily close to `3/4`, **any decay of exponent strictly greater than `1/2`, at any single
> abscissa in `(3/4, 1)`, suffices.** `PROVED`.

### 5.3 `PROVED` — U1-min and `(U1-φ-a′)`(ii) are the same unknown, oppositely signed

`LAW_U1PHI_PROOF_ROUTE.md` §4.3 retrodicts the guard by
`|Z_{G_q}(σ+it)| = |κ_q(1−σ+it)|·|Z_{G_q}(1−σ+it)|` with `|κ_q| ≍ q^{1−2σ}`, predicting
`q^{+1/2}` growth at `Re s = 1/4` — i.e. predicting **U1-min FALSE**.

But `|κ_q| ≍ q^{1−2σ}` is `|E_q · φ_q|` at the reflected abscissa, and `|E_q| ≍ (q/2π)^{2σ'−1}`
with `σ' = 1 − σ`. So the prediction is exactly the assumption **`|φ_q(1−σ+it)| ≍ 1`**, i.e. *no
decay at an abscissa in `(3/4, 1)`* — which is the negation of `(U1-φ-a′)`(ii).

> **Ruling.** The lane's adverse heuristic and its open obligation are **one statement**:
> *how large is `φ_q` on `3/4 < Re s < 1`?* No evidence in the lane bears on it: Theorems E3/E4
> are `PROVED` only for `Re s > 1` where the Dirichlet series converges; the critical-line phase
> work of `LAW_U1PHI_TEST.md` lives at `Re s = 1/2` where `|φ_q| = 1` by unitarity and carries no
> modulus information; and `LAW_U1PHI_PROOF_ROUTE.md` §9 explicitly flags its own `σ = 0.75` and
> `σ = 1.05` rows as **truncation artefacts, not evidence**. `OPEN`, with zero evidence either
> way. That is the honest state of the crux.

### 5.4 `PROVED` (the gap) — `(U1-φ-a′)` as written omits the horizontal edges

The maximum principle on `Rect = [1−σ, σ] × [t_∞ − δ, t_∞ + δ]` needs **four** sides:

| side | supplied by |
|---|---|
| `Re s = σ` | `(U1-φ-a′)`(i) |
| `Re s = 1 − σ` | `(U1-φ-a′)`(i) + (ii) via `|Z(1−s)| = |κ_q(s)||Z(s)|` |
| `Im s = t_∞ ± δ`, `Re s ∈ [1−σ, σ]` | **nothing** |

**Repair, and its price.** Phragmén–Lindelöf for the strip `1 − σ ≤ Re s ≤ σ`: if `|Z_{G_q}| ≤ A`
on both vertical lines **for all real `t`**, and `Z_{G_q}` is of finite order in the strip for
each fixed `q` (permitted to be `q`-dependent — P–L's conclusion is the edge bound `A` regardless
of the a-priori constants, provided the order is below the strip's Phragmén–Lindelöf threshold),
then `|Z_{G_q}| ≤ A` throughout the strip. `Z_Γ` is of order 2 (`CITATION`:
Borthwick–Judge–Perry Thm 1.1 for the torsion-free statement; Teo Thm 2.2's regularized-
determinant factorization for the orbifold case — the same import `LAW_U3_TRANSPORT.md` §2.5
already carries), which is far below the threshold. `PROVABLE`; nobody has written it out.

> **Price:** `(U1-φ-a′)`(i) and (ii) must hold **for all real `t`**, not for `|t| ≤ t_∞ + 1` as
> written. So: **the *theorem* needs no `t`-uniformity (§4), but this *implementation* does.**
> An implementation that bounds the two horizontal segments directly would avoid it; none is known.
> This is a hypothesis-strengthening that `LAW_U1PHI_PROOF_ROUTE.md` §5.1 does not record, and it
> should be written into that note.

---

## 6. Two further audit findings

### 6.1 `PROVED` — Step 3's "`Ω̃` avoids the poles of `Z_{Γ_θ}`" is an unstated hypothesis

No parent note states it. It is free (`Ω̃ ⊂ {Im s > 1}`, poles all real), but it is a genuine
constraint on `Ω̃`: it forbids pushing the corridor down toward the real axis, which one might
otherwise be tempted to do to shorten it. Record it in `LAW_T2_DETERMINANT.md` §3.2's statement
of (T2′).

### 6.2 `PROVED` — `(U1-φ-b)` alone does **not** close U1

`LAW_U1_GROWTH.md` §6 states "*Either one, together with §2's uniform Euler bound and Lemma U1-0,
closes U1*". For `(U1-φ-b)` — a `q`-uniform resonance count on `|s − 1/2| ≤ 8` — this is false as
an inference:

- a Hadamard factorization `Z_{G_q}(s) = e^{P_q(s)} ∏_ρ E_2(s/ρ)` bounds `|Z|` on a compact only
  given (a) `q`-uniform control of the degree-`≤ 2` polynomial `P_q`, and (b) `q`-uniform control
  of the **global** zero distribution, not merely of the count inside one disc;
- (b) is **not** available: `LAW_U1_GROWTH.md` §5.2 (U1.16) `PROVED` that the Weyl counting is
  uniform only in the `T²` coefficient, while the elliptic mass
  `M(q) = (1/π)log(2e^γ q/π) + O(q^{−2})` enters the **linear-in-`T`** coefficient and at `T ≈ 8`
  is the same size as the `T²` term (`17.6` vs `16.0` at `q = 1000`);
- (a) is untouched anywhere in the lane.

> **Ruling.** `(U1-φ-b)` is an **ingredient** of a Hadamard route, not a closure of it.
> `LAW_U1_GROWTH.md` §6's "either one … closes U1" should be amended to
> *"(U1-φ-a) closes U1; (U1-φ-b) is one of at least three ingredients a Hadamard route needs, the
> others being uniform control of the global zero distribution — refuted-as-free by U1.16 — and of
> the Hadamard exponential."* This matters because `(U1-φ-b)` is currently listed as a live
> alternative in the ledger and, on the audit's reading, it is not one.

---

## 7. Comparison table — U1 vs (U1-φ-a′) vs U1-min

| | **U1** (`LAW_T2_DETERMINANT.md` §3.2 / `LAW_U1_GROWTH.md` §1.2) | **(U1-φ-a′)** (`LAW_U1PHI_PROOF_ROUTE.md` §5.1) | **U1-min** (§4, this note) |
|---|---|---|---|
| **logical type** | the obligation, as historically posed | a *sufficient condition* for it (one implementation) | the obligation, minimal |
| **object bounded** | `Z_{G_q}` | `Z_{G_q}` **and** `φ_q` | `Z_{G_q}` |
| **domain** | `K = [−1/10, σ₀] × [t_∞ ± 3/10]` **∪** `{Re s ≥ σ₀}` | **one vertical segment** `Re s = σ`, `σ ∈ (3/4,1)` | open connected corridor `(1/4 − r, σ_R+1) × (t_∞ ± δ)`, `r, δ` free |
| **leftmost abscissa touched** | `−1/10` | `1 − σ ∈ (0, 1/4)` | `1/4 − r` — **arbitrarily close to `1/4`** |
| **growth shape** | `A e^{B(1+|s|)²}` originally; boundedness after U1.1 | boundedness | boundedness |
| **`t`-extent** | `|Im s − t_∞| ≤ 3/10` on `K`, **all `t`** on `Re s ≥ σ₀` | written `\|t\| ≤ t_∞+1`; **must be all `t`** once §5.4's P–L repair is applied | `\|Im s − t_∞\| < δ`, `δ` arbitrarily small. **No `t`-uniformity.** |
| **`q`-uniformity** | required | required | required — **irreducible** |
| **what it additionally demands** | a bound at `Re s = −1/10`, used by nothing | `\|φ_q(σ+it)\| = O(q^{−(2σ−1)})`; §5.2: any exponent `> 1/2` suffices | nothing beyond §4 |
| **refuted?** | **no** (its `Re s = −1` consequence was never implied — `LAW_U1PHI_PROOF_ROUTE.md` §4.1, confirmed §4 here) | **no** — E3 kills only `σ ≥ 1`; the window `(3/4,1)` is untouched | **no** |
| **evidence FOR** | extended guard flat (`+0.071`, `q = 12…100`) and decaying at `Re s = 1/2` (`−0.574`) — `HEURISTIC`, proxy modulo U4 | **none** — the strip `(3/4,1)` has never been measured; the `σ = 0.75` receipt rows are flagged truncation artefacts | same as U1's, and the guard points that support it (`dU_0`, `dU_2`) lie **inside** `Ω̃_min` |
| **evidence AGAINST** | `LAW_U1_GROWTH.md` §7.3's `+1.50` — but that slope is dominated by `Re s ≤ 0.0732`, **outside `Ω̃_min`**, so it does not bear on U1-min | the FE retrodiction `\|κ_q\| ≍ q^{1−2σ}` presumes `\|φ_q\| ≍ 1` at `1−σ`, i.e. presumes (ii) false — but that presumption is itself unmeasured (§5.3) | `dU_2` (`Re s = 1/4`) slope `+0.61` over `q = 12…40` (`LAW_U1PHI_PROOF_ROUTE.md` §4.3) — **the one adverse data point inside the minimal domain**; unreconciled with the flat aggregate |
| **status** | superseded by U1-min | `GAP` (both halves) | **`OPEN` — the whole remaining obligation** |

**Reading of the table.** The historical U1 asked for a bound on a region that reaches to
`Re s = −1/10`. Every adverse measurement the lane has (`§7.3`'s `+1.50`, `§4.3`'s `dU_3`/`dU_4`
slopes, `Uφp.12`'s proved divergence) is concentrated at `Re s ≤ 0.0732` — **outside `Ω̃_min`**.
Every supportive measurement (`dU_0` at `Re s = 1/2`, the flat identified-domain aggregate) is
**inside** it. **The lane has been measuring, and worrying about, a region its theorem does not
need.** One data point inside the minimal domain is adverse (`dU_2`, `q ≤ 40`), and reconciling it
against the extended range is the cheapest next act (§4).

---

## 8. Status ledger of this note

| # | Claim | Status | Where |
|---|---|---|---|
| M.1 | The 12-step chain; only Step 6 is open | **`PROVED`** | §1, §2 |
| M.2 | Step 2 needs only `ord_{s_∞} Z_{Γ_θ} ≥ 1`, not `= 2` | **`PROVED`** | §1 Step 2 |
| M.3 | Step 4's `E` may be a single convergent sequence | **`PROVED`** | §1 Step 4 |
| M.4 | Lemma M-1: a disc around `s_∞` alone is insufficient | **`PROVED`** | §3.1 |
| M.5 | The corridor `1/4 − r → σ_R` at height `t_∞` is irreducible | **`PROVED`** | §3.1 |
| M.6 | One-point bound + equicontinuity ⟺ local uniform boundedness | **`PROVED`** | §3.2 |
| M.7 | Montel-via-zero-free-right-edge + FE: dead twice (disjointness; `Uφp.12`) | **`PROVED`** | §3.3 |
| M.8 | Vitali's hypotheses are already at the classical floor; Osgood does not help | **`PROVED`** | §3.4 |
| M.9 | **U1-min**, stated, with per-clause minimality | **`OPEN`** (the statement); `PROVED` (the minimality analysis) | §4 |
| M.10 | `r < 1/4` and margin `1/4 − r` — **corrects `r < 1/8`, `η = 1/8 − r`** | **`PROVED`** | §1 Step 11 |
| M.11 | A single `(U1-φ-a′)` instance needs `σ > 3/4 + r`, not merely `σ > 3/4` | **`PROVED`** | §5.1 |
| M.12 | Required `φ_q` decay exponent is **any `> 1/2`**, `r` being free | **`PROVED`** | §5.2 |
| M.13 | U1-min and `(U1-φ-a′)`(ii) are one unknown: `φ_q` on `3/4 < Re s < 1`, **zero evidence either way** | **`PROVED`** (the equivalence of statements) | §5.3 |
| M.14 | `(U1-φ-a′)` omits the horizontal edges; P–L repairs it at the price of all-`t` | **`PROVED`** (gap) + **`PROVABLE`** (repair) | §5.4 |
| M.15 | "`Ω̃` avoids the poles of `Z_{Γ_θ}`" is an unstated hypothesis | **`PROVED`** | §6.1 |
| M.16 | **`(U1-φ-b)` alone does not close U1** — corrects `LAW_U1_GROWTH.md` §6 | **`PROVED`** | §6.2 |
| M.17 | Every adverse guard measurement lies outside `Ω̃_min`; one (`dU_2`) lies inside | **`PROVED`** (from the parents' own tables) | §7 |

---

## 9. Corrections owed to parent notes

1. **`LAW_T2_DETERMINANT.md` §3.2** — `r ∈ (0,1/8)` and "margin `η = 1/8 − r`" → `r ∈ (0,1/4)`,
   margin `1/4 − r`. Add Step 3's hypothesis: `Ω̃` must avoid the (real) poles of `Z_{Γ_θ}`.
2. **`LAW_U1_GROWTH.md` §9** — same `r` correction in the assembled theorem statement.
3. **`LAW_U1_GROWTH.md` §6** — "*Either one … closes U1*" over-claims for `(U1-φ-b)`; amend per
   §6.2.
4. **`LAW_U1_GROWTH.md` §1.2 / `LAW_U2B_CLOSURE.md` Lemma U2b-8** — the left edge `−1/10` is not
   required by any step. Replace with `1/4 − r`. This is not cosmetic: it is what moves the crux
   out of Theorem E3's kill zone (§5.1).
5. **`LAW_U1PHI_PROOF_ROUTE.md` §5.1** — record that a single instance needs `σ > 3/4 + r`; that
   the exponent may be pushed to `1/2⁺`; and that (i)/(ii) must hold for all real `t` once the
   horizontal edges are repaired by Phragmén–Lindelöf (§5.4).

---

## 10. Honest verdict

**The lane's serving assumption is substantively right and quantitatively wrong.** The tail
argument does need a `q`-uniform boundedness statement, and there is no soft version of it:
Lemma M-1 shows the domain cannot be shrunk to a disc, §3.2 shows the equicontinuity phrasing is
cosmetic, §3.3 shows Montel-via-FE is dead at every abscissa the Euler product can reach, and
§3.4 shows Vitali is already being used at its classical floor. **U1 is not replaceable by a
weaker kind of hypothesis.**

What *is* wrong is the domain. U1 as implemented asks for control on `[−1/10, σ₀] × [t_∞ ± 3/10]`;
the theorem asks for control on `(1/4 − r, σ_R+1) × (t_∞ ± δ)` with `r, δ` free. The lane's three
`PROVED` negative results — Theorem E3, `Uφp.12`'s `|Z_{G_q}(1−σ₀−it)| → ∞`, and `§7.3`'s adverse
guard slope — **all live strictly outside the minimal domain.** None of them bears on U1-min.

**So: U1 as stated is NOT minimal, and the excess is exactly the part that has been refuted.**
The crux, correctly located, is one sentence: **how large is `φ_q(s)` on `3/4 < Re s < 1`?** —
where the lane has, at present, no evidence in either direction, because that strip lies below the
abscissa of convergence of the only handle on `φ_q` it possesses and above the critical line where
unitarity makes the modulus trivial.

---

## 11. What this note claims and does not claim

**Claims.** The 12-step chain with per-step hypotheses (§1); that only Step 6 is open (§2); Lemma
M-1 (§3.1); the equivalence of the equicontinuity phrasing (§3.2); the double kill of the
zero-free/FE route at `σ₀ > 1` (§3.3); the statement U1-min with per-clause minimality (§4); the
`r < 1/4` correction and the consequent `σ > 3/4 + r` / exponent-`> 1/2` sharpening (§5.1–5.2);
the identification of U1-min with `(U1-φ-a′)`(ii) as one unknown (§5.3); the missing horizontal
edges (§5.4); the unstated pole-avoidance hypothesis (§6.1); and that `(U1-φ-b)` alone does not
close U1 (§6.2).

**Does not claim.** **No progress on U1-min itself** — it is `OPEN` and this note does not move
it. No new numerics: every number quoted is read from a parent note's table and inherits that
note's label and caveats (float, no interval arithmetic, no certificate, proxy modulo U4). No
independent re-verification of U2b's `S_q ≤ 0.4861`, of U3's citations (`V1`–`V3` remain owed), or
of `LAW_U1PHI_PROOF_ROUTE.md`'s Theorems E3/E4 — this audit takes their `PROVED` labels at face
value and its conclusions are conditional on them. In particular **`LAW_U1PHI_PROOF_ROUTE.md` is
itself flagged PENDING adversarial verification**, and M.11–M.13 inherit that pendency. No claim
that `Ω̃_min` is the unique minimal domain — only that its listed clauses are each irreducible.
The Phragmén–Lindelöf repair of §5.4 is `PROVABLE`, sketched, not written out. No prior-art
clearance for anything here; nothing in this note is novel mathematics — it is bookkeeping over
the lane's own results.

**A refutation was actively sought**, and the honest answer to the brief's framing is **split**:
the brief asked whether a *weaker kind* of hypothesis suffices, and the answer is **no** — all
three named candidates fail, two provably (§3.1, §3.3) and one because it is the same statement
(§3.2). But the brief's underlying suspicion was right for a different reason: the hypothesis is
minimal in *kind* and grossly over-stated in *domain*, and the over-statement is precisely
coextensive with the region where the lane has already proved things go wrong.

---

READY FOR JUDGING

---

## Addendum (frontier, same day): the named cheap check — per-point refit over full range

From existing receipts only (u1_sup.json + u1_sup_q40.json +
u1_guard_extended.json, q = 12..100), log-log slopes of |det+·det−| per ∂U
point:

| point | Re s | slope (full q≤100) | slope (q≤40) |
|---|---|---|---|
| dU_0 | 0.500 | **−0.574** | −1.026 |
| dU_1 | 0.427 | **−0.193** | −1.287 |
| dU_2 | 0.250 | **+1.056** | +1.065 |
| dU_6 | 0.250 (below t_∞) | −0.039 | −0.504 |
| dU_7 | 0.427 (below) | −0.610 | −0.978 |

**Finding: dU_2 (the point directly ABOVE s_∞ at Re = 1/4) grows steadily
(0.52 → 8.09 from q=16 to 100, slope +1.06) while its mirror dU_6 (directly
BELOW s_∞) is flat.** This is inside/on the boundary of Ω̃_min and is NOT
dissolved by the identification-domain argument. Asymmetry above-vs-below
t_∞ suggests structure (approaching zeros/divisor above the anchor?) rather
than generic growth, but that is a hypothesis, not a reconciliation.
Adjudication delegated to the running strip measurement lane (direct φ_q on
σ ∈ (3/4,1)) and, if needed, a dedicated dU_2 trace (finer t-scan at
Re = 1/4). U1-min's status: OPEN with one adverse boundary point and two
supportive interior points.
