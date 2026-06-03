#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bgoal_escape_char.py  (goal B) — characterize the escape from naive D under T_q.

Naive map T_q(x,y) = (y, k*lam*y - x), k = floor((1+x)/(lam*y)), lam=2cos(pi/q).
Naive domain D = {x>0, y>0, x+lam*y>1}.

Questions:
 1) Reproduce escape rate from random seeds in D (per corrected findings).
 2) WHERE do orbits escape to? below line (x+lam*y<1)? above box (x>1 or y>1)? y'<=0?
 3) Does the BOUNDED triangle Dbox = {0<x<=1,0<y<=1,x+lam*y>1} stay invariant?
 4) Distribution of digits k produced -- are large/anomalous digits appearing (admissibility)?
"""
import math, random

def lam(q): return 2*math.cos(math.pi/q)

def step(x, y, l):
    k = math.floor((1+x)/(l*y))
    yp = k*l*y - x
    return (y, yp), k

def in_D(x, y, l, eps=1e-12):
    return x > eps and y > eps and (x + l*y) > 1 + eps

def in_box(x, y, l, eps=1e-12):
    return 0 < x <= 1+eps and 0 < y <= 1+eps and (x + l*y) > 1 - eps

def rand_seed_in_D(l):
    # sample uniformly in unit box, reject until in D (above line), x,y in (0,1)
    for _ in range(10000):
        x = random.random(); y = random.random()
        if in_D(x, y, l):
            return x, y
    return None

def classify_escape(x, y, l):
    """why did (x,y) leave D? return tag"""
    if x <= 0 or y <= 0:
        return 'nonpos'
    if x + l*y <= 1:
        return 'below_line'
    return 'in_D'  # shouldn't happen

def run(q, nseed=2000, nstep=500):
    l = lam(q)
    random.seed(12345)
    esc_D = 0; esc_box = 0
    reasons = {}
    digit_hist = {}
    box_invariant = True
    maxstep_in_D = []
    for _ in range(nseed):
        s = rand_seed_in_D(l)
        if s is None: continue
        x, y = s
        steps_survived = nstep
        escaped = False
        for t in range(nstep):
            (x, y), k = step(x, y, l)
            digit_hist[k] = digit_hist.get(k, 0) + 1
            if not in_D(x, y, l):
                reasons[classify_escape(x, y, l)] = reasons.get(classify_escape(x,y,l),0)+1
                steps_survived = t
                escaped = True
                break
            if not in_box(x, y, l):
                box_invariant = False
        if escaped:
            esc_D += 1
        maxstep_in_D.append(steps_survived)
    return dict(q=q, l=round(l,6), esc_rate=esc_D/nseed,
                reasons=reasons, digits=dict(sorted(digit_hist.items())),
                box_invariant=box_invariant,
                med_survive=sorted(maxstep_in_D)[len(maxstep_in_D)//2])

if __name__ == "__main__":
    for q in [3,4,5,6,7,8,12,13]:
        r = run(q, nseed=1000, nstep=500)
        print(f"q={r['q']:>3} lam={r['l']:>8} esc_rate={r['esc_rate']:.3f} "
              f"med_survive={r['med_survive']:>3} box_inv={r['box_invariant']} "
              f"reasons={r['reasons']} digits={r['digits']}")
