"""f7links_e1_recheck.py -- independent re-derivation of the q=7 E1 gate
(assembly link 4b) from the RAW per-block fields of the banked receipt.

This does NOT re-run the enlarged-contour certification (that is
f7_stage4b_reopt.py, ~175 s). It re-derives every summary field of
f7_receipts/F7_E1_ENLARGED_CONTRACTION_V2_RECEIPT.json from its 19 raw
per-block ball strings, in Arb ball arithmetic, so no hard-coded summary
literal is trusted (the 1-C5 discipline of F7_R3B_ASSEMBLY_CERT.md).

Checks, per block:
  (a) ratio_upper_bound < 1                          [the rho_hat gate]
  (b) eta = R/R_enlarged < 1
  (c) remaining pole/branch-cut clearance > 0        [Clause-2a holomorphy]
  (d) enlargement > 0 and enlargement = R_enl - R    [internal consistency]
  (e) enlargement <= 0.15 * R  and  <= clearance/4   [the recorded rule]
and globally: rho_hat = max ratio, eta_max = max eta, both re-derived and
compared with the receipt's own summary strings; rho_hat below the q=5 chain's
rho_hat <= 0.948343590350471954782853.

Writes f7_receipts/F7LINKS_E1_RECHECK_RECEIPT.json only.
Interpreter: /Users/za/.venvs/farey-rh/bin/python
"""

import json
import os

from flint import arb, ctx

PREC = 384
ctx.prec = PREC

Q5_RHO_HAT = "0.948343590350471954782853"

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "f7_receipts", "F7_E1_ENLARGED_CONTRACTION_V2_RECEIPT.json")
rec = json.load(open(src))


def ball(s):
    """Parse a flint ball string '[mid +/- rad]' back into an arb."""
    s = s.strip()
    assert s.startswith("[") and s.endswith("]"), s
    body = s[1:-1]
    if "+/-" in body:
        mid, rad = body.split("+/-")
        return arb(mid.strip(), rad.strip())
    return arb(body.strip())


def upper_str(x, digits):
    scale = 10 ** digits
    units = int((x.upper() * scale).ceil().unique_fmpz())
    for _ in range(4):
        if x < arb(units) / scale:
            s = str(abs(units)).rjust(digits + 1, "0")
        else:
            units += 1
            continue
        sign = "-" if units < 0 else ""
        return f"{sign}{s[:len(s) - digits]}.{s[len(s) - digits:]}"
    raise AssertionError("no certified ceiling")


cap = arb(rec["enlargement_relative_cap"])
rows = []
rho_hat = None
eta_max = None
for b in rec["per_block"]:
    R = ball(b["original_radius_upper_bound"])
    Renl = ball(b["enlarged_radius"])
    e = ball(b["enlargement_lower_bound"])
    clr = ball(b["certified_clearance_lower_bound"])
    rem = ball(b["remaining_pole_cut_clearance_lower_bound"])
    ratio = ball(b["ratio_upper_bound"])
    eta = ball(b["eta_R_over_R_enlarged_upper_bound"])

    checks = {
        "ratio_lt_1": bool(ratio < arb(1)),
        "eta_lt_1": bool(eta < arb(1)),
        "remaining_clearance_positive": bool(rem > arb(0)),
        "enlargement_positive": bool(e > arb(0)),
        # R_enl = R + e up to ball overlap (the receipt stores directed bounds)
        "enlarged_radius_consistent": bool(((R + e) - Renl).abs_upper() < arb(10) ** -30),
        "enlargement_within_relative_cap": bool(e < cap * R * (1 + arb(10) ** -30)),
        "enlargement_within_quarter_clearance": bool(e < clr / 4 * (1 + arb(10) ** -30)),
        # eta is R/R_enl; re-derive it
        "eta_consistent": bool((eta - R / Renl).abs_upper() < arb(10) ** -30),
        # remaining clearance = clearance - enlargement
        "remaining_clearance_consistent":
            bool(((clr - e) - rem).abs_upper() < arb(10) ** -30),
    }
    rows.append({"label": b["label"], "tail": b["tail"],
                 "ratio_upper_rounded_up": upper_str(ratio, 12),
                 "eta_upper_rounded_up": upper_str(eta, 12),
                 "remaining_clearance_lower": b["remaining_pole_cut_clearance_lower_bound"][:30] + "...",
                 "checks": checks,
                 "all_checks_pass": all(checks.values())})
    if rho_hat is None or ratio.upper() > rho_hat.upper():
        rho_hat, rho_label = ratio, b["label"]
    if eta_max is None or eta.upper() > eta_max.upper():
        eta_max = eta

out = {
    "schema": "f7links-e1-recheck/v1",
    "precision_bits": PREC,
    "backend": "python-flint Arb ball arithmetic (re-derivation from raw fields)",
    "source_receipt": os.path.relpath(src, here),
    "source_receipt_verdict": rec["verdict"],
    "blocks_seen": len(rows),
    "expected_blocks": 19,
    "block_count_ok": len(rows) == 19,
    "per_block": rows,
    "all_blocks_pass_all_checks": all(r["all_checks_pass"] for r in rows),
    "rho_hat_rederived_upper_rounded_up": upper_str(rho_hat, 16),
    "rho_hat_worst_block": rho_label,
    "rho_hat_matches_receipt_summary":
        bool((rho_hat - ball(rec["rho_hat_upper_bound"])).abs_upper() < arb(10) ** -40),
    "rho_hat_worst_block_matches_receipt":
        rho_label == rec["rho_hat_worst_block_label"],
    "eta_max_rederived_upper_rounded_up": upper_str(eta_max, 16),
    "eta_max_matches_receipt_summary":
        bool((eta_max - ball(rec["eta_max_upper_bound"])).abs_upper() < arb(10) ** -40),
    "rho_hat_below_q5_chain_value": bool(rho_hat < arb(Q5_RHO_HAT)),
    "q5_rho_hat": Q5_RHO_HAT,
    "enlargement_rule": rec["enlargement_rule"],
    "enlargement_relative_cap": rec["enlargement_relative_cap"],
    "immutable_inputs": rec["immutable_inputs"],
}
out["all_gates_pass"] = all([out["block_count_ok"],
                            out["all_blocks_pass_all_checks"],
                            out["rho_hat_matches_receipt_summary"],
                            out["rho_hat_worst_block_matches_receipt"],
                            out["eta_max_matches_receipt_summary"],
                            out["rho_hat_below_q5_chain_value"]])
out["verdict"] = ("PASS_E1_REDERIVED_FROM_RAW_FIELDS" if out["all_gates_pass"]
                  else "FAIL")

dest = os.path.join(here, "f7_receipts", "F7LINKS_E1_RECHECK_RECEIPT.json")
with open(dest, "w") as fh:
    json.dump(out, fh, indent=1, sort_keys=True)
summary = {k: v for k, v in out.items() if k != "per_block"}
print(json.dumps(summary, indent=1, sort_keys=True))
for r in rows:
    print(f"  {r['label']:<22} ratio<= {r['ratio_upper_rounded_up']}  "
          f"eta<= {r['eta_upper_rounded_up']}  ok={r['all_checks_pass']}")
print("\nwrote", dest)
