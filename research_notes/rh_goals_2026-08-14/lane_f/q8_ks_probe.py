#!/usr/bin/env python3
"""q=8 even-parity K_s lattice and elementary product lower bound."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from flint import arb, ctx


LANE_F = Path(__file__).resolve().parent
PIN_RE = "0.4252310423737965"
PIN_IM = "4.345760788321986"
HALF_WIDTH = "1e-6"
OUT_DEFAULT = LANE_F / "f8_receipts" / "Q8_KS_PROBE_RECEIPT.json"


def matmul(left, right):
    return [[sum((left[i][k] * right[k][j] for k in range(2)), arb(0)) for j in range(2)] for i in range(2)]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--terms", type=int, default=24)
    parser.add_argument("--out", type=Path, default=OUT_DEFAULT)
    args = parser.parse_args()
    ctx.prec = 384
    lam = (arb(2) + arb(2).sqrt()).sqrt()
    m1 = [[arb(0), arb(-1)], [arb(1), lam]]
    m2 = [[arb(0), arb(-1)], [arb(1), arb(2) * lam]]
    # Even q=2h+2, h=3: K is the 3-cycle L1,L1,L2, hence the scalar word
    # A_s=L1^2 L2 and Möbius matrix M2*M1*M1.
    word = matmul(matmul(m2, m1), m1)
    trace = (word[0][0] + word[1][1]).upper()
    determinant = (word[0][0] * word[1][1] - word[0][1] * word[1][0]).upper()
    ell = ((trace - (trace * trace - arb(4)).sqrt()) / arb(2)).upper()
    a = (-ell.log()).upper()
    spacing = (arb.pi() / a).upper()
    sigma_lo = arb(PIN_RE) - arb(HALF_WIDTH)
    t0 = (ell ** (arb(2) * sigma_lo)).upper()
    terms = []
    product_lower = arb(1)
    for n in range(args.terms):
        t = (ell ** (arb(2) * (sigma_lo + n))).upper()
        product_lower *= arb(1) - t
        terms.append(t)
    tail_sum = (ell ** (arb(2) * (sigma_lo + args.terms)) / (arb(1) - ell * ell)).upper()
    product_lower = (product_lower * (arb(1) - tail_sum)).lower()
    center_im = arb(PIN_IM)
    k_mid = round(float((center_im / spacing).mid()))
    candidates = []
    # The K_s zero lattice is s=-n+2*pi*i*k/log(1/b), n>=0.  The box gate
    # is Euclidean distance from the *closed rectangle* to that lattice, not
    # merely the vertical clearance.  The previous draft subtracted only the
    # imaginary half-width; that understated the required diagonal margin
    # and failed to reproduce F8_CERT_PLAN's 0.6227577 figure.
    re_center = arb(PIN_RE)
    half_width = arb(HALF_WIDTH)
    for k in range(max(0, k_mid - 2), k_mid + 3):
        dy = (center_im - arb(k) * spacing).abs_lower()
        dx = (re_center - half_width).lower()
        # For n=0 and Re(s_0)>half_width, both coordinates are outside the
        # rectangle.  Keep the calculation explicit rather than using a
        # floating-point hypot so the lower bound is rounded downward.
        box_distance = (dx * dx + (dy - half_width) * (dy - half_width)).sqrt().lower()
        center_distance = (re_center * re_center + dy * dy).sqrt().lower()
        candidates.append({"n": 0, "k": k, "center_distance_lower": center_distance.str(80, more=True), "box_distance_lower": box_distance.str(80, more=True)})
    nearest = min(candidates, key=lambda row: float(arb(row["box_distance_lower"]).lower()))
    receipt = {"schema": "q8-ks-lattice-product-probe/v1", "status": "PROBE_AWAITING_COLD_REFEREE", "q": 8, "h": 3, "lambda": lam.str(80, more=True), "word": "M2*M1*M1", "trace": trace.str(80, more=True), "determinant": determinant.str(80, more=True), "hyperbolic_trace_lower": trace.lower().str(80, more=True), "ell": ell.str(80, more=True), "a": a.str(80, more=True), "vertical_spacing": spacing.str(80, more=True), "sigma_lower": sigma_lo.str(80, more=True), "t0_upper": t0.str(80, more=True), "product_terms": args.terms, "tail_sum_upper": tail_sum.str(80, more=True), "detKs_abs_lower": product_lower.str(80, more=True), "candidate_distances": candidates, "nearest_box_distance_lower": nearest["box_distance_lower"], "scope": "OPEN: the q=8 K_s cycle/word and product bound require a cold referee and MMS source-convention check before promotion", "box": {"re": PIN_RE, "im": PIN_IM, "half_width": HALF_WIDTH}}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"trace_lower": receipt["hyperbolic_trace_lower"], "ell": receipt["ell"], "vertical_spacing": receipt["vertical_spacing"], "nearest_box_distance_lower": receipt["nearest_box_distance_lower"], "detKs_abs_lower": receipt["detKs_abs_lower"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
