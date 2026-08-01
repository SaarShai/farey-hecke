from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class HumanPilotSurfaceTests(unittest.TestCase):
    def test_participant_surface_is_static_and_label_blind(self) -> None:
        markup = (ROOT / "web" / "pilot.html").read_text(encoding="utf-8")
        script = (ROOT / "web" / "pilot.js").read_text(encoding="utf-8")
        manifest = json.loads((ROOT / "web" / "pilot_manifest.example.json").read_text(encoding="utf-8"))

        self.assertIn('src="/pilot.js"', markup)
        self.assertIn("Download verified workflow JSONL", markup)
        self.assertIn("workflow-measurement-v1", script)
        self.assertIn("crypto.subtle.digest", script)
        self.assertIn("ground_truth", script)
        self.assertIn("label-blind", markup)
        self.assertNotIn("innerHTML", script)
        self.assertNotIn("truth", json.dumps(manifest).lower())
        self.assertEqual(len(manifest["items"]), 4)


if __name__ == "__main__":
    unittest.main()
