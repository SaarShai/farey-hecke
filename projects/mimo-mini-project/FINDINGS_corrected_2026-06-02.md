# Hecke BCZ ergodic optimization — CORRECTED findings (session 2026-06-02, goal #1)

> **SUPERSEDED IN PART (2026-06-03, goal B):** the "naive map / triangle D" analyzed below is only
> the **i=q−1 branch** of the genuine Taha BCZ_q map, on a **mis-stated unbounded domain** (λ on the
> wrong variable). The ≈100% escape and the q≤11 "feasibility wall" are artifacts of that one-branch
> restriction. On the GENUINE clean triangle 𝒯^q (invariant for ALL q, flat measure) the optimization
> is well-posed all-q with X_Ω(q)=1/λ³ (q≥5), 2/9, √2/8 (q=3,4); no-GS via cusp escape. The naive
> V(q) coincides with the genuine value only for q=3,4. See
> `FINDINGS_goalB_genuine_domain_2026-06-03.md`. The PROVEN Lean q=3,4 values are unaffected.

Adversarial-honesty pass on the general-q "no ground state" goal. **Headline correction:** the clean
optimizer family `(1^{q−3},2)` and the simple triangle model are valid only for a *bounded* range of q
(feasible exactly for **q ≤ 11**), NOT all q. The discovery doc's X(q) table for q≥13 and its
"no-GS for all q" claim were **not substantiated** — they were produced by `Xq_exact_for_word`, which
computes only the *lower* scale bound `s_lo` and never checks the floor *upper* bound / feasibility.
This file records what is rigorously true, what is numerical, and exactly what is retracted.

## 0. Object (unchanged)
`λ=λ_q=2cos(π/q)`. `T_q(x,y)=(y, ⌊(1+x)/(λy)⌋·λy − x)` on `D={x>0,y>0,x+λy>1}`. `P=xy`.
`X(q)=inf` over `T_q`-invariant prob. measures of `ess-sup_μ P`.

## 1. RIGOROUS structural results (proofs in §6; hold for all q≥3)

**T1 (all periodic orbits are parabolic).** With the floor sequence fixed along an orbit, `T_q` is
*linear*: `(c_n,c_{n+1}) ↦ M(k_n)(c_n,c_{n+1})`, `M(k)=[[0,1],[-1,kλ]]∈SL₂`. A period-p orbit is a
nonzero fixed vector of `M_tot=M(k_{p-1})⋯M(k_0)`, which exists iff `1` is an eigenvalue iff
`tr M_tot = 2` (parabolic). So every periodic orbit in `D` is the **+1-eigenvector of a parabolic word**,
hence a **scale-free family** `c_n(s)=s·v_n`. (Consistent with: BCZ map = horocycle-flow Poincaré
section ⇒ periodic orbits ↔ closed horocycles ↔ parabolic/unipotent.) Corollary: there are **no
isolated (hyperbolic) periodic orbits** in `D`; the ergodic-optimization inf over periodic measures is
an inf over feasible parabolic words of a boundary value.

**T2 (closed form of the `(1^{q−3},2)` family).** For q≥4 this word is parabolic and its eigen-orbit is
```
        c_n(R) = R · sin((n+1)π/q),   n = 0,…,q−3   (period q−2),
```
i.e. the orbit cycles through `R·{sin(π/q),…,sin((q−2)π/q)}`. The all-1 recurrence
`c_{n+2}=λc_{n+1}−c_n` is rotation by π/q (Chebyshev); the lone 2 closes the period.

**T3 (conserved quantity).** On any floor-1 (rotation) run, `E=c_n²+c_{n+1}²−λc_nc_{n+1}` is invariant,
and on the family `E=R²sin²(π/q)`.

**T4 (max product of the family).** `max_n c_n c_{n+1} = R²·m(q)`,
`m(q)=cos(π/q)` (q even), `cos²(π/2q)` (q odd). [verified exactly q=4..12]

**T5 (single-defect closure law).** `(1^{p−1},m)` is parabolic ⟺ `m = 1 + tan(pπ/2q)·tan(π/q)`.
For `m=2` this forces `p=q−2` (the unique single-defect optimizer); no other small-m integer solutions
exist (the only other integer hits are the `tan(π/2)`-singularity artifact at p=q). ⇒ for q≥12, **no
single-defect parabolic word is feasible**.

## 2. UPPER BOUND + non-attainment (rigorous, feasible range q≤11)
For 4≤q≤11 the family lies in `D` for all `R∈(R_lo,R_hi]` (nonempty open window), giving genuine
periodic-orbit invariant measures with `ess-sup P = R²m(q)`. Hence
```
        X(q) ≤ V(q) := R_lo(q)² · m(q),   approached as R→R_lo⁺, NOT attained
```
(`R_lo` is an OPEN bound — triangle `x+λy=1` or a floor-jump edge). Exact values (mpmath, 50 dp):

| q | λ | X(q)=V(q) | closed form | binding (open) | regime vs 1/(4λ) |
|---|---|-----------|-------------|----------------|------------------|
| 3 | 1 | 0.2222222… | **2/9** | floor-jump | two-lobe (X<1/4λ) |
| 4 | √2 | 0.1767767… | **√2/8** (GLOBAL MIN) | triangle | **tangent (X=1/4λ)** |
| 5 | φ | 0.2500000 | **1/4** | floor-jump | connected (X>1/4λ) |
| 6 | √3 | 0.2886751… | **√3/6** | triangle | connected |
| 7 | — | 0.3887395… | deg-6 alg. | floor-jump | connected |
| 8 | — | 0.4619398… | **cos(π/8)/2** | floor-jump | connected |
| 9 | — | 0.5868241… | deg-6 alg. | floor-jump | connected |
| 10 | — | 0.6881910… | **cot(π/5)/2** | floor-jump | connected |
| 11 | — | 0.8379846… | — | floor-jump | connected |

`X(4)=√2/8` is the global minimum over the feasible range; `X(q)` strictly increases on 4..11.

## 3. FEASIBILITY BOUNDARY (corrects the discovery)
**T6.** `(1^{q−3},2)` is feasible (nonempty OPEN scale window) ⟺ **q ≤ 11**. q=12 is degenerate
(window collapses to a point: for even q the floor cap `R≤1/max_j sin(jπ/q)=1` is hit exactly at the
90° sample, while triangle needs `R≥1/min_n(2sin((n+1)π/q)+sin((n+3)π/q))≥1`). q≥13: window empty
(`R_lo>R_hi`). Feasibility ⟺ `max_{floor-1 steps} v_{n+2} < min_n(v_n+λv_{n+1})`, `v_n=sin((n+1)π/q)`;
the spread of `sin(jπ/q)` over the rotation arc defeats this for large q.

**Exhaustive search for ANY feasible parabolic word, q=13,14,16 (all returned 0 feasible):**
- ALL `{1,2}`-words up to period **30** (74 253 543 necklaces — q=13,16). **0 feasible.**
- ALL `{1,2,3}`-words up to period **18** (33 302 927 necklaces each — M1 fleet, q=13,14,16). **0 feasible.**
- high-floor sparse (≤3 defects, defect value ≤26). **0 feasible.**
- (`{1,2,3,4}`≤period 16 on M2 still running — bonus, will only strengthen.)
Validation: the identical search reproduces the q≤11 optimizers `(1^{q−3},2)` exactly. Conclusion:
**no feasible parabolic word for q∈{13,14,16} within (floors≤2, period≤30) ∪ (floors≤3, period≤18).**

**Why this happens (honest interpretation).** The naive triangle `D` is the correct natural-extension
domain only for q=3 (classical SL₂(ℤ) BCZ). For **all q≥4** ~100% of generic seeds *escape* `D`
within 500 steps (measured: q=3 → 0% escape; q=4,6,8,11,12,13,16 → 99.9–100%). The true Rosen/Hecke
natural-extension domain `Ω_q ⊊ D` is a proper (q-dependent, for non-arithmetic q fractal/multi-piece)
subset — a KNOWN feature of Rosen continued fractions (Burton–Kraaikamp–Schmidt; Nakada). The simple
`(1^{q−3},2)` family happens to sit inside `Ω_q` for q≤11; for q≥12 it does not, and the clean triangle
model breaks. The arithmetic Hecke groups are q∈{3,4,6} (Takeuchi); the model is cleanest there.

## 4. STATUS ledger (strict separation)
- **PROVEN (Lean, axioms `[propext,Classical.choice,Quot.sound]`, no sorryAx):** no ground state for
  q=3 (`no_ground_state`, value 2/9) and q=4 (`g4_no_ground_state`, value √2/8). Unchanged, still valid.
- **RIGOROUS (paper, this file §6):** T1–T6; upper bound `X(q)≤V(q)` + non-attainment for q≤11;
  feasibility boundary q≤11.
- **NUMERICAL:** the exact X(q) values & closed forms q=4..11; `(1^{q−3},2)` is the min-X feasible
  parabolic word for q≤11; no feasible parabolic word for q≥12 within the searched bounds.
- **LOWER BOUND `X(q)≥V(q)` (i.e. no orbit beats the family) + no-GS:** PROVEN only q=3,4 (Lean);
  q=5..11 numerical+structural; **q≥12: model invalid as posed**.
- **RETRACTED:** discovery `DISCOVERY_Hecke_ergodic_optimization.md` X(q) for q≥13 ("computed exactly
  q=3..30", "strictly increasing →∞", "no-GS universal across the Hecke family for q=3..30"). These
  rest on infeasible orbits. The honest claim is the q≤11 range + arithmetic q∈{3,4,6}.

## 5. Regimes (T7) — why the lower bound is q-specific
Max product on the cusp line `x+λy=1` is `1/(4λ)`. Region `{x+λy>1, xy≤V}`:
- q=3: `V=2/9 < 1/4=1/(4λ)` ⇒ **two disjoint lobes** (the clean q=3 proof: a_{m+1}<1/3 or >2/3).
- q=4: `V=√2/8 = 1/(4√2)=1/(4λ)` ⇒ hyperbola **tangent** to line (double root) — the hard "Middle".
- q≥5: `V(q) > 1/(4λ)` ⇒ region **connected**; one-step geometry can't force the product up, the lower
  bound must use the dynamics (multi-step). This is why no single argument covers all q.

## 6. Proof sketches (the rigorous bits)
**T1:** above. **T2:** `2cos(π/q)sin((n+2)π/q)=sin((n+1)π/q)+sin((n+3)π/q)` gives the floor-1
recurrence for n=0..q−4; `sin((q−2)π/q)=sin(2π/q)` and `2λ sin(π/q)=2sin(2π/q)` give the floor-2
closing `c_1=2λc_0−c_{q−3}`, and `sin((q−1)π/q)=sin(π/q)` gives `c_{q−2}=c_0`. Scale-free since the
relations are linear-homogeneous in R. **T3:** direct: under `c_{n+2}=λc_{n+1}−c_n`,
`E_{n+1}−E_n=(c_{n+2}−c_n)(c_{n+2}+c_n−λc_{n+1})=(c_{n+2}−c_n)·0=0`; on the family
`sin²a+sin²b−2cosθ·sin a sin b=sin²θ` with `b=a+θ`. **T4:** `sin(jθ)sin((j+1)θ)=½(cosθ−cos((2j+1)θ))`,
maximal when `(2j+1)θ` nearest π. **T5:** `tr(M(1)^{p-1}M(m))=2cos(pπ/q)+(m−1)λ·sin(pπ/q)/sin(π/q)=2`
⇒ `m−1=tan(pπ/2q)tan(π/q)`. **T6:** feasibility `s_lo<s_hi` ⟺ `max_{flr1} v_{n+2}<min_n(v_n+λv_{n+1})`;
evaluate on `v_n=sin((n+1)π/q)`.

## 7. Files
`code/optimizer_closed_form.py` (T2–T4, X(q), regime), `code/hunt_necklace.py` (exhaustive parabolic
search), `code/hunt_sparse.py` (multi-defect), `code/inf_direct.py` + escape test (naive-D non-invariance),
`code/ergodic_hecke_hunt.py` (original; note its `Xq_exact_for_word` skips feasibility — source of the
retracted large-q values).
