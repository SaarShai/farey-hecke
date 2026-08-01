#!/usr/bin/env python3
"""Freeze and reveal a genuinely prospective, outcome-blind audit pilot.

The freeze phase commits item identities, metadata, predictions, strata, and
three complete orders before any target outcome is available.  The reveal
phase is fail-closed: it writes no result until every frozen item is final.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import statistics
import tempfile
import urllib.request
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from typing import Any

import economic_validation as safe
import real_data_ml_simulation as audit
from coprimebatch.prefix_balance import verify_quota_result


SCHEMA = "prospective-blind-audit-freeze-v1"
RESULT_SCHEMA = "prospective-blind-audit-result-v1"
PILOT_ID = "mlb-2026-08-03-to-2026-08-09"
DEFAULT_START = "2026-08-03"
DEFAULT_END = "2026-08-09"
DEFAULT_SEED = 20260801
DEFAULT_WARMUP = 10
MLB_SCHEDULE = "https://statsapi.mlb.com/api/v1/schedule"
MLB_STANDINGS = "https://statsapi.mlb.com/api/v1/standings"
FORBIDDEN_ITEM_KEYS = {"actual", "correct", "isWinner", "outcome", "score", "winner"}


class PilotError(RuntimeError):
    """Fail-closed protocol error."""


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def _atomic_write(path: Path, value: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(value)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_name, path)
    except BaseException:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def atomic_json(path: Path, value: object) -> None:
    _atomic_write(path, json.dumps(value, indent=2, sort_keys=True).encode("utf-8") + b"\n")


def fetch_bytes(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "farey-hecke-blind-audit/1"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def parse_json_bytes(value: bytes, source: str) -> dict[str, Any]:
    try:
        payload = json.loads(value)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PilotError(f"{source} is not valid JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise PilotError(f"{source} must contain a JSON object")
    return payload


def iso_utc(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise PilotError(f"timestamp lacks timezone: {value}")
    return parsed.astimezone(timezone.utc)


def schedule_url(start_date: str, end_date: str) -> str:
    return (
        f"{MLB_SCHEDULE}?sportId=1&startDate={start_date}&endDate={end_date}"
    )


def standings_url(season: int) -> str:
    return (
        f"{MLB_STANDINGS}?leagueId=103,104&season={season}"
        "&standingsTypes=regularSeason&hydrate=team"
    )


def reveal_url(game_pks: list[int]) -> str:
    joined = ",".join(str(value) for value in game_pks)
    return f"{MLB_SCHEDULE}?sportId=1&gamePks={joined}&hydrate=team,linescore"


def extract_standings(payload: dict[str, Any]) -> dict[int, dict[str, Any]]:
    teams: dict[int, dict[str, Any]] = {}
    for record in payload.get("records", []):
        for entry in record.get("teamRecords", []):
            team = entry.get("team", {})
            team_id = int(team["id"])
            wins = int(entry["wins"])
            losses = int(entry["losses"])
            if team_id in teams or wins < 0 or losses < 0 or wins + losses == 0:
                raise PilotError("standings contain a duplicate or invalid team record")
            teams[team_id] = {
                "team_id": team_id,
                "name": str(team["name"]),
                "wins": wins,
                "losses": losses,
            }
    if len(teams) != 30:
        raise PilotError(f"expected 30 MLB teams in standings, found {len(teams)}")
    return teams


def extract_schedule_games(payload: dict[str, Any]) -> list[dict[str, Any]]:
    games: list[dict[str, Any]] = []
    seen: set[int] = set()
    for date in payload.get("dates", []):
        for game in date.get("games", []):
            game_pk = int(game["gamePk"])
            if game_pk in seen:
                raise PilotError(f"duplicate gamePk in schedule: {game_pk}")
            seen.add(game_pk)
            teams = game["teams"]
            status = game["status"]
            games.append(
                {
                    "game_pk": game_pk,
                    "game_date": str(game["gameDate"]),
                    "status_abstract": str(status["abstractGameState"]),
                    "status_detail": str(status["detailedState"]),
                    "away_team_id": int(teams["away"]["team"]["id"]),
                    "away_team": str(teams["away"]["team"]["name"]),
                    "home_team_id": int(teams["home"]["team"]["id"]),
                    "home_team": str(teams["home"]["team"]["name"]),
                }
            )
    games.sort(key=lambda game: (iso_utc(game["game_date"]), game["game_pk"]))
    declared = payload.get("totalGames")
    if declared is not None and int(declared) != len(games):
        raise PilotError(f"schedule declares {declared} games but contains {len(games)}")
    if not games:
        raise PilotError("schedule contains no games")
    return games


def _rate(record: dict[str, Any]) -> Fraction:
    return Fraction(record["wins"] + 1, record["wins"] + record["losses"] + 2)


def build_items(
    schedule: dict[str, Any], standings: dict[str, Any], frozen_at: str
) -> list[dict[str, Any]]:
    teams = extract_standings(standings)
    games = extract_schedule_games(schedule)
    frozen_time = iso_utc(frozen_at)
    provisional: list[tuple[dict[str, Any], Fraction]] = []
    for game in games:
        if game["status_abstract"] != "Preview":
            raise PilotError(
                f"game {game['game_pk']} was not outcome-blind at freeze: "
                f"{game['status_abstract']} / {game['status_detail']}"
            )
        if iso_utc(game["game_date"]) <= frozen_time:
            raise PilotError(f"game {game['game_pk']} was not strictly future at freeze")
        away = teams.get(game["away_team_id"])
        home = teams.get(game["home_team_id"])
        if away is None or home is None:
            raise PilotError(f"missing standings for game {game['game_pk']}")
        away_rate = _rate(away)
        home_rate = _rate(home)
        predicted_side = "home" if home_rate >= away_rate else "away"
        margin = abs(home_rate - away_rate)
        item = {
            **game,
            "away_record": {"wins": away["wins"], "losses": away["losses"]},
            "home_record": {"wins": home["wins"], "losses": home["losses"]},
            "away_smoothed_rate": str(away_rate),
            "home_smoothed_rate": str(home_rate),
            "predicted_side": predicted_side,
            "predicted_team_id": game[f"{predicted_side}_team_id"],
            "margin_fraction": str(margin),
            "margin_float": float(margin),
        }
        provisional.append((item, margin))

    ranked = sorted(
        range(len(provisional)),
        key=lambda index: (provisional[index][1], provisional[index][0]["game_pk"]),
    )
    margin_bins = {
        index: min(4, rank * 5 // len(provisional))
        for rank, index in enumerate(ranked)
    }
    items: list[dict[str, Any]] = []
    for index, (item, _) in enumerate(provisional):
        margin_bin = margin_bins[index]
        item["margin_bin"] = margin_bin
        item["stratum"] = f"predicted-{item['predicted_side']}:margin-{margin_bin}"
        items.append(item)
    return items


def item_priority(seed: int, game_pk: int) -> str:
    return sha256_bytes(f"blind-audit-priority-v1|{seed}|{game_pk}".encode("ascii"))


def order_digest(name: str, game_pks: list[int]) -> str:
    return sha256_bytes(
        canonical_bytes({"schema": "blind-audit-order-v1", "name": name, "game_pks": game_pks})
    )


def build_orders(items: list[dict[str, Any]], seed: int) -> tuple[dict[str, Any], dict[str, Any]]:
    strata = [item["stratum"] for item in items]
    priorities = [item_priority(seed, item["game_pk"]) for item in items]
    quota, queues = audit.quota_plan(strata)
    report = verify_quota_result(quota)
    if not report.passed:
        raise PilotError(f"quota certificate failed: {report.errors}")
    random_indices = sorted(range(len(items)), key=lambda index: (priorities[index], index))
    ranked_queues = {
        name: sorted(queue, key=lambda index: (priorities[index], index))
        for name, queue in queues.items()
    }
    quota_indices = audit.materialize_order(quota, ranked_queues)
    index_orders = {
        "production": list(range(len(items))),
        "seeded_random": random_indices,
        "quota_balanced": quota_indices,
    }
    orders: dict[str, Any] = {}
    for name, indices in index_orders.items():
        game_pks = [items[index]["game_pk"] for index in indices]
        orders[name] = {
            "game_pks": game_pks,
            "sha256": order_digest(name, game_pks),
            "randomization_certified": name in {"seeded_random", "quota_balanced"},
        }
    certificate = {
        "verified": report.passed,
        "categories": list(quota.categories),
        "counts": list(quota.counts),
        "order_codes_sha256": quota.order_sha256,
        "max_declared_cell_discrepancy": str(quota.max_discrepancy),
    }
    return orders, certificate


def _manifest_core(manifest: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in manifest.items() if key != "commitment_sha256"}


def _script_sha256() -> str:
    return sha256_file(Path(__file__).resolve())


def build_freeze_manifest(
    schedule_bytes: bytes,
    standings_bytes: bytes,
    *,
    schedule_source: str,
    standings_source: str,
    frozen_at: str,
    start_date: str,
    end_date: str,
    seed: int,
    pilot_id: str = PILOT_ID,
) -> dict[str, Any]:
    schedule = parse_json_bytes(schedule_bytes, "schedule snapshot")
    standings = parse_json_bytes(standings_bytes, "standings snapshot")
    items = build_items(schedule, standings, frozen_at)
    orders, certificate = build_orders(items, seed)
    manifest: dict[str, Any] = {
        "schema": SCHEMA,
        "pilot_id": pilot_id,
        "frozen_at_utc": frozen_at,
        "outcome_state": "ABSENT_BY_DESIGN",
        "cohort": {
            "start_date": start_date,
            "end_date": end_date,
            "item_count": len(items),
            "first_scheduled_utc": items[0]["game_date"],
            "last_scheduled_utc": items[-1]["game_date"],
            "fixed_game_pks": [item["game_pk"] for item in items],
        },
        "sources": {
            "schedule": {"url": schedule_source, "sha256": sha256_bytes(schedule_bytes)},
            "standings": {"url": standings_source, "sha256": sha256_bytes(standings_bytes)},
        },
        "model": {
            "name": "smoothed-season-record-v1",
            "rule": "predict the side with larger Laplace-smoothed season win rate; ties predict home",
            "rate": "(wins + 1) / (wins + losses + 2)",
            "outcomes_used": False,
        },
        "strata": {
            "rule": "predicted side x outcome-blind batch margin rank quintile",
            "margin": "absolute difference of the two smoothed season win rates",
            "bins": 5,
            "outcomes_used": False,
        },
        "randomization": {
            "seed": seed,
            "priority_rule": "SHA256('blind-audit-priority-v1|<seed>|<game_pk>')",
            "pairing": "same per-item priorities define global random and within-stratum quota queues",
        },
        "analysis_preregistration": {
            "primary_metric": "integrated absolute prefix error after warmup",
            "warmup": min(DEFAULT_WARMUP, len(items)),
            "safe_stop_half_width": 0.05,
            "confidence_alpha": 0.05,
            "distribution_free_stop": "valid for all three fixed orders",
            "randomization_stop": "stratified exact hypergeometric; valid only for seeded_random and quota_balanced",
            "missing_outcomes": "reveal writes nothing until every fixed gamePk is Final with a non-tied score",
        },
        "items": items,
        "orders": orders,
        "quota_certificate": certificate,
        "generator_sha256": _script_sha256(),
    }
    manifest["commitment_sha256"] = sha256_bytes(canonical_bytes(_manifest_core(manifest)))
    return manifest


def render_freeze_readme(manifest: dict[str, Any], freeze_file_sha256: str) -> str:
    orders = manifest["orders"]
    return "\n".join(
        [
            "# Prospective blind audit pilot",
            "",
            f"Pilot: `{manifest['pilot_id']}`",
            f"Frozen before outcomes: `{manifest['frozen_at_utc']}`",
            f"Fixed future games: **{manifest['cohort']['item_count']}**",
            "Outcome state: **ABSENT_BY_DESIGN**",
            "",
            "## Commitments",
            "",
            f"- freeze.json SHA-256: `{freeze_file_sha256}`",
            f"- manifest core SHA-256: `{manifest['commitment_sha256']}`",
            f"- production order: `{orders['production']['sha256']}`",
            f"- seeded-random order: `{orders['seeded_random']['sha256']}`",
            f"- quota-balanced order: `{orders['quota_balanced']['sha256']}`",
            "",
            "The three full game-ID sequences, source snapshots, prediction rule, strata, randomization seed, and analysis rule are frozen in `freeze.json`.",
            "`reveal` fails closed until every fixed game ID is final. The production order receives only the distribution-free stopping certificate; exact hypergeometric stopping requires the committed randomization used by the other two orders.",
            "",
            "## Commands",
            "",
            "```bash",
            "PYTHONPATH=src python3 prospective_blind_audit.py verify --pilot-dir pilots/mlb-2026-08-03-to-2026-08-09",
            "PYTHONPATH=src python3 prospective_blind_audit.py status --pilot-dir pilots/mlb-2026-08-03-to-2026-08-09",
            "PYTHONPATH=src python3 prospective_blind_audit.py reveal --pilot-dir pilots/mlb-2026-08-03-to-2026-08-09",
            "```",
            "",
        ]
    )


def write_freeze(
    pilot_dir: Path,
    schedule_bytes: bytes,
    standings_bytes: bytes,
    manifest: dict[str, Any],
) -> None:
    if pilot_dir.exists():
        raise PilotError(f"pilot directory already exists; refusing overwrite: {pilot_dir}")
    (pilot_dir / "sources").mkdir(parents=True)
    _atomic_write(pilot_dir / "sources" / "schedule.json", schedule_bytes)
    _atomic_write(pilot_dir / "sources" / "standings.json", standings_bytes)
    atomic_json(pilot_dir / "freeze.json", manifest)
    freeze_sha = sha256_file(pilot_dir / "freeze.json")
    _atomic_write(pilot_dir / "freeze.sha256", f"{freeze_sha}  freeze.json\n".encode("ascii"))
    _atomic_write(
        pilot_dir / "README.md", render_freeze_readme(manifest, freeze_sha).encode("utf-8")
    )


def _read_manifest(pilot_dir: Path) -> dict[str, Any]:
    path = pilot_dir / "freeze.json"
    if not path.is_file():
        raise PilotError(f"missing freeze manifest: {path}")
    return parse_json_bytes(path.read_bytes(), str(path))


def _expected_sidecar(pilot_dir: Path, name: str) -> str:
    path = pilot_dir / f"{name}.sha256"
    try:
        line = path.read_text(encoding="ascii").strip()
    except FileNotFoundError as exc:
        raise PilotError(f"missing digest sidecar: {path}") from exc
    parts = line.split()
    if len(parts) != 2 or parts[1] != f"{name}.json":
        raise PilotError(f"malformed digest sidecar: {path}")
    return parts[0]


def verify_freeze(pilot_dir: Path) -> dict[str, Any]:
    manifest = _read_manifest(pilot_dir)
    if manifest.get("schema") != SCHEMA or manifest.get("outcome_state") != "ABSENT_BY_DESIGN":
        raise PilotError("freeze schema or outcome state is invalid")
    actual_file_sha = sha256_file(pilot_dir / "freeze.json")
    if actual_file_sha != _expected_sidecar(pilot_dir, "freeze"):
        raise PilotError("freeze.json does not match freeze.sha256")
    commitment = sha256_bytes(canonical_bytes(_manifest_core(manifest)))
    if commitment != manifest.get("commitment_sha256"):
        raise PilotError("manifest core commitment does not match")
    schedule_path = pilot_dir / "sources" / "schedule.json"
    standings_path = pilot_dir / "sources" / "standings.json"
    if sha256_file(schedule_path) != manifest["sources"]["schedule"]["sha256"]:
        raise PilotError("schedule snapshot digest does not match")
    if sha256_file(standings_path) != manifest["sources"]["standings"]["sha256"]:
        raise PilotError("standings snapshot digest does not match")
    for item in manifest["items"]:
        forbidden = FORBIDDEN_ITEM_KEYS.intersection(item)
        if forbidden:
            raise PilotError(f"freeze item contains outcome-bearing keys: {sorted(forbidden)}")
        if iso_utc(item["game_date"]) <= iso_utc(manifest["frozen_at_utc"]):
            raise PilotError("freeze contains an item that was not future")
    rebuilt_items = build_items(
        parse_json_bytes(schedule_path.read_bytes(), str(schedule_path)),
        parse_json_bytes(standings_path.read_bytes(), str(standings_path)),
        manifest["frozen_at_utc"],
    )
    if rebuilt_items != manifest["items"]:
        raise PilotError("items do not recompute from committed source snapshots")
    rebuilt_orders, rebuilt_certificate = build_orders(
        rebuilt_items, int(manifest["randomization"]["seed"])
    )
    if rebuilt_orders != manifest["orders"] or rebuilt_certificate != manifest["quota_certificate"]:
        raise PilotError("orders or quota certificate do not recompute")
    item_ids = [item["game_pk"] for item in manifest["items"]]
    if len(item_ids) != manifest["cohort"]["item_count"] or len(set(item_ids)) != len(item_ids):
        raise PilotError("cohort item count or uniqueness is invalid")
    for name, order in manifest["orders"].items():
        if sorted(order["game_pks"]) != sorted(item_ids):
            raise PilotError(f"{name} is not a complete cohort permutation")
        if order_digest(name, order["game_pks"]) != order["sha256"]:
            raise PilotError(f"{name} digest does not match its sequence")
    return {
        "freeze_verified": True,
        "pilot_id": manifest["pilot_id"],
        "items": len(item_ids),
        "freeze_file_sha256": actual_file_sha,
        "commitment_sha256": commitment,
        "orders": {name: value["sha256"] for name, value in manifest["orders"].items()},
    }


def extract_live_games(payload: dict[str, Any]) -> dict[int, dict[str, Any]]:
    games: dict[int, dict[str, Any]] = {}
    for date in payload.get("dates", []):
        for game in date.get("games", []):
            game_pk = int(game["gamePk"])
            teams = game["teams"]
            status = game["status"]
            entry: dict[str, Any] = {
                "game_pk": game_pk,
                "game_date": str(game["gameDate"]),
                "status_abstract": str(status["abstractGameState"]),
                "status_detail": str(status["detailedState"]),
            }
            for side in ("away", "home"):
                entry[f"{side}_team_id"] = int(teams[side]["team"]["id"])
                if "score" in teams[side]:
                    entry[f"{side}_score"] = int(teams[side]["score"])
            games[game_pk] = entry
    return games


def live_status(manifest: dict[str, Any], live_payload: dict[str, Any]) -> dict[str, Any]:
    games = extract_live_games(live_payload)
    fixed = manifest["cohort"]["fixed_game_pks"]
    missing = [game_pk for game_pk in fixed if game_pk not in games]
    final = [game_pk for game_pk in fixed if games.get(game_pk, {}).get("status_abstract") == "Final"]
    pending = [game_pk for game_pk in fixed if game_pk in games and game_pk not in final]
    return {
        "item_count": len(fixed),
        "final_count": len(final),
        "pending_count": len(pending),
        "missing_count": len(missing),
        "all_final": len(final) == len(fixed),
        "pending_game_pks": pending,
        "missing_game_pks": missing,
    }


def _order_indices(manifest: dict[str, Any], name: str) -> list[int]:
    index = {item["game_pk"]: position for position, item in enumerate(manifest["items"])}
    return [index[game_pk] for game_pk in manifest["orders"][name]["game_pks"]]


def distribution_free_path(outcomes: list[int], order: list[int]) -> dict[str, Any]:
    total = len(outcomes)
    successes = 0
    lower: list[float] = []
    upper: list[float] = []
    width: list[float] = []
    for prefix, index in enumerate(order, 1):
        successes += outcomes[index]
        remaining = total - prefix
        lo = successes / total
        hi = (successes + remaining) / total
        lower.append(lo)
        upper.append(hi)
        width.append(hi - lo)
    return {"lower": lower, "upper": upper, "width": width}


def trajectory(outcomes: list[int], order: list[int], items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    final_accuracy = sum(outcomes) / len(outcomes)
    running = 0
    rows: list[dict[str, Any]] = []
    for prefix, index in enumerate(order, 1):
        running += outcomes[index]
        estimate = running / prefix
        error = estimate - final_accuracy
        rows.append(
            {
                "prefix": prefix,
                "game_pk": items[index]["game_pk"],
                "correct": outcomes[index],
                "running_accuracy": estimate,
                "signed_error": error,
                "absolute_error": abs(error),
            }
        )
    return rows


def analyze(manifest: dict[str, Any], live_payload: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    status = live_status(manifest, live_payload)
    if not status["all_final"]:
        raise PilotError(
            f"reveal blocked: {status['final_count']}/{status['item_count']} final, "
            f"{status['pending_count']} pending, {status['missing_count']} missing"
        )
    games = extract_live_games(live_payload)
    outcomes: list[int] = []
    revealed: list[dict[str, Any]] = []
    for item in manifest["items"]:
        game = games[item["game_pk"]]
        if game.get("home_team_id") != item["home_team_id"] or game.get("away_team_id") != item["away_team_id"]:
            raise PilotError(f"team identity changed for game {item['game_pk']}")
        if "home_score" not in game or "away_score" not in game:
            raise PilotError(f"final game lacks score: {item['game_pk']}")
        if game["home_score"] == game["away_score"]:
            raise PilotError(f"final game has tied score: {item['game_pk']}")
        winner = "home" if game["home_score"] > game["away_score"] else "away"
        correct = int(winner == item["predicted_side"])
        outcomes.append(correct)
        revealed.append(
            {
                "game_pk": item["game_pk"],
                "home_score": game["home_score"],
                "away_score": game["away_score"],
                "winner_side": winner,
                "correct": correct,
            }
        )
    strata = [item["stratum"] for item in manifest["items"]]
    warmup = int(manifest["analysis_preregistration"]["warmup"])
    order_results: dict[str, Any] = {}
    for name in ("quota_balanced", "seeded_random", "production"):
        order = _order_indices(manifest, name)
        rows = trajectory(outcomes, order, manifest["items"])
        tail = rows[warmup - 1 :]
        descriptive = {
            "integrated_absolute_prefix_error": statistics.fmean(row["absolute_error"] for row in tail),
            "integrated_squared_prefix_error": statistics.fmean(row["signed_error"] ** 2 for row in tail),
            "one_percent_settling_prefix": next(
                (
                    prefix
                    for prefix in range(1, len(rows) + 1)
                    if all(row["absolute_error"] <= 0.01 for row in rows[prefix - 1 :])
                ),
                len(rows),
            ),
        }
        worst_case = distribution_free_path(outcomes, order)
        stopping: dict[str, Any] = {
            "distribution_free_exact_5pp": safe.first_stop(worst_case, 0.05),
            "randomization_exact_5pp": None,
            "randomization_certificate": "ineligible: order has no committed random-within-stratum mechanism",
        }
        if manifest["orders"][name]["randomization_certified"]:
            exact = safe.confidence_path(outcomes, order, strata, alpha=0.05)
            stopping = {
                "distribution_free_exact_5pp": safe.first_stop(worst_case, 0.05),
                "randomization_exact_5pp": safe.first_stop(exact, 0.05),
                "randomization_simultaneous_coverage": exact["simultaneous_coverage"],
                "randomization_manifest_sha256": exact["manifest_sha256"],
                "randomization_certificate": "eligible: committed random priorities are outcome-blind",
            }
        order_results[name] = {
            "prefix_metrics": descriptive,
            "stopping": stopping,
            "trajectory": rows,
            "trajectory_sha256": sha256_bytes(canonical_bytes(rows)),
        }
    return revealed, {
        "final_accuracy": sum(outcomes) / len(outcomes),
        "correct_count": sum(outcomes),
        "item_count": len(outcomes),
        "warmup": warmup,
        "orders": order_results,
    }


def _result_core(result: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in result.items() if key != "commitment_sha256"}


def render_result_report(result: dict[str, Any]) -> str:
    analysis = result["analysis"]
    lines = [
        "# Prospective blind audit result",
        "",
        f"Pilot: `{result['pilot_id']}`",
        f"Revealed: `{result['revealed_at_utc']}`",
        f"Final model accuracy: **{analysis['final_accuracy']:.1%}** ({analysis['correct_count']}/{analysis['item_count']})",
        "",
        "| order | integrated absolute prefix error | exact distribution-free 5pp stop | exact randomization 5pp stop |",
        "|---|---:|---:|---:|",
    ]
    for name in ("quota_balanced", "seeded_random", "production"):
        entry = analysis["orders"][name]
        randomized = entry["stopping"]["randomization_exact_5pp"]
        lines.append(
            f"| {name} | {entry['prefix_metrics']['integrated_absolute_prefix_error']:.6f} | "
            f"{entry['stopping']['distribution_free_exact_5pp']} | "
            f"{randomized if randomized is not None else 'ineligible'} |"
        )
    lines.extend(
        [
            "",
            "The production order has no random-within-stratum mechanism, so assigning it a hypergeometric 'exact' stopping certificate would be invalid. Its distribution-free bound remains exact and comparable.",
            "",
            f"Freeze SHA-256: `{result['freeze_file_sha256']}`",
            f"Result commitment SHA-256: `{result['commitment_sha256']}`",
            "",
        ]
    )
    return "\n".join(lines)


def build_result(
    pilot_dir: Path, live_bytes: bytes, *, reveal_source: str, revealed_at: str
) -> dict[str, Any]:
    verify_freeze(pilot_dir)
    manifest = _read_manifest(pilot_dir)
    live_payload = parse_json_bytes(live_bytes, "reveal snapshot")
    revealed, analysis = analyze(manifest, live_payload)
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "pilot_id": manifest["pilot_id"],
        "freeze_file_sha256": sha256_file(pilot_dir / "freeze.json"),
        "freeze_commitment_sha256": manifest["commitment_sha256"],
        "revealed_at_utc": revealed_at,
        "source": {"url": reveal_source, "sha256": sha256_bytes(live_bytes)},
        "outcomes": revealed,
        "analysis": analysis,
    }
    result["commitment_sha256"] = sha256_bytes(canonical_bytes(_result_core(result)))
    return result


def write_result(pilot_dir: Path, live_bytes: bytes, result: dict[str, Any]) -> None:
    if (pilot_dir / "result.json").exists() or (pilot_dir / "sources" / "reveal.json").exists():
        raise PilotError("result already exists; refusing overwrite")
    _atomic_write(pilot_dir / "sources" / "reveal.json", live_bytes)
    atomic_json(pilot_dir / "result.json", result)
    result_sha = sha256_file(pilot_dir / "result.json")
    _atomic_write(pilot_dir / "result.sha256", f"{result_sha}  result.json\n".encode("ascii"))
    _atomic_write(pilot_dir / "RESULT.md", render_result_report(result).encode("utf-8"))


def verify_result(pilot_dir: Path) -> dict[str, Any]:
    freeze_report = verify_freeze(pilot_dir)
    path = pilot_dir / "result.json"
    if not path.exists():
        return {**freeze_report, "result_state": "NOT_REVEALED"}
    result = parse_json_bytes(path.read_bytes(), str(path))
    if result.get("schema") != RESULT_SCHEMA:
        raise PilotError("result schema is invalid")
    if sha256_file(path) != _expected_sidecar(pilot_dir, "result"):
        raise PilotError("result.json does not match result.sha256")
    if result["freeze_file_sha256"] != sha256_file(pilot_dir / "freeze.json"):
        raise PilotError("result is not bound to the current freeze")
    if result["commitment_sha256"] != sha256_bytes(canonical_bytes(_result_core(result))):
        raise PilotError("result core commitment does not match")
    reveal_path = pilot_dir / "sources" / "reveal.json"
    if sha256_file(reveal_path) != result["source"]["sha256"]:
        raise PilotError("reveal source digest does not match")
    rebuilt = build_result(
        pilot_dir,
        reveal_path.read_bytes(),
        reveal_source=result["source"]["url"],
        revealed_at=result["revealed_at_utc"],
    )
    if rebuilt != result:
        raise PilotError("result does not recompute from freeze and reveal snapshots")
    return {
        **freeze_report,
        "result_state": "VERIFIED",
        "result_file_sha256": sha256_file(path),
        "result_commitment_sha256": result["commitment_sha256"],
    }


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def command_freeze(args: argparse.Namespace) -> int:
    schedule_source = schedule_url(args.start_date, args.end_date)
    standings_source = standings_url(int(args.start_date[:4]))
    schedule_bytes = fetch_bytes(schedule_source)
    standings_bytes = fetch_bytes(standings_source)
    frozen_at = utc_now()
    manifest = build_freeze_manifest(
        schedule_bytes,
        standings_bytes,
        schedule_source=schedule_source,
        standings_source=standings_source,
        frozen_at=frozen_at,
        start_date=args.start_date,
        end_date=args.end_date,
        seed=args.seed,
        pilot_id=args.pilot_id,
    )
    write_freeze(args.pilot_dir, schedule_bytes, standings_bytes, manifest)
    print(json.dumps(verify_freeze(args.pilot_dir), indent=2, sort_keys=True))
    return 0


def _fetch_live(manifest: dict[str, Any]) -> tuple[str, bytes, dict[str, Any]]:
    url = reveal_url(manifest["cohort"]["fixed_game_pks"])
    value = fetch_bytes(url)
    return url, value, parse_json_bytes(value, "live schedule")


def command_status(args: argparse.Namespace) -> int:
    verify_freeze(args.pilot_dir)
    manifest = _read_manifest(args.pilot_dir)
    _, _, payload = _fetch_live(manifest)
    print(json.dumps(live_status(manifest, payload), indent=2, sort_keys=True))
    return 0


def command_reveal(args: argparse.Namespace) -> int:
    verify_freeze(args.pilot_dir)
    manifest = _read_manifest(args.pilot_dir)
    url, live_bytes, payload = _fetch_live(manifest)
    status = live_status(manifest, payload)
    if not status["all_final"]:
        print(json.dumps(status, indent=2, sort_keys=True))
        return 3
    result = build_result(args.pilot_dir, live_bytes, reveal_source=url, revealed_at=utc_now())
    write_result(args.pilot_dir, live_bytes, result)
    print(json.dumps(verify_result(args.pilot_dir), indent=2, sort_keys=True))
    return 0


def command_verify(args: argparse.Namespace) -> int:
    print(json.dumps(verify_result(args.pilot_dir), indent=2, sort_keys=True))
    return 0


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    subparsers = result.add_subparsers(dest="command", required=True)
    freeze = subparsers.add_parser("freeze", help="freeze a new outcome-blind pilot")
    freeze.add_argument("--pilot-dir", type=Path, required=True)
    freeze.add_argument("--start-date", default=DEFAULT_START)
    freeze.add_argument("--end-date", default=DEFAULT_END)
    freeze.add_argument("--seed", type=int, default=DEFAULT_SEED)
    freeze.add_argument("--pilot-id", default=PILOT_ID)
    freeze.set_defaults(function=command_freeze)
    for name, function in (
        ("status", command_status),
        ("reveal", command_reveal),
        ("verify", command_verify),
    ):
        subparser = subparsers.add_parser(name)
        subparser.add_argument("--pilot-dir", type=Path, required=True)
        subparser.set_defaults(function=function)
    return result


def main() -> int:
    args = parser().parse_args()
    try:
        return int(args.function(args))
    except PilotError as exc:
        print(f"ERROR: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
