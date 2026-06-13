import math
import numpy as np

rng = np.random.default_rng(20260612)

def hecke_w(q):
    lam = 2.0*math.cos(math.pi/q)
    w = [(1.0,0.0)]
    for _ in range(q+2):
        x,y = w[-1]
        w.append((lam*x - y, x))
    return lam, w

def step(a,b,lam,w,q):
    """One Taha G_q-BCZ step. Returns (a',b',branch i, k, P)."""
    sub = q-1
    d_prev = w[1][0]*a + w[1][1]*b
    for i in range(2,q):
        di = w[i][0]*a + w[i][1]*b
        if d_prev > 1.0 and di <= 1.0:
            sub = i; break
        d_prev = di
    wi  = w[sub][0]*a + w[sub][1]*b
    wi1 = w[sub+1][0]*a + w[sub+1][1]*b
    yi  = w[sub][1]
    P = a*wi/yi
    k = math.floor((1.0 - wi1)/(lam*wi))
    return wi, wi1 + k*lam*wi, sub, k, P

def Xq(q):
    lam = 2.0*math.cos(math.pi/q)
    if q==3: return 2.0/9.0
    if q==4: return math.sqrt(2.0)/8.0
    return 1.0/lam**3

for q in [3,5,7]:
    lam,w = hecke_w(q)
    X = Xq(q)
    invl3 = 1.0/lam**3
    # run a long orbit, record (a,b,branch,k,P)
    a=rng.random(); b=rng.random()
    while not (0<a<=1 and (1-lam*a)<b<=1):
        a=rng.random(); b=rng.random()
    for _ in range(500):
        a,b,_,_,_ = step(a,b,lam,w,q)
    traj=[]
    for _ in range(400000):
        a_old,b_old=a,b
        a,b,i,k,P = step(a,b,lam,w,q)
        traj.append((a_old,b_old,i,k,P))

    # (1) Verify P = a*b on LAST branch (q-1) and P=c_n*c_{n+1} identification
    lastbr = [t for t in traj if t[2]==q-1]
    maxerr = max(abs(t[4]-t[0]*t[1]) for t in lastbr) if lastbr else float('nan')
    print(f"\n=== q={q}  lam={lam:.6f}  X={X:.6f}  1/lam^3={invl3:.6f} ===")
    print(f"  last-branch fraction: {len(lastbr)/len(traj):.3f}")
    print(f"  max|P - a*b| on last branch (T_{q-1}): {maxerr:.2e}  (P=a*b => P=c_n*c_{{n+1}})")

    # (2) Find a genuine FLOOR-1 RUN on the last branch: consecutive steps with branch=q-1 AND k=1.
    # During such a run c_n := a_n satisfies c_{n+2}=lam*c_{n+1}-c_n.
    best_run=[]; cur=[]
    for idx,t in enumerate(traj):
        if t[2]==q-1 and t[3]==1:
            cur.append(idx)
        else:
            if len(cur)>len(best_run): best_run=cur[:]
            cur=[]
    if len(cur)>len(best_run): best_run=cur[:]
    print(f"  longest floor-1 (k=1) run on last branch: length {len(best_run)}")
    if len(best_run)>=2:
        # build c_n sequence = a_n over the run, plus the b of the last for closure
        idxs=best_run
        cs=[traj[i][0] for i in idxs] + [traj[idxs[-1]][1]]
        # verify recurrence c_{n+2}=lam c_{n+1}-c_n
        recerr=0.0
        for j in range(len(cs)-2):
            recerr=max(recerr, abs(cs[j+2]-(lam*cs[j+1]-cs[j])))
        # energy along run
        Es=[cs[j]**2+cs[j+1]**2-lam*cs[j]*cs[j+1] for j in range(len(cs)-1)]
        E0=Es[0]
        Evar=max(abs(e-E0) for e in Es)
        # P along run = c_n c_{n+1}
        Ps=[cs[j]*cs[j+1] for j in range(len(cs)-1)]
        minP=min(Ps)
        # predicted symmetric-max P=E0/(2-lam); and value 1/lam^3
        Pmax_pred=E0/(2-lam)
        print(f"   c_n sequence (first 6): {[round(x,5) for x in cs[:6]]}")
        print(f"   recurrence err max|c_{{n+2}}-(lam c_{{n+1}}-c_n)|: {recerr:.2e}")
        print(f"   ENERGY along run: E0={E0:.6f}, max|E-E0|={Evar:.2e}  (conserved? {'YES' if Evar<1e-9 else 'NO'})")
        print(f"   P=c_n c_{{n+1}} along run: min={minP:.6f}, max={max(Ps):.6f}")
        print(f"   predicted symmetric-MAX P=E0/(2-lam)={Pmax_pred:.6f}")
        print(f"   min P in run >= 1/lam^3={invl3:.6f}?  {minP>=invl3}  (min P - 1/lam^3 = {minP-invl3:+.6f})")
