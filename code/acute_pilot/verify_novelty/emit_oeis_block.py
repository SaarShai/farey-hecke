#!/usr/bin/env python3
"""Emit an OEIS A089676 witness block in Kamenetsky's a089676_1.txt format.

Reads a plain file of 0/1 rows (one acute-set point per line, spaces optional)
and prints:

    a(<n>) >= <size>:
    (b b b ...) (b b b ...) ... (b b b ...)

matching the canonical witness-file style exactly: each point parenthesised,
bits space-separated, points separated by single spaces. Bit order is
left-to-right = coordinate 0..n-1, identical to verify.py / verify2.py parsing.

Usage:
    python3 emit_oeis_block.py <rows_file> <n>
    python3 emit_oeis_block.py <rows_file> <n> --header "By Your Name, D/MM/YYYY"

This does NOT verify acuteness -- run verify.py and verify2.py on the same file
first. The block is round-trip safe: re-parsing the printed block reproduces the
input set.
"""
import sys


def read_rows(path):
    rows = []
    n = None
    with open(path) as fh:
        for line in fh:
            bits = [c for c in line if c in "01"]
            if not bits:
                continue
            if n is None:
                n = len(bits)
            elif len(bits) != n:
                raise SystemExit(f"ragged row: {len(bits)} bits vs n={n}")
            rows.append(bits)
    return n, rows


def main(argv):
    if len(argv) < 3:
        print("usage: emit_oeis_block.py <rows_file> <n> [--header \"By Name, D/MM/YYYY\"]")
        return 2
    path = argv[1]
    n_expect = int(argv[2])
    header = None
    if "--header" in argv:
        i = argv.index("--header")
        header = argv[i + 1] if i + 1 < len(argv) else None

    n, rows = read_rows(path)
    if n != n_expect:
        print(f"ERROR: file dimension {n} != requested n {n_expect}", file=sys.stderr)
        return 1
    # de-dup check (a record witness must be all-distinct)
    keys = set(tuple(r) for r in rows)
    if len(keys) != len(rows):
        print(f"WARNING: {len(rows)-len(keys)} duplicate point(s) in input",
              file=sys.stderr)

    size = len(rows)
    if header:
        print("Best known lower bounds and their corresponding solutions "
              "for n=11 to 15 in A089676.")
        print(header)
        print()
    print(f"a({n}) >= {size}:")
    pts = ["(" + " ".join(r) + ")" for r in rows]
    print(" ".join(pts))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
