"""
Fast: compute s(q)=W(q)*q/pi for q=55..70 (just W, no Bdisc grid), find where
s approaches an ODD integer (13) from below = candidate resonance. Then run the
focused symmetric-placement HOP test (fast) to confirm B=B0+1 there, and check the
non-candidates give B=B0.
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
def Wcont(q,N=4_000_000,frac=0.9999995):
    lam,w=hecke_w(q); t=t_of(q); lam,LTinv,c0,amp,phistar=whiten(q)
    mu_max=1/(2-lam); E0=frac*t/mu_max; rho=math.sqrt(E0)
    phi=np.linspace(0,2*math.pi,N,endpoint=False)
    y0=rho*np.cos(phi); y1=rho*np.sin(phi)
    a=LTinv[0,0]*y0+LTinv[0,1]*y1; b=LTinv[1,0]*y0+LTinv[1,1]*y1
    wq2x,wq2y=w[q-2]; wq1x,wq1y=w[q-1]
    wprev=wq2x*a+wq2y*b; wi=wq1x*a+wq1y*b
    ok=((a>0)&(a<=1)&(b<=1)&(b>1-lam*a)&(a+lam*b>1)&(wprev>1)&(wi<=1)&(a*b<t))
    ok2=np.concatenate([ok,ok]); best=0;cur=0
    for v in ok2:
        if v: cur+=1; best=max(best,cur)
        else: cur=0
    return best*2*math.pi/N
def ptok(q,phi,E0,lam,w,LTinv,t):
    rho=math.sqrt(E0); y0=rho*math.cos(phi); y1=rho*math.sin(phi)
    a=LTinv[0,0]*y0+LTinv[0,1]*y1; b=LTinv[1,0]*y0+LTinv[1,1]*y1
    ind=(a>0 and a<=1 and b<=1 and b>1-lam*a and a+lam*b>1
         and (w[q-2][0]*a+w[q-2][1]*b>1) and (w[q-1][0]*a+w[q-1][1]*b<=1))
    return ind and (a*b<t)
def fit_sym(q,count,flo,fhi,nfr=12000):
    lam,w=hecke_w(q); t=t_of(q); theta=math.pi/q
    lam,LTinv,c0,amp,phistar=whiten(q); mu_max=1/(2-lam)
    half=(count-1)/2.0; rel=[(-half+i)*theta for i in range(count)]
    for ie in range(nfr):
        frac=flo+(fhi-flo)*ie/(nfr-1); E0=frac*t/mu_max
        if all(ptok(q,phistar+r,E0,lam,w,LTinv,t) for r in rel): return True,frac
    return False,None
if __name__=="__main__":
    qs=[int(x) for x in sys.argv[1:]] or list(range(55,69))
    print("q   s(q)      frac(s)  B0   par(B0)  hop(B0+1,sym)?  predB")
    for q in qs:
        W=Wcont(q); s=W*q/math.pi; fr=s-math.floor(s); B0=int(math.floor(s))+1
        par="ODD" if B0%2 else "EVEN"
        # only attempt hop if parity allows (B0 odd) -- but test anyway for honesty
        hop,frac=fit_sym(q,B0+1,1.0,1.04)
        pred=B0+1 if (B0%2==1 and hop) else B0
        flag="*** RES" if pred>B0 else ""
        print(f"{q:3d}  {s:.5f}  {fr:.4f}  {B0:3d}   {par:4s}   {str(hop):5s}(fr={frac if frac else '-'})   {pred:3d} {flag}",flush=True)
