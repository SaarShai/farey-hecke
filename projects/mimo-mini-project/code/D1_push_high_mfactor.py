"""
D1 high-m_factor push: discriminate (i) m-truncation undershoot
from (ii) genuine Q→∞ drift in NW(Q).

Sweep: Q ∈ {1e6, 2e6} × m_factor ∈ {20, 50, 100}.
Records NW(Q, m_factor) so we can extrapolate m_factor → ∞ at each Q,
then track the Q-trajectory of the extrapolated value.

Goal: nail down whether NW(∞) ≈ 0.66989 (Euler product) or some other
value, with at least 4 reliable digits.
"""
import sys, json, math, time
sys.path.insert(0, "/Users/za/Documents/Farey NOW/projects/mimo-mini-project/code")
from D1_NW_highQ import J_mikolas_optimized

OUT = "/Users/za/Documents/Farey NOW/projects/mimo-mini-project/phase3_synthesis/D1_high_mfactor_sweep.json"

configs = [
    (1_000_000, 50.0),
    (1_000_000, 100.0),
    (2_000_000, 20.0),
    (2_000_000, 50.0),
]

results = []
for Q, m_factor in configs:
    t0 = time.time()
    print(f"\n=== Q={Q:,} m_factor={m_factor} (m_max={int(m_factor*Q):,}) ===", flush=True)
    try:
        res = J_mikolas_optimized(Q, m_factor=m_factor)
        wall = time.time() - t0
        res["wall_s"] = wall
        results.append(res)
        print(f"  NW = {res['NW']:.10f}  wall = {wall:.1f}s", flush=True)
        # Extrapolation hint: NW vs m_factor at fixed Q
        for m, cum in res["cum_running"]:
            J_at = cum / (2 * math.pi ** 2)
            NW_at = Q * J_at / res["Phi_N"]
            print(f"    at m={m:>12,}: NW_partial={NW_at:.10f}", flush=True)
    except MemoryError:
        print(f"  OOM at (Q, m_factor) = ({Q}, {m_factor})", flush=True)
        break

with open(OUT, "w") as f:
    json.dump(results, f, indent=2, default=str)
print(f"\nwrote {OUT}", flush=True)

# Final summary
candidates = {
    "(1/2)·Π_p(1+1/(p²(p−1)))": 0.6698911504298892,  # Euler product
    "2/3":                       2.0/3.0,
    "12/π²·(prev)":              12/math.pi**2 * 0.55,  # placeholder family
    "twin-prime-const":          0.6601618158468696,
}
print("\nFinal NW values vs candidates:")
for r in results:
    print(f"  Q={r['Q']:>8,} mf={r['m_max']//r['Q']:>4}: NW={r['NW']:.10f}")
print("\nCandidate offsets (from largest-Q largest-mf result):")
if results:
    best = max(results, key=lambda r: (r["Q"], r["m_max"]))
    print(f"  best: Q={best['Q']:,}, m_max={best['m_max']:,}, NW={best['NW']:.10f}")
    for name, val in candidates.items():
        print(f"    diff to {name}: {best['NW'] - val:+.8f}")
