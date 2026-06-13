"""
goal1_last_branch_ceiling.py — LAST-BRANCH cluster ceiling B(q) for the Taha
G_q-BCZ map.  This is the CORRECT counter for the cluster-onset program.

A 'cluster' here = a maximal run of consecutive orbit points that BOTH
  (i) land on the last branch T_{q-1}  (sub == q-1, i.e. a + lam*b > 1), AND
  (ii) have observable P = a*b < X(q).
The run breaks when EITHER P >= X OR the point leaves the last branch.  This is
exactly the object the q=3,4,6 Lean proofs (`cluster_size_le_two_q{3,4,6}`) and
the exact q=5,7 reverse-direction witnesses bound: extremes are confined to the
last branch, where the map is (a,b) -> (b, -a + k*lam*b) and P = a*b.

--------------------------------------------------------------------------------
DISTINCTION from `code/goal1_cluster_ceiling_reconcile.py` (READ THIS):

  reconcile.py counts a CROSS-BRANCH run: condition `P < X` over ALL branches,
  ignoring which branch each point is on.  That over-counts.  At q>=19 it glues
  several genuine last-branch clusters together through short off-last-branch
  excursions (points on T_{q-2}, T_{q-3}, ... that happen to also have P<X),
  producing a spurious jump (a run of length 8 pinned at q=19..24).  The q=19
  "8-run" witness alternates branches T18/T16/T18/T16... with the T16 points
  sitting at razor-thin margins (X-P = +4.4e-5, +3.0e-4) — NOT a last-branch
  cluster.  That inflated the reported growth rate to ~q/3.

  This last-branch counter gives a clean monotone ceiling with slope ~q/6
  (linear-fit slope 0.168), e.g. q=3..24:
     B = 2,2,3,2,3,3,3,3,3,3,4,4,4,4,4,4,5,5,5,5,(5 or 6),6
  q=13->4 and q=19->5 transitions are robust; q=23/24->6 is at the Monte-Carlo
  resolution floor (B(23) flips 5<->6 with sampling depth) and is FRAGILE.

  NOTE: the q=13 VALUE (B=4) is the SAME under both counters — only the *rate*
  was inflated by reconcile.py, not that particular threshold.

  Do NOT assert a closed form (e.g. B = 2 + floor((q-1)/6)) as a law: on q<=24
  it is statistically indistinguishable from sqrt(q)/log(q) and is +1 wrong at
  q=5,23,24.  It is at best the cleanest fit on the bulk q=7..22, not a pinned
  asymptotic.

  What IS clean & verified: the arithmeticity dichotomy B=2 <=> lambda^2 in Z
  <=> q in {3,4,6} (the finite arithmetic Hecke groups, Takeuchi 1977).

X(3)=2/9, X(4)=sqrt2/8, X(q>=5)=1/lam^3.
"""
import math, sys
import numpy as np

rng = np.random.default_rng(20260609)


def lam_of(q):
    return 2.0 * math.cos(math.pi / q)


def Xq(q):
    lam = lam_of(q)
    if q == 3:
        return 2.0 / 9.0
    if q == 4:
        return math.sqrt(2.0) / 8.0
    return 1.0 / lam ** 3


def hecke_w(q):
    lam = lam_of(q)
    w = [(1.0, 0.0)]
    for _ in range(q + 2):
        x, y = w[-1]
        w.append((lam * x - y, x))
    return lam, w


def step(a, b, lam, w, q):
    """Full Taha G_q-BCZ step; returns (a', b', branch i, P = a*wi/yi)."""
    sub = q - 1
    d_prev = w[1][0] * a + w[1][1] * b
    for i in range(2, q):
        di = w[i][0] * a + w[i][1] * b
        if d_prev > 1.0 and di <= 1.0:
            sub = i
            break
        d_prev = di
    wi = w[sub][0] * a + w[sub][1] * b
    wi1 = w[sub + 1][0] * a + w[sub + 1][1] * b
    yi = w[sub][1]
    P = a * wi / yi
    k = math.floor((1.0 - wi1) / (lam * wi))
    return wi, wi1 + k * lam * wi, sub, P


def scan(q, n_steps, n_starts, burn=500):
    """LAST-BRANCH run counter: a run requires both i==(q-1) AND P<X(q)."""
    lam, w = hecke_w(q)
    X = Xq(q)
    best = 0
    hist = {}
    best_seq = None
    for _ in range(n_starts):
        while True:
            a = rng.random(); b = rng.random()
            if 0 < a <= 1 and (1 - lam * a) < b <= 1:
                break
        for _ in range(burn):
            a, b, _, _ = step(a, b, lam, w, q)
        cur = 0
        cseq = []
        for _ in range(n_steps):
            ao, bo = a, b
            a, b, i, P = step(a, b, lam, w, q)
            if i == (q - 1) and P < X:           # <-- last-branch AND sub-X
                cur += 1
                cseq.append((ao, bo, i, P))
            else:
                if cur > 0:
                    hist[cur] = hist.get(cur, 0) + 1
                    if cur > best:
                        best = cur; best_seq = cseq[:]
                cur = 0
                cseq = []
        if cur > 0:
            hist[cur] = hist.get(cur, 0) + 1
            if cur > best:
                best = cur; best_seq = cseq[:]
    return best, hist, X, lam, best_seq


if __name__ == "__main__":
    qmax = int(sys.argv[1]) if len(sys.argv) > 1 else 24
    NS = int(sys.argv[2]) if len(sys.argv) > 2 else 16
    NT = int(sys.argv[3]) if len(sys.argv) > 3 else 200_000
    print(f"LAST-BRANCH cluster ceiling (n_starts={NS} n_steps={NT})")
    print(f"{'q':>2} {'lam':>8} {'X':>9} {'B_lastbr':>8}  hist")
    for q in range(3, qmax + 1):
        b, h, X, lam, _ = scan(q, NT, NS)
        hs = " ".join(f"{k}:{v}" for k, v in sorted(h.items()))
        print(f"{q:>2} {lam:8.5f} {X:9.6f} {b:8d}  [{hs}]")
        sys.stdout.flush()
