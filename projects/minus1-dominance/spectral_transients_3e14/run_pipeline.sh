#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=$(CDPATH= cd -- "$HERE/../../.." && pwd)
CURVE="$ROOT/projects/minus1-dominance/curve_3e14.tsv"
OUTPUT="$HERE/output"

mkdir -p "$OUTPUT"
gp -q "$HERE/generate_dirichlet_zeros.gp" > "$OUTPUT/pari_low_zeros.tsv"
python3 "$HERE/spectral_reconstruction.py" \
  --curve "$CURVE" \
  --zeros "$OUTPUT/pari_low_zeros.tsv" \
  --output-dir "$OUTPUT"
python3 "$HERE/verify_outputs.py" \
  "$CURVE" \
  "$ROOT/projects/minus1-dominance/zeros_N8.json" \
  "$OUTPUT"
PYTHONDONTWRITEBYTECODE=1 python3 "$HERE/test_verify_outputs.py"
Rscript "$HERE/plot_reconstruction.R" \
  "$OUTPUT/reconstruction.tsv" \
  "$OUTPUT/spectral_reconstruction.pdf" \
  "$OUTPUT/spectral_reconstruction.png"

(
  cd "$ROOT"
  shasum -a 256 \
    projects/minus1-dominance/curve_3e14.tsv \
    projects/minus1-dominance/spectral_transients_3e14/generate_dirichlet_zeros.gp \
    projects/minus1-dominance/spectral_transients_3e14/spectral_reconstruction.py \
    projects/minus1-dominance/spectral_transients_3e14/verify_outputs.py \
    projects/minus1-dominance/spectral_transients_3e14/test_verify_outputs.py \
    projects/minus1-dominance/spectral_transients_3e14/output/pari_low_zeros.tsv \
    projects/minus1-dominance/spectral_transients_3e14/output/reconstruction.tsv \
    projects/minus1-dominance/spectral_transients_3e14/output/fit_metrics.tsv \
    projects/minus1-dominance/spectral_transients_3e14/output/rank_transitions.tsv \
    projects/minus1-dominance/spectral_transients_3e14/output/transition_summary.tsv \
    projects/minus1-dominance/spectral_transients_3e14/output/mode_attribution.tsv \
    projects/minus1-dominance/spectral_transients_3e14/output/spectral_reconstruction.pdf \
    projects/minus1-dominance/spectral_transients_3e14/output/spectral_reconstruction.png
) > "$OUTPUT/MANIFEST.sha256"
