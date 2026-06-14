"""
For each q, compute the EXACT geometric resonance predictor at high precision (mpmath):
On the conserved ellipse, parametrize by whitened phase phi. P(phi)=E0*g(phi),
g(phi)=c0+amp*cos(2(phi-phi*)), with the last-branch domain an arc [phiL,phiR].
The sub-threshold condition P<t carves arcs. At the governing ellipse where peak ab can
exceed t, a super-threshold NOTCH of angular half-width delta opens at the symmetric point.
RESONANCE = the -pi/q grid can place a point on each side of the notch w/o landing inside,
gaining +1 over floor(W q/pi)+1.

We compute, at the resonance-optimal ellipse (peak ab slightly > t), the notch angular width
delta(q) and compare to grid step s=pi/q. Resonance is POSSIBLE only when delta < s, and then
realized for the right offset. We report delta*q/pi (notch in grid units) and whether B>P1.
This isolates the arithmetic content: resonance <=> a grid point misses the notch arc.
"""
import math, sys
import mpmath as mp
mp.mp.dps=40

def lam_of(q): return 2*mp.cos(mp.pi/q)
def hecke_w(q):
    lam=lam_of(q); w=[(mp.mpf(1),mp.mpf(0))]
    for _ in range(q+3):
        x,y=w[-1]; w.append((lam*x-y,x))
    return lam,w
def setup(q):
    lam=lam_of(q); l21=-lam/2; l22=mp.sqrt(1-l21**2)
    LTinv=[[mp.mpf(1),-l21/l22],[mp.mpf(0),1/l22]]
    def coords(phi,E0):
        rho=mp.sqrt(E0); y0=rho*mp.cos(phi); y1=rho*mp.sin(phi)
        return LTinv[0][0]*y0+LTinv[0][1]*y1, LTinv[1][0]*y0+LTinv[1][1]*y1
    return lam,coords

def arc_pts(q, frac, Ngrid=4000):
    """return list of (phi, in-subthreshold-LB-domain bool) over a fine phi grid; find arcs."""
    lam,coords=setup(q); _,w=lam_of(q),hecke_w(q)[1]; t=1/lam**3
    mu_max=1/(2-lam); E0=frac*t/mu_max
    inb=[]
    for i in range(Ngrid):
        phi=2*mp.pi*i/Ngrid
        a,b=coords(phi,E0)
        ok=(a>0 and a<=1 and b<=1 and b>1-lam*a and a+lam*b>1
            and (w[q-2][0]*a+w[q-2][1]*b>1) and (w[q-1][0]*a+w[q-1][1]*b<=1) and a*b<t)
        inb.append(ok)
    return inb

def max_grid_in_arcs(q, frac, n_off=20000, Ngrid=6000):
    """exact discrete count at this frac, high-res: max over offset of #grid pts in subthr-LB region."""
    lam,coords=setup(q); _,w=lam_of(q),hecke_w(q)[1]; t=1/lam**3
    mu_max=1/(2-lam); E0=frac*t/mu_max
    theta=mp.pi/q; Nrot=2*q+12
    best=0
    # coarse offset scan; for each, count consecutive from n=0
    import numpy as np
    offs=np.linspace(0,float(2*mp.pi),n_off,endpoint=False)
    # precompute float coords fast
    lamf=float(lam); l21=-lamf/2; l22=math.sqrt(1-l21**2)
    LT00=1.0;LT01=-l21/l22;LT11=1/l22
    E0f=float(E0); rho=math.sqrt(E0f); tf=float(t)
    wq2=(float(w[q-2][0]),float(w[q-2][1])); wq1=(float(w[q-1][0]),float(w[q-1][1]))
    th=math.pi/q
    n_idx=np.arange(Nrot)
    PHI=offs[:,None]-n_idx[None,:]*th
    cp=np.cos(PHI);sp=np.sin(PHI)
    a=rho*(LT00*cp+LT01*sp); b=rho*(LT11*sp)
    wprev=wq2[0]*a+wq2[1]*b; wi=wq1[0]*a+wq1[1]*b
    ok=((a>0)&(a<=1)&(b<=1)&(b>1-lamf*a)&(a+lamf*b>1)&(wprev>1)&(wi<=1)&(a*b<tf))
    col0=ok[:,0]; ff=np.argmin(ok,axis=1); allT=ok.all(axis=1)
    rl=np.where(col0,np.where(allT,Nrot,ff),0)
    return int(rl.max())

if __name__=="__main__":
    qs=[int(x) for x in sys.argv[1:]]
    print("q   bestB  best_frac   notch?(peak>t reachable)")
    for q in qs:
        # scan frac near 1 to find the B-maximizing frac and whether peak>t needed
        bestB=0; bestfr=None
        fr=mp.mpf("0.95")
        import numpy as np
        for fri in np.linspace(0.95,1.08,260):
            B=max_grid_in_arcs(q,mp.mpf(str(fri)))
            if B>bestB: bestB=B; bestfr=fri
        # peak ab at bestfr = bestfr * t ; >t means notch present
        print(f"{q:3d}  {bestB:4d}   {bestfr:.4f}   {'NOTCH(peak>t)' if bestfr>1.0 else 'no-notch'}", flush=True)
