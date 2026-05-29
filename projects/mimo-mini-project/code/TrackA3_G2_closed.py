"""
Track A, experiment 3 -- VALIDATE the proof that closes G2.

Instead of "no periodic orbit on H" (G2), we prove the STRONGER orbit statement:
    (G=empty)  NO BCZ orbit in the open triangle has ALL products <= 2/9.
This directly kills the ground state (a ground-state measure would need mu(G)=1).

Proof mechanism to validate (T(x,y)=(y, floor((1+x)/y)y - x), P=xy, ground 2/9):
  In any forward-good orbit (all P_n <= 2/9), the window bound forces some
  P_m = 2/9 exactly at a step m>=1.  A point (a_m,a_{m+1}) with product 2/9 and
  a_m+a_{m+1}>1 has a_{m+1}<1/3 or a_{m+1}>2/3 (no middle).  KEY IDENTITY: when
  the floor is 1 (left coord <1/3, right coord >2/3), P_next = (right coord)^2 - P.
   * case (i)  a_{m+1}>2/3 : floor=1 => P_{m+1} = a_{m+1}^2 - 2/9 > 4/9-2/9 = 2/9.
                CONTRADICTION (forward-good demands P_{m+1}<=2/9).
   * case (ii) a_{m+1}<1/3 (=> a_m>2/3): the k=1 predecessor (a_m-a_{m+1}, a_m)
                has product a_m^2 - 2/9 > 2/9, so the predecessor is NOT
                forward-good => CONTRADICTION (a 2/9 point at m>=1 must have a
                forward-good predecessor).
This script checks all the numeric claims the proof relies on.
"""
import math
import numpy as np

g = 2.0 / 9.0
def T(x, y):
    k = math.floor((1.0 + x) / y)
    return (y, k * y - x), k
def in_T(x, y, tol=1e-12):
    return (tol < x < 1 - tol) and (tol < y < 1 - tol) and (x + y > 1 + tol)

# dense sample of H = {xy = 2/9} inside the OPEN triangle
xs = np.concatenate([np.linspace(0.2223, 0.3333, 4000),   # left branch  -> y in (2/3,1)
                     np.linspace(0.6667, 0.9999, 4000)])   # right branch -> y in (0,1/3)
H = [(x, g / x) for x in xs if in_T(x, g / x)]

print(f"sampled {len(H)} points of H in the open triangle")

# claim 0: no point of H has a_{m+1}=y in [1/3, 2/3]
mids = [(x, y) for (x, y) in H if 1/3 - 1e-9 <= y <= 2/3 + 1e-9]
print(f"[claim 0] H points with y in [1/3,2/3] (should be 0): {len(mids)}")

# claim case (i): y>2/3  =>  P(T p) = y^2 - 2/9  and  > 2/9
ci = [(x, y) for (x, y) in H if y > 2/3 + 1e-9]
bad_i = 0
maxerr_i = 0.0
min_Pnext_i = 1.0
for (x, y) in ci:
    (u, v), k = T(x, y)
    Pnext = u * v
    maxerr_i = max(maxerr_i, abs(Pnext - (y * y - g)))   # identity check
    min_Pnext_i = min(min_Pnext_i, Pnext)
    if not (k == 1 and Pnext > g - 1e-12):
        bad_i += 1
print(f"[case i ] y>2/3: n={len(ci)}  floor==1 & P_next>2/9 fails: {bad_i}"
      f"   |P_next-(y^2-2/9)| max={maxerr_i:.2e}   min P_next={min_Pnext_i:.6f} (>2/9={g:.6f})")

# claim case (ii): y<1/3 (=> x>2/3). The k=1 predecessor (x-y, x) is in T, has
# floor 1, and product x^2-2/9 > 2/9 => predecessor not forward-good.
cii = [(x, y) for (x, y) in H if y < 1/3 - 1e-9]
bad_ii = 0
min_Pprev_ii = 1.0
for (x, y) in cii:
    a_prev = x - y                      # k=1 predecessor first coord
    # predecessor point is (a_prev, x); check it maps to (x,y) with floor 1
    (u, v), k = T(a_prev, x)
    ok_pred = in_T(a_prev, x) and k == 1 and abs(u - x) < 1e-9 and abs(v - y) < 1e-9
    Pprev = a_prev * x                  # = x^2 - 2/9
    min_Pprev_ii = min(min_Pprev_ii, Pprev)
    if not (ok_pred and Pprev > g - 1e-12):
        bad_ii += 1
print(f"[case ii] y<1/3: n={len(cii)}  k=1 predecessor valid & product>2/9 fails: {bad_ii}"
      f"   min P_prev={min_Pprev_ii:.6f} (>2/9)")

# global cross-check: longest run of consecutive products <= 2/9 over many orbits
rng = np.random.default_rng(1)
best = 0
for _ in range(150000):
    x = rng.uniform(0.001, 0.999)
    ylo = max(0.001, 1 - x + 1e-6)
    if ylo >= 0.999:
        continue
    y = rng.uniform(ylo, 0.999)
    run = 0
    for _ in range(120):
        if not in_T(x, y):
            break
        if x * y <= g + 1e-12:
            run += 1
            best = max(best, run)
        else:
            run = 0
        (x, y), _ = T(x, y)
print(f"[global ] longest run of products <= 2/9 over 150k orbits: {best} "
      f"(proof rules out any infinite run => G is empty)")

print("\nALL CHECKS:", "PASS" if (len(mids) == 0 and bad_i == 0 and bad_ii == 0)
      else "FAIL -- proof mechanism does not hold, REVISIT")
