#!/usr/bin/env python3
"""
GOAL F (B) — certificate hunt for the CLEAN reformulated envelope.
Variables a,v (>0,<=1); params m=x_{i-1}>=lam, c=x_{i-2}>=1, relation E: m^2+c^2-lam m c = 1.
Generators (>=0 on region):
  g1 = a + c v - m         (branch guard L_{i-1}>1)
  g2 = c a + v - m         (domain lam a+b>1)
  g3 = 1 - a               (a<=1)
  g4 = 1 - v               (v<=1)
Targets:
  (A)  av*(1+c)^2 >= m^2                      [min(av)=m^2/(1+c)^2]
  (B)  lam^3 * m >= (1+c)^2                   [uniform Chebyshev ineq, uses E]
  combine -> lam^3 av >= m.
Hunt SOS/positive-combination certificates.
"""
import sympy as sp
a,v,m,c,lam = sp.symbols('a v m c lam', positive=True)
E = m**2 + c**2 - lam*m*c - 1   # = 0

g1 = a + c*v - m
g2 = c*a + v - m
g3 = 1 - a
g4 = 1 - v

print("="*70); print("Identity check: av(1+c)^2 = (a+cv)(ca+v) - c(a-v)^2")
lhs = sp.expand(a*v*(1+c)**2)
rhs = sp.expand((a+c*v)*(c*a+v) - c*(a-v)**2)
print("  diff =", sp.simplify(lhs-rhs))

print("\n"+"="*70); print("(A) av(1+c)^2 - m^2 : positive-combo hunt")
# try: av(1+c)^2 - m^2 = A*g1*g2 + B*g1*g4 + C*g2*g3 + D*g3*g4 + (squares)
A,B,C,D,F,G = sp.symbols('A B C D F G')
targetA = sp.expand(a*v*(1+c)**2 - m**2)
ansatzA = A*g1*g2 + B*g1*g4 + C*g2*g3 + D*g3*g4 + F*g1*g3 + G*g2*g4
diffA = sp.expand(targetA - ansatzA)
polyA = sp.Poly(diffA, a, v)
solA = sp.solve([co for co in polyA.coeffs()], [A,B,C,D,F,G], dict=True)
print("  solve(A,..) ->", solA)

print("\n"+"="*70); print("(B) lam^3 m - (1+c)^2 >= 0  using E (m^2+c^2-lam m c=1)")
# express as combination using E=0 and known positivity; try to write
#  lam^3 m - (1+c)^2 = (poly)*E + nonneg ?   with m,c on the Chebyshev curve.
# Since m,c specific, just verify it reduces. Use m as free, c via... actually m,c both vary.
# Substitute the curve param: m = sin(i*th)/sin th won't help symbolically; instead test
# whether lam^3 m - (1+c)^2 = alpha*(m - lam) + beta*(...) near cusp. Brute: solve for the
# representation  lam^3 m - (1+c)^2 = K1*(lam*m - 1 - c) + K2*(...) ... explore numerically.
import math
def build(q):
    L=2*math.cos(math.pi/q); x={-1:0.,0:1.}
    for i in range(1,q+2): x[i]=L*x[i-1]-x[i-2]
    return L,x
print("  check candidate factorization lam^3 m-(1+c)^2 vs (lam m - (1+c)) and (m-? ):")
for q in [5,6,7,8,9,11,13]:
    L,x=build(q)
    for i in range(2,q-1):
        mm=x[i-1]; cc=x[i-2]
        val=L**3*mm-(1+cc)**2
        # candidate: lam*m-(1+c) and lam*(lam m -(1+c))*(something)
        f1=L*mm-(1+cc)
        # try val = f1 * (lam^2 m + lam(1+c)+? )/? ... numeric ratio
        ratio = val/f1 if abs(f1)>1e-12 else float('nan')
        print(f"   q={q} i={i}: val={val:.5f} f1=lam*m-(1+c)={f1:.5f} val/f1={ratio:.5f}  "
              f"(lam^2 m=?{L*L*mm:.4f}, lam(1+c)={L*(1+cc):.4f})")
