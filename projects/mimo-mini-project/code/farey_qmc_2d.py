"""C1: Multi-dimensional Farey-QMC benchmark.

Build 2D and 3D Farey-product sequences. Compare against Sobol/Halton
on multi-dim test integrals. The 2D Farey product: take F_N × F_N (Cartesian).
"""
import numpy as np
import math

def farey_1d(N):
    """Generate F_N as ascending floats in [0,1]."""
    a, b, c, d = 0, 1, 1, N
    yield a/b
    while c <= N:
        k = (N + b) // d
        a, b, c, d = c, d, k*c - a, k*d - b
        yield a/b

def vdc_base(n, base):
    """van der Corput sequence in given base."""
    result = np.zeros(n)
    for i in range(1, n+1):
        f, r, x = 1.0, 0.0, i
        while x > 0:
            f /= base
            r += f * (x % base)
            x //= base
        result[i-1] = r
    return result

def halton_2d(n):
    """Halton 2D: base 2 × base 3."""
    return np.column_stack([vdc_base(n, 2), vdc_base(n, 3)])

def halton_3d(n):
    return np.column_stack([vdc_base(n, 2), vdc_base(n, 3), vdc_base(n, 5)])

def farey_2d(target_n):
    """2D Farey product. Take F_N x F_N where N is chosen so |F_N|² ≈ target_n."""
    N = int(math.sqrt(target_n * math.pi**2 / 3)**0.5 * math.sqrt(math.pi**2/3))  # rough
    # Just compute |F_N| empirically
    N = 1
    while True:
        f_count = sum(1 for _ in farey_1d(N))
        if f_count*f_count >= target_n: break
        N += 1
    farey = list(farey_1d(N))
    points = []
    for x in farey:
        for y in farey:
            points.append((x, y))
            if len(points) >= target_n: break
        if len(points) >= target_n: break
    return np.array(points[:target_n])

def farey_3d(target_n):
    N = 1
    while True:
        f_count = sum(1 for _ in farey_1d(N))
        if f_count**3 >= target_n: break
        N += 1
    farey = list(farey_1d(N))
    points = []
    for x in farey:
        for y in farey:
            for z in farey:
                points.append((x, y, z))
                if len(points) >= target_n: break
            if len(points) >= target_n: break
        if len(points) >= target_n: break
    return np.array(points[:target_n])

# 2D test integrals
def f_2d_smooth(p):  # ∫∫ exp(-x²-y²) dx dy from 0 to 1
    x, y = p[:,0], p[:,1]
    return np.exp(-x**2 - y**2)
EXACT_2D_SMOOTH = ((math.erf(1) * math.sqrt(math.pi) / 2))**2  # ≈ 0.5577

def f_2d_oscillatory(p):
    x, y = p[:,0], p[:,1]
    return np.sin(2*np.pi*x) * np.cos(2*np.pi*y) + 0.5
EXACT_2D_OSC = 0.5  # mean of sin·cos over [0,1]² = 0

def f_3d_smooth(p):
    return np.exp(-p[:,0]**2 - p[:,1]**2 - p[:,2]**2)
EXACT_3D = (math.erf(1) * math.sqrt(math.pi) / 2)**3

def err(points, f, exact):
    return abs(np.mean(f(points)) - exact)

print("="*70)
print("C1: 2D and 3D Farey-QMC vs Sobol/Halton")
print("="*70)

print("\n--- 2D Smooth: ∫∫ exp(-x²-y²) (exact ≈ {:.5f}) ---".format(EXACT_2D_SMOOTH))
print("N         Farey err     Halton err    Farey/Halton")
for n_target in [100, 500, 2000, 10000]:
    pts_f = farey_2d(n_target); pts_h = halton_2d(n_target)
    e_f = err(pts_f, f_2d_smooth, EXACT_2D_SMOOTH)
    e_h = err(pts_h, f_2d_smooth, EXACT_2D_SMOOTH)
    print(f"  {n_target:>5} | F={pts_f.shape[0]:>5} H={pts_h.shape[0]:>5}: {e_f:.4e}  {e_h:.4e}  {e_f/e_h if e_h>0 else 0:.3f}")

print("\n--- 2D Oscillatory: sin(2πx)·cos(2πy) + 0.5 (exact = 0.5) ---")
print("N         Farey err     Halton err    Farey/Halton")
for n_target in [100, 500, 2000, 10000]:
    pts_f = farey_2d(n_target); pts_h = halton_2d(n_target)
    e_f = err(pts_f, f_2d_oscillatory, EXACT_2D_OSC)
    e_h = err(pts_h, f_2d_oscillatory, EXACT_2D_OSC)
    print(f"  {n_target:>5} | F={pts_f.shape[0]:>5} H={pts_h.shape[0]:>5}: {e_f:.4e}  {e_h:.4e}  {e_f/e_h if e_h>0 else 0:.3f}")

print("\n--- 3D Smooth: exp(-x²-y²-z²) (exact ≈ {:.5f}) ---".format(EXACT_3D))
print("N         Farey err     Halton err    Farey/Halton")
for n_target in [100, 500, 2000]:
    pts_f = farey_3d(n_target); pts_h = halton_3d(n_target)
    e_f = err(pts_f, f_3d_smooth, EXACT_3D)
    e_h = err(pts_h, f_3d_smooth, EXACT_3D)
    print(f"  {n_target:>5} | F={pts_f.shape[0]:>5} H={pts_h.shape[0]:>5}: {e_f:.4e}  {e_h:.4e}  {e_f/e_h if e_h>0 else 0:.3f}")
