# Track A — sharp lower bound + no-ground-state for q=5,6 (goal A), and the uniform-window verdict

**Date:** 2026-06-02. **Scope:** feasible Hecke range, focus q=5 (Lean target) and q=6.
Companion to `FINDINGS_corrected_2026-06-02.md` (feasibility ≤11), `CLOSED_FORM_Xq.md` (V(q)),
`HeckeGeneralLB_VERIFIED.lean` (E-engine), `BCZHecke_noGroundState_q3q4_VERIFIED.lean` (q=3,4 template).

Object: `λ=λ_q=2cos(π/q)`, `T_q(x,y)=(y, ⌊(1+x)/(λy)⌋λy−x)` on `D={x>0,y>0,x+λy>1}`, `P=xy`,
`X(q)=inf_μ ess-sup_μ P`. Goal: `X(q)=V(q)` unattained (no ground state), via the **Lemma**
`G'_q := {orbits in D with all P_n ≤ V(q)} = ∅` (gives both `X(q)≥V(q)` and non-attainment).

---

## 0. HEADLINE — the goal's "rotation-sweep window = q−2" hypothesis is REFUTED (numerics)

The goal proposed: *a rotation run of length ≥ N=q−2 forces a product ≥ V(q)*, uniform in q.
**This is false.** Measured longest run of consecutive in-D products `< V(q)` (the strict sub-V run;
`code/maxrun_hillclimb.py`, `code/rotation_sweep_probe.py`, mpmath, hard random+hill-climb search):

| q | q−2 | measured max sub-V run W*(q) | mechanism |
|---|-----|------------------------------|-----------|
| 5 | 3 | **4** | rise→defect→rise, 2nd peak exceeds |
| 6 | 4 | **5** | same |
| 7 | 5 | **7** | |
| 8 | 6 | **8** | |
| 9 | 7 | **10** | |
| 10 | 8 | **11** | |
| 11 | 9 | **13** | |

Pattern `W*(q) = (q−2) + ⌊(q−2)/2⌋ − [q even] ≈ 3(q−2)/2`, NOT `q−2`. So the forcing window is
`W*(q)+1 ≈ 3(q−2)/2+1`. **Why the goal's q−2 fails:** a transient orbit can rise to a near-peak
*just below* V (e.g. q=11 reaches 0.9995·V), descend through the lone defect (floor 2), and rise
again — only the *second* peak (≈ one period = q−2 steps later) is forced strictly above V. The first
near-peak plus the descent arc add ≈ half a period, giving ≈ 3(q−2)/2. The orbit is NOT the periodic
family (which has a strict >V peak every period and so cannot sustain a long sub-V run): it is a
non-periodic transient that shadows the family near the cusp limit point and then escapes D.

**Consequence for the proof.** The lower bound genuinely needs (i) a window bound of length ≈3(q−2)/2
(NOT q−2), and (ii) handling of the defect's change to the conserved E across the run. The clean
*uniform* rotation-sweep as envisioned does not close; see §4 for the precise blocker. The runs are
**bounded** under hard search (no infinite sustain) — consistent with the Lemma being true for q≤11.

---

## 1. The two-part proof skeleton (rigorous, q=5; same shape ∀ feasible q)

`G'_q = ∅` follows from two facts:

- **(W) Window bound** = the lower bound `X(q)≥V(q)`: *no `W=W*(q)+1` consecutive in-D products are
  all `< V(q)`* (equivalently every in-D orbit has `sup P ≥ V`). With "all `P_n ≤ V`" this forces an
  **exact t-point** `P_m = V` in every window. For q=5, `W=5` (since `W*(5)=4`).
- **(X) t-point exclusion:** *no exact t-point `P_m=V` can sit in an orbit that stays in D with all
  `P_n ≤ V` forward.* RIGOROUS for q=5 (§2), verified `code/q5_exclusion_verify.py` (0 fails / 2·10⁵
  t-points, definite margins). Together: a t-point exists (W) but is excluded (X) ⇒ `G'_q=∅`. ∎

(This mirrors q=3: `WindowBound` (the v8/cluster 3-window theorem) + `not_two_ninths_at` (t-point
exclusion) ⇒ `exists_product_gt_two_ninths` ⇒ `no_ground_state`.)

---

## 2. q=5 t-point exclusion (X) — RIGOROUS

`λ=φ=(1+√5)/2`, `φ²=φ+1`, `V=1/4`. Band: with all `P_n≤1/4`, the engine `φ·c_{n+1}² ≤ P_n+P_{n+1}
≤ 1/2` gives every coordinate `c_n ≤ b:=√(1/(2φ))`. At a t-point `(x,y)=(c_m,c_{m+1})`, `xy=1/4`,
`x,y≤b`, so `y = 1/(4x) ≥ 1/(4b) = a := √(φ/8)`, i.e. `x,y ∈ [a,b]`, `ab=1/4`, `a=0.44973…`,
`b=0.55589…`. Let `k=⌊(1+x)/(φy)⌋ ≥ 1` (the forward floor) and `z := c_{m+2} = kφy − x`.

**Case I (k ≥ 2): immediate exceed.** `P_{m+1} = yz = kφy² − xy = kφy² − 1/4 ≥ 2φy² − 1/4`.
From `x²≤1/(2φ)` and `x=1/(4y)`: `y² ≥ φ/8`, so `φy² ≥ φ²/8 = (φ+1)/8` and `2φy² ≥ (φ+1)/4`. Thus
`P_{m+1} ≥ (φ+1)/4 − 1/4 = φ/4 > 1/4` (as `φ>1`). Contradiction with `P_{m+1}≤1/4`. ✓
*(margin ≥ φ/4 − 1/4 ≈ 0.1545 over the whole k=2 band.)*

**Case k=1 ⇒ hreg forces y > 1/2.** `z=φy−x`. The domain `hreg` at `m+1` reads `y+φz>1`, i.e.
`(1+φ²)y − φx > 1`, i.e. `(φ+2)y − φx > 1` (using `φ²=φ+1`). With `x=1/(4y)`, multiply by `4y>0`:
`4(φ+2)y² − 4y − φ > 0`, which factors as `4(φ+2)(y−½)(y + φ/(2(φ+2))) > 0`. The second factor is
`>0` for `y>0`, so **the domain constraint is equivalent to `y > 1/2`.** Hence a floor-1 t-point with
`y ≤ 1/2` violates `hreg` (cannot occur); in particular the symmetric limit point `(½,½)` is excluded
(its image lands exactly on `∂D`: `x+φy=1`). So Case k=1 ⇒ `y∈(½, b]`.

**Case III (k=1, y∈(½,b]): exceed within ≤ 2 more steps.** Here `z=φy−x`, `P_{m+1}=φy²−1/4 (≤1/4)`,
and the next floor `k₁=⌊(1+y)/(φz)⌋ = 2` throughout `(½,b]` (both floor bounds hold:
`2(2φ+1)y²−2y−φ ≤ 0` gives `k₁≥2`, and `y>½ ⇒ ratio<3` gives `k₁<3`). Let `w=c_{m+3}=2φz−y`,
`P_{m+2}=zw=2φz²−P_{m+1}=2φz²−φy²+1/4`.
- **(IIIa) `2z² > y²`** (holds for `y ≳ 0.5238`, i.e. quartic `8(2φ²−1)y⁴−8φy²+1>0`):
  `P_{m+2} = 2φz²−φy²+1/4 > 1/4`. ✓ (total 2 steps past the t-point).
- **(IIIb) `2z² ≤ y²`** (`y∈(½, 0.5238]`, the dip): `P_{m+2}≤1/4`; one more step. The next floor
  `k₂=⌊(1+z)/(φw)⌋=1`, `c_{m+4}=φw−z`, `P_{m+3}=φw²−P_{m+2} > 1/4`. ✓ (total 3 steps).

So **every t-point in an all-`≤1/4` in-D orbit forces a forward product `> 1/4`** within ≤3 steps —
contradiction. The closing margins (Cases II,III) `→0` as `y→½⁺`: this is exactly the
**non-attainment** — the infimizing family lands on `∂D` at `(½, 1/(2φ))` as `s→s_lo⁺`. ∎ (X for q=5)

**Numerical certification:** `code/q5_exclusion_verify.py` — 0 fails over 2·10⁵ t-points; min margins
I=0.1545, II=1.6·10⁻⁶, III=1.4·10⁻⁶ (II,III shrink near y=½ as expected); max forward steps = 3;
the floor-2→1 switch is at `y*=0.47251…<½`, the successor-in-D boundary is **exactly `y=½`**.

---

## 3. q=6 (even q) — parallel structure

`λ=√3`, `V=√3/6=0.288675…`, `maxprod=cos(π/6)=√3/2` (even-q branch — the orbit misses the ellipse
symmetric point). Coordinate bound `c_n≤b=√(2V/λ)=√(1/(2λ))·…`; here `b²=2V/λ=2·(√3/6)/√3=1/3`, so
`b=1/√3=0.57735`; t-point band `[V/b, b]=[½, 1/√3]` (note the band BOTTOM is exactly `½`, vs `a>½`
internal for q=5). Limit point still `(½, 1/(2λ))=(½, 1/(2√3))`. `W*(6)=5` (numeric). The t-point
exclusion runs the same way (floor-2 immediate-exceed branch + floor-1 domain-forced branch + a short
forward sweep), with `λ²=3` arithmetic in place of `φ²=φ+1`. **Status: paper structure identical to
q=5; the explicit per-branch inequalities are not yet hand-checked to the q=5 standard — pending.**

---

## 4. The uniform blocker (precise) — why q=5..11 are not one clean theorem

The conserved `E=c_n²+c_{n+1}²−λc_nc_{n+1}` (Lean `E_conserved_floor_one`) gives `P_n = λ²[E−(c_n−
c_{n+1})²]/(…)` and `max_E P = E/(2−λ)`; on the cusp-pinned ellipse `E*=1/(4λ²)`, `E*/(2−λ)=V` for
**odd q** (for even q the discrete orbit misses the ellipse max, so `V<E*/(2−λ)`). The rotation-sweep
would conclude "a floor-1 run reaches the symmetric point ⇒ `P≥E/(2−λ)≥V`." **Two gaps, both real:**
1. **Discreteness.** The orbit samples the ellipse at rotation-phases `θ=π/q` apart; it can *step over*
   the symmetric point without landing within `√(E−E*)` of it, so a finite floor-1 run need not realize
   `P` close to `E/(2−λ)`. Controlling the phase is q-specific.
2. **The defect changes E.** A sub-V orbit is not a single rotation: the lone floor-2 defect resets the
   ellipse `E1→E2`, and the cusp pin ties `E1,E2` so that only the *post-defect* peak (≈ one period
   later) is forced `>V`. This is the source of the `W*≈3(q−2)/2` window (§0), and it has no
   single-step / single-ellipse description.

Hence the lower bound is **per-q** (finite t-point exclusion with a q-growing number of forward steps,
≈ up to `⌈(q−2)/2⌉`, and a window bound of length `≈3(q−2)/2`). The E-engine is a genuine tool
(gives the clean Case-I coordinate bound and the `E*↔V` identity) but does not by itself close the
discreteness/defect gaps. **Verdict: deliver q=5 (rigorous, below) and q=6 (structure), and record
the blocker; do NOT claim a uniform rotation-sweep theorem.**

---

## 5. Status ledger (strict separation)

- **RIGOROUS (paper, this file):** q=5 t-point exclusion (X) — §2, every inequality reduced to
  `φ²=φ+1` algebra, numerically certified 0-fail with margins. The proof skeleton (W)+(X) (§1).
- **NUMERICAL (high-precision, hard search):** window lengths `W*(q)` q=5..11 (§0); the window bound
  (W) for q=5 (`X(5)≥1/4`, i.e. no 5 consecutive in-D products `<1/4`) — `W*(5)=4` robust; runs are
  bounded (no infinite sustain) for all q=5..11.
- **OPEN / not yet done:** (W) the q=5 window bound as a *hand/Lean* proof (the 6-coordinate floor-case
  inequality — the laborious analytic piece, analog of q=3's machine-checked v8 cluster bound);
  q=6 explicit inequalities; q=7..11 (same template, longer); the uniform theorem (blocked, §4).
- **RETRACTED:** the goal's "uniform window = q−2" hypothesis (refuted, §0).

Nothing sent outward. Lean target (q=5 machine-check) tracked separately in `lean/`.
