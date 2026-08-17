#!/usr/bin/env python3
# Provenance: adapted from lane_f/kaggle_f7/make_bundles.py (recovered
# 2026-08-17 from this session's pre-compaction scratchpad, validated
# byte-identical modulo the known det(1-K) provenance drift -- see that
# file's own header comment). f8's dependency graph is much smaller than
# f7's (3 engine files vs f7's ~20-file bundle), because f8's box needs
# N~30-34 rather than N~224-256, so no analytic R2 block-envelope layer or
# multi-chunk arc splitting was needed (see f8_certify_r3b_flagship.py's
# own module docstring for the architecture-deviation rationale).
"""Generate a single self-contained Kaggle bundle for the F8 R3b closed-box
certificate (chunk-00 == the WHOLE certificate, since it fits one session)."""
import base64
import json
import zlib
from pathlib import Path

REPO = Path("/Users/za/Documents/farey-hecke")
LANE_F = REPO / "research_notes/rh_goals_2026-08-14/lane_f"
WORKTREE = REPO / ".worktrees/aletheia-restore"
OUT_ROOT = LANE_F / "kaggle_f8"

FILES = [
    (WORKTREE / "code/zeta_cert_rosen_even.py", WORKTREE / "code/zeta_cert_rosen_even.py"),
    (WORKTREE / "code/zeta_cert_rosen.py", WORKTREE / "code/zeta_cert_rosen.py"),
    (WORKTREE / "code/zeta_cert_rosen_q5.py", WORKTREE / "code/zeta_cert_rosen_q5.py"),
    (LANE_F / "f8_certify_r3b_flagship.py", LANE_F / "f8_certify_r3b_flagship.py"),
]

RUNNER_TEMPLATE = '''# ==========================================================================
# f8-r3b-chunk-00  --  Kaggle CERTIFY kernel, q=8 R3b closed-box winding
# N_PRIMARY=32 (N_COMPARISON=30 cross-check also run). chunk-00 IS the whole
# box (4 edges, 16 arcs) -- fits one session, no further chunks needed.
# Self-contained: recreates the exact absolute-path scaffold
# f8_certify_r3b_flagship.py expects, then runs it unmodified.
# ==========================================================================
import base64, os, subprocess, sys, json, time, zlib

try:
    import flint  # noqa
except Exception:
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "python-flint"], check=True)

FILES_B64 = {
{file_entries}
}

for rel_path, b64 in FILES_B64.items():
    dest = os.path.join("/", rel_path)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "wb") as f:
        f.write(zlib.decompress(base64.b64decode(b64)))

LANE_F = "/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_f"
OUT = "/kaggle/working"
os.makedirs(OUT, exist_ok=True)

for N in (32, 30):
    cmd = [
        sys.executable, os.path.join(LANE_F, "f8_certify_r3b_flagship.py"),
        "--N", str(N),
        "--receipt", os.path.join(OUT, f"F8_R3B_CHUNK_00_N{N}_RECEIPT.json"),
        "--report", os.path.join(OUT, f"F8_R3B_CHUNK_00_N{N}_CERT.md"),
    ]
    print("RUNNING:", " ".join(cmd), flush=True)
    t0 = time.time()
    result = subprocess.run(cmd, cwd=LANE_F)
    print("EXIT CODE:", result.returncode, "  wall_seconds:", time.time() - t0, flush=True)
    if result.returncode != 0:
        sys.exit(result.returncode)
sys.exit(0)
'''


def b64_of(path: Path) -> str:
    return base64.b64encode(zlib.compress(path.read_bytes(), 9)).decode("ascii")


def rel_scaffold(path: Path) -> str:
    return str(path).lstrip("/")


OUT_ROOT.mkdir(parents=True, exist_ok=True)
bundle_dir = OUT_ROOT / "f8-r3b-chunk-00"
bundle_dir.mkdir(parents=True, exist_ok=True)

entries = []
for scaffold_path, src_path in FILES:
    rel = rel_scaffold(scaffold_path)
    entries.append(f'    "{rel}": "{b64_of(src_path)}",')
runner_src = RUNNER_TEMPLATE.replace("{file_entries}", "\n".join(entries))
runner_path = bundle_dir / "f8_r3b_chunk_00.py"
runner_path.write_text(runner_src)

meta = {
    "id": "saarshai/f8-r3b-chunk-00",
    "title": "f8-r3b-chunk-00",
    "code_file": "f8_r3b_chunk_00.py",
    "language": "python",
    "kernel_type": "script",
    "is_private": True,
    "enable_gpu": False,
    "enable_tpu": False,
    "enable_internet": True,
}
(bundle_dir / "kernel-metadata.json").write_text(json.dumps(meta, indent=2))
print(f"chunk 00 -> {bundle_dir} ({runner_path.stat().st_size} bytes)")
print("DONE.")
