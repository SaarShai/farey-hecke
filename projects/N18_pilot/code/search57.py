"""
Stronger / parallel search for a >=57-line equiangular system in R^18 at 1/5.
Recipe per Greaves-Syatriadi-Yatsyna 2021 (arXiv:2104.04330, Sec 2).

Speed ideas:
  * For a fixed v1, L1 = {v: <v,v1>=+-2} is computed ONCE (the only stream over
    the 73.6M norm-10 vectors).  Then MANY basis/clique attempts reuse L1.
  * Basis growth picks v2..v18 inside the shrinking survivor set (cheap int dot).
  * Clique search on final survivors: randomized greedy + tabu local swaps.
Run:  python3 search57.py <seed> <wall_seconds> <target> <attempts_per_v1>
Writes sys_seed<seed>_n<total>.json on first success at >= target.
"""
import sys, random, itertools, json, time
import numpy as np
from itertools import combinations, product

DIM = 18; NORM2 = 10; IP = 2


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


def clique_search(adj, n, rng, restarts, swap_iters):
    """Randomized greedy + simple plateau local search for a large clique."""
    best = []
    order = list(range(n))
    for _ in range(restarts):
        rng.shuffle(order)
        clique = []
        inclq = np.zeros(n, dtype=bool)
        for v in order:
            if adj[v, clique].all() if clique else True:
                clique.append(v); inclq[v] = True
        # local swap improvement: try (1,2)-swaps to grow
        for _ in range(swap_iters):
            improved = False
            # candidate additions: vertices adjacent to all clique
            cand = [u for u in range(n) if not inclq[u] and adj[u, clique].all()]
            if cand:
                u = rng.choice(cand)
                clique.append(u); inclq[u] = True; improved = True
            if not improved:
                break
        if len(clique) > len(best):
            best = clique[:]
    return best


def attempt_from_L1(L1, rng, target):
    survivors = L1.copy()
    # need a starting vector for the basis: it's v1 (already used) + grow inside L1
    chosen = []
    # NOTE: v1 is implicit; the survivors L1 are all <.,v1>=+-2, and v1 itself is
    # mutually +-2 with all of L1.  We grow 17 more inside L1 to complete basis.
    work = survivors
    while len(chosen) < DIM - 1:
        if work.shape[0] == 0:
            return None
        i = rng.randrange(work.shape[0])
        v = work[i]; chosen.append(v.copy())
        dots = work.astype(np.int32) @ v.astype(np.int32)
        work = work[np.abs(dots) == IP]
    # work = final survivors compatible with all of chosen (and v1)
    if work.shape[0] == 0:
        return ("basis-only", DIM, None)
    surv32 = work.astype(np.int32)
    Gm = surv32 @ surv32.T
    np.fill_diagonal(Gm, 0)
    adj = (np.abs(Gm) == IP)
    clique = clique_search(adj, work.shape[0], rng, restarts=300, swap_iters=40)
    total = 1 + len(chosen) + len(clique)   # v1 + 17 + clique
    return (clique, total, work)


def run(seed, wall, target, attempts_per_v1):
    rng = random.Random(seed)
    t0 = time.time()
    best_total = 0
    while time.time() - t0 < wall:
        v1 = random_norm10(rng)
        L1 = L1_from_v1(v1)            # expensive: one stream
        v1arr = np.array(v1, dtype=np.int16)
        for _ in range(attempts_per_v1):
            if time.time() - t0 >= wall:
                break
            r = attempt_from_L1(L1, rng, target)
            if r is None:
                continue
            clique, total, work = r
            if total > best_total:
                best_total = total
                print(f"seed {seed}: new best total={total} (t={time.time()-t0:.0f}s)", flush=True)
            if total >= target and isinstance(clique, list):
                # reconstruct full vector list: v1 + the 17 basis + clique vectors
                # we must recover the 17 basis vectors; re-run deterministically is
                # messy, so rebuild here by repeating with same rng path is hard.
                # Instead: we recorded 'work' (final survivors) and clique indices,
                # but lost the 17 basis vecs.  Patch: redo attempt capturing them.
                full = reconstruct(L1, v1arr, target, rng)
                if full is not None and len(full) >= target:
                    out = [[int(x) for x in v] for v in full]
                    fn = f"sys_seed{seed}_n{len(full)}.json"
                    with open(fn, "w") as f:
                        json.dump(out, f)
                    print(f"seed {seed}: SUCCESS total={len(full)} WROTE {fn}", flush=True)
                    return len(full)
    print(f"seed {seed}: done best_total={best_total}", flush=True)
    return best_total


def reconstruct(L1, v1arr, target, rng):
    """Repeat one attempt but keep ALL vectors so we can dump a full system."""
    for _try in range(2000):
        work = L1.copy(); chosen = [v1arr.copy()]
        ok = True
        while len(chosen) < DIM:
            if work.shape[0] == 0:
                ok = False; break
            i = rng.randrange(work.shape[0]); v = work[i]
            chosen.append(v.copy())
            dots = work.astype(np.int32) @ v.astype(np.int32)
            work = work[np.abs(dots) == IP]
        if not ok or np.linalg.matrix_rank(np.array(chosen, float)) < DIM:
            continue
        if work.shape[0] == 0:
            continue
        s32 = work.astype(np.int32); Gm = s32 @ s32.T
        np.fill_diagonal(Gm, 0); adj = (np.abs(Gm) == IP)
        clique = clique_search(adj, work.shape[0], rng, restarts=600, swap_iters=60)
        full = list(chosen) + [work[i] for i in clique]
        if len(full) >= target:
            return full
    return None


if __name__ == "__main__":
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    wall = float(sys.argv[2]) if len(sys.argv) > 2 else 600.0
    target = int(sys.argv[3]) if len(sys.argv) > 3 else 57
    apv = int(sys.argv[4]) if len(sys.argv) > 4 else 30
    run(seed, wall, target, apv)
