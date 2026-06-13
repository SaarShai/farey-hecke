# Uniform deep-mid EJECTION — second analytic gap CLOSED (X_Ω(q) ≥ 1/λ³ route)

**Date:** 2026-06-13. **Branch:** `hecke-goalL-2026-06-03`. **Task:** close the UNIFORM deep-mid
ejection (the second analytic gap toward the uniform Hecke onset theorem `X_Ω(q) ≥ 1/λ³`).
**Code:** `code/exp_uniform_ejection_2026-06-13.py` (transience + realized box),
`code/exp_uniform_ejection_paramtest_2026-06-13.py` (decisive box sweep),
`code/exp_uniform_ejection_refine_2026-06-13.py` (worst-case + analytic form).
**Lean:** `projects/aristotle_dispatch_v15/EjectionUniform.lean` (`ejection_kick_uniform`).

> **VERDICT: HOLDS.** Uniform deep-mid ejection is a FORMAL box-widening, NOT a real obstruction.
> The verified `ejection_kick` (box `l∈[49/25,99/50]=[1.96,1.98]`, q≈16..22 only) extends to a
> SINGLE box covering **every q ≥ 16** (`l∈[49/25,2)`, `r∈[22/25,63/50]`, `thr∈[1/8,663/5000]`).
> Transience `first_window = 1` confirmed for q = 16,17,18,20,22,23,24,30,40,50,75,100,150,200.
> The parametric inequality `thr ≤ l·v² − u·v` holds on the whole widened box with worst margin
> **+0.0086 > 0**. **Lean: PROVED, axiom-clean** `[propext, Classical.choice, Quot.sound]`, no sorry.

---

## 1. Numerical verdict

### (a) Transience to q=200 — HOLDS uniformly
From the deepest sub-1/λ³ deep-mid vertex, the genuine NEXT step exceeds 1/λ³ for every q:

| q | λ | 1/λ³ | deepest branch | min P/inv | **first_window** | max run (4000 steps) |
|---|---|------|----------------|-----------|-------------------|----------------------|
| 16 | 1.96157 | 0.13249 | i=11 | 0.9778 | **1** | 4 |
| 17 | 1.96595 | 0.13161 | i=11 | 0.9523 | **1** | 1 |
| 18 | 1.96962 | 0.13087 | i=12 | 0.9270 | **1** | 1 |
| 20 | 1.97538 | 0.12973 | i=13 | 0.8760 | **1** | 4 |
| 22 | 1.97964 | 0.12890 | i=13 | 0.8265 | **1** | 2 |
| 23 | 1.98137 | 0.12856 | i=14 | 0.8024 | **1** | 2 |
| 24 | 1.98289 | 0.12826 | i=14 | 0.7809 | **1** | 1 |
| 30 | 1.98904 | 0.12708 | i=17 | 0.6661 | **1** | 2 |
| 40 | 1.99384 | 0.12616 | i=22 | 0.5311 | **1** | 2 |
| 50 | 1.99605 | 0.12574 | i=27 | 0.4402 | **1** | 2 |
| 75 | 1.99825 | 0.12533 | i=40 | 0.3073 | **1** | 2 |
| 100 | 1.99901 | 0.12519 | i=52 | 0.2356 | **1** | 2 |
| 150 | 1.99956 | 0.12508 | i=77 | 0.1606 | **1** | 2 |
| 200 | 1.99975 | 0.12505 | i=102 | 0.1217 | **1** | 2 |

`first_window = 1` everywhere: you cannot dwell on a sub-threshold deep-mid branch even one extra
step. Confirms the q=16,20,24 result of `exp_energy_cusp_numeric_2026-06-12.md` extends to q=200.
(Casorati wiring `P_i = u·v − r·v²` re-verified, `|P − (uv−rv²)| < 7e-49`.)

### (b) Realized uniform box (genuine deep-mid sub-threshold steps, q=16..200)
With `u=L_{i-1}`, `v=L_i`, `r=x_{i-2}/x_{i-1}`, `l=λ`, `thr=1/λ³`:

| quantity | realized range | Lean box (rational, ⊇ realized) |
|---|---|---|
| `l` (=λ) | [1.96157, 1.99975] | `[49/25, 2]` |
| `u` (=L_{i−1}) | [1.0000000, 1.28518] | `1 < u` (strict; min realized 1.000000004) |
| `v` (=L_i) | [0.65515, 0.99978] | `v ≤ 1` |
| `r` (=x_{i−2}/x_{i−1}) | [0.89908, 1.24671] | `[22/25, 63/50] = [0.88, 1.26]` |
| `thr` (=1/λ³) | [0.125046, 0.132492] | `[1/8, 663/5000] = [0.125, 0.1326]` |
| `l·v − u` (htop) | [0.30623, 0.97863] | `≤ 1` |
| `2l·v − u` (hbot) | [1.61395, 2.97775] | `> 1` |
| margin `l·v²−u·v−thr` | [**+0.07488**, 0.85333] | `≥ 0` required |

### (c) Parametric box sweep — HOLDS (worst margin > 0)
Sweeping the ENTIRE widened rational box (550 876 feasible cells, `u` at its worst-case = largest
feasible edge), the worst case of the quantity the proof must keep ≥ 0:

```
min (l·v² − u·v − thr) = +0.00969778   at  l=1.96, u=1.0012, v=0.6267, r=1.26, thr=0.1326
```

Fine refinement: global worst margin **+0.0086** at the `hbot`-feasibility floor `v ≈ 0.6254`.
No violation anywhere. The route SURVIVES; the lemma is TRUE on the whole box.

**Key analytic structure (drives the Lean proof).** The adversarial extreme is when the
sub-threshold premise `hP` binds (`u·v = thr + r·v²`); there the margin collapses to
```
l·v² − u·v − thr  =  (l − r)·v² − 2·thr.
```
Since `l − r ≥ 49/25 − 63/50 = 7/10 > 0`, this is `≥ 0` iff `v² ≥ 2thr/(l−r)` (i.e. `v ≥ 0.6155`).
The dangerous low-v root (`v ≈ 0.168`, where the margin is **−0.245**) is killed by **`hbot`**
(`1 < 2λv − u`): with `hu` (`1 < u`) it forces `λv > 1` hence `v > 1/2`, and `Q := r·v² − v + thr > 0`
(from `hu`+`hP`) then forces `v ≥ 0.6254`. So **`hbot` is load-bearing** — without it the inequality
is FALSE on the low-v branch. (Note: a fixed-v=1 box would have missed this; the genuine worst case
is a DEEP branch, which is why the wide box is tighter (margin 0.0086) than the q16–21 box (0.053).)

---

## 2. Lean status — PROVED (no Aristotle dispatch needed)

`projects/aristotle_dispatch_v15/EjectionUniform.lean`, theorem `ejection_kick_uniform` — identical
statement to the verified `ejection_kick`, box widened to `l∈[49/25,2]`, `r∈[22/25,63/50]`,
`thr∈[1/8,663/5000]`. Closed by a 4-step structured certificate (not a single nlinarith — the wide
box overflowed 200k heartbeats with the old hint bag):

1. `hvhalf : 1/2 < v`  from `hbot`+`hu`+`l ≤ 2`  (λv > 1 ⟹ v > 1/λ ≥ 1/2);
2. `hQ : 0 < r·v² − v + thr`  from `hu`+`hP`  (`v < u·v < thr + r·v²`);
3. `hvfloor : 62/100 ≤ v`  from `hQ`+`hvhalf`+(`r ≤ 63/50`, `thr ≤ 663/5000`)  (high-root selection);
4. final `nlinarith` from `hP`+`hvfloor`+(`l ≥ 49/25`, `r ≤ 63/50`, `thr ≤ 663/5000`).

**Build (clean rebuild after deleting the olean):**
```
⚠ [8026/8027] Built EjectionUniform (8.3s)
info: ... 'HeckeEjectionUniform.ejection_kick_uniform' depends on axioms: [propext, Classical.choice, Quot.sound]
Build completed successfully (8027 jobs).
```
`~/.elan/bin/lake build EjectionUniform`, Mathlib v4.28.0. Axioms `[propext, Classical.choice,
Quot.sound]`, **no `sorryAx`**. (Benign unused-variable warnings on `hr`/`ht`/`htop`: those
hypotheses are retained to keep the statement a drop-in superset of `ejection_kick`'s interface,
but this certificate routes through the upper bounds on `r`,`thr` + `hbot`/`hu` and does not consume
the `r`/`thr` lower bounds or the `htop` upper edge.)

---

## 3. Precise remaining obligation

This closes the **uniform deep-mid ejection** (dwell ≤ 1 on sub-threshold deep-mid branches, all
`q ≥ 16`) as a parametric box-inequality on the genuine-map quantities `(l,u,v,r,thr)`. What this
lemma does NOT by itself supply for unconditional `X_Ω(q) ≥ 1/λ³` (cross-ref
`FINDINGS_genuinemap_wiring_2026-06-05.md` §5–8, `goal1.5_uniform_obstruction.md`):

1. **Box-containment in Lean for ALL q (not just numeric).** Here the realized `(l,u,v,r,thr)`
   ranges for q=16..200 are checked numerically to lie in the rational box; a uniform Lean proof
   that the genuine deep-mid `(l,r,thr)` land in `[49/25,2]×[22/25,63/50]×[1/8,663/5000]` for every
   q (the cheb-ratio `r`-range was the part left open in the wiring findings) is still required.
   The `l`,`thr` containment was done q=16..21 (`cheb_lwin_*`, `thr_in_box_of_lwin`); the all-q `r`
   bound `x_{i-2}/x_{i-1} ∈ [0.88, 1.26]` is the new numeric input here, not yet Lean.
2. **Branch selector / cusp guard plumbing** — packaging this ejection into the multi-branch
   `genStep` symbolic dynamics (still the standing `BCZHeckeGenuineAssembly_qge18` items).
3. **The FIRST analytic gap** (the uniform L1 F-window, reduced to the 1-D trig bound
   `inner_trig_box`) is independent of this and still open over the full λ-range.

Net: the **deep-mid ejection box is no longer a `q ≥ 23` hole** — it is a single uniform lemma,
machine-verified. The transience numerics (`first_window = 1` to q=200) confirm there was never a
dynamical obstruction here; the only residual is the all-q box-containment of `r` and the assembly
plumbing.
