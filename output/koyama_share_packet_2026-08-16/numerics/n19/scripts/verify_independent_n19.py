#!/usr/bin/env python3
"""Mechanical gates for the independent q=19 certificate and K=100 audit."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

from flint import acb, arb, ctx, dirichlet_char, fmpq


EXPECTED_CURVE_SHA256 = "57957bdb3ce3243272c3d4b8e9ffe7dfb734b759f48b63becf7ae6f924e1caab"


def digest(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            result.update(block)
    return result.hexdigest()


def rows(path: Path) -> list[dict[str, str]]:
    with path.open() as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def number(text: str) -> float:
    return float(text.replace(" ", ""))


def exact_arb(value: Fraction) -> arb:
    return arb(fmpq(value.numerator, value.denominator))


def verify(curve: Path, output: Path) -> None:
    assert digest(curve) == EXPECTED_CURVE_SHA256, "authoritative curve hash changed"
    certificate = json.loads((output / "n19_arb_certificate.json").read_text())
    assert certificate["curve_sha256"] == EXPECTED_CURVE_SHA256

    assert certificate["character"] == {
        "modulus": 19,
        "conrey_m": 13,
        "conductor": 19,
        "order": 18,
        "parity": 1,
        "primitive": True,
        "real_character": False,
        "principal": False,
        "chi_minus_one_exponent_mod_18": 9,
        "chi_minus_one": "-1",
    }, "character convention/metadata changed"
    phase_rows = certificate["phase_table"]
    assert len(phase_rows) == 18 and [row["a"] for row in phase_rows] == list(range(1, 19))

    root = certificate["root_bracket"]
    left = Fraction(int(root["left_numerator"]), int(root["left_denominator"]))
    right = Fraction(int(root["right_numerator"]), int(root["right_denominator"]))
    assert 0 < right - left < Fraction(1, 10**80), "root bracket is not narrower than 1e-80"
    assert right < Fraction("0.019") < Fraction("1.74")

    ctx.prec = 384
    chi = dirichlet_char(19, 13)
    left_z = chi.hardy_z(exact_arb(left)).real
    right_z = chi.hardy_z(exact_arb(right)).real
    assert left_z > arb(0) and right_z < arb(0), "Arb endpoint signs do not certify a zero"
    midpoint = (left + right) / 2
    midpoint_l = chi.l_function(acb(exact_arb(Fraction(1, 2)), exact_arb(midpoint)))
    assert abs(midpoint_l).abs_upper() < arb("1e-80"), "midpoint L residual is too large"

    mode = certificate["mode_contribution"]
    assert mode["n_top_decade_points"] == 53
    assert abs(float(mode["rms_top_decade"]) - 6.719327033349822) < 1e-12
    assert abs(float(mode["correlation_with_observed_centered"]) - 0.727600207814535) < 1e-12
    assert float(mode["top_decade_phase_excursion_radians"]) < 0.05

    zero_checks: list[dict[str, str]] = []
    zero_counts: dict[int, int] = {}
    pari_first: Fraction | None = None
    with (output / "pari_n19_100_zeros.tsv").open() as stream:
        for raw in stream:
            if raw.startswith("#") or not raw.strip():
                continue
            fields = raw.rstrip("\n").split("\t")
            if fields[0] == "CHECK":
                _, q, m, count_a, count_b, maxdiff, maxresidual, status = fields
                zero_checks.append(
                    {
                        "q": q,
                        "m": m,
                        "count_a": count_a,
                        "count_b": count_b,
                        "maxdiff": maxdiff,
                        "maxresidual": maxresidual,
                        "status": status,
                    }
                )
            elif fields[0] == "ZERO":
                _, q, m, index, gamma = fields
                assert q == "19"
                zero_counts[int(m)] = zero_counts.get(int(m), 0) + 1
                if m == "13" and index == "1":
                    pari_first = Fraction(gamma.replace(" ", ""))
    assert len(zero_checks) == 17, f"expected 17 deep zero checks, got {len(zero_checks)}"
    assert all(row["status"] == "PASS" for row in zero_checks), "a deep zero check failed"
    assert all(int(row["count_a"]) == int(row["count_b"]) >= 100 for row in zero_checks)
    assert max(number(row["maxdiff"]) for row in zero_checks) < 1e-28
    assert max(number(row["maxresidual"]) for row in zero_checks) < 1e-28
    assert len(zero_counts) == 17 and min(zero_counts.values()) >= 100
    # The GP file is printed at 38-digit precision, much wider than the Arb
    # bracket.  Compare at the precision actually carried by that file.
    assert pari_first is not None and abs(pari_first - midpoint) < Fraction(1, 10**38), (
        "PARI first zero disagrees with the Arb midpoint at GP output precision"
    )

    reconstruction = rows(output / "n19_deep_reconstruction.tsv")
    assert len(reconstruction) == 438 * 9
    for row in reconstruction:
        assert int(row["q"]) == 19
        for key in ("E_observed", "E_K25", "E_K50", "E_K100"):
            assert math.isfinite(float(row[key]))

    metrics = rows(output / "n19_deep_metrics.tsv")
    assert len(metrics) == 9 * 3
    assert {(int(row["a"]), int(row["K_zeros_per_character"])) for row in metrics} == {
        (a, k) for a in (2, 3, 8, 10, 12, 13, 14, 15, 18) for k in (25, 50, 100)
    }
    assert all(int(row["n_points"]) == 53 for row in metrics)
    minus_one = {int(row["K_zeros_per_character"]): row for row in metrics if int(row["a"]) == 18}
    assert [float(minus_one[k]["correlation"]) for k in (25, 50, 100)] == sorted(
        float(minus_one[k]["correlation"]) for k in (25, 50, 100)
    )
    assert float(minus_one[100]["correlation"]) > 0.99
    assert float(minus_one[100]["rmse"]) < float(minus_one[50]["rmse"]) < float(minus_one[25]["rmse"])

    stability = rows(output / "n19_deep_stability.tsv")
    assert len(stability) == 9 * 3
    assert all(math.isfinite(float(row["rms_difference"])) for row in stability)
    minus_one_stability = {
        (int(row["K_low"]), int(row["K_high"])): row
        for row in stability
        if int(row["a"]) == 18
    }
    assert float(minus_one_stability[(50, 100)]["rms_difference"]) < float(
        minus_one_stability[(25, 50)]["rms_difference"]
    )

    rank_summary = rows(output / "n19_deep_rank_summary.tsv")
    assert len(rank_summary) == 4
    observed = next(row for row in rank_summary if row["source"] == "observed")
    assert int(observed["rank_changes"]) == 17 and int(observed["leader_changes"]) == 8
    spectral = {int(row["K_zeros_per_character"]): row for row in rank_summary if row["source"] == "spectral"}
    assert set(spectral) == {25, 50, 100}
    assert all(int(row["rank_changes"]) > 0 and int(row["leader_changes"]) > 0 for row in spectral.values())
    assert int(spectral[100]["rank_changes"]) == 14
    assert int(spectral[100]["leader_changes"]) == 7
    assert float(spectral[100]["rank_agreement_with_observed"]) > 0.90
    assert float(spectral[100]["leader_agreement_with_observed"]) > 0.98

    print("INDEPENDENT N19 VERIFY PASS")
    print("arb_sign_bracket=PASS width<1e-80 midpoint_abs_L<1e-80")
    print("character=mod19 Conrey13 conductor19 order18 odd chi(-1)=-1")
    print("deep_zero_checks=17/17 PASS; minimum_count>=100")
    print("deep_reconstruction_rows=3942 metrics=27 stability=27")
    print("K100_minus1_correlation>0.99; rank_changes=14; leader_changes=7")


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: verify_independent_n19.py CURVE OUTPUT_DIR")
    verify(Path(sys.argv[1]), Path(sys.argv[2]))


if __name__ == "__main__":
    main()
