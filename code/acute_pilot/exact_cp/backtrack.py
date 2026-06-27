#!/usr/bin/env python3
"""Exact branch-and-bound for maximum acute set in {0,1}^n.

Maintain current acute set S and candidate set C = {v : S+{v} still acute, v > last added}.
We exploit: a vertex v keeps S acute iff for all pairs a,b in S: not forb3(v,a,b).
We DON'T fix an ordering of the cube a priori for C besides the index order to avoid
re-visiting permutations of the same set (standard MIS-style: only add vertices with
index > max index in S). This makes it a proper enumeration.

Symmetry: fix 0 in S (WLOG by translation). Then candidates are nonzero vertices.
To further cut symmetry we could fix coordinate-permutation canonical form, but that's
expensive; we rely on the 0-fix + index ordering.

Bound: |S| + |C| <= best  => prune (can't beat). Plus a cheap clique-style bound:
candidates form constraints; we use |C| as the simple bound. Optionally a greedy bound.

Returns best size found and a witness, or proves max if search completes.
"""
import sys, time

def forb3(A,B,C):
    return ((B^A)&(C^A))==0 or ((A^B)&(C^B))==0 or ((A^C)&(B^C))==0

class BT:
    def __init__(self, n, target=None, time_limit=1e18, start_best=0, start_S=None):
        self.n=n; self.N=1<<n
        self.target=target          # stop early if reach this size
        self.tl=time_limit
        self.t0=time.time()
        self.best=start_best
        self.bestS=start_S[:] if start_S else None
        self.nodes=0
        self.timed_out=False
        self.completed=False

    def compat(self, v, S):
        """Does S+{v} stay acute? S is acute already; only triples with v matter."""
        L=len(S)
        for i in range(L):
            a=S[i]; xa=a^v
            for j in range(i+1,L):
                b=S[j]; xb=b^v; ab=a^b
                if (xa&xb)==0 or (xa&ab)==0 or (xb&ab)==0:
                    return False
        return True

    def search(self, S, C):
        """S: current acute set (list). C: sorted list of candidate masks (all > some threshold,
        each individually compatible with S). Branch."""
        self.nodes+=1
        if (self.nodes & 0x3fff)==0 and time.time()-self.t0>self.tl:
            self.timed_out=True; return
        if self.timed_out: return
        if len(S)>self.best:
            self.best=len(S); self.bestS=S[:]
            if self.target and self.best>=self.target:
                return
        # bound
        if len(S)+len(C)<=self.best:
            return
        # branch over candidates in order; standard MIS: pick candidates one by one,
        # for each chosen v, restrict remaining C to those after v AND compatible with S+{v}.
        Cl=C
        for idx in range(len(Cl)):
            if self.timed_out: return
            if len(S)+(len(Cl)-idx)<=self.best:  # can't even reach best with remaining
                return
            v=Cl[idx]
            # build new candidate set: those after idx that stay compatible with S+{v}
            S.append(v)
            newC=[]
            for w in Cl[idx+1:]:
                # w must be compatible with S (already true) AND form no bad triple with v + S
                # i.e. S2=S (now includes v); check triples involving w and the NEW vertex v with others
                # Simplest: full compat(w, S) where S includes v. But w was compat with S\{v}; only
                # new triples are those involving v. Check forb3(w, v, s) for s in S\{v}, and forb3(w,v,?)...
                # Just do incremental: bad if forb3(w,v,s) for some s in S (s!=w), OR forb3 with v as one corner.
                ok=True
                xwv=w^v
                # check pairs (v, s) for s in S (S includes v at end)
                for s in S:
                    if s==v: continue
                    xws=w^s; vs=v^s
                    if (xwv&xws)==0 or (xwv&vs)==0 or (xws&vs)==0:
                        ok=False; break
                if ok:
                    newC.append(w)
            self.search(S, newC)
            S.pop()
        # also the option of NOT taking any more (handled by bound/return)
        # mark completion only at top level

def run(n, target=None, time_limit=300, start_S=None, order='mid'):
    bt=BT(n, target=target, time_limit=time_limit)
    # initial S: fix 0
    S=[0]
    # candidate order: 'mid' = sort by closeness of popcount to n/2 (records cluster there), then value
    nz=list(range(1,1<<n))
    c=n/2
    if order=='mid':
        nz.sort(key=lambda v:(abs(bin(v).count('1')-c), v))
    elif order=='val':
        nz.sort()
    # filter to those compatible with {0} (all nonzero are, since {0,v} can't form a triple alone)
    C=[v for v in nz]
    if start_S:
        # seed best with a known acute set size (lower bound) to prune
        bt.best=len(start_S)-1  # so we still try to beat it
    bt.search(S, C)
    if not bt.timed_out:
        bt.completed=True
    return bt

if __name__=="__main__":
    n=int(sys.argv[1])
    target=int(sys.argv[2]) if len(sys.argv)>2 and sys.argv[2]!='-' else None
    tl=float(sys.argv[3]) if len(sys.argv)>3 else 60
    order=sys.argv[4] if len(sys.argv)>4 else 'mid'
    bt=run(n, target=target, time_limit=tl, order=order)
    status = "COMPLETED (exact max proven)" if bt.completed else ("TIMEOUT" if bt.timed_out else "stopped")
    print(f"n={n}: best={bt.best} nodes={bt.nodes} status={status} time={time.time()-bt.t0:.1f}s")
    if bt.bestS:
        path=f"/Users/za/Documents/farey-hecke/code/acute_pilot/exact_cp/bt_witness_n{n}_s{bt.best}.txt"
        with open(path,"w") as f:
            for v in bt.bestS: f.write("".join('1' if (v>>i)&1 else '0' for i in range(n))+"\n")
        print("witness:",path)
