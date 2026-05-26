# Odlyzko-te Riele 1985 + subsequent improvements — VERIFIED facts

**Source**: research-lite subagent, 50 seconds, 6 tool uses

## Verified

1. **Odlyzko & te Riele (1985)**, J. Reine Angew. Math. 357, 138-160: proved `lim sup M(x)/√x > 1` by NON-CONSTRUCTIVE argument using LLL lattice reduction. **No explicit x value given.**
   - Wikipedia confirms; SCIRP citation confirms author/title.

2. **Kotnik & te Riele (2006)** + subsequent: conjectured smallest counterexample to Mertens conjecture at ≈ **exp(5.15 × 10²³)**.

3. **Platt (2024)** [arXiv:2502.21021]: reduced bound to ≈ **exp(1.96 × 10¹⁹)**.

## NOT verified (and likely wrong)

- **The specific constants "lim sup ≥ 1.06" and "lim inf ≤ -1.009"** that I cited in v12 (from T1B) are **NOT confirmed**. The agent could not find them in any primary source. Likely confabulation; quote in v12 should be retracted.

## Implication for v12 claims

v12 said:
> "If those bounds are correct and our Mertens-NW formula holds: there exist infinitely many Q with NW(Q) > C + 1.06²/6 ≈ C + 0.187. Computationally observable IF we can find specific Q with |M(Q)| > √Q."

**Retraction**:
- The 1.06 and -1.009 constants are not verified. The actual O-tR paper only proves lim sup > 1, no quantitative bound.
- The smallest known counterexample is conjectured beyond exp(10¹⁹) — **NOT computationally observable** at any plausible Q.

**Refined statement** (honest):
> "Odlyzko-te Riele 1985 disproved the Mertens conjecture |M(x)| < √x by a non-constructive argument. Under their result, lim sup M(x)/√x > 1, but the smallest counterexample is conjecturally beyond exp(10¹⁹) (Platt 2024). The Mertens-NW formula thus predicts NW(Q) − C can exceed 1/6 for these enormous Q, but no constructive witness is known."

## Useful for paper
- Cite Platt 2024 [arXiv:2502.21021] for the latest bound
- Cite O-tR 1985 for the disproof itself
- Drop the "1.06 / -1.009" specific bounds — these are folklore or confabulation
