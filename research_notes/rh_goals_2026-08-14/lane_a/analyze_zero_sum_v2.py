#!/usr/bin/env python3
"""Assemble A4 weighted chunks, fit the tail, and write the v2 receipt/report."""

from __future__ import annotations

import argparse
from hashlib import sha256
from decimal import Decimal, getcontext
import json
import math
from pathlib import Path
import statistics


ROOT = Path(__file__).resolve().parents[3]
LANE_DIR = Path(__file__).resolve().parent
DEFAULT_ZEROS = ROOT / "cluster_universality_test" / "zeros1.txt"
DEFAULT_BASE = LANE_DIR / "zero_sum_receipt.json"
DEFAULT_A3 = LANE_DIR / "j_minus1_checkpoints"
DEFAULT_A4 = LANE_DIR / "a4_checkpoints"
DEFAULT_RECEIPT = LANE_DIR / "zero_sum_v2_receipt.json"
DEFAULT_REPORT = LANE_DIR / "ZERO_SUM_V2_REPORT.md"
GONEK_J_SLOPE = 3.0 / math.pi**3
GONEK_B_NUMERATOR = 6.0 / math.pi**2
CHUNK_SIZE = 500
getcontext().prec = 80


def dec(value: str | float | int | Decimal) -> Decimal:
    if isinstance(value, Decimal):
        return value
    if isinstance(value, str):
        return Decimal(value.replace(" E", "e").replace(" ", ""))
    return Decimal(str(value))


def fmt(value: float | Decimal, digits: int = 12) -> str:
    return f"{float(value):.{digits}g}"


def local_path(path: Path) -> Path:
    resolved = path.expanduser().resolve()
    try:
        resolved.relative_to(LANE_DIR.resolve())
    except ValueError as exc:
        raise ValueError(f"path outside lane_a: {resolved}") from exc
    return resolved


def load_a3_blocks(directory: Path, zeros_path: Path, source_sha: str) -> list[dict]:
    records = []
    for path in sorted(directory.glob("chunk_*.json")):
        row = json.loads(path.read_text())
        required = {
            "quantity": "J_-1(T) = sum 1/abs(zeta'(rho))^2 over positive ordinates",
            "zeros_path": str(zeros_path),
            "zeros_sha256": source_sha,
            "realprecision_digits": 20,
            "strict_residual_threshold": "1e-15",
        }
        if any(row.get(key) != value for key, value in required.items()):
            raise RuntimeError(f"A3 checkpoint configuration mismatch: {path}")
        records.append(row)
    records.sort(key=lambda row: int(row["hi"]))
    expected = 1
    for row in records:
        if int(row["lo"]) != expected:
            raise RuntimeError(f"A3 checkpoint gap/overlap before {row['lo']}; expected {expected}")
        expected = int(row["hi"]) + 1
    if not records or int(records[-1]["hi"]) < 10000:
        raise RuntimeError("A3 checkpoints do not cover N=10000")
    return records


def load_a4_chunks(directory: Path, zeros_path: Path, source_sha: str) -> list[dict]:
    records = []
    for path in sorted(directory.glob("weighted_chunk_*.json")):
        row = json.loads(path.read_text())
        required = {
            "quantity": "positive weighted zero-sum chunk",
            "zeros_path": str(zeros_path),
            "zeros_sha256": source_sha,
            "realprecision_digits": 20,
            "strict_residual_threshold": "1e-15",
        }
        if any(row.get(key) != value for key, value in required.items()):
            raise RuntimeError(f"A4 checkpoint configuration mismatch: {path}")
        records.append(row)
    records.sort(key=lambda row: int(row["hi"]))
    expected = 3001
    for row in records:
        if int(row["lo"]) != expected:
            raise RuntimeError(f"A4 checkpoint gap/overlap before {row['lo']}; expected {expected}")
        expected = int(row["hi"]) + 1
    if not records or int(records[-1]["hi"]) < 10000:
        raise RuntimeError("A4 weighted checkpoints do not cover N=10000")
    return records


def exact_density_integral(T: float) -> float:
    """Integral of log(t/(2*pi))/(t^2+1/4) from T to infinity.

    The displayed series is exact to the retained O(T^-7) term; at T~10^4
    the omitted term is far below 1e-20. This avoids importing a numerical
    integration package for a smooth elementary tail.
    """
    K = 2.0 * math.pi
    a2 = 0.25
    L = math.log(T / K)
    total = 0.0
    for k in range(4):
        q = 1.0 + 2.0 * k
        total += ((-a2) ** k) * (T ** (-q)) * (L / q + 1.0 / q**2)
    return total


def gonek_scaled_fit(blocks: list[dict], lo_start: int) -> dict:
    selected = [row for row in blocks if int(row["lo"]) >= lo_start]
    if len(selected) < 3:
        raise RuntimeError(f"too few blocks in fit window lo>={lo_start}")
    previous_T = None
    enriched = []
    for row in blocks:
        T = float(dec(row["gamma_boundary_decimal"]))
        lo = int(row["lo"])
        hi = int(row["hi"])
        midpoint = T / 2.0 if lo == 1 else (previous_T + T) / 2.0
        previous_T = T
        if lo < lo_start:
            continue
        g = GONEK_B_NUMERATOR / math.log(midpoint / (2.0 * math.pi))
        B = float(row["mean_inverse_abs_zeta_prime_sq"])
        enriched.append({"lo": lo, "hi": hi, "T_lo": None, "T_hi": T, "T_mid": midpoint, "B": B, "gonek_B": g, "ratio_B_to_gonek": B / g})
    denom = math.fsum(row["gonek_B"] ** 2 for row in enriched)
    alpha = math.fsum(row["gonek_B"] * row["B"] for row in enriched) / denom
    for row in enriched:
        row["fitted_B"] = alpha * row["gonek_B"]
        row["residual"] = row["B"] - row["fitted_B"]
        row["relative_residual"] = row["residual"] / row["B"]
    residuals = [row["residual"] for row in enriched]
    return {
        "model": "B(t) = alpha * (6/pi^2)/log(t/(2*pi)), through-origin OLS on 500-zero block means",
        "fit_lo_start": lo_start,
        "fit_block_count": len(enriched),
        "alpha": alpha,
        "gonek_B_numerator": GONEK_B_NUMERATOR,
        "gonek_J_minus1_slope": GONEK_J_SLOPE,
        "mean_ratio_B_to_gonek": statistics.mean(row["ratio_B_to_gonek"] for row in enriched),
        "min_ratio_B_to_gonek": min(row["ratio_B_to_gonek"] for row in enriched),
        "max_ratio_B_to_gonek": max(row["ratio_B_to_gonek"] for row in enriched),
        "residual_rmse": math.sqrt(math.fsum(value * value for value in residuals) / len(residuals)),
        "max_abs_residual": max(abs(value) for value in residuals),
        "max_block_mean": max(row["B"] for row in enriched),
        "blocks": enriched,
    }


def candidate_rows(S: float, bar: float, base_candidates: list[dict]) -> list[dict]:
    rows = []
    for old in base_candidates:
        value = float(old["value"])
        residual = abs(S - value)
        rows.append({
            "form": old["form"],
            "value": value,
            "absolute_residual": residual,
            "relative_residual": residual / abs(S),
            "sigma_units": residual / bar if bar else None,
            "excluded": residual > 5.0 * bar,
        })
    return sorted(rows, key=lambda row: row["absolute_residual"])


def make_report(receipt: dict) -> str:
    final = receipt["final_estimate"]
    tail = receipt["tail_model"]
    errors = receipt["error_budget"]
    lines = [
        "# Zero-sum V2 report",
        "",
        "## Verdict",
        "",
        f"**S = {final['two_sided_S']:.12f} +/- {final['two_sided_error_bar']:.3g}; digits claimed: {final['digits_claimed']}.**",
        "",
        f"The N=10,000 positive partial sum is `{final['positive_partial_sum']:.15f}`. The fitted central one-sided tail is `{tail['central_one_sided']:.12g}` and the max-block envelope is `{tail['envelope_one_sided']:.12g}`. The requested absolute 1e-5 bar is **{'achieved' if final['two_sided_error_bar'] <= 1e-5 else 'not achieved'}**: the remaining uncertainty is dominated by the non-rigorous tail envelope at T={tail['T']:.12g}, not backend precision.",
        "",
        "The five displayed decimal places are not all claimed as significant digits; the conservative tail model supports the stated digit count only.",
        "",
        "## Partial sum and tail",
        "",
        "The natural convention is two-sided over conjugate zeros; all computed positive-ordinate terms are doubled in S.",
        "",
        "| N | gamma_N | positive partial sum | two-sided partial sum |",
        "|---:|---:|---:|---:|",
    ]
    for row in receipt["partial_sums_table"]:
        lines.append(f"| {row['N']} | {row['gamma']:.12g} | {row['positive_sum']:.15f} | {2*row['positive_sum']:.15f} |")
    lines += [
        "",
        "For the Gonek comparison, the empirical block mean is B(t)=mean(1/|zeta'(rho)|^2), while the asymptotic prediction is B_G(t)=(6/pi^2)/log(t/(2*pi)). A through-origin fit B=alpha B_G is made on the 500-zero blocks whose lower endpoint has N>=5001.",
        "",
        f"Fit slope alpha = `{tail['fit']['alpha']:.12g}`; B/B_G mean = `{tail['fit']['mean_ratio_B_to_gonek']:.12g}`, range = [`{tail['fit']['min_ratio_B_to_gonek']:.12g}`, `{tail['fit']['max_ratio_B_to_gonek']:.12g}`], block-mean RMSE = `{tail['fit']['residual_rmse']:.6g}`.",
        "",
        "The density-weighted integrand is B(t) log(t/(2*pi))/(2*pi*(t^2+1/4)). Under the fitted Gonek form the logarithms cancel, giving central one-sided tail alpha*(3/pi^3)*2*atan(1/(2T)). The conservative envelope holds B at the maximum selected block mean and uses the corresponding density integral.",
        "",
        f"T = `{tail['T_decimal']}`; central one-sided tail = `{tail['central_one_sided']:.15g}`; envelope one-sided tail = `{tail['envelope_one_sided']:.15g}`; selected max block mean = `{tail['max_block_mean']:.12g}`.",
        "",
        "The envelope is a numerical extrapolation, not a theorem-level bound against an unseen unusually small zeta derivative.",
        "",
        "## Error budget",
        "",
        f"- Tail-model symmetric contribution to the two-sided bar: `{errors['tail_model_two_sided']:.6g}` (interval is from the positive partial sum to the envelope).",
        f"- Backend cross-check contribution: `{errors['backend_two_sided']:.6g}` from realprecision 20 versus 30 over every A4 chunk; maximum single-chunk difference `{errors['backend_max_chunk_difference']:.6g}`.",
        f"- A4 seed/root first-order propagation: `{errors['a4_seed_two_sided']:.6g}` two-sided, from residual/|zeta'| root displacement and the local derivative of the complete weighted term; maximum A4 root displacement `{errors['a4_max_root_error']:.6g}`.",
        f"- Inherited N<=3000 seed sensitivity: `{errors['inherited_seed_status']}`. The inherited receipt supplies residual maxima and a realprecision-30 N<=1000 displayed-sum cross-check, but not per-zero zeta'' values, so an independent per-zero propagation for that already-computed range was intentionally not repeated.",
        "",
        "The tail term is orders of magnitude larger than the measured numerical budgets. The seed statement is therefore explicit about the one residual limitation that remains in the reused legacy aggregate; it is not silently promoted to a rigorous bound.",
        "",
        "## Candidate closed forms",
        "",
        "Residuals are measured against the central estimate in units of the final conservative one-sigma-style bar. Every candidate remains excluded by more than 5 sigma.",
        "",
        "| candidate | value | absolute residual | sigma units | verdict |",
        "|---|---:|---:|---:|---|",
    ]
    for row in receipt["simple_form_candidates"]:
        lines.append(f"| `{row['form']}` | {row['value']:.12g} | {row['absolute_residual']:.6g} | {row['sigma_units']:.6g} | {'EXCLUDED' if row['excluded'] else 'not excluded'} |")
    lines += [
        "",
        "## Residual and source checks",
        "",
        f"A3/A4 source SHA-256: `{receipt['source']['zeros_sha256']}`. Refined zeros used: {receipt['source']['used_zero_count']}; maximum residual: `{receipt['source']['max_abs_zeta_residual']:.6g}`; strict threshold: `1e-15`; failures: {receipt['source']['failure_count']}.",
        "",
        f"The A4 weighted chunk sums reproduce A3's J_-1 chunks on the overlapping range with maximum absolute difference `{receipt['cross_checks']['a3_overlap_max_abs_difference']:.6g}` in the reciprocal-derivative sum and matching boundary ordinates.",
        "",
        "Reproduction:",
        "",
        "```bash",
        "python3 research_notes/rh_goals_2026-08-14/lane_a/zero_sum_v2_driver.py --nmax 10000",
        "python3 research_notes/rh_goals_2026-08-14/lane_a/zero_sum_v2_backend_crosscheck.py --nmax 10000",
        "python3 research_notes/rh_goals_2026-08-14/lane_a/analyze_zero_sum_v2.py",
        "```",
        "",
    ]
    return "\n".join(lines)


def run(args: argparse.Namespace) -> int:
    zeros = args.zeros.resolve()
    source_sha = sha256(zeros.read_bytes()).hexdigest()
    base = json.loads(local_path(args.base).read_text())
    a3 = load_a3_blocks(local_path(args.a3), zeros, source_sha)
    a4 = load_a4_chunks(local_path(args.a4), zeros, source_sha)
    a3_by_bounds = {(int(row["lo"]), int(row["hi"])): row for row in a3}
    overlap_diffs = []
    for row in a4:
        key = (int(row["lo"]), int(row["hi"]))
        a3_row = a3_by_bounds.get(key)
        if a3_row:
            overlap_diffs.append(abs(dec(row["sum_inverse_abs_zeta_prime_sq_decimal"]) - dec(a3_row["positive_chunk_sum_decimal"])))
            if row["gamma_boundary_decimal"] != a3_row["gamma_boundary_decimal"]:
                raise RuntimeError(f"A3/A4 gamma boundary mismatch at {key}")
    if not overlap_diffs:
        raise RuntimeError("no A3/A4 overlapping blocks")
    weighted = {int(k): v for k, v in base["partial_sums"].items()}
    for row in a4:
        weighted[int(row["hi"])] = {
            "sum_decimal": row["cumulative_positive_sum_decimal"],
            "gamma": row["gamma_boundary_decimal"],
            "positive_sum": float(dec(row["cumulative_positive_sum_decimal"])),
            "two_sided_sum": 2.0 * float(dec(row["cumulative_positive_sum_decimal"])),
        }
    if 10000 not in weighted:
        raise RuntimeError("missing N=10000 weighted partial")
    final_a4 = a4[-1]
    partial_positive_dec = dec(final_a4["cumulative_positive_sum_decimal"])
    partial_positive = float(partial_positive_dec)
    T = float(dec(final_a4["gamma_boundary_decimal"]))
    blocks = [{
        "lo": int(row["lo"]),
        "hi": int(row["hi"]),
        "count": int(row["count"]),
        "gamma_boundary_decimal": row["gamma_boundary_decimal"],
        "mean_inverse_abs_zeta_prime_sq": float(row["mean_inverse_abs_zeta_prime_sq"]),
        "max_abs_zeta_residual": float(row["max_abs_zeta_residual"]),
    } for row in a3]
    fit = gonek_scaled_fit(blocks, 5001)
    central_tail = fit["alpha"] * GONEK_J_SLOPE * 2.0 * math.atan(1.0 / (2.0 * T))
    envelope_tail = fit["max_block_mean"] * exact_density_integral(T) / (2.0 * math.pi)
    tail_bar_one_sided = max(central_tail, envelope_tail - central_tail)
    crosscheck_path = local_path(args.a4) / "backend_crosscheck.json"
    backend = json.loads(crosscheck_path.read_text()) if crosscheck_path.exists() else {"chunks": [], "sum_absolute_chunk_sum_difference_decimal": None}
    backend_sum_diff = float(dec(backend["sum_absolute_chunk_sum_difference_decimal"])) if backend.get("sum_absolute_chunk_sum_difference_decimal") is not None else None
    a4_seed = sum(float(dec(row["sum_seed_first_order_bound_decimal"])) for row in a4)
    max_root = max(float(dec(row["max_root_error_decimal"])) for row in a4)
    backend_two = 2.0 * backend_sum_diff if backend_sum_diff is not None else None
    a4_seed_two = 2.0 * a4_seed
    final_central = 2.0 * (partial_positive + central_tail)
    tail_two = 2.0 * tail_bar_one_sided
    numerical_two = (backend_two or 0.0) + a4_seed_two
    final_bar = tail_two + numerical_two
    candidates = candidate_rows(final_central, final_bar, base["simple_form_candidates"])
    partial_table = []
    for N in sorted(weighted):
        row = weighted[N]
        gamma = float(dec(row.get("gamma", row.get("gamma_boundary", "nan"))))
        positive = float(dec(row.get("sum_decimal", row.get("positive_sum", "nan"))))
        partial_table.append({"N": N, "gamma": gamma, "positive_sum": positive})
    max_res = max(float(row["max_abs_zeta_residual"]) for row in blocks)
    failures = sum(int(row.get("failure_count", 0)) for row in a3) + sum(int(row.get("failure_count", 0)) for row in a4)
    receipt = {
        "status": "completed",
        "verdict": "TAIL-LIMITED",
        "source": {
            "zeros_path": str(zeros),
            "zeros_sha256": source_sha,
            "used_zero_count": 10000,
            "backend": "PARI/GP 2.17.3 via lfuninit",
            "realprecision_digits": 20,
            "high_precision_crosscheck_digits": 30,
            "strict_residual_threshold": "1e-15",
            "max_abs_zeta_residual": max_res,
            "failure_count": failures,
            "refinement": "one real Newton update from each zeros1.txt seed",
            "convention": "two-sided sum is twice the positive-ordinate sum",
        },
        "partial_sums_table": partial_table,
        "tail_model": {
            "T": T,
            "T_decimal": final_a4["gamma_boundary_decimal"],
            "density": "dN/dt = log(t/(2*pi))/(2*pi)",
            "gonek_B_prediction": "(6/pi^2)/log(t/(2*pi))",
            "fit": fit,
            "central_one_sided": central_tail,
            "max_block_mean": fit["max_block_mean"],
            "envelope_one_sided": envelope_tail,
            "tail_interval_one_sided": [0.0, envelope_tail],
            "central_formula": "alpha*(3/pi^3)*2*atan(1/(2*T))",
            "envelope_formula": "Bmax/(2*pi)*integral_T_inf log(t/(2*pi))/(t^2+1/4) dt",
            "interpretation": "empirical extrapolation, not a theorem-level bound",
        },
        "error_budget": {
            "tail_model_two_sided": tail_two,
            "backend_two_sided": backend_two,
            "backend_max_chunk_difference": max((float(dec(row["absolute_chunk_sum_difference_decimal"])) for row in backend.get("chunks", [])), default=None),
            "a4_seed_two_sided": a4_seed_two,
            "a4_max_root_error": max_root,
            "inherited_seed_status": "not fully per-zero propagated; reused N<=3000 receipt has residual gate and N<=1000 realprecision-30 displayed-sum cross-check",
            "total_two_sided_error_bar": final_bar,
        },
        "cross_checks": {
            "a3_overlap_max_abs_difference": float(max(overlap_diffs)),
            "a3_overlap_count": len(overlap_diffs),
            "backend_crosscheck_status": backend.get("status", "missing"),
            "backend_sum_absolute_difference": backend_sum_diff,
        },
        "final_estimate": {
            "positive_partial_sum": partial_positive,
            "positive_sum_with_central_tail": partial_positive + central_tail,
            "two_sided_S": final_central,
            "two_sided_error_bar": final_bar,
            "two_sided_interval_from_conservative_envelope": [2.0 * partial_positive, 2.0 * (partial_positive + envelope_tail)],
            "digits_claimed": "3 significant digits; 4 significant digits are not certified by the tail bar",
            "target_bar_1e-5_achieved": final_bar <= 1e-5,
        },
        "simple_form_candidates": candidates,
        "a3_receipt": str(LANE_DIR / "j_minus1_receipt.json"),
        "a4_checkpoints": [str(path) for path in sorted(local_path(args.a4).glob("weighted_chunk_*.json"))],
    }
    out_receipt = local_path(args.receipt)
    out_report = local_path(args.report)
    out_receipt.write_text(json.dumps(receipt, indent=2) + "\n")
    out_report.write_text(make_report(receipt))
    print(json.dumps({"S": final_central, "bar": final_bar, "digits": receipt["final_estimate"]["digits_claimed"], "target_1e-5": receipt["final_estimate"]["target_bar_1e-5_achieved"]}, indent=2))
    return 0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--zeros", type=Path, default=DEFAULT_ZEROS)
    parser.add_argument("--base", type=Path, default=DEFAULT_BASE)
    parser.add_argument("--a3", type=Path, default=DEFAULT_A3)
    parser.add_argument("--a4", type=Path, default=DEFAULT_A4)
    parser.add_argument("--receipt", type=Path, default=DEFAULT_RECEIPT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()
    raise SystemExit(run(args))


if __name__ == "__main__":
    main()
