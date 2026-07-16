#!/usr/bin/env python3
"""Task 1: Exhaustive quota_order vs unconstrained OPT_B for N<=9, C<=4."""

from __future__ import annotations

import json
import time
from fractions import Fraction
from pathlib import Path

from common import count_vectors, fmt_ratio, ratio_or_none
from coprimebatch.prefix_balance import quota_order
from prefix_balance_oracles import (
    exhaustive_quota_optimum,
    quota_metrics,
    quota_reachability_path,
)

OUT = Path(__file__).with_name("results_task1.json")


def main() -> int:
    t0 = time.perf_counter()
    vectors = count_vectors(max_n=9, max_categories=4)
    # Focus: sum <= 9. count_vectors already does that.
    findings: list[dict] = []
    max_ratio: Fraction | None = None
    max_ratio_vec: tuple[int, ...] | None = None
    checked = 0
    quota_violations = 0
    ratio_ge3 = 0
    errors: list[dict] = []

    for vec in vectors:
        n = sum(vec)
        positive = sum(1 for x in vec if x > 0)
        try:
            result = quota_order(vec)
        except Exception as exc:  # noqa: BLE001 — adversarial: any raise is a finding
            errors.append({"counts": list(vec), "error": repr(exc)})
            continue

        order = tuple(int(c) for c in result.order_codes)
        peak, _acc, window_errors = quota_metrics(vec, order, check_windows=True)
        if window_errors:
            quota_violations += 1
            findings.append(
                {
                    "kind": "quota_violation",
                    "counts": list(vec),
                    "order": list(order),
                    "errors": list(window_errors),
                    "cert_B": str(result.max_discrepancy),
                    "oracle_B": str(peak),
                }
            )

        # Independent recomputed B (windows off for metric)
        oracle_b, _, metric_errs = quota_metrics(vec, order, check_windows=False)
        if metric_errs:
            findings.append(
                {
                    "kind": "metric_error",
                    "counts": list(vec),
                    "order": list(order),
                    "errors": list(metric_errs),
                }
            )

        if result.max_discrepancy != oracle_b:
            findings.append(
                {
                    "kind": "certificate_B_mismatch",
                    "counts": list(vec),
                    "order": list(order),
                    "cert_B": str(result.max_discrepancy),
                    "oracle_B": str(oracle_b),
                }
            )

        opt_b, _opt_q, opt_order = exhaustive_quota_optimum(vec)
        ratio = ratio_or_none(oracle_b, opt_b)
        if ratio is not None and (max_ratio is None or ratio > max_ratio):
            max_ratio = ratio
            max_ratio_vec = vec

        if positive >= 2 and ratio is not None and ratio >= 3:
            ratio_ge3 += 1
            findings.append(
                {
                    "kind": "ratio_ge_3",
                    "counts": list(vec),
                    "order": list(order),
                    "oracle_B": str(oracle_b),
                    "opt_B": str(opt_b),
                    "opt_order": list(opt_order),
                    "ratio": str(ratio),
                    "claimed_strict_factor": result.strict_factor,
                }
            )

        # Reachability sanity: a quota-valid path should exist (Baranyai/Tijdeman)
        if n > 0 and positive >= 1:
            path = quota_reachability_path(vec)
            if path is None:
                findings.append(
                    {
                        "kind": "no_quota_path_exists",
                        "counts": list(vec),
                    }
                )

        checked += 1

    payload = {
        "task": 1,
        "elapsed_s": time.perf_counter() - t0,
        "vectors_enumerated": len(vectors),
        "checked": checked,
        "quota_violations": quota_violations,
        "ratio_ge3": ratio_ge3,
        "max_ratio": None if max_ratio is None else str(max_ratio),
        "max_ratio_float": None if max_ratio is None else float(max_ratio),
        "max_ratio_counts": None if max_ratio_vec is None else list(max_ratio_vec),
        "solver_errors": errors,
        "findings": findings,
        "verdict_hint": (
            "REFUTED"
            if findings or errors
            else f"HOLDS ({checked} instances); max_ratio={fmt_ratio(max_ratio)}"
        ),
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({k: payload[k] for k in payload if k != "findings"}, indent=2))
    print(f"findings: {len(findings)}  wrote {OUT}")
    return 1 if findings or errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
