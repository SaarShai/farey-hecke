import collections
for n in [11,12]:
    mask=(1<<n)-1
    V=list(range(1,1<<n))
    # 0-compatible degree distribution (just counts, edges huge so estimate via per-vertex)
    # For a single vertex P, count R with overlap & incomparable:
    # complement of: R&P==0 (disjoint) OR P subset R OR R subset P (and R!=0,R!=P)
    # Count disjoint: R subset complement(P): 2^(n-|P|)-1 (exclude 0) ... but also R could equal? R!=0
    # supersets of P: 2^(n-|P|) including P itself; proper supersets among nonzero: 2^(n-|P|)-1 (exclude P)
    # subsets of P (nonzero, != P): 2^|P|-2
    # We'll just sample to get max/avg degree.
    import random
    random.seed(1)
    samp=random.sample(V, 400)
    degs=[]
    for P in samp:
        pc=bin(P).count('1')
        disjoint=(1<<(n-pc))-1            # R nonzero, R&P==0 => R subset ~P, nonzero
        supersets=(1<<(n-pc))-1           # R proper superset of P (nonzero, !=P): choose subset of ~P nonempty
        subsets=(1<<pc)-2                 # R proper nonzero subset of P
        # careful double count: disjoint and subset/superset are exclusive. total nonzero others = 2^n-2
        bad=disjoint+supersets+subsets
        good=(1<<n)-2-bad
        degs.append(good)
    print(f"n={n}: nonzero={len(V)}; compat-0 degree min/avg/max = {min(degs)}/{sum(degs)//len(degs)}/{max(degs)}")
