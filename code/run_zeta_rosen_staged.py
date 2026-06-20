"""Staged resume driver for zeta_mayer_rosen.

Runs the three stages (q=3 regression, q=5, q=8) SEPARATELY and writes the
JSON artifact after EACH stage, so a runtime kill cannot lose completed work.
Params reduced from the in-file __main__ for a faster first pass while keeping
the method intact (N-stability over >=3 basis sizes, Weyl check, n_head check).
"""
import sys, os, json, time
import numpy as np
sys.path.insert(0, "code")
import zeta_mayer_rosen as z

def _jsafe(o):
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    return str(o)

OUT = "code/out/zeta_mayer_rosen.json"
out = {"description": "STAGED RESUME: MMS Rosen Selberg-zeta spectrum, Hecke "
       "q=5,8 (non-arithmetic) + q=3 regression anchor.",
       "params": {"q3": {"N": 36, "n_head": 8000},
                  "q58": {"N_LIST": [25, 35, 45], "n_grid": 130,
                          "n_head": 5000, "r_range": [0.5, 12.0]}}}

def save():
    tmp = OUT + ".tmp"
    with open(tmp, "w") as f:
        json.dump(out, f, indent=2, default=_jsafe)
    os.replace(tmp, OUT)  # atomic: a kill mid-write can't corrupt OUT

t0 = time.time()
print("STAGE 1/3: q=3 regression ...", flush=True)
out["q3_regression"] = z.q3_regression(N=36, n_head=8000)
save()
print(f"  q3 saved ({time.time()-t0:.0f}s)", flush=True)

N_LIST = [25, 35, 45]
print("STAGE 2/3: q=5 (non-arithmetic) ...", flush=True)
out["q5"] = z.run_q(5, 0.5, 12.0, 130, N_LIST, n_head=5000)
save()
print(f"  q5 saved ({time.time()-t0:.0f}s)", flush=True)

print("STAGE 3/3: q=8 (non-arithmetic) ...", flush=True)
out["q8"] = z.run_q(8, 0.5, 12.0, 130, N_LIST, n_head=5000)
save()
print(f"  q8 saved ({time.time()-t0:.0f}s)", flush=True)

print(f"ALL DONE ({time.time()-t0:.0f}s) -> {OUT}", flush=True)
