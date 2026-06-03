# Hecke BCZ ergodic-optimization — consolidated frontier status (2026-06-03)

Single source of truth after the multi-session arc (discovery → retraction → genuine domain →
q=5 dual values). Adversarial-honesty ledger: PROVEN (Lean) / NUMERICAL / OPEN kept separate.
Nothing sent outward; local repo only.

## The object
- `λ_q = 2cos(π/q)`, `θ=π/q`. Observable `P` = gap-product (`=xy` naive / `=1/R_q` genuine).
- `X(q) = inf_μ ess-sup_μ P` over invariant measures of the Hecke BCZ return map.
- TWO maps, do not conflate:
  - **Naive** `T_q(x,y)=(y,⌊(1+x)/(λy)⌋λy−x)` on `D={x>0,y>0,x+λy>1}` — this is **only the i=q−1
    branch** of the genuine map; excludes the b=0 cusp line.
  - **Genuine** (Taha arXiv:1810.10668): clean triangle `𝒯^q={0<a≤1, 1−λa<b≤1}`, flat measure
    `(2/λ)da db`, piecewise-linear with `q−2` branches `M_{i,k}`. THE canonical Hecke object.

## The arc (what changed, and why)
1. **Discovery (q=3,4 + naive all-q):** optimizer = parabolic word `(1^{q−3},2)`, no ground state,
   naive value `V(q)` (2/9, √2/8, 1/4, √3/6, … increasing). q=3,4 sharp + no-GS Lean-proven.
2. **Retraction #1 (feasibility):** `(1^{q−3},2)` is feasible only **q≤11** (q=12 degenerate, q≥13
   empty s-window); `Xq_exact_for_word` never checked the floor UPPER bound. "V(q) for all q / →∞"
   RETRACTED for q≥12. Independently confirmed (`svalid_range → None` for q≥13).
3. **Retraction #2 → resolution (genuine domain):** the naive D is invariant only for q=3 (~100%
   seed-escape q≥4). The genuine Taha map on `𝒯^q` is invariant for ALL q (escape 0). The naive map
   was just one branch. ⇒ the optimization is **well-posed for all q on `𝒯^q`** — the q≥12 "wall" was
   a one-branch artifact, not real math.
4. **Genuine value:** `X_Ω(q) = 1/λ³ = 1/(2cos(π/q))³` for q≥5 (cusp word `[(q−2,0)]`, branch matrix
   `[[1,λ],[0,1]]`, b=0 fixed line), `= 2/9, √2/8` for q=3,4. **Decreasing** in q → 1/8. No-GS = escape
   to cusp vertex `(1/λ,0)`. Verified feasible past the fake wall (q=12,13,16).
5. **Interior vs global (q=5 dual values):** naive D excludes the cusp line, so its optimization =
   the genuine **INTERIOR** optimum `= V(q)` (= 1/4 at q=5). The genuine **GLOBAL** inf (cusp
   included) = `1/λ³` (= 1/φ³ ≈ 0.236 at q=5). Both legit; canonical = global `1/λ³`.

## Verified ledger
### PROVEN — Lean, axioms `[propext, Classical.choice, Quot.sound]`, no sorryAx (each compile-confirmed EXIT=0)
| result | file | scope |
|---|---|---|
| sharp X(3)=2/9, X(4)=√2/8, no-GS | `lean/BCZHecke_noGroundState_q3q4_VERIFIED.lean` | naive=genuine for q=3,4 |
| uniform `X(q) ≥ λ/(2(1+λ)²) ∀q` + rotation invariant `E_conserved_floor_one` | `lean/HeckeGeneralLB_VERIFIED.lean` | model-agnostic, all q |
| genuine `X_Ω(5) ≤ 1/φ³`, non-attainment (cusp upper bound + no-GS) | `lean/BCZHeckeG5_genuine_VERIFIED.lean` | genuine GLOBAL, q=5 |
| `g5_tpoint_excl` (1/4-point exclusion, unconditional) + sharp X_interior(5)=1/4 cond. on `Q5Window` | `lean/BCZHeckeG5_sharp_tpoint_VERIFIED.lean` | genuine INTERIOR (=V), q=5 |
| weak `X(5) ≥ (√5−2)/2` | `lean/BCZHeckeG5_lowerbound_VERIFIED.lean` | superseded by sharp |
| abstract engines `essSup_ge_of_window`, `essSup_ge_of_no_sustained` | (in the above) | map/observable-agnostic |

### NUMERICAL (primary-verified maps, high precision)
- Genuine domain `𝒯^q` invariant q=3..8 (escape 0); flat measure (`⟨a⟩=2/3`). Validation gate:
  genuine hunt reproduces proven 2/9, √2/8.
- `X_Ω(q)=1/λ³` (q≥5) = rigorous UPPER bound + best-found inf (exhaustive period≤7, digit≤2 → nothing
  lower), feasible q=5..30 incl past wall. Closed form `f(q−2)=1/λ³` symbolically exact.
- Interior optimum `= V(q)` for q=5,6; `< V(q)` for q=7,8 (search-bounded).
- Window-`(q−2)` hypothesis REFUTED: longest sub-threshold run `W*(q) ≈ 3(q−2)/2`
  (q=5..11 → 4,5,7,8,10,11,13), bounded.
- Closed form `X(q)` (interior/naive) re-verified symbolically + geometrically (`Xq_independent_verify.py`, 11/11).

### OPEN (honest frontier)
- **Sharp GLOBAL lower bound `X_Ω(q) ≥ 1/λ³` for all q** — needs a Mañé / Conze–Guivarc'h sub-action
  (the cusp orbit is the calibrated orbit). The headline open theorem. → `GOAL_D`.
- **`Q5Window`** (window-5 cluster bound, no 5 consecutive interior products < 1/4) — the last gap for
  sharp INTERIOR X_interior(5)=1/4 (t-point exclusion already done).
- Sharp + no-GS for q=5..11 in general (interior); cluster law `C(q)` exact form.

## Goal-prompt inventory
- **LIVE:** `GOAL_D_genuine_lower_bound.md` — genuine global lower bound `X_Ω(q)≥1/λ³` + no-GS, all q
  (carries q=5 cusp witness + cheap measure-form companion + the open sub-action).
- **DONE/resolved:** `GOAL_2` (closed form), `GOAL_7` (arithmetic meaning), `GOAL_B` (genuine domain),
  `GOAL_1` (uniform LB).
- **SUPERSEDED (bannered):** `GOAL_A` (naive rotation-sweep — produced the genuine INTERIOR sharp
  t-point exclusion for q=5 + the window refutation, still valid for the interior object),
  `GOAL_C` (naive q=5=1/4 / 4-window — premise false; re-targeted to genuine, now done).

## Cross-session verification (this session's contribution)
Independent re-verification (anti-fabrication) of the goal sessions' outputs:
- Closed form X(q): symbolic proof-core + geometric rebuild (`code/Xq_independent_verify.py`, 11/11).
- Feasibility ceiling q≤11 confirmed (`svalid_range`).
- Genuine `f(q−2)=1/λ³`, crossover, parabolic branch matrix `M_{q−2,0}` (sympy).
- Compile-confirmed (EXIT=0, axioms clean): `HeckeGeneralLB_VERIFIED`, `BCZHeckeG5_genuine_VERIFIED`,
  `BCZHeckeG5_sharp_tpoint_VERIFIED`.
- #1-vs-#2 consistency (`λ/(2(1+λ)²) ≤ X(q)`); interior-vs-global reconciliation.
Writeup: `research_notes/VERIFY_crosssession_2026-06-02.md`.

## −1 dominance (separate committed goal — compute-blocked)
M2 sieve `curve_3e14.tsv` (prime-counting to 3e14) in progress; analysis pipeline pre-validated
(`projects/minus1-dominance/`, Part B reproduces baseline). Independent frontier cross-check kernel
staged (`kaggle_frontier/`, primesieve, push-blocked on a 401 Kaggle token). Finalize `LEDGER.md §4`
when the curve lands.

## Hard constraints (unchanged)
Nothing outbound / published / Koyama-contacted (USER-gated). Parent repo is local-only (no remote).
Public submodule `primes-equispaced` NOT to be pushed without per-action confirmation (KOYAMA.md is
local-only there). `~/Documents` Drive-synced: treat `* (1)` / `.git (1)` as conflict artifacts.
