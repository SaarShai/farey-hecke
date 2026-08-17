#!/usr/bin/env python3
"""
r4_defect.py -- LANE G, R4: defect lower bound for the theta-group scattering
coefficient phi_infty near t0 = gamma_1/2 (LAW_HEJHAL_S7_EXTRACT.md sec.4 R4,
LAW_RATE_MEASURE.md sec.phi_infty for the normalization).

phi_infty(s) = g(s) / (4^s - 1),
g(s) = sqrt(pi) * Gamma(s - 1/2) * zeta(2s - 1) / ( Gamma(s) * zeta(2s) )

EXACTLY the normalization of law_probes/rate_measure.py's phi_infty (itself
LAW_ANCHOR_T1_THETA.md eq 3.1 / C5) and agp_phi.py's _g_of_s -- reused
as-is, not re-derived, per task instructions.

Pure mpmath, self-contained (no flint/arb dependency needed -- g(s) is an
elementary closed form).

Run with: /Users/za/miniforge3/envs/pari-arb/bin/python3 r4_defect.py
"""
from __future__ import annotations

import json
from pathlib import Path

from mpmath import mp, mpf, mpc, gamma, sqrt, pi, zeta, findroot

OUT_DIR = Path(__file__).resolve().parent
MP_DPS = 50


def set_prec(dps=MP_DPS):
    mp.dps = dps


def g_of_s(s):
    return sqrt(pi) * gamma(s - mpf(1) / 2) * zeta(2 * s - 1) / (gamma(s) * zeta(2 * s))


def phi_infty(s):
    X = mpc(4) ** s
    return g_of_s(s) / (X - 1)


# --------------------------------------------------------------- constants
set_prec()
GAMMA1 = mpf("14.134725141734693790457251983562470270784257115699243175685567460149")
RHO1_HALF = mpc(mpf(1) / 4, GAMMA1 / 2)   # rho_1 / 2 = 1/4 + i*gamma_1/2  (pole of phi_infty)
T0 = GAMMA1 / 2                            # t0 on the CRITICAL LINE 1/2+it -> the analogous
                                            # height; note the pole itself sits at Re=1/4,
                                            # see sec.0 GATE-3 note below.


# ============================================================ Step 1: regime
def check_line_unitarity(npts=9, tspan=mpf("0.3")):
    """|phi_infty(1/2+it)| on the line, away from any pole -- is it == 1?"""
    rows = []
    for i in range(npts):
        t = T0 - tspan + 2 * tspan * i / (npts - 1)
        s = mpc(mpf(1) / 2, t)
        val = abs(phi_infty(s))
        rows.append((float(t), val))
    return rows


# ============================================================ Step 1b: pole check
def check_pole(rs=(mpf("1e-2"), mpf("1e-3"), mpf("1e-4"), mpf("1e-5"))):
    """|phi_infty(s0+r)| near s0 = rho_1/2 = 1/4+i*gamma_1/2 for phi_infty's OWN pole
    (per rate_measure.py GATE 3: phi_infty has a pole at rho_1/2, Re=1/4, not on the
    critical line Re=1/2).  Confirms simple-pole r^-1 growth and locates the pole."""
    rows = []
    for r in rs:
        s = RHO1_HALF + r
        rows.append((float(r), abs(phi_infty(s))))
    return rows


# ============================================================ Step 1c: off-line defect
def defect_offline(h, t, dps=MP_DPS):
    """D(h,t) = | phi_infty(1/2-h+it) * conj(phi_infty(1/2+h+it)) - 1 |
    -- the failure of Hejhal's reflection identity (7.22) OFF the critical line."""
    set_prec(dps)
    s_minus = mpc(mpf(1) / 2 - h, t)
    s_plus = mpc(mpf(1) / 2 + h, t)
    prod = phi_infty(s_minus) * phi_infty(s_plus).conjugate()
    return abs(prod - 1)


def defect_online(t, dps=MP_DPS):
    """d(t) = | |phi_infty(1/2+it)| - 1 | on the line itself."""
    set_prec(dps)
    s = mpc(mpf(1) / 2, t)
    return abs(abs(phi_infty(s)) - 1)


# ============================================================ main sweep
def main():
    set_prec()
    report = {}

    # Step 1: is |phi_infty(1/2+it)| == 1 on the line (away from pole)?
    line_rows = check_line_unitarity()
    report["line_unitarity_check"] = line_rows
    print("== line unitarity check |phi_infty(1/2+it)| ==")
    for t, v in line_rows:
        print(f"  t={t:.6f}  |phi_infty|={v}")

    # Step 1b: pole location check -- confirm pole is at rho_1/2 (Re=1/4), NOT on Re=1/2
    pole_rows = check_pole()
    report["pole_check_at_rho1_over_2"] = pole_rows
    print("\n== pole check at s = rho_1/2 = 1/4 + i*gamma_1/2 ==")
    for r, v in pole_rows:
        print(f"  r={r:.0e}  |phi_infty(rho1/2+r)|={v}")

    # Step 1: on-line defect near t0 = gamma_1/2 -- since the pole is OFF the line
    # (Re=1/4 not 1/2), check whether the on-line defect is itself already nonzero
    # and usable, before falling back to the reflection-identity route.
    print("\n== on-line defect d(t)=||phi_infty(1/2+it)|-1| near t0=gamma_1/2 ==")
    tspan = mpf("0.5")
    npts = 21
    online_rows = []
    for i in range(npts):
        t = T0 - tspan + 2 * tspan * i / (npts - 1)
        d = defect_online(t)
        online_rows.append((float(t), str(d)))
        print(f"  t={float(t):.4f}  d(t)={d}")
    report["online_defect_grid"] = online_rows

    # Step 2: operative-regime anchor numbers.
    # windows: delta=0.1 -> |t-t0|<=delta/20=0.005 ; delta=0.5 -> |t-t0|<=delta/20=0.025
    print("\n== ON-LINE defect anchor (min/max over window, delta/20) ==")
    anchor = {}
    for delta in (mpf("0.1"), mpf("0.5")):
        win = delta / 20
        npts_w = 41
        vals = []
        for i in range(npts_w):
            t = T0 - win + 2 * win * i / (npts_w - 1)
            d = defect_online(t)
            vals.append((float(t), d))
        dmin = min(vals, key=lambda x: x[1])
        dmax = max(vals, key=lambda x: x[1])
        anchor[f"delta={float(delta)}_online"] = {
            "window": f"|t-t0|<={float(win)}",
            "min": (dmin[0], str(dmin[1])),
            "max": (dmax[0], str(dmax[1])),
        }
        print(f"  delta={float(delta)}: window |t-t0|<={float(win)}: "
              f"min d={dmin[1]} at t={dmin[0]:.6f}, max d={dmax[1]} at t={dmax[0]:.6f}")

    # Also compute the OFF-line reflection-identity defect for comparison / completeness.
    print("\n== OFF-line reflection-identity defect D(h,t) ==")
    hs = [mpf("0.005"), mpf("0.01"), mpf("0.02"), mpf("0.05")]
    offline_rows = {}
    for h in hs:
        vals = []
        for delta in (mpf("0.1"), mpf("0.5")):
            win = delta / 20
            npts_w = 21
            row = []
            for i in range(npts_w):
                t = T0 - win + 2 * win * i / (npts_w - 1)
                d = defect_offline(h, t)
                row.append((float(t), d))
            dmin = min(row, key=lambda x: x[1])
            dmax = max(row, key=lambda x: x[1])
            offline_rows[f"h={float(h)}_delta={float(delta)}"] = {
                "min": (dmin[0], str(dmin[1])),
                "max": (dmax[0], str(dmax[1])),
            }
            print(f"  h={float(h)}, delta={float(delta)}: min D={dmin[1]} at t={dmin[0]:.6f}, "
                  f"max D={dmax[1]} at t={dmax[0]:.6f}")
    report["anchor_online"] = anchor
    report["anchor_offline"] = offline_rows

    # Step 3: residue fit near s = rho_1/2 (the pole ON the phi_infty formula).
    # phi_infty(s) ~ c/(s - rho1/2) for s near rho1/2 (simple pole from zeta(2s-1)
    # having a simple pole at 2s-1=1 i.e. s=1).  WAIT -- check: actual pole source.
    print("\n== residue fit at s = rho_1/2 ==")
    residue = fit_residue()
    report["residue_fit"] = residue
    print(f"  residue c (dps={MP_DPS}): {residue['c_high']}")
    print(f"  residue c (dps={MP_DPS//2}, doubling receipt): {residue['c_low']}")
    print(f"  relative disagreement: {residue['reldiff']}")

    (OUT_DIR / "r4_defect_data.json").write_text(json.dumps(report, indent=2, default=str))
    print(f"\nWrote {OUT_DIR / 'r4_defect_data.json'}")


def fit_residue(dps_high=MP_DPS, dps_low=MP_DPS // 2, r=mpf("1e-6")):
    """c = lim_{s->rho1/2} (s - rho1/2) * phi_infty(s), estimated at finite r
    along the real-offset direction, at two precisions (doubling receipt)."""
    def c_at(dps):
        set_prec(dps)
        s = RHO1_HALF + r
        val = (s - RHO1_HALF) * phi_infty(s)
        return val

    set_prec(dps_high)
    c_high = c_at(dps_high)
    c_low = c_at(dps_low)
    set_prec(dps_high)
    reldiff = abs(c_high - c_low) / abs(c_high)
    return {"c_high": str(c_high), "c_low": str(c_low), "reldiff": str(reldiff)}


if __name__ == "__main__":
    main()
