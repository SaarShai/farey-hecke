#!/usr/bin/env python3
"""Targeted no-network tests for path_b_b1_b2_c1.py."""
from __future__ import annotations

import csv
import json
import os
import tempfile
import unittest
from pathlib import Path

import mpmath as mp

import path_b_b1_b2_c1 as c1


class PathBTests(unittest.TestCase):
    def test_mu_prime_square_rule(self) -> None:
        mu = c1.build_mu_ec({2: 3, 3: -2, 5: 1}, 6)
        self.assertEqual(mu[2], -3)
        self.assertEqual(mu[4], 2)
        self.assertEqual(mu[3], 2)
        self.assertEqual(mu[6], -6)

    def test_malformed_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.csv"
            path.write_text("label,band\n37a1,B1\n")
            with self.assertRaisesRegex(ValueError, "malformed curves manifest"):
                c1.parse_manifest(path)

    def test_resume_verified_raw(self) -> None:
        spec = {"label": "x1", "band": "B1", "role": "control", "rank": 0, "weight": 2, "conductor": 400, "nearest_target_distance": 11}
        provenance = {"manifest": spec, "K": 10, "precision": 50, "N_zeros": 2, "Tmax": 100}
        raw = {"provenance": provenance, "provenance_hash": c1.canonical_hash(provenance),
               "zeros": ["1", "2"], "Lprime": [["1", "0"], ["1", "0"]],
               "cK": [["1", "0"], ["1", "0"]], "C1": ["1", "1"],
               "E_C1": "1.0", "E_C1_sq": "1.5"}
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "x1.json"
            path.write_text(json.dumps(raw))
            row = c1.existing_valid(path, spec, 10, 2, 100, 50)
            self.assertIsNotNone(row)
            self.assertEqual(row["E_C1_sq"], "1.5")
            raw["provenance_hash"] = "bad"
            path.write_text(json.dumps(raw))
            self.assertIsNone(c1.existing_valid(path, spec, 10, 2, 100, 50))

    def test_hash_is_json_roundtrip_stable(self) -> None:
        provenance = {"ap": {2: 3, 3: -2}, "nested": [{"conductor": 389}]}
        restored = json.loads(json.dumps(provenance))
        self.assertEqual(c1.canonical_hash(provenance), c1.canonical_hash(restored))

    def test_isogeny_representative_key(self) -> None:
        self.assertEqual(c1.isogeny_class("446c1"), "446c")
        self.assertEqual(c1.isogeny_class("446c2"), "446c")
        self.assertNotEqual(c1.isogeny_class("446c1"), c1.isogeny_class("446d1"))

    def test_raw_label_set_invariant(self) -> None:
        specs = [{"label": "a1"}, {"label": "b1"}]
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            (directory / "a1.json").write_text("{}")
            (directory / "b1.json").write_text("{}")
            c1.verify_raw_label_set(directory, specs)
            (directory / "stale.json").write_text("{}")
            with self.assertRaisesRegex(RuntimeError, "extra=.*stale"):
                c1.verify_raw_label_set(directory, specs)

    def test_stored_parity_metadata(self) -> None:
        historical = c1.DEFAULT_DATA / "PATH_B_20FORMS.csv"
        with historical.open(newline="") as fh:
            rows = {row["label"]: row for row in csv.DictReader(fh)}
        self.assertEqual((rows["37a1"]["rank"], rows["37a1"]["conductor"]), ("1", "37"))
        self.assertEqual((rows["389a1"]["rank"], rows["389a1"]["conductor"]), ("2", "389"))
        self.assertGreater(mp.mpf(rows["37a1"]["E_C1_sq"]), 0)
        self.assertGreater(mp.mpf(rows["389a1"]["E_C1_sq"]), 0)

    @unittest.skipUnless(os.environ.get("PATH_B_LIVE_PARITY") == "1", "set PATH_B_LIVE_PARITY=1 for PARI smoke parity")
    def test_live_stored_numeric_parity(self) -> None:
        """Full 200-zero K=10000 recomputation, tolerance permits PARI last-bit drift."""
        historical = c1.DEFAULT_DATA / "PATH_B_20FORMS.csv"
        with historical.open(newline="") as fh:
            expected = {row["label"]: mp.mpf(row["E_C1_sq"]) for row in csv.DictReader(fh)}
        with tempfile.TemporaryDirectory() as tmp:
            for label, rank, conductor in (("37a1", 1, 37), ("389a1", 2, 389)):
                spec = {"label": label, "band": "B1", "role": "target", "rank": rank, "weight": 2,
                        "conductor": conductor, "nearest_target_distance": 0}
                row = c1.compute_row(spec, 10000, 200, 160, 50, Path(tmp))
                self.assertLess(abs(mp.mpf(row["E_C1_sq"]) - expected[label]), mp.mpf("1e-9"))


if __name__ == "__main__":
    unittest.main()
