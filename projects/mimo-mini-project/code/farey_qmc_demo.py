"""Q4: Farey-based QMC vs Sobol vs Halton comparison.

We use the cluster=2 result: extreme gaps in F_N come in pairs. For QMC,
this means: when adaptively refining, refine PAIRS not singletons.

Build a simple QMC integrator using Farey points. Compare to scipy.stats.qmc
Sobol and Halton sequences on a test integral.
"""
import numpy as np
import math
import time

def farey_1d(N):
    """Generate the Farey sequence F_N as floats in [0, 1]."""
    a, b, c, d = 0, 1, 1, N
    yield a/b
    while c <= N:
        k = (N + b) // d
        a, b, c, d = c, d, k*c - a, k*d - b
        yield a/b

def halton_1d(n_points, base=2):
    """Halton sequence in 1D, base b."""
    result = np.zeros(n_points)
    for i in range(1, n_points + 1):
        f = 1.0
        r = 0.0
        x = i
        while x > 0:
            f = f / base
            r = r + f * (x % base)
            x = x // base
        result[i-1] = r
    return result

def sobol_1d(n_points):
    """Sobol sequence in 1D (van der Corput base 2 = Sobol 1D)."""
    return halton_1d(n_points, base=2)

# Test integrals: discontinuous, smooth, and oscillatory
def f_smooth(x):
    return np.exp(-x*x) * np.sin(5*x) + 0.5*np.cos(10*x)
EXACT_SMOOTH = 0.20687891175  # numerical truth

def f_step(x):
    return np.where(x < 0.3, 1.0, np.where(x < 0.7, 0.5, 0.2))
EXACT_STEP = 0.3*1.0 + (0.7-0.3)*0.5 + (1-0.7)*0.2  # = 0.3 + 0.2 + 0.06 = 0.56

def f_oscillatory(x):
    return np.sin(50*np.pi*x)**2  # mean = 1/2 over [0,1]
EXACT_OSC = 0.5

# QMC error: integral approximation = (1/N) Σ f(x_i)
def qmc_error(points, f, exact):
    return abs(np.mean(f(points)) - exact)

print("Q4: Farey-QMC vs Sobol/Halton on 1D integrals")
print("="*70)
for f_name, f, exact in [
    ("Smooth (exp+sin+cos)", f_smooth, EXACT_SMOOTH),
    ("Step function", f_step, EXACT_STEP),
    ("Oscillatory (sin² 50πx)", f_oscillatory, EXACT_OSC),
]:
    print(f"\n--- {f_name} (exact = {exact:.6f}) ---")
    print(f"{'N_target':>10} {'Farey err':>12} {'Sobol err':>12} {'Halton err':>12} {'Farey/Sobol':>12}")
    for N_target in [100, 500, 2000, 10000]:
        # Farey: collect points and use them
        farey_points = list(farey_1d(int(math.sqrt(N_target * math.pi**2 / 3))))
        farey_n = len(farey_points)
        sobol_points = sobol_1d(farey_n)
        halton_points = halton_1d(farey_n, base=2)  # actually van der Corput
        halton3_points = halton_1d(farey_n, base=3)
        
        e_farey = qmc_error(np.array(farey_points), f, exact)
        e_sobol = qmc_error(sobol_points, f, exact)
        e_halton = qmc_error(halton3_points, f, exact)
        
        ratio = e_farey / e_sobol if e_sobol > 0 else float('inf')
        print(f"  N={farey_n:>5}: {e_farey:.4e}  {e_sobol:.4e}  {e_halton:.4e}  {ratio:>5.3f}")

# Compare also against pseudo-random MC
print("\n--- Smooth function: pseudo-random MC for comparison ---")
np.random.seed(42)
for n in [100, 1000, 10000]:
    errors = [qmc_error(np.random.random(n), f_smooth, EXACT_SMOOTH) for _ in range(50)]
    print(f"  N={n}: MC error mean = {np.mean(errors):.4e}, std = {np.std(errors):.4e}")
