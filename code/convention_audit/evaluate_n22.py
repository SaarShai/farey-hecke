#!/usr/bin/env python3
"""Reproduce the two N=22 determinant conventions used in the audit.

This file imports the existing read-only sources.  It does not modify them and
prints JSON so the receipt can preserve the exact numerical check.  The
``sonnet_current`` lane is the implementation in collocation_even_sonnet.py.
The ``sonnet_corrected_basis`` lane changes only the missing radius_scale in
the input interpolation coordinate; it is a diagnostic control, not a source
implementation.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
N = 22
PINS = {
    "certified_pin": complex(0.45389518, 5.76353724),
    "sonnet_pin": complex(0.43318010, 5.67574682),
}


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def complex_mid(ball) -> complex:
    return complex(float(ball.real.mid()), float(ball.imag.mid()))


def certified_value(cert, s: complex) -> tuple[complex, float]:
    matrix, kappa = cert.build_reduced_matrix_ball(
        cert.acb(s.real, s.imag), N, +1, n_head=4
    )
    ball = cert._det_block(matrix, N, kappa, N)
    value = complex_mid(ball)
    return value, abs(value)


def sonnet_value(son, s: complex) -> tuple[complex, float]:
    value, _note = son.det_value(s, N)
    return value, abs(value)


def corrected_sonnet_value(son, s: complex) -> tuple[complex, float]:
    """Run Sonnet after correcting its input nodal coordinate by 0.5."""

    original_single = son.single_branch_block
    original_tail = son.tail_closed_block

    def single(s0, c_i, r_i, c_j, r_j, n, neg, nodes, coeff, radius_scale=0.5):
        return original_single(
            s0, c_i, r_i, c_j, r_j * radius_scale, n, neg,
            nodes, coeff, radius_scale
        )

    def tail(s0, c_i, r_i, c_j, r_j, n_start, neg, nodes, coeff,
             radius_scale=0.5):
        return original_tail(
            s0, c_i, r_i, c_j, r_j * radius_scale, n_start, neg,
            nodes, coeff, radius_scale
        )

    son.single_branch_block = single
    son.tail_closed_block = tail
    try:
        return sonnet_value(son, s)
    finally:
        son.single_branch_block = original_single
        son.tail_closed_block = original_tail


def main() -> None:
    cert = load_module("zeta_cert_rosen_q5_audit", ROOT / "code/zeta_cert_rosen_q5.py")
    son = load_module(
        "collocation_even_sonnet_audit",
        ROOT / "projects/g5-crosscheck/collocation_even_sonnet.py",
    )

    result = {
        "N": N,
        "n_head": 4,
        "sector_sign": 1,
        "pins": {name: [s.real, s.imag] for name, s in PINS.items()},
        "mms_certified_plus": {},
        "sonnet_current": {},
        "sonnet_corrected_basis": {},
    }
    for name, s in PINS.items():
        for key, evaluator in (
            ("mms_certified_plus", certified_value),
            ("sonnet_current", sonnet_value),
            ("sonnet_corrected_basis", corrected_sonnet_value),
        ):
            value, magnitude = evaluator(cert if key == "mms_certified_plus" else son, s)
            result[key][name] = {
                "det_real": value.real,
                "det_imag": value.imag,
                "det_abs": magnitude,
            }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
