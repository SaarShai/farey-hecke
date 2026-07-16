# Formula-level novelty audit

## Claim boundary

This audit supports only three bounded statements:

1. T1/T2 resolve a conjecture already documented in this repository.
2. The focused sources and searches below did not reveal the exact
   moving-multiplier triangular law or the arbitrary denominator-portfolio
   prime-step formulation.
3. The gap-permutation moment identities are classical finite-population
   machinery; the bounded contribution is applying the second and fourth
   moments to the conjecture published by García on 2026-07-15, deducing its
   qualitative two-sided bound, and turning the deduction into a certificate.

It does **not** establish exhaustive external novelty.

## Nearest known bodies of work

| New formulation | Nearest prior art | Safe distinction | Risk |
|---|---|---|---|
| \((a/b,\{pa/b\})\) over \(b<p\) has quantitative star discrepancy | Classical Farey equidistribution; BCZ/horocycle periodic-orbit equidistribution; Ramanujan-sum bounds | Multiplier grows with the Farey order; proof uses a moving Fourier frequency and a sub-resonant ETK box | Medium until specialist search |
| Triangular law for \(a/b-\{pa/b\}\) | Difference of two independent uniforms is classical; Dedekind-sum distributions and averages are extensive | Independence is proved for this coupled Farey shear, with an error rate and exact odd cancellation | Medium |
| Exact primitive-layer Gram kernel | Franel/Mikolás Farey \(L^2\); sawtooth gcd covariance; Ramanujan Parseval/product means | Arbitrary primitive denominator layers and explicit local factors for the pair-multiplicative quantity \(12K\) | High; likely classical identity in another notation |
| Prime energy driver \((p-1)(2-A(p-1))/(6p)\) | Static Farey/Mertens formulas; standard \(\zeta(s+1)/\zeta(s)\) coefficient machinery | Exact marginal-energy interpretation for the denominator-layer Gram portfolio | Medium/high |
| Gap-permutation moments and discrepancy | Classical sampling-without-replacement second/fourth moments; classical 1D \(L^2\) discrepancy; García's new \(L^1\) conjecture | Their sharp García-specific reduction proves the conjecture with \(c_1=9/160\), \(c_2=1/\sqrt6\), and yields an \(O(N)\) certificate | Low ingredient novelty; potentially useful immediate theorem and application |
| CoprimeBatch certificate/optimizer | 1D QMC, kernel quadrature, lattice rules, Farey MMD | Exact complete-reduced-residue batch certificate; optimizer only inside a fixed denominator set and exact layer count | Application synthesis, not pure-math novelty |

## Sources checked

- J. Franel's Farey/RH discrepancy work and the later Mikolás Farey criteria
  (typeset scans linked in the project history audit).
- Cox, Ghosh, Sultanow, [arXiv:2105.12352](https://arxiv.org/abs/2105.12352),
  for the static Farey--Mertens bridge.
- Karvonen, Zhigljavsky,
  [arXiv:2407.10214](https://arxiv.org/abs/2407.10214), for static Farey MMD.
- L. Tóth, [arXiv:1104.1906](https://arxiv.org/abs/1104.1906), and
  Chan--Kumchev, [arXiv:1009.4432](https://arxiv.org/abs/1009.4432), for
  products and moments of Ramanujan sums.
- Athreya--Cheung, [arXiv:1206.6597](https://arxiv.org/abs/1206.6597), for the
  BCZ section and Farey-orbit framework.
- García, [Mathematics 13 (2025), 140](https://www.mdpi.com/2227-7390/13/1/140),
  for exact Farey rank/local discrepancy.
- García, [Mathematics 14 (2026), 2543](https://doi.org/10.3390/math14142543),
  for a gap-based lower bound and the conjectured \(\sigma_gN^{3/2}\) scale of
  permutation-averaged absolute local discrepancy.
- Pozdnyakov--Steele,
  [JMAA 407 (2013), 129--137](https://doi.org/10.1016/j.jmaa.2013.05.010),
  especially equation (13), for the sampling-without-replacement prefix
  variance and related permutation inequalities.
- Isserlis,
  [Proc. Roy. Soc. A 131 (1931), 586--604](https://doi.org/10.1098/rspa.1931.0120),
  for classical fourth moments in sampling without replacement.
- Kirk--Pausinger,
  [Uniform Distribution Theory 18 (2023)](https://doi.org/10.2478/udt-2023-0005),
  and Warnock,
  [Applications of Number Theory to Numerical Analysis (1972)](https://doi.org/10.1016/B978-0-12-775950-0.50015-7),
  for classical one-dimensional \(L^2\)-discrepancy formulas.
- Pătraşcu--Pawlewicz,
  [arXiv:0708.0080](https://arxiv.org/abs/0708.0080), for fast Farey statistics.
- Girstmair and the cited Dedekind-sum literature for generalized sawtooth
  correlations and their distributions.

Searches were performed both by terminology and by formulas resembling
`sum c_m(k)c_n(k)/k^2`, `gcd(d,e)^2/(de)`, `zeta(s+1)/zeta(s)`, and the graph
`(x,{p x})` over Farey fractions.  Search absence is not evidence of absence.

## Known potholes carried into the wording

- The prime Fourier/Farey bridge is static prior art; only a per-step reading is
  project-specific.
- The full Mertens-sign architecture is false or contradicted by historical
  artifacts and is not part of this paper.
- Compile-clean formal files elsewhere in the repository do not certify the
  present asymptotic theorem.
- The kernel proof is elementary once written down.  Elegance and usefulness do
  not imply external novelty.
- A global factor does not preserve multiplicativity: \(12K\) is
  pair-multiplicative, while \(K\) is not.
- Midpoint grids are globally optimal in the stated Sobolev class.  Prime
  layers and divisor portfolios also give admissible uniform interior grids;
  the batch optimizer's only win is inside its exact range/layer constraint.
- The gap-permutation result proves existence of two universal constants, not
  García's sharper provisional constants or the minimum-ordering problem.  Its
  moment and continuous-\(L^2\) ingredients are explicitly credited as
  classical; novelty is claimed only for the García-specific deduction.

## Pre-publication search still required

1. MathSciNet/Zentralblatt search for Farey shear, moving dilations, and
   distributions of \(x-\{nx\}\) over rational points of bounded height.
2. Formula search in Dedekind--Rademacher/cotangent-sum literature for the exact
   primitive-layer covariance.
3. Search in RKHS/kernel quadrature for complete reduced-residue batch Gram
   matrices.
4. Specialist review by an analytic number theorist before using "new theorem"
   outside the project.
5. Check whether the exact deduction of García's two-sided conjecture has
   already been circulated in discrepancy or random-bridge language, even
   though it is absent from García's paper.  The constituent moment formulas
   themselves are already known.
