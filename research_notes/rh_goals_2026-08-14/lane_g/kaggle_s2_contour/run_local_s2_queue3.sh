#!/bin/bash
# Final self-healing queue: waits for queue2 to drain, then re-runs ANY of
# the 16 ranges that still lacks a status=complete receipt in either
# chunk_receipts/ (Kaggle) or local_receipts/ (local), 4 at a time.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
CODE=/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/second_pin
PY=/Users/za/.venvs/farey-rh/bin/python
OUT="$HERE/local_receipts"
complete() { # $1 = tag; returns 0 if a complete receipt exists
  "$PY" - "$1" <<'EOF'
import json,sys,os
tag=sys.argv[1]
for d in ('chunk_receipts','local_receipts'):
    p=os.path.join(os.environ['HERE'],d,f'S2_CHUNK_{tag}.json')
    try:
        if json.load(open(p)).get('status')=='complete': sys.exit(0)
    except Exception: pass
sys.exit(1)
EOF
}
export HERE
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
while ! grep -q "queue2 DRAINED" "$OUT/LOCAL_FILL.log" 2>/dev/null; do sleep 120; done
echo "$(date -u +%FT%TZ) queue3 start (self-heal sweep)" >> "$OUT/LOCAL_FILL.log"
live=0
for a in 0 12 24 36 48 60 72 84 96 108 120 132 144 156 168 180; do
  b=$((a+12)); tag=$(printf 'a%03d-%03d' "$a" "$b")
  if complete "$tag"; then continue; fi
  echo "$(date -u +%FT%TZ) queue3 running $tag" >> "$OUT/LOCAL_FILL.log"
  run_chunk "$a" "$b" &
  live=$((live+1))
  if [ "$live" -ge 4 ]; then wait -n 2>/dev/null || wait; live=$((live-1)); fi
done
wait
echo "$(date -u +%FT%TZ) queue3 DRAINED" >> "$OUT/LOCAL_FILL.log"
