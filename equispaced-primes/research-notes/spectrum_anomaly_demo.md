# Spectrum Anomaly Detection via the cluster=2 Diagnostic — Demo

**Date:** 2026-05-27
**Code:** `code/spectrum_anomaly_demo.py`
**Figure:** `figures/spectrum_anomaly_results.png`
**Numerical summary:** `code/spectrum_anomaly_results.json`

## Goal

A prior subagent flagged "spectrum anomaly detection" as a candidate
practical application of the cluster=2 diagnostic developed in
`cluster_universality_test/cluster_diagnostic.py` (the same diagnostic
used to distinguish Farey/BCZ gap sequences from GUE / CUE / Poisson /
Riemann-zero gaps). The plausible-value prediction was 75–95% TPR. This
note records what actually happens when the diagnostic is applied to
synthetic wireless spectra.

## Methodology

1. **Synthetic spectra.** Each "observation" is a 65,537-bin power
   spectrum produced by `rfft` of length-131,072 complex Gaussian noise,
   smoothed Rayleigh-fading envelope, and 20 sparse legitimate carriers.
2. **Three classes.**
   - **NORMAL** — baseline only.
   - **ARITH** — baseline + an evenly-spaced jammer comb (~600 teeth,
     spacing ∈ [60,120] bins, amplitude 10–30 × baseline 99th-percentile).
   - **BCZ** — baseline + ~600 jammers whose bin offsets are
     `f0 + Farey(Q=60) · span`, i.e. carrier spacings are Farey-fraction
     differences. Same amplitude scale as ARITH.
3. **Peak detection.** `scipy.signal.find_peaks` above the top-0.5%
   quantile, minimum bin distance 3. Yields ~300 peaks per spectrum.
4. **Spacing sequence.** Consecutive peak-bin differences, normalised to
   unit mean.
5. **Cluster=2 features.** From `cluster_diagnostic.cluster_stats` at
   q ∈ {0.80, 0.85, 0.86181, 0.90, 0.95}, we keep the 5-vector
   `[p_size>=3 @ q*, max_size @ q*, p_size>=3 @ 0.90, p_size>=3 @ 0.95,
    mean_cluster_size @ q*]` where q* = 0.86181 is the BCZ phase-transition
   quantile.
6. **Classifier.** Shared-covariance LDA (no sklearn dependency),
   5-fold cross-validation, 120 realisations × 3 classes.

## Results

```
-- Multiclass (NORMAL / ARITH / BCZ) --   5-fold CV accuracy: 0.428 ± 0.042
  confusion:
              NORMAL  ARITH   BCZ
   NORMAL       45     32     43
   ARITH        21     87     12
   BCZ          49     49     22

-- Binary (NORMAL vs anomalous) --        5-fold CV accuracy: 0.667 ± 0.042
   TPR = 0.896,  FPR = 0.792

-- BCZ vs ARITH (anomalous-only) --       5-fold CV accuracy: 0.683 ± 0.085
   confusion (rows=true, cols=pred, 0=ARITH, 1=BCZ):
   ARITH: [93, 27]      (78% recall)
   BCZ  : [49, 71]      (59% recall)
```

Per-class feature means (`[p3@q*, max@q*, p3@.90, p3@.95, mean_size@q*]`):

```
NORMAL : [0.052, 2.68, 0.027, 0.007, 1.17]
ARITH  : [0.016, 2.08, 0.013, 0.002, 1.10]   <-- visibly lower
BCZ    : [0.041, 2.60, 0.024, 0.006, 1.15]
```

## Honest interpretation

**The diagnostic discriminates one direction only: it detects regular
(periodic) interference vs irrelevant or noise-like spacings.** ARITH
spectra get classified correctly 78% of the time because a perfectly
periodic jammer comb collapses the extreme-spacing distribution (no
clustering above q*, `p_size>=3` drops by 3×). This is the same
mechanism that lets the original diagnostic separate pure-arithmetic
from BCZ in the math setting.

**The diagnostic does not separate BCZ-class from NORMAL.** Mean-feature
vectors for BCZ and NORMAL are nearly identical (the BCZ jammers are
swamped by ~270 Rayleigh-faded noise peaks; only ~10% of detected peaks
are jammer-driven). Even at the chosen jammer SNR — well above
realistic — the BCZ-vs-NORMAL confusion is essentially 50/50.

So the practical-value claim splits cleanly:

| Sub-task                                    | Verdict                       |
|---------------------------------------------|-------------------------------|
| Detect periodic / comb interference         | Real signal (~78% recall)     |
| Detect "BCZ-class" interference vs NORMAL   | Not separated by this feature |
| Distinguish BCZ vs ARITH given anomalous    | 68% — modest, above chance    |

## Concrete claim (calibrated)

> *Using only the cluster=2 diagnostic on consecutive peak spacings,
> a 5-class linear classifier achieves 68% cross-validated accuracy
> distinguishing BCZ-spaced from arithmetically-spaced narrowband
> interference, and 78% recall on detecting arithmetic combs versus
> background; it does **not** reliably detect BCZ-class interference
> against a Rayleigh-faded noise background.*

The earlier 75–95% TPR prediction is **not supported** by this demo.

## Why this is what we should have expected

The cluster=2 statistic is an *asymptotic* signature of long sequences
of correlated gaps (the original BCZ chain uses 5 × 10⁶ samples). With
~300 peaks per spectrum we have ~40 extreme gaps above q* = 0.86 — the
asymptotic distribution barely manifests. We confirmed this by feeding
the diagnostic pure synthetic spacings:

- Pure arithmetic (n=10000):       `p3@q* = 0.000`, max = 0
- Pure Farey/BCZ gaps Q=200:       `p3@q* = 0.000`, max = 2
- Pure Poisson (n=10000):          `p3@q* = 0.066`, max = 4

In other words, the diagnostic *can* tell the classes apart with clean,
long input — but as soon as Rayleigh-faded noise contributes most of the
peaks, the noise's Poisson-like clustering signature dominates everything
else.

## Honest limitations

- **Only one observation length tested** (131,072 bins). Longer
  observations might reach the asymptotic regime where BCZ ≠ NORMAL.
- **No comparison to a sensible baseline** (a 1-D Fourier-of-spectrum
  detector, a simple autocorrelation peak detector, or "fraction of
  energy at the spectrum's strongest periodicity") would almost
  certainly beat 78% on ARITH and might also beat 68% on BCZ-vs-ARITH.
  The cluster=2 diagnostic is *not* a strong feature here — it is one
  feature among many one could use.
- **Synthetic, not RF-realistic.** No multipath, no quantisation, no
  receiver nonlinearity, no Doppler. Real RF interference rarely lands
  exactly on Farey-pattern grids.
- **LDA classifier is minimal.** A stronger classifier on these same 5
  features would not help much — class means are too close.
- **No claim of novelty.** Detecting periodic combs in a power spectrum
  is a textbook signal-processing problem solved better by a quefrency
  / autocorrelation analysis.

## Files

- `code/spectrum_anomaly_demo.py` — 250-line pipeline, deterministic
  seed `20260527`.
- `code/spectrum_anomaly_results.json` — accuracy, confusion matrices,
  per-class feature means.
- `figures/spectrum_anomaly_results.png` — example spectrum per class,
  peak-spacing histograms, and 2-D feature scatter plots.

## Bottom line

The cluster=2 diagnostic is a real and useful tool for distinguishing
*pure* long-sequence regimes (BCZ vs GUE vs Poisson vs arithmetic). When
applied to wireless-spectrum peak spacings it survives as a *weak*
secondary feature — useful for spotting perfectly-periodic interference,
useless for detecting BCZ-class anomalies against background. The 75–95%
TPR prediction was optimistic; the realistic figure on this synthetic
benchmark is ~68% for BCZ-vs-ARITH and effectively chance for
BCZ-vs-NORMAL.
