"""
engine/certify/smoke.py
=======================
Self-contained smoke test for the CERTIFY stage (engine/certify/certify.py).

Certifies two Hecke transfer-operator claims and asserts the expected verdicts:

  (1) RESONANCE   q=3 even, s = 0.25 + 7.0674 i  ->  certified True,  winding = 1
      (the established q=3 even on-line resonance; a simple enclosed zero).
  (2) NON-RESONANCE control  q=3 even, s = 0.30 + 8.5 i  ->  certified False,
      winding = 0  (no enclosed zero).

Lightweight by design: N=18, prec as in the engine (q=3 is the cheap kappa=1
scalar block).  Other heavy Arb jobs may be running -- this stays small.

Run:
    cd /Users/za/Documents/farey-hecke
    python3 engine/certify/smoke.py
Exit code 0 on PASS, 1 on FAIL.
"""
from __future__ import annotations

import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import certify as C  # noqa: E402


def _fmt(c):
    e = c["enclosure"]
    return (f"certified={c['certified']} winding={e['winding_number']} "
            f"|det|_center_mid={e['absdet_center_mid']:.3e} "
            f"dim_tail_certified={c['dim_tail_certified']} "
            f"-> {c['certificate_path']}")


def main() -> int:
    t0 = time.time()
    failures = []

    # (1) RESONANCE -- expect certified True, winding 1 ---------------------
    res_claim = {
        "id": "smoke_q3_even_resonance",
        "statement": ("s=0.25+7.0674i is a simple zero of det(1-L^+_s) for the "
                      "Hecke G_3 transfer operator (even/mms+ sector)"),
        "kind": "numerical",
        "artifact": "hecke_transfer_operator_zero",
        "params": {"q": 3, "re": 0.25, "im": 7.0674, "sign": +1, "N": 18},
    }
    print("[1/2] RESONANCE  q=3 even  s=0.25+7.0674i ...", flush=True)
    res = C.certify(res_claim)
    print("      " + _fmt(res), flush=True)
    if not (res["certified"] is True
            and res["enclosure"]["winding_number"] == 1):
        failures.append(
            f"resonance: expected certified=True winding=1, "
            f"got certified={res['certified']} "
            f"winding={res['enclosure']['winding_number']}")

    # (2) NON-RESONANCE control -- expect certified False, winding 0 --------
    ctl_claim = {
        "id": "smoke_q3_even_control",
        "statement": ("s=0.30+8.5i is a simple zero of det(1-L^+_s) for the "
                      "Hecke G_3 transfer operator (CONTROL: expected NO zero)"),
        "kind": "numerical",
        "artifact": "hecke_transfer_operator_zero",
        # refine OFF for the control: do NOT Newton-hunt for a nearby zero,
        # certify the stated point's box exactly (it should enclose nothing).
        "params": {"q": 3, "re": 0.30, "im": 8.5, "sign": +1, "N": 18,
                   "refine": False},
    }
    print("[2/2] CONTROL    q=3 even  s=0.30+8.5i  (expect no enclosed zero) ...",
          flush=True)
    ctl = C.certify(ctl_claim)
    print("      " + _fmt(ctl), flush=True)
    if not (ctl["certified"] is False
            and ctl["enclosure"]["winding_number"] == 0):
        failures.append(
            f"control: expected certified=False winding=0, "
            f"got certified={ctl['certified']} "
            f"winding={ctl['enclosure']['winding_number']}")

    # verify the certificate files are valid machine-checkable JSON ----------
    for c in (res, ctl):
        p = c["certificate_path"]
        if not os.path.exists(p):
            failures.append(f"certificate file missing: {p}")
            continue
        with open(p) as f:
            disk = json.load(f)
        for k in ("claim_id", "method", "enclosure", "certified",
                  "certificate_path", "tool"):
            if k not in disk:
                failures.append(f"certificate {p} missing contract key {k!r}")

    dt = time.time() - t0
    print(f"\n--- smoke summary ({dt:.1f}s) ---")
    if failures:
        print("RESULT: FAIL")
        for f in failures:
            print("  - " + f)
        return 1
    print("RESULT: PASS")
    print("  resonance   -> certified True,  winding 1 (simple zero enclosed)")
    print("  control     -> certified False, winding 0 (no enclosed zero)")
    print("  certificates written + valid JSON with all contract keys")
    return 0


if __name__ == "__main__":
    sys.exit(main())
