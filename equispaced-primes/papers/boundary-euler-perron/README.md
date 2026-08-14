# Boundary Euler-product / Perron paper extraction

This is the audited single-author technical note selected from the broader
Koyama-era material.  It deliberately separates:

- the proved boundary prime-power identity with a canonical radial logarithm;
- the proved local double-pole residue;
- the unproved and currently excluded global partial-Möbius asymptotic.

The primary-source novelty audit is in `NOVELTY_AND_PROOF_STATUS.md`. Its
verdict is that the two proved statements do **not** clear a standalone-paper
novelty threshold; the defensible disposition is a technical appendix or
reproducibility certificate.

Build with the bundled Tectonic binary used in this workspace:

```sh
/Users/za/.codex/.tmp/bundled-marketplaces/openai-bundled/plugins/latex/bin/tectonic paper.tex
```

The document is not a submission draft. Its central theorem is closed, but the
novelty gate fails and its numerical audit remains future work.

Check the exact rational coefficient cancellation and two double-precision
finite-prime instances with:

```sh
python3 verify_finite_identity.py
```

This verifier covers the algebraic four-term decomposition, including the
imprimitive bad-prime correction. It does not certify the boundary limit.
