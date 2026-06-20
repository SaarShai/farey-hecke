#!/usr/bin/env python3
"""Self-contained smoke test for the Aletheia orchestrator.

Runs ``orchestrator.run`` on a trivial claim end-to-end. The three pipeline
stages (falsify / certify / verify) are imported lazily by the orchestrator:
if a sibling module is importable it is used, otherwise a clearly-labelled stub
is substituted. EITHER WAY this test must pass: it asserts the orchestrator
produces a structurally valid RunRecord and writes it to engine/runs/.

To keep the smoke test hermetic (no dependence on whatever real stage modules
happen to exist), it ALSO injects in-process fake stage modules so the "real
module importable" code path is exercised deterministically. The on-disk
RunRecord, however, is produced with the *actual* environment so the report
reflects reality.

Run:
    python3 engine/orchestrator/smoke_test.py
Exit code 0 = pass, 1 = fail.
"""

from __future__ import annotations

import json
import os
import sys
import types

# Allow `import orchestrator` whether run as a file or as a module.
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_ENGINE_DIR = os.path.dirname(_THIS_DIR)
for p in (_THIS_DIR, _ENGINE_DIR):
    if p not in sys.path:
        sys.path.insert(0, p)

# Import the orchestrator MODULE specifically (not the package __init__), so the
# full surface — including SCHEMA and internal helpers — is available regardless
# of whether bare `orchestrator` resolves to the package dir or the file.
import importlib  # noqa: E402

try:
    orchestrator = importlib.import_module("orchestrator.orchestrator")  # package form
except Exception:
    orchestrator = importlib.import_module("orchestrator")              # bare-file form


TRIVIAL_CLAIM = {
    "id": "smoke-trivial-001",
    "statement": "2 + 2 = 4",
    "kind": "numerical",
    "artifact": None,
    "params": {},
}


def _validate_runrecord(rec: dict) -> None:
    """Assert the RunRecord has the contract shape; raise AssertionError if not."""
    required = ["run_id", "schema", "claim", "falsify", "certify", "verify",
                "synthesis", "stage_status", "verdict", "timestamps"]
    for k in required:
        assert k in rec, f"RunRecord missing required key: {k!r}"
    assert rec["schema"] == orchestrator.SCHEMA, "schema mismatch"
    assert isinstance(rec["claim"], dict), "claim must be a dict"
    for stage in ("falsify", "certify", "verify"):
        assert isinstance(rec[stage], dict), f"{stage} artifact must be a dict"
        assert stage in rec["stage_status"], f"stage_status missing {stage}"
        src = rec["stage_status"][stage]["source"]
        assert src in ("real", "stub"), f"bad stage source: {src!r}"
    assert isinstance(rec["synthesis"], str) and rec["synthesis"], "empty synthesis"
    assert rec["verdict"] in ("survives", "refuted", "unknown"), "bad verdict"
    # JSON round-trip must succeed (proves serialisability).
    json.loads(json.dumps(rec, default=str))


def _report_sources(rec: dict, label: str) -> None:
    print(f"  [{label}] stage sources: " + ", ".join(
        f"{s}={rec['stage_status'][s]['source']}"
        for s in ("falsify", "certify", "verify")
    ))


def main() -> int:
    print("== Aletheia orchestrator smoke test ==")
    failures = []

    # ---- Phase A: REAL environment (stubs unless siblings are built) ------- #
    print("\n[A] run() against the ACTUAL environment, writing to engine/runs/")
    rec_real = orchestrator.run(TRIVIAL_CLAIM, counter=0, timestamp="2026-06-20T00:00:00Z")
    try:
        _validate_runrecord(rec_real)
        _report_sources(rec_real, "real-env")
        out_path = os.path.join(_ENGINE_DIR, "runs", rec_real["run_id"] + ".json")
        assert os.path.isfile(out_path), f"RunRecord not written to {out_path}"
        print(f"  RunRecord written: {out_path}")
        print("  PASS: valid RunRecord produced + persisted")
    except AssertionError as e:
        failures.append(f"phase A: {e}")
        print(f"  FAIL: {e}")

    # ---- Phase B: FAKE real stages injected (exercise the real-call path) -- #
    print("\n[B] run() with in-process FAKE stage modules (real-call path)")
    _inject_fake_stages()
    rec_fake = orchestrator.run(
        TRIVIAL_CLAIM, counter=1, timestamp="2026-06-20T00:00:00Z",
        write=False,
    )
    try:
        _validate_runrecord(rec_fake)
        _report_sources(rec_fake, "fake-real")
        for stage in ("falsify", "certify", "verify"):
            assert rec_fake["stage_status"][stage]["source"] == "real", \
                f"{stage} should have used the injected fake (real path)"
        assert rec_fake["verdict"] == "survives", "fake falsify should report survives"
        assert rec_fake["certify"]["certified"] is True, "fake certify should certify"
        assert rec_fake["verify"]["proved"] is True, "fake verify should prove"
        assert "CAVEAT" not in rec_fake["synthesis"], \
            "no stub caveat expected when all stages real"
        print("  PASS: real-call path composes all three stages")
    except AssertionError as e:
        failures.append(f"phase B: {e}")
        print(f"  FAIL: {e}")
    finally:
        _remove_fake_stages()

    # ---- Phase C: a raising real stage downgrades to stub ------------------ #
    print("\n[C] run() with a RAISING fake stage (graceful stub fallback)")
    _inject_raising_falsify()
    rec_raise = orchestrator.run(
        TRIVIAL_CLAIM, counter=2, timestamp="2026-06-20T00:00:00Z",
        write=False,
    )
    try:
        _validate_runrecord(rec_raise)
        assert rec_raise["stage_status"]["falsify"]["source"] == "stub", \
            "raising stage must downgrade to stub"
        assert rec_raise["stage_status"]["falsify"]["error"], \
            "stub fallback must capture the error"
        print("  PASS: raising stage downgraded to stub without aborting pipeline")
    except AssertionError as e:
        failures.append(f"phase C: {e}")
        print(f"  FAIL: {e}")
    finally:
        _remove_fake_stages()

    print("\n== RESULT ==")
    if failures:
        for f in failures:
            print("  FAIL " + f)
        print("SMOKE TEST FAILED")
        return 1
    print("ALL PHASES PASSED")
    return 0


# --------------------------------------------------------------------------- #
# In-process fake stage modules (so the real-call path is testable without the
# sibling agents' code). These register under both the package name and the
# bare sibling-file name the orchestrator probes.
# --------------------------------------------------------------------------- #

_FAKE_NAMES = [
    "engine.falsify.falsify", "falsify.falsify",
    "engine.certify.certify", "certify.certify",
    "engine.formal_verify.formal_verify", "formal_verify.formal_verify",
]


def _mk_module(name: str, **fns):
    mod = types.ModuleType(name)
    for k, v in fns.items():
        setattr(mod, k, v)
    sys.modules[name] = mod
    return mod


def _fake_falsify(claim):
    return {
        "claim_id": claim["id"],
        "attempts": [{"name": "q=3 control", "method": "control", "result": "pass"}],
        "verdict": "survives",
        "evidence": "fake",
    }


def _fake_certify(claim):
    return {
        "claim_id": claim["id"], "method": "interval", "enclosure": "[3.9, 4.1]",
        "certified": True, "certificate_path": "/tmp/fake.json", "tool": "fake-Arb",
    }


def _fake_verify(lemma, project_dir):
    return {
        "claim_id": "smoke-trivial-001", "lemma": lemma,
        "lean_file": "Fake.lean", "sorry_free": True,
        "axioms": ["propext", "Classical.choice", "Quot.sound"], "proved": True,
    }


def _inject_fake_stages():
    for n in ("engine.falsify.falsify", "falsify.falsify"):
        _mk_module(n, falsify=_fake_falsify)
    for n in ("engine.certify.certify", "certify.certify"):
        _mk_module(n, certify=_fake_certify)
    for n in ("engine.formal_verify.formal_verify", "formal_verify.formal_verify"):
        _mk_module(n, verify=_fake_verify)


def _inject_raising_falsify():
    def _boom(claim):
        raise RuntimeError("simulated stage failure")
    for n in ("engine.falsify.falsify", "falsify.falsify"):
        _mk_module(n, falsify=_boom)


def _remove_fake_stages():
    for n in _FAKE_NAMES:
        sys.modules.pop(n, None)


if __name__ == "__main__":
    raise SystemExit(main())
