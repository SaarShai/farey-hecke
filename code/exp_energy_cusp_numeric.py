"""
exp_energy_cusp_numeric.py
==========================
ADVERSARIAL numerical test of KOYAMA'S ROUTE for the uniform lower bound
    X_Omega(q) = inf_mu ess-sup_mu P  >=  1/lambda_q^3   (all Hecke q).

Koyama's claim: the bound follows from
  (energy)  E = c_n^2 + c_{n+1}^2 - l c_n c_{n+1}  conserved on a floor-1 (rotation) corridor,
  (cusp)    coupled with the rate of escape-of-mass into the cusp,
  => uniform spectral constraint via transfer operator.

We test, along GENUINE G_q-BCZ orbits (Taha 1810.10668, Thm 2.2), q=3,4,5,6,7,8,10,12:
 (a)(i)   orbit P_min and ratio to 1/l^3 (and to X(q)).
 (a)(ii)  distribution of corridor (floor-1 run, k=1) lengths;
          where is the orbit P-infimum hit -- corridor BOUNDARY (cusp entry/exit, k>=2 kick)
          or corridor INTERIOR (pure rotation k=1)?
 (a)(iii) escape-of-mass rate: fraction of orbit time near the cusp; tail of excursion-depth dist.
 (b)      how P_min / (1/l^3) approaches 1; rate vs O(1/q^2).
 (c)      ENERGY-ONLY feasibility: ignoring itinerary, what is the lowest P the conserved-energy
          bound alone permits on a corridor?  Construct energy-feasible-but-itinerary-infeasible
          region -> is the cusp-escape coupling LOGICALLY NECESSARY (energy alone too weak)?

The map is run in the (a,b) Farey-triangle coords and ALSO read off as the scalar
recurrence c_n (the consecutive denominators / coordinates the energy form lives on):
along the orbit a_{n+1}=w_i.(a_n,b_n), so the sequence of FIRST coordinates a_n is the
scalar sequence; the floor K_n = floor((1-w_{i+1}.(a,b))/(l w_i.(a,b))) is the corridor index.
On the last branch i=q-1 (the uniform classical-shaped branch) the map is
   (a,b) -> (b, -a + K l b),  K = floor((1+a)/(l b)),  P = a b,
and a floor-1 run there is exactly c_{n+2} = l c_{n+1} - c_n (the rotation recurrence).
"""
from __future__ import annotations
import math
import numpy as np

# ----------------------------------------------------------------------------- map
def hecke_w(q):
    lam = 2.0 * math.cos(math.pi / q)
    w = [(1.0, 0.0)]
    for _ in range(q + 1):
        x, y = w[-1]
        w.append((lam * x - y, x))
    return lam, w

def Xq(q):
    lam = 2.0 * math.cos(math.pi / q)
    if q == 3: return 2.0 / 9.0
    if q == 4: return math.sqrt(2.0) / 8.0
    return 1.0 / lam ** 3

def step(a, b, lam, w, q):
    """One genuine G_q-BCZ step. Returns (a',b', branch i, floor K, P, Lcusp)
    Lcusp = a+ l b - ... used for cusp-proximity; P=1/R_q observable."""
    # branch: smallest i in 2..q-1 with d_{i-1}>1 and d_i<=1 (d decreasing)
    sub = q - 1
    d_prev = w[1][0] * a + w[1][1] * b
    for i in range(2, q):
        di = w[i][0] * a + w[i][1] * b
        if d_prev > 1.0 and di <= 1.0:
            sub = i
            break
        d_prev = di
    i = sub
    wi = w[i][0] * a + w[i][1] * b
    wi1 = w[i + 1][0] * a + w[i + 1][1] * b
    yi = w[i][1]
    P = a * wi / yi
    K = math.floor((1.0 - wi1) / (lam * wi))
    a2, b2 = wi, wi1 + K * lam * wi
    return a2, b2, i, K, P

def random_start(lam, rng):
    while True:
        a = rng.random(); b = rng.random()
        if 0 < a <= 1 and (1 - lam * a) < b <= 1:
            return a, b

# ----------------------------------------------------------------------------- experiment
def run(q, n_steps=4_000_000, n_starts=8, burn=500, seed=20260612):
    rng = np.random.default_rng(seed + q)
    lam, w = hecke_w(q)
    X = Xq(q); inv = 1.0 / lam ** 3
    Pmin = math.inf
    Pmin_K = None              # floor at the P-min point
    Pmin_runpos = None         # position within its floor-1 run (0 = corridor entry)
    # corridor (floor-1 run) length histogram
    corr_hist = {}
    # for "where is P-inf hit": classify each step as corridor-interior (K==1 AND prev step K==1)
    # vs corridor-boundary (entry: this step K>=2, or next step K>=2)
    below_inv_interior = 0     # P<1/l^3 at a pure-rotation interior step
    below_inv_boundary = 0     # P<1/l^3 at a corridor boundary step (K>=2 here or adjacent)
    # escape-of-mass: count steps within cusp-proximity bands of the cusp vertex.
    # cusp vertex for last branch is (a,b)~(0,1)/(1,0): proximity ~ min(a,b) small => P=ab small.
    # We track P itself as cusp-depth proxy on last branch + fraction of time with K>=2 (a "kick").
    near_cusp = 0              # steps with P < 2*inv (deep band)
    n_kick = 0                 # steps with K>=2
    total = 0
    # excursion depth: for each maximal run of consecutive P<X, record (length, min P in run)
    run_lengths = []
    run_minP = []

    for _ in range(n_starts):
        a, b = random_start(lam, rng)
        for _ in range(burn):
            a, b, i, K, P = step(a, b, lam, w, q)
        prevK = None
        cur_run_len = 0          # current floor-1 corridor length
        # store per-step (P, K) in a small ring to classify P-min neighborhood
        seqP = []; seqK = []
        ex_len = 0; ex_min = math.inf  # current P<X excursion
        for _ in range(n_steps):
            a, b, i, K, P = step(a, b, lam, w, q)
            total += 1
            seqP.append(P); seqK.append(K)
            if K >= 2:
                n_kick += 1
            if P < 2 * inv:
                near_cusp += 1
            # corridor bookkeeping: floor-1 run length
            if K == 1:
                cur_run_len += 1
            else:
                if cur_run_len > 0:
                    corr_hist[cur_run_len] = corr_hist.get(cur_run_len, 0) + 1
                cur_run_len = 0
            # P-min tracking
            if P < Pmin:
                Pmin = P
                Pmin_K = K
            # excursion (run of P<X)
            if P < X:
                ex_len += 1
                ex_min = min(ex_min, P)
            else:
                if ex_len > 0:
                    run_lengths.append(ex_len); run_minP.append(ex_min)
                ex_len = 0; ex_min = math.inf
            prevK = K
        if cur_run_len > 0:
            corr_hist[cur_run_len] = corr_hist.get(cur_run_len, 0) + 1
        if ex_len > 0:
            run_lengths.append(ex_len); run_minP.append(ex_min)
        # classify below-inv steps as interior vs boundary using the stored sequence
        for idx in range(len(seqP)):
            if seqP[idx] < inv:
                kh = seqK[idx]
                kp = seqK[idx - 1] if idx > 0 else 99
                kn = seqK[idx + 1] if idx + 1 < len(seqK) else 99
                if kh == 1 and kp == 1 and kn == 1:
                    below_inv_interior += 1
                else:
                    below_inv_boundary += 1

    return dict(q=q, lam=lam, X=X, inv=inv, Pmin=Pmin, Pmin_K=Pmin_K,
                ratio_inv=Pmin / inv, ratio_X=Pmin / X,
                corr_hist=corr_hist, below_inv_interior=below_inv_interior,
                below_inv_boundary=below_inv_boundary,
                near_cusp_frac=near_cusp / total, kick_frac=n_kick / total,
                run_lengths=run_lengths, run_minP=run_minP, total=total)


# ----------------------------------------------------------------------------- (c) energy-only
def energy_only_minP(q, n_grid=20_000_000, seed=7):
    """Ignoring itinerary, on a floor-1 (rotation) corridor with conserved energy
    E = c_n^2 + c_{n+1}^2 - l c_n c_{n+1}, the orbit lies on the ELLIPSE of given E.
    The observable on the last branch is P = c_n*c_{n+1}.  Question: over the ellipse
    (all energy-feasible pairs (c_n,c_{n+1})>0), what is the RANGE of P = c_n c_{n+1}?
    Energy alone allows the pair to slide along the ellipse to the c-axes => P -> 0.
    We compute the energy-feasible min/max of P given the orbit's actual E budget,
    and compare to 1/l^3.  If energy-feasible-min(P) << 1/l^3 while genuine-orbit-min(P)
    ~ 1/l^3, the cusp/itinerary coupling is what lifts the bound (logically necessary).

    Concretely: take the genuine orbit's typical corridor energy E*, then the ellipse
    {c^2 + d^2 - l c d = E*, c,d>0} has P = c d ranging in [0, E*/(2-l)] (max at c=d).
    The lower end P->0 is energy-feasible.  So energy ALONE never pins P>=1/l^3.
    """
    lam, w = hecke_w(q)
    inv = 1.0 / lam ** 3
    rng = np.random.default_rng(seed + q)
    # sample genuine corridor energies E along orbits (consecutive c_n on the scalar last-branch)
    a, b = random_start(lam, rng)
    for _ in range(500):
        a, b, i, K, P = step(a, b, lam, w, q)
    Es = []
    Pcd = []  # actual P=c*d at corridor points
    c_prev = a
    for _ in range(2_000_000):
        a, b, i, K, P = step(a, b, lam, w, q)
        c = a  # first coordinate is the scalar c_n
        E = c_prev ** 2 + c ** 2 - lam * c_prev * c
        Es.append(E)
        Pcd.append(c_prev * c)
        c_prev = c
    Es = np.array(Es); Pcd = np.array(Pcd)
    Emed = float(np.median(Es))
    # energy-feasible P range for a typical corridor energy: P in [0, Emed/(2-lam)]
    Pmax_feasible = Emed / (2 - lam)
    return dict(q=q, lam=lam, inv=inv, E_median=Emed,
                P_energy_feasible_min=0.0, P_energy_feasible_max=Pmax_feasible,
                actual_P_min=float(Pcd.min()), actual_P_med=float(np.median(Pcd)))


if __name__ == "__main__":
    import json, sys
    QS = [3, 4, 5, 6, 7, 8, 10, 12]
    results = {}
    print("=" * 92)
    print("(a)(i)/(b)  ORBIT P_min vs 1/lambda^3 and X(q)  [genuine G_q-BCZ]")
    print(f"{'q':>2} {'lam':>8} {'1/l^3':>9} {'X(q)':>9} {'orbitPmin':>10} "
          f"{'Pmin/inv':>9} {'Pmin/X':>8} {'PminK':>6}")
    for q in QS:
        r = run(q)
        results[q] = r
        print(f"{q:>2} {r['lam']:8.5f} {r['inv']:9.6f} {r['X']:9.6f} {r['Pmin']:10.7f} "
              f"{r['ratio_inv']:9.5f} {r['ratio_X']:8.5f} {str(r['Pmin_K']):>6}")

    print("\n" + "=" * 92)
    print("(a)(ii)  CORRIDOR (floor-1 run) length distribution + WHERE P<1/l^3 occurs")
    print(f"{'q':>2} {'maxCorr':>8} {'meanCorr':>9} {'corr_hist(len:count, top6)':>30}")
    for q in QS:
        r = results[q]
        ch = r['corr_hist']
        mx = max(ch) if ch else 0
        tot = sum(k * v for k, v in ch.items())
        n = sum(ch.values())
        mean = tot / n if n else 0
        top = sorted(ch.items())[:6]
        print(f"{q:>2} {mx:>8} {mean:9.3f}   " + " ".join(f"{k}:{v}" for k, v in top))
    print(f"\n   P<1/l^3 location: INTERIOR (pure-rotation k=1, both neighbors k=1) "
          f"vs BOUNDARY (a k>=2 kick at/adjacent)")
    print(f"{'q':>2} {'#below_inv':>11} {'interior':>10} {'boundary':>10} {'bndry_frac':>11}")
    for q in QS:
        r = results[q]
        bi = r['below_inv_interior']; bb = r['below_inv_boundary']
        tot = bi + bb
        print(f"{q:>2} {tot:>11} {bi:>10} {bb:>10} {(bb/tot if tot else 0):11.4f}")

    print("\n" + "=" * 92)
    print("(a)(iii)  ESCAPE-OF-MASS rate (fraction of time near cusp / with k>=2 kick)")
    print(f"{'q':>2} {'near_cusp_frac':>15} {'kick_frac(k>=2)':>16} "
          f"{'maxExcDepth(minP/inv)':>22}")
    for q in QS:
        r = results[q]
        rm = np.array(r['run_minP']) if r['run_minP'] else np.array([r['inv']])
        deepest = rm.min() / r['inv']
        print(f"{q:>2} {r['near_cusp_frac']:15.5f} {r['kick_frac']:16.5f} {deepest:22.5f}")

    print("\n" + "=" * 92)
    print("(c)  ENERGY-ONLY feasibility: does conserved E ALONE permit P<1/l^3?")
    print("     On a corridor ellipse {c^2+d^2-l c d = E}, P=c d in [0, E/(2-l)].")
    print(f"{'q':>2} {'1/l^3':>9} {'E_median':>10} {'P_feas_max':>11} {'P_feas_min':>11} "
          f"{'actualPmin':>11}")
    energy = {}
    for q in QS:
        e = energy_only_minP(q)
        energy[q] = e
        print(f"{q:>2} {e['inv']:9.6f} {e['E_median']:10.6f} {e['P_energy_feasible_max']:11.6f} "
              f"{e['P_energy_feasible_min']:11.6f} {e['actual_P_min']:11.7f}")
    print("\n  => energy-feasible P range INCLUDES 0 (slide along ellipse to the axes),")
    print("     so the conserved-energy bound ALONE never forbids P<1/l^3.")
    print("     The lower bound P>=1/l^3 must come from the ITINERARY (cusp-branch geometry).")

    # save a compact JSON for the writeup
    out = {}
    for q in QS:
        r = results[q]; e = energy[q]
        ch = r['corr_hist']
        out[q] = dict(
            lam=r['lam'], inv=r['inv'], X=r['X'],
            orbit_Pmin=r['Pmin'], ratio_inv=r['ratio_inv'], ratio_X=r['ratio_X'],
            Pmin_K=r['Pmin_K'],
            max_corr=(max(ch) if ch else 0),
            mean_corr=(sum(k * v for k, v in ch.items()) / sum(ch.values()) if ch else 0),
            below_inv_interior=r['below_inv_interior'],
            below_inv_boundary=r['below_inv_boundary'],
            near_cusp_frac=r['near_cusp_frac'], kick_frac=r['kick_frac'],
            E_median=e['E_median'], P_energy_feas_max=e['P_energy_feasible_max'],
            energy_only_Pmin=e['actual_P_min'],
        )
    with open("code/out/exp_energy_cusp_numeric.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nsaved code/out/exp_energy_cusp_numeric.json")
