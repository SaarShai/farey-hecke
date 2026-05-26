# Summary of changes for run d5dcf7d1-fa12-48e4-a891-b19ce933150a
## Completed: MiMo Mini-Project Top 3 Discoveries

All three Lean files now compile cleanly against Lean 4.28.0 / Mathlib v4.28.0. Full details are in `ARISTOTLE_SUMMARY.md`.

### What was closed

**`BCZDenominatorRepulsion.lean` — FULLY PROVEN (0 sorries remaining)**

The main theorem `BCZ_denominator_correlation_neg_half` is now closed: under the BCZ joint density f(x,y) = 2 on the triangle {x+y > 1}, the Pearson correlation Cov(X,Y)/Var(X) = −1/2 exactly. Proof is pure arithmetic via `unfold` + `norm_num`.

**Key fix:** `bczMixedMoment` was corrected from `1/4` to `5/12` — the original value was a transcription error (the file's own derivation correctly computed E[XY] = 5/12). With 1/4, the theorem reduces to `False`.

Axiom check: `[propext, Classical.choice, Quot.sound]` ✅

### What remains RESEARCH-OPEN

**`MertensNWCorrelation.lean`** — 3 sorries remaining (all RESEARCH-OPEN/MATHLIB-PREREQ):
- `fareyAsymptote` definition (needs infinite Euler product / `tprod` API)
- `mertens_NW_pointwise_under_RH` (requires Mikolás identity + RH-conditional bounds)
- `mertens_NW_extreme_outliers` (requires Odlyzko–te Riele combination)
- Fixed: `Neg ℕ` type error in exponent, unused variable lint warning.

**`Cluster2Universality.lean`** — 6 sorries remaining (all RESEARCH-OPEN/MATHLIB-PREREQ):
- 3 definition placeholders (`fareyGap`, `isExtremeGap`, `clusterSizeAt`)
- 3 theorem sorries (cluster universality, extremal index, Wigner-Dyson)
- Fixed: parse error from orphan docstring.

### No axioms introduced. No theorems trivialized to `True`.

# ARISTOTLE_SUMMARY — MiMo Mini-Project Top 3 Discoveries

## Build Status

All three files compile cleanly against Lean 4.28.0 / Mathlib v4.28.0.

---

## File 1: `BCZDenominatorRepulsion.lean` — ✅ CLOSED

### Theorem closed

- **`BCZ_denominator_correlation_neg_half`**: Under the BCZ joint density
  f(x,y) = 2 on the triangle {x + y > 1, x,y ∈ (0,1)}, the Pearson
  correlation Cov(X,Y)/Var(X) equals exactly **−1/2**.

  Proof: pure arithmetic on the defined moment constants, closed by
  `unfold` + `norm_num`.

### Fixes applied

1. **`bczMixedMoment` corrected from `1/4` to `5/12`.**
   The original file had E[XY] = 1/4, which is incorrect. The correct
   integral ∫∫_T 2xy dx dy = 5/12 (as the file's own comment computed).
   With 1/4 the theorem statement reduces to `False`.

2. **Added `open Classical`** to resolve `Decidable` instance for
   `bczTriangle` membership in the `bczDensity` definition.

3. **Removed redundant `ring_nf`** — `norm_num` alone closes the goal
   after unfolding.

### Axiom check

```
'BCZ_denominator_correlation_neg_half' depends on axioms:
[propext, Classical.choice, Quot.sound]
```
✅ Clean — no `sorry`, no non-standard axioms.

### Remaining sorries

**None.** File is fully proven.

---

## File 2: `MertensNWCorrelation.lean` — RESEARCH-OPEN (3 sorries)

### Fixes applied

1. **Fixed `Neg ℕ` type error** in `mertens_NW_extreme_outliers`: changed
   `(Q : ℝ)^(-(1/2))` → `(Q : ℝ)^(-(1/2 : ℝ))` so the exponent is
   parsed as a real number, not as `-(Nat.div 1 2)`.

2. **Removed unused variable `h`** in `NW` definition (`if h : ...` → `if ...`).

### Remaining sorries (all RESEARCH-OPEN)

| Declaration | Annotation | Rationale |
|---|---|---|
| `fareyAsymptote` (def) | MATHLIB-PREREQ | Infinite Euler product C = (1/2)∏_p(1+1/(p²(p−1))) requires `tprod` API not in Mathlib v4.28.0 |
| `mertens_NW_pointwise_under_RH` | RESEARCH-OPEN | Full proof requires Mikolás Fourier identity, RH-conditional M(x) bound, and m≥2 fluctuation series bound |
| `mertens_NW_extreme_outliers` | RESEARCH-OPEN | Requires combining the Mertens-NW formula with Odlyzko–te Riele 1985 |

### Axiom check

All sorries are explicitly marked. No non-standard axioms introduced.

---

## File 3: `Cluster2Universality.lean` — RESEARCH-OPEN (6 sorries)

### Fixes applied

1. **Fixed parse error**: docstring `/-- Linear ordering ... -/` was not
   followed by a declaration; converted to a regular `--` comment.

### Remaining sorries (all RESEARCH-OPEN or MATHLIB-PREREQ)

| Declaration | Annotation | Rationale |
|---|---|---|
| `fareyGap` (def) | RESEARCH-OPEN | Requires sorted Farey enumeration and gap extraction |
| `isExtremeGap` (def) | RESEARCH-OPEN | Requires quantile threshold definition on Farey gaps |
| `clusterSizeAt` (def) | RESEARCH-OPEN | Requires recursive max-run-length definition |
| `cluster_size_two_universality` | RESEARCH-OPEN | Requires BCZ density theorem + extreme-value analysis |
| `farey_extremal_index_half` | RESEARCH-OPEN | Equivalent to cluster_size_two_universality |
| `farey_outside_wigner_dyson` | MATHLIB-PREREQ | Random matrix theory definitions not in Mathlib v4.28.0 |

### Axiom check

All sorries are explicitly marked. No non-standard axioms introduced.

---

## Summary Table

| File | Sorries closed | Sorries remaining | Status |
|---|---|---|---|
| `BCZDenominatorRepulsion.lean` | 1 (main theorem) | 0 | ✅ FULLY PROVEN |
| `MertensNWCorrelation.lean` | 0 | 3 | RESEARCH-OPEN |
| `Cluster2Universality.lean` | 0 | 6 | RESEARCH-OPEN |

## Statement Refinements

- **`BCZDenominatorRepulsion.lean`**: `bczMixedMoment` corrected from 1/4 to 5/12
  (the original value was a transcription error; the file's own derivation computed 5/12).
- **`MertensNWCorrelation.lean`**: exponent annotation `-(1/2 : ℝ)` added for type correctness.
- **`Cluster2Universality.lean`**: no mathematical changes; only syntactic fix (docstring → comment).

No axioms were introduced. No theorems were trivialized to `True`.
