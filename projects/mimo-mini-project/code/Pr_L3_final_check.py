"""Final high-stats check: Pr(L>=3) / eps^2 -> 324/143 = 2.2657..."""
import math
import time
import numpy as np
from numba import njit

T_STAR = 2.0 / 9.0
THEORY = 324.0 / 143.0


@njit
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


@njit
def count(x0, y0, N, t):
    x, y = x0, y0
    consec = 0
    n_3win = 0
    for _ in range(N):
        if x * y < t:
            consec += 1
            if consec >= 3:
                n_3win += 1
        else:
            consec = 0
        k = math.floor((1.0 + x) / y)
        x, y = y, k * y - x
    return n_3win


def main():
    x0, y0 = burn_in(10_000, 42)
    _ = count(x0, y0, 1000, T_STAR + 0.1)
    print(f"  Theory: 324/143 = {THEORY:.8f}")
    print()

    for eps in [1e-3, 3e-4, 1e-4]:
        t = T_STAR + eps
        ratios = []
        for sd in range(4):
            x0, y0 = burn_in(50_000, 42 + sd * 99971 + int(eps * 1e7))
            N = 1_000_000_000
            t0 = time.time()
            n = count(x0, y0, N, t)
            el = time.time() - t0
            ratio = n / N / eps**2
            ratios.append(ratio)
            print(f"  eps={eps:.0e}, seed{sd}: n_3win={n:,}, ratio={ratio:.4f}  ({el:.0f}s)")
        arr = np.array(ratios)
        print(f"    eps={eps:.0e} AVG = {arr.mean():.4f}  std_err = {arr.std()/2:.4f}")
        print(f"    deviation from theory: {arr.mean() - THEORY:+.4f}")
        print()


if __name__ == "__main__":
    main()
