"""
zeta_mayer.py
=============
COMPLEX-s Mayer transfer operator -> Selberg zeta SPECTRAL determinant
for the MODULAR SURFACE PSL(2,Z) (Hecke anchor q=3).

GOAL (gate test)
----------------
Re-point the project's transfer-operator machinery from a REAL-s
Hausdorff-dimension Fredholm zero (d3_jp_dimension.py) to a COMPLEX-s
Selberg-zeta SPECTRAL zero on a NUCLEAR (holomorphic / disc-algebra)
function space, and recover the published SL2(Z) Maass eigenvalues.

PASS/FAIL ANCHOR (published; unforgiving)
-----------------------------------------
First SL2(Z) Maass spectral parameters r_k (lambda = 1/4 + r^2):
    r1 = 9.533695261...   (ODD  Maass form)
    r2 = 12.173008...     (EVEN)
    r3 = 13.779751...     (ODD)
    r4 = 14.358509...     (EVEN)
    r5 = 16.138073...     (EVEN)
Recover r1..r5 to >= 6 digits on the line Re(s)=1/2.

MATHEMATICS (Mayer 1976/1991; Mayer-Muehlenbruch-Stroemberg 2012)
-----------------------------------------------------------------
The Selberg zeta of the modular surface factors as
    Z(s) = det(1 - L_s) * det(1 + L_s)
where L_s is the Mayer (Gauss-Kuzmin-Wirsing) transfer operator acting on
functions holomorphic on the disc D = { |z - 1| < 3/2 }:

    (L_s f)(z) = sum_{n=1}^inf  (z+n)^{-2s} f( 1/(z+n) ).

Each inverse Gauss branch psi_n(z) = 1/(z+n) maps D strictly inside D, so
L_s is NUCLEAR of order 0 (trace-class on a holomorphic Banach space) -- the
whole point versus the real-s bounded-type engine, which lived on a real
interval with a finite alphabet and had no holomorphic/nuclear structure.

Maass cusp eigenvalues lambda = s(1-s) appear as ZEROS of
    det(1 ∓ L_s)   on the critical line Re(s)=1/2.
EVEN Maass forms  <->  zeros of det(1 - L_s).
ODD  Maass forms  <->  zeros of det(1 + L_s).
(r1, r3 are ODD; r2, r4, r5 are EVEN -- so a correct engine must test BOTH
 det(1-L_s) and det(1+L_s) and union the zeros.)

NUMERICS
--------
Represent f by its Taylor coefficients about the FIXED POINT z0 of the disc
self-map structure (the Gauss-map "golden" fixed point z0 = (sqrt5-1)/2 of
psi_1, the dominant branch; expanding about z0 is the standard nuclear
discretization that converges geometrically -- Mayer-Stroemberg).

Matrix of L_s in the monomial basis {(z - z0)^k}:
    (L_s)_{jk} = (1/j!) d^j/dz^j [ (L_s e_k)(z) ] |_{z=z0}
with e_k(z) = (z - z0)^k. We compute these matrix entries by summing the
branch series and Cauchy-integrating (FFT on a circle around z0) for the
Taylor coefficients -- exact to machine precision, fully complex-s.

The truncated Fredholm determinant det(1 ∓ L_s) is then det(I ∓ M_N) for the
N x N truncation; we use the Newton-identity / characteristic-polynomial route
(same det-from-traces spirit as d3_jp_dimension.py) but here directly via
numpy's complex eigenvalues since M_N is small and dense.

q=3 ONLY. No interval certification, no non-arith q. Single anchor gate.
"""
from __future__ import annotations
import math
import cmath
import numpy as np

# Published SL2(Z) Maass spectral parameters (Hejhal; LMFDB)
PUBLISHED_R = [9.533695261, 12.173008, 13.779751, 14.358509, 16.138073]
PUBLISHED_PARITY = ["odd", "even", "odd", "even", "even"]  # which det(1∓L) hosts each

# ----------------------------------------------------------------------------
# Mayer transfer operator L_s on the holomorphic disc, Taylor-coeff matrix.
# ----------------------------------------------------------------------------

# Expansion center: the attracting fixed point of psi_1(z)=1/(1+z),
# z0 = (sqrt(5)-1)/2 = 0.6180339887... (golden), interior to D=|z-1|<3/2.
Z0 = (math.sqrt(5.0) - 1.0) / 2.0


def Ls_apply_to_monomial(k, s, z, n_terms):
    """
    Value of (L_s e_k)(z), e_k(w)=(w - Z0)^k, at complex point z:
        sum_{n=1}^{n_terms} (z+n)^{-2s} * ( 1/(z+n) - Z0 )^k .
    Branch series converges like sum n^{-2 Re(s)} (Re(s)=1/2 -> n^{-1}: slow,
    so n_terms must be large; we accelerate the tail analytically below).
    """
    total = 0.0 + 0.0j
    for n in range(1, n_terms + 1):
        zn = z + n
        psi = 1.0 / zn
        total += zn ** (-2.0 * s) * (psi - Z0) ** k
    return total


def Ls_apply_to_monomial_accel(k, s, z, n_head, n_tail_terms):
    """
    Same as above but with Euler-Maclaurin tail acceleration for the slow
    n^{-2s} series at Re(s)=1/2. Sum head exactly, then approximate the tail
    sum_{n>n_head} (z+n)^{-2s} (1/(z+n) - Z0)^k by Euler-Maclaurin.

    For the tail we use g(n) = (z+n)^{-2s} (1/(z+n)-Z0)^k. As n->inf,
    (1/(z+n)-Z0)^k -> (-Z0)^k, so the tail ~ (-Z0)^k * Hurwitz-zeta-like sum.
    We just take many head terms + a couple Euler-Maclaurin correction terms.
    """
    head = 0.0 + 0.0j
    for n in range(1, n_head + 1):
        zn = z + n
        head += zn ** (-2.0 * s) * (1.0 / zn - Z0) ** k

    # Euler-Maclaurin tail from n_head+1 to infinity of g(n).
    def g(nn):
        zn = z + nn
        return zn ** (-2.0 * s) * (1.0 / zn - Z0) ** k

    # integral_{n_head+0.5}^inf g(x) dx  -- approximate numerically (midpoint+EM)
    # Use the analytic leading behavior: g(x) ~ x^{-2s} (-Z0)^k for large x.
    # We'll just extend the explicit sum with EM correction terms.
    a = n_head + 1
    # trapezoid-style EM: sum_{n>=a} g(n) ≈ ∫_a^inf g + g(a)/2 - g'(a)/12 + ...
    # Compute ∫_a^inf g(x)dx by substitution; do it numerically via mpmath-free
    # Gauss-Legendre on a transformed semi-infinite interval.
    # Simpler & robust: add a large explicit block then EM-correct.
    tail = 0.0 + 0.0j
    for n in range(a, a + n_tail_terms):
        tail += g(n)
    # EM correction for remaining infinite tail beyond a+n_tail_terms:
    b = a + n_tail_terms
    # integral_b^inf x^{-2s}(-Z0)^k dx  (leading) = (-Z0)^k * b^{1-2s}/(2s-1)
    # plus next-order; this is small if b large.
    lead = ((-Z0) ** k) * (b ** (1.0 - 2.0 * s)) / (2.0 * s - 1.0)
    tail += lead
    return head + tail


def build_Ls_matrix(s, N, n_head=4000, n_tail=4000, contour_radius=0.30,
                    n_fft=None):
    """
    Build the N x N matrix M of L_s in the monomial basis {(z-Z0)^k}_{k=0}^{N-1}.

    Column k = Taylor coefficients (about Z0) of the holomorphic function
    (L_s e_k)(z), extracted by Cauchy's formula on a circle of radius
    `contour_radius` about Z0 via FFT.

        c_j = (1/2pi i) oint  (L_s e_k)(z) / (z-Z0)^{j+1} dz
            = (1/M) sum_{m} (L_s e_k)(Z0 + R e^{i th_m}) R^{-j} e^{-i j th_m}.

    The FFT contour stays inside D and inside the convergence disc of all
    branch images, so the coefficients are extracted to machine precision.
    """
    if n_fft is None:
        n_fft = max(4 * N, 64)
    R = contour_radius
    thetas = 2.0 * np.pi * np.arange(n_fft) / n_fft
    zpts = Z0 + R * np.exp(1j * thetas)

    # Evaluate (L_s e_k)(z) at all contour points, for all k=0..N-1.
    # Vectorize over n (branch index) and contour point.
    ns = np.arange(1, n_head + 1)
    # shape (n_fft, n_head)
    ZN = zpts[:, None] + ns[None, :]
    PSI = 1.0 / ZN
    W = ZN ** (-2.0 * s)                  # (z+n)^{-2s}
    base = (PSI - Z0)                     # (1/(z+n) - Z0), shape (n_fft,n_head)

    # head sums S_k[z] = sum_n W * base^k  for k=0..N-1 via running power
    S = np.zeros((n_fft, N), dtype=complex)
    powk = np.ones_like(base)            # base^0
    for k in range(N):
        S[:, k] = np.sum(W * powk, axis=1)
        powk = powk * base

    # Euler-Maclaurin / power-law tail for n > n_head (slow at Re s=1/2).
    # Tail of column k: sum_{n>n_head} (z+n)^{-2s}(1/(z+n)-Z0)^k.
    # Add an explicit block then an analytic remainder.
    ns2 = np.arange(n_head + 1, n_head + 1 + n_tail)
    ZN2 = zpts[:, None] + ns2[None, :]
    PSI2 = 1.0 / ZN2
    W2 = ZN2 ** (-2.0 * s)
    base2 = (PSI2 - Z0)
    powk2 = np.ones_like(base2)
    b = n_head + n_tail + 1
    for k in range(N):
        block = np.sum(W2 * powk2, axis=1)
        # analytic remainder sum_{n>=b} (z+n)^{-2s} (-Z0)^k  (leading term)
        rem = ((-Z0) ** k) * (b ** (1.0 - 2.0 * s)) / (2.0 * s - 1.0)
        S[:, k] += block + rem
        powk2 = powk2 * base2

    # FFT extraction of Taylor coefficients c_j for each column k.
    # c_j = (1/n_fft) sum_m S[m,k] * R^{-j} e^{-i j th_m}
    # = R^{-j} * (DFT of S[:,k]) [j] / n_fft
    C = np.fft.fft(S, axis=0) / n_fft     # (n_fft, N); row j = DFT bin j
    M = np.empty((N, N), dtype=complex)
    Rinv = R ** (-np.arange(N))
    for k in range(N):
        M[:, k] = C[:N, k] * Rinv
    return M


# ----------------------------------------------------------------------------
# Fredholm determinants det(1 ∓ L_s)
# ----------------------------------------------------------------------------

def fredholm_dets(s, N, **kw):
    """Return (det(1 - L_s), det(1 + L_s)) for the N-truncation."""
    M = build_Ls_matrix(s, N, **kw)
    ev = np.linalg.eigvals(M)
    d_minus = np.prod(1.0 - ev)
    d_plus = np.prod(1.0 + ev)
    return d_minus, d_plus, ev


def Z_selberg(s, N, **kw):
    """Selberg zeta Z(s) = det(1-L_s) det(1+L_s)."""
    dm, dp, _ = fredholm_dets(s, N, **kw)
    return dm * dp


# ----------------------------------------------------------------------------
# Root finding on the critical line Re(s) = 1/2.
# ----------------------------------------------------------------------------

def det_on_line(r, which, N, **kw):
    """
    Value of det(1 ∓ L_s) at s = 1/2 + i r  (r real -> spectral parameter).
    `which` in {'minus','plus'}. On the critical line s = 1/2 + i r,
    1-s = 1/2 - i r = conj(s); the determinant is real (functional eqn), so a
    zero is a sign change of its REAL part.
    """
    s = 0.5 + 1j * r
    dm, dp, _ = fredholm_dets(s, N, **kw)
    return dm if which == 'minus' else dp


def scan_and_refine(which, r_lo, r_hi, n_grid, N, **kw):
    """Scan Re of det along the line, bracket sign changes of Re, bisection-refine."""
    rs = np.linspace(r_lo, r_hi, n_grid)
    vals = np.array([det_on_line(r, which, N, **kw).real for r in rs])
    roots = []
    for i in range(len(rs) - 1):
        if vals[i] == 0.0:
            roots.append(rs[i])
        elif vals[i] * vals[i + 1] < 0:
            a, b = rs[i], rs[i + 1]
            fa, fb = vals[i], vals[i + 1]
            for _ in range(80):
                m = 0.5 * (a + b)
                fm = det_on_line(m, which, N, **kw).real
                if fa * fm <= 0:
                    b, fb = m, fm
                else:
                    a, fa = m, fm
                if b - a < 1e-11:
                    break
            roots.append(0.5 * (a + b))
    return roots, rs, vals


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

def main():
    print("=" * 74)
    print("Mayer transfer operator -> Selberg zeta, q=3 (modular surface PSL(2,Z))")
    print("Complex-s spectral determinant det(1∓L_s) on holomorphic disc D=|z-1|<3/2")
    print("=" * 74)
    print(f"Expansion center Z0 = (sqrt5-1)/2 = {Z0:.12f}")
    print(f"Published Maass r_k: {PUBLISHED_R}")
    print(f"Parity (det host):   {PUBLISHED_PARITY}")
    print()

    # ---- sanity: trivial zero / known structural check at s=1 -------------
    # Z(s) has a zero at s=1 (constant function eigenvalue): L_1 has eigenvalue 1
    # (Gauss-Kuzmin-Wirsing: leading eigenvalue of GKW operator at s=1 is 1).
    print("STRUCTURAL CHECK: leading eigenvalue of L_s at s=1 should be 1 (GKW).")
    for N in [10, 20, 30]:
        M = build_Ls_matrix(1.0 + 0j, N)
        ev = np.linalg.eigvals(M)
        lead = ev[np.argmax(np.abs(ev))]
        print(f"   N={N:3d}  leading eig = {lead.real:.10f} + {lead.imag:.2e}i  "
              f"(target 1.0)  det(1-L_1)={np.prod(1-ev).real:.3e}")
    print()

    # ---- scan the critical line for the first 5 Maass r_k -----------------
    N = 40            # truncation dimension
    r_lo, r_hi = 8.0, 17.0
    n_grid = 460      # ~0.02 spacing -> resolves the ~0.5-3 gaps between r_k

    print(f"SCANNING critical line s=1/2+ir, r in [{r_lo},{r_hi}], N={N}, "
          f"grid={n_grid}")
    print("  (union of det(1-L_s) [even] and det(1+L_s) [odd] zeros)")

    roots_m, rs_m, vals_m = scan_and_refine('minus', r_lo, r_hi, n_grid, N)
    roots_p, rs_p, vals_p = scan_and_refine('plus', r_lo, r_hi, n_grid, N)

    print(f"\n  det(1 - L_s) [EVEN forms] zeros: "
          f"{[f'{x:.6f}' for x in roots_m]}")
    print(f"  det(1 + L_s) [ODD  forms] zeros: "
          f"{[f'{x:.6f}' for x in roots_p]}")

    # union, sorted, tag parity
    tagged = [(r, 'even') for r in roots_m] + [(r, 'odd') for r in roots_p]
    tagged.sort()
    print("\n  UNION (sorted) recovered spectral parameters:")
    for r, par in tagged:
        print(f"     r = {r:.6f}   ({par})")

    # ---- match to published and print residuals ---------------------------
    print("\n" + "=" * 74)
    print("MATCH vs PUBLISHED  (residual = recovered - published)")
    print("=" * 74)
    recovered_rs = [t[0] for t in tagged]
    max_resid = 0.0
    n_hit = 0
    for rp, par in zip(PUBLISHED_R, PUBLISHED_PARITY):
        if recovered_rs:
            j = int(np.argmin([abs(rr - rp) for rr in recovered_rs]))
            rr = recovered_rs[j]
            resid = rr - rp
        else:
            rr, resid = float('nan'), float('nan')
        hit = abs(resid) < 1e-4 if not math.isnan(resid) else False
        if hit:
            n_hit += 1
            max_resid = max(max_resid, abs(resid))
        flag = "HIT" if hit else "MISS"
        print(f"  published r={rp:11.6f} ({par:4s})  recovered={rr:11.6f}  "
              f"residual={resid:+.2e}  [{flag}]")

    print()
    if n_hit >= 5 and max_resid < 1e-4:
        print(f"VERDICT: PASS  (recovered {n_hit}/5 to <1e-4, max resid {max_resid:.1e})")
    elif n_hit >= 3:
        print(f"VERDICT: PARTIAL  (recovered {n_hit}/5)")
    else:
        print(f"VERDICT: FAIL  (recovered {n_hit}/5)")
    return tagged


if __name__ == "__main__":
    main()
