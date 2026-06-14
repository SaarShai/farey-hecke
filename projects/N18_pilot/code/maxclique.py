"""
Stronger max-clique routines for the R^18 / norm-10 survivor graphs.
- nx_max_clique: exact-ish via networkx find_cliques (Bron-Kerbosch) with cutoff.
- tabu_clique: aggressive randomized tabu local search.
The goal: find a clique of size >=39 in a survivor graph (=> total 57 lines)
or report the true maximum if small enough to enumerate.
"""
import numpy as np
import random


def tabu_clique(adj, time_limit=30.0, target=None, seed=0):
    """Randomized multistart + plateau/tabu local search for a large clique."""
    import time
    rng = random.Random(seed)
    n = adj.shape[0]
    nbr = [np.nonzero(adj[i])[0] for i in range(n)]
    best = []
    t0 = time.time()
    while time.time() - t0 < time_limit:
        # random greedy seed
        start = rng.randrange(n)
        clique = [start]
        cset = {start}
        # candidate set = common neighbors
        cand = set(nbr[start].tolist())
        while cand:
            # pick candidate with most connections to other candidates (greedy)
            if len(cand) > 60:
                v = rng.choice(tuple(cand))
            else:
                v = max(cand, key=lambda u: sum(1 for w in cand if adj[u, w]))
            clique.append(v); cset.add(v)
            cand &= set(nbr[v].tolist())
        # plateau search: drop 1, add 2 cycles
        for _ in range(4000):
            if time.time() - t0 >= time_limit:
                break
            # try to add any vertex adjacent to all
            added = False
            for u in range(n):
                if u in cset:
                    continue
                if all(adj[u, c] for c in clique):
                    clique.append(u); cset.add(u); added = True
            if added:
                continue
            # (1,k)-swap: remove a random member, see if we can add >=2
            if len(clique) < 2:
                break
            rem = rng.choice(clique)
            trial = [c for c in clique if c != rem]
            tset = set(trial)
            adds = [u for u in range(n) if u not in tset
                    and all(adj[u, c] for c in trial)]
            if len(adds) >= 2:
                rng.shuffle(adds)
                trial2 = trial[:]
                t2set = set(trial2)
                for u in adds:
                    if all(adj[u, c] for c in trial2):
                        trial2.append(u); t2set.add(u)
                if len(trial2) > len(clique):
                    clique = trial2; cset = t2set
                    continue
            break
        if len(clique) > len(best):
            best = clique[:]
            if target and len(best) >= target:
                return best
    return best


def nx_max_clique(adj, time_limit=60.0, target=None):
    """Use networkx Bron-Kerbosch to enumerate cliques; stop at target or time."""
    import time, networkx as nx
    n = adj.shape[0]
    G = nx.Graph()
    G.add_nodes_from(range(n))
    ii, jj = np.nonzero(np.triu(adj, 1))
    G.add_edges_from(zip(ii.tolist(), jj.tolist()))
    best = []
    t0 = time.time()
    for clq in nx.find_cliques(G):
        if len(clq) > len(best):
            best = clq
            if target and len(best) >= target:
                return best
        if time.time() - t0 > time_limit:
            break
    return best


if __name__ == "__main__":
    import sys
    adj = np.load("surv_adj.npy")
    print("graph n=", adj.shape[0], "density",
          adj.sum()/(adj.shape[0]*(adj.shape[0]-1)))
    print("tabu (60s)...", flush=True)
    c = tabu_clique(adj, time_limit=60.0, target=39, seed=1)
    print("tabu best clique:", len(c))
    print("nx find_cliques (60s)...", flush=True)
    c2 = nx_max_clique(adj, time_limit=60.0, target=39)
    print("nx best clique:", len(c2))
