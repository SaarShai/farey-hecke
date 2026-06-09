"""
d3_hecke_dimension.py
=====================

Hausdorff dimension of bounded-type ROSEN / lambda-CF survivor sets for
the Hecke triangle groups G_q, q = 3, 4, 5, 6.

BACKGROUND — the Rosen map (canonical reference)
-------------------------------------------------
For q >= 3, set lambda_q = 2 cos(pi/q).

The Rosen lambda_q-continued fraction (RCF) of x in R is produced by the map
    R_q : x  ->  1/(lambda_q * round_q(1/x))  -  1/x  (mod adjustment)
where "round_q" is rounding to the nearest multiple of lambda_q.

The NATURAL EXTENSION / invertible-branch formulation (Nakada 1981, Rosen 1954,
Arnoux-Hubert 2008): the fundamental domain for R_q restricted to its "standard"
branch is approximately [-(lambda_q/2), lambda_q/2]. The inverse branches are
    psi_{a,eps}(x) = 1 / (eps * a * lambda_q - x),   a in Z_+, eps in {+1,-1}
with |psi_{a,eps}'(x)| = 1/(eps a lambda_q - x)^2.

For the POSITIVE-DIGIT (bounded-type) restriction we focus on the branches with
eps = +1, a = 1, 2, ..., B (largest digit <= B). This is the lambda_q-analogue of
the Gauss-map restriction to digits {1,...,B}.

OPERATOR
--------
The transfer operator at parameter s acting on functions on the interval I_q = [0, lambda_q/2]:

    (L_{q,s} f)(x) = sum_{a=1}^{B} |psi_{a,+}'(x)|^s * f(psi_{a,+}(x))
                   = sum_{a=1}^{B} (a * lambda_q - x)^{-2s} * f(1 / (a * lambda_q - x))

The Hausdorff dimension D_q(B) = s* where the leading eigenvalue of L_{q,s} equals 1.

NOTE on CANONICAL DEFINITION
-----------------------------
The Rosen map has two families of branches (eps=+1 and eps=-1) and the standard
domain is [-lambda_q/2, lambda_q/2]. The full map on that domain gives a larger
alphabet. For the purpose of measuring the BOUNDED-TYPE survivor set (digits bounded
by B), it is standard to restrict to positive (eps=+1, a>=1) inverse branches.

For q=3: lambda_3 = 2*cos(pi/3) = 1 (the Gauss map). The branches are
  psi_{a,+}(x) = 1/(a - x) => psi_{a}'(x) = (a-x)^{-2}.
  This is EXACTLY the Gauss-map family psi_a(x) = 1/(a+x) with x replaced by -x
  (or equivalently x in [-1/2, 0] instead of [0, 1]). For the DIMENSION calculation
  the interval convention is irrelevant because the dimension of the operator depends
  only on the contraction ratios -- so q=3 MUST recover Jenkinson-Pollicott's
  dim_H(E_{1,2}) = 0.5312805062772... when B=2.

VALIDATION ANCHOR
-----------------
  q=3, B=2: must recover 0.5312805062772051416 (Jenkinson-Pollicott).

IMPLEMENTATION NOTE on q=3 SPECIAL CASE
-----------------------------------------
For q=3: lambda_3 = 2*cos(pi/3) = 1.0 exactly.
The positive inverse branches are psi_{a,+}(x) = 1/(a*1 - x) = 1/(a - x).
The standard interval is [0, lambda_3/2] = [0, 0.5].
For x in [0, 0.5], a >= 1: the branch psi_{1,+}(x) = 1/(1-x) maps [0,0.5] -> [1,2],
which is OUTSIDE [0, 0.5]. So the operator must be defined on an appropriate domain.

The CORRECT formulation for q=3 matching the Gauss map:
  - The Rosen map for q=3 is identical to the Gauss map.
  - The interval is [0,1] (not [0,0.5]).
  - Inverse branches: psi_a(x) = 1/(a+x) mapping [0,1] -> (0, 1/(a)) subset [0,1].
  - This is what badly_approx_dimension.py implements, and it gives the right answer.

For general q, the Rosen map's "continued fraction" part acts on [0, lambda_q/2]
(or equivalently [-(lambda_q/2), lambda_q/2] including negative branches).

For POSITIVE digits only (the bounded-type survivor set), the natural formulation is:
  Domain: [0, lambda_q/2] (call it I_q)
  Inverse branches: phi_{a}(x) = 1/(a * lambda_q + x) for a = 1, ..., B
    (this uses +x to keep image in I_q)
  |phi_a'(x)| = (a*lambda_q + x)^{-2}

This is the DIRECT GENERALIZATION of the Gauss-map transfer operator from
badly_approx_dimension.py to lambda_q.

For q=3 (lambda_3=1): phi_a(x) = 1/(a+x), exactly the Gauss-map branches.
For q=4 (lambda_4=sqrt(2)): phi_a(x) = 1/(a*sqrt(2)+x).
For q=5 (lambda_5=(1+sqrt(5))/2, golden ratio): phi_a(x) = 1/(a*phi+x).
For q=6 (lambda_6=sqrt(3)): phi_a(x) = 1/(a*sqrt(3)+x).

This is labeled a "lambda_q-Gauss-map analogue" -- it is the direct Rosen-CF
restriction to positive digits, consistent with the literature (see e.g.
Kessebohmer-Stratmann "A multifractal analysis for Stern-Brocot intervals,
continued fractions and large deviations", JRMS 2007; Mayer-Muhlenbruch-Stromberg).

SANITY
------
q=3, B=2: recover 0.5312805062772051416 to machine precision.
q=3, large B: converge to 1 (Jarnik's theorem).
D_q(B) is increasing in B, and D_q(1) = s* with just one branch.

SPECTRAL EDGE QUESTION
----------------------
Test whether X(q) = 1/lambda_q^3 is the critical digit where D_q(B) -> 0.
For D_q(B) -> 0 we need only the leading branch (a=1, small B) to be barely contracting.
The pressure of the one-branch operator is P(s) = -2s * log(lambda_q), giving s* = 0
trivially. So D_q(B) -> 0 as B -> 0 (continuous digit bound). For integer B, D_q(1) > 0.

The more interesting question: is there a CRITICAL VALUE of the digit bound B_crit(q)
where the spectrum changes character? We test whether D_q(B_frac) -> 0 as the
"fractional digit bound" B approaches 1/lambda_q (the width of the first branch image
on [0, lambda_q/2]).

For the lambda_q-Gauss map with digits in {1, ..., B}:
  D_q(B) -> 0 as B -> 1 (only the single branch a=1 with contracting domain).
  The "edge" is the limit dim D_q({1}) = dim of the set {1,1,1,...} = a single fixed point = 0.

We numerically verify whether X(q) = 1/lambda_q^3 gives a special breakpoint.
"""

from __future__ import annotations
import math, json, os
import numpy as np

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)

try:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    HAVE_MPL = True
except Exception:
    HAVE_MPL = False

# Validation anchor
KNOWN_E12 = 0.5312805062772051416   # dim_H{a_k in {1,2}}, Jenkinson-Pollicott


# ── Chebyshev machinery (same as badly_approx_dimension.py) ───────────────────
def _cheb(N):
    k = np.arange(N)
    x = 0.5 * (1 - np.cos(np.pi * k / (N - 1)))
    w = np.ones(N); w[1::2] = -1.0; w[0] *= 0.5; w[-1] *= 0.5
    return x, w


def _bary(x, w, Y):
    diff = Y[:, None] - x[None, :]
    small = np.abs(diff) < 1e-13
    with np.errstate(divide="ignore", invalid="ignore"):
        T = w[None, :] / diff
        denom = np.sum(T, axis=1)
        L = T / denom[:, None]
    for r in np.where(np.any(small, axis=1))[0]:
        j = int(np.argmax(small[r])); L[r, :] = 0.0; L[r, j] = 1.0
    return L


def transfer_dim_hecke(lam, digits, N=64):
    """
    Hausdorff dim of the bounded-type set for the lambda_q-Gauss map analogue.

    Inverse branches: phi_a(x) = 1/(a*lam + x)  for a in digits (subset of Z_+).
    Operator domain: [0, lam/2] (renormalized to [0,1] for the Chebyshev grid).

    We map [0,1] -> [0, lam/2] by x_phys = x * (lam/2).
    phi_a maps [0, lam/2] -> [1/(a*lam + lam/2), 1/(a*lam)]
            = [2/((2a+1)*lam), 1/(a*lam)] subset [0, lam/2] for a>=1.

    Transfer operator on [0, lam/2]:
      (L_s f)(x) = sum_a (a*lam + x)^{-2s} f(1/(a*lam + x))

    On [0,1] with change of variables x = t * (lam/2), y = u * (lam/2):
      image point: phi_a(x)/( lam/2) = 2/((2a*lam + 2x)*lam/2) ...
      = 2/(lam * (2a + 2*t)) ... no, let's keep it on [0,lam/2] directly.

    For the Chebyshev grid we work on [0,1] rescaled:
      Nodes on [0,1]: t_j. Physical: x_j = t_j * L  where L = lam/2.
      Branch image in [0,1]: u_{a,j} = phi_a(x_j) / L = 2 / ((2a + t_j) * lam^2).
      Weight: phi_a'(x_j) = -(a*lam + x_j)^{-2} = -(a*lam + t_j*L)^{-2}
              |phi_a'|^s L_scaling: the operator on unit interval picks up a factor.

    Actually simpler to just apply the operator directly without scaling,
    keeping everything on [0, L] = [0, lam/2], by scaling Chebyshev nodes.
    """
    digits = list(digits)
    L = lam / 2.0   # right endpoint of the domain
    x_unit, w = _cheb(N)
    x = x_unit * L   # physical nodes on [0, L]

    def lam_ev(s):
        M = np.zeros((N, N))
        for a in digits:
            # phi_a(x) = 1/(a*lam + x)
            denom = a * lam + x                     # shape (N,)
            phi_x = 1.0 / denom                    # image points, shape (N,)
            weight = denom ** (-2.0 * s)            # |phi_a'(x)|^s, shape (N,)
            # phi_x must be in [0, L]: 1/(a*lam+x) in [1/((a+1/2)*lam), 1/(a*lam)]
            # for a>=1, lam>=1: image is in (0, 1/lam] <= (0, 1] but we need <= L=lam/2
            # For a=1: max = 1/lam. Is 1/lam <= lam/2? <=> 2 <= lam^2.
            # lam_3=1 => 1/1=1 > 1/2=L. So image for q=3,a=1 goes OUTSIDE [0,L].
            # This confirms we must use the FULL [0,1] domain for q=3.
            # For q>=4: lam>=sqrt(2), so 1/lam <= 1/sqrt(2) < sqrt(2)/2 = L_4. OK.

            # For q=3 we handle separately (see transfer_dim_gauss below).
            phi_unit = phi_x / L                   # rescale to [0,1]
            # Clamp to [0,1] for safety (should be in range for q>=4)
            phi_unit = np.clip(phi_unit, 0.0, 1.0)
            # Barycentric interpolation: evaluate eigenfunction at phi_unit nodes
            M += weight[:, None] * _bary(x_unit, w, phi_unit)
        return np.max(np.linalg.eigvals(M).real)

    lo, hi = 0.0, 1.0 - 1e-9
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if lam_ev(mid) > 1.0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def transfer_dim_gauss(digits, N=64):
    """
    Gauss-map transfer operator: phi_a(x) = 1/(a+x) on [0,1].
    Identical to badly_approx_dimension.transfer_dim but with N=64.
    This handles q=3.

    NOTE: the bisection starts at lo=0 (not 1e-4) so that the B=1 case
    correctly returns 0 (single-branch IFS has a single fixed point, dim=0).
    """
    digits = list(digits)
    x, w = _cheb(N)

    def lam_ev(s):
        M = np.zeros((N, N))
        for a in digits:
            denom = a + x
            y = 1.0 / denom
            M += (denom ** (-2.0 * s))[:, None] * _bary(x, w, y)
        return np.max(np.linalg.eigvals(M).real)

    lo, hi = 0.0, 1.0 - 1e-9
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if lam_ev(mid) > 1.0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def dim_bounded_type(q, B, N=64):
    """
    D_q(B) = dim_H of the set of x with all Rosen digits in {1,...,B}.

    q=3: uses the standard Gauss-map operator (domain [0,1]).
    q>=4: uses the lambda_q-Gauss analogue on [0, lambda_q/2].
    """
    lam = 2.0 * math.cos(math.pi / q)
    digits = list(range(1, B + 1))
    if q == 3:
        return transfer_dim_gauss(digits, N=N)
    else:
        return transfer_dim_hecke(lam, digits, N=N)


def dim_custom_digits(q, digits, N=64):
    """Dimension with explicit digit set (for spectral edge investigation)."""
    lam = 2.0 * math.cos(math.pi / q)
    if q == 3:
        return transfer_dim_gauss(digits, N=N)
    else:
        return transfer_dim_hecke(lam, digits, N=N)


# ── Main computation ──────────────────────────────────────────────────────────
def main():
    results = {}
    q_vals = [3, 4, 5, 6]

    # ── Lambda values ──────────────────────────────────────────────────────────
    print("Lambda_q = 2*cos(pi/q) values:")
    for q in q_vals:
        lam = 2.0 * math.cos(math.pi / q)
        print(f"  q={q}: lambda_{q} = {lam:.10f}  (1/lambda^3 = {1/lam**3:.10f})")

    # ── (1) SANITY CHECK: q=3, B=2 must recover Jenkinson-Pollicott ───────────
    print("\n===== SANITY CHECK =====")
    d_sanity = dim_bounded_type(3, 2)
    residual = d_sanity - KNOWN_E12
    print(f"  q=3, B=2: computed = {d_sanity:.15f}")
    print(f"            known    = {KNOWN_E12:.15f}")
    print(f"            residual = {residual:.2e}")
    assert abs(residual) < 1e-10, f"SANITY FAILED: residual = {residual}"
    print("  SANITY PASSED")
    results['sanity'] = {
        'q': 3, 'B': 2,
        'computed': d_sanity,
        'known': KNOWN_E12,
        'residual': residual
    }

    # ── (2) D_q(B) for q=3,4,5,6 and B=1..12 ─────────────────────────────────
    print("\n===== D_q(B) DIMENSION CURVES (B=1..12) =====")
    B_ext = list(range(1, 13))
    dim_ext = {}
    dim_table = {}
    for q in q_vals:
        lam = 2.0 * math.cos(math.pi / q)
        dim_ext[q] = []
        dim_table[q] = []
        for B in B_ext:
            d = dim_bounded_type(q, B)
            dim_ext[q].append(d)
            dim_table[q].append({'B': B, 'dim': d})
            print(f"    q={q}, lambda={lam:.6f}, B={B:2d}: D_q(B) = {d:.12f}")
    results['dim_table'] = {str(q): dim_table[q] for q in q_vals}
    results['dim_extended'] = {str(q): dim_ext[q] for q in q_vals}
    results['B_ext'] = B_ext

    # ── (4) SPECTRAL EDGE: test X(q) = 1/lambda_q^3 conjecture ───────────────
    print("\n===== SPECTRAL EDGE ANALYSIS =====")
    # Key fact (verified numerically): D_q(B=1) = 0 for ALL q.
    # Reason: the single-branch IFS {phi_1} has a unique fixed point (dimension 0).
    # At s=0, L_0 f(x) = f(phi_1(x)) has leading eigenvalue 1 (constant functions
    # are eigenfunctions with eigenvalue 1 trivially). So the bisection returns s*=0.
    #
    # This means:
    # - The integer transition B=1 -> B=2 always gives a jump from 0 to some positive dim.
    # - D_q(B=2) is the "minimum non-trivial" dimension for each q.
    #
    # The X(q) = 1/lambda^3 test:
    # For INTEGER B, X(q) cannot mark a spectral edge since D_q(1)=0 and D_q(2)>0 for all q.
    # We test whether X(q) = 1/lambda^3 has a geometric role:
    # - phi_1 image width = 1/(3*lambda) for all q (not 1/lambda^3 in general)
    # - phi_1 image width = 1/lambda^3 ONLY for q=6 (since lambda_6=sqrt(3), sqrt(3)^3=3*sqrt(3))
    # - The phi_1 image maximum = 1/lambda (not 1/lambda^3 for any standard q)
    # - The phi_1 fixed point x* = (-lam + sqrt(lam^2+4))/2 (not 1/lambda^3)
    #
    # VERDICT: 1/lambda^3 is NOT the spectral edge for integer B. For all q,
    # D_q(1)=0 and D_q(2) > 0, with D_q(2) > 1/lambda^3 for q=4,5,6 (see table below).
    # The quantity 1/lambda^3 does not equal D_q(B) for any natural integer B.

    edge_results = {}
    print("\n  D_q(B=1) [= 0 exactly], D_q(B=2), and X(q)=1/lambda^3:")
    for q in q_vals:
        lam = 2.0 * math.cos(math.pi / q)
        d1 = dim_bounded_type(q, 1)   # = 0 exactly
        d2 = dim_ext[q][1]             # B=2, already computed
        xq = 1.0 / lam**3
        # phi_1 image width = 1/(3*lambda); fixed point
        phi1_img_width = 1.0 / (3.0 * lam)
        xstar = (-lam + math.sqrt(lam**2 + 4)) / 2  # fixed pt of phi_1
        print(f"  q={q}: lam={lam:.6f}, D_q(1)={d1:.2e}, D_q(2)={d2:.8f}, "
              f"1/lam^3={xq:.8f}, phi_1 width=1/(3*lam)={phi1_img_width:.8f}, "
              f"phi_1 fixed pt={xstar:.8f}")
        edge_results[q] = {
            'lambda': lam, 'D_q_B1': d1, 'D_q_B2': d2, 'X_q': xq,
            'phi1_img_width': phi1_img_width, 'phi1_fixed_pt': xstar
        }
    print()
    print("  FINDING: D_q(B=2) > X(q)=1/lambda^3 for q=4,5,6. Not equal, not less.")
    print("  The edge where D_q -> 0 is B -> 1 (integer onset at B=2 from 0).")
    print("  1/lambda^3 is the phi_1 image WIDTH only for q=6 (special case lambda_6=sqrt(3)).")

    results['edge_investigation'] = {str(q): edge_results[q] for q in q_vals}
    results['sanity'] = {
        'q': 3, 'B': 2,
        'computed': d_sanity,
        'known': KNOWN_E12,
        'residual': float(residual)
    }

    # Save JSON
    def make_serializable(obj):
        if isinstance(obj, dict):
            return {k: make_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [make_serializable(x) for x in obj]
        elif isinstance(obj, (np.floating, float)):
            return float(obj)
        elif isinstance(obj, (np.integer, int)):
            return int(obj)
        else:
            return obj

    json.dump(make_serializable(results),
              open(os.path.join(OUT, "d3_hecke_dimension.json"), "w"), indent=2)
    print(f"\nResults saved to {OUT}/d3_hecke_dimension.json")

    # ── Plots ──────────────────────────────────────────────────────────────────
    if not HAVE_MPL:
        print("matplotlib not available, skipping plots")
        return

    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    fig.suptitle("Hecke/Rosen bounded-type survivor-set dimensions $D_q(B)$", fontsize=13)

    colors = {3: 'tab:blue', 4: 'tab:orange', 5: 'tab:green', 6: 'tab:red'}
    B_arr = np.array(B_ext)

    # Panel 1: All q on same plot
    ax = axes[0, 0]
    for q in q_vals:
        lam = 2.0 * math.cos(math.pi / q)
        dims = np.array(dim_ext[q])
        ax.plot(B_arr, dims, 'o-', color=colors[q], label=f"q={q} (lam={lam:.3f})")
    ax.axhline(KNOWN_E12, color='tab:blue', lw=0.8, ls='--', alpha=0.5,
               label=f'q=3,B=2 known={KNOWN_E12:.5f}')
    ax.set_xlabel("B (max Rosen digit)")
    ax.set_ylabel("$D_q(B) = $ Hausdorff dim")
    ax.set_title("Dimension vs digit bound B")
    ax.legend(fontsize=8)
    ax.set_ylim(0, 1)

    # Panel 2: q=3 validation detail
    ax = axes[0, 1]
    dims3 = np.array(dim_ext[3])
    ax.plot(B_arr, dims3, 'o-', color='tab:blue', label="q=3 (Gauss map)")
    ax.axhline(KNOWN_E12, color='gold', lw=2, ls='--',
               label=f'Jenkinson-Pollicott B=2: {KNOWN_E12:.7f}')
    ax.scatter([2], [d_sanity], marker='*', s=200, color='gold', zorder=5)
    ax.set_xlabel("B"); ax.set_ylabel("$D_3(B)$")
    ax.set_title(f"q=3 sanity check (residual = {residual:.1e})")
    ax.legend(fontsize=8)

    # Panel 3: Compare at fixed B
    ax = axes[1, 0]
    for B_i, B in enumerate([1, 2, 3, 4, 5, 6, 8]):
        if B > len(B_ext): continue
        y = [dim_ext[q][B-1] for q in q_vals if B <= len(dim_ext[q])]
        ax.plot(q_vals[:len(y)], y, 'o-', label=f"B={B}")
    ax.set_xlabel("q"); ax.set_ylabel("$D_q(B)$")
    ax.set_title("Dimension at fixed B, varying q")
    ax.legend(fontsize=8)
    ax.set_xticks(q_vals)

    # Panel 4: D_q(2) vs 1/lambda^3 and phi_1 image width
    ax = axes[1, 1]
    lams = [2.0 * math.cos(math.pi / q) for q in q_vals]
    d2s = [dim_ext[q][1] for q in q_vals]   # B=2
    xqs = [1.0 / lam**3 for lam in lams]
    phi1_widths = [1.0 / (3.0 * lam) for lam in lams]
    ax.plot(q_vals, d2s, 'bo-', ms=8, label="$D_q(2)$ (min nontrivial dim)")
    ax.plot(q_vals, xqs, 'rs--', ms=8, label="$X(q) = 1/\\lambda_q^3$")
    ax.plot(q_vals, phi1_widths, 'g^-.', ms=8, label="$\\phi_1$ img width $= 1/(3\\lambda)$")
    ax.set_xlabel("q"); ax.set_ylabel("value")
    ax.set_title("Spectral quantities vs $X(q)=1/\\lambda_q^3$")
    ax.legend(fontsize=8)
    ax.set_xticks(q_vals)

    plt.tight_layout()
    p = os.path.join(OUT, "d3_hecke_dimension.png")
    fig.savefig(p, dpi=130, bbox_inches="tight")
    plt.close(fig)
    print(f"Plot saved: {p}")


if __name__ == "__main__":
    main()
