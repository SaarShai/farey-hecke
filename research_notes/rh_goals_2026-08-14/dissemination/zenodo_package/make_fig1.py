#!/usr/bin/env python3
"""Reproduce fig1_qop_hist.pdf from the d8 shard receipts.

Recipe (verbatim from the FIG-TODO comment in main.tex): for each of the
16 SHARD_a{0..3}_l{...}.json receipts, group qOp_upper by
.payload.arc (redundantly checked against .payload.records[*].arc_index),
parse each interval-valued string '[m +/- r]' and take the upper endpoint
m+r, and draw one step histogram per arc (60 common bins) plus a vertical
reference line at 1/(1+sqrt(2)) ~= 0.41421 ("square-box predictor").

Usage: python3 make_fig1.py [shard_receipts_d8/] [out.pdf]
"""
import glob
import json
import math
import re
import sys

INTERVAL_RE = re.compile(r"\[([^+\-\s][^\s]*)\s*\+/-\s*([^\]]+)\]")


def upper_endpoint(interval_str):
    m = INTERVAL_RE.match(interval_str.strip())
    if not m:
        raise ValueError(f"unparseable interval string: {interval_str!r}")
    mid, rad = float(m.group(1)), float(m.group(2))
    return mid + rad


def load_qop_upper_by_arc(shard_dir):
    by_arc = {0: [], 1: [], 2: [], 3: []}
    for path in sorted(glob.glob(f"{shard_dir}/SHARD_a*_l*.json")):
        if path.endswith(".ckpt.json"):
            continue
        with open(path) as f:
            d = json.load(f)
        arc = d["payload"]["arc"]
        for rec in d["payload"]["records"]:
            assert rec["arc_index"] == arc, f"arc_index mismatch in {path}"
            by_arc[arc].append(upper_endpoint(rec["qOp_upper"]))
    return by_arc


def main():
    shard_dir = sys.argv[1] if len(sys.argv) > 1 else "shard_receipts_d8"
    out_path = sys.argv[2] if len(sys.argv) > 2 else "fig1_qop_hist.pdf"

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    by_arc = load_qop_upper_by_arc(shard_dir)
    all_vals = [v for vs in by_arc.values() for v in vs]
    print(f"loaded {len(all_vals)} qOp_upper values across {len(by_arc)} arcs "
          f"(range {min(all_vals):.5f}-{max(all_vals):.5f})")

    bins = 60
    lo, hi = min(all_vals), max(all_vals)
    edges = [lo + (hi - lo) * i / bins for i in range(bins + 1)]

    fig, ax = plt.subplots(figsize=(7, 4.5))
    for arc in sorted(by_arc):
        ax.hist(by_arc[arc], bins=edges, histtype="step", linewidth=1.5,
                label=f"arc {arc}")
    ref = 1.0 / (1.0 + math.sqrt(2.0))
    ax.axvline(ref, color="black", linestyle="--", linewidth=1,
                label=f"square-box predictor 1/(1+sqrt2) = {ref:.5f}")
    ax.set_xlabel("qOp_upper")
    ax.set_ylabel("leaf count")
    ax.set_title("Per-arc distribution of qOp_upper, 1024 depth-8 leaves")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out_path)
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
