"""Compute the (1/3, 2/3) polytope area exactly, verify it equals 81/143."""
from fractions import Fraction


def shoelace(verts):
    n = len(verts)
    s = Fraction(0)
    for i in range(n):
        x0, y0 = verts[i]
        x1, y1 = verts[(i + 1) % n]
        s += x0 * y1 - x1 * y0
    return abs(s) / 2


def main():
    # Polytope near (1/3, 2/3), branch (k_0=1, k_1=4):
    #   E1 triangle: u + v > 0
    #   E2 pair 0:   2u + v < 3 eps
    #   E3 k_0=1:    u < 2v        (i.e. 2v - u > 0)
    #   E4 pair 1:   3v - 2u < 3 eps
    #   E5 k_1=4:    5u < 4v       (i.e. 4v - 5u > 0)
    #   E6 pair 2:   5v - 6u < 3 eps
    # Set eps = 1 (rescaled by self-similarity).

    # Find all pairwise intersections of EQUALITY versions of the constraints.
    lines = {
        "E1": (Fraction(1), Fraction(1), Fraction(0)),       # u + v = 0
        "E2": (Fraction(2), Fraction(1), Fraction(3)),       # 2u + v = 3
        "E3": (Fraction(1), Fraction(-2), Fraction(0)),      # u - 2v = 0
        "E4": (Fraction(-2), Fraction(3), Fraction(3)),      # -2u + 3v = 3
        "E5": (Fraction(5), Fraction(-4), Fraction(0)),      # 5u - 4v = 0
        "E6": (Fraction(-6), Fraction(5), Fraction(3)),      # -6u + 5v = 3
    }

    def in_polytope(u, v):
        return (
            u + v > 0
            and 2 * u + v < 3
            and u < 2 * v
            and -2 * u + 3 * v < 3
            and 5 * u < 4 * v
            and -6 * u + 5 * v < 3
        )

    # Enumerate intersections.
    keys = list(lines.keys())
    verts = []
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            a1, b1, c1 = lines[keys[i]]
            a2, b2, c2 = lines[keys[j]]
            det = a1 * b2 - a2 * b1
            if det == 0:
                continue
            u = (c1 * b2 - c2 * b1) / det
            v = (a1 * c2 - a2 * c1) / det
            # Check non-strict for vertex membership (closed polytope).
            if not (u + v >= 0 and 2 * u + v <= 3 and u <= 2 * v
                    and -2 * u + 3 * v <= 3 and 5 * u <= 4 * v
                    and -6 * u + 5 * v <= 3):
                continue
            verts.append((u, v, keys[i], keys[j]))

    # Deduplicate.
    uniq = []
    for v in verts:
        is_new = True
        for u in uniq:
            if u[0] == v[0] and u[1] == v[1]:
                is_new = False
                break
        if is_new:
            uniq.append(v)

    print(f"  Vertices of P'_(1/3, 2/3):")
    for u, v, l1, l2 in uniq:
        print(f"    ({u}, {v})  = ({float(u):+.6f}, {float(v):+.6f})   from {l1} ∩ {l2}")

    pts = [(v[0], v[1]) for v in uniq]
    if len(pts) < 3:
        print(f"  Not enough vertices.")
        return

    # Sort counterclockwise.
    import math
    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts)
    def ang(p):
        return math.atan2(float(p[1] - cy), float(p[0] - cx))
    pts.sort(key=ang)
    print()
    A = shoelace(pts)
    print(f"  Area(P'_(1/3, 2/3)) = {A} = {float(A):.6f}")
    print()
    print(f"  Compare to (2/3, 1/3) corner: 81/143 = {float(Fraction(81, 143)):.6f}")
    print(f"  Equal? {A == Fraction(81, 143)}")


if __name__ == "__main__":
    main()
