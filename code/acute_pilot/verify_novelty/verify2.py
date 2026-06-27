#!/usr/bin/env python3
"""
SECOND INDEPENDENT VERIFIER for OEIS A089676 (max ACUTE set in {0,1}^n).
Author: independent verification arm (acute-set pilot).

DESIGN GOAL: be a *cross-check* of code/acute_pilot/verify.py that shares NO
implementation idea, so a bug in either could not hide in both.

  - verify.py uses the bitmask identity: a right angle at apex Q between P,R
    happens iff (P^Q) & (R^Q) == 0, computed with python int XOR/AND/popcount.
  - verify2.py (this file) does the OPPOSITE: it stores every vector as an
    EXPLICIT integer coordinate tuple/list and computes the geometric dot
    product (P-Q).(R-Q) = sum_i (p_i - q_i)*(r_i - q_i) directly, in plain
    arithmetic. A right angle is dot == 0. No XOR, no AND, no popcount.

MATH RECAP (for the record, derived independently here):
  Vertices live in {0,1}^n. For an apex Q and two other points P,R the angle PQR
  has cosine proportional to the dot product D = (P-Q).(R-Q). Each coordinate
  term (p_i - q_i)*(r_i - q_i) is one of {-1,0,1}*{-1,0,1}; but for 0/1 vectors
  it can NEVER be -1: (p_i-q_i) and (r_i-q_i) are both in {-1,0,1}, and a product
  of -1 needs one factor +1 and the other -1, i.e. one of p_i,r_i equals 1 while
  the other equals 0 AND q_i sits strictly between them -- impossible since q_i
  is also 0 or 1. So every per-coordinate term is in {0,1}, hence D >= 0 always,
  so NO obtuse angle is possible and the ONLY forbidden configuration is D == 0
  (a right angle). [This independently reproduces verify.py's comment, by a
  different route -- coordinate sign analysis rather than the XOR/AND identity.]
  A set S is ACUTE iff for every ordered triple (P, apex Q, R) with the three
  points distinct, D = (P-Q).(R-Q) != 0, i.e. D >= 1.

  We also assert internally that D is never negative (defends the math claim);
  if a negative D were ever seen the math model would be wrong and we abort.

CLI:
  python3 verify2.py --selftest                  # check the 5 OEIS records
  python3 verify2.py <witness_file> [n]          # rows of 0/1, one vector/line
  python3 verify2.py --selftest --quiet          # only final PASS/FAIL line

Exit 0 iff acute AND all points distinct (AND, in --selftest, sizes match claims).
"""

import sys
import os
import re
from itertools import combinations


# ---------------------------------------------------------------------------
# Core: explicit coordinate dot product. NO bitmask tricks anywhere below.
# ---------------------------------------------------------------------------

def dot_diff(P, Q, R):
    """Integer dot product (P-Q).(R-Q) for coordinate lists of equal length.

    Done coordinate by coordinate in plain arithmetic. Also sanity-asserts the
    sign theorem (term in {0,1}) so a mistaken witness format can't slip a
    negative term past us silently.
    """
    total = 0
    for p, q, r in zip(P, Q, R):
        term = (p - q) * (r - q)
        # For 0/1 inputs each term must be 0 or 1; guard against bad data.
        if term < 0:
            raise AssertionError(
                "negative coordinate term -- inputs are not 0/1 vectors"
            )
        total += term
    return total


def is_acute_explicit(points):
    """points: list of coordinate lists (each list of 0/1 ints).

    Returns (ok: bool, reason). O(m^3) over distinct triples, brute force.
    A right angle is dot == 0 at the apex. We test each unordered apex pair
    {a,b} against every apex Q != a,b; that covers all ordered right-angle
    triples since the right angle only depends on which point is the apex.
    """
    m = len(points)

    # all-distinct check (independent of any hashing trick: tuple compare)
    seen = set()
    for idx, v in enumerate(points):
        key = tuple(v)
        if key in seen:
            return (False, ("DUPLICATE_POINT", idx))
        seen.add(key)

    # brute O(m^3): for each apex Q, every pair of the other points
    for qi in range(m):
        Q = points[qi]
        others = [i for i in range(m) if i != qi]
        for ai, bi in combinations(others, 2):
            d = dot_diff(points[ai], Q, points[bi])
            if d == 0:
                return (False, ("RIGHT_ANGLE", "apex", qi, "legs", ai, bi))
    return (True, None)


# ---------------------------------------------------------------------------
# Parsing. Deliberately written fresh (not copied from verify.py).
# ---------------------------------------------------------------------------

def line_to_vec(line):
    """Extract the 0/1 digits from a line into a list of ints, or None if none."""
    bits = [int(c) for c in line if c == '0' or c == '1']
    return bits if bits else None


def read_witness_file(path):
    """Read a plain witness file: one 0/1 vector per non-empty line.

    Returns (n, points). Raises on ragged rows.
    """
    points = []
    n = None
    with open(path) as fh:
        for line in fh:
            vec = line_to_vec(line)
            if vec is None:
                continue
            if n is None:
                n = len(vec)
            elif len(vec) != n:
                raise ValueError(f"ragged row: {len(vec)} bits vs n={n}")
            points.append(vec)
    return n, points


def parse_oeis_records(path):
    """Parse Kamenetsky's combined OEIS file into {n: (claim, points)}.

    Each block looks like 'a(NN) >= CLAIM:' followed by parenthesised vectors
    '(0 1 0 ... )'. Written independently of verify.py's parser.
    """
    text = open(path).read()
    records = {}
    # find each header and the span of text until the next header (or EOF)
    headers = list(re.finditer(r'a\((\d+)\)\s*>=\s*(\d+):', text))
    for h_idx, h in enumerate(headers):
        n_val = int(h.group(1))
        claim = int(h.group(2))
        start = h.end()
        end = headers[h_idx + 1].start() if h_idx + 1 < len(headers) else len(text)
        block = text[start:end]
        vecs = re.findall(r'\(([01\s]+)\)', block)
        points = []
        n_seen = None
        for v in vecs:
            bits = [int(c) for c in v if c in '01']
            if not bits:
                continue
            if n_seen is None:
                n_seen = len(bits)
            elif len(bits) != n_seen:
                raise ValueError(f"ragged record vector at a({n_val})")
            points.append(bits)
        records[n_val] = (claim, n_seen, points)
    return records


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def run_selftest(quiet=False):
    here = os.path.dirname(os.path.abspath(__file__))
    # default to the shared witness file one directory up
    wf = os.path.join(here, "..", "a089676_witnesses.txt")
    wf = os.path.normpath(wf)
    if not os.path.exists(wf):
        print(f"FAIL: cannot find witness file at {wf}")
        return 1
    records = parse_oeis_records(wf)
    all_ok = True
    for n_val in sorted(records):
        claim, n_seen, points = records[n_val]
        ok, reason = is_acute_explicit(points)
        size = len(points)
        # a record is good iff: acute, size == claimed lower bound, and the
        # vector width matches n.
        good = ok and (size == claim) and (n_seen == n_val)
        all_ok &= good
        if not quiet:
            tag = "PASS" if good else f"FAIL {reason}"
            print(f"n={n_val}: dim={n_seen} size={size} claim={claim} "
                  f"acute={ok} {tag}")
    print("SELFTEST", "PASS" if all_ok else "FAIL")
    return 0 if all_ok else 1


def run_file(path, n_expect=None):
    n, points = read_witness_file(path)
    if n_expect is not None and n != n_expect:
        print(f"FAIL: dimension {n} != expected {n_expect}")
        return 1
    ok, reason = is_acute_explicit(points)
    print(f"n={n} size={len(points)} acute={ok}")
    if ok:
        print(f"PASS  (acute set of size {len(points)} in {{0,1}}^{n})")
        return 0
    print(f"FAIL  {reason}")
    return 1


def main(argv):
    quiet = "--quiet" in argv
    argv = [a for a in argv if a != "--quiet"]
    if len(argv) >= 2 and argv[1] == "--selftest":
        return run_selftest(quiet=quiet)
    if len(argv) < 2:
        print("usage: verify2.py <witness_file> [n]  |  verify2.py --selftest")
        return 2
    path = argv[1]
    n_expect = int(argv[2]) if len(argv) >= 3 else None
    return run_file(path, n_expect)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
