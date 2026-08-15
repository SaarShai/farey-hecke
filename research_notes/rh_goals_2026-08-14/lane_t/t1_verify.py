"""
Independent re-verification of the T1 v3 / amendment-A2 numerics.
Written from scratch (no reuse of the prior run's script, which was lost).

Conventions (pinned to T1 draft §2 (2.1) and Prop. 4.4):
  S_eps(w) = |M_W(1/2 + i|w|)|^2 * theta(|w|),  theta(w) = max(log(w/2pi), theta_min)
  theta_min = log(gamma_1 / 2pi)                      [clause (M4'') of A2]
  amplitude law taken with r_w == 1 (intensity-smoothed mean of 1/|zeta'|),
  which is the convention that reproduces the v2 number S_eps(gamma_d)=7.23e-35.

Windows:
  Gaussian (frozen v0):  W(x)=exp(-x^2),  M_W(s)=(1/2)Gamma(s/2)
                         |M_W(1/2+i w)| = (1/2)|Gamma(1/4 + i w/2)|
  Riesz k=1  (A2, W'):   W(x)=(1-x)_+,    M_W(s)=1/(s(s+1))
                         |M_W(1/2+i w)| = 1/sqrt((1/4+w^2)(9/4+w^2))

Fisher information, band-limited (T1 (4.0)):
  I_jk = (1/2pi) * int_{|nu|<=Omega} ghat_j(nu) conj(ghat_k(nu)) / S_eps(nu) dnu
with g_A = cos(w t+phi), g_w = -A t sin(w t+phi), g_phi = -A sin(w t+phi) on [0,T].
"""
import numpy as np

TWO_PI = 2.0 * np.pi

# ---------------------------------------------------------------- log-gamma
_LANCZOS_G = 7
_LANCZOS_C = np.array([
    0.99999999999980993, 676.5203681218851, -1259.1392167224028,
    771.32342877765313, -176.61502916214059, 12.507343278686905,
    -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7])


def log_gamma(z):
    """Complex log-Gamma (Lanczos), direct branch, valid for Re z > 0.

    No reflection formula: every argument we pass has Re z = 1/4 > 0, and the
    reflection branch would overflow via sin(pi z) once |Im z| exceeds ~350.
    """
    z = np.asarray(z, dtype=complex)
    assert np.all(z.real > 0.0), "direct Lanczos branch needs Re z > 0"
    zz = z - 1.0
    x = np.full(zz.shape, _LANCZOS_C[0], dtype=complex)
    for i in range(1, _LANCZOS_G + 2):
        x = x + _LANCZOS_C[i] / (zz + i)
    t = zz + _LANCZOS_G + 0.5
    return 0.5 * np.log(2 * np.pi) + (zz + 0.5) * np.log(t) - t + np.log(x)


def log_abs_MW(w, window):
    """log |M_W(1/2 + i w)|, vectorised, overflow-safe."""
    w = np.abs(np.asarray(w, dtype=float))
    if window == "gauss":
        return np.log(0.5) + log_gamma(0.25 + 0.5j * w).real
    if window == "riesz1":
        return -0.5 * (np.log(0.25 + w * w) + np.log(2.25 + w * w))
    raise ValueError(window)


GAMMA1 = 14.134725141734693
THETA_MIN = np.log(GAMMA1 / TWO_PI)


def log_S(w, window, floor=True):
    """log S_eps(w)."""
    w = np.abs(np.asarray(w, dtype=float))
    with np.errstate(divide="ignore", invalid="ignore"):
        th = np.log(np.where(w > 0, w, 1e-300) / TWO_PI)
    if floor:
        th = np.maximum(th, THETA_MIN)
    else:
        th = np.where(th <= 0, np.nan, th)
    return 2.0 * log_abs_MW(w, window) + np.log(th)


# ------------------------------------------------------- band-limited FIM
def D0(x, T):
    x = np.asarray(x, dtype=float)
    out = np.empty(x.shape, dtype=complex)
    small = np.abs(x) < 1e-12
    xs = np.where(small, 1.0, x)
    out = (np.exp(1j * xs * T) - 1.0) / (1j * xs)
    out[small] = T
    return out


def D1(x, T):
    x = np.asarray(x, dtype=float)
    out = np.empty(x.shape, dtype=complex)
    small = np.abs(x) < 1e-12
    xs = np.where(small, 1.0, x)
    d0 = (np.exp(1j * xs * T) - 1.0) / (1j * xs)
    out = T * np.exp(1j * xs * T) / (1j * xs) - d0 / (1j * xs)
    out[small] = T * T / 2.0
    return out


def fim_parts(w0, T, Omega, window, K=4.0, A=1.0, phi=0.4,
              dnu=2e-4, ref=None, white=False):
    """Return (I_total, I_near, I_rest) 3x3 real symmetric matrices.

    S_eps is normalised by S_eps(ref) (default ref=w0) to keep the Gaussian
    window's enormous dynamic range inside double precision; this rescales
    every I by a common positive factor and so leaves lambda_max(I_N^-1 I_R)
    and the ratio [I^-1]_ww / (24 S/(A^2 T^3)) exactly invariant.
    """
    if ref is None:
        ref = w0
    n = int(np.ceil(2 * Omega / dnu)) + 1
    h = 2.0 * Omega / (n - 1)
    logS_ref = log_S(np.array([ref]), window)[0]
    half = 2 * np.pi * K / T

    e_p, e_m = np.exp(1j * phi), np.exp(-1j * phi)
    I = np.zeros((3, 3)); IN = np.zeros((3, 3))

    # chunked trapezoid: keeps peak memory flat for very wide bands
    CH = 2_000_000
    for start in range(0, n, CH):
        stop = min(start + CH, n)
        idx = np.arange(start, stop)
        nu = -Omega + idx * h
        tw = np.full(nu.shape, h)                    # trapezoid weights
        tw[idx == 0] *= 0.5
        tw[idx == n - 1] *= 0.5

        inv_S = (np.ones_like(nu) if white else
                 np.exp(-(log_S(nu, window) - logS_ref)))

        d0p, d0m = D0(w0 - nu, T), D0(-w0 - nu, T)
        d1p, d1m = D1(w0 - nu, T), D1(-w0 - nu, T)
        g = [0.5 * (e_p * d0p + e_m * d0m),
             -A * (e_p * d1p - e_m * d1m) / (2j),
             -A * (e_p * d0p - e_m * d0m) / (2j)]

        near = (np.abs(np.abs(nu) - w0) <= half)
        for a in range(3):
            for b in range(a, 3):
                integ = (g[a] * np.conj(g[b])).real * inv_S * tw / (2 * np.pi)
                I[a, b] += integ.sum()
                IN[a, b] += integ[near].sum()

    for a in range(3):
        for b in range(a):
            I[a, b] = I[b, a]
            IN[a, b] = IN[b, a]
    return I, IN, I - IN


def lam_max(IN, IR):
    ev = np.linalg.eigvals(np.linalg.solve(IN, IR))
    return float(np.max(np.abs(ev)))


# ------------------------------------------------------------------ report
ZEROS = [14.134725141734693, 21.022039638771555, 25.010857580145688,
         30.424876125859513, 32.935061587739190, 37.586178158825671,
         40.918719012147495, 43.327073280914999, 48.005150881167159,
         49.773832477672302]
T = np.log(3e7)
GAMMA = 50.0
K = 4.0

print("=" * 74)
print("T = log(3e7) =", round(T, 6), "  Gamma =", GAMMA, "  Omega=2Gamma =", 2 * GAMMA, "  K =", K)
print("theta_min = log(gamma_1/2pi) =", round(THETA_MIN, 6))

print("\n--- (1) window magnitudes |M_W(1/2+i gamma_j)| ---")
print(f"{'j':>3} {'gamma_j':>11} {'gauss':>13} {'riesz1':>13} {'log(g/2pi)':>11}")
for j, g in enumerate(ZEROS, 1):
    if j in (1, 2, 3, 4, 5, 10):
        print(f"{j:>3} {g:>11.6f} {np.exp(log_abs_MW(g,'gauss')):>13.4e} "
              f"{np.exp(log_abs_MW(g,'riesz1')):>13.4e} {np.log(g/TWO_PI):>11.5f}")
gd = ZEROS[-1]
print("dynamic range gamma_1 -> gamma_10:  gauss = %.3e   riesz1 = %.4g" % (
    np.exp(log_abs_MW(ZEROS[0], 'gauss') - log_abs_MW(gd, 'gauss')),
    np.exp(log_abs_MW(ZEROS[0], 'riesz1') - log_abs_MW(gd, 'riesz1'))))
print("|M_W(1/2+i gamma_10)|: gauss %.4e -> riesz1 %.4e   (factor %.3e)" % (
    np.exp(log_abs_MW(gd, 'gauss')), np.exp(log_abs_MW(gd, 'riesz1')),
    np.exp(log_abs_MW(gd, 'riesz1') - log_abs_MW(gd, 'gauss'))))
print("S_eps(gamma_d) gauss = %.4e ;  S_eps(Omega=100) gauss = %.4e" % (
    np.exp(log_S(np.array([gd]), 'gauss'))[0],
    np.exp(log_S(np.array([100.0]), 'gauss'))[0]))
print("neighbour ratio |M_W(g2)/M_W(g1)|: gauss %.4e  riesz1 %.4f" % (
    np.exp(log_abs_MW(ZEROS[1], 'gauss') - log_abs_MW(ZEROS[0], 'gauss')),
    np.exp(log_abs_MW(ZEROS[1], 'riesz1') - log_abs_MW(ZEROS[0], 'riesz1'))))
print("|M_W(1/2+iw)| riesz1 range on |w|<=100: max %.4f (w=0)  min %.4e (w=100)" % (
    np.exp(log_abs_MW(0.0, 'riesz1')), np.exp(log_abs_MW(100.0, 'riesz1'))))

print("\n--- (2) Lindeberg ratio Lambda(Gamma) = 2 a_Gamma^2 / sigma^2(Gamma) ---")
print("   sigma^2(G) = (1/pi) int_G^inf a_w^2 log(w/2pi) dw   [Prop 4.4 + (M4)]")


def lindeberg(G, window, upper=None, npts=4_000_001):
    if upper is None:
        upper = G + 4000.0 if window == "gauss" else max(2e6, 2000 * G)
    u = np.linspace(np.log(G), np.log(upper), npts)      # log-grid
    w = np.exp(u)
    integ = np.exp(2 * log_abs_MW(w, window)) * np.log(w / TWO_PI) * w
    sig2 = np.trapezoid(integ, u) / np.pi
    return 2 * np.exp(2 * log_abs_MW(G, window)) / sig2


for G in (50.0, 200.0, 1000.0, 10000.0):
    lg = lindeberg(G, "gauss") if G <= 200 else float("nan")
    lr = lindeberg(G, "riesz1")
    closed = 6 * np.pi / (G * (np.log(G / TWO_PI) + 1.0 / 3.0))
    print(f"   Gamma={G:>7.0f}   gauss={lg:>10.4g}   riesz1={lr:>10.4g}   "
          f"closed-form 6pi/(G(log(G/2pi)+1/3))={closed:>10.4g}")

print("\n--- (3) GAP-4 flatness: max/min of S_eps over [g-2piK/T, g+2piK/T] ---")
half = 2 * np.pi * K / T
print("   half-width 2piK/T =", round(half, 5))
for j in (0, 4, 9):
    g = ZEROS[j]
    ww = np.linspace(g - half, g + half, 4001)
    for win in ("gauss", "riesz1"):
        s = np.exp(log_S(ww, win) - log_S(np.array([g]), win)[0])
        print(f"   gamma_{j+1:<2} = {g:8.4f}  {win:>7}  max/min = {s.max()/s.min():.4g}")

print("\n--- (4) factor 24: white noise, band-limited 3x3 FIM ---")
for (w0, Om) in ((3.7, 400.0), (14.1347, 400.0), (49.7738, 600.0)):
    I, _, _ = fim_parts(w0, T, Om, "riesz1", K=K, white=True, dnu=2e-4)
    val = np.linalg.inv(I)[1, 1] * T ** 3
    print(f"   w0={w0:>9.4f}  Omega={Om:>6.0f}   T^3*[I^-1]_ww = {val:.4f}")

print("\n--- (5) (B1) leakage at the approved cut Omega=2Gamma=100, window (W') ---")
print(f"{'j':>3} {'gamma_j':>10} {'lam_max(IN^-1 IR)':>19} {'[I^-1]_ww / local24':>21}")
rows = []
for j, g in enumerate(ZEROS, 1):
    I, IN, IR = fim_parts(g, T, 2 * GAMMA, "riesz1", K=K, dnu=2e-4)
    lm = lam_max(IN, IR)
    ratio = np.linalg.inv(I)[1, 1] / (24.0 / T ** 3)   # S_eps(w0) normalised to 1
    rows.append((j, g, lm, ratio))
    if j in (1, 2, 3, 4, 5, 10):
        print(f"{j:>3} {g:>10.4f} {lm:>19.4f} {ratio:>21.4f}")
print("   all ten ratios:", " ".join("%.3f" % r[3] for r in rows))
print("   all ten lam_max:", " ".join("%.3f" % r[2] for r in rows))

print("\n--- (6) same two quantities under the FROZEN GAUSSIAN window, Omega=100 ---")
I, IN, IR = fim_parts(gd, T, 2 * GAMMA, "gauss", K=K, dnu=2e-4)
print("   gamma_d: lam_max(IN^-1 IR) = %.4e ;  [I^-1]_ww/local24 = %.4e" % (
    lam_max(IN, IR), np.linalg.inv(I)[1, 1] / (24.0 / T ** 3)))

print("\n--- (7) Omega sweep at gamma_d under (W'): how wide may the band be? ---")
print(f"{'Omega':>8} {'lam_max(IN^-1 IR)':>19} {'[I^-1]_ww / local24':>21}")
for Om in (100.0, 200.0, 300.0, 400.0, 600.0, 1000.0, 15000.0):
    dn = 2e-4 if Om <= 1000 else 1e-3
    I, IN, IR = fim_parts(gd, T, Om, "riesz1", K=K, dnu=dn)
    print(f"{Om:>8.0f} {lam_max(IN, IR):>19.4f} "
          f"{np.linalg.inv(I)[1,1]/(24.0/T**3):>21.4f}")

print("\n--- (8) (M4'') floor sensitivity: vary theta_min, watch [I^-1]_ww ---")
base = None
for tm in (0.05, 0.2, 0.81076, 1.0, 2.0):
    globals()['THETA_MIN'] = tm
    I, _, _ = fim_parts(gd, T, 2 * GAMMA, "riesz1", K=K, dnu=2e-4)
    v = np.linalg.inv(I)[1, 1]
    if base is None:
        base = v
    print(f"   theta_min={tm:>7.5f}   [I^-1]_ww = {v:.10e}   rel.dev = {abs(v/base-1):.3e}")
globals()['THETA_MIN'] = np.log(GAMMA1 / TWO_PI)

print("\n--- (9) headline constants (window-free by Prop 4.4) ---")
for d, g in ((1, ZEROS[0]), (10, gd)):
    c = (6 * np.log(g / TWO_PI)) ** (1.0 / 3.0)
    print(f"   d={d:>2}  gamma_d={g:9.6f}  log(g/2pi)={np.log(g/TWO_PI):.6f}  "
          f"c=(6 log)^(1/3) = {c:.6f}")
print("   max_j RMSE bound at X=3e7, d=10: sqrt(6*%.5f)/%.4f = %.6f" % (
    np.log(gd / TWO_PI), T ** 1.5, np.sqrt(6 * np.log(gd / TWO_PI)) / T ** 1.5))
print("   at gamma_1: sqrt(6*%.5f)/%.4f = %.6f" % (
    np.log(ZEROS[0] / TWO_PI), T ** 1.5,
    np.sqrt(6 * np.log(ZEROS[0] / TWO_PI)) / T ** 1.5))
print("=" * 74)
