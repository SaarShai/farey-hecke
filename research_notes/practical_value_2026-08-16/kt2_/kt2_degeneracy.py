"""KT2 part B: near-degenerate slow eigenvalues, and how often they occur.

Part B1 (controlled degeneracy). Ground truth = two INDEPENDENT two-state
processes, product chain on 4 states. Its eigenvalues are exactly
    1,  1-2p,  1-2q,  (1-2p)(1-2q),
so the slow-eigenvalue gap is |2(p-q)| and can be tuned to zero. We sample a
trajectory from the exact chain, build the integer count matrix, and compare:
  * rigorous enclosure width (Arb, exact rational MLE) at prec 53 and 333,
  * Bayesian posterior 95% CI width for the same timescales,
  * whether numpy's float eigensolver returns a spurious complex pair,
  * whether the certificate proves the ordering lambda_2 > lambda_3.

Part B2 (how often in a real MSM). Prinz quadruple well, 8 seeds x 3 lags x
2 cluster counts. For each adjacent pair of slow timescales we record whether
the 95% posterior CIs overlap (statistically unresolved) and whether the
rigorous enclosures overlap (numerically unresolved).

Writes kt2_degeneracy.json.
"""
import json
import os

import numpy as np
from deeptime.clustering import KMeans
from deeptime.data import prinz_potential
from deeptime.markov import TransitionCountEstimator
from deeptime.markov.msm import BayesianMSM, MarkovStateModel

import kt2_common as kc

HERE = os.path.dirname(os.path.abspath(__file__))


def safe(fn, *a, **kw):
    try:
        return fn(*a, **kw)
    except Exception:
        return None


def product_chain(p, q):
    A = np.array([[1 - p, p], [p, 1 - p]])
    B = np.array([[1 - q, q], [q, 1 - q]])
    return np.kron(A, B)


def simulate(T, n, seed):
    rng = np.random.default_rng(seed)
    n_states = T.shape[0]
    cdf = np.cumsum(T, axis=1)
    s = 0
    out = np.empty(n, dtype=np.int32)
    u = rng.random(n)
    for t in range(n):
        s = int(np.searchsorted(cdf[s], u[t]))
        out[t] = s
    return out


def counts(dtraj, lag):
    # sliding-effective = sliding/lag: exact rational, and the counting mode
    # deeptime's BayesianMSM requires.
    return TransitionCountEstimator(lagtime=lag, count_mode="sliding-effective") \
        .fit_fetch(dtraj).submodel_largest()


def integer_counts(cm, lag):
    C = np.asarray(cm.count_matrix) * lag
    Ci = np.rint(C).astype(np.int64)
    assert np.allclose(C, Ci), "sliding-effective counts are not integer/lag"
    return Ci


def bayes_ci(cm, lag, k, n_samples=400):
    b = BayesianMSM(n_samples=n_samples, reversible=True, lagtime=lag).fit_fetch(cm)
    ts = np.array([m.timescales(k=k) for m in b.samples])
    lo, hi = np.percentile(ts, 2.5, axis=0), np.percentile(ts, 97.5, axis=0)
    return lo, hi, ts.std(axis=0)


def part_b1():
    p = 0.02
    out = []
    for rel in [1.0, 0.3, 0.1, 3e-2, 1e-2, 3e-3, 1e-3, 1e-4, 0.0]:
        q = p * (1 - rel)
        T = product_chain(p, q)
        true_gap = abs((1 - 2 * p) - (1 - 2 * q))
        for n in [10000, 100000]:
            d = simulate(T, n, seed=7)
            cm = counts(d, 1)
            C = integer_counts(cm, 1)
            if C.shape[0] < 4:
                continue
            # An isolation failure is itself a result: the certificate refuses
            # instead of returning an unjustified number.
            c53 = safe(kc.certified_spectrum, C, 1, prec=53, k=4)
            c333 = safe(kc.certified_spectrum, C, 1, prec=333, k=4)
            gap = safe(kc.certified_gap, C, 1, 1, 2, prec=333)
            if c333 is None:
                out.append({"rel_detuning": rel, "n": n,
                            "cert_isolation_failure": True,
                            "p53_failed": c53 is None, "p333_failed": True})
                print("B1", rel, n, "ISOLATION FAILURE (p333)", flush=True)
                continue
            Tm = C / C.sum(axis=1, keepdims=True)
            ev = np.linalg.eigvals(Tm)
            ev = ev[np.argsort(-np.abs(ev))]
            lo, hi, sd = bayes_ci(cm, 1, 3)
            rec = {
                "rel_detuning": rel, "p": p, "q": q, "true_slow_gap": true_gap,
                "n": n,
                "p53_failed": c53 is None,
                "cert_absrad_p53": None if c53 is None else [e["abs_rad"] for e in c53["eigs"]],
                "cert_absrad_p333": [e["abs_rad"] for e in c333["eigs"]],
                "cert_its_rad_p53": None if c53 is None else [e["its_rad"] for e in c53["eigs"]],
                "cert_its_mid": [e["its_mid"] for e in c333["eigs"]],
                "cert_gap23": gap,
                "numpy_max_abs_imag": float(np.max(np.abs(ev.imag))),
                "numpy_complex_pair": bool(np.max(np.abs(ev.imag)) > 1e-12),
                "bayes_ci95_width": (hi - lo).tolist(),
                "bayes_std": sd.tolist(),
                "bayes_ci_overlap_23": bool(lo[0] <= hi[1] and lo[1] <= hi[0]),
            }
            out.append(rec)
            print("B1", rel, n, "done", flush=True)
    return out


def part_b2():
    out = []
    for seed in range(8):
        sysd = prinz_potential(h=1e-5, n_steps=100)
        x = sysd.trajectory(np.array([[0.0]]), 50000, seed=100 + seed)
        for nclus in (20, 40):
            km = KMeans(n_clusters=nclus, fixed_seed=seed, n_jobs=1).fit_fetch(x)
            dt = km.transform(x)
            for lag in (5, 10, 25):
                cm = counts(dt, lag)
                C = integer_counts(cm, lag)
                if C.shape[0] < 6:
                    continue
                try:
                    cert = kc.certified_spectrum(C, lag, prec=333, k=5)
                except Exception as exc:  # isolation failure is itself a datum
                    out.append({"seed": seed, "nclus": nclus, "lag": lag,
                                "cert_error": str(exc)})
                    continue
                lo, hi, sd = bayes_ci(cm, lag, 4, n_samples=300)
                its_mid = [e["its_mid"] for e in cert["eigs"][1:]]
                its_rad = [e["its_rad"] for e in cert["eigs"][1:]]
                stat_overlap, cert_overlap, rel_gap = [], [], []
                for i in range(3):
                    stat_overlap.append(bool(lo[i] <= hi[i + 1] and lo[i + 1] <= hi[i]))
                    a_lo, a_hi = its_mid[i] - its_rad[i], its_mid[i] + its_rad[i]
                    b_lo, b_hi = its_mid[i + 1] - its_rad[i + 1], its_mid[i + 1] + its_rad[i + 1]
                    cert_overlap.append(bool(a_lo <= b_hi and b_lo <= a_hi))
                    rel_gap.append((its_mid[i] - its_mid[i + 1]) / its_mid[i])
                out.append({
                    "seed": seed, "nclus": nclus, "lag": lag,
                    "n_states": int(C.shape[0]),
                    "its_mid": its_mid, "its_rad": its_rad,
                    "bayes_ci95_width": (hi - lo).tolist(),
                    "rel_gap": rel_gap,
                    "stat_overlap": stat_overlap,
                    "cert_overlap": cert_overlap,
                })
                print("B2", seed, nclus, lag, "done", flush=True)
    return out


if __name__ == "__main__":
    res = {"b1_controlled_degeneracy": part_b1(), "b2_prinz_survey": part_b2()}
    with open(os.path.join(HERE, "kt2_degeneracy.json"), "w") as f:
        json.dump(res, f, indent=1)
    print("wrote kt2_degeneracy.json")
