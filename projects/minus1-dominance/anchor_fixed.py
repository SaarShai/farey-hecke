"""
Fix the sign convention. The Chebyshev bias: among the NON-residue a and the
residue 1, the NON-RESIDUE leads (pi(x;q,a)>pi(x;q,1) most of the time). The
mean of E_a=-1+#sqrt(a) is SMALLER for the NR (since #sqrt smaller), yet the NR
LEADS in raw pi-count. Reason: E_a normalizes phi(q)pi(x;q,a)-pi(x), and the
constant -1+#sqrt(a) is the contribution of PRIME SQUARES (p^2=a counted in psi
but they LOWER the pi-count race). The race delta(q;a,1)=density{pi(x;q,a)>pi(x;q,1)}.

The correct statement (Rubinstein-Sarnak): delta(q;a,1) = P(X_a > X_1) where
E[X_a] = -1+#sqrt(a)... but the EMPIRICAL bias has NR ahead, so delta(q;NR,1)>1/2.
The resolution is the SIGN of the indicator vs the X-difference. RS define
E(x;q,a) so that delta(q;a,b)=P(E_a-E_b>0) AND for a NR vs 1 this is >1/2. So the
sign such that NR wins must make mu(NR)-mu(1) > 0 in the X-convention. Concretely:
the count-bias variable is D = X_a - X_1 with mean = -(mu_a - mu_1)=#sqrt(1)-#sqrt(a)
i.e. mean = +2 for a NR, b=1 (q=4). So delta(4;3,1)=P(D>0) with MEAN +2.
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

def delta_NR_vs_1(chi,q,sqrt_count_1,Tmax=200):
    zs=find_zeros(chi,q,Tmax)
    amps=[4/mp.sqrt(mp.mpf(1)/4+g**2) for g in zs]  # |chi(a)-1|=2, *2/|rho|
    ctail=2*mp.quad(lambda t:(1/mp.pi)*mp.log(q*t/(2*mp.pi))/(mp.mpf(1)/4+t**2),[Tmax,mp.inf])
    sigma_tail2=8*ctail
    mu=mp.mpf(sqrt_count_1)   # mean = #sqrt(1)-#sqrt(a) = #sqrt(1)-0 = +sqrt_count_1
    def phi(xi):
        v=mp.e**(1j*xi*mu)*mp.e**(-xi**2*sigma_tail2/2)
        for A in amps: v*=mp.besselj(0,A*xi)
        return v
    integ=mp.quad(lambda xi: mp.im(phi(xi))/xi,[0,120])
    return float(0.5+integ/mp.pi),len(zs)

# q=4: #sqrt(1 mod 4)=#{1,3}=2 (1^2=1,3^2=1). So mean=+2.
d4,n4=delta_NR_vs_1(chi4,4,2,200)
print(f"delta(4;3,1) = {d4:.5f}   (RS ~ 0.9959)   [{n4} zeros]")
# q=3: #sqrt(1 mod 3)=#{1,2}? 2^2=4=1 mod3, 1^2=1 => 2 roots. mean=+2.
d3,n3=delta_NR_vs_1(chi3,3,2,200)
print(f"delta(3;2,1) = {d3:.5f}   (RS ~ 0.9990)   [{n3} zeros]")
