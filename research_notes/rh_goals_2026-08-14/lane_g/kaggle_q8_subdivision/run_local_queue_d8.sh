#!/bin/bash
# Depth-8 local queue: the 11 shards that do NOT fit the 5-slot Kaggle batch cap.
#
# Shard plan is build_bundle.py's own plan(depth=8, shard_size=64): 16 shards,
# arc-major, 64 leaves each, 256 leaves per arc, 1024 leaves total.
#   s00-s03 = arc 0 (Kaggle)      s04 = arc 1 [0,64)  (Kaggle)
#   s05-s07 = arc 1 [64,256)      s08-s11 = arc 2     s12-s15 = arc 3   (local)
#
# Receipts land in shard_receipts/d8/ -- a SEPARATE directory from the depth-7
# receipts, because SHARD_a2_l64-128.json and SHARD_a3_l0-64.json already exist
# there from the depth-7 wave.  The driver's checkpoint loader refuses a
# foreign-parameter checkpoint with SystemExit, so a collision would kill the
# shard rather than corrupt it; separating the directories avoids the abort.
#
# Each shard keeps its own checkpoint, so a kill resumes instead of restarting.
set -u
HERE="/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/kaggle_q8_subdivision"
PY="/Users/za/.venvs/farey-rh/bin/python"
OUTDIR="$HERE/shard_receipts/d8"
WORKERS="${WORKERS:-12}"
mkdir -p "$OUTDIR"

run_shard() {
  local arc="$1" start="$2" end="$3" sid="$4"
  local tag="a${arc}_l${start}-${end}"
  echo "=== QUEUE START $sid $tag $(date -u +%FT%TZ) ==="
  "$PY" "$HERE/q8_leaf_shard.py" \
    --arc "$arc" --leaf-start "$start" --leaf-end "$end" \
    --depth 8 --N 262 --K 1 --workers "$WORKERS" \
    --out "$OUTDIR/SHARD_${tag}.json" \
    --checkpoint "$OUTDIR/SHARD_${tag}.ckpt.json"
  echo "=== QUEUE EXIT $sid $tag rc=$? $(date -u +%FT%TZ) ==="
}

run_shard 1  64 128 s05
run_shard 1 128 192 s06
run_shard 1 192 256 s07
run_shard 2   0  64 s08
run_shard 2  64 128 s09
run_shard 2 128 192 s10
run_shard 2 192 256 s11
run_shard 3   0  64 s12
run_shard 3  64 128 s13
run_shard 3 128 192 s14
run_shard 3 192 256 s15
echo "=== QUEUE DRAINED $(date -u +%FT%TZ) ==="
