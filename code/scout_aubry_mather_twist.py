"""
scout_aubry_mather_twist.py
===========================
Aubry-Mather / area-preserving twist-map scout for the Taha G_q-BCZ map.

EXPERIMENT 1: Is the map a monotone TWIST map?
  A monotone twist map of the cylinder/annulus (x,y)->(x',y') satisfies
  d x'/d y > 0 (or <0) uniformly (Birkhoff twist condition). We compute the
  Jacobian numerically on a grid inside each branch and check the sign / range
  of the relevant off-diagonal partial. We try several coordinate readings:
    (A) raw (a,b)->(a',b'): twist = d a'/d b
    (B) the corridor block-monodromy M_W (linear, elliptic): twist of a LINEAR
        elliptic map is identically ZERO off-diagonal in rotated coords -> NOT twist.
  We also check area preservation |det J| = 1 (Casorati).

EXPERIMENT 2: rotation structure. For the corridor block M_W = [[-l,2l^2+1],[-1,2l]]
  (det 1, trace l = 2cos(pi/q)) the rotation number is theta/2pi = (1/2pi) arccos(l/2)
  = (1/2pi)(pi - pi/q)?? -- check what rotation angle actually is and whether it ties to pi/q.

EXPERIMENT 3: Birkhoff-average / Mather-beta-style minimal action.
  Treat P = a*b (gap product, the ergodic-opt observable) as a 'Lagrangian/cost'.
  For ergodic optimization, X_Omega = inf_mu int P dmu is the MINIMAL ergodic average
  (NOTE: our X_Omega = inf_mu ess-sup, NOT inf_mu mean -- a DIFFERENT functional!).
  We compute BOTH:
    - inf over orbits of the time-average of P  (Birkhoff/Mather-beta object)
    - inf over orbits of ess-sup (max) of P     (our actual X_Omega object)
  and compare to 1/lambda^3. This tests whether 1/lambda^3 is a Mather minimal-action
  value (mean) or strictly the support-edge (max) object.
"""
import math
import numpy as np

def hecke_setup(q):
    lam = 2.0*math.cos(math.pi/q)
    U = np.array([[lam,-1.0],[1.0,0.0]])
    w = [np.array([1.0,0.0])]
    for _ in range(q):
        w.append(U@w[-1])
    return lam, w

def bcz_step(a,b,lam,w,q):
    d = [float(w[i]@np.array([a,b])) for i in range(q+1)]
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

# ---------- EXPERIMENT 1: twist condition + area preservation ----------
def jacobian_numeric(a,b,lam,w,q,h=1e-7):
    a0,b0,i0,k0,_=bcz_step(a,b,lam,w,q)
    ax,bx,ix,kx,_=bcz_step(a+h,b,lam,w,q)
    ay,by,iy,ky,_=bcz_step(a,b+h,lam,w,q)
    # only valid if branch index & floor k unchanged (smooth patch)
    if (ix,kx)!=(i0,k0) or (iy,ky)!=(i0,k0):
        return None,i0
    da_da=(ax-a0)/h; da_db=(ay-a0)/h
    db_da=(bx-b0)/h; db_db=(by-b0)/h
    J=np.array([[da_da,da_db],[db_da,db_db]])
    return J,i0

def exp1_twist(q,N=4000):
    lam,w=hecke_setup(q)
    twists=[]   # da'/db
    dets=[]
    branch_twist={}
    rng=np.random.default_rng(7)
    n=0
    while n<N:
        a=rng.random(); b=rng.random()
        if not(0<a<=1 and (1-lam*a)<b<=1): continue
        # burn a few to land on attractor-ish region
        for _ in range(5):
            a,b,i,k,_=bcz_step(a,b,lam,w,q)
            if not(0<a<=1 and (1-lam*a)<b<=1): break
        J,i0=jacobian_numeric(a,b,lam,w,q)
        if J is None: continue
        twists.append(J[0,1])   # d a'/d b
        dets.append(np.linalg.det(J))
        branch_twist.setdefault(i0,[]).append(J[0,1])
        n+=1
    twists=np.array(twists); dets=np.array(dets)
    pos=np.sum(twists>1e-9); neg=np.sum(twists<-1e-9); zero=np.sum(np.abs(twists)<=1e-9)
    print(f"q={q} lam={lam:.5f}: |det J| range [{dets.min():.6f},{dets.max():.6f}] (area-preserving if ~1)")
    print(f"   da'/db: min={twists.min():.4f} max={twists.max():.4f}  sign-split pos/neg/zero = {pos}/{neg}/{zero}")
    print(f"   -> monotone twist (uniform sign) ? {'YES' if (pos==0 or neg==0) and zero==0 else 'NO (sign changes / zeros)'}")
    for i in sorted(branch_twist):
        arr=np.array(branch_twist[i])
        print(f"      branch T{i}: da'/db in [{arr.min():.4f},{arr.max():.4f}]  n={len(arr)}")
    return twists,dets

# ---------- EXPERIMENT 2: corridor block rotation number ----------
def exp2_rotation(q):
    lam=2.0*math.cos(math.pi/q)
    MW=np.array([[-lam,2*lam**2+1],[-1.0,2*lam]])
    det=np.linalg.det(MW); tr=np.trace(MW)
    # elliptic rotation angle from trace: 2cos(theta)=tr  => theta = arccos(tr/2)
    theta=math.acos(tr/2.0)
    ev=np.linalg.eigvals(MW)
    print(f"q={q}: M_W det={det:.6f} trace={tr:.6f} (=lam={lam:.6f}?) eig={ev}")
    print(f"   rotation angle theta=arccos(tr/2)={theta:.6f} rad = {theta/math.pi:.6f} pi")
    print(f"   pi/q = {math.pi/q:.6f} = {1.0/q:.6f} pi   |  pi - pi/q = {(1-1/q):.6f} pi")
    print(f"   rotation number rho=theta/2pi = {theta/(2*math.pi):.6f}")
    return theta

# ---------- EXPERIMENT 3: Mather-beta (mean) vs ess-sup (max) ----------
def exp3_mather_vs_esssup(q, n_orbits=4000, n_steps=3000, burn=300):
    lam,w=hecke_setup(q)
    X=X_of_q(q)
    rng=np.random.default_rng(11)
    min_mean=np.inf; min_max=np.inf
    means=[]; maxes=[]
    for _ in range(n_orbits):
        a=rng.random(); b=rng.random()
        if not(0<a<=1 and (1-lam*a)<b<=1): continue
        for _ in range(burn):
            a,b,i,k,P=bcz_step(a,b,lam,w,q)
        Ps=[]
        for _ in range(n_steps):
            a,b,i,k,P=bcz_step(a,b,lam,w,q)
            Ps.append(P)
        Ps=np.array(Ps)
        m=Ps.mean(); mx=Ps.max()
        means.append(m); maxes.append(mx)
        min_mean=min(min_mean,m); min_max=min(min_max,mx)
    means=np.array(means); maxes=np.array(maxes)
    print(f"q={q} lam={lam:.5f} X=1/lam^3={X:.6f}")
    print(f"   inf-over-orbits of MEAN(P)   = {min_mean:.6f}   (Mather-beta / minimal ergodic average candidate)")
    print(f"   inf-over-orbits of MAX(P)    = {min_max:.6f}    (our X_Omega = inf ess-sup)")
    print(f"   1/lam^3                      = {X:.6f}")
    print(f"   max(P)->X match? ratio min_max/X = {min_max/X:.4f}")
    print(f"   mean(P)->X match? ratio min_mean/X = {min_mean/X:.4f}")
    # also overall mean of P over big sample (Lebesgue/invariant average)
    print(f"   typical orbit mean(P) ~ {means.mean():.6f}, typical max(P) ~ {maxes.mean():.6f}")
    return min_mean,min_max,X

if __name__=="__main__":
    print("="*70)
    print("EXPERIMENT 1: TWIST CONDITION + AREA PRESERVATION (raw (a,b) map)")
    print("="*70)
    for q in [3,4,5,7]:
        exp1_twist(q)
        print()
    print("="*70)
    print("EXPERIMENT 2: CORRIDOR BLOCK M_W ROTATION NUMBER")
    print("="*70)
    for q in [5,7,12,18,30]:
        exp2_rotation(q)
        print()
    print("="*70)
    print("EXPERIMENT 3: MATHER-BETA (mean) vs ESS-SUP (max) vs 1/lam^3")
    print("="*70)
    for q in [3,5,7,12]:
        exp3_mather_vs_esssup(q)
        print()
