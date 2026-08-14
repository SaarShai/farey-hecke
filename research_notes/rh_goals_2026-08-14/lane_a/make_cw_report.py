#!/usr/bin/env python3
"""Turn cw_growth_values.csv into the required evidence-first report."""

from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CSV = ROOT / "cw_growth_values.csv"


def read_rows() -> list[dict]:
    rows = []
    with CSV.open(newline="") as handle:
        for raw in csv.DictReader(handle):
            row = {key: value for key, value in raw.items()}
            for key in (
                "N", "Phi", "n", "C_W", "C_W_direct", "C_alt_positive",
                "C_fast_proxy", "C_fast_minus_direct", "J_direct_inclusive",
                "J_fast_inclusive", "J_fast_minus_direct", "T_N", "Jordan_sum",
            ):
                if row.get(key) not in (None, ""):
                    row[key] = float(row[key]) if key not in ("N", "Phi", "n") else int(float(row[key]))
            rows.append(row)
    return rows


def fit_loglog(rows: list[dict]) -> tuple[float, float, list[float]]:
    xs = [math.log(math.log(row["N"])) for row in rows]
    ys = [row["C_W"] for row in rows]
    xbar = sum(xs) / len(xs)
    ybar = sum(ys) / len(ys)
    beta = sum((x - xbar) * (y - ybar) for x, y in zip(xs, ys)) / sum((x - xbar) ** 2 for x in xs)
    alpha = ybar - beta * xbar
    residuals = [y - (alpha + beta * x) for x, y in zip(xs, ys)]
    return alpha, beta, residuals


def fmt(x: float | None, digits: int = 9) -> str:
    return "—" if x is None else f"{x:.{digits}f}"


def main() -> None:
    rows = read_rows()
    by_n = {row["N"]: row for row in rows}
    direct_rows = [row for row in rows if row.get("C_W_direct") not in (None, "")]
    proxy_residuals = [abs(row["C_fast_minus_direct"]) for row in direct_rows]
    j_residuals = [abs(row["J_fast_minus_direct"]) for row in direct_rows]
    max_proxy = max(proxy_residuals)
    max_j = max(j_residuals)
    max_proxy_large = max(
        abs(row["C_fast_minus_direct"])
        for row in direct_rows
        if row["N"] >= 1000
    )

    fit_rows = [row for row in rows if row["N"] >= 10_000]
    alpha, beta, residuals = fit_loglog(fit_rows)
    fixed_beta = 0.24
    fixed_alpha = sum(
        row["C_W"] - fixed_beta * math.log(math.log(row["N"])) for row in fit_rows
    ) / len(fit_rows)
    fixed_residuals = [
        row["C_W"] - (fixed_alpha + fixed_beta * math.log(math.log(row["N"])))
        for row in fit_rows
    ]
    claimed_residuals = [
        row["C_W"] - (0.16 + 0.24 * math.log(math.log(row["N"])))
        for row in fit_rows
    ]
    const_target = 0.679
    const_residuals = [row["C_W"] - const_target for row in fit_rows]

    decade_pairs = []
    for row in rows:
        target = 10 * row["N"]
        if target in by_n:
            c0 = row["C_W"]
            c1 = by_n[target]["C_W"]
            increment = math.log(math.log(target)) - math.log(math.log(row["N"]))
            decade_pairs.append((row["N"], target, c1 - c0, increment, fixed_beta * increment))

    extra_pair = None
    if 300_000 in by_n and 3_000_000 in by_n:
        n0, n1 = 300_000, 3_000_000
        inc = math.log(math.log(n1)) - math.log(math.log(n0))
        extra_pair = (n0, n1, by_n[n1]["C_W"] - by_n[n0]["C_W"], inc, fixed_beta * inc)

    anchors = [
        (100, 0.497),
        (1_000, 0.635),
        (100_000, 0.668),
    ]

    observed_increments = [abs(item[2]) for item in decade_pairs]
    predicted_increments = [item[4] for item in decade_pairs]
    increment_ratios = [a / b for a, b in zip(observed_increments, predicted_increments)]

    # The requested alternatives are not separated by the sampled trajectory:
    # the fixed beta=.24 law is far too steep, while the exact 0.679+-0.002
    # claim is hit by some rows and missed by the 3e5 and 1e7 rows.  Report
    # UNDECIDED rather than calling a finite, spiky sample a theorem.
    verdict = "UNDECIDED at reached N"

    lines = []
    lines.append(f"{verdict}")
    lines.append("")
    lines.append("# C_W(N) growth audit")
    lines.append("")
    lines.append(
        "Verdict is deliberately scoped to the computed data through "
        f"N={max(row['N'] for row in rows):,}. The measured sequence is "
        "incompatible with the proposed fixed-slope loglog law, but the "
        "finite sample also has spikes (notably N=300,000 and 10,000,000) "
        "outside the claimed 0.679 ± 0.002 band."
    )
    lines.append("")
    lines.append("## Decade increments")
    lines.append("")
    lines.append(
        "The `0.24 prediction` is 0.24·[log log(10N) − log log N]. "
        "All C values below are actual rows in the CSV; no interpolation is used."
    )
    lines.append("")
    lines.append("| N | 10N | C_W(N) | C_W(10N) | measured Δ | Δloglog | 0.24·Δloglog | |Δ|/prediction |")
    lines.append("|---:|---:|---:|---:|---:|---:|---:|---:|")
    for n0, n1, delta, ll, pred in decade_pairs:
        ratio = abs(delta) / pred
        lines.append(
            f"| {n0:,} | {n1:,} | {by_n[n0]['C_W']:.9f} | {by_n[n1]['C_W']:.9f} | "
            f"{delta:+.9f} | {ll:.9f} | {pred:.9f} | {ratio:.3f} |"
        )
    if extra_pair is not None:
        n0, n1, delta, ll, pred = extra_pair
        lines.append("")
        lines.append(
            f"Additional requested 3× pair: `{n0:,} → {n1:,}` has "
            f"Δ={delta:+.9f}; 0.24·Δloglog={pred:.9f}."
        )
    lines.append("")
    high_ratios = [item[2] and abs(item[2]) / item[4] for item in decade_pairs if item[0] >= 1_000]
    lines.append(
        f"Across the high-N decade pairs (N≥1,000), max |Δ|/predicted increment = {max(high_ratios):.3f}; "
        "the measured changes are below the 0.24·loglog increments, "
        "but are not monotone or rapidly convergent to one fixed value. "
        "The 100→1,000 row is a low-N transient and is shown for completeness."
    )

    lines.append("")
    lines.append("## Anchor reproduction")
    lines.append("")
    lines.append("| N | expected | measured C_W | source | rounded | pass to 3 decimals |")
    lines.append("|---:|---:|---:|---|---:|:---:|")
    for n, expected in anchors:
        row = by_n[n]
        measured = row["C_W"]
        rounded = round(measured, 3)
        lines.append(
            f"| {n:,} | {expected:.3f} | {measured:.9f} | {row['C_W_source']} | "
            f"{rounded:.3f} | {'PASS' if rounded == expected else 'FAIL'} |"
        )
    lines.append("")
    lines.append(
        "The direct route reproduces the N=100 and N=1,000 anchors. N=100,000 "
        "is the fast Mertens/Jordan row and reproduces the stated 0.668 anchor."
    )

    lines.append("")
    lines.append("## Direct versus fast validation")
    lines.append("")
    lines.append(
        "The Mertens identity is exact for the inclusive CDF integral J, not for the "
        "requested discrete rank sum W. Therefore both residuals are reported:"
    )
    lines.append("")
    lines.append("| check over N≤2,000 | max absolute difference | interpretation |")
    lines.append("|---|---:|---|")
    lines.append(
        f"| fast J versus direct inclusive-J stream | {max_j:.3e} | identity/implementation check; numerical roundoff |"
    )
    lines.append(
        f"| N·J/Phi proxy versus requested C_W | {max_proxy:.9f} | finite statistic/convention gap; max over N=100,1000,2000 |"
    )
    lines.append(
        f"| same proxy residual restricted to N≥1,000 | {max_proxy_large:.9f} | decays approximately like a boundary correction, but is not zero |"
    )
    lines.append("")
    lines.append(
        "This is the key scope limitation: claiming zero fast-vs-direct error for C_W "
        "would conflate W with J. The report keeps the exact requested direct values "
        "and labels the large-N Mertens rows as a proxy whose small-N calibration is visible."
    )

    lines.append("")
    lines.append("## Measured trajectory")
    lines.append("")
    lines.append("| N | C_W row | row source | T(N) |")
    lines.append("|---:|---:|---|---:|")
    for row in rows:
        lines.append(
            f"| {row['N']:,} | {row['C_W']:.9f} | {row['C_W_source']} | {row['T_N']:.6f} |"
        )

    lines.append("")
    lines.append("## Loglog fit")
    lines.append("")
    lines.append(
        "Free least-squares fit on all measured rows with N≥10,000: "
        f"C_W = α + β log log N, α={alpha:.9f}, β={beta:.9f}."
    )
    lines.append(
        "The imported claim's fixed slope β=0.24 was also fit in α only: "
        f"α_fixed={fixed_alpha:.9f}."
    )
    lines.append("")
    lines.append("| N | residual free (β fitted) | residual best α, β=0.24 | residual claimed 0.16+0.24loglog | residual from C=0.679 |")
    lines.append("|---:|---:|---:|---:|---:|")
    for row, rfree, rfixed, rclaimed, rconst in zip(fit_rows, residuals, fixed_residuals, claimed_residuals, const_residuals):
        lines.append(
            f"| {row['N']:,} | {rfree:+.9f} | {rfixed:+.9f} | {rclaimed:+.9f} | {rconst:+.9f} |"
        )
    lines.append("")
    lines.append(
        f"Free-fit RMSE={math.sqrt(sum(x*x for x in residuals)/len(residuals)):.9f}; "
        f"best-α fixed-β RMSE={math.sqrt(sum(x*x for x in fixed_residuals)/len(fixed_residuals)):.9f}; "
        f"claimed-parameter RMSE={math.sqrt(sum(x*x for x in claimed_residuals)/len(claimed_residuals)):.9f}."
    )
    lines.append(
        "The fitted β is far below 0.24, so these runs reject the stated loglog slope "
        "as a description of this trajectory. They do not establish convergence to "
        "0.679 ± 0.002, because the sampled spikes remain larger than that band."
    )
    lines.append(
        "The fit uses the `C_W` column: its N≤2,000 rows are direct rank sums, while "
        "all N≥10,000 rows are the explicitly labeled Mertens/Jordan proxy."
    )

    lines.append("")
    lines.append("## Method and scope")
    lines.append("")
    lines.append(
        "Direct route: next-Farey recurrence, endpoint-inclusive ranks, numpy.longdouble "
        "accumulation, N≤2,000. Fast route: numpy Möbius sieve, Mertens prefix M, "
        "quotient-block evaluation of T(x), and the Jordan-totient convolution for J; "
        "no Farey fractions are enumerated at N≥10,000."
    )
    lines.append("")
    lines.append(
        "Largest reached: N=10,000,000 by the fast route. Runtime and sieve metadata "
        "are in cw_growth_receipt.json. No value beyond 10,000,000 is extrapolated; "
        "the α,β numbers are fits only."
    )
    lines.append("")
    lines.append(
        "Source files inspected: `research_notes/imported_farey_now/FRANEL_LANDAU_LOWER_BOUND.md:15-23,49-70`, "
        "`projects/mimo-mini-project/research_notes/Mertens_NW_conjecture.md:11-24,76-78`, and "
        "`equispaced-primes/bcz-cocycle/verify_bcz_cocycle.py:86-96,160-204`."
    )
    lines.append("")

    (ROOT / "CW_GROWTH_REPORT.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
