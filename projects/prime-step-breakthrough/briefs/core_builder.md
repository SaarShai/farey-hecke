---
GOAL: Implement the dependency-light mathematical core for T1--T4 and the coprime-batch optimizer.
ROLE: builder
SCOPE: projects/prime-step-breakthrough/pyproject.toml and projects/prime-step-breakthrough/src/coprimebatch/{__init__.py,arithmetic.py,kernel.py,shear.py,optimizer.py,cli.py}
INPUTS: projects/prime-step-breakthrough/RESEARCH_SPEC.md
NO_TOUCH: tests/, web/, paper/, research/, README.md, verify_all.py, any path outside projects/prime-step-breakthrough/
DELIVERABLE: importable Python 3.11+ package with exact Fraction mode, float mode, deterministic optimizer, and argparse CLI
VERIFY: PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=projects/prime-step-breakthrough/src python3 -m coprimebatch.cli --help; targeted self-checks for K(2,2), K(2,4), p=8501 sign scan, and deterministic optimizer
DONE: all public APIs below exist, self-checks pass, no prohibited paths changed, and final report lists commands/results
---

## Required public API

`coprimebatch.arithmetic`

- `factorint(n: int) -> dict[int, int]`, rejecting `n < 1`
- `mobius(n: int) -> int`
- `totient(n: int) -> int`
- `divisors(n: int) -> list[int]`
- `primes_up_to(n: int) -> list[int]`
- `ramanujan_sum(n: int, k: int) -> int`

`coprimebatch.kernel`

- frozen dataclass `PortfolioCertificate` with denominators, point_count,
  energy (`Fraction | float`), worst_case_error, and factorization_seconds
- `kernel_fraction(m, n) -> Fraction` using the local Euler factors or the
  divisor formula; no point enumeration
- `kernel_float(m, n) -> float`
- `portfolio_certificate(denominators, exact=True) -> PortfolioCertificate`
- `marginal_energy(denominators, candidate, exact=True)`
- `step_coefficient(n) -> Fraction` for a(n)
- `step_summatory(x) -> Fraction`
- `prime_energy_delta(p) -> Fraction` with primality validation
- `first_negative_prime_delta(limit) -> tuple[int, Fraction] | None`

`coprimebatch.shear`

- `triangular_even_moment(r) -> Fraction`
- `farey_shift_moments(p, max_order=6, exact=False) -> dict`, using the fixed
  interior convention and rejecting non-prime p
- `farey_interior_count(p) -> int`
- `weyl_sum(p, h, ell) -> int` via Ramanujan sums
- `weyl_bound(p, h, ell) -> int`; resonance must be explicit, never hidden

`coprimebatch.optimizer`

- frozen dataclass `OptimizationResult`
- `greedy_portfolio(candidates, layers, exact=False) -> OptimizationResult`
- `largest_totient_baseline`, `consecutive_high_baseline`, and
  `random_portfolio_baselines(candidates, layers, samples, seed)`
- `bruteforce_optimum(candidates, layers, exact=False)` for small pools
- `benchmark_case(start=2, stop=200, layers=10, seed=20260715)` returning a
  JSON-serialisable evidence dictionary

`coprimebatch.cli`

- subcommands `certificate`, `optimize`, `shift`, `prime-delta`, `benchmark`
- `--json` output; invalid inputs return nonzero with a concise error

Keep algorithms clear and independently testable.  Do not assert novelty in
docstrings.  Preserve exact arithmetic until callers request floats.
