#!/usr/bin/env python3
"""
Acuteness for LINEAR codes (subspaces of GF(2)^n):
  S = C linear is ACUTE  <=>  no two DISTINCT NONZERO codewords u,w have disjoint supports
  (because right angle at apex Q needs (P^Q)&(R^Q)=0; for linear C, u=P^Q,w=R^Q range over
   all nonzero codewords, and apex Q is free).
Equivalently: for all nonzero u,w in C with u!=w:  supp(u) & supp(w) != empty.
Note u=w is fine (that's P=R, not a triple). u&u=u!=0 always for nonzero u, so the constraint
is purely on DISTINCT pairs. Also note: if u,w in C then u^w in C; u&w=0 => w subset of complement.

A linear acute code of dim d gives 2^d acute points. We want max dim in length n.
Key fact: weight-w codewords pairwise intersect if 2w>n (any two w-subsets of [n] overlap when 2w>n).
=> a CONSTANT-WEIGHT code with all weights > n/2 is automatically acute as a SET (not nec. linear).
For LINEAR codes the all-zero word exists; its 'support' is empty so it would right-angle with everything?
Check: u=0 isn't allowed as a leg (P=Q). 0 in C is the apex/point itself, fine. The legs are NONZERO.
"""
import sys, itertools
sys.path.insert(0,'..')
from verify import is_acute, rows_to_masks

def linear_acute(basis, n):
    # generate code, test
    C=[0]
    for b in basis:
        C=C+[c^b for c in C]
    C=list(set(C))
    nz=[c for c in C if c]
    for i in range(len(nz)):
        for j in range(i+1,len(nz)):
            if (nz[i]&nz[j])==0:
                return False, (nz[i],nz[j]), C
    return True, None, C

if __name__=='__main__':
    print("module ok")
