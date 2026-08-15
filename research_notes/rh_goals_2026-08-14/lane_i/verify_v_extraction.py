#!/usr/bin/env python3
"""Exact step-1 audit for the frozen Kloosterman-gate inputs.

This is deliberately fail-closed.  The frozen inputs define two different
observables: an endpoint-inclusive integral observable and an older discrete
four-term observable.  The script verifies both source formulas, computes the
only source-backed centered residue-permutation candidate, and records that no
common A/B/C/N decomposition or Kloosterman completion is defined by the
named frozen files.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import sys
from fractions import Fraction
from math import gcd, isqrt
from pathlib import Path
from typing import Any


sys.set_int_max_str_digits(1_000_000)


ROOT = Path(__file__).resolve().parents[3]
PRIME_SRC = ROOT / "projects/prime-step-breakthrough/src"
KILL_TEST_PATH = ROOT / "equispaced-primes/papers/nw-mertens-note/integral_farey_kill_test.py"
PROTOCOL_PATH = KILL_TEST_PATH.with_name(
    "INTEGRAL_FAREY_KILL_TEST_PROTOCOL_2026-07-19.md"
)
RESEARCH_SPEC_PATH = ROOT / "projects/prime-step-breakthrough/RESEARCH_SPEC.md"
KERNEL_PATH = PRIME_SRC / "coprimebatch/kernel.py"
TEX_PATH = ROOT / "equispaced-primes/papers/sign-theorem/main.tex"

sys.path.insert(0, str(PRIME_SRC))
from coprimebatch.kernel import prime_energy_delta, step_summatory  # noqa: E402


def _load_kill_test() -> Any:
    spec = importlib.util.spec_from_file_location("frozen_kill_test", KILL_TEST_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {KILL_TEST_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


KILL_TEST = _load_kill_test()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def rational(value: Fraction) -> dict[str, str]:
    return {"numerator": str(value.numerator), "denominator": str(value.denominator)}


def decimal(value: Fraction, digits: int = 18) -> str:
    return KILL_TEST.decimal_string(value, digits)


def sign(value: Fraction) -> int:
    return (value > 0) - (value < 0)


def arithmetic_data(limit: int) -> tuple[list[int], list[int], list[int]]:
    return KILL_TEST.arithmetic_sieves(limit)


def phi_and_step_numerators(spf: list[int]) -> tuple[list[int], list[int]]:
    phi = list(range(len(spf)))
    step_num = [1] * len(spf)
    if len(spf) > 1:
        phi[1] = 1
    for n in range(2, len(spf)):
        q = spf[n]
        quotient = n // q
        phi[n] = phi[quotient] * q if quotient % q == 0 else phi[quotient] * (q - 1)
        step_num[n] = step_num[quotient] if quotient % q == 0 else step_num[quotient] * (1 - q)
    return phi, step_num


def dedekind_sum(h: int, k: int, cache: dict[tuple[int, int], Fraction]) -> Fraction:
    """Exact s(h,k)=sum ((r/k))((hr/k)) by reciprocity."""
    if k == 1:
        return Fraction(0)
    h %= k
    if h == 0:
        return Fraction(0)
    key = (h, k)
    if key in cache:
        return cache[key]
    value = (
        -Fraction(1, 4)
        + Fraction(h, 12 * k)
        + Fraction(k, 12 * h)
        + Fraction(1, 12 * h * k)
        - dedekind_sum(k, h, cache)
    )
    cache[key] = value
    return value


def source_backed_variance(
    p: int,
    mu: list[int],
    prefix_mobius: list[int],
    phi: list[int],
    direct_limit: int = 13,
) -> dict[str, Any]:
    """Compute the centered T_b fluctuation in two exact divisor forms."""
    limit = p - 1
    cache: dict[tuple[int, int], Fraction] = {}
    dedekind = [dedekind_sum(p, c, cache) for c in range(1, p)]

    # V = sum_b sum_{c|b} mu(b/c) s(p,c), with the original b outer loop.
    by_b = Fraction(0)
    for b in range(2, limit + 1):
        by_b += sum(
            (mu[b // c] * dedekind[c - 1] for c in range(1, b + 1) if b % c == 0),
            Fraction(0),
        )

    # The same sum after swapping b=c*d: sum_c s(p,c) M(floor(limit/c)).
    swapped = sum(
        (dedekind[c - 1] * prefix_mobius[limit // c] for c in range(1, p)),
        Fraction(0),
    )

    direct: Fraction | None = None
    if p <= direct_limit:
        direct = Fraction(0)
        for b in range(2, p):
            residues = [a for a in range(1, b) if gcd(a, b) == 1]
            t_b = sum(a * ((p * a) % b) for a in residues)
            direct += Fraction(t_b, b * b) - Fraction(len(residues), 4)

    result: dict[str, Any] = {
        "definition": (
            "V_residue(p)=sum_{2<=b<p} [ b^-2 sum_{1<=a<b,(a,b)=1} "
            "a*(p*a mod b) - phi(b)/4 ]"
        ),
        "dedekind_definition": "s(h,k)=sum_{1<=r<k} ((r/k))*((h*r/k))",
        "by_b": rational(by_b),
        "swapped": rational(swapped),
        "by_b_minus_swapped": rational(by_b - swapped),
        "decimal": decimal(by_b),
        "numerator_digits": len(str(abs(by_b.numerator))),
        "denominator_digits": len(str(by_b.denominator)),
        "direct_residue": None if direct is None else rational(direct),
        "direct_minus_by_b": None if direct is None else rational(direct - by_b),
        "dedekind_cache_size": len(cache),
        "source_convolution": (
            "T_b(p)-b^2*phi(b)/4 = b^2*sum_{c|b} mu(b/c)*s(p,c)"
        ),
    }
    return result


def historical_four_term_at_13(p: int = 13) -> dict[str, Any]:
    """Verify the available discrete four-term formula only at its small case."""
    if p != 13:
        raise ValueError("the bounded direct Farey witness is frozen at p=13")
    values = {(0, 1), (1, 1)}
    values.update(
        (a, b)
        for b in range(2, p + 1)
        for a in range(1, b)
        if gcd(a, b) == 1
    )
    old = sorted((value for value in values if value[1] <= p - 1), key=lambda x: Fraction(*x))
    new = sorted(values, key=lambda x: Fraction(*x))
    n = len(old)
    n_prime = len(new)
    old_rank = {value: index for index, value in enumerate(old)}
    new_rank = {value: index for index, value in enumerate(new)}
    d_old = {
        value: Fraction(old_rank[value]) - n * Fraction(*value) for value in old
    }
    d_new = {
        value: Fraction(new_rank[value]) - n_prime * Fraction(*value) for value in new
    }
    shifts = {
        value: Fraction(value[0] - (p * value[0]) % value[1], value[1])
        for value in old
        if value != (1, 1)
    }
    dilution = (Fraction(1, n * n) - Fraction(1, n_prime * n_prime)) * sum(
        (value * value for value in d_old.values()), Fraction(0)
    )
    cross = Fraction(2, n_prime * n_prime) * sum(
        (d_old[value] * shifts[value] for value in shifts), Fraction(0)
    )
    shift_squared = Fraction(1, n_prime * n_prime) * sum(
        (value * value for value in shifts.values()), Fraction(0)
    )
    new_fraction = Fraction(1, n_prime * n_prime) * sum(
        (d_new[(k, p)] * d_new[(k, p)] for k in range(1, p)), Fraction(0)
    )
    old_discrete = sum((value * value for value in d_old.values()), Fraction(0)) / (n * n)
    new_discrete = sum((value * value for value in d_new.values()), Fraction(0)) / (
        n_prime * n_prime
    )
    identity_error = dilution - cross - shift_squared - new_fraction - (
        old_discrete - new_discrete
    )
    return {
        "observable": "historical discrete Franel-Landau sum, not integral W",
        "n_old": n,
        "n_new": n_prime,
        "A_dilution": rational(dilution),
        "B_cross": rational(cross),
        "C_shift_squared": rational(shift_squared),
        "N_new_fraction": rational(new_fraction),
        "N_plus_B_plus_C_minus_A": rational(new_fraction + cross + shift_squared - dilution),
        "discrete_delta": rational(old_discrete - new_discrete),
        "identity_error": rational(identity_error),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).with_name("v_extraction_receipt.json"),
    )
    args = parser.parse_args()
    probes = (13, 8501, 92173)
    max_probe = max(probes)
    spf, mu, mertens = arithmetic_data(max_probe)
    phi, step_nums = phi_and_step_numerators(spf)
    prefix_mobius = [0] * (max_probe + 1)
    for n in range(1, max_probe + 1):
        prefix_mobius[n] = prefix_mobius[n - 1] + mu[n]

    records: dict[str, Any] = {}
    for p in probes:
        a_value = step_summatory(p - 1)
        prefactor = Fraction(p - 1, 6 * p)
        integral_delta = KILL_TEST.delta_from_A(p, a_value)
        interior_delta = prime_energy_delta(p)
        endpoint_correction = integral_delta + interior_delta
        phi_sum = sum(phi[2:p])
        n_old_interior = phi_sum
        n_prime_endpoint = phi_sum + p + 1
        a_minus_one = a_value - 1
        candidate_v = source_backed_variance(
            p, mu, prefix_mobius, phi, direct_limit=13
        )
        candidate_v_fraction = Fraction(
            int(candidate_v["by_b"]["numerator"]),
            int(candidate_v["by_b"]["denominator"]),
        )
        c_raw = (
            Fraction(phi_sum, 6)
            + a_minus_one / 3
            - 2 * candidate_v_fraction
        )
        records[str(p)] = {
            "p": p,
            "mu_p": mu[p],
            "mertens_p": mertens[p],
            "interior_count_H": phi_sum,
            "n_old_endpoint_inclusive": phi_sum + 2,
            "n_new_endpoint_inclusive": n_prime_endpoint,
            "A_driver": rational(a_value),
            "A_driver_minus_1": rational(a_minus_one),
            "prime_prefactor": rational(prefactor),
            "integral_DeltaW": {
                "exact": rational(integral_delta),
                "decimal": decimal(integral_delta),
                "sign": sign(integral_delta),
            },
            "interior_kernel_step": {
                "exact": rational(interior_delta),
                "decimal": decimal(interior_delta),
                "sign": sign(interior_delta),
            },
            "endpoint_bookkeeping": {
                "integral_plus_interior_minus_prefactor": rational(
                    endpoint_correction - prefactor
                ),
                "endpoint_cross_term": rational(-prefactor),
            },
            "candidate_V": candidate_v,
            "candidate_C_raw": rational(c_raw),
            "candidate_C_normalized_by_n_prime_squared": rational(
                c_raw / (n_prime_endpoint * n_prime_endpoint)
            ),
            "gate_ABCN_status": (
                "undefined_for_endpoint_integral_observable; only the p=13 "
                "historical-discrete witness is computed below"
            ),
        }

    receipt: dict[str, Any] = {
        "schema_version": 1,
        "protocol_step": "1 only",
        "status": "SOURCE_MISMATCH_BLOCKS_UNIQUE_V_EXTRACTION",
        "go_no_go": "not assessed",
        "scope_boundary": {
            "step_2_completion": "not run",
            "step_3_exponent_comparison": "not run",
            "proof_attempt": "not run",
            "GO_NO_GO": "not concluded",
        },
        "source_findings": {
            "research_spec_ABCN": "absent",
            "research_spec_observable": "interior R_(p-1) and primitive-layer Gram energy",
            "integral_protocol_observable": "endpoint-inclusive integral count discrepancy",
            "historical_four_term_observable": "normalized discrete Franel-Landau sum",
            "common_decomposition": False,
            "source_backed_V_candidate": "V_residue / centered T_b fluctuation",
            "source_backed_kloosterman_completion": False,
            "reason": (
                "The frozen paper explicitly identifies the fluctuation as a "
                "Dedekind-sum convolution and says the direct Kloosterman "
                "formulation is invalid."
            ),
        },
        "source_sha256": {
            str(RESEARCH_SPEC_PATH.relative_to(ROOT)): sha256(RESEARCH_SPEC_PATH),
            str(PROTOCOL_PATH.relative_to(ROOT)): sha256(PROTOCOL_PATH),
            str(KILL_TEST_PATH.relative_to(ROOT)): sha256(KILL_TEST_PATH),
            str(KERNEL_PATH.relative_to(ROOT)): sha256(KERNEL_PATH),
            str(TEX_PATH.relative_to(ROOT)): sha256(TEX_PATH),
        },
        "probes": records,
        "historical_discrete_four_term_p13": historical_four_term_at_13(),
        "exact_zero_error_checks": {
            "endpoint_bookkeeping_all_probes": all(
                records[str(p)]["endpoint_bookkeeping"][
                    "integral_plus_interior_minus_prefactor"
                ]
                == {"numerator": "0", "denominator": "1"}
                for p in probes
            ),
            "candidate_V_divisor_reindexing_all_probes": all(
                records[str(p)]["candidate_V"]["by_b_minus_swapped"]
                == {"numerator": "0", "denominator": "1"}
                for p in probes
            ),
            "candidate_V_direct_residue_p13": records["13"]["candidate_V"][
                "direct_minus_by_b"
            ]
            == {"numerator": "0", "denominator": "1"},
            "candidate_C_identity_all_probes": all(
                Fraction(
                    int(records[str(p)]["candidate_C_raw"]["numerator"]),
                    int(records[str(p)]["candidate_C_raw"]["denominator"]),
                )
                == Fraction(
                    records[str(p)]["interior_count_H"], 6
                )
                + Fraction(
                    int(records[str(p)]["A_driver_minus_1"]["numerator"]),
                    int(records[str(p)]["A_driver_minus_1"]["denominator"]),
                )
                / 3
                - 2
                * Fraction(
                    int(records[str(p)]["candidate_V"]["by_b"]["numerator"]),
                    int(records[str(p)]["candidate_V"]["by_b"]["denominator"]),
                )
                for p in probes
            ),
            "historical_discrete_four_term_p13": False,
        },
    }
    # Replace the placeholder without using a self-reference in the literal.
    receipt["exact_zero_error_checks"]["historical_discrete_four_term_p13"] = (
        receipt["historical_discrete_four_term_p13"]["identity_error"]
        == {"numerator": "0", "denominator": "1"}
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "status": receipt["status"],
        "output": str(args.output),
        "probes": list(probes),
        "zero_error_checks": receipt["exact_zero_error_checks"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
