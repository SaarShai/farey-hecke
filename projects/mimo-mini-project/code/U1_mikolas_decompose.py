"""U1: Direct Mikolás decomposition of J(Q).

Identity:
  J(Q) = (1/(2π²)) · Σ_{m=1}^∞ |S_Q(m)|² / m²
where S_Q(m) = Σ_{q=1}^Q c_q(m) and c_q(m) is the Ramanujan sum:
  c_q(m) = Σ_{a=1, gcd(a,q)=1}^q e^{2πima/q} = Σ_{d | gcd(m,q)} d·μ(q/d)

Note c_q(1) = μ(q), so S_Q(1) = M(Q).

Goal: for small Q (say 500-5000), compute the m=1 term, m≥2 term, and total.
Verify total matches stream_J output. Test claim: does Σ_{m≥2} term
contribute the constant C - (avg of M²/(2π²)·Q/Φ ≈ 1/6)?

Theory predicts:
  NW(Q) = (π²/3Q)·(1/(2π²))·Σ |S_Q(m)|²/m² · Q
        = (1/(6Q)) · Σ_m |S_Q(m)|²/m²
        + lower order corrections

So m=1 contributes M(Q)²/(6Q). What does m≥2 contribute?
"""
import math
import sys


def sieve_mobius(N):
    mu = [1] * (N + 1)
    mu[0] = 0
    is_prime = [True] * (N + 1)
    is_prime[0] = is_prime[1] = False
    for p in range(2, N + 1):
        if is_prime[p]:
            for j in range(p, N + 1, p):
                if j > p: is_prime[j] = False
                mu[j] = -mu[j]
            for j in range(p * p, N + 1, p * p):
                mu[j] = 0
    return mu


def ramanujan_sum(q, m, mu):
    """c_q(m) = Σ_{d | gcd(q,m)} d · μ(q/d)"""
    g = math.gcd(q, m)
    s = 0
    d = 1
    while d * d <= g:
        if g % d == 0:
            s += d * mu[q // d]
            if d * d != g:
                d2 = g // d
                s += d2 * mu[q // d2]
        d += 1
    return s


def S_Q(Q, m, mu):
    """Σ_{q=1}^Q c_q(m)."""
    return sum(ramanujan_sum(q, m, mu) for q in range(1, Q + 1))


def euler_phi_sum(Q, mu):
    """Φ(Q) = Σ_{q=1}^Q φ(q) using μ * id."""
    # φ(q) = q · Σ_{d|q} μ(d)/d, summing is heavy.
    # Direct sieve:
    phi = list(range(Q + 1))
    for p in range(2, Q + 1):
        if phi[p] == p:  # p is prime
            for j in range(p, Q + 1, p):
                phi[j] -= phi[j] // p
    return sum(phi[1:Q+1])


def main():
    Q = int(sys.argv[1]) if len(sys.argv) > 1 else 500
    M_max = int(sys.argv[2]) if len(sys.argv) > 2 else 20000

    mu = sieve_mobius(Q + 1)
    M_Q = sum(mu[1:Q+1])
    Phi_Q = euler_phi_sum(Q, mu)
    print(f"Q={Q}, M(Q)={M_Q}, Φ(Q)={Phi_Q}")

    # Compute |S_Q(m)|²/m² for m = 1 to M_max
    s1 = S_Q(Q, 1, mu)
    assert s1 == M_Q, f"S_Q(1) should equal M(Q), got {s1} vs {M_Q}"
    print(f"S_Q(1) = M(Q) = {M_Q} ✓")

    sum_m1 = (s1 * s1) / 1
    sum_m_ge2 = 0.0
    sum_all = sum_m1

    # Track contributions per decade
    decades = {1: 0.0, 10: 0.0, 100: 0.0, 1000: 0.0, 10000: 0.0}
    for m in range(2, M_max + 1):
        s = S_Q(Q, m, mu)
        contrib = (s * s) / (m * m)
        sum_m_ge2 += contrib
        sum_all += contrib
        for dec in decades:
            if m <= dec * 10 and m > dec:
                decades[dec] += contrib

    J_estimated = sum_all / (2 * math.pi**2)
    NW_estimated = Q * J_estimated / Phi_Q

    m1_NW_contrib = (M_Q * M_Q) / (6 * Q)  # = m=1 part of NW under leading-order approx
    print()
    print(f"Σ_m |S_Q(m)|²/m² split:")
    print(f"  m=1     : {sum_m1:.4f}   ({sum_m1/sum_all*100:.1f}%)")
    print(f"  m≥2     : {sum_m_ge2:.4f}   ({sum_m_ge2/sum_all*100:.1f}%)")
    print(f"  Total   : {sum_all:.4f}")
    print()
    print(f"J(Q) estimated  = {J_estimated:.6f}")
    print(f"NW(Q) estimated = Q·J(Q)/Φ(Q) = {NW_estimated:.6f}")
    print(f"  (using m up to {M_max}; truncation likely positive error)")
    print()
    print(f"Decade contributions to Σ:")
    for dec, c in decades.items():
        print(f"  m ∈ ({dec}, {dec*10}]: {c:.4f}")
    print()
    print(f"m=1 only NW contribution (leading): M²/(6Q) = {m1_NW_contrib:.6f}")
    print(f"Implied m≥2 contribution to NW:    {NW_estimated - m1_NW_contrib:.6f}")
    print(f"Should approach C = 0.66989 (asymptote) for large Q.")


if __name__ == "__main__":
    main()
