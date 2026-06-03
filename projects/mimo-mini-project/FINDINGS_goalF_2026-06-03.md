# Goal F — general-q scalar no-sustained ⇒ X_Ω(q)=1/λ³: a CRITICAL CORRECTION

**Date:** 2026-06-03. **One-line verdict:** the prize as stated is **unattainable because its premise is
false**. The per-branch envelope **(B)** — "`P ≥ 1/λ³` on every non-scalar branch" — and hence the
**scalar reduction** (goal D's load-bearing result) hold **only for `5 ≤ q ≤ 15`**; both are **FALSE for
`q ≥ 16`**. The headline *value* `X_Ω(q)=1/λ³` nonetheless survives numerically for all tested q (cusp
upper bound is exact; no orbit beats it), but the general-q lower bound needs a genuine **multi-branch**
argument with a **window that grows ~`q/3`** — substantially harder than the "factor-2 / floor case
analysis" the goal anticipated. The sub-action/averaging route stays dead.

**Strict separation: PROVEN (Lean) / NUMERICAL / OPEN.** Nothing sent outward.

λ = λ_q = 2cos(π/q), θ=π/q. x_i = sin((i+1)θ)/sinθ (Chebyshev U_i), x_{-1}=0, x_0=1, x_{q-2}=1,
x_{q-3}=λ, x_{q-1}=0; recurrence x_{i+1}=λx_i−x_{i-1}, det x_{i-1}²−x_i x_{i-2}=1. Domain
𝒯^q={0<a≤1, 1−λa<b≤1}. L_j=a x_j + b x_{j-1}; branch i ⟺ L_{i-1}>1 ∧ L_i≤1; observable
P_i = a·L_i/x_{i-1}.

---

## 0. Headline (what changed, and why it is solid)

1. **THE CORRECTION (machine-checkable).** The per-branch envelope **(B)** `P_i ≥ 1/λ³` on branches
   `i=2..q−2` is **FALSE for q ≥ 16**. Prior work (`FINDINGS_goalD_*`) asserted (B) "verified all q≤8"
   and built the scalar reduction on it as holding for *all* q; that was an over-extrapolation from
   `q≤8`. Exhaustive recheck of the **actual genuine map**:

   > **(B)/reduction holds exactly for `5 ≤ q ≤ 15`; fails for `q ≥ 16`.**

   First failure `q=16`, branch `i=10` (genuine, non-scalar). Explicit witness, all constraints checked
   by hand:
   - `(a,b) = (0.785695, −0.541196)` — in 𝒯^q (`0<a≤1`, `b≤1`, `b>1−λa=−0.541196`);
   - on the cusp-side boundary of branch `i=10` (`L_9=1.000000`, `L_{10}=0.785695≤1`);
   - `P = a·L_{10}/x_9 = 0.130355 < 1/λ³ = 0.132492`.

   So a genuine point on a **non-scalar** branch has `P < 1/λ³`: the reduction "`P<1/λ³` ⇒ scalar
   branch" is broken at q=16. The minimum of `P_i` on a non-scalar branch `i` equals `x_{i-1}/(1+x_{i-2})²`
   (see §2); this drops below `1/λ³` for the middle branches once `q ≥ 16`.

2. **The headline VALUE survives (numerical, all q).** The genuine cusp orbit `[(q−2,0)]` gives
   `P = s²/λ → 1/λ³` exactly as `s→(1/λ)⁺`, for every q (machine-exact). And **no orbit beats it**:
   the adversarial **max-run** of consecutive `P<1/λ³` is finite for every q (so esssup `≥ 1/λ³`), and the
   minimised orbit-esssup over long genuine orbits stays `≥ 1/λ³`. Hence `X_Ω(q)=1/λ³` is still the
   value — but it is now **NUMERICAL for q≥16** (the q≤15 reduction proof no longer reaches it).

3. **The window GROWS ~`q/3` (not bounded).** Adversarial max-run of `P<1/λ³` on the genuine map:

   | q | 10 | 13 | 15 | 16 | 20 | 30 | 50 | 80 |
   |---|----|----|----|----|----|----|----|----|
   | max run | 3 | 4 | 4 | 4 | 8 | 10 | 16 | 24 |

   Finite for each q (so the value holds) but unbounded in q (`≈ q/3`). The goal-D table (q≤13: 3,2,3,3,3,4)
   stopped right before the growth becomes visible. ⇒ **no fixed window**; the clean uniform object is the
   genuine orbit-level "no orbit sustains all `P≤1/λ³`", and it is genuinely multi-branch for `q≥16`.

4. **Transience is the real general mechanism.** Although middle branches carry `P<1/λ³` points for
   `q≥16`, they are **transient**: from the extreme low-`P` vertex `a=v=x_{i-1}/(1+x_{i-2})`, the next
   one or two genuine steps already have `P ≥ 1/λ³` (running max jumps to ~0.8–0.96 within 40 steps,
   first step `≥thr` at n=0–1). So you cannot *dwell* at low `P` on a middle branch — but you *can* chain
   moderately-low values for ~`q/3` steps, which is why the window grows yet stays finite.

---

## 1. PROVEN this session (Lean, axioms `[propext, Classical.choice, Quot.sound]`, EXIT=0)

- **`cusp_envelope` (ALL q, parametric in `l≥φ`)** — `lean/BCZHeckeCusp_envelope_allq_VERIFIED.lean`:
  on the genuine **cusp branch `i=q−2`** (`x_{q-2}=1,x_{q-3}=l,x_{q-4}=l²−1`; guards
  `l a+(l²−1)b>1`, domain `l a+b>1`, upper `a+l b≤1`, `0<a≤1`), `P=a(a+l b)/l ≥ 1/l³`.
  This **generalises the q=5 `branch3_envelope` to every q** (the cusp branch is uniformly tight — its
  min is exactly `1/l³` at the cusp vertex `(1/l,0)` for all q; it is the *middle* branches, not the
  cusp branch, that violate (B) for q≥16). Certificate (verified symbolically,
  `code/Fgoal_cusp_cert_verify.py`), `W:=l²a(a+l b)−1`, `G:=l a+(l²−1)b−1`, `d:=l a+b−1`:
  - case `a≥1/l`: `(l²−2)·W = (l³−l−1)·aG + (l²−2)(l a−1)(1−a) + (l²−l−1)·a d`;
  - case `a≤1/l`: first `l²a≥1` (from `a≥1/(l+1)`, via upper guard + domain + `l²≥l+1`), then
    `(l²−2)·W = (l³−l−1)·a d + (l²−2)(l²a−1)(1−l a) + (l²−l−1)·aG`.
  All coefficients `≥0` for `l≥φ` (`l²−2>0`, `l³−l−1>0`, `l²−l−1≥0`); `l²−2>0` ⇒ `W≥0`.

Reused/valid from prior sessions: all-q cusp UB + non-attainment (`BCZHeckeGenuine_allq_VERIFIED`),
the W=3/W=4/no-sustained engines, the scalar `hecke_ground_value_pos` (½-strength), q=3/4 no-GS,
q=5 envelope/sharp.

---

## 2. (B) for `5 ≤ q ≤ 15` — clean reformulation + proof (where it IS true)

Using the det relation, branch `i` in coordinates `(a, v:=L_i)` with `m=x_{i-1}, c=x_{i-2}`
(`m²+c²−λmc=1`) has the clean constraint form
```
   (i)  a + c v > m        [L_{i-1} > 1]          (ii)  c a + v > m   [domain λa+b>1],
   0 < a ≤ 1,  0 < v ≤ 1,   P_i = a v / m.
```
Identity (pure ring): `a v (1+c)² = (a+cv)(ca+v) − c(a−v)²`. The minimum of `a v` over the region is
at the vertex `a=v=m/(1+c)` (where (i),(ii) are both tight), giving `min P_i = m/(1+c)² =
x_{i-1}/(1+x_{i-2})²`. Hence
```
   (B)  ⟺   λ³ · x_{i-1} ≥ (1 + x_{i-2})²     for every branch i=2..q−2.
```
Equivalently, with `p=x_i`: `(p−1)·(p² + (3c+1)p + (1+2c+c²−c³)) ≥ 0` — true for the **actual
Chebyshev triples** at `q≤15`, but the quadratic factor goes negative once a middle branch reaches
`x_{i-2}` large with `x_i` near 1, which first happens at **q=16** (verified `code/Fgoal_*`,
all q to 200). So:

- **q=5..15:** (B) holds (finite, machine-verified inequality set); with the cusp UB and the scalar
  no-sustained (C) at those q (finite windows `W(q)≤5`), the chain gives `X_Ω(q)=1/λ³` + no-GS.
- **q≥16:** (B) is FALSE; the chain is broken. The reduction cannot be the route.

---

## 3. NUMERICAL ledger (this session, primary-verified genuine map)

- Reduction premise (`P<1/λ³` only on scalar branch): TRUE q=5..15, FALSE q≥16 (witness §0.1).
  `min_i P_i = x_{i-1}/(1+x_{i-2})²` matches brute-force; `λ³x_{i-1}−(1+x_{i-2})²` ≥0 for q≤15, <0 q≥16.
- Headline value `X_Ω(q)=1/λ³`: cusp UB exact all q; no orbit beats it (max-run finite, §0.3);
  adversarial min orbit-esssup = 1.120/1.122/1.123 × `1/λ³` at q=20/30/50 (random orbits approach but
  never beat the measure-zero cusp inf). **Value holds; proof open for q≥16.**
- Window grows ~q/3 (§0.3 table); transience (§0.4).
- **β_min (averaging route) — DEAD.** Verified the q=5 witness with correct floor digits: scalar word
  `(1,1,2)`, periodic orbit `c=(0.30902, 0.5, 0.5)` (parabolic, eigval 1), products
  `(0.15451, 0.25, 0.15451)`, **time-avg P = 0.186342 < 1/φ³ = 0.236068** (ratio 0.789), esssup
  `= 0.25 = V(5)`. So `β_min < 1/λ³` at q=5 ⇒ by Mañé no sub-action is calibrated at `1/λ³`. A *uniform*
  sub-action must cover q=5 ⇒ **the averaging/sub-action route is globally dead** regardless of q≥6
  (where a bounded word search gives β_min=1/λ³, not ruling it out *there* but irrelevant to uniformity).

---

## 4. OPEN / honest frontier (re-scoped)

- **The general-q lower bound `X_Ω(q) ≥ 1/λ³` for q≥16** is the genuine open problem. It is NOT
  reducible to the scalar map (reduction false q≥16), NOT a fixed-window bound (window ~q/3), and NOT
  an averaging/sub-action bound (β_min<1/λ³ at least at q=5). It requires a multi-branch argument
  exploiting transience uniformly. **Harder than the goal's "factor-2/floor" framing.**
- For q=5..15 the program closes (B)+(C); (C) at each q is a finite scalar window bound (`W(q)≤5`),
  formalizable per-q (q=5 done; q=6,7 next if pursued).

## 5. Files
- Code: `code/Fgoal_envelope_explore.py`, `Fgoal_envelope_relaxed.py`, `Fgoal_clean_reformulation.py`,
  `Fgoal_cert*.py`, `Fgoal_cusp_cert_verify.py`, `Fgoal_largeq_*.py`, `Fgoal_maxrun_largeq.py`,
  `Fgoal_betamin_global.py`.
- Lean: `lean/BCZHeckeCusp_envelope_allq_VERIFIED.lean` (NEW, all-q cusp envelope).
- Corrects: `FINDINGS_goalD_genuine_lowerbound_2026-06-03.md` §0.1 (reduction "all q" → q≤15 only),
  `FINDINGS_goalB_*` headline (value 1/λ³ still numerically OK, but reduction-proof is q≤15).
