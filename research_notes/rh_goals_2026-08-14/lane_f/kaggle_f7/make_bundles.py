#!/usr/bin/env python3
# Provenance: recovered 2026-08-17 from this session's pre-compaction scratchpad
# (/private/tmp/claude-501/-Users-za-Documents-farey-hecke/.../scratchpad/make_bundles.py).
# Originally written to generate the F7 kaggle_f7/ bundles (F7_STAGE3_LAUNCH.md
# §6 noted the generator "lives in the session scratchpad, not the repo" and
# "was not committed anywhere" — this commit closes that gap). Validated
# 2026-08-17 by regenerating chunk-00 and diffing byte-for-byte against the
# committed kaggle_f7/f7-r3b-chunk-00/f7_r3b_chunk_00.py: wrapper, FILES_B64
# key set, path rewrites and kernel-metadata.json all matched exactly; the
# only diff was the zeta_cert_rosen.py blob, which is exactly the known
# additive det(1-K) repair applied post-run (see F7_R3B_ASSEMBLY_CERT.md
# provenance note) — not a generator defect.
"""Generate 16 self-contained Kaggle bundles for the F7 R3b closed-cover launch.

Each bundle embeds every file f7_certify_r3b_flagship.py needs at its
hardcoded absolute paths, recreates that exact directory scaffold under
/kaggle/working/_scaffold, and invokes the unmodified certify script with
--arcs <chunk range>.
"""
import base64
import json
import textwrap
import zlib
from pathlib import Path

REPO = Path("/Users/za/Documents/farey-hecke")
LANE_F = REPO / "research_notes/rh_goals_2026-08-14/lane_f"
LANE_G = REPO / "research_notes/rh_goals_2026-08-14/lane_g"
WORKTREE = REPO / ".worktrees/aletheia-restore"
OUT_ROOT = LANE_F / "kaggle_f7"

# (scaffold absolute path, local source path)
FILES = [
    (WORKTREE / "code/tc_rerun/certify_r3_flagship.py", WORKTREE / "code/tc_rerun/certify_r3_flagship.py"),
    (WORKTREE / "code/tc_rerun/tc_rerun.py", WORKTREE / "code/tc_rerun/tc_rerun.py"),
    (WORKTREE / "code/tc_rerun/r3b_engine.py", WORKTREE / "code/tc_rerun/r3b_engine.py"),
    (WORKTREE / "code/tb_certify/certify_tb_blocks.py", WORKTREE / "code/tb_certify/certify_tb_blocks.py"),
    (WORKTREE / "code/tb_certify/certify_tb_blocks_v2.py", WORKTREE / "code/tb_certify/certify_tb_blocks_v2.py"),
    (WORKTREE / "code/zeta_cert_rosen.py", WORKTREE / "code/zeta_cert_rosen.py"),
    (WORKTREE / "code/zeta_cert_rosen_q5.py", WORKTREE / "code/zeta_cert_rosen_q5.py"),
    (LANE_F / "f7_certify_r3b_flagship.py", LANE_F / "f7_certify_r3b_flagship.py"),
    (LANE_F / "f7_certify_r2_flagship.py", LANE_F / "f7_certify_r2_flagship.py"),
    (LANE_F / "f7_certify_tb_blocks.py", LANE_F / "f7_certify_tb_blocks.py"),
    (LANE_F / "f7_r3b_engine.py", LANE_F / "f7_r3b_engine.py"),
    (LANE_F / "f7_source_builder.py", LANE_F / "f7_source_builder.py"),
    (LANE_F / "f7_r3b_endpoint.py", LANE_F / "f7_r3b_endpoint.py"),
    (LANE_F / "F7_PILOT2_REPORT.md", LANE_F / "F7_PILOT2_REPORT.md"),
    (LANE_F / "F7_TB_R2_RECEIPTS.md", LANE_F / "F7_TB_R2_RECEIPTS.md"),
    (LANE_F / "f7_receipts/F7_R2_FLAGSHIP_ENVELOPE_RECEIPT.json", LANE_F / "f7_receipts/F7_R2_FLAGSHIP_ENVELOPE_RECEIPT.json"),
    (LANE_F / "f7_receipts/F7_TB_BLOCK_CERTIFICATES_RECEIPT.json", LANE_F / "f7_receipts/F7_TB_BLOCK_CERTIFICATES_RECEIPT.json"),
    (LANE_F / "f7_receipts/F7_W_ENVELOPE_CERT_RECEIPT.json", LANE_F / "f7_receipts/F7_W_ENVELOPE_CERT_RECEIPT.json"),
    (LANE_G / "tb_disc_opt.json", LANE_G / "tb_disc_opt.json"),
    (WORKTREE / "code/out/resonance_geometry.json", WORKTREE / "code/out/resonance_geometry.json"),
]

CHUNKS = [(i, i * 12, i * 12 + 12) for i in range(16)]

RUNNER_TEMPLATE = '''# ==========================================================================
# f7-r3b-chunk-{idx:02d}  --  Kaggle CERTIFY kernel, q=7 R3b closed-cover
# base-arc range {lo}:{hi} (of 192), N_PRIMARY=256 / N_COMPARISON=224.
# Self-contained: recreates the exact absolute-path scaffold
# f7_certify_r3b_flagship.py expects, then runs it unmodified.
# ==========================================================================
import base64, os, subprocess, sys, json, time, zlib

try:
    import flint  # noqa
except Exception:
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "python-flint"], check=True)

# values are zlib-compressed then base64-encoded (Kaggle script size cap is 1MB)
FILES_B64 = {{
{file_entries}
}}

for rel_path, b64 in FILES_B64.items():
    dest = os.path.join("/", rel_path)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "wb") as f:
        f.write(zlib.decompress(base64.b64decode(b64)))

LANE_F = "/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_f"
OUT = "/kaggle/working"
os.makedirs(OUT, exist_ok=True)

cmd = [
    sys.executable, os.path.join(LANE_F, "f7_certify_r3b_flagship.py"),
    "--arcs", "{lo}:{hi}",
    "--workers", "4",
    "--receipt", os.path.join(OUT, "F7_R3B_CHUNK_{idx:02d}_RECEIPT.json"),
    "--checkpoint", os.path.join(OUT, "F7_R3B_CHUNK_{idx:02d}_CHECKPOINT.json"),
    "--report", os.path.join(OUT, "F7_R3B_CHUNK_{idx:02d}_CERT.md"),
]
print("RUNNING:", " ".join(cmd), flush=True)
t0 = time.time()
result = subprocess.run(cmd, cwd=LANE_F)
print("EXIT CODE:", result.returncode, "  wall_seconds:", time.time() - t0, flush=True)
sys.exit(result.returncode)
'''

def b64_of(path: Path) -> str:
    return base64.b64encode(zlib.compress(path.read_bytes(), 9)).decode("ascii")

def rel_scaffold(path: Path) -> str:
    # strip leading "/" so it can be joined back with os.path.join("/", rel)
    return str(path).lstrip("/")

OUT_ROOT.mkdir(parents=True, exist_ok=True)

manifest = []
for idx, lo, hi in CHUNKS:
    bundle_dir = OUT_ROOT / f"f7-r3b-chunk-{idx:02d}"
    bundle_dir.mkdir(parents=True, exist_ok=True)
    entries = []
    for scaffold_path, src_path in FILES:
        rel = rel_scaffold(scaffold_path)
        entries.append(f'    "{rel}": "{b64_of(src_path)}",')
    runner_src = RUNNER_TEMPLATE.format(
        idx=idx, lo=lo, hi=hi, file_entries="\n".join(entries)
    )
    runner_path = bundle_dir / f"f7_r3b_chunk_{idx:02d}.py"
    runner_path.write_text(runner_src)
    meta = {
        "id": f"saarshai/f7-r3b-chunk-{idx:02d}",
        "title": f"f7-r3b-chunk-{idx:02d}",
        "code_file": f"f7_r3b_chunk_{idx:02d}.py",
        "language": "python",
        "kernel_type": "script",
        "is_private": True,
        "enable_gpu": False,
        "enable_tpu": False,
        "enable_internet": True,
    }
    (bundle_dir / "kernel-metadata.json").write_text(json.dumps(meta, indent=2))
    manifest.append({"idx": idx, "arcs": f"{lo}:{hi}", "dir": str(bundle_dir), "ref": meta["id"]})
    print(f"chunk {idx:02d}  arcs {lo}:{hi}  -> {bundle_dir}  ({runner_path.stat().st_size} bytes)")

print("DONE.")
