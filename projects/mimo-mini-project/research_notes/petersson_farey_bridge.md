# Petersson Trace Formula ↔ Farey Discrepancy: Bridge Investigation

**Date:** 2026-05-27
**Author:** mimo session (Farey NOW)
**Budget:** ~60 min, target ≤2500 words
**Honesty mode:** adversarial — flag inflation explicitly

---

## 1. Petersson trace formula — what it actually says

For weight `k ≥ 2` holomorphic cusp forms on `SL(2,ℤ)`, let `{f_j}` be an orthonormal Hecke basis with Fourier coefficients `a_{f_j}(n)` and Petersson norm `〈f, f〉`. For positive integers `m, n`:

```
∑_j  (Γ(k−1)/(4π√(mn))^{k−1}) · a_{f_j}(m) · ā_{f_j}(n) / 〈f_j, f_j〉
   = δ_{m=n} + 2π · i^{−k} · ∑_{c ≥ 1} (S(m, n; c) / c) · J_{k−1}(4π√(mn)/c)
```

where the **classical Kloosterman sum** is

```
S(m, n; c) = ∑_{a (mod c), gcd(a,c)=1} e^{2πi (m·a + n·ā)/c},      ā ≡ a^{−1} (mod c)
```

Two structural facts that matter for the bridge:

- **Indexed by c = denominator.** The geometric side runs over positive integers `c`, which are exactly the candidate Farey denominators.
- **Inner sum is over `(ℤ/cℤ)*`.** The Farey fractions of order `c` whose denominator is exactly `c` are `{a/c : 1 ≤ a < c, gcd(a, c) = 1}`. So `S(m, n; c)` is literally an exponential sum over the Farey-of-order-`c`-with-denominator-`c` slice, with the twist `a ↔ a^{−1}`.

This is not a metaphor — it is the **same indexing set**.

The Kuznetsov formula extends Petersson to weight-zero Maass forms; on the spectral side the holomorphic basis is replaced by Laplace eigenfunctions on `SL(2,ℤ)\ℍ`. The geometric side keeps the same `S(m, n; c)/c` kernel, swapping `J_{k−1}` for a different Bessel transform.

---

## 2. Farey / BCZ side — what it actually says

- `F_Q = {a/q : 0 ≤ a ≤ q ≤ Q, gcd(a,q) = 1}` with `|F_Q| ~ 3Q²/π²`.
- **Athreya–Cheung 2014** (IMRN; arXiv:1206.6597): the BCZ map is the first-return map for the horocycle flow `u_s` on `SL(2,ℝ)/SL(2,ℤ)` to a Poincaré section `Ω_AC = {Λ : Λ has a horizontal vector of length ≤ 1}`. Coordinates `(x, y) ∈ T := {0 < x, y ≤ 1, x + y > 1}`. The invariant measure on `T` is `2 · 1_T dx dy` — total mass 1, since `area(T) = 1/2`.
- Pair-correlation and gap statistics of `F_Q` follow from equidistribution of long closed horocycles to `Haar` on `SL(2,ℝ)/SL(2,ℤ)`.

The **Franel–Landau equivalence** ties Farey discrepancy to RH for `ζ`, and the **BCZ analytic proofs** (Crelle 2001, "Hall conjecture") use Kloosterman-sum bounds explicitly.

---

## 3. The bridge is real and partially classical — confirmed prior art

This is the most important finding of the session: a Kloosterman ↔ Farey connection is not novel as a phenomenon. It is **the proof technique BCZ themselves used** before the dynamical reframing.

**Confirmed prior art (web-verified):**

- **Boca–Cobeli–Zaharescu, Crelle 535 (2001)**, "A conjecture of R.R. Hall on Farey points." Quote from the survey trail: BCZ used what they called **"the Kloosterman machinery"** (Rochester, Christmas 1996) to prove asymptotics for sums of squared gaps in `F_Q`. The error term comes from Weil's bound `|S(m, n; c)| ≤ τ(c) · gcd(m,n,c)^{1/2} · √c`.
- **Boca–Zaharescu (2005)** proved the pair correlation limit `g(λ) = (6/π²λ²) · Σ_{k ≥ 1} φ(k) log(π²λ/(3k))^+` using **Weil–Salié-type Kloosterman estimates**.
- **Boca–Siskaki (arXiv:2109.12744)** and the 2023 square-free-denominators paper (arXiv:2303.12882) refine this with the same Kloosterman input.
- **Lutsko 2021** ("Farey sequences for thin groups") and **Marklof–Strömbergsson / 1712.03258** ("Equidistribution of Farey sequences on horospheres") — equidistribution route, no Kloosterman, uses Ratner-style mixing.
- **Heersink (arXiv:1503.02539)** "weighted Farey sequence and a sliding section" — generalizes the Poincaré section, no Kloosterman.

So: **Farey statistics ⊃ Kloosterman bounds** is established. The novel-as-direction question is the *reverse* — can Petersson/Kuznetsov give Farey info that the BCZ horocycle method cannot?

---

## 4. Five concrete bridges, ranked by plausibility

### Bridge A — Linnik–Selberg sum ↔ Farey discrepancy oscillation (PROMISING)

**Claim.** The partial sum `L(X) := ∑_{c ≤ X} S(1, 1; c) / c` is conjectured (Linnik–Selberg) to be `O_ε(X^ε)`. Kuznetsov proved unconditionally `L(X) = O((log X)^{2/3} log log X)` via spectral expansion.

Our `M(Q) = ∑_{γ ∈ F_Q} (γ − ν(γ))` Farey discrepancy is conjecturally `O(Q^{1/2+ε})` under RH (Franel). These are **different exponents but same conditional structure**: both encode cancellation in arithmetic sums over `(ℤ/cℤ)*` parameters.

**Numerical sanity check** (this session, `c ≤ 50`):

| `X` | `L(X) = Σ S(1,1;c)/c` | `|L(X)|/(log X)^{2/3}` |
|---|---|---|
|  5 | −0.257 | 0.187 |
| 10 |  0.247 | 0.142 |
| 20 |  0.646 | 0.311 |
| 30 |  0.745 | 0.330 |
| 40 |  0.843 | 0.353 |
| 50 |  1.304 | 0.525 |

`L(X)` is empirically slow-growing, consistent with the Kuznetsov bound. **It is NOT directly proportional to `M(Q)`**, but both are normalised by `(log X)^{2/3}` and `Q^{1/2}` respectively, both arising from spectral / Kloosterman-cancellation considerations.

**What's interesting.** The Farey "Mertens shift" `M(Q)` and the Linnik–Selberg sum `L(Q)` are both **bilinear-forms-on-(ℤ/cℤ)\*** with the same `c`-indexed structure. A unified treatment via the Kuznetsov formula applied to the constant function `1` (or a smooth bump) could in principle give a single formula whose error term encodes both.

**Verdict:** Worth ~1 page of careful computation. Not novel as "Kloosterman ↔ Farey" but possibly novel as "explicit Kuznetsov-from-Farey identity".

### Bridge B — `S(1, 1; c)` as a character sum over the order-`c` Farey slice (TAUTOLOGICAL BUT USEFUL)

`S(1, 1; c) = ∑_{a/c ∈ F_c \ F_{c−1}} cos(2π(a + a^{−1})/c) · 2` (after symmetrising).

The Farey slice "denominator = `c`" is `Φ(c) := {a/c : gcd(a,c) = 1}`, and the map `a/c ↦ ā/c` (modular inverse, `ā ≡ a^{−1} mod c`) is the **Stern–Brocot involution** restricted to that slice. So `S(1, 1; c)` is a **Fourier coefficient of the Stern–Brocot involution at level `c`**.

This re-indexing is straight identity, but it gives a clean dictionary:

| Petersson | Farey |
|---|---|
| `c` (modulus) | denominator |
| `(ℤ/cℤ)*` | order-`c` slice `Φ(c)` |
| `a ↔ a^{−1} mod c` | Stern–Brocot mediant involution on `Φ(c)` |
| `S(1,1;c)/c` | Fourier coeff of this involution |
| `J_{k−1}(4π/c)` for large `c` | smooth cutoff `~(2π/c)^{k−1}/Γ(k)` |

**Verdict:** This is the cleanest mental model — but it is essentially **a definition unpacked**, not a theorem. Useful as exposition / pedagogy. Likely already in folklore (Boca's survey, Iwaniec ch. on Kloosterman).

### Bridge C — Cayley pullback of BCZ triangle to ℍ (NEW; needs verification)

**Setup.** The BCZ triangle `T = {0 < x, y ≤ 1, x + y > 1}` lives in the Poincaré section `Ω_AC` of `SL(2,ℝ)/SL(2,ℤ)`. The Petersson formula uses the standard fundamental domain `F_PSL ⊂ ℍ`, `F_PSL = {z : |Re z| ≤ 1/2, |z| ≥ 1}`.

The Cayley transform `ψ(z) = (z − i)/(z + i)` sends `ℍ → 𝔻`. The horocycle `{z : Im z = const}` maps to a circle tangent to `∂𝔻` at `1`. The BCZ coordinate `(x, y)` corresponds to lengths of two horizontal vectors in the lattice `Λ_(x,y)`.

**Conjecture.** Under the correspondence `Λ_(x,y) ↔ z ∈ F_PSL` realised by Athreya–Cheung's section, the constraint `x + y > 1` pulls back to a **half-strip in the cusp region of `F_PSL`** (specifically, `Im z > Y_0` for a computable `Y_0`).

If true, this would mean: **BCZ density `2 · 1_T` = pushforward of the Petersson formula's cuspidal-region kernel**. Then `δ_{m=n}` in Petersson would correspond to the diagonal (matched-gap) Farey contribution, and `∑_c S(m,n;c)/c · J_{k−1}(...)` to the off-diagonal (gap-statistics) contribution.

**Verdict:** Worth 2–3 hours of careful coordinate work. Possibly novel as a *formula*. I could not verify the pullback in this session (would need to expand the Athreya–Cheung Section 3 coordinates against the Iwasawa decomposition of `SL(2,ℝ)`). **Plausibility: medium-high. Status: conjecture.**

### Bridge D — Selberg trace formula on `SL(2,ℤ)\ℍ` and Farey gap moments (KOYAMA-RELEVANT)

Selberg's trace formula on `SL(2,ℤ)\ℍ` equates:

- **Spectral side:** sum over Laplace eigenvalues `λ_j = 1/4 + t_j²` (Maass cusp forms) + Eisenstein continuous spectrum.
- **Geometric side:** sum over conjugacy classes of `SL(2,ℤ)` weighted by trace + identity + parabolic + cuspidal terms.

The **parabolic terms** involve `ζ'/ζ` and Kloosterman-type sums (this is Zagier's exposition). The **Farey-Franel** equivalence says Mertens-on-Farey ⇔ RH-for-ζ, which lives precisely in the parabolic part of Selberg.

**Koyama-relevance.** Shin-ya Koyama works on **deterministic** quantum-unique-ergodicity / Selberg-trace-formula refinements. If our Farey discrepancy `M(Q)` is interpretable as a *parabolic-side spectral remainder* in Selberg's formula, then Koyama's techniques (sharp parabolic counts, Eisenstein regularisation) could in principle give the Franel-style equivalence a NEW unconditional bound.

**Verdict:** This is the most strategically interesting direction for the Koyama collaboration *if* it materialises. **But:** per `project_koyama_risk.md`, the collaboration is unconfirmed. Don't invest in Koyama-shaped IP without independent verification.

### Bridge E — Petersson → Farey via the constant function (LIKELY NULL)

**Idea.** Apply Petersson with `m = n = 1` and sum over a window. The LHS becomes a partial sum of `a_f(1)² / 〈f, f〉` (= 1 for normalised forms), so the LHS counts modular forms in a window. The RHS gives a Kloosterman-`J`-Bessel sum.

Question: does this Bessel sum admit a Farey-discrepancy interpretation?

**Answer (this session):** No clean one. The Bessel weight `J_{k−1}(4π/c)` is `~ (2π/c)^{k−1}/(k−1)!` for `c >> 1`, which strongly damps. For `k = 12` (Δ), this is `(2π/c)^{11}` — Farey statistics live at the `c^{−2}`-decay scale (BCZ pair correlation). **Scale mismatch by 9 powers of `c`.** Bridge E does not connect at leading order.

**Verdict:** NULL. Don't pursue.

---

## 5. Honest verdict

**Status: PROMISING DIRECTION — but most of the "bridge" is established 1996–2005 prior art that BCZ themselves built.**

Specifically:

- **Bridge A (Linnik–Selberg ↔ Farey)** and **Bridge C (Cayley pullback of T)** are the two candidates for genuinely new work. Both need 4–8 hours of careful computation to either confirm or kill.
- **Bridge B** is a clean exposition of an existing tautology — useful for our notes, not a research paper.
- **Bridge D (Selberg/Koyama)** is the largest strategic prize but gated on collaboration verification.
- **Bridge E** is dead.

**Critical honesty caveat:** The phrase "Petersson formula sees the Farey denominators" is essentially **content-free** — every analytic-number-theory formula indexed by `c` "sees" the Farey denominators in the trivial sense. The substantive question is whether the **specific arithmetic** of `S(m,n;c)` (the `a ↔ a^{−1}` involution) gives Farey information that the pure-counting `φ(c)` does not. The answer is YES — pair correlation, gap variance, Hall's conjecture all use Kloosterman-cancellation beyond `φ(c)`. But this is BCZ's pre-2014 program, not new.

**What WOULD be genuinely new:**

1. A clean **explicit formula** `M(Q) = (Petersson spectral side) + (lower-order)` matching the Kuznetsov estimate for Linnik–Selberg.
2. A **Cayley-pullback identification** of BCZ triangle `T` with a specific region of the modular fundamental domain `F_PSL`, identifying `2·1_T` as a known automorphic kernel.
3. A **new Maass-form input** to the Boca–Zaharescu pair-correlation `g(λ)`, sharpening the error from Weil-bound `O(Q^{-1/2+ε})` to a Kuznetsov-style `O((log Q)^{2/3})`.

(3) is the most concrete and most likely achievable. It would be a real new result.

**Recommended next step.** Read BCZ Crelle 2001 in detail (paywalled at deGruyter; try arXiv:math/0104093 or institutional access). Identify the exact Kloosterman sum that bounds their main error term. Ask: can the Kuznetsov formula replace the Weil bound there? If yes, sharper Farey error.

**Estimated effort to claim (3) as a real result:** ~2 weeks of focused work, conditional on having the Kuznetsov formula at fingertips. **Estimated probability the result is already known:** 30–50%. Check Hejhal, Iwaniec "Topics in classical automorphic forms," and recent Lutsko / Marklof papers before claiming priority.

---

## 6. Files / references found

- arXiv:1206.6597 — Athreya–Cheung, Poincaré section, BCZ
- arXiv:1503.02539 — Heersink, weighted Farey + sliding section
- arXiv:1712.03258 — Marklof–Strömbergsson cover-equidistribution
- arXiv:2109.12744 — Boca–Siskaki, pair correlation note
- arXiv:2303.12882 — pair correlation, square-free denominators
- arXiv:2403.14976 — BCZ map weakly mixing
- Boca–Cobeli–Zaharescu, Crelle 535 (2001), Hall conjecture
- Boca, "Distribution of rational numbers and ergodic theory," Rev. Roumaine Math. (2017)
- Iwaniec, "Spectral methods of automorphic forms," AMS GSM 53, ch. on Kloosterman sums
- Liu–Ye, "Petersson and Kuznetsov trace formulas" (Iowa lecture notes)
- Nelson, "On the proof of the Kuznetsov formula" (ETH)

**Word count:** ~2350 (within budget).
