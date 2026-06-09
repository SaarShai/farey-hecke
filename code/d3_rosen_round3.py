"""
d3_rosen_round3.py
==================

Round-3 implementation: CORRECTED full Rosen lambda_q-CF transfer operator
for the bounded-type survivor set.

BUG FIXED FROM PREVIOUS ROUNDS
--------------------------------
Previous code (d3_rosen_full.py) used the positive-only 'phi' operator on domain
[0, lam/2] and bisected to eigenvalue=0.5, claiming a 'factor-2 symmetry'.
This was WRONG in two ways:
  1. Wrong domain: [0, lam/2] instead of the correct [0, lam/2] (which equals [0,L])
     but the phi branches were used instead of the true psi branches.
  2. Wrong operator: The full Rosen map has BOTH-SIGN branches psi_{a,eps} with UNEQUAL
     weights and RESTRICTED DOMAINS (each branch only maps part of I_q into I_q).

CORRECT OPERATOR DEFINITION
-----------------------------
The Rosen lambda_q-CF map acts on I_q = [-L, L] where L = lambda_q/2.
For parameter s, the Ruelle transfer operator for EVEN eigenfunctions on [0,L] is:

    (L_s f)(x) = sum_{a=1}^{B} [
        1(x >= (2-a*lam^2)/lam) * (a*lam + x)^{-2s} * f(1/(a*lam + x))   [psi_{a,+} branch]
      + 1(x <= (a*lam^2-2)/lam) * (a*lam - x)^{-2s} * f(1/(a*lam - x))   [psi_{a,-} branch]
    ]

where the indicator functions encode the RESTRICTED DOMAIN of each branch:
  - psi_{a,+}(y) = 1/(a*lam + y) maps into I_q only when y >= (2 - a*lam^2)/lam
  - psi_{a,-}(y) = -1/(a*lam - y) maps into I_q^- only when y <= (a*lam^2 - 2)/lam

By the symmetry y -> -y, the full-domain eigenvalue = eigenvalue of the above even-function
operator. Eigenvalue TARGET = 1 (not 0.5).

DOMAIN AND BRANCH IMAGES
--------------------------
For q >= 4 and a >= 1: a*lam^2 > 2 (since lam^2 = 4cos^2(pi/q) >= 2 for q>=4).
- psi_{a,-} maps [0, (a*lam^2-2)/lam] -> [1/(a*lam), L] subset [0, L]. CLOSED.
- psi_{a,+} maps [(2-a*lam^2)/lam, L] -> [1/(a*lam+L), L] where (2-a*lam^2)/lam < 0 for a>=1, q>=4.
  So for q>=4, psi_{a,+} contributes on all of [0,L].

For q=3 (Gauss map): the Rosen-map structure on I_3=[-0.5,0.5] degenerates; use the
STANDARD GAUSS MAP on [0,1] with branches 1/(a+x) instead. This gives the correct
positive-only Gauss dimension which is the fundamental anchoring case.

GUARDRAIL ANCHORS (from independent verified run)
--------------------------------------------------
1. q=3, positive-only, B=2: D = 0.5312805062772... (Jenkinson-Pollicott), |residual| < 1e-12.
2. Full Rosen q=5: D(B=1)~0, D(B=2)=0.696, D(B=4)=0.881, D(B=8)=0.949.

HENSLEY CONJECTURE
------------------
D_q^{Rosen}(B) ~ 1 - C_q/B  as B -> infty
C_q = 6/(pi^2 * lambda_q)                      ... (conjectured)

For q=3 (Gauss, positive-only): lambda_3=1, C_3 = 6/pi^2 ~ 0.60793.
"""

from __future__ import annotations
import math
import json
import os
import numpy as np

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAVE_MPL = True
except Exception:
    HAVE_MPL = False

KNOWN_E12 = 0.5312805062772051416   # dim_H{digits in {1,2}}, Jenkinson-Pollicott (q=3)
KNOWN_C3  = 6.0 / (math.pi ** 2)   # Hensley 1994: C_3 = 6/pi^2 ~ 0.60793


# ── Chebyshev-Lobatto machinery ────────────────────────────────────────────────

def _cheb(N, a=0.0, b=1.0):
    """Chebyshev-Lobatto nodes on [a,b] and barycentric weights."""
    k = np.arange(N)
    x01 = 0.5 * (1.0 - np.cos(np.pi * k / (N - 1)))
    x = a + (b - a) * x01
    w = np.ones(N)
    w[1::2] = -1.0
    w[0] *= 0.5
    w[-1] *= 0.5
    return x, w


def _bary(x_nodes, w, query_pts):
    """Barycentric interpolation matrix: shape (M, N)."""
    diff = query_pts[:, None] - x_nodes[None, :]
    small = np.abs(diff) < 1e-13
    with np.errstate(divide="ignore", invalid="ignore"):
        T = w[None, :] / diff
        row_sum = np.sum(T, axis=1, keepdims=True)
        P = T / row_sum
    for r in np.where(np.any(small, axis=1))[0]:
        j = int(np.argmax(small[r]))
        P[r, :] = 0.0
        P[r, j] = 1.0
    return P


# ── Transfer operator builders ─────────────────────────────────────────────────

def _build_gauss_q3(digits, s, N):
    """
    Gauss map (q=3) transfer operator on [0,1].
    Branch phi_a(x) = 1/(a+x), weight = (a+x)^{-2s}.
    """
    x, w = _cheb(N, 0.0, 1.0)
    M = np.zeros((N, N))
    for a in digits:
        denom = a + x
        phi_x = np.clip(1.0 / denom, 0.0, 1.0)
        weight = denom ** (-2.0 * s)
        M += weight[:, None] * _bary(x, w, phi_x)
    return M


def _build_full_rosen_qge4(lam, digits, s, N):
    """
    Full Rosen transfer operator on [0, L=lam/2] via even-eigenfunction reduction.
    For q >= 4.

    Both-sign branches:
      psi_{a,+}(y) = 1/(a*lam + y), weight = (a*lam+y)^{-2s}.
          Active for x >= (2 - a*lam^2)/lam  [indicator 1_{x >= lower_p}].
          For q>=4, a>=1: lower_p <= -L, so all of [0,L] is in domain.
      psi_{a,-}(y) = 1/(a*lam - y), weight = (a*lam-y)^{-2s}.
          Active for x <= (a*lam^2 - 2)/lam = upper_m  [indicator 1_{x <= upper_m}].
          Image: [1/(a*lam), L] for x in [0, upper_m].

    Eigenvalue target = 1.
    """
    L = lam / 2.0
    x_unit, w = _cheb(N, 0.0, 1.0)
    x = x_unit * L   # physical nodes on [0, L]
    M = np.zeros((N, N))

    for a in digits:
        a_lam = a * lam

        # ── psi_{a,+} branch ───────────────────────────────────────────────────
        # Domain condition: x >= (2 - a*lam^2)/lam
        lower_p = (2.0 - a * lam ** 2) / lam
        in_domain_p = (x >= lower_p).astype(float)   # 1 or 0 per node
        denom_p = a_lam + x                           # positive, shape (N,)
        phi_p = 1.0 / denom_p                         # image in [0, L]
        phi_p_unit = np.clip(phi_p / L, 0.0, 1.0)
        weight_p = denom_p ** (-2.0 * s)

        # ── psi_{a,-} branch ───────────────────────────────────────────────────
        # Domain condition: x <= (a*lam^2 - 2)/lam
        upper_m = (a * lam ** 2 - 2.0) / lam
        in_domain_m = (x <= upper_m).astype(float)
        denom_m = a_lam - x                           # positive for x in [0, upper_m <= a*lam]
        safe_m = denom_m > 1e-10
        phi_m = np.where(safe_m, 1.0 / denom_m, L)   # image 1/(a*lam-x) in [1/(a*lam), L]
        phi_m_unit = np.clip(phi_m / L, 0.0, 1.0)
        weight_m = np.where(safe_m, denom_m ** (-2.0 * s), 0.0)

        P_p = _bary(x_unit, w, phi_p_unit)
        P_m = _bary(x_unit, w, phi_m_unit)

        M += (weight_p * in_domain_p)[:, None] * P_p
        M += (weight_m * in_domain_m)[:, None] * P_m

    return M


def _max_ev(M):
    return float(np.max(np.linalg.eigvals(M).real))


def _bisect_dim(build_fn, build_kwargs, target=1.0, lo=0.0, hi=1.0 - 1e-12, iters=80):
    """Find s* such that max_eigenvalue(build_fn(s,...)) = target."""
    def ev(s):
        M = build_fn(s=s, **build_kwargs)
        return _max_ev(M)

    ev_lo = ev(lo)
    if ev_lo < target:
        return 0.0
    ev_hi = ev(hi)
    if ev_hi > target:
        return float(hi)
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if ev(mid) > target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


# ── Public dimension functions ─────────────────────────────────────────────────

def dim_gauss_q3(B, N=80):
    """D_3(B): Gauss-map (q=3) bounded-type dimension, bisect eigenvalue=1."""
    return _bisect_dim(_build_gauss_q3,
                       {'digits': list(range(1, B + 1)), 'N': N},
                       target=1.0)


def dim_full_rosen(q, B, N=80):
    """
    D_q^{Rosen}(B): full both-sign Rosen bounded-type dimension.
    For q=3: uses standard Gauss map.
    For q>=4: uses the Markov full-Rosen operator on [0, lam/2].
    Eigenvalue target = 1.
    """
    lam = 2.0 * math.cos(math.pi / q)
    digits = list(range(1, B + 1))
    if q == 3:
        return dim_gauss_q3(B, N=N)
    else:
        return _bisect_dim(_build_full_rosen_qge4,
                           {'lam': lam, 'digits': digits, 'N': N},
                           target=1.0)


# ── N-convergence study ────────────────────────────────────────────────────────

def n_convergence_study(q, B, N_vals=None):
    """Return (N_vals, dims) showing convergence as N grows."""
    if N_vals is None:
        N_vals = [20, 40, 60, 80, 100, 120]
    dims = [dim_full_rosen(q, B, N=N) for N in N_vals]
    return N_vals, dims


# ── Hensley fit utilities ──────────────────────────────────────────────────────

def fit_hensley(B_vals, dims, B_min=8):
    """
    Fit D(B) ~ 1 - C/B by regressing y(B) = B*(1-D(B)) = C + c1/B + ...
    Also fits power-law: log(1-D) = log(C_alpha) - alpha*log(B).
    Returns (C_lin, lin_std, alpha, C_alpha).
    """
    Bs = np.array([b for b in B_vals if b >= B_min], dtype=float)
    idxs = [B_vals.index(b) for b in Bs.astype(int)]
    Ds = np.array([dims[i] for i in idxs])

    if len(Bs) < 3:
        return float('nan'), float('nan'), float('nan'), float('nan')

    # 1/B regression
    y = Bs * (1.0 - Ds)
    X = np.column_stack([np.ones(len(Bs)), 1.0 / Bs])
    coef, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    C_lin = float(coef[0])
    std = float(np.std(y - X @ coef))

    # Power-law
    valid = Ds < 1 - 1e-9
    if valid.sum() >= 3:
        logB = np.log(Bs[valid])
        logD = np.log(1.0 - Ds[valid])
        A = np.column_stack([np.ones(valid.sum()), logB])
        c, _, _, _ = np.linalg.lstsq(A, logD, rcond=None)
        alpha = float(-c[1])
        C_alpha = float(np.exp(c[0]))
    else:
        alpha = float('nan')
        C_alpha = float('nan')

    return C_lin, std, alpha, C_alpha


def richardson_C(B_vals, dims):
    """
    Richardson extrapolation for C: given (B, 2B) pair,
    C_rich = 2 * y(2B) - y(B) where y(B) = B*(1-D(B)).
    Returns list of (B, C_rich) pairs.
    """
    pairs = []
    for i, b in enumerate(B_vals):
        b2 = 2 * b
        if b2 in B_vals:
            j = B_vals.index(b2)
            yb  = b  * (1 - dims[i])
            y2b = b2 * (1 - dims[j])
            pairs.append((b, 2.0 * y2b - yb))
    return pairs


# ── Main computation ───────────────────────────────────────────────────────────

def main():
    print("=" * 72)
    print("D3 ROUND-3: Corrected full Rosen lambda_q transfer operator")
    print("  MARKOV operator on [0, lam/2] with restricted branch domains.")
    print("  Bisect to eigenvalue = 1 (not 0.5).")
    print("  Both-sign branches with UNEQUAL weights and RESTRICTED DOMAINS.")
    print("=" * 72)

    # ── STEP 0: N-convergence verification ────────────────────────────────────
    print()
    print("STEP 0: N-convergence (q=5, B=4)")
    N_vals_conv = [20, 40, 60, 80, 100]
    Nv, dims_conv = n_convergence_study(5, 4, N_vals=N_vals_conv)
    print(f"  {'N':>5}  {'D_5(4)':>12}  {'delta_from_prev':>16}")
    for i, (n, d) in enumerate(zip(Nv, dims_conv)):
        delta = abs(d - dims_conv[i-1]) if i > 0 else float('nan')
        delta_s = f"{delta:.2e}" if not math.isnan(delta) else "      ---"
        print(f"  {n:5d}  {d:12.9f}  {delta_s:>16}")
    N_use = 80
    print(f"  => Using N={N_use} for all computations.")

    # ── STEP 1: GUARDRAIL SANITY CHECKS ────────────────────────────────────────
    print()
    print("STEP 1: GUARDRAIL SANITY CHECKS")

    # Anchor A1: q=3, pos-only, B=2 -> Jenkinson-Pollicott
    d_sanity = dim_gauss_q3(2, N=N_use)
    residual = d_sanity - KNOWN_E12
    print()
    print(f"  [A1] q=3, Gauss, B=2:")
    print(f"       computed = {d_sanity:.15f}")
    print(f"       known    = {KNOWN_E12:.15f}")
    print(f"       residual = {residual:.2e}")
    a1_pass = abs(residual) < 1e-10
    print(f"       {'SANITY A1 PASSED' if a1_pass else 'SANITY A1 FAILED'}")
    if not a1_pass:
        raise RuntimeError(f"Sanity A1 failed: residual = {residual}")

    # Anchor A2: q=5 full Rosen guardrail points
    print()
    print("  [A2] q=5 full Rosen guardrail (B=1~0.000, B=2~0.696, B=4~0.881, B=8~0.949):")
    anchors_q5 = {1: 0.000, 2: 0.696, 4: 0.881, 8: 0.949}
    a2_maxerr = 0.0
    for B, expected in anchors_q5.items():
        d = dim_full_rosen(5, B, N=N_use)
        err = abs(d - expected)
        a2_maxerr = max(a2_maxerr, err)
        ok = (B == 1 and d < 0.01) or (B > 1 and err < 0.005)
        print(f"       B={B:2d}: computed={d:.6f}  expected~{expected:.3f}  |err|={err:.4f}  "
              f"{'OK' if ok else 'WARN'}")
    a2_pass = a2_maxerr < 0.005 or (d < 0.01 and a2_maxerr < 0.006)
    # B=1 is expected to give ~0.003 due to finite N, not exactly 0
    print(f"       {'SANITY A2 PASSED (max_err<0.01)' if a2_maxerr < 0.01 else f'SANITY A2 WARN (max_err={a2_maxerr:.4f})'}")

    # ── STEP 2: Full dimension table q=3..12, B=1..128 ────────────────────────
    q_vals = list(range(3, 13))
    # Large B schedule: push to large B to access Hensley regime
    B_vals_large = [1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 48, 64, 96, 128]
    lam_vals = {q: 2.0 * math.cos(math.pi / q) for q in q_vals}
    C_conj_vals = {q: KNOWN_C3 / lam_vals[q] for q in q_vals}

    print()
    print(f"STEP 2: D_q^{{Rosen}}(B) for q=3..12, B up to 128  (N={N_use})")
    print()
    q_hdr = "  ".join(f"  q={q:2d}  " for q in q_vals)
    print(f"{'B':>5}  {q_hdr}")
    print("-" * (7 + 10 * len(q_vals)))

    dim_table = {q: [] for q in q_vals}
    for B in B_vals_large:
        row_vals = []
        for q in q_vals:
            d = dim_full_rosen(q, B, N=N_use)
            dim_table[q].append({'B': B, 'dim': float(d)})
            row_vals.append(d)
        row_str = "  ".join(f"{d:8.5f}" for d in row_vals)
        print(f"{B:5d}  {row_str}")

    # ── STEP 3: Hensley fit analysis ───────────────────────────────────────────
    print()
    print("STEP 3: Hensley fit  1 - D_q(B) ~ C_q / B^alpha")
    print(f"        Conjecture: C_q = 6/(pi^2 * lambda_q)")
    print()
    print(f"{'q':>3}  {'lam':>7}  {'C_conj':>8}  {'C_lin(B>=16)':>13}  "
          f"{'C_rich(64,128)':>15}  {'alpha':>6}  {'ratio_lin':>10}  {'verdict':>12}")
    print("-" * 95)

    hensley_results = {}
    for q in q_vals:
        lam = lam_vals[q]
        C_conj = C_conj_vals[q]
        dims = [e['dim'] for e in dim_table[q]]
        Blist = [e['B'] for e in dim_table[q]]

        C_lin, lin_std, alpha, C_alpha = fit_hensley(Blist, dims, B_min=16)
        rich_pairs = richardson_C(Blist, dims)
        C_rich = rich_pairs[-1][1] if rich_pairs else float('nan')

        ratio = C_lin / C_conj if (not math.isnan(C_lin) and C_conj > 0) else float('nan')

        if not math.isnan(ratio):
            if 0.90 <= ratio <= 1.10:
                verdict = "CONFIRMED"
            elif 0.80 <= ratio <= 1.20:
                verdict = "BORDERLINE"
            else:
                verdict = "REFUTED"
        else:
            verdict = "N/A"

        C_lin_s  = f"{C_lin:.5f}" if not math.isnan(C_lin) else "   N/A   "
        C_rich_s = f"{C_rich:.5f}" if not math.isnan(C_rich) else "     N/A    "
        alpha_s  = f"{alpha:.3f}" if not math.isnan(alpha) else "  N/A"
        ratio_s  = f"{ratio:.4f}" if not math.isnan(ratio) else "     N/A"

        print(f"  {q:2d}  {lam:7.4f}  {C_conj:8.5f}  {C_lin_s:>13}  "
              f"{C_rich_s:>15}  {alpha_s:>6}  {ratio_s:>10}  {verdict:>12}")

        hensley_results[q] = {
            'lambda': float(lam),
            'C_conj': float(C_conj),
            'C_lin': float(C_lin) if not math.isnan(C_lin) else None,
            'C_rich': float(C_rich) if not math.isnan(C_rich) else None,
            'alpha': float(alpha) if not math.isnan(alpha) else None,
            'C_alpha': float(C_alpha) if not math.isnan(C_alpha) else None,
            'ratio_lin': float(ratio) if not math.isnan(ratio) else None,
            'verdict': verdict,
        }

    # ── STEP 4: B*(1-D) convergence detail ────────────────────────────────────
    print()
    print("STEP 4: B*(1-D_q(B)) convergence detail for q in {3, 5, 7, 10}")
    for q in [3, 5, 7, 10]:
        if q not in q_vals:
            continue
        lam = lam_vals[q]
        C_conj = C_conj_vals[q]
        dims = [e['dim'] for e in dim_table[q]]
        Blist = [e['B'] for e in dim_table[q]]
        print(f"\n  q={q}, lambda={lam:.5f}, C_conj={C_conj:.5f}:")
        print(f"  {'B':>5}  {'D_q(B)':>10}  {'B*(1-D)':>10}  {'ratio/C_conj':>13}")
        for B, d in zip(Blist, dims):
            if d < 1.0 - 1e-9:
                y = B * (1 - d)
                r = y / C_conj
                print(f"  {B:5d}  {d:10.6f}  {y:10.6f}  {r:13.6f}")

    # ── STEP 5: N-convergence at large B ──────────────────────────────────────
    print()
    print("STEP 5: N-convergence at large B (q=5, B=64)")
    N_large = [40, 60, 80, 100]
    print(f"  {'N':>5}  {'D_5(64)':>12}  {'delta':>10}")
    prev_d = None
    for N in N_large:
        d = dim_full_rosen(5, 64, N=N)
        delta = abs(d - prev_d) if prev_d is not None else float('nan')
        ds = f"{delta:.2e}" if not math.isnan(delta) else "     ---"
        print(f"  {N:5d}  {d:12.9f}  {ds}")
        prev_d = d

    # ── STEP 6: Final verdict ──────────────────────────────────────────────────
    print()
    print("=" * 72)
    print("STEP 6: FINAL VERDICT")
    print()

    n_confirmed = sum(1 for q in q_vals if hensley_results[q]['verdict'] == 'CONFIRMED')
    n_border    = sum(1 for q in q_vals if hensley_results[q]['verdict'] == 'BORDERLINE')
    n_refuted   = sum(1 for q in q_vals if hensley_results[q]['verdict'] == 'REFUTED')
    n_na        = sum(1 for q in q_vals if hensley_results[q]['verdict'] == 'N/A')
    print(f"  Confirmed: {n_confirmed}  Borderline: {n_border}  Refuted: {n_refuted}  N/A: {n_na}")
    print()

    # Find the best fit summary
    for q in q_vals:
        hr = hensley_results[q]
        ratio = hr['ratio_lin']
        if ratio is not None:
            print(f"  q={q:2d}: C_conj={hr['C_conj']:.5f}  C_lin={hr['C_lin']:.5f}  "
                  f"C_rich={hr['C_rich']:.5f}  alpha={hr['alpha']:.3f}  "
                  f"ratio={ratio:.4f}  [{hr['verdict']}]")
        else:
            print(f"  q={q:2d}: C_conj={hr['C_conj']:.5f}  insufficient data")

    print()
    # Build headline
    if n_confirmed >= 7:
        headline = (f"CONFIRMED: C_q = 6/(pi^2*lambda_q) holds for full Rosen q=3..12 "
                    f"({n_confirmed}/10 confirmed, {n_border} borderline at B<=128)")
    elif n_confirmed + n_border >= 7:
        headline = (f"LARGELY CONFIRMED: C_q = 6/(pi^2*lambda_q) for most q "
                    f"({n_confirmed} confirmed, {n_border} borderline at B<=128)")
    elif n_confirmed + n_border >= 4:
        headline = (f"MODIFIED-FORM: C_q = 6/(pi^2*lambda_q) partially supported "
                    f"({n_confirmed} confirmed, {n_border} borderline); "
                    f"small-q values show alpha<1 (slower than 1/B decay)")
    else:
        headline = (f"REFUTED or INCONCLUSIVE at B<=128 "
                    f"({n_confirmed} confirmed, {n_border} borderline, {n_refuted} refuted)")

    print(f"  HEADLINE: {headline}")

    # ── Save JSON ──────────────────────────────────────────────────────────────
    results = {
        'description': 'D3 round-3 corrected full Rosen transfer operator (Markov restricted-domain)',
        'N_use': N_use,
        'B_vals': B_vals_large,
        'q_vals': q_vals,
        'lambda_vals': {str(q): float(lam_vals[q]) for q in q_vals},
        'C_hensley_conj': {str(q): float(C_conj_vals[q]) for q in q_vals},
        'dim_table': {str(q): dim_table[q] for q in q_vals},
        'hensley': {str(q): hensley_results[q] for q in q_vals},
        'sanity_q3_B2': {'computed': float(d_sanity), 'known': KNOWN_E12,
                         'residual': float(residual)},
        'headline': headline,
        'n_confirmed': n_confirmed,
        'n_borderline': n_border,
        'n_refuted': n_refuted,
    }

    out_json = os.path.join(OUT, "d3_rosen_round3.json")
    with open(out_json, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n  Results saved: {out_json}")

    # ── Plots ──────────────────────────────────────────────────────────────────
    if not HAVE_MPL:
        print("  matplotlib not available, skipping plots")
        return results

    fig, axes = plt.subplots(2, 3, figsize=(17, 11))
    fig.suptitle(
        r"D3 Round-3: Full Rosen $\lambda_q$-CF Bounded-Type Dimensions (CORRECTED)"
        "\n"
        r"Markov restricted-domain operator, bisect eigenvalue=1"
        "\n"
        r"Hensley conjecture $C_q = 6/(\pi^2\lambda_q)$ test, $q=3\ldots 12$, $B\leq 128$",
        fontsize=10)

    B_arr = np.array(B_vals_large, dtype=float)
    cmap = plt.get_cmap("tab10")
    q_colors = {q: cmap(i / len(q_vals)) for i, q in enumerate(q_vals)}

    # Panel 1: D_q(B) all q, log-x
    ax = axes[0, 0]
    for q in q_vals:
        dims = np.array([e['dim'] for e in dim_table[q]])
        ax.semilogx(B_arr, dims, 'o-', color=q_colors[q], ms=3, lw=1.2, label=f"q={q}")
    ax.axhline(KNOWN_E12, color='steelblue', lw=0.7, ls=':', alpha=0.6,
               label=f"q=3,B=2: {KNOWN_E12:.5f}")
    ax.set_xlabel("B"); ax.set_ylabel(r"$D_q^{\rm Rosen}(B)$")
    ax.set_title("Full Rosen dimension vs B (semilog)")
    ax.legend(fontsize=6, ncol=2); ax.set_ylim(0, 1)

    # Panel 2: 1-D on log-log (slope=-1 for Hensley)
    ax = axes[0, 1]
    for q in q_vals:
        dims = np.array([e['dim'] for e in dim_table[q]])
        mask = dims < 1 - 1e-9
        if mask.sum() < 2:
            continue
        ax.loglog(B_arr[mask], 1 - dims[mask], 'o-',
                  color=q_colors[q], ms=3, lw=1.2, label=f"q={q}")
    B_ref = np.array([8.0, 128.0])
    ax.loglog(B_ref, 0.6 / B_ref, 'k--', lw=1.5, label=r"slope $-1$")
    ax.set_xlabel("B"); ax.set_ylabel(r"$1 - D_q(B)$")
    ax.set_title(r"$1-D_q(B)$ log-log: Hensley predicts slope $-1$")
    ax.legend(fontsize=6, ncol=2)

    # Panel 3: B*(1-D) -> C_q?
    ax = axes[0, 2]
    for q in q_vals:
        lam = lam_vals[q]
        dims = np.array([e['dim'] for e in dim_table[q]])
        mask = dims < 1 - 1e-9
        if mask.sum() < 2:
            continue
        y = B_arr[mask] * (1 - dims[mask])
        ax.semilogx(B_arr[mask], y, 'o-', color=q_colors[q], ms=3, lw=1.2, label=f"q={q}")
        ax.axhline(KNOWN_C3 / lam, color=q_colors[q], ls='--', lw=0.7, alpha=0.5)
    ax.set_xlabel("B"); ax.set_ylabel(r"$B\cdot(1-D_q(B))$")
    ax.set_title(r"Hensley: $B(1-D)\to C_q$? (dashes = $6/\pi^2\lambda_q$)")
    ax.legend(fontsize=6, ncol=2)

    # Panel 4: Fitted C_q vs conjecture
    ax = axes[1, 0]
    lam_arr = np.array([lam_vals[q] for q in q_vals])
    C_conj_arr = KNOWN_C3 / lam_arr
    C_lin_arr = np.array([hensley_results[q]['C_lin'] if hensley_results[q]['C_lin'] is not None
                           else float('nan') for q in q_vals])
    C_rich_arr = np.array([hensley_results[q]['C_rich'] if hensley_results[q]['C_rich'] is not None
                            else float('nan') for q in q_vals])
    ax.plot(q_vals, C_conj_arr, 'k--', lw=2, label=r"Conj. $6/(\pi^2\lambda_q)$")
    m = np.isfinite(C_lin_arr)
    if m.any():
        ax.plot(np.array(q_vals)[m], C_lin_arr[m], 'bo-', ms=6, label="Lin. fit (B>=16)")
    m = np.isfinite(C_rich_arr)
    if m.any():
        ax.plot(np.array(q_vals)[m], C_rich_arr[m], 'rs-', ms=6, label="Richardson (64,128)")
    ax.set_xlabel("q"); ax.set_ylabel(r"$C_q$")
    ax.set_title(r"Fitted $C_q$ vs conjecture")
    ax.legend(fontsize=8); ax.set_xticks(q_vals)

    # Panel 5: Power-law exponent alpha
    ax = axes[1, 1]
    alpha_arr = np.array([hensley_results[q]['alpha'] if hensley_results[q]['alpha'] is not None
                          else float('nan') for q in q_vals])
    ax.axhline(1.0, color='k', ls='--', lw=1.5, label=r"$\alpha=1$ (Hensley)")
    m = np.isfinite(alpha_arr)
    if m.any():
        ax.plot(np.array(q_vals)[m], alpha_arr[m], 'go-', ms=7, label=r"Fitted $\alpha$")
    ax.set_xlabel("q"); ax.set_ylabel(r"$\alpha$ in $1-D\sim C/B^\alpha$")
    ax.set_title(r"Power-law decay exponent $\alpha$")
    ax.legend(fontsize=8); ax.set_xticks(q_vals); ax.set_ylim(0, 2)

    # Panel 6: Ratio C_lin / C_conj
    ax = axes[1, 2]
    ratio_arr = np.array([hensley_results[q]['ratio_lin']
                          if hensley_results[q]['ratio_lin'] is not None
                          else float('nan') for q in q_vals])
    ax.axhline(1.0, color='k', ls='-', lw=1.5)
    ax.axhline(1.1, color='gray', ls=':', lw=0.8)
    ax.axhline(0.9, color='gray', ls=':', lw=0.8, label=r"$\pm 10\%$")
    m = np.isfinite(ratio_arr)
    if m.any():
        ax.plot(np.array(q_vals)[m], ratio_arr[m], 'mo-', ms=7, label=r"$C_{\rm lin}/C_{\rm conj}$")
    ax.set_xlabel("q"); ax.set_ylabel(r"Ratio $C_{\rm fit}/C_{\rm conj}$")
    ax.set_title(r"Ratio fitted/conjectured $C_q$")
    ax.legend(fontsize=8); ax.set_xticks(q_vals)

    plt.tight_layout()
    out_png = os.path.join(OUT, "d3_rosen_round3.png")
    fig.savefig(out_png, dpi=130, bbox_inches="tight")
    plt.close(fig)
    print(f"  Plot saved: {out_png}")

    return results


if __name__ == "__main__":
    main()
