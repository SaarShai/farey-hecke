#!/usr/bin/env python3
"""Threshold-split hygiene audit of Q8_TB_BLOCK_CERTIFICATES_F1024_RECEIPT.json.

The receipt is written by two unconnected gates:

  * every PER-TERM flag was evaluated against q8_tb_support.THRESHOLD, whose
    module default is arb("0.70") (q8_tb_support.py:17-18).  The producing
    driver lane_f/q8_candidate_tb_cert.py imports f8_certify_tb_blocks only for
    geometry (:31-33) and never calls its run(), so the 0.99 re-target at
    f8_certify_tb_blocks.py:396-397 never executes;
  * the TOP-LEVEL rho gate and certification_verdict were written against a
    hardcoded "0.99" literal (q8_candidate_tb_cert.py:71-73, :79).

The direction is conservative -- per-term flags were gated STRICTER than the
headline verdict claims -- but two numbers in one hash-pinned receipt are gated
differently, and the per-term key is literally named "ratio_less_than_0_70"
(q8_tb_support.py:125,154,166,183,211) regardless of the live THRESHOLD, so the
name is unreliable as evidence in general.

This audit re-reads every certified ratio out of the pinned receipt and
re-evaluates it against BOTH thresholds in Arb, so the conservativeness is a
receipt fact rather than an argument.  It changes nothing in lane_f.

Bounds: ratios are the receipt's certified UPPER endpoints; margins DOWN.
Outputs a hash-pinnable JSON receipt: sorted keys, no wall-clock field.
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

import q8_tb_support as tb  # noqa: E402

PREC_BITS = 384
DIGITS = 30
TB_RECEIPT = LANE_F / "f8_receipts" / "Q8_TB_BLOCK_CERTIFICATES_F1024_RECEIPT.json"
OUT_DEFAULT = HERE / "Q8_THRESHOLD_SPLIT_AUDIT_RECEIPT.json"
STRICT = "0.70"
HEADLINE = "0.99"


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
    parser.add_argument("--out", type=Path, default=OUT_DEFAULT)
    args = parser.parse_args()
    ctx.prec = PREC_BITS

    data = json.loads(TB_RECEIPT.read_text(encoding="utf-8"))
    strict = arb(STRICT)
    headline = arb(HEADLINE)

    rows = []
    term_count = 0
    worst = None
    worst_label = None
    for block in data["blocks"]:
        label = block["label"]
        terms = []
        for term in block.get("head_terms", []):
            terms.append(("head", term.get("n"), term["ratio_upper_bound"],
                          term.get("ratio_less_than_0_70"), term.get("pass")))
        deep = block.get("deep_tail")
        if deep is not None:
            terms.append(("deep_tail", deep.get("first_n"), deep["ratio_upper_bound"],
                          deep.get("ratio_less_than_0_70"), deep.get("pass")))
        block_rows = []
        for kind, n, ratio_text, flag070, flag_pass in terms:
            term_count += 1
            ratio = arb(ratio_text)
            lt_strict = bool(tb.definitely_negative(ratio - strict))
            lt_headline = bool(tb.definitely_negative(ratio - headline))
            if worst is None or ratio.upper() > worst.upper():
                worst = ratio
                worst_label = f"{label} [{kind} n={n}]"
            block_rows.append({
                "kind": kind,
                "n": n,
                "ratio_upper_bound": ratio_text,
                "recomputed_lt_0_70": lt_strict,
                "recomputed_lt_0_99": lt_headline,
                "receipt_flag_named_ratio_less_than_0_70": flag070,
                "receipt_flag_agrees_with_0_70_recomputation": (flag070 == lt_strict),
                "margin_to_0_70_lower_bound": txt(strict - ratio),
            })
        rows.append({
            "block": block["block"],
            "label": label,
            "block_ratio_upper_bound": block["ratio_upper_bound"],
            "block_pass": block.get("pass"),
            "gated_at": STRICT,
            "terms": block_rows,
        })

    rho = arb(data["rho_star_upper_bound"])
    rho_lt_strict = bool(tb.definitely_negative(rho - strict))
    rho_lt_headline = bool(tb.definitely_negative(rho - headline))
    all_terms_lt_strict = all(t["recomputed_lt_0_70"] for b in rows for t in b["terms"])
    all_flags_agree = all(t["receipt_flag_agrees_with_0_70_recomputation"]
                          for b in rows for t in b["terms"])

    conservative = all_terms_lt_strict and rho_lt_strict and rho_lt_headline

    receipt = {
        "schema": "q8-threshold-split-audit/v1",
        "role": "threshold-split hygiene for Q8_TB_BLOCK_CERTIFICATES_F1024_RECEIPT.json",
        "verdict": "PASS_MIXED_THRESHOLDS_ARE_CONSERVATIVE" if conservative else "FAIL",
        "q": 8,
        "backend": "python-flint Arb/Acb ball arithmetic",
        "precision_bits": PREC_BITS,
        "split_description": {
            "per_term_flags_gated_at": STRICT,
            "per_term_gate_code": "q8_tb_support.py:17-18 (module default), read at :118 and :142",
            "why_not_overridden": (
                "lane_f/q8_candidate_tb_cert.py:31-33 imports f8_certify_tb_blocks for "
                "geometry only and never calls run(), so the 0.99 re-target at "
                "f8_certify_tb_blocks.py:396-397 never executes"
            ),
            "headline_verdict_gated_at": HEADLINE,
            "headline_gate_code": "q8_candidate_tb_cert.py:71-73, :79 (hardcoded literals)",
            "receipt_threshold_field_is_bare_string_not_arb_ball": (
                data.get("threshold") == HEADLINE
            ),
            "key_name_hazard": (
                "the per-term key is literally 'ratio_less_than_0_70' at "
                "q8_tb_support.py:125,154,166,183,211 regardless of the live "
                "THRESHOLD; in this receipt the name happens to be truthful, but the "
                "same key is FALSE-BY-NAME in F7_TB_BLOCK_CERTIFICATES_RECEIPT.json "
                "(gated 0.80) and F8_TB_BLOCK_CERTIFICATES_RECEIPT.json (gated 0.99). "
                "The name must never be cited as evidence of a 0.70 gate."
            ),
        },
        "conservativeness_argument": (
            "0.70 < 0.99, and the per-term flags carry the STRICTER gate while the "
            "headline verdict carries the LOOSER one. Any term that passed at 0.70 "
            "passes at 0.99; the recorded verdict PASS_RHO_LT_0.99 is therefore "
            "implied by, and strictly weaker than, what was actually certified. The "
            "residual risk of the split runs the other way -- a run whose declared "
            "gate is 0.99 could have been REJECTED by the un-overridden 0.70 "
            "per-term gate (certify_block raises when no K passes), producing a "
            "spurious failure, never a spurious pass."
        ),
        "terms_audited": term_count,
        "all_terms_below_0_70": all_terms_lt_strict,
        "all_receipt_flags_agree_with_0_70_recomputation": all_flags_agree,
        "rho_star_upper_bound": data["rho_star_upper_bound"],
        "rho_star_lt_0_70": rho_lt_strict,
        "rho_star_lt_0_99": rho_lt_headline,
        "rho_star_margin_to_0_70_lower_bound": txt(strict - rho),
        "worst_term_ratio_upper_bound": txt(worst),
        "worst_term_label": worst_label,
        "blocks": rows,
        "immutable_inputs": {
            "TB_F1024_receipt_sha256": sha256(TB_RECEIPT),
            "receipt_certification_verdict": data.get("certification_verdict"),
            "receipt_threshold_text": data.get("threshold_text"),
        },
        "recommendation": (
            "Re-emit the F1024 receipt from a driver that sets q8_tb_support.THRESHOLD "
            "explicitly and records the value it used, and rename the per-term key to "
            "carry the live threshold. Until then this audit, not the receipt's own "
            "field names, is the citable evidence for what was gated at what."
        ),
        "scope": (
            "Audits only the threshold bookkeeping of the pinned TB receipt. Does not "
            "re-derive the ratios from geometry (they are consumed as the receipt's "
            "certified upper endpoints) and bears on no other gate."
        ),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "verdict": receipt["verdict"],
        "terms_audited": term_count,
        "all_terms_below_0_70": all_terms_lt_strict,
        "all_flags_agree": all_flags_agree,
        "worst_term": worst_label,
        "worst_ratio": receipt["worst_term_ratio_upper_bound"],
        "rho_margin_to_0_70": receipt["rho_star_margin_to_0_70_lower_bound"],
    }, indent=2))
    return 0 if conservative else 1


if __name__ == "__main__":
    raise SystemExit(main())
