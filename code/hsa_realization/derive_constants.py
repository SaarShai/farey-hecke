import sympy as sp

# Sealed defs:
#   Mmap l (a,b) = (b, -a + l*b)
#   Eform l (a,b) = a^2 - l*a*b + b^2   (conserved by Mmap)
#   Pgen l (a,b)  = a*(a + l*b)/l
# theta with l = 2 cos theta, so cos theta = l/2.
# Claim: along orbit p_k = Mmap^[k] p,  Pgen(p_k) = alpha*E + rho*E*cos(phi - 2 k theta)
#  with alpha, rho depending only on l (E = Eform l p).

a, b, l, th = sp.symbols('a b l theta', real=True)
c = sp.cos(th); s = sp.sin(th)
# l = 2 c

# Whitening: E = x^T A x, A = [[1,-c],[-c,1]] (since E = a^2 - 2c ab + b^2 = a^2 - l a b + b^2). YES l=2c.
A = sp.Matrix([[1, -c],[-c, 1]])
# Cholesky upper LT = [[1,-c],[0,s]], so A = LT^T LT
LT = sp.Matrix([[1, -c],[0, s]])
print("check A = LT^T LT:", sp.simplify(LT.T*LT - A))

# Pgen quadratic form: Pgen = a*(a+l b)/l = (a^2 + l a b)/l = a^2/l + a b.
# with l = 2c:  Q = [[1/l, 1/2],[1/2, 0]]  since x^T Q x = a^2/l + a b. (sym: off-diag 1/2 each)
Q = sp.Matrix([[1/l, sp.Rational(1,2)],[sp.Rational(1,2), 0]])
x = sp.Matrix([a,b])
print("check Pgen form:", sp.simplify((x.T*Q*x)[0] - (a*(a+l*b)/l)))

# In whitened coords u = LT x, |u|^2 = E. Mmap = rotation by -theta in u-coords.
# Pgen = x^T Q x = u^T (LT^{-T} Q LT^{-1}) u =: u^T B u, B symmetric 2x2.
LTinv = LT.inv()
B = sp.simplify(LTinv.T * Q * LTinv)
B = B.subs(l, 2*c)
B = sp.simplify(B)
print("B (whitened Pgen form) =")
sp.pprint(B)

# For u on circle radius sqrt(E): u = sqrt(E)*(cos psi, sin psi).
# u^T B u = E*(B11 cos^2 + 2 B12 cos sin + B22 sin^2)
#         = E*( (B11+B22)/2 + (B11-B22)/2 cos2psi + B12 sin2psi )
B11,B12,B22 = B[0,0], B[0,1], B[1,1]
mean = sp.simplify((B11+B22)/2)
amp  = sp.simplify(sp.sqrt(((B11-B22)/2)**2 + B12**2))
print("alpha (mean coeff) =", sp.simplify(mean))
print("rho   (amp  coeff) =", sp.simplify(amp))

# express in c,s
alpha_cs = sp.simplify(mean)
rho_cs   = sp.simplify(amp)
print("alpha simplified:", sp.simplify(alpha_cs))
print("rho   simplified:", sp.simplify(rho_cs))

# Scout claim: alpha = 1/(4c) + 3c/(4 s^2);  rho = sqrt(8c^2+1)/(4 s^2 c)
alpha_claim = 1/(4*c) + 3*c/(4*s**2)
rho_claim   = sp.sqrt(8*c**2+1)/(4*s**2*c)
print("alpha - claim =", sp.simplify(alpha_cs - alpha_claim))
print("rho^2 - claim^2 =", sp.simplify(rho_cs**2 - rho_claim**2))
