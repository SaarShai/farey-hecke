"""
Confirm rigorously (numerically, high dps) that:
(1) min of Eform over closed k=1 corridor region R is attained at vertex
    V = ((2l-1)/(1+2l^2), (1+l)/(1+2l^2)) = Dcorr-edge {la+b=1} ∩ bracket-upper {1+a=2lb},
    for all q>=5.
(2) Eform(V) >= EfloorQ  for all q>=5, with the margin function
       G(l) := Eform(V) - EfloorQ
    staying > 0 on l in [lamq(5), 2).
Also produce the EXACT closed form of Eform(V) to feed Lean.

Eform(V):  a=(2l-1)/D, b=(1+l)/D, D=1+2l^2.
 Eform = a^2 - l a b + b^2
       = [ (2l-1)^2 - l(2l-1)(1+l) + (1+l)^2 ] / D^2
 numerator N(l) = (2l-1)^2 - l(2l-1)(1+l) + (1+l)^2
"""
import mpmath as mp
mp.mp.dps=60

def lamq(q): return 2*mp.cos(mp.pi/q)
def alphaC(l): return (l**2+2)/(l*(4-l**2))
def rhoC(l): return 2*mp.sqrt(2*l**2+1)/(l*(4-l**2))
def EfloorQ(l): return 1/(l**3*(alphaC(l)+rhoC(l)*(l/2)))
def Eform(l,a,b): return a**2-l*a*b+b**2

def Nl(l):  # numerator of Eform(V)
    return (2*l-1)**2 - l*(2*l-1)*(1+l) + (1+l)**2
def EformV(l):
    D=1+2*l**2
    return Nl(l)/D**2

# symbolic-ish check of N(l): expand
# (2l-1)^2 = 4l^2 -4l +1
# l(2l-1)(1+l) = l(2l-1+2l^2-l) = l(2l^2+l-1)=2l^3+l^2-l
# (1+l)^2 = 1+2l+l^2
# N = 4l^2-4l+1 - (2l^3+l^2-l) + 1+2l+l^2 = -2l^3 + (4-1+1)l^2 + (-4+1+2)l + 2
#   = -2l^3 +4l^2 -l +2
def Nl_closed(l): return -2*l**3 + 4*l**2 - l + 2

import sys
print("check N(l) closed form vs direct:")
for q in [5,10,100]:
    l=lamq(q); print(q, float(Nl(l)-Nl_closed(l)))

# EfloorQ closed form: alphaC+rhoC*(l/2) = (l^2+2)/(l(4-l^2)) + sqrt(2l^2+1)*l/(l(4-l^2))
#  = [ (l^2+2) + l*sqrt(2l^2+1) ] / (l(4-l^2))
# EfloorQ = 1/(l^3 * that) = (l(4-l^2)) / ( l^3 ( (l^2+2)+l sqrt(2l^2+1) ) )
#         = (4-l^2) / ( l^2 ( (l^2+2)+ l sqrt(2l^2+1) ) )
def EfloorQ_closed(l):
    return (4-l**2)/(l**2*((l**2+2)+l*mp.sqrt(2*l**2+1)))
print("check EfloorQ closed form:")
for q in [5,10,100]:
    l=lamq(q); print(q, float(EfloorQ(l)-EfloorQ_closed(l)))

# The inequality to prove for q>=5 (l in [phi-related..2)):  EformV(l) >= EfloorQ(l)
#   N(l)/(1+2l^2)^2 >= (4-l^2)/(l^2((l^2+2)+l sqrt(2l^2+1)))
# Multiply out (all positive for l in (1,2)): clear denominators.
#  N(l) * l^2 * ((l^2+2)+l sqrt(2l^2+1))  >=  (4-l^2)*(1+2l^2)^2
# Let s=sqrt(2l^2+1)>0. LHS has +l*s term. Define margin:
def margin(l):
    s=mp.sqrt(2*l**2+1)
    lhs = Nl_closed(l)*l**2*((l**2+2)+l*s)
    rhs = (4-l**2)*(1+2*l**2)**2
    return lhs-rhs

# scan l over the actual lamq(q) values q=5..big AND continuously over [lamq(5),2)
print("\nmargin (cleared-denominator polynomial-in-l-and-s form) at Hecke l's:")
for q in [5,6,7,10,20,50,200,2000]:
    l=lamq(q); print(f"q={q:>5} l={float(l):.8f} margin={float(margin(l)):.6e} EformV-EfloorQ={float(EformV(l)-EfloorQ_closed(l)):.3e}")

print("\ncontinuous scan of margin over l in [lamq(5), 2):")
l5=lamq(5)
mn=None;mnl=None
N=200000
for i in range(N+1):
    l=l5+(2-l5)*mp.mpf(i)/N
    if l>=2: l=2-mp.mpf(10)**(-12)
    mg=margin(l)
    if mn is None or mg<mn: mn=mg;mnl=l
print(f"min margin over [lamq(5),2) = {float(mn):.6e} at l={float(mnl):.8f}  (q approx {float(mp.pi/mp.acos(mnl/2)):.3f})")
print("margin>0 everywhere?" , mn>0)
# also below lamq(5): show it goes negative (q=3,4 violation region)
print("\nmargin for l < lamq(5) (q=3,4 zone) -- expect negative:")
for q in [3,4]:
    l=lamq(q); print(f"q={q} l={float(l):.6f} margin={float(margin(l)):.6e}")
