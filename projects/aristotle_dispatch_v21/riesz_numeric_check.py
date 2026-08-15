from mpmath import mp, mpf, zeta, zetazero, diff
mp.dps = 30
NMAX = 20000
mu=[1]*(NMAX+1); mu[0]=0; primes=[]; is_c=[False]*(NMAX+1)
for i in range(2,NMAX+1):
    if not is_c[i]: primes.append(i); mu[i]=-1
    for p in primes:
        if i*p>NMAX: break
        is_c[i*p]=True
        if i%p==0: mu[i*p]=0; break
        mu[i*p]=-mu[i]
NZ=200
rhos=[zetazero(k) for k in range(1,NZ+1)]
w=[1/(r*(r+1))/diff(zeta,r) for r in rhos]
def Rtriv(N):
    return mp.fsum([mp.power(N,mpf(-2*n))/(mpf(-2*n)*(mpf(-2*n)+1)*diff(zeta,mpf(-2*n))) for n in range(1,8)])
print("gamma_100=",mp.nstr(rhos[99].imag,8)," gamma_200=",mp.nstr(rhos[199].imag,8))
for N in [2000,8000,20000]:
    lhs = mp.fsum([mu[n]*(1-mpf(n)/N) for n in range(1,N+1)])
    row=[N, mp.nstr(lhs,10)]
    for K in (25,50,100,200):
        zs = 2*mp.fsum([(mp.power(N,r)*wk).real for r,wk in zip(rhos[:K],w[:K])])
        rhs = -2 + mpf(12)/N + zs + Rtriv(N)
        row.append("K=%d diff=%s"%(K,mp.nstr(lhs-rhs,4)))
    print(*row)
