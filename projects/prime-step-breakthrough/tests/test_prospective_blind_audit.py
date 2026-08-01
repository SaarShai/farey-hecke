from __future__ import annotations

import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

import prospective_blind_audit as pilot


def fixtures(count: int = 20, *, final: bool = False) -> tuple[bytes, bytes]:
    frozen = datetime(2026, 1, 1, tzinfo=timezone.utc)
    teams = [
        {"team": {"id": index + 1, "name": f"Team {index + 1}"}, "wins": 40 + index, "losses": 60 - index}
        for index in range(30)
    ]
    standings = {"records": [{"teamRecords": teams}]}
    games = []
    for index in range(count):
        away_id = index % 30 + 1
        home_id = (index + 7) % 30 + 1
        away_score = index % 5 + 1
        home_score = (index * 3) % 7 + 1
        if home_score == away_score:
            home_score += 1
        teams_payload = {
            "away": {"team": {"id": away_id, "name": f"Team {away_id}"}},
            "home": {"team": {"id": home_id, "name": f"Team {home_id}"}},
        }
        if final:
            teams_payload["away"]["score"] = away_score
            teams_payload["home"]["score"] = home_score
        games.append(
            {
                "gamePk": 900000 + index,
                "gameDate": (frozen + timedelta(days=1, minutes=index)).isoformat().replace("+00:00", "Z"),
                "status": {
                    "abstractGameState": "Final" if final else "Preview",
                    "detailedState": "Final" if final else "Scheduled",
                },
                "teams": teams_payload,
            }
        )
    schedule = {"totalGames": count, "dates": [{"date": "2026-01-02", "games": games}]}
    return json.dumps(schedule).encode(), json.dumps(standings).encode()


class ProspectiveBlindAuditTests(unittest.TestCase):
    def freeze(self, root: Path) -> tuple[Path, dict[str, object], bytes]:
        schedule, standings = fixtures()
        manifest = pilot.build_freeze_manifest(
            schedule,
            standings,
            schedule_source="fixture:schedule",
            standings_source="fixture:standings",
            frozen_at="2026-01-01T00:00:00Z",
            start_date="2026-01-02",
            end_date="2026-01-02",
            seed=17,
            pilot_id="fixture-pilot",
        )
        target = root / "pilot"
        pilot.write_freeze(target, schedule, standings, manifest)
        return target, manifest, schedule

    def test_freeze_has_no_target_outcomes_and_three_complete_commitments(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target, manifest, _ = self.freeze(Path(directory))
            report = pilot.verify_freeze(target)
            self.assertTrue(report["freeze_verified"])
            item_ids = sorted(item["game_pk"] for item in manifest["items"])
            self.assertEqual(manifest["outcome_state"], "ABSENT_BY_DESIGN")
            for item in manifest["items"]:
                self.assertFalse(pilot.FORBIDDEN_ITEM_KEYS.intersection(item))
            self.assertEqual(set(manifest["orders"]), {"production", "seeded_random", "quota_balanced"})
            for order in manifest["orders"].values():
                self.assertEqual(sorted(order["game_pks"]), item_ids)

    def test_freeze_is_deterministic_except_declared_time_and_script_hash(self) -> None:
        schedule, standings = fixtures()
        kwargs = dict(
            schedule_source="fixture:schedule",
            standings_source="fixture:standings",
            frozen_at="2026-01-01T00:00:00Z",
            start_date="2026-01-02",
            end_date="2026-01-02",
            seed=17,
            pilot_id="fixture-pilot",
        )
        self.assertEqual(
            pilot.build_freeze_manifest(schedule, standings, **kwargs),
            pilot.build_freeze_manifest(schedule, standings, **kwargs),
        )

    def test_tampered_manifest_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target, _, _ = self.freeze(Path(directory))
            payload = json.loads((target / "freeze.json").read_text())
            payload["items"][0]["predicted_side"] = "away"
            pilot.atomic_json(target / "freeze.json", payload)
            with self.assertRaisesRegex(pilot.PilotError, "freeze.json does not match"):
                pilot.verify_freeze(target)

    def test_tampered_source_snapshot_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target, _, _ = self.freeze(Path(directory))
            (target / "sources" / "schedule.json").write_bytes(b"{}")
            with self.assertRaisesRegex(pilot.PilotError, "schedule snapshot digest"):
                pilot.verify_freeze(target)

    def test_incomplete_reveal_is_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target, manifest, schedule = self.freeze(Path(directory))
            status = pilot.live_status(manifest, json.loads(schedule))
            self.assertFalse(status["all_final"])
            with self.assertRaisesRegex(pilot.PilotError, "reveal blocked"):
                pilot.build_result(
                    target,
                    schedule,
                    reveal_source="fixture:pending",
                    revealed_at="2026-01-03T00:00:00Z",
                )
            self.assertFalse((target / "result.json").exists())

    def test_final_reveal_binds_freeze_and_distinguishes_certificates(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target, _, _ = self.freeze(Path(directory))
            final_schedule, _ = fixtures(final=True)
            result = pilot.build_result(
                target,
                final_schedule,
                reveal_source="fixture:final",
                revealed_at="2026-01-03T00:00:00Z",
            )
            pilot.write_result(target, final_schedule, result)
            verified = pilot.verify_result(target)
            self.assertEqual(verified["result_state"], "VERIFIED")
            orders = result["analysis"]["orders"]
            self.assertIsNone(orders["production"]["stopping"]["randomization_exact_5pp"])
            self.assertIsInstance(orders["seeded_random"]["stopping"]["randomization_exact_5pp"], int)
            self.assertIsInstance(orders["quota_balanced"]["stopping"]["randomization_exact_5pp"], int)
            exact = {
                entry["stopping"]["distribution_free_exact_5pp"]
                for entry in orders.values()
            }
            self.assertEqual(len(exact), 1)

    def test_freeze_refuses_nonfuture_game(self) -> None:
        schedule, standings = fixtures()
        payload = json.loads(schedule)
        payload["dates"][0]["games"][0]["gameDate"] = "2025-12-31T23:59:59Z"
        with self.assertRaisesRegex(pilot.PilotError, "not strictly future"):
            pilot.build_freeze_manifest(
                json.dumps(payload).encode(),
                standings,
                schedule_source="fixture:schedule",
                standings_source="fixture:standings",
                frozen_at="2026-01-01T00:00:00Z",
                start_date="2026-01-02",
                end_date="2026-01-02",
                seed=17,
            )


if __name__ == "__main__":
    unittest.main()
