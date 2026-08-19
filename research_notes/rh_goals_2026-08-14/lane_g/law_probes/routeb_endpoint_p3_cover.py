"""Arb receipt for the endpoint p=3 Route-B effective-tail candidate.

This is a receipt, not an independent proof of the upstream RATE inputs.  It
replays the enlarged rectangle geometry and the endpoint activation arithmetic
using outward Arb intervals.  The imported atom-moment and FW constants are
labelled in the accompanying note and still require the scope stated there.
"""

from flint import acb, arb, ctx


ctx.dps = 70
pi = arb.pi()
sigma_R = arb("1.5")
delta = arb("2.38")
radius = arb("0.025")
L = sigma_R - arb("0.5")
H = 2 * delta
t0 = (acb.zeta_zero(1) / 2).imag
# Absolute complex-plane seed centre is sigma=3/4.  The harmonic rectangle
# below uses x=Re(s)-1/2, hence its corresponding centre is x=1/4.
z0 = acb(arb("0.75"), t0)


def phi_inf(s):
    return (
        pi.sqrt()
        * (s - arb("0.5")).gamma()
        * (2 * s - 1).zeta()
        / (s.gamma() * (2 * s).zeta() * ((acb(4).log() * s).exp() - 1))
    )


def positive_int_floor(a):
    # All uses below are positive integers; this avoids decimal parsing.
    s = str(a)
    assert "+/-" not in s and "e" not in s.lower()
    whole, frac = s.split(".", 1)
    assert set(frac) <= {"0"}
    return int(whole)


def harmonic_tail(nmax):
    n0 = nmax + 2
    a = pi * (L - (arb("0.25") + radius)) / H
    return (
        4
        / pi
        / arb(n0)
        / (1 - (-2 * pi * L / H).exp())
        * (-arb(n0) * a).exp()
        / (1 - (-a).exp())
    ).upper()


N = 8192
nmax = 101
tail_upper = harmonic_tail(nmax)
cells = []
for k in range(N):
    theta = arb(2 * pi * (arb(k) + arb("0.5")) / N, pi / N)
    z = z0 + radius * acb(theta.cos(), theta.sin())
    m_lower = abs(phi_inf(z)).lower()

    x = arb("0.25") + radius * theta.cos()
    y = delta + radius * theta.sin()
    omega = arb(0)
    for n in range(1, nmax + 1, 2):
        nn = arb(n)
        omega += (
            4
            / (nn * pi)
            * (nn * pi * x / H).sinh()
            / (nn * pi * L / H).sinh()
            * (nn * pi * y / H).sin()
        )
    nu_lower = omega.lower() - tail_upper
    cells.append((m_lower, nu_lower))


# The full vertical boundary is |s| <= S.  This is the boundary quantity in
# the paired majorant, not the smaller modulus on the seed circle.
S = (sigma_R**2 + (t0 + delta) ** 2).sqrt()

# Arb cover of all four sides of the enlarged rectangle for the theta
# boundary term in K_+.  The critical-line side is included explicitly; its
# exact unitary value is not substituted for the interval calculation.
Nedge = 4096
edge_max = arb(0)
edge_name = ""
edge_index = -1
for name in ("left", "right"):
    sigma_edge = arb("0.5") if name == "left" else sigma_R
    for j in range(Nedge):
        center = t0 - delta + (arb(j) + arb("0.5")) * (2 * delta / Nedge)
        radius_t = delta / Nedge
        tbox = center + arb(0, radius_t)
        value = abs(phi_inf(acb(sigma_edge, tbox))).upper()
        if value > edge_max:
            edge_max, edge_name, edge_index = value, name, j
for name in ("bottom", "top"):
    t_edge = t0 - delta if name == "bottom" else t0 + delta
    for j in range(Nedge):
        center = arb("0.5") + (arb(j) + arb("0.5")) * (L / Nedge)
        radius_s = L / Nedge
        sbox = center + arb(0, radius_s) + acb(0, t_edge)
        value = abs(phi_inf(sbox)).upper()
        if value > edge_max:
            edge_max, edge_name, edge_index = value, name, j

C4 = arb(2) ** 62 + 1
M = arb(2)  # exact endpoint value M(3/2)
a = M * 2 * pi**2 * (S + 1) * 3 * C4
b = M * 3 * 128 * (1 + arb(2).log()) * 2  # p*C1*G(3), G(3)=2
a_up = a.upper()
b_up = b.upper()


def endpoint_error(q):
    qq = arb(q)
    return (a_up * (qq.log() + 5 + arb(65) / qq) + b_up) / qq**2


K = arb(125)
q = 31951437654668744792


def ratio_at(q_value, m_lower, nu_lower):
    e = endpoint_error(q_value)
    lhs = K ** (1 - nu_lower) * e**nu_lower
    return lhs / m_lower, lhs, e


min_m = min(c[0] for c in cells)
min_nu = min(c[1] for c in cells)
max_q = arb(0)
max_prev = arb(0)
max_q_index = -1
max_prev_index = -1
max_q_m = arb(0)
max_q_nu = arb(0)
pass_all = True
for k, (m_lower, nu_lower) in enumerate(cells):
    rq, lhs, e = ratio_at(q, m_lower, nu_lower)
    rp, _, _ = ratio_at(q - 1, m_lower, nu_lower)
    if rq.upper() > max_q.upper():
        max_q, max_q_index, max_q_m, max_q_nu = rq, k, m_lower, nu_lower
    if rp.upper() > max_prev.upper():
        max_prev, max_prev_index = rp, k
    pass_all = pass_all and bool(lhs.upper() < m_lower)

eps = arb("4.68")
C6 = 100 * (1 / eps + (1 + 1 / eps**2).sqrt())
theta_sup = edge_max
Kraw = C6 + theta_sup
derivative_bracket = a_up * (2 * arb(q).log() + 9 + arb(195) / q) + 2 * b_up

print("sigma_R=", sigma_R, "p=3", "alpha=2")
print("delta=", delta, "radius=", radius, "L=", L, "H=", H)
print("t0=", t0)
print("circle_boxes=", N, "harmonic_boxes=", N, "series_nmax=", nmax)
print("harmonic_tail_upper=", tail_upper)
print("min_phi_lower=", min_m)
print("min_nu_lower=", min_nu)
print("S_vertical_upper=", S.upper())
print("theta_boundary_sup_upper=", edge_max, "edge=", edge_name, "cell=", edge_index)
print("C4=", positive_int_floor(C4))
print("M_endpoint=", M)
print("a_upper=", a_up)
print("b_upper=", b_up)
print("C6_epsilon_4.68=", C6)
print("Kraw_upper=", Kraw)
print("CERT_Kraw_lt_125=", bool(Kraw < K))
print("q=", q)
print("E_endpoint_upper=", endpoint_error(q).upper())
print("max_ratio_q_upper=", max_q.upper(), "cell=", max_q_index)
print("max_ratio_q_cell_m_lower=", max_q_m)
print("max_ratio_q_cell_nu_lower=", max_q_nu)
print("PASS_all_cells_q=", pass_all)
print("q_minus_1=", q - 1)
print("max_ratio_prev_upper=", max_prev.upper(), "cell=", max_prev_index)
print("PREV_CERTIFICATE_FAILS=", bool(max_prev.upper() > 1))
print("endpoint_derivative_bracket_lower=", derivative_bracket.lower())
print("MONOTONE_FOR_q_ge_12=", bool(derivative_bracket.lower() > 0))
