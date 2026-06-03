import mpmath as mp
mp.mp.dps = 20
def chi4(n):
    n%=4; return {1:1,3:-1}.get(n,0)
def chi3(n):
    n%=3; return {1:1,2:-1}.get(n,0)
def Lval(chi,q,s):
    return sum(chi(r)*mp.zeta(s,mp.mpf(r)/q) for r in range(1,q+1))*mp.power(q,-s)
def parity(chi): return 0 if chi(-1)==1 else 1
def Z(chi,q,a,t):
    s=mp.mpc(mp.mpf(1)/2,t)
    return mp.re(mp.power(mp.mpf(q)/mp.pi,(s+a)/2)*mp.gamma((s+a)/2)*Lval(chi,q,s))
def find_zeros(chi,q,Tmax,step=mp.mpf('0.1')):
    a=parity(chi);out=[];t=mp.mpf('0.02');p=Z(chi,q,a,t)
    while t<Tmax:
        t2=t+step;c=Z(chi,q,a,t2)
        if p*c<0:
            g=mp.findroot(lambda x:Z(chi,q,a,x),(t+t2)/2)
            if not out or abs(mp.re(g)-out[-1])>1e-3: out.append(mp.re(g))
        p=c;t=t2
    return out
for chi,q,nm in [(chi4,4,'chi4(odd)'),(chi3,3,'chi3(odd)')]:
    Tmax=120
    zs=find_zeros(chi,q,Tmax)
    s=2*sum(1/(mp.mpf(1)/4+g**2) for g in zs)
    tail=2*mp.quad(lambda t:(1/mp.pi)*mp.log(q*t/(2*mp.pi))/(mp.mpf(1)/4+t**2),[Tmax,mp.inf])
    cz=s+tail
    a=parity(chi)
    LL=mp.re(mp.diff(lambda z:mp.log(Lval(chi,q,z)),mp.mpf(1),h=mp.mpf('1e-8')))
    arch=mp.log(mp.mpf(q)/mp.pi)+mp.digamma((1+a)/mp.mpf(2))
    print(f"{nm}: c_chi(zeros,{len(zs)} zeros<{Tmax})={mp.nstr(cz,8)}  [sum={mp.nstr(s,7)} tail={mp.nstr(tail,4)}]")
    print(f"   arch=log(q/pi)+psi((1+a)/2)={mp.nstr(arch,7)}  2L'/L(1)={mp.nstr(2*LL,7)}  arch+2L'/L={mp.nstr(arch+2*LL,7)}  resid={mp.nstr(cz-(arch+2*LL),5)}")
