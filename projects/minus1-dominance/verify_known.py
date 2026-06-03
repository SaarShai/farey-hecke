"""
Cross-check c_chi (Method B) against KNOWN literature.

The cleanest published anchor: Rubinstein-Sarnak give delta(q;N,R) densities.
For q=4: delta(4;3,1) ~ 0.9959; q=3: delta(3;2,1) ~ 0.9990.
These come from the SINGLE quadratic char mod q (the only nonprincipal char),
so the race 3-vs-1 (resp 2-vs-1) is governed entirely by that one chi.

Also: Fiorilli-Martin (J. reine angew. Math 676 (2013)) and Rubinstein-Sarnak
tabulate the variance V(q) = sum over chi of c_chi style constants. We verify
our c_chi against the value of the first few zeros of L(s,chi_4) and L(s,chi_3),
whose imaginary parts are classically known:
   L(s,chi_4) (the char mod 4, = the Dirichlet beta function): first zeros
     gamma = 6.0209..., 10.2437..., 12.9880..., 16.343..., ...
   L(s,chi_3): first zero gamma = 8.0397..., 11.249..., ...
"""
import mpmath as mp
mp.mp.dps = 40
import math

# chi_4: the nonprincipal char mod 4: chi(1)=1, chi(3)=-1, else 0. = Dirichlet beta.
def chi4(n):
    n%=4
    return {1:1,3:-1}.get(n,0)
# chi_3: nonprincipal char mod 3: chi(1)=1, chi(2)=-1.
def chi3(n):
    n%=3
    return {1:1,2:-1}.get(n,0)

def L_value(chi,q,s):
    return sum(chi(r)*mp.zeta(s,mp.mpf(r)/q) for r in range(1,q+1))*mp.power(q,-s)

# beta function check: L(s,chi4)=Dirichlet beta(s); beta(1)=pi/4. Evaluate near 1.
print("L(1+e,chi4)~pi/4 =",mp.nstr(mp.pi/4,12),"  got",mp.nstr(L_value(chi4,4,1+mp.mpf('1e-20')),12))
print("L(1+e,chi3)~pi/(3 sqrt3)=",mp.nstr(mp.pi/(3*mp.sqrt(3)),12),"  got",mp.nstr(L_value(chi3,3,1+mp.mpf('1e-20')),12))

# find first zeros on critical line for chi4 (Dirichlet beta zeros) to check sqrt(1/4+g^2)
def Zrot(chi,q,even,t):
    a=0 if even else 1
    s=mp.mpc(0.5,t)
    Lam=mp.power(mp.mpf(q)/mp.pi,(s+a)/2)*mp.gamma((s+a)/2)*L_value(chi,q,s)
    gp=mp.power(mp.mpf(q)/mp.pi,(s+a)/2)*mp.gamma((s+a)/2)
    return mp.re(Lam/gp*abs(gp))

def zeros(chi,q,even,Tmax,step=mp.mpf('0.1')):
    out=[];t=mp.mpf('0.01');p=Zrot(chi,q,even,t)
    while t<Tmax:
        t2=t+step;c=Zrot(chi,q,even,t2)
        if p*c<0:
            g=mp.findroot(lambda x:Zrot(chi,q,even,x),(t+t2)/2);out.append(mp.re(g))
        p=c;t=t2
    return out

z4=zeros(chi4,4,False,40)   # chi4 is ODD
z3=zeros(chi3,3,False,40)   # chi3 is ODD
print("chi4 first zeros (expect ~6.0209,10.2437,12.988):",[mp.nstr(g,7) for g in z4[:4]])
print("chi3 first zeros (expect ~8.0397,11.249,15.70):",[mp.nstr(g,7) for g in z3[:4]])

def c_chi_zeros(zs,Tmax):
    s=sum(1/(mp.mpf(1)/4+g**2) for g in zs)*2  # +- pairs
    tail=2*mp.quad(lambda t:(1/mp.pi)*mp.log(4*t/(2*mp.pi))/t**2,[Tmax,mp.inf])
    return s,tail
c4,t4=c_chi_zeros(z4,40); c3,t3=c_chi_zeros(z3,40)
print(f"c_chi4 (zeros, |g|<40) = {mp.nstr(c4,9)}  +tail~{mp.nstr(t4,3)} => {mp.nstr(c4+t4,9)}")
print(f"c_chi3 (zeros, |g|<40) = {mp.nstr(c3,9)}  +tail~{mp.nstr(t3,3)} => {mp.nstr(c3+t3,9)}")

# Method B analytic:
def LpoverL(chi,q,s): return mp.diff(lambda z:mp.log(L_value(chi,q,z)),s,h=mp.mpf('1e-12'))
def c_chi_B(chi,q,even):
    a=0 if even else 1
    s1=mp.mpf(1)+mp.mpf('1e-18')
    return mp.re(mp.log(mp.mpf(q)/mp.pi)+mp.digamma((1+a)/mp.mpf(2))+2*mp.re(LpoverL(chi,q,s1)))
print(f"c_chi4 (Method B analytic) = {mp.nstr(c_chi_B(chi4,4,False),9)}")
print(f"c_chi3 (Method B analytic) = {mp.nstr(c_chi_B(chi3,3,False),9)}")
