# Priority-Nesting Probe: Farey vs Dyadic vs WFQ

**Date:** 2026-06-05
**Simulation:** `priority_nesting_probe.py`
**Verdict:** LEAD SURVIVES (narrowly). The one non-dominated result in the
silent-coordination corpus. Farey beats the natural drop-in alternative
(dyadic) at priority-proportional bandwidth allocation for heavy-tailed /
continuous priority distributions — at a real and N-growing min-gap (drift) cost.

---

## What was tested

The single unrefuted lead from the corpus: **heterogeneous slot sizes with
nested, non-disruptive, zero-communication growth.** Uniform TDMA gives every
agent the same slot (no priority). Dyadic bisection gives power-of-two slot
sizes. Farey/Stern-Brocot gives a continuum of nested slot sizes. WFQ gives
exact proportional allocation but must repartition (disruptive / needs comms).

Channel = circle [0,1); each placed point owns the arc to its next neighbor
(= its bandwidth share). Largest weight assigned to largest available arc
(identical fair procedure for all schemes).

- **EXP1 (proportionality):** static N-agent population, weights ~ {uniform,
  two_class, zipf, lognormal}. Metric: TV distance of actual shares from ideal
  `w_i/W` (lower=better; WFQ=0). Plus worst-case relative error and min-arc.
- **EXP2 (disruption):** agents arrive 1..N; count position MOVES per join
  (a move = recompute => needs communication).

## Results

**Head-to-head TV(Farey)/TV(dyadic)** — <1 means Farey better:

| dist | N=16 | N=50 | N=100 | N=200 |
|------|-----:|-----:|------:|------:|
| uniform   | 10.31 | 2.49 | 2.74 | 2.94 |  (dyadic wins — but uniform = no priority)
| two_class | 0.67 | 0.98 | 0.89 | 0.88 |  (≈tie, slight Farey)
| zipf      | 0.41 | 0.42 | 0.36 | 0.33 |  (**Farey ~2.5–3× better**)
| lognormal | 0.71 | 0.84 | 0.78 | 0.77 |  (Farey ~20–30% better)

**Worst-case relative error** (how badly the most-misserved agent is treated):
- zipf N=100: Farey 0.60 vs dyadic 3.05 (**5× better**)
- lognormal N=200: Farey 4.6 vs dyadic 22.9 (**5× better**)

Dyadic's coarse power-of-2 palette badly mis-serves agents whose target share
falls between powers of two. Farey's denser gap palette stays bounded.

**Drift cost (min-arc / uniform-slot; higher=better):**

| scheme | N=16 | N=50 | N=100 | N=200 |
|--------|-----:|-----:|------:|------:|
| farey  | 0.400 | 0.183 | 0.140 | 0.107 |
| dyadic | 0.500 | 0.781 | 0.781 | 0.781 |

Farey's smallest slot shrinks with N (0.40 → 0.11) while dyadic holds ~0.78.
At N=200 Farey's min gap is ~7× smaller → ~7× tighter clock-sync requirement.
This is the kill-test's drift concern, confirmed and quantified, and it is
structural (Farey gaps are non-uniform; smallest gap ~ 1/n²).

**Disruption (cumulative position moves):** Farey = 0, dyadic = 0, WFQ = O(N²)
(19,900 at N=200). Both nested schemes are genuinely zero-position-disruption;
WFQ buys its exactness with full repartition every join.

## Honest interpretation

- The lead is **real and non-dominated**: for heavy-tailed/continuous
  priorities (the realistic priority case), Farey gives a single closed-form,
  zero-comm, non-disruptive enumeration that approximates proportional
  allocation ~2.5–3× better than dyadic on average and ~5× better worst-case.
  Uniform TDMA can't do priority at all; WFQ needs comms. So in its niche,
  Farey is not dominated by the trivial alternatives — unlike every other
  application in the corpus.
- It is **narrow**: advantage holds for wide/continuous priority spread and
  **modest N**. The min-gap penalty grows with N, so at large N the drift cost
  likely overwhelms the accuracy gain. Best fit: small-to-moderate populations
  with good clocks.
- For **equal priority** dyadic wins outright — but equal priority is just
  uniform TDMA, outside this niche.

## Open question (the next decisive test)

This beats *vanilla base-2 dyadic*. It does NOT prove the Farey structure
specifically is necessary. A target-matched nested palette (mixed-radix van
der Corput, or per-class block allocation designed from the pre-agreed
priority classes) might match Farey's accuracy with a better min-gap. The
counter-argument: Farey is one universal closed-form enumeration that handles
*arbitrary* heavy-tailed priorities with no per-deployment design — a bespoke
palette must be re-designed per distribution.

**Next kill-test:** Farey vs a target-matched nested palette. If the bespoke
scheme matches Farey's TV with materially better min-gap, the Farey-specific
claim collapses to "use a fine nested palette." If Farey holds (universal,
design-free), the lead is genuinely Farey's.

## Classification (Aletheia)
- Autonomy: Level A (autonomous probe)
- Significance: Level 1 (minor, conditional novelty — one measured non-dominated
  niche; needs the target-matched-palette kill-test before any publication claim)
- Verification: simulation only; continuous-arc model (discrete-slot quantization
  may shrink the advantage); single fair-assignment heuristic
