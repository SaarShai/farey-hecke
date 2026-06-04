# GATE 2 (genuine multi-branch confinement) — probe episode + verification

**Date:** 2026-06-03. **Status:** preliminary signs gathered; GATE 2 NOT closed but
**reframed off the generic-KAM wall** and its hardness **localized to one named analytic
step**. Value X_Ω(q)=1/λ³ **re-verified** at q=60,70 by true-map escape. Nothing outward.

PROVEN(Lean) / NUMERICAL(verified) / OPEN strictly separated. These are NUMERICAL probes
(preliminary signs), NOT proofs.

## What GATE 2 is
Genuine `X_Ω(q)=1/λ³` for q≥18 needs: **no sustained sub-threshold genuine orbit** ⟺ the
maximal forward-invariant subset of `S={P<1/λ³}` is empty. **The wall:** the genuine BCZ_q
map is AREA-PRESERVING — confirmed exactly here: per-step Jacobian
`DT=[[X(i),X(i-1)],[X(i+1)+kλX(i),X(i)+kλX(i-1)]]`, `det DT = X(i)²−X(i-1)X(i+1) = 1`
(Chebyshev/Casorati identity, `X(i)=U_i(cos π/q)`). Area-preservation permits KAM islands ⇒
soft Lyapunov arguments cannot exclude a sub-threshold invariant set; need the group structure.

## The experiment suite (6 distinct methods)
| # | method | what it tests | code |
|---|---|---|---|
| E1 | survivor set (grid forward-invariant fixpoint) | global emptiness of max invariant set | `Igoal_survivor.py` (exists) |
| E2 | stability census (det=1 Jacobian, \|tr\| class) | is S hyperbolic except a finite-dwell rotation? | `Egate2_stability.py` |
| E2b | closed-loop / periodic-orbit search | any CLOSED sub-thr orbit = island? | `Egate2_periodic.py` |
| E3 | monodromy-word symbolic dynamics | switch ⟹ hyperbolic (proven L2); generators? | (seeded; `Hgoal_*`,`Igoal_corridors`) |
| E4 | invariant cone-field | constructive uniform expansion (Lean-friendly) | (designed) |
| E5 | Lyapunov/Foster drift | explicit V with positive drift ⟹ finite dwell | (designed; per-branch Positivstellensatz) |
| E6 | q→∞ renormalization / scaling | uniformity: control O(1/q²) escape margin | (seeded) |

## Results (NUMERICAL)
### E2 — stability census (`Egate2_stability.py`, q=18,25,40)
- Exactly **2 neutral per-step cells**, BOTH on branch q−1: `(q−1,k=1)` trace **λ** (order-q
  elliptic) and `(q−1,k=0)` trace **0** (order-2 elliptic) = **the two elliptic generators of
  G_q=(2,q,∞)**. All other 100+ cells hyperbolic (\|tr\|>2).
- ⚠ NOT uniformly hyperbolic at the boundary: q=18 has finite **elliptic length-4** composite
  stretches (\|trM\|=1.532<2). Finite elliptic stretch ≠ island (needs to CLOSE).

### E2b — closed-loop search (`Egate2_periodic.py`, q=18,25,40,60)
- q=18,25,40: **0 closed loops**. Longest sub-thr runs traverse branches **{q−1, q−3}** (=the
  2-branch corridor; confirms confinement numerically). floors {0,1,3,4} (so runs ride through
  HYPERBOLIC floor-3/4 steps too — sub-threshold ≠ neutral).
- q=60: **5 closed loops FLAGGED** (eps=2e-4), shortest = `(q−1,3)(q−1,0)(q−3,0)` repeated.

### Verification of the q=60 flag (`Egate2_verify.py`) — it was the ELLIPTIC ROTATION
- The flagged word is **W_q=(q−1,3)(q−1,0)(q−3,0)** with monodromy **trace = λ EXACTLY** (all
  q): ELLIPTIC, **rotation by π/q**, near-period **2q** (36,50,80,120,140 at q=18,25,40,60,70).
  Matches goal-H. So E2b's "loops" are near-returns of this slow rotation, NOT exact orbits.
- Rigorous **survivor_set: q=60 → 0** (no invariant set; eps-flags = ARTIFACTS). q=70 → **33**
  survivor cells (a≈b≈0.334) **with `NaN-in-cast` warnings** — the documented fine-grid failure.

### Verification of the q=70 survivor=33 flag (`Egate2_q70.py`) — ARTIFACT
- True-map escape (exact float64, no grid binning), box a,b∈[0.33,0.358], 140² seeds,
  horizon 4000: **q=70 → 17848 sub-thr seeds, max DWELL 15, 0 trapped** (all escape).
  q=60 control → max dwell 13, 0 trapped. ⇒ survivor_set=33 was a **GRID ARTIFACT**;
  **X_Ω(60),X_Ω(70)=1/λ³ STAND** (re-confirmed independently this session).

## Methodological finding (durable — record it)
At large q, **BOTH naive numeric tests FALSE-POSITIVE**: eps-closure (E2b → fake loops at q=60)
AND grid survivor_set (→ fake survivors at q=70, NaN-cast mis-binning). Only **true-map
long-horizon escape** is reliable. The shrinking escape margin (below) is what fools the cheap
tests; any GATE 2 evidence — and the eventual proof — must use true-map escape.

## What this clarifies about GATE 2 (the road)
- **Mechanism CONFIRMED:** sustained sub-thr motion = the elliptic **W_q rotation by π/q** through
  the **2-branch corridor {q−1,q−3}**, finite dwell ~q/4..q/5, then escapes (rotation carries the
  point out of (in-domain ∩ sub-thr) before a period closes). **No islands** (true-map q≤70).
- **Hardness NAMED & localized:** as q→∞ the rotation slows (angle π/q→0), dwell grows, the
  **escape margin → O(1/q²)**. Uniform GATE 2 = rigorously bound that vanishing margin. This is
  **(L1)**, OPEN, and genuinely delicate (it is *why* the cheap tests fail).
- **Route, sharpened:** finite/per-q part → **E5** per-branch drift cert (reuse proven cert tech
  `kick_pure`/window/goal-L emitter); all-q part → **E6** q→∞ parabolic-limit renormalization
  controlling the O(1/q²) margin.
- **Caveats / still open:** (L1) uniform vanishing-margin bound = the crux (unproven). The order-2
  generator `(q−1,k=0)` + hyperbolic floor-3/4 steps mean the full corridor symbolic dynamics is
  richer than two generators; (L2) covers switches (proven), the run-word combinatorics need the
  corridor symbolic dynamics machinery.

## Net
GATE 2 went from "generic 2D-KAM, no mechanism, unbounded" to: **no-islands established
(true-map q≤70), mechanism = finite-dwell π/q-rotation through the 2-branch corridor, difficulty
pinned to one named analytic step (L1: uniform O(1/q²) escape-margin)**. Value certain, freshly
re-verified. Closing (L1) is GATE 2's discovery content (the dynamics↔G_q bridge made rigorous).

## Files
`code/Egate2_stability.py`, `code/Egate2_periodic.py`, `code/Egate2_verify.py`,
`code/Egate2_q70.py`. Reused `code/Igoal_survivor.py`. Logs in `/tmp/lean-minus1/_e2*.log`.
