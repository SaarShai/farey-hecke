"""
D1 push: N·W(N) at Q ∈ {10^6} with large m_factor.
Goal: 5+ digit precision to lock in C = 2/3.
"""

import sys
sys.path.insert(0, "/Users/za/Documents/Farey NOW/projects/mimo-mini-project/code")
from D1_NW_highQ import J_mikolas_optimized
import json, time, math

OUT = "/Users/za/Documents/Farey NOW/projects/mimo-mini-project/phase3_synthesis/D1_1M_result.json"

results = []
for Q, m_factor in [(1_000_000, 20.0)]:
    t0 = time.time()
    res = J_mikolas_optimized(Q, m_factor=m_factor)
    res["wallclock_s"] = time.time() - t0
    results.append(res)
    print(f"Q={Q:>8} m_factor={m_factor} m_max={res['m_max']} J={res['J']:.6f} NW={res['NW']:.10f} wall={res['wallclock_s']:.1f}s", flush=True)
    if "cum_running" in res:
        for m, cum in res["cum_running"]:
            J_at = cum / (2 * math.pi ** 2)
            NW_at = Q * J_at / res["Phi_N"]
            print(f"  at m={m:>8}: NW={NW_at:.10f}", flush=True)

with open(OUT, "w") as f:
    json.dump(results, f, indent=2, default=str)
print(f"wrote {OUT}")

# Compare to candidates
NW = results[-1]["NW"]
candidates = {
    "2/3": 2/3,
    "Laplace limit": 0.6627434193491815,
    "twin-prime / 2": 0.6601618158468696,
    "π²/15": math.pi ** 2 / 15,
}
print(f"\nFinal NW(Q=10^6) = {NW:.10f}")
for name, val in candidates.items():
    print(f"  diff to {name:>20s} ({val:.10f}) = {NW - val:+.8f}")
