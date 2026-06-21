"""
Seek a CERTIFICATE that  Eform(a,b) >= EfloorQ  on the region R, of the form
   Eform(a,b) - m = lam1*(la+b-1) + lam2*(2lb-1-a) + Q(a,b)
where m = EfloorQ(l), lam1,lam2 >= 0 (KKT multipliers at V, both binding constraints
are 'feasible side >=0' pushing AWAY from V), and Q is a positive-semidefinite quadratic
(Q = Eform itself is PSD; gradient matching at V).

Actually cleaner: Eform is a convex quadratic, V is the constrained minimizer with the
two active constraints g1 = la+b-1 >=0 and g2 = 2lb-1-a >=0 (V has g1=g2=0).
KKT: grad Eform(V) = lam1 grad g1 + lam2 grad g2,  lam1,lam2>=0.
Then for any feasible (a,b): g1>=0,g2>=0 and by convexity
  Eform(a,b) >= Eform(V) + grad Eform(V).((a,b)-V)
             = Eform(V) + lam1 g1 + lam2 g2  >= Eform(V).
So Eform(a,b) >= Eform(V) PROVIDED lam1,lam2>=0. Verify the KKT multipliers are >=0.

grad Eform = (2a - l b, 2b - l a).
grad g1 = (l, 1). grad g2 = (-1, 2l).
Solve (2a-lb, 2b-la) = lam1 (l,1) + lam2 (-1,2l) at V.
"""
import mpmath as mp
mp.mp.dps=50
def lamq(q): return 2*mp.cos(mp.pi/q)
def V(l):
    D=1+2*l**2; return ((2*l-1)/D,(1+l)/D)
def kkt(l):
    a,b=V(l)
    gx=2*a-l*b; gy=2*b-l*a
    # solve [l, -1; 1, 2l] [lam1;lam2] = [gx;gy]
    det=l*2*l-(-1)*1  # =2l^2+1
    lam1=(gx*2*l-(-1)*gy)/det
    lam2=(l*gy-1*gx)/det
    return lam1,lam2,a,b
print("KKT multipliers (need lam1,lam2 >= 0) over q>=5:")
allnn=True
for q in [5,6,7,8,10,15,30,100,1000,10**6]:
    l=lamq(q); lam1,lam2,a,b=kkt(l)
    nn = lam1>=0 and lam2>=0
    allnn = allnn and nn
    print(f"q={q:>8} l={float(l):.6f} lam1={float(lam1):.6e} lam2={float(lam2):.6e} {'OK' if nn else 'NEG!'}")
print("all nonneg q>=5:",allnn)
# closed form of lam1,lam2:
# a=(2l-1)/D, b=(1+l)/D, D=2l^2+1
# gx=2a-lb=(2(2l-1)-l(1+l))/D=(4l-2-l-l^2)/D=(-l^2+3l-2)/D = -(l-1)(l-2)/D = (l-1)(2-l)/D >0
# gy=2b-la=(2(1+l)-l(2l-1))/D=(2+2l-2l^2+l)/D=(-2l^2+3l+2)/D = (2-l)(... )? factor: -2l^2+3l+2 = -(2l^2-3l-2)=-(2l+1)(l-2)=(2l+1)(2-l)>0
print("\ncheck gx,gy closed forms:")
for q in [5,10,100]:
    l=lamq(q); a,b=V(l); D=2*l**2+1
    gx=2*a-l*b; gy=2*b-l*a
    print(q, float(gx-(l-1)*(2-l)/D), float(gy-(2*l+1)*(2-l)/D))
# lam1 = (gx*2l+gy)/det ; lam2=(l gy - gx)/det ; det=2l^2+1=D
print("\nlam closed forms (det=D=2l^2+1):")
for q in [5,10,100]:
    l=lamq(q); D=2*l**2+1
    gx=(l-1)*(2-l)/D; gy=(2*l+1)*(2-l)/D
    lam1=(gx*2*l+gy)/D; lam2=(l*gy-gx)/D
    # numerator lam1*D^2 = (l-1)(2-l)2l + (2l+1)(2-l) = (2-l)[2l(l-1)+(2l+1)] = (2-l)(2l^2-2l+2l+1)=(2-l)(2l^2+1)=(2-l)D
    # => lam1 = (2-l)D/D^2 = (2-l)/D
    # lam2*D^2 = l(2l+1)(2-l) - (l-1)(2-l) = (2-l)[l(2l+1)-(l-1)]=(2-l)(2l^2+l-l+1)=(2-l)(2l^2+1)=(2-l)D
    # => lam2 = (2-l)/D
    print(q, 'lam1=',float(lam1),'(2-l)/D=',float((2-l)/D),'lam2=',float(lam2))
print("\n=> lam1 = lam2 = (2-l)/(2l^2+1) > 0 for l<2. CLEAN KKT certificate.")
