# Experiment — does X(q)=1/λ_q³ bridge to the Hurwitz constant / Lagrange-spectrum bottom?

**Date:** 2026-06-13. **Branch:** `hecke-goalL-2026-06-03`. **Verdict: NO CLEAN RELATION
(negative result, decisive).** The ergodic-optimization ground value / cluster-onset
threshold `X(q)=1/λ_q³` is **not** algebraically tied to the Rosen/Hecke Hurwitz constant
`H(q)` or the bottom of the Lagrange spectrum. Anchors validated; PSLQ rules out hidden
relations. Code: `code/exp_diophantine_bridge.py`, `code/exp_rosen_lagrange_fast.py`.

---

## 1. Literature (exact, cited)

**Hurwitz constant / bottom of the Lagrange spectrum for the Hecke group G_q**
(Rosen λ_q-continued fractions, λ_q = 2cos(π/q)):

- **Haas & Series**, "The Hurwitz constant and Diophantine approximation on Hecke groups",
  *J. London Math. Soc.* (2) **34** (1986) 219–234. Hurwitz constant
  `h'_q = inf_α M(α)`, `M(α)=limsup_n m_n(α)`, `|α − k/m| < 1/(c m²)`:

  > **`h'_q = 2`  (q even);   `h'_q = 2·√(1 + (1 − λ_q/2)²)`  (q odd).**

- **Kim & Sim**, arXiv:2206.05441, "The Markoff and Lagrange spectra on the Hecke group H₄".
  Lagrange number `L_G(ξ)=limsup_M |M⁻¹ξ − M⁻¹∞|` (Euclidean geodesic diameter). Classical
  `L₀` bottom = √5. For H₄ the discrete Markoff part below `2√2` is
  `{√(8 − 2/x²): x∈N} ∪ {√(8 − 4/y²): y∈M}`; the **bottom** is the `y=1` value `√(8−4)=2`
  (next is `√6`), **agreeing with Haas–Series even-q = 2.**

**Anchor (validated symbolically + geometrically):**
- q=3, odd, λ=1 ⇒ `h'_3 = 2√(1+1/4) = √5` (classical Hurwitz). ✓ (sympy exact.)
- Independent geometric check: the axis of the Hecke word `T S T⁻¹ S` has Euclidean geodesic
  diameter **2.2360679… = √5** at q=3 (`numpy`, matches to 7 digits).

## 2. Exact table (sympy; q=3 anchor passes)

| q | parity | λ_q | X(q)=1/λ³ (q≥5) | H(q) Haas–Series | H(q)² |
|---|--------|-----|------------------|------------------|-------|
| 3 | odd  | 1            | (X=2/9; 1/λ³=1)      | √5 = 2.23607 | 5 |
| 4 | even | √2           | (X=√2/8; 1/λ³=√2/4)  | 2            | 4 |
| 5 | odd  | φ=1.61803    | √5−2 = 0.236068      | 2.03615      | 7.5−1.5√5 = 4.1459 |
| 6 | even | √3           | √3/9 = 0.192450      | 2            | 4 |
| 7 | odd  | 1.80194      | 0.170915             | 2.00978      | 4.0392 |
| 8 | even | 1.84776      | 0.158513             | 2            | 4 |
| 9 | odd  | 1.87939      | 0.150644             | 2.00363      | 4.0146 |

Odd-q closed form: **`H² = λ² − 4λ + 8 = (λ−2)² + 4`**. Even-q: `H² = 4` (constant, **λ-independent**).

## 3. Relation tests — all NEGATIVE

**PSLQ multiplicative search** (mpmath dps 50–60), `X^a H^b λ^c`:
- q≥5 (incl. q=6): PSLQ returns **`[1, 0, 3]`** ⇒ `X·λ³ = 1`, **H-exponent = 0**. The
  Hurwitz constant does **not** enter; X relates only to λ (trivially, by definition).
- q=4: PSLQ returns `[1, 4, −3]` ⇒ `X = λ³/H⁴ = √2/8`. **Coincidental** — only because
  `H(4)=2 ⇒ H⁴=16` and X(4) is the *interior* (half) optimum; it is `λ³/16` in disguise.
  q=6 (also H=2) does **not** satisfy `[1,4,−3]` (`λ³/16 = 0.325 ≠ 0.192`); PSLQ gives `[1,0,3]`.
- `pslq(log X_u, log H)` with λ forbidden: **None** for q=5,7,9,11 ⇒ X is not any clean
  power of H.

**Per-q additive** `pslq(X, H², 1)`:
- q=5: `[3, 2, −9]` ⇒ `X = 3 − ⅔H²` (golden-field accident). q=7,9,11: **None**. Not a family law.

**Uniform-law scan** `X_u(q)·H(q)^k` across q∈{5,7,9,11}, all k∈[−3,3]:
relative spread stays **0.48–0.60** for every k (a real identity ⇒ spread ≈ 0). **No k uniformizes.**

**Eyeballed combos** (all q-dependent, none constant): `H²/λ³` = 5.00, 0.98, 0.69, 0.61, 0.57
(strictly ↓; the "5" at q=3 is the λ³=1 artifact). `X·H` = 0.50, 0.35, 0.48, 0.38, … (non-monotone).

## 4. Numerical Lagrange machinery — validated, anchor-confirmed

- Classical Lagrange-number formula `L(α)=limsup_n([a_{n+1};…]+[0;a_n,…,a_1])` validated on
  periodic CFs: golden [1,1,…]→2.285→√5 (tail-truncated), [2,2,…]→2.831≈2√2=√8, [1,2]→3.10≈√(221)/5.
  **Bottom = golden = √5 confirmed.** (Random-α sampling can't hit the measure-zero
  badly-approximable points — expected, not a bug; the spectrum bottom is realised by
  periodic small-digit points, which Haas–Series pin exactly.)
- Geodesic-diameter route: word `TST⁻¹S` axis diameter = √5 at q=3 (anchor ✓); = √6 at q=4,
  √7 at q=6 (these are *upper* words, not the minimal H-S geodesic for q>3, but confirm the
  geometric normalization).

## 5. Why the bridge fails (the honest mechanism)

`H(q)` and `X(q)` live in **incompatible normalizations**:

- `X(q)=1/λ_q³` is a **denominator-product (gap-product)** quantity, scaling as `λ⁻³`,
  strictly decreasing in q, in the field `Q(λ_q²)`-flavoured tower.
- `H(q)` is a **hyperbolic-geometry / Euclidean-geodesic-diameter** quantity. By the
  Haas–Series theorem it **saturates at 2 for every even q** — it is *identically
  λ-independent on the even side* — and on the odd side it depends on λ only through the
  bounded combination `(λ−2)²+4 ∈ (4,5]`, tending to 4 as λ→2. It therefore **cannot
  track** the monotone `1/λ³`.

So the natural Diophantine "Hurwitz/Lagrange bottom" of the Hecke group is the **wrong
invariant** to meet the ergodic-optimization ground value. The gap-product P is a
*pair-of-consecutive-denominators* observable (large-deviation / extreme-gap object); the
Hurwitz constant is a *single-orbit limsup approximation rate*. They are genuinely different
functionals of the same dynamics, and the data says they do not coincide up to algebra.

**One real (but shallow) identity worth recording:** the *interior-vs-cusp* split at q=4,
`X(4)=√2/8 = λ³/16 = λ³/H(4)⁴`, and the even-q saturation `H≡2`, together explain why q=4
*looked* special in earlier notes — it is the unique even-q where the interior optimum is
exactly `λ³/H⁴`. This does not generalize.

## 6. Verdict for the scout

**DROP as a bridge.** This is a clean *negative* result: it closes a natural-looking
conjecture (ergodic-opt ground value ↔ Diophantine Hurwitz/Lagrange bottom) with both
anchor-validated literature values and PSLQ non-existence evidence. Mild publishable value
as a "these two extremal constants of the Hecke family are unrelated" remark inside a larger
paper, but **not** a standalone breakthrough and **no** application leverage. The `1/λ³`
cube remains unexplained by Diophantine approximation; its meaning (if any) is internal to
the BCZ/ergodic-optimization side, not the continued-fraction side.

## 7. Reproducibility
- `code/exp_diophantine_bridge.py` — exact X(q), H(q), relation battery, q=3 anchor assert.
- `code/exp_rosen_lagrange_fast.py` — float64 Rosen λ_q-CF estimator (machinery; spectrum
  bottom realised by periodic points, not random α).
- PSLQ + uniform-scan: inline (mpmath dps 50–60), reproduced in this note's §3.
