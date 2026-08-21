#!/bin/bash
# Local fallback queue for the shards Kaggle refused with
#   "Kernel push error: Maximum batch CPU session count of 5 reached."
# Runs the queued shards sequentially, each with its own checkpoint so a kill
# resumes instead of restarting.  Receipts land in shard_receipts/.
set -u
HERE="/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/kaggle_q8_subdivision"
PY="/Users/za/.venvs/farey-rh/bin/python"
WORKERS="${WORKERS:-12}"
mkdir -p "$HERE/shard_receipts"

run_shard() {
  local arc="$1" start="$2" end="$3"
  local tag="a${arc}_l${start}-${end}"
  echo "=== QUEUE START $tag $(date -u +%FT%TZ) ==="
  "$PY" "$HERE/q8_leaf_shard.py" \
    --arc "$arc" --leaf-start "$start" --leaf-end "$end" \
    --depth 7 --N 262 --K 1 --workers "$WORKERS" \
    --out "$HERE/shard_receipts/SHARD_${tag}.json" \
    --checkpoint "$HERE/shard_receipts/SHARD_${tag}.ckpt.json"
  echo "=== QUEUE EXIT $tag rc=$? $(date -u +%FT%TZ) ==="
}

run_shard 2 64 128   # s05
run_shard 3 0 64     # s06
run_shard 3 64 128   # s07
echo "=== QUEUE DRAINED $(date -u +%FT%TZ) ==="
