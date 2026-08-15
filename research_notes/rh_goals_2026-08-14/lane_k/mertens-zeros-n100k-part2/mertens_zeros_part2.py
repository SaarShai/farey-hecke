#!/usr/bin/env python3
"""Refine one independent chunk of the Odlyzko 100k-zero table.

The source table is bundled next to this script by the Kaggle kernel bundle.
The five copied scripts are intentionally identical; the part number is read
from the filename so each private kernel has a fixed, auditable range.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import time
from pathlib import Path

import mpmath as mp


mp.mp.dps = 25
RESIDUAL_GATE = mp.mpf("1e-15")
RANGES = {
    1: (10_000, 27_999),
    2: (28_000, 45_999),
    3: (46_000, 63_999),
    4: (64_000, 81_999),
    # The requested inclusive endpoint makes this chunk 18,001 rows.
    5: (82_000, 100_000),
}


def part_number() -> int:
    # Kaggle renames the script to /kaggle/src/script.py, so the part is fixed here.
    return 2


def locate_table() -> Path:
    direct = [
        Path.cwd() / "zeros1.txt",
        Path(__file__).resolve().parent / "zeros1.txt",
    ]
    for candidate in direct:
        if candidate.is_file():
            return candidate
    kaggle_input = Path("/kaggle/input")
    if kaggle_input.is_dir():
        matches = sorted(kaggle_input.rglob("zeros1.txt"))
        if matches:
            return matches[0]
    raise FileNotFoundError("zeros1.txt was not found in the kernel bundle")


def refine(seed: str) -> tuple[mp.mpf, mp.mpf, mp.mpf]:
    seed_value = mp.mpf(seed)

    def zeta_on_line(t) -> mp.mpc:
        # t may go complex under the secant iteration; build s = 1/2 + i*t
        # with complex arithmetic instead of the mpc(str, t) constructor.
        return mp.zeta(mp.mpf("0.5") + mp.mpc(0, 1) * t)

    # Two real secant seeds keep the search on the ordinate while evaluating
    # the requested complex zeta function directly.
    gamma = mp.findroot(
        zeta_on_line,
        (seed_value - mp.mpf("0.03"), seed_value + mp.mpf("0.03")),
        solver="secant",
        tol=mp.mpf("1e-20"),
        maxsteps=40,
    )
    if isinstance(gamma, mp.mpc):
        if abs(mp.im(gamma)) > mp.mpf("1e-12"):
            raise RuntimeError(f"non-real refined ordinate from seed {seed}")
        gamma = mp.re(gamma)
    residual = abs(zeta_on_line(gamma))
    if not residual < RESIDUAL_GATE:
        raise RuntimeError(
            f"residual gate failed for seed {seed}: {mp.nstr(residual, 12)}"
        )
    zeta_prime = mp.zeta(mp.mpc("0.5", gamma), derivative=1)
    return gamma, abs(zeta_prime) ** 2, residual


def append_rows(path: Path, rows: list[tuple[str, str, str, str]]) -> None:
    new_file = not path.exists()
    with path.open("a", newline="") as handle:
        writer = csv.writer(handle)
        if new_file:
            writer.writerow(
                ["index", "gamma_refined", "abs_zeta_prime_sq", "residual"]
            )
        writer.writerows(rows)
        handle.flush()


def nstr(value: mp.mpf) -> str:
    return mp.nstr(value, 30)


def main() -> int:
    part = part_number()
    first, last = RANGES[part]
    table = locate_table()
    seeds = [line.strip() for line in table.read_text().splitlines() if line.strip()]
    if len(seeds) < last:
        raise RuntimeError(f"seed table has {len(seeds)} rows, need {last}")

    out_dir = Path("/kaggle/working")
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / f"mertens_zeros_part{part}.csv"
    stats_path = out_dir / f"mertens_zeros_part{part}.json"
    start_time = time.monotonic()
    pending: list[tuple[str, str, str, str]] = []
    residuals: list[mp.mpf] = []
    completed = 0

    for index in range(first, last + 1):
        gamma, derivative_sq, residual = refine(seeds[index - 1])
        pending.append((str(index), nstr(gamma), nstr(derivative_sq), nstr(residual)))
        residuals.append(residual)
        completed += 1
        if len(pending) == 500 or index == last:
            append_rows(csv_path, pending)
            pending.clear()
            print(
                f"part={part} index={index} completed={completed}/{last-first+1} "
                f"residual={nstr(residual)} elapsed={time.monotonic()-start_time:.1f}s",
                flush=True,
            )

    stats = {
        "part": part,
        "index_first": first,
        "index_last": last,
        "rows": completed,
        "mpmath_dps": 25,
        "method": "mp.findroot(secant) on zeta(1/2+i*t); mp.zeta derivative=1",
        "residual_gate": "residual < 1e-15",
        "max_residual": nstr(max(residuals)),
        "seed_table": str(table),
        "seed_table_sha256": hashlib.sha256(table.read_bytes()).hexdigest(),
        "csv": str(csv_path),
        "wall_seconds": time.monotonic() - start_time,
    }
    stats_path.write_text(json.dumps(stats, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
