#!/usr/bin/env python3
"""Task 2: Binary mechanical prefix-optimality + lower-word negative control."""

from __future__ import annotations

import json
import time
from fractions import Fraction
from pathlib import Path

from common import fmt_ratio
from coprimebatch.prefix_balance import quota_mechanical_order
from prefix_balance_oracles import (
    exhaustive_quota_optimum,
    lower_binary_mechanical,
    nearest_binary_mechanical,
    quota_metrics,
)

OUT = Path(__file__).with_name("results_task2.json")


def prefixwise_compare(
    counts: tuple[int, int], order: tuple[int, ...]
) -> tuple[Fraction, Fraction]:
    peak, acc, errs = quota_metrics(counts, order, check_windows=False)
    if errs:
        raise AssertionError(errs)
    return peak, acc


def main() -> int:
    t0 = time.perf_counter()
    findings: list[dict] = []
    errors: list[dict] = []
    checked = 0
    max_pairs = 0

    for a in range(0, 13):
        for b in range(0, 13 - a):
            max_pairs += 1
            counts = (a, b)
            try:
                result = quota_mechanical_order(a, b)
            except Exception as exc:  # noqa: BLE001
                errors.append({"counts": list(counts), "error": repr(exc)})
                continue

            order = tuple(int(c) for c in result.order_codes)
            oracle_peak, oracle_acc = prefixwise_compare(counts, order)
            opt_peak, opt_acc, opt_order = exhaustive_quota_optimum(counts)

            # Claim: prefixwise EXACT optimality for primary B and accumulated Q
            if oracle_peak != opt_peak or oracle_acc != opt_acc:
                findings.append(
                    {
                        "kind": "mechanical_not_prefix_optimal",
                        "counts": list(counts),
                        "order": list(order),
                        "mech_B": str(oracle_peak),
                        "mech_Q": str(oracle_acc),
                        "opt_B": str(opt_peak),
                        "opt_Q": str(opt_acc),
                        "opt_order": list(opt_order),
                        "cert_B": str(result.max_discrepancy),
                        "exact_optimum_flag": result.exact_optimum,
                    }
                )

            if result.max_discrepancy != oracle_peak:
                findings.append(
                    {
                        "kind": "certificate_B_mismatch",
                        "counts": list(counts),
                        "cert_B": str(result.max_discrepancy),
                        "oracle_B": str(oracle_peak),
                    }
                )

            indep = nearest_binary_mechanical(a, b)
            if indep != order:
                findings.append(
                    {
                        "kind": "differs_from_independent_nearest",
                        "counts": list(counts),
                        "solver": list(order),
                        "oracle_nearest": list(indep),
                    }
                )

            checked += 1

    # Documented counterexample: lower mechanical is NOT minimax for (1,4)
    lower = lower_binary_mechanical(1, 4)
    lower_b, lower_q = prefixwise_compare((1, 4), lower)
    opt_b, opt_q, opt_order = exhaustive_quota_optimum((1, 4))
    nearest = nearest_binary_mechanical(1, 4)
    nearest_b, nearest_q = prefixwise_compare((1, 4), nearest)
    lower_is_suboptimal = lower_b > opt_b or (lower_b == opt_b and lower_q > opt_q)
    if not lower_is_suboptimal:
        findings.append(
            {
                "kind": "lower_word_unexpectedly_optimal_on_1_4",
                "lower_order": list(lower),
                "lower_B": str(lower_b),
                "lower_Q": str(lower_q),
                "opt_B": str(opt_b),
                "opt_Q": str(opt_q),
            }
        )

    payload = {
        "task": 2,
        "elapsed_s": time.perf_counter() - t0,
        "pairs_enumerated": max_pairs,
        "checked": checked,
        "lower_word_1_4": {
            "order": list(lower),
            "B": str(lower_b),
            "Q": str(lower_q),
            "opt_B": str(opt_b),
            "opt_Q": str(opt_q),
            "opt_order": list(opt_order),
            "nearest_order": list(nearest),
            "nearest_B": str(nearest_b),
            "nearest_Q": str(nearest_q),
            "confirmed_not_minimax": lower_is_suboptimal,
        },
        "solver_errors": errors,
        "findings": findings,
        "verdict_hint": (
            "REFUTED"
            if findings or errors
            else f"HOLDS ({checked} pairs); lower(1,4) not minimax confirmed"
        ),
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({k: payload[k] for k in payload if k != "findings"}, indent=2))
    print(f"findings: {len(findings)}  wrote {OUT}")
    return 1 if findings or errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
