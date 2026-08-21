#!/usr/bin/env python3
"""Build the private Kaggle dataset + kernel bundle for the q=8 depth-7 campaign.

The dataset carries the UNMODIFIED lane_f engine and the hash-pinned receipts it
reads.  Files are stored FLAT (Kaggle's uploader does not preserve nested
directories without archiving); ``manifest.json`` records, for every file, its
flat dataset name, its relative path inside the lane tree, its sha256 and its
role.  The kernel re-verifies every sha256 before reconstructing the tree, so a
corrupted or substituted dataset file aborts the run rather than producing a
receipt.

Nothing here touches lane_f.  Read-only packaging.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RH = HERE.parents[1]
LANE_F = RH / "lane_f"
LANE_G = RH / "lane_g"

PYTHON_FLINT_PIN = "0.9.0"

# (source path, path relative to the reconstructed tree root, role)
PAYLOAD = [
    (LANE_F / "q8_schur_contour.py", "lane_f/q8_schur_contour.py",
     "lane_f checker, UNMODIFIED (commit 3f8dd58 lineage, v4-operator-norm-gate)"),
    (LANE_F / "q8_contour_helpers.py", "lane_f/q8_contour_helpers.py",
     "contour geometry + certified winding (hash-pinned by the checker)"),
    (LANE_F / "q8_r3b_engine.py", "lane_f/q8_r3b_engine.py",
     "q8 R3b block/derivative engine (hash-pinned by the checker)"),
    (LANE_F / "f8_source_builder.py", "lane_f/f8_source_builder.py",
     "F1024 source geometry builder (hash-pinned by the checker)"),
    (LANE_F / "f8_certify_tb_blocks.py", "lane_f/f8_certify_tb_blocks.py",
     "TB block certifier (hash-pinned by the checker)"),
    (LANE_F / "q8_tb_support.py", "lane_f/q8_tb_support.py",
     "TB support primitives (imported by f8_certify_tb_blocks)"),
    (LANE_G / "law_probes" / "kaggle_boundary_rate" / "zeta_cert_rosen_q5.py",
     "lane_g/law_probes/kaggle_boundary_rate/zeta_cert_rosen_q5.py",
     "vendored q-agnostic Arb/Hurwitz primitives (f8_source_builder TRACKED_ENGINE_DIR)"),
    (LANE_G / "law_probes" / "kaggle_boundary_rate" / "zeta_cert_rosen_even.py",
     "lane_g/law_probes/kaggle_boundary_rate/zeta_cert_rosen_even.py",
     "vendored trusted generic even-q engine (cross-check import)"),
    (LANE_G / "law_probes" / "kaggle_boundary_rate" / "zeta_cert_rosen.py",
     "lane_g/law_probes/kaggle_boundary_rate/zeta_cert_rosen.py",
     "vendored odd-q engine (transitively imported by the even engine)"),
    (LANE_F / "f8_receipts" / "Q8_R2_F1024_LOCAL_RECEIPT.json",
     "lane_f/f8_receipts/Q8_R2_F1024_LOCAL_RECEIPT.json",
     "pinned R2 receipt (PINNED_RECEIPT_SHA256['R2'])"),
    (LANE_F / "f8_receipts" / "Q8_TB_BLOCK_CERTIFICATES_F1024_RECEIPT.json",
     "lane_f/f8_receipts/Q8_TB_BLOCK_CERTIFICATES_F1024_RECEIPT.json",
     "pinned TB receipt (PINNED_RECEIPT_SHA256['TB'])"),
    (LANE_F / "f8_receipts" / "Q8_W_ENVELOPE_F1024_RECEIPT.json",
     "lane_f/f8_receipts/Q8_W_ENVELOPE_F1024_RECEIPT.json",
     "pinned W envelope receipt (PINNED_RECEIPT_SHA256['W'])"),
    (LANE_G / "l_out" / "Q8_R2OUT_F1024_REPIN_THETA1p230_RECEIPT.json",
     "lane_g/l_out/Q8_R2OUT_F1024_REPIN_THETA1p230_RECEIPT.json",
     "pinned L-OUT omitted-output receipt (PINNED_LOUT_SHA256)"),
    (HERE / "q8_leaf_shard.py", "driver/q8_leaf_shard.py",
     "leaf-sharded driver (this campaign; adds no mathematics)"),
    (HERE / "merge_shards.py", "driver/merge_shards.py",
     "merge-time verifier (carried for provenance; not run in-kernel)"),
]

KERNEL_TEMPLATE = '''# ==========================================================================
# {kernel_slug}
# q=8 Schur contour, depth-{depth} parallel subdivision campaign.
# arc {arc}, leaves [{leaf_start}, {leaf_end}) of {leaves_per_arc}, N={N}.
#
# The lane_f checker runs UNMODIFIED.  Every dataset file is sha256-verified
# against manifest.json before the tree is reconstructed; a mismatch aborts.
# ==========================================================================
import glob
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

TREE = "/kaggle/working/tree"
OUT = "/kaggle/working"

# Kaggle mounts a dataset under a name derived from its TITLE, which need not
# equal the id slug ("{dataset_slug}").  Discover the mount by looking for the
# manifest rather than hardcoding a path that silently 404s.
# The mount is also nested (observed: /kaggle/input/datasets/<owner>/<slug>/),
# so search recursively, not just one level down.
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
checkpoint = os.path.join(OUT, "{checkpoint_name}")
cmd = [
    sys.executable, os.path.join(TREE, "driver", "q8_leaf_shard.py"),
    "--lane-f", os.path.join(TREE, "lane_f"),
    "--arc", "{arc}",
    "--leaf-start", "{leaf_start}",
    "--leaf-end", "{leaf_end}",
    "--depth", "{depth}",
    "--N", "{N}",
    "--K", "{K}",
    "--workers", "{workers}",
    "--deadline-seconds", "{deadline}",
    "--out", receipt,
    "--checkpoint", checkpoint,
]
print("RUNNING:", " ".join(cmd), flush=True)
print("cpu_count", os.cpu_count(), flush=True)
t0 = time.time()
result = subprocess.run(cmd)
print("EXIT CODE:", result.returncode, " wall_seconds:", time.time() - t0, flush=True)
# Exit 3 == deadline hit with a partial receipt: still a useful artifact, so do
# not fail the kernel and lose the output.
sys.exit(0 if result.returncode in (0, 3) else result.returncode)
'''


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def flat_name(tree_path: str) -> str:
    return tree_path.replace("/", "__")


def build_dataset(
    out_root: Path, username: str, dataset_slug: str, created: str, depth: int
) -> Path:
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
                "repo_path": str(source.relative_to(RH.parents[1])),
            }
        )
    manifest = {
        "schema": "farey-hecke.q8-schur-subdivision-campaign/1",
        "created": created,
        "lane": "lane_g packaging of an UNMODIFIED lane_f engine",
        "purpose": (
            f"depth-{depth} parallel subdivision of the q=8 Schur contour arc "
            "gate; qOp = 83.79 at depth 0 halves per bisection, so depth 7 is "
            "the smallest depth that clears qOp at all (worst mid-arc leaf "
            "1.3089 at depth 6), and depth 8 is the smallest that also clears "
            "the finite-Taylor zero-exclusion gate (worst rH 0.1945 against "
            "the square-box predictor 0.41421)"
        ),
        "python": ">=3.11",
        "dependencies": {"python-flint": PYTHON_FLINT_PIN},
        "geometry": {
            "K_per_edge": 1,
            "arcs": 4,
            "depth": depth,
            "leaves_per_arc": 1 << depth,
            "leaves_total": 4 * (1 << depth),
        },
        "status_contract": (
            "Shard receipts are CHECKER OUTPUT, not a theorem.  E1, the q=8 "
            "MMS/Hilbert identification, K_s, analytic gates 5-6 and "
            "continuation condition 8 of the 12-item ledger are untouched."
        ),
        "files": files,
    }
    (dataset_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    (dataset_dir / "dataset-metadata.json").write_text(
        json.dumps(
            {
                "title": "q8 schur contour subdivision inputs",
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
    shards: list[tuple[int, int, int]],
    depth: int,
    N: int,
    K: int,
    workers: int,
    deadline: int,
    prefix: str,
) -> list[dict[str, str]]:
    made = []
    for index, (arc, leaf_start, leaf_end) in enumerate(shards):
        kernel_slug = f"{prefix}-s{index:02d}"
        kernel_dir = out_root / "kernels" / kernel_slug
        kernel_dir.mkdir(parents=True, exist_ok=True)
        receipt_name = f"SHARD_a{arc}_l{leaf_start}-{leaf_end}.json"
        script = KERNEL_TEMPLATE.format(
            kernel_slug=kernel_slug,
            dataset_slug=dataset_slug,
            flint_pin=PYTHON_FLINT_PIN,
            arc=arc,
            leaf_start=leaf_start,
            leaf_end=leaf_end,
            leaves_per_arc=1 << depth,
            depth=depth,
            N=N,
            K=K,
            workers=workers,
            deadline=deadline,
            receipt_name=receipt_name,
            checkpoint_name=receipt_name.replace(".json", ".ckpt.json"),
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
                "arc": arc,
                "leaf_start": leaf_start,
                "leaf_end": leaf_end,
                "receipt": receipt_name,
            }
        )
    return made


def plan(depth: int, shard_size: int) -> list[tuple[int, int, int]]:
    leaves = 1 << depth
    if leaves % shard_size:
        raise SystemExit("shard size must divide the leaves per arc")
    return [
        (arc, start, start + shard_size)
        for arc in range(4)
        for start in range(0, leaves, shard_size)
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-root", type=Path, default=HERE / "bundle")
    parser.add_argument("--username", default="saarshai")
    parser.add_argument("--dataset-slug", default="q8-schur-subdivision-inputs")
    parser.add_argument("--prefix", default="q8-schur-d7")
    parser.add_argument("--depth", type=int, default=7)
    parser.add_argument("--N", type=int, default=262)
    parser.add_argument("--K", type=int, default=1)
    parser.add_argument("--shard-size", type=int, default=64)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--deadline", type=int, default=39600)
    parser.add_argument("--created", default="2026-08-20")
    args = parser.parse_args()

    args.out_root.mkdir(parents=True, exist_ok=True)
    dataset_dir = build_dataset(
        args.out_root, args.username, args.dataset_slug, args.created, args.depth
    )
    shards = plan(args.depth, args.shard_size)
    kernels = build_kernels(
        args.out_root, args.username, args.dataset_slug, shards, args.depth,
        args.N, args.K, args.workers, args.deadline, args.prefix,
    )
    summary = {
        "dataset_dir": str(dataset_dir),
        "dataset_id": f"{args.username}/{args.dataset_slug}",
        "shard_count": len(shards),
        "leaves_total": 4 * (1 << args.depth),
        "leaves_per_shard": args.shard_size,
        "kernels": kernels,
    }
    (args.out_root / "PLAN.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
