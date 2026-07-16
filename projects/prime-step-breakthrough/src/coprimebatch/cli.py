"""Command-line interface for coprime-batch certificates and diagnostics."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, is_dataclass
from fractions import Fraction
from typing import Sequence

from .kernel import (
    first_negative_prime_delta,
    marginal_energy,
    portfolio_certificate,
    prime_energy_delta,
)
from .gap_permutation import farey_gaps, gap_permutation_certificate
from .optimizer import benchmark_case, greedy_portfolio
from .shear import farey_shift_moments
from .web import BALANCE_JSON_INPUT_CAP, balance_response


class _Parser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise ValueError(message)


def _add_json_flag(parser: argparse.ArgumentParser, *, inherited: bool = False) -> None:
    kwargs: dict[str, object] = {"action": "store_true", "help": "emit JSON"}
    if inherited:
        kwargs["default"] = argparse.SUPPRESS
    parser.add_argument("--json", **kwargs)


def build_parser() -> argparse.ArgumentParser:
    parser = _Parser(prog="coprimebatch", description=__doc__)
    _add_json_flag(parser)
    subparsers = parser.add_subparsers(dest="command", required=True)

    certificate = subparsers.add_parser("certificate", help="certify a portfolio")
    certificate.add_argument("denominators", nargs="+", type=int)
    certificate.add_argument("--candidate", type=int, help="also report marginal energy")
    certificate.add_argument(
        "--float", action="store_true", dest="float_mode", help="return float energy"
    )
    _add_json_flag(certificate, inherited=True)

    optimize = subparsers.add_parser("optimize", help="greedily select layers")
    optimize.add_argument("candidates", nargs="*", type=int)
    optimize.add_argument("--start", type=int, default=2)
    optimize.add_argument("--stop", type=int, default=200)
    optimize.add_argument("--layers", type=int, default=10)
    optimize.add_argument("--exact", action="store_true")
    _add_json_flag(optimize, inherited=True)

    shift = subparsers.add_parser("shift", help="compute finite Farey-shift moments")
    shift.add_argument("p", type=int)
    shift.add_argument("--max-order", type=int, default=6)
    shift.add_argument("--exact", action="store_true")
    _add_json_flag(shift, inherited=True)

    prime_delta = subparsers.add_parser(
        "prime-delta", help="compute or scan prime energy deltas"
    )
    prime_delta.add_argument("p", type=int, nargs="?")
    prime_delta.add_argument("--limit", type=int)
    _add_json_flag(prime_delta, inherited=True)

    benchmark = subparsers.add_parser("benchmark", help="run the fixed comparison")
    benchmark.add_argument("--start", type=int, default=2)
    benchmark.add_argument("--stop", type=int, default=200)
    benchmark.add_argument("--layers", type=int, default=10)
    benchmark.add_argument("--seed", type=int, default=20260715)
    _add_json_flag(benchmark, inherited=True)

    gaps = subparsers.add_parser("gaps", help="certify an ordered gap vector")
    gaps.add_argument("gaps", nargs="*", help="rational gaps such as 1/6 or 0.25")
    gaps.add_argument("--farey-order", type=int)
    gaps.add_argument(
        "--float", action="store_true", dest="float_mode", help="return float metrics"
    )
    _add_json_flag(gaps, inherited=True)

    balance = subparsers.add_parser(
        "balance", help="construct and certify a prefix-balanced order"
    )
    balance.add_argument(
        "counts",
        nargs="*",
        metavar="NAME=COUNT",
        help="categorical inventory for quota or binary mode",
    )
    balance.add_argument(
        "--mode",
        choices=("quota", "binary", "constrained-quota", "exact", "constrained"),
        default="quota",
    )
    balance.add_argument(
        "--problem-json",
        metavar="FILE",
        help="BalanceProblem JSON file, or - for standard input",
    )
    balance.add_argument(
        "--constraints-json",
        metavar="FILE",
        help="compact occurrence-constraint JSON file, or - for standard input",
    )
    balance.add_argument(
        "--preset",
        help="allowlisted compact application preset id",
    )
    balance.add_argument(
        "--full-order",
        action="store_true",
        help="include the full order when it is below the hard API cap",
    )
    _add_json_flag(balance, inherited=True)
    return parser


def _json_value(value: object) -> object:
    if isinstance(value, Fraction):
        return str(value)
    if is_dataclass(value):
        return _json_value(asdict(value))
    if isinstance(value, dict):
        return {str(key): _json_value(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_json_value(item) for item in value]
    return value


def _certificate_payload(args: argparse.Namespace) -> dict[str, object]:
    exact = not args.float_mode
    certificate = portfolio_certificate(args.denominators, exact=exact)
    payload: dict[str, object] = {
        "command": "certificate",
        "exact": exact,
        **asdict(certificate),
    }
    if args.candidate is not None:
        payload["candidate"] = args.candidate
        payload["marginal_energy"] = marginal_energy(
            args.denominators, args.candidate, exact=exact
        )
    return payload


def _optimize_payload(args: argparse.Namespace) -> dict[str, object]:
    if args.candidates:
        if args.start != 2 or args.stop != 200:
            raise ValueError("positional candidates cannot be combined with --start/--stop")
        candidates = args.candidates
    else:
        if args.stop < args.start:
            raise ValueError("--stop must be at least --start")
        candidates = range(args.start, args.stop + 1)
    result = greedy_portfolio(candidates, args.layers, exact=args.exact)
    return {"command": "optimize", "exact": args.exact, **asdict(result)}


def _prime_delta_payload(args: argparse.Namespace) -> dict[str, object]:
    if (args.p is None) == (args.limit is None):
        raise ValueError("provide exactly one of P or --limit")
    if args.p is not None:
        delta = prime_energy_delta(args.p)
        return {
            "command": "prime-delta",
            "p": args.p,
            "delta": delta,
            "delta_float": float(delta),
            "negative": delta < 0,
        }
    result = first_negative_prime_delta(args.limit)
    return {
        "command": "prime-delta",
        "limit": args.limit,
        "result": None
        if result is None
        else {
            "p": result[0],
            "delta": result[1],
            "delta_float": float(result[1]),
        },
    }


def _gaps_payload(args: argparse.Namespace) -> dict[str, object]:
    if bool(args.gaps) == (args.farey_order is not None):
        raise ValueError("provide rational gaps or --farey-order, but not both")
    exact = not args.float_mode
    source: dict[str, object]
    if args.farey_order is not None:
        values = farey_gaps(args.farey_order, exact=exact)
        source = {"kind": "farey", "order": args.farey_order}
    else:
        values = args.gaps
        source = {"kind": "supplied"}
    certificate = gap_permutation_certificate(values, exact=exact)
    return {
        "command": "gaps",
        "exact": exact,
        "source": source,
        **asdict(certificate),
    }


def _balance_counts(values: Sequence[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"count {value!r} must use NAME=COUNT syntax")
        name, raw_count = value.split("=", 1)
        if not name:
            raise ValueError("category names must not be empty")
        if name in counts:
            raise ValueError(f"duplicate category name: {name!r}")
        try:
            count = int(raw_count)
        except ValueError as exc:
            raise ValueError(f"count for {name!r} must be an integer") from exc
        if str(count) != raw_count and not (raw_count.startswith("+") and str(count) == raw_count[1:]):
            raise ValueError(f"count for {name!r} must be a base-10 integer")
        if count < 0:
            raise ValueError(f"count for {name!r} must be nonnegative")
        counts[name] = count
    return counts


def _balance_json(path: str, option: str) -> dict[str, object]:
    if path == "-":
        source = sys.stdin.read(BALANCE_JSON_INPUT_CAP + 1)
        if len(source.encode("utf-8")) > BALANCE_JSON_INPUT_CAP:
            raise ValueError(
                f"{option} input is capped at {BALANCE_JSON_INPUT_CAP} UTF-8 bytes"
            )
    else:
        try:
            with open(path, "rb") as handle:
                raw = handle.read(BALANCE_JSON_INPUT_CAP + 1)
        except OSError as exc:
            raise ValueError(f"cannot read {option} file: {exc}") from exc
        if len(raw) > BALANCE_JSON_INPUT_CAP:
            raise ValueError(
                f"{option} input is capped at {BALANCE_JSON_INPUT_CAP} UTF-8 bytes"
            )
        try:
            source = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"{option} must contain valid UTF-8 JSON") from exc
    try:
        def unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
            result: dict[str, object] = {}
            for key, value in pairs:
                if key in result:
                    raise ValueError(f"duplicate JSON object key: {key!r}")
                result[key] = value
            return result

        payload = json.loads(source, object_pairs_hook=unique_object)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{option} must contain valid UTF-8 JSON") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"{option} must contain a JSON object")
    return payload


def _balance_problem_json(path: str) -> dict[str, object]:
    return _balance_json(path, "--problem-json")


def _balance_constraints_json(path: str) -> dict[str, object]:
    return _balance_json(path, "--constraints-json")


def _balance_payload(args: argparse.Namespace) -> dict[str, object]:
    if args.mode == "constrained-quota":
        if not args.counts or args.constraints_json is None:
            raise ValueError(
                "constrained-quota mode requires NAME=COUNT values and --constraints-json"
            )
        if args.problem_json is not None or args.preset is not None:
            raise ValueError(
                "constrained-quota mode accepts counts and --constraints-json, not --problem-json or --preset"
            )
        return balance_response(
            {
                "mode": args.mode,
                "counts": _balance_counts(args.counts),
                "constraints": _balance_constraints_json(args.constraints_json),
                "full_order": args.full_order,
            }
        )

    if args.constraints_json is not None:
        raise ValueError("--constraints-json requires --mode constrained-quota")
    supplied = bool(args.counts) + (args.problem_json is not None) + (args.preset is not None)
    if supplied != 1:
        raise ValueError("provide exactly one of NAME=COUNT values, --problem-json, or --preset")
    request: dict[str, object] = {
        "mode": args.mode,
        "full_order": args.full_order,
    }
    if args.counts:
        request["counts"] = _balance_counts(args.counts)
    elif args.problem_json is not None:
        request["problem"] = _balance_problem_json(args.problem_json)
    else:
        request["preset"] = args.preset
    return balance_response(request)


def _dispatch(args: argparse.Namespace) -> dict[str, object]:
    if args.command == "certificate":
        return _certificate_payload(args)
    if args.command == "optimize":
        return _optimize_payload(args)
    if args.command == "shift":
        return {
            "command": "shift",
            "exact": args.exact,
            **farey_shift_moments(args.p, args.max_order, exact=args.exact),
        }
    if args.command == "prime-delta":
        return _prime_delta_payload(args)
    if args.command == "benchmark":
        return {
            "command": "benchmark",
            **benchmark_case(args.start, args.stop, args.layers, args.seed),
        }
    if args.command == "gaps":
        return _gaps_payload(args)
    if args.command == "balance":
        return _balance_payload(args)
    raise ValueError(f"unknown command: {args.command}")


def _text_output(payload: dict[str, object]) -> str:
    return "\n".join(
        f"{key}: {_json_value(value)}" for key, value in payload.items()
    )


def main(argv: Sequence[str] | None = None) -> int:
    try:
        args = build_parser().parse_args(argv)
        payload = _dispatch(args)
        if args.json:
            print(json.dumps(_json_value(payload), sort_keys=True))
        else:
            print(_text_output(payload))
        return 0
    except (TypeError, ValueError, ArithmeticError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
