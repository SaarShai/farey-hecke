"""
dps=50 confirmation of the PARITY mechanism at the two cleanest cases:
  q=23: s=4.969 -> approaches ODD integer 5 -> B0=5 ODD -> +1 target 6 EVEN ->
        symmetric straddle places center GAP on notch -> HOP succeeds -> B=6.
  q=47: s=9.997 -> approaches EVEN integer 10 -> B0=10 EVEN -> +1 target 11 ODD ->
        symmetric placement puts a point ON the peak (notch) -> blocked -> B=10,
        despite arc being only 0.003*theta short of fitting an 11th point.
We dump, for each, the best symmetric placement of the +1 target count and show:
  - q=23: the 6 points straddle phistar (none at phistar), all sub-thr+LB.
  - q=47: the 11 points (odd) force one point AT phistar where P>t (in notch) -> invalid.
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
def valid(q,phi,E0,lam,w,LTinv,t):
    a,b=ab(LTinv,phi,E0)
    ind=(a>0 and a<=1 and b<=1 and b>1-lam*a and a+lam*b>1
         and (w[q-2][0]*a+w[q-2][1]*b>1) and (w[q-1][0]*a+w[q-1][1]*b<=1))
    return ind,(a*b<t),a*b
def test(q,count,frac):
    lam,w=hecke_w(q); t=1/lam**3; theta=mp.pi/q
    lam,LTinv,c0,amp,phistar=setup(q); mu_max=1/(2-lam); E0=frac*t/mu_max
    half=(count-1)/mp.mpf(2)
    print(f"  q={q} count={count} frac={mp.nstr(frac,8)} (parity of count: {'ODD' if count%2 else 'EVEN'})")
    allok=True
    for i in range(count):
        rel=(-half+i)*theta
        phi=phistar+rel
        ind,sub,P=valid(q,phi,E0,lam,w,LTinv,t)
        ok=ind and sub
        allok=allok and ok
        onpeak = abs(rel)<theta/4
        tag=" <== ON PEAK (notch)" if onpeak else ""
        print(f"    rel={mp.nstr(rel/theta,5)}*th  P={mp.nstr(P,8)} (t-P={mp.nstr(t-P,3)}) LB={ind} sub={sub} {'OK' if ok else 'FAIL'}{tag}")
    print(f"    => placement {'VALID (all pts in-domain+sub-thr)' if allok else 'INVALID'}\n")
if __name__=="__main__":
    # q=23: target 6 (even) at the gain frac
    test(23,6,mp.mpf("1.00163"))
    # q=47: target 11 (odd) - try the frac that maximizes arc (just below where 11th would fit)
    test(47,11,mp.mpf("1.0005"))
    # also show q=47 target 10 (even) fits fine at frac<1
    test(47,10,mp.mpf("0.985"))
