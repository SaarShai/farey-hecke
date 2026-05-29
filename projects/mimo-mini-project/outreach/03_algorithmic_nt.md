# Outreach drafts — Algorithmic / analytic number theory (broader audience)

**Status**: DRAFT (not sent). Review before use.
**Date**: 2026-05-27
**Common attachments**: 1-page Jordan-totient reduction note + cluster=2 diagnostic table

---

## 1. Brian Conrey — `conrey@aimath.org`
**Subject**: Cluster=2 universality diagnostic + Jordan-totient reduction — AIM relevance?

Dear Professor Conrey,

Two related results from recent work I thought might fit an AIM workshop:

(1) A computable cluster-size diagnostic that separates the Farey/BCZ universality class (~95% size-2 clusters at extreme-quantile q = 0.99 in direct enumeration; 88-99.6% in 50M Monte Carlo of the BCZ chain) from all classical Wigner-Dyson ensembles (0.5-0.75% under the same statistic). The closed-form threshold is q*_BCZ = (11 − 8·ln(3/2))/9 ≈ 0.86181. Riemann ζ zeros (LMFDB 100k) sit at 3%, consistent with GUE at low q. (2) A Jordan-totient convolution identity reducing 3D arithmetic-function sums Σ_{d,d'} gcd² f(Q/d)g(Q/d')/(dd') to 1D forms.

Together they are perhaps 1.5 papers' worth of content (one for *Annals of Applied Probability* / *Experimental Math*, one for *J. Number Theory*). I'd value your reading on whether either lands inside an active AIM working-group theme — especially the cluster diagnostic for spacing universality. I can share the data, derivation notes, and Lean 4 partial formalization at your convenience.

— Saar Shai

---

## 2. Peter Sarnak — `sarnak@math.princeton.edu`
**Subject**: Closed-form universality threshold for BCZ chain dynamics — diagnostic for spacing classes

Dear Professor Sarnak,

I obtained a closed-form universality threshold q*_BCZ = (11 − 8·ln(3/2))/9 ≈ 0.86181 for the size-2/size-3+ cluster transition in the BCZ chain (equivalently the Boca-Cobeli-Zaharescu density on the {x+y>1} triangle). The threshold matches 10⁶ Farey enumeration and 50M Monte Carlo of the chain to ±5×10⁻⁴, and a companion cluster-size statistic separates the BCZ/Farey class (~95% size-2 at q=0.99) from Wigner-Dyson (0.5–0.75%) by two orders of magnitude — placing it as a candidate diagnostic for "intermediate statistics" in the Katz-Sarnak framework.

Given your interest in spacing-statistics universality and the Katz-Sarnak heuristic, I'd appreciate any reading on (a) whether this lands as a recognizable item in the universality taxonomy and (b) whether the diagnostic deserves application to families of automorphic L-zeros. Lean 4 partial formalization, derivation notes, and the comparison table are ready to share.

— Saar Shai

---

## 3. Andrew Odlyzko — `odlyzko@umn.edu`
**Subject**: New convergent Mertens-square constant + cluster diagnostic on ζ zeros

Dear Professor Odlyzko,

Two empirical findings from a recent computational session that may interest you:

(1) Σ_{n≥1} M(n)²/n³ = 1.1361623076908 to 13 stable digits at N = 10⁸ (computed directly, cross-checked via the Mellin transform 𝒯(s) = 1/(s²·ζ(s))). The constant does not appear in OEIS or in references I've consulted. (2) A cluster-size diagnostic at extreme quantile q = 0.99 places Riemann ζ-zero spacings (your LMFDB 100k data) at 3% size-2 clusters — consistent with GUE at low q — while the Farey/BCZ universality class sits at 95%, a clean 30× separation.

Given your foundational computational work on M(x) and on ζ-zero statistics, I would welcome your reading on whether the 1.13616 constant has been previously computed (possibly in a context I missed), and whether the cluster diagnostic is consistent with your long experience computing zero spacings. Notes + data ready to share.

— Saar Shai

---

## 4. John Cremona — `J.E.Cremona@warwick.ac.uk`
**Subject**: Two computational-NT findings for possible LMFDB relevance

Dear Professor Cremona,

I'm writing about two recent computational findings that may have small LMFDB relevance:

(1) A new convergent constant Σ M(n)²/n³ = 1.1361623076908 (13 stable digits at N = 10⁸), candidate for LMFDB's "named constants" if it remains unattested elsewhere. (2) A cluster-size diagnostic on extreme-quantile gaps (q ≥ 0.99) which separates the Farey/BCZ universality class (88–95% size-2) from classical RMT ensembles (0.5–0.75%) and places Riemann ζ-zeros (your 100k LMFDB data) at 3% — consistent with GUE at low q. The diagnostic is potentially applicable to any spacing-statistics dataset that LMFDB hosts (Dirichlet L-zeros, modular form Hecke eigenvalues, etc.).

Would either of these be of interest as community-contributed computations or as a test-bed for the LMFDB zeros corpus? I have a short note, raw data, and reproducible Kaggle pipeline ready to share.

— Saar Shai

---

## Not contacted (unconfirmed)
- Andrew Granville — Montréal homepage stub, no email visible; can try via co-author chain
- Jonathan Keating — Oxford/Bristol pages returning 404
- Nina Snaith — Bristol page 404

## Notes for sending
- Group C is the "broad audience" group — keep claims modest, lead with the diagnostic.
- For Sarnak in particular: do NOT claim it solves the Katz-Sarnak universality problem. Frame as a diagnostic, not a theorem about families.
- Cremona angle is the most concrete: LMFDB integration is a clean ask.
