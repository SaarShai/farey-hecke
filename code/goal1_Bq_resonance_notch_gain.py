"""
goal1_Bq_resonance_notch_gain.py
For each q, determine whether the NOTCH regime (peak ab > t, frac>1) gains an extra
discrete step over the no-notch regime (peak ab <= t, frac<=1).

B_nonotch(q) = max discrete count over E0 with frac<=1 (peak ab <= t, NO super-thr notch).
B_notch(q)   = max discrete count over ALL E0 (incl frac>1, peak pokes above t).
notch_gain(q)= B_notch - B_nonotch  (0 or 1).

A "resonance" in the strict sense = notch_gain==1 : the lattice hops the notch to gain a step.
EMPIRICAL RESULT (q=7..39): gain == +1 ONLY at q=23 (the rest: optimum at frac<1).
The gatekeeper is PARITY of B_nonotch (odd -> even target straddles peak gap -> hop OK).
See research_notes/resonance_threedistance_2026-06-14.md.
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
    lam=lam_of(q); l21=-lam/2; l22=math.sqrt(1-l21**2)
    return np.array([[l22/l22,-l21/l22],[0.0,1.0/l22]])

def maxrun(q,frac_lo,frac_hi,n_E0=800,n_off=8000):
    lam,w=hecke_w(q); t=t_of(q); theta=math.pi/q; LTinv=whiten_LTinv(q)
    mu_max=1/(2-lam); Nrot=2*q+8
    offs=np.linspace(0,2*math.pi,n_off,endpoint=False)
    n_idx=np.arange(Nrot)
    PHI=offs[:,None]-n_idx[None,:]*theta
    wq2x,wq2y=w[q-2]; wq1x,wq1y=w[q-1]
    best=0; bestfrac=None
    for ie in range(n_E0):
        frac=frac_lo+(frac_hi-frac_lo)*ie/(n_E0-1); E0=frac*t/mu_max; rho=math.sqrt(E0)
        y0=rho*np.cos(PHI); y1=rho*np.sin(PHI)
        a=LTinv[0,0]*y0+LTinv[0,1]*y1; b=LTinv[1,0]*y0+LTinv[1,1]*y1
        wprev=wq2x*a+wq2y*b; wi=wq1x*a+wq1y*b
        ok=((a>0)&(a<=1)&(b<=1)&(b>1-lam*a)&(a+lam*b>1)&(wprev>1)&(wi<=1)&(a*b<t))
        col0=ok[:,0]; firstFalse=np.argmin(ok,axis=1); allTrue=ok.all(axis=1)
        runlen=np.where(col0,np.where(allTrue,Nrot,firstFalse),0)
        m=int(runlen.max())
        if m>best: best=m; bestfrac=frac
    return best,bestfrac

if __name__=="__main__":
    qs=[int(x) for x in sys.argv[1:]] or list(range(7,41))
    print("q   B_nonotch(frac<=1)  B_notch(all)  gain  bestfrac_notch")
    for q in qs:
        Bnn,_=maxrun(q,0.80,1.0000)
        Bn,fr=maxrun(q,0.80,1.10)
        gain=Bn-Bnn
        flag="*** GAIN" if gain>0 else ""
        print(f"{q:3d}    {Bnn:3d}              {Bn:3d}        {gain}   {fr:.4f}  {flag}",flush=True)
