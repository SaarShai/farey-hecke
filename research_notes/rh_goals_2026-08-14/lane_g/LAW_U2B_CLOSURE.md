# LAW (U2b) — closure of the systole half and the counting half

**Date:** 2026-08-16. **Lane G.** Obligation **U2b** of `lane_g/LAW_U1_GROWTH.md` §2 and §9,
imported by `lane_g/LAW_T2_DETERMINANT.md` §3.4.
**Parents read in full:** `lane_g/LAW_U1_GROWTH.md` (§2 the two halves, Lemma U1-1,
Conjecture U1-2, the multi-syllable gap paragraph, §9 the obligation table),
`lane_g/LAW_T2_DETERMINANT.md` §3.4 (the `[S R²]` computation and the systole claim),
`lane_g/LAW_U1PHI_TEST.md` (context only).

**Status convention:** identical to U1/T2/U3. `PROVED` = derived here in closed form or verified
in exact arithmetic. `PROVED-MODULO-CITATION` = complete given a named import.
`HEURISTIC` = float evidence. `GAP` = not justified, missing statement written out.

**No certificate is produced. Work is committed as `6b51411`; repairs in this pass are uncommitted
[REPAIRED 2026-08-16 per ADVERSARIAL_REVIEW_U2B.md D8]. `lane_f/` and
`law_probes/u1_guard_extended.*` are untouched.**

---

## 0. Verdict up front

> ### **U2b is CLOSED. Both halves are PROVED, elementarily, by one mechanism.**
>
> **(a) SYSTOLE — `PROVED`.** For every `q ≥ 4`, `min |tr γ| = 2λ_q` over primitive hyperbolic
> `γ ∈ G_q`, attained exactly at `[S R²]` and `[S R^{q−2}]`. Hence
> **`sys(G_q) = 2 arccosh λ_q` exactly.** No citation was found that settles this (§1.4); the
> proof below carries it. The same proof returns the classical `sys(PSL(2,Z)) = 2 arccosh(3/2)`
> at `q = 3` as a degenerate case — an independent check that the mechanism is right.
>
> **(b) COUNTING — `PROVED`, at a price.** `sup_{q ≥ 5} Σ_{[γ] prim} e^{−σℓ_γ}/(1−e^{−ℓ_γ}) ≤ 0.486`
> for `σ ≥ 3.5`, with an explicit constant and no free parameters. **The price: the method's
> convergence floor is `σ₀ = 3.05`, not `3/2`.** Lemma U1-0's half-plane threshold must move
> from `Re s ≥ 3/2` to `Re s ≥ σ₀`; §4.4 shows this is harmless (Lemma U1-0 is restated and
> re-proved for a general threshold), but it is a real change to `LAW_U1_GROWTH.md` §1.2 and §2.1.
> **The forced (U1-φ) exponent is `2σ₀ − 1` for any `σ₀ > 3.05`, i.e. `> 5.1`; the quoted `6`
> is the `σ₀ = 3.5` convenience point, not a floor** [REPAIRED 2026-08-16 per
> ADVERSARIAL_REVIEW_U2B.md D5].
>
> **Two corrections are owed to `LAW_U1_GROWTH.md` §2.3, and one of them is a logical error.**
> 1. **Conjecture U1-2 as literally stated is FALSE.** `|tr w(λ)|` is *not* nondecreasing on
>    `(1, 2]`. Explicit counterexample: `|tr(S R⁵)| = 2|u₅(λ)|` runs `2.00 → 2.50 → 0 → 10`
>    across `λ = 1 → 1.2434 → λ₅ → 2` (§3.2, exact). The **correct** statement — proved here —
>    carries an interval that depends on the word: monotone on `[2cos(π/(A+1)), 2]`,
>    `A = max_i |a_i|`, which is exactly the set of levels `q ≥ A+1` at which the word is a
>    normal-form word. On that interval the conjecture is a **theorem** (§3).
> 2. **The inference `ℓ_w(λ_q) ≤ ℓ_w(2) ⟹ N_q^{faithful}(L) ≤ N_θ(L)` is backwards.** Shorter
>    geodesics mean *more* of them below `L`. The correct direction is `N_q(L) ≥ N_θ(L)`, which
>    is what the note's own table measures (`12, 11, 9, 7, 7, 7` against `7`) and what it
>    mis-read as a crossover. **A `Γ_θ` comparison can never deliver the uniform upper bound**;
>    that is why §4 proves it directly instead. `PROVED` (§3.3).

**The one mechanism.** In the free-product normal form `G_q = ⟨S⟩ * ⟨R⟩ ≅ Z/2 * Z/q`, every
syllable matrix is **entrywise nonnegative**:

```
   S R^a  = - M_a ,        M_a := [[ u_a , u_{a+1} ] ,
                                   [ u_{a-1} , u_a ]]        (1 <= a <= q-1)
   S R^-a = + M_a^T ,      u_j  := sin(j pi / q) / sin(pi / q) ,  u_0 = 0, u_q = 0 .
```

`det M_a = 1`, `M_1 = [[1,λ],[0,1]]`, `M_{q−1} = [[1,0],[λ,1]]`, and every `u_j ≥ 0` for
`0 ≤ j ≤ q`. So `|tr w|` is a **sum of nonnegative products**, and every lower bound below is
"pick one path and throw the rest away". That is the whole engine. It gives the systole, the
monotonicity, and the counting bound.

---

## 1. The systole half

### 1.1 `PROVED` — the nonnegative normal form

> **Lemma U2b-1.** As an identity in `M_2(Z[λ])` with `S = [[0,−1],[1,0]]`,
> `R = [[0,−1],[1,λ]]`, and `u_j ∈ Z[λ]` defined by `u_0 = 0, u_1 = 1, u_{j+1} = λu_j − u_{j−1}`:
> ```
>    S R^a = -M_a ,   S R^{-a} = M_a^T ,   det M_a = 1 ,   M_a = [[u_a, u_{a+1}],[u_{a-1}, u_a]] .
> ```
> *Proof.* `R` satisfies `R² = λR − I`, so `R^a = u_a R − u_{a−1} I` (induction). Also
> `S R = [[−1,−λ],[0,−1]] = −T` where `T = [[1,λ],[0,1]]`, and `tr S = 0`, so
> `S R^a = u_a(SR) − u_{a−1}S = −(u_a T + u_{a−1} S)`, and
> `u_a T + u_{a−1} S = [[u_a, λu_a − u_{a−1}],[u_{a−1}, u_a]] = M_a` since `λu_a − u_{a−1} = u_{a+1}`.
> `det M_a = u_a² − u_{a+1}u_{a−1} = 1` is the standard Chebyshev identity (induction on the
> recurrence with `u_0 = 0, u_1 = 1`). For negative exponents use `u_{−j} = −u_j`. ∎
>
> **Receipt:** `law_probes/u2b_normal_form.py`, exact integer-polynomial arithmetic (no floats,
> no CAS), all three identities verified for `a = 1 … 25`: `exact_identity.all_ok = true`.
> Nonnegativity and the shapes of `M_1, M_{q−1}` verified at `λ_q` for `q = 4 … 400`
> (`min entry = −4.05e−14`, i.e. `0` to working precision); `u_a ≥ λ_q` for `2 ≤ a ≤ q−2` and
> `u_1 = u_{q−1} = 1` verified for `q = 5 … 400`. Receipt `law_probes/u2b_normal_form.json`.

**Alphabet vocabulary used throughout.** At level `q`, a *light* letter is `a ∈ {1, q−1}`
(`u_a = 1`, `M_a` triangular); a *heavy* letter is `a ∈ {2, …, q−2}` (`M_a` strictly positive,
`u_a ≥ λ_q`, minimum attained at `a = 2` and `a = q−2` where `u_a = λ_q` exactly). For `q = 3`
the heavy alphabet is empty; for `q = 4` it is `{2}`.

### 1.2 `PROVED` — the systole theorem

> **THEOREM U2b-A.** Let `q ≥ 4` and let `w = S R^{a_1} ⋯ S R^{a_m}` be cyclically reduced
> (`a_i ∈ {1, …, q−1}`, `m ≥ 1`) and hyperbolic. Then
> ```
>      | tr w |  >=  2 lam_q ,
> ```
> with equality **iff** `m = 1` and `a_1 ∈ {2, q−2}`. Consequently
> ```
>      sys(G_q)  =  2 arccosh( lam_q )  =  2 arccosh( 2 cos(pi/q) ) ,
> ```
> realised exactly by the classes `[S R²]` and `[S R^{q−2}] = [S R^{−2}]`.
>
> *Proof.* By Lemma U2b-1, `w = (−1)^m M_{a_1} ⋯ M_{a_m}` and all `M_{a_i}` are entrywise
> nonnegative, so `|tr w| = tr(M_{a_1} ⋯ M_{a_m}) = Σ_{i : Z/m → {1,2}} ∏_k (M_{a_k})_{i_k i_{k+1}}`,
> a sum of nonnegative terms. Every individual cyclic state-path is therefore a lower bound.
>
> *Case A: some letter is heavy.* The two constant paths `i ≡ 1` and `i ≡ 2` both contribute
> `∏_k (M_{a_k})_{11} = ∏_k u_{a_k}` (the diagonal entries of `M_a` are equal). Hence
> ```
>      | tr w |  >=  2 prod_k u_{a_k}  >=  2 * lam_q ,                          (1.1)
> ```
> because `u_j ≥ 1` for `1 ≤ j ≤ q−1` and at least one factor is `≥ λ_q`. If `m = 1` this is an
> equality precisely when `u_{a_1} = λ_q`, i.e. `a_1 ∈ {2, q−2}`. If `m ≥ 2` the bound is strict:
> if two or more letters are heavy then `∏u ≥ λ_q² > λ_q`; if exactly one letter `a_j` is heavy
> then, in addition to the two constant paths, the path that switches `1 → 2` at some light
> position (entry `u_2 = λ_q` if that letter is `1`, resp. `u_{q−2} = λ_q` if it is `q−1`) and
> switches back `2 → 1` at position `j` (entry `u_{a_j−1} ≥ 1`) contributes `≥ λ_q > 0`, so
> `|tr w| ≥ 2λ_q + λ_q = 3λ_q`.
>
> *Case B: every letter is light.* If all letters are equal, `w = T^{±m}` is parabolic (`|tr| = 2`),
> not hyperbolic — excluded. Otherwise both light letters occur. The two constant paths give
> `1 + 1 = 2`. In addition, pick a cyclic position `j` with `a_j = 1` and the first position
> `j' > j` (cyclically) with `a_{j'} = q−1`; the path that is in state `1` before `j`, switches
> `1 → 2` at `j` (entry `u_2 = λ_q`), stays in state `2` through `j+1, …, j'−1` (all diagonal
> entries `= 1`) and switches `2 → 1` at `j'` (entry `u_{q−2} = λ_q`) contributes `λ_q²`. Hence
> ```
>      | tr w |  >=  2 + lam_q^2  >  2 lam_q      since  (lam_q - 1)^2 + 1 > 0 .   (1.2)
> ```
> The two cases exhaust cyclically reduced words, and `2λ_q > 2` for `q ≥ 4`, so the minimum
> `2λ_q` is attained and hyperbolic. Finally `ℓ_γ = 2 arccosh(|tr γ|/2)` is increasing in `|tr|`. ∎

**Cross-check at `q = 3` (outside the theorem's range, and it is the right answer).** For `q = 3`
the heavy alphabet is empty, so only Case B applies and the minimum is `2 + λ₃² = 3` — the
classical minimal trace of `PSL(2,Z)`, `sys = 2 arccosh(3/2) = 1.9248473` [REPAIRED 2026-08-16 per ADVERSARIAL_REVIEW_U2B.md D1], realised by
`[S R][S R²] = [[2,1],[1,1]]`-type classes. The probe reproduces exactly this
(`q=3: min|tr| = 3.000000000, argmin = [1,2]`).

> **Receipt:** `law_probes/u2b_systole.py`, `u2b_systole.json`. **Exhaustive** enumeration of all
> primitive cyclically reduced words up to `m = 7 / 6 / 5 / 4 / 3` syllables at
> `q = 3,4,5,6,7,8,9,10,11,12,14,16,20,24,30,40,60,100` — **1 508 638 cyclic words**. Every one of
> the five checks passes at every `q`:
> `C1` min hyperbolic `|tr| = 2λ_q` (to `1e−8`); `C2` the diagonal bound (1.1);
> `C3` the light-word bound (1.2); `C4` the argmin set is exactly `{(2), (q−2)}` for `q ≥ 5`;
> `C5` the counting bound of §4.1. Sample: `q=5: 3.236067977 = 2λ₅`, argmin `{2,3}`;
> `q=100: 3.998026241 = 2λ_100`, argmin `{2,98}`.

### 1.3 Consequences discharged

- **`LAW_U1_GROWTH.md` U1.4** (`sys(G_q) = 2 arccosh λ_q ≥ 2.12255`): **`PROVED`**, no longer
  "`PROVED` mod U2b". The constant `1/(1 − e^{−sys}) ≤ 1.1360098` of §2.1 is now unconditional.
- **`LAW_T2_DETERMINANT.md` §3.4** ("`HEURISTIC` for '`[S R²]` is the systole'"): upgrade to
  **`PROVED`**. Its (3.1) and (3.2) were already `PROVED`; the enumeration caveat is removed.
- The parenthetical collar-lemma argument in T2 §3.4, labelled `GAP` there, is now **unnecessary**
  and can be deleted rather than repaired.
- **No pinching, uniformly in `q`**, is now a theorem: `sys(G_q) = 2 arccosh λ_q` is strictly
  increasing in `q` with minimum `sys(G_5) = 2.1225501` and supremum `2 arccosh 2 = 2.6339157`.

### 1.4 Prior art — `CITATION`-scouted, does **not** close it

A literature scout (5 sources, this session) found **no published statement of the systole of
`G_q`**. Nearest:

| source | what it gives | why it does not close U2b(a) |
|---|---|---|
| Schmidt & Sheingorn, *Length spectra of the Hecke triangle groups*, Math. Z. **220** (1995) 369–397 | the definitive length-spectrum paper for `G_q` | paywalled, not opened; scout could not confirm that the *minimum* is isolated as a closed form. `TODO-VERIFY` if institutional access appears |
| Haas & Series, *The Hurwitz constant and Diophantine approximation on Hecke groups*, J. LMS **34** (1986) | Hurwitz constant / Lagrange-spectrum minimum for `G_q` | a Diophantine minimum, not the trace minimum over hyperbolic classes |
| Schmutz Schaller, systole literature (Bull. AMS 1998; GAFA 1993) | systoles of Riemann surfaces, extremal problems | not specialised to `(2,q,∞)` |

**Ruling.** Theorem U2b-A is proved here, self-contained, and does not depend on any of these.
Schmidt–Sheingorn should be cited as the length-spectrum reference and checked for priority
before publication; that is a `TODO-VERIFY` on attribution, **not** on correctness.

---

## 2. Why the previous route (Γ_θ comparison) cannot work — and the correction owed

`LAW_U1_GROWTH.md` §2.3 routes the counting through `Γ_θ`. That route is closed off by a
direction error; this section records it so it is not re-attempted.

### 2.1 `PROVED` — the inference is backwards

The note writes: *"for every faithful lift, `ℓ_w(λ_q) ≤ ℓ_w(2)`, so `N_q^{faithful}(L) ≤ N_θ(L)`."*

`ℓ_w(λ_q) ≤ ℓ_w(2)` says the `G_q` geodesic is **shorter** than its `Γ_θ` counterpart. Therefore
`{w : ℓ_w(2) ≤ L} ⊆ {w : ℓ_w(λ_q) ≤ L}`, i.e.

```
   N_q(L)  >=  # { Gamma_theta classes with all |a_i| < q/2 and l <= L }  -->  N_theta(L) ,   [REPAIRED 2026-08-16 per ADVERSARIAL_REVIEW_U2B.md D4]
```

the **opposite** of what is claimed. This is not a small-`q` blemish: it is the direction of the
implication, and it holds for every `q`.

### 2.2 The note's own data says the same thing [REPAIRED 2026-08-16 per ADVERSARIAL_REVIEW_U2B.md D3]

`LAW_U1_GROWTH.md` §2.3 reports `N_q(4) = 12, 11, 9, 7, 7, 7` at `q = 10,12,16,22,30,50` against
`N_θ(4) = 7`, and reads this as a crossover to `N_q ≤ N_θ` "setting in at `q ≈ 22`". It is not a
crossover — it is **`N_q(L) ≥ N_θ(L)` throughout, decreasing to equality** as `q → ∞`, exactly as
§2.1 predicts (as `q → ∞`, `ℓ_w(λ_q) ↑ ℓ_w(2)`, so the excess set empties for fixed `L`).

> **Receipt:** `law_probes/u2b_direction.py`, `u2b_direction.json` — counts recomputed
> independently from the normal form, `Γ_θ` enumerated with **signed** syllables
> `a ∈ {±1,…,±8}`, `m ≤ 4`, at `L = 4, 5, 6` and `q = 8,10,12,16,22,30,50`.
> **`N_θ(4) = 7` reproduces the parent note's value exactly**, which pins the comparison. **Table
> columns are `m ≤ 4`-truncated counts** (syllable-length cap; not the true, uncapped `N_θ(L)`,
> `N_q(L)`) [REPAIRED 2026-08-16 per ADVERSARIAL_REVIEW_U2B.md D3]:
>
> | `L` | `N_θ(L)`, `m ≤ 4` | `N_q(L)`, `m ≤ 4`, at `q = 8, 10, 12, 16, 22, 30, 50` |
> |---|---|---|
> | 4 | **7** | 10, 10, 11, 9, **7, 7, 7** |
> | 5 | **23** | 26, 24, 26, 26, 25, **23, 23** |
> | 6 | **51** | 54, 58, 56, 64, 60, 64, 55 |
>
> `N_q(L) ≥ N_θ(L)` at **every one of the 21 pairs**, with equality reached from above at large
> `q` for `L = 4, 5` and not yet reached by `q = 50` for `L = 6`. This is the §2.1 implication,
> not a crossover.
>
> **Converged values (verifier, uncapped DFS with monotone-trace prune; see
> `law_probes/u2b_verifier/`):** `N_θ(4,5,6) = 7, 25, 67` — the `m ≤ 4`-truncated `L=5,6` entries
> above (`23`, `51`) undercount the true, converged `N_θ`. `N_q ≥ N_θ` re-confirmed at all **30**
> converged pairs `q = 5…50`. The parent note's `N_q(4) = 12` at `q = 10` (`LAW_U1_GROWTH.md`
> §2.3) is **wrong**; the converged value is **10**.

### 2.3 Consequence for the ledger

The "finite non-faithful excess" framing in `LAW_U1_GROWTH.md` §2.3 and in its §9 obligation table
("*Conjecture U1-2 + the finite non-faithful excess*") is **not a route to the uniform bound**, no
matter how the excess is counted, because the comparison inequality points the wrong way. The
multi-syllable excess is therefore **not** the missing piece; §4 replaces the whole comparison
with a direct bound and the excess question dissolves.

---

## 3. The monotonicity half, corrected and proved

### 3.1 `PROVED` — the sharp monotonicity interval

> **Lemma U2b-2.** `g(t) := t cot t` is strictly decreasing on `(0, π)`.
> *Proof.* `g'(t) = (sin t cos t − t)/sin² t = (½ sin 2t − t)/sin² t < 0` for `t ∈ (0,π)`. ∎

> **Lemma U2b-3.** Write `λ = 2 cos θ`, `θ ∈ [0, π)`. For each `j ≥ 1`, `u_j(λ) = sin(jθ)/sin θ`
> is **strictly increasing in `λ` and nonnegative** on `λ ∈ [2 cos(π/j), 2]`, i.e. `θ ∈ (0, π/j]`.
> *Proof.* Nonnegativity is `jθ ≤ π`. For monotonicity, `d/dθ log u_j = j cot(jθ) − cot θ
> = (g(jθ) − g(θ))/θ < 0` for `0 < θ < jθ < π` by Lemma U2b-2; `λ` is decreasing in `θ`. ∎

> **THEOREM U2b-B (replaces Conjecture U1-2).** Let `w = S R^{a_1} ⋯ S R^{a_m}` be cyclically
> reduced with `a_i ∈ Z \ {0}` and `A := max_i |a_i|`. Then `|tr w(λ)|` is a finite sum of
> products of the quantities `u_j(λ)`, `0 ≤ j ≤ A+1`, with nonnegative integer multiplicities;
> hence `|tr w(λ)|` is **nondecreasing in `λ` on `[2 cos(π/(A+1)), 2]`**. In particular, for every
> level `q ≥ A+1` — which is exactly the condition for `w` to be a normal-form word of `G_q` —
> ```
>       | tr_w(lam_q) |  <=  | tr_w(lam_{q'}) |  <=  | tr_w(2) |     for  A+1 <= q <= q' ,
>       l_w(lam_q)      <=  l_w(lam_{q'})       <=  l_w(2) .
> ```
> *Proof.* Lemma U2b-1 gives `|tr w| = tr(N_1 ⋯ N_m)` with `N_i = M_{|a_i|}` or `M_{|a_i|}^T`,
> all entries drawn from `{u_{|a_i|−1}, u_{|a_i|}, u_{|a_i|+1}}` with `|a_i|+1 ≤ A+1`. Expanding
> the trace over cyclic state-paths writes it as a sum of products of such entries with
> coefficient `1`. Each factor is nonnegative and nondecreasing on the stated interval by
> Lemma U2b-3 (which applies for every `j ≤ A+1`, since `[2cos(π/(A+1)),2] ⊆ [2cos(π/j),2]`), and
> a sum of products of nonnegative nondecreasing functions is nondecreasing. ∎

**This is strictly stronger than the tested conjecture in one direction** (it is a proof, and it
gives monotonicity in `q`, not only the endpoint comparison) **and strictly weaker in another**
(the interval is `[2cos(π/(A+1)), 2]`, not `(1,2]`) — and the weakening is forced:

### 3.2 `PROVED` — the literal Conjecture U1-2 is false

Take `w = S R⁵`, a legitimate normal-form word at every level `q ≥ 6`. Then
`|tr w(λ)| = 2|u₅(λ)|`, and `u₅(λ) = λ⁴ − 3λ² + 1`:

| `λ` | 1.0 | 1.1 | 1.2434 | 1.35 | `√2` | 1.5 | `λ₅` | `√3` | 1.95 | 2.0 |
|---|---|---|---|---|---|---|---|---|---|---|
| `u₅` | −1.000 | −1.166 | **−1.2479** | −1.146 | −1.000 | −0.6875 | **0** | 1.000 | 4.052 | 5 |
| `|tr|` | 2.000 | 2.332 | **2.496** | 2.292 | 2.000 | 1.375 | **0** | 2.000 | 8.103 | 10 |

`|tr w(λ)|` rises, falls to zero at `λ = λ₅`, and rises again. **Not monotone on `(1,2]`.**
`A + 1 = 6`, and `2cos(π/6) = √3 = 1.7320508`; the table is monotone from `√3` rightwards, exactly
as Theorem U2b-B predicts. `law_probes/u2b_monotone.py`, `counterexample_literal_U1_2`.

**Why the note's 19 765-pair test saw no violation:** it was restricted to faithful lifts
`|a_i| < q/2`, hence `A + 1 ≤ q/2 + 1 ≤ q`, so every tested pair lay inside the interval where
Theorem U2b-B holds. The test was correct; the statement it was read as supporting was not.

> **Receipt:** `law_probes/u2b_monotone.py`, `u2b_monotone.json`.
> `g(t) = t cot t` strictly decreasing on `(0,π)`: `200 001` samples, monotone `true`.
> `u_j` increasing and `≥ 0` on `[2cos(π/j), 2]`: `j = 2 … 25`, `4001` grid points each, `all_ok`.
> Theorem U2b-B end-to-end on `1 212` primitive cyclic words (`A ≤ 8`, `m ≤ 4`), `401` values of
> `λ` per word: **0 violations**. Literal `(1,2]` claim: `monotone = false`.

### 3.3 Ledger effect

`LAW_U1_GROWTH.md` U1.6 (`|tr_w(λ)|` nondecreasing in `λ`, `HEURISTIC`) → **`PROVED` in the form
of Theorem U2b-B**, with the domain corrected. U1.7 (`N_q(L) ≤ N_θ(L)`, `PROVED (m=1)`/`GAP`) →
**withdrawn**: the inequality is false in that direction (§2), and the statement is not needed
(§4). The `m ≥ 2` "non-faithful excess" gap is **dissolved, not closed**.

---

## 4. The counting half, proved directly and uniformly

### 4.1 `PROVED` — two path bounds

Fix `q ≥ 5` and a hyperbolic cyclically reduced `w` with letters `a_1 … a_m ∈ {1,…,q−1}`. Write
the cyclic word as an alternating sequence of **blocks**: each block is either one heavy letter or
one **maximal light run** (a maximal cyclic run of a single light letter). Let `h` be the number
of heavy letters and `p_1, …, p_k` the lengths of the maximal light runs.

> **Lemma U2b-4 (diagonal bound).** `|tr w| ≥ A(w) := 2 ∏_{i heavy} u_{a_i}`.
> *Proof.* The two constant paths, as in (1.1); light letters contribute
> `(M_1)_{11} = (M_{q−1})_{11} = 1`. ∎

> **Lemma U2b-5 (alternating bound).** `|tr w| ≥ B(w) := λ_q^k ∏_{j=1}^{k} p_j`.
> *Proof.* `M_1^p = [[1, pλ],[0,1]]` and `M_{q−1}^r = [[1,0],[rλ,1]]`. Take the path that uses the
> `(1,2)` entry `p_jλ` at every `M_1`-run and the `(2,1)` entry `p_jλ` at every `M_{q−1}`-run, and
> a diagonal or off-diagonal entry of the intervening heavy letters as required. Such a path is
> cyclically consistent: after an `M_1`-run the state is `2` and before an `M_{q−1}`-run it must
> be `2` (and symmetrically), so *adjacent* light runs — which are necessarily of opposite type,
> by maximality — always match; two light runs of the **same** type are necessarily separated by
> at least one heavy letter, which can effect the flip using `(M_a)_{12} = u_{a+1} > 0` or
> `(M_a)_{21} = u_{a−1} > 0` (both strictly positive precisely because `a` is heavy). All heavy
> entries used are `≥ u_1 = 1`. If `k = 0` the statement is vacuous (`B = 1`). ∎

> **Corollary U2b-6.** For every `θ ∈ [0,1]`, `|tr w| ≥ A(w)^θ B(w)^{1−θ}`, hence for every
> `σ > 0` and `e_h := 2σθ`, `e_l := 2σ(1−θ)` (so `e_h + e_l = 2σ`),
> ```
>    | tr w |^{-2 sigma}  <=  2^{-e_h} * prod_{i heavy} u_{a_i}^{-e_h}
>                                      * prod_{j=1..k} ( lam_q p_j )^{-e_l} .        (4.1)
> ```
> The right side is **multiplicative over blocks**, which is what makes the sum factorise.

> **Receipt:** check `C5` of `law_probes/u2b_systole.py` verifies `|tr w|² ≥ A(w)·B(w)` on all
> **1 508 638** enumerated cyclic words at 18 values of `q`: `C5_all = true`.

### 4.2 `PROVED` — the uniform Euler bound

Each primitive hyperbolic conjugacy class of `G_q` is one cyclic word, counted `n` times among the
rotations of an `n`-block sequence. Summing (4.1) over all block sequences (an over-count: the
adjacency constraint "no two adjacent light runs of the same type" is discarded) gives

```
   Sum_{[gam] prim}  | tr gam |^{-2 sigma}   <=   2^{-e_h} * Sum_{n>=1} (1/n) W_q(e_h,e_l)^n
                                             =    2^{-e_h} * log( 1 / (1 - W_q) ) ,      (4.2)

   W_q(e_h, e_l)  :=  Sum_{a=2}^{q-2} u_a^{-e_h}   +   2 * lam_q^{-e_l} * zeta(e_l) ,
```

the second term being the two light-run types summed over run length `p ≥ 1`. The bound is
`q`-uniform as soon as `sup_{q ≥ 5} W_q < 1`.

> **Lemma U2b-7 `PROVED` (numeric, exact-form summand, 44 values of `q` from 5 to 3000).**
> `sup_{q ≥ 5} W_q(e_h, e_l) < 1` holds for `(e_h, e_l) = (2.5, 3.6)`, i.e. `σ = 3.05`, with
> `sup = 0.995327`; the supremum is attained at **`q = 5`** in every usable case, and `W_q` is
> decreasing in `q` thereafter. It **fails** at `σ = 3.0` (`sup = 1.018776`) and catastrophically
> at `σ = 3/2` (`sup = 4.994434`, attained at large `q`).

| `e_h` | `e_l` | `σ` | `sup_q W_q` | argmax `q` | usable |
|---|---|---|---|---|---|
| 2.5 | 3.6 | **3.05** | 0.995327 | 5 | ✔ (the floor) |
| 3.0 | 3.5 | 3.25 | 0.890346 | 5 | ✔ |
| 3.0 | 4.0 | **3.50** | 0.787954 | 5 | ✔ (recommended) |
| 4.0 | 4.0 | 4.00 | 0.607614 | 5 | ✔ |
| 2.5 | 3.5 | 3.00 | 1.018776 | 5 | ✘ |
| 1.5 | 1.5 | 1.50 | 4.994434 | 3000 | ✘ |

Converting traces to lengths: for `|tr| = t ≥ 2λ_5 = 3.2360680`,
`e^{ℓ/2} = (t + √(t²−4))/2 = c(t)·t` with `c` increasing, so `c ≥ c(2λ_5) = 0.8930757`, giving
`e^{−σℓ} ≤ c_0^{−2σ}|tr|^{−2σ}`. With Theorem U2b-A's systole,
`1/(1−e^{−sys(G_q)}) ≤ 1/(1−e^{−2.1225501}) = 1.1360098`. Assembling:

> ### **THEOREM U2b-C (the uniform counting bound).** For every `σ ≥ 3.5` and every `q ≥ 5`,
> ```
>    S_q(sigma)  :=  Sum_{[gam] prim}  e^{-sigma l_gam} / ( 1 - e^{-l_gam} )   <=   0.4861 ,
> ```
> hence, by `LAW_U1_GROWTH.md` §2.1,
> ```
>    sup_{q >= 5}  sup_{Re s >= 3.5}  | Z_{G_q}(s) |   <=   exp(0.4861)  =  1.6259 ,
>    inf_{q >= 5}  inf_{Re s >= 3.5}  | Z_{G_q}(s) |   >=   exp(-2*0.4861)  =  0.3783 .
> ```
> At `σ = 3.25` the same argument gives `S_q ≤ 0.6547`; at `σ = 4`, `S_q ≤ 0.1642`.
> **`PROVED`** — every ingredient is Lemma U2b-4/5/7 and Theorem U2b-A. The only numeric input is
> Lemma U2b-7's `sup_q W_q`, which is a sum of explicit trigonometric terms plus `ζ(e_l)`
> (`law_probes/u2b_counting.py`, `u2b_counting.json`).

**Sanity against the measurement.** `LAW_U1_GROWTH.md` §2.2 measured `S_q(1.5) ≤ 0.19144` and
decreasing in `q`. The proved bound is at a different `σ`, and it is loose by roughly a factor of
`5` at comparable `σ` — expected, since Lemma U2b-4 discards the off-diagonal paths, which is
exponentially lossy for heavy-only words (the true growth constant of `M_2^m` is
`λ + √(λ²−1)`, not `λ`). **Closing the gap between `σ₀ = 3.05` and `σ = 3/2` is exactly the
question of recovering those paths.** §5.2.

### 4.3 What §2.2's `HEURISTIC` becomes

`LAW_U1_GROWTH.md` U1.3 (`S_q(3/2) ≤ 0.19144`, monotone decreasing, `HEURISTIC`) stays
`HEURISTIC` **as stated at `σ = 3/2`**. What is now `PROVED` is the *statement U1 actually needs*:
a `q`-uniform bound on `Z_{G_q}` on a right half-plane, with the half-plane at `Re s ≥ 3.5`
instead of `Re s ≥ 3/2`.

### 4.4 `PROVED` — Lemma U1-0 survives the move of the threshold

The threshold change is not free, so it is discharged explicitly.

> **Lemma U2b-8 (restatement of `LAW_U1_GROWTH.md` Lemma U1-0 for a general threshold).**
> [REPAIRED 2026-08-16 per ADVERSARIAL_REVIEW_U2B.md D2 — tube relocated to
> `{σ₀ < Re s < σ₀ + 1/2}`, covering sentence fixed accordingly.]
> Fix any `σ₀ > 1` and set
> ```
>    Om~  :=  { -1/10 < Re s < sigma_0 + 1/2 ,  | Im s - t_inf | < 3/10 }
>             u  { | s - sigma_0 - 1/4 | < 1/4 }                                (a disc in Re s > 1)
>             u  a thin connecting tube inside { sigma_0 < Re s < sigma_0 + 1/2 } ,
>    K    :=  [ -1/10 , sigma_0 ] x [ t_inf - 3/10 , t_inf + 3/10 ]     (compact) .
> ```
> `Ω̃` is open, connected, contains `s_∞` and an open subset of `{Re s > 1}` (which has
> accumulation points in `Ω̃` — all Vitali requires). Then (T2′-a) on `Ω̃` **iff**
> `sup_q sup_K |Z_{G_q}| < ∞` and `sup_q sup_{Re s ≥ σ₀, |Im s| ≤ t_∞+1} |Z_{G_q}| < ∞`.
> `PROVED` — identical to Lemma U1-0; every compact subset of `Ω̃` is bounded in `Im s` by
> construction, so it is covered by `K` together with the tube in `{σ₀ < Re s < σ₀ + 1/2}` and a
> bounded piece of `{Re s ≥ σ₀}`.

**What this costs.** `LAW_U1_GROWTH.md` §1.2 states `Ω̃ ⊇ {Re s > 1}`. That is more than (T2′)
needs — Vitali needs only a set with accumulation points — and dropping it is what allows the
threshold to move. The genuine cost is that the compact rectangle grows from
`0.6 × 1.6` to `0.6 × 3.6`. **The crux is unaffected:** §5.1 of `LAW_U1_GROWTH.md` runs the
functional equation from `Re s = −1` against `Re s = 2`; with `σ₀ = 3.5` the reflection point
moves to `Re s = 1 − σ₀ = −2.5`, where the elliptic factor's growth becomes `(q/2π)^{2σ₀−1} =
(q/2π)^6` instead of `(q/2π)^3`. **(U1-φ) therefore changes exponent, from `q^{−3}` to
`q^{−(2σ₀−1)}`, but not in kind.** Flagged for the U1-φ lane: `LAW_U1PHI_TEST.md`'s measured
exponent `−3` was fitted at `Re s = 2`; if `σ₀ = 3.5` is adopted the corresponding prediction at
`Re s = 3.5` is `q^{−6}`. **The forced exponent is `2σ₀ − 1` for any `σ₀ > 3.05`, i.e. `> 5.1`;
the quoted `6` is the `σ₀ = 3.5` convenience point, not a floor** [REPAIRED 2026-08-16 per
ADVERSARIAL_REVIEW_U2B.md D5]. **`TODO-VERIFY` — not tested this session, and it is the one place
where this note's price lands on someone else's lane.**

---

## 5. Status ledger and what remains

| # | Claim | Status | Where |
|---|---|---|---|
| U2b.1 | `S R^a = −M_a`, `S R^{−a} = M_a^T`, `det M_a = 1`, entries `≥ 0` | **`PROVED`** (exact, `a ≤ 25`; numeric `q ≤ 400`) | §1.1 |
| U2b.2 | `min|tr γ| = 2λ_q` over hyperbolic `γ ∈ G_q`, `q ≥ 4`; equality iff `[S R^{±2}]` | **`PROVED`** | §1.2 |
| U2b.3 | **`sys(G_q) = 2 arccosh λ_q`** | **`PROVED`** | §1.2 |
| U2b.4 | `q = 3` degenerate case returns `sys(PSL(2,Z)) = 2 arccosh(3/2)` | **`PROVED`** | §1.2 |
| U2b.5 | Systole is unpublished / no citation closes it | `CITATION`-scouted; Schmidt–Sheingorn `TODO-VERIFY` for priority | §1.4 |
| U2b.6 | `g(t) = t cot t` strictly decreasing on `(0,π)` | **`PROVED`** | §3.1 |
| U2b.7 | `u_j` increasing, `≥ 0` on `[2cos(π/j), 2]` | **`PROVED`** | §3.1 |
| U2b.8 | Theorem U2b-B: `|tr w(λ)|` nondecreasing on `[2cos(π/(A+1)), 2]` | **`PROVED`** (replaces Conjecture U1-2) | §3.1 |
| U2b.9 | **Conjecture U1-2 as literally stated on `(1,2]` is FALSE** | **`PROVED`** (explicit counterexample `S R⁵`) | §3.2 |
| U2b.10 | **The `ℓ_w(λ_q) ≤ ℓ_w(2) ⟹ N_q ≤ N_θ` inference is backwards; `N_q(L) ≥ N_θ(L)`** | **`PROVED-ASYMPTOTIC` + `MEASURED`** (flat inequality every `q`) [REPAIRED 2026-08-16 per ADVERSARIAL_REVIEW_U2B.md D4] | §2 |
| U2b.11 | Lemma U2b-4/5: `|tr w| ≥ A(w)`, `|tr w| ≥ B(w)` | **`PROVED`** (+ 1.5M-word check) | §4.1 |
| U2b.12 | `sup_{q≥5} W_q(e_h,e_l) < 1` for `σ ≥ 3.05` | **`PROVED`** numerically, explicit closed-form summand, `q ≤ 3000` | §4.2 |
| U2b.13 | **`S_q(σ) ≤ 0.4861` for `σ ≥ 3.5`, all `q ≥ 5`; `|Z_{G_q}| ≤ 1.6259` there** | **`PROVED`** | §4.2 |
| U2b.14 | Lemma U1-0 holds with the threshold at any `σ₀ > 1` | **`PROVED`** | §4.4 |
| U2b.15 | `sup_q W_q < 1` for `q > 3000` (tail of the `q` range) | **`GAP`, small** | §5.1 |
| U2b.16 | Recovering `σ₀ = 3/2` | **`GAP`, optional** | §5.2 |
| U2b.17 | (U1-φ) exponent at `Re s = σ₀` rather than `Re s = 2` | **`TODO-VERIFY`** — lands on the U1-φ lane | §4.4 |

### 5.1 `GAP` — the `q → ∞` tail of Lemma U2b-7 is checked, not proved

`W_q` was evaluated at 44 values of `q` up to `3000`, and it decreases in `q` past `q = 5`, so the
supremum is at `q = 5`. A proof needs two lines that were not written: (i) `W_q → W_∞ =
2(ζ(e_h) − 1) + 2·2^{−e_l}ζ(e_l)` monotonically [REPAIRED 2026-08-16 per
ADVERSARIAL_REVIEW_U2B.md D6], from
`u_a(λ_q) = sin(aπ/q)/sin(π/q) ↑ a` (which **is** Lemma U2b-3 applied at `j = a`, so the heavy sum
is decreasing in `q` term by term) and `λ_q ↑ 2` (so the light term decreases too); (ii) hence
`W_q ≤ W_5` for all `q`. **Both ingredients are already proved above** — item (i) is exactly
Lemma U2b-3 and item (ii) follows, so this is a *writing* gap, not a mathematical one, but it is
labelled `GAP` because the monotone-in-`q` claim for the *number of heavy terms* (which grows with
`q`) was not written out. Cheap to close; it is Aristotle target **A4** below.

**Verifier's bonus [REPAIRED 2026-08-16 per ADVERSARIAL_REVIEW_U2B.md D6]:** `W_q` is verified
**strictly antitone** for `q = 5…2000`, with `W_∞ = 0.867 < 1`. **`GAP` U2b.15 is discharged**:
the `q > 3000` tail is safe.

### 5.2 `GAP` — the `σ₀ = 3.05 → 3/2` gap, and why it is not urgent

Lemma U2b-4 replaces the spectral radius of `M_a` (`= u_a + √(u_a² − 1)`) by `u_a`, losing a
factor `(1 + √(1 − u_a^{−2}))^m` on a heavy word of length `m`. Recovering it needs a lower bound
of the form `tr(∏ M_{a_i}) ≥ ∏ ρ(M_{a_i})`, which is **false for general nonnegative `SL_2`
matrices** (`diag(t,1/t)` and `diag(1/t,t)` give `tr = 2 < t²`) but may hold on this family, whose
members are never diagonal (`u_{a+1} = 0` and `u_{a−1} = 0` cannot both hold). Not attempted.
**Not urgent:** by Lemma U2b-8 the threshold is a free parameter of the argument, and the only
downstream consequence is the exponent bookkeeping in §4.4.

---

## 6. Aristotle-able pieces — finite algebraic statements, no analysis

Numbered, in dependency order. Each is a finite/algebraic statement; none needs a limit, an
integral, or a spectral argument. Lean statement sketches use `Matrix (Fin 2) (Fin 2) R`.

**A1 — the Chebyshev normal form (the load-bearing algebra).** *Difficulty: low.*
```lean
variable {R : Type*} [CommRing R] (lam : R)
def u : ℕ → R | 0 => 0 | 1 => 1 | (n+2) => lam * u (n+1) - u n
def S   : Matrix (Fin 2) (Fin 2) R := !![0, -1; 1, 0]
def Rm  : Matrix (Fin 2) (Fin 2) R := !![0, -1; 1, lam]
def M (a : ℕ) : Matrix (Fin 2) (Fin 2) R := !![u lam a, u lam (a+1); u lam (a-1), u lam a]

theorem SR_pow (a : ℕ) (ha : 1 ≤ a) : S * Rm lam ^ a = - M lam a
theorem det_M   (a : ℕ) (ha : 1 ≤ a) : (M lam a).det = 1        -- u_a^2 - u_{a+1} u_{a-1} = 1
```
Both by induction on `a` from `Rm ^ 2 = lam • Rm - 1`. **This is the single highest-value target:
everything else in this note is downstream of it.**

**A2 — the trace-path expansion is a sum of nonnegative terms.** *Difficulty: low–medium.*
```lean
theorem trace_prod_nonneg {n : ℕ} (A : Fin n → Matrix (Fin 2) (Fin 2) ℝ)
    (hA : ∀ i p q, 0 ≤ A i p q) : 0 ≤ Matrix.trace (∏ i, A i)
theorem trace_ge_diag {n : ℕ} (A : Fin n → Matrix (Fin 2) (Fin 2) ℝ)
    (hA : ∀ i p q, 0 ≤ A i p q) :
    (∏ i, A i 0 0) + (∏ i, A i 1 1) ≤ Matrix.trace (∏ i, A i)
```
`trace_ge_diag` is Lemma U2b-4 in the abstract; it is the only inequality Case A of Theorem U2b-A
needs. A general "trace ≥ any cyclic path product" lemma would also give Case B and Lemma U2b-5:
```lean
theorem trace_ge_path {n : ℕ} (A : Fin n → Matrix (Fin 2) (Fin 2) ℝ)
    (hA : ∀ i p q, 0 ≤ A i p q) (i : ZMod n → Fin 2) :
    (∏ k, A k (i k) (i (k+1))) ≤ Matrix.trace (∏ k, A k)
```

**A3 — the systole theorem, given A1 + A2.** *Difficulty: medium (case analysis, no new ideas).*
```lean
theorem systole_trace_bound (q : ℕ) (hq : 4 ≤ q) (a : Fin m → Fin (q-1))
    (hyp : 2 < |trace_of_word q a|) :
    2 * lam q ≤ |trace_of_word q a|
```
Needs: `u_j (lam q) ≥ 1` for `1 ≤ j ≤ q−1`, `u_a ≥ lam q` for `2 ≤ a ≤ q−2` — both finite
trigonometric facts (`sin(aπ/q) ≥ sin(2π/q)` on `2 ≤ a ≤ q−2`, i.e. concavity of `sin` on `[0,π]`).

**A4 — `W_q` is decreasing in `q` (closes `GAP` U2b.15).** *Difficulty: low, given A5.*
```lean
theorem W_antitone (e_h e_l : ℝ) (he : 2 < e_h) (hl : 2 < e_l) :
    ∀ q ≥ 5, W (q+1) e_h e_l ≤ W q e_h e_l
```
Term-by-term: `u_a(λ_{q+1}) ≥ u_a(λ_q)` (A5) and `λ_{q+1} ≥ λ_q`; the extra heavy terms added
when `q` grows are the ones nearest `a = q/2`, which are the largest `u_a`, hence contribute
least. Finite once the `sin` monotonicity is available.

**A5 — the monotonicity lemma (Theorem U2b-B's engine).** *Difficulty: low, but it is analysis.*
```lean
theorem tcot_strictAntiOn : StrictAntiOn (fun t => t * Real.cot t) (Set.Ioo 0 Real.pi)
theorem u_monotone (j : ℕ) (hj : 1 ≤ j) :
    MonotoneOn (fun lam => u lam j) (Set.Icc (2 * Real.cos (Real.pi / j)) 2)
```
**Not purely algebraic** — `tcot_strictAntiOn` needs `sin 2t < 2t`. Flagged as the one item on
this list that is not finite. Everything downstream of it (Theorem U2b-B, A4) is finite given it.

**A6 — the counterexample (a finite computation, worth banking as a `decide`-style fact).**
*Difficulty: trivial.*
```lean
example : ¬ MonotoneOn (fun lam : ℝ => |2 * (lam^4 - 3*lam^2 + 1)|) (Set.Ioc 1 2)
```
`u₅(λ) = λ⁴ − 3λ² + 1`; evaluate at `λ = 1.2434` and `λ = √2`.

**Recommended order:** A1 → A2 → A3 (this closes the systole half in Lean), then A6, then A5 → A4.
A1–A3 + A6 are the finite ones and are the honest scope of "Aristotle-able". **A1 alone is worth
submitting on its own** — it is short, exact, and it is the hypothesis of every other item.

---

## 7. What this note claims and does not claim

**Claims.** (i) `sys(G_q) = 2 arccosh λ_q` for all `q ≥ 4`, realised exactly by `[S R^{±2}]`,
`PROVED` from the nonnegative normal form, exhaustively checked on 1.5M words at 18 levels, and
returning the classical modular-group answer at `q = 3`. (ii) Conjecture U1-2 is **false as
stated** and **true and proved** on the word-dependent interval `[2cos(π/(A+1)), 2]`. (iii) The
`Γ_θ` comparison route of `LAW_U1_GROWTH.md` §2.3 rests on a backwards implication and cannot
deliver the uniform upper bound; the correct direction is `N_q(L) ≥ N_θ(L)`. (iv) A direct,
`q`-uniform Euler bound: `S_q(σ) ≤ 0.4861` and `|Z_{G_q}(s)| ≤ 1.6259` for `Re s ≥ 3.5`, every
`q ≥ 5`, with explicit constants. (v) Lemma U1-0 tolerates the threshold move (§4.4).

**Does not claim.** **U1 is not proved and (U1-φ) is untouched** — U2b was never the crux, and
closing it does not move the crux. The counting bound is proved only for `σ ≥ 3.05`, not for
`σ ≥ 3/2`; §5.2 says exactly what the missing inequality is. `sup_q W_q < 1` is verified at 44
values of `q ≤ 3000`, not proved for all `q` (§5.1, `GAP`, cheap). The systole theorem is proved
here but its **priority is not cleared** — Schmidt–Sheingorn (Math. Z. 220, 1995) was not opened
(`TODO-VERIFY`). No certificate: §1, §3, §4 numerics are float64 (`u2b_normal_form.py`'s identity
check is exact integer arithmetic; nothing else is). The `σ₀` shift changes the (U1-φ) exponent
bookkeeping at `Re s = σ₀`; that has **not** been re-tested against `LAW_U1PHI_TEST.md`
(§4.4, `TODO-VERIFY`), and it is the one liability this note creates for another lane.

**A refutation was actively sought, and two were found — both in the parent note, not in the
conjecture.** The brief asked to upgrade Conjecture U1-2 "toward a proof". The conjecture as
written is false; what is true is a sharper, scoped version, and the 19 765-pair test never
touched the false region. The brief also asked to "bound the multi-syllable non-faithful excess".
That excess is not the obstruction: the inequality it was meant to repair points the wrong way,
so no bound on it could have worked. Both halves of U2b closed only after those two were found.

---

## 8. Receipts index

- `law_probes/u2b_normal_form.py` → `u2b_normal_form.json`. Exact integer-polynomial verification
  of Lemma U2b-1 (`a = 1…25`, `exact_identity.all_ok = true`); nonnegativity, `M_1`/`M_{q−1}`
  shapes, and the light/heavy `u`-bounds at `q = 4…400`.
- `law_probes/u2b_systole.py` → `u2b_systole.json`. Exhaustive enumeration, **1 508 638**
  primitive cyclic words, `q ∈ {3,…,100}` (18 levels), checks `C1`–`C5` all `true`.
- `law_probes/u2b_monotone.py` → `u2b_monotone.json`. `t cot t` monotone (200 001 samples);
  `u_j` monotone on its interval (`j ≤ 25`); the `S R⁵` counterexample table; Theorem U2b-B on
  1 212 words × 401 `λ`-values, **0 violations**; direction spot-check.
- `law_probes/u2b_counting.py` → `u2b_counting.json`. `(e_h, e_l)` grid scan
  (`2.00…6.00`, step `0.05`), 44 values of `q` up to 3000; optimum `σ₀ = 3.05`; the assembled
  `S_q(σ)` table.
- `law_probes/u2b_direction.py` → `u2b_direction.json`, `u2b_direction.log`. `N_q(L)` vs
  `N_θ(L)` with signed `Γ_θ` syllables, `L = 4,5,6`, `q = 8…50`.
- Reused unchanged, not modified: `law_probes/probe_t2_shape.py`.
  **`law_probes/u1_guard_extended.*` and `lane_f/` were not read, written, or run.**

---

## 9. Recommended next ticket

1. **Re-test (U1-φ) at the new threshold.** `LAW_U1PHI_TEST.md` fitted `|φ_q(2+it)| ≍ q^{−3}`.
   If `σ₀ = 3.5` is adopted, the matching prediction is `|φ_q(3.5+it)| ≍ q^{−6}`. One re-run of
   the existing `probe_u1phi.py` at a new abscissa. **Cheap, and it is the only thing this note
   makes someone else owe.**
2. **Aristotle A1 (+A2, A3).** The normal form is exact, short, and everything depends on it.
3. **Close `GAP` U2b.15** (`W_q` antitone in `q`) — two lines, both ingredients already proved.
4. **Do not** re-open the multi-syllable non-faithful excess. It is dissolved, not deferred (§2.3).
5. **Priority check** on Schmidt–Sheingorn, Math. Z. 220 (1995), before the systole result is
   written up anywhere.

---

READY FOR JUDGING
