#!/usr/bin/env python3
"""Minimal reproducers for adversarial fuzz findings / documented edge cases."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "tests")]

from constrained_quota_oracles import exhaustive_optimum
from coprimebatch.prefix_balance import (
    CategoricalConstraintProblem,
    FixedOccurrenceBlock,
    InfeasibleProblemError,
    OccurrenceRef,
    quota_mechanical_order,
    quota_order,
)
from prefix_balance_oracles import (
    exhaustive_quota_optimum,
    lower_binary_mechanical,
    quota_metrics,
)


def ratio_2_1() -> None:
    counts = (2, 1)
    result = quota_order(counts)
    order = tuple(result.order_codes)
    b, _, err = quota_metrics(counts, order, check_windows=True)
    assert not err, err
    opt_b, _, opt_order = exhaustive_quota_optimum(counts)
    ratio = b / opt_b
    print(f"(2,1) quota_order={list(order)} B={b} OPT={opt_b} order={list(opt_order)} ratio={ratio}")
    assert ratio == 2


def lower_word_1_4() -> None:
    lower = lower_binary_mechanical(1, 4)
    lb, lq, _ = quota_metrics((1, 4), lower, check_windows=False)
    opt_b, opt_q, opt_order = exhaustive_quota_optimum((1, 4))
    nearest = tuple(quota_mechanical_order(1, 4).order_codes)
    print(f"lower(1,4)={list(lower)} B={lb} Q={lq}")
    print(f"opt={list(opt_order)} B={opt_b} Q={opt_q}")
    print(f"mechanical={list(nearest)}")
    assert lb > opt_b or (lb == opt_b and lq > opt_q)


def pin_splits_block() -> None:
    problem = CategoricalConstraintProblem(
        counts={"a": 0, "b": 3},
        fixed_blocks=(
            FixedOccurrenceBlock(
                "blk",
                (
                    OccurrenceRef("b", 1),
                    OccurrenceRef("b", 2),
                    OccurrenceRef("b", 3),
                ),
            ),
        ),
        pinned_suffix=(OccurrenceRef("b", 3),),
    )
    oracle = exhaustive_optimum(problem)
    assert oracle is not None and oracle.feasible_orders == 1
    try:
        from coprimebatch.prefix_balance import solve_constrained_quota

        solve_constrained_quota(problem)
        raise AssertionError("expected PIN_SPLITS_BLOCK")
    except InfeasibleProblemError as exc:
        assert "PIN_SPLITS_BLOCK" in str(exc)
        print(f"PIN_SPLITS_BLOCK as documented: {exc}")


if __name__ == "__main__":
    ratio_2_1()
    lower_word_1_4()
    pin_splits_block()
    print("all reproducers OK")
