# FunSearch/AlphaEvolve target hunt — synthesis + pick + pilot

Date 2026-06-27. 6-domain survey fleet (A OEIS / B erdosproblems / C geometry / D coding-design /
E Ramsey-Turan / F fresh-2023-26), each adversarially novelty-checked vs AlphaEvolve / FunSearch /
specialist tables. Goal framing: research_notes/FUNSEARCH_TARGET_GOAL.md. Survey files:
research_notes/hunt_funsearch_{A..F}_*.md.

## Meta-finding (changes the strategy)
The LLM-evolutionary-construction paradigm is ALREADY deployed across the prestige extremal domains
mid-2026, so those are crowded/owned:
- **Coding/design theory** — CPro1 (arXiv 2603.00174, Feb 2026), a 4000-program o4-mini fleet, improved
  24 constant-weight code bounds. Domain actively swept.
- **Ramsey/Turan** — AlphaEvolve/RGCS (2603.09172, Mar 2026) swept 2-color off-diagonal cliques;
  OpenEvolve (2605.01120, May 2026) swept Zarankiewicz z(m,n;3,3).
- **Geometry packing/Heilbronn/kissing** — AlphaEvolve (2511.02864, 2025) + Packomania + Friedman.
The clean ELBOW-ROOM left for a sample-limited fleet is the NICHE long tail the big sweeps skipped:
combinatorics-on-words and specific finite point/vector configurations with an OEIS-citable record.

## Ranking (realistic-shot-in-weeks × not-owned × exactly-verifiable × significance)

1. **[WINNER] C — Maximum acute set in {0,1}^n (OEIS A089676).** Beat a standing 2018 lower bound;
   softest = **a(13) ≥ 33** (also a(11)≥24, a(12)≥32). Verification = pure integer dot-product
   `(P^Q)&(R^Q)≠0` (instant, anyone-checkable). Records heuristic, UNIMPROVED since 2018; literature
   says naive search fails → STRUCTURE-bottleneck = our edge. Tiny mutable binary objects. NOT in
   AlphaEvolve/FunSearch/Packomania/SAT. Independently re-verified vs OEIS record #108 (May 30 2026).
   Failed pilot = a cheap clean negative. **Pilot launched on this.**
2. **F — Binary orientable sequences, small order (OS(8): 92 vs upper bound 96, exact max OPEN).**
   Bit-exact millisecond verify; 2^96 necklaces unenumerable → structure-bottleneck; records
   heuristic; no AlphaEvolve/FunSearch connection found. **Strong backup** if C is a hard plateau.
3. **A — Discrete Heilbronn triangle on the n×n lattice (OEIS A248866).** Integer-exact, untouched
   since 2015, continuous Heilbronn is AlphaEvolve-owned but the DISCRETE lattice variant is unswept.
   Weaker deliverable: a record CONFIG / {5,6}-conjecture test (exact optimality needs an upper-bound
   argument). Solid #3.
4. **E — Multicolor quadrilateral Ramsey r_k(C_4), r_5∈[27,29].** Only viable as STRUCTURED algebraic
   search (blind = 5^351, FLOPS-dead); domain now AlphaEvolve/OpenEvolve-swept. Time-sensitive.
5. **D — Four MOLS of order 22 (N(22)≥4).** Famous decades-open small case but a SWING not a tap-in
   (survived decades of IP/constraint campaigns); coding domain actively CPro1-swept. Too hard for a
   weeks-pilot; a fallback CAMPAIGN target only.
6. **B — Erdős #213 integral octagon.** Dormant 18 yrs but HIGH existence-risk (Kreisel-Kurz exhausted
   diameter 70000); erdosproblems is thin non-owned ground (≈ {#213, #769}).

## Decision
Pilot = **C (A089676 acute sets), primary target 34 in {0,1}^13**. F held as the backup pivot.

## Pilot setup (done before launch)
- Independently confirmed the record vs OEIS directly (a(0..10)=1,2,2,4,5,6,8,9,10,16,17; a(11..15)
  lower bounds 24,32,33,64,128, Kamenetsky 2018, unchanged at edit #108).
- Built + validated a TRUSTED exact verifier code/acute_pilot/verify.py (PASSES all 5 record
  witnesses). Key identity: cube-vertex angle at apex Q is right iff (P^Q)&(R^Q)==0; no obtuse angle
  possible, so acute ⟺ no right angle.
- Ruled out the free structural shots: single-coordinate split and delete-coordinate+greedy-repair of
  the structured a(14)=64 / a(15)=128 sets top out at 32 (the codes are balanced/tight). So 33 is a
  genuine plateau → a real search problem.

## Pilot fleet (5 agents, launched 2026-06-27)
1. c_localsearch — high-throughput C greedy + (1,k)-swap local search, all cores.
2. structure — analyze the 64/128 code structure; extend/shorten/coset to length ≤13; recursive
   a(k+2m)≥a(k)a(m) / Bevan a(3k)≥a(k)^2 + repair.
3. penalty_sa — fixed-cardinality SA/tabu/min-conflicts, drive right-angle violations to 0 at k=record+1.
4. exact_cp — CP-SAT / lazy-clause SAT / branch-and-bound on the SMALL instances (n=11 target 25,
   n=12 target 33).
5. verify_novelty — independent SECOND from-scratch verifier (no bitmask trick) cross-checking every
   witness; web re-confirm records still unbeaten; OEIS-submission template.

Every claimed record-beating witness must pass BOTH verify.py and the independent verify2.py before it
counts. Result (record beaten / clean negative + plateau evidence) to be consolidated after fleet return.
