#!/bin/bash
# G7 chunk slot-feeder v2 (POSIX-safe: no mapfile; push success verified by
# kernel status, not CLI exit code — kaggle CLI exits 0 on slot-cap errors).
# Exits when all 16 chunks have reached a terminal-or-active state at least once.
# Launch: nohup bash slot_feeder.sh > slot_feeder.log 2>&1 &
cd "$(dirname "$0")" || exit 1
PUSHED_FILE=pushed_chunks.txt
printf '%s\n' 00 01 02 03 04 > "$PUSHED_FILE"   # reset: only 00-04 verified pushed
while true; do
  pushed_count=$(wc -l < "$PUSHED_FILE" | tr -d ' ')
  if [ "$pushed_count" -ge 16 ]; then echo "$(date) all 16 pushed; feeder exiting"; break; fi
  active=0
  while read -r c; do
    st=$(kaggle kernels status "saarshai/f7-r3b-chunk-$c" 2>/dev/null | grep -o 'RUNNING\|QUEUED' | head -1)
    [ -n "$st" ] && active=$((active+1))
  done < "$PUSHED_FILE"
  echo "$(date) pushed=$pushed_count active=$active"
  free=$((5-active))
  for n in $(seq -w 0 15); do
    [ "$free" -le 0 ] && break
    if ! grep -q "^$n$" "$PUSHED_FILE"; then
      ( cd "f7-r3b-chunk-$n" && kaggle kernels push -p . ) >> push_attempts.log 2>&1
      sleep 20
      st=$(kaggle kernels status "saarshai/f7-r3b-chunk-$n" 2>/dev/null | grep -o 'RUNNING\|QUEUED\|COMPLETE' | head -1)
      if [ -n "$st" ]; then
        echo "$(date) chunk $n pushed, status $st"; echo "$n" >> "$PUSHED_FILE"; free=$((free-1))
      else
        echo "$(date) chunk $n push not accepted (status empty); will retry next cycle"
        break
      fi
    fi
  done
  sleep 600
done
