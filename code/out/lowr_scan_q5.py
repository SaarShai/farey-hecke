"""
Low-r COMPLETENESS check for q=5 ODD (mms-) sector.
Read-only: imports the unmodified operator from code/zeta_mayer_rosen.py.
Fine-scans |det(1 - L_{s,-})| for r in [0.2, 6.5] (below reported floor 6.47)
to confirm NO odd zero was skipped.
"""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import zeta_mayer_rosen as Z

Q = 5
SIGN = -1          # mms- = ODD protected sector
N = 30             # prompt says small N (30) fine
N_HEAD = 8000

r_lo, r_hi = 0.2, 6.5
n_grid = 320       # ~0.02 spacing, fine enough to catch any |det|~1e-7 dip

absf = lambda r: abs(Z.det_on_line(Q, r, SIGN, N, n_head=N_HEAD))

rs = np.linspace(r_lo, r_hi, n_grid)
vals = np.array([absf(r) for r in rs])

# local minima
minima = []
for i in range(1, len(rs)-1):
    if vals[i] < vals[i-1] and vals[i] <= vals[i+1]:
        rm, fm = Z._golden_min(absf, rs[i-1], rs[i+1])
        minima.append((float(rm), float(fm)))

print(f"q={Q} sign={SIGN} (mms-/ODD)  N={N}  n_head={N_HEAD}")
print(f"scan r in [{r_lo},{r_hi}] grid={n_grid} (spacing {(r_hi-r_lo)/(n_grid-1):.4f})")
print(f"global |det| floor over grid = {vals.min():.3e} at r={rs[int(vals.argmin())]:.4f}")
print(f"global |det| max  over grid  = {vals.max():.3e}")
print("\nALL local minima of |det| in [0.2,6.5]:")
for rm, fm in minima:
    flag = "  <== CANDIDATE ZERO (below 1e-2)" if fm < 1e-2 else ""
    print(f"   r*={rm:8.4f}   |det|={fm:.3e}{flag}")

cands = [(rm,fm) for rm,fm in minima if fm < 1e-2]
print(f"\nN candidate zeros (|det|<1e-2) below 6.47: {len(cands)}")

# Also do the SAME scan for the mms+ (even) sector as a control
print("\n--- control: mms+ (even/+1) sector, same window ---")
absfp = lambda r: abs(Z.det_on_line(Q, r, +1, N, n_head=N_HEAD))
valsp = np.array([absfp(r) for r in rs])
print(f"mms+ global |det| floor = {valsp.min():.3e} at r={rs[int(valsp.argmin())]:.4f}")

out = {
    'q': Q, 'sign': SIGN, 'N': N, 'n_head': N_HEAD,
    'r_lo': r_lo, 'r_hi': r_hi, 'n_grid': n_grid,
    'grid_floor': float(vals.min()),
    'grid_floor_r': float(rs[int(vals.argmin())]),
    'minima': minima,
    'candidate_zeros_below_647': cands,
    'mms_plus_floor': float(valsp.min()),
    'grid_r': rs.tolist(),
    'grid_absdet_minus': vals.tolist(),
    'grid_absdet_plus': valsp.tolist(),
}
op = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lowr_scan_q5.json")
json.dump(out, open(op, 'w'), indent=2)
print(f"\nSaved: {op}")
