#!/usr/bin/env python3
"""
Closed-form continuous width and resonance-gain oracle for the Hecke B(q)
rotation-arc model.

This replaces the grid computation of W(q) with the explicit boundary equation
on the governing ellipse E=(2-lambda)/lambda^3.

Definitions:
    theta = pi/q, lambda = 2 cos(theta), r = tan(theta/2)
    W(q) = 2 alpha_q
where alpha_q is determined by the last-branch lower-edge boundary
    (1+lambda) cos(alpha) - (lambda-1) r sin(alpha) = lambda^(3/2).

Equivalently:
    alpha_q = acos(lambda^(3/2) / hypot(1+lambda, (lambda-1)r))
              - atan2((lambda-1)r, 1+lambda).

The limiting constant is exact:
    W_inf = 2 asin(1/3)
    W(q) = W_inf - pi/(3q) + 31 sqrt(2) pi^2/(18 q^2) + O(q^-3).

The resonance check below is the symmetric notch-hop criterion. It predicts the
+1 cases where the continuous count floor(Wq/pi)+1 is beaten by one terminal
sub-threshold k=2 point.
"""
from __future__ import annotations

from dataclasses import dataclass
import argparse
import math
from typing import Iterable


@dataclass(frozen=True)
class WidthResonance:
    q: int
    theta: float
    lam: float
    W: float
    s: float
    B0: int
    B_pred: int
    resonance: bool
    frac_min: float | None
    frac_max: float | None
    k_pattern: str | None


def _validate_q(q: int) -> None:
    if q < 5:
        raise ValueError("q must be >= 5 for the q>=5 Hecke onset regime")


def lam(q: int) -> float:
    _validate_q(q)
    return 2.0 * math.cos(math.pi / q)


def continuous_half_width(q: int) -> float:
    """Return alpha_q, half of the continuous governing arc width W(q)."""
    _validate_q(q)
    th = math.pi / q
    la = 2.0 * math.cos(th)
    r = math.tan(th / 2.0)  # sqrt((2-lambda)/(2+lambda)) exactly.
    A = 1.0 + la
    B = (la - 1.0) * r
    C = la ** 1.5
    return math.acos(C / math.hypot(A, B)) - math.atan2(B, A)


def continuous_width(q: int) -> float:
    """Closed-form continuous width W(q) of the governing last-branch arc."""
    return 2.0 * continuous_half_width(q)


def continuous_count(q: int) -> int:
    """B0(q) = floor(W(q)/(pi/q)) + 1, the no-notch/continuous count."""
    th = math.pi / q
    # Tiny negative guard avoids a floating upward nudge at exact boundaries.
    return math.floor(continuous_width(q) / th + 1e-12) + 1


def resonance_window(q: int, target_count: int) -> tuple[bool, float | None, float | None]:
    """
    Return whether an even target_count fits by hopping the central notch.

    For a symmetric target run of N=target_count lattice points:
      * if N is odd, the centre point impales the peak when frac>1, so no hop;
      * if N is even, the nearest points sit at +-theta/2 and can straddle a
        narrow super-threshold notch.

    frac_min: lower bound needed to push the two extreme points into the
              last-branch domain.
    frac_max: upper bound before the two closest-to-peak points become
              super-threshold.
    A resonance exists when 1 < frac_min < frac_max.
    """
    _validate_q(q)
    if target_count % 2 == 1:
        return False, None, None

    th = math.pi / q
    la = 2.0 * math.cos(th)
    r = math.tan(th / 2.0)

    psi_ext = (target_count - 1) * th / 2.0
    D_ext = (1.0 + la) * math.cos(psi_ext) - (la - 1.0) * r * abs(math.sin(psi_ext))
    if D_ext <= 0.0:
        return False, None, None

    frac_min = (la ** 1.5 / D_ext) ** 2

    psi_near = th / 2.0
    G_near = math.cos(psi_near) ** 2 - (r ** 2) * math.sin(psi_near) ** 2
    frac_max = 1.0 / G_near

    return (1.0 < frac_min < frac_max), frac_min, frac_max


def predicted_count(q: int) -> WidthResonance:
    """Return the continuous count plus a possible +1 resonance gain."""
    _validate_q(q)
    th = math.pi / q
    la = 2.0 * math.cos(th)
    W = continuous_width(q)
    B0 = math.floor(W / th + 1e-12) + 1
    ok, lo, hi = resonance_window(q, B0 + 1)
    B = B0 + (1 if ok else 0)
    return WidthResonance(
        q=q,
        theta=th,
        lam=la,
        W=W,
        s=W / th,
        B0=B0,
        B_pred=B,
        resonance=ok,
        frac_min=lo,
        frac_max=hi,
        k_pattern=("[1 x %d, 2]" % (B - 1) if ok else None),
    )


def W_inf() -> float:
    return 2.0 * math.asin(1.0 / 3.0)


def asymptotic_width(q: int) -> float:
    """Two-term expansion through q^-2."""
    th = math.pi / q
    return W_inf() - th / 3.0 + (31.0 * math.sqrt(2.0) / 18.0) * th * th


def scan(qs: Iterable[int]) -> list[WidthResonance]:
    return [predicted_count(q) for q in qs]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("qs", nargs="*", type=int, help="q values to print; default: landmark table")
    parser.add_argument("--scan", type=int, metavar="QMAX", help="scan q=7..QMAX and print resonances")
    args = parser.parse_args()

    if args.scan is not None:
        rows = [row for row in scan(range(7, args.scan + 1)) if row.resonance]
        print("q B0 B_pred s=Wq/pi frac_min frac_max")
        for r in rows:
            print(f"{r.q:5d} {r.B0:5d} {r.B_pred:6d} {r.s:14.9f} {r.frac_min:.12g} {r.frac_max:.12g}")
        return

    qs = args.qs or [7, 13, 19, 23, 24, 30, 40, 61, 126, 570]
    print(f"W_inf = {W_inf():.15f}; slope = W_inf/pi = {W_inf()/math.pi:.15f}")
    print("q lambda W(q) s=Wq/pi B0 Bpred resonance frac-window")
    for r in scan(qs):
        window = "-"
        if r.frac_min is not None:
            window = f"({r.frac_min:.10g}, {r.frac_max:.10g})"
        print(
            f"{r.q:4d} {r.lam:.12f} {r.W:.12f} {r.s:11.6f}"
            f" {r.B0:3d} {r.B_pred:5d} {str(r.resonance):>9s} {window}"
        )


if __name__ == "__main__":
    main()
