#!/usr/bin/env python3
"""Bevan (2006) Thm 4.3 general acute-set product construction (verbatim).
Acute (cubic) D-set from S_1..S_M (acute, dims d_r, sizes n_r, n_1<=...<=n_M) plus
an acute 'Z' set (dim d_Z, size n_Z >= prod_{r=2}^M n_r).
  T = { v^1_{k1} v^2_{k2} ... v^M_{kM} z_{kZ} : 0<=k_r<n_r },  kZ = <<k1..kM>>_{n1..nM}
  <<k1..kM>> = sum_{r=2}^M ((k_{r-1}-k_r) mod n_r) * prod_{s=r+1}^M n_s
D = sum d_r + d_Z,  N = prod n_r.   Every triple is acute (proof: Thm 4.3).
"""
def kz_index(ks, ns):
    """ks,ns: lists len M (1-indexed math -> 0-indexed here). Returns <<k1..kM>>."""
    M=len(ns); total=0
    for r in range(2,M+1):  # math index r=2..M
        kr1=ks[r-2]; kr=ks[r-1]; nr=ns[r-1]
        diff=(kr1-kr)%nr
        prodtail=1
        for s in range(r+1,M+1): prodtail*=ns[s-1]
        total += diff*prodtail
    return total

def bevan_product(Sblocks, Sdims, Zset, Zdim):
    """Sblocks: list of M sets (each list of int bitmasks, dim Sdims[r]). Must be sorted by size asc.
    Zset: acute set (list of bitmasks) dim Zdim, size>=prod_{r>=2} n_r. Returns (points, D)."""
    M=len(Sblocks); ns=[len(s) for s in Sblocks]
    assert all(ns[i]<=ns[i+1] for i in range(M-1)), "S-blocks must be size-sorted ascending"
    need=1
    for r in range(2,M+1): need*=ns[r-1]
    assert len(Zset)>=need, f"Z too small: {len(Zset)} < {need}"
    import itertools
    pts=[]
    ranges=[range(n) for n in ns]
    # bit offsets
    offs=[]; o=0
    for d in Sdims: offs.append(o); o+=d
    zoff=o
    for ks in itertools.product(*ranges):
        kZ=kz_index(list(ks),ns)
        val=0
        for r in range(M):
            val |= Sblocks[r][ks[r]] << offs[r]
        val |= Zset[kZ] << zoff
        pts.append(val)
    D=sum(Sdims)+Zdim
    return pts, D
