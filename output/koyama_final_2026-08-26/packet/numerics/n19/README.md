# Independent N=19 certification and K=100 audit

This subtree contains two deliberately separated computations.

1. `certify_n19.py` constructs the primitive character modulo 19 with Conrey
   index 13 directly in Python FLINT 0.9.0.  Arb ball evaluation of its real
   Hardy Z-function at exact rational endpoints gives opposite, sign-definite
   values.  Continuity certifies existence of at least one critical-line zero
   in the resulting interval.  PARI is used only afterward to compare the
   independently found ordinate.
2. `generate_n19_100_zeros.gp` and `n19_deep_reconstruction.py` extend the
   spectral diagnostic from K=25 to K=50 and K=100 positive zeros per
   nonprincipal character.  Each character is run in a separate GP process to
   keep memory bounded.  Two `lfunzeros` meshes must agree and every direct
   L-value residual must be below `1e-28`.

The Arb sign-change bracket proves existence, not uniqueness within the
bracket, zero completeness below it, GRH, or any eventual prime-race ordering.
The safe manuscript claim is therefore that an active critical-line zero
exists near `0.018956399080226143`, far below the printed `1.74` ordinate.

## Reproduce

From the packet root:

```sh
sh numerics/n19/scripts/run_pipeline.sh
```

Requirements: PARI/GP, `uv`, and Python 3.  The pipeline pins and obtains
`python-flint==0.9.0`; the independent mode calculation additionally pins
`mpmath==1.3.0`.

Primary human-readable results:

- `output/N19_CERTIFICATE.md`
- `output/N19_DEEP_STABILITY.md`

Machine-readable results and gates:

- `output/n19_arb_certificate.json`
- `output/n19_certificate.tsv`
- `output/pari_n19_100_zeros.tsv`
- `output/n19_deep_reconstruction.tsv`
- `output/n19_deep_metrics.tsv`
- `output/n19_deep_stability.tsv`
- `output/n19_deep_rank_summary.tsv`
- `verify_independent_n19.py`
- `test_verify_independent_n19.py`
- `output/ORIGINAL_REPO_MANIFEST.sha256` (original repository paths and hashes)

The portable packet copies are covered by the top-level
`support/SHA256SUMS.txt`.
