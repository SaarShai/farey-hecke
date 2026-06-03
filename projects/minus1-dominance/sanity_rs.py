"""
Anchor the canonical RS density delta(q;a,1) for q=3,4 (single nonsquare a=q-1)
via the EXACT Rubinstein-Sarnak / Feuerverger-Martin one-dimensional formula:

  X_{q;a,1} has mean  -rho(q)   (here rho(q)=#sqrt of 1) ... actually for the
  2-class race the relevant 1-D variable is
     X = (bias) + sum over zeros, with
  delta(q;a,1) = Prob(X>0),  X normal-ish with
     mean mu = rho(q)   (the +1-per-square-root Chebyshev bias, here q=3,4 => the
              nonsquare leads),
     variance V = V(q;a,1) = sum_chi |chi(a)-chi(1)|^2 b(chi).
  Then in the GAUSSIAN approximation delta ~ Phi(mu/sqrt(V)).
The TRUE distribution is not Gaussian, but for q=3,4 the Gaussian gives the right
ballpark; the literature value (RS/FM) is delta(4;3,1)=0.99590, delta(3;2,1)=0.99906.
We compute V by direct low-zero summation of the single relevant odd character.
"""
import mpmath as mp
mp.mp.dps=25

# q=4, chi = odd char mod 4 (chi4). q=3, chi = odd char mod 3 (chi3).
# For these, V(q; q-1, 1) = |chi(q-1)-1|^2 * b(chi) = |-1-1|^2 b = 4 b(chi).
# rho(q)=2 (x^2=1 has 2 solns). mean mu of the limiting dist = rho(q)? RS show the
# mean of E(x;q,a)-E(x;q,1) is c(q,1)-c(q,a) = (number of sqrt of 1) - (sqrt of a).
# a=q-1 nonsquare => sqrt count 0; sqrt of 1 =2. So mean difference = 2.
# delta = Prob(X>0); with X ~ mean 2 (a leads), Gaussian std sqrt(V).

# low zeros (Odlyzko / LMFDB) of L(s,chi4) and L(s,chi3):
gam_chi4=[6.020948,10.243770,12.988098,16.342537,18.291914,21.402942,23.580285,
          25.708623,27.670273,30.413545,31.733511,34.137145,36.481,37.674,40.014]
# L(s,chi3): lowest zero ~ 8.0397
gam_chi3=[8.039737,11.249803,15.704619,18.261284,20.451141,23.090806,25.479,27.581,
          30.295,31.717,34.117,36.099]

def b_from(gammas):
    s=sum(2/(mp.mpf('0.25')+mp.mpf(g)**2) for g in gammas)  # both signs
    T=gammas[-1]
    # tail: zero density rho(t)~(1/2pi)log(qt/2pi); approximate with conductor q.
    return s  # partial; tail small (~1/T per side), report partial as lower bound

for q,gam,cond in [(4,gam_chi4,4),(3,gam_chi3,3)]:
    b=b_from(gam)
    # add a crude tail integral both signs using density (1/pi)log(cond*t/2pi)/2 ...
    T=gam[-1]
    tail=mp.quad(lambda t:(1/mp.pi)*mp.log(cond*t/(2*mp.pi))/(t*t),[T,mp.inf])
    bfull=b+tail
    V=4*bfull
    mu=mp.mpf(2)   # mean difference (Chebyshev bias = #sqrt(1)-#sqrt(a)=2)
    # one-dim Gaussian approx
    delta_gauss=mp.ncdf(mu/mp.sqrt(V))
    print(f"q={q}: b(chi)~{mp.nstr(bfull,6)}  V=4b~{mp.nstr(V,6)}  "
          f"mu/sqrtV={mp.nstr(mu/mp.sqrt(V),5)}  Gaussian delta~{mp.nstr(delta_gauss,6)}")
print()
print("Literature (RS1994/FM): delta(4;3,1)=0.99590, delta(3;2,1)=0.99906.")
print("Gaussian is only an approximation (true dist non-Gaussian, heavier in the")
print("leading direction), so Gaussian delta is an UNDER-estimate but same ballpark,")
print("confirming the V scale and the role of the variance.")
