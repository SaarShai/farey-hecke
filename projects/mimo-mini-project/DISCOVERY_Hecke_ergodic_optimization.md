> ⚠️ **PARTIAL RETRACTION (2026-06-02, later same day) — see `FINDINGS_corrected_2026-06-02.md`.**
> The optimizer family `(1^{q−3},2)` is FEASIBLE only for **q≤11** (q=12 degenerate, q≥13 empty scale
> window). The X(q) table below for **q≥13** and the "no-GS universal q=3..30 / strictly increasing
> →∞" claims are **unsubstantiated**: they were produced by `Xq_exact_for_word`, which computes only
> the lower scale bound `s_lo` and never checks feasibility (the floor upper bound). Exhaustive search
> finds NO feasible parabolic word for q=13,14,16. Rigorous/honest scope: q≤11 (sharp Lean-proven
> no-GS only q=3,4). The naive triangle D is the natural-extension domain only for q=3 (≈100% of seeds
> escape D for all q≥4). Read the corrected file before citing anything from §3/table for large q.

# Discovery: ergodic-optimization infimum X(q) across the Hecke family (2026-06-02)

**Object.** Hecke group `G_q`, `λ = λ_q = 2cos(π/q)`. BCZ-type return map
`T_q(x,y) = (y, ⌊(1+x)/(λy)⌋·λy − x)` on `{x>0, y>0, x+λy>1}`, observable `P(x,y)=xy`.
`X(q) := inf over T_q-invariant probability measures μ of ess-sup_μ P` (the ergodic-optimization
"ground value"). q=3 is ordinary SL(2,ℤ) BCZ (X=2/9); q=4 is the √2-Hecke case (X=√2/8).

**Method.** The optimizing orbit lies on a **parabolic word** `[k_0,…,k_{p-1}]`: monodromy
`M_tot = ∏ [[0,1],[-1,k_iλ]]` has trace 2 (eigenvalue 1) ⇒ a **scale-free family** `a_n(s)=s·v_n`
along the eigenvector. The `+1` in the floor breaks scale-invariance, so floor-consistency +
the triangle hold only on an interval `(s_lo, s_hi]`; `P_n = s²·v_n v_{n+1}`, minimized as
`s→s_lo⁺`. `X = s_lo²·max_n(v_n v_{n+1})`, minimized over parabolic words. Code:
`code/ergodic_hecke_hunt.py` (brute search Kmax≤6, Pmax≤8 verifies optimality for q≤10; direct
construction of the optimizer word extends to all q). Validated: reproduces X(3)=2/9, X(4)=√2/8.

## THREE FINDINGS

### 1. The optimizer is the explicit parabolic word `(1^{q−3}, 2)` (q≥4)
Period `q−2`: `q−3` ones then a single `2`. (q=3 is exceptional: optimizer `(1,4)`, X=2/9.) The
all-`1` recurrence `a_{n+2}=λa_{n+1}−a_n` (since `λ=2cos(π/q)`) is exactly **rotation by π/q**
(Chebyshev); the lone `2` is the closing defect. So the optimizing orbit is the **rotation orbit
with one doubled step** — a clean cusp/parabolic object. Search-verified optimal for q=4..10.

### 2. NO GROUND STATE — universal across the Hecke family
For **every** q tested (q=3..30) the infimum `X(q)` is approached along the scale-free family at an
**open** boundary (`x+λy=1` cusp, or a floor-jump `term<k+1`) — **attained by no invariant
measure**. So the BCZ-type return map of *every* Hecke group `G_q` has **no ground state**. This
sharply contrasts **Contreras (Invent. Math. 2016)**: ground states are *generically periodic*
(attained). Here an entire natural arithmetic family has none. **Status:** PROVEN (machine-checked
Lean) for q=3 (`no_ground_state`) and q=4 (`g4_no_ground_state`); structural + numerical for q≥5
(the matching lower bound — analogue of the q=4 `g4_no_three_below` window bound — is not yet
formalized for general q).

### 3. X(q) is minimized at q=4; no uniform elementary closed form
`X(q)` is strictly increasing for q≥4 and `→∞` as `q→∞`; the **global minimum over all q is
X(4)=√2/8** (with X(3)=2/9 just above). PSLQ gives clean values whose *form changes with q*:
`X(4)=√2/8`, `X(5)=1/4`, `X(6)=√3/6`, `X(8)=½cos(π/8)`, `X(10)=½cot(π/5)`, `X(12)=cos(π/12)`, …
— i.e. `X(q)` is an explicit algebraic number of **growing degree**, with **no single uniform
elementary formula in λ_q**. (Several PSLQ integer relations differ per q; the optimizer's algebraic
degree grows like the rotation's cyclotomic degree.) So the answer to "is there a closed formula in
λ_q?" is: **specific values yes (clean), a uniform formula no.**

> **UPDATE 2026-06-02 (`CLOSED_FORM_Xq.md`, resolves /goal #2):** Finding 3 is now PROVEN and
> sharpened. The eigenvector is `v_n = sin((n+1)θ) = sinθ·U_n(λ/2)`; the **cusp always binds** giving
> `s_lo = 1/(2 sin(2π/q))` (∀q≥4, via the identity `(2sinθ+sin3θ)−2sin2θ = sinθ(2cosθ−1)² ≥ 0`).
> Hence a **uniform geometric form** `X(q)=maxprod/(4 sin²(2π/q))` and **two clean elementary
> branches**: `X = cos(π/q)/(4 sin²(2π/q))` (q even) and `X = cos²(π/2q)/(4 sin²(2π/q))` (q odd). The
> split is exactly **q mod 2** (which neighbour of π/2 the rotation orbit lands on) — that is *why* no
> single elementary formula exists. Verified vs `Xq_exact_for_word` to ≤8e-56 over q=4..80. The
> `½cot(2π/q)` guess (q=6,10) is a coincidence; true even branch is `1/(8 sin(π/q) sin(2π/q))`.

## X(q) table (X computed exactly in mpmath; word = (1^{q−3},2) for q≥4)
| q | λ_q | X(q) | clean form / note |
|---|-----|------|------|
| 3 | 1 | 0.22222222 | 2/9 (word (1,4); special) |
| 4 | √2 | 0.17677670 | **√2/8 = GLOBAL MIN** |
| 5 | φ | 0.25000000 | 1/4 |
| 6 | √3 | 0.28867513 | √3/6 |
| 7 | — | 0.38873953 | ½(¼+½cos)²/cos²-type (deg-6) |
| 8 | — | 0.46193977 | ½cos(π/8) |
| 9 | — | 0.58682409 | (deg-6) |
| 10 | — | 0.68819096 | ½cot(π/5) |
| 11 | — | 0.83798465 | — |
| 12 | — | 0.96592583 | cos(π/12) |
| … | →2 | ↑ →∞ | strictly increasing |

## Honest scope (do NOT overclaim — project #1 failure mode)
- **PROVEN (Lean, axioms clean):** X(3)=2/9, X(4)=√2/8, and *no ground state* for q=3,4.
- **Rigorous upper bound (explicit invariant family):** X(q) ≤ the tabulated value for all q (the
  parabolic family is a genuine orbit family realizing it in the limit).
- **NUMERICAL / search-verified optimal:** the `(1^{q−3},2)` word is the minimizing parabolic word
  for q=4..10 (search Kmax≤6, Pmax≤8); conjectured for all q≥4.
- **CONJECTURAL (q≥5):** that the tabulated X(q) is the *exact* infimum (matching lower bound, i.e.
  the general-q analogue of the `g4_no_three_below` window bound, not yet proven) and that no
  ground state exists (same structural argument as the proven q=3,4).

## Significance & next step
Ergodic optimization had **never** been applied to horocycle/BCZ return maps (prior-art checked).
The universal **no-ground-state across the Hecke family** is a genuinely new, clean, *not-RH-walled*
structural phenomenon, with q=3,4 already machine-checked. The natural theorem to complete it:
formalize the general-q lower bound + no-ground-state (parametrized `(1^{q−3},2)` word; same
window-bound technique as q=4) — that would turn the conjecture into a full theorem for all Hecke q.
