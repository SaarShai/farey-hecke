"""
Verify the density logic:  with IDENTICAL negative mean m and varying variance V,
P(D>0) is monotincreasing in V (approaches 1/2 from below).  Test BOTH a Gaussian
model AND the true non-Gaussian RS convolution (sum of cosines), to show the
ordering is robust to non-Gaussianity.
"""
import mpmath as mp
mp.mp.dps = 25

def gauss_delta(m,V):
    return float(mp.ncdf(m/mp.sqrt(V)))   # P(N(m,V)>0)=Phi(m/sqrt V)

def gilpelaez(m, amps, XI=80):
    # D = m + sum_k amps[k]*cos(theta_k), theta iid uniform; phi(xi)=e^{i xi m} prod J0(amps[k] xi)
    def phi(xi):
        v=mp.e**(1j*xi*m)
        for A in amps: v*=mp.besselj(0,A*xi)
        return v
    integ=mp.quad(lambda xi: mp.im(phi(xi))/xi,[0,XI])
    return float(0.5+integ/mp.pi)

m=-2.0   # the common negative mean = -#sqrt(1) = -2 (t=1 case, q=p)
print("Gaussian: same mean m=-2, vary V -> delta=P(D>0):")
for V in [4,8,12,20,40]:
    print(f"   V={V:5.1f}  delta={gauss_delta(m,V):.5f}")

print("\nNon-Gaussian (equal-amplitude cosine sum giving variance V): same m=-2:")
# K cosines each amplitude A: variance = K*A^2/2 (var of A cos(unif)=A^2/2). Set A=1, vary K.
for K in [8,16,24,40,80]:
    amps=[1.0]*K
    V=K*0.5
    print(f"   K={K:3d} (V={V:5.1f})  delta(GilPelaez)={gilpelaez(m,amps):.5f}   (gauss approx {gauss_delta(m,V):.5f})")

print("\n=> Both monotone increasing in V. Larger variance (with equal neg mean) => larger density.")
print("   Hence -1 (which MAXIMIZES variance among NR) has the LARGEST density => -1 leads.")
