#!/bin/bash
# Push + start the 5 depth-8 Kaggle shards (s00-s04) as soon as a batch CPU
# session slot frees.
#
# Why a poller: the 5 depth-7 kernels are RUNNING and Kaggle's CLI has NO
# cancel/stop verb (only list/files/get/init/push/pull/output/status/logs/
# update/delete).  A no-op push meant to supersede them is itself refused by
# the very quota it would free ("Maximum batch CPU session count of 5
# reached"), and `delete` is destructive, so the non-destructive route is to
# wait for their own 39600 s deadline guard to expire (~11:00 UTC 2026-08-21)
# and claim the slots then.  This is off the critical path: the local queue
# carries 11 shards for ~23 h, so Kaggle shards starting ~6 h from launch and
# finishing ~6.3 h later still land well inside the local window.
#
# Idempotent: a kernel already pushed is skipped on later passes.
set -u
HERE="/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/kaggle_q8_subdivision"
KAGGLE="/Users/za/.local/bin/kaggle"
BUNDLE="$HERE/bundle/kernels"
SHARDS="q8-schur-d8-s00 q8-schur-d8-s01 q8-schur-d8-s02 q8-schur-d8-s03 q8-schur-d8-s04"
SLEEP="${SLEEP:-300}"

pushed_marker() { echo "$HERE/shard_receipts/d8/.pushed_$1"; }

echo "=== D8 KAGGLE PUSHER START $(date -u +%FT%TZ) ==="
while :; do
  remaining=0
  for slug in $SHARDS; do
    [ -f "$(pushed_marker "$slug")" ] && continue
    remaining=$((remaining + 1))
    echo "--- push attempt $slug $(date -u +%FT%TZ) ---"
    out="$("$KAGGLE" kernels push -p "$BUNDLE/$slug" 2>&1 | grep -iv key)"
    echo "$out"
    if echo "$out" | grep -qi "Maximum batch CPU session count"; then
      echo "SLOT BUSY: $slug deferred"
      break
    fi
    # Do NOT decide success from the push message alone: if the wording drifts,
    # a successful push would be retried forever, spawning duplicate versions.
    # Authority is the kernel's own status.  Anything that is not an explicit
    # error gets 25 s to register, then status decides.
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
  # recount after the pass
  left=0
  for slug in $SHARDS; do
    [ -f "$(pushed_marker "$slug")" ] || left=$((left + 1))
  done
  if [ "$left" -eq 0 ]; then
    echo "=== ALL 5 D8 KERNELS PUSHED $(date -u +%FT%TZ) ==="
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
echo "=== D8 KAGGLE PUSHER DONE $(date -u +%FT%TZ) ==="
