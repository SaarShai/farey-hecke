# Exact multidimensional prefix balance: quota words, certificates, and constrained ordering

Working paper, 2026-07-15.  This is a proof-qualified project manuscript, not
an external novelty or priority claim.  Its implemented labels are subordinate
to the independent verifier and release artifacts.

## Abstract

We study finite orders whose every prefix should represent the progress-weighted
total of several declared features.  Exact centering turns the problem into
ordering zero-sum rational vectors to minimize maximum prefix
`L-infinity` norm.  This contains García's one-dimensional centered-gap delta
exactly.  For equal-mass one-hot categories, occurrence windows reduce the
problem to unit-job scheduling.  A house-monotone quota path establishes
feasibility, and release-aware earliest-deadline-first scheduling constructs a
quota word in `O(N log C)` time and `O(C)` working memory.  The result has
discrepancy below one and a strict factor below three relative to the true
unconstrained categorical optimum.  In the binary case, nearest-integer
mechanical prefixes are simultaneously optimal at every prefix.  For small
general instances we give a trace-aware two-pass subset dynamic program.  For
blocks, end pins, and precedence constraints we give exact feasibility checks
and independently checkable a-posteriori bounds, but no inherited free-order
factor.  The application claim is limited to balance of declared finite cells.

## 1. Exact contract and relation to the gap problem

Let `I={1,...,N}`.  Item `i` has a distinct identifier, a positive integer
progress mass `w_i`, and an exact rational contribution vector
`a_i in Q^d`.  Put

```text
W = sum_i w_i,                 A = sum_i a_i,
u_i = W a_i - w_i A.
```

Then `sum_i u_i=0`.  For a permutation `pi`, let

```text
P_k(pi) = sum_{j=1}^k u_{pi(j)},       P_0=0,
B(pi)   = max_{0<=k<=N} ||P_k(pi)||_infinity / W,
Q(pi)   = sum_{k=1}^N ||P_k(pi)||_infinity / W.
```

The primary objective is `B`; `Q` is minimized only among orders attaining the
globally smallest `B`.  Unless constraints are stated, the comparison set is
all permutations of the labelled items.  All norms in this paper are
`L-infinity` except in explicitly delimited prior-art remarks.

### Theorem 1 (progress-weighted centering and exact one-dimensional reduction)

**Assumptions.** Contributions are rational, masses are positive integers, and
the comparison set is any fixed collection of feasible permutations.

**Claim.** At prefix `k`,

```text
P_k/W = sum_{j<=k} a_{pi(j)}
        - (sum_{j<=k} w_{pi(j)} / W) A.                 (1.1)
```

Thus `B` is the largest coordinate error between accumulated contribution and
the progress-proportional share of the final contribution.  If
`g_1,...,g_N` are exact rational gaps summing to one, set `d=1`, `w_i=1`, and
`a_i=g_i`.  Then

```text
P_k/W = sum_{j<=k} g_{pi(j)} - k/N,                    (1.2)
```

exactly García's local prefix delta.

**Proof.** Sum `u_i=W a_i-w_i A` over the prefix and divide by `W`; (1.1)
follows.  In the gap case `W=N` and `A=1`, giving (1.2).  The identity is
algebraic and does not change when the comparison set is restricted.  QED

**Complexity and implementation status.** Once centered vectors are available
or generated sequentially, exact streaming evaluation costs `O(Nd)` rational
coordinate operations and `O(d)` evaluator state.  V1 validation currently
materializes all centered vectors before evaluation, so the implemented general
path uses `Theta(Nd)` input-derived storage.  It accepts integers and exact
fractions; binary floating point receives no exact theorem label.  The existing
gap interface and the new exact-vector interface use the same identity.

### Categorical specialization

Let each item have unit mass and category `c`, and put `a_i=e_c`.  If category
`c` has total count `n_c` and prefix count `x_c(k)`, then

```text
P_k[c]/N = x_c(k) - k n_c/N.                           (1.3)
```

Accordingly, categorical `B` is the largest absolute deviation of any declared
category count from its fractional prefix quota.  A joint stratum is simply a
category whose label is a tuple of declared feature levels.  Equation (1.3)
does not control variation within a cell or an unrecorded feature.

## 2. Quota windows and the scalable constructor

Assume `N=sum_c n_c>0`, discard zero-count categories from scheduling, and let
`C` be the number of positive categories.  Label the occurrences of category
`c` by `j=1,...,n_c` in their time order.  Define

```text
r(c,j) = floor((j-1)N/n_c)+1,
d(c,j) = ceil(jN/n_c).                                 (2.1)
```

Time slots and occurrence positions are `1,...,N`.

### Theorem 2 (quota-window equivalence)

**Assumptions and comparison set.** Counts are nonnegative integers with
positive total.  The comparison set is every category word with exactly the
given inventory.  The norm is the categorical `L-infinity` norm in (1.3).

**Claim.** A category word satisfies, for every `c` and `0<=k<=N`,

```text
floor(k n_c/N) <= x_c(k) <= ceil(k n_c/N)              (2.2)
```

if and only if occurrence `(c,j)` is scheduled at a time `t(c,j)` in the
closed integer window `[r(c,j),d(c,j)]`.

**Proof.** The earliest prefix at which upper quota permits `j` occurrences is
the least integer `k` with `ceil(k n_c/N)>=j`.  This is the least `k` satisfying
`k n_c/N>j-1`, namely `floor((j-1)N/n_c)+1`.  Hence upper quota for every
prefix is equivalent to `t(c,j)>=r(c,j)`.  The first prefix at which lower
quota requires `j` occurrences is the least `k` with
`floor(k n_c/N)>=j`, namely `ceil(jN/n_c)`.  Hence lower quota is equivalent
to `t(c,j)<=d(c,j)`.  Combining the two implications proves equivalence.  QED

**Complexity and implementation status.** Window endpoints use exact integer
division.  They are generated lazily by the V1 quota constructor.

### Theorem 3 (existence, EDF correctness, and head compression)

**Assumptions and comparison set.** Those of Theorem 2, with no pins, blocks,
or precedence constraints.  Ties use a fixed total order on category IDs.

**Claim.** A quota word exists.  Release-aware earliest-deadline-first (EDF)
scheduling produces one.  With one outstanding head per positive category and
two heaps, construction takes `O(N log C)` time and `O(C)` working memory,
excluding the necessary `O(N)` output.

**Proof of existence.** The house-monotone quota result of Balinski and Young
gives, for the entitlement vector `(n_c/N)_c`, a sequence of apportionments for
house sizes `k=0,...,N` in which each coordinate is its lower or upper quota
and exactly one coordinate increases at each step.  At house size `N`, all
entitlements are the integers `n_c`, so the increments form a word with the
required inventory and (2.2).  Theorem 2 converts it to a feasible window
schedule.

**EDF exchange proof.** Fix any feasible schedule.  At time `t`, let `e` be a
released unscheduled job of smallest deadline, and suppose the feasible
schedule instead places `h` at `t` and `e` at `s>=t`.  Exchange them.  Job `e`
is released at `t`, so moving it earlier is legal.  Job `h` was released at
`t`, so it is released at `s`.  Moreover `d(e)<=d(h)` by EDF choice and
`s<=d(e)` because the original schedule was feasible; hence `s<=d(h)`.  The
exchange preserves feasibility.  Repeating fixes EDF's choice at every slot.
Because a feasible schedule exists, EDF never encounters an empty released set
or an expired minimum deadline.

For a fixed category, both `r(c,j)` and `d(c,j)` are strictly increasing in
`j`, since `N/n_c>=1`.  If two occurrences of that category are simultaneously
released, EDF always prefers the earlier one.  It is therefore sufficient to
store only the first unscheduled occurrence of each category.  A future heap
is keyed by release; released heads move to a ready heap keyed by deadline and
the stable category tie key.  Each of `N` jobs causes `O(1)` heap operations on
heaps of size at most `C`.  This proves the time and memory bounds.  QED

**Implementation status.** The theorem is the contract of `quota_order`.
Exact comparison keys and stable UTF-8 byte ties are required.  The result may
receive the theorem label only after independent quota-window verification.

### Proposition 4 (exact maximum-discrepancy scan in linear time)

**Assumptions and comparison set.** Any completed categorical word with exact
nonnegative inventory and positive total.  This is an evaluation result, so it
does not change the comparison set.  The norm is the categorical
`L-infinity` norm in (1.3).

**Claim.** The exact `B` of a categorical word can be computed in `O(N+C)`
integer operations and `O(C)` memory, rather than `O(NC)`.

**Proof.** Fix `c`.  Between its `j`-th and `(j+1)`-st occurrences, `x_c(k)=j`
is constant, so `|x_c(k)-k n_c/N|` is the absolute value of an affine function
of `k`; its maximum on that integer interval occurs at an endpoint.  At an
occurrence of `c` at time `t`, check the two exact numerators

```text
|N(j-1)-(t-1)n_c|   and   |Nj-t n_c|.                 (2.3)
```

These are the endpoint immediately before and after the jump.  The first and
last constant-count intervals are also covered; the terminal error is zero.
Every occurrence contributes two checks, so their maximum divided by `N` is
exactly `B`.  QED

**Implementation status.** The specialized result stores the category counts
and next occurrence indices only; `Q` is not part of the million-scale theorem
contract.

## 3. The categorical certificate

For every positive category define

```text
q_c = N/gcd(n_c,N),
L_quota = max_c floor(q_c/2)/q_c.                     (3.1)
```

Let `OPT_B` be the minimum categorical `B` over all unconstrained words with
the inventory.

### Theorem 5 (integrality lower bound and strict factor below three)

**Assumptions and comparison set.** Equal masses, one-hot categories, positive
total, and the unconstrained comparison set.  The norm is `L-infinity` over all
category coordinates and prefixes.

**Claim.** `L_quota<=OPT_B`.  Every quota word has `B<1`.  If at least two
categories are positive, then

```text
B/OPT_B < 3.                                          (3.2)
```

If exactly one category is positive, `B=OPT_B=0` and the order is exact; no
ratio is formed.

**Proof.** For every order, `x_c(k)` is an integer, so its error from
`k n_c/N` is at least the distance of that rational to the nearest integer.
Writing `n_c/N` in lowest terms with denominator `q_c`, the residues as `k`
varies are all multiples of `1/q_c`; their maximum distance to an integer is
`floor(q_c/2)/q_c`.  Taking the maximum over `c` proves (3.1) is a lower bound.

Under (2.2), a nonintegral quota lies strictly between its floor and ceiling,
so either allowed integer is at distance strictly below one; an integral quota
has zero error.  Hence `B<1`.  With at least two positive categories, every
positive `n_c` lies strictly between `0` and `N`, so `q_c>=2`.  For every
integer `q>=2`, `floor(q/2)/q>=1/3`; consequently `OPT_B>=L_quota>=1/3`.
Combining this with `B<1` yields (3.2).  With one positive category all prefixes
are forced and exact.  QED

**Complexity and implementation status.** GCD evaluation costs `O(C log N)`
bit operations up to standard integer-arithmetic factors.  V1 reports the
actual exact upper bound `U=B`, lower bound `L_quota`, `U-L_quota`, and
`U/L_quota` when positive, plus the strict-factor label `3`.  The label is not
valid for unequal mass, non-one-hot features, or a constrained comparison set.
Zero-count categories stay in result metadata with identically zero error.  An
all-zero software inventory is the empty exact solution by convention; it lies
outside the `N>0` theorem.

## 4. The exact binary word and the Farey boundary

Let two category counts be `a,b>=0`, `N=a+b>0`, and let `x(k)` count the first
category.

### Theorem 6 (nearest mechanical word is prefixwise optimal)

**Assumptions and comparison set.** Two categories, equal masses, and all
binary words containing `a` first-category items and `b` second-category items.
The norm is categorical `L-infinity`, which here equals
`|x(k)-ka/N|` because the two coordinate errors are opposites.

**Claim.** Define

```text
x*(k)=floor(ka/N+1/2),       y_k=x*(k)-x*(k-1).        (4.1)
```

Then `y_k` is a feasible binary word.  At every prefix it minimizes absolute
error among all integer prefix counts.  Therefore it simultaneously minimizes
`B`, minimizes `Q`, and minimizes `Q` subject to optimal `B`.  Its optimum peak
is `floor(q/2)/q`, where `q=N/gcd(a,N)`.

**Proof.** Since `0<=a/N<=1`, successive differences in (4.1) are zero or one;
also `x*(0)=0` and `x*(N)=a`.  Thus the differences form a feasible word.  For
each fixed `k`, `floor(ka/N+1/2)` is a nearest integer to `ka/N` under the
declared upward tie convention.  No other word can use a noninteger prefix
count, so no other word has smaller error at that prefix.  Simultaneous
pointwise minimality implies minimal maximum and minimal sum.  The residue
calculation in Theorem 5 gives the displayed optimum.  QED

**Complexity and implementation status.** Generating the word and its exact
certificate takes `O(N)` time and output and `O(1)` auxiliary state.  It is the
contract of `quota_mechanical_order`; it is separate from EDF.

The lower word `floor(ka/N)` is quota-valid but not generally minimax.  For
`(a,b)=(1,4)`, its peak is `4/5`, while (4.1) has the optimal peak `2/5`.

Write `g=gcd(a,N)`, `p=a/g`, and `q=N/g`.  The increments in (4.1) are a
rational mechanical word of slope `p/q` and period `q`, repeated `g` times.
Under the standard binary-word convention, the primitive period is a cyclic
conjugate (with the stated boundary convention at ties) of the primitive
Christoffel word of that slope.  The canonical lower Christoffel word is a
particular Lyndon/conjugacy representative, not necessarily (4.1).  Reduced
fractions label the Stern-Brocot/Farey tree and the corresponding primitive
Christoffel construction, which explains the arithmetic connection.  It does
not imply that EDF selects (4.1), does not produce a canonical word for three
or more categories, and is not the source of Theorem 5's factor.

## 5. The exact small-instance oracle

V1 fixed blocks are contracted to macro-units while retaining every internal
trace.  After the exact pinned prefix, macro-unit `b` has total centered vector
`z_b` and internal trace vectors `t_{b,r}` including its successive original
item prefixes.  Let `S` be a subset of the `m` unpinned middle macro-units and

```text
p(S)=p_prefix + sum_{b in S} z_b.
```

Only a unit whose predecessor mask is contained in `S` may follow.  Forced
prefix and suffix trace costs are constants independent of the middle order.

### Theorem 7 (two-pass trace-aware subset DP)

**Assumptions and comparison set.** Exact rational vectors; valid V1 blocks,
whole-unit ordered end pins, and a precedence DAG; at most the declared oracle
limit of middle macro-units and original items.  The comparison set is exactly
the feasible V1 orders.  `B` is primary and `Q` secondary.

**Claim.** The following two passes return the lexicographic optimum `(B*,Q*)`.

Pass one stores only the smallest attainable peak `M[S]`.  For eligible `b`,
let

```text
h(S,b)=max_r ||p(S)+t_{b,r}||_infinity/W.
M[S union {b}] = min_b max(M[S],h(S,b)).              (5.1)
```

After incorporating the fixed suffix maximum, the full-state value is `B*`.
Pass two admits only transitions with all internal prefix norms at most `B*`
and stores the smallest accumulated sum

```text
C[S union {b}] = min_b (C[S]
                    + sum_r ||p(S)+t_{b,r}||_infinity/W).  (5.2)
```

Adding the forced suffix sum yields `Q*`.

**Proof.** The base prefix vector `p(S)` depends only on the subset, not its
order.  Every feasible middle order has a unique final transition into each of
its states.  In pass one, extending a smaller prior peak can never produce a
larger `max` than extending a larger prior peak, so Bellman's principle applies
to (5.1).  Induction on `|S|` proves `M[S]` is the true smallest peak to that
state.  The full state plus fixed suffix therefore gives the global `B*`.

After `B*` is fixed, feasibility under the peak cap is a local property of
each trace transition.  Accumulated cost is additive, so induction applies to
(5.2), proving it gives the smallest `Q` among all orders with peak at most
`B*`.  Since no order has smaller peak, this is the required lexicographic
optimum.  QED

**Why one lexicographic label is wrong.** Take unconstrained scalar
contributions, unit masses, and stable IDs `a,...,g`:

```text
(14,14,-20,5,11,2,-26).                               (5.3)
```

Their total is zero, so the normalized centered prefixes equal the displayed
values.  At subset `{a,c,d,f}`, order `acdf` has label `(14,22)`, while `fdca`
has lexicographically smaller partial label `(13,23)`.  A one-label DP discards
`acdf`.  Yet continuation `egb` gives order `acdfegb` with prefix sums
`14,-6,-1,1,12,-14,0`, hence `(B,Q)=(14,48)`.  Exhausting all `7!=5040`
orders confirms this is optimal, while the one-label DP returns `(14,49)`.
The future peak equalizes the earlier peaks, making the discarded lower sum
decisive.

**Complexity and implementation status.** With `m` macro-units, `n` original
items, and dimension `d`, direct trace evaluation is
`O(2^m (m+nd))` exact operations per pass and `Theta(d 2^m)` state-vector
storage plus `O(2^m)` scalar labels and predecessors, input, and output.  Unit,
item, and state-coordinate limits are explicit.  V1 `solve_exact` must return
`ORACLE_LIMIT_EXCEEDED` beyond them and must agree with an independently coded
small exhaustive oracle before receiving an exact label.

## 6. Constraints and a-posteriori certificates

After rejecting duplicate/unknown IDs, overlapping or repeated block items,
split blocks, reversed internal edges, and prefix/suffix phase conflicts, V1
contracts each fixed block.  Kahn's algorithm is then a complete feasibility
test for the remaining restricted macro-DAG: an acyclic contracted graph has a
topological middle order, and expansion preserves each fixed internal order;
a residual graph supplies a contracted-cycle witness.  This statement does not
cover arbitrary interior pins or flexible block interiors.

Let `OPT_K` be the best `B` over the feasible constrained comparison set.  For
any returned feasible order let `U=B(pi)` be recomputed exactly by the runtime
checker.  Separately implemented exhaustive test oracles judge small cases;
the runtime checker itself shares the production parser and centered-vector
builder.

### Theorem 8 (valid lower bounds for the same constrained optimum)

**Assumptions.** The constrained comparison set is nonempty and all quantities
below are computed from original item-level traces in the same normalization.

**Claim.** Each of the following is at most `OPT_K`:

1. `L_jump=max_i ||u_i||_infinity/(2W)`;
2. `L_quota` of (3.1) for categorical inventories;
3. the largest norm on a forced ordered prefix, and the backward-determined
   norms on a forced ordered suffix;
4. the minimum possible entry-state norm forced by the named occurrence ranks
   at the start of a categorical fixed block;
5. one half of the maximum `L-infinity` diameter between two internal trace
   points of any fixed block;
6. for a categorical precedence `(a,r)<(b,s)`, the positive part of
   `(r n_b-(s-1)n_a)/(n_a+n_b)`;
7. the exact oracle value, when the oracle covers the same comparison set.

Therefore their maximum `L` yields

```text
L <= OPT_K <= U.                                      (6.1)
```

Report `U-L`, and report `U/L` only when `L>0`.

**Proof.** An item jump joins two consecutive prefix vectors.  By the triangle
inequality, `||u_i||/W<=||P_{k-1}||/W+||P_k||/W<=2B`, proving item 1.  Item 2
uses only integer prefix counts and therefore remains a lower bound after the
comparison set is restricted.  Forced prefix states are shared by every
feasible order.  Forced suffix states are determined backward from total zero,
so item 3 is shared as well.  At a categorical block entry, each participating
category count is exactly one below its first named occurrence; minimizing its
state norm over every possible number of preceding nonparticipant items proves
item 4.  If a block begins at vector `z`, two internal states are `z+s` and
`z+t`; their distance is at most `||z+s||+||z+t||<=2B`, proving item 5.
Immediately after `(a,r)` but before `(b,s)`, `x_a>=r` and `x_b<=s-1`.
Eliminating the unknown prefix position from those two deviations gives item
6.  Item 7 is equality by Theorem 7.  The maximum of valid lower bounds is
valid, and the returned feasible order gives the upper bound.  QED

**Complexity and implementation status.** The jump and forced-trace bounds are
streamable.  A block diameter may be computed directly for small blocks or by
coordinate extrema in `L-infinity`.  The exact minimization in item 4 is a
valid mathematical bound; scalable V1 uses a linear-time relaxation of it:
per-coordinate distance from the feasible entry interval and the weighted
two-point radius of the participants with extreme ideal entry times.  This can
be weaker than item 4 but remains a valid lower bound.  V1 reports the
comparison set and whether the primary-`B` interval is closed, an unconstrained
factor applies, or the guarantee is only a posteriori.  Secondary-`Q`
exactness is a separate claim.

### Theorem 9 (compact constrained categorical scheduling)

Let occurrence `(c,j)` mean the `j`-th member of category `c`'s fixed input
queue.  Consider exact prefix and suffix sequences of occurrences, disjoint
fixed-order blocks whose occurrences for any one category are consecutive,
and a sparse set of occurrence-precedence edges.  The comparison set is all
interleavings of the fixed within-category queues satisfying those declared
constraints.  It is smaller than all permutations of separately labeled
items; every optimum or ratio below refers only to this precise set.

Contract each fixed block to a macro-vertex.  Implicit category-chain edges,
declared precedence edges, and exact pin phases induce a directed macro-graph.
At any stage a singleton category head is ready when its explicit predecessors
have been emitted; a block is ready exactly when its first occurrence is the
current head of every participating category and all explicit predecessors
have been emitted.  Exact prefix macros are replayed first, suffix macros are
withheld until the middle is exhausted, and ready middle macros are chosen by
block-adjusted earliest-deadline pressure.  Quota releases are priorities, not
feasibility gates.

**Claim.** The frontier is exactly the set of zero-indegree vertices in the
remaining contracted graph.  Hence emitting any ready macro preserves
feasibility, and an empty frontier before completion is a proof of
infeasibility.  With `K` declared occurrence references and `C` categories,
the scheduling core runs in

```text
O((N+K) log(C+K)) time,
O(C+K) auxiliary memory plus O(N) packed output.          (6.2)
```

The released certificate returns exact achieved `U` and `Q` and the Theorem 8
interval against the true constrained queue-interleaving optimum `OPT_B` for
the primary objective.  If `L=U`, only primary `B` optimality is proved.  The
reported `Q` is an exact measurement of the constructed order, not a proof that
`Q` is minimal among `B`-optimal orders.  Its direct exact metric scan is
`Theta(NC)`, so the complete constructor-plus-certificate cost is

```text
O(NC + (N+K) log(C+K)) time,                              (6.3)
O(C+K) auxiliary memory plus O(N) packed output.
```

This distinction is operationally important when the number of categories is
large.  The interface rejects requests whose declared `N*C` work exceeds its
published cap.  The constrained result receives no uniform factor-three label.

**Proof.** A later implicit occurrence has its previous category occurrence
as a predecessor.  A nonaligned block has an unscheduled natural predecessor
in at least one participating queue.  Positive contracted indegree records an
unscheduled explicit predecessor, and a withheld suffix has a phase
predecessor while middle macros remain.  Conversely, a unit with none of these
blockers is a zero-indegree macro and is structurally ready.  Thus the
algorithm is Kahn deletion with a deterministic priority among zero-indegree
vertices; the priority cannot create a cycle.  If output remains but no unit
is ready, every remaining vertex has a predecessor and the finite graph
contains a directed cycle.  Each ordinary occurrence causes one heap event and
packed append, each block causes one heap event plus work linear in its length,
and each declared edge is processed once, proving (6.2).  Block-alignment state
is updated once when each participating category reaches its block head, and
the block-entry lower bound uses interval distances plus one extreme-ideal-time
pair, so neither step hides a participant-pair scan.  The released verifier
scans all `C` coordinates at each prefix to recompute exact `U` and `Q`, giving
(6.3).  Theorem 8 supplies `L`.  QED

The packed category-code word reconstructs every occurrence identity by
streaming per-category counters.  Therefore million-item transport does not
materialize a million item IDs or `BalanceItem` objects, while verification can
still check every pin, block, edge, count, objective, and digest.

### Constraint counterexamples

Block contraction cannot ignore internal traces: the fixed block `[M,-M]` has
zero total but an internal excursion `M`.  More generally, no constant factor
independent of V1 constraints survives.  In one dimension take `m` items of
value `+1` and `m` of value `-1`.  Unconstrained alternation has `B=1`.  A
`2m-1`-edge chain that orders all positives and then all negatives is a sparse
DAG whose sole feasible order has `B=m`.  The same example can be imposed by a
fixed block or a pinned positive prefix.  Thus the categorical `<3` theorem
cannot be attached to the constrained scheduler.

## 7. Why the general-vector constructor is deferred

For the normalized zero-sum vectors `v_i=u_i/W`, let
`R=max_i ||v_i||`.  The classical Steinitz theorem of Grinberg and
Sevastyanov gives an unconstrained permutation with every prefix norm at most
`dR` for an arbitrary norm.  When `R>0`, together with `OPT>=R/2`, this is an
existential `2d` approximation statement.  If `R=0`, every order is exact.  It
is not the implemented scalable algorithm.

The constructive paths inspected for this release do not meet the frozen
million-item gate.  Bárány's 1981 account reports Kadec's constructor with
`O(N^d)` dependence and gives his own stronger-radius construction with
quadratic dependence on `N`; neither is a verified `O(Nd)` production route.
Recent constructive `L2` prefix-discrepancy work uses different norms and
heavier machinery and does not establish the V1 `L-infinity`, constrained,
million-item claim.  Accordingly, general vectors receive the exact small
oracle or a feasible constrained order with (6.1), never the categorical
factor.

## 8. Application and claim boundary

The theorem-backed operational object is a prefix-balanced order of a finite
categorical or joint-stratum inventory.  It can be relevant when work may stop,
be inspected, or checkpointed at a prefix.  If every item is always processed,
ordering alone cannot change the final all-item aggregate.

- A rendering preset demonstrates balance of declared sample cells.  It is not
  a replacement for progressive multi-jittered, Sobol, blue-noise, or renderer-
  integrated sampling and does not imply image-error improvement.
- A finance preset demonstrates balance of declared scenario cells.  It does
  not certify tail coverage, pricing error, regulatory stress adequacy, money
  saved, or production integration.
- An experiment preset may reorder already available, pre-randomized laboratory
  batches.  It is not a treatment-allocation method and makes no causal,
  clinical, ethical, or regulatory claim.
- Fair scheduling is a direct structural neighbour, but packet sizes, arrivals,
  service guarantees, and precedence constraints require their own models.

Finite cell balance is not full multidimensional star discrepancy.  No claim
about arbitrary anchored boxes, nonlinear boundaries, rare tails, within-cell
geometry, or unmeasured variables follows without an additional approximation
theorem.

## 9. Classification and open problems

**Classical inputs:** house-monotone quota existence, EDF exchange ideas,
mechanical/Christoffel words, and Steinitz existence.

**Project deductions:** the exact contribution/mass bridge to the gap delta;
the particular occurrence-window/heap synthesis; the exact endpoint scan;
the integrality certificate and strict `<3` combination; the trace-aware
two-pass oracle; and the combined constrained certificate.  This classification
does not assert external novelty.

**Implemented contract:** exact fraction arithmetic, quota EDF, the binary
mechanical constructor, small exact oracle, restricted V1 constraints, and
independent verification.  A release may call these implemented only when the
live verifier and interface gates pass.

**Open:** a practical dimension-only general-vector constructor at million
scale; nontrivial factors for useful precedence classes; stronger scalable
lower bounds; certified feature dictionaries approximating geometric
discrepancy; and measured downstream gains in real rendering, scenario, or
experimental systems.

## References used for theorem scope

Exact source-by-source scope, including negative findings, is recorded in
`research/MULTIDIMENSIONAL_PRIOR_ART.md`.  The principal classical sources are
Balinski--Young on quotatone apportionment, Horn on scheduling, Berstel--de
Luca on Christoffel words, Grinberg--Sevastyanov and Bárány on Steinitz
rearrangements, and the domain papers cited there.  The proofs above are
self-contained except for quota-path existence and the stated classical
Steinitz existence theorem.
