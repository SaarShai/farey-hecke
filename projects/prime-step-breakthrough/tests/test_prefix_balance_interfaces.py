from __future__ import annotations

import io
import json
import os
import subprocess
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from unittest import mock
from fractions import Fraction
from http.server import ThreadingHTTPServer
from pathlib import Path
from types import SimpleNamespace

import coprimebatch
from coprimebatch.prefix_balance import BalanceItem, BalanceProblem, quota_order, solve_exact
from coprimebatch.web import (
    CONSTRAINED_QUOTA_BLOCK_WIDTH_CAP,
    CONSTRAINED_QUOTA_CATEGORY_CAP,
    CONSTRAINED_QUOTA_CONSTRAINT_REFERENCE_CAP,
    CONSTRAINED_QUOTA_EXACT_METRIC_CELL_CAP,
    FULL_ORDER_ITEM_CAP,
    Handler,
    RequestError,
    _body,
    _loopback_host,
    api_response,
    balance_response,
    serve,
)


ROOT = Path(__file__).resolve().parents[1]


def _fraction(payload: dict[str, object] | None) -> Fraction | None:
    return None if payload is None else Fraction(str(payload["fraction"]))


class PrefixBalanceInterfaceTests(unittest.TestCase):
    @staticmethod
    def _cli(*arguments: str) -> tuple[int, str, str]:
        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        env["PYTHONPATH"] = str(ROOT / "src") + os.pathsep + env.get("PYTHONPATH", "")
        completed = subprocess.run(
            [sys.executable, "-m", "coprimebatch.cli", *arguments],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
            timeout=60,
        )
        return completed.returncode, completed.stdout, completed.stderr

    @staticmethod
    def _compact_constraints() -> dict[str, object]:
        return {
            "fixed_blocks": [
                {
                    "block_id": "middle",
                    "occurrences": [
                        {"category": "B", "occurrence": 1},
                        {"category": "A", "occurrence": 2},
                    ],
                }
            ],
            "pinned_prefix": [{"category": "A", "occurrence": 1}],
            "pinned_suffix": [{"category": "B", "occurrence": 2}],
            "precedence": [
                {
                    "edge_id": "prefix-before-suffix",
                    "before": {"category": "A", "occurrence": 1},
                    "after": {"category": "B", "occurrence": 2},
                }
            ],
        }

    def test_public_python_api_exports_balance_contract(self) -> None:
        for name in (
            "BalanceItem",
            "BalanceProblem",
            "QuotaResult",
            "OrderingResult",
            "quota_order",
            "quota_mechanical_order",
            "solve_exact",
            "solve_constrained",
            "verify_order",
            "verify_quota_result",
            "OccurrenceRef",
            "FixedOccurrenceBlock",
            "OccurrencePrecedence",
            "CategoricalConstraintProblem",
            "ConstrainedQuotaResult",
            "solve_constrained_quota",
            "verify_constrained_quota",
        ):
            self.assertTrue(hasattr(coprimebatch, name), name)

    def test_quota_python_cli_and_api_semantics_match(self) -> None:
        expected = quota_order({"B": 3, "A": 2, "empty": 0})
        request = {"mode": "quota", "counts": {"B": 3, "A": 2, "empty": 0}}
        api = api_response("/api/balance", request)
        code, stdout, stderr = self._cli(
            "balance", "B=3", "A=2", "empty=0", "--mode", "quota", "--json"
        )
        self.assertEqual((code, stderr), (0, ""))
        cli = json.loads(stdout)
        self.assertEqual(cli, api)
        self.assertEqual(api["schema_version"], "prefix-balance-api-v1")
        self.assertEqual(api["inventory"]["categories"], list(expected.categories))
        self.assertEqual(api["inventory"]["counts"], list(expected.counts))
        self.assertEqual(_fraction(api["metrics"]["max_discrepancy"]), expected.max_discrepancy)
        self.assertEqual(_fraction(api["metrics"]["lower_bound"]), expected.lower_bound)
        self.assertEqual(api["guarantee"]["scope"], "unconstrained_categorical")
        self.assertEqual(api["guarantee"]["strict_factor"], 3)
        self.assertFalse(api["order"]["included"])
        self.assertNotIn("codes", api["order"])
        self.assertEqual(api["order"]["sha256"], expected.order_sha256)

    def test_binary_mode_preserves_named_category_codebook_and_is_exact(self) -> None:
        response = balance_response(
            {"mode": "binary", "counts": {"zeta": 4, "alpha": 1}, "full_order": True}
        )
        self.assertEqual(response["inventory"]["categories"], ["alpha", "zeta"])
        self.assertEqual(response["inventory"]["counts"], [1, 4])
        self.assertEqual(response["order"]["codes"], [1, 1, 0, 1, 1])
        self.assertTrue(response["guarantee"]["exact_optimum"])
        self.assertEqual(response["guarantee"]["scope"], "exact_binary")
        self.assertIsNone(response["guarantee"]["strict_factor"])

    def test_constrained_quota_http_cli_parity_and_ranked_full_order(self) -> None:
        request = {
            "mode": "constrained-quota",
            "counts": {"B": 2, "A": 2},
            "constraints": self._compact_constraints(),
            "full_order": True,
        }
        response = balance_response(request)
        self.assertEqual(response["mode"], "constrained-quota")
        self.assertEqual(response["inventory"]["categories"], ["A", "B"])
        self.assertEqual(response["inventory"]["counts"], [2, 2])
        self.assertEqual(
            response["order"]["occurrences"],
            [
                {"category": "A", "occurrence": 1},
                {"category": "B", "occurrence": 1},
                {"category": "A", "occurrence": 2},
                {"category": "B", "occurrence": 2},
            ],
        )
        self.assertEqual(
            response["order"]["preview"],
            {"head": response["order"]["occurrences"], "tail": []},
        )
        self.assertEqual(
            response["order"]["digest_encoding"],
            "uint32-big-endian-category-code-v1",
        )
        self.assertEqual(
            response["guarantee"]["scope"],
            "constrained_categorical_a_posteriori",
        )
        self.assertIn("primary_optimum_proved", response["guarantee"])
        self.assertNotIn("exact_optimum", response["guarantee"])
        self.assertEqual(
            response["guarantee"]["proved_objective"], "primary_B_only"
        )
        self.assertEqual(
            response["guarantee"]["comparison_set"],
            "all interleavings of fixed within-category occurrence queues satisfying the declared blocks, exact end pins, and precedence edges",
        )
        self.assertIsNone(response["guarantee"]["strict_factor"])
        self.assertTrue(any("factor-three" in item for item in response["warnings"]))
        self.assertTrue(any("primary B" in item for item in response["warnings"]))

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "constraints.json"
            path.write_text(json.dumps(self._compact_constraints()), encoding="utf-8")
            code, stdout, stderr = self._cli(
                "balance",
                "B=2",
                "A=2",
                "--mode",
                "constrained-quota",
                "--constraints-json",
                str(path),
                "--full-order",
                "--json",
            )
        self.assertEqual((code, stderr), (0, ""))
        self.assertEqual(json.loads(stdout), response)

    def test_constrained_quota_compact_preview_has_occurrence_ranks(self) -> None:
        response = balance_response(
            {
                "mode": "constrained-quota",
                "counts": {"A": 10, "B": 10},
                "constraints": {
                    "fixed_blocks": [],
                    "pinned_prefix": [],
                    "pinned_suffix": [],
                    "precedence": [],
                },
            }
        )
        preview = response["order"]["preview"]
        self.assertEqual((len(preview["head"]), len(preview["tail"])), (8, 8))
        for occurrence in preview["head"] + preview["tail"]:
            self.assertEqual(set(occurrence), {"category", "occurrence"})
            self.assertIn(occurrence["category"], {"A", "B"})
            self.assertGreaterEqual(occurrence["occurrence"], 1)
            self.assertLessEqual(occurrence["occurrence"], 10)
        self.assertNotIn("occurrences", response["order"])

    def test_exact_problem_rational_strings_matches_python_core(self) -> None:
        supplied = {
            "items": [
                {"item_id": "g1", "contribution": ["1/2"]},
                {"item_id": "g2", "contribution": ["1/6"]},
                {"item_id": "g3", "contribution": ["1/3"]},
            ],
            "precedence": [["g2", "g3"]],
        }
        problem = BalanceProblem(
            items=(
                BalanceItem("g1", (Fraction(1, 2),)),
                BalanceItem("g2", (Fraction(1, 6),)),
                BalanceItem("g3", (Fraction(1, 3),)),
            ),
            precedence=(("g2", "g3"),),
        )
        expected = solve_exact(problem)
        response = api_response(
            "/api/balance",
            {"mode": "exact", "problem": supplied, "full_order": True},
        )
        self.assertEqual(response["order"]["item_ids"], list(expected.order))
        self.assertEqual(_fraction(response["metrics"]["max_discrepancy"]), expected.max_discrepancy)
        self.assertEqual(
            _fraction(response["metrics"]["accumulated_discrepancy"]),
            expected.accumulated_discrepancy,
        )
        self.assertTrue(response["guarantee"]["exact_optimum"])
        self.assertEqual(_fraction(response["metrics"]["additive_gap"]), 0)

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "problem.json"
            path.write_text(json.dumps(supplied), encoding="utf-8")
            code, stdout, stderr = self._cli(
                "balance", "--mode", "exact", "--problem-json", str(path), "--full-order", "--json"
            )
        self.assertEqual((code, stderr), (0, ""))
        self.assertEqual(json.loads(stdout), response)

    def test_constrained_mode_reports_only_a_posteriori_guarantee(self) -> None:
        problem = {
            "items": [
                {"item_id": "a", "contribution": [0]},
                {"item_id": "b", "contribution": [1]},
                {"item_id": "c", "contribution": [2]},
            ],
            "pinned_prefix": ["a"],
            "precedence": [["b", "c"]],
        }
        response = api_response(
            "/api/balance", {"mode": "constrained", "problem": problem, "full_order": True}
        )
        self.assertEqual(response["order"]["item_ids"], ["a", "b", "c"])
        self.assertTrue(response["guarantee"]["exact_optimum"])
        self.assertEqual(response["guarantee"]["scope"], "constrained_a_posteriori")
        self.assertIsNone(response["guarantee"]["strict_factor"])
        self.assertFalse(response["explanation"]["categorical_factor_inherited"])

    def test_application_presets_are_allowlisted_and_compact(self) -> None:
        response = api_response(
            "/api/balance", {"mode": "quota", "preset": "rendering-progressive-joint-cells"}
        )
        self.assertEqual(response["application"]["preset_id"], "rendering-progressive-joint-cells")
        self.assertEqual(response["inventory"]["total_items"], 4096)
        self.assertFalse(response["order"]["included"])
        self.assertNotIn("codes", response["order"])
        with self.assertRaises(RequestError):
            api_response("/api/balance", {"mode": "quota", "preset": "not-a-preset"})

    def test_million_item_response_remains_compact(self) -> None:
        response = balance_response(
            {"mode": "quota", "counts": {"a": 250_000, "b": 750_000}}
        )
        self.assertEqual(response["inventory"]["total_items"], 1_000_000)
        self.assertLess(len(json.dumps(response)), 10_000)
        self.assertNotIn("codes", response["order"])
        self.assertEqual(len(response["order"]["preview"]["head"]), 8)
        self.assertEqual(len(response["order"]["preview"]["tail"]), 8)

    def test_million_item_constrained_response_remains_compact(self) -> None:
        response = balance_response(
            {
                "mode": "constrained-quota",
                "counts": {"A": 400_000, "B": 300_000, "C": 200_000, "D": 100_000},
                "constraints": {
                    "fixed_blocks": [
                        {
                            "block_id": "bootstrap",
                            "occurrences": [
                                {"category": "A", "occurrence": 1},
                                {"category": "B", "occurrence": 1},
                            ],
                        }
                    ],
                    "pinned_prefix": [{"category": "C", "occurrence": 1}],
                    "pinned_suffix": [{"category": "D", "occurrence": 100_000}],
                    "precedence": [
                        {
                            "edge_id": "A2-before-C2",
                            "before": {"category": "A", "occurrence": 2},
                            "after": {"category": "C", "occurrence": 2},
                        }
                    ],
                },
            }
        )
        self.assertEqual(response["order"]["total_items"], 1_000_000)
        self.assertLess(len(json.dumps(response)), 10_000)
        self.assertFalse(response["order"]["included"])
        self.assertNotIn("occurrences", response["order"])
        self.assertEqual(len(response["order"]["preview"]["head"]), 8)
        self.assertEqual(len(response["order"]["preview"]["tail"]), 8)
        self.assertEqual(
            response["order"]["preview"]["tail"][-1],
            {"category": "D", "occurrence": 100_000},
        )
        self.assertEqual(
            response["guarantee"]["scope"],
            "constrained_categorical_a_posteriori",
        )

    def test_full_order_hard_cap_is_enforced(self) -> None:
        with mock.patch("coprimebatch.web.quota_order") as constructor:
            with self.assertRaisesRegex(RequestError, str(FULL_ORDER_ITEM_CAP)):
                balance_response(
                    {
                        "mode": "quota",
                        "counts": {"a": FULL_ORDER_ITEM_CAP + 1},
                        "full_order": True,
                    }
                )
            constructor.assert_not_called()

    def test_constrained_quota_resource_caps_run_before_constructor(self) -> None:
        high_category_counts = {
            f"c{index:03d}": int(index == 0)
            for index in range(CONSTRAINED_QUOTA_CATEGORY_CAP + 1)
        }
        metric_counts = {
            "a": CONSTRAINED_QUOTA_EXACT_METRIC_CELL_CAP // 4,
            "b": CONSTRAINED_QUOTA_EXACT_METRIC_CELL_CAP // 4 + 1,
        }
        too_many_refs = [
            {"category": "a", "occurrence": 1}
        ] * (CONSTRAINED_QUOTA_CONSTRAINT_REFERENCE_CAP + 1)
        wide_block = {
            "block_id": "too-wide",
            "occurrences": [
                {"category": "a", "occurrence": occurrence}
                for occurrence in range(1, CONSTRAINED_QUOTA_BLOCK_WIDTH_CAP + 2)
            ],
        }
        cases = (
            (
                {
                    "mode": "constrained-quota",
                    "counts": high_category_counts,
                    "constraints": {},
                },
                str(CONSTRAINED_QUOTA_CATEGORY_CAP),
            ),
            (
                {
                    "mode": "constrained-quota",
                    "counts": metric_counts,
                    "constraints": {},
                },
                str(CONSTRAINED_QUOTA_EXACT_METRIC_CELL_CAP),
            ),
            (
                {
                    "mode": "constrained-quota",
                    "counts": {"a": 1},
                    "constraints": {"pinned_prefix": too_many_refs},
                },
                str(CONSTRAINED_QUOTA_CONSTRAINT_REFERENCE_CAP),
            ),
            (
                {
                    "mode": "constrained-quota",
                    "counts": {"a": CONSTRAINED_QUOTA_BLOCK_WIDTH_CAP + 1},
                    "constraints": {"fixed_blocks": [wide_block]},
                },
                str(CONSTRAINED_QUOTA_BLOCK_WIDTH_CAP),
            ),
        )
        with mock.patch("coprimebatch.web.solve_constrained_quota") as constructor:
            for payload, message in cases:
                with self.subTest(message=message), self.assertRaisesRegex(
                    RequestError, message
                ):
                    balance_response(payload)
            with self.assertRaisesRegex(
                RequestError, str(CONSTRAINED_QUOTA_CATEGORY_CAP)
            ):
                api_response("/api/balance", cases[0][0])
            constructor.assert_not_called()
        with mock.patch("coprimebatch.web.solve_constrained_quota") as constructor:
            with self.assertRaisesRegex(RequestError, str(FULL_ORDER_ITEM_CAP)):
                balance_response(
                    {
                        "mode": "constrained-quota",
                        "counts": {"a": FULL_ORDER_ITEM_CAP + 1},
                        "constraints": {},
                        "full_order": True,
                    }
                )
            constructor.assert_not_called()

    def test_invalid_balance_payloads_are_rejected(self) -> None:
        invalid = (
            {},
            {"mode": "unknown", "counts": {"a": 1}},
            {"mode": "quota", "counts": {"a": True}},
            {"mode": "quota", "counts": {"a": 1.0}},
            {"mode": "quota", "counts": {"a": 1}, "extra": 2},
            {"mode": "quota", "counts": {"a": 1}, "problem": {"items": []}},
            {"mode": "exact", "counts": {"a": 1}},
            {"mode": "quota", "problem": {"items": []}},
            {"mode": "binary", "counts": {"a": 1}},
            {
                "mode": "exact",
                "problem": {"items": [{"item_id": "x", "contribution": [0.5]}]},
            },
            {
                "mode": "exact",
                "problem": {"items": [{"item_id": "x", "contribution": [True]}]},
            },
            {
                "mode": "exact",
                "problem": {"items": [{"item_id": "x", "contribution": ["bad"]}]},
            },
            {
                "mode": "exact",
                "problem": {"items": [{"item_id": "x", "contribution": ["1e100000"]}]},
            },
            {"mode": "quota", "counts": {"x" * 257: 1}},
            {"mode": "quota", "counts": {"a": 1}, "full_order": 1},
            {"mode": "constrained-quota", "counts": {"a": 1}},
            {
                "mode": "constrained-quota",
                "counts": {"a": 1},
                "constraints": {},
                "preset": "rendering-progressive-joint-cells",
            },
            {"mode": "quota", "counts": {"a": 1}, "constraints": {}},
            {
                "mode": "constrained-quota",
                "counts": {"a": 1},
                "constraints": {"unknown": []},
            },
            {
                "mode": "constrained-quota",
                "counts": {"a": 1},
                "constraints": {
                    "pinned_prefix": [{"category": "a", "occurrence": 0}]
                },
            },
            {
                "mode": "constrained-quota",
                "counts": {"a": 1},
                "constraints": {
                    "fixed_blocks": [
                        {"block_id": "x", "items": []}
                    ]
                },
            },
        )
        for payload in invalid:
            with self.subTest(payload=payload), self.assertRaises(RequestError):
                balance_response(payload)

    def test_body_rejects_negative_and_oversized_content_length(self) -> None:
        for length, message in (("-1", "negative"), ("1000001", "too large")):
            request = SimpleNamespace(headers={"Content-Length": length}, rfile=io.BytesIO(b"{}"))
            with self.subTest(length=length), self.assertRaisesRegex(RequestError, message):
                _body(request)

        duplicate = b'{"counts":{"A":1,"A":2}}'
        request = SimpleNamespace(
            headers={"Content-Length": str(len(duplicate))},
            rfile=io.BytesIO(duplicate),
        )
        with self.assertRaisesRegex(RequestError, "duplicate JSON object key"):
            _body(request)

    def test_browser_count_parser_is_prototype_safe_and_claim_scoped(self) -> None:
        script = (ROOT / "web" / "app.js").read_text()
        markup = (ROOT / "web" / "index.html").read_text()
        self.assertIn("Object.create(null)", script)
        self.assertIn('mode: "constrained-quota"', script)
        self.assertIn("balance-fixed-blocks", markup)
        self.assertIn("balance-pinned-prefix", markup)
        self.assertIn("balance-pinned-suffix", markup)
        self.assertIn("balance-precedence", markup)
        self.assertIn("1-based rank", markup)
        self.assertIn("constraints can destroy the unconstrained factor below 3", markup)
        self.assertIn("Primary <var>B</var> optimum proved", markup)
        self.assertNotIn("Exact optimum", markup)
        self.assertIn("guarantee.primary_optimum_proved", script)
        self.assertNotIn("innerHTML", script)
        self.assertNotIn("rendering can improve progressive prefixes", markup)

    def test_cli_rejects_duplicate_json_keys(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "duplicate.json"
            path.write_text(
                '{"items":[{"item_id":"a","item_id":"b","contribution":[0]}]}',
                encoding="utf-8",
            )
            code, stdout, stderr = self._cli(
                "balance", "--mode", "exact", "--problem-json", str(path), "--json"
            )
        self.assertEqual(code, 2)
        self.assertEqual(stdout, "")
        self.assertIn("duplicate JSON object key", stderr)

    def test_constraints_cli_preserves_mode_and_input_size_guards(self) -> None:
        code, stdout, stderr = self._cli(
            "balance", "A=1", "--mode", "constrained-quota", "--json"
        )
        self.assertEqual(code, 2)
        self.assertEqual(stdout, "")
        self.assertIn("--constraints-json", stderr)

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "too-large.json"
            path.write_bytes(b"{" + b" " * 1_000_000 + b"}")
            code, stdout, stderr = self._cli(
                "balance",
                "A=1",
                "--mode",
                "constrained-quota",
                "--constraints-json",
                str(path),
                "--json",
            )
        self.assertEqual(code, 2)
        self.assertEqual(stdout, "")
        self.assertIn("1000000 UTF-8 bytes", stderr)

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "duplicate-constraints.json"
            path.write_text(
                '{"pinned_prefix":[{"category":"A","category":"B","occurrence":1}]}',
                encoding="utf-8",
            )
            code, stdout, stderr = self._cli(
                "balance",
                "A=1",
                "--mode",
                "constrained-quota",
                "--constraints-json",
                str(path),
                "--json",
            )
        self.assertEqual(code, 2)
        self.assertEqual(stdout, "")
        self.assertIn("duplicate JSON object key", stderr)

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "empty-constraints.json"
            path.write_text("{}", encoding="utf-8")
            counts = [
                f"c{index:03d}={int(index == 0)}"
                for index in range(CONSTRAINED_QUOTA_CATEGORY_CAP + 1)
            ]
            code, stdout, stderr = self._cli(
                "balance",
                *counts,
                "--mode",
                "constrained-quota",
                "--constraints-json",
                str(path),
                "--json",
            )
        self.assertEqual(code, 2)
        self.assertEqual(stdout, "")
        self.assertIn(str(CONSTRAINED_QUOTA_CATEGORY_CAP), stderr)

    def test_http_infeasibility_includes_structured_witness(self) -> None:
        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            host, port = server.server_address
            payload = {
                "mode": "exact",
                "problem": {
                    "items": [
                        {"item_id": "a", "contribution": [0]},
                        {"item_id": "b", "contribution": [1]},
                    ],
                    "precedence": [["a", "b"], ["b", "a"]],
                },
            }
            request = urllib.request.Request(
                f"http://{host}:{port}/api/balance",
                data=json.dumps(payload).encode("utf-8"),
                method="POST",
                headers={"Content-Type": "application/json"},
            )
            with self.assertRaises(urllib.error.HTTPError) as raised:
                urllib.request.urlopen(request, timeout=10)
            with raised.exception as error:
                body = json.loads(error.read().decode("utf-8"))
            self.assertEqual(raised.exception.code, 400)
            self.assertEqual(body["status"], 400)
            self.assertEqual(body["witness"]["code"], "CONTRACTED_DAG_CYCLE")
            self.assertIsInstance(body["witness"]["message"], str)
            self.assertIsInstance(body["witness"]["details"], dict)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)

    def test_research_server_rejects_non_loopback_bind_before_socket_open(self) -> None:
        for host in ("127.0.0.1", "localhost", "::1"):
            self.assertEqual(_loopback_host(host), host)
        with mock.patch("coprimebatch.web.ThreadingHTTPServer") as server:
            with self.assertRaisesRegex(ValueError, "explicit loopback"):
                serve("0.0.0.0", 0)
            server.assert_not_called()

    def test_cli_reports_invalid_count_without_traceback(self) -> None:
        code, stdout, stderr = self._cli("balance", "a=1.5", "--json")
        self.assertEqual(code, 2)
        self.assertEqual(stdout, "")
        self.assertIn("error:", stderr)
        self.assertNotIn("Traceback", stderr)


if __name__ == "__main__":
    unittest.main()
