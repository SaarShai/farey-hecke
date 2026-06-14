"""
bq_exact_arc.py -- dps=50 EXACT dump of the deepest rotation-arc cluster, proving
the three structural facts on the ELLIPSE itself (fast: walks the ellipse, no random orbit):
  (i)   interior steps k=1, terminal step k>=2 still sub-thr + last-branch;
  (ii)  all points share one E (it's an ellipse level set by construction) and the
        k=1 map advances whitened phase by exactly -pi/q  (verified: Rot matrix angle);
  (iii) the run ends at the first floor increment (first k>=2), included if sub-thr+LB.
Also verifies M=[[0,1],[-1,lam]] preserves E and is rotation by pi/q (exact).
"""
import mpmath as mp
mp.mp.dps = 50

def lam_of(q): return 2*mp.cos(mp.pi/q)
def t_of(q):   return 1/lam_of(q)**3
def hecke_w(q):
    lam=lam_of(q); w=[(mp.mpf(1),mp.mpf(0))]
    for _ in range(q+3):
        x,y=w[-1]; w.append((lam*x-y,x))
    return lam,w

def whiten(q):
    lam=lam_of(q)
    l11=mp.mpf(1); l21=-lam/2; l22=mp.sqrt(1-l21**2)
    det=l11*l22
    LTinv=[[l22/det,-l21/det],[mp.mpf(0),l11/det]]
    LT=[[l11,l21],[mp.mpf(0),l22]]
    def coords(phi,E0):
        rho=mp.sqrt(E0)
        y0=rho*mp.cos(phi); y1=rho*mp.sin(phi)
        return (LTinv[0][0]*y0+LTinv[0][1]*y1, LTinv[1][0]*y0+LTinv[1][1]*y1)
    def phi_of(a,b):
        y0=LT[0][0]*a+LT[0][1]*b; y1=LT[1][0]*a+LT[1][1]*b
        return mp.atan2(y1,y0)
    def E(a,b): return a*a-lam*a*b+b*b
    return coords,phi_of,E,LT,LTinv

def check_M_rotation(q):
    """M=[[0,1],[-1,lam]] : preserves E, det=1, tr=lam, conjugate to rotation by -pi/q."""
    lam=lam_of(q)
    coords,phi_of,E,LT,LTinv=whiten(q)
    # M acts on x; in y=L^T x coords: y' = L^T M (L^T)^{-1} y = Rot
    M=mp.matrix([[0,1],[-1,lam]])
    LTm=mp.matrix(LT); LTinvm=mp.matrix(LTinv)
    Rot=LTm*M*LTinvm
    ang=mp.atan2(Rot[1,0],Rot[0,0])
    det=mp.det(Rot)
    # E preserved: E(M x)=E(x) symbolically -> check on a random x
    a,b=mp.mpf("0.37"),mp.mpf("0.21")
    a2=b; b2=-a+lam*b
    return ang, det, E(a,b)-E(a2,b2), mp.det(M), (0+lam)  # tr

def is_lb(a,b,lam,w,q):
    return (w[q-2][0]*a+w[q-2][1]*b>1) and (w[q-1][0]*a+w[q-1][1]*b<=1)
def kval(a,b,lam,w,q):
    wi=w[q-1][0]*a+w[q-1][1]*b; wq=w[q][0]*a+w[q][1]*b
    return int(mp.floor((1-wq)/(lam*wi))) if wi>0 else None

def deepest_arc(q, frac, off_grid=8000):
    """find deepest consecutive last-branch+sub-thr run on the governing ellipse, dps=50."""
    lam,w=hecke_w(q); t=t_of(q); theta=mp.pi/q
    coords,phi_of,E,LT,LTinv=whiten(q)
    mu_max=1/(2-lam); E0=frac*t/mu_max
    best=0; bestoff=None
    for io in range(off_grid):
        off=2*mp.pi*io/off_grid
        run=0
        for n in range(2*q+6):
            a,b=coords(off-n*theta,E0)
            if (a>0 and a<=1 and b<=1 and b>1-lam*a and a+lam*b>1 and is_lb(a,b,lam,w,q) and a*b<t):
                run+=1
            else: break
        if run>best: best=run; bestoff=off
    # dump
    seq=[]
    for n in range(best):
        a,b=coords(bestoff-n*theta,E0)
        seq.append((a,b,kval(a,b,lam,w,q)))
    return best,E0,seq,E,phi_of,lam,t,theta

if __name__=="__main__":
    print("== M=[[0,1],[-1,lam]] : rotation/conserved-E check (dps=50) ==")
    for q in [7,23,40]:
        ang,det,dE,detM,trM=check_M_rotation(q)
        print(f"  q={q}: Rot angle={mp.nstr(ang,12)} (-pi/q={mp.nstr(-mp.pi/q,12)})  det(Rot)={mp.nstr(det,6)}  "
              f"E(x)-E(Mx)={mp.nstr(dE,4)}  det(M)={mp.nstr(detM,4)} tr(M)=lam={mp.nstr(trM,8)}")
    print()
    fracs={7:0.9795,13:0.9976,19:0.9902,23:1.0023,24:0.9922,30:0.9856,40:0.9862}
    for q in [7,13,19,23,24,30,40]:
        best,E0,seq,E,phi_of,lam,t,theta=deepest_arc(q,mp.mpf(str(fracs[q])))
        print(f"=== q={q}  deepest arc len={best}  E0={mp.nstr(E0,8)}  t={mp.nstr(t,8)} ===")
        kp=[k for (_,_,k) in seq]; print(f"    k-pattern={kp}")
        prev=None
        for (a,b,k) in seq:
            ph=phi_of(a,b); ev=E(a,b); dphi=""
            if prev is not None:
                dd=ph-prev; dd=(dd+mp.pi)%(2*mp.pi)-mp.pi
                dphi=f" dphi={mp.nstr(dd,6)}"
            print(f"    ab={mp.nstr(a*b,8)} k={k} E={mp.nstr(ev,10)} (t-ab={mp.nstr(t-a*b,3)}){dphi}")
            prev=ph
        print(f"    -pi/q={mp.nstr(-theta,6)}\n")
