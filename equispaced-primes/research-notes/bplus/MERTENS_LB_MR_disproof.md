---
schema_version: 1
title: "(MERTENS-LB-MR) Mertens-restricted version DISPROVED at p=237,733"
date: 2026-05-09
type: result
tier: working
confidence: 0.99
sources:
  - handoff-2026-05-09-followup/MERTENS_LB_literature_audit.md (audit's MR-survives claim)
  - handoff-2026-05-09-followup/MERTENS_LB_disproof_INDEPENDENT_VERIFICATION.md (universal version disproved)
  - /tmp/mertens_lb_mr.py (verifier)
  - handoff-2026-05-09-followup/MERTENS_LB_MR_verification.tsv (sample data)
tags: [mertens-lb-mr, polya-analog, b-plus, disproof, conjecture-failure]
---

# (MERTENS-LB-MR) is also FALSE — Pólya-flips at Mertens-restricted primes

## TL;DR

The literature audit (`MERTENS_LB_literature_audit.md`) verified that the Mertens-restricted version
**(MERTENS-LB-MR)**: `T(p−1) ≤ −c'` at primes p with M(p) ≤ −3 with c'=1.43 at 4,617 such primes p ≤ 99,991, and proposed it as the surviving variant relevant to B+ closure.

**This session's verification at p ∈ (99,991, 10⁷] DISPROVES it.** Out of 9,669 sampled Mertens-restricted primes, **221 satisfy T(p−1) > 0** — chronic Pólya-flips at MR primes. **First counterexample: p=237,733, M(p)=−20, T(p−1) = +6.658.**

**Both (MERTENS-LB) and (MERTENS-LB-MR) are DISPROVED.** SP-2's reduction `B+ closure ⟸ B₀(N) ≥ c·N ⟸ (MERTENS-LB-?)` is INVALID in either form. The empirical "evidence" R1+SP-2 cited (B₀(p−1) ≥ 0.4383·(p−1) at 4,600+ primes ≤ 99,991) sat exactly in the pre-flip regime — chronic failure begins immediately past R1's ceiling.

## Verification

**Method**: Mertens-restricted primes p with M(p) ≤ −3 in (99,991, 10⁷] sampled (all early ones up to 200K, then every-10th in (200K, 10⁶], every-100th in (10⁶, 10⁷]). For each, compute T(p−1) via Dirichlet hyperbola against the precomputed M cumulative sum.

| | |
|---|---|
| Sieve check | M(99,991)=−49, M(10⁶)=212, M(10⁷)=1037 — all match OEIS A002321 |
| Total primes in (99,991, 10⁷] | 654,987 |
| Mertens-restricted (M(p) ≤ −3) | 328,565 (50.2%) |
| Sample size | 9,669 |
| Compute time | 9.5 s on this machine |
| **Pólya-flips at MR primes** | **221** |
| Sign distribution | 221 positive, 9,448 non-positive |
| **Smallest counterexample** | **p=237,733, M(p)=−20, T(p−1) = +6.658** |
| Largest T(p−1) observed | +130.57 |
| Smallest c' that holds across sample | c' = −130.6 (i.e., the bound `≤ −c'` cannot hold for any c' > 0) |

## First 20 Pólya-flips at MR primes

| p | M(p) | T(p−1) |
|---:|---:|---:|
| 237,733 | −20 | +6.658 |
| 237,859 | −17 | +8.418 |
| 237,977 | −23 | +2.493 |
| 239,171 | −28 | +0.783 |
| 239,893 | −20 | +1.131 |
| 240,659 | −20 | +3.949 |
| 384,173 | −4 | +3.810 |
| 565,111 | −7 | +0.292 |
| 567,991 | −8 | +17.911 |
| 568,133 | −10 | +14.781 |
| 568,207 | −20 | +6.860 |
| 568,367 | −15 | +9.056 |
| 570,859 | −11 | +1.805 |
| 571,031 | −4 | +6.118 |
| 571,229 | −7 | +2.696 |
| 571,433 | −5 | +6.459 |
| 572,051 | −4 | +14.557 |
| 572,177 | −3 | +11.586 |
| 572,333 | −9 | +7.385 |
| 572,471 | −16 | +1.599 |

The flips cluster — typically multiple consecutive MR primes flip together (e.g., 237,733 / 237,859 / 237,977 / 239,171 are all within a 0.3% window) and they recur at multiple scales: ~237K, ~565K-572K range, ~862K (per the dataset patterns).

## Late-end behavior — flips taper but keep happening

| Largest 10 MR primes sampled | M(p) | T(p−1) |
|---:|---:|---:|
| p=9,545,171 | −15 | −27.10 |
| p=9,546,737 | −19 | −39.78 |
| p=9,548,249 | −65 | −77.99 |
| p=9,549,983 | −16 | −43.85 |
| p=9,584,513 | −6 | −111.63 |
| p=9,585,881 | −48 | −148.31 |
| p=9,587,407 | −92 | −177.11 |
| p=9,589,133 | −47 | −139.31 |
| p=9,591,343 | −9 | −113.76 |
| p=9,593,281 | −30 | −121.31 |

Near the upper end of the sweep (p ~ 10⁷), T(p−1) tends to be more negative — but flips still occur in the middle range (e.g., p=8,216,107 had T(p−1) = +9.19, flagged in the running output).

## Why the Mertens-restriction was not enough

The lit audit's argument: "M(p) ≤ −3 forces the k=1 term of T(p−1) to be M(p−1)/1 ≈ M(p) ≤ −3, biasing T into the negative regime."

This is **only the k=1 contribution**. At p ≈ 237K, the k=2..p−1 terms involve M(⌊p/k⌋) for ⌊p/k⌋ in [1, p/2], which span a much wider range of M values than just M(p) itself. M(x) at random scales x has values that can be much more positive than M(p) is negative — and the harmonic-weighted sum aggregates these. The Mertens-restriction at p does not prevent the OTHER terms from being large positive contributions.

This is a structural reason the Mertens-restriction alone cannot save the conjecture. Any Pólya-style disproof in the Möbius-harmonic family is likely to survive simple "restrict to a forcing-set" weakenings.

## Implications for the program

| | |
|---|---|
| (MERTENS-LB) universal | **DISPROVED** at N ≈ 300K, chronic |
| (MERTENS-LB-MR) Mertens-restricted | **DISPROVED** at p = 237,733, chronic |
| SP-2's reduction chain (in either form) | **INVALID** — sufficient condition is false |
| B+ Mertens-restricted at p > 99,991 | **GENUINELY UNCERTAIN** — empirical sweep stopped exactly where chronic-flip territory begins |
| **Direct verification of B₀(p−1) at flipped primes** | **infeasible at p ≈ 237K via direct Farey enumeration** (`\|F_{p-1}\| ~ 1.7×10¹⁰` pairs) — would need a closed form for `‖δ‖²` to use SP-2's identity |
| **Conjecture B+ truth** | **OPEN, possibly false at large p** — there's no longer ANY structural argument that B+ holds past p ≈ 10⁵, and the Möbius-harmonic sum it depends on flips chronically |

## Strategic conclusion

The program's "B+ Mertens-restricted is empirically true at 4,600+ primes" claim **does not extrapolate**. The (MERTENS-LB-MR) reduction has the same Pólya-shape as Pólya/Turán/Mertens-conjecture and fails at the same kind of small scale.

The Koyama-track pivot is **even more strongly motivated** now:
- The NDC, AK constant, B_∞, EC paths are independent of the Pólya-analog risk that killed both (MERTENS-LB) versions
- They have direct numerical verification at K=2×10⁶ already (40-digit precision)
- Akatsuka 2013 provides the rigorous framework
- Koyama himself has endorsed the conjectures

## Files written

- `MERTENS_LB_MR_verification.tsv` — full sample data (9,669 MR primes with T(p−1))
- `/tmp/mertens_lb_mr.py` — reproducible verifier
