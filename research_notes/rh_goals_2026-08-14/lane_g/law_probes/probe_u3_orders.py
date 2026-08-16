#!/usr/bin/env python3
"""Probe U3 — divisor orders of det Phi_theta at the two points the transport uses.

NON-RIGOROUS (mpmath, 40 dps, no interval arithmetic).  Confirms statements that
are PROVED in closed form in LAW_U3_TRANSPORT.md sections 3.2-3.3; nothing here
is load-bearing.

Checks
  (1) det Phi_theta has a pole of order exactly 2 at s_inf = rho_1/2.
  (2) det Phi_theta has a ZERO of order exactly 2 at 1 - conj(s_inf) = (1+rho_1)/2
      -- this is the point the Hejhal/Bruggeman-Fraczek-Mayer form of the divisor
      theorem refers to, so it is checked directly and the "phi is real on R"
      step is never needed.
  (3) The elementary factor E is finite and non-zero at both points.
  (4) Side check: the poles of E on Re s = 0 are SIMPLE (corrects the
      "order 2 in E" remark of LAW_ANCHOR_T1_THETA.md section 4.4;
      non-load-bearing).

Run:  /usr/bin/python3 probe_u3_orders.py     (system python3 has mpmath)
"""

from mpmath import mp, mpf, gamma, zeta, pi, power, zetazero, log

mp.dps = 40


def Lam(w):
    """Completed Riemann zeta  Lambda(w) = pi^{-w/2} Gamma(w/2) zeta(w)."""
    return power(pi, -w / 2) * gamma(w / 2) * zeta(w)


def g(s):
    """g(s) = Lambda(2s-1)/Lambda(2s)  = sqrt(pi) Gamma(s-1/2) zeta(2s-1)
                                          / (Gamma(s) zeta(2s))."""
    return Lam(2 * s - 1) / Lam(2 * s)


def E(s):
    """Elementary factor of det Phi_theta, in X = 2^s:
       E = -(X-2)(X+2) / ( X^2 (X-1)(X+1) )  =  (4 - 4^s)/(4^s (4^s - 1))."""
    X = power(2, s)
    return -(X - 2) * (X + 2) / (X ** 2 * (X - 1) * (X + 1))


def det_phi(s):
    """(DET) of LAW_ANCHOR_T1_THETA.md:  det Phi_theta = g(s)^2 E(s)."""
    return g(s) ** 2 * E(s)


def main():
    rho1 = zetazero(1)
    s_inf = rho1 / 2
    w = 1 - mp.conj(s_inf)          # = (1 + rho1)/2, since Re rho1 = 1/2

    print("rho_1            =", rho1)
    print("s_inf = rho_1/2  =", s_inf)
    print("1 - conj(s_inf)  =", w)
    print("(1 + rho_1)/2    =", (1 + rho1) / 2)

    print("\n(1) pole at s_inf:  (s - s_inf)^2 * det Phi_theta")
    for k in range(3, 8):
        r = mpf(10) ** (-k)
        print("    r=1e-%d  %s" % (k, mp.nstr(r ** 2 * det_phi(s_inf + r), 10)))

    print("\n(2) zero at 1-conj(s_inf):  det Phi_theta / (s - w)^2")
    for k in range(3, 8):
        r = mpf(10) ** (-k)
        print("    r=1e-%d  %s" % (k, mp.nstr(det_phi(w + r) / r ** 2, 10)))

    print("\n(3) E finite and non-zero at both points")
    print("    E(s_inf) =", mp.nstr(E(s_inf), 10))
    print("    E(w)     =", mp.nstr(E(w), 10))

    print("\n(4) side check: order of the poles of E on Re s = 0")
    for label, s0 in (("X=-1, k=1", 1j * pi / log(2)),
                      ("X=+1, k=2", 2j * pi / log(2))):
        print("    %s  s0 = %s" % (label, mp.nstr(s0, 12)))
        for k in (3, 5, 7):
            r = mpf(10) ** (-k)
            print("      r=1e-%d  r*E = %s   r^2*E = %s"
                  % (k, mp.nstr(r * E(s0 + r), 8), mp.nstr(r ** 2 * E(s0 + r), 8)))
        print("      g(s0) = %s  (finite, non-zero)" % mp.nstr(g(s0), 8))


if __name__ == "__main__":
    main()
