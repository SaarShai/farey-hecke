# Correspondence: Rogelio Tomas Garcia (rogelio.tomas@cern.ch)
# CERN physicist, Farey fraction rank formulas, 6 papers in math.NT

## Timeline
- Apr 5: Saar initial email — Farey rank discrepancy, novelty question
- Apr 5: Rogelio reply — enthusiastic, asks for paper
- Apr 6: Saar sends draft
- Apr 6: Rogelio detailed feedback (most useful critique so far):
  * Abstract too technical; proofs too short; notation clashes (W, A, D similar)
  * R(f) resembles his "local discrepancy with offset" (Eq 6, his 2025 MDPI paper)
  * Conjecture 4.1 not compelling (disproved immediately)
  * M(p)≤-3 threshold: empirical only, extending to 8M primes could push to M(p)≤-7
  * Mentions Hall (1970) on second moment of Farey gaps
  * arXiv endorsement: insufficient recent activity, maybe 3 months
- Apr 12: Saar update — explicit formula, four-term decomposition rigorous, revised theorems
- Apr 12: Rogelio — notes ΔW ~ -2Σ Re[p^{iγ_k}/(ρ_k·ζ'(ρ_k))] looks involved; suggests improving C_W bound using his rank formula papers:
  * https://cs.uwaterloo.ca/journals/JIS/VOL25/Tomas/tomas5.pdf (Theorem 3)
  * https://math.colgate.edu/~integers/y63/y63.pdf (Theorem 2)
  * https://inspirehep.net/files/f2047f6517e0f6abddc4df6189d4bffd (Theorem 1)
  * Second moment of discrepancy IS the Riemann Hypothesis — says this explicitly
- Apr 13: Saar revised paper response:
  * Hall (1970) Lemma 1 = injection principle; Theorem 1 gives F_2(N) asymptotics with γ, ζ'(2)/ζ(2)
  * Connected to our decomposition via D(f_r)-D(f_{r-1}) = 1-R·l_r
  * Added Remark 6.2: M(p)≤-3 threshold is empirical, DiscrepancyStep is the open gap
  * Added Remark 5.1: W(N) bounds = Riemann Hypothesis (explicit)
  * Renamed D→N to avoid clash with rank discrepancy D(f)
  * B-term connects to Dedekind sums
  * arXiv: understood, 3 months timeline OK

## Apr 15: Rogelio follow-up on point 3 (structure of A):
"One comment on 3, what I meant is that A is imply A=W(p-1)(1-(p-1)^2/p^2)~ W(p-1) for large p, right? hence you do not need to define A. You want a new version of Delta W = W(p-1) - W(p), but you have W(p-1) still in the new version. I see the goal of bringing some understanding between the contributions from all fractions and the k/p fracs."

## WAITING FOR: reply to Apr 15 comment on structure of A

## Key insights from Rogelio
1. M(p)≤-3 threshold is fragile — empirical artifact, not a theorem. We must not overclaim.
2. DiscrepancyStep (N+C>A) IS essentially RH at its core — his explicit statement.
3. His three rank-formula papers give sharper C_W bounds than our current N/(3N/4).
4. Hall (1970) Note: second moment of Farey gaps F_2(N) with explicit constants.
5. B-term's connection to Dedekind sums — needs Minelli collaboration.
6. R(f) = ΣD·δ/Σδ² may connect to his "local discrepancy with offset" — unexplored.

## What Rogelio could help with
- Adapting Hall (1970) techniques to bound our N+C terms (denominator-by-denominator framework)
- Proving N+C > A asymptotically using his explicit rank formulas
- Possibly collaborating on the DiscrepancyStep lemma
- NOT: arXiv endorsement for ~3 months

## Notation changes made based on Rogelio's feedback
- D (new-fraction term) → N (new-fraction contribution)
- Four terms now: A (dilution), B (cross), C (shift-squared), N (new-fraction)
- ΔW = A - B - C - N (with tiny 1/n'^2 correction)
