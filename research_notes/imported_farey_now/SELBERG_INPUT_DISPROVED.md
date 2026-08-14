# CRITICAL CORRECTION: The "Selberg Input" Is WRONG
# 2026-04-09

## The Claim (FALSE)
Σ_{n≤x} M(n)²/n² = (6/π²)·log x + O(1), unconditionally.

## The Truth
Σ_{n≤x} M(n)²/n² ≈ 2.26 at N=500,000 and barely growing.
The claimed (6/π²)·log(500K) = 7.98 — off by 3.5x.

## Root Cause: Confusion of Two Objects
- Σ μ(n)²/n = (6/π²)·log x + O(1) ← TRUE (squarefree counting)
- Σ M(n)²/n ≈ C·x where C ≈ 0.03 ← TRUE but C ≠ 6/π²
- The "Selberg" claim conflated μ(n)² with M(n)² = (Σ_{k≤n} μ(k))²

## Numerical Evidence
| N | Σ M(n)²/n² | (6/π²)log N | ratio |
|---|-----------|------------|-------|
| 100 | 1.965 | 2.800 | 0.70 |
| 1000 | 2.069 | 4.199 | 0.49 |
| 10000 | 2.143 | 5.599 | 0.38 |
| 100000 | 2.212 | 6.999 | 0.32 |
| 500000 | 2.257 | 7.977 | 0.28 |

The ratio is DECREASING, not approaching 1. The sum is sub-logarithmic.

## What IS True About M(n)² Mean Square
Under RH: (1/x)Σ_{n≤x} M(n)² → Σ_ρ 1/(|ρ|²|ζ'(ρ)|²) ≈ 0.03
This gives Σ M(n)²/n² ~ 0.03·log x under RH — divergent but with tiny constant.
Unconditionally: PNT gives M(n) = O(n·exp(-c√log n)), making M(n)²/n² summable.
So Σ M(n)²/n² likely CONVERGES unconditionally.

## Impact
- Paper J unconditional proof via diagonal sum: DEAD
- The Opus proof is structurally correct but built on false input
- The adversarial reviewer was right to flag the input
- Paper J must be CONDITIONAL on RH, or use a completely different approach

## Lesson
ALWAYS verify numerical claims computationally before building proofs on them.
Local models (and even Opus) confidently stated "Selberg 1946" without checking.
The 5-minute computation above would have caught this immediately.
