#!/usr/bin/env python3
"""Adversarial regressions for the q=8 Schur contour repair."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import random

from flint import acb, acb_mat, arb, ctx

import q8_contour_helpers as helper
import q8_r3b_engine as engine
import q8_schur_contour as contour


class Q8SchurContourRepairTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        ctx.prec = contour.PRECISION_BITS

    def test_complex_modulus_enclosure_contains_referee_endpoint_counterexample(self) -> None:
        segment = helper.closed_boundary_segments(
            arb(contour.PIN_RE),
            arb(contour.PIN_IM),
            arb(contour.HALF_WIDTH),
            arb(contour.HALF_WIDTH),
            1,
        )[0]
        midpoint = (segment["start"] + segment["end"]) / acb(2)
        radius = ((segment["end"] - segment["start"]).abs_upper() / arb(2)).upper()
        s_arc = contour.segment_box(segment["start"], segment["end"])
        midpoint_values, midpoint_derivatives = (
            engine.build_q8_block_matrices_and_s_derivative(
                midpoint, 2, contour.SIGN, contour.N_HEAD, engine.EXACT_FACTORS
            )
        )
        endpoint_values, endpoint_derivatives = (
            engine.build_q8_block_matrices_and_s_derivative(
                segment["end"], 2, contour.SIGN, contour.N_HEAD, engine.EXACT_FACTORS
            )
        )
        arc_values, arc_derivatives = engine.build_q8_block_matrices_and_s_derivative(
            s_arc, 2, contour.SIGN, contour.N_HEAD, engine.EXACT_FACTORS
        )
        midpoint_c, _ = contour.schur_value_and_derivative(
            midpoint_values, midpoint_derivatives
        )
        endpoint_c, _ = contour.schur_value_and_derivative(
            endpoint_values, endpoint_derivatives
        )
        _, arc_cprime = contour.schur_value_and_derivative(arc_values, arc_derivatives)
        endpoint_displacement = endpoint_c[0, 0] - midpoint_c[0, 0]
        bound = (radius * arc_cprime[0, 0].abs_upper()).upper()

        old_pure_imaginary = acb(0, bound)
        self.assertFalse(
            old_pure_imaginary.real.contains(endpoint_displacement.real),
            "the adversarial fixture must reproduce the referee's excluded real displacement",
        )
        self.assertTrue(
            contour.complex_modulus_enclosure(bound).contains(endpoint_displacement)
        )

    def test_f1024_geometry_and_all_source_hashes_are_bound(self) -> None:
        bounds = contour.load_operator_bounds(
            contour.DEFAULT_R2, contour.DEFAULT_TB, contour.DEFAULT_W, 2
        )
        self.assertEqual(bounds["factor_strings"], ["10", "4", "2"])
        self.assertTrue(bounds["geometry_verified"])
        self.assertTrue(all(bounds["source_hashes_verified"].values()))

        with tempfile.TemporaryDirectory() as directory:
            tampered_r2 = Path(directory) / contour.DEFAULT_R2.name
            tampered_r2.write_text(
                contour.DEFAULT_R2.read_text(encoding="utf-8") + " ", encoding="utf-8"
            )
            with self.assertRaisesRegex(ValueError, "immutable R2 receipt hash"):
                contour.load_operator_bounds(
                    tampered_r2, contour.DEFAULT_TB, contour.DEFAULT_W, 2
                )

    def test_recorded_tail_check_publishes_both_directions_and_gates_on_the_consumed_one(self) -> None:
        bounds = contour.load_operator_bounds(
            contour.DEFAULT_R2, contour.DEFAULT_TB, contour.DEFAULT_W, 2
        )
        check = bounds["recorded_tail_checks"]["256"]
        # The recorded R2 label does NOT cover this checker's own recomputation;
        # that computed fact is still published verbatim.
        self.assertEqual(check["source_upper_covers_recomputed_upper"], "False")
        # The checker consumes its own recomputation, so the conservative
        # direction -- and the one the gate names -- is that ours dominates.
        self.assertEqual(check["recomputed_upper_covers_source_upper"], "True")
        self.assertTrue(bounds["recorded_tail_checks_pass"])
        self.assertIn("recomputed.upper() >= source.upper()",
                      bounds["recorded_tail_checks_predicate"])
        # The disagreement must stay a rounding-order artefact, not a blow-up.
        self.assertTrue(
            arb(check["relative_gap_upper"]).upper() < arb("1e-15"),
            check["relative_gap_upper"],
        )

    def test_missing_output_projection_tail_forces_open_full_homotopy(self) -> None:
        bounds = contour.load_operator_bounds(
            contour.DEFAULT_R2, contour.DEFAULT_TB, contour.DEFAULT_W, 2
        )
        self.assertIsNone(bounds["full_tau"])
        self.assertFalse(bounds["full_tail_certified"])
        self.assertIn("output", bounds["full_tail_open_reason"].lower())
        self.assertGreater(bounds["input_tail_only"].upper(), arb(0))

    def test_tampered_lout_receipt_is_refused_by_hash(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            tampered = Path(directory) / contour.DEFAULT_LOUT.name
            tampered.write_text(
                contour.DEFAULT_LOUT.read_text(encoding="utf-8") + " ", encoding="utf-8"
            )
            with self.assertRaisesRegex(ValueError, "immutable L-OUT receipt hash"):
                contour.load_operator_bounds(
                    contour.DEFAULT_R2, contour.DEFAULT_TB, contour.DEFAULT_W, 2, tampered
                )

    def test_full_tail_certified_is_computed_at_the_target_boundary(self) -> None:
        # N=237 misses the 1e-15 target, N=238 is the first N that meets it, and
        # the pinned default N=262 carries margin.  Nothing here is hand-set.
        below = contour.load_operator_bounds(
            contour.DEFAULT_R2, contour.DEFAULT_TB, contour.DEFAULT_W, 237,
            contour.DEFAULT_LOUT,
        )
        self.assertFalse(below["full_tau_target_met"])
        self.assertFalse(below["full_tail_certified"])
        self.assertTrue(below["lout"]["gates_pass"])
        self.assertIn("target_met=False", below["full_tail_open_reason"])

        first = contour.load_operator_bounds(
            contour.DEFAULT_R2, contour.DEFAULT_TB, contour.DEFAULT_W, 238,
            contour.DEFAULT_LOUT,
        )
        self.assertTrue(first["full_tau_target_met"])
        self.assertTrue(first["full_tail_certified"])

        default = contour.load_operator_bounds(
            contour.DEFAULT_R2, contour.DEFAULT_TB, contour.DEFAULT_W,
            contour.DEFAULT_N, contour.DEFAULT_LOUT,
        )
        self.assertEqual(contour.DEFAULT_N, 262)
        self.assertTrue(default["full_tail_certified"])
        self.assertIsNone(default["full_tail_open_reason"])
        # full_tau = input_tail_only + output_projection_tail, both telescoped.
        self.assertTrue(
            default["full_tau"].upper()
            >= (default["input_tail_only"] + default["output_projection_tail"]).lower()
        )
        # The output side dominates by many orders at this N.
        self.assertTrue(
            default["input_tail_only"].upper() < default["output_projection_tail"].lower()
        )

    def test_lout_admissibility_gate_failure_blocks_the_verdict(self) -> None:
        payload = json.loads(contour.DEFAULT_LOUT.read_text(encoding="utf-8"))
        payload["theta_exact_strings"] = ["1.000", "1.000", "1.000"]
        with tempfile.TemporaryDirectory() as directory:
            forged = Path(directory) / contour.DEFAULT_LOUT.name
            forged.write_text(json.dumps(payload), encoding="utf-8")
            original = contour.PINNED_LOUT_SHA256
            try:
                contour.PINNED_LOUT_SHA256 = contour.sha256(forged)
                bounds = contour.load_operator_bounds(
                    contour.DEFAULT_R2, contour.DEFAULT_TB, contour.DEFAULT_W,
                    contour.DEFAULT_N, forged,
                )
            finally:
                contour.PINNED_LOUT_SHA256 = original
        gates = bounds["lout"]["gates"]
        self.assertFalse(gates["theta_strictly_greater_than_one"])
        self.assertFalse(bounds["lout"]["gates_pass"])
        self.assertFalse(bounds["full_tail_certified"])
        self.assertIn("lout_gates_pass=False", bounds["full_tail_open_reason"])

    def test_lout_rho_theta_is_reproduced_by_the_checkers_own_mobius(self) -> None:
        bounds = contour.load_operator_bounds(
            contour.DEFAULT_R2, contour.DEFAULT_TB, contour.DEFAULT_W, 2,
            contour.DEFAULT_LOUT,
        )
        audit = bounds["lout"]["rho_audit"]
        self.assertEqual(len(audit), 8)
        for label, row in audit.items():
            self.assertTrue(row["recorded_dominates_checker_mobius"], label)
            self.assertTrue(row["recorded_rho_theta_lt_1"], label)

    def test_checkpoint_boxes_are_reconstructed_from_final_ordered_records(self) -> None:
        records = [
            {
                "initial_arc": 1,
                "path": [],
                "status": "PASS",
                "finite_taylor_box": contour.acb_text(acb(2, 3)),
            },
            {
                "initial_arc": 0,
                "path": [],
                "status": "PASS",
                "finite_taylor_box": contour.acb_text(acb(1, 2)),
            },
        ]
        ordered, boxes = contour.ordered_records_and_boxes(records)
        self.assertEqual([record["initial_arc"] for record in ordered], [0, 1])
        self.assertEqual(len(boxes), 2)
        self.assertTrue(boxes[0].contains(acb(1, 2)))
        self.assertTrue(boxes[1].contains(acb(2, 3)))

    def test_checkpoint_with_incomplete_adaptive_cover_is_refused(self) -> None:
        params = {"arc_start": 0, "arc_end": 1}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "incomplete.json"
            path.write_text(
                json.dumps(
                    {
                        "schema": contour.CHECKPOINT_SCHEMA,
                        "params": params,
                        "completed_initial_arcs": [0],
                        "records": [
                            {
                                "initial_arc": 0,
                                "path": [0],
                                "status": "OPEN_MAX_DEPTH",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "exact partition"):
                contour.load_checkpoint(path, params)

    def test_checkpoint_parameters_bind_actual_checker_bytes(self) -> None:
        params = contour.checkpoint_parameters(2, 1, 0, 0, 4)
        actual = contour.sha256(Path(contour.__file__).resolve())
        self.assertEqual(params["checker_sha256"], actual)
        self.assertEqual(len(params["checker_sha256"]), 64)

        forged_params = dict(params)
        forged_params["checker_sha256"] = "0" * 64
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "wrong-checker.json"
            path.write_text(
                json.dumps(
                    {
                        "schema": contour.CHECKPOINT_SCHEMA,
                        "params": forged_params,
                        "completed_initial_arcs": [],
                        "records": [],
                    }
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "checkpoint schema/parameters"):
                contour.load_checkpoint(path, params)

    def test_forged_pass_boxes_that_wind_are_recomputed_and_rejected(self) -> None:
        segments = helper.closed_boundary_segments(
            arb(contour.PIN_RE),
            arb(contour.PIN_IM),
            arb(contour.HALF_WIDTH),
            arb(contour.HALF_WIDTH),
            1,
        )
        for segment in segments:
            segment["initial_arc"] = segment["arc_index"]
            segment["path"] = []

        radius = arb("0.6")
        forged_boxes = [
            acb(arb(1, radius), arb(0, radius)),
            acb(arb(0, radius), arb(1, radius)),
            acb(arb(-1, radius), arb(0, radius)),
            acb(arb(0, radius), arb(-1, radius)),
        ]
        forged_winding, _ = helper.certified_winding_from_arc_boxes(forged_boxes)
        self.assertEqual(forged_winding, 1)
        forged_records = [
            {
                "initial_arc": initial,
                "path": [],
                "status": "PASS",
                "finite_taylor_box": contour.acb_text(box),
            }
            for initial, box in enumerate(forged_boxes)
        ]
        bounds = contour.load_operator_bounds(
            contour.DEFAULT_R2, contour.DEFAULT_TB, contour.DEFAULT_W, 2
        )
        with self.assertRaisesRegex(ValueError, "did not recompute to PASS"):
            contour.recompute_saved_pass_records(forged_records, segments, 2, bounds)

    def test_v1_checkpoint_is_conservatively_refused(self) -> None:
        params = {"N": 2}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "old.json"
            path.write_text(
                json.dumps(
                    {
                        "schema": "q8-schur-contour-checkpoint/v1",
                        "params": params,
                        "completed_initial_arcs": [],
                        "records": [],
                    }
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "checkpoint schema"):
                contour.load_checkpoint(path, params)


class Q8OperatorNormGateTests(unittest.TestCase):
    """The tightened arc gate must bound the same object and fail closed."""

    @classmethod
    def setUpClass(cls) -> None:
        ctx.prec = contour.PRECISION_BITS

    @staticmethod
    def _random_matrix(size: int, rng: random.Random, radius: float = 0.0) -> acb_mat:
        matrix = acb_mat(size, size)
        for row in range(size):
            for col in range(size):
                matrix[row, col] = acb(
                    arb(rng.uniform(-1.0, 1.0), radius),
                    arb(rng.uniform(-1.0, 1.0), radius),
                )
        return matrix

    def test_operator_bound_never_exceeds_frobenius_on_random_instances(self) -> None:
        rng = random.Random(20260820)
        for size in (1, 2, 3, 5, 9, 17):
            for trial in range(4):
                matrix = self._random_matrix(size, rng, radius=0.0 if trial % 2 else 0.05)
                bound, components = contour.operator_norm_upper(matrix, size)
                frobenius = components["frobenius"]
                self.assertIsNotNone(frobenius)
                self.assertLessEqual(
                    bound.upper(),
                    frobenius.upper(),
                    f"tightened bound exceeded Frobenius at size {size}",
                )
                self.assertTrue(contour.definitely_positive(bound) or size == 0)

    def test_operator_bound_dominates_every_realised_vector_gain(self) -> None:
        """Soundness: ||A x||_2 <= bound * ||x||_2 for every sampled point/vector."""

        rng = random.Random(31415)
        for size in (2, 4, 8):
            matrix = self._random_matrix(size, rng, radius=0.01)
            bound, _components = contour.operator_norm_upper(matrix, size)
            point = acb_mat(size, size)
            for row in range(size):
                for col in range(size):
                    entry = matrix[row, col]
                    point[row, col] = acb(entry.real.upper(), entry.imag.lower())
            for _ in range(20):
                vector = [
                    acb(arb(rng.uniform(-1.0, 1.0)), arb(rng.uniform(-1.0, 1.0)))
                    for _ in range(size)
                ]
                norm_in = arb(0)
                for value in vector:
                    norm_in += value.abs_upper() ** 2
                norm_out = arb(0)
                for row in range(size):
                    image = acb(0)
                    for col in range(size):
                        image += point[row, col] * vector[col]
                    norm_out += image.abs_lower() ** 2
                self.assertLessEqual(
                    norm_out.sqrt().lower(),
                    (bound * norm_in.sqrt().upper()).upper(),
                    "operator bound under-shot a realised vector gain",
                )

    def test_weighted_schur_beats_frobenius_on_a_diagonal_matrix(self) -> None:
        """The tightening is real where Frobenius is genuinely lossy."""

        size = 12
        matrix = acb_mat(size, size)
        for index in range(size):
            matrix[index, index] = acb(1)
        bound, components = contour.operator_norm_upper(matrix, size)
        self.assertGreater(float(components["frobenius"].upper()), 3.4)
        self.assertLess(float(bound), 1.0001)
        self.assertGreaterEqual(float(bound), 1.0)

    def test_schur_test_refuses_non_positive_weights(self) -> None:
        absolute = [[arb(1), arb(1)], [arb(1), arb(1)]]
        self.assertIsNone(
            contour.schur_test_upper(absolute, [arb(1), arb(0)], [arb(1), arb(1)])
        )
        with self.assertRaisesRegex(ValueError, "weights must match"):
            contour.schur_test_upper(absolute, [arb(1)], [arb(1), arb(1)])

    def test_arc_gate_fails_closed_when_the_tightened_bound_exceeds_one(self) -> None:
        """qOp >= 1 must abort the arc before any determinant box is emitted."""

        segment = helper.closed_boundary_segments(
            arb(contour.PIN_RE),
            arb(contour.PIN_IM),
            arb(contour.HALF_WIDTH),
            arb(contour.HALF_WIDTH),
            1,
        )[0]
        segment = dict(segment, initial_arc=segment["arc_index"], path=[])
        bounds = contour.load_operator_bounds(
            contour.DEFAULT_R2, contour.DEFAULT_TB, contour.DEFAULT_W, 32, contour.DEFAULT_LOUT
        )
        record, box = contour.arc_certificate(32, segment, bounds)
        self.assertGreater(float(arb(record["qOp_upper"])), 1.0)
        self.assertFalse(record["qOp_lt_1"])
        self.assertEqual(record["status"], "FAIL_QOP")
        self.assertEqual(box, acb(0))
        self.assertNotIn("finite_taylor_box", record)
        # both numbers are published; the old one stays for audit
        self.assertLessEqual(
            arb(record["qOp_upper"]).upper(), arb(record["qF_upper"]).upper()
        )
        self.assertEqual(
            set(record["qOp_components"]),
            {"frobenius", "schur_unweighted", "schur_weighted"},
        )


if __name__ == "__main__":
    unittest.main()
