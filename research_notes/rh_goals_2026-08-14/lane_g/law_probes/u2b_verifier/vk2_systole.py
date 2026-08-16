# INDEPENDENT systole + path-bound check.
# Words built from ACTUAL SL2 matrices S and R (no M_a shortcut).
import math, itertools, sys

def run(q, MMAX, verbose=True):
    lam = 2*math.cos(math.pi/q)
    S = ((0.0,-1.0),(1.0,0.0))
    R = ((0.0,-1.0),(1.0,lam))
    def mm(A,B):
        return ((A[0][0]*B[0][0]+A[0][1]*B[1][0], A[0][0]*B[0][1]+A[0][1]*B[1][1]),
                (A[1][0]*B[0][0]+A[1][1]*B[1][0], A[1][0]*B[0][1]+A[1][1]*B[1][1]))
    I=((1.0,0.0),(0.0,1.0))
    Rp=[I]
    for a in range(1,q+1): Rp.append(mm(Rp[-1],R))
    SR=[None]+[mm(S,Rp[a]) for a in range(1,q)]      # actual S R^a
    s=math.sin(math.pi/q)
    uu=[math.sin(j*math.pi/q)/s for j in range(q+2)]
    heavy=set(range(2,q-1)); light={1,q-1}
    best=float('inf'); arg=[]; nw=0; nhyp=0
    viol_A=0; viol_B=0; minratioB=1e18
    for m in range(1,MMAX+1):
        for w in itertools.product(range(1,q),repeat=m):
            rots=[w[i:]+w[:i] for i in range(m)]
            if w!=min(rots): continue
            if len(set(rots))!=m: continue
            nw+=1
            P=I
            for a in w: P=mm(P,SR[a])
            tr=P[0][0]+P[1][1]
            at=abs(tr)
            # A(w)
            A=2.0
            for a in w:
                if a in heavy: A*=uu[a]
            if at < A-1e-9: viol_A+=1
            # B(w): maximal cyclic light runs
            if all(a in light for a in w):
                # cyclic runs of a single light letter
                runs=[]
                if len(set(w))==1:
                    runs=[m]
                else:
                    # rotate to a boundary
                    st=next(i for i in range(m) if w[i]!=w[i-1])
                    rot=w[st:]+w[:st]
                    cur=rot[0]; c=0
                    for a in rot:
                        if a==cur: c+=1
                        else: runs.append(c); cur=a; c=1
                    runs.append(c)
            else:
                st=next(i for i,a in enumerate(w) if a in heavy)
                rot=w[st:]+w[:st]
                runs=[]; cur=None; c=0
                for a in list(rot)+[None]:
                    if a is not None and a in light and a==cur: c+=1
                    else:
                        if cur is not None and cur in light: runs.append(c)
                        cur=a; c=1
            B=lam**len(runs)
            for p in runs: B*=p
            if at < B-1e-9: viol_B+=1
            if B>0: minratioB=min(minratioB, at/B)
            if at>2+1e-9:
                nhyp+=1
                if at<best-1e-9: best,arg=at,[w]
                elif abs(at-best)<1e-9 and len(arg)<8: arg.append(w)
    return dict(q=q,MMAX=MMAX,words=nw,hyp=nhyp,min_tr=best,two_lam=2*lam,
                argmin=arg,viol_A=viol_A,viol_B=viol_B,min_tr_over_B=minratioB)

plan=[(3,8),(4,8),(5,9),(6,7),(7,7),(8,6),(9,6),(10,5),(11,5),(12,5),(13,5),(14,5),(20,4),(25,4),(50,3),(100,3)]
allok=True
for q,mm in plan:
    r=run(q,mm)
    ok = (abs(r['min_tr']-r['two_lam'])<1e-8) if q>=4 else None
    print(f"q={q:4d} m<={mm} words={r['words']:8d} min|tr|={r['min_tr']:.9f} 2lam_q={r['two_lam']:.9f} "
          f"C1={ok} argmin={r['argmin']} violA={r['viol_A']} violB={r['viol_B']} min(tr/B)={r['min_tr_over_B']:.4f}")
    if q>=4 and not ok: allok=False
    if r['viol_A'] or r['viol_B']: allok=False
    sys.stdout.flush()
print("ALL OK:",allok)
