"""Closed-form computation of the polytope area near (2/3, 1/3).

Vertices found numerically:
  V1 = (0, 0)                  from E1 ∩ E4   (triangle ∩ k_1=1 branch)
  V2 = (-3/13, 3/13)           from E1 ∩ E6   (triangle ∩ pair 2)
  V3 = (21/11, 6/11)           from E2 ∩ E4   (pair 0 ∩ k_1=1 branch)
  V4 = (3/2, 3/4)              from E2 ∩ E5   (pair 0 ∩ pair 1)

Verify rationally:
  V1 = E1 ∩ E4:  u + v = 0  AND  2u - 7v = 0  =>  v = 0, u = 0.  OK
  V2 = E1 ∩ E6:  u + v = 0  AND  10v - 3u = 3  =>  u = -v, 10v + 3v = 3, v = 3/13.
                  V2 = (-3/13, 3/13).  Check E1: -3/13 + 3/13 = 0 OK.
                  Check E6: -3(-3/13) + 10(3/13) = 9/13 + 30/13 = 39/13 = 3.  OK.
  V3 = E2 ∩ E4:  u + 2v = 3  AND  2u = 7v  =>  u = 7v/2,  7v/2 + 2v = 3,  11v/2 = 3, v = 6/11, u = 21/11.
                  V3 = (21/11, 6/11).
                  Check E4: 2(21/11) - 7(6/11) = (42-42)/11 = 0.  OK.
  V4 = E2 ∩ E5:  u + 2v = 3  AND  -u + 6v = 3  =>  add: 8v = 6, v = 3/4, u = 3 - 3/2 = 3/2.
                  V4 = (3/2, 3/4).
                  Check E5: -3/2 + 18/4 = -3/2 + 9/2 = 6/2 = 3.  OK.

Now compute area by shoelace, sorted counterclockwise.

Need to order the vertices.  Let's compute angles from centroid:
  centroid ≈ ((0 + (-3/13) + 21/11 + 3/2) / 4, (0 + 3/13 + 6/11 + 3/4) / 4)
"""
from fractions import Fraction


def shoelace(verts):
    """Shoelace formula on list of (Fraction, Fraction) tuples.

    Vertices must be in cyclic order.
    """
    n = len(verts)
    s = Fraction(0)
    for i in range(n):
        x0, y0 = verts[i]
        x1, y1 = verts[(i + 1) % n]
        s += x0 * y1 - x1 * y0
    return abs(s) / 2


def main():
    # Vertices as Fractions (with eps = 1).
    V1 = (Fraction(0), Fraction(0))
    V2 = (Fraction(-3, 13), Fraction(3, 13))
    V3 = (Fraction(21, 11), Fraction(6, 11))
    V4 = (Fraction(3, 2), Fraction(3, 4))

    # Sort counterclockwise around centroid.
    pts = [V1, V2, V3, V4]
    cx = sum(p[0] for p in pts) / 4
    cy = sum(p[1] for p in pts) / 4
    print(f"  Centroid: ({cx}, {cy}) = ({float(cx):.4f}, {float(cy):.4f})")

    import math
    def ang(p):
        return math.atan2(float(p[1] - cy), float(p[0] - cx))
    pts_sorted = sorted(pts, key=ang)
    print()
    print(f"  Sorted counterclockwise:")
    for p in pts_sorted:
        print(f"    ({p[0]}, {p[1]})  = ({float(p[0]):.6f}, {float(p[1]):.6f})")

    A = shoelace(pts_sorted)
    print()
    print(f"  Area(P') = {A} = {float(A):.6f}")
    print()

    # Verify against numerical 0.566434.
    print(f"  Numerical: 0.566434")
    print(f"  Exact:     {float(A):.6f}")
    print()

    # Prefactor for Pr(L>=3):
    # vol(R_entry, one corner) = A * eps^2
    # vol(R_eps total) = 2 A * eps^2 (two corners by symmetry)
    # Pr_inv(R_eps) = (1 / vol_inv(T)) * integral_{R_eps} (2 dx dy)
    #              = 2 * vol(R_eps) / 1 = 4 A * eps^2
    # (since invariant measure is (2 dx dy on T) normalized to total mass 1).
    C_prefactor = 4 * A
    print(f"  Pr(L>=3) = (4 * {A}) * eps^2 + o(eps^2)")
    print(f"           = ({float(C_prefactor):.6f}) * eps^2")
    print()
    print(f"  Empirical chain MC: Pr(L>=3) / eps^2 ≈ 2.13-2.31 (round-2 paper)")
    print(f"  Predicted: 2 * 2 * {float(A):.4f} = {float(C_prefactor):.4f}")
    print()

    # As a rational:
    print(f"  Exact rational: Pr(L>=3) = ({C_prefactor.numerator}/{C_prefactor.denominator}) * eps^2 + o(eps^2)")


if __name__ == "__main__":
    main()
