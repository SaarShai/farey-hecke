#!/usr/bin/env python3
"""Independent realprecision=30 cross-check for A4 weighted chunks."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from decimal import Decimal, getcontext
import json
from pathlib import Path

from zero_sum_v2_driver import (
    DEFAULT_CHECKPOINT_DIR,
    DEFAULT_ZEROS,
    REALPRECISION,
    RESIDUAL_THRESHOLD,
    ROOT,
    local_path,
    load_checkpoints,
    run_gp,
    sha256_file,
    write_json_atomic,
)


getcontext().prec = 80
DEFAULT_OUTPUT = DEFAULT_CHECKPOINT_DIR / "backend_crosscheck.json"


def dec(value: str) -> Decimal:
    return Decimal(value.replace(" E", "e").replace(" ", ""))


def run(args: argparse.Namespace) -> int:
    zeros = args.zeros.resolve()
    checkpoint_dir = local_path(args.checkpoint_dir)
    output = local_path(args.output)
    source_sha = sha256_file(zeros)
    records = load_checkpoints(checkpoint_dir, zeros, source_sha, args.nmax)
    result = json.loads(output.read_text()) if output.exists() else {
        "schema_version": 1,
        "zeros_path": str(zeros),
        "zeros_sha256": source_sha,
        "low_precision_digits": REALPRECISION,
        "high_precision_digits": args.precision,
        "strict_residual_threshold": RESIDUAL_THRESHOLD,
        "chunks": [],
    }
    by_hi = {int(row["hi"]): row for row in result.get("chunks", [])}
    for hi in sorted(records):
        if hi in by_hi:
            continue
        low = records[hi]
        lo = int(low["lo"])
        high = run_gp(zeros, lo, hi, args.chunk_timeout, args.precision)
        row = {
            "lo": lo,
            "hi": hi,
            "low_precision_chunk_sum_decimal": low["positive_chunk_sum_decimal"],
            "high_precision_chunk_sum_decimal": high["positive_chunk_sum_decimal"],
            "absolute_chunk_sum_difference_decimal": str(abs(dec(low["positive_chunk_sum_decimal"]) - dec(high["positive_chunk_sum_decimal"]))),
            "low_precision_max_residual_decimal": low["max_abs_zeta_residual_decimal"],
            "high_precision_max_residual_decimal": high["max_abs_zeta_residual_decimal"],
            "high_precision_failure_count": int(high["failure_count"]),
            "high_precision_first_failure_index": int(high["first_failure_index"]),
        }
        by_hi[hi] = row
        result["chunks"] = [by_hi[key] for key in sorted(by_hi)]
        result["created_or_updated_utc"] = datetime.now(timezone.utc).isoformat()
        write_json_atomic(output, result)
        print(json.dumps({"chunk": f"{lo}-{hi}", "abs_difference": row["absolute_chunk_sum_difference_decimal"], "max_residual": row["high_precision_max_residual_decimal"]}, sort_keys=True), flush=True)
    result["status"] = "completed" if max(by_hi, default=0) >= args.nmax else "partial"
    result["max_absolute_chunk_sum_difference_decimal"] = str(max((dec(row["absolute_chunk_sum_difference_decimal"]) for row in by_hi.values()), default=Decimal(0)))
    result["sum_absolute_chunk_sum_difference_decimal"] = str(sum((dec(row["absolute_chunk_sum_difference_decimal"]) for row in by_hi.values()), Decimal(0)))
    write_json_atomic(output, result)
    print(json.dumps(result, indent=2))
    return 0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--zeros", type=Path, default=DEFAULT_ZEROS)
    parser.add_argument("--nmax", type=int, default=10000)
    parser.add_argument("--precision", type=int, default=30)
    parser.add_argument("--checkpoint-dir", type=Path, default=DEFAULT_CHECKPOINT_DIR)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--chunk-timeout", type=int, default=1200)
    args = parser.parse_args()
    raise SystemExit(run(args))


if __name__ == "__main__":
    main()
