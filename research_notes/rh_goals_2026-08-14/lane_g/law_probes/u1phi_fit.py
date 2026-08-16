#!/usr/bin/env python3
"""Post-hoc robustness fits for probe_u1phi.py output.

Model:   D_q(t) = c + beta*log q + gamma/q
The gamma/q term absorbs (a) the O(1/q) Barnes-exponent drift, since kappa_q
carries [Barnes]^{(1-2/q)/2} whose q-dependence is exp(-(1/q) log Barnes),
and (b) the O(1/q) remainder of Lemma U1-4b.  If beta is stable with and
without gamma, the slope is not a 1/q artefact.

Reports beta -> alpha = 1 - beta/(2t) -> exponent -3*alpha at sigma = 2.
Also does a tail-only fit (drop the two smallest q) as a second robustness check.
"""
import json
import math
import sys


def lstsq(cols, y):
    """Normal equations for y ~ sum_j b_j * cols[j]. Returns coefficient list."""
    k = len(cols)
    A = [[sum(cols[i][n] * cols[j][n] for n in range(len(y))) for j in range(k)]
         for i in range(k)]
    b = [sum(cols[i][n] * y[n] for n in range(len(y))) for i in range(k)]
    # gaussian elimination
    for i in range(k):
        p = max(range(i, k), key=lambda r: abs(A[r][i]))
        A[i], A[p] = A[p], A[i]
        b[i], b[p] = b[p], b[i]
        for r in range(i + 1, k):
            f = A[r][i] / A[i][i]
            for c in range(i, k):
                A[r][c] -= f * A[i][c]
            b[r] -= f * b[i]
    x = [0.0] * k
    for i in reversed(range(k)):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, k))) / A[i][i]
    return x


def report(name, qs, D, t):
    n = len(qs)
    one = [1.0] * n
    lg = [math.log(q) for q in qs]
    inv = [1.0 / q for q in qs]
    out = {}
    for label, cols in (("2-param  (c + b log q)", [one, lg]),
                        ("3-param  (c + b log q + g/q)", [one, lg, inv])):
        co = lstsq(cols, D)
        beta = co[1]
        pred = [sum(c[i] * co[j] for j, c in enumerate(cols)) for i in range(n)]
        resid = max(abs(D[i] - pred[i]) for i in range(n))
        alpha = 1.0 - beta / (2 * t)
        print(f"  {label:32s} beta={beta:+8.4f}  alpha={alpha:+7.4f}  "
              f"exponent={-3*alpha:+7.4f}  maxresid={resid:.4f}")
        out[label] = dict(beta=beta, alpha=alpha, exponent=-3 * alpha,
                          resid=resid)
    return out


def main(path):
    doc = json.load(open(path))
    print("=== U1-phi robustness fits ===")
    print("prediction (5.1): beta = 0, alpha = 1, exponent = -3")
    print("no-decay null   : beta = 2t, alpha = 0, exponent = 0\n")
    res = {}
    for tag, S in doc["series"].items():
        t = S["t"]
        qs, D = S["qs"], S["D_unwrapped"]
        print(f"[{tag}]  t = {t:.6f}   null beta = 2t = {2*t:.4f}   n = {len(qs)}")
        res[tag] = {"full": report("full", qs, D, t)}
        if len(qs) > 4:
            print("  -- tail only (drop 2 smallest q) --")
            res[tag]["tail"] = report("tail", qs[2:], D[2:], t)
        print()
    json.dump(res, open("u1phi_fit.json", "w"), indent=1)
    print("wrote u1phi_fit.json")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "u1phi.json")
