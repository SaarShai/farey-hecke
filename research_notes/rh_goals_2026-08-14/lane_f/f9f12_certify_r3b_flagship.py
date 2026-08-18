#!/usr/bin/env python3
"""F9-F12 R2+R3b closed-contour certificate, flagship boxes, q = 9,10,11,12.

PORT OF `f8_certify_r3b_flagship.py` (q=8), q-parameterized.  Everything that
makes the certificate rigorous is carried over UNCHANGED from that file --
same two criteria, same TAIL_SAFETY=4, same bisection discipline (max depth
10), same UNMODIFIED engines.  Only three things vary with q:

  * the engine module: `zeta_cert_rosen_even` for even q (MMS eq.(32)
    geometry, kappa = h_q = (q-2)/2), `zeta_cert_rosen` for odd q (MMS
    eq.(34), kappa = 2h+1).  Both expose the identical
    `cert_det(s, N, sign, q, n_head) -> (det_ball, tail, info, kappa)`
    signature, so the driver code below is parity-agnostic.  This is the
    same builder pairing `lane_g/law_probes/certdcM_winding.py` already uses
    (LAW_CERTIFIED_DEEPCOUNT_MULTI.md certified q=7 odd / q=12 even through
    exactly this pairing).
  * the box centre (`PINS` below).
  * N (chosen per q by `--boundary-sup-check`, as F8 did).

PROVENANCE OF THE BOXES -- the one real deviation from a pure port, stated
plainly.  q=8's box came from the `lane_k` 400-bit scan harvest
(`hecke_family_q7_q8_scan.json`, surface `q8_mms_plus`, pin 1).  That harvest
covers **q=7 and q=8 only**; no q=9..12 pin exists anywhere in the repo.  The
`PINS` values below were therefore produced this pass by
`f9f12_pin_finder.py`, which re-runs the scan's own three-stage protocol
(surface N=14 -> Newton N=22 -> stability re-Newton N=28) against the trusted
engines.  Each pin's N22->N28 drift is quoted next to it; q=8's own pin drift
was ~2.6e-13, so these are in the same health class.  The pin is only a
PROPOSED box centre -- it carries no rigour, and nothing below trusts it:
the winding certificate stands on the Arb balls it computes itself.

SCOPE, explicit: this certifies a closed-contour winding number for ONE box
per q.  It is an R3B-class box certificate, NOT an assembled off-line
theorem (no K_s gate re-verification, no sector-completeness argument, no
strip-exhaustion) -- the same scope F8 shipped.
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

import zeta_cert_rosen as ODD  # noqa: E402
import zeta_cert_rosen_even as EVEN  # noqa: E402

SIGN = 1  # mms+ flagship sector, matches F8/F7 convention
HALF_WIDTH = "1e-6"
N_HEAD = 4
TAIL_SAFETY = 4
ARCS_PER_EDGE = 4
ARCS_TOTAL = 4 * ARCS_PER_EDGE
MAX_DEPTH = 10

# (re, im) box centres from f9f12_pin_finder.py, lowest-height stability-
# passing pin of each q's scan.  Drift = |s(N=22) - s(N=28)| (pin health).
PINS: dict[int, tuple[str, str]] = {
    9: ("0.3742488091325338", "4.080139082773367"),      # drift 1.865e-14
    10: ("0.333692861999034", "3.853631836813213"),      # drift 5.561e-13
    11: ("0.3055125027342933", "3.6592963976938098"),    # drift 1.366e-14
    12: ("0.28732580259283225", "3.4924075186049106"),   # drift 4.445e-13
}

CODE_DIR = Path("/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code")
LANE_F = Path(__file__).resolve().parent


def engine_for(q: int):
    return EVEN if q % 2 == 0 else ODD


def engine_path(q: int) -> Path:
    return CODE_DIR / ("zeta_cert_rosen_even.py" if q % 2 == 0 else "zeta_cert_rosen.py")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


class Evaluator:
    """Verbatim from f8_certify_r3b_flagship.py except that the engine module
    is selected by parity instead of being the hard-wired even one."""

    def __init__(self, q: int, N: int):
        self.q = q
        self.M = engine_for(q)
        self.N = N
        self.cache: dict[tuple[float, float], acb] = {}
        self.calls = 0
        self.min_abs_lower = None
        self.max_tail = arb(0)
        self.max_tail_at = None
        self.escalated: list[list[float | int]] = []
        self.margin_ratios: dict[tuple[float, float], float] = {}
        self.kappa = None  # 4th return of cert_det; recorded in the receipt

    def det_ball(self, re: float, im: float) -> acb:
        key = (re, im)
        hit = self.cache.get(key)
        if hit is not None:
            return hit
        s = acb(arb(re), arb(im))
        det = tail = None
        for Ntry in (self.N, self.N + 4, self.N + 8):
            det, tail, info, kappa = self.M.cert_det(s, Ntry, SIGN, self.q, n_head=N_HEAD)
            self.calls += 1
            self.kappa = int(kappa)
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


def box_bounds(q: int):
    pin_re, pin_im = PINS[q]
    re, im, hw = float(pin_re), float(pin_im), float(HALF_WIDTH)
    return re - hw, re + hw, im - hw, im + hw


def boundary_sup_check(q: int, N: int) -> dict[str, Any]:
    """R2-equivalent N freeze: 4 corners PLUS the box centre (worst-case point
    for margin, being closest to the pin's estimated zero), reporting the
    worst TAIL_SAFETY*tail/|det| ratio.  Same brute-force analogue of F7's
    F_R(N) < m0 that F8 used."""
    re_lo, re_hi, im_lo, im_hi = box_bounds(q)
    pin_re, pin_im = PINS[q]
    pts = [
        (re_lo, im_lo), (re_hi, im_lo), (re_hi, im_hi), (re_lo, im_hi),
        (float(pin_re), float(pin_im)),
    ]
    ev = Evaluator(q, N)
    worst_ratio = 0.0
    worst_pt = None
    for pt in pts:
        ev.det_ball(*pt)
        ratio = ev.margin_ratios[pt]
        if ratio > worst_ratio:
            worst_ratio = ratio
            worst_pt = pt
    return {
        "q": q,
        "N": N,
        "kappa": ev.kappa,
        "points_checked": pts,
        "worst_margin_ratio_TAIL_SAFETY_times_tail_over_abs_det": worst_ratio,
        "worst_point": worst_pt,
        "criterion_a_pass": worst_ratio < 1.0,
        "min_abs_det_lower_on_points": ev.min_abs_lower,
        "max_tail_upper": float(ev.max_tail.upper()),
        "N_escalated_points": ev.escalated,
    }


def run_closed_contour(q: int, N: int, one_arc_only: bool = False) -> dict[str, Any]:
    re_lo, re_hi, im_lo, im_hi = box_bounds(q)
    corners = [(re_lo, im_lo), (re_hi, im_lo), (re_hi, im_hi), (re_lo, im_hi)]
    names = ["bottom", "right", "top", "left"]
    ev = Evaluator(q, N)

    if one_arc_only:
        t0 = time.time()
        pts = edge_points(corners[0], corners[1], ARCS_PER_EDGE)
        stats = {"segments": 0, "bisections": 0, "max_depth_used": 0}
        delta = certify_segment(ev, pts[0], pts[1], 0, stats)
        dt = time.time() - t0
        return {
            "smoke_test": True,
            "q": q,
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
        "q": q,
        "N": N,
        "kappa": ev.kappa,
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
    parser.add_argument("--q", type=int, required=True, choices=sorted(PINS))
    parser.add_argument("--N", type=int, default=32)
    parser.add_argument("--boundary-sup-check", action="store_true")
    parser.add_argument("--one-arc", action="store_true")
    parser.add_argument("--arcs", type=str, default=None,
                        help="i:j chunk filter, kept for make_bundles compatibility; "
                             "ignored -- ARCS_TOTAL fits one session at these N")
    parser.add_argument("--receipt", type=Path, default=None)
    parser.add_argument("--report", type=Path, default=None)
    args = parser.parse_args()

    q = args.q
    if PINS[q][0] == "PENDING":
        print(json.dumps({"q": q, "status": "NO_PIN",
                          "detail": "PINS[%d] not filled; run f9f12_pin_finder.py --q %d" % (q, q)}))
        return 2

    M = engine_for(q)
    ctx.prec = M.PREC_BITS if hasattr(M, "PREC_BITS") else 300

    if args.boundary_sup_check:
        print(json.dumps(boundary_sup_check(q, args.N), indent=2, default=str))
        return 0

    receipt_dir = LANE_F / ("f%d_receipts" % q)
    receipt = args.receipt or receipt_dir / ("F%d_R3B_RECEIPT_N%d.json" % (q, args.N))
    report = args.report or receipt_dir / ("F%d_R3B_CERT_N%d.md" % (q, args.N))

    result = run_closed_contour(q, args.N, one_arc_only=args.one_arc)
    pin_re, pin_im = PINS[q]
    result.update({
        "pin_name": "g%d_pin_1" % q,
        "pin_source": "f9f12_pin_finder.py -> f%d_receipts/F%d_PIN_SCAN.json (pins[0])" % (q, q),
        "s_box": {"re": pin_re, "im": pin_im, "half_width": HALF_WIDTH},
        "engine": {"path": str(engine_path(q)), "sha256": sha256(engine_path(q)),
                   "module": M.__name__, "parity": "even" if q % 2 == 0 else "odd"},
        "arcs_total": ARCS_TOTAL, "arcs_per_edge": ARCS_PER_EDGE,
        "N_head": N_HEAD, "prec_bits": ctx.prec,
    })
    receipt_dir.mkdir(parents=True, exist_ok=True)
    receipt.write_text(json.dumps(result, indent=2, default=str) + "\n")
    report.write_text(
        "# F%d R3b closed-contour certificate\n\n" % q
        + f"q={q}, N={args.N}, sign={SIGN}, "
        + f"{'SMOKE TEST' if args.one_arc else 'FULL BOX'}\n\n"
        + f"```json\n{json.dumps(result, indent=2, default=str)}\n```\n"
    )
    print(json.dumps({k: result[k] for k in result if k != "edges"}, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
