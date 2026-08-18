#!/usr/bin/env python3
"""Receipt for LAW_R1_COSET_STRUCTURE.md's fitted slopes and table ranges.

Added 2026-08-18 under [CORRECTION 2026-08-18 audit-14/15]: the note quoted
fit slopes (-1.72 / -1.85) that no committed script emitted. This script
recomputes every fitted/ranged number in the note DIRECTLY from the tables
printed in the note itself (sec.3.2 "total" column, sec.4 partial-window
table), with the fit convention stated explicitly: unweighted least squares
of log(y) on log(x) over all listed points.

Run: python3 r1_table_fits.py   (stdlib only)
"""
import math

# LAW_R1_COSET_STRUCTURE.md sec.3.2, "total (proxy for D)" column.
Q = [8, 12, 16, 24, 32, 48]
TOTAL = {
    1.1: [0.23976, 0.13903, 0.09516, 0.04695, 0.02462, 0.01027],
    1.5: [0.08532, 0.04012, 0.02404, 0.01090, 0.00583, 0.00250],
}

# LAW_R1_COSET_STRUCTURE.md sec.4 partial-window mass table.
XP = [10, 20, 30, 40]
WINDOW = {
    "8": [0.25532, 0.11922, 0.06086, 0.02673],
    "12": [0.19779, 0.11662, 0.06709, 0.02951],
    "16": [0.17617, 0.10791, 0.05153, 0.02591],
    "24": [0.18006, 0.09046, 0.05302, 0.02180],
    "32": [0.16529, 0.08324, 0.04955, 0.02034],
    "48": [0.15618, 0.07867, 0.04590, 0.01896],
    "theta": [0.17524, 0.08671, 0.04704, 0.02172],
}


def loglog_slope(xs, ys):
    """Unweighted least-squares slope of log(y) on log(x)."""
    lx = [math.log(v) for v in xs]
    ly = [math.log(v) for v in ys]
    n = len(lx)
    mx, my = sum(lx) / n, sum(ly) / n
    num = sum((a - mx) * (b - my) for a, b in zip(lx, ly))
    den = sum((a - mx) ** 2 for a in lx)
    return num / den


def main():
    print("[sec.3.2] aggregate total vs q, unweighted log-log least squares")
    for s, ys in TOTAL.items():
        print("  s=%.1f  slope = %.4f" % (s, loglog_slope(Q, ys)))

    print("[sec.4] partial-window mass vs X', slope per group")
    slopes = {k: loglog_slope(XP, v) for k, v in WINDOW.items()}
    for k, v in slopes.items():
        print("  q=%-6s slope = %.4f" % (k, v))
    print("  slope range: %.4f .. %.4f" % (min(slopes.values()), max(slopes.values())))

    print("[sec.4] per-column range and argmax")
    for i, x in enumerate(XP):
        col = {k: v[i] for k, v in WINDOW.items()}
        lo, hi = min(col.values()), max(col.values())
        arg = max(col, key=col.get)
        print("  X'=%-3d range %.5f .. %.5f   argmax q=%s" % (x, lo, hi, arg))


if __name__ == "__main__":
    main()
