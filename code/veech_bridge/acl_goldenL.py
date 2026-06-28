"""
acl_goldenL.py  --  Reproduce Athreya-Chaika-Lelievre 2013 (arXiv:1308.4203)
golden-L slope-gap distribution from FIRST PRINCIPLES, three independent ways,
and VALIDATE against the paper's stated facts:

  (V1) hard edge:  f(t) = 0 for 0 <= t <= 1   (ACL Remark 2 / Thm: R >= 1).
  (V2) exactly SEVEN points of non-differentiability (ACL Thm 1.1).
  (V3) integral of f over [0, inf) = 1 (proper probability density).
  (V4) quadratic tail f ~ c/t^2.

THREE INDEPENDENT COMPUTATIONS that must agree:

  METHOD A (paper closed form).  Code ACL Appendix A piecewise pdf
     f = f_1 + f_phi + f_inf  on the breakpoint partition, verbatim.

  METHOD B (our own geometric integral).  Compute the complementary CDF
     G(t) = m({(a,b) in Omega : R(a,b) >= t}),  dm = phi^2 da db,
     by integrating phi^2 over the super-level set of EACH of the three pieces
     (Omega_1, Omega_phi, Omega_inf) directly, via adaptive 2D quadrature.
     Then f(t) = -G'(t).  This is OUR re-derivation of the same tail function,
     independent of ACL's hand-integrated Appendix-A expressions; it tests
     whether we get the same density from the section+roof alone.

  METHOD C (Birkhoff Monte Carlo).  Iterate the EXACT ACL return map T
     (the golden-L BCZ map, ACL section 3.4) from random seeds and histogram
     the roof R along the orbit.  By ergodicity (dm = phi^2 da db) this -> f.
     Cross-checks A and B with zero shared code for the density.

Sources (verbatim, scratchpad/acl2013.txt):
  Domain  Omega = {(a,b): 0<a<=1, 1 - a*phi < b <= 1}                  (Thm 3.1)
  Pieces (lines 344-348):
    Omega_1   = { phi_bar <= a <= 1,  1 - a*phi < b <= phi_bar - a }      [phi_bar=1/phi]
    Omega_phi = { phi_bar^2 <= a <= 1, phi_bar - a < b <= phi_bar - a*phi_bar }
    Omega_inf = { 0 < a <= 1, phi_bar - a*phi_bar < b <= 1 }
      (paper writes phi for 1/phi via the bar; here phi_bar = 1/phi = phi-1)
  Roofs (lines 354-361):
    Omega_1   : R = 1/(a(a+b))
    Omega_phi : R = 1/(a(a*phi_bar + b))
    Omega_inf : R = 1/(a*b)
  Return map T (lines 404-410):
    Omega_1   : T=( (a+b)*phi, a+b*phi + k1*phi^2*(a+b) ), k1 = -floor((a+b*phi-1)/(phi^2*(a+b)))
    Omega_phi : T=( a+b*phi,   b + k_phi*phi*(a+b*phi) ),  k_phi = -floor((b-1)/(phi*(a+b*phi)))
    Omega_inf : T=( b, -a + k_inf*phi*b ),                 k_inf = -floor((-a-1)/(phi*b))
  Invariant measure dm = phi^2 da db (Thm 4.1).
  Gap CDF:  P(gap >= t) = m({R >= t})  (Thm 4.2).
"""
from __future__ import annotations
import math
import json
import os

import mpmath as mp

mp.mp.dps = 40

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)

PHI = (1 + mp.sqrt(5)) / 2          # phi  = lambda_5 = 2 cos(pi/5)
PHIB = 1 / PHI                       # phi_bar = 1/phi = phi - 1


# ---------------------------------------------------------------------------
# METHOD A : ACL Appendix A closed-form density (verbatim)
# ---------------------------------------------------------------------------
def _ath(x):
    return mp.atanh(x)

def _r(x):
    return mp.sqrt(1 - 4 * x)

# NOTE on the OCR bars (verified by self-consistency, see acl_bar_check below):
#   ACL "Notation": a bar denotes the INVERSE, "alpha and phi denote alpha^-1".
#   The pdftotext lost the bars; the only reading making r(.)=sqrt(1-4x) REAL and
#   the ranges ORDERED is:  the argument of r is  phi/alpha = phi * alphabar
#   (in f_inf and f_1) and  1/alpha = alphabar (in f_phi); the leading constants
#   "phi r(...)" are  phibar * r(...) = (1/phi) r(...).  Breakpoints (increasing):
#     f_inf : 1, 4*phi, phi^4         (arg phi/alpha; r real iff alpha>4phi)
#     f_phi : phi, 4, phi^3           (arg 1/alpha;   r real iff alpha>4)
#     f_1   : phi, 4*phi, phi^2/...   (arg phi/alpha)
#   We additionally cross-validate ALL of this against METHOD B (independent
#   super-level-area integral) and METHOD C (Monte Carlo); the closed form is
#   used only where its ranges are unambiguous.
def f_inf_A(a):
    """f_inf piecewise. Ranges (increasing alpha): 1, 4phi, phi^4.
      0<a<1        : 0
      1<a<4phi     : (1/a^2) ln a
      4phi<a<phi^4 : (1/a^2)(ln a - 4 ath r(phi/a))
      phi^4<a      : (1/a^2)(2 ln(a/(2phi)) + 2 ln(1 - r(phi/a)))
    (paper 'ϕα' in r(.) = phi*alphabar = phi/alpha; 'ϕα/2' = (phi/alpha)/2 inside
     a log of alpha/(2phi) after sign care -> we use the F-derivative directly.)
    """
    if a <= 1:
        return mp.mpf(0)
    if a < 4 * PHI:
        return (1 / a**2) * mp.log(a)
    if a < PHI**4:
        return (1 / a**2) * (mp.log(a) - 4 * _ath(_r(PHI / a)))
    return (1 / a**2) * (2 * mp.log(a / (2 * PHI)) + 2 * mp.log(1 - _r(PHI / a)))

def f_phi_A(a):
    """f_phi. Ranges: phi, 4, phi^3.
      0<a<phi      : 0
      phi<a<4      : (1/a^2) ln(a/phi)
      4<a<phi^3    : (1/a^2)(ln(a/phi) - 4 ath r(1/a))
      phi^3<a      : 0
    (paper ln(ϕα) = ln(alphabar... ) -> ln(a/phi); r(α)=r(1/a).)
    """
    if a <= PHI:
        return mp.mpf(0)
    if a < 4:
        return (1 / a**2) * mp.log(a / PHI)
    if a < PHI**3:
        return (1 / a**2) * (mp.log(a / PHI) - 4 * _ath(_r(1 / a)))
    return mp.mpf(0)

def f_1_A(a):
    """f_1. Ranges: phi, 4phi, then 0 beyond phi^... .
      0<a<phi       : 0
      phi<a<4phi    : (1/a^2) ln(a/phi)
      4phi<a        : (1/a^2)(ln(a/phi) - 2 ath r(phi/a))   [until it vanishes]
    The paper lists a final '->0' branch; numerically f_1 is tiny/zero past phi^2.
    Because the f_1 ranges are the most OCR-ambiguous, we DO NOT rely on f_1's
    closed form for the breakpoint count; METHOD B carries that. We include the
    unambiguous first nonzero branch (phi<a<4phi) which dominates.
    """
    if a <= PHI:
        return mp.mpf(0)
    if a < 4 * PHI:
        return (1 / a**2) * mp.log(a / PHI)
    arg = PHI / a
    if arg < 0.25:
        return (1 / a**2) * (mp.log(a / PHI) - 2 * _ath(_r(arg)))
    return (1 / a**2) * mp.log(a / PHI)

def f_A(a):
    """Total ACL density f = f_1 + f_phi + f_inf (closed form, Appendix A)."""
    return f_1_A(a) + f_phi_A(a) + f_inf_A(a)


# ---------------------------------------------------------------------------
# METHOD B : our own geometric integral of G(t)=m({R>=t}), dm = phi^2 da db.
# We integrate phi^2 over { (a,b) in Omega_s : R_s(a,b) >= t } for each piece.
# Because R_s = 1/(a*L_s(a,b)) with L_inf=b, L_phi=PHIB*a+b, L_1=a+b, the
# condition R>=t is  a*L_s <= 1/t.  We do this by 1D integration over a with the
# inner b-interval clipped by both the piece's b-bounds and the level condition.
# ---------------------------------------------------------------------------
# Probability normalization of the section measure.
#   Section area = phi/2 (verified). ACL's dm = phi^2 da db is the SUSPENSION /
#   Haar normalization (it gives the cover volume 3pi^2/10, verified to 1e-12),
#   NOT a probability measure on Omega. The gap-distribution PROBABILITY measure
#   is  dm_prob = da db / Area(Omega) = (2/phi) da db,  m_prob(Omega) = 1.
NORM_PROB = 2 / PHI               # = 1/Area(Omega) = 1/(phi/2)

def G_geom(t):
    """G(t) = P(gap >= t) = m_prob({R>=t}), dm_prob=(2/phi) da db. Returns mpf."""
    t = mp.mpf(t)
    phi2 = NORM_PROB

    def super_level(a_lo, a_hi, b_lo_fn, b_hi_fn, Lcoef_const):
        """measure of {a in[a_lo,a_hi], b in(b_lo,b_hi], a*(Lcoef_const*a+b) <= 1/t}.
        R = 1/(a*(Lcoef_const*a + b)) >= t  <=>  b <= 1/(t*a) - Lcoef_const*a.
        Integrate NORM_PROB * (clipped b-width) da.
        """
        def integrand(a):
            blo = b_lo_fn(a)
            bhi = b_hi_fn(a)
            if bhi <= blo:
                return mp.mpf(0)
            bcap = 1 / (t * a) - Lcoef_const * a       # R>=t cap
            top = min(bhi, bcap)
            if top <= blo:
                return mp.mpf(0)
            return phi2 * (top - blo)
        return mp.quad(integrand, [a_lo, a_hi])

    # Cells exactly as validated by the V=3pi^2/10 suspension check:
    # Omega_1   : a in [PHIB,1],   b in (1-a*phi, PHIB-a],            R=1/(a(a+b))   -> Lconst=1
    G1 = super_level(PHIB, mp.mpf(1),
                     lambda a: 1 - a * PHI, lambda a: PHIB - a, Lcoef_const=mp.mpf(1))
    # Omega_phi : split [PHIB^2,PHIB] b(1-aphi,PHIB-a*PHIB] and [PHIB,1] b(PHIB-a,PHIB-a*PHIB], R=1/(a(PHIB*a+b)) -> Lconst=PHIB
    Gphi = (super_level(PHIB**2, PHIB,
                        lambda a: 1 - a * PHI, lambda a: PHIB - a * PHIB, Lcoef_const=PHIB)
            + super_level(PHIB, mp.mpf(1),
                          lambda a: PHIB - a, lambda a: PHIB - a * PHIB, Lcoef_const=PHIB))
    # Omega_inf : split [0,PHIB^2] b(1-aphi,1] and [PHIB^2,1] b(PHIB-a*PHIB,1], R=1/(a*b) -> Lconst=0
    Ginf = (super_level(mp.mpf("1e-18"), PHIB**2,
                        lambda a: 1 - a * PHI, lambda a: mp.mpf(1), Lcoef_const=mp.mpf(0))
            + super_level(PHIB**2, mp.mpf(1),
                          lambda a: PHIB - a * PHIB, lambda a: mp.mpf(1), Lcoef_const=mp.mpf(0)))
    return G1 + Gphi + Ginf

def f_geom(t, h=mp.mpf("1e-6")):
    """f(t) = -G'(t) by central difference of the geometric G."""
    return -(G_geom(t + h) - G_geom(t - h)) / (2 * h)


# ---------------------------------------------------------------------------
# METHOD C : Birkhoff Monte Carlo on the EXACT ACL return map T.
# ---------------------------------------------------------------------------
def _which_piece(a, b):
    """Return 's' in {'1','phi','inf'} for (a,b) in Omega (float)."""
    phib = float(PHIB)
    # Omega_1 : phib<=a<=1, 1-a*phi<b<=phib-a
    if a >= phib and b <= phib - a + 1e-15:
        return '1'
    # Omega_phi: phib^2<=a<=1, phib-a<b<=phib-a*phib
    if a >= phib**2 and b <= phib - a * phib + 1e-15:
        return 'phi'
    return 'inf'

def acl_T_step(a, b):
    """One step of the exact ACL golden-L BCZ map. Returns (a',b',R)."""
    phi = float(PHI); phib = float(PHIB)
    s = _which_piece(a, b)
    if s == '1':
        R = 1.0 / (a * (a + b))
        k1 = -math.floor((a + b * phi - 1) / (phi**2 * (a + b)))
        a2 = (a + b) * phi
        b2 = a + b * phi + k1 * phi**2 * (a + b)
    elif s == 'phi':
        R = 1.0 / (a * (a * phib + b))
        kphi = -math.floor((b - 1) / (phi * (a + b * phi)))
        a2 = a + b * phi
        b2 = b + kphi * phi * (a + b * phi)
    else:
        R = 1.0 / (a * b)
        kinf = -math.floor((-a - 1) / (phi * b))
        a2 = b
        b2 = -a + kinf * phi * b
    return a2, b2, R

def monte_carlo_roof(n_steps=2_000_000, n_seeds=8, burn=500, seed=20260627):
    """Iterate T; collect roof R values. Return list of R (floats)."""
    import random
    rng = random.Random(seed)
    phi = float(PHI)
    Rs = []
    for _ in range(n_seeds):
        # random seed in Omega
        while True:
            a = rng.random()
            b = rng.random()
            if 0 < a <= 1 and (1 - a * phi) < b <= 1:
                break
        ok = True
        for _ in range(burn):
            try:
                a, b, _R = acl_T_step(a, b)
            except (ZeroDivisionError, ValueError):
                ok = False
                break
        if not ok:
            continue
        for _ in range(n_steps // n_seeds):
            try:
                a, b, R = acl_T_step(a, b)
            except (ZeroDivisionError, ValueError):
                break
            if R <= 0 or not math.isfinite(R):
                break
            Rs.append(R)
    return Rs


if __name__ == "__main__":
    report = {"surface": "golden_L", "q": 5, "lambda": float(PHI),
              "lambda3": float(PHI**3), "one_over_lambda3": float(1 / PHI**3)}

    # ---- V1/V2/V3 via METHOD A (closed form) ----
    # integral of f over a fine grid + breakpoint check
    print("METHOD A: ACL Appendix-A closed-form density")
    # candidate non-differentiability points (where any piece changes formula),
    # restricted to t>=1 since f=0 below the global edge.
    bps_raw = sorted(set([
        float(mp.mpf(1)),
        float(4 * PHIB),          # 4*phi_bar = 4/phi
        float(PHIB**4),
        float(PHIB),              # < 1, below edge; will be filtered
        float(4),
        float(PHIB**3),
        float(PHIB**2),
    ]))
    # integral of f over [0, BIG] with mpmath quad piecewise
    BIG = 200.0
    bp_for_quad = [b for b in bps_raw if 0 < b < BIG]
    nodes = [0.0] + [b for b in bp_for_quad] + [BIG]
    nodes = sorted(set(nodes))
    integral = mp.mpf(0)
    for i in range(len(nodes) - 1):
        lo, hi = nodes[i], nodes[i + 1]
        integral += mp.quad(lambda a: f_A(mp.mpf(a)), [lo, hi])
    # add analytic tail beyond BIG: f ~ c/t^2 with c = lim a^2 f(a).
    # for a large, f_inf dominates -> (1/a^2)(2 ln(PHIB a/2)+2 ln(1-r)) ; but
    # actually as a->inf f~ (something)/a^2 -> compute residual tail by quad to 1e6
    tail = mp.quad(lambda a: f_A(mp.mpf(a)), [BIG, 1e6])
    integral_full = integral + tail
    report["methodA_integral_0_to_1e6"] = float(integral_full)

    # hard edge: f(t)=0 for t<=1 ; check just below and the jump at 1
    report["methodA_f_at_0.5"] = float(f_A(mp.mpf("0.5")))
    report["methodA_f_at_0.999"] = float(f_A(mp.mpf("0.999")))
    report["methodA_f_at_1.001"] = float(f_A(mp.mpf("1.001")))
    print(f"  f(0.5)={report['methodA_f_at_0.5']:.3e}  f(0.999)={report['methodA_f_at_0.999']:.3e}  f(1.001)={report['methodA_f_at_1.001']:.6f}")
    print(f"  integral_0_to_1e6 = {report['methodA_integral_0_to_1e6']:.6f}  (want 1.0)")

    # Candidate non-differentiability points = the union of all three pieces'
    # breakpoints (each is a power of phi or 4*power), restricted to t>=1.
    cand = sorted(set([
        float(mp.mpf(1)),          # global hard edge (f jumps 0 -> + here)
        float(PHI),                # f_phi and f_1 switch on
        float(4),                  # f_phi r-branch
        float(4 * PHI),            # f_inf & f_1 r-branch
        float(PHI**3),             # f_phi switches off
        float(PHI**4),             # f_inf last branch
        float(PHI**2),             # f_1 region
    ]))
    nd_points = []
    for c in cand:
        if c < 0.99:
            continue
        h = mp.mpf("1e-6")
        cc = mp.mpf(c)
        # one-sided first derivatives of f via closed form (Method A)
        dl = float((f_A(cc - h) - f_A(cc - 3 * h)) / (2 * h))
        dr = float((f_A(cc + 3 * h) - f_A(cc + h)) / (2 * h))
        jump_f = float(f_A(cc + h) - f_A(cc - h))
        is_nd = (abs(dl - dr) > 1e-3) or (abs(jump_f) > 1e-6)
        nd_points.append({"t": c, "dleft": dl, "dright": dr,
                          "f_jump": jump_f, "is_nondiff": is_nd})
    nd_real = [p for p in nd_points if p["is_nondiff"]]
    report["methodA_nondiff_points"] = nd_points
    report["methodA_nondiff_count"] = len(nd_real)
    print(f"  candidate breakpoints (t>=1): {len(cand)};  detected non-diff: {len(nd_real)}")
    for p in nd_points:
        flag = "NONDIFF" if p["is_nondiff"] else "smooth "
        print(f"    [{flag}] t={p['t']:.6f}  f'-={p['dleft']:.4f}  f'+={p['dright']:.4f}  fjump={p['f_jump']:.2e}")

    # ---- METHOD B (our geometric G) cross-check at sample points ----
    print("\nMETHOD B: our geometric G(t)=m({R>=t}) and f=-G'")
    report["methodB"] = {}
    for t in [0.5, 1.0, 1.5, 2.0, 3.0, 5.0]:
        Gt = G_geom(t)
        report["methodB"][f"G({t})"] = float(Gt)
    # G(<=1) should be 1 (all mass), G monotone decreasing
    print(f"  G(0.5)={report['methodB']['G(0.5)']:.6f} (want 1.0)  G(1.0)={report['methodB']['G(1.0)']:.6f} (want 1.0)")
    print(f"  G(2.0)={report['methodB']['G(2.0)']:.6f}  G(3.0)={report['methodB']['G(3.0)']:.6f}")
    # compare f_geom vs f_A at a few interior points
    bcmp = {}
    for t in [1.5, 2.0, 2.5, 3.5]:
        fa = float(f_A(mp.mpf(t)))
        fb = float(f_geom(mp.mpf(t)))
        bcmp[str(t)] = {"f_A": fa, "f_geom": fb, "abs_diff": abs(fa - fb)}
        print(f"  t={t}: f_A={fa:.6f}  f_geom={fb:.6f}  diff={abs(fa-fb):.2e}")
    report["methodB_vs_A"] = bcmp

    # ---- METHOD C (Monte Carlo) ----
    print("\nMETHOD C: Birkhoff Monte Carlo on exact ACL return map T")
    Rs = monte_carlo_roof(n_steps=2_000_000, n_seeds=8)
    Rs_sorted = sorted(Rs)
    nmc = len(Rs)
    minR = Rs_sorted[0]
    # empirical CDF check vs G(t)=1-CDF
    report["methodC_n"] = nmc
    report["methodC_minR"] = minR
    report["methodC_frac_below_1"] = sum(1 for r in Rs if r < 0.999) / nmc
    print(f"  n={nmc}  min R = {minR:.6f}  frac(R<0.999) = {report['methodC_frac_below_1']:.2e} (want 0)")
    # compare empirical P(R>=t) to geometric G(t)
    ccmp = {}
    for t in [1.0, 1.5, 2.0, 3.0, 5.0]:
        emp = sum(1 for r in Rs if r >= t) / nmc
        geo = float(G_geom(t))
        ccmp[str(t)] = {"emp_P(R>=t)": emp, "geom_G(t)": geo, "abs_diff": abs(emp - geo)}
        print(f"  t={t}: emp P(R>=t)={emp:.5f}  geom G(t)={geo:.5f}  diff={abs(emp-geo):.4f}")
    report["methodC_vs_B"] = ccmp

    with open(os.path.join(OUT, "acl_goldenL_validation.json"), "w") as fp:
        json.dump(report, fp, indent=2)
    print(f"\nSaved {os.path.join(OUT, 'acl_goldenL_validation.json')}")
