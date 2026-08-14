#!/usr/bin/env python3
"""Assemble verified disjoint PARI/GP chunk outputs into the final receipt."""
from __future__ import annotations

import json
import math
from decimal import Decimal, getcontext
from pathlib import Path

getcontext().prec = 60
OUT = Path(__file__).with_name("zero_sum_receipt.json")


def tail(t: float, b: float) -> float:
    return b * (math.log(t / (2 * math.pi)) + 1.0) / (2 * math.pi * t)


positive = {
    100: {"sum_decimal": "0.014143636055307528166323303194652066514885810944939", "gamma_boundary": "236.5242296658162058024755079556629786895", "last_term": "1.119973820976382267588729334313511198959e-6"},
    300: {"sum_decimal": "0.014349494265830052515341359322883050484927217144387", "gamma_boundary": "541.8474371212012815471135089067366934", "last_term": "1.697151397496350019791027506105626265034e-7"},
    1000: {"sum_decimal": "0.014453988690945204289262086429312854356887409167449", "gamma_boundary": "1419.422480945995686465989038079916819232", "last_term": "6.401936845343375033823629646834431645181e-8"},
}
positive[3000] = {
    "sum_decimal": str(Decimal(positive[1000]["sum_decimal"]) + Decimal("2.6534999055519456767e-5") + Decimal("9.3886382343934035441e-6")),
    "gamma_boundary": "3533.328243396",
    "last_term": None,
}
for row in positive.values():
    row["positive_sum"] = float(row["sum_decimal"])
    row["two_sided_sum"] = 2.0 * row["positive_sum"]

blocks = [
    {"lo": 1, "hi": 100, "count": 100, "avg_abs_zeta_prime_sq": 7.424856136465548266013030128776962254359, "avg_inverse_abs_zeta_prime_sq": 0.24098167980550711178685986015373489571837790215},
    {"lo": 101, "hi": 300, "count": 200, "avg_abs_zeta_prime_sq": 14.27673809200597071991086326777665437267, "avg_inverse_abs_zeta_prime_sq": 0.13525052228865585287137955071364527432580820151286},
    {"lo": 301, "hi": 1000, "count": 700, "avg_abs_zeta_prime_sq": 22.94594754928510838732745994602841660554, "avg_inverse_abs_zeta_prime_sq": 0.11955532029817237823228398930515866475825703896519},
    {"lo": 1001, "hi": 2000, "count": 1000, "avg_abs_zeta_prime_sq": 31.286898629640162044, "avg_inverse_abs_zeta_prime_sq": 0.096100230448799721428},
    {"lo": 2001, "hi": 3000, "count": 1000, "avg_abs_zeta_prime_sq": 37.185308306437457359, "avg_inverse_abs_zeta_prime_sq": 0.083416242982841375780},
]

T3000 = float(positive[3000]["gamma_boundary"])
last_b = blocks[-1]["avg_inverse_abs_zeta_prime_sq"]
high_b_envelope = max(block["avg_inverse_abs_zeta_prime_sq"] for block in blocks[2:])
central_tail_3000 = tail(T3000, last_b)
conservative_tail_3000 = tail(T3000, 2.0 * high_b_envelope)
s3000 = positive[3000]["positive_sum"]
final_s = 2.0 * (s3000 + central_tail_3000)
error_bar = 2.0 * conservative_tail_3000
observed_increment = positive[3000]["positive_sum"] - positive[1000]["positive_sum"]
tail_1000 = tail(float(positive[1000]["gamma_boundary"]), blocks[2]["avg_inverse_abs_zeta_prime_sq"])

pi = math.pi
candidate_values = {
    "2/pi^2": 2.0 / pi**2,
    "1/(2*pi^2)": 1.0 / (2.0 * pi**2),
    "1/pi^3 = (2/pi^2)/(2*pi)": 1.0 / pi**3,
    "2/pi^4": 2.0 / pi**4,
    "3/pi^4": 3.0 / pi**4,
    "6/pi^4": 6.0 / pi**4,
    "(2/pi^2)/(2*pi)^2 = 1/(2*pi^4)": 1.0 / (2.0 * pi**4),
    "1/(2*pi^3)": 1.0 / (2.0 * pi**3),
}
candidates = sorted(
    ({"form": form, "value": value, "absolute_residual": abs(final_s - value), "relative_residual": abs(final_s - value) / final_s} for form, value in candidate_values.items()),
    key=lambda row: row["absolute_residual"],
)

receipt = {
    "status": "completed_through_N3000",
    "source": {
        "zeros_path": "/Users/za/Documents/farey-hecke/cluster_universality_test/zeros1.txt",
        "table_rows": 100000,
        "seed_precision_note": "zeros1.txt entries have about 9 decimal digits. Each used seed was refined by one real Newton update on zeta(1/2+i*t) using PARI/GP; the strict residual gate was checked at every used zero.",
        "backend": "PARI/GP 2.17.3 arbitrary precision via lfuninit",
        "realprecision_digits": 20,
        "high_precision_crosscheck": "A separate realprecision=30 run through N=1000 produced the same displayed partial sums; its max residual was 5.51057192390154456003139059199e-35.",
        "requested_mpmath": "mpmath was unavailable in the supplied python3 environment and package installation was blocked by DNS/network sandboxing; this fallback is recorded rather than hidden.",
    },
    "convention": {
        "natural_sum": "two-sided over rho=1/2+i*gamma with gamma positive and negative",
        "term": "1/((1/4+gamma^2)*|zeta_prime(rho)|^2)",
        "conjugacy": "negative ordinates contribute the same term, so the two-sided sum is twice the positive-ordinate sum",
        "reported_partial_sums": "positive and two-sided",
    },
    "N_values_requested": [100, 300, 1000, 3000, 10000],
    "N_values_used": [100, 300, 1000, 3000],
    "uncompleted_extension": {"N": 10000, "attempted": True, "completed": False, "reason": "Repeated bounded PARI/GP runs did not finish the high-ordinate extension in the available runtime; no unobserved N=10000 value is reported or inferred."},
    "partial_sums": {str(n): row for n, row in positive.items()},
    "chunk_receipts": {
        "1-1000": {"positive_sum": positive[1000]["sum_decimal"], "max_abs_zeta_residual": "2.0877261576520969455e-18"},
        "1001-2000": {"positive_sum": "2.6534999055519456767e-5", "max_abs_zeta_residual": "2.4389167939889694249e-18"},
        "2001-3000": {"positive_sum": "9.3886382343934035441e-6", "max_abs_zeta_residual": "5.2370020942838978552e-17"},
    },
    "refined_zero_sanity": {"used_zero_count": 3000, "max_abs_zeta_residual": "5.2370020942838978552e-17", "strict_threshold": "1e-15", "failure_count": 0, "first_failure_index": 0, "pass": True},
    "derivative_block_statistics": blocks,
    "tail_model": {
        "density_model": "dN/dt ~= log(t/(2*pi))/(2*pi)",
        "integral": "B*(log(T/(2*pi))+1)/(2*pi*T), with B the observed block mean of 1/|zeta_prime|^2",
        "central_tail_N3000_one_sided": central_tail_3000,
        "conservative_tail_N3000_one_sided": conservative_tail_3000,
        "high_block_envelope_mean_inverse_derivative_sq": high_b_envelope,
        "observed_N1000_to_N3000_one_sided_increment": observed_increment,
        "central_tail_N1000_one_sided_for_consistency_check": tail_1000,
        "consistency_ratio_observed_increment_over_N1000_tail": observed_increment / tail_1000,
        "interpretation": "This is a numerical average-growth envelope, not a rigorous theorem-level bound on unusually small zeta derivatives.",
    },
    "final_estimate": {
        "positive_sum_with_central_tail": s3000 + central_tail_3000,
        "two_sided_S": final_s,
        "two_sided_error_bar": error_bar,
        "two_sided_interval_from_conservative_tail": [2.0 * s3000, 2.0 * (s3000 + conservative_tail_3000)],
        "precision_claim": "Finite sums have more backend digits, but the source seed precision, convention audit, and heuristic tail support only about 3 significant digits for the infinite sum.",
    },
    "E5_reproduction": {
        "script": "projects/mimo-mini-project/code/E5_zeta_zero_sum.py",
        "source_convention": "one-sided positive zeros n=1..N; no conjugate term; |rho|^2=1/4+gamma^2",
        "N": 100,
        "reproduced_positive_sum": positive[100]["sum_decimal"],
        "E5_reported_display_value": 0.0141436361,
        "display_match": True,
        "absolute_difference_from_display_value": abs(positive[100]["positive_sum"] - 0.0141436361),
        "two_sided_value_at_N100": positive[100]["two_sided_sum"],
        "convention_factor": 2.0,
        "note": "E5 itself could not be imported because mpmath is absent; the formula was independently reproduced with PARI/GP and matches its reported 10-decimal value.",
    },
    "simple_form_candidates": candidates,
    "source_line_refs": {"log.md": "13", "FIVE_DISCOVERIES.md": "25-49", "E5_zeta_zero_sum.py": "4-17, 23, 26-40, 60-63", "SELBERG_INPUT_DISPROVED.md": "27-31"},
}

OUT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt["final_estimate"], indent=2))
