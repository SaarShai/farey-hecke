"""
goal1_q4_mechanism.py — reverse-engineer the EXACT case structure of q=4 clusters,
to ground the Lean proof. Adversarial: find any counterexample to the conjectured
lemmas; tabulate every size-2 cluster's branch/floor/coordinate structure.
"""
from __future__ import annotations
import math
import numpy as np

rng = np.random.default_rng(7)
LAM = math.sqrt(2.0)
X = math.sqrt(2.0) / 8.0   # 0.176776695...


def branch(a, b):
    """T_2 if a+sqrt2*b <= 1 else T_3.  (domain guarantees sqrt2*a+b>1, b<=1)"""
    return 2 if (a + LAM * b) <= 1.0 else 3


def P_obs(a, b):
    """observable P = 1/R_q."""
    if branch(a, b) == 3:        # w_3=(0,1): P = a*b
        return a * b
    else:                        # w_2=(1,sqrt2): P = a*(a+sqrt2 b)/sqrt2
        return a * (a + LAM * b) / LAM


def step(a, b):
    i = branch(a, b)
    if i == 3:
        # w_3.(a,b)=b ; w_4.(a,b)=-a ; k=floor((1+a)/(sqrt2 b))
        k = math.floor((1.0 + a) / (LAM * b))
        return b, -a + k * LAM * b, 3, k
    else:
        # w_2.(a,b)=a+sqrt2 b ; w_3.(a,b)=b ; k=floor((1-b)/(sqrt2(a+sqrt2 b)))
        s = a + LAM * b
        k = math.floor((1.0 - b) / (LAM * s))
        return s, b + k * LAM * s, 2, k


def in_domain(a, b, tol=1e-9):
    return (0 < a <= 1 + tol) and (1 - LAM * a - tol < b <= 1 + tol)


# ---- 1. min P over T_2 (test Lemma A: P>=1-sqrt2/2 on T_2) ----
def scan_T2_min(n=4_000_000):
    mn = 1e9
    arg = None
    cnt2 = 0
    # sample uniformly in bounding box of domain a in (0,1], b in (1-sqrt2 a,1]
    for _ in range(n):
        a = rng.random()
        b = (1 - LAM * a) + rng.random() * (1 - (1 - LAM * a))
        if not in_domain(a, b):
            continue
        if branch(a, b) == 2:
            cnt2 += 1
            p = P_obs(a, b)
            if p < mn:
                mn = p
                arg = (a, b)
    return mn, arg, cnt2


# ---- 2. tabulate size-2 clusters over a long orbit ----
def cluster_structure(n_steps=3_000_000, n_starts=30, burn=300):
    records = []          # one per size-2 cluster
    extreme_T2 = 0        # count extreme points that are in T_2 (should be 0)
    max_run = 0
    for _ in range(n_starts):
        # random start
        while True:
            a = rng.random(); b = rng.random()
            if in_domain(a, b):
                break
        for _ in range(burn):
            a, b, _, _ = step(a, b)
        seq = []
        for _ in range(n_steps):
            i = branch(a, b)
            p = P_obs(a, b)
            seq.append((a, b, i, p))
            if p < X and i == 2:
                extreme_T2 += 1
            a, b, _, _ = step(a, b)
        # find runs of p<X  (store index to recover k,ell)
        seqk = []  # (a,b,i,p,k)
        a2, b2 = None, None
        # recompute with k
        # rebuild seq with k by re-stepping
        run = []
        for rec in seq:
            if rec[3] < X:
                run.append(rec)
            else:
                if len(run) >= 1:
                    max_run = max(max_run, len(run))
                if len(run) == 2:
                    records.append((run[0], run[1], rec))  # two extreme + the next (non-extreme)
                run = []
    return records, extreme_T2, max_run


def cluster_k_stats(n_steps=2_000_000, n_starts=20, burn=300):
    """For each size-2 cluster, record (a,b,c,d,k,ell, third_branch)."""
    recs = []
    for _ in range(n_starts):
        while True:
            a = rng.random(); b = rng.random()
            if in_domain(a, b):
                break
        for _ in range(burn):
            a, b, _, _ = step(a, b)
        prev = []  # rolling buffer of (a,b,i,p,k_to_next)
        buf = []
        for _ in range(n_steps):
            i = branch(a, b)
            p = P_obs(a, b)
            a_n, b_n, ii, k = step(a, b)
            buf.append((a, b, i, p, k))
            a, b = a_n, b_n
        # scan buffer for runs of p<X of length exactly 2
        j = 0
        n = len(buf)
        while j < n:
            if buf[j][3] < X:
                start = j
                while j < n and buf[j][3] < X:
                    j += 1
                length = j - start
                if length == 2 and j < n:
                    p0 = buf[start]; p1 = buf[start+1]; p2 = buf[j]
                    recs.append((p0, p1, p2))
            else:
                j += 1
    return recs


if False:
    pass


if __name__ == "__main__":
    print(f"X = sqrt2/8 = {X:.10f};  1-sqrt2/2 = {1-LAM/2:.10f}")
    mn, arg, cnt2 = scan_T2_min()
    print(f"\n[Lemma A test] min P over T_2 (n_T2={cnt2}): {mn:.6f} at {arg}")
    print(f"   conjecture P>=1-sqrt2/2={1-LAM/2:.6f} on T_2 -> "
          f"{'HOLDS' if mn >= (1-LAM/2)-1e-6 else 'FAILS'}; "
          f"> X={X:.6f}: {'YES' if mn> X else 'NO'}")

    records, extreme_T2, max_run = cluster_structure()
    print(f"\nmax_run over orbit = {max_run}")
    print(f"extreme points in T_2 (should be 0): {extreme_T2}")
    print(f"# size-2 clusters tabulated: {len(records)}")

    # aggregate the structure of size-2 clusters
    from collections import Counter
    branch_pat = Counter()
    third_branch = Counter()
    ks = []
    ells = []
    b_mid = []   # shared middle coordinate
    a_first = []
    c_third = []
    for (r0, r1, r2) in records:
        # r0=(a,b), r1=(b,c) shared b; r2=(c,d)
        a0, b0, i0, p0 = r0
        a1, b1, i1, p1 = r1
        a2, b2, i2, p2 = r2
        branch_pat[(i0, i1)] += 1
        third_branch[i2] += 1
        b_mid.append(b0)       # b0 == a1 (shared small coordinate)
        a_first.append(a0)
        c_third.append(a2)     # a2 == b1 == c
    print(f"\nbranch pattern of (x_i,x_i+1) in size-2 clusters: {dict(branch_pat)}")
    print(f"branch of x_i+2 (third point): {dict(third_branch)}")
    b_mid = np.array(b_mid); a_first = np.array(a_first); c_third = np.array(c_third)
    print(f"\nshared middle coord b: min={b_mid.min():.4f} max={b_mid.max():.6f} "
          f"mean={b_mid.mean():.4f}")
    print(f"  sqrt2/4={LAM/4:.6f}  1/sqrt12={1/math.sqrt(12):.6f}  1-sqrt2/2={1-LAM/2:.6f}")
    print(f"first coord a (x_i.1): min={a_first.min():.6f} max={a_first.max():.4f}")
    print(f"third's large coord c: min={c_third.min():.6f} max={c_third.max():.4f}")

    # ---- k / ell statistics ----
    print("\n[k/ell statistics over size-2 clusters]")
    krecs = cluster_k_stats()
    from collections import Counter
    kc = Counter(); ellc = Counter(); tb = Counter()
    bmax_by_k = {}
    for (p0, p1, p2) in krecs:
        a0,b0,i0,pp0,k0 = p0
        a1,b1,i1,pp1,k1 = p1   # k1 = ell (second step)
        a2,b2,i2,pp2,k2 = p2
        kc[k0]+=1; ellc[k1]+=1; tb[i2]+=1
        bmax_by_k[k0] = max(bmax_by_k.get(k0,0), b0)
    print(f"  #clusters={len(krecs)}")
    print(f"  k (first step x_i->x_i+1) distribution: {dict(sorted(kc.items()))}")
    print(f"  ell (second step x_i+1->x_i+2) distribution: {dict(sorted(ellc.items()))}")
    print(f"  third-point branch: {dict(tb)}")
    print(f"  max b observed per k value: { {k: round(v,5) for k,v in sorted(bmax_by_k.items())} }")
    print(f"  -> if min k>=2 in clusters, then b^2<1/(4k)<=1/8 => b<sqrt2/4 => c>1/2 => cd>X")
