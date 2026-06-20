"""
engine/certify/certify.py
=========================
CERTIFY stage of the Aletheia math engine.

A reusable, problem-AGNOSTIC interval-certification module. It takes a numerical
`Claim` (per engine/GOAL.md) whose `artifact`/`params` point to a quantity to
rigorously certify, runs a rigorous certifier, and returns a `Certificate` dict
plus a machine-checkable JSON file written under engine/runs/.

CONTRACT (engine/GOAL.md):
    certify(claim: dict) -> Certificate
    Claim       = {id, statement, kind: "numerical"|"theorem", artifact, params}
    Certificate = {claim_id, method, enclosure, certified: bool,
                   certificate_path, tool}

REFERENCE PLUGIN: the Hecke transfer-operator argument-principle winding box.
The math is NOT reimplemented here -- we WRAP the certified Arb engines:
  * code/zeta_resonance_g5.py  (winding_offline = the off-line argument-principle
    box with parameterized real-center; cert_det; newton_locate) -- handles
    q in {3, 5}.
  * code/zeta_cert_rosen.py    (general odd q>=5: build_reduced_matrix_ball,
    certified_det, winding_offline).

A claim of kind "numerical" with
    artifact = "hecke_transfer_operator_zero"
    params   = {q, re, im, sign, N, n_head, ...}
asserts: "the complex s = re + i*im is a SIMPLE zero of det(1 - L^{sign}_s) for
the Hecke transfer operator of G_q".  The certifier:
  (1) optionally Newton-refines the seed s to land the candidate zero well inside
      the box (refine=True by default);
  (2) builds a rigorous argument-principle winding box around s using the engine's
      certified Arb det and a uniform dimension-tail bound over the box;
  (3) certified := (winding_number == 1)  -> a single simple enclosed zero.
A winding of 0 (no enclosed zero) => certified False (the non-resonance control).

HONESTY / RIGOR caveat (surfaced in every certificate):
  The winding rigor rests on a dimension-tail bound (the N->infinity truncation
  remainder of the Fredholm determinant), which in this engine is VALIDATED, not
  proved -- it is an empirical certified-det-increment estimate, inflated x4 over
  the box, NOT a proved analytic tail bound.  The certificate carries a
  `dim_tail_certified` flag: True iff the engine returned a finite tail ball at
  every box sample (so the interval det arithmetic is self-consistent), but the
  flag does NOT assert the tail bound is a theorem.  Treat the result as
  "rigorous modulo the validated dim-tail device".

PLUGGABILITY: certify() dispatches on claim["artifact"] through EVALUATORS.
To certify a non-Hecke quantity, register a new evaluator: a callable
    evaluator(claim) -> dict
returning at minimum {certified: bool, method: str, enclosure: dict, tool: str,
extra...}.  See `_hecke_transfer_operator_evaluator` for the reference shape.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import os
import sys

# ---------------------------------------------------------------------------
# Paths.  We import the certified Arb engines from the repo's code/ dir.
# ---------------------------------------------------------------------------
_HERE = os.path.dirname(os.path.abspath(__file__))
_ENGINE_DIR = os.path.dirname(_HERE)
_REPO_ROOT = os.path.dirname(_ENGINE_DIR)
_CODE_DIR = os.path.join(_REPO_ROOT, "code")
_RUNS_DIR = os.path.join(_ENGINE_DIR, "runs")

if _CODE_DIR not in sys.path:
    sys.path.insert(0, _CODE_DIR)


# ===========================================================================
#  numpy-/Arb-safe JSON sanitiser (so certificates are machine-checkable JSON).
# ===========================================================================
def _san(o):
    if isinstance(o, dict):
        return {k: _san(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_san(v) for v in o]
    if isinstance(o, bool):
        return o
    if isinstance(o, (int,)):
        return o
    if isinstance(o, (float,)):
        return o
    # numpy scalars / anything else -> coerce via float/str
    try:
        import numpy as _np  # noqa: local import; engine deps already require it
        if isinstance(o, (_np.bool_,)):
            return bool(o)
        if isinstance(o, (_np.integer,)):
            return int(o)
        if isinstance(o, (_np.floating,)):
            return float(o)
        if isinstance(o, (_np.complexfloating,)):
            return {"re": float(o.real), "im": float(o.imag)}
    except Exception:
        pass
    if isinstance(o, complex):
        return {"re": float(o.real), "im": float(o.imag)}
    if o is None:
        return None
    return str(o)


def _atomic_dump(obj, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(_san(obj), f, indent=2)
    os.replace(tmp, path)


def _claim_id(claim: dict) -> str:
    cid = claim.get("id")
    if cid:
        return str(cid)
    # derive a stable id from the claim content if none supplied
    blob = json.dumps(_san(claim), sort_keys=True).encode()
    return "claim_" + hashlib.sha1(blob).hexdigest()[:12]


# ===========================================================================
#  REFERENCE PLUGIN: Hecke transfer-operator simple-zero certifier.
# ===========================================================================
def _hecke_transfer_operator_evaluator(claim: dict) -> dict:
    """Rigorously certify that s = re + i*im is a SIMPLE zero of
    det(1 - L^{sign}_s) for the Hecke transfer operator of G_q.

    Returns the evaluator-result dict (merged into the Certificate by certify()).
    Wraps code/zeta_resonance_g5.py (q in {3,5}) or code/zeta_cert_rosen.py
    (general odd q>=5).
    """
    p = dict(claim.get("params") or {})
    q = int(p.get("q", 5))
    re = float(p["re"])
    im = float(p["im"])
    sign = int(p.get("sign", +1))           # +1 even (mms+), -1 odd (mms-)
    N = int(p.get("N", 18))
    n_head = int(p.get("n_head", 4))
    K = int(p.get("K", 24))
    refine = bool(p.get("refine", True))
    # box half-widths to try (inner -> outer); first that encloses cleanly wins
    boxes = p.get("boxes") or [
        [0.012, 0.012], [0.02, 0.02], [0.035, 0.03], [0.05, 0.04],
    ]

    log: list[str] = []

    # --- choose the engine wrapper -----------------------------------------
    # zeta_resonance_g5 covers q in {3,5} with cert_det(q, s, N, sign, n_head)
    # and winding_offline(q, re0, im0, hx, hy, N, sign, n_head, K).
    # zeta_cert_rosen covers general odd q>=5 with cert_det(s, N, sign, q, n_head)
    # and winding_offline(re0, im0, hx, hy, N, sign, q, n_head, K).
    from flint import acb, arb  # certified ball backend

    use_g5 = q in (3, 5)
    if use_g5:
        import zeta_resonance_g5 as ENG

        def cert_det(s):
            return ENG.cert_det(q, s, N, sign, n_head)

        def newton(re0, im0):
            return ENG.newton_locate(q, re0, im0, N, sign, n_head, log=log)

        def winding(re0, im0, hx, hy):
            return ENG.winding_offline(
                q, re0, im0, hx, hy, N, sign, n_head, K=K, log=log)

        backend = ENG.Zc.BACKEND
        prec_bits = ENG.PREC_BITS
        tool = "code/zeta_resonance_g5.py (Arb argument-principle winding box)"
    else:
        if q % 2 == 0:
            raise NotImplementedError(
                "even q transfer operator not generalized; reference plugin "
                "supports q=3 and odd q>=5")
        import zeta_cert_rosen as ENG

        def cert_det(s):
            return ENG.cert_det(s, N, sign, q, n_head)

        def newton(re0, im0):
            # zeta_cert_rosen has no built-in newton, and g5.newton_locate only
            # works for q in {3,5}; for general odd q>=5 run a tiny local Newton
            # on the certified midpoint det (holomorphic off-line -> valid).
            return _local_newton(cert_det, re0, im0, log)

        def winding(re0, im0, hx, hy):
            return ENG.winding_offline(
                re0, im0, hx, hy, N, sign, q, n_head, K=K, log=log)

        backend = ENG.BACKEND
        prec_bits = ENG.PREC_BITS
        tool = "code/zeta_cert_rosen.py (Arb argument-principle winding box)"

    # --- (0) seed |det| at the claimed point (uncertified midpoint) ---------
    s_seed = acb(arb(re), arb(im))
    det0, tail0, info0, kappa = cert_det(s_seed)
    absdet_seed = abs(complex(float(det0.real.mid()), float(det0.imag.mid())))
    seed_tail_certified = tail0 is not None

    # --- (1) optional Newton refine so the zero sits well inside the box ----
    center_re, center_im = re, im
    newton_info = None
    if refine:
        if use_g5:
            s0, fmin, hist = newton(re, im)
            center_re, center_im = s0.real, s0.imag
            newton_info = {"re": s0.real, "im": s0.imag,
                           "absdet_mid": fmin, "n_steps": len(hist) - 1}
        else:
            s0, fmin, hist = newton(re, im)
            center_re, center_im = s0.real, s0.imag
            newton_info = {"re": s0.real, "im": s0.imag,
                           "absdet_mid": fmin, "n_steps": len(hist) - 1}

    # --- (2) rigorous argument-principle winding box ------------------------
    winding_number = None
    winding_info = None
    dim_tail_certified = False
    for (hx, hy) in boxes:
        w, winfo = winding(center_re, center_im, float(hx), float(hy))
        if w is not None:
            winding_number = int(w)
            winding_info = winfo
            dim_tail_certified = True  # winding_offline only returns w!=None
                                        # when the dim-tail ball was finite at
                                        # every box sample (else it aborts).
            break
        else:
            winding_info = winfo  # remember last failure reason

    # --- (3) verdict: certified iff a SINGLE simple zero is enclosed --------
    certified = bool(winding_number == 1)

    # Build the |det| ball at the box center for the certificate record.
    s_center = acb(arb(center_re), arb(center_im))
    detc, tailc, infoc, _ = cert_det(s_center)
    det_re_lo = float((detc.real).lower())
    det_re_hi = float((detc.real).upper())
    det_im_lo = float((detc.imag).lower())
    det_im_hi = float((detc.imag).upper())
    absdet_center_mid = abs(
        complex(float(detc.real.mid()), float(detc.imag.mid())))

    enclosure = {
        # the certified geometric object: a box in C and the winding count
        "claim": ("s = re + i*im is a simple zero of det(1 - L^{sign}_s) "
                  "for the Hecke G_q transfer operator"),
        "q": q,
        "sign": sign,
        "sign_sector": "even (mms+)" if sign == +1 else "odd (mms-)",
        "kappa": int(kappa),
        "seed_point": {"re": re, "im": im},
        "center_point": {"re": center_re, "im": center_im},
        "winding_number": winding_number,
        "winding_ball": (winding_info or {}).get("winding_ball"),
        "box_hx": (winding_info or {}).get("box_hx"),
        "box_hy": (winding_info or {}).get("box_hy"),
        "tail_fix": (winding_info or {}).get("tail_fix"),
        "K_per_edge": (winding_info or {}).get("K_per_edge", K),
        # the |det| ball at the box center
        "det_real_ball": [det_re_lo, det_re_hi],
        "det_imag_ball": [det_im_lo, det_im_hi],
        "absdet_center_mid": absdet_center_mid,
        "absdet_seed_mid": absdet_seed,
        "N": N, "n_head": n_head, "prec_bits": prec_bits,
        "newton": newton_info,
        # provenance / honesty
        "dim_tail_certified": dim_tail_certified,
        "seed_dim_tail_certified": seed_tail_certified,
        "winding_failure_reason": (
            None if certified or winding_number is not None
            else (winding_info or {}).get("reason")),
    }

    return {
        "method": "argument-principle winding (Arb interval enclosure)",
        "certified": certified,
        "enclosure": enclosure,
        "tool": tool,
        "backend": backend,
        "log": log,
        # caveat surfaced at top level so the orchestrator can read it directly
        "dim_tail_certified": dim_tail_certified,
        "dim_tail_caveat": (
            "Winding rigor rests on a dimension-tail (truncation-remainder) "
            "bound that is VALIDATED (certified-det-increment estimate, "
            "inflated x4 over the box), NOT proved as an analytic theorem. "
            "dim_tail_certified=True means the engine returned finite tail "
            "balls at every box sample; it does NOT assert the tail bound is "
            "a theorem."),
    }


def _local_newton(cert_det_fn, re0, im0, log, iters=40, tol=1e-12, hfd=1e-6):
    """Tiny complex Newton on the certified midpoint det (for the general-q
    engine which lacks a built-in newton).  det is holomorphic off-line, so
    Newton in the single complex variable s is valid."""
    from flint import acb, arb

    def f(z):
        det, _t, _i, _k = cert_det_fn(acb(arb(z.real), arb(z.imag)))
        return complex(float(det.real.mid()), float(det.imag.mid()))

    s = complex(re0, im0)
    fs = f(s)
    hist = [(s.real, s.imag, abs(fs))]
    for _ in range(iters):
        fp = (f(s + hfd) - f(s - hfd)) / (2 * hfd)
        if fp == 0:
            break
        s_new = s - fs / fp
        if s_new.real >= 0.5:
            s_new = complex(0.49, s_new.imag)
        if s_new.real <= 0.0:
            s_new = complex(0.01, s_new.imag)
        fs_new = f(s_new)
        hist.append((s_new.real, s_new.imag, abs(fs_new)))
        if abs(s_new - s) < tol or abs(fs_new) < 1e-18:
            s, fs = s_new, fs_new
            break
        s, fs = s_new, fs_new
    if log is not None:
        log.append(f"  local-newton ({re0:.3f},{im0:.3f}) -> "
                   f"({s.real:.5f},{s.imag:.5f}) |det|={abs(fs):.3e}")
    return s, abs(fs), hist


# ===========================================================================
#  EVALUATOR REGISTRY (pluggable; dispatch on claim["artifact"]).
# ===========================================================================
EVALUATORS = {
    # reference plugin
    "hecke_transfer_operator_zero": _hecke_transfer_operator_evaluator,
}


def register_evaluator(artifact: str, fn) -> None:
    """Register a domain evaluator.  fn(claim) -> dict with at minimum
    {certified: bool, method: str, enclosure: dict, tool: str}."""
    EVALUATORS[artifact] = fn


# ===========================================================================
#  PUBLIC CONTRACT API.
# ===========================================================================
def certify(claim: dict) -> dict:
    """CERTIFY stage entrypoint.

    Args:
        claim: a Claim dict per engine/GOAL.md:
            {id, statement, kind: "numerical"|"theorem", artifact, params}
            For the reference plugin: kind="numerical",
            artifact="hecke_transfer_operator_zero",
            params={q, re, im, sign, N, n_head, ...}.

    Returns:
        Certificate dict per engine/GOAL.md:
            {claim_id, method, enclosure, certified: bool,
             certificate_path, tool}
        plus provenance fields (backend, dim_tail_certified, timestamp, ...).
        Also written to engine/runs/<claim_id>__certify.json as JSON.
    """
    if not isinstance(claim, dict):
        raise TypeError("claim must be a dict (the Claim contract)")
    kind = claim.get("kind", "numerical")
    if kind != "numerical":
        raise ValueError(
            f"certify() handles kind='numerical'; got kind={kind!r}. "
            "Theorem-kind claims go to the verify (Lean) stage.")
    artifact = claim.get("artifact")
    if artifact not in EVALUATORS:
        raise ValueError(
            f"no certify evaluator registered for artifact={artifact!r}; "
            f"known artifacts: {sorted(EVALUATORS)}. Use register_evaluator().")

    cid = _claim_id(claim)
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()

    result = EVALUATORS[artifact](claim)

    finished = datetime.datetime.now(datetime.timezone.utc).isoformat()

    cert_path = os.path.join(_RUNS_DIR, f"{cid}__certify.json")
    certificate = {
        "claim_id": cid,
        "statement": claim.get("statement"),
        "kind": kind,
        "artifact": artifact,
        "params": claim.get("params"),
        "method": result["method"],
        "enclosure": result["enclosure"],
        "certified": bool(result["certified"]),
        "certificate_path": cert_path,
        "tool": result["tool"],
        # provenance / honesty
        "backend": result.get("backend"),
        "dim_tail_certified": result.get("dim_tail_certified"),
        "dim_tail_caveat": result.get("dim_tail_caveat"),
        "log": result.get("log"),
        "timestamps": {"started": started, "finished": finished},
    }
    _atomic_dump(certificate, cert_path)
    return certificate


# ===========================================================================
#  CLI / quick manual run.
# ===========================================================================
if __name__ == "__main__":
    # default: certify the q=3 even resonance and print the Certificate
    demo = {
        "id": "demo_q3_even_resonance",
        "statement": "s=0.25+7.0674i is a simple zero of det(1-L^+_s) for Hecke G_3",
        "kind": "numerical",
        "artifact": "hecke_transfer_operator_zero",
        "params": {"q": 3, "re": 0.25, "im": 7.0674, "sign": +1, "N": 18},
    }
    c = certify(demo)
    print(json.dumps(_san({
        "claim_id": c["claim_id"], "certified": c["certified"],
        "winding": c["enclosure"]["winding_number"],
        "dim_tail_certified": c["dim_tail_certified"],
        "certificate_path": c["certificate_path"],
    }), indent=2))
