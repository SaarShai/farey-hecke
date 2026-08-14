#!/usr/bin/env python3
"""Exact MMS K_s divisor gate for the pinned Hecke-group points.

The source contract is deliberately narrow.  The local MMS extraction gives
the factorization context, while the fetched arXiv PDF supplies Section 6.2:
equations (42)--(43), Lemma 6.3, Proposition 2, and Remark 4.  This module
uses the paper's composition-operator reduction, not a fitted zero pattern.

Run from the repository with:

    /Users/za/.venvs/farey-rh/bin/python code/ks_gate/ks_gate.py

The default output paths are the requested lane_g receipt and report paths.
No input file is modified.
"""

from __future__ import annotations

import argparse
import cmath
import json
import math
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path("/Users/za/Documents/farey-hecke")
WORKTREE_ROOT = Path(__file__).resolve().parents[2]
G5_INPUT = WORKTREE_ROOT / "code/out/resonance_geometry.json"
Q46_INPUT = PROJECT_ROOT / "research_notes/rh_goals_2026-08-14/lane_b/q4q6_winding_receipt.json"
LANE_DIR = PROJECT_ROOT / "research_notes/rh_goals_2026-08-14/lane_g"
DEFAULT_RECEIPT = LANE_DIR / "ks_gate_receipt.json"
DEFAULT_REPORT = LANE_DIR / "KS_GATE_REPORT.md"

RECTANGLE_Q5 = {
    "re_lo": 0.35,
    "re_hi": 0.52,
    "im_lo": 3.0,
    "im_hi": 17.5,
}
ZERO_TOLERANCE = 1.0e-10
DET_TOLERANCE = 1.0e-32

SOURCE = {
    "local_extraction": {
        "path": str(WORKTREE_ROOT / "research_notes/MMS_0912.2236_EXTRACTION.txt"),
        "lines": "26-35",
        "use": "factorization and over-counted-orbit context; Section 6.2 is absent",
    },
    "external_primary": {
        "citation": "Mayer, Mühlenbruch, Strömberg, arXiv:0912.2236v2",
        "url": "https://arxiv.org/pdf/0912.2236",
        "locations": {
            "definition": "§6.2, equations (42)-(43), PDF text lines 2861-2894",
            "determinant_reduction": "Lemma 6.3, PDF text lines 3313-3326",
            "spectrum": "Proposition 2, PDF text lines 3415-3425",
            "closed_multiplier": "Remark 4, PDF text lines 3565-3587",
        },
    },
}


def matmul(left: tuple[float, float, float, float], right: tuple[float, float, float, float]) -> tuple[float, float, float, float]:
    """Multiply 2x2 matrices represented as (a,b,c,d)."""

    a, b, c, d = left
    e, f, g, h = right
    return (
        a * e + b * g,
        a * f + b * h,
        c * e + d * g,
        c * f + d * h,
    )


def branch_matrix(n: int, lam: float) -> tuple[float, float, float, float]:
    """Matrix of the inverse branch theta_n(z) = -1/(z+n*lambda)."""

    return (0.0, -1.0, 1.0, n * lam)


def operator_word(q: int) -> list[int]:
    """Return the scalar-product word from MMS Lemma 6.3."""

    if q % 2 == 0:
        h = (q - 2) // 2
        return [1] * (h - 1) + [2]
    h = (q - 3) // 2
    return [1] * h + [2] + [1] * (h - 1) + [2]


def scalar_composition_matrix(q: int) -> tuple[float, float, float, float]:
    """Matrix of the inverse-branch composition for the scalar determinant.

    If A_s = L_{a_1,s} ... L_{a_m,s}, its argument map is
    theta_{a_m} o ... o theta_{a_1}; hence the matrix product is accumulated
    on the left in operator-word order.
    """

    lam = 2.0 * math.cos(math.pi / q)
    matrix = (1.0, 0.0, 0.0, 1.0)
    for n in operator_word(q):
        matrix = matmul(branch_matrix(n, lam), matrix)
    return matrix


def group_data(q: int) -> dict[str, Any]:
    """Return the exact-lattice constants for q in {4,5,6}."""

    lam = 2.0 * math.cos(math.pi / q)
    matrix = scalar_composition_matrix(q)
    trace = matrix[0] + matrix[3]
    discriminant = trace * trace - 4.0
    ell = (trace - math.sqrt(discriminant)) / 2.0
    log_ell = math.log(ell)
    return {
        "q": q,
        "lambda": lam,
        "operator_word": operator_word(q),
        "composition_matrix": matrix,
        "trace": trace,
        "ell": ell,
        "log_ell": log_ell,
        "a": -log_ell,
        "vertical_spacing": math.pi / (-log_ell),
        "determinant_formula": "prod_{n>=0} (1 - ell_q^(2*s+2*n))",
        "zero_formula": "s = -n + i*pi*k/a_q, n>=0, k in Z",
    }


def det_one_minus_k(q: int, s: complex, tol: float = DET_TOLERANCE) -> tuple[complex, int]:
    """Evaluate the convergent Fredholm-determinant product at s."""

    data = group_data(q)
    log_ell = data["log_ell"]
    value = 1.0 + 0.0j
    for n in range(10000):
        term = cmath.exp((2.0 * s + 2.0 * n) * log_ell)
        value *= 1.0 - term
        if n >= 8 and abs(term) < tol:
            return value, n + 1
    raise RuntimeError(f"determinant product did not converge for q={q}, s={s}")


def nearest_zero(q: int, s: complex) -> dict[str, Any]:
    """Find the nearest point of the exact zero lattice to a point s."""

    data = group_data(q)
    spacing = data["vertical_spacing"]
    n_max = max(4, int(abs(s.real)) + 5)
    k0 = int(round(s.imag / spacing))
    candidates = []
    for n in range(n_max + 1):
        for k in range(k0 - 3, k0 + 4):
            zero = complex(-n, k * spacing)
            candidates.append((abs(s - zero), n, k, zero))
    distance, n, k, zero = min(candidates, key=lambda item: item[0])
    return {
        "distance": distance,
        "n": n,
        "k": k,
        "zero": {"re": zero.real, "im": zero.imag},
    }


def point_to_box_distance(zero: complex, bounds: tuple[float, float, float, float]) -> float:
    """Euclidean distance from a lattice point to a closed rectangular box."""

    re_lo, re_hi, im_lo, im_hi = bounds
    if zero.real < re_lo:
        dx = re_lo - zero.real
    elif zero.real > re_hi:
        dx = zero.real - re_hi
    else:
        dx = 0.0
    if zero.imag < im_lo:
        dy = im_lo - zero.imag
    elif zero.imag > im_hi:
        dy = zero.imag - im_hi
    else:
        dy = 0.0
    return math.hypot(dx, dy)


def box_clearance(q: int, bounds: tuple[float, float, float, float]) -> dict[str, Any]:
    """Find the nearest exact lattice point to a winding box."""

    data = group_data(q)
    spacing = data["vertical_spacing"]
    _, _, im_lo, im_hi = bounds
    k_lo = int(math.floor(im_lo / spacing)) - 2
    k_hi = int(math.ceil(im_hi / spacing)) + 2
    candidates = []
    for n in range(0, 8):
        for k in range(k_lo, k_hi + 1):
            zero = complex(-n, k * spacing)
            candidates.append((point_to_box_distance(zero, bounds), n, k, zero))
    distance, n, k, zero = min(candidates, key=lambda item: item[0])
    return {
        "distance": distance,
        "n": n,
        "k": k,
        "zero": {"re": zero.real, "im": zero.imag},
        "box_bounds": list(bounds),
    }


def rectangle_zeros(q: int, rectangle: dict[str, float]) -> list[dict[str, float]]:
    """Enumerate exact lattice zeros lying in a closed rectangle."""

    data = group_data(q)
    spacing = data["vertical_spacing"]
    zeros = []
    n_lo = max(0, int(math.ceil(-rectangle["re_hi"])))
    n_hi = int(math.floor(-rectangle["re_lo"]))
    if n_lo > n_hi:
        return zeros
    k_lo = int(math.ceil(rectangle["im_lo"] / spacing))
    k_hi = int(math.floor(rectangle["im_hi"] / spacing))
    for n in range(n_lo, n_hi + 1):
        for k in range(k_lo, k_hi + 1):
            zeros.append({"re": float(-n), "im": float(k * spacing)})
    return zeros


def load_pins() -> list[dict[str, Any]]:
    """Load the eight G5 points and five certified q4/q6 winding boxes."""

    with G5_INPUT.open() as handle:
        g5 = json.load(handle)
    pins: list[dict[str, Any]] = []
    for index, pin in enumerate(g5["g5_even_resonances"], start=1):
        pins.append({
            "id": f"g5_pin_{index}",
            "q": 5,
            "re": float(pin["re"]),
            "im": float(pin["im"]),
            "source": str(G5_INPUT),
            "box": None,
        })

    with Q46_INPUT.open() as handle:
        q46 = json.load(handle)
    for pin in q46["pins"]:
        box = pin.get("box")
        bounds = None
        if box is not None:
            bounds = tuple(float(value) for value in box["box_bounds"])
        pins.append({
            "id": pin["label"],
            "q": int(pin["q"]),
            "re": float(pin["target"]["re"]),
            "im": float(pin["target"]["im"]),
            "source": str(Q46_INPUT),
            "box": bounds,
            "winding_status": pin.get("status"),
        })
    return pins


def verdict_for_pin(pin: dict[str, Any]) -> dict[str, Any]:
    q = pin["q"]
    s = complex(pin["re"], pin["im"])
    center_zero = nearest_zero(q, s)
    det_value, terms = det_one_minus_k(q, s)
    if pin["box"] is None:
        clearance = center_zero
        clearance_kind = "point"
    else:
        clearance = box_clearance(q, pin["box"])
        clearance_kind = "closed_winding_box"
    if clearance["distance"] <= ZERO_TOLERANCE:
        verdict = "CONTAMINATED"
    elif clearance["distance"] > ZERO_TOLERANCE:
        verdict = "CLEAR"
    else:
        verdict = "UNRESOLVED"
    return {
        "pin_id": pin["id"],
        "q": q,
        "s": {"re": pin["re"], "im": pin["im"]},
        "input_source": pin["source"],
        "winding_status": pin.get("winding_status"),
        "box_bounds": list(pin["box"]) if pin["box"] is not None else None,
        "center_nearest_zero": center_zero,
        "clearance_kind": clearance_kind,
        "clearance": clearance,
        "det_one_minus_k_at_center": {
            "re": det_value.real,
            "im": det_value.imag,
            "abs": abs(det_value),
            "product_terms": terms,
        },
        "verdict": verdict,
        "tolerance": ZERO_TOLERANCE,
    }


def format_s(s: dict[str, float]) -> str:
    return f"{s['re']:.12f} + {s['im']:.12f}i"


def format_zero(zero: dict[str, float]) -> str:
    return f"({zero['re']:.12f}, {zero['im']:.12f})"


def render_report(receipt: dict[str, Any]) -> str:
    rows = []
    for result in receipt["pins"]:
        distance = result["clearance"]["distance"]
        distance_label = f"{distance:.12g}"
        if result["clearance_kind"] == "closed_winding_box":
            distance_label += " (box)"
        rows.append(
            f"| {result['pin_id']} | {result['q']} | {format_s(result['s'])} | "
            f"{distance_label} | {result['verdict']} |"
        )
    lines = [
        "| pin id | q | s value | K_s-zero distance | verdict |",
        "|---|---:|---|---:|---|",
        *rows,
        "",
        "# K_s definition and source",
        "",
        "The local extraction is sufficient for the over-counting context and the "
        "factorization, but it does not contain Section 6.2. I therefore used the "
        "primary MMS arXiv PDF, §6.2, equations (42)-(43), Lemma 6.3, Proposition 2, "
        "and Remark 4. The local extraction records the same context at "
        f"`{SOURCE['local_extraction']['path']}:26-35`.",
        "",
        "MMS identify the duplicated orbit as the two points `r_q` and `-r_q`, "
        "subtract the `O_+` contribution, and define `K_s = L_s^{O_+}`. In the "
        "paper's notation the inverse branches are "
        r"`theta_n(z) = -1/(z+n lambda_q)` and "
        "`(L_{n,s}g)(z) = (theta_n'(z))^s g(theta_n(z))`. The source locations are "
        "§6.2 eqs. (42)-(43), PDF text lines 2861-2894; the determinant reduction "
        "is Lemma 6.3, lines 3313-3326; the spectrum is Proposition 2, lines "
        "3415-3425. See [MMS arXiv PDF](https://arxiv.org/pdf/0912.2236).",
        "",
        "Writing `h=h_q`, the complete component definition from equations (42)-(43) "
        "is as follows. For even `q=2h+2`, on `B_h`,",
        "",
        r"`(K_s g)_i=L_{1,s}g_{i+1}` for `1<=i<=h-1`, and ` (K_s g)_h=L_{2,s}g_1`.",
        "",
        "For odd `q=2h+3` with `q>=5`, on `B_{2h+1}`,",
        "",
        r"`(K_s g)_i=L_{1,s}g_{i+1}` for `1<=i<=h`; "
        r"`(K_s g)_{h+1}=L_{2,s}g_{h+2}`;",
        "",
        r"`(K_s g)_{h+i}=L_{1,s}g_{h+i+1}` for `2<=i<=h`; and "
        r"`(K_s g)_{2h+1}=L_{2,s}g_1`.",
        "",
        "For q=5, `h_q=1`, so equation (43) is the explicit three-cycle",
        "",
        r"`(K_s g)_1 = L_{1,s}g_2`, ` (K_s g)_2 = L_{2,s}g_3`, ` (K_s g)_3 = L_{2,s}g_1`.",
        "",
        "Lemma 6.3 gives, for odd q, "
        r"`det(1-K_s) = det(1-L_{1,s}^{h_q} L_{2,s} L_{1,s}^{h_q-1} L_{2,s})`; "
        "therefore q=5 reduces to `A_s=L_{1,s}L_{2,s}L_{2,s}`.",
        "",
        "# Derived determinant and zero lattice",
        "",
        "Let `M_n = [[0,-1],[1,n lambda_q]]`, the Möbius matrix of `theta_n`. "
        "For q=5 the argument map of `A_s` is "
        r"`psi = theta_2 o theta_2 o theta_1`, with matrix `M_2 M_2 M_1`. "
        "Using `lambda_5^2=lambda_5+1`, the matrix is",
        "",
        r"`M_2 M_2 M_1 = [[-2 lambda_5, 1-2 lambda_5^2], "
        r"[4 lambda_5^2-1, 4 lambda_5^3-3 lambda_5]]`.",
        "",
        "Its determinant is 1 and its trace is",
        "",
        r"`tau_5 = 4 + 3 lambda_5`, `lambda_5 = 2 cos(pi/5) = (1+sqrt(5))/2`.",
        "",
        r"`ell_5 = (tau_5 - sqrt(tau_5^2-4))/2 = 0.11442064802926044`,",
        "",
        "the attracting multiplier's positive square root. The scalar composition "
        "operator therefore has eigenvalues `ell_5^(2s+2n)`, n=0,1,..., exactly "
        "the Proposition 2 spectrum after the Lemma 6.3 reduction. Thus",
        "",
        r"`det(1-K_s) = product_{n>=0} (1 - ell_5^(2s+2n))`.",
        "",
        r"Writing `a_5=-log(ell_5)=2.167873726556495`, a zero satisfies "
        r"`exp(-2 a_5 (s+n))=1`, hence the exact lattice is",
        "",
        r"`s = -n + i*pi*k/a_5`, for `n=0,1,2,...` and `k in Z`.",
        "",
        f"The vertical spacing is `{receipt['groups']['5']['vertical_spacing']:.15g}`. "
        f"The exact intersection with the requested rectangle "
        f"`Re in [{RECTANGLE_Q5['re_lo']}, {RECTANGLE_Q5['re_hi']}], "
        f"Im in [{RECTANGLE_Q5['im_lo']}, {RECTANGLE_Q5['im_hi']}]` is "
        f"`{receipt['rectangle_scan']['zeros_inside']}`: no K_s zeros.",
        "",
        "For the q=4 and q=6 controls, the same reduction gives `ell_4=sqrt(2)-1` "
        "and `ell_6=2-sqrt(3)`, respectively. Their zero lattices have the same "
        "horizontal rows `Re(s)=-n`; only the vertical spacings differ.",
        "",
        "# Per-pin justification",
        "",
        "Distances for G5 are point-to-lattice Euclidean distances. For q=4/q=6, "
        "the reported distance is the distance from the entire closed winding box "
        "to the nearest lattice zero, so it is a box-level nonvanishing margin. "
        f"The contamination tolerance is `{ZERO_TOLERANCE:.1e}`.",
        "",
    ]
    for result in receipt["pins"]:
        clearance = result["clearance"]
        center_zero = result["center_nearest_zero"]
        lines.extend([
            f"## {result['pin_id']} (q={result['q']})",
            "",
            f"- center: `{format_s(result['s'])}`",
            f"- nearest center lattice zero: `{format_zero(center_zero['zero'])}` "
            f"(n={center_zero['n']}, k={center_zero['k']}); center distance="
            f"`{center_zero['distance']:.15g}`",
            f"- gated clearance ({result['clearance_kind']}): "
            f"`{clearance['distance']:.15g}` to `{format_zero(clearance['zero'])}`",
            f"- numerical product check: `|det(1-K_s)|={result['det_one_minus_k_at_center']['abs']:.15g}` "
            f"using {result['det_one_minus_k_at_center']['product_terms']} terms",
            f"- verdict: **{result['verdict']}**",
            "",
        ])
    lines.extend([
        "# MISSING / BLOCKED",
        "",
        "No K_s definition or zero-set item remains unresolved. The local extraction "
        "does omit Section 6.2, so the exact definition was sourced from the fetched "
        "arXiv PDF as documented above. A shell `curl` attempt could not resolve "
        "`arxiv.org`; the browser fetch of the primary PDF succeeded. The receipt "
        "records this external-fetch dependency and the exact paper locations.",
        "",
        "The numerical determinant values are supporting evaluations. The CLEAR "
        "verdicts come from the exact analytic zero lattice and the stated geometric "
        "margins, not from the finite product alone.",
        "",
    ])
    return "\n".join(lines)


def build_receipt() -> dict[str, Any]:
    groups = {str(q): group_data(q) for q in (4, 5, 6)}
    pins = [verdict_for_pin(pin) for pin in load_pins()]
    return {
        "task": "MMS K_s divisor gate for G5 flagship pins and q4/q6 winding boxes",
        "source": SOURCE,
        "definition": {
            "operator": "K_s = L_s^{O_+}",
            "q5": "equation (43) gives the three-cycle (L1 g2, L2 g3, L2 g1)",
            "scalar_reduction_q5": "det(1-K_s)=det(1-L1,s L2,s L2,s)",
        },
        "derived_zero_lattice": {
            "formula": "s = -n + i*pi*k/a_q, n>=0, k in Z",
            "determinant_formula": "det(1-K_s)=prod_{n>=0}(1-ell_q^(2*s+2*n))",
            "status": "derived from MMS Section 6.2, Lemma 6.3, Proposition 2, and Möbius algebra",
        },
        "rectangle_scanned": RECTANGLE_Q5,
        "rectangle_scan": {
            "q": 5,
            "zeros_inside": rectangle_zeros(5, RECTANGLE_Q5),
            "status": "empty exact intersection",
        },
        "groups": groups,
        "pins": pins,
        "classification": {
            "tolerance": ZERO_TOLERANCE,
            "clear_definition": "point margin for G5; closed-box margin for q4/q6",
            "counts": {
                verdict: sum(result["verdict"] == verdict for result in pins)
                for verdict in ("CLEAR", "CONTAMINATED", "UNRESOLVED")
            },
        },
        "external_fetch_dependency": {
            "required": True,
            "local_extraction_missing_section": "Section 6.2 / K_s definition",
            "shell_fetch": "failed: curl could not resolve arxiv.org",
            "browser_primary_pdf": "succeeded: https://arxiv.org/pdf/0912.2236",
            "remaining": "reproducers need the cited arXiv PDF or a local copy of its Section 6.2",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path, default=DEFAULT_RECEIPT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()
    receipt = build_receipt()
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(receipt, indent=2) + "\n")
    args.report.write_text(render_report(receipt))
    print(json.dumps({
        "receipt": str(args.receipt),
        "report": str(args.report),
        "pins": len(receipt["pins"]),
        "counts": receipt["classification"]["counts"],
        "q5_rectangle_zeros": len(receipt["rectangle_scan"]["zeros_inside"]),
    }, indent=2))


if __name__ == "__main__":
    main()
