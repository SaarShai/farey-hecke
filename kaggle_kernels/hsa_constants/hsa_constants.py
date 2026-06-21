"""
Pin the pgen_orbit_realization constants for hSuperArc (Farey-Hecke).

Sealed defs (verbatim):
  Mmap l (a,b) = (b, -a + l*b)
  Eform l (a,b) = a^2 - l*a*b + b^2          (conserved by Mmap)
  Pgen l (a,b) = a*(a + l*b)/l
  l = lamq q = 2 cos(pi/q),  theta = pi/q,  c=cos, s=sin.

Claim (1a, the realization core):  along the orbit p_k = Mmap^[k] p,
  Pgen(p_k) = C0 + R cos(phi + 2 k theta),   C0 = alpha*E, R = rho*E, E = Eform l p,
with l-only constants
  alpha = 1/(4c) + 3c/(4 s^2)
  rho   = sqrt(8 c^2 + 1)/(4 s^2 c)
and Efloor = 1/(l^3 (alpha + rho c)).

Also pins the DISTINCT L1b Fobs constants (Fobs = 3l/2 + sqrt(1+2 l^2) cos),
mean 3l/(4 A2), amp 1/(2 sqrt A2), A2 = 1+2 l^2, and verifies alpha != mean_L1b,
rho != amp_L1b. Outputs to /kaggle/working.
"""
import mpmath as mp
import json, os
mp.mp.dps = 60

def consts(q):
    th = mp.pi/q; c = mp.cos(th); s = mp.sin(th); l = 2*c
    alpha = 1/(4*c) + 3*c/(4*s**2)
    rho   = mp.sqrt(8*c**2 + 1)/(4*s**2*c)
    Efloor = 1/(l**3*(alpha + rho*c))
    A2 = 1 + 2*l**2
    mean_L1b = 3*l/(4*A2)
    amp_L1b  = 1/(2*mp.sqrt(A2))
    return dict(th=th,c=c,s=s,l=l,alpha=alpha,rho=rho,Efloor=Efloor,
                A2=A2,mean_L1b=mean_L1b,amp_L1b=amp_L1b)

def Mmap(l,p): a,b=p; return (b,-a+l*b)
def Eform(l,p): a,b=p; return a*a-l*a*b+b*b
def Pgen(l,p): a,b=p; return a*(a+l*b)/l

results = {}
qs = [3,4,5,6,7,8,10,13,18,22,40,100]

print("="*70)
print("RAW-Pgen realization constants (sealed Pgen l (a,b)=a(a+lb)/l)")
print("="*70)
for q in qs:
    C = consts(q)
    l = C['l']; th = C['th']; alpha=C['alpha']; rho=C['rho']
    # ORBIT IDENTITY STRESS TEST over many corridor points, k=0..2q
    maxerr = mp.mpf(0)
    import random
    random.seed(q)
    npts = 200
    for _ in range(npts):
        a = mp.mpf(random.random())*0.9 + 0.05
        b = mp.mpf(random.random())*0.9 + 0.05
        p = (a,b)
        E = Eform(l,p)
        if E <= 0: continue
        C0 = alpha*E; R = rho*E
        # recover phi from k=0,1
        P0=Pgen(l,p); p1=Mmap(l,p); P1=Pgen(l,p1)
        cphi=(P0-C0)/R
        c2=mp.cos(2*th); s2=mp.sin(2*th)
        sphi=(cphi*c2-((P1-C0)/R))/s2
        phi=mp.atan2(sphi,cphi)
        pp=p
        for k in range(0,2*q+1):
            pred=C0+R*mp.cos(phi+2*k*th)
            maxerr=max(maxerr,abs(Pgen(l,pp)-pred))
            pp=Mmap(l,pp)
    results[str(q)] = dict(
        l=mp.nstr(l,40), alpha=mp.nstr(alpha,40), rho=mp.nstr(rho,40),
        cos=mp.nstr(C['c'],40), Efloor=mp.nstr(C['Efloor'],40),
        inv_l3=mp.nstr(1/l**3,40),
        orbit_max_err=mp.nstr(maxerr,8),
        mean_L1b=mp.nstr(C['mean_L1b'],40), amp_L1b=mp.nstr(C['amp_L1b'],40),
        alpha_minus_meanL1b=mp.nstr(alpha-C['mean_L1b'],12),
        rho_minus_ampL1b=mp.nstr(rho-C['amp_L1b'],12),
    )
    print(f"q={q:4d} l={mp.nstr(l,10)} alpha={mp.nstr(alpha,10)} rho={mp.nstr(rho,10)} "
          f"Efloor={mp.nstr(C['Efloor'],8)} 1/l^3={mp.nstr(1/l**3,8)} orbit_err={mp.nstr(maxerr,4)}")

# Asymptotics: alpha*(4-l^2)->3, rho*(4-l^2)->3 as q->inf
print("\nASYMPTOTICS alpha*(4-l^2), rho*(4-l^2) -> 3 :")
for q in [10,40,100,1000]:
    C=consts(q); l=C['l']
    print(f"  q={q}: alpha*(4-l^2)={mp.nstr(C['alpha']*(4-l**2),12)} rho*(4-l^2)={mp.nstr(C['rho']*(4-l**2),12)}")

# GATE check 1b at the E-floor: (1/l^3 - alpha*Efloor)/(rho*Efloor) <= cos(theta), with equality at floor
print("\nGATE at E=Efloor:  (1/l^3 - C0)/R  vs  cos(theta)  [equality by construction]:")
for q in [5,7,13,22]:
    C=consts(q); l=C['l']; th=C['th']; E=C['Efloor']
    lhs=(1/l**3 - C['alpha']*E)/(C['rho']*E)
    print(f"  q={q}: lhs={mp.nstr(lhs,30)} cos(th)={mp.nstr(C['c'],30)} diff={mp.nstr(lhs-C['c'],8)}")

out = dict(dps=mp.mp.dps,
           note="RAW-Pgen alpha=1/(4c)+3c/(4s^2), rho=sqrt(8c^2+1)/(4s^2 c), Efloor=1/(l^3(alpha+rho c)). Orbit identity Pgen(M^k p)=alpha E + rho E cos(phi+2k theta).",
           per_q=results)
os.makedirs("/kaggle/working", exist_ok=True)
with open("/kaggle/working/hsa_constants.json","w") as f:
    json.dump(out,f,indent=2)
print("\nWROTE /kaggle/working/hsa_constants.json")
