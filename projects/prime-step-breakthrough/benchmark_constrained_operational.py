#!/usr/bin/env python3
"""Frozen million-item sparse-constrained categorical benchmark.

The worker constructs one packed ordering while retaining only sparse
occurrence constraints.  This verifier independently streams every output,
reconstructs occurrence identities, recomputes the exact primary and
accumulated objectives, checks every declared constraint, and recomputes the
canonical digest.  Quota windows are deliberately not checked: the frozen
constraints contradict the unconstrained EDF word.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import resource
import struct
import subprocess
import sys
import time
from fractions import Fraction
from pathlib import Path
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
SCHEMA_VERSION = 1
MAX_SECONDS = 30.0
# The packed million-word run is ~45 MiB on the release host.  128 MiB leaves
# substantial interpreter/platform headroom while rejecting accidental
# materialization of a million occurrence objects in addition to the packed
# array.
MAX_RSS_BYTES = 134_217_728
DIGEST_ENCODING = "uint32-big-endian-category-code-v1"
COUNTS: dict[str, int] = {
    "alpha": 100_003,
    "beta": 200_009,
    "delta": 399_977,
    "gamma": 300_011,
}
TOTAL_ITEMS = 1_000_000
FROZEN_CONSTRAINTS = {
    "fixed_blocks": [
        {
            "block_id": "joint-block-001",
            "occurrences": [
                {"category": "alpha", "occurrence": 1001},
                {"category": "alpha", "occurrence": 1002},
                {"category": "delta", "occurrence": 1001},
                {"category": "beta", "occurrence": 2001},
                {"category": "gamma", "occurrence": 3001},
            ],
        }
    ],
    "pinned_prefix": [
        {"category": "alpha", "occurrence": 1},
        {"category": "beta", "occurrence": 1},
        {"category": "delta", "occurrence": 1},
        {"category": "gamma", "occurrence": 1},
    ],
    "pinned_suffix": [
        {"category": "gamma", "occurrence": 300_011},
        {"category": "delta", "occurrence": 399_977},
    ],
    "precedence": [
        {
            "edge_id": "rare-before-dense-001",
            "before": {"category": "alpha", "occurrence": 1000},
            "after": {"category": "delta", "occurrence": 1000},
        }
    ],
}
CONSTRAINTS = FROZEN_CONSTRAINTS
FROZEN_CONSTRAINTS_SHA256 = (
    "85b5161d9c938f437a3d24315d271abf5cdf8bc14eba1e972a410e006dd1ae1a"
)
CONSTRAINTS_SHA256 = FROZEN_CONSTRAINTS_SHA256
FROZEN_ORDER_SHA256 = (
    "3194a7661d0d90f6115bba41cfed1c506fd8f9442c0f54c0a8069ff90662c675"
)
FROZEN_UNCONSTRAINED_ORDER_SHA256 = (
    "c92afcfccfc6bd10a920b753c5d9c5cd6f929101ecc3f5f40fdbe937db5c3ebd"
)
FROZEN_RESULT_FIELDS = {
    "max_discrepancy": "360167777/200000",
    "accumulated_discrepancy": "455298078991/62500",
    "lower_bound": "1799839/1000",
    "additive_gap": "199977/200000",
    "ratio_bound": "360167777/359967800",
}


def _constraint_sha256(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _peak_rss_bytes() -> int:
    raw = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return raw if sys.platform == "darwin" else raw * 1024


def _refs(rows: list[dict[str, Any]]) -> list[tuple[str, int]]:
    return [(row["category"], row["occurrence"]) for row in rows]


def _consume_result(result: Any, baseline_digest: str) -> dict[str, Any]:
    categories = tuple(result.categories)
    expected = [COUNTS[name] for name in categories]
    errors: list[str] = []
    if categories != tuple(sorted(COUNTS, key=lambda name: name.encode("utf-8"))):
        errors.append("categories are not in canonical UTF-8 order")
    if tuple(result.counts) != tuple(expected):
        errors.append("reported inventory differs from frozen counts")

    prefix = _refs(CONSTRAINTS["pinned_prefix"])
    suffix = _refs(CONSTRAINTS["pinned_suffix"])
    block = _refs(CONSTRAINTS["fixed_blocks"][0]["occurrences"])
    edge = CONSTRAINTS["precedence"][0]
    watched = set(prefix + suffix + block)
    watched.add((edge["before"]["category"], edge["before"]["occurrence"]))
    watched.add((edge["after"]["category"], edge["after"]["occurrence"]))

    seen = [0] * len(categories)
    positions: dict[tuple[str, int], int] = {}
    first_tokens: list[tuple[str, int]] = []
    last_tokens: list[tuple[str, int]] = []
    digest = hashlib.sha256()
    peak_numerator = 0
    accumulated_numerator = 0
    emitted = 0
    for emitted, code in enumerate(result.order_codes, 1):
        if isinstance(code, bool) or not isinstance(code, int) or not 0 <= code < len(categories):
            errors.append(f"invalid category code at position {emitted}")
            continue
        digest.update(struct.pack(">I", code))
        seen[code] += 1
        token = (categories[code], seen[code])
        if emitted <= len(prefix):
            first_tokens.append(token)
        last_tokens.append(token)
        if len(last_tokens) > len(suffix):
            del last_tokens[0]
        if token in watched:
            positions[token] = emitted
        numerator = max(
            abs(TOTAL_ITEMS * occurrence - emitted * count)
            for occurrence, count in zip(seen, expected)
        )
        peak_numerator = max(peak_numerator, numerator)
        accumulated_numerator += numerator

    if emitted != TOTAL_ITEMS or seen != expected:
        errors.append("packed output does not consume the frozen inventory exactly")
    if first_tokens != prefix:
        errors.append("exact pinned prefix was not preserved")
    if last_tokens != suffix:
        errors.append("exact pinned suffix was not preserved")
    try:
        block_positions = [positions[token] for token in block]
        if block_positions != list(range(block_positions[0], block_positions[0] + len(block))):
            errors.append("fixed occurrence block is not contiguous and ordered")
        before = (edge["before"]["category"], edge["before"]["occurrence"])
        after = (edge["after"]["category"], edge["after"]["occurrence"])
        if positions[before] >= positions[after]:
            errors.append("precedence occurrence order is violated")
    except KeyError as exc:
        errors.append(f"watched constrained occurrence is missing: {exc}")

    canonical_digest = digest.hexdigest()
    peak = Fraction(peak_numerator, TOTAL_ITEMS)
    accumulated = Fraction(accumulated_numerator, TOTAL_ITEMS)
    if result.order_sha256 != canonical_digest:
        errors.append("reported order digest differs from streamed bytes")
    if result.max_discrepancy != peak:
        errors.append("reported U differs from independent exact recomputation")
    if result.accumulated_discrepancy != accumulated:
        errors.append("reported Q differs from independent exact recomputation")
    if not Fraction(0) <= result.lower_bound <= peak:
        errors.append("reported constrained lower bound is outside [0,U]")
    if result.strict_factor is not None:
        errors.append("constrained result inherited a forbidden factor label")
    if result.guarantee_scope != "constrained_categorical_a_posteriori":
        errors.append("constrained guarantee scope mismatch")
    if "interleavings" not in result.comparison_set or "occurrence" not in result.comparison_set:
        errors.append("comparison set does not identify fixed occurrence queues")
    if canonical_digest == baseline_digest:
        errors.append("constrained and unconstrained orders unexpectedly match")

    return {
        "output_positions": emitted,
        "order_sha256": canonical_digest,
        "unconstrained_order_sha256": baseline_digest,
        "digest_encoding": DIGEST_ENCODING,
        "constraint_sha256": CONSTRAINTS_SHA256,
        "emitted_counts": seen,
        "max_discrepancy": str(peak),
        "accumulated_discrepancy": str(accumulated),
        "lower_bound": str(result.lower_bound),
        "additive_gap": str(peak - result.lower_bound),
        "ratio_bound": str(peak / result.lower_bound) if result.lower_bound else None,
        "verified_constraints": {
            "fixed_blocks": 1,
            "pinned_prefix_items": len(prefix),
            "pinned_suffix_items": len(suffix),
            "precedence_edges": 1,
        },
        "validation_errors": errors[:20],
    }


def worker_evidence() -> dict[str, Any]:
    if str(SRC) not in sys.path:
        sys.path.insert(0, str(SRC))
    from coprimebatch.prefix_balance import (
        CategoricalConstraintProblem,
        FixedOccurrenceBlock,
        OccurrencePrecedence,
        OccurrenceRef,
        quota_order,
        solve_constrained_quota,
    )

    def ref(row: Mapping[str, Any]) -> Any:
        return OccurrenceRef(str(row["category"]), int(row["occurrence"]))

    problem = CategoricalConstraintProblem(
        counts=COUNTS,
        fixed_blocks=tuple(
            FixedOccurrenceBlock(
                str(block["block_id"]),
                tuple(ref(row) for row in block["occurrences"]),
            )
            for block in CONSTRAINTS["fixed_blocks"]
        ),
        pinned_prefix=tuple(ref(row) for row in CONSTRAINTS["pinned_prefix"]),
        pinned_suffix=tuple(ref(row) for row in CONSTRAINTS["pinned_suffix"]),
        precedence=tuple(
            OccurrencePrecedence(
                str(edge["edge_id"]), ref(edge["before"]), ref(edge["after"])
            )
            for edge in CONSTRAINTS["precedence"]
        ),
    )
    started = time.perf_counter()
    result = solve_constrained_quota(problem)
    baseline_digest = quota_order(COUNTS).order_sha256
    consumed = _consume_result(result, baseline_digest)
    elapsed = time.perf_counter() - started
    rss = _peak_rss_bytes()
    return {
        "schema_version": SCHEMA_VERSION,
        "workload": {
            "name": "categorical_1m_sparse_constraints_v1",
            "counts": COUNTS,
            "total_items": TOTAL_ITEMS,
            "constraints": CONSTRAINTS,
            "constraint_sha256": CONSTRAINTS_SHA256,
        },
        "result": consumed,
        "performance": {
            "worker_seconds": elapsed,
            "wall_seconds": None,
            "peak_rss_bytes": rss,
            "measurement": "fresh-subprocess wall and getrusage(RUSAGE_SELF)",
        },
        "thresholds": {
            "wall_seconds_strict_max": MAX_SECONDS,
            "peak_rss_bytes_max": MAX_RSS_BYTES,
        },
        "gates": {
            "output_complete": consumed["output_positions"] == TOTAL_ITEMS,
            "independent_validation": not consumed["validation_errors"],
            "all_constraint_classes": consumed["verified_constraints"]
            == {
                "fixed_blocks": 1,
                "pinned_prefix_items": 4,
                "pinned_suffix_items": 2,
                "precedence_edges": 1,
            },
            "wall_time": None,
            "peak_rss": rss <= MAX_RSS_BYTES,
        },
    }


def run_subprocess_benchmark() -> dict[str, Any]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    started = time.perf_counter()
    try:
        completed = subprocess.run(
            [sys.executable, str(Path(__file__).resolve()), "--worker"],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
            timeout=MAX_SECONDS,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(
            f"constrained benchmark worker exceeded the hard {MAX_SECONDS:g}s timeout"
        ) from exc
    wall = time.perf_counter() - started
    if completed.returncode:
        raise RuntimeError(
            f"constrained benchmark worker exited {completed.returncode}: {completed.stderr.strip()}"
        )
    evidence = json.loads(completed.stdout)
    evidence["performance"]["wall_seconds"] = wall
    evidence["gates"]["wall_time"] = wall < MAX_SECONDS
    return evidence


def validate_evidence(evidence: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if _constraint_sha256(FROZEN_CONSTRAINTS) != FROZEN_CONSTRAINTS_SHA256:
            errors.append("source frozen constraint fixture differs from its literal digest")
        workload = evidence["workload"]
        if evidence["schema_version"] != SCHEMA_VERSION:
            errors.append("schema_version mismatch")
        if workload["name"] != "categorical_1m_sparse_constraints_v1":
            errors.append("workload name mismatch")
        if workload["counts"] != COUNTS or workload["total_items"] != TOTAL_ITEMS:
            errors.append("frozen inventory mismatch")
        if workload["constraints"] != FROZEN_CONSTRAINTS:
            errors.append("frozen constraints were changed")
        if _constraint_sha256(workload["constraints"]) != FROZEN_CONSTRAINTS_SHA256:
            errors.append("frozen constraint payload digest mismatch")
        if workload["constraint_sha256"] != FROZEN_CONSTRAINTS_SHA256:
            errors.append("constraint digest mismatch")
        if evidence["thresholds"] != {
            "wall_seconds_strict_max": MAX_SECONDS,
            "peak_rss_bytes_max": MAX_RSS_BYTES,
        }:
            errors.append("frozen thresholds were changed")
        result = evidence["result"]
        if result["output_positions"] != TOTAL_ITEMS:
            errors.append("output position count mismatch")
        if result["emitted_counts"] != [COUNTS[name] for name in sorted(COUNTS)]:
            errors.append("emitted inventory mismatch")
        if result["constraint_sha256"] != FROZEN_CONSTRAINTS_SHA256:
            errors.append("result constraint digest mismatch")
        if result["order_sha256"] != FROZEN_ORDER_SHA256:
            errors.append("frozen constrained order digest mismatch")
        if result["unconstrained_order_sha256"] != FROZEN_UNCONSTRAINED_ORDER_SHA256:
            errors.append("frozen unconstrained order digest mismatch")
        for field, expected in FROZEN_RESULT_FIELDS.items():
            if result[field] != expected:
                errors.append(f"frozen result field {field} mismatch")
        if result["validation_errors"]:
            errors.append("independent result validation failed")
        if result["order_sha256"] == result["unconstrained_order_sha256"]:
            errors.append("constraint fixture did not alter the order")
        wall = evidence["performance"]["wall_seconds"]
        rss = evidence["performance"]["peak_rss_bytes"]
        wall_ok = isinstance(wall, (int, float)) and not isinstance(wall, bool) and 0 <= wall < MAX_SECONDS
        rss_ok = isinstance(rss, int) and not isinstance(rss, bool) and 0 < rss <= MAX_RSS_BYTES
        expected_gates = {
            "output_complete": result["output_positions"] == TOTAL_ITEMS,
            "independent_validation": result["validation_errors"] == [],
            "all_constraint_classes": result["verified_constraints"]
            == {
                "fixed_blocks": 1,
                "pinned_prefix_items": 4,
                "pinned_suffix_items": 2,
                "precedence_edges": 1,
            },
            "wall_time": wall_ok,
            "peak_rss": rss_ok,
        }
        if evidence["gates"] != expected_gates:
            errors.append("reported gates are inconsistent with measurements")
    except (KeyError, TypeError, ValueError, ZeroDivisionError) as exc:
        errors.append(f"invalid constrained benchmark artifact: {exc}")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    evidence = worker_evidence() if args.worker else run_subprocess_benchmark()
    errors = [] if args.worker else validate_evidence(evidence)
    evidence["all_gates_passed"] = not errors
    if errors:
        evidence["artifact_errors"] = errors
    rendered = json.dumps(evidence, indent=2, sort_keys=True)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
