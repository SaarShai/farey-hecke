"""T-c rerun machinery with independently parameterized q=5 disc radii.

The certified arithmetic, branch-series construction, and finite determinant
are loaded from ``code/zeta_cert_rosen_q5.py``.  This module changes only the
geometry argument passed to the normalized Taylor-basis builder; the original
source file is never edited.

The full T-c driver is in ``run_tc.py`` and is deliberately inert unless its
``--go`` flag is supplied.
"""

from __future__ import annotations

import importlib.util
import json
import sys
import time
from decimal import Decimal
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
WORKSPACE_ROOT = REPO_ROOT.parents[1]
SOURCE_PATH = REPO_ROOT / "code" / "zeta_cert_rosen_q5.py"
DISC_OPT_PATH = (
    WORKSPACE_ROOT
    / "research_notes"
    / "rh_goals_2026-08-14"
    / "lane_g"
    / "tb_disc_opt.json"
)
GEOMETRY_PATH = REPO_ROOT / "code" / "out" / "resonance_geometry.json"


def _load_certified_source():
    if not SOURCE_PATH.is_file():
        raise FileNotFoundError(f"certified source not found: {SOURCE_PATH}")
    spec = importlib.util.spec_from_file_location("tc_certified_q5", SOURCE_PATH)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load certified source: {SOURCE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


CERT = _load_certified_source()


def _load_disc_factors() -> tuple[float, float, float]:
    if not DISC_OPT_PATH.is_file():
        raise FileNotFoundError(f"disc optimization constants not found: {DISC_OPT_PATH}")
    with DISC_OPT_PATH.open() as handle:
        data = json.load(handle)
    factors = tuple(float(value) for value in data["a"])
    if len(factors) != 3 or any(value <= 0 for value in factors):
        raise ValueError(f"expected three positive disc factors in {DISC_OPT_PATH}")
    return factors  # type: ignore[return-value]


DISC_FACTORS = _load_disc_factors()


def _arb_decimal(value: float):
    # The JSON has a binary-rounding spelling for 3.14; retain the declared
    # decimal constants rather than importing that representation error.
    text = format(Decimal(str(value)).normalize(), "f")
    return CERT.arb(text)


def geometry_for_factors(factors: tuple[float, float, float] = DISC_FACTORS):
    """Return certified centers and radii for the supplied per-disc factors."""
    lam = CERT.lam_ball()
    points = CERT.partition_points_ball(lam)
    centers = [(points[i - 1] + points[i]) / 2 for i in range(1, 4)]
    half_widths = [(points[i] - points[i - 1]) / 2 for i in range(1, 4)]
    radii = [half_widths[i] * _arb_decimal(factors[i]) for i in range(3)]
    return lam, centers, radii


def build_reduced_matrix_ball_per_disc(
    s,
    N: int,
    sign: int,
    n_head: int = 4,
    factors: tuple[float, float, float] = DISC_FACTORS,
):
    """Build the q=5 mms+/- matrix with independently chosen disc radii.

    This is the source builder's eq.(34) block assembly with only its hard-coded
    ``disc_radii_ball(lam)`` replaced by ``geometry_for_factors(factors)``.
    Every series primitive and Arb operation is the certified source machinery.
    """
    lam, c, rho = geometry_for_factors(factors)
    kappa = 3
    twoh = 2
    k_idx = 3
    sgn = CERT.acb(sign)
    blocks: dict[tuple[int, int], list[Any]] = {}

    def add_cols(i: int, j: int, cols, prefac=None):
        key = (i, j)
        existing = blocks.get(key)
        if existing is None:
            existing = [CERT.acb_series([0]) for _ in range(N)]
            blocks[key] = existing
        for kk in range(N):
            col = cols[kk] if prefac is None else prefac * cols[kk]
            existing[kk] = existing[kk] + col

    def single_block(i: int, j: int, n: int, neg: bool):
        return CERT._single_block_allcols(
            s, c[i - 1], rho[i - 1], c[j - 1], rho[j - 1], lam, n, neg, N
        )

    def inf_block(i: int, j: int, n0: int, neg: bool):
        ci, ri, cj, rj = c[i - 1], rho[i - 1], c[j - 1], rho[j - 1]
        cols = CERT._tail_block_allcols(
            s, ci, ri, cj, rj, lam, n0 + n_head, neg, N
        )
        for ell in range(n0, n0 + n_head):
            head_cols = CERT._single_block_allcols(
                s, ci, ri, cj, rj, lam, ell, neg, N
            )
            for kk in range(N):
                cols[kk] = cols[kk] + head_cols[kk]
        return cols

    # MMS eq.(34), q=5, h=1, kappa=3.  This matches the current certified
    # source's block pattern exactly, including its sign parameter.
    add_cols(1, twoh, single_block(1, twoh, 2, False))
    add_cols(1, k_idx, inf_block(1, k_idx, 3, False))
    add_cols(1, twoh, single_block(1, twoh, 1, True), prefac=sgn)
    add_cols(1, k_idx, inf_block(1, k_idx, 2, True), prefac=sgn)

    add_cols(2, k_idx, inf_block(2, k_idx, 2, False))
    add_cols(2, twoh, single_block(2, twoh, 1, True), prefac=sgn)
    add_cols(2, k_idx, inf_block(2, k_idx, 2, True), prefac=sgn)

    for i in range(3, k_idx + 1):
        add_cols(i, i - 2, single_block(i, i - 2, 1, False))
        add_cols(i, k_idx, inf_block(i, k_idx, 2, False))
        add_cols(i, twoh, single_block(i, twoh, 1, True), prefac=sgn)
        add_cols(i, k_idx, inf_block(i, k_idx, 2, True), prefac=sgn)

    dim = kappa * N
    matrix = CERT.acb_mat(dim, dim)
    for (i, j), cols in blocks.items():
        for kk in range(N):
            series = cols[kk]
            for m in range(N):
                matrix[(i - 1) * N + m, (j - 1) * N + kk] = (
                    series[m] if m < len(series) else CERT.acb(0)
                )
    return matrix, kappa


def finite_determinant(
    s,
    N: int,
    sign: int = 1,
    n_head: int = 4,
    factors: tuple[float, float, float] = DISC_FACTORS,
):
    matrix, kappa = build_reduced_matrix_ball_per_disc(
        s, N, sign, n_head=n_head, factors=factors
    )
    return CERT._det_block(matrix, N, kappa, N)


def midpoint_complex(value) -> complex:
    return complex(float(value.real.mid()), float(value.imag.mid()))


def relative_difference(old: complex, new: complex) -> float:
    return abs(new - old) / abs(old)


def contour_points(hx: float, hy: float, K: int):
    points = []
    for t in range(K):
        points.append((-hx + 2 * hx * t / K, -hy))
    for t in range(K):
        points.append((hx, -hy + 2 * hy * t / K))
    for t in range(K):
        points.append((hx - 2 * hx * t / K, hy))
    for t in range(K):
        points.append((-hx, hy - 2 * hy * t / K))
    return points


def _contour_dets(
    re0: float,
    im0: float,
    hx: float,
    hy: float,
    N: int,
    sign: int,
    n_head: int,
    K: int,
    factors: tuple[float, float, float] = DISC_FACTORS,
):
    raw = []
    for dx, dy in contour_points(hx, hy, K):
        s = CERT.acb(CERT.arb(re0) + CERT.arb(dx), CERT.arb(im0) + CERT.arb(dy))
        matrix, kappa = build_reduced_matrix_ball_per_disc(
            s, N, sign, n_head=n_head, factors=factors
        )
        det = CERT._det_block(matrix, N, kappa, N)
        raw.append({"dx": dx, "dy": dy, "matrix": matrix, "det": det})
    return raw


def observed_coefficient_C(
    raw_points,
    N: int,
    rho_star: float,
):
    """Empirical C supported by all normalized matrix coefficients observed.

    The source matrix uses normalized output rows.  For row mode m, the
    observed envelope is |B[m,k]| / rho_star**m; the maximum over every matrix
    coefficient and every contour point is the reported data-supported C.
    """
    supported = 0.0
    by_point = []
    for point in raw_points:
        matrix = point["matrix"]
        local = 0.0
        dim = 3 * N
        for row in range(dim):
            mode = row % N
            scale = rho_star**mode
            for col in range(dim):
                value = float(matrix[row, col].abs_upper()) / scale
                local = max(local, value)
        by_point.append(local)
        supported = max(supported, local)
    return supported, by_point


def tail_radius(C: float, rho_star: float, N: int) -> float:
    return C * rho_star ** (N + 1) / (1.0 - rho_star)


def first_sufficient_N(contour_lower_bound: float, C: float, rho_star: float,
                       start: int = 0, stop: int = 200):
    for N in range(start, stop + 1):
        if contour_lower_bound - tail_radius(C, rho_star, N) > 0:
            return N
    return None


def _inflate_det(det, radius: float):
    return CERT.acb(
        det.real + CERT.arb(0, radius),
        det.imag + CERT.arb(0, radius),
    )


def _winding_from_dets(dets):
    total = CERT.arb(0)
    for index, first in enumerate(dets):
        second = dets[(index + 1) % len(dets)]
        product = second * first.conjugate()
        real_part, imag_part = product.real, product.imag
        if not (
            real_part.lower() > 0
            or imag_part.lower() > 0
            or imag_part.upper() < 0
        ):
            return None, {"reason": "half-turn test failed", "edge": index}
        total = total + product.arg().real
    winding_ball = total / (CERT.arb.pi() * 2)
    lo, hi = winding_ball.lower(), winding_ball.upper()
    nearest = round(float(winding_ball.mid()))
    if lo > nearest - CERT.arb(1) / 2 and hi < nearest + CERT.arb(1) / 2:
        return nearest, {
            "winding_ball": [float(lo), float(hi)],
            "winding": nearest,
        }
    return None, {"reason": "winding interval does not pin an integer",
                  "winding_ball": [float(lo), float(hi)]}


def evaluate_box(
    re0: float,
    im0: float,
    hx: float = 1e-6,
    hy: float = 1e-6,
    N: int = 48,
    sign: int = 1,
    n_head: int = 4,
    K: int = 24,
    factors: tuple[float, float, float] = DISC_FACTORS,
    apply_tail: bool = False,
    rho_override: float | None = None,
):
    """Evaluate one full four-edge box.

    ``apply_tail=False`` is the requested pure finite-N timing path.  When true,
    the data-supported formula F is applied uniformly to both real and imaginary
    Arb radii for a ready-to-run T-c result.
    """
    start = time.perf_counter()
    raw = _contour_dets(re0, im0, hx, hy, N, sign, n_head, K, factors=factors)
    lower_bounds = [float(point["det"].abs_lower()) for point in raw]
    finite_lower_bound = min(lower_bounds)
    rho_star = rho_override if rho_override is not None else _load_rho_star()
    C, C_by_point = observed_coefficient_C(raw, N, rho_star)
    F = tail_radius(C, rho_star, N)
    radius = F if apply_tail else 0.0
    dets = [_inflate_det(point["det"], radius) for point in raw]
    winding, winding_info = _winding_from_dets(dets)
    return {
        "wall_seconds": time.perf_counter() - start,
        "N": N,
        "K_per_edge": K,
        "center": [re0, im0],
        "half_width": [hx, hy],
        "finite_contour_lower_bound": finite_lower_bound,
        "finite_contour_lower_bounds": lower_bounds,
        "C_supported": C,
        "C_by_point": C_by_point,
        "rho_star": rho_star,
        "tail_radius_F": F,
        "tail_applied": apply_tail,
        "margin_after_F": finite_lower_bound - F,
        "winding": winding,
        "winding_info": winding_info,
        "n_contour_points": len(raw),
    }


def _load_rho_star() -> float:
    with DISC_OPT_PATH.open() as handle:
        return float(json.load(handle)["rho_star"])


def load_g5_pins():
    if not GEOMETRY_PATH.is_file():
        raise FileNotFoundError(f"G_5 geometry receipt not found: {GEOMETRY_PATH}")
    with GEOMETRY_PATH.open() as handle:
        data = json.load(handle)
    pins = []
    for index, item in enumerate(data["g5_even_resonances"], start=1):
        pins.append({
            "name": f"g5_pin_{index}",
            "re": float(item["re"]),
            "im": float(item["im"]),
            "N_stable": bool(item.get("N_stable", False)),
        })
    if len(pins) != 8:
        raise ValueError(f"expected exactly 8 G_5 pins, found {len(pins)}")
    return pins


G5_PINS = load_g5_pins()
ESSENTIAL_GAP_BOX = {
    "name": "essential_gap_box_g5_pin_6",
    "re": G5_PINS[5]["re"],
    "im": G5_PINS[5]["im"],
    "hx": 1e-6,
    "hy": 1e-6,
    "gap_target": 0.5 - G5_PINS[5]["re"],
    "source": "rightmost of the eight G_5 geometry pins; named gap box",
}
