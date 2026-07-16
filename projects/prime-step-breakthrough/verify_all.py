#!/usr/bin/env python3
"""Run static, unit, HTTP, benchmark, artifact, and cache-integrity gates."""

from __future__ import annotations

import ast
import hashlib
import json
import math
import os
import subprocess
import sys
from pathlib import Path
from fractions import Fraction
from typing import Any, Iterable


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parent
ARTIFACTS = ROOT / "artifacts"
BENCHMARK_ARTIFACT = ARTIFACTS / "benchmark.json"
CACHE_DIR_NAMES = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
GARCIA_LOWER_BOUND_CONSTANT = Fraction(9, 160)
GARCIA_LOWER_BOUND_CONSTANT_SQUARED = GARCIA_LOWER_BOUND_CONSTANT**2
GAP_EXACT_CORPUS = {
    2: (Fraction(1, 3), Fraction(2, 3)),
    3: (Fraction(1, 2), Fraction(1, 3), Fraction(1, 6)),
    4: (Fraction(1, 8), Fraction(1, 8), Fraction(3, 8), Fraction(3, 8)),
    5: tuple(Fraction(k, 15) for k in range(1, 6)),
    6: (Fraction(0), *(Fraction(k, 15) for k in range(1, 6))),
    7: tuple(Fraction(k, 28) for k in range(1, 8)),
    8: (Fraction(1, 16),) * 4 + (Fraction(3, 16),) * 4,
}
ZERO_VARIANCE_GAPS = (Fraction(1, 8),) * 8


def cache_paths(root: Path = ROOT) -> set[str]:
    found: set[str] = set()
    if not root.exists():
        return found
    for path in root.rglob("*"):
        if path.name in CACHE_DIR_NAMES or path.suffix in {".pyc", ".pyo"}:
            found.add(path.relative_to(root).as_posix())
    return found


def new_cache_paths(before: Iterable[str], after: Iterable[str]) -> set[str]:
    return set(after) - set(before)


def permutation_enumeration_calls(source: str) -> list[int]:
    """Return lines that call a permutation enumerator in production code."""

    tree = ast.parse(source)
    lines = []
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


def exact_mean_absolute_sum_from_prefix_subsets(
    gaps: tuple[Fraction, ...],
) -> tuple[Fraction, int]:
    """Independent exact permutation mean via labelled prefix subsets."""

    n = len(gaps)
    deviations = tuple(gap - Fraction(1, n) for gap in gaps)
    total = Fraction(0)
    states = 0
    for mask in range(1, (1 << n) - 1):
        size = mask.bit_count()
        centered_sum = sum(
            (deviations[index] for index in range(n) if mask & (1 << index)),
            Fraction(0),
        )
        total += abs(centered_sum) / math.comb(n, size)
        states += 1
    return total, states


def _source_hashes(root: Path = ROOT) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if relative.parts and relative.parts[0] == "artifacts":
            continue
        if any(part in CACHE_DIR_NAMES for part in relative.parts):
            continue
        if path.suffix in {".pyc", ".pyo"}:
            continue
        hashes[relative.as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return hashes


def static_check(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    python_files = sorted(
        path
        for path in root.rglob("*.py")
        if "artifacts" not in path.relative_to(root).parts
        and not any(part in CACHE_DIR_NAMES for part in path.relative_to(root).parts)
    )
    if not python_files:
        return ["no Python files found"]
    for path in python_files:
        try:
            ast.parse(path.read_text(), filename=str(path))
        except (OSError, SyntaxError, UnicodeError) as exc:
            errors.append(f"{path.relative_to(root)}: {exc}")
    required = {
        root / "benchmark.py",
        root / "verify_all.py",
        root / "tests" / "oracles.py",
        root / "tests" / "test_gap_permutation.py",
    }
    for path in sorted(required):
        if not path.is_file():
            errors.append(f"missing required verifier file: {path.relative_to(root)}")
    gap_module = root / "src" / "coprimebatch" / "gap_permutation.py"
    if not gap_module.is_file():
        errors.append("missing T5 production module: src/coprimebatch/gap_permutation.py")
    else:
        calls = permutation_enumeration_calls(gap_module.read_text())
        if calls:
            errors.append(
                "T5 production code enumerates permutations at lines "
                + ", ".join(str(line) for line in calls)
            )
    return errors


def validate_benchmark_artifact_data(evidence: dict[str, Any]) -> list[str]:
    """Independent artifact validator; does not import ``benchmark.py``."""

    errors: list[str] = []
    try:
        if evidence["schema_version"] != 3:
            errors.append("schema_version must equal 3")
        optimizer = evidence["optimizer"]
        optimizer_controls = evidence["optimizer_controls"]
        scaling = evidence["scaling"]
        divisor = scaling["divisor_portfolio_2_20"]
        prefactored = scaling["raw_vs_prefactored_high_bit"]
        negative = evidence["negative_controls"]
        gap_evidence = evidence["gap_permutation"]
        t2 = evidence["t2_empirical_evidence"]
        gates = evidence["gates"]

        expected_parameters = {
            "start": 2,
            "stop": 200,
            "layers": 10,
            "seed": 20260715,
        }
        if optimizer["parameters"] != expected_parameters:
            errors.append("frozen optimizer parameters mismatch")
        metadata = optimizer["constraint_metadata"]
        if metadata["exact_layer_count"] != 10:
            errors.append("exact layer count metadata mismatch")
        if metadata["denominator_cap"] != 200:
            errors.append("denominator cap metadata mismatch")
        if metadata["seed"] != 20260715:
            errors.append("optimizer seed metadata mismatch")
        if not metadata["greedy_tie_break"]:
            errors.append("greedy tie-break metadata missing")
        if not metadata["random_sampling"]:
            errors.append("random sampling law metadata missing")
        if len(optimizer["greedy"]["denominators"]) != 10:
            errors.append("greedy portfolio does not contain ten layers")
        if optimizer["baselines"]["random"]["samples"] != 500:
            errors.append("random baseline must contain 500 samples")
        if not optimizer["deterministic"]:
            errors.append("optimizer is not deterministic")

        deterministic_ratio = float(optimizer["ratios"]["to_best_deterministic"])
        random_ratio = float(optimizer["ratios"]["to_random_median"])
        if deterministic_ratio > 0.75:
            errors.append("optimizer deterministic-baseline ratio exceeds frozen 0.75")
        if random_ratio > 0.80:
            errors.append("optimizer random-median ratio exceeds frozen 0.80")
        matrix = optimizer_controls["small_instance_matrix"]
        if len(matrix["cases"]) != 21:
            errors.append("fixed small-instance matrix must contain 21 cases")
        worst = matrix["worst_case"]
        if worst["candidates"] != list(range(2, 10)) or worst["layers"] != 5:
            errors.append("worst small case must be candidates 2..9/k=5")
        if abs(worst["optimality_gap_ratio"] - 1.0708404486680856) > 1e-12:
            errors.append("known approximately 7.084% greedy loss was not retained")
        if any(case["optimality_gap_ratio"] < 1.0 - 1e-15 for case in matrix["cases"]):
            errors.append("small matrix reports greedy below brute-force optimum")

        midpoint = optimizer_controls["same_point_midpoint"]
        prime = optimizer_controls["admissible_prime_1597"]
        if midpoint["rho"] < 1.0 - 1e-15:
            errors.append("rho < 1 is a normalization failure")
        expected_rho = midpoint["optimized_worst_case_error"] / midpoint["worst_case_error"]
        if abs(midpoint["rho"] - expected_rho) > 1e-12:
            errors.append("rho does not equal the same-point midpoint loss ratio")
        if not midpoint["optimizer_loses"]:
            errors.append("midpoint negative-control loss was hidden")
        if not prime["same_point_count"] or prime["point_count"] != midpoint["point_count"]:
            errors.append("S={1597} is not compared at the same point count")
        if not prime["optimizer_loses"]:
            errors.append("admissible S={1597} loss was hidden")

        expected_denominators = [2**power for power in range(1, 21)]
        if divisor["denominators"] != expected_denominators:
            errors.append("scaling case is not the full divisor portfolio of 2^20")
        if divisor["implicit_points"] != 2**20 - 1:
            errors.append("2^20 divisor portfolio point count mismatch")
        if divisor["materialized_points"] != 0:
            errors.append("scaling run materialized nodes")
        if divisor["points_not_materialized"] != divisor["implicit_points"]:
            errors.append("avoided-enumeration count mismatch")
        for key in ("factorization_seconds", "kernel_seconds", "total_seconds"):
            if not isinstance(divisor[key], (int, float)) or divisor[key] < 0:
                errors.append(f"scaling divisor case {key} must be nonnegative")
        if divisor["total_seconds"] >= 1.0:
            errors.append("scaling wall time does not satisfy the strict one-second gate")
        if not prefactored["exact_values_match"]:
            errors.append("raw and prefactored certificate values differ")
        if prefactored["prefactored"]["factorization_seconds"] != 0.0:
            errors.append("complete supplied factor map performed raw factorization")
        if prefactored["timing_is_evidence_not_a_speed_gate"] is not True:
            errors.append("prefactor timing was incorrectly promoted to a strict speed gate")

        cases = negative["kernel_mismatched_functions"]["cases"]
        if not cases:
            errors.append("kernel-mismatched negative controls are missing")
        if not negative["kernel_mismatched_functions"]["losses_retained"]:
            errors.append("negative-control losses were filtered")
        for case in cases:
            if "optimizer_loses" not in case or "winner" not in case:
                errors.append("negative-control case lacks an honest loss/winner field")
        if "optimizer_loses" not in negative["uniform_grid"]:
            errors.append("uniform-grid reference lacks optimizer_loses")

        bound_contract = gap_evidence["l1_bound_contract"]
        input_contract = gap_evidence["input_contract"]
        exact_constant_square = Fraction(
            bound_contract["rigorous_lower_constant_squared_exact"]
        )
        binary64_constant = float(
            bound_contract["rigorous_lower_constant_binary64"]
        )
        if bound_contract["rigorous_lower_constant_expression"] != "9/160":
            errors.append("García lower-bound constant expression must equal 9/160")
        if exact_constant_square != GARCIA_LOWER_BOUND_CONSTANT_SQUARED:
            errors.append("García exact lower-bound constant square mismatch")
        if (
            not math.isfinite(binary64_constant)
            or binary64_constant <= 0.0
            or Fraction.from_float(binary64_constant) > GARCIA_LOWER_BOUND_CONSTANT
            or Fraction.from_float(math.nextafter(binary64_constant, math.inf))
            <= GARCIA_LOWER_BOUND_CONSTANT
        ):
            errors.append("García binary64 lower constant is not tightly rounded down")
        if input_contract != {"minimum_gap_count": 2, "singleton_supported": False}:
            errors.append("gap singleton/minimum-count contract mismatch")

        exact_records = gap_evidence["exact_corpus"]
        if [record["n"] for record in exact_records] != list(range(2, 9)):
            errors.append("T5 exact corpus must cover N=2..8")
        for record in exact_records:
            if tuple(Fraction(value) for value in record["gaps"]) != GAP_EXACT_CORPUS[
                record["n"]
            ]:
                errors.append(f"N={record['n']} frozen rational gap corpus changed")
        if tuple(
            Fraction(value)
            for value in gap_evidence["zero_variance_case"]["gaps"]
        ) != ZERO_VARIANCE_GAPS:
            errors.append("frozen zero-variance rational gap corpus changed")
        for record in (*exact_records, gap_evidence["zero_variance_case"]):
            n = record["n"]
            gap_values = tuple(Fraction(value) for value in record["gaps"])
            deviations = tuple(
                Fraction(value) for value in record["centered_deviations"]
            )
            if len(gap_values) != n or sum(gap_values, Fraction(0)) != 1:
                errors.append(f"N={n} rational gap corpus is malformed")
            if deviations != tuple(
                gap - Fraction(1, n) for gap in gap_values
            ) or sum(deviations, Fraction(0)) != 0:
                errors.append(f"N={n} rational deviation corpus is not exact zero-sum")
            exact_mean, subset_states = exact_mean_absolute_sum_from_prefix_subsets(
                gap_values
            )
            if Fraction(record["exact_mean_absolute_sum"]) != exact_mean:
                errors.append(f"N={n} exact permutation absolute mean mismatch")
            if record["labelled_subset_states_evaluated"] != subset_states:
                errors.append(f"N={n} subset-state evidence count mismatch")
            lower = Fraction.from_float(float(record["rigorous_l1_lower_bound"]))
            upper = Fraction.from_float(float(record["l1_upper_bound_sum"]))
            lower_passed = lower <= exact_mean
            upper_passed = exact_mean <= upper
            if record["lower_bound_passed"] is not lower_passed:
                errors.append(f"N={n} stored lower-bound verdict mismatch")
            if record["upper_bound_passed"] is not upper_passed:
                errors.append(f"N={n} stored upper-bound verdict mismatch")
            if record["two_sided_l1_bound_passed"] is not (
                lower_passed and upper_passed
            ):
                errors.append(f"N={n} stored two-sided bound verdict mismatch")
            if not lower_passed:
                errors.append(f"N={n} exact permutation mean is below rigorous lower")
            if not upper_passed:
                errors.append(f"N={n} exact permutation mean exceeds finite upper")
            variance = Fraction(record["gap_variance"])
            if lower**2 > exact_constant_square * variance * n**3:
                errors.append(f"N={n} rigorous lower was not rounded conservatively")
            if record["rigorous_l1_lower_bound_constant"] != binary64_constant:
                errors.append(f"N={n} lower-bound constant differs from contract")
            if record["labelled_permutations_avoided"] != math.factorial(record["n"]):
                errors.append(f"N={record['n']} labelled work-avoided count mismatch")
            if not record["exact_metric_types"]:
                errors.append(f"N={record['n']} exact arithmetic missing")
            if record["distinct_permutations"] is None:
                errors.append(f"N={record['n']} exact distinct count missing")
        zero_variance = gap_evidence["zero_variance_case"]
        if (
            zero_variance["n"] != 8
            or Fraction(zero_variance["gap_variance"]) != 0
            or Fraction(zero_variance["exact_mean_absolute_sum"]) != 0
            or zero_variance["rigorous_l1_lower_bound"] != 0.0
            or zero_variance["l1_upper_bound_sum"] != 0.0
        ):
            errors.append("zero-variance two-sided L1 evidence mismatch")
        farey = gap_evidence["farey_example"]
        if farey["order"] != 5:
            errors.append("fixed Farey example missing")
        if sum((Fraction(gap) for gap in farey["gaps"]), Fraction(0)) != 1:
            errors.append("Farey gaps do not sum exactly to one")
        million = gap_evidence["million_gap"]
        if million["gap_count"] < 1_000_000:
            errors.append("million-gap case is too small")
        if not million["exact_metric_types"]:
            errors.append("million-gap case did not exercise exact arithmetic")
        if million["distinct_permutations"] is not None:
            errors.append("million-gap case computed a prohibited exact factorial count")
        if not math.isfinite(million["log10_distinct_permutations"]):
            errors.append("million-gap log10 distinct count is not finite")
        if million["permutations_materialized"] != 0:
            errors.append("million-gap case enumerated permutations")
        if t2["is_theorem_gate"] is not False:
            errors.append("T2 empirical evidence was promoted to a theorem gate")

        frozen_gate_fields = {
            "optimizer_vs_best_deterministic": ("maximum", 0.75),
            "optimizer_vs_random_median": ("maximum", 0.80),
            "scaling_point_count": ("minimum", 1_000_000),
            "scaling_wall_time": ("maximum_seconds", 1.0),
            "rho_normalization": ("minimum", 1.0),
            "gap_million_exact_path": ("minimum_gaps", 1_000_000),
        }
        for gate_name, (field, frozen_value) in frozen_gate_fields.items():
            if gates[gate_name][field] != frozen_value:
                errors.append(f"frozen threshold changed: {gate_name}.{field}")
        two_sided_gate = gates["gap_l1_two_sided_bounds"]
        if (
            Fraction(two_sided_gate["constant_squared_exact"])
            != GARCIA_LOWER_BOUND_CONSTANT_SQUARED
            or two_sided_gate["corpus_n_min"] != 2
            or two_sided_gate["corpus_n_max"] != 8
        ):
            errors.append("frozen two-sided García gate metadata changed")

        recomputed: dict[str, bool] = {
            "optimizer_deterministic": bool(optimizer["deterministic"]),
            "optimizer_vs_best_deterministic": deterministic_ratio <= 0.75,
            "optimizer_vs_random_median": random_ratio <= 0.80,
            "small_instance_truth": all(
                case["optimality_gap_ratio"] >= 1.0 - 1e-15
                for case in matrix["cases"]
            )
            and abs(worst["optimality_gap_ratio"] - 1.0708404486680856) <= 1e-12,
            "scaling_point_count": divisor["implicit_points"] == 2**20 - 1,
            "scaling_wall_time": divisor["total_seconds"] < 1.0,
            "rho_normalization": midpoint["rho"] >= 1.0 - 1e-15,
            "negative_controls_retained": bool(
                negative["kernel_mismatched_functions"]["losses_retained"]
                and cases
                and midpoint["optimizer_loses"]
                and prime["optimizer_loses"]
            ),
            "prefactored_value_parity": bool(prefactored["exact_values_match"])
            and prefactored["prefactored"]["factorization_seconds"] == 0.0,
            "gap_exact_corpus": [record["n"] for record in exact_records]
            == list(range(2, 9))
            and all(record["exact_metric_types"] for record in exact_records),
            "gap_l1_two_sided_bounds": all(
                record["two_sided_l1_bound_passed"] for record in exact_records
            )
            and zero_variance["two_sided_l1_bound_passed"]
            and Fraction(zero_variance["gap_variance"]) == 0
            and zero_variance["rigorous_l1_lower_bound"] == 0.0
            and zero_variance["l1_upper_bound_sum"] == 0.0,
            "gap_farey_example": farey["order"] == 5
            and sum((Fraction(gap) for gap in farey["gaps"]), Fraction(0)) == 1,
            "gap_million_exact_path": million["gap_count"] >= 1_000_000
            and million["exact_metric_types"]
            and million["distinct_permutations"] is None
            and math.isfinite(million["log10_distinct_permutations"])
            and million["permutations_materialized"] == 0,
        }
        for gate_name, expected in recomputed.items():
            if gates[gate_name]["passed"] is not expected:
                errors.append(f"stored gate verdict mismatch: {gate_name}")
        if evidence["all_gates_passed"] is not all(recomputed.values()):
            errors.append("all_gates_passed mismatch")
    except (KeyError, TypeError, ValueError, OverflowError) as exc:
        errors.append(f"invalid benchmark artifact schema: {exc}")
    return errors


def validate_benchmark_artifact(path: Path = BENCHMARK_ARTIFACT) -> list[str]:
    try:
        evidence = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot read benchmark artifact: {exc}"]
    if not isinstance(evidence, dict):
        return ["benchmark artifact root must be an object"]
    return validate_benchmark_artifact_data(evidence)


def _run_stage(
    name: str, command: list[str], env: dict[str, str], timeout: int = 240
) -> tuple[str, bool, str]:
    print(f"\n== {name} ==")
    print("$ " + " ".join(command))
    try:
        completed = subprocess.run(
            command,
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        output = f"TIMEOUT after {timeout}s\n{exc.stdout or ''}\n{exc.stderr or ''}".strip()
        print(output)
        return name, False, output
    output = "\n".join(part.rstrip() for part in (completed.stdout, completed.stderr) if part)
    if output:
        print(output)
    passed = completed.returncode == 0
    print(f"[{name}] {'PASS' if passed else 'FAIL'} (exit {completed.returncode})")
    return name, passed, output


def _test_modules() -> tuple[list[str], list[str]]:
    regular: list[str] = []
    http: list[str] = []
    for path in sorted((ROOT / "tests").glob("test*.py")):
        module = f"tests.{path.stem}"
        lowered = path.stem.lower()
        if any(token in lowered for token in ("http", "api", "server")):
            http.append(module)
        else:
            regular.append(module)
    return regular, http


def main() -> int:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONPATH"] = str(ROOT / "src") + os.pathsep + env.get("PYTHONPATH", "")
    before_caches = cache_paths()
    before_hashes = _source_hashes()

    results: list[tuple[str, bool, str]] = []
    static_errors = static_check()
    print("== static checks ==")
    if static_errors:
        print("\n".join(static_errors))
    else:
        print("AST parse and required-file checks passed")
    results.append(("static checks", not static_errors, "\n".join(static_errors)))

    regular_modules, http_modules = _test_modules()
    if regular_modules:
        results.append(
            _run_stage(
                "unit tests",
                [sys.executable, "-m", "unittest", "-v", *regular_modules],
                env,
            )
        )
    else:
        results.append(("unit tests", False, "no regular unittest modules found"))

    if http_modules:
        results.append(
            _run_stage(
                "HTTP tests",
                [sys.executable, "-m", "unittest", "-v", *http_modules],
                env,
            )
        )
    else:
        print("\n== HTTP tests ==\nSKIP: no HTTP test module present")

    results.append(
        _run_stage(
            "benchmark gates",
            [sys.executable, str(ROOT / "benchmark.py"), "--output", str(BENCHMARK_ARTIFACT)],
            env,
        )
    )

    artifact_errors = validate_benchmark_artifact()
    print("\n== benchmark artifact validation ==")
    if artifact_errors:
        print("\n".join(artifact_errors))
    else:
        print(f"PASS: {BENCHMARK_ARTIFACT}")
    results.append(
        ("benchmark artifact validation", not artifact_errors, "\n".join(artifact_errors))
    )

    after_caches = cache_paths()
    cache_delta = sorted(new_cache_paths(before_caches, after_caches))
    if cache_delta:
        cache_message = "new repo cache/bytecode paths: " + ", ".join(cache_delta)
    else:
        cache_message = "no new repo cache/bytecode paths"
    print(f"\n== cache integrity ==\n{cache_message}")
    results.append(("cache integrity", not cache_delta, cache_message))

    after_hashes = _source_hashes()
    mutations = sorted(
        path
        for path in before_hashes.keys() | after_hashes.keys()
        if before_hashes.get(path) != after_hashes.get(path)
    )
    mutation_message = (
        "source tree unchanged outside artifacts"
        if not mutations
        else "source changes during verification: " + ", ".join(mutations)
    )
    print(f"\n== mutation boundary ==\n{mutation_message}")
    results.append(("mutation boundary", not mutations, mutation_message))

    failed = [name for name, passed, _ in results if not passed]
    print("\n== summary ==")
    print(
        json.dumps(
            {
                "passed": not failed,
                "stages_run": [name for name, _, _ in results],
                "failed_stages": failed,
                "benchmark_artifact": str(BENCHMARK_ARTIFACT),
            },
            sort_keys=True,
        )
    )
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
