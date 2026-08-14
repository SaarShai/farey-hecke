#!/usr/bin/env python3
"""M2 non-factor witnesses at the first three zeta-zero points.

This runner is intentionally an adapter around the read-only certified
builders in ``code/zeta_cert_rosen_q5.py`` and
``code/zeta_cert_rosen_even.py``.  It does not duplicate the transfer
operator.  The q=4 control is evaluated and written before any non-arithmetic
surface is attempted; a failed control exits without running the witnesses.

The source builders use Arb/acb balls for the finite-N determinant.  Their
dimension-tail routine is retained exactly, including its [N-8,N-6,N-4,N-2,N]
det-increment convention and q_cap=0.85.  This file records the finite-N
component radii separately from the dimension-tail radius, and uses the
actual final ``acb.abs_lower()`` result for the nonzero verdict.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from decimal import Decimal
from pathlib import Path

from flint import acb, arb, ctx


HERE = Path(__file__).resolve()
WORKTREE_ROOT = HERE.parents[2]
CODE_ROOT = WORKTREE_ROOT / "code"
PROJECT_ROOT = Path("/Users/za/Documents/farey-hecke")
LANE_DIR = PROJECT_ROOT / "research_notes/rh_goals_2026-08-14/lane_g"
REPORT_PATH = LANE_DIR / "M2_NONFACT_WITNESSES.md"
RECEIPT_PATH = LANE_DIR / "m2_nonfact_receipt.json"

sys.path.insert(0, str(CODE_ROOT))
import zeta_cert_rosen_even as EVEN  # noqa: E402
import zeta_cert_rosen_q5 as Q5  # noqa: E402


PREC_BITS = 400
N = 28
N_HEAD = 4
SIGN = +1
CONTROL_MID_ABS_MAX = 1e-7
GAMMAS = (
    ("zeta_1", "14.134725141734693"),
    ("zeta_2", "21.022039638771554"),
    ("zeta_3", "25.010857580145688"),
)


def _arb_float(value: arb) -> float:
    return float(value)


def _arb_interval(value: arb) -> dict[str, str | float]:
    return {
        "lower": str(value.lower()),
        "upper": str(value.upper()),
        "mid": str(value.mid()),
        "radius": str(value.rad()),
    }


def _source_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _s_point(gamma_text: str) -> tuple[str, str, acb]:
    gamma = Decimal(gamma_text)
    im = gamma / Decimal(2)
    re_text = "0.25"
    im_text = format(im, "f")
    return re_text, im_text, acb(arb(re_text), arb(im_text))


def _finite_and_tail(q: int, s: acb) -> tuple[acb, arb | None, dict, int, str]:
    """Return the finite-N det, dimension tail, and source path label.

    q=5 is hard-coded in the q5 module, so retain the same internal sequence
    used by its ``certified_det`` while keeping the pre-tail determinant for
    the rounding/tail split.  Even q uses its public ``cert_det`` helper.
    """
    if q == 5:
        matrix, kappa = Q5.build_reduced_matrix_ball(
            s, N, SIGN, n_head=N_HEAD)
        finite_det = Q5._det_block(matrix, N, kappa, N)
        tail, info = Q5.dim_tail_from_matrix(matrix, N, kappa)
        path = "zeta_cert_rosen_q5.build_reduced_matrix_ball -> _det_block -> dim_tail_from_matrix"
        return finite_det, tail, info, kappa, path
    finite_det, tail, info, kappa = EVEN.cert_det(
        s, N, SIGN, q, n_head=N_HEAD)
    path = "zeta_cert_rosen_even.cert_det -> build_reduced_matrix_ball/_det_block/dim_tail_from_matrix"
    return finite_det, tail, info, kappa, path


def _tail_inflated(finite_det: acb, tail: arb | None) -> acb:
    if tail is None:
        re = arb(finite_det.real.mid(), arb("inf"))
        im = arb(finite_det.imag.mid(), arb("inf"))
    else:
        re = finite_det.real + arb(0, tail)
        im = finite_det.imag + arb(0, tail)
    return acb(re, im)


def evaluate(q: int, surface: str, zero_label: str, gamma_text: str) -> dict:
    re_text, im_text, s = _s_point(gamma_text)
    started = time.monotonic()
    finite_det, tail, info, kappa, eval_path = _finite_and_tail(q, s)
    final_det = _tail_inflated(finite_det, tail)
    abs_lower = final_det.abs_lower()
    midpoint = complex(
        float(finite_det.real.mid()), float(finite_det.imag.mid()))
    rounding_re = _arb_float(finite_det.real.rad())
    rounding_im = _arb_float(finite_det.imag.rad())
    rounding_max = max(rounding_re, rounding_im)
    lower_positive = bool(abs_lower > 0)
    tail_present = tail is not None
    witness_status = (
        "CERTIFIED-NONZERO"
        if tail_present and lower_positive
        else "NOT-CERTIFIED"
    )
    return {
        "surface": surface,
        "q": q,
        "sector": "mms+",
        "sign": SIGN,
        "zero_label": zero_label,
        "gamma": gamma_text,
        "s": {"re": re_text, "im": im_text},
        "N": N,
        "n_head": N_HEAD,
        "precision_bits": PREC_BITS,
        "kappa": kappa,
        "evaluation_path": eval_path,
        "status": witness_status,
        "witness_label": (
            "certified-modulo-tail-heuristic"
            if tail_present and lower_positive else "not-certified"
        ),
        "certified_modulo": "tail-heuristic" if tail_present else "none",
        "finite_det_ball": str(finite_det),
        "finite_real_ball": _arb_interval(finite_det.real),
        "finite_imag_ball": _arb_interval(finite_det.imag),
        "final_det_ball": str(final_det),
        "final_real_ball": _arb_interval(final_det.real),
        "final_imag_ball": _arb_interval(final_det.imag),
        "finite_det_midpoint": {
            "re": midpoint.real,
            "im": midpoint.imag,
            "abs": abs(midpoint),
        },
        "certified_abs_lower_bound": _arb_float(abs_lower),
        "certified_abs_lower_bound_arb": str(abs_lower),
        "tail_contribution": _arb_float(tail) if tail_present else None,
        "tail_contribution_arb": str(tail) if tail_present else None,
        "rounding_contribution": rounding_max,
        "rounding_contribution_definition": "max(rad(finite Re det), rad(finite Im det))",
        "rounding_real_radius": rounding_re,
        "rounding_imag_radius": rounding_im,
        "dimension_tail_heuristic": True,
        "dimension_tail_certified_by_source": tail_present,
        "dimension_tail_info": info,
        "wall_seconds": time.monotonic() - started,
    }


def _control_record() -> dict:
    record = evaluate(4, "G_4", "zeta_1", GAMMAS[0][1])
    midpoint_abs = record["finite_det_midpoint"]["abs"]
    record["control_consistent_with_zero"] = (
        record["certified_abs_lower_bound"] <= 0.0
        and midpoint_abs <= CONTROL_MID_ABS_MAX
    )
    record["control_mid_abs_threshold"] = CONTROL_MID_ABS_MAX
    record["control_verdict"] = (
        "PASS-CONSISTENT-WITH-ZERO"
        if record["control_consistent_with_zero"]
        else "FAIL"
    )
    return record


def _base_receipt() -> dict:
    return {
        "receipt": "M2_NONFACT_WITNESSES",
        "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "status": "RUNNING",
        "protocol": {
            "N": N,
            "n_head": N_HEAD,
            "sign": SIGN,
            "sector": "mms+",
            "precision_bits": PREC_BITS,
            "zeta_zero_ordinates": [g for _, g in GAMMAS],
            "s_definition": "s_n = 0.25 + i*gamma_n/2",
            "control_first": True,
            "control": "q=4 at s_1 must contain zero and have tiny midpoint",
            "control_mid_abs_threshold": CONTROL_MID_ABS_MAX,
            "dimension_tail_convention": {
                "dims": [20, 22, 24, 26, 28],
                "step": 2,
                "window": 4,
                "q_cap": 0.85,
                "formula": "last_increment * q/(1-q)",
                "inflation": "tail is added to both Re and Im",
            },
            "lower_bound_source": "actual final acb.abs_lower() after tail inflation",
            "rounding_contribution_source": "finite-N determinant component Arb radii before tail inflation",
        },
        "source_files": {
            "q5": str(CODE_ROOT / "zeta_cert_rosen_q5.py"),
            "even": str(CODE_ROOT / "zeta_cert_rosen_even.py"),
            "mayer_reference": str(CODE_ROOT / "zeta_mayer_rosen.py"),
            "tail_review": str(PROJECT_ROOT / "research_notes/rh_goals_2026-08-14/lane_b/ADVERSARIAL_REVIEW_V1.md"),
        },
        "source_sha256": {
            "zeta_cert_rosen_q5.py": _source_hash(CODE_ROOT / "zeta_cert_rosen_q5.py"),
            "zeta_cert_rosen_even.py": _source_hash(CODE_ROOT / "zeta_cert_rosen_even.py"),
            "zeta_mayer_rosen.py": _source_hash(CODE_ROOT / "zeta_mayer_rosen.py"),
        },
        "control": None,
        "witnesses": [],
    }


def _fmt(value: float | None) -> str:
    if value is None:
        return "—"
    return f"{value:.6e}"


def _render_report(receipt: dict) -> str:
    control = receipt.get("control")
    witnesses = receipt.get("witnesses", [])
    status = receipt.get("status", "UNKNOWN")
    lines = [
        "# M2 non-factor nonvanishing witnesses",
        "",
        f"## Verdict: **{status}**",
        "",
        "The lower-bound column is the actual Arb `acb.abs_lower()` value for the final ball, after the source module's dimension-tail radius is added to both coordinates. A row is `CERTIFIED-NONZERO` only when that actual lower bound is strictly positive and the tail evaluation returns a finite radius.",
        "",
        "| Surface | Zero point | Verdict | Certified lower bound on `|det|` | Tail contribution | Rounding contribution |",
        "|---|---:|---|---:|---:|---:|",
    ]
    for row in witnesses:
        witness_label = row.get(
            "witness_label",
            "certified-modulo-tail-heuristic"
            if row["status"] == "CERTIFIED-NONZERO" else "not-certified",
        )
        lines.append(
            f"| {row['surface']} (`q={row['q']}`, {row['sector']}) | {row['zero_label']} (`gamma={row['gamma']}`) | **{row['status']}**<br>`{witness_label}` | {_fmt(row['certified_abs_lower_bound'])} | {_fmt(row['tail_contribution'])} | {_fmt(row['rounding_contribution'])} |"
        )
    if not witnesses:
        lines.append("| — | — | No witness evaluations were run after the failed control | — | — | — |")

    lines.extend([
        "",
        "## Control (executed first)",
        "",
    ])
    if control is None:
        lines.append("Control record missing: **FAIL**.")
    else:
        lines.extend([
            f"- G_4 at `s_1 = {control['s']['re']} + i*{control['s']['im']}`: **{control['control_verdict']}**.",
            f"- Finite-N midpoint: `{control['finite_det_midpoint']}`; midpoint `|det|` = `{control['finite_det_midpoint']['abs']:.6e}`.",
            f"- Final Arb ball: `{control['final_det_ball']}`.",
            f"- Actual final `acb.abs_lower()`: `{control['certified_abs_lower_bound_arb']}`.",
            f"- Tail contribution: `{_fmt(control['tail_contribution'])}`; rounding contribution: `{_fmt(control['rounding_contribution'])}`.",
        ])
    if control is not None and not control["control_consistent_with_zero"]:
        lines.append("- The control failed, so the required stop rule was applied and no main witnesses were evaluated.")

    lines.extend([
        "",
        "## Ball and tail accounting",
        "",
        f"All evaluations used `precision_bits={PREC_BITS}`, `N={N}`, `n_head={N_HEAD}`, and `sign=+1` (`mms+`). The standard source tail check used dimensions `[20, 22, 24, 26, 28]`, `step=2`, `window=4`, and `q_cap=0.85`; it extrapolates the last determinant increment as `last_increment*q/(1-q)` and adds that radius to both the real and imaginary components. The reported rounding contribution is `{receipt['protocol']['rounding_contribution_source']}`.",
        "",
        "The q=5 rows use `zeta_cert_rosen_q5.py`'s certified builder and its q=5 odd-q block formula with `sign=+1`; the q=8 and q=10 rows use `zeta_cert_rosen_even.py`'s even-q `cert_det` path. The q=8 source explicitly says that the general even-q builder is anchor-validated only at q=8; q=10 is therefore a mechanical general-q evaluation and is disclosed as not independently anchor-validated by that module.",
        "",
        "## Required honesty statements",
        "",
        "(a) the dimension-tail component of the ball radius is heuristic (see lane_b/ADVERSARIAL_REVIEW_V1.md section 4.3) — label every witness \"certified-modulo-tail-heuristic\" and report the tail contribution separately from the rounding contribution;",
        "",
        "Every row with a positive lower bound is therefore labeled **certified-modulo-tail-heuristic** in the receipt/report sense: the Arb finite-N and rounding enclosure is computed by ball arithmetic, while the dimension-tail extrapolation is the existing heuristic convention.",
        "",
        "(b) if det = zeta(2s)*h with h analytic in a neighborhood, then det(s_n)=0; certified det(s_n)!=0 refutes this for the tested points;",
        "",
        "This is pointwise only: three tested points do not establish a global no-factor theorem, and the determinant here is the tested transfer-operator determinant under the stated sector/convention.",
        "",
        "## Raw Arb evidence",
        "",
        "The following strings are the source/runtime ball outputs retained in the machine-readable receipt; the lower-bound verdict was checked from the actual final `acb.abs_lower()` call, not from midpoint magnitude.",
        "",
        "| Surface / point | Finite-N `acb` ball | Tail | Final `acb` ball | Actual `abs_lower()` |",
        "|---|---|---:|---|---:|",
    ])
    if control is not None:
        lines.append(
            f"| CONTROL G_4 / {control['zero_label']} | `{control['finite_det_ball']}` | `{_fmt(control['tail_contribution'])}` | `{control['final_det_ball']}` | `{control['certified_abs_lower_bound_arb']}` |"
        )
    for row in witnesses:
        lines.append(
            f"| {row['surface']} / {row['zero_label']} | `{row['finite_det_ball']}` | `{_fmt(row['tail_contribution'])}` | `{row['final_det_ball']}` | `{row['certified_abs_lower_bound_arb']}` |"
        )
    lines.extend([
        "",
        "## Scope",
        "",
        "Only the requested control and point evaluations were run. Existing source files and lane_b files were read-only references; this runner writes only the report and receipt named by the task.",
        "",
    ])
    return "\n".join(lines)


def _write_outputs(receipt: dict) -> None:
    LANE_DIR.mkdir(parents=True, exist_ok=True)
    receipt_text = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    report_text = _render_report(receipt)
    receipt_tmp = RECEIPT_PATH.with_name(RECEIPT_PATH.name + ".tmp")
    report_tmp = REPORT_PATH.with_name(REPORT_PATH.name + ".tmp")
    receipt_tmp.write_text(receipt_text)
    report_tmp.write_text(report_text)
    os.replace(receipt_tmp, RECEIPT_PATH)
    os.replace(report_tmp, REPORT_PATH)


def main() -> int:
    ctx.prec = PREC_BITS
    receipt = _base_receipt()

    print("[control] q=4 at zeta zero 1", flush=True)
    control = _control_record()
    receipt["control"] = control
    control_pass = bool(control["control_consistent_with_zero"])
    receipt["status"] = "CONTROL_PASS_CONTINUING" if control_pass else "CONTROL_FAILED_STOPPED"
    _write_outputs(receipt)
    print(
        f"[control] {control['control_verdict']} midpoint_abs="
        f"{control['finite_det_midpoint']['abs']:.6e} "
        f"abs_lower={control['certified_abs_lower_bound_arb']}",
        flush=True,
    )
    if not control_pass:
        return 2

    specs = (
        (5, "G_5", "q5 certified builder"),
        (8, "G_8", "even-q certified builder"),
        (10, "G_10", "even-q certified builder"),
    )
    for q, surface, _description in specs:
        for zero_label, gamma_text in GAMMAS:
            print(f"[{surface}/{zero_label}] evaluating N={N}", flush=True)
            row = evaluate(q, surface, zero_label, gamma_text)
            receipt["witnesses"].append(row)
            receipt["status"] = "RUNNING"
            _write_outputs(receipt)
            print(
                f"[{surface}/{zero_label}] {row['status']} "
                f"lower={row['certified_abs_lower_bound_arb']} "
                f"tail={_fmt(row['tail_contribution'])} "
                f"rounding={_fmt(row['rounding_contribution'])}",
                flush=True,
            )

    all_certified = all(
        row["status"] == "CERTIFIED-NONZERO"
        for row in receipt["witnesses"]
    )
    receipt["status"] = (
        "PASS_ALL_WITNESSES"
        if all_certified
        else "COMPLETED_WITH_UNCERTIFIED_ROWS"
    )
    _write_outputs(receipt)
    return 0 if all_certified else 1


if __name__ == "__main__":
    raise SystemExit(main())
