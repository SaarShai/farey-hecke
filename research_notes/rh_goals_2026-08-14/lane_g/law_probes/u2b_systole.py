"""u2b_systole.py (lane_g / U2b-a) -- exhaustive check of the systole theorem
and of the two path bounds that prove it.

THEOREM U2b-A (proved in LAW_U2B_CLOSURE.md Sec.2). For q >= 4 and every
cyclically reduced w = S R^{a_1} ... S R^{a_m} (a_i in {1..q-1}) that is
hyperbolic,  |tr w| >= 2 lam_q,  with equality iff m = 1 and a in {2, q-2}.
Hence sys(G_q) = 2 arccosh(lam_q), realised exactly by [S R^2] / [S R^{q-2}].
For q = 3 the heavy alphabet is empty and the minimum is 2 + lam^2 = 3.

Checks per q, over ALL cyclically reduced words with m <= MMAX:
 (C1) min |tr| over hyperbolic words == 2 lam_q      (q >= 4)
 (C2) diagonal-path bound   |tr w| >= 2 * prod_i u_{a_i}
 (C3) light-only mixed words satisfy |tr w| >= 2 + lam^2
 (C4) argmin set == {(2,), (q-2,)}
 (C5) counting bound  |tr w|^2 >= A(w) * B(w),
        A = 2 * prod_{heavy i} u_{a_i},  B = lam^k * prod_j p_j
        (k = number of maximal light runs, p_j their lengths)
"""
import json, math, sys, itertools

def run(q, MMAX):
    L = 2*math.cos(math.pi/q); s = math.sin(math.pi/q)
    uu = [math.sin(j*math.pi/q)/s for j in range(q+2)]
    M = {a: ((uu[a], uu[a+1]), (uu[a-1], uu[a])) for a in range(1, q)}
    heavy = set(range(2, q-1)); light = {1, q-1}
    res = {"q": q, "lam": L, "two_lam": 2*L, "MMAX": MMAX,
           "C2_ok": True, "C3_ok": True, "C5_ok": True,
           "min_hyp_tr": None, "argmin": [], "n_words": 0, "n_hyp": 0}
    best = float('inf'); arg = []
    seen = set()
    for m in range(1, MMAX+1):
        for w in itertools.product(range(1, q), repeat=m):
            # keep one representative per cyclic class, primitive only
            rots = [w[i:]+w[:i] for i in range(m)]
            if w != min(rots): continue
            if len(set(rots)) != m: continue           # non-primitive cyclic word
            res["n_words"] += 1
            P = ((1.0, 0.0), (0.0, 1.0))
            for a in w:
                A_, B_ = P, M[a]
                P = ((A_[0][0]*B_[0][0]+A_[0][1]*B_[1][0], A_[0][0]*B_[0][1]+A_[0][1]*B_[1][1]),
                     (A_[1][0]*B_[0][0]+A_[1][1]*B_[1][0], A_[1][0]*B_[0][1]+A_[1][1]*B_[1][1]))
            tr = P[0][0] + P[1][1]
            prod_u = 1.0
            for a in w: prod_u *= uu[a]
            if tr < 2*prod_u - 1e-9: res["C2_ok"] = False
            if all(a in light for a in w) and len(set(w)) > 1:
                if tr < 2 + L*L - 1e-9: res["C3_ok"] = False
            # A and B
            A_h = 2.0
            for a in w:
                if a in heavy: A_h *= uu[a]
            runs, i = [], 0
            ws = list(w)
            if all(a in light for a in ws):
                runs = []
                # single cyclic run per letter type
                cur = None; cnt = 0; tmp = []
                for a in ws + [None]:
                    if a is not None and a in light and a == cur: cnt += 1
                    else:
                        if cur is not None and cur in light: tmp.append(cnt)
                        cur = a; cnt = 1
                # cyclic merge
                if len(tmp) > 1 and ws[0] == ws[-1]:
                    tmp[0] += tmp[-1]; tmp.pop()
                runs = tmp
            else:
                # rotate so position 0 is heavy, then scan
                st = next(i for i, a in enumerate(ws) if a in heavy)
                rot = ws[st:] + ws[:st]
                cur = None; cnt = 0
                for a in rot + [None]:
                    if a is not None and a in light and a == cur: cnt += 1
                    else:
                        if cur is not None and cur in light: runs.append(cnt)
                        cur = a; cnt = 1
            B_l = L**len(runs)
            for p in runs: B_l *= p
            if tr*tr < A_h*B_l - 1e-7: res["C5_ok"] = False
            if tr > 2 + 1e-9:
                res["n_hyp"] += 1
                if tr < best - 1e-9: best, arg = tr, [w]
                elif abs(tr-best) < 1e-9 and len(arg) < 6: arg.append(w)
    res["min_hyp_tr"] = best; res["argmin"] = [list(a) for a in arg]
    res["C1_ok"] = abs(best - 2*L) < 1e-8 if q >= 4 else None
    res["C4_ok"] = sorted(res["argmin"]) == sorted([[2],[q-2]]) if q >= 5 else None
    return res

if __name__ == "__main__":
    plan = [(3,7),(4,7),(5,7),(6,6),(7,6),(8,6),(9,5),(10,5),(11,5),(12,5),
            (14,5),(16,4),(20,4),(24,4),(30,4),(40,4),(60,3),(100,3)]
    out = {"probe": "u2b_systole", "rows": []}
    for q, mm in plan:
        r = run(q, mm); out["rows"].append(r)
        print(f"q={q:4d} MMAX={mm} min|tr|={r['min_hyp_tr']:.9f} 2lam={2*math.cos(math.pi/q):.9f} "
              f"argmin={r['argmin']} C1={r['C1_ok']} C2={r['C2_ok']} C3={r['C3_ok']} "
              f"C4={r['C4_ok']} C5={r['C5_ok']} words={r['n_words']}")
        sys.stdout.flush()
    out["summary"] = {
      "C1_all": all(r["C1_ok"] for r in out["rows"] if r["C1_ok"] is not None),
      "C2_all": all(r["C2_ok"] for r in out["rows"]),
      "C3_all": all(r["C3_ok"] for r in out["rows"]),
      "C4_all": all(r["C4_ok"] for r in out["rows"] if r["C4_ok"] is not None),
      "C5_all": all(r["C5_ok"] for r in out["rows"]),
      "total_words": sum(r["n_words"] for r in out["rows"])}
    print(json.dumps(out["summary"], indent=1))
    json.dump(out, open("u2b_systole.json", "w"), indent=1)
