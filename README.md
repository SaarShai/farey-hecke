# farey-hecke

Consolidated mathematics-research repo (private). Combines:

- **All of "Farey NOW"** — the active project, including the live Hecke
  ergodic-optimization work, the −1-dominance track, the Farey/Stern-Brocot
  Lean library, and the MiMo certs.
- **The curated, still-valid material from `Primes-Equispaced`** — under
  [`equispaced-primes/`](equispaced-primes/) (Lean formal-conjectures, Koyama
  collaboration, shippable papers, function-field D3, BCZ-cocycle D1, DPAC).
  See its [curation note](equispaced-primes/README.md) for what was kept vs cut
  and the dead-claim / corrected-citation warnings.
- **All previously-uncommitted / unpushed work** at the time of consolidation
  (2026-06-04).

The unpruned `Primes-Equispaced` archive still lives at
`github.com/SaarShai/Primes-Equispaced`.

## Branches

| Branch | What it is |
|---|---|
| `main` | Consolidated base: Farey NOW + curated `equispaced-primes/`. |
| `hecke-goalL-2026-06-03` | **The Hecke progress branch.** All Hecke goal work (goals L, M, N, O, GATE 2) on top of `main`, plus the uncommitted working-tree changes captured at consolidation. This is the active head. |

`hecke-goalL-2026-06-03` is a superset of `main`.

## The Hecke headline (honest status)

Hecke–BCZ ergodic optimization: the min-max (essential-sup) value of the BCZ
return-time product over the Hecke triangle is

```
X_Ω(q) = 1/λ³   for q ≥ 5   (λ = 2cos(π/q); attained at the cusp, no global section)
X_Ω(3) = 2/9,   X_Ω(4) = √2/8
```

Honest band:

- **Fully machine-proven (Lean, axiom-clean): q = 3..15.** Scalar window lemmas
  q = 7..16 are machine-verified; the scalar reduction holds q = 5..15.
- **q ≥ 16/17: value SURVIVES numerically** — true-map escape confirms no invariant
  sub-1/λ³ set for q ≤ 70, value adversarially safe to q ≤ 200 — but the **uniform
  proof is OPEN**: it reduces to (L1) a quantitative O(1/q²) escape-margin / window
  law and (L2) no-regime-chaining (the composite-trace law is proven all-q). The
  corridor set is the `(2,q,∞)` elliptic torsion; KAM-type obstruction to a clean
  classification.

Live work and findings: [`projects/mimo-mini-project/`](projects/mimo-mini-project)
(see the `FINDINGS_goal*` and `CLOSED_FORM_Xq.md` files). Lean certs:
`projects/mimo-mini-project/lean/` and the `lean/BCZHecke*` files.

> **Verify before trusting any `*_VERIFIED` filename.** Re-compile the Lean yourself
> (EXIT 0 + axioms `{propext, Classical.choice, Quot.sound}`, no `sorryAx`). The
> filenames are aspirational.

## What's where

```
.
├── projects/mimo-mini-project/   # LIVE Hecke ergodic-optimization work + Lean certs
├── projects/minus1-dominance/    # −1-dominance track (LEDGER, curve_3e14.tsv)
├── projects/farey-lean/          # Farey/Stern-Brocot Lean library
├── equispaced-primes/            # curated equispaced-primes lineage (see its README)
├── code/, figures/, research_notes/, cluster_universality_test/, koyama_replication_bundle/
└── (Token Economy tooling: skills/, hooks/, adapters/, te, token-economy.yaml, README_token_economy.md)
```

## Notes

- **Token Economy** (`te`, `token-economy.yaml`, `skills/`, `hooks/`, `adapters/`,
  `README_token_economy.md`) is **local tooling only** — context/cost management. It is
  not the subject of the research.
- This repo lives under `~/Documents` (Google-Drive synced). `.lake` build artifacts are
  gitignored; regenerate with `lake exe cache get` before building Lean.
- Provenance: the consolidation source (Farey NOW's relocated git history) is kept as the
  git remote `local-source`.
