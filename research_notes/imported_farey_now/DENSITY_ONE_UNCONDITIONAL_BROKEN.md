# DENSITY-ONE UNCONDITIONAL CLAIM: BROKEN
# 2026-04-10 — Opus adversarial verification

## VERDICT: INVALID

The M1 Max 45KB "proof" has a fatal flaw.

## THE FLAW
The proof conflates:
- DENSITY of exceptional zeros (how many have Re(ρ) > 1/2) — controlled by Ingham-Huxley
- INFLUENCE of exceptional zeros (how much they affect F at OTHER ordinates) — NOT controlled

Even ONE zero with Re(ρ_j) = 0.6 contributes N^{0.6} to interference at EVERY bulk zero.
The resonant term at a bulk zero is N^{0.5}. So N^{0.6} >> N^{0.5} — non-resonant dominates.

The proof assumes restricting WHICH zeros you examine removes the INFLUENCE of excluded zeros.
It does not. Off-line zeros pollute the spectroscope GLOBALLY.

## WHAT WOULD BE NEEDED
A: Show off-line zero contributions cancel on average (hard — needs new large sieve result)
B: Show N^{β_j}/(|γ_j-γ_k|) is small for most k (fails — spacing is O(1), need N^{0.1})
C: Assume RH (works but then it's conditional)

## HONEST STATUS
The "unconditional density-one" result is actually CONDITIONAL on RH.
The strongest unconditional statement remains: "Σ p^{β-1} diverges for any zero" (just divergence, not concentration).

## LESSON
Same pattern as Selberg input: local model claims unconditional, adversarial review reveals it's conditional.
NEVER trust unconditional claims without Opus/Codex verification.
