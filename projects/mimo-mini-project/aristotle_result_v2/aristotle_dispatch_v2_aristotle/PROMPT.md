# Aristotle Dispatch v2 — MiMo mini-project follow-up

Context: this is a follow-up to project `56972ade-8666-4b74-8a51-b7bdda84f78a`,
where Aristotle proved `BCZ_denominator_correlation_neg_half` (0 sorries) and
honestly annotated 9 RESEARCH-OPEN sorries in two other files.

This dispatch contains three new files:

1. **`BCZExtended.lean`** — extended BCZ moments + variances + sum/difference
   identities. All theorems should be CLOSEABLE by `unfold` + `norm_num` since
   they're pure arithmetic from the defined moments.

2. **`BCZChainAntiClustering.lean`** — the discrete BCZ Stern-Brocot recursion
   b_{i+2} = ⌊(b_i + N)/b_{i+1}⌋ · b_{i+1} − b_i and the key Lemma stating that
   small b_{i+1} forces large b_{i+2}. This is the central step in proving
   cluster-size ≥ 3 impossibility at fixed quantile q < 1. The full lemma
   needs Farey-neighbor coprimality; a weaker version is provable from
   integer-division arithmetic alone.

3. **`MikolasDoubleSum.lean`** — the structural decomposition
   J(Q) = (1/12) Σ_{d,d'} gcd(d,d')² M(Q/d) M(Q/d') / (d d').
   The "easy" cases (S_Q(1) = M(Q), S_Q(2) = M(Q) + 2M(Q/2)) should be
   provable; the Mikolás identity itself is RESEARCH-OPEN.

## Honesty discipline (same as v1)

- **NO** `axiom` declarations introducing new mathematical content
- **NO** trivializing theorems with `True` or `decide` on a degenerate statement
- **YES** annotate every remaining `sorry` with `-- RESEARCH-OPEN` or `-- MATHLIB-PREREQ`
- **YES** preserve the empirical evidence comments in each file

## Expected outcome

- `BCZExtended.lean`: **all theorems should be FULLY PROVEN** by `unfold +
  norm_num`. If any fail, that means I made an arithmetic error.
- `BCZChainAntiClustering.lean`: `bcz_next_lower_bound` should close via
  `Nat.div_mul_le_self` or equivalent. The main `bcz_anti_clustering` likely
  remains RESEARCH-OPEN without Farey-neighbor structure.
- `MikolasDoubleSum.lean`: `S_Q_one` should close. `S_Q_two` and `S_Q_prime`
  may close with `Finset.divisors` manipulation. The Fourier-side identity
  and double-sum identity are RESEARCH-OPEN.

## What to verify

- Lean 4.28.0 / Mathlib v4.28.0 compatibility
- No `sorry` introduced beyond what's annotated
- No axioms beyond `[propext, Classical.choice, Quot.sound]`
