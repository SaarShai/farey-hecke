#!/bin/bash
# Local re-run of the four wave-1 S2 chunks that came back PARTIAL from
# Kaggle (11 h in-kernel deadline hit mid-arc; driver has no resume).
# 4 concurrent chunk orchestrators x 3 workers = 12 cores, nice 10.
# Receipts land in local_receipts/ (kept separate from Kaggle
# chunk_receipts/ until verified COMPLETE, then copied over).
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
CODE=/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/second_pin
PY=/Users/za/.venvs/farey-rh/bin/python
OUT="$HERE/local_receipts"
mkdir -p "$OUT"
run_chunk() {
  local a=$1 b=$2
  local tag=$(printf 'a%03d-%03d' "$a" "$b")
  ( cd "$CODE" && nice -n 10 "$PY" certify_r3b_flagship.py \
      --arcs "$a:$b" --workers 3 --skip-comparison \
      --receipt "$OUT/S2_CHUNK_${tag}.json" \
      --checkpoint "$OUT/S2_CHUNK_${tag}.ckpt.json" \
      --report "$OUT/S2_CHUNK_${tag}.md" \
      > "$OUT/local_${tag}.log" 2>&1 )
  echo "$(date -u +%FT%TZ) chunk $tag exit=$?" >> "$OUT/LOCAL_FILL.log"
}
echo "$(date -u +%FT%TZ) local S2 fill start: 0:12 12:24 24:36 48:60" >> "$OUT/LOCAL_FILL.log"
run_chunk 0 12 &
run_chunk 12 24 &
run_chunk 24 36 &
run_chunk 48 60 &
wait
echo "$(date -u +%FT%TZ) local S2 fill DRAINED" >> "$OUT/LOCAL_FILL.log"
