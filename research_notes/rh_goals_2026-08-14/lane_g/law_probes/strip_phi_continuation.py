#!/usr/bin/env python3
"""
strip_phi_continuation.py -- LANE G, TASK A.

Measure |phi_q(sigma + i t)| on the CRUX STRIP sigma in {0.80,0.85,0.90,0.95},
t in {1.5, 3.5, t_inf}, q in {8,12,16,22,30,40,56} -- the (U1-phi-a') target of
lane_g/LAW_U1PHI_PROOF_ROUTE.md Sec 5.1(ii).

The Dirichlet series (2.1) DIVERGES there (abscissa Re s = 1).  The only
continuation available from the c-spectrum is main-term subtraction:

   D(s) = sum_{c'<=X} N(c') c'^{-2s} + C_q X^{2-2s}/(s-1) + eps(s;X),
   C_q  = 1/(pi vol(F_q)) = 1/(pi^2 (1 - 2/q)),
   eps  = int_X^inf t^{-2s} dR(t),   R(t) = A(t) - C_q t^2.

strip_method_validation.py benchmarks eps EXACTLY at q=3 with exact
coefficients (N(c) = totient(c)) out to X = 1e7: eps ~ X^{-(2 sigma - 1)},
and 6 digits at sigma = 0.8 needs X ~ 5e8.

This script does the honest thing at the X the group enumeration can actually
reach, and reports the MEASURED accuracy against the three arithmetic closed
forms on the SAME strip points.

Float / mpmath.  NON-RIGOROUS.  The parent note LAW_U1PHI_PROOF_ROUTE.md is
itself PENDING ADVERSARIAL VERIFICATION; every number here inherits that.
"""
import json, math, sys, time
from mpmath import mp, mpf, mpc, gamma, sqrt, pi, zeta, fabs

mp.dps = 30
TINF = '7.0673625708673465'


def enumerate_c_spectrum(q, norm_bound, cmax, tol=1e-7):
    """BFS over G_q = <S, T_lam>; returns lam, {c' -> (c', set of d residues)}."""
    lam = 2.0 * math.cos(math.pi / q)
    S = (0.0, -1.0, 1.0, 0.0)
    T = (1.0, lam, 0.0, 1.0)
    Ti = (1.0, -lam, 0.0, 1.0)
    gens = (S, T, Ti)

    def mul(X, Y):
        return (X[0]*Y[0] + X[1]*Y[2], X[0]*Y[1] + X[1]*Y[3],
                X[2]*Y[0] + X[3]*Y[2], X[2]*Y[1] + X[3]*Y[3])

    def canon(X):
        for v in X:
            if abs(v) > tol:
                return tuple(-u for u in X) if v < 0 else X
        return X

    def key(X):
        return tuple(round(v, 6) for v in canon(X))

    I = (1.0, 0.0, 0.0, 1.0)
    seen = {key(I)}
    frontier = [I]
    classes = {}
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
                a, b, c, d = canon(Y)
                if abs(c) <= tol:
                    continue
                if c < 0:
                    a, b, c, d = -a, -b, -c, -d
                cp = lam * c
                if cp > cmax:
                    continue
                ck = round(cp, 6)
                dr = d % cp
                if cp - dr < 1e-6:
                    dr = 0.0
                classes.setdefault(ck, (cp, set()))[1].add(round(dr, 5))
        frontier = nxt
    return lam, classes, n_elts


def prefac(s):
    return sqrt(pi) * gamma(s - mpf(1) / 2) / gamma(s)


def phi_cont(classes, s, q, X):
    """Continued phi_q: head sum over c' <= X plus the exact main-term tail."""
    tot = mpc(0)
    for ck, (cp, ds) in classes.items():
        if cp <= X:
            tot += mpf(len(ds)) * mpf(cp) ** (-2 * s)
    Cq = 1 / (pi ** 2 * (1 - mpf(2) / q))
    tail = Cq * mpf(X) ** (2 - 2 * s) / (s - 1)
    return prefac(s) * (tot + tail)


def g_of_s(s):
    return sqrt(pi) * gamma(s - mpf(1)/2) * zeta(2*s - 1) / (gamma(s) * zeta(2*s))


def phi_arith(p, s):
    return g_of_s(s) * (1 + mpf(p) ** (1 - s)) / (1 + mpf(p) ** s)


def counting_check(classes, q, lam, Xs):
    """A(X) vs C_q X^2 -- tests BFS completeness AND the constant simultaneously."""
    Cq = 1.0 / (math.pi ** 2 * (1 - 2.0 / q))
    out = []
    items = sorted(classes.items())
    for X in Xs:
        A = sum(len(d) for ck, (cp, d) in items if cp <= X)
        out.append({"X": X, "A": A, "C_q_X2": Cq * X * X,
                    "ratio": A / (Cq * X * X) if X else None})
    return out


def main():
    NB = float(sys.argv[1]) if len(sys.argv) > 1 else 1200.0
    CM = float(sys.argv[2]) if len(sys.argv) > 2 else 120.0
    sigmas = [mpf('0.80'), mpf('0.85'), mpf('0.90'), mpf('0.95')]
    ts = [mpf('1.5'), mpf('3.5'), mpf(TINF)]
    Xs_trunc = [CM / 2, CM]                     # two truncations -> stability
    qs_arith = [3, 4, 6]
    qs_test = [8, 12, 16, 22, 30, 40, 56]

    out = {"description": "TASK A: |phi_q| on the crux strip sigma in (3/4,1) "
                          "via main-term-subtracted continuation",
           "params": {"norm_bound": NB, "cmax": CM, "mp_dps": mp.dps,
                      "trunc_X": Xs_trunc},
           "caveat": "Parent LAW_U1PHI_PROOF_ROUTE.md is PENDING ADVERSARIAL "
                     "VERIFICATION. All numbers float, non-rigorous.",
           "validation": [], "counting": [], "sweep": {}}

    # ---- A. validation on arithmetic levels, ON THE STRIP
    for q, p in ((3, None), (4, 2), (6, 3)):
        t0 = time.time()
        lam, cls, ne = enumerate_c_spectrum(q, NB, CM)
        out["counting"].append({"q": q, "lam": lam, "n_elts": ne,
                                "rows": counting_check(cls, q, lam,
                                                       [CM/8, CM/4, CM/2, CM])})
        if q == 3:   # exact-coefficient completeness check: N(c) must be totient(c)
            def tot(n):
                r, m = n, n
                f = 2
                while f * f <= m:
                    if m % f == 0:
                        while m % f == 0:
                            m //= f
                        r -= r // f
                    f += 1
                if m > 1:
                    r -= r // m
                return r
            bad = []
            for ck, (cp, ds) in sorted(cls.items()):
                n = int(round(cp))
                if abs(cp - n) < 1e-6 and n <= CM:
                    if len(ds) != tot(n):
                        bad.append([n, len(ds), tot(n)])
            out["bfs_completeness_q3"] = {"n_c_checked": len(cls),
                                          "mismatches": bad[:20],
                                          "n_mismatch": len(bad)}
        for sg in sigmas:
            for t in ts:
                s = mpc(sg, t)
                exact = g_of_s(s) if p is None else phi_arith(p, s)
                row = {"q": q, "sigma": float(sg), "t": float(t),
                       "exact_abs": float(fabs(exact))}
                for X in Xs_trunc:
                    est = phi_cont(cls, s, q, X)
                    row[f"est_abs_X{int(X)}"] = float(fabs(est))
                    row[f"rel_err_X{int(X)}"] = float(fabs(est - exact) / fabs(exact))
                out["validation"].append(row)
        print(f"q={q} done  n_elts={ne}  {time.time()-t0:.0f}s", flush=True)

    for r in out["validation"]:
        print(f"  q={r['q']} s={r['sigma']}+{r['t']:.4f}i  |phi|exact={r['exact_abs']:.6f} "
              f" relerr(X={int(Xs_trunc[0])})={r[f'rel_err_X{int(Xs_trunc[0])}']:.2e}"
              f"  relerr(X={int(CM)})={r[f'rel_err_X{int(CM)}']:.2e}", flush=True)

    worst = max(r[f"rel_err_X{int(CM)}"] for r in out["validation"])
    out["worst_arith_rel_err"] = worst
    out["digits_validated"] = -math.log10(worst)
    print(f"\nWORST arithmetic relative error on the strip at X={CM}: {worst:.3e} "
          f"({-math.log10(worst):.2f} digits)\n", flush=True)

    # ---- B. the q-sweep on the strip (labelled by the accuracy just measured)
    for q in qs_test:
        t0 = time.time()
        lam, cls, ne = enumerate_c_spectrum(q, NB, CM)
        out["counting"].append({"q": q, "lam": lam, "n_elts": ne,
                                "rows": counting_check(cls, q, lam,
                                                       [CM/8, CM/4, CM/2, CM])})
        for sg in sigmas:
            for t in ts:
                s = mpc(sg, t)
                k = f"sigma={float(sg)},t={float(t):.4f}"
                rec = {"q": q}
                for X in Xs_trunc:
                    v = phi_cont(cls, s, q, X)
                    rec[f"abs_X{int(X)}"] = float(fabs(v))
                out["sweep"].setdefault(k, []).append(rec)
        print(f"q={q} sweep done  n_elts={ne}  {time.time()-t0:.0f}s", flush=True)

    # ---- C. q-slopes, at both truncations (stability = the real error bar)
    slopes = {}
    for k, rows in out["sweep"].items():
        e = {}
        for X in Xs_trunc:
            xs = [math.log(r["q"]) for r in rows]
            ys = [math.log(r[f"abs_X{int(X)}"]) for r in rows]
            n = len(xs)
            mx, my = sum(xs)/n, sum(ys)/n
            num = sum((a-mx)*(b-my) for a, b in zip(xs, ys))
            den = sum((a-mx)**2 for a in xs)
            e[f"slope_X{int(X)}"] = num/den
        sg = float(k.split(',')[0].split('=')[1])
        e["required_exponent"] = -(2*sg - 1)
        e["trunc_spread"] = abs(e[f"slope_X{int(Xs_trunc[1])}"] -
                                e[f"slope_X{int(Xs_trunc[0])}"])
        slopes[k] = e
    out["slopes"] = slopes
    print("=== q-slope of |phi_q| on the strip (q = 8..56) ===")
    for k, e in slopes.items():
        print(f"  {k}:  slope(X={int(Xs_trunc[0])})={e[f'slope_X{int(Xs_trunc[0])}']:+.4f}"
              f"  slope(X={int(CM)})={e[f'slope_X{int(CM)}']:+.4f}"
              f"  spread={e['trunc_spread']:.4f}   REQUIRED={e['required_exponent']:+.2f}")

    with open(__file__.replace('.py', '.json'), 'w') as f:
        json.dump(out, f, indent=1, default=str)
    print("\nwrote", __file__.replace('.py', '.json'))


if __name__ == "__main__":
    main()
