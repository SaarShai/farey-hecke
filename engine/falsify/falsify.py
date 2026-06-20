"""
engine/falsify/falsify.py
=========================
FALSIFY stage of the Aletheia certified-math engine (see engine/GOAL.md).

A reusable, CONFIG-DRIVEN adversarial-refutation harness. Given a numerical
`Claim`, it runs a BATTERY of refutation attempts and returns a `FalsifyReport`
with verdict "survives" iff EVERY attempt passes. A refutation harness DEFAULTS
TO SKEPTICISM: any attempt that errors, times out, returns an undecided/None
score, or is simply MISSING is treated as a FAILURE -> the claim is refuted.
A claim only survives if it actively passes every adversarial probe we threw.

The four standard attempts (each supplied by the caller as a callable in
`claim["params"]`):

  (a) CONTROL      -- a case where the claim should NOT hold; must behave
                      DIFFERENTLY from the claim case (e.g. arithmetic q=3 vs
                      non-arith q=5, or the wrong spectral sector).
  (b) INDEPENDENT  -- a second computation / path of the SAME quantity must
                      AGREE with the primary computation.
  (c) STABILITY    -- vary truncation N / precision / grid: a genuine result is
                      stable; an artifact drifts.
  (d) NULL         -- a neighboring / off point must NOT also satisfy the claim.

Contract (engine/GOAL.md):
  FalsifyReport = {claim_id, attempts: [{name, method, result}], verdict, evidence}

Each attempt callable receives the claim's `params` dict and must return an
"attempt result" dict. The harness interprets it via a `passed` field:
  {"passed": bool, "method": str, "detail": str, ... arbitrary diagnostics ...}
If a callable returns something without a usable boolean `passed`, or raises,
or is absent, the attempt is scored FAILED (skeptical default).

The Hecke reference plugin lives in `hecke_plugin.py`; see `make_resonance_claim`.

This module imports nothing heavy (no Arb). All numeric work lives in the
caller-supplied callables, so the harness is domain-agnostic and unit-testable
with pure-Python stubs.
"""
from __future__ import annotations

import json
import os
import time
import traceback
from typing import Any, Callable, Dict, List, Optional

# The four standard adversarial attempts, in the order the contract names them.
# Each maps attempt name -> the params-key holding its callable.
ATTEMPT_SPECS = [
    ("control", "control_fn"),
    ("independent", "independent_fn"),
    ("stability", "sweep_fn"),
    ("null", "null_fn"),
]


def _coerce_result(name: str, fn_key: str, raw: Any) -> Dict[str, Any]:
    """Normalize whatever an attempt callable returned into a scored result.

    SKEPTICAL: anything we can't read as an explicit pass is a FAIL.
    """
    if not isinstance(raw, dict):
        return {
            "name": name,
            "method": fn_key,
            "passed": False,
            "scored": False,
            "detail": f"attempt callable returned non-dict ({type(raw).__name__}); "
                      "cannot score -> treated as FAILED (skeptical default)",
        }
    passed = raw.get("passed", None)
    if not isinstance(passed, bool):
        out = dict(raw)
        out.update({
            "name": name,
            "method": raw.get("method", fn_key),
            "passed": False,
            "scored": False,
            "detail": "attempt result lacked a boolean 'passed' field -> "
                      "treated as FAILED (skeptical default). "
                      + str(raw.get("detail", "")),
        })
        return out
    out = dict(raw)
    out.update({
        "name": name,
        "method": raw.get("method", fn_key),
        "passed": bool(passed),
        "scored": True,
    })
    return out


def _run_one(name: str, fn_key: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Run one attempt callable defensively. Missing/raising -> FAILED."""
    fn = params.get(fn_key, None)
    if fn is None:
        return {
            "name": name,
            "method": fn_key,
            "passed": False,
            "scored": False,
            "detail": f"no '{fn_key}' supplied in claim params -> attempt MISSING "
                      "-> treated as FAILED (skeptical default). A claim cannot "
                      "survive an un-run adversarial probe.",
        }
    if not callable(fn):
        return {
            "name": name,
            "method": fn_key,
            "passed": False,
            "scored": False,
            "detail": f"'{fn_key}' is not callable ({type(fn).__name__}) -> FAILED.",
        }
    t0 = time.time()
    try:
        raw = fn(params)
    except Exception as exc:  # noqa: BLE001  -- harness must swallow & score
        return {
            "name": name,
            "method": fn_key,
            "passed": False,
            "scored": False,
            "detail": f"attempt raised {type(exc).__name__}: {exc} -> FAILED "
                      "(skeptical default).",
            "traceback": traceback.format_exc(limit=6),
            "seconds": time.time() - t0,
        }
    res = _coerce_result(name, fn_key, raw)
    res["seconds"] = time.time() - t0
    return res


def falsify(claim: Dict[str, Any]) -> Dict[str, Any]:
    """Run the adversarial battery against `claim`; return a FalsifyReport dict.

    `claim` must follow the engine Claim contract:
        {id, statement, kind, artifact, params}
    where `params` carries the attempt callables (control_fn, independent_fn,
    sweep_fn, null_fn) plus whatever data they need.

    Returns FalsifyReport = {claim_id, attempts, verdict, evidence}.
    verdict == "survives" iff EVERY standard attempt passed; else "refuted".
    """
    claim_id = claim.get("id", "<no-id>")
    params = claim.get("params", {}) or {}

    attempts: List[Dict[str, Any]] = []
    for name, fn_key in ATTEMPT_SPECS:
        res = _run_one(name, fn_key, params)
        # The contract's attempt shape is {name, method, result}. We keep that
        # outer shape and stash the full diagnostic dict under "result".
        attempts.append({
            "name": res["name"],
            "method": res["method"],
            "result": res,
        })

    n_total = len(attempts)
    n_passed = sum(1 for a in attempts if a["result"].get("passed") is True)
    n_scored = sum(1 for a in attempts if a["result"].get("scored") is True)
    survives = (n_passed == n_total) and (n_scored == n_total)
    verdict = "survives" if survives else "refuted"

    failed = [a["name"] for a in attempts if a["result"].get("passed") is not True]

    evidence = {
        "n_attempts": n_total,
        "n_passed": n_passed,
        "n_scored": n_scored,
        "failed_attempts": failed,
        "rule": "survives iff ALL attempts pass AND all were actually scored; "
                "uncertain/missing/erroring => refuted (skeptical default).",
        "statement": claim.get("statement", ""),
        "per_attempt": {
            a["name"]: {
                "passed": a["result"].get("passed"),
                "detail": a["result"].get("detail", ""),
            } for a in attempts
        },
    }

    return {
        "claim_id": claim_id,
        "attempts": attempts,
        "verdict": verdict,
        "evidence": evidence,
    }


# ---------------------------------------------------------------------------
#  numpy-free JSON helper (Arb / numpy objects are stringified defensively).
# ---------------------------------------------------------------------------
def _san(o: Any) -> Any:
    if isinstance(o, dict):
        return {str(k): _san(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_san(v) for v in o]
    if isinstance(o, bool) or o is None:
        return o
    if isinstance(o, (int, float, str)):
        return o
    # callables, Arb balls, numpy scalars, etc. -> repr (never crash the dump)
    try:
        return float(o)  # numpy scalars
    except Exception:  # noqa: BLE001
        return repr(o)


def save_report(report: Dict[str, Any], path: str) -> str:
    """Atomic numpy/Arb-safe JSON write of a FalsifyReport."""
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(_san(report), f, indent=2)
    os.replace(tmp, path)
    return path
