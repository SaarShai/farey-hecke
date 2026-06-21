import sympy as sp
a,b,l,th = sp.symbols('a b l theta', real=True)
c=sp.cos(th)
# substitute l = 2c at the end
def Mmap(p): a,b=p; return (b,-a+l*b)
def Pgen(p): a,b=p; return a*(a+l*b)/l
def Eform(p): a,b=p; return a*a-l*a*b+b*b

p0=(a,b); p1=Mmap(p0); p2=Mmap(p1)
P0=Pgen(p0); P1=Pgen(p1); P2=Pgen(p2)
E=Eform(p0)
# alpha from B-form with l=2c:  alpha = 1/(4c)+3c/(4 s^2), but express in l:
# c=l/2, s^2=1-l^2/4=(4-l^2)/4
alpha_l = sp.Rational(1,2)/l + 3*(l/2)/( (4-l**2) )  # = 1/(4c)+3c/(4 s^2) with c=l/2, s^2=(4-l^2)/4
alpha_l = sp.simplify(alpha_l)
print("alpha(l) =", alpha_l)   # expect 1/(2l) + 3l/(2(4-l^2))
C0 = alpha_l*E
# recurrence: h(k+1)+h(k-1) = 2cos(2theta) h(k), with cos(2theta)=2c^2-1 = l^2/2 -1
cos2 = l**2/2 - 1
h0=P0-C0; h1=P1-C0; h2=P2-C0
recur = sp.simplify(h2 + h0 - 2*cos2*h1)
print("recurrence residual h2+h0-2cos2*h1 =", recur)
# Also check amplitude: h0^2 - 2 cos2 h0 h1 + h1^2 = R^2 sin^2(2theta)? i.e. invariant
amp_inv = sp.simplify(h0**2 - 2*cos2*h0*h1 + h1**2)
print("amp invariant h0^2-2cos2 h0 h1+h1^2 =", sp.simplify(amp_inv))
# this should equal R^2 * sin^2(2theta) = (rho E)^2 (1-cos2^2)
rho_l = sp.sqrt(8*(l/2)**2+1)/(4*((4-l**2)/4)*(l/2))  # sqrt(8c^2+1)/(4 s^2 c)
rho_l = sp.simplify(rho_l)
print("rho(l) =", rho_l)
sin2sq = 1-cos2**2
print("R^2 sin2^2 - amp_inv =", sp.simplify((rho_l*E)**2*sin2sq - amp_inv))
