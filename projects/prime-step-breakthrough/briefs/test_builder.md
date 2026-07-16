---
GOAL: Build an independent falsification-first test, benchmark, and one-command verification suite for the frozen core API.
ROLE: verifier-builder
SCOPE: projects/prime-step-breakthrough/tests/, projects/prime-step-breakthrough/benchmark.py, projects/prime-step-breakthrough/verify_all.py
INPUTS: RESEARCH_SPEC.md and briefs/core_builder.md; assume the frozen API exactly
NO_TOUCH: src/, web/, paper/, research/, README.md, any path outside projects/prime-step-breakthrough/
DELIVERABLE: unittest-based suite with no third-party test dependency, machine-readable benchmark artifact generation, and a root verify_all.py
VERIFY: PYTHONDONTWRITEBYTECODE=1 python3 projects/prime-step-breakthrough/verify_all.py
DONE: independent direct oracles test every mathematical formula, preregistered gates are encoded, negative controls are retained, no prohibited path changed, and final report lists failures honestly
---

Required independent checks:

1. Direct piecewise-`Fraction` integration of primitive-layer step functions
   versus `kernel_fraction` for every pair 2..30.
2. Divisor-sum and local-factor kernel implementations cross-check (the oracle
   must not simply call the production function).
3. Direct node enumeration versus portfolio certificate for fixed and seeded
   random portfolios.
4. Gram quadratic forms nonnegative on seeded integer coefficient vectors.
5. Prime energy delta formula versus direct kernel sums for small primes;
   exact scan proving first negative delta is p=8501.
6. Divisor-portfolio identity reconstructing a uniform grid.
7. Direct Ramanujan/Weyl sums for small p and frequencies, including an
   explicit resonance test outside the ETK cutoff.
8. Exact odd moments zero and exact even moment enumeration for small primes;
   empirical T2 convergence is evidence, not a theorem test.
9. Optimizer determinism, invalid inputs, brute-force gap on a small pool, and
   the frozen 2..200/10-layer gate.
10. Scaling benchmark with at least one million implicit points; factorisation
    and kernel times reported separately.
11. CLI subprocess smoke tests and JSON schema/value checks.
12. `verify_all.py` runs unit tests, benchmark gates, HTTP tests when present,
    and static checks without writing bytecode/cache into the repo.

Write benchmark evidence under `artifacts/` only at runtime; `verify_all.py`
may create that directory.  Do not weaken a gate to make current code pass.
