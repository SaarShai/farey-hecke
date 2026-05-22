#!/usr/bin/env python3
"""Character-sum sanity check for Koyama identity (3.1).

(Z/11)* is cyclic of order 10. Primitive root g=2. Index ind_g(a) defined.
Characters: chi_k(a) = exp(2*pi*i * k * ind(a) / 10), k=0..9.

Identity verified:
  pi(x;N,a) - pi(x;N,1) = (1/phi(N)) * sum_{chi mod N} (chi(a)^{-1} - 1) * S(chi)
where S(chi) = sum_{p<=x} chi(p) = sum_{r in (Z/N)*} c[r] * chi(r).
"""
import cmath, math

c11 = {1:44583143398, 2:44583148725, 3:44583127498, 4:44583198117, 5:44583129618,
       6:44583173801, 7:44583150749, 8:44583218236, 9:44583165567, 10:44583154901}
N = 11
phi = 10
# primitive root: 2 mod 11
g = 2
ind = {}
v = 1
for k in range(phi):
    ind[v] = k
    v = (v * g) % N
# verify
assert sorted(ind) == list(range(1,11)), ind

def chi(k, a):
    return cmath.exp(2j * math.pi * k * ind[a] / phi)

def S(k):
    return sum(c11[r] * chi(k, r) for r in range(1, N))

# Identity check for each residue a
print(f"{'a':>3} {'direct':>10} {'character_sum':>22}")
for a in range(1, N):
    direct = c11[a] - c11[1]
    chsum = sum((chi(k, a).conjugate() - 1) * S(k) for k in range(phi)) / phi
    print(f"{a:>3d} {direct:>10d} {chsum.real:>22.6f}  imag={chsum.imag:.2e}")
