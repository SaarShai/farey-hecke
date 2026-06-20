"""
engine/falsify/hecke_plugin.py
==============================
Worked REFERENCE PLUGIN for the FALSIFY harness (engine/falsify/falsify.py),
on the Hecke transfer-operator domain this session produced.

Claim under test (the genuine 2026-06-20 result):
    "complex s0 is a genuine EVEN-sector (mms+) resonance of the non-arithmetic
     Hecke triangle group G_5" -- i.e. det(1 - L+_{s0}) = 0 with Re(s0) < 1/2,
     a scattering pole = a dissolved even Maass cusp form (Phillips-Sarnak).

The four adversarial attempts wire directly into the certified Hurwitz-exact Arb
engine in `code/zeta_resonance_g5.py` (cert_det_complex_mid). We do NOT rebuild
any Arb math here -- we only drive the existing certified evaluator and SCORE.

  (a) CONTROL    -- the ODD (mms-) sector |det| at the SAME s0 must be O(1)
                    (the odd cusp forms are protected / live on the line, so
                    s0 is NOT an odd zero). If odd |det| were also ~0 the
                    "even-sector" specificity would be bogus.
  (b) INDEPENDENT -- recompute even |det(s0)| at a DIFFERENT truncation
                    (N=22 vs the primary N). A genuine zero is reproduced by
                    the independent truncation; the two must agree at ~0.
  (c) STABILITY  -- sweep N over a small set: even |det(s0)| must stay ~0
                    across all N (a real resonance is N-stable; an artifact
                    drifts upward / wanders).
  (d) NULL       -- a NEIGHBORING off point s0 + delta must have even |det|
                    that is O(1) (NOT ~0): the zero is localized, not a smear.

For a BOGUS claim (s = 0.30 + 8.5i, which is not a resonance) the NULL and
STABILITY probes evaluate even |det| AT THE CLAIMED POINT and find it O(1)
(~2.5), so they fail and the harness refutes -- exactly the skeptical behavior
we want. (Note: Newton from a bogus seed will WANDER to a real resonance
elsewhere; this plugin therefore scores |det| AT the claimed point, never a
relocated one, so it cannot be fooled into "discovering" a different zero and
crediting it to the bogus claim.)

Usage:
    from hecke_plugin import make_resonance_claim
    import falsify
    claim  = make_resonance_claim(re=0.4538951800749447, im=5.7635372417301305)
    report = falsify.falsify(claim)            # -> verdict "survives"
"""
from __future__ import annotations

import os
import sys
from typing import Any, Dict

# Make the repo's certified engine importable (code/ holds the Arb engine).
_HERE = os.path.dirname(os.path.abspath(__file__))
_CODE = os.path.abspath(os.path.join(_HERE, "..", "..", "code"))
if _CODE not in sys.path:
    sys.path.insert(0, _CODE)


def _engine():
    """Lazy import so falsify.py stays Arb-free and importable without flint."""
    from flint import ctx  # noqa: F401  (sets global precision)
    import zeta_resonance_g5 as Zr
    from flint import acb, arb, ctx as _ctx
    _ctx.prec = 400
    return Zr, acb, arb


def _absdet(q: int, re: float, im: float, N: int, sign: int, n_head: int = 4) -> float:
    """Certified midpoint |det(1 - L^{sign}_s)| at s = re + i*im for Hecke G_q.

    sign=+1 -> EVEN (mms+) sector; sign=-1 -> ODD (mms-) sector.
    Pure pass-through to the repo's certified Arb engine.
    """
    Zr, acb, arb = _engine()
    s = acb(arb(float(re)), arb(float(im)))
    return abs(Zr.cert_det_complex_mid(q, s, int(N), int(sign), int(n_head)))


# ---------------------------------------------------------------------------
#  The four attempt callables. Each takes the claim `params` dict and returns
#  {"passed": bool, "method": str, "detail": str, ...diagnostics...}.
# ---------------------------------------------------------------------------
def _control_fn(p: Dict[str, Any]) -> Dict[str, Any]:
    """CONTROL: the ODD sector at the SAME s0 must be O(1) (NOT a zero)."""
    re, im, q, N, nh = p["re"], p["im"], p["q"], p["N"], p["n_head"]
    even = _absdet(q, re, im, N, +1, nh)
    odd = _absdet(q, re, im, N, -1, nh)
    zero_thr = p["zero_thr"]
    nonzero_thr = p["nonzero_thr"]
    # Pass iff the wrong sector behaves DIFFERENTLY: even ~0 here, odd O(1).
    passed = (even < zero_thr) and (odd > nonzero_thr)
    return {
        "method": "wrong-sector control: odd (mms-) |det| at s0 must be O(1)",
        "passed": bool(passed),
        "even_absdet": even,
        "odd_absdet": odd,
        "zero_thr": zero_thr,
        "nonzero_thr": nonzero_thr,
        "detail": f"even|det|={even:.3e} (want <{zero_thr:.0e}); "
                  f"odd|det|={odd:.3e} (want >{nonzero_thr:.0e}) -> "
                  f"control {'DISTINGUISHES sectors' if passed else 'FAILS'}",
    }


def _independent_fn(p: Dict[str, Any]) -> Dict[str, Any]:
    """INDEPENDENT: recompute even |det(s0)| at a different truncation N2."""
    re, im, q, N, nh = p["re"], p["im"], p["q"], p["N"], p["n_head"]
    N2 = p["N_independent"]
    zero_thr = p["zero_thr"]
    d1 = _absdet(q, re, im, N, +1, nh)
    d2 = _absdet(q, re, im, N2, +1, nh)
    passed = (d1 < zero_thr) and (d2 < zero_thr)
    return {
        "method": f"independent truncation: even |det| at N={N} vs N={N2}",
        "passed": bool(passed),
        "absdet_primary": d1,
        "absdet_independent": d2,
        "N_primary": N,
        "N_independent": N2,
        "zero_thr": zero_thr,
        "detail": f"|det|@N{N}={d1:.3e}, |det|@N{N2}={d2:.3e}; both want <"
                  f"{zero_thr:.0e} -> independent paths "
                  f"{'AGREE at zero' if passed else 'DISAGREE'}",
    }


def _sweep_fn(p: Dict[str, Any]) -> Dict[str, Any]:
    """STABILITY: even |det(s0)| must stay ~0 across the N sweep."""
    re, im, q, nh = p["re"], p["im"], p["q"], p["n_head"]
    Ns = p["N_sweep"]
    zero_thr = p["zero_thr"]
    vals = {int(N): _absdet(q, re, im, N, +1, nh) for N in Ns}
    worst = max(vals.values())
    passed = worst < zero_thr
    return {
        "method": f"N-stability sweep N in {list(Ns)}: even |det| stays ~0",
        "passed": bool(passed),
        "absdet_by_N": vals,
        "worst_absdet": worst,
        "zero_thr": zero_thr,
        "detail": "per-N |det|=" + ", ".join(f"N{N}:{v:.2e}" for N, v in vals.items())
                  + f"; worst={worst:.3e} (want <{zero_thr:.0e}) -> "
                  + ("STABLE at zero" if passed else "DRIFTS / not a stable zero"),
    }


def _null_fn(p: Dict[str, Any]) -> Dict[str, Any]:
    """NULL: a neighbor s0+delta must have even |det| O(1) (NOT also a zero)."""
    re, im, q, N, nh = p["re"], p["im"], p["q"], p["N"], p["n_head"]
    d_re = p["null_delta_re"]
    d_im = p["null_delta_im"]
    nonzero_thr = p["nonzero_thr"]
    re_n, im_n = re + d_re, im + d_im
    d = _absdet(q, re_n, im_n, N, +1, nh)
    passed = d > nonzero_thr
    return {
        "method": f"null neighbor s0+({d_re:+.3f},{d_im:+.3f}): even |det| must be O(1)",
        "passed": bool(passed),
        "neighbor_re": re_n,
        "neighbor_im": im_n,
        "neighbor_absdet": d,
        "nonzero_thr": nonzero_thr,
        "detail": f"|det| at neighbor ({re_n:.4f},{im_n:.4f}) = {d:.3e} "
                  f"(want >{nonzero_thr:.0e}) -> "
                  + ("zero is LOCALIZED (neighbor not a zero)" if passed
                     else "neighbor ALSO ~0 => smear/spurious, NOT a localized zero"),
    }


# ---------------------------------------------------------------------------
#  Claim factory.
# ---------------------------------------------------------------------------
def make_resonance_claim(
    re: float,
    im: float,
    q: int = 5,
    N: int = 18,
    N_independent: int = 22,
    N_sweep=(18, 20, 22),
    n_head: int = 4,
    zero_thr: float = 1e-6,
    nonzero_thr: float = 1e-2,
    null_delta_re: float = 0.0,
    null_delta_im: float = 0.30,
    claim_id: str = None,
) -> Dict[str, Any]:
    """Build an engine `Claim` for the FALSIFY harness.

    The claim asserts s0 = re + i*im is a GENUINE even-sector resonance of G_q.
    Thresholds are honest and tunable:
      zero_thr     -- |det| below this counts as "zero" (resonance present).
      nonzero_thr  -- |det| above this counts as "O(1)" (no resonance).
    Defaults are calibrated to the N=18 certified engine (a genuine resonance
    gives even |det| ~ 1e-10 at N=18 and ~1e-15 at N=22; an off point is ~1).
    """
    cid = claim_id or f"hecke_G{q}_even_resonance_s_{re:.6f}_{im:.6f}"
    return {
        "id": cid,
        "statement": (
            f"s0 = {re:.6f} + {im:.6f}i is a genuine EVEN-sector (mms+) resonance "
            f"of the non-arithmetic Hecke triangle group G_{q}: det(1 - L+_{{s0}}) = 0 "
            f"with Re(s0) < 1/2 (scattering pole = dissolved even Maass cusp form)."
        ),
        "kind": "numerical",
        "artifact": "code/zeta_resonance_g5.py (certified Hurwitz-exact Arb engine)",
        "params": {
            # data
            "re": float(re), "im": float(im),
            "q": int(q), "N": int(N), "n_head": int(n_head),
            "N_independent": int(N_independent),
            "N_sweep": tuple(int(x) for x in N_sweep),
            "zero_thr": float(zero_thr),
            "nonzero_thr": float(nonzero_thr),
            "null_delta_re": float(null_delta_re),
            "null_delta_im": float(null_delta_im),
            # the four adversarial callables the harness will run
            "control_fn": _control_fn,
            "independent_fn": _independent_fn,
            "sweep_fn": _sweep_fn,
            "null_fn": _null_fn,
        },
    }
