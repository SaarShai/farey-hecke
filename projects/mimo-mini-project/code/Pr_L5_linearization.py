"""Extending to L >= 5, 6, ... — full chain on the (1/3,2/3)<->(2/3,1/3) 2-cycle.

At corner (2/3, 1/3), the BCZ map iterates as follows (using linearization at (2/3,1/3)):
   X_0 = 2/3 + u_0
   X_1 = 1/3 + v_0       (= 1/3 + u_1 viewed from corner (1/3,2/3) starting)

In linearized coords (u, v), the chain stays on the 2-cycle iff the floor sequence
alternates 4, 1, 4, 1, ...

Each iterate is LINEAR in (u, v).  Let me compute the iterates symbolically.
"""
from fractions import Fraction
from itertools import combinations
import math


# State at step i: linearized as a vector (X_i - target, X_{i+1} - target_next).
# Target_i alternates (2/3, 1/3) for even i, (1/3, 2/3) for odd i.

# Maintain (X_i, X_{i+1}) as affine expressions in (u, v) where u = X_0 - 2/3, v = X_1 - 1/3.

# X_0 = 2/3 + u
# X_1 = 1/3 + v
# k_0 = 4 -> X_2 = 4*X_1 - X_0 = 4/3 + 4v - 2/3 - u = 2/3 + 4v - u
# k_1 = 1 -> X_3 = X_2 - X_1 = 2/3 + 4v - u - 1/3 - v = 1/3 + 3v - u
# k_2 = 4 -> X_4 = 4*X_3 - X_2 = 4/3 + 12v - 4u - 2/3 - 4v + u = 2/3 + 8v - 3u
# k_3 = 1 -> X_5 = X_4 - X_3 = 2/3 + 8v - 3u - 1/3 - 3v + u = 1/3 + 5v - 2u
# k_4 = 4 -> X_6 = 4*X_5 - X_4 = 4/3 + 20v - 8u - 2/3 - 8v + 3u = 2/3 + 12v - 5u
# k_5 = 1 -> X_7 = X_6 - X_5 = 2/3 + 12v - 5u - 1/3 - 5v + 2u = 1/3 + 7v - 3u

# Let's automate: represent X_i = base_i + A_i * u + B_i * v
# base_i alternates 2/3, 1/3, 2/3, 1/3, ...

def iterate_chain(N_iter):
    """Compute symbolic iterates X_0, ..., X_N as affine in (u, v)."""
    # X_i = (base, A, B) meaning X_i = base + A*u + B*v
    X = [None] * (N_iter + 1)
    X[0] = (Fraction(2, 3), Fraction(1), Fraction(0))      # 2/3 + u
    X[1] = (Fraction(1, 3), Fraction(0), Fraction(1))      # 1/3 + v
    for i in range(N_iter - 1):
        # k_i = 4 for even i, 1 for odd i (target 2-cycle)
        k = 4 if i % 2 == 0 else 1
        b_prev, A_prev, B_prev = X[i]
        b_curr, A_curr, B_curr = X[i+1]
        # X_{i+2} = k * X_{i+1} - X_i
        b_next = k * b_curr - b_prev
        A_next = k * A_curr - A_prev
        B_next = k * B_curr - B_prev
        X[i+2] = (b_next, A_next, B_next)
    return X


def product_constraint(Xi, Xi1):
    """Compute the LINEARIZED constraint X_i * X_{i+1} < 2/9 + eps.

    Returns (a, b, c) meaning a*u + b*v < c*eps (scaled: c=3 because eps -> 3eps in (u,v)/eps coords).
    Actually, we'll return the natural form: a*u + b*v < 3*eps (we scale eps -> 1, u' = u/eps).
    """
    b1, A1, B1 = Xi
    b2, A2, B2 = Xi1
    # Product = b1*b2 + b1*(A2*u + B2*v) + b2*(A1*u + B1*v) + O(2)
    # Linear part = (b1*A2 + b2*A1) u + (b1*B2 + b2*B1) v
    # Base = b1*b2 should equal 2/9 if X_i is at corner.
    base = b1 * b2
    if base != Fraction(2, 9):
        # Not at the critical corner; product is bounded away from 2/9; not extreme.
        return None
    a = b1 * A2 + b2 * A1
    b = b1 * B2 + b2 * B1
    # Constraint: base + a*u + b*v < 2/9 + eps  =>  a*u + b*v < eps
    # In scaled coords (u', v') = (u/eps, v/eps): a*u' + b*v' < 1.
    # Multiply through by 3 to clear denominators (1/3 factors come from b's).
    # Constraint in raw form: a*u + b*v < eps.
    return (a, b, Fraction(1))  # will multiply by 3 later if needed


def floor_constraint(Xi, Xi1, k_required):
    """Floor at (X_i, X_{i+1}) equals k_required.

    f = (1 + X_i) / X_{i+1}, k = floor(f).
    At linearization: (1 + base_x)/(base_y) = some integer.
    For (X_i, X_{i+1}) near (2/3, 1/3): f at base = (5/3)/(1/3) = 5.  So k=4 or 5.
    For (X_i, X_{i+1}) near (1/3, 2/3): f at base = (4/3)/(2/3) = 2.  So k=1 or 2.

    k_required = 4 (at (2/3,1/3)): f < 5 => (1+X_i) < 5*X_{i+1}.
    k_required = 1 (at (1/3,2/3)): f < 2 => (1+X_i) < 2*X_{i+1}.
    """
    b1, A1, B1 = Xi
    b2, A2, B2 = Xi1
    # condition: (1 + X_i) < (k_required + 1) * X_{i+1}
    # i.e., (1 + b1 + A1*u + B1*v) < (k+1)(b2 + A2*u + B2*v)
    # base: 1 + b1 - (k+1)*b2 should equal 0 for marginal floor.
    kp1 = k_required + 1
    base = 1 + b1 - kp1 * b2
    if base != 0:
        # Not marginal; constraint is automatic or impossible.
        return None
    a = A1 - kp1 * A2
    b = B1 - kp1 * B2
    # Constraint: a*u + b*v < 0  (homogeneous, no eps).
    return (a, b, Fraction(0))


def compute_polytope_L(L_target):
    """Compute the linearized polytope for L >= L_target at corner (2/3, 1/3).

    Constraints:
      - Triangle: u + v > 0  (or -u - v < 0)
      - Product constraints: X_i * X_{i+1} < 2/9 + eps for i = 0, 1, ..., L-1
      - Floor constraints: k_i = 4 for even i in [0, L-2], k_i = 1 for odd i.
    """
    X = iterate_chain(L_target + 1)
    constraints = {}
    # Triangle
    constraints['E_triangle'] = (Fraction(-1), Fraction(-1), Fraction(0))
    # Product constraints (L of them: i = 0 .. L-1)
    for i in range(L_target):
        pc = product_constraint(X[i], X[i+1])
        if pc is None:
            print(f"  Pair {i} product base != 2/9, returning None")
            return None
        constraints[f'E_pair{i}'] = pc
    # Floor constraints (L-1 of them: i = 0 .. L-2)
    # Actually L-2 floors are required to determine the chain through L+1 points.
    # The Lth product X_{L-1} X_L requires floors k_0, ..., k_{L-2}.
    for i in range(L_target - 1):
        k_req = 4 if i % 2 == 0 else 1
        fc = floor_constraint(X[i], X[i+1], k_req)
        if fc is None:
            return None
        constraints[f'E_k{i}_{k_req}'] = fc
    return constraints


def polytope_area(constraints, scale_eps=Fraction(1)):
    """Compute area of polytope {a*u + b*v < c*eps for inhomogeneous, < 0 for homogeneous}.

    Scale (u, v) -> (u/eps, v/eps) so that constraints become a*u' + b*v' < c.
    """
    # Substitute u = eps * u', v = eps * v'.  Inhomogeneous: c*eps becomes c (in u' coords).
    # Homogeneous (c=0) stays homogeneous.
    # Enumerate pairs, find intersections, test feasibility.
    names = list(constraints.keys())
    verts = []
    for n1, n2 in combinations(names, 2):
        a1, b1, c1 = constraints[n1]
        a2, b2, c2 = constraints[n2]
        det = a1 * b2 - a2 * b1
        if det == 0:
            continue
        u = (c1 * b2 - c2 * b1) / det
        v = (a1 * c2 - a2 * c1) / det
        # Test feasibility
        ok = True
        for n3 in names:
            if n3 in (n1, n2):
                continue
            a, b, c = constraints[n3]
            val = a * u + b * v
            if val > c + Fraction(1, 10**12):  # tolerance for "ON boundary"
                ok = False
                break
        if ok:
            verts.append((u, v))
    # Unique
    unique_pts = sorted(set(verts))
    if len(unique_pts) < 3:
        return Fraction(0), unique_pts
    # Sort CCW
    cx = sum(p[0] for p in unique_pts) / len(unique_pts)
    cy = sum(p[1] for p in unique_pts) / len(unique_pts)
    sorted_pts = sorted(unique_pts, key=lambda p: math.atan2(float(p[1] - cy), float(p[0] - cx)))
    n = len(sorted_pts)
    two_area = Fraction(0)
    for i in range(n):
        x1, y1 = sorted_pts[i]
        x2, y2 = sorted_pts[(i+1) % n]
        two_area += x1 * y2 - x2 * y1
    return abs(two_area) / 2, sorted_pts


# Run for L = 3, 4, 5, 6, 7
print(f"{'L':>3s}  {'area_corner':>15s}  {'2*area_corner':>15s}  {'Pr/eps^2 (Pr=4*area)':>22s}  {'#verts':>8s}")
print("-" * 80)
results = []
for L in range(3, 9):
    cons = compute_polytope_L(L)
    if cons is None:
        print(f"  L={L}: constraints undefined")
        continue
    area, verts = polytope_area(cons)
    # area is area at ONE corner.  Total Leb^2 = 2 * area.  Pr_inv = 2 * (2*area) = 4*area.
    pr_coef = 4 * area
    print(f"{L:3d}  {str(area):>15s}  {str(2*area):>15s}  {str(pr_coef):>22s}  {len(verts):8d}")
    print(f"      = {float(area):.6f}      = {float(2*area):.6f}        = {float(pr_coef):.6f}")
    results.append((L, area, verts))

print()
print("Vertices for L=3 (sanity check, should give 81/143):")
cons3 = compute_polytope_L(3)
a3, v3 = polytope_area(cons3)
for p in v3:
    print(f"  ({p[0]}, {p[1]})")
print(f"Area = {a3} (expected 81/143 = {Fraction(81,143)})")

print()
print("Vertices for L=4:")
cons4 = compute_polytope_L(4)
a4, v4 = polytope_area(cons4)
for p in v4:
    print(f"  ({p[0]}, {p[1]})")
print(f"Area = {a4}")

print()
print("Vertices for L=5:")
cons5 = compute_polytope_L(5)
a5, v5 = polytope_area(cons5)
for p in v5:
    print(f"  ({p[0]}, {p[1]})")
print(f"Area = {a5}")

print()
print("Vertices for L=6:")
cons6 = compute_polytope_L(6)
a6, v6 = polytope_area(cons6)
for p in v6:
    print(f"  ({p[0]}, {p[1]})")
print(f"Area = {a6}")
