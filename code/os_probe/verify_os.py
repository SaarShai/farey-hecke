#!/usr/bin/env python3
"""
Exact verifier for binary ORIENTABLE SEQUENCES of order n (OS(n)).

Definition (Gabric-Sawada, arXiv:2401.14341; debruijnsequence.org):
A cyclic binary sequence S of period L is an orientable sequence of order n
iff the multiset of all length-n cyclic windows AND all their reversals are
ALL DISTINCT. Equivalently: collect the 2L strings { window_i, reverse(window_i) }
for i in 0..L-1; they must be 2L distinct length-n strings.

Consequences (all implied by the above, used as cross-checks):
  - all L forward windows distinct (no repeated n-window): de Bruijn condition
  - no window equals the reverse of any window (including itself => no palindromic
    window)

We implement the verifier DIRECTLY from the 2L-distinctness definition, and
additionally report the component checks for transparency.

A cyclic sequence of period L has L windows (indices wrap around).
We require L > n is NOT assumed; standard convention treats S as cyclic of
length L and windows wrap. (For L <= n the notion degenerates; we still apply
the same rule.)
"""
import sys


def windows(s):
    """All L cyclic length-n windows of cyclic string s (n = len implied by caller).
    Here n is global via closure; we pass n explicitly instead."""
    raise NotImplementedError


def all_windows(s, n):
    L = len(s)
    d = s + s[:n - 1]  # unroll to handle wrap
    return [d[i:i + n] for i in range(L)]


def is_orientable(s, n, verbose=False):
    """Return (ok, reason). s is a binary string (cyclic, period len(s))."""
    if any(c not in '01' for c in s):
        return False, "non-binary character"
    L = len(s)
    if L == 0:
        return False, "empty"
    wins = all_windows(s, n)

    # Core definition: 2L strings {w, reverse(w)} all distinct.
    bag = []
    for w in wins:
        bag.append(w)
        bag.append(w[::-1])
    if len(set(bag)) != 2 * L:
        # diagnose
        # 1) duplicate forward window?
        if len(set(wins)) != L:
            seen = {}
            for i, w in enumerate(wins):
                if w in seen:
                    return False, f"repeated forward window {w} at positions {seen[w]} and {i}"
                seen[w] = i
        # 2) palindrome window (w == reverse(w))
        for i, w in enumerate(wins):
            if w == w[::-1]:
                return False, f"palindromic window {w} at position {i}"
        # 3) window equals reverse of another window
        winset = set(wins)
        for i, w in enumerate(wins):
            r = w[::-1]
            if r in winset and r != w:
                return False, f"window {w} (pos {i}) is reverse of another window {r}"
        return False, "2L-distinctness failed (unclassified)"

    if verbose:
        print(f"  L={L}, n={n}: {L} windows + {L} reversals = {2*L} all distinct. OK.")
    return True, "valid OS(n)"


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("seq", help="binary string OR path to file containing it")
    ap.add_argument("-n", type=int, default=8)
    ap.add_argument("-v", action="store_true")
    args = ap.parse_args()
    s = args.seq
    import os
    if os.path.exists(s):
        s = open(s).read().strip()
    s = ''.join(ch for ch in s if ch in '01')
    ok, reason = is_orientable(s, args.n, verbose=True)
    print(f"period L = {len(s)}")
    print(f"order  n = {args.n}")
    print(f"RESULT: {'VALID' if ok else 'INVALID'} -- {reason}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
