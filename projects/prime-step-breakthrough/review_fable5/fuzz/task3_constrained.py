#!/usr/bin/env python3
"""Task 3: Constrained quota solver vs exhaustive queue-interleaving oracle."""

from __future__ import annotations

import json
import random
import time
from fractions import Fraction
from pathlib import Path

from common import fmt_ratio
from constrained_quota_oracles import (
    constraint_errors,
    exact_metrics,
    exhaustive_optimum,
    normalized_inventory,
)
from coprimebatch.prefix_balance import (
    CategoricalConstraintProblem,
    FixedOccurrenceBlock,
    InfeasibleProblemError,
    OccurrencePrecedence,
    OccurrenceRef,
    solve_constrained_quota,
)

OUT = Path(__file__).with_name("results_task3.json")
RNG = random.Random(20260716)


def make_categories(k: int) -> tuple[str, ...]:
    return tuple(chr(ord("a") + i) for i in range(k))


def random_counts(n: int, k: int) -> dict[str, int]:
    cats = make_categories(k)
    # Stars and bars positive-biased: allow zeros
    cuts = sorted(RNG.randint(0, n) for _ in range(k - 1))
    parts = [cuts[0]] + [cuts[i] - cuts[i - 1] for i in range(1, k - 1)] + [n - cuts[-1]]
    if k == 1:
        parts = [n]
    return {cats[i]: parts[i] for i in range(k)}


def occurrence_pool(counts: dict[str, int]) -> list[OccurrenceRef]:
    refs: list[OccurrenceRef] = []
    for cat, count in sorted(counts.items()):
        for occ in range(1, count + 1):
            refs.append(OccurrenceRef(cat, occ))
    return refs


def random_block(refs: list[OccurrenceRef], length: int) -> FixedOccurrenceBlock | None:
    if length < 2 or len(refs) < length:
        return None
    # Prefer contiguous-in-queue same-category runs OR mixed categories
    if RNG.random() < 0.45:
        # same-category contiguous occurrences
        by_cat: dict[str, list[OccurrenceRef]] = {}
        for ref in refs:
            by_cat.setdefault(ref.category, []).append(ref)
        candidates = [v for v in by_cat.values() if len(v) >= length]
        if not candidates:
            return None
        run = RNG.choice(candidates)
        start = RNG.randint(0, len(run) - length)
        chosen = tuple(run[start : start + length])
    else:
        chosen = tuple(RNG.sample(refs, length))
    return FixedOccurrenceBlock(block_id="b0", occurrences=chosen)


def build_random_instance(n: int, k: int) -> CategoricalConstraintProblem:
    counts = random_counts(n, k)
    refs = occurrence_pool(counts)
    fixed_blocks: tuple[FixedOccurrenceBlock, ...] = ()
    pinned_prefix: tuple[OccurrenceRef, ...] = ()
    pinned_suffix: tuple[OccurrenceRef, ...] = ()
    precedence: tuple[OccurrencePrecedence, ...] = ()

    if refs and RNG.random() < 0.7:
        length = RNG.choice([2, 3] if n >= 3 else [2])
        block = random_block(refs, length)
        if block is not None:
            fixed_blocks = (block,)

    if refs and RNG.random() < 0.55:
        pinned_prefix = (RNG.choice(refs),)

    if refs and RNG.random() < 0.55:
        # avoid identical pin when possible
        candidates = [r for r in refs if not pinned_prefix or r != pinned_prefix[0]]
        if candidates:
            pinned_suffix = (RNG.choice(candidates),)

    edges: list[OccurrencePrecedence] = []
    if len(refs) >= 2 and RNG.random() < 0.65:
        left, right = RNG.sample(refs, 2)
        edges.append(OccurrencePrecedence("e0", left, right))
    if len(refs) >= 3 and RNG.random() < 0.35:
        left, right = RNG.sample(refs, 2)
        edges.append(OccurrencePrecedence("e1", left, right))
    precedence = tuple(edges)

    return CategoricalConstraintProblem(
        counts=counts,
        fixed_blocks=fixed_blocks,
        pinned_prefix=pinned_prefix,
        pinned_suffix=pinned_suffix,
        precedence=precedence,
    )


def systematic_cases() -> list[CategoricalConstraintProblem]:
    cases: list[CategoricalConstraintProblem] = []

    # repeated-category block
    cases.append(
        CategoricalConstraintProblem(
            counts={"a": 3, "b": 2},
            fixed_blocks=(
                FixedOccurrenceBlock(
                    "blk",
                    (OccurrenceRef("a", 1), OccurrenceRef("a", 2)),
                ),
            ),
        )
    )
    # mixed block + prefix pin
    cases.append(
        CategoricalConstraintProblem(
            counts={"a": 2, "b": 2, "c": 2},
            fixed_blocks=(
                FixedOccurrenceBlock(
                    "blk",
                    (OccurrenceRef("a", 1), OccurrenceRef("b", 1)),
                ),
            ),
            pinned_prefix=(OccurrenceRef("c", 1),),
        )
    )
    # block + suffix pin
    cases.append(
        CategoricalConstraintProblem(
            counts={"a": 3, "b": 3},
            fixed_blocks=(
                FixedOccurrenceBlock(
                    "blk",
                    (OccurrenceRef("b", 2), OccurrenceRef("a", 2)),
                ),
            ),
            pinned_suffix=(OccurrenceRef("a", 3),),
        )
    )
    # precedence chain
    cases.append(
        CategoricalConstraintProblem(
            counts={"a": 2, "b": 2, "c": 2},
            precedence=(
                OccurrencePrecedence("e0", OccurrenceRef("a", 1), OccurrenceRef("b", 1)),
                OccurrencePrecedence("e1", OccurrenceRef("b", 1), OccurrenceRef("c", 1)),
            ),
        )
    )
    # zero-count category present
    cases.append(
        CategoricalConstraintProblem(
            counts={"a": 2, "b": 0, "c": 2},
            pinned_prefix=(OccurrenceRef("a", 1),),
            precedence=(
                OccurrencePrecedence("e0", OccurrenceRef("a", 2), OccurrenceRef("c", 1)),
            ),
        )
    )
    # single category
    cases.append(CategoricalConstraintProblem(counts={"a": 5}))
    # equal counts
    cases.append(
        CategoricalConstraintProblem(
            counts={"a": 3, "b": 3},
            pinned_prefix=(OccurrenceRef("a", 1),),
            pinned_suffix=(OccurrenceRef("b", 3),),
        )
    )
    # N divisible by counts
    cases.append(
        CategoricalConstraintProblem(
            counts={"a": 2, "b": 2, "c": 2},
            fixed_blocks=(
                FixedOccurrenceBlock(
                    "blk",
                    (OccurrenceRef("a", 1), OccurrenceRef("a", 2)),
                ),
            ),
        )
    )
    # N not divisible
    cases.append(
        CategoricalConstraintProblem(
            counts={"a": 2, "b": 3},
            precedence=(
                OccurrencePrecedence("e0", OccurrenceRef("b", 1), OccurrenceRef("a", 1)),
            ),
        )
    )
    # empty
    cases.append(CategoricalConstraintProblem(counts={"a": 0, "b": 0}))
    # only block spanning all of one category then pin conflict-ish
    cases.append(
        CategoricalConstraintProblem(
            counts={"a": 2, "b": 2},
            fixed_blocks=(
                FixedOccurrenceBlock(
                    "blk",
                    (OccurrenceRef("a", 1), OccurrenceRef("b", 1), OccurrenceRef("a", 2)),
                ),
            ),
            pinned_suffix=(OccurrenceRef("b", 2),),
        )
    )
    return cases


def check_instance(problem: CategoricalConstraintProblem) -> dict | None:
    """Return a finding dict, or None if OK / infeasible-agree.

    PIN_SPLITS_BLOCK vs expanded-oracle feasibility is recorded as a soft note
    (documented unsupported), not a certificate failure.
    """
    oracle = exhaustive_optimum(problem)
    try:
        result = solve_constrained_quota(problem)
    except InfeasibleProblemError as exc:
        if oracle is None:
            return None  # agree infeasible
        kind = (
            "pin_splits_block_documented"
            if "PIN_SPLITS_BLOCK" in str(exc)
            else "solver_infeasible_but_oracle_feasible"
        )
        return {
            "kind": kind,
            "counts": dict(problem.counts) if hasattr(problem.counts, "items") else list(problem.counts),
            "witness": str(exc),
            "oracle_opt_B": str(oracle.max_discrepancy),
            "oracle_feasible": oracle.feasible_orders,
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "kind": "solver_error",
            "counts": dict(problem.counts) if hasattr(problem.counts, "items") else list(problem.counts),
            "error": repr(exc),
            "oracle_feasible": None if oracle is None else oracle.feasible_orders,
        }

    if oracle is None:
        return {
            "kind": "solver_feasible_but_oracle_infeasible",
            "counts": dict(problem.counts) if hasattr(problem.counts, "items") else list(problem.counts),
            "order": list(result.order_codes),
            "U": str(result.max_discrepancy),
            "L": str(result.lower_bound),
        }

    codes = tuple(int(c) for c in result.order_codes)
    cerr = constraint_errors(problem, codes)
    if cerr:
        return {
            "kind": "constraint_violation",
            "counts": dict(problem.counts) if hasattr(problem.counts, "items") else list(problem.counts),
            "order": list(codes),
            "errors": list(cerr),
        }

    recomputed_b, recomputed_q, merr = exact_metrics(problem.counts, codes)
    if merr:
        return {
            "kind": "metric_error",
            "order": list(codes),
            "errors": list(merr),
        }

    if recomputed_b != result.max_discrepancy:
        return {
            "kind": "U_mismatch_vs_recomputed",
            "order": list(codes),
            "U": str(result.max_discrepancy),
            "recomputed_B": str(recomputed_b),
        }

    if recomputed_q != result.accumulated_discrepancy:
        return {
            "kind": "Q_mismatch_vs_recomputed",
            "order": list(codes),
            "cert_Q": str(result.accumulated_discrepancy),
            "recomputed_Q": str(recomputed_q),
        }

    opt_b = oracle.max_discrepancy
    L = result.lower_bound
    U = result.max_discrepancy
    if not (L <= opt_b <= U):
        return {
            "kind": "certificate_interval_fail",
            "counts": dict(problem.counts) if hasattr(problem.counts, "items") else list(problem.counts),
            "L": str(L),
            "OPT_B": str(opt_b),
            "U": str(U),
            "order": list(codes),
            "opt_order": list(oracle.order_codes),
            "feasible_orders": oracle.feasible_orders,
            "fixed_blocks": [
                [(r.category, r.occurrence) for r in b.occurrences] for b in problem.fixed_blocks
            ],
            "pinned_prefix": [(r.category, r.occurrence) for r in problem.pinned_prefix],
            "pinned_suffix": [(r.category, r.occurrence) for r in problem.pinned_suffix],
            "precedence": [
                ((e.before.category, e.before.occurrence), (e.after.category, e.after.occurrence))
                for e in problem.precedence
            ],
        }

    return None


def problem_snapshot(problem: CategoricalConstraintProblem) -> dict:
    return {
        "counts": dict(problem.counts) if hasattr(problem.counts, "items") else list(problem.counts),
        "fixed_blocks": [
            [(r.category, r.occurrence) for r in b.occurrences] for b in problem.fixed_blocks
        ],
        "pinned_prefix": [(r.category, r.occurrence) for r in problem.pinned_prefix],
        "pinned_suffix": [(r.category, r.occurrence) for r in problem.pinned_suffix],
        "precedence": [
            ((e.before.category, e.before.occurrence), (e.after.category, e.after.occurrence))
            for e in problem.precedence
        ],
    }


def main() -> int:
    t0 = time.perf_counter()
    feasible_checked = 0
    infeasible_agree = 0
    random_attempts = 0
    target_feasible = 500

    pin_split_notes: list[dict] = []
    hard_findings: list[dict] = []

    def record(problem: CategoricalConstraintProblem, source: str) -> None:
        nonlocal feasible_checked, infeasible_agree
        oracle = exhaustive_optimum(problem)
        finding = check_instance(problem)
        if finding is not None:
            finding["instance"] = problem_snapshot(problem)
            finding["source"] = source
            if finding["kind"] == "pin_splits_block_documented":
                pin_split_notes.append(finding)
            else:
                hard_findings.append(finding)
        elif oracle is None:
            infeasible_agree += 1
        else:
            feasible_checked += 1

    for problem in systematic_cases():
        record(problem, "systematic")

    while feasible_checked < target_feasible and random_attempts < 30000 and len(hard_findings) < 40:
        random_attempts += 1
        n = RNG.randint(2, 8)
        k = RNG.choice([2, 3] if n >= 3 else [2])
        if k == 3 and n < 3:
            k = 2
        record(build_random_instance(n, k), "random")

    findings = hard_findings
    finding_counts: dict[str, int] = {}
    for finding in findings:
        kind = str(finding.get("kind", "unknown"))
        finding_counts[kind] = finding_counts.get(kind, 0) + 1
    payload = {
        "task": 3,
        "elapsed_s": time.perf_counter() - t0,
        "feasible_checked_solver_accepted": feasible_checked,
        "infeasible_agree": infeasible_agree,
        "pin_splits_block_rejects_expanded_feasible": len(pin_split_notes),
        "other_solver_infeas_oracle_feas": finding_counts.get(
            "solver_infeasible_but_oracle_feasible", 0
        ),
        "random_attempts": random_attempts,
        "certificate_interval_failures": finding_counts.get(
            "certificate_interval_fail", 0
        ),
        "constraint_violations_on_returned_orders": finding_counts.get(
            "constraint_violation", 0
        ),
        "findings_math_certificate": findings[:30],
        "documented_restriction_note": (
            "PIN_SPLITS_BLOCK: solver intentionally rejects pins that partially "
            "overlap a fixed block. Expanded-order oracle treats some of these "
            "as feasible. Contract documents this as unsupported."
        ),
        "pin_split_reproducer": {
            "counts": {"a": 0, "b": 3},
            "fixed_blocks": [[("b", 1), ("b", 2), ("b", 3)]],
            "pinned_suffix": [("b", 3)],
            "expanded_feasible": True,
            "solver_witness": "PIN_SPLITS_BLOCK",
        },
        "verdict_hint": (
            "REFUTED"
            if findings
            else (
                f"HOLDS on {feasible_checked} solver-accepted feasible instances "
                "(L<=OPT_B<=U); PIN_SPLITS_BLOCK rejects "
                f"{len(pin_split_notes)} expanded-feasible instances by "
                "documented design"
            )
        ),
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n")
    print(
        json.dumps(
            {k: payload[k] for k in payload if k != "findings"},
            indent=2,
        )
    )
    print(f"findings: {len(findings)}  wrote {OUT}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
