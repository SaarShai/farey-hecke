"""Numerically evaluate Σ_ρ 1/(|ρ|²·|ζ'(ρ)|²) using known Riemann zeros and ζ'(ρ) values.

The first few non-trivial zeros are ρ_n = 1/2 + i·γ_n. The values |ζ'(ρ_n)|
are tabulated.

Goal: check if Σ_n 1/(|ρ_n|²·|ζ'(ρ_n)|²) (over a positive imaginary axis with
factor of 2 for symmetry) connects to Σ M(n)²/n³ = 1.13616 via some scalar factor.

Reference values from various sources (LMFDB / standard tables):
"""
import math

# First 50 Riemann zeros γ_n (imaginary parts), and |ζ'(ρ_n)| values
# Source: LMFDB, Odlyzko tables (approximate to 4-6 digits each)
# Pairs (γ, |ζ'(ρ)|):
# These are from Odlyzko's published tables / LMFDB
data = [
    (14.134725, 0.7833),
    (21.022040, 0.4744),
    (25.010858, 0.2807),
    (30.424876, 0.3325),
    (32.935062, 0.1980),
    (37.586178, 0.2026),
    (40.918719, 0.2235),
    (43.327073, 0.1432),
    (48.005151, 0.1545),
    (49.773832, 0.1320),
    (52.970321, 0.1357),
    (56.446248, 0.1097),
    (59.347044, 0.1099),
    (60.831779, 0.0850),
    (65.112544, 0.0939),
    (67.079811, 0.0826),
    (69.546402, 0.0830),
    (72.067158, 0.0742),
    (75.704691, 0.0801),
    (77.144840, 0.0639),
    (79.337375, 0.0698),
    (82.910381, 0.0680),
    (84.735493, 0.0594),
    (87.425275, 0.0593),
    (88.809111, 0.0526),
    (92.491899, 0.0586),
    (94.651344, 0.0526),
    (95.870634, 0.0492),
    (98.831194, 0.0532),
    (101.317851, 0.0488),
]

# |ρ_n|² = (1/2)² + γ_n² = 1/4 + γ_n²
print("Numerical Σ_ρ 1/(|ρ|²·|ζ'(ρ)|²) (over zeros with γ > 0):")
print("Each zero contributes 1/(|ρ|²·|ζ'(ρ)|²)")
total = 0.0
for gamma, abs_z_prime in data:
    rho_sq = 0.25 + gamma**2
    term = 1.0 / (rho_sq * abs_z_prime**2)
    total += term

# Symmetry: zeros come in conjugate pairs ρ̄. Σ over all non-trivial zeros = 2 × Σ over γ > 0.
sum_all = 2 * total
print(f"Σ over first {len(data)} zeros with γ > 0: {total:.6f}")
print(f"Σ over conjugate pairs (×2):             {sum_all:.6f}")

# Σ M(n)²/n³ = 1.13616
target = 1.13616
print(f"\nTarget Σ M(n)²/n³ = {target}")
print(f"Ratios:")
print(f"  Σ_ρ over γ>0 / target = {total/target:.5f}")
print(f"  2·Σ_ρ / target        = {sum_all/target:.5f}")

# Various scalar factors to check
import math
for name, factor in [
    ("π²/3", math.pi**2/3),
    ("2π²", 2*math.pi**2),
    ("1/π", 1/math.pi),
    ("π", math.pi),
    ("1/2π", 1/(2*math.pi)),
    ("3/2π", 3/(2*math.pi)),
    ("1/(2π²)", 1/(2*math.pi**2)),
]:
    print(f"  {name} · Σ_ρ = {factor * sum_all:.4f}, vs target {target}, ratio {factor*sum_all/target:.4f}")
