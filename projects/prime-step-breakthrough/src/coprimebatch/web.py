"""Dependency-free HTTP API and static-file server for CoprimeBatch Designer."""

from __future__ import annotations

import argparse
import json
import mimetypes
import re
import socket
import threading
import time
from dataclasses import asdict, is_dataclass
from fractions import Fraction
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from math import comb, gcd, isfinite, isqrt
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import urlparse

from . import gap_permutation, kernel, optimizer, shear
from .applications import application_preset_payload
from .prefix_balance import (
    BalanceItem,
    BalanceProblem,
    CategoricalConstraintProblem,
    ConstrainedQuotaResult,
    FixedOccurrenceBlock,
    InfeasibleProblemError,
    OccurrencePrecedence,
    OccurrenceRef,
    OrderingResult,
    QuotaResult,
    quota_mechanical_order,
    quota_order,
    solve_constrained_quota,
    solve_constrained,
    solve_exact,
    verify_constrained_quota,
    verify_order,
    verify_quota_result,
)


ROOT = Path(__file__).resolve().parents[2] / "web"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8765
DEFAULT_START = 2
DEFAULT_STOP = 200
DEFAULT_LAYERS = 10
DEFAULT_SEED = 20260715
BALANCE_SCHEMA_VERSION = "prefix-balance-api-v1"
FULL_ORDER_ITEM_CAP = 10_000
FULL_ORDER_UTF8_CAP = 500_000
ORDER_PREVIEW_ITEMS = 8
BALANCE_ITEM_CAP = 5_000_000
BALANCE_CATEGORY_UTF8_CAP = 256
RATIONAL_TEXT_CAP = 1_024
RATIONAL_BIT_CAP = 4_096
BALANCE_JSON_INPUT_CAP = 1_000_000
CONSTRAINED_QUOTA_CATEGORY_CAP = 256
CONSTRAINED_QUOTA_EXACT_METRIC_CELL_CAP = 8_000_000
CONSTRAINED_QUOTA_CONSTRAINT_REFERENCE_CAP = 10_000
CONSTRAINED_QUOTA_BLOCK_WIDTH_CAP = 1_024

# Admission caps for the exact-arithmetic research endpoints.  Unlike the
# balance path these do super-linear exact work per request, so an uncapped
# magnitude is a single-request CPU/RAM denial of service even inside the 1 MB
# body cap.  Each cap bounds the worst-case request to a few seconds, matching
# the constrained-quota metric-cell tolerance.  Direct Python callers are not
# subject to these interface caps.
GAP_FAREY_ORDER_CAP = 512
GAP_SUPPLIED_COUNT_CAP = 20_000
# Exact supplied gaps can create a common denominator whose bit length grows
# with every distinct input denominator.  Counting entries or HTTP bytes alone
# therefore does not bound the big-integer work.  This proxy is evaluated on
# parsed, normalized rationals before the certificate entry point:
#
#   gap_bit_work = N * (sum(bitlen(unique denominators))
#                       + max(bitlen(numerator)))
#
# Repeated equal denominators remain cheap, while a compact body containing
# many pairwise-coprime large denominators is rejected.
GAP_SUPPLIED_EXACT_WORK_BIT_CAP = 8_000_000
# Certificate fields square cumulative residual denominators.  Bounding the
# actual common denominator to 5,000 bits keeps all derived exact integers,
# including squared-denominator quantities, comfortably JSON-serializable.
GAP_SUPPLIED_COMMON_DENOMINATOR_BIT_CAP = 5_000
SHIFT_PRIME_CAP = 512
SHIFT_MAX_ORDER_CAP = 12
OPTIMIZE_CANDIDATE_CAP = 64
OPTIMIZE_SAMPLE_CAP = 2_000
OPTIMIZE_BENCHMARK_SPAN_CAP = 512
OPTIMIZE_TRIAL_DIVISION_BUDGET = 5_000_000
OPTIMIZE_KERNEL_WORK_CELL_CAP = 1_000_000
CERTIFICATE_DENOMINATOR_COUNT_CAP = 256
CERTIFICATE_DENOMINATOR_BIT_CAP = 4_096
# Exact kernel output can contain a common denominator approaching the product
# of the distinct input prime powers.  Keep that aggregate comfortably below
# Python's default 4,300-decimal-digit integer-to-string safety limit so every
# admitted exact result remains JSON-serializable.
CERTIFICATE_OUTPUT_INTEGER_BIT_CAP = 12_000
CERTIFICATE_KERNEL_BIT_CELL_CAP = 10_000_000
# Bound on total trial-division work (sum of isqrt over every value that is
# factored by trial division, including supplied factor bases, which are
# primality-checked with the same O(sqrt n) routine before the product check).
CERTIFICATE_TRIAL_DIVISION_BUDGET = 50_000_000

# Per-connection socket read deadline and a global bound on concurrently
# handled connections.  Together they defend the loopback service against a
# slowloris-style thread/buffer exhaustion attack.
SOCKET_TIMEOUT_SECONDS = 15.0
MAX_CONCURRENT_CONNECTIONS = 64

LOOPBACK_HOSTS = frozenset({"127.0.0.1", "localhost", "::1"})
_RATIONAL_PATTERN = re.compile(r"[+-]?[0-9]+(?:/[0-9]+)?\Z")


class RequestError(ValueError):
    def __init__(self, message: str, status: HTTPStatus = HTTPStatus.BAD_REQUEST):
        super().__init__(message)
        self.status = status


def _unique_json_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise RequestError(f"duplicate JSON object key: {key!r}")
        result[key] = value
    return result


def _jsonable(value: Any) -> Any:
    if isinstance(value, Fraction):
        return {
            "fraction": str(value),
            "numerator": value.numerator,
            "denominator": value.denominator,
            "decimal": float(value),
        }
    if is_dataclass(value):
        return _jsonable(asdict(value))
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    if isinstance(value, Path):
        return str(value)
    return value


def _body(request: BaseHTTPRequestHandler) -> dict[str, Any]:
    try:
        length = int(request.headers.get("Content-Length", "0"))
    except ValueError as exc:
        raise RequestError("Content-Length must be an integer") from exc
    if length < 0:
        raise RequestError("Content-Length must not be negative")
    if length > BALANCE_JSON_INPUT_CAP:
        raise RequestError("request body is too large")
    raw = request.rfile.read(length)
    if not raw:
        return {}
    try:
        payload = json.loads(
            raw.decode("utf-8"), object_pairs_hook=_unique_json_object
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RequestError("request body must be valid UTF-8 JSON") from exc
    if not isinstance(payload, dict):
        raise RequestError("request body must be a JSON object")
    return payload


def _int(value: Any, name: str, minimum: int | None = None) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise RequestError(f"{name} must be an integer")
    if minimum is not None and value < minimum:
        raise RequestError(f"{name} must be at least {minimum}")
    return value


def _ints(value: Any, name: str, minimum: int | None = None) -> list[int]:
    if not isinstance(value, list) or not value:
        raise RequestError(f"{name} must be a non-empty JSON array")
    return [_int(item, name, minimum) for item in value]


def _exact(value: Any) -> bool:
    if value is None:
        return True
    if not isinstance(value, bool):
        raise RequestError("exact must be a boolean")
    return value


def _integer_key(value: Any, name: str) -> int:
    if isinstance(value, bool):
        raise RequestError(f"{name} keys must be integers")
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        text = value.strip()
        if text and (text.isdigit() or (text.startswith("-") and text[1:].isdigit())):
            return int(text)
    raise RequestError(f"{name} keys must be integers")


def _factorizations(value: Any) -> dict[int, dict[int, int]] | None:
    if value is None:
        return None
    if not isinstance(value, dict):
        raise RequestError("factorizations must be a JSON object")
    result: dict[int, dict[int, int]] = {}
    for denominator_key, supplied in value.items():
        denominator = _integer_key(denominator_key, "factorization denominator")
        if denominator in result:
            raise RequestError("factorization denominator keys collide")
        if not isinstance(supplied, dict):
            raise RequestError("each factorization must be a JSON object")
        factors: dict[int, int] = {}
        for prime_key, exponent in supplied.items():
            prime = _integer_key(prime_key, "factor")
            if prime in factors:
                raise RequestError("factor keys collide")
            factors[prime] = _int(exponent, "factor exponent", 1)
        result[denominator] = factors
    return result


def _enforce_certificate_limits(
    denominators: list[int],
    factorizations: Mapping[int, Mapping[int, int]] | None,
) -> None:
    """Bound the exact trial-division and Gram work of a portfolio request."""

    if len(denominators) > CERTIFICATE_DENOMINATOR_COUNT_CAP:
        raise RequestError(
            "certificate denominator count is capped at "
            f"{CERTIFICATE_DENOMINATOR_COUNT_CAP}"
        )
    denominator_bits = 0
    budget = 0
    for denominator in denominators:
        bits = denominator.bit_length()
        if bits > CERTIFICATE_DENOMINATOR_BIT_CAP:
            raise RequestError(
                "certificate denominators are capped at "
                f"{CERTIFICATE_DENOMINATOR_BIT_CAP} bits"
            )
        denominator_bits += bits
        if denominator_bits > CERTIFICATE_OUTPUT_INTEGER_BIT_CAP:
            raise RequestError(
                "certificate aggregate exact-output size is capped at "
                f"{CERTIFICATE_OUTPUT_INTEGER_BIT_CAP} bits"
            )
        supplied = factorizations.get(denominator) if factorizations else None
        if supplied:
            # Supplied factor bases are primality-checked with O(sqrt base)
            # trial division before the product is validated, so they must be
            # counted even though the denominator itself is not refactored.
            # The exponent must also be bounded: validation materialises
            # ``prime ** exponent`` before the product-mismatch check, so an
            # oversized exponent forces giant-integer work.  A valid factor of
            # ``denominator`` satisfies ``prime ** exponent <= denominator``,
            # hence ``exponent <= denominator.bit_length()``; a larger exponent
            # can only fail the product check, so rejecting it loses nothing.
            exponent_cap = max(denominator.bit_length(), 1)
            supplied_product_bit_proxy = 0
            for base, exponent in supplied.items():
                if exponent > exponent_cap:
                    raise RequestError(
                        "certificate factorization exponent exceeds the "
                        "denominator's bit length"
                    )
                supplied_product_bit_proxy += exponent * max(base.bit_length(), 1)
                # For every valid prime-power product this proxy is at most
                # twice the product's true bit length.  Rejecting above that
                # threshold prevents a mismatching factor map from first
                # materialising a far larger integer during validation.
                if supplied_product_bit_proxy > 2 * bits:
                    raise RequestError(
                        "certificate supplied factorization exceeds the "
                        "denominator bit-work budget"
                    )
                if base >= 2:
                    budget += isqrt(base)
        else:
            budget += isqrt(denominator)
        if budget > CERTIFICATE_TRIAL_DIVISION_BUDGET:
            raise RequestError(
                "certificate exact factorization work is capped; supply a "
                "factorization or use smaller denominators"
            )

    pair_count = len(denominators) * (len(denominators) + 1) // 2
    kernel_bit_cells = pair_count * denominator_bits
    if kernel_bit_cells > CERTIFICATE_KERNEL_BIT_CELL_CAP:
        raise RequestError(
            "certificate combined kernel/bit work is capped at "
            f"{CERTIFICATE_KERNEL_BIT_CELL_CAP} bit-cells"
        )


def _certificate(payload: dict[str, Any]) -> dict[str, Any]:
    denominators = _ints(payload.get("denominators"), "denominators", 2)
    factorizations = _factorizations(payload.get("factorizations"))
    _enforce_certificate_limits(denominators, factorizations)
    started = time.perf_counter()
    result = kernel.portfolio_certificate(
        denominators,
        exact=_exact(payload.get("exact")),
        factorizations=factorizations,
    )
    elapsed = time.perf_counter() - started
    data = _jsonable(result)
    if isinstance(data, dict):
        data.setdefault("kernel_seconds", elapsed)
        data.setdefault("input_constraints", {
            "denominators": "complete reduced-residue batches",
            "endpoints": "excluded by the frozen interior convention",
        })
    return data


def _optimize(payload: dict[str, Any]) -> dict[str, Any]:
    if payload.get("benchmark"):
        start = _int(payload.get("start", DEFAULT_START), "start", 2)
        stop = _int(payload.get("stop", DEFAULT_STOP), "stop", 2)
        if stop - start > OPTIMIZE_BENCHMARK_SPAN_CAP:
            raise RequestError(
                "benchmark candidate span (stop - start) is capped at "
                f"{OPTIMIZE_BENCHMARK_SPAN_CAP}"
            )
        candidates = list(range(start, stop + 1))
        layers = _int(payload.get("layers", DEFAULT_LAYERS), "layers", 1)
        _enforce_optimize_limits(
            candidates,
            layers,
            samples=500,
            include_bruteforce=False,
        )
        result = optimizer.benchmark_case(
            start=start,
            stop=stop,
            layers=layers,
            seed=_int(payload.get("seed", DEFAULT_SEED), "seed"),
        )
        return _jsonable(result)
    candidates = _ints(payload.get("candidates"), "candidates", 2)
    if len(candidates) > OPTIMIZE_CANDIDATE_CAP:
        raise RequestError(
            f"optimize candidate count is capped at {OPTIMIZE_CANDIDATE_CAP}"
        )
    layers = _int(payload.get("layers"), "layers", 1)
    exact = _exact(payload.get("exact"))
    seed = _int(payload.get("seed", DEFAULT_SEED), "seed")
    samples = _int(payload.get("samples", 50), "samples", 1)
    if samples > OPTIMIZE_SAMPLE_CAP:
        raise RequestError(f"optimize samples are capped at {OPTIMIZE_SAMPLE_CAP}")
    _enforce_optimize_limits(
        candidates,
        layers,
        samples=samples,
        include_bruteforce=len(candidates) <= 18,
    )
    result: dict[str, Any] = {
        "constraints": {"candidates": candidates, "layers": layers},
        "greedy": optimizer.greedy_portfolio(candidates, layers, exact=exact),
        "largest_totient": optimizer.largest_totient_baseline(candidates, layers),
        "consecutive_high": optimizer.consecutive_high_baseline(candidates, layers),
        "random": optimizer.random_portfolio_baselines(candidates, layers, samples, seed),
        "warning": "If arbitrary 1D nodes are allowed, use a uniform or established quadrature rule instead.",
    }
    if len(candidates) <= 18:
        result["bruteforce"] = optimizer.bruteforce_optimum(candidates, layers, exact=exact)
    return _jsonable(result)


def _enforce_optimize_limits(
    candidates: list[int],
    layers: int,
    *,
    samples: int,
    include_bruteforce: bool,
) -> None:
    """Reject optimizer requests whose combined exact work exceeds a safe cap.

    Individual count and sample limits are insufficient: trial division scales
    with denominator magnitude, random baselines repeat factorization work, and
    the small-pool exact branch enumerates ``comb(C, layers)`` subsets.  This
    conservative proxy is evaluated before any optimizer entry point runs.
    """

    if layers > len(candidates):
        raise RequestError("layers cannot exceed the candidate count")
    roots = [isqrt(value) for value in candidates]
    trial_division_units = 5 * sum(roots) + samples * layers * max(roots)
    if trial_division_units > OPTIMIZE_TRIAL_DIVISION_BUDGET:
        raise RequestError(
            "optimize exact factorization work is capped at "
            f"{OPTIMIZE_TRIAL_DIVISION_BUDGET} trial-division units"
        )

    subset_evaluations = comb(len(candidates), layers) if include_bruteforce else 0
    kernel_cells = (
        2 * len(candidates) * len(candidates)
        + (samples + 4 + subset_evaluations) * layers * layers
    )
    if kernel_cells > OPTIMIZE_KERNEL_WORK_CELL_CAP:
        raise RequestError(
            "optimize combined matrix/evaluation work is capped at "
            f"{OPTIMIZE_KERNEL_WORK_CELL_CAP} cells"
        )


def _shift(payload: dict[str, Any]) -> dict[str, Any]:
    prime = _int(payload.get("p"), "p", 2)
    if prime > SHIFT_PRIME_CAP:
        raise RequestError(f"shift prime p is capped at {SHIFT_PRIME_CAP}")
    max_order = _int(payload.get("max_order", 6), "max_order", 0)
    if max_order > SHIFT_MAX_ORDER_CAP:
        raise RequestError(f"shift max_order is capped at {SHIFT_MAX_ORDER_CAP}")
    moments = shear.farey_shift_moments(
        prime, max_order=max_order, exact=_exact(payload.get("exact")))
    return _jsonable({
        "p": prime,
        "interior_count": shear.farey_interior_count(prime),
        "moments": moments,
        "triangular_prediction": {
            str(2 * r): _jsonable(shear.triangular_even_moment(r))
            for r in range(max_order // 2 + 1)
        },
        "limitations": [
            "The fixed interior convention excludes denominator-one endpoints.",
            "The triangular law is an asymptotic prediction, not a finite-sample identity.",
        ],
    })


def _gaps(payload: dict[str, Any]) -> dict[str, Any]:
    exact = _exact(payload.get("exact"))
    supplied = payload.get("gaps")
    farey_order = payload.get("farey_order")
    if (supplied is None) == (farey_order is None):
        raise RequestError("provide gaps or farey_order, but not both")
    if farey_order is not None:
        order = _int(farey_order, "farey_order", 2)
        if order > GAP_FAREY_ORDER_CAP:
            raise RequestError(f"farey_order is capped at {GAP_FAREY_ORDER_CAP}")
        values = gap_permutation.farey_gaps(order, exact=exact)
        source: dict[str, Any] = {"kind": "farey", "order": order}
    else:
        if not isinstance(supplied, list):
            raise RequestError("gaps must be a JSON array")
        if len(supplied) > GAP_SUPPLIED_COUNT_CAP:
            raise RequestError(
                f"supplied gaps are capped at {GAP_SUPPLIED_COUNT_CAP} entries"
            )
        values = _bounded_gap_values(supplied, exact=exact)
        source = {"kind": "supplied"}
    result = gap_permutation.gap_permutation_certificate(values, exact=exact)
    return _jsonable({"source": source, **asdict(result)})


def _strict_keys(value: dict[str, Any], allowed: set[str], name: str) -> None:
    if any(not isinstance(key, str) for key in value):
        raise RequestError(f"{name} field names must be strings")
    unknown = sorted(set(value).difference(allowed))
    if unknown:
        raise RequestError(f"{name} contains unknown fields: {', '.join(unknown)}")


def _rational(value: Any, name: str) -> int | Fraction:
    if isinstance(value, bool) or isinstance(value, float):
        raise RequestError(f"{name} must be an integer or rational string")
    if isinstance(value, int):
        if value.bit_length() > RATIONAL_BIT_CAP:
            raise RequestError(f"{name} exceeds the exact rational bit-length cap")
        return value
    if isinstance(value, str):
        text = value.strip()
        if not text:
            raise RequestError(f"{name} must not be empty")
        if len(text) > RATIONAL_TEXT_CAP or not _RATIONAL_PATTERN.fullmatch(text):
            raise RequestError(
                f"{name} must use a bounded integer or numerator/denominator string"
            )
        try:
            result = Fraction(text)
        except (ValueError, ZeroDivisionError) as exc:
            raise RequestError(f"{name} must be an integer or rational string") from exc
        if (
            result.numerator.bit_length() > RATIONAL_BIT_CAP
            or result.denominator.bit_length() > RATIONAL_BIT_CAP
        ):
            raise RequestError(f"{name} exceeds the exact rational bit-length cap")
        return result
    raise RequestError(f"{name} must be an integer or rational string")


def _bounded_gap_values(values: list[Any], *, exact: bool) -> list[Any]:
    """Parse supplied gaps and bound exact common-denominator arithmetic."""

    parsed: list[Any] = []
    unique_denominators: set[int] = set()
    unique_denominator_bits = 0
    max_numerator_bits = 1
    common_denominator = 1
    for index, value in enumerate(values):
        if isinstance(value, float):
            if not isfinite(value):
                raise RequestError(f"gaps[{index}] must be finite")
            # ``Fraction(str(value))`` is the exact-path normalization used by
            # the core.  Construct it here so its true bit cost is admitted.
            admitted = Fraction(str(value))
            output: Any = value
        else:
            admitted_value = _rational(value, f"gaps[{index}]")
            admitted = (
                admitted_value
                if isinstance(admitted_value, Fraction)
                else Fraction(admitted_value)
            )
            output = admitted_value
        parsed.append(output)
        if not exact:
            continue
        denominator = admitted.denominator
        common_denominator = (
            common_denominator // gcd(common_denominator, denominator) * denominator
        )
        if common_denominator.bit_length() > GAP_SUPPLIED_COMMON_DENOMINATOR_BIT_CAP:
            raise RequestError(
                "supplied exact-gap common denominator is capped at "
                f"{GAP_SUPPLIED_COMMON_DENOMINATOR_BIT_CAP} bits so exact "
                "results remain JSON-serializable"
            )
        if denominator not in unique_denominators:
            unique_denominators.add(denominator)
            unique_denominator_bits += denominator.bit_length()
        max_numerator_bits = max(max_numerator_bits, admitted.numerator.bit_length())
        work = len(parsed) * (unique_denominator_bits + max_numerator_bits)
        if work > GAP_SUPPLIED_EXACT_WORK_BIT_CAP:
            raise RequestError(
                "supplied exact-gap rational work is capped at "
                f"{GAP_SUPPLIED_EXACT_WORK_BIT_CAP} bit-cells; use fewer or "
                "smaller distinct denominators, or exact=false"
            )
    return parsed


def _string_list(value: Any, name: str) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise RequestError(f"{name} must be a JSON array")
    result: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item:
            raise RequestError(f"{name} must contain non-empty strings")
        result.append(item)
    return tuple(result)


def _string_groups(value: Any, name: str) -> tuple[tuple[str, ...], ...]:
    if not isinstance(value, list):
        raise RequestError(f"{name} must be a JSON array")
    return tuple(_string_list(group, f"{name} entry") for group in value)


def _problem(value: Any) -> BalanceProblem:
    if not isinstance(value, dict):
        raise RequestError("problem must be a JSON object")
    _strict_keys(
        value,
        {"items", "fixed_blocks", "pinned_prefix", "pinned_suffix", "precedence"},
        "problem",
    )
    supplied_items = value.get("items")
    if not isinstance(supplied_items, list):
        raise RequestError("problem.items must be a JSON array")
    items: list[BalanceItem] = []
    for index, supplied in enumerate(supplied_items):
        if not isinstance(supplied, dict):
            raise RequestError(f"problem.items[{index}] must be a JSON object")
        _strict_keys(supplied, {"item_id", "contribution", "mass", "category"}, f"problem.items[{index}]")
        item_id = supplied.get("item_id")
        if not isinstance(item_id, str) or not item_id:
            raise RequestError(f"problem.items[{index}].item_id must be a non-empty string")
        try:
            item_id.encode("utf-8")
        except UnicodeEncodeError as exc:
            raise RequestError(f"problem.items[{index}].item_id must be valid UTF-8") from exc
        contribution = supplied.get("contribution")
        if not isinstance(contribution, list) or not contribution:
            raise RequestError(f"problem.items[{index}].contribution must be a non-empty JSON array")
        category = supplied.get("category")
        if category is not None and (not isinstance(category, str) or not category):
            raise RequestError(f"problem.items[{index}].category must be null or a non-empty string")
        if category is not None:
            try:
                category.encode("utf-8")
            except UnicodeEncodeError as exc:
                raise RequestError(
                    f"problem.items[{index}].category must be valid UTF-8"
                ) from exc
        items.append(
            BalanceItem(
                item_id=item_id,
                contribution=tuple(
                    _rational(coordinate, f"problem.items[{index}].contribution")
                    for coordinate in contribution
                ),
                mass=_int(supplied.get("mass", 1), f"problem.items[{index}].mass", 1),
                category=category,
            )
        )
    fixed_blocks = _string_groups(value.get("fixed_blocks", []), "problem.fixed_blocks")
    pinned_prefix = _string_list(value.get("pinned_prefix", []), "problem.pinned_prefix")
    pinned_suffix = _string_list(value.get("pinned_suffix", []), "problem.pinned_suffix")
    precedence = _string_groups(value.get("precedence", []), "problem.precedence")
    if any(len(edge) != 2 for edge in precedence):
        raise RequestError("problem.precedence entries must contain exactly two item ids")
    return BalanceProblem(
        items=tuple(items),
        fixed_blocks=fixed_blocks,
        pinned_prefix=pinned_prefix,
        pinned_suffix=pinned_suffix,
        precedence=precedence,
    )


def _counts(value: Any) -> dict[str, int]:
    if not isinstance(value, dict):
        raise RequestError("counts must be a JSON object")
    result: dict[str, int] = {}
    for category, count in value.items():
        if not isinstance(category, str) or not category:
            raise RequestError("counts keys must be non-empty strings")
        try:
            category_bytes = category.encode("utf-8")
        except UnicodeEncodeError as exc:
            raise RequestError("counts keys must be valid UTF-8") from exc
        if len(category_bytes) > BALANCE_CATEGORY_UTF8_CAP:
            raise RequestError(
                f"counts keys are capped at {BALANCE_CATEGORY_UTF8_CAP} UTF-8 bytes"
            )
        result[category] = _int(count, f"count for {category!r}", 0)
    total = sum(result.values())
    if total > BALANCE_ITEM_CAP:
        raise RequestError(
            f"categorical inventory is capped at {BALANCE_ITEM_CAP} items per request"
        )
    return result


def _bounded_name(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value:
        raise RequestError(f"{name} must be a non-empty string")
    try:
        encoded = value.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise RequestError(f"{name} must be valid UTF-8") from exc
    if len(encoded) > BALANCE_CATEGORY_UTF8_CAP:
        raise RequestError(
            f"{name} is capped at {BALANCE_CATEGORY_UTF8_CAP} UTF-8 bytes"
        )
    return value


def _occurrence_ref(value: Any, name: str) -> OccurrenceRef:
    if not isinstance(value, dict):
        raise RequestError(f"{name} must be a JSON object")
    _strict_keys(value, {"category", "occurrence"}, name)
    return OccurrenceRef(
        category=_bounded_name(value.get("category"), f"{name}.category"),
        occurrence=_int(value.get("occurrence"), f"{name}.occurrence", 1),
    )


def _occurrence_refs(value: Any, name: str) -> tuple[OccurrenceRef, ...]:
    if not isinstance(value, list):
        raise RequestError(f"{name} must be a JSON array")
    return tuple(
        _occurrence_ref(item, f"{name}[{index}]")
        for index, item in enumerate(value)
    )


def _categorical_constraint_problem(
    counts: dict[str, int], value: Any
) -> CategoricalConstraintProblem:
    if not isinstance(value, dict):
        raise RequestError("constraints must be a JSON object")
    _strict_keys(
        value,
        {"fixed_blocks", "pinned_prefix", "pinned_suffix", "precedence"},
        "constraints",
    )

    supplied_blocks = value.get("fixed_blocks", [])
    if not isinstance(supplied_blocks, list):
        raise RequestError("constraints.fixed_blocks must be a JSON array")
    fixed_blocks: list[FixedOccurrenceBlock] = []
    for index, supplied in enumerate(supplied_blocks):
        name = f"constraints.fixed_blocks[{index}]"
        if not isinstance(supplied, dict):
            raise RequestError(f"{name} must be a JSON object")
        _strict_keys(supplied, {"block_id", "occurrences"}, name)
        fixed_blocks.append(
            FixedOccurrenceBlock(
                block_id=_bounded_name(supplied.get("block_id"), f"{name}.block_id"),
                occurrences=_occurrence_refs(
                    supplied.get("occurrences"), f"{name}.occurrences"
                ),
            )
        )

    supplied_precedence = value.get("precedence", [])
    if not isinstance(supplied_precedence, list):
        raise RequestError("constraints.precedence must be a JSON array")
    precedence: list[OccurrencePrecedence] = []
    for index, supplied in enumerate(supplied_precedence):
        name = f"constraints.precedence[{index}]"
        if not isinstance(supplied, dict):
            raise RequestError(f"{name} must be a JSON object")
        _strict_keys(supplied, {"edge_id", "before", "after"}, name)
        precedence.append(
            OccurrencePrecedence(
                edge_id=_bounded_name(supplied.get("edge_id"), f"{name}.edge_id"),
                before=_occurrence_ref(supplied.get("before"), f"{name}.before"),
                after=_occurrence_ref(supplied.get("after"), f"{name}.after"),
            )
        )

    return CategoricalConstraintProblem(
        counts=counts,
        fixed_blocks=tuple(fixed_blocks),
        pinned_prefix=_occurrence_refs(
            value.get("pinned_prefix", []), "constraints.pinned_prefix"
        ),
        pinned_suffix=_occurrence_refs(
            value.get("pinned_suffix", []), "constraints.pinned_suffix"
        ),
        precedence=tuple(precedence),
    )


def _enforce_constrained_quota_resource_limits(
    problem: CategoricalConstraintProblem,
) -> None:
    """Reject compact requests whose declared exact work exceeds local limits."""

    category_count = len(problem.counts)
    if category_count > CONSTRAINED_QUOTA_CATEGORY_CAP:
        raise RequestError(
            "constrained-quota category count is capped at "
            f"{CONSTRAINED_QUOTA_CATEGORY_CAP}"
        )

    total_items = sum(problem.counts.values())
    exact_metric_cells = total_items * category_count
    if exact_metric_cells > CONSTRAINED_QUOTA_EXACT_METRIC_CELL_CAP:
        raise RequestError(
            "constrained-quota exact metric work N*C is capped at "
            f"{CONSTRAINED_QUOTA_EXACT_METRIC_CELL_CAP}"
        )

    widest_block = max(
        (len(block.occurrences) for block in problem.fixed_blocks), default=0
    )
    if widest_block > CONSTRAINED_QUOTA_BLOCK_WIDTH_CAP:
        raise RequestError(
            "each constrained-quota fixed block is capped at "
            f"{CONSTRAINED_QUOTA_BLOCK_WIDTH_CAP} occurrence references"
        )

    constraint_references = (
        sum(len(block.occurrences) for block in problem.fixed_blocks)
        + len(problem.pinned_prefix)
        + len(problem.pinned_suffix)
        + 2 * len(problem.precedence)
    )
    if constraint_references > CONSTRAINED_QUOTA_CONSTRAINT_REFERENCE_CAP:
        raise RequestError(
            "constrained-quota occurrence references, counting both endpoints "
            "of each precedence edge, are capped at "
            f"{CONSTRAINED_QUOTA_CONSTRAINT_REFERENCE_CAP}"
        )


def _exact_fraction(value: Fraction | None) -> dict[str, int | str] | None:
    if value is None:
        return None
    exact = Fraction(value)
    return {
        "fraction": str(exact),
        "numerator": exact.numerator,
        "denominator": exact.denominator,
    }


def _preview(values: list[Any]) -> dict[str, list[Any]]:
    if len(values) <= 2 * ORDER_PREVIEW_ITEMS:
        return {"head": values, "tail": []}
    return {
        "head": values[:ORDER_PREVIEW_ITEMS],
        "tail": values[-ORDER_PREVIEW_ITEMS:],
    }


def _full_order_requested(value: Any) -> bool:
    if value is None:
        return False
    if not isinstance(value, bool):
        raise RequestError("full_order must be a boolean")
    return value


def _enforce_full_order_limit(total: int, utf8_size: int = 0) -> None:
    if total > FULL_ORDER_ITEM_CAP:
        raise RequestError(
            f"full order is capped at {FULL_ORDER_ITEM_CAP} items; use the digest and preview"
        )
    if utf8_size > FULL_ORDER_UTF8_CAP:
        raise RequestError(
            f"full order UTF-8 payload is capped at {FULL_ORDER_UTF8_CAP} bytes; use the digest and preview"
        )


def _quota_balance_response(
    mode: str,
    result: QuotaResult,
    *,
    full_order: bool,
    categories: tuple[str, ...] | None = None,
) -> dict[str, Any]:
    report = verify_quota_result(result)
    if not report.passed:
        raise ArithmeticError(f"quota result failed verification: {report.errors!r}")
    display_categories = tuple(result.categories) if categories is None else categories
    codes = result.order_codes
    names = [display_categories[code] for code in codes[:ORDER_PREVIEW_ITEMS]]
    if len(codes) > 2 * ORDER_PREVIEW_ITEMS:
        tail_names = [display_categories[codes[index]] for index in range(len(codes) - ORDER_PREVIEW_ITEMS, len(codes))]
        preview = {"head": names, "tail": tail_names}
    else:
        preview = {"head": [display_categories[code] for code in codes], "tail": []}
    order: dict[str, Any] = {
        "included": full_order,
        "total_items": len(codes),
        "sha256": result.order_sha256,
        "digest_encoding": result.digest_encoding,
        "preview": preview,
    }
    if full_order:
        _enforce_full_order_limit(len(codes))
        order["codes"] = list(codes)
    return {
        "schema_version": BALANCE_SCHEMA_VERSION,
        "mode": mode,
        "algorithm": result.algorithm,
        "inventory": {
            "categories": list(display_categories),
            "counts": list(result.counts),
            "total_items": len(codes),
        },
        "metrics": {
            "max_discrepancy": _exact_fraction(result.max_discrepancy),
            "accumulated_discrepancy": None,
            "lower_bound": _exact_fraction(result.lower_bound),
            "ratio_bound": _exact_fraction(result.ratio_bound),
            "additive_gap": _exact_fraction(result.max_discrepancy - result.lower_bound),
        },
        "guarantee": {
            "exact_optimum": result.exact_optimum,
            "scope": result.guarantee_scope,
            "comparison_set": result.comparison_set,
            "strict_factor": result.strict_factor,
        },
        "order": order,
        "feasibility": {"feasible": True, "verified": True},
        "explanation": _jsonable(result.explanation),
    }


def _occurrence_payload(category: str, occurrence: int) -> dict[str, int | str]:
    return {"category": category, "occurrence": occurrence}


def _ranked_occurrence_preview(
    categories: tuple[str, ...], counts: tuple[int, ...], codes: Any
) -> dict[str, list[dict[str, int | str]]]:
    if len(codes) <= 2 * ORDER_PREVIEW_ITEMS:
        seen = [0] * len(categories)
        head: list[dict[str, int | str]] = []
        for code in codes:
            seen[code] += 1
            head.append(_occurrence_payload(categories[code], seen[code]))
        return {"head": head, "tail": []}

    seen = [0] * len(categories)
    head = []
    for code in codes[:ORDER_PREVIEW_ITEMS]:
        seen[code] += 1
        head.append(_occurrence_payload(categories[code], seen[code]))

    remaining = list(counts)
    reverse_tail: list[dict[str, int | str]] = []
    for index in range(len(codes) - 1, len(codes) - ORDER_PREVIEW_ITEMS - 1, -1):
        code = codes[index]
        reverse_tail.append(_occurrence_payload(categories[code], remaining[code]))
        remaining[code] -= 1
    return {"head": head, "tail": list(reversed(reverse_tail))}


def _all_ranked_occurrences(
    categories: tuple[str, ...], codes: Any
) -> list[dict[str, int | str]]:
    seen = [0] * len(categories)
    occurrences: list[dict[str, int | str]] = []
    for code in codes:
        seen[code] += 1
        occurrences.append(_occurrence_payload(categories[code], seen[code]))
    return occurrences


def _constrained_quota_balance_response(
    problem: CategoricalConstraintProblem,
    result: ConstrainedQuotaResult,
    *,
    full_order: bool,
) -> dict[str, Any]:
    report = verify_constrained_quota(problem, result)
    if not report.passed:
        raise ArithmeticError(
            f"constrained quota result failed verification: {report.errors!r}"
        )
    categories = tuple(result.categories)
    counts = tuple(result.counts)
    codes = result.order_codes
    order: dict[str, Any] = {
        "included": full_order,
        "total_items": len(codes),
        "sha256": result.order_sha256,
        "digest_encoding": result.digest_encoding,
        "preview": _ranked_occurrence_preview(categories, counts, codes),
    }
    if full_order:
        _enforce_full_order_limit(len(codes))
        occurrences = _all_ranked_occurrences(categories, codes)
        encoded_size = len(
            json.dumps(occurrences, ensure_ascii=False, separators=(",", ":")).encode(
                "utf-8"
            )
        )
        _enforce_full_order_limit(len(codes), encoded_size)
        order["occurrences"] = occurrences
    return {
        "schema_version": BALANCE_SCHEMA_VERSION,
        "mode": "constrained-quota",
        "algorithm": result.algorithm,
        "inventory": {
            "categories": list(categories),
            "counts": list(counts),
            "total_items": len(codes),
        },
        "metrics": {
            "max_discrepancy": _exact_fraction(result.max_discrepancy),
            "accumulated_discrepancy": _exact_fraction(
                result.accumulated_discrepancy
            ),
            "lower_bound": _exact_fraction(result.lower_bound),
            "ratio_bound": _exact_fraction(result.ratio_bound),
            "additive_gap": _exact_fraction(result.additive_gap),
        },
        "guarantee": {
            "primary_optimum_proved": result.primary_optimum_proved,
            "proved_objective": "primary_B_only",
            "scope": result.guarantee_scope,
            "comparison_set": result.comparison_set,
            "strict_factor": None,
        },
        "order": order,
        "feasibility": _jsonable(result.feasibility),
        "warnings": [
            "No uniform factor-three guarantee applies under constraints.",
            "A closed interval proves optimality only for primary B; reported Q is measured exactly but is not claimed optimal.",
        ],
        "explanation": _jsonable(result.explanation),
    }


def _ordering_balance_response(
    mode: str,
    problem: BalanceProblem,
    result: OrderingResult,
    *,
    full_order: bool,
) -> dict[str, Any]:
    report = verify_order(problem, result.order)
    if not report.passed or report.order_sha256 is None:
        raise ArithmeticError(f"ordering result failed verification: {report.errors!r}")
    order_values = list(result.order)
    order: dict[str, Any] = {
        "included": full_order,
        "total_items": len(order_values),
        "sha256": report.order_sha256,
        "digest_encoding": "uint32-length-prefixed-utf8-item-id-v1",
        "preview": _preview(order_values),
    }
    if full_order:
        _enforce_full_order_limit(
            len(order_values), sum(len(item_id.encode("utf-8")) for item_id in order_values)
        )
        order["item_ids"] = order_values
    return {
        "schema_version": BALANCE_SCHEMA_VERSION,
        "mode": mode,
        "algorithm": result.algorithm,
        "metrics": {
            "max_discrepancy": _exact_fraction(result.max_discrepancy),
            "accumulated_discrepancy": _exact_fraction(result.accumulated_discrepancy),
            "lower_bound": _exact_fraction(result.lower_bound),
            "ratio_bound": _exact_fraction(result.ratio_bound),
            "additive_gap": _exact_fraction(result.additive_gap),
        },
        "guarantee": {
            "exact_optimum": result.exact_optimum,
            "scope": result.guarantee_scope,
            "comparison_set": result.comparison_set,
            "strict_factor": None,
        },
        "order": order,
        "feasibility": _jsonable(result.feasibility),
        "explanation": _jsonable(result.explanation),
    }


def balance_response(payload: dict[str, Any]) -> dict[str, Any]:
    """Parse one frozen balance request and return the canonical JSON-ready schema."""

    if not isinstance(payload, dict):
        raise RequestError("balance request must be a JSON object")
    _strict_keys(
        payload,
        {"mode", "counts", "constraints", "problem", "preset", "full_order"},
        "balance request",
    )
    mode = payload.get("mode", "quota")
    allowed_modes = {"quota", "binary", "constrained-quota", "exact", "constrained"}
    if not isinstance(mode, str) or mode not in allowed_modes:
        raise RequestError(
            "mode must be one of: quota, binary, constrained-quota, exact, constrained"
        )
    full_order = _full_order_requested(payload.get("full_order"))

    if mode == "constrained-quota":
        if "counts" not in payload or "constraints" not in payload:
            raise RequestError(
                "constrained-quota mode requires both counts and constraints"
            )
        if "problem" in payload or "preset" in payload:
            raise RequestError(
                "constrained-quota mode accepts counts and constraints, not problem or preset"
            )
        count_mapping = _counts(payload["counts"])
        problem = _categorical_constraint_problem(
            count_mapping, payload["constraints"]
        )
        _enforce_constrained_quota_resource_limits(problem)
        if full_order:
            _enforce_full_order_limit(sum(count_mapping.values()))
        return _constrained_quota_balance_response(
            problem, solve_constrained_quota(problem), full_order=full_order
        )

    if "constraints" in payload:
        raise RequestError("constraints are supported only in constrained-quota mode")
    supplied = sum(key in payload for key in ("counts", "problem", "preset"))
    if supplied != 1:
        raise RequestError("provide exactly one of counts, problem, or preset")

    application: dict[str, object] | None = None
    if "preset" in payload:
        if mode != "quota":
            raise RequestError("application presets are available only in quota mode")
        preset_id = payload["preset"]
        if not isinstance(preset_id, str):
            raise RequestError("preset must be a string")
        try:
            application = application_preset_payload(preset_id)
        except (KeyError, TypeError, ValueError) as exc:
            raise RequestError(str(exc)) from exc
        count_mapping = _counts(application["counts"])
    elif "counts" in payload:
        if mode not in {"quota", "binary"}:
            raise RequestError("counts are supported only in quota or binary mode")
        count_mapping = _counts(payload["counts"])
    else:
        if mode not in {"exact", "constrained"}:
            raise RequestError("problem is supported only in exact or constrained mode")
        problem = _problem(payload["problem"])
        if full_order:
            _enforce_full_order_limit(
                len(problem.items),
                sum(len(item.item_id.encode("utf-8")) for item in problem.items),
            )
        result = solve_exact(problem) if mode == "exact" else solve_constrained(problem)
        return _ordering_balance_response(mode, problem, result, full_order=full_order)

    if full_order:
        _enforce_full_order_limit(sum(count_mapping.values()))
    if mode == "quota":
        response = _quota_balance_response(mode, quota_order(count_mapping), full_order=full_order)
    else:
        ordered = sorted(count_mapping.items(), key=lambda row: row[0].encode("utf-8"))
        if len(ordered) != 2:
            raise RequestError("binary mode requires exactly two category keys")
        categories = tuple(category for category, _count in ordered)
        result = quota_mechanical_order(ordered[0][1], ordered[1][1])
        response = _quota_balance_response(
            mode, result, full_order=full_order, categories=categories
        )
    if application is not None:
        response["application"] = application
    return response


def api_response(path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    if path == "/api/health":
        return {"status": "ok", "service": "coprimebatch", "api": "frozen-core-v1"}
    if path == "/api/certificate":
        return _certificate(payload or {})
    if path == "/api/optimize":
        return _optimize(payload or {})
    if path == "/api/shift":
        return _shift(payload or {})
    if path == "/api/gaps":
        return _gaps(payload or {})
    if path == "/api/balance":
        return balance_response(payload or {})
    raise RequestError("unknown API route", HTTPStatus.NOT_FOUND)


def _host_is_loopback(host_header: str | None) -> bool:
    """Return whether a ``Host`` header names a loopback authority only.

    The loopback *bind* stops direct remote TCP, but it does not stop a
    DNS-rebinding attack in which a malicious page whose domain re-resolves to
    ``127.0.0.1`` reaches this API through the browser.  Restricting the ``Host``
    authority to the loopback allow-list is the standard local-server defense.
    """

    if host_header is None:
        return False
    host = host_header.strip()
    if not host:
        return False
    if host.startswith("["):
        # Bracketed IPv6 authority such as [::1]:8765.  Match the complete
        # authority so a suffix such as ``[::1]attacker`` cannot be ignored.
        match = re.fullmatch(r"\[([^\]]+)\](?::([0-9]+))?", host)
        if match is None:
            return False
        name = match.group(1)
    elif host == "::1":
        name = host
    elif host.count(":") == 1:
        name, port = host.rsplit(":", 1)
        if not name or not port.isdigit():
            return False
    elif ":" in host:
        return False
    else:
        name = host
    return name.lower() in LOOPBACK_HOSTS


def _origin_is_loopback(origin_header: str | None) -> bool:
    """Accept an absent Origin or an HTTP(S) origin on a loopback host only."""

    if origin_header is None:
        return True
    origin = origin_header.strip()
    if not origin or origin.lower() == "null":
        return False
    parsed = urlparse(origin)
    if parsed.scheme.lower() not in {"http", "https"}:
        return False
    if parsed.username is not None or parsed.password is not None:
        return False
    if parsed.path not in ("", "/") or parsed.params or parsed.query or parsed.fragment:
        return False
    try:
        parsed.port
    except ValueError:
        return False
    return parsed.hostname is not None and parsed.hostname.lower() in LOOPBACK_HOSTS


class Handler(BaseHTTPRequestHandler):
    server_version = "CoprimeBatchHTTP/1.0"
    # Break slowloris-style trickled/partial requests: a client that does not
    # deliver its declared body within the deadline loses its worker thread.
    timeout = SOCKET_TIMEOUT_SECONDS

    def _reject_non_loopback_host(self) -> bool:
        if _host_is_loopback(self.headers.get("Host")):
            return False
        self._error(
            RequestError(
                "Host header must name a loopback authority",
                HTTPStatus.FORBIDDEN,
            )
        )
        return True

    def _reject_unsafe_post_headers(self) -> bool:
        if not _origin_is_loopback(self.headers.get("Origin")):
            self._error(
                RequestError(
                    "Origin header must name a loopback HTTP(S) origin",
                    HTTPStatus.FORBIDDEN,
                )
            )
            return True
        if self.headers.get_content_type().lower() != "application/json":
            self._error(
                RequestError(
                    "API POST requests require Content-Type: application/json",
                    HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
                )
            )
            return True
        return False

    def _send_json(self, status: HTTPStatus, data: Any) -> None:
        encoded = json.dumps(_jsonable(data), ensure_ascii=False, separators=(",", ":")).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(encoded)

    def _error(self, error: Exception) -> None:
        if isinstance(error, RequestError):
            status = error.status
        elif isinstance(error, (TypeError, ValueError, ArithmeticError)):
            status = HTTPStatus.BAD_REQUEST
        else:
            status = HTTPStatus.INTERNAL_SERVER_ERROR
        payload: dict[str, Any] = {
            "error": str(error) or "internal server error",
            "status": status.value,
        }
        if isinstance(error, InfeasibleProblemError):
            payload["witness"] = _jsonable(error.witness)
        self._send_json(status, payload)

    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
        if self._reject_non_loopback_host():
            return
        path = urlparse(self.path).path
        if path.startswith("/api/"):
            try:
                self._send_json(HTTPStatus.OK, api_response(path))
            except Exception as exc:  # API errors must remain JSON.
                self._error(exc)
            return
        self._serve_static(path)

    def do_POST(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
        if self._reject_non_loopback_host():
            return
        if self._reject_unsafe_post_headers():
            return
        path = urlparse(self.path).path
        if not path.startswith("/api/"):
            self._error(RequestError("POST is only supported for API routes", HTTPStatus.NOT_FOUND))
            return
        try:
            self._send_json(HTTPStatus.OK, api_response(path, _body(self)))
        except Exception as exc:
            self._error(exc)

    def _serve_static(self, path: str) -> None:
        relative = "index.html" if path in ("", "/") else path.removeprefix("/")
        candidate = (ROOT / relative).resolve()
        if ROOT not in candidate.parents and candidate != ROOT:
            self._error(RequestError("invalid static path", HTTPStatus.NOT_FOUND))
            return
        if not candidate.is_file():
            self._error(RequestError("static file not found", HTTPStatus.NOT_FOUND))
            return
        data = candidate.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", mimetypes.guess_type(candidate.name)[0] or "application/octet-stream")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_PUT(self) -> None:  # noqa: N802
        self._error(RequestError("method not allowed", HTTPStatus.METHOD_NOT_ALLOWED))

    def do_DELETE(self) -> None:  # noqa: N802
        self._error(RequestError("method not allowed", HTTPStatus.METHOD_NOT_ALLOWED))

    def log_message(self, format: str, *args: Any) -> None:
        return


class _BoundedThreadingHTTPServer(ThreadingHTTPServer):
    """Threading server that caps the number of concurrently handled requests.

    A plain ``ThreadingHTTPServer`` spawns an unbounded worker thread (and its
    read buffer) per connection, so a slowloris client that opens many parked
    connections can exhaust threads and memory.  A non-blocking semaphore caps
    live handlers; connections beyond the cap are closed immediately instead of
    parking a thread.
    """

    max_concurrent_connections = MAX_CONCURRENT_CONNECTIONS

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._connection_slots = threading.BoundedSemaphore(
            self.max_concurrent_connections
        )

    def process_request(self, request: Any, client_address: Any) -> None:
        if not self._connection_slots.acquire(blocking=False):
            # At capacity: drop the connection instead of parking a thread.
            self.shutdown_request(request)
            return
        super().process_request(request, client_address)

    def process_request_thread(self, request: Any, client_address: Any) -> None:
        try:
            super().process_request_thread(request, client_address)
        finally:
            self._connection_slots.release()


class _IPv6ThreadingHTTPServer(_BoundedThreadingHTTPServer):
    address_family = socket.AF_INET6


def _loopback_host(host: str) -> str:
    if not isinstance(host, str) or host.lower() not in LOOPBACK_HOSTS:
        allowed = ", ".join(sorted(LOOPBACK_HOSTS))
        raise ValueError(f"host must be an explicit loopback address: {allowed}")
    return host.lower()


def serve(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> None:
    host = _loopback_host(host)
    server_type = (
        _IPv6ThreadingHTTPServer if host == "::1" else _BoundedThreadingHTTPServer
    )
    with server_type((host, port), Handler) as server:
        print(f"CoprimeBatch server listening on http://{host}:{server.server_port}", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    args = parser.parse_args(argv)
    try:
        serve(args.host, args.port)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
