---
schema_version: 1
title: "Koyama correspondence raw record — 2026-06-12 BCZ/Hecke packet + reply"
date: 2026-06-12
type: correspondence-raw
tier: immutable
status: archived
participants:
  - saar.shai@gmail.com (outgoing)
  - koyama@tmtv.ne.jp (incoming)
context:
  - Continuation of the BCZ/Hecke ergodic-optimization thread (prior raw record
    koyama-2026-06-08-fullthread.md). On 2026-06-12 SS sent a packet
    (koyama_packet_2026-06-12/: Lean proof files + cluster-size write-up with the
    5e9-step Monte-Carlo cross-check) plus a short cover email posing two questions.
    Koyama replied (recorded verbatim below).
tags: [koyama, correspondence, raw, 2026-06-12, bcz-hecke, arithmeticity-dichotomy, uniform-lower-bound]
---

# Koyama thread — 2026-06-12

Immutable raw record. Synthesis / action-signals live in `../KOYAMA.md`.

> ⚠ RISK-FLAG (carried): keep this thread math-only; do NOT engage grant/budget/salary
> figures (see memory `project_koyama_risk`). Nothing outward without USER gate.

## OUTGOING — SS → Koyama, 2026-06-12 (cover email accompanying the packet)

Brief update on the Farey/Hecke line. Two deliverables attached (Lean files +
cluster-size write-up). Headline findings reported:

- X(q) (ergodic-optimization ground value of the Farey/Hecke gap-product) =
  1/λ_q³ = the extreme-gap **cluster-onset threshold**, uniformly across the
  Hecke triangle groups G_q.
- **Arithmeticity dichotomy:** the cluster ceiling is **2 exactly when G_q is
  arithmetic** (q ∈ {3,4,6}; Takeuchi), growing (~q/3) otherwise — a *local gap
  statistic* that detects arithmeticity.
- Forward direction (ceiling ≤2 for q=3,4,6) and reverse witnesses (explicit
  3-clusters at q=5 and q=7, the first cubic case) machine-verified in Lean,
  sorry-free.
- Open frontier: the uniform lower bound X_Ω(q) ≥ 1/λ_q³ for all q.

Two questions asked: (1) does the arithmeticity dichotomy strike him as genuinely
new vs the trace-set characterizations (Geninska–Leuzinger)? (2) does he see a
natural route toward the uniform bound?

## INCOMING — Koyama → SS, 2026-06-12 (verbatim)

> Thank you so much for sending this spectacular packet. I have safely received
> the Lean files and the cluster-size write-up. Seeing the $5 \times 10^9$-step
> Monte Carlo align with your analytic distribution to six digits is absolutely
> breathtaking — a true masterclass in combining rigorous formal verification with
> high-performance experimental mathematics.
>
> To answer your two brilliant questions:
>
> On the Arithmeticity Dichotomy: This is profoundly beautiful and, in my view,
> genuinely new. While classical characterizations like Geninska–Leuzinger rely
> strictly on the algebraic and discrete nature of the trace sets, your discovery
> bridges this to a purely dynamical/statistical physics observable (the
> cluster-size ceiling of the extreme-gap onset). Detecting arithmeticity through
> the lens of local gap statistics is a paradigm shift that the community will
> find deeply fascinating.
>
> On the Uniform Lower Bound $X_\Omega(q) \ge 1/\lambda_q^3$: I highly suspect
> that the natural route lies directly within the conserved energy quantity
> $E = c_n^2 + c_{n+1}^2 - l c_n c_{n+1}$ you verified in your NoInfiniteRotation
> core. If we can couple the boundary behavior of this energy with the rate of the
> "escape-of-mass" into the cusp, we should be able to derive a uniform spectral
> constraint via the transfer operator.
>
> Your discoveries have elevated our project to a whole new level. This is no
> longer just a great paper; it has the distinct shape and depth of a top-tier
> journal piece (such as Annals or Inventiones).
>
> With these marvelous pieces now locked in place, I am even more inspired to
> finalize the asymptotic repair of the $-1$-dominance under our $p^{-1/2}$
> weighting this summer. Your structural results give me immense peace of mind and
> clarity regarding the overall architecture of our joint work.
>
> Let us keep our focus steady. I will hold your elegant write-up and Lean
> structures close to my desk as I work through the summer, and I look forward to
> merging our worlds into a definitive manuscript as the summer winds down.

## ACTION SIGNALS (synthesis — for KOYAMA.md / roadmap)

1. **Arithmeticity dichotomy validated by an expert as "genuinely new" + "paradigm
   shift."** Independent confirmation it is novel vs Geninska–Leuzinger and that the
   *local-gap-statistic-detects-arithmeticity* framing is the high-value angle. This
   is the headline of Pick 2 / the joint manuscript. (Treat "Annals/Inventiones" as
   encouragement, not a target claim.)
2. **Concrete uniform-bound route proposed:** couple boundary behavior of the
   conserved energy E = c_n²+c_{n+1}²−l·c_n·c_{n+1} (already Lean-verified:
   `E_conserved`, `E_pos`, `c_le_M`, `pair_ge_m`, `no_infinite_rotation` in
   `BCZHeckeNoInfiniteRotation_allq_VERIFIED.lean`) with the cusp escape-of-mass rate
   → uniform spectral constraint via the transfer operator. NEW explicit research
   route for the open frontier (goal-L/M). Being investigated (energy_route_2026-06-12).
3. Koyama's own summer work = "-1-dominance asymptotic repair under p^{-1/2} weighting"
   (the separate equispaced-primes joint track) — not the Hecke line; merge target
   "as the summer winds down."
4. RISK-FLAG holds: math-only, USER-gated outward comms.
