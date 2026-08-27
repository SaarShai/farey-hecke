#!/usr/bin/env python3
"""Verify every shared raw count through 1.3e13 against out2.tsv."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
MODULI = (7, 8, 11, 19, 23)
MAX_X = 13_000_000_000_000


def parse_curve(path: Path) -> dict[int, dict[int, dict[int, int]]]:
    curve = {modulus: defaultdict(dict) for modulus in MODULI}
    with path.open() as stream:
        for line in stream:
            if line.startswith(("#", "TOTAL")):
                continue
            fields = line.rstrip("\n").split("\t")
            if len(fields) != 4:
                continue
            modulus, x, residue, count = map(int, fields)
            if modulus in curve:
                curve[modulus][x][residue] = count
    return curve


def parse_baseline(path: Path) -> dict[int, dict[int, dict[int, int]]]:
    baseline = {modulus: {} for modulus in MODULI}
    modulus = None
    columns: list[int] = []
    raw_mode = False
    with path.open() as stream:
        for line in stream:
            text = line.rstrip("\n")
            if text.startswith("## N ="):
                modulus = int(text.split("=")[1])
                raw_mode = False
            elif text.startswith("x\tcount_a="):
                columns = [int(item.split("=")[1]) for item in text.split("\t")[1:]]
                raw_mode = True
            elif text.startswith("# diffs") or text.startswith("x\tdiff_a="):
                raw_mode = False
            elif text and not text.startswith("#") and raw_mode and modulus in baseline:
                fields = text.split("\t")
                x = int(fields[0])
                counts = [int(value) for value in fields[1:]]
                baseline[modulus][x] = dict(zip(columns, counts, strict=True))
    return baseline


def main() -> None:
    curve = parse_curve(HERE / "curve_3e14.tsv")
    baseline = parse_baseline(HERE / "out2.tsv")
    comparisons = 0
    mismatches: list[tuple[int, int, int, int, int]] = []
    for modulus in MODULI:
        shared = sorted(set(curve[modulus]) & set(baseline[modulus]))
        for x in (value for value in shared if value <= MAX_X):
            for residue, expected in baseline[modulus][x].items():
                observed = curve[modulus][x].get(residue)
                comparisons += 1
                if observed != expected:
                    mismatches.append((modulus, x, residue, expected, observed))
    assert comparisons == 567, f"expected 567 comparisons, obtained {comparisons}"
    assert not mismatches, f"baseline mismatches: {mismatches[:10]}"
    print("PASS: 567/567 shared raw-count cells match exactly; 0 mismatches")


if __name__ == "__main__":
    main()
