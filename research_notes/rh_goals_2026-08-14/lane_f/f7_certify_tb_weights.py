#!/usr/bin/env python3
"""q=7 T-b certified weight envelope (schema tb-weight-envelope-cert/v2).

Port of `tb_certify/certify_tb_weights_v2.py` to q=7.  This stage is an
UNDOCUMENTED PREREQUISITE of the R2 envelope: `certify_r2_flagship.py`
validates the schema string and consumes, per block,
`plain_weight_sup_upper_bound` (load-bearing for single branches and for the
deep-tail cross-check) and, per head term, `v2_image_ratio_upper_bound`
(cross-checked against the TB V2 receipt's own head ratio).

All the mathematics is reused from the q=5 module: `weight_sup`,
`hurwitz_phi0_sup`, `deep_weight_image_bound` and `certify_block` take
(centers, radii, lam, arcs, s) as arguments and are q-independent.  What is new
here is only the q=7 geometry (read from the q=7 TB receipt), the single q=7
flagship pin, kappa=5 row aggregation, and the 19-block source.

Difference in scope from q=5, stated explicitly: the q=5 receipt closed with a
PASS/NOT verdict against per-pin T-c contour lower bounds.  There is no T-c
stage at q=7 in stages 1-2, so no such verdict is manufactured: the receipt
carries the certified W envelopes and marks the contour comparison
NOT_APPLICABLE_NO_Q7_TC_STAGE.  Nothing downstream (R2) reads that field.

All reported values are Arb upper endpoints (rounded UP).
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import sys
import time
from pathlib import Path
from typing import Any

CODE_DIR = Path("/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code")
sys.path.insert(0, str(CODE_DIR / "tb_certify"))
sys.path.insert(0, str(CODE_DIR))

from flint import acb, arb, ctx  # noqa: E402

import certify_tb_blocks as tb  # noqa: E402
import certify_tb_weights_v2 as w  # noqa: E402


PREC_BITS = 384
M_DEFAULT = 512
Q = 7
KAPPA = 5
N_DEFAULT = 224
PIN_NAME = "g7_pin_1"
PIN_RE = "0.4751647621098225"
PIN_IM = "4.668743786424289"
HALF_WIDTH = "1e-6"

LANE_F = Path("/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_f")
DEFAULT_RECEIPT_DIR = LANE_F / "f7_receipts"
BLOCKS_RECEIPT_DEFAULT = DEFAULT_RECEIPT_DIR / "F7_TB_BLOCK_CERTIFICATES_RECEIPT.json"
SWEEP_DEFAULT = LANE_F / "f7_tb_disc_sweep.py"
REPORT_NAME = "F7_W_ENVELOPE_CERT.md"
RECEIPT_NAME = "F7_W_ENVELOPE_CERT_RECEIPT.json"

Block = tuple[int, int, int, bool, bool]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_blocks(path: Path) -> tuple[list[Block], int]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "BLOCKS" for target in node.targets
        ):
            return [tuple(item) for item in ast.literal_eval(node.value)], node.lineno
    raise ValueError(f"BLOCKS assignment not found in {path}")


def s_box() -> tuple[acb, dict[str, Any]]:
    hx = arb(HALF_WIDTH)
    re = arb(PIN_RE) + arb(0, hx)
    im = arb(PIN_IM) + arb(0, hx)
    return acb(re, im), {
        "center": {"re": PIN_RE, "im": PIN_IM},
        "half_width": {"re": w.arb_text(hx), "im": w.arb_text(hx)},
        "re_interval": w.arb_text(re),
        "im_interval": w.arb_text(im),
        "principal_branch": True,
    }


def geometry(v2: dict[str, Any]):
    lam = arb(v2["lambda"])
    centers = [arb(value) for value in v2["centers"]]
    radii = [arb(value) for value in v2["source_radii"]]
    multipliers = [arb(value) for value in v2["radius_multipliers"]]
    arcs = [
        [tb.arc_ball(centers[i], radii[i], index, M_DEFAULT) for index in range(M_DEFAULT)]
        for i in range(KAPPA)
    ]
    return lam, centers, radii, multipliers, arcs


def f_bound(W: arb, rho: arb, N: int) -> arb:
    value = (arb(1) + arb(KAPPA) * W / (arb(1) - rho)).exp()
    return value * (arb(KAPPA) * W * rho**N / (arb(1) - rho))


def render_report(receipt: dict[str, Any], code_path: Path, receipt_path: Path) -> str:
    box = receipt["boxes"][0]
    lines = [
        "# F7 — q=7 T-b certified weight envelope (iteration-2 schema)",
        "",
        "## VERDICT SUMMARY",
        "",
        f"Box `{box['name']}` (closed {HALF_WIDTH} Acb s-box around "
        f"{PIN_RE} + {PIN_IM}i), kappa = {KAPPA}, {receipt['blocks_source']['count']} blocks.",
        "",
        "| box | W^(>=1) | W^(0) sanity | F at N | rho* used | contour lower bound |",
        "|---|---:|---:|---:|---:|---|",
        f"| {box['name']} | `{box['W_ge1_upper_bound']}` | `{box['W0_upper_bound']}` | "
        f"`{receipt['summary'][0]['F_upper_bound']}` (N={receipt['N_evaluation']}) | "
        f"`{receipt['rho_star']}` | {receipt['summary'][0]['contour_lower_bound']} |",
        "",
        "`W^(0)` is a conditioning sanity value and does not enter `F`. No PASS/NOT "
        "verdict is issued: q=7 has no T-c stage in stages 1-2, so there is no certified "
        "contour lower bound to compare against, and none is invented here.",
        "",
        "## Method",
        "",
        f"- Backend: `{receipt['backend']}`, precision `{receipt['precision_bits']}` bits, "
        f"closed-arc cover `M={receipt['M']}`.",
        f"- The {receipt['blocks_source']['count']} allowed blocks and every finite tail head "
        "ratio are read from the q=7 TB block receipt; no tail branch is re-summed term by term.",
        "- Deep image factor `|theta_n|/R_j <= 1/(R_j*d_n)`; weight majorant `A*d_n^(-p)`, "
        "`p = 2*sigma_lower`, so the product integral has exponent `1+p`.",
        f"- `F(W, rho*, N) = exp(1 + {KAPPA}W/(1-rho*)) * {KAPPA}W*rho*^N/(1-rho*)`.",
        "",
        "## Per-block records",
        "",
        "| block | head weighted sum | deep k=1 tail | W^(>=1) block | W^(0) block | plain weight sup |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for block in box["blocks"]:
        deep = block["deep_tail"]
        deep_text = "n/a" if deep is None else f"`{deep['deep_sum_upper_bound']}`"
        plain = block["plain_weight_sup_upper_bound"]
        lines.append(
            f"| {block['label']} | `{block['head_weighted_sum_upper_bound']}` | {deep_text} | "
            f"`{block['W_ge1_block_upper_bound']}` | `{block['W0_block_upper_bound']}` | "
            f"{'`' + plain + '`' if plain else 'n/a'} |"
        )
    lines.extend(
        [
            "",
            "## Row sums by source disc",
            "",
            "| source disc | W^(>=1) row sum | W^(0) row sum |",
            "|---:|---:|---:|",
        ]
    )
    for source, value in box["W_ge1_row_sums_by_source_disc"].items():
        lines.append(
            f"| {source} | `{value}` | `{box['W0_row_sums_by_source_disc'][source]}` |"
        )
    lines.extend(
        [
            "",
            "## Reproducibility",
            "",
            f"Receipt: [{receipt_path.name}]({receipt_path}).",
            "",
            "```bash",
            f"/Users/za/.venvs/farey-rh/bin/python {code_path} \\",
            f"  --blocks-receipt {receipt['v2_receipt_source']['path']} \\",
            f"  --sweep-source {receipt['blocks_source']['path']} \\",
            f"  --out-dir {receipt_path.parent} --precision-bits {receipt['precision_bits']} "
            f"--M {receipt['M']} --N {receipt['N_evaluation']}",
            "```",
            "",
            f"Wall time: {receipt['runtime_seconds']:.1f} s.",
            "",
        ]
    )
    return "\n".join(lines)


def run(args: argparse.Namespace) -> dict[str, Any]:
    if args.precision_bits != PREC_BITS or args.M != M_DEFAULT:
        raise SystemExit("precision must be 384 bits and M must be 512")
    ctx.prec = args.precision_bits
    start = time.perf_counter()
    blocks_receipt_path = Path(args.blocks_receipt).resolve()
    sweep_source = Path(args.sweep_source).resolve()
    out_dir = Path(args.out_dir).resolve()

    v2 = json.loads(blocks_receipt_path.read_text(encoding="utf-8"))
    if v2.get("schema") != "tb-block-certificates/v2":
        raise ValueError("unexpected TB block-certificate schema")
    if v2.get("q") != Q:
        raise ValueError(f"TB receipt q is not {Q}: {v2.get('q')!r}")
    blocks, blocks_line = load_blocks(sweep_source)
    if len(blocks) != 19 or not v2["blocks_source"]["exact_count_check"]:
        raise ValueError("the certified source must contain exactly 19 blocks")
    if [list(block) for block in blocks] != v2["blocks_source"]["blocks"]:
        raise ValueError("live BLOCKS assignment differs from the TB receipt")

    lam, centers, radii, multipliers, arcs = geometry(v2)
    rho = arb(v2["rho_star_upper_bound"])
    s, s_info = s_box()
    v2_by_block = {tuple(item["block"]): item for item in v2["blocks"]}

    block_records = []
    for block in blocks:
        block_records.append(
            w.certify_block(block, v2_by_block[tuple(block)], centers, radii, lam, arcs, s, s_info)
        )
        print(f"[{len(block_records):2d}/19] {block_records[-1]['label']}", flush=True)

    W_ge1_rows = {
        str(source): w.arb_text(
            w.sum_arb([arb(item["W_ge1_block_upper_bound"]) for item in block_records
                       if item["source_disc"] == source])
        )
        for source in range(1, KAPPA + 1)
    }
    W0_rows = {
        str(source): w.arb_text(
            w.sum_arb([arb(item["W0_block_upper_bound"]) for item in block_records
                       if item["source_disc"] == source])
        )
        for source in range(1, KAPPA + 1)
    }
    W = w.max_arb([arb(value) for value in W_ge1_rows.values()])
    W0 = w.max_arb([arb(value) for value in W0_rows.values()])
    F = f_bound(W, rho, args.N)

    box = {
        "name": PIN_NAME,
        "pin_source_center": {"re": PIN_RE, "im": PIN_IM},
        "N_stable_source_flag": True,
        "s_ball": s_info,
        "blocks": block_records,
        "W_ge1_row_sums_by_source_disc": W_ge1_rows,
        "W0_row_sums_by_source_disc": W0_rows,
        "W_ge1_upper_bound": w.arb_text(W),
        "W0_upper_bound": w.arb_text(W0),
    }
    summary = [
        {
            "box": PIN_NAME,
            "W_ge1_upper_bound": w.arb_text(W),
            "W0_upper_bound": w.arb_text(W0),
            "F_upper_bound": w.arb_text(F),
            "N": args.N,
            "rho_star_used": w.arb_text(rho),
            "contour_lower_bound": "NOT_APPLICABLE_NO_Q7_TC_STAGE",
            "margin_lower_bound": "NOT_APPLICABLE_NO_Q7_TC_STAGE",
            "verdict": "NOT_APPLICABLE_NO_Q7_TC_STAGE",
            "minimal_certifying_N": None,
        }
    ]
    receipt = {
        "schema": "tb-weight-envelope-cert/v2",
        "backend": "python-flint Arb/Acb ball arithmetic",
        "precision_bits": args.precision_bits,
        "M": args.M,
        "q": Q,
        "kappa": KAPPA,
        "N_evaluation": args.N,
        "rho_star": w.arb_text(rho),
        "rho_star_source": (
            "certified q=7 TB block receipt rho_star_upper_bound "
            f"({blocks_receipt_path.name}); NOT a supplied literal"
        ),
        "aggregation": {
            "W_ge1": "max over source-disc row sums; tail = TB head sum of |u_n|*rho_n plus the "
                     "certified deep |u_n|/(R_j*d_n) first-term-plus-integral bound; single = plain |u_n| sup",
            "W0": "max over source-disc row sums; tail = direct Hurwitz-closed Phi_0 sup; single = plain |u_n| sup",
            "W0_enters_F": False,
            "deep_integral_exponent": "1 + 2*sigma_lower",
        },
        "blocks_source": {
            "path": str(sweep_source),
            "sha256": sha256(sweep_source),
            "assignment_line": blocks_line,
            "count": len(blocks),
            "exact_count_check": len(blocks) == 19,
            "blocks": [list(block) for block in blocks],
        },
        "v2_receipt_source": {
            "path": str(blocks_receipt_path),
            "sha256": sha256(blocks_receipt_path),
            "schema": v2["schema"],
            "rho_star_v2": v2["rho_star"],
        },
        "pins_source": {
            "path": "F7_CONSTANTS_MANIFEST.md section 5, pin 1 (mms+, sign=+1)",
            "count": 1,
            "exact_count_check": True,
        },
        "tc_bounds_source": {
            "kind": "NOT_APPLICABLE_NO_Q7_TC_STAGE",
            "note": "q=7 stages 1-2 carry no T-c contour lower bound; none is fabricated.",
        },
        "geometry": {
            "lambda": w.arb_text(lam),
            "centers": [w.arb_text(value) for value in centers],
            "source_radii": [w.arb_text(value) for value in radii],
            "radius_multipliers": [w.arb_text(value) for value in multipliers],
        },
        "boxes": [box],
        "summary": summary,
        "runtime_seconds": time.perf_counter() - start,
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    receipt_path = out_dir / RECEIPT_NAME
    report_path = out_dir / REPORT_NAME
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report_path.write_text(render_report(receipt, Path(__file__).resolve(), receipt_path), encoding="utf-8")
    print(json.dumps({
        "receipt": str(receipt_path),
        "report": str(report_path),
        "W_ge1": w.arb_text(W),
        "W0": w.arb_text(W0),
        "F": w.arb_text(F),
        "runtime_seconds": receipt["runtime_seconds"],
    }, indent=2))
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--blocks-receipt", default=str(BLOCKS_RECEIPT_DEFAULT))
    parser.add_argument("--sweep-source", default=str(SWEEP_DEFAULT))
    parser.add_argument("--out-dir", default=str(DEFAULT_RECEIPT_DIR))
    parser.add_argument("--precision-bits", type=int, default=PREC_BITS)
    parser.add_argument("--M", type=int, default=M_DEFAULT)
    parser.add_argument("--N", type=int, default=N_DEFAULT)
    run(parser.parse_args())


if __name__ == "__main__":
    main()
