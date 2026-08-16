"""u2b_monotone.py (lane_g / U2b-b) -- trace monotonicity, corrected.

THEOREM U2b-B. g(t) := t cot t is strictly decreasing on (0, pi); hence for
lam = 2 cos(theta), u_j(lam) = sin(j theta)/sin(theta) is strictly INCREASING
in lam on theta in (0, pi/j), i.e. on lam in (2 cos(pi/j), 2], where it is >= 0.
Consequently, for a cyclically reduced word with A := max_i |a_i|, |tr w(lam)|
is a sum of products of u_j, j <= A+1, hence nondecreasing in lam on
[2 cos(pi/(A+1)), 2]  ==  exactly the levels q >= A+1 at which w is a
normal-form word.  In particular |tr_w(lam_q)| <= |tr_w(2)|.

COUNTEREXAMPLE to the literal Conjecture U1-2 ("nondecreasing on (1,2]"):
u_5 and hence |tr(S R^5)| = 2 u_5 is NOT monotone on (1,2].

DIRECTION CHECK: the note infers N_q(L) <= N_theta(L) from l_w(lam_q) <=
l_w(2). That inference is backwards; measured here.
"""
import json, math, itertools

OUT = {"probe": "u2b_monotone"}

# --- (1) g(t) = t cot t strictly decreasing on (0,pi)
xs = [1e-6 + i*(math.pi-2e-6)/200000 for i in range(200001)]
g = [x*math.cos(x)/math.sin(x) for x in xs]
OUT["g_tcot_decreasing"] = {"monotone": all(g[i+1] < g[i] + 1e-15 for i in range(len(g)-1)),
                            "n_samples": len(xs), "g(0+)": g[0], "g(pi-)": g[-1]}

# --- (2) u_j increasing in lam exactly on (2cos(pi/j), 2]
def u(j, lam):
    th = math.acos(lam/2.0)
    return j if th < 1e-14 else math.sin(j*th)/math.sin(th)
rows = []
ok = True
for j in range(2, 26):
    lo = 2*math.cos(math.pi/j)
    grid = [lo + (2.0-lo)*i/4000 for i in range(4001)]
    v = [u(j, x) for x in grid]
    inc = all(v[i+1] >= v[i] - 1e-11 for i in range(len(v)-1))
    nonneg = min(v) >= -1e-11
    ok &= inc and nonneg
    rows.append({"j": j, "lam_lo=2cos(pi/j)": lo, "increasing_on_[lo,2]": inc, "min_u": min(v)})
OUT["u_j_increasing_on_its_interval"] = {"all_ok": ok, "j_range": "2..25", "rows": rows[:4]}

# --- (3) counterexample to the literal (1,2] claim
pts = [1.0, 1.1, 1.2434, 1.35, math.sqrt(2), 1.5, 2*math.cos(math.pi/5), 1.75, math.sqrt(3), 1.95, 2.0]
tab = [{"lam": round(x, 6), "u_5": round(u(5, x), 6), "|tr(SR^5)|": round(2*abs(u(5, x)), 6)} for x in pts]
OUT["counterexample_literal_U1_2"] = {
    "word": "S R^5  (single syllable a=5, legitimate normal form for every q >= 6)",
    "table": tab,
    "monotone_on_(1,2]": all(abs(tab[i+1]["u_5"]) >= abs(tab[i]["u_5"]) - 1e-12 for i in range(len(tab)-1)),
    "note": "|tr| rises to ~2.50 at lam=1.2434, falls to 0 at lam=lam_5, then rises to 10 at lam=2"}

# --- (4) monotonicity holds on the CORRECT interval, tested on many words
viol = 0; tested = 0
for A in range(1, 9):
    for m in range(1, 5):
        for w in itertools.product(range(1, A+1), repeat=m):
            if max(w) != A: continue
            rots = [w[i:]+w[:i] for i in range(m)]
            if w != min(rots) or len(set(rots)) != m: continue
            lo = 2*math.cos(math.pi/(A+1))
            prev = None
            for i in range(401):
                lam = lo + (2.0-lo)*i/400
                uu = {j: u(j, lam) for j in range(0, A+2)}
                P = ((1.0, 0.0), (0.0, 1.0))
                for a in w:
                    B = ((uu[a], uu[a+1]), (uu[a-1], uu[a]))
                    P = ((P[0][0]*B[0][0]+P[0][1]*B[1][0], P[0][0]*B[0][1]+P[0][1]*B[1][1]),
                         (P[1][0]*B[0][0]+P[1][1]*B[1][0], P[1][0]*B[0][1]+P[1][1]*B[1][1]))
                t = abs(P[0][0]+P[1][1])
                if prev is not None and t < prev - 1e-9: viol += 1
                prev = t
            tested += 1
OUT["monotone_on_correct_interval"] = {"words_tested": tested, "violations": viol}

# --- (5) direction check N_q(L) vs N_theta(L)
def count(lam, L, mmax, amax):
    n = 0
    for m in range(1, mmax+1):
        for w in itertools.product(range(1, amax+1), repeat=m):
            rots = [w[i:]+w[:i] for i in range(m)]
            if w != min(rots) or len(set(rots)) != m: continue
            uu = {j: u(j, lam) for j in range(0, amax+2)}
            P = ((1.0, 0.0), (0.0, 1.0))
            for a in w:
                B = ((uu[a], uu[a+1]), (uu[a-1], uu[a]))
                P = ((P[0][0]*B[0][0]+P[0][1]*B[1][0], P[0][0]*B[0][1]+P[0][1]*B[1][1]),
                     (P[1][0]*B[0][0]+P[1][1]*B[1][0], P[1][0]*B[0][1]+P[1][1]*B[1][1]))
            t = abs(P[0][0]+P[1][1])
            if t > 2 + 1e-9 and 2*math.acosh(t/2) <= L + 1e-9: n += 1
    return n
dir_rows = []
for L in (4.0, 5.0):
    nth = count(2.0, L, 4, 12)      # Gamma_theta: syllables 1..12, m<=4
    for q in (8, 10, 12, 16, 22, 30, 50):
        nq = count(2*math.cos(math.pi/q), L, 4, q-1)
        dir_rows.append({"L": L, "q": q, "N_q": nq, "N_theta": nth, "N_q>=N_theta": nq >= nth})
OUT["direction_check"] = {"rows": dir_rows,
    "all_N_q_ge_N_theta": all(r["N_q>=N_theta"] for r in dir_rows),
    "claim": "N_q(L) >= N_theta(L); the note's N_q <= N_theta inference is backwards"}

print(json.dumps({k: (v if k != "u_j_increasing_on_its_interval" else v["all_ok"]) for k, v in OUT.items()
                  if k not in ("counterexample_literal_U1_2",)}, indent=1)[:2500])
print("counterexample table:", json.dumps(OUT["counterexample_literal_U1_2"]["table"]))
json.dump(OUT, open("u2b_monotone.json", "w"), indent=1)
