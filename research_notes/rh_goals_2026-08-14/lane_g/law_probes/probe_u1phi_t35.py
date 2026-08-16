#!/usr/bin/env python3
"""Third-height run for the U1-phi test (LAW_U1PHI_TEST.md §5.2 rec 1).

Reuses probe_u1phi.py's proxy verbatim; only the height changes: t = 3.5
on the same q grid, making the two-height fit overdetermined.
"""
import importlib.util, json, time, cmath, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("u1phi", os.path.join(HERE, "probe_u1phi.py"))
u1phi = importlib.util.module_from_spec(spec)
sys.modules["u1phi"] = u1phi
spec.loader.exec_module(u1phi)  # main() is guarded under __main__

u1phi.ctx.prec = 400
T3 = 3.5
QS = [12, 14, 16, 18, 20, 22, 26, 30, 34, 40]
N = 32

doc = {"N": N, "t": T3, "rows": []}
for q in QS:
    t0 = time.time()
    p = u1phi.proxy(q, complex(0.5, T3), N)
    row = {"q": q, "s": [0.5, T3], "abs": abs(p), "arg": cmath.phase(p),
           "wall": time.time() - t0}
    doc["rows"].append(row)
    print(f"q={q:3d}  |P|={abs(p):.7e}  arg P={cmath.phase(p):+.6f}  ({row['wall']:.0f}s)",
          flush=True)

with open(os.path.join(HERE, "u1phi_t35.json"), "w") as f:
    json.dump(doc, f, indent=1)
print("wrote u1phi_t35.json")
