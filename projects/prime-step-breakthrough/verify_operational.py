#!/usr/bin/env python3
"""Run all frozen operational prefix-balance gates and original regressions."""

from __future__ import annotations

import ast
import hashlib
import json
import os
import subprocess
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable, Mapping


sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
CACHE_DIR_NAMES = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
MAX_SECONDS = 30.0
MAX_RSS_BYTES = 134_217_728
TOTAL_ITEMS = 1_000_000
FROZEN_COUNTS = {
    "alpha": 100_003,
    "beta": 200_009,
    "delta": 399_977,
    "gamma": 300_011,
}
FROZEN_CONSTRAINTS = {
    "fixed_blocks": [
        {
            "block_id": "joint-block-001",
            "occurrences": [
                {"category": "alpha", "occurrence": 1001},
                {"category": "alpha", "occurrence": 1002},
                {"category": "delta", "occurrence": 1001},
                {"category": "beta", "occurrence": 2001},
                {"category": "gamma", "occurrence": 3001},
            ],
        }
    ],
    "pinned_prefix": [
        {"category": "alpha", "occurrence": 1},
        {"category": "beta", "occurrence": 1},
        {"category": "delta", "occurrence": 1},
        {"category": "gamma", "occurrence": 1},
    ],
    "pinned_suffix": [
        {"category": "gamma", "occurrence": 300_011},
        {"category": "delta", "occurrence": 399_977},
    ],
    "precedence": [
        {
            "edge_id": "rare-before-dense-001",
            "before": {"category": "alpha", "occurrence": 1000},
            "after": {"category": "delta", "occurrence": 1000},
        }
    ],
}
FROZEN_CONSTRAINTS_SHA256 = (
    "85b5161d9c938f437a3d24315d271abf5cdf8bc14eba1e972a410e006dd1ae1a"
)
FROZEN_CONSTRAINED_ORDER_SHA256 = (
    "3194a7661d0d90f6115bba41cfed1c506fd8f9442c0f54c0a8069ff90662c675"
)
FROZEN_UNCONSTRAINED_ORDER_SHA256 = (
    "c92afcfccfc6bd10a920b753c5d9c5cd6f929101ecc3f5f40fdbe937db5c3ebd"
)
FROZEN_CONSTRAINED_RESULT_FIELDS = {
    "max_discrepancy": "360167777/200000",
    "accumulated_discrepancy": "455298078991/62500",
    "lower_bound": "1799839/1000",
    "additive_gap": "199977/200000",
    "ratio_bound": "360167777/359967800",
}
REQUIRED_WITNESS_CODES = {
    "DUPLICATE_ITEM_ID",
    "DIMENSION_MISMATCH",
    "NONRATIONAL_CONTRIBUTION",
    "INVALID_MASS",
    "CENTERING_RESIDUAL",
    "UNKNOWN_CONSTRAINT_ID",
    "BLOCK_OVERLAP",
    "BLOCK_REPEATED_ITEM",
    "BLOCK_INTERNAL_PRECEDENCE_REVERSED",
    "PREFIX_SUFFIX_OVERLAP",
    "PIN_SPLITS_BLOCK",
    "PIN_ORDER_PRECEDENCE_CONFLICT",
    "CONTRACTED_DAG_CYCLE",
    "ORACLE_LIMIT_EXCEEDED",
    "OCCURRENCE_OUT_OF_RANGE",
    "BLOCK_OCCURRENCE_ORDER_CONFLICT",
    "BLOCK_CATEGORY_GAP",
    "PIN_OCCURRENCE_ORDER_CONFLICT",
    "FRONTIER_DEADLOCK",
}


def cache_paths(root: Path = ROOT) -> set[str]:
    found: set[str] = set()
    for path in root.rglob("*"):
        if path.name in CACHE_DIR_NAMES or path.suffix in {".pyc", ".pyo"}:
            found.add(path.relative_to(root).as_posix())
    return found


def new_cache_paths(before: Iterable[str], after: Iterable[str]) -> set[str]:
    return set(after) - set(before)


def source_hashes(root: Path = ROOT) -> dict[str, str]:
    """Hash executable/research sources while excluding mutable evidence."""

    hashes: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if relative.parts and relative.parts[0] == "artifacts":
            continue
        if any(part in CACHE_DIR_NAMES for part in relative.parts):
            continue
        if path.suffix not in {".py", ".md", ".toml", ".html", ".css", ".js"}:
            continue
        hashes[relative.as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return hashes


def source_changes(before: Mapping[str, str], after: Mapping[str, str]) -> list[str]:
    names = sorted(set(before) | set(after))
    return [name for name in names if before.get(name) != after.get(name)]


def permutation_enumeration_calls(source: str) -> list[int]:
    """Find factorial enumeration calls forbidden in the production core."""

    tree = ast.parse(source)
    lines: list[int] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        function = node.func
        name = function.id if isinstance(function, ast.Name) else (
            function.attr if isinstance(function, ast.Attribute) else ""
        )
        if name in {"permutations", "permutation_iterator"}:
            lines.append(node.lineno)
    return lines


def missing_witness_codes(source: str) -> list[str]:
    return sorted(code for code in REQUIRED_WITNESS_CODES if code not in source)


def static_check(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    required = (
        root / "src" / "coprimebatch" / "prefix_balance.py",
        root / "tests" / "prefix_balance_oracles.py",
        root / "tests" / "test_prefix_balance.py",
        root / "benchmark_operational.py",
        root / "benchmark_constrained_operational.py",
        root / "verify_operational.py",
        root / "verify_all.py",
    )
    for path in required:
        if not path.is_file():
            errors.append(f"missing required path: {path.relative_to(root)}")
    for path in sorted(root.rglob("*.py")):
        relative = path.relative_to(root)
        if any(part in CACHE_DIR_NAMES for part in relative.parts):
            continue
        try:
            ast.parse(path.read_text(), filename=str(path))
        except (OSError, SyntaxError, UnicodeError) as exc:
            errors.append(f"{relative}: {exc}")
    core = root / "src" / "coprimebatch" / "prefix_balance.py"
    if core.is_file():
        core_source = core.read_text()
        calls = permutation_enumeration_calls(core_source)
        if calls:
            errors.append(
                "production prefix_balance enumerates permutations at lines "
                + ", ".join(map(str, calls))
            )
        missing = missing_witness_codes(core_source)
        if missing:
            errors.append("production core omits witness codes: " + ", ".join(missing))
    return errors


def independent_validate_benchmark_artifact(evidence: Mapping[str, Any]) -> list[str]:
    """Cold validator separate from ``benchmark_operational.validate_evidence``."""

    errors: list[str] = []
    try:
        if evidence["schema_version"] != 1:
            errors.append("schema version must equal one")
        workload = evidence["workload"]
        if workload["name"] != "categorical_1m_4_unequal_v1":
            errors.append("workload name mismatch")
        if workload["counts"] != FROZEN_COUNTS:
            errors.append("frozen counts mismatch")
        if workload["total_items"] != TOTAL_ITEMS or sum(workload["counts"].values()) != TOTAL_ITEMS:
            errors.append("million-item total mismatch")
        if workload["positive_categories"] != 4 or any(value <= 0 for value in workload["counts"].values()):
            errors.append("workload must have four positive categories")
        if evidence["thresholds"] != {
            "wall_seconds_strict_max": MAX_SECONDS,
            "peak_rss_bytes_max": MAX_RSS_BYTES,
        }:
            errors.append("performance thresholds were weakened")
        result = evidence["result"]
        expected_counts = [FROZEN_COUNTS[name] for name in sorted(FROZEN_COUNTS)]
        if result["output_positions"] != TOTAL_ITEMS:
            errors.append("not every output position was consumed")
        if result["emitted_counts"] != expected_counts:
            errors.append("emitted category counts mismatch")
        digest = result["order_sha256"]
        if not isinstance(digest, str) or len(digest) != 64:
            errors.append("SHA-256 digest is malformed")
        else:
            try:
                bytes.fromhex(digest)
            except ValueError:
                errors.append("SHA-256 digest is not hexadecimal")
        if result["digest_encoding"] != "uint32-big-endian-category-code-v1":
            errors.append("digest encoding mismatch")
        if result["validation_errors"] != []:
            errors.append("worker recorded validation errors")
        if not Fraction(0) <= Fraction(result["max_discrepancy"]) < 1:
            errors.append("categorical discrepancy does not satisfy strict one bound")
        lower = Fraction(result["lower_bound"])
        if not Fraction(1, 3) <= lower <= Fraction(1, 2):
            errors.append("categorical lower bound is outside the theorem range")
        performance = evidence["performance"]
        wall = performance["wall_seconds"]
        rss = performance["peak_rss_bytes"]
        wall_ok = isinstance(wall, (int, float)) and not isinstance(wall, bool) and 0 <= wall < MAX_SECONDS
        rss_ok = isinstance(rss, int) and not isinstance(rss, bool) and 0 < rss <= MAX_RSS_BYTES
        if not wall_ok:
            errors.append("fresh-subprocess strict wall-time gate failed")
        if not rss_ok:
            errors.append("OS peak-RSS gate failed")
        expected_gates = {
            "output_complete": result["output_positions"] == TOTAL_ITEMS,
            "independent_validation": result["validation_errors"] == [],
            "wall_time": wall_ok,
            "peak_rss": rss_ok,
        }
        if evidence["gates"] != expected_gates:
            errors.append("reported pass booleans are inconsistent with measurements")
        if evidence.get("all_gates_passed") is not True:
            errors.append("benchmark did not report all frozen gates passed")
    except (KeyError, TypeError, ValueError, ZeroDivisionError) as exc:
        errors.append(f"invalid operational benchmark artifact: {exc}")
    return errors


def independent_validate_constrained_artifact(evidence: Mapping[str, Any]) -> list[str]:
    """Cold-check the million sparse-constraint evidence and frozen boundary."""

    errors: list[str] = []
    try:
        workload = evidence["workload"]
        if evidence["schema_version"] != 1:
            errors.append("schema version must equal one")
        if workload["name"] != "categorical_1m_sparse_constraints_v1":
            errors.append("constrained workload name mismatch")
        if workload["counts"] != FROZEN_COUNTS or workload["total_items"] != TOTAL_ITEMS:
            errors.append("constrained frozen inventory mismatch")
        constraints = workload["constraints"]
        if constraints != FROZEN_CONSTRAINTS:
            errors.append("exact frozen constraint payload mismatch")
        if (
            len(constraints["fixed_blocks"]) != 1
            or len(constraints["pinned_prefix"]) != 4
            or len(constraints["pinned_suffix"]) != 2
            or len(constraints["precedence"]) != 1
        ):
            errors.append("not every frozen constraint class is present")
        canonical_constraints = hashlib.sha256(
            json.dumps(constraints, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        if canonical_constraints != FROZEN_CONSTRAINTS_SHA256:
            errors.append("constraint payload differs from independent literal digest")
        if workload["constraint_sha256"] != FROZEN_CONSTRAINTS_SHA256:
            errors.append("constraint digest is not the independently frozen digest")
        if evidence["thresholds"] != {
            "wall_seconds_strict_max": MAX_SECONDS,
            "peak_rss_bytes_max": MAX_RSS_BYTES,
        }:
            errors.append("constrained performance thresholds were weakened")
        result = evidence["result"]
        if result["output_positions"] != TOTAL_ITEMS:
            errors.append("constrained output is incomplete")
        if result["emitted_counts"] != [FROZEN_COUNTS[name] for name in sorted(FROZEN_COUNTS)]:
            errors.append("constrained emitted inventory mismatch")
        if result["constraint_sha256"] != FROZEN_CONSTRAINTS_SHA256:
            errors.append("result constraint digest mismatch")
        if result["order_sha256"] != FROZEN_CONSTRAINED_ORDER_SHA256:
            errors.append("frozen constrained order digest mismatch")
        if result["unconstrained_order_sha256"] != FROZEN_UNCONSTRAINED_ORDER_SHA256:
            errors.append("frozen unconstrained order digest mismatch")
        for field, expected in FROZEN_CONSTRAINED_RESULT_FIELDS.items():
            if result[field] != expected:
                errors.append(f"frozen constrained result field {field} mismatch")
        if result["order_sha256"] == result["unconstrained_order_sha256"]:
            errors.append("constraints did not change the order")
        if result["validation_errors"] != []:
            errors.append("constrained worker recorded validation errors")
        upper = Fraction(result["max_discrepancy"])
        lower = Fraction(result["lower_bound"])
        if not Fraction(0) <= lower <= upper:
            errors.append("constrained interval does not satisfy 0 <= L <= U")
        if Fraction(result["additive_gap"]) != upper - lower:
            errors.append("constrained additive gap mismatch")
        ratio = result["ratio_bound"]
        if (None if lower == 0 else Fraction(ratio)) != (None if lower == 0 else upper / lower):
            errors.append("constrained ratio mismatch")
        expected_verified = {
            "fixed_blocks": 1,
            "pinned_prefix_items": 4,
            "pinned_suffix_items": 2,
            "precedence_edges": 1,
        }
        if result["verified_constraints"] != expected_verified:
            errors.append("constrained verification counts mismatch")
        wall = evidence["performance"]["wall_seconds"]
        rss = evidence["performance"]["peak_rss_bytes"]
        wall_ok = isinstance(wall, (int, float)) and not isinstance(wall, bool) and 0 <= wall < MAX_SECONDS
        rss_ok = isinstance(rss, int) and not isinstance(rss, bool) and 0 < rss <= MAX_RSS_BYTES
        expected_gates = {
            "output_complete": result["output_positions"] == TOTAL_ITEMS,
            "independent_validation": result["validation_errors"] == [],
            "all_constraint_classes": result["verified_constraints"] == expected_verified,
            "wall_time": wall_ok,
            "peak_rss": rss_ok,
        }
        if evidence["gates"] != expected_gates:
            errors.append("constrained gate booleans disagree with measurements")
        if evidence.get("all_gates_passed") is not True:
            errors.append("constrained benchmark did not pass every gate")
    except (KeyError, TypeError, ValueError, ZeroDivisionError) as exc:
        errors.append(f"invalid constrained benchmark artifact: {exc}")
    return errors


def _run(command: list[str]) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONHASHSEED"] = "0"
    env["PYTHONPATH"] = str(SRC) + (
        os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else ""
    )
    return subprocess.run(
        command,
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def main() -> int:
    baseline_sources = source_hashes()
    baseline_caches = cache_paths()
    errors: list[str] = []

    static_errors = static_check()
    if static_errors:
        errors.extend(f"static: {error}" for error in static_errors)
    print(f"static gate: {'PASS' if not static_errors else 'FAIL'}")

    javascript = _run(["node", "--check", "web/app.js"])
    if javascript.returncode:
        errors.append(
            f"browser JavaScript syntax check failed\n{javascript.stdout}\n{javascript.stderr}"
        )
    print(
        "browser JavaScript syntax gate: "
        f"{'PASS' if javascript.returncode == 0 else 'FAIL'}"
    )

    unit = _run(
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            "tests",
            "-p",
            "test_*.py",
            "-v",
        ]
    )
    if unit.returncode:
        errors.append(f"operational unit suite failed\n{unit.stdout}\n{unit.stderr}")
    print(f"operational unit/oracle gate: {'PASS' if unit.returncode == 0 else 'FAIL'}")

    benchmark = _run([sys.executable, "benchmark_operational.py"])
    if benchmark.returncode:
        errors.append(
            f"operational benchmark process failed\n{benchmark.stdout}\n{benchmark.stderr}"
        )
        evidence = None
    else:
        try:
            evidence = json.loads(benchmark.stdout)
        except json.JSONDecodeError as exc:
            evidence = None
            errors.append(f"operational benchmark emitted invalid JSON: {exc}")
    benchmark_errors = (
        ["benchmark evidence unavailable"]
        if evidence is None
        else independent_validate_benchmark_artifact(evidence)
    )
    errors.extend(f"benchmark: {error}" for error in benchmark_errors)
    print(f"million-item subprocess gate: {'PASS' if not benchmark_errors else 'FAIL'}")
    if evidence is not None:
        print(
            "  positions={positions} wall={wall:.6f}s rss={rss} digest={digest}".format(
                positions=evidence["result"]["output_positions"],
                wall=evidence["performance"]["wall_seconds"],
                rss=evidence["performance"]["peak_rss_bytes"],
                digest=evidence["result"]["order_sha256"],
            )
        )

    constrained_benchmark = _run([sys.executable, "benchmark_constrained_operational.py"])
    if constrained_benchmark.returncode:
        errors.append(
            "constrained operational benchmark process failed\n"
            + constrained_benchmark.stdout
            + "\n"
            + constrained_benchmark.stderr
        )
        constrained_evidence = None
    else:
        try:
            constrained_evidence = json.loads(constrained_benchmark.stdout)
        except json.JSONDecodeError as exc:
            constrained_evidence = None
            errors.append(f"constrained benchmark emitted invalid JSON: {exc}")
    constrained_errors = (
        ["constrained benchmark evidence unavailable"]
        if constrained_evidence is None
        else independent_validate_constrained_artifact(constrained_evidence)
    )
    errors.extend(f"constrained benchmark: {error}" for error in constrained_errors)
    print(
        "million-item sparse-constraint gate: "
        f"{'PASS' if not constrained_errors else 'FAIL'}"
    )
    if constrained_evidence is not None:
        print(
            "  positions={positions} wall={wall:.6f}s rss={rss} digest={digest}".format(
                positions=constrained_evidence["result"]["output_positions"],
                wall=constrained_evidence["performance"]["wall_seconds"],
                rss=constrained_evidence["performance"]["peak_rss_bytes"],
                digest=constrained_evidence["result"]["order_sha256"],
            )
        )

    original = _run([sys.executable, "verify_all.py"])
    if original.returncode:
        errors.append(f"original verifier failed\n{original.stdout}\n{original.stderr}")
    print(f"original verify_all regression gate: {'PASS' if original.returncode == 0 else 'FAIL'}")

    changed_sources = source_changes(baseline_sources, source_hashes())
    if changed_sources:
        errors.append("source mutation during verification: " + ", ".join(changed_sources))
    print(f"source-mutation gate: {'PASS' if not changed_sources else 'FAIL'}")

    created_caches = new_cache_paths(baseline_caches, cache_paths())
    if created_caches:
        errors.append("cache files created: " + ", ".join(sorted(created_caches)))
    print(f"cache-mutation gate: {'PASS' if not created_caches else 'FAIL'}")

    if errors:
        print("\nOPERATIONAL VERIFICATION FAILED", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("OPERATIONAL VERIFICATION PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
