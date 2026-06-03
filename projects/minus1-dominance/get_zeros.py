"""
Compute imaginary parts gamma>0 of low-lying nontrivial zeros of L(s,chi) for
each primitive/imprimitive Dirichlet character mod N, via mpmath.

We use mpmath's ability to evaluate Dirichlet L-functions and find zeros on the
critical line by sign changes of the Hardy-like Z-function for each chi.
For the RS density Monte Carlo we need, per character chi, the multiset
{gamma>0}. The variance weight uses 1/(1/4+gamma^2); the series converges so a
few hundred zeros per character suffice for high accuracy on delta.
"""
import mpmath as mp
mp.mp.dps = 25

def char_table(N):
    import itertools
    from math import gcd
    U=[a for a in range(1,N) if gcd(a,N)==1]
    def order(g):
        o=1;x=g
        while x!=1: x=(x*g)%N; o+=1
        return o
    def gensub(elems):
        S={1};ch=True
        while ch:
            ch=False
            for e in elems:
                for s in list(S):
                    v=(s*e)%N
                    if v not in S: S.add(v);ch=True
        return S
    basis=[];sub={1}
    for g in U:
        if g==1:continue
        ns=gensub([x for x,_ in basis]+[g])
        if len(ns)>len(sub):
            basis.append((g,order(g)));sub=ns
            if len(sub)==len(U):break
    ge=[g for g,_ in basis];go=[o for _,o in basis]
    coords={}
    for exps in itertools.product(*[range(o) for o in go]):
        val=1
        for g,e in zip(ge,exps):val=(val*pow(g,e,N))%N
        coords[val]=exps
    chars=list(itertools.product(*[range(o) for o in go]))
    def cval(k,a):
        e=coords[a%N]
        arg=sum(mp.mpf(kj*ej)/oj for kj,ej,oj in zip(k,e,go))
        return mp.e**(2j*mp.pi*arg)
    return U,ge,go,coords,chars,cval

def L_chi(s, k, N, cval, U, maxn=4000):
    # Dirichlet L via Euler-Maclaurin-free direct + Hurwitz for analytic cont.
    # Use Hurwitz zeta representation: L(s,chi)=N^{-s} sum_{r in U} chi(r) zeta(s, r/N)
    tot=mp.mpf(0)
    for r in U:
        tot += cval(k,r)*mp.zeta(s, mp.mpf(r)/N)
    return N**(-s)*tot

def find_zeros(k,N,cval,U,Tmax=40,step=mp.mpf('0.05')):
    # locate sign changes of the real "rotated" L on critical line.
    # Build Z(t)=exp(i theta) L(1/2+it) made real via functional eqn is fiddly for
    # imprimitive chars; instead detect zeros by |L| dips + argument principle-lite:
    # we track L(1/2+it) and record t where Re and Im both cross -> use that
    # complex L has a zero when it passes through 0; detect by local min of |L|
    # with sign change of arg over 2pi. Simpler robust approach: sample L on the
    # line and find t where successive samples bracket a zero of the real part of
    # L*conj(gamma-factor). For our purposes (variance weights), approximate via
    # mpmath's zeros of the *completed* function is overkill. We use sign changes
    # of Re(L*phase) is unreliable. Instead: detect zeros as local minima of |L|
    # below a threshold and refine by 2D Newton.
    zeros=[]
    t=step
    prev=L_chi(mp.mpf('0.5')+1j*(t-step),k,N,cval,U)
    while t<Tmax:
        cur=L_chi(mp.mpf('0.5')+1j*t,k,N,cval,U)
        nxt=L_chi(mp.mpf('0.5')+1j*(t+step),k,N,cval,U)
        if abs(cur)<abs(prev) and abs(cur)<abs(nxt) and abs(cur)<0.5:
            # refine with secant on the complex function along the line via Newton in t
            try:
                z=mp.findroot(lambda tt: L_chi(mp.mpf('0.5')+1j*tt,k,N,cval,U), t)
                zr=mp.re(z)
                if abs(L_chi(mp.mpf('0.5')+1j*zr,k,N,cval,U))<1e-8 and zr>0:
                    if not zeros or abs(zr-zeros[-1])>1e-4:
                        zeros.append(zr)
            except Exception:
                pass
        prev=cur; t+=step
    return zeros

if __name__=="__main__":
    import sys, json
    N=int(sys.argv[1]) if len(sys.argv)>1 else 8
    Tmax=mp.mpf(sys.argv[2]) if len(sys.argv)>2 else mp.mpf(60)
    U,ge,go,coords,chars,cval=char_table(N)
    out={}
    for k in chars:
        if all(x==0 for x in k): continue  # skip principal
        z=find_zeros(k,N,cval,U,Tmax=Tmax)
        out[str(k)]=[float(x) for x in z]
        chi_m1 = cval(k,N-1)
        print(f"chi_{k}: chi(-1)={complex(chi_m1):.3f}  #zeros<{float(Tmax)}={len(z)}  first={[round(float(x),4) for x in z[:5]]}")
    json.dump(out, open(f"zeros_N{N}.json","w"))
    print("saved zeros_N%d.json"%N)
