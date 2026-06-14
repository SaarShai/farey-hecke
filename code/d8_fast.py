"""
Fast exact B(q) discrete rotation-arc count + continuous proxies, q-range from argv.
Optimized: vectorize over (E0, offset) and compute run-from-col0 via cumulative-AND argmin.
Outputs CSV: q,B,Wq_q_over_pi,P1,P2 to stdout (one line per q, prefixed 'D8 ').
"""
import math, sys
import numpy as np

def lam_of(q): return 2.0*math.cos(math.pi/q)
def t_of(q):   return 1.0/lam_of(q)**3
def hecke_w(q):
    lam=lam_of(q); w=[(1.0,0.0)]
    for _ in range(q+3):
        x,y=w[-1]; w.append((lam*x-y,x))
    return lam,w
def whiten_LTinv(q):
    lam=lam_of(q); l11=1.0; l21=-lam/2; l22=math.sqrt(1-l21**2); det=l11*l22
    return np.array([[l22/det,-l21/det],[0.0,l11/det]])

def Bq_discrete(q, n_E0=1400, n_off=10000):
    lam,w=hecke_w(q); t=t_of(q); theta=math.pi/q
    LTinv=whiten_LTinv(q); Nrot=2*q+10
    offs=np.linspace(0,2*math.pi,n_off,endpoint=False)
    n_idx=np.arange(Nrot)
    PHI=offs[:,None]-n_idx[None,:]*theta
    cosP=np.cos(PHI); sinP=np.sin(PHI)
    wq2x,wq2y=w[q-2]; wq1x,wq1y=w[q-1]
    mu_max=1.0/(2-lam)
    best=0
    fracs=0.80+0.30*np.arange(n_E0)/(n_E0-1)   # peak ab in [0.80t, 1.10t]
    for frac in fracs:
        E0=frac*t/mu_max; rho=math.sqrt(E0)
        a=rho*(LTinv[0,0]*cosP+LTinv[0,1]*sinP)
        b=rho*(LTinv[1,0]*cosP+LTinv[1,1]*sinP)
        wprev=wq2x*a+wq2y*b; wi=wq1x*a+wq1y*b
        ok=((a>0)&(a<=1)&(b<=1)&(b>1-lam*a)&(a+lam*b>1)&(wprev>1)&(wi<=1)&(a*b<t))
        col0=ok[:,0]
        firstFalse=np.argmin(ok,axis=1)
        allTrue=ok.all(axis=1)
        runlen=np.where(col0, np.where(allTrue,Nrot,firstFalse),0)
        m=int(runlen.max())
        if m>best: best=m
    return best

def Wq_continuous(q, Ngrid=600000):
    lam=lam_of(q); l21=-lam/2; l22=math.sqrt(1-l21**2)
    LTinv=np.array([[1.0,-l21/l22],[0.0,1/l22]])
    _,w=hecke_w(q); t=1.0/lam**3
    frac=1.0-1e-8; E0=frac*t/(1.0/(2-lam)); rho=math.sqrt(E0)
    phi=np.linspace(0,2*math.pi,Ngrid,endpoint=False)
    a=rho*(LTinv[0,0]*np.cos(phi)+LTinv[0,1]*np.sin(phi))
    b=rho*(LTinv[1,0]*np.cos(phi)+LTinv[1,1]*np.sin(phi))
    wq2x,wq2y=w[q-2]; wq1x,wq1y=w[q-1]
    wprev=wq2x*a+wq2y*b; wi=wq1x*a+wq1y*b
    ok=((a>0)&(a<=1)&(b<=1)&(b>1-lam*a)&(a+lam*b>1)&(wprev>1)&(wi<=1)&(a*b<t))
    # longest contiguous True with wrap via run encoding
    if ok.all(): return 2*math.pi
    d=np.diff(np.concatenate([[0],ok.view(np.int8),[0]]))
    starts=np.where(d==1)[0]; ends=np.where(d==-1)[0]
    runs=ends-starts
    # wrap: if first and last cells both True, merge
    best=runs.max() if len(runs) else 0
    if ok[0] and ok[-1] and len(runs)>=2:
        best=max(best, runs[0]+runs[-1])
    return best*2*math.pi/Ngrid

if __name__=="__main__":
    qlo=int(sys.argv[1]); qhi=int(sys.argv[2])
    for q in range(qlo,qhi+1):
        B=Bq_discrete(q); W=Wq_continuous(q); wqp=W*q/math.pi
        P1=int(math.floor(wqp))+1; P2=2+(q-1)//6
        print(f"D8 {q} {B} {wqp:.6f} {P1} {P2}", flush=True)
