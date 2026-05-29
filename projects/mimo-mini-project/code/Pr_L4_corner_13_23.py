"""Verify corner (1/3, 2/3) gives the same polytope area for L=4."""
from fractions import Fraction
from itertools import combinations
import math


# At (1/3, 2/3): X_0 = 1/3 + u, X_1 = 2/3 + v.
# k_0 = 1 -> X_2 = X_1 - X_0 = 1/3 + v - u
# k_1 = 4 -> X_3 = 4*X_2 - X_1 = 4(1/3 + v - u) - (2/3 + v) = 2/3 + 3v - 4u
# k_2 = 1 -> X_4 = X_3 - X_2 = (2/3 + 3v - 4u) - (1/3 + v - u) = 1/3 + 2v - 3u
# Products:
# X_0 X_1 = (1/3 + u)(2/3 + v) = 2/9 + v/3 + 2u/3 + uv = 2/9 + (v + 2u)/3 + O(2)
#   => 2u + v < 3 eps
# X_1 X_2 = (2/3 + v)(1/3 + v - u) = 2/9 + (v-u)/3·(2) + v/3 + ...
#         = 2/9 + 2(v-u)/3 + v/3
#         = 2/9 + (2v - 2u + v)/3 = 2/9 + (3v - 2u)/3
#   => 3v - 2u < 3 eps
# X_2 X_3 = (1/3 + v - u)(2/3 + 3v - 4u) = 2/9 + (3v-4u)/3 + 2(v-u)/3 + (v-u)(3v-4u)
#         = 2/9 + (3v - 4u + 2v - 2u)/3 = 2/9 + (5v - 6u)/3
#   => 5v - 6u < 3 eps
# X_3 X_4 = (2/3 + 3v - 4u)(1/3 + 2v - 3u) = 2/9 + (2v-3u)·(2/3) + (3v-4u)/3 + ...
#         = 2/9 + (4v - 6u)/3 + (3v - 4u)/3 = 2/9 + (7v - 10u)/3
#   => 7v - 10u < 3 eps
# Floors:
# k_0 = 1 at (1/3, 2/3): f = (1+1/3)/(2/3) = 2. So k=1 iff f < 2 iff (1+X_0) < 2 X_1
#   1 + 1/3 + u < 2(2/3 + v) = 4/3 + 2v
#   u < 2v.
# k_1 = 4 at (X_1, X_2) near (2/3, 1/3): f = (1+2/3)/(1/3) = 5.  k=4 iff f<5 iff (1+X_1) < 5 X_2.
#   1 + 2/3 + v < 5(1/3 + v - u) = 5/3 + 5v - 5u
#   v < 4v - 5u
#   5u < 3v.
# k_2 = 1 at (X_2, X_3) near (1/3, 2/3): f = (1+1/3)/(2/3) = 2. k=1 iff (1+X_2) < 2 X_3.
#   1 + 1/3 + v - u < 2(2/3 + 3v - 4u) = 4/3 + 6v - 8u
#   v - u < 6v - 8u
#   7u < 5v.
# Triangle: u + v > 0.

constraints = {
    'E1_tri': (Fraction(-1), Fraction(-1), Fraction(0)),
    'E2_p0':  (Fraction(2),  Fraction(1),  Fraction(3)),     # 2u + v < 3
    'E3_p1':  (Fraction(-2), Fraction(3),  Fraction(3)),     # -2u + 3v < 3
    'E4_p2':  (Fraction(-6), Fraction(5),  Fraction(3)),     # -6u + 5v < 3
    'E5_p3':  (Fraction(-10),Fraction(7),  Fraction(3)),     # -10u + 7v < 3
    'E_k0_1': (Fraction(1),  Fraction(-2), Fraction(0)),     # u - 2v < 0
    'E_k1_4': (Fraction(5),  Fraction(-4), Fraction(0)),     # 5u - 4v < 0 (CORRECTED)
    'E_k2_1': (Fraction(7),  Fraction(-5), Fraction(0)),     # 7u - 5v < 0
}

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
    ok = True
    for n3 in names:
        if n3 in (n1, n2):
            continue
        a, b, c = constraints[n3]
        val = a * u + b * v
        if val > c:
            ok = False
            break
    if ok:
        verts.append((n1, n2, (u, v)))

print("Vertices of P_4'_(1/3,2/3):")
for (n1, n2, pt) in verts:
    print(f"  {n1} ∩ {n2}: ({pt[0]}, {pt[1]}) = ({float(pt[0]):.4f}, {float(pt[1]):.4f})")

unique = sorted(set([p for (_,_,p) in verts]))
cx = sum(p[0] for p in unique)/len(unique)
cy = sum(p[1] for p in unique)/len(unique)
spts = sorted(unique, key=lambda p: math.atan2(float(p[1]-cy), float(p[0]-cx)))
n = len(spts)
two_area = Fraction(0)
for i in range(n):
    x1,y1 = spts[i]
    x2,y2 = spts[(i+1)%n]
    two_area += x1*y2 - x2*y1
print(f"\nArea = {abs(two_area)/2} = {float(abs(two_area)/2):.6f}")
print(f"Expected (matching corner (2/3,1/3)): 27/76 = {27/76:.6f}")
