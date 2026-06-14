"""
Reproduce a 57-line equiangular system in R^18 at angle 1/5, following the
published recipe of Greaves-Syatriadi-Yatsyna 2021 (arXiv:2104.04330, Sec 2):

  L0 = { v in Z^18 : <v,v> = 10 }   (|L0| = 36,808,740)
  Pick v1 in L0; L1 = { v in L0 : <v,v1> = +-2 }.
  Pick v2 in L1; L2 = { v in L1 : <v,v2> = +-2 }.  ... repeat to v1..v18.
  If v1..v18 linearly independent, form graph G on L18 with v~w iff <v,w>=+-2.
  v1..v18 together with a clique in G span an equiangular system in R^18.
  (norm 10, inner products +-2  ->  angle alpha = 2/10 = 1/5.)

We add v1..v18 incrementally (each L_i is intersected), which keeps the surviving
set small fast.  We then greedily/branch grow a clique to reach 57 vectors total.

This is a randomized search; a single successful run yields a self-certifying
exact 57-line Gram matrix (verified separately by eqlines.verify_equiangular_system).
"""
import sys, random, itertools, json, time
import numpy as np

DIM = 18
NORM2 = 10
IP = 2  # |inner product|


def gen_L0():
    """All integer vectors of squared norm 10 in Z^18, up to we keep all.
    Norm-10 partitions into squares using entries in {0,+-1,+-2,+-3}:
      10 = 3^2+1^2  (1 three, 1 one)
      10 = 2^2+2^2+1^2+1^2  (2 twos, 2 ones)
      10 = 2^2+1^2*6        (1 two, 6 ones)
      10 = 1^2*10           (10 ones)
    Generate all sign/position choices.  This is 36,808,740 vectors total.
    We yield them as tuples.
    """
    n = DIM
    from itertools import combinations, product
    # pattern: multiset of absolute values (nonzero), then place & sign
    # abs-value multisets summing of squares to 10:
    patterns = [
        [3,1],
        [2,2,1,1],
        [2,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1],
    ]
    for pat in patterns:
        k = len(pat)
        # distinct value groups for placement count (positions are labeled)
        for positions in combinations(range(n), k):
            # assign the multiset pat to these k positions: all distinct
            # orderings of pat over positions
            seen = set()
            for perm in set(itertools.permutations(pat)):
                # signs
                for signs in product((1,-1), repeat=k):
                    v = [0]*n
                    for idx, p, s in zip(positions, perm, signs):
                        v[idx] = p*s
                    yield tuple(v)


def count_L0():
    c = 0
    for _ in gen_L0():
        c += 1
    return c


def ip(a, b):
    return sum(x*y for x, y in zip(a, b))


def build_one(seed, time_budget=60.0):
    """Run the incremental recipe once; return list of >=57 vectors or None."""
    random.seed(seed)
    t0 = time.time()
    # Materialize L0 once (heavy).  We store as numpy int8 array for speed.
    L0 = np.array([v for v in gen_L0()], dtype=np.int16)
    N0 = L0.shape[0]
    chosen = []
    survivors = L0
    for step in range(DIM):
        if time.time() - t0 > time_budget:
            return None, "timeout-building-basis"
        i = random.randrange(survivors.shape[0])
        v = survivors[i]
        chosen.append(v.copy())
        dots = survivors @ v
        mask = (np.abs(dots) == IP)
        survivors = survivors[mask]
        if survivors.shape[0] == 0 and len(chosen) < DIM:
            return None, f"empty-at-step-{step}"
    # check chosen 18 are independent
    M = np.array(chosen, dtype=float)
    if np.linalg.matrix_rank(M) < DIM:
        return None, "deps"
    # Build graph on survivors (= L18): v~w iff |<v,w>|=2.  Add chosen ∪ clique.
    # All of `chosen` are mutually +-2 by construction; survivors are all +-2
    # with every chosen vector.  Need a clique among survivors.
    surv = survivors
    if surv.shape[0] == 0:
        return chosen, "only-basis-18"
    # adjacency among survivors
    G = surv @ surv.T
    np.fill_diagonal(G, 0)
    adj = (np.abs(G) == IP)
    # greedy max clique (randomized restarts) among survivors
    best_clique = greedy_clique(adj, surv.shape[0], random)
    full = list(chosen) + [surv[i] for i in best_clique]
    return full, f"basis18+clique{len(best_clique)}=total{len(full)}"


def greedy_clique(adj, n, rng, restarts=200):
    best = []
    order = list(range(n))
    for _ in range(restarts):
        rng.shuffle(order)
        clique = []
        for v in order:
            if all(adj[v, u] for u in clique):
                clique.append(v)
        if len(clique) > len(best):
            best = clique[:]
    return best


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "count"
    if cmd == "count":
        print("Counting |L0| ...", flush=True)
        print("|L0| =", count_L0())
    elif cmd == "build":
        seed = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        budget = float(sys.argv[3]) if len(sys.argv) > 3 else 120.0
        full, info = build_one(seed, budget)
        print("seed", seed, "info", info,
              "total", (len(full) if full else 0), flush=True)
        if full and len(full) >= 57:
            out = [[int(x) for x in v] for v in full]
            with open(f"sys_seed{seed}_n{len(full)}.json", "w") as f:
                json.dump(out, f)
            print("WROTE", f"sys_seed{seed}_n{len(full)}.json", flush=True)
