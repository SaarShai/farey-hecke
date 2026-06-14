import math,sys
import numpy as np
def lam_of(q): return 2.0*math.cos(math.pi/q)
def hecke_w(q):
    lam=lam_of(q); w=[(1.0,0.0)]
    for _ in range(q+3):
        x,y=w[-1]; w.append((lam*x-y,x))
    return lam,w
def whiten(q):
    lam=lam_of(q); l21=-lam/2; l22=math.sqrt(1-l21**2)
    return np.array([[1.0,-l21/l22],[0.0,1/l22]])
def Bq(q,n_E0=900,n_off=7000):
    lam,w=hecke_w(q); t=1.0/lam**3; th=math.pi/q; LT=whiten(q); Nrot=2*q+10
    offs=np.linspace(0,2*math.pi,n_off,endpoint=False); ni=np.arange(Nrot)
    PHI=offs[:,None]-ni[None,:]*th; cp=np.cos(PHI); sp=np.sin(PHI)
    wq2x,wq2y=w[q-2]; wq1x,wq1y=w[q-1]; mu=1.0/(2-lam)
    best=0
    for fr in np.linspace(0.82,1.10,n_E0):
        E0=fr*t/mu; rho=math.sqrt(E0)
        a=rho*(LT[0,0]*cp+LT[0,1]*sp); b=rho*(LT[1,0]*cp+LT[1,1]*sp)
        wp=wq2x*a+wq2y*b; wi=wq1x*a+wq1y*b
        ok=((a>0)&(a<=1)&(b<=1)&(b>1-lam*a)&(a+lam*b>1)&(wp>1)&(wi<=1)&(a*b<t))
        col0=ok[:,0]; ff=np.argmin(ok,axis=1); allT=ok.all(axis=1)
        rl=np.where(col0,np.where(allT,Nrot,ff),0); m=int(rl.max())
        if m>best: best=m
    return best
def Wq(q,Ngrid=400000):
    lam=lam_of(q); LT=whiten(q); _,w=hecke_w(q); t=1.0/lam**3
    E0=(1.0-1e-9)*t/(1.0/(2-lam)); rho=math.sqrt(E0)
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
for q in range(int(sys.argv[1]),int(sys.argv[2])+1):
    B=Bq(q); W=Wq(q); wqp=W*q/math.pi; P1=int(math.floor(wqp))+1
    print(f"D8 {q} {B} {wqp:.6f} {P1} {2+(q-1)//6}",flush=True)
