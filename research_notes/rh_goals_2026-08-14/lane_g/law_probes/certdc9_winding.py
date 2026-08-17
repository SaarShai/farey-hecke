"""certdc9 -- CERTIFIED (Arb ball) deep-resonance winding count for q = 9.

Window (from LAW_ROUTEB_DEEPCOUNT.md, unchanged): Re s in [0.023, 0.4],
Im s in [2, 12].  Both sign sectors of det(1 - L_{s,sign}); on 0 < Re s < 1/2
det(1 - K_s) is zero-free (LAW_Q3_BRANCH_DIAGNOSIS.md), so the two sector zero
counts sum to the resonance count.

Ball evaluator: zeta_cert_rosen.cert_det (Arb acb ball det + geometric
dimension-tail radius), used UNMODIFIED.  This driver adds only the adaptive
subdivision + strict half-turn certification that winding_offline's fixed
K = 24 / weak guard cannot supply on a 20.75-long contour.

Certification criteria (both rigorous given the ball arithmetic):
  (a) every boundary sample: |det| ball, inflated by 4 * tail, has
      abs_lower() > 0  -> det provably nonzero at that point;
  (b) every consecutive pair: w = det(B) * conj(det(A)) has
      w.real.lower() > 0  -> the argument increment lies provably in
      (-pi/2, pi/2), so the unwrapped sum is the true argument variation.
Failure of (b) triggers bisection; failure of (a) is fatal for that edge.

Note (b) is STRICTER than winding_offline's guard, which accepts any ball not
straddling the branch cut and therefore does not by itself exclude a >pi jump.
"""
from __future__ import annotations
import json
import os
import sys
import time

sys.path.insert(0, "/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code")

from flint import acb, arb, ctx  # noqa: E402
import zeta_cert_rosen as Z  # noqa: E402

Q = 9
RE_LO, RE_HI = 0.023, 0.4
IM_LO, IM_HI = 2.0, 12.0
N = int(os.environ.get("CERTDC9_N", "16"))
N_HEAD = 4
MAX_DEPTH = int(os.environ.get("CERTDC9_DEPTH", "10"))
TAIL_SAFETY = 4
INIT_V = int(os.environ.get("CERTDC9_INITV", "100"))   # samples per vertical edge
INIT_H = int(os.environ.get("CERTDC9_INITH", "8"))     # samples per horizontal edge

OUT = os.path.dirname(os.path.abspath(__file__))


class Evaluator:
    def __init__(self, sign):
        self.sign = sign
        self.cache = {}
        self.calls = 0
        self.min_abs_lower = None
        self.max_tail = arb(0)
        self.uncertified_tail = []
        self.escalated = []

    def det_ball(self, re, im):
        key = (re, im)
        hit = self.cache.get(key)
        if hit is not None:
            return hit
        s = acb(arb(re), arb(im))
        # Each ball det_N +/- tail_N encloses the true infinite-dimensional
        # determinant, so escalating N at a single hard point keeps every
        # enclosure valid while restoring the dim-tail ratio test.
        det = tail = None
        for Ntry in (N, N + 4, N + 8):
            det, tail, info, _k = Z.cert_det(s, Ntry, self.sign, Q,
                                             n_head=N_HEAD)
            self.calls += 1
            if tail is not None:
                if Ntry != N:
                    self.escalated.append([re, im, Ntry])
                break
        if tail is None:
            self.uncertified_tail.append([re, im])
            raise RuntimeError(f"dim-tail UNCERTIFIED at ({re},{im}) "
                               f"up to N={N + 8}")
        if tail > self.max_tail:
            self.max_tail = tail
        r = tail * TAIL_SAFETY
        ball = acb(det.real + arb(0, r), det.imag + arb(0, r))
        al = float(ball.abs_lower())
        if self.min_abs_lower is None or al < self.min_abs_lower:
            self.min_abs_lower = al
        if not (ball.abs_lower() > 0):
            raise RuntimeError(f"det ball contains 0 at ({re},{im}); "
                               f"tail*{TAIL_SAFETY}={float(r):.3e}")
        self.cache[key] = ball
        return ball


def certify_segment(ev, p0, p1, depth, log, stats):
    """Certified argument variation from p0 to p1 (points on one edge)."""
    A = ev.det_ball(*p0)
    B = ev.det_ball(*p1)
    w = B * A.conjugate()
    if w.real.lower() > 0:
        stats["segments"] += 1
        return w.arg().real
    if depth >= MAX_DEPTH:
        raise RuntimeError(
            f"half-turn criterion unmet at max depth between {p0} and {p1}; "
            f"w.real=[{float(w.real.lower()):.3e},{float(w.real.upper()):.3e}]")
    stats["bisections"] += 1
    if depth + 1 > stats["max_depth_used"]:
        stats["max_depth_used"] = depth + 1
    mid = (0.5 * (p0[0] + p1[0]), 0.5 * (p0[1] + p1[1]))
    return (certify_segment(ev, p0, mid, depth + 1, log, stats)
            + certify_segment(ev, mid, p1, depth + 1, log, stats))


def edge_points(a, b, n):
    """n+1 points from a to b inclusive."""
    return [(a[0] + (b[0] - a[0]) * t / n, a[1] + (b[1] - a[1]) * t / n)
            for t in range(n + 1)]


def run_sector(sign):
    ev = Evaluator(sign)
    corners = [(RE_LO, IM_LO), (RE_HI, IM_LO), (RE_HI, IM_HI), (RE_LO, IM_HI)]
    names = ["bottom Im=2", "right Re=0.4", "top Im=12", "left Re=0.023"]
    counts = [INIT_H, INIT_V, INIT_H, INIT_V]
    total = arb(0)
    edges = []
    for e in range(4):
        a, b = corners[e], corners[(e + 1) % 4]
        pts = edge_points(a, b, counts[e])
        stats = {"segments": 0, "bisections": 0, "max_depth_used": 0}
        t0 = time.time()
        acc = arb(0)
        for i in range(len(pts) - 1):
            acc = acc + certify_segment(ev, pts[i], pts[i + 1], 0, None, stats)
        dt = time.time() - t0
        total = total + acc
        edges.append({
            "edge": names[e], "from": list(a), "to": list(b),
            "initial_samples": counts[e] + 1,
            "certified_segments": stats["segments"],
            "bisections": stats["bisections"],
            "max_bisection_depth": stats["max_depth_used"],
            "delta_arg": float(acc.mid()),
            "delta_arg_rad_ball": [float(acc.lower()), float(acc.upper())],
            "status": "CERTIFIED (a)+(b)",
            "wall_s": round(dt, 1),
        })
        print(f"  [sign {sign:+d}] {names[e]}: dArg={float(acc.mid()):+.6f} "
              f"segs={stats['segments']} bisect={stats['bisections']} "
              f"depth={stats['max_depth_used']} {dt:.0f}s", flush=True)
    wnd = total / (arb.pi() * 2)
    lo, hi = wnd.lower(), wnd.upper()
    nint = round(float(wnd.mid()))
    ok = bool(lo > nint - arb(1) / 2 and hi < nint + arb(1) / 2)
    return {
        "sign": sign, "N": N, "prec_bits": Z.PREC_BITS,
        "winding_ball": [float(lo), float(hi)],
        "winding_mid": float(wnd.mid()),
        "certified_integer": int(nint) if ok else None,
        "integer_isolated": ok,
        "det_calls": ev.calls,
        "min_det_abs_lower_on_contour": ev.min_abs_lower,
        "max_dim_tail": float(ev.max_tail),
        "N_escalated_points": ev.escalated,
        "tail_safety": TAIL_SAFETY,
        "edges": edges,
    }


def main():
    t0 = time.time()
    res = {}
    for sign in (1, -1):
        print(f"sector sign={sign:+d} N={N}", flush=True)
        res[str(sign)] = run_sector(sign)
    tot = None
    if all(res[k]["integer_isolated"] for k in res):
        tot = sum(res[k]["certified_integer"] for k in res)
    out = {
        "label": "CERTIFIED (Arb ball) -- conditional on the geometric "
                 "dimension-tail bound of dim_tail_from_matrix",
        "q": Q, "N": N, "n_head": N_HEAD, "prec_bits": Z.PREC_BITS,
        "window": {"re": [RE_LO, RE_HI], "im": [IM_LO, IM_HI]},
        "evaluator": "zeta_cert_rosen.cert_det (unmodified)",
        "sectors": res,
        "certified_deep_count": tot,
        "measured_deep_count_LAW_ROUTEB_DEEPCOUNT": 7,
        "wall_s": round(time.time() - t0, 1),
    }
    path = os.path.join(OUT, f"certdc9_winding_q9_N{N}.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps({k: out[k] for k in
                      ("certified_deep_count", "wall_s")}, indent=2))
    print("wrote", path)


if __name__ == "__main__":
    main()
