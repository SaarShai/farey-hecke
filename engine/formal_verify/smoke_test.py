"""Self-contained smoke test for the Aletheia VERIFY stage.

Exercises the REQUIRED post-processing path WITHOUT submitting a new (billable)
Aristotle job: it points at an EXISTING completed project and asserts the
ProofCertificate contract.

    project_id 3d185f73-bec0-4932-a2e7-0ef18f0a8948
      -> poll (already COMPLETE) -> download (gzipped tar) -> extract
      -> Main.lean sorry-free  AND  ARISTOTLE_SUMMARY.md axiom check
      -> emit ProofCertificate with proved=True

Run:  python3 engine/formal_verify/smoke_test.py
Exit 0 on PASS, 1 on FAIL.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import formal_verify as fv  # noqa: E402

EXISTING_PROJECT_ID = "3d185f73-bec0-4932-a2e7-0ef18f0a8948"
LEMMA = (
    "hecke_lambda_five: for x = 2*cos(pi/5), x^2 - x - 1 = 0; "
    "hecke_lambda_seven: for x = 2*cos(pi/7), x^3 - x^2 - 2*x + 1 = 0"
)
EXPECTED_AXIOMS = fv.CLEAN_AXIOMS  # [propext, Classical.choice, Quot.sound]


def main() -> int:
    print(f"[smoke] post-processing existing project {EXISTING_PROJECT_ID}")
    cert = fv.verify_project(EXISTING_PROJECT_ID, lemma=LEMMA, claim_id="hecke_minpoly_lambda")

    print("[smoke] ProofCertificate:")
    print(json.dumps(cert, indent=2))

    failures: list[str] = []

    # Contract-shape checks.
    for key in ("claim_id", "lemma", "lean_file", "sorry_free", "axioms", "proved"):
        if key not in cert:
            failures.append(f"missing contract key: {key}")

    if cert.get("status") != "COMPLETE":
        failures.append(f"status != COMPLETE: {cert.get('status')}")
    if cert.get("sorry_free") is not True:
        failures.append(f"sorry_free is not True: {cert.get('sorry_free')}")
    if cert.get("axioms") != EXPECTED_AXIOMS:
        failures.append(f"axioms {cert.get('axioms')} != {EXPECTED_AXIOMS}")
    if cert.get("proved") is not True:
        failures.append(f"proved is not True: {cert.get('proved')}")
    lf = cert.get("lean_file")
    if not (lf and Path(lf).name == "Main.lean"):
        failures.append(f"lean_file not a Main.lean path: {lf}")

    if failures:
        print("\n[smoke] FAIL")
        for f in failures:
            print(f"  - {f}")
        return 1

    print("\n[smoke] PASS: sorry_free=True, axioms==clean set, proved=True")
    print("[smoke] (build/axiom result is Aristotle-reported, not re-run locally)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
