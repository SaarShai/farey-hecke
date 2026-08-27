#!/usr/bin/env python3
"""Deterministic verification gates for the spectral-transient package."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from pathlib import Path


EXPECTED_CURVE_SHA256 = "57957bdb3ce3243272c3d4b8e9ffe7dfb734b759f48b63becf7ae6f924e1caab"
MODULI = (7, 8, 11, 19, 23)


def rows(path: Path) -> list[dict[str, str]]:
    with path.open() as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def digest(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            result.update(block)
    return result.hexdigest()


def as_float(text: str) -> float:
    return float(text.replace(" ", ""))


def verify(curve: Path, prior_n8: Path, output: Path) -> None:
    assert digest(curve) == EXPECTED_CURVE_SHA256, "authoritative curve hash changed"

    checks = rows(output / "zero_crosscheck.tsv")
    assert len(checks) == 55, f"expected 55 nonprincipal characters, got {len(checks)}"
    assert all(row["status"] == "PASS" for row in checks), "a zero check failed"
    assert max(as_float(row["max_abs_difference"]) for row in checks) < 1e-28
    assert max(as_float(row["max_abs_lfun_at_zero"]) for row in checks) < 1e-28

    reconstruction = rows(output / "reconstruction.tsv")
    expected_rows = 438 * (3 + 3 + 5 + 9 + 11)
    assert len(reconstruction) == expected_rows, (
        f"expected {expected_rows} reconstruction rows, got {len(reconstruction)}"
    )
    for row in reconstruction:
        for key in ("E_observed", "E_K1", "E_K3", "E_K10", "E_K25"):
            assert math.isfinite(float(row[key])), f"non-finite {key}: {row}"

    summaries = rows(output / "transition_summary.tsv")
    assert len(summaries) == 20
    top = {int(row["q"]): row for row in summaries if row["window"] == "top_decade"}
    assert set(top) == set(MODULI)
    assert all(int(row["n_points"]) == 53 for row in top.values())
    assert all(int(row["rank_changes"]) > 0 for row in top.values())

    metrics = rows(output / "fit_metrics.tsv")
    selected = [
        row
        for row in metrics
        if row["window"] == "top_decade"
        and int(row["a"]) == int(row["q"]) - 1
        and int(row["K_zeros_per_character"]) == 25
    ]
    assert len(selected) == 5
    assert all(math.isfinite(float(row["correlation"])) for row in selected)

    prior = json.loads(prior_n8.read_text())
    prior_first = sorted(values[0] for values in prior.values())
    modes = rows(output / "mode_attribution.tsv")
    pari_first = sorted(
        float(row["gamma"])
        for row in modes
        if int(row["q"]) == 8 and int(row["zero_index_for_character"]) == 1
    )
    assert len(prior_first) == len(pari_first) == 3
    assert max(abs(a - b) for a, b in zip(prior_first, pari_first)) < 1e-12, (
        "PARI and the prior mpmath N=8 first-zero anchors disagree"
    )

    print("VERIFY PASS")
    print(f"curve_sha256={EXPECTED_CURVE_SHA256}")
    print("zero_checks=55/55 mesh agreement and residual < 1e-28")
    print(f"reconstruction_rows={len(reconstruction)}")
    print("prior_mpmath_N8_first_zeros=3/3 agree within 1e-12")
    print("top_decade_points=53 for every modulus; all have rank changes")


def main() -> None:
    if len(sys.argv) != 4:
        raise SystemExit("usage: verify_outputs.py CURVE PRIOR_N8_JSON OUTPUT_DIR")
    verify(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]))


if __name__ == "__main__":
    main()

