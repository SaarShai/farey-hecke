#!/usr/bin/env python3
"""Task 4: solve_exact vs exhaustive general optimum for small rational vectors."""

from __future__ import annotations

import json
import time
from fractions import Fraction
from itertools import combinations_with_replacement
from pathlib import Path

from common import fmt_ratio
from coprimebatch.prefix_balance import BalanceItem, BalanceProblem, solve_exact
from prefix_balance_oracles import (
    OracleItem,
    SEVEN_ITEM_LEX_COUNTEREXAMPLE,
    SUM_FIRST_COUNTEREXAMPLE,
    exhaustive_general_optimum,
    general_order_metrics,
)

OUT = Path(__file__).with_name("results_task4.json")


def audit_instances() -> tuple[list[BalanceProblem], dict[str, int]]:
    """Return the complete, deterministic small-instance audit family."""

    problems: list[BalanceProblem] = []
    seen: set[tuple] = set()
    family_new_counts: dict[str, int] = {}

    def add(problem: BalanceProblem, family: str) -> None:
        key = tuple(sorted((item.contribution, item.mass) for item in problem.items))
        if key in seen:
            return
        seen.add(key)
        problems.append(problem)
        family_new_counts[family] = family_new_counts.get(family, 0) + 1

    def add_scalar_family(name: str, alphabet: tuple, max_n: int) -> None:
        for n in range(1, max_n + 1):
            for values in combinations_with_replacement(alphabet, n):
                add(
                    BalanceProblem(
                        items=tuple(
                            BalanceItem(f"{name}{i}", (value,), 1)
                            for i, value in enumerate(values)
                        )
                    ),
                    name,
                )

    add_scalar_family("signs", (-1, 1), 7)
    add_scalar_family("integers", (-2, -1, 0, 1, 2), 4)
    add_scalar_family(
        "fractions",
        (
            Fraction(-1, 2),
            Fraction(-1, 3),
            Fraction(1, 3),
            Fraction(1, 2),
            Fraction(2, 3),
        ),
        4,
    )

    vectors = tuple((a, b) for a in (-1, 0, 1) for b in (-1, 0, 1))
    for n in range(1, 4):
        for values in combinations_with_replacement(vectors, n):
            add(
                BalanceProblem(
                    items=tuple(
                        BalanceItem(f"vectors{i}", value, 1)
                        for i, value in enumerate(values)
                    )
                ),
                "vectors_2d",
            )

    weighted_signs = ((-1, 1), (1, 1), (-1, 2), (1, 2))
    for n in range(1, 5):
        for values in combinations_with_replacement(weighted_signs, n):
            add(
                BalanceProblem(
                    items=tuple(
                        BalanceItem(f"weighted{i}", (value,), mass)
                        for i, (value, mass) in enumerate(values)
                    )
                ),
                "weighted_signs",
            )

    for name, values in (
        ("seven_item_lex_trap", SEVEN_ITEM_LEX_COUNTEREXAMPLE),
        ("sum_first_trap", SUM_FIRST_COUNTEREXAMPLE),
    ):
        add(
            BalanceProblem(
                items=tuple(
                    BalanceItem(f"{name}{i}", (value,), 1)
                    for i, value in enumerate(values)
                )
            ),
            name,
        )

    if len(problems) != 547:
        raise AssertionError(f"audit family drifted: expected 547, got {len(problems)}")
    return problems, family_new_counts


def to_oracle_items(problem: BalanceProblem) -> tuple[OracleItem, ...]:
    return tuple(
        OracleItem(item_id=item.item_id, contribution=item.contribution, mass=item.mass)
        for item in problem.items
    )


def main() -> int:
    t0 = time.perf_counter()
    problems, family_counts = audit_instances()

    findings: list[dict] = []
    errors: list[dict] = []
    checked = 0

    for problem in problems:
        oracle_items = to_oracle_items(problem)
        oracle = exhaustive_general_optimum(oracle_items)
        assert oracle is not None
        try:
            result = solve_exact(problem)
        except Exception as exc:  # noqa: BLE001
            errors.append(
                {
                    "items": [list(it.contribution) for it in problem.items],
                    "error": repr(exc),
                }
            )
            continue

        recomputed_b, recomputed_q = general_order_metrics(oracle_items, result.order)
        if recomputed_b != result.max_discrepancy or recomputed_q != result.accumulated_discrepancy:
            findings.append(
                {
                    "kind": "solver_metrics_mismatch",
                    "order": list(result.order),
                    "cert_B": str(result.max_discrepancy),
                    "cert_Q": str(result.accumulated_discrepancy),
                    "recomputed_B": str(recomputed_b),
                    "recomputed_Q": str(recomputed_q),
                    "items": [list(map(str, it.contribution)) for it in problem.items],
                }
            )

        if recomputed_b != oracle.max_discrepancy or recomputed_q != oracle.accumulated_discrepancy:
            findings.append(
                {
                    "kind": "not_lex_optimal",
                    "order": list(result.order),
                    "solver_B": str(recomputed_b),
                    "solver_Q": str(recomputed_q),
                    "opt_B": str(oracle.max_discrepancy),
                    "opt_Q": str(oracle.accumulated_discrepancy),
                    "opt_order": list(oracle.order),
                    "items": [list(map(str, it.contribution)) for it in problem.items],
                }
            )

        if not result.exact_optimum:
            findings.append(
                {
                    "kind": "exact_flag_false",
                    "items": [list(map(str, it.contribution)) for it in problem.items],
                }
            )

        checked += 1
        if checked % 500 == 0:
            print(f"… checked {checked}/{len(problems)} findings={len(findings)}", flush=True)

    payload = {
        "task": 4,
        "elapsed_s": time.perf_counter() - t0,
        "problems": len(problems),
        "checked": checked,
        "families": family_counts,
        "known_traps": ["SEVEN_ITEM_LEX_COUNTEREXAMPLE", "SUM_FIRST_COUNTEREXAMPLE"],
        "solver_errors": errors[:20],
        "solver_error_count": len(errors),
        "findings_count": len(findings),
        "findings": findings[:20],
        "verdict_hint": (
            "REFUTED"
            if findings or errors
            else f"HOLDS ({checked} instances)"
        ),
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({k: payload[k] for k in payload if k != "findings"}, indent=2))
    print(f"findings: {len(findings)}  wrote {OUT}")
    return 1 if findings or errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
