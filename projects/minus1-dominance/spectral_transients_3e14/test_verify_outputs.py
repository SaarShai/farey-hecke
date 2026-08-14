#!/usr/bin/env python3
"""Negative fixtures proving the spectral artifact gates trip."""

from __future__ import annotations

import csv
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from verify_outputs import verify


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CURVE = ROOT / "projects/minus1-dominance/curve_3e14.tsv"
PRIOR_N8 = ROOT / "projects/minus1-dominance/zeros_N8.json"
OUTPUT = HERE / "output"
REQUIRED_OUTPUTS = (
    "zero_crosscheck.tsv",
    "reconstruction.tsv",
    "transition_summary.tsv",
    "fit_metrics.tsv",
    "mode_attribution.tsv",
)


class VerifyOutputsTests(unittest.TestCase):
    def copy_output(self, directory: Path) -> Path:
        target = directory / "output"
        target.mkdir()
        for name in REQUIRED_OUTPUTS:
            shutil.copy2(OUTPUT / name, target / name)
        return target

    def test_current_artifacts_pass(self) -> None:
        verify(CURVE, PRIOR_N8, OUTPUT)

    def test_corrupt_curve_hash_trips(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            bad_curve = Path(raw) / "curve.tsv"
            shutil.copy2(CURVE, bad_curve)
            with bad_curve.open("ab") as stream:
                stream.write(b"corruption")
            with self.assertRaisesRegex(AssertionError, "curve hash changed"):
                verify(bad_curve, PRIOR_N8, OUTPUT)

    def test_failed_zero_status_trips(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            output = self.copy_output(Path(raw))
            path = output / "zero_crosscheck.tsv"
            text = path.read_text().replace("\tPASS\n", "\tFAIL\n", 1)
            path.write_text(text)
            with self.assertRaisesRegex(AssertionError, "zero check failed"):
                verify(CURVE, PRIOR_N8, output)

    def test_missing_reconstruction_row_trips(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            output = self.copy_output(Path(raw))
            path = output / "reconstruction.tsv"
            lines = path.read_text().splitlines()
            path.write_text("\n".join(lines[:-1]) + "\n")
            with self.assertRaisesRegex(AssertionError, "reconstruction rows"):
                verify(CURVE, PRIOR_N8, output)

    def test_prior_zero_anchor_mismatch_trips(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            prior_path = Path(raw) / "zeros_N8.json"
            prior = json.loads(PRIOR_N8.read_text())
            first_key = next(iter(prior))
            prior[first_key][0] += 0.01
            prior_path.write_text(json.dumps(prior))
            with self.assertRaisesRegex(AssertionError, "first-zero anchors disagree"):
                verify(CURVE, prior_path, OUTPUT)

    def test_zero_rank_change_summary_trips(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            output = self.copy_output(Path(raw))
            path = output / "transition_summary.tsv"
            with path.open() as stream:
                rows = list(csv.DictReader(stream, delimiter="\t"))
            for row in rows:
                if row["q"] == "7" and row["window"] == "top_decade":
                    row["rank_changes"] = "0"
            with path.open("w", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter="\t")
                writer.writeheader()
                writer.writerows(rows)
            with self.assertRaises(AssertionError):
                verify(CURVE, PRIOR_N8, output)


if __name__ == "__main__":
    unittest.main()

