# Fable 5 adversarial-review packet

Date: 2026-07-16  
Repository: `/Users/za/Documents/farey-hecke`  
Project: `projects/prime-step-breakthrough`  
Release commit: `94e101f` (`feat: add constrained multidimensional prefix optimizer`)  
Review mode requested: independent, refute-if-possible, repair-authorized

## 1. Review mission

This packet is a map and an execution authorization, not a conclusion. Fable 5 should independently inspect the source, proofs, tests, frozen artifacts, and interfaces; re-run the key checks; try to construct counterexamples; and, when it finds a real defect or materially stronger design, may fix, amend, extend, refactor, or improve the tool and its supporting documentation.

The authorization covers the implementation subtree, tests, verifiers, benchmarks, interfaces, mathematical exposition, and application contracts. It does not authorize sending correspondence, publishing externally, changing unrelated projects, weakening a proof or test to make it pass, or silently changing the declared comparison set. Preserve the original behavior when a finding is only stylistic; make a change when it improves correctness, security, performance, clarity, or evidence quality.

For every accepted repair, Fable 5 must:

1. state the defect or improvement and its root cause;
2. patch the smallest coherent set of files;
3. add or update a regression/negative test that would have caught it;
4. run the relevant unit, oracle, interface, benchmark, and live UI checks;
5. obtain an independent review of the repaired claim; and
6. record the remaining limitations and exact verification output.

This is an end-to-end patch, regression test, independent review, and live verification loop; do not stop at a written critique when an in-scope repair is safe to make.

1. claims that hold, with evidence;
2. claims that are overstated, ambiguous, or false;
3. the smallest repair needed for each failure;
4. whether the mathematical result, software, and application claims are credible at their respective scopes.

Do not accept a green test suite as proof of a theorem. Do not accept a proof sketch as evidence that the implementation follows it. Review these as three separate layers:

- mathematical validity;
- implementation and certificate integrity;
- downstream application relevance.

## 2. Executive summary

The project began with exact rational prime-fraction/Farey observations and a per-step discrepancy: actual cumulative progress minus ideal cumulative progress. It now contains two related product layers.

### 2.1 Original one-dimensional research package

The package retains the original GapPermutation/Farey work:

- exact supplied-order gap discrepancy;
- exact permutation-average quadratic and continuous-\(L^2\) quantities;
- rigorous two-sided mean-\(L^1\) bounds;
- distinct-order counts;
- Farey gaps, prime-step shear, triangular shift law, coprime-layer kernel, and prime-energy calculations.

This layer evaluates or certifies gap structures. It is not the same as the new constrained scheduler.

### 2.2 New multidimensional operational layer

The new layer orders finite inventories so every prefix remains close to the final declared feature mix. It supports:

- unconstrained categorical quota words;
- exact binary mechanical words;
- exact small rational-vector optimization;
- explicit small constrained rational-vector optimization; and
- million-scale compact categorical scheduling with fixed blocks, exact prefix and suffix pins, and sparse precedence edges.

It returns an ordering plus an auditable certificate. For the primary metric `B`, the certificate has the form:

```text
L <= OPT_B <= U
```

`U` is the exact achieved maximum prefix discrepancy. `L` is a valid lower bound for the same declared comparison set. `U-L` and `U/L` are reported when defined. `primary_optimum_proved` is true only when `L=U`, and proves only primary `B`; the exact achieved accumulated metric `Q` is not claimed optimal among all `B`-optimal orders.

## 3. Mathematical lineage

### 3.1 One-dimensional bridge

For items with exact rational gap contributions `g_i`, total mass `W`, and ideal total `A`, the centered contribution is

```text
u_i = W*g_i - A
```

For unit masses and gaps summing to one, the normalized prefix is exactly

```text
sum_{j<=k} g_{pi(j)} - k/N
```

This is García's local prefix delta. The multidimensional code generalizes the same identity to contribution vectors `a_i`:

```text
W = sum_i w_i
A = sum_i a_i
u_i = W*a_i - w_i*A
P_k = sum_{j<=k} u_{pi(j)}
B(pi) = max_k ||P_k||_infinity / W
Q(pi) = sum_k ||P_k||_infinity / W
```

The exact bridge is Theorem 1 in `paper/MULTIDIMENSIONAL_PREFIX_BALANCE.md` and implemented in `src/coprimebatch/prefix_balance.py`.

### 3.2 Categorical specialization

For category `c`, use the one-hot vector `e_c`. If its final count is `n_c` and the prefix count is `x_c(k)`, then the coordinate discrepancy is

```text
x_c(k) - k*n_c/N
```

This is the operational interpretation: at every interruption point, how far is each declared category ahead of or behind its final proportional share?

### 3.3 Farey/mechanical structure

The binary path uses the nearest-integer mechanical word. Rational slopes, Christoffel/mechanical words, and the Stern--Brocot/Farey structure explain why some binary quota schedules are prefixwise optimal. The lower mechanical word `floor(k*a/N)` is deliberately not mislabeled as minimax; `(1,4)` is a counterexample.

Farey work also supplies exact rational test structures and the surrounding research context:

- moving Farey graph/shear results;
- triangular law for `x-{p*x}`;
- exact coprime-denominator-layer Gram kernel;
- prime-energy identities.

These results are not all runtime dependencies of the scheduler. The reviewer must distinguish mathematical ancestry, implemented theorem, and deferred research.

### 3.4 The García deduction

The paper records a finite-population fourth-moment bound and interpolation that prove the qualitative form of García's Conjecture 1:

```text
(9/160)*sigma_g*N^(3/2) <= mean_r_g
mean_r_g <= (1/sqrt(6))*sigma_g*N^(3/2)
```

The constants are rigorous but do not claim García's provisional constants. The underlying finite-population moments, discrepancy identities, mechanical words, EDF/exchange ideas, and quota existence results include classical ingredients. The project claims a García-specific deduction and synthesis, not priority for every ingredient.

## 4. Algorithmic paths

All public paths live in `src/coprimebatch/prefix_balance.py`.

| Path | Function | Intended scope | Exactness/guarantee |
|---|---|---|---|
| Unconstrained categorical | `quota_order` | Millions of one-hot category items | Release-aware EDF; quota-valid; strict `<3` factor relative to unconstrained categorical optimum when at least two categories are positive. |
| Binary mechanical | `quota_mechanical_order` | Two categories | Prefixwise exact for primary and accumulated objectives. Separate from EDF. |
| Exact general-vector | `solve_exact` | Small rational-vector instances | Two-pass subset DP; refuses explicit limits with `ORACLE_LIMIT_EXCEEDED`. |
| Explicit constrained | `solve_constrained` | Small/general rational vectors and supported constraints | Feasible ordering plus a-posteriori lower/upper certificate; no constrained universal factor. |
| Compact constrained categorical | `solve_constrained_quota` | Million-scale category inventories | Packed deterministic frontier/Kahn scheduler; fixed blocks, whole end pins, sparse occurrence precedence; input-specific `L<=OPT_B<=U`. |

### 4.1 Quota constructor

For category count `n_c` in total inventory `N`, occurrence `j` has an exact integer release/deadline window:

```text
release(c,j) = floor((j-1)*N/n_c) + 1
deadline(c,j) = ceil(j*N/n_c)
```

The scheduler keeps only each category's next outstanding occurrence. Two heaps implement release-aware earliest-deadline-first scheduling. This gives `O(N log C)` scheduling and `O(C)` auxiliary memory, excluding output.

### 4.2 Compact constrained path

The compact problem identifies occurrences as `(category, 1-based occurrence)` instead of allocating a Python object for every item. It contracts valid fixed blocks into macro-units, tracks block readiness and sparse precedence, respects whole-unit prefix/suffix pins, and uses quota pressure only as a priority—not as a feasibility proof.

The scheduling core is:

```text
O((N+K) log(C+K)) time
O(C+K) auxiliary memory + packed O(N) output
```

The released certificate directly recomputes exact `B` and `Q` in `Theta(NC)` for its complete bound:

```text
O(NC + (N+K) log(C+K))
```

Interface admission caps are deliberate:

- at most 256 categories;
- at most 8,000,000 declared `N*C` metric cells;
- at most 10,000 occurrence references;
- at most 1,024 occurrences in one fixed block.

These are released-interface resource limits, not mathematical limits.

## 5. Constraint and comparison-set contract

The constrained comparison set is exactly:

> all interleavings of fixed within-category occurrence queues that satisfy the declared fixed blocks, exact whole-unit prefix/suffix pins, and precedence edges.

Supported V1 constraints:

- disjoint fixed contiguous blocks with fixed internal order;
- exact ordered prefix pins;
- exact ordered suffix pins; and
- sparse precedence DAG edges.

Unsupported or deferred:

- arbitrary interior pins that split a block;
- flexible block interiors;
- arbitrary continuous-vector million-scale construction;
- full continuous star discrepancy;
- constraint-independent approximation constants;
- production multi-user service hardening.

The reviewer must check that no report silently changes “fixed-queue interleavings” into all permutations of separately labeled items.

## 6. Lower-bound certificate

The constrained lower bound is the maximum of valid terms, including:

- item-jump lower bound;
- categorical integrality lower bound when applicable;
- exact forced-prefix/suffix discrepancy;
- fixed-block internal trace diameter;
- categorical block-entry relaxation;
- precedence-separation terms; and
- exact optimum when the small oracle ran.

The verifier recomputes the lower bound and achieved metrics. A closed interval proves primary `B` only. A large ratio is a weak certificate, not a success label.

## 7. Code map

### Core and research modules

- `src/coprimebatch/prefix_balance.py` — all new prefix-balance data models, constructors, validators, metrics, constraints, and certificates.
- `src/coprimebatch/gap_permutation.py` — original one-dimensional GapPermutation Certificate.
- `src/coprimebatch/shear.py` — Farey shear, shift moments, triangular law, and Weyl-related calculations.
- `src/coprimebatch/kernel.py` — coprime-layer/prime-energy kernel and portfolio certificates.
- `src/coprimebatch/arithmetic.py` — exact arithmetic primitives.
- `src/coprimebatch/optimizer.py` — earlier optimizer/baseline utilities.
- `src/coprimebatch/applications.py` — synthetic rendering, finance, and lab categorical presets. These are demonstrations, not integrations.

### Interfaces

- `src/coprimebatch/cli.py` — CLI modes: `quota`, `binary`, `exact`, `constrained`, and `constrained-quota`.
- `src/coprimebatch/web.py` — dependency-free loopback JSON HTTP service.
- `web/index.html`, `web/app.js`, `web/styles.css` — browser interface.
- `src/coprimebatch/__init__.py` — public exports.

### Verification code

- `verify_all.py` — original suite and live HTTP regression.
- `verify_operational.py` — static checks, independent oracles, interface parity, mutation checks, scaling subprocesses, artifact checks, and cache hygiene.
- `tests/prefix_balance_oracles.py` — independent quota/exhaustive oracles.
- `tests/constrained_quota_oracles.py` — constrained comparison/oracle helpers.
- `tests/test_prefix_balance.py` — exact-vector path tests.
- `tests/test_constrained_quota.py` — compact constrained tests.
- `tests/test_prefix_balance_interfaces.py` — CLI/API/browser-contract tests.
- `benchmark_operational.py` — frozen million-item unconstrained benchmark.
- `benchmark_constrained_operational.py` — frozen million-item constrained benchmark.

## 8. Interfaces and transport

The Python API is authoritative. CLI, HTTP, and browser use the shared result schema.

Large orders are transported as:

- item count;
- bounded preview;
- exact rational strings;
- canonical SHA-256 digest;
- certificate and explanation;
- not one million JSON objects.

The HTTP server accepts only loopback binds (`127.0.0.1`, `localhost`, `::1`), caps request bodies, and applies pre-solve work caps. It has no authentication, TLS, rate limiting, process isolation, or production work queue.

## 9. Frozen operational evidence

Fixture: one million items, four unequal positive categories, all supported constraint classes active, including a repeated consecutive category block.

Frozen values:

```text
constraint digest:
85b5161d9c938f437a3d24315d271abf5cdf8bc14eba1e972a410e006dd1ae1a

order digest:
3194a7661d0d90f6115bba41cfed1c506fd8f9442c0f54c0a8069ff90662c675

U = 360167777/200000
L = 1799839/1000
Q = 455298078991/62500
additive gap = 199977/200000
ratio = 360167777/359967800
```

The complete released certificate has direct `Theta(NC)` metric work. The stable full run was about 4.14 seconds at about 46.5 MB RSS under a hard 30-second worker timeout and 128-MiB ceiling. The final cold review independently ran about 4.08 seconds at about 47.0 MB RSS and reproduced the digest/metrics.

## 10. Fresh verification evidence

The latest fresh run before this packet was created:

```text
PYTHONDONTWRITEBYTECODE=1 python3 verify_operational.py

static gate: PASS
browser JavaScript syntax gate: PASS
operational unit/oracle gate: PASS
million-item subprocess gate: PASS
  positions=1000000 wall=1.520917s rss=40599552
million-item sparse-constraint gate: PASS
  positions=1000000 wall=4.182120s rss=46907392
original verify_all regression gate: PASS
source-mutation gate: PASS
cache-mutation gate: PASS
OPERATIONAL VERIFICATION PASS
```

The original verification record reports 60 unit tests, 7 live HTTP tests, and 13/13 benchmark gates. The operational verifier chains that regression.

Recorded live-browser evidence exercised keyboard input, native selections, clicks, all four compact constraint classes, malformed JSON, recovery, result scope labels, exact bounds, previews, and digest display. It is software/UI evidence, not domain integration evidence. See `artifacts/BROWSER_VERIFICATION_OPERATIONAL.md`.

## 11. Independent review history

### First cold rejection

The first cold review rejected release because it found:

- complexity wording that hid block-entry work;
- trust in forged metadata;
- an unfrozen benchmark artifact;
- ambiguity around exact `Q` versus primary `B`;
- missing resource caps.

### Repairs

The implementation then:

- stated complete certificate complexity as `O(NC + (N+K) log(C+K))`;
- recomputed feasibility, metrics, explanations, and packed storage;
- froze constraints, digests, `U`, `L`, `Q`, gap, and ratio;
- labeled closure as `primary_B_only`;
- added admission caps, hard timeout, and RSS ceiling;
- added a repeated-category block and gap/reversal negative tests.

### Final reviews

- Sol Ultra (`gpt-5.6-sol`, xhigh) accepted after required repairs.
- Final cold rereview: `ACCEPT — no remaining blockers`.
- Focused cold suite: 31 tests in about 5.96 seconds.

These are review artifacts, not substitutes for Fable 5's independent pass. They are starting evidence, not a freeze: a reviewer is expected to repair anything that does not survive adversarial scrutiny.

## 12. Security and blast-radius notes

The project is an isolated new subtree. Existing unrelated work at the repo root was preserved.

Manual security review found no credentials, auth logic, dynamic evaluation, unsafe deserialization, user-controlled process execution, or new runtime dependency. The automated lexical scanner produced REVIEW/HIGH-style noise on mathematical words such as `verify` and `token`; the actual scoped surface is the package, CLI, loopback server, browser, benchmarks, and tests.

The HTTP service is research software. Do not expose it to an untrusted network without a real deployment boundary.

## 13. Fable 5 attack plan

### Mathematical attacks

1. Re-derive Theorem 1 from the mass-weighted vector contract and check every normalization.
2. Prove or refute the quota-window equivalence with hand-built edge cases: zero counts, one positive category, equal counts, highly unequal counts, and divisibility boundaries.
3. Search for a counterexample to the unconstrained strict `<3` claim and verify that the implementation emits it only in its declared scope.
4. Check the binary mechanical-word theorem against all small rational slopes; specifically test `(1,4)` against the lower mechanical word.
5. Recompute every constrained lower-bound term independently and test whether the maximum remains valid when blocks overlap, repeat a category, or interact with pins and precedence.
6. Attack the claim that `L=U` proves only primary `B`, not secondary `Q`.
7. Check whether any “Farey” or “García” wording accidentally claims more novelty or generality than the paper establishes.

### Implementation attacks

1. Forge every result field independently and with self-consistent digests.
2. Replace packed `array('I')` order storage with tuples, lists, wrong widths, truncated output, duplicated occurrences, and reordered category labels.
3. Generate constrained cycles, reversed internal edges, split pins, block gaps, duplicate occurrence references, and sparse-frontier deadlocks.
4. Compare the production solver against the independent exhaustive oracle on every feasible small constrained instance, not only registered examples.
5. Recompute `U`, `Q`, inventory, occurrence windows, constraints, digest, and lower bounds from raw input without trusting returned explanation fields.
6. Measure actual peak memory and wall time at the admission-cap boundaries.
7. Inspect direct Python calls separately from capped CLI/HTTP calls.
8. Test deterministic output across category insertion orders, UTF-8 names, zero-count categories, and repeated blocks.

### Interface and security attacks

1. Try non-loopback binds, path traversal, oversized bodies, unsupported methods, malformed JSON, huge integer strings, and full-order response abuse.
2. Check CLI/HTTP/browser schema parity and exact-fraction rendering for large numerators.
3. Confirm that application presets cannot be replaced with arbitrary server paths or treated as domain validation.
4. Determine whether the local HTTP threading model can exhaust resources even within the declared body/cell caps.

### Application attacks

1. For every preset, place the real loss/error signal adversarially inside one category and demonstrate that category balance does not imply downstream accuracy.
2. Identify which proposed domains have a meaningful interruption-prefix loss and which do not.
3. Separate compute savings, labor savings, earlier-information value, and mistake prevention; reject any unsupported monetary claim.
4. Specify the smallest real integration experiment and its baseline: stable-order versus seeded-random versus optimizer, same jobs, same workers, preregistered prefix metric.

## 14. Required Fable 5 output

Return a table with:

```text
claim | holds/refuted/uncertain | evidence command or source | severity | repair
```

Then provide:

- the strongest surviving mathematical result;
- the strongest surviving operational result;
- the most dangerous untested assumption;
- any claim that must be removed before publication or deployment;
- the minimum next experiment;
- a release recommendation: publishable mathematics, research software, pilot-ready, or not ready.

If repairs are required, continue through the repair-and-verify loop instead of stopping at a critique. Include a second table:

```text
finding | files changed | regression test | independent review | live verification | residual risk
```

The end state is not “review complete” until every accepted repair has a fresh passing signal at the layer of its claim. If a repair cannot be safely completed without user-owned credentials, publication authority, destructive ambiguity, or a new domain decision, mark it blocked and explain exactly what is needed.

## 15. Source index

- Main overview: `README.md`
- Mathematical contract: `paper/MULTIDIMENSIONAL_PREFIX_BALANCE.md`
- Architecture: `OPERATIONAL_ARCHITECTURE.md`
- API contract: `IMPLEMENTATION_CONTRACT.md`
- Current state and evidence: `OPERATIONAL_STATE.md`
- Blindspots: `BLINDSPOT_AUDIT_V2.md`
- Prior art: `research/MULTIDIMENSIONAL_PRIOR_ART.md`
- Application boundaries: `artifacts/APPLICATION_VALIDATION.md`
- Final gates: `artifacts/FINAL_GATES.md`
- Review history: `artifacts/OPERATIONAL_REVIEWS.md`
- Browser record: `artifacts/BROWSER_VERIFICATION_OPERATIONAL.md`
- Main implementation: `src/coprimebatch/prefix_balance.py`
- Independent tests/oracles: `tests/`, `verify_all.py`, `verify_operational.py`

The packet's claims are intentionally narrower than the project's aspirations: the strongest implemented result is a proof-qualified categorical/fixed-queue optimizer with an input-specific constrained certificate, not a universal continuous-vector optimizer or a validated domain product.
