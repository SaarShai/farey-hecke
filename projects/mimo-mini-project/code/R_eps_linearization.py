"""Analytical / symbolic linearization of R_eps near the critical pair (1/3, 2/3).

The BCZ map near (1/3, 2/3):
  Let u = x - 1/3, v = y - 2/3 with u + v >= 0 (triangle constraint).

  At (1/3, 2/3), the floor k = floor((1 + 1/3) / (2/3)) = floor(2) = 2.
  But this is exactly the boundary: (1 + x)/y at (1/3, 2/3) equals 2.
  For points slightly inside the triangle (x + y > 1), we need to figure out
  which side of the floor-discontinuity we are on.

  k = floor((1 + x) / y).  k = 2 iff (1 + x)/y in [2, 3), i.e. y in ((1+x)/3, (1+x)/2].
  At x = 1/3 + u, y = 2/3 + v:
    (1+x)/y = (4/3 + u) / (2/3 + v) = 2 + (u - 2v)/(2/3 + v) ≈ 2 + (3/2)(u - 2v)
  So k = 2 iff (u - 2v) > 0 (to leading order, near boundary).
  k = 1 iff (1+x)/y < 2, i.e. (u - 2v) < 0.

  CASE k=1: T(x,y) = (y, y - x) = (2/3 + v, 1/3 + (v - u))
            Set (x', y') = (2/3 + v, 1/3 + (v - u)).
            Note x' + y' = 1 + 2v - u.  Triangle requires this > 1, so 2v > u.
            But k=1 requires u < 2v (same condition!).
  CASE k=2: T(x,y) = (y, 2y - x) = (2/3 + v, 1 + 2v - (1/3 + u)) = (2/3 + v, 2/3 + 2v - u)
            Set (x', y') = (2/3 + v, 2/3 + 2v - u).  x' + y' = 4/3 + 3v - u > 1
            iff u < 3v + 1/3, automatic for small (u,v).

  ─── So (1/3, 2/3) is the floor-discontinuity, with:
      k=1 above the line v = u/2  (image: (2/3+v, 1/3 + (v-u)) — lands near (2/3, 1/3))
      k=2 below the line v = u/2  (image: (2/3+v, 2/3 + 2v - u) — lands near (2/3, 2/3))

  But (2/3, 2/3) is OUTSIDE the triangle (2/3 + 2/3 = 4/3, OK; both in (0,1) — wait,
  IS it in T?  Yes: x'+y' = 4/3 > 1, x'<1, y'<1 — so (2/3, 2/3) IS in T.  However,
  at (2/3, 2/3), x*y = 4/9 > 2/9, so the second pair is NOT extreme.
  So the k=2 branch of T_BCZ AT (1/3, 2/3) maps to (2/3, 2/3) which is NOT extreme.
  Therefore, to be in R_eps, we MUST be in the k=1 branch (above the line v = u/2).
"""
import math
import numpy as np
import time
from numba import njit

T_STAR = 2.0 / 9.0


@njit(cache=True)
def bcz_step(x, y):
    k = math.floor((1.0 + x) / y)
    return y, k * y - x


@njit(cache=True)
def get_floor(x, y):
    return math.floor((1.0 + x) / y)


def study_critical_point():
    """Examine the BCZ map at and near (1/3, 2/3)."""
    print("=" * 70)
    print("BCZ map at and near (1/3, 2/3)")
    print("=" * 70)
    # exact (1/3, 2/3): k = floor(2) = 2.  T = (2/3, 2*2/3 - 1/3) = (2/3, 1).
    # But y=1 is the boundary.
    # So at exactly (1/3, 2/3), the map is degenerate.
    x, y = 1.0 / 3.0, 2.0 / 3.0
    k = get_floor(x, y)
    print(f"  At (1/3, 2/3): k = {k}, T = ({y}, {k*y - x})")

    # Slightly inside (u + v > 0, both small):
    for (u, v) in [(0.01, 0.01), (0.01, -0.001), (-0.001, 0.01), (0.001, 0.0), (0.0, 0.001),
                   (0.001, 0.001), (-0.001, 0.002)]:
        x, y = 1.0 / 3.0 + u, 2.0 / 3.0 + v
        if x + y <= 1.0:
            continue
        k = get_floor(x, y)
        x1, y1 = bcz_step(x, y)
        x2, y2 = bcz_step(x1, y1)
        print(f"  (1/3+{u:+.3e}, 2/3+{v:+.3e}): k0={k}, x1={x1:.4f}, y1={y1:.4f}, "
              f"x*y={x*y:.4f}, x1*y1={x1*y1:.4f}, x2*y2={x2*y2:.4f}")

    print()
    print("  Conclusion: must use k=1 branch (u - 2v < 0, equiv. v > u/2)")
    print("  Image under k=1: (x', y') = (y, y - x) = (2/3 + v, 1/3 + (v - u))")
    print("  At this point: x'*y' = (2/3 + v)(1/3 + v - u)")
    print("  Linearize: (2/3)(1/3) + (2/3)(v - u) + (1/3)v + O((u,v)^2)")
    print("           = 2/9 + (2/3)(v - u) + (1/3)v")
    print("           = 2/9 + v - (2/3)u")
    print()


def derive_linear_geometry():
    """Derive R_eps in linearized coordinates and compute its area."""
    print("=" * 70)
    print("LINEARIZED R_eps near (1/3, 2/3) — analytical")
    print("=" * 70)
    # Pair 0: (X_0, X_1) = (1/3 + u, 2/3 + v), product = 2/9 + (2/3)v + (1/3)u + uv.
    # P0 = X_0 * X_1 = (1/3 + u)(2/3 + v) = 2/9 + v/3 + 2u/3 + uv.
    # P0 < 2/9 + eps  <=>  (v + 2u)/3 + uv < eps.
    # Linearize:  P0 - 2/9 ≈ (2u + v)/3.
    # So pair 0 extreme:  2u + v < 3 eps  (and >0 part is automatic in linearization).
    # Actually we need P0 < t = 2/9 + eps, AND (x,y) ∈ T which requires u + v > 0.

    print("  Pair 0 = (1/3 + u, 2/3 + v):  P0 = 2/9 + (2u + v)/3 + uv")
    print("  P0 < 2/9 + eps  <=>  2u + v < 3 eps  (linearized)")
    print()

    # Now apply k=1 branch (v > u/2 needed for valid map AND for image to land in
    # the extreme region near (2/3, 1/3)):
    # (X_1, X_2) = (2/3 + v, 1/3 + (v - u)) — image of T_BCZ in k=1 branch.
    # P1 = X_1 * X_2 = (2/3 + v)(1/3 + v - u)
    #    = 2/9 + (2/3)(v - u) + (1/3)v + v(v - u)
    #    = 2/9 + v - (2/3)u + v(v - u)
    print("  Pair 1 (k=1 branch) = (2/3 + v, 1/3 + (v - u)):")
    print("    P1 = 2/9 + v - (2u/3) + v(v - u)")
    print("    P1 < 2/9 + eps  <=>  v - (2u/3) < eps  (linearized)")
    print("                     <=>  3v - 2u < 3 eps")
    print()

    # Now the second iterate.  Starting from (X_1, X_2) = (2/3 + v, 1/3 + v - u).
    # Let u' = X_1 - 2/3 = v, v' = X_2 - 1/3 = v - u.  We are now near (2/3, 1/3).
    # At (2/3, 1/3): (1 + x)/y = (5/3)/(1/3) = 5.  So k=5.
    # Locally, k = floor((1 + 2/3 + u')/(1/3 + v')) = floor(5 + (3 u' - 15 v')/(1 + 3v'))
    # near 5, so k=5 for u' - 5v' < 0 (i.e., v' > u'/5).  Otherwise k=4 (below) or 6 (above)?
    # Actually the linearization needs care.  Let me compute exactly.
    # (1 + 2/3 + u') / (1/3 + v')  at (u', v') = (0, 0) is 5.
    # Derivative: d/du' (1 + 2/3 + u')/(1/3 + v') = 1/(1/3 + v')|_(0,0) = 3.
    # Derivative: d/dv' = -(1 + 2/3 + u')/(1/3 + v')^2 |_(0,0) = -(5/3)/(1/9) = -15.
    # So (1+x)/y ≈ 5 + 3 u' - 15 v'.
    # k = 5 for (1+x)/y in [5,6) <=>  3u' - 15v' in [0, 1) — almost always 5 if (u', v') small
    # k = 4 if 3u' - 15v' < 0 <=>  u' < 5v' <=>  v < (v - u)/5 <=> v - 5(v-u) > 0 <=> 5u > 4v
    # ─── So for (u, v) with 5u < 4v: k_at_pair_1 = 5.
    #     For 5u > 4v: k_at_pair_1 = 4.
    # NOTE: we need to verify with the earlier constraint v > u/2.
    # If v > u/2 AND 5u > 4v, then v > u/2 and v < 5u/4.  Possible (e.g., u/2 < v < 5u/4 for u > 0).

    print("  Pair 1 -> Pair 2 via BCZ (now near (2/3, 1/3), generic k=5):")
    print("    Let u' = X_1 - 2/3 = v, v' = X_2 - 1/3 = v - u")
    print("    (1+x)/y near 5: linearization 5 + 3 u' - 15 v' = 5 + 3v - 15(v - u) = 5 + 15u - 12v")
    print("    k = 5 if 15u - 12v < 1, i.e. (15u - 12v) ~ O(eps) — almost always 5.")
    print()
    print("    Under k=5:  T(X_1, X_2) = (X_2, 5*X_2 - X_1)")
    print("              = (1/3 + v - u, 5/3 + 5(v - u) - 2/3 - v) = (1/3 + v - u, 1 + 4v - 5u)")
    print("    But X_3 = 1 + 4v - 5u, which is ≈ 1.  For X_3 < 1 (triangle), need 5u > 4v.")
    print("    Hmm — that's the k=4 condition!  Let me re-check.")
    print()
    # Actually, let's compute directly.
    # Pair (X_1, X_2) = (2/3 + v, 1/3 + v - u).
    # k = floor((1 + 2/3 + v)/(1/3 + v - u))
    # Numerically check:
    for (u, v) in [(0.001, 0.001), (0.001, 0.002), (0.001, 0.0006), (0.0001, 0.0001)]:
        x1, y1 = 2.0/3.0 + v, 1.0/3.0 + v - u
        if x1 + y1 > 1.0 and 0 < x1 < 1 and 0 < y1 < 1:
            k1 = get_floor(x1, y1)
            x2, y2 = bcz_step(x1, y1)
            p2 = x2 * y2
            print(f"    (u,v)=({u},{v}): X1*X2={x1*y1:.6f}, k1={k1}, X2={x2:.5f}, X3={y2:.5f}, X2*X3={p2:.6f}")

    print()
    print("  So at (X_1, X_2) near (2/3, 1/3), the floor k_1 = 5 almost always.")
    print("  Under k=5: X_3 = 5 X_2 - X_1 = 5(1/3 + v - u) - (2/3 + v) = 1 - 5u + 4v")
    print("  X_3 ≈ 1, so the image is near the boundary y=1.")
    print()
    print("  Pair 2 product:  P2 = X_2 * X_3 = (1/3 + v - u)(1 - 5u + 4v)")
    print("                       = 1/3 - 5u/3 + 4v/3 + (v - u)(1 - 5u + 4v)")
    print("                       = 1/3 - 5u/3 + 4v/3 + (v - u) + O((u,v)^2)")
    print("                       = 1/3 + (v - u) - 5u/3 + 4v/3")
    print("                       = 1/3 + v - u - 5u/3 + 4v/3")
    print("                       = 1/3 + (3v + 4v)/3 - (3u + 5u)/3")
    print("                       = 1/3 + (7v - 8u)/3")
    print()
    print("  But 1/3 vs 2/9:  1/3 - 2/9 = 1/9 > 0.  So P2 ≈ 1/3 = 3/9, which is ALWAYS > 2/9 !!!")
    print()
    print("  >>>  HMMM — this contradicts the existence of size-3 clusters near (1/3, 2/3) <<<")
    print()

    # Hold on.  Let me re-think.  The (1/3, 2/3) corner gives P2 ≈ 1/3 > 2/9.
    # So a triple-extreme run cannot start at (1/3, 2/3) — the third pair lands at
    # X_2 ≈ 1/3, X_3 ≈ 1, so X_2 * X_3 ≈ 1/3.
    # The size-3 cluster must START somewhere ELSE — perhaps near (2/3, 1/3)?
    # By symmetry: (X_0, X_1) near (2/3, 1/3) means u_a = X_0 - 2/3, v_a = X_1 - 1/3.
    # P_0 = X_0 * X_1 = (2/3 + u_a)(1/3 + v_a) = 2/9 + 2v_a/3 + u_a/3 + u_a v_a.
    # P_0 < 2/9 + eps  <=>  u_a + 2 v_a < 3 eps.
    # Near (2/3, 1/3), (1+x)/y = (5/3 + u_a)/(1/3 + v_a) ≈ 5 + 3 u_a - 15 v_a, so k0 = 5
    # (or 4 if u_a < 5 v_a, which can't happen if u_a, v_a are small AND u_a + 2v_a < 3 eps
    # — wait, u_a can be near zero and v_a too).  Need to check what k_0 is in the regime
    # u_a + 2 v_a < 3 eps near (2/3, 1/3).
    print("  ---  By symmetry, try starting near (2/3, 1/3): ---")
    print("  Pair 0 = (2/3 + u_a, 1/3 + v_a),  P0 < 2/9 + eps  iff  u_a + 2 v_a < 3 eps.")
    print()
    # k_0 = floor((1 + 2/3 + u_a) / (1/3 + v_a)) = floor((5/3 + u_a)/(1/3 + v_a))
    # = floor(5 + 3 u_a - 15 v_a + ...)
    # k = 5 for u_a > 5 v_a; k = 4 for u_a < 5 v_a (and >...)
    # Check: at u_a = v_a = 0 + tiny: 5/3 / 1/3 = 5 exactly.  k = floor(5) = 5.
    # But the floor at exactly 5 is 5, not 4. So generically k = 5 for points with
    # u_a > 5 v_a + something small, k = 4 for u_a < 5 v_a + something small.  Actually:
    # k = floor(5 + (3 u_a - 15 v_a)/(1 + 3 v_a)).  For very small (u_a, v_a):
    #   k = 5 if 3 u_a - 15 v_a >= 0, i.e. u_a >= 5 v_a.
    #   k = 4 if 3 u_a - 15 v_a < 0, i.e. u_a < 5 v_a.
    print("  k_0 = 5 if u_a >= 5 v_a;  k_0 = 4 if u_a < 5 v_a")
    print()
    # Under k_0 = 5:
    # X_1' (= image of X_2) = 5 (1/3 + v_a) - (2/3 + u_a) = 1 + 5 v_a - u_a.
    # So image = (1/3 + v_a, 1 + 5 v_a - u_a).
    # Need image in T: y = 1 + 5 v_a - u_a < 1 iff 5 v_a < u_a, consistent with k=5 branch.
    # P1 = X_1 * X_2 = (1/3 + v_a)(1 + 5 v_a - u_a)
    #    = 1/3 - u_a/3 + v_a + 5 v_a^2 - v_a u_a + 5 v_a/3
    #    = 1/3 - u_a/3 + 8 v_a / 3 + O((u_a, v_a)^2)
    # So P1 ≈ 1/3 -- NOT < 2/9 (since 1/3 > 2/9).
    # So under k=5, P1 ≈ 1/3, not extreme.
    # Under k_0 = 4:
    # X_1' (= image of X_2) = 4 (1/3 + v_a) - (2/3 + u_a) = 2/3 + 4 v_a - u_a.
    # So image = (1/3 + v_a, 2/3 + 4 v_a - u_a).
    # This lands near (1/3, 2/3) — the OTHER critical pair.
    # P1 = X_1 * X_2 = (1/3 + v_a)(2/3 + 4 v_a - u_a)
    #    = 2/9 + 4 v_a / 3 - u_a / 3 + 2 v_a / 3 + ...
    #    = 2/9 + (4 v_a + 2 v_a)/3 - u_a/3
    #    = 2/9 + 2 v_a - u_a / 3
    # So P1 < 2/9 + eps  iff  2 v_a - u_a / 3 < eps  iff  6 v_a - u_a < 3 eps.

    print("  Under k_0 = 4 (i.e., u_a < 5 v_a):")
    print("    image = (X_1, X_2) = (1/3 + v_a, 2/3 + 4 v_a - u_a)  ← near (1/3, 2/3)")
    print("    P1 = 2/9 + 2 v_a - u_a / 3 + O(...)")
    print("    P1 < 2/9 + eps  iff  6 v_a - u_a < 3 eps  (linearized)")
    print()
    # Now from (1/3 + v_a, 2/3 + 4 v_a - u_a), apply BCZ again.
    # Set u_b = v_a, v_b = 4 v_a - u_a.  At (1/3 + u_b, 2/3 + v_b), the floor
    # k = floor((1 + 1/3 + u_b)/(2/3 + v_b)) = floor((4/3 + u_b)/(2/3 + v_b))
    # = 2 + (u_b - 2 v_b)/(2/3 + v_b) ≈ 2 + (3/2)(u_b - 2 v_b)
    # Wait, let me redo: f(u_b, v_b) = (4/3 + u_b)/(2/3 + v_b).  f(0,0) = 2.
    # df/du_b = 1/(2/3) = 3/2.  df/dv_b = -(4/3)/(2/3)^2 = -3.
    # So f ≈ 2 + (3/2) u_b - 3 v_b.
    # k = 1 if u_b < 2 v_b (since then f < 2).
    # k = 2 if u_b > 2 v_b.
    print("  From (1/3 + u_b, 2/3 + v_b) where u_b = v_a, v_b = 4 v_a - u_a:")
    print("    k_1 = 1 if u_b < 2 v_b  <=>  v_a < 2(4 v_a - u_a) <=> 2 u_a < 7 v_a")
    print("    k_1 = 2 if u_b > 2 v_b  <=>  v_a > 2(4 v_a - u_a) <=> 2 u_a > 7 v_a")
    print()
    # Under k_1 = 1: image = (X_2, X_3) = (2/3 + v_b, 1/3 + (v_b - u_b))
    #              = (2/3 + 4 v_a - u_a, 1/3 + 4 v_a - u_a - v_a)
    #              = (2/3 + 4 v_a - u_a, 1/3 + 3 v_a - u_a)
    # P2 = X_2 * X_3 = (2/3 + 4 v_a - u_a)(1/3 + 3 v_a - u_a)
    #    = 2/9 + 2(3 v_a - u_a)/3 + (4 v_a - u_a)/3 + O(...)
    #    = 2/9 + (6 v_a - 2 u_a)/3 + (4 v_a - u_a)/3
    #    = 2/9 + (10 v_a - 3 u_a)/3
    # P2 < 2/9 + eps  iff  10 v_a - 3 u_a < 3 eps.
    print("  Under k_1 = 1 (i.e., 2 u_a < 7 v_a):")
    print("    (X_2, X_3) = (2/3 + 4 v_a - u_a, 1/3 + 3 v_a - u_a)")
    print("    P2 = 2/9 + (10 v_a - 3 u_a)/3 + O(...)")
    print("    P2 < 2/9 + eps  iff  10 v_a - 3 u_a < 3 eps  (linearized)")
    print()
    # Under k_1 = 2: image = (X_2, X_3) = (2/3 + v_b, 4/3 + 2 v_b - 1/3 - u_b)
    #              = (2/3 + 4 v_a - u_a, 1 + 2(4 v_a - u_a) - v_a)
    #              = (2/3 + 4 v_a - u_a, 1 + 7 v_a - 2 u_a)
    # P2 = X_2 * X_3 ≈ (2/3)(1) + ... ≈ 2/3.  Not extreme (>2/9).
    print("  Under k_1 = 2: P2 ≈ 2/3 — not extreme.")
    print()
    print("  ─── CONCLUSION ─── ")
    print("  The size-3 entry region near (2/3, 1/3) is defined by the linear inequalities:")
    print()
    print("    u_a + v_a > 0       (triangle)")
    print("    u_a + 2 v_a < 3 eps  (pair 0 extreme)")
    print("    u_a < 5 v_a          (k_0 = 4 branch)")
    print("    6 v_a - u_a < 3 eps  (pair 1 extreme)")
    print("    2 u_a < 7 v_a        (k_1 = 1 branch)")
    print("    10 v_a - 3 u_a < 3 eps  (pair 2 extreme)")
    print()
    print("  Equivalently, in (u, v) where u = u_a, v = v_a, the polytope is:")
    print("    u + v > 0")
    print("    u + 2 v < 3 eps")
    print("    u < 5 v")
    print("    6 v - u < 3 eps")
    print("    2 u < 7 v")
    print("    10 v - 3 u < 3 eps")
    print()
    # Note u_a < 5 v_a is implied by 2 u_a < 7 v_a (since 7/2 = 3.5 < 5 — wait,
    # actually 2 u < 7 v means u < 3.5 v, which is stronger than u < 5 v).  So u < 5 v
    # is implied.  Drop it.
    # Also: 6 v - u < 3 eps and 10 v - 3 u < 3 eps.  Is one implied?
    # 10 v - 3 u = 6 v - u + (4 v - 2 u).  If 2 u > 7 v, then 4 v - 2 u < -3 v < 0,
    # so 10 v - 3 u < 6 v - u, so 10 v - 3 u < 3 eps is automatic from 6 v - u < 3 eps,
    # given u > 5 v / 2... wait we're in the regime u < 3.5 v.  Then 4 v - 2 u > 4 v - 7 v = -3 v.
    # So 10 v - 3 u = (6 v - u) + (4 v - 2 u).  In our regime 2 u < 7 v, we have 4 v - 2 u > 4 v - 7 v = -3v.
    # 10 v - 3 u > 6 v - u - 3 v = 3 v - u.  And 3 v - u > 0 iff u < 3 v.  Hmm.
    # Not clean.  Let me just compute the polytope area.

    print("  Polytope (drop the implied constraint u < 5v):")
    print("    P = { (u, v) : u + v > 0, u + 2v < 3eps, 2u < 7v, 6v - u < 3eps, 10v - 3u < 3eps }")
    print()
    print("  Area of P as a function of eps: compute by Monte Carlo or direct integration.")
    print()

    # Area scales linearly in eps^2 by self-similarity: scale (u, v) -> (eps * u', eps * v').
    # Then constraints become:
    #   u' + v' > 0
    #   u' + 2 v' < 3
    #   2 u' < 7 v'
    #   6 v' - u' < 3
    #   10 v' - 3 u' < 3
    # And area(P) = eps^2 * area(P').
    # Compute area(P'):

    # Vertices: find intersections of pairs of boundary lines that satisfy other constraints.
    # Lines:
    # L1: u' + 2 v' = 3                (pair 0)
    # L2: 7 v' - 2 u' = 0  (i.e., u' = 7v'/2)  (k_1 = 1 boundary)
    # L3: 6 v' - u' = 3                (pair 1)
    # L4: 10 v' - 3 u' = 3             (pair 2)
    # L5: u' + v' = 0                  (triangle)
    # L6: u' = 5 v'                    (k_0 = 4 boundary; might be cut)

    print("  Compute area(P') with eps = 1 by MC:")
    n = 50_000_000
    np.random.seed(0)
    # Sample (u', v') in box [-3, 6] x [-3, 6]
    u = np.random.uniform(-3, 6, n)
    v = np.random.uniform(-3, 6, n)
    accept = (
        (u + v > 0)
        & (u + 2 * v < 3)
        & (2 * u < 7 * v)
        & (6 * v - u < 3)
        & (10 * v - 3 * u < 3)
        & (u < 5 * v)  # k_0 = 4 branch
    )
    area_box = 9.0 * 9.0
    area_P = area_box * accept.sum() / n
    print(f"    Area(P') ≈ {area_P:.5f}")
    print(f"    => vol(R_eps near (2/3, 1/3)) ≈ {area_P:.4f} * eps^2")
    print()
    # By the involution symmetry (x,y) <-> (y,x) (which conjugates the BCZ map
    # for time-reversal), there's a symmetric region near (1/3, 2/3) — but actually
    # we just showed that the size-3 chain STARTING at (1/3, 2/3) gives P_2 ≈ 1/3,
    # not extreme.  So there's no direct counterpart near (1/3, 2/3).
    # HOWEVER: a size-3 cluster has 3 consecutive extreme pairs (X_0,X_1),(X_1,X_2),(X_2,X_3),
    # which is also the same as a 4-iterate window.  The "start" point (X_0, X_1) of
    # such a cluster can be near (2/3, 1/3) as shown above.
    # But the PROBABILITY of a pair being IN a size-3+ cluster requires conditioning
    # on the pair (in this case any of the three pairs).  Each pair (X_0, X_1) in
    # the size-3 cluster contributes once.
    # If we count "size-3 cluster entries" (the leftmost pair (X_0, X_1) of the
    # cluster), volume of entries = vol(R_eps near (2/3, 1/3)) only.
    # If we count "pairs IN a size-3 cluster", multiply by ~3 (one per pair).
    # Actually 3 distinct positions in the cluster have 3 distinct R-regions.
    # Let's enumerate.
    print("  ── Note: a size-3 cluster has 3 distinct STARTING positions for each ── ")
    print("    pair.  We've computed: entries (X_0, X_1) near (2/3, 1/3).")
    print("    The middle pair (X_1, X_2) of the cluster lives near (1/3, 2/3)")
    print("    (image of (2/3, 1/3) under k_0=4).")
    print("    The last pair (X_2, X_3) lives near (2/3, 1/3) again")
    print("    (image of (1/3, 2/3) under k_1=1).")
    print()
    # Pr(L>=3) = (1 / vol(T) / density) * integral over T of indicator(pair-IN-size-3+).
    # Triangle vol = 1/2.  Density = 2.  Total measure 1.
    # Pair-IN-size-3+ = at least one of the three positions holds.
    # By the BCZ invariance: in equilibrium, the three regions all have the same
    # invariant measure (the BCZ map is measure-preserving).
    # So Pr(L>=3) = 3 * 2 * vol(R_entry).
    # Wait: the three positions (R_entry, R_middle, R_last) are DISJOINT subsets of
    # T (different geometric locations); their UNION has invariant measure
    # = 3 * (invariant measure of each, by BCZ invariance).
    # Invariant measure of R_entry under density 2 = 2 * vol(R_entry) / 1 (already normalized).
    # So Pr(pair is in some size-3+ cluster) = 3 * 2 * vol(R_entry).
    # With area_P ≈ 0.108: Pr/eps^2 ≈ 3 * 2 * 0.108 = 0.65 — but empirical is ~ 2.2!
    # Let me double-check the empirical Pr/eps^2:
    # From MC above: Pr(L>=3)/eps^2 around 2.2 (in our MC) and similar in the scaling
    # law paper.
    # Hmm.  Actually re-reading the scaling law: Pr(L >= 3) "via n_3p / n_total".
    # n_total = total clusters, n_3p = size-3+ clusters.  But what we want for the
    # rigorous derivation is:
    # Pr(pair is part of size-3+ cluster) = 3 * Pr(pair is leftmost of size-3+ cluster)
    #                                     = 3 * vol(R_entry) / vol(T) * density_factor.
    # Or:
    # Pr(L>=3 in cluster | pair is extreme) = ... different.
    # Let's compute Pr(any pair has X*Y < t AND X_1 X_2 < t AND X_2 X_3 < t) — this is
    # vol(R_entry) * 2 (with normalized density). i.e. Pr_inv(R_entry) = 2 * vol(R_entry).
    # vol(R_entry) ≈ 0.108 * eps^2, so Pr_inv(R_entry) ≈ 0.216 * eps^2.
    print(f"    Prediction: Pr_inv(R_entry) = 2 * vol(R_entry) ≈ {2 * area_P:.4f} * eps^2")
    print(f"    Empirical Pr/eps^2 (from MC above) ≈ 2.1-2.3.")
    print()
    print("  >>> There's a factor of ~10x discrepancy.  Why?")
    print()
    print("  Possible reasons:")
    print("  1. The empirical 'Pr(L>=3)' = n_3p / n_clusters, not n_3p_pairs / n_pairs.")
    print("     If clusters are 1/2 the pairs density, factor would shift.")
    print("  2. The 3-cluster region near (1/3, 2/3) — we missed branches?")
    print("  3. The R_entry region has multiple components (e.g., the k_0 = 4 + k_1 = 1")
    print("     vs k_0 = 5 + ...) we didn't enumerate.")
    print("  4. The empirical 'pair belongs to size-3+ run' factor of 3 was already")
    print("     in our '3 * vol' count — but in the chain MC code, n_3p counts size-3+")
    print("     CLUSTERS (not pairs).  Pr(L>=3 cluster) = (# size-3+ clusters) / (chain length).")
    print()


if __name__ == "__main__":
    study_critical_point()
    print()
    derive_linear_geometry()
