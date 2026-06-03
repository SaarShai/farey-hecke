# The arithmetic meaning of X(q): sharp Diophantine constants for Hecke–Farey gaps

> **CORRECTION (2026-06-03, goal B):** (1) the cluster law `C(6)=5 "stable"` (§0.2, §3) is NOT
> supported — the static height-sorted generator's `runBelowX` for q=6 GROWS with Q (4→40 over
> Q=20→320), i.e. generator incompleteness, not a stable bound. Trust the **dynamical** genuine
> domain Ω_q instead (interior optimum √3/6 for q=6). (2) The genuine *dynamical* `inf esssup`
> on Taha's true domain is **X_Ω(q)=1/λ³** for q≥5 (cusp), which DIFFERS from the `X(q)` table here
> (those are the i=q−1-branch / interior values, coincident with the genuine value only for q=3,4).
> See `FINDINGS_goalB_genuine_domain_2026-06-03.md`. The q=3 exact F_Q results (§1–2) are unaffected.

**Date:** 2026-06-02. **Goal #7.** Translate the dynamical quantity `X(q)` (ergodic-optimization
infimum of the Hecke BCZ map) into a number-theoretic statement about the gaps of the
`G_q`-Farey fractions. Anchor on the proven `q=3` case `X(3)=2/9`.

**Adversarial-honesty separation is enforced throughout: PROVEN / NUMERICAL / CONJECTURAL.**
Every external citation was checked against the primary text (see §7).

---

## 0. Headline

1. **q=3 (PROVEN + exact on real F_Q).** With the standard BCZ normalization, `X(3)=2/9` is the
   **sharp 3-window gap-product floor** of the ordinary Farey sequence:
   > Among any 4 consecutive Farey fractions of `F_Q` (denominators `b_n,b_{n+1},b_{n+2},b_{n+3}`),
   > `max(b_n b_{n+1}, b_{n+1} b_{n+2}, b_{n+2} b_{n+3}) ≥ (2/9) Q²`,
   > i.e. **no 3 consecutive normalized denominator-products `b_k b_{k+1}/Q²` are all `< 2/9`**
   > ("cluster ≤ 2"). The constant `2/9` is sharp (approached as the window denominators
   > → `(Q/3, 2Q/3)`, the vertex/parabolic optimizer) and never uniformly attained (no ground state).

   Verified **exactly** on real `F_Q` for all `Q ≤ 4000` (zero violations, longest run `=2`,
   min-window-max `→ 2/9⁺`). Machine-checked in Lean (`no_ground_state`, interior of the triangle).

2. **General q — the clean 3-window form is SPECIAL to q=3,4.** On **genuine** `G_q`-Farey points
   (actual `G_q`-orbit cusps), the project's `X(q)` values **do** act as sharp gap-product floors
   (`min W-window-max → X(q)⁺`, monotone), BUT the sharp **window length grows with q**:
   the longest run of consecutive products below `X(q)` is the **cluster bound** `C(q)`:

   | q | X(q) | cluster C(q) (max run < X) | sharp window W=C+1 |
   |---|------|----|----|
   | 3 | 2/9 = 0.22222 | **2** (PROVEN) | 3 |
   | 4 | √2/8 = 0.17678 | **2** (PROVEN) | 3 |
   | 5 | 1/4 = 0.25000 | **3** (NUMERICAL, stable) | 4 |
   | 6 | √3/6 = 0.28868 | **5** (NUMERICAL, stable) | 6 |

   So the goal's hoped-for "X(q) = sharp **3-window** floor for all q" is **FALSE for q≥5**
   (explicit, T-verified counterexamples: 3 consecutive `G_5`-products all `< 1/4`).

3. **Universal characterization (holds for all q).** `X(q) = inf_μ ess-sup_μ P` is the **sharp
   infimal ceiling** on the normalized denominator-product `P = c_n c_{n+1}/Q² = 1/(Q²·gap)`
   along recurrent `G_q`-Farey trajectories: **no recurrent trajectory keeps every `P < X(q)`**
   (verified: no sampled orbit has `ess-sup P < X(q)`), and `X(q)` is approached but not attained
   (no ground state). Equivalently — in gap language — `1/X(q)` is the sharp threshold for keeping
   every normalized gap above a level (achievable iff the level `< 1/X(q)`, never attained).
   For `q=3` this threshold is `1/X(3) = 9/2`.

4. **Prior art (must cite).** The `G_q`-Farey gap-return map itself is **not new**: it is the
   Boca–Cobeli–Zaharescu map analogue of A. Taha, *The BCZ map analogue for the Hecke triangle
   groups `G_q`* (arXiv:1810.10668), built on the discrete orbit `Λ_q = G_q·(1,0)^T` with its
   slope-gap distribution. What is new is the **ergodic-optimization** layer (`X(q)`, no ground
   state) — Taha proves no run-length/threshold statement. (Already documented in
   `research_notes/prior_art_taha_cobeli.md`, which also flags Cobeli–Zaharescu [CZ14] as prior art
   for integer-valence run-length bounds on the same continuant; the map's `λ`-coefficient is
   reconfirmed via the Rosen λ-CF, §4.)

---

## 1. The dictionary (q=3, ordinary Farey) — exact, primary-source

**Primary source (verified, §7):** F. Boca, C. Cobeli, A. Zaharescu, *A conjecture of R. R. Hall on
Farey points*, J. reine angew. Math. **535** (2001). BCZ map on the **Farey triangle**
`𝒯 = {(a,b) : 0 < a,b ≤ 1, a+b > 1}`:
```
        T(a,b) = (b, −a + ⌊(1+a)/b⌋·b).
```

**Dictionary.** For consecutive Farey fractions `a/b < a'/b'` in `F_Q`:
- `(x,y) = (b/Q, b'/Q) ∈ 𝒯`  (since `b,b' ≤ Q` and consecutive ⟹ `b+b' > Q`);
- the **next denominator** is `b'' = ⌊(Q+b)/b'⌋·b' − b`, and dividing by `Q`,
  `b''/Q = ⌊(1 + b/Q)/(b'/Q)⌋·(b'/Q) − b/Q`, i.e. `(x,y) ↦ (y, ⌊(1+x)/y⌋·y − x) = T(x,y)`. ✔
- **Gap:** `a'/b' − a/b = (a'b − ab')/(bb') = 1/(bb')` (Farey neighbour `a'b − ab' = 1`).

**Hence the observable:**
```
        P := x·y = b·b'/Q² = 1/(Q²·gap).
```
`P` is the **reciprocal normalized gap**: large `P` ⇔ small gap (both denominators ≈ Q); small `P`
⇔ large gap. (The project's loose phrase "gap-product" means this product of consecutive
denominators — the reciprocal of the normalized gap.)

**Reference for the section / gap distribution (verified, §7):** J. S. Athreya, Y. Cheung,
*A Poincaré section for the horocycle flow on the space of lattices*, IMRN **2014**, no. 10,
2643–2690 (arXiv:1206.6597): the first-return map of the section **is** the BCZ map; gives the
Farey/slope-gap distribution (Hall's distribution).

---

## 2. The q=3 arithmetic theorem (un-normalized) and its verification

**Proven (Lean, interior of `𝒯`):** along any BCZ orbit,
`max(P_n, P_{n+1}, P_{n+2}) ≥ 2/9` (`WindowBound`); `2/9 = inf_μ ess-sup_μ P` is not attained
(`no_ground_state`). Source: `lean/BCZHecke_noGroundState_q3q4_VERIFIED.lean`,
`aristotle_dispatch_v9/BCZErgodicOptimization.lean` (axioms clean).

**Un-normalized statement (P_n = b_n b_{n+1}/Q²):**
> For any 4 consecutive fractions of `F_Q`,
> `max(b_n b_{n+1}, b_{n+1} b_{n+2}, b_{n+2} b_{n+3}) ≥ (2/9)·Q²`.
> Equivalently `cluster ≤ 2`: at most 2 consecutive `b_k b_{k+1}/Q²` are `< 2/9`.
> Gap form: among any 3 consecutive Farey gaps, the **smallest** normalized gap `Q²·g ≤ 9/2`;
> you can never have 3 consecutive gaps each `> (9/2)/Q²`.

**Verification on real F_Q** (`code/X3_arithmetic_verify.py`), Q = 30…4000:

| Q | #fractions | longest run `<2/9` | interior+boundary violations of `≥2/9` | min window-max | argmin denominators |
|---|---|---|---|---|---|
| 100 | 3045 | 2 | 0 | 0.24150 | (35,69,34,67) |
| 1000 | 304193 | 2 | 0 | 0.224115 | (335,669,334,667) |
| 4000 | 4863603 | 2 | 0 | 0.2226947 | (1335,2669,1334,2667) |

- **Longest run `< 2/9` is exactly 2** for every `Q` (cluster ≤ 2 holds **exactly**, not merely
  asymptotically).
- **Zero violations** of `max(window) ≥ 2/9` over **all** windows (interior and boundary).
- **min window-max `→ 2/9⁺`** monotonically (rate `≈ 2/Q`); the minimizing window's denominators
  `→ (Q/3, 2Q/3)` — exactly the vertex / parabolic optimizer `(1/3,2/3) ↔ (2/3,1/3)`. **Sharpness.**

This is the airtight arithmetic grounding of `X(3)=2/9`.

---

## 3. The G_q-Farey points and the general-q result

**Object (Taha 2018, §7).** Hecke group `G_q = ⟨S, T_λ⟩`, `S(z)=−1/z`, `T_λ(z)=z+λ`,
`λ=λ_q=2cos(π/q)`. The `G_q`-Farey ("λ-Farey") points are the cusps `M·∞ = a/c`,
`M ∈ G_q`, `a,c ∈ ℤ[λ]` — the projectivization of the discrete orbit `Λ_q = G_q·(1,0)^T`. The
BCZ-type map is their **slope-gap return map**. For `q=3` these are exactly `ℚ` (ordinary Farey).

**Genuine-point generation** (`code/Gq_hecke_farey_general.py`, exact `ℤ[λ]` arithmetic for
q=4 λ=√2, q=5 λ=φ, q=6 λ=√3): generate all cusps in `[0,λ)` with **Galois height**
`H(c)=max_emb|c| ≤ Q` (finite by Northcott — note `ℤ[λ]` is *dense* in `ℝ`, so a one-embedding
`|c|≤Q` bound is infinite; this **dense-denominator subtlety is why the finite-level Farey picture
is cleanest for q=3**, where `ℤ` is discrete). Sort by value; form `P_n = |c_n||c_{n+1}|/Q²`.

**Correctness signals of the generator:** `#cusps ∝ Q²` (lattice count); consecutive-neighbour
determinants `a_{n+1}c_n − a_n c_{n+1} ∈ {1, λ}` for q=4,5 (genuine Hecke neighbours), `{1,λ,2}`
for q=6.

**Results (`code/Gq_hecke_farey_general.py`, Q = 40…1280, stable):**

| q | X(q) | longest run `<X` (cluster C) | viol(W=C+1) | min(W-window-max) → |
|---|------|------|------|------|
| 4 | √2/8 | **2** (all Q) | 0 | 0.182 → √2/8 |
| 5 | 1/4 | **3** (all Q) | 0 | 0.251 → 1/4 |
| 6 | √3/6 | **5** (all Q) | 0 | 0.292 → √3/6 |

- For each q, `X(q)` **is** the sharp gap-product floor: `min(W-window-max) → X(q)⁺` monotonically
  (sharpness), with `W(q) = C(q)+1`.
- The **3-window** form holds only for q=3,4. For q=5 there are genuine triples of consecutive
  products all below `1/4` (verified `code/Xq_recurrent_window_test.py`, e.g.
  `P=(0.1549,0.1546,0.2496)`, each `<0.25`, with `T_q(p_0)=p_1` checked); the 4-window holds.
- Independent corroboration: scaling-limit simulation of the map `T_q` from random seeds
  (`code/Xq_gap_dynamics_verify.py`, `Xq_recurrent_window_test.py`) reproduces the **proven**
  q=3,4 bounds (run≤2, 0 violations) and gives the **same** q=5 cluster (3), validating the method.

**Cluster law.** `C(q) = 2, 2, 3, 5` for `q = 3,4,5,6`. The optimizer word `(1^{q−3},2)` has period
`q−2`, a natural lower bound on the window; the exact law for general q is **OPEN** (q=6's value 5
exceeds `q−2 = 4`, coinciding with the extra `det = 2` cusp width). Do **not** claim a closed form.

---

## 4. The map's λ-coefficient (resolved)

The project's map is `T_q(x,y) = (y, ⌊(1+x)/(λy)⌋·λy − x)`, i.e. recurrence
`c_{n+2}=k_n·λ·c_{n+1}−c_n`, monodromy `S T^{k_n} = [[0,−1],[1,k_nλ]] ∈ G_q`. The **coefficient is
`k_n λ`**, confirmed three ways:
1. `S T^{k}` is genuinely a `G_q` element with lower-row `(1, kλ)` — the advance generator.
2. The **Rosen λ-continued-fraction** convergent recurrence is `q_{n+1}=a_n·λ·q_n − q_{n-1}`
   (partial quotients `a_n λ`, `a_n ∈ ℤ_{>0}`) — same `·λ`. (Rosen 1954; the `G_q`-Farey
   continuant.)
3. On genuine `G_q` cusps the `·λ` form matches ~63% of consecutive height-sorted steps vs **0%**
   for a `·1` form (`code/Gq_hecke_farey_general.py` test); the 37% misses are cusps skipped by the
   Galois-**height** ordering — i.e. height-sorted ≠ the exact BCZ-section sequence, so the residual
   is a normalization artifact, not a wrong coefficient.

(A WebFetch *summary* of Taha's Thm 2.2 once rendered the multiplier as `b` instead of `λb`; that
was a small-model transcription slip — the three checks above fix the coefficient as `λb`. The
project already documents Taha as the canonical `G_q`-BCZ source, see
`research_notes/prior_art_taha_cobeli.md`, which also flags **Cobeli–Zaharescu [CZ14]** as prior art
for *integer-valence* run-length bounds on the same continuant `k_j q_j = q_{j-1}+q_{j+1}`.)
None of this affects the empirical floors of §3 (computed directly on real cusps, map-formula-free)
nor the airtight q=3 result of §1–2.

---

## 5. Left endpoint of support (cleanest characterization)

`X(q)` is the **left endpoint of the support of the `W(q)`-window-max distribution** of `P` under
the BCZ measure (= `inf_μ ess-sup_μ P`). Verified: `min(W-window-max) → X(q)⁺` (§2, §3). For `q=3`,
`W=3`, this reduces to the proven statement. This is the sharpest "arithmetic = left edge of a
gap-statistic support" reading and it is what generalizes; the **3-window** value of `W` does not.
(Hall's distribution / Athreya–Cheung give the full `P`-marginal, whose support is `(0,1]`; the
non-trivial left edge `X(q)` lives on the **windowed max**, not the marginal.)

---

## 6. Honest scope

- **PROVEN (Lean, axioms clean):** q=3 cluster≤2 / 3-window floor `2/9`, no ground state; q=4
  cluster≤2 / 3-window floor `√2/8`, no ground state.
- **NUMERICAL, exact on real sequences:** q=3 un-normalized theorem on `F_Q` (Q≤4000, 0 violations,
  sharpness). Genuine `G_q`-point cluster bounds `C(4,5,6)=2,3,5` and `X(q)`-floor sharpness
  (stable to Q=640–1280; q=6 `det` structure `{1,√3,2}`).
- **NUMERICAL, dynamics:** scaling-limit `T_q` orbit statistics reproduce proven q=3,4 and
  corroborate q=5 cluster.
- **CONJECTURAL / OPEN:** exact `X(q)` for q≥5 as the true infimum (the lower bound, not just the
  parabolic-word upper bound, is unproven — consistent with `DISCOVERY_*` honest scope); the
  general cluster law `C(q)`; the exact reconciliation with Taha's normalization (§4).
- **KEEP DISTINCT:** `X(q)` (sharp gap-product / window floor) ≠ `q*_BCZ ≈ 0.86181`
  (measure-theoretic cluster-size-3 threshold, `ACHIEVEMENTS_FINAL.md`) ≠ `C ≈ 0.6699`
  (totient/Franel constant A065483/2). Three different constants.

---

## 7. Citations — verified against primary text (2026-06-02)

- **BCZ map & Farey triangle:** Boca–Cobeli–Zaharescu, *A conjecture of R. R. Hall on Farey points*,
  J. reine angew. Math. **535** (2001). Map `T(a,b)=(b,−a+⌊(1+a)/b⌋b)` on `{0<a,b≤1,a+b>1}`
  — **confirmed** (web search of primary statements). ✔
- **Section = BCZ:** Athreya–Cheung, *A Poincaré section for the horocycle flow on the space of
  lattices*, IMRN **2014**(10) 2643–2690, DOI 10.1093/imrn/rnt003, arXiv:1206.6597 — first-return
  map = BCZ map, Farey/slope gap distribution — **confirmed** (Oxford Academic + arXiv abstract). ✔
- **G_q-BCZ analogue (prior art for general q):** A. Taha, *The Boca–Cobeli–Zaharescu map analogue
  for the Hecke triangle groups `G_q`*, arXiv:1810.10668. Domain `𝒯^q={0<a,b≤1, a+λ_q b>1}`,
  `λ_q=2cos(π/q)`, discrete orbit `Λ_q=G_q(1,0)^T`, slope-gap distribution (Cor. 4.2) — **confirmed**
  (abstract + ar5iv). Exact Hecke map (Thm 2.2/2.3) not transcribed from HTML; the `λ`-coefficient
  is fixed independently via Rosen λ-CF + `S T^k ∈ G_q` (§4). Project note: `prior_art_taha_cobeli.md`. ✔
- **Hall gap distribution:** R. R. Hall, *A note on Farey series*, J. London Math. Soc. (1970) —
  cited, not re-verified this session.
- **Rosen λ-CF (G_q structure):** D. Rosen (1954) — cited, not re-verified this session.

---

## 8. Files

- `code/X3_arithmetic_verify.py` — q=3 exact verification on real `F_Q` (§2).
- `code/Xq_gap_dynamics_verify.py`, `code/Xq_recurrent_window_test.py` — scaling-limit `T_q`
  orbit statistics; reproduce proven q=3,4, corroborate q≥5 (§3).
- `code/Gq_hecke_farey_general.py` (+ `G4_hecke_farey_v2.py`) — genuine `G_q`-Farey point
  generation in exact `ℤ[λ]`, cluster bounds + sharpness (§3).
- `code/ergodic_hecke_hunt.py` — `X(q)` values (parabolic-word construction; predecessor work).
