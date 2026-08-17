"""evenxval_compare.py -- compare the independent mpmath builder
(evenxval_mp.json) against the certified Arb builder (evenxval_ref.json)
point-by-point.  Relative error = |mp - ref| / |ref|.  Gate: <= 1e-8 at
every point; > 1e-6 is a LOUD finding and is reported as such.

Run with: /Users/za/miniforge3/envs/pari-arb/bin/python3
"""
from __future__ import annotations
import json
import os

import mpmath as mp

mp.mp.dps = 50

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "evenxval_compare.json")

GATE = 1e-8
LOUD = 1e-6


def load(name):
    with open(os.path.join(HERE, name)) as f:
        return json.load(f)


def arb_mid(s):
    """Midpoint of an Arb ball string '[mid +/- rad]' (or a plain number)."""
    return s.split("+/-")[0].strip().lstrip("[").rstrip("]").strip()


def main():
    mp_rows = load("evenxval_mp.json")["points"]
    ref_rows = load("evenxval_ref.json")["points"]
    ref = {(r["sigma"], r["t"], r["sign"]): r for r in ref_rows}
    table = []
    worst = mp.mpf(0)
    worst_at = None
    loud = []
    for r in mp_rows:
        key = (r["sigma"], r["t"], r["sign"])
        rr = ref[key]
        z_mp = mp.mpc(mp.mpf(r["det_re"]), mp.mpf(r["det_im"]))
        z_rf = mp.mpc(mp.mpf(arb_mid(rr["det_re"])),
                      mp.mpf(arb_mid(rr["det_im"])))
        rel = abs(z_mp - z_rf) / abs(z_rf)
        row = {
            "sigma": r["sigma"], "t": r["t"], "sign": r["sign"],
            "abs_ref": mp.nstr(abs(z_rf), 12),
            "rel_err": mp.nstr(rel, 6),
            "pass_1e-8": bool(rel < GATE),
            "tail_ref": rr["tail"],
        }
        table.append(row)
        if rel > worst:
            worst = rel
            worst_at = key
        if rel > LOUD:
            loud.append(row)
        print(f"sign={r['sign']:+d} s={r['sigma']}+i{r['t']:<5} "
              f"|ref|={mp.nstr(abs(z_rf), 6):>16}  rel_err={mp.nstr(rel, 3)} "
              f"{'PASS' if rel < GATE else 'FAIL'}")
    verdict = ("PASS: all 24 evaluations agree to <= 1e-8"
               if not loud and worst < GATE else
               ("LOUD: disagreement beyond 1e-6 at " +
                ", ".join(f"(sign={r['sign']:+d}, s={r['sigma']}+i{r['t']})"
                          for r in loud) if loud else
                "FAIL: some point(s) between 1e-8 and 1e-6"))
    rec = {
        "probe": "evenxval_compare",
        "gate": GATE, "loud_threshold": LOUD,
        "n_points": len(table),
        "worst_rel_err": mp.nstr(worst, 6),
        "worst_at": {"sigma": worst_at[0], "t": worst_at[1],
                     "sign": worst_at[2]},
        "loud_findings": loud,
        "verdict": verdict,
        "table": table,
    }
    with open(OUT, "w") as f:
        json.dump(rec, f, indent=2)
    print(f"\nworst rel err {mp.nstr(worst, 3)} at {worst_at}")
    print(verdict)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
