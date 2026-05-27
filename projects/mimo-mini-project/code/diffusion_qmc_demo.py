"""C3: Toy diffusion sampling — Farey vs Sobol vs Random noise schedule.

Setup: minimal score-based diffusion on a 1D distribution. Generation
quality depends on noise sampling schedule. Test 3 schedules:
  - Random Gaussian (standard MC)
  - Sobol-mapped Gaussian (quasi-MC)
  - Farey-mapped Gaussian (our method)

Measure: distance between generated samples and target distribution
(Wasserstein-1 or KL divergence) for fixed number of steps.

This is a TOY model — real diffusion is much more complex — but it
demonstrates whether Farey-based noise gives advantage in diffusion sampling.
"""
import numpy as np
from scipy import stats
import math

def farey_1d(N):
    a, b, c, d = 0, 1, 1, N
    yield a/b
    while c <= N:
        k = (N + b) // d
        a, b, c, d = c, d, k*c - a, k*d - b
        yield a/b

def vdc(n, base=2):
    result = np.zeros(n)
    for i in range(1, n+1):
        f, r, x = 1.0, 0.0, i
        while x > 0:
            f /= base; r += f * (x % base); x //= base
        result[i-1] = r
    return result

def normal_from_uniform(u_array):
    """Map uniform [0,1] samples to standard normal via inverse CDF."""
    # Clip to avoid -inf
    u = np.clip(u_array, 1e-9, 1 - 1e-9)
    return stats.norm.ppf(u)

def get_farey_uniform(n_target):
    """Get n_target uniform samples from Farey sequence."""
    N = 1
    while True:
        farey = list(farey_1d(N))
        if len(farey) >= n_target: break
        N += 1
    return np.array(farey[:n_target])

def get_sobol_uniform(n):
    return vdc(n, 2)

# Target distribution: mixture of 3 Gaussians
np.random.seed(42)
def target_density(x):
    return (1/3)*(stats.norm.pdf(x, -3, 0.5) + stats.norm.pdf(x, 0, 1) + stats.norm.pdf(x, 4, 0.3))

# Sample exact target via inverse CDF approximation (50k samples)
exact_samples = np.concatenate([
    np.random.normal(-3, 0.5, 16667),
    np.random.normal(0, 1, 16667),
    np.random.normal(4, 0.3, 16666),
])

def diffusion_sample(noise_samples_uniform, n_steps=50, sigma_max=10.0, sigma_min=0.01):
    """Toy 1D diffusion sampler.
    
    Initialize x0 ~ N(0, sigma_max²).
    At each step, denoise toward target using a learned score function (here: analytic).
    The noise injection uses noise_samples_uniform (mapped to Normal via Phi^{-1}).
    """
    n_samples = len(noise_samples_uniform) // n_steps
    if n_samples < 1: return np.array([])
    # Reshape noise: each sample uses n_steps noise vectors
    noise = normal_from_uniform(noise_samples_uniform[:n_samples * n_steps]).reshape(n_samples, n_steps)
    
    # Sigma schedule: log-linear from sigma_max to sigma_min
    sigmas = np.exp(np.linspace(np.log(sigma_max), np.log(sigma_min), n_steps + 1))
    
    # Initialize x at sigma_max
    x = noise[:, 0] * sigma_max
    
    # Iterative denoising using analytic score
    for t in range(n_steps):
        sigma = sigmas[t]
        # Tweedie-like score for our mixture target with added noise sigma
        # ∇log p(x | sigma) ≈ E[(x_clean - x) / sigma²]
        # We approximate using single-step Tweedie under "smoothed target"
        
        # Score (gradient of log density) at smoothed target
        components = [(-3, 0.5), (0, 1), (4, 0.3)]
        weights = np.zeros((len(x), 3))
        for i, (mu, s) in enumerate(components):
            weights[:, i] = (1/3) * stats.norm.pdf(x, mu, np.sqrt(s**2 + sigma**2))
        weights = weights / weights.sum(axis=1, keepdims=True)
        
        score = np.zeros_like(x)
        for i, (mu, s) in enumerate(components):
            score += weights[:, i] * (mu - x) / (s**2 + sigma**2)
        
        # Euler-Maruyama step (with noise injection)
        dt = np.log(sigmas[t]/sigmas[t+1])
        x = x + dt * (sigma**2) * score + sigma * math.sqrt(2*dt) * (noise[:, min(t+1, n_steps-1)])
    
    return x

# Compare 3 noise schedules
n_target_samples = 2000
n_steps = 30
print(f"\nDiffusion sampling demo: {n_target_samples} samples, {n_steps} steps")
print("Target: 3-Gaussian mixture\n")

# Generate noise via 3 methods
n_uniform_needed = n_target_samples * n_steps

# Random MC
np.random.seed(0)
random_u = np.random.random(n_uniform_needed)

# Sobol (van der Corput)
sobol_u = get_sobol_uniform(n_uniform_needed)

# Farey
farey_u = get_farey_uniform(n_uniform_needed)

# Run diffusion
sample_random = diffusion_sample(random_u, n_steps=n_steps)
sample_sobol = diffusion_sample(sobol_u, n_steps=n_steps)
sample_farey = diffusion_sample(farey_u, n_steps=n_steps)

# Compare via Wasserstein-1 distance to exact target
from scipy.stats import wasserstein_distance
w_random = wasserstein_distance(sample_random, exact_samples)
w_sobol = wasserstein_distance(sample_sobol, exact_samples)
w_farey = wasserstein_distance(sample_farey, exact_samples)

print(f"Wasserstein-1 distance to target:")
print(f"  Random MC:     {w_random:.4f}")
print(f"  Sobol QMC:     {w_sobol:.4f}  (ratio to Random: {w_sobol/w_random:.3f})")
print(f"  Farey QMC:     {w_farey:.4f}  (ratio to Random: {w_farey/w_random:.3f})")
print(f"\n  Farey/Sobol ratio: {w_farey/w_sobol:.3f}")
print(f"\nLower = better. If Farey/Sobol < 1: Farey wins.")

# Also check higher moments
for name, sample in [("Random", sample_random), ("Sobol", sample_sobol), ("Farey", sample_farey)]:
    print(f"\n{name} sample stats: mean={sample.mean():.3f}, std={sample.std():.3f}, skew={stats.skew(sample):.3f}")
