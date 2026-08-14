"""T-b: optimize independent per-disc inflation factors (a1,a2,a3) minimizing
the max allowed-block contraction ratio for q=5."""
import math, sys, json, itertools
sys.path.insert(0, "/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code")
from zeta_mayer_rosen import hecke_params, partition_points
import numpy as np

q = 5
lam, hq, kappa = hecke_params(q)
pts = partition_points(q)
half = [(pts[i]-pts[i-1])/2 for i in range(1,len(pts))]
cs   = [(pts[i]+pts[i-1])/2 for i in range(1,len(pts))]
th = np.exp(2j*np.pi*np.arange(2048)/2048)
BLOCKS = [(1,2,2,False,False),(1,3,3,False,True),(1,2,1,True,False),(1,3,2,True,True),
          (2,3,2,False,True),(2,2,1,True,False),(2,3,2,True,True),
          (3,1,1,False,False),(3,3,2,False,True),(3,2,1,True,False),(3,3,2,True,True)]
def theta(z,n,neg): return 1.0/(z-n*lam) if neg else -1.0/(z+n*lam)
def rho_star(a):
    rho=0.0; worst=None
    for (i,j,n,neg,tail) in BLOCKS:
        z = cs[i-1] + a[i-1]*half[i-1]*th
        for nn in (range(n,60) if tail else [n]):
            r = np.max(np.abs(theta(z,nn,neg)-cs[j-1]))/(a[j-1]*half[j-1])
            if r>rho: rho, worst = r,(i,j,(-nn if neg else nn))
    return rho, worst
best=(9,None,None)
grid=[1.0,1.1,1.2,1.35,1.5,1.7,1.9,2.2,2.6,3.0]
for a in itertools.product(grid,repeat=3):
    r,w = rho_star(a)
    if r<best[0]: best=(r,a,w)
r,a,w = best
print(f"BEST rho* = {r:.4f} at (a1,a2,a3)={a}, worst block {w}")
# local refine
for _ in range(3):
    g=[max(0.9,x) for x in a]
    cand=[tuple(np.clip([a[0]+da,a[1]+db,a[2]+dc],0.95,4.0)) for da in (-0.07,0,0.07) for db in (-0.07,0,0.07) for dc in (-0.07,0,0.07)]
    for c in cand:
        rr,ww=rho_star(c)
        if rr<r: r,a,w=rr,c,ww
print(f"REFINED rho* = {r:.4f} at (a1,a2,a3)=({a[0]:.3f},{a[1]:.3f},{a[2]:.3f}), worst {w}")
N7 = math.log(1e-7)/math.log(r); N15 = math.log(1e-15)/math.log(r)
print(f"per-mode decay: N for 1e-7 = {N7:.0f}, for 1e-15 = {N15:.0f}")
json.dump({"rho_star":r,"a":list(a),"worst":list(w),"N_1e-7":N7,"N_1e-15":N15},
          open("/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/tb_disc_opt.json","w"), indent=1)
