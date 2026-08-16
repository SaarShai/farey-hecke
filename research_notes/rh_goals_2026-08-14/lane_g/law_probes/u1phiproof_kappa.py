#!/usr/bin/env python3
"""
u1phiproof_kappa.py -- LANE G, (U1-phi) proof route: the assembled kernel.

Uses the Eisenstein-constant-term phi_q of u1phiproof_eisenstein.py together
with the EXACT elliptic factor

    E_q(s) = prod_{k=0}^{q-1} sin(pi (s+k)/q)^{(q-2k-1)/q}

(no use of the HEURISTIC Lemma U1-4b asymptotic) to measure the q-dependence
of the product |phi_q(s) E_q(s)|, which is the only q-dependent part of Teo's
functional-equation kernel kappa_q(s) = Z_{G_q}(1-s)/Z_{G_q}(s)
(LAW_U1_GROWTH.md Sec 3.1: every other factor is q-independent except the
Barnes bracket, whose q-dependence is only in the exponent (1-2/q)/2 and is
therefore an O(1) convergent factor, log-log slope 0).

(U1-phi-a) is exactly the assertion  |phi_q E_q| = O(1)  at Re s = 2.
The U2b-forced version is the same at Re s = sigma_0 >= 3.05.

Also part D: the tail ratio of the phi_q Dirichlet series, which upgrades the
real-s positivity lower bound to a lower bound valid for all |t| <= t_inf+1.
"""
import json, math
from mpmath import mp, mpf, mpc, sin, pi, fabs, gamma, sqrt, exp, log

mp.dps = 30
import importlib.util, os
spec = importlib.util.spec_from_file_location(
    "eis", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "u1phiproof_eisenstein.py"))
eis = importlib.util.module_from_spec(spec); spec.loader.exec_module(eis)


def E_q(q, s):
    tot = mpc(0)
    for k in range(q):
        e = mpf(q - 2 * k - 1) / q
        tot += e * log(sin(pi * (s + k) / q))
    return exp(tot)


def tail_ratio(classes, sigma):
    ks = sorted(classes.keys())
    c1 = ks[0]
    lead = mpf(c1) ** (-2 * sigma) * len(classes[c1][1])
    tail = sum(mpf(len(classes[c][1])) * mpf(c) ** (-2 * sigma) for c in ks[1:])
    return float(tail / lead)


def main():
    tinf = mpf('7.0673625708673465')
    out = {"description": "|phi_q E_q| = the q-dependent part of Teo's kappa_q",
           "note": "E_q evaluated EXACTLY from the sine product, not via Lemma U1-4b"}
    qs = [12, 16, 20, 24, 30, 40, 60, 100]
    rows = {}
    for name, s in (("s=2+i t_inf", mpc(2, tinf)),
                    ("s=3.5+i t_inf", mpc('3.5', tinf)),
                    ("s=1.05+i t_inf", mpc('1.05', tinf)),
                    ("s=0.75+i t_inf", mpc('0.75', tinf))):
        rr = []
        for q in qs:
            lam, cls, _ = eis.enumerate_c_spectrum(q)
            ph = eis.phi_trunc(cls, s)
            ee = E_q(q, s)
            rr.append({"q": q, "abs_phi": float(fabs(ph)),
                       "abs_E": float(fabs(ee)),
                       "abs_phi_E": float(fabs(ph * ee))})
        xs = [math.log(r["q"]) for r in rr]
        for key in ("abs_phi", "abs_E", "abs_phi_E"):
            ys = [math.log(r[key]) for r in rr]
            n = len(xs); mx = sum(xs)/n; my = sum(ys)/n
            sl = sum((x-mx)*(y-my) for x, y in zip(xs, ys))/sum((x-mx)**2 for x in xs)
            rows.setdefault(name, {})[key + "_slope"] = sl
        rows[name]["data"] = rr
        rows[name]["U1phi_requires_phi_slope"] = float(1 - 2 * s.real)
        rows[name]["U1phi_requires_phiE_slope"] = 0.0
    out["kernel"] = rows

    # ---- part D: uniform tail ratio of the phi Dirichlet series
    td = []
    for q in [5, 7, 12, 20, 40, 100]:
        lam, cls, _ = eis.enumerate_c_spectrum(q)
        td.append({"q": q, "c_min": sorted(cls)[0],
                   "tail_ratio_sigma2": tail_ratio(cls, mpf(2)),
                   "tail_ratio_sigma3.5": tail_ratio(cls, mpf('3.5'))})
    out["tail_ratio"] = td

    # ---- part E: worst case over the t-window |t| <= t_inf+1, sigma = 2 and 3.5
    win = []
    for sigma in (mpf(2), mpf('3.5')):
        for q in [12, 40, 100]:
            lam, cls, _ = eis.enumerate_c_spectrum(q)
            vals = []
            N = 81
            for j in range(N):
                t = -(tinf + 1) + 2 * (tinf + 1) * mpf(j) / (N - 1)
                vals.append(float(fabs(eis.phi_trunc(cls, mpc(sigma, t)))))
            win.append({"sigma": float(sigma), "q": q,
                        "min_abs_phi_over_window": min(vals),
                        "max_abs_phi_over_window": max(vals),
                        "required_if_U1phi_a": float(mpf(q) ** (-(2 * sigma - 1)))})
    out["t_window"] = win

    print(json.dumps(out, indent=1, default=str))
    with open(__file__.replace('.py', '.json'), 'w') as f:
        json.dump(out, f, indent=1, default=str)


if __name__ == "__main__":
    main()
