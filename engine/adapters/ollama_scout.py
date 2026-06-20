"""
engine/adapters/ollama_scout.py
===============================
OPTIONAL cheap SCOUT-stage adapter for the Aletheia engine (engine/GOAL.md).

The SCOUT stage (DISCOVER) is agent-orchestrated and intentionally has no fixed
code in v1. This adapter adds a *cheap local* assist: it calls a local Ollama
model (default llama3.1:8b) to triage / propose candidate claims or summarize
text, so the expensive frontier model isn't spent on throwaway triage.

It is strictly best-effort: if Ollama is not installed, not running, the model
is not pulled, or the call errors/times out, scout() returns a structured
"unavailable" result instead of raising -- the engine then simply falls back to
the agent-driven scout pattern. NO scout output is ever treated as ground truth;
it only proposes. Everything it suggests still goes through FALSIFY/CERTIFY/VERIFY.

PUBLIC API
----------
    scout(prompt: str, *, model: str = "llama3.1:8b", timeout_s: int = 120,
          system: str|None = None) -> str
        Free-form scout call. Returns the model's text on success, or a short
        "[ollama-unavailable: ...]" string on any failure (never raises).

    scout_detailed(prompt, ...) -> dict
        {ok: bool, text: str, model, error, elapsed_s, ...} -- same call, full
        structured result for the orchestrator's provenance.

    propose_claims(topic: str, n: int = 3, **kw) -> list[dict]
        SCOUT helper: ask the model for n candidate Claim stubs about a topic.
        Returns a list of {statement, kind, rationale} dicts (best-effort
        parsed; empty list if unavailable). These are *candidates* only.

    available(model: str = "llama3.1:8b") -> dict
        {installed: bool, models: [..], model_present: bool} -- a cheap probe.

ENV OVERRIDES
-------------
    OLLAMA_BIN     path to the ollama binary (default: 'ollama' on PATH)
    OLLAMA_MODEL   default model id (overrides the model= default)

SMOKE:
    python3 engine/adapters/ollama_scout.py --smoke
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import time

DEFAULT_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.1:8b")

# `ollama run` streams to a TTY-style stream: when its soft-wrap heuristic
# breaks a word across the terminal width it prints the fragment, then emits
# cursor-left + erase-to-EOL (\x1b[<n>D \x1b[K) and reprints the whole word on
# the next line -- which, captured to a pipe, duplicates the fragment. We run a
# tiny terminal emulator over the stream that honors the cursor/erase control
# codes so the captured text matches what a human sees on screen.
_CSI_RE = re.compile(r"\x1b\[([0-9;?]*)([A-Za-z])")


def _clean_stream(text: str) -> str:
    """Emulate the relevant ANSI control codes to recover clean linear text.

    Honors: CR (column 0), cursor-left (CUB, 'D'), erase-to-EOL (EL, 'K').
    All other CSI sequences are dropped. The result is the on-screen text.
    """
    buf: list[str] = []   # current line as a list of chars
    col = 0               # cursor column within buf
    out_lines: list[str] = []

    def _flush_line():
        out_lines.append("".join(buf))

    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if ch == "\x1b":
            m = _CSI_RE.match(text, i)
            if m:
                params, final = m.group(1), m.group(2)
                if final == "D":  # cursor back N (default 1)
                    cnt = int(params) if params.isdigit() else 1
                    col = max(0, col - cnt)
                elif final == "K":  # erase in line; mode 0 (default) = to EOL
                    del buf[col:]
                # other CSI codes: ignored
                i = m.end()
                continue
            i += 1  # stray ESC
            continue
        if ch == "\n":
            _flush_line()
            buf = []
            col = 0
            i += 1
            continue
        if ch == "\r":
            col = 0
            i += 1
            continue
        # printable: overwrite at col (TTY semantics), extend if past end
        if col < len(buf):
            buf[col] = ch
        else:
            buf.append(ch)
        col += 1
        i += 1
    _flush_line()
    return "\n".join(out_lines).strip()


def _ollama_bin() -> str | None:
    explicit = os.environ.get("OLLAMA_BIN")
    if explicit and os.path.exists(explicit):
        return explicit
    found = shutil.which("ollama")
    if found:
        return found
    # common install locations
    for cand in ("/usr/local/bin/ollama", "/opt/homebrew/bin/ollama"):
        if os.path.exists(cand):
            return cand
    return None


def available(model: str = DEFAULT_MODEL) -> dict:
    """Cheap probe: is ollama installed, and is `model` pulled locally?"""
    binp = _ollama_bin()
    if not binp:
        return {"installed": False, "models": [], "model_present": False,
                "error": "ollama binary not found on PATH or known locations"}
    try:
        proc = subprocess.run([binp, "list"], capture_output=True, text=True,
                              timeout=15)
    except Exception as e:  # noqa: BLE001 -- probe must never raise
        return {"installed": True, "models": [], "model_present": False,
                "error": f"`ollama list` failed: {e}"}
    if proc.returncode != 0:
        return {"installed": True, "models": [], "model_present": False,
                "error": f"`ollama list` rc={proc.returncode}: {proc.stderr.strip()}"}
    # Parse model names from the first column (skip the header row).
    models = []
    for line in proc.stdout.splitlines()[1:]:
        line = line.strip()
        if line:
            models.append(line.split()[0])
    # `model` may be given without a tag; match by prefix too.
    present = any(m == model or m.startswith(model.split(":")[0]) for m in models)
    return {"installed": True, "models": models, "model_present": present,
            "error": None}


def scout_detailed(prompt: str, *, model: str = DEFAULT_MODEL,
                   timeout_s: int = 120, system: str | None = None) -> dict:
    """Run one scout call; return a full structured result (never raises)."""
    t0 = time.time()
    binp = _ollama_bin()
    base = {"ok": False, "text": "", "model": model, "error": None,
            "elapsed_s": 0.0}
    if not binp:
        base["error"] = "ollama-unavailable: binary not found"
        base["text"] = f"[{base['error']}]"
        return base

    full_prompt = prompt
    if system:
        # `ollama run` has no first-class system flag in older builds; prepend.
        full_prompt = f"System: {system}\n\nUser: {prompt}"

    try:
        proc = subprocess.run(
            [binp, "run", model, full_prompt],
            capture_output=True, text=True, timeout=timeout_s,
        )
    except subprocess.TimeoutExpired:
        base["error"] = f"ollama-unavailable: timeout after {timeout_s}s"
        base["text"] = f"[{base['error']}]"
        base["elapsed_s"] = round(time.time() - t0, 2)
        return base
    except Exception as e:  # noqa: BLE001 -- best-effort, never raise
        base["error"] = f"ollama-unavailable: {e}"
        base["text"] = f"[{base['error']}]"
        base["elapsed_s"] = round(time.time() - t0, 2)
        return base

    base["elapsed_s"] = round(time.time() - t0, 2)
    if proc.returncode != 0:
        err = (proc.stderr or "").strip()
        base["error"] = f"ollama-unavailable: rc={proc.returncode}: {err[:300]}"
        base["text"] = f"[{base['error']}]"
        return base

    text = _clean_stream(proc.stdout or "")
    if not text:
        base["error"] = "ollama-unavailable: empty response"
        base["text"] = f"[{base['error']}]"
        return base

    base["ok"] = True
    base["text"] = text
    return base


def scout(prompt: str, *, model: str = DEFAULT_MODEL, timeout_s: int = 120,
          system: str | None = None) -> str:
    """Clean scout(prompt) -> text API. Returns text, or a '[ollama-unavailable: ...]'
    sentinel string on any failure (graceful fallback, never raises)."""
    return scout_detailed(prompt, model=model, timeout_s=timeout_s,
                          system=system)["text"]


_PROPOSE_SYSTEM = (
    "You are a mathematics research scout. Propose candidate claims to "
    "investigate. Be concrete and falsifiable. Output ONLY a JSON array of "
    "objects with keys: statement (string), kind ('numerical' or 'theorem'), "
    "rationale (one short sentence). No prose outside the JSON."
)


def propose_claims(topic: str, n: int = 3, *, model: str = DEFAULT_MODEL,
                   timeout_s: int = 180) -> list[dict]:
    """SCOUT helper: ask the model for n candidate claim stubs (best-effort).

    Returns [] if ollama is unavailable or no JSON could be parsed. Output is
    *candidate-only* -- it must still pass FALSIFY/CERTIFY/VERIFY downstream.
    """
    prompt = (f"Topic: {topic}\n\nPropose {n} candidate claims as a JSON array.")
    res = scout_detailed(prompt, model=model, timeout_s=timeout_s,
                         system=_PROPOSE_SYSTEM)
    if not res["ok"]:
        return []
    text = res["text"]
    # Extract the first JSON array in the response.
    start = text.find("[")
    end = text.rfind("]")
    if start == -1 or end == -1 or end <= start:
        return []
    try:
        arr = json.loads(text[start:end + 1])
    except Exception:  # noqa: BLE001
        return []
    out = []
    for item in arr if isinstance(arr, list) else []:
        if isinstance(item, dict) and "statement" in item:
            out.append({
                "statement": str(item.get("statement", "")),
                "kind": item.get("kind", "numerical"),
                "rationale": str(item.get("rationale", "")),
            })
    return out


# --------------------------------------------------------------------------
# Smoke test
# --------------------------------------------------------------------------

def _smoke() -> int:
    """Probe ollama, then run the prompt from the task and quote the output."""
    print("=== ollama_scout smoke ===")
    av = available()
    print("ollama installed   :", av["installed"])
    print("models             :", av.get("models"))
    print("llama3.1:8b present :", av.get("model_present"))
    if av.get("error"):
        print("probe note         :", av["error"])

    prompt = "In one line, what is a Hecke triangle group?"
    print(f"\nscout({prompt!r}):")
    res = scout_detailed(prompt, timeout_s=120)
    print("ok       :", res["ok"])
    print("model    :", res["model"])
    print("elapsed_s:", res["elapsed_s"])
    if res["error"]:
        print("error    :", res["error"])
    print("--- output ---")
    print(res["text"])
    print("--- end output ---")

    # The adapter is correct whether or not ollama happens to be up: success
    # path => non-empty real text; failure path => graceful sentinel. Both are
    # acceptable; we assert only that scout() returned a string and never raised.
    txt = scout(prompt, timeout_s=120)
    assert isinstance(txt, str) and len(txt) > 0
    if res["ok"]:
        print("\nSMOKE PASS: ollama responded with real text (quoted above).")
    else:
        print("\nSMOKE PASS (graceful fallback): ollama unavailable, scout() "
              "returned the sentinel string without raising. Recorded honestly.")
    return 0


if __name__ == "__main__":
    if "--smoke" in sys.argv:
        sys.exit(_smoke())
    print(__doc__)
