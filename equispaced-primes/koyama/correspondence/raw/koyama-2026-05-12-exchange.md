---
schema_version: 1
title: "Koyama correspondence raw record — 2026-05-12 exchange"
date: 2026-05-12
type: correspondence-raw
tier: immutable
status: archived
participants:
  - saar@... (outgoing)
  - koyama@tmtv.ne.jp (incoming)
context:
  - Reply pair following the 2026-05-04 CREST-deadline pause.
  - Saar's outgoing message tightens claim posture across C1, Sym²/Petersson,
    e^{-γ} constant, shifted Perron remainder, and GL(2)/EC pointwise
    analogue.
  - Koyama's incoming message proposes co-authored journal submission and
    requests the Technical/Computational section: methodology of
    double-verification, Lean 4 formalization path, and current numerical
    findings.
tags: [koyama, correspondence, raw, 2026-05-12, journal-submission]
---

# Koyama correspondence raw record — 2026-05-12 exchange

This file is the immutable raw record of the 2026-05-12 email pair. Synthesis
and follow-up actions belong in [`../KOYAMA.md`](../KOYAMA.md) and the
handoff packets, not here.

## Outgoing — Saar → Koyama (claim-tightening)

> I have tightened the adjacent elliptic-curve and C_1 statements we
> discussed. The apparent rank trend remains interesting, but I would now
> describe it as conductor-confounded rather than a clean rank law: once
> log(N) is included, the rank coefficient is not stable enough to state as a
> law. I am keeping Delta separate from the elliptic-curve rank discussion;
> its corrected C_1^2 anchor remains close to 0.950232, but convergence to 1
> should be presented only as a possible target, not as a theorem. Similarly,
> the raw Sym²/Petersson proportionality we tested is falsified in that exact
> form, though this does not rule out a completed or archimedean-corrected
> Sym² normalization.
>
> On the NDC/DRH side, the most important correction is the constant. The
> earlier 1/zeta(2) numerical target should be replaced by the
> Mertens/Aoki-Koyama normalization with an e^{-gamma} factor. The local
> Perron residue computation and the corrected B_infty structure are stable,
> but I would not yet present the full shifted Perron remainder as a closed
> theorem, because the remaining difficulty is controlling the aggregate
> contribution from the other zeros. For elliptic curves / GL(2), the
> smoothed computations remain useful evidence, but the pointwise fixed-curve
> analogue also seems to require a genuine theorem controlling reciprocal
> derivatives at off-central zeros, or else it should be stated as an
> averaged/profile result.
>
> The Farey spectroscope and explicit-formula bridge remain the conceptual
> starting point; DPAC remains a formalization/conjectural target, and the
> Lean 4 / post-bias cryptography material remains ready. If you know a
> GL(2) theorem controlling 1/L'(rho,E), a minimum-modulus estimate for
> elliptic-curve L-functions, or a shifted Perron remainder theorem of this
> kind, that would be exactly the missing input for the next step.

## Incoming — Koyama → Saar (journal-submission proposal)

> Regarding the next step: Journal Submission
>
> I would like to list you as a co-author and submit our findings to a
> journal as soon as possible. While I still need to investigate the
> discrepancies in the tables (which I will do as soon as I have time), I
> would like us to start preparing the manuscript.
>
> Your recent updates on the $e^{-\gamma}$ factor, the conductor-confounded
> trend, and the requirements for the shifted Perron remainder are
> fascinating. I believe these "open challenges" and the rigorous
> verification you've done at $10^{13}$ should be the core of our paper.
>
> Could you start drafting the Technical/Computational section (Methodology
> of the double-verification, the Lean 4 formalization path, and the current
> numerical findings)?
>
> I will focus on the Kiban-S application now (separate matter), and after
> than, I will resolve the table discrepancies so we can finalize the data
> for submission.
>
> Let's secure our priority on this discovery by getting the paper out soon.

## Operational implications (record only — no action taken without approval)

1. Joint paper is now formally proposed; Saar listed as co-author.
2. Paper core = "open challenges" + rigorous numerical verification up to
   the verified scale (Koyama paraphrases as `10^{13}`; cross-check our
   internal verified ranges before printing this number).
3. First deliverable owned by Saar: Technical/Computational section —
   double-verification methodology, Lean 4 formalization path, current
   numerical findings.
4. Koyama defers table-discrepancy reconciliation until after the
   Kiban-S deadline (recorded internal deadline: 2026-05-20).
5. No outbound email or commit is sent without explicit user approval.
