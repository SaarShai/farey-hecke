"""Negative fixture: a contour ball containing zero must not certify."""
from __future__ import annotations

import certify_q4q6_winding as cert
from flint import acb, arb


def fake_det_record(_q, _re, _im, _N):
    return acb(0), arb(0), {"q": 0.0, "dims": []}, 1


def main():
    original = cert._det_record
    cert._det_record = fake_det_record
    try:
        winding, info = cert.contour_winding(4, 0.25, 7.0, 1e-6, 1e-6, 28, 24)
    finally:
        cert._det_record = original
    assert winding is None
    assert info["reason"] == "contour_ball_straddles_zero"
    print("NEGATIVE_CONTOUR_STRADDLE=PASS")


if __name__ == "__main__":
    main()
