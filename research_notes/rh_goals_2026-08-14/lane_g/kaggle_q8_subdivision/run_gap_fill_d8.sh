#!/bin/bash
# Depth-8 GAP FILL: the 5 Kaggle-partial spans (s00-s04), seeded from the
# harvested checkpoints copied into shard_receipts/d8/ (see
# lane_g/D8_HARVEST_RECEIPT.md, gap-fill section).  Same driver + receipt
# schema as run_local_queue_d8.sh; the driver resumes from --checkpoint, so
# only the 101 missing leaves are computed (pending 23+14+7+27+30).
set -u
HERE="/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/kaggle_q8_subdivision"
PY="/Users/za/.venvs/farey-rh/bin/python"
OUTDIR="$HERE/shard_receipts/d8"
WORKERS="${WORKERS:-12}"
mkdir -p "$OUTDIR"

run_shard() {
  local arc="$1" start="$2" end="$3" sid="$4"
  local tag="a${arc}_l${start}-${end}"
  echo "=== GAPFILL START $sid $tag $(date -u +%FT%TZ) ==="
  "$PY" "$HERE/q8_leaf_shard.py" \
    --arc "$arc" --leaf-start "$start" --leaf-end "$end" \
    --depth 8 --N 262 --K 1 --workers "$WORKERS" \
    --out "$OUTDIR/SHARD_${tag}.json" \
    --checkpoint "$OUTDIR/SHARD_${tag}.ckpt.json"
  echo "=== GAPFILL EXIT $sid $tag rc=$? $(date -u +%FT%TZ) ==="
}

run_shard 0   0  64 s00
run_shard 0  64 128 s01
run_shard 0 128 192 s02
run_shard 0 192 256 s03
run_shard 1   0  64 s04
echo "=== GAPFILL DRAINED $(date -u +%FT%TZ) ==="
