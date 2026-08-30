#!/usr/bin/env python3
"""
High-precision computation of Riemann zeta zero analysis quantities.
Uses mpmath for arbitrary precision and scipy for numerical integration.
"""

import math
from mpmath import mp, log, exp, sqrt, pi, sin, cos, mpf, fabs, asin, quad, ceil
import numpy as np
from scipy.integrate import quad as scipy_quad
import warnings
warnings.filterwarnings('ignore')

# Set precision to ensure at least 16 significant digits
mp.dps = 50  # 50 decimal places

# ============================================================================
# 1. BASIC CONSTANTS
# ============================================================================
T = log(mpf('3e7'))
K = mpf(4)
twopi = 2*pi
gamma10 = mpf('49.773832477672302')
GAMMA_OP = mpf('51.23362034')
h = twopi*K/T

print("="*80)
print("HIGH-PRECISION RIEMANN ZERO ANALYSIS")
print("="*80)

print("\n1. FUNDAMENTAL PARAMETERS:")
print(f"   T = log(3e7) = {T}")
print(f"   8*pi = {8*pi}")
print(f"   h = 8*pi*K/T = {h}")

print("\n2. M5 THRESHOLD:")
print(f"   gamma10 + h = {gamma10 + h}")

print("\n3. GAMMA_OP OFFSET:")
offset = GAMMA_OP - (gamma10 + h)
print(f"   GAMMA_OP - (gamma10 + h) = {offset}")

print("\n4. T*(GAMMA_OP - gamma10) vs 8*pi:")
T_offset = T*(GAMMA_OP - gamma10)
print(f"   T*(GAMMA_OP - gamma10) = {T_offset}")
print(f"   8*pi = {8*pi}")
print(f"   difference = {T_offset - 8*pi}")

print("\n5. OMEGA:")
Omega = 2*GAMMA_OP
print(f"   Omega = 2*GAMMA_OP = {Omega}")

print("\n6. SCALING FUNCTIONS:")
gamma_ratio = GAMMA_OP/(2*pi)
L = log(gamma_ratio)
L_plus_third = L + mpf(1)/mpf(3)
L_plus_fifth = L + mpf(1)/mpf(5)
print(f"   GAMMA_OP/(2*pi) = {gamma_ratio}")
print(f"   L = log(GAMMA_OP/(2*pi)) = {L}")
print(f"   L + 1/3 = {L_plus_third}")
print(f"   GAMMA_OP*(L + 1/3) = {GAMMA_OP * L_plus_third}")
print(f"   L + 1/5 = {L_plus_fifth}")

print("\n7. LAMBDA_AS:")
Lambda_as = 6*pi/(GAMMA_OP * L_plus_third)
print(f"   Lambda_as = 6*pi/(GAMMA_OP*(L+1/3)) = {Lambda_as}")

print("\n8. SIG2 and SIGMA:")
sig2 = GAMMA_OP**(-3)/(3*pi) * L_plus_third
print(f"   sig2 = GAMMA_OP^(-3)/(3*pi)*(L+1/3) = {sig2}")
print(f"   sqrt(sig2) = {sqrt(sig2)}")

print("\n9. RHO/SIG3 RATIO:")
rho_over_sig3_base = (mpf(16)/(15*pi**2)) * (3*pi)**(mpf(1.5)) * GAMMA_OP**(-mpf(0.5)) * (L + mpf(0.2))/(L_plus_third)**mpf(1.5)
print(f"   rho/sig3 = {rho_over_sig3_base}")
print(f"   0.56 * (rho/sig3) = {mpf('0.56') * rho_over_sig3_base}")

print("\n10. L_D DERIVATIVE:")
L_d = log(gamma10/(2*pi))
print(f"   L_d = log(gamma10/(2*pi)) = {L_d}")
print(f"   6*L_d = {6*L_d}")
print(f"   sqrt(6*L_d) = {sqrt(6*L_d)}")
C_X = (6*L_d)**(mpf(1)/mpf(3))
print(f"   C_X = (6*L_d)^(1/3) = {C_X}")

print("\n11. POWER FORMS:")
T_15 = T**mpf(1.5)
T_3 = T**3
local_RMSE = sqrt(6*L_d)/T_15
print(f"   T^1.5 = {T_15}")
print(f"   T^3 = {T_3}")
print(f"   local_RMSE = sqrt(6*L_d)/T^1.5 = {local_RMSE}")

print("\n12. GAMMA1 ANALYSIS:")
gamma1 = mpf('14.134725141734693')
L1 = log(gamma1/(2*pi))
sqrt_6L1_over_T15 = sqrt(6*L1)/T_15
print(f"   gamma1 = {gamma1}")
print(f"   L1 = log(gamma1/(2*pi)) = {L1}")
print(f"   sqrt(6*L1)/T^1.5 = {sqrt_6L1_over_T15}")

print("\n13. HARMONIC SERIES:")
H9 = sum(mpf(1)/mpf(k) for k in range(1, 10))
print(f"   H9 = sum(1/k, k=1..9) = {H9}")
print(f"   H9/pi = {H9/pi}")
print(f"   1/(1 + H9/(pi*K)) = {1/(1 + H9/(pi*K))}") 

print("\n14. NSTAR (SAMPLE COUNTS):")
nstar_1 = Omega*T/pi
nstar_2 = 2*Omega*T/pi
print(f"   Omega*T/pi = {nstar_1}")
print(f"   2*Omega*T/pi = {nstar_2}")
print(f"   ceil(Omega*T/pi) = {ceil(nstar_1)}")
print(f"   ceil(2*Omega*T/pi) = {ceil(nstar_2)}")

print("\n15. ALPHA AND PRIOR SUPPORT:")
alpha = pi*K/T
mu_minus_alpha = gamma10 - alpha
mu_minus_alpha_over_2pi = mu_minus_alpha / (2*pi)
print(f"   alpha = pi*K/T = {alpha}")
print(f"   mu - alpha = gamma10 - alpha = {mu_minus_alpha}")
print(f"   log((mu-alpha)/(2*pi)) = {log(mu_minus_alpha_over_2pi)}")

Ieff = T**3 / (6*log(mu_minus_alpha_over_2pi))
Ipi = T**2 / (K**2)
I_sum = Ieff + Ipi
print(f"   I_eff = T^3/(6*log((mu-alpha)/(2*pi))) = {Ieff}")
print(f"   I_pi = T^2/K^2 = {Ipi}")
print(f"   I_eff + I_pi = {I_sum}")
print(f"   1/(I_eff + I_pi) = {1/I_sum}")
print(f"   sqrt(1/(I_eff + I_pi)) = {sqrt(1/I_sum)}")

# ============================================================================
# 2. ZERO ORDINATES AND GAPS
# ============================================================================
print("\n" + "="*80)
print("RIEMANN ZERO ORDINATES AND GAPS")
print("="*80)

g = {
    1: mpf('14.134725141734693'),
    2: mpf('21.022039638771555'),
    3: mpf('25.010857580145688'),
    4: mpf('30.424876125859513'),
    5: mpf('32.935061587739189'),
    6: mpf('37.586178294788217'),
    7: mpf('40.918890098303744'),
    8: mpf('43.327073280914999'),
    9: mpf('48.005150881167159'),
    10: mpf('49.773832477672302'),
    11: mpf('52.970321477714460'),
}

print(f"\nZero gaps vs h = {h} and 2h = {2*h}:")
print(f"{'j':>3} {'g[j+1]-g[j]':>25} {'gap/h':>15} {'gap/(2h)':>15}")
print("-" * 65)
for j in range(1, 11):
    gap = g[j+1] - g[j]
    ratio_h = gap / h
    ratio_2h = gap / (2*h)
    print(f"{j:3d} {gap:25.16e} {ratio_h:15.10f} {ratio_2h:15.10f}")

# ============================================================================
# 3. MAGNITUDE AND LOG FUNCTIONS
# ============================================================================
print("\n" + "="*80)
print("MAGNITUDE AND LOG ANALYSIS")
print("="*80)

print(f"\n{'j':>3} {'|M_W|':>25} {'log(w/(2*pi))':>25}")
print("-" * 55)
for j in range(1, 11):
    w = g[j]
    M_W = 1/sqrt((mpf(0.25)+w**2)*(mpf(2.25)+w**2))
    log_w = log(w/(2*pi))
    print(f"{j:3d} {M_W:25.16e} {log_w:25.16e}")

# ============================================================================
# 4. D AND DSTAR FUNCTIONS
# ============================================================================
def D_func(w):
    """D(w) = -2*w/(0.25+w^2) - 2*w/(2.25+w^2) + 1/(w*log(w/(2*pi)))"""
    if w <= 0:
        return mpf('nan')
    log_w = log(w/(2*pi))
    return -2*w/(mpf(0.25)+w**2) - 2*w/(mpf(2.25)+w**2) + 1/(w*log_w)

def Dstar_func(w):
    """Dstar(w) = 2*w/(0.25+w^2) + 2*w/(2.25+w^2) + 1/(w*log(w/(2*pi)))"""
    if w <= 0:
        return mpf('nan')
    log_w = log(w/(2*pi))
    return 2*w/(mpf(0.25)+w**2) + 2*w/(mpf(2.25)+w**2) + 1/(w*log_w)

def Dp_func(w):
    """D'(w) = derivative of D(w)"""
    if w <= 0:
        return mpf('nan')
    log_w = log(w/(2*pi))
    term1 = 2*(w**2 - mpf(0.25))/(w**2 + mpf(0.25))**2
    term2 = 2*(w**2 - mpf(2.25))/(w**2 + mpf(2.25))**2
    term3 = -(log_w + 1)/(w**2 * log_w**2)
    return term1 + term2 + term3

print("\n" + "="*80)
print("D(w) AND DSTAR(w) EVALUATION")
print("="*80)

for j in [1, 2, 3, 4, 5, 10]:
    print(f"\nZero j={j}: g[{j}] = {g[j]}")
    wminus = g[j] - h
    wplus = g[j] + h
    
    D_minus = D_func(wminus)
    D_center = D_func(g[j])
    D_plus = D_func(wplus)
    
    Dstar_minus = Dstar_func(wminus)
    term1 = 2*h*Dstar_minus
    exp_term = exp(term1)
    exp_neg_term = exp(-term1)
    
    print(f"  D(w-h) where w-h={wminus:.16e}: {D_minus:.16e}")
    print(f"  D(w)   where w={g[j]:.16e}: {D_center:.16e}")
    print(f"  D(w+h) where w+h={wplus:.16e}: {D_plus:.16e}")
    print(f"  Dstar(w-h): {Dstar_minus:.16e}")
    print(f"  2*h*Dstar(w-h): {term1:.16e}")
    print(f"  exp(2*h*Dstar(w-h)): {exp_term:.16e}")
    print(f"  exp(-2*h*Dstar(w-h)): {exp_neg_term:.16e}")
    
    # Check if D is negative on [w-h, w+h]
    test_points = [wminus + (wplus - wminus)*mpf(k)/mpf(20) for k in range(21)]
    D_vals = [D_func(wp) for wp in test_points]
    D_all_negative = all(d < 0 for d in D_vals)
    print(f"  D negative on [w-h,w+h]? {D_all_negative} (min D = {min(D_vals):.16e})")

# ============================================================================
# 5. PRIOR SUPPORT AND LEMMA 1 BANDS
# ============================================================================
print("\n" + "="*80)
print("THEOREM B LEFT ENDPOINT AND PRIOR SUPPORT")
print("="*80)

mu = g[10]
alpha = pi*K/T
wL = mu - alpha - h
w_prior_left = mu - alpha

print(f"\nmu = g[10] = {mu}")
print(f"alpha = pi*K/T = {alpha}")
print(f"wL = mu - alpha - h = {wL}")
print(f"w_prior_left = mu - alpha = {w_prior_left}")

Dstar_wL = Dstar_func(wL)
term_wL = 2*h*Dstar_wL
print(f"\nAt wL = {wL:.16e}:")
print(f"  Dstar(wL) = {Dstar_wL:.16e}")
print(f"  2*h*Dstar(wL) = {term_wL:.16e}")
print(f"  exp(2*h*Dstar(wL)) = {exp(term_wL):.16e}")
print(f"  F_flat_left = exp(-2*h*Dstar(wL)) = {exp(-term_wL):.16e}")

Dstar_prior = Dstar_func(w_prior_left)
term_prior = 2*h*Dstar_prior
print(f"\nAt w_prior_left = {w_prior_left:.16e}:")
print(f"  Dstar(w_prior_left) = {Dstar_prior:.16e}")
print(f"  2*h*Dstar(w_prior_left) = {term_prior:.16e}")
print(f"  exp(2*h*Dstar(w_prior_left)) = {exp(term_prior):.16e}")
print(f"  exp(-2*h*Dstar(w_prior_left)) = {exp(-term_prior):.16e}")

tone_d_band = g[10] - h
Dstar_tone_d = Dstar_func(tone_d_band)
term_tone_d = 2*h*Dstar_tone_d
print(f"\nAt tone-d band g[10]-h = {tone_d_band:.16e}:")
print(f"  Dstar(g[10]-h) = {Dstar_tone_d:.16e}")
print(f"  2*h*Dstar(g[10]-h) = {term_tone_d:.16e}")
print(f"  exp(2*h*Dstar(g[10]-h)) = {exp(term_tone_d):.16e}")
print(f"  exp(-2*h*Dstar(g[10]-h)) = {exp(-term_tone_d):.16e}")

# ============================================================================
# 6. ABEL-TYPE REMAINDER
# ============================================================================
print("\n" + "="*80)
print("ABEL-TYPE REMAINDER")
print("="*80)

g1_minus_h = g[1] - h
print(f"\nFor omega >= g[1] - h = {g1_minus_h:.16e}:")
print(f"Abel relative remainder 6*pi/(omega*T):")
print(f"  at omega = g[1]-h: {6*pi/(g1_minus_h*T):.16e}")
print(f"  at omega = g[10]: {6*pi/(g[10]*T):.16e}")

# ============================================================================
# 7. LEMMA 2 CONTINUOUS REMAINDER BOUNDS
# ============================================================================
print("\n" + "="*80)
print("LEMMA 2 CONTINUOUS REMAINDER BOUNDS")
print("="*80)

def compute_lemma2_bounds(omega, T_val):
    """Compute Lemma 2 remainder error bounds at omega."""
    e1_bound = T_val**2/(2*omega) + T_val/(2*omega**2) + 1/(4*omega**3)
    e2_bound = T_val/(2*omega) + 1/(4*omega**2)
    e3_bound = 1/(2*omega)
    return e1_bound, e2_bound, e3_bound

test_omegas = [g[1]-h, g[1], g[10]-h, g[10], mpf(12.0)]

print(f"\n{'omega':>20} {'e1_bound':>20} {'e2_bound':>20} {'e3_bound':>20}")
print("-" * 85)
for omega in test_omegas:
    e1, e2, e3 = compute_lemma2_bounds(omega, T)
    print(f"{omega:20.12e} {e1:20.12e} {e2:20.12e} {e3:20.12e}")

# ============================================================================
# 8. WINDOW CORRECTION C_WIN
# ============================================================================
print("\n" + "="*80)
print("WINDOW CORRECTION C_WIN ANALYSIS")
print("="*80)

print("\nInverse of 2x2 system (omega, phi):")
print(f"{'omega':>20} {'num_lo':>20} {'det_hi':>20} {'inv11_lo':>20} {'ratio':>15} {'deficit':>15} {'C_win':>20}")
print("-" * 135)

for omega in test_omegas:
    e1_bound, e2_bound, e3_bound = compute_lemma2_bounds(omega, T)
    
    num_lo = T/2 - e3_bound
    det_hi = (T**3/6 + e1_bound)*(T/2 + e3_bound) - (T**2/4 - e2_bound)**2
    
    if det_hi > 0:
        inv11_lo = num_lo / det_hi
        leading = 24 / T**3
        ratio = inv11_lo / leading
        deficit = 1 - ratio
        C_win_cont = deficit * omega * T
    else:
        inv11_lo = mpf('nan')
        leading = 24 / T**3
        ratio = mpf('nan')
        deficit = mpf('nan')
        C_win_cont = mpf('nan')
    
    print(f"{omega:20.12e} {num_lo:20.12e} {det_hi:20.12e} {inv11_lo:20.12e} {ratio:15.10f} {deficit:15.10f} {C_win_cont:20.12e}")

# ============================================================================
# 9. 3x3 SYSTEM WITH A COORDINATE
# ============================================================================
print("\n" + "="*80)
print("3x3 SYSTEM WITH A-COORDINATE (SIGN ANALYSIS)")
print("="*80)

import itertools

def compute_3x3_inverse_sample(omega, T_val, e1_bound, e2_bound, e3_bound):
    """
    Compute inverse of 3x3 with A, omega, phi coordinates.
    Try all 2^6=64 sign combinations of error bounds.
    Return max deficit in ratio to 24/T^3.
    """
    signs_list = list(itertools.product([-1, 1], repeat=6))
    max_ratio = mpf(0)
    
    for s_e1, s_e2_om, s_e2_phi, s_e3, s_Aom, s_Aphi in signs_list:
        # Build 3x3 matrix entries with signs
        # Main diagonal: AA, omegaomega, phiphi
        AA_lo = T_val/2 - s_e3*e3_bound
        AA_hi = T_val/2 + s_e3*e3_bound
        om_om_lo = T_val**3/6 - s_e1*e1_bound
        om_om_hi = T_val**3/6 + s_e1*e1_bound
        phi_phi_lo = T_val/2 - s_e3*e3_bound
        phi_phi_hi = T_val/2 + s_e3*e3_bound
        
        # Off-diagonal bounds
        A_om_bound = s_e2_om*e2_bound  # |int t sin cos| ~ |int t sin^2|
        A_phi_bound = s_Aphi*e3_bound   # |int cos sin|
        om_phi_bound = T_val**2/4 - s_e2_phi*e2_bound  # |int t^2 sin cos| ~ |int t^2 sin^2| upper
        
        # Try worst-case to maximize denominator effect
        # Use mid-range values for a rough check
        AA_use = T_val/2
        om_om_use = T_val**3/6 + e1_bound
        phi_phi_use = T_val/2 + e3_bound
        A_om_use = T_val/(2*omega) + 1/(4*omega**2)
        A_phi_use = 1/(2*omega)
        om_phi_use = T_val**2/4 - e2_bound
        
        try:
            import numpy as np
            M = np.array([
                [float(AA_use), float(A_om_use), float(A_phi_use)],
                [float(A_om_use), float(om_om_use), float(om_phi_use)],
                [float(A_phi_use), float(om_phi_use), float(phi_phi_use)]
            ], dtype=np.float64)
            
            det_M = np.linalg.det(M)
            if det_M > 0:
                M_inv = np.linalg.inv(M)
                inv_om_om = M_inv[1, 1]
                leading = 24 / float(T_val)**3
                ratio = inv_om_om / leading
                if ratio > max_ratio:
                    max_ratio = mpf(str(ratio))
        except:
            pass
    
    return max_ratio

print("\n3x3 inverse ωω vs 24/T^3 (sampling all sign combos):")
print(f"{'omega':>20} {'max(ratio)':>15} {'max(deficit)':>15}")
print("-" * 55)

for omega in test_omegas:
    e1_bound, e2_bound, e3_bound = compute_lemma2_bounds(omega, T)
    max_ratio = compute_3x3_inverse_sample(omega, T, e1_bound, e2_bound, e3_bound)
    max_deficit = 1 - max_ratio
    print(f"{omega:20.12e} {max_ratio:15.10f} {max_deficit:15.10f}")

# ============================================================================
# 10. DISCRETE GRAM (NYQUIST SAMPLING)
# ============================================================================
print("\n" + "="*80)
print("DISCRETE GRAM ANALYSIS")
print("="*80)

n = int(ceil(2*Omega*T/pi))
Delta = T / n
print(f"\nNyquist-and-a-half sampling:")
print(f"  n = ceil(2*Omega*T/pi) = {n}")
print(f"  Delta = T/n = {Delta:.16e}")

sum_t2 = (T/n)**2 * n*(n-1)*(2*n-1)/6
sum_t = (T/n)*n*(n-1)/2

print(f"  sum(t_k^2) = {sum_t2:.16e}")
print(f"  sum(t_k) = {sum_t:.16e}")
print(f"  n_samples = {n}")

print(f"\n{'omega':>15} {'omega*Delta':>20} {'sin(omega*Delta)':>20}")
print("-" * 60)
for omega in [Omega, g[10]]:
    omega_delta = omega * Delta
    sin_val = sin(omega_delta)
    print(f"{omega:15.10f} {omega_delta:20.16e} {sin_val:20.16e}")

# ============================================================================
# 11. RIESZ QUADRATURE (HIGH-PRECISION INTEGRATION)
# ============================================================================
print("\n" + "="*80)
print("EXACT RIESZ QUADRATURE (scipy.quad)")
print("="*80)

def a_func(w):
    """a(w) = 1/sqrt((w^2+0.25)*(w^2+2.25))"""
    return 1.0 / np.sqrt((w**2 + 0.25)*(w**2 + 2.25))

def a_mpmath(w):
    """High-precision version"""
    return 1/sqrt((w**2 + mpf(0.25))*(w**2 + mpf(2.25)))

def integrand_sig2(w, Gamma):
    """a(w)^2 * log(w/(2*pi))"""
    a_w = a_func(w)
    return a_w**2 * np.log(w / (2*np.pi))

def integrand_rho(w, Gamma):
    """a(w)^3 * log(w/(2*pi))"""
    a_w = a_func(w)
    return a_w**3 * np.log(w / (2*np.pi))

# Use scipy.quad with high precision
print("\nRiesz quadrature at Gamma = GAMMA_OP = 51.23362034:")

try:
    sig2_R_integrand = lambda w: integrand_sig2(w, float(GAMMA_OP))
    sig2_R_result, sig2_R_err = scipy_quad(sig2_R_integrand, float(GAMMA_OP), np.inf, 
                                            epsabs=1e-14, epsrel=1e-12, limit=100)
    sig2_R = mpf(sig2_R_result) / pi
    
    rho_R_integrand = lambda w: integrand_rho(w, float(GAMMA_OP))
    rho_R_result, rho_R_err = scipy_quad(rho_R_integrand, float(GAMMA_OP), np.inf,
                                          epsabs=1e-14, epsrel=1e-12, limit=100)
    rho_R = (mpf(16)/(3*pi**2)) * mpf(rho_R_result)
    
    a_Gamma = a_func(float(GAMMA_OP))
    Lambda_R = 2 * a_Gamma**2 / float(sig2_R)
    
    print(f"  sig2_R = {sig2_R:.16e}")
    print(f"  Lambda_R = 2*a(Gamma)^2 / sig2_R = {Lambda_R:.16e}")
    print(f"  rho_R = {rho_R:.16e}")
    print(f"  dK_R = 0.56 * rho_R / sig2_R^1.5 = {0.56 * float(rho_R) / float(sig2_R)**1.5:.16e}")
except Exception as e:
    print(f"  Riesz integration error: {e}")

print("\nRiesz quadrature at Gamma = 50 (cross-check):")
try:
    Gamma_50 = mpf(50)
    sig2_R_50_integrand = lambda w: integrand_sig2(w, 50)
    sig2_R_50_result, sig2_R_50_err = scipy_quad(sig2_R_50_integrand, 50, np.inf,
                                                   epsabs=1e-14, epsrel=1e-12, limit=100)
    sig2_R_50 = mpf(sig2_R_50_result) / pi
    
    rho_R_50_integrand = lambda w: integrand_rho(w, 50)
    rho_R_50_result, rho_R_50_err = scipy_quad(rho_R_50_integrand, 50, np.inf,
                                                epsabs=1e-14, epsrel=1e-12, limit=100)
    rho_R_50 = (mpf(16)/(3*pi**2)) * mpf(rho_R_50_result)
    
    a_50 = a_func(50)
    Lambda_R_50 = 2 * a_50**2 / float(sig2_R_50)
    
    print(f"  sig2_R = {sig2_R_50:.16e}")
    print(f"  Lambda_R = {Lambda_R_50:.16e}")
    print(f"  rho_R = {rho_R_50:.16e}")
except Exception as e:
    print(f"  Riesz integration error: {e}")

print("\nLambda_as at Gamma = 50 (cross-check):")
Lambda_as_50 = 6*pi/(50*(log(mpf(50)/(2*pi)) + mpf(1)/mpf(3)))
print(f"  Lambda_as(50) = 6*pi/(50*(log(50/(2*pi))+1/3)) = {Lambda_as_50:.16e}")

# ============================================================================
# 12. RMSE AND COLOURED INVERSE
# ============================================================================
print("\n" + "="*80)
print("RMSE AND COLOURED INVERSE")
print("="*80)

coloured_inverse_ref = mpf('0.993916700836')
RMSE_old = mpf('0.04932816')
RMSE_current = RMSE_old * sqrt(coloured_inverse_ref)

print(f"\nColoured inverse (referee): {coloured_inverse_ref:.16e}")
print(f"RMSE coefficient: {RMSE_old:.16e}")
print(f"RMSE = 0.04932816 * sqrt(coloured_inverse) = {RMSE_current:.16e}")

print(f"\nLocal RMSE with full L_d (using gamma10):")
L_d_full = log(gamma10/(2*pi))
local_RMSE_full = sqrt(6*L_d_full) / T_15
print(f"  L_d = {L_d_full:.16e}")
print(f"  local_RMSE = sqrt(6*L_d)/T^1.5 = {local_RMSE_full:.16e}")

L_d_truncated = mpf('2.06961231767041')
local_RMSE_truncated = sqrt(6*L_d_truncated) / T_15
print(f"\nLocal RMSE with truncated L_d = 2.06961231767041:")
print(f"  local_RMSE = sqrt(6*L_d)/T^1.5 = {local_RMSE_truncated:.16e}")

# ============================================================================
# 13. F_WIN AND SUPPORT-UNIFORM
# ============================================================================
print("\n" + "="*80)
print("F_WIN TONES AND SUPPORT-UNIFORM")
print("="*80)

# Compute worst-case C_win (max over omega >= g[1]-h)
print("\nF_win at each tone (using worst-case C_win):")
print(f"{'j':>3} {'g[j]':>20} {'1 - C_win/(g[j]*T)':>25}")
print("-" * 50)

C_win_max = mpf(0)  # Track worst case
for omega in [g[1]-h, g[1], g[10]-h, g[10], mpf(12.0)]:
    if omega > 0:
        e1, e2, e3 = compute_lemma2_bounds(omega, T)
        num_lo = T/2 - e3
        det_hi = (T**3/6 + e1)*(T/2 + e3) - (T**2/4 - e2)**2
        if det_hi > 0:
            inv11_lo = num_lo / det_hi
            leading = 24 / T**3
            ratio = inv11_lo / leading
            deficit = 1 - ratio
            C_win_omega = deficit * omega * T
            if C_win_omega > C_win_max:
                C_win_max = C_win_omega

for j in [1, 2, 3, 4, 5, 10]:
    F_win_j = 1 - C_win_max / (g[j] * T)
    print(f"{j:3d} {g[j]:20.12e} {F_win_j:25.16e}")

print(f"\nSupport-uniform F_win:")
print(f"  mu = g[10] = {mu:.16e}")
print(f"  mu - alpha = {w_prior_left:.16e}")
print(f"  F_win_uniform = 1 - C_win/((mu-alpha)*T) = {1 - C_win_max/(w_prior_left*T):.16e}")

# ============================================================================
# 14. MISCELLANEOUS CONSTANTS
# ============================================================================
print("\n" + "="*80)
print("MISCELLANEOUS CONSTANTS AND COMPARISONS")
print("="*80)

term_16pi = 16*pi*K/T
print(f"\n16*pi*K/T = {term_16pi:.16e}")

# Old exponential (if available)
old_exp_term = exp(16*pi*K/(gamma10*T))
print(f"Old: exp(16*pi*K/(gamma10*T)) = {old_exp_term:.16e}")

print(f"\nr_d = 6*L_d/(K^2*T):")
r_d = 6*L_d / (K**2 * T)
print(f"  r_d = {r_d:.16e}")
print(f"  sqrt(6)/sqrt(1+r_d) = {sqrt(mpf(6))/sqrt(1+r_d):.16e}")

# ============================================================================
# 15. D' MONOTONICITY
# ============================================================================
print("\n" + "="*80)
print("D'(w) MONOTONICITY CHECK")
print("="*80)

print(f"\nD'(w) at selected points:")
print(f"{'w':>20} {'D\\'(w)':>25}")
print("-" * 50)

test_w_values = [g[1]-h, mpf(12), mpf(14), mpf(20), mpf(48), mpf(50), mpf(52)]
for w_test in test_w_values:
    dp_val = Dp_func(w_test)
    print(f"{w_test:20.12e} {dp_val:25.16e}")

# Check monotonicity on [g[1]-h, g[10]+h]
print(f"\nMonotonicity check on [g[1]-h, g[10]+h]:")
g1_minus_h = g[1] - h
g10_plus_h = g[10] + h
print(f"  Interval: [{g1_minus_h:.12e}, {g10_plus_h:.12e}]")

sample_points = [g1_minus_h + (g10_plus_h - g1_minus_h)*mpf(k)/mpf(49) for k in range(50)]
Dp_vals = [Dp_func(wp) for wp in sample_points]
min_Dp = min(Dp_vals)
max_Dp = max(Dp_vals)

print(f"  min D'(w) over 50 sample points: {min_Dp:.16e}")
print(f"  max D'(w) over 50 sample points: {max_Dp:.16e}")
print(f"  D' > 0 throughout? {min_Dp > 0}")

print("\n" + "="*80)
print("END OF HIGH-PRECISION COMPUTATION")
print("="*80)
