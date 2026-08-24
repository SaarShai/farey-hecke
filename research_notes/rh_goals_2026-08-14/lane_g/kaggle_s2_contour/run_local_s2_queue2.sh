#!/bin/bash
# Follow-on local queue: waits for the wave-1 fill (run_local_s2_fill.sh) to
# drain, then certifies the six ranges not yet started anywhere but Kaggle's
# unpushed s10-s15 backlog (a120-192). First-complete wins vs Kaggle; the
# merge takes any receipt with status=complete per range.
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
# wait for wave-1 fill to drain
while ! grep -q DRAINED "$OUT/LOCAL_FILL.log" 2>/dev/null; do sleep 120; done
echo "$(date -u +%FT%TZ) queue2 start: 120..192 in two batches of 3+3 x4workers? no: 4-then-2" >> "$OUT/LOCAL_FILL.log"
run_chunk 120 132 &
run_chunk 132 144 &
run_chunk 144 156 &
run_chunk 156 168 &
wait
run_chunk 168 180 &
run_chunk 180 192 &
wait
echo "$(date -u +%FT%TZ) queue2 DRAINED" >> "$OUT/LOCAL_FILL.log"
