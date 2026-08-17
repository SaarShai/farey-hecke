#!/usr/bin/env python3
"""Independent Arb/FLINT corroboration of the exceptional q=19 zero.

This program does not call PARI/GP.  It constructs the Conrey character
directly with python-flint, brackets a sign change of its real Hardy Z
function using exact rational ordinates and Arb ball evaluation, and
independently recomputes the one-mode statistics against the source curve.

The sign change proves existence of at least one zero in the bracket by
continuity.  It does not prove uniqueness or completeness of all lower zeros.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from fractions import Fraction
from pathlib import Path

import mpmath as mp
from flint import acb, arb, ctx, dirichlet_char, fmpq


Q = 19
CONREY_M = 13
CHARACTER_ORDER = 18
ARBITRARY_PRECISION_BITS = 384
BISECTION_STEPS = 220
TOP_DECADE_LOWER = 30_000_000_000_000


def digest(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            result.update(block)
    return result.hexdigest()


def to_arb(value: Fraction) -> arb:
    return arb(fmpq(value.numerator, value.denominator))


def hardy_z_real(chi: dirichlet_char, ordinate: Fraction) -> arb:
    value = chi.hardy_z(to_arb(ordinate))
    assert value.imag.contains(0), "Hardy Z lost its real-axis invariant"
    return value.real


def sign(value: arb) -> int:
    if value > arb(0):
        return 1
    if value < arb(0):
        return -1
    return 0


def bisect_sign_change(
    chi: dirichlet_char, left: Fraction, right: Fraction, steps: int
) -> tuple[Fraction, Fraction, arb, arb]:
    left_value = hardy_z_real(chi, left)
    right_value = hardy_z_real(chi, right)
    left_sign = sign(left_value)
    right_sign = sign(right_value)
    if left_sign == 0 or right_sign == 0 or left_sign == right_sign:
        raise ValueError("initial bracket does not have sign-definite opposite endpoints")

    for _ in range(steps):
        midpoint = (left + right) / 2
        midpoint_value = hardy_z_real(chi, midpoint)
        midpoint_sign = sign(midpoint_value)
        if midpoint_sign == 0:
            raise ArithmeticError("Arb could not determine the midpoint sign")
        if midpoint_sign == left_sign:
            left, left_value = midpoint, midpoint_value
        else:
            right, right_value = midpoint, midpoint_value
    return left, right, left_value, right_value


def decimal_text(value: Fraction, digits: int = 100) -> str:
    mp.mp.dps = digits + 10
    return mp.nstr(mp.mpf(value.numerator) / value.denominator, digits)


def discrete_log_table(generator: int, modulus: int) -> dict[int, int]:
    result: dict[int, int] = {}
    value = 1
    for exponent in range(modulus - 1):
        if value in result:
            raise ValueError("generator does not span the full unit group")
        result[value] = exponent
        value = value * generator % modulus
    if len(result) != modulus - 1:
        raise ValueError("incomplete discrete-log table")
    return result


def verify_character_convention(chi: dirichlet_char) -> list[dict[str, int]]:
    # For prime 19, 2 is a primitive root and 13 = 2^5.  The Conrey
    # convention therefore gives exponent 5*log_2(a) modulo 18.
    logs = discrete_log_table(2, Q)
    conrey_log = logs[CONREY_M]
    assert conrey_log == 5
    rows: list[dict[str, int]] = []
    for a in range(1, Q):
        expected = conrey_log * logs[a] % CHARACTER_ORDER
        actual = int(chi.chi_exponent(a))
        if actual != expected:
            raise AssertionError(
                f"Conrey phase mismatch at a={a}: FLINT={actual}, derived={expected}"
            )
        rows.append({"a": a, "exponent_mod_18": actual})
    return rows


def parse_curve(path: Path) -> dict[int, dict[int, int]]:
    curve: dict[int, dict[int, int]] = {}
    with path.open() as stream:
        for raw in stream:
            if raw.startswith("#") or raw.startswith("TOTAL"):
                continue
            fields = raw.rstrip("\n").split("\t")
            if len(fields) != 4:
                continue
            q, x, a, count = map(int, fields)
            if q == Q:
                curve.setdefault(x, {})[a] = count
    if len(curve) != 438:
        raise ValueError(f"expected 438 q=19 abscissae, got {len(curve)}")
    return curve


def pearson(left: list[mp.mpf], right: list[mp.mpf]) -> mp.mpf:
    mean_left = mp.fsum(left) / len(left)
    mean_right = mp.fsum(right) / len(right)
    centered_left = [value - mean_left for value in left]
    centered_right = [value - mean_right for value in right]
    numerator = mp.fsum(a * b for a, b in zip(centered_left, centered_right))
    denominator = mp.sqrt(
        mp.fsum(value * value for value in centered_left)
        * mp.fsum(value * value for value in centered_right)
    )
    return numerator / denominator


def mode_statistics(curve_path: Path, gamma: Fraction) -> dict[str, str | int]:
    mp.mp.dps = 100
    gamma_mp = mp.mpf(gamma.numerator) / gamma.denominator
    curve = parse_curve(curve_path)
    xs = [x for x in sorted(curve) if x >= TOP_DECADE_LOWER]
    observed: list[mp.mpf] = []
    contribution: list[mp.mpf] = []
    rho = mp.mpf("0.5") + 1j * gamma_mp
    for x in xs:
        log_x = mp.log(x)
        observed.append(
            18 * log_x / mp.sqrt(x) * (curve[x][18] - curve[x][1])
        )
        # chi(-1)=-1, hence conjugate(chi(-1))-1 = -2 exactly.
        contribution.append(-2 * mp.re(-2 * mp.exp(1j * gamma_mp * log_x) / rho))

    centered_observed = [value - mp.fsum(observed) / len(observed) for value in observed]
    rms = mp.sqrt(mp.fsum(value * value for value in contribution) / len(contribution))
    phase_excursion = gamma_mp * mp.log(mp.mpf(xs[-1]) / xs[0])
    return {
        "n_top_decade_points": len(xs),
        "rms_top_decade": mp.nstr(rms, 30),
        "correlation_with_observed_centered": mp.nstr(
            pearson(centered_observed, contribution), 30
        ),
        "endpoint_contribution": mp.nstr(contribution[-1], 30),
        "maximum_absolute_amplitude": mp.nstr(
            4 / mp.sqrt(mp.mpf("0.25") + gamma_mp * gamma_mp), 30
        ),
        "log_x_period": mp.nstr(2 * mp.pi / gamma_mp, 30),
        "top_decade_phase_excursion_radians": mp.nstr(phase_excursion, 30),
    }


def first_pari_gamma(path: Path) -> Fraction:
    with path.open() as stream:
        for raw in stream:
            fields = raw.rstrip("\n").split("\t")
            if (
                len(fields) == 5
                and fields[0] == "ZERO"
                and fields[1:4] == ["19", "13", "1"]
            ):
                return Fraction(fields[4].replace(" ", ""))
    raise ValueError("missing PARI q=19, m=13, first zero")


def build_certificate(curve_path: Path, pari_path: Path | None) -> dict[str, object]:
    ctx.prec = ARBITRARY_PRECISION_BITS
    chi = dirichlet_char(Q, CONREY_M)

    metadata = {
        "modulus": int(chi.modulus()),
        "conrey_m": int(chi.number()),
        "conductor": int(chi.conductor()),
        "order": int(chi.order()),
        "parity": int(chi.parity()),
        "primitive": bool(chi.is_primitive()),
        "real_character": bool(chi.is_real()),
        "principal": bool(chi.is_principal()),
        "chi_minus_one_exponent_mod_18": int(chi.chi_exponent(-1)),
        "chi_minus_one": "-1",
    }
    expected_metadata = {
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
    }
    if metadata != expected_metadata:
        raise AssertionError(f"unexpected character metadata: {metadata}")
    phase_table = verify_character_convention(chi)

    left, right, left_z, right_z = bisect_sign_change(
        chi,
        Fraction("0.01895639908022614"),
        Fraction("0.01895639908022615"),
        BISECTION_STEPS,
    )
    midpoint = (left + right) / 2
    midpoint_l = chi.l_function(acb(to_arb(Fraction(1, 2)), to_arb(midpoint)))
    midpoint_l_abs = abs(midpoint_l)
    if not midpoint_l_abs.abs_upper() < arb("1e-80"):
        raise AssertionError(f"unexpectedly large midpoint residual: {midpoint_l_abs}")

    comparison: dict[str, str] | None = None
    if pari_path is not None:
        pari_gamma = first_pari_gamma(pari_path)
        difference = abs(midpoint - pari_gamma)
        comparison = {
            "pari_gamma": decimal_text(pari_gamma, 50),
            "absolute_difference": decimal_text(difference, 40),
        }

    return {
        "method": {
            "library": "python-flint 0.9.0 / Arb ball arithmetic",
            "precision_bits": ARBITRARY_PRECISION_BITS,
            "bisection_steps": BISECTION_STEPS,
            "independent_of_pari_for_root_search": True,
            "claim": "existence of at least one critical-line zero in bracket by sign change",
            "not_claimed": ["uniqueness in bracket", "completeness below bracket", "GRH"],
        },
        "character": metadata,
        "phase_table": phase_table,
        "root_bracket": {
            "left_numerator": str(left.numerator),
            "left_denominator": str(left.denominator),
            "right_numerator": str(right.numerator),
            "right_denominator": str(right.denominator),
            "left_decimal": decimal_text(left),
            "right_decimal": decimal_text(right),
            "width": decimal_text(right - left, 30),
            "left_hardy_z": left_z.str(40),
            "right_hardy_z": right_z.str(40),
            "left_sign": sign(left_z),
            "right_sign": sign(right_z),
            "midpoint_decimal": decimal_text(midpoint),
            "midpoint_l_value": midpoint_l.str(40),
            "midpoint_l_abs_upper": midpoint_l_abs.abs_upper().str(40),
            "below_manuscript_1_74": right < Fraction("1.74"),
        },
        "pari_comparison_after_independent_search": comparison,
        "curve_sha256": digest(curve_path),
        "mode_contribution": mode_statistics(curve_path, midpoint),
    }


def write_report(path: Path, certificate: dict[str, object]) -> None:
    character = certificate["character"]
    root = certificate["root_bracket"]
    mode = certificate["mode_contribution"]
    comparison = certificate["pari_comparison_after_independent_search"]
    lines = [
        "# Independent q=19 low-zero certificate",
        "",
        "## Result",
        "",
        "Python FLINT/Arb, without using PARI for the root search, evaluates the real Hardy",
        "Z-function with sign-definite interval endpoints.  Continuity therefore proves that",
        "at least one critical-line zero lies in the displayed bracket.  The computation does",
        "not establish uniqueness, zero completeness below the bracket, or GRH.",
        "",
        "| field | certified/computed value |",
        "|---|---:|",
        f"| modulus / Conrey index | {character['modulus']} / {character['conrey_m']} |",
        f"| conductor / order | {character['conductor']} / {character['order']} |",
        f"| parity / chi(-1) | {character['parity']} / {character['chi_minus_one']} |",
        f"| left endpoint | `{root['left_decimal']}` |",
        f"| right endpoint | `{root['right_decimal']}` |",
        f"| bracket width | `{root['width']}` |",
        f"| Hardy Z endpoint signs | {root['left_sign']}, {root['right_sign']} |",
        f"| midpoint | `{root['midpoint_decimal']}` |",
        f"| Arb upper bound for abs L(midpoint) | `{root['midpoint_l_abs_upper']}` |",
        f"| top-decade one-mode RMS | {mode['rms_top_decade']} |",
        f"| correlation with centered observed E_19(x;18,1) | {mode['correlation_with_observed_centered']} |",
        f"| phase excursion over sampled top decade | {mode['top_decade_phase_excursion_radians']} radians |",
    ]
    if comparison:
        lines.extend(
            [
                f"| later comparison with PARI ordinate | `{comparison['pari_gamma']}` |",
                f"| absolute FLINT-PARI difference | `{comparison['absolute_difference']}` |",
            ]
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "This independently contradicts the manuscript's description of approximately",
            "1.74 as the lowest complex q=19 ordinate: a critical-line zero exists near",
            "0.018956399080226143.  Its very long log-x period and large top-decade RMS make it",
            "an active slow mode at the 300-trillion scale.  The calculation alone does not",
            "identify this zero as the globally lowest zero without an independent completeness",
            "argument; the safe claim is existence far below 1.74.",
            "",
        ]
    )
    path.write_text("\n".join(lines))


def write_tsv(path: Path, certificate: dict[str, object]) -> None:
    character = certificate["character"]
    root = certificate["root_bracket"]
    mode = certificate["mode_contribution"]
    rows = [
        ("modulus", character["modulus"]),
        ("conrey_m", character["conrey_m"]),
        ("conductor", character["conductor"]),
        ("order", character["order"]),
        ("parity", character["parity"]),
        ("chi_minus_one", character["chi_minus_one"]),
        ("root_left", root["left_decimal"]),
        ("root_right", root["right_decimal"]),
        ("root_width", root["width"]),
        ("left_hardy_z_sign", root["left_sign"]),
        ("right_hardy_z_sign", root["right_sign"]),
        ("midpoint_l_abs_upper", root["midpoint_l_abs_upper"]),
        ("top_decade_points", mode["n_top_decade_points"]),
        ("mode_rms_top_decade", mode["rms_top_decade"]),
        ("mode_correlation", mode["correlation_with_observed_centered"]),
        ("top_decade_phase_excursion_radians", mode["top_decade_phase_excursion_radians"]),
    ]
    with path.open("w", newline="") as stream:
        writer = csv.writer(stream, delimiter="\t")
        writer.writerow(["field", "value"])
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--curve", type=Path, required=True)
    parser.add_argument("--pari", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    certificate = build_certificate(args.curve, args.pari)
    (args.output_dir / "n19_arb_certificate.json").write_text(
        json.dumps(certificate, indent=2, sort_keys=True) + "\n"
    )
    write_report(args.output_dir / "N19_CERTIFICATE.md", certificate)
    write_tsv(args.output_dir / "n19_certificate.tsv", certificate)
    print("N19 ARB CERTIFICATE PASS")
    print(f"root_bracket={certificate['root_bracket']['left_decimal']}..{certificate['root_bracket']['right_decimal']}")
    print(f"bracket_width={certificate['root_bracket']['width']}")
    print(f"mode_rms_top_decade={certificate['mode_contribution']['rms_top_decade']}")
    print(f"mode_correlation={certificate['mode_contribution']['correlation_with_observed_centered']}")


if __name__ == "__main__":
    main()
