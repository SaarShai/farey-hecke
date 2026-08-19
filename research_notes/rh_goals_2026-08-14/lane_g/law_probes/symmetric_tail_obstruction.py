"""Arb receipt for the proposed symmetric Route-B reflection.

This is a read-only diagnostic.  It evaluates the theta entry used by the
Route-B notes, its reflected product, and the exact lower bound forced on the
left-side error by the finite-group functional equation.  The final
harmonic-measure number is geometry-only; it is not a transport certificate.
"""

from flint import acb, arb, ctx


ctx.dps = 120


def phi_infty(s: acb) -> acb:
    """The theta (infinity,infinity) entry used in the RATE notes."""

    half = acb("0.5")
    return (
        acb.pi().sqrt()
        * (s - half).gamma()
        * (2 * s - acb(1)).zeta()
        / (s.gamma() * (2 * s).zeta() * (acb(4) ** s - acb(1)))
    )


def vertical_harmonic_measure(x: arb, L: arb, H: arb, nmax: int = 401):
    """Arb enclosure of midpoint harmonic measure of the right side.

    The odd separated-variables series is summed through nmax.  The returned
    interval adds an absolute geometric tail bound, so alternating signs are
    not used as an unverified cancellation.
    """

    total = arb(0)
    for n in range(1, nmax + 1, 2):
        sign = 1 if ((n - 1) // 2) % 2 == 0 else -1
        total += (
            arb(4)
            / (n * arb.pi())
            * (n * arb.pi() * x / H).sinh()
            / (n * arb.pi() * L / H).sinh()
            * sign
        )

    a = arb.pi() * (L - x) / H
    denominator = 1 - (-2 * arb.pi() * L / H).exp()
    n0 = nmax + 2
    tail = (
        arb(4)
        / (arb.pi() * n0)
        * (-n0 * a).exp()
        / (denominator * (1 - (-2 * a).exp()))
    )
    return total - tail, total + tail, tail


def main() -> None:
    one = acb(1)
    t0 = (acb.zeta_zero(1) / 2).imag
    sigma_r = arb("1.5")
    s_r = acb(sigma_r, t0)
    s_l = one - s_r.conjugate()
    phi_r = phi_infty(s_r)
    phi_l = phi_infty(s_l)

    # The p=3 endpoint candidate from LAW_EFFECTIVE_TAIL_COVER_SOL, evaluated
    # independently from its displayed formula at this fixed right point.
    delta = arb("2.38")
    s_vertical = (sigma_r**2 + (t0.real + delta) ** 2).sqrt()
    c4 = arb(2) ** 62 + 1
    c1 = arb(128) * (1 + arb(2).log())
    a_coeff = arb(12) * arb.pi() ** 2 * (s_vertical + 1) * c4
    b_coeff = arb(12) * c1
    q_endpoint = arb("31951437654668744792")
    e_endpoint = q_endpoint ** (-2) * (
        a_coeff * (q_endpoint.log() + 5 + 65 / q_endpoint) + b_coeff
    )

    theta_product = phi_r * phi_l.conjugate()
    r = acb(2) ** s_r - acb(2) ** (one - s_r)
    exact_product = 1 / (1 - r * r)
    defect = 1 / phi_r.conjugate() - phi_l
    phi_q_right_floor = abs(phi_r) - e_endpoint
    reciprocal_correction = e_endpoint / (abs(phi_r) * phi_q_right_floor)
    left_floor = abs(defect) - reciprocal_correction

    print("t0=", t0)
    print("sR=", s_r)
    print("sL=", s_l)
    print("phiR_abs_lower=", abs(phi_r).lower())
    print("phiR_abs_upper=", abs(phi_r).upper())
    print("theta_product=", theta_product)
    print("theta_product_minus_1_abs_lower=", abs(theta_product - one).lower())
    print("theta_product_minus_exact_abs_upper=", abs(theta_product - exact_product).upper())
    print("D_theta_reflection_abs_lower=", abs(defect).lower())
    print("S_vertical_upper=", s_vertical.upper())
    print("q_endpoint=", q_endpoint)
    print("E_endpoint_upper=", e_endpoint.upper())
    print("phi_q_right_floor_lower=", phi_q_right_floor.lower())
    print("reciprocal_correction_upper=", reciprocal_correction.upper())
    print("F_left_floor_lower=", left_floor.lower())
    print("F_left_over_E_lower=", (left_floor / e_endpoint).lower())

    # zeta(2s) removes the zeta-denominator pole of phi_infty, but the
    # rational factor 4^s-1 has an uncancelled pole inside this full symmetric
    # rectangle at s = 2*pi*i/log(2).  The residue below is for
    # H(s)=sqrt(pi)*Gamma(s-1/2)*zeta(2s-1)/(Gamma(s)*(4^s-1)).
    pole_t = (2 * acb.pi() / acb(2).log()).real
    pole_s = acb(arb(0), pole_t)
    pole_residue = (
        acb.pi().sqrt()
        * (pole_s - acb("0.5")).gamma()
        * (2 * pole_s - acb(1)).zeta()
        / (pole_s.gamma() * acb(4).log())
    )
    print("rational_pole_t_lower=", pole_t.lower())
    print("rational_pole_t_upper=", pole_t.upper())
    print("rational_pole_residue_abs_lower=", abs(pole_residue).lower())
    print("rational_pole_residue_abs_upper=", abs(pole_residue).upper())
    print("zeta_2s_at_rational_pole_abs_lower=", abs((2 * pole_s).zeta()).lower())
    print("zeta_2sminus1_at_rational_pole_abs_lower=", abs((2 * pole_s - acb(1)).zeta()).lower())

    # Geometry-only diagnostic for Ω_sym=[-1/2,3/2] x [t0-2.38,t0+2.38]
    # at the theta zero's real coordinate 3/4.  L=2 and x=5/4 from the
    # left, while the reflected left-side distance is 3/4.
    L = arb(2)
    H = 2 * delta
    right_lo, right_hi, right_tail = vertical_harmonic_measure(arb("1.25"), L, H)
    left_lo, left_hi, left_tail = vertical_harmonic_measure(arb("0.75"), L, H)
    print("symmetric_union_harmonic_measure_lower=", (right_lo + left_lo).lower())
    print("symmetric_union_harmonic_measure_upper=", (right_hi + left_hi).upper())
    print("symmetric_harmonic_tail_upper_right=", right_tail.upper())
    print("symmetric_harmonic_tail_upper_left=", left_tail.upper())


if __name__ == "__main__":
    main()
