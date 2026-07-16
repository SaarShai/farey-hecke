from __future__ import annotations

import copy
import dataclasses
import hashlib
import json
import subprocess
import sys
import time
import unittest
from unittest import mock
from array import array
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import benchmark_constrained_operational
import verify_operational
from coprimebatch import prefix_balance as prefix_balance_module
from coprimebatch.prefix_balance import (
    CategoricalConstraintProblem,
    FixedOccurrenceBlock,
    InfeasibleProblemError,
    OccurrencePrecedence,
    OccurrenceRef,
    solve_constrained_quota,
    verify_constrained_quota,
)
from tests.constrained_quota_oracles import (
    canonical_digest,
    constraint_errors,
    exact_metrics,
    exhaustive_optimum,
)


def ref(category: str, occurrence: int) -> OccurrenceRef:
    return OccurrenceRef(category, occurrence)


def all_constraint_problem() -> CategoricalConstraintProblem:
    return CategoricalConstraintProblem(
        {"a": 3, "b": 3, "c": 2},
        fixed_blocks=(
            FixedOccurrenceBlock("block-1", (ref("b", 1), ref("c", 1))),
        ),
        pinned_prefix=(ref("a", 1),),
        pinned_suffix=(ref("b", 3),),
        precedence=(
            OccurrencePrecedence("edge-1", ref("a", 2), ref("c", 2)),
        ),
    )


class CompactConstrainedQuotaTests(unittest.TestCase):
    def assertWitness(self, code: str, problem: CategoricalConstraintProblem) -> None:  # noqa: N802
        with self.assertRaises(InfeasibleProblemError) as caught:
            solve_constrained_quota(problem)
        witness = caught.exception.witness
        self.assertEqual(witness.code, code)
        self.assertTrue(witness.message)
        self.assertIsInstance(witness.details, dict)

    def test_all_constraint_types_are_satisfied_and_metrics_are_exact(self) -> None:
        problem = all_constraint_problem()
        result = solve_constrained_quota(problem)
        report = verify_constrained_quota(problem, result)
        self.assertTrue(report.passed, report.errors)
        codes = tuple(result.order_codes)
        self.assertEqual(constraint_errors(problem, codes), ())
        peak, accumulated, errors = exact_metrics(problem.counts, codes)
        self.assertEqual(errors, ())
        self.assertEqual(result.max_discrepancy, peak)
        self.assertEqual(result.accumulated_discrepancy, accumulated)
        self.assertEqual(result.order_sha256, canonical_digest(codes))
        self.assertEqual(result.additive_gap, result.max_discrepancy - result.lower_bound)
        self.assertEqual(result.guarantee_scope, "constrained_categorical_a_posteriori")
        self.assertIsNone(result.strict_factor)
        self.assertIn("within-category", result.comparison_set)
        self.assertTrue(result.feasibility.get("verified"))

    def test_structured_occurrence_and_graph_witnesses(self) -> None:
        base = {"a": 3, "b": 2}
        fixtures = (
            (
                "OCCURRENCE_OUT_OF_RANGE",
                CategoricalConstraintProblem(
                    base,
                    precedence=(OccurrencePrecedence("bad", ref("a", 4), ref("b", 1)),),
                ),
            ),
            (
                "DUPLICATE_BLOCK_ID",
                CategoricalConstraintProblem(
                    base,
                    fixed_blocks=(
                        FixedOccurrenceBlock("same", (ref("a", 1),)),
                        FixedOccurrenceBlock("same", (ref("b", 1),)),
                    ),
                ),
            ),
            (
                "DUPLICATE_EDGE_ID",
                CategoricalConstraintProblem(
                    base,
                    precedence=(
                        OccurrencePrecedence("same", ref("a", 1), ref("b", 1)),
                        OccurrencePrecedence("same", ref("a", 2), ref("b", 2)),
                    ),
                ),
            ),
            (
                "PIN_SPLITS_BLOCK",
                CategoricalConstraintProblem(
                    base,
                    fixed_blocks=(
                        FixedOccurrenceBlock("pair", (ref("a", 1), ref("b", 1))),
                    ),
                    pinned_prefix=(ref("a", 1),),
                ),
            ),
            (
                "BLOCK_OCCURRENCE_ORDER_CONFLICT",
                CategoricalConstraintProblem(
                    base,
                    fixed_blocks=(
                        FixedOccurrenceBlock(
                            "reversed-a", (ref("a", 2), ref("a", 1))
                        ),
                    ),
                ),
            ),
            (
                "BLOCK_CATEGORY_GAP",
                CategoricalConstraintProblem(
                    base,
                    fixed_blocks=(
                        FixedOccurrenceBlock(
                            "gapped-a", (ref("a", 1), ref("a", 3))
                        ),
                    ),
                ),
            ),
            (
                "CONTRACTED_DAG_CYCLE",
                CategoricalConstraintProblem(
                    base,
                    precedence=(
                        OccurrencePrecedence("ab", ref("a", 1), ref("b", 1)),
                        OccurrencePrecedence("ba", ref("b", 1), ref("a", 1)),
                    ),
                ),
            ),
        )
        for code, problem in fixtures:
            with self.subTest(code=code):
                self.assertWitness(code, problem)

    def test_verifier_rejects_forged_result_fields_and_order(self) -> None:
        problem = all_constraint_problem()
        result = solve_constrained_quota(problem)
        self.assertTrue(verify_constrained_quota(problem, result).passed)
        broken_codes = array("I", result.order_codes)
        broken_codes[0], broken_codes[1] = broken_codes[1], broken_codes[0]
        mutations = (
            dataclasses.replace(result, schema_version="forged"),
            dataclasses.replace(result, algorithm="forged"),
            dataclasses.replace(result, categories=tuple(reversed(result.categories))),
            dataclasses.replace(result, counts=tuple(reversed(result.counts))),
            dataclasses.replace(result, order_sha256="0" * 64),
            dataclasses.replace(result, digest_encoding="forged"),
            dataclasses.replace(result, max_discrepancy=result.max_discrepancy + 1),
            dataclasses.replace(
                result,
                accumulated_discrepancy=result.accumulated_discrepancy + 1,
            ),
            dataclasses.replace(result, lower_bound=result.lower_bound + 1),
            dataclasses.replace(result, ratio_bound=Fraction(1, 100)),
            dataclasses.replace(result, additive_gap=result.additive_gap + 1),
            dataclasses.replace(result, guarantee_scope="unconstrained_categorical"),
            dataclasses.replace(result, comparison_set="forged"),
            dataclasses.replace(result, strict_factor=3),
            dataclasses.replace(
                result,
                primary_optimum_proved=not result.primary_optimum_proved,
            ),
            dataclasses.replace(result, order_codes=broken_codes),
            dataclasses.replace(result, feasibility={"verified": True}),
            dataclasses.replace(result, explanation={"certificate": "forged"}),
        )
        for forged in mutations:
            with self.subTest(forged=forged):
                self.assertFalse(verify_constrained_quota(problem, forged).passed)

    def test_verifier_requires_documented_packed_order_storage(self) -> None:
        problem = all_constraint_problem()
        result = solve_constrained_quota(problem)
        copied = dataclasses.replace(result, order_codes=array("I", result.order_codes))
        self.assertTrue(verify_constrained_quota(problem, copied).passed)
        unsupported = (
            dataclasses.replace(result, order_codes=tuple(result.order_codes)),
            dataclasses.replace(result, order_codes=array("L", result.order_codes)),
        )
        for forged in unsupported:
            with self.subTest(storage=type(forged.order_codes), typecode=getattr(forged.order_codes, "typecode", None)):
                self.assertFalse(verify_constrained_quota(problem, forged).passed)

    def test_tiny_exhaustive_oracle_brackets_the_true_constrained_optimum(self) -> None:
        problems = (
            CategoricalConstraintProblem({"a": 2, "b": 2}),
            CategoricalConstraintProblem(
                {"a": 2, "b": 2},
                pinned_prefix=(ref("a", 1),),
            ),
            CategoricalConstraintProblem(
                {"a": 2, "b": 1, "c": 1},
                fixed_blocks=(
                    FixedOccurrenceBlock("bc", (ref("b", 1), ref("c", 1))),
                ),
                precedence=(
                    OccurrencePrecedence("a-before-c", ref("a", 1), ref("c", 1)),
                ),
            ),
            CategoricalConstraintProblem(
                {"a": 3, "b": 2},
                pinned_suffix=(ref("a", 3), ref("b", 2)),
                precedence=(
                    OccurrencePrecedence("late-a", ref("b", 1), ref("a", 2)),
                ),
            ),
        )
        for problem in problems:
            with self.subTest(problem=problem):
                optimum = exhaustive_optimum(problem)
                self.assertIsNotNone(optimum)
                assert optimum is not None
                result = solve_constrained_quota(problem)
                codes = tuple(result.order_codes)
                peak, accumulated, errors = exact_metrics(problem.counts, codes)
                self.assertEqual(errors, ())
                self.assertEqual(constraint_errors(problem, codes), ())
                self.assertEqual(result.max_discrepancy, peak)
                self.assertEqual(result.accumulated_discrepancy, accumulated)
                self.assertLessEqual(result.lower_bound, optimum.max_discrepancy)
                self.assertLessEqual(optimum.max_discrepancy, result.max_discrepancy)
                if result.lower_bound:
                    self.assertEqual(
                        result.ratio_bound,
                        result.max_discrepancy / result.lower_bound,
                    )
                else:
                    self.assertIsNone(result.ratio_bound)
                if result.primary_optimum_proved:
                    self.assertEqual(result.max_discrepancy, optimum.max_discrepancy)

    def test_closed_interval_proves_primary_B_only_not_lexicographic_B_Q(self) -> None:
        problem = CategoricalConstraintProblem(
            {"a": 3, "b": 3, "c": 2},
            precedence=(
                OccurrencePrecedence("a3-before-b1", ref("a", 3), ref("b", 1)),
            ),
        )
        result = solve_constrained_quota(problem)
        optimum = exhaustive_optimum(problem)
        self.assertIsNotNone(optimum)
        assert optimum is not None
        self.assertTrue(result.primary_optimum_proved)
        self.assertFalse(hasattr(result, "exact_optimum"))
        self.assertEqual(result.max_discrepancy, optimum.max_discrepancy)
        self.assertEqual(result.max_discrepancy, Fraction(3, 2))
        self.assertEqual(result.accumulated_discrepancy, Fraction(53, 8))
        self.assertEqual(optimum.accumulated_discrepancy, Fraction(13, 2))
        self.assertNotEqual(
            result.accumulated_discrepancy, optimum.accumulated_discrepancy
        )
        self.assertEqual(
            result.explanation.get("proved_objective"), "primary_B_only"
        )

    def test_result_mutable_dictionaries_are_freshly_owned(self) -> None:
        problem = all_constraint_problem()
        first = solve_constrained_quota(problem)
        second = solve_constrained_quota(problem)
        self.assertIsNot(first.feasibility, second.feasibility)
        self.assertIsNot(first.explanation, second.explanation)
        first.feasibility["mutated"] = True
        first.explanation["mutated"] = True
        self.assertNotIn("mutated", second.feasibility)
        self.assertNotIn("mutated", second.explanation)

    def test_multi_item_prefix_does_not_leave_a_stale_frontier_entry(self) -> None:
        problem = CategoricalConstraintProblem(
            {"a": 2, "b": 1, "c": 3},
            fixed_blocks=(
                FixedOccurrenceBlock("ab", (ref("a", 1), ref("b", 1))),
            ),
            pinned_prefix=(ref("c", 1), ref("c", 2)),
            pinned_suffix=(ref("a", 2),),
        )
        result = solve_constrained_quota(problem)
        self.assertTrue(verify_constrained_quota(problem, result).passed)
        self.assertEqual(constraint_errors(problem, tuple(result.order_codes)), ())

    def test_mutated_million_constraints_fail_even_with_self_consistent_digest(self) -> None:
        artifact_path = ROOT / "artifacts" / "constrained_operational_benchmark.json"
        evidence = json.loads(artifact_path.read_text(encoding="utf-8"))
        self.assertEqual(benchmark_constrained_operational.validate_evidence(evidence), [])
        self.assertEqual(
            verify_operational.independent_validate_constrained_artifact(evidence), []
        )

        forged = copy.deepcopy(evidence)
        forged_constraints = forged["workload"]["constraints"]
        forged_constraints["precedence"][0]["after"]["occurrence"] += 1
        self_digest = hashlib.sha256(
            json.dumps(
                forged_constraints, sort_keys=True, separators=(",", ":")
            ).encode("utf-8")
        ).hexdigest()
        forged["workload"]["constraint_sha256"] = self_digest
        forged["result"]["constraint_sha256"] = self_digest
        self.assertNotEqual(
            self_digest,
            benchmark_constrained_operational.FROZEN_CONSTRAINTS_SHA256,
        )
        self.assertTrue(benchmark_constrained_operational.validate_evidence(forged))
        self.assertTrue(
            verify_operational.independent_validate_constrained_artifact(forged)
        )

    def test_wide_block_preparation_and_certificate_scaling_canary(self) -> None:
        participants = 5_000
        counts = {f"c{index:04d}": 1 for index in range(participants)}
        problem = CategoricalConstraintProblem(
            counts,
            fixed_blocks=(
                FixedOccurrenceBlock(
                    "wide",
                    tuple(ref(category, 1) for category in counts),
                ),
            ),
        )
        started = time.perf_counter()
        prepared = prefix_balance_module._compact_prepare(problem)
        lower, terms = prefix_balance_module._compact_lower_bound(prepared)
        elapsed = time.perf_counter() - started
        self.assertEqual(lower, max(terms.values()))
        self.assertLess(
            elapsed,
            2.0,
            f"5,000-participant block preparation/certificate took {elapsed:.3f}s",
        )

    def test_million_benchmark_has_hard_timeout_and_memory_sensitive_gate(self) -> None:
        timeout = subprocess.TimeoutExpired(["worker"], 30)
        with mock.patch.object(
            benchmark_constrained_operational.subprocess,
            "run",
            side_effect=timeout,
        ) as patched:
            with self.assertRaisesRegex(RuntimeError, "hard 30s timeout"):
                benchmark_constrained_operational.run_subprocess_benchmark()
        self.assertEqual(
            patched.call_args.kwargs["timeout"],
            benchmark_constrained_operational.MAX_SECONDS,
        )
        self.assertLessEqual(
            benchmark_constrained_operational.MAX_RSS_BYTES,
            128 * 1024 * 1024,
        )


if __name__ == "__main__":
    unittest.main()
