# L1b Formalization Status — 2026-06-13

## What was done

Proved the trig-inequality core of L1b in Lean (Mathlib v4.28.0), and assessed
the full remaining gap between that result and the L1b_target sorry in the skeleton file.

---

## Decomposition of L1b_target

**L1b_target** (skeleton file `projects/mimo-mini-project/lean/BCZHeckeGATE2_L1_skeleton.lean`):

```lean
∀ q : ℕ, 18 ≤ q → 0 < L_blk q →
  1 / lamq q ^ 3 ≤ g_corr (L_blk q) q (...)
```

where `g_corr L q = sInf (image (fcorr L q) (Ioo -(π/2 - H) (π/2 - H)))`.

The proof decomposes into three independent sub-obligations:

---

### (A) Trig inequality — cos²(33π/512) < 24/25  
**Status: PROVED in Lean, 0 sorry, axioms clean.**

File: `projects/aristotle_dispatch_v15/L1bTrigCore.lean`  
Theorem: `L1bTrig.cos_sq_lt : Real.cos (33 * Real.pi / 512) ^ 2 < 24 / 25`

lake build tail:
```
✓ [8027/8027] Building L1bTrigCore
info: L1bTrigCore.lean:109:0: cos_sq_lt : cos (33 * π / 512) ^ 2 < 24 / 25
info: L1bTrigCore.lean:110:0: 'L1bTrig.cos_sq_lt' depends on axioms:
      [propext, Classical.choice, Quot.sound]
Build completed successfully (8027 jobs).
```

Proof route:
1. Pi bounds (`Real.pi_gt_d4`, `Real.pi_lt_d4`) → x = 33π/512 ∈ (0.20248, 0.20249)
2. `Real.cos_bound` (|x| ≤ 1) → `cos x ≤ 1 - x²/2 + x⁴·(5/96)`
3. Set `a = x²` (a ∈ [a_lo, a_hi] = [42989460921/1048576000000, 16793827281/409600000000])
4. `24/25 - (1 - a/2 + a²·5/96)² > 0` by `nlinarith` with bounds on `a` (margin ≈ 0.000406).

Numerical margin: `24/25 - cos²(33π/512) = 4.43e-4`. The Taylor upper bound
`1 - x²/2 + x⁴·(5/96)` has margin ≈ 0.0102 away from the threshold.

**This is a pure ATP result (no sorry, no Aristotle needed).**

---

### (B) Uniform margin / 1-D calculus bound: g_corr(L_blk q, q) ≥ 1/λ³ for all q ≥ 18  
**Status: UNFORMALIZED. The central remaining gap.**

This requires two Lean steps that do not yet exist:

**B1 (analytic-functional, harder):** Show that the `sInf` of `fcorr` over the open
domain interval is bounded below by a tractable expression. Concretely: show that for
all `μc ∈ (-(π/2 - H), π/2 - H)`:

```
fcorr(μc) = (3λ/2 + √A₂ · windowMaxCos(μc)) / (2·A₂·Blam²·cos²(|μc| + H))
           ≥ 1/λ³
```

This is an inequality about a continuous function on a compact (closure of an) interval.
The derisk analysis shows the minimum is at μc = 0 with `max_cos → 1`, but
**no Lean lemma currently connects `g_corr` to any pointwise lower bound.**

The obstacle: `windowMaxCos` is a `Finset.sup'` over trig expressions; its lower bound
requires that at least one `n` in `0..L-1` gives a cosine value ≥ `C_D = 2√6/5`.
This is a Lean argument about the cosine's range over the window, i.e., an arc-coverage
lemma: "the L-block window always covers an arc containing the point where cos ≥ C_D".
This arc-coverage step is entirely absent from the current Lean codebase.

**B2 (arithmetic, partially addressed by (A)):** Once B1 is established (i.e., once
we have a clean lower bound `LB(q)` for `g_corr(L_blk q, q)`), show `LB(q) ≥ 1/λ³` for
each `q ≥ 18`. The limiting argument uses:

- H(q) = (L_blk q - 1)·π/(2q) ≥ 33π/512 + π/(2q) [from `ceil(33q/256) ≥ 33q/256`]
- F(H) = 3/(25·cos²(H)) is increasing → F(H(q)) ≥ F(33π/512 + π/(2q))
- F(H_inf) = 3/(25·cos²(33π/512)) > 1/8 [follows directly from (A)]
- But `1/λ³ > 1/8` for finite q (approaches 1/8 from above), so the comparison
  F(H(q)) ≥ 1/λ³ still requires showing the O(1/q) increment in H more than offsets
  the O(1/q²) excess of 1/λ³ over 1/8.

This is a finite-q argument that is NOT closed by (A) alone. The exact identity
`δ_inf = F(H_inf) - 1/8 = 3/(25·cos²(33π/512)) - 1/8 = 5.77e-5 > 0` (which
requires (A)) is one piece; proving F(H(q)) ≥ 1/λ³ for each finite q additionally
requires a precise expansion of both sides in 1/q. Lean tools available: `nlinarith`
with explicit coefficients, `Real.cos_bound`, `pi` bounds.

---

### (C) Finite range q = 18..N (interval certification)  
**Status: UNFORMALIZED. Possible via decidability / norm_num for small q.**

The interval certification paper (`GATE2_L1b_arcwidth_interval.py`) verifies
`g_corr(L_blk q, q) ≥ 1/λ³` for q = 18..10000 via 40-decimal interval arithmetic.

In Lean, covering q = 18..17 (to reduce to q ≥ 18 where the tail argument applies)
is feasible via `decide` or `native_decide` if `g_corr` is computable — but `g_corr`
is `noncomputable` (uses `sInf` on reals). So the finite range requires the same
analytic argument as (B), applied per-q with explicit numerical witnesses, which is
essentially the same difficulty.

A more tractable route: accept a sorry for finitely many q (e.g., 18..100) dispatched
to Aristotle with interval-arithmetic witnesses, then close the tail analytically.

---

## Is L1b_target gated ONLY on (A) + monotonicity?

**No.** The central gap is B1: the pointwise bound on `fcorr` for ALL `μc` in the
domain, connecting `g_corr` (an `sInf`) to the limiting value `F(H_inf)`. This is
a real-analysis step about the arc-width of the cosine window, not reducible to the
trig inequality alone.

More precisely:
- (A) [cos_sq_lt] proves `F(H_inf) > 1/8`, which is the limiting margin.
- B1 requires showing the min of `fcorr` over the μc domain equals/approaches `F(H_inf)`,
  which needs the arc-coverage argument (that `windowMaxCos(μc) ≥ C_D` for μc near 0,
  equivalently that L_blk is large enough to contain an arc of width > 2·arccos(C_D)/2).
- The arc-coverage step ALSO uses (A) — it reduces to `cos(33π/512) < C_D = 2√6/5`,
  which is exactly `cos²(33π/512) < 24/25 = C_D²`. So (A) is the UNIQUE algebraic
  core, but it does not by itself close the functional analysis gap.

---

## Summary table

| Component | Status | Lean artifact |
|-----------|--------|---------------|
| (A) cos²(33π/512) < 24/25 | **PROVED (0 sorry)** | `L1bTrig.cos_sq_lt` in `aristotle_dispatch_v15/L1bTrigCore.lean` |
| (B1) pointwise fcorr ≥ lb for all μc | **UNFORMALIZED** | No Lean lemma; needs arc-coverage argument for `windowMaxCos` |
| (B2) F(H(q)) ≥ 1/λ³ for each q ≥ 18 | **UNFORMALIZED** | Needs O(1/q) vs O(1/q²) expansion in Lean; uses (A) |
| (C) q = 18..finite interval | **UNFORMALIZED** | Requires same analytic steps as (B), per-q |

The single remaining algebraic fact (A) is machine-verified. The main obstruction to
closing L1b_target is B1: the arc-coverage / pointwise-fcorr lower bound, which is a
Lean real-analysis argument not yet present in the codebase.

---

## Files

- `projects/aristotle_dispatch_v15/L1bTrigCore.lean` — proved `cos_sq_lt`, 0 sorry
- `projects/aristotle_dispatch_v15/lakefile.toml`, `lean-toolchain` (v4.28.0)
- `research_notes/L1b_derisk_2026-06-12.md` — full asymptotic analysis
- `projects/mimo-mini-project/lean/BCZHeckeGATE2_L1_skeleton.lean` — the `L1b_target` sorry
