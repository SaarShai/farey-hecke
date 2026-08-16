# LAW (U3) — the scattering-pole → Selberg-zero transport

**Date:** 2026-08-15. **Lane G.**
**Obligation:** `U3` of `lane_g/LAW_T2_DETERMINANT.md` §5.2 = `C14` of `lane_g/LAW_ANCHOR_T1_THETA.md`
§7.1 = `G6`/`N2` of `lane_g/M1F_EISENSTEIN_DERIVATION.md` §5.4, §6. Blocks **both** tail
formulations, (T2) and (T2′), and is the cheapest of the open items.
**Parents read in full:** `LAW_T2_DETERMINANT.md`, `LAW_ANCHOR_T1_THETA.md`,
`M1F_EISENSTEIN_DERIVATION.md` §5.

**Status convention (identical to M1F / T1 / T2):**
`PROVED` = derived here in closed form, or verified in exact/symbolic arithmetic.
`CITATION(ref)` = imported, import named, and *read* in the form quoted.
`TODO-VERIFY(ref, what)` = the content is quoted from a source I read, but the *primary* source it
attributes it to was **not opened in this session**; the named check is owed to a human with the book.
`HEURISTIC` = float evidence. `GAP` = not justified, with the missing statement written out.

**No equation or theorem number appears below that I did not read on a page I actually retrieved.**
Where a number belongs to a book I could not open, it is carried as `TODO-VERIFY` together with the
*secondary* source that asserts it, and the secondary source is quoted verbatim.

**No certificate is produced. Nothing is committed. `lane_f` is untouched.**

---

## 0. Verdict up front

> ### **U3: CLOSED-BY-CITATION**, and independently **CLOSED-WITH-PROOF** modulo one cited
> ### functional equation. **Two logically independent routes agree.**
> ### `Z_{Γ_θ}` has a zero at `s_∞ = ρ₁/2 = 0.25 + 7.0673625708673468952…i` of order
> ### **exactly `2·m(ρ₁)`**, hence **≥ 2**, and **= 2** given the (verified) simplicity of `ρ₁`.
> ### Every cancellation channel is excluded explicitly. **The G_q version is pure citation.**

What changed. `M1F` §5.2 reduced `G6` to "a single, standard, citable fact … I am not asserting a
number for it", and `M1F` §6.1 recorded a scout that "**resolved nothing**". This note resolves it:

1. **The transport theorem is found, stated, and quoted verbatim** from a peer-reviewed paper that
   attributes it to a named theorem in Hejhal with a page number (§2.2). It is *exactly* the U3
   statement, including the multiplicity.
2. **The full divisor of `Z_Γ` for a cofinite Fuchsian group — including elliptic fixed points —**
   is quoted item by item (§2.3), from a second, independent paper attributing it to Venkov and to
   Hejhal, again with page numbers. Item 6 of that list **is** U3.
3. **The functional equation `M1F` §5.2 needed is found in explicit closed form** (§2.5), for
   exactly our class of surfaces (cofinite, cusps **and ramification points**), in a published
   paper whose statement I read. With it, `M1F` §5.2's shape argument becomes a complete proof —
   an independent second route to the same conclusion. `M1F` obligation **N2 is discharged in
   content**; only the Hejhal *page check* remains, and it is now optional rather than load-bearing.
4. **A previously unnoticed hazard is removed.** The classical statement is phrased as
   "*`Z` has a zero at `β` of the same order as the zero of `det Φ` at `1 − β̄`*" — a **conjugate**
   point. Rather than import "`φ` is real on `R`" to convert it, §3.3 evaluates
   `det Φ_θ` **at `1 − s̄_∞` directly in closed form** and finds an order-2 zero there. The
   transport is therefore applied in the exact form in which it is stated.

**One correction to a parent note, flagged rather than buried** (§3.7, non-load-bearing):
`LAW_ANCHOR_T1_THETA.md` §4.4 says the poles of `det Φ_θ` at `s = ikπ/log 2` are "of order 2 in
`E`". They are **simple** (`PROVED` + numeric: `res = 3/(2 log 2) = 2.164042`).

---

## 1. The setting, fixed once

`Γ ⊂ PSL(2,R)` is **cofinite** (finite covolume `|X| = vol(Γ\H) < ∞`), **non-cocompact**, with
`n ≥ 1` cusp classes and `v ≥ 0` elliptic classes of orders `m_1,…,m_v`. `X = Γ\H` is then a
hyperbolic orbifold "of type `(g; n; m_1,…,m_v)`". Both objects of interest are of this kind:

| group | `g` | `n` (cusps) | elliptic orders | `|X|` | check |
|---|---|---|---|---|---|
| `Γ_θ = ⟨S, T²⟩` | 0 | **2** (`∞` width 2, `1` width 1) | `{2}` (the class of `S`) | `π` | `2π(−2 + 2 + (1−½)) = π` ✓ |
| `G_q = ⟨S, T_{λ_q}⟩` | 0 | **1** | `{2, q}` | `π(1−2/q)` | `2π(−2+1+(1−½)+(1−1/q)) = π(1−2/q)` ✓ |

`PROVED` (Gauss–Bonnet for orbifolds; the cusp inventory of `Γ_θ` is `LAW_ANCHOR_T1_THETA.md` §1.2,
`PROVED`; the `(2,q,∞)` structure of `G_q` is `M1F` §1.5 / `LAW_T2_DETERMINANT.md` §1.1, `PROVED`).

> **Note this, because it disqualifies one otherwise-tempting citation.** *Both* groups contain
> elliptic elements — `S` has order 2 — so **`Γ_θ\H` and `G_q\H` are orbifolds, not surfaces**, and
> `Γ_θ`, `G_q` are **not torsion-free**. Any divisor theorem stated for torsion-free `Γ` (e.g.
> Borthwick–Judge–Perry, §2.4 below) is **corroboration only**, not the citation we may lean on.
> §2.2, §2.3 and §2.5 are each stated for general cofinite `Γ`, elliptic elements included.

`Φ(s) = (φ_{ij}(s))_{1≤i,j≤n}` is the scattering matrix, defined by the constant terms of the
Eisenstein series at the cusps, and `φ(s) := det Φ(s)`. Definition read verbatim from
`CITATION(Teo, arXiv:1901.07898v2, §2, p. 3)`:

> "`E_i(σ_j z, s) = δ_{ij} y^s + φ_{ij}(s) y^{1−s} + exponentially decaying terms.`
>  The scattering matrix `Φ(s)` defined by `Φ(s) = (φ_{ij}(s))_{1≤i,j≤n}` is a symmetric matrix.
>  We denote by `φ(s)` its determinant."

This is the same normalisation `M1F` (3.2), `LAW_ANCHOR_T1_THETA.md` §2 and (2.5) use — the same
`σ_a`-scaled constant term, the same `y^{1−s}` coefficient. **The normalisation matches**, which is
the one place a transport of this kind can silently go wrong.

`Z_Γ(s) = ∏_{[P₀] prim. hyp.} ∏_{k≥0} (1 − N(P₀)^{−(s+k)})`, absolutely convergent for `Re s > 1`.

---

## 2. The divisor identity — the theorem

### 2.1 The statement we need, isolated

> **THEOREM U3 (scattering-pole → Selberg-zero transport).**
> Let `Γ` be cofinite with `n ≥ 1` cusps (elliptic elements permitted). Let `s₀ ∈ C` with
> `Re s₀ < 1/2` and `Im s₀ ≠ 0`. If `φ(s) = det Φ(s)` has a pole of order `m` at `s₀`, then the
> Selberg zeta function `Z_Γ` has a **zero of order exactly `m`** at `s₀`.
>
> Equivalently, in the form in which the literature states it: `Z_Γ` has a zero at `β` of the same
> order as the zero of `φ` at `1 − β̄`, for `Re β < 1/2`, `Im β > 0`.

Two routes to it are given: §2.2–2.4 quote it as a **divisor theorem** (`CLOSED-BY-CITATION`);
§2.5–2.6 **derive** it from the functional equation (`CLOSED-WITH-PROOF`, modulo one citation).

### 2.2 Route A, source 1 — the statement in exactly our form `CITATION`

`CITATION(Bruggeman–Fraczek–Mayer)` R. W. Bruggeman, M. Fraczek, D. Mayer, *Perturbation of zeros of
the Selberg zeta-function for `Γ₀(4)`*, **Experimental Mathematics 22 (2013) 217–242**;
arXiv:1201.2324v1, §3.4 "Zeros of the Selberg zeta-function", p. 41. **Read verbatim:**

> "we … need the relation to automorphic forms, which is summarized in **Theorem 5.3 in Chapter X
> of [7], p. 498**. We quote the results concerning zeros in the region `Im β > 0`. …
> **a)** At points `β` on the central line `½ + i(0,∞)` the function `Z(α,·)` has a zero of order
> `dim Maass₀(α,β)`. …
> **b)** At points with `Re β < ½` and `Im β > 0` the function `Z(α,·)` has **a zero of the same
> order as the zero of the determinant of the scattering matrix at `1 − β̄`**. These are the
> resonances. …
> The determinant of the scattering matrix has a zero at `1 − β̄` if and only if it has a
> singularity at `β`."

with `[7] = D. A. Hejhal, The Selberg trace formula for PSL(2,R), Lect. Notes in Math. 1001,
Springer, 1983` (their bibliography, read verbatim).

**This is Theorem U3, including the multiplicity ("of the same order") and including the
pole↔zero conversion ("zero at `1 − β̄` iff singularity at `β`").** `α` is a character parameter;
`α = 0` is the trivial character, i.e. the plain Selberg zeta.

`TODO-VERIFY(Hejhal LNM 1001 vol. II, Ch. X Thm 5.3, p. 498 — open the book and confirm the theorem
number, the page, and that the hypothesis class is cofinite `Γ` **with elliptic elements allowed**,
not merely torsion-free.)` I did not open Hejhal. Bruggeman–Fraczek–Mayer's own group `Γ₀(4)` is
torsion-free, so their application does not by itself certify the elliptic case — **this is why
§2.3 and §2.5 are supplied.**

### 2.3 Route A, source 2 — the complete divisor of `Z_Γ`, elliptic elements included `CITATION`

`CITATION(Friedman–Jorgenson–Smajlović)` J. S. Friedman, J. Jorgenson, L. Smajlović, *Super-zeta
functions and regularized determinants associated to cofinite Fuchsian groups with
finite-dimensional unitary representations*, **Letters in Mathematical Physics 111 (2021), art. 15**;
arXiv:2011.12795v1, §2.5, pp. 6–7. Standing hypothesis, read verbatim from their abstract: "*Let `M`
be a finite volume, non-compact hyperbolic Riemann surface, **possibly with elliptic fixed
points***". **The divisor list, read verbatim** (`k` = number of cusps; `φ(s) = det Φ(s)`;
`q(σ) :=` multiplicity of the pole of `φ` at `σ`):

> "We now state the divisor of the `Z(s)` (see **[24, p. 49] [12, p. 499]**):
> 1. Zeros at the points `s_j` on the line `Re(s) = ½` symmetric relative to the real axis and in
>    `(1/2, 1]`, … multiplicity `m(s_j) = m(λ_j)` …
> 2. Zeros at the points `s_j ∈ [0, 1/2)` where `s_j(1−s_j) = λ_j ∈ [0, 1/4)` … multiplicity
>    `m̃(s_j) = m(λ_j) − q(1−s_j) ≥ 0` …
> 3. The point `s = ½` can be a zero or a pole, and the order of the point as a divisor is
>    `a = 2d_{1/4} − ½(k − tr Φ(½))` …
> 4. Poles at `s = −n − ½`, where `n = 1, 2, …`, each with multiplicity `k`;
> 5. Finitely many real zeros `1 − ρ_i < 1/2`, where `i = 1 … N`;
> 6. **Zeros at each `s = 1 − ρ`, `1 − ρ̄` where `ρ` is a zero of `φ(s)` with `Re(ρ) > ½` and
>    `Im(ρ) > 0`;**
> 7. Zeros at points `s = −n ∈ −N = {0, −1, −2, …}`, with multiplicities `m_n = h (vol(M)/2π)(2n+1)
>    − Σ_{{R}_Γ} Σ_{k=1}^{d_R−1} tr(χ^{−1}(R)) sin(kπ(2n+1)/d_R) / (d_R sin(kπ/d_R))`."

with, from their bibliography (read verbatim): `[12] D. A. Hejhal, The Selberg trace formula for
PSL(2,R), vol. II, Lecture Notes in Mathematics 1001, Springer-Verlag, 1983`; `[24] A. Venkov,
Spectral theory of automorphic functions and its applications, Mathematics and its Applications
(Soviet Series) 51, Kluwer Academic Publishers Group, Dordrecht, 1990`.

**Three things this buys that §2.2 alone does not.**

- **Item 6 is U3.** Combined with `φ(s)φ(1−s) = 1` (their (2.6), and `PROVED` for `Γ_θ` in
  `LAW_ANCHOR_T1_THETA.md` C8), "`ρ` a zero of `φ` with `Re ρ > ½`" ⟺ "`1 − ρ` a pole of `φ` with
  `Re < ½`". So: **every pole of `φ` off the real axis in `Re s < 1/2` is a zero of `Z`.**
- **Item 7 contains the elliptic sum `Σ_{{R}_Γ}` explicitly** — the list is stated for a group
  *with* elliptic classes, and the elliptic contribution lands **only at `s = −n ∈ −N`**, i.e.
  **only on the real axis**. This is precisely what §3.5 needs.
- **The complete pole set of `Z_Γ` is items 3 and 4 — `s = ½` and `s = −n − ½` — all real.**
  Hence `Z_Γ` is **holomorphic off the real axis**, so nothing can cancel a zero produced by item 6.

`TODO-VERIFY(Venkov 1990 book p. 49; Hejhal LNM 1001 vol. II p. 499 — confirm the seven-item divisor
and, in particular, the multiplicity attached to item 6, which FJS state without a multiplicity.)`
The multiplicity is supplied by §2.2 ("of the same order"); the two sources are consistent but the
multiplicity is asserted by only one of them.

### 2.4 Corroboration (torsion-free only, **not** load-bearing) `CITATION`

`CITATION(Borthwick–Judge–Perry)` D. Borthwick, C. Judge, P. A. Perry, *Selberg's zeta function and
the spectral geometry of geometrically finite hyperbolic surfaces*, **Comment. Math. Helv. 80 (2005)
483–515**; arXiv:math/0310364v2, **Theorem 1.1**, p. 1. **Read verbatim:**

> "**Theorem 1.1.** Let `n_C` denote the number of cusps of `X`, and let `χ` denote the Euler
> characteristic of `X`. The Selberg zeta function `Z_X` extends to a meromorphic function of order
> two, with a divisor that can be divided into spectral and topological components: **The spectral
> zeros of `Z_X` are given by the resonance set `R_X` (with multiplicities).** In addition, `Z_X(s)`
> has topological zeros at `s = −k` for `k ∈ N₀`, of order `(2k+1)·(−χ)`, and topological poles of
> order `n_C` at `s ∈ ½ − N₀`."

and, same page:

> "If `X` has finite area, then meromorphic continuation with the order bound and divisor as given
> here can be deduced from the Selberg trace formula (see [11])."

**Why this is corroboration only.** BJP's `X` is a *surface*: their Theorem 1.3 and Corollary 1.4
are about "a finitely generated, **torsion-free**, discrete subgroup of `SL(2,R)`". `Γ_θ` and `G_q`
have torsion. The agreement with §2.3 on the shape of the divisor — spectral zeros = resonances with
multiplicity; topological zeros at `−N₀`; topological poles of order `n_C` on `½ − N₀`, all real —
is nonetheless a genuine independent check of the parts we use.

### 2.5 Route B — the functional equation, in closed form, for orbifolds `CITATION`

This is the object `M1F` §5.2 assumed only the *shape* of, and `M1F` obligation **N2** asked to be
pinned. It is found, for exactly our class (cofinite, cusps **and** ramification points).

`CITATION(Teo)` L.-P. Teo, *Ruelle zeta function for cofinite hyperbolic Riemann surfaces with
ramification points*, **Letters in Mathematical Physics 110 (2020) 61–82**; arXiv:1901.07898v2,
**Proposition 2.5**, p. 7. **Read verbatim** (notation of their Theorem 2.2: `X` of type
`(g; n; m_1,…,m_v)`, `|X|` = area, `n` = number of cusps, `v` = number of ramification points of
orders `m_j`, `Γ₂` = Barnes double gamma, `A = n − tr Φ(½)`, `C = −n log 2`):

> "**Proposition 2.5.** The functional equation of the Selberg zeta function is given by
> `Z(1−s) = κ(s) Z(s)`, **(2.6)** where
>
> `κ(s) = (−1)^{A/2} e^{C(2s−1)} φ(s) × ∏_{j=1}^{v} ∏_{k=0}^{m_j−1} [ sin(π(s+k)/m_j) ]^{(m_j−2k−1)/m_j}
>        × [ (2π)^{2s−1} Γ₂(s)² Γ(1−s) / ( Γ₂(1−s)² Γ(s) ) ]^{|X|/2π}
>        × [ Γ(3/2 − s) / Γ(s + 1/2) ]^{n}`."

and, from their **Theorem 2.2** (p. 6), the factorization that names the pieces:

> "`det(∆ − s(1−s)) = Z_∞(s) Z(s) Z_ell(s) Γ(s + ½)^{−n} (2s−1)^{A/2} e^{B(s−½)² + C(s−½) + D}`
>  **(2.4)** where `Z(s) = ∏_P ∏_{k=0}^{∞} (1 − p^{−s−k})` **(2.5)** is the Selberg zeta function of
>  the surface `X`,
>  `Z_∞(s) = [ (2π)^s Γ₂(s)² / Γ(s) ]^{|X|/2π}`,
>  `Z_ell(s) = ∏_{j=1}^{v} ∏_{k=0}^{m_j−1} Γ((s+k)/m_j)^{(2k+1−m_j)/m_j}`,
>  `A = n − tr Φ(½)`, `B = −|X|/2π`, `C = −n log 2`."

`TODO-VERIFY(Teo, LMP 110 (2020) 61–82 — I read arXiv:1901.07898v2, not the journal version;
confirm that the journal numbering is still Theorem 2.2 / Proposition 2.5 and that `(2.6)` is
unchanged. Also confirm the branch convention for the fractional exponents.)`

**This is the "Selberg zeta = product over resonances × Barnes/Γ factors" the brief named**, in its
regularized-determinant form: `Z_∞` is the Barnes factor (identity contribution), `Z_ell` the
elliptic Γ-factor, `Γ(s+½)^{−n}` the parabolic factor, and `φ(s)` enters the functional equation
alone and undivided.

### 2.6 `PROVED` (given (2.6)) — Theorem U3, derived

> **Lemma U3-A.** `Z_Γ(s)` is holomorphic and non-vanishing on `{Re s > 1/2} ∩ {Im s ≠ 0}`.
>
> *Proof.* Read off §2.3's divisor list. Zeros: item 1 lies on `Re s = ½` or in the real interval
> `(1/2, 1]`; item 2 in `[0, 1/2)`; item 5 is real; item 6 lies in `Re s < 1/2` (since
> `Re(1−ρ) < 1/2` when `Re ρ > 1/2`); item 7 is at non-positive integers. Poles: items 3 and 4, at
> `s = ½` and `s = −n − ½`, all real. **No divisor point of `Z_Γ` lies in the open region
> `Re s > 1/2`, `Im s ≠ 0`.** ∎
>
> (Independently, and without the list: `Z_Γ` is given by an absolutely convergent Euler product in
> `Re s > 1`, hence holomorphic and zero-free there; and in `½ < Re s ≤ 1` its only zeros come from
> exceptional eigenvalues `λ_j ∈ [0, 1/4)`, whose `s_j` are **real**. `CITATION`, standard;
> this is the same fact `M1F` §5.2 used and labelled.)

> **Lemma U3-B.** Every factor of `κ(s)` **except `φ(s)`** is finite and non-zero at every non-real
> `s`. `PROVED`.
>
> *Proof, factor by factor from (2.6).*
> - `(−1)^{A/2} e^{C(2s−1)}`: a non-zero constant times `exp` of an entire function. Never `0`, never `∞`.
> - **elliptic factor** `∏_j ∏_k [sin(π(s+k)/m_j)]^{(m_j−2k−1)/m_j}`: `sin(πz) = 0` iff `z ∈ Z`, so
>   `sin(π(s+k)/m_j) = 0` forces `(s+k)/m_j ∈ Z`, i.e. `s ∈ R`. `sin` has no poles. A fractional
>   power of a nowhere-zero, finite holomorphic function on a simply connected region avoiding the
>   zero set is again nowhere zero and finite (fix any branch). So: finite and non-zero off `R`.
> - **Barnes factor** `[(2π)^{2s−1} Γ₂(s)²Γ(1−s)/(Γ₂(1−s)²Γ(s))]^{|X|/2π}`: `Γ₂` is entire with
>   zeros only at non-positive integers; `Γ(1−s)` has poles only at `s = 1, 2, …`; `1/Γ(s)` is entire
>   with zeros only at `s = 0, −1, −2, …`; `(2π)^{2s−1}` is nowhere zero and entire. **All
>   zeros and poles of the bracket are real**, so the same branch argument applies.
> - **parabolic factor** `[Γ(3/2−s)/Γ(s+1/2)]^{n}`: poles of `Γ(3/2−s)` at `s = 3/2, 5/2, …`; zeros
>   of `1/Γ(s+½)` at `s = −½, −3/2, …`. All real. ∎
>
> `PROVED`, given only the *shape* of (2.6) — which is exactly the reduction `M1F` §5.2 performed,
> now with the shape supplied by a read source instead of assumed.

> **Theorem U3, proof.** Let `s₀` be non-real with `Re s₀ < 1/2`, and let `φ` have a pole of order
> `m ≥ 1` at `s₀`. Apply `ord_{s₀}` to (2.6):
> ```
>    ord_{s0} [ Z(1 - s) ]  =  ord_{s0} kappa  +  ord_{s0} Z .
> ```
> The left side is `ord_{1−s₀} Z_Γ`, and `Re(1−s₀) > 1/2` with `Im(1−s₀) ≠ 0`, so by **Lemma U3-A**
> it is `0`. By **Lemma U3-B**, `ord_{s₀} κ = ord_{s₀} φ = −m`. Hence
> ```
>    ord_{s0} Z_Gamma  =  + m .
> ```
> `Z_Γ` has a zero of order exactly `m` at `s₀`. ∎ `PROVED` given `CITATION(Teo Prop. 2.5)`.

**The two routes agree**, and they are logically independent: Route A reads the divisor off a
classical theorem; Route B derives it from the functional equation and the location of the divisors
of the elementary factors. Route B additionally certifies the **orbifold** case, since (2.6) carries
the ramification points explicitly.

---

## 3. Specialization to `Γ_θ`

### 3.1 `Γ_θ` satisfies the hypotheses `PROVED`

Cofinite, `|X| = π`, `n = 2` cusps, one elliptic class of order `m_1 = 2`, genus 0 (§1). Theorem U3
applies. (Route B is the one that certifies this, since `v = 1 ≠ 0`; Route A's source §2.3 also
permits elliptic points explicitly.)

### 3.2 The pole datum, imported from (T1) `PROVED`

From `LAW_ANCHOR_T1_THETA.md` (DET), §4.1–4.2, all `PROVED`:

```
   det Phi_theta(s) = g(s)^2 E(s),     g(s) = Lambda(2s-1)/Lambda(2s),
   E(s) = (4 - 4^s)/( 4^s (4^s - 1) ),   zeros of E on Re s = 1,  poles of E on Re s = 0.
```

`det Φ_θ` has a pole of order `2·m(ρ)` at `s = ρ/2` for every nontrivial zero `ρ` of `ζ`, with
`m(ρ)` its multiplicity; four candidate cancellation channels are excluded there (T1 §4.2). For the
first zero, `s_∞ = ρ₁/2 = 0.25 + 7.0673625708673468952…i`, order `2m(ρ₁)`.

### 3.3 `PROVED` — the transport applied **in the form in which it is stated**

§2.2's statement is about the zero of `φ` at `1 − β̄`, not the pole at `β`. Converting one to the
other in general needs `φ(s̄) = conj φ(s)` (true here — the Dirichlet coefficients are integer
counts — but it is an extra import). **We do not need it**, because for `Γ_θ` the value at the
conjugate point is available in closed form:

```
   rho_1 = 1/2 + i gamma_1 ,  gamma_1 = 14.134725141734693790457...   (Re rho_1 = 1/2, verified)
   s_inf   = rho_1 / 2        = 0.25 + i gamma_1/2
   1 - conj(s_inf) = 0.75 + i gamma_1/2 = (1 + rho_1)/2                        (3.1)
```

`(3.1)` uses `Re ρ₁ = ½` only; it is arithmetic. At `w := (1+ρ₁)/2`:

- `2w − 1 = ρ₁`, so `Λ(2w−1) = Λ(ρ₁) = 0` to order `m(ρ₁)`;
- `2w = 1 + ρ₁` has `Re = 3/2`, outside the critical strip, where `Λ` has no zeros; `Λ`'s only poles
  are at `w′ = 0, 1`, i.e. `s ∈ {0, ½, 1}`, and `w ∉ {0, ½, 1}`. So `Λ(2w) ≠ 0, ∞`;
- hence `g` has a zero of order exactly `m(ρ₁)` at `w`, and `g²` a zero of order `2m(ρ₁)`;
- `Re w = 3/4`, and `E`'s zeros lie on `Re s = 1`, its poles on `Re s = 0` (T1 §4.1, `PROVED`), so
  `E(w)` is **finite and non-zero**.

```
   ord_{w} ( det Phi_theta )  =  2 m(rho_1) ,     w = 1 - conj(s_inf).          (3.2)  PROVED
```

Now apply §2.2(b) with `β = s_∞` (`Re β = 1/4 < 1/2` ✓, `Im β = 7.067… > 0` ✓):

> **`ord_{s_∞} Z_{Γ_θ} = ord_{1−s̄_∞} (det Φ_θ) = 2 m(ρ₁)`.**

And applying §2.3 item 6 with `ρ = w` (`Re ρ = 3/4 > ½` ✓, `Im ρ > 0` ✓): `Z_{Γ_θ}` has zeros at
`1 − ρ = 0.25 − iγ₁/2` and at `1 − ρ̄ = 0.25 + iγ₁/2 = s_∞`. **Same conclusion, same point.**
And applying Theorem U3 of §2.6 (Route B) with `s₀ = s_∞`, `m = 2m(ρ₁)`: same conclusion again.

### 3.4 The result

> ### **(U3-θ) `PROVED` (given the §2 citations).**
> ### `Z_{Γ_θ}` has a zero at `s_∞ = ρ₁/2 = 0.25 + 7.0673625708673468952…i` of order **`2·m(ρ₁)`**.
> ### Since `m(ρ₁) ≥ 1`, the order is **`≥ 2`**. `ρ₁` is a simple zero of `ζ`
> ### `CITATION(van de Lune–te Riele–Winter; Odlyzko)`, so the order is **exactly 2**.
>
> More generally `Z_{Γ_θ}` has a zero of order `2m(ρ)` at `s = ρ/2` for **every** nontrivial zero
> `ρ` of `ζ` — the whole `Re s = 1/4` family, unconditionally, by de la Vallée Poussin
> (`Re ρ < 1 ⇒ Re(ρ/2) < 1/2`) and `Im(ρ/2) ≠ 0`.
>
> **This is exactly the input `LAW_T2_DETERMINANT.md` §3.2's Hurwitz step consumes**
> ("`Z_{Γ_θ}` has a zero of order 2 at `s_∞` … from (T1) + the scattering→Selberg transport,
> obligation U3"). U3 is discharged.

### 3.5 Every cancellation channel, excluded explicitly `PROVED`

The brief asked for the trivial/topological bookkeeping to be checked at the exact point. It is.
**`Im s_∞ = γ₁/2 = 7.0673625708673468952… ≠ 0`**, and every non-resonance divisor point of `Z_Γ`
is **real**. Channel by channel, against §2.3's list:

| channel | divisor points | why `s_∞` is not one |
|---|---|---|
| **half-integer topological poles** (item 4; BJP "poles of order `n_C` at `s ∈ ½ − N₀`") | `s = ½ − n`, `n ∈ N₀` — **all real** | `Im s_∞ = 7.067 ≠ 0`. **No half-integer collision.** |
| the special point `s = ½` (item 3, order `a = 2d_{1/4} − ½(k − tr Φ(½))`) | `s = ½` — real | `Im s_∞ ≠ 0`; also `Re s_∞ = ¼ ≠ ½` |
| **trivial zeros** (item 7; BJP `(2k+1)(−χ)` at `s = −k`), **including the elliptic sum `Σ_{{R}_Γ}`** | `s = −n ∈ −N₀` — **all real** | `Im s_∞ ≠ 0`. The elliptic contribution of `S` (order 2) lands only here. |
| discrete-spectrum zeros (item 1) | `Re s = ½`, or real in `(½,1]` | `Re s_∞ = ¼` |
| small-eigenvalue zeros (item 2) | `s_j ∈ [0, ½)` — real | `Im s_∞ ≠ 0` |
| finitely many real residual zeros (item 5) | `1 − ρ_i < ½` — real | `Im s_∞ ≠ 0` |
| another resonance at the same point | would need `ρ′/2 = ρ₁/2`, i.e. `ρ′ = ρ₁` | only raises the order; it does not |
| **any pole of `Z_{Γ_θ}` at `s_∞`** | poles of `Z_Γ` are items 3 + 4 only — **all real** | `Z_{Γ_θ}` is **holomorphic off `R`**; nothing can cancel the zero |

The last row is the one that matters logically: a divisor is additive, so a zero of order `2m(ρ₁)`
can only be reduced by a coincident **pole**, and `Z_Γ` has none off the real axis.

**And on the scattering side**, the pole itself was already shown non-cancellable in
`LAW_ANCHOR_T1_THETA.md` §4.2, over a complete factorisation `det Φ_θ = Λ(2s−1)² Λ(2s)^{−2} E`:
four channels excluded, "there is no fifth channel". The two exclusions compose: `φ` has a genuine
pole of order `2m(ρ₁)` at `s_∞`; `Z` has a genuine zero of that order there.

### 3.6 Numeric confirmation — `HEURISTIC` by label, confirming exact statements

Script `lane_g/law_probes/probe_u3_orders.py` (mpmath, 40 dps; **not committed**). It confirms
(3.2) and the T1 pole order, i.e. **both** points the transport statement mentions.

```
rho_1            = 0.5 + 14.13472514173469379045725198356247027078 i
s_inf = rho_1/2  = 0.25 + 7.067362570867346895228625991781235135392 i
1 - conj(s_inf)  = 0.75 + 7.067362570867346895228625991781235135392 i  == (1+rho_1)/2   ✓ (3.1)

(1) pole at s_inf :  (s - s_inf)^2 * det Phi_theta  ->  -0.149434183 - 0.393984600 i   (finite, non-zero)
    r = 1e-3 .. 1e-7 :  -0.14855-0.39159i, -0.14935-0.39374i, -0.14943-0.39396i,
                        -0.14943-0.39398i, -0.14943-0.39398i        => ORDER EXACTLY 2
    [matches LAW_ANCHOR_T1_THETA.md section 5.4 to all printed digits]

(2) zero at 1-conj(s_inf) :  det Phi_theta / (s - w)^2  ->  -0.841624 - 2.218948 i   (finite, non-zero)
    r = 1e-3 .. 1e-7 :  -0.83642-2.20555i, -0.84110-2.21761i, -0.84157-2.21882i,
                        -0.84162-2.21894i, -0.84162-2.21895i        => ORDER EXACTLY 2

(3) E(s_inf) = 1.400510162 - 0.755662569 i     E(w) = 0.553024779 - 0.298391355 i
    both finite and non-zero, as section 3.3 and T1 section 4.1 require
```

**So `det Φ_θ` has an order-2 pole at `s_∞` and an order-2 zero at `1 − s̄_∞`** — the transport's
hypothesis is verified in both of its equivalent phrasings, numerically as well as in closed form.

### 3.7 Side finding — a correction owed to `LAW_ANCHOR_T1_THETA.md` §4.4 `PROVED`

T1 §4.4 states that the poles of `det Φ_θ` at `s = ikπ/log 2` (`k ∈ Z`, `Re s = 0`) are "of order 2
in `E`". They are **simple**. In `X = 2^s`, `E = −(X−2)(X+2)/(X²(X−1)(X+1))` has simple poles at
`X = ±1`; `dX/ds = X log 2 ≠ 0`, so the poles in `s` are simple. Probe item (4):

```
   r * E(s0 + r)  ->  2.164042 = 3/(2 log 2)     r^2 * E(s0 + r)  ->  0     at s0 = i pi/log 2 and 2 i pi/log 2
   g(s0) finite and non-zero at both points
```

So `det Φ_θ = g²E` has **simple** poles there, and (by Theorem U3, since those points are non-real
with `Re = 0 < 1/2`) `Z_{Γ_θ}` has **simple** zeros at `s = ikπ/log 2`, `k ≠ 0` — not double ones.
**Non-load-bearing** (T1's anchor claim is about `s_∞`, where the order 2 is correct and comes from
`g²`, not from `E`), but the lane text should be corrected.

---

## 4. The `G_q` version — what the same transport needs per `q`

> ### **Nothing per-`q`. It is pure citation.** `PROVED` (that the hypotheses hold) + `CITATION`.

Theorem U3 has exactly three hypotheses: `Γ` cofinite; `n ≥ 1` cusps; `s₀` non-real with
`Re s₀ < 1/2`. For every `q ≥ 3`:

| hypothesis | `G_q` | status |
|---|---|---|
| cofinite | `vol(G_q\H) = π(1 − 2/q) < π` | `PROVED` (M1F §1.5) |
| `n ≥ 1` cusps | `n = 1` (the cusp at `∞`, width `λ_q`) | `PROVED` |
| elliptic elements allowed | orders `{2, q}`; permitted by §2.3 and by (2.6) with `v = 2` | `CITATION` |
| `s₀` non-real, `Re s₀ < 1/2` | a hypothesis on the point, not on `q` | — |

> **(U3-q).** For every `q ≥ 3` and every non-real `s₀` with `Re s₀ < 1/2`: if the (`1×1`)
> scattering function `φ_q(s)` of `G_q` has a pole of order `m` at `s₀`, then `Z_{G_q}` has a zero
> of order exactly `m` at `s₀`. Conversely no zero of `Z_{G_q}` off the real axis in `Re s < 1/2`
> can be cancelled, since `Z_{G_q}` has no poles off the real axis.

There is **no `q`-dependent constant, no `q`-uniformity, and no growth estimate** in this statement —
each `q` is a separate application of the same theorem. Contrast U1 (`LAW_T2_DETERMINANT.md` §5.2),
which is `q`-uniform and is the real work.

**The honest limitation, stated loudly and then shown not to matter.**
For non-arithmetic `G_q` (`q ∉ {3,4,6,∞}`) **we do not know the poles of `φ_q`.** There is no closed
form: `φ_q` is not a ratio of completed `L`-functions, and Phillips–Sarnak
(`CITATION`, J. Amer. Math. Soc. **5** (1992) 1–32; the reference is standard for this point, and it
is the same reference the repo's Maass-spectrum work already uses) is the reason to expect there
never to be one. So (U3-q) is a transport with **no known input** at non-arithmetic `q`.

**This does not block the LAW route**, and the reason is structural: under **(T2′)**
(`LAW_T2_DETERMINANT.md` §3.2) the `q`-side zeros are produced by **Hurwitz from `Z_{Γ_θ}`**, not by
a `q`-side scattering computation. The transport is consumed **once, at the anchor `q = ∞`
(i.e. `Γ_θ`)**, which is precisely §3. (U3-q) is therefore recorded as *available*, not *needed*:

- **needed:** (U3-θ) — §3. **Discharged.**
- **available but not needed:** (U3-q) for finite `q`. Would become load-bearing only if someone
  tried to prove the `G_q` off-line zero by locating a scattering pole of `G_q` directly — which,
  absent a closed form for `φ_q`, is not a route the lane has.

---

## 5. Status ledger, step by step

| # | Step | Status | Note |
|---|---|---|---|
| U3.1 | Definition/normalisation of `Φ(s)`, `φ = det Φ` matches M1F (3.2) / T1 §2 | `CITATION(Teo arXiv:1901.07898v2 §2 p.3)` | same `y^{1−s}` constant-term convention; checked term by term |
| U3.2 | `φ(s)φ(1−s) = 1` | `PROVED` for `Γ_θ` (T1 C8, sympy + `<5e−40`); `CITATION(FJS (2.6))` in general | used to convert "zero of `φ` in `Re>½`" ↔ "pole of `φ` in `Re<½`" |
| U3.3 | **Transport statement** — zero of `Z` at `β` of the same order as the zero of `φ` at `1−β̄`, for `Re β < ½`, `Im β > 0` | `CITATION(Bruggeman–Fraczek–Mayer, Exp. Math. 22 (2013) 217–242, §3.4(b))` | verbatim; attributes to Hejhal LNM 1001 Ch. X Thm 5.3 p. 498 |
| U3.4 | Hejhal Ch. X Thm 5.3, p. 498 — hypothesis class includes elliptic elements | `TODO-VERIFY(Hejhal LNM 1001 vol. II — open p. 498; confirm thm number + that cofinite-with-torsion is covered)` | book not opened; **mitigated** by U3.5 and U3.8 |
| U3.5 | **Full divisor of `Z_Γ`, 7 items, elliptic sum explicit** | `CITATION(Friedman–Jorgenson–Smajlović, LMP 111 (2021) art. 15, §2.5)` | verbatim; standing hypothesis "possibly with elliptic fixed points" |
| U3.6 | Multiplicity in item 6 of that list | `TODO-VERIFY(Venkov 1990 p. 49 / Hejhal vol. II p. 499 — FJS state item 6 without a multiplicity)` | supplied by U3.3; two sources consistent, one silent |
| U3.7 | Torsion-free corroboration (spectral zeros = resonances; poles of order `n_C` on `½−N₀`) | `CITATION(Borthwick–Judge–Perry, CMH 80 (2005) 483–515, Thm 1.1)` | **not** applicable to `Γ_θ` (torsion); corroboration only |
| U3.8 | **Functional equation `Z(1−s) = κ(s)Z(s)` with `κ` in closed form, orbifolds included** | `CITATION(Teo, LMP 110 (2020) 61–82, Prop. 2.5 / Thm 2.2)` | **discharges M1F obligation N2 in content**; `TODO-VERIFY` on journal numbering |
| U3.9 | Lemma U3-A: `Z_Γ` holomorphic + zero-free on `Re s > ½`, `Im s ≠ 0` | `PROVED` from U3.5 (+ standard Euler-product argument) | this is the step M1F §5.2 labelled and used |
| U3.10 | Lemma U3-B: every factor of `κ` except `φ` is finite/non-zero off `R` | `PROVED` (§2.6, factor by factor) | Barnes `Γ₂`, `Γ`-ratios, `sin`-powers: all divisors real |
| U3.11 | **Theorem U3 derived from U3.8–U3.10** | `PROVED` given U3.8 | independent of U3.3/U3.4 |
| U3.12 | `Γ_θ`, `G_q` are cofinite orbifolds of type `(0; 2; 2)` and `(0; 1; 2,q)` | `PROVED` (§1, Gauss–Bonnet cross-check) | |
| U3.13 | `det Φ_θ` has a pole of order `2m(ρ)` at `ρ/2`; no cancellation | `PROVED` (T1 §4.2 + §5.4) | inherited unchanged |
| U3.14 | `1 − s̄_∞ = (1+ρ₁)/2` and `ord` of `det Φ_θ` there `= 2m(ρ₁)` | `PROVED` (§3.3, closed form) + numeric | avoids needing "`φ` real on `R`" |
| U3.15 | **`ord_{s_∞} Z_{Γ_θ} = 2m(ρ₁) ≥ 2`** | `PROVED` given U3.3 (or U3.11) | three independent applications agree |
| U3.16 | `m(ρ₁) = 1`, so the order is exactly 2 | `CITATION(van de Lune–te Riele–Winter; Odlyzko)` | `≥ 2` holds without it, which is all (T2′) needs |
| U3.17 | Every cancellation channel excluded, half-integer collision explicit | `PROVED` (§3.5) | `Im s_∞ = 7.067… ≠ 0`; all non-resonance divisor points real; `Z_Γ` pole-free off `R` |
| U3.18 | **(U3-q)**: same transport, any `q`, no per-`q` input | `PROVED` (hypotheses) + `CITATION` (theorem) | §4 |
| U3.19 | Poles of `φ_q` for non-arithmetic `q` are unknown | `GAP` — **but not on the LAW route** | (T2′) consumes U3 only at the anchor; §4 |
| U3.20 | T1 §4.4's "order 2 in `E`" at `s = ikπ/log 2` | `PROVED` **wrong** — the poles are simple | §3.7; non-load-bearing lane-text correction |

**No step is `GAP` on the LAW route.** The only `GAP` in the table, U3.19, is off-route and is
explained as such.

---

## 6. STILL-GAPPED? — no, but here is exactly what a referee would still ask for

The brief asked for a loud STILL-GAPPED if per-surface input we do not have were needed. **It is
not.** The transport needs *no* per-surface input beyond cofiniteness and a cusp. What remains is
**citation hygiene**, not mathematics, and it is enumerated so nobody mistakes its size:

| # | Owed | Kind | Blocking? |
|---|---|---|---|
| **V1** | Open **Hejhal, LNM 1001 vol. II, Ch. X, Thm 5.3, p. 498** and confirm the theorem number, the page, and that torsion is allowed. | library check | **No** — Route B (§2.6) does not use it; §2.3 covers torsion independently. |
| **V2** | Open **Venkov 1990, p. 49** and confirm the 7-item divisor **with the multiplicity of item 6**. | library check | **No** — the multiplicity is in §2.2. |
| **V3** | Confirm **Teo, LMP 110 (2020) 61–82** journal numbering for Thm 2.2 / Prop. 2.5 / eq. (2.6), and the branch convention for the fractional exponents in `κ`. | library check | **No** for the conclusion (only the divisor *locations* of the factors are used, and those are branch-independent). |
| **V4** | Prior-art: none of this is new. The divisor of `Z_Γ` is 1980s classical. **Make no novelty claim for anything in §2.** | standing instruction | — |
| **V5** | `m(ρ₁) = 1` (simplicity of the first zeta zero) is `CITATION`. If one insists on a fully self-contained statement, use the unconditional `order ≥ 2`. | — | **No** — (T2′) §3.2 needs "a zero", and Hurwitz counts multiplicity; `≥ 2` suffices for the conclusion "`Z_{G_q}` has ≥ 1 zero in `D(s_∞,r)`". |

**One genuine mathematical caution, recorded.** §2.2's source applies the theorem to `Γ₀(4)`, which
is torsion-free; §2.3's source states the divisor for groups with elliptic points but leaves item 6's
multiplicity implicit; §2.5's source covers ramification points and gives the functional equation but
does not itself state the divisor. **No single retrieved source does all three at once.** The
conclusion is safe because the three overlap pairwise and Route B is self-contained given (2.6) —
but that is the honest shape of the evidence, and it is why V1 is worth someone's afternoon.

---

## 7. What this note claims and does not claim

**Claims.**
(i) Theorem U3 is a citable classical theorem, quoted verbatim from a peer-reviewed source with the
multiplicity attached (§2.2), corroborated by a full divisor list valid for groups with elliptic
points (§2.3) and by a torsion-free divisor theorem (§2.4).
(ii) The functional equation `M1F` §5.2 assumed the shape of is exhibited in closed form for
cofinite orbifolds with cusps and ramification points (§2.5) — **`M1F` obligation N2 is discharged
in content** — and from it Theorem U3 is **derived** (§2.6), independently of (i).
(iii) `Z_{Γ_θ}` has a zero at `s_∞ = ρ₁/2` of order `2m(ρ₁) ≥ 2`, `= 2` given `ρ₁` simple; the whole
`Re s = 1/4` family `{ρ/2}` likewise (§3.4). **Obligation U3 / C14 / G6 is discharged.**
(iv) Every cancellation channel is excluded, with the half-integer/trivial-divisor exclusion made
explicit via `Im s_∞ = 7.0673625708… ≠ 0`, and with the observation that `Z_Γ` is pole-free off the
real axis so that no coincident pole exists to cancel against (§3.5).
(v) The `G_q` version needs **no per-`q` input** and is pure citation (§4).
(vi) Side correction: the `Re s = 0` poles of `det Φ_θ` are **simple**, not double (§3.7).

**Does not claim.**
No novelty for anything in §2 — the divisor of the Selberg zeta of a cofinite group is 1980s
classical (V4). No theorem number is asserted from a book I did not open; V1–V3 are carried openly.
Nothing is claimed about the *location* of poles of `φ_q` for non-arithmetic `q` (U3.19, `GAP`, and
off-route). No progress on U1, U2b, U4 or U5 — those are untouched. No certificate; §3.6 is
float/mpmath, no interval arithmetic. No claim that `Z_{Γ_θ}`'s zero at `s_∞` says anything about
any finite `q` on its own — that is the Hurwitz step, and it is U1's problem.

**A refutation was actively sought.** The failure modes checked were: (a) a normalisation mismatch
between the repo's `φ_{ab}` convention and the literature's — checked term by term, §1, **matches**;
(b) the theorem applying only to torsion-free groups, which would have excluded `Γ_θ` outright —
this **is** a real hazard for §2.4 and it is why §2.3/§2.5 were sought; (c) the conjugate point
`1 − β̄` being a different point from the one T1 certified — checked in closed form and numerically,
§3.3/§3.6, and `det Φ_θ` **does** have the matching order-2 zero there; (d) a trivial-divisor
collision at `s_∞` — excluded, §3.5. One thing **was** refuted: T1 §4.4's order-2 claim for the
`Re s = 0` poles (§3.7).

---

## References

**[CITATION, read]** R. W. Bruggeman, M. Fraczek, D. Mayer, *Perturbation of zeros of the Selberg
zeta-function for `Γ₀(4)`*, **Experimental Mathematics 22 (2013) 217–242**; arXiv:1201.2324v1.
§3.4, p. 41 — the transport statement, quoted verbatim in §2.2. Attributes it to Hejhal LNM 1001,
Ch. X, Thm 5.3, p. 498.

**[CITATION, read]** J. S. Friedman, J. Jorgenson, L. Smajlović, *Super-zeta functions and
regularized determinants associated to cofinite Fuchsian groups with finite-dimensional unitary
representations*, **Lett. Math. Phys. 111 (2021), art. 15**; arXiv:2011.12795v1. §2.4–2.5, pp. 6–7 —
the divisor of `φ(s)` and the 7-item divisor of `Z(s)`, quoted verbatim in §2.3. Attributes to
Venkov 1990 p. 49 and Hejhal vol. II p. 499.

**[CITATION, read]** L.-P. Teo, *Ruelle zeta function for cofinite hyperbolic Riemann surfaces with
ramification points*, **Lett. Math. Phys. 110 (2020) 61–82**; arXiv:1901.07898v2. Thm 2.2 (p. 6),
Prop. 2.5 and eq. (2.6) (p. 7) — the regularized-determinant factorization and the explicit
functional equation, quoted verbatim in §2.5.

**[CITATION, read]** D. Borthwick, C. Judge, P. A. Perry, *Selberg's zeta function and the spectral
geometry of geometrically finite hyperbolic surfaces*, **Comment. Math. Helv. 80 (2005) 483–515**;
arXiv:math/0310364v2, Thm 1.1 (p. 1) — quoted verbatim in §2.4. **Torsion-free; corroboration only.**

**[CITATION, NOT read — TODO-VERIFY]** D. A. Hejhal, *The Selberg Trace Formula for `PSL(2,R)`*,
vol. 2, Lecture Notes in Mathematics **1001**, Springer, 1983. **Ch. X, Thm 5.3, p. 498** (per
Bruggeman–Fraczek–Mayer); **p. 499** (per Friedman–Jorgenson–Smajlović). Obligation **V1**.
*(This corrects `M1F` §5.1 and the T2 brief, which guessed "ch. 6+" / "ch. 11" — the divisor and
functional equation of `Z_Γ` for cofinite `Γ` are in **Chapter X**, around pp. 498–499.)*

**[CITATION, NOT read — TODO-VERIFY]** A. B. Venkov, *Spectral Theory of Automorphic Functions and
Its Applications*, Mathematics and its Applications (Soviet Series) **51**, Kluwer, Dordrecht, 1990,
**p. 49**. Obligation **V2**.

**[CITATION, NOT read]** J. Fischer, *An approach to the Selberg trace formula via the Selberg
zeta-function*, Lecture Notes in Mathematics **1253**, Springer, 1987. The standard self-contained
development of `Z_Γ` for cofinite `Γ` with elliptic elements and arbitrary multiplier systems;
listed as the natural place to check V1/V2 if Hejhal is unavailable. *(Cited by
Bruggeman–Fraczek–Mayer as their [3].)*

**[CITATION]** W. Müller, *Spectral geometry and scattering theory for certain complete surfaces of
finite volume*, **Invent. Math. 109 (1992) 265–305** — the resonance-theoretic formulation. Named in
`M1F` §5.1; **not** needed for U3 as closed here, and **not** read.

**[CITATION]** R. Phillips, P. Sarnak, *Perturbation theory for the Laplacian on automorphic
functions*, **J. Amer. Math. Soc. 5 (1992) 1–32** — the reason not to expect a closed form for
`φ_q` at non-arithmetic `q` (§4). Not read this session.

**[CITATION, classical]** de la Vallée Poussin / Hadamard (`Re ρ < 1`); van de Lune–te Riele–Winter,
Odlyzko (simplicity and location of the low zeros of `ζ`).

**Parents in this repo:** `lane_g/LAW_ANCHOR_T1_THETA.md` (§4.1–4.3, §5.4, C11–C14);
`lane_g/M1F_EISENSTEIN_DERIVATION.md` (§5.1–5.4, §6 obligations G6/N2);
`lane_g/LAW_T2_DETERMINANT.md` (§3.2, §5.2 obligation U3).

**Probe script (not committed):** `lane_g/law_probes/probe_u3_orders.py`.
