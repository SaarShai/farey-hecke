"""
Memory-efficient reproduction of a 57-line equiangular system in R^18 at 1/5.
Recipe: Greaves-Syatriadi-Yatsyna 2021 (arXiv:2104.04330, Sec 2).

We avoid materializing all 73.6M norm-10 vectors.  Instead:
  - pick random v1 (from a small sampled pool of norm-10 vectors),
  - STREAM generate L0 once, keep only L1 = {v : <v,v1> = +-2}  (much smaller),
  - thereafter intersect within the in-memory survivor array (fast).
Then grow basis v1..v18 and a clique among final survivors.

Outputs an exact integer 57x18 system as JSON on success.
"""
import sys, random, itertools, json, time
import numpy as np
from itertools import combinations, product

DIM = 18
NORM2 = 10
IP = 2


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


def random_norm10(rng, count):
    """Sample `count` random norm-10 vectors (rejection over patterns)."""
    n = DIM
    pats = [[3, 1], [2, 2, 1, 1], [2, 1, 1, 1, 1, 1, 1], [1]*10]
    weights = [1224, 293760, 28514304, 44808192]
    out = []
    for _ in range(count):
        pat = rng.choices(pats, weights=weights)[0]
        k = len(pat)
        positions = rng.sample(range(n), k)
        perm = list(pat); rng.shuffle(perm)
        v = [0]*n
        for idx, p in zip(positions, perm):
            v[idx] = p * rng.choice((1, -1))
        out.append(v)
    return out


def L1_from_v1(v1):
    """Stream L0 and collect all v with <v,v1> = +-2."""
    v1 = list(v1)
    res = []
    for v in gen_L0_stream():
        s = 0
        for a, b in zip(v, v1):
            s += a*b
        if s == IP or s == -IP:
            res.append(v)
    return np.array(res, dtype=np.int16)


def greedy_clique(adj, n, rng, restarts=400):
    best = []
    order = list(range(n))
    for _ in range(restarts):
        rng.shuffle(order)
        clique = []
        for v in order:
            ok = True
            for u in clique:
                if not adj[v, u]:
                    ok = False
                    break
            if ok:
                clique.append(v)
        if len(clique) > len(best):
            best = clique[:]
    return best


def run(seed, time_budget=600.0, target=57):
    rng = random.Random(seed)
    t0 = time.time()
    v1 = random_norm10(rng, 1)[0]
    survivors = L1_from_v1(v1)          # all v with <v,v1>=+-2
    chosen = [np.array(v1, dtype=np.int16)]
    # incremental basis growth
    while len(chosen) < DIM:
        if time.time() - t0 > time_budget:
            return None, "timeout-basis", None
        if survivors.shape[0] == 0:
            return None, f"empty-basis-at-{len(chosen)}", None
        i = rng.randrange(survivors.shape[0])
        v = survivors[i]
        chosen.append(v.copy())
        dots = survivors.astype(np.int32) @ v.astype(np.int32)
        survivors = survivors[np.abs(dots) == IP]
    M = np.array(chosen, dtype=float)
    if np.linalg.matrix_rank(M) < DIM:
        return None, "deps", None
    if survivors.shape[0] == 0:
        return chosen, "only-basis-18", 18
    # clique among survivors
    surv32 = survivors.astype(np.int32)
    Gm = surv32 @ surv32.T
    np.fill_diagonal(Gm, 0)
    adj = (np.abs(Gm) == IP)
    clique = greedy_clique(adj, survivors.shape[0], rng)
    full = list(chosen) + [survivors[i] for i in clique]
    total = len(full)
    info = f"basis18+clique{len(clique)}=total{total}  |L1|={len(L1cache(survivors))}"
    if total >= target:
        out = [[int(x) for x in v] for v in full]
        fn = f"sys_seed{seed}_n{total}.json"
        with open(fn, "w") as f:
            json.dump(out, f)
        return full, f"basis18+clique{len(clique)}=total{total} WROTE {fn}", total
    return full, f"basis18+clique{len(clique)}=total{total}", total


def L1cache(x):
    return x


if __name__ == "__main__":
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    budget = float(sys.argv[2]) if len(sys.argv) > 2 else 600.0
    target = int(sys.argv[3]) if len(sys.argv) > 3 else 57
    full, info, total = run(seed, budget, target)
    print(f"seed {seed}: {info}", flush=True)
