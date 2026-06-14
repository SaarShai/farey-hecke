# Citation-grade novelty audit — V1 "θ = 1/2 extremal index for homogeneous-dynamics gap processes"

**Date:** 2026-06-14. **Auditor stance:** default "likely known"; weigh near-misses hard
(we overclaimed once on the reciprocity scan — do not repeat). Method: WebSearch + WebFetch
on the four EVT-for-homogeneous-dynamics papers, the parabolic/intermittent rare-event-EVT
literature (Freitas–Freitas–Todd lineage), the continued-fraction EVT literature, and the
BCZ / slope-gap density literature. Source for the candidate:
`research_notes/theta_half_repp_2026-06-14.md`.

## The statement under audit (V1)
> The extremal index / cluster law of the GAP-PRODUCT (or slope-gap) rare-event point process
> for cross-sections of HOROCYCLE / unipotent flows on cusped homogeneous spaces (BCZ map,
> Hecke G_q-BCZ, Veech slope-gap sections) has a UNIVERSAL value **θ = 1/2** in the large-gap
> (deep-tail) limit, arising from a deterministic **period-2 cusp-return involution** (a ↦ b
> swap), with a DEGENERATE point-mass-at-2 cluster-size law (not the geometric law of the
> standard repelling-periodic theory).

---

## VERDICT: **NOVEL (narrow, methods-honest scope).**

No prior work computes an **extremal index** (or any clustering / compound-Poisson cluster-size
statistic) for **any** horocycle/BCZ/slope-gap gap process. Every adjacent result is one of:
(i) a cusp-EXCURSION extreme-value *law* (Gumbel/Fréchet, **no clustering**, θ implicitly 1) —
the WRONG tail and not a clustering statistic; (ii) a parabolic-EVT result that gives **θ = 0**
at a neutral fixed point (degenerate); (iii) a repelling-periodic compound-Poisson result with a
**geometric** cluster law for a **hyperbolic** point; or (iv) a slope-gap / Farey-gap **density**
computation with no EVT/clustering content. The candidate's specific object (gap-product lower
tail), value (θ = 1/2), mechanism (period-2 cusp-swap involution at a parabolic point), and law
(degenerate δ₂, **non**-geometric) are each absent from the literature, and their combination is
new. **The one caveat that keeps this short of a clean theorem is internal, not prior-art:** the
convergence theorem (REPP limit under the invariant measure) is the named open residual the
candidate already flags, AND — see §"honest sentence" — the very equality θ = 1/E[L] it leans on
is exactly the equality that one of the near-miss papers (1808.02970) shows can FAIL at an
indifferent point. So: novel *object & computation*, but the limit-law claim is conditional and
must be stated as such.

---

## Closest papers (titles + arXiv id + one-line relevance)

1. **Marklof, Pollicott — "Extreme events for horocycle flows"**, arXiv:2408.01781 (2024/25).
   The single closest paper by vocabulary. EVT for the horocycle flow, limit law via **Hall's
   Farey-gap formula**. But the observable is the **maximum cusp EXCURSION** (deepest penetration
   — the large-gap *tail of a single running max*), the limit is an extreme-value *density*
   ω_y(s) with C₁e^{−|s|} ≤ ω_y ≤ C₂e^{−|s|}, and — verified by reading the HTML — they **do NOT
   compute or mention an extremal index, clustering, compound Poisson, or cluster size**. Opposite
   tail to V1's gap-product lower tail; no θ. Does not pre-empt V1.

2. **Kirsebom, Mallahi-Karai — extreme value law for the unipotent flow on SL₂(ℝ)/SL₂(ℤ)**,
   arXiv:2209.07283 (the EVL that Marklof–Pollicott extends).
   Maximum hitting time → **Gumbel**; standard EVT, **no clustering** (extremal index implicitly
   1), no cluster size / compound Poisson. Cusp-excursion observable, not the gap-product. The
   foundational paper of this lineage and it explicitly has no clustering.

3. **Marklof, Strömbergsson, Yu — "Extreme events and impact statistics for unipotent actions on
   the space of lattices"**, arXiv:2510.11371 (2025).
   Rank-k unipotent generalization of #1/#2. Hitting-time + "impact" tail asymptotics; new
   non-Gumbel distributions for k<n−1. Still single-extreme *laws* / tail densities, **not an
   extremal-index / clustering** computation. (Consistent with the prior MEMORY scout: its EVL
   density has exponential support both sides, no hard edge — a different object entirely.)

4. **(Author group Azevedo–Freitas–Freitas–…) — "Rare Events for the Manneville–Pomeau Map"**,
   arXiv:1503.01372 / hal-01127757.
   The closest *parabolic-EVT* near-miss. Confirms the degeneracy the candidate documents: **at
   the neutral/indifferent fixed point ζ=0 the extremal index is θ = 0** ("measures the intensity
   of clustering, is equal to 0 at ζ=0"); non-degenerate limits at ζ=0 are recovered only via
   *adapted normalizing sequences*, **not** a finite θ. Compound Poisson (geometric clusters)
   only at *periodic* points. So the standard parabolic theory gives θ = 0, **not** θ = 1/2 —
   V1's finite θ from a period-2 swap is precisely what this framework does **not** produce. This
   is the paper that most directly shows the candidate's value is not a corollary of known
   parabolic-EVT.

5. **Freitas, Freitas, Todd — "The compound Poisson limit ruling periodic extreme behaviour of
   non-uniformly hyperbolic dynamics"**, arXiv:1204.2304 (CMP 2013).
   The canonical clustering theorem: θ = 1 − 1/|det DTᵖ(ζ)|, cluster law **geometric**
   π(κ)=θ(1−θ)^{κ−1}, for **repelling periodic** points (Rychlik, Manneville–Pomeau periodic
   points, Benedicks–Carleson). Its formula degenerates to θ = 0 at a neutral point and never
   yields a degenerate δ₂ law. V1's δ₂ point-mass + parabolic point are outside its scope.

6. **Azevedo, Freitas, Freitas, Rodrigues — "Dynamical counterexamples regarding the Extremal
   Index and the mean of the limiting cluster size distribution"**, arXiv:1808.02970.
   The closest *mechanism* near-miss: observables maximized at **two** points (one **indifferent**
   periodic, one repelling/non-periodic), giving non-geometric cluster behaviour, AND — load-
   bearing for V1 — they prove **θ ≠ 1/(mean of the limiting cluster size)** can hold (the
   equality survives only as θ⁻¹ = lim of the *finite-time* mean). Purely **abstract interval-map
   constructions**, not homogeneous dynamics, no BCZ/horocycle, no θ = 1/2. Does not pre-empt V1's
   *object*, but it is the precise warning that V1's "θ = 1/E[L] = 1/2" step is not automatic at a
   parabolic point and must be proved, not asserted.

*(Also logged, lower relevance / confirming the gap: ACL golden-L slope-gap 1308.4203, KSW Veech
slope-gap 2102.10069, 2n-gon 2109.04495, double-heptagon 2508.19252, Athreya–Chaika 1204.5642 —
all **density / support-edge**, zero EVT-clustering content. Athreya–Cheung 1206.6597 and BCZ
weakly-mixing 2403.14976 / logarithm-laws 2403.15160 — BCZ ergodic theory, no extremal index.
Continued-fraction EVT — Gauss/Hurwitz digit maxima, arXiv:1904.07582 / 2202.07976 — gets
**θ = 1, Poisson, no clustering**, i.e. even the closely-arithmetic CF processes do not cluster.
2D periodic-orbit compound Poisson 1709.00530 — Pólya–Aeppli/geometric, **hyperbolic** orbits
only.)*

---

## Narrowest genuinely-new version (what survives the audit)

> **"First extremal-index (clustering) computation for a horocycle-section gap process":** the
> deep-tail extreme-gap (gap-product lower-tail) exceedance process of the BCZ / Hecke G_q-BCZ
> horocycle cross-section clusters with extremal index **θ = 1/2**, q-independently, via a
> deterministic **period-2 cusp-swap involution**, with a **degenerate δ₂** (non-geometric)
> cluster-size law — distinct from both (a) the cusp-EXCURSION extreme-value *laws* of
> Marklof–Pollicott / Kirsebom–Mallahi-Karai / MSY (single-max laws, no clustering, other tail),
> and (b) the standard repelling-periodic geometric-cluster theory (FFT 1204.2304), whose formula
> gives θ = 0 at the relevant *parabolic* point.

This is **NOT** subsumed by Marklof–Pollicott (different tail, no θ at all) and **NOT** a corollary
of FFT/parabolic-EVT (θ = 0 there, geometric not δ₂). The genuinely-new content is the
**extremal-index/clustering layer on a homogeneous-dynamics gap process**, which no prior paper
addresses. What is NOT new and must not be claimed: the gap *density/edge* itself (KSW/Taha/ACL),
and the cusp-excursion *EVL* (Marklof–Pollicott et al.). The novelty is strictly the **clustering
statistic of the small-gap tail**, a question the field has simply not posed for these processes.

**Scope downgrades to apply (keep honest):** (i) the candidate's `theta_half` note already grades
itself "(b) proved-modulo-a-named-limit-theorem" — keep that; the REPP convergence under the
parabolic, polynomial-mixing measure is genuinely open and the FFT machinery does not supply it.
(ii) Add the 1808.02970 caveat: at an indifferent point the equality θ = 1/E[L] is *not*
automatic, so the "θ = 1/2 because mean cluster size = 2" line is a deterministic-clustering
heuristic, not yet the extremal index of the stochastic process — these may differ and the gap is
exactly the open theorem.

---

## One honest sentence

The clustering / extremal-index question for the small-gap tail of a horocycle-section gap
process is genuinely **unaddressed in the literature** (every neighbour does either a cusp-
excursion single-max *law* with no clustering, or a repelling-periodic *geometric* cluster theory
that degenerates to θ = 0 at the parabolic cusp), so V1 is a **novel object and computation** —
but it is honestly only a *conjectural* θ = 1/2 until the parabolic REPP limit is proved AND the
θ = 1/E[L] equality is established (which arXiv:1808.02970 shows can fail at exactly this kind of
indifferent point), so claim it as "first extremal-index computation for a horocycle-section gap
process, conditional on a named (open) parabolic limit theorem," not as a finished theorem.
