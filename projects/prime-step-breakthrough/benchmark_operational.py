#!/usr/bin/env python3
"""Frozen one-million-item operational prefix-balance benchmark.

The default mode launches a fresh worker process so wall time includes import
and construction cost.  The worker consumes every emitted position, checks its
occurrence window and exact prefix discrepancy independently, computes the
canonical digest, and reports OS peak RSS.  No production verification helper
is used as ground truth.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
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
MAX_RSS_BYTES = 134_217_728
COUNTS: dict[str, int] = {
    "alpha": 100_003,
    "beta": 200_009,
    "delta": 399_977,
    "gamma": 300_011,
}
TOTAL_ITEMS = 1_000_000
DIGEST_ENCODING = "uint32-big-endian-category-code-v1"
UNSUPPORTED_TRUE_CLAIMS = {
    "clinical_validity",
    "monetary_savings",
    "production_ready",
    "star_discrepancy_certified",
    "tail_risk_accuracy",
}


def _peak_rss_bytes() -> int:
    raw = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return raw if sys.platform == "darwin" else raw * 1024


def _integrality_lower_bound(counts: list[int]) -> Fraction:
    total = sum(counts)
    values = []
    for count in counts:
        if count:
            denominator = total // math.gcd(count, total)
            values.append(Fraction(denominator // 2, denominator))
    return max(values, default=Fraction(0))


def unsupported_claim_paths(payload: Any, prefix: str = "") -> list[str]:
    """Find forbidden truthy domain self-certifications in nested metadata."""

    found: list[str] = []
    if isinstance(payload, Mapping):
        for key, value in payload.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if key in UNSUPPORTED_TRUE_CLAIMS and bool(value):
                found.append(path)
            found.extend(unsupported_claim_paths(value, path))
    elif isinstance(payload, (list, tuple)):
        for index, value in enumerate(payload):
            found.extend(unsupported_claim_paths(value, f"{prefix}[{index}]"))
    return found


def _consume_result(result: Any) -> dict[str, Any]:
    categories = tuple(result.categories)
    errors: list[str] = []
    if set(categories) != set(COUNTS):
        errors.append("result category names do not match frozen inventory")
    expected = [COUNTS.get(category, -1) for category in categories]
    if tuple(expected) != tuple(result.counts):
        errors.append("result counts do not match category names")
    total = sum(max(count, 0) for count in expected)
    seen = [0] * len(categories)
    digest = hashlib.sha256()
    peak_numerator = 0
    accumulated_numerator = 0
    emitted = 0
    for emitted, code in enumerate(result.order_codes, 1):
        if isinstance(code, bool) or not isinstance(code, int):
            errors.append(f"position {emitted} has a non-integer code")
            continue
        if not 0 <= code < len(categories):
            errors.append(f"position {emitted} has out-of-range code {code}")
            continue
        digest.update(struct.pack(">I", code))
        seen[code] += 1
        occurrence = seen[code]
        count = expected[code]
        if occurrence > count:
            errors.append(f"category {code} exceeds inventory")
            continue
        release = ((occurrence - 1) * total) // count + 1
        deadline = (occurrence * total + count - 1) // count
        if not release <= emitted <= deadline:
            errors.append(
                f"category {code} occurrence {occurrence} at {emitted} "
                f"outside [{release},{deadline}]"
            )
        discrepancy_numerator = max(
            abs(total * value - emitted * inventory)
            for value, inventory in zip(seen, expected)
        )
        peak_numerator = max(peak_numerator, discrepancy_numerator)
        accumulated_numerator += discrepancy_numerator
    if emitted != TOTAL_ITEMS:
        errors.append(f"emitted {emitted} positions, expected {TOTAL_ITEMS}")
    if seen != expected:
        errors.append(f"emitted counts {seen!r} != expected {expected!r}")
    canonical_digest = digest.hexdigest()
    peak = Fraction(peak_numerator, total or 1)
    accumulated = Fraction(accumulated_numerator, total or 1)
    if result.order_sha256 != canonical_digest:
        errors.append("result digest differs from independently consumed bytes")
    if result.digest_encoding != DIGEST_ENCODING:
        errors.append("digest encoding is not the frozen encoding")
    if result.max_discrepancy != peak:
        errors.append("reported maximum discrepancy differs from recomputation")
    lower = _integrality_lower_bound(expected)
    if result.lower_bound != lower:
        errors.append("reported categorical lower bound differs from recomputation")
    scope_tokens = set(
        result.guarantee_scope.lower().replace("_", " ").replace("-", " ").split()
    )
    if not {"unconstrained", "categorical"} <= scope_tokens:
        errors.append("million result has the wrong guarantee scope")
    if result.strict_factor != 3:
        errors.append("million result is missing the strict factor-three label")
    unsupported = unsupported_claim_paths(result.explanation)
    if unsupported:
        errors.append("unsupported domain claims: " + ", ".join(unsupported))
    return {
        "output_positions": emitted,
        "order_sha256": canonical_digest,
        "digest_encoding": DIGEST_ENCODING,
        "emitted_counts": seen,
        "max_discrepancy": str(peak),
        "accumulated_discrepancy": str(accumulated),
        "lower_bound": str(lower),
        "validation_errors": errors[:20],
    }


def worker_evidence() -> dict[str, Any]:
    if str(SRC) not in sys.path:
        sys.path.insert(0, str(SRC))
    from coprimebatch.prefix_balance import quota_order

    started = time.perf_counter()
    result = quota_order(COUNTS)
    consumed = _consume_result(result)
    internal_elapsed = time.perf_counter() - started
    return {
        "schema_version": SCHEMA_VERSION,
        "workload": {
            "name": "categorical_1m_4_unequal_v1",
            "counts": COUNTS,
            "total_items": TOTAL_ITEMS,
            "positive_categories": 4,
        },
        "result": consumed,
        "performance": {
            "worker_seconds": internal_elapsed,
            "wall_seconds": None,
            "peak_rss_bytes": _peak_rss_bytes(),
            "measurement": "fresh-subprocess OS wall and getrusage(RUSAGE_SELF)",
        },
        "thresholds": {
            "wall_seconds_strict_max": MAX_SECONDS,
            "peak_rss_bytes_max": MAX_RSS_BYTES,
        },
        "gates": {
            "output_complete": consumed["output_positions"] == TOTAL_ITEMS,
            "independent_validation": not consumed["validation_errors"],
            "wall_time": None,
            "peak_rss": _peak_rss_bytes() <= MAX_RSS_BYTES,
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
            f"benchmark worker exceeded the hard {MAX_SECONDS:g}s timeout"
        ) from exc
    wall = time.perf_counter() - started
    if completed.returncode:
        raise RuntimeError(
            f"benchmark worker exited {completed.returncode}: {completed.stderr.strip()}"
        )
    try:
        evidence = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"benchmark worker emitted invalid JSON: {exc}") from exc
    evidence["performance"]["wall_seconds"] = wall
    evidence["gates"]["wall_time"] = wall < MAX_SECONDS
    return evidence


def validate_evidence(evidence: Mapping[str, Any]) -> list[str]:
    """Validate the frozen artifact schema without trusting its pass booleans."""

    errors: list[str] = []
    try:
        if evidence["schema_version"] != SCHEMA_VERSION:
            errors.append("schema_version mismatch")
        workload = evidence["workload"]
        if workload != {
            "name": "categorical_1m_4_unequal_v1",
            "counts": COUNTS,
            "total_items": TOTAL_ITEMS,
            "positive_categories": 4,
        }:
            errors.append("frozen workload mismatch")
        thresholds = evidence["thresholds"]
        if thresholds != {
            "wall_seconds_strict_max": MAX_SECONDS,
            "peak_rss_bytes_max": MAX_RSS_BYTES,
        }:
            errors.append("frozen thresholds were changed")
        result = evidence["result"]
        if result["output_positions"] != TOTAL_ITEMS:
            errors.append("output position count mismatch")
        if result["emitted_counts"] != [COUNTS[name] for name in sorted(COUNTS)]:
            errors.append("emitted counts mismatch")
        if not isinstance(result["order_sha256"], str) or len(result["order_sha256"]) != 64:
            errors.append("canonical digest is malformed")
        if result["digest_encoding"] != DIGEST_ENCODING:
            errors.append("digest encoding mismatch")
        if result["validation_errors"]:
            errors.append("independent result validation failed")
        peak = Fraction(result["max_discrepancy"])
        lower = Fraction(result["lower_bound"])
        if not Fraction(0) <= peak < 1:
            errors.append("maximum discrepancy is outside theorem range")
        if lower != _integrality_lower_bound([COUNTS[name] for name in sorted(COUNTS)]):
            errors.append("integrality lower bound mismatch")
        performance = evidence["performance"]
        wall = performance["wall_seconds"]
        rss = performance["peak_rss_bytes"]
        if isinstance(wall, bool) or not isinstance(wall, (int, float)) or not 0 <= wall < MAX_SECONDS:
            errors.append("strict wall-time gate failed")
        if isinstance(rss, bool) or not isinstance(rss, int) or not 0 < rss <= MAX_RSS_BYTES:
            errors.append("peak-RSS gate failed")
        expected_gates = {
            "output_complete": result["output_positions"] == TOTAL_ITEMS,
            "independent_validation": not result["validation_errors"],
            "wall_time": isinstance(wall, (int, float)) and not isinstance(wall, bool) and wall < MAX_SECONDS,
            "peak_rss": isinstance(rss, int) and not isinstance(rss, bool) and rss <= MAX_RSS_BYTES,
        }
        if evidence["gates"] != expected_gates:
            errors.append("gate booleans are forged or inconsistent")
    except (KeyError, TypeError, ValueError, ZeroDivisionError) as exc:
        errors.append(f"invalid artifact schema: {exc}")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--output", type=Path, help="write evidence to this path")
    args = parser.parse_args(argv)
    evidence = worker_evidence() if args.worker else run_subprocess_benchmark()
    errors = [] if args.worker else validate_evidence(evidence)
    evidence["all_gates_passed"] = not errors
    if errors:
        evidence["artifact_errors"] = errors
    rendered = json.dumps(evidence, indent=2, sort_keys=True)
    if args.output:
        args.output.write_text(rendered + "\n")
    else:
        print(rendered)
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
