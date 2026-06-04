"""
D3 — exact closed form of C_FF(q).  DERIVE-THEN-VERIFY.

Derivation (analytic, by hand; this script VERIFIES it):

  S_D = (q/(q-1)) * sum_{0<=j1,j2<=D} B(j1,j2) M_A(D-j1) M_A(D-j2)
  where (Euler product over irreducibles of F_q[t]):
     sum B(j1,j2) x^{j1} y^{j2} = (1 - xy/q)/((1-x)(1-y)(1-qxy))
  => B(j1,j2) depends only on M=min(j1,j2):
     b(M) = (q+1) q^{M-1} - 1/q              [b(0)=1]
  M_A(D-j) = 1 (j=D), 1-q (0<=j<D), 0 (j>D).
  Phi_D = (q^{2D+1}+1)/(q+1)   (exact).
  R_D = (q^2-1) q^D S_D / (q^{2D+1}+1).

  W(D)=b(D);  V(D)=sum_{j=0}^D b(j);  U(D)=sum_{M=0}^D (2(D-M)+1) b(M).
  S_D = (q/(q-1)) [ (q-1)^2 U(D) - 2q(q-1) V(D) + q^2 W(D) ].

  Leading q^D coeffs: W~(q+1)/q, V~(q+1)/(q-1), U~(q+1)^2/(q-1)^2
  => S_D ~ [q(q+1)/(q-1)] q^D  => C_FF(q) = (q^2-1)/q * q(q+1)/(q-1) = (q+1)^2.

VERIFY:
 (1) closed-form R_D (from b(M)) must EQUAL the Q6 exact fractions for q=2,
     D=1..6: 127/64, 2037/704, 11733/2752, 20423/3648, 292181/43712,
     1307989/174784  (independent earlier exact enumeration).
 (2) symbolic limit_{D->inf} R_D == (q+1)^2 for symbolic q (sympy).
 (3) numeric R_D -> (q+1)^2 for q=2,3,5,7 at large D (exact Fraction).
"""
from fractions import Fraction
import sympy as sp

def b(M, q):
    # b(M) = (q+1) q^{M-1} - 1/q   (exact); use Fraction for numeric q
    return (q+1)*Fraction(q)**(M-1) - Fraction(1, q)

def W(D, q): return b(D, q)
def V(D, q): return sum((b(j, q) for j in range(0, D+1)), Fraction(0))
def U(D, q): return sum(((2*(D-M)+1)*b(M, q) for M in range(0, D+1)), Fraction(0))

def S_D(D, q):
    q=Fraction(q)
    return (q/(q-1))*((q-1)**2*U(D,q) - 2*q*(q-1)*V(D,q) + q**2*W(D,q))

def Phi_D(D, q):
    q=Fraction(q)
    return (q**(2*D+1)+1)/(q+1)

def R_D(D, q):
    q=Fraction(q)
    return (q**2-1)*q**D*S_D(D,q)/(q**(2*D+1)+1)

# ---- (1) verify closed form vs Q6 exact fractions (q=2) ----
Q6_q2 = {1:Fraction(127,64),2:Fraction(2037,704),3:Fraction(11733,2752),
         4:Fraction(20423,3648),5:Fraction(292181,43712),6:Fraction(1307989,174784)}
print("="*78)
print("(1) closed-form R_D  vs  Q6 independent exact enumeration (q=2):")
ok1=True
for D in range(1,7):
    r=R_D(D,2); match=(r==Q6_q2[D])
    ok1&=match
    print(f"   D={D}: closed={r}  Q6={Q6_q2[D]}  {'MATCH' if match else 'MISMATCH'}")
print(f"   => closed form {'VERIFIED against independent enumeration' if ok1 else 'FAILS'}")

# also q=3 spot check vs Q6 (R_1=2666/567, R_2=42950/4941)
print("   q=3 spot: R_1 closed=",R_D(1,3)," Q6=2666/567 ;",
      "R_2 closed=",R_D(2,3)," Q6=42950/4941")
print("   match:", R_D(1,3)==Fraction(2666,567) and R_D(2,3)==Fraction(42950,4941))

# ---- (2) symbolic limit ----
print("="*78)
q,D = sp.symbols('q D', positive=True)
qq=sp.Symbol('q', positive=True)
def bsym(M): return (qq+1)*qq**(M-1)-sp.Rational(1,1)/qq
Ds=sp.Symbol('D', positive=True, integer=True)
# closed sums (symbolic in Ds)
Ws=(qq+1)*qq**(Ds-1)-1/qq
Vs=sp.summation((qq+1)*qq**(sp.Symbol('j',integer=True)-1)-1/qq, (sp.Symbol('j',integer=True),0,Ds))
M=sp.Symbol('M',integer=True)
Us=sp.summation((2*(Ds-M)+1)*((qq+1)*qq**(M-1)-1/qq),(M,0,Ds))
Ss=sp.simplify((qq/(qq-1))*((qq-1)**2*Us-2*qq*(qq-1)*Vs+qq**2*Ws))
Rs=sp.simplify((qq**2-1)*qq**Ds*Ss/(qq**(2*Ds+1)+1))
lim=sp.limit(Rs, Ds, sp.oo)
print("(2) symbolic  lim_{D->inf} R_D =", sp.simplify(lim), "   [(q+1)^2 =", sp.expand((qq+1)**2),"]")
print("    equals (q+1)^2 ?", sp.simplify(lim-(qq+1)**2)==0)

# ---- (3) numeric large-D ----
print("="*78)
print("(3) numeric R_D at large D vs (q+1)^2 :")
for qv in (2,3,5,7):
    for Dv in (20,40):
        rv=R_D(Dv,qv)
        print(f"   q={qv} D={Dv}: R_D={float(rv):.10f}  (q+1)^2={ (qv+1)**2 }  "
              f"diff={float(rv-(qv+1)**2):.3e}")
print("="*78)
print("CONCLUSION: if (1) MATCH and (2) ==(q+1)^2 and (3) -> (q+1)^2,")
print("then  C_FF(q) = (q+1)^2  is PROVEN (derived) and VERIFIED")
print("(closed form reproduces independent exact enumeration; exact symbolic limit).")
print("="*78)
