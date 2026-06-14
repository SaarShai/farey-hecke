"""
Analytic structure of the governing arc width W(q) and its q->oo limit.

On E=E0, peak ab = E0/(2-lam) (at symmetric pt a=b).  Governing ellipse: peak ab = t
=> E0 = t*(2-lam) = (2-lam)/lam^3.  At this E0 the symmetric point a=b sits exactly AT
threshold; the sub-threshold last-branch arc is bounded by the DOMAIN lower edges
(Taha last-branch: a+lam*b>1 and the branch test w_{q-2}.(a,b)>1, w_{q-1}.(a,b)<=1),
NOT by the ab<t cut (which only excludes the single peak).

The two governing edges turn out to be the lines through which the arc exits the
last-branch corridor.  We compute W(q) = angular span (in whitened phase) of the
last-branch sub-threshold arc at E0=(2-lam)/lam^3, and its limit.

We also give the limiting arc-FRACTION  c* = W_inf/(2pi)  and slope  W_inf/pi.
"""
import mpmath as mp
mp.mp.dps = 40
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
        rho=mp.sqrt(E0);y0=rho*mp.cos(phi);y1=rho*mp.sin(phi)
        return LTinv[0][0]*y0+LTinv[0][1]*y1, LTinv[1][0]*y0+LTinv[1][1]*y1
    return lam,coords
def Wq(q,frac=mp.mpf("0.99999"),Ngrid=200000):
    lam,coords=setup(q);_,w=lam_of(q),hecke_w(q)[1]; t=1/lam**3
    mu_max=1/(2-lam);E0=frac*t/mu_max
    # find longest contiguous in-domain last-branch sub-thr arc
    best=0;cur=0
    arr=[]
    for i in range(2*Ngrid):
        phi=2*mp.pi*i/Ngrid
        a,b=coords(phi,E0)
        ok=(a>0 and a<=1 and b<=1 and b>1-lam*a and a+lam*b>1
            and (w[q-2][0]*a+w[q-2][1]*b>1) and (w[q-1][0]*a+w[q-1][1]*b<=1) and a*b<t)
        if ok:cur+=1;best=max(best,cur)
        else:cur=0
    return best*2*mp.pi/Ngrid
if __name__=="__main__":
    print("q     W(q) rad    W*q/pi    floor+1    arc-frac W/2pi")
    for q in [7,13,19,23,24,30,40,60,100,200,500,1000]:
        N=80000 if q>=100 else 150000
        W=Wq(q,Ngrid=N)
        print(f"{q:4d}  {mp.nstr(W,8)}  {mp.nstr(W*q/mp.pi,7)}  {int(mp.floor(W*q/mp.pi))+1:3d}     {mp.nstr(W/(2*mp.pi),6)}",flush=True)
