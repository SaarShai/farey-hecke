#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ogoal_transfer.py  (goal O) — Ulam transfer (Ruelle-Perron-Frobenius) operator for the genuine
Taha BCZ_q map, weighted potential phi=-beta*P, and the standard Gibbs measures mu_beta.

DEMONSTRATION (numerical). Builds the discretized weighted transfer operator
   (L_beta f)(x) = sum_{T y = x} e^{-beta P(y)} f(y)        (|det T'|=1, Lebesgue-preserving)
via a MASS-CONSERVING (sampled) Ulam method on a grid over Tq={0<a<=1, 1-lam a<b<=1}.
Each source cell is sampled on a sub-grid and its mass distributed over ALL target cells the
samples land in (so mass is not lost when an image straddles cells -- fixes the q>=7 leakage
of a single-center deterministic Ulam).

Per (q,beta):
  - leading eigenvalue rho(beta)=e^{pressure(-beta P)}; pressure log rho; free energy -log rho/beta
  - Gibbs mu_beta = leading LEFT eigenvector (cell masses); <P>_{mu_beta}; <a>,<b>
  - mu_beta mass within several cusp-vertex neighbourhoods (to test concentration vs escape)

HONEST OBJECTIVE NOTE: mu_beta is the standard (Birkhoff / min-AVERAGE) zero-temperature object;
as beta->inf it selects inf_mu int P = beta_min < 1/lam^3.  The project value X_Omega=1/lam^3 is
the min-MAX (ess-sup) object, demonstrated rigorously in Ogoal_value_seq.py.  This script shows
WHERE the standard mu_beta concentrates (interior, NOT the cusp) -- the cusp escape is special to
the ess-sup objective.  beta=0 must give rho=1 and the flat invariant density (validation gate).
"""
import math, json, os, sys
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import eigs

def lam(q): return 2*math.cos(math.pi/q)
def ellipse_x(q):
    """x[i] with w_i=(x[i], x[i-1]); x[-1]=0,x[0]=1, x[i]=lam x[i-1]-x[i-2]."""
    l = lam(q); x = {-1:0.0, 0:1.0}
    for i in range(1, q+5): x[i] = l*x[i-1]-x[i-2]
    return l, x
def in_Tq(a, b, l, eps=1e-9):
    return (a > 1e-9) and (a <= 1+eps) and (1 - l*a - eps < b <= 1+eps)
def branch_of(q, x, a, b, eps=1e-9):
    for i in range(2, q):
        if a*x[i-1]+b*x[i-2] > 1-eps and a*x[i]+b*x[i-1] <= 1+eps:
            return i
    return None
def step_P(q, x, l, a, b):
    i = branch_of(q, x, a, b)
    if i is None: return None
    Li = a*x[i]+b*x[i-1]; Li1 = a*x[i+1]+b*x[i]
    if l*Li <= 0: return None
    k = math.floor((1-Li1)/(l*Li))
    P = a*Li/x[i-1]
    return P, (Li, Li1+k*l*Li)

def build(q, N, S=6):
    l, x = ellipse_x(q)
    a0, a1 = 0.0, 1.0
    b0, b1 = 1.0-l, 1.0
    da = (a1-a0)/N; db = (b1-b0)/N
    cell_id = {}; centers = []
    for ia in range(N):
        ac = (ia+0.5)*da
        for ib in range(N):
            bc = b0 + (ib+0.5)*db
            if in_Tq(ac, bc, l):
                cell_id[(ia, ib)] = len(centers); centers.append((ac, bc))
    n = len(centers); centers = np.array(centers)
    def locate(a, b):
        ia = int((a-a0)/da); ib = int((b-b0)/db)
        if ia >= N: ia = N-1
        if ib >= N: ib = N-1
        if ia < 0 or ib < 0: return None
        return cell_id.get((ia, ib))
    rows=[]; cols=[]; data=[]; Pcell=np.full(n, np.nan)
    inv = {v:k for k,v in cell_id.items()}
    for src in range(n):
        ia, ib = inv[src]
        ca = ia*da; cb = b0 + ib*db
        tgt = {}; psum=0.0; pn=0; tot=0
        for sa in range(S):
            for sb in range(S):
                a = ca + (sa+0.5)/S*da
                b = cb + (sb+0.5)/S*db
                if not in_Tq(a, b, l): continue
                r = step_P(q, x, l, a, b)
                if r is None: continue
                P,(na, nb) = r
                if not in_Tq(na, nb, l): continue
                tid = locate(na, nb)
                if tid is None: continue
                tgt[tid] = tgt.get(tid, 0)+1; psum += P; pn += 1; tot += 1
        if tot == 0: continue
        Pcell[src] = psum/pn
        for tid, c in tgt.items():
            rows.append(src); cols.append(tid); data.append(c/tot)
    return dict(l=l, N=N, n=n, centers=centers,
                rows=np.array(rows), cols=np.array(cols), data=np.array(data),
                Pcell=Pcell)

def gibbs(q, N=140, S=6, betas=(0,0.25,0.5,1,2,3,4,6,8,12,16,24,32,48,64)):
    # NOTE: beta capped at ~64; beyond, the weighted spectrum collapses (rho underflows) and
    # ARPACK returns a spurious near-null eigenvector (a-edge garbage). 0..64 is the reliable
    # window for the freezing trend; precise beta_min comes from the word search (Ogoal_value_seq).
    gd = build(q, N, S); l = gd['l']; n = gd['n']
    rows, cols, data, Pcell = gd['rows'], gd['cols'], gd['data'], gd['Pcell']
    valid = ~np.isnan(Pcell)
    cusp = np.array([1.0/l, 0.0])
    dist = np.linalg.norm(gd['centers']-cusp, axis=1)
    Pfill = np.nan_to_num(Pcell, nan=1e9)
    Pref = float(np.min(Pcell[valid]))   # rescale potential: weights O(1), eigvec invariant
    out = []; dens = {}
    for beta in betas:
        # exp(-beta(P-Pref)); invalid cells (Pfill=1e9) -> weight 0
        wt = np.exp(-beta*(Pfill-Pref))
        W = csr_matrix((data*wt[rows], (rows, cols)), shape=(n, n))
        try:
            ev, evec = eigs(W.T.tocsc(), k=1, which='LM', maxiter=8000, tol=1e-12)
        except Exception as e:
            out.append(dict(beta=float(beta), error=str(e))); continue
        rho_s = float(abs(ev[0]))                    # rescaled leading eigenvalue (O(1))
        log_rho = math.log(rho_s) - beta*Pref if rho_s > 0 else None   # true log rho
        mu = np.abs(np.real(evec[:, 0]))
        if mu.sum() <= 0: out.append(dict(beta=float(beta), error="zero mu")); continue
        mu = mu/mu.sum()
        Pm = float(np.sum(mu[valid]*Pcell[valid]))
        am = float(np.sum(mu*gd['centers'][:,0])); bm = float(np.sum(mu*gd['centers'][:,1]))
        free = (-log_rho/beta) if (beta > 0 and log_rho is not None) else None
        massr = {f"{r}": float(mu[dist < r].sum()) for r in (0.05,0.1,0.15,0.2,0.3,0.5)}
        pk = int(np.argmax(mu))
        rho = math.exp(log_rho) if (log_rho is not None and log_rho > -700) else 0.0
        out.append(dict(beta=float(beta), rho=rho,
                        pressure=log_rho, free_energy=free,
                        P_avg=Pm, a_avg=am, b_avg=bm, mass_within=massr,
                        peak_center=[float(gd['centers'][pk,0]), float(gd['centers'][pk,1])],
                        peak_dist_cusp=float(dist[pk])))
        dens[f"{beta}"] = mu.astype(np.float32)
    meta = dict(q=q, lam=l, inv_lam3=1.0/l**3, N=N, S=S, n_cells=n,
                cusp=[float(cusp[0]), 0.0])
    return meta, out, gd['centers'], dist, np.nan_to_num(Pcell, nan=0.0), dens

if __name__ == "__main__":
    qs = [int(z) for z in sys.argv[1:]] or [5, 6, 7, 12]
    HERE = os.path.dirname(os.path.abspath(__file__))
    summary = {}
    for q in qs:
        meta, res, centers, dist, Pcell, dens = gibbs(q)
        print(f"\n===== q={q}  lam={meta['lam']:.6f}  1/lam^3={meta['inv_lam3']:.6f}  "
              f"cells={meta['n_cells']} =====")
        print("  beta     rho       free=-lnrho/b   <P>_mu    <a>     mass<0.15  peak_d_cusp")
        for r in res:
            if 'error' in r: print(f"   {r['beta']:6.1f}  ERROR {r['error']}"); continue
            fe = f"{r['free_energy']:.5f}" if r['free_energy'] is not None else "  --   "
            print(f"   {r['beta']:6.1f}  {r['rho']:.5f}   {fe}      {r['P_avg']:.5f}  "
                  f"{r['a_avg']:.4f}   {r['mass_within']['0.15']:.4f}    {r['peak_dist_cusp']:.3f}")
        b0 = res[0]
        print(f"   [validate] beta=0: rho={b0['rho']:.5f} (expect 1.0);  <P>_mu0={b0['P_avg']:.4f} (flat avg)")
        last = res[-1]
        print(f"   [zero-temp] free->{last['free_energy']:.4f} (beta_min, Birkhoff) vs 1/lam^3="
              f"{meta['inv_lam3']:.4f};  cusp-mass(<0.15): {b0['mass_within']['0.15']:.4f}"
              f"->{last['mass_within']['0.15']:.4f}")
        summary[q] = dict(meta=meta, results=res)
        np.savez_compressed(os.path.join(HERE, f"Ogoal_transfer_q{q}.npz"),
                            centers=centers, dist=dist, Pcell=Pcell,
                            betas=np.array([float(k) for k in dens]),
                            **{f"mu_{k}": v for k, v in dens.items()})
    with open(os.path.join(HERE, "Ogoal_transfer_summary.json"), "w") as f:
        json.dump(summary, f, indent=2)
    print("\nwrote Ogoal_transfer_summary.json + Ogoal_transfer_q*.npz")
