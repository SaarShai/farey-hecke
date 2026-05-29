# Koyama absolute-zeta function ↔ q*_BCZ: rigorous hunt

**Date:** 2026-05-27
**Status:** **NO CONNECTION FOUND** (with structural reason). Plausibility revised
65% → ≲ 5%.

## 0. Target constant

The BCZ-cluster threshold is
```
q*_BCZ = (11 − 8·ln(3/2)) / 9 ≈ 0.86180879279274277…
I       = (8·ln(3/2) − 2) / 9 ≈ 0.13819120720725722…   (q* = 1 − I)
```
where `I` is the integral of `2·𝟙_{x+y>1}` over `{xy < 2/9}` inside the open
unit square — the BCZ-cluster mass below threshold. The two are interchangeable
under PSLQ; we test `I` because the integer-relation structure is cleaner.

## 1. What absolute zeta functions actually are

From Kurokawa, *Absolute zeta functions*, Proc. Japan Acad. 81A (2005) and
Deitmar–Koyama–Kurokawa (DKK), *Counting and zeta functions over F₁*, Abh. Math.
Sem. Univ. Hamburg 85 (2015) doi:10.1007/s12188-015-0104-3, the construction is:

> Given a counting function `N : (1,∞) → ℂ` of the form
> `N(u) = Σ_α m(α) u^α` (finite sum, α ∈ ℚ_{≥0}, m(α) ∈ ℤ),
> define
> `Z_N(w, s) = Σ_α m(α) (s − α)^{−w}`,
> `ζ_N(s) = exp(∂_w Z_N(w, s) |_{w=0}) = ∏_α (s − α)^{−m(α)}`.

So for a finite-type monoid (F₁) scheme:

- `ζ_{𝔸¹}(s) = (s−1)⁻¹` (single exponent α=1, m=1)
- `ζ_{𝔾ₘ}(s) = (s−1)/s`
- `ζ_{ℙ¹}(s) = 1 / [s(s−1)]`
- `ζ_{ℙⁿ}(s) = 1 / ∏_{k=0}^{n} (s−k)`
- More generally for any monoid scheme of finite type, `ζ_X(s)` is a rational
  function of `s` with integer exponents.

### Where transcendentals enter

`ζ_N` itself is *rational* at integer s. Transcendentals only appear in
**derivative values** `(d/ds) log ζ_N(s) |_{s=k}`:
```
(log ζ_N)'(k) = − Σ_α m(α) / (k − α)
ζ_N'(0) / ζ_N(0)-style values give    Σ m(α) log(−α)  (regularised)
```
The transcendentals are **logarithms of the exponents α appearing in the
counting polynomial**. For a monoid scheme of finite type with α ∈ ℤ_{≥0},
these are logs of integers — never `log(3/2)` *directly* (you'd need
a ratio of differences `(k−α₁)/(k−α₂) = 3/2`, e.g., (5−2)/(4−2), but the
resulting coefficient structure is rigid).

References:
- arXiv:0805.4286 — DKK, *Counting functions and multiple zeta values via F₁*
- arXiv:1304.2472 — Kurokawa–Ochiai, *Dualities for absolute zeta functions*
- arXiv:2308.03232 — Koyama–Kurokawa, *Absolute zeta functions arising from
  ceiling and floor Puiseux polynomials*
- arXiv:2012.10486 — *Absolute Euler product representation* (Noetherian F₁-schemes)

## 2. PSLQ search (decisive negative)

**Setup:** `mpmath`, precision 100 decimal digits, `maxcoeff` up to 10⁸,
tolerance 10⁻⁷⁰ to 10⁻⁸⁰. Test whether `I` lies in the ℚ-span of a basis
*beyond* the trivial `{1, ln 2, ln 3}` decomposition.

**Basis tested (singletons + pairs added to {1, ln 2, ln 3}):**
```
ln 5, ln 7, log(2π), γ (Euler), G (Catalan), ζ(3), π²/6, π,
Li₂(1/2), Li₂(1/3), Li₂(2/3), Li₂(1/9), Li₂(2/9), Li₂(−1/2), Li₂(−1), Li₃(1/2),
log Γ(3/2)
```

**Result.** The **only** integer relation found is the definitional one,
`9·I + 2 + 8·ln 2 − 8·ln 3 = 0`, equivalently
`9·q* − 11 + 8·ln 2 − 8·ln 3 = 0`.

No non-trivial relation involves any element of the augmented basis (coefficient
on every extra constant comes out zero). One spurious hit appeared from PSLQ
returning a relation with `0` coefficient on `I` itself — when checked
symbolically (`2 ln 3 − ln π + 2 log Γ(3/2) ≡ 0`) it reduces to `2 ln(3/2) = 0`,
which is false; that is a known PSLQ artefact (relation among the auxiliary
constants only, not involving the target). Discarded.

This rules out, at confidence ≈ 100% within the basis, that `q*_BCZ` is a
ℚ-linear combination of standard absolute-zeta-derivable constants
(logs of primes ≤ 7, log 2π, γ, π², ζ(3), Catalan, low-order polylogs at small
rational arguments, log-gamma at half-integers).

## 3. Structural reason it cannot match a finite-type F₁ absolute zeta

The factor `1/9` and weight `8` in `(11 − 8·ln(3/2))/9` carry information.

For a finite-type monoid scheme with counting polynomial
`N(u) = Σ m_α u^α` (m_α ∈ ℤ, α ∈ ℤ_{≥0}), the derivative-value
`(log ζ_N)'(k) = −Σ m_α/(k − α)` at integer `k` is a **rational** sum with
denominator dividing `∏(k − α)`. A `log 3 − log 2` contribution requires a
*log-derivative* term, i.e., evaluation strictly *at* an `α` (residue), which
gives `m_α · log` of the multiplicity — not of a ratio. To force the ratio
`3/2` to appear with multiplicity 8 *and* an outer factor `1/9`, you would
need a scheme whose counting polynomial has exponents `α` arranged so that
`(s−α₁)/(s−α₂) = 3/2` at some integer `s`, multiplicity 8, and a residue
denominator producing `1/9`. Working through small cases (`α ∈ {0,1,2,…,9}`,
m ∈ {−2,…,2}) systematically fails: either the multiplicity vector cannot
deliver coefficient 8 without also contributing other primes (5,7) to the
log basis, or the outer denominator is wrong.

Symbolically: the trivial relation `9·I = 8·ln 3 − 8·ln 2 − 2` has all four
small-integer coefficients sharing **no** common F₁-counting-polynomial origin.
The `−2` constant term (rational, non-zero) is also a red flag: monoid-scheme
ζ′(0)-style values give purely log-transcendental terms — rational constants
come from `ζ(0)` itself, which would have to add an *integer* (the
`−χ_top(X)` style) and contradicts the explicit `−2/9`.

## 4. Why the original 65% intuition fails

The 65% was based on three soft cues:
1. `q*_BCZ` is a closed-form transcendental with `ln(3/2)` — feels "special".
2. Absolute zeta functions are a natural F₁ object on `SL(2,ℤ)\ℍ`.
3. The BCZ triangle is a fundamental-domain piece, plausibly an F₁-scheme.

Each cue weakens on examination:
1. `ln(3/2)` is generic — it arises whenever you integrate `dx/x` from 2 to 3
   (which is exactly what the BCZ-triangle integral does in computing the mass
   over `xy < 2/9`). It is **not** a marker of F₁ structure.
2. The natural F₁-scheme on `SL(2,ℤ)\ℍ` is the modular curve `Y(1)`; its
   absolute zeta has been studied (Manin, Soulé, Connes–Consani) and its
   special values involve `log 2π`, `γ`, modular discriminant — **not** the
   specific BCZ triangle integral.
3. The BCZ triangle is **not** an F₁-subscheme in any natural way — it is a
   real semi-algebraic piece carved out by the inequality `xy < 2/9` inside
   `[0,1]²`. The cut `xy < 2/9` has no F₁-interpretation; `2/9` is a
   real-analytic threshold from the BCZ three-distance density, not a count
   over `𝔽_q`.

## 5. Verdict

**NO CONNECTION.** `q*_BCZ` is what it appears to be: an elementary
transcendental obtained by Lebesgue integration of `2·𝟙_{x+y>1}` over
`{xy < 2/9} ∩ [0,1]²`. The `ln(3/2)` factor is generic (antiderivative of
`dx/x` over `[2/3, 1]`-style intervals), and the prefactor `1/9` traces back
to the specific BCZ-three-distance density level `2/9`, not to any
zeta-functional special value.

There is no avenue to re-cast `q*_BCZ` as

- ζ_X(k) for any natural F₁-scheme X,
- a Kurokawa derivative `ζ_X'(0)` for X of finite type,
- a multiple zeta value or polylog at a small rational argument,
- a Stieltjes constant or `Γ`-special-value combination,

within the integer-relation reach tested (maxcoeff 10⁸, prec 100 dps,
13-constant augmented basis).

## 6. Action for the paper

- **Do not** claim a Koyama/absolute-zeta connection.
- **Do not** cite DKK or Kurokawa absolute-zeta references in support of
  `q*_BCZ`.
- The threshold `q*_BCZ` should be presented as what it provably is: the
  closed-form result of an explicit Lebesgue integral over the BCZ
  three-distance density support. This is already its strongest framing.
- If a structural-zeta connection is ever to be made for the broader BCZ /
  Farey program, the natural target is the **Selberg zeta of `SL(2,ℤ)\ℍ`**
  (real-analytic, classical) rather than the F₁ / absolute zeta family —
  but that is a separate hunt and outside this note's scope.

## 7. Reproducibility

PSLQ script (mpmath ≥ 1.3): the `python3` blocks in this session at
prec=100 dps, maxcoeff ∈ {10⁶, 10⁸}. Trivial relation
`[9, 2, 8, −8]` confirms `9·I + 2 + 8·ln 2 − 8·ln 3 = 0`. All
augmented-basis singleton and pair tests return `None` or relations with
zero coefficient on `I`.

---

**Bottom line.** Plausibility revised from 65% to ≲ 5%. The hand-wave is
killed by both (a) explicit PSLQ search up to integer-relation coefficient 10⁸
in a generous transcendental basis, and (b) structural incompatibility of the
prefactor/multiplicity pattern with finite-type monoid-scheme absolute zetas.
