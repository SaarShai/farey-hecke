# Fixed-cardinality penalty search for OEIS A089676 (acute sets in {0,1}^n)

## Goal
Beat a Kamenetsky-2018 record lower bound by exhibiting an acute set of size
record+1. Primary: **34 in {0,1}^13** (record a(13)≥33). Also: 25 in dim 11
(a(11)≥24), 33 in dim 12 (a(12)≥32).

A set S ⊆ {0,1}^n is *acute* iff no ordered triple (apex Q; legs P,R) forms a
right angle, i.e. never (P^Q)&(R^Q)==0. (Obtuse is impossible for 0/1 vectors,
so right angles are the only forbidden configuration.)

## Method
Fixed-cardinality **penalty optimization**: hold the target size k fixed,
energy = number of right-angle violations, drive energy → 0. Three engines,
each its own move operator (all share the SAME violation counter, validated
against the trusted `verify.py` zero-set — every record set gives energy 0 in
each engine):

- `sa.c`  — simulated annealing, single-vertex replacement, involvement-biased
  vertex selection, reheat-on-stagnation. Fast (~1M moves/s).
- `sa2.c` / `sa3.c` — min-conflicts full/bounded candidate scan, WalkSAT-style
  focused repair. (Slower; superseded by LNS.)
- `lns.c` / `lns2.c` — **Large-Neighborhood Search (destroy & repair)**: remove
  D high-involvement vertices, greedily (lns) or randomized-greedily (lns2,
  Boltzmann window + variable D) re-insert at min-added-violation positions.
  This is the operator that escaped the SA floor.

Seeding: record set R (size = record) as the anchor, plus the best extra
vertex (chosen by exhaustive min-added-violation scan) to form the size-(record+1)
start state. Random-init starts were also run for diversity.

## Key structural finding (exhaustive, exact)
For each n, scan ALL candidate "extra" vertices v ∉ R and count violations that
adding v to the record set R would create (R itself is acute = 0 violations):

| n  | record \|R\| | min added-violations over all v | # vertices achieving it |
|----|-----------|--------------------------------|------------------------|
| 11 | 24        | 14                             | 40                     |
| 12 | 32        | 25                             | 96                     |
| 13 | 33        | **7**                          | **1 (unique)**         |

So *without modifying R*, the cheapest size-(record+1) set has 7 violations for
n=13 (and they ALL involve the one good extra vertex). n=13 is by far the most
favorable target; n=12 is the hardest (min 25).

## Search results (energy = # unordered right-angle violations)

| target           | engine          | lowest energy reached |
|------------------|-----------------|-----------------------|
| n=13 k=34        | single-vertex SA| 7  (= the R-anchored floor) |
| n=13 k=34        | LNS destroy/repair | **4** |
| n=11 k=25        | SA / sa2        | 10 |
| n=12 k=33        | SA              | 25 |

The descent for the primary target: SA bottoms at **7** (exactly the "keep R,
add best vertex" floor — confirmed by the exhaustive table). LNS escapes that
basin and reaches **4**, robustly, across many independent workers / both greedy
and randomized repair / variable destroy size. Driving below 4 did not occur in
the budget spent.

## Local-optimality probes (exact, exhaustive single-vertex)
- The n=13 **E=7** state (record set R + unique best extra vertex) is a *strict
  local minimum under all single-vertex changes*: `probe.c` exhaustively tried
  every value at every position and found NO improving move. This is exactly why
  single-vertex SA cannot beat 7.
- A captured n=13 **E=4** state (from LNS) is *also 1-opt optimal* — no single
  vertex change lowers it. Escaping it needs a coordinated ≥2-vertex move.
- `probe3.c` ran an exhaustive 2-change and a pruned 3-change restricted to the
  (only 7) violation-involved vertices, with candidate values from the
  Hamming-≤2 pool around the current set (3086 values). **Result: 2-change
  best=4, 3-change best=4** — i.e. NO coordinated 2- or 3-vertex change in the
  structurally-plausible neighborhood improves the E=4 state at all. The E=4
  minimum is 1-opt, 2-opt, AND 3-opt optimal. (`probe3.log`)
- The 2-change delta-energy was validated exact vs full recount (20000 random
  trials, all correct — `chk2.c`).

## Honest read on the landscape
- The record set R for n=13 is a **very tight, deep local optimum**. Every
  independent single-vertex-SA run from its basin returns to exactly energy 7;
  random restarts land far worse (E≈30–42), i.e. the good basin is special and
  hard to reach except by seeding from R.
- LNS (destroy-and-repair) is the only operator that broke the SA floor (7→4),
  but it then plateaus at energy 4 just as robustly.
- For n=11 (floor 10) and n=12 (floor 25 = the exhaustive add-one minimum) the
  search essentially cannot repair the record set to absorb an extra vertex.
- **No record was beaten.** The closest approach is the primary target n=13
  k=34 at energy 4 (4 right-angle violations away from a size-34 acute set),
  and that E=4 state is provably 1/2/3-opt optimal in the plausible
  neighborhood. This is consistent with the records being genuinely hard /
  near-optimal at these dimensions: the penalty landscape for k=record+1 has a
  deep nonzero floor that local search (SA, WalkSAT, LNS up to 3-opt repair)
  cannot cross within a substantial multi-core budget.

## Final best witnesses (best-found, NON-acute — for the record, not a record)
- `best_n13_k34_e4.txt`  — size 34 in {0,1}^13, **4** unordered right-angle
  violations (closest to the a(13)≥33 → 34 goal).
- `best_n11_k25_e10.txt` — size 25 in {0,1}^11, **10** violations.
- `best_n12_k33_e25.txt` — size 33 in {0,1}^12, **25** violations.
Each independently recounted and run through `verify.py` (all correctly report
acute=False, i.e. NOT a valid acute set). No `verify.py` PASS is claimed.

## Verification protocol
Any energy-0 hit is written as a 0/1 witness and MUST pass:
`python3 ../verify.py <file> 13` (exit 0 + PASS). No such hit was produced, so
no PASS is claimed. The violation counter in every engine was validated to give
energy 0 on all five record witnesses (matching the trusted verifier's zero set).

## Files
- `sa.c sa2.c sa3.c lns.c lns2.c` — search engines (C, single-thread; run many
  in parallel for fan-out).
- `sa.py` — original Python SA + the exact `replace_delta` validation harness
  (delta vs full recount: ALL CORRECT over 300 random trials).
- `seed_n{11,12,13}.txt` — record sets as decimal masks (seeds).
- `seedplus_n13_*.txt`, `seedlow_n13_*.txt` — record set + best/low extra vertex.
- `runs/` — campaign logs and BEST-energy witness states (non-zero).
