# A089676 exact/near-exact attack — NOTES

Target: BEAT the standing lower bounds (Kamenetsky 2018, unimproved through 2026)
- a(11) >= 24  (find a 25-vertex acute set in {0,1}^11)
- a(12) >= 32  (find a 33-vertex acute set in {0,1}^12)
- a(13) >= 33
A proven improvement (explicit 0/1 witness passing the trusted verifier) is the win.
An exact UPPER bound (e.g. a(11)=24) would be secondary but notable.

## Problem recap
A089676(n) = max size of S ⊆ {0,1}^n with NO right angle among any ordered triple.
Right angle at apex Q between P,R ⇔ (P^Q)&(R^Q)==0. (No obtuse angle possible for 0/1
vectors, so right angle is the only forbidden case.) = max independent set in the
3-uniform hypergraph of "right-angle triples".

Known exact: a(0..10) = 1,2,2,4,5,6,8,9,10,16,17 (a(10)=17 proven by Cariboni via
combinatorial search). Records a(11..15) >= 24,32,33,64,128 are LOWER bounds only.
Note: 24 = a(5)·a(3) = 6·4 and 32 = a(6)·a(3) = 8·4 — the records are exactly the
product-construction lower bounds a(k+2m) >= a(k)·a(m).

## Key structural reduction (verified, analyze_struct.py)
Translation by any vector t (XOR) and coordinate permutation preserve acuteness ⇒ WLOG 0 ∈ S.
With 0 ∈ S, a triple {0,P,R} is forbidden iff  P&R==0  OR  P⊆R  OR  R⊆P.
So S\{0} must be a CLIQUE in the "0-compatible" graph G (edge = P,R overlap AND
incomparable), PLUS satisfy the all-nonzero triple constraints.
- BUT G is extremely dense (avg degree ~1783/2047 for n=11), so the clique part barely
  prunes; the genuine 3-uniform all-nonzero triple constraints are the real difficulty.
- ~13% of 0-compatible triples are STILL forbidden ⇒ problem does NOT reduce to max clique.

## Methods tried & tractability (HONEST)

### 1. CP-SAT (OR-tools) lazy-clause loop — FAILS to converge (cpsat_lazy.py)
Decision model: x_v binary, fix x_0=1, Σx_v ≥ K, eager pairwise 0-compat clauses,
LAZY all-nonzero triple clauses (solve → extract S → block violated triples → repeat).
THRASHES: even for the KNOWN-feasible n=10,K=17 it found a fresh size-17 set each iter,
each violating ~50–90 triples; after 65 iters / 30k lazy clauses still not converged.
The triples are far too numerous to discover one configuration at a time.
Eager triple enumeration is infeasible: 0-compatible graph density >0.88 on candidate
pools of 1000+ vertices ⇒ tens of millions of forbidden triples. NOT VIABLE at this scale.

### 2. Exact branch-and-bound (backtrack.py) — correct but does NOT scale
MIS-style enumeration with 0 fixed + candidate pruning + |S|+|C|≤best bound.
Validated EXACT: n=5→6, n=6→8, n=7→9 all COMPLETED, match OEIS.
BUT: n=7 = 1.6M nodes / 35s; n=8 TIMES OUT at 2M nodes. Node count explodes.
⇒ Exact proof of an upper bound at n=11 is COMPLETELY INFEASIBLE (search space
astronomically beyond n=8). Documented as a hard wall, not pursued further.

### 3. Simulated annealing / local search (sa_*.py) — validated, competitive
Fixed-size-K min-conflicts formulation (conflicts = # forbidden triples; acute ⇔ 0).
Best engine (sa_best.py): numpy full-candidate-scan picks the GLOBAL best swap-in each
move + incremental per-vertex conflict updates; tabu + kicks. Validated:
- Reproduces a(10)=17 in 0.3s, and a(11)=24 FROM SCRATCH in ~80s (independent witness,
  PASSES trusted verify.py).
- At K=25 (n=11): plateaus around ~10 conflicts; could not reach 0.

### 4. Large-Neighborhood Search = destroy + EXACT repair (lns.py) — strong, decisive locally
Keep a core of the acute set, remove d vertices, EXACT-backtrack the optimal refill.
The exact `max_extension` is INSTANT for cores ≥16 (candidate set tiny) ⇒ verifiable.
- Seeded from the known 24-set, seeking 25, destroy d∈{6,8,10,12}: reached only 24
  (exact repair completes in 0.0s and PROVES no 25-extension for those cores).
- ⇒ The known 24-basin is ROBUST: even destroying half the set and optimally refilling
  cannot escape to 25.

## Findings
- BOTH the published a(11)=24 set and an independently SA-found 24-set are MAXIMAL: no
  single vertex can be added (0 extensions out of 2048). So a 25-set, if it exists, is
  NOT a superset of any addition-maximal 24-set — it must be structurally different.
- Translated-to-0, the n=11 record uses only EVEN popcounts {0,4,6,8}; n=12 uses {0,5,6,8,9}.
- Restricting the candidate pool to even-popcount HURT search (worse plateau than full pool).
- An independently SA-found 24-set shares only 6/24 vertices (best over all translations) with
  the published record ⇒ a genuinely DIFFERENT 24-set, also addition-maximal. Two distinct
  24-basins, both fail to extend to 25.

## d-STABILITY CERTIFICATES (exact, sound, multiprocessing — stability.py)
"d-stable" = exhaustively remove EVERY d-subset of the record's non-zero vertices and run an
EXACT backtracking refill seeking R+1; if NONE reaches R+1, the R-set is provably d-stable
(⇔ every (R+1)-set must differ from the record in MORE than d vertices, i.e. share < R−d of them).

SOUNDNESS: each per-subset exact search has a time limit; the certificate is valid only if
EVERY search COMPLETED (exhausted), not timed out. stability.py tracks timeouts and reports
"[SOUND]" only when 0 timeouts. (`max_extension.last_timed_out` flag.) Validated:
max_extension correctly finds known extensions and correctly returns None for maximal sets.

Results (n=11, published a(11)=24 set; seeking 25) — ALL CONFIRMED:
- d=2: 253 subsets — STABLE.
- d=3: 1,771 subsets — STABLE.
- d=4: 8,855 subsets — STABLE.
- d=5: 33,649 subsets — STABLE.
- d=6: 100,947 subsets — STABLE [SOUND]: all 100,947 exact searches COMPLETED, 0 timeouts (473s).
  ⇒ the published a(11)=24 set is PROVABLY 6-STABLE: any acute 25-set must differ from it in
    MORE than 6 vertices (share ≤17 of the 24).
- independent (different-basin, shares only 6/24) 24-set: d=4, 8,855 subsets — STABLE [SOUND]
  (all completed). A second, structurally different 24-set is also exact-certified 4-stable.

Results (n=12, published a(12)=32 set; seeking 33):
- a(12)=32 set is addition-MAXIMAL (0 single extensions).
- d=3: 4,495 subsets — STABLE.
- d=4: 31,465 subsets — STABLE (cores size 28, instant ⇒ sound).

⇒ Both records are robustly locally optimal: no replacement of up to d (n=11: 6; n=12: 4)
  vertices reaches the next size. Verifiable evidence of robustness, NOT a global proof.

## FROM-SCRATCH SEARCH RESULT (primary target, K=25 n=11)
14-worker SA fleet (sa_best engine), 30 min, diverse random starts + restarts + kicks:
ALL 14 workers converged to exactly 10 forbidden triples (distribution [10×13, 11]).
A 25-set has C(25,3)=2300 triples; the best reachable had 10 still-forbidden — a tight,
reproducible plateau across every independent worker. NO acute (0-conflict) 25-set found.
The uniform floor at 10 across independent basins is strong (if heuristic) evidence that an
acute 25-set is at best extremely rare in {0,1}^11.

## HONEST OUTCOME
- NO improvement to any record found. a(11)≥24, a(12)≥32, a(13)≥33 stand.
  Best K=25 search (from scratch, diverse fleet + hybrid) plateaued at ~10 forbidden triples
  (out of C(25,3)=2300 triples) — close, but no acute 25-set.
- NO exact upper bound improved either: full exact enumeration is infeasible (already times out
  at n=8). The trivial a(11) ≤ 2^11 is unimproved.
- The DURABLE, verifiable artifacts:
  1. A clean, validated toolchain: exact backtracking (matches OEIS a(5..7) with COMPLETED
     proofs), strong SA (reproduces a(10)=17 and a(11)=24 from scratch), LNS exact-repair,
     and a hybrid — all cross-checked by the trusted verify.py.
  2. Exact d-stability certificates: the published a(11)=24 set is d-stable up to d shown above,
     and a second, structurally-different 24-set is also stable — concrete computational
     evidence that 24 is hard to beat in dim 11. Same for a(12)=32 (d≤4).
  3. Independent reproduction of records (witnesses differ from published yet PASS verify.py).

## Files
- core.py            — bitmask acute checker (mirrors verify.py logic)
- analyze_struct.py  — verifies the 0-fixed {0,P,R} reduction + 0-compatible graph stats
- cpsat_lazy.py      — CP-SAT lazy-clause loop (documents the thrashing failure)
- backtrack.py       — exact branch-and-bound (proves a(5..7); times out n≥8)
- sa_best.py         — BEST SA engine (numpy full-scan best-swap + incremental conflicts)
- sa_fast.py, sa_v2.py, sa_v3.py, sa_numpy.py, sa_engine.py — engine iterations (kept for record)
- lns.py             — Large-Neighborhood Search: destroy + EXACT refill (max_extension)
- hybrid.py          — SA → exact-repair of the conflicting region
- fleet.py / hybrid_fleet.py — multiprocessing drivers for the above
- stability.py       — exhaustive d-stability certificates (sound, parallel)
- driver.py          — multi-seed/mode SA driver
- verify_all.sh      — re-checks EVERY witness here with the trusted verify.py
- *witness*.txt      — verified acute sets (incl. independent a(10)=17, a(11)=24 reproductions)

## How to reproduce
- Validate engines:    python3 code/acute_pilot/exact_cp/sa_best.py 11 24 120 7 all   (→ size 24)
- Exact small-n proof: python3 code/acute_pilot/exact_cp/backtrack.py 6 - 60          (→ 8, COMPLETED)
- Stability cert:      python3 code/acute_pilot/exact_cp/stability.py 11 5 8          (→ 5-STABLE)
- Re-verify all:       bash code/acute_pilot/exact_cp/verify_all.sh
