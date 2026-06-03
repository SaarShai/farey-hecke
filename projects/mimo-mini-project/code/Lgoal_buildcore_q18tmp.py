#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GOAL L Objective A: build the FULL Lean scalar-window file for a given q in 7..16.
Strategy (see session notes): for q>=7 every interior floor in a complete W-window is forced to
K=1 (Kmax=1), so the window core is the SINGLE (1,..,1) Positivstellensatz case.  Cert is found in
2 variables (a,b) after the linear K=1 recurrence collapses c,d,.. to Chebyshev expressions, then
EMITTED in the natural variable form (coords c,d,.. kept) by bridging each product to its (a,b)-
reduced form via `linear_combination (field + recurrence cofactors)`.  Floor-helper proves K<=1
(the tight (lam^2-lam)^2>=2 contradiction) from the isolating bound 9/5<lam.

Outputs /tmp/lean-minus1/G{q}CORE.lean with:
  g{q}_lam_lo : 9/5 < lam              (synthetic division; for multi-root q it is a hypothesis)
  g{q}_floor_helper                    (K>=2 interior-floor contradiction)
  g{q}_core                            (W+1 coords, both edges, cap, recurrence+floor bounds, all
                                        W products < 1/lam^3  ==>  False)
  g{q}_no_window_below_genuine         (orbit form)
"""
import sys, sympy as sp
from sympy import cos, pi, Rational, minimal_polynomial
sys.path.insert(0, 'code')
import importlib, Lgoal_emit as E
importlib.reload(E)
LAM = E.LAM

UNIQUE_ROOT = {7, 8, 9, 12, 15}        # one minpoly root in (1,2): 9/5<lam from hps alone
WINDOW = {7: 4, 8: 4, 9: 4, 10: 4, 11: 4, 12: 5, 13: 5, 14: 5, 15: 5, 16: 5, 18: 6, 19: 6, 20: 6}
# q=12: W=4 (1,1,1)-window has no deg<=3 Positivstellensatz cert locally; the WEAKER W=5 window
# (no 5 consecutive sub-thr products) is still infeasible AND has a deg-2 cert -> same X_Omega=1/lam^3.
LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g']

def lx(e):
    return str(sp.expand(e)).replace('**', '^')

# ----- synthetic-division data for 9/5 < lam (unique-root q) ----------------------
def synth(q):
    t = sp.symbols('t'); lam = 2*cos(pi/q)
    m = sp.Poly(minimal_polynomial(lam, t), t); d = m.degree()
    mm = [Rational(c, m.all_coeffs()[0]) for c in m.all_coeffs()]
    pmon = sp.Poly([Rational(x) for x in mm], t)
    s = Rational(9, 5)
    quo, _ = sp.div(pmon, sp.Poly(t - s, t))
    r = pmon.eval(s)
    g = sum(c*LAM**(quo.degree() - i) for i, c in enumerate(quo.all_coeffs()))
    return d, lx(g), str(-r)

def field_relation(q):
    F = E.field(q); d = F['d']
    rhs = sum(F['tail'][j]*LAM**(d-1-j) for j in range(d))
    return d, lx(rhs)

# ----- the (1,..,1) core cert in 2 vars, emitted in variable form ----------------
def build_core_cert(q, W):
    F = E.field(q)
    coords_v = sp.symbols(' '.join(LETTERS[:W+1]))          # variable coords a,b,c,..
    coords_v = list(coords_v)
    a, b = coords_v[0], coords_v[1]
    # recurrence (K=1): coords_ab[i] = expression in a,b (reduced)
    coords_ab = [a, b]
    for j in range(W-1):
        coords_ab.append(E.redp(LAM*coords_ab[-1] - coords_ab[-2], F))
    # generators in BOTH var form (for mul_nonneg) and ab form (for the LP / red)
    # each gen: (lean_name, var_expr, ab_expr, src_kind, src_idx)
    G = []
    def add(name, ve, src):
        G.append((name, sp.expand(ve), E.redp(ve.subs({coords_v[i]: coords_ab[i] for i in range(W+1)}), F), src))
    for i in range(W+1): add(f'pos{i}', coords_v[i], ('pos', i))
    for i in range(W+1): add(f'cap{i}', 1 - coords_v[i], ('cap', i))
    for i in range(W):   add(f'reg{i}', coords_v[i] + LAM*coords_v[i+1] - 1, ('reg', i))
    for i in range(W):   add(f'gen{i}', LAM*coords_v[i] + coords_v[i+1] - 1, ('gen', i))
    for i in range(W):   add(f'slk{i}', 1 - coords_v[i]*coords_v[i+1]*LAM**3, ('slk', i))
    for i in range(W-1): add(f'flu{i}', 2*LAM*coords_v[i+1] - 1 - coords_v[i], ('flu', i))
    # LP over ab forms (2-var); try degree-2 cone then degree-3
    gens_ab = [(g[0], g[2]) for g in G]
    a_, b_ = a, b
    r = E.lp_cert(F, [a_, b_], gens_ab, [], [])
    if r is None:
        r = E.lp_cert(F, [a_, b_], gens_ab, [], [], deg3=True)
    if r is None:
        return None
    usedP, _, _, _ = r
    return F, coords_v, coords_ab, G, usedP

def emit_case(q, W):
    out = build_core_cert(q, W)
    if out is None:
        return None
    F, coords_v, coords_ab, G, usedP = out
    d = F['d']
    gmap = {g[0]: g for g in G}
    cv = coords_v
    # ideal generators for cofactor bridging: recurrence (K=1) + minpoly
    rec = [cv[i] + cv[i+2] - LAM*cv[i+1] for i in range(W-1)]   # =0
    d2, rhs = field_relation(q)
    minp = LAM**d - sum(F['tail'][j]*LAM**(d-1-j) for j in range(d))
    ideal = rec + [minp]
    order = list(reversed(cv)) + [LAM]      # eliminate high coords first, then reduce lam
    L = []
    nm = f"case_q{q}"
    L.append(f"lemma {nm} ({' '.join(LETTERS[:W+1])} lam : ℝ) (hps : lam^{d2} = {rhs}) "
             f"(h2 : (1:ℝ) < lam) (h3 : lam < 2)")
    L.append("    " + " ".join(f"(hp{LETTERS[i]} : 0 < {LETTERS[i]})" for i in range(W+1)))
    L.append("    " + " ".join(f"(hc{LETTERS[i]} : {LETTERS[i]} ≤ 1)" for i in range(W+1)))
    L.append("    " + " ".join(f"(hr{i} : {LETTERS[i]}+lam*{LETTERS[i+1]} > 1)" for i in range(W)))
    L.append("    " + " ".join(f"(hg{i} : lam*{LETTERS[i]}+{LETTERS[i+1]} > 1)" for i in range(W)))
    L.append("    " + " ".join(f"(hk{i} : {LETTERS[i]}+{LETTERS[i+2]} = 1*lam*{LETTERS[i+1]})" for i in range(W-1)))
    L.append("    " + " ".join(f"(hf{i} : 1+{LETTERS[i]} < (1+1)*(lam*{LETTERS[i+1]}))" for i in range(W-1)))
    L.append("    " + " ".join(f"(hP{i} : {LETTERS[i]}*{LETTERS[i+1]} < 1/lam^3)" for i in range(W)) + " :")
    L.append("    False := by")
    L.append("  have hpos : (0:ℝ) < lam := by linarith")
    L.append("  have hp3 : (0:ℝ) < lam^3 := by positivity")
    # derive nonneg generator facts (named after gen names)
    for (name, ve, abe, src) in G:
        kind, idx = src
        if kind == 'pos':
            L.append(f"  have {name} : (0:ℝ) ≤ {LETTERS[idx]} := le_of_lt hp{LETTERS[idx]}")
        elif kind == 'cap':
            L.append(f"  have {name} : (0:ℝ) ≤ {lx(ve)} := by nlinarith [hc{LETTERS[idx]}]")
        elif kind == 'reg':
            L.append(f"  have {name} : (0:ℝ) ≤ {lx(ve)} := by nlinarith [hr{idx}]")
        elif kind == 'gen':
            L.append(f"  have {name} : (0:ℝ) ≤ {lx(ve)} := by nlinarith [hg{idx}]")
        elif kind == 'flu':
            L.append(f"  have {name} : (0:ℝ) ≤ {lx(ve)} := by nlinarith [hf{idx}]")
        elif kind == 'slk':
            co = f"{LETTERS[idx]}*{LETTERS[idx+1]}"
            L.append(f"  have {name} : (0:ℝ) ≤ {lx(ve)} := by")
            L.append(f"    have hh : ({co})*lam^3 < 1 := (lt_div_iff₀ hp3).mp hP{idx}")
            L.append(f"    nlinarith [hh]")
    # emit used products with cofactor bridge to ab-reduced form
    qnames = []
    for n, term in enumerate(usedP):
        key = term[0]
        kind = key[0]
        if kind in ('P', 'Pp'):
            i, j = key[1], key[2]
            gi, gj = G[i], G[j]
            vi, vj = gi[1], gj[1]
            raw = sp.expand((LAM*vi*vj) if kind == 'Pp' else (vi*vj))
            if kind == 'Pp':
                mn = f"mul_nonneg hpos.le (mul_nonneg {gi[0]} {gj[0]})"
                rawstr = f"lam*(({lx(vi)})*({lx(vj)}))"
            else:
                mn = f"mul_nonneg {gi[0]} {gj[0]}"
                rawstr = f"({lx(vi)})*({lx(vj)})"
        else:  # 'T' triple product g_i g_j g_k
            i, j, k = key[1], key[2], key[3]
            gi, gj, gk = G[i], G[j], G[k]
            vi, vj, vk = gi[1], gj[1], gk[1]
            raw = sp.expand(vi*vj*vk)
            mn = f"mul_nonneg (mul_nonneg {gi[0]} {gj[0]}) {gk[0]}"
            rawstr = f"(({lx(vi)})*({lx(vj)}))*({lx(vk)})"
        # reduce raw mod ideal -> red (canonical, in a,b, lam^<d) + cofactors
        quo, red = sp.reduced(raw, ideal, *order)
        red = sp.expand(red)
        terms = []
        for ig, gpoly in enumerate(ideal):
            if quo[ig] != 0:
                if ig < len(rec):
                    terms.append(f"({lx(quo[ig])})*hk{ig}")
                else:
                    terms.append(f"({lx(quo[ig])})*hps")
        lc = " + ".join(terms) if terms else "0"
        qn = f"qq{n}"; qnames.append(qn)
        L.append(f"  have {qn} : (0:ℝ) ≤ {lx(red)} := by")
        L.append(f"    have hr : (0:ℝ) ≤ {rawstr} := {mn}")
        L.append(f"    have he : {rawstr} = {lx(red)} := by linear_combination {lc}")
        L.append(f"    linarith [hr, he]")
    L.append(f"  linarith [{', '.join(qnames)}, h2, h3]")
    return "\n".join(L), nm

def emit_lam_lo(q):
    """g{q}_lam_lo : 9/5 < lam.  Unique-root q: from hps (synthetic division). Else: needs the
    analytic input cos(pi/q)>9/10 — emitted as an `axiom`-free lemma taking it as hypothesis is
    avoided; instead for multi-root q we emit a TODO marker handled by the caller."""
    d, g, negr = synth(q)
    d2, rhs = field_relation(q)
    L = []
    L.append(f"/-- `9/5 < lam_{q}` via synthetic division of the minpoly by `(t-9/5)`. -/")
    L.append(f"lemma g{q}_lam_lo (lam : ℝ) (hps : lam^{d2} = {rhs}) (h2 : (1:ℝ) < lam) (h3 : lam < 2) :")
    L.append(f"    (9:ℝ)/5 < lam := by")
    L.append(f"  have hg : (0:ℝ) < {g} := by nlinarith [h2, h3, sq_nonneg (lam-1), sq_nonneg (lam-2), sq_nonneg lam, pow_pos (show (0:ℝ)<lam by linarith) 3, pow_pos (show (0:ℝ)<lam by linarith) 5, pow_pos (show (0:ℝ)<lam by linarith) 7]")
    L.append(f"  have key : (lam - 9/5) * ({g}) = {negr} := by linear_combination hps")
    L.append(f"  nlinarith [key, hg]")
    return "\n".join(L)

def emit_floor_helper(q):
    L = []
    L.append(f"/-- Interior-floor contradiction (K>=2 impossible inside a sub-threshold window): if a")
    L.append(f"middle coord `m` has `lam^4 m^2 < 1` (= the K>=2 bound) and a neighbour `n` with `lam^4 n^2")
    L.append(f"< 2` and edge `1 - lam m < n`, then False.  Uses only `9/5 < lam < 2` via `(lam^2-lam)^2")
    L.append(f">= 2` — field-independent. -/")
    L.append(f"lemma g{q}_floor_helper (lam m n : ℝ) (h2 : (1:ℝ) < lam) (h3 : lam < 2)")
    L.append(f"    (hlo : (9:ℝ)/5 < lam) (hm : 0 < m) (hn : 0 < n)")
    L.append(f"    (hms : lam^4 * m^2 < 1) (hns : lam^4 * n^2 < 2) (hedge : 1 - lam*m < n) : False := by")
    L.append(f"  have hpos : (0:ℝ) < lam := by linarith")
    L.append(f"  have hl2 : (1:ℝ) < lam^2 := by nlinarith [h2]")
    L.append(f"  have hlm : lam^2 * m < 1 := by nlinarith [hms, mul_pos (mul_pos hpos hpos) hm, sq_nonneg (lam^2*m)]")
    L.append(f"  have hlm1 : lam*m < 1 := by nlinarith [hlm, hl2, hm, mul_pos hpos hm]")
    L.append(f"  have h1lm : (0:ℝ) < 1 - lam*m := by linarith")
    L.append(f"  have hnsq : (1 - lam*m)^2 < n^2 := by nlinarith [hedge, h1lm, hn]")
    L.append(f"  have hml : (36:ℝ)/25 ≤ lam^2 - lam := by nlinarith [mul_pos (show (0:ℝ)<lam-9/5 by linarith) (show (0:ℝ)<lam+4/5 by linarith)]")
    L.append(f"  have hKey : (2:ℝ) ≤ lam^4 - 2*lam^3 + lam^2 := by nlinarith [hml, sq_nonneg (lam^2-lam), mul_pos hpos (show (0:ℝ)<lam-1 by linarith)]")
    L.append(f"  have hA : lam^4 * (1 - lam*m)^2 < 2 := by nlinarith [hnsq, hns, mul_pos (mul_pos (mul_pos hpos hpos) hpos) hpos]")
    L.append(f"  nlinarith [hA, hKey, h1lm, hlm, hpos, hl2, mul_pos hpos h1lm, sq_nonneg (lam - lam^2*m), sq_nonneg (lam*(1-lam*m))]")
    return "\n".join(L)

def emit_core(q, W):
    d2, rhs = field_relation(q)
    uniq = q in UNIQUE_ROOT
    cs = LETTERS[:W+1]
    L = []
    L.append(f"/-- **q={q} window-{W} core.** {W+1} coords of a genuine scalar orbit (both Taha edges + cap")
    L.append(f"+ {W-1} integer floors K_i>=1 with recurrence and floor-upper) cannot have all {W} products")
    L.append(f"`< 1/lam^3`.  Each interior floor is forced to 1 (floor-helper), reducing to the single")
    L.append(f"Chebyshev case `case_q{q}`. -/")
    L.append(f"theorem g{q}_core ({' '.join(cs)} lam : ℝ) (hps : lam^{d2} = {rhs}) (h2 : (1:ℝ) < lam) (h3 : lam < 2)")
    if not uniq:
        L.append(f"    (hlo : (9:ℝ)/5 < lam)")
    L.append(f"    " + " ".join(f"(hp{cs[i]} : 0 < {cs[i]})" for i in range(W+1)))
    L.append(f"    " + " ".join(f"(hc{cs[i]} : {cs[i]} ≤ 1)" for i in range(W+1)))
    L.append(f"    " + " ".join(f"(hr{i} : {cs[i]}+lam*{cs[i+1]} > 1)" for i in range(W)))
    L.append(f"    " + " ".join(f"(hg{i} : lam*{cs[i]}+{cs[i+1]} > 1)" for i in range(W)))
    L.append(f"    ({' '.join('K'+str(i) for i in range(W-1))} : ℤ)")
    L.append(f"    " + " ".join(f"(hk{i} : {cs[i]}+{cs[i+2]} = (K{i}:ℝ)*lam*{cs[i+1]})" for i in range(W-1)))
    L.append(f"    " + " ".join(f"(hKge{i} : 1 ≤ K{i})" for i in range(W-1)))
    L.append(f"    " + " ".join(f"(hf{i} : 1+{cs[i]} < ((K{i}:ℝ)+1)*(lam*{cs[i+1]}))" for i in range(W-1)))
    L.append(f"    " + " ".join(f"(hP{i} : {cs[i]}*{cs[i+1]} < 1/lam^3)" for i in range(W)) + " :")
    L.append(f"    False := by")
    L.append(f"  have hpos : (0:ℝ) < lam := by linarith")
    if uniq:
        L.append(f"  have hlo : (9:ℝ)/5 < lam := g{q}_lam_lo lam hps h2 h3")
    L.append(f"  have hp3 : (0:ℝ) < lam^3 := by positivity")
    L.append(f"  have hp4nn : (0:ℝ) ≤ lam^4 := by positivity")
    for i in range(W):
        L.append(f"  have hP{i}c : {cs[i]}*{cs[i+1]}*lam^3 < 1 := (lt_div_iff₀ hp3).mp hP{i}")
    for i in range(W-1):
        L.append(f"  have hKr{i} : (1:ℝ) ≤ (K{i}:ℝ) := by exact_mod_cast hKge{i}")
        L.append(f"  have heng{i} : {cs[i]}*{cs[i+1]} + {cs[i+1]}*{cs[i+2]} = (K{i}:ℝ)*lam*{cs[i+1]}^2 := by linear_combination {cs[i+1]}*hk{i}")
        L.append(f"  have hK{i}b : (K{i}:ℝ)*lam^4*{cs[i+1]}^2 < 2 := by")
        L.append(f"    have h : ({cs[i]}*{cs[i+1]}+{cs[i+1]}*{cs[i+2]})*lam^3 = (K{i}:ℝ)*lam^4*{cs[i+1]}^2 := by linear_combination lam^3*heng{i}")
        L.append(f"    nlinarith [hP{i}c, hP{i+1}c, h]")
        L.append(f"  have hbU{i} : lam^4*{cs[i+1]}^2 < 2 := by")
        L.append(f"    have hn : (0:ℝ) ≤ lam^4*{cs[i+1]}^2 := mul_nonneg hp4nn (sq_nonneg _)")
        L.append(f"    nlinarith [hK{i}b, hKr{i}, mul_nonneg (by linarith : (0:ℝ) ≤ (K{i}:ℝ)-1) hn]")
    # prove each K_i <= 1
    for i in range(W-1):
        if i <= W-3:
            mname, nname = cs[i+1], cs[i+2]
            hns = f"hbU{i+1}"
            hedge = f"by linarith [hg{i+1}]"     # lam*coord_{i+1}+coord_{i+2}>1
        else:  # last floor
            mname, nname = cs[i+1], cs[i]
            hns = f"hbU{i-1}"                      # bounds coord_i = coord_{(i-1)+1}
            hedge = f"by linarith [hr{i}]"        # coord_i+lam*coord_{i+1}>1
        L.append(f"  have hKle{i} : K{i} ≤ 1 := by")
        L.append(f"    by_contra hcon; push_neg at hcon")
        L.append(f"    have h2K : (2:ℝ) ≤ (K{i}:ℝ) := by exact_mod_cast (by omega : (2:ℤ) ≤ K{i})")
        L.append(f"    have hn : (0:ℝ) ≤ lam^4*{cs[i+1]}^2 := mul_nonneg hp4nn (sq_nonneg _)")
        L.append(f"    have hms : lam^4*{mname}^2 < 1 := by nlinarith [hK{i}b, h2K, mul_nonneg (by linarith : (0:ℝ) ≤ (K{i}:ℝ)-2) hn]")
        L.append(f"    exact g{q}_floor_helper lam {mname} {nname} h2 h3 hlo hp{mname} hp{nname} hms {hns} ({hedge})")
    L.append(f"  interval_cases " + " <;> interval_cases ".join('K'+str(i) for i in range(W-1)) + " <;>")
    L.append(f"    push_cast at " + " ".join(f"hk{i} hf{i}" for i in range(W-1)) + " <;>")
    L.append(f"    exact case_q{q} {' '.join(cs)} lam hps h2 h3 "
             + " ".join(f"hp{cs[i]}" for i in range(W+1)) + " "
             + " ".join(f"hc{cs[i]}" for i in range(W+1)) + " "
             + " ".join(f"hr{i}" for i in range(W)) + " "
             + " ".join(f"hg{i}" for i in range(W)) + " "
             + " ".join(f"hk{i}" for i in range(W-1)) + " "
             + " ".join(f"hf{i}" for i in range(W-1)) + " "
             + " ".join(f"hP{i}" for i in range(W)))
    return "\n".join(L)

def emit_orbit(q, W):
    cs = LETTERS[:W+1]
    d2, rhs = field_relation(q)
    uniq = q in UNIQUE_ROOT
    L = []
    prod = " ∧\n            ".join(f"c (i+{i}) * c (i+{i+1}) < 1/lam^3" for i in range(W))
    L.append(f"/-- **q={q} window-{W}, orbit form.** Along any genuine scalar orbit (both Taha edges + cap +")
    L.append(f"genuine floor recurrence), no {W} consecutive products are all `< 1/lam^3`. -/")
    L.append(f"theorem g{q}_no_window_below_genuine")
    L.append(f"    (lam : ℝ) (hps : lam^{d2} = {rhs}) (h2 : (1:ℝ) < lam) (h3 : lam < 2)")
    if not uniq:
        L.append(f"    (hlo : (9:ℝ)/5 < lam)")
    L.append(f"    (c : ℕ → ℝ) (hposc : ∀ n, 0 < c n) (hcap : ∀ n, c n ≤ 1)")
    L.append(f"    (hreg : ∀ n, c n + lam * c (n+1) > 1) (hgen : ∀ n, lam * c n + c (n+1) > 1)")
    L.append(f"    (hrec : ∀ n, c n + c (n+2) = (⌊(1 + c n)/(lam*c (n+1))⌋ : ℝ)*lam*c (n+1)) :")
    L.append(f"    ∀ i, ¬ ({prod}) := by")
    L.append(f"  have hpos' : 0 < lam := by linarith")
    L.append(f"  intro i hcon")
    L.append(f"  obtain ⟨" + ", ".join(f"hh{i}" for i in range(W)) + "⟩ := hcon")
    L.append(f"  have flr : ∀ n, (1:ℤ) ≤ ⌊(1 + c n)/(lam*c (n+1))⌋ := by")
    L.append(f"    intro n")
    L.append(f"    have hden : 0 < lam*c (n+1) := mul_pos hpos' (hposc (n+1))")
    L.append(f"    have hsum : 0 < (⌊(1 + c n)/(lam*c (n+1))⌋ : ℝ)*lam*c (n+1) := by")
    L.append(f"      rw [← hrec n]; linarith [hposc n, hposc (n+2)]")
    L.append(f"    have h0' : (0:ℝ) < (⌊(1 + c n)/(lam*c (n+1))⌋ : ℝ) := by nlinarith [hsum, hden]")
    L.append(f"    have : (0:ℤ) < ⌊(1 + c n)/(lam*c (n+1))⌋ := by exact_mod_cast h0'")
    L.append(f"    omega")
    L.append(f"  have flrUB : ∀ n, 1 + c n < ((⌊(1 + c n)/(lam*c (n+1))⌋ : ℝ)+1)*(lam*c (n+1)) := by")
    L.append(f"    intro n")
    L.append(f"    have hden : 0 < lam*c (n+1) := mul_pos hpos' (hposc (n+1))")
    L.append(f"    have := Int.lt_floor_add_one ((1 + c n)/(lam*c (n+1)))")
    L.append(f"    rw [div_lt_iff₀ hden] at this")
    L.append(f"    linarith [this]")
    L.append(f"  exact g{q}_core " + " ".join(f"(c (i+{i}))" for i in range(W+1)) + " lam hps h2 h3"
             + ("" if uniq else " hlo"))
    L.append(f"    " + " ".join(f"(hposc (i+{i}))" for i in range(W+1)))
    L.append(f"    " + " ".join(f"(hcap (i+{i}))" for i in range(W+1)))
    L.append(f"    " + " ".join(f"(hreg (i+{i}))" for i in range(W)))
    L.append(f"    " + " ".join(f"(hgen (i+{i}))" for i in range(W)))
    L.append(f"    " + " ".join(f"(⌊(1 + c (i+{i}))/(lam*c (i+{i+1}))⌋)" for i in range(W-1)))
    L.append(f"    " + " ".join(f"(hrec (i+{i}))" for i in range(W-1)))
    L.append(f"    " + " ".join(f"(flr (i+{i}))" for i in range(W-1)))
    L.append(f"    " + " ".join(f"(flrUB (i+{i}))" for i in range(W-1)))
    L.append(f"    " + " ".join(f"hh{i}" for i in range(W)))
    return "\n".join(L)

def assemble(q):
    W = WINDOW[q]
    cres = emit_case(q, W)
    if cres is None:
        return None
    case_body, _ = cres
    parts = ["import Mathlib", "set_option maxHeartbeats 1600000", "noncomputable section",
             "open Int", ""]
    if q in UNIQUE_ROOT:
        parts.append(emit_lam_lo(q)); parts.append("")
    parts.append(emit_floor_helper(q)); parts.append("")
    parts.append(case_body); parts.append("")
    parts.append(emit_core(q, W)); parts.append("")
    parts.append(emit_orbit(q, W)); parts.append("")
    parts.append(f"#print axioms g{q}_floor_helper")
    parts.append(f"#print axioms case_q{q}")
    parts.append(f"#print axioms g{q}_core")
    parts.append(f"#print axioms g{q}_no_window_below_genuine")
    if q in UNIQUE_ROOT:
        parts.append(f"#print axioms g{q}_lam_lo")
    return "\n".join(parts)

if __name__ == '__main__':
    q = int(sys.argv[1])
    out = assemble(q)
    if out is None:
        print("-- CERT NOT FOUND for q", q); sys.exit(1)
    open(f'/tmp/lean-minus1/G{q}CORE.lean', 'w').write(out)
    print(f"written /tmp/lean-minus1/G{q}CORE.lean ({len(out.splitlines())} lines)")
