# Koyama Tables 3–7 Replication — Artefact Bundle

Drop this directory into the CREST grant supplementary materials.

## What the panel should read

1. **`CREST_EXECUTIVE_ONEPAGE.pdf`** — one-page summary, grant-ready.
2. **`plots/dominance_figure.pdf`** — the headline figure: dominance trajectory of -1 (mod N) across the 9-checkpoint grid, plus rank bar chart at the headline checkpoints.
3. **`REPLICATION_REPORT.md`** — full cell-by-cell comparison vs Koyama draft, all internal-consistency checks, all caveats.
4. **`MANIFEST.txt`** — reproducibility recipe (toolchain, build flags, single-command cold checkout).
5. **`HASHES.sha256`** — sha256 of every artefact in the bundle.

## What the panel does not need to read but exists for audit

- `replicate.cpp`, `replicate2` — primary primesieve C++ implementations
- `independent_sieve.c` — hand-rolled plain-C cross-check sieve
- `out.tsv`, `out2.tsv`, `indep_full.tsv`, `indep_1e11.tsv`, `m1b_indep_1e11.tsv`, `m1b_indep_full.tsv` — full residue-count and diff tables, all checkpoints
- `delegations/_charsum_full.py` — 495-cell Dirichlet character orthogonality verifier
- `delegations/_table4_diagnostic.py` — Koyama Table 4 hypothesis battery (rules out 7 alternative conventions, confirms x-label error in row 3)
- `delegations/cohere.md` — first-pass adversarial review (used to harden the report wording)
- `delegations/email_to_koyama_DRAFT.md` — outstanding-questions email to the author (DRAFT, not sent)

## Headline numbers

| Quantity | Value |
|---|---|
| pi(1.3·10^13) | 445,831,610,611 |
| Cells of Tables 3–7 reproduced exactly | 75 of 92 |
| Internal-consistency check (Dirichlet identity (3.1)) | 495/495 cells PASS, worst residual 1.4e-4 |
| Library-independence at x = 1.3·10^13 | YES (primesieve vs hand-rolled C) |
| Hardware-independence at x ≤ 1.3·10^12 | YES (M1 Max ↔ M1B, 420/420 coprime-residue cells PASS) |
| Hardware-independence at x = 1.3·10^13 | extending on M1B; not on critical path |
| Conjecture 2 dominance reproduced at x = 1.3·10^13 | N ∈ {7, 8, 19} |

## Reproduction recipe

```bash
brew install primesieve pandoc tectonic
cd koyama_replication
clang++ -O3 -std=c++17 -I/opt/homebrew/include \
        -L/opt/homebrew/lib -lprimesieve replicate.cpp -o replicate
./replicate > out.tsv 2> progress.log                  # ~70 min M1 Max core
cc -O3 -std=c99 -lm independent_sieve.c -o indep
./indep 13000000000000 > indep_full.tsv 2> indep_full.log   # ~3.7 h
python3 delegations/_charsum_full.py                   # 495-cell Dirichlet check
python3 plots/make_figure.py                           # regenerate figures
shasum -a 256 -c HASHES.sha256                         # bit-equal?
pandoc CREST_EXECUTIVE_ONEPAGE.md -o CREST_EXECUTIVE_ONEPAGE.pdf --pdf-engine=tectonic
```
