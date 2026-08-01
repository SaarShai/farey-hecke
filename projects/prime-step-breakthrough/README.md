# Prime-Step Breakthrough

This project turns the original prime-denominator/Farey-step observation into
a proof-qualified research package and a working certificate.

The main new consequence is a two-sided theorem for the mean absolute local
discrepancy over all permutations of a fixed gap multiset.  It proves the
qualitative \(\sigma_gN^{3/2}\) law conjectured by Rogelio Tomás García in
2026, while explicitly crediting the classical finite-population moment and
one-dimensional discrepancy identities used in the proof.  A companion
\(O(N)\) certificate evaluates rigorous bounds and exact quadratic averages
without enumerating as many as \(N!\) orderings.

The same package also proves a quantitative equidistribution theorem for the
moving Farey graph \((x,\{px\})\), derives the triangular law for the original
per-step shift \(x-\{px\}\), and implements an exact Gram-kernel certificate
for complete coprime denominator layers.

## Operational prefix balance

The `prefix_balance` module orders finite inventories so every intermediate
prefix stays representative in declared features.  Item `i` has positive
integer progress mass `w_i` and exact rational contribution vector `a_i`.  With

```text
W = sum w_i,  A = sum a_i,  u_i = W a_i - w_i A,
```

the primary objective is the largest prefix `L-infinity` norm
`max_k ||sum_{j<=k} u_j||_infinity/W`.  The accumulated prefix norm is a
secondary objective for the exact small solver.

This contains both motivating cases exactly:

- For rational one-dimensional gaps, `w_i=1` and `a_i=g_i` give García's local
  prefix delta `sum_{j<=k} g_j-k/N`.
- For categories, `w_i=1` and `a_i=e_c` give the category error
  `x_c(k)-k n_c/N` in every coordinate.

The guarantee depends on the path:

- `quota_order(counts)` runs in `O(N log C)` time and `O(C)` working memory,
  stays inside every category's floor/ceiling prefix quota, and is strictly
  better than a factor three relative to the true **unconstrained categorical**
  optimum when at least two categories are positive.
- `quota_mechanical_order(a, b)` is exact for the binary primary and accumulated
  prefix objectives.
- `solve_exact(problem)` is an exact two-pass oracle for small rational-vector
  instances. It refuses configured size limits rather than relabeling a
  heuristic as exact.
- `solve_constrained(problem)` supports fixed-order contiguous blocks, exact
  ordered prefix/suffix pins, and a sparse precedence DAG. It reports an
  runtime-recomputed certificate `L <= OPT <= U`, additive gap `U-L`, and
  ratio `U/L` only when `L>0`. It receives no categorical factor guarantee.
- `solve_constrained_quota(problem)` supplies the compact million-scale version
  for categorical inventories.  Constraints identify the 1-based occurrence
  within a category rather than a materialized item object.  It supports fixed
  blocks, exact end pins, and sparse precedence.  Its scheduling core uses
  `O((N+K) log(C+K))` time and `O(C+K)` auxiliary memory plus packed output.
  The released certificate independently recomputes both exact objectives in
  `Theta(NC)`, so its complete time bound is
  `O(NC + (N+K) log(C+K))`; interfaces cap declared `N*C` work.
  Its exact `U` and valid `L` compare against all feasible interleavings of the
  fixed within-category queues—not all permutations of separately labeled
  items—and its ratio is a posteriori, with no factor-three label.  When
  `L=U`, `primary_optimum_proved` certifies the primary `B` objective only;
  achieved `Q` is exact but is not claimed minimal among `B`-optimal orders.

The general-vector constructor is not million-scale and carries no constant
factor. The scalable theorem applies only to categorical or joint-stratum
counts—not arbitrary vectors, continuous star discrepancy, or undeclared
features.

## What to read

- [`paper/PREPRINT.md`](paper/PREPRINT.md): theorem statements, proofs,
  application, and limitations.
- [`paper/GARCIA_UPDATE_DRAFT.md`](paper/GARCIA_UPDATE_DRAFT.md): concise
  correspondence follow-up tailored to the existing thread.
- [`RESEARCH_SPEC.md`](RESEARCH_SPEC.md): frozen conventions and acceptance
  gates.
- [`BLINDSPOT_AUDIT.md`](BLINDSPOT_AUDIT.md): unknown-unknowns, historical
  failures, and claim boundaries.
- [`research/NOVELTY_AUDIT.md`](research/NOVELTY_AUDIT.md): nearest prior art
  and the bounded novelty claim.
- [`artifacts/benchmark.json`](artifacts/benchmark.json): machine-readable
  verification evidence.
- [`paper/MULTIDIMENSIONAL_PREFIX_BALANCE.md`](paper/MULTIDIMENSIONAL_PREFIX_BALANCE.md):
  multidimensional theorem and proof contract.
- [`OPERATIONAL_ARCHITECTURE.md`](OPERATIONAL_ARCHITECTURE.md): exact objective,
  constraints, guarantee scopes, and transport design.
- [`artifacts/APPLICATION_VALIDATION.md`](artifacts/APPLICATION_VALIDATION.md):
  application workloads, negative controls, sources, and claim boundaries.
- [`artifacts/REAL_DATA_ML_SIMULATION.md`](artifacts/REAL_DATA_ML_SIMULATION.md):
  real UCI handwritten-digit evaluation, 2,000 paired ordering simulations,
  downstream prefix-error gains, sample-count thresholds, and a negative control.
- [`artifacts/WORKFLOW_MEASUREMENT_PROTOCOL.md`](artifacts/WORKFLOW_MEASUREMENT_PROTOCOL.md):
  hash-chained prospective human-workflow instrumentation, cost formula, and
  the gate for any labor-saving claim.
- [`artifacts/ECONOMIC_DECISION_2026-08-01.md`](artifacts/ECONOMIC_DECISION_2026-08-01.md):
  the current no-go/paid-pilot economic decision, including the negative
  production-order baseline result and scenario-value calculations.
- [`prospective_uci_blind.py`](prospective_uci_blind.py) and
  [`pilots/uci-optdigits-2026-08-01-label-blind-v2/`](pilots/uci-optdigits-2026-08-01-label-blind-v2/):
  a label-blind freeze/reveal study for the UCI audit workload.  It is
  prospective with respect to the committed analysis and orders, but remains
  offline public-dataset evidence rather than a production or human-time
  result.

## Python examples

Compact categorical inventories do not materialize a million Python objects:

```python
from coprimebatch.applications import application_preset
from coprimebatch.prefix_balance import quota_order, verify_quota_result

preset = application_preset("rendering-progressive-joint-cells")
result = quota_order(preset.counts_dict())
assert verify_quota_result(result).passed
print(len(result.order_codes), result.order_sha256)
print(result.lower_bound, result.max_discrepancy, result.ratio_bound)
```

General exact and constrained inputs use exact integers or `Fraction` values:

```python
from coprimebatch.prefix_balance import BalanceItem, BalanceProblem, solve_exact

problem = BalanceProblem(
    items=(
        BalanceItem("a", (1, 0), category="a"),
        BalanceItem("b", (0, 1), category="b"),
        BalanceItem("c", (1, 0), category="a"),
    ),
    precedence=(("a", "c"),),
)
certificate = solve_exact(problem)
print(certificate.order, certificate.max_discrepancy)
```

Sparse categorical constraints remain compact even at one million items:

```python
from coprimebatch.prefix_balance import (
    CategoricalConstraintProblem,
    FixedOccurrenceBlock,
    OccurrencePrecedence,
    OccurrenceRef,
    solve_constrained_quota,
    verify_constrained_quota,
)

r = OccurrenceRef
problem = CategoricalConstraintProblem(
    counts={"a": 2, "b": 2},
    fixed_blocks=(FixedOccurrenceBlock("joint", (r("b", 1), r("a", 2))),),
    pinned_prefix=(r("a", 1),),
    pinned_suffix=(r("b", 2),),
)
certificate = solve_constrained_quota(problem)
assert verify_constrained_quota(problem, certificate).passed
print(
    certificate.max_discrepancy,
    certificate.lower_bound,
    certificate.primary_optimum_proved,
)
```

The CLI, JSON HTTP endpoint, and browser use the same result schema. Large
orders cross those interfaces as an item count, bounded preview, canonical
SHA-256 digest, and exact rational strings instead of one million JSON entries.
The compact Python certificate deliberately exposes its order only as a
32-bit unsigned `array('I')`; the runtime verifier rejects tuple/list copies or
arrays with another item width so the documented packed-storage contract is
checked rather than inferred.
The shared constrained-quota entrypoint admits at most 256 categories,
8,000,000 declared exact-metric cells `N*C`, 10,000 occurrence references
(counting both endpoints of each precedence edge), and 1,024 occurrences in
one fixed block. These are request-admission limits for the released direct
`Theta(NC)` certificate, not mathematical limits of the model.
Run `python3 -m coprimebatch.cli --help` for the installed CLI contract.

## Run the certificate

From this directory:

```bash
PYTHONPATH=src python3 -m coprimebatch.cli gaps 1/4 1/2 1/4 --json
PYTHONPATH=src python3 -m coprimebatch.cli gaps --farey-order 8 --json
PYTHONPATH=src python3 -m coprimebatch.web --host 127.0.0.1 --port 8765
```

Then open `http://127.0.0.1:8765/` for the keyboard-accessible browser UI.
This dependency-free HTTP server is localhost research software. It has no
authentication, TLS, rate limiting, process isolation, or production work
queue. Its bind guard accepts only `127.0.0.1`, `localhost`, or `::1`; every
request must carry a nonblank loopback `Host`, browser POSTs must have an absent or
loopback `Origin`, and API POSTs require `application/json`. Exact-arithmetic
compute endpoints have count, per-value bit-length, common-denominator and
aggregate exact-output, factorization, and combined arithmetic-work admission budgets. These reject
compact bodies of distinct huge rationals and valid-but-oversized prefactored
kernels before solver entry and keep accepted exact results JSON-serializable.
Connections have a 15-second socket timeout and the server
handles at most 64 concurrently. These are bounded local-research controls, not
hard wall-clock cancellation: up to 64 same-host clients can still occupy the
server until their reads time out. Do not route it to an untrusted network
without authentication, process isolation, total request deadlines, and a
hardened deployment layer. Direct Python and CLI research calls remain uncapped
unless their individual contract says otherwise.

Other research commands include:

```bash
PYTHONPATH=src python3 -m coprimebatch.cli shift 101 --max-order 6 --exact --json
PYTHONPATH=src python3 -m coprimebatch.cli certificate 2 3 5 7 --json
PYTHONPATH=src python3 -m coprimebatch.cli benchmark --json
```

Operational categorical and preset requests use the `balance` command:

```bash
PYTHONPATH=src python3 -m coprimebatch.cli balance A=2 B=3 --mode quota --json
PYTHONPATH=src python3 -m coprimebatch.cli balance --mode binary A=1 B=4 --full-order --json
PYTHONPATH=src python3 -m coprimebatch.cli balance --preset rendering-progressive-joint-cells --json
PYTHONPATH=src python3 -m coprimebatch.cli balance A=2 B=2 --mode constrained-quota --constraints-json constraints.json --json
```

Small exact or constrained problems use `--problem-json FILE` (or `-` for
standard input). The corresponding local HTTP request is:

```bash
curl -sS http://127.0.0.1:8765/api/balance \
  -H 'Content-Type: application/json' \
  -d '{"mode":"quota","counts":{"A":2,"B":3}}'
```

The request modes are `quota`, `binary`, `exact`, `constrained`, and
`constrained-quota`.  The compact constrained mode supplies `counts` together
with occurrence-ranked `constraints`; other modes supply exactly one of
`counts`, `problem`, or an allowlisted `preset`.  Large orders are compact
unless `full_order` is explicitly requested below the hard response cap.
`PIN_SPLITS_BLOCK` is a structural admission witness: a pinned prefix or suffix
must contain every occurrence of any fixed block it touches, in the block's
declared order. It does not assert that the more general split-block problem is
mathematically infeasible; that comparison set is outside V1.

The browser includes one generic categorical input plus three allowlisted
synthetic presets:

- rendering progressive joint cells: **benchmark-ready demonstration**;
- financial scenario cells: **demonstration only**;
- pre-randomized laboratory inventory strata: **demonstration only; never
  treatment allocation**.

All three prove only declared joint-cell prefix balance. There is no real
renderer, finance, laboratory, or clinical integration; no observed savings,
accuracy, error reduction, regulatory validation, adoption, or final-all-items
claim.

## Verify everything

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify_operational.py
```

The operational verifier chains the original `verify_all.py` regression and
runs independent exact-arithmetic oracles, CLI/API parity,
malformed-input checks, fixed benchmark gates, scaling canaries, JavaScript
syntax checks, artifact-schema validation, cache hygiene, and mutation-boundary
checks.  Rendered browser interaction is recorded separately because it must
be exercised in a real browser rather than simulated by the unit suite.

It also runs a one-million-item, four-category
subprocess gate with a hard 30-second worker timeout and at most 128 MiB
peak RSS. It consumes the entire packed order, independently checks occurrence
windows and the canonical digest, and compares exact small cases with exhaustive
oracles.  A second frozen million-item gate uses fixed blocks, exact end pins,
and sparse precedence in the same compact execution, independently recomputes
`U`, `Q`, inventory, digest, and every constraint, and checks that the fixture
actually differs from unconstrained EDF.  Passing either software gate does
not validate a domain integration.

## Honest boundary

This is a significant project result, not a claim that external mathematical
priority has been exhaustively established.  The García-specific deduction is
the defensible new theorem after a bounded literature search; its underlying
sampling moments are classical.  The Farey-shear and coprime-layer results
remain subject to specialist formula-level review before publication.  The
CoprimeBatch optimizer is useful only under its declared complete-layer
constraint and is not competitive with unrestricted midpoint or established
quadrature rules.

The operational prefix-balance extension is likewise scoped. It has no
million-scale arbitrary-vector constructor, no general-vector constant-factor
guarantee, no arbitrary interior pins or flexible block interiors, and no
evidence yet that balancing declared cells improves a renderer, risk estimate,
scientific conclusion, or final result after all items are processed. One UCI
model-audit replay now shows a statistical prefix-estimation gain under declared
prediction/confidence strata, but it does not yet establish a deployable stopping
rule, human-time saving, workflow-overhead saving, or monetary benefit.
