#!/usr/bin/env python3
"""Path B conductor-control queue runner.

This script is deliberately split into two halves:

1. PARI/GP bridge: check whether `gp` is available, emit the exact B1/B2
   discovery commands, and optionally run those discovery scripts on a machine
   that has `gp` plus `pari-elldata`.
2. NumPy-only decision bridge: ingest the stored Path B CSV plus any computed
   selected-control CSV rows and run the requested row-bootstrap gates.

It does not claim that B1/B2 controls pass unless computed control rows are
present and pass the bootstrap, leave-one-out, and leverage gates.
"""

from __future__ import annotations

import argparse
import csv
import math
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np


SEED = 20260510
BOOTSTRAPS = 20000

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BASE_CSV = ROOT / "koyama-shared" / "data" / "PATH_B_20FORMS.csv"
DEFAULT_CONTROL_CSVS = [
    ROOT / "koyama-shared" / "data" / "PATH_B_SELECTED_CONTROLS.csv",
    ROOT / "koyama-shared" / "data" / "PATH_B_CONTROL_ROWS.csv",
    ROOT / "koyama-shared" / "data" / "PATH_B_B1_B2_CONTROLS.csv",
]

ELLDATA_DIRS = [
    Path("/opt/homebrew/share/pari/elldata"),
    Path("/usr/local/share/pari/elldata"),
    Path("/usr/share/pari/elldata"),
    Path("/opt/local/share/pari/elldata"),
]

BANDS = {
    "B1": {
        "lo": 350,
        "hi": 650,
        "target_conductors": [389, 433, 446, 571],
        "required": {0: 3, 1: 3},
        "high_rank": 2,
    },
    "B2": {
        "lo": 4500,
        "hi": 5600,
        "target_conductors": [5077],
        "required": {0: 2, 1: 2, 2: 2},
        "high_rank": 3,
    },
}

PREFLIGHT_GP_BODY = """default(realprecision, 50);
print("ellsearch389_count,", #ellsearch(389));
E=ellinit("5077a1");
print("5077a1,rank,", ellanalyticrank(E)[1], ",N,", ellglobalred(E)[1]);
"""

B1_DISCOVERY_BODY = """default(realprecision, 50);
for(N=350,650,
  C=ellsearch(N);
  for(i=1,#C,
    lab=C[i][1];
    E=ellinit(lab);
    r=ellanalyticrank(E)[1];
    if(r<=1, print(lab,",",r,",",ellglobalred(E)[1]))
  )
)
"""

B2_DISCOVERY_BODY = """default(realprecision, 50);
for(N=4500,5600,
  C=ellsearch(N);
  for(i=1,#C,
    lab=C[i][1];
    E=ellinit(lab);
    r=ellanalyticrank(E)[1];
    if(r<=2, print(lab,",",r,",",ellglobalred(E)[1]))
  )
)
"""

GP_BODIES = {
    "preflight": PREFLIGHT_GP_BODY,
    "b1": B1_DISCOVERY_BODY,
    "b2": B2_DISCOVERY_BODY,
}


@dataclass(frozen=True)
class Row:
    label: str
    rank: int
    weight: int
    conductor: int
    y: float
    n_zeros: int | None
    source: str


@dataclass
class FitResult:
    name: str
    n: int
    p: int
    beta: float | None = None
    ci: tuple[float, float] | None = None
    p_nonpos: float | None = None
    loo_range: tuple[float, float] | None = None
    max_leverage: float | None = None
    r2: float | None = None
    rmse: float | None = None
    accepted: bool = False
    status: str = "not_run"
    skipped_bootstrap: int = 0


def gp_heredoc(body: str) -> str:
    return "gp -q --default parisizemax=4G <<'GP'\n" + body.rstrip() + "\nGP"


def compute_command(label: str) -> str:
    return f"""LABEL={label}
TMAX=1000
KMAX=10000
gp -q --default parisizemax=4G <<GP
default(realprecision, 50);
E=ellinit("$LABEL");
print("META,", "$LABEL", ",", ellanalyticrank(E)[1], ",", ellglobalred(E)[1]);
Z=lfunzeros(E,[1e-6,$TMAX]);
n=min(#Z,200);
for(i=1,n, print("ZERO,",i,",",Z[i]));
forprime(p=2,$KMAX, print("AP,",p,",",ellap(E,p)));
for(i=1,n,
  v=lfun(E,1+I*Z[i],1);
  print("LPRIME,",i,",",real(v),",",imag(v))
);
GP"""


def gp_status() -> tuple[str | None, list[Path]]:
    gp_path = shutil.which("gp")
    present_dirs = [path for path in ELLDATA_DIRS if path.exists()]
    return gp_path, present_dirs


def run_gp(body: str) -> str:
    proc = subprocess.run(
        ["gp", "-q", "--default", "parisizemax=4G"],
        input=body,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or f"gp exited {proc.returncode}")
    return proc.stdout


def parse_int(value: str | None, default: int = 0) -> int:
    if value is None or value == "":
        return default
    return int(float(value))


def parse_float(value: str | None) -> float | None:
    if value is None or value == "":
        return None
    return float(value)


def read_rows(path: Path, source: str) -> tuple[list[Row], list[str]]:
    rows: list[Row] = []
    warnings: list[str] = []
    if not path.exists():
        return rows, warnings

    with path.open(newline="") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None:
            warnings.append(f"{path}: empty CSV")
            return rows, warnings
        fieldnames = set(reader.fieldnames)
        required = {"label", "rank", "conductor"}
        if not required.issubset(fieldnames):
            warnings.append(f"{path}: missing required columns {sorted(required - fieldnames)}")
            return rows, warnings
        if "E_C1_sq" not in fieldnames:
            warnings.append(f"{path}: metadata only; no E_C1_sq column, not used in gates")
            return rows, warnings

        for line_no, raw in enumerate(reader, start=2):
            label = (raw.get("label") or "").strip()
            error = (raw.get("error") or "").strip()
            y = parse_float(raw.get("E_C1_sq"))
            if not label or error or y is None or not math.isfinite(y):
                continue
            try:
                rank = parse_int(raw.get("rank"))
                conductor = parse_int(raw.get("conductor"))
                weight = parse_int(raw.get("weight"), default=2)
                n_zeros = parse_int(raw.get("N_zeros"), default=0) if "N_zeros" in fieldnames else None
            except ValueError as exc:
                warnings.append(f"{path}:{line_no}: skipped parse error: {exc}")
                continue
            rows.append(Row(label, rank, weight, conductor, y, n_zeros, source))
    return rows, warnings


def load_all_rows(base_csv: Path, control_csvs: Iterable[Path]) -> tuple[list[Row], list[str], list[Path]]:
    warnings: list[str] = []
    loaded_paths: list[Path] = []
    by_label: dict[str, Row] = {}

    for path, source in [(base_csv, "base"), *[(p, "control") for p in control_csvs]]:
        rows, row_warnings = read_rows(path, source)
        warnings.extend(row_warnings)
        if rows:
            loaded_paths.append(path)
        for row in rows:
            if row.label in by_label:
                warnings.append(f"{path}: duplicate label {row.label} ignored; first row kept")
                continue
            by_label[row.label] = row

    return list(by_label.values()), warnings, loaded_paths


def ec_rows(rows: Iterable[Row]) -> list[Row]:
    return [row for row in rows if row.label != "Delta" and row.rank >= 0 and row.weight == 2]


def rows_for_band(rows: Iterable[Row], band: str) -> list[Row]:
    spec = BANDS[band]
    lo = int(spec["lo"])
    hi = int(spec["hi"])
    high_rank = int(spec["high_rank"])
    ranks = set(int(r) for r in spec["required"]) | {high_rank}
    return [
        row
        for row in rows
        if lo <= row.conductor <= hi and row.rank in ranks
    ]


def band_counts(rows: Iterable[Row]) -> dict[int, int]:
    counts: dict[int, int] = {}
    for row in rows:
        counts[row.rank] = counts.get(row.rank, 0) + 1
    return counts


def missing_requirements(rows: Iterable[Row], band: str) -> dict[int, int]:
    counts = band_counts(rows)
    missing: dict[int, int] = {}
    for rank, required in BANDS[band]["required"].items():
        have = counts.get(int(rank), 0)
        if have < int(required):
            missing[int(rank)] = int(required) - have
    high_rank = int(BANDS[band]["high_rank"])
    if counts.get(high_rank, 0) == 0:
        missing[high_rank] = 1
    return missing


def design_matrix(rows: list[Row], model: str) -> tuple[np.ndarray, np.ndarray, list[str], int]:
    y = np.array([row.y for row in rows], dtype=float)
    rank = np.array([row.rank for row in rows], dtype=float)
    cols = [np.ones(len(rows)), rank]
    names = ["intercept", "rank"]

    if model in {"rank_logN", "rank_logN_interaction"}:
        logn = np.log(np.array([row.conductor for row in rows], dtype=float))
        lognc = logn - float(np.mean(logn))
        cols.append(lognc)
        names.append("logNc")
        if model == "rank_logN_interaction":
            cols.append(rank * lognc)
            names.append("rank:logNc")
    elif model == "rank_tier":
        tiers = []
        for row in rows:
            if BANDS["B1"]["lo"] <= row.conductor <= BANDS["B1"]["hi"]:
                tiers.append(0.0)
            elif BANDS["B2"]["lo"] <= row.conductor <= BANDS["B2"]["hi"]:
                tiers.append(1.0)
            else:
                tiers.append(float("nan"))
        tier = np.array(tiers, dtype=float)
        if np.isnan(tier).any():
            raise ValueError("rank_tier requires rows inside B1/B2")
        cols.append(tier)
        names.append("tier_B2")

    return np.column_stack(cols), y, names, names.index("rank")


def solve_beta(X: np.ndarray, y: np.ndarray) -> np.ndarray | None:
    if len(y) <= X.shape[1]:
        return None
    if np.linalg.matrix_rank(X) < X.shape[1]:
        return None
    return np.linalg.solve(X.T @ X, X.T @ y)


def fit_model(
    name: str,
    rows: list[Row],
    model: str,
    *,
    seed: int,
    bootstraps: int,
) -> FitResult:
    X, y, names, rank_idx = design_matrix(rows, model)
    result = FitResult(name=name, n=len(rows), p=X.shape[1])
    beta = solve_beta(X, y)
    if beta is None:
        result.status = "incomplete_or_singular"
        return result

    fitted = X @ beta
    resid = y - fitted
    ss_res = float(np.sum(resid**2))
    ss_tot = float(np.sum((y - float(np.mean(y))) ** 2))
    result.beta = float(beta[rank_idx])
    result.r2 = float(1.0 - ss_res / ss_tot) if ss_tot > 0 else float("nan")
    result.rmse = float(np.sqrt(np.mean(resid**2)))

    xtx_inv = np.linalg.inv(X.T @ X)
    leverage = np.einsum("ij,jk,ik->i", X, xtx_inv, X)
    result.max_leverage = float(np.max(leverage))

    loo_betas: list[float] = []
    for drop in range(len(rows)):
        keep = np.arange(len(rows)) != drop
        loo_beta = solve_beta(X[keep], y[keep])
        if loo_beta is None:
            result.status = "loo_singular"
            return result
        loo_betas.append(float(loo_beta[rank_idx]))
    result.loo_range = (float(min(loo_betas)), float(max(loo_betas)))

    rng = np.random.default_rng(seed)
    boot_betas: list[float] = []
    skipped = 0
    n = len(rows)
    for _ in range(bootstraps):
        idx = rng.integers(0, n, n)
        boot_beta = solve_beta(X[idx], y[idx])
        if boot_beta is None:
            skipped += 1
            continue
        boot_betas.append(float(boot_beta[rank_idx]))
    result.skipped_bootstrap = skipped
    if not boot_betas:
        result.status = "bootstrap_singular"
        return result

    boots = np.array(boot_betas, dtype=float)
    ci_low, ci_high = np.quantile(boots, [0.025, 0.975])
    result.ci = (float(ci_low), float(ci_high))
    result.p_nonpos = float(np.mean(boots <= 0.0))
    result.accepted = (
        result.beta > 0.0
        and result.ci[0] > 0.0
        and result.p_nonpos <= 0.025
        and result.loo_range[0] > 0.0
        and result.max_leverage < 0.50
    )
    result.status = "pass" if result.accepted else "fail"
    return result


def fmt_float(value: float | None, digits: int = 6) -> str:
    if value is None:
        return "n/a"
    return f"{value:.{digits}f}"


def fmt_ci(ci: tuple[float, float] | None) -> str:
    if ci is None:
        return "n/a"
    return f"[{ci[0]:.6f}, {ci[1]:.6f}]"


def fmt_range(values: tuple[float, float] | None) -> str:
    if values is None:
        return "n/a"
    return f"[{values[0]:.6f}, {values[1]:.6f}]"


def print_fit(result: FitResult) -> None:
    print(
        f"{result.name}: status={result.status}; n={result.n}; p={result.p}; "
        f"rank_beta={fmt_float(result.beta)}; ci95={fmt_ci(result.ci)}; "
        f"P(beta<=0)={fmt_float(result.p_nonpos, 5)}; "
        f"LOO={fmt_range(result.loo_range)}; "
        f"max_leverage={fmt_float(result.max_leverage)}; "
        f"R2={fmt_float(result.r2)}; RMSE={fmt_float(result.rmse)}; "
        f"bootstrap_skipped={result.skipped_bootstrap}"
    )


def run_gate_set(rows: list[Row], label: str, models: list[tuple[str, str]], seed: int, bootstraps: int) -> list[FitResult]:
    print(f"\n[{label}] rows={len(rows)}")
    for row in sorted(rows, key=lambda r: (r.conductor, r.rank, r.label)):
        print(f"  {row.label}: rank={row.rank}, N={row.conductor}, y={row.y:.6f}, source={row.source}")

    results: list[FitResult] = []
    for model_label, model in models:
        result = fit_model(model_label, rows, model, seed=seed, bootstraps=bootstraps)
        print_fit(result)
        results.append(result)
    return results


def parse_discovery_lines(path: Path) -> list[tuple[str, int, int]]:
    controls: list[tuple[str, int, int]] = []
    with path.open() as fh:
        for line in fh:
            stripped = line.strip()
            if not stripped or stripped.startswith(("BAND", "FALLBACK_BAND")):
                continue
            parts = [part.strip() for part in stripped.split(",")]
            if len(parts) < 3:
                continue
            try:
                controls.append((parts[0], int(parts[1]), int(parts[2])))
            except ValueError:
                continue
    return controls


def select_controls(discovery_path: Path, band: str) -> None:
    spec = BANDS[band]
    lo = int(spec["lo"])
    hi = int(spec["hi"])
    targets = [int(n) for n in spec["target_conductors"]]
    required = {int(rank): int(count) for rank, count in spec["required"].items()}
    discovered = [
        (label, rank, conductor)
        for label, rank, conductor in parse_discovery_lines(discovery_path)
        if lo <= conductor <= hi and rank in required
    ]

    print(f"Selected {band} controls from {discovery_path}:")
    for rank, count in sorted(required.items()):
        bucket = [item for item in discovered if item[1] == rank]
        bucket.sort(key=lambda item: (min(abs(item[2] - target) for target in targets), item[2], item[0]))
        selected = bucket[:count]
        if len(selected) < count:
            print(f"  rank {rank}: only {len(selected)}/{count} discovered")
        for label, selected_rank, conductor in selected:
            dist = min(abs(conductor - target) for target in targets)
            print(f"  {label},{selected_rank},{conductor},nearest_target_distance={dist}")


def emit_gp(which: str) -> None:
    names = ["preflight", "b1", "b2"] if which == "all" else [which]
    for name in names:
        print(f"\n# {name.upper()} GP command")
        print(gp_heredoc(GP_BODIES[name]))


def execute_discovery(which: str) -> int:
    gp_path, present_dirs = gp_status()
    if not gp_path:
        print("gp not on PATH; discovery not run", file=sys.stderr)
        return 2
    if not present_dirs:
        print("warning: no standard pari-elldata directory found", file=sys.stderr)

    names = ["b1", "b2"] if which == "all" else [which]
    for name in names:
        print(f"# {name.upper()} discovery output")
        print(run_gp(GP_BODIES[name]).rstrip())
    return 0


def run_default(args: argparse.Namespace) -> int:
    control_csvs = list(DEFAULT_CONTROL_CSVS if args.use_default_controls else [])
    control_csvs.extend(Path(path) for path in args.controls_csv)
    rows, warnings, loaded_paths = load_all_rows(args.base_csv, control_csvs)
    ec = ec_rows(rows)

    gp_path, present_dirs = gp_status()
    print("Path B conductor-control runner")
    print(f"root={ROOT}")
    print(f"gp={'absent' if gp_path is None else gp_path}")
    print("pari_elldata_dirs=" + (", ".join(str(p) for p in present_dirs) if present_dirs else "none-found"))
    print("loaded_csvs=" + (", ".join(str(p) for p in loaded_paths) if loaded_paths else "none"))
    for warning in warnings:
        print(f"warning: {warning}")
    print(f"ec_rows={len(ec)}; seed={args.seed}; bootstraps={args.bootstrap}")

    for band in ("B1", "B2"):
        band_rows = rows_for_band(ec, band)
        counts = band_counts(band_rows)
        missing = missing_requirements(band_rows, band)
        counts_text = ", ".join(f"rank{rank}={count}" for rank, count in sorted(counts.items())) or "none"
        missing_text = ", ".join(f"rank{rank}:{count}" for rank, count in sorted(missing.items())) or "none"
        print(f"\n{band} matrix: counts={counts_text}; missing={missing_text}")
        if missing:
            print(f"{band} verdict=incomplete_controls")
        else:
            results = run_gate_set(
                band_rows,
                band,
                [(f"{band} rank", "rank"), (f"{band} rank+logN", "rank_logN")],
                args.seed,
                args.bootstrap,
            )
            print(f"{band} verdict={'pass' if all(r.accepted for r in results) else 'fail'}")

    b1_rows = rows_for_band(ec, "B1")
    b2_rows = rows_for_band(ec, "B2")
    combined_missing = {f"B1 rank{k}": v for k, v in missing_requirements(b1_rows, "B1").items()}
    combined_missing.update({f"B2 rank{k}": v for k, v in missing_requirements(b2_rows, "B2").items()})
    print("\nB1+B2 matrix: missing=" + (", ".join(f"{k}:{v}" for k, v in combined_missing.items()) or "none"))
    if combined_missing:
        print("B1+B2 verdict=incomplete_controls")
    else:
        results = run_gate_set(
            b1_rows + b2_rows,
            "B1+B2",
            [
                ("B1+B2 rank+logN", "rank_logN"),
                ("B1+B2 interaction", "rank_logN_interaction"),
                ("B1+B2 rank+tier", "rank_tier"),
            ],
            args.seed,
            args.bootstrap,
        )
        print(f"B1+B2 verdict={'pass' if all(r.accepted for r in results) else 'fail'}")

    if args.current_diagnostic:
        run_gate_set(
            ec,
            "current EC diagnostic, not an acceptance claim",
            [
                ("current rank", "rank"),
                ("current rank+logN", "rank_logN"),
                ("current interaction", "rank_logN_interaction"),
            ],
            args.seed,
            args.bootstrap,
        )

    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-csv", type=Path, default=DEFAULT_BASE_CSV)
    parser.add_argument("--controls-csv", action="append", default=[], help="computed selected-control CSV with E_C1_sq")
    parser.add_argument("--no-default-controls", dest="use_default_controls", action="store_false")
    parser.set_defaults(use_default_controls=True)
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--bootstrap", type=int, default=BOOTSTRAPS)
    parser.add_argument("--current-diagnostic", action="store_true", help="also refit all current EC rows")
    parser.add_argument("--emit-gp", choices=["preflight", "b1", "b2", "all"], help="print exact GP command packet")
    parser.add_argument("--discover", choices=["b1", "b2", "all"], help="run GP discovery if gp is available")
    parser.add_argument("--compute-command", metavar="LABEL", help="print exact per-curve GP input command")
    parser.add_argument("--select-discovery", type=Path, help="parse GP discovery output and select nearest controls")
    parser.add_argument("--select-band", choices=["B1", "B2"], default="B1")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.emit_gp:
        emit_gp(args.emit_gp)
    if args.compute_command:
        print(compute_command(args.compute_command))
    if args.select_discovery:
        select_controls(args.select_discovery, args.select_band)
    if args.discover:
        return execute_discovery(args.discover)
    if args.emit_gp or args.compute_command or args.select_discovery:
        return 0
    return run_default(args)


if __name__ == "__main__":
    raise SystemExit(main())
