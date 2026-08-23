# ==========================================================================
# s2-contour-n288-s05
# S2 second-pin G_5 winding box, N=288 contour campaign.
# chunk 5: base arcs [60, 72) of 192, N=288, workers=4.
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

receipt = os.path.join(OUT, "S2_CHUNK_a060-072.json")
cmd = [
    sys.executable,
    os.path.join(TREE, ".worktrees/aletheia-restore/code/second_pin/certify_r3b_flagship.py"),
    "--arcs", "60:72",
    "--workers", "4",
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
DEADLINE = 39600
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
