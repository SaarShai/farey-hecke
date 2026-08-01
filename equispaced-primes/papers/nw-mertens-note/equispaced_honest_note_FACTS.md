# Scoped fact ledger for the honest note

This file is a submission-facing ledger, not an archive of earlier claims.
Every numerical statement retained below has an executable definition and a
local output record in `NUMERICAL_EVIDENCE_2026-07-18.md`.

## Exact statement

For every prime \(p\),
\[
 \sum_{f\in\mathcal F_{p-1}}e^{2\pi i p f}=M(p)+2.
\]
It follows directly from the Ramanujan identity \(c_b(p)=\mu(b)\) for
\((b,p)=1\), with the two Farey endpoints included.  The note makes no claim
about novelty, priority, or a freshly checked formalization.

## Finite numerical facts

| Object | Exact definition | Witness | Local result |
|---|---|---:|---|
| Broad ΔW sign implication | \(M(p)<0\Rightarrow\Delta W(p)\leq0\), \(\Delta W=W(p-1)-W(p)\) | 92,173 | \(M=-2\), \(\Delta W=+3.561440773266696686177868\times10^{-11}\) |
| Restricted R1 cross-term positivity | \(B_{\rm R1}(p)\geq0\) for \(M(p)\leq-3\) | 237,733 | \(M=-20\), \(B_{\rm R1}=-3.018492026640170288085938\times10^{10}\) |
| Restricted R1 cross-term positivity | same | 243,799 | \(M=-3\), \(B_{\rm R1}=-9.190201299936826705932617\times10^{9}\) |

`B_R1` is not `ΔW`: it uses the one-indexed rank convention
\(B_{\rm R1}=2\sum(\operatorname{rank}_{\rm R1}(f)-|\mathcal F|f)\delta_p(f)\)
and `rank_R1(0/1)=1`.

## Explicit non-facts

- No range-wide claim through 100,000 is retained.
- No proportion, including the formerly reported approximately 73% at
  \(X=10^7\), is retained: there is no exact event definition, denominator,
  runnable local computation, and saved output artifact.
- No density, density-one, RH-conditional, or RH-progress claim is retained.
- The floating numerical outputs certify reported signs computationally; they
  are not interval-arithmetic or exact-rational proofs.
