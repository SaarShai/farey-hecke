# General-q lower bound & no-ground-state — strategy + partial progress (2026-06-02, goal #1)

Status: **PARTIAL.** What is rigorous, what is sketched, what is open. Companion to
`../FINDINGS_corrected_2026-06-02.md` (the feasibility correction) and `HeckeGeneralLB_VERIFIED.lean`
(the machine-checked uniform lower bound).

## 0. Reduction (rigorous, all q)
The whole no-GS theorem reduces to ONE lemma plus an easy upper bound:
- **(C) upper bound** (easy, q≤11): the family `c_n(R)=R sin((n+1)π/q)` is a genuine orbit in D for
  `R∈(R_lo,R_hi]`; its periodic-orbit measure has `essSup P = R²m(q) → V(q)` as `R→R_lo⁺`, not
  attained (open bound). ⇒ `X(q) ≤ V(q)`, unattained.
- **(B-strong) lower bound** (the crux): *no orbit in D has `c_n c_{n+1} ≤ V(q)` for all n.*
  ⇒ every orbit has `sup_n P_n > V(q)` ⇒ `X(q) ≥ V(q)` AND not attained. Together with (C):
  `X(q)=V(q)`, no ground state.
PROVEN (Lean): (B-strong) for q=3 (`exists_product_gt_two_ninths`) and q=4 (`g4_no_sustained`).

## 1. Engine (rigorous, all q) — `HeckeGeneralLB_VERIFIED.lean`
`P_n + P_{n+1} = K_n·λ·c_{n+1}²`, `K_n=⌊(1+c_n)/(λc_{n+1})⌋ ≥ 1`. Immediate consequences:
- coords bounded: if all `P_n ≤ B` then `c_{n+1}² ≤ 2B/λ`;
- with the domain `c_n+λc_{n+1}>1` ⇒ **uniform positive ground value `X(q) ≥ λ/(2(1+λ)²) > 0`**
  (machine-checked `hecke_ground_value_pos`). Not sharp, but holds for ALL q with no case split.
- rotation invariant `E=c_n²+c_{n+1}²−λc_nc_{n+1}` preserved on floor-1 steps (`E_conserved_floor_one`);
  `=R²sin²(π/q)` on the optimizer; `max product on ellipse E = E/(2−λ)`.

## 2. Why the sharp lower bound is q-specific (the three regimes)
Max product on the cusp line `x+λy=1` is `1/(4λ)`. The set `{x+λy>1, xy≤V}`:
- **q=3** `V=2/9 < 1/(4λ)=1/4`: two disjoint lobes (`a<1/3` or `a>2/3`). The clean 2-case proof.
- **q=4** `V=√2/8 = 1/(4λ)`: hyperbola tangent to line (double root) → the hard "Middle" case
  (floor 1 forced, then next floor forced =3). 4 cases.
- **q≥5** `V(q) > 1/(4λ)`: region **connected** — one-step geometry never forces the product up; the
  bound must use ≥2 dynamical steps. No single argument covers all three regimes ⇒ per-q case analysis.

## 3. Conceptual route to the SHARP bound (sketch, not yet rigorous)
Two-step "rotation-sweep + spike" dichotomy for an orbit with all `P_n ≤ V`:
1. coords bounded by `C=√(2V/λ)` (§1).
2. On any maximal floor-1 run, the pair rotates by π/q on a fixed ellipse `E*`; `P_n` is sinusoidal
   in the rotation angle with max `E*/(2−λ)`. A run of length `≳ q` samples near that max, forcing
   `sup P ≥ E*/(2−λ)`; the domain `c+λc'>1` lower-bounds `E*`. (Need: a clean lower bound on `E*`
   from the domain, and that the run is long enough — the gap.)
3. If instead a floor `K≥2` occurs, `P_n+P_{n+1}=Kλc_{n+1}² ≥ 2λc_{n+1}²` spikes the product.
Either branch should yield `sup P ≥ V(q)`; making the constants meet `V(q)=R_lo²m(q)` exactly is the
open work.

## 4. Worked partial: q=5 t-point band-narrowing (toward a q=5 Lean proof)
λ=φ (`φ²=φ+1`), `V=1/4`, optimizer `(1,1,2)` orbit `(a,b,b)=(R sin36°,R sin72°,R sin72°)`; at `R_lo`
the max-product pair is `(b,b)=(½,½)` (product ¼) on `∂D`. For a t-point `(x,y)`, `xy=¼`, all `P≤¼`:
- §1 bounds: `x,y ≤ √(1/(2λ)) ≈ 0.556`, and `xy=¼` ⇒ `x,y ∈ [0.4498, 0.5559]` (narrow band).
- forward floor `K_m≥2` ⇒ `P_{m+1}=K_mλy²−¼ ≥ 2λ·0.4498²−¼ ≈ 0.405 > ¼`. ✗ ⇒ **floor =1**.
- floor 1 ⇒ `c_{m+2}=λy−x ∈ [0.171,0.450]`; the next ratio `(1+y)/(λc_{m+2})` is `≈1.99–5.4`.
  When `c_{m+2}` near its max and `y` near `0.45`, the ratio dips just below 2 ⇒ a genuine **Middle**
  sub-case (like q=4) where the next floor is forced (here =2) by the tight φ-bounds, then `P_{m+2}>¼`.
This mirrors the q=4 structure (Case A / A′ / Middle), with φ-arithmetic (`φ²=φ+1`) in place of `s²=2`.
Formalizable by the `g4` template; **not yet done** (≈1000-line effort, one Middle case).

## 5. Honest status ledger
- **rigorous, all q:** reduction (§0), engine + uniform `X(q) ≥ λ/(2(1+λ)²)` (Lean), E-invariant (Lean),
  upper bound `X(q) ≤ V(q)` q≤11, regime classification.
- **PROVEN sharp + no-GS (Lean):** q=3, q=4.
- **numerical:** sharp `X(q)=V(q)` q=5..11.
- **open:** sharp lower bound for q=5..11 (paper route §3/§4 incomplete); the conceptual all-q proof
  (§3 gap); and the entire large-q regime q≥12 (model invalid as posed — different natural-extension
  domain for non-arithmetic q).
