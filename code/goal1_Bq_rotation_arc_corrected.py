"""
Fast (double-precision) corrected rotation-arc counter, vectorized over phase offset.
Count = max consecutive -theta-rotation lattice points on ellipse E0 that are
last-branch AND sub-threshold (NO k==1 gate -> includes terminal k>=2 point).
Maximized over E0 (band hugging onset from below) and phase offset.
The COUNT is a robust integer; borderline q re-checked at dps=50 separately.
"""
import numpy as np, math, sys

def lam_of(q): return 2*math.cos(math.pi/q)
def t_of(q):   return 1/lam_of(q)**3
def hecke_w(q):
    lam=lam_of(q); w=[(1.0,0.0)]
    for _ in range(q+3):
        x,y=w[-1]; w.append((lam*x-y,x))
    return lam,w

def whiten_LTinv(q):
    lam=lam_of(q)
    l11=1.0; l21=-lam/2; l22=math.sqrt(1-l21**2)
    det=l11*l22
    return np.array([[l22/det,-l21/det],[0.0,l11/det]])

def max_run(q, n_E0=600, n_off=4000):
    lam,w=hecke_w(q); t=t_of(q); theta=math.pi/q
    LTinv=whiten_LTinv(q)
    mu_max=1/(2-lam)
    Nrot=2*q+6
    # phase offsets (vectorized): for each offset we sample n=0..Nrot-1
    offs=np.linspace(0,2*math.pi,n_off,endpoint=False)
    n_idx=np.arange(Nrot)
    # phi[off, n] = off - n*theta
    PHI = offs[:,None]-n_idx[None,:]*theta            # shape (n_off, Nrot)
    best=0; best_frac=None; best_kp=None
    wq2x,wq2y = w[q-2]; wq1x,wq1y=w[q-1]; wqx,wqy=w[q]
    for ie in range(n_E0):
        frac = 0.85 + 0.40*ie/(n_E0-1)                # peak ab in [0.85t,1.25t]
        E0=frac*t/mu_max; rho=math.sqrt(E0)
        y0=rho*np.cos(PHI); y1=rho*np.sin(PHI)
        a=LTinv[0,0]*y0+LTinv[0,1]*y1
        b=LTinv[1,0]*y0+LTinv[1,1]*y1
        wprev=wq2x*a+wq2y*b
        wi=wq1x*a+wq1y*b
        ok=((a>0)&(a<=1)&(b<=1)&(b>1-lam*a)&(a+lam*b>1)
            &(wprev>1)&(wi<=1)&(a*b<t))
        # for each offset row, length of run starting at n=0 (consecutive True from col 0)
        # find first False per row
        col0=ok[:,0]
        # cumulative AND from left
        firstFalse=np.argmin(ok,axis=1)   # index of first False; if all True -> 0 (argmin returns 0)
        allTrue=ok.all(axis=1)
        runlen=np.where(col0, np.where(allTrue, Nrot, firstFalse), 0)
        m=int(runlen.max())
        if m>best:
            best=m; best_frac=frac
            # recover k-pattern for the best offset
            r=int(np.argmax(runlen))
            kp=[]
            for n in range(m):
                phi=offs[r]-n*theta
                yy0=rho*math.cos(phi); yy1=rho*math.sin(phi)
                aa=LTinv[0,0]*yy0+LTinv[0,1]*yy1
                bb=LTinv[1,0]*yy0+LTinv[1,1]*yy1
                wwi=wq1x*aa+wq1y*bb; wwq=wqx*aa+wqy*bb
                kk=int(math.floor((1-wwq)/(lam*wwi))) if wwi>0 else None
                kp.append(kk)
            best_kp=kp
    return best, best_frac, best_kp

if __name__=="__main__":
    qs=[int(x) for x in sys.argv[1:]] or list(range(7,41))
    for q in qs:
        b,fr,kp=max_run(q)
        print(f"q={q:2d}  B_corrected={b}  (frac~{fr:.4f}, kpattern={kp})", flush=True)
