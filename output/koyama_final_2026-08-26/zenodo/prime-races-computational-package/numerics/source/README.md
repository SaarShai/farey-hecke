# Ordinary prime-count race data

- `curve_3e14.tsv` — authoritative ordinary-count curve: N in {7, 8, 11, 19, 23},
  438 logarithmically spaced checkpoints through 3e14, per-class counts.
  SHA-256: 57957bdb3ce3243272c3d4b8e9ffe7dfb734b759f48b63becf7ae6f924e1caab.
- `out2.tsv` — independently checked baseline through 1.3e13.
- `verify_shared_baseline.py` — exact integer comparison of the 567 shared
  cells (paths are relative to this directory):
  `python3 verify_shared_baseline.py`.
- `zeros_N8.json` — pre-existing independent mpmath first-zero anchors mod 8,
  used by the spectral pipeline's verifier.
