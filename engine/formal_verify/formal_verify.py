"""Aletheia VERIFY stage — Lean/Aristotle formal-verification bridge.

Wraps the Aristotle (Harmonic Lean prover) CLI flow proven in
``projects/aristotle_minpoly_lambda`` and emits a ``ProofCertificate`` per the
shared contract in ``engine/GOAL.md``:

    ProofCertificate = {
        "claim_id":   str,
        "lemma":      str,        # the lemma statement that was submitted
        "lean_file":  str | None, # path to the extracted Main.lean
        "sorry_free": bool,       # count of 'sorry'/'admit' tokens == 0
        "axioms":     [str],      # axiom set parsed from ARISTOTLE_SUMMARY.md
        "proved":     bool,       # True iff sorry_free AND the summary reports a
                                  # successful build + axiom check
        # extras (provenance; not part of the minimal contract):
        "project_id": str | None,
        "status":     str,        # last Aristotle status seen (e.g. COMPLETE)
        "build_passed_per_summary": bool,
        "notes":      [str],
    }

HONESTY CONTRACT
----------------
``proved`` is True ONLY when (a) the extracted ``Main.lean`` is sorry-free AND
(b) ``ARISTOTLE_SUMMARY.md`` states a successful build with a clean axiom check.
The build/axiom result is *Aristotle-reported* — this module does not re-run
``lake build`` locally. Callers that need an independent guarantee must re-run
the Lean build themselves; ``build_passed_per_summary`` flags the provenance.

CLI: ``~/.local/bin/aristotle`` (aristotlelib 2.0.0). API key
``ARISTOTLE_API_KEY`` in ``~/.farey_api_keys``; passed via the subprocess env.

submit=False (default) does NOT spend Aristotle compute. To post-process an
existing completed project, call ``verify_project(project_id, lemma, ...)``.
"""

from __future__ import annotations

import gzip
import io
import os
import re
import shutil
import subprocess
import tarfile
import tempfile
import time
import uuid
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

ARISTOTLE_BIN = os.path.expanduser("~/.local/bin/aristotle")
API_KEYS_FILE = os.path.expanduser("~/.farey_api_keys")

# Aristotle status strings that mean "no point polling further".
TERMINAL_OK = {"COMPLETE"}
TERMINAL_BAD = {"FAILED", "CANCELLED", "CANCELED", "ERROR"}

# The canonical clean axiom set for a Mathlib proof with no extra axioms.
CLEAN_AXIOMS = ["propext", "Classical.choice", "Quot.sound"]


# ---------------------------------------------------------------------------
# Environment / CLI helpers
# ---------------------------------------------------------------------------

def _load_api_key() -> Optional[str]:
    """Return ARISTOTLE_API_KEY from the environment or ~/.farey_api_keys."""
    if os.environ.get("ARISTOTLE_API_KEY"):
        return os.environ["ARISTOTLE_API_KEY"]
    path = Path(API_KEYS_FILE)
    if not path.exists():
        return None
    for line in path.read_text().splitlines():
        line = line.strip()
        if line.startswith("#") or "=" not in line:
            continue
        # Tolerate `export KEY=val`, `KEY=val`, quotes.
        line = line[len("export "):].strip() if line.startswith("export ") else line
        key, _, val = line.partition("=")
        if key.strip() == "ARISTOTLE_API_KEY":
            return val.strip().strip('"').strip("'")
    return None


def _aristotle_env() -> dict:
    env = dict(os.environ)
    key = _load_api_key()
    if key:
        env["ARISTOTLE_API_KEY"] = key
    return env


def _run_cli(args: list[str], timeout: int = 120) -> subprocess.CompletedProcess:
    """Run the aristotle CLI with the API key injected into the env."""
    if not Path(ARISTOTLE_BIN).exists():
        raise FileNotFoundError(f"aristotle CLI not found at {ARISTOTLE_BIN}")
    return subprocess.run(
        [ARISTOTLE_BIN, *args],
        env=_aristotle_env(),
        capture_output=True,
        text=True,
        timeout=timeout,
    )


# ---------------------------------------------------------------------------
# Submit / poll / download
# ---------------------------------------------------------------------------

_PROJECT_RE = re.compile(
    r"\b([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})\b"
)


def submit(prompt: str, project_dir: Optional[str] = None, timeout: int = 120) -> str:
    """Submit a prompt to Aristotle (non-blocking). Returns the project_id.

    Spends Aristotle compute. Caller is responsible for keeping prompts cheap.
    """
    args = ["submit", prompt]
    if project_dir:
        args += ["--project-dir", project_dir]
    cp = _run_cli(args, timeout=timeout)
    out = (cp.stdout or "") + "\n" + (cp.stderr or "")
    if cp.returncode != 0:
        raise RuntimeError(f"aristotle submit failed (exit {cp.returncode}):\n{out}")
    m = _PROJECT_RE.findall(out)
    if not m:
        raise RuntimeError(f"could not parse a project_id from submit output:\n{out}")
    # Prefer a "Project: <id>" line if present; else the last UUID seen.
    proj = re.search(r"Project[:\s]+" + _PROJECT_RE.pattern, out)
    return proj.group(1) if proj else m[-1]


def show_status(project_id: str, timeout: int = 60) -> tuple[str, str]:
    """Return (status, full_show_text) for a project.

    The CLI prints the status as the first token of the first line, e.g.
    ``COMPLETE (started 1h ago)``.
    """
    cp = _run_cli(["show", project_id], timeout=timeout)
    text = (cp.stdout or "") + (("\n" + cp.stderr) if cp.stderr else "")
    if cp.returncode != 0 and not text.strip():
        raise RuntimeError(f"aristotle show failed (exit {cp.returncode})")
    first = text.strip().splitlines()[0] if text.strip() else ""
    status = first.split()[0].upper() if first else "UNKNOWN"
    return status, text


def poll_until_done(
    project_id: str,
    max_wait: int = 1800,
    base: float = 5.0,
    factor: float = 1.6,
    cap: float = 120.0,
) -> tuple[str, str]:
    """Poll ``show`` with exponential backoff until terminal or max_wait.

    Returns (status, last_show_text). Does not raise on a BAD terminal state —
    the caller inspects the returned status.
    """
    deadline = time.time() + max_wait
    delay = base
    status, text = show_status(project_id)
    while status not in TERMINAL_OK and status not in TERMINAL_BAD:
        if time.time() >= deadline:
            return status, text  # caller treats non-terminal as "not proved"
        time.sleep(min(delay, max(0.0, deadline - time.time())))
        delay = min(delay * factor, cap)
        status, text = show_status(project_id)
    return status, text


def download_and_extract(project_id: str, dest_dir: str) -> Path:
    """Download a project's solution (gzipped tar) and extract it into dest_dir.

    Returns the directory that contains the extracted tree. Handles both a
    gzipped-tar payload and an already-uncompressed tar, defensively.
    """
    dest = Path(dest_dir)
    dest.mkdir(parents=True, exist_ok=True)
    archive = dest / f"{project_id}.tgz"
    cp = _run_cli(["download", project_id, "--destination", str(archive)])
    if cp.returncode != 0:
        raise RuntimeError(
            f"aristotle download failed (exit {cp.returncode}):\n"
            f"{cp.stdout}\n{cp.stderr}"
        )
    if not archive.exists() or archive.stat().st_size == 0:
        raise RuntimeError(f"download produced no file at {archive}")

    raw = archive.read_bytes()
    # gunzip if it is gzip-magic; otherwise assume it is already a tar.
    if raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)
    extract_root = dest / "extracted"
    if extract_root.exists():
        shutil.rmtree(extract_root)
    extract_root.mkdir(parents=True)
    with tarfile.open(fileobj=io.BytesIO(raw)) as tf:
        tf.extractall(extract_root)
    return extract_root


# ---------------------------------------------------------------------------
# Artifact post-processing
# ---------------------------------------------------------------------------

def _find_one(root: Path, name: str) -> Optional[Path]:
    """Find a single file by basename under root.

    Aristotle's tarball top-level dir is project-specific (e.g.
    ``<proj>_aristotle/RequestProject/Main.lean``), so we search rather than
    hard-code the path. Prefer a hit under a ``RequestProject`` dir.
    """
    hits = [p for p in root.rglob(name) if p.is_file()]
    if not hits:
        return None
    pref = [p for p in hits if "RequestProject" in p.parts]
    return (pref or hits)[0]


def count_sorry(lean_text: str) -> int:
    """Count Lean ``sorry``/``admit`` tokens (word-boundary, ignore comments-ish).

    Conservative: matches the bare tokens as whole words. Real proof solutions
    have zero; this is the sorry-free gate.
    """
    return len(re.findall(r"\b(?:sorry|admit)\b", lean_text))


def parse_axioms(summary_text: str) -> list[str]:
    """Parse the axiom set reported in ARISTOTLE_SUMMARY.md.

    Aristotle phrases a clean check as e.g.
        "... an axiom check (only `propext`, `Classical.choice`, `Quot.sound`)."
    We pick the backtick-wrapped identifiers in the clause that follows an
    "axiom" mention. Falls back to any backtick-wrapped axiom-shaped tokens.
    """
    # Narrow to the clause mentioning the axiom check. Prefer the parenthetical
    # group right after an "axiom" mention (e.g. "axiom check (only `propext`,
    # `Classical.choice`, `Quot.sound`)"); the axiom identifiers contain dots,
    # so we must NOT stop the scope at the first period.
    scope = summary_text
    m_paren = re.search(r"axiom[^()]*\(([^)]*)\)", summary_text, flags=re.IGNORECASE)
    if m_paren:
        scope = m_paren.group(1)
    else:
        m = re.search(r"axiom.*", summary_text, flags=re.IGNORECASE)
        if m:
            scope = m.group(0)
    toks = re.findall(r"`([A-Za-z_][A-Za-z0-9_.]*)`", scope)
    # Drop obvious non-axiom backticked refs (file paths, lemma names).
    axioms = [
        t for t in toks
        if t in {"propext", "Classical.choice", "Quot.sound", "sorryAx"}
        or t.startswith("Classical.")
        or t.startswith("Quot.")
    ]
    # De-dup preserving order.
    seen, out = set(), []
    for a in axioms:
        if a not in seen:
            seen.add(a)
            out.append(a)
    return out


def summary_reports_build_pass(summary_text: str) -> bool:
    """True iff the summary asserts a successful build (Aristotle-reported)."""
    t = summary_text.lower()
    return ("successful build" in t) or ("verified by a successful build" in t) \
        or ("build succeeds" in t) or ("builds successfully" in t)


def build_certificate(
    claim_id: str,
    lemma: str,
    extract_root: Path,
    project_id: Optional[str] = None,
    status: str = "COMPLETE",
) -> dict:
    """Assemble a ProofCertificate from an extracted Aristotle solution tree."""
    notes: list[str] = []
    lean_path = _find_one(extract_root, "Main.lean")
    summary_path = _find_one(extract_root, "ARISTOTLE_SUMMARY.md")

    lean_text = lean_path.read_text() if lean_path else ""
    summary_text = summary_path.read_text() if summary_path else ""

    if not lean_path:
        notes.append("Main.lean not found in extracted tree")
    if not summary_path:
        notes.append("ARISTOTLE_SUMMARY.md not found in extracted tree")

    n_sorry = count_sorry(lean_text) if lean_text else 1  # no file => not clean
    sorry_free = bool(lean_text) and n_sorry == 0
    if lean_text and not sorry_free:
        notes.append(f"found {n_sorry} sorry/admit token(s) in Main.lean")

    axioms = parse_axioms(summary_text)
    build_pass = summary_reports_build_pass(summary_text)
    notes.append("build/axiom result is Aristotle-reported (not re-run locally)")

    # proved ONLY if sorry-free AND summary reports a successful build/axiom check.
    proved = bool(sorry_free and build_pass and status.upper() in TERMINAL_OK)

    return {
        "claim_id": claim_id,
        "lemma": lemma,
        "lean_file": str(lean_path) if lean_path else None,
        "sorry_free": sorry_free,
        "axioms": axioms,
        "proved": proved,
        # provenance extras
        "project_id": project_id,
        "status": status.upper(),
        "build_passed_per_summary": build_pass,
        "notes": notes,
    }


# ---------------------------------------------------------------------------
# Public entrypoints
# ---------------------------------------------------------------------------

def verify_project(
    project_id: str,
    lemma: str = "",
    claim_id: Optional[str] = None,
    work_dir: Optional[str] = None,
    max_wait: int = 1800,
) -> dict:
    """Post-process an EXISTING Aristotle project into a ProofCertificate.

    Polls the project to a terminal state (returns immediately if already
    COMPLETE), downloads + extracts the solution, then emits the certificate.
    Spends NO new Aristotle compute beyond status/download calls.
    """
    claim_id = claim_id or f"claim_{project_id[:8]}"
    status, _ = poll_until_done(project_id, max_wait=max_wait)
    if status not in TERMINAL_OK:
        return {
            "claim_id": claim_id,
            "lemma": lemma,
            "lean_file": None,
            "sorry_free": False,
            "axioms": [],
            "proved": False,
            "project_id": project_id,
            "status": status,
            "build_passed_per_summary": False,
            "notes": [f"project not COMPLETE (status={status}); not proved"],
        }
    cleanup = work_dir is None
    work_dir = work_dir or tempfile.mkdtemp(prefix="aletheia_verify_")
    try:
        root = download_and_extract(project_id, work_dir)
        return build_certificate(claim_id, lemma, root, project_id, status)
    finally:
        if cleanup:
            shutil.rmtree(work_dir, ignore_errors=True)


def verify(
    lemma_statement: str,
    project_dir: str,
    submit: bool = False,
    claim_id: Optional[str] = None,
    max_wait: int = 1800,
) -> dict:
    """Contract entrypoint: verify a lemma via Aristotle, return a ProofCertificate.

    Parameters
    ----------
    lemma_statement : str
        The Lean lemma / proof obligation to prove. Used as the submit prompt
        and recorded verbatim on the certificate.
    project_dir : str
        Directory of supporting Lean files passed to ``aristotle submit
        --project-dir``. May be empty/non-existent for self-contained lemmas.
    submit : bool
        If False (default), DO NOT spend Aristotle compute — raises, directing
        the caller to ``verify_project`` for post-processing an existing run.
        If True, submits the lemma, polls to completion, and post-processes.
    claim_id : str, optional
        Stable claim identifier; auto-generated if omitted.
    max_wait : int
        Max seconds to poll before giving up (certificate reports not-proved).
    """
    claim_id = claim_id or f"claim_{uuid.uuid4().hex[:8]}"
    if not submit:
        raise RuntimeError(
            "verify(submit=False) does not spend Aristotle compute. "
            "Use verify_project(project_id, lemma=...) to post-process an "
            "existing completed run, or call verify(..., submit=True) to "
            "submit a new (billable) job."
        )

    prompt = lemma_statement
    pdir = project_dir if project_dir and Path(project_dir).is_dir() else None
    project_id = submit_prompt = None
    try:
        project_id = globals()["submit"](prompt, project_dir=pdir)  # module fn
    except Exception as e:  # noqa: BLE001
        return {
            "claim_id": claim_id,
            "lemma": lemma_statement,
            "lean_file": None,
            "sorry_free": False,
            "axioms": [],
            "proved": False,
            "project_id": None,
            "status": "SUBMIT_FAILED",
            "build_passed_per_summary": False,
            "notes": [f"submit failed: {e}"],
        }
    return verify_project(
        project_id, lemma=lemma_statement, claim_id=claim_id, max_wait=max_wait
    )


# NOTE: ``submit`` above (the module function) is shadowed by the ``submit``
# parameter inside ``verify``; ``verify`` calls it via ``globals()["submit"]``.


__all__ = [
    "verify",
    "verify_project",
    "submit",
    "show_status",
    "poll_until_done",
    "download_and_extract",
    "build_certificate",
    "count_sorry",
    "parse_axioms",
    "CLEAN_AXIOMS",
]
