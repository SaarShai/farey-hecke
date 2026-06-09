# Aristotle v12 — `cluster_size_le_two_q6`: BCZ cluster ≤ 2 for the Hecke group G_6

## Goal

Make `BCZ6Cluster.lean` compile (`lake build`, Mathlib **v4.28.0**), **0 sorry**,
`#print axioms cluster_size_le_two_q6` = `[propext, Classical.choice, Quot.sound]`.

This is the **third arithmetic Hecke case** (q∈{3,4,6}; λ₆=√3, X(6)=√3/9=1/λ³), after
the proved q=3 (v8) and q=4 (v11). The theorem: along the Taha G_6-BCZ orbit, three
consecutive points cannot all have the ergodic-opt observable `P < √3/9`.

**The mathematics is fully worked out and verified numerically** (code/goal1_q6_*.py:
`max_run=2`, `third_extreme_in_T5=0`, every lemma margin computed). The file contains
the complete proof skeleton. q=6 does NOT reduce to the clean q=4 case-analysis, so
two steps are genuine polynomial certificates flagged below — your job is to find them.

## Structure (do not change the statement, defs, domain T6, map bczMap6, or observable Pobs)

* `s3 = √3`, `s3*s3 = 3`. `dᵢ` = the Taha dot-products (see header).
* Branches T₂..T₅ by the first `dᵢ ≤ 1`; T₅ (`d₄=a+√3b>1`) is the last branch, where
  `P=ab` and the map is `(b, −a+k√3b)`.
* `lemA2`, `lemA3` — T₂/T₃ non-extreme. **Clean** (`(1−a)(1−dᵢ)≥0` plus the linear
  identities `a+d₂=√3 d₁`, `a+d₃=(√3−1)(d₁+d₂)`). The `nlinarith` calls should work or
  need only minor hint tweaks.
* `lemA4` — **T₄ non-extreme, TIGHT** (`a·d₄ ≥ 1/3`, equality at the corner (1/√3,0),
  numeric min margin +4e-5). I provide the **exact ring identity** `hid`
  (`a·d₄ − 1/3 = ⅓(d₁−1) + ⅓(d₃−1) + (a−√3/3)(d₄−√3/3)`, proved by `linear_combination`).
  The remaining `nlinarith` must show this is ≥0: the first two terms are ≥0 (d₁,d₃>1),
  and the cross term (which can be negative) is dominated. **FIND THIS CERTIFICATE**
  (higher-degree `nlinarith`, `polyrith`, or a helper lemma / case split on `s3*a ≷ 1`).
* `nonextreme_off_T5`, `extreme_imp_T5` — branch case-split; should be fine.
* Main theorem: `xᵢ,xᵢ₊₁ ∈ T₅`; `a+c=k√3b`; third point `(c,d)`, `d=−b+ℓ√3c`.
  Split on whether `(c,d) ∈ T₅`:
  - `∉ T₅`: `nonextreme_off_T5` (done).
  - `∈ T₅`: need `cd ≥ √3/9`. Split on `k`:
    - **`k ≥ 3`: CLEAN** (provided): `kb²<2/9 ⇒ b²<2/27 ⇒ c>1−√3b>√2/3 ⇒ c²>2/9 ⇒
      cd ≥ √3c²−bc > 2X−X = X`. These `nlinarith` calls should work.
    - **`k ∈ {1,2}`: HARD** (`interval_cases k`). This is the coupled certificate using
      `ab<X`, `bc<X`, `a+c=k√3b`, the three T₅ conditions, `d=−b+ℓ√3c`, `ℓ≥1`. Numeric
      min `cd−X = +0.028` (NOT tangent — there is room). **FIND THIS** (you may split
      further on `ℓ`, `push_cast` the integer `k`, and add hint products). The reduced
      lemma WITHOUT `ab<X` is false, so `ab<X` and `hsum` (a+c=k√3b) are essential.

## What likely needs fixing besides the two hard certificates

* `set`-fold / projection rewrites (`hmapi`, `hmapi1`, `hb_eq1`, `hc_eq2`, `hd_eq`) —
  same pattern as v11; trim/append `simp only [Prod.fst,Prod.snd]` as needed.
* Mathlib v4.28.0 name drift: `Real.mul_self_sqrt`, `le_div_iff₀`, `div_le_div_iff`,
  `lt_of_mul_lt_mul_left`, `Int.floor_nonneg`, `interval_cases`, `linear_combination`.
* `push_cast` / `norm_num` after `interval_cases k` to turn `((1:ℤ):ℝ)` into `1` in `hsum`.

## Constraints

* 0 `sorry`; standard axioms only. Keep `lemA2/lemA3/nonextreme/extreme/main`-plumbing
  transparent (`linarith`/`nlinarith`/`rw`/`rcases`/`omega`). For the **two flagged hard
  certificates** (`lemA4`, the `k∈{1,2}` closing) a `nlinarith`/`polyrith` certificate or
  helper lemmas are fine — but NOT `sorry`. Avoid `aesop`/`grind`/`simp_all` elsewhere.
* Do not weaken the theorem, the domain, the map, or the observable.

## Report

List all changes, the certificates you found for the two hard lemmas (and the tactic
used), and paste `#print axioms cluster_size_le_two_q6`.
