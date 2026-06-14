"""
HYPOTHESIS: notch-gain (B = B0+1) happens iff:
  (a) B0(q) [no-notch count, peak<=t] is ODD  => target B0+1 is EVEN => symmetric straddle
      places the center GAP on the peak/notch (no lattice pt on the peak), AND
  (b) the deficit (B0+1)*... fits within the hop-able frac window (2delta<theta).
For EVEN B0, the +1 target is ODD => a lattice pt lands ON the peak (notch) => blocked.

We compute, exactly, for q=7..50:
  B0(q) = max symmetric-fit count with peak<=t (no notch)  [== continuous floor(s)+1]
  parity of B0
  whether B0+1 fits with EVEN straddle (the hop) -> predicted resonant
and compare to true B(q).
"""
import numpy as np, math, sys
def lam_of(q): return 2*math.cos(math.pi/q)
def t_of(q): return 1/lam_of(q)**3
def hecke_w(q):
    lam=lam_of(q); w=[(1.0,0.0)]
    for _ in range(q+3):
        x,y=w[-1]; w.append((lam*x-y,x))
    return lam,w
def whiten(q):
    lam=lam_of(q); l21=-lam/2; l22=math.sqrt(1-l21**2)
    LTinv=np.array([[1.0,-l21/l22],[0.0,1.0/l22]])
    Q=LTinv.T@np.array([[0,0.5],[0.5,0]])@LTinv
    c0=(Q[0,0]+Q[1,1])/2; Ac=(Q[0,0]-Q[1,1])/2; Bs=Q[0,1]
    amp=math.hypot(Ac,Bs); phistar=math.atan2(Bs,Ac)/2
    return lam,LTinv,c0,amp,phistar
def ptok(q,phi,E0,lam,w,LTinv,t):
    rho=math.sqrt(E0); y0=rho*math.cos(phi); y1=rho*math.sin(phi)
    a=LTinv[0,0]*y0+LTinv[0,1]*y1; b=LTinv[1,0]*y0+LTinv[1,1]*y1
    ind=(a>0 and a<=1 and b<=1 and b>1-lam*a and a+lam*b>1
         and (w[q-2][0]*a+w[q-2][1]*b>1) and (w[q-1][0]*a+w[q-1][1]*b<=1))
    return ind and (a*b<t)
def fit_count(q,count,frac_lo,frac_hi,nfr=6000):
    """does `count` symmetric-about-phistar lattice pts fit somewhere in [frac_lo,frac_hi]?
    Also allow a phase shift so it's not forced symmetric (general placement).
    We use symmetric (best for straddle) for the hop; for no-notch we also allow general offset."""
    lam,w=hecke_w(q); t=t_of(q); theta=math.pi/q
    lam,LTinv,c0,amp,phistar=whiten(q); mu_max=1/(2-lam)
    half=(count-1)/2.0
    rel=[(-half+i)*theta for i in range(count)]
    for ie in range(nfr):
        frac=frac_lo+(frac_hi-frac_lo)*ie/(nfr-1); E0=frac*t/mu_max
        if all(ptok(q,phistar+r,E0,lam,w,LTinv,t) for r in rel): return True,frac
    return False,None
def B0_nonotch(q):
    # largest count fitting with peak<=t (frac<=1), general offset (not forced symmetric)
    lam,w=hecke_w(q); t=t_of(q); theta=math.pi/q
    lam,LTinv,c0,amp,phistar=whiten(q); mu_max=1/(2-lam); Nrot=2*q+8
    best=0
    n_off=8000
    offs=np.linspace(0,2*math.pi,n_off,endpoint=False); n_idx=np.arange(Nrot)
    PHI=offs[:,None]-n_idx[None,:]*theta
    wq2x,wq2y=w[q-2]; wq1x,wq1y=w[q-1]
    for ie in range(800):
        frac=0.80+0.20*ie/799; E0=frac*t/mu_max; rho=math.sqrt(E0)
        y0=rho*np.cos(PHI); y1=rho*np.sin(PHI)
        a=LTinv[0,0]*y0+LTinv[0,1]*y1; b=LTinv[1,0]*y0+LTinv[1,1]*y1
        wprev=wq2x*a+wq2y*b; wi=wq1x*a+wq1y*b
        ok=((a>0)&(a<=1)&(b<=1)&(b>1-lam*a)&(a+lam*b>1)&(wprev>1)&(wi<=1)&(a*b<t))
        col0=ok[:,0]; ff=np.argmin(ok,axis=1); allT=ok.all(axis=1)
        rl=np.where(col0,np.where(allT,Nrot,ff),0); m=int(rl.max())
        if m>best: best=m
    return best
if __name__=="__main__":
    trueB={7:3,8:3,9:3,10:3,11:3,12:3,13:4,14:4,15:4,16:4,17:4,18:4,19:5,20:5,21:5,22:5,
           23:6,24:6,25:6,26:6,27:6,28:6,29:7,30:7,31:7,32:7,33:8,34:8,35:8,36:8,37:8,38:9,39:9,40:9}
    print("q   B0(nonotch)  parity  hop(B0+1)fits?  predB   trueB  ok?")
    for q in range(7,41):
        B0=B0_nonotch(q)
        par="ODD" if B0%2==1 else "EVEN"
        hopfit,fr=fit_count(q,B0+1,1.0,1.05)
        pred=B0+1 if (B0%2==1 and hopfit) else B0
        ok="OK" if pred==trueB[q] else "MISMATCH"
        print(f"{q:3d}    {B0:3d}       {par:4s}   {str(hopfit):5s} (fr={fr if fr else '-'})   {pred:3d}    {trueB[q]:3d}   {ok}",flush=True)
