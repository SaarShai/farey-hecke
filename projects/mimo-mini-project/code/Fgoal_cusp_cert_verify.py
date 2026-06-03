#!/usr/bin/env python3
"""
Verify the GENERAL-lambda cusp-branch envelope certificate (i=q-2, holds for ALL q>=5).
Cusp branch: x_{q-2}=1, x_{q-3}=lam, x_{q-4}=lam^2-1.
P = a(a+lam b)/lam.  Goal: lam^2 a(a+lam b) >= 1, i.e. Q:=lam^3 a(a+lam b)-lam >= 0.
Guards: G = lam a + (lam^2-1) b - 1 > 0  [L_{q-3}>1];  d = lam a + b - 1 > 0 [domain];
        a<=1, a>0;  upper guard U = 1 - (a+lam b) >=0 [L_{q-2}<=1].
Two-case split at a=1/lam.
"""
import sympy as sp
a,b,lam = sp.symbols('a b lam', positive=True)
G = lam*a + (lam**2-1)*b - 1
d = lam*a + b - 1
Q = lam**3*a*(a+lam*b) - lam

print("CASE a>=1/lam: Q = A*a*G + lam*(lam a-1)*(1-a) + C*a*d, A,C>=0 ?")
A = lam*(lam**3-lam-1)/(lam**2-2)
C = lam*(lam**2-lam-1)/(lam**2-2)
cert1 = A*a*G + lam*(lam*a-1)*(1-a) + C*a*d
print("  identity residual Q-cert1 =", sp.simplify(sp.expand(Q-cert1)))
# A,C signs for lam in [phi,2): lam^2-2>0; lam^3-lam-1>0; lam^2-lam-1>=0
for L in [1.6180,1.7320,1.9,1.99]:
    print(f"   lam={L}: A={float(A.subs(lam,L)):.4f}>=0, C={float(C.subs(lam,L)):.4f}>=0, lam^2-2={L*L-2:.4f}")

print("\nCASE a<=1/lam: need lam^2 a >=1 first (from upper guard U & domain), then")
print("  Q = A2*a*d + lam*(lam^2 a-1)*(1-lam a) + C2*a*G ?")
A2 = lam*(lam**4-lam**2-lam)/(lam**2-2)   # guess scaled
C2 = lam*(lam**3-lam**2-lam)/(lam**2-2)
cert2 = A2*a*d + lam*(lam**2*a-1)*(1-lam*a) + C2*a*G
print("  identity residual Q-cert2 =", sp.simplify(sp.expand(Q-cert2)))
# derive lam^2 a>=1 from U>=0 and d>=0 ?  U: a+lam b<=1 ; d: lam a+b>=1.
# from d: b>=1-lam a; sub into U: a+lam(1-lam a)<=a+lam b<=1 => a+lam-lam^2 a<=1 => a(1-lam^2)<=1-lam
#   => a(lam^2-1)>=lam-1 => a(lam-1)(lam+1)>=(lam-1) => a(lam+1)>=1 => a>=1/(lam+1).
# Hmm that gives a>=1/(lam+1), not lam^2 a>=1. Check if a>=1/(lam+1) enough with case a<=1/lam.
print("\n  Derive a>=1/(lam+1) from U,d:  (then lam^2 a >= lam^2/(lam+1); is that >=1? need lam^2>=lam+1 i.e lam>=phi)")
for L in [1.6180,1.7320,1.99]:
    print(f"   lam={L}: lam^2/(lam+1)={L*L/(L+1):.4f} (>=1 iff lam>=phi)")
print("  => for lam>=phi: a>=1/(lam+1) => lam^2 a>=lam^2/(lam+1)>=1. GOOD. (uses upper guard U + domain d + lam>=phi)")

# Final sanity: numeric check Q>=0 on cusp-branch region for several lam (incl >2-ish? no, lam<2)
import random, math
print("\nNumeric sanity Q>=0 on cusp-branch region:")
bad=0
for q in [5,6,8,12,20,40]:
    L=2*math.cos(math.pi/q)
    for _ in range(200000):
        aa=random.uniform(1e-4,1.0)
        bb=random.uniform(-1, 1.0)
        if L*aa+(L*L-1)*bb-1>0 and L*aa+bb-1>0 and aa<=1 and (aa+L*bb)<=1:
            if L**3*aa*(aa+L*bb)-L < -1e-9: bad+=1
print("  violations:", bad)
