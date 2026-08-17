#!/usr/bin/env python3
"""crb_smallr.py -- cold review: extend the corrected-inequality test to r in (0,0.5]
and to a fine grid, where the raw inf was attained at the grid edge r=0.5."""
import math, json
from mpmath import mp, mpf, mpc, sqrt, pi, gamma, zeta, log
mp.dps = 40
def g(s): return sqrt(pi)*gamma(s-mpf(1)/2)*zeta(2*s-1)/(gamma(s)*zeta(2*s))
def phi(q,s):
    if q==3: return g(s)
    p={4:2,6:3}[q]; return g(s)*(1+mpf(p)**(1-s))/(1+mpf(p)**s)
def mdlp(q,s): return -mp.diff(lambda z: log(phi(q,z)), s, h=mpf('1e-10'))
out=[]
for q in (3,4,6):
    tl=float(2*log(2*mp.cos(pi/q)))
    best=None
    for i in range(1,501):
        r=mpf(i)/500          # r in (0, 1]
        v=float(mdlp(q,mpc(mpf('0.5'),r)).real)
        c=v+float(1/(mpf('0.25')+r**2))
        if best is None or c<best[2]: best=(float(r),v,c)
    out.append(dict(q=q,two_log_lambda=tl,r_min=best[0],raw=best[1],corrected=best[2],
                    holds=bool(best[2]>=tl-1e-9),margin=best[2]-tl))
    print(out[-1],flush=True)
json.dump(out,open('/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/law_probes/crb_smallr.json','w'),indent=1)
