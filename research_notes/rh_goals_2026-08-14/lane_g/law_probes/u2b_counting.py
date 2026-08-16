"""u2b_counting.py (lane_g / U2b-b) -- the q-uniform geodesic counting bound.

PROPOSITION U2b-C.  For every hyperbolic cyclically reduced w at level q,
    |tr w| >= A(w) := 2 * prod_{heavy i} u_{a_i}          (both diagonal paths)
    |tr w| >= B(w) := lam^k * prod_{j=1..k} p_j           (alternating path)
where heavy = {2..q-2}, light = {1, q-1}, and p_1..p_k are the lengths of the
maximal light runs.  Hence |tr w| >= A^th * B^(1-th) for every th in [0,1], and
with e_h := 2*sig*th, e_l := 2*sig*(1-th),

  Sum_{[gam] prim} |tr|^{-2 sig} <= 2^{-e_h} * sum_{n>=1} (1/n) W_q^n
                                  = 2^{-e_h} * log( 1/(1-W_q) ),
  W_q(e_h,e_l) := sum_{a=2}^{q-2} u_a^{-e_h} + 2 * lam^{-e_l} * zeta(e_l).

This is q-uniform as soon as sup_{q>=5} W_q < 1.  This probe finds the minimal
sigma_0 = (e_h+e_l)/2 for which that holds, and the resulting bound on
S_q(sigma) = sum e^{-sig l}/(1-e^{-l}).

Part 2: corrected direction check N_q(L) vs N_theta(L) WITH negative syllables.
"""
import json, math, itertools

_ZC = {}
def zeta(s, N=20000):
    if s in _ZC: return _ZC[s]
    # Euler-Maclaurin tail for Re s > 1
    tot = sum(k**-s for k in range(1, N))
    tot += N**(1-s)/(s-1) + 0.5*N**-s + s*N**(-s-1)/12.0
    _ZC[s] = tot
    return tot

_UT = {}
def utab(q):
    if q not in _UT:
        s = math.sin(math.pi/q)
        _UT[q] = [math.sin(a*math.pi/q)/s for a in range(2, q-1)]
    return _UT[q]
def W(q, e_h, e_l):
    lam = 2*math.cos(math.pi/q)
    h = sum(v**-e_h for v in utab(q))
    return h + 2*(lam**-e_l)*zeta(e_l)

OUT = {"probe": "u2b_counting"}
QS = list(range(5, 41)) + [50, 60, 80, 120, 200, 400, 1000, 3000]

# --- scan for the minimal sigma_0
grid = []
best = None
for e_h in [x/20 for x in range(40, 121)]:      # 2.00 .. 6.00
    for e_l in [x/20 for x in range(40, 121)]:
        sig = (e_h+e_l)/2
        if best is not None and sig >= best[0]: continue
        sup = max(W(q, e_h, e_l) for q in QS)
        if sup < 1.0:
            best = (sig, e_h, e_l, sup)
OUT["optimal"] = {"sigma_0": best[0], "e_h": best[1], "e_l": best[2],
                  "sup_q W": best[3], "q_grid": f"{QS[0]}..{QS[-1]} ({len(QS)} values)"}

# --- table at a few working choices
tab = []
for (e_h, e_l) in [(best[1], best[2]), (3.0, 4.0), (4.0, 4.0), (3.0, 3.5), (2.5, 3.5), (1.5, 1.5)]:
    ws = {q: W(q, e_h, e_l) for q in QS}
    argmax = max(ws, key=lambda k: ws[k])
    sup = ws[argmax]
    tab.append({"e_h": e_h, "e_l": e_l, "sigma": (e_h+e_l)/2, "sup_q W": sup,
                "argmax_q": argmax, "usable": sup < 1.0,
                "bound_sum_|tr|^-2sig": (2**-e_h)*math.log(1/(1-sup)) if sup < 1 else None})
OUT["table"] = tab

# --- resulting S_q(sigma) bound, with the sharp trace->length constant
# For |tr| = t >= 2 lam_5, e^{l/2} = (t + sqrt(t^2-4))/2 = c(t) * t with
# c(t) = (1+sqrt(1-4/t^2))/2 increasing, so c >= c(2 lam_5) = 0.89316...
lam5 = 2*math.cos(math.pi/5); t0 = 2*lam5
c0   = (1 + math.sqrt(1 - 4/t0**2))/2
sys5 = 2*math.acosh(lam5)
asm = []
for (e_h, e_l) in [(best[1], best[2]), (3.0, 3.5), (3.0, 4.0), (4.0, 4.0)]:
    sig = (e_h+e_l)/2
    sup = max(W(q, e_h, e_l) for q in QS)
    if sup >= 1: continue
    sum_tr = (2**-e_h)*math.log(1/(1-sup))
    S_bound = (c0**(-2*sig)) * sum_tr / (1 - math.exp(-sys5))
    asm.append({"e_h": e_h, "e_l": e_l, "sigma": sig, "sup_q W": sup,
                "sum |tr|^{-2sig} <=": sum_tr,
                "S_q(sigma) <=": S_bound})
OUT["assembled"] = {"sys(G_5)": sys5, "c0": c0,
                    "1/(1-e^-sys5)": 1/(1-math.exp(-sys5)), "rows": asm}

print(json.dumps(OUT, indent=1))
json.dump(OUT, open("u2b_counting.json", "w"), indent=1)
