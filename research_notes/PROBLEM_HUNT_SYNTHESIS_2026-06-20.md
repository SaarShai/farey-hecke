# Problem-hunt synthesis — 6 domains, adversarially verified (2026-06-20)

Surveyed 6 wide domains for an open problem matching our edge; each top pick adversarially killed.
RESULT: 0 strong candidates. 5 weak, 1 reject. The failure is uniform and diagnostic.

| Domain | Top pick | Verdict | Why it fails |
|---|---|---|---|
| D1 extremal/Ramsey | R(K4,K4-e,K4-e) lower bound | weak | Lean-cert OWNED (formal_ramsey, IJCAI'25 SAT+CAS, PBLean'26) + type-mismatched to lower bounds; search edge generic; beating specialist Wesley on his turf |
| D2 geometry | Polymath16 chi(R^d) cases | weak | walls (Nechushtan 2002, 24y); DRAT certs OWNED (Heule 2018); Parts/Voronov/Raigorodskii ahead monthly |
| D3 number theory | Ideal Prouhet-Tarry-Escott n=11 | weak | witness speculative; method published; cert+fleet not novel search |
| D4 CF/additive | Rickards-Stange reciprocity CF dims | reject | certified-CF-dimension is OWNED mature method (Pollicott-Vytnova 200 digits); raw-FLOPS wall (v>=1e13) |
| D5 experimental | Machin/arctan Lehmer-measure records | weak | the incumbent's OWN open-source tool (find_arctan_formulae) already does PSLQ+grouping; generic |
| D6 dynamics | certified billiard tiles, obtuse triangles | weak | McBilliards OWNS the search; only "Lean-certify an existing tile" tractable = low-value verification-of-known |

## THE DIAGNOSIS (why every pick failed)
Our supposed edges -- certified/interval computation AND Lean/Aristotle verification -- are NOT a
moat. In every area they are already a MATURE OWNED capability (Pollicott-Vytnova, Heule DRAT,
formal_ramsey, McBilliards, find_arctan_formulae). And a lower-bound/construction WITNESS is checkable
in seconds by anyone, so the verification edge is aimed at the half we can't reach. The only genuinely
differentiated capability we have is the FLEET OF PARALLEL REASONING AGENTS + ADVERSARIAL FALSIFICATION
-- and none of these "compute/verify"-framed problems make THAT load-bearing.

## THE REFRAME (where we can actually contribute)
Our real edge is AI-NATIVE: large-scale parallel hypothesis GENERATION + falsification + synthesis --
i.e. the FunSearch / AlphaEvolve paradigm, NOT certified computation.
- FunSearch (Romera-Paredes et al, Nature 2024): LLM-guided evolutionary program search found a LARGER
  cap set in dimension 8 and better online-bin-packing heuristics -- genuine NEW mathematics.
- AlphaEvolve (Google DeepMind, 2025): evolutionary LLM search improved matrix-multiplication (reported
  4x4 complex in 48 scalar mults, beating the long-standing 49) and matched/improved bounds on ~50 open
  extremal-combinatorics problems.
This is exactly our infrastructure (a fleet that proposes+falsifies+verifies at scale). It PRODUCES
real new math, it is NEW (2024-25) hence not saturated, and contributions are CONCRETE + trivially
VERIFIABLE (a better explicit object).

CAVEAT (honest): AlphaEvolve is DeepMind's, far better-resourced, and not public. We would run a
scrappier version on a CAREFULLY CHOSEN, BEATABLE, NON-OWNED extremal-construction target -- realistic
for a modest but real contribution (a record nibble / new construction), not a guaranteed headline.

## RECOMMENDATION
Stop framing our edge as "certified computation" (owned everywhere). Pursue the FUNSEARCH/ALPHAEVOLVE
MODE: pick an extremal-CONSTRUCTION problem (cap-set-like, packing/covering bound, no-3-in-line,
Heilbronn, minimum-overlap, a specific Ramsey/Turan construction) where (a) the record is plausibly
beatable, (b) it is NOT already done by AlphaEvolve/a specialist, (c) the object is trivially
verifiable -- and run fleet evolutionary construction-search + adversarial falsification at it.
Choosing that target needs the SAME brutal novelty discipline that just killed 6 picks.
