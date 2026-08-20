#!/usr/bin/env python3
"""q=8 E1 enlarged-disc contraction, regenerated at the q=7 GATED receipt standard.

The tracked probe lane_f/q8_e1_probe.py emits
lane_f/f8_receipts/Q8_E1_ENLARGED_PROBE_RECEIPT.json with
status = "DIAGNOSTIC_ONLY": no verdict, no immutable_inputs, no eta, per-source
rather than per-block rows, and a wall-clock runtime_seconds field that makes it
un-hash-pinnable.  The q=7 analogue
lane_f/f7_receipts/F7_E1_ENLARGED_CONTRACTION_V2_RECEIPT.json
(schema f7-e1-enlarged-contraction/v2, written by lane_f/f7_stage4b_reopt.py)
carries verdict, immutable_inputs, eta_max_upper_bound, per-block rows, and no
clock.

This driver reruns the SAME mathematics from the SAME tracked lane_f routines
and emits the q=7-standard artifact.  lane_f is read-only here: the module-level
THRESHOLD is set in-process, exactly as the tracked probe does at
q8_e1_probe.py:48-49, and nothing is written outside lane_g/binding_close/.

Two deliberate improvements over both predecessors, both of which the cold
referee flagged:

  1. The ratio DENOMINATOR CONVENTION is made explicit.  q8_tb_support.head_term
     divides by radii[j-1], and the probe passes enlarged_radii into BOTH slots
     of certify_block, so the probe's published rho_hat is
     ENLARGED-target-relative -- while q=7's receipt, under the same field name,
     is BASE-target-relative.  This receipt publishes BOTH, each under an
     unambiguous name, and derives the base-relative value from the certified
     sups directly rather than through the 1.15 inflation shortcut.
  2. Per-block remaining pole/branch-cut clearance is recorded (the diagnostic
     recorded clearance per SOURCE DISC only), and the live threshold is
     recorded, which the diagnostic never did.

Bounds: ratios and sups are certified UPPER endpoints (UP); clearances,
enlargements and margins are certified LOWER endpoints (DOWN).
Receipt is sorted-key and clock-free, hence hash-pinnable.
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
DIGITS = 100
E1_THRESHOLD_TEXT = "0.99"
ENLARGEMENT_MARGIN_DIVISOR = 4
ENLARGEMENT_RELATIVE_CAP = "0.15"

OUT_DEFAULT = HERE / "Q8_E1_ENLARGED_CONTRACTION_GATED_RECEIPT.json"
TB_RECEIPT = LANE_F / "f8_receipts" / "Q8_TB_BLOCK_CERTIFICATES_F1024_RECEIPT.json"
PROBE_RECEIPT = LANE_F / "f8_receipts" / "Q8_E1_ENLARGED_PROBE_RECEIPT.json"

# Refuse to proceed if the pinned inputs moved (q=7 guard, f7_stage4b_reopt.py:78-79).
TB_EXPECTED_SHA256 = "5f9cd3f9179c5b15539b3666bd3a2a3144995408648369dc1db6eda36f51d35c"
PROBE_EXPECTED_SHA256 = "7b0f0df79dd7c98ac4ede0673ef9fb189c093d6cb5ea24da470df70131799c96"


def txt(value: arb) -> str:
    return value.str(DIGITS, more=True)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--M", type=int, default=512)
    parser.add_argument("--K-start", type=int, default=12)
    parser.add_argument("--K-max", type=int, default=64)
    parser.add_argument("--out", type=Path, default=OUT_DEFAULT)
    parser.add_argument("--allow-input-drift", action="store_true")
    args = parser.parse_args()
    ctx.prec = PREC_BITS

    tb_sha = sha256(TB_RECEIPT)
    probe_sha = sha256(PROBE_RECEIPT)
    if not args.allow_input_drift and (tb_sha != TB_EXPECTED_SHA256
                                       or probe_sha != PROBE_EXPECTED_SHA256):
        raise SystemExit("immutable TB / E1-probe receipt hashes changed — refuse to proceed")

    lam = f8.lam_ball()
    points, centers, half, multipliers, base_radii = f8.disc_geometry_for(lam, FACTORS)
    kappa = f8.KAPPA

    pole_rows, cut_rows = tb.clearance_rows(f8.BLOCKS, centers, base_radii, lam)

    # Per-SOURCE-DISC clearance, exactly as q8_e1_probe.py:36-41.
    source_clearances = []
    for source in range(1, kappa + 1):
        margins = [arb(row["margin"]) for row in pole_rows + cut_rows
                   if row["block"][0] == source]
        source_clearances.append(min(margins, key=lambda value: value.lower()).lower())

    # Per-BLOCK clearance (new here; the diagnostic recorded only the per-source min).
    block_clearance = {}
    for row in pole_rows + cut_rows:
        key = tuple(row["block"])
        margin = arb(row["margin"])
        if key not in block_clearance or margin.lower() < block_clearance[key].lower():
            block_clearance[key] = margin

    enlargements = []
    for index, radius in enumerate(base_radii):
        enlargements.append(min(source_clearances[index] / arb(ENLARGEMENT_MARGIN_DIVISOR),
                                arb(ENLARGEMENT_RELATIVE_CAP) * radius.lower()))
    enlarged_radii = [base_radii[i] + enlargements[i] for i in range(kappa)]

    # E1 needs only rho_hat < 1; the base TB support's stricter internal 0.70
    # would reject legitimate enlargements. Same override as q8_e1_probe.py:48-49,
    # applied IN PROCESS ONLY and recorded in the receipt below.
    tb.THRESHOLD = arb(E1_THRESHOLD_TEXT)
    tb.THRESHOLD_TEXT = E1_THRESHOLD_TEXT

    per_block = []
    ok = True
    rho_enl = None
    rho_enl_label = None
    rho_base = None
    rho_base_label = None
    eta_max = None
    for block in f8.BLOCKS:
        i, j, n0, neg, tail = block
        row, _, _ = tb.certify_block(block, centers, enlarged_radii, lam,
                                     args.M, args.K_start, args.K_max)
        sup = arb(row["certified_sup_upper_bound"])
        ratio_enl = arb(row["ratio_upper_bound"])
        ratio_base = sup / base_radii[j - 1]
        eta = base_radii[i - 1] / enlarged_radii[i - 1]
        clearance = block_clearance[tuple(block)]
        remaining = clearance - enlargements[i - 1]
        lt_one_enl = bool(tb.definitely_negative(ratio_enl - arb(1)))
        lt_one_base = bool(tb.definitely_negative(ratio_base - arb(1)))
        eta_lt_one = bool(tb.definitely_negative(eta - arb(1)))
        remaining_positive = bool(tb.definitely_positive(remaining))
        block_ok = bool(row["pass"]) and lt_one_enl and lt_one_base and eta_lt_one \
            and remaining_positive
        ok = ok and block_ok
        if rho_enl is None or ratio_enl.upper() > rho_enl.upper():
            rho_enl, rho_enl_label = ratio_enl, row["label"]
        if rho_base is None or ratio_base.upper() > rho_base.upper():
            rho_base, rho_base_label = ratio_base, row["label"]
        if eta_max is None or eta.upper() > eta_max.upper():
            eta_max = eta
        per_block.append({
            "block": list(block),
            "label": row["label"],
            "tail": bool(tail),
            "source_disc": i,
            "target_disc": j,
            "n0": n0,
            "K_used": row["K_used"],
            "method_kind": ("enlarged_source_arc_cover_with_crude_deep_tail" if tail
                            else "enlarged_source_arc_cover_single_head"),
            "original_radius_upper_bound": txt(base_radii[i - 1]),
            "enlargement_lower_bound": txt(enlargements[i - 1]),
            "enlarged_radius": txt(enlarged_radii[i - 1]),
            "eta_R_over_R_enlarged_upper_bound": txt(eta),
            "eta_strictly_below_one": eta_lt_one,
            "certified_sup_upper_bound": row["certified_sup_upper_bound"],
            "certified_clearance_lower_bound": txt(clearance),
            "remaining_pole_cut_clearance_lower_bound": txt(remaining),
            "remaining_clearance_strictly_positive": remaining_positive,
            "ratio_upper_bound_enlarged_target_relative": row["ratio_upper_bound"],
            "ratio_upper_bound_base_target_relative": txt(ratio_base),
            "ratio_less_than_one_enlarged_target_relative": lt_one_enl,
            "ratio_less_than_one_base_target_relative": lt_one_base,
            "pass": block_ok,
        })

    # Reproduction check against the pinned DIAGNOSTIC artifact: the enlarged-
    # relative rho_hat must be string-identical to what the tracked probe published.
    probe = json.loads(PROBE_RECEIPT.read_text(encoding="utf-8"))
    probe_rho = probe["rho_hat_upper_bound"]
    reproduces = (rho_enl.str(80, more=True) == probe_rho)

    verdict = "PASS_RHO_HAT_LT_1" if (ok and reproduces) else "FAIL"

    receipt = {
        "schema": "q8-e1-enlarged-contraction/v2-gated",
        "role": ("q=8 analogue of lane_f/f7_receipts/F7_E1_ENLARGED_CONTRACTION_V2_RECEIPT.json; "
                 "supersedes the DIAGNOSTIC_ONLY lane_f/f8_receipts/Q8_E1_ENLARGED_PROBE_RECEIPT.json"),
        "verdict": verdict,
        "gate": "rho_hat < 1 on the ENLARGED source contours (all 8 eq.(32) blocks), in BOTH denominator conventions",
        "q": 8,
        "even_q": True,
        "h_q": kappa,
        "kappa": kappa,
        "backend": "python-flint Arb/Acb ball arithmetic",
        "precision_bits": PREC_BITS,
        "M_enlarged_contour_arcs": args.M,
        "K_start": args.K_start,
        "K_max": args.K_max,
        "lambda": txt(lam),
        "lambda_exact_form": "sqrt(2 + sqrt(2))",
        "radius_multipliers_exact_strings": list(FACTORS),
        "partition_points": [txt(value) for value in points],
        "centers": [txt(value) for value in centers],
        "base_radii": [txt(value) for value in base_radii],
        "source_clearance_lower_bound": [txt(value) for value in source_clearances],
        "enlargement_lower_bound": [txt(value) for value in enlargements],
        "enlarged_radii": [txt(value) for value in enlarged_radii],
        "enlargement_rule": "e_i = min(clearance_i / 4, 0.15 * R_i), clearance per SOURCE DISC",
        "enlargement_margin_divisor": ENLARGEMENT_MARGIN_DIVISOR,
        "enlargement_relative_cap": ENLARGEMENT_RELATIVE_CAP,
        "threshold_used_for_internal_term_gate": E1_THRESHOLD_TEXT,
        "threshold_note": (
            "q8_tb_support.THRESHOLD is set in-process to 0.99 for this run, as the "
            "tracked probe does at q8_e1_probe.py:48-49. The per-term key emitted by "
            "q8_tb_support is hardcoded 'ratio_less_than_0_70' and is therefore "
            "MISNAMED under this override; the gate that matters here is rho_hat < 1, "
            "recorded explicitly per block in both conventions."
        ),
        "denominator_convention": {
            "enlarged_target_relative": (
                "q8_tb_support.head_term divides by radii[j-1]; certify_block is called "
                "with enlarged_radii in BOTH slots, so this is the convention the "
                "tracked DIAGNOSTIC probe published under the bare name rho_hat_upper_bound"
            ),
            "base_target_relative": (
                "certified sup divided by the BASE target radius r_j; this is the "
                "convention F7_E1_ENLARGED_CONTRACTION_V2_RECEIPT.json uses under that "
                "same bare name, and it is the one the Hardy/Hilbert norm chain needs"
            ),
        },
        "rho_hat_upper_bound_enlarged_target_relative": txt(rho_enl),
        "rho_hat_worst_block_label_enlarged_target_relative": rho_enl_label,
        "rho_hat_upper_bound_base_target_relative": txt(rho_base),
        "rho_hat_worst_block_label_base_target_relative": rho_base_label,
        "rho_hat_less_than_one_enlarged_target_relative": bool(tb.definitely_negative(rho_enl - arb(1))),
        "rho_hat_less_than_one_base_target_relative": bool(tb.definitely_negative(rho_base - arb(1))),
        "eta_max_upper_bound": txt(eta_max),
        "all_eta_strictly_below_one": all(row["eta_strictly_below_one"] for row in per_block),
        "all_remaining_clearances_positive": all(row["remaining_clearance_strictly_positive"] for row in per_block),
        "block_count": len(per_block),
        "block_count_expected": 8,
        "per_block": per_block,
        "reproduces_pinned_diagnostic_probe": reproduces,
        "pinned_diagnostic_rho_hat_upper_bound": probe_rho,
        "immutable_inputs": {
            "TB_F1024_receipt_sha256": tb_sha,
            "TB_F1024_certified_rho_star_upper_bound":
                json.loads(TB_RECEIPT.read_text(encoding="utf-8"))["rho_star_upper_bound"],
            "E1_diagnostic_probe_receipt_sha256": probe_sha,
            "geometry_source": "lane_f/f8_certify_tb_blocks.disc_geometry_for(lam, ('10','4','2'))",
            "block_source": "lane_f/f8_certify_tb_blocks.BLOCKS (MMS eq.(32), h=kappa=3, 8 occurrences)",
        },
        "scope": (
            "Certifies E1 enlarged-disc strict contraction for the 8 eq.(32) blocks at "
            "q=8, in both denominator conventions, with per-block eta and remaining "
            "pole/branch-cut clearance. Enlarged-disc weight HOLOMORPHY is proved "
            "separately (HARDY_HILBERT_BINDING_SOL.md B6a) and consumed here only "
            "through the recorded positive remaining clearances. Contour, R2/R3, K_s "
            "nonvanishing, the omitted-output tail and full_tail_certified remain OPEN."
        ),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "verdict": verdict,
        "rho_hat_enlarged_relative": receipt["rho_hat_upper_bound_enlarged_target_relative"][:34],
        "rho_hat_base_relative": receipt["rho_hat_upper_bound_base_target_relative"][:34],
        "worst_base_block": rho_base_label,
        "eta_max": receipt["eta_max_upper_bound"][:34],
        "reproduces_pinned_diagnostic_probe": reproduces,
        "blocks": len(per_block),
    }, indent=2))
    return 0 if verdict == "PASS_RHO_HAT_LT_1" else 1


if __name__ == "__main__":
    raise SystemExit(main())
