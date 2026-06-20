# Minimal polynomials of `2·cos(π/n)` — toward a Mathlib contribution

Sorry-free Lean 4 / Mathlib proofs that `λ_n = 2·cos(π/n)` satisfies its monic
integer minimal polynomial, for `n = 5, 7, 9`. Proofs collected in
[`Lemmas.lean`](Lemmas.lean).

`λ_n = 2·cos(π/n)` is the Hecke triangle-group parameter for `G_n`; these
identities are the per-`n` algebraic facts underlying that work.

---

## The gap in Mathlib

Mathlib has the Chebyshev polynomials of the first kind
(`Polynomial.Chebyshev.T`) and the bridging identity
`Polynomial.Chebyshev.T_real_cos : eval (cos θ) (T ℝ n) = cos (n · θ)`, but it
does **not** have the minimal polynomials of `2·cos(π/n)` (nor of `cos(π/n)` /
`cos(2π/n)`) as named results. This gap is real (no `minpoly` lemma for these
algebraic numbers exists in Mathlib at time of writing; cf. arXiv:2501.16478,
which discusses exactly this family of cyclotomic-derived minimal polynomials).
The lemmas here are concrete `n = 5, 7, 9` instances of that missing family.

---

## The general statement

For an integer `n ≥ 2`, let `λ_n = 2·cos(π/n)`. Then:

* **Degree.** The minimal polynomial of `λ_n` over `ℚ` has degree `φ(2n)/2`,
  where `φ` is Euler's totient. (Verified for the cases here:
  `φ(10)/2 = 2`, `φ(14)/2 = 3`, `φ(18)/2 = 3`, and for the stretch target
  `φ(22)/2 = 5`.)

* **Roots.** Its roots are exactly
  `{ 2·cos(kπ/n) : 1 ≤ k < 2n, gcd(k, 2n) = 1 }`.
  Equivalently, `λ_n = ζ + ζ⁻¹` where `ζ = e^{iπ/n}` is a primitive `2n`-th root
  of unity, so the minimal polynomial of `2·cos(π/n)` is the image of the
  `2n`-th cyclotomic polynomial `Φ_{2n}` under the "trace map"
  `ζ ↦ ζ + ζ⁻¹` (a degree-2 quotient, hence `deg = φ(2n)/2`).

* **Chebyshev factorization (the engine of the proofs).** Since
  `T_n(cos θ) = cos(nθ)`, setting `θ = π/n` gives `T_n(cos(π/n)) = cos π = -1`,
  i.e. with `x = 2·cos(π/n)`, `T_n(x/2) = -1`. The polynomial `T_n(x/2) + 1`
  (degree `n`, leading coefficient `1/2`) factors over `ℚ` as a product of the
  cyclotomic-trace minimal factors; the minimal polynomial of `λ_n` is the
  monic factor having `λ_n` as a root. Concretely, for `n = 7` and `n = 11` the
  factorization is
  `2·(T_n(x/2) + 1) = (x + 2)·(minpoly(x))²`,
  and the cubic / quintic factor is the sought minimal polynomial.

---

## What is proved here (`n = 5, 7, 9`)

| `n` | `λ_n = 2·cos(π/n)` | minimal polynomial | degree `= φ(2n)/2` | lemma | route |
|----:|--------------------|--------------------|:---:|-------|-------|
| 5 | `1.6180339887…` (golden ratio) | `x² − x − 1` | 2 | `two_cos_pi_div_five_min_poly`  | `Real.cos_pi_div_five` + `(√5)²=5` |
| 7 | `1.8019377358…` | `x³ − x² − 2x + 1` | 3 | `two_cos_pi_div_seven_min_poly` | Chebyshev `T₇`, factor `(x+2)·(·)²` |
| 9 | `1.8793852416…` | `x³ − 3x − 1` | 3 | `two_cos_pi_div_nine_min_poly`  | triple-angle `Real.cos_three_mul` |

Each lemma states `p(2·cos(π/n)) = 0` for the monic integer polynomial `p`
above. All three are sorry-free; as machine-checked by the Aristotle Lean prover
the proofs depend only on the standard axioms `propext`, `Classical.choice`,
`Quot.sound`.

> **Scope / honesty.** These lemmas prove that `λ_n` is a **root** of the stated
> polynomial (`p(λ_n) = 0`). They do **not** yet prove that `p` is the
> **minimal** polynomial (irreducibility over `ℚ` + `minpoly ℚ λ_n = p`). For
> `n = 5, 7, 9` the stated `p` is in fact irreducible over `ℚ` (degree ≤ 3 with
> no rational root, by the rational-root test), so "root of `p`" plus "`deg p`
> matches `φ(2n)/2`" pins it down; but the irreducibility/`minpoly` half is not
> formalized in this file. A Mathlib-grade contribution should add that half
> (see below).

---

## What a general-`n` Mathlib lemma would need

A reusable Mathlib contribution (rather than three hand-instances) would aim at:

1. **A `λ_n` ↔ Chebyshev evaluation lemma**, e.g.
   `eval (2·cos(π/n)) (T ℝ n) = -1` (have:
   `Polynomial.Chebyshev.T_real_cos` already gives the half-step), and a clean
   `x = 2c` rescaling so the relation is stated on `λ_n` directly rather than on
   `c = cos(π/n)`. This removes the per-`n` recurrence-unfolding seen in the
   `n = 7` proof.

2. **The cyclotomic-trace bridge.** Connect `2·cos(π/n) = ζ_{2n} + ζ_{2n}⁻¹` to
   Mathlib's cyclotomic machinery (`Polynomial.cyclotomic`,
   `IsPrimitiveRoot`, `IsCyclotomicExtension`). The minimal polynomial of
   `ζ + ζ⁻¹` over `ℚ` is the "real cyclotomic" / minimal polynomial of
   `2cos`, sometimes denoted `Ψ_{2n}`. Mathlib already proves
   `cyclotomic n` is the minimal polynomial of a primitive root
   (`Polynomial.cyclotomic_eq_minpoly` / `IsPrimitiveRoot.minpoly_eq_cyclotomic`);
   the missing piece is the **degree-2 descent** to the maximal real subfield
   (`minpoly` of the trace).

3. **The degree formula** `natDegree (minpoly ℚ (2·cos(π/n))) = φ(2n)/2`,
   following from (2) and `Polynomial.natDegree_cyclotomic = φ(2n)`.

4. **The root set** `{2·cos(kπ/n) : gcd(k,2n)=1}` as the roots, with
   irreducibility over `ℚ` (the harder half), giving
   `minpoly ℚ (2·cos(π/n)) = Ψ_{2n}`.

The lemmas in this file are the verified `n = 5, 7, 9` base cases / sanity
anchors for such a general development; the `n = 7` proof in particular
demonstrates the Chebyshev-`T`-recurrence route that a general lemma would
abstract.

---

## Stretch target: `n = 11`

Numerically derived and falsify-checked (see the report): the minimal polynomial
of `2·cos(π/11)` (degree `φ(22)/2 = 5`) is

```
x⁵ − x⁴ − 4x³ + 3x² + 3x − 1
```

with `2·cos(π/11) ≈ 1.9189859472`, and its five real roots are exactly
`2·cos(kπ/11)` for `gcd(k,22)=1` (`k = 1,3,5,7,9`). It satisfies the same
Chebyshev factorization shape as `n = 7`:

```
2·(T₁₁(x/2) + 1) = (x + 2)·(x⁵ − x⁴ − 4x³ + 3x² + 3x − 1)²
```

(verified symbolically; the quintic divides `T₁₁(x/2)+1` with zero remainder).
Whether the Lean proof for `n = 11` was completed is recorded in the run report
— if proved sorry-free it is added to `Lemmas.lean`, otherwise only `n = 5,7,9`
ship and `n = 11` remains numerically derived but not formally verified.

---

## Provenance

Proofs produced and verified sorry-free via the Aristotle Lean prover
(toolchain `leanprover/lean4:v4.28.0`, recent Mathlib). Sources consolidated
from `projects/aristotle_minpoly_lambda/solution/Main.lean` (`n = 5, 7`) and
`engine/demos/d_d_fresh_verify/aristotle_lambda9/.../RequestProject/Main.lean`
(`n = 9`). The numeric derivation / falsification of the `n = 11` minimal
polynomial used `sympy` (exact `minimal_polynomial`) cross-checked against a
floating-point root evaluation.
