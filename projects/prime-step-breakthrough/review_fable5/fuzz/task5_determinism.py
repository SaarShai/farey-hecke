#!/usr/bin/env python3
"""Task 5: Determinism under dict insertion order / UTF-8 category names."""

from __future__ import annotations

import json
import time
from collections import OrderedDict
from pathlib import Path

from coprimebatch.prefix_balance import (
    CategoricalConstraintProblem,
    FixedOccurrenceBlock,
    OccurrencePrecedence,
    OccurrenceRef,
    quota_order,
    solve_constrained_quota,
)

OUT = Path(__file__).with_name("results_task5.json")


def main() -> int:
    t0 = time.perf_counter()
    findings: list[dict] = []
    checked = 0

    # --- quota_order: same multiset, different dict insertion / UTF-8 names ---
    base = {"zebra": 2, "apple": 3, "mango": 1}
    variants = [
        dict(base),
        dict(reversed(list(base.items()))),
        OrderedDict([("mango", 1), ("zebra", 2), ("apple", 3)]),
        OrderedDict([("apple", 3), ("mango", 1), ("zebra", 2)]),
        # UTF-8 names that sort differently as unicode vs naive
        {"café": 2, "cafe": 3, "caffè": 1},
        {"caffè": 1, "café": 2, "cafe": 3},
        {"cafe": 3, "caffè": 1, "café": 2},
    ]

    # For latin names: expect identical category order (utf-8 sort) and identical codes/digest
    latin_results = []
    for counts in variants[:4]:
        r = quota_order(counts)
        latin_results.append(
            {
                "input_keys": list(counts.keys()),
                "categories": list(r.categories),
                "counts": list(r.counts),
                "order_codes": list(r.order_codes),
                "digest": r.order_sha256,
                "B": str(r.max_discrepancy),
            }
        )
        checked += 1

    ref = latin_results[0]
    for row in latin_results[1:]:
        if (
            row["categories"] != ref["categories"]
            or row["order_codes"] != ref["order_codes"]
            or row["digest"] != ref["digest"]
            or row["B"] != ref["B"]
        ):
            findings.append(
                {
                    "kind": "quota_order_dict_order_dependent",
                    "reference": ref,
                    "divergent": row,
                }
            )

    utf_results = []
    for counts in variants[4:]:
        r = quota_order(counts)
        utf_results.append(
            {
                "input_keys": list(counts.keys()),
                "categories": list(r.categories),
                "order_codes": list(r.order_codes),
                "digest": r.order_sha256,
                "B": str(r.max_discrepancy),
            }
        )
        checked += 1
    uref = utf_results[0]
    for row in utf_results[1:]:
        if (
            row["categories"] != uref["categories"]
            or row["order_codes"] != uref["order_codes"]
            or row["digest"] != uref["digest"]
        ):
            findings.append(
                {
                    "kind": "quota_order_utf8_order_dependent",
                    "reference": uref,
                    "divergent": row,
                    "note": "If categories sort by UTF-8 bytes, insertion order must not matter",
                }
            )

    # Sequence form with same numeric counts should match mapping after utf8 name sort remap
    seq = quota_order([3, 1, 2])  # categories "0","1","2"
    checked += 1

    # --- solve_constrained_quota determinism ---
    def constrained(counts_map):
        cats = sorted(counts_map.keys(), key=lambda s: s.encode("utf-8"))
        # Use first two categories with positive count for a block/pin if possible
        positive = [c for c in cats if counts_map[c] > 0]
        blocks = ()
        prefix = ()
        prec = ()
        if len(positive) >= 2 and counts_map[positive[0]] >= 1 and counts_map[positive[1]] >= 1:
            blocks = (
                FixedOccurrenceBlock(
                    "b",
                    (
                        OccurrenceRef(positive[0], 1),
                        OccurrenceRef(positive[1], 1),
                    ),
                ),
            )
            if counts_map[positive[0]] >= 2:
                prec = (
                    OccurrencePrecedence(
                        "e",
                        OccurrenceRef(positive[0], 1),
                        OccurrenceRef(positive[0], 2),
                    ),
                )
        return CategoricalConstraintProblem(
            counts=counts_map,
            fixed_blocks=blocks,
            pinned_prefix=prefix,
            precedence=prec,
        )

    cmaps = [
        {"x": 2, "y": 2, "z": 1},
        {"z": 1, "x": 2, "y": 2},
        {"y": 2, "z": 1, "x": 2},
    ]
    crows = []
    for cmap in cmaps:
        r = solve_constrained_quota(constrained(cmap))
        crows.append(
            {
                "input_keys": list(cmap.keys()),
                "categories": list(r.categories),
                "order_codes": list(r.order_codes),
                "digest": r.order_sha256,
                "L": str(r.lower_bound),
                "U": str(r.max_discrepancy),
            }
        )
        checked += 1
    cref = crows[0]
    for row in crows[1:]:
        if (
            row["categories"] != cref["categories"]
            or row["order_codes"] != cref["order_codes"]
            or row["digest"] != cref["digest"]
        ):
            findings.append(
                {
                    "kind": "constrained_dict_order_dependent",
                    "reference": cref,
                    "divergent": row,
                }
            )

    payload = {
        "task": 5,
        "elapsed_s": time.perf_counter() - t0,
        "checked": checked,
        "latin_results": latin_results,
        "utf8_results": utf_results,
        "sequence_example": {
            "counts": [3, 1, 2],
            "categories": list(seq.categories),
            "order_codes": list(seq.order_codes),
            "digest": seq.order_sha256,
        },
        "constrained_results": crows,
        "findings": findings,
        "verdict_hint": (
            "REFUTED"
            if findings
            else f"HOLDS ({checked} instances); output independent of dict insertion order"
        ),
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({k: payload[k] for k in payload if k not in {"latin_results", "utf8_results", "constrained_results", "findings"}}, indent=2))
    print(f"findings: {len(findings)}  wrote {OUT}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
