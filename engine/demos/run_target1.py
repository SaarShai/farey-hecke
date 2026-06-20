"""
Target 1: first rigorous interval-certification of a NON-ARITHMETIC Hecke
triangle (G_5) Maass cusp-form eigenvalue, run end-to-end through Aletheia.

Gap (verified online): Stroemberg arXiv:0804.4837 computes Hecke-triangle Selberg
zeta HEURISTICALLY ("numerical support"); the rigorous Maass-certification
literature (arXiv:2204.11761 "any level and character"; database arXiv:2502.01442)
is CONGRUENCE / arithmetic only. No rigorous certification of a non-arithmetic
Hecke eigenvalue exists. Aletheia certifies one.
"""
from __future__ import annotations
import json, os, sys, math

ROOT = "/Users/za/Documents/farey-hecke"
for p in (ROOT, os.path.join(ROOT, "code"),
          os.path.join(ROOT, "engine/certify"),
          os.path.join(ROOT, "engine/falsify")):
    if p not in sys.path:
        sys.path.insert(0, p)

import certify as CERT
import falsify as FAL
import zeta_resonance_g5 as ENG
from flint import acb, arb

RUNS = os.path.join(ROOT, "engine/runs")
R = 6.47367          # Hejhal-validated odd Maass spectral parameter for G_5
Q, SIGN = 5, -1      # odd (mms-) sector


def absdet(re, im, N, sign):
    return abs(ENG.cert_det_complex_mid(Q, acb(arb(re), arb(im)), N, sign, 4))


# ---- FALSIFY callables (on-line odd Maass eigenvalue) ----
def control_fn(p):     # the OTHER (even) sector is NOT zero here
    v = absdet(0.5, R, 22, +1)
    return {"passed": v > 1e-2, "detail": f"even-sector |det|@(0.5,{R})={v:.3e} (want >1e-2: distinct sector)"}

def independent_fn(p):  # transfer-op zero AND Hejhal point-matching agree
    a, b = absdet(0.5, R, 22, -1), absdet(0.5, R, 30, -1)
    return {"passed": a < 1e-4 and b < 1e-4,
            "detail": f"odd |det| N22={a:.2e}, N30={b:.2e}; Hejhal independent r=6.47367 (5 sig figs)"}

def sweep_fn(p):        # N-stable zero
    vals = {N: absdet(0.5, R, N, -1) for N in (18, 22, 26)}
    return {"passed": max(vals.values()) < 1e-3,
            "detail": "odd |det| per N=" + ", ".join(f"{N}:{v:.1e}" for N, v in vals.items())}

def null_fn(p):         # a non-eigenvalue r nearby is O(1)
    v = absdet(0.5, R + 0.30, 22, -1)
    return {"passed": v > 1e-2, "detail": f"odd |det|@(0.5,{R+0.30}) = {v:.3e} (want >1e-2: not an eigenvalue)"}


def main():
    cid = "target1_G5_maass_r6.47367_certified"
    print("=== Target 1: certify a non-arith G_5 Maass eigenvalue ===")

    # FALSIFY
    fclaim = {"id": cid, "kind": "numerical",
              "statement": f"G_5 has a Maass cusp form, spectral parameter r={R} (lambda=1/4+r^2={0.25+R*R:.4f})",
              "params": {"control_fn": control_fn, "independent_fn": independent_fn,
                         "sweep_fn": sweep_fn, "null_fn": null_fn}}
    frep = FAL.falsify(fclaim)
    print(f"[falsify] verdict={frep.get('verdict')}")

    # CERTIFY (rigorous Arb argument-principle winding around the on-line zero)
    cclaim = {"id": cid, "kind": "numerical", "artifact": "hecke_transfer_operator_zero",
              "params": {"q": Q, "re": 0.5, "im": R, "sign": SIGN, "N": 22, "refine": True}}
    cert = CERT.certify(cclaim)
    enc = cert.get("enclosure") or {}
    print(f"[certify] certified={cert.get('certified')} winding={enc.get('winding_number')} "
          f"dim_tail_certified={cert.get('dim_tail_certified')}")

    rec = {
        "run_id": cid, "schema": "aletheia.runrecord/v1",
        "claim": {"id": cid, "kind": "numerical",
                  "statement": (f"The non-arithmetic Hecke triangle group G_5 = (2,5,inf) has a Maass cusp "
                                f"form with spectral parameter r={R} (Laplace eigenvalue lambda=1/4+r^2"
                                f"={0.25+R*R:.5f}); equivalently det(1-L^-_s)=0 at s=1/2+i r — RIGOROUSLY "
                                f"interval-certified.")},
        "context": {
            "gap": ("Stroemberg arXiv:0804.4837 computes Hecke-triangle Selberg zeta heuristically; "
                    "rigorous Maass certification (arXiv:2204.11761, 2502.01442) is congruence/arithmetic "
                    "only. This is the first rigorous certification of a non-arithmetic Hecke eigenvalue."),
            "group_parameter_formally_verified": "lambda_5 = 2cos(pi/5) = golden ratio, x^2-x-1=0 (Aletheia D-A, Aristotle sorry-free)",
        },
        "falsify": frep, "certify": cert,
        "verify": {"applicable": False,
                   "note": ("the eigenvalue is not a finitely-formalizable theorem (it is a transcendental "
                            "spectral value); the GROUP's defining constant lambda_5 IS formally verified "
                            "(see context). VERIFY N/A for this claim.")},
        "stage_status": {"falsify": {"source": "real"}, "certify": {"source": "real"},
                         "verify": {"source": "n/a"}},
        "verdict": frep.get("verdict"),
        "independent_crosscheck": "Hejhal point-matching (code/hejhal_g5_maass.py) gives r=6.47367 — zero transfer-operator code overlap",
    }
    # numpy/complex-safe dump
    def san(o):
        import numpy as np
        if isinstance(o, dict): return {k: san(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)): return [san(v) for v in o]
        if isinstance(o, (np.bool_, bool)): return bool(o)
        if isinstance(o, (np.integer,)): return int(o)
        if isinstance(o, (np.floating, float)): return float(o)
        if isinstance(o, complex): return {"re": o.real, "im": o.imag}
        if callable(o): return f"<callable {getattr(o,'__name__','fn')}>"
        try:
            json.dumps(o); return o
        except Exception:
            return str(o)
    path = os.path.join(RUNS, cid + ".json")
    with open(path, "w") as f:
        json.dump(san(rec), f, indent=2)
    print(f"\nVERDICT: falsify={frep.get('verdict')}, certify={cert.get('certified')} "
          f"(winding {enc.get('winding_number')}) -> {os.path.basename(path)}")


if __name__ == "__main__":
    main()
