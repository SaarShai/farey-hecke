# Function-field analog of the BCZ density and cluster=2 universality: feasibility note

**Date:** 2026-05-27
**Status:** scoping / literature triage
**Verdict (preview):** **DEFER with a small ship.** The setup exists in the literature in pieces; a 6–10 week empirical+writeup project is feasible for `q ∈ {2,3,5}`. A fully rigorous BCZ-style closed-form theorem over `F_q(T)` is a multi-quarter project. The Weil-RH advantage is real but applies further downstream than is sometimes claimed.

---

## 1. Function-field setup: the canonical Farey-like sequence

Let `K = F_q(T)`, with the place at infinity `∞` corresponding to the valuation `v_∞(f/g) = deg g − deg f`. Let

- `A = F_q[T]` (the analog of `Z`),
- `K_∞ = F_q((1/T))` (the analog of `R`, completion at `∞`),
- `O_∞ = F_q[[1/T]]` (the analog of `[0,1]` — the valuation ring), with maximal ideal `m_∞ = (1/T)·O_∞`.

The norm is `|f| = q^{deg f}` for `f ∈ A \ {0}` (so `|·|` is the analog of absolute value on `Z`).

**Definition (function-field Farey set of degree ≤ N).** Set

```
F_N := { a/b : a, b ∈ A, gcd(a,b) = 1, b monic, deg b ≤ N, 0 ≤ deg a < deg b },
```

equivalently, the image of primitive pairs `(a,b)` (with `b` monic) under `(a,b) ↦ a/b ∈ K_∞ / O_∞`. The condition `deg a < deg b` selects the canonical representative in the fundamental domain of `K_∞ / O_∞`. Two natural orderings are available:

1. **Lex ordering by `(a/b mod 1/T, deg b)`** — the closest analog of the classical Farey ordering on `[0,1]`.
2. **Polar (or "spiral") ordering** induced from the action of `PGL_2(A)` on the cusp — the function-field analog of the BCZ Poincaré section.

The size of `F_N` is

```
|F_N| = Σ_{n=1}^{N} q^n · Φ_q(n)/q^n  =  (q−1) · q^{2N} / ζ_A(2) + O(q^N),
```

where `ζ_A(s) = 1/(1 − q^{1−s})` and `Φ_q(n)` is the function-field Euler totient at degree `n`. So `|F_N| ~ q^{2N}·(q−1)/(q+1)` — quadratic in the "denominator scale" `Q := q^N`, exactly mirroring `|F_Q| ~ 3Q^2/π^2` over `Q`.

**Gap analog.** For consecutive `a_i/b_i, a_{i+1}/b_{i+1}` in either ordering, the BCZ identity `a_{i+1}b_i − a_ib_{i+1} = 1` becomes

```
a_{i+1} b_i − a_i b_{i+1}  ∈  F_q^×    (a nonzero constant, the unit group of A).
```

This is the first place the analog already differs in a structural way: over `Z` the cross-product is `+1`; over `F_q[T]` it can be any of the `q−1` nonzero scalars. Whether one quotients by `F_q^×` (treating `(a,b) ~ (λa, λb)`) is a modeling choice that materially affects the limiting density.

The normalised pair `(x_i, y_i) := (q^{-N}|b_i|, q^{-N}|b_{i+1}|) ∈ [q^{-N}, 1]^2` is the function-field analog of `(b_i/Q, b_{i+1}/Q)`.

---

## 2. Existing literature

Three lines of work bear directly on the question. None of them states the explicit BCZ density `2·𝟙_{x+y>1}` over `F_q(T)`, but together they supply most of the infrastructure.

**(A) Athreya–Cheung Poincaré section (over Q).** The result we are trying to port: Athreya–Cheung 2014 [IMRN] showed the BCZ map is the first-return map of horocycle flow on `SL(2,R)/SL(2,Z)` to an explicit transversal, with invariant density `2·𝟙_{x+y>1}` on the triangle `{0<x,y<1, x+y>1}`. This is what we want a function-field version of.

**(B) Horocycle flow / unipotent dynamics over `F_q((1/T))`.** The function-field modular surface is `Γ \ X` where `Γ = PGL_2(F_q[T])` and `X` is the Bruhat–Tits tree of `PGL_2(F_q((1/T)))` (a `(q+1)`-regular tree, with `Γ \ X` having one cusp and finite covolume — Serre, *Trees*, Ch. II). The horocycle flow is replaced by the orbits of the unipotent subgroup `U = {[[1,u],[0,1]] : u ∈ F_q((1/T))}`. Key results:

- **Athreya–Ghosh, *Ultrametric logarithm laws I & II*** (Monatsh. Math. 2012) — function-field analogs of Sullivan/Kleinbock–Margulis logarithm laws; horocycle case via mixing of the diagonal flow.
- **Broise-Alamichel–Parkkonen–Paulin**, *Equidistribution and Counting Under Equilibrium States* (Progress in Math. 329, Birkhäuser 2019), Ch. 16 (also arXiv:1612.06717) — counting and equidistribution of rational points `a/b ∈ K/O_∞` with `|b| ≤ Q` along horoballs.
- **Horesh–Paulin**, *Effective equidistribution of lattice points in positive characteristic* (J. Théor. Nombres Bordeaux 34 (2022); arXiv:2001.01534) — **effective joint equidistribution of renormalized primitive pairs `(a,b) ∈ A^2` with `gcd(a,b)=1`** in `K_∞^2`: the renormalised primitive lattice converges to an explicit absolutely continuous limit. The density is implicit; extracting the `2·𝟙_{x+y>1}` analog requires unpacking the pushforward.
- **Dang–Paulin–Sayous 2024** (arXiv:2503.13995) — divergent diagonal orbits in positive char; supplies measure-theoretic tools.

**(C) Classical Farey gap results extended.** Boca–Heersink–Spiegelhalter 2013 (Integers A44) and Sayous 2024 (IJNT 2025, arXiv:2407.04380) treat Farey gaps under divisibility constraints and over imaginary quadratic number fields — the latter uses the homogeneous-dynamics method we'd need to port. **No analog over `F_q(T)` is in the literature** (verified via arXiv searches on "polynomial Farey", "Farey function field", "BCZ function field"; the 2024 "polynomial Farey" paper is about polynomial *coprimality conditions* on Z-Farey, not function-field Farey).

**Gap in the literature:** the equidistribution machinery exists (Horesh–Paulin); the explicit BCZ density / Poincaré section over `F_q(T)` has not been written down. That is what a real ship would deliver.

---

## 3. Concrete computational plan

Computing the function-field analog of the BCZ joint distribution for small `(q, N)` is straightforward and cheap. Estimates:

| `q` | `N` | `|F_N|` (approx) | consecutive pairs | RAM | wallclock (single core) |
|---|---|---|---|---|---|
| 2 | 6 | ~ 2·10³ | ~ 2·10³ | <1 MB | seconds |
| 2 | 10 | ~ 3·10⁵ | ~ 3·10⁵ | ~ 30 MB | minutes |
| 2 | 14 | ~ 5·10⁷ | ~ 5·10⁷ | ~ 5 GB | ~ 1 hour |
| 3 | 10 | ~ 4·10⁷ | ~ 4·10⁷ | ~ 4 GB | ~ 1 hour |
| 5 | 8 | ~ 1.5·10⁸ | ~ 1.5·10⁸ | ~ 15 GB | ~ 4 hours |

(Counts use `|F_N| ~ q^{2N}(q−1)/(q+1)`.)

**Algorithm.**
1. Enumerate monic `b ∈ F_q[T]` of degree `n ∈ {1,...,N}`.
2. For each, enumerate `a` with `deg a < deg b` and `gcd(a,b) = 1` (function-field Euclidean algorithm — O(deg² log q) per pair, fully parallel).
3. Sort by chosen ordering. We recommend two parallel pipelines: (a) lex ordering on `a/b mod 1/T` (using the `1/T`-adic expansion of `a/b` as the sort key), and (b) the polar ordering induced by the BT-tree cusp section.
4. For each consecutive pair, record `(x, y) = (|b_i|/q^N, |b_{i+1}|/q^N)`, and the cross-product `c = a_{i+1}b_i − a_ib_{i+1} ∈ F_q^×`.
5. Histogram on `(0,1]^2`. Test:
    - density limit (function-field BCZ analog);
    - cluster=2 universality threshold `q*` for the chain `b_{i+2} = ⌊(b_i + B)/b_{i+1}⌋ · b_{i+1} − b_i` (with `B = T^N` playing the role of `N`);
    - compare numerical `q*_{q,N}` against the conjectured `(11 − 8·ln(3/2))/9` (and its function-field correction).

**Computing budget:** a single workstation suffices through `(q,N) = (2,14)`, `(3,10)`, `(5,8)`. Anything beyond — `(2,18)` or `(3,12)` — wants a small cluster (~ 100 core-hours).

**Code reuse:** the existing `bcz_chain_1B.py` adapts straightforwardly. Replace `Z` arithmetic with `F_q[T]` arithmetic (use SageMath's `PolynomialRing(GF(q), 'T')`; gcd/Euclidean step is built in). One subtlety: floor division `⌊(b_i + N)/b_{i+1}⌋` becomes polynomial quotient `(b_i + B) // b_{i+1}` — no truncation ambiguity, but the *constant of integration* (i.e., what to do with the `F_q^×` cross-product) needs a modeling choice (see §4 risk #1).

---

## 4. Risk assessment (where the analog might break)

1. **Cross-product ambiguity (`q−1` instead of `1`).** Over `Z`, consecutive Farey neighbours satisfy `a_{i+1}b_i − a_ib_{i+1} = 1`. Over `F_q[T]` it is a nonzero constant — `q−1` possible values. Whether the limiting density is `2·𝟙_{x+y>1}` on the triangle, or splits into `q−1` translates of it, depends on whether we quotient by `F_q^×`. **Probability of derailment: moderate.** Likely resolves to: the right BCZ density is `(2/(q−1)) · 𝟙_{x+y>1}` *per cross-product class*, total mass 2 on the union. Empirically verifiable in week 1.

2. **Equidistribution rate is polynomial, not square-root.** Effective mixing for the BT-tree horocycle flow gives an error term of size `q^{−εN}` for some explicit `ε` (Horesh–Paulin), but the constant `ε` may be smaller than the analogous `1/2 − ε` rate from real horocycle mixing (Selberg / Ratner). This affects how fast empirical histograms converge — and could mean `N = 8` is too small to see the BCZ density cleanly even for `q = 5`. **Probability of derailment: low-moderate.** Mitigation: use larger `q`, smaller `N` — `q = 7, N = 6` gives `~3·10⁹` pairs of which we'd subsample.

3. **The chain `b_{i+2} = ⌊(b_i + B)/b_{i+1}⌋ b_{i+1} − b_i` may not be the right dynamics.** The Q-chain comes from the *next-term* algorithm for the Farey sequence, which uses the Stern–Brocot tree. The Stern–Brocot tree over `F_q[T]` exists (Berthé, Nakada and others have studied it) but its branching factor is `q` not 2; the recursion structure changes accordingly. **Probability of derailment: moderate-high.** The cluster=2 transition `q* = (11 − 8 ln(3/2))/9` was derived from a *specific* integration on the BCZ triangle; the function-field analog may produce a *family* of thresholds indexed by `q` rather than a single universal constant. *This is actually the most likely outcome* — and it would still be a publishable result, just not "universality" in the strictest sense.

4. **`ln(3/2)` becomes a `q`-adic logarithm.** The closed form `(11 − 8 ln(3/2))/9` came from integrating `−x ln x` style densities on the BCZ triangle. The function-field analog of these integrals will replace `ln` by either `log_q` (a clean replacement, yielding `(11 − 8 log_q(3/2))/9`) or by a more exotic special value (`L'_A(1)` style — Carlitz logarithms, Anderson–Thakur). **Probability of derailment: low for `log_q` case, moderate for Carlitz case.** Diagnosis is purely computational: fit empirical `q*` as a function of `q` and see whether `log_q(3/2)` or `(q-1)log(3/2)/log(q)` or a Carlitz-log term fits.

5. **Position of "1" in the triangle.** The BCZ triangle is `{x+y > 1, 0 < x, y < 1}` — the "1" is the cutoff between gaps-of-Farey-fractions and the next-fraction algorithm. Over `F_q[T]`, the analog cutoff might be `|x+y| > q^{−N}` or `deg(b_i b_{i+1}) ≥ N+1` rather than `x+y > 1`. **Probability of derailment: low.** This is just a normalisation choice; only one normalisation yields the right `q^{2N}`-scale density.

---

## 5. The "Weil RH makes the wall finite" claim — interpreted

The MEMORY note says function-field RH (= Weil/Deligne) makes "the wall finite". For the **cluster=2 universality** question specifically, this means the following.

The **error term** in the equidistribution of Farey fractions over `Q` is controlled by zeros of `ζ(s)`: the Mertens-type sums `Σ_{n ≤ Q} μ(n)/n` whose decay (under RH) is `O(Q^{−1/2+ε})` is what gives the polynomial convergence rate of empirical BCZ densities to the limit. Over `Q`, RH is *conjectural*.

Over `F_q(T)`, the relevant zeta function is `Z_C(u) = P(u) / ((1−u)(1−qu))` where `P(u) ∈ Z[u]` of degree `2g` (here `C = P¹`, `g = 0`, so `P = 1` and everything is *trivially* a product of geometric series). The "RH" — `|α_i| = √q` for the inverse roots — is Weil 1948 and Deligne 1974. The point isn't that Weil RH is *needed* for `F_q(T)` (genus 0 makes it trivial); it's that **all the equidistribution error terms one would write down are *explicit finite sums* of `q^{-N/2}` terms**, with no conjectural input.

Concretely: where the `Z`-version of BCZ universality needs a Tauberian/Selberg-zero-free-region argument, the `F_q(T)`-version reduces to a finite Frobenius eigenvalue computation. This is a **real but bounded** advantage: it converts what would be conjectural error rates over `Z` into unconditional polynomial rates over `F_q(T)`. It does **not** automatically give the closed-form `q*` analog — that still requires doing the integral on the function-field BCZ triangle correctly.

A clean statement of the advantage: "any cluster=`k` universality threshold provable conditionally on RH over `Q` is *unconditionally* provable over `F_q(T)`, *if* the BCZ density analog is established." The "if" is exactly the work item.

---

## 6. Verdict

**SHIP a short empirical note + DEFER the rigorous theorem.**

Recommended path (target: 6–8 weeks part-time):

1. **Week 1.** Adapt `bcz_chain_1B.py` to `F_q[T]`. Run `(q,N) ∈ {(2,10), (2,12), (3,8), (3,10), (5,6), (5,8)}`. Histogram joint `(x_i, x_{i+1})` densities. Resolve risk #1 (cross-product split) empirically.
2. **Week 2.** Test cluster=2 threshold: compute `q*_{q,N}` for each `(q,N)`. Fit candidate closed forms `(11 − 8·log_q(3/2))/9` etc.
3. **Week 3.** Write a 6–8 page empirical note: "Function-field analog of the BCZ joint density and the cluster=2 threshold — numerical evidence." Position as a *companion/conjecture* paper to the Q-paper. Cite Horesh–Paulin and Broise-Alamichel–Parkkonen–Paulin as the equidistribution backbone that *should* prove the density limit.
4. **Weeks 4–8 (optional, stretch).** Try to extract the explicit BCZ density from Horesh–Paulin's Theorem 1.1 by pushforward. If successful → rigorous statement; if not → cleanly identified open problem.

**Do NOT** attempt the rigorous closed-form theorem first. The pure-theory route is a 6-month project that would likely conflict with the AC§8 N·W→C note that MEMORY flags as the strategic priority.

**Honest novelty estimate.** If executed: the empirical note is **genuinely new** (no such histograms or thresholds exist in the literature). The rigorous density theorem, if achieved, is **moderately new** (Horesh–Paulin do most of the work — extracting the explicit density is more "unpacking" than "discovery"). The cluster=2 closed-form analog, if it survives, is **clearly new**.

**Strategic fit.** The empirical note slots naturally next to the existing BCZ chain MC result (commit `1263e65`) and the q*_BCZ closed form. It complements rather than competes with the AC§8 / N·W→C direction. Cost: small. Risk-of-derailment: managed via early empirical checks on risks #1, #3, #4.

---

## References (primary)

- Athreya, J. S., Cheung, Y., *A Poincaré section for the horocycle flow on the space of lattices*. IMRN 2014(10), 2643–2690. [arXiv:1206.6597]
- Athreya, J. S., Ghosh, A., *Ultrametric logarithm laws, II*. Monatsh. Math. 167 (2012). [arXiv:1103.1698]
- Athreya, J. S., Ghosh, A., Prasad, A., *Ultrametric logarithm laws I*. (And: *Logarithm laws for strong unstable foliations*, arXiv:1205.4515, Paulin.)
- Boca, F., Cobeli, C., Zaharescu, A., *A conjecture of R. R. Hall on Farey points*. J. reine angew. Math. 535 (2001), 207–236.
- Boca, F., Heersink, B., Spiegelhalter, P., *Gap distribution of Farey fractions under some divisibility constraints*. Integers 13 (2013), A44.
- Broise-Alamichel, A., Parkkonen, J., Paulin, F., *Equidistribution and Counting Under Equilibrium States in Negative Curvature and Trees*. Progress in Math. 329, Birkhäuser 2019. (Ch. 16: function fields.) [arXiv:1612.06717]
- Dang, N.-T., Paulin, F., Sayous, R., *Equidistribution of divergent diagonal orbits in positive characteristic*. arXiv:2503.13995 (2024).
- Horesh, T., Paulin, F., *Effective equidistribution of lattice points in positive characteristic*. J. Théor. Nombres Bordeaux 34 (2022). [arXiv:2001.01534]
- Horesh, T., Paulin, F., *Joint effective equidistribution of partial lattices in positive characteristic*. arXiv:2404.04368 (2024).
- Sayous, R., *Gaps in the complex Farey sequence of an imaginary quadratic number field*. IJNT 2025. [arXiv:2407.04380]
- Serre, J.-P., *Trees*, Springer 1980. (Ch. II for `PGL_2(F_q[T])` acting on the BT tree.)
- Deligne, P., *La conjecture de Weil I*. Publ. Math. IHES 43 (1974). (For "RH over function fields".)

**Word count: ~2350.**
