#!/usr/bin/env python3
"""
Validation harness. Ties the exact verifier and SAT model to KNOWN ground truth
(Gabric-Sawada arXiv:2401.14341, Table 2) so any reader can re-check the setup.

Ground truth (Table 2, binary OS(n)):
   n :  longest-known L*   upper bound U
   5 :       6                6
   6 :      16               17
   7 :      36               40   (we PROVE max=36 via SAT here)
   8 :      92               96

Run:  python3 test_validate.py
"""
import sys
from verify_os import is_orientable
from sat_os import solve


def check(cond, msg):
    print(("PASS" if cond else "FAIL") + ": " + msg)
    if not cond:
        sys.exit(1)


def main():
    # --- verifier unit tests ---
    # palindromic window rejected
    ok, _ = is_orientable("0110", 4)
    check(not ok, "verifier rejects palindromic window (0110, n=4)")
    # reverse collision rejected
    ok, _ = is_orientable("0001", 4)
    check(not ok, "verifier rejects window==reverse-of-another (0001, n=4)")
    # repeated forward window rejected
    ok, _ = is_orientable("00000000", 4)
    check(not ok, "verifier rejects repeated forward window")

    # known maximal witnesses ACCEPTED
    w5 = "001011"            # OS(5), period 6 (= max)
    w6 = "0001010110010111"  # OS(6), period 16
    check(is_orientable(w5, 5)[0], "verifier ACCEPTS known max OS(5) period-6 witness")
    check(is_orientable(w6, 6)[0], "verifier ACCEPTS known OS(6) period-16 witness")

    # corrupting a known witness => rejected (flip one bit)
    bad = "0" + w5[1:] if w5[0] == "1" else "1" + w5[1:]
    check(not is_orientable(bad, 5)[0], "verifier REJECTS one-bit corruption of OS(5) witness")

    # --- SAT model agrees with known maxima ---
    sat6, s6 = solve(6, 5, verbose=False)
    check(sat6 and is_orientable(s6, 5)[0], "SAT: OS(5) period 6 SAT and verifies")
    sat7, _ = solve(7, 5, verbose=False)
    check(not sat7, "SAT: OS(5) period 7 UNSAT (=> max OS(5)=6, matches lit)")

    sat16, s16 = solve(16, 6, verbose=False)
    check(sat16 and is_orientable(s16, 6)[0], "SAT: OS(6) period 16 SAT and verifies")
    sat17, _ = solve(17, 6, verbose=False)
    check(not sat17, "SAT: OS(6) period 17 UNSAT (=> max OS(6)=16)")

    print("\nALL VALIDATION CHECKS PASSED.")


if __name__ == "__main__":
    main()
