"""
D5: Implement MiMo's L-zero phase tomography algorithm.

Take LHS_n(A) from the previous sprint's (q=2, M=T³) data.
Apply character sum to isolate the order-4 character component.
Build Hankel matrix. Eigenvalues are (sqrt(2) * e^{i theta_j})^2.
Extract theta_j (the L-zero phases of L(u, chi_4)).

Then COMPARE to the direct L-function zero computation.
"""

import json
import math
import cmath
import sys

# Load the previous sprint's data
try:
    with open("/tmp/ak_d2/out_T3.json") as f:
        data = json.load(f)
except FileNotFoundError:
    print("Need /tmp/ak_d2/out_T3.json — running compute.py first...")
    sys.exit(1)

# Data layout: data['pi_K'] = pi_{1/2,K}(2^n) cumulative; data['pi_class'] = dict A -> [pi(...; A) ...]
Phi = data['Phi']
units = data['units']
N = data['N']
pi_K = data['pi_K']
pi_class = {int(k): v for k, v in data['pi_class'].items()}

# Compute LHS_n(A) = pi_K(n) - Phi * pi_class[A](n)
LHS = {}
for A in units:
    LHS[A] = [pi_K[n] - Phi * pi_class[A][n] for n in range(N + 1)]

# Characters of G = (F_2[T]/T^3)^* ~ Z/4Z, generator g = 1+T which is packed as 3
# Powers of g: g^0=1 (=1), g^1=3 (=1+T), g^2=5 (=1+T^2), g^3=7 (=1+T+T^2)
# chi_k(g^j) = exp(2*pi*i*k*j/4)
# Conjugate character chi_bar_k(g^j) = exp(-2*pi*i*k*j/4)

# Map A -> j (discrete log w.r.t. g=3)
# A=1 -> j=0; A=3 -> j=1; A=5 -> j=2; A=7 -> j=3
def dlog(A):
    return {1: 0, 3: 1, 5: 2, 7: 3}[A]

# chi_bar_k(A) = exp(-2 pi i k * dlog(A) / 4)
def chi_bar(k, A):
    j = dlog(A)
    return cmath.exp(-2j * math.pi * k * j / 4)

# Extract chi_k component of LHS_n
def Delta_chi(k, n):
    return sum(chi_bar(k, A) * LHS[A][n] for A in units)

# Print the four character components for n = 1..10
print("Δ_n^(chi_k) for k=0,1,2,3, n=1..10 (k=0 trivial, k=2 quadratic real, k=1,3 conjugate order-4):")
print(f"{'n':>3} | {'k=0':>20} {'k=1':>30} {'k=2':>20} {'k=3':>30}")
for n in range(1, 11):
    row = [f"{n:>3} |"]
    for k in range(4):
        d = Delta_chi(k, n)
        row.append(f"{d.real:+10.5f}{d.imag:+10.5f}i")
    print(" ".join(row))

# Focus on the order-4 character k=1.
# Δ_n^(chi_1) = sum over zeros (sqrt(2) e^{i theta_j})^n
# For (q=2, M=T^3), L(u, chi_1) is degree 2 (since deg M - 1 = 2), so 2 zeros.
# Two unknowns. Need at least 4 measurements (2 d_chi).

# Build a 2x2 Hankel matrix using n=1,2,3 (i.e., H[i,j] = Δ_{i+j+1}^{(chi_1)})
# Then eigenvalues of H are (sqrt(2) e^{i theta_j})^? — actually let's be careful.

# Prony's method: signal s_n = Σ_j C_j r_j^n where r_j are unknown poles.
# Build Hankel-like matrices and solve.

# Construct s_n = Δ_n^(chi_1) for n=1..6.
sig = [Delta_chi(1, n) for n in range(1, 11)]
print("\nSignal s_n = Δ_n^(chi_1):")
for n, s in enumerate(sig, 1):
    print(f"  n={n:>2}: {s.real:+10.5f} {s.imag:+10.5f}i  (|.| = {abs(s):8.5f})")

# Prony: build Hankel H_0 of size d x d where d=2 (number of poles), starting at index k.
# H_0 (i, j) = s_{i+j}, H_1 (i, j) = s_{i+j+1} for i, j = 0..d-1.
# Then H_1 = H_0 * diag(r_j) projected — actually the standard approach is:
# the roots of the polynomial p(x) = x^d - p_{d-1} x^{d-1} - ... - p_0 are the poles,
# where (p_0, ..., p_{d-1}) solves H_0 * p = h where h = (s_d, s_{d+1}, ..., s_{2d-1}).

# For d=2, want p_0, p_1 such that s_{n+2} = p_1 s_{n+1} + p_0 s_n for all n.
# Use n=1, 2: H = [[s_1, s_2], [s_2, s_3]], rhs = [s_3, s_4].

import numpy as np

s = np.array(sig, dtype=complex)
# Use indices 1..6 (signal positions 0..5 in our array; sig[i] = s_{i+1})

d = 2  # number of poles
# Use Pisarenko/Prony with multiple equations
def prony(signal, d):
    """Prony's method. Returns list of poles."""
    N = len(signal)
    # Build matrix equation: signal[d], signal[d+1], ..., signal[N-1]
    # = sum_{k=0}^{d-1} p_k * signal[k], signal[k+1], etc.
    n_eqs = N - d
    if n_eqs < d:
        return []
    H = np.zeros((n_eqs, d), dtype=complex)
    rhs = np.zeros(n_eqs, dtype=complex)
    for i in range(n_eqs):
        for j in range(d):
            H[i, j] = signal[i + j]
        rhs[i] = signal[i + d]
    # Solve H @ p = rhs (least squares)
    p, *_ = np.linalg.lstsq(H, rhs, rcond=None)
    # Poles are roots of x^d - p[d-1] x^{d-1} - ... - p[0]
    poly_coeffs = np.concatenate(([1.0], -p[::-1]))
    poles = np.roots(poly_coeffs)
    return poles

poles = prony(s, d=2)
print(f"\nProny estimated poles for chi_1 (signal length {len(s)}):")
for i, p in enumerate(poles):
    mag = abs(p)
    arg = math.degrees(cmath.phase(p))
    print(f"  pole #{i}: {p.real:+10.5f} {p.imag:+10.5f}i  (|p|={mag:8.5f}, arg={arg:+8.3f}°)")

# Expected: poles should be the zeros u_j of L(u, chi_1) but with a transformation.
# L(u, chi_1) has zeros at u = q^{-1/2} e^{i theta_j} = (1/sqrt(2)) e^{i theta_j}
# So the "frequency" e^{i theta_j} corresponds in the signal s_n to ratio r = sqrt(2) e^{i theta_j}
# (since (sqrt(2) e^{i theta_j})^n is the contribution).
# So poles should have |p| = sqrt(2) ≈ 1.414.

# From lfunc.py, the directly-computed L(u, chi_1) values at u=1/sqrt(2):
# L = 0.5 + i*(sqrt(2)-1)/2 ≈ 0.5 + 0.2071i, |L| ≈ 0.541
# L coefficients (from lfunc.py output): coeffs=[(1.0, 0.0), (~0, 1.0), (-1.0, -1.0)]
# So L(u, chi_1) = 1 + i u + (-1 - i) u^2.
# Zeros: solve (-1-i) u^2 + i u + 1 = 0
# u = [-i ± sqrt(-1 - 4(-1-i))] / (2(-1-i))
# = [-i ± sqrt(3 + 4i)] / (-2 - 2i)

import cmath as _cmath
# Solve (-1-i) u^2 + i u + 1 = 0
a, b, c = (-1-1j), 1j, 1
disc = b**2 - 4*a*c
print(f"\nDirect L(u, chi_1) = 1 + i u + (-1-i) u^2; zeros:")
for sign in [+1, -1]:
    u = (-b + sign * _cmath.sqrt(disc)) / (2*a)
    mag = abs(u)
    arg = math.degrees(_cmath.phase(u))
    print(f"  u_zero: {u.real:+10.5f} {u.imag:+10.5f}i  (|u|={mag:8.5f}, arg={arg:+8.3f}°)")
    # The Prony pole r corresponds to r = 1/u (since signal s_n ~ sum C_j r_j^n, and r_j = q/u_j actually)
    # More precisely: signal s_n = sum_zero ... let me work this out carefully.

print("\nExpected Prony poles: r_j = sqrt(2) * e^{i theta_j} where theta_j = arg(u_zero).")
print("So |r_j| should be sqrt(2) ≈ 1.41421, and arg(r_j) = arg(u_zero).")
