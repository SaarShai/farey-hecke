---
model: mimo-v2.5
max_tokens: 12000
---

# L6 — Lit check: prime-denominator Farey subsequence F^prime_N

## The empirical fact (Discovery #6)

F^prime_N = {p/q : q prime ≤ N, 0 ≤ p < q} ∪ {0}.

Properties:
- D*(F^prime_N) / D*(F_N) → 1/2 at matched point count (verified Q=200-5000)
- Lag-1 gap correlation collapses to ~0 (vs F_N's +0.5)
- Cardinality |F^prime_N| ≈ N²/(2 ln N) by PNT (asymptotically sparser than F_N)

## Lit check questions

1. **Is F^prime_N already studied in QMC?** Names to check: Niederreiter, Drmota-Tichy, Owen, Hickernell.

2. **Is the D* improvement = 1/2 known?** This is a clean ratio at a clean limit — suspicious that it would have been missed.

3. **In number theory**: enumerations restricted to prime denominators appear in:
   - Vaughan's identity arguments (sums over primes)
   - Linnik's constant work
   - But are these viewed as low-discrepancy sequences?

4. **In sieve theory**: Selberg sieve / Brun sieve work with prime-restricted sums. Is there a discrepancy interpretation?

5. **Equidistribution of p/q for q prime**: Vinogradov-style — does anyone analyze this as a sequence with explicit discrepancy bound?

## What I want

For each source:
- Has F^prime_N been studied?
- Is D*(F^prime)/D*(F) → 1/2 stated?
- If new, this is a clean contribution to QMC literature (a new low-discrepancy sequence).

Also: are there extensions worth pursuing?
- F^prime_N restricted further (e.g., q in specific arithmetic progression)
- 2D analog (prime denominators in 2D Stern-Brocot)
- Empirical comparison to standard sequences
