# Goal E — Closing q=5: a CRITICAL correction to the window-4 lemma + status

**Date:** 2026-06-03. **Headline:** the window-4 scalar lemma **as stated in the goal E brief is
FALSE**; it becomes **TRUE** only after adding the genuine Taha-domain lower-edge hypothesis
`φ·c_n + c_{n+1} > 1` (the `1−φa<b` edge of `𝒯⁵`), which the brief omitted. The `c_n≤1` cap that the
brief flagged as "essential" is **not** the load-bearing ingredient. This note records the
counterexample, the corrected statement, the proof architecture, and the formalization status.

Strict separation: **PROVEN (Lean) / NUMERICAL / CONJECTURAL**. Nothing sent outward.

---

## 0. The correction (load-bearing)

### 0a. The brief's hypothesis set is incomplete ⇒ the lemma is FALSE
The brief states the scalar object with:
- `hpos: 0<c n`, `hreg: c_n + φ c_{n+1} > 1` (branch-4 guard), `hrec` (floor recurrence),
  `hle1: c_n ≤ 1` (cap).

With **only** these, the window-4 claim "no 4 consecutive `P_n=c_n c_{n+1} < 1/φ³`" is **false**.

**Explicit counterexample** (machine-checked feasible; `code/Egoal_verify_truth.py`), floor word
`K=(K0,K1,K2)=(1,1,2)`:
```
(c0..c4) = (0.25946, 0.45768, 0.48110, 0.32070, 0.55680)      (all in (0,1], cap holds)
floors  : K0=⌊(1+c0)/(φc1)⌋=1, K1=1, K2=2  (consistent)
products: P0=0.1188, P1=0.2202, P2=0.1543, P3=0.1786   — ALL < 1/φ³=0.23607
branch-4 guards c_n+φc_{n+1}>1: 1.0001, 1.236, 1.000, 1.222  — all hold
```
So all four products are below `1/φ³` with every `hreg`/`hpos`/`hle1` satisfied. **Window-4 fails.**

### 0b. Why: the missing genuine edge
The genuine domain is Taha's `𝒯⁵ = {0<a≤1, 1−φa<b≤1}`. The lower edge `1−φa<b ⟺ φa+b>1`, i.e. in the
scalar sequence **`φ·c_n + c_{n+1} > 1` (call it `hgen`)** — DISTINCT from `hreg: c_n + φc_{n+1}>1`
(which is the branch-4 / `w₃` condition). A genuine branch-4 orbit point lies in `𝒯⁵` **and** is on
branch 4, so **BOTH** edges hold for every consecutive pair. The counterexample above violates `hgen`
(`φc0+c1 = 0.420+0.458 = 0.878 < 1`): it is on branch 4 of the *map* but **outside the genuine
triangle**, so it is not a genuine orbit point. The orbit search (which stays in `𝒯⁵`) never sees it —
hence the brief's "max run = 3" numerics were right *for genuine orbits* but the *local* scalar lemma
needs `hgen` to exclude the off-triangle witnesses.

### 0c. Corrected statement (TRUE)
> **`g5_no_four_below_genuine` (corrected).** For a scalar sequence with `0<c_n≤1`, the recurrence
> `c_n+c_{n+2}=⌊(1+c_n)/(φc_{n+1})⌋·φc_{n+1}`, **and both edges**
> `c_n+φc_{n+1}>1` AND `φc_n+c_{n+1}>1` for all `n`, no four consecutive products
> `P_n=c_n c_{n+1}` are all `< 1/φ³`.

**NUMERICAL certification** (`Egoal_verify_truth2.py`, `Egoal_lock.py`): with both edges, the
per-floor-combo minimum of `max(P_0,…,P_3)` over the feasible `(a,b)`-polygon is
```
global min-over-combos = 0.246730  >  1/φ³ = 0.236068   (margin +0.010662, at K=(2,1,2))
```
ALL-4-below is **EMPTY** (window-4 holds), **with and without** the cap `c≤1` — so the cap is
*not* the essential hypothesis; the genuine edge `hgen` is. Worst (tightest) floor words and margins:
| K=(K0,K1,K2) | min‑max P | margin |
|---|---|---|
| (2,1,2) | 0.246730 | +0.0107 |
| (1,1,2) | 0.251131 | +0.0151 |
| (2,1,1) | 0.251220 | +0.0152 |
| (1,2,1) | 0.251126 | +0.0151 |
All other feasible combos have margin > 0.04. Near-threshold floors are all ≤ 2.

---

## 1. Proof architecture (for the corrected lemma)

Pure 5-coord core `g5_core(a,b,c,d,e)` (= `c_m…c_{m+4}`), both edges on all 4 pairs, floors
`K0,K1,K2≥1` with recurrence + floor upper bounds, all four products `<1/φ³` ⟹ `False`.

1. **Engine** `P_i+P_{i+1}=K_i φ (mid)²` ⇒ each middle coord `b,c,d` has `φ⁴(mid)²<2`
   (i.e. `mid<√(2/φ⁴)≈0.540`), from `K_i≥1` and two products below.  [PROVEN in Lean — see §2]
2. **Floor bound `K0,K1,K2 ≤ 3`.** If `K_i≥4` then `φ⁴(mid)²<1/2` ⇒ `mid<0.270` ⇒ `φ·mid<0.437`;
   the edge `φ·mid+next>1` (with `next<0.540`) gives `next>0.563`, so `φ⁴next²>2`, contradicting
   `φ⁴next²<2`. Packaged as a reusable kernel `g5_floor_helper`.  [PROVEN in Lean — see §2]
3. **`interval_cases K0,K1,K2 ∈{1,2,3}` (27 cases).** Substitute `c,d,e` (linear in `a,b` at fixed
   floors). Loose combos die by the edge/positivity slack; the 4 tight combos need a degree-4
   Positivstellensatz certificate (margin ~0.01). **[the open formalization nut — see §3]**
4. Orbit form ⇒ `essSup_ge_of_window4` (verified) ⇒ `X_Ω(5) ≥ 1/φ³`; with the cusp upper bound
   (`BCZHeckeG5_genuine_VERIFIED.lean`) ⇒ `X_Ω(5)=1/φ³`; non-attainment ⇒ no ground state.

---

## 2. PROVEN (Lean, compile EXIT=0, axioms `[propext,Classical.choice,Quot.sound]`)

`lean/BCZHeckeG5_window_core_VERIFIED.lean` (3787 lines, this session):
- `g5_floor_helper`, the floor-bound section (engine identities, `(3φ+2)mid²<2`, `K0,K1,K2≤3`);
- the **27 case lemmas** `case111…case333` (every floor combo in `{1,2,3}³`), each a degree-4
  inequality discharged by an exact ℚ(φ) Positivstellensatz certificate (12–23 product terms);
- **`g5_core`** (the 5-coord pure window-4 theorem);
- **`g5_no_four_below_genuine`** (the orbit form, = the `hWin` input of `essSup_ge_of_window4`).
Prior infra reused verbatim (cusp UB, per-branch envelopes, window-4/no-sustained engines, q3/q4).

## 3. How the tight cases were closed (the resolved crux + reusable method)

The 4 tightest combos `(2,1,2),(1,1,2),(2,1,1),(1,2,1)` (margin ~0.01, irrational threshold) make a
direct `nlinarith` **time out** (degree-4 product explosion). The fix, now machine-checked:
- Work with φ as a FREE variable (`hps : phi^2 = phi+1`), NOT a `noncomputable def` — the def unfolds
  to `(1+√5)/2` and `nlinarith` whnf-times-out on `phi^3`.
- Find an **exact ℚ(φ) certificate** (not the numeric one — the √5¹ parts must separately cancel):
  build the rational matrix of [(a..e)-monomial × (φ⁰,φ¹)] coefficients of the generators (pairwise
  products + φ-scaled + recurrence×monomial), take the **sympy `.nullspace()` of the non-constant
  rows**, then a **small float-LP over the nullspace basis** (inequality-only ⇒ robust; the naive
  rigid-equality float LP is infeasible/unstable, which is why earlier degree-2/3 attempts "failed").
- Emit each used product as a φ-reduced `have … := by … linear_combination M*hps; linarith`, and close
  with one `linarith` (no product-forming). All 27 combos certify; each lemma compiles in seconds.

So the goal's contingency ("stage a dispatch package for Aristotle if it resists") was **not needed** —
the cases are closed locally and axiom-clean.

---

## 4. Files (this session)

- `code/Egoal_scalar_pretest.py`, `Egoal_casestructure.py`, `Egoal_floorbox.py`, `Egoal_relax.py`,
  `Egoal_verify_truth.py` (found the counterexample), `Egoal_verify_truth2.py` (corrected truth),
  `Egoal_lock.py` (cap-irrelevance + margins), `code/min_support.py`, `code/gen3.py` (cert search).
- `lean/BCZHeckeG5_window_core.lean` (φ-algebra + `g5_floor_helper` + floor bounds; tight cases pending).

## 5. Bottom line (strict separation)

- **PROVEN (Lean), the full corrected core — `lean/BCZHeckeG5_window_core_VERIFIED.lean`:**
  - `g5_floor_helper` + floor bounds `K0,K1,K2 ≤ 3`;
  - **all 27 floor-combo case lemmas** `case111…case333` (the degree-4 inequalities, incl. the 4
    tight ones) — each via an EXACT ℚ(φ) Positivstellensatz certificate;
  - **`g5_core`** (the 5-coord pure window-4 theorem) via `interval_cases` + dispatch;
  - **`g5_no_four_below_genuine`** (orbit form): along any genuine branch-4 scalar orbit (both Taha
    edges + cap), no four consecutive products `< 1/φ³`. This is EXACTLY the `hWin` hypothesis of the
    verified `essSup_ge_of_window4`.
  Compile EXIT=0; `#print axioms` on the case lemmas = `[propext, Classical.choice, Quot.sound]`.
- **The technique (this is the reusable contribution).** `nlinarith` cannot do the tight cases
  (degree-4, irrational threshold `1/φ³`, margin ~0.01 → product explosion / timeout). What works:
  (i) reduce φ²→φ+1 so the cert is linear in φ; (ii) find an EXACT ℚ(φ) certificate via **sympy exact
  nullspace + a tiny float-LP over the nullspace basis** (rigid-equality float LP fails — the nullspace
  removes the equalities, leaving inequality-only LP that HiGHS solves robustly), using generators
  {pairwise products, φ-scaled products, recurrence×monomial}; (iii) emit each used product as
  `have q : 0 ≤ <φ-reduced> := by have hr := mul_nonneg ..; have he : raw = reduced := by
  linear_combination M*hps; linarith [hr,he]`, then close with a single `linarith` (no product-forming).
  Scripts: `/tmp/lean-minus1/emit5.py`, `build_core.py`.
- **NUMERICAL:** corrected window-4 TRUE (both edges; cap irrelevant); counterexample shows the brief's
  statement FALSE; worst margin +0.0107 at K=(2,1,2).
- **REMAINING (capstone wiring, engines all verified):** instantiate `essSup_ge_of_window4` with
  `g5_no_four_below_genuine` ⟹ `X_Ω(5) ≥ 1/φ³` for any invariant measure confined to the scalar
  branch; combine with the per-branch envelopes (`branch2/3_envelope`, verified) for the genuine
  multi-branch reduction, the cusp upper bound (verified) for `X_Ω(5)=1/φ³`, and the non-attainment
  (`cuspSeg_no_ground_state`, verified) for no ground state. Each piece is machine-checked; the
  remaining work is the measure-theoretic glue connecting the genuine map `G5` to the scalar sequence.
- **CORRECTION to the brief:** add `hgen: φ c_n + c_{n+1} > 1`; the `c≤1` cap is NOT essential.
