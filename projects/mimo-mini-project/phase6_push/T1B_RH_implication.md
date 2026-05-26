---
model: mimo-v2.5-pro
max_tokens: 12000
---

# T1B — Odlyzko-te Riele 1985 implication for NW(Q) extreme outliers

## Setup

Empirically: NW(Q) − C ≈ M(Q)²/(6Q) for typical Q.

Mertens conjecture (1897): |M(x)| < √x for all x ≥ 1.
- Disproved by **Odlyzko & te Riele 1985**, J. Reine Angew. Math. 357, 138-160.
- They showed lim sup M(x)/√x > 1.06 and lim inf M(x)/√x < -1.009.
- So |M(x)|/√x > 1 occurs **infinitely often** (under their disproof + Riemann hypothesis assumed for some of the argument).

## Question to address rigorously

If the Mertens-NW relation holds:
  NW(Q) − C ≈ M(Q)²/(6Q)

and there exist Q where |M(Q)|/√Q > 1, then there exist Q where:
  NW(Q) − C > Q/(6Q) = 1/6

i.e., NW(Q) > C + 1/6 ≈ 0.836.

### Verify

1. **Is Odlyzko-te Riele's disproof unconditional?** Or does it require RH?

2. The "lim sup M(x)/√x > 1.06" claim — does it have an EFFECTIVE bound? I.e., for some x ≤ x_0, does the inequality hold? Or is x_0 huge (e.g., 10^14)?

3. Pintz, Kotnik-te Riele, etc., have refined bounds. State the current best:
   - lim sup M(x)/√x ≥ ?
   - lim inf M(x)/√x ≤ ?
   - And whether unconditional or conditional.

4. **For our purposes**: does there exist a Q at which we could COMPUTE M(Q) and find |M(Q)| > √Q? What's the smallest such Q?
   - Hurst (2018) computed M(x) up to x ~ 10^16
   - Was the disproof EVER witnessed computationally? Or is it a non-constructive existence proof?

5. Combine: if for some Q ≤ 10^16 we have |M(Q)| > √Q, then computing NW(Q) for that Q would yield NW(Q) > C + 1/6.

## What I want

1. Exact statement of Odlyzko-te Riele 1985 result with citation page.
2. Whether the proof was constructive (i.e., we know a specific x).
3. Best subsequent bounds (Pintz, Kotnik-te Riele, Sayed-Ahmad).
4. Honest assessment: do we KNOW a Q where |M(Q)| > √Q, or is it conditional/asymptotic?
5. **Specific testable prediction**: predict NW(Q) at the smallest known Q with |M(Q)| > √Q. Or, if none is known, predict at the Q with the largest known |M(Q)|/√Q.

Honesty: cite real papers only. State "I'm not sure" if uncertain.
