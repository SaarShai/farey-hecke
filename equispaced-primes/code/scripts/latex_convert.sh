#!/usr/bin/env bash
# LaTeX conversion test for Delta-machine Compositio paper draft.
# Usage:  ./scripts/latex_convert.sh [output_dir]
# Pre-req: brew install pandoc texlive (~5 min on macOS)
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT_DIR="${1:-$REPO_ROOT/paper/latex_build}"
SRC="$REPO_ROOT/paper/Delta_machine_paper_compositio_draft.md"

mkdir -p "$OUT_DIR"
cd "$OUT_DIR"

if ! command -v pandoc >/dev/null 2>&1; then
  echo "ERROR: pandoc not installed. Install via:  brew install pandoc"
  echo "       For full PDF builds also:           brew install --cask mactex-no-gui"
  exit 1
fi

echo "=== pandoc version ==="
pandoc --version | head -1

echo ""
echo "=== converting to LaTeX ==="
pandoc -f markdown -t latex \
  --standalone \
  --number-sections \
  -V documentclass=article \
  -V geometry:margin=1in \
  -V fontsize=11pt \
  "$SRC" -o "$OUT_DIR/delta_machine.tex" 2>&1 | tee "$OUT_DIR/pandoc.log"

echo ""
echo "=== output stats ==="
wc -l "$OUT_DIR/delta_machine.tex"

echo ""
echo "=== warnings/errors ==="
grep -iE "warn|error|fail" "$OUT_DIR/pandoc.log" | head -20 || echo "(clean)"

if command -v pdflatex >/dev/null 2>&1; then
  echo ""
  echo "=== building PDF (pdflatex pass 1) ==="
  pdflatex -interaction=nonstopmode -output-directory "$OUT_DIR" "$OUT_DIR/delta_machine.tex" \
    > "$OUT_DIR/pdflatex.log" 2>&1 || true
  echo "=== building PDF (pdflatex pass 2 — for refs) ==="
  pdflatex -interaction=nonstopmode -output-directory "$OUT_DIR" "$OUT_DIR/delta_machine.tex" \
    >> "$OUT_DIR/pdflatex.log" 2>&1 || true
  if [ -f "$OUT_DIR/delta_machine.pdf" ]; then
    echo "PDF built: $OUT_DIR/delta_machine.pdf"
  else
    echo "PDF build failed; see $OUT_DIR/pdflatex.log"
  fi
else
  echo ""
  echo "(pdflatex not installed; skipping PDF build. Install via:  brew install --cask mactex-no-gui)"
fi
