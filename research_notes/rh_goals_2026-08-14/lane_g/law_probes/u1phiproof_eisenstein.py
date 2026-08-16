#!/usr/bin/env python3
"""
u1phiproof_eisenstein.py  --  LANE G, (U1-phi) proof route 3.

Computes the scattering determinant phi_q(s) of the Hecke triangle group
G_q = <S, T_lam>, lam = 2 cos(pi/q), DIRECTLY from the Eisenstein constant
term, via the classical allowed-moduli Dirichlet series

    phi_q(s) = sqrt(pi) * Gamma(s-1/2)/Gamma(s) * sum_{c' in C_q} N_q(c') c'^{-2s}

    C_q  = { c' = lam_q * c : c the lower-left entry of some gamma in G_q, c>0 }
    N_q(c') = # { d mod c' : (a b ; c' d) in sigma^-1 G_q sigma }   (>= 0 integers)

sigma = diag(lam^{1/2}, lam^{-1/2}) scales the width-lam cusp at infinity to
width 1; it multiplies every lower-left entry by lam and leaves d alone.
Reference for the formula: Iwaniec, *Spectral Methods of Automorphic Forms*,
Thm 3.4 / eq (3.21); it is the same import the repo already uses in
lane_g/M1F_EISENSTEIN_DERIVATION.md (3.2).

VALIDATION (the point of the script):
  q=3 (lam=1, PSL(2,Z))   phi = g(s)                          , g = sqrt(pi)G(s-1/2)zeta(2s-1)/(G(s)zeta(2s))
  q=4 (lam=sqrt2, p=2)    phi = g(s)(1+2^{1-s})/(1+2^s)       [M1F (3.6)]
  q=6 (lam=sqrt3, p=3)    phi = g(s)(1+3^{1-s})/(1+3^s)       [M1F (3.6)]

DELIVERABLE: the q-dependence of |phi_q(s)| on Re s > 1, tested against the
(U1-phi-a) prediction |phi_q(2+it)| = O(q^{-3}) and the U2b-forced
|phi_q(3.5+it)| = O(q^{-6}).

Float / mpmath only.  NON-RIGOROUS: series truncated at c' <= CMAX, group
enumerated by BFS with an entry-norm bound.  No interval arithmetic.
"""
import json, math, sys
from mpmath import mp, mpf, mpc, gamma, sqrt, pi, zeta, fabs

mp.dps = 30

# ----------------------------------------------------------------- enumeration
def enumerate_c_spectrum(q, norm_bound=260.0, cmax=26.0, tol=1e-7):
    """BFS over G_q = <S, T_lam>; returns dict c' -> set of d-residues mod c'."""
    lam = 2.0 * math.cos(math.pi / q) if q is not None else 2.0
    S = (0.0, -1.0, 1.0, 0.0)
    T = (1.0, lam, 0.0, 1.0)
    Ti = (1.0, -lam, 0.0, 1.0)
    gens = (S, T, Ti)

    def mul(X, Y):
        return (X[0]*Y[0] + X[1]*Y[2], X[0]*Y[1] + X[1]*Y[3],
                X[2]*Y[0] + X[3]*Y[2], X[2]*Y[1] + X[3]*Y[3])

    def canon(X):
        # PSL: identify X and -X.  Sign-normalise on first entry above tol.
        for v in X:
            if abs(v) > tol:
                if v < 0:
                    return tuple(-u for u in X)
                return X
        return X

    def key(X):
        return tuple(round(v, 6) for v in canon(X))

    I = (1.0, 0.0, 0.0, 1.0)
    seen = {key(I)}
    frontier = [I]
    classes = {}          # rounded c' -> (c' value, set of rounded d residues)
    n_elts = 1
    while frontier:
        nxt = []
        for X in frontier:
            for g in gens:
                Y = mul(X, g)
                if max(abs(v) for v in Y) > norm_bound:
                    continue
                k = key(Y)
                if k in seen:
                    continue
                seen.add(k)
                n_elts += 1
                nxt.append(Y)
                # record the double coset
                a, b, c, d = canon(Y)
                if abs(c) <= tol:
                    continue
                if c < 0:
                    a, b, c, d = -a, -b, -c, -d
                cp = lam * c                    # scaled lower-left entry
                if cp > cmax:
                    continue
                ck = round(cp, 6)
                dr = d % cp
                if cp - dr < 1e-6:
                    dr = 0.0
                bucket = classes.setdefault(ck, (cp, set()))
                bucket[1].add(round(dr, 5))
        frontier = nxt
    return lam, classes, n_elts


def phi_trunc(classes, s):
    """sqrt(pi) G(s-1/2)/G(s) * sum N(c') c'^{-2s}."""
    tot = mpc(0)
    for ck, (cp, ds) in classes.items():
        tot += mpf(len(ds)) * mpf(cp) ** (-2 * s)
    return sqrt(pi) * gamma(s - mpf(1) / 2) / gamma(s) * tot


def g_of_s(s):
    return sqrt(pi) * gamma(s - mpf(1) / 2) * zeta(2 * s - 1) / (gamma(s) * zeta(2 * s))


def phi_arith(p, s):
    """M1F (3.6): phi for the arithmetic Hecke group G_q, q=4 (p=2), q=6 (p=3)."""
    return g_of_s(s) * (1 + mpf(p) ** (1 - s)) / (1 + mpf(p) ** s)


# ----------------------------------------------------------------------- main
def main():
    out = {"description": "phi_q via Eisenstein constant term; (U1-phi-a) test",
           "params": {"norm_bound": 260.0, "cmax": 26.0, "mp_dps": mp.dps}}

    # ---- A. validation on the three arithmetic levels
    val = []
    for q, closed in ((3, None), (4, 2), (6, 3)):
        lam, cls, ne = enumerate_c_spectrum(q)
        for sval in (mpf(2), mpf('3.5'), mpc('1.05', '7.0673625708673465'),
                     mpc(2, '7.0673625708673465')):
            got = phi_trunc(cls, sval)
            exp = g_of_s(sval) if closed is None else phi_arith(closed, sval)
            val.append({"q": q, "s": str(sval), "phi_series": str(got),
                        "phi_closed": str(exp),
                        "rel_err": float(fabs(got - exp) / fabs(exp))})
        # c-spectrum report
        cs = sorted(cls.items())[:6]
        val.append({"q": q, "lam": lam, "n_elts": ne,
                    "c_spectrum_head": [[c, len(d)] for c, (c2, d) in cs]})
    out["validation"] = val

    # ---- B. the q-sweep: is |phi_q| = O(q^-3) at Re s = 2, O(q^-6) at 3.5?
    tinf = mpf('7.0673625708673465')
    heights = {"s=2": mpf(2),
               "s=2+i t_inf": mpc(2, tinf),
               "s=3.5": mpf('3.5'),
               "s=3.5+i t_inf": mpc('3.5', tinf),
               "s=1.05+i t_inf": mpc('1.05', tinf)}
    qs = [3, 4, 5, 6, 7, 8, 10, 12, 16, 20, 24, 30, 40, 60, 100]
    sweep = {k: [] for k in heights}
    cmin = []
    for q in qs:
        lam, cls, ne = enumerate_c_spectrum(q)
        ks = sorted(cls.keys())
        cmin.append({"q": q, "lam": lam, "c_min": ks[0],
                     "N(c_min)": len(cls[ks[0]][1]),
                     "c_2nd": ks[1] if len(ks) > 1 else None,
                     "N(c_2nd)": len(cls[ks[1]][1]) if len(ks) > 1 else None,
                     "n_c_values": len(ks), "n_elts": ne})
        for name, sval in heights.items():
            v = phi_trunc(cls, sval)
            sweep[name].append({"q": q, "abs_phi": float(fabs(v)),
                                "arg_phi": float(mp.arg(v))})
    out["c_min_report"] = cmin
    out["sweep"] = sweep

    # ---- C. log-log slopes of |phi_q| in q over q = 12..100
    slopes = {}
    for name, rows in sweep.items():
        sub = [r for r in rows if r["q"] >= 12]
        xs = [math.log(r["q"]) for r in sub]
        ys = [math.log(r["abs_phi"]) for r in sub]
        n = len(xs)
        mx, my = sum(xs) / n, sum(ys) / n
        num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
        den = sum((x - mx) ** 2 for x in xs)
        slopes[name] = {"lsq_slope_q12_100": num / den,
                        "endpoint_slope": (ys[-1] - ys[0]) / (xs[-1] - xs[0]),
                        "phi_q12": math.exp(ys[0]), "phi_q100": math.exp(ys[-1])}
    out["slopes"] = slopes

    print(json.dumps(out, indent=1, default=str))
    with open(__file__.replace('.py', '.json'), 'w') as f:
        json.dump(out, f, indent=1, default=str)


if __name__ == "__main__":
    main()
