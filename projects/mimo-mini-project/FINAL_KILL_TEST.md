# Final Kill-Test: Priority-Nesting Lead

**Date:** 2026-06-05
**Simulation:** `final_kill_test.py`
**Verdict:** NOT KILLED. Farey owns a genuine, non-dominated niche — but it is
four conjunctive conditions deep. Honest significance: a minor applied result,
publishable only if framed at exactly that niche and not oversold.

---

## Q1 — Is Farey special among universal design-free nested palettes?

Compared Farey/Stern-Brocot vs van der Corput radix 2, 3, 5 (all universal,
design-free, zero-comm, non-disruptive). Heavy-tailed priority dists:

| dist · N=100 | farey TV | dyadic2 | vdc3 | vdc5 |
|---|---:|---:|---:|---:|
| zipf | **0.146** | 0.403 | 0.450 | 0.398 |
| lognormal | **0.196** | 0.268 | 0.302 | 0.265 |

Worst-case relative error, zipf N=100: farey **0.60** vs 2.9–3.2 for all radix.
No radix matches Farey on heavy tails; higher radix is coarser, not better.

**Answer: Farey IS special.** The mediant structure gives a denser, non-geometric
gap palette that radix schemes cannot replicate. Farey owns the universal
design-free frontier for heavy-tailed priority demand.

Cost unchanged: Farey min-gap 0.11–0.18 ×uniform vs radix 0.4–0.82. The ~5–7×
tighter clock-sync requirement is real and grows with N.

(For uniform / two_class priorities, radix matches or beats Farey — but those
are not the heavy-tail niche; uniform priority = plain uniform TDMA.)

## Q2 — Does a target-matched oracle dominate Farey?

A fixed partition at cumulative target shares (knows the distribution at design
time). At full population N=100:

| dist | farey TV | oracle TV | farey mingap | oracle mingap |
|---|---:|---:|---:|---:|
| zipf | 0.146 | **0.000** | 0.140 | **0.193** |
| two_class | 0.351 | **0.000** | 0.140 | **0.357** |
| lognormal | 0.198 | **0.000** | 0.140 | 0.051 ← worse |

When the target/size is known, the oracle dominates Farey on accuracy and
(usually) drift. **But it is a fixed partition for the final size, so it wastes
bandwidth when underpopulated:**

| utilization | oracle @25% pop | @50% | @75% | farey (any) |
|---|---:|---:|---:|---:|
| all dists | ~0.25 | ~0.50 | ~0.75 | **1.00** |

The oracle leaks `(1 − t/N)` of the channel while the fleet is still growing.
Farey (full subdivision) uses 100% of bandwidth at every population size.

(Note: even the oracle can't beat Farey's min-gap on extreme tails — lognormal
forces a 0.051 slot. Heavy tails demand tiny slots regardless of scheme.)

## The bounded niche where Farey is non-dominated

All four must hold:

1. **Heavy-tailed / continuous priority demand** — else uniform/dyadic suffice.
2. **Final population / target NOT known in advance** — else the target-matched
   oracle wins on accuracy + drift.
3. **Full bandwidth wanted at every growth stage** — Farey's unique combination:
   design-free + 100% utilization at all sizes + best universal heavy-tail
   accuracy. The oracle gets accuracy but leaks bandwidth underpopulated.
4. **Modest N / clocks tolerant of ~5–7× smaller min-gap** — the structural cost.

In that intersection Farey beats every alternative tested:
- vs uniform/dyadic/radix → better heavy-tail accuracy (Q1)
- vs target-matched oracle → no target knowledge needed; 100% util at every size (Q2)
- vs WFQ → zero-comm, non-disruptive (probe 1)

## Defensible claim (and its limits)

"Stern-Brocot/Farey ordering yields the design-free, full-utilization, nested
heterogeneous-TDMA palette with best-in-class proportional accuracy for
unknown, heavy-tailed priority demand — at a min-gap (clock-sync) cost that
grows with N."

Limits / what a real paper still needs:
- Not proven OPTIMAL among ALL universal nested palettes — only best vs
  Farey + radix-{2,3,5}. Add Kronecker/golden-ratio and other low-discrepancy
  nested constructions before any optimality claim.
- Continuous-arc model; discrete-slot quantization may shrink the edge.
- The four-condition niche is narrow; real-world instances are plausible
  (incremental priority polling, lock/cache striping, comb allocation) but
  unverified against a concrete deployment.

## Classification (Aletheia)
- Autonomy: Level A
- Significance: Level 1 (minor, conditional novelty — one precisely-bounded
  non-dominated niche; needs broader competitor set + discrete model before
  a publication claim)
- Verification: simulation only
