# Aristotle v7 — Reviewer's slicker proof of cluster_size_le_two

## Context

A previous Aristotle dispatch (v6, project 493c17d4) closed `cluster_size_le_two`
via a route that needed the KL band condition `y > 2/3` and a sub-case on `y < 1/3`.

An independent reviewer proposed a cleaner proof that **eliminates the `y > 2/3` branch
immediately** via the integer recurrence `a + c = k·b ≥ b` (where k = ⌊(1+a)/b⌋ ≥ 1).

The two arguments yield the same theorem; the reviewer's is structurally simpler.

## Targets

Close the sorries in `BCZClusterReviewerProof.lean` in order:

1. **`bcz_sum_eq_k_mul_b`** — `(bczMap (x,y)).2 + x = k·y` where `k = ⌊(1+x)/y⌋`.
   - This is immediate from `bczMap`'s definition; should close in 1-2 lines.

2. **`bcz_b_gt_two_thirds_impossible`** — the key new step. If `xy < 2/9` and
   `y·(bczMap(x,y)).2 < 2/9` and `y > 2/3`, derive a contradiction:
   - From `xy < 2/9` and `y > 2/3`: `x < 2/(9y)`.
   - From `y·(bczMap(x,y)).2 < 2/9` and `y > 2/3`: `(bczMap(x,y)).2 < 2/(9y)`.
   - Sum: `x + (bczMap(x,y)).2 < 4/(9y) < y` (since `4/(9y) < y ⟺ y² > 4/9 ⟺ y > 2/3`).
   - But `(bczMap(x,y)).2 + x = ⌊(1+x)/y⌋ · y ≥ y` (since floor ≥ 1).
   - Contradiction.
   - Should be closeable with `nlinarith` + the floor-ge-1 fact + `bcz_sum_eq_k_mul_b`.

3. **`bcz_b_lt_one_third`** — combine the quadratic squeeze `y < 1/3 ∨ y > 2/3`
   with the previous lemma to conclude `y < 1/3`. The squeeze itself is `nlinarith`
   given `xy < 2/9` and `x + y > 1` and `0 < x, y < 1`.

4. **`bcz_c_gt_two_thirds`** — `c = (bczMap (x,y)).2 > 1 - y > 2/3` since `y < 1/3` and
   triangle gives `y + c > 1` for `(y, c) = (bczMap (x,y)).{1,2}` being in the triangle.

5. **`bcz_second_floor_eq_one`** — `(1+y)/c < 2` since `(1+y)/c < (4/3)/(2/3) = 2`.

6. **`bcz_third_pair_nonextreme`** — `c(c-b) > (1-b)(1-2b)` (since `c > 1-b` and
   `c-b > 1-2b`), and `(1-b)(1-2b) > 2/9` for `b < 1/3` (algebra: `9(1-b)(1-2b) = 9 - 27b + 18b² > 2`
   ⟺ `18b² - 27b + 7 > 0`; at `b=0`: 7>0, at `b=1/3`: 18/9-9+7=0, so > 0 for b<1/3).

7. **`cluster_size_le_two_slicker`** — combine.

## Constraints

- 0 sorries, only standard axioms.
- If the reviewer's path turns out to need additional steps, document what was found.
- Acceptance: equivalent theorem `cluster_size_le_two_slicker` proven without the
  KL_strengthened intermediate.

## Comparison goal

Whichever proof (v6 or v7) is shorter / uses simpler tactics is the preferred
version for the Mathlib PR.
