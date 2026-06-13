"""
scout_am_cusp.py — directly probe the cusp structure that attains 1/lam^3,
and the nature of the minimizing 'measure'.
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

for q in [5,7,12,18]:
    lam,w=hecke_setup(q)
    X=X_of_q(q)
    # cusp tip per repo: (a,b)=(1/lam, 0) region. P at cusp branch i=q-2: P=a(a+lb)/l.
    # The cusp fixed structure: the parabolic vertex. Evaluate P near tip a=1/l, b=0+.
    print(f"=== q={q} lam={lam:.6f} 1/lam^3={X:.6f} ===")
    # the orbit landing closest to cusp: track min over a long orbit of P and the
    # running MAX-excursion; the inf-ess-sup is the orbit whose MAX stays lowest.
    rng=np.random.default_rng(1)
    best_supP=np.inf; best_start=None
    # adaptively seed near the cusp branch entry to find low-max orbits
    for trial in range(60000):
        a=rng.random(); b=rng.random()*0.2  # bias toward small b (near cusp)
        if not(0<a<=1 and (1-lam*a)<b<=1): continue
        for _ in range(50): a,b,i,k,P=bcz_step(a,b,lam,w,q)
        if not(0<a<=1 and (1-lam*a)<b<=1): continue
        Ps=[]
        a0,b0=a,b
        for _ in range(400):
            a,b,i,k,P=bcz_step(a,b,lam,w,q)
            Ps.append(P)
        sup=max(Ps)
        if sup<best_supP:
            best_supP=sup; best_start=(a0,b0)
    print(f"  inf-over-(biased) orbits of sup P = {best_supP:.6f}  ratio/X = {best_supP/X:.4f}")
    # value of P exactly at the cusp tip configuration:
    # tip a=1/lam, b->0. The cusp branch i=q-2; P = a*(w_i.(a,b))/y_i.
    a,b=1.0/lam,1e-9
    a2,b2,i,k,P=bcz_step(a,b,lam,w,q)
    print(f"  P at cusp tip (a=1/lam,b~0): P={P:.6f}  (1/lam^3={X:.6f})  branch i={i}")
    # also tip the OTHER way: a~0,b=1
    a,b=1e-9,1.0
    a2,b2,i,k,P=bcz_step(a,b,lam,w,q)
    print(f"  P at (a~0,b=1): P={P:.6f}  branch i={i}")
    print()
