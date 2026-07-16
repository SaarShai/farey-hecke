# Operational Prefix-Balance Architecture

Status: frozen for implementation on 2026-07-15 after independent mathematics,
systems, application, quota-constructor, general-vector-constructor, and
refutation passes.

## 1. Exact mathematical contract

Item `i` has a distinct stable identifier, a positive integer progress mass
`w_i`, and an exact rational contribution vector `a_i` in dimension `d`.  Write

```text
W = sum_i w_i,  A = sum_i a_i,
u_i = W a_i - w_i A.
```

The centered rational vectors satisfy `sum_i u_i = 0`.  For order `pi`, define

```text
P_k(pi) = sum_{j <= k} u_{pi(j)},
B(pi)   = max_{0 <= k <= N} ||P_k(pi)||_infinity / W,
Q(pi)   = sum_{k=1}^{N} ||P_k(pi)||_infinity / W.
```

`B` is primary.  `Q` breaks ties in the exact oracle without worsening the
globally optimal `B`.  The exact/general V1 path accepts integers and rational
fractions.  The million-scale quota path uses integers only.  Binary
floating-point input cannot receive an exact theorem label.

For exact rational one-dimensional gaps summing to one, take `w_i=1`,
`a_i=g_i`.  Then
`P_k/W = sum_{j<=k} g_{pi(j)} - k/N`, exactly García's local prefix delta.

For categories, take `w_i=1`, `a_i=e_c`.  If category `c` has inventory `n_c`
and prefix count `x_c(k)`, then

```text
P_k[c] / N = x_c(k) - k n_c/N.
```

This is a genuinely multidimensional finite-feature problem, but it controls
only the declared categories or joint strata.

## 2. The theorem-backed million-scale constructor

For every positive category count `n_c`, the `j`-th occurrence has integer
window

```text
r(c,j) = floor((j-1)N/n_c) + 1,
d(c,j) = ceil(jN/n_c).
```

Scheduling every unit occurrence within its window is equivalent to

```text
floor(k n_c/N) <= x_c(k) <= ceil(k n_c/N)
```

for every category and prefix.  House-monotone quota theory proves that a
feasible path exists.  Release-aware earliest-deadline-first scheduling finds
one by the unit-job exchange argument.  Releases and deadlines are strictly
increasing within a category, so only its first outstanding occurrence is
stored.  Two heaps therefore give `O(N log C)` time and `O(C)` working memory,
excluding the packed `O(N)` output buffer returned by V1.  A true iterator API
is deferred.  All scheduling comparisons use exact integers and stable UTF-8
byte-key ties.

The resulting categorical discrepancy obeys `B < 1`.  For

```text
q_c = N / gcd(n_c, N),
L_quota = max_c floor(q_c/2) / q_c,
```

integrality gives `L_quota <= OPT_B`.  If at least two categories are positive,
`L_quota >= 1/3`, hence `B/OPT_B < 3`.  One positive category has `B=OPT=0` and
is reported as exact, never as `0/0`.

For two categories, the nearest-integer mechanical word
`x(k)=floor(k a/N + 1/2)` is available as a separate prefixwise exact
construction.  It is a rational mechanical/Christoffel conjugate and connects
to the Farey/Stern-Brocot tree.  The lower mechanical word `floor(k a/N)` is
quota-valid but need not be minimax (counts `(1,4)` are a counterexample).  EDF
may return another valid quota word; it is not silently labeled the exact binary
optimizer or the canonical lower Christoffel word.

## 3. Exact small-instance oracle

The exact oracle accepts general centered rational/integer vectors and all V1
constraints after fixed-block contraction.  A state is a subset of middle
macro-units; its prefix vector and expanded length are determined by that set.
Only units whose predecessor mask is contained in the state may transition.
Every internal item prefix of a block is evaluated.

A single lexicographic label per subset is unsound.  The oracle is two-pass:

1. compute the globally minimal peak `B*` by subset dynamic programming;
2. recompute the DP, admitting only transitions whose item-level prefixes stay
   at or below `B*`, and minimize accumulated `Q`.

This is compared with a separately implemented exhaustive oracle on registered
small cases.  The production verifier intentionally reuses production parsing
and arithmetic, so software independence comes from the test oracle rather than
that runtime checker.  Unit, item, and state-coordinate limits are explicit;
exceeding them returns `ORACLE_LIMIT_EXCEEDED`, never a heuristic answer carrying
an exact label.

## 4. Constraint engine

V1 supports:

- disjoint fixed contiguous blocks with fixed internal order;
- an exact ordered pinned prefix and exact ordered pinned suffix;
- a sparse precedence DAG with stable edge identifiers.

Pins must contain whole macro-units; arbitrary interior pins and flexible block
interiors are out of V1.  A precedence edge internal to a block must agree with
its listed order.  After contraction, phase/order checks plus Kahn's algorithm
are a complete feasibility test for this restricted contract.  Witnesses name
the original item, block, or edge IDs for duplicate IDs, unknown IDs, overlap,
split blocks, reversed internal edges, pin-order conflicts, and contracted
cycles.

Two constrained representations share the same objective and witnesses.  The
explicit representation handles arbitrary small rational vectors and stable
item IDs.  The compact categorical representation names `(category,
occurrence)` where occurrence is the 1-based rank in that category's fixed
input queue.  Its packed category-code word reconstructs those identities
without allocating one object per item.

The scalable compact scheduler is deterministic block-adjusted EDF-pressure
Kahn.  Category heads, sparse occurrence events, block state, and declared
edges are retained; quota releases rank ready work but never gate feasibility.
Valid consecutive-in-category blocks contract to macro-units, exact end pins
define phases, and an empty structural frontier is a contracted-cycle proof.
The scheduling core runs in `O((N+K) log(C+K))` time and `O(C+K)` auxiliary
memory plus packed output, where `K` is sparse constraint size.  The released
certificate directly recomputes both exact objectives in `Theta(NC)`, giving a
complete bound of `O(NC + (N+K) log(C+K))`; shared interface validation rejects
requests above `C=256`, `N*C=8,000,000`, 10,000 occurrence references
(precedence contributes two endpoint references), or fixed-block width 1,024.
These admission constants preserve the frozen `N=1,000,000`, `C=4` fixture.
Constraints can force error linear in `N`, so this path receives no quota or
Steinitz constant.

## 5. A-posteriori certificates

Every returned order is streamed through the runtime checker to obtain an exact
upper bound `U=B(pi)`.  A separately implemented exhaustive oracle supplies
software independence on registered small cases.  Valid lower bounds for the
same constrained comparison set include:

- `max_i ||u_i||_infinity/(2W)`, because an item jump joins two prefixes;
- categorical integrality `L_quota`;
- the exact maximum along a forced prefix or suffix;
- a linear-time categorical block-entry relaxation from the feasible entry
  interval and extreme ideal entry times;
- one half of a fixed block's internal-trace diameter;
- the two-category separation forced by each occurrence-precedence edge;
- an exact optimum when the small oracle ran.

Their maximum is `L`.  The certificate reports `L <= OPT_B <= U`, additive gap
`U-L`, and `U/L` only when `L>0`.  Closure `L=U` proves only the primary
maximum-discrepancy objective `B`; the compact constructor reports achieved
`Q` exactly but does not claim that `Q` is minimal among `B`-optimal orders.
A large ratio is evidence of a weak guarantee,
not relabeled success.  The categorical strict `<3` label is emitted only for
the unconstrained, equal-mass, one-hot path.

## 6. Interfaces and million-item transport

The Python API is authoritative.  CLI and HTTP use a shared canonical JSON
shape.  Small explicit constrained problems may be inline.  Million-item quota
and sparse-constrained categorical problems use compact category counts plus
occurrence-ranked constraints; their order is represented by a digest, count,
and bounded preview rather than a million JSON objects.  The constrained true
optimum is explicitly over fixed-queue interleavings, not all labeled-item
permutations.  HTTP never accepts arbitrary server paths.  Application presets
are allowlisted data constructors, not filenames supplied by clients.
The bundled threaded HTTP server is localhost research software, not a hardened
deployment boundary: it provides no authentication, TLS, rate limiting,
process isolation, or production work admission beyond the declared request
caps.  The runtime bind guard accepts only `127.0.0.1`, `localhost`, or `::1`;
requests require a nonblank loopback `Host`; browser POSTs require an absent or loopback
`Origin`; and API POSTs require `application/json`. Endpoint-specific count and
magnitude limits are combined with rational/common-denominator bit-complexity,
exact-output-size, factorization, prefactored-kernel, and matrix/evaluation work budgets before
exact compute starts. A 15-second socket timeout and 64-handler
semaphore bound slow connections. They do not provide a total computation
deadline or cancellation, so the service must not be routed to untrusted
networks as shipped. Direct Python and CLI research entrypoints are intentionally
outside these HTTP-only budgets unless separately documented.

The browser exposes generic counts plus rendering, finance-scenario, and
pre-randomized laboratory-batch demonstrations.  It displays theorem scope,
comparison set, exact bounds, preview/digest, constraint pressure, and the
domain limitation beside the result.

## 7. Claim tiers

1. **Proved and implemented:** exact centered contract; quota-window
   equivalence; EDF quota constructor; categorical `<3` factor; exact
   certificates and feasibility verification.
2. **Implemented with a-posteriori guarantee:** million-scale compact
   categorical fixed blocks, end pins, and sparse precedence edges; explicit
   arbitrary small rational vectors use the same constraint classes.
3. **Demonstration only:** rendering, finance, and experiment joint-cell
   presets.  No production, monetary, regulatory, clinical, or downstream-loss
   claim.
4. **Deferred research:** a million-scale constant-factor constructor for
   arbitrary vectors, full star discrepancy, arbitrary interior pins, flexible
   blocks, and constraint-independent approximation factors.
