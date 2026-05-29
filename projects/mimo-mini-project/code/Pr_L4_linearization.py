"""Derivation of the linearized polytope for Pr(L >= 4).

For L >= 4 at corner (2/3, 1/3): the chain is
  (X_0, X_1) near (2/3, 1/3),   k_0 = 4 -> (X_1, X_2) near (1/3, 2/3)
  (X_1, X_2) near (1/3, 2/3),   k_1 = 1 -> (X_2, X_3) near (2/3, 1/3)
  (X_2, X_3) near (2/3, 1/3),   k_2 = 4 -> (X_3, X_4) near (1/3, 2/3)

Need: X_0 X_1, X_1 X_2, X_2 X_3, X_3 X_4 < 2/9 + eps.

Write X_0 = 2/3 + u, X_1 = 1/3 + v.

Recall from R_eps derivation:
  X_2 = 4 X_1 - X_0 = 2/3 + 4v - u
  X_3 = X_2 - X_1 = 1/3 + 3v - u    [since k_1 = 1, X_3 = X_2 - X_1]
  X_4 = 4 X_3 - X_2 = 4(1/3 + 3v - u) - (2/3 + 4v - u) = 2/3 + 8v - 3u

So (X_3, X_4) = (1/3 + 3v - u, 2/3 + 8v - 3u), near (1/3, 2/3).

Compute X_3 X_4 (LINEAR ORDER):
  X_3 X_4 = (1/3 + 3v - u)(2/3 + 8v - 3u)
          = 2/9 + (8v - 3u)/3 + 2(3v - u)/3 + O(quadratic)
          = 2/9 + (8v - 3u + 6v - 2u)/3
          = 2/9 + (14v - 5u)/3

So X_3 X_4 < 2/9 + eps  <=>  14v - 5u < 3 eps.

Also we need k_2 = 4 (i.e., the floor at (X_2, X_3) must equal 4):
  f at (X_2, X_3) = (1 + X_2)/X_3 = (1 + 2/3 + 4v - u)/(1/3 + 3v - u)
                  = (5/3 + 4v - u)/(1/3 + 3v - u)
  At (u,v)=(0,0): f = (5/3)/(1/3) = 5.  Hmm, that's k=5 not k=4!

Wait, let me recompute.  At (X_2, X_3) near (2/3, 1/3), but with what x and y?
  X_2 = 2/3 + 4v - u   (the x-coord of pair 2 is X_2)
  X_3 = 1/3 + 3v - u   (the y-coord is X_3)

OK so f(X_2, X_3) = (1 + X_2)/X_3.  At base (2/3, 1/3): f = (5/3)/(1/3) = 5.

So k_2 = floor(5 + ...) = 5 or 4 depending on sign.

For k_2 = 4: f < 5, i.e., (1 + X_2)/X_3 < 5, i.e., 1 + X_2 < 5 X_3.
  1 + 2/3 + 4v - u < 5(1/3 + 3v - u)
  5/3 + 4v - u < 5/3 + 15v - 5u
  4v - u < 15v - 5u
  4u < 11v.

For k_2 = 5: 4u > 11v, image X_4 = 5 X_3 - X_2 = 5(1/3 + 3v - u) - (2/3 + 4v - u)
            = 1 + 11v - 4u.  Then X_3 X_4 = (1/3 + 3v - u)(1 + 11v - 4u)
            = 1/3 + ... ~ 1/3 > 2/9, NOT extreme.

So the ONLY branch giving L>=4 at corner (2/3, 1/3) is (k_0=4, k_1=1, k_2=4).

Let me redo the polytope constraints:

  E1 (triangle):  u + v > 0
  E2 (pair 0):    u + 2v < 3 eps      [X_0 X_1 < 2/9 + eps]
  E3 (k_0 = 4):   u < 5v
  E4 (pair 1):    6v - u < 3 eps      [X_1 X_2 < 2/9 + eps]
  E5 (k_1 = 1):   2u < 7v
  E6 (pair 2):    10v - 3u < 3 eps    [X_2 X_3 < 2/9 + eps]
  E7 (k_2 = 4):   4u < 11v
  E8 (pair 3):    14v - 5u < 3 eps    [X_3 X_4 < 2/9 + eps]

Note: under 2u < 7v (E5), 2u/v < 7/2.  Compare 4u < 11v: 4u/v < 11, so u/v < 11/4 = 2.75.
And 7v/2: u/v < 7/2 = 3.5.  So E7 (u/v < 11/4) is TIGHTER than E5 (u/v < 7/2) when v>0.
That means E7 implies E5, so E5 becomes redundant.

Also, recall E3 (u < 5v) was redundant under E5.  Now with E7 = u < 11v/4 < 5v, E3 is also redundant.

So the active constraints are: E1, E2, E4, E6, E7, E8.

Scale (u, v) = eps * (u', v'):
  E1':  u' + v' > 0
  E2':  u' + 2v' < 3
  E4':  6v' - u' < 3
  E6':  10v' - 3u' < 3
  E7':  4u' < 11v'      [HOMOGENEOUS, no eps scaling]
  E8':  14v' - 5u' < 3

Wait, E7 is u < 11v/4, equivalently 4u - 11v < 0, which is HOMOGENEOUS — does not
scale with eps.  So under (u, v) = eps * (u', v'), it stays as 4u' - 11v' < 0.

So the SCALED polytope P_4' is:
  u' + v' > 0
  u' + 2 v' < 3
  6 v' - u' < 3
  10 v' - 3 u' < 3
  4 u' < 11 v'         [homogeneous]
  14 v' - 5 u' < 3

5 inhomogeneous + 1 homogeneous = the polytope is bounded and Leb²(P_4') = (area).
Then Leb²(P_eps^{(4)}) = eps^2 * area.

WAIT — that would mean Pr(L>=4) ~ eps^2, NOT eps^3!  So the constraint count works out
because k_2=4 is a HOMOGENEOUS constraint (does not consume an order of eps).

But let me check: is the new constraint E8 (14v - 5u < 3 eps) actually ACTIVE given E2, E4, E6?
Let me check at the boundary of the L>=3 polytope.  Recall the L>=3 polytope at corner (2/3, 1/3) had:
  Constraints: E1, E2, E4, E5, E6, and the polytope was a QUADRILATERAL with vertices
    V_1 = (0, 0)        from E1 ∩ E5
    V_2 = (-3/13, 3/13) from E1 ∩ E6
    V_3 = (21/11, 6/11) from E2 ∩ E5
    V_4 = (3/2, 3/4)    from E2 ∩ E4

Wait but with k_2=4 active, E5 (2u' < 7v') is implied by E7 (4u' < 11v').  And E5 was
one of the binding constraints (V_1, V_3 lie on E5).  Now E7 replaces it as a tighter
binding constraint.  So V_1, V_3 will move to lie on E7.

But also E8 (14v' - 5u' < 3) is a new constraint.  Let me check: at V_4 = (3/2, 3/4):
  14*(3/4) - 5*(3/2) = 21/2 - 15/2 = 6/2 = 3.  So V_4 is exactly ON E8!  Interesting.

At V_2 = (-3/13, 3/13):
  14*(3/13) - 5*(-3/13) = 42/13 + 15/13 = 57/13 ≈ 4.38 > 3.  So V_2 is OUTSIDE E8.
  E8 cuts away V_2.

So the L>=4 polytope is the L>=3 polytope with E5 replaced by E7 (tighter) and with the new
constraint E8 cutting off the V_2 corner.

Let me enumerate vertices of P_4' systematically.
"""
from fractions import Fraction
from itertools import combinations


def vertex(L1, L2):
    """Intersect two lines: a1 u + b1 v = c1, a2 u + b2 v = c2."""
    a1, b1, c1 = L1
    a2, b2, c2 = L2
    det = a1 * b2 - a2 * b1
    if det == 0:
        return None
    u = (c1 * b2 - c2 * b1) / det
    v = (a1 * c2 - a2 * c1) / det
    return (Fraction(u), Fraction(v))


# All constraints as (a, b, c) meaning a*u + b*v < c (or > for triangle).
# Direction: True means a*u + b*v < c is satisfied (interior), False means we want > c.
constraints = {
    'E1_triangle':   (Fraction(-1), Fraction(-1), Fraction(0)),    # u + v > 0 <=> -u - v < 0
    'E2_pair0':      (Fraction(1),  Fraction(2),  Fraction(3)),    # u + 2v < 3
    'E4_pair1':      (Fraction(-1), Fraction(6),  Fraction(3)),    # -u + 6v < 3
    'E6_pair2':      (Fraction(-3), Fraction(10), Fraction(3)),    # -3u + 10v < 3
    'E7_k2_4':       (Fraction(4),  Fraction(-11),Fraction(0)),    # 4u - 11v < 0
    'E8_pair3':      (Fraction(-5), Fraction(14), Fraction(3)),    # -5u + 14v < 3
}


def check_interior(point, exclude=None):
    """Verify point satisfies all constraints (strict or weakly)."""
    u, v = point
    for name, (a, b, c) in constraints.items():
        if name == exclude:
            continue
        val = a * u + b * v
        if val > c:
            return False, name, val, c
    return True, None, None, None


# Enumerate all pairs of constraints, find intersection, test feasibility.
names = list(constraints.keys())
verts = []
for n1, n2 in combinations(names, 2):
    pt = vertex(constraints[n1], constraints[n2])
    if pt is None:
        continue
    # Check that pt lies on the boundary of both (it does by construction).
    # Then check it satisfies the OTHER constraints weakly.
    ok = True
    for n3 in names:
        if n3 in (n1, n2):
            continue
        a, b, c = constraints[n3]
        if a * pt[0] + b * pt[1] > c:
            ok = False
            break
    if ok:
        verts.append((n1, n2, pt))

print("Vertices of P_4':")
for (n1, n2, (u, v)) in verts:
    print(f"  {n1} ∩ {n2}:  (u', v') = ({u}, {v}) = ({float(u):.4f}, {float(v):.4f})")
print()


# Now sort vertices CCW and compute area via shoelace.
import math
unique_pts = list(set([pt for (_, _, pt) in verts]))
print(f"Number of unique vertices: {len(unique_pts)}")
# Center
cx = sum(p[0] for p in unique_pts) / len(unique_pts)
cy = sum(p[1] for p in unique_pts) / len(unique_pts)
sorted_pts = sorted(unique_pts, key=lambda p: math.atan2(float(p[1] - cy), float(p[0] - cx)))
print("CCW sorted vertices:")
for p in sorted_pts:
    print(f"  ({p[0]}, {p[1]}) = ({float(p[0]):.4f}, {float(p[1]):.4f})")

# Shoelace
n = len(sorted_pts)
two_area = Fraction(0)
for i in range(n):
    x1, y1 = sorted_pts[i]
    x2, y2 = sorted_pts[(i+1) % n]
    two_area += x1 * y2 - x2 * y1
area = abs(two_area) / 2
print(f"\nArea of P_4' = {area} = {float(area):.6f}")
