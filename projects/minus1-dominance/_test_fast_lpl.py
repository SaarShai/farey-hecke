#!/usr/bin/env python3
"""
Validate the FAST L'/L(1,chi) method against compute_delta.py's slow mp.diff route.

Fast identity (prime q, non-principal chi, hence primitive):
  L(s,chi) = q^{-s} sum_{r=1}^{q-1} chi(r) zeta(s, r/q)
  zeta(s,a) = 1/(s-1) + gamma_0(a) - gamma_1(a)(s-1) + ...,  gamma_0(a) = -psi(a)
  Since sum_r chi(r) = 0 the pole cancels:
    A0 = sum_r chi(r) gamma_0(r/q),  A1 = sum_r chi(r) gamma_1(r/q)
    L'/L(1,chi) = -log q - A1/A0.
  Then c_chi = log(q/pi) + psi((1+a_chi)/2) + 2 Re L'/L(1,chi),  a_chi = (1-chi(-1))/2.
  V(q;a,1) = sum_{chi != chi0} c_chi |chi(a)-1|^2.
"""
import math, cmath
import mpmath as mp
mp.mp.dps = 30

# --- slow reference (lifted from compute_delta.py) ---
def units(q): return [a for a in range(1, q) if math.gcd(a, q) == 1]
def primitive_root(q):
    U = units(q); n = len(U)
    def order(g):
        o=1; x=g%q
        while x!=1: x=(x*g)%q; o+=1
        return o
    for g in U:
        if order(g)==n: return g
def characters(q):
    U=units(q); n=len(U); g=primitive_root(q)
    dlog={}; x=1
    for j in range(n): dlog[x]=j; x=(x*g)%q
    chars=[]
    for k in range(n):
        chi={a: mp.e**(2j*mp.pi*k*dlog[a]/n) for a in U}
        chars.append(chi)
    return chars, U, n
def is_principal(chi,U): return all(abs(chi[a]-1)<1e-9 for a in U)
def Lfun(s,q,chi):
    return mp.power(q,-s)*mp.fsum(chi[r]*mp.zeta(s,mp.mpf(r)/q) for r in chi if abs(chi[r])>1e-12)
def LpL_slow(q,chi):
    return mp.diff(lambda s: mp.log(Lfun(s,q,chi)), mp.mpf(1), h=mp.mpf('1e-8'))

# --- fast method ---
def LpL_fast(q,chi,g0,g1):
    # g0[r]=gamma_0(r/q)=-psi(r/q); g1[r]=gamma_1(r/q)
    A0=mp.fsum(chi[r]*g0[r] for r in chi if abs(chi[r])>1e-12)
    A1=mp.fsum(chi[r]*g1[r] for r in chi if abs(chi[r])>1e-12)
    return -mp.log(q) - A1/A0

print("Testing mp.stieltjes(1, a) availability ...")
try:
    v = mp.stieltjes(1, mp.mpf(1)/3)
    print(f"  mp.stieltjes(1,1/3) = {mp.nstr(v,12)}  OK")
except Exception as e:
    print(f"  FAILED: {e}")
    raise SystemExit(1)

for q in [7, 11, 19, 23]:
    chars,U,n = characters(q)
    g0 = {r: -mp.psi(0, mp.mpf(r)/q) for r in range(1,q)}
    g1 = {r: mp.stieltjes(1, mp.mpf(r)/q) for r in range(1,q)}
    maxerr = mp.mpf(0)
    for chi in chars:
        if is_principal(chi,U): continue
        s = LpL_slow(q,chi); f = LpL_fast(q,chi,g0,g1)
        e = abs(s-f); maxerr = max(maxerr, e)
    print(f"q={q}: max |LpL_slow - LpL_fast| over {n-1} nonprincipal chars = {mp.nstr(maxerr,6)}")

# Now full variance V(q;a,1) both ways, confirm -1 is argmax over nonresidues.
def residues(q):
    U=units(q); sq=set((a*a)%q for a in U)
    return sorted(sq), sorted(set(U)-sq)
def c_chi(q,chi,lpl):
    achi = 0 if chi[q-1].real>0 else 1
    return mp.log(mp.mpf(q)/mp.pi) + mp.psi(0,(1+achi)/mp.mpf(2)) + 2*lpl.real
print("\nV(q;a,1) via FAST method; rank a=-1 among nonresidues (1=max V):")
for q in [7,11,19,23]:
    chars,U,n = characters(q)
    g0={r:-mp.psi(0,mp.mpf(r)/q) for r in range(1,q)}
    g1={r:mp.stieltjes(1,mp.mpf(r)/q) for r in range(1,q)}
    nonprinc=[chi for chi in chars if not is_principal(chi,U)]
    cc=[c_chi(q,chi,LpL_fast(q,chi,g0,g1)) for chi in nonprinc]
    QR,NR=residues(q)
    Vs={}
    for a in NR:
        Vs[a]=float(mp.fsum(cc[i]*abs(nonprinc[i][a]-1)**2 for i in range(len(nonprinc))))
    order=sorted(NR,key=lambda a:-Vs[a])
    rank=order.index(q-1)+1
    print(f"  q={q}: V(-1)={Vs[q-1]:.4f}  argmax={order[0]}  rank(-1)={rank}/{len(NR)}  "
          f"{'OK max' if rank==1 else 'NOT MAX'}")
