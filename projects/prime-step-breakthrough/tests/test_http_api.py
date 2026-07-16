from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import threading
import time
import unittest
import urllib.error
import urllib.request
from fractions import Fraction
from http import HTTPStatus
from http.server import ThreadingHTTPServer
from math import log2
from pathlib import Path
from typing import Any
from unittest.mock import patch

from coprimebatch.arithmetic import primes_up_to
from coprimebatch.gap_permutation import farey_gaps, gap_permutation_certificate
from coprimebatch.kernel import portfolio_certificate
from coprimebatch.optimizer import benchmark_case
from coprimebatch.shear import farey_shift_moments
from coprimebatch import web
from coprimebatch.web import (
    CERTIFICATE_TRIAL_DIVISION_BUDGET,
    CERTIFICATE_DENOMINATOR_COUNT_CAP,
    CERTIFICATE_DENOMINATOR_BIT_CAP,
    CERTIFICATE_KERNEL_BIT_CELL_CAP,
    CERTIFICATE_OUTPUT_INTEGER_BIT_CAP,
    GAP_FAREY_ORDER_CAP,
    GAP_SUPPLIED_COUNT_CAP,
    GAP_SUPPLIED_COMMON_DENOMINATOR_BIT_CAP,
    GAP_SUPPLIED_EXACT_WORK_BIT_CAP,
    Handler,
    OPTIMIZE_BENCHMARK_SPAN_CAP,
    OPTIMIZE_CANDIDATE_CAP,
    OPTIMIZE_KERNEL_WORK_CELL_CAP,
    OPTIMIZE_SAMPLE_CAP,
    OPTIMIZE_TRIAL_DIVISION_BUDGET,
    SHIFT_MAX_ORDER_CAP,
    SHIFT_PRIME_CAP,
    SOCKET_TIMEOUT_SECONDS,
    _BoundedThreadingHTTPServer,
    _host_is_loopback,
    _origin_is_loopback,
)


ROOT = Path(__file__).resolve().parents[1]
_MISSING = object()


class LiveHttpApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        host, port = cls.server.server_address
        cls.base_url = f"http://{host}:{port}"

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=5)

    @classmethod
    def _request(
        cls,
        method: str,
        path: str,
        payload: object = _MISSING,
        *,
        raw: bytes | None = None,
    ) -> tuple[int, dict[str, Any], str]:
        if raw is not None and payload is not _MISSING:
            raise ValueError("use payload or raw, not both")
        data = raw
        if payload is not _MISSING:
            data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            cls.base_url + path,
            data=data,
            method=method,
            headers={"Content-Type": "application/json"} if data is not None else {},
        )
        try:
            response = urllib.request.urlopen(request, timeout=10)
        except urllib.error.HTTPError as error:
            with error:
                body = error.read().decode("utf-8")
                return error.code, json.loads(body), error.headers.get("Content-Type", "")
        with response:
            body = response.read().decode("utf-8")
            return response.status, json.loads(body), response.headers.get("Content-Type", "")

    @classmethod
    def _raw_get(cls, path: str) -> tuple[int, bytes, str]:
        with urllib.request.urlopen(cls.base_url + path, timeout=10) as response:
            return response.status, response.read(), response.headers.get("Content-Type", "")

    @staticmethod
    def _cli_json(*arguments: str) -> dict[str, Any]:
        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        env["PYTHONPATH"] = str(ROOT / "src") + os.pathsep + env.get("PYTHONPATH", "")
        completed = subprocess.run(
            [sys.executable, "-m", "coprimebatch.cli", *arguments, "--json"],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
            timeout=60,
        )
        if completed.returncode:
            raise AssertionError(completed.stderr or completed.stdout)
        return json.loads(completed.stdout)

    @staticmethod
    def _without_timings(value: Any) -> Any:
        if isinstance(value, dict):
            return {
                key: LiveHttpApiTests._without_timings(item)
                for key, item in value.items()
                if key not in {"factorization_seconds", "kernel_seconds"}
            }
        if isinstance(value, list):
            return [LiveHttpApiTests._without_timings(item) for item in value]
        return value

    def _assert_fraction_payload(
        self, payload: dict[str, Any], expected: Fraction
    ) -> None:
        self.assertTrue(
            {"fraction", "numerator", "denominator", "decimal"} <= payload.keys()
        )
        self.assertEqual(payload["fraction"], str(expected))
        self.assertEqual(Fraction(payload["fraction"]), expected)
        self.assertEqual(payload["numerator"], expected.numerator)
        self.assertEqual(payload["denominator"], expected.denominator)
        self.assertEqual(payload["decimal"], float(expected))

    def test_health_and_static_assets_are_served(self) -> None:
        status, health, content_type = self._request("GET", "/api/health")
        self.assertEqual(status, 200)
        self.assertIn("application/json", content_type)
        self.assertEqual(
            health,
            {"status": "ok", "service": "coprimebatch", "api": "frozen-core-v1"},
        )

        status, page, content_type = self._raw_get("/")
        self.assertEqual(status, 200)
        self.assertIn("text/html", content_type)
        self.assertIn(b"CoprimeBatch Designer", page)
        status, script, content_type = self._raw_get("/app.js")
        self.assertEqual(status, 200)
        self.assertIn("javascript", content_type)
        self.assertIn(b"/api/certificate", script)
        self.assertIn(b"/api/optimize", script)
        self.assertIn(b"/api/shift", script)
        self.assertIn(b"/api/gaps", script)

    def test_certificate_core_cli_and_http_values_agree(self) -> None:
        denominators = (2, 3, 5, 8)
        expected = portfolio_certificate(denominators, exact=True)
        status, api, content_type = self._request(
            "POST", "/api/certificate", {"denominators": list(denominators), "exact": True}
        )
        cli = self._cli_json("certificate", *(str(n) for n in denominators))

        self.assertEqual(status, 200)
        self.assertIn("application/json", content_type)
        self.assertEqual(api["denominators"], list(expected.denominators))
        self.assertEqual(api["point_count"], expected.point_count)
        self._assert_fraction_payload(api["energy"], expected.energy)
        self.assertAlmostEqual(api["worst_case_error"], expected.worst_case_error, places=15)
        self.assertEqual(cli["denominators"], api["denominators"])
        self.assertEqual(cli["point_count"], api["point_count"])
        self.assertEqual(Fraction(cli["energy"]), expected.energy)

    def test_fixed_optimizer_core_cli_and_http_values_agree(self) -> None:
        parameters = {"start": 2, "stop": 15, "layers": 3, "seed": 17}
        expected = benchmark_case(**parameters)
        status, api, _ = self._request(
            "POST", "/api/optimize", {"benchmark": True, **parameters}
        )
        cli = self._cli_json(
            "benchmark",
            "--start",
            "2",
            "--stop",
            "15",
            "--layers",
            "3",
            "--seed",
            "17",
        )
        self.assertEqual(status, 200)
        for payload in (api, cli):
            self.assertEqual(payload["parameters"], parameters)
            self.assertEqual(payload["greedy"]["denominators"], expected["greedy"]["denominators"])
            self.assertEqual(payload["greedy"]["point_count"], expected["greedy"]["point_count"])
            self.assertEqual(payload["ratios"], expected["ratios"])
            self.assertEqual(
                self._without_timings(payload["small_instance"]),
                self._without_timings(expected["small_instance"]),
            )
            self.assertTrue(payload["deterministic"])

    def test_shift_core_cli_and_http_values_agree(self) -> None:
        expected = farey_shift_moments(11, max_order=4, exact=True)
        status, api, _ = self._request(
            "POST", "/api/shift", {"p": 11, "max_order": 4, "exact": True}
        )
        cli = self._cli_json("shift", "11", "--max-order", "4", "--exact")
        self.assertEqual(status, 200)
        self.assertEqual(api["p"], 11)
        self.assertEqual(api["interior_count"], expected["point_count"])
        for order in range(5):
            key = str(order)
            api_value = api["moments"]["raw_sums"][key]
            self._assert_fraction_payload(api_value, expected["raw_sums"][order])
            self.assertEqual(Fraction(cli["raw_sums"][key]), expected["raw_sums"][order])
        self.assertEqual(api["moments"]["raw_sums"]["1"]["numerator"], 0)
        self.assertEqual(api["moments"]["raw_sums"]["3"]["numerator"], 0)

    def test_gap_core_cli_and_http_values_agree(self) -> None:
        gaps = (Fraction(1, 2), Fraction(1, 3), Fraction(1, 6))
        expected = gap_permutation_certificate(gaps, exact=True)
        status, api, _ = self._request(
            "POST",
            "/api/gaps",
            {"gaps": ["1/2", "1/3", "1/6"], "exact": True},
        )
        cli = self._cli_json("gaps", "1/2", "1/3", "1/6")
        self.assertEqual(status, 200)
        self.assertEqual(api["gap_count"], expected.gap_count)
        self.assertEqual(cli["gap_count"], expected.gap_count)
        for key in (
            "gap_variance",
            "supplied_l1",
            "supplied_quadratic",
            "supplied_l2_squared",
            "expected_quadratic",
            "expected_l2_squared",
        ):
            api_value = api[key]
            self._assert_fraction_payload(api_value, getattr(expected, key))
            self.assertEqual(Fraction(cli[key]), getattr(expected, key))
        self.assertEqual(api["distinct_permutations"], 6)
        self.assertEqual(cli["distinct_permutations"], 6)
        for key in (
            "rigorous_l1_lower_bound",
            "rigorous_l1_lower_bound_constant",
            "l1_upper_bound_sum",
            "l1_upper_bound_cauchy",
        ):
            self.assertEqual(api[key], getattr(expected, key))
            self.assertEqual(cli[key], getattr(expected, key))

        status, uniform, _ = self._request(
            "POST",
            "/api/gaps",
            {"gaps": ["1/4", "1/4", "1/4", "1/4"], "exact": True},
        )
        self.assertEqual(status, 200)
        self.assertEqual(
            Fraction(
                uniform["gap_variance"]["numerator"],
                uniform["gap_variance"]["denominator"],
            ),
            0,
        )
        self.assertEqual(uniform["rigorous_l1_lower_bound"], 0.0)
        self.assertEqual(uniform["l1_upper_bound_sum"], 0.0)

        status, farey, _ = self._request(
            "POST", "/api/gaps", {"farey_order": 5, "exact": True}
        )
        self.assertEqual(status, 200)
        self.assertEqual(
            [
                Fraction(value["numerator"], value["denominator"])
                for value in farey["gaps"]
            ],
            list(farey_gaps(5, exact=True)),
        )

    def test_exact_fraction_strings_survive_javascript_unsafe_integer_sizes(self) -> None:
        expected_shift = farey_shift_moments(101, max_order=4, exact=True)
        status, shifted, _ = self._request(
            "POST", "/api/shift", {"p": 101, "max_order": 4, "exact": True}
        )
        self.assertEqual(status, 200)
        for order in (2, 4):
            expected = expected_shift["raw_sums"][order]
            self.assertGreater(
                max(abs(expected.numerator), expected.denominator), 2**53
            )
            self._assert_fraction_payload(
                shifted["moments"]["raw_sums"][str(order)], expected
            )

        denominators = (2_147_483_647, 4_294_967_291)
        expected_certificate = portfolio_certificate(denominators, exact=True)
        status, certificate, _ = self._request(
            "POST",
            "/api/certificate",
            {"denominators": list(denominators), "exact": True},
        )
        self.assertEqual(status, 200)
        self.assertGreater(
            max(
                abs(expected_certificate.energy.numerator),
                expected_certificate.energy.denominator,
            ),
            2**53,
        )
        self._assert_fraction_payload(certificate["energy"], expected_certificate.energy)

    def test_client_errors_are_json_4xx_not_internal_500(self) -> None:
        cases = (
            ("GET", "/api/missing", _MISSING, None, 404),
            ("POST", "/api/certificate", _MISSING, b"{not-json", 400),
            ("POST", "/api/certificate", [2, 3], None, 400),
            ("POST", "/api/certificate", {"denominators": []}, None, 400),
            ("POST", "/api/certificate", {"denominators": [2, 2]}, None, 400),
            ("POST", "/api/optimize", {"candidates": [2, 3], "layers": True}, None, 400),
            ("POST", "/api/shift", {"p": 9}, None, 400),
            ("POST", "/api/gaps", {"gaps": ["1/3", "1/3"]}, None, 400),
            ("POST", "/api/gaps", {"gaps": ["1"]}, None, 400),
            ("POST", "/api/gaps", {"gaps": ["-1/2", "3/2"]}, None, 400),
            ("POST", "/api/gaps", {"gaps": ["bad", "1"]}, None, 400),
            (
                "POST",
                "/api/gaps",
                {"gaps": ["1/2", "1/2"], "farey_order": 5},
                None,
                400,
            ),
            ("PUT", "/api/health", {}, None, 405),
            ("POST", "/not-api", {}, None, 404),
        )
        for method, path, payload, raw, expected_status in cases:
            with self.subTest(method=method, path=path, payload=payload):
                status, body, content_type = self._request(
                    method, path, payload, raw=raw
                )
                self.assertEqual(status, expected_status)
                self.assertIn("application/json", content_type)
                self.assertEqual(body["status"], expected_status)
                self.assertIsInstance(body["error"], str)
                self.assertTrue(body["error"])

    def test_compute_endpoints_reject_uncapped_work_before_solving(self) -> None:
        over_cap = (
            ("/api/gaps", {"farey_order": GAP_FAREY_ORDER_CAP + 1}, str(GAP_FAREY_ORDER_CAP)),
            (
                "/api/gaps",
                {"gaps": ["1"] * (GAP_SUPPLIED_COUNT_CAP + 1)},
                str(GAP_SUPPLIED_COUNT_CAP),
            ),
            ("/api/shift", {"p": SHIFT_PRIME_CAP + 1}, str(SHIFT_PRIME_CAP)),
            (
                "/api/shift",
                {"p": 11, "max_order": SHIFT_MAX_ORDER_CAP + 1},
                str(SHIFT_MAX_ORDER_CAP),
            ),
            (
                "/api/optimize",
                {"benchmark": True, "start": 2, "stop": 2 + OPTIMIZE_BENCHMARK_SPAN_CAP + 1},
                str(OPTIMIZE_BENCHMARK_SPAN_CAP),
            ),
            (
                "/api/optimize",
                {"candidates": [2, 3, 5], "layers": 1, "samples": OPTIMIZE_SAMPLE_CAP + 1},
                str(OPTIMIZE_SAMPLE_CAP),
            ),
            (
                "/api/optimize",
                {"candidates": [(1 << 61) - 1], "layers": 1, "samples": 1},
                str(OPTIMIZE_TRIAL_DIVISION_BUDGET),
            ),
            (
                "/api/optimize",
                {
                    "benchmark": True,
                    "start": (1 << 61) - 1,
                    "stop": (1 << 61) - 1,
                    "layers": 1,
                },
                str(OPTIMIZE_TRIAL_DIVISION_BUDGET),
            ),
            (
                "/api/optimize",
                {
                    "candidates": list(range(2, 2 + OPTIMIZE_CANDIDATE_CAP)),
                    "layers": 32,
                    "samples": OPTIMIZE_SAMPLE_CAP,
                },
                str(OPTIMIZE_KERNEL_WORK_CELL_CAP),
            ),
            (
                "/api/optimize",
                {
                    "candidates": list(range(2, 20)),
                    "layers": 9,
                    "samples": 1,
                },
                str(OPTIMIZE_KERNEL_WORK_CELL_CAP),
            ),
            (
                "/api/certificate",
                {"denominators": [(1 << 61) + 15]},
                "factorization",
            ),
            (
                "/api/certificate",
                {"denominators": [2] * (CERTIFICATE_DENOMINATOR_COUNT_CAP + 1)},
                str(CERTIFICATE_DENOMINATOR_COUNT_CAP),
            ),
        )
        for path, payload, needle in over_cap:
            with self.subTest(path=path, payload=payload):
                status, body, _ = self._request("POST", path, payload)
                self.assertEqual(status, 400)
                self.assertIn(needle, body["error"])

        # A supplied factorization keeps a large denominator affordable.
        big = (1 << 61) + 15
        status, body, _ = self._request(
            "POST",
            "/api/certificate",
            {"denominators": [big], "factorizations": {str(big): {str(big): 1}}},
        )
        # The supplied base is itself huge, so it is still rejected on budget.
        self.assertEqual(status, 400)
        self.assertIn("factorization", body["error"])

        # A tiny base with an oversized exponent must be rejected before the
        # validator materialises ``base ** exponent`` (product-check DoS).
        status, body, _ = self._request(
            "POST",
            "/api/certificate",
            {"denominators": [999], "factorizations": {"999": {"3": 60_000_000}}},
        )
        self.assertEqual(status, 400)
        self.assertIn("exponent", body["error"])

        # A genuine factorization (exponent within the denominator bit length)
        # still solves.
        status, _, _ = self._request(
            "POST",
            "/api/certificate",
            {"denominators": [8], "factorizations": {"8": {"2": 3}}},
        )
        self.assertEqual(status, 200)

        # Values just under the caps still solve normally.
        under_cap = (
            ("/api/gaps", {"farey_order": 5}),
            ("/api/shift", {"p": 11, "max_order": 4}),
            ("/api/optimize", {"benchmark": True, "start": 2, "stop": 15, "layers": 3}),
            ("/api/certificate", {"denominators": [2, 3, 5, 7]}),
        )
        for path, payload in under_cap:
            with self.subTest(path=path, payload=payload):
                status, _, _ = self._request("POST", path, payload)
                self.assertEqual(status, 200)

    def test_optimize_work_caps_reject_before_solver_entry(self) -> None:
        with patch.object(web.optimizer, "benchmark_case") as solve:
            status, body, _ = self._request(
                "POST",
                "/api/optimize",
                {
                    "benchmark": True,
                    "start": (1 << 61) - 1,
                    "stop": (1 << 61) - 1,
                    "layers": 1,
                },
            )
            self.assertEqual(status, 400)
            self.assertIn("factorization work", body["error"])
            solve.assert_not_called()

    def test_exact_gap_bit_work_rejects_before_certificate_entry(self) -> None:
        gaps = [f"1/{(1 << (1_000 + index)) - 1}" for index in range(100)]
        with patch.object(web.gap_permutation, "gap_permutation_certificate") as solve:
            status, body, _ = self._request(
                "POST", "/api/gaps", {"gaps": gaps, "exact": True}
            )
            self.assertEqual(status, 400)
            self.assertIn(
                str(GAP_SUPPLIED_COMMON_DENOMINATOR_BIT_CAP), body["error"]
            )
            solve.assert_not_called()

        # Repeated modest denominators do not pay a false unique-denominator
        # penalty and an ordinary exact certificate still solves.
        status, _, _ = self._request(
            "POST", "/api/gaps", {"gaps": ["1/200"] * 200, "exact": True}
        )
        self.assertEqual(status, 200)

    def test_exact_gap_output_size_rejects_before_certificate_entry(self) -> None:
        primes = (2, 3, 5, 7, 13, 17, 19, 23, 29, 31)

        def exact_gaps(bits: int) -> list[str]:
            cumulative: list[Fraction] = []
            for index, prime in enumerate(primes, start=1):
                denominator = prime ** int(bits / log2(prime))
                numerator = index * denominator // 11
                while numerator % prime == 0:
                    numerator += 1
                cumulative.append(Fraction(numerator, denominator))
            points = [Fraction(0), *cumulative, Fraction(1)]
            gaps = [right - left for left, right in zip(points, points[1:])]
            self.assertTrue(all(gap > 0 for gap in gaps))
            self.assertEqual(sum(gaps, start=Fraction(0)), 1)
            return [str(gap) for gap in gaps]

        with patch.object(web.gap_permutation, "gap_permutation_certificate") as solve:
            status, body, _ = self._request(
                "POST", "/api/gaps", {"gaps": exact_gaps(750), "exact": True}
            )
            self.assertEqual(status, 400)
            self.assertIn(
                str(GAP_SUPPLIED_COMMON_DENOMINATOR_BIT_CAP), body["error"]
            )
            solve.assert_not_called()

        # A structurally identical large exact case below the common-
        # denominator cap must complete the whole JSON transport path.
        accepted = exact_gaps(450)
        status, body, _ = self._request(
            "POST", "/api/gaps", {"gaps": accepted, "exact": True}
        )
        self.assertEqual(status, 200)
        self.assertEqual(body["gap_count"], len(accepted))
        self.assertGreater(body["supplied_quadratic"]["denominator"], 0)

    def test_certificate_bit_work_rejects_before_kernel_entry(self) -> None:
        primes = (
            2, 3, 5, 7, 11, 13, 17, 19, 23,
            29, 31, 37, 41, 43, 47, 53, 59, 61,
        )
        exponents = [int(4_000 / log2(prime)) for prime in primes]
        denominators = [
            prime**exponent for prime, exponent in zip(primes, exponents)
        ]
        factorizations = {
            str(value): {str(prime): exponent}
            for prime, exponent, value in zip(primes, exponents, denominators)
        }
        with patch.object(web.kernel, "portfolio_certificate") as solve:
            status, body, _ = self._request(
                "POST",
                "/api/certificate",
                {"denominators": denominators, "factorizations": factorizations},
            )
            self.assertEqual(status, 400)
            self.assertIn(str(CERTIFICATE_OUTPUT_INTEGER_BIT_CAP), body["error"])
            solve.assert_not_called()

        # A separate many-layer case stays below the output-size cap but
        # exceeds pairwise kernel work.
        kernel_primes = primes_up_to(229)[:50]
        kernel_exponents = [int(200 / log2(prime)) for prime in kernel_primes]
        kernel_denominators = [
            prime**exponent
            for prime, exponent in zip(kernel_primes, kernel_exponents)
        ]
        kernel_factorizations = {
            str(value): {str(prime): exponent}
            for prime, exponent, value in zip(
                kernel_primes, kernel_exponents, kernel_denominators
            )
        }
        with patch.object(web.kernel, "portfolio_certificate") as solve:
            status, body, _ = self._request(
                "POST",
                "/api/certificate",
                {
                    "denominators": kernel_denominators,
                    "factorizations": kernel_factorizations,
                },
            )
            self.assertEqual(status, 400)
            self.assertIn(str(CERTIFICATE_KERNEL_BIT_CELL_CAP), body["error"])
            solve.assert_not_called()

        overwide = 1 << CERTIFICATE_DENOMINATOR_BIT_CAP
        with patch.object(web.kernel, "portfolio_certificate") as solve:
            status, body, _ = self._request(
                "POST",
                "/api/certificate",
                {
                    "denominators": [overwide],
                    "factorizations": {str(overwide): {"2": CERTIFICATE_DENOMINATOR_BIT_CAP}},
                },
            )
            self.assertEqual(status, 400)
            self.assertIn(str(CERTIFICATE_DENOMINATOR_BIT_CAP), body["error"])
            solve.assert_not_called()

        # A single valid denominator exactly at the per-value bit cap remains
        # usable even though its point count exceeds binary64's integer range.
        at_cap = 1 << (CERTIFICATE_DENOMINATOR_BIT_CAP - 1)
        status, body, _ = self._request(
            "POST",
            "/api/certificate",
            {
                "denominators": [at_cap],
                "factorizations": {
                    str(at_cap): {"2": CERTIFICATE_DENOMINATOR_BIT_CAP - 1}
                },
            },
        )
        self.assertEqual(status, 200)
        self.assertEqual(body["worst_case_error"], float.fromhex("0x0.0000000000001p-1022"))

        # Large accepted exact output must survive the complete solver and JSON
        # transport path, not merely admission.
        accepted_primes = (2, 3, 5)
        accepted_exponents = [int(3_900 / log2(prime)) for prime in accepted_primes]
        accepted_denominators = [
            prime**exponent
            for prime, exponent in zip(accepted_primes, accepted_exponents)
        ]
        status, body, _ = self._request(
            "POST",
            "/api/certificate",
            {
                "denominators": accepted_denominators,
                "factorizations": {
                    str(value): {str(prime): exponent}
                    for prime, exponent, value in zip(
                        accepted_primes, accepted_exponents, accepted_denominators
                    )
                },
            },
        )
        self.assertEqual(status, 200)
        self.assertEqual(body["denominators"], accepted_denominators)
        self.assertGreater(body["energy"]["denominator"], 0)

        with patch.object(web.optimizer, "greedy_portfolio") as solve:
            status, body, _ = self._request(
                "POST",
                "/api/optimize",
                {
                    "candidates": list(range(2, 20)),
                    "layers": 9,
                    "samples": 1,
                },
            )
            self.assertEqual(status, 400)
            self.assertIn("combined matrix/evaluation work", body["error"])
            solve.assert_not_called()

    def test_host_header_must_be_loopback(self) -> None:
        request = urllib.request.Request(
            self.base_url + "/api/health",
            method="GET",
            headers={"Host": "attacker.example.com"},
        )
        with self.assertRaises(urllib.error.HTTPError) as raised:
            urllib.request.urlopen(request, timeout=10)
        self.assertEqual(raised.exception.code, 403)
        raised.exception.close()

        for spoof in ("evil.test", "attacker.example.com:8765"):
            request = urllib.request.Request(
                self.base_url + "/api/balance",
                data=json.dumps({"mode": "quota", "counts": {"a": 1}}).encode(),
                method="POST",
                headers={"Host": spoof, "Content-Type": "text/plain"},
            )
            with self.subTest(host=spoof), self.assertRaises(
                urllib.error.HTTPError
            ) as raised:
                urllib.request.urlopen(request, timeout=10)
            self.assertEqual(raised.exception.code, 403)
            raised.exception.close()

        # The normal loopback Host set by urllib is accepted.
        status, health, _ = self._request("GET", "/api/health")
        self.assertEqual((status, health["status"]), (200, "ok"))

    def test_post_rejects_hostile_origin_and_non_json_content_type(self) -> None:
        payload = json.dumps({"mode": "quota", "counts": {"a": 1}}).encode()
        for headers, expected_status in (
            (
                {
                    "Origin": "https://attacker.example",
                    "Content-Type": "application/json",
                },
                403,
            ),
            (
                {
                    "Origin": self.base_url,
                    "Content-Type": "text/plain",
                },
                415,
            ),
        ):
            request = urllib.request.Request(
                self.base_url + "/api/balance",
                data=payload,
                method="POST",
                headers=headers,
            )
            with self.subTest(headers=headers), self.assertRaises(
                urllib.error.HTTPError
            ) as raised:
                urllib.request.urlopen(request, timeout=10)
            self.assertEqual(raised.exception.code, expected_status)
            raised.exception.close()

        request = urllib.request.Request(
            self.base_url + "/api/balance",
            data=payload,
            method="POST",
            headers={"Origin": self.base_url, "Content-Type": "application/json"},
        )
        with urllib.request.urlopen(request, timeout=10) as response:
            self.assertEqual(response.status, 200)


class HostHeaderUnitTests(unittest.TestCase):
    def test_loopback_authorities_are_accepted(self) -> None:
        for host in (
            "127.0.0.1",
            "127.0.0.1:8765",
            "localhost",
            "localhost:8765",
            "::1",
            "[::1]",
            "[::1]:8765",
        ):
            self.assertTrue(_host_is_loopback(host), host)

    def test_non_loopback_authorities_are_rejected(self) -> None:
        for host in (
            None,
            "",
            "attacker.example.com",
            "attacker.example.com:8765",
            "10.0.0.5",
            "[2001:db8::1]:8765",
            "127.0.0.1.attacker.example.com",
            "[::1]attacker.example.com",
            "[::1]:not-a-port",
            "localhost:",
        ):
            self.assertFalse(_host_is_loopback(host), host)

    def test_only_loopback_http_origins_are_accepted(self) -> None:
        for origin in (
            None,
            "http://127.0.0.1:8765",
            "https://localhost",
            "http://[::1]:8765",
        ):
            self.assertTrue(_origin_is_loopback(origin), origin)
        for origin in (
            "",
            "null",
            "https://attacker.example",
            "file://localhost/tmp/x",
            "http://localhost.attacker.example",
            "http://localhost/path",
        ):
            self.assertFalse(_origin_is_loopback(origin), origin)


class SlowConnectionHardeningTests(unittest.TestCase):
    def test_handler_sets_socket_timeout(self) -> None:
        self.assertEqual(Handler.timeout, SOCKET_TIMEOUT_SECONDS)
        self.assertGreater(Handler.timeout, 0)

    def test_bounded_server_drops_connections_beyond_the_cap(self) -> None:
        release = threading.Event()

        class _BlockingHandler(Handler):
            def do_GET(self) -> None:  # noqa: N802
                release.wait(timeout=5)
                self._send_json(HTTPStatus.OK, {"ok": True})

        class _TinyServer(_BoundedThreadingHTTPServer):
            max_concurrent_connections = 2

        server = _TinyServer(("127.0.0.1", 0), _BlockingHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        host, port = server.server_address
        held: list[socket.socket] = []
        try:
            # Fill every slot with a request that blocks inside the handler.
            for _ in range(2):
                connection = socket.create_connection((host, port), timeout=5)
                connection.sendall(
                    b"GET /api/health HTTP/1.1\r\nHost: 127.0.0.1\r\n\r\n"
                )
                held.append(connection)
            # Give the workers a moment to occupy both semaphore slots.
            time.sleep(0.3)
            # An extra connection must be dropped without an HTTP response:
            # either a clean empty read (FIN) or a reset (RST), depending on
            # the platform, but never a served "200 OK".
            with socket.create_connection((host, port), timeout=5) as extra:
                extra.sendall(b"GET /api/health HTTP/1.1\r\nHost: 127.0.0.1\r\n\r\n")
                extra.settimeout(5)
                try:
                    received = extra.recv(1024)
                except ConnectionResetError:
                    received = b""
                self.assertEqual(received, b"")
        finally:
            release.set()
            for connection in held:
                connection.settimeout(2)
                try:
                    connection.recv(4096)
                except (ConnectionResetError, OSError):
                    pass
                connection.close()
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)


if __name__ == "__main__":
    unittest.main()
