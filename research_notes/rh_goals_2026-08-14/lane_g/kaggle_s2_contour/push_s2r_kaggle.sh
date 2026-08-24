#!/bin/bash
# Feed the 16 S2 N=288 contour chunks (s00-s15) through Kaggle's 5 batch-CPU
# slots as they free up.  Modeled exactly on kaggle_q8_subdivision/
# push_d8_kaggle.sh — including the KernelWorkerStatus literal-enum status
# check (a bare RUNNING/ERROR grep falsely confirmed on "ConnectionError"
# during an offline window, 2026-08-21).
#
# NON-DESTRUCTIVE: the d8 wave-2 kernels (q8-schur-d8-s00..s04) currently hold
# the 5 slots and are NEVER cancelled or deleted; this poller waits for slots
# and feeds the S2 chunks through in waves.  Idempotent: a chunk with a
# .pushed marker is skipped on later passes.
set -u
HERE="/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/kaggle_s2_contour"
KAGGLE="/Users/za/.local/bin/kaggle"
BUNDLE="$HERE/bundle/kernels"
MARKERS="$HERE/chunk_receipts"
SHARDS=""
for i in $(seq -w 0 21); do SHARDS="$SHARDS s2-contour-n288r-s$i"; done
SLEEP="${SLEEP:-300}"

mkdir -p "$MARKERS"
pushed_marker() { echo "$MARKERS/.pushed_$1"; }

echo "=== S2R CONTOUR KAGGLE PUSHER START $(date -u +%FT%TZ) ==="
while :; do
  for slug in $SHARDS; do
    [ -f "$(pushed_marker "$slug")" ] && continue
    echo "--- push attempt $slug $(date -u +%FT%TZ) ---"
    out="$("$KAGGLE" kernels push -p "$BUNDLE/$slug" 2>&1 | grep -iv key)"
    echo "$out"
    if echo "$out" | grep -qi "Maximum batch CPU session count"; then
      echo "SLOT BUSY: $slug deferred"
      break
    fi
    # Do NOT decide success from the push message alone: if the wording
    # drifts, a successful push would be retried forever, spawning duplicate
    # versions.  Authority is the kernel's own status.  Anything that is not
    # an explicit error gets 25 s to register, then status decides.
    sleep 25
    st="$("$KAGGLE" kernels status "saarshai/$slug" 2>&1 | grep -iv "key\|Warning")"
    echo "status: $st"
    # Require the CLI's own enum ("KernelWorkerStatus.X") — a bare RUNNING/
    # ERROR match falsely confirmed on "ConnectionError" during an offline
    # window (2026-08-21, markers set with no kernel existing).
    if echo "$st" | grep -qE "KernelWorkerStatus\.(RUNNING|QUEUED|COMPLETE|ERROR|CANCEL)"; then
      touch "$(pushed_marker "$slug")"
      echo "PUSHED $slug (status confirms the kernel exists and has a run)"
    else
      echo "NO CONFIRMED RUN for $slug; will retry next pass"
      break
    fi
  done
  left=0
  for slug in $SHARDS; do
    [ -f "$(pushed_marker "$slug")" ] || left=$((left + 1))
  done
  if [ "$left" -eq 0 ]; then
    echo "=== ALL 16 S2 KERNELS PUSHED $(date -u +%FT%TZ) ==="
    break
  fi
  echo "waiting: $left kernel(s) still unpushed; sleeping ${SLEEP}s"
  sleep "$SLEEP"
done

echo "=== FINAL STATUSES $(date -u +%FT%TZ) ==="
for slug in $SHARDS; do
  printf "%s: " "$slug"
  "$KAGGLE" kernels status "saarshai/$slug" 2>&1 | grep -iv "key\|Warning"
done
echo "=== S2 CONTOUR KAGGLE PUSHER DONE $(date -u +%FT%TZ) ==="
