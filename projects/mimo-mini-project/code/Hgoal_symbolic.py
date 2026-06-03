#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GOAL H — SYMBOLIC core of the rotation mechanism (exact, q-independent in lam).

Branch matrices (using boundary Chebyshev values, valid ALL q>=5):
  x_{q-1}=0, x_{q-2}=1, x_{q-3}=lam, x_{q-4}=lam^2-1.
  M_{q-1,k} = [[0,1],[-1,k*lam]]            (scalar branch)
  M_{q-3,0} = [[lam, lam^2-1],[1, lam]]     (branch q-3)
  Cusp word M_{q-2,0} = [[1,lam],[0,1]]     (parabolic, realizes 1/lam^3)

Claims (exact symbolic):
 (1) W_q = (q-1,3)(q-1,0)(q-3,0) monodromy M has det 1 and trace = lam  => ELLIPTIC, conjugate
     to the fundamental rotation R=[[lam,-1],[1,0]] (trace lam, rotation by pi/q).
 (2) The companion R has trace lam too. So both scalar rotation AND the multi-branch sustained
     word are the SAME rotation by pi/q.  Cusp word: trace 2 (parabolic) -- the unique extremal.
 (3) Invariant ellipse of M and product-on-ellipse extremes.
 (4) Generic family W_q(k1) = (q-1,k1)(q-1,0)(q-3,0): trace as a function of k1 -- which k1 give
     |trace|<2 (elliptic, sustainable runs)?
"""
import sympy as sp

lam = sp.symbols('lam', positive=True)

Mqm1 = lambda k: sp.Matrix([[0,1],[-1,k*lam]])
Mqm3 = sp.Matrix([[lam, lam**2-1],[1, lam]])
Mcusp = sp.Matrix([[1,lam],[0,1]])
R = sp.Matrix([[lam,-1],[1,0]])

print("=== (1) W_q = (q-1,3)(q-1,0)(q-3,0) monodromy ===")
# word order: first apply (q-1,3), then (q-1,0), then (q-3,0): M = M_{q-3,0} M_{q-1,0} M_{q-1,3}
M = Mqm3 * Mqm1(0) * Mqm1(3)
M = sp.simplify(M)
print("  M =", M.tolist())
print("  det(M) =", sp.simplify(M.det()), "  trace(M) =", sp.simplify(M.trace()))

print("\n=== (2) fundamental rotation R and cusp word ===")
print("  trace(R) =", sp.simplify(R.trace()), " det(R)=", sp.simplify(R.det()))
print("  trace(cusp word M_{q-2,0}) =", sp.simplify(Mcusp.trace()), " (parabolic if 2)")

print("\n=== (3) invariant ellipse Q'(a,b) of M and product extremes ===")
# invariant form of [[p,q],[r,s]] is proportional to r a^2 + (s-p) ab - q b^2
p,qq,r,s = M[0,0],M[0,1],M[1,0],M[1,1]
Qp = sp.expand(r*sp.Symbol('a')**2 + (s-p)*sp.Symbol('a')*sp.Symbol('b') - qq*sp.Symbol('b')**2)
print("  invariant form r a^2+(s-p)ab-q b^2 =", Qp)
# check M^T Qmat M = Qmat (up to sign)
a,b = sp.symbols('a b')
Qmat = sp.Matrix([[r, (s-p)/2],[(s-p)/2, -qq]])
chk = sp.simplify(M.T*Qmat*M - Qmat)
print("  M^T Qmat M - Qmat =", chk.tolist(), " (zero => M preserves this ellipse)")

print("\n=== (4) family (q-1,k1)(q-1,0)(q-3,0): trace vs k1 (elliptic iff |trace|<2) ===")
k1 = sp.symbols('k1')
Mf = sp.simplify(Mqm3 * Mqm1(0) * Mqm1(k1))
trf = sp.simplify(Mf.trace())
print("  trace(k1) =", trf)
for kv in range(0,6):
    tv = trf.subs(k1,kv)
    # numeric at q=20 (lam=2cos(pi/20))
    import math
    lv = 2*math.cos(math.pi/20)
    print(f"    k1={kv}: trace={sp.simplify(tv)}  numeric@q=20={float(tv.subs(lam,lv)):.5f} "
          f"({'elliptic' if abs(float(tv.subs(lam,lv)))<2 else 'hyperbolic'})")

print("\n=== (5) two-step variants: which short words are elliptic (trace lam-like)? ===")
# (q-1,k)(q-3,0)
for kv in range(0,5):
    Mt = sp.simplify(Mqm3*Mqm1(kv))
    print(f"  (q-1,{kv})(q-3,0): trace={sp.simplify(Mt.trace())}")
# pure scalar rotation (q-1,1) is R-like? (q-1,1)=[[0,1],[-1,lam]] trace lam
print(f"  (q-1,1) alone: trace={sp.simplify(Mqm1(1).trace())}  (=lam => the scalar rotation R-conj)")
