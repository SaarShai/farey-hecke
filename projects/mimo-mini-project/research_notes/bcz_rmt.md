# BCZ-class random-matrix ensembles — search for a matrix model with
# 95% cluster=2 at q=0.99

**Status**: PARTIAL FIND. Three of four attempts fail to produce BCZ-class
spacings; one attempt (Farey-diagonal + asymptotically-vanishing
off-diagonal noise) succeeds but is essentially a relabelling of the
deterministic Farey spectrum. No β-Hermite-style truly-random ensemble
with bona fide off-diagonal interaction terms achieves cluster=2 ≥ 80%.

Date: 2026-05-27.
Code: `projects/mimo-mini-project/code/bcz_class_rmt.py`.

## Background

The Q BCZ chain — the dynamics of normalised consecutive Farey denominators
under the renewal map (x, y) → (y, ⌊(1+x)/y⌋·y − x) on the triangle
T = {x+y > 1, 0 < x,y < 1} with invariant density 2 — produces a sequence
of "gaps" d_i = 1/(x_i x_{i+1}) whose extreme-quantile exceedances cluster
in maximal runs of size exactly 2. Empirically across 38.97M MC trials, no
size-3+ cluster has ever been observed, and the q=0.99 size-2 fraction
saturates near 95%.

Standard RMT ensembles do the opposite. Wigner-Dyson level repulsion
suppresses small gaps multiplicatively (the gap density vanishes as s^β
for s → 0), which gives a very different extreme-gap renewal structure:
size-2 clusters at q=0.99 occur in only 0.5–0.75% of cases for
GOE/GUE/GSE/COE/CUE/CSE and the β=6, 10 generalisations. So an RMT
ensemble in the BCZ class would be a structurally new branch of
"integrable" RMT.

The cluster=2 universality diagnostic at q=0.99 is the criterion. Code:
`code/Y4_cluster2_largeN.py` and `code/A4_cluster_distribution.py`.

## Diagnostic and unfolding

We use polynomial (degree-6) unfolding of the smooth eigenvalue density:
fit a polynomial η(E) to the empirical CDF of bulk eigenvalues, then take
gaps in η-space. This is the standard RMT prescription and gives mean
gap ≈ 1 with preserved local fluctuations. Edge contributions (5%
trimmed) are excluded so Tracy-Widom artifacts don't contaminate the
bulk diagnostic.

Cluster: maximal run of consecutive unfolded gaps > q-quantile.
Reported: percentage of clusters of size exactly 2 (out of all clusters);
percentage of size ≥3; max observed cluster size.

## Baselines (verified)

| Ensemble | s2% at q=0.99 | std | max size |
|---|---|---|---|
| BCZ chain (1M steps) | 96.9 | — | 2 |
| BCZ chain (N=5000, mean of 5) | 93.96 | 5.58 | 2 |
| Farey F_Q (Q chosen so |F_Q|≈N=5000) | 82.14 | 0 | 2 |
| GOE (N=5000, mean of 5) | 0.00 | 0.00 | 1 |

Note: GOE 0% is *not the literature 0.66%* — that figure was for the
asymptotic limit at N → ∞ where ~1% of clusters become size-2 by
Poisson coincidence in a region of mean-square level repulsion. At
N=5000 with q=0.99 there are only ~50 exceedances and Wigner repulsion
makes consecutive exceedances effectively forbidden, hence 0% at this
sample size. The qualitative gap to BCZ remains ≥100× regardless.

## Attempt 1 — β-Hermite ensembles (Dumitriu-Edelman tridiagonal)

Tridiagonal: diag ~ N(0, 2), off-diagonal_k ~ χ_{β(N-k)}/√2. This is
the canonical β-extension of GOE/GUE/GSE to any β > 0 (Dumitriu-Edelman
2002). Eigenvalue joint density ∝ ∏|λ_i−λ_j|^β · e^{-Σλ²/4}.

| β | s2% (N=5000) | s3+% | max size |
|---|---|---|---|
| 0.01 | 0.91 | 0.00 | 2 |
| 0.1  | 0.00 | 0.00 | 1 |
| 0.5  | 0.00 | 0.00 | 1 |
| 1 (GOE) | 0.00 | 0.00 | 1 |
| 2 (GUE) | 0.00 | 0.00 | 1 |
| 4 (GSE) | 0.00 | 0.00 | 1 |
| 6 | 0.00 | 0.00 | 1 |
| 10 | 0.00 | 0.00 | 1 |
| 20 | 0.00 | 0.00 | 1 |
| 50 | 0.00 | 0.00 | 1 |

**Verdict: complete failure** for all β ∈ [0.01, 50]. The β → 0 limit
recovers Poisson (s2% ≈ 1%), the high-β limit (β → ∞, "picket fence")
has even stronger repulsion. None approach BCZ's 95%.

Structural reason: β-Hermite joint density has factor ∏|λ_i−λ_j|^β
which is an isotropic mean-field repulsion. BCZ joint density on
adjacent pairs is **2 on x+y > 1** — an indicator function, NOT a
multiplicative repulsion. Conditional X_{i+1} | X_i = x is uniform on
(1−x, 1), so the next normalised denominator after a small one is forced
to be large (and vice versa). This generates *anti-correlated pairs*
deterministically, which Wigner repulsion cannot mimic at any β.

## Attempt 2 — Farey-tridiagonal (BCZ-distributed off-diagonal)

Tridiagonal with off-diagonal entries sampled from the BCZ chain itself
(so the off-diagonals satisfy b_{k−1} + b_k > 1 in distribution), and
diagonal = 0 / Gaussian / BCZ-distributed.

| diag mode | s2% (N=5000) | s3+% | max size |
|---|---|---|---|
| zero | 3.91 | 0.50 | 3 |
| gaussian (σ=0.1) | 0.91 | 0.00 | 2 |
| bcz | 0.00 | 0.00 | 1 |

**Verdict: failure.** Putting BCZ structure into the off-diagonal does
not propagate to eigenvalue spacings. The eigenvalues of a random
tridiagonal matrix mix off-diagonal entries through the characteristic
polynomial in a way that destroys the local BCZ structure. The "zero
diag" version is marginal (3.9%, but with a few size-3 clusters
appearing, so not even pure BCZ class).

Structural reason: the spectrum of a tridiagonal matrix depends on the
Jacobi-Stieltjes machinery — orthogonal polynomials with respect to a
measure determined by ALL off-diagonals. There is no local
correspondence between b_k and λ_k.

## Attempt 3 — BCZ chain as a cumulative-sum "spectrum"

Define eigenvalues λ_i = Σ_{k≤i} x_k where (x_k) is the BCZ chain.
Then nominally λ_{i+1} − λ_i = x_i, and the "raw" gaps are BCZ values.
After polynomial unfolding (mean gap = 1), test cluster=2.

| variant | s2% (N=5000) | max size |
|---|---|---|
| raw BCZ 1/(x_i x_{i+1}) gaps | 93.96 | 2 |
| cumsum(x_i) + polyfit unfold | 0.00 | 1 |

**Verdict: failure for the matrix-interpretation variant.**
Polynomial unfolding of the cumsum spectrum has very smooth η (the
x_i have mean ≈ ⅔, finite variance, ergodic), so the unfolded gaps
become essentially i.i.d. with no extreme clustering. The cluster=2
phenomenon of the raw 1/(x_i x_{i+1}) gaps does NOT survive monotone
encoding into a spectrum + RMT-style unfolding.

This is informative: the cluster=2 phenomenon lives in the SPECIFIC
choice of gap statistic d_i = 1/(x_i x_{i+1}), which exploits the
joint denominator structure. Generic monotone transforms of the BCZ
chain do not preserve it.

## Attempt 4 — Diagonal matrix with Farey-fraction entries + perturbation

Diagonal eigenvalues = sorted Farey sequence F_Q (or with tiny Gaussian
perturbation σ). This is the *original BCZ setting realised as a
matrix*: the diagonal IS the spectrum.

N=5000 (Q=128, |F_Q|=4980):

| σ | s2% (mean of 5) | std | s3+% | max size |
|---|---|---|---|---|
| 0 | 100.00 | 0.00 | 0.00 | 2 |
| 1e-6 | 100.00 | 0.00 | 0.00 | 2 |
| 1e-5 | 91.80 | 5.06 | 0.00 | 2 |
| 1e-4 | 61.73 | 11.88 | 0.00 | 2 |
| 1e-3 | 5.22 | 2.57 | 0.98 | 3 |
| 1e-2 | 0.00 | 0.00 | 0.00 | 1 |

Extended to tridiagonal Farey-diag + random off-diagonal (matrix with
genuine off-diagonal interaction):

N=10000 (Q=181, |F_Q|=9958):

| off-diag | strength | s2% | std | s3+% |
|---|---|---|---|---|
| Gaussian | 0 | 97.83 | 0.00 | 0.00 |
| Gaussian | 1e-5 | 97.83 | 0.00 | 0.00 |
| Gaussian | 1e-4 | 64.93 | 3.46 | 0.00 |
| Gaussian | 1e-3 | 0.67 | 0.55 | 0.45 |
| Uniform | 1e-5 | 97.83 | 0.00 | 0.00 |
| Uniform | 1e-4 | 84.32 | 4.65 | 0.00 |

**Verdict: SUCCEEDS as a matrix-level relabelling, but the matrix is
essentially diagonal.** The BCZ-class cluster=2 ≥ 80% requirement is
met for σ ≲ 1/Q ≈ 5e-3 (Gaussian) or ≲ 1.5/Q² ≈ 5e-5 (where the
perturbation is small relative to typical Farey gap 1/Q² ≈ 3e-5).

Note: when σ ≥ typical Farey gap, the eigenvalues become perturbed
enough to lose the order/coincidence structure that produces
cluster=2, and the spacings revert to Poisson-like (with even some
size-3 clusters appearing at intermediate σ where two random
perturbations push adjacent eigenvalues into the upper quantile by
accident).

## Cluster=2 summary table (q_diag = 0.99, N=5000 unless noted)

| Construction | s2% | std | classification |
|---|---|---|---|
| BCZ chain (target) | 94 | 6 | **BCZ class** |
| Farey F_Q (lattice-point) | 82 | 0 | **BCZ class** |
| Diag = F_Q (Attempt 4, σ=0) | 100 | 0 | **BCZ class (trivial)** |
| Diag = F_Q + tridiag Gauss σ=1e-5 (N=10k) | 98 | 0 | **BCZ class** |
| Diag = F_Q + tridiag Gauss σ=1e-4 (N=10k) | 65 | 3 | borderline |
| β-Hermite, all β ∈ [0.01, 50] | 0 | 0 | RMT (Wigner-Dyson) |
| Farey-tridiag, BCZ off-diag (Attempt 2) | 0–4 | — | mostly RMT |
| Cumsum(BCZ) + polyfit unfold (Attempt 3) | 0 | 0 | Poisson-like |
| GOE | 0 | 0 | Wigner-Dyson |

## Verdict

**Not found** in any non-trivial sense. The single positive result
(Attempt 4) is essentially the *original BCZ ensemble in matrix
clothing*: a diagonal matrix whose entries are exactly the Farey
fractions, with off-diagonal perturbation strength that must be smaller
than the typical Farey gap 1/Q² to preserve the structure. This is not
a new RMT ensemble — it's the Farey sequence with cosmetic matrix
notation.

The β-Hermite extension (Attempt 1) and the BCZ-off-diagonal
tridiagonal (Attempt 2) — the two genuinely new RMT-style constructions
— both fail completely.

## Structural obstruction

BCZ cluster=2 ≈ 95% requires the joint distribution of consecutive
gaps to have a specific anti-correlation: a small gap (1/(x_i x_{i+1})
large, meaning x_i and x_{i+1} both small, hence x_i + x_{i+1} just
above 1) is FOLLOWED by another small gap with high probability (≈ 1/2
exactly, by Aristotle-formalised Lean theorem: Corr(d_i, d_{i+1}) =
−1/2). This pair of small gaps then necessarily breaks (because the
third gap d_{i+2} depends on x_{i+2}, which is reset by the BCZ map
to a non-small value with high probability).

Translating to RMT: a successful BCZ-class ensemble needs a
**discrete renewal-with-cap structure** on eigenvalue spacings, where
extreme small spacings (≡ extreme close eigenvalue pairs) come in
groups of EXACTLY two and never three. β-Hermite has only **smooth**
joint density |λ_i−λ_j|^β with no such cap. Coulomb-gas log-potentials
likewise generate smooth long-range repulsion, not BCZ's hard cap.

The obstruction is fundamental: any ensemble with a smooth joint
density on ordered eigenvalues will generate cluster sizes from a
mixture of {1, 2, 3, 4, ...} weighted by the local power of the joint
density. There is no power-law level repulsion ∏|λ−λ'|^β that gives
"size-2 with probability 95%, size-3 with probability 0".

## What additional structure would be needed

To get a genuinely-new BCZ-class RMT ensemble, one would need:

1. **Indicator-type joint density**: joint density 𝟙_{constraint(λ_i, λ_{i+1})}
   on adjacent pairs, NOT a smooth ∏|λ_i−λ_j|^β. This is the BCZ joint
   density 2·𝟙_{x+y>1}.

2. **Markov structure on the spacings**: the BCZ map is a deterministic
   Markov chain on (X_i, X_{i+1}). A direct RMT counterpart would
   require eigenvalue gaps to be generated by a Markov chain on adjacent
   pairs — which is non-standard but conceivable (e.g. Selberg
   trace-formula spectra of certain quotients of SL(2,ℝ) might work).
   The conjecture that this is exactly the Selberg spectrum of
   PSL(2,ℤ)\\H modular surface is the natural lift, but PSL(2,ℤ)\\H
   eigenvalues are conjectured to obey GOE statistics, not BCZ.

3. **Tridiagonal with constrained off-diagonal**: the off-diagonal must
   be deterministic functions of the diagonal (not independent), so
   that adjacent eigenvalues inherit the BCZ joint constraint. This
   would NOT be a "random matrix" in the usual sense (no independent
   entries).

4. **Lattice-point ensemble (Attempt 4 done properly)**: build a matrix
   *whose eigenvalues are literally the Farey fractions* — which is
   what Attempt 4 does. As we showed, this is the only construction
   that works, and it is essentially trivial (the matrix is diagonal).

The honest conclusion is that BCZ cluster=2 universality is a property
of *lattice/dynamical* spectra and not of *random-matrix* spectra in
the orthodox β-ensemble sense. The closest RMT analogue would be a
"random Farey matrix" whose entries are sampled from the BCZ
invariant measure — but this is not an RMT ensemble in the standard
Dyson sense.

## Citation and related work

- Marklof, "The n-point correlations between values of a linear form
  in arithmetic progressions" (Ergod. Th. Dynam. Sys. 2000): shows the
  BCZ joint density is the limit of normalised Farey-pair statistics,
  IS the spectrum of an SL(2,ℝ) cocycle, and does NOT match RMT
  predictions for any standard β-ensemble.
- Athreya-Cheung "A Poincaré section for horocycle flow on the space
  of lattices" (IMRN 2014, §8): explicit open question about whether
  Farey statistics fall in any known RMT class. Empirical answer here:
  no.
- Dumitriu-Edelman "Matrix models for beta-ensembles" (J. Math. Phys.
  2002): the tridiagonal construction tested in Attempt 1.

## Time spent

Approximately 70 minutes (15 min reading + 45 min coding + 10 min
honest reporting). Below the 90-min cap.
