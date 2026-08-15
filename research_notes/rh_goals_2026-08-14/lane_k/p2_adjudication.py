#!/usr/bin/env python3
"""P2 adjudication: Mertens constant S to 4-5 digits + Gonek J_{-1}(T) verdict.

Inputs:
  harvest/mertens_zeros_FULL.csv  (indices 10000..100000, gamma_refined,
                                   abs_zeta_prime_sq, residual; 5-gate PASS)
  v2 receipt constants (lane_a/ZERO_SUM_V2_REPORT.md):
    two-sided partial sum through N=10000 = 0.029014789373050
    (positive one-sided 0.014507394686525)

S = sum_rho 1/(|rho|^2 |zeta'(rho)|^2), two-sided (double positive-ordinate terms),
|rho|^2 = 1/4 + gamma^2.

J_{-1}(T) = sum_{0<gamma<=T} 1/|zeta'(rho)|^2, Gonek: ~ (3/pi^3) T.

Method notes:
- The FULL table row index 10000 duplicates the v2 range endpoint (v2 summed
  N=1..10000). Extension terms are indices 10001..100000.
- Tail model as in v2: through-origin fit of block means B(t) = mean(1/|zeta'|^2)
  against B_G(t) = (6/pi^2)/log(t/2pi) on 500-zero blocks; central one-sided
  tail = alpha*(3/pi^3)*2*atan(1/(2T)); envelope holds max block mean.
- All arithmetic mpmath dps=40. NON-RIGOROUS tail (numerical extrapolation),
  same caveat as v2.
"""
import csv
from mpmath import mp, mpf, atan, pi, log

mp.dps = 40

V2_TWO_SIDED_10K = mpf('0.029014789373050')
ROWS = []
with open('harvest/mertens_zeros_FULL.csv') as f:
    for r in csv.DictReader(f):
        ROWS.append((int(r['index']), mpf(r['gamma_refined']), mpf(r['abs_zeta_prime_sq'])))
ROWS.sort()
assert ROWS[0][0] == 10000 and ROWS[-1][0] == 100000 and len(ROWS) == 90001

# --- Mertens extension ---
ext_pos = mpf(0)
for i, g, zp2 in ROWS:
    if i >= 10001:
        ext_pos += 1 / ((mpf('0.25') + g*g) * zp2)
S_central_partial = V2_TWO_SIDED_10K + 2*ext_pos
T = ROWS[-1][1]

# --- block means for tail fit (500-zero blocks over the new range) ---
blocks = []
for start in range(0, len(ROWS)-1, 500):
    chunk = ROWS[start:start+500]
    if len(chunk) < 500:
        break
    bm = sum(1/zp2 for _, _, zp2 in chunk) / len(chunk)
    t_lo = chunk[0][1]
    blocks.append((t_lo, bm))
# through-origin fit alpha on blocks with t_lo > 20000 (deep range)
num = den = mpf(0)
sel = [(t, bm) for t, bm in blocks if t > 20000]
ratios = []
for t, bm in sel:
    bg = (6/pi**2) / log(t/(2*pi))
    num += bm*bg; den += bg*bg
    ratios.append(bm/bg)
alpha = num/den
max_bm = max(bm for t, bm in sel)
central_tail_1s = alpha * (3/pi**3) * 2*atan(1/(2*T))
# envelope: hold max block mean with density integral (as v2): integrand
# max_bm * log(t/2pi)/(2pi(t^2+1/4)) integrated t=T..inf ~ max_bm*(log(T/2pi)+1)/(2piT)
env_tail_1s = max_bm * (log(T/(2*pi)) + 1) / (2*pi*T)
S_central = S_central_partial + 2*central_tail_1s
bar = 2*env_tail_1s  # symmetric-ish conservative bar (interval partial..partial+2*env)

print("=== MERTENS CONSTANT S ===")
print("partial two-sided through N=100000:", S_central_partial)
print("T =", T)
print("alpha (refit, blocks t>20000, n=%d):" % len(sel), alpha)
print("ratio range:", min(ratios), max(ratios))
print("central one-sided tail:", central_tail_1s)
print("envelope one-sided tail:", env_tail_1s)
print("S central (partial + central tail):", S_central)
print("conservative interval: [%s, %s]" % (S_central_partial, S_central_partial + 2*env_tail_1s))
print("bar (two-sided envelope):", bar)

# --- Gonek J_{-1}(T) ---
print("\n=== GONEK J_{-1}(T)/((3/pi^3)T) ===")
# cumulative from v2 range: need J at 10000th zero. v2 didn't bank it; compute
# ratio only on increments? J_{-1} needs 1..N sum. Approximate lower part via
# alpha-model? NO - report both: increment-only fits and note the offset.
# But: J_{-1}(T) - J_{-1}(T0) is exactly known for T0 = gamma_10000.
# Gonek asymptotic difference: (3/pi^3)(T - T0). Fit on differences kills the
# unknown constant J_{-1}(T0) additively -> use regression with intercept.
import bisect
J = mpf(0)
pts = []
for k, (i, g, zp2) in enumerate(ROWS):
    if i >= 10001:
        J += 1/zp2
        if k % 2000 == 0:
            pts.append((g, J))
pts.append((ROWS[-1][1], J))
C = 3/pi**3
# model: J(T)-J(T0) = c1*(T-T0) + c2*(T*logT - T0*logT0) [secondary term]
T0 = ROWS[0][1]
# least squares on (x1, x2) -> y
X1 = []; X2 = []; Y = []
for g, j in pts:
    X1.append(g - T0)
    X2.append(g*log(g) - T0*log(T0))
    Y.append(j)
n = len(Y)
s11 = sum(x*x for x in X1); s12 = sum(a*b for a, b in zip(X1, X2))
s22 = sum(x*x for x in X2); sy1 = sum(a*b for a, b in zip(X1, Y)); sy2 = sum(a*b for a, b in zip(X2, Y))
det = s11*s22 - s12*s12
c1 = (sy1*s22 - sy2*s12)/det
c2 = (s11*sy2 - s12*sy1)/det
print("two-term fit  J-J0 = c1*(T-T0) + c2*(T logT - T0 logT0):")
print("  c1 =", c1, " (Gonek predicts c1 -> 3/pi^3 =", C, ")")
print("  c2 =", c2)
print("  c1/(3/pi^3) =", c1/C)
# one-term fit
c1_only = sy1/s11
print("one-term fit  c1 =", c1_only, "  ratio:", c1_only/C)
# endpoint increment ratio
inc_ratio = J / (C*(T - T0))
print("raw increment ratio J/( (3/pi^3)(T-T0) ):", inc_ratio)
# split-halves for trend
mid = ROWS[len(ROWS)//2][1]
J_first = mpf(0); J_second = mpf(0)
for i, g, zp2 in ROWS:
    if i >= 10001:
        if g <= mid: J_first += 1/zp2
        else: J_second += 1/zp2
print("first-half increment ratio:", J_first/(C*(mid-T0)))
print("second-half increment ratio:", J_second/(C*(T-mid)))
