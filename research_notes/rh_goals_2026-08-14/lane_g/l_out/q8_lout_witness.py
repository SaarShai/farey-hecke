#!/usr/bin/env python3
"""Boundary-sup WITNESSES and envelope preconditions for corrected condition 4a'.

`L_OUT_CONDITION4_ADJUDICATION.md` sec "Corrected conditions" replaces the
mis-specified condition 4a with

    4a'.  selected_column_bounds_theta[k] >= W_k  for every block, k <= K_head,
          W_k := max over >= 256 boundary points z of |u| = theta of
                 |f_k(z)|.lower(),
          evaluated at a POINT z and a POINT s inside the pinned s-box, by an
          evaluation path that does not reuse the receipt's arc-cover
          enclosure; plus the three envelope preconditions
              A_theta >= W_0 ,
              C_theta >= sup_z sum_n |w_n psi_n| / r_j ,
              rho_theta >= max( sup_{n,z} |u_n(z)| , q ).

Why a point evaluation is a rigorous LOWER bound of the true boundary sup:
`W_k` is `|f_k(z_p)|.lower()` at an individual boundary point `z_p`, so
`W_k <= |f_k(z_p)| <= sup_{|u|=theta} |f_k| = M_k(theta)`.  A point `s` inside
the pinned box is likewise one admissible `s`.  Nothing here is an upper bound
and nothing here is consumed by `tau_out`; the witness only certifies that the
recorded bound has not fallen BELOW the object it claims to majorize.

The arc-cover enclosure of the receipt is not reused: `z` carries zero radius,
so the `r_j^-k` binomial sum is evaluated on points rather than on balls.

Definitions (matching `lane_f/q8_r2_local.exact_tail_columns_on_arc`):

    psi_n(z) = 1/(z - n lam)      if neg else  -1/(z + n lam)
    w_n(z)   = ((z - n lam)^2)^-s if neg else  ((z + n lam)^2)^-s
    u_n(z)   = (psi_n(z) - c_j) / r_j
    f_k(z)   = sum_{n >= n0} w_n(z) u_n(z)^k      (tail family)
    f_k(z)   = w_{n0}(z) u_{n0}(z)^k              (single branch)
"""

from __future__ import annotations

import sys
from pathlib import Path

from flint import acb, arb, ctx

LANE_G = Path(__file__).resolve().parent.parent
LANE_F = LANE_G.parent / "lane_f"
sys.path.insert(0, str(LANE_F))

import q8_r2_local as r2local  # noqa: E402

# Point s: the CENTRE of the pinned s-box, zero radius.  One admissible s.
S_POINT = acb(arb(r2local.PIN_RE), arb(r2local.PIN_IM))

DEFAULT_WITNESS_POINTS = 256
DEFAULT_PRECONDITION_POINTS = 128
DEFAULT_PRECONDITION_NMAX = 2000


def boundary_points(c_i: arb, radius: arb, count: int) -> list[acb]:
    """`count` POINT samples of the circle |z - c_i| = radius (zero radius)."""

    two_pi = arb.pi() * 2
    out = []
    for index in range(count):
        angle = two_pi * arb(index) / arb(count)
        out.append(acb(c_i + radius * angle.cos(), radius * angle.sin()))
    return out


def _psi_and_weight(z: acb, lam: arb, n: int, neg: bool) -> tuple[acb, acb]:
    denominator = z - acb(arb(n) * lam) if neg else z + acb(arb(n) * lam)
    psi = acb(1) / denominator if neg else acb(-1) / denominator
    weight = (denominator * denominator) ** (-S_POINT)
    return psi, weight


def witness_columns(block, centers, radii, radius_theta, lam, k_head, points):
    """W_k for one block: max over boundary points of |f_k(z)|.lower()."""

    i, j, n0, neg, tail = block
    c_j, r_j = centers[j - 1], radii[j - 1]
    zs = boundary_points(centers[i - 1], radius_theta, points)
    best = [arb(0) for _ in range(k_head + 1)]
    worst = [0] * (k_head + 1)
    for index, z in enumerate(zs):
        if tail:
            columns = r2local.exact_tail_columns_on_arc(
                S_POINT, z, c_j, r_j, lam, n0, neg, k_head
            )
            values = [column.abs_lower() for column in columns]
        else:
            psi, weight = _psi_and_weight(z, lam, n0, neg)
            u = (psi - acb(c_j)) / acb(r_j)
            values = [(weight * u**k).abs_lower() for k in range(k_head + 1)]
        for k, value in enumerate(values):
            if value.lower() > best[k].lower():
                best[k], worst[k] = value.lower(), index
    return best, worst


def envelope_preconditions(block, centers, radii, radius_theta, lam, points, n_max):
    """Sampled lower estimates of the two sups the envelope derivation needs.

    Returns (c_sum_sampled, u_sup_sampled).  Both are maxima over SAMPLED
    boundary points, and `c_sum_sampled` additionally truncates the branch sum
    at `n_max`, so each is a LOWER estimate of the true sup.  `C_theta >= ...`
    and `rho_theta >= ...` against these are therefore NECESSARY conditions,
    not proofs of the preconditions.
    """

    i, j, n0, neg, tail = block
    c_j, r_j = centers[j - 1], radii[j - 1]
    zs = boundary_points(centers[i - 1], radius_theta, points)
    top = n_max if tail else n0
    c_sum_best = arb(0)
    u_sup_best = arb(0)
    for z in zs:
        total = arb(0)
        for n in range(n0, top + 1):
            psi, weight = _psi_and_weight(z, lam, n, neg)
            total += (weight * psi).abs_lower() / r_j
            u_abs = ((psi - acb(c_j)) / acb(r_j)).abs_lower()
            if u_abs.lower() > u_sup_best.lower():
                u_sup_best = u_abs.lower()
        if total.lower() > c_sum_best.lower():
            c_sum_best = total.lower()
    return c_sum_best, u_sup_best
