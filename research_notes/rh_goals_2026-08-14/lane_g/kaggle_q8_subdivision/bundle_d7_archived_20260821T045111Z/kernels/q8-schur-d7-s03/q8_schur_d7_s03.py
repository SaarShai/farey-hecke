# ==========================================================================
# q8-schur-d7-s03
# q=8 Schur contour, depth-7 parallel subdivision campaign.
# arc 1, leaves [64, 128) of 128, N=262.
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
# equal the id slug ("q8-schur-subdivision-inputs").  Discover the mount by looking for the
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
        [sys.executable, "-m", "pip", "install", "-q", "python-flint==0.9.0"],
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

receipt = os.path.join(OUT, "SHARD_a1_l64-128.json")
checkpoint = os.path.join(OUT, "SHARD_a1_l64-128.ckpt.json")
cmd = [
    sys.executable, os.path.join(TREE, "driver", "q8_leaf_shard.py"),
    "--lane-f", os.path.join(TREE, "lane_f"),
    "--arc", "1",
    "--leaf-start", "64",
    "--leaf-end", "128",
    "--depth", "7",
    "--N", "262",
    "--K", "1",
    "--workers", "4",
    "--deadline-seconds", "39600",
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
