"""
T5: Adjudicate whether the residual exponent "0.63" in

    NW(Q) - C = M(Q)^2/(6Q) - Theta(Q^{-0.63})

is a GENUINE critical exponent, or a PRE-ASYMPTOTIC sqrt(Q)-oscillation
envelope (the function-field prediction: true exponent is exactly 1/2,
modulated by zeta-zero oscillations, mimicking ~0.63 over a finite range).

GROUND TRUTH for NW(Q):
  NW(Q) = Q * J(Q) / Phi(Q),  Phi(Q) = |F_Q| (Farey count incl. 1/1),
  J(Q)  = int_0^1 E_Q(x)^2 dx  computed EXACTLY (float) by enumerating F_Q
          and integrating the piecewise-linear E_Q exactly per interval.
This is the exact second moment -- NO truncation bias (unlike the
Mikolas-truncated J, which underestimates J by O(1/m_max) and is therefore
useless for measuring an O(Q^{-0.6}) residual).

C = A065483 (totient/Feller-Tornier-adjacent), the empirical NW limit.
M(Q) = classical Mertens function (cheap linear sieve).

We then:
 (3) fit R(Q) ~ A Q^{-delta} on sliding geometric windows [Q,4Q] -> drift table
 (4) test whether |R(Q)| sqrt(Q) oscillates / changes sign
 (5) build an explicit-formula toy model R_model = sum_rho Q^{-1/2}cos(gamma log Q+phi)
     whose TRUE exponent is exactly 0.5, fit a single power to it, see if
     delta_eff comes out ~0.6 over the same Q range.
"""
from __future__ import annotations
import sys, math, time, json
import numpy as np

CODE = "/Users/za/Documents/Farey NOW/projects/mimo-mini-project/code"
BCZ = "/Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-15-D1-bcz-cocycle"
sys.path.insert(0, BCZ)
from verify_bcz_cocycle import J_direct_fast, farey  # exact J(Q), Farey enumerator

# The empirical NW limit C. The repo is ambiguous about its exact closed
# form: twin-prime/2 = 0.66016181584... is used in most project code; the
# task brief cites A065483 ~ 0.6602. R(Q)=NW-C-M^2/(6Q) is SENSITIVE to C at
# the ~1e-4 level (comparable to R at large Q), so we run the analysis for
# several candidate C AND estimate C from the data (NW - M^2/(6Q) -> C as
# Q->inf), then check that conclusions are robust across all of them.
C_CANDIDATES = {
    "twinprime_half": 0.6601618158468696,   # Pi_2 / 2 (most-used in repo)
    "A065483_task":   0.6602994192095995,    # value cited in task brief
}


# ----------------------------------------------------------------------
def sieve_mertens(N: int) -> np.ndarray:
    """M[n] = sum_{k<=n} mu(k), n=0..N, via linear sieve."""
    mu = np.zeros(N + 1, dtype=np.int8)
    mu[1] = 1
    is_comp = bytearray(N + 1)
    primes = []
    for i in range(2, N + 1):
        if not is_comp[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            ip = i * p
            if ip > N:
                break
            is_comp[ip] = 1
            if i % p == 0:
                mu[ip] = 0
                break
            else:
                mu[ip] = -mu[i]
    return np.cumsum(mu.astype(np.int64))


def nw_exact(Q: int) -> tuple[float, int]:
    """Exact NW(Q) = Q J(Q)/Phi(Q) and Phi(Q)=|F_Q|."""
    F = farey(Q)
    Phi = len(F)
    J = J_direct_fast(Q)
    return Q * J / Phi, Phi


# ----------------------------------------------------------------------
def fit_power(Qs, Rabs):
    """log|R| = log A - delta log Q.  Return (delta, logA, n)."""
    x = np.log(np.asarray(Qs, float))
    y = np.log(np.asarray(Rabs, float))
    A = np.vstack([np.ones_like(x), x]).T
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    logA, slope = coef
    return -slope, logA, len(x)


# ----------------------------------------------------------------------
def explicit_formula_model(Qs, gammas, seed=0):
    """R_model(Q) = sum_gamma c_g Q^{-1/2} cos(gamma log Q + phi_g).
    TRUE envelope exponent is exactly 1/2. Random amplitudes/phases."""
    rng = np.random.default_rng(seed)
    Qs = np.asarray(Qs, float)
    R = np.zeros_like(Qs)
    for g in gammas:
        c = rng.uniform(0.5, 1.5)
        phi = rng.uniform(0, 2 * math.pi)
        R += c * Qs ** (-0.5) * np.cos(g * np.log(Qs) + phi)
    return R


# ----------------------------------------------------------------------
def analyze_for_C(Cval, Qarr, NWarr, Marr, label, out):
    """Run drift + sqrt(Q) tests for one choice of C. Returns summary dict."""
    Rarr = NWarr - Cval - Marr ** 2 / (6.0 * Qarr)
    res = {"C": Cval, "label": label}

    dg, lAg, ng = fit_power(Qarr, np.abs(Rarr))
    res["global_delta"] = dg

    # drift windows [Q0, 4 Q0]
    drift = []
    for q0 in np.geomspace(Qarr[0], Qarr[-1] / 4.0, 8):
        lo, hi = q0, 4 * q0
        sel = (Qarr >= lo) & (Qarr <= hi)
        if sel.sum() < 4:
            continue
        d, _, _ = fit_power(Qarr[sel], np.abs(Rarr[sel]))
        drift.append({"Q_lo": float(lo), "Q_hi": float(hi),
                      "npts": int(sel.sum()), "delta": float(d)})
    res["drift_windows"] = drift

    # R*sqrt(Q)
    Rsq = Rarr * np.sqrt(Qarr)
    signs = np.sign(Rarr)
    res["sign_changes_of_R"] = int(np.sum(signs[1:] * signs[:-1] < 0))
    res["Rsq_min"] = float(Rsq.min())
    res["Rsq_max"] = float(Rsq.max())
    res["Rsq_first_last_ratio"] = float(abs(Rsq[-1]) / (abs(Rsq[0]) + 1e-30))
    res["R_times_sqrtQ"] = [{"Q": int(q), "R_sqrtQ": float(v)}
                            for q, v in zip(Qarr, Rsq)]
    res["R_series"] = [{"Q": int(q), "R": float(r)}
                       for q, r in zip(Qarr, Rarr)]

    print(f"\n----- C = {label} ({Cval:.10f}) -----", flush=True)
    print(f"  global delta on |R| = {dg:.3f}", flush=True)
    print(f"  DRIFT [Q0,4Q0]:  " +
          "  ".join(f"{d['Q_lo']:.0f}->{d['delta']:.2f}" for d in drift),
          flush=True)
    print(f"  R*sqrtQ range [{Rsq.min():+.4f},{Rsq.max():+.4f}]  "
          f"|last|/|first|={res['Rsq_first_last_ratio']:.3f}  "
          f"sign-changes(R)={res['sign_changes_of_R']}", flush=True)
    return res


def main():
    t_all = time.time()
    out = {"method": "exact J_direct_fast (no truncation bias)",
           "C_candidates": C_CANDIDATES}

    # ---- (1)(2) generate dense, log-spaced exact NW(Q) ----
    # Geometric grid; J_direct_fast is O(Q^2). Q<=~26k feasible in budget.
    Qs = sorted(set(int(round(q)) for q in np.geomspace(1000, 26000, 34)))
    print(f"Generating exact NW(Q) at {len(Qs)} log-spaced Q in "
          f"[{Qs[0]},{Qs[-1]}]", flush=True)
    Mert = sieve_mertens(Qs[-1] + 10)

    rows = []
    for Q in Qs:
        t = time.time()
        NW, Phi = nw_exact(Q)
        Mq = int(Mert[Q])
        rows.append({"Q": Q, "Phi": int(Phi), "NW": NW, "M": Mq,
                     "mert_term": Mq * Mq / (6.0 * Q)})
        print(f"  Q={Q:6d} NW={NW:.7f} M={Mq:5d}  ({time.time()-t:.1f}s)",
              flush=True)
    out["data"] = rows

    Qarr = np.array([r["Q"] for r in rows], float)
    NWarr = np.array([r["NW"] for r in rows], float)
    Marr = np.array([r["M"] for r in rows], float)

    # data-driven C: average of (NW - M^2/(6Q)) over the largest-Q half,
    # where both correction terms are smallest. (Both M^2/6Q and the residual
    # ->0, so this estimates C; it is only a sanity anchor.)
    anchor = NWarr - Marr ** 2 / (6.0 * Qarr)
    half = len(anchor) // 2
    C_data = float(np.mean(anchor[half:]))
    out["C_data_estimate"] = C_data
    print(f"\nData-anchored C estimate (mean of NW - M^2/6Q over upper half) "
          f"= {C_data:.6f}", flush=True)

    # ---- (3)(4) run the full analysis for each candidate C ----
    out["per_C"] = {}
    for label, Cval in {**C_CANDIDATES, "data_estimate": C_data}.items():
        out["per_C"][label] = analyze_for_C(Cval, Qarr, NWarr, Marr, label, out)

    # ---- (5) explicit-formula toy model with TRUE exponent = 1/2 ----
    print("\n=== (5) Explicit-formula model (TRUE exp=0.5) over same Q range ===",
          flush=True)
    gammas = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
              37.586178, 40.918719, 43.327073, 48.005151, 49.773832]
    deltas_eff = []
    for seed in range(12):
        Rm = explicit_formula_model(Qarr, gammas, seed=seed)
        d, lA, n = fit_power(Qarr, np.abs(Rm))
        deltas_eff.append(d)
    deltas_eff = np.array(deltas_eff)
    out["model"] = {
        "gammas": gammas,
        "true_exponent": 0.5,
        "delta_eff_mean": float(deltas_eff.mean()),
        "delta_eff_std": float(deltas_eff.std()),
        "delta_eff_all": [float(x) for x in deltas_eff],
    }
    print(f"  fitted single-power delta_eff over 12 random realizations:")
    print(f"    mean={deltas_eff.mean():.3f}  std={deltas_eff.std():.3f}  "
          f"range=[{deltas_eff.min():.3f},{deltas_eff.max():.3f}]", flush=True)

    out["wall_seconds"] = time.time() - t_all
    with open(f"{CODE}/T5_adjudicate_063_results.json", "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nWrote {CODE}/T5_adjudicate_063_results.json "
          f"({out['wall_seconds']:.0f}s total)", flush=True)


if __name__ == "__main__":
    main()
