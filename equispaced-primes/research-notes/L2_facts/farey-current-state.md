---
schema_version: 2
title: Farey Current State
type: fact
domain: project
tier: semantic
confidence: 0.95
created: 2026-04-24
updated: 2026-04-24
verified: 2026-04-24
sources:
  - raw/farey-archive/handoff/complete_farey_handoff.md.txt
  - raw/farey-archive/state-docs/CLAIM_STATUS.md.txt
  - projects/farey-research/data/PHASE1_500ZEROS_CORRECTED.json
  - projects/farey-research/data/PHASE1_EC_RECOMPUTE.json
  - projects/farey-research/data/RANK3_5077A1.json
  - projects/farey-research/data/RANK0_CLUSTER.json
  - projects/farey-research/data/CONDUCTOR_CONTROL_37b.json
  - projects/farey-research/data/W2_PRIME_FIT.json
supersedes: []
superseded-by: 
tags: [farey, current-state, c1, verified]
---

# Farey Current State

## Research Object

Spectroscope statistic:

`C1(f,rho) = |c_K(rho,f)| * |L'(rho,f)| / (log K + gamma_Euler)`

with

`c_K(rho,f) = sum_{n <= K} mu_f(n) * exp(-n/K) * n^{-rho}`.

Arithmetic normalization:

- Weight-2 elliptic curves: `rho = 1 + i gamma`.
- Delta weight-12: `rho = 6 + i gamma`.
- Never mix analytic `rho = 1/2 + i gamma` with arithmetic coefficients.

## Verified Numerical State

All values below are post-`mu_f(p^2)` bugfix and use `K = 10^4`.

| form | rank | weight | conductor | sample | E[C1^2] | status |
|---|---:|---:|---:|---:|---:|---|
| Delta level 1 | n/a | 12 | 1 | 683 zeros | 0.950231842 | confirmed anchor |
| 37a1 | 1 | 2 | 37 | 500 zeros | 2.189911545 | confirmed |
| 389a1 | 2 | 2 | 389 | 500 zeros | 3.113923728 | confirmed |
| 5077a1 | 3 | 2 | 5077 | 500 zeros | 4.617 | confirmed rank-3 anchor |
| 11a1-24a1 rank-0 cluster | 0 | 2 | 11-24 | 200 each | mean 1.886 | confirmed, CV 8.9% |
| 37b1/37b2/37b3 | 0 | 2 | 37 | 200 each | mean 2.052 | conductor-control evidence |

## W2 Prime Summary

Working empirical model for 22 weight-2 EC points:

`E[C1^2] = 0.4785 - 0.1668 * rank + 0.4727 * log(N)`

with `R^2 = 0.809819`. `log(N)` is significant in this fit; the rank coefficient is unstable in the 22-point regression, while control tests still show rank-sensitive structure at fixed or nearby conductor.

## Operating Warnings

- `mu_f(p^2) = p^{k-1}`, not the Hecke eigenvalue `a_{p^2}`.
- Pre-2026-04-15 C1 results are invalid unless independently reverified.
- Old pure-rank W2 framing is superseded by W2 prime.
- Raw `L(Sym^2 f,k)/<f,f>` proportionality is empirically falsified for 37a1 vs 389a1 direction.
