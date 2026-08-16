#!/usr/bin/env python3
"""
strip_method_validation.py -- LANE G, TASK A step 0.

Question: can the Dirichlet series (2.1) for phi_q be analytically continued
into the CRUX STRIP  sigma in (3/4, 1)  well enough to trust non-arithmetic
numbers to >= 6 digits?

The only continuation available from the c-spectrum data is Mellin /
partial-summation with the exact main term subtracted:

   D(s) = sum_{c'} N(c') c'^{-2s}
        = sum_{c' <= X} N(c') c'^{-2s}  +  2s * int_X^inf A(t) t^{-2s-1} dt
   A(t) = sum_{c' <= t} N(c') = C_q t^2 + R(t),    C_q = 1/(pi * vol(F_q))
                                                       = 1/(pi^2 (1 - 2/q))
   => D_hat(s; X) = sum_{c'<=X} N(c')c'^{-2s} + 2s C_q X^{2-2s}/(2s-2)
      error       = 2s int_X^inf R(t) t^{-2s-1} dt.

This script measures that error EXACTLY in the one case where both the
coefficients and the answer are known in closed form: q = 3 (lam = 1,
PSL(2,Z)), where N(c) = Euler phi(c) and D(s) = zeta(2s-1)/zeta(2s).

If the method cannot reach 6 digits at q=3 with exact coefficients out to
X = 10^7, it cannot possibly reach 6 digits for a non-arithmetic q, whose
c-spectrum must be produced by BFS at cost ~ X^2.

Float / mpmath.  NON-RIGOROUS.
"""
import json, math
import numpy as np
from mpmath import mp, mpf, mpc, zeta, fabs

mp.dps = 30
TINF = 7.0673625708673465


def totient_sieve(n):
    phi = np.arange(n + 1, dtype=np.int64)
    for p in range(2, n + 1):
        if phi[p] == p:  # p prime
            phi[p::p] -= phi[p::p] // p
    return phi


def main():
    XMAX = 10 ** 7
    print("sieving totients to", XMAX, flush=True)
    phi = totient_sieve(XMAX)
    c = np.arange(XMAX + 1, dtype=np.float64)

    C3 = 3.0 / math.pi ** 2                      # 1/(pi*vol(F_3)) = 1/(pi*pi/3)
    # sanity on the main-term constant
    A = np.cumsum(phi[1:].astype(np.float64))
    for X in (10 ** 4, 10 ** 5, 10 ** 6, 10 ** 7):
        print(f"  A({X})/X^2 = {A[X-1]/X**2:.9f}  vs C3 = {C3:.9f}", flush=True)

    sigmas = [0.80, 0.85, 0.90, 0.95]
    ts = [1.5, 3.5, TINF]
    Xs = [10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6, 10 ** 7]

    rows = []
    logc = np.log(c[1:])
    for sg in sigmas:
        for t in ts:
            s = complex(sg, t)
            # partial sums of phi(c) c^{-2s} at the checkpoints
            w = np.exp(-2 * sg * logc) * np.exp(-2j * t * logc)
            terms = phi[1:].astype(np.float64) * w
            cum = np.cumsum(terms)
            exact = zeta(2 * mpc(sg, t) - 1) / zeta(2 * mpc(sg, t))
            r = {"sigma": sg, "t": t, "exact_abs": float(fabs(exact)),
                 "exact": [float(exact.real), float(exact.imag)], "by_X": []}
            for X in Xs:
                head = cum[X - 1]
                sc = mpc(sg, t)
                # sum_{c>X} N(c) c^{-2s} with dA ~ 2 C t dt:
                #   int_X^inf t^{-2s} * 2 C t dt = C X^{2-2s} / (s-1)
                tail = C3 * mpf(X) ** (2 - 2 * sc) / (sc - 1)
                est = mpc(head.real, head.imag) + tail
                relerr = float(fabs(est - exact) / fabs(exact))
                r["by_X"].append({"X": X, "est_abs": float(fabs(est)),
                                  "rel_err": relerr,
                                  "digits": -math.log10(relerr) if relerr > 0 else 99})
            rows.append(r)
            print(f"sigma={sg} t={t:.4f} |exact|={float(fabs(exact)):.6f}  " +
                  "  ".join(f"X=1e{int(math.log10(d['X']))}:{d['rel_err']:.2e}"
                            for d in r["by_X"]), flush=True)

    # empirical convergence exponent of the truncation error in X, and the X
    # needed for 1e-6
    for r in rows:
        e = [d["rel_err"] for d in r["by_X"]]
        x = [math.log10(d["X"]) for d in r["by_X"]]
        # slope over the last three checkpoints
        sl = (math.log10(e[-1]) - math.log10(e[-3])) / (x[-1] - x[-3])
        r["logslope_err_vs_X"] = sl
        r["X_needed_1e-6"] = (10 ** (x[-1] + (math.log10(e[-1]) - (-6)) / (-sl))
                              if sl < 0 else None)

    out = {"description": "TASK A step 0: can the phi_q Dirichlet series be "
                          "continued into sigma in (3/4,1)? Benchmarked at q=3 "
                          "with EXACT coefficients N(c)=totient(c) against the "
                          "closed form zeta(2s-1)/zeta(2s).",
           "method": "D_hat(s;X) = sum_{c<=X} N(c)c^{-2s} + 2s C X^{2-2s}/(2s-2)",
           "C3": C3, "rows": rows}
    with open(__file__.replace(".py", ".json"), "w") as f:
        json.dump(out, f, indent=1)
    print("\n=== needed X for 1e-6 ===")
    for r in rows:
        xn = r["X_needed_1e-6"]
        print(f"  sigma={r['sigma']} t={r['t']:.4f}  err-slope={r['logslope_err_vs_X']:+.3f}"
              f"  X_needed={xn if xn is None else f'{xn:.3e}'}")


if __name__ == "__main__":
    main()
