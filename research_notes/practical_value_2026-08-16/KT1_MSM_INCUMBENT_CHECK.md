# KT1 — Does incumbent MSM uncertainty make certification pointless?

Scope: PyEMMA/deeptime documentation, their indexed GitHub material, and primary MSM literature, checked 2026-08-16. “Not found” below means not found in this bounded scan, not proof of absence.

## 1. Current PyEMMA/deeptime uncertainty treatment

PyEMMA's Bayesian workflow samples MSMs and propagates each sample through the requested observable. Its `SampledMSM` API describes `sample_conf` as a “Sample confidence interval ... over all samples,” alongside `sample_mean` and `sample_std`; timescales are computed as \(-\tau/\log|\lambda_i|\) ([PyEMMA `SampledMSM`](https://www.emma-project.org/v2.2.3/api/generated/pyemma.msm.SampledMSM.html)). The official pentapeptide tutorial says, exactly, “The uncertainty of the implied timescales is quantified based upon Markov models sampled according to a Bayesian scheme,” and plots `sample_mean('timescales') ± sample_std('timescales')` ([PyEMMA tutorial](https://emma-project.org/latest/tutorials/notebooks/00-pentapeptide-showcase.html)).

Deeptime follows the same pattern: `BayesianMSMPosterior` stores a prior and sampled `MarkovStateModel`s; `timescales()` returns “Timescales of the prior and timescales of the samples,” while confidence is the requested posterior interval mass ([API](https://deeptime-ml.github.io/latest/api/generated/deeptime.markov.msm.BayesianMSMPosterior.html)). Its official notebook says the returned sample statistics contain “mean, standard deviation, as well as confidence intervals” and explains that samples are drawn from a Bayesian posterior ([deeptime ML-MSM notebook](https://deeptime-ml.github.io/latest/notebooks/mlmsm.html)).

Therefore these intervals cover uncertainty induced by finite transition-count data under the chosen likelihood/prior and model assumptions, propagated through ordinary floating-point spectral calculations. None of the cited APIs claims outward-rounded bounds, a backward-error certificate, or inclusion of eigensolver/roundoff error. Calling them numerical-error enclosures would be unsupported.

## 2. Reported numerical-trust pain

The strongest verified evidence is correctness history, not a demonstrated LAPACK-roundoff failure. The concrete records below are merged tracker fixes/PRs recorded in release notes, not user-filed reports that isolate an eigensolver defect:

* PyEMMA's release notes state: “This bug led to wrongly scaled time units for mean first passage times, correlation and relaxation times as well for timescales for this estimator” and link change [#1116](https://github.com/markovmodel/PyEMMA/pull/1116) ([release record](https://github.com/markovmodel/PyEMMA/releases)).
* The same release record says PyEMMA fixed “bug in ImpliedTimescales, which happened when an estimation failed for a given lag time,” linked as [#1248](https://github.com/markovmodel/PyEMMA/pull/1248), and separately changed the Chapman–Kolmogorov validator to avoid side effects, [#1255](https://github.com/markovmodel/PyEMMA/pull/1255) ([release record](https://github.com/markovmodel/PyEMMA/releases)). These are reproducibility/trust pain in spectral-timescale output or validation plumbing, although they are not certified as linear-algebra instability.

I searched indexed issues/PRs and user-forum material for both projects using combinations of `eigenvalue`, `eigensolver`, `timescale`, `complex`, `platform`, and `non-reversible`. I could not verify a specific user report of platform-dependent eigensolver results, spurious complex eigenvalues, non-reversible eigenvector ill-conditioning, or PyEMMA/deeptime disagreement. No such quote is invented here; GitHub's indexed release material was substantially more accessible than old mailing-list archives in this scan. PyEMMA is archived and points users to deeptime ([repository notice](https://github.com/markovmodel/PyEMMA)).

## 3. What MSM validation literature asks for

Prinz et al., *Markov models of molecular kinetics: generation and validation* (2011), J. Chem. Phys. 134, 174105, DOI [10.1063/1.3565032](https://doi.org/10.1063/1.3565032), describes approximation error, statistical uncertainty, reversible estimation, and a robust kinetic validation test ([abstract](https://pubmed.ncbi.nlm.nih.gov/21548671/)). Its Chapman–Kolmogorov prescription says model agreement should be judged “within the statistical uncertainties induced by the data” ([paper PDF](https://www.bcp.fu-berlin.de/en/chemie/chemie/forschung/PhysTheoChem/agkeller/_Docs/Publications_pdf/Prinz2011.pdf)).

Husic and Pande, *Markov State Models: From an Art to a Science* (2018), JACS 140, 2386–2396, DOI [10.1021/jacs.7b12191](https://doi.org/10.1021/jacs.7b12191), frames the advance as variational model selection and cross-validation ([PubMed](https://pubmed.ncbi.nlm.nih.gov/29323881/)). Wu and Noé's VAMP paper proposes VAMP-E for “cross-validation for hyper-parameter optimization and model selection” ([arXiv](https://arxiv.org/abs/1707.04659)). The review literature also describes GMRQ/VAMP-2 as cross-validated model-selection scores ([review](https://pmc.ncbi.nlm.nih.gov/articles/PMC8479766/)).

These sources target sampling, discretization, Markovianity, approximation, and generalization. I found no expressed demand in them for guaranteed floating-point eigenvalue enclosures. Certification would supplement, not replace, CK tests or variational validation.

## 4. Existing rigorous/validated spectral bounds

No MSM-specific interval-arithmetic eigenvalue/timescale-gap certificate was found in this scan. The closest prior art is generic rather than molecular-MSM-specific:

* S. M. Rump, “Computational error bounds for multiple or nearly multiple eigenvalues,” *Linear Algebra Appl.* 324 (2001), 209–226, DOI [10.1016/S0024-3795(00)00283-7](https://doi.org/10.1016/S0024-3795(00)00283-7), provides verified numerical-linear-algebra machinery for difficult eigenvalues.
* M. Hladík, D. Daney, and E. P. Tsigaridas, “Bounds on real eigenvalues and singular values of interval matrices,” *SIAM J. Matrix Anal. Appl.* 31(4) (2010), 2116–2129, describes computable outer bounds for general and symmetric interval matrices ([author bibliography and abstract](https://who.paris.inria.fr/Elias.Tsigaridas/b2hd-hdt-simax-2010.html)).
* Analytic spectral bounds for symmetric Markov chains also exist, but they are not per-instance outward-rounded MSM eigensolver receipts ([Eigenvalue Bounds for Symmetric Markov Chains](https://drops.dagstuhl.de/storage/00lipics/lipics-vol353-approx-random2025/LIPIcs.APPROX-RANDOM.2025.34/LIPIcs.APPROX-RANDOM.2025.34.pdf)).

These works mean the numerical primitives are not novel. What this scan did **not** find is their packaging in the molecular-dynamics MSM workflow as machine-checkable enclosures for fitted eigenvalues, implied timescales, or timescale gaps. Thus no verified MSM-context scoop was identified.

## 5. Kill-condition application

Sampling/model error is often the scientifically important uncertainty, and the mainstream validation literature does not identify spectral roundoff as a leading problem. But “universally dominant” is not established. Small, well-sampled matrices, close/clustered slow eigenvalues, non-reversible models, regression tests, and cross-version method comparisons are niches where a deterministic certificate can establish eigenvalue ordering/separation and provide a reproducible receipt—something posterior intervals do not claim.

## VERDICT: **PROCEED-TO-KT2**

The literal KILL conjunction fails: documented PyEMMA releases include wrong timescale scaling and implied-timescale failure handling, and incumbent Bayesian intervals do not enclose implementation or floating-point spectral error. This is a niche/assurance verdict, not evidence that numerical error usually exceeds sampling uncertainty. KT2 should test whether real, well-sampled MSM matrices produce certificate widths materially smaller than posterior widths and whether close spectral gaps occur often enough to justify integration cost.
