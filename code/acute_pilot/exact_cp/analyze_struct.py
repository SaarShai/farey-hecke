"""Structural analysis: fix 0 in S (WLOG by translation symmetry).
With 0 in S and other points being subsets (as bitmasks), classify the
3 right-angle conditions for a triple involving / not involving 0.

Right angle at apex Q between P,R:  (P^Q)&(R^Q)==0.

Case A: apex = 0.  P^0=P, R^0=R => forbidden if P & R == 0  (disjoint supports).
Case B: apex = P (P,R nonzero, plus 0 in set): triple {0,P,R}, apex P:
        (0^P)&(R^P) = P & (R^P) == 0.
        P&(R^P) = P & (R & ~P | ~R & P) ... = P&~R (the part of P not in R). ==0 means P subset R.
Case C: apex = R symmetric: R subset P.
So triple {0,P,R} is forbidden iff: P&R==0  OR  P subset R  OR  R subset P.
=> Allowed (acute-compatible w.r.t 0) iff P,R OVERLAP but neither contains the other:
   P&R != 0  AND  P\R != 0  AND  R\P != 0  ("crossing/incomparable & intersecting").
This is the (2,1)-separating / antichain-with-intersection condition.

For triples NOT containing 0 (P,Q,R all nonzero), full 3 apex checks apply.
"""
import itertools
def popcount(x): return bin(x).count('1')

# Verify the {0,P,R} reduction empirically for n=5
n=5
def ra(P,Q,R): return ((P^Q)&(R^Q))==0
def forbidden0PR(P,R):
    return ra(P,0,R) or ra(0,P,R) or ra(0,R,P)
def reduced(P,R):
    return (P&R==0) or ((P & ~R)& ((1<<n)-1))==0 or ((R&~P)&((1<<n)-1))==0
ok=True
for P in range(1,1<<n):
    for R in range(1,1<<n):
        if P==R: continue
        if forbidden0PR(P,R) != reduced(P,R):
            ok=False; print("MISMATCH",P,R)
print("0-PR reduction correct:", ok)

# Count "compatible with 0" pairs: how many nonzero P have at least the pairwise property is about pairs.
# Count candidate vertices that could ever pair: all nonzero except... every nonzero can pair with some.
# Real constraint: build graph G on nonzero vertices, edge iff pair {P,R} is "0-compatible"
# (overlap & incomparable). Then S\{0} must be a clique in G AND additionally satisfy
# all-nonzero triple conditions. So S\{0} is a clique in G with extra 3-uniform constraints.
V=[v for v in range(1,1<<n)]
mask=(1<<n)-1
def compat0(P,R):
    return (P&R)!=0 and (P&~R&mask)!=0 and (R&~P&mask)!=0
import collections
deg=collections.Counter()
edges=0
for i in range(len(V)):
    for j in range(i+1,len(V)):
        if compat0(V[i],V[j]):
            edges+=1; deg[V[i]]+=1; deg[V[j]]+=1
print(f"n={n}: nonzero verts={len(V)}, 0-compatible pairs(edges)={edges}")
print("max degree in compat-0 graph:", max(deg.values()) if deg else 0)
