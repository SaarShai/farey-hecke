"""
Compute the published RS density anchor delta(4;3,1) and delta(3;2,1) end-to-end
to validate the whole pipeline. Known values (Rubinstein-Sarnak 1994):
   delta(4;3,1) ~ 0.9959      delta(3;2,1) ~ 0.9990
The race 3-vs-1 mod 4 is governed by the single odd quadratic char chi_4:
   X_3 - X_1 = mu_diff + 2 * Z_{chi4}, where chi4(3)-chi4(1) = -1-1 = -2.
   mu_3 = -1+#sqrt(3 mod 4)= -1+0 = -1; mu_1 = -1+#sqrt(1 mod 4)= -1+2 = +1.
   => mu_diff = mu_3 - mu_1 = -2.
   D = -2 + (chi4(3)-1)*Z = -2 - 2 Z_{chi4}, Z_chi4 = sum_{gamma} cos(theta_g)*2/sqrt(1/4+g^2).
   amplitude per zero gamma>0:  |chi(3)-1| * 2/sqrt(1/4+g^2) = 2 * 2/sqrt(1/4+g^2)=4/sqrt(1/4+g^2).
"""
import mpmath as mp
mp.mp.dps = 25
def chi4(n):
    n%=4; return {1:1,3:-1}.get(n,0)
def chi3(n):
    n%=3; return {1:1,2:-1}.get(n,0)
def Lval(chi,q,s):
    return sum(chi(r)*mp.zeta(s,mp.mpf(r)/q) for r in range(1,q+1))*mp.power(q,-s)
def Z(chi,q,t):
    s=mp.mpc(mp.mpf(1)/2,t)
    return mp.re(mp.power(mp.mpf(q)/mp.pi,(s+1)/2)*mp.gamma((s+1)/2)*Lval(chi,q,s))
def find_zeros(chi,q,Tmax,step=mp.mpf('0.1')):
    out=[];t=mp.mpf('0.02');p=Z(chi,q,t)
    while t<Tmax:
        t2=t+step;c=Z(chi,q,t2)
        if p*c<0:
            g=mp.findroot(lambda x:Z(chi,q,x),(t+t2)/2)
            if not out or abs(mp.re(g)-out[-1])>1e-3: out.append(mp.re(g))
        p=c;t=t2
    return out

def delta_race(chi,q,Tmax=200):
    zs=find_zeros(chi,q,Tmax)
    # amplitudes A_g = |chi(a)-1| * 2/sqrt(1/4+g^2) with |chi(a)-1|=2 (a is the NR, chi(a)=-1)
    amps=[4/mp.sqrt(mp.mpf(1)/4+g**2) for g in zs]
    # tail variance from zeros above Tmax: sum 4^2 * c_tail where c_tail=2*int density/(1/4+t^2)
    ctail=2*mp.quad(lambda t:(1/mp.pi)*mp.log(q*t/(2*mp.pi))/(mp.mpf(1)/4+t**2),[Tmax,mp.inf])
    var_tail=16*ctail   # |chi(a)-1|^2 * c_tail = 4 * 4 * ctail? |chi(a)-1|^2=4, amp^2 sum=4*(4/(..))
    # Actually amp_g^2 = 16/(1/4+g^2); per-cosine variance = amp^2/2 = 8/(1/4+g^2).
    # tail variance = sum_{g>Tmax} 8/(1/4+g^2) = 8 * (2 * int density/(1/4+t^2)) = 8*ctail... 
    sigma_tail2 = 8*ctail
    mu=mp.mpf(-2)
    def phi(xi):
        v=mp.e**(1j*xi*mu)*mp.e**(-xi**2*sigma_tail2/2)
        for A in amps: v*=mp.besselj(0,A*xi)
        return v
    integ=mp.quad(lambda xi: mp.im(phi(xi))/xi,[0,120])
    return float(0.5+integ/mp.pi), len(zs)

d4,n4=delta_race(chi4,4,200)
print(f"delta(4;3,1) computed = {d4:.5f}   (RS published ~ 0.9959)   [{n4} zeros used]")
d3,n3=delta_race(chi3,3,200)
print(f"delta(3;2,1) computed = {d3:.5f}   (RS published ~ 0.9990)   [{n3} zeros used]")
