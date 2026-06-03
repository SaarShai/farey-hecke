"""
Clean Hardy Z-function for a primitive Dirichlet L-function, validated against
the KNOWN zeros of the Dirichlet beta function L(s,chi_4):
  6.020948, 10.243770, 12.988098, 16.342940, 18.291916, 22.275932, ...
(reference: A. Spira; LMFDB L-function 1-4-4.3-r1-0-0)

Completed L:  Lambda(s,chi)=(q/pi)^{(s+a)/2} Gamma((s+a)/2) L(s,chi),  a=(1-chi(-1))/2.
Functional eq:  Lambda(s,chi) = eps * Lambda(1-s, conj chi),  |eps|=1.
For a real primitive chi (conj chi=chi), eps = +1 (it equals tau(chi)/(i^a sqrt q)
and for real chi the Gauss sum tau(chi)=i^a sqrt q, so eps=+1).
Hence Lambda(1/2+it,chi) = eps * conj(Lambda(1/2+it,chi)) => Lambda(1/2+it) is REAL
when eps=+1.  So  Z(t) := Lambda(1/2+it,chi)  is already real; its sign changes are
the zeros.  (No extra rotation needed for real chi with eps=+1.)
"""
import mpmath as mp
mp.mp.dps = 30

def chi4(n):
    n%=4; return {1:1,3:-1}.get(n,0)
def chi3(n):
    n%=3; return {1:1,2:-1}.get(n,0)
def chi8a(n):  # the two real chars mod 8
    n%=8; return {1:1,3:-1,5:-1,7:1}.get(n,0)  # even, kronecker(2,.)
def chi8b(n):
    n%=8; return {1:1,3:1,5:-1,7:-1}.get(n,0)  # odd? check

def Lval(chi,q,s):
    return sum(chi(r)*mp.zeta(s,mp.mpf(r)/q) for r in range(1,q+1))*mp.power(q,-s)

def Z(chi,q,a,t):
    s=mp.mpc(mp.mpf(1)/2,t)
    Lam=mp.power(mp.mpf(q)/mp.pi,(s+a)/2)*mp.gamma((s+a)/2)*Lval(chi,q,s)
    return mp.re(Lam)  # real for eps=+1 real chi

def parity(chi):
    return 0 if chi(-1)==1 else 1   # a=0 even, a=1 odd

def find_zeros(chi,q,Tmax,step=mp.mpf('0.05')):
    a=parity(chi); out=[]; t=mp.mpf('0.02'); p=Z(chi,q,a,t)
    while t<Tmax:
        t2=t+step; c=Z(chi,q,a,t2)
        if p*c<0:
            g=mp.findroot(lambda x:Z(chi,q,a,x),(t+t2)/2)
            out.append(mp.re(g))
        p=c; t=t2
    return out

z4=find_zeros(chi4,4,30)
print("chi4 (a=%d) zeros:"%parity(chi4),[mp.nstr(g,8) for g in z4])
print("   KNOWN:        6.020948 10.243770 12.988098 16.342940 18.291916 22.275932")
z3=find_zeros(chi3,3,30)
print("chi3 (a=%d) zeros:"%parity(chi3),[mp.nstr(g,8) for g in z3])
print("   KNOWN:        8.039737 11.249193 15.704619 18.26199 20.42154")

# ---- c_chi from validated zeros, high Tmax, with tail integral ----
def c_chi_zeros(chi,q,Tmax=300):
    zs=find_zeros(chi,q,Tmax)
    # dedupe near-equal
    zs2=[]
    for g in sorted(zs):
        if not zs2 or abs(g-zs2[-1])>1e-4:
            zs2.append(g)
    s=2*sum(1/(mp.mpf(1)/4+g**2) for g in zs2)   # +/- pairs
    # tail T>Tmax: number of zeros up to height T for L(s,chi) is
    # N(T) ~ (T/pi) log(qT/(2 pi e)); density n(t)=N'(t)=(1/pi)log(qt/2pi).
    tail=2*mp.quad(lambda t:(1/mp.pi)*mp.log(q*t/(2*mp.pi))/(mp.mpf(1)/4+t**2),[Tmax,mp.inf])
    return s, tail, len(zs2)

print("\n=== c_chi via validated zeros (Tmax=300) ===")
for chi,q,nm in [(chi4,4,'chi4'),(chi3,3,'chi3')]:
    s,tail,nz=c_chi_zeros(chi,q,300)
    print(f"{nm}: sum(|g|<300, {nz} zeros)={mp.nstr(s,9)}  tail={mp.nstr(tail,4)}  c_chi={mp.nstr(s+tail,9)}")

# ---- Now match analytic formula. The TRUE identity (Rubinstein-Sarnak 1994):
# For primitive chi mod q, define b(chi)=sum_gamma 1/(1/4+gamma^2). Then
#   b(chi) = log(q/pi) + (gamma_Euler?)... we DETERMINE the constant by matching.
def LpL(chi,q): return mp.re(mp.diff(lambda z:mp.log(Lval(chi,q,z)),mp.mpf(1),h=mp.mpf('1e-10')))
print("\n=== Determine analytic constant by matching ===")
for chi,q,nm in [(chi4,4,'chi4'),(chi3,3,'chi3')]:
    a=parity(chi)
    cz=sum(c_chi_zeros(chi,q,300)[:2])
    LL=LpL(chi,q)
    arch=mp.log(mp.mpf(q)/mp.pi)+mp.digamma((1+a)/mp.mpf(2))
    # cz should equal arch + 2*LL + K for some universal K. Solve K:
    K=cz-(arch+2*LL)
    print(f"{nm}: c_chi(zeros)={mp.nstr(cz,8)} arch={mp.nstr(arch,8)} 2L'/L(1)={mp.nstr(2*LL,8)}  residual K={mp.nstr(K,6)}")
