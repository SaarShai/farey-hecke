#!/usr/bin/env python3
"""Goal E numeric pre-test (THE one that matches the Lean hypothesis).

Scalar Hecke map T_q (branch i=q-1):  c_{n+2} = K_n * lam * c_{n+1} - c_n,
  K_n = floor((1+c_n)/(lam*c_{n+1})),  domain c_n + lam*c_{n+1} > 1, c_n>0.
Genuine cap: c_n <= 1 for ALL n  (this is the hypothesis `hle1`).

Tests, for t = 1/lam^3:
 (A) max run of consecutive products P_n=c_n c_{n+1} < t, WITH the cap vs WITHOUT.
     The window-W lemma claims max run = W-1. Goal: W=4 at q=5 (max run 3), and
     show the cap is ESSENTIAL (without it the run is longer => the lemma is false).
 (B) the worst floor itineraries (K_n words) realizing the maximal run -> case structure.
 (C) a dense LOCAL search over (a,b,K0,K1,K2) of 5-coord windows satisfying all the
     Lean hypotheses, reporting every itinerary that gets all 4 products < t (should be
     NONE if window-4 is true), and the near-misses (run=3) -> the boundary cases.
"""
import math, random
import numpy as np
from collections import Counter
random.seed(2026)

def lam(q): return 2*math.cos(math.pi/q)

def run_orbit_test(q, cap, NS=400000, STEPS=60):
    l = lam(q); thr = 1.0/l**3
    maxrun = 0; worst_word = None
    for _ in range(NS):
        # seed in (0,1]x(0,1] region with c+lam*cp>1
        a = random.uniform(1e-4, 1.0)
        blo = max(1 - l*a, 1e-9)
        if blo > 1: continue
        b = random.uniform(blo + 1e-9, 1.0)
        c, cp = a, b
        run = 0; word = []
        for n in range(STEPS):
            if not (c > 0 and cp > 0 and c + l*cp > 1): break
            if cap and (c > 1.0 or cp > 1.0): break
            K = math.floor((1 + c)/(l*cp))
            if K < 1: break
            P = c*cp
            c2 = K*l*cp - c
            if P < thr - 1e-12:
                run += 1; word.append(K)
                if run > maxrun:
                    maxrun = run; worst_word = list(word)
            else:
                run = 0; word = []
            c, cp = cp, c2
    return thr, maxrun, worst_word

print("=== (A) ORBIT max-run, cap vs no-cap ===")
for q in [5, 6, 7, 8, 13]:
    thr, mr_cap, w_cap = run_orbit_test(q, cap=True)
    _,   mr_no,  w_no  = run_orbit_test(q, cap=False)
    print(f"q={q}: thr={thr:.6f}  CAP maxrun={mr_cap} (win={mr_cap+1}) word~{w_cap}"
          f"   NOCAP maxrun={mr_no} (win={mr_no+1}) word~{w_no}")

print("\n=== (C) q=5 LOCAL dense search over (a,b,K0,K1,K2) windows w/ all hyps + cap ===")
q = 5; l = lam(q); thr = 1.0/l**3
print(f"q=5 thr=1/phi^3={thr:.8f}")
# scan a,b on a fine grid; for each, the floors K0,K1,K2 are DETERMINED by the map,
# but we also enumerate K freely to map the feasible-itinerary set.
best_run = 0
run3_words = Counter()
run3_examples = {}
all4_hits = 0
N = 1200
def step_coord(c, cp, K):
    return K*l*cp - c
for ia in range(1, N+1):
    a = ia/N
    blo = max(1 - l*a, 1e-9)
    if blo > 1: continue
    nb = 200
    for ib in range(nb+1):
        b = blo + (1.0 - blo)*ib/nb
        if not (0 < b <= 1.0): continue
        if not (a + l*b > 1): continue
        # follow the actual map for 4 products, requiring cap+domain throughout
        c0, c1 = a, b
        coords = [c0, c1]; Ks = []; Ps = []; ok = True
        for s in range(3):
            cc, cp = coords[-2], coords[-1]
            if not (cp > 0 and cc + l*cp > 1): ok = False; break
            K = math.floor((1+cc)/(l*cp))
            if K < 1: ok = False; break
            c2 = step_coord(cc, cp, K)
            coords.append(c2); Ks.append(K)
        if len(coords) < 5: continue
        if any(x <= 0 for x in coords): continue
        if any(x > 1.0 + 1e-12 for x in coords): continue   # CAP on all 5
        # domain on all consecutive pairs
        domok = all(coords[j] + l*coords[j+1] > 1 for j in range(4))
        if not domok: continue
        Ps = [coords[j]*coords[j+1] for j in range(4)]
        below = [p < thr - 1e-12 for p in Ps]
        # count run of consecutive below starting anywhere in the 4-window
        nbelow = sum(below)
        # longest consecutive
        lr = 0; cur = 0
        for bb in below:
            if bb: cur += 1; lr = max(lr, cur)
            else: cur = 0
        if all(below):
            all4_hits += 1
            if all4_hits <= 5:
                print(f"  !!! ALL4 below: a={a:.4f} b={b:.4f} K={Ks} P={[round(p,5) for p in Ps]}")
        if lr > best_run:
            best_run = lr
        if lr >= 3:
            run3_words[tuple(Ks)] += 1
            if tuple(Ks) not in run3_examples:
                run3_examples[tuple(Ks)] = (round(a,4), round(b,4),
                                            [round(p,5) for p in Ps],
                                            [round(c,4) for c in coords])
print(f"  local best consecutive run = {best_run}   ALL4-below hits = {all4_hits}")
print(f"  run>=3 floor-words (K0,K1,K2) -> count:")
for word, cnt in run3_words.most_common():
    print(f"    K={word}: {cnt}   ex {run3_examples[word]}")
