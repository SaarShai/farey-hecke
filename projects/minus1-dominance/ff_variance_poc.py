#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ff_variance_poc.py -- UNCONDITIONAL function-field (F_q[t]) prime-race variance, and the
-1/variance-ordering question (analogue of Fiorilli-Martin Thm 1.10), tested by BRUTE FORCE.

Framework (exact, function-field explicit formula): for chi mod M,
    a(n;chi) := sum_{f monic, deg f = n} Lambda(f) chi(f) = - sum_j gamma_{j,chi}^n,
with |gamma_{j,chi}| = sqrt q for all inverse zeros (Weil's RH for function fields -- a THEOREM).
Hence the mean-square race amplitude is, UNCONDITIONALLY (no Grand Simplicity / LI needed; that
only governs the limiting *distribution*, not this second moment):
    V_emp(M;a,1) := < |Phi(M) (psi(n;M,a) - psi(n;M,1))|^2 / q^n >_n
                  -> sum_{chi != chi0} |chi(a)-1|^2 N_chi   (N_chi = #zeros of L(u,chi)),
the per-zero weight being UNIFORM (=1), unlike the number field's height weight 1/(1/4+gamma^2).

This script computes V_emp by brute force (counting monic irreducibles by degree & residue mod M)
-- self-validating, hypothesis-free -- for several M, and reports whether a=-1 (the constant -1)
is the variance-MAX non-residue. PREDICTION: for IRREDUCIBLE M every non-principal chi has the
same N_chi = deg M - 1, so V is CONSTANT across non-residues (the FM "-1 special" effect is
ABSENT over prime moduli); any -1 distinction must come from COMPOSITE-M conductor structure.

q must be an odd prime here. STATUS: this V_emp is UNCONDITIONAL (Weil), exact up to the
explicit off-diagonal/resonance terms that average to 0 when Frobenius angles are distinct.
"""
import sys, math
from collections import defaultdict

# ---------------- F_q[t] polynomial arithmetic (coeffs low->high, over F_q) ----------------
def norm(p, q):
    p = [c % q for c in p]
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return tuple(p)

def pdeg(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return -1 if (len(p) == 1 and p[0] == 0) else len(p) - 1

def pmul(a, b, q):
    if (len(a) == 1 and a[0] == 0) or (len(b) == 1 and b[0] == 0):
        return (0,)
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                r[i + j] = (r[i + j] + x * y) % q
    return norm(r, q)

def pmod(a, m, q):
    a = list(norm(a, q)); m = list(norm(m, q))
    dm = len(m) - 1
    inv = pow(m[-1], q - 2, q)
    while len(a) - 1 >= dm and not (len(a) == 1 and a[0] == 0):
        da = len(a) - 1
        coef = (a[-1] * inv) % q
        for i in range(len(m)):
            a[da - dm + i] = (a[da - dm + i] - coef * m[i]) % q
        while len(a) > 1 and a[-1] == 0:
            a.pop()
    return norm(a, q)

def pgcd(a, m, q):
    a = norm(a, q); m = norm(m, q)
    while not (len(m) == 1 and m[0] == 0):
        a, m = m, pmod(a, m, q)
    return a  # not normalized to monic; only emptiness/degree matters

def is_unit_modM(a, M, q):
    g = pgcd(a, M, q)
    return pdeg(g) == 0  # gcd is a nonzero constant

# ---------------- enumerate monic polynomials & monic irreducibles up to degree N ----------
def monic_polys_of_deg(n, q):
    if n == 0:
        yield (1,)
        return
    # coeffs c0..c_{n-1} free in F_q, c_n=1
    from itertools import product
    for tail in product(range(q), repeat=n):
        yield norm(tuple(tail) + (1,), q)

def sieve_irreducibles(N, q):
    """Return dict deg -> list of monic irreducible polys of that degree, for deg 1..N."""
    irr = {d: [] for d in range(1, N + 1)}
    lowers = []  # all monic irreducibles found so far (deg < current)
    for d in range(1, N + 1):
        for f in monic_polys_of_deg(d, q):
            # test irreducible: not divisible by any monic irreducible of deg <= d//2
            ok = True
            for g in lowers:
                if pdeg(g) > d // 2:
                    break
                if pdeg(pmod(f, g, q)) == -1:  # g | f
                    ok = False
                    break
            if ok:
                irr[d].append(f)
        lowers.extend(irr[d])
        lowers.sort(key=pdeg)
    return irr

# ---------------- residue helpers ----------------
def residues_coprime(M, q):
    """All residues r (deg < deg M) coprime to M = units of A/M."""
    from itertools import product
    dM = pdeg(M)
    U = []
    for coeffs in product(range(q), repeat=dM):
        r = norm(tuple(coeffs), q)
        if not (len(r) == 1 and r[0] == 0) and is_unit_modM(r, M, q):
            U.append(r)
    return U

def squares_modM(U, M, q):
    sq = set()
    for u in U:
        sq.add(pmod(pmul(u, u, q), M, q))
    return sq

# ---------------- main PoC for a given M ----------------
def analyze_M(M, q, N, label, irr):
    dM = pdeg(M)
    U = residues_coprime(M, q)
    Phi = len(U)
    sq = squares_modM(U, M, q)
    NR = [u for u in U if u not in sq]
    minus1 = norm((q - 1,), q)  # constant -1
    one = (1,)
    # psi(n; M, r) = sum_{f monic, deg f = n} Lambda(f) [f == r mod M], Lambda(P^k)=deg P
    psi = {n: defaultdict(int) for n in range(1, N + 1)}
    for dP, plist in irr.items():
        for P in plist:
            # prime powers P^k with deg = k*dP <= N
            Pk = (1,)
            k = 0
            while True:
                k += 1
                Pk = pmul(Pk, P, q)
                n = k * dP
                if n > N:
                    break
                r = pmod(Pk, M, q)
                psi[n][r] += dP  # Lambda(P^k) = deg P
    # V_emp(a) = mean over n of |Phi*(psi(n,a)-psi(n,1))|^2 / q^n   (skip very small n)
    n0 = max(1, dM)  # start past trivial low-degree regime
    Vemp = {}
    for a in U:
        if a == one:
            continue
        s = 0.0; cnt = 0
        for n in range(n0, N + 1):
            D = psi[n].get(a, 0) - psi[n].get(one, 0)
            s += (Phi * D) ** 2 / (q ** n)
            cnt += 1
        Vemp[a] = s / cnt
    # rank non-residues by V_emp
    NRsorted = sorted(NR, key=lambda a: -Vemp[a])
    is_m1_nr = minus1 in NR
    print(f"\n=== {label}: q={q}, M={M} (deg {dM}), Phi={Phi}, #NR={len(NR)}, N={N} ===")
    print(f"    -1 = {minus1}; is -1 a non-residue? {is_m1_nr}")
    spread = (max(Vemp.values()) - min(Vemp.values())) / (sum(Vemp.values())/len(Vemp))
    print(f"    V_emp spread (max-min)/mean over ALL units a!=1 = {spread:.4f}  "
          f"({'~DEGENERATE (all equal)' if spread < 0.05 else 'NON-degenerate'})")
    if is_m1_nr:
        rank = NRsorted.index(minus1) + 1
        print(f"    among non-residues: V_emp(-1)={Vemp[minus1]:.3f}, rank {rank}/{len(NR)} "
              f"(1=max)  argmax a={NRsorted[0]} V={Vemp[NRsorted[0]]:.3f}")
        print(f"    -> a=-1 is {'the variance-MAX NR' if rank==1 else 'NOT max (rank %d)'%rank}")
    # show the NR variance values (rounded) to see degeneracy/structure
    print("    V_emp over non-residues:", {a: round(Vemp[a], 2) for a in NRsorted})
    return Vemp, NR, minus1

if __name__ == "__main__":
    q = 3
    N = 12   # max degree enumerated; sieve ONCE, reused across all M
    print(f"Function-field prime-race variance PoC over F_{q}[t], brute force to degree {N}.")
    print("PREDICTION: irreducible M -> V constant across NR (no -1 effect); composite M -> structure.")
    import time; t0 = time.time()
    irr = sieve_irreducibles(N, q)
    print(f"[sieve] irreducibles to deg {N} in {time.time()-t0:.1f}s; "
          f"counts/deg = {{{', '.join(str(d)+':'+str(len(irr[d])) for d in irr)}}}")
    t = (0, 1)
    tm1 = norm((q - 1, 1), q)   # t - 1
    tp1 = norm((1, 1), q)       # t + 1 = t - 2 over F_3
    analyze_M(norm((1, 0, 1), q), q, N, "A: irreducible deg-2  t^2+1", irr)
    analyze_M(norm((1, 2, 0, 1), q), q, N, "B: irreducible deg-3  t^3+2t+1", irr)
    analyze_M(pmul(t, tm1, q), q, N, "C: composite  t(t-1)", irr)
    analyze_M(pmul(pmul(t, tm1, q), tp1, q), q, N, "D: composite  t(t-1)(t+1)", irr)
    P = norm((1, 0, 1), q)
    analyze_M(pmul(P, P, q), q, N, "E: prime-power  (t^2+1)^2", irr)
