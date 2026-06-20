"""
engine/falsify/smoke_test.py
============================
Self-contained smoke test for the FALSIFY harness (engine/falsify/falsify.py)
and its Hecke reference plugin (hecke_plugin.py).

Runs and ASSERTS three things:

  (1) VERIFIED G_5 even resonance  s = 0.4539 + 5.7635i  -> verdict "survives"
      (all four adversarial attempts pass against the certified Arb engine).

  (2) BOGUS claim                  s = 0.30 + 8.5i        -> verdict "refuted"
      (the point is not a resonance: null/stability/independent fail).

  (3) Pure-Python SKEPTICAL-DEFAULT checks (no Arb): a claim with a MISSING
      attempt, and one with an ERRORING attempt, must both be "refuted" --
      proving the harness defaults to skepticism on uncertainty.

Light by design: q=5, N in {18,20,22}; heavy jobs may be running concurrently.

Run:
    cd engine/falsify && python3 smoke_test.py
"""
from __future__ import annotations

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import falsify
from hecke_plugin import make_resonance_claim


def _print_report(tag, report):
    print(f"\n=== {tag} ===")
    print(f"claim_id: {report['claim_id']}")
    print(f"VERDICT : {report['verdict']}")
    for a in report["attempts"]:
        r = a["result"]
        mark = "PASS" if r.get("passed") else "FAIL"
        print(f"  [{mark}] {a['name']:<11} ({r.get('seconds', 0):.1f}s) :: {r.get('detail','')}")


def _pure_python_skeptic_checks():
    """No Arb. Verify missing + erroring attempts force 'refuted'."""
    ok = {"passed": True, "method": "stub-ok", "detail": "stub passes"}

    def good(_p):
        return ok

    def boom(_p):
        raise RuntimeError("simulated attempt failure")

    # (3a) MISSING attempt (no null_fn) -> refuted
    claim_missing = {
        "id": "stub_missing_null", "statement": "stub", "kind": "numerical",
        "artifact": "none",
        "params": {"control_fn": good, "independent_fn": good, "sweep_fn": good},
    }
    rep_missing = falsify.falsify(claim_missing)
    assert rep_missing["verdict"] == "refuted", rep_missing
    assert "null" in rep_missing["evidence"]["failed_attempts"], rep_missing

    # (3b) ERRORING attempt -> refuted, and the error is captured
    claim_err = {
        "id": "stub_erroring", "statement": "stub", "kind": "numerical",
        "artifact": "none",
        "params": {"control_fn": good, "independent_fn": boom,
                   "sweep_fn": good, "null_fn": good},
    }
    rep_err = falsify.falsify(claim_err)
    assert rep_err["verdict"] == "refuted", rep_err
    assert "independent" in rep_err["evidence"]["failed_attempts"], rep_err

    # (3c) ALL stubs pass -> survives (control logic sanity)
    claim_all = {
        "id": "stub_all_pass", "statement": "stub", "kind": "numerical",
        "artifact": "none",
        "params": {"control_fn": good, "independent_fn": good,
                   "sweep_fn": good, "null_fn": good},
    }
    rep_all = falsify.falsify(claim_all)
    assert rep_all["verdict"] == "survives", rep_all

    print("\n=== (3) pure-Python skeptical-default checks ===")
    print(f"  missing null_fn      -> {rep_missing['verdict']:<8} (failed: "
          f"{rep_missing['evidence']['failed_attempts']})")
    print(f"  erroring independent -> {rep_err['verdict']:<8} (failed: "
          f"{rep_err['evidence']['failed_attempts']})")
    print(f"  all stubs pass       -> {rep_all['verdict']:<8}")


def main():
    t0 = time.time()
    failures = []

    # (3) cheap pure-Python contract checks first (no Arb dependency).
    _pure_python_skeptic_checks()

    # (1) VERIFIED G_5 even resonance -> survives.
    good_claim = make_resonance_claim(
        re=0.4538951800749447, im=5.7635372417301305,
        q=5, N=18, N_independent=22, N_sweep=(18, 20, 22),
    )
    rep_good = falsify.falsify(good_claim)
    _print_report("(1) VERIFIED resonance s=0.4539+5.7635i (expect SURVIVES)", rep_good)
    if rep_good["verdict"] != "survives":
        failures.append(f"(1) expected survives, got {rep_good['verdict']}")

    # (2) BOGUS claim -> refuted.
    bogus_claim = make_resonance_claim(
        re=0.30, im=8.5,
        q=5, N=18, N_independent=22, N_sweep=(18, 20, 22),
    )
    rep_bogus = falsify.falsify(bogus_claim)
    _print_report("(2) BOGUS claim s=0.30+8.5i (expect REFUTED)", rep_bogus)
    if rep_bogus["verdict"] != "refuted":
        failures.append(f"(2) expected refuted, got {rep_bogus['verdict']}")

    # Persist the two Hecke reports as artifacts (atomic, Arb-safe).
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
    falsify.save_report(rep_good, os.path.join(out_dir, "falsify_verified_resonance.json"))
    falsify.save_report(rep_bogus, os.path.join(out_dir, "falsify_bogus_claim.json"))

    print(f"\n--- wrote reports to {out_dir}/ ---")
    print(f"--- total {time.time()-t0:.1f}s ---")

    if failures:
        print("\nSMOKE TEST FAILED:")
        for f in failures:
            print("  -", f)
        sys.exit(1)
    print("\nSMOKE TEST PASSED: verified->survives, bogus->refuted, "
          "skeptical-defaults->refuted.")
    sys.exit(0)


if __name__ == "__main__":
    main()
