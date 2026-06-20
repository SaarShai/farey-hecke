# Lean-prep: minimal polynomial of λ_7 = 2 cos(π/7)  (Aristotle-ready)

This is a **prepared Lean statement** (the main loop should lift it into a
`projects/...` RequestProject dir and submit to Aristotle — this subagent's
write paths do not include `projects/`, so the statement is staged here).

## Statement to prove (sorry-free target)

```lean
lemma lambda_7_min_poly :
    let x : Real := 2 * Real.cos (Real.pi / 7)
    x^3 - x^2 - 2*x + 1 = 0 := by
  sorry
```

- Numerically verified this session: `2*cos(pi/7) = 1.8019377358048383`, and
  `x^3 - x^2 - 2x + 1 = 0.0` (float). (The other sign convention
  `x^3 + x^2 - 2x - 1` is the minpoly of `2cos(2π/7)`, ≠ 0 here = 4.49.)
- λ_7 is the Hecke parameter whose G_7 surface carries the certified odd Maass
  eigenvalue r* = 5.921981251 (this session). The cubic is the algebraic
  foundation (κ, the Markov-partition CF values, the disc geometry) of that
  certified computation.

## Proof recipe (DIRECTLY adapted from the PROVEN n=11 quintic)

The repo already has `lambda_11_min_poly` PROVED sorry-free (Aristotle-verified,
commit a728961, `projects/mathlib_2cos_minpoly/aristotle_lambda11/.../Main.lean`).
The n=7 cubic is the strictly easier sibling — same template:

1. Set θ := π/7, c := cos θ, x := 2c.
2. Chebyshev key identity (here T_7): cos(7θ) = cos(π) = −1, i.e.
   `64 c^7 − 112 c^5 + 56 c^3 − 7 c = −1`, i.e.
   `64 c^7 − 112 c^5 + 56 c^3 − 7 c + 1 = 0`.
   Obtain via `Polynomial.Chebyshev.T` eval recurrence
   (`Polynomial.eval c (Chebyshev.T ℝ 7) = Real.cos (7 * θ)`), as in the n=11 proof.
3. Factor: `64c^7 − 112c^5 + 56c^3 − 7c + 1 = (2c+1)·(c³ − ... )`-style. In terms
   of x = 2c the degree-7 cosine identity factors through the **cubic**
   `x³ − x² − 2x + 1` (the primitive factor, since cos(7θ)=−1 has the 14th roots
   of unity as solutions and 2cos(π/7) is a primitive one). Discharge the final
   `x³ − x² − 2x + 1 = 0` by `nlinarith` using `0 < cos(π/7)` (so the spurious
   `(2c+1)` factor is nonzero), exactly the closing move of the n=11 proof:
   `sq_eq_zero_iff.mp (by nlinarith [Real.cos_pos_of_mem_Ioo ...])` — but here it
   is a single linear/cubic elimination, not a square.

## Why this is high-confidence Aristotle-closable

- It is a *lower-degree instance of an already-machine-verified lemma family*
  (n=11 quintic done; n=7 cubic is easier — fewer Chebyshev terms, primitive
  factor is a cubic not a quintic).
- The whole `set_option` preamble + `import Mathlib` + Chebyshev recurrence
  scaffold transfers verbatim from the n=11 `Main.lean`.

## Honesty

This Lean lemma is the **algebraic substrate** of the G_7 result, NOT a Lean
proof of the Maass eigenvalue itself (the eigenvalue claim is an Arb interval
certificate — `winding = 1` — which is numeric-certified, not Lean-proved; that
distinction is preserved throughout the package note).
