"""
Compute delta(q; a, 1) = P(X_a > X_1) for the RS limiting distribution, via the
EXACT characteristic function (RS Fourier method) -- NOT a Gaussian approximation.

The random variable of interest is  D_a := X_a - X_1.
From the explicit-formula representation, each zero gamma of L(s,chi) (chi != chi0)
contributes an INDEPENDENT term (under LI). Grouping the real & conjugate parts,
the standard RS result (their eq. (3.1)-(3.3)) is that D_a has characteristic
function

  E[ exp(i xi D_a) ] = exp(i xi (mu_a - mu_1)) * prod_{gamma>0 over all chi!=chi0}
        J0( 2 |alpha_gamma(a)| xi / sqrt(1/4+gamma^2) )

where for each chi and each zero gamma_chi>0, the per-frequency real amplitude is
  alpha_gamma(a) = (chi(a) - chi(1)) = chi(a) - 1   (coefficient of that zero in D_a),
and J0 is the Bessel function of order 0 (the char. function of one term
A*cos(theta), theta uniform, is J0(A xi)). The factor sqrt(1/4+gamma^2)=|rho|.

CRUCIAL: the |.| means amplitudes from chi and conj(chi) (which share |gamma|) must
be combined as a single 2D random phase, giving amplitude
  |chi(a)-1| * 2/sqrt(1/4+gamma^2)  per zero gamma>0 of chi
(each conjugate pair {chi, bar chi} sharing the same |gamma| -> a single J0 with
the modulus). For a REAL (quadratic) chi, chi=bar chi, and chi(a)-1 in {-2,0}.

So the variance of D_a is  Var = sum_{chi} c_chi |chi(a)-1|^2  (matches recipe), and
the FULL distribution is the convolution of the per-zero arcsine (cosine) laws ->
NON-GAUSSIAN, with the non-Gaussianity strongest when one chi dominates c_chi.

We invert:  P(D_a>0) = 1/2 + (1/pi) ∫_0^inf Im( phi_D(xi) ) / xi  dxi  (Gil-Pelaez),
where phi_D(xi) = E[e^{i xi D_a}].

INPUTS NEEDED:  the zeros gamma_chi for each chi != chi0 (to form the J0 product),
OR -- as RS do for moderate accuracy -- the variance c_chi per chi plus a small
number of explicit low zeros and a Gaussian/Edgeworth tail for the rest.

This script provides BOTH:
  (A) exact Gil-Pelaez inversion using an explicit list of low zeros per chi
      and a Gaussian factor exp(-xi^2 sigma_tail^2/2) for the high-zero tail;
  (B) a pure-Gaussian baseline (mean mu_a-mu_1, variance Var) to MEASURE the
      non-Gaussian correction -- this is how we test whether skew/kurtosis (not
      mean, not variance alone) is what separates -1 from other NR.
"""
import mpmath as mp
mp.mp.dps = 30
import math

def gauss_delta(mu_diff, var):
    # P(D>0) for D~Normal(mu_diff, var)
    return float(mp.ncdf(mu_diff/mp.sqrt(var)))

def gilpelaez_delta(mu_diff, zero_amps, sigma_tail2=0.0, XI=60, n=4000):
    """zero_amps: list of per-(chi,gamma>0) amplitudes A = |chi(a)-1| * 2/sqrt(1/4+gamma^2).
       phi_D(xi)=exp(i xi mu_diff) * exp(-xi^2 sigma_tail2/2) * prod J0(A xi).
       Returns P(D_a>0)."""
    def phi(xi):
        val = mp.e**(1j*xi*mu_diff) * mp.e**(-xi**2*sigma_tail2/2)
        for A in zero_amps:
            val *= mp.besselj(0, A*xi)
        return val
    # Gil-Pelaez: P(D>0)=1/2 + 1/pi ∫_0^∞ Im(phi(xi))/xi dxi
    integ = mp.quad(lambda xi: mp.im(phi(xi))/xi, [0, XI])
    return float(mp.mpf('0.5') + integ/mp.pi)

if __name__ == "__main__":
    # smoke test: symmetric single cosine term -> should give 1/2 (mu=0)
    print("smoke (mu=0, one zero): ", gilpelaez_delta(0.0,[1.0]))
    print("smoke (mu=0, gauss tail only): ", gilpelaez_delta(0.0,[],sigma_tail2=1.0))
    print("gauss baseline (mu=0.5,var=1):", gauss_delta(0.5,1.0))
