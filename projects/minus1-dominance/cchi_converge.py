"""Show c_chi(zeros, Tmax) -> analytic formula as Tmax grows: confirms
   c_chi = log(q/pi) + psi((1+a)/2) + 2 Re L'/L(1,chi)  is the EXACT identity."""
import mpmath as mp
mp.mp.dps = 20
def chi4(n):
    n%=4; return {1:1,3:-1}.get(n,0)
def Lval(chi,q,s):
    return sum(chi(r)*mp.zeta(s,mp.mpf(r)/q) for r in range(1,q+1))*mp.power(q,-s)
def Z(chi,q,a,t):
    s=mp.mpc(mp.mpf(1)/2,t)
    return mp.re(mp.power(mp.mpf(q)/mp.pi,(s+a)/2)*mp.gamma((s+a)/2)*Lval(chi,q,s))
def find_zeros(chi,q,Tmax,step=mp.mpf('0.1')):
    a=1;out=[];t=mp.mpf('0.02');p=Z(chi,q,a,t)
    while t<Tmax:
        t2=t+step;c=Z(chi,q,a,t2)
        if p*c<0:
            g=mp.findroot(lambda x:Z(chi,q,a,x),(t+t2)/2)
            if not out or abs(mp.re(g)-out[-1])>1e-3: out.append(mp.re(g))
        p=c;t=t2
    return out
chi,q=chi4,4
LL=mp.re(mp.diff(lambda z:mp.log(Lval(chi,q,z)),mp.mpf(1),h=mp.mpf('1e-8')))
analytic=mp.log(mp.mpf(q)/mp.pi)+mp.digamma(mp.mpf(1))+2*LL
print(f"chi4 analytic formula c_chi = {mp.nstr(analytic,9)}")
prev=None
for Tmax in [60,120,240,400]:
    zs=find_zeros(chi,q,Tmax)
    s=2*sum(1/(mp.mpf(1)/4+g**2) for g in zs)
    tail=2*mp.quad(lambda t:(1/mp.pi)*mp.log(q*t/(2*mp.pi))/(mp.mpf(1)/4+t**2),[Tmax,mp.inf])
    print(f"  Tmax={Tmax:4d}: sum(zeros)={mp.nstr(s,8)}  +tail={mp.nstr(tail,4)}  total={mp.nstr(s+tail,8)}  (analytic-total={mp.nstr(analytic-(s+tail),4)})")
