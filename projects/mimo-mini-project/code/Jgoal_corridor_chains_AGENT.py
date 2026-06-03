#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GOAL J — targeted corridor-chain refutation probe (sharpest vector at large q).
The random word stream under-samples STRUCTURED long words. The goal-H/I danger is a
sub-threshold CYCLE that chains elliptic corridors F_k=(q-1,k)(q-1,0)(q-3,0).
Here we DIRECTLY enumerate:
  (a) every single F_k block (k=0..6) ess-sup,
  (b) all 2- and 3-block chains  F_{k1} F_{k2} (F_{k3}),  k_i in {1,2,3} (the elliptic ones),
      = periods up to 9, the explicit corridor-chaining words,
  (c) rotation powers R^m where R=(q-1,1) and the W_q word repeated,
and report the MIN ess-sup vs 1/lam^3. Any value < thr -> REFUTATION (hi-prec verify).
Reuses validated machinery from Jgoal_bulletproof_q81_150_AGENT.
"""
import itertools, math
import numpy as np
import Jgoal_bulletproof_q81_150_AGENT as J

def probe(q):
    l, x = J.build(q); thr = 1.0/l**3
    best = (math.inf, None)
    tested = 0
    blocks = {k: [(q-1, k), (q-1, 0), (q-3, 0)] for k in range(0, 7)}
    # (a) single blocks
    cand = [blocks[k] for k in range(0, 7)]
    # (b) 2- and 3-block chains over elliptic digits k in {0,1,2,3}
    digs = [0, 1, 2, 3]
    for k1, k2 in itertools.product(digs, repeat=2):
        cand.append(blocks[k1] + blocks[k2])
    for k1, k2, k3 in itertools.product(digs, repeat=3):
        cand.append(blocks[k1] + blocks[k2] + blocks[k3])
    # (c) rotation R=(q-1,1) powers, and W_q^m
    for m in range(1, 13):
        cand.append([(q-1, 1)]*m)
    for m in range(1, 5):
        cand.append(blocks[3]*m)        # W_q repeated
    # also mix with cusp letter and q-5 support
    for k1 in digs:
        cand.append(blocks[k1] + [(q-2, 0)])
        cand.append(blocks[k1] + [(q-5, 0)])
        cand.append([(q-1, k1), (q-1, 0), (q-5, 0)])
    for w in cand:
        tested += 1
        res = J.word_esssup(w, x, q, l)
        if res is None: continue
        Xc, s_lo, s_hi = res
        if Xc < best[0] - 1e-14:
            best = (Xc, w)
    return best, thr, tested

if __name__ == "__main__":
    refut = []
    for q in [81, 97, 113, 131, 149]:
        (Xc, w), thr, tested = probe(q)
        ratio = Xc/thr if Xc < math.inf else math.inf
        below = Xc < thr - 1e-9
        print(f"q={q}: thr={thr:.10f} corridor_min={Xc:.10f} ratio={ratio:.8f} "
              f"{'<<< BELOW' if below else 'OK'} tested={tested} word={w}")
        if below:
            hp = J.hi_prec_verify(q, w, dps=60)
            print(f"     HI-PREC: {hp}")
            refut.append((q, w, Xc, thr))
    print(f"\nCORRIDOR_REFUTATION = {len(refut) > 0}")
