"""C₁ distribution shape analysis — histogram + fit to known distributions."""
import mpmath as mp, json, statistics, math
from pathlib import Path
mp.mp.dps = 25

DATA_DIR = Path.home() / "farey_py_tasks" / "data"
with open(DATA_DIR / "C1_500_distribution.json") as f: data = json.load(f)

def analyze_dist(label, vals):
    cs = [c for _, c, _ in vals]
    N = len(cs)
    m = statistics.mean(cs)
    s = statistics.stdev(cs)
    m2 = statistics.mean(c*c for c in cs)
    m3 = statistics.mean(c**3 for c in cs)
    m4 = statistics.mean(c**4 for c in cs)
    skew = (m3 - 3*m*m2 + 2*m**3) / s**3
    kurt = (m4 - 4*m3*m + 6*m2*m*m - 3*m**4) / s**4 - 3
    print(f"\n{label} N={N}:")
    print(f"  Mean   = {m:.4f}")
    print(f"  Std    = {s:.4f}")
    print(f"  E[C²]  = {m2:.4f}")
    print(f"  Skew   = {skew:.4f}")
    print(f"  Kurt   = {kurt:.4f}  (Normal=0, Exponential=6, χ²_k = 12/k)")
    # Histogram
    bins = [0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.5, 3.0, 4.0, 6.0]
    counts = [sum(1 for c in cs if bins[i] <= c < bins[i+1]) for i in range(len(bins)-1)]
    print(f"  Hist [0-0.2, 0.2-0.4, ..., 4-6]:")
    for i, c in enumerate(counts):
        bar = "█" * int(c * 40 / max(counts))
        print(f"    [{bins[i]:.1f}, {bins[i+1]:.1f}): {c:>4} {bar}")

    # Check for distributions
    # Gaussian prediction: kurt=0
    # Half-normal (|Gaussian|): mean = σ√(2/π), variance = σ²(1-2/π)
    # Rayleigh: E[X] = σ√(π/2), E[X²] = 2σ², σ = √(m2/2)
    sigma_ray = math.sqrt(m2/2)
    print(f"  If Rayleigh, σ_Ray = {sigma_ray:.4f}, expected mean = σ√(π/2) = {sigma_ray*math.sqrt(math.pi/2):.4f} (observed {m:.4f})")
    # χ-distribution with k dof: E[X²] = k, E[X] = √2·Γ((k+1)/2)/Γ(k/2)
    # If E[X²]=k, observed k = m2
    k_est = m2
    expected_mean_chi = math.sqrt(2) * math.gamma((k_est+1)/2) / math.gamma(k_est/2)
    print(f"  If χ-dist with k={k_est:.2f}, expected mean = {expected_mean_chi:.4f} (observed {m:.4f})")

    return m, m2

analyze_dist("37a1", data["37a1"])
analyze_dist("Δ", data["delta"])

print("\nDONE")
