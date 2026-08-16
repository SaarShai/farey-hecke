#!/usr/bin/env python3
"""q3impact_detK_factor.py -- quantify |det(1-K_q)(s)| at every point where this
lane has quoted a MAGNITUDE of a transfer-operator determinant.

Reads nothing but banked receipts (u1_sup*.json, u1_guard_extended.json,
q3diag_detK.json); writes only q3impact_detK_factor.{json,log}.

det(1 - K_s) = prod_{n>=0} (1 - b_q^{s+n});  even q: b_q = (2-lam_q)/(2+lam_q).
Source: MMS arXiv:0912.2236 (see LAW_Q3_BRANCH_DIAGNOSIS.md sec.1.2).
"""
import json, os, math
import mpmath as mp

mp.mp.dps = 40
HERE = os.path.dirname(os.path.abspath(__file__))
out = {}


def lam(q):
    return 2 * mp.cos(mp.pi / q)


def b_even(q):
    L = lam(q)
    return (2 - L) / (2 + L)


# odd-q b_q from the banked orbit-product receipt
BANKED = json.load(open(os.path.join(HERE, "q3diag_detK.json")))["b_q"]


def b_of(q):
    if str(q) in BANKED:
        return mp.mpf(repr(BANKED[str(q)]["b_q"]))
    if q % 2 == 0:
        return b_even(q)
    raise ValueError("odd q %d not banked" % q)


def detK(q, s, nmax=200):
    b = b_of(q)
    p = mp.mpf(1)
    s = mp.mpmathify(s)
    for n in range(nmax):
        term = mp.power(b, s + n)
        p *= (1 - term)
        if abs(term) < mp.mpf(10) ** (-45):
            break
    return p


# ---------------------------------------------------------------- b_q table
out["b_q"] = {}
for q in [3, 4, 5, 6, 7, 8, 12, 16, 22, 30, 40, 56, 72, 100]:
    b = b_of(q)
    out["b_q"][q] = {
        "b_q": float(b),
        "log_1_over_b": float(mp.log(1 / b)),
        "im_zero_spacing_2pi_over_log": float(2 * mp.pi / mp.log(1 / b)),
    }

# ------------------------------------------- U1 guard: dU ring around s_inf
s_inf = mp.mpf("0.25") + 1j * mp.mpf("7.067362570867346")
s_inf = mp.mpc(mp.mpf("0.25"), mp.mpf("7.067362570867346"))
R = mp.mpf("0.25")
ring = {}
for j in range(8):
    ring[j] = s_inf + R * mp.exp(2j * mp.pi * j / 8)

rows = []
for q in [12, 16, 22, 30, 40, 56, 72, 100]:
    for j in range(8):
        s = ring[j]
        D = detK(q, s)
        rows.append({
            "q": q, "point": "dU_%d" % j,
            "re": float(mp.re(s)), "im": float(mp.im(s)),
            "abs_detK": float(abs(D)),
            "one_over_abs_detK": float(1 / abs(D)),
        })
out["u1_guard_ring"] = rows

# distance from Re s = 0 ring point to nearest det(1-K_q) zero (n=0 line)
z = []
for q in [12, 16, 22, 30, 40, 56, 72, 100]:
    b = b_of(q)
    sp = 2 * mp.pi / mp.log(1 / b)
    t = mp.im(s_inf)
    k = mp.nint(t / sp)
    z.append({"q": q, "spacing": float(sp), "k": int(k),
              "nearest_zero_im": float(k * sp),
              "dist": float(abs(t - k * sp)),
              "abs_detK_at_dU4": float(abs(detK(q, mp.mpc(0, t))))})
out["dU4_zero_proximity"] = z

# ------------------------------- U1 sec.7.2 Euler control points (Re s > 1)
ctrl = []
for q in [12, 16, 22, 30, 40]:
    for s, tag in [(mp.mpf(2), "2.0"),
                   (mp.mpc(mp.mpf("1.5"), mp.mpf("7.0674")), "1.5+7.0674i")]:
        D = detK(q, s)
        ctrl.append({"q": q, "s": tag, "abs_detK": float(abs(D)),
                     "one_minus_absdetK": float(1 - abs(D))})
out["u1_72_control_points"] = ctrl

# --------------------------------------------- U2b: Re s >= 3.5 uniform bnd
u2b = []
bmax_q, bmax = None, mp.mpf(0)
for q in range(5, 201):
    b = b_of(q) if (q % 2 == 0 or str(q) in BANKED) else None
    if b is None:
        continue
    if b > bmax:
        bmax, bmax_q = b, q
for q in [5, 6, 7, 8, 12, 100]:
    b = b_of(q)
    lo = float(mp.nprod(lambda n: 1 - mp.power(b, mp.mpf("3.5") + n), [0, 60]))
    hi = float(mp.nprod(lambda n: 1 + mp.power(b, mp.mpf("3.5") + n), [0, 60]))
    u2b.append({"q": q, "b_q": float(b), "min_absdetK_Re3.5": lo,
                "max_absdetK_Re3.5": hi, "max_rel_dev": max(abs(1 - lo), abs(hi - 1))})
out["u2b_Re3.5"] = {"worst_b_q_over_q_ge_5": {"q": bmax_q, "b_q": float(bmax)},
                    "rows": u2b}

# ------------------------------------------------ G_5 flagship / resonances
g5 = []
for s in [mp.mpc("0.45", "7.0674"), mp.mpc("0.5", "7.0674"),
          mp.mpc("0.4", "7.0"), mp.mpc("0.45", "0"), mp.mpc("2.0", "0")]:
    D = detK(5, s)
    g5.append({"s": [float(mp.re(s)), float(mp.im(s))],
               "abs_detK5": float(abs(D)), "dev_from_1": float(abs(D) - 1)})
out["g5_points"] = g5

# --------------------------- d log|det(1-K_q)| / d log q at the ring points
slope = []
for j in [0, 3, 4, 6]:
    s = ring[j]
    qs = [12, 16, 22, 30, 40, 56, 72, 100]
    xs = [math.log(q) for q in qs]
    ys = [math.log(float(abs(detK(q, s)))) for q in qs]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sl = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    slope.append({"point": "dU_%d" % j, "re": float(mp.re(s)),
                  "dlog_absdetK_dlog_q": sl,
                  "log_absdetK": dict(zip(map(str, qs), ys))})
out["dlog_slopes"] = slope

with open(os.path.join(HERE, "q3impact_detK_factor.json"), "w") as f:
    json.dump(out, f, indent=1, default=str)
print(json.dumps(out, indent=1, default=str))
