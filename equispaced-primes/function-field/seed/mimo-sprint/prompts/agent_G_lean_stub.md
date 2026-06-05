---
agent: G
day: 2
purpose: Lean4 stub theorem for unconditional D2 result (q=2, M=T^3, A=1)
---

# Agent G — Lean4 stub for D2 unconditional theorem

## Context

The cleanest D2 case — (q=2, M=T³, A=1 trivial unit class) — should be statable in Lean4 as a `theorem … := sorry` against the in-repo mathlib. The repo has a `primes-equispaced/` Lean4 project (mathlib pinned, vendored at `primes-equispaced/.lake/packages/mathlib/`).

Statement (English, prior to Lean):

  Let K = F₂(T)(ζ_{T³}) be the (T³)-th cyclotomic function field over F₂(T). Let G = (F₂[T]/T³)*. Let π_{1/2,K}(2ⁿ) = Σ_{P irreducible monic ≤ deg n} 2^{−deg P / 2}. Let π_{1/2}(2ⁿ; T³, 1) = Σ_{P irr, deg ≤ n, P ≡ 1 mod T³} 2^{−deg P / 2}. Then:

      lim_{n→∞} [ π_{1/2,K}(2ⁿ) − 4 · π_{1/2}(2ⁿ; T³, 1) − (1/2) log n ] = c

  for some constant c, **unconditionally**, by AK Theorem 3.4 + Kaneko–Koyama–Kurokawa DRH-over-function-fields.

## Your task

1. **Write a `.lean` file** at `projects/ak-bias-followups/mimo-sprint/results/agent_G_D2_stub.lean` containing:
   - imports of relevant mathlib parts. Confirmed available in pinned mathlib:
     - `Mathlib.NumberTheory.FunctionField` (file: `Mathlib/NumberTheory/FunctionField.lean`)
     - `Mathlib.NumberTheory.LSeries.*` (subdir `Mathlib/NumberTheory/LSeries/`)
     - `Mathlib.NumberTheory.Cyclotomic.*` (subdir `Mathlib/NumberTheory/Cyclotomic/`)
     - `Mathlib.NumberTheory.DirichletCharacter` (subdir)
     - `Mathlib.NumberTheory.ClassNumber.FunctionField`
   - definitions for π_{1/2,K} and π_{1/2}(·; M, A) over function fields. Use `Polynomial (ZMod 2)` for F_2[T] and `Polynomial.irreducible_iff_prime` / related lemmas for the irreducibility predicate.
   - the main theorem statement, body = `sorry`
   - a comment block citing AK Thm 3.4 and KKK DRH

2. **Make it type-check** modulo `sorry`. The file should compile under the in-repo mathlib. To verify, propose the exact `lake build` command from inside `primes-equispaced/`.

3. **Identify gaps in mathlib.** If a needed definition (e.g. cyclotomic function field, function-field L-series) doesn't exist in the pinned mathlib, list it as a prerequisite lemma — with a Lean4 sketch — that would need to land before the main theorem.

## Output format

```json
{
  "lean_file_path": "projects/ak-bias-followups/mimo-sprint/results/agent_G_D2_stub.lean",
  "lean_file_contents": "<full file as a string>",
  "build_command": "cd primes-equispaced && lake build AK.D2.Stub",
  "expected_compile_status": "compiles modulo `sorry`",
  "mathlib_gaps": [
    {"missing": "<symbol/def>", "sketch": "<Lean4 def sketch>", "blocks_compile": true | false}
  ],
  "main_theorem_signature": "theorem AK_D2_T3_trivial_class : ...",
  "uncertainty_flags": ["<anything you're not sure compiles>"]
}
```

## Norms

- Pinned mathlib may or may not have function-field L-series. If it doesn't, write the prerequisite definitions and don't pretend they exist.
- The goal is a well-typed *statement*, not a proof. `sorry` body is acceptable everywhere.
- Don't import everything; minimize the import list to what's actually used.
- If you can't get even the statement to type-check, output the cleanest approximation + a list of what's missing.
