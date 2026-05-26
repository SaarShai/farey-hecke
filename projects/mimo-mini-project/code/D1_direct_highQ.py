"""
D1: push direct J(Q) computation to Q=50000 and Q=100000 for asymptotic C.
"""
import sys, time, json, math
sys.path.insert(0, "/Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-15-D1-bcz-cocycle")
from verify_bcz_cocycle import J_direct_fast, ensure_sieve, farey

OUT = "/Users/za/Documents/Farey NOW/projects/mimo-mini-project/phase3_synthesis/D1_direct_highQ.json"

results = []
for Q in [30_000, 50_000, 100_000]:
    t0 = time.time()
    ensure_sieve(Q)
    F_len = sum(1 for _ in farey(Q))
    J = J_direct_fast(Q)
    NW = Q * J / F_len
    wall = time.time() - t0
    results.append({"Q": Q, "F_len": F_len, "J": J, "NW": NW, "wall_s": wall})
    print(f"Q={Q:>7} |F|={F_len:>12} J={J:>14.6f} NW={NW:>11.8f} wall={wall:.1f}s", flush=True)

with open(OUT, "w") as f:
    json.dump(results, f, indent=2, default=str)
print(f"wrote {OUT}")
