"""KT2 part C: does the picture change for larger / worse-conditioned MSMs?

Prinz quadruple well, 500k frames, lag 10, with 50 / 100 / 200 / 400 / 800
microstates. Finer discretisation means sparser, nearly-reducible count
matrices, i.e. the regime where a float eigensolver could plausibly struggle.

Per size we record:
  * certified enclosure radius of the leading implied timescales (prec 53
    working precision, and prec 333),
  * the ACTUAL float error of numpy's eigensolver, measured as
    |lambda_numpy - lambda_certified| against the certified enclosure,
  * the eigenvector-matrix condition number (numpy) as a conditioning proxy,
  * Bayesian 95% CI width for the same timescales,
  * wall-clock cost of the certificate.

Writes kt2_scale.json.
"""
import json
import os
import time

import numpy as np
from deeptime.clustering import KMeans
from deeptime.data import prinz_potential
from deeptime.markov import TransitionCountEstimator
from deeptime.markov.msm import BayesianMSM

import kt2_common as kc

HERE = os.path.dirname(os.path.abspath(__file__))
LAG = 10
NFRAMES = 500000
SIZES = [50, 100, 200, 400]
K = 5


def main():
    sysd = prinz_potential(h=1e-5, n_steps=100)
    x = sysd.trajectory(np.array([[0.0]]), NFRAMES, seed=42)
    out = []
    for nclus in SIZES:
        km = KMeans(n_clusters=nclus, fixed_seed=13, n_jobs=1, max_iter=200).fit_fetch(x)
        dt = km.transform(x)
        cm = TransitionCountEstimator(lagtime=LAG, count_mode="sliding-effective") \
            .fit_fetch(dt).submodel_largest()
        C = np.asarray(cm.count_matrix) * LAG
        Ci = np.rint(C).astype(np.int64)
        assert np.allclose(C, Ci)
        n = Ci.shape[0]
        rec = {"n_clusters": nclus, "n_states": n,
               "min_row_count": int(Ci.sum(axis=1).min()),
               "sparsity": float((Ci == 0).mean())}
        # prec 333 is only affordable on the small matrices; the cost of the
        # verified eigensolver at high precision is itself a KT2 datum.
        precs = (53, 333) if n <= 100 else (53,)
        for prec in precs:
            t = time.time()
            try:
                c = kc.certified_spectrum(Ci, LAG, prec=prec, k=K)
                rec[f"cert_p{prec}"] = {
                    "its_mid": [e["its_mid"] for e in c["eigs"][1:]],
                    "its_rad": [e["its_rad"] for e in c["eigs"][1:]],
                    "abs_rad": [e["abs_rad"] for e in c["eigs"]],
                    "seconds": time.time() - t}
            except Exception as exc:
                rec[f"cert_p{prec}"] = {"error": str(exc),
                                        "seconds": time.time() - t}
        # float eigensolver: actual error vs certified enclosure
        T = Ci / Ci.sum(axis=1, keepdims=True)
        ev, V = np.linalg.eig(T)
        order = np.argsort(-np.abs(ev))
        ev = ev[order]
        rec["numpy_cond_eigvec"] = float(np.linalg.cond(V))
        ref = rec.get("cert_p333") if "its_mid" in rec.get("cert_p333", {}) \
            else rec.get("cert_p53")
        if ref and "abs_rad" in ref:
            ref_full = kc.certified_spectrum(
                Ci, LAG, prec=333 if n <= 100 else 53, k=K)
            rec["numpy_abs_eig_error"] = [
                float(abs(abs(ev[i]) - e["abs_mid"]))
                for i, e in enumerate(ref_full["eigs"])]
            rec["numpy_max_abs_imag_top"] = float(np.max(np.abs(ev[:K].imag)))
        t = time.time()
        b = BayesianMSM(n_samples=200, reversible=True, lagtime=LAG).fit_fetch(cm)
        ts = np.array([m.timescales(k=K - 1) for m in b.samples])
        lo, hi = np.percentile(ts, 2.5, axis=0), np.percentile(ts, 97.5, axis=0)
        rec["bayes"] = {"ci95_width": (hi - lo).tolist(),
                        "std": ts.std(axis=0).tolist(),
                        "prior_its": np.asarray(b.prior.timescales(k=K - 1)).tolist(),
                        "seconds": time.time() - t}
        out.append(rec)
        with open(os.path.join(HERE, "kt2_scale.json"), "w") as f:
            json.dump({"lag": LAG, "n_frames": NFRAMES, "results": out}, f, indent=1)
        print("size", nclus, "states", n, "done", flush=True)
    with open(os.path.join(HERE, "kt2_scale.json"), "w") as f:
        json.dump({"lag": LAG, "n_frames": NFRAMES, "results": out}, f, indent=1)
    print("wrote kt2_scale.json")


if __name__ == "__main__":
    main()
