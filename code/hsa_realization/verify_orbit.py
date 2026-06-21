import mpmath as mp
mp.mp.dps = 50

def lamq(q): return 2*mp.cos(mp.pi/q)
def Mmap(l,p): a,b=p; return (b, -a + l*b)
def Eform(l,p): a,b=p; return a*a - l*a*b + b*b
def Pgen(l,p): a,b=p; return a*(a+l*b)/l

def consts(q):
    th=mp.pi/q; c=mp.cos(th); s=mp.sin(th); l=2*c
    alpha = 1/(4*c) + 3*c/(4*s**2)
    rho   = mp.sqrt(8*c**2+1)/(4*s**2*c)
    Efloor= 1/(l**3*(alpha+rho*c))
    return th,c,s,l,alpha,rho,Efloor

print("REFERENCE VALUES (sealed Pgen normalization):")
for q in [5,7,22]:
    th,c,s,l,alpha,rho,Efloor=consts(q)
    print(f"q={q} l={mp.nstr(l,8)} alpha={mp.nstr(alpha,8)} rho={mp.nstr(rho,8)} cos={mp.nstr(c,8)} Efloor={mp.nstr(Efloor,8)} 1/l^3={mp.nstr(1/l**3,8)}")

print("\nORBIT-SINUSOID IDENTITY CHECK: Pgen(M^k p) =? C0 + R cos(phi + 2 k theta), C0=alpha E, R=rho E")
import random
for q in [5,7,13,22]:
    th,c,s,l,alpha,rho,Efloor=consts(q)
    # pick a corridor point
    p=(mp.mpf('0.6'), mp.mpf('0.5'))
    E=Eform(l,p)
    C0=alpha*E; R=rho*E
    # determine phi from k=0,1
    P0=Pgen(l,p)
    pk=Mmap(l,p); P1=Pgen(l,pk)
    # P0 = C0 + R cos phi ; P1 = C0 + R cos(phi+2theta)
    cphi=(P0-C0)/R
    # solve sign of sin from P1
    # cos(phi+2th)=cphi*cos2th - sphi*sin2th
    c2=mp.cos(2*th); s2=mp.sin(2*th)
    target1=(P1-C0)/R
    # target1 = cphi*c2 - sphi*s2  => sphi = (cphi*c2 - target1)/s2
    sphi=(cphi*c2-target1)/s2
    phi=mp.atan2(sphi,cphi)
    # now verify k=2..10
    maxerr=mp.mpf(0)
    pp=p
    for k in range(0,12):
        Pk=Pgen(l,pp)
        pred=C0+R*mp.cos(phi+2*k*th)
        maxerr=max(maxerr,abs(Pk-pred))
        pp=Mmap(l,pp)
    print(f"q={q}: E={mp.nstr(E,6)} phi={mp.nstr(phi,6)} max|err| over k=0..11 = {mp.nstr(maxerr,4)}")

# Also confirm phi via closed form: whitening atan2 of (LT^{-T} x)?? scout says phi = -phi0, phi0 = atan2 of whitened coords.
print("\nPHASE closed-form check (phi = atan2 from whitened B-form):")
for q in [5,7,13]:
    th,c,s,l,alpha,rho,Efloor=consts(q)
    p=(mp.mpf('0.6'), mp.mpf('0.5')); a,b=p
    E=Eform(l,p)
    # whitened u = LT x, LT=[[1,-c],[0,s]]
    u1=a-c*b; u2=s*b
    psi=mp.atan2(u2,u1)
    # B-form: Pgen = E*(alpha + (B11-B22)/2 cos2psi + B12 sin2psi)
    # = E*(alpha + Rcoeff cos(2psi - delta)) with delta=atan2(2B12,(B11-B22))
    B11=1/(2*c); B12=1/s; B22=3*c/(2*s**2)
    delta=mp.atan2(2*B12,(B11-B22))
    pred=E*(alpha+rho*mp.cos(2*psi-delta))
    print(f"q={q}: Pgen(p)={mp.nstr(Pgen(l,p),8)} vs E*(alpha+rho cos(2psi-delta))={mp.nstr(pred,8)} (phi0=2psi-delta scaled)")
