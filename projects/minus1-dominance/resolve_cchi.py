"""
Resolve c_chi = sum_gamma 1/(1/4+gamma^2) cleanly using a CORRECT zero finder.

For the Dirichlet beta function L(s,chi_4) the nontrivial zeros on the critical
line have well-documented imaginary parts:
   gamma_1 = 6.020948..., gamma_2 = 10.243770..., gamma_3 = 12.988098...,
   gamma_4 = 16.342940..., gamma_5 = 18.291916..., ...   (Spira; LMFDB)
We use mpmath to find them as zeros of L(1/2+it,chi_4) directly (real & imag both
vanish at a true zero), and sum 1/(1/4+gamma^2).

Then compare to candidate analytic formulas to find which constant is right.
"""
import mpmath as mp
mp.mp.dps = 30
import math

def chi4(n):
    n%=4; return {1:1,3:-1}.get(n,0)
def chi3(n):
    n%=3; return {1:1,2:-1}.get(n,0)

def Lval(chi,q,s):
    return sum(chi(r)*mp.zeta(s,mp.mpf(r)/q) for r in range(1,q+1))*mp.power(q,-s)

# Robust zero finding: scan |L(1/2+it)| for local minima ~0, refine with findroot on COMPLEX L.
def find_zeros(chi,q,Tmax,step=0.25):
    zeros=[]
    ts=[mp.mpf(i)*mp.mpf(step) for i in range(1,int(Tmax/step)+1)]
    vals=[Lval(chi,q,mp.mpc(0.5,t)) for t in ts]
    for i in range(1,len(ts)-1):
        # bracket where real part changes sign AND magnitude small -> candidate
        if mp.re(vals[i-1])*mp.re(vals[i])<0:
            try:
                z=mp.findroot(lambda t: Lval(chi,q,mp.mpc(0.5,t)), ts[i])
                g=mp.re(z)
                if g>0.01 and all(abs(g-z2)>1e-6 for z2 in zeros) and abs(mp.im(z))<1e-6:
                    # verify it's actually a zero
                    if abs(Lval(chi,q,mp.mpc(0.5,g)))<1e-8:
                        zeros.append(g)
            except: pass
    return sorted(zeros)

z4=find_zeros(chi4,4,50)
z3=find_zeros(chi3,3,50)
print("chi4 zeros:",[mp.nstr(g,8) for g in z4])
print("  expected: 6.020948,10.243770,12.988098,16.342940,18.291916,...")
print("chi3 zeros:",[mp.nstr(g,8) for g in z3])
print("  expected: 8.039737,11.249193,15.704619,...")

def csum(zs,q,Tmax):
    s=2*sum(1/(mp.mpf(1)/4+g**2) for g in zs)  # +/- pairs
    # tail: density of zeros for L(s,chi) mod q near height T ~ (1/pi)log(qT/2pi)
    tail=2*mp.quad(lambda t:(1/mp.pi)*mp.log(q*t/(2*mp.pi))/(mp.mpf(1)/4+t**2),[Tmax,mp.inf])
    return s,tail

s4,t4=csum(z4,4,50); s3,t3=csum(z3,3,50)
print(f"\nc_chi4 = {mp.nstr(s4,9)} (|g|<50) + tail {mp.nstr(t4,4)} = {mp.nstr(s4+t4,9)}")
print(f"c_chi3 = {mp.nstr(s3,9)} (|g|<50) + tail {mp.nstr(t3,4)} = {mp.nstr(s3+t3,9)}")

# Candidate analytic formulas for c_chi:
def LpL(chi,q,s): return mp.diff(lambda z:mp.log(Lval(chi,q,z)),s,h=mp.mpf('1e-10'))
for chi,q,even,nm in [(chi4,4,False,'chi4'),(chi3,3,False,'chi3')]:
    a=0 if even else 1
    s1=mp.mpf(1)
    LL=mp.re(LpL(chi,q,s1+mp.mpf('1e-15')))
    # candidate 1: log(q/pi)+psi((1+a)/2)+2 L'/L(1)
    c1=mp.log(mp.mpf(q)/mp.pi)+mp.digamma((1+a)/mp.mpf(2))+2*LL
    # candidate 2: with factor 1/2 on arch
    c2=0.5*(mp.log(mp.mpf(q)/mp.pi)+mp.digamma((1+a)/mp.mpf(2)))+2*LL
    # candidate 3: B(chi) + L'/L(1) form -> 2*(0.5 log(q/pi)+0.5 psi + L'/L(1))
    c3=mp.log(mp.mpf(q)/mp.pi)+mp.digamma((mp.mpf(1)+a)/2)+2*LL
    print(f"{nm}: L'/L(1)={mp.nstr(LL,7)}  cand1={mp.nstr(c1,7)} cand2={mp.nstr(c2,7)}")
