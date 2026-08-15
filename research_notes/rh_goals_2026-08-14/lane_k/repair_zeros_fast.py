# INDEX CONVENTION (fixed 2026-08-15): CSV 'index' is 1-BASED into
# the Odlyzko seed table: row index i <-> seeds[i-1] <-> mp.zetazero(i).
#!/usr/bin/env python3
"""Fast seed-validated repair: bisection on Hardy Z within seed-midpoint
brackets. For bad row at index i (0-based into Odlyzko zeros1.txt), the
bracket [(s[i-1]+s[i])/2, (s[i]+s[i+1])/2] contains exactly the i-th zero
(seed table verified complete over the range by the RvM count gate G5).
Z(t) = mp.siegelz is real on the critical line; a sign change in the
bracket pins the zero; bisection to width 1e-21.
Writes <csv>.repaired.csv + receipt. Same detection rule as before:
|gamma_refined - seed| > 1e-6.
"""
import csv, json, sys, glob
from mpmath import mp

mp.dps = 30
SEEDS = "/Users/za/Documents/farey-hecke/cluster_universality_test/zeros1.txt"
seeds = [float(l) for l in open(SEEDS) if l.strip()]

def bisect_zero(lo, hi):
    zlo, zhi = mp.siegelz(lo), mp.siegelz(hi)
    assert zlo * zhi < 0, f"no sign change in bracket ({lo},{hi})"
    while hi - lo > mp.mpf("1e-21"):
        mid = (lo + hi) / 2
        zm = mp.siegelz(mid)
        if zm == 0:
            return mid
        if zlo * zm < 0:
            hi, zhi = mid, zm
        else:
            lo, zlo = mid, zm
    return (lo + hi) / 2

for f in sorted(glob.glob(sys.argv[1])):
    rows = list(csv.DictReader(open(f)))
    bad = [r for r in rows if abs(float(r["gamma_refined"]) - seeds[int(r["index"]) - 1]) > 1e-6]
    receipt = {"file": f, "rows": len(rows), "bad": len(bad),
               "method": "siegelz bisection in seed-midpoint bracket, dps=30, width 1e-21",
               "repairs": []}
    for r in bad:
        i = int(r["index"])
        lo = mp.mpf((seeds[i - 2] + seeds[i - 1]) / 2)
        hi = mp.mpf((seeds[i - 1] + seeds[i]) / 2)
        g = bisect_zero(lo, hi)
        assert abs(float(g) - seeds[i - 1]) < 1e-6, f"bisected zero far from seed at {i}"
        d = mp.zeta(mp.mpf("0.5") + mp.mpc(0, 1) * g, derivative=1)
        resid = abs(mp.zeta(mp.mpf("0.5") + mp.mpc(0, 1) * g))
        receipt["repairs"].append({
            "index": i, "old": r["gamma_refined"], "new": mp.nstr(g, 28),
            "seed": repr(seeds[i - 1]),
            "old_minus_seed": float(r["gamma_refined"]) - seeds[i - 1],
            "residual": mp.nstr(resid, 5)})
        r["gamma_refined"] = mp.nstr(g, 30)
        r["abs_zeta_prime_sq"] = mp.nstr(abs(d) ** 2, 30)
        r["residual"] = mp.nstr(resid, 5)
    ts = [float(r["gamma_refined"]) for r in rows]
    receipt["monotone_after"] = all(b > a for a, b in zip(ts, ts[1:]))
    out = f.replace(".csv", ".repaired.csv")
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=rows[0].keys())
        w.writeheader(); w.writerows(rows)
    json.dump(receipt, open(out + ".receipt.json", "w"), indent=1)
    print(f, "bad:", len(bad), "monotone_after:", receipt["monotone_after"], flush=True)
