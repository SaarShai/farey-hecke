# Exact 3-cluster witness — Taha G₅-BCZ map (q=5)

**Date generated:** 2026-06-12  
**Method:** sympy exact arithmetic over Q(√5)  
**Script:** `code/goal1_q5_witness_exact.py`

## Setup

- q = 5, λ = φ = (1+√5)/2
- **X(5) = 1/φ³ = √5 − 2** ≈ 0.2360679774997897
- Domain: T⁵ = {0 < a ≤ 1, 1 − φa < b ≤ 1}
- Last branch T₄: {a + φb > 1}
- Map on T₄: (a,b) → (b, −a + kφb),  k = ⌊(1+a)/(φb)⌋
- Observable: P = a·b  (y-component of w₄ = (0,1) is 1)

## Starting point

**Rational start:** a₀ = 3/5, b₀ = 1/3  (total denominator sum = 8; smallest found).

## Exact coordinates

| Point | a | b | k | P | X − P |
|-------|---|---|---|---|-------|
| 1 | 3/5 | 1/3 | 2 | 1/5 | √5 − 11/5 ≈ 0.03606798 |
| 2 | 1/3 | −4/15 + √5/3 | 1 | −4/45 + √5/9 | -86/45 + 8*sqrt(5)/9 ≈ 0.07650487 |
| 3 | −4/15 + √5/3 | 11/30 + √5/30 | — | −19/450 + 17√5/150 | -881/450 + 133*sqrt(5)/150 ≈ 0.02486916 |

## Verified inequalities (all exact, no floats)

### k₁ = 2: floor((1+a₀)/(φ·b₀)) = 2

- (1+a₀)/(φ·b₀) = 12(√5−1)/5 ≈ 2.9665631460
- ratio − 2 = -22/5 + 12*sqrt(5)/5 ≈ 0.9665631460 > 0  ✓
- 3 − ratio = 27/5 - 12*sqrt(5)/5 ≈ 0.0334368540 > 0  ✓

### k₂ = 1: floor((1+a₁)/(φ·b₁)) = 1

- (1+a₁)/(φ·b₁) = 210/109 - 10*sqrt(5)/109 ≈ 1.7214616534
- ratio − 1 = 101/109 - 10*sqrt(5)/109 ≈ 0.7214616534 > 0  ✓
- 2 − ratio = 8/109 + 10*sqrt(5)/109 ≈ 0.2785383466 > 0  ✓

### Domain and branch membership

All three points satisfy (verified by `.is_positive` on simplified Q(√5) expressions):
- 0 < a ≤ 1
- 1 − φa < b ≤ 1
- a + φb > 1  (last branch T₄)

### P < X(5) (all strict)

- P₁ = 1/5,  X−P₁ = √5−11/5 ≈ 0.03606798 > 0  ✓
- P₂ = −4/45+√5/9,  X−P₂ = -86/45 + 8*sqrt(5)/9 ≈ 0.07650487 > 0  ✓
- P₃ = −19/450+17√5/150,  X−P₃ = -881/450 + 133*sqrt(5)/150 ≈ 0.02486916 > 0  ✓

## Lean formalization notes

- All inequalities of the form `p + q·√5 > 0` reduce to rational arithmetic:
  - If q ≥ 0: suffices `p > 0` or `5q² > p²` with p < 0.
  - All margins here have positive leading rational+sqrt5 terms.
- The witness is self-contained: no appeal to ergodic averages, no floating-point.
- k₁=2 certificate: `2·φ·(1/3) < 8/5 < 3·φ·(1/3)` reduces to `(1+√5)/3 ≤ 8/5` and `8/5 < (1+√5)/2`.
- k₂=1 certificate: `φ·b₁ ≤ 4/3 < 2·φ·b₁` reduces to rational+√5 inequalities above.
- The cluster is on the **last branch T₄** throughout (uniform map form across all q).

## Significance

This is the first exact algebraic 3-cluster witness for q=5 (non-arithmetic Hecke group G₅).
It confirms numerically that B(5) ≥ 3 (cluster ceiling is at least 3), consistent with
the onset₃/X(5) ≈ 1 from the orbit scan. The witness is suitable for direct Lean
formalization as a certificate in a `cluster_size_le_two` falsification proof.
