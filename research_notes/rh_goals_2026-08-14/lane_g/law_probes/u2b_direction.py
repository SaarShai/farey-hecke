"""u2b_direction.py -- N_q(L) vs N_theta(L), signed syllables."""
import json, math, itertools
OUT={"probe":"u2b_direction"}
# --- Part 2: direction check with negative syllables (matches the note's N_theta)
def u(j, lam):
    th = math.acos(min(1.0, max(-1.0, lam/2.0)))
    return float(j) if th < 1e-14 else math.sin(j*th)/math.sin(th)
def trace(w, lam, amax):
    uu = {j: u(j, lam) for j in range(0, amax+2)}
    P = ((1.0, 0.0), (0.0, 1.0))
    for a in w:
        aa = abs(a)
        B = ((uu[aa], uu[aa+1]), (uu[aa-1], uu[aa])) if a > 0 else ((uu[aa], uu[aa-1]), (uu[aa+1], uu[aa]))
        P = ((P[0][0]*B[0][0]+P[0][1]*B[1][0], P[0][0]*B[0][1]+P[0][1]*B[1][1]),
             (P[1][0]*B[0][0]+P[1][1]*B[1][0], P[1][0]*B[0][1]+P[1][1]*B[1][1]))
    return abs(P[0][0]+P[1][1])
def count_theta(L, mmax, amax):
    n = 0
    alpha = [a for a in range(-amax, amax+1) if a != 0]
    for m in range(1, mmax+1):
        for w in itertools.product(alpha, repeat=m):
            rots = [w[i:]+w[:i] for i in range(m)]
            if w != min(rots) or len(set(rots)) != m: continue
            t = trace(w, 2.0, amax)
            if t > 2+1e-9 and 2*math.acosh(t/2) <= L+1e-9: n += 1
    return n
def count_q(q, L, mmax):
    n = 0
    for m in range(1, mmax+1):
        for w in itertools.product(range(1, q), repeat=m):
            rots = [w[i:]+w[:i] for i in range(m)]
            if w != min(rots) or len(set(rots)) != m: continue
            t = trace(w, 2*math.cos(math.pi/q), q)
            if t > 2+1e-9 and 2*math.acosh(t/2) <= L+1e-9: n += 1
    return n
rows = []
for L in (4.0, 5.0, 6.0):
    nth = count_theta(L, 4, 8)
    for q in (8, 10, 12, 16, 22, 30, 50):
        rows.append({"L": L, "q": q, "N_q": count_q(q, L, 4), "N_theta": nth})
OUT["direction_signed"] = {"rows": rows,
    "all_N_q_ge_N_theta": all(r["N_q"] >= r["N_theta"] for r in rows)}


print(json.dumps(OUT["direction_signed"], indent=1))
json.dump(OUT, open("u2b_direction.json","w"), indent=1)
