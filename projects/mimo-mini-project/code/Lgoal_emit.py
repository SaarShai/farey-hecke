#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GOAL L, Objective A: GENERAL per-q scalar window-lemma emitter (q in 7..16).
Generalises emit5.py/build_core.py beyond the quadratic fields phi (q=5), lam^2=3 (q=6) to
ARBITRARY q: minpoly of lam=2cos(pi/q) of degree d, power-basis reduction, single (1,..,1)
Positivstellensatz core case (Kmax=1 for q>=7: every INTERIOR floor in a full W-window is forced
to 1) + a floor-helper infeasibility cert (also Positivstellensatz, no tight-lam bounds needed:
the LP residual is a NEGATIVE RATIONAL so `linarith` closes it from hps + 1<lam<2 alone).

W(q): 4 for q<=12, 5 for q in 13..16  (from code/Kgoal_exact_run_q6_16.py; max sub-thr run = W-1).

Outputs a SELF-CONTAINED Lean file proving:
  - lam-power field relation `hps : lam^d = <tail>`,
  - g{q}_floor_helper : K>=2 contradiction (interior floor forced to 1),
  - g{q}_core         : W+1 coords, both Taha edges, cap, W-1 recurrences (K_j:Z>=1 + floor-upper),
                        all W products < 1/lam^3  ==>  False,
  - g{q}_no_window_below_genuine : orbit form (the hWin input of the window engine).
The measure-theoretic capstone (window engine + X_q = 1/lam^3) is wired separately per q.
"""
import sympy as sp
from sympy import cos, pi, Rational, minimal_polynomial
from itertools import combinations_with_replacement
import numpy as np
from scipy.optimize import linprog

LAM = sp.symbols('lam')

# ---------------------------------------------------------------- field algebra
def field(q):
    lam = 2*cos(pi/q); t = sp.symbols('t')
    m = sp.Poly(minimal_polynomial(lam, t), t); d = m.degree()
    mc = m.all_coeffs(); lead = mc[0]
    mm = [Rational(c, lead) for c in mc]            # monic, leading first
    tail = [-mm[i] for i in range(1, d+1)]          # lam^d = sum tail[j] lam^{d-1-j}
    # reduction table lam^k -> vector over {1,lam,...,lam^{d-1}}
    pb = {k: [Rational(1) if i == k else Rational(0) for i in range(d)] for k in range(d)}
    def shift(v):
        out = [Rational(0)]*d
        for k in range(d-1):
            out[k+1] += v[k]
        top = v[d-1]
        for j in range(d):
            out[d-1-j] += top*tail[j]
        return out
    def vecpow(k):
        if k in pb:
            return pb[k]
        pb[k] = shift(vecpow(k-1)); return pb[k]
    lamf = float((2*sp.cos(sp.pi/q)).evalf(50))
    minpoly_lam = LAM**d - sum(tail[j]*LAM**(d-1-j) for j in range(d))
    return dict(q=q, d=d, tail=tail, lamf=lamf, minpoly=sp.expand(minpoly_lam),
                vecpow=vecpow)

def redp(expr, F):
    """Reduce a polynomial in LAM (coeffs may contain a,b,...) to power basis deg<d."""
    d = F['d']; vecpow = F['vecpow']
    p = sp.Poly(sp.expand(expr), LAM)
    out = sp.Integer(0)
    for (k,), co in p.terms():
        v = vecpow(k)
        out += co*sum(v[i]*LAM**i for i in range(d))
    return sp.expand(out)

def comps(expr, F, V):
    """Split reduced expr into the d power-basis components, each a poly in V."""
    d = F['d']; e = redp(expr, F); p = sp.Poly(e, LAM)
    out = {}
    for w in range(d):
        part = sp.expand(p.coeff_monomial(LAM**w) if w > 0 else p.coeff_monomial(1))
        if part == 0:
            continue
        for mono, co in sp.Poly(part, *V).terms():
            out.setdefault(mono, [sp.Integer(0)]*d)
            out[mono][w] += co
    return out

# ---------------------------------------------------------------- generic LP cert
def lp_cert(F, V, gens, eqs, eq_monos, deg3=False):
    """
    gens : list of (lean_hyp_name, expr>=0)  -- nonneg generators (reduced over field)
    eqs  : list of (lean_hyp_name, expr==0)  -- equality constraints (recurrences)
    eq_monos : monomials to multiply each eq by (free-sign multipliers)
    deg3 : if True, also include triple products g_i g_j g_k (Handelman degree 3).
    Returns (usedP, usedF) or None.  Cert = sum nonneg*(products) + free*eqs == neg rational.
    """
    d = F['d']; lamf = F['lamf']
    terms = []
    for i, j in combinations_with_replacement(range(len(gens)), 2):
        ex = redp(gens[i][1]*gens[j][1], F)
        terms.append((('P', i, j), ex))
        terms.append((('Pp', i, j), redp(LAM*ex, F)))   # *lam (still nonneg since lam>0)
    if deg3:
        for i, j, k in combinations_with_replacement(range(len(gens)), 3):
            ex = redp(gens[i][1]*gens[j][1]*gens[k][1], F)
            terms.append((('T', i, j, k), ex))
    nNon = len(terms)
    free = []
    for (en, ee) in eqs:
        for mono in eq_monos:
            free.append((('E', en, str(mono)), redp(ee*mono, F)))
            free.append((('Ep', en, str(mono)), redp(LAM*ee*mono, F)))
    allt = terms + free
    sp_ = [comps(ex, F, V) for _, ex in allt]
    mset = set()
    for s in sp_:
        mset |= set(s.keys())
    ml = sorted(mset, key=lambda m: (sum(m), m)); mi = {m: i for i, m in enumerate(ml)}; M = len(ml)
    const = tuple([0]*len(V))
    A = sp.zeros(d*M, len(allt))
    for k, s in enumerate(sp_):
        for mono, vec in s.items():
            for w in range(d):
                A[d*mi[mono]+w, k] = vec[w]
    # rows that must vanish: every (mono, w) EXCEPT (const, w=0)
    keeprow = d*mi[const] + 0
    nc = [r for r in range(d*M) if r != keeprow]
    ns = A[nc, :].nullspace()
    if not ns:
        return None
    Nb = sp.Matrix.hstack(*ns); dim = Nb.shape[1]
    cr = A[keeprow, :]                     # the surviving constant-row -> want it NEGATIVE
    cfun = [(cr*Nb)[k] for k in range(dim)]
    Lf = np.array(Nb.tolist(), dtype=float); cf = np.array([float(x) for x in cfun])
    # find nonneg combo (first nNon coords >=0) with constant residual <= -1
    Aub = np.vstack([-Lf[:nNon], cf.reshape(1, -1)]); bub = np.concatenate([np.zeros(nNon), [-1.0]])
    res = linprog(c=Lf[:nNon].sum(axis=0), A_ub=Aub, b_ub=bub,
                  bounds=[(None, None)]*dim, method='highs')
    if not res.success:
        return None
    x = Lf@res.x
    usedP = [(terms[k][0], terms[k][1]) for k in range(nNon) if x[k] > 1e-7]
    usedF = [allt[k][0] for k in range(nNon, len(allt)) if abs(x[k]) > 1e-7]
    return (usedP, gens, eqs, usedF)

def lx(ex):
    return str(sp.expand(ex)).replace('**', '^')

# ---------------------------------------------------------------- emit helpers
def hps_decl(F):
    d = F['d']
    rhs = sum(F['tail'][j]*LAM**(d-1-j) for j in range(d))
    return f"lam^{d} = {lx(rhs)}"

if __name__ == '__main__':
    # smoke test: print field data and a floor-helper cert search for q=7
    import sys
    q = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    F = field(q)
    print(f"q={q} d={F['d']}  hps: {hps_decl(F)}")
    print(f"  lam^3 -> {lx(redp(LAM**3, F))}")
    print(f"  lam^4 -> {lx(redp(LAM**4, F))}")
    # floor helper cert: vars m,n ; generators
    m, n = sp.symbols('m n'); Vf = [m, n]
    gens = [('hm', m), ('hn', n),
            ('hms', 1 - LAM**4*m**2),          # K>=2 => lam^4 m^2 < 1
            ('hns', 2 - LAM**4*n**2),          # lam^4 n^2 < 2
            ('hedge', n - (1 - LAM*m)),        # gen edge 1-lam m < n
            ('hlam1', LAM - 1)]                # 1 < lam
    r = lp_cert(F, Vf, gens, [], [])
    print("  floor-helper cert:", "FOUND" if r else "none",
          ([(t[0]) for t in r[0]] if r else ""))
