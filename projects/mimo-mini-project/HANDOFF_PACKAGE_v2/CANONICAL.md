# HANDOFF_PACKAGE_v2 — Canonical Shipped Artifact

**Status**: This package is the canonical, locally-verified Lean 4 corpus for the
BCZ cluster=2 / sharpness result and the supporting moment and threshold lemmas.

**Build verification**: All four `.lean` files in `lean/` compile under
Mathlib v4.28.0 with `import Mathlib` (broad import). They are reused verbatim
in the buildable sibling project at `../mathlib_pr_v3/` (which has the same
files + a working `lakefile.toml`). The 2026-05-27 local `lake build` against
Mathlib v4.28.0 succeeds with **0 sorries** and uses no broad automation
(`aesop`, `grind`, `simp_all +decide` are absent by design).

## Files (lean/)

| File | Lines | Role |
|------|-------|------|
| `BCZDenominatorRepulsion.lean` | 437 | Moment bounds for BCZ denominator (v4) |
| `BCZThresholdIntegration.lean` | 252 | Closed-form q*_BCZ via integral split (v5) |
| `BCZClusterCleanProof.lean`     | 216 | cluster_size_le_two for t ≤ 2/9 (v8, reviewer's clean six-step) |
| `BCZSharpness.lean`             | 132 | For t > 2/9, 2-cycle gives arbitrarily long extreme runs (v9) |

Together these establish the **sharp phase transition at t = 2/9**:
- v8 gives the upper bound (cluster ≤ 2 for t ≤ 2/9)
- v9 gives the matching lower bound (arbitrarily long extreme runs for t > 2/9)
- v5 closes the closed-form constant q*_BCZ = (11 − 8 ln(3/2))/9
- v4 supplies the moment lemmas used by v5

## Relation to mathlib_pr_v3/

`../mathlib_pr_v3/` is the **buildable** sibling: same `.lean` content, working
`lakefile.toml`, `lean-toolchain` v4.28.0-pinned, cached Mathlib build under
`.lake/`. To rebuild from scratch:

```
cd ../mathlib_pr_v3
export PATH=~/.elan/bin:$PATH
lake update      # one-time, ~5–15 min
lake build       # ~3–8 min
```

## Relation to mathlib_pr_minimal_broken/

`../mathlib_pr_minimal_broken/` is an aspirational "minimal-imports" repackage
of the same proofs aimed at PR-readiness (replacing `import Mathlib` with
targeted Mathlib imports). As of 2026-05-27 it has three residual errors
(bad import, lemma-name typo, three unsolved Integrable goals at L107/194/221
of the threshold file). A fix-it pass is in progress; see that directory's
notes for status. It is NOT canonical and should not be cited.

## Round-2 reviewer corrections incorporated

- Mellin denominator: `w(2-w)` not `w(3-w)` (sign-convention bug from round 1)
- Framing: "high-contrast empirical diagnostic", not "binary classifier"
- "16-digit agreement between algorithms", not "16 digits of constant"
- AC2014 elliptic/parabolic/hyperbolic classification acknowledged as prior art
- Cobeli-Zaharescu 2015 §4–5 cited for the run-length lemmas in our framework

## Citation

Saar Shai (2026). Cluster=2 universality and sharp phase transition at t = 2/9
for the Boca–Cobeli–Zaharescu chain. Formal Lean proof, Mathlib v4.28.0.
