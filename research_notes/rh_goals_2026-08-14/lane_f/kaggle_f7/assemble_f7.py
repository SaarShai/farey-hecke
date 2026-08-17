#!/usr/bin/env python3
"""F7 R3b assembly: merge the 16 banked chunk receipts into one closed-contour
verdict for the 192-arc boundary of the q=7 pin box.

No new mathematics: the winding and adjacent-box closure test are the pinned
orchestrator's own `merge_chunks_and_verify_closure` /
`certified_winding_via_overlap_polygon` (imported, not re-implemented), so the
merged verdict is produced by exactly the code the chunks were certified with.
This script adds only the assembly-level gates the chunked run defers:

1. coverage: the 16 `chunk_arc_range`s tile [0,192) once, contiguously;
2. hash pinning: engine / R2 / TB_V2 / orchestrator / derivative / endpoint
   sha256s, plus the R2 constants block, identical in all 16 receipts;
3. seam closure: at every one of the 16 chunk seams, the geometric contour
   endpoint chains (s_end of the last arc of chunk i equals s_start of the
   first arc of chunk i+1, as Arb balls) and the determinant boxes overlap;
4. global margins: min minimum_finite_lower_minus_F_margin (rounded DOWN),
   max maximum_rH (rounded UP), total arc/subarc counts;
5. the final gate: winding 1, all enclosures exclude zero, complete cover,
   positive margin.

All gate comparisons use Arb ball bounds, never bare floats.

Usage: /Users/za/.venvs/farey-rh/bin/python assemble_f7.py [--write]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from decimal import Decimal
from pathlib import Path
from typing import Any

from flint import acb, arb, ctx

LANE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LANE_DIR))

import f7_certify_r3b_flagship as f7  # noqa: E402
import certify_r3_flagship as r3_attempt1  # noqa: E402

HARVEST = Path(__file__).resolve().parent / "harvest"
RECEIPT_OUT = LANE_DIR / "F7_R3B_ASSEMBLY_RECEIPT.json"
REPORT_OUT = LANE_DIR / "F7_R3B_ASSEMBLY_CERT.md"

SCHEMA = "f7-r3b-assembly-certificate/v1"
PRECISION_BITS = 384
N_PRIMARY = f7.N_PRIMARY
N_COMPARISON = f7.N_COMPARISON
BASE_ARCS = 4 * f7.K_PER_EDGE
CHUNK_COUNT = 16

RECOVERY_ROOT = Path("/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/out")

HASH_KEYS = (
    "R2_receipt",
    "TB_V2_receipt",
    "attempt1_report",
    "R1_restatement",
    "engine",
    "R2_code",
    "R3b_orchestrator",
    "R3b_derivative",
    "R3b_endpoint",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_sha(obj: Any) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def arb_text(value: arb) -> str:
    return f7.arb_text(value)


def _directed_decimal(value: arb, digits: int, upward: bool) -> str:
    """Plain decimal string that is certified to lie on the safe side of the
    ball: `upward=False` returns d <= inf(value), `upward=True` d >= sup(value).
    The inequality is re-checked in Arb, and the last decimal place is nudged
    until it holds, so no bare float ever enters a gate value.
    """
    bound = arb(value.upper()) if upward else arb(value.lower())
    text = bound.str(digits, radius=False)
    candidate = Decimal(text)
    step = Decimal(1).scaleb(candidate.as_tuple().exponent)
    for _ in range(8):
        probe = arb(str(candidate))
        if upward and (probe >= bound) is True:
            return str(candidate)
        if not upward and (probe <= bound) is True:
            return str(candidate)
        candidate = candidate + step if upward else candidate - step
    raise AssertionError(f"could not round {'up' if upward else 'down'}: {text}")


def down(value: arb, digits: int = 24) -> str:
    """Certified DOWNward-rounded decimal string for a lower bound."""
    return _directed_decimal(value, digits, upward=False)


def up(value: arb, digits: int = 24) -> str:
    """Certified UPward-rounded decimal string for an upper bound."""
    return _directed_decimal(value, digits, upward=True)


def load_chunks() -> list[dict[str, Any]]:
    chunks = []
    for index in range(CHUNK_COUNT):
        path = HARVEST / f"chunk-{index:02d}" / f"F7_R3B_CHUNK_{index:02d}_RECEIPT.json"
        if not path.is_file():
            raise FileNotFoundError(f"missing chunk receipt: {path}")
        with path.open(encoding="utf-8") as handle:
            chunks.append({
                "index": index,
                "path": path,
                "receipt_sha256": sha256_file(path),
                "receipt": json.load(handle),
            })
    return chunks


def gate_coverage(chunks: list[dict[str, Any]]) -> dict[str, Any]:
    ranges = []
    for chunk in chunks:
        cover = chunk["receipt"]["closed_contour"][str(N_PRIMARY)]
        ranges.append((tuple(cover["chunk_arc_range"]), chunk["index"]))
    ranges.sort()
    cursor = 0
    failures = []
    for (start, end), index in ranges:
        if start != cursor:
            failures.append({
                "chunk": index,
                "reason": "seam gap or overlap",
                "expected_start": cursor,
                "chunk_start": start,
            })
        cursor = max(cursor, end)
    if cursor != BASE_ARCS:
        failures.append({
            "reason": "merged ranges do not tile the base cover",
            "merged_end": cursor,
            "expected": BASE_ARCS,
        })
    return {
        "pass": not failures,
        "chunk_arc_ranges": [list(pair[0]) for pair in ranges],
        "tiles_exactly": [0, BASE_ARCS] if not failures else None,
        "failures": failures,
    }


def gate_hashes(chunks: list[dict[str, Any]]) -> dict[str, Any]:
    binding_values: dict[str, set[str]] = {key: set() for key in HASH_KEYS}
    paths: dict[str, str] = {}
    for chunk in chunks:
        bindings = chunk["receipt"]["source_bindings"]
        for key in HASH_KEYS:
            binding_values[key].add(bindings[key]["sha256"])
            paths[key] = bindings[key]["path"]
    mismatched = {k: sorted(v) for k, v in binding_values.items() if len(v) != 1}
    r2_constants = {canonical_sha(c["receipt"]["R2_constants"]) for c in chunks}
    precisions = {c["receipt"]["precision_bits"] for c in chunks}
    immutables = {c["receipt"]["immutable_hashes_verified"] for c in chunks}
    pinned = {
        "R2_receipt_matches_orchestrator_pin":
            next(iter(binding_values["R2_receipt"])) == f7.R2_EXPECTED_SHA256
            if len(binding_values["R2_receipt"]) == 1 else False,
        "TB_V2_receipt_matches_orchestrator_pin":
            next(iter(binding_values["TB_V2_receipt"])) == f7.TB_V2_EXPECTED_SHA256
            if len(binding_values["TB_V2_receipt"]) == 1 else False,
    }
    live = {}
    for key in HASH_KEYS:
        path = Path(paths[key])
        live[key] = sha256_file(path) if path.is_file() else None
    live_agrees = {
        key: (live[key] is not None and {live[key]} == binding_values[key])
        for key in HASH_KEYS
    }
    # A binding whose PRIMARY path has drifted since the run is a provenance
    # note, not a cross-chunk mismatch (all 16 chunks still agree on the sha
    # they ran). Recover the certified bytes from the run-time copies kept
    # under code/out/kaggle_top4/ and record where they are.
    drift = {}
    for key in HASH_KEYS:
        if live_agrees[key]:
            continue
        wanted = sorted(binding_values[key])[0]
        found = None
        name = Path(paths[key]).name
        for candidate in sorted(RECOVERY_ROOT.rglob(name)):
            if sha256_file(candidate) == wanted:
                found = str(candidate)
                break
        drift[key] = {
            "primary_path": paths[key],
            "receipt_sha256": wanted,
            "live_primary_sha256": live[key],
            "certified_bytes_recovered_at": found,
            "all_16_chunks_agree_on_receipt_sha256": len(binding_values[key]) == 1,
        }
    return {
        "pass": (
            not mismatched
            and len(r2_constants) == 1
            and precisions == {PRECISION_BITS}
            and immutables == {True}
            and all(pinned.values())
        ),
        "common_source_bindings": {
            key: {"path": paths[key], "sha256": sorted(binding_values[key])[0]}
            for key in HASH_KEYS
        },
        "mismatched_bindings": mismatched,
        "R2_constants_canonical_sha256": sorted(r2_constants),
        "precision_bits": sorted(precisions),
        "immutable_hashes_verified": sorted(immutables),
        "orchestrator_pin_agreement": pinned,
        "live_file_sha256_agrees_with_receipts": live_agrees,
        "primary_path_drift_since_run": drift,
        "chunk_receipt_sha256": {
            f"chunk-{c['index']:02d}": c["receipt_sha256"] for c in chunks
        },
    }


def merged_records(chunks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    covers = sorted(
        (chunk["receipt"]["closed_contour"][str(N_PRIMARY)] for chunk in chunks),
        key=lambda cover: cover["chunk_arc_range"][0],
    )
    return [
        record
        for cover in covers
        for record in sorted(cover["records"], key=f7._lineage_sort_key)
    ]


def _ball_pair_agree(left: dict[str, str], right: dict[str, str]) -> bool:
    """Two recorded Acb endpoints agree if each coordinate ball overlaps and the
    mid-points are contained in the other's ball (certified endpoint chaining)."""
    a = f7.acb_from_text(left)
    b = f7.acb_from_text(right)
    for x, y in ((a.real, b.real), (a.imag, b.imag)):
        if not (x - y).contains(0):
            return False
        if not (x.contains(arb(y.mid())) and y.contains(arb(x.mid()))):
            return False
    return True


def gate_seams(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Re-verify closure at every arc junction, and report the 16 chunk seams
    explicitly (the plan's REQUIRED seam-closure re-verification)."""
    total = len(records)
    seam_indices = [(index * (BASE_ARCS // CHUNK_COUNT)) % BASE_ARCS for index in range(CHUNK_COUNT)]
    junctions = []
    all_geometry_ok = True
    all_boxes_ok = True
    for index in range(total):
        previous = records[index - 1]
        current = records[index]
        geometry_ok = _ball_pair_agree(previous["s_end"], current["s_start"])
        left = f7.acb_from_text(previous["finite_Taylor_det_box"])
        right = f7.acb_from_text(current["finite_Taylor_det_box"])
        intersection = r3_attempt1.box_intersection(left, right)
        box_ok = intersection is not None
        all_geometry_ok &= geometry_ok
        all_boxes_ok &= box_ok
        if index in seam_indices:
            junctions.append({
                "junction_base_arc_index": index,
                "left_chunk": (index - 1) % BASE_ARCS // (BASE_ARCS // CHUNK_COUNT),
                "right_chunk": index // (BASE_ARCS // CHUNK_COUNT),
                "left_arc_index": previous["base_arc_index"],
                "right_arc_index": current["base_arc_index"],
                "contour_endpoints_chain": geometry_ok,
                "adjacent_finite_det_boxes_overlap": box_ok,
                "s_junction": current["s_start"],
            })
    contiguous_indices = [record["base_arc_index"] for record in records]
    return {
        "pass": all_geometry_ok and all_boxes_ok and contiguous_indices == list(range(BASE_ARCS)),
        "junction_count_checked": total,
        "all_contour_endpoints_chain": all_geometry_ok,
        "all_adjacent_finite_det_boxes_overlap": all_boxes_ok,
        "merged_base_arc_indices_are_0_to_191_in_order": contiguous_indices == list(range(BASE_ARCS)),
        "chunk_seam_count": len(junctions),
        "chunk_seams": junctions,
    }


def gate_margins(chunks: list[dict[str, Any]], records: list[dict[str, Any]]) -> dict[str, Any]:
    per_chunk = []
    min_margin = None
    min_finite_lower = None
    max_rH = None
    max_rG = None
    accepted = 0
    evaluations = 0
    splits = 0
    for chunk in chunks:
        cover = chunk["receipt"]["closed_contour"][str(N_PRIMARY)]
        margin = arb(cover["minimum_finite_lower_minus_F_margin"])
        finite_lower = arb(cover["minimum_finite_Taylor_abs_lower_bound"])
        rH = arb(cover["maximum_rH"])
        rG = arb(cover["maximum_Taylor_radius"])
        min_margin = margin if min_margin is None else arb.min(min_margin, margin)
        min_finite_lower = (
            finite_lower if min_finite_lower is None else arb.min(min_finite_lower, finite_lower)
        )
        max_rH = rH if max_rH is None else arb.max(max_rH, rH)
        max_rG = rG if max_rG is None else arb.max(max_rG, rG)
        accepted += cover["accepted_closed_subarc_count"]
        evaluations += cover["arc_evaluation_count"]
        splits += cover["adaptive_subdivision_count"]
        per_chunk.append({
            "chunk": f"chunk-{chunk['index']:02d}",
            "chunk_arc_range": cover["chunk_arc_range"],
            "status": cover["status"],
            "chunk_gate_pass": bool(cover["chunk_gate_pass"]),
            "complete_closed_cover": bool(cover["complete_closed_cover"]),
            "accepted_closed_subarc_count": cover["accepted_closed_subarc_count"],
            "adaptive_subdivision_count": cover["adaptive_subdivision_count"],
            "all_finite_Taylor_enclosures_exclude_zero":
                bool(cover["all_finite_Taylor_enclosures_exclude_zero"]),
            "all_F_inflated_closed_arc_enclosures_exclude_zero":
                bool(cover["all_F_inflated_closed_arc_enclosures_exclude_zero"]),
            "minimum_finite_lower_minus_F_margin": cover["minimum_finite_lower_minus_F_margin"],
            "minimum_finite_lower_minus_F_margin_rounded_down":
                down(arb(cover["minimum_finite_lower_minus_F_margin"])),
            "maximum_rH": cover["maximum_rH"],
            "wall_seconds": cover["wall_seconds"],
        })

    per_arc_margins = [arb(record["finite_lower_minus_F_margin"]) for record in records]
    per_arc_min = per_arc_margins[0]
    for value in per_arc_margins[1:]:
        per_arc_min = arb.min(per_arc_min, value)

    positive = f7.definitely_positive(min_margin) and f7.definitely_positive(per_arc_min)
    rH_below_one = (max_rH < arb(1)) is True
    return {
        "pass": bool(positive and rH_below_one),
        "per_chunk": per_chunk,
        "minimum_finite_lower_minus_F_margin_ball": arb_text(min_margin),
        "minimum_finite_lower_minus_F_margin_rounded_down": down(min_margin),
        "minimum_finite_lower_minus_F_margin_from_per_arc_records_rounded_down": down(per_arc_min),
        "per_arc_and_per_chunk_minima_agree": bool((min_margin - per_arc_min).contains(0)),
        "margin_certified_strictly_positive": bool(positive),
        "minimum_finite_Taylor_abs_lower_bound_ball": arb_text(min_finite_lower),
        "minimum_finite_Taylor_abs_lower_bound_rounded_down": down(min_finite_lower),
        "maximum_Taylor_radius_rG_ball": arb_text(max_rG),
        "maximum_Taylor_radius_rG_rounded_up": up(max_rG),
        "maximum_rH_ball": arb_text(max_rH),
        "maximum_rH_rounded_up": up(max_rH),
        "maximum_rH_strictly_below_one": bool(rH_below_one),
        "total_base_closed_arc_count": BASE_ARCS,
        "total_accepted_closed_subarc_count": accepted,
        "total_arc_evaluation_count": evaluations,
        "total_adaptive_subdivision_count": splits,
        "total_chunk_wall_seconds": sum(
            chunk["receipt"]["closed_contour"][str(N_PRIMARY)]["wall_seconds"] for chunk in chunks
        ),
        "total_chunk_runtime_seconds": sum(
            chunk["receipt"]["runtime_seconds"] for chunk in chunks
        ),
    }


def gate_comparison_arm(chunks: list[dict[str, Any]]) -> dict[str, Any]:
    """The N_COMPARISON arm is the designed NOT_CERTIFIED control: it must FAIL."""
    statuses = sorted({
        chunk["receipt"]["closed_contour"][str(N_COMPARISON)]["status"] for chunk in chunks
    })
    gates = sorted({
        bool(chunk["receipt"]["closed_contour"][str(N_COMPARISON)]["closed_contour_gate_pass"])
        for chunk in chunks
    })
    return {
        "pass": statuses == ["NOT_CERTIFIED"] and gates == [False],
        "N": N_COMPARISON,
        "statuses": statuses,
        "closed_contour_gate_pass": gates,
        "role": "designed control arm; a PASS here would signal a tail-bound bug",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write receipt and report")
    args = parser.parse_args()

    ctx.prec = PRECISION_BITS
    chunks = load_chunks()

    coverage = gate_coverage(chunks)
    hashes = gate_hashes(chunks)
    records = merged_records(chunks)
    seams = gate_seams(records)
    margins = gate_margins(chunks, records)
    control = gate_comparison_arm(chunks)

    covers = [chunk["receipt"]["closed_contour"][str(N_PRIMARY)] for chunk in chunks]
    exclusions = {
        "all_chunks_finite_Taylor_enclosures_exclude_zero": all(
            cover["all_finite_Taylor_enclosures_exclude_zero"] for cover in covers
        ),
        "all_chunks_F_inflated_enclosures_exclude_zero": all(
            cover["all_F_inflated_closed_arc_enclosures_exclude_zero"] for cover in covers
        ),
        "all_chunks_complete_closed_cover": all(
            cover["complete_closed_cover"] for cover in covers
        ),
        "all_chunks_gate_pass": all(cover["chunk_gate_pass"] for cover in covers),
    }

    winding, winding_info = f7.merge_chunks_and_verify_closure(covers, BASE_ARCS)
    increments = winding_info.pop("argument_increment_records", None)
    winding_gate = {
        "pass": winding == 1,
        "merged_winding": winding,
        "winding_ball": winding_info.get("winding_ball"),
        "argument_increment_record_count": len(increments) if increments else 0,
        "info": winding_info,
        "merge_function": "f7_certify_r3b_flagship.merge_chunks_and_verify_closure "
                          "(the pinned orchestrator's own merge/closure routine)",
    }

    gates = {
        "coverage": coverage,
        "hash_pinning": hashes,
        "seam_closure": seams,
        "margins": margins,
        "arc_exclusions": {"pass": all(exclusions.values()), **exclusions},
        "winding": winding_gate,
        "comparison_control_arm": control,
    }
    all_pass = all(gate["pass"] for gate in gates.values())
    verdict = (
        f"THEOREM-GRADE closed-contour YES at N={N_PRIMARY}"
        if all_pass
        else f"closed-contour NO at N={N_PRIMARY} (assembly gate failure)"
    )

    receipt = {
        "schema": SCHEMA,
        "verdict": verdict,
        "all_assembly_gates_pass": all_pass,
        "precision_bits": PRECISION_BITS,
        "backend": "python-flint Arb/Acb ball arithmetic",
        "q": 7,
        "sign": f7.SIGN,
        "pin": {
            "name": "g7_pin_1",
            "re": f7.PIN_RE,
            "im": f7.PIN_IM,
            "coordinate_half_width": f7.PIN_HALF_WIDTH,
        },
        "N_primary": N_PRIMARY,
        "N_comparison": N_COMPARISON,
        "k_per_edge": f7.K_PER_EDGE,
        "base_closed_arc_count": BASE_ARCS,
        "chunk_count": CHUNK_COUNT,
        "exact_factor_strings": list(f7.EXACT_FACTORS),
        "gates": gates,
        "assembly_script_sha256": sha256_file(Path(__file__).resolve()),
    }

    if args.write:
        with RECEIPT_OUT.open("w", encoding="utf-8") as handle:
            json.dump(receipt, handle, indent=2, sort_keys=False)
            handle.write("\n")
        print(f"wrote {RECEIPT_OUT}")

    print(json.dumps({
        "verdict": verdict,
        "gate_pass": {name: gate["pass"] for name, gate in gates.items()},
        "winding": winding,
        "winding_ball": winding_gate["winding_ball"],
        "min_margin_down": margins["minimum_finite_lower_minus_F_margin_rounded_down"],
        "max_rH_up": margins["maximum_rH_rounded_up"],
        "primary_path_drift_since_run": hashes["primary_path_drift_since_run"],
        "accepted_subarcs": margins["total_accepted_closed_subarc_count"],
        "seam_failures": [
            seam for seam in seams["chunk_seams"]
            if not (seam["contour_endpoints_chain"] and seam["adjacent_finite_det_boxes_overlap"])
        ],
    }, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
