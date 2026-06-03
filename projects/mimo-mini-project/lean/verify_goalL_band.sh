#!/usr/bin/env bash
# Reproducibly verify the Goal-L Hecke scalar window-lemma band (q = 7..16) + the lam-bound lemma.
# Each file proves the genuine-domain window lemma whose orbit form feeds the verified essSup engine
# (=> X_Omega(q) = 1/lam^3).  Re-compiles every file against a full-Mathlib v4.28.0 env and asserts
#   EXIT=0  AND  axioms = [propext, Classical.choice, Quot.sound]  (no sorryAx).
#
# Usage:   ./verify_goalL_band.sh [ENV_DIR]
#   ENV_DIR = a Lake project with Mathlib v4.28.0 built (8018 oleans). Default: /tmp/lean-minus1
#   (rebuild per project_farey_lean_infra if gone: fresh checkout + `lake exe cache get`).
#
# Per-file heartbeat budget is embedded via `set_option maxHeartbeats` in each file:
#   q=7..11  (window W=4):  1.6M   (each ~1-2 min)
#   q=12..16 (window W=5): 20M     (q=16 deg-8 field ~8 min; the rest faster)
# Total wall-clock ~20-30 min single-threaded.

set -uo pipefail
ENV_DIR="${1:-/tmp/lean-minus1}"
LAKE="$HOME/.elan/bin/lake"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FILES=(HeckeLamBounds_VERIFIED \
       BCZHeckeG7_window_VERIFIED  BCZHeckeG8_window_VERIFIED  BCZHeckeG9_window_VERIFIED \
       BCZHeckeG10_window_VERIFIED BCZHeckeG11_window_VERIFIED BCZHeckeG12_window_VERIFIED \
       BCZHeckeG13_window_VERIFIED BCZHeckeG14_window_VERIFIED BCZHeckeG15_window_VERIFIED \
       BCZHeckeG16_window_VERIFIED)

[ -d "$ENV_DIR" ] || { echo "ENV_DIR '$ENV_DIR' not found (need a built Mathlib v4.28.0 Lake project)"; exit 2; }
[ -x "$LAKE" ]    || { echo "lake not found at $LAKE"; exit 2; }

pass=0; fail=0
for f in "${FILES[@]}"; do
  cp "$HERE/$f.lean" "$ENV_DIR/$f.lean"
  out="$( cd "$ENV_DIR" && "$LAKE" env lean "$f.lean" 2>&1 )"; ec=$?
  bad_axiom=$(echo "$out" | grep -E "depends on axioms" | grep -vE "\[propext, Classical.choice, Quot.sound\]" | head -1)
  sorry=$(echo "$out" | grep -c "sorryAx")
  if [ "$ec" -eq 0 ] && [ "$sorry" -eq 0 ] && [ -z "$bad_axiom" ]; then
    echo "OK    $f  (EXIT=0, axioms clean)"; pass=$((pass+1))
  else
    echo "FAIL  $f  (EXIT=$ec, sorryAx=$sorry)"; [ -n "$bad_axiom" ] && echo "      extra axiom: $bad_axiom"
    echo "$out" | grep -iE "error|timeout" | head -3 | sed 's/^/      /'
    fail=$((fail+1))
  fi
done
echo "----"
echo "BAND RESULT: $pass passed, $fail failed (of ${#FILES[@]})"
[ "$fail" -eq 0 ] && echo "X_Omega(q)=1/lam^3 window lemmas verified for q=7..16." || exit 1
