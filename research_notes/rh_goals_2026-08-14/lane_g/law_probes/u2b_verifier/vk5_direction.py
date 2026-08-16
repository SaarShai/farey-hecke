# INDEPENDENT direction check: N_q(L) vs N_theta(L), incl. SMALL q and larger truncation.
import math, itertools, sys
def u(j,lam):
    if abs(lam-2.0)<1e-15: return float(j)
    th=math.acos(lam/2.0); return math.sin(j*th)/math.sin(th)
def tr_word(w,lam,amax):
    uu={j:u(j,lam) for j in range(0,amax+2)}
    P=((1.0,0.0),(0.0,1.0))
    for a in w:
        aa=abs(a)
        B=((uu[aa],uu[aa+1]),(uu[aa-1],uu[aa])) if a>0 else ((uu[aa],uu[aa-1]),(uu[aa+1],uu[aa]))
        P=((P[0][0]*B[0][0]+P[0][1]*B[1][0],P[0][0]*B[0][1]+P[0][1]*B[1][1]),
           (P[1][0]*B[0][0]+P[1][1]*B[1][0],P[1][0]*B[0][1]+P[1][1]*B[1][1]))
    return abs(P[0][0]+P[1][1])
def count(alpha,lam,L,mmax,amax):
    n=0
    for m in range(1,mmax+1):
        for w in itertools.product(alpha,repeat=m):
            rots=[w[i:]+w[:i] for i in range(m)]
            if w!=min(rots) or len(set(rots))!=m: continue
            t=tr_word(w,lam,amax)
            if t>2+1e-9 and 2*math.acosh(t/2)<=L+1e-9: n+=1
    return n
# N_theta truncation sensitivity
print("N_theta(L) truncation sensitivity (signed syllables |a|<=amax, m<=mmax):")
for L in (4.0,5.0,6.0):
    row=[]
    for (amax,mmax) in [(8,4),(12,4),(20,4),(8,5),(12,5),(20,6)]:
        alpha=[a for a in range(-amax,amax+1) if a!=0]
        row.append(((amax,mmax),count(alpha,2.0,L,mmax,amax)))
    print("  L=",L,row); sys.stdout.flush()
# small q
print("small-q N_q vs N_theta (m<=4, matching the author's truncation):")
for L in (4.0,5.0,6.0):
    alpha=[a for a in range(-8,9) if a!=0]
    nth=count(alpha,2.0,L,4,8)
    for q in (5,6,7,8):
        nq=count(list(range(1,q)),2*math.cos(math.pi/q),L,4,q)
        print(f"   L={L} q={q}: N_q={nq}  N_theta={nth}  N_q>=N_theta? {nq>=nth}")
    sys.stdout.flush()
