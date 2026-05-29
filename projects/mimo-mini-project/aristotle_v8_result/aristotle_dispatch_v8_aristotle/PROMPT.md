# Aristotle v8 — clean six-step proof of cluster_size_le_two

## Context

This is the THIRD attempt at the cluster=2 bound.

- v6 closed it via a "Key Lemma KL" detour (the 0.702-band) that turned out to be unnecessary.
- v7 used the slicker route (reviewer's proof) but the proof terms came back with broad `aesop`/`grind`/`simp_all` calls — an independent reviewer described it as "smoke in the engine room" and not Mathlib-PR-ready.

This v8 dispatch has the SAME mathematical content as v7 but encoded as **six named lemmas, one per logical step**, with the user's hand-written proof bodies already filled in where straightforward. Your job is to **fix the remaining proof details** and ensure everything compiles cleanly with NO heavy automation hiding the proof structure.

## File

`BCZClusterCleanProof.lean` (~280 lines).

## Constraints

1. **Each named lemma should compile** with mostly elementary tactics: `linarith`, `nlinarith`, `Int.le_floor`, `div_lt_iff₀`, `le_div_iff₀`, `Int.floor_eq_iff`, `mul_lt_mul'`, etc.
2. **Do NOT use broad `aesop`** in any proof unless absolutely needed; if you do, comment why.
3. **Do NOT use `grind +locals`** — this hides what's being proven.
4. **Do NOT use `simp_all +decide`** — these are too broad.
5. **Acceptable**: `simp [bczMap]` (specific lemma application), `nlinarith`, `linarith`, `norm_num`, `ring`, `push_neg`, `by_contra`, `rcases`, named lemma applications.
6. Final result: 0 sorries, only standard axioms (propext, Classical.choice, Quot.sound).
7. The proof should be visually scannable by a Mathlib referee — each step's contribution to the argument should be obvious.

## Acceptance

- Each of `step1_quadratic_squeeze`, `step2_rule_out_b_gt_two_thirds`, `step3_b_lt_one_third`, `step4_c_gt_two_thirds`, `step5_next_floor_eq_one`, `step6_third_product_nonextreme` compiles.
- `cluster_size_le_two_clean` compiles by chaining the six steps.
- The full file builds against Mathlib v4.28.0 with `lake build`.
- If any of the user's hand-written proof bodies don't quite work, fix them — but record what was changed and why.
- Report any tactics you added that go beyond the constraints above.

## If a step is genuinely stuck

Decompose further. Add a helper lemma. Don't reach for `aesop` to skip understanding.

## Mathematical hint for tricky cases

- Step 1 quadratic: `9b² − 9b + 2 = 9(b − 1/3)(b − 2/3)`. Factoring helps `nlinarith`.
- Step 2: the key nonlinear step is `4/(9b) < b ⟺ b > 2/3`. `nlinarith` with `b > 2/3` should handle it.
- Step 6: `(1-b)(1-2b) − 2/9 = (18b² − 27b + 7)/9`. At `b = 0`: 7/9 > 0. At `b = 1/3`: 0. Decreasing on (0, 1/3). So strictly positive on the open interval. `nlinarith` with `b > 0`, `b < 1/3` should close it.

## Why this matters

After this v8 lands cleanly, the trilogy of Lean files (BCZDenominatorRepulsion + BCZThresholdIntegration + this) is the Mathlib-PR-ready cluster=2 formalization. The current v6 + v7 files are kept for comparison but v8 is the canonical submission version.
