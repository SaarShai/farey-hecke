# Goal N — closing q≥18: the floor-1 window law + closed-form reduction (crux analysis)

**Date:** 2026-06-03. **Status:** the q≥18 gap reduced to ONE explicit inequality, with closed forms
VERIFIED and two concrete attack routes. The full uniform proof is NOT closed; the remaining step is an
explicit 1-D trig optimization (uniform) or finite 2-variable semialgebraic certs (per-q). Aristotle v10
is attempting it with these hints.

**PROVEN(Lean) / NUMERICAL(verified) / OPEN strictly separated. Nothing outward.**

## The target
`scalar_no_sustained_below` (the q≥18 closer): for `l=λ∈(1,2)`, no scalar BCZ orbit keeps every product
`c_n c_{n+1} < 1/l³`. Architecture (every link PROVEN except the kick): sub-thr orbit ⟹ not eventually
floor-1 (`infinitely_many_high_floor`, PROVEN) ⟹ floor changes ⟹ the kick clears `1/l³`. The kick bound
is the open crux. Below it is pinned to an explicit window law.

## 1. The floor-1 window law (NUMERICAL, decisive — `code/Ngoal_gbound.py`, `Ngoal_Ebound.py`)
Floor-1 run: `c_{n+2}=λc_{n+1}−c_n` from `(c0,c1)`; in-domain `= c_n>0 ∧ c_n+λc_{n+1}>1`.
- `L_max(q) = q` EXACTLY (positivity ceiling: `c_n=r cos(nθ−ψ)`, `θ=π/q`, positive for ~q steps).
- `g(L,q) := min over in-domain length-L runs of (max_{n<L} c_n c_{n+1})` is **monotone increasing** and
  **crosses `thr=1/λ³` at `L*(q)`**: `q=5,7,11,17,25 ⟹ L*=4,4,5,6,7` (max sub-thr floor-1 run `=L*−1≈q/4`).
- ⇒ **no in-domain floor-1 run of length `≥L*(q)≈q/4` stays sub-threshold.**

## 2. Closed forms (VERIFIED to 1e-12, `code` checks) — the reduction
With `c_n = r cos(nθ−ψ)` (the floor-1 rotation, `θ=π/q`, `λ=2cosθ`):
- **Product:** `p_n = c_n c_{n+1} = (r²/2)·[λ/2 + cos((2n+1)θ − 2ψ)]` — sinusoid (freq `2θ`, period `q`
  steps), mean `r²λ/4`, amplitude `r²/2`, `max_n p_n = E/(2−λ) = r²(λ+2)/4`. `r² = 4E/(4−λ²)`.
- **Domain (also one sinusoid):** `c_n+λc_{n+1} = r√(1+2λ²)·cos(nθ − ψ + δ)`,
  `δ = atan2(sin2θ, 1+2cos²θ)` (since `(1+2cos²θ)²+sin²2θ = 1+8cos²θ = 1+2λ²`).
- **Forced amplitude (VERIFIED, ratio 1.004):** length-L in-domain ⟹ all `cos(nθ−ψ+δ)>1/(r√(1+2λ²))` ⟹
  the L domain-phases (span `(L−1)θ`) fit in the cos-positive arc ⟹
  **`r ≥ r_min(L) = 1/(√(1+2λ²)·cos((L−1)θ/2))`.**
Hence `g(L,q) = min over (r,ψ) [r·D_n>1, n<L] of max_{n<L} p_n` — an EXPLICIT trig optimization. The
coupling: domain-phase `β_n=nθ−ψ+δ` centered at 0 (min r) FIXES product-phase `φ_n=2β_n+(θ−2δ)` near 0
(near the `cos=1` peak), so small r ⟹ product near peak; avoiding the peak needs larger r. The min-g
balances this 1-parameter (ψ) tradeoff. `L*(q)≈q/4` is where the balance hits `thr`.

## 3. TWO provable targets
### (a) UNIFORM (task 1) — REDUCED to an explicit 1-variable trig inequality (verified all q≥18)
The min over `(r,ψ)` is a 1-D optimization over the window-CENTER `μ` (the min-r config for each centering):
with `H=(L−1)θ/2`, `A²=1+2λ²`, `γ=θ−2δ`, the **closed-form lower bound**
```
g_closed(L,q) := min_μ  (1/(2A² cos²(|μ|+H))) · [ λ/2 + max_{0≤n<L} cos(2(μ+(n−(L−1)/2)θ) + γ) ]
```
is a **rigorous lower bound on the true `g`** (`true g ≥ g_closed`: any in-domain config has `r ≥ r_min(μ)`
and `λ/2+maxcos ≥ 0`), and **reproduces empirical `g` to ~1%** (VERIFIED q=7,17,25). Hence the uniform
target is the EXPLICIT 1-variable inequality
```
   g_closed(⌈0.28 q⌉, q) ≥ 1/λ³     for all q ≥ 18      [VERIFIED numerically q=18..80]
```
(`c=0.28`: smallest uniform constant; `0.26` fails at q=18; `0.28` is tight enough to fire — floor-1
sub-thr runs are `~q/4=0.25q`). Proving this 1-variable trig inequality (interval arithmetic / per-q /
careful analysis) closes the floor-1 window UNIFORMLY. (The cruder MEAN route `max p≥mean`,
`|Σcos|≤|sin Lθ/sinθ|`, gives a fully-elementary but WEAK constant `c=0.72` — rigorous but too weak to
fire on real `~0.3q` runs; the sharp `c=0.28` needs the `maxcos` form above.)

### (b) PER-q (task 2) — finite 2-variable certs, STAGED (extends the proven band concretely)
For each `q`, the floor-1 window lemma is a **2-variable semialgebraic emptiness**:
`¬ ∃ (c0,c1)∈ℝ²: (c0>0) ∧ (c_n+λc_{n+1}>1 ∀n<L*) ∧ (c_n c_{n+1}<1/λ³ ∀n<L*)`, where `c_n` are the
Chebyshev iterates (linear in `(c0,c1)`), `L*=L*(q)≈q/4`. This is exactly the goal-L window-lemma shape
(single floor-1 case, all `K=1`) but with the genuine window `L*(q)`; 2 variables + `~2L*` polynomial
constraints ⟹ Positivstellensatz-checkable per q. Proving it for `q=18,19,…,30` (with `L*=5..8`) extends
the machine-checked band past 17 concretely. Emitter pattern = goal-L `code/Lgoal_buildcore.py` adapted to
the floor-1 window (drop the floor-branch cases; the only case is `K=1`). STAGE for Aristotle/Lean.
⚠ This is the SCALAR floor-1 window only; the genuine q≥18 lower bound additionally needs the inter-run
chaining (the kicks = the proven `(L2)` parabolic/hyperbolic step) — but the floor-1 window is the new
piece and the dominant difficulty.

## 4. Status
- PROVEN(Lean): the architecture links (`no_infinite_rotation`, `infinitely_many_high_floor`, engine,
  `(L2)` F-family, cusp). NEW this session, all axiom-clean.
- NUMERICAL(verified): the window law (`L*≈q/4`, `L_max=q`), the closed forms (product/domain sinusoids,
  `r_min`), all to 1e-12 / 0.4%.
- OPEN: (a) the uniform trig inequality `g(⌈q/4⌉,q)≥1/λ³` (reduced to explicit 1-D calculus); (b) per-q
  certs `q=18..30` (finite, staged). Either closes the floor-1 window; plus the proven kick chaining ⇒
  q≥18 ⇒ the full theorem.

## Files
`code/Ngoal_gbound.py` (window law `g`), `code/Ngoal_Ebound.py` (`f`=min E), closed-form checks inline.
Handoff `GOAL_N_close_q18.md` (updated with the closed forms). Aristotle v10 project
`c890631c-ef4d-4f7e-8f32-5a2264e47bc5` (attempting, with these hints).

## ADDENDUM (orchestration, 2026-06-03) — 4-route results + a STATEMENT CORRECTION
Four parallel routes attacked q≥18; each independently re-verified. Net:
- **Route 1 (uniform window, VERIFIED computer-assisted):** `g_closed(⌈7q/25⌉,q)≥1/λ³` ∀q≥18 — validated
  interval arithmetic q=18..500 + analytic tail q≥23. Binding q=21 margin +4.6e-4; margin GROWS to +0.0107
  as q→∞ (not O(1/q²)-vanishing). Independently re-ran (binding q=21 confirmed). `code/Ngoal_uniform_*.py`.
  NOT Lean (interval arithmetic).
- **Route 2 (per-q Lean):** q=18 AND q=21 scalar window lemmas VERIFIED (axiom-clean, re-compiled).
  q=19,20 emits FAILED (sympy LP didn't produce a cert / killed). `lean/BCZHeckeG{18,21}_window_VERIFIED.lean`.
- **Route 3 (genuine assembly):** VERIFIED Lean but WRONG OBSERVABLE (`Pgen=a(a+λb)/λ ≥ P_actual` 100%,
  wrong direction for inf-essSup LB) ⇒ NOT a close. Salvaged `kick_pure` (verified, pure-algebra kick).
  See `FINDINGS_route3_verdict_2026-06-03.md`.
- **Route 4 (Aristotle, 9h31m):** did NOT close it. TWO outputs: (a) a VERIFIED **counterexample** —
  `scalar_no_sustained_below` as I stated it (`1<l<2`) is FALSE: l=√2 (q=4) has a 2-periodic orbit
  (`9/25, 9√2/25`), floors (1,2), all products `9√2/25·9/25 = 0.18328 < 1/l³=0.35355` (numerically
  re-verified: domain+recurrence exact). EXPECTED since `X_Ω(4)=√2/8≠1/λ³`. (b) sorry-free building blocks
  matching my closed forms — `energy_trig_form: E=r²sin²θ` (= my `r²=4E/(4−λ²)`, since `4−λ²=4sin²θ`),
  `cos/sin_chebyshev_recurrence`, `product_to_sum`, `c_at_high_floor`, `all_products_small_forces_c_bound`.

**STATEMENT CORRECTION (important):** the scalar window theorem holds for **q≥5 (l>√2)**, NOT general
`l∈(1,2)`. The q=4 (`l=√2`) counterexample uses a K=2 step — confirming the floor-1 window alone is
NECESSARY-not-SUFFICIENT: the K≥2 handling is where q=4 (value √2/8) differs from q≥5 (value 1/λ³). All
q≥18 work is in the q≥5 regime and unaffected; the dispatch statement should carry `q≥5`/`l>√2`.

**CONSOLIDATED q≥18 VERDICT:** the SCALAR/floor-1 window crux is rigorously established (route 1 uniform
computer-assisted + route 2 per-q Lean q=18,21). Genuine `X_Ω(q≥18)` still needs: (a) Lean-formalize
route 1 (the trig building blocks from Aristotle + the closed forms are the materials); (b) the K≥2-step /
multi-branch handling (where q=4 fails, q≥5 holds) assembled into genuine (C′) — the 2-branch confinement
is numeric (q≤30). Value certain. No single route closed it; the crux ingredient is now rigorous.
