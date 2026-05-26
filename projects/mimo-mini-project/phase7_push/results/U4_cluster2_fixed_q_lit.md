# Cluster=2 fixed-q regime — literature/novelty assessment

**Source**: research-lite subagent, 59 seconds, 6 tool uses

## What's already known
- **BCZ framework** (Boca, Cobeli, Zaharescu, 2001+) — standard machinery for Farey gap distributions via horocycle flow. [BCZ map is weakly mixing, arXiv:2403.14976]
- **Athreya-Cheung Poincaré section** [arXiv:1206.6597] — sliding-section formalism for horocycle flow. Foundational.
- **Hall's classical result** — normalized gap distribution equals (2ζ(2)·xy)⁻¹ on the unit triangle (limiting MEASURE, not extremal index)
- **Extremal index ⟺ mean cluster size**: θ = 1/2 ⟺ mean cluster size = 2. This is **standard EVT theory**, not novel.

## Novelty assessment (subagent verdict)

| Claim | Lit status |
|---|---|
| BCZ limiting distributions | Standard |
| Extremal index θ = 1/2 | Standard |
| **Empirical cluster-size-2 persistence (99.5% at q=0.9999, N ∈ [10⁴, 10⁵])** | **Not in literature** |
| **"Cluster size exactly 2 with prob → 1" in any classical sequence** | **Zero literature** |
| **Size-3 clusters have zero frequency** | **Not explained by existing theory** |

## Path to publication
Recommendation from subagent:
> Publishable if you can prove **θ ≥ 1/2 universally for Farey gaps** (implying mean cluster size ≤ 2) or exhibit a mechanism from the BCZ or Athreya-Cheung cocycles that forces cluster size ≤ 2 at high quantiles.

## What we have already (T3C)
- Rigorous proof outline under BCZ for SCALING regime (1−q_N = κ/N): Type A/B case analysis → cluster size exactly 2
- FIXED-q regime: empirically holds, theoretically open

## Concrete next steps
1. **Strengthen T3C**: convert the scaling-regime case analysis into a published proof
2. **Fixed-q proof**: try to show "at fixed q, ∃ N₀ such that ∀N > N₀, P(cluster size = 2 | exceed) > 1 − ε"
3. **Submit to Experimental Mathematics** (or Annals of Applied Probability) with empirical + scaling-regime proof + fixed-q conjecture

## References to add
- arXiv:2403.14976 — BCZ map weakly mixing (latest)
- arXiv:1206.6597 — Athreya-Cheung Poincaré section
- arXiv:0810.1150 — extremal index cluster size theory
- arXiv:1301.0277 — gap distribution with divisibility constraints
- arXiv:1503.02539 — weighted Farey and horocycle flow
