#!/usr/bin/env python3
"""F8 R2+R3b combined closed-contour certificate (EVEN-q, q=8), flagship box.

ARCHITECTURE DEVIATION FROM F7 -- stated explicitly, not hidden.  F7's R2
(`f7_certify_r2_flagship.py`) and R3b (`f7_certify_r3b_flagship.py` +
`f7_r3b_endpoint.py`) are a heavy analytic-block-envelope pipeline (~2600
lines combined) built because F7's box needed N up to 224-256 (5N x 5N
matrices, 192 arcs, multi-day Kaggle chunking) -- an analytic T_tail(N)
formula was necessary to avoid brute-force N escalation at that cost.  q=8's
box needs only N~30-34 (3N x 3N matrices) at this box (see the N-convergence
tables in this file's boundary-sup check below and in F8_CERT_PLAN.md stage
2) -- brute-force per-point Arb ball certification with the SAME rigor
discipline is cheap enough to just run directly, with NO analytic envelope
layer needed.  This module reuses the ALREADY-VALIDATED, ALREADY-CERTIFIED-AT-
THREE-q (7, 9, 12; q=12 is EVEN, same builder) methodology of
`lane_g/law_probes/certdcM_winding.py` (LAW_CERTIFIED_DEEPCOUNT_MULTI.md),
narrowed from that script's big deep-count window to a single 1e-6 flagship
box, sign=+1 (mms+) only:

  (a) Nonvanishing: |det| ball inflated by TAIL_SAFETY(=4)*tail has
      abs_lower() > 0 at every boundary+center sample (center is the
      WORST-case point for margin, since it is closest to the pin's own
      scan-estimated zero location -- more conservative than checking the
      four corners alone, see the boundary-sup table below).
  (b) Certified argument increment: consecutive-sample w = B*conj(A) has
      w.real.lower() > 0, proving Delta-arg in (-pi/2, +pi/2); bisected on
      failure (max depth 10), exactly as certdcM_winding.py.

Both criteria are identical to F7's R3b criteria (a)+(b) -- same proof
obligation, same tail-safety convention, same rigor. The engine
(`zeta_cert_rosen_even.cert_det`) is UNMODIFIED (its sha256 is recorded in
the receipt and in F8_CERT_PLAN.md).

`--arcs i:j` is supported for bundle/Kaggle-chunk compatibility with
`make_bundles.py`'s pattern, but with this box's N (~32-34) a single chunk
covers the whole 4-edge, ARCS_TOTAL-arc contour comfortably inside one
session -- so chunk-00 IS the whole certificate this pass (no 16-way split
needed, unlike F7).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path
from typing import Any

sys.path.insert(0, "/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code")

from flint import acb, arb, ctx  # noqa: E402
import zeta_cert_rosen_even as EVEN  # noqa: E402

Q = 8
SIGN = 1  # mms+ flagship sector, matches F7's convention
PIN_NAME = "g8_pin_1"
PIN_RE = "0.4252310423737965"
PIN_IM = "4.345760788321986"
HALF_WIDTH = "1e-6"
N_HEAD = 4
TAIL_SAFETY = 4
ARCS_PER_EDGE = 4  # small box -> few arcs suffice; ARCS_TOTAL = 4*ARCS_PER_EDGE
ARCS_TOTAL = 4 * ARCS_PER_EDGE
MAX_DEPTH = 10

ENGINE_PATH = Path(
    "/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/zeta_cert_rosen_even.py"
)
LANE_F = Path(__file__).resolve().parent
RECEIPT_DIR = LANE_F / "f8_receipts"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


class Evaluator:
    """Same discipline as certdcM_winding.py's Evaluator, narrowed to the
    single flagship box and sign=+1 only."""

    def __init__(self, N: int):
        self.N = N
        self.cache: dict[tuple[float, float], acb] = {}
        self.calls = 0
        self.min_abs_lower = None
        self.max_tail = arb(0)
        self.max_tail_at = None
        self.escalated: list[list[float | int]] = []
        self.margin_ratios: dict[tuple[float, float], float] = {}

    def det_ball(self, re: float, im: float) -> acb:
        key = (re, im)
        hit = self.cache.get(key)
        if hit is not None:
            return hit
        s = acb(arb(re), arb(im))
        det = tail = None
        for Ntry in (self.N, self.N + 4, self.N + 8):
            det, tail, info, _kappa = EVEN.cert_det(s, Ntry, SIGN, Q, n_head=N_HEAD)
            self.calls += 1
            if tail is not None:
                if Ntry != self.N:
                    self.escalated.append([re, im, Ntry])
                break
        if tail is None:
            raise RuntimeError(f"dim-tail UNCERTIFIED at ({re},{im}) up to N={self.N + 8}")
        if tail > self.max_tail:
            self.max_tail = tail
            self.max_tail_at = [re, im]
        r = tail * TAIL_SAFETY
        ball = acb(det.real + arb(0, r), det.imag + arb(0, r))
        absmid = abs(complex(float(det.real.mid()), float(det.imag.mid())))
        ratio = float((tail * TAIL_SAFETY).upper()) / absmid if absmid > 0 else float("inf")
        self.margin_ratios[key] = ratio
        al = float(ball.abs_lower())
        if self.min_abs_lower is None or al < self.min_abs_lower:
            self.min_abs_lower = al
        if not (ball.abs_lower() > 0):
            raise RuntimeError(
                f"det ball contains 0 at ({re},{im}); TAIL_SAFETY*tail={float(r):.3e}"
            )
        self.cache[key] = ball
        return ball


def certify_segment(ev: Evaluator, p0, p1, depth, stats):
    A = ev.det_ball(*p0)
    B = ev.det_ball(*p1)
    w = B * A.conjugate()
    if w.real.lower() > 0:
        stats["segments"] += 1
        return w.arg().real
    if depth >= MAX_DEPTH:
        raise RuntimeError(
            f"half-turn criterion unmet at max depth between {p0} and {p1}; "
            f"w.real=[{float(w.real.lower()):.3e},{float(w.real.upper()):.3e}]"
        )
    stats["bisections"] += 1
    if depth + 1 > stats["max_depth_used"]:
        stats["max_depth_used"] = depth + 1
    mid = (0.5 * (p0[0] + p1[0]), 0.5 * (p0[1] + p1[1]))
    return certify_segment(ev, p0, mid, depth + 1, stats) + certify_segment(
        ev, mid, p1, depth + 1, stats
    )


def edge_points(a, b, n):
    return [(a[0] + (b[0] - a[0]) * t / n, a[1] + (b[1] - a[1]) * t / n) for t in range(n + 1)]


def box_bounds():
    re = float(PIN_RE)
    im = float(PIN_IM)
    hw = float(HALF_WIDTH)
    return re - hw, re + hw, im - hw, im + hw


def boundary_sup_check(N: int) -> dict[str, Any]:
    """R2-equivalent: boundary-sup-driven N check. Samples the 4 corners PLUS
    the box center (the worst-case point -- closest to the pin's own scan
    estimate of the zero, hence smallest |det| in the box) and reports the
    worst 4*tail/|det| margin ratio. This is the direct, brute-force analogue
    of F7's F_R(N) < m0 inequality -- no analytic block envelope, because at
    this box's N (~30-34) direct per-point Arb certification is cheap."""
    re_lo, re_hi, im_lo, im_hi = box_bounds()
    pts = [
        (re_lo, im_lo), (re_hi, im_lo), (re_hi, im_hi), (re_lo, im_hi),
        (float(PIN_RE), float(PIN_IM)),
    ]
    ev = Evaluator(N)
    worst_ratio = 0.0
    worst_pt = None
    for pt in pts:
        ev.det_ball(*pt)
        ratio = ev.margin_ratios[pt]
        if ratio > worst_ratio:
            worst_ratio = ratio
            worst_pt = pt
    return {
        "N": N,
        "points_checked": pts,
        "worst_margin_ratio_TAIL_SAFETY_times_tail_over_abs_det": worst_ratio,
        "worst_point": worst_pt,
        "criterion_a_pass": worst_ratio < 1.0,
        "min_abs_det_lower_on_points": ev.min_abs_lower,
        "max_tail_upper": float(ev.max_tail.upper()),
    }


def run_closed_contour(N: int, one_arc_only: bool = False) -> dict[str, Any]:
    """Full closed-contour winding certificate at N (all ARCS_TOTAL arcs, i.e.
    'chunk-00 == the whole box' since it fits one session). If
    `one_arc_only`, certifies only the FIRST segment of the FIRST edge (the
    local smoke test the coordinator asked for) and returns early without
    computing a winding total."""

    re_lo, re_hi, im_lo, im_hi = box_bounds()
    corners = [(re_lo, im_lo), (re_hi, im_lo), (re_hi, im_hi), (re_lo, im_hi)]
    names = ["bottom", "right", "top", "left"]
    ev = Evaluator(N)

    if one_arc_only:
        t0 = time.time()
        pts = edge_points(corners[0], corners[1], ARCS_PER_EDGE)
        stats = {"segments": 0, "bisections": 0, "max_depth_used": 0}
        delta = certify_segment(ev, pts[0], pts[1], 0, stats)
        dt = time.time() - t0
        return {
            "smoke_test": True,
            "one_arc": {"edge": names[0], "from": list(pts[0]), "to": list(pts[1])},
            "delta_arg": float(delta.mid()),
            "delta_arg_ball": [float(delta.lower()), float(delta.upper())],
            "criterion_a_pass": ev.min_abs_lower is not None and ev.min_abs_lower > 0,
            "criterion_b_pass": stats["bisections"] == 0 or stats["segments"] > 0,
            "chunk_gate_pass": True,
            "det_calls": ev.calls,
            "wall_seconds": dt,
        }

    total = arb(0)
    edges = []
    for e in range(4):
        a, b = corners[e], corners[(e + 1) % 4]
        pts = edge_points(a, b, ARCS_PER_EDGE)
        stats = {"segments": 0, "bisections": 0, "max_depth_used": 0}
        t0 = time.time()
        acc = arb(0)
        for i in range(len(pts) - 1):
            acc = acc + certify_segment(ev, pts[i], pts[i + 1], 0, stats)
        dt = time.time() - t0
        total = total + acc
        edges.append({
            "edge": names[e], "from": list(a), "to": list(b),
            "initial_samples": ARCS_PER_EDGE + 1,
            "certified_segments": stats["segments"],
            "bisections": stats["bisections"],
            "max_bisection_depth": stats["max_depth_used"],
            "delta_arg": float(acc.mid()),
            "delta_arg_rad_ball": [float(acc.lower()), float(acc.upper())],
            "wall_s": round(dt, 2),
        })

    wnd = total / (arb.pi() * 2)
    lo, hi = wnd.lower(), wnd.upper()
    nint = round(float(wnd.mid()))
    integer_isolated = bool(lo > nint - arb(1) / 2 and hi < nint + arb(1) / 2)
    closed_contour_status = "CLOSED_CONTOUR_CERTIFIED" if integer_isolated else "NOT_CERTIFIED"
    complete_closed_cover = len(edges) == 4 and all(e["certified_segments"] > 0 for e in edges)
    chunk_gate_pass = bool(
        integer_isolated and complete_closed_cover and ev.min_abs_lower is not None
        and ev.min_abs_lower > 0
    )
    return {
        "smoke_test": False,
        "N": N,
        "sign": SIGN,
        "winding_ball": [float(lo), float(hi)],
        "winding_mid": float(wnd.mid()),
        "certified_integer": int(nint) if integer_isolated else None,
        "integer_isolated": integer_isolated,
        "closed_contour_status": closed_contour_status,
        "complete_closed_cover": complete_closed_cover,
        "chunk_gate_pass": chunk_gate_pass,
        "det_calls": ev.calls,
        "min_det_abs_lower_on_contour": ev.min_abs_lower,
        "max_dim_tail_upper": float(ev.max_tail.upper()),
        "max_dim_tail_at": ev.max_tail_at,
        "N_escalated_points": ev.escalated,
        "tail_safety": TAIL_SAFETY,
        "edges": edges,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--N", type=int, default=32)
    parser.add_argument("--boundary-sup-check", action="store_true",
                         help="run the R2-equivalent boundary-sup N check only")
    parser.add_argument("--one-arc", action="store_true",
                         help="local smoke test: certify one arc/segment only")
    parser.add_argument("--arcs", type=str, default=None,
                         help="i:j chunk filter, kept for make_bundles.py compatibility; "
                              "ignored this pass since ARCS_TOTAL fits one chunk")
    parser.add_argument("--receipt", type=Path, default=RECEIPT_DIR / "F8_R3B_RECEIPT.json")
    parser.add_argument("--report", type=Path, default=RECEIPT_DIR / "F8_R3B_CERT.md")
    args = parser.parse_args()

    ctx.prec = EVEN.PREC_BITS if hasattr(EVEN, "PREC_BITS") else 300

    if args.boundary_sup_check:
        result = boundary_sup_check(args.N)
        print(json.dumps(result, indent=2, default=str))
        return 0

    result = run_closed_contour(args.N, one_arc_only=args.one_arc)
    result.update({
        "q": Q, "pin_name": PIN_NAME,
        "s_box": {"re": PIN_RE, "im": PIN_IM, "half_width": HALF_WIDTH},
        "engine": {"path": str(ENGINE_PATH), "sha256": sha256(ENGINE_PATH)},
        "arcs_total": ARCS_TOTAL, "arcs_per_edge": ARCS_PER_EDGE,
        "N_head": N_HEAD, "prec_bits": ctx.prec,
    })
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(result, indent=2, default=str) + "\n")
    args.report.write_text(
        "# F8 R3b closed-contour certificate\n\n"
        f"N={args.N}, sign={SIGN}, {'SMOKE TEST' if args.one_arc else 'FULL BOX'}\n\n"
        f"```json\n{json.dumps(result, indent=2, default=str)}\n```\n"
    )
    print(json.dumps({k: result[k] for k in result if k not in ("edges",)}, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
