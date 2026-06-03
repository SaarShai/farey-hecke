"""Cross-check computed mod-8 zeros against direct mpmath L-function eval.
The three primitive real chars mod 8 are:
 - chi_8 (the even one, conductor 8, chi(-1)=+1, kronecker (2/n)-ish): first zero ~?
 - chi_{-8} (odd, chi(-1)=-1)
 - chi_{-4}*... actually mod 8 chars: principal, chi_-4(induced), chi_8, chi_-8.
Let's just independently locate the first zero of each by scanning |L| and
confirm L(1/2+i gamma)=0 to high precision.
"""
import mpmath as mp
mp.mp.dps=30
from get_zeros import char_table, L_chi
N=8
U,ge,go,coords,chars,cval=char_table(N)
for k in chars:
    if all(x==0 for x in k): continue
    # first zero scan
    g=None
    t=mp.mpf('0.2')
    while t<8:
        z=mp.findroot(lambda tt:L_chi(mp.mpf('0.5')+1j*tt,k,N,cval,U), t, tol=1e-20) if abs(L_chi(mp.mpf('0.5')+1j*t,k,N,cval,U))<1.0 else None
        if z is not None and mp.re(z)>0.1 and abs(L_chi(mp.mpf('0.5')+1j*mp.re(z),k,N,cval,U))<1e-12:
            g=mp.re(z); break
        t+=mp.mpf('0.1')
    chi_m1=cval(k,N-1)
    val=L_chi(mp.mpf('0.5')+1j*g,k,N,cval,U) if g else None
    print(f"chi_{k} chi(-1)={complex(chi_m1).real:+.0f}  first gamma={float(g):.6f}  |L(1/2+ig)|={float(abs(val)):.2e}")
# Known: L-function mod 8 even real character (chi_8) first zero ~ 6.0207...
# odd char chi_-8 first zero ~ 3.576..., chi_-4 induced first zero ~?
