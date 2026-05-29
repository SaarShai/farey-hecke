# LMFDB cluster-size diagnostic — first applied test on arithmetic L-function zeros

**Date:** 2026-05-27
**Author:** computational experiment, this session
**Status:** completed; results below are the first application of the
`size-2 cluster diagnostic` to *arithmetic* (i.e. number-theoretic, not
toy Farey or RMT) zero sequences.

## Question

We previously established
[`cluster_universality_test/cluster_diagnostic_extended.py`]:

- BCZ Farey-gap chain: **~95% size-2 clusters at q=0.99** in 1M samples
- All six standard RMT ensembles (GOE/GUE/GSE/COE/CUE/CSE,
  including β-Hermite β ∈ {1,2,4,6,10}): **~0% at q=0.99**
- Poisson exponential gaps: **~1.1% at q=0.99**
- φ-rotation flow gaps: 0%
- Riemann ζ at low height (100k zeros): 0% at q=0.99 (matches GUE)

**Open question.** Does any *other* arithmetic L-function show the BCZ-class
~95% pattern, or are they all GUE-equivalent? A positive hit would be a new
member of the Farey universality class — a striking discovery. A clean
negative would confirm that BCZ class is *specifically* the
SL(2,ℤ)\SL(2,ℝ) horocycle structure, narrowing the class definition.

## Method

1. **Zero data.** Bulk LMFDB downloads are gated by reCAPTCHA (we observed
   the `/L/download_zeros/` endpoint returns ≤10 zeros per L-function via
   the public URL). We therefore compute zeros locally with **PARI/GP**
   via `subprocess` (cached to
   `projects/mimo-mini-project/data/zeros/<label>_T<Tmax>.txt`).
2. **Unfolding.** For a primitive self-dual L-function of degree d and
   analytic conductor q, local density is
   ρ(T) = (log q + d log(T/2π)) / (2π) (Iwaniec–Kowalski Thm 5.8).
   Gaps divided by 1/ρ(midpoint), then rescaled to exact mean 1.
3. **Diagnostic.** For q ∈ {0.95, 0.99, 0.999}: threshold at q-quantile,
   run-length-encode the >threshold mask, report size-2 fraction and
   p_size≥3 (gaps in size≥3 clusters / total extreme gaps). Identical
   conventions to `cluster_diagnostic_extended.py`.

## Per-L-function results

(Sample sizes and per-q size-2 percentages are filled in from the
`lmfdb_diagnostic_results.json` companion file; we transcribe the
size-2% and verdict here. q=0.999 is reported but underpowered at our
sample sizes — flagged below.)

All numbers below are read from `lmfdb_diagnostic_results.json`. Columns:
`#zer` = #zeros used; `H_max` = height of largest zero; `n_ext` = #extreme
gaps at the quantile; `s2%` = 100 × size-2-fraction.

| L-function | deg | cond | #zer | H_max | q | n_ext | n_clusters | s2% | max_size | verdict |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Riemann ζ (Odlyzko, low h) | 1 | 1 | 100,000 | 7.5e4 | 0.99 | 1000 | 1000 | **0.00** | 1 | GUE (control ✓) |
| Riemann ζ | 1 | 1 |  |  | 0.95 | 5000 | 4993 | **0.14** | 2 | (7 size-2 in 4993) |
| Riemann ζ | 1 | 1 |  |  | 0.999 | 100 | 100 | **0.00** | 1 | (underpowered) |
| L(χ_{-3}) | 1 | 3 | 4,173 | 3999 | 0.99 | 42 | 42 | **0.00** | 1 | GUE-like |
| L(χ_{-4}) | 1 | 4 | 4,356 | 3999 | 0.99 | 44 | 44 | **0.00** | 1 | GUE-like |
| L(χ_5)    | 1 | 5 | 4,498 | 4000 | 0.99 | 45 | 45 | **0.00** | 1 | GUE-like |
| L(χ_8)    | 1 | 8 | 4,795 | 3999 | 0.99 | 48 | 48 | **0.00** | 1 | GUE-like |
| L(s, Δ) (wt 12, lvl 1) | 2 | 1 | 1,138 | 899 | 0.99 | 12 | 12 | **0.00** | 1 | GUE-like (small sample) |
| L(s, f_16) (wt 16, lvl 1) | 2 | 1 | 1,138 | 900 | 0.99 | 12 | 12 | **0.00** | 1 | GUE-like (small sample) |
| L(s, E_{11a1}) (wt 2, lvl 11) | 2 | 11 | 728 | 499 | 0.99 | 8 | 8 | **0.00** | 1 | GUE-like (very small sample; T=500 because T=2500 exceeded 20-min PARI budget) |
| L(s, Sym² Δ) (deg 3) | 3 | 1 | n/a | n/a | n/a | -- | -- | -- | -- | **not tested** -- PARI `lfunsympow` unimplemented |

For reference (from `cluster_universality_test/cluster_diagnostic_extended.py`):

- BCZ Farey chain (1M gaps): 88.2% @ q=0.95, **94.6% @ q=0.99**
- GOE/GUE/GSE/COE/CUE/CSE: 0.5–0.7% @ q=0.95, **0.00% @ q=0.99**
- Poisson: 4.6% @ q=0.95, 1.1% @ q=0.99

## Verdict per L-function

**All tested arithmetic L-functions land in the RMT/GUE class.**
No L-function tested shows the BCZ ~95% size-2 signature.

- ζ, L(χ_{-3}), L(χ_{-4}): degree 1 GL(1) — match GUE (Katz–Sarnak unitary
  symmetry, as expected for any fixed primitive Dirichlet L-function).
- L(s, Δ), L(s, f_16): degree 2 GL(2), trivial level — match GUE.
- L(s, E_{11a1}): GL(2), level 11, rank 0 — predicted GUE-like (or O+ at
  low height; the local statistics are identical to GUE in either case
  because the cluster diagnostic is sensitive only to the bulk pair-/triple-
  correlation, not the symmetry sign).
- Sym² Δ: **not tested.** PARI 2.15.x's `lfunsympow` is documented but
  returns "sorry, lfunsympow is not yet implemented" at runtime. Manually
  constructing the degree-3 Dirichlet series is feasible but out of scope
  in this session. We do *not* claim Sym² Δ is GUE; we *did not test it*.

## Comparison to the Farey ~95% baseline

The Farey/BCZ baseline at q=0.99 is **94.6% size-2** with 5,139 clusters
(extreme-gap denominator 10,000). At q=0.999, the BCZ chain still produces
clusters above the threshold because of the deterministic mediant structure
that forbids size-3+ runs (Stern–Brocot mediant obstruction). The size-2
fraction stays high.

The arithmetic L-functions tested produce, at q=0.99 with ~4,000 zeros,
between 12 and 44 extreme gaps and **zero size-2 clusters in every case**.
This is not a sample-size artifact: at the same denominator scale,
GUE-simulated ensembles also give 0% size-2 (per the prior extended run).

If any L-function tested were in the BCZ class, we would expect 80%+ of
the 12–44 extreme gaps to live in size-2 clusters; we see 0%. The result
is **clean and unambiguous** at the available sample sizes.

The smallest, weakest tests are Δ and f_16 (only 1,138 zeros each → 12
extreme gaps at q=0.99). At those sample sizes, a 50% deviation from BCZ
class would still be detected. We see 0%.

## Honest caveats

1. **Sym² Δ untested.** PARI's `lfunsympow` returns an "unimplemented"
   error. We can compute Sym² L from scratch via Hecke eigenvalues τ(n)
   and the explicit degree-3 Euler factors (α_p² + β_p² = τ(p)² − 2p^{11}
   at unramified p, etc.), then plug into `lfuncreate` with a Dirichlet
   coefficient list. We did not do this in-session. **Open question
   remains for Sym² Δ.**

2. **No Maass L-functions.** Spectral-side L-functions of Maass cusp forms
   require a Hecke eigenvalue table; PARI's `mfinit` covers only the
   holomorphic side. Skipped.

3. **No GL_3+ tests.** Degree-3 Selmer-style L-functions and L(s, π) for
   higher GL(n) cusp forms are not directly available in PARI's `lfun`
   interface; the available degree-3+ entry points (`lfungenus2` for GL(4)
   from genus-2 curves) are very slow (~107s for 320 zeros at T=100, so
   ~50 min for 1000 zeros). **Open**: higher-rank L-functions remain
   untested. The conjecture from
   `research_notes/universality_rank_conjecture.md` (rank+1 cluster bound,
   so rank-2 should be ≤3) cannot be probed without this data.

4. **Conductor and height range matter for variance, not for the cluster
   diagnostic.** Our chi_{-3}, chi_{-4}, Δ, f_16 zeros are at relatively
   low height (T ≤ 4000 or 900), and the bulk standard deviation of
   unfolded gaps is 0.36 rather than the asymptotic GUE 0.42. This is
   the well-known "low-zeros transition regime" finite-conductor effect
   (Katz–Sarnak); the cluster diagnostic does not depend on the variance
   and gives the same 0% size-2 verdict in any case.

5. **The conclusion does NOT prove "Farey is the unique BCZ-class
   arithmetic statistic."** It tests six L-functions and finds none in
   the class. Many large families remain: Maass forms, GL_n for n ≥ 3
   cuspidal Π, Sym^k Δ for k ≥ 2, real quadratic ψ-class L-functions on
   higher rank groups, Rankin–Selberg products. A "no" from each of the
   six tested arithmetic L-functions is evidence for, but not a proof of,
   the narrower thesis that BCZ class is specifically the SL(2,Z)
   horocycle structure.

6. **Sample sizes vary.** Riemann ζ has 100k zeros (Odlyzko table from
   `cluster_universality_test/zeros1.txt`); the others are 1.1k–4.4k
   freshly computed from PARI. At q=0.99 this corresponds to 12–1,000
   extreme gaps. q=0.999 is genuinely underpowered for the small samples
   (2–100 extreme gaps); we report it but caution against over-reading.

## Interpretation

For all six tested arithmetic L-functions, **the cluster=2 diagnostic
behaves as if the underlying statistics were GUE**. This is exactly the
Katz–Sarnak prediction. None of these is in the BCZ universality class.

The result *narrows* the BCZ class: it is not a generic "arithmetic
modular structure," it is *specifically* the SL(2,ℤ)\SL(2,ℝ) horocycle
flow / continued-fraction mediant structure. The mediant obstruction
(Stern–Brocot) that forces cluster ≤ 2 is, on present evidence, *not*
shared by holomorphic newforms of any weight ≥ 2, by Kronecker characters,
or by elliptic-curve L-functions.

This is consistent with the
`universality_rank_conjecture.md` deep-review verdict: cluster bounds are
expected to depend on a continued-fraction-like mediant structure tied to
the lattice rank of the underlying group action, not on the arithmetic
nature of the Dirichlet coefficients.

## Files produced

- `projects/mimo-mini-project/code/lmfdb_cluster_diagnostic.py`
- `projects/mimo-mini-project/code/lmfdb_diagnostic_results.json`
- `projects/mimo-mini-project/data/zeros/{chi_m3,chi_m4,chi_5,chi_8,delta,wt16,ec_11a1}_T*.txt`
- this note.

## What this means for the larger project

This was an honest test of the central narrowing question: "is BCZ a
truly new universality class, or is it part of a larger arithmetic
family?" The answer, restricted to the six L-functions we could test in
session, is: **BCZ stands alone** among them.

This sharpens the claim and makes the Athreya–Cheung §8 / N·W → C lane
(per `project_farey_forward_verdict`) the right place to focus: cluster=2
appears genuinely tied to the SL(2,ℤ) horocycle structure, not to
arithmetic modularity more broadly.

The Sym² Δ gap and higher-rank GL(n) gap remain *open*. The natural next
test (per `function_field_BCZ_feasibility.md` and the deferred rank-2
probe) would be the 2-D Brentjes/Voronoi cluster diagnostic, *not* more
GL(1)/GL(2) L-functions.
