#!/usr/bin/env python3
"""crb_qm_identify.py -- COLD REVIEW probe (read-only on all existing files).

Independent checks, using ONLY the closed-form arithmetic scattering
determinants (Gamma, zeta), no determinant pipeline:

T1  reproduce agp_b4star's inf_r of -(phi'/phi)(1/2+ir) at q = 3,4,6 on an
    independent grid.
T2  DETERMINE q_M from the closed form: -(phi'/phi)(sigma) -> 2 log q_M as
    sigma -> +infinity (Hejhal's constant = 2 log(smallest modulus)).
    Compare against 2 log q (the lane's identification) and
    2 log(2 cos(pi/q)) = 2 log lambda_q (this reviewer's candidate).
T3  test the CORRECTED pointwise inequality
      -(phi'/phi)(1/2+ir) + 2(s_1-1/2)/((s_1-1/2)^2+r^2) >= 2 log lambda_q
    with the single exceptional s_1 = 1 (constant eigenfunction, pole of phi).
T4  log-q coefficient of the order-q elliptic Gamma-factor term alone
    (the sum  SUM_k ((q-2k-1)/q)(pi/q) cot(pi(s+k)/q) ).
"""
import math, json
from mpmath import mp, mpf, mpc, sqrt, pi, gamma, zeta, log, tan, sin

mp.dps = 40

def g(s):
    return sqrt(pi)*gamma(s-mpf(1)/2)*zeta(2*s-1)/(gamma(s)*zeta(2*s))

def phi(q, s):
    if q == 3: return g(s)
    p = {4:2, 6:3}[q]
    return g(s)*(1+mpf(p)**(1-s))/(1+mpf(p)**s)

def mdlp(q, s):            # -(phi'/phi)(s)
    return -mp.diff(lambda z: log(phi(q, z)), s, h=mpf('1e-10'))

def ell_term(q, s):        # order-q elliptic Gamma-factor log-derivative
    return sum((mpf(q-2*k-1)/q)*(pi/q)/tan(pi*(s+k)/q) for k in range(q))

out = {}

# ---- T1 / T3
lam = lambda q: 2*mp.cos(pi/q)
rows = []
for q in (3,4,6):
    grid = [mpf('0.5')+mpf(i)*mpf('0.01') for i in range(0, 4000)]   # r in [0.5,40.5)
    vals = [(float(r), float(mdlp(q, mpc(mpf('0.5'), r)).real)) for r in grid]
    mn = min(vals, key=lambda t: t[1])
    corr = [(r, v + float(1/(mpf('0.25')+mpf(r)**2))) for r, v in vals]
    mnc = min(corr, key=lambda t: t[1])
    rows.append(dict(q=q, two_log_q=2*math.log(q),
                     two_log_lambda=float(2*log(lam(q))),
                     inf_raw=mn[1], argmin_raw=mn[0],
                     inf_corrected=mnc[1], argmin_corrected=mnc[0],
                     mean_2_12=sum(v for r,v in vals if 2<=r<=12)/sum(1 for r,v in vals if 2<=r<=12),
                     corrected_holds=bool(mnc[1] >= float(2*log(lam(q))) - 1e-9),
                     raw_holds_vs_2logq=bool(mn[1] >= 2*math.log(q))))
    print(rows[-1], flush=True)
out['T1_T3'] = rows

# ---- T2  sigma -> infinity limit
lim = []
for q in (3,4,6):
    r = {}
    for sg in (5, 10, 20, 40, 80):
        r[sg] = float(mdlp(q, mpf(sg)).real)
    lim.append(dict(q=q, limits=r, two_log_q=2*math.log(q),
                    two_log_lambda=float(2*log(lam(q)))))
    print(lim[-1], flush=True)
out['T2'] = lim

# ---- T4  elliptic term growth
ell = []
prev = None
for q in (100, 200, 400, 1000, 2000, 4000):
    v = float(ell_term(q, mpc(mpf('0.5'), mpf('7.067362570867346'))).real)
    if prev: slope = (v-prev[1])/(math.log(q)-math.log(prev[0]))
    else: slope = None
    ell.append(dict(q=q, value=v, local_slope_in_log_q=slope))
    print(ell[-1], flush=True)
    prev = (q, v)
out['T4'] = ell

p = '/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/law_probes/crb_qm_identify.json'
json.dump(out, open(p,'w'), indent=1)
print('wrote', p)
