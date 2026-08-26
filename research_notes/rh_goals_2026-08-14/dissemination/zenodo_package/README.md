# Data-availability package

%% OWNER-TODO: licence (e.g. CC-BY-4.0 for text/data, MIT/Apache-2.0 for
%% code) to be chosen and this placeholder replaced before deposit.

Supporting material for the preprint at
`research_notes/rh_goals_2026-08-14/dissemination/preprint/main.tex`,
assembled per that paper's §6 ("Machine verification") and its
"Data availability" subsection.

## Contents

```
lean/
  VERIFICATION.md                          -- axiom lists, re-elaboration recipe, toolchain versions
  v34_TwoPinNoLine/TwoPinNoLine.lean        -- paper §6, §4.4 (Corollary "no common line")
  v33_LawSkeletonI/LawSkeletonI.lean        -- paper §6 (the LAW's Lean-verified finish, H1-H5)
  v33_Scat1Lemma31Reflection/Scat1Lemma31Reflection.lean
                                             -- paper §4.4.1 (pole-to-zero reflection core)
certificates/
  pin1_flagship/R3B_FLAGSHIP_CERT.md, R3B_FLAGSHIP_CERT_RECEIPT.json
                                             -- paper §4.3 pin 1 (DECLARED 2026-08-15), Theorem "two pins"
  pin2_second/W_ENVELOPE_CERT_S2.md, W_ENVELOPE_CERT_S2_RECEIPT.json
                                             -- paper §4.3 pin 2 (REFEREED / PROMOTED 2026-08-26)
shard_receipts_d8/
  SHARD_a{0-3}_l{0-64,64-128,128-192,192-256}.json (16 files, non-checkpoint)
                                             -- paper §sec:q8 / FIG-1: 1024 depth-8 leaves, 4 arcs
make_fig1.py                                -- regenerates fig1_qop_hist.pdf from shard_receipts_d8/
fig1_qop_hist.pdf                           -- rendered output of make_fig1.py (checked into this package)
MANIFEST.txt                                -- sha256 of every file in this package
```

## Mapping to paper sections

- **§6 Machine verification / Data availability.** `lean/` and
  `lean/VERIFICATION.md`: the three Lean 4 sources the paper names as
  machine-verified artifacts, with exact axiom lists
  `[propext, Classical.choice, Quot.sound]`, the re-elaboration recipe,
  and the pinned Lean/Mathlib toolchain (`leanprover/lean4:v4.28.0`,
  Mathlib `rev = v4.28.0`).
- **§4.3 "The two certified pins at q=5" (Theorem "two pins").**
  `certificates/pin1_flagship/` and `certificates/pin2_second/`: the
  interval-arithmetic winding=1 contour certificates (Arb argument
  principle, directed rounding) for the two Selberg-zeta zeros of
  `G_5` that the paper's two-pin witness (§4.4, Metatheorem III)
  transports to `\varphi_5` via the Lean reflection core.
- **§sec:q8 / Figure 1 (qOp distribution).** `shard_receipts_d8/` (the
  16 non-checkpoint depth-8 shard receipts covering all 1024 leaves
  across 4 arcs) and `make_fig1.py`, which reproduces
  `fig1_qop_hist.pdf` from them: parse each `qOp_upper` interval string
  `'[m +/- r]'`, take the upper endpoint `m+r`, group by arc, 60 common
  bins, step histograms, reference line at `1/(1+sqrt(2))`.

## Artifacts the paper cites that are NOT included

- No specific certificate filename for the two q=5 pins is given as a
  literal path anywhere in `main.tex`; the mapping above was made by
  matching the paper's prose description (dates, "flagship"/"second
  pin" naming, winding=1 verdict) against the corresponding files under
  `research_notes/rh_goals_2026-08-14/lane_g/`. This is a best-effort
  identification, not a citation the paper spells out — flag for owner
  confirmation before the Zenodo DOI is minted.
- The Appendix A independent-numerics referee code and the
  cross-host determinism / merge-checkpoint files
  (`Q8_D8_MERGED_CHECKPOINT.json`, `Q8_D8_MERGE_REPORT.json`) mentioned
  in prose but not named as individually cited artifacts were left out
  of this package to keep it scoped to what §6 and Figure 1 actually
  need; add them if the owner wants the full audit trail archived too.

## Regenerating Figure 1

```
python3 make_fig1.py shard_receipts_d8/ fig1_qop_hist.pdf
```

Requires `matplotlib`. Verified reproduction range: 1024 values loaded,
`qOp_upper` in `[0.21881, 0.32723]`, matching the paper's stated
"approximately 0.22-0.33" annotation.
