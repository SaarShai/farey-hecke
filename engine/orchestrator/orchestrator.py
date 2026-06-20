#!/usr/bin/env python3
"""Aletheia — pipeline orchestrator (the spine).

Composes the certified-math pipeline

    DISCOVER (scout) -> FALSIFY -> CERTIFY -> VERIFY -> SYNTHESIZE

into a single `run(claim) -> RunRecord` call, and writes a machine-auditable
provenance record to ``engine/runs/<run_id>.json``.

Design contract (see ``engine/GOAL.md``):

    certify.certify(claim: dict)              -> Certificate
    falsify.falsify(claim: dict)              -> FalsifyReport
    formal_verify.verify(lemma, project_dir)  -> ProofCertificate
    orchestrator.run(claim: dict)             -> RunRecord     # this module

The three stage modules are built CONCURRENTLY by sibling agents. This module
therefore imports them **lazily and defensively** inside ``run()``: if a module
is not importable yet (or raises on call), the orchestrator substitutes a
clearly-labelled stub artifact carrying ``{"stub": true}`` and keeps going. The
pipeline runs end-to-end either way, and the RunRecord states, per stage,
whether the artifact came from the real module or a stub.

Reproducibility: ``run_id`` is derived deterministically from the claim id plus
a per-claim counter; no wall-clock or RNG enters the id. Timestamps are recorded
for provenance but can be pinned via the optional ``timestamp`` argument so that
a run is byte-for-byte reproducible when desired.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import importlib
import importlib.util
import json
import os
import re
import sys
import traceback
from typing import Any, Callable, Dict, Optional, Tuple

# --------------------------------------------------------------------------- #
# Paths
# --------------------------------------------------------------------------- #

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))          # .../engine/orchestrator
_ENGINE_DIR = os.path.dirname(_THIS_DIR)                        # .../engine
_RUNS_DIR = os.path.join(_ENGINE_DIR, "runs")                  # .../engine/runs

# Make sibling-file imports possible even without package __init__.py files.
if _ENGINE_DIR not in sys.path:
    sys.path.insert(0, _ENGINE_DIR)


# --------------------------------------------------------------------------- #
# RunRecord format
# --------------------------------------------------------------------------- #
#
# A RunRecord is a plain JSON-serialisable dict (so it round-trips through
# engine/runs/<run_id>.json with no custom decoder). Shape (per GOAL.md, with
# orchestrator-added provenance fields):
#
#   {
#     "run_id":     str,            # deterministic: <claim_id>--NNNN
#     "schema":     "aletheia.runrecord/v1",
#     "claim":      dict,           # the input Claim (echoed verbatim)
#     "falsify":    dict,           # FalsifyReport  (or stub)
#     "certify":    dict,           # Certificate    (or stub)
#     "verify":     dict,           # ProofCertificate (or stub)
#     "synthesis":  str,            # honest one-paragraph summary
#     "stage_status": {             # provenance: real vs stub vs error, per stage
#         "falsify": {"source": "real"|"stub", "error": str|None},
#         "certify": {...},
#         "verify":  {...}
#     },
#     "verdict":    "survives"|"refuted"|"unknown",   # rolled up from falsify
#     "timestamps": {"started": iso8601, "finished": iso8601}
#   }
#
# `RunRecord` is exported as an alias of `dict` for type hints / discoverability.
RunRecord = Dict[str, Any]

SCHEMA = "aletheia.runrecord/v1"


# --------------------------------------------------------------------------- #
# run_id derivation (deterministic, no wall-clock / RNG)
# --------------------------------------------------------------------------- #

def _slug(text: str) -> str:
    """Filesystem-safe slug of a claim id."""
    s = re.sub(r"[^A-Za-z0-9._-]+", "-", str(text)).strip("-")
    return s or "claim"


def make_run_id(claim_id: str, counter: Optional[int] = None) -> str:
    """Derive a deterministic run id from a claim id + counter.

    If ``counter`` is None, scan ``engine/runs/`` for existing records of this
    claim and pick the next free integer. The id never embeds wall-clock time
    or randomness, so a given (claim_id, counter) pair always maps to the same
    file. Concurrent writers should pass an explicit ``counter`` to avoid races.
    """
    slug = _slug(claim_id)
    if counter is None:
        counter = _next_counter(slug)
    return f"{slug}--{counter:04d}"


def _next_counter(slug: str) -> int:
    """Next free counter for ``slug`` based on files already in runs/."""
    n = 0
    if os.path.isdir(_RUNS_DIR):
        pat = re.compile(r"^" + re.escape(slug) + r"--(\d+)\.json$")
        for fn in os.listdir(_RUNS_DIR):
            m = pat.match(fn)
            if m:
                n = max(n, int(m.group(1)) + 1)
    return n


# --------------------------------------------------------------------------- #
# Lazy, defensive stage loading
# --------------------------------------------------------------------------- #

def _try_import_attr(module_path: str, attr: str) -> Optional[Callable]:
    """Import ``module_path`` and return its ``attr``; None on any failure.

    Tries the package form first (e.g. ``engine.falsify.falsify``), then the
    bare sibling-file form (e.g. ``falsify.falsify``) since ``_ENGINE_DIR`` is
    on ``sys.path``. Returns None — never raises — if the module isn't built
    yet, isn't importable, or lacks the entrypoint.
    """
    candidates = [module_path]
    # Bare form: strip a leading "engine." so "engine.falsify.falsify" -> "falsify.falsify".
    if module_path.startswith("engine."):
        candidates.append(module_path[len("engine."):])
    for cand in candidates:
        try:
            mod = importlib.import_module(cand)
        except Exception:
            continue
        fn = getattr(mod, attr, None)
        if callable(fn):
            return fn
    return None


def _stub_falsify(claim: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "claim_id": claim.get("id"),
        "attempts": [],
        "verdict": "unknown",
        "evidence": "STUB: engine.falsify.falsify not importable at run time; "
                    "no adversarial refutation was performed.",
        "stub": True,
    }


def _stub_certify(claim: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "claim_id": claim.get("id"),
        "method": None,
        "enclosure": None,
        "certified": False,
        "certificate_path": None,
        "tool": None,
        "stub": True,
        "note": "STUB: engine.certify.certify not importable at run time; "
                "no interval/ball certificate was produced.",
    }


def _stub_verify(claim: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "claim_id": claim.get("id"),
        "lemma": claim.get("lemma") or claim.get("statement"),
        "lean_file": None,
        "sorry_free": False,
        "axioms": [],
        "proved": False,
        "stub": True,
        "note": "STUB: engine.formal_verify.verify not importable at run time; "
                "no Lean proof certificate was produced.",
    }


def _run_stage(
    name: str,
    real_fn: Optional[Callable],
    real_call: Callable[[Callable], Dict[str, Any]],
    stub_fn: Callable[[], Dict[str, Any]],
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Execute one pipeline stage with stub fallback + error capture.

    Returns ``(artifact, status)`` where status is
    ``{"source": "real"|"stub", "error": str|None}``. A real module that raises
    is downgraded to its stub with the traceback summarised in ``error`` — the
    pipeline never aborts on a single stage failure.
    """
    if real_fn is None:
        return stub_fn(), {"source": "stub", "error": None}
    try:
        artifact = real_call(real_fn)
        if not isinstance(artifact, dict):
            raise TypeError(
                f"{name} returned {type(artifact).__name__}, expected dict per GOAL.md"
            )
        # Mark provenance without clobbering a stage that self-declared a stub.
        artifact.setdefault("stub", False)
        return artifact, {"source": "real", "error": None}
    except Exception:
        err = traceback.format_exc(limit=4).strip()
        stub = stub_fn()
        stub["note"] = (
            f"STUB FALLBACK: real {name} raised at run time. "
            + stub.get("note", "")
        )
        stub["error"] = err
        return stub, {"source": "stub", "error": err.splitlines()[-1] if err else "error"}


# --------------------------------------------------------------------------- #
# Synthesis — honest one-paragraph summary
# --------------------------------------------------------------------------- #

def synthesize(run_record: RunRecord) -> str:
    """Emit an honest one-paragraph natural-language summary of a run.

    Reports what survived falsification, what was certified, and what was
    formally verified — and is explicit about any stage that was stubbed or
    failed, so the summary never overstates the run.
    """
    claim = run_record.get("claim", {}) or {}
    cid = claim.get("id", "<unknown>")
    stmt = claim.get("statement", "<no statement>")
    fal = run_record.get("falsify", {}) or {}
    cert = run_record.get("certify", {}) or {}
    ver = run_record.get("verify", {}) or {}
    status = run_record.get("stage_status", {}) or {}

    def _src(stage: str) -> str:
        return (status.get(stage, {}) or {}).get("source", "stub")

    parts = [f'Claim "{cid}" — {stmt}.']

    # FALSIFY
    if _src("falsify") == "stub":
        parts.append("Adversarial falsification was NOT run (stage stubbed), so "
                     "the claim has not been stress-tested.")
    else:
        verdict = fal.get("verdict", "unknown")
        n = len(fal.get("attempts", []) or [])
        if verdict == "survives":
            parts.append(f"It survived {n} adversarial refutation attempt(s) "
                         "(controls / independent methods / sweeps).")
        elif verdict == "refuted":
            parts.append(f"It was REFUTED by falsification ({n} attempt(s)); the "
                         "claim does not hold and downstream certificates are moot.")
        else:
            parts.append(f"Falsification ran ({n} attempt(s)) but returned an "
                         "inconclusive verdict.")

    # CERTIFY
    if _src("certify") == "stub":
        parts.append("No interval/ball certificate was produced (certify stubbed).")
    elif cert.get("certified"):
        encl = cert.get("enclosure")
        tool = cert.get("tool") or cert.get("method") or "interval arithmetic"
        encl_txt = f" (enclosure {encl})" if encl is not None else ""
        parts.append(f"It was rigorously certified by {tool}{encl_txt}.")
    else:
        parts.append("Certification ran but did NOT certify the claim "
                     "(enclosure not rigorous / inconclusive).")

    # VERIFY
    if _src("verify") == "stub":
        parts.append("No formal (Lean) proof was attempted (verify stubbed).")
    elif ver.get("proved") and ver.get("sorry_free"):
        axioms = ver.get("axioms") or []
        ax_txt = f" under axioms {axioms}" if axioms else ""
        parts.append(f"A sorry-free Lean proof was machine-verified{ax_txt}.")
    elif ver.get("proved"):
        parts.append("A Lean proof was produced but is NOT sorry-free / fully "
                     "axiom-clean.")
    else:
        parts.append("Formal verification ran but did not close the proof.")

    # Honest overall caveat.
    stubbed = [s for s in ("falsify", "certify", "verify") if _src(s) == "stub"]
    if stubbed:
        parts.append(f"CAVEAT: stage(s) {stubbed} were stubbed at run time, so "
                     "this run is a pipeline-composition demonstration, not a "
                     "fully certified result.")
    return " ".join(parts)


# --------------------------------------------------------------------------- #
# The spine: run()
# --------------------------------------------------------------------------- #

def run(
    claim: Dict[str, Any],
    *,
    counter: Optional[int] = None,
    timestamp: Optional[str] = None,
    project_dir: Optional[str] = None,
    write: bool = True,
    runs_dir: Optional[str] = None,
) -> RunRecord:
    """Compose FALSIFY -> CERTIFY -> VERIFY -> SYNTHESIZE for one claim.

    Parameters
    ----------
    claim : dict
        A Claim per GOAL.md: ``{id, statement, kind, artifact, params}``.
    counter : int, optional
        Pins the run_id counter for reproducibility / concurrency-safety.
    timestamp : str, optional
        ISO-8601 string to pin both timestamps (reproducible runs). If None,
        the current UTC time is used.
    project_dir : str, optional
        Lean project dir handed to ``formal_verify.verify``. Defaults to the
        claim's ``params["project_dir"]`` if present.
    write : bool
        Whether to write the RunRecord to ``engine/runs/<run_id>.json``.
    runs_dir : str, optional
        Override the output directory (used by tests). Defaults to engine/runs.

    Returns
    -------
    RunRecord (dict)
    """
    if not isinstance(claim, dict):
        raise TypeError("claim must be a dict per the GOAL.md contract")
    claim_id = claim.get("id") or "anonymous-claim"

    started = timestamp or _now_iso()
    run_id = make_run_id(claim_id, counter)

    # --- Lazily resolve the three sibling stage entrypoints. ---------------- #
    falsify_fn = _try_import_attr("engine.falsify.falsify", "falsify")
    certify_fn = _try_import_attr("engine.certify.certify", "certify")
    verify_fn = _try_import_attr("engine.formal_verify.formal_verify", "verify")

    # --- Stage 1: FALSIFY --------------------------------------------------- #
    falsify_art, falsify_status = _run_stage(
        "falsify.falsify",
        falsify_fn,
        lambda fn: fn(claim),
        lambda: _stub_falsify(claim),
    )
    verdict = falsify_art.get("verdict", "unknown")

    # --- Stage 2: CERTIFY --------------------------------------------------- #
    # Honest gating: if falsification REFUTED the claim, downstream certs are
    # moot. We still run the stages (so the record is complete) but the
    # synthesis flags the refutation.
    certify_art, certify_status = _run_stage(
        "certify.certify",
        certify_fn,
        lambda fn: fn(claim),
        lambda: _stub_certify(claim),
    )

    # --- Stage 3: VERIFY (Lean / Aristotle) --------------------------------- #
    lemma = claim.get("lemma") or claim.get("statement") or ""
    pdir = project_dir or (claim.get("params") or {}).get("project_dir")
    verify_art, verify_status = _run_stage(
        "formal_verify.verify",
        verify_fn,
        lambda fn: fn(lemma, pdir),
        lambda: _stub_verify(claim),
    )

    finished = timestamp or _now_iso()

    record: RunRecord = {
        "run_id": run_id,
        "schema": SCHEMA,
        "claim": claim,
        "falsify": falsify_art,
        "certify": certify_art,
        "verify": verify_art,
        "synthesis": "",  # filled below once the record is assembled
        "stage_status": {
            "falsify": falsify_status,
            "certify": certify_status,
            "verify": verify_status,
        },
        "verdict": verdict if verdict in ("survives", "refuted") else "unknown",
        "timestamps": {"started": started, "finished": finished},
    }

    # --- Stage 4: SYNTHESIZE ------------------------------------------------ #
    record["synthesis"] = synthesize(record)

    if write:
        out_dir = runs_dir or _RUNS_DIR
        _write_record(record, out_dir)

    return record


def _now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _write_record(record: RunRecord, out_dir: str) -> str:
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{record['run_id']}.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(record, fh, indent=2, sort_keys=False, default=str)
        fh.write("\n")
    return path


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def _main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="Aletheia pipeline orchestrator.")
    ap.add_argument("--claim", help="Path to a Claim JSON file.")
    ap.add_argument("--counter", type=int, default=None,
                    help="Pin the run_id counter (reproducible).")
    ap.add_argument("--timestamp", default=None,
                    help="Pin ISO-8601 timestamp (reproducible).")
    ap.add_argument("--smoke", action="store_true",
                    help="Run the built-in smoke-test claim and print the RunRecord.")
    args = ap.parse_args(argv)

    if args.smoke or not args.claim:
        claim = _SMOKE_CLAIM
    else:
        with open(args.claim, "r", encoding="utf-8") as fh:
            claim = json.load(fh)

    record = run(claim, counter=args.counter, timestamp=args.timestamp)
    print(json.dumps(record, indent=2, default=str))
    print("\n--- SYNTHESIS ---")
    print(record["synthesis"])
    return 0


# A trivial, self-contained claim for the smoke test / CLI default.
_SMOKE_CLAIM = {
    "id": "smoke-trivial-001",
    "statement": "2 + 2 = 4",
    "kind": "numerical",
    "artifact": None,
    "params": {},
}


if __name__ == "__main__":
    raise SystemExit(_main())
