"""
run_all_demos.py — drive Aletheia demonstrations D-A / D-B / D-C directly
(main-loop execution; the subagent API was overloaded). Each demo composes the
real engine stages and writes a RunRecord to engine/runs/. D-D (live Aristotle)
is run separately.
"""
from __future__ import annotations
import json, os, sys, time, math, traceback

ROOT = "/Users/za/Documents/farey-hecke"
for p in (ROOT, os.path.join(ROOT, "code"),
          os.path.join(ROOT, "engine/certify"),
          os.path.join(ROOT, "engine/falsify"),
          os.path.join(ROOT, "engine/formal_verify"),
          os.path.join(ROOT, "engine/orchestrator")):
    if p not in sys.path:
        sys.path.insert(0, p)

import certify as CERT
import falsify as FAL
import hecke_plugin as HP
import formal_verify as FV
import orchestrator as ORCH

RUNS = os.path.join(ROOT, "engine/runs")
os.makedirs(RUNS, exist_ok=True)
FIXED_TS = "2026-06-20T12:00:00Z"   # pinned for reproducible run_ids


def _san(o):
    import numpy as np
    if isinstance(o, dict):
        return {k: _san(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_san(v) for v in o]
    if isinstance(o, (np.bool_, bool)):
        return bool(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating, float)):
        return float(o)
    if isinstance(o, complex):
        return {"re": o.real, "im": o.imag}
    if callable(o):
        return f"<callable {getattr(o, '__name__', 'fn')}>"
    try:
        json.dumps(o)
        return o
    except Exception:
        return str(o)


def dump(obj, name):
    path = os.path.join(RUNS, name)
    with open(path, "w") as f:
        json.dump(_san(obj), f, indent=2)
    return path


# ===========================================================================
# D-A : ALL FOUR STAGES REAL — minpoly of lambda_q
# ===========================================================================
from flint import arb, ctx
ctx.prec = 256


def _poly_eval_arb(coeffs, x):
    """Horner eval of monic-ish integer poly (high to low) at arb x -> arb."""
    acc = arb(0)
    for c in coeffs:
        acc = acc * x + arb(int(c))
    return acc


def _poly_root_evaluator(claim):
    """RIGOROUS: certify the real poly has a root in [val-h, val+h] via an
    arb sign-change bracket (the two endpoint balls strictly straddle 0)."""
    p = claim["params"]
    coeffs = p["coeffs"]          # high -> low degree
    val = float(p["value"])       # claimed root 2cos(pi/q)
    h = arb("0.01")
    lo, hi = arb(val) - h, arb(val) + h
    plo, phi = _poly_eval_arb(coeffs, lo), _poly_eval_arb(coeffs, hi)
    # rigorous opposite-sign test (arb comparisons are certified)
    straddles = bool((plo < 0 and phi > 0) or (plo > 0 and phi < 0))
    return {
        "certified": straddles,
        "method": "arb interval sign-change bracket (rigorous IVT)",
        "enclosure": {
            "interval": [float(lo.mid()), float(hi.mid())],
            "p_lo_ball": str(plo), "p_hi_ball": str(phi),
            "poly_coeffs_hi_to_lo": list(coeffs),
        },
        "tool": "python-flint arb @ prec=256",
        "dim_tail_certified": None,
    }


CERT.register_evaluator("polynomial_real_root", _poly_root_evaluator)


def _mk_poly_falsify_params(coeffs, val, other_val):
    """Four adversarial callables for a polynomial-root claim."""
    def horner(cs, x):
        a = 0.0
        for c in cs:
            a = a * x + c
        return a

    def expanded(cs, x):  # independent eval: sum c_i x^(n-i)
        n = len(cs) - 1
        return sum(c * (x ** (n - i)) for i, c in enumerate(cs))

    def control_fn(p):    # a DIFFERENT lambda must NOT be a root
        v = horner(coeffs, other_val)
        return {"passed": abs(v) > 1e-2,
                "detail": f"control value {other_val:.5f} -> |poly|={abs(v):.3e} (want >1e-2: not a root)"}

    def independent_fn(p):  # two eval methods agree ~0 at the root
        a, b = horner(coeffs, val), expanded(coeffs, val)
        return {"passed": abs(a) < 1e-6 and abs(b) < 1e-6 and abs(a - b) < 1e-9,
                "detail": f"horner={a:.2e}, expanded={b:.2e} (both ~0, agree)"}

    def sweep_fn(p):       # |poly(root)| stays ~0 as precision grows
        worst = 0.0
        for pr in (60, 120, 240):
            ctx.prec = pr
            worst = max(worst, abs(float(_poly_eval_arb(coeffs, arb(val)).mid())))
        ctx.prec = 256
        return {"passed": worst < 1e-6,
                "detail": f"|poly(root)| worst over prec {{60,120,240}} = {worst:.2e}"}

    def null_fn(p):        # a perturbed value is NOT a root
        v = horner(coeffs, val + 0.05)
        return {"passed": abs(v) > 1e-2,
                "detail": f"perturbed root+0.05 -> |poly|={abs(v):.3e} (want >1e-2)"}
    return dict(control_fn=control_fn, independent_fn=independent_fn,
                sweep_fn=sweep_fn, null_fn=null_fn)


def _real_verify(claim_id, lemma, project_id="3d185f73-bec0-4932-a2e7-0ef18f0a8948"):
    """Real ProofCertificate from the CACHED Aristotle proof (no new compute)."""
    import tempfile
    dest = tempfile.mkdtemp(prefix="aletheia_demo_verify_")
    root = FV.download_and_extract(project_id, dest)
    return FV.build_certificate(claim_id, lemma, root, project_id=project_id,
                                status="COMPLETE")


def demo_A(q, coeffs, lemma, theorem, other_val, tag):
    val = 2.0 * math.cos(math.pi / q)
    cid = f"demo_A_lambda{q}_minpoly"
    claim = {
        "id": cid,
        "statement": f"lambda_{q} = 2*cos(pi/{q}) = {val:.6f} is a real root of {lemma}",
        "kind": "numerical",
        "artifact": "polynomial_real_root",
        "lemma": lemma,
        "params": {"coeffs": coeffs, "value": val,
                   **_mk_poly_falsify_params(coeffs, val, other_val)},
    }
    # compose the stages DIRECTLY against the registered engine functions
    # (avoids the orchestrator's separate package-path certify instance, which
    # does not carry this process's runtime evaluator registration).
    fal = FAL.falsify(claim)
    cer = CERT.certify(claim)               # CERT has the poly_root evaluator registered
    pc = _real_verify(cid, lemma)           # REAL cached-proof ProofCertificate
    rec = {
        "run_id": ORCH.make_run_id(cid, 0), "schema": "aletheia.runrecord/v1",
        "claim": {"id": cid, "statement": claim["statement"],
                  "kind": claim["kind"], "lemma": lemma},
        "falsify": fal, "certify": cer, "verify": pc,
        "stage_status": {"falsify": {"source": "real"},
                         "certify": {"source": "real"},
                         "verify": {"source": "real",
                                    "note": f"cached Aristotle proof {pc.get('project_id')} ({theorem})"}},
        "verdict": fal.get("verdict"),
        "timestamps": {"started": FIXED_TS, "finished": FIXED_TS},
    }
    rec["synthesis"] = ORCH.synthesize(rec) if hasattr(ORCH, "synthesize") else ""
    path = dump(rec, f"{cid}.json")
    print(f"[D-A {tag}] falsify={rec['falsify'].get('verdict')} "
          f"certify={rec['certify'].get('certified')} "
          f"verify.proved={pc.get('proved')} sorry_free={pc.get('sorry_free')} "
          f"axioms={pc.get('axioms')} -> {os.path.basename(path)}")
    return rec


# ===========================================================================
# D-B : ADVERSARIAL TEETH — false claim refuted, true claim survives
# ===========================================================================
def demo_B():
    out = {}
    # full-precision Newton coords of a genuine G_5 even resonance (sharp zero);
    # the FALSE twin sits on Re=1/4 at the SAME Im (like arith q=3) -> not a zero.
    cases = [
        ("false", 0.25, 5.76353724, "FALSE: G_5 resonance sits on Re=1/4 (like arith q=3)"),
        ("true", 0.45389518, 5.76353724, "TRUE: genuine G_5 even resonance (full-precision coords)"),
    ]
    for tag, re, im, desc in cases:
        claim = HP.make_resonance_claim(re, im, q=5, claim_id=f"demo_B_{tag}_s_{re}_{im}")
        claim["statement"] = desc + " :: " + claim["statement"]
        rep = FAL.falsify(claim)
        failed = [a["name"] for a in rep.get("attempts", []) if not a.get("result", {}).get("passed")]
        rec = {"run_id": f"demo_B_{tag}", "schema": "aletheia.runrecord/v1",
               "claim": {k: claim[k] for k in ("id", "statement", "kind")},
               "falsify": rep, "verdict": rep.get("verdict"),
               "failed_probes": failed, "timestamps": {"started": FIXED_TS}}
        path = dump(rec, f"demo_B_{tag}.json")
        print(f"[D-B {tag}] verdict={rep.get('verdict')} failed_probes={failed} -> {os.path.basename(path)}")
        out[tag] = rec
    return out


# ===========================================================================
# D-C : NOVEL CERTIFIED — arithmeticity signature across 3 surfaces
# ===========================================================================
def _certify_point(q, re, im, sign=+1, cid=None):
    claim = {"id": cid or f"res_q{q}_{re:.4f}_{im:.4f}",
             "kind": "numerical", "artifact": "hecke_transfer_operator_zero",
             "params": {"q": q, "re": re, "im": im, "sign": sign, "N": 18, "refine": True}}
    return CERT.certify(claim)


def demo_C():
    import numpy as np
    geo = json.load(open(os.path.join(ROOT, "code/out/resonance_geometry.json")))
    g7 = json.load(open(os.path.join(ROOT, "code/out/resonance_g7.json")))
    def restd(pts):
        r = [p["re"] for p in pts]
        return {"n": len(r), "re_std": float(np.std(r)),
                "re_min": float(min(r)), "re_max": float(max(r))}
    sig = {
        "q3_arith": {**restd(geo["q3_even_resonances"]), "shape": "vertical line Re=1/4"},
        "g5_nonarith": {**restd(geo["g5_even_resonances"]), "shape": "scattered cloud"},
        "g7_nonarith": {**restd(g7["g7_even_resonances"]), "shape": "scattered cloud"},
    }
    # ADVERSARIAL pre-check: does the general-q engine reproduce a known q=5 point?
    pre = _certify_point(5, 0.45389518, 5.76353724, cid="precheck_g5")
    g7_ok = bool(pre.get("certified"))
    # certify representative anchors
    anchors = []
    for (q, re, im, lbl) in [(3, 0.25, 7.0674, "q3 on Re=1/4"),
                             (5, 0.45389518, 5.76353724, "g5 cloud pt"),
                             (5, 0.485, 13.565, "g5 near-line pt")]:
        c = _certify_point(q, re, im, cid=f"anchor_{lbl.replace(' ','_')}")
        anchors.append({"label": lbl, "q": q, "re": re, "im": im,
                        "certified": c.get("certified"),
                        "winding": (c.get("enclosure") or {}).get("winding_number")})
        print(f"[D-C] anchor {lbl}: certified={c.get('certified')} winding={(c.get('enclosure') or {}).get('winding_number')}")
    rec = {
        "run_id": "demo_C_arith_signature", "schema": "aletheia.runrecord/v1",
        "claim": {"id": "arith_signature",
                  "statement": ("Resonance geometry detects arithmeticity: the arithmetic "
                                "Hecke surface q=3 has even-sector resonances on a vertical "
                                "LINE (Re=1/4, the Riemann zeros); the non-arithmetic G_5 and "
                                "G_7 have them SCATTERED in Re (clouds). Scattering / "
                                "continuous-spectrum resonances, certified by Arb winding."),
                  "kind": "numerical"},
        "signature": sig,
        "certified_anchors": anchors,
        "g7_engine_precheck_reproduces_q5": g7_ok,
        "timestamps": {"started": FIXED_TS},
    }
    path = dump(rec, "demo_C_arith_signature.json")
    print(f"[D-C] signature: q3 std={sig['q3_arith']['re_std']:.2e} | "
          f"g5 std={sig['g5_nonarith']['re_std']:.3f} | g7 std={sig['g7_nonarith']['re_std']:.3f} "
          f"| g7_engine_precheck={g7_ok} -> {os.path.basename(path)}")
    return rec


if __name__ == "__main__":
    t0 = time.time()
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("all", "A"):
        print("=== D-A: all four stages real ===")
        try:
            demo_A(5, [1, -1, -1], "x^2 - x - 1 = 0", "hecke_lambda_five",
                   2 * math.cos(math.pi / 7), "lambda5")  # coeffs hi->lo: x^2 - x - 1
        except Exception:
            traceback.print_exc()
        try:
            demo_A(7, [1, -1, -2, 1], "x^3 - x^2 - 2x + 1 = 0", "hecke_lambda_seven",
                   2 * math.cos(math.pi / 5), "lambda7")
        except Exception:
            traceback.print_exc()
    if which in ("all", "B"):
        print("=== D-B: adversarial teeth ===")
        try:
            demo_B()
        except Exception:
            traceback.print_exc()
    if which in ("all", "C"):
        print("=== D-C: novel certified arithmeticity signature ===")
        try:
            demo_C()
        except Exception:
            traceback.print_exc()
    print(f"\n[done {time.time()-t0:.1f}s]")
