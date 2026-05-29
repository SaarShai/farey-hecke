#!/usr/bin/env python3
"""
spectrum_anomaly_demo.py
========================

Demonstration: can the *cluster=2* diagnostic (from cluster_universality_test/
cluster_diagnostic.py) distinguish wireless-spectrum anomalies?

Three signal classes are generated as 1-D power spectra (output of
|FFT|^2 of a noisy time-domain segment + Rayleigh fading + carriers):

  NORMAL    : Gaussian + Rayleigh fading + a few sparse legitimate carriers
  ARITH     : NORMAL + an evenly-spaced jammer comb
  BCZ       : NORMAL + interference whose tone spacings follow Farey/BCZ
              fractional spacings (denominators in [Q_min, Q_max])

For each spectrum we:
  1. detect peaks above a quantile threshold,
  2. compute consecutive-peak frequency-bin spacings,
  3. normalise them to unit mean,
  4. run cluster_stats(...) at q = q*_BCZ = 0.86181 and a few neighbours,
  5. use  p_size_ge_3  and  max_size  as a 2-d feature vector,
  6. train a single linear-SVM (binary: NORMAL vs anomalous;
     multiclass: NORMAL / ARITH / BCZ),
  7. report cross-validated classification accuracy.

Output:
  ../figures/spectrum_anomaly_results.png
  prints metrics; also writes spectrum_anomaly_results.json next to this file.

This is a *small synthetic demo*; honest limitations are listed in the
companion research note.
"""

import json
import os
import sys
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# Reuse the project's cluster diagnostic.
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(PROJ, "cluster_universality_test"))
from cluster_diagnostic import cluster_stats  # noqa: E402

RNG = np.random.default_rng(20260527)

# ---------------------------------------------------------------------------
# 1.  Signal generators
# ---------------------------------------------------------------------------
N_FFT = 131072          # spectrogram length in bins (long observation window)
FS = 1.0                # normalised sampling rate
N_REALISATIONS = 120    # per class
DEFAULT_NCARR = 20      # legitimate carriers per spectrum


def _rayleigh_fading(n_bins, rng, scale=1.0):
    """Multiplicative Rayleigh fading envelope over frequency."""
    r = rng.rayleigh(scale=scale, size=n_bins)
    # smooth so adjacent bins are correlated (coherence bandwidth)
    k = 64
    kern = np.ones(k) / k
    r = np.convolve(r, kern, mode="same")
    return r / r.mean()


def _baseline_spectrum(rng, n_bins=N_FFT, n_carriers=DEFAULT_NCARR):
    """White-noise power spectrum, Rayleigh-faded, plus a few sparse carriers
       at random bin locations.  Returns the |X|^2-like array (length n_bins/2)."""
    # complex Gaussian time-domain
    x = (rng.standard_normal(n_bins) + 1j * rng.standard_normal(n_bins)) / np.sqrt(2)
    X = np.fft.rfft(x.real)
    P = np.abs(X) ** 2
    P *= _rayleigh_fading(len(P), rng)
    # add legitimate carriers (random, well-separated)
    carrier_bins = rng.choice(np.arange(50, len(P) - 50), size=n_carriers, replace=False)
    for b in carrier_bins:
        P[b] += rng.uniform(40, 80)
        P[b - 1] += rng.uniform(5, 10)
        P[b + 1] += rng.uniform(5, 10)
    return P


def generate_normal(rng):
    return _baseline_spectrum(rng)


def generate_arith(rng, n_jammers=600, amp_factor=(10, 30)):
    """Baseline + an evenly-spaced jammer comb.  amp_factor is multiplied by
       the baseline spectrum's 99th-percentile to give jammers a controlled SNR."""
    P = _baseline_spectrum(rng)
    L = len(P)
    base = float(np.quantile(P, 0.99))
    spacing = rng.integers(60, 120)          # bins between comb teeth
    start = rng.integers(60, spacing + 60)
    bins = np.arange(start, L - 5, spacing)[:n_jammers]
    for b in bins:
        P[b] += rng.uniform(*amp_factor) * base
    return P


def _farey_denominators(Q):
    """Sorted Farey fractions p/q with q in [2, Q]; returns the (unique) values."""
    fr = set()
    for q in range(2, Q + 1):
        for p in range(1, q):
            if np.gcd(p, q) == 1:
                fr.add(p / q)
    return np.array(sorted(fr))


def generate_bcz(rng, n_jammers=600, amp_factor=(10, 30), Q=60):
    """Baseline + interference at frequencies F0 + delta * f  where
       f runs over Farey fractions with denominator <= Q.  amp_factor as in
       generate_arith.  These spacings reproduce the BCZ gap statistics that
       the cluster=2 diagnostic was built to characterise."""
    P = _baseline_spectrum(rng)
    L = len(P)
    base = float(np.quantile(P, 0.99))
    fr = _farey_denominators(Q)
    if len(fr) > n_jammers:
        idx = rng.choice(len(fr), size=n_jammers, replace=False)
        fr = np.sort(fr[idx])
    span = rng.integers(L // 3, L // 2)
    f0 = rng.integers(80, L - span - 20)
    bins = (f0 + (fr * span)).astype(int)
    bins = np.unique(np.clip(bins, 1, L - 2))
    for b in bins:
        P[b] += rng.uniform(*amp_factor) * base
    return P


# ---------------------------------------------------------------------------
# 2.  Peak detection + spacing statistics
# ---------------------------------------------------------------------------
def peak_spacings(P, top_frac=0.005, min_distance=3):
    """Find the top (top_frac) of bins as peaks (with a small min-distance
       so adjacent bins do not double-count), return consecutive spacings
       normalised to unit mean."""
    thr = float(np.quantile(P, 1.0 - top_frac))
    peaks, _ = find_peaks(P, height=thr, distance=min_distance)
    if len(peaks) < 8:
        return None
    gaps = np.diff(peaks).astype(np.float64)
    if gaps.mean() <= 0:
        return None
    return gaps / gaps.mean()


# ---------------------------------------------------------------------------
# 3.  Cluster-2 features
# ---------------------------------------------------------------------------
Q_LIST = [0.80, 0.85, 0.86181, 0.90, 0.95]
Q_STAR = 0.86181


def cluster_features(gaps):
    """Return feature vector  [p3@q*, max_size@q*, p3@0.90, p3@0.95, mean_size@q*]."""
    s = cluster_stats(gaps, Q_LIST)
    sq = s[Q_STAR]
    if sq["n_clusters"] == 0:
        return np.array([0.0, 0.0, 0.0, 0.0, 0.0])
    mean_size = sq["n_extreme"] / max(sq["n_clusters"], 1)
    return np.array([
        sq["p_size_ge_3"],
        float(sq["max_size"]),
        s[0.90]["p_size_ge_3"],
        s[0.95]["p_size_ge_3"],
        mean_size,
    ])


# ---------------------------------------------------------------------------
# 4.  Build dataset
# ---------------------------------------------------------------------------
def build_dataset(n_per_class=N_REALISATIONS, rng=RNG):
    X, y, examples = [], [], {}
    classes = [("NORMAL", generate_normal),
               ("ARITH",  generate_arith),
               ("BCZ",    generate_bcz)]
    for ci, (name, gen) in enumerate(classes):
        for k in range(n_per_class):
            P = gen(rng)
            g = peak_spacings(P)
            if g is None:
                continue
            X.append(cluster_features(g))
            y.append(ci)
            if k == 0:
                examples[name] = (P.copy(), g.copy())
    return np.array(X), np.array(y), classes, examples


# ---------------------------------------------------------------------------
# 5.  Classifiers
# ---------------------------------------------------------------------------
def kfold_indices(n, k, rng):
    idx = np.arange(n)
    rng.shuffle(idx)
    return np.array_split(idx, k)


def _fit_lda(Xtr, ytr):
    """Simple shared-covariance LDA (no sklearn dependency)."""
    classes = np.unique(ytr)
    means = {c: Xtr[ytr == c].mean(axis=0) for c in classes}
    cov = np.cov(Xtr.T) + 1e-6 * np.eye(Xtr.shape[1])
    inv = np.linalg.inv(cov)
    priors = {c: (ytr == c).mean() for c in classes}
    return means, inv, priors, classes


def _pred_lda(model, X):
    means, inv, priors, classes = model
    scores = np.zeros((len(X), len(classes)))
    for i, c in enumerate(classes):
        mu = means[c]
        scores[:, i] = (X @ inv @ mu) - 0.5 * mu @ inv @ mu + np.log(priors[c])
    return classes[np.argmax(scores, axis=1)]


def cv_accuracy(X, y, k=5, rng=None):
    rng = rng or np.random.default_rng(0)
    folds = kfold_indices(len(X), k, rng)
    accs = []
    confusions = np.zeros((len(np.unique(y)), len(np.unique(y))), dtype=int)
    for i in range(k):
        test = folds[i]
        train = np.concatenate([folds[j] for j in range(k) if j != i])
        model = _fit_lda(X[train], y[train])
        pred = _pred_lda(model, X[test])
        accs.append((pred == y[test]).mean())
        for t, p in zip(y[test], pred):
            confusions[t, p] += 1
    return float(np.mean(accs)), float(np.std(accs)), confusions


# ---------------------------------------------------------------------------
# 6.  Plot
# ---------------------------------------------------------------------------
def make_plot(examples, X, y, classes, out_path):
    fig, axes = plt.subplots(3, 3, figsize=(15, 11))
    colors = {"NORMAL": "#2c7fb8", "ARITH": "#d95f0e", "BCZ": "#31a354"}

    # row 0: spectra
    for j, (name, _) in enumerate(classes):
        P, g = examples[name]
        ax = axes[0, j]
        ax.plot(P, color=colors[name], lw=0.6)
        ax.set_title(f"{name} : example spectrum", fontsize=11)
        ax.set_xlabel("freq bin")
        ax.set_ylabel("power")
        ax.set_xlim(0, len(P))

    # row 1: spacing histograms
    for j, (name, _) in enumerate(classes):
        P, g = examples[name]
        ax = axes[1, j]
        ax.hist(g, bins=40, color=colors[name], alpha=0.85, density=True)
        ax.set_title(f"{name} : normalised peak spacings", fontsize=11)
        ax.set_xlabel("gap / mean")
        ax.set_ylabel("density")
        ax.set_xlim(0, max(4.0, g.max() * 0.9))

    # row 2: feature scatter (cols share one combined axis)
    ax = axes[2, 0]
    for ci, (name, _) in enumerate(classes):
        m = y == ci
        ax.scatter(X[m, 0], X[m, 4], s=14, alpha=0.7,
                   label=name, color=colors[name])
    ax.set_xlabel("p_size>=3 at q* = 0.86181")
    ax.set_ylabel("mean cluster size at q*")
    ax.set_title("cluster-2 feature scatter")
    ax.legend()

    ax = axes[2, 1]
    for ci, (name, _) in enumerate(classes):
        m = y == ci
        ax.scatter(X[m, 2], X[m, 3], s=14, alpha=0.7,
                   label=name, color=colors[name])
    ax.set_xlabel("p_size>=3 at q = 0.90")
    ax.set_ylabel("p_size>=3 at q = 0.95")
    ax.set_title("higher-quantile features")
    ax.legend()

    ax = axes[2, 2]
    for ci, (name, _) in enumerate(classes):
        m = y == ci
        ax.scatter(X[m, 0], X[m, 1], s=14, alpha=0.7,
                   label=name, color=colors[name])
    ax.set_xlabel("p_size>=3 at q*")
    ax.set_ylabel("max cluster size at q*")
    ax.set_title("size-tail features")
    ax.legend()

    fig.suptitle("Spectrum Anomaly Detection via cluster=2 diagnostic",
                 fontsize=14, y=0.995)
    fig.tight_layout()
    fig.savefig(out_path, dpi=140)
    plt.close(fig)


# ---------------------------------------------------------------------------
# 7.  Main
# ---------------------------------------------------------------------------
def main():
    print(f"Building dataset: {N_REALISATIONS} realisations x 3 classes ...")
    X, y, classes, examples = build_dataset()
    class_names = [c[0] for c in classes]
    print(f"  X shape = {X.shape},  y bincount = {np.bincount(y).tolist()}")

    # MULTICLASS
    acc_mc, std_mc, conf_mc = cv_accuracy(X, y, k=5,
                                          rng=np.random.default_rng(11))
    print("\n-- Multiclass (NORMAL / ARITH / BCZ) --")
    print(f"  5-fold CV accuracy: {acc_mc:.3f} +- {std_mc:.3f}")
    print("  confusion (rows = true, cols = pred):")
    print(f"           {'  '.join(f'{n:>7}' for n in class_names)}")
    for ti, n in enumerate(class_names):
        print(f"    {n:>7} {'  '.join(f'{conf_mc[ti,pi]:7d}' for pi in range(3))}")

    # BINARY: NORMAL vs anomalous (ARITH or BCZ)
    yb = (y != 0).astype(int)
    acc_b, std_b, conf_b = cv_accuracy(X, yb, k=5,
                                       rng=np.random.default_rng(13))
    tn, fp = conf_b[0]
    fn, tp = conf_b[1]
    tpr = tp / max(tp + fn, 1)
    fpr = fp / max(fp + tn, 1)
    print("\n-- Binary (NORMAL vs anomalous) --")
    print(f"  5-fold CV accuracy: {acc_b:.3f} +- {std_b:.3f}")
    print(f"  TPR = {tpr:.3f},  FPR = {fpr:.3f}")

    # BCZ-vs-ARITH only (the real claim of the demo)
    mask_aa = y != 0
    yaa = (y[mask_aa] == 2).astype(int)  # 1 = BCZ
    acc_aa, std_aa, conf_aa = cv_accuracy(X[mask_aa], yaa, k=5,
                                          rng=np.random.default_rng(17))
    print("\n-- BCZ vs ARITH (anomalous-only subset) --")
    print(f"  5-fold CV accuracy: {acc_aa:.3f} +- {std_aa:.3f}")
    print("  confusion (rows = true, cols = pred,  0=ARITH, 1=BCZ):")
    for ti in range(2):
        print(f"    {ti}: {conf_aa[ti].tolist()}")

    out_fig = os.path.join(PROJ, "figures", "spectrum_anomaly_results.png")
    make_plot(examples, X, y, classes, out_fig)
    print(f"\nSaved figure: {out_fig}")

    summary = dict(
        n_per_class=N_REALISATIONS,
        feature_names=["p3_qstar", "max_qstar", "p3_q90", "p3_q95", "mean_qstar"],
        multiclass=dict(acc=acc_mc, std=std_mc, confusion=conf_mc.tolist()),
        binary=dict(acc=acc_b, std=std_b, tpr=tpr, fpr=fpr,
                    confusion=conf_b.tolist()),
        bcz_vs_arith=dict(acc=acc_aa, std=std_aa, confusion=conf_aa.tolist()),
        class_means=dict(zip(class_names,
                             [X[y == ci].mean(axis=0).tolist()
                              for ci in range(3)])),
    )
    with open(os.path.join(HERE, "spectrum_anomaly_results.json"), "w") as f:
        json.dump(summary, f, indent=2)
    print("Saved JSON: spectrum_anomaly_results.json")


if __name__ == "__main__":
    main()
