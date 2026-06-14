"""
Target a >=58-line system in R^18 at 1/5 (a real lower-bound improvement).

Reformulation: an n-line system at 1/5 from norm-10 / +-2 vectors is exactly a
CLIQUE of size n in the graph on norm-10 vectors with edges = (inner product +-2),
restricted to a linearly-independent-spanning-18 set (rank 18 is automatic once
we have >=18 independent vectors all pairwise +-2 -- the Gram of a clique has
smallest eigenvalue -5 with the right multiplicity iff it spans <=18 dims).

We:
  pick v1, compute L1 (one stream),
  build the +-2 graph on a manageable subset reachable from v1 (= L1 itself is
  already all +-2 with v1; we want a large clique in L1's induced +-2 graph that
  includes v1),
  run aggressive tabu max-clique aiming for clique size 58 (incl v1).
On success we verify rank 18 and dump.  (Empirically clique 57 was reachable;
we push for 58.)
"""
import sys, random, itertools, json, time
import numpy as np
from itertools import combinations, product

DIM = 18; IP = 2


def gen_L0_stream():
    n = DIM
    patterns = [[3, 1], [2, 2, 1, 1], [2, 1, 1, 1, 1, 1, 1], [1]*10]
    for pat in patterns:
        k = len(pat)
        perms = set(itertools.permutations(pat))
        for positions in combinations(range(n), k):
            for perm in perms:
                for signs in product((1, -1), repeat=k):
                    v = [0]*n
                    for idx, p, s in zip(positions, perm, signs):
                        v[idx] = p*s
                    yield v


def random_norm10(rng):
    n = DIM
    pats = [[3, 1], [2, 2, 1, 1], [2, 1, 1, 1, 1, 1, 1], [1]*10]
    weights = [1224, 293760, 28514304, 44808192]
    pat = rng.choices(pats, weights=weights)[0]
    k = len(pat)
    positions = rng.sample(range(n), k)
    perm = list(pat); rng.shuffle(perm)
    v = [0]*n
    for idx, p in zip(positions, perm):
        v[idx] = p * rng.choice((1, -1))
    return v


def L1_from_v1(v1):
    v1 = list(v1); res = []
    for v in gen_L0_stream():
        s = 0
        for a, b in zip(v, v1):
            s += a*b
        if s == IP or s == -IP:
            res.append(v)
    return np.array(res, dtype=np.int16)


def tabu_clique(adj, time_limit, target, rng):
    n = adj.shape[0]
    nbr = [np.nonzero(adj[i])[0] for i in range(n)]
    best = []
    t0 = time.time()
    while time.time() - t0 < time_limit:
        start = rng.randrange(n)
        clique = [start]; cset = {start}
        cand = set(nbr[start].tolist())
        while cand:
            if len(cand) > 80:
                v = rng.choice(tuple(cand))
            else:
                v = max(cand, key=lambda u: sum(1 for w in cand if adj[u, w]))
            clique.append(v); cset.add(v)
            cand &= set(nbr[v].tolist())
        # plateau + (1,2)-swaps
        stall = 0
        while stall < 200 and time.time() - t0 < time_limit:
            added = False
            for u in range(n):
                if u not in cset and all(adj[u, c] for c in clique):
                    clique.append(u); cset.add(u); added = True
            if added:
                stall = 0; continue
            if len(clique) < 1:
                break
            rem = rng.choice(clique)
            trial = [c for c in clique if c != rem]; tset = set(trial)
            adds = [u for u in range(n) if u not in tset
                    and all(adj[u, c] for c in trial)]
            if len(adds) >= 2:
                rng.shuffle(adds)
                for u in adds:
                    if all(adj[u, c] for c in trial):
                        trial.append(u); tset.add(u)
                if len(trial) > len(clique):
                    clique = trial; cset = tset; stall = 0; continue
            stall += 1
        if len(clique) > len(best):
            best = clique[:]
            print(f"  clique improved to {len(best)} (t={time.time()-t0:.0f}s)", flush=True)
            if len(best) >= target:
                return best
    return best


def grow_basis_then_survivors(L1, v1arr, rng, basis_pick=14):
    """Grow `basis_pick` more vectors inside L1 (all mutually ±2) to shrink the
    survivor set to a manageable size, then return (chosen_basis, survivors).
    Picking fewer than 17 leaves a larger survivor pool (bigger clique room) but
    still small enough to build the induced graph.  We pick until survivors fit
    in memory (<= ~6000) AND we have >= 0 basis."""
    chosen = [v1arr.copy()]
    work = L1
    # pick basis vectors until survivors are small enough OR we hit DIM-1
    while work.shape[0] > 6000 and len(chosen) < DIM:
        i = rng.randrange(work.shape[0]); v = work[i]
        chosen.append(v.copy())
        dots = work.astype(np.int32) @ v.astype(np.int32)
        work = work[np.abs(dots) == IP]
        if work.shape[0] == 0:
            return chosen, work
    return chosen, work


def run(seed, wall, target):
    rng = random.Random(seed)
    t0 = time.time()
    best_overall = 0
    while time.time() - t0 < wall:
        v1 = random_norm10(rng)
        L1 = L1_from_v1(v1)
        v1arr = np.array(v1, dtype=np.int16)
        # many attempts reuse this L1
        for _att in range(40):
            if time.time() - t0 >= wall:
                break
            chosen, work = grow_basis_then_survivors(L1, v1arr, rng)
            if work.shape[0] == 0:
                continue
            # build induced ±2 graph on the (small) survivor set
            s32 = work.astype(np.int32)
            Gm = s32 @ s32.T; np.fill_diagonal(Gm, 0)
            adj = (np.abs(Gm) == IP)
            # the chosen basis vectors are all mutually ±2 and ±2 with every
            # survivor, so total system = chosen + (clique in survivors).
            need = target - len(chosen)
            remaining = wall - (time.time() - t0)
            clique = tabu_clique(adj, min(remaining, 60), need, rng)
            total = len(chosen) + len(clique)
            if total > best_overall:
                best_overall = total
                print(f"seed {seed}: best total={total} (basis {len(chosen)} + clique {len(clique)}, |surv|={work.shape[0]})", flush=True)
            if total >= target:
                vecs = [list(map(int, c)) for c in chosen] + \
                       [list(map(int, work[i])) for i in clique]
                M = np.array(vecs, float)
                rk = np.linalg.matrix_rank(M)
                if rk <= DIM:
                    fn = f"sys58_seed{seed}_n{total}.json"
                    json.dump(vecs, open(fn, "w"))
                    print(f"seed {seed}: SUCCESS total={total} rank={rk} WROTE {fn}", flush=True)
                    return total
                else:
                    print(f"seed {seed}: total={total} rank {rk}>18 reject", flush=True)
    print(f"seed {seed}: done best={best_overall}", flush=True)
    return best_overall


if __name__ == "__main__":
    seed = int(sys.argv[1]); wall = float(sys.argv[2]); target = int(sys.argv[3])
    run(seed, wall, target)
