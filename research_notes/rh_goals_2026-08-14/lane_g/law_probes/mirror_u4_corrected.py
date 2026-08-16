#!/usr/bin/env python3
"""
mirror_u4_corrected.py -- LANE G: the mirror test with the CORRECTED Teo kernel.

THE TRANSCRIPTION ERROR.  mirror_u4.py's K_q() implements Teo's Barnes bracket
(Prop. 2.5, arXiv:1901.07898v2) as

    [ (2pi)^{2s-1} * barnesg(s)^2 * Gamma(1-s) / (barnesg(1-s)^2 * Gamma(s)) ]^{|X|/2pi}

identifying Teo's Gamma_2 with mpmath's `barnesg` (the Barnes G-function).
That identification is WRONG -- they are RECIPROCAL:

    Barnes G :  G(s+1)      = Gamma(s) * G(s)          -> G(s) ~ s   at s -> 0
    Teo   G_2:  Gamma_2(s)  = Gamma(s) * Gamma_2(s+1)  -> simple POLE, residue 1

(Teo p. 5 definition; the recursion is his displayed relation
"Gamma_2(s) = Gamma(s) Gamma_2(s+1)", and he states on p. 10 that "Gamma_2(s)
has a simple pole of order 1 at s = 0 with residue one".  Both normalise to
Gamma_2(1) = G(1) = 1.)  Hence

                    Gamma_2(s) = 1 / G(s).

So the Gamma_2^2 ratio in the bracket must be INVERTED relative to barnesg:

    [ (2pi)^{2s-1} * barnesg(1-s)^2 * Gamma(1-s) / (barnesg(s)^2 * Gamma(s)) ]^{|X|/2pi}

This is a near-inversion of the whole bracket (the G^2 ratio dominates the
Gamma and (2pi) pieces by many orders), which is exactly why the back-solved
diagnosis in LAW_MIRROR_Q3_DISCRIMINATOR.md read as "flip the exponent sign"
and still left a residual factor of order 1.

Everything else in the assembly is confirmed verbatim against the source.

Run: /Users/za/miniforge3/envs/pari-arb/bin/python3 mirror_u4_corrected.py
"""
from __future__ import annotations
import json, math, sys, time
from pathlib import Path

REPO = Path("/Users/za/Documents/farey-hecke")
sys.path.insert(0, str(REPO / ".worktrees/aletheia-restore/code"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import zeta_cert_rosen as ODD                                       # noqa: E402
import zeta_cert_rosen_even as EVEN                                 # noqa: E402
from flint import acb, arb, ctx                                     # noqa: E402
from mpmath import (mp, mpf, mpc, gamma, sqrt, pi, sin, tan,        # noqa: E402
                    barnesg, fabs, power, zeta)

from mirror_u4 import E_q, K_q as K_q_old                           # noqa: E402

mp.dps = 30
TINF = mpf('7.0673625708673465')
SIGMAS = ('1.25', '1.40', '1.50')


# ------------------------------------------------------------------ the kernel
def barnes_bracket(s, q, invert_G):
    """Teo's [ (2pi)^{2s-1} Gamma_2(s)^2 Gamma(1-s) / (Gamma_2(1-s)^2 Gamma(s)) ]^{|X|/2pi}

    |X_q|/2pi = (1 - 2/q)/2 for signature (0;1;2,q).
    invert_G=True  -> Gamma_2 = 1/G   (CORRECT, this file)
    invert_G=False -> Gamma_2 = G     (the mirror_u4.py transcription)
    """
    g2 = (barnesg(1 - s)**2 / barnesg(s)**2) if invert_G else \
         (barnesg(s)**2 / barnesg(1 - s)**2)
    inner = power(2*pi, 2*s - 1) * g2 * gamma(1 - s) / gamma(s)
    return power(inner, (1 - mpf(2)/q) / 2)


def K_q_corrected(s, q, invert_G=True, tan_branch=+1):
    """kappa_q(s) / phi_q(s) -- every Teo factor except phi, corrected."""
    ex = power(2, -(2*s - 1))                       # e^{C(2s-1)}, C = -log 2
    el2 = power(tan(pi * s / 2), mpf(tan_branch) / 2)
    elq = E_q(s, q)
    bar = barnes_bracket(s, q, invert_G)
    par = gamma(mpf(3)/2 - s) / gamma(s + mpf(1)/2)
    return ex * el2 * elq * bar * par


# ------------------------------------------------------------------- phi exact
def g_of_s(s):
    return sqrt(pi) * gamma(s - mpf(1)/2) * zeta(2*s - 1) / (gamma(s) * zeta(2*s))


def phi_exact(q, s):
    if q == 3:
        return g_of_s(s)
    p = {4: 2, 6: 3}[q]
    return g_of_s(s) * (1 + mpf(p)**(1 - s)) / (1 + mpf(p)**s)


# ------------------------------------------------------------------ proxy side
def P_q(q, s, N):
    mod = ODD if q % 2 else EVEN
    sb = acb(arb(s.real), arb(s.imag))
    a = 1.0
    for sign in (+1, -1):
        v = mod.cert_det_complex_mid(sb, N, sign, q, n_head=4)
        a *= abs(complex(float(v.real), float(v.imag)))
    return a


def main():
    ctx.prec = 400
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 32
    out = {"description": "mirror test with CORRECTED Teo kernel (Gamma_2 = 1/G)",
           "source": "L.-P. Teo, arXiv:1901.07898v2, Prop. 2.5 (p. 7), Thm 2.2 (p. 6)",
           "relation": "P_q(1-s)/P_q(s) == |phi_q(s)| * |K_q(s)|   (U4 + Teo)",
           "params": {"N": N, "prec": 400, "t": float(TINF)},
           "controls": [], "rows": [], "residual_candidates": []}

    # ---- C1: |K_q(1/2+it)| == 1 must still hold (it is blind to the fix)
    for q in (3, 4, 6):
        z = mpc(mpf('0.5'), TINF)
        kn = float(fabs(K_q_corrected(z, q)))
        ko = float(fabs(K_q_old(z, q)))
        out["controls"].append({"q": q, "abs_K_corrected_at_half": kn,
                                "abs_K_old_at_half": ko})
        print(f"C1 q={q}: |K_corr(1/2+it)|={kn:.12f}   |K_old|={ko:.12f}", flush=True)

    # ---- the mirror test
    for q in (3, 4, 6):
        for sg in SIGMAS:
            s = complex(float(sg), float(TINF))
            ms = mpc(mpf(sg), TINF)
            t0 = time.time()
            try:
                ps = P_q(q, s, N)
                pm = P_q(q, complex(1 - s.real, -s.imag), N)
            except Exception as exc:                       # noqa: BLE001
                print(f"q={q} sg={sg} DET FAIL {exc!r}"[:160], flush=True)
                continue
            if not (math.isfinite(ps) and math.isfinite(pm)):
                print(f"q={q} sg={sg} non-finite det", flush=True)
                continue
            lhs = pm / ps
            phi = float(fabs(phi_exact(q, ms)))
            kc = float(fabs(K_q_corrected(ms, q)))
            ko = float(fabs(K_q_old(ms, q)))
            row = {"q": q, "sigma": float(sg), "P_at_s": ps, "P_at_1ms": pm,
                   "LHS_ratio": lhs, "abs_phi_exact": phi,
                   "abs_K_corrected": kc, "abs_K_old": ko,
                   "RHS_corrected": phi * kc, "RHS_old": phi * ko,
                   "ratio_corrected": lhs / (phi * kc),
                   "ratio_old": lhs / (phi * ko),
                   "wall_s": time.time() - t0}
            out["rows"].append(row)
            print(f"q={q} sg={sg}: LHS={lhs:.6e} |phi|={phi:.6e} "
                  f"|K_corr|={kc:.6e}  ratio_corr={lhs/(phi*kc):.9f}   "
                  f"(ratio_old={lhs/(phi*ko):.3e})", flush=True)

    # ---- residual diagnosis: named candidates, one at a time
    print("\n=== residual candidates ===", flush=True)
    for row in out["rows"]:
        q, sg = row["q"], row["sigma"]
        ms = mpc(mpf(repr(sg)), TINF)
        phi = row["abs_phi_exact"]
        cand = {"q": q, "sigma": sg, "ratio_base": row["ratio_corrected"]}
        # candidate 1: opposite tan branch (exponent -1/2 instead of +1/2)
        k = float(fabs(K_q_corrected(ms, q, tan_branch=-1)))
        cand["ratio_tan_branch_flipped"] = row["LHS_ratio"] / (phi * k)
        # candidate 2: Gamma_2 = G (i.e. the old bracket) -- for reference
        k = float(fabs(K_q_corrected(ms, q, invert_G=False)))
        cand["ratio_G_not_inverted"] = row["LHS_ratio"] / (phi * k)
        out["residual_candidates"].append(cand)
        print(f"  q={q} sg={sg}: base={cand['ratio_base']:.9f}  "
              f"tanflip={cand['ratio_tan_branch_flipped']:.6e}  "
              f"G_notinv={cand['ratio_G_not_inverted']:.6e}", flush=True)

    rs = [r["ratio_corrected"] for r in out["rows"]]
    if rs:
        worst = max(abs(math.log10(abs(r))) for r in rs)
        out["verdict"] = {"max_abs_log10_ratio_corrected": worst,
                          "identity_holds": bool(worst < 1e-3),
                          "ratio_min": min(rs), "ratio_max": max(rs)}
        print(f"\nVERDICT: max |log10(LHS/RHS)| = {worst:.3e}  "
              f"ratios in [{min(rs):.9f}, {max(rs):.9f}]", flush=True)

    p = __file__.replace('.py', '.json')
    with open(p, 'w') as f:
        json.dump(out, f, indent=1, default=str)
    print("wrote", p)


if __name__ == "__main__":
    main()
