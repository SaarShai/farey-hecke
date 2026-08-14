#!/usr/bin/env python3
"""Negative fixtures proving every load-bearing N=19 gate can fail."""

from __future__ import annotations

import csv
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from verify_independent_n19 import verify


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
CURVE = ROOT / "projects/minus1-dominance/curve_3e14.tsv"
OUTPUT = HERE / "output"
FILES = (
    "n19_arb_certificate.json",
    "pari_n19_100_zeros.tsv",
    "n19_deep_reconstruction.tsv",
    "n19_deep_metrics.tsv",
    "n19_deep_stability.tsv",
    "n19_deep_rank_summary.tsv",
)


def table(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open() as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        return list(reader.fieldnames or []), list(reader)


def write_table(path: Path, fields: list[str], data: list[dict[str, str]]) -> None:
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        writer.writerows(data)


class IndependentN19VerifierTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.output = Path(self.temp.name)
        for name in FILES:
            shutil.copy2(OUTPUT / name, self.output / name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def assert_gate_trips(self) -> None:
        with self.assertRaises(AssertionError):
            verify(CURVE, self.output)

    def test_known_good_artifact_passes(self) -> None:
        verify(CURVE, self.output)

    def test_character_corruption_trips(self) -> None:
        path = self.output / "n19_arb_certificate.json"
        data = json.loads(path.read_text())
        data["character"]["order"] = 17
        path.write_text(json.dumps(data))
        self.assert_gate_trips()

    def test_nonbracketing_interval_trips(self) -> None:
        path = self.output / "n19_arb_certificate.json"
        data = json.loads(path.read_text())
        root = data["root_bracket"]
        root["right_numerator"] = root["left_numerator"]
        root["right_denominator"] = root["left_denominator"]
        path.write_text(json.dumps(data))
        self.assert_gate_trips()

    def test_failed_deep_zero_check_trips(self) -> None:
        path = self.output / "pari_n19_100_zeros.tsv"
        content = path.read_text()
        path.write_text(content.replace("\tPASS\n", "\tFAIL\n", 1))
        self.assert_gate_trips()

    def test_missing_reconstruction_row_trips(self) -> None:
        path = self.output / "n19_deep_reconstruction.tsv"
        fields, data = table(path)
        write_table(path, fields, data[:-1])
        self.assert_gate_trips()

    def test_missing_metric_trips(self) -> None:
        path = self.output / "n19_deep_metrics.tsv"
        fields, data = table(path)
        write_table(path, fields, data[:-1])
        self.assert_gate_trips()

    def test_erased_k100_rank_instability_trips(self) -> None:
        path = self.output / "n19_deep_rank_summary.tsv"
        fields, data = table(path)
        for row in data:
            if row["K_zeros_per_character"] == "100":
                row["rank_changes"] = "0"
        write_table(path, fields, data)
        self.assert_gate_trips()


if __name__ == "__main__":
    unittest.main()
