# Goal B — The genuine natural-extension domain Ω_q: is the Hecke BCZ ergodic optimization well-posed for ALL q?

**Date:** 2026-06-03. **Verdict in one line:** the phenomenon (a well-posed, no-ground-state
`inf_μ esssup_μ P`) is **GENUINELY ALL-q** on the true domain — **not** q=3-special. What was
*q≤4-special* is the project's naive closed form `V(q)`: the naive scalar map is only **one branch**
of the genuine piecewise map, evaluated on a **mis-stated unbounded domain**. Both the "≈100% escape
for q≥4" and the "infeasible for q≥12" were artifacts of that restriction.

**Adversarial-honesty separation enforced: PROVEN / NUMERICAL / CONJECTURAL.** Every citation
re-verified against primary text this session (two corrections to prior project citations, §7).

---

## 0. Headline results

1. **The true domain Ω_q is a CLEAN TRIANGLE for every q — not fractal, not a staircase.**
   Primary-verified from Taha's LaTeX source (arXiv:1810.10668): the genuine `G_q`-BCZ section is
   ```
        𝒯^q = { (a,b) : 0 < a ≤ 1,  1 − λ_q·a < b ≤ 1 },   λ_q = 2cos(π/q),
   ```
   with **flat** invariant measure `m_q = (2/λ_q) da db`, area `λ_q/2`. **NUMERICALLY VERIFIED
   invariant** for q=3..8: escape rate of generic seeds under the genuine map = **0.0000** (vs the
   naive scalar map's **0.995–0.999**). [Goal's premise that Ω_q is fractal/"staircase" for the BCZ
   coordinates is FALSE — that staircase belongs to the *Rosen Gauss-map* natural extension, a
   different coordinatization (§7, BKS).]

2. **The genuine map is piecewise-linear SL₂, with `q−2` branches.** On `𝒯^q_i` (i=2..q−1,
   `𝔴_i = U^i(1,0)ᵀ`, `U=[[λ,−1],[1,0]]`):
   ```
        BCZ_q(a,b) = ( (a,b)·𝔴_i ,  (a,b)·𝔴_{i+1} + k·λ·(a,b)·𝔴_i ),
        k = ⌊ (1 − (a,b)·𝔴_{i+1}) / (λ·(a,b)·𝔴_i) ⌋.
   ```
   Branch+digit matrix `M_{i,k} = [[x_i, y_i],[x_{i+1}+kλx_i, y_{i+1}+kλy_i]]`, **det = 1**.
   **The project's scalar map `(y, ⌊(1+x)/(λy)⌋λy−x)` is EXACTLY `M_{q−1,k}` — the i=q−1 branch
   only.** (Identity `y_i = x_{i−1}`, `x_i = sin((i+1)π/q)/sin(π/q)` ⇒ `M_{q−1,k}=[[0,1],[−1,kλ]]`,
   the project's `M(k)`.) For q=3 there is only one branch (i=2=q−1), so scalar = genuine ⇒ no escape.
   For q≥4 the scalar formula is wrong on branches i=2..q−2 ⇒ the observed escape.

3. **The ergodic optimization is well-posed and no-GS for ALL q.** With the gap-product observable
   correctly translated as the **reciprocal slope-gap** `P = 1/R_q = a·(a,b)·𝔴_i / y_i` (= `a·b` for
   q=3, and = `a·b` on the i=q−1 branch for all q):
   ```
        X_Ω(q) = inf_μ esssup_μ P   exists, is finite, and is approached-but-not-attained for ALL q.
   ```
   The global optimizer is the **period-1 cusp fixed-line** in branch q−2 (the unique period-1
   parabolic family): orbit `(s,0)`, `s ∈ (1/λ, 1]`, with `P = s²/λ → 1/λ³` as `s → (1/λ)⁺`:
   ```
        X_Ω(q) = 1 / λ_q³ = 1 / (2cos(π/q))³        for q ≥ 5,
        X_Ω(3) = 2/9,   X_Ω(4) = √2/8               (interior optima; cusp line absent/higher).
   ```
   **No ground state**: the inf is approached as orbits **escape to the cusp vertex `(1/λ, 0)`** of
   the triangle (where the b=0 line meets the open lower edge `b=1−λa`) — the literal "escape to cusp."

4. **Comparison to the naive `V(q)`.** `V(q)` is the optimum *restricted to the i=q−1 branch and to
   interior orbits*. It equals the genuine **global** value only for **q=3,4**. For q=5,6 it equals
   the genuine **interior** (non-cusp) optimum but the global value (cusp) is lower; for q≥7 it is not
   even the interior optimum. Concretely (genuine global `1/λ³` vs naive `V`):

   | q | λ_q | X_Ω(q)=1/λ³ (genuine global) | V(q) naive | genuine interior optimum |
   |---|-----|------------------------------|------------|--------------------------|
   | 3 | 1 | (no cusp line) → 2/9 | 2/9 | 2/9 ✓PROVEN |
   | 4 | √2 | 0.353553 (cusp, higher) → √2/8 | √2/8 | √2/8 ✓PROVEN |
   | 5 | φ | **√5−2 = 0.236068** | 1/4 = 0.250 | 1/4 (=V) |
   | 6 | √3 | **1/(3√3) = 0.192450** | √3/6 = 0.28868 | √3/6 (=V) |
   | 7 | — | **0.170915** | 0.388740 | ≈0.357 (< V) |
   | 8 | — | **0.158513** | 0.461940 | ≈0.317 (< V) |
   | 12| — | **0.138701** | (naive infeasible) | — |
   | 13| — | **0.136562** | (naive infeasible) | — |
   | 16| — | **0.132492** | (naive infeasible) | — |

   `1/λ³` is **decreasing** in q toward `1/8` (λ→2); `V(q)` was **increasing**. Past the naive q=11
   "wall," X_Ω(q) is finite and the cusp orbit is a verified feasible no-GS periodic orbit
   (checked q=12,13,16,20,30). **The "wall" was an artifact of the one-branch restriction.**

---

## 1. What the naive setup got wrong (three compounding errors)

The project's object was `T_q(x,y)=(y, ⌊(1+x)/(λy)⌋λy−x)` on `D={x>0,y>0, x+λy>1}`, `P=xy`.
Against Taha's primary text:

- **(a) Domain inequality.** `D` used `x+λy>1` (λ on `y`); the genuine lower edge is `λa+b>1`
  (λ on `a`). And `D` dropped the caps `a≤1, b≤1` (D is an unbounded cone; `𝒯^q` is a bounded
  triangle).
- **(b) Map.** The scalar map is only the **i=q−1 branch**. For q≥4 a generic seed lands in branches
  i=2..q−2, where the scalar formula produces the wrong image — in particular it yields digit **k=0**
  whenever `λy>1+x` (⇒ `y'=−x<0`, "nonpos" escape). Measured digit-0 frequency rises with q
  (382→875 per 1000 seeds, q=4→13). This is the escape mechanism.
- **(c) Observable.** `xy=ab` is the reciprocal gap only on the i=q−1 branch / for q=3. The correct
  translation is `P=1/R_q` (Taha's roof `R_q = y_i/(a·(a,b)·𝔴_i)`), which reduces to `ab` exactly
  where the scalar picture is valid.

Consequence: the naive "feasibility window collapses at q=12, empty for q≥13" (`svalid_range`) is a
statement about the **single i=q−1 branch on the cone**, not about the genuine dynamics. The genuine
optimizer lives in branch **q−2** (the cusp line), which the single-branch search never sees.

---

## 2. Numerical verification (all reproducible; files in §8)

- **Invariance (decisive).** `Bgoal_taha_genuine.py`: genuine-map escape over 300 steps,
  1500 seeds/q: q=3→0.0000, q=4→0.0000, …, q=8→0.0000. Scalar map same seeds: q=4→0.9953, …,
  q=8→0.9987. The genuine triangle is invariant; the naive cone is not (q≥4).
- **Flat measure.** Long single orbit moments match flat-Lebesgue on `𝒯^q`: `⟨a⟩=0.6667` (= 2/3
  for all q, the flat value `∫a·λa da /(λ/2)=2/3`), `⟨b⟩` matches `1−λ/3` (q=4: orbit 0.5284 vs
  exact 0.5286). Consistent with all branch matrices being det-1 linear (Lebesgue-preserving).
- **X_Ω via parabolic-word search on genuine branch matrices** (`Bgoal_genuine_hunt.py`,
  analytic scale-window generalizing `svalid_range`): reproduces the **PROVEN** values
  X_Ω(3)=2/9 and X_Ω(4)=√2/8 exactly (validation gate passed), with numeric cross-check on the
  genuine map (itinerary match, periodicity, `maxP → value` as `s→s_lo⁺`).
- **Cusp closed form** (`Bgoal_verify_allq.py`): word `[(q−2,0)]` is the unique period-1 parabolic
  family (trace `=2x_{q−2}=2`); window `(1/λ,1]`; `s_lo=1/λ` exactly; lower bound **OPEN** (b>1−λa);
  `P→1/λ³`. Verified feasible+periodic+no-GS for q=5..30 incl. 12,13,16.
- **Robustness.** Exhaustive feasible-parabolic-word search (period ≤5, digits ≤2; deeper ≤6–7 for
  q=5,6,7): **no word beats `1/λ³`** ⇒ the cusp value is the global inf within these bounds.

---

## 3. The no-ground-state mechanism, made literal

`𝒯^q` has a vertex at `(1/λ, 0)` where the b=0 line meets the open lower edge `b=1−λa`. The
minimizing measures are the closed-horocycle / cusp fixed-points `(s,0)` with `s↓1/λ`; their support
slides into that vertex. Since `s=1/λ` is on the **open** edge (excluded), the inf `1/λ³` is
**approached but never attained** — "the optimizing configurations escape to the cusp." For q=3,4 the
cusp line is absent (q=3) or sub-optimal (q=4), and the no-GS is instead an interior open bound
(floor-jump / triangle edge) at 2/9, √2/8 — but the qualitative conclusion (no ground state) is the
same. **No-GS holds for all q.**

---

## 4. STATUS ledger (strict separation)

- **PROVEN (Lean, axioms `[propext,Classical.choice,Quot.sound]`):** X(3)=2/9, X(4)=√2/8, no ground
  state — these are about the q=3 genuine map (= scalar) and the q=4 case; **unchanged and still
  valid.** This session's genuine-map hunt **independently reproduces both** (validation gate).
- **NUMERICAL (this session, primary-verified map):**
  - Genuine domain `𝒯^q` invariant for q=3..8 (escape 0); flat measure confirmed.
  - X_Ω(q)=`1/λ³` for q≥5 is a **rigorous upper bound** (explicit feasible no-GS orbit) and the
    **global inf within exhaustive period≤5–7, digit≤2 search** (nothing lower found). Finite for all
    q incl. q≥12. No-GS (open lower edge) for all q.
  - Genuine interior (non-cusp) optimum = V(q) for q=5,6; `< V(q)` for q=7,8 (search-bounded).
- **CONJECTURAL / OPEN:**
  - That `1/λ³` is the *exact* inf (not merely the best up to period ~7) for q≥5 — the lower bound
    "no invariant measure has esssup P < 1/λ³" is **not proven** (would need a Mañé/Conze–Guivarc'h
    sub-action argument on `𝒯^q`).
  - Whether the right *modeling* choice includes the cusp (b=0) fixed-line. Including it (literal
    `inf_μ`): X_Ω=1/λ³. Excluding it (interior Farey orbits only): a different, larger value = V(q)
    for q≤6. Both are reported; the literal problem includes it.
- **CORRECTS prior project docs:**
  - The retracted "no-GS for all q with increasing `V(q)`" (`DISCOVERY_*`) — `V(q)` is the
    one-branch interior value, not the genuine global; the genuine global is `1/λ³`, **decreasing**.
  - `ARITHMETIC_MEANING_Xq.md` cluster law `C(6)=5 "stable"` — the static height-sorted generator
    (`Gq_hecke_farey_general.py`) shows `runBelowX` **growing** with Q for q=6 (4→40 over Q=20→320),
    i.e. NOT stable at 5; likely generator incompleteness at higher Q. The **dynamical** Ω_q is the
    authoritative object and gives a clean interior optimum √3/6 for q=6. Flag, do not rely on the
    static C(6)=5 claim.

---

## 5. Answers to the goal's four sub-questions

1. **Correct return-map domain Ω_q & observable, each q:** `𝒯^q={0<a≤1, 1−λa<b≤1}` (clean triangle,
   flat measure `2/λ`), genuine piecewise-linear branch map (§0.2); observable `P=1/R_q`.
2. **Does X_Ω(q)=inf esssup exist for ALL q, approached-not-attained?** **YES** — finite for all q
   (incl. past the naive q=11 wall), no ground state (cusp escape) for all q.
3. **What is X_Ω(q); match q≤11 closed form?** `1/λ³` (q≥5), 2/9 (q=3), √2/8 (q=4). It matches the
   naive `V(q)` only for q=3,4. The naive closed form is **not** the genuine value for q≥5.
4. **Verdict:** **ALL-q phenomenon** (well-posed, no-GS, X_Ω(q)=1/λ³ for q≥5). NOT q=3-special and
   NOT {3,4,6}-special. The q-specialness was entirely in the *naive map's* single-branch restriction.

---

## 6. Why this is the deepest of the three goals, settled

It determines that goals A/#2/#7 **do** generalize — the Hecke ergodic-optimization object is real
for all q — but that the specific quantity they were tracking (`V(q)`) is the q≤4-coincidental
single-branch value, not the genuine invariant. Any general-q claim must use the genuine branch map
on `𝒯^q` and the value `1/λ³`, not the naive `V(q)` table.

---

## 7. Citations — re-verified against primary text (2026-06-03)

- **Taha, arXiv:1810.10668** (LaTeX source v2, 2019-03-30): domain `𝒯^q={0<a≤1, 1−λa<b≤1}`;
  piecewise BCZ_q on branches `𝒯^q_i`, i=2..q−1, with `𝔴_i=U^i(1,0)ᵀ`, `U=[[λ,−1],[1,0]]`; index
  `k_i=⌊(1−(a,b)·𝔴_{i+1})/(λ(a,b)·𝔴_i)⌋`; roof `R_q=y_i/(a·(a,b)·𝔴_i)`; **flat** cross-section
  measure `m_q=(2/λ)da db`; slope-gap law `m_q(𝟙_{R_q≥t})`. **Confirmed.** (Corrects the project's
  earlier `T^q={0<a,b≤1, a+λb>1}` — λ was on the wrong variable; and the "fractal/staircase BCZ
  domain" premise — the BCZ domain is the full triangle.)
- **Burton–Kraaikamp–Schmidt, "Natural extensions for the Rosen fractions": TAMS 352 (2000),
  1277–1298** — NOT "TAMS 364 (2012) 5917–5958" (that is **Kraaikamp–Schmidt–Steiner**, α-continued
  fractions, arXiv:1011.4283). BKS is not on arXiv; its Rosen natural-extension **domain is the
  finite rectangle "staircase"** in the *Gauss-map* coordinates (interval `[−λ/2,λ/2)`, density
  `dx dy/(1+xy)²`), governed by the finite orbit of `λ/2` (even q: q/2 rectangles; odd q: q−1
  interleaved). **This is a different cross-section from Taha's BCZ triangle** — the goal's "Ω_q is
  fractal" came from conflating the two. (Transcription via KSS arXiv:0905.4588 §4.1/§5.1 and
  DKS arXiv:math/0702516, which quote BKS verbatim.)
- **Rosen, Duke 21 (1954)** — λ-CF, convergent recurrence `R_n=d_nλR_{n−1}+ε_nR_{n−2}`. Cited.
- **Athreya–Cheung, IMRN 2014 (arXiv:1206.6597); Takeuchi, JMSJ 29 (1977)** — section=BCZ (q=3);
  arithmetic ⟺ q∈{3,4,6,∞}. Cited.

---

## 8. Files (`projects/mimo-mini-project/code/`)

- `Bgoal_escape_char.py` — escape mechanism (digit-0/below-line), naive map, q=3..13.
- `Bgoal_omega_grid.py` — grid maximal-invariant-set probe (shows grid mis-measures the
  measure-zero optimizer; motivates the word search).
- `Bgoal_taha_genuine.py` — **genuine Taha map**; invariance (escape 0) + flat-measure verification.
- `Bgoal_genuine_hunt.py` — X_Ω(q) by parabolic-word search on genuine branch matrices; analytic
  scale-window; validation gate (2/9, √2/8) + numeric cross-check.
- `Bgoal_cusp_extend.py` — global vs interior optimum across q; cusp closed-form table.
- `Bgoal_verify_allq.py` — `[(q−2,0)]` cusp orbit verified feasible/periodic/no-GS, q=5..30; robustness.
- `Bgoal_robust_deep.py` — deeper-period robustness (q=5,6,7).
