#!/usr/bin/env python3
"""A4 continuation for the weighted zero sum.

The existing receipt is authoritative for the already computed 1--3000
weighted sum. This driver computes only missing 500-zero chunks, leaving A3's
J_-1 checkpoints untouched. Each checkpoint contains raw GP decimals and the
first-order root-residual sensitivity budget used by the v2 analysis.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation, getcontext
import hashlib
import json
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
LANE_DIR = Path(__file__).resolve().parent
BASE_RECEIPT = LANE_DIR / "zero_sum_receipt.json"
DEFAULT_ZEROS = ROOT / "cluster_universality_test" / "zeros1.txt"
DEFAULT_CHECKPOINT_DIR = LANE_DIR / "a4_checkpoints"
DEFAULT_MANIFEST = DEFAULT_CHECKPOINT_DIR / "a4_partial_manifest.json"
CHUNK_SIZE = 500
REALPRECISION = 20
RESIDUAL_THRESHOLD = "1e-15"
getcontext().prec = 80


def local_path(path: Path) -> Path:
    resolved = path.expanduser().resolve()
    try:
        resolved.relative_to(LANE_DIR.resolve())
    except ValueError as exc:
        raise ValueError(f"path outside lane_a: {resolved}") from exc
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
        raise ValueError(f"invalid GP decimal: {value!r}") from exc


def decimal_text(value: Decimal) -> str:
    return format(value, ".60g")


def gp_program(zeros_path: Path, lo: int, hi: int, precision: int = REALPRECISION) -> str:
    gp_path = str(zeros_path).replace("\\", "\\\\").replace('"', '\\"')
    return f'''default(realprecision,{precision})
default(parisizemax,2G)
xs=readvec("{gp_path}");
Tmax=xs[{hi}]+10;
L=lfuninit(1,[Tmax],2);
refine(t0)={{
  my(t=t0,s,z,zp);
  s=1/2+I*t;
  z=lfun(L,s);
  zp=lfun(L,s,1);
  t=real(t-z/(I*zp));
  t
}};
S=0; sum_inv=0; sum_zpsq=0; sum_seed_bound=0; max_root_error=0;
maxres=0; failcount=0; firstfail=0; last_t=0; count=0;
process(n)={{
  my(t,s,z,zp,zpp,res,zpsq,inv,term,root_error,log_slope);
  t=refine(xs[n]); s=1/2+I*t; z=lfun(L,s); zp=lfun(L,s,1); zpp=lfun(L,s,2);
  res=abs(z); if(res>maxres,maxres=res);
  if(res>={RESIDUAL_THRESHOLD},failcount=failcount+1);
  if(res>={RESIDUAL_THRESHOLD} && firstfail==0,firstfail=n);
  zpsq=abs(zp)^2; inv=1/zpsq; term=inv/(1/4+t^2);
  root_error=res/abs(zp);
  log_slope=abs(-2*t/(1/4+t^2)-2*real(I*zpp/zp));
  sum_inv=sum_inv+inv; sum_zpsq=sum_zpsq+zpsq;
  sum_seed_bound=sum_seed_bound+term*log_slope*root_error;
  if(root_error>max_root_error,max_root_error=root_error);
  S=S+term; last_t=t; count=count+1
}};
for(n={lo},{hi},process(n));
print("A4|",{lo},"|",{hi},"|",count,"|",S,"|",last_t,"|",maxres,"|",failcount,"|",firstfail,"|",sum_inv,"|",sum_zpsq,"|",sum_seed_bound,"|",max_root_error);
'''


def run_gp(zeros_path: Path, lo: int, hi: int, timeout: int, precision: int = REALPRECISION) -> dict[str, str]:
    gp = shutil.which("gp") or "/opt/homebrew/bin/gp"
    if not Path(gp).exists():
        raise RuntimeError("PARI/GP executable not found")
    try:
        proc = subprocess.run(
            [gp, "-q"],
            input=gp_program(zeros_path, lo, hi, precision),
            text=True,
            capture_output=True,
            check=False,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"GP chunk {lo}-{hi} exceeded {timeout}s") from exc
    if proc.returncode != 0:
        raise RuntimeError(f"GP chunk {lo}-{hi} failed with {proc.returncode}:\n{proc.stdout}\n{proc.stderr}")
    errors = [
        line for line in (proc.stdout + "\n" + proc.stderr).splitlines()
        if "***" in line and "Warning" not in line
    ]
    if errors:
        raise RuntimeError(f"GP chunk {lo}-{hi} reported an error:\n{proc.stdout}\n{proc.stderr}")
    rows = [line for line in proc.stdout.splitlines() if line.startswith("A4|")]
    if len(rows) != 1:
        raise RuntimeError(f"missing/duplicate A4 line for {lo}-{hi}:\n{proc.stdout}\n{proc.stderr}")
    fields = rows[0].split("|")
    if len(fields) != 13:
        raise RuntimeError(f"malformed A4 line for {lo}-{hi}: {rows[0]}")
    _, got_lo, got_hi, count, chunk_sum, gamma, max_residual, failures, first_failure, sum_inv, sum_zpsq, seed_bound, max_root_error = fields
    if (int(got_lo), int(got_hi), int(count)) != (lo, hi, hi - lo + 1):
        raise RuntimeError(f"wrong chunk bounds/count for {lo}-{hi}: {rows[0]}")
    return {
        "lo": got_lo,
        "hi": got_hi,
        "count": count,
        "positive_chunk_sum_decimal": chunk_sum,
        "gamma_boundary_decimal": gamma,
        "max_abs_zeta_residual_decimal": max_residual,
        "failure_count": failures,
        "first_failure_index": first_failure,
        "sum_inverse_abs_zeta_prime_sq_decimal": sum_inv,
        "sum_abs_zeta_prime_sq_decimal": sum_zpsq,
        "sum_seed_first_order_bound_decimal": seed_bound,
        "max_root_error_decimal": max_root_error,
    }


def checkpoint_path(directory: Path, lo: int, hi: int) -> Path:
    return directory / f"weighted_chunk_{lo:05d}_{hi:05d}.json"


def write_json_atomic(path: Path, value: dict) -> None:
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n")
    temporary.replace(path)


def make_checkpoint(raw: dict[str, str], zeros_path: Path, source_sha: str, cumulative: Decimal, precision: int) -> dict:
    lo, hi, count = int(raw["lo"]), int(raw["hi"]), int(raw["count"])
    chunk_sum = decimal_from_gp(raw["positive_chunk_sum_decimal"])
    return {
        "schema_version": 1,
        "quantity": "positive weighted zero-sum chunk",
        "zeros_path": str(zeros_path),
        "zeros_sha256": source_sha,
        "lo": lo,
        "hi": hi,
        "count": count,
        "realprecision_digits": precision,
        "strict_residual_threshold": RESIDUAL_THRESHOLD,
        "positive_chunk_sum_decimal": raw["positive_chunk_sum_decimal"],
        "positive_chunk_sum": float(chunk_sum),
        "cumulative_positive_sum_decimal": decimal_text(cumulative),
        "cumulative_positive_sum": float(cumulative),
        "gamma_boundary_decimal": raw["gamma_boundary_decimal"],
        "gamma_boundary": float(decimal_from_gp(raw["gamma_boundary_decimal"])),
        "max_abs_zeta_residual_decimal": raw["max_abs_zeta_residual_decimal"],
        "max_abs_zeta_residual": float(decimal_from_gp(raw["max_abs_zeta_residual_decimal"])),
        "failure_count": int(raw["failure_count"]),
        "first_failure_index": int(raw["first_failure_index"]),
        "sum_inverse_abs_zeta_prime_sq_decimal": raw["sum_inverse_abs_zeta_prime_sq_decimal"],
        "sum_inverse_abs_zeta_prime_sq": float(decimal_from_gp(raw["sum_inverse_abs_zeta_prime_sq_decimal"])),
        "mean_inverse_abs_zeta_prime_sq": float(decimal_from_gp(raw["sum_inverse_abs_zeta_prime_sq_decimal"]) / count),
        "sum_abs_zeta_prime_sq_decimal": raw["sum_abs_zeta_prime_sq_decimal"],
        "sum_abs_zeta_prime_sq": float(decimal_from_gp(raw["sum_abs_zeta_prime_sq_decimal"])),
        "sum_seed_first_order_bound_decimal": raw["sum_seed_first_order_bound_decimal"],
        "sum_seed_first_order_bound": float(decimal_from_gp(raw["sum_seed_first_order_bound_decimal"])),
        "max_root_error_decimal": raw["max_root_error_decimal"],
        "max_root_error": float(decimal_from_gp(raw["max_root_error_decimal"])),
        "created_utc": datetime.now(timezone.utc).isoformat(),
    }


def load_base(receipt_path: Path) -> tuple[dict, Decimal]:
    receipt = json.loads(receipt_path.read_text())
    if receipt.get("status") not in {"completed", "completed_through_N3000"}:
        raise RuntimeError("base zero_sum_receipt.json is not a completed N=3000 receipt")
    if receipt.get("partial_sums", {}).get("3000") is None:
        raise RuntimeError("base receipt has no N=3000 partial sum")
    if not receipt.get("refined_zero_sanity", {}).get("pass"):
        raise RuntimeError("base receipt residual gate did not pass")
    return receipt, decimal_from_gp(receipt["partial_sums"]["3000"]["sum_decimal"])


def load_checkpoints(directory: Path, zeros_path: Path, source_sha: str, nmax: int) -> dict[int, dict]:
    records: dict[int, dict] = {}
    for path in sorted(directory.glob("weighted_chunk_*.json")):
        record = json.loads(path.read_text())
        required = {
            "quantity": "positive weighted zero-sum chunk",
            "zeros_path": str(zeros_path),
            "zeros_sha256": source_sha,
            "realprecision_digits": REALPRECISION,
            "strict_residual_threshold": RESIDUAL_THRESHOLD,
        }
        if any(record.get(key) != value for key, value in required.items()):
            raise RuntimeError(f"checkpoint configuration mismatch: {path}")
        lo, hi = int(record["lo"]), int(record["hi"])
        if hi > nmax:
            continue
        if hi != lo + int(record["count"]) - 1 or hi in records:
            raise RuntimeError(f"invalid checkpoint bounds: {path}")
        records[hi] = record
    expected = 3001
    for hi in sorted(records):
        lo = int(records[hi]["lo"])
        if lo != expected:
            raise RuntimeError(f"checkpoint gap/overlap before {lo}; expected {expected}")
        expected = hi + 1
    return records


def run(args: argparse.Namespace) -> int:
    zeros_path = args.zeros.resolve()
    checkpoint_dir = local_path(args.checkpoint_dir)
    manifest_path = local_path(args.manifest)
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    if args.nmax < 3000 or args.nmax % CHUNK_SIZE:
        raise ValueError("nmax must be >=3000 and a multiple of 500")
    source_sha = sha256_file(zeros_path)
    base_receipt, base_sum = load_base(local_path(args.base_receipt))
    records = load_checkpoints(checkpoint_dir, zeros_path, source_sha, args.nmax)
    cumulative = base_sum
    for hi in sorted(records):
        cumulative += decimal_from_gp(records[hi]["positive_chunk_sum_decimal"])
        expected = decimal_from_gp(records[hi]["cumulative_positive_sum_decimal"])
        if abs(cumulative - expected) > Decimal("1e-35"):
            raise RuntimeError(f"cumulative checkpoint mismatch at N={hi}")
    next_lo = (max(records) + 1) if records else 3001
    while next_lo <= args.nmax:
        hi = next_lo + CHUNK_SIZE - 1
        raw = run_gp(zeros_path, next_lo, hi, args.chunk_timeout, REALPRECISION)
        cumulative += decimal_from_gp(raw["positive_chunk_sum_decimal"])
        record = make_checkpoint(raw, zeros_path, source_sha, cumulative, REALPRECISION)
        write_json_atomic(checkpoint_path(checkpoint_dir, next_lo, hi), record)
        records[hi] = record
        print(json.dumps({"checkpoint": f"{next_lo}-{hi}", "positive_sum": record["cumulative_positive_sum"], "T": record["gamma_boundary"], "max_residual": record["max_abs_zeta_residual"]}, sort_keys=True), flush=True)
        next_lo = hi + 1
    manifest = {
        "schema_version": 1,
        "status": "completed" if max(records, default=3000) >= args.nmax else "partial",
        "base_receipt": str(local_path(args.base_receipt)),
        "base_nmax": 3000,
        "zeros_path": str(zeros_path),
        "zeros_sha256": source_sha,
        "backend": "PARI/GP via lfuninit",
        "realprecision_digits": REALPRECISION,
        "strict_residual_threshold": RESIDUAL_THRESHOLD,
        "nmax_requested": args.nmax,
        "nmax_completed": max(records, default=3000),
        "base_positive_sum_decimal": decimal_text(base_sum),
        "positive_sum_through_nmax_decimal": decimal_text(cumulative),
        "checkpoint_files": [checkpoint_path(checkpoint_dir, int(record["lo"]), int(record["hi"])).name for record in records.values()],
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "a3_input_note": "A3 j_minus1_checkpoints/ is read-only input to the v2 analysis; no A3 file is written by this driver.",
    }
    write_json_atomic(manifest_path, manifest)
    print(json.dumps(manifest, indent=2))
    return 0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--zeros", type=Path, default=DEFAULT_ZEROS)
    parser.add_argument("--nmax", type=int, default=10000)
    parser.add_argument("--base-receipt", type=Path, default=BASE_RECEIPT)
    parser.add_argument("--checkpoint-dir", type=Path, default=DEFAULT_CHECKPOINT_DIR)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--chunk-timeout", type=int, default=900)
    args = parser.parse_args()
    raise SystemExit(run(args))


if __name__ == "__main__":
    main()
