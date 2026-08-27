# LAW preemption check — synthesis (2026-08-27)

Binary question (sol repair item 12): is the fixed-q LAW (T^2 log T weighted
growth of off-line scattering zeros for a fixed non-arithmetic Hecke triangle
group G_q) an immediate corollary of Selberg 1990 / Hejhal 1983 / Kelmer in
orbifold generality?

Three research lanes (SELBERG1990.md, HEJHAL1983.md, KELMER.md, this dir).

## Verdict: NOT PREEMPTED BY ANY LOCATED THEOREM — but NOT SETTLED.

- **Kelmer (arXiv:1402.4780, IMRN 2015): definitively does NOT apply.**
  Theorem 3 requires TORSION-FREE finite-volume hyperbolic manifolds; G_q has
  elliptic elements of orders 2 and q (orbifold). Also a different counting
  function (weighted sum ~ (kappa(d-1)/2pi) T log T for manifolds, vs our
  F_q ~ T^2 log T with the triangular weight). Hypothesis failure is
  concrete and checkable. This is the strongest citation a hostile referee
  would raise, and it does not cover our case as stated.
- **Selberg 1990 (Piatetski-Shapiro Festschrift): scope UNRESOLVED from
  secondary sources.** Secondary citations describe dense accumulation of
  scattering poles along Re s = 1/2 for cofinite one-cusp groups; no
  secondary source located states a fixed-group off-line weighted count in
  orbifold generality. The primary text was not readable by the lane.
- **Hejhal LNM 1001 (Thm 7.11 / Cor 7.12): quantifiers are asymptotic in q
  ("sufficiently large q"), consistent with sol's characterization; fixed-q
  infinitude not confirmed as proved anywhere. Primary text not readable by
  the lane.

## Consequences
1. main_v2.tex's framing (LAW as an OPEN QUESTION only) is exactly right and
   stays. No change required.
2. The Kelmer torsion-free gap is now documented ammunition: if a future
   analytic note proves the orbifold/fixed-q case, the delta over Kelmer is
   the elliptic-element contribution to the trace/scattering argument, and
   the delta over Hejhal is the fixed-q quantifier.
3. REMAINING RISK: the two primary texts (Selberg Collected Works II /
   Festschrift paper; Hejhal LNM 1001 ch. 7) were not read directly. The
   binary question is not fully closed until someone reads them.
   OWNER-TODO: obtain both (library/scan); or ask Koyama, who will know the
   Selberg 1990 statement from memory.

Caveat: lanes were bounded (research-lite, 3-5 sources); negative claims
here mean "not located", not "does not exist".
