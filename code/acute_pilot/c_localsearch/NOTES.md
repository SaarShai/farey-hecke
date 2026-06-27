# A089676 — high-throughput local search for acute sets in {0,1}^n

Goal: BEAT an unimproved Kamenetsky-2018 lower bound for the max ACUTE set in the n-cube.
Targets: a(13)>=34 (primary), a(11)>=25, a(12)>=33, a(14)>=65 (secondary).

## Core fact used everywhere
For 0/1 vectors P,Q,R the angle at apex Q is a RIGHT angle iff `((P^Q)&(R^Q))==0`.
No obtuse angle is possible (dot >= 0 always), so a set S is ACUTE iff NO ordered triple
(apex, leg, leg) has a right angle. `can_add(S,x)` is O(|S|^2): check (A) apex=x over all
pairs in S, and (B) apex=q in S with one leg = x over all other points.

## Symmetry (verified)
Acuteness is invariant under (1) XOR by any fixed vector t, and (2) any coordinate permutation.
v3 uses this to randomize seeds (random t + random perm) so the SAME record seed lands in many
different local-search basins. Also used: any subset of an acute set, projected by dropping a
coordinate after restricting to one value of it, is acute -> "split-down" seeding from a(n+1).

## Programs (all use the (P^Q)&(R^Q)==0 test, pthreads, all cores)
- `acute.c`   v1 — randomized greedy + (1,k)-swap plateau search, single flat seed.
- `acute2.c`  v2 — split-down seeding from a(n+1)/a(n+2) records (subset-projection -> guaranteed
                   acute seeds), perturb-refill local search, near-miss seed recycling.
- `acute3.c`  v3 — adds symmetry-randomized seeds + best-improvement (lookahead-1) refill + larger
                   plateau patience. Strongest variant.
- `acute_sa.c` SA — fixed-size simulated annealing minimizing # right-angle triples (energy 0 = acute
                   set of that exact size). Move = replace one vertex; delta via per-slot recount.
- `augment.c`  EXACT small-k augmentation test: given an acute set of size m, search COMPLETELY for a
                   way to reach m+1 by remove-k / add-(k+1). k=0 (single addable vertex) and the
                   remove-k loops are exhaustive over all combinations; the "add j vertices" inner
                   search is complete backtracking over the addable-candidate set. A definitive
                   local-optimum certificate.

## Results (this run)
| n  | record (2018) | best reached here | beaten? |
|----|---------------|-------------------|---------|
| 9  | 16 (exact)    | 16                | n/a     |
| 11 | 24            | 24                | no      |
| 12 | 32            | 32                | no      |
| 13 | 33            | 33                | no      |

Best witnesses saved in `witnesses/` and each PASSES the trusted `verify.py`:
- `witnesses/best_n11_size24.txt`  -> verify.py PASS (size 24, n=11)
- `witnesses/best_n12_size32.txt`  -> verify.py PASS (size 32, n=12)
- `witnesses/best_n13_size33.txt`  -> verify.py PASS (size 33, n=13)

## RIGOROUS local-optimum certificate (strongest finding)
`augment` was run on each record set. Result — EXHAUSTIVELY, no augmentation to size+1 exists by
removing up to 3 points and re-adding up to 4 (all removal-combinations enumerated; complete
backtracking on additions):
- n=11 record (24): k=0 none addable; 1-stable (24 combos); 2-stable (276); 3-stable (2024 triples).
- n=12 record (32): k=0 none; 1-stable (32); 2-stable (496); 3-stable (4960).
- n=13 record (33): k=0 none; 1-stable (33); 2-stable (528); 3-stable (5456).
So all three records sit in deep local optima: not reachable from size+1 by any small (<=3) repair.
This is a complete, deterministic certificate (not a heuristic stall), and it explains why the
randomized local searches pin exactly at the record and never tunnel out.

## Honest read on difficulty
- From a COLD start, naive greedy reaches a(11)=24 trivially, but only ~26/33 for n=12 and ~29/33
  for n=13 — i.e. the records are NOT reachable by simple greedy; they sit on a hard plateau.
- All three local-search variants (v1/v2/v3), seeded from the records and from a(n+1)/a(n+2)
  split-downs with symmetry diversification, reliably re-find the records but did NOT exceed any of
  them within the compute spent here (16 cores, ~20+ min on n=13 alone, shorter on n=11/n=12).
- Simulated annealing (acute_sa) is markedly WEAKER on this landscape: replace-one-vertex moves get
  stuck with nonzero residual energy well below the record size. Greedy-feasible local search is the
  right tool here; the bottleneck is the combinatorial plateau, not the move primitive.
- These bounds have stood unimproved 2018->2026 across multiple searchers; +1 appears to be a genuine
  hard plateau, consistent with what we observe (long stalls exactly at the record size).

## Verification protocol followed
Every reported size is a 0/1 file re-checked by the TRUSTED `code/acute_pilot/verify.py` (independent
of our C checker). No size is claimed without a quoted verify.py PASS.
