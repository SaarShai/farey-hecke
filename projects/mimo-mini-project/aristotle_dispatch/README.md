# MiMo Mini-Project: Top 3 Verified Discoveries — Aristotle Dispatch

Dispatch from the MiMo mini-project research session (May 2026). Three Lean
files stating the strongest discoveries after multi-phase adversarial
verification.

See `PROMPT.md` for per-file dispatch instructions.

## The 3 discoveries

1. **MertensNWCorrelation.lean**: NW(Q) − C ≈ M(Q)²/(6Q) pointwise, where
   NW(Q) is the normalized Farey L²-discrepancy and M(Q) is the Mertens
   function. Empirical Pearson 0.971 over 28 Q values; off-grid predictions
   verified at Q=199933 and Q=926265.

2. **Cluster2Universality.lean**: top-quantile Farey gaps form maximal
   clusters of size exactly 2 with probability → 1 as quantile → 1.
   Empirically 99.2-99.3% at q=0.9999 across multiple N up to 10⁵.

3. **BCZDenominatorRepulsion.lean**: under the Boca-Cobeli-Zaharescu
   joint density of normalized consecutive Farey denominators,
   Corr(X, Y) = -1/2 exactly. Verified empirically on actual Farey F_N
   to 4 decimal places at N=1000, 3000, 10000. **This file should be
   tractable to fully close.**

## Project context

GitHub: https://github.com/SaarShai/Primes-Equispaced (under
`projects/mimo-mini-project/`).

The full history (~50 MiMo dispatches, ~25 stream_J_v2 computations,
multiple adversarial rounds with refutations and defenses) is in
`projects/mimo-mini-project/phase3_synthesis/FINAL_DISCOVERIES_v11.md`
within the same repository.

## Adversarial discipline maintained

Throughout the session, multiple LLM-generated claims were caught wrong
by direct numerical computation (e.g., the "lag-1 correlation = 1/2"
conjecture was refuted by 1M-sample MC of the BCZ chain giving 0.162).

Aristotle's role here is to:
- Verify Lean syntax of the theorem statements
- Close tractable sub-results (especially in File 3, the BCZ integration)
- Annotate any unprovable-in-current-Mathlib gaps with MATHLIB-PREREQ
- Refrain from fake-proofs via trivialization

Co-authored-by: Aristotle (Harmonic) <aristotle-harmonic@harmonic.fun>
