"""
d3_rosen_nuclear_gap.py
=======================
NUCLEAR (holomorphic disc-algebra) recomputation of the 1-D Rosen lambda_q-CF
transfer-operator SPECTRAL GAP at the bounded-type dimension s = D_q.

WHY THIS EXISTS
---------------
The prior run `code/d3_rosen_spectral_gap.py` (-> out/d3_rosen_spectral_gap.json)
computed the gap via BARYCENTRIC CHEBYSHEV COLLOCATION on [0, lam/2].  That
discretization resolves the leading eigenvalue lambda_1 ~ 1 fine, but FAILS to
N-converge on lambda_2: the gap drifts ~1e-2 under N=40..120 and never stabilizes
to 1e-6 (collocation of a non-self-adjoint transfer operator converges only
algebraically, and the sub-leading eigenvalue is the worst-resolved mode).

This script replaces collocation by the NUCLEAR Fredholm-determinant
discretization used in `code/zeta_mayer_rosen.py`: each Markov-partition
component g_i is represented by its Taylor coefficients about a real center c_i,
extracted by Cauchy's formula (FFT on a circle).  Because every Rosen branch
theta_n sends the partition discs strictly inside one another (MMS Lemma 4.4),
the operator is nuclear of order 0 (MMS Thm 4.10) and the N-truncated block
matrix spectrum converges GEOMETRICALLY in N.

THE OPERATOR
------------
Same bounded-type Rosen lambda_q-CF map as d3_rosen_spectral_gap.py: the
both-sign nearest-lambda-multiple Gauss map restricted to digits a in {1..B}
(the bounded-type survivor set whose Hausdorff dimension is D_q(B)).  We build
it on the MMS even/odd reduced block structure (eqs 32-34 of Mayer-Muehlenbruch-
Stroemberg, DCDS 32 (2012) 2453, arXiv:0912.2236) -- the SAME map, but each
branch theta_n = S T^n acts between holomorphic disc-algebras on the Markov
partition cells Phi_i subset [-lam/2, 0].  The MMS reduction makes the indicator
("restricted domain") of d3_rosen_round3 unnecessary: branch incidence is
encoded as which (i,j) blocks are nonzero, so NO non-analytic cutoff enters and
the Cauchy-FFT extraction is exact.

The digit-tail operators L^inf_{n,s} are TRUNCATED at l <= B (no analytic
remainder) -- this is exactly the bounded-type restriction "digits <= B", and is
what makes lambda_1 = 1 at s = D_q(B) (the full untruncated tails would give the
full-measure Gauss map, dimension 1, lambda_1 = 1 only at s = 1).

GAP
---
At s = D_q(B) the even-sector reduced operator L_{s,+} carries the leading
eigenvalue lambda_1 ~ 1 (sanity-checked below).  The full transfer-operator
spectrum is the UNION of the even (L_{s,+}) and odd (L_{s,-}) reduced spectra.
We read lambda_1 (max modulus over BOTH sectors) and lambda_2 (next), then

    gap   = |lambda_2 / lambda_1|
    alpha_q = -log(gap)              (decay-of-correlations rate).

N-convergence study over N = 20, 30, 40, 50 reports Delta(gap); the nuclear
method should be flat to many digits where collocation drifted ~1e-2.

STRUCTURAL CAVEAT (DO NOT VIOLATE)
----------------------------------
This is the 1-D CF-map decay-of-correlations gap ONLY.  It does NOT prove
horocycle effective equidistribution: the 2-D BCZ-Farey section is parabolic /
zero-entropy with polynomial mixing, NO spectral gap, 1 in the essential
spectrum.  No interval certification, no Lean here.

SELF-CONTAINED.  The nuclear-block machinery (_atomic_block, disc_centers,
partition_points, hecke_params, disc_radii) is COPIED below from
zeta_mayer_rosen.py so this script does not import it at runtime (that file is
being edited on a concurrent track).  D_q is computed by an independent COPY of
the bounded-type dimension bisection (digit-truncated nuclear operator), and is
cross-checked against d3_rosen_round3.dim_full_rosen if that module imports.
"""

from __future__ import annotations
import math
import json
import os
import numpy as np

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)

# q=3 Gauss anchor (Jenkinson-Pollicott dim_H{digits 1,2}) for the convenience cross-check.
KNOWN_E12 = 0.5312805062772051416


# ===========================================================================
#  Markov-partition geometry  (COPIED from zeta_mayer_rosen.py)
# ===========================================================================

def _cf_value(digits, lam):
    """Value of the finite lambda_q-CF [[0; digits]] = ST^{d1} ST^{d2} ... 0."""
    x = 0.0
    for a in reversed(digits):
        x = -1.0 / (a * lam + x)
    return x


def hecke_params(q):
    lam = 2.0 * math.cos(math.pi / q)
    if q % 2 == 0:
        hq = (q - 2) // 2
        kappa = hq
    else:
        hq = (q - 3) // 2
        kappa = 2 * hq + 1
    return lam, hq, kappa


def partition_points(q):
    """Sorted boundary points phi_0<...<phi_kappa of the Markov partition of
    [-lambda/2, 0]; Phi_i=(phi_{i-1},phi_i).  (MMS Sec 2.6.)"""
    lam, hq, kappa = hecke_params(q)
    L = lam / 2.0
    if q % 2 == 0:
        phis = []
        for i in range(0, hq + 1):
            d = [1] * (hq - i)
            phis.append(_cf_value(d, lam) if d else 0.0)
        phis[0] = -L
        return sorted(phis)
    else:
        phi = {0: -L}
        for i in range(1, hq + 1):
            phi[2 * i] = _cf_value([1] * (hq - i) + [2] + [1] * hq, lam)
        for i in range(0, (kappa - 1) // 2 + 1):
            d = [1] * (hq - i)
            phi[2 * i + 1] = _cf_value(d, lam) if d else 0.0
        ordered = [phi[k] for k in range(0, kappa + 1)]
        return sorted(ordered)


def disc_centers(q):
    """Real center c_i (midpoint of Phi_i) for each component i=1..kappa."""
    pts = partition_points(q)
    return [0.5 * (pts[i - 1] + pts[i]) for i in range(1, len(pts))]


def disc_radii(q, safety=2.5):
    """Per-disc length-scale rad_i = safety*half-width(Phi_i): the Cauchy-FFT
    contour radius and the monomial-basis normalization."""
    pts = partition_points(q)
    return [safety * 0.5 * (pts[i] - pts[i - 1]) for i in range(1, len(pts))]


# ===========================================================================
#  Single-branch nuclear block  (COPIED from zeta_mayer_rosen.py)
# ===========================================================================

def _atomic_block(s, i_center, i_rad, j_center, j_rad, N, lam, n, neg, n_fft):
    """
    Single Rosen branch theta_n in NORMALIZED monomial bases, returned as the
    (N x N) matrix taking Taylor coeffs of g_j (about c_j, scaled by rad_j) to
    Taylor coeffs of weight*g_j(theta_n) (about c_i, scaled by rad_i), via
    Cauchy-FFT on |z-c_i|=rad_i.
      neg=False (n>=1):  (B g)(z) = (theta_n')^s  g(-1/(z+n*lam))
      neg=True  (n>=1):  (B g)(z) = (theta_-n')^s g(+1/(z-n*lam))
    HOLOMORPHIC weight (denom^2)^{-s} avoids the denom<0 branch cut.
    """
    thetas = 2.0 * np.pi * np.arange(n_fft) / n_fft
    zpts = i_center + i_rad * np.exp(1j * thetas)
    if not neg:
        denom = zpts + n * lam
        arg = -1.0 / denom
    else:
        denom = zpts - n * lam
        arg = 1.0 / denom
    weight = (denom * denom) ** (-s)
    base = (arg - j_center) / j_rad
    S = np.empty((n_fft, N), dtype=complex)
    powk = np.ones_like(base)
    for k in range(N):
        S[:, k] = weight * powk
        powk = powk * base
    C = np.fft.fft(S, axis=0) / n_fft
    return C[:N, :]


# ===========================================================================
#  Bounded-type reduced block matrix (digit-truncated tails -> digits <= B)
# ===========================================================================
#
#  This is the MMS even/odd reduced operator L_{s,sign} (eqs 32-34) with every
#  L^inf_{n,s} tail TRUNCATED at l <= B (no analytic remainder).  Truncating the
#  tail at B is exactly the bounded-type restriction "CF digits a in {1..B}",
#  i.e. the same survivor set whose dimension is D_q(B) and the same map the
#  collocation script discretized -- now on the nuclear basis.

def _tail_trunc_block(s, ic, ir, jc, jr, N, lam, n0, neg, B, n_fft):
    """sum over branches l = n0 .. B of the single-branch nuclear block."""
    tot = np.zeros((N, N), dtype=complex)
    for l in range(n0, B + 1):
        tot += _atomic_block(s, ic, ir, jc, jr, N, lam, l, neg, n_fft)
    return tot


def build_reduced_matrix_bounded(q, s, N, sign, B, n_fft=None):
    """
    (kappa*N)x(kappa*N) block matrix of the bounded-type reduced operator
    L_{s,sign} (sign=+1 even, -1 odd), digits a in {1..B}, on the per-component
    Taylor bases.  Block incidence follows MMS eqs 32-34; the digit-tail
    L^inf operators are truncated at l <= B.
    """
    lam, hq, kappa = hecke_params(q)
    if n_fft is None:
        n_fft = max(4 * N, 64)
    c = disc_centers(q)
    rad = disc_radii(q)
    blocks = {}

    def add(i, j, mat):
        blocks[(i, j)] = blocks.get((i, j), 0) + mat

    def L_single(i, j, n, neg):
        return _atomic_block(s, c[i - 1], rad[i - 1], c[j - 1], rad[j - 1],
                             N, lam, n, neg, n_fft)

    def L_inf(i, j, n0, neg):
        return _tail_trunc_block(s, c[i - 1], rad[i - 1], c[j - 1], rad[j - 1],
                                 N, lam, n0, neg, B, n_fft)

    if q == 3:
        # scalar Gauss-degenerate cell: kappa=1, tails 3.. and -2..
        add(1, 1, L_inf(1, 1, 3, False))
        add(1, 1, sign * L_inf(1, 1, 2, True))
    elif q % 2 == 0:
        h = hq                       # kappa == h
        add(1, h, L_inf(1, h, 2, False))
        add(1, h, sign * L_inf(1, h, 1, True))
        for i in range(2, h + 1):
            add(i, i - 1, L_single(i, i - 1, 1, False))
            add(i, h, L_inf(i, h, 2, False))
            add(i, h, sign * L_inf(i, h, 1, True))
    else:
        k = kappa
        twoh = 2 * hq
        add(1, twoh, L_single(1, twoh, 2, False))
        add(1, k, L_inf(1, k, 3, False))
        add(1, twoh, sign * L_single(1, twoh, 1, True))
        add(1, k, sign * L_inf(1, k, 2, True))
        add(2, k, L_inf(2, k, 2, False))
        add(2, twoh, sign * L_single(2, twoh, 1, True))
        add(2, k, sign * L_inf(2, k, 2, True))
        for i in range(3, k + 1):
            add(i, i - 2, L_single(i, i - 2, 1, False))
            add(i, k, L_inf(i, k, 2, False))
            add(i, twoh, sign * L_single(i, twoh, 1, True))
            add(i, k, sign * L_inf(i, k, 2, True))

    M = np.zeros((kappa * N, kappa * N), dtype=complex)
    for (i, j), blk in blocks.items():
        M[(i - 1) * N:i * N, (j - 1) * N:j * N] = blk
    return M


# ===========================================================================
#  Bounded-type dimension D_q(B) on the SAME nuclear operator (self-contained)
# ===========================================================================

def _lam_max_even(q, s, N, B, n_fft=None):
    M = build_reduced_matrix_bounded(q, s + 0j, N, +1, B, n_fft=n_fft)
    return float(np.max(np.abs(np.linalg.eigvals(M))))


# --- standard Gauss-map nuclear anchor (q=3 Jenkinson-Pollicott) ---
# The MMS scalar q=3 cell (lam=1, tails theta_3.. / theta_{-2}..) is a DEGENERATE
# form that does NOT reproduce the standard Gauss-map [0,1] survivor-set dimension,
# so for the q=3 convenience anchor we use the standard Gauss map 1/(a+x) on [0,1]
# in the SAME nuclear (disc-algebra / Cauchy-FFT) discretization.
_GAUSS_Z0 = (math.sqrt(5.0) - 1.0) / 2.0   # golden mean, interior fixed-point center


def _gauss_nuclear_block(s, N, B, R=0.30, n_fft=None):
    if n_fft is None:
        n_fft = max(4 * N, 64)
    th = 2.0 * np.pi * np.arange(n_fft) / n_fft
    z = _GAUSS_Z0 + R * np.exp(1j * th)
    S = np.zeros((n_fft, N), dtype=complex)
    for a in range(1, B + 1):
        zn = z + a
        psi = 1.0 / zn
        w = zn ** (-2.0 * s)
        base = (psi - _GAUSS_Z0) / R
        powk = np.ones_like(base)
        for k in range(N):
            S[:, k] += w * powk
            powk = powk * base
    C = np.fft.fft(S, axis=0) / n_fft
    return C[:N, :]


def dim_gauss_nuclear(B, N, lo=0.30, hi=0.9999, iters=70):
    """Standard-Gauss-map bounded-type dimension (q=3 anchor) on the nuclear basis."""
    def lmax(s):
        return float(np.max(np.linalg.eigvals(_gauss_nuclear_block(s + 0j, N, B)).real))
    if lmax(lo) < 1.0:
        return float(lo)
    if lmax(hi) > 1.0:
        return float(hi)
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if lmax(mid) > 1.0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def dim_nuclear(q, B, N, lo=0.30, hi=0.9999, iters=70):
    """D_q(B) where the NUCLEAR even operator has leading eigenvalue 1."""
    f_lo = _lam_max_even(q, lo, N, B)
    f_hi = _lam_max_even(q, hi, N, B)
    if f_lo < 1.0:
        return float(lo)
    if f_hi > 1.0:
        return float(hi)
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if _lam_max_even(q, mid, N, B) > 1.0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


# ===========================================================================
#  Full-spectrum gap at s = D_q  (union of even + odd reduced spectra)
# ===========================================================================

def full_spectrum_mods(q, s, N, B, n_fft=None):
    """Moduli of the FULL transfer-operator spectrum = eigenvalues of the even
    block UNION the odd block, sorted descending; plus per-sector leaders."""
    Mp = build_reduced_matrix_bounded(q, s + 0j, N, +1, B, n_fft=n_fft)
    Mm = build_reduced_matrix_bounded(q, s + 0j, N, -1, B, n_fft=n_fft)
    evp = np.linalg.eigvals(Mp)
    evm = np.linalg.eigvals(Mm)
    mods = np.sort(np.concatenate([np.abs(evp), np.abs(evm)]))[::-1]
    return mods, float(np.max(np.abs(evp))), float(np.max(np.abs(evm)))


def gap_at(q, s, N, B, n_fft=None):
    mods, l1_even, l1_odd = full_spectrum_mods(q, s, N, B, n_fft=n_fft)
    l1 = float(mods[0])
    l2 = float(mods[1]) if len(mods) > 1 else 0.0
    gap = l2 / l1 if l1 > 0 else float("nan")
    alpha = -math.log(gap) if gap > 0 else float("inf")
    return {
        "lambda1": l1,
        "lambda2": l2,
        "lambda3": float(mods[2]) if len(mods) > 2 else 0.0,
        "lambda1_even": l1_even,
        "lambda1_odd": l1_odd,
        "gap": gap,
        "alpha": alpha,
    }


# ===========================================================================
#  Driver
# ===========================================================================

def load_collocation_gap():
    p = os.path.join(OUT, "d3_rosen_spectral_gap.json")
    try:
        with open(p) as f:
            return json.load(f).get("per_q_gap", {})
    except Exception:
        return {}


def try_round3_Dq(q, B, N=80):
    """Cross-check D_q against the independent collocation bisection if importable."""
    try:
        import d3_rosen_round3 as r3
        return float(r3.dim_full_rosen(q, B, N=N))
    except Exception:
        return None


def main():
    print("=" * 78)
    print("D3 NUCLEAR SPECTRAL GAP: 1-D Rosen lambda_q-CF transfer operator")
    print("  alpha_q = -log|lambda_2/lambda_1| at s = D_q(B), NUCLEAR disc-algebra basis.")
    print("  Replaces the non-convergent barycentric collocation of d3_rosen_spectral_gap.py.")
    print("  CAVEAT: 1-D CF decay-of-correlations gap ONLY (no horocycle, no certification).")
    print("=" * 78)

    Q_VALS = [5, 7, 8, 13]
    B = 12                       # same bounded-type truncation as the collocation run
    N_GRID = [20, 30, 40, 50]
    N_REF = 50                   # reference basis size for the headline per-q value

    coll = load_collocation_gap()

    # q=3 Gauss anchor convenience cross-check (dimension only)
    print("\nq=3 GAUSS ANCHOR cross-check (D_H{digits 1,2} = 0.5312805062772051,"
          " standard Gauss map, nuclear basis)")
    d3 = dim_gauss_nuclear(2, N=N_REF)
    print(f"  nuclear D_3(B=2) = {d3:.13f}   known = {KNOWN_E12:.13f}   "
          f"residual = {d3 - KNOWN_E12:+.2e}")

    per_q = {}
    conv = {}

    for q in Q_VALS:
        lam, hq, kappa = hecke_params(q)
        print("\n" + "-" * 78)
        print(f"q={q}  lambda={lam:.6f}  kappa={kappa}  B={B}")

        # D_q on the nuclear operator itself (N=N_REF) + independent collocation cross-check
        Dq = dim_nuclear(q, B, N=N_REF)
        Dq_r3 = try_round3_Dq(q, B, N=80)
        xcheck = f"  (collocation dim_full_rosen={Dq_r3:.8f}, d={Dq-Dq_r3:+.2e})" if Dq_r3 is not None else ""
        print(f"  D_q(B={B}) nuclear = {Dq:.10f}{xcheck}")

        # N-convergence study of the gap at THIS D_q
        print(f"\n  N-convergence of gap at s=D_q:")
        print(f"    {'N':>4}  {'lam1':>12}  {'lam2':>12}  {'gap':>14}  "
              f"{'alpha':>11}  {'d(gap)':>12}")
        rows = []
        prev = None
        max_dgap = 0.0
        for N in N_GRID:
            g = gap_at(q, Dq, N, B)
            dgap = abs(g["gap"] - prev) if prev is not None else float("nan")
            if not math.isnan(dgap):
                max_dgap = max(max_dgap, dgap)
            ds = f"{dgap:.3e}" if not math.isnan(dgap) else "       ---"
            print(f"    {N:4d}  {g['lambda1']:12.8f}  {g['lambda2']:12.8f}  "
                  f"{g['gap']:14.10f}  {g['alpha']:11.7f}  {ds:>12}")
            rows.append({"N": N, **{k: g[k] for k in
                         ("lambda1", "lambda2", "lambda3",
                          "lambda1_even", "lambda1_odd", "gap", "alpha")},
                         "delta_gap": None if math.isnan(dgap) else float(dgap)})
            prev = g["gap"]

        fine_dgap = abs(rows[-1]["gap"] - rows[-2]["gap"])
        stable_1e6 = fine_dgap < 1e-6
        stable_1e4 = fine_dgap < 1e-4
        print(f"    => max d(gap) over grid = {max_dgap:.3e};  "
              f"fine d(gap) N={N_GRID[-2]}->{N_GRID[-1]} = {fine_dgap:.3e}  "
              f"[{'STABLE<1e-6' if stable_1e6 else ('STABLE<1e-4' if stable_1e4 else 'DRIFT>=1e-4')}]")

        ref = rows[-1]
        l1_sanity = abs(ref["lambda1"] - 1.0) < 5e-3
        coll_g = coll.get(str(q), {}).get("gap")
        coll_s = f"{coll_g:.6f}" if coll_g is not None else "n/a"
        print(f"    lambda1 sanity (|lam1-1|<5e-3 at s=D_q): {ref['lambda1']:.8f}  "
              f"[{'OK' if l1_sanity else 'CHECK'}]")
        print(f"    nuclear gap (N={N_REF}) = {ref['gap']:.8f}  vs  "
              f"collocation(drifting) gap = {coll_s}")

        per_q[q] = {
            "lambda": float(lam), "kappa": int(kappa), "B": B,
            "D_q_nuclear": float(Dq),
            "D_q_collocation_xcheck": Dq_r3,
            "lambda1": ref["lambda1"], "lambda2": ref["lambda2"],
            "lambda3": ref["lambda3"],
            "lambda1_even": ref["lambda1_even"], "lambda1_odd": ref["lambda1_odd"],
            "gap": ref["gap"], "alpha": ref["alpha"],
            "lambda1_sanity_ok": bool(l1_sanity),
            "collocation_gap": coll_g,
        }
        conv[q] = {
            "rows": rows,
            "max_drift": float(max_dgap),
            "fine_drift": float(fine_dgap),
            "stable_1e6": bool(stable_1e6),
            "stable_1e4": bool(stable_1e4),
        }

    # verdict
    print("\n" + "=" * 78)
    print("VERDICT")
    s6 = [q for q in Q_VALS if conv[q]["stable_1e6"]]
    s4 = [q for q in Q_VALS if conv[q]["stable_1e4"]]
    max_fine = max(conv[q]["fine_drift"] for q in Q_VALS)
    print(f"  N-grid: {N_GRID}")
    print(f"  Stable to 1e-6 (fine d(gap)): {s6}")
    print(f"  Stable to 1e-4 (fine d(gap)): {s4}")
    print(f"  Worst fine d(gap) over all q: {max_fine:.3e}")
    print(f"  Collocation (d3_rosen_spectral_gap.json) fine drift was ~1e-2, NONE stable to 1e-6.")
    if len(s6) == len(Q_VALS):
        print("  => NUCLEAR METHOD N-CONVERGED to 1e-6 for ALL q where collocation drifted ~1e-2.")
    elif len(s4) == len(Q_VALS):
        print("  => NUCLEAR METHOD N-CONVERGED to 1e-4 for ALL q (collocation never reached 1e-6).")
    else:
        print("  => PARTIAL: see per-q fine drift above.")

    out = {
        "description": "NUCLEAR (holomorphic disc-algebra) spectral gap of the "
                       "1-D Rosen lambda_q-CF transfer operator, alpha_q="
                       "-log|lambda_2/lambda_1| at s=D_q(B). Replaces the "
                       "non-convergent barycentric-collocation run.",
        "caveat": "1-D CF-map decay-of-correlations gap ONLY; does NOT imply "
                  "horocycle effective equidistribution (2-D BCZ section is "
                  "parabolic/zero-entropy, no gap, 1 in essential spectrum). "
                  "No interval certification, no Lean.",
        "method": "MMS even/odd reduced transfer operator (eqs 32-34, "
                  "arXiv:0912.2236) on per-cell Taylor bases via Cauchy-FFT; "
                  "digit tails truncated at l<=B (bounded-type survivor set); "
                  "gap from the union of even+odd reduced spectra.",
        "B": B,
        "N_grid": N_GRID,
        "N_ref": N_REF,
        "q3_gauss_anchor": {"D_3_B2_nuclear": float(d3), "known": KNOWN_E12,
                            "residual": float(d3 - KNOWN_E12)},
        "per_q_gap": {str(q): per_q[q] for q in Q_VALS},
        "N_convergence": {str(q): conv[q] for q in Q_VALS},
        "verdict": {
            "stable_1e6_qs": s6,
            "stable_1e4_qs": s4,
            "worst_fine_drift": float(max_fine),
            "collocation_comparison": "collocation fine drift ~1e-2, none stable to 1e-6",
        },
    }
    out_json = os.path.join(OUT, "d3_rosen_nuclear_gap.json")
    with open(out_json, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\n  Saved: {out_json}")
    return out


if __name__ == "__main__":
    main()
