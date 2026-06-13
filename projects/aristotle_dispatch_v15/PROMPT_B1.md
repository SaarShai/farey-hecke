# Aristotle Dispatch: L1b Arc-Coverage (B1) — Close windowMaxCos_lb and fcorr_lb

## Project directory
`projects/aristotle_dispatch_v15/`

## Context

We are proving **L1b_target** (skeleton in `projects/mimo-mini-project/lean/BCZHeckeGATE2_L1_skeleton.lean`):
```
∀ q : ℕ, 18 ≤ q → 0 < L_blk q → 1 / lamq q ^ 3 ≤ g_corr (L_blk q) q hL
```
where `g_corr L q = sInf (image (fcorr L q) (Ioo -(π/2-H) (π/2-H)))` and
`fcorr L q muc = (3λ/2 + √A₂ · windowMaxCos L q muc) / (2·A₂·Blam²·cos²(|muc|+H))`.

## What is already proved (0 sorry) in `L1bArcCoverage.lean`

All proved with axioms `[propext, Classical.choice, Quot.sound]` only:

1. `cos_sq_lt : Real.cos (33 * Real.pi / 512) ^ 2 < 24 / 25`
2. `H_lt_half_pi : ∀ q ≥ 18, Hq (L_blk q) q < Real.pi / 2`
3. `denom_cos_pos : ∀ {H muc}, H ∈ [0,π/2) → muc ∈ domain → 0 < cos(|muc|+H)`
4. `arc_coverage_ineq : 2 * arccos(2√6/5) / π < 33/256`

The sInf reduction `B1_target` is also proved GIVEN `fcorr_lb` (which is sorry).

## TARGET 1: `windowMaxCos_lb` (B1a)

```lean
theorem windowMaxCos_lb (q : ℕ) (hq : 18 ≤ q) (hL : 0 < L_blk q)
    {muc : ℝ} (hmuc : muc ∈ Set.Ioo (-(Real.pi / 2 - Hq (L_blk q) q)) (Real.pi / 2 - Hq (L_blk q) q)) :
    2 * Real.sqrt 6 / 5 ≤ windowMaxCos (L_blk q) q hL muc
```

where `windowMaxCos L q hL muc = Finset.sup' (Finset.range L) ... (fun n => cos(φ_n(muc)))` with
```
φ_n(muc) = 2*(muc - xiq q) + (2*n - (L-1)) * (π/q) + etaq q
```

**Proof strategy**:

Set `L = L_blk q`, `θ = π/q`, `C_D = 2√6/5`, `H = Hq L q = (L-1)*θ/2`.

**Key fact** (from `arc_coverage_ineq`): `arccos(C_D) < 33π/512 ≤ H` (since `H ≥ (ceil(33q/256)+1)*θ/2 ≥ 33π/512`).

The phases `φ_n = 2(muc - ξ) + (2n - (L-1))·θ + η` form an arithmetic progression in n with step `2θ`.
At `n = n_mid = (L-1)/2`: `φ_{n_mid} = 2(muc - ξ) + η =: φ_c`.

**Claim**: there exists `n₀ ∈ {0,...,L-1}` with `|φ_{n₀}| ≤ arccos(C_D)`, hence `cos(φ_{n₀}) ≥ C_D`.

**Sub-claim** (arc-coverage): The phases `φ_n` for `n ∈ {0,...,L-1}` cover the interval `[φ_c - (L-1)θ, φ_c + (L-1)θ]` with step `2θ`. So the closest phase to `0` satisfies:
```
|φ_{n₀} - 0| ≤ θ + |φ_c|
```
(by the floor argument: n₀ = round(−φ_c / (2θ)) + (L-1)/2).

**Bound on |φ_c|**: 
- `|muc| < π/2 - H` (from domain assumption)
- `|ξ_q| ≤ atan(λ sinθ / (3λ²+1+λcosθ)) ≤ arctan(2sinθ/(3·4-1)) ≤ arctan(sinθ/5) ≤ sinθ/5 ≤ θ/5`
- `|η_q| ≤ atan(sinθ/(3cosθ)) ≤ arctan(tanθ/3) ≤ θ/3`
- So `|φ_c| = |2(muc-ξ)+η| ≤ 2(π/2-H) + 2|ξ| + |η| ≤ π - 2H + 2θ/5 + θ/3 = π - 2H + 11θ/15`

**Condition for coverage**: We need `|φ_{n₀}| ≤ arccos(C_D)`, i.e.:
```
θ + |φ_c| ≤ arccos(C_D)  ... this is NOT generally true
```
Actually the correct statement is: since the window has total sweep `2(L-1)θ ≥ 4H - 2θ`, and the
closest phase to 0 is at distance at most `θ` from any target point in the sweep range centered at `φ_c`,
we need `|φ_c| + θ ≤ (L-1)θ = 2H - θ` (i.e. |φ_c| ≤ 2H - 2θ) AND `|φ_c| ≤ (L-1)θ - arccos(C_D)`.

**Simpler route**: For the central index `n_mid` (when L is odd, `n_mid = (L-1)/2`), we have
`φ_{n_mid} = 2(muc - ξ) + η`. For muc = 0, ξ → 0, η → 0: `φ_{n_mid} → 0`, so `cos(φ_{n_mid}) → 1 > C_D`.
For general muc in the domain, `|φ_{n_mid}|` can be as large as `π - 2H + O(θ)`. When this is large,
some OTHER index in the window brings a phase near 0. The precise argument:

The window's phase range is `[φ_c - (L-1)θ, φ_c + (L-1)θ]`. This interval has half-length `(L-1)θ ≥ 2H - θ ≥ 2·33π/512 - π/18 > 0.39 > arccos(C_D) ≈ 0.204`. So the interval always contains a point in `[-arccos(C_D), arccos(C_D)]` provided `|φ_c| ≤ (L-1)θ - arccos(C_D) + arccos(C_D) = (L-1)θ`... actually need `|φ_c| ≤ (L-1)θ`.

`|φ_c| ≤ π - 2H + 11θ/15 ≤ π - 2·33π/512 + 11π/(15·18)` for q ≥ 18.

And `(L-1)θ = 2H ≥ 2·(33π/512) = 33π/256 ≈ 0.405`. We need `|φ_c| ≤ (L-1)θ` for the interval to contain 0 in its range, but `|φ_c|` can be up to `≈ π ≈ 3.14`. 

**Correct approach**: The window covers an arc of length `(L-1)·2θ` and is periodic with period `2π`. Since `|φ_c|` may be large, but `(L-1)·2θ ≥ 4·33π/512 ≈ 0.81`, and the window step is `2θ`, the nearest phase to a target covers a `2π`-periodic arc. The claim reduces to: `(L-1)·2θ ≥ 2·arccos(C_D)`, which gives a window long enough to hit the arc `[-arccos(C_D), arccos(C_D)]` (mod 2π) once the center `φ_c` is within `(L-1)θ - arccos(C_D)` of it. But `|φ_c|` can exceed this.

**Revised claim for Lean**: The MAX cos over the window ≥ C_D follows because:
- The cosine function achieves its maximum at the phase closest to 0 (mod 2π).
- The window's phases are `φ_c + (2k-(L-1))θ` for k=0..L-1.
- There exists k such that `|(2k-(L-1))θ + φ_c| ≡ 0 (mod 2π)` to within θ.
- Sufficient: some k has `|φ_c + (2k-(L-1))θ| ≤ arccos(C_D)` (no mod needed if near 0).

For this sufficient condition: pick k₀ = round((-φ_c/(2θ)) + (L-1)/2). Then `|φ_c + (2k₀-(L-1))θ| ≤ θ`. If additionally `θ ≤ arccos(C_D)` AND `k₀ ∈ {0,...,L-1}` (i.e. `|φ_c| ≤ (L-1)θ`), we're done.

For q ≥ 18: θ = π/18 ≈ 0.175, arccos(C_D) ≈ 0.204. So θ < arccos(C_D). ✓
And `(L-1)θ ≥ 33π/256 ≈ 0.405 > θ`, but `|φ_c| ≤ π - 2H + O(θ)`. For q = 18, H ≈ 33π/512 + π/36 ≈ 0.290, so `π - 2H ≈ 2.56`. This exceeds `(L-1)θ ≈ 0.58`. So k₀ may not be in range.

**The fix**: Use the 2π periodicity of cosine. The window (L-1)·2θ = 4H ≈ 4·0.29 = 1.16 for q=18. The arc `[-arccos(C_D), arccos(C_D)]` has width 2·arccos(C_D) ≈ 0.408. Since the window covers arc 4H ≈ 1.16 > 2·arccos(C_D) ≈ 0.408, it must contain a phase in `[-arccos(C_D), arccos(C_D)]` shifted by any multiple of 2π. But φ_c mod 2π may still keep the arc out of range if the window total (1.16) < 2π - 2·arccos(C_D) ≈ 5.87. The window need not wrap around 2π.

**True key point** (from derisk analysis): The minimizer of `fcorr` is at `muc = 0`, where `windowMaxCos → 1`. The bound `windowMaxCos ≥ C_D` for ALL muc in domain is the claim. For muc near the endpoint `±(π/2-H)`, `windowMaxCos` may be smaller. The derisk shows the functional minimum is at muc=0, not at the endpoint. So the correct Lean statement is subtler: we need the min of fcorr (not max of windowMaxCos) to be ≥ 1/λ³.

**Alternative route (recommended for Aristotle)**: Skip `windowMaxCos_lb` and directly prove `fcorr_lb` by a different route:
- Show `fcorr(muc) ≥ (3λ/2 - √A₂) / (2·A₂·Blam²·cos²(|muc|+H))` using cos ≥ -1.
- Show `3λ/2 - √A₂ ≥ 0` for λ ∈ (1,2).
- This gives a weaker lower bound; but combining with the denominator bound `cos²(|muc|+H) ≤ 24/25` from `cos_sq_lt` + H ≥ 33π/512, the estimate may suffice.

Actually: `3λ/2 - √A₂ = 3λ/2 - √(1+2λ²)`. For λ = 2cos(π/q) ∈ (1,2), at q=18: λ ≈ 1.902, `3λ/2 ≈ 2.85`, `√A₂ = √(1+2·3.62) ≈ 2.84`. So `3λ/2 - √A₂ ≈ 0.01 > 0`. And 1/λ³ ≈ 0.145. The denominator `2·A₂·Blam²·cos²(|muc|+H) ≤ 2·A₂·Blam²`. At q=18: A₂ ≈ 8.24, Blam² ≈ (5/3)²-correction ≈ 2.69. So denominator ≤ 2·8.24·2.69 ≈ 44.3. LB ≈ 0.01/44.3 ≈ 0.0002 << 1/λ³ ≈ 0.145. This lower bound is too weak.

**Correct route for `fcorr_lb`**: Must use `windowMaxCos ≥ cos(0) = 1` specifically at muc = 0 and n = (L-1)/2 (i.e., the central index gives phase exactly 2(0-ξ)+η ≈ 0 for muc=0), combined with continuity. But this only works at muc=0, not uniformly.

**Honest assessment**: The uniform bound `fcorr(muc) ≥ 1/λ³` for ALL muc in domain is NOT a simple consequence of `windowMaxCos ≥ C_D`. The derisk analysis shows the minimum of fcorr occurs at muc=0 with `max_cos → 1`, not with cos = C_D. The C_D arc-coverage bound is relevant for the ENDPOINT analysis (showing the min doesn't occur at the boundary), not for the direct pointwise bound.

**Correct formulation for Aristotle**:

**TARGET**: Prove the following composite sorry-free:
```lean
theorem fcorr_lb (q : ℕ) (hq : 18 ≤ q) (hL : 0 < L_blk q)
    {muc : ℝ} (hmuc : muc ∈ Set.Ioo (...)) :
    1 / lamq q ^ 3 ≤ fcorr (L_blk q) q hL muc
```

**Approach 1 (central witness)**: Show that `windowMaxCos L q hL 0 = 1` (the central phase at muc=0 has cos=1) and extend by continuity + monotonicity of fcorr? No, fcorr is not monotone in muc.

**Approach 2 (worst-case endpoint)**: Use the H-based bound. The minimum of fcorr over muc occurs at some interior point. The analysis in `L1b_derisk_2026-06-12.md` shows:
```
min_{muc} fcorr(muc) ≥ (3λ/2 + √A₂) / (2·A₂·Blam²·cos²(H))
```
(since `windowMaxCos ≥ 1` at muc=0 with the max over n at the central index, and the denominator is bounded by its value at |muc|=0 which equals cos²(H)). Wait: at muc=0, `cos(|muc|+H) = cos(H)` and for muc ≠ 0, `cos(|muc|+H) < cos(H)` (since H is fixed and |muc|+H > H, and cos is decreasing). So the denominator INCREASES as |muc| increases. And the numerator also changes (windowMaxCos depends on muc). The minimum of `fcorr` is NOT simply at muc=0.

**From the derisk**: The minimum is numerically at muc ≈ 0, and equals ≈ `(3λ/2 + √A₂) / (2·A₂·Blam²·cos²(H))`. The reason: at muc=0 the windowMaxCos achieves its maximum (≈1 for the central phase), while the denominator achieves its minimum (cos²(H)). The ratio is maximized, making fcorr(0) close to its minimum over all muc only if the numerator decreases proportionally with denominator. The actual minimum is a saddle analysis.

**What Aristotle should do**:

Option A: Prove `windowMaxCos L q hL 0 ≥ 1` (trivial: the central phase φ_{n_mid} at muc=0 gives cos(0) = 1 when ξ=η=0, but ξ,η ≠ 0 exactly; this needs bounds on ξ,η). Then `fcorr L q hL 0 ≥ (3λ/2+√A₂) / (2·A₂·Blam²·cos²(H)) ≥ 1/λ³` where the last step uses `cos_sq_lt` and the algebra.

Option B: Prove `sInf image ≥ 1/λ³` directly via a monotone/compactness argument without going through pointwise bound.

## PROOF OBLIGATIONS (0 sorry target)

### Obligation 1: `windowMaxCos_lb` (or a substitute)

Show that for all muc in domain, `windowMaxCos (L_blk q) q hL muc ≥ C_D = 2√6/5`.

This is a Lean `Finset.sup'` lower bound. The argument:
1. `H_ge : Hq (L_blk q) q ≥ 33 * Real.pi / 512` — from `ceil(33q/256) ≥ 33q/256`
2. `arccos_CD_lt_H : Real.arccos (2 * Real.sqrt 6 / 5) < Hq (L_blk q) q` — from `arc_coverage_ineq`
3. Pick `n₀ = (L_blk q - 1) / 2` (the central index; take floor if L is even).
   The phase at muc=0, n=n₀ is `φ_{n₀}(0) = 2*(0 - xiq q) + (2*n₀ - (L-1)) * thetaq q + etaq q`.
   For large q, `xiq q → 0`, `etaq q → 0`, `2*n₀ - (L-1) → 0`, so `φ_{n₀}(0) → 0`.
   For q ≥ 18, bound `|xiq q| + |etaq q| ≤ ...` using `Complex.arg` bounds.
   Then `cos(φ_{n₀}(muc))` is estimated, and if `|φ_{n₀}(muc)| ≤ arccos(C_D)`, we have the bound.
4. If muc is near the endpoint, use a different index.

This is genuinely hard for q=18..100 and needs explicit ξ,η bounds.

**Simpler substitute obligation**: Prove `windowMaxCos L q hL 0 ≥ 1` first (i.e., at muc=0 the max cosine is 1), by showing there exists n with φ_n = 0 exactly (or approximately) using xiq, etaq bounds.

**Actually, the correct fix**: At n = n_mid = (L-1)/2, the phase is:
```
φ_{n_mid}(muc) = 2*(muc - xiq q) + (2*(L-1)/2 - (L-1)) * thetaq q + etaq q
                = 2*(muc - xiq q) + 0 + etaq q
                = 2*muc - 2*xiq q + etaq q
```
So at muc = 0: `φ_{n_mid}(0) = -2*xiq q + etaq q`. For this to give cos ≥ C_D, we need `|-2xiq q + etaq q| ≤ arccos(C_D) ≈ 0.204`.

`|xiq q| ≤ π/2`, `|etaq q| ≤ π/2`. In general for large q: `xiq q ≈ 2θ/15` and `etaq q ≈ θ/3` (from derisk), so `-2xiq + etaq ≈ -4θ/15 + θ/3 = -4θ/15 + 5θ/15 = θ/15 → 0`. For q=18: θ=π/18≈0.175, so this ≈ 0.012. But need to prove this rigorously via `Complex.arg` bounds.

### Obligation 2: `fcorr_lb`

Given `windowMaxCos_lb` (or the substitute), prove:
```
1 / lamq q ^ 3 ≤ fcorr (L_blk q) q hL muc
```

i.e. `1/λ³ * (2·A₂·Blam²·cos²(|muc|+H)) ≤ 3λ/2 + √A₂·W`

where W = windowMaxCos ≥ C_D (if using obligation 1) or W ≥ 1 at muc=0.

Substituting:
- λ = lamq q = 2cos(π/q)
- A₂ = 1 + 2λ² = 1 + 8cos²(π/q)
- Blam² = (12λ⁴+8λ²+1)/(2λ²+1)² — rational in cos(π/q)
- cos²(|muc|+H) ≤ 1 (crude), or ≤ cos²(H) ≤ 24/25 (from cos_sq_lt, H ≥ 33π/512)

Using the coarse bound W ≥ 1, cos² ≤ 24/25:
```
RHS ≥ 3λ/2 + √A₂
LHS = 1/λ³ * 2·A₂·Blam² * cos²(H)
    ≤ 1/λ³ * 2·A₂·Blam² * (24/25)
```
Need: `λ³·(3λ/2 + √A₂) ≥ 2·A₂·Blam²·(24/25)`.

With λ = 2c (c = cos(π/q)), A₂ = 1+8c², √A₂ = √(1+8c²), Blam² = (12·16c⁴+8·4c²+1)/(1+8c²)²·... wait, let me recalculate:
- λ = 2c, λ² = 4c², λ⁴ = 16c⁴
- A₂ = 1 + 2·4c² = 1+8c²
- 12λ⁴+8λ²+1 = 192c⁴+32c²+1
- (2λ²+1)² = (8c²+1)²
- Blam² = (192c⁴+32c²+1)/(8c²+1)²

Need: `8c³·(3c + √(1+8c²)) ≥ (48/25)·(1+8c²)·(192c⁴+32c²+1)/(8c²+1)²`

For q=18 (c=cos(π/18)≈0.951): 8c³≈6.89, 3c≈2.85, √(1+8·0.904)≈√8.23≈2.87. LHS≈6.89·5.72≈39.4. RHS: (48/25)·8.23·(192·0.742+32·0.904+1)/(8·0.904+1)²≈1.92·8.23·(142.6+28.9+1)/(8.23)²≈1.92·8.23·172.5/67.7≈1.92·8.23·2.55≈40.3. Hmm, LHS < RHS at q=18 with this crude bound!

So the crude bound `W ≥ 1, cos² ≤ 24/25` does NOT suffice. Need a tighter bound on cos².

Using `cos²(|muc|+H) ≤ cos²(H) ≤ 24/25` is wrong direction: `H ≥ 33π/512` implies `cos²(H) ≤ 24/25` only for the UPPER bound direction. And the minimum of fcorr requires the denominator to be bounded away from 0, not bounded above.

**Clarification**: To lower-bound fcorr, we need to lower-bound the NUMERATOR and upper-bound the DENOMINATOR:
- numerator ≥ 3λ/2 + √A₂·C_D (using W ≥ C_D)
- denominator ≤ 2·A₂·Blam²·cos²(0+H) = 2·A₂·Blam²·cos²(H) (since cos is decreasing and |muc| ≥ 0)

Wait: cos²(|muc|+H) is maximized at |muc|=0 (giving cos²(H)) and DECREASES as |muc| increases. So:
- denominator = 2·A₂·Blam²·cos²(|muc|+H) ≤ 2·A₂·Blam²·cos²(H)

Therefore: `fcorr(muc) ≥ (3λ/2 + √A₂·C_D) / (2·A₂·Blam²·cos²(H))`

And `cos²(H) ≤ 24/25` (from `cos_sq_lt` applied to H ≥ 33π/512).

So `fcorr(muc) ≥ (3λ/2 + √A₂·C_D) / (2·A₂·Blam²·(24/25)) = 25·(3λ/2 + √A₂·C_D) / (48·A₂·Blam²)`.

Need: `25·(3λ/2 + √A₂·C_D) / (48·A₂·Blam²) ≥ 1/λ³`.
i.e. `25·λ³·(3λ/2 + √A₂·C_D) ≥ 48·A₂·Blam²`.

With c=cos(π/18)≈0.951, λ=2c≈1.902, C_D=2√6/5≈0.980, √A₂≈2.87, Blam²≈2.69, A₂≈8.23:
LHS ≈ 25·6.87·(2.85+2.87·0.980) ≈ 25·6.87·(2.85+2.81) ≈ 25·6.87·5.66 ≈ 972.
RHS ≈ 48·8.23·2.69 ≈ 1063. Still LHS < RHS!

**The problem**: The bound is marginally too tight at q=18. The correct proof needs H-monotonicity and the exact series expansion, not just the worst-case H = 33π/512.

**For Aristotle, the correct path**: Use the EXACT H(q) ≥ 33π/512 + π/(2q) (from the derisk §3.i), which gives cos²(H) ≤ cos²(33π/512 + π/36) for q=18. This sharpens the bound. Then the polynomial inequality may be tractable with `nlinarith` + explicit witnesses.

OR: Accept a sorry for the finitely many q ∈ [18, N] (e.g., N=100) and close the tail q > N analytically. The derisk gives monotone convergence of the margin.

## BUILD INSTRUCTIONS

```bash
cd projects/aristotle_dispatch_v15
export PATH="$HOME/.elan/bin:$PATH"
lake build L1bArcCoverage
```

Should show: `Build completed successfully` with only the `windowMaxCos_lb` and `fcorr_lb` warnings (2 sorries), and:
```
'arc_coverage_ineq' depends on axioms: [propext, Classical.choice, Quot.sound]
'H_lt_half_pi' depends on axioms: [propext, Classical.choice, Quot.sound]
```

## WHAT TO PROVE (prioritized)

1. **MUST**: `fcorr_lb` using ANY valid path (it need not go through `windowMaxCos_lb`).
   - Best path: use the dominator bound `cos²(|muc|+H) ≤ cos²(Hq L q)` + H-lower-bound + `cos_sq_lt`.
   - Explicit polynomial inequality in `c = cos(π/q)` for `c ∈ (cos(π/18), 1)` via `nlinarith` with witnesses.
   - If only closable for q ≥ N (some N), introduce sorries for q ∈ [18, N-1] with `norm_num`.

2. **BONUS**: `windowMaxCos_lb` as a standalone lemma (useful for other applications).

3. **DO NOT** introduce new sorry beyond the 2 current ones. Use `nlinarith` with EXPLICIT hints (not `aesop`/`grind`/`simp_all` unless essential).

## REPORTING (place in this PROMPT_B1.md below, or in a new file B1_RESULT.md)

After attempting each obligation:
- Quote `lake build` tail (last 20 lines)
- Quote `#print axioms` for every theorem proved
- State exactly what remains sorry and what the precise remaining obligation is
