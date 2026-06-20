# Aristotle task: certified spectral-gap inequality for the Rosen/Hecke transfer operator

## What to prove (plain words)

`RequestProject/Main.lean` contains three lemmas in namespace `EquidistGap`.
They are ALREADY proved sorry-free and were verified locally against Mathlib
`v4.28.0` (axiom-clean: `[propext, Classical.choice, Quot.sound]`). The task for
Aristotle is to **confirm they build sorry-free** and, if any proof step is
brittle on your toolchain, **repair it** while keeping the statements verbatim.

The three statements:

1. `gap_q5_ge` — Given certified eigenvalue-modulus bounds for the `q = 5`
   Rosen/Hecke transfer operator at `s = 1`
   (`0.9999999999 ≤ |λ₁| ≤ 1`, `0 ≤ |λ₂| ≤ 0.2025127171`),
   the spectral gap satisfies `1 - |λ₂|/|λ₁| ≥ 0.79`.

2. `gap_q7_ge` — Same shape for `q = 7`
   (`0.999999999998 ≤ |λ₁| ≤ 1`, `0 ≤ |λ₂| ≤ 0.3406773837`):
   `1 - |λ₂|/|λ₁| ≥ 0.65`.

3. `decay_of_correlations` — For `0 ≤ ρ ≤ 1 - gap`, the `n`-step correlation
   factor obeys `ρ^n ≤ (1-gap)^n` (monotonicity of `pow`).

`l1`, `l2` are real variables standing for `|λ₁|`, `|λ₂|`; the numeric bounds
enter as hypotheses.

## Why these bounds are the inputs (provenance)

The modulus enclosures are NOT asserted by fiat — they come from an external
**certified** computation (python-flint Arb-ball arithmetic, Rump-verified ball
eigensolver `acb_mat.eig(algorithm="rump")`) on the finite-N nuclear truncation
of the MMS transfer operator `L_1`:

| q | `|λ₁|` enclosure        | `|λ₂|` enclosure              | certified gap_lo |
|---|-------------------------|-------------------------------|------------------|
| 5 | `[1−1e−13, 1]`          | `[0.202512717, 0.202512718]`  | `0.797487282915` |
| 7 | `[1−2e−12, 1]`          | `[0.340677383, 0.340677384]`  | `0.659322616376` |

(Source: `code/equidist_gap/cert_gap_rosen.py` → `out/cert_gap_rosen.json`.)
The Lean lemmas use slightly LOOSER round rational bounds (`0.79`, `0.65`) so the
arithmetic is robust; tightening to the certified `0.7974…` / `0.6593…` is
optional and also true.

## Acceptance

- `lake build` succeeds, no `sorry`, axioms ⊆ `[propext, Classical.choice, Quot.sound]`.
- Statements unchanged.

## Toolchain

`lean4:v4.28.0`, Mathlib `v4.28.0` (see `lakefile.toml`, `lean-toolchain`).
Key lemmas used: `gcongr` (division monotonicity), `div_le_iff₀`,
`pow_le_pow_left₀`. If a name drifted, substitute the current Mathlib equivalent.
