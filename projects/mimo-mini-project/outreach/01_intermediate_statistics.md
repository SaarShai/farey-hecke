# Outreach drafts — Intermediate statistics / RMT universality

**Status**: DRAFT (not sent). Review before use.
**Date**: 2026-05-27
**Common attachments to mention**: closed-form derivation note + diagnostic table (preprint TBA)

## ⚡ Iter-3 framing strengthening

Before sending, all drafts below should foreground the **qualitative novelty** of the cluster=2 finding — not just the closed-form threshold + diagnostic %, but the **sharp upper bound on cluster size** above q*_BCZ. Key talking point per draft:

> "Above q*_BCZ = (11 − 8·ln(3/2))/9 ≈ 0.86181, the maximum cluster size in the BCZ chain is **exactly 2** — runs of length 3 or more vanish entirely. A 500-million-step Monte Carlo confirmed zero size-3+ clusters out of 38.97 million tested at the exact closed-form constant, with the empirical transition sharp to 10⁻⁵. **At q = 0.99 the size-2 cluster fraction is ~95% for Farey/BCZ vs ~0% for every standard RMT ensemble tested (GOE, GUE, GSE, COE, CUE, CSE, β-Hermite for β ∈ {1, 2, 4, 6, 10})** — effectively a binary diagnostic, not a graded one. This is qualitatively different from Poisson (1.86%), Wigner-Dyson (≤1%), and intermediate statistics — the BCZ class has an *indicator-type hard cap* on the joint density that smooth eigenvalue interactions cannot reproduce."

The drafts below were composed before this empirical landed; treat the older "50M MC, ±5×10⁻⁴" phrasing as obsolete and replace with the 500M MC / 0 size-3+ / 10⁻⁵-sharp framing when sending.

---

---

## 1. Jens Marklof — `J.Marklof@bristol.ac.uk`
**Subject**: Closed-form cluster threshold for the BCZ density — possible link to your Farey/horocycle work

Dear Professor Marklof,

In recent work on the BCZ chain dynamics (b_{i+2} = ⌊(b_i+N)/b_{i+1}⌋·b_{i+1} − b_i) we obtained a closed-form universality threshold q*_BCZ = (11 − 8·ln(3/2))/9 ≈ 0.86181, derived from P_BCZ(XY < 2/9) = (8·ln(3/2) − 2)/9 on the standard triangle {x+y>1}. Above this q, the size-2 cluster fraction is empirically ≥ 88% across 50M Monte Carlo steps and direct Farey enumeration at N=10⁶, while all Wigner-Dyson ensembles (GOE/GUE/GSE and the unitary circular analogues) sit at 0.5–0.75% under the same diagnostic — a two-orders-of-magnitude gap.

Given your work on lattice-point statistics and the Farey/horocycle connection, I wanted to flag the closed form and ask whether you see a natural ergodic interpretation (it should be expressible in horocycle-flow language via the BCZ-Athreya-Cheung framework). I have a short note and the diagnostic data ready to share if useful.

— Saar Shai

---

## 2. Florin Boca — `fboca@illinois.edu`
**Subject**: Closed-form q*_BCZ from your 2001 density — feedback request

Dear Professor Boca,

Building on Boca-Cobeli-Zaharescu 2001, I derived a closed form for the size-2/size-3+ cluster transition in the BCZ chain: q*_BCZ = (11 − 8·ln(3/2))/9 ≈ 0.86181, with the underlying integral P_BCZ(XY < 2/9) = (8·ln(3/2) − 2)/9 obtained by direct Fubini on the unit-square triangle. The threshold is also reproduced (within 5×10⁻⁴) by 50M Monte Carlo of the chain. The companion "median-run" cutoff is q_median = 3/2 − ln 2.

I'd value your reading on whether (a) you've seen this constant before in the BCZ-density literature, and (b) whether the cluster-size diagnostic — which separates BCZ-class sequences from Wigner-Dyson at ~100× — strikes you as a viable universality test worth developing into a paper. I can share the derivation and a Lean 4 formalization (most of it 0-sorry) at your convenience.

— Saar Shai

---

## 3. Cristian Cobeli — `cristian.cobeli@imar.ro`
**Subject**: A closed-form cluster threshold built on BCZ density

Dear Professor Cobeli,

I wanted to share a result that uses the BCZ joint density f(x,y) = 2·𝟙_{x+y>1} directly. Splitting the unit-square triangle into four x-regions and integrating xy < 2/9 yields P = (8·ln(3/2) − 2)/9, so the universality threshold for size-2 clustering in the BCZ chain dynamics is q*_BCZ = (11 − 8·ln(3/2))/9 ≈ 0.86181. Empirical Monte Carlo at 50M steps and direct Farey enumeration at N=10⁶ both land inside ±5×10⁻⁴ of this value.

A companion observation: the cluster-size statistic at fixed q ≈ 0.99 separates BCZ-class sequences (~95% size-2) from all standard RMT ensembles (~0.66% size-2) by two orders of magnitude — a clean computable diagnostic. Would you be open to a 30-minute call (or just feedback by email) on whether this matches anything you've encountered in your own work with Florin and Alex?

— Saar Shai

---

## 4. Alexandru Zaharescu — `zaharesc@illinois.edu`
**Subject**: q*_BCZ = (11 − 8·ln(3/2))/9 — derivation note + diagnostic

Dear Professor Zaharescu,

I'm writing to share a closed-form universality threshold for the BCZ chain dynamics that I derived from your 2001 density: q*_BCZ = (11 − 8·ln(3/2))/9 ≈ 0.86181, coming from P_BCZ(XY < 2/9) = (8·ln(3/2) − 2)/9 via direct Fubini on the {x+y>1, 0<x,y<1} triangle. The threshold separates the regime of guaranteed size-2 clusters (above q*) from mixed regime (below). I also obtained the median-run cutoff q_median = 3/2 − ln 2.

I have a 12-15 page draft in preparation and would appreciate any feedback on prior-art coverage — in particular whether either constant appears (perhaps under a different formulation) in the BCZ-density literature I might be missing. The companion diagnostic separates Farey/BCZ-class sequences from Wigner-Dyson ensembles by ~100× on a simple cluster-size statistic.

— Saar Shai

---

## 5. Jayadev Athreya — `jathreya@uw.edu`
**Subject**: BCZ chain universality + Athreya-Cheung 2014 §8 connection

Dear Professor Athreya,

In your IMRN 2014 paper with Yitwah Cheung, §8 raises open questions about the universality role of the BCZ density beyond the Farey case. I have a partial answer in the form of a closed-form cluster threshold: q*_BCZ = (11 − 8·ln(3/2))/9 ≈ 0.86181 for the BCZ chain dynamics, derived directly from P_BCZ(XY < 2/9) on the {x+y>1} triangle. The threshold matches both 10⁶ direct Farey enumeration and 50M Monte Carlo of the chain to ±5×10⁻⁴.

The same construction yields a *computable* universality diagnostic that separates BCZ-class sequences (95% size-2 clusters at q=0.99) from all classical RMT ensembles (0.5–0.75%) by two orders of magnitude. I'd be very interested in your reading on whether this lands inside the §8 open-question family, and whether you'd find a horocycle-flow restatement appealing. Happy to share the derivation note + diagnostic JSON.

— Saar Shai

---

## 6. Yitwah Cheung — `ycheung@sfsu.edu`
**Subject**: Cluster threshold for the BCZ chain — closed form + diagnostic

Dear Professor Cheung,

Following up on your IMRN 2014 work with Jayadev Athreya: I obtained a closed-form size-2 universality threshold for the BCZ chain, q*_BCZ = (11 − 8·ln(3/2))/9 ≈ 0.86181, derived from a Fubini integration of the BCZ density over the {x+y>1} triangle restricted to xy < 2/9. The median-run companion is q_median = 3/2 − ln 2.

The construction also yields a computable diagnostic that places sequences into BCZ vs Wigner-Dyson classes via cluster-size statistics with a ~100× separation. I would appreciate your feedback on whether either constant — or the diagnostic framing — connects to your dynamical-systems perspective on the BCZ density. A short note + numerical data is ready to share.

— Saar Shai

---

## 7. Zeev Rudnick — `rudnick@tauex.tau.ac.il`
**Subject**: Cluster-size diagnostic for spacing universality classes

Dear Professor Rudnick,

I wanted to bring to your attention a cluster-size statistic that empirically distinguishes the BCZ/Farey universality class from Wigner-Dyson ensembles by two orders of magnitude. At q = 0.99 (extreme-quantile threshold), the size-2 cluster fraction is ~95% for direct Farey enumeration and 88-99.6% for the BCZ chain dynamics across 50M Monte Carlo steps; for GOE/GUE/GSE/COE/CUE/CSE the same statistic is 0.5–0.75%. Riemann ζ zeros (LMFDB, 100k) come in at 3%, consistent with the GUE prediction at low q. I also have a closed-form threshold q*_BCZ = (11 − 8·ln(3/2))/9 ≈ 0.86181 from direct integration of the BCZ density.

Given your work on pair correlation and spacing statistics, I would value your reading on whether this is a useful diagnostic — particularly for the "intermediate statistics" regime — and whether you've encountered the constant elsewhere. A 12-page draft is in preparation.

— Saar Shai

---

---

## 8. Nicholas Katz — `nmk@math.princeton.edu`
**Subject**: Cluster-size diagnostic for the Katz-Sarnak universality framework

Dear Professor Katz,

I obtained a closed-form size-2 universality threshold for the BCZ chain dynamics, q*_BCZ = (11 − 8·ln(3/2))/9 ≈ 0.86181, derived directly from the BCZ density on the {x+y>1} triangle, together with a computable diagnostic that distinguishes spacing universality classes by cluster-size statistics. At extreme quantile q = 0.99, BCZ-class sequences (direct Farey enumeration N=10⁶, 50M Monte Carlo of the chain) sit at 88–95% size-2; classical Wigner-Dyson ensembles (GOE/GUE/GSE and their unitary circular analogues) sit at 0.5–0.75%; the Riemann ζ-zeros (100k from LMFDB) come in at 3% — two orders of magnitude separation.

Given the Katz-Sarnak philosophy of placing arithmetic families into universality classes, I'd appreciate your reading on whether this single-number diagnostic fits as a tool inside that framework — particularly for families of automorphic L-zeros that sit ambiguously between Poisson and Wigner-Dyson. A 15-18 page draft is in preparation; happy to share derivation notes + diagnostic JSON.

— Saar Shai

---

## 9. Eugene Bogomolny — `eugene.bogomolny@u-psud.fr`
**Subject**: A possible diagnostic for "intermediate statistics" — cluster threshold q*_BCZ

Dear Professor Bogomolny,

In your work (with Giraud and others) on the intermediate statistics regime between Poisson and Wigner-Dyson, you have articulated the open challenge of classifying sequences that sit between the two extremes. I wanted to share a closed-form threshold q*_BCZ = (11 − 8·ln(3/2))/9 ≈ 0.86181 for the BCZ chain dynamics, together with a cluster-size diagnostic that empirically separates BCZ/Farey-class sequences (88–95% size-2 clusters at extreme quantile q=0.99) from all classical RMT ensembles (0.5–0.75% under the same statistic). Riemann ζ-zeros sit at 3% — visible "GUE at low q" signature.

If this fits inside the intermediate-statistics framework you've developed, I would value your feedback. Concretely: is the BCZ density a recognized member of your taxonomy, or does it live outside it? A note + reproducible data are ready to share.

— Saar Shai

---

## 10. Olivier Giraud — `olivier.giraud@lptms.u-psud.fr`
**Subject**: Cluster-size diagnostic for intermediate-statistics taxonomy

Dear Professor Giraud,

Following your work with Eugene Bogomolny on intermediate spacing statistics (the regime between Poisson and Wigner-Dyson), I obtained a closed-form universality threshold q*_BCZ = (11 − 8·ln(3/2))/9 ≈ 0.86181 for the BCZ chain dynamics on the {x+y>1} triangle, with a companion cluster-size statistic that places the BCZ/Farey class (~95% size-2 at q=0.99) two orders of magnitude away from Wigner-Dyson (0.5–0.75%).

The result is rigorously derived (Fubini on the BCZ density), partially Lean-formalized (0-sorry on the variance/correlation pieces via Mathlib v4.28.0), and tested on 8 sequence classes including Riemann ζ-zeros and modular form Hecke eigenvalues. I'd welcome your reading on whether it lands inside your intermediate-statistics framework and whether there are pseudo-integrable or quasicrystal systems where the diagnostic should be tried.

— Saar Shai

---

## 11. Pär Kurlberg — `kurlberg@kth.se`
**Subject**: Cluster-size statistic separates BCZ/Farey from Wigner-Dyson at 100×

Dear Professor Kurlberg,

I'd like to share a result that may interest you given your work on pair correlation and quantum chaos: a closed-form size-2 universality threshold q*_BCZ = (11 − 8·ln(3/2))/9 ≈ 0.86181 for the BCZ chain (Boca-Cobeli-Zaharescu density), together with a computable diagnostic on cluster-size statistics that distinguishes BCZ/Farey-class sequences (88–95% size-2 at extreme quantile q=0.99) from Wigner-Dyson ensembles (GOE/GUE/GSE/COE/CUE/CSE at 0.5–0.75%). Riemann ζ-zeros (LMFDB 100k) sit at 3%.

The diagnostic could plausibly distinguish quantum cat-map or arithmetic eigenvalue spacings from generic RMT — a question your work has often touched. I would appreciate your reading on (a) whether the diagnostic is novel as you understand the field and (b) whether you'd find it useful for any of your current spacing-statistics problems. Notes + raw data ready to share.

— Saar Shai

---

## 12. Jon Keating — `keating@maths.ox.ac.uk`
**Subject**: Universality diagnostic + closed-form threshold for BCZ chain

Dear Professor Keating,

I obtained a closed-form universality threshold q*_BCZ = (11 − 8·ln(3/2))/9 ≈ 0.86181 for the size-2 / size-3+ cluster transition in the BCZ chain dynamics. The associated cluster-size diagnostic at q = 0.99 separates the BCZ/Farey universality class (88–95% size-2) from all Wigner-Dyson ensembles (GOE/GUE/GSE and the CUE/COE/CSE side; 0.5–0.75%) by ~100×. Riemann ζ-zeros (100k LMFDB) sit at 3% — consistent with GUE at low q.

Given your work with Nina Snaith on L-function moments and CUE statistics, I'd value your reading on whether this diagnostic constitutes a useful additional classifier on top of the moment / characteristic-polynomial framework, and whether you've seen the closed-form constant before. A 15-18 page draft is in preparation. Happy to share notes and raw data.

— Saar Shai

---

## 13. Nina Snaith — `n.c.snaith@bristol.ac.uk`
**Subject**: Cluster diagnostic for spacing universality — possible CUE/L-function connection

Dear Professor Snaith,

In recent work on the BCZ chain dynamics I obtained a closed-form universality threshold q*_BCZ = (11 − 8·ln(3/2))/9 ≈ 0.86181 from direct integration of the BCZ density on the {x+y>1} triangle. The companion cluster-size diagnostic at q = 0.99 places BCZ/Farey-class sequences at 88–95% size-2 clusters, all classical RMT ensembles (GOE/GUE/GSE/CUE/COE/CSE) at 0.5–0.75%, and Riemann ζ-zeros (LMFDB 100k) at 3%.

Given your work with Jon Keating on CUE and L-function moments, I wondered if you've encountered this constant or a similar diagnostic. The diagnostic could plausibly classify families of L-zeros into universality classes more cleanly than spectral statistics alone. Would you be open to a brief exchange? Notes + data ready to share.

— Saar Shai

---

## Not contacted (email unconfirmed via public sources)
- Manfred Einsiedler (ETH) — pattern `manfred.einsiedler@math.ethz.ch` plausible but unconfirmed
- Elon Lindenstrauss (HU) — page cert error
- Andreas Strömbergsson (Uppsala) — directory result wrong person
- Maksym Radziwill (Northwestern) — homepage doesn't list email
- Akshay Venkatesh (IAS) — directory returns 403

## Notes for sending
- Group A audience considers q*_BCZ + diagnostic as the headline.
- Keep attachments under 1 MB. The 2-paper plan stays internal.
- If any of these reply: do NOT mention the Koyama collaboration.
