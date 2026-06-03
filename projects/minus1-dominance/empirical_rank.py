#!/usr/bin/env python3
"""
empirical_rank.py  (LOCAL ONLY — no network)

For each N in {7,8,11,19,23}, parse the two VERIFIED gold-checkpoint files,
take the LARGEST available x, compute D(x;N,a)=pi(x;N,a)-pi(x;N,1) for every
coprime residue a, identify the quadratic NON-residues mod N, and report:
  - the rank of the (-1 mod N) class among the non-residues (1 = largest D),
  - whether the -1 class is STRICTLY largest among all non-residues.

Both files are parsed independently and cross-checked: the integer D-values
must agree exactly at the largest x, else we abort (no fabrication).

Files (both have identical block layout):
  ## N = k
  x  count_a=1 count_a=2 ...           <- absolute counts pi(x;k,a)
  # diffs pi(x;k,a)-pi(x;k,1)
  x  diff_a=2 diff_a=3 ...             <- diffs (a=1 omitted, since D=0 there)
"""

import os
import sys

FILES = [
    "/Users/za/Documents/Farey NOW/koyama_replication_bundle/out2.tsv",
    "/Users/za/Documents/Farey NOW/koyama_replication_bundle/indep_full.tsv",
]
NS = [7, 8, 11, 19, 23]


def egcd_ok(a, n):
    while n:
        a, n = n, a % n
    return a == 1


def coprime_residues(n):
    return [a for a in range(1, n) if egcd_ok(a, n)]


def quadratic_residues(n):
    """Set of QRs among units mod n (a is QR iff a == b^2 mod n for some unit b)."""
    qr = set()
    for b in coprime_residues(n):
        qr.add((b * b) % n)
    return qr


def parse_counts(path):
    """
    Return dict: N -> dict with
        'rows': dict x -> { a : count(x;N,a) }   (a includes a=1 and all coprime a)
    Parsed from the 'count_a=' blocks only (absolute counts).
    """
    result = {}
    cur_N = None
    header_as = None  # list of a-values matching columns after x
    mode = None  # 'count' while inside a count block
    with open(path) as fh:
        for raw in fh:
            line = raw.rstrip("\n")
            if not line.strip():
                continue
            if line.startswith("## N ="):
                cur_N = int(line.split("=")[1].strip())
                result.setdefault(cur_N, {"rows": {}})
                mode = None
                header_as = None
                continue
            if line.startswith("# diffs"):
                # leaving the count block; ignore diff block entirely here
                mode = None
                header_as = None
                continue
            if line.startswith("#"):
                # other comment
                continue
            parts = line.split("\t")
            if parts[0] == "x":
                # header row: parse the a-values from 'count_a=K' tokens
                if any(tok.startswith("count_a=") for tok in parts[1:]):
                    header_as = [int(tok.split("=")[1]) for tok in parts[1:]]
                    mode = "count"
                else:
                    # a diff header (diff_a=) — not used here
                    mode = None
                    header_as = None
                continue
            if line.startswith("TOTAL"):
                continue
            # data row
            if mode == "count" and header_as is not None and cur_N is not None:
                x = int(parts[0])
                vals = [int(v) for v in parts[1:]]
                if len(vals) != len(header_as):
                    raise ValueError(
                        f"{path}: N={cur_N} x={x} col mismatch "
                        f"{len(vals)} vs {len(header_as)}"
                    )
                result[cur_N]["rows"][x] = dict(zip(header_as, vals))
    return result


def compute_D_at_max_x(counts_for_N):
    """Given {'rows': {x:{a:count}}}, pick max x, return (x, {a: D=count_a - count_1})."""
    rows = counts_for_N["rows"]
    xmax = max(rows.keys())
    row = rows[xmax]
    base = row[1]  # count(x;N,1)
    D = {a: row[a] - base for a in row}
    return xmax, D


def analyze(N, D):
    units = sorted(D.keys())
    qr = quadratic_residues(N)
    nonres = [a for a in units if a not in qr and a != 1]  # a=1 is the QR base
    # -1 class
    minus1 = (N - 1) % N
    # rank among non-residues by D descending (1 = largest)
    nr_sorted = sorted(nonres, key=lambda a: D[a], reverse=True)
    # rank of minus1 among NR
    if minus1 in nonres:
        rank = nr_sorted.index(minus1) + 1
    else:
        rank = None  # -1 is a QR (shouldn't happen for these N: -1 is NR iff N=3 mod 4)
    # strictly largest among ALL non-residues?
    Dm = D[minus1]
    others = [D[a] for a in nonres if a != minus1]
    strict = (minus1 in nonres) and all(Dm > o for o in others)
    # also: is -1 strictly largest among ALL units (not just NR)?
    all_others = [D[a] for a in units if a != minus1]
    strict_all_units = all(Dm > o for o in all_others)
    return {
        "units": units,
        "qr": sorted(qr),
        "nonres": nonres,
        "minus1": minus1,
        "minus1_in_nonres": minus1 in nonres,
        "rank": rank,
        "n_nonres": len(nonres),
        "strict_among_NR": strict,
        "strict_among_all_units": strict_all_units,
        "D": D,
        "nr_sorted": nr_sorted,
    }


def main():
    parsed = {}
    for path in FILES:
        if not os.path.exists(path):
            print(f"MISSING FILE: {path}", file=sys.stderr)
            sys.exit(2)
        parsed[path] = parse_counts(path)

    # Cross-check the two files at the largest x for each N (exact integer agreement)
    print("=== CROSS-CHECK (two independent sieves) ===")
    base = parsed[FILES[0]]
    other = parsed[FILES[1]]
    for N in NS:
        x0, D0 = compute_D_at_max_x(base[N])
        x1, D1 = compute_D_at_max_x(other[N])
        agree = (x0 == x1) and (D0 == D1)
        print(f"N={N}: xmax={x0} ; files agree exactly: {agree}")
        if not agree:
            print(f"  !! DISAGREEMENT N={N}: x0={x0} x1={x1}")
            print(f"     D0={D0}")
            print(f"     D1={D1}")
            sys.exit(3)
    print()

    print("=== PER-N RANK ANALYSIS at largest x (x = 1.3e13) ===")
    summary = {}
    for N in NS:
        xmax, D = compute_D_at_max_x(base[N])
        res = analyze(N, D)
        summary[N] = (xmax, res)
        print(f"\n## N = {N}   (x = {xmax})")
        print(f"  units (coprime a): {res['units']}")
        print(f"  quadratic residues mod {N}: {res['qr']}")
        print(f"  -1 class = {N}-1 = {res['minus1']}  (-1 is NON-residue: {res['minus1_in_nonres']})")
        print(f"  D-values for ALL coprime a (D(x;N,a)=pi(x;N,a)-pi(x;N,1)):")
        for a in res["units"]:
            tag = ""
            if a == 1:
                tag = "  [base a=1, D=0]"
            elif a == res["minus1"]:
                tag = "  <-- -1 class"
            kind = "QR" if a in set(res["qr"]) else "NR"
            print(f"      a={a:2d} [{kind}]: D = {res['D'][a]:>12d}{tag}")
        print(f"  NON-residues: {res['nonres']}  (count={res['n_nonres']})")
        print(f"  NR sorted by D desc: " +
              ", ".join(f"a={a}(D={res['D'][a]})" for a in res["nr_sorted"]))
        if res["rank"] is not None:
            print(f"  RANK of -1 (a={res['minus1']}) among non-residues: "
                  f"{res['rank']} of {res['n_nonres']}  (1=largest)")
        print(f"  -1 STRICTLY largest among NON-residues: {res['strict_among_NR']}")
        print(f"  -1 strictly largest among ALL units:   {res['strict_among_all_units']}")

    # Reconfirm the stated known facts
    print("\n=== RECONFIRM KNOWN FACTS ===")
    _, r8 = summary[8]
    print(f"N=8 strict among NR: {r8['strict_among_NR']}  "
          f"(rank={r8['rank']} of {r8['n_nonres']})  [expected: strict, rank 1]")

    _, r11 = summary[11]
    D11_10 = r11["D"][10]
    rank11 = r11["rank"]
    print(f"N=11 a=10 D={D11_10}  [expected 11503]; "
          f"rank of -1 among NR = {rank11} of {r11['n_nonres']}  "
          f"[expected: NOT top group, ~3rd-4th of 5]")

    _, r19 = summary[19]
    print(f"N=19 a=18 D={r19['D'][18]}; rank of -1 among NR = "
          f"{r19['rank']} of {r19['n_nonres']}  [expected: mid, ~3rd of 9]")

    for N in (7, 23):
        _, r = summary[N]
        print(f"N={N} a={r['minus1']} D={r['D'][r['minus1']]}; "
              f"rank of -1 among NR = {r['rank']} of {r['n_nonres']}; "
              f"strict={r['strict_among_NR']}  [expected: bias onset ~e^33.4~3e14, NOT yet at 1.3e13]")


if __name__ == "__main__":
    main()
