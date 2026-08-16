# Prior-art scan — low-discrepancy sampling / QMC / hyperuniformity angle

**Date:** 2026-08-16 · **Lane:** practical-value prior art (replaces a dead codex lane)
**Scope:** is there practical/market value in (a) our Farey critical-hyperuniformity finding
S(k) ~ k^{1.8–1.9}, (b) Farey/Stern–Brocot low-discrepancy expertise, (c) certified numerics
applied to discrepancy bounds?

## Bounded-scan caveats (read first)

- Web-search only (WebSearch/WebFetch), one session, ~25 sources inspected, 8 questions'
  worth of ground covered at survey depth. **No paywalled full texts were read**; several
  judgements rest on abstracts, arXiv HTML, and search snippets.
- **No systematic database sweep** (no MathSciNet / zbMATH / Web of Science). A negative
  ("we found no paper on X") here means *not surfaced by targeted keyword search*, not
  *proven absent*. Treat all novelty claims below as ≤ 80% confidence.
- Our own asset was re-read locally
  (`research_notes/PAPER_arithmeticity_dichotomy_SUBMISSION.md` Appendix C;
  `research_notes/twin_index_hyperuniformity_2026-06-14.md`) to fix exactly what is claimed:
  rescaled Farey point set, S(k) ~ k^{1.8–1.9}, estimator validated against Poisson /
  lattice / jittered-lattice controls, `[NUMERICAL]` only — **no proof**.
- No git commands were run.

---

## Q1. Is "hyperuniformity of number-theoretic point sets" an active literature?

**Yes — very active, and it has been for ~8 years.** This is not an open field.

Anchors:

1. Torquato, Zhang, de Courcy-Ireland, *Uncovering multiscale order in the prime numbers
   via scattering*, J. Stat. Mech. (2018) 093401. arXiv:1802.10498.
   DOI: 10.1088/1742-5468/aad6be —
   https://arxiv.org/abs/1802.10498 ·
   https://iopscience.iop.org/article/10.1088/1742-5468/aad6be
   Primes in suitable intervals are *effectively limit-periodic*, dense Bragg peaks at
   rational wavenumbers, and hyperuniform in that regime.
2. Torquato, Zhang, de Courcy-Ireland, *Hidden multiscale order in the primes*,
   J. Phys. A 52 (2019) 135002. arXiv:1804.06279 — https://arxiv.org/abs/1804.06279
3. Zhang / Martelli et al., *The structure factor of primes* —
   https://arxiv.org/pdf/1801.01541 (independent, near-simultaneous).
4. Brauchart, Grabner, Kusner, Ziefle, *Hyperuniform point sets on the sphere:
   deterministic constructions* / *…probabilistic aspects*, Constr. Approx. (2018/2019).
   arXiv:1709.02613, arXiv:1809.02645 — https://arxiv.org/abs/1709.02613
5. *Hyperuniform point sets on flat tori: deterministic and probabilistic aspects*,
   Constr. Approx. (2020). DOI: 10.1007/s00365-020-09512-3. arXiv:1902.02973 —
   https://arxiv.org/pdf/1902.02973
6. *Hyperuniform point sets on projective spaces* (2024) — https://arxiv.org/html/2403.03572
7. *Hyperuniformity of self-similar point processes* (2023) — https://arxiv.org/pdf/2310.20517
8. Oğuz, Socolar, Steinhardt, Torquato, *Hyperuniformity and anti-hyperuniformity in
   one-dimensional substitution tilings*, Acta Cryst. A75 (2019) —
   https://journals.iucr.org/a/issues/2019/01/00/vf5001/

**Farey specifically:** four separate keyword attacks (Farey + hyperuniform, Farey +
structure factor, Farey + number variance, Farey + diffraction) surfaced **no paper**
computing the structure factor or hyperuniformity class of the Farey point set. The nearest
neighbours are Huxley–Zhigljavsky on Farey-fraction distribution vs hyperbolic lattice
points (https://ssa.cf.ac.uk/zhigljavsky/pdfs/number%20theory/Huxley_Zh.pdf) and the
substitution-tiling / self-similar HU papers above, which cover Stern–Brocot-*like*
self-similar structures in the abstract but not F_Q.

**Assessment.** The *exponent* α ≈ 1.8 for Farey looks unpublished. But the *framework* is
saturated, the technique (estimate S(k), read off α) is routine, and the 1-D marginal /
class-II-boundary regime is well-catalogued. This is a "fill in one more row of the table"
result, not a new phenomenon. Also note the exponent is soft: our own note gives a range
1.8–1.9 and describes the set as sitting *exactly on* the d=1 perturbed-lattice edge — a
referee will ask whether the true answer is the clean marginal α = 2 with a log, which is
precisely the boundary case the substitution-tiling literature already treats.

---

## Q2. Does the QMC community use hyperuniformity as a quality measure?

**The crossover already exists and is owned by the Graz school (Brauchart–Grabner–Kusner)
plus the DPP/statistics community.** Specifically:

- The flat-tori and sphere papers prove **hyperuniformity ⟹ uniform distribution**, and that
  **QMC-design sequences of strength ≥ (d+1)/2, spherical designs of optimal growth order,
  jittered samplings, and certain determinantal point processes are hyperuniform**
  (arXiv:1902.02973; DOI 10.1007/s00365-020-09512-3). That *is* the discrepancy ↔ structure
  factor bridge, already built.
- Hawat, Gautier, Bardenet, Lachièze-Rey, *On estimating the structure factor of a point
  process, with applications to hyperuniformity*, Statistics and Computing 33 (2023).
  DOI: 10.1007/s11222-023-10219-1. arXiv:2203.08749 —
  https://arxiv.org/abs/2203.08749 — plus shipped software `structure-factor`
  (https://for-a-few-dpps-more.github.io/structure-factor/). Estimating S(k) for a point
  process is a solved, packaged problem.
- Dick, Goda, Suzuki, *On the quasi-uniformity properties of QMC point sets and sequences,
  Part I* (2025), arXiv:2502.06202 — the community's own "second quality metric beyond
  discrepancy" work uses **quasi-uniformity / covering radius**, not the structure factor.

**Is the field saturated for new constructions?** Mostly, but not entirely — and the
appetite is real, just already being fed:

- Rusch, Kirk, Bronstein, Lemieux, Rus, *Message-Passing Monte Carlo: generating
  low-discrepancy point sets via graph neural networks*, PNAS 121 (2024) e2409913121.
  DOI: 10.1073/pnas.2409913121. arXiv:2405.15059 — https://arxiv.org/abs/2405.15059.
  Near-optimal star discrepancy for small n, low d.
- Clément, Doerr, Paquete, *Heuristic approaches to obtain low-discrepancy point sets via
  subset selection*, arXiv:2306.15276; and the IOHprofiler **Star Discrepancy Competition**
  (https://iohprofiler.github.io/competitions/stardiscr24) — an organised community
  benchmark, i.e. the "find better point sets" niche is now a *competition* with incumbents.
- *A Bayesian approach to low-discrepancy subset selection*, arXiv:2602.14607 (2026).
- QMCPy (Choi, Hickernell et al.), arXiv:2502.14256 — the practitioner-facing library;
  rank-1 lattices, digital nets, Halton, randomisations. Any new construction must land here
  to be used.

**Fatal problem for the Farey angle.** Farey is a *1-dimensional* construction, and QMC in
d = 1 is trivially solved (equispaced / van der Corput give D_N ≍ N^{-1} log N or better).
Worse, the Farey set is a **bad** low-discrepancy set: its star discrepancy is exactly
D(F_Q) = 1/Q, and |F_Q| ~ 3Q²/π², so D ≍ N^{-1/2} — *Monte-Carlo rate, not QMC rate*. See
the closed-form discrepancy statement in *A general lower bound for average local
discrepancy and an application to the Farey sequence*, Mathematics 14 (2026) 2543,
https://www.mdpi.com/2227-7390/14/14/2543, and the classical Franel–Landau equivalence
(RH ⟺ Farey L¹-deviation is o(x^{1/2+ε})). Farey fractions are studied *because* their
irregularity encodes RH — the opposite of what a sampler wants. So "Farey as a new
low-discrepancy construction" is dead on arrival; hyperuniformity does not rescue it,
because HU controls large-scale density fluctuations while QMC error is governed by the
worst local box.

---

## Q3. Would a certified star-discrepancy tool (rigorous enclosures) be new/wanted?

**Wanted-ish; not new; and the hard part is not the certification.**

State of the art:

- Exact: Dobkin–Eppstein–Mitchell (DEM), O(n^{1+d/2}); usable to about d = 8 for a few
  hundred points, d = 10 for a few dozen. Summarised in Clément et al.,
  *Computing star discrepancies with numerical black-box optimization algorithms*,
  arXiv:2306.16998 — https://arxiv.org/pdf/2306.16998
- Hardness: Giannopoulos, Knauer, Wahlström, Werner, *Hardness of discrepancy computation
  and ε-net verification in high dimension*, J. Complexity 28 (2012) —
  NP-hard and W[1]-hard. So no exact tool will ever scale.
- **Rigorous upper bounds already exist**: Thiémard, *An algorithm to compute bounds for the
  star discrepancy*, J. Complexity 17 (2001) 850–880. DOI: 10.1006/jcom.2001.0600 —
  https://www.sciencedirect.com/science/article/pii/S0885064X01906004 — δ-bracketing covers,
  deterministic guaranteed enclosure.
- Gnewuch's bracketing-cover cardinality improvements, and the 2024 revisit:
  *Improved bounds for the bracketing number of orthants, or revisiting an algorithm of
  Thiémard…*, arXiv:2401.00801 — https://arxiv.org/abs/2401.00801. Active, current, 2024.
- Lower bounds: TA / TA_improved (threshold accepting, Gnewuch–Wahlström–Winzen), genetic
  algorithms (arXiv:1304.1978), random-walk estimators
  (https://www.degruyterbrill.com/document/doi/10.1515/mcma-2022-2125/html).

So the **enclosure** (upper bound, guaranteed) is Thiémard-2001 + Gnewuch, and the
**certified interval** is upper-bound ∩ heuristic lower bound. Our differentiator would be
Arb/interval-arithmetic rigour — but the existing upper bounds are already *combinatorially*
rigorous, not floating-point-fragile; discrepancy is a max of differences of counts and
volumes, so rounding error is not the bottleneck. **Certified numerics buys almost nothing
here.** The real gap is *engineering*: no widely used, maintained package ships Thiémard's
bounds. QMCPy does not; the competition entrants ship research code. A well-packaged
`star-discrepancy-bounds` (Thiémard + Gnewuch covers + TA lower bound, QMCPy-compatible)
would plausibly get users — but it is software plumbing over other people's algorithms,
carries no research credit, and the IOHprofiler competition crowd may already have
consolidated code we did not surface in this bounded scan (**flagged as the biggest
unchecked risk in this document**).

---

## Q4. Verdict

| Angle | Verdict |
|---|---|
| Farey hyperuniformity S(k)~k^1.8 as a *finding* | **Niche contribution** — likely unpublished exponent, saturated framework, low impact |
| Hyperuniformity as a QMC quality measure | **Commodity** — Graz school owns it since 2018 |
| Farey/Stern–Brocot as a new low-discrepancy construction | **Dead** — D(F_Q)=1/Q ≍ N^{-1/2}, worse than MC-rate competitors; d=1 anyway |
| Certified star-discrepancy tool | **Commodity algorithm, open engineering slot** — no research novelty; modest tool value; unverified competitor risk |

**Overall: niche-contribution, tending to commodity.** Nothing here is genuinely open in the
sense the project cares about, and the practical-value story is weaker than the pure-math
story — consistent with the existing local ruling in
`research_notes/wide_appeal_verdict_2026-06-13.md` ("the value of this work is mathematical").

**Single best-value artifact, if any is produced:** a *short* Experimental Mathematics /
INTEGERS-style note, "The Farey point set is critically hyperuniform", ~6 pages: the
estimator + controls we already ran, the Stern–Brocot gap-anticorrelation mechanism, the
C/T² gap tail ⇒ marginal-class derivation, and an explicit statement that this does **not**
make Farey a good QMC sampler (citing D(F_Q)=1/Q and Franel–Landau). Cost is low — the
numerics exist — and it converts a stranded appendix remark into a citable unit. Pre-condition:
a real MathSciNet/zbMATH sweep for "Farey + hyperuniform/structure factor", because this whole
recommendation hangs on a keyword-search negative.

**Do not** build a discrepancy-bounds tool as a research bet, and **do not** pitch Farey as
a sampling construction.

## Source list

- https://arxiv.org/abs/1802.10498 · DOI 10.1088/1742-5468/aad6be
- https://arxiv.org/abs/1804.06279
- https://arxiv.org/pdf/1801.01541
- https://arxiv.org/abs/1709.02613 · https://arxiv.org/pdf/1809.02645
- https://arxiv.org/pdf/1902.02973 · DOI 10.1007/s00365-020-09512-3
- https://arxiv.org/html/2403.03572
- https://arxiv.org/pdf/2310.20517
- https://journals.iucr.org/a/issues/2019/01/00/vf5001/
- https://arxiv.org/abs/2203.08749 · DOI 10.1007/s11222-023-10219-1 · https://for-a-few-dpps-more.github.io/structure-factor/
- https://arxiv.org/abs/2502.06202
- https://arxiv.org/abs/2405.15059 · DOI 10.1073/pnas.2409913121
- https://arxiv.org/pdf/2306.15276 · https://iohprofiler.github.io/competitions/stardiscr24
- https://arxiv.org/pdf/2602.14607
- https://arxiv.org/abs/2502.14256 (QMCPy)
- https://arxiv.org/pdf/2306.16998
- https://www.sciencedirect.com/science/article/pii/S0885064X01906004 · DOI 10.1006/jcom.2001.0600
- https://arxiv.org/abs/2401.00801
- https://arxiv.org/pdf/1304.1978 · https://www.degruyterbrill.com/document/doi/10.1515/mcma-2022-2125/html
- https://www.mdpi.com/2227-7390/14/14/2543
- https://ssa.cf.ac.uk/zhigljavsky/pdfs/number%20theory/Huxley_Zh.pdf
