# Goal H — `X_Ω(q) ≥ 1/λ³` for q≥16: the ROTATION mechanism (genuine progress + honest crux)

**Date:** 2026-06-03. **One-line verdict:** the multi-branch lower bound is governed by a single,
clean, *exact* mechanism — **the sustained sub-threshold runs are rotations by `π/q`**. Every maximal
recurring low-`P` word has **elliptic monodromy of trace exactly `λ = 2cos(π/q)`** (conjugate to the
fundamental rotation `R`), so the product observable is a quasi-sinusoid that is forced back above
`1/λ³` within `O(q)` steps — exactly the "transience" the goal anticipated, now made algebraically
exact and machine-verified. The headline value `X_Ω(q)=1/λ³` is **re-confirmed** (exhaustive
digit≤4/period≤5 search: only the cusp word realizes it; nothing goes below). A **fully q-uniform
proof of (C′) remains open** — the precise remaining nut is isolated and stated below.

**Strict separation: PROVEN (Lean) / NUMERICAL / OPEN.** Nothing sent outward.

λ = λ_q = 2cos(π/q), θ=π/q. x_i = sin((i+1)θ)/sinθ; boundary values x_{q-1}=0, x_{q-2}=1, x_{q-3}=λ,
x_{q-4}=λ²−1. Genuine `BCZ_q` on `𝒯^q={0<a≤1, 1−λa<b≤1}`, branches i=2..q−1, piecewise-LINEAR SL₂.
Observable `P = a·L_i/x_{i-1} = c_n c_{n+1}/x_{i_n−1}` (c_n = aₙ). thr := 1/λ³.

---

## 0. Headline (what is new, and why it is solid)

1. **The sustained word is a ROTATION (exact, all q).** The longest sub-threshold runs are pure-scalar
   only at q=16; from **q≥17** they are NOT pure-scalar but follow the period-3 word
   > **`W_q = (q−1, 3) (q−1, 0) (q−3, 0)`**  — scalar branch `q−1` + branch `q−3`, *skipping* the cusp `q−2`.

   Its monodromy (using only the universal boundary Chebyshev values, so q-independent in λ) is
   `M_{q-3,0}·M_{q-1,0}·M_{q-1,3} = [[−λ, 2λ²+1],[−1, 2λ]]`, with **det = 1 and trace = λ**. Hence `M`
   is **elliptic, conjugate to the fundamental rotation `R=[[λ,−1],[1,0]]`** (trace λ, eigenvalues
   `e^{±iπ/q}`). Verified symbolically (`code/Hgoal_symbolic.py`) and **machine-checked in Lean for all
   q** (`lean/BCZHeckeRotation_allq_VERIFIED.lean`, `trace_Wq`, `det_Wq`).

2. **The run is literally a rotation by π/q per block.** Along the actual longest runs (q=20,30,40,50)
   the *cumulative* monodromy after k blocks has trace **exactly `2cos(kπ/q)` = `R^k`**
   (`code/Hgoal_rotation.py`): the renormalized 3-step state rotates by `π/q` per block on the invariant
   ellipse `Q'(a,b)=a²−3λab+(2λ²+1)b²` (Lean: `Wq_preserves_ellipse`, `Qp_posdef`). The product `P` is
   a quadratic form on the rotating state ⇒ a quasi-sinusoid in block-index ⇒ below thr only on a bounded
   arc ⇒ run `≈ (arc)/(π/q) ~ q`. The multi-branch word takes **3 steps per π/q rotation** (vs 1 for the
   scalar rotation), which is exactly why the multi-branch max-run (`~0.4q`) is ~3× the pure-scalar one.

3. **Elliptic ⇄ hyperbolic dichotomy via a trace polynomial (the transience, exact).** The family
   `(q−1, k₁)(q−1,0)(q−3,0)` has monodromy **trace `= λ(k₁−2)`** (Lean: `trace_family`). For
   `0<λ<2` this is `|trace|<2` (ELLIPTIC ⇒ a sustainable rotation) **iff `k₁ ∈ {1,2,3}`**, and
   `|trace|>2` (HYPERBOLIC ⇒ the orbit escapes the corridor within `O(1)` steps) for `k₁=0` or `k₁≥4`.
   `k₁=3` gives the *largest* `|trace|=λ` = the *slowest* rotation = the *longest* run — which is exactly
   the observed `W_q`. This is the transience mechanism the goal asked for, now a one-line algebraic
   dichotomy.

4. **The value `X_Ω(q)=1/λ³` is re-confirmed (no refutation).** Exhaustive search over ALL words on the
   top branches `{q−4,…,q−1}`, **digit ≤ 4, period ≤ 5** (683 036 words/q, `code/Hgoal_wordtest.py`):
   the minimal min-esssup is **exactly `1/λ³`, realized only by the cusp word `[(q−2,0)]`** (parabolic,
   trace 2). No word — including all elliptic `W_q`-type words and the *second* parabolic word
   `(q−1,1)(q−3,0)` (trace 2, value ≈0.50 ≫ thr, infeasible at q=20) — goes below thr. This *extends*
   goal-B's digit≤2 search and removes the "digit-3 was unsearched" worry.

5. **The sub-threshold set `{P<thr}`, characterized (q=16,20,30,50, `code/Hgoal_driver.py`).** Below-thr
   points live on: the **scalar branch `q−1`** (always, min `1/(1+λ)² < thr`), a **band of middle
   branches** `i ∈ [≈q/2−w, q−3]` (only for q≥16; min `x_{i-1}/(1+x_{i-2})²`, down to ~0.055 at q=50),
   and **never the cusp branch `q−2`** (`cusp_envelope`: `P≥1/λ³` there, the clean separator). The
   **deep** middle branches (near the peak `i≈q/2`) are **strongly transient**: from their low-`P` vertex
   the orbit jumps to `P≈0.3–0.7` in **one** step — they cannot chain. Only the *near-top* branch `q−3`
   participates in sustained runs (because `(…)(q−3,0)` closes the elliptic `W_q`).

---

## 1. PROVEN this session (Lean, axioms `[propext, Classical.choice, Quot.sound]`, EXIT=0)

`lean/BCZHeckeRotation_allq_VERIFIED.lean` — the **exact algebraic skeleton of the rotation mechanism**,
parametric in `l=λ`, valid for every q≥5 (uses only the universal top-branch generators
`A k=[[0,1],[−1,kl]]`, `B=[[l,l²−1],[1,l]]`, `Cc=[[1,l],[0,1]]`, `Rr=[[l,−1],[1,0]]`):

- `det_Wq`, `trace_Wq` : `W_q` monodromy is SL₂ with **trace l** ⇒ elliptic, conjugate to `R` (all q).
- `trace_family (k)` : trace of `(q−1,k)(q−1,0)(q−3,0)` is `l·(k−2)` ⇒ the elliptic/hyperbolic dichotomy.
- `Wq_entries` : explicit `[[−l,2l²+1],[−1,2l]]`.
- `trace_cusp = 2`, `det_cusp = 1`, `trace_Rr = l`, `det_Rr = 1`, `trace_secondParabolic = 2`.
- `Wq_preserves_ellipse` : `W_q` fixes the form `Q'(a,b)=a²−3l ab+(2l²+1)b²` (the renormalized rotation).
- `Qp_posdef` : `Q'` is positive-definite for `0<l<2` (genuinely an ellipse; discriminant `l²−4<0`).
- `product_le_on_ellipse`, `product_ge_on_ellipse` : the EXACT oscillation range of the product on the
  rotation ellipse `E=c²+c'²−l c c'`: `−E/(2+l) ≤ c·c' ≤ E/(2−l)`, both tight (at `c=∓c'`). The
  quantitative heart of (L1) — the rotation sweeps the product up to `E/(2−l)`, which exceeds `1/l³`
  unless `E` is tiny, and tiny `E` violates the domain.  (Trivial squares `(c∓c')²≥0`; all q.)

Reused/valid: `cusp_envelope` (all-q cusp branch `P≥1/l³`), `essSup_ge_of_no_sustained` (the engine that
(C′) feeds), `essSup_ge_of_window4`, `hecke_ground_value_pos` (½-strength uniform LB), `E_conserved_floor_one`,
the all-q cusp UB + non-attainment, q=3/4/5 sharp.

---

## 2. The mechanism, precisely (paper-level), and the reduction of (C′)

Target: **(C′) no `BCZ_q`-orbit on `𝒯^q` keeps every `P ≤ 1/λ³`** ⇒ (via `essSup_ge_of_no_sustained`)
`X_Ω(q) ≥ 1/λ³`; with the all-q cusp UB ⇒ equality + no ground state, all q.

**The corridor picture.** Away from the cusp fixed-line (where `P>thr` strictly by `cusp_envelope`),
any orbit segment that stays sub-threshold is confined to a "rotation corridor" and its renormalized
dynamics is conjugate to a power `R^m` of the fundamental rotation (trace `2cos(mπ/q)`; the slowest,
`m=1`, is `W_q`). On such a segment:
- the renormalized state rotates by `mπ/q` per block on an invariant ellipse `Q'=E'`;
- `P` restricted to the orbit is a quadratic form on the rotating state, i.e. `P = α + β·cos(2(block)·mπ/q + ψ)`;
- its maximum over the ellipse is `> thr` for every genuine (non-degenerate) `E'` — only the *parabolic
  limit* (trace → 2, the cusp word) attains `thr`. Hence within `≤` half a rotation period
  (`≤ q/m` blocks) the product exceeds `thr`: **the run is finite, `~q` steps.**

So (C′) reduces to two clean lemmas:
- **(L1) Rotation-oscillation.** On any elliptic `R^m`-conjugate regime, with the domain constraint
  `c_n+λc_{n+1}>1` forcing the invariant ellipse `E' ≥ E_min(q) > 0`, the block-max product exceeds
  `thr`. [Linear algebra on a compact ellipse + the domain lower bound on `E'`. The margin is `O(1/q²)`
  — `2−λ ≈ π²/(2q²)` — which is why it is delicate and why fixed windows fail.]
- **(L2) No regime-chaining.** An orbit cannot stay sub-threshold by *switching* between distinct
  elliptic regimes: every transition between corridors (a hyperbolic/floor "kick") itself produces a
  step with `P>thr`. [This is the genuinely open part — area-preservation alone permits invariant
  KAM-island sets inside an open region, so (L2) needs the specific corridor geometry. Numerically
  airtight: every long run is a *single* `W_q` rotation; no chained-regime sub-threshold run was ever
  found, at any q up to 80.]

(L1)+(L2) ⇒ (C′). Both are NEW, precise targets; (L1) is plausibly formalizable, (L2) is the crux.

---

## 3. NUMERICAL ledger (this session, primary-verified genuine map)

- **Value safe:** digit≤4/period≤5 exhaustive (683 036 words) at q=16,20,30 → min-esssup `=1/λ³`
  realized only by the cusp word; nothing below. (`Hgoal_wordtest.py`.)
- **Sustained word `W_q`** found at q=20,30,40,50 with itineraries `[(q−1,3),(q−1,0),(q−3,0)]^k…`;
  per-block trace `=λ` and cumulative trace `=2cos(kπ/q)` to machine precision (`Hgoal_rotation.py`,
  `Hgoal_dichotomy.py`). max-run: 4,8,11,15,20 for q=16,20,30,40,50 (`~0.4q`, finite, unbounded in q).
- **Dwell-time histograms** (`Hgoal_driver.py`): runs of length ≥3 are rare and capped per q
  (q=50: max-run 20, almost all runs length 1–2).
- **Transience depth** (`Hgoal_boundary.py`): deep middle branches exit `{P<thr}` in 1 step; only
  branch `q−3` chains.
- **Boundary (`Hgoal_boundary.py`):** the longest sustained run is **pure-scalar only at q=16**
  (run 4, branch-set `{15}`); **multi-branch `W_q` from q=17 onward** (branch-set `{q−3,q−1}`; max-run
  5,5,8,8,8,8 for q=17..22). So the *dynamical* scalar reduction — distinct from goal-F's *static*
  reduction, which already fails at q=16 because middle-branch points exist *statically* — actually
  **extends to q≤16** (those static middle-branch sub-thr points are transient and never sustained at
  q=16). The genuinely multi-branch regime is **q≥17**.
- **Transience depth (`Hgoal_boundary.py`):** from each below-thr branch's low-`P` vertex, the number of
  consecutive sub-thr steps is **exactly 1 for every deep middle branch** (`i≤q−4`) and the scalar branch,
  but **3 for branch `q−3`** (= one full `W_q` rotation block). Confirms: only `q−3` chains, and it chains
  by exactly the 3-step rotation unit.

---

## 4. OPEN / honest frontier (re-scoped, sharper than goal F)

- **(L2) "no regime-chaining"** is the single remaining nut for a q-uniform (C′). Everything else
  (the rotation structure, the elliptic/hyperbolic dichotomy, the invariant ellipse, the value) is
  exact and largely machine-checked. This is *much* sharper than goal-F's "harder than factor-2/floor".
- **(L1)** is a finite linear-algebra + domain estimate; a clean target for the next Lean push.
- The `O(1/q²)` margin (`2−λ`) is the structural reason no fixed window works and a uniform constant
  `c>½` in `hecke_ground_value_pos` is not obviously reachable by the 2-step engine — the rotation
  (multi-step) is essential.

## 5. Files
- Code: `code/Hgoal_driver.py` (chars {P<thr}, dwell, anchors), `Hgoal_itin.py`, `Hgoal_wordtest.py`
  (value re-confirmation, digit≤4), `Hgoal_symbolic.py` (sympy: trace=λ, ellipse, dichotomy),
  `Hgoal_rotation.py` (rotation-along-runs, cumulative trace = R^k), `Hgoal_dichotomy.py`,
  `Hgoal_boundary.py`.
- Lean: `lean/BCZHeckeRotation_allq_VERIFIED.lean` (NEW, all-q rotation skeleton).
- Updates: `FRONTIER_STATUS_2026-06-03.md` (goal-H entry); sharpens `FINDINGS_goalF_2026-06-03.md`
  (the "transience handle" is now the explicit rotation-by-π/q mechanism).
