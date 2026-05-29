"""Complete linearization for BOTH corners with ALL branches.

CORNER 1: near (1/3, 2/3).  k_0 ∈ {1, 2}.

CASE (k_0 = 1):
  T(x, y) = (y, y - x) = (2/3 + v, 1/3 + v - u)
  Pair 0 extreme: 2u + v < 3 eps
  k_0 = 1 condition: f0 = (1+x)/y < 2  <=>  (1+x) < 2y  <=>  4/3+u < 4/3+2v  <=>  u < 2v.
  Image is near (2/3, 1/3).  Let u' = X_1 - 2/3 = v, v' = X_2 - 1/3 = v - u.
  P1 = X_1 * X_2 = (2/3 + v)(1/3 + v - u) = 2/9 + (v - u)/3 + v/3 + ...
                  Wait let me redo:
  P1 = (2/3 + v)(1/3 + v - u) = (2/3)(1/3) + (2/3)(v - u) + v(1/3) + v(v - u)
     = 2/9 + (2v - 2u)/3 + v/3 + ...
     = 2/9 + (3v - 2u)/3 + ...
  P1 < 2/9 + eps <=> 3v - 2u < 3 eps  ✓

  Then at (X_1, X_2) = (2/3 + v, 1/3 + v - u), with u' = v, v' = v - u:
  f1 = (1 + X_1)/X_2 = (5/3 + v)/(1/3 + v - u) at (u',v')=(v, v-u).
  f1 at (0,0) = 5.  Linearization: f1 ≈ 5 + 3 u' - 15 v' = 5 + 3v - 15(v-u) = 5 + 15u - 12v.
  k_1 = 5  iff  f1 in [5, 6) iff 15u - 12v in [0, 1) — generically iff 15u >= 12v iff 5u >= 4v.
  k_1 = 4  iff  f1 < 5  iff  5u < 4v.
  But we're already in the k_0 = 1 branch, requiring u < 2v.  Combined: u < 2v AND 5u < 4v means u < 4v/5 (tighter).  So k_1 = 4 is the branch u < 4v/5.  k_1 = 5 is u in (4v/5, 2v).

  SUB-CASE (k_0=1, k_1=4):
    X_3 = 4 X_2 - X_1 = 4(1/3 + v - u) - (2/3 + v) = 2/3 + 3v - 4u.  Image near (1/3, 2/3).
    P2 = X_2 * X_3 = (1/3 + v - u)(2/3 + 3v - 4u)
       = 2/9 + (1/3)(3v - 4u) + (2/3)(v - u) + (v - u)(3v - 4u)
       = 2/9 + (3v - 4u)/3 + 2(v - u)/3 + ...
       = 2/9 + (3v - 4u + 2v - 2u)/3
       = 2/9 + (5v - 6u)/3
    P2 < 2/9 + eps  iff  5v - 6u < 3 eps.

  SUB-CASE (k_0=1, k_1=5):
    X_3 = 5 X_2 - X_1 = 5(1/3 + v - u) - (2/3 + v) = 1 + 4v - 5u.
    P2 = X_2 * X_3 = (1/3 + v - u)(1 + 4v - 5u)
       = 1/3 + (4v - 5u)/3 + (v - u) + ...
       = 1/3 + (4v - 5u + 3v - 3u)/3
       = 1/3 + (7v - 8u)/3
    P2 ≈ 1/3 > 2/9 (always).  NOT in R_eps.

CASE (k_0 = 2):
  T(x, y) = (y, 2y - x) = (2/3 + v, 2(2/3+v) - (1/3+u)) = (2/3 + v, 1 + 2v - u).
  X_2 = 1 + 2v - u.  Need X_2 < 1, so u > 2v (k_0 = 2 condition).
  Triangle X_1 + X_2 = 2/3+v + 1 + 2v - u = 5/3 + 3v - u > 1: automatic.
  P1 = X_1 * X_2 = (2/3 + v)(1 + 2v - u) = 2/3 + (4v - 2u)/3 + v + ...
                 = 2/3 + (4v - 2u + 3v)/3 = 2/3 + (7v - 2u)/3
  P1 ≈ 2/3 > 2/9 (always).  NOT in R_eps.

So near (1/3, 2/3), the only contributing branch is (k_0=1, k_1=4):
  TRIANGLE:  u + v > 0
  PAIR 0:    2u + v < 3 eps
  K_0=1:     u < 2v
  PAIR 1:    3v - 2u < 3 eps
  K_1=4:     5u < 4v
  PAIR 2:    5v - 6u < 3 eps

CORNER 2: near (2/3, 1/3).  By time-reversal symmetry — let's redo to be sure.

CASE (k_0 = 4) -> (k_1 = 1):  (computed previously)
  TRIANGLE:  u + v > 0  (u = X_0 - 2/3, v = X_1 - 1/3)
  PAIR 0:    u + 2v < 3 eps
  K_0=4:     u < 5v
  PAIR 1:    6v - u < 3 eps
  K_1=1:     2u < 7v
  PAIR 2:    10v - 3u < 3 eps

CASE (k_0 = 5):  X_2 = 5 X_1 - X_0 = 5(1/3 + v) - (2/3 + u) = 1 + 5v - u.
  P1 = (1/3 + v)(1 + 5v - u) ≈ 1/3, not extreme.

CASE (k_0 = 4, k_1 = 2):  X_3 = 2 X_2 - X_1 = 2(2/3 + 4v - u) - (1/3 + v) = 1 + 7v - 2u.
  P2 = (2/3 + 4v - u)(1 + 7v - 2u) ≈ 2/3, not extreme.

So near (2/3, 1/3), only contributing branch is (k_0=4, k_1=1).

TOTAL prefactor: 2 * 81/143 = 162/143 ≈ 1.133 (volume in T).
Pr(invariant) = 2 * vol(R) / 1 = 324/143 ≈ 2.266.

But chain MC shows Pr(L>=3 entries) / eps^2 ≈ 0.75, factor 3 smaller!

NEW HYPOTHESIS:
The chain Pr(entry at index i) counts ONE entry per cluster.  In invariant time,
the BCZ chain "visits" the entry region with rate (invariant measure of region).
But the entry happens at the START of a cluster; the chain then spends 3+ steps
in the cluster, during which it visits the MIDDLE and END regions (which are
also in R_eps for OTHER definitions).  Maybe I need:
  Pr(entry) = vol(set of pairs (X_0, X_1) starting a size-3 cluster)
            = vol(set with X_0*X_1 < t AND X_{-1}*X_0 >= t AND next 2 pairs extreme)
The "X_{-1}*X_0 >= t" excludes pairs that ARE in the middle of a longer extreme run.

Without this exclusion, vol_R = "pair starts size 3+ run from any position" —
which double-counts the middle of size-4+ clusters.  In the rare event of size-4,
both (X_0,X_1) and (X_1,X_2) are "start of 3-run" — counted twice.

But our region was just "X_0*X_1, X_1*X_2, X_2*X_3 all < t" — without requiring
X_{-1}*X_0 >= t.  Under invariant measure, this counts:
  Pr(size-3+ run starts at or before pair X_0).
  = Sum over k of Pr(pair X_0 is in a cluster of size >= 3 at position >= 0).
  ≈ E[L | L>=3] * Pr(cluster of size >= 3 starts somewhere within last L pairs of X_0).
For our region (entries to a 3-pair extreme window): the count is "pair is start
of a 3-pair extreme window" — which is the same as the running count of
"3 consecutive extreme pairs starting here".  This counts each size-K cluster
(K-2) times if K >= 3 (for K=3: 1, for K=4: 2, ... in general K-2 times).
E[K - 2 | K >= 3] = E[K | K >= 3] - 2 ≈ 5 - 2 = 3.

Hmm.  Let me re-think.  Let n_pair = total pairs.  Let n_3win = number of 3-pair
windows (X_i, X_{i+1}, X_{i+2}, X_{i+3}) with all products < t.  For a single
cluster of size K, the number of such 3-windows is max(0, K - 2).
For K >= 3, this is K - 2.  So:
  n_3win = sum over clusters of (K-2) * (1 if K >= 3 else 0)
         = (sum over size-3+ clusters of K) - 2 * (number of size-3+ clusters)
         = n_3p_pairs - 2 * n_3p_clusters.

And Pr_inv(R_eps from theory) = lim_N (n_3win / N).

From empirical at eps = 1e-2:  n_extr = 31M, n_3p clusters = (Pr(L>=3 cluster) * n_clusters).
At eps = 1e-2, our chain showed n_entries (clusters of size >= 3) = 14,907 and
n_size3p (pairs in size-3+ clusters) = 74,124 out of N = 200M = > Pr_size3p = 3.7e-4.
n_3win = 74,124 - 2*14,907 = 44,310.
Pr_3win = 44,310 / 200M = 2.22e-4 = 2.22 * eps^2 = 2.22e-4 / 1e-4 = 2.22.

So Pr_inv(R_eps) = 2.22 * eps^2 — MATCHES the theory 2.27 * eps^2!

So the prefactor 324/143 = 2.2657 IS the right one, and Pr_inv(R_eps) is the
density of "3-window extreme" events, which equals (n_3p_pairs - 2 * n_3p_clusters) / N.

Let me verify this systematically.
"""
import math
import time
import numpy as np
from numba import njit


@njit(cache=True)
def bcz_step(x, y):
    k = math.floor((1.0 + x) / y)
    return y, k * y - x


@njit(cache=True)
def burn_in(N_burn, seed):
    np.random.seed(seed)
    while True:
        x = np.random.random()
        y = np.random.random()
        if x + y > 1.0:
            break
    for _ in range(N_burn):
        k = math.floor((1.0 + x) / y)
        x, y = y, k * y - x
    return x, y


@njit(cache=True)
def count_3windows(x0, y0, N_steps, t):
    """Count 3-pair extreme windows (X_i, X_{i+1}, X_{i+2}, X_{i+3}) with
    all three products < t.  Each such window contributes once.
    """
    x, y = x0, y0
    # Maintain a sliding "consecutive extreme count" — number of consecutive
    # extreme pairs ending at current index.
    consec = 0
    n_3win = 0
    n_3p_clusters = 0
    n_3p_pairs = 0
    current_run = 0
    for _ in range(N_steps):
        if x * y < t:
            current_run += 1
            consec += 1
            if consec >= 3:
                # The window ending here (positions i-2, i-1, i) is fully extreme.
                n_3win += 1
        else:
            if current_run >= 3:
                n_3p_clusters += 1
                n_3p_pairs += current_run
            current_run = 0
            consec = 0
        k = math.floor((1.0 + x) / y)
        x, y = y, k * y - x
    if current_run >= 3:
        n_3p_clusters += 1
        n_3p_pairs += current_run
    return n_3win, n_3p_clusters, n_3p_pairs


T_STAR = 2.0 / 9.0
PREDICT = 324.0 / 143.0  # 2.2657...


def main():
    print(f"  Theory: Pr_inv(R_eps) = 324/143 = {PREDICT:.6f}")
    print(f"  Pr_inv(R_eps) counts 3-pair extreme windows = (size-K-cluster -> K-2 windows)")
    print()
    eps_list = [1e-1, 3e-2, 1e-2, 3e-3, 1e-3]
    N = 500_000_000

    # warmup numba
    x0, y0 = burn_in(10_000, 42)
    _ = count_3windows(x0, y0, 10_000, T_STAR + 0.1)

    print(f"  Chain MC: N = {N:,} per eps")
    print(f"{'eps':>8s}  {'n_3win':>12s}  {'n_3p_clust':>12s}  {'n_3p_pair':>12s}  "
          f"{'n_3win/eps^2':>14s}  {'check':>14s}")
    for eps in eps_list:
        t = T_STAR + eps
        x0, y0 = burn_in(50_000, 42 + int(eps * 1e7))
        t0 = time.time()
        n_3win, n_3pc, n_3pp = count_3windows(x0, y0, N, t)
        el = time.time() - t0
        pr_3win = n_3win / N
        ratio = pr_3win / (eps ** 2)
        # cross-check: n_3win should equal n_3p_pair - 2 * n_3p_clust
        check = n_3pp - 2 * n_3pc
        ratio_check = (check / N) / (eps ** 2)
        print(f"{eps:8.0e}  {n_3win:12,}  {n_3pc:12,}  {n_3pp:12,}  "
              f"{ratio:14.4f}  {ratio_check:14.4f}  ({el:.0f}s)")


if __name__ == "__main__":
    main()
