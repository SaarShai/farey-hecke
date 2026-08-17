#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PACKET=$(CDPATH= cd -- "$HERE/../../.." && pwd)
CURVE="$PACKET/numerics/source/curve_3e14.tsv"
PARI25="$PACKET/numerics/spectral/output/pari_low_zeros.tsv"
OUTPUT="$HERE/../output"

mkdir -p "$OUTPUT"
ZERO_TMP=$(mktemp "$OUTPUT/.pari_n19_100_zeros.XXXXXX")
ZERO_PARTS=$(mktemp -d "$OUTPUT/.pari_n19_parts.XXXXXX")
cleanup() {
  rm -f "$ZERO_TMP"
  for PART in "$ZERO_PARTS"/*.tsv; do
    if [ -f "$PART" ]; then rm -f "$PART"; fi
  done
  rmdir "$ZERO_PARTS" 2>/dev/null || true
}
trap cleanup EXIT HUP INT TERM
generate_one() {
  M=$1
  PART="$ZERO_PARTS/$M.tsv"
  ATTEMPT=1
  while [ "$ATTEMPT" -le 3 ]; do
    : > "$PART"
    if N19_CONREY_M=$M gp -q "$HERE/generate_n19_100_zeros.gp" > "$PART" && \
      awk -F '\t' '
        $1 == "CHECK" {checks++; if ($8 == "PASS" && $4 >= 100 && $5 >= 100) passes++}
        $1 == "ZERO" {zeros++}
        END {exit !(checks == 1 && passes == 1 && zeros >= 100)}
      ' "$PART"; then
      return 0
    fi
    ATTEMPT=$((ATTEMPT + 1))
  done
  echo "q=19 Conrey $M failed after 3 attempts" >&2
  return 1
}

# Four independent GP processes keep the wall time short while bounding memory.
for BATCH in "2 3 4 5" "6 7 8 9" "10 11 12 13" "14 15 16 17" "18"; do
  for M in $BATCH; do generate_one "$M" & done
  wait
done
for M in $(seq 2 18); do
  cat "$ZERO_PARTS/$M.tsv" >> "$ZERO_TMP"
done
mv "$ZERO_TMP" "$OUTPUT/pari_n19_100_zeros.tsv"

PYTHONDONTWRITEBYTECODE=1 uv run --no-project \
  --with python-flint==0.9.0 --with mpmath==1.3.0 \
  python3 "$HERE/certify_n19.py" \
  --curve "$CURVE" --pari "$PARI25" --output-dir "$OUTPUT"

PYTHONDONTWRITEBYTECODE=1 python3 "$HERE/n19_deep_reconstruction.py" \
  --curve "$CURVE" --zeros "$OUTPUT/pari_n19_100_zeros.tsv" --output-dir "$OUTPUT"

PYTHONDONTWRITEBYTECODE=1 uv run --no-project --with python-flint==0.9.0 \
  python3 "$HERE/verify_independent_n19.py" "$CURVE" "$OUTPUT"

PYTHONDONTWRITEBYTECODE=1 uv run --no-project --with python-flint==0.9.0 \
  python3 "$HERE/test_verify_independent_n19.py"

(
  cd "$PACKET"
  find numerics/source numerics/spectral/output/pari_low_zeros.tsv \
    numerics/n19/scripts numerics/n19/output \
    -type f ! -name PACKAGE_MANIFEST.sha256 -print | \
    LC_ALL=C sort | xargs shasum -a 256
) > "$OUTPUT/PACKAGE_MANIFEST.sha256"
