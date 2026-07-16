# Prefix-Balance V1 Implementation Contract

This file is the sole API contract for the first build wave.  Builders may
raise an issue, but must not silently change these names or semantics.

## Core module

Create `src/coprimebatch/prefix_balance.py` with no third-party dependencies.

### Public data types

```python
@dataclass(frozen=True)
class BalanceItem:
    item_id: str
    contribution: tuple[int | Fraction, ...]
    mass: int = 1
    category: str | None = None

@dataclass(frozen=True)
class BalanceProblem:
    items: tuple[BalanceItem, ...]
    fixed_blocks: tuple[tuple[str, ...], ...] = ()
    pinned_prefix: tuple[str, ...] = ()
    pinned_suffix: tuple[str, ...] = ()
    precedence: tuple[tuple[str, str], ...] = ()

@dataclass(frozen=True)
class ConstraintWitness:
    code: str
    message: str
    details: dict[str, object]

class InfeasibleProblemError(ValueError):
    witness: ConstraintWitness

@dataclass
class QuotaResult:
    schema_version: str
    algorithm: str
    categories: tuple[str, ...]
    counts: tuple[int, ...]
    order_codes: array
    max_discrepancy: Fraction
    lower_bound: Fraction
    ratio_bound: Fraction | None
    strict_factor: int | None
    exact_optimum: bool
    order_sha256: str
    digest_encoding: str
    guarantee_scope: str
    comparison_set: str
    explanation: dict[str, object]

@dataclass(frozen=True)
class OrderingResult:
    schema_version: str
    algorithm: str
    order: tuple[str, ...]
    max_discrepancy: Fraction
    accumulated_discrepancy: Fraction
    lower_bound: Fraction
    ratio_bound: Fraction | None
    additive_gap: Fraction
    exact_optimum: bool
    guarantee_scope: str
    comparison_set: str
    feasibility: dict[str, object]
    explanation: dict[str, object]

@dataclass(frozen=True)
class VerificationReport:
    passed: bool
    errors: tuple[str, ...]
    max_discrepancy: Fraction | None
    accumulated_discrepancy: Fraction | None
    order_sha256: str | None
```

All mutable dictionaries must be freshly owned by the result.  The exact field
set may gain timing-free diagnostic fields, but names above may not disappear.

### Public functions

```python
quota_order(counts: Mapping[str, int] | Sequence[int]) -> QuotaResult
quota_mechanical_order(first: int, second: int) -> QuotaResult
verify_quota_result(result: QuotaResult) -> VerificationReport

solve_exact(problem: BalanceProblem, *, max_units: int = 18,
            max_items: int = 24) -> OrderingResult
solve_constrained(problem: BalanceProblem) -> OrderingResult
verify_order(problem: BalanceProblem,
             order: Sequence[str]) -> VerificationReport
```

`quota_order` uses release-aware EDF, exact integer release/deadline formulas,
stable UTF-8 byte-key ties, an `array('I')` order, and canonical SHA-256 over
four-byte unsigned big-endian category codes.  Zero-count categories remain in
the result but never appear in the order.  An all-zero inventory returns the
empty exact optimum.  Duplicate/invalid keys and negative/bool counts fail.

`quota_mechanical_order` emits the nearest-integer binary mechanical word with
first-category prefix count `floor(k*first/(first+second) + 1/2)`.  It is
separate from EDF and is prefixwise exact for both primary and accumulated
objectives.  It must not use the merely quota-valid lower word
`floor(k*first/(first+second))`; counts `(1,4)` distinguish them.

`solve_exact` implements the two-pass trace-aware subset DP from
`OPERATIONAL_ARCHITECTURE.md`.  It refuses limits with code
`ORACLE_LIMIT_EXCEEDED`.  `solve_constrained` contracts fixed blocks, respects
whole-unit end pins and the sparse DAG, and uses categorical urgency when every
item has a category; otherwise it uses stable-ID Kahn order.  It never emits the
categorical `<3` label unless the problem is unconstrained, equal-mass, and
one-hot.

The general/exact problem path accepts `int` and `Fraction` contributions and
rejects `bool`, `float`, nonfinite, or other numeric objects with
`NONRATIONAL_CONTRIBUTION`.  Thus `contribution=(g_i,)`, `mass=1` exactly
reproduces the existing rational one-dimensional gap prefix delta.  The
specialized million-item quota path remains integer-only.

### Required witness codes

```text
DUPLICATE_ITEM_ID
DIMENSION_MISMATCH
NONRATIONAL_CONTRIBUTION
INVALID_MASS
CENTERING_RESIDUAL
UNKNOWN_CONSTRAINT_ID
BLOCK_OVERLAP
BLOCK_REPEATED_ITEM
BLOCK_INTERNAL_PRECEDENCE_REVERSED
PREFIX_SUFFIX_OVERLAP
PIN_SPLITS_BLOCK
PIN_ORDER_PRECEDENCE_CONFLICT
CONTRACTED_DAG_CYCLE
ORACLE_LIMIT_EXCEEDED
```

Additional precise codes are allowed.  Solver failure is never an
infeasibility witness outside the supported V1 contract.

## Independent verification module

Create `tests/prefix_balance_oracles.py`, `tests/test_prefix_balance.py`,
`benchmark_operational.py`, and `verify_operational.py` without editing the
production module.

The verifier must independently implement quota reachability/exhaustive
permutation oracles, result recomputation, artifact validation, negative
threshold mutations, source/cache mutation checks, and the registered
million-item subprocess benchmark.  Frozen thresholds are `<30.0` seconds and
`<=134,217,728` bytes peak RSS, with the worker forcibly timed out at 30 seconds.
The benchmark fixture is one million items,
four positive unequal counts, and must consume all output into a canonical
digest while independently checking occurrence windows.

## Integration deferred to wave two

Wave-one builders must not edit `__init__.py`, `cli.py`, `web.py`, `web/`,
`README.md`, `verify_all.py`, existing tests, or existing artifacts.  Those
shared integration paths have one sequential owner after core and verifier
contracts pass.
