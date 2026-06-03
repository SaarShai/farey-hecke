#!/usr/bin/env python3
"""
GOAL F (B) — hunt explicit algebraic certificates (general lambda) for the per-branch envelope.

CUSP branch i=q-2:  x_{q-2}=1, x_{q-3}=lam, x_{q-4}=lam^2-1.
   P = a(a+lam b)/lam.  Want  Q := lam^3*a*(a+lam*b) - lam >= 0   (i.e. lam^2 a(a+lam b) >= 1).
   Region (lower constraints):  a>0, a<=1, L:=lam a + (lam^2-1) b > 1 [branch guard L_{q-3}],
                                d:= lam a + b > 1 [domain],  and upper guard a+lam b <=1.
   Generalize q=5's two-case identity. Find multipliers via linear algebra (coeffs poly in lam).

GENERAL branch i (2<=i<=q-2): parameters X3=x_{i-3}, X2=x_{i-2}, X1=x_{i-1}, X0=x_i with
   X1 = lam X2 - X3,  X0 = lam X1 - X2,  det: X1^2 - X0 X2 = 1, X2^2 - X1 X3 = 1.
   P_i = a*(a X0 + b X1)/X1.  Want  Qg := lam^3 a (a X0 + b X1) - X1 >= 0.
   Lower constraints: a>0, a<=1, L1:=a X1 + b X2 > 1 [L_{i-1}], d:= lam a + b >1 [domain].
"""
import sympy as sp

a,b,lam = sp.symbols('a b lam', positive=True)

print("="*70)
print("CUSP branch certificate hunt (general lam)")
print("="*70)
Lq3 = lam*a + (lam**2-1)*b        # L_{q-3} branch guard form
dom = lam*a + b                    # domain L_1
Q = lam**3*a*(a+lam*b) - lam      # >=0 target

# --- Case a >= 1/lam : try Q = A*a*(Lq3-1) + B*(lam*a-1)*(1-a) + C*a*(dom-1) + R, R=SOS? ---
# First, mimic q=5: Q5 had lam^2 a(a+lam b)-1 = lam^2 a (Lq3-1)+(lam a-1)(1-a). For general lam
# check residual:
resid1 = sp.expand(Q - ( lam**3*a*(Lq3-1) + lam*(lam*a-1)*(1-a) ))
print("\n[case a>=1/lam] residual of q5-style guess (should be small if generalizes):")
print("  resid1 =", sp.collect(sp.expand(resid1), [a,b]))

# General solve: Q = A*a*(Lq3-1) + B*(lam*a-1)*(1-a) + C*a*(dom-1)  with A,B,C polynomials in lam.
A,B,C,D = sp.symbols('A B C D')
ansatz = A*a*(Lq3-1) + B*(lam*a-1)*(1-a) + C*a*(dom-1) + D*a**2*(lam-1)  # extra a^2 generator
diff = sp.expand(Q - ansatz)
# collect monomials in a,b
poly = sp.Poly(diff, a, b)
eqs = [sp.Eq(coef,0) for coef in poly.coeffs()]
# match by monomial
mons = poly.monoms(); coefs = poly.coeffs()
print("\n[case a>=1/lam] coefficient eqs (monomial: coeff in A,B,C,D,lam):")
for m,c in zip(mons,coefs):
    print("   a^%d b^%d :"%(m[0],m[1]), sp.simplify(c),"= 0")
sol = sp.solve([c for c in coefs],[A,B,C,D],dict=True)
print("  solve ->", sol)

print("\n" + "="*70)
print("CUSP: try the TWO-case split with the cusp vertex a*=1/lam (q5 used 1/phi and 1/phi^2)")
print("="*70)
# Case a <= 1/lam: Q = A*a*(dom-1) + B*(lam^2 a -1)*(1-lam a) + C*a*(Lq3-1) + D*a^2*(...)
A,B,C,D = sp.symbols('A B C D')
ansatz2 = A*a*(dom-1) + B*(lam**2*a-1)*(1-lam*a) + C*a*(Lq3-1) + D*a**2
diff2 = sp.expand(Q - ansatz2)
poly2 = sp.Poly(diff2,a,b)
sol2 = sp.solve([c for c in poly2.coeffs()],[A,B,C,D],dict=True)
print("  case a<=1/lam solve ->", sol2)

print("\n" + "="*70)
print("Direct: is Q expressible as nonneg combo using a*(Lq3-1), a*(dom-1), (1-a), squares?")
print("="*70)
# Most general degree-2 ansatz with multipliers linear in a (const + a):
m1c,m1a,m2c,m2a,m3c,m3a,s0 = sp.symbols('m1c m1a m2c m2a m3c m3a s0')
mult1 = m1c+m1a*a   # times (Lq3-1)
mult2 = m2c+m2a*a   # times (dom-1)
mult3 = m3c+m3a*a   # times (1-a)
ans = mult1*(Lq3-1)+mult2*(dom-1)+mult3*(1-a)
diff3 = sp.expand(Q-ans)
poly3 = sp.Poly(diff3,a,b)
sol3 = sp.solve([c for c in poly3.coeffs()],[m1c,m1a,m2c,m2a,m3c,m3a],dict=True)
print("  general linear-multiplier solve ->", sol3)
