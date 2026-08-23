#!/usr/bin/env python3
"""Build the private Kaggle dataset + kernel bundle for the S2 second-pin
N=288 contour campaign (192 base arcs, 16 chunks of 12).

Mirrors kaggle_q8_subdivision/build_bundle.py: files are stored FLAT (Kaggle's
uploader flattens nested directories); ``manifest.json`` records each file's
flat name, its path inside the reconstructed tree, its sha256 and role.  The
kernel re-verifies every sha256 before reconstructing the tree; the
orchestrator then re-verifies the R2/TB receipt sha pins itself
(``R2_EXPECTED_SHA256`` / ``TB_V2_EXPECTED_SHA256``).

The tree layout MUST reproduce the repo-relative geometry the second_pin code
derives its paths from:
  <root>/.worktrees/aletheia-restore/code/second_pin/  (CODE_DIR)
  <root>/.worktrees/aletheia-restore/code/{tc_rerun,tb_certify,zeta_cert_rosen_q5.py}
  <root>/research_notes/rh_goals_2026-08-14/lane_g/...  (LANE_DIR)

Read-only packaging; nothing in lane_g or the worktree is modified.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent           # lane_g/kaggle_s2_contour
LANE_G = HERE.parent
RH_ROOT = LANE_G.parents[2]                      # farey-hecke repo root
WT = RH_ROOT / ".worktrees" / "aletheia-restore"
SP = WT / "code" / "second_pin"
LANE_REL = "research_notes/rh_goals_2026-08-14/lane_g"

PYTHON_FLINT_PIN = "0.9.0"

# (source path, path relative to the reconstructed tree root, role)
PAYLOAD = [
    # --- code (sys.modules closure of certify_r3b_flagship, this session) ---
    (SP / "certify_r3b_flagship.py",
     ".worktrees/aletheia-restore/code/second_pin/certify_r3b_flagship.py",
     "S2 contour orchestrator (second_pin copy; N_PRIMARY=288, B3 seam merge, "
     "--skip-comparison, in-memory T_tail extension)"),
    (SP / "certify_r3_flagship.py",
     ".worktrees/aletheia-restore/code/second_pin/certify_r3_flagship.py",
     "S2 R3 helper copy (closed_boundary_segments, load_and_validate_r2, "
     "winding primitives; S2 pin + S2 W binding)"),
    (SP / "certify_r2_flagship.py",
     ".worktrees/aletheia-restore/code/second_pin/certify_r2_flagship.py",
     "S2 R2 certifier copy (tail formulas single_block_tail/tail_block_tail "
     "used by the in-memory T_tail(288) extension)"),
    (SP / "r3b_endpoint.py",
     ".worktrees/aletheia-restore/code/second_pin/r3b_endpoint.py",
     "S2 endpoint certificate (enlarged contours; Kimi 1-C3 guard; S2 box)"),
    (WT / "code" / "tc_rerun" / "tc_rerun.py",
     ".worktrees/aletheia-restore/code/tc_rerun/tc_rerun.py",
     "source builder wrapper (loads the tracked q5 engine by path)"),
    (WT / "code" / "tc_rerun" / "r3b_engine.py",
     ".worktrees/aletheia-restore/code/tc_rerun/r3b_engine.py",
     "R3b block/derivative engine (hash-pinned by the orchestrator)"),
    (WT / "code" / "tb_certify" / "certify_tb_blocks.py",
     ".worktrees/aletheia-restore/code/tb_certify/certify_tb_blocks.py",
     "TB arc helper (imported by r3b_endpoint; R2 arc_helper binding)"),
    (WT / "code" / "zeta_cert_rosen_q5.py",
     ".worktrees/aletheia-restore/code/zeta_cert_rosen_q5.py",
     "certified q=5 Arb engine, UNMODIFIED (R2 engine binding)"),
    # --- immutable data inputs (verify_immutable_inputs + load_and_validate_r2) ---
    (LANE_G / "second_pin" / "R2_SECONDPIN_ENVELOPE_RECEIPT.json",
     f"{LANE_REL}/second_pin/R2_SECONDPIN_ENVELOPE_RECEIPT.json",
     "S2 R2 receipt (sha-pinned as R2_EXPECTED_SHA256)"),
    (LANE_G / "TB_BLOCK_CERTIFICATES_V2_RECEIPT.json",
     f"{LANE_REL}/TB_BLOCK_CERTIFICATES_V2_RECEIPT.json",
     "TB V2 receipt (sha-pinned as TB_V2_EXPECTED_SHA256)"),
    (LANE_G / "second_pin" / "W_ENVELOPE_CERT_S2_RECEIPT.json",
     f"{LANE_REL}/second_pin/W_ENVELOPE_CERT_S2_RECEIPT.json",
     "S2 W envelope receipt (R2 W_V2_head_data_only binding)"),
    (LANE_G / "second_pin" / "R2R3_SECONDPIN_CERT.md",
     f"{LANE_REL}/second_pin/R2R3_SECONDPIN_CERT.md",
     "attempt-1 report (mandatory immutable input)"),
    (LANE_G / "TB_R1_HILBERT_RESTATEMENT.md",
     f"{LANE_REL}/TB_R1_HILBERT_RESTATEMENT.md",
     "R1 restatement (mandatory immutable input)"),
    (LANE_G / "ADVERSARIAL_REVIEW_V3_TBCHAIN.md",
     f"{LANE_REL}/ADVERSARIAL_REVIEW_V3_TBCHAIN.md",
     "adversarial review (R2 binding input)"),
    (LANE_G / "TB_LEMMA_CHAIN.md",
     f"{LANE_REL}/TB_LEMMA_CHAIN.md",
     "TB lemma chain (load_and_validate_r2 required input)"),
    (LANE_G / "tb_disc_opt.json",
     f"{LANE_REL}/tb_disc_opt.json",
     "disc optimization constants (loaded at tc_rerun import time)"),
    (WT / "code" / "out" / "resonance_geometry.json",
     ".worktrees/aletheia-restore/code/out/resonance_geometry.json",
     "G_5 geometry receipt (loaded at tc_rerun import time; G5_PINS)"),
    # --- campaign provenance ---
    (HERE / "merge_s2_chunks.py", "driver/merge_s2_chunks.py",
     "merge-time driver (carried for provenance; runs locally, not in-kernel)"),
]

KERNEL_TEMPLATE = '''# ==========================================================================
# {kernel_slug}
# S2 second-pin G_5 winding box, N=288 contour campaign.
# chunk {chunk}: base arcs [{arc_start}, {arc_end}) of 192, N={N}, workers={workers}.
#
# The second_pin orchestrator runs with --arcs (chunk mode, no winding claim)
# and --skip-comparison (the N=128 control arm runs once at assembly, not in
# every chunk).  Every dataset file is sha256-verified against manifest.json
# before the tree is reconstructed; the orchestrator then re-verifies its own
# R2/TB sha pins.  A mismatch aborts.
# ==========================================================================
import glob
import hashlib
import json
import os
import shutil
import signal
import subprocess
import sys
import time

TREE = "/kaggle/working/tree"
OUT = "/kaggle/working"

INPUT_ROOT = "/kaggle/input"
print("mounted inputs:", sorted(os.listdir(INPUT_ROOT)), flush=True)
candidates = sorted(
    glob.glob(os.path.join(INPUT_ROOT, "**", "manifest.json"), recursive=True)
)
if len(candidates) != 1:
    raise SystemExit("expected exactly one mounted manifest.json, found %r" % candidates)
DATASET = os.path.dirname(candidates[0])
print("dataset mount:", DATASET, flush=True)

try:
    import flint  # noqa: F401
except Exception:
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-q", "python-flint=={flint_pin}"],
        check=True,
    )
import flint  # noqa: E402
print("python-flint", flint.__version__, flush=True)

manifest = json.load(open(os.path.join(DATASET, "manifest.json")))
print("manifest", manifest["schema"], manifest["created"], flush=True)
for entry in manifest["files"]:
    source = os.path.join(DATASET, entry["dataset_name"])
    digest = hashlib.sha256(open(source, "rb").read()).hexdigest()
    if digest != entry["sha256"]:
        raise SystemExit(
            "DATASET FILE HASH MISMATCH %s: %s != %s"
            % (entry["dataset_name"], digest, entry["sha256"])
        )
    destination = os.path.join(TREE, entry["tree_path"])
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    shutil.copyfile(source, destination)
print("verified and staged", len(manifest["files"]), "files", flush=True)

receipt = os.path.join(OUT, "{receipt_name}")
cmd = [
    sys.executable,
    os.path.join(TREE, ".worktrees/aletheia-restore/code/second_pin/certify_r3b_flagship.py"),
    "--arcs", "{arc_start}:{arc_end}",
    "--workers", "{workers}",
    "--skip-comparison",
    "--receipt", receipt,
    "--checkpoint", receipt.replace(".json", ".ckpt.json"),
    "--report", receipt.replace(".json", ".md"),
]
print("RUNNING:", " ".join(cmd), flush=True)
print("cpu_count", os.cpu_count(), flush=True)
t0 = time.time()
# Soft deadline well under Kaggle's 12 h batch cap: on expiry SIGTERM the
# orchestrator (it checkpoints and exits cleanly) and keep the partial output.
DEADLINE = {deadline}
proc = subprocess.Popen(cmd)
rc = None
while True:
    rc = proc.poll()
    if rc is not None:
        break
    if time.time() - t0 > DEADLINE:
        print("DEADLINE: sending SIGTERM to the orchestrator", flush=True)
        proc.send_signal(signal.SIGTERM)
        try:
            rc = proc.wait(timeout=600)
        except subprocess.TimeoutExpired:
            proc.kill()
            rc = proc.wait()
        break
    time.sleep(10)
print("EXIT CODE:", rc, " wall_seconds:", time.time() - t0, flush=True)
# The receipt/checkpoint are the artifacts; do not fail the kernel and lose
# them on a deadline SIGTERM (exit 143) — only on hard errors.
sys.exit(0 if rc in (0, 143) else rc)
'''


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def flat_name(tree_path: str) -> str:
    return tree_path.replace("/", "__")


def build_dataset(out_root: Path, username: str, dataset_slug: str, created: str) -> Path:
    dataset_dir = out_root / "dataset"
    dataset_dir.mkdir(parents=True, exist_ok=True)
    files = []
    for source, tree_path, role in PAYLOAD:
        if not source.exists():
            raise SystemExit(f"missing payload file: {source}")
        name = flat_name(tree_path)
        (dataset_dir / name).write_bytes(source.read_bytes())
        files.append(
            {
                "dataset_name": name,
                "tree_path": tree_path,
                "sha256": sha256(source),
                "bytes": source.stat().st_size,
                "role": role,
                "repo_path": str(source.relative_to(RH_ROOT)),
            }
        )
    manifest = {
        "schema": "farey-hecke.s2-contour-n288-campaign/1",
        "created": created,
        "lane": "lane_g S2 second winding box (owner-approved ~58 CPU-h escalation)",
        "purpose": (
            "closed-contour certification of the second G_5 pin box "
            "0.41054373549473627 + 7.81976824701551188 i (half-width 1e-6) at "
            "N=288: 192 base arcs in 16 chunks of 12; N*=288 frozen from "
            "F288_PROBE.json (F_R(288)=2.09e-8 certified) with N*=274 the "
            "measured floor (S2_NSCALING_RECEIPT.md); winding is claimed only "
            "at merge time (merge_s2_chunks.py), never by a chunk"
        ),
        "python": ">=3.11",
        "dependencies": {"python-flint": PYTHON_FLINT_PIN},
        "geometry": {
            "K_per_edge": 48,
            "base_arcs": 192,
            "chunks": 16,
            "arcs_per_chunk": 12,
            "N_primary": 288,
        },
        "status_contract": (
            "Chunk receipts are CHUNK output (status CHUNK_ARCS_CLEAR at "
            "best), not a theorem.  The winding claim requires the local "
            "merge + overlap-polygon closure, then the assembly doc; the "
            "NO_VERTICAL_LINE corollary upgrade stays referee-gated."
        ),
        "files": files,
    }
    (dataset_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    (dataset_dir / "dataset-metadata.json").write_text(
        json.dumps(
            {
                "title": "s2 contour n288 inputs",
                "id": f"{username}/{dataset_slug}",
                "licenses": [{"name": "other"}],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return dataset_dir


def build_kernels(
    out_root: Path,
    username: str,
    dataset_slug: str,
    chunks: int,
    arcs_per_chunk: int,
    N: int,
    workers: int,
    deadline: int,
    prefix: str,
) -> list[dict[str, object]]:
    made = []
    for chunk in range(chunks):
        arc_start = chunk * arcs_per_chunk
        arc_end = arc_start + arcs_per_chunk
        kernel_slug = f"{prefix}-s{chunk:02d}"
        kernel_dir = out_root / "kernels" / kernel_slug
        kernel_dir.mkdir(parents=True, exist_ok=True)
        receipt_name = f"S2_CHUNK_a{arc_start:03d}-{arc_end:03d}.json"
        script = KERNEL_TEMPLATE.format(
            kernel_slug=kernel_slug,
            flint_pin=PYTHON_FLINT_PIN,
            chunk=chunk,
            arc_start=arc_start,
            arc_end=arc_end,
            N=N,
            workers=workers,
            deadline=deadline,
            receipt_name=receipt_name,
        )
        code_file = f"{kernel_slug.replace('-', '_')}.py"
        (kernel_dir / code_file).write_text(script, encoding="utf-8")
        (kernel_dir / "kernel-metadata.json").write_text(
            json.dumps(
                {
                    "id": f"{username}/{kernel_slug}",
                    "title": kernel_slug,
                    "code_file": code_file,
                    "language": "python",
                    "kernel_type": "script",
                    "is_private": True,
                    "enable_gpu": False,
                    "enable_tpu": False,
                    "enable_internet": True,
                    "dataset_sources": [f"{username}/{dataset_slug}"],
                    "competition_sources": [],
                    "kernel_sources": [],
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        made.append(
            {
                "kernel_id": f"{username}/{kernel_slug}",
                "dir": str(kernel_dir),
                "chunk": chunk,
                "arc_start": arc_start,
                "arc_end": arc_end,
                "receipt": receipt_name,
            }
        )
    return made


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-root", type=Path, default=HERE / "bundle")
    parser.add_argument("--username", default="saarshai")
    parser.add_argument("--dataset-slug", default="s2-contour-n288-inputs")
    parser.add_argument("--prefix", default="s2-contour-n288")
    parser.add_argument("--chunks", type=int, default=16)
    parser.add_argument("--arcs-per-chunk", type=int, default=12)
    parser.add_argument("--N", type=int, default=288)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--deadline", type=int, default=39600)
    parser.add_argument("--created", default="2026-08-23")
    args = parser.parse_args()

    if args.chunks * args.arcs_per_chunk != 192:
        raise SystemExit("chunks * arcs_per_chunk must tile the 192-arc cover")
    args.out_root.mkdir(parents=True, exist_ok=True)
    dataset_dir = build_dataset(
        args.out_root, args.username, args.dataset_slug, args.created
    )
    kernels = build_kernels(
        args.out_root, args.username, args.dataset_slug, args.chunks,
        args.arcs_per_chunk, args.N, args.workers, args.deadline, args.prefix,
    )
    summary = {
        "dataset_dir": str(dataset_dir),
        "dataset_id": f"{args.username}/{args.dataset_slug}",
        "chunk_count": len(kernels),
        "base_arcs": 192,
        "arcs_per_chunk": args.arcs_per_chunk,
        "N_primary": args.N,
        "kernels": kernels,
    }
    (args.out_root / "PLAN.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
