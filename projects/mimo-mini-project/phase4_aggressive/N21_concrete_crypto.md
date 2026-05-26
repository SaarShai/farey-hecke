---
model: mimo-v2.5-pro
max_tokens: 12000
---

# N21 — Concrete cryptographic / signal-processing pipeline from Farey discoveries

We have these tools:
- Farey-based low-discrepancy sequence with D*(F_N) = 1/N − π²/(3N²) + O(1/N³)
- F^prime_N (prime-denominator subset) with D* approximately D*(F_N)/2
- BCZ-density-driven gap statistics (cluster-2, lag-1=+1/2)
- MUSIC L-zero tomography (can be used as deterministic test signal)

## Concrete asks

Design ONE concrete deliverable pipeline. Pick best:

### A. Quasi-Monte Carlo integrator
Use F_N or F^prime_N as low-discrepancy sequence for QMC. Compete with Sobol, Halton, lattice rules. Specific advantage to claim:
- Provable D* asymptotic (not just hand-wavy)
- F^prime_N has half the discrepancy — better convergence
- Deterministic, no random seeds

Provide: target benchmark integral, expected MSE comparison vs Sobol.

### B. Pseudo-random generator
Farey-based PRNG with provable Kuipers-Niederreiter discrepancy. Generates rational numbers with guaranteed equidistribution.

Provide: cryptographic vs statistical use cases.

### C. Test signal for signal-processing
The Riemann zeta zeros and Maass eigenvalues are RIGOROUSLY KNOWN, INFINITE, DETERMINISTIC. Use them as test signals for line-spectral estimation algorithms (MUSIC, ESPRIT, atomic norm minimization). Benchmark library.

Provide: dataset structure, downloadable format, baseline algorithm comparisons.

### D. Verifiable random function (VRF)
Farey sequence values can be used as VRF outputs since each F_N is deterministic. Cluster-2 structure of gaps could serve as commitment binding.

Provide: cryptographic security properties to claim, attack model.

### E. Compressive sensing benchmark
Cluster-size-2 gap distribution is a NEW universality. Could test compressive sensing recovery on signals with this gap structure.

Provide: signal model, recovery algorithm, expected results.

## Pick TOP 2

Pick the 2 most actionable for ~1 month of focused engineering. Specific code paths, baselines, evaluation metrics.

Skip ones that are too vague or already saturated.
