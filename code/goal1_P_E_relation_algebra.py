import sympy as sp
cn,cn1,l,E0,P=sp.symbols('c_n c_{n+1} lambda E_0 P',real=True)
# Exact identity: E + lambda P = c_n^2 + c_{n+1}^2
E=cn**2+cn1**2-l*cn*cn1
print("Identity check: E + lambda*P - (c_n^2+c_{n+1}^2) =",
      sp.simplify(E + l*(cn*cn1) - (cn**2+cn1**2)))
# So c_n^2+c_{n+1}^2 = E0 + lambda*P. With AM-GM c_n^2+c_{n+1}^2 >= 2|P| (P=cn cn1):
#   E0 + lambda*P >= 2P  =>  E0 >= (2-lambda)P  =>  P <= E0/(2-lambda).   (UPPER bound on P!)
# And c_n^2+c_{n+1}^2 <= ... gives no positive lower bound. Confirms: energy gives P <= E0/(2-l),
# an UPPER bound (max gap-product), not a lower bound.
print("\nFrom c_n^2+c_{n+1}^2 = E0 + lambda*P and AM-GM (c_n^2+c_{n+1}^2 >= 2 c_n c_{n+1}=2P):")
print("   E0 + lambda*P >= 2P  =>  P <= E0/(2-lambda)   [UPPER bound; equality at c_n=c_{n+1}]")
print("   Lower: c_n^2+c_{n+1}^2 has NO upper bound from E alone on positive arc as one coord->0")
print("   => energy gives ONLY an upper bound on P, infimum of P on the level set is 0.")

# Where does 1/lambda^3 come from then? It is the value of P at the SYMMETRIC point of the
# *boundary-tangent / cusp* configuration. Check: the cusp/last-branch fixed structure.
# The classical last-branch map (b,-a+k lam b). Parabolic/cusp fixed point: a=b (=t), k chosen.
# 1/lambda^3 = value where ess-sup is minimized. Let's see if 1/lam^3 = E*/(2-lam) for some
# canonical E*. Solve E*/(2-lam)=1/lam^3 => E* = (2-lam)/lam^3.
lam=sp.symbols('lambda',positive=True)
Estar=(2-lam)/lam**3
print("\nIf 1/lam^3 = E*/(2-lam) (the symmetric-MAX P of a corridor of energy E*),")
print("   then E* = (2-lambda)/lambda^3 =", sp.simplify(Estar))
import math
for q in [5,7,13]:
    L=2*math.cos(math.pi/q)
    print(f"   q={q}: lam={L:.5f}, E*=(2-lam)/lam^3={(2-L)/L**3:.6f}, 1/lam^3={1/L**3:.6f}")
