# Low-zero reconstruction of the 300-trillion prime-race curves

This package reconstructs the verified ordinary-count curves for
`N in {7,8,11,19,23}` from the lowest Dirichlet `L`-function zeros.

It is a finite spectral diagnostic.  It does not prove GRH, certify that PARI
found every zero, establish an eventual class ordering, or transfer a theorem
about a regularized statistic to ordinary prime counts.

## Reproduce

Requirements: PARI/GP, Python 3, and R.

```sh
sh run_pipeline.sh
```

The pipeline:

1. computes every nonprincipal character's zeros through height 80 twice,
   with PARI `lfunzeros` mesh parameters 64 and 96;
2. refuses reconstruction unless the two zero lists agree character by
   character and every returned ordinate has `abs(L(1/2+i*gamma)) < 1e-28`;
3. reconstructs the standard normalized race using the first 1, 3, 10, and
   25 positive zeros of every nonprincipal character;
4. writes fit metrics, every observed rank/leader transition, per-mode
   top-decade attribution, and a publication figure.

The verifier additionally matches all three modulo-8 first-zero anchors against
the pre-existing independent mpmath file `../zeros_N8.json` to `1e-12` and
checks the immutable curve hash.  `MANIFEST.sha256` records every source and
generated artifact used in the result.

`transition_summary.tsv` reports how often the rank and leader change in each
window.  This is the compact quantitative test of the claim that interference
has disappeared near the proposed onset scale.

The authoritative input curve remains
`../curve_3e14.tsv`; generated files live under `output/`.

## Independent N=19 follow-up

`independent_n19/` independently brackets the exceptional Conrey-13 zero with
Python FLINT/Arb and extends the N=19 reconstruction to K=50 and K=100 zeros per
character.  Its root search does not call PARI; PARI is used separately for the
deep spectral list and an after-the-fact ordinate comparison.  Run:

```sh
sh independent_n19/run_pipeline.sh
```

See `independent_n19/output/N19_CERTIFICATE.md` and
`independent_n19/output/N19_DEEP_STABILITY.md` for the concise results and
limits of the claims.
