# q=5 (Hecke G₅) — refutation of the 4-window bound + corrected target (2026-06-02, goal C)

**Bottom line.** Goal C asked to formalize the **4-window** bound `g5_no_four_below` ("no 4
consecutive products `P_n = c_n c_{n+1} < 1/4`") as the crux of a machine-checked sharp
`X(5)=1/4` no-ground-state. The mandated numeric pre-check **refuted that bound before any Lean
grinding** (exactly the failure mode the pre-check is meant to catch). What is true:

- **X(5) = 1/4 (lower bound) is numerically solid** — no in-`D` forward orbit keeps `sup_n P_n`
  below `1/4` (min over long-horizon orbits = `0.25180…`).
- **The 4-window bound is FALSE.** There is an explicit floor-consistent, in-region
  forward-orbit segment with **all four** products `< 1/4`.
- **Longest run of consecutive sub-`1/4` products on genuine `T₅`-orbits = 4** (three
  independent methods agree). So the smallest *correct* local window is **5**, not 4.
- **The window-5 local lemma is true but has no low-degree certificate** → the sharp bound needs
  multi-step dynamics, which the q=3,4 template does not supply. (No paper proof of `X(5)≥1/4`
  exists either; FINDINGS §4 lists q=5 as "numerical+structural".)

## 1. The explicit 4-below witness (refutes window = 4)
Floors `(k₀,k₁,k₂) = (1,1,2)` — the optimizer word `(1,1,2)` entry transient. Cleanest grid hit:
```
coords (a,b,c,d,e) ≈ (0.2591, 0.4580, 0.4820, 0.3219, 0.5597)
products (ab,bc,cd,de) ≈ (0.1186, 0.2208, 0.1552, 0.1802)   ← ALL < 1/4 (max 0.2208)
```
Checks (`code/g5_escape_diagnostic.py`): recurrences `a+c=φb`, `b+d=φc`, `c+e=2φd` hold; floors
are genuinely `1,1,2`; all four region sums `> 1`; **forward** orbit stays in `D` ≥12 steps (its
next products climb: `0.327, 0.225, 0.254, 0.453, …`); **backward** there is *no* preimage in `D`
(step 0 escapes). So it is a legitimate *entry-edge* forward segment — precisely a position-`i=0`
window the measure engine `essSup_ge_of_window` must cover. Hence window = 4 cannot drive the
engine.

## 2. Max below-run = 4 (so window 5 is the corrected target)
`code/g5_sustained_search.py` (204 598 in-`D` seeds, 4 000-step horizon) and
`code/g5_maxrun_refine.py` (fine grid + recursive refinement + floor-word enumeration over
`{1,2,3}` words up to length 9) **all return longest below-run = 4**, witnessed by the `(1,1,2)`
motif. No 5-run found. Genuine optimizer orbit `c_n=R sin((n+1)π/5)` (word `(1,1,2)`, period 3):
products cycle `R²·{0.559, 0.905, 0.559}`; at `R→R_lo=0.52573…`, that is `{0.1545, 0.25, 0.1545}`
→ runs below `1/4` have length **2** (the every-3rd `0.25` peak interrupts them). The 4-run is a
pure entry transient, never sustained.

## 3. Why no fixed-window local lemma has a low-degree certificate (the connected-regime wall)
For a single pair, `bc < 1/4` together with the region `b + φc > 1` (so `b > 1 − φc`) gives
`c − φc² < 1/4`, i.e. `φc² − c + 1/4 > 0`. Its discriminant is `1 − 4·φ·(1/4) = 1 − φ < 0`, so the
inequality is **vacuous** — a single step is unconstrained. Contrast q=4: the analog is
`s²·(…)` with discriminant **0** (tangent), giving the *double root* `b = s/4` that `g4_core`
exploits (`mul_nonneg hsp.le (sq_nonneg (b − s/4))`). The q=5 region/threshold pair
`V(5)=1/4 > 1/(4λ)=(√5−1)/8` is the *connected* regime (FINDINGS §5/T7): the sub-`1/4` region and
the cusp line do not pinch, so one-step geometry cannot force the product up. The window-5 bound is
true only through the multi-step rotation: over 6 coords the floor-1 recurrence rotates by
`5·36°=180°`, sweeping past the product peak `= φ²·E` (conserved `E`); combined with the region
lower bound on `E` this pins one of the 5 products `≥ 1/4`. That is a genuine dynamical argument,
not a fixed-window `nlinarith`.

## 4. What was machine-checked instead (honest, sorry-free, axiom-clean)
`lean/BCZHeckeG5_lowerbound_VERIFIED.lean` (Lean v4.28.0, exit 0; `#print axioms` =
`[propext, Classical.choice, Quot.sound]` on every theorem):
- `g5_value` : `φ/(2(1+φ)²) = (√5−2)/2` (exact closed form; `2(1+φ)² = 7+3√5`).
- `g5_no_sustained_lb` : no `T₅`-orbit keeps every product `≤ (√5−2)/2` (instantiation of the
  proven all-q engine `hecke_ground_value_pos` at `λ=φ`).
- `essSup_ge_of_no_sustained` (new abstract engine) + `essSup_g5Product_ge` : any `g5Map`-invariant
  probability measure on `g5Triangle` has `ess-sup P ≥ (√5−2)/2`.

So **X(5) ≥ (√5−2)/2 ≈ 0.11803** is now machine-checked. Ordering:
`(√5−2)/2 ≈ 0.118  <  1/(4λ)=(√5−1)/8 ≈ 0.1545  <  V(5)=1/4`. This is the *general* positive
ground value at q=5, **not** the sharp value.

## 5. Status ledger (strict separation)
- **PROVEN (Lean, axiom-clean):** `X(5) ≥ (√5−2)/2 > 0` (scalar + measure form). [this session]
- **NUMERICAL:** `X(5)=1/4`; longest below-run = 4; window-5 bound holds; window-4 bound FALSE.
- **CONJECTURAL / not formalized:** sharp `X(5) ≥ 1/4` and the sharp no-ground-state. Needs the
  multi-step dynamics (window 5 + conserved-`E` rotation peak); no paper proof exists.
- **RETRACTED from goal C as posed:** `g5_no_four_below` (4-window) — refuted; do not formalize.

## 6. Corrected route (the real, harder target — staged, not done)
To reach sharp `X(5)=1/4` one must prove, in Lean, the **window-5** local lemma (6 coords, 4 floors)
*using* `E_conserved_floor_one` (already proven) to lower-bound the swept product peak on floor-1
runs, plus q=4-style defect cases for floors `≥2`. Then a window-5 engine
(`essSup_ge_of_window` generalized to a 5-element `max`) + a `1/4`-point exclusion lemma yields
`g5_no_ground_state`. This is a multi-session formalization and a genuine research result; the
all-floor-1 sub-case is the natural first Aristotle dispatch (USER-gated — not submitted).

## 7. Files
`code/g5_window_precheck.py` (optimizer family + direct `g5_core` feasibility → found 4-below),
`code/g5_escape_diagnostic.py` (forward/backward extension → entry-edge artifact),
`code/g5_sustained_search.py` (max below-run=4, min sup=0.2518),
`code/g5_maxrun_refine.py` (3-way confirmation of max-run=4),
`lean/BCZHeckeG5_lowerbound_VERIFIED.lean` (the machine-checked positive bound).
