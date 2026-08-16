#!/usr/bin/env python3
"""
q3diag_detK.py -- LANE G / PC.9 + PC.10 SETTLED.

MMS (Mayer-Muehlenbruch-Stroemberg, arXiv:0912.2236, "The transfer operator for
the Hecke triangle groups"), Theorem `main-theorem` (= eq. \\eqref{LoverK} of the
introduction):

      Z_S(s) = det(1 - L_s) / det(1 - K_s)
             = det[(1 - L_{s,+})(1 - L_{s,-})] / det(1 - K_s).

The DENOMINATOR is missing from the repo builders.  MMS's own reason (intro,
p.2): the Hurwitz-Nakada map f_q has TWO periodic points r_q, -r_q that are
G_q-equivalent, so det(1-L_s) counts the corresponding closed geodesic TWICE;
K_s := L_s^{O_+} removes one copy.

MMS Proposition (Sec. `secK`) gives sigma(K_s) explicitly:

      sigma(K_s) = { prod_{l=0}^{kappa_q - 1} ( f_q^l(r_q) )^{2s+2n},  n >= 0 },

so, writing  b_q := prod_{l=0}^{kappa_q-1} ( f_q^l(r_q) )^2  (a positive number,
= psi'(z*) in MMS's proof),

      det(1 - K_s) = prod_{n>=0} ( 1 - b_q^{s+n} ).                        (D)

r_q = [0; \\ov{3}] for q = 3, [0; \\ov{1^{h-1},2}] for even q = 2h+2, and
[0; \\ov{1^h,2,1^{h-1},2}] for odd q = 2h+3 >= 5 (MMS Lemma `lemma:det_op`).
MMS's Remark gives the closed forms  b_q = (2-lam)/(2+lam)  for even q; this
file re-derives b_q from the orbit product and cross-checks against it.

For q = 3, b_3 = ((3-sqrt5)/2)^2 = phi^{-4} = 1/6.854102..., i.e. det(1-K_s) is
exactly the Selberg Euler factor prod_k (1 - N(P)^{-s-k}) of the SHORTEST closed
geodesic on the modular surface (N(P) = phi^4, discriminant 5).

TESTS RUN HERE
  T1  q=3, six mirror points: is  P_repo / P_indep_Mayer  ==  |det(1-K_s)| ?
  T2  q=3, large sigma (2,3,4): same.
  T3  q=3,4,6 sigma sweeps: does dividing the repo P by |det(1-K)| collapse the
      mirror-identity ratio to 1?   ratio_corrected = ratio_repo * D(s)/D(1-s).
  T4  zeros of det(1-K_s): s in -N_0 + i(2pi/log b_q) Z  -- all with Re s <= 0.

All repo/Mayer numbers are READ from the already-banked JSON receipts
(q3cont_compare.json, q3cont_largesigma.json, mirror_u4_corrected.json,
q3cont_q4_sigmasweep.json); no existing file is modified and no determinant is
recomputed here.  The only new computation is (D), which is elementary.

Run: /Users/za/miniforge3/envs/pari-arb/bin/python3 q3diag_detK.py
"""
from __future__ import annotations
import json
from pathlib import Path
from mpmath import mp, mpf, mpc, sqrt, log, pi, exp, fabs

mp.dps = 40
HERE = Path(__file__).parent
TINF = mpf('7.0673625708673465')


# ---------------------------------------------------------------- b_q
def lam(q):
    return 2 * mp.cos(pi / q)


def cf_value(word, lm, cycles=400):
    """[0; \\ov{word}] in the lambda-CF convention x = -1/(a*lam + x)."""
    x = mpf(0)
    for _ in range(cycles):
        for a in reversed(word):
            x = -1 / (a * lm + x)
    return x


def r_word(q):
    if q == 3:
        return [3]
    if q % 2 == 0:
        h = (q - 2) // 2
        return [1] * (h - 1) + [2]
    h = (q - 3) // 2
    return [1] * h + [2] + [1] * (h - 1) + [2]


def b_q(q):
    """b_q = prod_{l=0}^{kappa-1} (f^l(r_q))^2, orbit = cyclic shifts of the word."""
    lm = lam(q)
    w = r_word(q)
    k = len(w)
    prod = mpf(1)
    for i in range(k):
        prod *= cf_value(w[i:] + w[:i], lm) ** 2
    return prod, k


def det_1_minus_K(s, q, terms=200):
    """det(1-K_s) = prod_{n>=0} (1 - b_q^{s+n})  -- eq. (D)."""
    b, _ = b_q(q)
    out = mpc(1)
    for n in range(terms):
        t = exp((s + n) * log(b))
        out *= (1 - t)
        if abs(t) < mpf(10) ** (-mp.dps - 5) and n > 2:
            break
    return out


def D(sigma, sign_t, q):
    """|det(1-K)| at s = sigma + i*sign_t*TINF."""
    return fabs(det_1_minus_K(mpc(mpf(sigma), sign_t * TINF), q))


# ---------------------------------------------------------------- report
def main():
    out = {"source": "MMS arXiv:0912.2236, Theorem `main-theorem` / eq (LoverK); "
                     "Proposition in Sec. secK for sigma(K_s)",
           "identity": "Z_S = det(1-L_s)/det(1-K_s); repo builders compute the "
                       "NUMERATOR only",
           "b_q": {}, "T1_q3_six_points": [], "T2_q3_large_sigma": [],
           "T3_sigma_sweeps": {}, "T4_detK_zeros": {}}

    print("b_q = prod (f^l(r_q))^2   [MMS Prop., Sec. secK]")
    for q in (3, 4, 5, 6, 7, 8):
        b, k = b_q(q)
        row = {"kappa": k, "b_q": float(b), "1/b_q": float(1 / b),
               "word": r_word(q)}
        if q % 2 == 0:                       # MMS Remark closed form, even q
            lm = lam(q)
            row["MMS_remark_closed_form"] = float((2 - lm) / (2 + lm))
            row["closed_form_rel_err"] = float(
                fabs(b - (2 - lm) / (2 + lm)) / b)
        out["b_q"][str(q)] = row
        print(f"  q={q}  kappa={k}  word={r_word(q)}  b_q={float(b):.12f}  "
              f"1/b_q={float(1/b):.9f}"
              + (f"   [MMS remark (2-lam)/(2+lam) rel err "
                 f"{row['closed_form_rel_err']:.2e}]" if q % 2 == 0 else ""))
    print(f"  q=3 check: phi^-4 = {float((( 1+sqrt(5))/2)**-4):.15f}")

    # ---- T1
    print("\nT1  q=3: is  P_repo/P_indep == |det(1-K_s)| ?")
    cmp = json.load(open(HERE / "q3cont_compare.json"))
    print(f"  {'sigma':>6} {'point':>8} {'measured P_repo/P_indep':>24} "
          f"{'|det(1-K)| predicted':>22} {'rel err':>10}")
    for r in cmp["rows"]:
        for lab, key, sg, st in (("s", "P_repo_over_P_mayer_at_s",
                                  r["sigma"], +1),
                                 ("1-s", "P_repo_over_P_mayer_at_1ms",
                                  1 - r["sigma"], -1)):
            meas = r[key]
            pred = float(D(sg, st, 3))
            rel = abs(meas - pred) / abs(meas)
            out["T1_q3_six_points"].append(
                {"sigma": r["sigma"], "point": lab, "Re_s": sg,
                 "measured": meas, "predicted_absdetK": pred, "rel_err": rel})
            print(f"  {r['sigma']:6.2f} {lab:>8} {meas:24.9f} {pred:22.9f} "
                  f"{rel:10.2e}")

    # ---- T2
    print("\nT2  q=3 large sigma (Sec.4 of the parent note)")
    ls = json.load(open(HERE / "q3cont_largesigma.json"))
    for r in ls["rows"]:
        meas, pred = r["ratio"], float(D(r["sigma"], +1, 3))
        rel = abs(meas - pred) / abs(meas)
        out["T2_q3_large_sigma"].append(
            {"sigma": r["sigma"], "measured": meas,
             "predicted_absdetK": pred, "rel_err": rel})
        print(f"  sigma={r['sigma']:.1f}  measured={meas:.12f}  "
              f"predicted={pred:.12f}  rel err={rel:.2e}")

    # ---- T3
    print("\nT3  mirror-identity ratio, corrected:  ratio_corr = "
          "ratio_repo * D(s)/D(1-s)")
    sweeps = {}
    sw3 = json.load(open(HERE / "mirror_u4_corrected_sigmasweep.json"))
    sweeps["3"] = sw3
    sw4 = json.load(open(HERE / "q3cont_q4_sigmasweep.json"))
    sweeps["4"] = sw4
    mu = json.load(open(HERE / "mirror_u4_corrected.json"))
    out["_sweep_files"] = ["mirror_u4_corrected_sigmasweep.json",
                           "q3cont_q4_sigmasweep.json",
                           "mirror_u4_corrected.json"]

    def rows_of(obj):
        """the banked sweep rows; every one of the three JSONs stores the
        corrected mirror ratio under the key "ratio" in obj["rows"]."""
        return obj["rows"]

    for qs, obj in (("3", sw3), ("4", sw4)):
        q = int(qs)
        rows = rows_of(obj)
        res = []
        print(f"\n  q = {q}")
        print(f"    {'sigma':>6} {'ratio_repo':>12} {'D(s)/D(1-s)':>14} "
              f"{'ratio_corrected':>16}")
        for r in rows:
            sg = r["sigma"]
            rr = r["ratio"]
            f = float(D(sg, +1, q) / D(1 - sg, -1, q))
            rc = rr * f
            res.append({"sigma": sg, "ratio_repo": rr,
                        "D_s_over_D_1ms": f, "ratio_corrected": rc})
            print(f"    {sg:6.2f} {rr:12.6f} {f:14.6f} {rc:16.9f}")
        out["T3_sigma_sweeps"][qs] = res

    # the three-point table of mirror_u4_corrected.json, all q incl. 6
    print("\n  mirror_u4_corrected.json three-point table, all q:")
    print(f"    {'q':>2} {'sigma':>6} {'ratio_repo':>12} {'D(s)/D(1-s)':>14} "
          f"{'ratio_corrected':>16}")
    tab = []
    for r in rows_of(mu):
        q = int(r.get("q", 0))
        if q not in (3, 4, 6):
            continue
        sg = r["sigma"]
        rr = r["ratio_corrected"]
        f = float(D(sg, +1, q) / D(1 - sg, -1, q))
        tab.append({"q": q, "sigma": sg, "ratio_repo": rr,
                    "D_s_over_D_1ms": f, "ratio_corrected": rr * f,
                    "ratio_key": key[0]})
        print(f"    {q:2d} {sg:6.2f} {rr:12.6f} {f:14.6f} {rr*f:16.9f}")
    out["T3_three_point_table"] = tab

    # ---- T4
    print("\nT4  zeros of det(1-K_s):  s = -n + 2 pi i k / log b_q")
    for q in (3, 4, 5, 6):
        b, _ = b_q(q)
        sp = float(2 * pi / fabs(log(b)))
        out["T4_detK_zeros"][str(q)] = {
            "Re_s_values": "0, -1, -2, ...",
            "imag_spacing_2pi_over_log_b": sp}
        print(f"  q={q}: Re s in -N_0, Im spacing {sp:.9f}  "
              f"(zero-free for Re s > 0)")

    p = HERE / "q3diag_detK.json"
    json.dump(out, open(p, "w"), indent=1)
    print("\nwrote", p)


if __name__ == "__main__":
    main()
