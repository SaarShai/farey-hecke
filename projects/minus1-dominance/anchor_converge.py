import mpmath as mp
mp.mp.dps = 22
def chi4(n):
    n%=4; return {1:1,3:-1}.get(n,0)
def Lval(chi,q,s):
    return sum(chi(r)*mp.zeta(s,mp.mpf(r)/q) for r in range(1,q+1))*mp.power(q,-s)
def Z(chi,q,t):
    s=mp.mpc(mp.mpf(1)/2,t)
    return mp.re(mp.power(mp.mpf(q)/mp.pi,(s+1)/2)*mp.gamma((s+1)/2)*Lval(chi,q,s))
def find_zeros(chi,q,Tmax,step=mp.mpf('0.08')):
    out=[];t=mp.mpf('0.02');p=Z(chi,q,t)
    while t<Tmax:
        t2=t+step;c=Z(chi,q,t2)
        if p*c<0:
            g=mp.findroot(lambda x:Z(chi,q,x),(t+t2)/2)
            if not out or abs(mp.re(g)-out[-1])>1e-3: out.append(mp.re(g))
        p=c;t=t2
    return out
def delta(chi,q,Tmax):
    zs=find_zeros(chi,q,Tmax)
    amps=[4/mp.sqrt(mp.mpf(1)/4+g**2) for g in zs]
    ctail=2*mp.quad(lambda t:(1/mp.pi)*mp.log(q*t/(2*mp.pi))/(mp.mpf(1)/4+t**2),[Tmax,mp.inf])
    sigma_tail2=8*ctail
    mu=mp.mpf(2)
    def phi(xi):
        v=mp.e**(1j*xi*mu)*mp.e**(-xi**2*sigma_tail2/2)
        for A in amps: v*=mp.besselj(0,A*xi)
        return v
    return float(0.5+mp.quad(lambda xi: mp.im(phi(xi))/xi,[0,140])/mp.pi),len(zs)
for Tmax in [200,400,700]:
    d,n=delta(chi4,4,Tmax)
    print(f"delta(4;3,1) Tmax={Tmax} ({n} zeros) = {d:.5f}   (RS~0.99590)")
