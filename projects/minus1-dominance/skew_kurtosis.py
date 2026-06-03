"""
Is the RS distribution of D_a = mu + sum_k A_k cos(theta_k) SKEWED?

Each term A cos(theta), theta~Uniform(0,2pi), is SYMMETRIC about 0 (cos(theta) and
cos(theta+pi)=-cos(theta) equiprobable). Sum of independent symmetric r.v.s is
symmetric. So D_a - mu is SYMMETRIC => skewness = 0 EXACTLY.

THEREFORE the discriminator among non-residues is NOT skew. The CRUX subtlety's
"non-Gaussian SKEW" hypothesis is FALSE for the a-vs-1 race in the standard RS
model (where the mean is the only asymmetry, and it ties across NR). The non-
Gaussianity is in the KURTOSIS / tail shape (4th+ cumulants), which is SYMMETRIC.

But kurtosis at FIXED variance shifts P(D>0) only at second order and SYMMETRICALLY
in the tails -- it does NOT create a systematic ordering by itself the way variance
does. Confirm numerically: compare two symmetric laws, same mean & variance,
different kurtosis -> delta barely moves; whereas changing variance moves it a lot.
"""
import mpmath as mp
mp.mp.dps = 25

def gilpelaez(m, amps, XI=100):
    def phi(xi):
        v=mp.e**(1j*xi*m)
        for A in amps: v*=mp.besselj(0,A*xi)
        return v
    return float(0.5+mp.quad(lambda xi: mp.im(phi(xi))/xi,[0,XI])/mp.pi)

# moments of D = sum A_k cos(theta_k): E=0; Var=sum A^2/2; 3rd central=0 (symmetric);
# excess kurtosis depends on concentration of amplitudes.
m=-2.0
print("Fixed mean=-2.  Compare variance effect vs kurtosis effect:")
# Case A: one big cosine (very leptokurtic/platykurtic), variance V
A=mp.sqrt(2*12); print(f"  1 cosine, V=12: delta={gilpelaez(m,[A]):.5f}  (kurtosis extreme)")
# Case B: many small cosines, SAME variance V=12 (-> approaches Gaussian)
K=200; A2=mp.sqrt(2*12/K); print(f"  {K} cosines, V=12: delta={gilpelaez(m,[A2]*K):.5f}  (near-Gaussian)")
import math
print(f"  Gaussian V=12: delta={float(mp.ncdf(m/mp.sqrt(12))):.5f}")
print("  --> at FIXED variance, kurtosis/shape changes delta only slightly.")
print()
print("Now vary variance (shape fixed, many cosines):")
for V in [8,12,20,40]:
    K=100;A=mp.sqrt(2*V/K)
    print(f"  V={V:4.1f}: delta={gilpelaez(m,[A]*K):.5f}")
print("  --> variance is the DOMINANT lever. Confirms: -1 leads via MAX VARIANCE.")
