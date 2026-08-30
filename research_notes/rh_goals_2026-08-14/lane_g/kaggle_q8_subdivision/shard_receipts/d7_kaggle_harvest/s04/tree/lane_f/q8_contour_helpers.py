"""Tracked closed-contour helpers used by the q=8 finite Taylor probe."""

from __future__ import annotations

from typing import Any

from flint import acb, arb


def definitely_positive(value: arb) -> bool:
    return value.lower() > arb(0)


def arb_text(value: arb, digits: int = 80) -> str:
    return value.str(digits, more=True)


def min_arb(values: list[arb]) -> arb:
    if not values:
        raise ValueError("min_arb requires a nonempty list")
    result = values[0]
    for value in values[1:]:
        result = arb.min(result, value)
    return result


def closed_boundary_segments(center_re, center_im, hx, hy, k_per_edge=4):
    segments: list[dict[str, Any]] = []
    K = arb(k_per_edge)

    def add(edge, edge_name, edge_index, start, end):
        re_lo = arb.min(start.real, end.real)
        re_hi = arb.max(start.real, end.real)
        im_lo = arb.min(start.imag, end.imag)
        im_hi = arb.max(start.imag, end.imag)
        segments.append({
            "arc_index": len(segments), "edge": edge, "edge_name": edge_name,
            "edge_index": edge_index, "start": start, "end": end,
            "s_box": acb(arb((re_lo + re_hi) / arb(2), (re_hi - re_lo) / arb(2)),
                         arb((im_lo + im_hi) / arb(2), (im_hi - im_lo) / arb(2))),
        })

    for t in range(k_per_edge):
        x0 = center_re - hx + arb(2 * t) * hx / K
        x1 = center_re - hx + arb(2 * (t + 1)) * hx / K
        add(0, "bottom", t, acb(x0, center_im - hy), acb(x1, center_im - hy))
    for t in range(k_per_edge):
        y0 = center_im - hy + arb(2 * t) * hy / K
        y1 = center_im - hy + arb(2 * (t + 1)) * hy / K
        add(1, "right", t, acb(center_re + hx, y0), acb(center_re + hx, y1))
    for t in range(k_per_edge):
        x0 = center_re + hx - arb(2 * t) * hx / K
        x1 = center_re + hx - arb(2 * (t + 1)) * hx / K
        add(2, "top", t, acb(x0, center_im + hy), acb(x1, center_im + hy))
    for t in range(k_per_edge):
        y0 = center_im + hy - arb(2 * t) * hy / K
        y1 = center_im + hy - arb(2 * (t + 1)) * hy / K
        add(3, "left", t, acb(center_re - hx, y0), acb(center_re - hx, y1))
    return segments


def interval_intersection(left: arb, right: arb) -> arb | None:
    lower = max(left.lower(), right.lower())
    upper = min(left.upper(), right.upper())
    if lower > upper:
        return None
    return arb((lower + upper) / arb(2), (upper - lower) / arb(2))


def box_intersection(left: acb, right: acb) -> acb | None:
    real = interval_intersection(left.real, right.real)
    imag = interval_intersection(left.imag, right.imag)
    return None if real is None or imag is None else acb(real, imag)


def right_half_plane_rotation(value: acb) -> tuple[acb, str] | None:
    for rotation, label in ((acb(1), "1"), (acb(-1), "-1"), (acb(0, -1), "-i"), (acb(0, 1), "i")):
        if (rotation * value).real.lower() > 0:
            return rotation, label
    return None


def argument_interval(value: acb) -> arb:
    result = value.arg()
    return result.real if hasattr(result, "real") else result


def certified_winding_from_arc_boxes(boxes: list[acb]) -> tuple[int | None, dict[str, Any]]:
    if any(not definitely_positive(box.abs_lower()) for box in boxes):
        bad = next(index for index, box in enumerate(boxes) if not definitely_positive(box.abs_lower()))
        return None, {"reason": "arc determinant box contains zero", "bad_arc": bad}
    endpoints = []
    for index in range(len(boxes)):
        intersection = box_intersection(boxes[index - 1], boxes[index])
        if intersection is None:
            return None, {"reason": "adjacent determinant boxes do not overlap", "endpoint": index}
        endpoints.append(intersection)
    total = arb(0)
    records = []
    for index, box in enumerate(boxes):
        selected = right_half_plane_rotation(box)
        if selected is None:
            return None, {"reason": "no certified half-plane rotation", "arc": index}
        rotation, label = selected
        start = rotation * endpoints[index]
        end = rotation * endpoints[(index + 1) % len(endpoints)]
        if start.real.lower() <= 0 or end.real.lower() <= 0:
            return None, {"reason": "endpoint intersection escapes rotated half-plane", "arc": index}
        delta = argument_interval(end) - argument_interval(start)
        total += delta
        records.append({"arc": index, "rotation": label, "start_arg": arb_text(argument_interval(start)),
                        "end_arg": arb_text(argument_interval(end)), "delta": arb_text(delta)})
    winding_ball = total / (arb(2) * arb.pi())
    nearest = round(float(winding_ball.mid()))
    pinned = winding_ball.lower() > arb(nearest) - arb(1) / 2 and winding_ball.upper() < arb(nearest) + arb(1) / 2
    return (nearest if pinned else None), {"winding_ball": arb_text(winding_ball), "candidate_integer": nearest,
        "integer_pinned": bool(pinned), "arc_argument_records": records}
