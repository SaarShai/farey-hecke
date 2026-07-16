# Independent review record

Status: pre-commit review ledger for the 2026-07-15 research package.

## Review separation

The proposal, implementation, and verification lanes were separated.  Advisors
could suggest proofs or counterexamples, but deterministic exact-arithmetic
gates and cold reviewers—not the proposing advisor—decided promotion.

## Mathematical reviews

### GPT-5.6 Sol, xhigh reasoning

The literal model identifier `gpt-5.6-sol-ultra` was unavailable in the local
Codex route.  The operational substitute requested by the user was
`gpt-5.6-sol` at `model_reasoning_effort="xhigh"`.

The first review caught two material issues before freeze:

- (K(m,n)) itself is not pair-multiplicative; only (12K(m,n)) is.  The
  counterexample (K(6,6)=1/9\ne K(2,2)K(3,3)=1/108) is now explicit.
- The initial application comparison hid admissible prime/divisor-grid and
  same-point midpoint losses.  Those are now mandatory negative controls.

The final theorem review independently re-expanded the finite-population
fourth moment, checked the variance and interpolation steps, and found the
stronger sharp bound
\[
 \mathbb E S_i^4\le\frac13\left(\sum_j\Delta_j^2\right)^2.
\]
It proposed (c_1=9/160), checked (N=2,3), identified equality at
(N=4,i=2), and required the universal upper inequality to be non-strict in
the zero-variance case.

Verdict: **pass after corrections**.

### Cold independent proof canary

A separate read-only verifier derived the fourth-moment coefficients from
scratch, reduced them to the two endpoint quadratics according to the sign of
(A), checked the central-index count modulo four, and reproduced the exact
constant (9/160).  It additionally checked:

- every coefficient for all prefix sizes through (N=80);
- 126,399 seeded rational centered populations;
- direct all-permutation prefix oracles through (N=8); and
- the equality witness ((1,1,-1,-1)) at (N=4,i=2).

It also performed a post-edit claim/attribution audit and required the paper to
credit classical finite-population moments and the classical continuous-
(L^2) identity, while claiming novelty only for the García-specific
deduction.

Verdict: **pass after editorial corrections**.

### Other-vendor frontier advisor

A separate frontier advisor reviewed T1--T4's architecture and constants.  Its
useful confirmations were retained; one overbroad novelty inference was
rejected because search absence cannot establish priority.  No theorem relies
on that advisor alone.

Verdict: **supporting review only, not a publication-grade novelty search**.

## Prior-art collision review

The cold reviewer found direct classical predecessors for the ingredients of
Theorem 6:

- Pozdnyakov--Steele (2013), equation (13), for the prefix variance;
- Isserlis (1931) and later finite-population treatments for fourth moments;
  and
- the Koksma--Warnock line, with Kirk--Pausinger (2023) as a modern
  formula-level source, for one-dimensional continuous (L^2) discrepancy.

García's 2026 paper states the centered-random-walk heuristic and the
two-sided conjecture but does not contain the moment proof or rigorous
constants.  The safe novelty statement is therefore:

> Applying classical finite-population moment formulas to García's fixed-gap
> permutation model, reducing the fourth moment to a sharp universal bound,
> and combining it with interpolation proves García's qualitative two-sided
> conjecture.  Novelty is not claimed for the underlying moment or discrepancy
> identities.

This was a bounded primary-source search.  MathSciNet, zbMATH, and a specialist
citation-graph review remain pre-publication work.

## Deterministic review gates

The final machine gate is `python3 verify_all.py`.  It covers independent
piecewise-rational kernel integration, exact Farey-shift moments, exhaustive
gap permutations, direct interval integration, the sharp fourth-moment
equality case, optimizer truth on small instances, negative controls,
million-gap scaling, CLI/API parity, malformed requests, artifact validation,
and mutation boundaries.

Rendered browser interaction is a separate live gate: keyboard entry, clicks,
result rendering, exact-rational wire preservation, error display/recovery,
and CLI/API comparison are recorded after the final source is loaded.
