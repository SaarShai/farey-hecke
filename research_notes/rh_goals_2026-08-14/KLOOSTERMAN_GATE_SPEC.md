# Pre-registered gate: Kloosterman route to DiscrepancyStep (G3-S1)
Frontier spec v1, 2026-08-14. Ticket: kloosterman-gate. Frozen BEFORE any
computation or proof attempt; amendments must be logged.

## Target theorem (unconditional)

For every prime p with M(p) ≤ −3 (M = Mertens): the exact integral
observable inequality N + B + C > A holds, where A, B, C, N are the four
components of the per-step Farey discrepancy decomposition at p (exact
definitions: projects/prime-step-breakthrough/RESEARCH_SPEC.md and
equispaced-primes/papers/nw-mertens-note/INTEGRAL_FAREY_KILL_TEST_PROTOCOL
_2026-07-19.md — the frozen kill-test observable). Finite evidence: holds
for all 4,617 qualifying primes ≤ 100,000 (exact scan, zero exceptions).

## The binding analytic piece

Per the 2026-07-02 analysis: the missing input is control of the
residue-permutation variance of a ↦ pa mod b over b ≤ p−1 — "arithmetic
info beyond PNT + Cauchy–Schwarz". Candidate tool: Weil-grade Kloosterman
bounds |S(m,n;c)| ≤ d(c)√c (Ustinov-style applications to Farey/mediant
statistics; in-repo pointers: Nakamura 1401.2980 usage, Matomäki 2009).

## PRE-REGISTERED SUFFICIENCY BAR

Write V(p) := the variance-type sum that must be bounded (to be extracted
verbatim from the B+C+N vs A decomposition in step 1 of the probe). The
theorem follows if V(p) ≤ K · p^{3/2+ε} with an explicit K (this is the
"square-root cancellation on average" level that Weil bounds typically
give after d(c)-losses). NO-GO CONDITION (binding): if honest accounting
shows the needed bound is V(p) = o(p^{2}/log^A p) with a POWER of p beyond
p^{3/2+ε} — i.e., the route needs more than Weil-square-root cancellation
(quarter-power gains, spacing correlations of zeros, or RH-strength input)
— the probe STOPS, records NO-GO, and the thread folds per the 2026-06-29
verdict. No "one more idea" extensions past the bar.

## Probe protocol (1–2 wk equivalent, agent-assisted)

1. Extract V(p) symbolically from the exact decomposition; verify the
   extraction numerically at p = 13, 8501, 92173 (exact rationals).
2. Reduce V(p) to complete/incomplete Kloosterman sums (completion +
   partial summation); COUNT the losses (each completion costs log; d(c)
   divisor losses summed explicitly).
3. Compare the achieved exponent against the bar. GO ⇒ full proof
   write-up + Aristotle on the finite lemmas. NO-GO ⇒ record + close.

## Success/failure outputs (both publishable-adjacent)

- GO: unconditional sign-structure theorem at the Franel–Landau boundary
  (JNT-tier; would be the program's strongest unconditional result).
- NO-GO: a documented reduction showing exactly which exponent barrier
  blocks elementary/Weil methods — folded into the D3 note's outlook
  section as a precise open problem.
