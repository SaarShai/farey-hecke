"""
High-precision verification of resonance candidates: for given q, compute
  - B(q) via very fine discrete grid (n_E0=3000, n_off=40000)
  - W(q) via very fine continuous grid + the fractional part {W*q/pi}
and report B, floor(Wq/pi)+1, deviation, and frac part.
Also dump the resonance frac (peak/t) at which B is realized.
"""
import math, sys
import numpy as np

def lam_of(q): return 2.0*math.cos(math.pi/q)
def t_of(q): return 1.0/lam_of(q)**3
def hecke_w(q):
    lam=lam_of(q); w=[(1.0,0.0)]
    for _ in range(q+3):
        x,y=w[-1]; w.append((lam*x-y,x))
    return lam,w
def whiten(q):
    lam=lam_of(q); l21=-lam/2; l22=math.sqrt(1-l21**2)
    return np.array([[1.0,-l21/l22],[0.0,1/l22]])

def Bq(q,n_E0=3000,n_off=40000,flo=0.80,fhi=1.12):
    lam,w=hecke_w(q); t=t_of(q); th=math.pi/q; LT=whiten(q); Nrot=2*q+12
    offs=np.linspace(0,2*math.pi,n_off,endpoint=False); ni=np.arange(Nrot)
    PHI=offs[:,None]-ni[None,:]*th; cp=np.cos(PHI); sp=np.sin(PHI)
    wq2x,wq2y=w[q-2]; wq1x,wq1y=w[q-1]; mu=1.0/(2-lam)
    best=0; bestfr=None
    for fr in np.linspace(flo,fhi,n_E0):
        E0=fr*t/mu; rho=math.sqrt(E0)
        a=rho*(LT[0,0]*cp+LT[0,1]*sp); b=rho*(LT[1,0]*cp+LT[1,1]*sp)
        wp=wq2x*a+wq2y*b; wi=wq1x*a+wq1y*b
        ok=((a>0)&(a<=1)&(b<=1)&(b>1-lam*a)&(a+lam*b>1)&(wp>1)&(wi<=1)&(a*b<t))
        col0=ok[:,0]; ff=np.argmin(ok,axis=1); allT=ok.all(axis=1)
        rl=np.where(col0,np.where(allT,Nrot,ff),0); m=int(rl.max())
        if m>best: best=m; bestfr=fr
    return best,bestfr

def Wq(q,Ngrid=3000000):
    lam=lam_of(q); LT=whiten(q); _,w=hecke_w(q); t=1.0/lam**3
    frac=1.0-1e-9; E0=frac*t/(1.0/(2-lam)); rho=math.sqrt(E0)
    phi=np.linspace(0,2*math.pi,Ngrid,endpoint=False)
    a=rho*(LT[0,0]*np.cos(phi)+LT[0,1]*np.sin(phi)); b=rho*(LT[1,0]*np.cos(phi)+LT[1,1]*np.sin(phi))
    wq2x,wq2y=w[q-2]; wq1x,wq1y=w[q-1]
    wp=wq2x*a+wq2y*b; wi=wq1x*a+wq1y*b
    ok=((a>0)&(a<=1)&(b<=1)&(b>1-lam*a)&(a+lam*b>1)&(wp>1)&(wi<=1)&(a*b<t))
    if ok.all(): return 2*math.pi
    d=np.diff(np.concatenate([[0],ok.view(np.int8),[0]]))
    s=np.where(d==1)[0]; e=np.where(d==-1)[0]; runs=e-s
    best=runs.max() if len(runs) else 0
    if ok[0] and ok[-1] and len(runs)>=2: best=max(best,runs[0]+runs[-1])
    return best*2*math.pi/Ngrid

if __name__=="__main__":
    for q in [int(x) for x in sys.argv[1:]]:
        B,fr=Bq(q); W=Wq(q); wqp=W*q/math.pi
        P1=int(math.floor(wqp))+1
        print(f"q={q:3d}  B={B}  Wq*q/pi={wqp:.5f}  frac={{{wqp-math.floor(wqp):.4f}}}  floor+1={P1}  dev={B-P1:+d}  bestfrac(peak/t)={fr:.4f}  {'RES' if B>P1 else ('ANTI' if B<P1 else '')}", flush=True)
