"""
Derive the observable P = a*b in rotation coordinates on the conserved ellipse
E(a,b) = a^2 - lambda*a*b + b^2, where M = [[0,1],[-1,lambda]] acts as rotation by
theta = -pi/q (lambda = 2 cos(pi/q)).

Goal: express P along the M-orbit as a sinusoid of the rotation phase, so that
"P < 1/lambda^3" is a sub-arc of the ellipse, and measure its angular width.

KEY QUESTION for the uniform (q>=22) confinement: is the SUPER-threshold arc width
Delta_sup(q) bounded BELOW by a uniform positive multiple of theta = pi/q? If so, a
theta-rotation cannot dwell sub-threshold for more than (period - Delta_sup)/theta
steps, but more importantly NO rotation-invariant measure can avoid the super arc.
"""
import mpmath as mp
mp.mp.dps = 60

def lam(q): return 2*mp.cos(mp.pi/q)

# Whitening: E(a,b) = x^T A x, A = [[1,-l/2],[-l/2,1]]. Eigen-decompose to map the
# ellipse to a circle of radius r, parametrized by angle phi, then P = a*b as f(phi).
# M is rotation by theta = pi/q in the whitened circle (sign: -pi/q, irrelevant for width).

def Pof_phi(q, E0, phi):
    """P = a*b as a function of circle-angle phi on energy-E0 ellipse.
    Whitened coords: a = sqrt(E0)*(u), with A = R diag(mu1,mu2) R^T.
    Use direct param: ellipse a^2 - l a b + b^2 = E0. Param by phi via the
    M-rotation eigenbasis. Eigenvalues of A=[[1,-l/2],[-l/2,1]] are 1-l/2, 1+l/2,
    eigenvectors (1,1)/sqrt2 and (1,-1)/sqrt2.
    a = (s + t)/sqrt2, b=(s - t)/sqrt2 ; E0 = (1-l/2)s^2 + (1+l/2) t^2.
    s = sqrt(E0/(1-l/2)) cos phi, t = sqrt(E0/(1+l/2)) sin phi.
    P = a*b = (s^2 - t^2)/2.
    """
    l = lam(q)
    s = mp.sqrt(E0/(1-l/2))*mp.cos(phi)
    t = mp.sqrt(E0/(1+l/2))*mp.sin(phi)
    a = (s+t)/mp.sqrt(2); b=(s-t)/mp.sqrt(2)
    P = a*b
    return a,b,P

# P = (s^2 - t^2)/2 = (E0/2)[ cos^2/(1-l/2) - sin^2/(1+l/2) ]
#   = (E0/2)[ A0 + B0 cos(2phi) ] with
#   A0 = (1/(1-l/2) - 1/(1+l/2))/2 = (l/2)/( (1-l/2)(1+l/2) ) = (l/2)/(1 - l^2/4)
#   B0 = (1/(1-l/2) + 1/(1+l/2))/2 = 1/(1 - l^2/4)
# So P(phi) = (E0/2)/(1-l^2/4) * [ l/2 + cos(2phi) ].  Amplitude > offset since 1 > l/2.
# => P ranges in (E0/2)/(1-l^2/4)*[l/2 -1, l/2 +1].  Min < 0, max > 0.
def P_closed(q,E0,phi):
    l=lam(q)
    D=1-l*l/4
    return (E0/2)/D*(l/2+mp.cos(2*phi))

for q in [22,30,47,60]:
    E0 = mp.mpf(1)
    import random
    maxd=0
    for _ in range(5):
        phi=mp.mpf(random.random())*2*mp.pi
        a,b,P=Pof_phi(q,E0,phi)
        Pc=P_closed(q,E0,phi)
        maxd=max(maxd,abs(P-Pc))
    print(f"q={q}: closed-form vs direct max diff = {mp.nstr(maxd,3)}")
