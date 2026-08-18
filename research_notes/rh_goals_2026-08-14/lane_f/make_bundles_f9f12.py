#!/usr/bin/env python3
# Provenance: adapted from lane_f/make_bundles_f8.py (itself adapted from
# lane_f/kaggle_f7/make_bundles.py). Only two things change: the driver
# embedded is the q-parameterized f9f12_certify_r3b_flagship.py, and the
# runner passes --q. The dependency graph is the same 3 engine files, since
# f9f12_certify_r3b_flagship.py imports BOTH parity engines (odd q=9,11 use
# zeta_cert_rosen, even q=10,12 use zeta_cert_rosen_even; both pull
# zeta_cert_rosen_q5).
"""Generate one self-contained Kaggle canary bundle per q in 9..12 for the
F9-F12 R3b closed-box certificates (one chunk == the whole box per q)."""
import argparse
import base64
import json
import zlib
from pathlib import Path

REPO = Path("/Users/za/Documents/farey-hecke")
LANE_F = REPO / "research_notes/rh_goals_2026-08-14/lane_f"
WORKTREE = REPO / ".worktrees/aletheia-restore"
OUT_ROOT = LANE_F / "kaggle_f9f12"

FILES = [
    WORKTREE / "code/zeta_cert_rosen_even.py",
    WORKTREE / "code/zeta_cert_rosen.py",
    WORKTREE / "code/zeta_cert_rosen_q5.py",
    LANE_F / "f9f12_certify_r3b_flagship.py",
]

RUNNER_TEMPLATE = '''# ==========================================================================
# f{q}-r3b-chunk-00  --  Kaggle CERTIFY kernel, q={q} R3b closed-box winding
# N_PRIMARY={n1} (N_COMPARISON={n2} cross-check also run). chunk-00 IS the
# whole box (4 edges, 16 arcs) -- fits one session.
# Self-contained: recreates the exact absolute-path scaffold
# f9f12_certify_r3b_flagship.py expects, then runs it unmodified.
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

for N in ({n1}, {n2}):
    cmd = [
        sys.executable, os.path.join(LANE_F, "f9f12_certify_r3b_flagship.py"),
        "--q", "{q}", "--N", str(N),
        "--receipt", os.path.join(OUT, f"F{q}_R3B_CHUNK_00_N{N}_RECEIPT.json"),
        "--report", os.path.join(OUT, f"F{q}_R3B_CHUNK_00_N{N}_CERT.md"),
    ]
    print("RUNNING:", " ".join(cmd), flush=True)
    t0 = time.time()
    result = subprocess.run(cmd, cwd=LANE_F)
    print("EXIT CODE:", result.returncode, "  wall_seconds:", time.time() - t0, flush=True)
    if result.returncode != 0:
        sys.exit(result.returncode)
sys.exit(0)
'''

# N_PRIMARY, N_COMPARISON per q, frozen by the local --boundary-sup-check
# sweep (see F9_F12_BASE_EXTENSION.md).
N_PAIRS = {9: (32, 28), 10: (36, 32), 11: (32, 28), 12: (36, 32)}


def b64_of(path: Path) -> str:
    return base64.b64encode(zlib.compress(path.read_bytes(), 9)).decode("ascii")


def build(q: int) -> Path:
    n1, n2 = N_PAIRS[q]
    entries = [f'    "{str(p).lstrip("/")}": "{b64_of(p)}",' for p in FILES]
    runner_src = (RUNNER_TEMPLATE
                  .replace("{file_entries}", "\n".join(entries))
                  .replace("{q}", str(q))
                  .replace("{n1}", str(n1))
                  .replace("{n2}", str(n2)))
    bundle_dir = OUT_ROOT / f"f{q}-r3b-chunk-00"
    bundle_dir.mkdir(parents=True, exist_ok=True)
    runner_path = bundle_dir / f"f{q}_r3b_chunk_00.py"
    runner_path.write_text(runner_src)
    (bundle_dir / "kernel-metadata.json").write_text(json.dumps({
        "id": f"saarshai/f{q}-r3b-chunk-00",
        "title": f"f{q}-r3b-chunk-00",
        "code_file": f"f{q}_r3b_chunk_00.py",
        "language": "python",
        "kernel_type": "script",
        "is_private": True,
        "enable_gpu": False,
        "enable_tpu": False,
        "enable_internet": True,
    }, indent=2))
    print(f"q={q} -> {bundle_dir} ({runner_path.stat().st_size} bytes)")
    return bundle_dir


def verify(q: int) -> bool:
    """Decompress every embedded blob and diff against the live source."""
    src = (OUT_ROOT / f"f{q}-r3b-chunk-00" / f"f{q}_r3b_chunk_00.py").read_text()
    ns: dict = {}
    start = src.index("FILES_B64 = {")
    end = src.index("\n}\n", start) + 3
    exec(src[start:end], ns)  # noqa: S102 -- local, self-generated literal dict
    ok = True
    for rel, b64 in ns["FILES_B64"].items():
        live = Path("/" + rel).read_bytes()
        if zlib.decompress(base64.b64decode(b64)) != live:
            print(f"  MISMATCH: {rel}")
            ok = False
    print(f"q={q} embed integrity: {'all blobs byte-identical' if ok else 'FAILED'}")
    return ok


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", default=[9, 10, 11, 12])
    args = ap.parse_args()
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    for q in args.q:
        build(q)
        verify(q)
    print("DONE.")
