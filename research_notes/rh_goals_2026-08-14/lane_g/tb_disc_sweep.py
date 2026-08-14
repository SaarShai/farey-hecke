"""T-b disc-geometry sweep: per-ALLOWED-block contraction ratios vs safety factor.
Blocks per zeta_mayer_rosen.build_reduced_matrix odd-q structure (q=5)."""
import math, sys, json
sys.path.insert(0, "/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code")
from zeta_mayer_rosen import hecke_params, partition_points
import numpy as np

q = 5
lam, hq, kappa = hecke_params(q)
pts = partition_points(q)
half = [(pts[i]-pts[i-1])/2 for i in range(1,len(pts))]
cs   = [(pts[i]+pts[i-1])/2 for i in range(1,len(pts))]
th = np.exp(2j*np.pi*np.arange(4096)/4096)

def theta(z, n, neg):
    return 1.0/(z - n*lam) if neg else -1.0/(z + n*lam)

# allowed blocks (out_i, in_j, n, neg, is_tail) 1-indexed, from eq.34 code
BLOCKS = [(1,2,2,False,False),(1,3,3,False,True),(1,2,1,True,False),(1,3,2,True,True),
          (2,3,2,False,True),(2,2,1,True,False),(2,3,2,True,True),
          (3,1,1,False,False),(3,3,2,False,True),(3,2,1,True,False),(3,3,2,True,True)]
NTAIL = 80
print("safety | rho_star | worst block | N for tail 1e-7 (per-mode rho^N)")
results=[]
for safety in (1.0,1.1,1.25,1.5,1.75,2.0,2.5):
    rho=0.0; worst=None
    for (i,j,n,neg,tail) in BLOCKS:
        z = cs[i-1] + safety*half[i-1]*th
        ns = range(n, NTAIL) if tail else [n]
        for nn in ns:
            img = theta(z, nn, neg)
            r = np.max(np.abs(img - cs[j-1]))/(safety*half[j-1])
            if r > rho: rho, worst = r, (i,j,(-nn if neg else nn))
    N7 = math.log(1e-7)/math.log(rho) if rho<1 else float('inf')
    print(f"{safety:5.2f}  | {rho:.4f}  | {worst} | {N7:.0f}" if rho<1 else f"{safety:5.2f}  | {rho:.4f}  | {worst} | VIOLATION (no nesting)")
    results.append({"safety":safety,"rho_star":float(rho),"worst_block":list(worst),"N_1e-7":(None if rho>=1 else N7)})
json.dump(results, open("/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/tb_disc_sweep.json","w"), indent=1)
