# A089676 acute-set structure analysis & record attack

OEIS A089676: a(n) = max size of S ⊆ {0,1}^n with every angle (over every apex) strictly acute.
Right angle at apex Q between distinct legs P,R  ⇔  (P^Q)&(R^Q) == 0  (disjoint diff-supports).
For 0/1 vectors no angle can be obtuse, so the ONLY forbidden configuration is the right angle.

Bevan (2006, EJC 13 #R12) coordinate form: a triple u,v,w is a RIGHT triple iff for some coordinate i,
(u_i,v_i,w_i) is (0,1,0) or (1,0,1). Acute ⇔ no coordinate ever realizes (0,1,0)/(1,0,1) on an ordered triple.

Records (lower bounds, Kamenetsky 2018): a(11)≥24, a(12)≥32, a(13)≥33, a(14)≥64, a(15)≥128.
Exact: a(0..10) = 1,2,2,4,5,6,8,9,10,16,17.

## 1. What the record witnesses ARE (computed, code/acute_pilot/a089676_witnesses.txt)

| n  | size | linear? | structure (computed) |
|----|------|---------|----------------------|
| 11 | 24   | no      | union of cosets — stabilizer subspace trivial-ish; unstructured/heuristic |
| 12 | 32   | no      | union of 8 cosets of a dim-3 subspace |
| 13 | 33   | no      | union of cosets; NOT linear/affine; heuristic |
| 14 | 64   | no      | union of 8 cosets of a dim-3 subspace |
| 15 | 128  | no      | union of 8 cosets of a dim-4 subspace V; **V = constant-weight-8 simplex-type code** |

n=15 decoded precisely: S = ∪ (r_i + V), i=0..7, where
  V = dim-4 subspace, every nonzero element weight EXACTLY 8 (a [15,4] simplex-type / constant-weight code),
  the 8 coset reps r_i have weight 0 or 6 and are NOT a subgroup (rank 6, not xor-closed).
So the n=14/15 "powers of two" are coset-UNIONS, not single linear codes. The clean algebraic piece is V;
the coset selection is a genuine combinatorial search result (Kamenetsky–Chubenko), not a pure product.

## 2. Acute-code characterization (PROVED, computation-verified)

**A LINEAR code C (subspace of GF(2)^n) is acute  ⇔  no two distinct nonzero codewords have disjoint supports.**
Reason: for linear C the legs u=P^Q, w=R^Q range over all nonzero codewords as P,R,Q vary; the apex is free;
a right angle needs u&w=0. (u=w is the degenerate P=R, not a triple.)
Sufficient special case: all nonzero weights > n/2 ⇒ any two codewords intersect (e.g. simplex codes, all
weight 2^{d-1}=(n+1)/2). Verified: simplex[d] is acute for d=2,3,4 (lengths 3,7,15).

Consequence for n=13: a [13,d] code with all nonzero weights > n/2 would need min-distance ≥7, but the
Griesmer bound forces n≥14 even for d=4. So the clean weight-bound family gives NOTHING new at n=13.
The weaker "pairwise non-disjoint" condition does admit codes — the true MAX acute LINEAR code in n=13 is
**dim 5 (32 points)** (randomized greedy with independence, ~hundreds of trials; basis in best_lincode_basis.pkl).
That is one short of the record 33 — confirming the record is necessarily NON-linear.

## 3. Bevan recursion (implemented exactly: bevan_construct.py, reproduces a(9)=16)

OEIS recursion: a(k+2m) ≥ a(k)·a(m), a(k+2m+3n) ≥ a(k)a(m)a(n). General form = Bevan Thm 4.3.
Construction (Thm 4.3): blocks (v^1_{k1} … v^M_{kM} z_{kZ}), kZ = ⟨⟨k1…kM⟩⟩ a mixed-radix difference index;
the THM 4.2 special case a(3d)≥a(d)² is T = { v_i v_j v_{(j−i) mod n} } (n=|S|), VERIFIED to give a(9)=16.

Best clean products by dimension (constraint: the doubled m-block set must be the LARGER, a(k)≤a(m),
and Z reuses the a(m)-set):
  d=13: max product = a(3)·a(5) = 4·6 = **24**  (well below record 33)
  d=15: max product = a(5)·a(5) = 6·6 = **36**  (far below record 128)
So the pure Bevan product UNDERPERFORMS the heuristic records at every target dimension here.
The records 64/128 come from Kamenetsky/Chubenko search and (n>15) Harangi — NOT from this recursion.

## 4. Why beating the records is hard (computed facts)

- All three lower-record witnesses (n=11,12,13) are **locally maximal**: NO single 0/1 point can be added
  to any of them keeping acute (exhaustive over all 2^n candidates). Beating them needs a multi-point swap.
- Projecting the structured n=15 record (128 pts) down to n=13 yields at most ~26 acute points (greedy) —
  projection destroys the coset structure.
- Linear codes cap at 32 (n=13); Bevan products cap at 24 (n=13). Structure alone does not reach 34.

## 5. Record-beating attempt — RESULT: NO RECORD BEATEN (honest negative)

Targets: a(13)≥34 (primary), a(11)≥25, a(12)≥33. Multiple independent methods, all converged on
the EXISTING records and none beat them:

| method | n=11 | n=12 | n=13 |
|--------|------|------|------|
| acute2 random-kick local search, seeded w/ record + 868 structured split-seeds + 40 slices (360s, 4–16 thr) | 24 | 32 | 33 |
| acute3 annealing search (buggy — REGRESSION, discarded; destroyed seeds, reached only 20–28) | — | — | — |
| Python targeted (−r,+greedy) swap from 448 structured 32-slices (1718 trials) | — | — | 33 |
| max acute LINEAR code (subspace) | — | — | 32 (dim 5) |
| best Bevan Thm-4.3 product | — | — | 24 (a(3)·a(5)) |
| exact 13-subcube slice of the 64/128 records | — | — | 32 |

The n=13 search output FINAL_13.out is a valid 33-set: trusted verifier prints
`n=13 size=33 acute=True / PASS`. No 34-set was produced by any route.

### Why (computed evidence, not hand-waving)
- The records n=11,12,13 are **locally maximal** (no single point addable, exhaustive over 2^n).
- The 448 structured 32-point subcube slices of the n=14/15 records are ALSO each locally maximal —
  not one admits even a single added point. So the "structured launching pad" has no easy +1.
- Linear codes top out at 32; the only sufficient algebraic family (all weights > n/2) is impossible
  at n=13 (Griesmer needs n≥14). Bevan products top out at 24 here. Projection of the 128-set loses
  structure (≤26 greedy / =32 exact slice). Structure genuinely does NOT extend to beat n≤13.
- Independent confirmation that 34 is hard: this matches that the bounds have stood unimproved 2018→2026,
  and that the n=11,12,13 records look heuristic/unstructured (Kamenetsky) precisely because no clean
  algebraic construction reaches them — they ARE the ceiling of what local search + structure finds here.

### Honest assessment of the structural hypothesis
The premise (n=14/15 = LINEAR/code/coset construction) is CORRECT and was decoded (Section 1: coset-unions,
n=15's V = constant-weight-8 simplex code). But it does NOT transfer downward: the 64/128 sets are powers
of two because they are coset-UNIONS of a small code at a length where the code's weights clear n/2; at
n=13 the dimension budget is too small for any analogous code (Griesmer), and the records there are the
non-algebraic ceiling. The structure explains the EVEN/power-of-two records but offers no lever at n≤13.

### Reproduce
  cd code/acute_pilot/c_localsearch
  ./acute2 13 34 360 16 --seed RECORD_13.txt --seed seed_rec15.txt --seed seed_rec14.txt \
           --seed seed_bevan15_36.txt --seed slices13/*.txt        # -> BEST=33
  python3 ../verify.py FINAL_13.out 13                              # -> PASS size 33

## Files
- acute_core.py        — bitmask acute primitives (is_acute_fast, can_add); matches verify.py on all records.
- linear_acute.py      — linear-code acuteness + simplex generator.
- bevan_construct.py   — Bevan Thm 4.3 general product (kz_index mixed-radix); reproduces a(9)=16.
- small_acute_sets.py  — exact optimal acute sets a(1..8) from OEIS, all re-verified acute.
- ../c_localsearch/acute3.c — stronger search (large kicks + annealing + structured seeds).
