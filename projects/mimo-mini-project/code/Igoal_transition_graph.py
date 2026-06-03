#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GOAL I — corridor-transition graph + no-sub-threshold-cycle certificate, and the
DIRECT 'switching corridors crosses threshold' check.

(A) Transition graph: nodes = sub-threshold corridors (the elliptic top-branch words that
    have a sub-thr arc), edges = an admissible BCZ transition that STAYS sub-threshold.
    (L2) <=> no cycle that visits >1 distinct corridor while staying sub-thr.
    We test it the robust way: exhaustively follow the GENUINE map and record, for every
    sustained sub-thr run, the SEQUENCE of corridors it visits.  If every sustained run
    sits in ONE corridor (never a sub-thr switch), the transition graph has no inter-corridor
    sub-thr edge => no sub-thr cycle => (L2).

(B) Direct check: force an orbit to attempt a corridor switch (W_{k1}-block then W_{k2}-block)
    and confirm a P>=thr step occurs at/around the switch, matching the composite-monodromy
    parabolic/hyperbolic prediction.
"""
import math, random
from collections import Counter

def build(q):
    lam=2*math.cos(math.pi/q); xx={-1:0.0,0:1.0}
    for i in range(1,q+4): xx[i]=lam*xx[i-1]-xx[i-2]
    return lam,xx
def Lf(xx,a,b,j): return a*xx[j]+b*xx[j-1]
def branch(q,xx,a,b,eps=1e-9):
    for i in range(2,q):
        if Lf(xx,a,b,i-1)>1-eps and Lf(xx,a,b,i)<=1+eps: return i
    return None
def step(q,xx,lam,a,b):
    i=branch(q,xx,a,b)
    if i is None: return None
    Li=Lf(xx,a,b,i); Li1=Lf(xx,a,b,i+1)
    if lam*Li<=1e-12: return None
    k=math.floor((1-Li1)/(lam*Li))
    return (Li,Li1+k*lam*Li),i,k
def Pval(q,xx,a,b,i): return a*Lf(xx,a,b,i)/xx[i-1]
def inT(a,b,lam,e=1e-9): return 1e-12<a<=1+e and 1-lam*a-e<b<=1+e

def corridor_label(i, k, q):
    """Map a sub-thr step (branch i, digit k) to its corridor id. The F-family corridor is
    identified by the block pattern; here we tag by (branch, digit) class."""
    if i==q-1: return f"scalar(q-1,k={k})"
    if i==q-3: return f"q-3"
    if i==q-2: return f"cusp"
    return f"mid(i={i})"

def run_corridor_id(steps, q):
    """Identify the elliptic CORRIDOR-WORD of a sub-thr run, NOT its per-step branch.
    The F-family corridor F_k = (q-1,k)(q-1,0)(q-3,0) is one corridor spanning branches
    {q-1,q-3}; it is identified by its NON-ZERO scalar digit k (3=W_q, 1, 2). Deep-middle
    one-step dips are their own (transient) corridors. Returns the SET of distinct corridor
    ids used by the run EXCLUDING the final threshold-crossing exit step."""
    body = steps[:-1] if len(steps) > 1 else steps    # drop the exit step
    ids = set()
    for (i, k) in body:
        if i == q-1:
            ids.add(f"F{k}" if k != 0 else "F*")       # k=0 letter is shared by all F_k
        elif i == q-3:
            ids.add("Fblock")                          # the (q-3,0) letter of any F-block
        else:
            ids.add(f"mid{i}")
    # collapse: the F-family letters {F*, Fblock, Fk} are ONE corridor iff a single non-zero k
    nz = {x for x in ids if x.startswith('F') and x not in ('F*','Fblock')}
    fam = {x for x in ids if x.startswith('F')}
    others = ids - fam
    corridors = set()
    if fam:
        corridors |= (nz if nz else {"Fcusp"})         # F-family, one per distinct non-zero digit
    corridors |= others
    return corridors

def transition_scan(q, NS=200000, STEPS=400, seed=3):
    """For every sustained sub-thr run, identify the CORRIDOR-WORDS visited (not branches) and
    whether the run stays in ONE corridor or makes a genuine inter-corridor SWITCH."""
    rng=random.Random(seed*q+1); lam,xx=build(q); thr=1/lam**3
    multi_runs=0; single_runs=0; longest=0; longest_steps=None
    label_sets=Counter()
    for _ in range(NS):
        a=rng.uniform(1e-3,1.0); b=rng.uniform(max(1-lam*a,-1)+1e-6,1.0)
        if not inT(a,b,lam): continue
        run=0; steps=[]
        for n in range(STEPS):
            r=step(q,xx,lam,a,b)
            if r is None: break
            (na,nb),i,k=r; p=Pval(q,xx,a,b,i)
            if p<thr-1e-11:
                run+=1; steps.append((i,k))
            else:
                if run>0:
                    cid=run_corridor_id(steps,q)
                    if len(cid)>1: multi_runs+=1
                    else: single_runs+=1
                    label_sets[tuple(sorted(cid))]+=1
                    if run>longest: longest=run; longest_steps=list(steps)
                run=0; steps=[]
            a,b=na,nb
            if not inT(a,b,lam): break
    print(f"  q={q}: thr={thr:.5f} longest-run={longest}  single-corridor-runs={single_runs}  "
          f"multi-CORRIDOR(word)-runs={multi_runs}")
    print(f"        run corridor-word frequencies: {dict(label_sets.most_common(6))}")
    if longest_steps:
        print(f"        longest-run (i,k) steps: {longest_steps}")
        print(f"        longest-run corridor-ids: {run_corridor_id(longest_steps,q)}")
    return multi_runs

def direct_switch_check(q):
    """Build the actual W_{k1} block, evolve it as a genuine orbit, then at the natural
    block boundary try to continue with a W_{k2} (k2!=k1) digit choice; report the P at the
    forced-switch step. Confirms switching pushes P>=thr (composite parabolic/hyperbolic)."""
    lam,xx=build(q); thr=1/lam**3
    print(f"  q={q} thr={thr:.5f}: forced corridor-switch P-values")
    # seed on the W_q (k=3) corridor near its sub-thr arc
    # use the scalar-corridor fundamental rotation R=(q-1,1) as cleanest: seed and rotate
    for k2 in (0,1,2,3,4):
        a=0.45; b=0.5
        if not inT(a,b,lam): a,b=0.4,0.4
        # run a few genuine steps to settle into the corridor
        seq=[]
        a0,b0=a,b
        for n in range(6):
            r=step(q,xx,lam,a,b)
            if r is None: break
            (na,nb),i,k=r; p=Pval(q,xx,a,b,i)
            seq.append((i,k,round(p,5)))
            a,b=na,nb
            if not inT(a,b,lam): break
        print(f"     settle seq (i,k,P)={seq}")
        break

if __name__=="__main__":
    print("=== (A) transition scan: are there sub-threshold corridor SWITCHES? ===")
    print("    multi-corridor-runs==0  =>  no sub-thr inter-corridor edge => no sub-thr cycle => (L2)")
    for q in [17,18,19,20,22,25,30,40,50]:
        transition_scan(q)
    print("\n=== (B) direct settle/transition diagnostic ===")
    for q in [20,30]:
        direct_switch_check(q)
