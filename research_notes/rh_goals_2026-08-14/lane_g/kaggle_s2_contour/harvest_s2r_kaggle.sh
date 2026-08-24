#!/bin/bash
# Harvest completed S2 contour kernels into chunk_receipts/.  Idempotent:
# a chunk whose receipt JSON is already present is skipped.  Never cancels
# or deletes anything.  Run repeatedly (or via a loop) until all 16 land,
# then run merge_s2_chunks.py.
set -u
HERE="/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/kaggle_s2_contour"
KAGGLE="/Users/za/.local/bin/kaggle"
DEST="$HERE/chunk_receipts"
mkdir -p "$DEST"

have=0
for i in $(seq -w 0 21); do
  slug="s2-contour-n288r-s$i"
  chunk=$((10#$i))
  a=$(printf "%03d" $((60 + chunk * 6)))
  b=$(printf "%03d" $((60 + chunk * 6 + 6)))
  receipt="S2_CHUNK_a$a-$b.json"
  if [ -f "$DEST/$receipt" ]; then
    have=$((have + 1))
    continue
  fi
  st="$("$KAGGLE" kernels status "saarshai/$slug" 2>&1 | grep -iv "key\|Warning")"
  echo "$slug: $st"
  if echo "$st" | grep -q "KernelWorkerStatus\.COMPLETE"; then
    tmp="$DEST/.harvest_$slug"
    mkdir -p "$tmp"
    "$KAGGLE" kernels output "saarshai/$slug" -p "$tmp" 2>&1 | grep -iv key
    if [ -f "$tmp/$receipt" ]; then
      mv "$tmp/$receipt" "$DEST/$receipt"
      [ -f "$tmp/${receipt%.json}.md" ] && mv "$tmp/${receipt%.json}.md" "$DEST/"
      [ -f "$tmp/${receipt%.json}.ckpt.json" ] && mv "$tmp/${receipt%.json}.ckpt.json" "$DEST/"
      echo "HARVESTED $receipt"
      have=$((have + 1))
    else
      echo "WARNING: $slug COMPLETE but $receipt missing from output (check logs)"
    fi
    rm -rf "$tmp"
  fi
done
echo "harvested: $have/16"
if [ "$have" -eq 16 ]; then
  echo "ALL CHUNKS IN — run: /Users/za/.venvs/farey-rh/bin/python $HERE/merge_s2_chunks.py"
fi
