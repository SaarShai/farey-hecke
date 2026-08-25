#!/bin/bash
# Replaces queue3: keeps N chunks in flight using a portable poll (macOS bash
# 3.2 has no `wait -n`, which turned queue3's dispatcher into a full barrier).
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
CODE=/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/second_pin
PY=/Users/za/.venvs/farey-rh/bin/python
OUT="$HERE/local_receipts"
MAX=4
export HERE
complete() {
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
inflight() { ps ax -o command= | grep -c '[c]ertify_r3b_flagship.py --arcs'; }
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
echo "$(date -u +%FT%TZ) queue4 start (portable dispatcher, MAX=$MAX)" >> "$OUT/LOCAL_FILL.log"
for a in 0 12 24 36 48 60 72 84 96 108 120 132 144 156 168 180; do
  b=$((a+12)); tag=$(printf 'a%03d-%03d' "$a" "$b")
  complete "$tag" && continue
  # already running (e.g. a108-120 inherited from queue3)?
  if ps ax -o command= | grep -q "[c]ertify_r3b_flagship.py --arcs $a:$b"; then
    echo "$(date -u +%FT%TZ) queue4 adopting in-flight $tag" >> "$OUT/LOCAL_FILL.log"
    continue
  fi
  while [ "$(inflight)" -ge "$MAX" ]; do sleep 60; done
  echo "$(date -u +%FT%TZ) queue4 running $tag" >> "$OUT/LOCAL_FILL.log"
  run_chunk "$a" "$b" &
  sleep 5
done
wait
echo "$(date -u +%FT%TZ) queue4 DRAINED" >> "$OUT/LOCAL_FILL.log"
