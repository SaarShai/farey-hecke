#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PACKET=$(CDPATH= cd -- "$HERE/../../.." && pwd)
CURVE="$PACKET/numerics/source/curve_3e14.tsv"
OUTPUT="$HERE/../output"

mkdir -p "$OUTPUT"
gp -q "$HERE/generate_dirichlet_zeros.gp" > "$OUTPUT/pari_low_zeros.tsv"
python3 "$HERE/spectral_reconstruction.py" \
  --curve "$CURVE" \
  --zeros "$OUTPUT/pari_low_zeros.tsv" \
  --output-dir "$OUTPUT"
python3 "$HERE/verify_outputs.py" \
  "$CURVE" \
  "$PACKET/numerics/source/zeros_N8.json" \
  "$OUTPUT"
PYTHONDONTWRITEBYTECODE=1 python3 "$HERE/test_verify_outputs.py"
Rscript "$HERE/plot_reconstruction.R" \
  "$OUTPUT/reconstruction.tsv" \
  "$OUTPUT/spectral_reconstruction.pdf" \
  "$OUTPUT/spectral_reconstruction.png"

(
  cd "$PACKET"
  find numerics/source numerics/spectral/scripts numerics/spectral/output \
    -type f ! -name PACKAGE_MANIFEST.sha256 -print | \
    LC_ALL=C sort | xargs shasum -a 256
) > "$OUTPUT/PACKAGE_MANIFEST.sha256"
