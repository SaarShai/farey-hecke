"""Full decomposition: both corners + exact polytope area + connection to empirical Pr.

Goal:
  1. Verify that R_eps has TWO components: one near (2/3, 1/3) and one near (1/3, 2/3).
  2. Confirm the (1/3, 2/3) component comes from time-reversal (x,y)<->(y,x).
  3. Compute the EXACT polytope area (not MC, but vertex enumeration).
  4. Reconcile with empirical Pr(L>=3) / eps^2 ~ 2.2 from chain MC.
"""
import math
import numpy as np
from numba import njit

T_STAR = 2.0 / 9.0


@njit(cache=True)
def bcz_step(x, y):
    k = math.floor((1.0 + x) / y)
    return y, k * y - x


@njit(cache=True)
def is_size3_entry(x, y, t):
    if x <= 0.0 or y <= 0.0 or x >= 1.0 or y >= 1.0 or x + y <= 1.0:
        return False
    if x * y >= t:
        return False
    x1, y1 = bcz_step(x, y)
    if x1 * y1 >= t:
        return False
    x2, y2 = bcz_step(x1, y1)
    if x2 * y2 >= t:
        return False
    return True


@njit(cache=True)
def is_in_size3_cluster(x, y, t):
    """Is (x, y) part of a size-3+ cluster?

    Compute backwards iterates of x, y up to 2 steps, then check forward
    iterates up to 2 steps.  Pair (x, y) is part of a size-3+ cluster iff
    one of (X_{-2..0}, X_{-1..1}, X_{0..2}) starts a size-3 run.

    But backwards BCZ is not directly computable — actually it IS, since BCZ
    is invertible on T.  T_BCZ inverse: given (y, z) with z = k y - x,
    x = k y - z, so we need to recover k = floor((1+x)/y) — but this isn't
    determined by (y, z) alone.  Actually the BCZ map is bijective on T;
    given (y, z) ∈ T, x is uniquely determined: from the formula z = ky - x
    and the constraint x in (0,1) with x + y > 1, k is uniquely determined as
    k = floor((1+x)/y), and x = ky - z, so we get a unique k from solving
    (1 + ky - z)/y in [k, k+1) <=> 1 + ky - z in [ky, ky + y) <=> 1 - z in [0, y)
    <=> z in (1 - y, 1].  So z must be in (1 - y, 1], which is just the
    triangle constraint y + z > 1 plus z < 1.  Then k can be anything s.t.
    x = ky - z is in (0,1).  Hmm — so k IS undetermined by (y, z) alone.

    Conclusion: BCZ is NOT injective backwards (multiple pre-images, indexed by k).
    So we can't simply backwards-iterate.

    Alternative: just check if the chain starting at (x, y) has the pair
    as part of a size-3+ run.  This corresponds to:
      - (x, y) is the START of a size-3 run (already what is_size3_entry computes).
      - (x, y) is the MIDDLE of a size-3 run: x*y < t AND prev pair was extreme
        AND next pair is extreme.  But we don't have "prev pair".
      - (x, y) is the END of a size-3 run.

    Simpler approach: count chains by entry.  Pr(L>=3 cluster STARTS here) = vol(R_entry).
    Conditional on a cluster starting here, it contains ≥ 3 consecutive pairs.

    The "fraction of pairs that belong to size-3+ clusters" is then
      3 * Pr_inv(R_entry)  + (extra for size > 3)
    But since E[L | L >= 3] ≈ 5 empirically, the "extra" is significant.

    Let's just compute the entry probability and compare to n_3p / n_clusters.
    """
    return is_size3_entry(x, y, t)


def exact_polytope_area():
    """Exact vertex enumeration for the (2/3, 1/3) polytope.

    Polytope at eps = 1:
      P' = { (u, v) :
        u + v > 0                  (E1: triangle)
        u + 2 v < 3                (E2: pair 0)
        2 u < 7 v                  (E4: k_1=1 branch)
        6 v - u < 3                (E5: pair 1)
        10 v - 3 u < 3             (E6: pair 2)
      }
    """
    # Find all pairwise intersections of boundary lines (E1...E6), then keep
    # those satisfying all other constraints.
    lines = [
        ("E1", np.array([1, 1, 0])),    # u + v = 0
        ("E2", np.array([1, 2, 3])),    # u + 2v = 3
        ("E4", np.array([2, -7, 0])),   # 2u - 7v = 0
        ("E5", np.array([-1, 6, 3])),   # -u + 6v = 3
        ("E6", np.array([-3, 10, 3])),  # -3u + 10v = 3
    ]

    def in_polytope(u, v, tol=1e-9):
        return (
            u + v > -tol
            and u + 2 * v < 3 + tol
            and 2 * u < 7 * v + tol
            and -u + 6 * v < 3 + tol
            and -3 * u + 10 * v < 3 + tol
        )

    verts = []
    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            a, b = lines[i][1], lines[j][1]
            A = np.array([[a[0], a[1]], [b[0], b[1]]], dtype=float)
            rhs = np.array([a[2], b[2]], dtype=float)
            try:
                uv = np.linalg.solve(A, rhs)
                u, v = uv
            except np.linalg.LinAlgError:
                continue
            if in_polytope(u, v):
                verts.append((u, v, lines[i][0], lines[j][0]))

    # Deduplicate
    uniq = []
    for v in verts:
        is_new = True
        for u in uniq:
            if abs(u[0] - v[0]) < 1e-8 and abs(u[1] - v[1]) < 1e-8:
                is_new = False
                break
        if is_new:
            uniq.append(v)

    print(f"  Vertices of P' (eps=1):")
    for u, v, l1, l2 in uniq:
        print(f"    ({u:+.6f}, {v:+.6f})   from {l1} ∩ {l2}")

    # Compute area via convex hull or shoelace formula.
    pts = np.array([(v[0], v[1]) for v in uniq])
    if len(pts) < 3:
        print("  Not enough vertices.")
        return None
    # Sort by angle around centroid.
    cx, cy = pts.mean(axis=0)
    angles = np.arctan2(pts[:, 1] - cy, pts[:, 0] - cx)
    order = np.argsort(angles)
    pts_sorted = pts[order]
    # Shoelace.
    area = 0.0
    n = len(pts_sorted)
    for i in range(n):
        x0, y0 = pts_sorted[i]
        x1, y1 = pts_sorted[(i + 1) % n]
        area += x0 * y1 - x1 * y0
    area = abs(area) / 2.0
    print(f"\n  Exact area(P') = {area:.6f}")
    return area


def verify_two_corners():
    """Verify R_eps has hits near BOTH (1/3, 2/3) and (2/3, 1/3)."""
    print("=" * 70)
    print("Verify R_eps has hits in BOTH corners")
    print("=" * 70)
    eps = 1e-3
    t = T_STAR + eps
    n_grid = 800
    # First corner: (1/3, 2/3)
    cx, cy = 1.0 / 3.0, 2.0 / 3.0
    w = 0.05
    n1 = 0
    for i in range(n_grid):
        for j in range(n_grid):
            u = -w + 2 * w * (i + 0.5) / n_grid
            v = -w + 2 * w * (j + 0.5) / n_grid
            x, y = cx + u, cy + v
            if is_size3_entry(x, y, t):
                n1 += 1
    # Second corner: (2/3, 1/3)
    cx, cy = 2.0 / 3.0, 1.0 / 3.0
    n2 = 0
    for i in range(n_grid):
        for j in range(n_grid):
            u = -w + 2 * w * (i + 0.5) / n_grid
            v = -w + 2 * w * (j + 0.5) / n_grid
            x, y = cx + u, cy + v
            if is_size3_entry(x, y, t):
                n2 += 1
    cell = (2 * w / n_grid) ** 2
    vol1 = n1 * cell
    vol2 = n2 * cell
    print(f"  vol near (1/3, 2/3) = {vol1:.4e}  ({n1} hits)")
    print(f"  vol near (2/3, 1/3) = {vol2:.4e}  ({n2} hits)")
    print(f"  vol1/eps^2 = {vol1/(eps**2):.4f}")
    print(f"  vol2/eps^2 = {vol2/(eps**2):.4f}")
    print(f"  total = {(vol1+vol2)/(eps**2):.4f}")
    return vol1 + vol2


def find_all_branches_at_critical():
    """Enumerate which (k_0, k_1) branch combinations give size-3 entries.

    Near (1/3, 2/3): k_0 = floor((1+x)/y) at (1/3, 2/3) = floor(2) = 2.
                     Generically: k_0 = 1 (if (1+x)/y < 2) or k_0 = 2.
    Near (2/3, 1/3): k_0 = floor((1+x)/y) at (2/3, 1/3) = floor(5) = 5.
                     Generically: k_0 = 4 (if (1+x)/y < 5) or k_0 = 5.

    Test all 4 (k_0, k_1) branch combos near each center.
    """
    print("=" * 70)
    print("Enumerate (k_0, k_1) branches with size-3 entry near each critical pair")
    print("=" * 70)
    eps = 1e-3
    t = T_STAR + eps
    n_grid = 500
    w = 0.03

    for (cx, cy, label) in [(1/3, 2/3, "(1/3, 2/3)"), (2/3, 1/3, "(2/3, 1/3)")]:
        print(f"\n  Near {label}:")
        branches = {}
        for i in range(n_grid):
            for j in range(n_grid):
                u = -w + 2 * w * (i + 0.5) / n_grid
                v = -w + 2 * w * (j + 0.5) / n_grid
                x, y = cx + u, cy + v
                if not (0 < x < 1 and 0 < y < 1 and x + y > 1):
                    continue
                if x * y >= t:
                    continue
                k0 = math.floor((1 + x) / y)
                x1, y1 = bcz_step(x, y)
                if x1 * y1 >= t:
                    continue
                if not (0 < x1 < 1 and 0 < y1 < 1 and x1 + y1 > 1):
                    continue
                k1 = math.floor((1 + x1) / y1)
                x2, y2 = bcz_step(x1, y1)
                if x2 * y2 >= t:
                    continue
                key = (k0, k1)
                branches[key] = branches.get(key, 0) + 1
        for k, n in sorted(branches.items()):
            print(f"    (k_0={k[0]}, k_1={k[1]}):  {n} hits")


def main():
    print("=" * 70)
    print("EXACT polytope area near (2/3, 1/3) — vertex enumeration")
    print("=" * 70)
    area = exact_polytope_area()
    print()
    print(f"  Implied vol(R_entry, single corner) = {area:.4f} * eps^2")
    print(f"  Times 2 (both corners by time-reversal): {2*area:.4f} * eps^2")
    print(f"  Pr_inv (density 2 on T): Pr = 2 * vol_total = {4*area:.4f} * eps^2")
    print()

    verify_two_corners()
    print()
    find_all_branches_at_critical()


if __name__ == "__main__":
    main()
