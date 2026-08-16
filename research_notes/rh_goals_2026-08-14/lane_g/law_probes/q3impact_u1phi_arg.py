#!/usr/bin/env python3
"""q3impact_u1phi_arg.py -- LAW_U1PHI_TEST sec.4 uses D_q(t) = -2 arg P_q(1/2+it).
Since Z_S = P_q / det(1-K_q), the correct statistic is
    D_q^corr = -2 arg Z_S = D_q^repo + 2 arg det(1-K_q)(1/2+it).
Recompute the sec.4.2 series, the sec.4.3 spans, the sec.4.4 LSQ/endpoint slopes
beta(t), and the two-height exponent -3*alpha, with the correction applied.
D_q^repo values are the BANKED tables of LAW_U1PHI_TEST sec.4.2 (read from
u1phi.json when present, else the note's tabulated values).
Writes only its own .json/.log.
"""
import json, os, math
import mpmath as mp

mp.mp.dps = 40
HERE = os.path.dirname(os.path.abspath(__file__))


def b_of(q):
    L = 2 * mp.cos(mp.pi / q)
    return (2 - L) / (2 + L)


def detK(q, s, nmax=200):
    b, p = b_of(q), mp.mpc(1)
    for n in range(nmax):
        t = mp.power(b, s + n)
        p *= (1 - t)
        if abs(t) < mp.mpf(10) ** -45:
            break
    return p


T15 = 1.5
TINF = 7.0673625708673465
# banked D_q^repo from LAW_U1PHI_TEST sec.4.2
SER = {
    "1.5": ([12, 14, 16, 18, 20, 22, 26, 30, 34, 40],
            [1.384, 0.918, 0.374, -0.044, -0.267, -0.344, -0.275, -0.096, 0.107, 0.397]),
    "t_inf": ([12, 16, 20, 24, 28, 32, 36, 40],
              [4.061, 2.860, 2.602, 2.472, 3.276, 2.037, 2.117, 2.761]),
}
TS = {"1.5": T15, "t_inf": TINF}


def lsq(qs, ys):
    xs = [math.log(q) for q in qs]
    n = len(xs); mx = sum(xs) / n; my = sum(ys) / n
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / \
           sum((x - mx) ** 2 for x in xs)


def endpt(qs, ys):
    return (ys[-1] - ys[0]) / (math.log(qs[-1]) - math.log(qs[0]))


out = {"note": "D_q^corr = D_q^repo + 2 arg det(1-K_q)(1/2+it)", "series": {}}
res = {}
for key, (qs, ds) in SER.items():
    t = TS[key]
    corr, args = [], []
    for q, d in zip(qs, ds):
        a = float(mp.arg(detK(q, mp.mpc(mp.mpf("0.5"), mp.mpf(repr(t))))))
        args.append(a)
        corr.append(d + 2 * a)
    out["series"][key] = {
        "t": t, "q": qs, "D_repo": ds,
        "arg_detK": args, "two_arg_detK": [2 * a for a in args],
        "D_corrected": corr,
        "span_repo": max(ds) - min(ds), "span_corr": max(corr) - min(corr),
        "null_swing_2t_log": 2 * t * math.log(qs[-1] / qs[0]),
        "beta_lsq_repo": lsq(qs, ds), "beta_lsq_corr": lsq(qs, corr),
        "beta_endpt_repo": endpt(qs, ds), "beta_endpt_corr": endpt(qs, corr),
    }
    res[key] = out["series"][key]

# two-height solve: beta(t) = 2t(1-alpha) + delta
for tag in ["lsq", "endpt"]:
    b1 = res["1.5"]["beta_%s_corr" % tag]; b2 = res["t_inf"]["beta_%s_corr" % tag]
    r1 = res["1.5"]["beta_%s_repo" % tag]; r2 = res["t_inf"]["beta_%s_repo" % tag]
    def solve(x1, x2):
        oma = (x2 - x1) / (2 * (TINF - T15))          # 1 - alpha
        delta = x1 - 2 * T15 * oma
        return {"one_minus_alpha": oma, "alpha": 1 - oma,
                "delta": delta, "exponent_minus3alpha": -3 * (1 - oma)}
    out.setdefault("two_height", {})[tag] = {"repo": solve(r1, r2),
                                             "corrected": solve(b1, b2)}
    out["two_height"][tag]["beta_ratio_repo"] = r2 / r1
    out["two_height"][tag]["beta_ratio_corrected"] = b2 / b1

json.dump(out, open(os.path.join(HERE, "q3impact_u1phi_arg.json"), "w"),
          indent=1, default=str)
print(json.dumps(out, indent=1, default=str))
