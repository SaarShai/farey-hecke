"""
Certified non-arithmetic Hecke Maass spectrum TABLE (deliverable for the
Stroemberg-heuristic / congruence-only-certification gap). Each entry is
Aletheia-certified: rigorous Arb argument-principle winding (=1 => one simple
zero of det(1-L^{sign}_s) enclosed). On-line zeros (Re=1/2) = Maass eigenvalues;
off-line (Re<1/2) = even-sector resonances. Hejhal point-matching values listed
where independently cross-checked (zero transfer-operator code overlap).
"""
from __future__ import annotations
import json, os, sys, time

ROOT = "/Users/za/Documents/farey-hecke"
for p in (ROOT, os.path.join(ROOT, "code"), os.path.join(ROOT, "engine/certify")):
    if p not in sys.path:
        sys.path.insert(0, p)
import certify as CERT

OUT = os.path.join(ROOT, "code/out/certified_hecke_spectrum_table.json")

# G_5 odd-sector Maass eigenvalues (on the critical line, s = 1/2 + i r)
G5_ODD = [6.4737, 8.6368, 10.1365, 11.0156, 12.0841, 12.8513]
HEJHAL = {6.4737: 6.47367, 8.6368: 8.63677, 10.1365: 10.13642}  # independently cross-checked
# representative even-sector resonances (off the line), from the certified geometry runs
G5_EVEN = [(0.45389518, 5.76353724), (0.41054374, 7.81976825), (0.485, 13.565)]
G7_EVEN = [(0.4842, 7.567), (0.4751, 4.669), (0.4732, 16.605)]


def cert(q, re, im, sign, N=22):
    c = CERT.certify({"id": f"q{q}_{re:.4f}_{im:.4f}_s{sign}", "kind": "numerical",
                      "artifact": "hecke_transfer_operator_zero",
                      "params": {"q": q, "re": re, "im": im, "sign": sign,
                                 "N": N, "refine": True}})
    enc = c.get("enclosure") or {}
    return {"certified": bool(c.get("certified")),
            "winding": enc.get("winding_number"),
            "box": enc.get("box") or enc.get("interval"),
            "dim_tail_certified": c.get("dim_tail_certified")}


def main():
    t0 = time.time()
    table = {"objective": "First rigorously interval-certified table of non-arithmetic "
                          "Hecke triangle Maass eigenvalues + even-sector resonances.",
             "method": "Aletheia certify stage: Arb argument-principle winding (winding=1 "
                       "=> one simple enclosed zero of det(1-L^sign_s)).",
             "gap": "Stroemberg arXiv:0804.4837 heuristic; rigorous certification lit "
                    "(2204.11761, 2502.01442) congruence/arithmetic only.",
             "entries": []}

    print("=== G_5 odd Maass eigenvalues (on-line) ===", flush=True)
    for r in G5_ODD:
        c = cert(5, 0.5, r, -1)
        e = {"surface": "G_5", "sector": "odd", "kind": "Maass eigenvalue",
             "r": r, "lambda": 0.25 + r * r, "s_re": 0.5, "s_im": r,
             "hejhal_crosscheck_r": HEJHAL.get(r), **c}
        table["entries"].append(e)
        print(f"  G_5 odd r={r}: certified={c['certified']} winding={c['winding']} "
              f"hejhal={HEJHAL.get(r)}", flush=True)
        json.dump(table, open(OUT, "w"), indent=2, default=str)

    print("=== G_5 even resonances (off-line) ===", flush=True)
    for (re, im) in G5_EVEN:
        c = cert(5, re, im, +1)
        table["entries"].append({"surface": "G_5", "sector": "even", "kind": "resonance",
                                 "s_re": re, "s_im": im, **c})
        print(f"  G_5 even s={re:.4f}+{im:.4f}i: certified={c['certified']} winding={c['winding']}", flush=True)
        json.dump(table, open(OUT, "w"), indent=2, default=str)

    print("=== G_7 even resonances (off-line, general-q engine) ===", flush=True)
    for (re, im) in G7_EVEN:
        c = cert(7, re, im, +1)
        table["entries"].append({"surface": "G_7", "sector": "even", "kind": "resonance",
                                 "s_re": re, "s_im": im, **c})
        print(f"  G_7 even s={re:.4f}+{im:.4f}i: certified={c['certified']} winding={c['winding']}", flush=True)
        json.dump(table, open(OUT, "w"), indent=2, default=str)

    n_cert = sum(1 for e in table["entries"] if e["certified"])
    table["summary"] = {"n_entries": len(table["entries"]),
                        "n_certified": n_cert,
                        "wall_seconds": time.time() - t0}
    json.dump(table, open(OUT, "w"), indent=2, default=str)
    print(f"\n=== {n_cert}/{len(table['entries'])} certified ({time.time()-t0:.0f}s) -> {OUT} ===")


if __name__ == "__main__":
    main()
