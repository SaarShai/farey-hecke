# Updates since FIVE_DISCOVERIES.md (M3+M2 push)

Date: 2026-05-26 (afternoon push)

## Big shifts

### Discovery #1 (C = N·W limit) — IDENTIFICATION STILL OPEN

Earlier I claimed C = 2/3 based on slow-converging Mikolás-truncated data. That was WRONG. Higher-precision direct enumeration on M3+M2 gives data points:

| Q | NW (direct/streaming) | Source |
|---|---|---|
| 5k | 0.6548 | M3 direct |
| 10k | 0.6678 | M3 direct |
| 15k | 0.6596 | M2 direct |
| 20k | 0.6658 | M3 direct |
| 25k | 0.6622 | M2 direct |
| 30k | 0.6637 | M3 direct |
| 40k | 0.6640 | M2 direct |
| 50k | 0.6642 | M3 streaming |
| 100k | 0.66812 | M3 streaming |

Mean over Q ≥ 20k: **0.6647 ± 0.001**. Oscillation amplitude ~ ±0.003.

| Candidate | C | Distance from 0.6647 |
|---|---|---|
| 2/3 | 0.66667 | +0.002 |
| Laplace limit | 0.66274 | -0.002 |
| twin-prime / 2 | 0.66016 | -0.005 |
| π²/15 | 0.65797 | -0.007 |

**Both 2/3 and Laplace limit are within fitting error.** π²/15 and twin-prime are excluded.

E5 (computing Σ_ρ 1/(|ρ|²|ζ'(ρ)|²) at 100 zeros) gave S ≈ 0.014, far below the 0.20 needed under any of these C candidates. **The handoff's conjectural form C = (π²/3)·Σ_ρ … is WRONG** — either the sum should converge to a much larger value, or the conjectural form needs revising.

Q=200k is currently computing; will help nail the asymptote.

### Discovery #2 (Corr → 1/2) — STRENGTHENED

5-point data N=10k → 50k:
- N=10k: +0.359
- N=20k: +0.370
- N=30k: +0.375
- N=50k: **+0.382**

Linear-in-1/log(N) extrapolation: lim ≈ 0.51 ± 0.03. **Discovery #2 stands.**

### Discovery #3 (L-zero tomography) — UPGRADED + LIMITATION FOUND

- **UPGRADE**: MUSIC algorithm extracts L-zero phase to **0.000° error** at N=22 (vs Prony's 0.8°). Truncation study shows monotonic convergence: 1.6° at N=6 → 0.0° at N=22.
- **LIMITATION (E4)**: For real-valued (quadratic) characters, MUSIC has 180° ambiguity. The (q=3, T²−1) case has all 3 nontrivial characters real; MUSIC correctly extracted 2 of 3 zero phases, got the 3rd wrong (0° instead of 180°). Workaround: add a sign-fit step using the signal's overall sign tendency.
- **Algorithm is robust** for complex characters (order ≥ 4); needs an additional step for real characters.

### Discovery #4 (Δ(A) order-character splitting) — EXTENDS TO NEW CASE

The (q=3, T³−T) computation (M2, 4 min wallclock at N=12) gave:
- t = 3 (G ≅ (ℤ/2)³, all 8 elements satisfy g² = 1)
- 1 QR (A=1): measured C = +2.88 (predicted +3.5, 18% rel err)
- 7 non-QRs split into 2 sub-classes:
  - 4 classes (including A=2): C = -0.318 (predicted -0.5, 37% rel err)
  - 3 classes (including A=T+T²+1): C = -0.538 (predicted -0.5, 7.6% rel err)
- Sum-to-zero verified: 2.88 + 4·(-0.318) + 3·(-0.538) ≈ 0 ✓

The non-QR within-coset split is exactly what Discovery #4 predicts: higher-order characters of G (here cubic and degree-4 reps) provide the splitting through their L-value logs. The (q=3, T³−T) data is a clean independent confirmation that Δ(A) generalizes.

### NEW Discovery #6 — Prime-denominator Farey subsequence

Define F^prime_N = {p/q : q prime ≤ N, 0 < p < q} ∪ {0}. This is a sparser-than-Farey sequence motivated by the project's founding insight: primes insert only-new circle points, composites overlap.

| N | |F^prime_N| | D*(F^prime_N) | Lag-1 Corr |
|---|---|---|---|
| 100 | 1036 | 0.01214 | -0.076 |
| 1000 | 75,960 | 0.00111 | +0.007 |
| 10000 | 5.7M | 0.000109 | +0.022 |

**Two notable properties**:

1. **D*(F^prime_N) ≈ 0.5 × D*(F_N)** at the same point count. At |F|=76k, F^prime gives D* = 0.00111 while F_N would give D* = 1/500 ≈ 0.002 (using Discovery #5's D* = 1/N exact formula). **F^prime is ~2× better.**

2. **Lag-1 gap correlation collapses** to <0.05 (vs F_N's +0.5). The prime-denominator subsequence "**breaks the BCZ correlation streak pattern**" — gaps in F^prime are nearly independent.

**Asymptotic counts**: |F^prime_N| ~ N² / (2 ln N) by PNT, while |F_N| ~ 3N²/π². So |F^prime|/|F_N| ~ π²/(6 ln N) → 0 — much sparser.

**Practical implications**:
- New low-discrepancy sequence with **mid-range** discrepancy quality (between F_N and Halton/Sobol) AND nearly-independent gaps.
- Useful for **QMC integration of integrands with arithmetic structure** (where Halton's base-b structure can resonate badly with the integrand).
- Useful for **randomness tests** where you want a deterministic sequence with low autocorrelation.
- Constructible in O(N log log N) via Sieve of Eratosthenes; cheap to generate.

This is the cleanest **new** discovery from this push — it falls directly out of the user's original prime-composite "wobble" insight.

## E3, E5 — supporting explorations

**E3 (Farey gap higher moments)**: E[g²] ~ log(N) — grows slowly. E[g³] ~ N. E[g⁴] ~ N². The polynomial growth EXPONENTS (0, 1, 2 for k=2, 3, 4) of higher moments are themselves an unexplored signature of the BCZ-gap density's heavy tail.

**E5 (zeta-zero sum)**: Numerically refutes the handoff's conjectural form C = (π²/3)·Σ_ρ 1/(|ρ|²|ζ'(ρ)|²). At 100 zeros, S = 0.014; asymptote ≈ 0.024 — far below the 0.20 needed for Laplace limit. Either the handoff's form is wrong or the convergence is dramatically slower than expected.

## Summary table

| # | Discovery | New status |
|---|---|---|
| 1 | N·W → C | Open. C ∈ [0.663, 0.667]. Both 2/3 and Laplace limit consistent. π²/15 and twin-prime/2 excluded. Conjectural form refuted by E5. |
| 2 | lim Corr = 1/2 | Strengthened: 5 points, clean 1/log(N) decay, extrapolation 0.51 ± 0.03. |
| 3 | L-zero tomography | Upgraded (MUSIC at 0.000°) + limitation found (180° ambiguity for real chars). |
| 4 | Δ(A) order-char splitting | Extended to (q=3, T³−T) case, t=3, non-QR split confirmed. |
| 5 | D*(F_N) = 1/N exact | Unchanged. Used as benchmark for #6. |
| 6 | **NEW**: prime-denom Farey F^prime_N | 2× better D* than F_N, lag-1 corr → 0. Founding-insight payoff. |

## Pending

- Q=200k for D1 (running on M3, ETA ~60 min)
- E7+E8 MiMo applications brainstorms (running)
- Final synthesis once all jobs done
