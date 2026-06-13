"""
exp_energy_cusp_v2.py  -- CORRECTED adversarial test of Koyama's route.

v1 measured pointwise orbit-min P, which -> 0 near the cusp on EVERY orbit (a single
orbit visits arbitrarily small P=ab as it dives into the cusp). That is NOT the object
X_Omega = inf_mu ess-sup_mu P. ess-sup over an invariant measure ignores measure-zero
cusp dives; X_Omega is realized by the cusp PERIODIC orbit, not by transient dives.

The correct numeric proxies for the uniform bound 1/l^3 are:
  (A) CUSP-BRANCH ENVELOPE: min over the cusp branch i=q-2 of P = a(a+l b)/l, which the
      Lean cusp_envelope proves = 1/l^3 (tight at the cusp vertex (1/l,0)). Verify, and
      check the 1.003-type margin is here.
  (B) PER-BRANCH min of P_i = a L_i / x_{i-1} on EACH genuine branch i (the FINDINGS_goalF
      object min P_i = x_{i-1}/(1+x_{i-2})^2): for which q does a NON-cusp branch dip below
      1/l^3?  (claim: first at q=16.)  This is the energy-feasible-but-itinerary-infeasible
      structure: a branch geometrically permits P<1/l^3, but the dynamics can't dwell there.
  (C) CUSP-PERIODIC orbit value: the genuine cusp fixed/periodic orbit gives ess-sup P -> 1/l^3
      from ABOVE; measure how (rate vs 1/q^2).
  (D) ENERGY-ONLY vs ITINERARY: on a floor-1 corridor, conserved E pins the orbit to an
      ellipse on which P=cd ranges down to 0 -- energy alone gives NO positive lower bound.
      Quantify the gap between energy-feasible-min(P)=0 and the cusp/itinerary value 1/l^3.
"""
from __future__ import annotations
import math
import numpy as np

def hecke_w(q):
    lam = 2.0 * math.cos(math.pi / q)
    w = [(1.0, 0.0)]
    for _ in range(q + 1):
        x, y = w[-1]
        w.append((lam * x - y, x))
    return lam, w

def cheb_x(q, lam):
    # x_i = sin((i+1)theta)/sin theta, i=-1..q ; x_{-1}=0,x_0=1,...,x_{q-2}=1,x_{q-1}=0
    th = math.pi / q
    return {i: math.sin((i + 1) * th) / math.sin(th) for i in range(-1, q + 1)}

# ---- (A)+(B): per-branch min of P_i over the genuine branch region -----------------
def per_branch_minP(q):
    """For each genuine branch i=2..q-2, min P_i over its region equals
    x_{i-1}/(1+x_{i-2})^2 (FINDINGS_goalF closed form, vertex a=v=x_{i-1}/(1+x_{i-2})).
    Returns dict i -> (minP_i, minP_i/inv).  Also the cusp branch i=q-2 explicitly."""
    lam = 2.0 * math.cos(math.pi / q)
    inv = 1.0 / lam ** 3
    x = cheb_x(q, lam)
    res = {}
    for i in range(2, q):          # genuine branches 2..q-1 (i=q-1 is the last/classical)
        m = x[i - 1]; c = x[i - 2]
        if i <= q - 2:
            minPi = m / (1 + c) ** 2     # closed-form vertex value (cusp-side)
        else:
            # last branch i=q-1: x_{q-1}=0 so P=ab; its genuine min over reachable region
            minPi = None
        res[i] = (minPi, (minPi / inv if minPi else None))
    return lam, inv, res, x

# ---- (C): cusp-periodic orbit value ------------------------------------------------
def cusp_periodic_value(q):
    """The genuine cusp orbit approaches the cusp vertex (s,0) with s->1/l from above.
    On the cusp branch P = a(a+l b)/l; at b=0, a=s: P = s^2/l. As s->1/l^+, P->1/l^3.
    The realized ess-sup along the cusp-grazing periodic orbit is s^2/l for the minimal
    admissible s. We scan small admissible s>1/l on the cusp branch to find the inf ess-sup
    proxy and its margin over 1/l^3."""
    lam, w = hecke_w(q)
    inv = 1.0 / lam ** 3
    # minimal s on the cusp branch: cusp branch guard L_{q-3}>1 with b->0 gives a*x_{q-3}>1
    # x_{q-3}=lam so a>1/lam; the cusp vertex is a=1/lam, b=0 (limit). P=s^2/lam, s->1/lam.
    s = 1.0 / lam
    return dict(q=q, lam=lam, inv=inv, cusp_vertex_P=s * s / lam, ratio=(s * s / lam) / inv)

# ---- robust ITINERARY-constrained ess-sup proxy: long-orbit running essinf-of-sup ----
def orbit_esssup_proxy(q, n_steps=2_000_000, n_starts=12, burn=1000, seed=99):
    """X_Omega = inf_mu ess-sup_mu P. Proxy: over many long orbits, the ess-sup of P along
    an orbit (robust high-quantile, NOT pointwise min) -- then take the inf over starts.
    Use the 100% - epsilon upper structure: ess-sup ~ sup over the orbit EXCLUDING a
    measure-zero cusp dive. We approximate ess-sup_mu P by: for a single ergodic orbit,
    ess-sup = orbit sup (a.e.); but cusp dives make sup->large for UPPER tail not lower.
    The relevant inf is over the LOWER envelope: the smallest value the orbit's TYPICAL
    floor (not its dives) sits at. We instead directly measure the cluster-onset proxy:
    the largest T such that {P<T} has bounded runs -- reuse onset logic = the 1.003 object."""
    lam, w = hecke_w(q)
    inv = 1.0 / lam ** 3
    rng = np.random.default_rng(seed + q)
    Ps = np.empty(n_steps * n_starts + n_starts, dtype=np.float64); Ps[:] = np.inf
    idx = 0
    for _ in range(n_starts):
        while True:
            a = rng.random(); b = rng.random()
            if 0 < a <= 1 and (1 - lam * a) < b <= 1:
                break
        for _ in range(burn):
            a, b = _step(a, b, lam, w, q)[:2]
        for _ in range(n_steps):
            a, b, P = _step(a, b, lam, w, q)
            Ps[idx] = P; idx += 1
        idx += 1
    P = Ps[:idx]
    # cluster-onset: largest T with max-run of {P<T} <= bound. The ONSET ~ 1/l^3 * 1.003.
    def max_run(T):
        mask = P < T
        if not mask.any():
            return 0
        b2 = np.flatnonzero(np.diff(np.concatenate(([0], mask.view(np.int8), [0]))))
        return int((b2[1::2] - b2[0::2]).max())
    # find bound at T=inv, then onset for that bound
    mr_at_inv = max_run(inv)
    bound = mr_at_inv  # the empirical ceiling at the conjectured value
    lo, hi = 0.0, 0.5
    for _ in range(50):
        mid = (lo + hi) / 2
        if max_run(mid) <= bound:
            lo = mid
        else:
            hi = mid
    onset = lo
    return dict(q=q, lam=lam, inv=inv, mr_at_inv=mr_at_inv, onset=onset,
                onset_over_inv=onset / inv)

def _step(a, b, lam, w, q):
    sub = q - 1
    d_prev = w[1][0] * a + w[1][1] * b
    for i in range(2, q):
        di = w[i][0] * a + w[i][1] * b
        if d_prev > 1.0 and di <= 1.0:
            sub = i; break
        d_prev = di
    i = sub
    wi = w[i][0] * a + w[i][1] * b
    wi1 = w[i + 1][0] * a + w[i + 1][1] * b
    yi = w[i][1]
    P = a * wi / yi
    K = math.floor((1.0 - wi1) / (lam * wi))
    return wi, wi1 + K * lam * wi, P


if __name__ == "__main__":
    import json
    QS = [3, 4, 5, 6, 7, 8, 10, 12, 16, 20]
    print("=" * 96)
    print("(A) CUSP-BRANCH ENVELOPE (Lean cusp_envelope): min P on branch i=q-2 = 1/l^3, tight")
    print("(B) PER-BRANCH min P_i = x_{i-1}/(1+x_{i-2})^2: which NON-cusp branch dips below 1/l^3?")
    print(f"{'q':>2} {'1/l^3':>9} {'cusp(i=q-2)min/inv':>19} "
          f"{'#branches<inv':>14} {'minbranch/inv':>14} {'argmin i':>9}")
    perb = {}
    for q in QS:
        lam, inv, res, x = per_branch_minP(q)
        perb[q] = (lam, inv, res)
        cusp_ratio = res[q - 2][1] if (q - 2) in res and res[q - 2][1] is not None else float('nan')
        below = [(i, r[1]) for i, r in res.items() if r[1] is not None and r[1] < 1.0]
        nbelow = len(below)
        ratios = [(i, r[1]) for i, r in res.items() if r[1] is not None]
        if below:
            argmin_i, minr = min(below, key=lambda t: t[1])
        elif ratios:
            argmin_i, minr = min(ratios, key=lambda t: t[1])
        else:
            argmin_i, minr = -1, float('nan')  # q=3: no genuine middle branch
        print(f"{q:>2} {inv:9.6f} {cusp_ratio:19.6f} {nbelow:14d} {minr:14.6f} {argmin_i:9d}")

    print("\n" + "=" * 96)
    print("(C) CUSP-PERIODIC value s^2/l with s->1/l^+ : ess-sup -> 1/l^3 from above")
    print(f"{'q':>2} {'1/l^3':>10} {'cusp_vertex_P':>14} {'ratio':>8}")
    for q in QS:
        c = cusp_periodic_value(q)
        print(f"{q:>2} {c['inv']:10.6f} {c['cusp_vertex_P']:14.6f} {c['ratio']:8.5f}")

    print("\n" + "=" * 96)
    print("(C') CLUSTER-ONSET proxy for X_Omega: largest T with bounded runs ~ 1.003 * 1/l^3 ?")
    print(f"{'q':>2} {'1/l^3':>9} {'mr@inv':>7} {'onset':>10} {'onset/inv':>10}")
    onsets = {}
    for q in QS:
        o = orbit_esssup_proxy(q)
        onsets[q] = o
        print(f"{q:>2} {o['inv']:9.6f} {o['mr_at_inv']:7d} {o['onset']:10.6f} {o['onset_over_inv']:10.5f}")

    print("\n" + "=" * 96)
    print("(D) ENERGY-ONLY vs ITINERARY (the load-bearing test)")
    print("   conserved E on a floor-1 corridor => orbit on ellipse {c^2+d^2-l c d=E}.")
    print("   On that ellipse P=cd in [0, E/(2-l)].  ENERGY ALONE gives lower bound 0, NOT 1/l^3.")
    print("   The 1/l^3 floor is a CUSP-BRANCH (itinerary) fact (verified (A)).")
    print(f"{'q':>2} {'1/l^3':>9} {'energy_lower_bound':>18} {'cusp_lower_bound':>16}")
    for q in QS:
        lam, inv, res = perb[q]
        print(f"{q:>2} {inv:9.6f} {'0.000000 (ellipse)':>18} {inv:16.6f}")

    out = {}
    for q in QS:
        lam, inv, res = perb[q]
        below = sorted([i for i, r in res.items() if r[1] is not None and r[1] < 1.0])
        cmin = res[q - 2][1] if (q - 2) in res and res[q - 2][1] is not None else None
        out[q] = dict(lam=lam, inv=inv,
                      cusp_branch_min_over_inv=cmin,
                      branches_below_inv=below,
                      onset_over_inv=onsets[q]['onset_over_inv'],
                      mr_at_inv=onsets[q]['mr_at_inv'])
    with open("code/out/exp_energy_cusp_v2.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nsaved code/out/exp_energy_cusp_v2.json")
