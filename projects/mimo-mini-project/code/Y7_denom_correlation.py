"""Y7: Verify Corr(b_i/N, b_{i+1}/N) = -1/2 directly on Farey.

X14 + MC said BCZ density gives Corr(X, Y) = -1/2 for normalized denominators.
This is the ONLY "1/2" surviving from BCZ. Verify it on actual Farey sequence.
"""
import math, time

def stream_denoms(N):
    """Yield consecutive (b_i, b_{i+1}) pairs in F_N."""
    a, b, c, d = 0, 1, 1, N
    prev_b = b
    while c <= N:
        k = (N + b) // d
        a, b, c, d = c, d, k*c - a, k*d - b
        yield (prev_b, b)
        prev_b = b

def corr_denoms(N):
    """Pearson correlation of (b_i/N, b_{i+1}/N) over consecutive Farey fractions."""
    n = 0
    sx = sy = sxy = sx2 = sy2 = 0.0
    for bi, bj in stream_denoms(N):
        xi = bi / N
        yi = bj / N
        n += 1
        sx += xi
        sy += yi
        sxy += xi * yi
        sx2 += xi * xi
        sy2 += yi * yi
    mean_x = sx / n
    mean_y = sy / n
    var_x = sx2/n - mean_x*mean_x
    var_y = sy2/n - mean_y*mean_y
    cov = sxy/n - mean_x*mean_y
    return cov / math.sqrt(var_x * var_y), n, mean_x, var_x

if __name__ == "__main__":
    for N in [1000, 3000, 10000, 30000]:
        t0 = time.time()
        rho, n_pairs, mx, vx = corr_denoms(N)
        wall = time.time() - t0
        print(f"N={N:>5} |pairs|={n_pairs:>11}  Corr(b_i/N, b_{{i+1}}/N) = {rho:.4f} "
              f"(expected -1/2)  E[X]={mx:.4f} (exp 2/3)  Var(X)={vx:.4f} (exp 1/18≈0.0556)  wall={wall:.1f}s", flush=True)
