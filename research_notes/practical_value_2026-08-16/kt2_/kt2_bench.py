"""KT2 main benchmark: certificate width vs Bayesian posterior width.

System: Prinz quadruple-well potential (deeptime.data.prinz_potential), the
standard 1-D MSM benchmark from Prinz et al. 2011.

For each sample size we build a count matrix at a fixed lag on the largest
connected set, then compare
  (a) rigorous enclosure width of |lambda_i| and of the implied timescale,
      for the exact non-reversible MLE (kt2_common.certified_spectrum), and
  (b) deeptime BayesianMSM posterior std / 95% CI width of the same timescales.

Usage: python kt2_bench.py
Writes kt2_bench.json next to this file.
"""
import json
import os
import time

import numpy as np
from deeptime.clustering import KMeans
from deeptime.data import prinz_potential
from deeptime.markov import TransitionCountEstimator
from deeptime.markov.msm import BayesianMSM, MaximumLikelihoodMSM

import kt2_common as kc

HERE = os.path.dirname(os.path.abspath(__file__))
LAG = 10
NSTATES = 25
K = 4  # leading eigenvalues examined (lambda_1 = 1 plus 3 slow processes)
SIZES = [1000, 10000, 100000, 500000]
N_BAYES = 500


def make_trajectory(n_frames, seed=42):
    sys = prinz_potential(h=1e-5, n_steps=100)
    x = sys.trajectory(np.array([[0.0]]), n_frames, seed=seed)
    return x


def counts_from(dtraj, lag):
    # "sliding-effective" = sliding counts divided by the lag. It is what
    # deeptime requires for a Bayesian posterior, and it is still an EXACT
    # rational matrix (integer/lag), so the same object can be certified.
    est = TransitionCountEstimator(lagtime=lag, count_mode="sliding-effective")
    cm = est.fit_fetch(dtraj).submodel_largest()
    return cm


def integer_counts(cm, lag):
    C = np.asarray(cm.count_matrix) * lag
    Ci = np.rint(C).astype(np.int64)
    assert np.allclose(C, Ci), "sliding-effective counts are not integer/lag"
    return Ci


def bayes_stats(cm, k):
    bmsm = BayesianMSM(n_samples=N_BAYES, reversible=True, lagtime=LAG).fit_fetch(cm)
    ts = np.array([m.timescales(k=k - 1) for m in bmsm.samples])  # (S, k-1)
    prior = np.asarray(bmsm.prior.timescales(k=k - 1))
    lo = np.percentile(ts, 2.5, axis=0)
    hi = np.percentile(ts, 97.5, axis=0)
    return {
        "prior_its": prior.tolist(),
        "mean_its": ts.mean(axis=0).tolist(),
        "std_its": ts.std(axis=0).tolist(),
        "ci95_lo": lo.tolist(),
        "ci95_hi": hi.tolist(),
        "ci95_width": (hi - lo).tolist(),
    }


def main():
    t0 = time.time()
    traj = make_trajectory(max(SIZES), seed=42)
    print(f"trajectory {traj.shape} in {time.time()-t0:.1f}s", flush=True)
    km = KMeans(n_clusters=NSTATES, fixed_seed=13, n_jobs=1).fit_fetch(traj)
    dtraj_full = km.transform(traj)

    results = []
    for n in SIZES:
        dtraj = dtraj_full[:n]
        cm = counts_from(dtraj, LAG)
        Ci = integer_counts(cm, LAG)
        rec = {"n_frames": n, "n_states": int(Ci.shape[0]),
               "total_counts": int(Ci.sum())}
        for prec in (53, 333):
            t = time.time()
            rec[f"cert_p{prec}"] = kc.certified_spectrum(Ci, LAG, prec=prec, k=K)
            rec[f"cert_p{prec}"]["seconds"] = time.time() - t
        t = time.time()
        rec["gap23"] = kc.certified_gap(Ci, LAG, 1, 2, prec=333)
        rec["gap34"] = kc.certified_gap(Ci, LAG, 2, 3, prec=333)
        t = time.time()
        rec["bayes"] = bayes_stats(cm, K)
        rec["bayes"]["seconds"] = time.time() - t
        rec["mle_rev_its"] = np.asarray(
            MaximumLikelihoodMSM(reversible=True, lagtime=LAG)
            .fit_fetch(cm).timescales(k=K - 1)).tolist()
        rec["mle_nonrev_its"] = np.asarray(
            MaximumLikelihoodMSM(reversible=False, lagtime=LAG)
            .fit_fetch(cm).timescales(k=K - 1)).tolist()
        results.append(rec)
        print(f"n={n} states={rec['n_states']} done", flush=True)

    out = {"lag": LAG, "n_cluster_states": NSTATES, "n_bayes_samples": N_BAYES,
           "seed": 42, "results": results}
    with open(os.path.join(HERE, "kt2_bench.json"), "w") as f:
        json.dump(out, f, indent=1)
    print("wrote kt2_bench.json")


if __name__ == "__main__":
    main()
