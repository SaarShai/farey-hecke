#!/usr/bin/env python3
"""
Probe (U1-phi) -- the falsifiable test of prediction (5.1) of LAW_U1_GROWTH.md.

PREDICTION (5.1):
    phi_q(s) ~ (pi/q)^{2s-1} * phi_theta(s) * Gamma(s)Gamma(3/2-s)/(Gamma(1-s)Gamma(1/2+s))
i.e. |phi_q(2+it)| = O(q^{-3}).   That is (U1-phi-a).

WHY THE CRITICAL LINE CARRIES THE ANSWER.
phi_q is not computable for non-arithmetic q.  But Teo's functional equation
(LAW_U3_TRANSPORT.md 2.5) gives

    Z_q(1-s) = kappa_q(s) Z_q(s),
    kappa_q(s) = (-1)^{A_q/2} 2^{-(2s-1)} phi_q(s) tan(pi s/2)^{1/2} E_q(s)
                 * [Barnes(s)]^{(1-2/q)/2} * [Gamma(3/2-s)/Gamma(s+1/2)] .

On Re s = 1/2 one has 1-s = conj(s) and Z_q has real coefficients, so

    kappa_q(1/2+it) = conj(Z_q(1/2+it)) / Z_q(1/2+it) = exp(-2 i arg Z_q(1/2+it)).

Every factor of kappa_q has modulus 1 there (LAW_U1_GROWTH 3.1, verified),
so on the critical line the ENTIRE content of the prediction is a PHASE
statement -- exactly the information the modulus cannot carry, and exactly
what the sup-guard (which measures |Z_q| only) is blind to.

THE ANSATZ AND THE EXPONENT.
Suppose the q-dependence of phi_q is a pure power of the Teo variable:
    phi_q(s) = (c_q)^{2s-1} * psi(s) * (1 + o(1)),    c_q = C * q^{-alpha}.
Prediction (5.1) is exactly alpha = 1 (c_q = pi/q).  Then

  * arg phi_q(1/2+it) picks up  2 t log c_q = -2 alpha t log q + const;
  * arg E_q(1/2+it)   picks up  +2 t log q + const   (LAW_U1_GROWTH Lemma U1-4b,
    log E_q = (2s-1) log(q/2pi) + log(Gamma(1-s)/Gamma(s)) + O(1/q));
  * every other factor of kappa_q is q-independent except the Barnes exponent
    (1-2/q)/2, whose q-dependence is O(1/q).

Hence
    D_q(t) := arg kappa_q(1/2+it) = -2 arg Z_q(1/2+it)
            = const(t) + 2 t (1 - alpha) log q + O(1/q).           (*)

    beta(t) := d D_q(t) / d log q  =  2 t (1 - alpha).

    alpha = 1 - beta/(2t).      |phi_q(2+it)| ~ q^{-3 alpha}.

So the DECISIVE NUMBER is  -3 alpha = -3 + 3 beta / (2t).
    beta = 0    <=>  alpha = 1  <=>  exponent -3  <=>  PREDICTION CONSISTENT.
    beta = 2t   <=>  alpha = 0  <=>  exponent  0  <=>  phi_q has no q-decay,
                                                       PREDICTION REFUTED.

Running at TWO values of t tests the ansatz itself: beta(t) must be
proportional to t.  If it is not, the "pure power (c_q)^{2s-1}" ansatz is
wrong and no single exponent exists.

WHAT IS MEASURED.  Z_q(1/2+it) is replaced by the repo's only in-strip
evaluator, the Rosen/MMS transfer-operator determinant product
    P_q(s) := det(1 - L_{s,q}^{+}) * det(1 - L_{s,q}^{-}),
identified with Z_{G_q}(s) by R5 at q=5 and by obligation U4 in general.
The evaluation points 1/2 + i t with t > 1 lie INSIDE the R5 common
continuation domain Omega* = {Re s > 1/2} u {Re s > 0, Im s > 1} -- unlike
the guard's dU_4, which sat on its boundary.

NON-RIGOROUS: midpoint evaluation, no ball radii, no winding certificate.
This probe uses the ARGUMENT of P_q, which earlier probes never used; the
control points at real s > 1 (where Z_q > 0) check that arg P_q = 0 there,
i.e. that the identification carries no spurious q-dependent phase.

Usage:  python3 probe_u1phi.py [--N 32] [--out u1phi.json]
"""
from __future__ import annotations

import argparse
import cmath
import json
import math
import sys
import time
from pathlib import Path

REPO = Path("/Users/za/Documents/farey-hecke")
sys.path.insert(0, str(REPO / ".worktrees/aletheia-restore/code"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import zeta_cert_rosen_even as E  # noqa: E402
from flint import acb, arb, ctx  # noqa: E402

T_PHYS = 7.0673625708673465  # Im s_inf
T_LOW = 1.5                  # second height; still Im > 1, inside Omega*


def det_mid(q: int, s: complex, N: int, sign: int) -> complex:
    sb = acb(arb(s.real), arb(s.imag))
    v = E.cert_det_complex_mid(sb, N, sign, q, n_head=4)
    return complex(float(v.real), float(v.imag))


def proxy(q: int, s: complex, N: int) -> complex:
    return det_mid(q, s, N, +1) * det_mid(q, s, N, -1)


def unwrap(qs, raw):
    """Continuous branch of D_q along increasing q, starting in (-pi, pi]."""
    out = []
    prev = None
    for v in raw:
        if prev is None:
            w = v
        else:
            w = v + 2 * math.pi * round((prev - v) / (2 * math.pi))
        out.append(w)
        prev = w
    return out


def fit_slope(xs, ys):
    """Least squares y = a + b x; returns (b, a, max|resid|)."""
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    b = sxy / sxx
    a = my - b * mx
    r = max(abs(y - (a + b * x)) for x, y in zip(xs, ys))
    return b, a, r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--N", type=int, default=32)
    ap.add_argument("--qs", default="12,14,16,18,20,22,26,30,34,40")
    ap.add_argument("--qs-hi", default="12,16,20,24,28,32,36,40")
    ap.add_argument("--out", default="u1phi.json")
    a = ap.parse_args()
    ctx.prec = 400

    qs_lo = [int(x) for x in a.qs.split(",")]
    qs_hi = [int(x) for x in a.qs_hi.split(",")]
    doc = {"N": a.N, "t_low": T_LOW, "t_phys": T_PHYS, "rows": [], "ctrl": []}

    # ---- control: arg of the proxy at real s > 1, where Z_q(s) > 0 ----
    print("=== control: arg P_q at real s > 1 (must be ~0) ===", flush=True)
    for q in sorted(set(qs_lo) | set(qs_hi)):
        t0 = time.time()
        p = proxy(q, complex(2.0, 0.0), a.N)
        row = {"q": q, "s": [2.0, 0.0], "abs": abs(p), "arg": cmath.phase(p),
               "wall": time.time() - t0}
        doc["ctrl"].append(row)
        print(f"  q={q:3d}  |P|={abs(p):.7f}  arg P={cmath.phase(p):+.3e}  "
              f"({row['wall']:.0f}s)", flush=True)

    # ---- the measurement ----
    series = {}
    for tag, t, qs in (("low", T_LOW, qs_lo), ("phys", T_PHYS, qs_hi)):
        print(f"\n=== t = {t} ({tag}) ===", flush=True)
        raw = []
        for q in qs:
            s = complex(0.5, t)
            t0 = time.time()
            p = proxy(q, s, a.N)
            argZ = cmath.phase(p)
            D = -2.0 * argZ
            raw.append(D)
            doc["rows"].append({"tag": tag, "q": q, "t": t,
                                "P_re": p.real, "P_im": p.imag,
                                "absP": abs(p), "argZ": argZ, "D_raw": D,
                                "wall": time.time() - t0})
            print(f"  q={q:3d}  |P|={abs(p):.6e}  argZ={argZ:+.6f}  "
                  f"D_raw={D:+.6f}  ({time.time()-t0:.0f}s)", flush=True)
        # bring into (-pi,pi] then unwrap in q
        raw0 = [((v + math.pi) % (2 * math.pi)) - math.pi for v in raw]
        D = unwrap(qs, raw0)
        xs = [math.log(q) for q in qs]
        beta, c0, resid = fit_slope(xs, D)
        alpha = 1.0 - beta / (2.0 * t)
        series[tag] = {"t": t, "qs": qs, "D_wrapped": raw0, "D_unwrapped": D,
                       "beta": beta, "intercept": c0, "max_resid": resid,
                       "alpha": alpha, "exponent_at_sigma2": -3.0 * alpha,
                       "beta_over_2t": beta / (2.0 * t),
                       "max_step_rad": max(abs(D[i + 1] - D[i])
                                           for i in range(len(D) - 1))}
        print(f"  fit: D = {c0:+.4f} + {beta:+.4f} log q   (max resid {resid:.4f})")
        print(f"  beta/(2t) = {beta/(2*t):+.4f}   alpha = {alpha:+.4f}   "
              f"exponent at sigma=2:  {-3*alpha:+.4f}   (prediction: -3)")
        print(f"  max unwrap step = {series[tag]['max_step_rad']:.4f} rad "
              f"(must be < pi = 3.1416 for the branch to be safe)")

    doc["series"] = series
    if "low" in series and "phys" in series:
        bl, bp = series["low"]["beta"], series["phys"]["beta"]
        doc["ansatz_check"] = {
            "beta_low": bl, "beta_phys": bp,
            "ratio_measured": bp / bl if bl else None,
            "ratio_predicted_by_ansatz": T_PHYS / T_LOW,
        }
        print(f"\n=== ansatz check: beta must be proportional to t ===")
        print(f"  beta(t={T_LOW})={bl:+.4f}  beta(t={T_PHYS:.4f})={bp:+.4f}")
        print(f"  ratio measured = {bp/bl if bl else float('nan'):+.4f}   "
              f"predicted = {T_PHYS/T_LOW:+.4f}")

    with open(a.out, "w") as f:
        json.dump(doc, f, indent=1, default=str)
    print("\nwrote", a.out)


if __name__ == "__main__":
    main()
