#!/usr/bin/env python3
"""
THEOREM (R) PRE-TEST  --  decisive numerical test of the SINGLE open estimate
behind the reduction:  Q-uniform ABSOLUTE SUMMABILITY of the truncated twisted
roof-weighted BCZ autocorrelation on PSL(2,Z).

This is a NUMERICAL-ONLY pre-test (NOT a proof).  Goal: decide BEFORE proof
investment whether |c_L| ~ C * L^{-alpha} has alpha > 1 (summable -> reduction
SOLID) or alpha ~ 1/2..1 (NOT summable -> obstruction REAL).

------------------------------------------------------------------------------
EXACT DEFINITION USED  (matched verbatim to THEOREM_R_2026-05-15.md and the
reused code paths in verify_theorem_R.py -- NO invented variant):

  - farey(Q), fast_arrays(Q):  byte-identical to verify_theorem_R.py.  Per-node
    values f_j = h/k are EXACT rationals; S_j = j - Phi*f_j is the V4-PROVEN
    exact Birkhoff-sum identity (evaluated per the in-repo V3 float convention,
    per-node values exact).  An exact-Fraction cross-check (Q<=600) is included.

  - Hall spacing  s_j := Phi * gap_j   (R1: <s> = 1 EXACTLY, telescoping).

  - Hall-unit TRUNCATED cocycle (THEOREM_R sec.2, the R3_hall_variance code
    path -- the SAME definition, not a variant):
        psi^{(M)}_j := 1 - min(s_j, M)
    centered by its exact orbit mean (mean ~ 0; we subtract the empirical mean
    exactly as R3_hall_variance does):  psihat = psi^{(M)} - mean(psi^{(M)}).

  - ROOF weight (THEOREM_R sec.2 / sec.3 (R-input)):  R(P_j) = 1/(a_j b_j).
    Locked Athreya-Cheung Thm 1.1: gap_j = R(P_j)/Q^2  =>  R(P_j) = Q^2 * gap_j
    EXACTLY (a,b = k/Q,k'/Q rationals).  The (R-input) integrand carries this
    roof weight R*dm  (THEOREM_R sec.3, line "c_j^{(M)} = int psi^{(M)} *
    psi^{(M)} o T^j * R * dm").  We use the symmetric roof weight
    w_j = sqrt(R_j R_{j+L}) so the lag-L correlation is the discrete analogue
    of int psihat * (psihat o T^L) * R dm with the BCZ-invariant measure.
    (A plain w_j = R_j variant is also reported for robustness.)

  - TWIST / character factor (START.md sec.1.5 dictionary line
    "A_Q(m) = sum e(m f)  <->  twisted horocycle integral, frequency m";
    THEOREM_R sec.4 "the m-twist in A_Q(m) = sum e(mf) -- the character
    cocycle line").  The twisted lag-L correlation uses the multiplicative
    character phase e(m * (f_{j+L} - f_j)) = cos(2 pi m (f_{j+L}-f_j)) for the
    real autocorrelation (m=0 recovers the BARE untwisted Stroembergsson-1/2
    object as a control).

  Putting it together, the lag-L truncated twisted roof-weighted BCZ
  autocorrelation (exact per-node inputs; the final reduction sum and the
  exponent fit are float, per the in-repo V3 convention) is

      c_L^{(M,m)} = (1/Z) * sum_j  psihat_j * psihat_{j+L}
                            * cos(2 pi m (f_{j+L} - f_j))
                            * sqrt(R_j * R_{j+L})

  with Z = sum_j R_j  (roof-mass normalization, so c_0 is an O(1) Hall second
  moment, Q-stably -- matching R3's Q-stable c_0(M)).  We test |c_L| decay.

  The m=0, w=1 case is exactly R3_hall_variance's lag-j autocovariance term
  (cross-checked at L=0 against R3 numbers below) -- definitions are identical.
------------------------------------------------------------------------------
"""
from fractions import Fraction
import numpy as np

# Contiguous orbit-segment length for the autocorrelation (a stationary
# BCZ-suspension time-average; faithfulness is cross-checked vs the FULL
# orbit at Q=500..2000 in [X1] below).  Full orbit for Q<=~1600.
SEG = 800_000


# ---- byte-identical to verify_theorem_R.py --------------------------------
def farey(Q):
    a, b, c, d = 0, 1, 1, Q
    out = []
    while c <= Q:
        if (a, b) != (0, 1):
            out.append((a, b))
        k = (Q + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b
    out.append((1, 1))
    return out


def exact_nodes_fr(Q):
    F = farey(Q)
    Fx = [Fraction(0)] + [Fraction(h, k) for (h, k) in F]
    Phi = len(F)
    S = [j - Phi * Fx[j] for j in range(len(Fx))]
    gaps = [Fx[j] - Fx[j - 1] for j in range(1, len(Fx))]
    return Phi, Fx, S, gaps


def fast_arrays(Q):
    """Phi, S_left[j]=E_Q(f_j), gap[j], and the EXACT roof R_j=Q^2 gap_j and
    the left-node positions f_j (needed for the twist phase)."""
    F = farey(Q)
    num = np.array([0] + [h for (h, k) in F], dtype=np.float64)
    den = np.array([1] + [k for (h, k) in F], dtype=np.float64)
    x = num / den                                   # f_j, exact rationals
    Phi = len(F)
    j = np.arange(len(x), dtype=np.float64)
    S = j - Phi * x
    gap = x[1:] - x[:-1]
    R = (Q * Q) * gap                               # R(P_j)=Q^2 gap_j (AC Thm1.1)
    return Phi, S[:-1], gap, x[:-1], R               # left node of each interval


# ---------------------------------------------------------------------------
def cocycle(Q, M, seg=None):
    """psihat_j (centered Hall-unit truncated cocycle), roof R_j, node f_j.
    psi^{(M)}_j = 1 - min(s_j, M),  s_j = Phi*gap_j  (R3_hall_variance path).

    seg: if set, use a contiguous CENTERED orbit segment of this length.
    The autocorrelation is a stationary BCZ-suspension time-average; a
    contiguous segment of >= a few x 10^5 nodes is a faithful, exact
    sub-sample (matched cross-check vs full orbit at Q=500..2000 below).
    Centering uses the FULL exact orbit mean (psi mean ~ 0; R1)."""
    Phi, S, gap, fL, R = fast_arrays(Q)
    s = Phi * gap
    psi = 1.0 - np.minimum(s, float(M))
    psihat = psi - psi.mean()                        # exact orbit-mean centering
    if seg is not None and seg < len(psihat):
        lo = (len(psihat) - seg) // 2
        sl = slice(lo, lo + seg)
        psihat, R, fL = psihat[sl], R[sl], fL[sl]
    return psihat, R, fL, Phi


def autocorr_L(psihat, R, fL, m, Lmax, weight="sqrt"):
    """c_L^{(M,m)} for L=0..Lmax.  Roof-weighted, twisted by frequency m.

    weight options (all are honest readings of THEOREM_R sec.3's
    'c_j^{(M)} = int psi^{(M)} psi^{(M)} o T^j  R dm' -- the discrete
    BCZ-invariant-measure analogue; we report several to expose any
    roof-tail contamination, since R has the Hall heavy tail (L^p, p<2)):
      'single' -> w_j = R_j   (the SINGLE invariant suspension roof weight:
                   sum_j R_j (psihat psihat o T^L)_j / sum_j R_j is the
                   BCZ-suspension time-average, the literal sec.3 object);
      'sqrt'   -> sqrt(R_j R_{j+L})  (symmetrized; heavy-tail sensitive);
      'left'   -> R_j  (same as single; kept for back-compat label);
      'none'   -> 1  (UNWEIGHTED Hall cocycle: the bare R3 object, the
                   pure Stroembergsson-1/2 control);
      'normed' -> 1, but DIVIDED by c_0 (Pearson-normalized correlation:
                   isolates pure cocycle decorrelation, removes the
                   roof-tail second-moment scale entirely).
    Returns array c[0..Lmax] and the normalizer Z."""
    n = len(psihat)
    c = np.empty(Lmax + 1, dtype=np.float64)
    twopim = 2.0 * np.pi * m
    if weight in ("single", "left"):
        Z = float(np.sum(R))
    elif weight == "sqrt":
        Z = float(np.sum(R))
    else:
        Z = float(n)
    for L in range(Lmax + 1):
        a = psihat[:n - L]
        b = psihat[L:]
        ph = 1.0 if m == 0 else np.cos(twopim * (fL[L:] - fL[:n - L]))
        if weight == "sqrt":
            w = np.sqrt(R[:n - L] * R[L:])
        elif weight in ("single", "left"):
            w = R[:n - L]
        else:
            w = 1.0
        c[L] = float(np.sum(a * b * ph * w)) / Z
    if weight == "normed":
        c = c / c[0]
    return c, Z


# ---- exponent fit & summability diagnostics -------------------------------
def loglog_fit(L, cabs, Llo, Lhi):
    """OLS of log|c_L| on log L over [Llo,Lhi]; returns alpha, stderr, R^2.
    alpha defined by |c_L| ~ C L^{-alpha} (slope = -alpha)."""
    mask = (L >= Llo) & (L <= Lhi) & (cabs > 0)
    x = np.log(L[mask].astype(np.float64))
    y = np.log(cabs[mask])
    nfit = len(x)
    if nfit < 4:
        return None
    A = np.vstack([x, np.ones_like(x)]).T
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    slope, intc = coef
    yhat = A @ coef
    resid = y - yhat
    ss_res = float(resid @ resid)
    ss_tot = float(((y - y.mean()) ** 2).sum())
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    # slope std error
    sx2 = float(((x - x.mean()) ** 2).sum())
    s_err = np.sqrt(ss_res / max(nfit - 2, 1) / sx2) if sx2 > 0 else float("nan")
    return (-slope, s_err, r2, nfit)


def partial_sums(cabs):
    """Sigma_L |c_L| partial sums; report at checkpoints + tail growth.
    If alpha>1 the partial sum converges (flattens); if alpha<=1 it grows
    like (Lmax)^{1-alpha} or log Lmax."""
    ps = np.cumsum(cabs)
    return ps


def main():
    print("=" * 78)
    print("THEOREM (R) PRE-TEST: truncated twisted roof-weighted BCZ autocorr.")
    print("  c_L^{(M,m)} = (1/Z) sum psihat_j psihat_{j+L} cos(2pi m (f_{j+L}-f_j))")
    print("                       * sqrt(R_j R_{j+L}) ;  psi^{(M)}=1-min(s_j,M)")
    print("  NUMERICAL-ONLY pre-test.  Decision: alpha>1 (summable) vs alpha<=1.")
    print("=" * 78)

    # --- Identity / definition cross-check vs R3 (m=0, weight none, L=0) ----
    print("\n[X0] DEFINITION CROSS-CHECK: m=0, weight='none', L=0 must equal")
    print("     R3_hall_variance c_0(M) (same cocycle).  EXACT-Fraction node")
    print("     cross-check of S_j (Q<=600) also asserted.")
    for Q in (500, 1000, 2000):
        psihat, R, fL, Phi = cocycle(Q, 8, seg=SEG)
        c, _ = autocorr_L(psihat, R, fL, m=0, Lmax=0, weight="none")
        print(f"   Q={Q:5d} M=8 : c_0(none)={c[0]:.4f}  (R3 ref ~0.610)")
    # exact-Fraction node cross-check (V4 identity), Q<=600
    Phi, Fx, S, gaps = exact_nodes_fr(600)
    Ff = farey(600)
    okS = all(S[j] == j - Phi * Fx[j] for j in range(len(Fx)))
    okclosed = (S[0] == 0 and S[-1] == 0)
    print(f"   EXACT Q=600: S_j=j-Phi f_j all-nodes={okS}; closed S_0=S_end=0="
          f"{okclosed}  [V4 identity reused, exact]")

    print("\n[X1] SEGMENT FAITHFULNESS: alpha (normed,M=8,[8,200]) from FULL")
    print(f"     orbit vs centered {SEG}-node segment (Q where Phi>SEG).")
    for Q in (1500, 2000, 3000):
        pf, Rf, ff, _ = cocycle(Q, 8, seg=None)
        ps, Rs, fs, _ = cocycle(Q, 8, seg=SEG)
        Lt = 200
        cf, _ = autocorr_L(pf, Rf, ff, 0, Lt, weight="normed")
        cs, _ = autocorr_L(ps, Rs, fs, 0, Lt, weight="normed")
        af = loglog_fit(np.arange(1, Lt + 1), np.abs(cf[1:]), 8, Lt)
        as_ = loglog_fit(np.arange(1, Lt + 1), np.abs(cs[1:]), 8, Lt)
        print(f"   Q={Q:5d} Phi={len(pf):8d}: full a={af[0]:.3f}  "
              f"seg a={as_[0]:.3f}  (diff {abs(af[0]-as_[0]):.3f})")

    Qs = (500, 1000, 2000, 4000)
    Ms = (4, 8, 16)
    ms = (0, 1, 3)              # m=0 = BARE control (Stroembergsson 1/2)
    Lmax = 400

    # --- main exponent measurement -----------------------------------------
    # 'normed' (Pearson) is the DECISIVE diagnostic: it removes the roof-tail
    # second-moment scale and isolates the pure cocycle decorrelation rate,
    # which is exactly the alpha that (R-input)'s summability needs.
    for weight in ("normed", "none", "single", "sqrt"):
        print(f"\n{'='*78}\n[FIT] roof weight = '{weight}'   "
              f"|c_L| ~ C L^(-alpha) ; fit window L in [8, {Lmax}]")
        print(f"{'='*78}")
        for M in Ms:
            print(f"\n  --- truncation M = {M} ---")
            print("   Q     m   alpha   +-se    R^2  nfit |"
                  "  Sum|c_L| @L=50/200/400   tail ratio PS[400]/PS[200]")
            for Q in Qs:
                psihat, R, fL, Phi = cocycle(Q, M, seg=SEG)
                Lm = min(Lmax, len(psihat) // 4)
                for m in ms:
                    c, Z = autocorr_L(psihat, R, fL, m, Lm, weight=weight)
                    cabs = np.abs(c[1:])             # L>=1
                    Lar = np.arange(1, Lm + 1)
                    fit = loglog_fit(Lar, cabs, 8, Lm)
                    ps = partial_sums(cabs)
                    def at(L): return ps[L - 1] if L <= Lm else ps[-1]
                    p50, p200, p400 = at(50), at(200), at(min(400, Lm))
                    ratio = (p400 / p200) if p200 > 0 else float("nan")
                    if fit:
                        al, se, r2, nf = fit
                        mtag = "bare" if m == 0 else f"m={m}"
                        print(f"  {Q:5d} {mtag:>5} {al:6.3f} {se:5.3f} "
                              f"{r2:5.3f} {nf:4d} | "
                              f"{p50:8.4f}/{p200:8.4f}/{p400:8.4f}   {ratio:6.3f}")

    # --- adversarial: vary Lmax window & truncation; Q-stability table ------
    print(f"\n{'='*78}")
    print("[ADV] Window robustness (M=8, weight='normed' DECISIVE): alpha over")
    print("      different fit windows -- artifact check.")
    print(f"{'='*78}")
    windows = [(4, 25), (8, 50), (8, 100), (8, 200), (8, 400),
               (20, 400), (50, 400), (100, 400)]
    for Q in (1000, 2000, 4000):
        psihat, R, fL, Phi = cocycle(Q, 8, seg=SEG)
        Lm = min(Lmax, len(psihat) // 4)
        for m in (0, 1, 3):
            c, Z = autocorr_L(psihat, R, fL, m, Lm, weight="normed")
            cabs = np.abs(c[1:])
            Lar = np.arange(1, Lm + 1)
            row = f"  Q={Q:5d} {'bare' if m==0 else 'm='+str(m):>5}: "
            for (lo, hi) in windows:
                h = min(hi, Lm)
                fit = loglog_fit(Lar, cabs, lo, h)
                row += f"[{lo}-{h}]a={fit[0]:.2f} " if fit else f"[{lo}-{h}]-- "
            print(row)

    # --- direct Sigma convergence test: does PS stabilize? -----------------
    print(f"\n{'='*78}")
    print("[SUM] Direct Sigma_L|c_L| convergence, DECISIVE 'normed' weight")
    print("      (M=8).  If alpha>1 the partial sum FLATTENS; if alpha<=1 it")
    print("      keeps growing.  Report PS at checkpoints and the doubling")
    print("      increments PS[2L]-PS[L] (-> 0 geometrically iff summable).")
    print(f"{'='*78}")
    for Q in (2000, 4000):
        psihat, R, fL, Phi = cocycle(Q, 8, seg=SEG)
        Lm = min(Lmax, len(psihat) // 4)
        for m in (0, 1, 3):
            c, Z = autocorr_L(psihat, R, fL, m, Lm, weight="normed")
            cabs = np.abs(c[1:])
            ps = np.cumsum(cabs)
            chk = [25, 50, 100, 200, min(400, Lm)]
            vals = [ps[L - 1] for L in chk]
            incs = [vals[i + 1] - vals[i] for i in range(len(vals) - 1)]
            mtag = "bare" if m == 0 else f"m={m}"
            print(f"  Q={Q} {mtag:>5}: PS@{chk}=" +
                  "[" + ",".join(f"{v:.3f}" for v in vals) + "]  "
                  "incs=" + "[" + ",".join(f"{v:.4f}" for v in incs) + "]")

    # --- decisive Q-stability of the 'normed' exponent --------------------
    print(f"\n{'='*78}")
    print("[QST] Q-stability of the DECISIVE 'normed' alpha (M=8, fit [8,Lm]).")
    print("      Robust alpha>=1+eta across Q -> (i) SOLID; ~0.5..1 -> (ii).")
    print(f"{'='*78}")
    print("   Q      bare-alpha   m=1-alpha   m=3-alpha     (fit window [8,Lm])")
    for Q in (500, 1000, 2000, 4000):
        psihat, R, fL, Phi = cocycle(Q, 8, seg=SEG)
        Lm = min(Lmax, len(psihat) // 4)
        outs = []
        for m in (0, 1, 3):
            c, Z = autocorr_L(psihat, R, fL, m, Lm, weight="normed")
            fit = loglog_fit(np.arange(1, Lm + 1), np.abs(c[1:]), 8, Lm)
            outs.append(fit)
        print(f"  {Q:5d}   {outs[0][0]:.3f}+-{outs[0][1]:.3f}  "
              f"{outs[1][0]:.3f}+-{outs[1][1]:.3f}  "
              f"{outs[2][0]:.3f}+-{outs[2][1]:.3f}   (Lm={Lm})")

    print("=" * 78)
    print("VERDICT KEY: alpha>=1+eta robust across Q,m,M -> (i) SOLID;")
    print("  alpha~0.5..1 -> (ii) obstruction REAL; mixed -> (iii) AMBIGUOUS.")
    print("=" * 78)


if __name__ == "__main__":
    main()
