#!/usr/bin/env python3
"""
Run the cluster=2 diagnostic on Sym^2 Delta (degree-3, conductor 1, symplectic).

This closes the one arithmetic test that lmfdb_cluster_diagnostic.py had to skip:
PARI's `lfunsympow` is unimplemented, so the degree-3 Sym^2 Delta L-function was
never built there.  We build it by hand from the arithmetic Euler factor
    1 - b1 X + p^11 b1 X^2 - p^33 X^3 ,   b1 = tau(p)^2 - p^11 ,
verified against PARI's functional equation (lfuncheckfeq exponent = -111, i.e.
machine precision) with analytic gamma vector Vga=[1,11,12], k=1, conductor 1.

Zeros are precomputed in data/zeros/sym2_delta_T2500.txt (analytic norm, Re=1/2).
We reuse the *byte-identical* unfold_zeros + cluster_stats from the main module so
the comparison against the six previously-tested L-functions is apples-to-apples.

Prediction (from the local/symmetry-insensitive nature of the diagnostic): GUE
class -- size-2 fraction ~0%, size>=3 clusters present, max cluster size >> 2.
A degree-3 arithmetic L-function is NOT in the BCZ/mediant class.
"""
import os
import numpy as np

from lmfdb_cluster_diagnostic import unfold_zeros, cluster_stats

HERE = os.path.dirname(os.path.abspath(__file__))
ZEROS = os.path.join(HERE, "..", "data", "zeros", "sym2_delta_T2500.txt")


def main():
    gammas = np.loadtxt(ZEROS)
    gammas = np.sort(gammas[np.isfinite(gammas)])
    q_list = [0.95, 0.99, 0.999]
    gaps = unfold_zeros(gammas, deg=3, conductor=1)
    gaps = gaps / gaps.mean()
    st = cluster_stats(gaps, q_list)

    print("=" * 78)
    print(" Sym^2 Delta  (degree 3, conductor 1, symplectic)  -- cluster=2 diagnostic")
    print("=" * 78)
    print(f"  #zeros={len(gammas)}  #gaps={len(gaps)}  "
          f"height=[{gammas.min():.2f},{gammas.max():.2f}]  "
          f"mean=1.000  std={gaps.std():.4f}")
    print(f"{'q':>8} | {'thr':>7} | {'n_extr':>7} | {'n_clu':>7} | "
          f"{'size2%':>7} | {'p>=3':>8} | {'maxsz':>5} | hist(1..8)")
    for q in q_list:
        s = st[q]
        h = ", ".join(f"{k}:{s['hist'][k]}" for k in sorted(s['hist'])[:8])
        print(f"{q:8.4f} | {s['threshold']:7.4f} | {s['n_extreme']:7d} | "
              f"{s['n_clusters']:7d} | {100*s['size2_frac']:7.3f} | "
              f"{s['p_size_ge_3']:8.5f} | {s['max_size']:5d} | {h}")
    s99 = st[0.99]
    cls = ("BCZ/mediant" if s99['size2_frac'] > 0.5 and s99['max_size'] <= 2
           else "GUE/RMT (size>=3 present, not BCZ class)")
    print("-" * 78)
    print(f"  VERDICT @ q=0.99: size2={100*s99['size2_frac']:.2f}%  "
          f"max_size={s99['max_size']}  ->  {cls}")
    print("=" * 78)


if __name__ == "__main__":
    main()
