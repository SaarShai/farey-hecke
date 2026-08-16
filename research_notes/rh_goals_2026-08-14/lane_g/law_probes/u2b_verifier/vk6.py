# CONVERGED N_q(L) and N_theta(L) via DFS with the monotone-trace prune.
# Fact used (proved from the nonneg normal form): tr(P*M_a) >= tr(P) since diag(M_a)=u_a>=1.
import math, sys
def uvals(lam,amax):
    if abs(lam-2.0)<1e-15: return [float(j) for j in range(amax+2)]
    th=math.acos(lam/2.0); return [math.sin(j*th)/math.sin(th) for j in range(amax+2)]
def enum(alpha,lam,L,amax,mmax=40):
    """count primitive cyclic words (canonical rotation) with 2 < |tr| <= 2cosh(L/2)"""
    uu=uvals(lam,amax+1)
    def Mof(a):
        aa=abs(a)
        return ((uu[aa],uu[aa+1]),(uu[aa-1],uu[aa])) if a>0 else ((uu[aa],uu[aa-1]),(uu[aa+1],uu[aa]))
    Ms={a:Mof(a) for a in alpha}
    T=2*math.cosh(L/2)
    found=set(); cnt=0
    stack=[((a,),Ms[a]) for a in alpha]
    while stack:
        w,P=stack.pop()
        tr=abs(P[0][0]+P[1][1])
        if tr>T+1e-9:  # trace monotone under extension -> prune whole subtree
            continue
        m=len(w)
        rots=[w[i:]+w[:i] for i in range(m)]
        if w==min(rots) and len(set(rots))==m and tr>2+1e-9:
            cnt+=1
        if m<mmax:
            for a in alpha:
                B=Ms[a]
                Q=((P[0][0]*B[0][0]+P[0][1]*B[1][0],P[0][0]*B[0][1]+P[0][1]*B[1][1]),
                   (P[1][0]*B[0][0]+P[1][1]*B[1][0],P[1][0]*B[0][1]+P[1][1]*B[1][1]))
                stack.append((w+(a,),Q))
    return cnt
for L in (4.0,5.0,6.0):
    res={}
    for amax in (10,16,24):
        alpha=[a for a in range(-amax,amax+1) if a!=0]
        res[amax]=enum(alpha,2.0,L,amax)
    print(f"L={L}: N_theta converged? amax10={res[10]} amax16={res[16]} amax24={res[24]}")
    row=[]
    for q in (5,6,7,8,10,12,16,22,30,50):
        row.append((q,enum(list(range(1,q)),2*math.cos(math.pi/q),L,q)))
    print(f"   N_q: {row}")
    sys.stdout.flush()
