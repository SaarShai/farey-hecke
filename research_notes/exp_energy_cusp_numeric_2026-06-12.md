# Adversarial numeric test of Koyama's energy x cusp-escape route to X_Ω(q) ≥ 1/λ³

**Date:** 2026-06-12. **Task:** INV-numeric-falsify. **Branch:** `hecke-goalL-2026-06-03`.
**Code:** `code/exp_energy_cusp_numeric.py` (v1, pointwise — flawed proxy, kept for the record),
`code/exp_energy_cusp_v2.py` (corrected per-branch / cusp / onset), `code/exp_transience_q16.py`
(dwell test). Outputs in `code/out/exp_energy_cusp_*.json`. Map: canonical Taha G_q-BCZ
(`code/goal1_*.py`), reproduces q=3 BCZ and the cluster anchors.

> **VERDICT (one line).** The route is **numerically SUPPORTED for the *value* X_Ω(q)=1/λ³**,
> but the **CUSP (itinerary) side is the entire load-bearing content; the CONSERVED ENERGY E
> does NOT supply the lower bound at all** — it supplies *finiteness of corridors*, not the
> floor 1/λ³. Koyama's "boundary behavior of E" is not where the infimum lives: the infimum
> is pinned by the **cusp-branch envelope** `P = a(a+λb)/λ ≥ 1/λ³` (branch i=q−2), an
> itinerary/geometry fact, with the energy invariant playing a *disjoint* role (corridor
> finiteness). So the coupling as Koyama frames it ("couple E-boundary with cusp-escape rate")
> is **misattributed**: cusp does all the lower-bound work; energy does the *upper*-side
> finiteness work. Below q=16 the two even decouple cleanly; at q≥16 the per-branch floor
> *fails* and only **transience** (dynamics can't dwell on the sub-1/λ³ middle branches) saves
> the value — and transience is again an itinerary fact, not an energy fact.

---

## 0. A methodological correction (adversarial self-check)

A naive reading of "min P → 1/λ³" is WRONG and I falsified it on myself first
(`exp_energy_cusp_numeric.py` v1). The **pointwise** orbit-minimum of `P = a·b` is **~10⁻⁴**
for every q (ratio to 1/λ³ ≈ 0.0002–0.002): a single ergodic orbit dives arbitrarily deep
into the cusp (`a·b → 0`) on a measure-zero set. So `inf over the orbit of P` is 0, not 1/λ³.

The object that equals 1/λ³ is **X_Ω(q) = inf_μ ess-sup_μ P** (inf over *invariant measures*
of the *essential* supremum). The cusp dives are measure-zero and invisible to ess-sup; the
infimum is realized by the **cusp periodic orbit**, where ess-sup P = (1/λ)²/λ = 1/λ³ exactly.
The "onset/X ~ 1.003" margin lives in the **cluster-onset threshold**, not in any pointwise P.
All numbers below use the correct objects.

---

## (a)(i) + (b) — the value 1/λ³ and how it is approached

**Cusp-periodic value (the realizer of X_Ω).** On the cusp branch the orbit grazes the cusp
vertex `(s,0)` with `s → (1/λ)⁺`, giving ess-sup `P = s²/λ → 1/λ³` exactly, for **every q**
(ratio 1.00000 to machine precision, `exp_energy_cusp_v2.py` block C). So the *upper bound*
`X_Ω ≤ 1/λ³` is exact and uniform — never in doubt.

**Cluster-onset proxy** (largest threshold `T` keeping {P<T} runs at the empirical ceiling;
`onset/inv` is the "1.003" object). This approaches **1 from above**:

| q | 3 | 4 | 5 | 6 | 7 | 8 | 10 | 12 | 16 | 20 |
|---|---|---|---|---|---|---|----|----|----|----|
| onset / (1/λ³) | (X=2/9)* | 1.00023 | 1.00316 | 1.00077 | 1.00115 | 1.00827 | 1.00735 | 1.00142 | 1.00561 | 1.01408 |

(*q=3,4 use X(q)=2/9, √2/8 ≠ 1/λ³, the arithmetic interior values; for q≥5 X=1/λ³.) The
margin is small (≤1.4% through q=20) and **does not monotonically shrink like 1/q²** — it
wiggles (1.003 at q=5, 0.0008 at q=12, 1.4% at q=20). It is *from above* and *O(small)*,
consistent with X_Ω=1/λ³ as the onset, but I could **not** confirm a clean `1+c/q²` law;
the approach is non-monotone (sampling noise + the genuine ~q/3 window growth both contribute).
**Honest:** "margin ~ O(1/q²)" is NOT supported; "margin small & positive, onset from above"
IS supported.

## (a)(ii) — corridor (floor-1 / rotation run) lengths; where is the infimum hit?

Floor-1 (K=1, pure-rotation, energy-conserving) corridor-length distribution along genuine
orbits (`exp_energy_cusp_numeric.py`):

| q | 3 | 4 | 5 | 6 | 7 | 8 | 10 | 12 |
|---|---|---|---|---|---|---|----|----|
| max corridor len | 1 | 2 | 3 | 4 | 5 | 6 | 8 | 9 |
| mean corridor len | 1.00 | 1.61 | 2.36 | 2.81 | 2.87 | 2.82 | 2.69 | 2.59 |

Max corridor length grows ≈ q/3 (matches FINDINGS_goalF window). **Where does P dip below
1/λ³?** Classifying every sub-1/λ³ step as INTERIOR (K=1 with both neighbours K=1, pure
rotation) vs BOUNDARY (a K≥2 "kick" at or adjacent):

| q | 3 | 4 | 5 | 6 | 7 | 8 | 10 | 12 |
|---|---|---|---|---|---|---|----|----|
| boundary-fraction of sub-1/λ³ steps | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.999 | 0.998 |

**~100% of the sub-threshold mass sits at corridor BOUNDARIES (cusp entry/exit, the K≥2 kick),
NOT in the pure-rotation interior.** This is the one place the data *agrees* with Koyama's
phrase "boundary behavior" — the extreme gaps occur where a rotation corridor meets a high-floor
kick (the cusp excursion), exactly as "boundary behavior of E" would suggest. BUT: this is the
boundary of the *corridor in the cusp direction*, governed by the **floor jump K** and the
cusp-branch geometry — the conserved E is the thing that is constant *across* the interior and
says nothing about the boundary value (see (c)/(d)).

## (a)(iii) — escape-of-mass rate

| q | 3 | 4 | 5 | 6 | 7 | 8 | 10 | 12 |
|---|---|---|---|---|---|---|----|----|
| frac time "near cusp" (P<2/λ³) | 1.00 | 0.93 | 0.74 | 0.63 | 0.58 | 0.56 | 0.54 | 0.53 |
| frac time with a kick (K≥2) | 0.667 | 0.333 | 0.255 | 0.222 | 0.205 | 0.195 | 0.184 | 0.179 |

Kick-fraction (excursions out of pure rotation) **decreases** with q toward ~1/6, i.e.
corridors get longer so kicks get rarer — consistent with the ~q/3 window. Deepest-excursion
P/(1/λ³) over the run-length histogram is dominated by the measure-zero cusp dives (≈10⁻³),
again not the right object; the *cluster onset* (a)(i)/(b) is the honest escape-rate summary.

---

## (c) — THE CRUX: energy-feasible-but-itinerary-infeasible region

**Setup.** On a floor-1 corridor the orbit obeys `c_{n+2}=λc_{n+1}−c_n` and conserves
`E = c_n²+c_{n+1}²−λ c_n c_{n+1}` (the Lean `E_conserved`). The observable on the last
(classical) branch is `P = c_n c_{n+1}`. **Question:** does the conserved-energy constraint
ALONE force `P ≥ 1/λ³`?

**Answer: NO — emphatically.** On the energy ellipse `{c²+d²−λcd=E, c,d>0}` the product
`P=cd` ranges over `(0, E/(2−λ)]`. The lower end is **0** (slide the pair toward a coordinate
axis), and even the *dynamically realized* lower envelope of an actual rotation corridor is
`E/(2+λ)`, which is **far below 1/λ³** for every q:

| q | λ | E (sample corridor) | corridor min P=cd | E/(2+λ) | **1/λ³** |
|---|---|---|---|---|---|
| 5 | 1.618 | 0.463 | 0.270 | 0.128 | 0.236 |
| 6 | 1.732 | 0.432 | 0.270 | 0.116 | 0.192 |
| 7 | 1.802 | 0.413 | 0.270 | 0.109 | 0.171 |
| 8 | 1.848 | 0.401 | 0.270 | 0.104 | 0.159 |

On a *pure rotation corridor* (energy conserved exactly) **12%–20% of the steps have
`P = cd < 1/λ³`** — energy conservation produces sub-threshold products *freely*. So:

> **The conserved energy E does NOT lower-bound P. Energy ALONE permits P arbitrarily below
> 1/λ³.** The energy-feasible region for P is `(0, E/(2−λ)]` ∋ values `< 1/λ³`. The lower
> bound P ≥ 1/λ³ therefore CANNOT come from E; it must come from the ITINERARY — specifically
> the cusp-branch envelope.

**Where the 1/λ³ floor actually lives (the cusp-branch envelope, Lean-verified).** Per-branch
min of the genuine observable `P_i = a·L_i/x_{i-1}`, closed form `min P_i = x_{i-1}/(1+x_{i-2})²`:

- **Cusp branch i=q−2:** `min P = 1/λ³` **exactly, for every q** (ratio 1.000000, all q
  tested 4..20). This is `cusp_envelope` in
  `koyama_packet_2026-06-12/lean/BCZHeckeCusp_envelope_allq_VERIFIED.lean`, tight at the cusp
  vertex `(1/λ,0)`. **The lower bound is a CUSP fact, full stop.**
- **Non-cusp middle branches:** `min P_i ≥ 1/λ³` holds for `5 ≤ q ≤ 15`, then **FAILS at q=16**
  (branch i=10, min P_i/(1/λ³) = 0.9778), and the violation grows: q=20 reaches 0.876, q=24
  reaches 0.781 (independently reproduced here; matches FINDINGS_goalF q=16 first-failure
  witness `(a,b)≈(0.7857,−0.5412)`, P≈0.13036 < 1/λ³≈0.13249).

**This is precisely the "energy-feasible-but-itinerary-infeasible" region** the task asked to
construct, and it exists for **q ≥ 16**: those middle-branch points are geometrically admissible
(in the domain, on a genuine branch, energy-consistent) with `P < 1/λ³`, yet the bound still
holds for X_Ω because the dynamics cannot **dwell** there:

**Transience test (`exp_transience_q16.py`).** Starting AT the deepest sub-1/λ³ middle-branch
vertex, the forward genuine orbit:

| q | deepest branch | start P/(1/λ³) | consecutive steps below 1/λ³ from vertex | max run (2000 steps) |
|---|---|---|---|---|
| 16 | i=10 | 0.978 | **1** | 2 |
| 20 | i=13 | 0.876 | **1** | 4 |
| 24 | i=14 | 0.781 | **1** | 1 |

The *very next* genuine step already exceeds 1/λ³ (`first_window=1`). You cannot sit on the
sub-threshold middle branch — the map kicks you out immediately. So `ess-sup_μ P ≥ 1/λ³` is
preserved **dynamically**, by transience, NOT by any per-step lower bound and NOT by energy.

---

## (d) — Which coupling is load-bearing? (the verdict on Koyama)

Decompose Koyama's proposed coupling "E-boundary × cusp-escape rate":

| ingredient | what it actually delivers | load-bearing for X_Ω ≥ 1/λ³ ? |
|---|---|---|
| **Conserved E** (NoInfiniteRotation core) | corridors are FINITE (no infinite rotation); orbit bounds `c_n ≤ M`, `c_{n+1}+c_{n+2} ≥ m` | **NO for the lower bound.** It bounds the *length* of a sub-threshold run (the q/3 window), i.e. it gives FINITENESS, not the floor. Its own lower envelope `E/(2+λ)` sits *below* 1/λ³. |
| **Cusp-branch envelope** `P=a(a+λb)/λ ≥ 1/λ³` | the lower bound on the optimiser's branch (i=q−2), tight at the cusp vertex | **YES — this IS the bound.** Uniformly true (Lean-verified all q). |
| **Transience** (kick out of low-P middle branches) | for q≥16 where per-branch floor fails, dynamics can't dwell sub-1/λ³ | **YES for q≥16** — itinerary fact, the multi-branch generalization of the cusp argument. |

**So the load-bearing object is the CUSP/itinerary side, in two layers:** (1) the cusp-branch
envelope (q-uniform, proved), and (2) transience on the non-cusp branches for q≥16 (numerical,
the open multi-branch piece). **The energy invariant is genuinely useful but for the OTHER half
of the problem** — it is the mechanism behind `no_infinite_rotation` (finiteness of the
sub-threshold run / the upper bound on cluster length), which is necessary to turn the
pointwise cusp envelope into a statement about `ess-sup_μ`. It does *not* and *cannot* supply
the 1/λ³ value.

**Where Koyama's framing is right, and where it is off:**
- RIGHT: extremes occur at corridor BOUNDARIES / cusp entries ((a)(ii): ~100% boundary), so
  "boundary behavior" is the correct locus, and "couple with escape-of-mass into the cusp" is
  the correct mechanism for the *finiteness*/no-dwelling half.
- OFF / MISATTRIBUTED: "the natural route lies *within* the conserved energy E" for the lower
  bound. The energy E never sees 1/λ³ (its feasible P-range includes 0 and its corridor floor
  is E/(2+λ) < 1/λ³). The 1/λ³ is a **cusp-branch geometry** constant. A transfer-operator
  spectral constraint built only from E would bound *spreading/finiteness*, not the floor.

**Does the route CLOSE the uniform bound? — Not as stated, and a real gap remains.**
- For **q ≤ 15**: the value closes via the cusp envelope + per-branch envelope (every branch
  ≥ 1/λ³) + corridor-finiteness (the E-driven window) — all Lean-provable per-q, cusp piece
  already all-q. Energy's role here is only finiteness.
- For **q ≥ 16**: the per-branch envelope is **FALSE** (middle branches dip below 1/λ³), so the
  clean reduction breaks. The bound survives **only by transience** — a genuine **multi-branch,
  dynamical** statement that is currently **numerical only** (`first_window=1`, max run ~q/3).
  Coupling energy-boundary to cusp-escape via a transfer operator is a *plausible vehicle* for
  formalizing this transience, but (i) the spectral object must encode the cusp-branch geometry
  (not just E), and (ii) the "can't dwell on sub-1/λ³ middle branches uniformly in q" claim is
  exactly the open KAM-type / discreteness obstacle flagged in `goal1.5_uniform_obstruction.md`
  FINDING 3 — Koyama's route does not by itself remove it.

---

## Summary table — is the route numerically supported?

| claim | supported? | evidence |
|---|---|---|
| X_Ω(q) = 1/λ³ as a *value* (uniform) | **YES** | cusp-periodic ess-sup = 1/λ³ exact all q; cluster-onset from above (1.0002–1.014) q≤20 |
| margin → 1 like O(1/q²) | **NO (not confirmed)** | onset/inv non-monotone (1.003 @ q5, 0.0008 @ q12, 1.4% @ q20) |
| extremes at corridor boundary (cusp entry) | **YES** | ~100% of sub-1/λ³ steps are boundary/kick steps, ~0% pure-rotation interior |
| conserved E supplies the lower bound 1/λ³ | **NO** | energy-feasible P ∈ (0, E/(2−λ)]; corridor floor E/(2+λ) < 1/λ³; 12–20% of rotation steps are sub-1/λ³ |
| cusp-branch envelope supplies 1/λ³ | **YES (Lean-verified)** | min P on i=q−2 = 1/λ³ all q, tight at cusp vertex |
| per-branch floor ≥ 1/λ³ (the easy reduction) | **q≤15 only** | FALSE from q=16 (branch i=10, ratio 0.978), grows to 0.78 @ q=24 |
| q≥16 saved by transience (itinerary) | **YES (numeric)** | from deepest vertex, next step exits sub-1/λ³ (first_window=1); max run ~q/3 finite |

**Bottom line for the workflow:** Koyama's energy×cusp route is **half-right and
mislabeled**. The **cusp (itinerary) half is load-bearing for the lower bound** and is the
already-proven uniform piece (cusp_envelope). The **energy half is load-bearing for the
*other* requirement (corridor finiteness / no infinite rotation)**, not for 1/λ³. The genuine
open gap is the **q≥16 multi-branch transience** (the per-branch envelope fails), which is an
itinerary/discreteness statement; the energy invariant does not close it, and "boundary
behavior of E" is not where the infimum 1/λ³ comes from.
