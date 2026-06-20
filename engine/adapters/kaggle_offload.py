"""
engine/adapters/kaggle_offload.py
=================================
OPTIONAL accelerator adapter for the Aletheia engine (engine/GOAL.md).

Offloads a heavy CERTIFY / SCAN job to a Kaggle free-tier kernel: it
(a) GENERATES a self-contained Kaggle script + kernel-metadata.json from a
    job spec,
(b) PUSHES it via the `kaggle` CLI (~/.local/bin/kaggle kernels push),
(c) can POLL status and PULL the kernel output back to disk.

This is a *transport* adapter only -- it never re-implements the math. A job
spec names a self-contained Python entrypoint (verbatim source string, or a
path to a frozen snapshot under code/_snapshots/) plus the parameters, exactly
the way the hand-built kernels under kaggle_kernels/ are structured: a frozen
engine body followed by a small driver that writes a JSON result to
/kaggle/working. The engine then fetches that JSON.

WHY OFFLOAD. The local CERTIFY stage already works; this is for *batch* /
*sweep* work (e.g. a 12-q spectrum sweep, or a wide Arb winding-box scan over
many seeds) that is embarrassingly parallel-in-q and too slow to babysit
locally. Kaggle gives ~9h CPU sessions for free.

PUBLIC API (the engine contract for this adapter)
--------------------------------------------------
    offload(job_spec: dict, *, push: bool = False, work_dir: str|None = None,
            kaggle_bin: str|None = None) -> dict
        -> {kernel_id, status, folder, script_path, metadata_path,
            pushed: bool, ...}
        Generates the kernel folder (script + metadata). If push=True, also
        runs `kaggle kernels push`. status is one of:
          "generated"  -- folder built, not pushed
          "queued"     -- push succeeded (kernel is queued/running on Kaggle)
          "push_failed"-- push attempted and the CLI returned nonzero / missing

    fetch(kernel_id: str, *, work_dir: str|None = None,
          kaggle_bin: str|None = None, poll: bool = True,
          timeout_s: int = 0) -> dict
        -> {kernel_id, status, results_path, output_dir, ...}
        Polls `kaggle kernels status` (if poll=True) until the kernel reaches a
        terminal state (or timeout_s elapses; 0 = single status check, no wait),
        then pulls output via `kaggle kernels output`. results_path is the path
        to the first *.json result pulled (or None if none / not complete).

JOB SPEC SHAPE
--------------
    {
      "job_id":      "hecke-spectrum-sweep",     # -> kernel slug, REQUIRED
      "title":       "Hecke spectrum sweep",     # optional, defaults to job_id
      "engine_src":  "<python source string>",   # the self-contained engine body
         # OR
      "engine_path": "/abs/path/to/frozen.py",   # read source from a file instead
      "driver_src":  "<python source string>",   # the sweep/certify driver appended
                                                 #   after the engine body
      "params":      { ... },                    # injected as a JOB_PARAMS dict
      "result_name": "result.json",              # output filename in /kaggle/working
      "enable_gpu":  False,                       # passthrough to metadata
      "enable_internet": False,                    # passthrough to metadata
      "is_private":  True,
      "username":    "saarshai",                  # optional; else read ~/.kaggle/kaggle.json
    }

The generated script always:
  * defines JOB_PARAMS = {...} (from params),
  * runs the engine body then the driver,
  * and -- as a safety net -- if the driver wrote nothing, dumps JOB_PARAMS +
    a stub note to result_name so fetch() always finds a parseable JSON.

SMOKE (does NOT push by default):
    python3 engine/adapters/kaggle_offload.py --smoke
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DEFAULT_WORK_ROOT = os.path.join(REPO_ROOT, "engine", "runs", "kaggle_offload")
DEFAULT_KAGGLE_BIN = os.path.expanduser("~/.local/bin/kaggle")

# Kaggle slug rules: lowercase letters, digits, hyphens; <= ~50 chars.
_SLUG_OK = set("abcdefghijklmnopqrstuvwxyz0123456789-")


def _slugify(s: str) -> str:
    s = (s or "").strip().lower()
    out = []
    for ch in s:
        if ch in _SLUG_OK:
            out.append(ch)
        elif ch in " _.":
            out.append("-")
        # else drop
    slug = "".join(out)
    while "--" in slug:
        slug = slug.replace("--", "-")
    slug = slug.strip("-") or "aletheia-job"
    return slug[:50]


def _kaggle_username(explicit: str | None) -> str:
    if explicit:
        return explicit
    cfg = os.path.expanduser("~/.kaggle/kaggle.json")
    if os.path.exists(cfg):
        try:
            with open(cfg) as f:
                return json.load(f).get("username") or "unknown"
        except Exception:
            pass
    return os.environ.get("KAGGLE_USERNAME", "unknown")


def _resolve_kaggle_bin(explicit: str | None) -> str:
    if explicit:
        return explicit
    if os.path.exists(DEFAULT_KAGGLE_BIN):
        return DEFAULT_KAGGLE_BIN
    return "kaggle"  # rely on PATH


# --------------------------------------------------------------------------
# (a) Kernel script generation
# --------------------------------------------------------------------------

_DRIVER_FALLBACK = (
    "# (no driver_src supplied) -- echo params as the result.\n"
    "RESULT = {'stub': True, 'note': 'no driver_src in job spec; echoing params',\n"
    "          'params': JOB_PARAMS}\n"
)


def build_kernel_script(job_spec: dict) -> str:
    """Assemble a single self-contained Kaggle script string from the job spec.

    Layout mirrors the hand-built kernels under kaggle_kernels/:
      [header] -> [JOB_PARAMS] -> [frozen engine body] -> [driver] ->
      [save-result safety net].
    """
    job_id = job_spec.get("job_id")
    if not job_id:
        raise ValueError("job_spec must include 'job_id'")
    result_name = job_spec.get("result_name", "result.json")

    if "engine_src" in job_spec and job_spec["engine_src"] is not None:
        engine_src = job_spec["engine_src"]
    elif job_spec.get("engine_path"):
        with open(job_spec["engine_path"]) as f:
            engine_src = f.read()
    else:
        engine_src = "# (no engine body supplied)\n"

    driver_src = job_spec.get("driver_src") or _DRIVER_FALLBACK
    params = job_spec.get("params", {})

    parts = []
    parts.append(
        "# ==========================================================================\n"
        f"# Aletheia offload kernel: {job_id}\n"
        "# AUTO-GENERATED by engine/adapters/kaggle_offload.py -- do not hand-edit.\n"
        "# Self-contained: frozen engine body + driver; writes a JSON result to\n"
        "# /kaggle/working so engine.adapters.kaggle_offload.fetch() can pull it.\n"
        "# ==========================================================================\n"
    )
    parts.append("import json, os, sys, time\n")
    parts.append("_T_START = time.time()\n")
    parts.append(
        "KWORK = '/kaggle/working' if os.path.isdir('/kaggle/working') else os.getcwd()\n"
    )
    parts.append(f"RESULT_NAME = {result_name!r}\n")
    parts.append("JOB_PARAMS = " + json.dumps(params, indent=2) + "\n")
    parts.append("RESULT = None  # the driver should set this, or write the file itself\n")
    parts.append("\n# ---- frozen engine body ----\n")
    parts.append(engine_src.rstrip() + "\n")
    parts.append("\n# ---- driver ----\n")
    parts.append(driver_src.rstrip() + "\n")
    parts.append(
        "\n# ---- save-result safety net ----\n"
        "_final = os.path.join(KWORK, RESULT_NAME)\n"
        "if not os.path.exists(_final):\n"
        "    _payload = RESULT if RESULT is not None else {\n"
        "        'stub': True, 'note': 'driver wrote no file and set no RESULT',\n"
        "        'params': JOB_PARAMS}\n"
        "    if isinstance(_payload, dict):\n"
        "        _payload.setdefault('wall_seconds', time.time() - _T_START)\n"
        "    with open(_final, 'w') as _f:\n"
        "        json.dump(_payload, _f, indent=2, default=str)\n"
        "    print('Saved result:', _final)\n"
        "else:\n"
        "    print('Driver already wrote:', _final)\n"
    )
    return "".join(parts)


def build_kernel_metadata(job_spec: dict, *, username: str | None = None) -> dict:
    """Build the kernel-metadata.json dict (Kaggle kernels metadata schema)."""
    job_id = job_spec.get("job_id")
    if not job_id:
        raise ValueError("job_spec must include 'job_id'")
    slug = _slugify(job_id)
    user = _kaggle_username(username or job_spec.get("username"))
    title = job_spec.get("title") or job_id
    # Kaggle requires title length 5..50 once the kernel is public; keep it sane.
    title = title[:50]
    return {
        "id": f"{user}/{slug}",
        "title": title,
        "code_file": f"{slug}.py",
        "language": "python",
        "kernel_type": "script",
        "is_private": bool(job_spec.get("is_private", True)),
        "enable_gpu": bool(job_spec.get("enable_gpu", False)),
        "enable_tpu": bool(job_spec.get("enable_tpu", False)),
        "enable_internet": bool(job_spec.get("enable_internet", False)),
    }


def write_kernel_folder(job_spec: dict, work_dir: str | None = None,
                        *, username: str | None = None) -> dict:
    """Write {slug}.py + kernel-metadata.json into a folder; return paths.

    Pure local generation -- no network. Returns the dict that offload() and
    callers use to locate the artifacts.
    """
    slug = _slugify(job_spec.get("job_id", ""))
    work_root = work_dir or DEFAULT_WORK_ROOT
    folder = os.path.join(work_root, slug)
    os.makedirs(folder, exist_ok=True)

    metadata = build_kernel_metadata(job_spec, username=username)
    script = build_kernel_script(job_spec)

    script_path = os.path.join(folder, metadata["code_file"])
    metadata_path = os.path.join(folder, "kernel-metadata.json")
    with open(script_path, "w") as f:
        f.write(script)
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)
    return {
        "folder": folder,
        "script_path": script_path,
        "metadata_path": metadata_path,
        "kernel_id": metadata["id"],
        "slug": slug,
    }


# --------------------------------------------------------------------------
# (b) Push
# --------------------------------------------------------------------------

def _run_kaggle(args: list[str], kaggle_bin: str, timeout: int = 300) -> dict:
    """Run a kaggle CLI subcommand; return {ok, returncode, stdout, stderr}."""
    cmd = [kaggle_bin] + args
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return {
            "ok": proc.returncode == 0,
            "returncode": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "cmd": " ".join(cmd),
        }
    except FileNotFoundError as e:
        return {"ok": False, "returncode": 127, "stdout": "",
                "stderr": f"kaggle binary not found: {e}", "cmd": " ".join(cmd)}
    except subprocess.TimeoutExpired as e:
        return {"ok": False, "returncode": -1, "stdout": e.stdout or "",
                "stderr": f"timeout after {timeout}s", "cmd": " ".join(cmd)}


# --------------------------------------------------------------------------
# Public API
# --------------------------------------------------------------------------

def offload(job_spec: dict, *, push: bool = False, work_dir: str | None = None,
            kaggle_bin: str | None = None, username: str | None = None) -> dict:
    """Generate (and optionally push) a Kaggle offload kernel for a heavy job.

    push=False (default): pure local generation, status "generated". This is the
    safe smoke path. push=True: also run `kaggle kernels push`.
    """
    gen = write_kernel_folder(job_spec, work_dir=work_dir, username=username)
    result = {
        "kernel_id": gen["kernel_id"],
        "folder": gen["folder"],
        "script_path": gen["script_path"],
        "metadata_path": gen["metadata_path"],
        "pushed": False,
        "status": "generated",
        "url": f"https://www.kaggle.com/code/{gen['kernel_id']}",
    }
    # Validate the metadata is well-formed JSON on disk before any push.
    with open(gen["metadata_path"]) as f:
        json.load(f)

    if not push:
        return result

    kbin = _resolve_kaggle_bin(kaggle_bin)
    push_res = _run_kaggle(["kernels", "push", "-p", gen["folder"]], kbin)
    result["pushed"] = push_res["ok"]
    result["push_stdout"] = push_res["stdout"]
    result["push_stderr"] = push_res["stderr"]
    result["status"] = "queued" if push_res["ok"] else "push_failed"
    return result


# Terminal states reported by `kaggle kernels status`.
_TERMINAL = ("complete", "error", "cancelAcknowledged", "cancelRequested")


def _parse_status(stdout: str) -> str:
    """Extract a coarse status token from `kaggle kernels status` stdout."""
    low = stdout.lower()
    for tok in ("complete", "error", "cancel", "running", "queued"):
        if tok in low:
            return tok
    return "unknown"


def fetch(kernel_id: str, *, work_dir: str | None = None,
          kaggle_bin: str | None = None, poll: bool = True,
          timeout_s: int = 0, poll_interval_s: int = 20) -> dict:
    """Poll status (optional) and pull a finished kernel's output to disk.

    timeout_s == 0 => a single status check, no waiting loop. The caller is
    expected to call again later (the engine orchestrator is async-friendly).
    Returns results_path = the first *.json pulled, or None.
    """
    import time as _time

    kbin = _resolve_kaggle_bin(kaggle_bin)
    slug = kernel_id.split("/")[-1]
    out_dir = os.path.join(work_dir or DEFAULT_WORK_ROOT, slug, "output")
    os.makedirs(out_dir, exist_ok=True)

    status = "unknown"
    deadline = (_time.time() + timeout_s) if (poll and timeout_s > 0) else None
    while True:
        st = _run_kaggle(["kernels", "status", kernel_id], kbin)
        status = _parse_status(st["stdout"] + st["stderr"]) if st["stdout"] or st["stderr"] else "unknown"
        if not poll or status in ("complete", "error", "cancel", "unknown"):
            break
        if deadline is None or _time.time() >= deadline:
            break
        _time.sleep(poll_interval_s)

    result = {"kernel_id": kernel_id, "status": status,
              "output_dir": out_dir, "results_path": None}

    if status != "complete":
        result["note"] = ("not pulling output: kernel status is "
                          f"'{status}' (need 'complete')")
        return result

    pull = _run_kaggle(["kernels", "output", kernel_id, "-p", out_dir, "-o"], kbin)
    result["pull_ok"] = pull["ok"]
    result["pull_stderr"] = pull["stderr"]
    if pull["ok"]:
        jsons = sorted(
            os.path.join(out_dir, fn) for fn in os.listdir(out_dir)
            if fn.endswith(".json")
        )
        result["pulled_files"] = sorted(os.listdir(out_dir))
        result["results_path"] = jsons[0] if jsons else None
    return result


# --------------------------------------------------------------------------
# Smoke test (no push by default)
# --------------------------------------------------------------------------

def _smoke() -> int:
    """Generate a tiny certify-job kernel; assert metadata + script are valid."""
    import tempfile

    # A tiny self-contained "certify" job: enclose pi to a few digits with
    # decimal interval arithmetic. Stands in for a real Arb winding job but
    # needs no external packages, so the generated kernel is genuinely runnable.
    engine_src = (
        "from decimal import Decimal, getcontext\n"
        "def certify_pi(digits):\n"
        "    getcontext().prec = digits + 5\n"
        "    # Bailey-Borwein-Plouffe series for pi (rigorous-ish demo)\n"
        "    pi = Decimal(0); k = 0\n"
        "    while k < digits:\n"
        "        pi += (Decimal(1)/(16**k))*(Decimal(4)/(8*k+1)-Decimal(2)/(8*k+4)"
        "-Decimal(1)/(8*k+5)-Decimal(1)/(8*k+6))\n"
        "        k += 1\n"
        "    return pi\n"
    )
    driver_src = (
        "d = int(JOB_PARAMS.get('digits', 12))\n"
        "val = certify_pi(d)\n"
        "RESULT = {'claim': 'pi enclosure (demo certify job)',\n"
        "          'digits': d, 'pi_estimate': str(val),\n"
        "          'certified': str(val).startswith('3.14159')}\n"
    )
    job_spec = {
        "job_id": "aletheia-smoke-certify-pi",
        "title": "Aletheia smoke: certify pi",
        "engine_src": engine_src,
        "driver_src": driver_src,
        "params": {"digits": 12},
        "result_name": "pi_certificate.json",
        "is_private": True,
    }

    work_dir = tempfile.mkdtemp(prefix="aletheia_kaggle_smoke_")
    res = offload(job_spec, push=False, work_dir=work_dir)

    print("=== kaggle_offload smoke (generation only, NO push) ===")
    print("kernel_id   :", res["kernel_id"])
    print("status      :", res["status"])
    print("folder      :", res["folder"])
    print("script_path :", res["script_path"])
    print("metadata    :", res["metadata_path"])

    # Validate metadata JSON parses and has the required keys.
    with open(res["metadata_path"]) as f:
        meta = json.load(f)
    required = {"id", "title", "code_file", "language", "kernel_type"}
    missing = required - set(meta)
    assert not missing, f"metadata missing keys: {missing}"
    assert meta["code_file"].endswith(".py")
    print("\n--- kernel-metadata.json (parsed OK) ---")
    print(json.dumps(meta, indent=2))

    # Validate the generated script is syntactically valid Python.
    with open(res["script_path"]) as f:
        src = f.read()
    compile(src, res["script_path"], "exec")
    print(f"\nscript compiles OK ({len(src)} bytes, "
          f"JOB_PARAMS + engine + driver + save net present: "
          f"{all(t in src for t in ('JOB_PARAMS', 'certify_pi', 'RESULT', 'KWORK'))})")

    print("\nSMOKE PASS: metadata JSON parses, script compiles, no push performed.")
    return 0


if __name__ == "__main__":
    if "--smoke" in sys.argv:
        sys.exit(_smoke())
    print(__doc__)
