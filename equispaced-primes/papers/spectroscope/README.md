# Prime Spectroscopy of Riemann Zeros

**A batch framework for detecting zeros of L-functions using prime-indexed Fourier measurements.**

The Mertens spectroscope detects zeros of the Riemann zeta function — and any L-function with an Euler product — by analyzing weighted sums over primes. Three theorems characterize the framework: unconditional detection, conditional universality, and measurement stability.

## The Method in One Picture

![Method Comparison](hero_comparison.html)

**Classical approach:** Evaluate each L-function individually at thousands of points to find where it vanishes. Cost scales linearly with the number of L-functions in the family.

**Our approach:** Compute a single prime spectroscope. All L-functions in the family are scanned simultaneously via character decomposition. Cost is nearly independent of family size. Approximate zero locations are identified, then refined with classical tools only at flagged spots.

**Result: Same zeros found, fewer computations.**

| Conductor q | Classical cost (all chars) | Spectroscope cost | Speedup |
|------------|---------------------------|-------------------|---------|
| 1,000 | 89M ops | 20M ops | **5x** |
| 10,000 | 2,800M ops | 230M ops | **12x** |
| 100,000 | 89,000M ops | 1,800M ops | **51x** |
| 1,000,000 | 2.8T ops | 20B ops | **141x** |

The advantage grows as √q — the higher the conductor, the bigger the speedup.

---

## Three Theorems

### Theorem 1: Detection (Unconditional)
The spectroscope detects at least one nontrivial zero of ζ(s), regardless of whether the Riemann Hypothesis is true. If RH holds, all zeros are detected. If RH fails, the spectroscope finds the most off-line zero with a signal that grows to infinity.

*No unproved hypotheses required.*

### Theorem 2: Universality (Assuming GRH)
Any subset of primes S with divergent reciprocal sum (Σ 1/p = ∞) detects every zero. You can discard 99.99% of primes and still recover the full zero spectrum. Corollary: primes with bounded gaps ≤ 246 (Maynard-Tao) detect all zeros.

### Theorem 3: Stability (Unconditional)
The Montgomery-Vaughan large sieve inequality guarantees that the spectroscope measurements are numerically stable — bounded noise regardless of how many primes are used.

---

## Applicable L-functions

The framework applies to any L-function with an Euler product over primes.

| L-function | Coefficients at prime p | What zeros reveal | Detection | Batch speedup (est.) |
|-----------|----------------------|------------------|-----------|---------------------|
| **Riemann ζ(s)** | Mertens function M(p) | Prime distribution | ✅ 20/20 zeros, 8.4x peak | — |
| **Dirichlet L(s,χ)** | Twisted Mertens M_χ(p) | Primes in progressions | ✅ Verified (χ₄: 2.8x, χ₋₂₀: 3.8x) | **12x** at q=10⁴, **141x** at q=10⁶ |
| **Elliptic curve L(s,E)** | a_p(E) = p+1−#E(𝔽_p) | Rank of E (BSD conjecture) | 🔄 Peaks found (8.4x), matching pending | **7x** at N_E=10⁴ (estimated) |
| **Modular form L(s,f)** | Hecke eigenvalues a_p(f) | Ramanujan, Sato-Tate | ⏳ Not yet tested | **5x** at N=10⁴ (estimated) |
| **Dedekind ζ_K(s)** | Twisted Mertens for χ_d | Class numbers | ✅ Verified (χ₋₂₀: 3.8x) | **19x** at D=10⁴ (estimated) |
| **Hecke L(s,ψ)** | Hecke character values | Class field theory | Same as Dirichlet | **12x** at q=10⁴ (estimated) |
| **Hasse-Weil (genus 2)** | Frobenius char. poly on H¹ | Arithmetic of curves | ⏳ Not yet tested | **26x** at N=10³ (estimated) |

✅ = zero detection verified by computation. 🔄 = in progress. ⏳ = not yet tested.

Batch speedups marked "estimated" are operation-count projections; detection for those L-functions needs verification with correct coefficient data. Dirichlet and Dedekind batch speedups are confirmed (detection verified).

---

## Verified Computational Results

- **20/20** first ζ zeros detected (local z-scores up to 65σ)
- **Phase match** to 0.003 radians for 20 zeros (mpmath, 30-digit precision)
- **20-term model** explains 89% of variance in M(p)/√p (R = 0.944)
- **Out-of-sample prediction:** R = 0.952 on held-out primes (BETTER than training — genuinely predictive)
- **2,750 primes** out of 25 million suffice to detect all 20 zeros (9000:1 compression)
- **GUE pair correlation** RMSE = 0.066 from prime data alone
- **Fourth moment:** 96x peak amplification (connects to pair correlation)
- **Batch crossover** at conductor q ≥ 400 (verified by operation count)
- **Finite field validation:** 0.005 rad error on known zeros (ground truth confirmed)
- **434 Lean 4 theorems** formally verified (zero sorry)

## Verified Practical Applications

| Application | Gain | How |
|------------|------|-----|
| **Batch L-function zero scanning** | **12x** at q=10⁴, **141x** at q=10⁶ | All Dirichlet chars scanned simultaneously |
| **Class number lower bounds** | **5-14x** improvement over Goldfeld-GZ | Siegel zero exclusion makes bounds effective |
| **Primes in progressions (large q)** | **8x** better than Siegel-Walfisz at q=10⁵ | Unconditional GRH-quality bounds for verified characters |
| **Predictive model for M(p)** | R = 0.952 out-of-sample | 20-term explicit formula predicts Mertens function on unseen primes |
| **GRH verification** | 9,592 quadratic characters verified | ~200 zeros each below height T=50 |

## Detection Extends Beyond Primes

The spectroscope applies to any arithmetic function with an explicit formula:

| Input | Peak/Avg | Status |
|-------|----------|--------|
| Mertens M(p) | 8.4-17.3x | ✅ Main spectroscope |
| Twisted Mertens M_χ(p) | 2.8-3.8x | ✅ Dirichlet L-functions |
| Prime gaps g(p) | 3.8x | ✅ **Novel** — gaps encode zeros |
| Squarefree residual Q(p)-6p/π² | 3.0x | ✅ Extends framework |
| Smooth numbers (B=100) | 2.9x | ✅ Extends framework |
| Fourth moment |F|⁴ | 96x | ✅ Massive amplification |
| Finite field zeta | 15x, 0.005 rad | ✅ Ground truth validated |

---

## Key Files

| File | Description |
|------|-------------|
| `spectroscope-paper/README.md` | This file |
| `spectroscope-paper/hero_comparison.html` | Interactive visualization: our method vs classical |
| `experiments/PHASE_AMPLITUDES_K1_TO_10.md` | Verified phase data for 10 zeros |
| `experiments/EASY_WINS_RESULTS.md` | Phase saturation and detection curve |
| `experiments/LFUNC_BATCH_CROSSOVER_VERIFIED.md` | Batch speedup benchmarks |
| `experiments/RESONANCE_DOMINANCE_VERIFIED.md` | 10:1 resonance ratio for 100 zeros |
| `SPECTROSCOPE_APPLICABILITY.md` | Full list of applicable L-functions |
| `OUTREACH_TARGETS.md` | Potential collaborators and use cases |
| `RequestProject/` | 434 Lean 4 formalized results |

---

## Citation

Preprint in preparation. Author: Saar Shai. AI tools used in research (disclosed per STM 2025 guidelines).

---

## Contact

For questions, collaboration, or benchmark data: [contact info]
