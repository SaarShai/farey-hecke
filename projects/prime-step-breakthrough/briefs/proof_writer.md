---
GOAL: Produce a self-contained proof-qualified preprint and formula-level novelty audit for T1--T4.
ROLE: mathematician and hostile claim editor
SCOPE: projects/prime-step-breakthrough/paper/PREPRINT.md and projects/prime-step-breakthrough/research/{NOVELTY_AUDIT.md,PROOF_OBLIGATIONS.md}
INPUTS: RESEARCH_SPEC.md, BLINDSPOT_AUDIT.md, historical sources explicitly cited there
NO_TOUCH: src/, tests/, web/, briefs/, README.md, verify_all.py, any path outside projects/prime-step-breakthrough/
DELIVERABLE: theorem/proof manuscript, claim ledger, source comparison, unresolved-obligation list
VERIFY: every displayed formula is independently rederived; source URLs and local paths resolve; theorem status labels are internally consistent; grep finds no unqualified external novelty claim
DONE: T1--T4 each have definitions, statement, proof, caveat, computational check boundary, and prior-art boundary; any gap causes demotion rather than handwaving
---

The T1 proof must spell out the two-dimensional ETK weight sum, why the cutoff
below p removes every nonzero resonance, and how the divisor bound is uniform
over the cutoff box.  The T2 proof must calculate Hardy--Krause variation or
cite the exact theorem hypothesis, distinguish normalized and raw moments, and
handle p=2/r=0.  T3 must derive the Fourier coefficient, Parseval constant,
divisor formula, local factors, integration-by-parts sign, sharpness witness,
and endpoint convention.  T4 must derive the cross-kernel sum and state exactly
what is standard about the zeta-ratio/RH consequence.

Primary literature search must cover at least Mikolas, Franel, Ramanujan-sum
product means, Farey MMD, sawtooth/Dedekind covariance, Garcia rank formulas,
and Farey order-statistics algorithms.  "Not found" is evidence scope, never a
proof of novelty.
