"""
dps=50 EXACT confirmation that B(61)>=14 (the predicted resonance):
place 14 lattice pts symmetric about phistar at the gain frac and verify all are
in-domain (last-branch) AND sub-threshold. Also confirm 13 (B0) at frac<1, and that
15 is impossible (parity: odd -> impales peak). Also confirm 2delta<theta at gain frac.
This is the genuine-map cluster (an exact arc of the M-rotation), so a valid placement
== a real length-14 sub-threshold last-branch run exists in the Taha map.
"""
import mpmath as mp
mp.mp.dps=50
def lam_of(q): return 2*mp.cos(mp.pi/q)
def hecke_w(q):
    lam=lam_of(q); w=[(mp.mpf(1),mp.mpf(0))]
    for _ in range(q+3):
        x,y=w[-1]; w.append((lam*x-y,x))
    return lam,w
def setup(q):
    lam=lam_of(q); l21=-lam/2; l22=mp.sqrt(1-l21**2)
    LTinv=mp.matrix([[mp.mpf(1),-l21/l22],[mp.mpf(0),1/l22]])
    S=mp.matrix([[0,mp.mpf(1)/2],[mp.mpf(1)/2,0]]); Q=LTinv.T*S*LTinv
    c0=(Q[0,0]+Q[1,1])/2; Ac=(Q[0,0]-Q[1,1])/2; Bs=Q[0,1]
    amp=mp.sqrt(Ac**2+Bs**2); phistar=mp.atan2(Bs,Ac)/2
    return lam,LTinv,c0,amp,phistar
def ab(LTinv,phi,E0):
    rho=mp.sqrt(E0); y0=rho*mp.cos(phi); y1=rho*mp.sin(phi)
    return LTinv[0,0]*y0+LTinv[0,1]*y1, LTinv[1,0]*y0+LTinv[1,1]*y1
def valid_count(q,count,flo,fhi,nfr=40000):
    lam,w=hecke_w(q); t=1/lam**3; theta=mp.pi/q
    lam,LTinv,c0,amp,phistar=setup(q); mu_max=1/(2-lam)
    half=(count-1)/mp.mpf(2); rel=[(-half+i)*theta for i in range(count)]
    for ie in range(nfr):
        frac=flo+(fhi-flo)*ie/(nfr-1); E0=frac*t/mu_max
        good=True
        for r in rel:
            a,b=ab(LTinv,phistar+r,E0)
            ind=(a>0 and a<=1 and b<=1 and b>1-lam*a and a+lam*b>1
                 and (w[q-2][0]*a+w[q-2][1]*b>1) and (w[q-1][0]*a+w[q-1][1]*b<=1))
            if not(ind and a*b<t): good=False; break
        if good:
            # notch width here
            rhs=(mu_max/frac-c0)/amp; d2=mp.acos(rhs) if rhs<1 else mp.mpf(0)
            return True,frac,d2,theta,t
    return False,None,None,mp.pi/q,1/lam_of(q)**3
if __name__=="__main__":
    q=61
    for count in [13,14,15]:
        ok,frac,d2,theta,t=valid_count(q,count,mp.mpf("0.95"),mp.mpf("1.01"))
        extra=""
        if ok and frac>1: extra=f"  2delta={mp.nstr(d2/theta,5)}*theta (<theta:{d2<theta})"
        print(f"q=61 count={count} ({'EVEN' if count%2==0 else 'ODD'}): fits={ok} frac={mp.nstr(frac,8) if frac else '-'}{extra}")
