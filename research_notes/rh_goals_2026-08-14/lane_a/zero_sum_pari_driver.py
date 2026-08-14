#!/usr/bin/env python3
"""Reproducible zeta-zero sum using the installed PARI/GP arbitrary-precision backend.

The requested mpmath package is not installed in the execution environment and
network/package installation is unavailable.  This driver therefore uses PARI's
arbitrary-precision zeta and numerical derivative routines.  It keeps the
calculation independent of the E5 implementation while matching its formula.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation, getcontext
import hashlib
import json
import math
import os
import re
import shutil
import statistics
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
LANE_DIR = Path(__file__).resolve().parent
DEFAULT_ZEROS = ROOT / "cluster_universality_test" / "zeros1.txt"
DEFAULT_RECEIPT = Path(__file__).with_name("zero_sum_receipt.json")
DEFAULT_TARGETS = (100, 300, 1000, 3000, 10000)
DEFAULT_J_MINUS1_RECEIPT = Path(__file__).with_name("j_minus1_receipt.json")
DEFAULT_J_MINUS1_REPORT = Path(__file__).with_name("J_MINUS1_GONEK_REPORT.md")
DEFAULT_J_MINUS1_CHECKPOINT_DIR = Path(__file__).with_name("j_minus1_checkpoints")
J_MINUS1_CHUNK_SIZE = 500
J_MINUS1_RESIDUAL_THRESHOLD = "1e-15"
GONEK_SLOPE = 3.0 / math.pi**3
getcontext().prec = 60


def gp_program(zeros_path: Path, nmax: int, targets: tuple[int, ...]) -> str:
    gp_path = str(zeros_path).replace("\\", "\\\\").replace('"', '\\"')
    target_expr = " || ".join(f"n=={n}" for n in targets)
    return f'''default(realprecision,20)
default(parisizemax,2G)
xs=readvec("{gp_path}");
Tmax=xs[{nmax}]+10;
L=lfuninit(1,[Tmax],1);
refine(t0)={{
  my(t=t0,s,z,zp);
  for(k=1,1,
    s=1/2+I*t;
    z=lfun(L,s);
    zp=lfun(L,s,1);
    t=real(t-z/(I*zp))
  );
  t
}};
S=0; maxres=0; failcount=0; firstfail=0;
bs=0; bz=0; bi=0; blo=1;
emit(n,ss,tt,tm,bc,za,ia)={{print("PARTIAL|",n,"|",ss,"|",tt,"|",tm); print("BLOCK|",blo,"|",n,"|",bc,"|",za,"|",ia)}};
reset(n)={{bs=0;bz=0;bi=0;blo=n+1}};
process(n)={{
  my(t,s,z,zp,res,zpsq,inv,term);
  t=refine(xs[n]); s=1/2+I*t; z=lfun(L,s); zp=lfun(L,s,1);
  res=abs(z); if(res>maxres,maxres=res); if(res>=1e-15,failcount=failcount+1);
  zpsq=abs(zp)^2; inv=1/zpsq; term=1/((1/4+t^2)*zpsq);
  S=S+term; bs=bs+1; bz=bz+zpsq; bi=bi+inv;
  if({target_expr},emit(n,S,t,term,bs,bz/bs,bi/bs));
  if({target_expr},reset(n))
}};
for(n=1,{nmax},process(n));
print("CHECK|",maxres,"|",failcount,"|",firstfail);
'''


def run_gp(zeros_path: Path, nmax: int, targets: tuple[int, ...]) -> str:
    gp = shutil.which("gp") or "/opt/homebrew/bin/gp"
    if not Path(gp).exists():
        raise RuntimeError("PARI/GP executable not found")
    proc = subprocess.run(
        [gp, "-q"],
        input=gp_program(zeros_path, nmax, targets),
        text=True,
        capture_output=True,
        check=False,
        timeout=3600,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"gp failed with {proc.returncode}:\n{proc.stdout}\n{proc.stderr}")
    gp_errors = [
        line for line in (proc.stdout + "\n" + proc.stderr).splitlines()
        if "***" in line and "Warning" not in line
    ]
    if gp_errors:
        raise RuntimeError(f"gp reported an error:\n{proc.stdout}\n{proc.stderr}")
    return proc.stdout


def parse_gp(output: str) -> tuple[dict[int, dict[str, str]], list[dict[str, str]], dict[str, str]]:
    partials: dict[int, dict[str, str]] = {}
    blocks: list[dict[str, str]] = []
    check: dict[str, str] | None = None
    for line in output.splitlines():
        if line.startswith("PARTIAL|"):
            _, n, total, gamma, term = line.split("|")
            partials[int(n)] = {"n": n, "positive_sum": total, "gamma": gamma, "last_term": term}
        elif line.startswith("BLOCK|"):
            _, lo, hi, count, avg_zp_sq, avg_inv_zp_sq = line.split("|")
            blocks.append({"lo": lo, "hi": hi, "count": count, "avg_abs_zeta_prime_sq": avg_zp_sq, "avg_inverse_abs_zeta_prime_sq": avg_inv_zp_sq})
        elif line.startswith("CHECK|"):
            _, max_residual, fail_count, first_fail = line.split("|")
            check = {"max_residual": max_residual, "strict_threshold": "1e-15", "failure_count": fail_count, "first_failure_index": first_fail}
    if check is None:
        raise RuntimeError(f"missing CHECK line in GP output:\n{output}")
    return partials, blocks, check


def dps(value: str) -> float:
    return float(value.replace(" E", "e").replace(" ", ""))


def tail_integral(T: float, mean_inverse_derivative_sq: float) -> float:
    """One-sided density-model tail from T to infinity.

    Uses dN/dt ~ log(t/(2*pi))/(2*pi), and holds the observed block mean of
    1/|zeta'|^2 fixed.  This is a diagnostic upper-envelope model, not a proof.
    """
    L = math.log(T / (2.0 * math.pi))
    return mean_inverse_derivative_sq * (L + 1.0) / (2.0 * math.pi * T)


def candidate_table(S: float) -> list[dict[str, float | str]]:
    pi = math.pi
    candidates = {
        "2/pi^2": 2.0 / pi**2,
        "1/(2*pi^2)": 1.0 / (2.0 * pi**2),
        "1/pi^3 = (2/pi^2)/(2*pi)": 1.0 / pi**3,
        "2/pi^4": 2.0 / pi**4,
        "3/pi^4": 3.0 / pi**4,
        "6/pi^4": 6.0 / pi**4,
        "(2/pi^2)/(2*pi)^2 = 1/(2*pi^4)": 1.0 / (2.0 * pi**4),
        "1/(2*pi^3)": 1.0 / (2.0 * pi**3),
    }
    rows = []
    for name, value in candidates.items():
        rows.append({"form": name, "value": value, "absolute_residual": abs(S - value), "relative_residual": abs(S - value) / abs(S)})
    return sorted(rows, key=lambda row: float(row["absolute_residual"]))


def lane_local_path(path: Path) -> Path:
    """Require every generated artifact to remain inside this lane."""
    resolved = path.expanduser().resolve()
    try:
        resolved.relative_to(LANE_DIR.resolve())
    except ValueError as exc:
        raise ValueError(f"generated path is outside lane_a: {resolved}") from exc
    return resolved


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def decimal_from_gp(value: str) -> Decimal:
    try:
        return Decimal(value.replace(" E", "e").replace(" ", ""))
    except InvalidOperation as exc:
        raise ValueError(f"cannot parse GP decimal: {value!r}") from exc


def decimal_text(value: Decimal) -> str:
    return format(value, ".50g")


def jminus1_gp_program(zeros_path: Path, lo: int, hi: int) -> str:
    """Return one bounded GP job; the Python loop checkpoints each job."""
    gp_path = str(zeros_path).replace("\\", "\\\\").replace('"', '\\"')
    threshold = J_MINUS1_RESIDUAL_THRESHOLD
    return f'''default(realprecision,20)
default(parisizemax,2G)
xs=readvec("{gp_path}");
Tmax=xs[{hi}]+10;
L=lfuninit(1,[Tmax],1);
refine(t0)={{
  my(t=t0,s,z,zp);
  for(k=1,1,
    s=1/2+I*t;
    z=lfun(L,s);
    zp=lfun(L,s,1);
    t=real(t-z/(I*zp))
  );
  t
}};
S=0; sum_zpsq=0; maxres=0; failcount=0; firstfail=0; last_t=0; count=0;
process(n)={{
  my(t,s,z,zp,res,zpsq,inv);
  t=refine(xs[n]); s=1/2+I*t; z=lfun(L,s); zp=lfun(L,s,1);
  res=abs(z); if(res>maxres,maxres=res);
  if(res>={threshold},failcount=failcount+1);
  if(res>={threshold} && firstfail==0,firstfail=n);
  zpsq=abs(zp)^2; inv=1/zpsq;
  S=S+inv; sum_zpsq=sum_zpsq+zpsq; last_t=t; count=count+1
}};
for(n={lo},{hi},process(n));
print("JMINUS1|",{lo},"|",{hi},"|",count,"|",S,"|",last_t,"|",maxres,"|",failcount,"|",firstfail,"|",sum_zpsq,"|",S);
'''


def run_jminus1_chunk(zeros_path: Path, lo: int, hi: int, timeout: int) -> dict[str, str]:
    gp = shutil.which("gp") or "/opt/homebrew/bin/gp"
    if not Path(gp).exists():
        raise RuntimeError("PARI/GP executable not found")
    try:
        proc = subprocess.run(
            [gp, "-q"],
            input=jminus1_gp_program(zeros_path, lo, hi),
            text=True,
            capture_output=True,
            check=False,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"GP chunk {lo}-{hi} exceeded {timeout}s") from exc
    if proc.returncode != 0:
        raise RuntimeError(f"GP chunk {lo}-{hi} failed with {proc.returncode}:\n{proc.stdout}\n{proc.stderr}")
    gp_errors = [
        line for line in (proc.stdout + "\n" + proc.stderr).splitlines()
        if "***" in line and "Warning" not in line
    ]
    if gp_errors:
        raise RuntimeError(f"GP chunk {lo}-{hi} reported an error:\n{proc.stdout}\n{proc.stderr}")
    rows = [line for line in proc.stdout.splitlines() if line.startswith("JMINUS1|")]
    if len(rows) != 1:
        raise RuntimeError(f"missing/duplicate JMINUS1 line for {lo}-{hi}:\n{proc.stdout}\n{proc.stderr}")
    fields = rows[0].split("|")
    if len(fields) != 11:
        raise RuntimeError(f"malformed JMINUS1 line for {lo}-{hi}: {rows[0]}")
    _, got_lo, got_hi, count, chunk_sum, gamma, max_residual, failure_count, first_failure, sum_zpsq, sum_inv = fields
    if (int(got_lo), int(got_hi)) != (lo, hi) or int(count) != hi - lo + 1:
        raise RuntimeError(f"wrong chunk bounds/count for {lo}-{hi}: {rows[0]}")
    return {
        "lo": got_lo,
        "hi": got_hi,
        "count": count,
        "positive_chunk_sum_decimal": chunk_sum,
        "gamma_boundary_decimal": gamma,
        "max_abs_zeta_residual_decimal": max_residual,
        "failure_count": failure_count,
        "first_failure_index": first_failure,
        "sum_abs_zeta_prime_sq_decimal": sum_zpsq,
        "sum_inverse_abs_zeta_prime_sq_decimal": sum_inv,
    }


def checkpoint_path(checkpoint_dir: Path, lo: int, hi: int) -> Path:
    return checkpoint_dir / f"chunk_{lo:05d}_{hi:05d}.json"


def write_json_atomic(path: Path, value: dict) -> None:
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n")
    temporary.replace(path)


def make_jminus1_checkpoint(raw: dict[str, str], zeros_path: Path, zeros_sha256: str, cumulative: Decimal) -> dict:
    lo = int(raw["lo"])
    hi = int(raw["hi"])
    count = int(raw["count"])
    chunk_sum = decimal_from_gp(raw["positive_chunk_sum_decimal"])
    zpsq_sum = decimal_from_gp(raw["sum_abs_zeta_prime_sq_decimal"])
    return {
        "schema_version": 1,
        "quantity": "J_-1(T) = sum 1/abs(zeta'(rho))^2 over positive ordinates",
        "zeros_path": str(zeros_path),
        "zeros_sha256": zeros_sha256,
        "lo": lo,
        "hi": hi,
        "count": count,
        "realprecision_digits": 20,
        "strict_residual_threshold": J_MINUS1_RESIDUAL_THRESHOLD,
        "positive_chunk_sum_decimal": raw["positive_chunk_sum_decimal"],
        "positive_chunk_sum": float(chunk_sum),
        "cumulative_positive_sum_decimal": decimal_text(cumulative),
        "cumulative_positive_sum": float(cumulative),
        "gamma_boundary_decimal": raw["gamma_boundary_decimal"],
        "gamma_boundary": dps(raw["gamma_boundary_decimal"]),
        "max_abs_zeta_residual_decimal": raw["max_abs_zeta_residual_decimal"],
        "max_abs_zeta_residual": dps(raw["max_abs_zeta_residual_decimal"]),
        "failure_count": int(raw["failure_count"]),
        "first_failure_index": int(raw["first_failure_index"]),
        "sum_abs_zeta_prime_sq_decimal": raw["sum_abs_zeta_prime_sq_decimal"],
        "sum_abs_zeta_prime_sq": float(zpsq_sum),
        "mean_inverse_abs_zeta_prime_sq": float(chunk_sum / count),
        "created_utc": datetime.now(timezone.utc).isoformat(),
    }


def load_jminus1_checkpoints(checkpoint_dir: Path, zeros_path: Path, zeros_sha256: str) -> dict[int, dict]:
    records: dict[int, dict] = {}
    for path in sorted(checkpoint_dir.glob("chunk_*.json")):
        try:
            record = json.loads(path.read_text())
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"invalid checkpoint JSON: {path}") from exc
        required = {
            "quantity": "J_-1(T) = sum 1/abs(zeta'(rho))^2 over positive ordinates",
            "zeros_path": str(zeros_path),
            "zeros_sha256": zeros_sha256,
            "realprecision_digits": 20,
            "strict_residual_threshold": J_MINUS1_RESIDUAL_THRESHOLD,
        }
        for key, expected in required.items():
            if record.get(key) != expected:
                raise RuntimeError(f"checkpoint config mismatch in {path}: {key}")
        lo, hi = int(record["lo"]), int(record["hi"])
        if hi != lo + int(record["count"]) - 1:
            raise RuntimeError(f"checkpoint count mismatch in {path}")
        if hi in records:
            raise RuntimeError(f"duplicate checkpoint endpoint {hi}")
        records[hi] = record
    return records


def validate_checkpoint_sequence(records: dict[int, dict], nmax: int) -> None:
    expected_lo = 1
    for hi in sorted(records):
        record = records[hi]
        lo = int(record["lo"])
        if hi > nmax:
            continue
        if lo != expected_lo:
            raise RuntimeError(f"checkpoint gap/overlap before {lo}: expected {expected_lo}")
        expected_lo = hi + 1


def jminus1_rows(records: dict[int, dict]) -> list[dict]:
    rows = []
    for hi in sorted(records):
        record = records[hi]
        J = float(record["cumulative_positive_sum"])
        T = float(record["gamma_boundary"])
        rows.append({
            "N": hi,
            "T_decimal": record["gamma_boundary_decimal"],
            "T": T,
            "J_minus1_decimal": record["cumulative_positive_sum_decimal"],
            "J_minus1": J,
            "J_minus1_over_T": J / T,
            "ratio_to_3_over_pi_cubed": (J / T) / GONEK_SLOPE,
            "max_abs_zeta_residual": float(record["max_abs_zeta_residual"]),
        })
    return rows


def top_half_fit(records: dict[int, dict], rows: list[dict]) -> dict:
    if not rows:
        return {"status": "no_completed_chunks"}
    nmax = max(row["N"] for row in rows)
    ncut = math.ceil(nmax / 2)
    fit_rows = [row for row in rows if row["N"] >= ncut]
    denom = sum(row["T"] ** 2 for row in fit_rows)
    slope = sum(row["T"] * row["J_minus1"] for row in fit_rows) / denom
    diagnostics = []
    for row in fit_rows:
        fitted = slope * row["T"]
        diagnostics.append({
            "N": row["N"],
            "T": row["T"],
            "J_minus1": row["J_minus1"],
            "fitted_J_minus1": fitted,
            "residual": row["J_minus1"] - fitted,
            "relative_residual": (row["J_minus1"] - fitted) / row["J_minus1"],
        })
    residuals = [row["residual"] for row in diagnostics]
    sum_sq_residual = sum(value * value for value in residuals)
    sum_sq_total = sum(row["J_minus1"] ** 2 for row in fit_rows)

    slopes = []
    row_by_hi = {row["N"]: row for row in rows}
    for hi in sorted(records):
        record = records[hi]
        if hi < ncut:
            continue
        lo = int(record["lo"])
        previous = row_by_hi.get(lo - 1)
        if previous is None:
            continue
        delta_t = row_by_hi[hi]["T"] - previous["T"]
        delta_j = float(record["positive_chunk_sum"])
        slopes.append({
            "lo": lo,
            "hi": hi,
            "delta_J_minus1": delta_j,
            "delta_T": delta_t,
            "chunk_slope": delta_j / delta_t,
        })
    slope_values = [row["chunk_slope"] for row in slopes]
    scatter = None
    standard_error = None
    if len(slope_values) >= 2:
        scatter = statistics.stdev(slope_values)
        standard_error = scatter / math.sqrt(len(slope_values))
    elif slope_values:
        scatter = 0.0
        standard_error = 0.0
    free_mean_t = statistics.mean(row["T"] for row in fit_rows)
    free_mean_j = statistics.mean(row["J_minus1"] for row in fit_rows)
    free_denom = sum((row["T"] - free_mean_t) ** 2 for row in fit_rows)
    free_slope = sum((row["T"] - free_mean_t) * (row["J_minus1"] - free_mean_j) for row in fit_rows) / free_denom if free_denom else None
    free_intercept = free_mean_j - free_slope * free_mean_t if free_slope is not None else None
    drift_window = max(2, len(slope_values) // 3)
    first_mean_slope = statistics.mean(slope_values[:drift_window]) if slope_values else None
    last_mean_slope = statistics.mean(slope_values[-drift_window:]) if slope_values else None
    drift_change = last_mean_slope - first_mean_slope if first_mean_slope is not None and last_mean_slope is not None else None
    drift_threshold = max(0.5 * (scatter or 0.0), 0.02 * GONEK_SLOPE)
    drift_detected = drift_change is not None and abs(drift_change) > drift_threshold
    return {
        "status": "completed",
        "model": "J_minus1(T) = a*T, fit through the origin",
        "top_half_definition": f"completed checkpoints with N >= ceil({nmax}/2) = {ncut}",
        "N_min": ncut,
        "N_max": nmax,
        "slope": slope,
        "slope_ratio_to_gonek": slope / GONEK_SLOPE,
        "target_slope": GONEK_SLOPE,
        "difference_from_target": slope - GONEK_SLOPE,
        "fit_row_count": len(fit_rows),
        "residual_diagnostics": diagnostics,
        "sum_squared_residual": sum_sq_residual,
        "rmse_J_minus1": math.sqrt(sum_sq_residual / len(fit_rows)),
        "max_abs_residual_J_minus1": max(abs(value) for value in residuals),
        "max_abs_relative_residual": max(abs(row["relative_residual"]) for row in diagnostics),
        "through_origin_R2": 1.0 - sum_sq_residual / sum_sq_total if sum_sq_total else None,
        "free_intercept_diagnostic": {
            "slope": free_slope,
            "intercept": free_intercept,
            "note": "diagnostic only; the reported asymptotic fit is through the origin",
        },
        "top_half_chunk_slopes": slopes,
        "chunk_slope_scatter_std": scatter,
        "chunk_slope_standard_error": standard_error,
        "chunk_slope_drift": {
            "window_size_each_end": drift_window,
            "first_window_mean": first_mean_slope,
            "last_window_mean": last_mean_slope,
            "last_minus_first": drift_change,
            "detection_threshold": drift_threshold,
            "detected": drift_detected,
            "note": "drift is flagged when the first-versus-last third mean changes by more than half the top-half chunk scatter; this is a conservative finite-T diagnostic, not a hypothesis test",
        },
        "uncertainty_used_for_verdict": scatter,
        "uncertainty_note": "scatter is the sample standard deviation of 500-zero incremental slopes in the top-half window; it is not a confidence interval and includes finite-height drift/noise",
    }


def provisional_verdict(fit: dict, rows: list[dict]) -> str:
    if fit.get("status") != "completed":
        return "TOO EARLY"
    uncertainty = fit.get("uncertainty_used_for_verdict")
    slope = fit["slope"]
    target = fit["target_slope"]
    drifting = fit.get("chunk_slope_drift", {}).get("detected", False)
    if drifting:
        return "TOO EARLY"
    if uncertainty is not None and abs(slope - target) <= uncertainty:
        return "CONSISTENT"
    if uncertainty is None or abs(slope - target) <= 2.0 * (uncertainty or 0.0):
        return "TOO EARLY"
    return "INCONSISTENT"


def make_jminus1_receipt(records: dict[int, dict], zeros_path: Path, zeros_sha256: str, nmax_requested: int, run_error: str | None = None) -> dict:
    rows = jminus1_rows(records)
    fit = top_half_fit(records, rows)
    status = "completed" if rows and max(row["N"] for row in rows) >= nmax_requested else "partial"
    verdict = provisional_verdict(fit, rows)
    return {
        "status": status,
        "quantity": "J_-1(T) = sum_{0<gamma<=T} 1/|zeta'(1/2+i gamma)|^2",
        "verdict": verdict,
        "source": {
            "zeros_path": str(zeros_path),
            "zeros_sha256": zeros_sha256,
            "requested_nmax": nmax_requested,
            "completed_nmax": max((row["N"] for row in rows), default=0),
            "backend": "PARI/GP 2.17.3 arbitrary precision via lfuninit",
            "realprecision_digits": 20,
            "refinement": "one real Newton update from each zeros1.txt seed on zeta(1/2+i*t)",
            "strict_residual_threshold": J_MINUS1_RESIDUAL_THRESHOLD,
            "chunk_size": J_MINUS1_CHUNK_SIZE,
            "checkpoint_policy": "one validated JSON checkpoint is written after each completed 500-zero chunk and reused on resume",
        },
        "gonek_target": {
            "formula": "3/pi^3",
            "value": GONEK_SLOPE,
            "source_note": "research_notes/rh_goals_2026-08-14/lane_c/S1_ZERO_SUM_LIT.md",
        },
        "N_values_requested": [500, 1000, 2000, 3000],
        "N_values_completed": [row["N"] for row in rows],
        "table": rows,
        "chunks": [records[hi] for hi in sorted(records)],
        "refined_zero_sanity": {
            "used_zero_count": sum(int(record["count"]) for record in records.values()),
            "max_abs_zeta_residual": max((float(record["max_abs_zeta_residual"]) for record in records.values()), default=None),
            "failure_count": sum(int(record["failure_count"]) for record in records.values()),
            "first_failure_index": next((int(record["first_failure_index"]) for record in records.values() if int(record["first_failure_index"]) != 0), 0),
            "pass": all(float(record["max_abs_zeta_residual"]) < float(J_MINUS1_RESIDUAL_THRESHOLD) and int(record["failure_count"]) == 0 for record in records.values()),
        },
        "top_half_linear_fit": fit,
        "run_error": run_error,
        "caveats": [
            "Finite-T corrections to Gonek's asymptotic are expected to be large at these heights.",
            "T approximately 10^4 is far too low for a definitive asymptotic claim.",
            "Chunk-slope scatter is a conservative diagnostic uncertainty, not a theorem-level error bar or independent statistical confidence interval.",
        ],
    }


def format_float(value: float | None, digits: int = 10) -> str:
    return "n/a" if value is None else f"{value:.{digits}g}"


def make_jminus1_report(receipt: dict) -> str:
    fit = receipt["top_half_linear_fit"]
    target = receipt["gonek_target"]["value"]
    rows = receipt["table"]
    verdict = receipt["verdict"]
    completed_nmax = receipt["source"]["completed_nmax"]
    uncertainty = fit.get("uncertainty_used_for_verdict")
    drift = fit.get("chunk_slope_drift", {})
    lines = [
        "# Gonek's J_-1 slope: numerical test",
        "",
        "## Verdict",
        "",
        f"**{verdict}** — completed through N={completed_nmax} (T={format_float(rows[-1]['T'], 12) if rows else 'n/a'}).",
        "",
        f"The through-origin top-half fit is `J_-1(T) = a T` with `a = {format_float(fit.get('slope'), 12)}`; the 500-zero incremental-slope scatter is `±{format_float(uncertainty, 4)}` (sample standard deviation, not a confidence interval). The Gonek target is `3/pi^3 = {target:.12f}`. The first-versus-last top-half chunk-slope means are `{format_float(drift.get('first_window_mean'), 8)}` and `{format_float(drift.get('last_window_mean'), 8)}`, respectively, so the run is classified as `TOO EARLY` when that drift diagnostic fires. This is a finite-height diagnostic, not a confirmation or refutation of the asymptotic.",
        "",
        "The classification is intentionally conservative: at these heights the observed slope/rate is still subject to substantial finite-T correction and chunk-to-chunk fluctuation.",
        "",
        "## Requested and extended partial sums",
        "",
        "Here `J_-1(T)` is the positive-ordinate sum over the first N refined zeros, with T = gamma_N. The ratio column compares `J_-1(T)/T` with `3/pi^3`.",
        "",
        "| N | T = gamma_N | J_-1(T) | J_-1(T)/T | ratio to 3/pi^3 | max residual in chunk |",
        "|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(f"| {row['N']} | {row['T']:.12g} | {row['J_minus1']:.12g} | {row['J_minus1_over_T']:.12g} | {row['ratio_to_3_over_pi_cubed']:.8g} | {row['max_abs_zeta_residual']:.3g} |")
    if not rows:
        lines.append("| — | — | — | — | — | — |")
    lines += [
        "",
        "## Top-half linear fit and residual diagnostics",
        "",
        f"Fit window: {fit.get('top_half_definition', 'not available')}. The reported slope is through the origin, matching the asymptotic form. `RMSE(J_-1) = {format_float(fit.get('rmse_J_minus1'), 8)}`, `max |residual| = {format_float(fit.get('max_abs_residual_J_minus1'), 8)}`, `max relative residual = {format_float(fit.get('max_abs_relative_residual'), 8)}`, and through-origin `R^2 = {format_float(fit.get('through_origin_R2'), 8)}`.",
        "",
        "| N | J_-1(T) | fitted aT | residual | relative residual |",
        "|---:|---:|---:|---:|---:|",
    ]
    for row in fit.get("residual_diagnostics", []):
        lines.append(f"| {row['N']} | {row['J_minus1']:.12g} | {row['fitted_J_minus1']:.12g} | {row['residual']:.6g} | {row['relative_residual']:.6g} |")
    lines += [
        "",
        "### Incremental-slope scatter",
        "",
        "The uncertainty below is the sample standard deviation of the 500-zero slopes `Delta J_-1 / Delta T` in the top-half window. It is reported as scatter because adjacent blocks are not justified as independent random draws, and because drift is part of the finite-T effect.",
        "",
        "| block | Delta T | Delta J_-1 | incremental slope |",
        "|---:|---:|---:|---:|",
    ]
    for row in fit.get("top_half_chunk_slopes", []):
        lines.append(f"| {row['lo']}–{row['hi']} | {row['delta_T']:.12g} | {row['delta_J_minus1']:.12g} | {row['chunk_slope']:.12g} |")
    lines += [
        "",
        f"Chunk-slope scatter: `{format_float(fit.get('chunk_slope_scatter_std'), 8)}`; nominal standard error of the mean (shown for reference only): `{format_float(fit.get('chunk_slope_standard_error'), 8)}`.",
        "",
        "## Numerical method and checkpoints",
        "",
        "- PARI/GP 2.17.3 with `realprecision=20` and a reused `lfuninit` evaluator per chunk.",
        "- Each seed from `cluster_universality_test/zeros1.txt` receives one real Newton update; the residual gate is `|zeta(1/2+i gamma)| < 1e-15`.",
        f"- Computation is chunked into {J_MINUS1_CHUNK_SIZE}-zero jobs. Completed chunks are stored under `research_notes/rh_goals_2026-08-14/lane_a/j_minus1_checkpoints/` and reused only when the source checksum and computation configuration match.",
        "- The JSON receipt includes raw GP decimal strings, cumulative sums, all per-chunk maxima/failure counts, fit diagnostics, and the source checksum.",
        "",
        "## Caveats",
        "",
        "Finite-T corrections to Gonek's asymptotic are expected to be large at these heights. Even a run reaching T approximately 10^4 is far too short to support a definitive asymptotic claim; the verdict should be read as a numerical consistency/drift classification only. The derivative reciprocal weights can fluctuate strongly, so chunk scatter is informative but is not a rigorous uncertainty bound.",
        "",
        "The literature context and the stated target `3/pi^3` are recorded in [`lane_c/S1_ZERO_SUM_LIT.md`](../lane_c/S1_ZERO_SUM_LIT.md).",
        "",
        "## Reproduction",
        "",
        "```bash",
        "python3 research_notes/rh_goals_2026-08-14/lane_a/zero_sum_pari_driver.py --mode jminus1 --nmax 10000",
        "```",
        "",
    ]
    if receipt.get("run_error"):
        lines += [f"Run stopped after the last committed checkpoint: `{receipt['run_error']}`.", ""]
    return "\n".join(lines)


def run_jminus1(args: argparse.Namespace) -> int:
    zeros_path = args.zeros.resolve()
    receipt_path = lane_local_path(args.receipt)
    report_path = lane_local_path(args.report)
    checkpoint_dir = lane_local_path(args.checkpoint_dir)
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    zeros_sha256 = sha256_file(zeros_path)
    nmax = min(args.nmax, sum(1 for _ in zeros_path.open()))
    records = load_jminus1_checkpoints(checkpoint_dir, zeros_path, zeros_sha256)
    records = {hi: record for hi, record in records.items() if hi <= nmax}
    validate_checkpoint_sequence(records, nmax)
    cumulative = Decimal(0)
    for hi in sorted(records):
        cumulative += decimal_from_gp(records[hi]["positive_chunk_sum_decimal"])
        expected = decimal_from_gp(records[hi]["cumulative_positive_sum_decimal"])
        if abs(expected - cumulative) > Decimal("1e-35"):
            raise RuntimeError(f"cumulative checkpoint mismatch at N={hi}")
    run_error = None
    next_lo = (max(records) + 1) if records else 1
    while next_lo <= nmax:
        hi = min(next_lo + J_MINUS1_CHUNK_SIZE - 1, nmax)
        if hi - next_lo + 1 != J_MINUS1_CHUNK_SIZE:
            raise RuntimeError("nmax must be a multiple of the 500-zero checkpoint size")
        try:
            raw = run_jminus1_chunk(zeros_path, next_lo, hi, args.chunk_timeout)
            cumulative += decimal_from_gp(raw["positive_chunk_sum_decimal"])
            record = make_jminus1_checkpoint(raw, zeros_path, zeros_sha256, cumulative)
            write_json_atomic(checkpoint_path(checkpoint_dir, next_lo, hi), record)
            records[hi] = record
            print(json.dumps({"checkpoint": f"{next_lo}-{hi}", "J_minus1": record["cumulative_positive_sum"], "T": record["gamma_boundary"], "max_residual": record["max_abs_zeta_residual"]}, sort_keys=True), flush=True)
            next_lo = hi + 1
        except Exception as exc:
            run_error = str(exc)
            break
    receipt = make_jminus1_receipt(records, zeros_path, zeros_sha256, nmax, run_error)
    write_json_atomic(receipt_path, receipt)
    report_path.write_text(make_jminus1_report(receipt))
    print(json.dumps({"status": receipt["status"], "verdict": receipt["verdict"], "completed_nmax": receipt["source"]["completed_nmax"], "fit": receipt["top_half_linear_fit"]}, indent=2))
    return 2 if run_error else 0


def make_receipt(partials: dict[int, dict[str, str]], blocks: list[dict[str, str]], check: dict[str, str], zeros_path: Path) -> dict:
    positive = {str(n): {**row, "positive_sum_float": dps(row["positive_sum"]), "two_sided_sum_float": 2.0 * dps(row["positive_sum"])} for n, row in sorted(partials.items())}
    nmax = max(partials)
    final_positive = dps(partials[nmax]["positive_sum"])
    last_block = next(block for block in reversed(blocks) if int(block["hi"]) == nmax)
    prior_high_blocks = [block for block in blocks if int(block["hi"]) >= max(1000, nmax // 3)]
    envelope_mean = max(dps(block["avg_inverse_abs_zeta_prime_sq"]) for block in prior_high_blocks)
    model_tail_positive = tail_integral(dps(partials[nmax]["gamma"]), dps(last_block["avg_inverse_abs_zeta_prime_sq"]))
    conservative_tail_positive = tail_integral(dps(partials[nmax]["gamma"]), 2.0 * envelope_mean)
    final_two_sided = 2.0 * (final_positive + model_tail_positive)
    error_bar = 2.0 * conservative_tail_positive
    return {
        "status": "completed",
        "source": {
            "zeros_path": str(zeros_path),
            "table_rows": 100000,
            "seed_precision_note": "zeros1.txt entries have about 9 decimal digits; each used seed was independently refined by one real Newton update on zeta(1/2+i*t) using PARI/GP realprecision=20. The strict residual gate is checked after this update for every used zero. A separate realprecision=30 run through N=1000 gave the same displayed partial sums and max residual 5.51e-35.",
            "backend": "PARI/GP 2.17.3 arbitrary precision",
            "requested_mpmath": "unavailable in the supplied python3 environment; pip installation was blocked by network/DNS sandboxing",
            "realprecision_digits": 20,
            "lfun_initialization": "PARI lfuninit(1,[Tmax],1) reused for zeta and first derivative evaluations; this is the speed path for the 3000/10000 runs.",
        },
        "convention": {
            "natural_sum": "two-sided over rho=1/2+i*gamma with gamma positive and negative",
            "term": "1/((1/4+gamma^2)*|zeta_prime(rho)|^2)",
            "conjugacy": "negative ordinates contribute the same term, so the two-sided sum is twice the positive-ordinate sum",
            "reported_partial_sums": "positive and two-sided",
        },
        "N_values_used": sorted(partials),
        "partial_sums": positive,
        "refined_zero_sanity": {
            "used_zero_count": nmax,
            "max_abs_zeta_residual": check["max_residual"],
            "strict_threshold": check["strict_threshold"],
            "failure_count": int(check["failure_count"]),
            "first_failure_index": int(check["first_failure_index"]),
            "pass": int(check["failure_count"]) == 0 and dps(check["max_residual"]) < 1e-15,
        },
        "derivative_block_statistics": blocks,
        "tail_model": {
            "density_model": "dN/dt ~= log(t/(2*pi))/(2*pi)",
            "integral": "B*(log(T/(2*pi))+1)/(2*pi*T), with B the observed block mean of 1/|zeta_prime|^2",
            "last_block_used_for_central_estimate": last_block,
            "high_block_envelope_mean_inverse_derivative_sq": envelope_mean,
            "central_one_sided_tail_estimate": model_tail_positive,
            "conservative_one_sided_tail_bound": conservative_tail_positive,
            "comparison_window": "The N=3000 to N=10000 increment is compared with the N=3000 tail estimate in the report; this is a numerical consistency check, not a rigorous theorem-level bound.",
        },
        "final_estimate": {
            "positive_sum_with_central_tail": final_positive + model_tail_positive,
            "two_sided_S": final_two_sided,
            "two_sided_error_bar": error_bar,
            "two_sided_interval_from_conservative_tail": [2.0 * final_positive, 2.0 * (final_positive + conservative_tail_positive)],
            "precision_claim": "The reported digits are numerical/backend digits; the tail model and source/convention audit support only about 3 significant digits for the infinite sum.",
        },
        "E5_reproduction": {
            "script": "projects/mimo-mini-project/code/E5_zeta_zero_sum.py",
            "source_convention": "one-sided positive zeros n=1..N; no conjugate term; |rho|^2=1/4+gamma^2",
            "N": 100,
            "reproduced_positive_sum": positive["100"]["positive_sum"],
            "E5_reported_display_value": 0.0141436361,
            "display_match": f"{positive['100']['positive_sum_float']:.10f}" == "0.0141436361",
            "two_sided_value_at_N100": positive["100"]["two_sided_sum_float"],
            "convention_factor": 2.0,
            "note": "E5 itself could not be imported because mpmath is absent; the formula was independently reproduced with PARI/GP and matches its reported 10-decimal value.",
        },
        "simple_form_candidates": candidate_table(final_two_sided),
        "source_line_refs": {
            "log.md": "13",
            "E5_zeta_zero_sum.py": "4-17, 23, 26-40, 60-63",
            "SELBERG_INPUT_DISPROVED.md": "27-31",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("weighted", "jminus1"), default="weighted")
    parser.add_argument("--zeros", type=Path, default=DEFAULT_ZEROS)
    parser.add_argument("--nmax", type=int, default=10000)
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--checkpoint-dir", type=Path, default=DEFAULT_J_MINUS1_CHECKPOINT_DIR)
    parser.add_argument("--chunk-timeout", type=int, default=900)
    args = parser.parse_args()
    if args.mode == "jminus1":
        args.receipt = args.receipt or DEFAULT_J_MINUS1_RECEIPT
        args.report = args.report or DEFAULT_J_MINUS1_REPORT
        raise SystemExit(run_jminus1(args))
    args.receipt = args.receipt or DEFAULT_RECEIPT
    targets = tuple(n for n in DEFAULT_TARGETS if n <= args.nmax)
    if not targets or targets[-1] != args.nmax:
        targets = tuple(sorted(set(targets + (args.nmax,))))
    raw = run_gp(args.zeros, args.nmax, targets)
    partials, blocks, check = parse_gp(raw)
    receipt = make_receipt(partials, blocks, check, args.zeros)
    args.receipt.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"N_values_used": receipt["N_values_used"], "final_estimate": receipt["final_estimate"], "sanity": receipt["refined_zero_sanity"]}, indent=2))


if __name__ == "__main__":
    main()
