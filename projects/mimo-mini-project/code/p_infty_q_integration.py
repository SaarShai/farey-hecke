"""A4: Derive p_∞(q) closed form by integrating over (k₁, k₂) BCZ chain configurations.

For each minimal pattern, find the volume in (X₁, X₂) space where:
- 3 consecutive BCZ products are all < t_q
- BCZ constraints satisfied
- 2 is the density factor (BCZ density)

p_∞(q) ≈ Σ_{(k₁,k₂) patterns} ∫∫ 2 dX₁ dX₂ over the valid region for that pattern
"""
import math
from scipy import integrate, optimize

def P_BCZ_XY_less(t):
    """P(XY < t) under BCZ density f = 2 on T = {x+y>1, x,y∈(0,1)}."""
    # Closed-form integration
    if t >= 0.5:
        return 1.0  # All extreme
    if t >= 0.25:
        # General formula
        def integrand(x):
            if x <= 0 or x >= 1: return 0
            y_low = max(0, 1-x)
            y_high = 1 if x <= t else t/x
            return 2*max(0, y_high - y_low)
        return integrate.quad(integrand, 0, 1, limit=200)[0]
    else:
        def integrand(x):
            if x <= 0 or x >= 1: return 0
            y_low = max(0, 1-x)
            y_high = 1 if x <= t else t/x
            return 2*max(0, y_high - y_low)
        return integrate.quad(integrand, 0, 1, limit=200)[0]

def t_at_q(q):
    """Find t such that P_BCZ(XY < t) = 1 - q."""
    target = 1 - q
    result = optimize.brentq(lambda t: P_BCZ_XY_less(t) - target, 0.001, 0.5)
    return result

def vol_pattern_k1_k2(t, k1, k2):
    """Volume (in 2D) of (X₁, X₂) satisfying:
       X₃ = k1·X₂ - X₁ > 0, X₄ = k2·X₃ - X₂ > 0
       X₁+X₂>1, X₂+X₃>1, X₃+X₄>1
       X₁X₂<t, X₂X₃<t, X₃X₄<t.
       Returns ∫∫ 2 dX₁ dX₂ over this region.
    """
    # Grid integration
    N = 500
    h = 1.0/N
    vol = 0.0
    for i in range(N):
        x1 = (i+0.5)*h
        for j in range(N):
            x2 = (j+0.5)*h
            x3 = k1*x2 - x1
            x4 = k2*x3 - x2
            if x3 <= 0 or x4 <= 0 or x3 >= 1 or x4 >= 1: continue
            if x1+x2 <= 1 or x2+x3 <= 1 or x3+x4 <= 1: continue
            if x1*x2 >= t or x2*x3 >= t or x3*x4 >= t: continue
            vol += 2 * h * h  # Density 2
    return vol

# Compute p_∞(q) for various q
print("p_∞(q) via (k1,k2)-pattern integration:")
print("q       t_q       (1,2) vol   (1,4) vol   (4,1) vol   total   empirical p_∞")
empirical = {0.50: 0.184, 0.60: 0.0996, 0.70: 0.0352, 0.78: 0.00802, 0.807: 0.00507, 0.85: 0.00049}
for q in [0.50, 0.60, 0.70, 0.78, 0.807, 0.85, 0.86, 0.861, 0.8618]:
    t = t_at_q(q)
    v12 = vol_pattern_k1_k2(t, 1, 2)
    v14 = vol_pattern_k1_k2(t, 1, 4)
    v41 = vol_pattern_k1_k2(t, 4, 1)
    total = v12 + v14 + v41
    emp = empirical.get(q, "")
    print(f"{q:.4f}  {t:.4f}    {v12:.6f}   {v14:.6f}   {v41:.6f}   {total:.6f}   {emp}")
