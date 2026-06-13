"""
scout_am_minimizer.py
=====================
Pin down WHICH invariant measure attains X_Omega = inf_mu ess-sup_mu P = 1/lam^3,
and whether that is a Mather-style minimizing measure for ANY natural functional.

Repo claim (energy_route): 1/lam^3 is the CUSP-TIP value P=(1/l)^2*(1/l), attained
at the cusp fixed structure (a,b)->(1/l, 0)-ish. The minimizing measure for the
ess-sup functional is a Dirac/periodic orbit at the cusp, NOT a measure that
minimizes the AVERAGE. We test:
  (1) Find the cusp periodic orbit and its P-values; confirm max P on it = 1/lam^3.
  (2) Mather's beta-function is for the AVERAGE. The MINIMIZING average (alpha/beta)
      is attained by the measure MINIMIZING int P. Is THAT measure the same cusp orbit?
      If the inf-mean measure != inf-ess-sup measure, the two theories give DIFFERENT
      distinguished measures -> our object is NOT Mather's beta-function value.
  (3) The ess-sup / 'minimax' functional X(mu)=ess-sup_mu P. inf_mu X(mu) is the
      'minimal maximum excursion'. In ergodic-optimization language this is a
      DIFFERENT object from beta(phi)=sup int (Jenkinson). Confirm numerically that
      X_Omega is NOT lim inf_x (1/n) sum P (the ergodic minimizing AVERAGE) -- it is
      a support-edge.
"""
import math
import numpy as np

def hecke_setup(q):
    lam=2.0*math.cos(math.pi/q)
    U=np.array([[lam,-1.0],[1.0,0.0]])
    w=[np.array([1.0,0.0])]
    for _ in range(q):
        w.append(U@w[-1])
    return lam,w

def bcz_step(a,b,lam,w,q):
    d=[float(w[i]@np.array([a,b])) for i in range(q+1)]
    sub=None
    for i in range(2,q):
        if d[i-1]>1.0 and d[i]<=1.0:
            sub=i; break
    if sub is None:
        for i in range(2,q):
            if d[i]<=1.0:
                sub=i; break
        if sub is None: sub=q-1
    i=sub
    wi=d[i]; wi1=d[i+1]; yi=float(w[i][1])
    P=a*wi/yi
    k=math.floor((1.0-wi1)/(lam*wi))
    a2=wi; b2=wi1+k*lam*wi
    return a2,b2,i,k,P

def X_of_q(q):
    lam=2.0*math.cos(math.pi/q)
    if q==3: return 2.0/9.0
    if q==4: return math.sqrt(2.0)/8.0
    return 1.0/lam**3

def find_periodic_orbits(q, n_seeds=200000, maxlen=8, tol=1e-9):
    """Search for short periodic orbits; record their min/mean/max P and whether
    max P touches 1/lam^3 (cusp) or min P touches it."""
    lam,w=hecke_setup(q)
    X=X_of_q(q)
    rng=np.random.default_rng(3)
    found={}
    # detect periodicity by returning close to start within maxlen steps
    for _ in range(n_seeds):
        a=rng.random(); b=rng.random()
        if not(0<a<=1 and (1-lam*a)<b<=1): continue
        traj=[(a,b)]; Ps=[]
        ok=True
        per=None
        for step in range(maxlen):
            a,b,i,k,P=bcz_step(a,b,lam,w,q)
            Ps.append(P)
            for j,(aa,bb) in enumerate(traj):
                if abs(a-aa)<tol and abs(b-bb)<tol:
                    per=step+1-j
                    break
            if per: break
            traj.append((a,b))
        if per:
            cyc=Ps[-per:]
            key=(per,round(min(cyc),4),round(max(cyc),4))
            if key not in found:
                found[key]=dict(period=per,minP=min(cyc),maxP=max(cyc),meanP=sum(cyc)/per,Ps=[round(p,5) for p in cyc])
    return lam,X,found

if __name__=="__main__":
    for q in [3,5,7,12]:
        lam,X,found=find_periodic_orbits(q)
        print(f"\n=== q={q} lam={lam:.6f}  1/lam^3={X:.6f} ===")
        # sort by maxP
        items=sorted(found.values(), key=lambda d:d['maxP'])
        print(f"  found {len(items)} distinct short periodic orbits")
        # the orbit with SMALLEST maxP = the inf-ess-sup minimizer candidate
        if items:
            best=items[0]
            print(f"  MIN-maxP orbit: period={best['period']} maxP={best['maxP']:.6f} "
                  f"minP={best['minP']:.6f} meanP={best['meanP']:.6f}")
            print(f"     -> maxP / (1/lam^3) = {best['maxP']/X:.6f}  (==1 would mean cusp orbit IS the ess-sup minimizer)")
            print(f"     P-cycle: {best['Ps']}")
        # the orbit with SMALLEST meanP = the Mather-beta (average) minimizer candidate
        items_mean=sorted(found.values(), key=lambda d:d['meanP'])
        if items_mean:
            bm=items_mean[0]
            print(f"  MIN-meanP orbit: period={bm['period']} meanP={bm['meanP']:.6f} maxP={bm['maxP']:.6f}")
            print(f"     -> meanP / (1/lam^3) = {bm['meanP']/X:.6f}")
        # smallest single P value seen (touches 0? cusp gives P->1/lam^3 as the FLOOR of maxP)
        allmin=min(d['minP'] for d in found.values()) if found else None
        print(f"  smallest single P over all short orbits = {allmin:.6f}  (1/lam^3={X:.6f})")
