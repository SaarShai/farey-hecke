#!/usr/bin/env python3
"""R-B8-2: certified admissibility of the q=8 checker discs as MMS Lemma 4.4 discs.

MMS (arXiv:0912.2236v2, sha256 a10020bd08...) Lemma 4.4 asserts the EXISTENCE of
open discs D_i (i in A_kappa = {+-1..+-kappa}) with

    Phi_i subset D_i        and     vartheta_n(D_i) subset D_j  for all n in N_{i,j},

where (eq.(13), p.10) Phi_i := [phi_{i-1}, phi_i] is the Markov cell itself,
vartheta_n = S T^n, i.e. vartheta_n(z) = -1/(z + n*lambda), and for q = 2h+2
(Lemma 4.2, p.13-14)

    N_{1,h} = Z_{>=2},  N_{1,-h} = Z_{<=-1},
    N_{i,i-1} = {1},  N_{i,h} = Z_{>=2},  N_{i,-h} = Z_{<=-1}   (2 <= i <= h).

Lemma 4.4 is an EXISTENCE statement; its proof exhibits ONE admissible family
(intervals I_i = ([[-1;(-1)^i]], lambda/4), Lemma 4.7 / p.19).  It does not
single that family out.  Any disc family satisfying the two displayed
conditions is an admissible realization, and the whole of MMS section 4/5
(nuclearity Thm 4.10, the B = (+) B(D_i) construction, Lemma 5.1) uses only
those two conditions.

This script certifies, in 384-bit Arb ball arithmetic, that the checker's own
discs D_i := D(c_i, a_i h_i), (a_1,a_2,a_3) = (10,4,2) -- the F1024 geometry
that lane_f/f8_certify_tb_blocks.py builds and that every pinned q=8 receipt
uses -- satisfy exactly those two conditions at q=8, h=kappa=3.

Conventions.  All discs are OPEN and real-centred, so each is the disc whose
diameter is its real trace.  vartheta_n is a Moebius map with REAL
coefficients, so it commutes with complex conjugation; provided its pole
-n*lambda lies outside the closed real trace [c-r, c+r], it maps D(c,r) onto
the open disc whose diameter is the image interval.  Image centre/radius are
therefore computed exactly from the two endpoint images.

Bounds: containment margins are certified LOWER endpoints (DOWN); the
uniform-tail threshold uses UPPER endpoints (UP).  A check passes only if the
strict inequality is certified by the ball arithmetic (no overlap with 0).

Outputs a hash-pinnable JSON receipt: sorted keys, no wall-clock field.
Reads lane_f; writes only into lane_g/binding_close/.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from flint import arb, ctx

HERE = Path(__file__).resolve().parent
LANE_G = HERE.parent
LANE_F = LANE_G.parent / "lane_f"
sys.path.insert(0, str(LANE_F))

import f8_certify_tb_blocks as f8  # noqa: E402
import q8_tb_support as tb  # noqa: E402

FACTORS = ("10", "4", "2")
PREC_BITS = 384
DIGITS = 40
N_CHECK_DEFAULT = 8
OUT_DEFAULT = HERE / "Q8_MMS_DISC_ADMISSIBILITY_RECEIPT.json"

TB_RECEIPT = LANE_F / "f8_receipts" / "Q8_TB_BLOCK_CERTIFICATES_F1024_RECEIPT.json"
MMS_PDF = LANE_G / "MMS_arxiv_0912.2236.pdf"


def txt(value: arb) -> str:
    return value.str(DIGITS, more=True)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def strictly_positive(value: arb) -> bool:
    return bool(tb.definitely_positive(value))


class Disc:
    """Open real-centred disc D(centre, radius)."""

    def __init__(self, centre: arb, radius: arb, name: str) -> None:
        self.c = centre
        self.r = radius
        self.name = name

    def contains(self, other: "Disc") -> tuple[bool, arb]:
        """Certified strict containment self ) other, with margin r - |dc| - r'."""
        margin = self.r - (self.c - other.c).abs_upper() - other.r
        return strictly_positive(margin), margin


def theta(n: int, lam: arb) -> tuple[arb, arb]:
    """vartheta_n(z) = -1/(z + n*lambda): returns (pole, sign) with map -1/(z-pole)."""
    return -arb(n) * lam, arb(-1)


def image_disc(disc: Disc, n: int, lam: arb, name: str) -> tuple[Disc, arb]:
    """Exact image of an open real-centred disc under vartheta_n.

    Returns (image disc, certified pole clearance = |pole - c| - r).
    """
    pole, sign = theta(n, lam)
    clearance = (disc.c - pole).abs_lower() - disc.r
    left = disc.c - disc.r
    right = disc.c + disc.r
    u = sign / (left - pole)
    v = sign / (right - pole)
    centre = (u + v) / arb(2)
    radius = (u - v).abs_upper() / arb(2)
    return Disc(centre, radius, name), clearance


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-check", type=int, default=N_CHECK_DEFAULT)
    parser.add_argument("--out", type=Path, default=OUT_DEFAULT)
    args = parser.parse_args()
    ctx.prec = PREC_BITS

    lam = f8.lam_ball()
    points, centers, half, multipliers, radii = f8.disc_geometry_for(lam, FACTORS)
    h = f8.KAPPA
    assert h == 3

    D = {i: Disc(centers[i - 1], radii[i - 1], f"D_{i}") for i in range(1, h + 1)}
    for i in range(1, h + 1):
        D[-i] = Disc(-centers[i - 1], radii[i - 1], f"D_-{i}")

    checks: list[dict] = []
    ok = True

    def record(kind: str, i: int, j: int, n: int | None, passed: bool,
               margin: arb, extra: dict | None = None) -> None:
        nonlocal ok
        row = {
            "check": kind,
            "source_disc": i,
            "target_disc": j,
            "n": n,
            "margin_lower_bound": txt(margin),
            "pass": bool(passed),
        }
        if extra:
            row.update(extra)
        checks.append(row)
        ok = ok and bool(passed)

    # ---- C0: Phi_i = [phi_{i-1}, phi_i] subset D_i (MMS eq.(13) cell) --------
    for i in range(1, h + 1):
        left_margin = radii[i - 1] - (points[i - 1] - centers[i - 1]).abs_upper()
        right_margin = radii[i - 1] - (points[i] - centers[i - 1]).abs_upper()
        margin = left_margin if left_margin.lower() < right_margin.lower() else right_margin
        record("C0_Phi_i_in_D_i", i, i, None, strictly_positive(margin), margin,
               {"phi_left": txt(points[i - 1]), "phi_right": txt(points[i])})

    # ---- C3: vartheta_1(D_i) subset D_{i-1}, N_{i,i-1} = {1}, 2 <= i <= h ----
    for i in range(2, h + 1):
        img, clearance = image_disc(D[i], 1, lam, f"theta_1(D_{i})")
        passed_c, margin = D[i - 1].contains(img)
        record("C3_head_theta1", i, i - 1, 1,
               passed_c and strictly_positive(clearance), margin,
               {"pole_clearance_lower_bound": txt(clearance),
                "image_centre": txt(img.c), "image_radius_upper_bound": txt(img.r),
                "N_ij": "{1}"})

    # ---- C1: vartheta_n(D_i) subset D_h for n >= 2  (N_{i,h} = Z_{>=2}) -----
    # ---- C2: vartheta_{-n}(D_i) subset D_{-h} for n >= 1 (N_{i,-h}=Z_{<=-1}) -
    families = [("C1_tail_positive", 2, +1, h), ("C2_tail_negative", 1, -1, -h)]
    tail_lemma: list[dict] = []
    for kind, n0, sgn, target in families:
        for i in range(1, h + 1):
            for k in range(n0, args.n_check + 1):
                n = sgn * k
                img, clearance = image_disc(D[i], n, lam, f"theta_{n}(D_{i})")
                passed_c, margin = D[target].contains(img)
                record(kind, i, target, n,
                       passed_c and strictly_positive(clearance), margin,
                       {"pole_clearance_lower_bound": txt(clearance),
                        "image_centre": txt(img.c),
                        "image_radius_upper_bound": txt(img.r)})
            # uniform tail: |theta_n(z)| <= 1/(d_n - r_i) for all z in D_i, and
            # D(0, eps) subset D_{+-h} whenever eps < r_h - |c_h| = h_h.
            n_first = sgn * (args.n_check + 1)
            pole, _ = theta(n_first, lam)
            d = (D[i].c - pole).abs_lower()
            gap = d - D[i].r
            inner = radii[h - 1] - centers[h - 1].abs_upper()  # r_h - |c_h| = h_h
            crit = gap * inner - arb(1)
            passed = strictly_positive(gap) and strictly_positive(crit)
            ok = ok and passed
            tail_lemma.append({
                "check": f"{kind}_uniform_tail",
                "source_disc": i,
                "target_disc": target,
                "n_from": n_first,
                "distance_to_pole_lower_bound": txt(d),
                "gap_d_minus_r_lower_bound": txt(gap),
                "inner_radius_of_target_lower_bound": txt(inner),
                "criterion_gap_times_inner_minus_one_lower_bound": txt(crit),
                "monotone_in_n_step": txt(lam),
                "pass": bool(passed),
            })

    receipt = {
        "schema": "q8-mms-disc-admissibility/v1",
        "role": "R-B8-2: checker discs are admissible MMS Lemma 4.4 discs at q=8",
        "verdict": "PASS_ADMISSIBLE" if ok else "FAIL",
        "q": 8,
        "even_q": True,
        "h_q": h,
        "kappa": h,
        "backend": "python-flint Arb/Acb ball arithmetic",
        "precision_bits": PREC_BITS,
        "lambda": txt(lam),
        "lambda_exact_form": "sqrt(2 + sqrt(2))",
        "radius_multipliers_exact_strings": list(FACTORS),
        "partition_points": [txt(value) for value in points],
        "centers": [txt(value) for value in centers],
        "base_radii": [txt(value) for value in radii],
        "mms_conditions": {
            "source": "MMS arXiv:0912.2236v2, Lemma 4.4 (p.16), Phi_i per eq.(13) p.10, N_{i,j} per Lemma 4.2 p.13-14",
            "condition_1": "Phi_i subset D_i",
            "condition_2": "vartheta_n(D_i) subset D_j for all n in N_{i,j}",
            "vartheta": "vartheta_n(z) = -1/(z + n*lambda)   (= S T^n)",
            "N_ij_even_q": {
                "N_{1,h}": "Z_{>=2}", "N_{1,-h}": "Z_{<=-1}",
                "N_{i,i-1}": "{1} for 2<=i<=h",
                "N_{i,h}": "Z_{>=2} for 2<=i<=h",
                "N_{i,-h}": "Z_{<=-1} for 2<=i<=h",
                "all_other_pairs": "empty",
            },
            "negative_index_reduction": (
                "D_{-i} := -D_i.  Phi_{-i} = -Phi_i (eq.(13)), N_{-i,j} = -N_{i,-j} "
                "(Lemma 4.2), and vartheta_{-n}(-z) = -vartheta_n(z); hence every "
                "condition at a negative source index is the exact mirror of one "
                "verified here.  No further computation is required."
            ),
        },
        "n_checked_explicitly_through": args.n_check,
        "checks": checks,
        "uniform_tail_lemma": tail_lemma,
        "all_checks_pass": ok,
        "immutable_inputs": {
            "TB_F1024_receipt_sha256": sha256(TB_RECEIPT),
            "MMS_pdf_sha256": sha256(MMS_PDF),
            "geometry_source": "lane_f/f8_certify_tb_blocks.disc_geometry_for(lam, ('10','4','2'))",
        },
        "scope": (
            "Certifies the two defining conditions of MMS Lemma 4.4 for the checker's "
            "F1024 discs at q=8. Does NOT claim the checker discs equal MMS's own "
            "exhibited intervals of Lemma 4.7/p.19 (they do not); Lemma 4.4 is an "
            "existence statement and section 4/5 use only the two conditions."
        ),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    failures = [row for row in checks + tail_lemma if not row["pass"]]
    print(json.dumps({
        "verdict": receipt["verdict"],
        "checks": len(checks),
        "tail_lemmas": len(tail_lemma),
        "failures": failures[:5],
    }, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
