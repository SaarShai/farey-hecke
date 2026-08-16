"""u2b_normal_form.py  (lane_g / U2b)  -- the nonnegative normal form.

Claim NF. Let lam be an indeterminate, S = [[0,-1],[1,0]], R = [[0,-1],[1,lam]],
and u_j in Z[lam] the Chebyshev-like sequence u_0 = 0, u_1 = 1,
u_{j+1} = lam*u_j - u_{j-1}   (so u_j(2cos(pi/q)) = sin(j pi/q)/sin(pi/q)).
Then, as an identity in the matrix ring over Z[lam],

    S R^a  = - M_a ,      S R^{-a} = + M_a^T ,
    M_a := [[u_a, u_{a+1}], [u_{a-1}, u_a]],       det M_a = 1.

At lam = lam_q = 2cos(pi/q) and 1 <= a <= q-1 every entry of M_a is >= 0,
M_1 = [[1,lam],[0,1]] and M_{q-1} = [[1,0],[lam,1]], and u_a >= lam for
2 <= a <= q-2 ("heavy" letters) while u_1 = u_{q-1} = 1 ("light" letters).

Exact part: integer-coefficient polynomial arithmetic, no floats.
"""
import json, math, sys

# ---- minimal Z[lam] polynomial arithmetic: poly = tuple of int coeffs, low->high
def padd(p, q):
    n = max(len(p), len(q)); return tuple((p[i] if i < len(p) else 0) + (q[i] if i < len(q) else 0) for i in range(n))
def pneg(p): return tuple(-c for c in p)
def pmul(p, q):
    if not p or not q: return (0,)
    r = [0]*(len(p)+len(q)-1)
    for i, a in enumerate(p):
        if a:
            for j, b in enumerate(q): r[i+j] += a*b
    return tuple(r)
def ptrim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0: p.pop()
    return tuple(p)
def peq(p, q): return ptrim(p) == ptrim(q)
ZERO, ONE, LAM = (0,), (1,), (0, 1)

def mmul(A, B):
    return [[padd(pmul(A[0][0],B[0][0]), pmul(A[0][1],B[1][0])), padd(pmul(A[0][0],B[0][1]), pmul(A[0][1],B[1][1]))],
            [padd(pmul(A[1][0],B[0][0]), pmul(A[1][1],B[1][0])), padd(pmul(A[1][0],B[0][1]), pmul(A[1][1],B[1][1]))]]
def mneg(A): return [[pneg(A[0][0]), pneg(A[0][1])],[pneg(A[1][0]), pneg(A[1][1])]]
def mT(A): return [[A[0][0], A[1][0]],[A[0][1], A[1][1]]]
def meq(A, B): return all(peq(A[i][j], B[i][j]) for i in range(2) for j in range(2))
def mdet(A): return padd(pmul(A[0][0],A[1][1]), pneg(pmul(A[0][1],A[1][0])))

def u(j):
    a, b = ZERO, ONE
    if j == 0: return ZERO
    for _ in range(j-1): a, b = b, padd(pmul(LAM, b), pneg(a))
    return b

S    = [[ZERO, (-1,)], [ONE, ZERO]]
R    = [[ZERO, (-1,)], [ONE, LAM]]
Rinv = [[LAM, ONE], [(-1,), ZERO]]          # R^{-1}, det R = 1

OUT = {"claim": "S R^a = -M_a, S R^-a = M_a^T, det M_a = 1, exact in Z[lam]"}
rows, ok_all = [], True
P, Pinv = [[ONE,ZERO],[ZERO,ONE]], [[ONE,ZERO],[ZERO,ONE]]
for a in range(1, 26):
    P, Pinv = mmul(P, R), mmul(Pinv, Rinv)
    lhs, lhs_inv = mmul(S, P), mmul(S, Pinv)
    Ma = [[u(a), u(a+1)],[u(a-1), u(a)]]
    r = {"a": a,
         "SRa_eq_negMa":  meq(lhs, mneg(Ma)),
         "SRnega_eq_MaT": meq(lhs_inv, mT(Ma)),
         "detMa_eq_1":    peq(mdet(Ma), ONE)}
    ok_all &= r["SRa_eq_negMa"] and r["SRnega_eq_MaT"] and r["detMa_eq_1"]
    rows.append(r)
OUT["exact_identity"] = {"all_ok": bool(ok_all), "a_range": "1..25", "rows": rows[:5]}

# ---- numeric facts at lam = lam_q
num = {"all_nonneg": True, "M1_M q-1_shape": True, "heavy_u_ge_lam": True,
       "light_u_eq_1": True, "min_entry": 1e9}
for q in range(4, 401):
    L  = 2*math.cos(math.pi/q); s = math.sin(math.pi/q)
    uu = [math.sin(j*math.pi/q)/s for j in range(q+2)]
    for a in range(1, q):
        m = min(uu[a-1], uu[a], uu[a+1])
        num["min_entry"] = min(num["min_entry"], m)
        if m < -1e-12: num["all_nonneg"] = False
        if a in (1, q-1) and abs(uu[a]-1) > 1e-10: num["light_u_eq_1"] = False
    if not (abs(uu[1]-1) < 1e-11 and abs(uu[2]-L) < 1e-11 and abs(uu[0]) < 1e-14): num["M1_M q-1_shape"] = False
    if not (abs(uu[q-1]-1) < 1e-10 and abs(uu[q]) < 1e-10 and abs(uu[q-2]-L) < 1e-10): num["M1_M q-1_shape"] = False
    if q >= 5 and any(uu[a] < L - 1e-11 for a in range(2, q-1)): num["heavy_u_ge_lam"] = False
OUT["numeric_q_4_to_400"] = num
print(json.dumps(OUT, indent=1))
json.dump(OUT, open(sys.argv[1] if len(sys.argv) > 1 else "u2b_normal_form.json", "w"), indent=1)
