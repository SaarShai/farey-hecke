#!/usr/bin/env python3
"""INDEPENDENT brute-force cross-check of orientable-sequence maxima OS(n).
Written from scratch (no reuse of the agent's sat_os/verify_os) to validate the SAT
encoding's UNSAT claims. An OS(n) of length L: cyclic binary seq whose L length-n windows
AND their L reversals are 2L distinct strings (⇒ no repeated window, no window = another's
reverse, no palindromic window). exists(n,L) exhausts all 2^L strings (rotation not pruned;
fine for L<=20). Confirms SAT@L* and UNSAT@(L*+1) independently of the SAT solver."""
import sys

def is_os(bits, n):
    L = len(bits)
    if L < n: return False
    strs = set()
    for i in range(L):
        w = tuple(bits[(i+j) % L] for j in range(n))
        wr = w[::-1]
        strs.add(w); strs.add(wr)
    return len(strs) == 2*L

def exists(n, L):
    for x in range(1 << L):
        bits = [(x >> k) & 1 for k in range(L)]
        if is_os(bits, n):
            return ''.join(map(str, bits))
    return None

if __name__ == "__main__":
    # (n, L) cases: validate SAT at L* and UNSAT at L*+1 (the settle)
    cases = [(5,6),(5,7),(6,16),(6,17)]
    if len(sys.argv) == 3:
        cases = [(int(sys.argv[1]), int(sys.argv[2]))]
    for n, L in cases:
        w = exists(n, L)
        if w is None:
            print(f"n={n} L={L}: NO OS exists (exhaustive over 2^{L}={1<<L}) -> UNSAT")
        else:
            ok = is_os([int(c) for c in w], n)
            print(f"n={n} L={L}: OS EXISTS -> SAT  witness={w}  (recheck={ok})")
